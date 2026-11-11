# Data preparation

A successful file-inventory check means the layout is plausible, not that every
platform file can be parsed or that the scientific workflow has succeeded.
Match the actual reader version and inspect metadata/coordinate alignment.

## Platform directories

| Platform | Current expected reader/layout |
| --- | --- |
| Visium | `filtered_feature_bc_matrix.h5` plus `spatial/`; Space Ranger coordinates/images compatible with Seurat |
| Slide-seq | `counts.csv.gz`, `counts.tsv.gz`, or `counts.txt.gz`, plus `spatial.csv`/`spatial.csv.gz` |
| MERFISH | Vizgen outputs compatible with `LoadVizgen`, including expression/metadata and applicable boundary files |
| CosMx | NanoString expression matrix, metadata, FOV positions and related exports compatible with `LoadNanostring` |
| CODEX | `codex.csv` or the compatible Akoya input expected by the selected reader |
| Xenium | Compatible `cell_feature_matrix.h5`, cells/transcripts/boundaries exports for `LoadXenium` |
| Stereo-seq | Current object reader uses `stereo_seq.h5ad`, including `obsm/spatial` and `obs/cell_name` |
| Spatial ATAC | `fragments.tsv.gz`, index `.tbi`, and spatial resources where available; ArchR/Signac runtime |

Filenames in older tutorials such as `raw_counts.csv.gz` and
`spatial_info.csv.gz` are not the current Slide-seq reader contract. Validate the
exact source/version rather than renaming a different matrix blindly.

### Visium example

```text
slice_1/
  filtered_feature_bc_matrix.h5
  spatial/
    scalefactors_json.json
    tissue_lowres_image.png
    tissue_hires_image.png
    tissue_positions.csv          # or tissue_positions_list.csv
  truth.txt                      # optional real labels, not mandatory
```

### Multiple slices

```text
alignment_input/
  slice_1/
    filtered_feature_bc_matrix.h5
    spatial/
  slice_2/
    filtered_feature_bc_matrix.h5
    spatial/
```

Preserve subdirectory paths when uploading a folder or ZIP. Integration needs
exactly two valid sample directories; alignment-only needs at least two. Mixed
platform inputs require matching per-sample platform labels.

If `truth.txt` is supplied, the wrapper reads tab-separated barcode/label pairs:

```text
barcode_1	CellTypeA
barcode_2	CellTypeB
```

Ensure barcode alignment and label provenance. Without truth, preprocessing may
supply cluster-derived labels. **Those are not independent biological ground
truth and must not be reported as such.** Do not manufacture labels to enable a
metric or tune on a test label set.

## Uploads, paths, and assets

- Raw downstream web upload requires a `.zip` containing the selected platform data.
- Alignment upload may contain several sample folders/files; preserve names and structure.
- Server paths are paths on the compute service, not paths on the user's laptop.
  They must be enabled and inside configured allowed roots.
- A compatible owned dataset asset can be reused without uploading another copy.
- Completed integration output can seed downstream analysis only when ownership,
  completion state, and `.rds`/`.h5ad` availability checks pass.
- Archives with unsafe paths, excessive expansion, or unsupported layouts may be rejected.

## Python-core parquet input

```text
molo_input/
  Molo1/
    Count.parquet
    SCT.parquet
    spatial.parquet
    meta.parquet
    image.png           # optional
  Molo2/
    Count.parquet
    SCT.parquet
    spatial.parquet
    meta.parquet
```

- Matrix parquet files use cells/spots as rows and aligned features as columns,
  including the `cells` identifier column used by the exporter.
- `Count.parquet` represents the input count-like matrix; `SCT.parquet` is a
  preprocessing-dependent normalized/scaled matrix. Do not call arbitrary
  `adata.X` values SCT, or silently treat log-normalized input as raw counts.
- Coordinates and metadata must preserve matrix row order, and features must be
  compatible across the two batches.
- Prefer the matching R `Molo_save_data` exporter in a prepared environment.
  Inspect exported dimensions/identifiers before training.

## Custom object input

`Molo_Create(data_type="Custom")` supports a compatible `matrix.parquet` plus
applicable `embedding.parquet`, `umap.parquet`, `meta.csv`, and `spatial.csv`.
The `custom_index` argument defaults to `__index_level_0__`. Custom object creation
is not a promise that every arbitrary table can be submitted through a raw web
platform page. Use [R functions](api.md) and validate the object contract.
