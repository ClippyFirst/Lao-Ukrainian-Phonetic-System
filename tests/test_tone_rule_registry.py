"""Structural checks for the canonical tone-rule registry.

These tests verify table integrity and conservative fallback behavior. They do
not independently validate the linguistic correctness of the Vientiane model.
"""
import unittest
import csv
from pathlib import Path

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

    def test_every_rule_has_source_backed_profile_provenance(self):
        root = Path(__file__).resolve().parents[1]
        with (root / "data" / "evidence" / "sources.csv").open(encoding="utf-8", newline="") as f:
            sources = {row["source_id"] for row in csv.DictReader(f)}
        with (root / "data" / "evidence" / "claims.csv").open(encoding="utf-8", newline="") as f:
            claims = {row["claim_id"]: row for row in csv.DictReader(f)}

        for row in self.rules:
            with self.subTest(rule=row["rule_id"]):
                self.assertEqual(row.get("profile"), "Vientiane")
                claim_id = row.get("evidence_id")
                self.assertIn(claim_id, claims)
                claim = claims[claim_id]
                self.assertEqual(claim["status"], "methodology")
                for source_id in claim["evidence_ids"].split(";"):
                    self.assertIn(source_id, sources)

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

    def test_tone_mark_rules_are_restricted_to_live_syllables(self):
        for row in self.rules:
            if row["tone_mark"] != "none":
                with self.subTest(rule=row["rule_id"]):
                    self.assertEqual(row["syllable_type"], "live")

    def test_rare_tone_marks_are_middle_class_only_and_source_linked(self):
        rare_rules = {
            row["tone_mark"]: row
            for row in self.rules
            if row["tone_mark"] in {"mai_ti", "mai_catawa"}
        }
        self.assertEqual(set(rare_rules), {"mai_ti", "mai_catawa"})
        self.assertEqual(rare_rules["mai_ti"]["class"], "middle")
        self.assertEqual(rare_rules["mai_ti"]["tone"], "high-falling")
        self.assertEqual(rare_rules["mai_catawa"]["class"], "middle")
        self.assertEqual(rare_rules["mai_catawa"]["tone"], "low-rising")
        for row in rare_rules.values():
            self.assertEqual(row["syllable_type"], "live")
            self.assertEqual(row["evidence_id"], "CLM-LAO-TONE-RARE-MARKS")

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

    def test_complete_class_type_length_mark_cross_product(self):
        """All 60 selector combinations resolve only when a registry rule matches."""
        mark_graphemes = {
            "none": None,
            "mai_ek": "່",
            "mai_tho": "້",
            "mai_ti": "໊",
            "mai_catawa": "໋",
        }
        rule_index = {
            (row["class"], row["syllable_type"], row["length"], row["tone_mark"]): row
            for row in self.rules
        }
        for onset_class in ("high", "middle", "low"):
            for syllable_type in ("live", "dead"):
                for length in ("short", "long"):
                    # Use a sonorant coda for live short syllables, a stop for
                    # dead long syllables, and no coda for the other cases.
                    coda = None
                    if syllable_type == "live" and length == "short":
                        coda = "ງ"
                    elif syllable_type == "dead" and length == "long":
                        coda = "ກ"
                    vowel = {"length": length, "ipa": "aː" if length == "long" else "a"}
                    for mark_name, mark_grapheme in mark_graphemes.items():
                        candidates = (
                            (onset_class, syllable_type, length, mark_name),
                            (onset_class, syllable_type, "*", mark_name),
                            (onset_class, "*", "*", mark_name),
                        )
                        expected = next(
                            (rule_index[key] for key in candidates if key in rule_index),
                            None,
                        )
                        tone, status, matched_rules = determine_tone(
                            "ກ", vowel, coda, mark_grapheme, onset_class=onset_class
                        )
                        case = (onset_class, syllable_type, length, mark_name)
                        with self.subTest(case=case):
                            if expected is None:
                                self.assertIsNone(tone)
                                self.assertEqual(status, "ANALYSIS DEPENDENT")
                                self.assertEqual(
                                    matched_rules,
                                    ["TONE-NOT-ESTABLISHED-FOR-COMBINATION"],
                                )
                            else:
                                self.assertEqual(tone, expected["tone"])
                                self.assertEqual(status, expected["status"])
                                self.assertEqual(matched_rules, [expected["rule_id"]])

    def test_tone_marks_do_not_resolve_dead_syllables(self):
        """Tone marks are used with open/live syllables, not dead syllables."""
        onsets = {"high": "ຂ", "middle": "ກ", "low": "ຄ"}
        marks = {"mai_ek": "່", "mai_tho": "້", "mai_ti": "໊", "mai_catawa": "໋"}
        dead_contexts = (
            ({"length": "short", "ipa": "a"}, None),
            ({"length": "long", "ipa": "aː"}, "ກ"),
        )

        for onset_class, onset in onsets.items():
            for mark_name, mark_grapheme in marks.items():
                for vowel, coda in dead_contexts:
                    tone, status, matched_rules = determine_tone(
                        onset, vowel, coda, mark_grapheme, onset_class=onset_class
                    )
                    with self.subTest(
                        onset_class=onset_class,
                        mark=mark_name,
                        length=vowel["length"],
                        coda=coda,
                    ):
                        self.assertIsNone(tone)
                        self.assertEqual(status, "ANALYSIS DEPENDENT")
                        self.assertEqual(
                            matched_rules,
                            ["TONE-NOT-ESTABLISHED-FOR-COMBINATION"],
                        )

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
