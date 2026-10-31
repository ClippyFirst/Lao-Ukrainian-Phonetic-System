import unittest

from lao_ukrainian import analyze


class TestCore(unittest.TestCase):
    def test_long_open_high_class(self):
        s = analyze("ຂາ").syllables[0]
        self.assertEqual(s.phonemic_ipa, "kʰaː")
        self.assertEqual(s.practical_ukrainian, "к\u0027а")
        self.assertEqual(s.tone, "low-rising")

    def test_tone_contour_is_preserved_from_the_matched_rule(self):
        rising = analyze("ຂາ").syllables[0]
        mid = analyze("ກ່າ").syllables[0]
        self.assertEqual(rising.tone, "low-rising")
        self.assertEqual(rising.tone_contour, "˩˥")
        self.assertEqual(mid.tone, "high-mid")
        self.assertEqual(mid.tone_contour, "˧")

    def test_middle_class_inherent_tone(self):
        self.assertEqual(analyze("ກາ").syllables[0].tone, "low-rising")

    def test_low_class_inherent_tone(self):
        self.assertEqual(analyze("ຄາ").syllables[0].tone, "high-rising")

    def test_tone_mark_matrix(self):
        self.assertEqual(analyze("ກ່າ").syllables[0].tone, "high-mid")
        self.assertEqual(analyze("ກ້າ").syllables[0].tone, "high-falling")
        self.assertEqual(analyze("ຄ້າ").syllables[0].tone, "high-falling")

    def test_low_class_ng(self):
        s = analyze("ງາ").syllables[0]
        self.assertEqual(s.phonemic_ipa, "ŋaː")
        self.assertEqual(s.practical_ukrainian, "нга")
        self.assertEqual(s.tone, "high-rising")

    def test_palatal_affricate(self):
        s = analyze("ຈາ").syllables[0]
        self.assertEqual(s.phonemic_ipa, "tɕaː")
        self.assertEqual(s.practical_ukrainian, "ча")

    def test_checked_coda(self):
        s = analyze("ກັບ").syllables[0]
        self.assertEqual(s.phonemic_ipa, "kap")
        self.assertEqual(s.practical_ukrainian, "кап")
        self.assertEqual(s.syllable_type, "dead")
        self.assertEqual(s.tone, "high-rising")

    def test_closed_uo_spelling(self):
        s = analyze("ດວງ").syllables[0]
        self.assertEqual(s.phonemic_ipa, "duːəŋ")
        self.assertEqual(s.practical_ukrainian, "дуанг")

    def test_open_uo_spelling(self):
        s = analyze("ດວາງ").syllables[0]
        self.assertEqual(s.phonemic_ipa, "duːəŋ")
        self.assertEqual(s.practical_ukrainian, "дуанг")

    def test_medial_o_vowel(self):
        s = analyze("ຈອກ").syllables[0]
        self.assertEqual(s.phonemic_ipa, "tɕɔːk")
        self.assertEqual(s.practical_ukrainian, "чок")

    def test_ti_and_catawa_marks(self):
        self.assertEqual(analyze("ກ໊າ").syllables[0].tone, "high-falling")
        self.assertEqual(analyze("ກ໋າ").syllables[0].tone, "low-rising")

    def test_multiple_tone_marks_withhold_ipa_and_ukrainian_output(self):
        result = analyze("ກ່້າ")
        s = result.syllables[0]
        self.assertEqual(s.status, "EVIDENCE LIMITED")
        self.assertIsNone(s.phonemic_ipa)
        self.assertIsNone(s.practical_ukrainian)
        self.assertEqual(s.ukrainian_candidates, [])
        self.assertIsNone(s.tone)
        self.assertIn("PHON-IPA-WITHHELD-MULTIPLE-TONE-MARKS", s.rules)
        self.assertIn("MULTIPLE_TONE_MARKS", s.warnings)

    def test_silent_high_digraph(self):
        s = analyze("ຫນອງ").syllables[0]
        self.assertEqual(s.phonemic_ipa, "nɔːŋ")
        self.assertEqual(s.consonant_class, "high")
        self.assertEqual(s.tone, "low-rising")

    def test_ligature_high_digraph(self):
        s = analyze("ໜາ").syllables[0]
        self.assertEqual(s.phonemic_ipa, "naː")
        self.assertEqual(s.consonant_class, "high")
        self.assertEqual(s.tone, "low-rising")

    def test_r_is_analysis_dependent(self):
        s = analyze("ຣະ").syllables[0]
        self.assertEqual(s.phonemic_ipa, "la")
        self.assertEqual(s.status, "ANALYSIS DEPENDENT")

    def test_vowel_carrier(self):
        s = analyze("ອາ").syllables[0]
        self.assertEqual(s.phonemic_ipa, "aː")
        self.assertEqual(s.practical_ukrainian, "а")


    def test_unconsumed_material_before_preposed_vowel_withholds_output(self):
        s = analyze("xເເກ").syllables[0]
        self.assertEqual(s.status, "ANALYSIS DEPENDENT")
        self.assertIsNone(s.phonemic_ipa)
        self.assertIsNone(s.practical_ukrainian)
        self.assertTrue(any(w.startswith("UNCONSUMED_BEFORE_ONSET:") for w in s.warnings))

    def test_unconsumed_grapheme_withholds_whole_unit_ipa_and_target(self):
        s = analyze("ກາລ").syllables[0]
        self.assertEqual(s.status, "EVIDENCE LIMITED")
        self.assertIsNone(s.phonemic_ipa)
        self.assertIsNone(s.practical_ukrainian)
        self.assertEqual(s.ukrainian_candidates, [])
        self.assertIn("PHON-IPA-WITHHELD-UNCONSUMED-ORTHOGRAPHY", s.rules)
        self.assertTrue(any(w.startswith("UNCONSUMED_AFTER_VOWEL:") for w in s.warnings))

    def test_unconsumed_material_before_legal_final_withholds_full_output(self):
        s = analyze("ກາກງ").syllables[0]
        self.assertEqual(s.status, "EVIDENCE LIMITED")
        self.assertIsNone(s.phonemic_ipa)
        self.assertIsNone(s.practical_ukrainian)
        self.assertEqual(s.ukrainian_candidates, [])
        self.assertTrue(
            any(w.startswith("UNCONSUMED_AFTER_VOWEL:") for w in s.warnings)
        )
