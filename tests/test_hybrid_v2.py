import unittest

from lao_ukrainian.core import analyze
from lao_ukrainian.hybrid_v2 import combine_neural_tones


class HybridV2Tests(unittest.TestCase):
    def test_neural_tone_overlay_keeps_deterministic_segmental_ipa_and_target(self):
        baseline = analyze("ຂາ")
        original = baseline.syllables[0]
        result = combine_neural_tones(
            baseline, "kʰaː˧˥",
            model_id="byumatrixlab/lao-ipa-tonal",
            model_revision="a" * 40,
        )
        updated = result.analysis.syllables[0]
        self.assertEqual(result.tone_alignment_status, "ORDER_ALIGNED")
        self.assertEqual(result.tone_overlays, 1)
        self.assertEqual(updated.phonemic_ipa, original.phonemic_ipa)
        self.assertEqual(updated.practical_ukrainian, original.practical_ukrainian)
        self.assertEqual(updated.tone_contour, "˧˥")
        self.assertEqual(updated.phonetic_result.tone_category, "high-rising")
        self.assertTrue(all(segment.certainty == "UNCERTAIN" for segment in updated.phonetic_result.segments if segment.kind == "tone"))
        self.assertEqual(updated.phonetic_result.phonemic_ipa, original.phonetic_result.phonemic_ipa)
        self.assertIn(
            "HYBRID-V2:DETERMINISTIC-SEGMENTAL+NEURAL-TONE",
            updated.rules,
        )

    def test_two_syllables_require_exact_alignment_and_preserve_per_syllable_tones(self):
        result = combine_neural_tones(
            analyze("ຂາຢາ"),
            "kʰaː˩˧jaː˧˥",
            model_id="byumatrixlab/lao-ipa-tonal",
            model_revision="a" * 40,
        )
        self.assertEqual(result.tone_alignment_status, "ORDER_ALIGNED")
        self.assertEqual(result.aligned_syllables, 2)
        self.assertEqual(result.tone_overlays, 2)
        self.assertEqual(
            [item.tone_contour for item in result.analysis.syllables],
            ["˩˧", "˧˥"],
        )

    def test_syllable_count_mismatch_withholds_all_neural_tones(self):
        baseline = analyze("ຂາຢາ")
        result = combine_neural_tones(
            baseline, "kʰaː˧˥",
            model_id="byumatrixlab/lao-ipa-tonal",
            model_revision="a" * 40,
        )
        self.assertEqual(result.tone_alignment_status, "NOT_ALIGNED")
        self.assertEqual(result.tone_overlays, 0)
        self.assertTrue(any("SEQUENCE-NOT-UNIQUELY-ALIGNED" in warning for warning in result.warnings))

    def test_unsupported_neural_ipa_withholds_tones(self):
        result = combine_neural_tones(
            analyze("ຂາ"), "ɕaː˧˥",
            model_id="byumatrixlab/lao-ipa-tonal",
            model_revision="a" * 40,
        )
        self.assertEqual(result.tone_alignment_status, "NOT_ALIGNED")
        self.assertEqual(result.tone_overlays, 0)
        self.assertIn("NEURAL-IPA-UNSUPPORTED; tone overlay withheld", result.warnings)

    def test_unknown_contour_is_not_promoted(self):
        result = combine_neural_tones(
            analyze("ຂາ"), "kʰaː˩˥",
            model_id="byumatrixlab/lao-ipa-tonal",
            model_revision="a" * 40,
        )
        self.assertEqual(result.tone_overlays, 0)
        self.assertEqual(result.skipped_tone_units, 1)

    def test_input_analysis_is_not_mutated(self):
        baseline = analyze("ຂາ")
        original_contour = baseline.syllables[0].tone_contour
        combine_neural_tones(
            baseline, "kʰaː˧˥",
            model_id="byumatrixlab/lao-ipa-tonal",
            model_revision="a" * 40,
        )
        self.assertEqual(baseline.syllables[0].tone_contour, original_contour)


if __name__ == "__main__":
    unittest.main()
