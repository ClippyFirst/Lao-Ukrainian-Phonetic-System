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
                       "rights_status": "OPEN", "redistributable": True, "license_id": "CC-BY-4.0",
                       "rights_evidence": {"basis": "LICENSE", "locator": "https://creativecommons.org/licenses/by/4.0/",
                                           "verified_by": "curator-1", "verified_at": "2026-11-01"}}
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

    def test_rejects_license_that_does_not_allow_redistribution(self):
        self.records[0]["source"]["license_id"] = "CC-BY-NC-SA-4.0"
        self.write_all()
        run = self.run_cli("validate", expected=1)
        self.assertIn("does not permit redistribution", run.stderr)

    def test_shared_ipa_schema_is_referenced_by_annotation_and_adjudication(self):
        schema_dir = ROOT / "schemas"
        ipa_schema = json.loads((schema_dir / "ipa-gold-ipa.schema.json").read_text(encoding="utf-8"))
        annotation = json.loads((schema_dir / "ipa-gold-annotation.schema.json").read_text(encoding="utf-8"))
        adjudication = json.loads((schema_dir / "ipa-gold-adjudication.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(ipa_schema["additionalProperties"], False)
        self.assertEqual(set(ipa_schema["required"]), {"value", "kind"})
        self.assertEqual(set(ipa_schema["properties"]), {
            "value", "kind", "syllable_boundaries", "tone", "vowel_length", "phonation"
        })
        self.assertEqual(annotation["properties"]["ipa"]["$ref"], "./ipa-gold-ipa.schema.json")
        self.assertEqual(adjudication["properties"]["final_ipa"]["oneOf"][0]["$ref"],
                         "./ipa-gold-ipa.schema.json")
        self.assertNotIn("$defs", annotation)
        self.assertNotIn("$defs", adjudication)

    def test_rejects_license_registry_missing_required_schema_flag(self):
        registry = json.loads((ROOT / "data" / "benchmark" / "licenses.json").read_text(encoding="utf-8"))
        del registry["licenses"]["CC-BY-4.0"]["share_alike"]
        license_path = self.root / "licenses.json"
        license_path.write_text(json.dumps(registry), encoding="utf-8")
        run = self.run_cli("validate", "--licenses", license_path, expected=1)
        self.assertIn("share_alike", run.stderr)

    def test_rejects_empty_license_registry(self):
        registry = json.loads((ROOT / "data" / "benchmark" / "licenses.json").read_text(encoding="utf-8"))
        registry["licenses"] = {}
        license_path = self.root / "licenses.json"
        license_path.write_text(json.dumps(registry), encoding="utf-8")
        run = self.run_cli("validate", "--licenses", license_path, expected=1)
        self.assertIn("at least one license", run.stderr)

    def test_rejects_invalid_license_uri(self):
        registry = json.loads((ROOT / "data" / "benchmark" / "licenses.json").read_text(encoding="utf-8"))
        registry["licenses"]["CC-BY-4.0"]["url"] = "not-a-uri"
        license_path = self.root / "licenses.json"
        license_path.write_text(json.dumps(registry), encoding="utf-8")
        run = self.run_cli("validate", "--licenses", license_path, expected=1)
        self.assertIn("valid URI", run.stderr)

    def test_rejects_unregistered_license(self):
        self.records[0]["source"]["license_id"] = "MADE-UP-LICENSE"
        self.write_all()
        run = self.run_cli("validate", expected=1)
        self.assertIn("unregistered license_id", run.stderr)

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
        for name in ("record", "annotation", "adjudication", "split", "licenses", "ipa"):
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
        self.assertEqual(rows[0]["license_id"], "CC-BY-4.0")
        self.assertTrue(rows[0]["rights_evidence_locator"].startswith("https://"))

    def test_rejects_annotation_missing_schema_required_notes(self):
        del self.annotations[0]["notes"]
        self.write_all()
        run = self.run_cli("validate", expected=1)
        self.assertIn("notes", run.stderr)

    def test_rejects_non_iso_annotation_date(self):
        self.annotations[0]["annotated_at"] = "yesterday"
        self.write_all()
        run = self.run_cli("validate", expected=1)
        self.assertIn("annotated_at", run.stderr)

    def test_rejects_unknown_record_properties(self):
        self.records[0]["unreviewed_ipa"] = "not-gold"
        self.write_all()
        run = self.run_cli("validate", expected=1)
        self.assertIn("unknown properties", run.stderr)

    def test_rejects_unknown_ipa_properties(self):
        self.annotations[0]["ipa"]["guessed_pronunciation"] = "not-gold"
        self.annotations[1]["ipa"]["guessed_pronunciation"] = "not-gold"
        self.write_all()
        run = self.run_cli("validate", expected=1)
        self.assertIn("unknown properties", run.stderr)

    def test_assign_splits_rejects_duplicate_record_ids(self):
        self.records.append(dict(self.records[0]))
        self.write_jsonl("records", self.records)
        run = self.run_cli("assign-splits", "--output", self.root / "generated.jsonl", expected=1)
        self.assertIn("duplicate record_id", run.stderr)

    def test_assign_splits_rejects_empty_lexeme_group_id(self):
        self.records[0]["lexeme_group_id"] = " "
        self.write_jsonl("records", self.records)
        run = self.run_cli("assign-splits", "--output", self.root / "generated.jsonl", expected=1)
        self.assertIn("lexeme_group_id", run.stderr)

    def test_assign_splits_rejects_inconsistent_group_versions(self):
        self.records.append(dict(self.records[0], record_id="r2",
                                 orthography={"text":"second", "normalized":"second"}))
        self.splits.append({"record_id":"r2", "group_id":"lemma-1", "split":"train",
                            "seed":"test-seed", "version":"v2"})
        self.write_all()
        run = self.run_cli("assign-splits", "--output", self.root / "generated.jsonl", expected=1)
        self.assertIn("inconsistent frozen split metadata", run.stderr)

    def test_empty_gold_is_not_release_ready(self):
        self.annotations = []
        self.adjudications = []
        self.splits = []
        self.write_all()
        run = self.run_cli("gate", "--min-train", "1", "--min-dev", "1", "--min-test", "1", expected=1)
        self.assertIn("release gate failed", run.stderr.lower())


    def test_rejects_independent_annotations_with_mixed_ipa_kinds(self):
        self.annotations[1]["ipa"] = ipa("ka", "PHONETIC_BROAD")
        self.adjudications[0]["decision"] = "RESOLVED"
        self.adjudications[0]["final_ipa"] = ipa("ka")
        self.adjudications[0]["rationale"] = "The annotators used different representation kinds."
        self.write_all()
        run = self.run_cli("validate", expected=1)
        self.assertIn("same IPA kind", run.stderr)

    def test_rejects_resolved_ipa_with_kind_different_from_annotations(self):
        self.annotations[1]["ipa"] = ipa("kʰa")
        self.adjudications[0]["decision"] = "RESOLVED"
        self.adjudications[0]["final_ipa"] = ipa("ka", "PHONETIC_BROAD")
        self.adjudications[0]["rationale"] = "The final result must retain the annotation convention."
        self.write_all()
        run = self.run_cli("validate", expected=1)
        self.assertIn("final_ipa.kind must match annotation IPA kind", run.stderr)

    def test_assign_splits_rejects_unknown_properties_in_existing_manifest(self):
        self.splits[0]["unexpected"] = "must-not-be-dropped"
        self.write_all()
        output = self.root / "generated.jsonl"
        run = self.run_cli("assign-splits", "--seed", "test-seed", "--output", output, expected=1)
        self.assertIn("unknown properties: unexpected", run.stderr)

if __name__ == "__main__":
    unittest.main()
