"""Contract tests for the optional Lao external-G2P diagnostic harness.

These tests validate reproducibility safeguards, not pronunciation accuracy.
"""
import json
import runpy
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS = runpy.run_path(str(ROOT / "scripts" / "compare_external_g2p.py"))
nfc = HARNESS["nfc"]


class ExternalG2PHarnessTests(unittest.TestCase):
    def test_nfc_normalization_preserves_phonetic_distinctions(self):
        # Canonical Unicode equivalence is allowed; tone, length and syllable
        # boundaries must not be stripped to inflate exact-match rates.
        self.assertEqual(nfc("  kʰaː˥.ŋ  "), "  kʰaː˥.ŋ  ")
        self.assertEqual(nfc("a\u0304"), "ā")
        self.assertIsNone(nfc(None))

    def test_comparison_fixture_is_explicitly_engineering_only(self):
        fixture = json.loads(
            (ROOT / "tests" / "fixtures" / "vowel_precedence_cases.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertTrue(fixture["cases"])
        purpose = fixture.get("purpose", "").lower()
        self.assertTrue("engineering" in purpose or "regression" in purpose)
        # This fixture cannot be misrepresented as independently adjudicated gold.
        self.assertIn("not", purpose)

    def test_harness_keeps_nfc_as_its_only_normalization(self):
        source = (ROOT / "scripts" / "compare_external_g2p.py").read_text(
            encoding="utf-8"
        )
        self.assertIn('unicodedata.normalize("NFC", value)', source)
        self.assertNotIn("ignore_tones=True", source)
        self.assertNotIn('replace("ː", "")', source)


if __name__ == "__main__":
    unittest.main()
