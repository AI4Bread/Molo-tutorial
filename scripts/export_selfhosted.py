#!/usr/bin/env python3
"""Export the canonical English guide to the bilingual site's legacy page paths.

No network calls, application imports, secrets or scientific execution. Run from
an exact canonical Git revision, then publish the reviewed mirror in its own repo.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "https://github.com/AI4Bread/Molo-tutorial"
PAGE_MAP = {
    "index.md": "index.md", "introduction.md": "introduction.md",
    "architecture.md": "architecture.md", "installation.md": "getting-started.md",
    "data-preparation.md": "data-preparation.md", "web.md": "web-workflow.md",
    "basic_pipeline.md": "basic-pipeline.md", "api.md": "r-functions.md",
    "python-cli.md": "python-cli.md", "http-api.md": "api.md",
    "parameters.md": "parameters.md", "results.md": "results.md",
    "deployment.md": "deployment.md",
    "documentation-maintenance.md": "documentation-site.md",
    "provenance.md": "provenance.md", "FAQ.md": "faq.md",
    "reference/r-parameters.md": "reference/r-parameters.md",
    "reference/cli-options.md": "reference/cli-options.md",
    "reference/http-routes.md": "reference/http-routes.md",
}


def rewrite_links(text):
    # Only relative Markdown destinations; preserve code and external URLs.
    def replace(match):
        url = match[1]
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc or parsed.path not in PAGE_MAP:
            return match[0]
        return "](" + PAGE_MAP[parsed.path] + ("#" + parsed.fragment if parsed.fragment else "") + ")"
    return re.sub(r"\]\(([^\s)]+)\)", replace, text)


def map_nav(value):
    if isinstance(value, list):
        return [map_nav(v) for v in value]
    if isinstance(value, dict):
        return {k: map_nav(v) for k, v in value.items()}
    return PAGE_MAP.get(value, value)


def export_files():
    docs = ROOT / "docs"
    actual = {p.relative_to(docs).as_posix() for p in docs.rglob("*.md")}
    if actual != set(PAGE_MAP):
        raise ValueError(f"Review page mapping after adding/removing pages: {actual ^ set(PAGE_MAP)}")
    files = {"source_en/" + target: rewrite_links((docs / source).read_text()).encode()
             for source, target in PAGE_MAP.items()}
    for asset in (docs / "assets").rglob("*"):
        if asset.is_file():
            files["source_en/" + asset.relative_to(docs).as_posix()] = asset.read_bytes()
    config = yaml.safe_load((ROOT / "mkdocs.yml").read_text())
    config.update(site_url="https://docs.molopipeline.site/en/", docs_dir="source_en",
                  site_dir="site/en", edit_uri="", nav=map_nav(config["nav"]))
    config["extra"]["alternate"] = [
        {"name": "English", "link": "/en/", "lang": "en"},
        {"name": "简体中文", "link": "/", "lang": "zh"},
    ]
    files["mkdocs.en.yml"] = yaml.safe_dump(config, allow_unicode=True, sort_keys=False).encode()
    files["reference/source-contract.json"] = (ROOT / "reference/source-contract.json").read_bytes()
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    manifest = {"schema_version": 1, "canonical_repository": REPOSITORY,
                "canonical_revision": revision, "canonical_docs": "docs/",
                "page_mapping": PAGE_MAP,
                "files_sha256": {n: hashlib.sha256(v).hexdigest() for n, v in sorted(files.items())}}
    files["canonical-source.json"] = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode()
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    changes = []
    for relative, content in export_files().items():
        path = args.destination / relative
        if args.check:
            if not path.is_file() or path.read_bytes() != content:
                changes.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    if changes:
        raise SystemExit("Self-hosted mirror differs: " + ", ".join(changes))
    print("Self-hosted mirror checked" if args.check else "Self-hosted mirror exported")


if __name__ == "__main__":
    main()
