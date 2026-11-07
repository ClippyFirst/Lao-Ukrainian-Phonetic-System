import unittest

from scripts.diagnose_mekongphon_train_split import (
    alignment_error_profile,
    extract_tone_suffix,
    levenshtein,
    parse_tone_categories,
    warning_code,
)


class MekongPhonTrainDiagnosticTests(unittest.TestCase):
    def test_extracts_interleaved_tone_contours_without_changing_segments(self):
        self.assertEqual(extract_tone_suffix("kaːpa", "kaː˩˧pa˧"), "˩˧˧")

    def test_rejects_segmental_reference_that_is_not_a_subsequence(self):
        self.assertIsNone(extract_tone_suffix("kʰaː", "kɔː˩˧"))

    def test_parses_longest_mekong_contours_first(self):
        self.assertEqual(
            parse_tone_categories("˩˧˧˥˧˧˩˥˨"),
            ["low-rising", "high-rising", "high-mid", "low-falling", "high-falling"],
        )

    def test_unknown_contour_fails_closed(self):
        self.assertIsNone(parse_tone_categories("˩˥"))

    def test_alignment_profile_aggregates_segmental_edits_only(self):
        profile = alignment_error_profile(["kʰaː", "pa"], ["kʰɔː", "pa"])
        self.assertEqual(profile["total_substitutions"], 1)
        self.assertEqual(profile["top_substitutions"][0], {"pair": "a=>ɔ", "count": 1})

    def test_warning_code_drops_source_derived_tail_payload(self):
        self.assertEqual(warning_code("UNCONSUMED_AFTER_VOWEL:ມເປັນລະບຽບ"), "UNCONSUMED_AFTER_VOWEL")

    def test_levenshtein_handles_empty_and_unicode_strings(self):
        self.assertEqual(levenshtein("", "ກ"), 1)
        self.assertEqual(levenshtein("kʰaː", "kʰɔː"), 1)


if __name__ == "__main__":
    unittest.main()
