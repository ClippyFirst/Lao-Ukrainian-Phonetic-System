"""Tests for optional lexical hints; these are not word-boundary gold."""
import tempfile
import unittest
from pathlib import Path

from lao_ukrainian.lexical_hints import (
    find_orthographic_word_hints,
    load_orthographic_hint_entries,
)


class LexicalBoundaryHintTests(unittest.TestCase):
    def test_loader_skips_license_header_and_deduplicates_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "words.txt"
            path.write_text("# BSD notice\nສະບາຍ\nສະບາຍ\n\n", encoding="utf-8")
            self.assertEqual(load_orthographic_hint_entries(path), ("ສະບາຍ",))

    def test_returns_all_overlapping_matches_without_selecting_boundaries(self):
        syllables = ["ສະ", "ບາຍ", "ດີ"]
        hints = find_orthographic_word_hints(syllables, ["ສະບາຍ", "ບາຍດີ", "ສະບາຍດີ"])
        self.assertEqual(
            [(h["start_syllable"], h["end_syllable"], h["surface"]) for h in hints],
            [(0, 2, "ສະບາຍ"), (0, 3, "ສະບາຍດີ"), (1, 3, "ບາຍດີ")],
        )
        self.assertTrue(all(h["authority"] == "SOFT_HINT_ONLY" for h in hints))

    def test_single_syllable_entries_are_not_hints_by_default(self):
        self.assertEqual(find_orthographic_word_hints(["ກາ", "ດີ"], ["ກາ", "ດີ"]), [])

    def test_hints_do_not_change_syllable_sequence(self):
        syllables = ["ພາ", "ສາ", "ລາວ"]
        before = list(syllables)
        find_orthographic_word_hints(syllables, ["ພາສາ", "ລາວ"])
        self.assertEqual(syllables, before)

    def test_invalid_minimum_is_rejected(self):
        with self.assertRaises(ValueError):
            find_orthographic_word_hints(["ກາ"], ["ກາ"], min_syllables=0)


if __name__ == "__main__":
    unittest.main()
