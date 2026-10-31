import json
import unittest
from pathlib import Path

from lao_ukrainian import analyze
from lao_ukrainian.parser import parse_syllable


class TestToneMarkStorageOrder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).parent / "fixtures" / "tone_mark_order_cases.json"
        cls.fixture = json.loads(path.read_text(encoding="utf-8"))

    def test_fixture_valid_mark_positions_remain_supported(self):
        for case in self.fixture["valid"]:
            with self.subTest(case=case["id"]):
                parsed = parse_syllable(case["surface"])
                self.assertFalse(
                    any(w.startswith("MALFORMED_TONE_MARK_") for w in parsed["warnings"]),
                    parsed["warnings"],
                )
                result = analyze(case["surface"])
                self.assertIsNotNone(result.syllables[0].phonemic_ipa)
                self.assertFalse(any(w.startswith("MALFORMED_TONE_MARK_") for w in result.syllables[0].warnings))

    def test_fixture_invalid_mark_positions_withhold_phonetic_result(self):
        for case in self.fixture["invalid"]:
            with self.subTest(case=case["id"]):
                parsed = parse_syllable(case["surface"])
                self.assertTrue(
                    any(w.startswith("MALFORMED_TONE_MARK_") for w in parsed["warnings"]),
                    parsed["warnings"],
                )
                result = analyze(case["surface"])
                syllable = result.syllables[0]
                self.assertIsNone(syllable.phonemic_ipa)
                self.assertIsNone(syllable.practical_ukrainian)
                self.assertEqual(syllable.ukrainian_candidates, [])
                self.assertIsNone(syllable.tone)
                self.assertEqual(syllable.status, "EVIDENCE LIMITED")


if __name__ == "__main__":
    unittest.main()
