import json
import unittest
from pathlib import Path
from lao_ukrainian import analyze
from lao_ukrainian.data import load_registry
from lao_ukrainian.parser import STRUCTURES

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


class TestSharedVowelPrecedenceFixtures(unittest.TestCase):
    def test_shared_fixture_ipa(self):
        fixture_path = Path(__file__).parent / "fixtures" / "vowel_precedence_cases.json"
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        self.assertEqual(fixture["schema_version"], 1)
        for case in fixture["cases"]:
            with self.subTest(case=case["id"]):
                result = analyze(case["surface"])
                self.assertEqual(len(result.syllables), 1, "fixture must remain one syllable")
                self.assertEqual(result.syllables[0].surface, case["surface"])
                self.assertEqual(result.syllables[0].phonemic_ipa, case["phonemic_ipa"])


class TestVowelRegistryCoverage(unittest.TestCase):
    def test_every_registry_vowel_has_a_python_structure(self):
        registry_ids = {item["id"] for item in load_registry()["vowels"]}
        parser_ids = {vowel_id for _, _, _, vowel_id in STRUCTURES}
        self.assertEqual(registry_ids - parser_ids, set(),
                         "Vowel registry IDs without parser structures")
