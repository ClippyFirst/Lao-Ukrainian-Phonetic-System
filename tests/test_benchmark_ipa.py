import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "benchmark_ipa.py"

def write_tsv(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

class BenchmarkIpaTests(unittest.TestCase):
    def run_benchmark(self, gold_rows, pred_rows):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            gold, pred, output = td / "gold.tsv", td / "pred.tsv", td / "report.json"
            write_tsv(gold, ["id", "text", "gold_ipa", "gold_status", "profile", "source_id"], gold_rows)
            write_tsv(pred, ["id", "engine", "raw_output", "ipa", "status", "version"], pred_rows)
            run = subprocess.run(
                [sys.executable, str(SCRIPT), "--gold", str(gold), "--predictions", str(pred), "--output", str(output)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(run.returncode, 0, msg=run.stderr)
            return json.loads(output.read_text(encoding="utf-8"))

    def test_empty_gold_does_not_report_accuracy(self):
        report = self.run_benchmark([], [
            {"id":"x", "engine":"candidate", "raw_output":"raw", "ipa":"a", "status":"ok", "version":"1"}
        ])
        self.assertEqual(report["gold"]["accuracy_status"], "NOT_MEASURED")
        self.assertIsNone(report["engines"]["candidate"]["exact_match_rate"])
        self.assertEqual(report["engines"]["candidate"]["status"], "NOT_MEASURED_NO_ADJUDICATED_OVERLAP")

    def test_scores_only_adjudicated_rows_and_preserves_diacritics(self):
        gold = [
            {"id":"a", "text":"x", "gold_ipa":"aː", "gold_status":"ADJUDICATED", "profile":"standard", "source_id":"src#1"},
            {"id":"b", "text":"y", "gold_ipa":"not-gold", "gold_status":"PROJECT_PROBE_NOT_GOLD", "profile":"", "source_id":""},
        ]
        pred = [
            {"id":"a", "engine":"candidate", "raw_output":"aː", "ipa":"aː", "status":"ok", "version":"1"},
            {"id":"b", "engine":"candidate", "raw_output":"not-gold", "ipa":"not-gold", "status":"ok", "version":"1"},
        ]
        report = self.run_benchmark(gold, pred)
        metrics = report["engines"]["candidate"]
        self.assertEqual(report["gold"]["rows_adjudicated"], 1)
        self.assertEqual(metrics["n_adjudicated_predictions"], 1)
        self.assertEqual(metrics["exact_matches"], 1)
        self.assertEqual(metrics["exact_match_rate"], 1.0)

    def test_mismatch_reports_edit_distance(self):
        report = self.run_benchmark(
            [{"id":"a", "text":"x", "gold_ipa":"k", "gold_status":"ADJUDICATED", "profile":"standard", "source_id":"src#1"}],
            [{"id":"a", "engine":"candidate", "raw_output":"g", "ipa":"g", "status":"ok", "version":"1"}],
        )
        metrics = report["engines"]["candidate"]
        self.assertEqual(metrics["exact_matches"], 0)
        self.assertEqual(metrics["codepoint_cer"], 1.0)

if __name__ == "__main__":
    unittest.main()
