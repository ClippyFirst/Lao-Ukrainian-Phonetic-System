import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from types import SimpleNamespace
from unittest.mock import patch

from lao_ukrainian.cli import main


class MekongPhonCliTests(unittest.TestCase):
    def test_default_cli_runs_tonal_ipa_stage_only(self):
        result = SimpleNamespace(
            input="ຂາ",
            model_id="byumatrixlab/lao-ipa-tonal",
            model_revision="e02608cfcb18abfe6b1916f5f4774bfac9ac788d",
            raw_ipa="kʰaː˩˥",
            status="OK",
            warnings=(),
            to_dict=lambda: {"raw_ipa": "kʰaː˩˥"},
        )
        output = StringIO()
        with patch.object(sys, "argv", ["lao-ua", "ຂາ"]), \
             patch("lao_ukrainian.mekongphon.transcribe_ipa", return_value=result) as ipa, \
             patch("lao_ukrainian.mekongphon.transcribe_lao") as target, \
             redirect_stdout(output):
            main()

        ipa.assert_called_once_with(
            "ຂາ", tonal=True, revision=None, device="auto", num_beams=5
        )
        target.assert_not_called()
        self.assertIn("IPA: kʰaː˩˥", output.getvalue())
        self.assertNotIn("Ukrainian:", output.getvalue())

    def test_missing_neural_dependencies_never_fall_back_to_rules(self):
        output = StringIO()
        with patch.object(sys, "argv", ["lao-ua", "ຂາ"]), \
             patch("lao_ukrainian.mekongphon.transcribe_ipa",
                   side_effect=RuntimeError("Install optional neural dependencies")) as ipa, \
             patch("lao_ukrainian.cli.analyze",
                   side_effect=AssertionError("silent fallback is forbidden")), \
             redirect_stdout(output):
            with self.assertRaisesRegex(RuntimeError, "optional neural dependencies"):
                main()

        ipa.assert_called_once()

    def test_ukrainian_adaptation_is_explicit_second_stage(self):
        result = SimpleNamespace(
            input="ຂາ",
            model_id="byumatrixlab/lao-ipa-tonal",
            model_revision="e02608cfcb18abfe6b1916f5f4774bfac9ac788d",
            raw_ipa="kʰaː˩˥",
            ukrainian="к'а",
            status="OK",
            warnings=(),
            to_dict=lambda: {"raw_ipa": "kʰaː˩˥", "ukrainian": "к'а"},
        )
        output = StringIO()
        with patch.object(sys, "argv", ["lao-ua", "ຂາ", "--to-ukrainian"]), \
             patch("lao_ukrainian.mekongphon.transcribe_ipa") as ipa, \
             patch("lao_ukrainian.mekongphon.transcribe_lao", return_value=result) as target, \
             redirect_stdout(output):
            main()

        ipa.assert_not_called()
        target.assert_called_once_with(
            "ຂາ", tonal=True, revision=None, device="auto", num_beams=5
        )
        self.assertIn("Ukrainian: к'а [OK]", output.getvalue())


if __name__ == "__main__":
    unittest.main()
