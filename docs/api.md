# Molo Functions  

In this section, we provide detailed explanations of the functionalities and parameter configurations for each function in the Molo package.  

## Molo_Create  

### Function  
Creates a Molo object from standard-format raw data files.  

### Parameters and Meanings  
* **data_type**: Platform type (e.g., `"Visium"`, default)  
* **folder_path**: Directory path containing input files (default: current directory `"./"`)  
* **n_cells**: Optional parameter specifying subset cell count (default: no restriction)  
* **n_features**: Optional parameter specifying feature selection count (default: no restriction)  
* **ATAC_dataset**: ATAC-seq reference genome species (options: `"mouse"` or `"human"`, default: `"mouse"`)  
* **CODEX_type**: Multiplexed imaging platform type (default: `"processor"`)  
* **softmax**: Whether to apply softmax normalization (logical value, default: `FALSE`)  
* **custom_index**: Custom index column identifier (default: `"__index_level_0__"`)  

### Return Value  
A constructed Molo object.  

### Basic Example  
```R  
molo_obj <- Molo_Create(data_type = "Visium",  
                        folder_path = "./Visium/",  
                        n_cells = 2000,  
                        n_features = 3000)  
```

## Molo_reduction_cluster  

### Function  
Performs dimensionality reduction and clustering analysis on a Molo object.  

### Parameters and Meanings  
* **obj**: Input Molo object  
* **only_QC**: Whether to perform only quality control filtering (logical value)  
* **nFeature_range**: Valid gene count range (vector format, e.g., `c(200, 2500)`)  
* **nCount_range**: Valid UMI count range (vector format, e.g., `c(500, 15000)`)  
* **molo_env**: Runtime configuration parameters (environment variable object)  
* **labeled_ref**: Reference annotated dataset file path (recommended: rds-format Seurat object)  
* **molo_plot_path**: Output directory path for result images (default: generated from environment variables)  
* **save_type**: Result saving format (e.g., static image `"png"`/interactive image `"echarts"`)  
* **run_Banksy**: Whether to enable Banksy spatial clustering (logical value)  
* **image_alpha**: Spatial image transparency (numeric range 0-1)  
* **pt_size**: Visualization point size (numeric, auto-adjusted by default)  
* **atac_steps**: ATAC-seq processing pipeline step identifiers (character vector)  
* **show_progress**: Whether to display progress information (logical value)  

### Return Value  
A Molo object containing dimensionality reduction embeddings and clustering labels.  

### Basic Example  
```R  
molo_obj <- Molo_reduction_cluster(obj = molo_obj,  
                                   only_QC = FALSE,  
                                   nFeature_range = c(200, 2500),  
                                   nCount_range = c(500, 15000),  
                                   molo_plot_path = "./plots/")  
```

## Molo_var_features  

### Function  
Identifies spatially variable features and marker genes in a Molo object.  

### Parameters and Meanings  
* **obj**: Input Molo object  
* **features**: Predefined feature set for analysis (optional; default: all features)  
* **sp_var_features**: Number of top spatially variable features to select (numeric)  
* **molo_plot_path**: Storage directory for visualization results (default: generated from environment variables)  
* **save_type**: Output image format (e.g., static `"png"`/interactive `"echarts"`)  
* **font_size**: Visualization text size (numeric, default: `12`)  
* **image_alpha**: Spatial layer transparency (numeric range `0-1`, default: `0.6`)  
* **pt_size**: Feature expression point size (numeric, default: `1.0`)  
* **show_progress**: Whether to display progress (logical value, default: `TRUE`)  

### Return Value  
A Molo object containing spatially variable feature analysis results.  

### Basic Example  
  ```R  
molo_obj <- Molo_var_features(obj = molo_obj,  
                                sp_var_features = 20,  
                                molo_plot_path = "./plots/")  
  ```

## Molo_top_GO_terms  

### Function  
Performs GO enrichment analysis and visualizes core pathways across clusters.  

### Parameters and Meanings  
* **obj**: Molo object with cluster annotations  
* **dataset**: Species database for gene annotation (options: `"mouse"` or `"human"`)  
* **plot_cols**: Custom color palette for visualization (optional; uses built-in colors by default)  
* **molo_plot_path**: Storage directory for GO result images (default: generated from environment variables)  
* **font_size**: Visualization label text size (numeric, default: `12`)  
* **show_progress**: Whether to display progress (logical value, default: `TRUE`)  

### Return Value  
A Molo object containing GO enrichment analysis results.  

### Basic Example  
  ```R  
molo_obj <- Molo_top_GO_terms(obj = molo_obj,  
                                dataset = "mouse",  
                                molo_plot_path = "./plots/")  
  ```

## Molo_cell_chat  

### Function  
Performs cell-cell communication analysis using CellChat.  

### Parameters and Meanings  
* **obj**: Molo object with cell type annotations  
* **plot_cols**: Custom color mapping for cell groups (optional; uses built-in colors by default)  
* **dataset**: Species database for ligand-receptor pairs (options: `"mouse"` or `"human"`)  
* **molo_plot_path**: Output directory for cell communication images (default: generated from environment variables)  
* **font_size**: Visualization label text size (numeric, default: `12`)  
* **show_progress**: Whether to display progress (logical value, default: `TRUE`)  

### Return Value  
A Molo object containing CellChat analysis results.  

### Basic Example  
  ```R  
molo_obj <- Molo_cell_chat(obj = molo_obj,  
                             dataset = "mouse",  
                             molo_plot_path = "./plots/")  
  ```

## Molo_traj  

### Function  
Performs cell trajectory inference using Monocle3.  

### Parameters and Meanings  
* **obj**: Molo object with dimensionality reduction results  
* **plot_cols**: Custom color mapping for trajectories (optional; uses built-in colors by default)  
* **molo_plot_path**: Storage directory for trajectory analysis images (default: generated from environment variables)  
* **show_progress**: Whether to display progress (logical value, default: `TRUE`)  

### Return Value  
A Molo object containing trajectory inference metadata.  

### Basic Example  
  ```R  
molo_obj <- Molo_traj(obj = molo_obj, molo_plot_path = "./plots/")  
  ```

## Molo_Integrate  

### Function  
Performs spatial data integration using the Molo framework.  

### Parameters and Meanings  
* **obj_list**: List of input Molo objects  
* **var_features**: Number of highly variable features to select (integer, default: `3000`)  
* **py_path**: Python interpreter executable path (default: `"home/user/anaconda3/envs/Molo/bin/python"`)  
* **device**: Model training device (options: `"cuda:0"`/`"cpu"`, default: `"cuda:0"`)  
* **save_path**: Integration result storage directory (default: `"./molo_save/"`)  
* **pretrain_epoch**: Pretraining iterations (integer, default: `100`)  
* **train_epoch**: Main training iterations (integer, default: `300`)  
* **tmp**: Temporary directory for intermediate files (default: `"./_molo_tmp/"`)  
* **edge**: Edge construction strategy (character, default: `"together"`)  
* **sp_alignment**: Spatial alignment method (character, default: `"Molo"`)  
* **plot_3D_width**: 3D visualization image width (numeric, default: `8.0`)  
* **plot_3D_height**: 3D visualization image height (numeric, default: `6.0`)  
* **plot_3D_spot_size**: 3D plot point size (numeric, default: `0.5`)  
* **dist_threshold**: Maximum spatial matching distance threshold (numeric, default: `5.0`)  
* **pis_path**: Precomputed alignment probability file path (optional, default: `NULL`)  
* **sp_alignment_s**: Spatial alignment regularization strength (numeric, default: `0.7`)  
* **use_harmony**: Whether to enable Harmony integration correction (logical value, default: `FALSE`)  
* **compute_iLISI**: Whether to compute integration quality metrics (logical value, default: `TRUE`)  
* **edge_type**: Edge connection type (character, default: `"together"`)  
* **edge_sp**: Spatial neighborhood edge count (integer, default: `10`)  
* **edge_mtx**: Feature similarity edge count (integer, default: `10`)  
* **hidden_dims**: Neural network hidden layer dimensions (integer, default: `250`)  
* **reduction_dims**: Latent space dimensions (integer, default: `30`)  
* **mse_loss**: Mean squared error loss weight (numeric, default: `1.0`)  
* **tri_loss**: Triplet loss weight (numeric, default: `1.0`)  
* **ggae_loss**: Graph autoencoder loss weight (numeric, default: `1.0`)  
* **cos_loss**: Cosine similarity loss weight (numeric, default: `1.0`)  
* **bce_loss**: Binary cross-entropy loss weight (numeric, default: `1.0`)  
* **kl_loss**: KL divergence loss weight (numeric, default: `1.0`)  
* **K_h**: Similarity scaling hyperparameter (numeric, default: `5.0`)  
* **verbose**: Whether to display progress information (logical value, default: `TRUE`)  

### Return Value  
An integrated Molo object.  

### Basic Example  
  ```R  
integrated_obj <- Molo_Integrate(obj_list = list(molo1, molo2),  
                                   var_features = 3000)  
  ```
