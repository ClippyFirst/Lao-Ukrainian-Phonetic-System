"""Word-level segmentation regressions; not an independently adjudicated IPA gold set."""

import unittest

from lao_ukrainian import analyze
from lao_ukrainian.parser import segment_syllables


class MultisyllableSegmentationTests(unittest.TestCase):
    def test_unspaced_common_words_are_segmented_into_syllables(self):
        cases = {
            "ສະບາຍດີ": ["ສະ", "ບາຍ", "ດີ"],
            "ຂອບໃຈ": ["ຂອບ", "ໃຈ"],
        }
        for source, expected in cases.items():
            with self.subTest(source=source):
                self.assertEqual(segment_syllables(source), expected)

    def test_every_recognized_syllable_is_analyzed_in_sequence(self):
        result = analyze("ສະບາຍດີ")
        self.assertEqual([item.surface for item in result.syllables], ["ສະ", "ບາຍ", "ດີ"])
        self.assertTrue(all(item.phonemic_ipa for item in result.syllables))
        self.assertEqual(result.status, "OK")

    def test_zwsp_is_an_explicit_boundary_and_spaces_remain_phrase_boundaries(self):
        self.assertEqual(segment_syllables("ສະ\u200bບາຍ ດີ"), ["ສະ", "ບາຍ", "ດີ"])

    def test_unsupported_material_is_retained_as_a_partial_unit(self):
        source = "ສະxບາຍ"
        parts = segment_syllables(source)
        self.assertEqual("".join(parts), source)
        result = analyze(source)
        self.assertEqual("".join(item.surface for item in result.syllables), source)
        self.assertTrue(any(item.phonemic_ipa is None for item in result.syllables))
        self.assertEqual(result.status, "PARTIAL")

    def test_stranded_registered_onset_does_not_receive_a_prefix_pronunciation(self):
        source = "ກາລ"
        self.assertEqual(segment_syllables(source), [source])
        syllable = analyze(source).syllables[0]
        self.assertIsNone(syllable.phonemic_ipa)
        self.assertEqual(syllable.status, "EVIDENCE LIMITED")

    def test_non_core_lao_character_remains_visible_beside_a_valid_syllable(self):
        result = analyze("ຄົນຆ")
        self.assertEqual([item.surface for item in result.syllables], ["ຄົນ", "ຆ"])
        self.assertIsNotNone(result.syllables[0].phonemic_ipa)
        self.assertIsNone(result.syllables[1].phonemic_ipa)
        self.assertEqual(result.status, "PARTIAL")

    def test_tone_marks_are_validated_per_syllable_within_a_word(self):
        source = "ກ່າຂ່າ"
        self.assertEqual(segment_syllables(source), ["ກ່າ", "ຂ່າ"])
        result = analyze(source)
        self.assertEqual([item.surface for item in result.syllables], ["ກ່າ", "ຂ່າ"])
        self.assertTrue(all(item.phonemic_ipa for item in result.syllables))

    def test_multiple_tone_marks_are_not_rescued_by_segmentation(self):
        source = "ກ່້າ"
        self.assertEqual(segment_syllables(source), [source])
        syllable = analyze(source).syllables[0]
        self.assertIsNone(syllable.phonemic_ipa)
        self.assertIn("MULTIPLE_TONE_MARKS", syllable.warnings)


if __name__ == "__main__":
    unittest.main()
