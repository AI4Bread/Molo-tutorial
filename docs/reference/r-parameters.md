# Complete R parameters

Source-audited on **2026-11-11**, Web app **1.6.0**. Generated from the [source contract](../provenance.md); do not edit tables by hand. Defaults below are **entry-point defaults**, not universal recommendations.

## `Molo_Convert`

Source: `Molo_FastAPI/app/core/R/molo_convert.R` (line 268).

```r
Molo_Convert(
  obj,
  start = "Seurat",
  end = "Molo",
  data_type = "Visium",
  assay = "Molo",
  folder_path
)
```

| Parameter | Default expression |
| --- | --- |
| `obj` | **required** |
| `start` | `"Seurat"` |
| `end` | `"Molo"` |
| `data_type` | `"Visium"` |
| `assay` | `"Molo"` |
| `folder_path` | **required** |

## `Molo_Create`

Source: `Molo_FastAPI/app/core/R/molo_analysis.R` (line 2012).

```r
Molo_Create(
  data_type = "Visium",
  folder_path = "./",
  n_cells = NULL,
  n_features = NULL,
  ATAC_dataset = "mouse",
  ATAC_arrow_files = NULL,
  CODEX_type = "processor",
  softmax = FALSE,
  custom_index = "__index_level_0__"
)
```

| Parameter | Default expression |
| --- | --- |
| `data_type` | `"Visium"` |
| `folder_path` | `"./"` |
| `n_cells` | `NULL` |
| `n_features` | `NULL` |
| `ATAC_dataset` | `"mouse"` |
| `ATAC_arrow_files` | `NULL` |
| `CODEX_type` | `"processor"` |
| `softmax` | `FALSE` |
| `custom_index` | `"__index_level_0__"` |

## `Molo_Integrate`

Source: `Molo_FastAPI/app/core/R/integrate/molo_integrate_v3_DLPFC_LA+MLP.R` (line 108).

```r
Molo_Integrate(
  obj_list,
  var_features = 3000,
  py_path = Sys.which("python"),
  device = "cuda:1",
  save_path = "./molo_save/",
  pretrain_epoch = 100,
  train_epoch = 300,
  tmp = "./_molo_tmp/",
  sp_alignment = "Molo+LPGW",
  lpgw_ref_idx = "0",
  gene_align_alpha = 0.1,
  gene_glmpca_latent_dim = 50,
  gene_overlap_frac = 0.9,
  edge_type = "together",
  plot_3D_width = 8.0,
  plot_3D_height = 6.0,
  plot_3D_spot_size = 0.5,
  dist_threshold = NULL,
  pis_path = NULL,
  sp_alignment_s = 0.7,
  use_harmony = FALSE,
  compute_iLISI = TRUE,
  edge_sp = 10,
  edge_mtx = 10,
  hidden_dims = 250,
  reduction_dims = 30,
  shared_dims = 20,
  mse_loss = 1.0,
  rec_loss = 1,
  mnn_loss = 0.9086822346479394,
  nc_loss = 8.21865755284329,
  gme_loss = 0.2881476150721262,
  la_loss = 0.9340807418916036,
  shared_scale = 0.06947880705627452,
  private_scale = 0.3844879738634757,
  sample_size = 512,
  molo_alignment_route = "auto",
  alignment_only = FALSE,
  tuning_mode = "none",
  tune_preset = "default",
  tune_trials = 0,
  tuning_objective = "auto",
  verbose = TRUE
)
```

| Parameter | Default expression |
| --- | --- |
| `obj_list` | **required** |
| `var_features` | `3000` |
| `py_path` | `Sys.which("python")` |
| `device` | `"cuda:1"` |
| `save_path` | `"./molo_save/"` |
| `pretrain_epoch` | `100` |
| `train_epoch` | `300` |
| `tmp` | `"./_molo_tmp/"` |
| `sp_alignment` | `"Molo+LPGW"` |
| `lpgw_ref_idx` | `"0"` |
| `gene_align_alpha` | `0.1` |
| `gene_glmpca_latent_dim` | `50` |
| `gene_overlap_frac` | `0.9` |
| `edge_type` | `"together"` |
| `plot_3D_width` | `8.0` |
| `plot_3D_height` | `6.0` |
| `plot_3D_spot_size` | `0.5` |
| `dist_threshold` | `NULL` |
| `pis_path` | `NULL` |
| `sp_alignment_s` | `0.7` |
| `use_harmony` | `FALSE` |
| `compute_iLISI` | `TRUE` |
| `edge_sp` | `10` |
| `edge_mtx` | `10` |
| `hidden_dims` | `250` |
| `reduction_dims` | `30` |
| `shared_dims` | `20` |
| `mse_loss` | `1.0` |
| `rec_loss` | `1` |
| `mnn_loss` | `0.9086822346479394` |
| `nc_loss` | `8.21865755284329` |
| `gme_loss` | `0.2881476150721262` |
| `la_loss` | `0.9340807418916036` |
| `shared_scale` | `0.06947880705627452` |
| `private_scale` | `0.3844879738634757` |
| `sample_size` | `512` |
| `molo_alignment_route` | `"auto"` |
| `alignment_only` | `FALSE` |
| `tuning_mode` | `"none"` |
| `tune_preset` | `"default"` |
| `tune_trials` | `0` |
| `tuning_objective` | `"auto"` |
| `verbose` | `TRUE` |

## `Molo_Pipeline`

Source: `Molo_FastAPI/app/core/R/molo_pipeline.R` (line 27).

```r
Molo_Pipeline(
  molo_obj = NULL,
  only_QC = FALSE,
  steps = c("reduction_clustering", "var_features", "top_GO_terms", "cellchat", "traj_infer"),
  atac_steps = 5,
  nCount_range = NULL,
  nFeature_range = NULL,
  plot_path = "./plots/",
  dataset = "mouse",
  molo_env = "/user/Anaconda3/envs/Molo/",
  labeled_ref = NULL,
  run_Banksy = FALSE,
  save_type = "graph",
  image_alpha = 1,
  pt_size = 1.5,
  var_features = NULL,
  sp_var_features = FALSE,
  plot_cols = NULL,
  show_progress = FALSE,
  return_obj = TRUE
)
```

| Parameter | Default expression |
| --- | --- |
| `molo_obj` | `NULL` |
| `only_QC` | `FALSE` |
| `steps` | `c("reduction_clustering", "var_features", "top_GO_terms", "cellchat", "traj_infer")` |
| `atac_steps` | `5` |
| `nCount_range` | `NULL` |
| `nFeature_range` | `NULL` |
| `plot_path` | `"./plots/"` |
| `dataset` | `"mouse"` |
| `molo_env` | `"/user/Anaconda3/envs/Molo/"` |
| `labeled_ref` | `NULL` |
| `run_Banksy` | `FALSE` |
| `save_type` | `"graph"` |
| `image_alpha` | `1` |
| `pt_size` | `1.5` |
| `var_features` | `NULL` |
| `sp_var_features` | `FALSE` |
| `plot_cols` | `NULL` |
| `show_progress` | `FALSE` |
| `return_obj` | `TRUE` |

## `Molo_cell_chat`

Source: `Molo_FastAPI/app/core/R/molo_analysis.R` (line 114).

```r
Molo_cell_chat(
  obj,
  plot_cols = NULL,
  dataset = "mouse",
  molo_plot_path,
  font_size = NULL,
  show_progress = FALSE
)
```

| Parameter | Default expression |
| --- | --- |
| `obj` | **required** |
| `plot_cols` | `NULL` |
| `dataset` | `"mouse"` |
| `molo_plot_path` | **required** |
| `font_size` | `NULL` |
| `show_progress` | `FALSE` |

## `Molo_reduction_1`

Source: `Molo_FastAPI/app/core/R/molo_analysis.R` (line 79).

```r
Molo_reduction_1(
  obj,
  molo_env,
  molo_plot_path
)
```

| Parameter | Default expression |
| --- | --- |
| `obj` | **required** |
| `molo_env` | **required** |
| `molo_plot_path` | **required** |

## `Molo_reduction_cluster`

Source: `Molo_FastAPI/app/core/R/molo_analysis.R` (line 86).

```r
Molo_reduction_cluster(
  obj,
  only_QC = FALSE,
  nFeature_range = c(10, 2500),
  nCount_range = c(10,2500),
  molo_env = "/user/anaconda3/envs/Molo/",
  labeled_ref = NULL,
  molo_plot_path,
  save_type = "graph",
  run_Banksy = FALSE,
  image_alpha = 1,
  pt_size = 2,
  atac_steps = 5,
  resolution = 0.5,
  n_neighbors = 20,
  show_progress = FALSE
)
```

| Parameter | Default expression |
| --- | --- |
| `obj` | **required** |
| `only_QC` | `FALSE` |
| `nFeature_range` | `c(10, 2500)` |
| `nCount_range` | `c(10,2500)` |
| `molo_env` | `"/user/anaconda3/envs/Molo/"` |
| `labeled_ref` | `NULL` |
| `molo_plot_path` | **required** |
| `save_type` | `"graph"` |
| `run_Banksy` | `FALSE` |
| `image_alpha` | `1` |
| `pt_size` | `2` |
| `atac_steps` | `5` |
| `resolution` | `0.5` |
| `n_neighbors` | `20` |
| `show_progress` | `FALSE` |

## `Molo_save_data`

Source: `Molo_FastAPI/app/core/R/integrate/molo_integrate_v3_DLPFC_LA+MLP.R` (line 1).

```r
Molo_save_data(
  obj,
  var_features = 3000,
  folder_path = "./_molo_tmp/",
  prefer_sct = TRUE
)
```

| Parameter | Default expression |
| --- | --- |
| `obj` | **required** |
| `var_features` | `3000` |
| `folder_path` | `"./_molo_tmp/"` |
| `prefer_sct` | `TRUE` |

## `Molo_top_GO_terms`

Source: `Molo_FastAPI/app/core/R/molo_analysis.R` (line 104).

```r
Molo_top_GO_terms(
  obj,
  dataset = "mouse",
  plot_cols = NULL,
  molo_plot_path,
  font_size = NULL,
  show_progress = FALSE
)
```

| Parameter | Default expression |
| --- | --- |
| `obj` | **required** |
| `dataset` | `"mouse"` |
| `plot_cols` | `NULL` |
| `molo_plot_path` | **required** |
| `font_size` | `NULL` |
| `show_progress` | `FALSE` |

## `Molo_traj`

Source: `Molo_FastAPI/app/core/R/molo_analysis.R` (line 124).

```r
Molo_traj(
  obj,
  plot_cols = NULL,
  molo_plot_path,
  show_progress = FALSE
)
```

| Parameter | Default expression |
| --- | --- |
| `obj` | **required** |
| `plot_cols` | `NULL` |
| `molo_plot_path` | **required** |
| `show_progress` | `FALSE` |

## `Molo_var_features`

Source: `Molo_FastAPI/app/core/R/molo_analysis.R` (line 59).

```r
Molo_var_features(
  obj,
  features = NULL,
  sp_var_features = FALSE,
  molo_plot_path,
  save_type = "graph",
  font_size = NULL,
  image_alpha = 1,
  pt_size = 2,
  show_progress = FALSE
)
```

| Parameter | Default expression |
| --- | --- |
| `obj` | **required** |
| `features` | `NULL` |
| `sp_var_features` | `FALSE` |
| `molo_plot_path` | **required** |
| `save_type` | `"graph"` |
| `font_size` | `NULL` |
| `image_alpha` | `1` |
| `pt_size` | `2` |
| `show_progress` | `FALSE` |
