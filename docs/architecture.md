# Model architecture and system design

**Source-audited: 2026-11-11 · Web application 1.6.0**

This page describes the **executed current implementation**, not every historical
class, manuscript proposal, or research-only CUDA script. Public function defaults
and source-file hashes are recorded in the [source provenance](provenance.md).

## End-to-end design

```text
Account / project / dataset asset
  -> validated input + analysis configuration
  -> FastAPI -> SQLite job record -> Redis / Celery queue
      -> R object conversion / platform reader
      -> physical spatial registration
      -> alignment-only outputs OR two-batch latent integration
      -> optional R downstream analysis and derived assets
  -> manifest / result package -> authenticated job view / email link
```

The persistent Molo object and project/asset records connect stages. A successful
HTTP submission is a queue acknowledgement, not successful analysis or delivery.
Reviewers have restricted read-only access; ordinary analyses use a registered
account session, not a new email code for every submission. See [Web workflow](web.md).

## 1. Spatial registration is a separate stage

The public `Molo_img_trans` entry delegates to the current exported route selector
in `molo_three_stage_alignment.py`. Its components are:

| Component | Current design |
| --- | --- |
| V1 | Joint feature rasterization and coarse global search, with guarded local deformation controls |
| Stage2 | Expression-guarded centroid/local translation candidate search |
| P2 | Conservative local residual-field refinement |

| Requested route | Stages actually selected |
| --- | --- |
| `v1_only` | V1 |
| `stage2_only` | Stage2 |
| `v1_p2` | V1 then P2 |
| `three_stage` | V1 then Stage2 then P2 |
| `ra2_three_stage` | Stage2 then P2, despite the historical route name |
| `raw` | Unchanged coordinates |
| `auto` | RA2-like/small-spot stacks select Stage2 then P2; otherwise V1 then P2, unless full three-stage is explicitly preferred |

The exported small-spot threshold is a median of **1200 spots per slice** by
configuration default, not a biological cutoff. Wrappers/configuration can select
a route explicitly. Record the requested **and resolved** route and diagnostics;
`auto` does not mean that all three stages necessarily ran. Internal route choices
are distinct from the web form's `Molo`/`Raw` method field and from R/CLI composite
methods such as `Molo+LPGW`.

The route's fitting does not use truth labels as alignment supervision. Labels
may be used separately for evaluation. Do not confuse this CPU/SciPy export with
historical or research GPU implementations, or infer validation from diagnostics.

Alignment-only exits before graph-model training; its saved embedding/UMAP fields
can be zero-filled format placeholders, not learned biological structure.

## 2. Two-stream variational graph integration

Full integration currently requires **exactly two batches**, A and B. Multiple
physically aligned slices do not establish arbitrary-batch latent integration.

1. Build spatial, expression, or combined KNN edges (`edge_type`). Within-batch
   edges are selected, batch-B indices are remapped, and graphs are made undirected.
   Cross-batch graph edges are not directly fed into the two encoders.
2. Independent `GNNEncoder` modules `enc_a` and `enc_b` use a graph-attention hidden
   layer and separate graph-attention heads for `mu` and `logvar`.
3. Reparameterization samples `z = mu + eps * exp(0.5 * logvar)` for training.
4. Split each posterior into **shared** and **private** coordinates. Defaults are
   30 total, 20 shared and 10 private dimensions. This split is an architectural
   design, not proof of complete biological/batch disentanglement.
5. Two `FeatureDecoder` MLPs reconstruct features from the **full** latent vector.
   Two `Translator` MLPs map shared posterior means A→B and B→A for cycle loss.

```text
A features + A graph -> enc_a -> mu_A, logvar_A -> z_A -> dec_a -> reconstructed A
                                  | shared/private
                                  + shared means <-> Translator cycle <-> shared means
                                  | shared/private
B features + B graph -> enc_b -> mu_B, logvar_B -> z_B -> dec_b -> reconstructed B
```

## 3. Losses actually optimized

The current training loop sums these terms:

```text
L = rec * edge_BCE + mse * feature_MSE
    + shared_scale * KL_shared + private_scale * KL_private
    + la * translator_cycle_MSE
    + mnn * MNN + nc * NC + gme * GME
```

| Term | Implementation role |
| --- | --- |
| Edge BCE | Positive-edge and sampled-negative-edge reconstruction from latent inner products |
| Feature MSE | Batch-specific decoder reconstruction of sampled input features |
| Shared/private KL | Standard-normal posterior regularization with separate coefficients |
| LA | A→B→A and B→A→B cycle consistency on sampled shared posterior means |
| MNN | Shared-expression mutual-neighbor constraints on shared latent means |
| NC | Bidirectional neighborhood consistency using soft targets |
| GME | Within-batch expression/latent pairwise-geometry preservation |

`shared_scale` and `private_scale` are **KL loss weights**, not multipliers applied
to the exported latent coordinates. There are discriminator-related helper
functions in the file, but the active loop does **not** instantiate/train an
adversarial discriminator or include a GAN term. Historical triplet/adversarial
or old loss-argument lists must not be presented as the current optimized model.

Each epoch uses a unified sample size `min(sample_size, n_A, n_B)` (default 512)
for feature reconstruction and cross-/within-batch constraints. Edge BCE and KL
operate over the full batch graphs/posteriors; this is **not** an entirely
mini-batched GNN. No shared expressed genes causes the MNN/NC constraints to lose
their shared-expression signal. Inspect warnings and available losses.

The parser retains a pretraining argument, but the examined active model loop
runs `train_epoch`; its presence alone does not prove a separate pretraining phase.
Use [Defaults and tuning](parameters.md), which distinguishes R, CLI and web values.

## 4. Inference and saved artifacts

Inference uses posterior means, concatenates both **complete** latent vectors and
applies each decoder to its batch's mean. Therefore:

- `embedding.parquet` is not restricted to the shared dimensions.
- In integration mode, `matrix.parquet` is decoder reconstruction, not raw UMI.
- Alignment-only preserves the input matrix representation instead; zero latent
  placeholders are not trained embeddings.
- The compatibility checkpoint saves `enc_a` only. It is not the complete two-
  encoder/two-decoder/translator model and cannot guarantee full restoration.

The top-level random-seed helper is not called in the examined main script.
Do not promise fixed-seed reproducibility or a new accuracy result from this audit.

## 5. Runtime architecture and boundaries

| Layer | Responsibility |
| --- | --- |
| FastAPI/Jinja | Account-scoped pages, form validation, ownership checks and job submission |
| SQLite WAL | Persistent job/account/project/asset metadata |
| Redis + Celery | Broker/backend, routing, async worker execution |
| `analysis` / `alignment` | R downstream orchestration / spatial and integration workflow |
| `packaging` / `notifications` | Filtered deliverables / result and account emails |
| Beat + `maintenance` | Optional scheduled reconciliation/retention; no automatic cleanup without running consumers/scheduler |

Deployment templates are not proof of installed units. The currently restored
host uses user-level systemd web/Redis/four worker services; Beat/maintenance were
left off to protect older results. Do not copy administrator-specific paths or
secrets into public documentation. [Deployment](deployment.md) explains the
portable requirements; [results](results.md) separates scientific, packaging and
delivery outcomes.
