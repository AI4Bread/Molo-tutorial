# Web workflow

The current online interface is a **FastAPI asynchronous application**, not Shiny.
Use [molo.ai4bread.com](https://molo.ai4bread.com/) or
[molopipeline.site](https://molopipeline.site/).

## 1. Register, log in, or inspect a reviewer demo

- Registration requests an email code to verify the account. Use the same
  registered account for subsequent analyses.
- Normal submissions require an authenticated session. Results are addressed to
  the account's registered email; **there is no fresh email code field per job**.
- Reviewer access is a restricted demonstration. Parameters can be inspected,
  but analysis submissions, retries, clones, and other unsafe writes are blocked.
- Sessions are host-specific. Log in again if you switch between the two domains.

## 2. Prepare a project and dataset

Use **Dataset Library** (`/projects`) to organize projects and validated input
assets, or upload input from an analysis form. Keep the assigned project, asset,
and Job IDs. Asset ownership and compatibility are checked on submission.

Choose an input source:

| Input | Behavior |
| --- | --- |
| Upload | Alignment accepts folder/files or an archive; downstream raw upload requires `.zip` |
| Server path | Only enabled/allowlisted server roots are accepted; this is not a path on your laptop |
| Dataset asset | Reuse a compatible asset owned by or accessible to your account |
| Completed integration | Downstream workflows can reuse an accessible completed integration result |

Passing an initial file inventory check does not guarantee that a platform reader
can parse every file. See [data preparation](data-preparation.md).

## 3. Alignment or integration

Open `/analyse/alignment/`.

| Workspace | Samples | Result |
| --- | --- | --- |
| Multi-slice alignment | At least two | Physical coordinates/registration without full latent integration |
| Pairwise alignment and integration | Exactly two | Physical alignment plus expression/latent integration |

The form accepts `mode=align_only` or `mode=integrate`, and alignment method `Molo`
or `Raw`. These web values are deliberately narrower than the internal R/Python
method/route controls. Do not submit a CLI-only route as a web form value.

Optional pairwise integration presets are **default / quick / standard / robust**
with **0 / 10 / 50 / 100** tuning trials. Counts are derived from the preset and
limited by server configuration, not an arbitrary client input. See
[Defaults and tuning](parameters.md).

## 4. Downstream analysis

Open `/analyse/downstream/{analysis_type}`, where the type is one of:

`visium`, `atac`, `slideseq`, `xenium`, `cosmx`, `merfish`, `codex`, `stereoseq`.

| HTTP form field | Handler default | Meaning |
| --- | --- | --- |
| `resolution` | `0.5` | Clustering resolution |
| `n_neighbors` | `30` | Neighborhood size; differs from the R generic default of 20 |
| `species` | `mouse` | `mouse` or `human`; match biology and reference resources |
| `n_feature_min` | `2500` | Declared endpoint default, not a universal biological QC recommendation |
| `analysis_steps` | empty list, then normalized | QC is inserted automatically; optional steps selected below |

Step identifiers are `qc`, `cluster`, `go`, `cell_chat`, and `traj`. The R
pipeline uses different names; do not interchange them. Species, platform, data
quality, annotation, and optional packages determine whether a stage is meaningful.

## 5. Follow jobs and reuse results

The task is queued asynchronously; submission success is not analysis success.
You may close the page and return to **My Jobs** (`/jobs`). Job details distinguish
analysis, packaging, and delivery. Retry/clone/cancel and resend actions are
permission- and state-dependent; do not repeatedly submit the same data to recover
an existing Job ID.

Projects, datasets, jobs, and derived assets can be inspected through analysis
chains. Downstream pages can recover jobs by `?task_id=<job_id>`.

## 6. Download before expiry

Download links are time-limited and associated with the result package. The
configured retention window is normally 48 hours in the example configuration,
but cleanup only occurs when maintenance services are actually running. Do not
assume permanent storage or that a successful analysis implies a successful email.
See [outputs and limitations](results.md).
