"""Pure helper tests for the benchmark's contour/category alignment."""

import unittest

from scripts.benchmark_mekongphon_three_engines import (
    extract_tone_suffix,
    parse_mekong_tone_categories,
    render_mekong_tonal,
    length_marker_metrics,
    word_final_coda_metrics,
    syllable_boundary_availability,
    strip_tone_symbols,
    validate_lexicon_split,
)


class MekongPhonBenchmarkHelperTests(unittest.TestCase):
    def test_tone_suffix_extraction_preserves_inserted_contours(self):
        self.assertEqual(extract_tone_suffix("kaː", "kaː˩˧"), "˩˧")
        self.assertEqual(extract_tone_suffix("kʰaːp", "kʰaː˩˧p˧˥"), "˩˧˧˥")

    def test_suffix_extraction_fails_closed_when_segmental_sequence_is_not_present(self):
        self.assertIsNone(extract_tone_suffix("kaː", "kɔː˩˧"))

    def test_mekong_contour_notation_maps_to_five_tone_categories(self):
        suffix = "˩˧˧˥˧˧˩˥˨"
        self.assertEqual(
            parse_mekong_tone_categories(suffix),
            ["low-rising", "high-rising", "high-mid", "low-falling", "high-falling"],
        )

    def test_typed_categories_can_be_rendered_in_benchmark_notation(self):
        self.assertEqual(
            render_mekong_tonal(["kaː", "pa"], ["low-rising", "high-mid"]),
            "kaː˩˧pa˧",
        )
        self.assertEqual(render_mekong_tonal(["kaː"], ["unknown"]), "")
        self.assertEqual(render_mekong_tonal([], ["low-rising"]), "")

    def test_length_marker_metrics_are_word_level_and_keep_coverage(self):
        result = length_marker_metrics(
            ["kʰaːŋ", "ka", "paː"],
            ["kʰaŋ", "ka", ""],
        )
        self.assertEqual(result["covered_items"], 2)
        self.assertEqual(result["reference_long_vowel_marker_total"], 2)
        self.assertEqual(result["prediction_long_vowel_marker_total"], 0)
        self.assertEqual(result["items_with_exact_marker_count"], 1)

    def test_word_final_coda_metrics_use_only_core_inventory(self):
        result = word_final_coda_metrics(
            ["kʰaːŋ", "kʰaː", "kʰaːl"],
            ["kʰaːn", "kʰaːŋ", "kʰaːl"],
            {"p", "t", "k", "ʔ", "m", "n", "ŋ", "w", "j"},
            {"l", "r"},
        )
        self.assertEqual(result["scorable_items"], 2)
        self.assertEqual(result["word_final_coda_presence_accuracy"], 0.5)
        self.assertEqual(result["reference_coda_identity_items"], 1)
        self.assertEqual(result["coda_identity_exact_items"], 0)

    def test_boundary_metric_is_explicitly_unavailable_without_reference_marks(self):
        result = syllable_boundary_availability(
            ["kʰaːŋ", "tʰiːlaŋ"],
            ["kʰaːŋ˩˧", "tʰiː˧˥laŋ˩˧"],
        )
        self.assertEqual(result["status"], "NOT_SCORABLE")
        self.assertEqual(result["segmental_reference_items_with_explicit_boundaries"], 0)
        self.assertEqual(result["tonal_reference_items_with_explicit_boundaries"], 0)

    def test_tone_stripping_preserves_segmental_length(self):
        self.assertEqual(strip_tone_symbols("kʰaː˩˧"), "kʰaː")

    def test_train_and_eval_lexicons_are_checked_for_overlap(self):
        stats = validate_lexicon_split(
            [{"orth": "ກ"}, {"orth": "ຂ"}, {"orth": "ກ"}],
            [{"orth": f"ຄ{i}"} for i in range(100)],
        )
        self.assertEqual(stats["train_eval_overlap"], 0)
        with self.assertRaises(ValueError):
            validate_lexicon_split(
                [{"orth": "ກ"}],
                [{"orth": "ກ"}] + [{"orth": f"ຂ{i}"} for i in range(99)],
            )

    def test_unknown_contour_sequence_is_not_guessed(self):
        self.assertIsNone(parse_mekong_tone_categories("˩˥"))


if __name__ == "__main__":
    unittest.main()
