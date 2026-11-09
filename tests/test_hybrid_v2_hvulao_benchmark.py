import unittest
from collections import Counter

from scripts.benchmark_hybrid_v2_hvulao_1k import new_counts


class HybridV2HVULaoBenchmarkTests(unittest.TestCase):
    def test_counter_schema_starts_at_zero_and_separates_coverage_lanes(self):
        counts = new_counts()
        self.assertEqual(counts["rows_with_ukrainian_rendering"], 0)
        self.assertEqual(counts["rows_with_complete_segmental_ipa"], 0)
        self.assertEqual(counts["rows_with_parseable_tonal_ipa"], 0)
        self.assertEqual(counts["tone_prediction_units"], 0)
        self.assertIsInstance(counts["errors"], Counter)
        self.assertIsInstance(counts["input_rejections"], Counter)
        self.assertIsInstance(counts["tonal_ipa_parse_statuses"], Counter)
        self.assertIsInstance(counts["tonal_ipa_parse_warning_categories"], Counter)
        self.assertIsInstance(counts["tone_alignment_warning_categories"], Counter)

