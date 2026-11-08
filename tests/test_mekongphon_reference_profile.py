"""Regression tests for the explicit MekongPhon-compatible deterministic IPA profile."""

import unittest

from lao_ukrainian import analyze
from lao_ukrainian.mekongphon_reference_profile import (
    DEFAULT_PROFILE,
    PROFILE_NAME,
    SUPPORTED_IPA_PROFILES,
    VOWEL_IPA_OVERRIDES,
    apply_ipa_profile,
)


class MekongPhonReferenceProfileTests(unittest.TestCase):
    def test_default_profile_is_unchanged(self):
        default = analyze("ດວງ")
        explicit = analyze("ດວງ", ipa_profile=DEFAULT_PROFILE)
        self.assertEqual(default.syllables[0].phonemic_ipa, "duːəŋ")
        self.assertEqual(
            explicit.syllables[0].phonemic_ipa,
            default.syllables[0].phonemic_ipa,
        )
        self.assertEqual(
            explicit.syllables[0].practical_ukrainian,
            default.syllables[0].practical_ukrainian,
        )

    def test_reference_profile_changes_only_the_requested_ipa_convention(self):
        default = analyze("ດວງ").syllables[0]
        compatible = analyze("ດວງ", ipa_profile=PROFILE_NAME).syllables[0]
        self.assertEqual(compatible.phonemic_ipa, "duaːŋ")
        self.assertEqual(compatible.phonetic_result.status, "SUPPORTED")
        self.assertEqual(compatible.phonetic_result.phonemic_ipa, compatible.phonemic_ipa)
        self.assertEqual(compatible.practical_ukrainian, "дуанг")
        self.assertEqual(default.tone, compatible.tone)
        self.assertEqual(default.tone_contour, compatible.tone_contour)
        self.assertIn("IPA-PROFILE-MEKONGPHON-VOWEL:UO_LONG_ALT", compatible.rules)

    def test_reference_profile_uses_contextual_onset_correspondences(self):
        baseline = analyze("ວັນ").syllables[0]
        compatible = analyze("ວັນ", ipa_profile=PROFILE_NAME).syllables[0]
        self.assertEqual(baseline.phonemic_ipa, "ʋan")
        self.assertEqual(compatible.phonemic_ipa, "wan")
        self.assertEqual(compatible.phonetic_result.status, "SUPPORTED")
        self.assertEqual(baseline.tone, compatible.tone)
        self.assertIn("IPA-PROFILE-MEKONGPHON-ONSET:ວ", compatible.rules)

    def test_provisional_r_onset_remains_uncertain_in_reference_profile(self):
        baseline = analyze("ຣະ").syllables[0]
        compatible = analyze("ຣະ", ipa_profile=PROFILE_NAME).syllables[0]
        self.assertEqual(baseline.phonemic_ipa, "la")
        self.assertEqual(compatible.phonemic_ipa, "ra")
        self.assertEqual(compatible.phonetic_result.status, "UNCERTAIN")
        self.assertIsNone(compatible.practical_ukrainian)

    def test_unknown_profile_is_rejected(self):
        with self.assertRaises(ValueError):
            analyze("ຂາ", ipa_profile="guess")

    def test_profile_function_preserves_unmapped_units(self):
        parsed = {"onset": "ກ", "vowel": {"id": "AA"}}
        result = apply_ipa_profile(parsed, "k", "aː", "ŋ", PROFILE_NAME)
        self.assertEqual(result, ("k", "aː", "ŋ", []))

    def test_every_transferred_vowel_rule_is_explicit_and_deterministic(self):
        for vowel_id, expected in VOWEL_IPA_OVERRIDES.items():
            with self.subTest(vowel_id=vowel_id):
                parsed = {"onset": "ກ", "vowel": {"id": vowel_id}}
                _, actual, _, rules = apply_ipa_profile(
                    parsed, "k", "old-ipa", "", PROFILE_NAME
                )
                self.assertEqual(actual, expected)
                self.assertEqual(rules, [f"IPA-PROFILE-MEKONGPHON-VOWEL:{vowel_id}"])

    def test_supported_profile_registry_is_explicit(self):
        self.assertEqual(SUPPORTED_IPA_PROFILES, ("vientiane", "mekongphon-reference"))


if __name__ == "__main__":
    unittest.main()
