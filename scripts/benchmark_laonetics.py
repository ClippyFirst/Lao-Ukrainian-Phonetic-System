#!/usr/bin/env python3
"""Aggregate-only Laonetics comparison on the pinned MekongPhon 100-word split.

Research probe only: Laonetics is CC-BY-NC-4.0 and is not imported into
production. No input rows or per-item predictions are written to disk.
"""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import unicodedata
import urllib.request
from pathlib import Path

DATA_URL = (
    "https://raw.githubusercontent.com/byu-matrix-lab/MekongPhon/"
    "f80f6c1840c4818b51e05f2e00cded4701a5b662/data/splits/lao_eval.csv"
)
DATA_SHA256 = "5351af5ed545f68886a99f0e8d88c91fdbdf46c4df885d40e166b8a3b32cd241"
NODE_RUNNER = r"""
const fs = require("fs");
const pkg = require("laonetics");
const Translator = pkg.LaoneticsTranslater || (pkg.default && pkg.default.LaoneticsTranslater);
if (typeof Translator !== "function") throw new Error("LaoneticsTranslater export unavailable");
const translator = new Translator();
const inputs = JSON.parse(fs.readFileSync(0, "utf8"));
const outputs = inputs.map((word) => {
  const result = translator.getKaraoke(word, ["ph"]);
  return result && result.roms && result.roms[0]
    ? result.roms[0].join("")
    : "";
});
process.stdout.write(JSON.stringify(outputs));
"""


def norm(value: str) -> str:
    return unicodedata.normalize("NFC", value.strip())


def levenshtein(left: str, right: str) -> int:
    previous = list(range(len(right) + 1))
    for i, a in enumerate(left, 1):
        current = [i]
        for j, b in enumerate(right, 1):
            current.append(min(current[-1] + 1, previous[j] + 1,
                               previous[j - 1] + (a != b)))
        previous = current
    return previous[-1]


def main() -> int:
    request = urllib.request.Request(
        DATA_URL, headers={"User-Agent": "ClippyFirst-Laonetics-benchmark/1.0"}
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = response.read()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != DATA_SHA256:
        raise RuntimeError(f"Pinned evaluation SHA-256 mismatch: {digest}")
    rows = list(csv.DictReader(payload.decode("utf-8-sig").splitlines()))
    if len(rows) != 100 or any(not r.get("orth") or not r.get("pron_no_tones") for r in rows):
        raise RuntimeError("Expected 100 non-empty rows in pinned MekongPhon holdout")

    words = [norm(r["orth"]) for r in rows]
    refs = [norm(r["pron_no_tones"]) for r in rows]
    run = subprocess.run(
        ["node", "-e", NODE_RUNNER], input=json.dumps(words, ensure_ascii=False),
        text=True, capture_output=True, check=True, timeout=120,
    )
    predictions = json.loads(run.stdout)
    if len(predictions) != len(refs):
        raise RuntimeError("Laonetics output row count mismatch")
    predictions = [norm(p) for p in predictions]
    edits = sum(levenshtein(ref, pred) for ref, pred in zip(refs, predictions))
    denominator = sum(len(ref) for ref in refs)
    covered = sum(bool(pred) for pred in predictions)
    exact = sum(ref == pred for ref, pred in zip(refs, predictions))

    report = {
        "schema_version": "1.0",
        "benchmark": "MekongPhon pinned 100-word held-out lexicon; segmental-only",
        "accuracy_claim": None,
        "independent_expert_gold_count": 0,
        "engine": {
            "name": "Laonetics",
            "version": "0.4.3",
            "upstream": "https://github.com/ltruchot/laonetics",
            "upstream_commit": "eeab0c4ead4c1f67599573eb9e5cba56506260e3",
            "license": "CC-BY-NC-4.0",
            "mode": "ph (IPA-like phonetic rendering)",
        },
        "provenance": {
            "dataset_url": DATA_URL,
            "dataset_revision": "f80f6c1840c4818b51e05f2e00cded4701a5b662",
            "dataset_sha256": digest,
            "rows": len(rows),
            "reference": "pron_no_tones",
            "normalization": "Unicode NFC; trim outer whitespace only",
        },
        "segmental": {
            "n": len(refs),
            "exact": exact,
            "exact_rate": exact / len(refs),
            "cer_full_denominator": edits / denominator if denominator else None,
            "output_coverage": covered / len(refs),
            "missing": len(refs) - covered,
            "reference_codepoints": denominator,
            "edit_distance": edits,
        },
        "tonal": None,
        "interpretation": (
            "Reference concordance only, not independent accuracy. Laonetics "
            "is an older rule-based karaoke/romanization library; its ph lane "
            "emits IPA-like segmental forms without a scored tone lane. "
            "The result is research-only and the CC-BY-NC-4.0 package is not "
            "eligible for production redistribution or commercial use."
        ),
    }
    out = Path("artifacts/laonetics-mekongphon-100.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
