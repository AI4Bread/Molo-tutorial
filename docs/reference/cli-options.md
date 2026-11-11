# Complete Python CLI options

Source-audited on **2026-11-11**, Web app **1.6.0**. Generated from the [source contract](../provenance.md); do not edit tables by hand. Defaults below are **entry-point defaults**, not universal recommendations.

Use these flags with `Molo_FastAPI/app/core/python/main_process.py`, not with an R function or a web form.

| Flag | Destination | Type | Parser default |
| --- | --- | --- | --- |
| `-data_path` | `data_path` | `str` | `required` |
| `-save_path` | `save_path` | `str` | `required` |
| `-device` | `device` | `str` | `'cuda:1'` |
| `-pre_train_epoch` | `pre_train_epoch` | `int` | `200` |
| `-train_epoch` | `train_epoch` | `int` | `600` |
| `-sp_alignment` | `sp_alignment` | `str` | `'Molo'` |
| `-plot_3D_width` | `plot_3D_width` | `float` | `8.0` |
| `-plot_3D_height` | `plot_3D_height` | `float` | `6.0` |
| `-plot_3D_spot_size` | `plot_3D_spot_size` | `float` | `0.5` |
| `-dist_threshold` | `dist_threshold` | `string/untyped` | `None` |
| `-paste2_pis_path` | `pis_path` | `str` | `None` |
| `-sp_alignment_s` | `sp_alignment_s` | `float` | `0.7` |
| `-use_harmony` | `use_harmony` | `int` | `0` |
| `-compute_iLISI` | `compute_iLISI` | `int` | `0` |
| `-alignment_only` | `alignment_only` | `int` | `0` |
| `-lpgw_overlap_frac` | `lpgw_overlap_frac` | `float` | `0.7` |
| `-lpgw_loss` | `lpgw_loss` | `str` | `'square'` |
| `-lpgw_ref_idx` | `lpgw_ref_idx` | `int` | `0` |
| `-gene_align_alpha` | `gene_align_alpha` | `float` | `0.1` |
| `-gene_glmpca_latent_dim` | `gene_glmpca_latent_dim` | `int` | `50` |
| `-gene_overlap_frac` | `gene_overlap_frac` | `float` | `0.9` |
| `-molo_alignment_route` | `molo_alignment_route` | `str` | `'auto'` |
| `-edge_type` | `edge_type` | `str` | `'together'` |
| `-edge_sp` | `edge_sp` | `int` | `10` |
| `-edge_mtx` | `edge_mtx` | `int` | `10` |
| `-h_dims` | `hidden_dims` | `int` | `250` |
| `-r_dims` | `reduction_dims` | `int` | `30` |
| `-shared_dims` | `shared_dims` | `int` | `20` |
| `-mse` | `mse` | `float` | `1.0` |
| `-rec` | `rec` | `float` | `1` |
| `-mnn` | `mnn` | `float` | `0.9086822346479394` |
| `-nc` | `nc` | `float` | `8.21865755284329` |
| `-gme` | `gme` | `float` | `0.2881476150721262` |
| `-la` | `la` | `float` | `0.9340807418916036` |
| `-shared_scale` | `shared_scale` | `float` | `0.06947880705627452` |
| `-private_scale` | `private_scale` | `float` | `0.3844879738634757` |
| `-sample_size` | `sample_size` | `int` | `512` |
