# Python CLI

Use `Molo_FastAPI/app/core/python/main_process.py` in the complete scientific
runtime, not in the documentation virtual environment. The script imports
scientific dependencies; simply importing it is not a read-only validation step.

## Pairwise integration

Prepare the [parquet inputs](data-preparation.md), then run from the source root:

```bash
conda activate Molo
python -u Molo_FastAPI/app/core/python/main_process.py \
  -data_path ./molo_input \
  -save_path ./results/pairwise \
  -device cpu \
  -sp_alignment Molo \
  -molo_alignment_route three_stage \
  -train_epoch 300 \
  -compute_iLISI 1 \
  -r_dims 30 \
  -shared_dims 20
```

This command explicitly overrides parser defaults (`device="cuda:1"`, route
`auto`, `train_epoch=600`, `compute_iLISI=0`). Use a verified visible CUDA device
when appropriate. The script falls back to CPU when CUDA is unavailable; an
invalid GPU index on a CUDA-capable host is not guaranteed to fall back.

Full latent integration requires exactly two batches and `shared_dims < r_dims`.
Keep inputs and each run's output separate; do not overwrite an earlier experiment.

## Spatial alignment only

```bash
python -u Molo_FastAPI/app/core/python/main_process.py \
  -data_path ./molo_input \
  -save_path ./results/alignment_only \
  -device cpu \
  -sp_alignment Molo \
  -molo_alignment_route three_stage \
  -alignment_only 1
```

Alignment-only output does not establish successful full integration. `auto` can
select a different route; keep diagnostics of the route actually executed.

## Exact options and R/CLI mappings

All 37 parser flags are in [Complete CLI options](reference/cli-options.md).
Important differences:

| R argument | CLI flag |
| --- | --- |
| `pretrain_epoch` | `-pre_train_epoch` |
| `hidden_dims` | `-h_dims` |
| `reduction_dims` | `-r_dims` |
| `pis_path` | `-paste2_pis_path` |
| `mnn_loss`, `nc_loss`, `gme_loss`, `la_loss` | `-mnn`, `-nc`, `-gme`, `-la` |
| `mse_loss`, `rec_loss` | `-mse`, `-rec` |

The accepted distance-threshold default is `None`/automatic, not a fixed 5.0.
The parser also accepts nullable text representations before converting a numeric
threshold. Do not pass R logical literals as Python integer flag values: use 0/1.

## Pretraining, seeding, and checkpoints

`-pre_train_epoch` is accepted and recorded, but the main loop uses
`range(train_epoch)`; this does not establish a separate executed pretraining
phase. The top-level seed-setting call is commented out. Record actual seed
behavior rather than claiming all runs deterministic.

The saved checkpoint is an encoder component. It is not sufficient by itself to
restore the full dual-stream model. Output matrices, metrics, and provenance must
be retained separately; see [results](results.md).

## Benchmark scripts

Historical benchmark/research scripts have moved under `TESTTOOLS/` in the
examined working tree. Some retain earlier root assumptions. This tutorial does
not advertise an unverified `Integrate/` command or claim that a benchmark was
reproduced during the documentation update. Review each protocol, data source,
paths, split rules, and environment before running a research script.
