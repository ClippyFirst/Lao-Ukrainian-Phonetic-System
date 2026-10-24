#!/usr/bin/env python3
"""Evidence-gated IPA benchmark; standard library only.

Gold TSV: id, text, gold_ipa, gold_status, profile, source_id
Prediction TSV: id, engine, raw_output, ipa, status, version
Only ADJUDICATED, non-empty gold IPA rows enter the denominator.
"""
from __future__ import annotations
import argparse, csv, json, unicodedata
from collections import defaultdict
from pathlib import Path

GOLD_FIELDS = ["id", "text", "gold_ipa", "gold_status", "profile", "source_id"]
PRED_FIELDS = ["id", "engine", "raw_output", "ipa", "status", "version"]

def read_tsv(path: Path, required: list[str]) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        missing = set(required) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path}: missing columns: {', '.join(sorted(missing))}")
        rows = list(reader)
    return [{k: (v or "") for k, v in row.items()} for row in rows]

def norm(s: str) -> str:
    return unicodedata.normalize("NFC", s.strip())

def distance(a: str, b: str) -> int:
    # Levenshtein distance over Unicode code points, not IPA feature classes.
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(cur[-1] + 1, prev[j] + 1, prev[j-1] + (ca != cb)))
        prev = cur
    return prev[-1]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", type=Path, required=True)
    ap.add_argument("--predictions", type=Path, required=True)
    ap.add_argument("--output", type=Path, default=Path("benchmark-report.json"))
    args = ap.parse_args()
    gold_rows = read_tsv(args.gold, GOLD_FIELDS)
    pred_rows = read_tsv(args.predictions, PRED_FIELDS)
    gold = {}
    for row in gold_rows:
        if not row["id"] or row["id"] in gold:
            raise ValueError(f"gold IDs must be non-empty and unique: {row['id']!r}")
        gold[row["id"]] = row
    # An ADJUDICATED label must be auditable. Fail closed instead of silently
    # excluding malformed gold rows and accidentally changing the denominator.
    for row in gold_rows:
        if row["gold_status"] == "ADJUDICATED":
            if not norm(row["gold_ipa"]):
                raise ValueError(f"ADJUDICATED gold row {row['id']!r} requires non-empty gold_ipa")
            if not row["source_id"].strip():
                raise ValueError(f"ADJUDICATED gold row {row['id']!r} requires source_id")
            if not row["profile"].strip():
                raise ValueError(f"ADJUDICATED gold row {row['id']!r} requires profile")
    eligible = {k: v for k, v in gold.items()
                if v["gold_status"] == "ADJUDICATED" and norm(v["gold_ipa"])}
    predictions = defaultdict(dict)
    unknown_ids = []
    for row in pred_rows:
        if not row["engine"] or not row["id"]:
            raise ValueError("prediction engine and id must be non-empty")
        engine = row["engine"]
        if row["id"] in predictions[engine]:
            raise ValueError(f"prediction (engine,id) must be unique: {(engine, row['id'])!r}")
        predictions[engine][row["id"]] = row
        if row["id"] not in gold:
            unknown_ids.append({"engine": engine, "id": row["id"]})
    report = {
        "schema_version": "1.0",
        "method": {
            "gold_gate": "gold_status == ADJUDICATED and non-empty gold_ipa",
            "normalization": "Unicode NFC plus outer whitespace trim only",
            "exact_match": "strict full-string IPA match; tone, length and syllable separators remain significant",
            "cer": "Levenshtein over Unicode code points; not articulatory/feature-weighted",
            "missing_predictions": "every eligible gold row is in each engine's denominator; absent/empty IPA counts as a missing prediction and incurs reference-length edit cost",
            "accuracy_claim": "descriptive only for the supplied adjudicated rows; no generalization claim",
        },
        "gold": {"rows_total": len(gold), "rows_adjudicated": len(eligible),
                 "accuracy_status": "MEASURED_ON_ADJUDICATED_SUBSET" if eligible else "NOT_MEASURED"},
        "unknown_prediction_ids": unknown_ids,
        "engines": {},
    }
    for engine in sorted(predictions):
        rows = []
        for ident, g in eligible.items():
            pred = predictions[engine].get(ident)
            ref = norm(g["gold_ipa"])
            p = norm(pred["ipa"]) if pred else ""
            rows.append({
                "id": ident, "profile": g["profile"],
                "exact_match": bool(p) and p == ref,
                "missing_prediction": not bool(p),
                "prediction_row_present": pred is not None,
                "edit_distance": distance(ref, p) if p else len(ref),
                "reference_codepoints": len(ref),
                "raw_output_present": bool(pred and pred["raw_output"]),
                "status": pred["status"] if pred else "MISSING_ROW",
                "version": pred["version"] if pred else "",
            })
        n = len(rows)
        edits = sum(r["edit_distance"] for r in rows)
        chars = sum(r["reference_codepoints"] for r in rows)
        report["engines"][engine] = {
            "n_adjudicated_gold_rows": n,
            "exact_matches": sum(r["exact_match"] for r in rows),
            "exact_match_rate": sum(r["exact_match"] for r in rows) / n if n else None,
            "missing_predictions": sum(r["missing_prediction"] for r in rows),
            "missing_prediction_rate": sum(r["missing_prediction"] for r in rows) / n if n else None,
            "codepoint_cer": edits / chars if chars else None,
            "profiles": sorted({r["profile"] for r in rows if r["profile"]}),
            "versions": sorted({r["version"] for r in predictions[engine].values() if r["version"]}),
            "rows": rows,
            "status": "SCORED" if n else "NOT_MEASURED_NO_ADJUDICATED_GOLD",
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "gold_adjudicated": len(eligible),
                      "engines": {k: {"n": v["n_adjudicated_gold_rows"], "status": v["status"],
                                      "missing": v["missing_predictions"]}
                                  for k, v in report["engines"].items()}}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
