"""Conservative parser contracts; these tests are not a pronunciation gold set."""

import unittest

from lao_ukrainian.parser import parse_syllable


class ConservativeParseContracts(unittest.TestCase):
    def test_trailing_vowel_after_legal_final_is_not_silently_discarded(self):
        result = parse_syllable("ກາງະ")

        self.assertIsNone(result["coda"])
        self.assertTrue(
            any(
                warning.startswith("UNCONSUMED_AFTER_VOWEL:")
                for warning in result["warnings"]
            )
        )

    def test_legal_final_coda_is_recognized_at_the_end_of_the_syllable(self):
        result = parse_syllable("ການ")

        self.assertEqual(result["coda"], "ນ")
        self.assertFalse(
            any(
                warning.startswith("UNCONSUMED_AFTER_VOWEL:")
                for warning in result["warnings"]
            )
        )

    def test_material_before_final_legal_coda_is_not_silently_discarded(self):
        result = parse_syllable("ກາກງ")

        self.assertIsNone(result["coda"])
        self.assertTrue(
            any(
                warning.startswith("UNCONSUMED_AFTER_VOWEL:")
                for warning in result["warnings"]
            )
        )


if __name__ == "__main__":
    unittest.main()
