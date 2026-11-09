"""Regression checks for the deterministic Kaikki Lao source-provenance sample manifest."""
import csv
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "evidence" / "kaikki_lao_ipa_provenance_sample_2026-11-09.csv"


class KaikkiProvenanceManifestTests(unittest.TestCase):
    def test_manifest_is_a_complete_deterministic_100_page_sample(self):
        with MANIFEST.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 100)
        self.assertEqual([int(row["sample_rank"]) for row in rows], list(range(1, 101)))
        self.assertEqual(len({row["word"] for row in rows}), 100)
        self.assertEqual(len({row["pageid"] for row in rows}), 100)
        self.assertEqual(len({row["revid"] for row in rows}), 100)
        self.assertTrue(all(row["has_direct_lo_pron"] == "true" for row in rows))
        cutoff = datetime(2026, 10, 1, 23, 59, 59, tzinfo=timezone.utc)
        for row in rows:
            timestamp = datetime.fromisoformat(row["revision_timestamp"].replace("Z", "+00:00"))
            self.assertLessEqual(timestamp, cutoff)
            self.assertIn("lo-pron", row["pronunciation_template_names"].split(";"))
            self.assertGreater(int(row["source_wikitext_chars"]), 0)

    def test_manifest_hash_order_is_monotonic(self):
        with MANIFEST.open(encoding="utf-8", newline="") as handle:
            hashes = [int(row["codepoint_fnv1a32"]) for row in csv.DictReader(handle)]
        self.assertEqual(hashes, sorted(hashes))


if __name__ == "__main__":
    unittest.main()
