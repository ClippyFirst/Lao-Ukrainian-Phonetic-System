import unittest
from lao_ukrainian import normalize_lao, validate_unicode

class TestUnicode(unittest.TestCase):
    def test_nfc(self): self.assertEqual(normalize_lao("ກາ"),"ກາ")
    def test_reject_mixed_cyrillic(self): self.assertTrue(validate_unicode("ກа"))
    def test_accept_lao_tone_mark(self): self.assertEqual(validate_unicode("ກ່າ"),[])
