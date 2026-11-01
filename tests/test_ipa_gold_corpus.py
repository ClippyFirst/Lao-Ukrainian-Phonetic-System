import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_NAME = ROOT.name.lower()
LANGUAGE = "khmer" if "khmer" in REPO_NAME else "burmese" if "burmese" in REPO_NAME else "lao"
SCRIPT = ROOT / "scripts" / "ipa_gold_corpus.py"

def ipa(value="ka", kind="PHONEMIC"):
    return {"value": value, "kind": kind, "syllable_boundaries": [value],
            "tone": None, "vowel_length": None, "phonation": None}

class IpaGoldCorpusTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.paths = {name: self.root / f"{name}.jsonl" for name in
                      ("records", "annotations", "adjudications", "splits")}
        self.records = [{
            "record_id": "r1", "language": LANGUAGE,
            "orthography": {"text": "ກາ", "normalized": "ກາ"},
            "lexeme_group_id": "lemma-1",
            "profile": {"id": "standard-lao", "variety": "Vientiane-oriented Standard Lao"},
            "source": {"source_id": "src-1", "citation": "Test source", "locator": "p. 1",
                       "rights_status": "OPEN", "redistributable": True, "license_id": "CC-BY-4.0"}
        }]
        self.annotations = [
            {"annotation_id": "a1", "record_id": "r1", "annotator_id": "ling-1",
             "ipa": ipa(), "confidence": "HIGH", "uncertainty": [], "notes": "", "annotated_at": "2026-11-01"},
            {"annotation_id": "a2", "record_id": "r1", "annotator_id": "ling-2",
             "ipa": ipa(), "confidence": "HIGH", "uncertainty": [], "notes": "", "annotated_at": "2026-11-01"}
        ]
        self.adjudications = [{
            "record_id": "r1", "adjudicator_id": "ling-3", "annotation_ids": ["a1", "a2"], "decision": "AGREEMENT",
            "final_ipa": ipa(), "rationale": "Both independent annotations agree.",
            "adjudicated_at": "2026-11-01"
        }]
        self.splits = [{"record_id": "r1", "group_id": "lemma-1", "split": "train",
                        "seed": "test-seed", "version": "v1"}]
        self.write_all()

    def tearDown(self):
        self.tmp.cleanup()

    def write_jsonl(self, name, rows):
        self.paths[name].write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")

    def write_all(self):
        for name, rows in (("records", self.records), ("annotations", self.annotations),
                           ("adjudications", self.adjudications), ("splits", self.splits)):
            self.write_jsonl(name, rows)

    def run_cli(self, command, *extra, expected=0):
        args = [sys.executable, str(SCRIPT), command, "--records", str(self.paths["records"])]
        if command == "assign-splits":
            args += ["--splits", str(self.paths["splits"])]
        else:
            args += ["--annotations", str(self.paths["annotations"]),
                     "--adjudications", str(self.paths["adjudications"]),
                     "--splits", str(self.paths["splits"]), "--language", LANGUAGE]
        args += list(map(str, extra))
        run = subprocess.run(args, text=True, capture_output=True, check=False)
        self.assertEqual(run.returncode, expected, msg=run.stdout + run.stderr)
        return run

    def test_accepts_two_independent_annotations_and_separate_adjudicator(self):
        run = self.run_cli("validate")
        report = json.loads(run.stdout)
        self.assertEqual(report["adjudicated_records"], 1)
        self.assertEqual(report["gold_status"], "ADJUDICATED_DATA_PRESENT")

    def test_rejects_adjudication_without_two_distinct_annotators(self):
        self.annotations.pop()
        self.write_all()
        run = self.run_cli("validate", expected=1)
        self.assertIn("exactly two distinct annotators", run.stderr)

    def test_rejects_adjudicator_who_is_an_annotator(self):
        self.adjudications[0]["adjudicator_id"] = "ling-1"
        self.write_all()
        run = self.run_cli("validate", expected=1)
        self.assertIn("must differ from both annotators", run.stderr)

    def test_rejects_agreement_label_when_annotations_disagree(self):
        self.annotations[1]["ipa"] = ipa("pa")
        self.write_all()
        run = self.run_cli("validate", expected=1)
        self.assertIn("AGREEMENT requires identical", run.stderr)

    def test_agreement_compares_tone_and_syllable_metadata_not_only_ipa_text(self):
        self.annotations[1]["ipa"]["tone"] = "H"
        self.write_all()
        run = self.run_cli("validate", expected=1)
        self.assertIn("AGREEMENT requires identical", run.stderr)

    def test_rejects_unresolved_case_with_final_ipa(self):
        self.adjudications[0].update({"decision": "UNRESOLVED", "final_ipa": ipa(), "rationale": "Not resolved."})
        self.write_all()
        run = self.run_cli("validate", expected=1)
        self.assertIn("UNRESOLVED must not contain final_ipa", run.stderr)

    def test_rejects_split_assignment_that_does_not_match_frozen_seed(self):
        self.splits[0]["split"] = "test"
        self.write_all()
        run = self.run_cli("validate", expected=1)
        self.assertIn("does not match deterministic hash", run.stderr)

    def test_rejects_split_leakage_for_same_lexeme_group(self):
        self.records.append(dict(self.records[0], record_id="r2", orthography={"text": "ກາໆ", "normalized": "ກາໆ"}))
        self.splits.append({"record_id": "r2", "group_id": "lemma-1", "split": "test", "seed": "test-seed", "version": "v1"})
        self.write_all()
        run = self.run_cli("validate", expected=1)
        self.assertIn("lexeme_group_id crosses splits", run.stderr)

    def test_rejects_non_redistributable_source_in_release_gate(self):
        self.records[0]["source"].update({"rights_status": "RESTRICTED", "redistributable": False})
        self.write_all()
        run = self.run_cli("gate", "--min-train", "1", "--min-dev", "0", "--min-test", "0", expected=1)
        self.assertIn("not redistributable", run.stderr)

    def test_split_assignment_is_deterministic_and_group_safe(self):
        self.records.append(dict(self.records[0], record_id="r2", orthography={"text": "ກາໆ", "normalized": "ກາໆ"}))
        self.splits = []
        self.write_all()
        self.run_cli("assign-splits", "--seed", "fixed-seed", "--output", self.root / "generated.jsonl")
        first = (self.root / "generated.jsonl").read_text(encoding="utf-8")
        self.run_cli("assign-splits", "--seed", "fixed-seed", "--output", self.root / "generated-2.jsonl")
        second = (self.root / "generated-2.jsonl").read_text(encoding="utf-8")
        self.assertEqual(first, second)
        rows = [json.loads(line) for line in first.splitlines()]
        self.assertEqual(len({row["split"] for row in rows}), 1)


    def test_new_records_inherit_frozen_group_split_and_seed(self):
        self.splits = []
        self.write_all()
        frozen = self.root / "frozen.jsonl"
        self.run_cli("assign-splits", "--seed", "first-seed", "--output", frozen)
        frozen_rows = [json.loads(line) for line in frozen.read_text(encoding="utf-8").splitlines()]
        self.write_jsonl("splits", frozen_rows)
        self.records.append(dict(self.records[0], record_id="r2",
                                 orthography={"text": "ກາໆ", "normalized": "ກາໆ"}))
        self.write_jsonl("records", self.records)
        extended = self.root / "extended.jsonl"
        self.run_cli("assign-splits", "--seed", "second-seed", "--output", extended)
        rows = [json.loads(line) for line in extended.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(rows[0]["split"], rows[1]["split"])
        self.assertEqual(rows[1]["seed"], "first-seed")

    def test_json_schemas_are_valid_draft_2020_documents(self):
        for name in ("record", "annotation", "adjudication", "split"):
            schema = json.loads((ROOT / "schemas" / f"ipa-gold-{name}.schema.json").read_text(encoding="utf-8"))
            self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
            self.assertEqual(schema["type"], "object")

    def test_gold_export_contains_only_adjudicated_redistributable_rows(self):
        output = self.root / "gold.tsv"
        self.run_cli("export-gold", "--output", output)
        with output.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["gold_status"], "ADJUDICATED")
        self.assertEqual(rows[0]["gold_ipa"], "ka")

    def test_empty_gold_is_not_release_ready(self):
        self.annotations = []
        self.adjudications = []
        self.splits = []
        self.write_all()
        run = self.run_cli("gate", "--min-train", "1", "--min-dev", "1", "--min-test", "1", expected=1)
        self.assertIn("release gate failed", run.stderr.lower())

if __name__ == "__main__":
    unittest.main()
