"""Semantic and publishing-contract checks; no scientific code is executed."""
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("export_selfhosted", ROOT / "scripts/export_selfhosted.py")
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)


class ArchitectureAndMirrorTests(unittest.TestCase):
    def test_architecture_covers_active_model_and_boundaries(self):
        text = (ROOT / "docs/architecture.md").read_text()
        for term in ["enc_a", "enc_b", "FeatureDecoder", "Translator", "KL_shared", "KL_private",
                     "translator_cycle_MSE", "MNN", "NC", "GME", "exactly two batches",
                     "does **not** instantiate/train", "zero-filled", "ra2_three_stage"]:
            self.assertIn(term, text)

    def test_architecture_sources_have_audited_hashes(self):
        contract = json.loads((ROOT / "reference/source-contract.json").read_text())
        for file in ["model.py", "compute_MNN.py", "compute_NC.py", "compute_GME.py",
                     "image_trans.py", "molo_three_stage_alignment.py"]:
            self.assertTrue(any(k.endswith("/" + file) for k in contract["files_sha256"]))

    def test_export_preserves_legacy_api_meaning(self):
        text = "[R](api.md#x) [HTTP](http-api.md) [external](https://example.org/api.md)"
        self.assertEqual(exporter.rewrite_links(text),
                         "[R](r-functions.md#x) [HTTP](api.md) [external](https://example.org/api.md)")
        self.assertEqual(exporter.PAGE_MAP["web.md"], "web-workflow.md")
        self.assertEqual(exporter.PAGE_MAP["FAQ.md"], "faq.md")

    def test_mirror_hashes_and_every_page_covered(self):
        files = exporter.export_files()
        manifest = json.loads(files["canonical-source.json"])
        for name, digest in manifest["files_sha256"].items():
            self.assertEqual(hashlib.sha256(files[name]).hexdigest(), digest)
        self.assertEqual(len(manifest["page_mapping"]), 19)
        self.assertIn(b"/api/auth/register/start", files["source_en/api.md"])
        self.assertIn(b"sp_var_features=FALSE", files["source_en/r-functions.md"])


if __name__ == "__main__":
    unittest.main()
