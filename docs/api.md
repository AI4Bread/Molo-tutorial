# R function reference

This preserved `/api/` URL documents **R functions**. For web endpoints, use the
[HTTP API guide](http-api.md). Defaults and signatures below are tied to the
2026-11-11 current-source audit, not the historical Shiny release.

Every argument and its exact default expression is in
[Complete R parameters](reference/r-parameters.md). This page explains their roles.

## Molo_Create

Creates a Molo object from a platform directory. Main arguments:

- `data_type`: reader/platform selector; match the exact supported spelling.
- `folder_path`: input directory, not a ZIP file.
- `n_cells`, `n_features`: optional sampling limits, not a replacement for QC.
- `ATAC_dataset`, `ATAC_arrow_files`: ATAC species/reference and optional existing ArrowFiles.
- `CODEX_type`, `softmax`: imaging input/normalization options.
- `custom_index`: cell identifier column for Custom data.

```r
molo_obj <- Molo_Create(data_type = "Visium", folder_path = "./visium/")
```

## Molo_reduction_cluster

Performs QC, reduction, clustering, and associated spatial/neighborhood analysis.
Supply `obj`, `molo_plot_path`, and an appropriate `molo_env` for your machine.

- R generic defaults include `resolution=0.5`, `n_neighbors=20`,
  `nFeature_range=c(10, 2500)`, and `nCount_range=c(10,2500)`.
- The web handler instead declares `n_neighbors=30`. These are separate interfaces.
- `only_QC`, `run_Banksy`, `labeled_ref`, `atac_steps`, and plotting settings
  control additional behavior. A reference annotation must have known provenance.
- The built-in environment path is a legacy placeholder; override it explicitly.

```r
molo_obj <- Molo_reduction_cluster(
  obj = molo_obj,
  molo_env = "/path/to/miniconda3/envs/Molo/",
  molo_plot_path = "./plots/",
  resolution = 0.5,
  n_neighbors = 20,
  show_progress = TRUE
)
```

## Molo_var_features

Identifies/visualizes variable features. `features=NULL` lets the implementation
select features; `sp_var_features=FALSE` is a **logical control**, not a count of
features. The earlier tutorial's `sp_var_features=20` example was misleading.
Supply `molo_plot_path`. Plot defaults include `save_type="graph"`,
`image_alpha=1`, `pt_size=2`, and `show_progress=FALSE`.

```r
molo_obj <- Molo_var_features(
  obj = molo_obj, sp_var_features = FALSE, molo_plot_path = "./plots/"
)
```

## Molo_top_GO_terms

GO enrichment for an appropriately annotated/clustered object. `dataset="mouse"`
is the default; use `"human"` when appropriate. `plot_cols` controls group colors,
`font_size=NULL` delegates text sizing, and `molo_plot_path` is required.
Species/reference resources must match the input gene identifiers.

```r
molo_obj <- Molo_top_GO_terms(
  obj = molo_obj, dataset = "mouse", molo_plot_path = "./plots/"
)
```

## Molo_cell_chat

CellChat-based communication analysis with `dataset="mouse"` by default. Meaningful
cell/group annotation, a suitable ligand-receptor database, and the corresponding
R environment are required. Missing or unsuitable data may yield no valid output;
this is not evidence that biological communication is absent.

```r
molo_obj <- Molo_cell_chat(
  obj = molo_obj, dataset = "mouse", molo_plot_path = "./plots/"
)
```

## Molo_traj

Monocle3 trajectory inference. Requires a compatible reduced/annotated object and
trajectory environment. `plot_cols=NULL` and `show_progress=FALSE` are the current
generic defaults. A computed pseudotime is not a validated developmental direction.

```r
molo_obj <- Molo_traj(obj = molo_obj, molo_plot_path = "./plots/")
```

## Molo_Integrate

Registers input Molo objects and runs integration unless `alignment_only=TRUE`.
Full latent integration currently accepts **two objects/batches**. Important groups:

| Group | Parameters |
| --- | --- |
| Input/export | `obj_list`, `var_features`, `tmp`, `save_path`, `py_path` |
| Compute/training | `device`, `pretrain_epoch`, `train_epoch`, `sample_size` |
| Physical registration | `sp_alignment`, `molo_alignment_route`, `alignment_only`, `lpgw_ref_idx`, `gene_align_alpha`, `gene_glmpca_latent_dim`, `gene_overlap_frac` |
| Geometry/plots | `plot_3D_width`, `plot_3D_height`, `plot_3D_spot_size`, `dist_threshold`, `pis_path`, `sp_alignment_s` |
| Graph/model | `edge_type`, `edge_sp`, `edge_mtx`, `hidden_dims`, `reduction_dims`, `shared_dims` |
| Loss/latent weights | `mse_loss`, `rec_loss`, `mnn_loss`, `nc_loss`, `gme_loss`, `la_loss`, `shared_scale`, `private_scale` |
| Evaluation | `use_harmony`, `compute_iLISI`, `verbose` |
| Tuning | `tuning_mode`, `tune_preset`, `tune_trials`, `tuning_objective` |

Current R defaults include `py_path=Sys.which("python")`, `device="cuda:1"`,
`sp_alignment="Molo+LPGW"`, `molo_alignment_route="auto"`, and
`dist_threshold=NULL`. The website passes its own method/device values, so these
are **not** necessarily the effective web defaults.

```r
integrated_obj <- Molo_Integrate(
  obj_list = list(molo1, molo2),
  py_path = "/path/to/miniconda3/envs/Molo/bin/python",
  device = "cpu",  # or a verified GPU visible to this process
  sp_alignment = "Molo",
  molo_alignment_route = "three_stage",
  train_epoch = 300,
  save_path = "./results/pairwise/",
  tmp = "./results/pairwise/tmp/"
)
```

This example **overrides** the R route default to request three-stage alignment;
`auto` does not guarantee that route. `pretrain_epoch` is recorded/passed, but do
not infer a separately executed pretraining phase. See [defaults](parameters.md)
and [limitations](results.md).

## Molo_Convert, Molo_save_data, Molo_Pipeline

- `Molo_Convert` bridges Molo and Seurat representations. Set `start`, `end`,
  `data_type`, `assay`, and `folder_path` as appropriate to the conversion path.
- `Molo_save_data` exports preprocessing-dependent parquet inputs. Its
  `prefer_sct` switch controls SCT preference; fallback scaling is not identical
  to SCT normalization. Do not label arbitrary normalized AnnData values as SCT.
- `Molo_Pipeline` chains downstream R functions. Its step names differ from HTTP
  step names; see [Basic R pipeline](basic_pipeline.md).
- `Molo_reduction_1` is a lower-level reduction helper with explicit environment
  and plot-path arguments; prefer the documented cluster wrapper when appropriate.

Full signatures, including required arguments and nullable defaults, are in
[Complete R parameters](reference/r-parameters.md).
