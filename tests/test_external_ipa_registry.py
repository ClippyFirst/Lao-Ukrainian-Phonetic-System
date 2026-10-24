"""Contract tests for the external IPA/G2P candidate registry.

The registry is research metadata, not an enabled runtime dependency.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "external-ipa-renderers.json"


class ExternalIpaRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def test_manifest_has_required_top_level_contract(self):
        data = self.registry
        self.assertEqual(data["schema_version"], "1.0")
        self.assertTrue(data["language"]["name"])
        self.assertTrue(data["language"]["iso_639_3_or_639_1"])
        self.assertTrue(data["integration_contract"]["pipeline"])
        self.assertIn("tone", " ".join(data["integration_contract"]["preserve"]).lower())
        self.assertTrue(data["integration_contract"]["prohibited"])

    def test_candidates_have_unique_ids_and_valid_https_links(self):
        candidates = self.registry["candidates"]
        self.assertGreater(len(candidates), 0)
        ids = [item["id"] for item in candidates]
        self.assertEqual(len(ids), len(set(ids)))
        for item in candidates:
            with self.subTest(candidate=item.get("id")):
                self.assertRegex(item["id"], re.compile(r"^[a-z0-9][a-z0-9-]*$"))
                self.assertTrue(item["name"])
                self.assertTrue(item["kind"])
                self.assertTrue(item["output"])
                self.assertTrue(item["license"])
                self.assertRegex(item["url"], r"^https?://")
                self.assertIn(item["status"], {"candidate", "benchmark-resource", "supporting-tool", "display-only"})

    def test_unverified_candidates_cannot_be_enabled_by_default(self):
        for item in self.registry["candidates"]:
            with self.subTest(candidate=item["id"]):
                self.assertIs(item["verified_in_repo"], False)
                self.assertIs(item["enabled_by_default"], False)

    def test_renderer_and_g2p_candidates_cannot_bypass_ipa_boundary(self):
        contract = self.registry["integration_contract"]
        pipeline = contract["pipeline"].lower()
        self.assertIn("ipa", pipeline)
        self.assertIn("ukrainian", pipeline)
        prohibited = " ".join(contract["prohibited"]).lower()
        self.assertIn("direct source-grapheme-to-ukrainian", prohibited)


if __name__ == "__main__":
    unittest.main()
