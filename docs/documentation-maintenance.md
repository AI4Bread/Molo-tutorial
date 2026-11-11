# Documentation maintenance

## English defaults and preserved URLs

Read the Docs project `molo-docs` is connected to
[AI4Bread/Molo-tutorial](https://github.com/AI4Bread/Molo-tutorial), branch `main`,
default version `latest`, language English. The site uses MkDocs Material with
explicit English UI/search settings. Historical addresses `/api/`, `/web/`,
`/installation/`, `/basic_pipeline/`, and `/FAQ/` remain present.

## Two publishing targets, one English source

`AI4Bread/Molo-tutorial/docs/` is the canonical English source for both sites.
The Molo navigation dropdown preserves **Self-hosted Documentation** and
**Read the Docs**, both opening a separate tab. No domain is removed.

The bilingual deployment remains in `LPLSXYJ/molo-docs`; its English pages are
exported from a pinned canonical Git commit instead of being maintained as a
second divergent tutorial. Chinese pages are translations/maintenance material;
exact parameter signatures remain in the shared generated tables.

```bash
python scripts/export_selfhosted.py --destination /path/to/molo-docs/Molo_Document
python scripts/export_selfhosted.py --destination /path/to/molo-docs/Molo_Document --check
```

The exporter preserves old self-hosted paths: `/api/` remains HTTP API there,
whereas RTD `/api/` is the R reference. It rewrites relative links explicitly;
never redirect identical path strings between the two sites without a map.
`canonical-source.json` records the revision and file hashes. Self-hosted CI checks
that the mirror still matches that pinned revision. To publish a new revision,
update the exported files/manifest together and review/merge it in that repository.
Building locally or updating a server checkout does not publish GitHub Pages.

If only Read the Docs is retained later, preserve the self-hosted legacy URLs
with page-specific redirects and retain the canonical source/history. No such
removal or domain migration is performed by this update.

## Read the Docs configuration

`.readthedocs.yaml` selects Ubuntu 24.04, Python 3.12, `mkdocs.yml`, strict warnings,
and `requirements-docs.txt`. Only documentation packages are installed. Never
execute a scientific workflow, import the application, load production secrets,
or require a GPU during the documentation build.

The primary docs dependencies are pinned. Transitive dependencies remain resolved
by pip; this is not a complete scientific or binary-environment lockfile.

Official configuration reference:
[Read the Docs configuration v2](https://docs.readthedocs.com/platform/stable/config-file/v2.html).

## Source-to-document contract

```bash
python scripts/capture_source_contract.py --source-root /path/to/authorized/Molo
python scripts/render_reference.py
python scripts/render_reference.py --check
python -m unittest discover -s tests -v
mkdocs build --strict
python scripts/check_built_links.py
```

Capture extracts public R signatures, Python parser defaults, mounted HTTP routes,
JSON schemas, and file SHA-256 hashes **without executing the source**. Raw runtime
configuration, data, credentials, accounts, and databases are not collected.
Inspect diffs before publishing; review semantics and examples manually. Update
audit dates/metadata only after inspecting a new authorized source snapshot.

To detect drift against a previously captured source:

```bash
python scripts/capture_source_contract.py \
  --source-root /path/to/authorized/Molo --check
```

Generated tables are deterministic and checked by GitHub Actions. Semantic tests
also reject obsolete per-job email verification, stale Shiny instructions, old
R arguments, and missing historical page routes.

## Publication acceptance

1. Build locally with strict mode and check local navigation/anchors.
2. Review the source diff, generated tables, privacy scan, and CI results.
3. Push the reviewed commit to the authorized repository branch.
4. Confirm GitHub webhook delivery and a **new Read the Docs build**.
5. Verify that the build succeeded for the **same pushed commit**, not an older one.
6. Request live pages and inspect English language, new navigation, current
   parameters, and preserved old URLs.

A successful Git push or GitHub Actions run alone is not evidence that Read the
Docs published the update. If no build starts, an administrator must check the
project's repository integration/webhook or trigger a build. Never invent a
Read the Docs token or share credentials in issues/commits.
