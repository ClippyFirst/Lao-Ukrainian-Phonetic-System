"""Tests for the offline Lao word-boundary research baseline."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "benchmark_lao_word_boundaries.py"


def git_blob_sha1(text):
    raw = text.encode("utf-8")
    return hashlib.sha1(f"blob {len(raw)}".encode("ascii") + bytes([0]) + raw).hexdigest()


class LaoWordBoundaryResearchTests(unittest.TestCase):
    def run_script(self, raw, segmented, dictionary, *extra):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw_path = root / "raw.txt"
            segmented_path = root / "segmented.txt"
            dictionary_path = root / "dictionary.txt"
            raw_path.write_text(raw, encoding="utf-8")
            segmented_path.write_text(segmented, encoding="utf-8")
            dictionary_path.write_text(dictionary, encoding="utf-8")
            return subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--raw",
                    str(raw_path),
                    "--segmented",
                    str(segmented_path),
                    "--dictionary",
                    str(dictionary_path),
                    *extra,
                ],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_longest_and_shortest_prefix_strategies_are_distinct(self):
        raw = "ກຂຄ\n"
        segmented = "ກ ຂຄ\n"
        dictionary = "# word list\nກ\nກຂ\nຂ\nຂຄ\n"
        result = self.run_script(raw, segmented, dictionary)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        longest, shortest = report["results"]
        self.assertEqual(longest["strategy"], "longest")
        self.assertEqual(shortest["strategy"], "shortest")
        self.assertEqual(longest["true_positive"], 0)
        self.assertEqual(longest["false_positive"], 1)
        self.assertEqual(longest["false_negative"], 1)
        self.assertEqual(shortest["true_positive"], 1)
        self.assertEqual(shortest["false_positive"], 1)
        self.assertEqual(shortest["false_negative"], 0)
        self.assertEqual(report["dictionary_entries"], 4)
        self.assertEqual(report["input_sentence_pairs"], 1)

    def test_unaligned_pairs_are_excluded_not_silently_scored(self):
        raw = "ກຂ\nກຂ\n"
        segmented = "ກ ຂ\nກ ຄ\n"
        dictionary = "ກ\nຂ\n"
        result = self.run_script(raw, segmented, dictionary)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        for strategy in report["results"]:
            self.assertEqual(strategy["aligned_sentences"], 1)
            self.assertEqual(strategy["unaligned_sentences"], 1)

    def test_line_count_mismatch_fails_closed(self):
        result = self.run_script("ກ\n", "ກ\nຂ\n", "ກ\n")
        self.assertEqual(result.returncode, 2)
        self.assertIn("same number of lines", result.stderr)

    def test_git_blob_hash_mismatch_fails_closed(self):
        result = self.run_script(
            "ກ\n",
            "ກ\n",
            "ກ\n",
            "--raw-blob-sha1",
            "0" * 40,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("Git blob SHA-1 mismatch", result.stderr)

    def test_expected_git_blob_hash_is_reported(self):
        raw = "ກ\n"
        segmented = "ກ\n"
        dictionary = "ກ\n"
        result = self.run_script(
            raw,
            segmented,
            dictionary,
            "--raw-blob-sha1",
            git_blob_sha1(raw),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["input_git_blob_sha1"]["raw"], git_blob_sha1(raw))
        self.assertFalse(report["limitations"] == [])
        self.assertIn("not ALA-LC Note 9", report["scope"])


if __name__ == "__main__":
    unittest.main()
