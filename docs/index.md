# Molo Documentation

**Current-source documentation · 2026-11-11 · FastAPI application 1.6.0**

Molo connects spatial-omics object creation, physical alignment, pairwise latent
integration, and downstream biological analysis. The current online application
uses **FastAPI, Celery, Redis, and SQLite**, not the historical Shiny web interface.

[Open Molo](https://molo.ai4bread.com/){ .md-button .md-button--primary }
[Web workflow](web.md){ .md-button }
[R functions](api.md){ .md-button }

## Choose your workflow

| You want to… | Start here |
| --- | --- |
| Use the hosted site without installing software | [Web workflow](web.md) |
| Prepare platform-specific input | [Data preparation](data-preparation.md) |
| Run R functions on your own data | [Basic R pipeline](basic_pipeline.md), [R reference](api.md) |
| Run the pairwise Python core | [Python CLI](python-cli.md) |
| Automate authenticated web requests | [HTTP API](http-api.md) |
| Understand defaults and tune integration | [Defaults and tuning](parameters.md) |
| Deploy and maintain a server | [Server deployment](deployment.md) |

!!! important "Two different API references"
    The preserved `/api/` address is the **R function reference**. Web HTTP routes
    and authentication are covered separately in [HTTP API](http-api.md).

## Before interpreting a result

Physical alignment of several slices is not full multi-batch latent integration;
the latter currently accepts **two batches**. Review the
[outputs and limitations](results.md) and [source provenance](provenance.md).

The alternate application address [molopipeline.site](https://molopipeline.site/)
remains available. Chinese documentation is retained at the
[separate bilingual guide](https://docs.molopipeline.site/).
