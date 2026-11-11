#!/usr/bin/env python3
"""Extract documentation contracts without importing/sourcing the Molo application.

Only public signatures, parser defaults, routes, and source hashes are exported.
Never pass a runtime directory or publish .env/data/database files.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re

REPO = Path(__file__).resolve().parents[1]
R_FILES = ["molo_analysis.R", "molo_convert.R", "molo_pipeline.R",
           "integrate/molo_integrate_v3_DLPFC_LA+MLP.R"]
R_NAMES = {"Molo_Create", "Molo_Convert", "Molo_Pipeline", "Molo_Integrate",
           "Molo_reduction_1", "Molo_reduction_cluster", "Molo_var_features",
           "Molo_top_GO_terms", "Molo_cell_chat", "Molo_traj", "Molo_save_data"}


def mask_comments(text):
    out, quote, escape, comment = [], None, False, False
    for c in text:
        if comment:
            out.append("\n" if c == "\n" else " ")
            if c == "\n":
                comment = False
        elif quote:
            out.append(c)
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == quote:
                quote = None
        elif c in "\"'`":
            quote = c
            out.append(c)
        elif c == "#":
            comment = True
            out.append(" ")
        else:
            out.append(c)
    return "".join(out)


def balanced(text, start):
    depth, quote, escape = 0, None, False
    for i in range(start, len(text)):
        c = text[i]
        if quote:
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == quote:
                quote = None
        elif c in "\"'`":
            quote = c
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return text[start + 1:i]
    raise ValueError("Unbalanced R signature")


def split_formals(text):
    parts, current, depth, quote, escape = [], [], 0, None, False
    for c in text + ",":
        if quote:
            current.append(c)
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == quote:
                quote = None
        elif c in "\"'`":
            quote = c
            current.append(c)
        elif c in "([{":
            depth += 1
            current.append(c)
        elif c in ")]}":
            depth -= 1
            current.append(c)
        elif c == "," and depth == 0:
            value = " ".join("".join(current).split())
            if value:
                name, sep, default = value.partition("=")
                parts.append({"name": name.strip(), "default": default.strip() if sep else None})
            current = []
        else:
            current.append(c)
    return parts


def public_r_signatures(text, path):
    text = mask_comments(text)
    patterns = [r'(?m)^\s*(Molo_\w+)\s*(?:<-|=)\s*function\s*\(',
                r'setGeneric\(\s*["\'](Molo_\w+)["\']\s*,\s*function\s*\(']
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            if match[1] in R_NAMES:
                yield {"name": match[1], "source": path,
                       "line": text[:match.end()].count("\n") + 1,
                       "parameters": split_formals(balanced(text, match.end() - 1))}


def expression(node):
    return ast.unparse(node) if node is not None else "required"


def extract(root):
    app = root / "Molo_FastAPI"
    files, functions, routes, cli, models = {}, [], [], [], []

    def read(path):
        rel = path.relative_to(root).as_posix()
        content = path.read_bytes()
        files[rel] = hashlib.sha256(content).hexdigest()
        return content.decode()

    for file in R_FILES:
        path = app / "app/core/R" / file
        functions.extend(public_r_signatures(read(path), path.relative_to(root).as_posix()))
    assert {f["name"] for f in functions} == R_NAMES
    assert len(functions) == len(R_NAMES), "Duplicate public R definitions"
    defaults_tree = ast.parse(read(app / "app/core/python/molo_defaults.py"))
    defaults = {}
    for node in defaults_tree.body:
        if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", "") == "DEFAULT_INTEGRATION_PARAMS":
            defaults = ast.literal_eval(node.value)
    cli_tree = ast.parse(read(app / "app/core/python/main_process.py"))
    for node in ast.walk(cli_tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "add_argument":
            kws = {k.arg: k.value for k in node.keywords}
            default = kws.get("default")
            value = expression(default) if default is not None else "None"
            if isinstance(default, ast.Subscript) and isinstance(default.value, ast.Name) and default.value.id == "DEFAULT_INTEGRATION_PARAMS":
                value = repr(defaults[ast.literal_eval(default.slice)])
            cli.append({"flags": [ast.literal_eval(a) for a in node.args],
                        "dest": ast.literal_eval(kws["dest"]),
                        "default": "required" if "required" in kws and ast.literal_eval(kws["required"]) else value,
                        "type": expression(kws.get("type")) if "type" in kws else "string/untyped",
                        "line": node.lineno})
    main_text = read(app / "app/main.py")
    main_tree = ast.parse(main_text)
    mounted = {n.args[0].value.id for n in ast.walk(main_tree)
               if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
               and n.func.attr == "include_router" and n.args and isinstance(n.args[0], ast.Attribute)}
    version = next(ast.literal_eval(n.value) for n in main_tree.body
                   if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "APP_VERSION" for t in n.targets))
    for name in sorted(mounted):
        path = app / "app/routers" / (name + ".py")
        tree = ast.parse(read(path))
        prefix = ""
        for node in tree.body:
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call) and getattr(node.value.func, "id", "") == "APIRouter":
                prefix = next((ast.literal_eval(k.value) for k in node.value.keywords if k.arg == "prefix"), "")
            if isinstance(node, ast.ClassDef) and any(getattr(b, "id", "") == "BaseModel" for b in node.bases):
                fields = [{"name": n.target.id, "type": expression(n.annotation),
                           "default": expression(n.value)} for n in node.body if isinstance(n, ast.AnnAssign)]
                models.append({"name": node.name, "fields": fields})
            if not isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
                continue
            args = node.args.args
            defaults_list = [None] * (len(args) - len(node.args.defaults)) + node.args.defaults
            parameters = [{"name": arg.arg, "type": expression(arg.annotation), "default": expression(default)}
                          for arg, default in zip(args, defaults_list)
                          if arg.arg not in {"request", "background_tasks"}]
            for dec in node.decorator_list:
                if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute) and getattr(dec.func.value, "id", "") == "router":
                    methods = next((ast.literal_eval(k.value) for k in dec.keywords if k.arg == "methods"), [dec.func.attr.upper()])
                    if dec.func.attr not in {"get", "post", "patch", "delete", "put", "api_route"}:
                        continue
                    for method in methods:
                        routes.append({"method": method, "path": prefix + ast.literal_eval(dec.args[0]),
                                       "source": path.relative_to(root).as_posix(), "line": node.lineno,
                                       "handler": node.name, "parameters": parameters})
    # Additional files cited by prose: hash, do not publish their contents.
    extras = ["app/core/R/run_alignment_wrapper.R", "app/core/python/molo_tuner.py",
              "app/services/alignment_service.py", "app/services/app_settings.py",
              "app/services/runtime_settings.py", "app/services/auth_service.py",
              "app/services/reviewer_mode.py", "app/services/dataset_validator.py",
              "app/celery_app.py", "app/config/downstream.example.yaml", "requirements.txt"]
    for file in extras:
        read(app / file)
    return {"schema_version": 1, "audited_on": "2026-11-11", "web_app_version": version,
            "scope": "read-only working-source snapshot; no scientific execution; source tree is dirty",
            "source_repository": "https://github.com/AI4Bread/Molo",
            "source_base_commit": "878014a82d75732b5795008378311b000dc897d6",
            "files_sha256": dict(sorted(files.items())),
            "r_functions": sorted(functions, key=lambda x: x["name"]),
            "python_cli": cli, "integration_defaults": defaults,
            "http_routes": sorted(routes, key=lambda x: (x["path"], x["method"])),
            "request_models": models}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=REPO / "reference/source-contract.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = json.dumps(extract(args.source_root), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if args.output.read_text() != result:
            raise SystemExit("Source contract drift detected; review before regenerating")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result)
    print("Source contract checked" if args.check else "Source contract captured")


if __name__ == "__main__":
    main()
