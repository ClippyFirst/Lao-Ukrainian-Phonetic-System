import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch
from lao_ukrainian import analyze
from lao_ukrainian.cli import main


class GraphemePreviewTests(unittest.TestCase):
    def test_unconsumed_tail_gets_partial_preview_only(self):
        syllable = analyze("ກາລ").syllables[0]
        preview = syllable.grapheme_preview
        self.assertIsNone(syllable.phonemic_ipa)
        self.assertIsNone(syllable.practical_ukrainian)
        self.assertEqual(preview.ipa_preview, "kaː")
        self.assertEqual(preview.status, "PROVISIONAL")
        self.assertEqual(preview.unresolved_graphemes, ("ລ",))
        self.assertEqual(preview.phonetic_result.status, "PROVISIONAL")
        self.assertTrue(all(s.certainty == "PROVISIONAL" for s in preview.phonetic_result.segments))

    def test_multiple_tone_marks_show_segmental_preview_without_tone(self):
        syllable = analyze("ຂ່້າ").syllables[0]
        self.assertIsNone(syllable.phonemic_ipa)
        self.assertEqual(syllable.grapheme_preview.ipa_preview, "kʰaː")
        self.assertIn("TONE_NOT_INFERRED_BY_GRAPHEME_PREVIEW", syllable.grapheme_preview.warnings)
        self.assertIsNone(syllable.grapheme_preview.phonetic_result.tone_category)
        self.assertIsNone(syllable.practical_ukrainian)

    def test_partial_onset_is_visible_when_vowel_structure_is_unknown(self):
        preview = analyze("ຂເ").syllables[0].grapheme_preview
        self.assertEqual(preview.ipa_preview, "kʰ")
        self.assertEqual(preview.unresolved_graphemes, ("ເ",))
        self.assertEqual(preview.graphemes[0].role, "syllable-onset")

    def test_non_core_pali_grapheme_gets_no_invented_ipa(self):
        preview = analyze("ຆາ").syllables[0].grapheme_preview
        self.assertIsNone(preview.ipa_preview)
        self.assertEqual(preview.status, "UNRESOLVED")
        self.assertIn("ຆ", preview.unresolved_graphemes)

    def test_complete_syllable_does_not_receive_fallback_preview(self):
        self.assertIsNone(analyze("ຂາ").syllables[0].grapheme_preview)

    def test_text_cli_displays_provisional_preview_separately(self):
        output = StringIO()
        with patch("sys.argv", ["lao-ua", "ກາລ"]), redirect_stdout(output):
            main()
        rendered = output.getvalue()
        self.assertIn("IPA=None", rendered)
        self.assertIn("IPA preview=kaː [PROVISIONAL]", rendered)
        self.assertIn("unresolved=ລ", rendered)


if __name__ == "__main__":
    unittest.main()
