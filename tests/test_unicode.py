import unittest
from lao_ukrainian import normalize_lao, validate_unicode

class TestUnicode(unittest.TestCase):
    def test_nfc(self): self.assertEqual(normalize_lao("ກາ"),"ກາ")
    def test_reject_mixed_cyrillic(self): self.assertTrue(validate_unicode("ກа"))
    def test_accept_lao_tone_mark(self): self.assertEqual(validate_unicode("ກ່າ"),[])
    def test_accept_crlf_whitespace(self): self.assertEqual(validate_unicode("ກ\r\nຂ"),[])
    def test_reject_non_whitespace_control(self): self.assertTrue(any("control character U+0001" in item for item in validate_unicode("ກ\x01ຂ")))
    def test_reject_zero_width_space(self): self.assertTrue(any("U+200B" in item for item in validate_unicode("ກ\u200bຂ")))
