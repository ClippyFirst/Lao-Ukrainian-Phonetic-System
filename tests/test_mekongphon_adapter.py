import unittest

from lao_ukrainian.mekongphon import MODEL_REVISIONS, MODEL_WEIGHT_SHA256, MekongPhonEngine, build_result
from lao_ukrainian.phonetic_result import from_external_ipa


class MekongPhonAdapterTests(unittest.TestCase):

    def test_default_engines_use_the_verified_immutable_model_revisions(self):
        tonal = MekongPhonEngine(tonal=True)
        nontonal = MekongPhonEngine(tonal=False)
        self.assertEqual(tonal.revision, MODEL_REVISIONS["tonal"])
        self.assertEqual(nontonal.revision, MODEL_REVISIONS["nontonal"])
        self.assertRegex(tonal.revision, r"^[0-9a-f]{40}$")
        self.assertRegex(nontonal.revision, r"^[0-9a-f]{40}$")
        self.assertIsNone(tonal._loaded)
        self.assertIsNone(nontonal._loaded)

    def test_pinned_model_weight_sha256_values_are_immutable(self):
        self.assertEqual(
            MODEL_WEIGHT_SHA256["tonal"],
            "5cf6110fdafd9626e96db128ec580b3da705904e1c0478b727c9dc6a14a7b119",
        )
        self.assertEqual(
            MODEL_WEIGHT_SHA256["nontonal"],
            "3f3c452e55646dc124c8dc1dab80754e68290782a9c6e5f40c463e49a05a485c",
        )
        for digest in MODEL_WEIGHT_SHA256.values():
            self.assertRegex(digest, r"^[0-9a-f]{64}$")

    def test_external_ipa_preserves_raw_output_and_terminal_tone(self):
        result = from_external_ipa(
            "kʰaː˩˥",
            provenance=("MEKONGPHON", "byumatrixlab/lao-ipa-tonal"),
        )
        self.assertEqual(result.external_ipa, "kʰaː˩˥")
        self.assertEqual(result.phonemic_ipa, "kʰaː")
        self.assertEqual(result.tone_contour_ipa, "˩˥")
        self.assertEqual([part.ipa for part in result.segments], ["kʰ", "aː", "˩", "˥"])
        self.assertEqual([part.kind for part in result.segments], ["consonant", "vowel", "tone", "tone"])
        self.assertEqual(result.status, "SUPPORTED")

    def test_unknown_ipa_symbol_fails_closed(self):
        result = from_external_ipa("ɕa")
        self.assertEqual(result.status, "UNSUPPORTED")
        self.assertIn("UNSUPPORTED-EXTERNAL-IPA-SYMBOLS", result.uncertainty)

    def test_internal_tone_mark_is_typed_and_preserved(self):
        result = from_external_ipa("kʰ˩aː˥")
        self.assertEqual(result.status, "SUPPORTED")
        self.assertEqual(result.phonemic_ipa, "kʰaː")
        self.assertEqual(result.tone_contour_ipa, "˩˥")
        self.assertEqual(
            [part.kind for part in result.segments],
            ["consonant", "tone", "vowel", "tone"],
        )

    def test_tonal_model_output_uses_existing_segmental_target_adapter(self):
        result = build_result(
            "ຂາ", "kʰ˩aː˥",
            model_id="byumatrixlab/lao-ipa-tonal",
            model_revision="a" * 40,
            tonal=True,
        )
        self.assertEqual(result.status, "OK")
        self.assertEqual(result.ukrainian, "к'а")
        self.assertEqual(result.phonetic_result.external_ipa, "kʰ˩aː˥")

    def test_model_revision_is_recorded_and_mutability_warned(self):
        result = build_result(
            "ຂາ", "kʰaː",
            model_id="byumatrixlab/lao-ipa-nontonal",
            model_revision="main",
            tonal=False,
        )
        self.assertEqual(result.model_revision, "main")
        self.assertIn("MODEL-REVISION-NOT-IMMUTABLE", result.warnings)

    def test_explicit_internal_syllable_boundary_enables_initial_yodation(self):
        result = build_result(
            "ຂາຢາ", "kʰaː˩.jaː˧",
            model_id="byumatrixlab/lao-ipa-tonal",
            model_revision="a" * 40,
            tonal=True,
        )
        self.assertEqual(result.phonetic_result.syllable_boundaries, (0, 3, 6))
        self.assertEqual(result.ukrainian, "к'ая")

    def test_initial_yodation_does_not_collapse_a_diphthong(self):
        result = build_result(
            "ຢຽ", "jiə",
            model_id="byumatrixlab/lao-ipa-nontonal",
            model_revision="b" * 40,
            tonal=False,
        )
        self.assertEqual(result.ukrainian, "йіа")

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
