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
