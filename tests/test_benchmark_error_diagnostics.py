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

    def test_unresolved_tone_categories_render_an_explicit_unknown_marker(self):
        self.assertEqual(BENCHMARK.render_mekong_tonal(["kʰa"], [None]), "kʰa?")

    def test_project_predict_emits_minor_syllable_diagnostics_without_runtime_error(self):
        predict = BENCHMARK.load_project()
        result = predict("ຄະຄາ")
        self.assertEqual(result["status"], "PARTIAL")
        self.assertIsNone(result["tone_categories"][0])
        context = result["tone_contexts"][0]
        self.assertTrue(context["candidate_minor_shape"])
        self.assertTrue(context["candidate_minor_open_a_shape"])
        self.assertTrue(context["following_major_weighted"])
        self.assertEqual(context["analysis_status"], "analysis-dependent")

    def test_unresolved_tone_is_not_counted_as_a_literal_category(self):
        result = BENCHMARK.score_tone_categories(
            [["high-mid", "low-rising"], ["high-falling"]],
            [[None, "low-rising"], ["high-mid"]],
        )
        self.assertEqual(result["covered_categories"], 2)
        self.assertEqual(result["unresolved_categories"], 1)
        self.assertEqual(result["unresolved_words"], 1)
        self.assertEqual(result["coverage"], 2 / 3)
        self.assertEqual(result["category_error_rate"], 0.5)
        self.assertEqual(result["exact_matches"], 0)
        self.assertEqual(result["complete_words"], 1)

    def test_tone_category_length_mismatch_is_reported_as_unresolved(self):
        result = BENCHMARK.score_tone_categories(
            [["high-mid", "low-rising"]],
            [["high-mid"]],
        )
        self.assertEqual(result["word_length_mismatches"], 1)
        self.assertEqual(result["covered_categories"], 0)
        self.assertEqual(result["unresolved_categories"], 2)
        self.assertEqual(result["coverage"], 0.0)

    def test_project_predict_emits_minor_syllable_diagnostics_without_runtime_error(self):
        predict = BENCHMARK.load_project()
        result = predict("ຄະຄາ")
        self.assertEqual(result["status"], "PARTIAL")
        self.assertEqual(result["tone_categories"][0], None)
        context = result["tone_contexts"][0]
        self.assertTrue(context["candidate_minor_shape"])
        self.assertTrue(context["candidate_minor_open_a_shape"])
        self.assertTrue(context["following_major_weighted"])
        self.assertEqual(context["analysis_status"], "analysis-dependent")

    def test_optional_affricate_tie_bars_are_secondary_allographs_only(self):
        self.assertEqual(BENCHMARK.remove_optional_ipa_tie_bars("t͡ɕa"), "tɕa")
        self.assertEqual(BENCHMARK.remove_optional_ipa_tie_bars("t͜ɕa"), "tɕa")
        self.assertEqual(BENCHMARK.remove_optional_ipa_tie_bars("kʰaː"), "kʰaː")


if __name__ == "__main__":
    unittest.main()
