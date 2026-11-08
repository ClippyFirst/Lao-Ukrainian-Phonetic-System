"""Regression tests for the explicit MekongPhon-compatible deterministic IPA profile."""

import unittest
import json
import sys
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from lao_ukrainian import analyze as _analyze
from lao_ukrainian.core import analyze as analyze_default

# Existing comparison fixtures intentionally use the Vientiane baseline.
def analyze(text, *, ipa_profile="vientiane"):
    return _analyze(text, ipa_profile=ipa_profile)
from lao_ukrainian.cli import main as cli_main
from lao_ukrainian.hybrid_rules import RuleConflictError, select_rule
from lao_ukrainian.mekongphon_reference_profile import (
    DEFAULT_PROFILE,
    PROFILE_NAME,
    HYBRID_PROFILE,
    HYBRID_RULES,
    SUPPORTED_IPA_PROFILES,
    VOWEL_IPA_OVERRIDES,
    apply_ipa_profile,
)


class MekongPhonReferenceProfileTests(unittest.TestCase):
    def test_default_engine_profile_is_hybrid_and_vientiane_is_explicit(self):
        default = analyze_default("ດວງ")
        explicit = analyze("ດວງ", ipa_profile=DEFAULT_PROFILE)
        self.assertEqual(default.syllables[0].phonemic_ipa, "duaːŋ")
        self.assertIn("HYBRID-RULE:HYB-MPH-VOWEL-UO_LONG_ALT", default.syllables[0].rules)
        self.assertEqual(explicit.syllables[0].phonemic_ipa, "duːəŋ")
        self.assertNotEqual(
            explicit.syllables[0].phonemic_ipa,
            default.syllables[0].phonemic_ipa,
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

    def test_cli_defaults_to_hybrid_profile(self):
        output = StringIO()
        with patch("sys.argv", ["lao-ua", "ດວງ", "--json"]), redirect_stdout(output):
            cli_main()
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["syllables"][0]["phonemic_ipa"], "duaːŋ")
        self.assertIn("HYBRID-RULE:HYB-MPH-VOWEL-UO_LONG_ALT", payload["syllables"][0]["rules"])

    def test_cli_selects_reference_profile_without_neural_engine(self):
        output = StringIO()
        with patch(
            "sys.argv",
            ["lao-ua", "ດວງ", "--ipa-profile", "mekongphon-reference", "--json"],
        ), redirect_stdout(output):
            cli_main()
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["syllables"][0]["phonemic_ipa"], "duaːŋ")
        self.assertEqual(payload["syllables"][0]["practical_ukrainian"], "дуанг")

    def test_supported_profile_registry_is_explicit(self):
        self.assertEqual(SUPPORTED_IPA_PROFILES, ("vientiane", "mekongphon-reference", "hybrid-deterministic"))

    def test_hybrid_profile_composes_vientiane_baseline_with_evidence_rules(self):
        baseline = analyze("ດວງ").syllables[0]
        reference = analyze("ດວງ", ipa_profile=PROFILE_NAME).syllables[0]
        hybrid = analyze("ດວງ", ipa_profile=HYBRID_PROFILE).syllables[0]
        self.assertEqual(hybrid.phonemic_ipa, reference.phonemic_ipa)
        self.assertEqual(hybrid.practical_ukrainian, reference.practical_ukrainian)
        self.assertNotEqual(hybrid.phonemic_ipa, baseline.phonemic_ipa)
        self.assertIn("HYBRID-RULE:HYB-MPH-VOWEL-UO_LONG_ALT", hybrid.rules)
        self.assertEqual(hybrid.tone, baseline.tone)
        self.assertEqual(hybrid.tone_contour, baseline.tone_contour)
        self.assertEqual(hybrid.phonetic_result.phonemic_ipa, hybrid.phonemic_ipa)

    def test_hybrid_profile_keeps_unmatched_vientiane_units(self):
        baseline = analyze("ຂາ").syllables[0]
        hybrid = analyze("ຂາ", ipa_profile=HYBRID_PROFILE).syllables[0]
        self.assertEqual(hybrid.phonemic_ipa, baseline.phonemic_ipa)
        self.assertFalse(any(rule.startswith("HYBRID-RULE:") for rule in hybrid.rules))

    def test_rule_selector_prefers_more_specific_context_independent_of_order(self):
        rules = [
            {"rule_id": "generic", "target": "vowel", "conditions": {"vowel_id": "IA_LONG"}, "value": "x", "priority": 0},
            {"rule_id": "specific", "target": "vowel", "conditions": {"vowel_id": "IA_LONG", "onset_class": "high"}, "value": "y", "priority": 0},
        ]
        context = {"vowel_id": "IA_LONG", "onset_class": "high"}
        self.assertEqual(select_rule(rules, context, target="vowel").value, "y")
        self.assertEqual(select_rule(list(reversed(rules)), context, target="vowel").value, "y")

    def test_rule_selector_rejects_equal_rank_conflicts(self):
        rules = [
            {"rule_id": "left", "target": "onset", "conditions": {"onset": "ວ"}, "value": "ʋ", "priority": 1},
            {"rule_id": "right", "target": "onset", "conditions": {"onset": "ວ"}, "value": "w", "priority": 1},
        ]
        with self.assertRaises(RuleConflictError):
            select_rule(rules, {"onset": "ວ"}, target="onset")

    def test_hybrid_cli_selects_profile_without_neural_engine(self):
        output = StringIO()
        with patch("sys.argv", ["lao-ua", "ດວງ", "--ipa-profile", HYBRID_PROFILE, "--json"]), redirect_stdout(output):
            cli_main()
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["syllables"][0]["phonemic_ipa"], "duaːŋ")
        self.assertIn("HYBRID-RULE:HYB-MPH-VOWEL-UO_LONG_ALT", payload["syllables"][0]["rules"])


if __name__ == "__main__":
    unittest.main()
