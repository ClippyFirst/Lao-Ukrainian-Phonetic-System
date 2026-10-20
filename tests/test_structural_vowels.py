import unittest
from lao_ukrainian import analyze

class TestStructuralVowels(unittest.TestCase):
    def test_preposed_e_long(self):
        self.assertEqual(analyze("ເກ").syllables[0].phonemic_ipa,"keː")

    def test_preposed_e_short(self):
        self.assertEqual(analyze("ເກະ").syllables[0].phonemic_ipa,"ke")

    def test_preposed_ai(self):
        self.assertEqual(analyze("ໄກ່").syllables[0].phonemic_ipa,"kai")

    def test_postposed_nasal_coda(self):
        self.assertEqual(analyze("ການ").syllables[0].phonemic_ipa,"kaːn")

    def test_long_open_o_carrier(self):
        self.assertEqual(analyze("ອໍ").syllables[0].phonemic_ipa,"ɔː")


    def test_preposed_oe_short_is_not_shadowed_by_long_e(self):
        self.assertEqual(analyze("ເກິ").syllables[0].vowel, "OE")
        self.assertEqual(analyze("ເກິ").syllables[0].phonemic_ipa, "kɤ")

    def test_preposed_oe_long_is_not_shadowed_by_long_e(self):
        self.assertEqual(analyze("ເກີ").syllables[0].vowel, "OEE")
        self.assertEqual(analyze("ເກີ").syllables[0].phonemic_ipa, "kɤː")

    def test_preposed_ia_long_is_not_shadowed_by_long_e(self):
        self.assertEqual(analyze("ເກຽ").syllables[0].vowel, "IA_LONG")
        self.assertEqual(analyze("ເກຽ").syllables[0].phonemic_ipa, "kiːə")
