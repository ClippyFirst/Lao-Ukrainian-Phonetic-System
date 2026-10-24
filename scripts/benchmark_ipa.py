#!/usr/bin/env python3
"""Evidence-gated IPA benchmark for ClippyFirst language adapters.

Gold TSV columns: id, text, gold_ipa, gold_status, profile, source_id
Prediction TSV columns: id, engine, raw_output, ipa, status, version
Only rows with gold_status=ADJUDICATED and a non-empty gold_ipa count as gold.
This reports strict Unicode NFC exact match and code-point CER; it does not claim
phonetic feature equivalence. No adjudicated rows means accuracy is NOT_MEASURED.
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
    pred_keys = set()
    by_engine = defaultdict(list)
    unknown_ids = []
    for row in pred_rows:
        key = (row["engine"], row["id"])
        if not row["engine"] or not row["id"] or key in pred_keys:
            raise ValueError(f"prediction (engine,id) must be non-empty and unique: {key!r}")
        pred_keys.add(key)
        if row["id"] not in gold:
            unknown_ids.append({"engine": row["engine"], "id": row["id"]})
            continue
        g = gold[row["id"]]
        if g["gold_status"] != "ADJUDICATED" or not norm(g["gold_ipa"]):
            continue
        p = norm(row["ipa"])
        ref = norm(g["gold_ipa"])
        by_engine[row["engine"]].append({
            "id": row["id"], "profile": g["profile"],
            "exact_match": bool(p) and p == ref,
            "missing_prediction": not bool(p),
            "edit_distance": distance(ref, p) if p else len(ref),
            "reference_codepoints": len(ref),
            "raw_output_present": bool(row["raw_output"]),
            "status": row["status"], "version": row["version"],
        })
    eligible = sum(1 for g in gold.values() if g["gold_status"] == "ADJUDICATED" and norm(g["gold_ipa"]))
    report = {
        "schema_version": "1.0",
        "method": {
            "gold_gate": "gold_status == ADJUDICATED and non-empty gold_ipa",
            "normalization": "Unicode NFC plus outer whitespace trim only",
            "exact_match": "strict full-string IPA match; tone, length and syllable separators remain significant",
            "cer": "Levenshtein over Unicode code points; not articulatory/feature-weighted",
            "accuracy_claim": "none; scores are descriptive for the supplied adjudicated rows only",
        },
        "gold": {"rows_total": len(gold), "rows_adjudicated": eligible,
                 "accuracy_status": "MEASURED_ON_ADJUDICATED_SUBSET" if eligible else "NOT_MEASURED"},
        "unknown_prediction_ids": unknown_ids,
        "engines": {},
    }
    engines = sorted({r["engine"] for r in pred_rows})
    for engine in engines:
        rows = by_engine.get(engine, [])
        n = len(rows)
        edits = sum(r["edit_distance"] for r in rows)
        chars = sum(r["reference_codepoints"] for r in rows)
        report["engines"][engine] = {
            "n_adjudicated_predictions": n,
            "exact_matches": sum(r["exact_match"] for r in rows),
            "exact_match_rate": sum(r["exact_match"] for r in rows) / n if n else None,
            "missing_predictions": sum(r["missing_prediction"] for r in rows),
            "codepoint_cer": edits / chars if chars else None,
            "profiles": sorted({r["profile"] for r in rows if r["profile"]}),
            "versions": sorted({r["version"] for r in pred_rows if r["engine"] == engine and r["version"]}),
            "rows": rows,
            "status": "SCORED" if n else "NOT_MEASURED_NO_ADJUDICATED_OVERLAP",
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "gold_adjudicated": eligible,
                      "engines": {k: {"n": v["n_adjudicated_predictions"], "status": v["status"]}
                                  for k, v in report["engines"].items()}}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
