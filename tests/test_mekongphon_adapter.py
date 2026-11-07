import unittest

from lao_ukrainian.mekongphon import build_result
from lao_ukrainian.phonetic_result import from_external_ipa


class MekongPhonAdapterTests(unittest.TestCase):
    def test_external_ipa_preserves_raw_output_and_terminal_tone(self):
        result = from_external_ipa(
            "kʰaː˩˥",
            provenance=("MEKONGPHON", "byumatrixlab/lao-ipa-tonal"),
        )
        self.assertEqual(result.external_ipa, "kʰaː˩˥")
        self.assertEqual(result.phonemic_ipa, "kʰaː")
        self.assertEqual(result.tone_contour_ipa, "˩˥")
        self.assertEqual([part.ipa for part in result.segments], ["kʰ", "aː"])
        self.assertEqual(result.status, "SUPPORTED")

    def test_unknown_ipa_symbol_fails_closed(self):
        result = from_external_ipa("ɕa")
        self.assertEqual(result.status, "UNSUPPORTED")
        self.assertIn("UNSUPPORTED-EXTERNAL-IPA-SYMBOLS", result.uncertainty)

    def test_internal_tone_mark_is_not_silently_discarded(self):
        result = from_external_ipa("kʰ˩aː")
        self.assertEqual(result.status, "UNSUPPORTED")

    def test_model_revision_is_recorded_and_mutability_warned(self):
        result = build_result(
            "ຂາ", "kʰaː",
            model_id="byumatrixlab/lao-ipa-nontonal",
            model_revision="main",
            tonal=False,
        )
        self.assertEqual(result.model_revision, "main")
        self.assertIn("MODEL-REVISION-NOT-IMMUTABLE", result.warnings)

    def test_invalid_ipa_never_produces_ukrainian_output(self):
        result = build_result(
            "ຂາ", "[not IPA]",
            model_id="byumatrixlab/lao-ipa-tonal",
            model_revision="a" * 40,
            tonal=True,
        )
        self.assertIsNone(result.ukrainian)
        self.assertEqual(result.status, "IPA_UNSUPPORTED")


if __name__ == "__main__":
    unittest.main()
