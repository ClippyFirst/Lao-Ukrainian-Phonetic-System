"""Regression tests for the offline LaoNLP dictionary audit utility."""
import csv
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_laonlp_dictionary.py"


class LaoNlpDictionaryAuditTests(unittest.TestCase):
    def run_audit(self, content, *args):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "dictionary.csv"
            path.write_text(content, encoding="utf-8", newline="")
            return subprocess.run(
                [sys.executable, str(SCRIPT), str(path), *args],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_counts_repeated_headers_placeholders_and_duplicate_words(self):
        content = (
            "ID,LaoWord,English,Pronunciation,Type\n"
            '1,ກ,"first, gloss",ka,n\n'
            "2,ກ,second,ka,n\n"
            "3,LaoWord,English,Pronunciation,Type\n"
            "4,,,,\n"
        )
        result = self.run_audit(content)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["rows_after_first_header"], 4)
        self.assertEqual(report["repeated_header_rows"], 1)
        self.assertEqual(report["malformed_header_like_rows"], 0)
        self.assertEqual(report["header_like_rows_total"], 1)
        self.assertEqual(report["id_only_placeholder_rows"], 1)
        self.assertEqual(report["usable_records"], 2)
        self.assertEqual(report["unique_lao_words"], 1)
        self.assertEqual(report["forms_with_multiple_records"], 1)
        self.assertEqual(report["malformed_width_rows"], 0)
        self.assertFalse(report["runtime_imported"])


    def test_malformed_header_like_rows_are_separate_from_exact_headers(self):
        content = (
            "ID,LaoWord,English,Pronunciation,Type\n"
            "1,ກ,gloss,ka,n\n"
            "2,,English,Pronuciation,Type\n"
            "3,LaoWord,English,Pronunciation,Type\n"
            "4,,,,\n"
        )
        result = self.run_audit(content)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["repeated_header_rows"], 1)
        self.assertEqual(report["malformed_header_like_rows"], 1)
        self.assertEqual(report["header_like_rows_total"], 2)
        self.assertEqual(report["id_only_placeholder_rows"], 1)
        self.assertEqual(report["usable_records"], 1)
        self.assertEqual(report["unique_lao_words"], 1)

    def test_hash_mismatch_fails_closed(self):
        result = self.run_audit(
            "ID,LaoWord,English,Pronunciation,Type\n1,ກ,first,ka,n\n",
            "--expected-sha1",
            "0000000000000000000000000000000000000000",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("Git blob SHA-1 mismatch", result.stderr)

    def test_expected_hash_uses_git_blob_object_sha1(self):
        content = "ID,LaoWord,English,Pronunciation,Type\n1,ກ,first,ka,n\n"
        raw = content.encode("utf-8")
        expected = hashlib.sha1(f"blob {len(raw)}".encode("ascii") + bytes([0]) + raw).hexdigest()
        result = self.run_audit(content, "--expected-sha1", expected)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["git_blob_sha1"], expected)

    def test_wrong_header_fails_closed(self):
        result = self.run_audit("id,word,gloss,pron,type\n1,ກ,first,ka,n\n")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unexpected CSV header", result.stderr)


if __name__ == "__main__":
    unittest.main()
