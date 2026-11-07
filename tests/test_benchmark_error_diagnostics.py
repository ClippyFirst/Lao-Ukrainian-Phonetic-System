import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "benchmark_mekongphon_three_engines.py"
SPEC = importlib.util.spec_from_file_location("mekongphon_benchmark", SCRIPT)
BENCHMARK = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(BENCHMARK)


class TestBenchmarkErrorDiagnostics(unittest.TestCase):
    def test_alignment_profile_counts_substitutions_deletions_and_insertions(self):
        result = BENCHMARK.alignment_error_profile(
            ["kʰaː", "ŋ", "tɕ"],
            ["kʰəː", "", "tɕa"],
        )
        self.assertEqual(result["total_substitutions"], 1)
        self.assertEqual(result["total_deletions"], 1)
        self.assertEqual(result["total_insertions"], 1)
        self.assertEqual(result["top_substitutions"][0], {"pair": "a=>ə", "count": 1})
        self.assertEqual(result["top_deletions"][0], {"symbol": "ŋ", "count": 1})
        self.assertEqual(result["top_insertions"][0], {"symbol": "a", "count": 1})

    def test_alignment_profile_is_deterministic_on_ambiguous_edit_paths(self):
        first = BENCHMARK.alignment_error_profile(["aa"], ["a"])
        second = BENCHMARK.alignment_error_profile(["aa"], ["a"])
        self.assertEqual(first, second)
        self.assertEqual(first["total_deletions"], 1)

    def test_exact_matches_have_no_edit_confusions(self):
        result = BENCHMARK.alignment_error_profile(["ŋaː"], ["ŋaː"])
        self.assertEqual(result["total_substitutions"], 0)
        self.assertEqual(result["total_deletions"], 0)
        self.assertEqual(result["total_insertions"], 0)

    def test_neutral_syllable_has_no_invented_contour(self):
        self.assertEqual(
            BENCHMARK.render_mekong_tonal(
                ["kʰa", "kʰaː"], ["neutral", "high-rising"]
            ),
            "kʰakʰaː˧˥",
        )


if __name__ == "__main__":
    unittest.main()
