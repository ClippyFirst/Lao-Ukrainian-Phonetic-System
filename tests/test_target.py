import unittest

from lao_ukrainian import (
    PhoneticResult,
    adapt_phonetic_result,
    phonetic_result_from_ipa,
    practical_from_ipa,
)


def adapt(ipa: str) -> str | None:
    return practical_from_ipa(phonetic_result_from_ipa(ipa))


class TestTarget(unittest.TestCase):
    def test_aspiration_is_marked(self):
        self.assertEqual(adapt("kʰaː"), "к'а")
        self.assertEqual(adapt("tʰaː"), "т'а")
        self.assertEqual(adapt("pʰaː"), "п'а")

    def test_h_g_and_x_are_distinguished(self):
        self.assertEqual(adapt("haː"), "га")
        self.assertEqual(adapt("ɡaː"), "ґа")
        self.assertEqual(adapt("xaː"), "ха")

    def test_affricates_and_digraphs(self):
        self.assertEqual(adapt("tɕɔː"), "чо")
        self.assertEqual(adapt("t͡sa"), "ца")
        self.assertEqual(adapt("d͡za"), "дза")
        self.assertEqual(adapt("d͡ʒa"), "джа")

    def test_palatalization(self):
        self.assertEqual(adapt("nʲa"), "ньа")

    def test_velar_nasal(self):
        self.assertEqual(adapt("ŋaː"), "нга")

    def test_ukrainian_shcha_sequence_is_not_split_into_sh_and_ch(self):
        self.assertEqual(adapt("ʃt͡ʃa"), "ща")
        self.assertEqual(adapt("ʃa"), "ша")
        self.assertEqual(adapt("t͡ʃa"), "ча")

    def test_sh_and_zh_are_not_confused_with_affricates(self):
        self.assertEqual(adapt("ʃa"), "ша")
        self.assertEqual(adapt("ʒa"), "жа")
        self.assertEqual(adapt("ɦaː"), "га")

    def test_adapter_requires_a_typed_result(self):
        with self.assertRaises(TypeError):
            practical_from_ipa("kʰaː")

    def test_uncertain_result_is_withheld(self):
        result = phonetic_result_from_ipa("la", status="UNCERTAIN",
                                          uncertainty=("ONSET-ANALYSIS-DEPENDENT",))
        self.assertIsNone(adapt_phonetic_result(result))

    def test_typed_result_preserves_metadata_and_segment_boundaries(self):
        result = phonetic_result_from_ipa(
            "kʰaː", vowel_length="long", tone="low-rising",
            tone_contour="˩˥", provenance=("TONE-01",),
        )
        self.assertIsInstance(result, PhoneticResult)
        self.assertEqual(result.phonemic_ipa, "kʰaː")
        self.assertEqual([segment.ipa for segment in result.segments], ["kʰ", "aː"])
        self.assertEqual(result.syllable_boundaries, (0, 2))
        self.assertEqual(result.vowel_length, "long")
        self.assertEqual(result.tone_category, "low-rising")
        self.assertEqual(result.tone_contour_ipa, "˩˥")
        self.assertEqual(result.provenance, ("TONE-01",))
        self.assertEqual(adapt_phonetic_result(result), "к'а")

    def test_unsupported_ipa_fails_closed(self):
        result = phonetic_result_from_ipa("kʰaː☃")
        self.assertEqual(result.status, "UNSUPPORTED")
        self.assertIsNone(adapt_phonetic_result(result))


if __name__ == "__main__":
    unittest.main()
