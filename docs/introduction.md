# Introduction

Molo uses a persistent Molo object to connect spatial registration, shared/private
latent representation learning, and downstream biological workflows. Its role is
not merely a generic collection of unrelated analysis tools.

## Current architecture

| Layer | Current implementation |
| --- | --- |
| Web UI | FastAPI, Jinja2 templates, JavaScript/CSS |
| Durable job and account state | SQLite WAL; project and dataset-asset records |
| Asynchronous execution | Redis broker/result backend, Celery queues |
| Spatial alignment and expression integration | R wrappers, Python core, dual-stream graph model |
| Downstream analysis | R object creation, reduction/clustering, GO, CellChat, trajectory and ATAC workers |
| Public access | HTTPS reverse proxy and deployment-specific tunnel/network routing |

The web application reports version **1.6.0**. Individual historical R files may
contain older header versions; they are not the web application's release number.

## Distinct analysis modes

- **Multi-slice alignment**: physical registration of at least two valid samples.
- **Pairwise integration**: exactly two samples for full latent integration;
  mixed platform labels must describe the corresponding input samples.
- **Downstream analysis**: a supported raw input, compatible integrated output,
  or owned dataset asset feeds selected downstream stages.

The UI supports Visium, ATAC, Slide-seq, Xenium, CosMx, MERFISH, CODEX, and
Stereo-seq downstream pages. `Custom` data is supported by R/core workflows and
alignment inputs; it is not a separate downstream web page.

## Evidence boundaries

Example code is an executable template for a prepared environment, not a promise
that every optional dependency or biological comparison has been revalidated.
Inspect [results and limitations](results.md) before interpreting ARI, iLISI,
reconstruction matrices, or inferred labels.
