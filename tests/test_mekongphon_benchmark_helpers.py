"""Pure helper tests for the benchmark's contour/category alignment."""

import unittest

from scripts.benchmark_mekongphon_three_engines import (
    extract_tone_suffix,
    parse_mekong_tone_categories,
    render_mekong_tonal,
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
            render_mekong_tonal("kaː", ["low-rising", "high-mid"]),
            "kaː˩˧˧",
        )
        self.assertEqual(render_mekong_tonal("kaː", ["unknown"]), "")
        self.assertEqual(render_mekong_tonal("", ["low-rising"]), "")

    def test_unknown_contour_sequence_is_not_guessed(self):
        self.assertIsNone(parse_mekong_tone_categories("˩˥"))


if __name__ == "__main__":
    unittest.main()
