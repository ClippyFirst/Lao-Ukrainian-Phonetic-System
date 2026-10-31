import json
import unittest
from pathlib import Path

from lao_ukrainian import analyze
from lao_ukrainian.data import load_registry
from lao_ukrainian.parser import parse_syllable


class TestLaoLabializedOnsets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).parent / "fixtures" / "onset_cluster_cases.json"
        cls.fixture = json.loads(path.read_text(encoding="utf-8"))

    def test_registry_contains_all_source_listed_labialized_onsets(self):
        registry = load_registry()["onset_clusters"]
        self.assertEqual(len(registry), 11)
        self.assertEqual({row["ipa_initial"] for row in registry.values()},
                         {"tʷʰ", "tɕʷ", "kʷ", "kʷʰ", "ʔʷ", "sʷ", "ŋʷ", "lʷ"})

    def test_unambiguous_labialized_onsets_cross_the_ipa_boundary(self):
        for case in self.fixture["clusters"]:
            with self.subTest(case=case["id"]):
                parsed = parse_syllable(case["surface"])
                self.assertEqual(parsed["onset_form"], case["onset_form"])
                self.assertEqual(parsed["onset"], case["onset"])
                self.assertEqual(parsed["onset_class"], case["onset_class"])
                self.assertEqual(parsed["onset_ipa"], case["ipa"].removesuffix("it") if case["ipa"].endswith("it") else None)
                result = analyze(case["surface"])
                syllable = result.syllables[0]
                self.assertEqual(syllable.phonemic_ipa, case["ipa"])
                self.assertIsNone(syllable.practical_ukrainian)
                self.assertEqual(syllable.ukrainian_candidates, [])
                self.assertEqual(syllable.status, "EVIDENCE LIMITED")
                self.assertIn(f"ONSET-CLUSTER:{case['onset_form']}", syllable.rules)

    def test_attested_spelling_is_structurally_recognized_without_claiming_gold(self):
        for case in self.fixture["attested_spelling_controls"]:
            with self.subTest(case=case["id"]):
                parsed = parse_syllable(case["surface"])
                self.assertEqual(parsed["onset_form"], case["onset_form"])
                result = analyze(case["surface"])
                self.assertEqual(result.syllables[0].phonemic_ipa, case["ipa"])
                self.assertIsNone(result.syllables[0].practical_ukrainian)

    def test_overlapping_cw_aa_and_uo_open_rhyme_is_withheld(self):
        for case in self.fixture["ambiguous"]:
            with self.subTest(case=case["id"]):
                parsed = parse_syllable(case["surface"])
                self.assertIn(case["warning"], parsed["warnings"])
                result = analyze(case["surface"])
                syllable = result.syllables[0]
                self.assertIsNone(syllable.phonemic_ipa)
                self.assertIsNone(syllable.practical_ukrainian)
                self.assertIsNone(syllable.tone)
                self.assertEqual(result.status, "PARTIAL")

    def test_labialized_onset_before_rounded_vowel_is_not_accepted(self):
        for case in self.fixture["rounded_rejected"]:
            with self.subTest(case=case["id"]):
                parsed = parse_syllable(case["surface"])
                self.assertIn(case["warning"], parsed["warnings"])
                result = analyze(case["surface"])
                self.assertIsNone(result.syllables[0].phonemic_ipa)
                self.assertIsNone(result.syllables[0].practical_ukrainian)

    def test_preposed_vowel_precedes_silent_high_class_digraph_as_a_unit(self):
        for case in self.fixture["high_class_digraphs"]:
            with self.subTest(case=case["id"]):
                parsed = parse_syllable(case["surface"])
                self.assertEqual(parsed["onset_form"], case["onset_form"])
                self.assertEqual(parsed["onset"], case["onset"])
                self.assertEqual(parsed["onset_class"], case["onset_class"])
                result = analyze(case["surface"])
                self.assertEqual(result.syllables[0].phonemic_ipa, case["ipa"])


if __name__ == "__main__":
    unittest.main()
