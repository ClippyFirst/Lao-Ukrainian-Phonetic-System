import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "lao"


def rows(name):
    with (DATA / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class ToneRuleContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = rows("tone_rules.csv")
        cls.claims = {row["claim_id"]: row for row in rows("../evidence/claims.csv")}
        cls.sources = {row["source_id"] for row in rows("../evidence/sources.csv")}

    def test_rule_ids_and_condition_values_are_valid(self):
        ids = [row["rule_id"] for row in self.rules]
        self.assertEqual(len(ids), len(set(ids)), "tone rule IDs must be unique")
        for row in self.rules:
            with self.subTest(rule_id=row["rule_id"]):
                self.assertIn(row["class"], {"high", "middle", "low"})
                self.assertIn(row["syllable_type"], {"live", "dead", "*"})
                self.assertIn(row["length"], {"short", "long", "*"})
                self.assertIn(row["tone_mark"], {"none", "mai_ek", "mai_tho", "mai_ti", "mai_catawa"})
                self.assertIn(row["status"], {"well-supported", "analysis-dependent", "proposed", "not-established"})
                self.assertTrue(row["profile"].strip())
                # The resolver supports exact, class+syllable-type wildcard-length,
                # and class-wide wildcard rules, but not wildcard syllable type
                # with a specific length.
                self.assertFalse(row["syllable_type"] == "*" and row["length"] != "*")

    def test_every_tone_rule_resolves_to_a_claim_and_registered_sources(self):
        for row in self.rules:
            with self.subTest(rule_id=row["rule_id"]):
                self.assertIn(row["evidence_id"], self.claims)
                source_ids = {
                    value for value in self.claims[row["evidence_id"]]["evidence_ids"].split(";")
                    if value
                }
                self.assertTrue(source_ids, row["evidence_id"])
                self.assertLessEqual(source_ids, self.sources)

    def test_declared_matrix_has_no_ambiguous_winner(self):
        marks = {"none", "mai_ek", "mai_tho", "mai_ti", "mai_catawa"}
        for cls in ("high", "middle", "low"):
            for syllable_type in ("live", "dead"):
                for length in ("short", "long"):
                    for mark in marks:
                        with self.subTest(cls=cls, syllable_type=syllable_type, length=length, mark=mark):
                            candidates = [
                                row for row in self.rules
                                if row["class"] == cls
                                and row["tone_mark"] == mark
                                and row["syllable_type"] in {syllable_type, "*"}
                                and row["length"] in {length, "*"}
                            ]
                            if not candidates:
                                continue
                            priority = max(
                                (row["syllable_type"] != "*") * 2 + (row["length"] != "*")
                                for row in candidates
                            )
                            winners = [
                                row for row in candidates
                                if (row["syllable_type"] != "*") * 2 + (row["length"] != "*") == priority
                            ]
                            self.assertEqual(
                                len(winners), 1,
                                "each supported combination must have one most-specific rule",
                            )


if __name__ == "__main__":
    unittest.main()
