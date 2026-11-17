import csv
import unittest
from pathlib import Path

from lao_ukrainian.data import load_registry
from lao_ukrainian.parser import parse_syllable

ROOT = Path(__file__).resolve().parents[1]


class TestGraphemeInventory(unittest.TestCase):
    def setUp(self):
        with (ROOT / "data/lao/grapheme_inventory.csv").open(encoding="utf-8", newline="") as stream:
            self.rows = list(csv.DictReader(stream))
        self.by_grapheme = {row["grapheme"]: row for row in self.rows}

    def test_unicode_18_lao_block_assigned_codepoints_are_in_inventory(self):
        pairs = sorted((int(row["codepoint"][2:], 16), row) for row in self.rows)
        codepoints = [cp for cp, _ in pairs]
        self.assertEqual(len(codepoints), 83)
        self.assertEqual(len(codepoints), len(set(codepoints)))
        self.assertEqual(len({row["grapheme"] for row in self.rows}), len(self.rows))
        self.assertTrue(all(ord(row["grapheme"]) == cp for cp, row in pairs))
        self.assertEqual(codepoints, [3713,3714,3716,3718,3719,3720,3721,3722,3724,3725,3726,3727,3728,3729,3730,3731,3732,3733,3734,3735,3736,3737,3738,3739,3740,3741,3742,3743,3744,3745,3746,3747,3749,3751,3752,3753,3754,3755,3756,3757,3758,3759,3760,3761,3762,3763,3764,3765,3766,3767,3768,3769,3770,3771,3772,3773,3776,3777,3778,3779,3780,3782,3784,3785,3786,3787,3788,3789,3790,3792,3793,3794,3795,3796,3797,3798,3799,3800,3801,3804,3805,3806,3807])

    def test_inventory_distinguishes_core_extensions_and_nonphonological_items(self):
        self.assertEqual(self.by_grapheme["ກ"]["engine_status"], "CORE_POSITIONAL")
        self.assertEqual(self.by_grapheme["ຣ"]["engine_status"], "ANALYSIS_DEPENDENT")
        self.assertEqual(self.by_grapheme["ຆ"]["engine_status"], "NON_CORE_NO_MODERN_IPA")
        self.assertEqual(self.by_grapheme["ຨ"]["engine_status"], "NON_CORE_NO_MODERN_IPA")
        self.assertEqual(self.by_grapheme["ໞ"]["engine_status"], "OUT_OF_SCOPE_KHMU")
        self.assertEqual(self.by_grapheme["່"]["engine_status"], "TONE_ONLY")
        self.assertEqual(self.by_grapheme["໐"]["engine_status"], "NONPHONOLOGICAL")


    def test_ishida_nine_coda_spellings_match_the_source_aware_final_map(self):
        registry = load_registry()
        actual = {
            grapheme: row["ipa_final"]
            for grapheme, row in registry["consonants"].items()
            if row["ipa_final"]
        }
        self.assertEqual(actual, {
            "ບ": "p", "ດ": "t", "ກ": "k", "ມ": "m", "ນ": "n",
            "ຣ": "n", "ງ": "ŋ", "ວ": "w", "ຍ": "j",
        })
        # Ishida’s chart includes ຢ, but its explicit list and IPA table do not
        # support it as a coda. Keep the source-internal discrepancy fail-closed.
        self.assertEqual(registry["consonants"]["ຢ"]["ipa_final"], "")
        unresolved = parse_syllable("ກາຢ", registry)
        self.assertIsNone(unresolved["coda"])
        self.assertIn("UNCONSUMED_AFTER_VOWEL:ຢ", unresolved["warnings"])


if __name__ == "__main__":
    unittest.main()
