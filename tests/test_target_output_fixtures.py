"""Shared regression tests for the IPA-first Ukrainian target adapter."""
import json
import unittest
from pathlib import Path

from lao_ukrainian import analyze


FIXTURE = Path(__file__).parent / "fixtures" / "target_output_cases.json"


class TestTargetOutputFixtures(unittest.TestCase):
    def test_syllable_initial_yodation_and_w_glide_in_real_lao_analysis(self):
        cases = {
            "ຢາ": ("jaː", "я"),
            "ເຢ": ("jeː", "є"),
            "ຢີ": ("jiː", "ї"),
            "ຢູ": ("juː", "ю"),
            "ເຂົາ": ("kʰaw", "к'ав"),
        }
        for surface, expected in cases.items():
            with self.subTest(surface=surface):
                result = analyze(surface)
                self.assertEqual(len(result.syllables), 1)
                self.assertEqual(result.syllables[0].phonemic_ipa, expected[0])
                self.assertEqual(result.syllables[0].practical_ukrainian, expected[1])

    def test_shared_ipa_to_ukrainian_cases(self):
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(fixture["schema_version"], 1)
        for case in fixture["cases"]:
            with self.subTest(case=case["id"]):
                result = analyze(case["surface"])
                self.assertEqual(len(result.syllables), 1)
                syllable = result.syllables[0]
                self.assertEqual(syllable.phonemic_ipa, case["phonemic_ipa"])
                self.assertEqual(syllable.practical_ukrainian, case["ukrainian"])


if __name__ == "__main__":
    unittest.main()
