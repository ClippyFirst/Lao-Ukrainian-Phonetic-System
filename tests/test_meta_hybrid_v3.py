import unittest
from unittest.mock import patch

from lao_ukrainian.mekongphon import build_result
from lao_ukrainian.meta_hybrid_v3 import (
    compare_segmental_lanes,
    run_meta_hybrid_v3,
)
from lao_ukrainian.core import analyze


class MetaHybridV3Tests(unittest.TestCase):
    def test_exact_segmental_agreement_is_reported_without_changing_authority(self):
        analysis = analyze("ຂາ")
        result = compare_segmental_lanes(analysis, "kʰaː")
        self.assertEqual(result.status, "EXACT_AGREEMENT")
        self.assertTrue(result.exact_agreement)
        self.assertEqual(result.selected_source, "CLIPPYFIRST_HYBRID_DETERMINISTIC")

    def test_disagreement_is_exposed_not_voted_away(self):
        result = compare_segmental_lanes(analyze("ຂາ"), "kʰeː")
        self.assertEqual(result.status, "DISAGREEMENT")
        self.assertFalse(result.exact_agreement)
        self.assertEqual(result.selected_source, "CLIPPYFIRST_HYBRID_DETERMINISTIC")
        self.assertIn("ENGINE-DISAGREEMENT-IS-NOT-AN-ACCURACY-JUDGMENT", result.warnings)

    def test_provisional_deterministic_ipa_is_not_scored(self):
        result = compare_segmental_lanes(analyze("ກາລ"), "kaːl")
        self.assertEqual(result.status, "UNSCORABLE")
        self.assertIsNone(result.exact_agreement)

    def test_invalid_input_does_not_load_neural_models(self):
        with patch("lao_ukrainian.meta_hybrid_v3.MekongPhonEngine.transcribe") as transcribe:
            result = run_meta_hybrid_v3("ກ\u0085ຂ")
        transcribe.assert_not_called()
        self.assertIn("DETERMINISTIC-INPUT-INVALID", result.warnings)

    def test_runs_both_neural_lanes_and_keeps_ukrainian_deterministic(self):
        def fake_transcribe(engine, text):
            return build_result(
                text,
                "kʰaː˧˥" if engine.tonal else "kʰaː",
                model_id=engine.model_id,
                model_revision=engine.revision,
                tonal=engine.tonal,
                num_beams=engine.num_beams,
            )

        with patch(
            "lao_ukrainian.meta_hybrid_v3.MekongPhonEngine.transcribe",
            new=fake_transcribe,
        ):
            result = run_meta_hybrid_v3("ຂາ", device="cpu")

        self.assertEqual(result.segmental_comparison.status, "EXACT_AGREEMENT")
        self.assertIsNotNone(result.nontonal_result)
        self.assertIsNotNone(result.tonal_result)
        self.assertEqual(result.tone_alignment.tone_alignment_status, "ORDER_ALIGNED")
        self.assertEqual(result.ukrainian, analyze("ຂາ").syllables[0].practical_ukrainian)

    def test_one_neural_lane_failure_does_not_hide_the_other_or_rules_lane(self):
        def flaky_transcribe(engine, text):
            if not engine.tonal:
                raise RuntimeError("nontonal unavailable")
            return build_result(
                text, "kʰaː˧˥", model_id=engine.model_id,
                model_revision=engine.revision, tonal=True,
                num_beams=engine.num_beams,
            )

        with patch(
            "lao_ukrainian.meta_hybrid_v3.MekongPhonEngine.transcribe",
            new=flaky_transcribe,
        ):
            result = run_meta_hybrid_v3("ຂາ", device="cpu")

        self.assertIsNone(result.nontonal_result)
        self.assertIsNotNone(result.tonal_result)
        self.assertEqual(result.segmental_comparison.status, "UNAVAILABLE")
        self.assertEqual(result.tone_alignment.tone_alignment_status, "ORDER_ALIGNED")
        self.assertIn("NON-TONAL-ENGINE-FAILED", result.warnings)


if __name__ == "__main__":
    unittest.main()
