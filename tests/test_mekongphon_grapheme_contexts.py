import json
import unittest
from scripts.analyze_mekongphon_grapheme_contexts import analyze_rows, align_tokens, grapheme_units, structural_components, tokenize_ipa
from lao_ukrainian.data import load_registry
from lao_ukrainian.parser import parse_syllable
from lao_ukrainian.phonology import phonologize
from lao_ukrainian.target import adapt_phonetic_result
from lao_ukrainian.phonetic_result import from_phonology

class GraphemeContextTests(unittest.TestCase):
    def test_ipa_inventory_keeps_affricates_and_long_vowels(self):
        self.assertEqual(tokenize_ipa("t͡ɕaː"), ["t͡ɕ", "aː"])
        mapping, edits, insertions = align_tokens(["t͡ɕ", "aː"], ["t͡ɕ", "ɔː"])
        self.assertEqual(mapping, {0:"t͡ɕ", 1:"ɔː"})
        self.assertEqual((edits, insertions), (1,0))

    def test_long_schwa_is_a_single_typed_ipa_vowel(self):
        result = from_phonology("əː")
        self.assertEqual([segment.ipa for segment in result.segments], ["əː"])
        self.assertEqual(result.segments[0].kind, "vowel")
        self.assertEqual(result.status, "SUPPORTED")

    def test_lao_labialized_onsets_are_supported_ipa_segments(self):
        for ipa in ("kʷʰ", "tʷʰ", "kʷ", "tɕʷ", "ʔʷ", "sʷ", "ŋʷ", "lʷ"):
            with self.subTest(ipa=ipa):
                result = from_phonology(ipa)
                self.assertEqual(result.status, "SUPPORTED")
                self.assertEqual([segment.ipa for segment in result.segments], [ipa])
                self.assertEqual(result.segments[0].kind, "consonant")
                self.assertIsNone(adapt_phonetic_result(result, load_registry()))

    def test_reduced_schwa_offglide_is_a_supported_vowel(self):
        result = from_phonology("ə̯")
        self.assertEqual(result.status, "SUPPORTED")
        self.assertEqual(result.segments[0].ipa, "ə̯")
        self.assertEqual(result.segments[0].kind, "vowel")

    def test_combining_vowel_sign_is_a_separate_source_grapheme_element(self):
        self.assertEqual(grapheme_units("ກັນ"), [("ກ",0,1),("ັ",1,2),("ນ",2,3)])

    def test_same_grapheme_is_resolved_by_syllable_position(self):
        registry = load_registry()
        onset = parse_syllable("ວາ", registry)
        coda = parse_syllable("ກາວ", registry)
        self.assertFalse(onset["warnings"])
        self.assertFalse(coda["warnings"])
        self.assertEqual(phonologize(onset, registry, ipa_profile="vientiane")[0], "ʋaː")
        self.assertEqual(phonologize(coda, registry)[0], "kaːw")

    def test_same_consonant_has_distinct_onset_and_coda_values(self):
        registry = load_registry()
        onset = parse_syllable("ດາ", registry)
        coda = parse_syllable("ກາດ", registry)
        self.assertEqual(phonologize(onset, registry)[0], "daː")
        self.assertEqual(phonologize(coda, registry)[0], "kaːt")

    def test_preposed_e_distinguishes_short_and_long_by_structure(self):
        registry = load_registry()
        short = parse_syllable("ເກະ", registry)
        long = parse_syllable("ເກ", registry)
        self.assertEqual(short["vowel"]["ipa"], "e")
        self.assertEqual(long["vowel"]["ipa"], "eː")
        self.assertEqual(phonologize(short, registry)[0], "ke")
        self.assertEqual(phonologize(long, registry)[0], "keː")

    def test_same_grapheme_gets_distinct_onset_and_coda_context_rules(self):
        rows = [
            {"orth": "ວາ", "pron_no_tones": "waː"},
            {"orth": "ກາວ", "pron_no_tones": "kaːw"},
            {"orth": "ວາ", "pron_no_tones": "waː"},
        ]
        result = analyze_rows(rows, load_registry())
        rules = result["candidate_contextual_rules"]
        onset = next(rule for rule in rules if rule["grapheme"] == "ວ" and rule["role"] == "onset_base")
        coda = next(rule for rule in rules if rule["grapheme"] == "ວ" and rule["role"] == "coda")
        self.assertEqual(onset["realizations"][0]["engine_ipa"], "ʋ")
        self.assertEqual(onset["realizations"][0]["reference_ipa"], "w")
        self.assertEqual(onset["observations"], 2)
        self.assertEqual(coda["realizations"][0]["engine_ipa"], "w")
        self.assertEqual(coda["realizations"][0]["reference_ipa"], "w")
        self.assertEqual(coda["observations"], 1)
        position_rules = result["grapheme_position_rules"]
        onset_position = next(rule for rule in position_rules if rule["grapheme"] == "ວ" and rule["role"] == "onset_base")
        coda_position = next(rule for rule in position_rules if rule["grapheme"] == "ວ" and rule["role"] == "coda")
        self.assertEqual(onset_position["realizations"][0]["engine_ipa"], "ʋ")
        self.assertEqual(coda_position["realizations"][0]["engine_ipa"], "w")
        serialized = json.dumps(result, ensure_ascii=False)
        self.assertNotIn('"orth":', serialized)
        self.assertNotIn('"ວາ"', serialized)

    def test_o_is_silent_vowel_carrier_or_part_of_o_vowel_by_structure(self):
        registry = load_registry()
        carrier = parse_syllable("ອາ", registry)
        vowel_sign = parse_syllable("ກອງ", registry)
        self.assertEqual(phonologize(carrier, registry)[0], "aː")
        self.assertEqual(phonologize(vowel_sign, registry)[0], "kɔːŋ")

    def test_preposed_vowel_context_keeps_short_and_long_e_distinct(self):
        rows = [
            {"orth": "ເກະ", "pron_no_tones": "ke"},
            {"orth": "ເກ", "pron_no_tones": "keː"},
        ]
        result = analyze_rows(rows, load_registry())
        rules = [rule for rule in result["candidate_contextual_rules"]
                 if rule["grapheme"] == "ເ" and rule["role"] == "preposed_vowel_sign"]
        by_vowel = {rule["vowel_id"]: rule["realizations"][0] for rule in rules}
        self.assertEqual(by_vowel["E"]["engine_ipa"], "e")
        self.assertEqual(by_vowel["E"]["reference_ipa"], "e")
        self.assertEqual(by_vowel["EE"]["engine_ipa"], "eː")
        self.assertEqual(by_vowel["EE"]["reference_ipa"], "eː")

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
        registry=load_registry(); surface="ຂວັນ"; parsed=parse_syllable(surface,registry)
        self.assertFalse(parsed["warnings"])
        structure=structural_components(surface,parsed,registry)
        self.assertTrue(structure["cluster"])
        self.assertEqual(structure["onset_ipa"],"kʷʰ")

if __name__=="__main__": unittest.main()
