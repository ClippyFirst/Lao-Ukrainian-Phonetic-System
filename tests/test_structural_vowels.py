import unittest
from lao_ukrainian import analyze

class TestStructuralVowels(unittest.TestCase):
    def test_preposed_e(self):
        self.assertEqual(analyze("ເກ").syllables[0].phonemic_ipa,"ke")
    def test_preposed_ai(self):
        self.assertEqual(analyze("ໄກ່").syllables[0].phonemic_ipa,"kai")
    def test_postposed_nasal_coda(self):
        self.assertEqual(analyze("ການ").syllables[0].phonemic_ipa,"kaːn")
