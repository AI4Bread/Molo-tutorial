# Results and limitations

Molo distinguishes analysis, packaging, and notification state. A queued response,
a healthy web page, an old plot, and an analysis result are different evidence.

## Alignment and integration

Typical application results live below `Molo_FastAPI/data/tasks/{job_id}/results/`.
Python CLI output is written to the requested `-save_path` instead.

| Artifact | Meaning |
| --- | --- |
| `Raw_Alignment_3D.png` / `.pdf` | Input coordinate preview |
| `Molo_Alignment_3D.png` / `.pdf` | Aligned coordinate preview |
| `matrix.parquet` | Decoder-reconstructed expression; **not original UMI counts** |
| `embedding.parquet` | Learned latent representation |
| `umap.parquet` | Derived visualization embedding |
| `spatial.csv`, `meta.csv` | Coordinates and metadata |
| `integrated_molo.rds` | R object from the wrapper workflow, not a guaranteed Python-only artifact |
| `alignment_info.txt`, diagnostics/metrics JSON | Parameters, selected route, and available metric status |

Exact files depend on method, mode, preprocessing, and completed stages.
Alignment-only does not generate evidence of a trained integration model. Shared
and private latent components have distinct meanings; the saved main embedding
can include the complete latent representation, not only the shared component.

## Downstream

The configured output root contains per-job directories with `manifest.json`,
`config.json`, `logs/`, `intermediate/`, and `plots/`. Inspect actual manifest
stage status and artifact lists. Optional GO/CellChat/trajectory output can be
missing because of data, annotation, resources, or execution failure; it is not
by itself a negative biological result.

## Packages, delivery, and retention

| State field | What to check |
| --- | --- |
| `analysis_status` | queued/running/completed/failed/expired and current stage |
| `package_status` | Whether packaging is ready, pending, failed, or not applicable |
| `delivery_status` | Whether notification was sent, failed, retried, or uncertain |
| Progress/stage fields | Coarse execution progress, not an accuracy estimate |

A completed analysis can still fail packaging or SMTP delivery. Result packages
are built by a separate queue with path/suffix/sensitivity filtering; internal
logs, private settings, and raw uploads are not a substitute for user deliverables.

The example runtime retention is 48 hours. Actual policy is administrator-configured
and requires active cleanup scheduling. Expired records may remain after result
files are removed. Download and preserve authorized outputs and provenance before
expiry; do not rely on indefinite hosted storage.

## Scientific interpretation

- Use real independent labels when a metric requires them; clustering pseudo-labels
  are not equivalent to ground truth. AD/Normal demos explicitly lack truth labels.
- Report exact iLISI normalization, evaluation population, and direction. Different
  definitions cannot be combined as if identical.
- Alignment accuracy variants differ in coverage and bidirectional penalties.
  Keep their formulas and evaluated points separate.
- Full latent integration supports two batches. Multi-slice alignment alone is
  not evidence that the full model supports arbitrary numbers of batches.
- The saved checkpoint contains an encoder component only; do not claim a full
  retrain-free model restoration from it.
- Default weights are selected settings from a named study, not independent
  validation across every platform.
- A pretraining argument or a seed helper in source is not proof those phases or
  seed settings were executed. Preserve run-level parameters and logs.

See [source provenance](provenance.md) for the scope of this documentation audit.
