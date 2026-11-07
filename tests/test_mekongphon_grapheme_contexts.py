import unittest
from scripts.analyze_mekongphon_grapheme_contexts import align_tokens, grapheme_units, structural_components, tokenize_ipa
from lao_ukrainian.data import load_registry
from lao_ukrainian.parser import parse_syllable

class GraphemeContextTests(unittest.TestCase):
    def test_ipa_inventory_keeps_affricates_and_long_vowels(self):
        self.assertEqual(tokenize_ipa("t͡ɕaː"), ["t͡ɕ", "aː"])
        mapping, edits, insertions = align_tokens(["t͡ɕ", "aː"], ["t͡ɕ", "ɔː"])
        self.assertEqual(mapping, {0:"t͡ɕ", 1:"ɔː"})
        self.assertEqual((edits, insertions), (1,0))

    def test_combining_marks_remain_attached_to_base_grapheme(self):
        self.assertEqual(grapheme_units("ກັນ"), [("ກັ",0,2),("ນ",2,3)])

    def test_preposed_vowel_is_joint_structure(self):
        registry=load_registry(); surface="ເກ"; parsed=parse_syllable(surface,registry)
        self.assertFalse(parsed["warnings"])
        structure=structural_components(surface,parsed,registry)
        self.assertEqual(structure["components"][0]["ipa"],"k")
        self.assertEqual(structure["components"][1]["ipa"],"eː")
        self.assertEqual(structure["components"][1]["surface"],"ເ")

    def test_high_digraph_separates_silent_class_modifier(self):
        registry=load_registry(); surface="ຫມູ"; parsed=parse_syllable(surface,registry)
        self.assertFalse(parsed["warnings"])
        structure=structural_components(surface,parsed,registry)
        self.assertTrue(structure["high_digraph"])
        self.assertEqual(structure["onset"],"ມ")
        self.assertEqual(structure["onset_ipa"],"m")

    def test_labialized_cluster_is_joint_onset_unit(self):
        registry=load_registry(); surface="ກວາ"; parsed=parse_syllable(surface,registry)
        self.assertFalse(parsed["warnings"])
        structure=structural_components(surface,parsed,registry)
        self.assertTrue(structure["cluster"])
        self.assertEqual(structure["onset_ipa"],"kʷ")

if __name__=="__main__": unittest.main()
