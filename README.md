# Molo documentation

English documentation for the current Molo spatial-omics workflow, audited against
the deployed **FastAPI application 1.6.0 source on 2026-11-11**. This is a documentation
repository, not the scientific runtime or a container image.

- Documentation: <https://molo-docs.readthedocs.io/en/latest/>
- Online application: <https://molo.ai4bread.com/>
- Alternate application: <https://molopipeline.site/>
- Existing bilingual guide: <https://docs.molopipeline.site/en/>

The old `/api/` URL remains the R function guide. The web HTTP API is documented
separately at `/http-api/`. Historical page URLs are preserved.

## Preview and validate

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-docs.txt
python scripts/render_reference.py --check
python -m unittest discover -s tests -v
mkdocs build --strict
python scripts/check_built_links.py
mkdocs serve -a 127.0.0.1:8001
```

Read the Docs loads `.readthedocs.yaml`; GitHub Actions runs the same validation.
Do not install scientific R/Python packages in the documentation build.

## Update from an authorized current source snapshot

```bash
python scripts/capture_source_contract.py --source-root /path/to/authorized/Molo
python scripts/render_reference.py
```

Review generated differences and update prose/examples before publishing. Capture
is static: it does not import FastAPI, run analyses, initialize databases, read
runtime `.env` files, or collect data. Only public signatures and hashes are
published. See `docs/provenance.md` and `docs/documentation-maintenance.md`.
