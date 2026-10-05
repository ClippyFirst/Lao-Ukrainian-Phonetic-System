import unittest
from lao_ukrainian import analyze

class TestCore(unittest.TestCase):
    def test_long_open_high_class(self):
        s=analyze("ຂາ").syllables[0]
        self.assertEqual(s.phonemic_ipa,"kʰaː")
        self.assertEqual(s.practical_ukrainian,"ка")
        self.assertEqual(s.tone,"low-rising")

    def test_low_class_ng(self):
        s=analyze("ງາ").syllables[0]
        self.assertEqual(s.phonemic_ipa,"ŋaː")
        self.assertEqual(s.practical_ukrainian,"нга")
        self.assertEqual(s.tone,"high-rising")

    def test_palatal_affricate(self):
        s=analyze("ຈາ").syllables[0]
        self.assertEqual(s.phonemic_ipa,"tɕaː")
        self.assertEqual(s.practical_ukrainian,"ча")

    def test_checked_coda(self):
        s=analyze("ກັບ").syllables[0]
        self.assertEqual(s.phonemic_ipa,"kap")
        self.assertEqual(s.practical_ukrainian,"кап")
        self.assertEqual(s.syllable_type,"dead")

    def test_vowel_carrier(self):
        s=analyze("ອາ").syllables[0]
        self.assertEqual(s.phonemic_ipa,"aː")
        self.assertEqual(s.practical_ukrainian,"а")
