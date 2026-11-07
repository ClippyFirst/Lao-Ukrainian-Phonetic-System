import unittest

from lao_ukrainian import analyze, segment_unspaced_token


class TestConservativeUnspacedSyllabification(unittest.TestCase):
    def test_unique_structural_path_segments_unspaced_lao(self):
        self.assertEqual(
            segment_unspaced_token("ສະບາຍດີ"),
            ["ສະ", "ບາຍ", "ດີ"],
        )

    def test_phrase_mode_runs_each_syllable_through_existing_ipa_pipeline(self):
        result = analyze("ສະບາຍດີ", infer_unspaced=True)
        self.assertEqual([row.surface for row in result.syllables], ["ສະ", "ບາຍ", "ດີ"])
        self.assertTrue(all(row.phonetic_result is not None for row in result.syllables))
        self.assertTrue(all(row.phonemic_ipa for row in result.syllables))

    def test_default_api_contract_remains_syllable_oriented(self):
        result = analyze("ສະບາຍດີ")
        self.assertEqual(len(result.syllables), 1)
        self.assertEqual(result.syllables[0].surface, "ສະບາຍດີ")

    def test_ambiguous_or_malformed_token_is_not_guessed(self):
        self.assertIsNone(segment_unspaced_token("ກາລ"))

    def test_tone_mark_stays_attached_to_its_syllable(self):
        self.assertEqual(
            segment_unspaced_token("ກ່າບາຍ"),
            ["ກ່າ", "ບາຍ"],
        )

    def test_explicit_zero_width_space_remains_a_boundary(self):
        result = analyze("ສະບາຍ\u200bດີ", infer_unspaced=True)
        self.assertEqual([row.surface for row in result.syllables], ["ສະ", "ບາຍ", "ດີ"])


if __name__ == "__main__":
    unittest.main()
