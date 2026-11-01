#!/usr/bin/env python3
"""Validate and manage independently annotated IPA gold data.

Uses only the Python standard library. Synthetic fixtures belong in tests only.
No automatic phonemizer output is ever promoted to gold.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import unicodedata
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

SPLITS = ("train", "dev", "test")
IPA_KINDS = ("PHONEMIC", "PHONETIC_BROAD", "PHONETIC_NARROW")
ADJUDICATED_DECISIONS = ("AGREEMENT", "RESOLVED")
RIGHTS = ("OPEN", "PROJECT_CREATED", "RESTRICTED", "UNKNOWN")
SPLIT_PROPERTIES = {"record_id", "group_id", "split", "seed", "version"}
GOLD_FIELDS = ("id", "text", "gold_ipa", "gold_status", "profile", "source_id", "ipa_kind", "license_id", "rights_evidence_locator")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise ValueError(f"required corpus file does not exist: {path}")
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            try:
                value = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc.msg}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_no}: each JSONL row must be an object")
            rows.append(value)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value


def reject_unknown_properties(value: dict[str, Any], allowed: set[str], label: str) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise ValueError(f"{label}: unknown properties: {', '.join(unknown)}")


def require_iso_date(value: Any, label: str) -> str:
    raw = require_text(value, label)
    try:
        parsed = date.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError(f"{label} must be an ISO 8601 calendar date (YYYY-MM-DD)") from exc
    if parsed.isoformat() != raw:
        raise ValueError(f"{label} must use canonical YYYY-MM-DD format")
    return raw


def require_uri(value: Any, label: str) -> str:
    raw = require_text(value, label)
    parsed = urlsplit(raw)
    if not parsed.scheme or (parsed.scheme.lower() in ("http", "https") and not parsed.netloc):
        raise ValueError(f"{label} must be a valid URI")
    return raw


def validate_ipa(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an IPA object")
    reject_unknown_properties(value, {"value", "kind", "syllable_boundaries", "tone", "vowel_length", "phonation"}, label)
    ipa = require_text(value.get("value"), f"{label}.value")
    kind = require_text(value.get("kind"), f"{label}.kind")
    if kind not in IPA_KINDS:
        raise ValueError(f"{label}.kind must be one of {', '.join(IPA_KINDS)}")
    if unicodedata.normalize("NFC", ipa) != ipa:
        raise ValueError(f"{label}.value must be NFC-normalized; do not silently rewrite IPA")
    boundaries = value.get("syllable_boundaries", [])
    if not isinstance(boundaries, list) or any(not isinstance(item, str) or not item for item in boundaries):
        raise ValueError(f"{label}.syllable_boundaries must be an array of non-empty strings")
    for feature in ("tone", "vowel_length", "phonation"):
        if value.get(feature) is not None and not isinstance(value[feature], str):
            raise ValueError(f"{label}.{feature} must be a string or null")
    return value


def validate_corpus(args: argparse.Namespace) -> dict[str, Any]:
    records = read_jsonl(args.records)
    try:
        license_document = json.loads(args.licenses.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{args.licenses}: invalid license registry JSON: {exc.msg}") from exc
    if not isinstance(license_document, dict):
        raise ValueError(f"{args.licenses}: license registry must be an object")
    reject_unknown_properties(license_document, {"schema_version", "licenses"}, "license registry")
    require_text(license_document.get("schema_version"), "license registry.schema_version")
    license_registry = license_document.get("licenses")
    if not isinstance(license_registry, dict) or not license_registry:
        raise ValueError(f"{args.licenses}: licenses must contain at least one license")
    for license_id, license_info in license_registry.items():
        if not isinstance(license_info, dict):
            raise ValueError(f"license registry entry {license_id!r} must be an object")
        for field in ("redistributable", "commercial_use", "attribution_required", "share_alike"):
            if field not in license_info:
                raise ValueError(f"license registry entry {license_id!r} missing required property {field}")
            value = license_info[field]
            if field == "redistributable":
                if not isinstance(value, bool):
                    raise ValueError(f"license registry entry {license_id!r} must define boolean redistributable")
            elif value is not None and not isinstance(value, bool):
                raise ValueError(f"license registry entry {license_id!r}.{field} must be boolean or null")
        if license_info.get("url") is not None:
            require_uri(license_info["url"], f"license registry entry {license_id!r}.url")
        if "note" in license_info and not isinstance(license_info["note"], str):
            raise ValueError(f"license registry entry {license_id!r}.note must be a string")
        if license_info["redistributable"]:
            if license_info["commercial_use"] is not True:
                raise ValueError(f"license registry entry {license_id!r}: redistributable license must explicitly permit commercial use")
            for field in ("attribution_required", "share_alike"):
                if not isinstance(license_info[field], bool):
                    raise ValueError(f"license registry entry {license_id!r}: redistributable license must define boolean {field}")
    annotations = read_jsonl(args.annotations)
    adjudications = read_jsonl(args.adjudications)
    splits = read_jsonl(args.splits)

    record_by_id: dict[str, dict[str, Any]] = {}
    for row in records:
        reject_unknown_properties(row, {"record_id", "language", "orthography", "lexeme_group_id", "profile", "source"}, "record")
        ident = require_text(row.get("record_id"), "record.record_id")
        if ident in record_by_id:
            raise ValueError(f"duplicate record_id: {ident}")
        if row.get("language") != args.language:
            raise ValueError(f"record {ident}: language must be {args.language!r}")
        orth = row.get("orthography")
        if not isinstance(orth, dict):
            raise ValueError(f"record {ident}: orthography must be an object")
        require_text(orth.get("text"), f"record {ident}.orthography.text")
        require_text(orth.get("normalized"), f"record {ident}.orthography.normalized")
        segmentation = orth.get("segmentation")
        if segmentation is not None and (not isinstance(segmentation, list) or any(not isinstance(item, str) for item in segmentation)):
            raise ValueError(f"record {ident}.orthography.segmentation must be an array of strings or null")
        require_text(row.get("lexeme_group_id"), f"record {ident}.lexeme_group_id")
        profile = row.get("profile")
        if not isinstance(profile, dict):
            raise ValueError(f"record {ident}: profile must be an object")
        require_text(profile.get("id"), f"record {ident}.profile.id")
        require_text(profile.get("variety"), f"record {ident}.profile.variety")
        for field in ("region", "register", "speaker_id", "audio_id"):
            if profile.get(field) is not None and not isinstance(profile[field], str):
                raise ValueError(f"record {ident}.profile.{field} must be a string or null")
        source = row.get("source")
        if not isinstance(source, dict):
            raise ValueError(f"record {ident}: source must be an object")
        for field in ("source_id", "citation", "locator", "license_id"):
            require_text(source.get(field), f"record {ident}.source.{field}")
        if source.get("url") is not None:
            require_uri(source["url"], f"record {ident}.source.url")
        digest = source.get("sha256")
        if digest is not None and (not isinstance(digest, str) or len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest)):
            raise ValueError(f"record {ident}.source.sha256 must be a lowercase 64-character SHA-256 digest")
        license_id = source["license_id"]
        license_info = license_registry.get(license_id)
        if not isinstance(license_info, dict):
            raise ValueError(f"record {ident}: unregistered license_id {license_id!r}")
        if not isinstance(license_info.get("redistributable"), bool):
            raise ValueError(f"license registry entry {license_id!r} must define boolean redistributable")
        rights_evidence = source.get("rights_evidence")
        if not isinstance(rights_evidence, dict):
            raise ValueError(f"record {ident}: source.rights_evidence must be an object")
        basis = require_text(rights_evidence.get("basis"), f"record {ident}.source.rights_evidence.basis")
        if basis not in ("LICENSE", "DIRECT_PERMISSION", "PUBLIC_DOMAIN", "PROJECT_CREATED", "UNKNOWN"):
            raise ValueError(f"record {ident}: invalid rights evidence basis {basis!r}")
        for field in ("locator", "verified_by"):
            require_text(rights_evidence.get(field), f"record {ident}.source.rights_evidence.{field}")
        require_iso_date(rights_evidence.get("verified_at"), f"record {ident}.source.rights_evidence.verified_at")
        if source.get("rights_status") not in RIGHTS:
            raise ValueError(f"record {ident}: source.rights_status must be one of {', '.join(RIGHTS)}")
        if not isinstance(source.get("redistributable"), bool):
            raise ValueError(f"record {ident}: source.redistributable must be boolean")
        if source["redistributable"] and not license_info["redistributable"]:
            raise ValueError(f"record {ident}: license {license_id!r} does not permit redistribution")
        rights_status = source["rights_status"]
        if rights_status == "OPEN" and (not license_info["redistributable"] or basis not in ("LICENSE", "DIRECT_PERMISSION", "PUBLIC_DOMAIN")):
            raise ValueError(f"record {ident}: OPEN rights require a redistributable license and verified rights evidence")
        if rights_status == "PROJECT_CREATED" and (license_id != "PROJECT-CREATED" or basis != "PROJECT_CREATED"):
            raise ValueError(f"record {ident}: PROJECT_CREATED rights require PROJECT-CREATED license and evidence")
        if rights_status in ("RESTRICTED", "UNKNOWN") and source["redistributable"]:
            raise ValueError(f"record {ident}: {rights_status} source cannot be marked redistributable")
        record_by_id[ident] = row

    annotations_by_record: dict[str, list[dict[str, Any]]] = defaultdict(list)
    annotation_ids: set[str] = set()
    annotator_ids: dict[str, set[str]] = defaultdict(set)
    for row in annotations:
        ident = require_text(row.get("record_id"), "annotation.record_id")
        if ident not in record_by_id:
            raise ValueError(f"annotation references unknown record_id: {ident}")
        annotation_id = require_text(row.get("annotation_id"), "annotation.annotation_id")
        reject_unknown_properties(row, {"annotation_id", "record_id", "annotator_id", "ipa", "confidence", "uncertainty", "notes", "annotated_at"}, f"annotation {annotation_id}")
        if annotation_id in annotation_ids:
            raise ValueError(f"duplicate annotation_id: {annotation_id}")
        annotation_ids.add(annotation_id)
        annotator = require_text(row.get("annotator_id"), f"annotation {annotation_id}.annotator_id")
        if annotator in annotator_ids[ident]:
            raise ValueError(f"record {ident}: duplicate annotation by annotator {annotator}")
        annotator_ids[ident].add(annotator)
        validate_ipa(row.get("ipa"), f"annotation {annotation_id}.ipa")
        if row.get("confidence") not in ("HIGH", "MEDIUM", "LOW", "UNSET"):
            raise ValueError(f"annotation {annotation_id}: invalid confidence")
        uncertainty = row.get("uncertainty")
        if not isinstance(uncertainty, list) or any(not isinstance(item, str) for item in uncertainty):
            raise ValueError(f"annotation {annotation_id}: uncertainty must be an array of strings")
        if not isinstance(row.get("notes"), str):
            raise ValueError(f"annotation {annotation_id}: notes must be a string")
        require_iso_date(row.get("annotated_at"), f"annotation {annotation_id}.annotated_at")
        annotations_by_record[ident].append(row)
    for ident, rows in annotations_by_record.items():
        if len(rows) > 2:
            raise ValueError(f"record {ident}: exactly two distinct annotators are supported; found more than two")
        if len({row["ipa"]["kind"] for row in rows}) > 1:
            raise ValueError(f"record {ident}: independent annotations must use the same IPA kind")

    adjudication_by_record: dict[str, dict[str, Any]] = {}
    for row in adjudications:
        ident = require_text(row.get("record_id"), "adjudication.record_id")
        reject_unknown_properties(row, {"record_id", "adjudicator_id", "annotation_ids", "decision", "final_ipa", "rationale", "adjudicated_at"}, f"adjudication {ident}")
        if ident not in record_by_id:
            raise ValueError(f"adjudication references unknown record_id: {ident}")
        if ident in adjudication_by_record:
            raise ValueError(f"duplicate adjudication for record_id: {ident}")
        adjudicator = require_text(row.get("adjudicator_id"), f"adjudication {ident}.adjudicator_id")
        decision = require_text(row.get("decision"), f"adjudication {ident}.decision")
        rationale = require_text(row.get("rationale"), f"adjudication {ident}.rationale")
        require_iso_date(row.get("adjudicated_at"), f"adjudication {ident}.adjudicated_at")
        source_annotators = annotator_ids.get(ident, set())
        if len(source_annotators) != 2:
            raise ValueError(f"record {ident}: adjudication requires exactly two distinct annotators")
        refs = row.get("annotation_ids")
        if not isinstance(refs, list) or len(refs) != 2 or set(refs) != {a["annotation_id"] for a in annotations_by_record.get(ident, [])}:
            raise ValueError(f"adjudication {ident}: annotation_ids must reference both independent annotations")
        if adjudicator in source_annotators:
            raise ValueError(f"record {ident}: adjudicator_id must differ from both annotators")
        pair = annotations_by_record[ident]
        same = pair[0]["ipa"] == pair[1]["ipa"]
        if decision == "AGREEMENT":
            final_ipa = validate_ipa(row.get("final_ipa"), f"adjudication {ident}.final_ipa")
            if not same:
                raise ValueError(f"record {ident}: AGREEMENT requires identical independent IPA annotations")
            if final_ipa != pair[0]["ipa"]:
                raise ValueError(f"record {ident}: AGREEMENT final_ipa must equal both annotations")
        elif decision == "RESOLVED":
            final_ipa = validate_ipa(row.get("final_ipa"), f"adjudication {ident}.final_ipa")
            if same:
                raise ValueError(f"record {ident}: identical annotations must use AGREEMENT, not RESOLVED")
            if final_ipa["kind"] != pair[0]["ipa"]["kind"]:
                raise ValueError(f"record {ident}: final_ipa.kind must match annotation IPA kind")
        elif decision == "UNRESOLVED":
            if row.get("final_ipa") is not None:
                raise ValueError(f"record {ident}: UNRESOLVED must not contain final_ipa")
        else:
            raise ValueError(f"record {ident}: decision must be AGREEMENT, RESOLVED or UNRESOLVED")
        adjudication_by_record[ident] = row

    split_by_record: dict[str, dict[str, Any]] = {}
    split_by_group: dict[str, str] = {}
    split_meta_by_group: dict[str, tuple[str, str]] = {}
    for row in splits:
        ident = require_text(row.get("record_id"), "split.record_id")
        reject_unknown_properties(row, SPLIT_PROPERTIES, f"split {ident}")
        if ident not in record_by_id:
            raise ValueError(f"split references unknown record_id: {ident}")
        if ident in split_by_record:
            raise ValueError(f"duplicate split assignment for record_id: {ident}")
        group = require_text(row.get("group_id"), f"split {ident}.group_id")
        if group != record_by_id[ident]["lexeme_group_id"]:
            raise ValueError(f"split {ident}: group_id must equal record.lexeme_group_id")
        split = row.get("split")
        if split not in SPLITS:
            raise ValueError(f"split {ident}: split must be train, dev or test")
        seed = require_text(row.get("seed"), f"split {ident}.seed")
        version = require_text(row.get("version"), f"split {ident}.version")
        if group in split_by_group and split_by_group[group] != split:
            raise ValueError(f"lexeme_group_id crosses splits: {group}")
        if group in split_meta_by_group and split_meta_by_group[group] != (seed, version):
            raise ValueError(f"lexeme_group_id has inconsistent split seed/version: {group}")
        if split != group_split(group, seed):
            raise ValueError(f"split {ident} does not match deterministic hash for seed {seed!r}")
        split_by_group[group] = split
        split_meta_by_group[group] = (seed, version)
        split_by_record[ident] = row

    adjudicated = {ident: row for ident, row in adjudication_by_record.items()
                   if row["decision"] in ADJUDICATED_DECISIONS}
    unresolved = [ident for ident, row in adjudication_by_record.items() if row["decision"] == "UNRESOLVED"]
    return {
        "language": args.language,
        "records": record_by_id,
        "annotations_by_record": annotations_by_record,
        "adjudications": adjudication_by_record,
        "splits": split_by_record,
        "adjudicated": adjudicated,
        "unresolved": unresolved,
        "summary": {
            "records_total": len(records),
            "annotations_total": len(annotations),
            "adjudicated_records": len(adjudicated),
            "unresolved_records": len(unresolved),
            "split_assignments": len(split_by_record),
            "gold_status": "ADJUDICATED_DATA_PRESENT" if adjudicated else "NOT_READY_NO_ADJUDICATED_GOLD",
        },
    }


def group_split(group_id: str, seed: str) -> str:
    digest = hashlib.sha256(f"{seed}\0{group_id}".encode("utf-8")).digest()
    bucket = int.from_bytes(digest[:8], "big") % 100
    return "train" if bucket < 80 else "dev" if bucket < 90 else "test"


def command_assign(args: argparse.Namespace) -> int:
    seed = require_text(args.seed, "--seed")
    version = require_text(args.version, "--version")
    records = read_jsonl(args.records)
    existing = read_jsonl(args.splits)
    record_by_id: dict[str, dict[str, Any]] = {}
    for record in records:
        ident = require_text(record.get("record_id"), "record.record_id")
        if ident in record_by_id:
            raise ValueError(f"duplicate record_id: {ident}")
        require_text(record.get("lexeme_group_id"), f"record {ident}.lexeme_group_id")
        record_by_id[ident] = record

    existing_by_group: dict[str, dict[str, Any]] = {}
    existing_by_id: dict[str, dict[str, Any]] = {}
    for row in existing:
        ident = require_text(row.get("record_id"), "split.record_id")
        reject_unknown_properties(row, SPLIT_PROPERTIES, f"split {ident}")
        if ident not in record_by_id:
            raise ValueError(f"split references unknown record_id: {ident}")
        group = require_text(row.get("group_id"), f"split {ident}.group_id")
        if group != record_by_id[ident].get("lexeme_group_id"):
            raise ValueError(f"split {ident}: group_id must equal record.lexeme_group_id")
        if row.get("split") not in SPLITS:
            raise ValueError(f"split {ident}: invalid split")
        row_seed = require_text(row.get("seed"), f"split {ident}.seed")
        row_version = require_text(row.get("version"), f"split {ident}.version")
        if row["split"] != group_split(group, row_seed):
            raise ValueError(f"split {ident} does not match deterministic hash for its seed")
        assignment = {"split": row["split"], "seed": row_seed, "version": row_version}
        group_prior = existing_by_group.get(group)
        if group_prior and group_prior != assignment:
            raise ValueError(f"inconsistent frozen split metadata for lexeme_group_id: {group}")
        if ident in existing_by_id:
            raise ValueError(f"duplicate split assignment for record_id: {ident}")
        existing_by_group[group] = assignment
        existing_by_id[ident] = assignment

    output = []
    for ident, record in sorted(record_by_id.items()):
        group = record["lexeme_group_id"]
        prior = existing_by_id.get(ident)
        group_prior = existing_by_group.get(group)
        assigned = group_prior["split"] if group_prior else group_split(group, seed)
        output.append({
            "record_id": ident, "group_id": group, "split": assigned,
            "seed": prior["seed"] if prior else group_prior["seed"] if group_prior else seed,
            "version": prior["version"] if prior else group_prior["version"] if group_prior else version,
        })
    write_jsonl(args.output, output)
    print(json.dumps({"assigned_records": len(output), "output": str(args.output),
                      "seed": seed, "existing_assignments_preserved": len(existing)}, ensure_ascii=False))
    return 0

def export_gold(args: argparse.Namespace, data: dict[str, Any]) -> int:
    rows = []
    for ident, adjudication in sorted(data["adjudicated"].items()):
        record = data["records"][ident]
        source = record["source"]
        if source["rights_status"] not in ("OPEN", "PROJECT_CREATED") or not source["redistributable"]:
            continue
        ipa = adjudication["final_ipa"]
        rows.append({
            "id": ident, "text": record["orthography"]["text"], "gold_ipa": ipa["value"],
            "gold_status": "ADJUDICATED", "profile": record["profile"]["id"],
            "source_id": source["source_id"], "ipa_kind": ipa["kind"],
            "license_id": source["license_id"],
            "rights_evidence_locator": source["rights_evidence"]["locator"],
        })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=GOLD_FIELDS, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({"exported_gold_rows": len(rows), "excluded_rights_rows":
                      len(data["adjudicated"]) - len(rows), "output": str(args.output)}))
    return 0


def release_gate(args: argparse.Namespace, data: dict[str, Any]) -> int:
    problems = []
    adjudicated = data["adjudicated"]
    if not adjudicated:
        problems.append("no independently adjudicated IPA records")
    counts = {split: 0 for split in SPLITS}
    for ident in adjudicated:
        record = data["records"][ident]
        assignment = data["splits"].get(ident)
        if assignment is None:
            problems.append(f"adjudicated record {ident} has no frozen split")
        else:
            counts[assignment["split"]] += 1
        source = record["source"]
        if source["rights_status"] not in ("OPEN", "PROJECT_CREATED") or not source["redistributable"]:
            problems.append(f"adjudicated record {ident} source is not redistributable")
    minimums = {"train": args.min_train, "dev": args.min_dev, "test": args.min_test}
    for split, minimum in minimums.items():
        if counts[split] < minimum:
            problems.append(f"{split} has {counts[split]} adjudicated records; requires {minimum}")
    if problems:
        raise ValueError("release gate failed: " + "; ".join(problems))
    print(json.dumps({"release_ready": True, "adjudicated_records": len(adjudicated),
                      "counts_by_split": counts, "minimums": minimums}))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    def add_paths(command: argparse.ArgumentParser) -> None:
        command.add_argument("--records", type=Path, default=Path("data/benchmark/records.jsonl"))
        command.add_argument("--annotations", type=Path, default=Path("data/benchmark/annotations.jsonl"))
        command.add_argument("--adjudications", type=Path, default=Path("data/benchmark/adjudications.jsonl"))
        command.add_argument("--splits", type=Path, default=Path("data/benchmark/splits.jsonl"))
        command.add_argument("--language", required=True, choices=("lao", "khmer", "burmese"))
        command.add_argument("--licenses", type=Path, default=Path("data/benchmark/licenses.json"))
    validate = sub.add_parser("validate", help="validate corpus provenance and annotation workflow")
    add_paths(validate)
    validate.add_argument("--report", type=Path)
    for name in ("export-gold", "gate"):
        command = sub.add_parser(name)
        add_paths(command)
        command.add_argument("--output", type=Path, default=Path("data/benchmark/gold.tsv") if name == "export-gold" else None)
    gate = sub.choices["gate"]
    gate.add_argument("--min-train", type=int, default=100)
    gate.add_argument("--min-dev", type=int, default=25)
    gate.add_argument("--min-test", type=int, default=25)
    assign = sub.add_parser("assign-splits", help="assign deterministic group-safe splits; preserves existing assignments")
    assign.add_argument("--records", type=Path, default=Path("data/benchmark/records.jsonl"))
    assign.add_argument("--splits", type=Path, default=Path("data/benchmark/splits.jsonl"))
    assign.add_argument("--seed", default="clippyfirst-ipa-gold-v1")
    assign.add_argument("--version", default="v1")
    assign.add_argument("--output", type=Path, default=Path("data/benchmark/splits.jsonl"))
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "assign-splits":
            return command_assign(args)
        data = validate_corpus(args)
        if args.command == "validate":
            report = data["summary"]
            rendered = json.dumps(report, ensure_ascii=False, indent=2)
            if args.report:
                args.report.parent.mkdir(parents=True, exist_ok=True)
                args.report.write_text(rendered + "\n", encoding="utf-8")
            print(rendered)
            return 0
        if args.command == "export-gold":
            return export_gold(args, data)
        if args.command == "gate":
            return release_gate(args, data)
        parser.error(f"unknown command: {args.command}")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
