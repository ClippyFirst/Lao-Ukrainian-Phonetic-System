#!/usr/bin/env python3
"""Run a text-domain stress benchmark on the independent HVULao_NLP 1k test set.

This corpus contains raw Lao sentences and word-segmentation annotations, not IPA.
The report therefore measures engine coverage, runtime, failures and pairwise
output disagreement only. It must never be presented as G2P accuracy.
Only aggregate metrics are written; sentence text and predictions are not retained.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import statistics
import time
import unicodedata
import urllib.request
from pathlib import Path

SOURCE_REPO = "HaHVU/HVULao_NLP"
SOURCE_REVISION = "ec8be4f1a541f3a5c76b4ebda39a9b2795d5c568"
SOURCE_PATH = "Datatest1k/testorgin1000.txt"
SOURCE_GIT_BLOB_SHA1 = "947448807484bb994877ae5d32cba1cfdd5e2d9b"
SOURCE_ROWS = 1000
MODEL_ID = "byumatrixlab/lao-ipa-nontonal"
MODEL_REVISION = "d6ea20cb73eaab8f3adc4eb044e61bdb9bef3f5b"
NUM_BEAMS = 5


def nfc(value: str) -> str:
    return unicodedata.normalize("NFC", value.strip())


def git_blob_sha1(payload: bytes) -> str:
    header = f"blob {len(payload)}\\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def load_dataset() -> tuple[list[str], str]:
    url = (
        f"https://raw.githubusercontent.com/{SOURCE_REPO}/"
        f"{SOURCE_REVISION}/{SOURCE_PATH}"
    )
    request = urllib.request.Request(url, headers={"User-Agent": "ClippyFirst-HVULao-1k-benchmark/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = response.read()
    digest = git_blob_sha1(payload)
    if digest != SOURCE_GIT_BLOB_SHA1:
        raise ValueError(f"Pinned HVULao_NLP Git blob changed: {digest}")
    lines = [nfc(line) for line in payload.decode("utf-8-sig").splitlines()]
    lines = [line for line in lines if line]
    if len(lines) != SOURCE_ROWS:
        raise ValueError(f"Expected {SOURCE_ROWS} non-empty sentences, got {len(lines)}")
    if any(not any("\\u0e80" <= ch <= "\\u0eff" for ch in line) for line in lines):
        raise ValueError("A test row contains no Lao-block character")
    return lines, digest


def compact_ipa(value: str) -> str:
    return nfc("".join(value.split()))


def complete_rule_ipa(analysis) -> str:
    syllables = analysis.syllables
    if not syllables or any(not item.phonemic_ipa for item in syllables):
        return ""
    return compact_ipa("".join(item.phonemic_ipa for item in syllables))


def levenshtein(a: str, b: str) -> int:
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        current = [i]
        for j, cb in enumerate(b, 1):
            current.append(min(
                current[-1] + 1,
                previous[j] + 1,
                previous[j - 1] + (ca != cb),
            ))
        previous = current
    return previous[-1]


def latency_summary(values: list[float]) -> dict:
    if not values:
        return {"mean_ms": None, "median_ms": None, "p95_ms": None, "total_s": None}
    ordered = sorted(values)
    p95 = ordered[min(len(ordered) - 1, int(0.95 * len(ordered)))]
    return {
        "mean_ms": statistics.mean(values) * 1000,
        "median_ms": statistics.median(values) * 1000,
        "p95_ms": p95 * 1000,
        "total_s": sum(values),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path,
        default=Path("artifacts/hvulao-1k-three-engine-stress.json"),
    )
    args = parser.parse_args()

    rows, blob_sha = load_dataset()
    from lao_ukrainian.core import analyze
    from lao_ukrainian.mekongphon import MekongPhonEngine

    neural = MekongPhonEngine(
        tonal=False, revision=MODEL_REVISION, device="cpu", num_beams=NUM_BEAMS
    )
    smoke = neural.transcribe("ຂາ")
    if smoke.model_id != MODEL_ID or smoke.model_revision != MODEL_REVISION:
        raise RuntimeError("MekongPhon smoke inference did not resolve the pinned model")

    stages = {
        "vientiane_rules": {"predictions": [], "times": [], "errors": Counter(), "withheld": Counter(), "syllables": Counter()},
        "mekongphon_reference_rules": {"predictions": [], "times": [], "errors": Counter(), "withheld": Counter(), "syllables": Counter()},
        "mekongphon_neural": {"predictions": [], "times": [], "errors": Counter()},
    }

    for source in rows:
        for key, profile in (
            ("vientiane_rules", None),
            ("mekongphon_reference_rules", "mekongphon-reference"),
        ):
            stage = stages[key]
            try:
                started = time.perf_counter()
                result = analyze(source) if profile is None else analyze(source, ipa_profile=profile)
                stage["times"].append(time.perf_counter() - started)
                stage["predictions"].append(complete_rule_ipa(result))
                stage["syllables"].update(item.status for item in result.syllables)
                if not stage["predictions"][-1]:
                    for item in result.syllables:
                        stage["withheld"].update(str(w).split(":", 1)[0] for w in item.warnings)
            except Exception as exc:
                stage["errors"][type(exc).__name__] += 1
                stage["predictions"].append("")

        stage = stages["mekongphon_neural"]
        try:
            started = time.perf_counter()
            prediction = neural.predict_raw_ipa(source)
            stage["times"].append(time.perf_counter() - started)
            stage["predictions"].append(compact_ipa(prediction))
        except Exception as exc:
            stage["errors"][type(exc).__name__] += 1
            stage["predictions"].append("")

    summaries = {}
    for key, stage in stages.items():
        predictions = stage["predictions"]
        summaries[key] = {
            "sentence_coverage": sum(bool(value) for value in predictions) / len(rows),
            "complete_outputs": sum(bool(value) for value in predictions),
            "withheld_or_failed": sum(not bool(value) for value in predictions),
            "runtime_errors_by_type": dict(sorted(stage["errors"].items())),
            "latency": latency_summary(stage["times"]),
        }
        if "syllables" in stage:
            summaries[key]["syllable_status_counts"] = dict(sorted(stage["syllables"].items()))
            summaries[key]["withheld_warning_categories"] = dict(sorted(stage["withheld"].items()))

    shared = [
        i for i in range(len(rows))
        if all(stages[key]["predictions"][i] for key in stages)
    ]
    pairwise = {}
    for left, right in (
        ("vientiane_rules", "mekongphon_reference_rules"),
        ("vientiane_rules", "mekongphon_neural"),
        ("mekongphon_reference_rules", "mekongphon_neural"),
    ):
        edits = sum(
            levenshtein(stages[left]["predictions"][i], stages[right]["predictions"][i])
            for i in shared
        )
        denominator = sum(len(stages[right]["predictions"][i]) for i in shared)
        pairwise[f"{left}_vs_{right}"] = {
            "n_shared_complete_sentences": len(shared),
            "disagreement_cer_against_right_output": edits / denominator if denominator else None,
            "edit_distance": edits,
            "right_output_codepoints": denominator,
        }

    report = {
        "schema_version": "1.0",
        "status": "independent_text_domain_stress_test_not_ipa_accuracy",
        "benchmark": {
            "name": "HVULao_NLP 1k raw-sentence test split",
            "repository": SOURCE_REPO,
            "revision": SOURCE_REVISION,
            "path": SOURCE_PATH,
            "rows": len(rows),
            "git_blob_sha1": blob_sha,
            "dataset_license": "CC-BY-4.0 (Mendeley Data version 2)",
            "input_kind": "raw Lao sentences; paired segmentation reference is not IPA",
            "limitations": [
                "No IPA reference is supplied; CER against a gold IPA transcription is not measurable.",
                "Pairwise output disagreement is not accuracy and cannot identify which engine is correct.",
                "This is a sentence-domain stress test, not a replacement for an adjudicated phonetic benchmark.",
            ],
        },
        "engines": {
            "vientiane_rules": {"implementation": "ClippyFirst deterministic default"},
            "mekongphon_reference_rules": {"implementation": "ClippyFirst deterministic opt-in profile"},
            "mekongphon_neural": {
                "model_id": MODEL_ID,
                "revision": MODEL_REVISION,
                "num_beams": NUM_BEAMS,
                "device": "cpu",
            },
        },
        "results": summaries,
        "pairwise_output_disagreement": pairwise,
        "all_three_complete_sentences": len(shared),
        "runtime_errors": sum(sum(stage["errors"].values()) for stage in stages.values()),
        "measurement_notes": [
            "One hosted CPU run; model load and initial smoke inference excluded from latency.",
            "Whitespace is removed only for pairwise IPA comparison; tone and length marks are retained.",
            "No source sentences or per-sentence IPA predictions are persisted.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["runtime_errors"]:
        raise RuntimeError(f"Runtime errors: {report['runtime_errors']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
