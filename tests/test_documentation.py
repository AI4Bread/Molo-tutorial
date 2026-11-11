import ast
import importlib.util
import json
from pathlib import Path
import re
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = json.loads((ROOT / "reference/source-contract.json").read_text())


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DocumentationContractTests(unittest.TestCase):
    def test_complete_audited_entrypoints(self):
        self.assertEqual(len(CONTRACT["r_functions"]), 11)
        self.assertEqual(len(CONTRACT["python_cli"]), 37)
        self.assertEqual(len(CONTRACT["http_routes"]), 51)
        self.assertEqual(CONTRACT["web_app_version"], "1.6.0")

    def test_exact_current_integration_signature(self):
        f = next(f for f in CONTRACT["r_functions"] if f["name"] == "Molo_Integrate")
        p = {p["name"]: p["default"] for p in f["parameters"]}
        self.assertEqual(len(p), 43)
        self.assertEqual(p["py_path"], 'Sys.which("python")')
        self.assertEqual(p["sp_alignment"], '"Molo+LPGW"')
        self.assertEqual(p["dist_threshold"], "NULL")
        self.assertEqual(p["shared_dims"], "20")
        for old in ["tri_loss", "ggae_loss", "cos_loss", "bce_loss", "kl_loss", "K_h", "edge"]:
            self.assertNotIn(old, p)

    def test_promoted_weights_agree_between_R_and_CLI(self):
        f = next(f for f in CONTRACT["r_functions"] if f["name"] == "Molo_Integrate")
        r = {p["name"]: p["default"] for p in f["parameters"]}
        cli = {p["dest"]: p["default"] for p in CONTRACT["python_cli"]}
        for key, value in CONTRACT["integration_defaults"].items():
            r_key = key if key.endswith("scale") else key + "_loss"
            self.assertEqual(float(r[r_key]), value)
            self.assertEqual(float(cli[key]), value)
            self.assertIn(str(value), (ROOT / "docs/parameters.md").read_text())

    def test_distinct_neighbor_and_epoch_defaults(self):
        f = next(f for f in CONTRACT["r_functions"] if f["name"] == "Molo_reduction_cluster")
        self.assertEqual(next(p["default"] for p in f["parameters"] if p["name"] == "n_neighbors"), "20")
        route = next(r for r in CONTRACT["http_routes"] if r["handler"] == "submit_analysis")
        self.assertEqual(next(p["default"] for p in route["parameters"] if p["name"] == "n_neighbors"), "Form(30)")
        cli = {p["dest"]: p["default"] for p in CONTRACT["python_cli"]}
        self.assertEqual(cli["train_epoch"], "600")
        self.assertEqual(cli["pre_train_epoch"], "200")

    def test_current_authentication_and_no_legacy_router(self):
        routes = {(r["method"], r["path"]) for r in CONTRACT["http_routes"]}
        self.assertIn(("POST", "/api/auth/register/start"), routes)
        self.assertIn(("POST", "/auth/login"), routes)
        self.assertNotIn(("POST", "/api/email-verifications"), routes)
        self.assertNotIn(("POST", "/analyse/visium/run"), routes)
        f = next(r for r in CONTRACT["http_routes"] if r["handler"] == "run_alignment")
        names = {p["name"] for p in f["parameters"]}
        self.assertNotIn("email", names)
        self.assertNotIn("verification_code", names)
        self.assertIn("dataset_asset_ids", names)
        self.assertIn("tune_preset", names)

    def test_generated_tables_match_committed_contract(self):
        rendered = load_script("render_reference").render(CONTRACT)
        for name, expected in rendered.items():
            self.assertEqual((ROOT / "docs/reference" / name).read_text(), expected)

    def test_english_build_and_dependencies_are_explicit(self):
        config = yaml.safe_load((ROOT / "mkdocs.yml").read_text())
        self.assertEqual(config["theme"]["language"], "en")
        self.assertEqual(config["plugins"][0]["search"]["lang"], "en")
        self.assertTrue(config["strict"])
        rtd = yaml.safe_load((ROOT / ".readthedocs.yaml").read_text())
        self.assertEqual(rtd["python"]["install"], [{"requirements": "requirements-docs.txt"}])
        self.assertTrue(rtd["mkdocs"]["fail_on_warning"])

    def test_historical_page_urls_remain(self):
        for name in ["index", "introduction", "installation", "api", "basic_pipeline", "web", "FAQ"]:
            self.assertTrue((ROOT / "docs" / (name + ".md")).is_file())

    def test_ci_cache_uses_the_actual_documentation_requirements(self):
        workflow = yaml.safe_load((ROOT / ".github/workflows/docs.yml").read_text())
        setup = next(s for s in workflow["jobs"]["docs"]["steps"]
                     if s.get("uses", "").startswith("actions/setup-python@"))
        self.assertEqual(setup["with"]["cache-dependency-path"], "requirements-docs.txt")
        self.assertTrue((ROOT / setup["with"]["cache-dependency-path"]).is_file())

    def test_python_examples_are_syntactically_valid(self):
        count = 0
        for path in (ROOT / "docs").rglob("*.md"):
            for block in re.findall(r"```python\n(.*?)\n```", path.read_text(), re.S):
                ast.parse(block, filename=str(path))
                count += 1
        self.assertGreaterEqual(count, 4)

    def test_examples_do_not_use_obsolete_apis_or_literal_newlines(self):
        for path in (ROOT / "docs").rglob("*.md"):
            for block in re.findall(r"```(?:r|R|python|bash)\n(.*?)\n```", path.read_text(), re.S):
                self.assertNotIn("/api/email-verifications", block)
                self.assertNotIn("create_molo(", block)
                self.assertNotIn("Molo_web(", block)
                self.assertNotIn(r"\n", block)

    def test_source_contract_contains_no_runtime_file_content(self):
        for name, digest in CONTRACT["files_sha256"].items():
            self.assertNotIn("runtime/", name)
            self.assertNotIn(".env", name)
            self.assertRegex(digest, r"^[a-f0-9]{64}$")
        text = (ROOT / "reference/source-contract.json").read_text()
        for private in ["/mnt/sda/fulaiyi", "SMTP_PASSWORD=", "DOWNLOAD_TOKEN_SECRET=", "gho_"]:
            self.assertNotIn(private, text)


class StaticExtractionTests(unittest.TestCase):
    def test_nested_defaults_and_required_parameters(self):
        capture = load_script("capture_source_contract")
        self.assertEqual(capture.split_formals('obj, x = c(1, 2), y = "a,b", z = list(x=1)'), [
            {"name": "obj", "default": None},
            {"name": "x", "default": "c(1, 2)"},
            {"name": "y", "default": '"a,b"'},
            {"name": "z", "default": "list(x=1)"},
        ])

    def test_comment_masks_keep_strings_and_line_positions(self):
        capture = load_script("capture_source_contract")
        sample = '# Molo_Create <- function(x) {}\nMolo_Create <- function(obj, x="#") {}\n'
        f = list(capture.public_r_signatures(sample, "fixture.R"))
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0]["line"], 2)
        self.assertEqual(f[0]["parameters"][1]["default"], '"#"')

    def test_S4_generic_not_method_selects_defaults(self):
        capture = load_script("capture_source_contract")
        sample = ('setGeneric("Molo_traj", function(obj, plot_cols=NULL) {})\n'
                  'setMethod("Molo_traj", "Molo", function(obj, plot_cols) {})\n')
        f = list(capture.public_r_signatures(sample, "fixture.R"))
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0]["parameters"][1]["default"], "NULL")


if __name__ == "__main__":
    unittest.main()
