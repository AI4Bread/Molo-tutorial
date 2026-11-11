# Server deployment

This guide is for maintainers. Hosted users should start with [Web workflow](web.md).
Paths below are **portable examples**, not the audited server's private settings.
No deployment commands are executed by the documentation build.

## Components and queues

| Component | Role | Template concurrency |
| --- | --- | --- |
| Redis | Broker and result backend; loopback only, durable persistence | N/A |
| SQLite WAL | Accounts, sessions, jobs, projects, dataset records | N/A |
| Web | `uvicorn app.main:app` behind HTTPS proxy | 2 |
| `analysis` worker | Downstream orchestration | 3 |
| `alignment` worker | Alignment/integration/tuning | 1 |
| `notifications` worker | Auth and result email | 2 |
| `packaging` worker | Safe download packages | 1 |
| `maintenance` worker | Reconciliation and expiry cleanup | 1 |
| Beat | Periodic reconciliation/cleanup publication | Exactly one scheduler |

Use Redis 6.2 or newer; deployment guidance recommends the 7.2 series. Match
version/security requirements to your environment. Do not disable an unrelated
Redis or replace another application's broker.

## Private environment

Create a private, non-committed environment file from the matching source example.
At minimum review:

| Variable | Requirement |
| --- | --- |
| `APP_ENV` | `production` for a public deployment |
| `PUBLIC_BASE_URL` | Canonical public HTTPS origin used by generated emails/download URLs |
| `AUTH_SECRET`, `DOWNLOAD_TOKEN_SECRET` | Independent, non-placeholder secrets at least 32 characters |
| `JOB_DATABASE_PATH` | Persistent writable SQLite database |
| `REDIS_URL`, `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND` | Explicit broker/backend databases on your dedicated Redis |
| `MOLO_VENV` | Correct environment root containing web/worker executables |
| `DOWNSTREAM_CONFIG_PATH` | Absolute path to your validated worker/runtime YAML |
| `MAIL_BACKEND` and SMTP fields | Real encrypted SMTP in production; never publish credentials |
| `MOLO_REVIEW_MODE_ENABLED` | Enable only after real demo artifacts/preflight are available |
| `MOLO_ENABLE_SERVER_PATH_INPUT`, `MOLO_SERVER_PATH_ROOTS` | Disable or tightly allowlist; never expose arbitrary filesystem paths |
| `MOLO_TUNING_ENABLED`, `MOLO_TUNE_MAX_TRIALS` | Search availability and maximum trial count |
| `MAX_UPLOAD_BYTES`, `MAX_ALIGNMENT_UPLOAD_FILES`, `MAX_QUEUED_JOBS` | Resource/admission limits |

Set all Redis variables explicitly. The application fallback for a missing result
backend is `REDIS_URL`; it does not automatically select DB1. Template DB0/DB1 and
a deployment's DB2/DB3 are different intentional configurations.

The parser defaults include 50 queued jobs and a normal analysis limit of 86400
seconds; tuning behavior differs. Upload/proxy limits and available disk must
agree. Do not copy illustrative secrets or public hostnames without setting your own.

## Downstream YAML

Copy `app/config/downstream.example.yaml` from the matching source and edit:

- `project_root`, `molo_source_dir`, `default_output_root`.
- `runtime.alignment_default_device` and `alignment_allowed_devices`.
- Scientific `conda_path`, `rscript`, and applicable `r_lib` values.
- Trajectory environment, ATAC `macs2_env`, worker and orchestrator paths.
- Concurrency, retention, and cleanup scheduling.

The example YAML uses `cuda:0`; the examined R/CLI defaults use `cuda:1`.
These are not interchangeable. Validate process-visible device numbering and
ensure the requested default is in the configured pool.

## Start with supervision

Inspect existing services before starting anything. The source supplies systemd
units using `/opt/molo`, account `molo`, `/etc/molo/molo.env`, and `/var/lib/molo`.
Adapt them to the actual install; do not copy them blindly into a different tree.

Typical order after backups/configuration review:

1. Dedicated persistent Redis.
2. Job/project/dataset schema initialization using the intended database.
3. Required workers on the correct queues.
4. Exactly one Beat scheduler, **only after** retention/reconciliation effects are reviewed.
5. Web and HTTPS proxy, then public routing and health checks.

Schema initialization and reviewer preflight can write databases and demonstration
files. A temporary startup check should not automatically enable expiry cleanup
of historical results. Detached processes do not provide reboot persistence or
restart supervision; install and verify suitable service management for production.

Example web/worker entry points, each in a managed service with the same private
configuration loaded:

```bash
cd /opt/molo/Molo_FastAPI
export MOLO_VENV=/opt/molo/.venv
# Load your reviewed private environment using your service manager.
bash deploy/run-celery-worker.sh analysis
# Other independent service instances: alignment, notifications, packaging, maintenance.
# Web is a separate service:
bash deploy/run-web.sh
```

The scripts use `exec` and run continuously; do not paste all commands into one
foreground terminal expecting them to start sequentially.

## HTTPS, tunnel, and domains

A working SSH tunnel does not prove a working web ingress. Validate each hop:

```text
DNS -> public HTTPS gateway -> web tunnel/network -> private proxy -> 127.0.0.1:8000
```

Use a certificate covering the exact hostname, trusted proxy headers, appropriate
upload/timeouts, and loopback/private upstream binding. A certificate for
`molopipeline.site` does not cover `molo.ai4bread.com`. Two working domains do not
share a login cookie automatically. Configure one canonical `PUBLIC_BASE_URL` for
notifications and protect existing sites when adding a new virtual host.

## Acceptance and backups

```bash
curl --fail https://molo.ai4bread.com/health/live
curl --fail https://molo.ai4bread.com/health/ready
# With the matching scientific environment and private config loaded:
celery -A app.celery_app:celery_app inspect ping
celery -A app.celery_app:celery_app inspect active
celery -A app.celery_app:celery_app inspect reserved
```

Readiness checks database, Redis, disk, and configuration. Separately validate
login, upload, a representative analysis, packaging, authorized download, and
email delivery in an approved isolated run.

Use coordinated backups of SQLite and Redis. Use SQLite's backup mechanism rather
than copying only a live main file without WAL; do not copy a single Redis AOF
segment as if it were the complete broker state. Keep schema/source/configuration
versions together. Use warm worker shutdown and allow sufficient time for tuned
jobs; do not force-kill unrelated scientific processes.
