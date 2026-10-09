import unittest
from lao_ukrainian import practical_from_ipa

class TestTarget(unittest.TestCase):
    def test_aspiration(self): self.assertEqual(practical_from_ipa("kʰaː"),"ка")
    def test_h(self): self.assertEqual(practical_from_ipa("haː"),"га")
    def test_velar_nasal(self): self.assertEqual(practical_from_ipa("ŋaː"),"нга")
