import unittest

from scripts.benchmark_additional_lao_g2p import has_runtime_errors, renderable_external_prediction


class AdditionalLaoG2PBenchmarkTests(unittest.TestCase):
    def test_empty_or_missing_external_prediction_is_explicit_unknown(self):
        self.assertEqual(renderable_external_prediction(""), "?")
        self.assertEqual(renderable_external_prediction(None), "?")
        self.assertEqual(renderable_external_prediction("kʰa"), "kʰa")

    def test_zero_runtime_errors_is_successful(self):
        self.assertFalse(has_runtime_errors([{"unexpected_errors": 0}]))

    def test_any_runtime_error_fails_the_benchmark(self):
        self.assertTrue(has_runtime_errors([
            {"engine": "first", "unexpected_errors": 0},
            {"engine": "second", "unexpected_errors": 1},
        ]))


if __name__ == "__main__":
    unittest.main()
