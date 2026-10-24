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
build_summary = HARNESS["build_summary"]
classify_mismatch = HARNESS["classify_mismatch"]


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
        self.assertIn("not", purpose)

    def test_harness_keeps_nfc_as_its_only_normalization(self):
        source = (ROOT / "scripts" / "compare_external_g2p.py").read_text(
            encoding="utf-8"
        )
        self.assertIn('unicodedata.normalize("NFC", value)', source)
        self.assertNotIn("ignore_tones=True", source)
        self.assertNotIn('replace("ː", "")', source)

    def test_implementation_agreement_is_never_reported_as_accuracy(self):
        summary = build_summary(
            [
                {
                    "exact_match": True,
                    "project_matches_fixture": True,
                    "external_matches_fixture": True,
                    "mismatch_category": None,
                },
                {
                    "exact_match": False,
                    "project_matches_fixture": True,
                    "external_matches_fixture": False,
                    "mismatch_category": "UNCLASSIFIED_REQUIRES_REVIEW",
                },
                {
                    "exact_match": False,
                    "project_matches_fixture": False,
                    "external_matches_fixture": False,
                    "mismatch_category": "RUNTIME_ERROR",
                },
            ],
            expected_count=3,
        )
        self.assertEqual(summary["implementation_agreement_rate"], 1 / 3)
        self.assertEqual(summary["exact_matches_between_implementations"], 1)
        self.assertEqual(summary["implementation_mismatches"], 1)
        self.assertEqual(summary["runtime_errors"], 1)
        self.assertEqual(summary["independent_gold_count"], 0)
        self.assertIsNone(summary["accuracy"])
        self.assertNotIn("exact_match_rate", summary)
        self.assertEqual(summary["score_status"], "NOT_SCORED_NO_INDEPENDENT_GOLD")
        source = (ROOT / "scripts" / "compare_external_g2p.py").read_text(encoding="utf-8")
        self.assertIn('return 2 if summary["runtime_errors"] else 0', source)
        self.assertNotIn("return 2 if runtime_errors else 0", source)


    def test_mismatch_categories_are_diagnostic_and_do_not_rewrite_raw_values(self):
        self.assertIsNone(classify_mismatch("kɤ", "kɤ"))
        self.assertEqual(classify_mismatch("kɤ", "kɤ˧˥"), "TONE_SUFFIX_ONLY")
        self.assertEqual(classify_mismatch("kiə", "kiːə˧˥"), "TONE_AND_LENGTH_DIFFERENCE")
        self.assertEqual(classify_mismatch("kai", "kaj˩˧"), "DIPHTHONG_OFFGLIDE_CONVENTION")
        self.assertEqual(classify_mismatch("kiːə", "keː˩˧iːə"), "SEGMENTAL_OR_VOWEL_SEQUENCE_DIFFERENCE")
        self.assertEqual(classify_mismatch(None, "kɤ"), "MISSING_OUTPUT")

    def test_summary_reports_review_categories_without_accuracy(self):
        summary = build_summary([
            {"exact_match": False, "project_matches_fixture": True, "external_matches_fixture": False, "mismatch_category": "TONE_SUFFIX_ONLY"},
            {"exact_match": False, "project_matches_fixture": True, "external_matches_fixture": False, "mismatch_category": "SEGMENTAL_OR_VOWEL_SEQUENCE_DIFFERENCE"},
        ], expected_count=2)
        self.assertEqual(summary["mismatch_category_counts"], {
            "SEGMENTAL_OR_VOWEL_SEQUENCE_DIFFERENCE": 1,
            "TONE_SUFFIX_ONLY": 1,
        })
        self.assertEqual(summary["independent_gold_count"], 0)
        self.assertIsNone(summary["accuracy"])
        self.assertEqual(summary["score_status"], "NOT_SCORED_NO_INDEPENDENT_GOLD")

if __name__ == "__main__":
    unittest.main()
