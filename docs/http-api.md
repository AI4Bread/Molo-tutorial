# HTTP API

This page describes the **current authenticated FastAPI API**. The
[R function reference](api.md) instead describes R functions. Legacy page names
differ between publishing targets; this page is HTTP on both.
All mounted routes, declared form arguments, and JSON models are listed in
[Complete HTTP routes](reference/http-routes.md).

## Session authentication

Use a session cookie and keep one application hostname throughout a workflow.
Registration and password reset use emailed codes; normal job submission does
not require a new email verification code. Do not use the obsolete
`/api/email-verifications` route.

| Route | Body/behavior |
| --- | --- |
| `POST /api/auth/register/start` | JSON: `username`, `email`, `password`, `password_confirm` |
| `POST /api/auth/register/complete` | JSON: `challenge_id`, `email`, `code`; establishes session |
| `POST /auth/login` | Form: `identity`, `password`, optional `next_url`; sets cookie and redirects |
| `POST /auth/logout` | Deletes session and clears cookie |
| `GET /api/auth/me` | Current authenticated account |
| `POST /api/auth/password-reset/start` | JSON: `email` |
| `POST /api/auth/password-reset/complete` | JSON: `challenge_id`, `email`, `code`, `password`, `password_confirm` |
| `POST /auth/reviewer-login` | Restricted read-only demonstration when enabled |

Unauthenticated HTML navigation normally redirects to login; API-style requests
may return 401. Account ownership is checked for jobs/projects/datasets. Reviewer
sessions cannot submit analyses or invoke unsafe write methods.

```python
import getpass
import requests

base = "https://molo.ai4bread.com"
session = requests.Session()
response = session.post(
    f"{base}/auth/login",
    data={
        "identity": input("Username or email: ").strip(),
        "password": getpass.getpass("Password: "),
        "next_url": "/jobs",
    },
    allow_redirects=False,
    timeout=30,
)
if response.status_code != 303:
    raise RuntimeError(f"Login failed: HTTP {response.status_code}")
session.get(f"{base}/api/auth/me", timeout=30).raise_for_status()
```

This is a client example, not a request executed by the documentation build.
Never log passwords, verification codes, cookies, or download tokens.

## Submit pairwise alignment/integration

`POST /analyse/alignment/run` accepts form/multipart fields, **not a JSON body**.
Use `mode=align_only` or `integrate`; `sp_alignment=Molo` or `Raw`;
`input_type=upload` or `server`. Server paths require an allowlisted configuration.

```python
from pathlib import Path

archive = Path("pairwise_input.zip")
with archive.open("rb") as handle:
    response = session.post(
        f"{base}/analyse/alignment/run",
        data={
            "mode": "integrate",
            "data_type": "Visium,Visium",
            "sp_alignment": "Molo",
            "input_type": "upload",
            "tune_preset": "default",
        },
        files=[("files", (archive.name, handle, "application/zip"))],
        timeout=120,
    )
response.raise_for_status()
job_id = response.json()["task_id"]
print(job_id)
```

The response reports queued analysis and pending delivery; it does not prove
scientific success. `tune_trials` must match its preset when supplied. Project
and reusable-asset options are `project_id`, repeated `dataset_asset_ids`, and
`dataset_name`. The registered account supplies the result email.

## Submit downstream analysis

`POST /analyse/downstream/{analysis_type}/submit` is also a form endpoint.
`data_source` accepts `upload`, `server`, or `integrated`. Example reusing a
completed integration owned by the current account:

```python
response = session.post(
    f"{base}/analyse/downstream/visium/submit",
    data=[
        ("data_source", "integrated"),
        ("integrated_task_id", job_id),
        ("analysis_steps", "qc"),
        ("analysis_steps", "cluster"),
        ("species", "mouse"),
        ("resolution", "0.5"),
        ("n_neighbors", "30"),
        ("n_feature_min", "2500"),
    ],
    timeout=60,
)
response.raise_for_status()
downstream_job_id = response.json()["task_id"]
```

Run this only **after** the integration is completed and a compatible result is
available; otherwise expect state/ownership/compatibility errors. The example
QC threshold is the handler default, not a validated value for all data.
Optional steps use `go`, `cell_chat`, and `traj`; `qc` is inserted if omitted.
For raw uploads use a `file` multipart field with a ZIP. Reusable inputs also
support `project_id`, `dataset_asset_id`, and `dataset_name`.

## Track and manage jobs

```python
response = session.get(f"{base}/jobs/{job_id}", timeout=30)
response.raise_for_status()
status = response.json()
print(status.get("analysis_status"), status.get("package_status"), status.get("delivery_status"))
```

| Operation | Endpoint |
| --- | --- |
| Job details | `GET /jobs/{job_id}` |
| Cancel | `POST /jobs/{job_id}/cancel` |
| Retry | `POST /jobs/{job_id}/retry` |
| Clone | `POST /jobs/{job_id}/clone` |
| Editable clone template | `GET /jobs/{job_id}/clone-template` |
| Resend result email | `POST /jobs/{job_id}/resend-email` |
| Secure result download | `GET /results/download/{token}` |

Actions depend on ownership and job state. Repeated POSTs can create work or send
mail; do not use them as health probes. A download GET may update a counter.

## Projects, datasets, and analysis chains

Use `/api/projects` and `/api/datasets` for account-scoped project/asset records.
Dataset upload uses multipart at `/api/datasets/uploads`, and validation uses
`POST /api/datasets/{asset_id}/validate`. JSON payload models and route arguments
are in the [generated reference](reference/http-routes.md).

Analysis provenance can be queried through:

- `GET /chains/job/{job_id}`
- `GET /chains/asset/{asset_id}`
- `GET /chains/project/{project_id}`

## Health and common errors

`GET /health/live` reports the process is alive. `GET /health/ready` separately
checks database, Redis, disk space, and configuration. Neither proves a scientific
task or SMTP delivery succeeded.

| HTTP status | Common interpretation |
| --- | --- |
| 401 / login redirect | Missing/expired authenticated session |
| 403 | Reviewer write restriction, disabled server path, or disallowed root |
| 404 | Missing or inaccessible job/asset; avoid inferring another user's data |
| 409 | Input/result not ready or invalid action state |
| 413 | Upload size/file-count limits |
| 422 | Unsupported parameters, invalid input, or rejected archive/asset |
| 429 | Queue/rate limit reached |
| 503 | Required service/configuration temporarily unavailable |

Inspect the specific response and job state. Do not blindly resubmit an existing job.
