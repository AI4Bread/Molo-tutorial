# Defaults and tuning

## Do not mix interfaces

| Setting | R `Molo_Integrate` | Python parser | Web/wrapper behavior |
| --- | --- | --- | --- |
| Device | `"cuda:1"` | `"cuda:1"` | Chosen by validated downstream runtime YAML |
| Alignment method | `"Molo+LPGW"` | `"Molo"` | Form allows `Molo` or `Raw`; passed to wrapper |
| Alignment route | `"auto"` | `"auto"` | Wrapper checks explicit option/environment; RA2 naming can select a specialized route |
| Pretraining argument | `pretrain_epoch=100` | `-pre_train_epoch 200` | Wrapper uses R default; not proof of a separate pretraining loop |
| Training epochs | `300` | `600` | Wrapper does not expose a web epoch form field |
| iLISI calculation | `TRUE` | `0` | Wrapper inherits R value |
| Latent/shared dimensions | `30` / `20` | `30` / `20` | R defaults unless explicitly changed in code/configuration |
| Distance threshold | `NULL` | `None` | No universal fixed value of 5 |

For downstream clustering, the R generic default is `n_neighbors=20` while the
HTTP handler default is `30`. Literal defaults are in the
[R](reference/r-parameters.md), [CLI](reference/cli-options.md), and
[HTTP](reference/http-routes.md) tables. Values in a form, deployment YAML, or
example command may deliberately override them.

## Current promoted integration weights

| Concept | R argument | CLI flag | Default |
| --- | --- | --- | --- |
| Reconstruction MSE | `mse_loss` | `-mse` | `1.0` |
| Reconstruction | `rec_loss` | `-rec` | `1` |
| Mutual nearest neighbors | `mnn_loss` | `-mnn` | `0.9086822346479394` |
| Neighborhood consistency | `nc_loss` | `-nc` | `8.21865755284329` |
| Geometric mean embedding | `gme_loss` | `-gme` | `0.2881476150721262` |
| Latent alignment | `la_loss` | `-la` | `0.9340807418916036` |
| Shared latent scaling | `shared_scale` | `-shared_scale` | `0.06947880705627452` |
| Private latent scaling | `private_scale` | `-private_scale` | `0.3844879738634757` |

These six promoted nontrivial weights are selected defaults from the DLPFC
full-model study (`trial_id=377`, `trial_number=32` in source metadata). They are
not a universal optimum, not an independent validation, and not equivalent to
setting every loss weight to one. Historical arguments such as `tri_loss`,
`ggae_loss`, `cos_loss`, `bce_loss`, `kl_loss`, `K_h`, or `edge` are not current
`Molo_Integrate` formals. The current graph selector is `edge_type`.

## Pairwise web tuning

| Preset | Trials | Mode |
| --- | --- | --- |
| `default` | 0 | No Optuna search; current defaults |
| `quick` | 10 | Optuna |
| `standard` | 50 | Optuna |
| `robust` | 100 | Optuna |

Tuning applies to pairwise integration, not the multi-slice alignment-only mode.
The request count must match the selected preset. `MOLO_TUNING_ENABLED` and
`MOLO_TUNE_MAX_TRIALS` control availability; robust requires a limit of 100.

Tuned analyses use the alignment queue. Default deployment concurrency is one;
do not raise it without isolated GPU/memory capacity. Tuning jobs are not covered
by the ordinary per-job Celery analysis timeout in the same way as standard jobs;
plan graceful shutdown time accordingly. Retained summaries include
`trials.jsonl`, `trials.csv`, `best_trial.json`, and `tuning_summary.json`.

The objective depends on available metrics; an unavailable truth label must not
be replaced with a fabricated biological label. Selecting a tuned configuration
on a dataset does not create an independent test result.

### Current Optuna search space

These are implementation bounds in `molo_tuner.py`, not recommended ranges for
every dataset or an interface for arbitrary web-side editing.

| Parameter | Candidate values / range | Sampling |
| --- | --- | --- |
| `edge_sp`, `edge_mtx` | 5, 10, 15, 20 | Categorical |
| `hidden_dims` | 128, 250, 512 | Categorical |
| `reduction_dims` | 20, 30, 50 | Categorical |
| `shared_dims` | 8, 12, 16, 20 | Categorical, then corrected to be smaller than reduction dimensions |
| `mse`, `rec` | 0.5–2.0 | Uniform float |
| `mnn`, `nc`, `gme`, `la` | 0.1–10.0 | Log float |
| `shared_scale`, `private_scale` | 0.01–2.0 | Log float |
| `sample_size` | 128, 256, 512 | Categorical |

For `tuning_objective="auto"`, finite available metrics are combined with the
source weights below and normalized by the sum of the weights actually present:
`iLISI` 0.35, `GraphConn` 0.20, `ASW_batch` 0.15, `KBET_accept` 0.10,
`ARI` 0.15, `ASW_Label` 0.05, and `alignment_accuracy_mean` 0.10. If none of these
weighted candidates is present, the implementation falls back to the first
finite candidate; no finite candidate is an error. An explicitly named unavailable
objective is also an error. Always record which metrics were actually available;
different available sets need not produce comparable scores.

## Reproducibility checklist

Record input sample order, preprocessing, input hashes, source hashes, device
visibility, alignment route actually selected, every model parameter, seed
behavior, versions, and output paths. Preserve real/estimated label distinctions
and the exact metric definition. Do not merge differently normalized iLISI or
coverage-filtered accuracy values into a single comparison.
