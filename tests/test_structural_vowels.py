import json
import unittest
from pathlib import Path
from lao_ukrainian import analyze
from lao_ukrainian.data import load_registry
from lao_ukrainian.parser import STRUCTURES, parse_syllable

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


class TestShortVowelCodaConstraints(unittest.TestCase):
    def test_short_a_without_coda_is_evidence_limited(self):
        parsed = parse_syllable("ກັ")
        self.assertIn("SHORT_VOWEL_REQUIRES_CODA:A2", parsed["warnings"])
        self.assertEqual(analyze("ກັ").status, "PARTIAL")

    def test_short_open_o_variant_without_coda_is_evidence_limited(self):
        parsed = parse_syllable("ກັອ")
        self.assertIn("SHORT_VOWEL_REQUIRES_CODA:AWW_SHORT_ALT", parsed["warnings"])

    def test_short_o_variant_with_coda_remains_supported(self):
        result = analyze("ກັອບ")
        self.assertEqual(result.syllables[0].phonemic_ipa, "kɔp")


class TestCodaPositionValidation(unittest.TestCase):
    def test_legal_coda_must_be_the_last_grapheme(self):
        parsed = parse_syllable("ກາງເ")
        self.assertIsNone(parsed["coda"])
        self.assertIn("UNCONSUMED_AFTER_VOWEL:ງເ", parsed["warnings"])
        self.assertEqual(analyze("ກາງເ").status, "PARTIAL")


class TestSharedCodaFixtures(unittest.TestCase):
    def test_shared_legal_coda_inventory(self):
        fixture_path = Path(__file__).parent / "fixtures" / "coda_cases.json"
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        for case in fixture["cases"]:
            with self.subTest(case=case["id"]):
                result = analyze(case["surface"])
                self.assertEqual(len(result.syllables), 1)
                self.assertEqual(result.syllables[0].phonemic_ipa, case["phonemic_ipa"])
                self.assertEqual(result.syllables[0].coda, case["coda"])

    def test_unregistered_final_is_not_a_coda(self):
        parsed = parse_syllable("ກາສ")
        self.assertIsNone(parsed["coda"])
        self.assertIn("UNCONSUMED_AFTER_VOWEL:ສ", parsed["warnings"])


class TestVowelPrecedenceNegativeControls(unittest.TestCase):
    """Near-neighbour controls for the highest-risk overlapping spellings.

    These are engineering controls for parser discrimination, not a Lao gold
    corpus; the fixture metadata carries the same limitation.
    """
    def test_near_neighbour_spellings_keep_distinct_vowel_categories(self):
        cases = [
            ("PRE-E-SHORT-VS-LONG", "ເກະ", "E", "ເກ", "EE"),
            ("PRE-AE-SHORT-VS-LONG", "ແກະ", "AE", "ແກ", "AEE"),
            ("PRE-O-SHORT-VS-LONG", "ໂກະ", "O", "ໂກ", "OO"),
            ("PRE-OE-SHORT-VS-LONG-E", "ເກິ", "OE", "ເກ", "EE"),
            ("PRE-OE-LONG-VS-LONG-E", "ເກີ", "OEE", "ເກ", "EE"),
            ("PRE-IA-SHORT-VS-LONG", "ເກັຽ", "IA", "ເກຽ", "IA_LONG"),
            ("PRE-UA-SHORT-VS-LONG", "ເກຶອ", "UA", "ເກືອ", "UA_LONG"),
            ("PRE-AW-VS-AW-LONG", "ເກາະ", "AW", "ເກົາ", "AW_LONG"),
            ("POST-UO-SHORT-VS-LONG", "ກົວະ", "UO", "ກົວ", "UO_LONG"),
            ("POST-O-SHORT-VS-LONG", "ກັອບ", "AWW_SHORT_ALT", "ກໍ", "AWW"),
            ("POST-UO-SHORT-ALT-VS-LONG", "ກັວບ", "UO_SHORT_ALT", "ກວງ", "UO_LONG_ALT"),
        ]
        for case_id, positive, positive_id, contrast, contrast_id in cases:
            with self.subTest(case=case_id, role="positive"):
                result = analyze(positive)
                self.assertEqual(len(result.syllables), 1)
                self.assertEqual(result.syllables[0].vowel, positive_id)
            with self.subTest(case=case_id, role="contrast"):
                result = analyze(contrast)
                self.assertEqual(len(result.syllables), 1)
                self.assertEqual(result.syllables[0].vowel, contrast_id)

    def test_invalid_extra_vowel_material_is_not_silently_consumed(self):
        for surface in ("ກາງເ", "ເກິະ", "ເກີະ"):
            with self.subTest(surface=surface):
                parsed = parse_syllable(surface)
                self.assertTrue(parsed["warnings"], surface)
                self.assertNotEqual(analyze(surface).status, "OK")
