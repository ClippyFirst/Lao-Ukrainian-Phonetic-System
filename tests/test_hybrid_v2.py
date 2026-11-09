import json
import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from lao_ukrainian.core import analyze
from lao_ukrainian.hybrid_v2 import combine_neural_tones, run_hybrid_v2
from lao_ukrainian.cli import main as cli_main


class HybridV2Tests(unittest.TestCase):
    def test_two_lanes_preserve_deterministic_target_and_full_neural_tonal_ipa(self):
        baseline = analyze("ຂາ")
        original = baseline.syllables[0]
        raw = "kʰaː˧˥"
        result = combine_neural_tones(
            baseline, raw,
            model_id="byumatrixlab/lao-ipa-tonal",
            model_revision="a" * 40,
        )
        self.assertEqual(result.tone_alignment_status, "ORDER_ALIGNED")
        self.assertEqual(len(result.tone_predictions), 1)
        prediction = result.tone_predictions[0]
        self.assertEqual(prediction.contour, "˧˥")
        self.assertEqual(prediction.category, "high-rising")
        self.assertEqual(prediction.certainty, "UNCERTAIN")
        self.assertEqual(result.tonal_ipa, raw)
        self.assertEqual(result.analysis.syllables[0].phonemic_ipa, original.phonemic_ipa)
        self.assertEqual(result.analysis.syllables[0].tone_contour, original.tone_contour)
        self.assertEqual(result.analysis.syllables[0].practical_ukrainian, original.practical_ukrainian)

    def test_multisyllable_tones_are_associated_by_unique_order_without_delimiters(self):
        result = combine_neural_tones(
            analyze("ຂາຢາ"),
            "kʰaː˩˧jaː˧˥",
            model_id="byumatrixlab/lao-ipa-tonal",
            model_revision="a" * 40,
        )
        self.assertEqual(result.tone_alignment_status, "ORDER_ALIGNED")
        self.assertEqual(result.aligned_syllables, 2)
        self.assertEqual(
            [(item.syllable_index, item.contour) for item in result.tone_predictions],
            [(0, "˩˧"), (1, "˧˥")],
        )

    def test_syllable_count_mismatch_withholds_association_but_preserves_raw_tonal_ipa(self):
        raw = "kʰaː˧˥"
        result = combine_neural_tones(
            analyze("ຂາຢາ"), raw,
            model_id="byumatrixlab/lao-ipa-tonal",
            model_revision="a" * 40,
        )
        self.assertEqual(result.tone_alignment_status, "NOT_ALIGNED")
        self.assertEqual(result.tone_predictions, ())
        self.assertEqual(result.tonal_ipa, raw)
        self.assertTrue(any("SEQUENCE-NOT-UNIQUELY-ALIGNED" in warning for warning in result.warnings))

    def test_unsupported_neural_ipa_withholds_association_and_preserves_raw(self):
        raw = "ɕaː˧˥"
        result = combine_neural_tones(
            analyze("ຂາ"), raw,
            model_id="byumatrixlab/lao-ipa-tonal",
            model_revision="a" * 40,
        )
        self.assertEqual(result.tone_alignment_status, "NOT_ALIGNED")
        self.assertEqual(result.tone_predictions, ())
        self.assertEqual(result.tonal_ipa, raw)
        self.assertTrue(any("NEURAL-IPA-UNSUPPORTED" in warning for warning in result.warnings))

    def test_unknown_contour_is_not_promoted(self):
        result = combine_neural_tones(
            analyze("ຂາ"), "kʰaː˩˥",
            model_id="byumatrixlab/lao-ipa-tonal",
            model_revision="a" * 40,
        )
        self.assertEqual(result.tone_predictions, ())
        self.assertEqual(result.skipped_tone_units, 1)



    def test_cli_exposes_dual_lane_json_contract(self):
        result = combine_neural_tones(
            analyze("ຂາ"), "kʰaː˧˥",
            model_id="byumatrixlab/lao-ipa-tonal",
            model_revision="a" * 40,
        )
        output = StringIO()
        with patch(
            "sys.argv",
            ["lao-ua", "ຂາ", "--engine", "hybrid-v2", "--json"],
        ), patch(
            "lao_ukrainian.hybrid_v2.run_hybrid_v2",
            return_value=result,
        ), redirect_stdout(output):
            cli_main()
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["tonal_ipa"], "kʰaː˧˥")
        self.assertEqual(payload["ukrainian"], result.ukrainian)
        self.assertEqual(payload["tone_predictions"][0]["certainty"], "UNCERTAIN")

    def test_neural_limit_or_runtime_failure_returns_visible_deterministic_fallback(self):
        baseline = analyze("ຂາ")
        with patch(
            "lao_ukrainian.hybrid_v2.MekongPhonEngine.transcribe",
            side_effect=ValueError("Input exceeds the model's 128-token limit"),
        ):
            result = run_hybrid_v2("ຂາ")
        self.assertEqual(result.tone_alignment_status, "NEURAL_UNAVAILABLE")
        self.assertEqual(result.neural_raw_ipa, "")
        self.assertEqual(result.tone_predictions, ())
        self.assertEqual(result.ukrainian, "".join(
            item.practical_ukrainian or "?" for item in baseline.syllables
        ))
        self.assertTrue(any("128-token limit" in warning for warning in result.warnings))

    def test_input_analysis_is_not_mutated(self):
        baseline = analyze("ຂາ")
        before = baseline.syllables[0].phonetic_result
        combine_neural_tones(
            baseline, "kʰaː˧˥",
            model_id="byumatrixlab/lao-ipa-tonal",
            model_revision="a" * 40,
        )
        self.assertEqual(baseline.syllables[0].phonetic_result, before)


if __name__ == "__main__":
    unittest.main()
