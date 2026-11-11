#!/usr/bin/env python3
"""Render reference tables from the committed, source-audited public contract."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def cell(value):
    return str(value).replace("|", "&#124;").replace("\n", " ")


def render(contract):
    intro = ("\nSource-audited on **2026-11-11**, Web app **1.6.0**. "
             "Generated from the [source contract](../provenance.md); do not edit tables by hand. "
             "Defaults below are **entry-point defaults**, not universal recommendations.\n\n")
    r = "# Complete R parameters\n" + intro
    for f in contract["r_functions"]:
        r += f"## `{f['name']}`\n\nSource: `{f['source']}` (line {f['line']}).\n\n"
        r += "```r\n" + f["name"] + "(\n"
        r += ",\n".join("  " + p["name"] + (" = " + p["default"] if p["default"] is not None else "") for p in f["parameters"])
        r += "\n)\n```\n\n| Parameter | Default expression |\n| --- | --- |\n"
        for p in f["parameters"]:
            r += f"| `{p['name']}` | `{cell(p['default'])}` |\n" if p["default"] is not None else f"| `{p['name']}` | **required** |\n"
        r += "\n"
    cli = "# Complete Python CLI options\n" + intro
    cli += "Use these flags with `Molo_FastAPI/app/core/python/main_process.py`, not with an R function or a web form.\n\n"
    cli += "| Flag | Destination | Type | Parser default |\n| --- | --- | --- | --- |\n"
    for p in contract["python_cli"]:
        cli += f"| `{cell(', '.join(p['flags']))}` | `{p['dest']}` | `{p['type']}` | `{cell(p['default'])}` |\n"
    http = "# Complete HTTP routes\n" + intro
    http += ("Only routers mounted by `app/main.py` are listed. Static files and framework-generated OpenAPI routes are omitted. "
             "Form/File declarations are form data, not JSON. Session authentication normally applies; see the [HTTP guide](../http-api.md). "
             "An omitted form field uses its declared default, but services can enforce additional constraints.\n\n")
    http += "| Method | Path | Handler | Parameters |\n| --- | --- | --- | --- |\n"
    for route in contract["http_routes"]:
        params = "; ".join(f"{p['name']}: {p['type']} = {p['default']}" for p in route["parameters"]) or "none"
        http += f"| {route['method']} | `{route['path']}` | `{route['handler']}` | {cell(params)} |\n"
    http += "\n## JSON request models\n\n"
    for model in contract["request_models"]:
        http += f"### `{model['name']}`\n\n| Field | Type | Default |\n| --- | --- | --- |\n"
        for p in model["fields"]:
            http += f"| `{p['name']}` | `{cell(p['type'])}` | `{cell(p['default'])}` |\n"
        http += "\n"
    return {name: text.rstrip() + "\n" for name, text in
            {"r-parameters.md": r, "cli-options.md": cli, "http-routes.md": http}.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    contract = json.loads((ROOT / "reference/source-contract.json").read_text())
    out = ROOT / "docs/reference"
    out.mkdir(parents=True, exist_ok=True)
    for name, text in render(contract).items():
        p = out / name
        if args.check:
            if not p.exists() or p.read_text() != text:
                raise SystemExit(f"Generated reference is stale: {p}")
        else:
            p.write_text(text)
    print("Generated references match contract" if args.check else "Generated references rendered")


if __name__ == "__main__":
    main()
