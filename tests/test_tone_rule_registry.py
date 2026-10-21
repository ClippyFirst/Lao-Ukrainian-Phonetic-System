"""Structural checks for the canonical tone-rule registry.

These tests verify table integrity and conservative fallback behavior. They do
not independently validate the linguistic correctness of the Vientiane model.
"""
import unittest

from lao_ukrainian.data import load_registry
from lao_ukrainian.phonology import determine_tone


class TestToneRuleRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = load_registry()
        self.rules = self.registry["tone_rules"]

    def test_rule_ids_and_selector_keys_are_unique(self):
        ids = [row["rule_id"] for row in self.rules]
        keys = [
            (row["class"], row["syllable_type"], row["length"], row["tone_mark"])
            for row in self.rules
        ]
        self.assertEqual(len(ids), len(set(ids)), "duplicate tone rule ID")
        self.assertEqual(len(keys), len(set(keys)), "overlapping exact tone selectors")

    def test_rule_fields_use_declared_values(self):
        classes = {"high", "middle", "low"}
        syllable_types = {"live", "dead", "*"}
        lengths = {"short", "long", "*"}
        marks = {"none", "mai_ek", "mai_tho", "mai_ti", "mai_catawa"}
        for row in self.rules:
            with self.subTest(rule=row["rule_id"]):
                self.assertIn(row["class"], classes)
                self.assertIn(row["syllable_type"], syllable_types)
                self.assertIn(row["length"], lengths)
                self.assertIn(row["tone_mark"], marks)
                self.assertTrue(row["tone"])
                self.assertTrue(row["contour"])
                self.assertTrue(row["status"])

    def test_every_declared_rule_is_reachable_by_the_selector(self):
        """Synthetic inputs check selector reachability, not phonetic truth."""
        mark_graphemes = {
            "none": None,
            "mai_ek": "່",
            "mai_tho": "້",
            "mai_ti": "໊",
            "mai_catawa": "໋",
        }
        for row in self.rules:
            length = row["length"] if row["length"] != "*" else "long"
            syllable_type = row["syllable_type"]
            coda = "ກ" if syllable_type == "dead" and length == "long" else None
            if syllable_type == "dead" and length == "short":
                coda = None
            vowel = {"length": length, "ipa": "aː" if length == "long" else "a"}
            tone, status, matched_rules = determine_tone(
                "ກ",
                vowel,
                coda,
                mark_graphemes[row["tone_mark"]],
                onset_class=row["class"],
            )
            with self.subTest(rule=row["rule_id"]):
                self.assertIsNotNone(tone)
                self.assertEqual(status, row["status"])
                self.assertEqual(matched_rules, [row["rule_id"]])

    def test_unlisted_class_and_tone_mark_combination_stays_unresolved(self):
        vowel = {"length": "long", "ipa": "aː"}
        tone, status, rules = determine_tone(
            "ຄ", vowel, None, "໊", onset_class="low"
        )
        self.assertIsNone(tone)
        self.assertEqual(status, "ANALYSIS DEPENDENT")
        self.assertEqual(rules, ["TONE-NOT-ESTABLISHED-FOR-COMBINATION"])


if __name__ == "__main__":
    unittest.main()
