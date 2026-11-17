import csv
import unittest
from pathlib import Path

from lao_ukrainian.data import load_registry
from lao_ukrainian.parser import parse_syllable


ROOT = Path(__file__).resolve().parents[1]


class TestLaoGlottalEvidenceBoundary(unittest.TestCase):
    def test_short_vowel_glottal_claims_are_source_scoped(self):
        with (ROOT / "data/evidence/sources.csv").open(encoding="utf-8", newline="") as stream:
            sources = {row["source_id"] for row in csv.DictReader(stream)}
        with (ROOT / "data/evidence/claims.csv").open(encoding="utf-8", newline="") as stream:
            claims = {row["claim_id"]: row for row in csv.DictReader(stream)}

        self.assertIn("SRC-UEDA", sources)
        self.assertIn("SRC-LEW-2014", sources)
        self.assertIn("SRC-COLE-LAO-PROSODY-2016", sources)

        ueda = claims["CLM-LAO-UEDA-LIGHT-SYLLABLE-SCOPE"]
        self.assertEqual(ueda["status"], "established_scoped")
        self.assertEqual(ueda["evidence_ids"], "SRC-UEDA")

        conflict = claims["CLM-LAO-SHORT-VOWEL-GLOTTAL-ANALYSIS-CONFLICT"]
        self.assertEqual(conflict["status"], "analysis_dependent")
        self.assertEqual(
            set(conflict["evidence_ids"].split(";")),
            {
                "SRC-UEDA",
                "SRC-LEW-2014",
                "SRC-COLE-LAO-PROSODY-2016",
                "SRC-ISHIDA-ORTHO-2026",
            },
        )
        self.assertTrue(set(conflict["evidence_ids"].split(";")) <= sources)

    def test_open_short_vowel_has_no_invented_orthographic_coda(self):
        parsed = parse_syllable("ກະ", load_registry())
        self.assertEqual(parsed["vowel"]["id"], "A")
        self.assertIsNone(parsed["coda"])
        self.assertEqual(parsed["warnings"], [])


if __name__ == "__main__":
    unittest.main()
