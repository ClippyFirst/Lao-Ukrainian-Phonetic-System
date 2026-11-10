import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from types import SimpleNamespace
from unittest.mock import patch

from lao_ukrainian.cli import main
from lao_ukrainian.core import analyze
from lao_ukrainian.hybrid_v2 import combine_neural_tones


class ResearchCliFormattingTests(unittest.TestCase):
    def test_hybrid_v2_text_output_uses_a_real_line_break(self):
        result = combine_neural_tones(
            analyze("ຂາ"),
            "kʰaː˧˥",
            model_id="byumatrixlab/lao-ipa-tonal",
            model_revision="a" * 40,
        )
        output = StringIO()
        with patch.object(
            sys, "argv", ["lao-ua", "ຂາ", "--engine", "hybrid-v2"]
        ), patch(
            "lao_ukrainian.hybrid_v2.run_hybrid_v2", return_value=result
        ), redirect_stdout(output):
            main()

        rendered = output.getvalue()
        self.assertIn("Input: ຂາ\nEngine: hybrid-v2", rendered)
        self.assertNotIn(r"\nEngine:", rendered)

    def test_meta_hybrid_v3_text_output_uses_a_real_line_break(self):
        result = SimpleNamespace(
            analysis=SimpleNamespace(input="ຂາ"),
            ukrainian="к'а",
            segmental_comparison=SimpleNamespace(
                status="EXACT_AGREEMENT",
                deterministic_ipa="kʰaː",
                neural_ipa="kʰaː",
            ),
            tonal_result=None,
            tone_alignment=None,
            warnings=(),
        )
        output = StringIO()
        with patch.object(
            sys, "argv", ["lao-ua", "ຂາ", "--engine", "meta-hybrid-v3"]
        ), patch(
            "lao_ukrainian.meta_hybrid_v3.run_meta_hybrid_v3",
            return_value=result,
        ), redirect_stdout(output):
            main()

        rendered = output.getvalue()
        self.assertIn("Input: ຂາ\nEngine: meta-hybrid-v3", rendered)
        self.assertNotIn(r"\nEngine:", rendered)


if __name__ == "__main__":
    unittest.main()
