# Version and source provenance

**Documentation audit: 2026-11-11 · Web app version: 1.6.0**

This revision replaces the 2025 Shiny-oriented tutorial with documentation of the
current FastAPI/Celery/Redis application and its R/Python entry points. An
authorized working-source snapshot was read without running scientific analyses.

!!! warning "A source audit is not a scientific reproduction"
    Reference extraction, documentation builds, page checks, and application
    readiness do not establish that every analysis, dataset, email provider, or
    optional R dependency has passed an end-to-end test.

## What was checked

- R function signatures, including S4 generic defaults and `Molo_Integrate`.
- Active dual-encoder training, feature decoders, translators, executed loss terms,
  and the exported spatial-registration route selector.
- Python `argparse` options and promoted integration defaults.
- Only routers mounted by `app/main.py`; JSON models and form fields.
- Registration/login, reviewer restrictions, dataset assets, queue routing,
  tuning presets, output conventions, and deployment templates.
- Source-file SHA-256 hashes are recorded in the
  [public source contract](https://github.com/AI4Bread/Molo-tutorial/blob/main/reference/source-contract.json).

The source tree was not clean. Its Git base was
`878014a82d75732b5795008378311b000dc897d6`, but **that commit alone does not reproduce
the audited working source**. File hashes identify the examined contents. Obtain
a complete matching source/environment release from maintainers before strict
reproduction. The documentation Git commit identifies this documentation revision,
not a new scientific software release.

## Entry-point defaults are distinct

R function defaults, Python parser defaults, web form defaults, wrapper overrides,
example YAML values, and administrator configuration can differ. See
[Defaults and tuning](parameters.md). A GPU index is machine/process-specific.

## Separate deployments

| Address | Role |
| --- | --- |
| [molo.ai4bread.com](https://molo.ai4bread.com/) | Primary application entry |
| [molopipeline.site](https://molopipeline.site/) | Alternate application entry |
| [This Read the Docs site](https://molo-docs.readthedocs.io/en/latest/) | Canonical English documentation and reference |
| [Existing English guide](https://docs.molopipeline.site/en/) | Separate bilingual documentation deployment |

A GitHub/Read the Docs build does not update the bilingual site's static files or
the running application. Sessions are host-specific; generated emails use the
configured `PUBLIC_BASE_URL` rather than automatically following a request host.

## Preserved limitations

- Full latent integration requires two batches; physical multi-slice alignment
  is a different mode.
- Output `matrix.parquet` is decoder reconstruction, not raw UMI counts.
- The saved checkpoint is an encoder component, not a complete restorable model.
- A declared pretraining argument does not prove a separate pretraining phase.
- A seed-setting helper exists, but its top-level call is commented out; do not
  infer every training run is fixed-seed.
- Cluster-inferred labels are not independent truth. AD/Normal reviewer artifacts
  explicitly distinguish unavailable real labels.
- Promoted loss defaults are from a DLPFC full-model selection, not a universal
  optimum or an independent new benchmark.

## Refresh

Use [Documentation maintenance](documentation-maintenance.md). Never commit runtime
databases, credentials, SMTP settings, or sample data. Regenerating tables does not
validate new algorithms or scientific claims.
