# Basic R pipeline

Use a complete, prepared scientific environment. The snippets below show the
current function names and call structure; they are **not** a claim that all
platform datasets or optional packages were executed during the documentation audit.

## Load current source

Run from `Molo_FastAPI/` in the matching source checkout, with required R packages
already installed. Source dependencies should match your maintainer-provided runtime.

```r
library(Seurat)
library(ggplot2)
library(patchwork)
source("app/core/R/molo_analysis.R")
source("app/core/R/molo_convert.R")
source("app/core/R/molo_pipeline.R")
source("app/core/R/integrate/molo_integrate_v3_DLPFC_LA+MLP.R")
```

Do not source a historical `Versions_of_web` copy into the same session. The
old `create_molo()` examples have been replaced with the current `Molo_Create()`.

## Single-platform downstream example

```r
molo_obj <- Molo_Create(data_type = "Visium", folder_path = "./data/visium/")
molo_obj <- Molo_Pipeline(
  molo_obj = molo_obj,
  steps = c("reduction_clustering", "var_features"),
  nCount_range = c(10, 2500),
  nFeature_range = c(10, 2500),
  dataset = "mouse",
  molo_env = "/path/to/miniconda3/envs/Molo/",
  plot_path = "./results/visium/",
  sp_var_features = FALSE,
  show_progress = TRUE
)
saveRDS(molo_obj, "./results/visium/molo_obj.rds")
```

The thresholds above are **explicit example values**, not validated QC thresholds
for every platform. Review distributions and select thresholds for your assay.

## Optional R pipeline steps

| `Molo_Pipeline(steps=...)` value | Operation | Web counterpart |
| --- | --- | --- |
| `reduction_clustering` | QC/reduction/clustering | `qc`, `cluster` |
| `var_features` | Variable-feature analysis | No identical standalone submission step |
| `top_GO_terms` | GO enrichment | `go` |
| `cellchat` | CellChat | `cell_chat` |
| `traj_infer` | Monocle3 trajectory | `traj` |

The R pipeline's default enables all five R steps; choose a subset explicitly if
packages, reference resources, or annotations are unavailable. The pipeline does
not expose every argument of the lower-level functions; use `Molo_reduction_cluster`
directly to control its `resolution` and `n_neighbors` arguments.

## Two-sample integration

```r
molo1 <- Molo_Create(data_type = "Visium", folder_path = "./data/slice_1/")
molo2 <- Molo_Create(data_type = "Visium", folder_path = "./data/slice_2/")
integrated_obj <- Molo_Integrate(
  obj_list = list(molo1, molo2),
  py_path = "/path/to/miniconda3/envs/Molo/bin/python",
  device = "cpu",
  sp_alignment = "Molo",
  molo_alignment_route = "three_stage",
  save_path = "./results/pairwise/",
  tmp = "./results/pairwise/tmp/",
  alignment_only = FALSE
)
```

CPU/GPU choice must match installed dependencies and compute capacity. This
example intentionally specifies a route rather than relying on `auto`.
Full latent integration requires exactly two batches; multi-slice physical
alignment uses `alignment_only=TRUE` and is not equivalent to joint integration.

## Other platforms

Use the input contracts in [Data preparation](data-preparation.md), not historical
filenames from older tutorials. ATAC, trajectory, and CellChat need their respective
scientific environments and resources. Validate a representative input before
attempting a large batch; do not infer full support from a platform appearing in a menu.
