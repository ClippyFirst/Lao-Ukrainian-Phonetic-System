import unittest
from lao_ukrainian import practical_from_ipa

class TestTarget(unittest.TestCase):
    def test_aspiration_is_marked(self):
        self.assertEqual(practical_from_ipa("kʰaː"), "к'а")
        self.assertEqual(practical_from_ipa("tʰaː"), "т'а")
        self.assertEqual(practical_from_ipa("pʰaː"), "п'а")
    def test_h_g_and_x_are_distinguished(self):
        self.assertEqual(practical_from_ipa("haː"), "га")
        self.assertEqual(practical_from_ipa("ɡaː"), "ґа")
        self.assertEqual(practical_from_ipa("xaː"), "ха")
    def test_affricates_and_digraphs(self):
        self.assertEqual(practical_from_ipa("tɕɔː"), "чо")
        self.assertEqual(practical_from_ipa("t͡sa"), "ца")
        self.assertEqual(practical_from_ipa("d͡za"), "дза")
        self.assertEqual(practical_from_ipa("d͡ʒa"), "джа")
    def test_palatalization(self):
        self.assertEqual(practical_from_ipa("nʲa"), "ньа")
    def test_velar_nasal(self):
        self.assertEqual(practical_from_ipa("ŋaː"), "нга")
    def test_ukrainian_shcha_sequence_is_not_split_into_sh_and_ch(self):
        self.assertEqual(practical_from_ipa("ʃt͡ʃa"), "ща")
        self.assertEqual(practical_from_ipa("ʃa"), "ша")
        self.assertEqual(practical_from_ipa("t͡ʃa"), "ча")
    def test_sh_and_zh_are_not_confused_with_affricates(self):
        self.assertEqual(practical_from_ipa("ʃa"), "ша")
        self.assertEqual(practical_from_ipa("ʒa"), "жа")
        self.assertEqual(practical_from_ipa("ɦaː"), "га")

