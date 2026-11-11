# FAQ

## Is this still a Shiny application?

No. The current online application is FastAPI/Celery/Redis with SQLite account
and job state. Historical screenshots and `Molo_web()` instructions describe a
different interface and are not the current deployment procedure.

## Is `/api/` the HTTP API?

It depends on the publishing target: RTD `/api/` is the [R function reference](api.md),
while self-hosted `/en/api/` is HTTP. Use the [HTTP API](http-api.md) link for
web routes and authentication; do not assume identical legacy paths.

## Do I need an email code for every job?

No. Account registration/password reset uses codes; normal submissions use an
authenticated account and its registered email. Do not use obsolete
`/api/email-verifications` examples with the current application.

## Can reviewer mode run a new analysis?

No. It is read-only demonstration access. Submit through a normal authorized
account; do not try to bypass reviewer write restrictions.

## Can I integrate three or more batches?

Not with the current full latent integration path. It requires exactly two.
Multi-slice physical alignment is a separate mode and supports at least two slices.

## Why does a menu option exist but my analysis fails?

Menus, source code, input validation, runtime dependencies, and successful
scientific execution are separate gates. Check the actual job log and stage state.
A lightweight file inventory check does not establish parser compatibility.

## Why does the GPU default differ between pages?

R, CLI, and deployment defaults are distinct. The web worker uses configured,
validated GPU visibility. See [Defaults and tuning](parameters.md).

## Can I copy the old `sp_var_features=20` example?

Use the documented logical control (`TRUE` or `FALSE`), not an invented feature
count. Check the current [R parameter table](reference/r-parameters.md).

## Why is a completed job missing an email, package, or figure?

Analysis, packaging, notification, optional stage output, and retention are
independent. Inspect all states; see [outputs](results.md). Do not infer success
from the existence of an old image or assume absent optional output is a negative
biological result.

## Why do both application domains work but I must log in again?

Session cookies are host-scoped. Use one domain consistently. Email links use the
administrator's canonical `PUBLIC_BASE_URL`, which may be the alternate hostname.

## Can I install everything with `requirements-docs.txt` or an unnamed Docker image?

No. Documentation dependencies only build this site. Obtain a complete matching
scientific environment from maintainers; see [Installation](installation.md).

## Are the default weights and reviewer demos independent validation?

No. Defaults have a named selection provenance, and demo artifacts are saved
examples. Check [provenance](provenance.md) and independently validate the
registered scientific comparison before claiming replication or generality.
