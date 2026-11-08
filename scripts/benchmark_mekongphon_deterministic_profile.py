#!/usr/bin/env python3
"""Evaluate the deterministic MekongPhon-reference IPA profile on the frozen holdout.

The 6,219-row MekongPhon train split informed the profile. This script evaluates
it only on the separate 100-row held-out split and reports aggregates only.
No source words, references, or per-item predictions are persisted.
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter
import hashlib
import json
import statistics
import time
import unicodedata
import urllib.request
from pathlib import Path

DATA_URL = (
    "https://raw.githubusercontent.com/byu-matrix-lab/MekongPhon/"
    "f80f6c1840c4818b51e05f2e00cded4701a5b662/data/splits/lao_eval.csv"
)
DATA_SHA256 = "5351af5ed545f68886a99f0e8d88c91fdbdf46c4df885d40e166b8a3b32cd241"
MODEL_ID = "byumatrixlab/lao-ipa-nontonal"
MODEL_REVISION = "d6ea20cb73eaab8f3adc4eb044e61bdb9bef3f5b"
NUM_BEAMS = 5


def nfc(value: str) -> str:
    return unicodedata.normalize("NFC", value.strip())


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


def load_dataset():
    request = urllib.request.Request(
        DATA_URL, headers={"User-Agent": "ClippyFirst-deterministic-profile-benchmark/1.0"}
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = response.read()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != DATA_SHA256:
        raise ValueError(f"Pinned MekongPhon holdout SHA-256 changed: {digest}")
    rows = list(csv.DictReader(payload.decode("utf-8-sig").splitlines()))
    required = {"orth", "pron_no_tones"}
    if len(rows) != 100 or not required.issubset(rows[0]):
        raise ValueError("Expected the pinned 100-row MekongPhon holdout schema")
    if any(not row["orth"].strip() or not row["pron_no_tones"].strip() for row in rows):
        raise ValueError("Holdout contains an empty orthography or IPA reference")
    return rows, digest


def complete_ipa(analysis) -> str:
    syllables = analysis.syllables
    if not syllables or any(not item.phonemic_ipa for item in syllables):
        return ""
    return nfc("".join(item.phonemic_ipa for item in syllables))


def remove_optional_ipa_tie_bars(value: str) -> str:
    return nfc(value.replace("\u0361", "").replace("\u035c", ""))


def warning_code(value: str) -> str:
    return value.split(":", 1)[0]


def score(references, predictions):
    edits = sum(levenshtein(ref, pred) for ref, pred in zip(references, predictions))
    denominator = sum(len(ref) for ref in references)
    covered = [(ref, pred) for ref, pred in zip(references, predictions) if pred]
    return {
        "coverage": len(covered) / len(references) if references else None,
        "exact_matches": sum(ref == pred for ref, pred in zip(references, predictions)),
        "tie_bar_normalized_exact_matches": sum(
            remove_optional_ipa_tie_bars(ref) == remove_optional_ipa_tie_bars(pred)
            for ref, pred in zip(references, predictions)
        ),
        "cer_full_denominator": edits / denominator if denominator else None,
        "reference_codepoints": denominator,
        "edit_distance": edits,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path,
        default=Path("artifacts/mekongphon-deterministic-rule-profile.json"),
    )
    args = parser.parse_args()

    rows, dataset_sha = load_dataset()
    from lao_ukrainian.core import analyze
    from lao_ukrainian.mekongphon import MekongPhonEngine

    neural = MekongPhonEngine(
        tonal=False, revision=MODEL_REVISION, device="cpu", num_beams=NUM_BEAMS
    )
    smoke = neural.transcribe("ຂາ")
    if smoke.model_id != MODEL_ID or smoke.model_revision != MODEL_REVISION:
        raise RuntimeError("MekongPhon smoke inference did not resolve the pinned model")

    references = []
    baseline_predictions = []
    profile_predictions = []
    hybrid_predictions = []
    neural_predictions = []
    baseline_times = []
    profile_times = []
    hybrid_times = []
    neural_times = []
    baseline_warning_counts = Counter()
    profile_warning_counts = Counter()
    profile_status_counts = Counter()
    hybrid_warning_counts = Counter()
    hybrid_status_counts = Counter()
    runtime_errors_by_stage = Counter()

    for row in rows:
        source = nfc(row["orth"])
        references.append(nfc(row["pron_no_tones"]))
        baseline_prediction = ""
        profile_prediction = ""
        hybrid_prediction = ""
        neural_prediction = ""

        try:
            started = time.perf_counter()
            baseline = analyze(source)
            baseline_times.append(time.perf_counter() - started)
            baseline_prediction = complete_ipa(baseline)
            if not baseline_prediction:
                for item in baseline.syllables:
                    baseline_warning_counts.update(warning_code(str(w)) for w in item.warnings)
        except Exception as exc:
            runtime_errors_by_stage["baseline:" + type(exc).__name__] += 1

        try:
            started = time.perf_counter()
            compatible = analyze(source, ipa_profile="mekongphon-reference")
            profile_times.append(time.perf_counter() - started)
            profile_prediction = complete_ipa(compatible)
            profile_status_counts.update(item.status for item in compatible.syllables)
            if not profile_prediction:
                for item in compatible.syllables:
                    profile_warning_counts.update(warning_code(str(w)) for w in item.warnings)
        except Exception as exc:
            runtime_errors_by_stage["profile:" + type(exc).__name__] += 1

        try:
            started = time.perf_counter()
            hybrid = analyze(source, ipa_profile="hybrid-deterministic")
            hybrid_times.append(time.perf_counter() - started)
            hybrid_prediction = complete_ipa(hybrid)
            hybrid_status_counts.update(item.status for item in hybrid.syllables)
            if not hybrid_prediction:
                for item in hybrid.syllables:
                    hybrid_warning_counts.update(warning_code(str(w)) for w in item.warnings)
        except Exception as exc:
            runtime_errors_by_stage["hybrid:" + type(exc).__name__] += 1

        try:
            started = time.perf_counter()
            neural_prediction = nfc(neural.predict_raw_ipa(source))
            neural_times.append(time.perf_counter() - started)
        except Exception as exc:
            runtime_errors_by_stage["neural:" + type(exc).__name__] += 1

        baseline_predictions.append(baseline_prediction)
        profile_predictions.append(profile_prediction)
        hybrid_predictions.append(hybrid_prediction)
        neural_predictions.append(neural_prediction)

    baseline_score = score(references, baseline_predictions)
    profile_score = score(references, profile_predictions)
    neural_score = score(references, neural_predictions)
    shared = [
        i for i, values in enumerate(zip(
            baseline_predictions, profile_predictions, hybrid_predictions, neural_predictions
        ))
        if all(values)
    ]
    shared_refs = [references[i] for i in shared]
    shared_scores = {
        "n": len(shared),
        "baseline_rules": score(shared_refs, [baseline_predictions[i] for i in shared]),
        "mekongphon_reference_rules": score(shared_refs, [profile_predictions[i] for i in shared]),
        "hybrid_deterministic_rules": score(shared_refs, [hybrid_predictions[i] for i in shared]),
        "mekongphon_neural": score(shared_refs, [neural_predictions[i] for i in shared]),
    }
    profile_vs_neural = [
        (profile_predictions[i], neural_predictions[i]) for i in shared
    ]
    pair_edits = sum(levenshtein(a, b) for a, b in profile_vs_neural)
    pair_denominator = sum(len(b) for _, b in profile_vs_neural)

    report = {
        "schema_version": "1.0",
        "status": "heldout_comparison_not_independent_accuracy",
        "dataset": {
            "repository": "BYU MATRIX Lab MekongPhon",
            "revision": "f80f6c1840c4818b51e05f2e00cded4701a5b662",
            "split": "lao_eval.csv",
            "rows": len(rows),
            "sha256": dataset_sha,
            "reference": "pron_no_tones",
            "redistribution": "Aggregate metrics only; no source rows or predictions retained.",
        },
        "neural_comparator": {
            "model_id": MODEL_ID,
            "revision": MODEL_REVISION,
            "num_beams": NUM_BEAMS,
            "device": "cpu",
        },
        "deterministic_profile": {
            "name": "mekongphon-reference",
            "training_basis": "Aggregate contextual correspondences from the separate pinned 6,219-row train split only",
            "purpose": "Reference-convention compatibility experiment; not a universal Vientiane phonology claim",
        },
        "scores_full_100": {
            "baseline_vientiane_rules": baseline_score,
            "mekongphon_reference_rules": profile_score,
            "hybrid_deterministic_rules": score(references, hybrid_predictions),
            "mekongphon_neural": neural_score,
        },
        "scores_identical_coverage": shared_scores,
        "profile_vs_neural_shared_coverage": {
            "n": len(shared),
            "cer_against_neural_output": (
                pair_edits / pair_denominator if pair_denominator else None
            ),
        },
        "latency_ms_per_input": {
            "baseline_rules_mean": (
                statistics.mean(baseline_times) * 1000 if baseline_times else None
            ),
            "mekongphon_reference_rules_mean": (
                statistics.mean(profile_times) * 1000 if profile_times else None
            ),
            "hybrid_deterministic_rules_mean": (
                statistics.mean(hybrid_times) * 1000 if hybrid_times else None
            ),
            "neural_model_inference_mean": (
                statistics.mean(neural_times) * 1000 if neural_times else None
            ),
            "note": "Each stage is timed independently; model load and initial smoke inference are excluded.",
        },
        "coverage_diagnostics": {
            "baseline_withheld_warning_codes": dict(sorted(baseline_warning_counts.items())),
            "profile_withheld_warning_codes": dict(sorted(profile_warning_counts.items())),
            "profile_syllable_status_counts": dict(sorted(profile_status_counts.items())),
            "hybrid_withheld_warning_codes": dict(sorted(hybrid_warning_counts.items())),
            "hybrid_syllable_status_counts": dict(sorted(hybrid_status_counts.items())),
        },
        "runtime_errors_by_stage": dict(sorted(runtime_errors_by_stage.items())),
        "runtime_errors": sum(runtime_errors_by_stage.values()),
        "limitations": [
            "The 100-word holdout is dictionary-seeded and is not independently adjudicated project gold.",
            "The profile is derived from the separate MekongPhon train split; it is an explicit compatibility experiment, not a universal phonetic standard.",
            "No rule is tuned from this held-out split; the default Vientiane profile is unchanged.",
            "The hybrid currently uses the same evidenced mappings with deterministic rule selection; this tests implementation parity, not new linguistic evidence.",
            "The comparison scores IPA only and does not score Ukrainian target adaptation.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if runtime_errors_by_stage:
        raise RuntimeError(f"Benchmark runtime errors by stage: {dict(runtime_errors_by_stage)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
