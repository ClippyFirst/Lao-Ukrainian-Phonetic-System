#!/usr/bin/env python3
"""Aggregate-only development diagnostic on MekongPhon's pinned Lao train split.

This split is used to discover error patterns and improve the rule engine. It is
not a held-out test set, independent IPA gold, or a source of production labels.
No source words, reference strings, or per-item predictions are written out.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import statistics
import time
import unicodedata
import urllib.request
from collections import Counter
from pathlib import Path

DATA_URL = (
    "https://raw.githubusercontent.com/byu-matrix-lab/MekongPhon/"
    "f80f6c1840c4818b51e05f2e00cded4701a5b662/data/splits/lao_train.csv"
)
DATA_REVISION = "f80f6c1840c4818b51e05f2e00cded4701a5b662"
EXPECTED_ROWS = 6219
MEKONG_CONTOUR_TO_CATEGORY = {
    "˩˧": "low-rising",
    "˧˥": "high-rising",
    "˧": "high-mid",
    "˧˩": "low-falling",
    "˥˨": "high-falling",
}


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


def extract_tone_suffix(segmental: str, tonal: str) -> str | None:
    index = 0
    tones: list[str] = []
    for char in tonal:
        if index < len(segmental) and char == segmental[index]:
            index += 1
        else:
            tones.append(char)
    return "".join(tones) if index == len(segmental) else None


def parse_tone_categories(suffix: str) -> list[str] | None:
    if not suffix:
        return []
    contours = sorted(MEKONG_CONTOUR_TO_CATEGORY, key=len, reverse=True)
    categories: list[str] = []
    index = 0
    while index < len(suffix):
        contour = next((item for item in contours if suffix.startswith(item, index)), None)
        if contour is None:
            return None
        categories.append(MEKONG_CONTOUR_TO_CATEGORY[contour])
        index += len(contour)
    return categories


def load_dataset() -> tuple[list[dict[str, str]], str]:
    request = urllib.request.Request(DATA_URL, headers={"User-Agent": "ClippyFirst-research-diagnostic/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = response.read()
    digest = hashlib.sha256(payload).hexdigest()
    rows = list(csv.DictReader(payload.decode("utf-8-sig").splitlines()))
    required = {"orth", "pron_no_tones", "pron_with_tones"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("MekongPhon train split is empty or has an unexpected schema")
    if len(rows) != EXPECTED_ROWS:
        raise ValueError(f"Expected {EXPECTED_ROWS} train rows, received {len(rows)}")
    if any(not row["orth"].strip() or not row["pron_no_tones"].strip()
           or not row["pron_with_tones"].strip() for row in rows):
        raise ValueError("MekongPhon train split contains empty source or IPA fields")
    return rows, digest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("artifacts/mekongphon-train-diagnostics.json"))
    args = parser.parse_args()

    rows, dataset_sha = load_dataset()
    from lao_ukrainian.core import analyze

    status_counts: Counter[str] = Counter()
    warning_counts: Counter[str] = Counter()
    partial_shapes: Counter[str] = Counter()
    tone_contexts: Counter[str] = Counter()
    tone_mismatches: Counter[str] = Counter()
    segmental_predictions: list[str] = []
    segmental_references: list[str] = []
    segmental_durations: list[float] = []
    tone_reference_categories = 0
    tone_category_covered = 0
    tone_category_errors = 0
    tone_category_unresolved = 0
    tone_category_word_length_mismatches = 0
    tone_category_exact_words = 0
    tone_category_complete_words = 0
    tone_category_alignment_failures = 0
    runtime_errors: Counter[str] = Counter()

    for row in rows:
        source = nfc(row["orth"])
        reference_segmental = nfc(row["pron_no_tones"])
        reference_tonal = nfc(row["pron_with_tones"])
        suffix = extract_tone_suffix(reference_segmental, reference_tonal)
        reference_categories = parse_tone_categories(suffix) if suffix is not None else None
        if reference_categories is None:
            tone_category_alignment_failures += 1
            reference_categories = []

        started = time.perf_counter()
        try:
            result = analyze(source)
        except Exception as exc:  # aggregate only the exception class, never the input
            runtime_errors[type(exc).__name__] += 1
            segmental_predictions.append("")
            segmental_references.append(reference_segmental)
            segmental_durations.append(time.perf_counter() - started)
            tone_reference_categories += len(reference_categories)
            tone_category_unresolved += len(reference_categories)
            continue
        elapsed = time.perf_counter() - started
        segmental_durations.append(elapsed)
        status_counts[str(result.status)] += 1
        syllables = result.syllables
        complete = bool(syllables) and all(
            item.phonetic_result and item.phonetic_result.phonemic_ipa
            for item in syllables
        )
        predicted_segmental = (
            nfc("".join(item.phonetic_result.phonemic_ipa for item in syllables))
            if complete else ""
        )
        segmental_predictions.append(predicted_segmental)
        segmental_references.append(reference_segmental)

        for item in syllables:
            for warning in item.warnings:
                warning_counts[str(warning)] += 1
            if item.status != "OK":
                shape = "|".join([
                    f"status={item.status}",
                    f"onset={item.onset or ''}",
                    f"vowel={item.vowel or ''}",
                    f"coda={item.coda or ''}",
                    f"mark={item.tone_mark or 'none'}",
                ])
                partial_shapes[shape] += 1

        tone_reference_categories += len(reference_categories)
        if not reference_categories:
            continue
        predicted_categories = [
            item.phonetic_result.tone_category
            if item.phonetic_result and item.phonetic_result.tone_category
            else None
            for item in syllables
        ]
        if predicted_segmental != reference_segmental:
            tone_category_unresolved += len(reference_categories)
            continue
        if len(predicted_categories) != len(reference_categories):
            tone_category_word_length_mismatches += 1
            tone_category_unresolved += len(reference_categories)
            continue

        word_complete = True
        word_exact = True
        for index, (expected, actual, item) in enumerate(
            zip(reference_categories, predicted_categories, syllables)
        ):
            context = "|".join([
                f"class={item.consonant_class or ''}",
                f"type={item.syllable_type or ''}",
                f"vowel={item.vowel or ''}",
                f"coda={item.coda or ''}",
                f"mark={item.tone_mark or 'none'}",
                f"position={'initial' if index == 0 else 'final' if index == len(syllables)-1 else 'medial'}",
                f"rule={next((r for r in item.rules if str(r).startswith('VNT-')), '')}",
            ])
            tone_contexts[context] += 1
            if actual is None:
                tone_category_unresolved += 1
                word_complete = False
                word_exact = False
            else:
                tone_category_covered += 1
                if actual != expected:
                    tone_category_errors += 1
                    word_exact = False
                    tone_mismatches[context + f"|expected={expected}|actual={actual}"] += 1
        if word_complete:
            tone_category_complete_words += 1
            if word_exact:
                tone_category_exact_words += 1

    edits = sum(levenshtein(ref, pred) for ref, pred in zip(segmental_references, segmental_predictions))
    reference_chars = sum(len(ref) for ref in segmental_references)
    segmental_covered = sum(bool(pred) for pred in segmental_predictions)
    segmental_exact = sum(ref == pred for ref, pred in zip(segmental_references, segmental_predictions))
    total_tone_words = sum(1 for row in rows if row["pron_with_tones"])
    report = {
        "schema_version": "1.0",
        "status": "development_diagnostic_not_accuracy",
        "dataset": {
            "project": "BYU MATRIX Lab MekongPhon",
            "revision": DATA_REVISION,
            "url": DATA_URL,
            "split": "lao_train.csv",
            "rows": len(rows),
            "sha256": dataset_sha,
            "use": "rule-discovery and development diagnostics only; not held-out evaluation or independent gold",
            "redistribution": "No source rows, IPA references, or per-item predictions are retained in this report.",
        },
        "method": {
            "normalization": "Unicode NFC and outer whitespace trim only",
            "segmental_reference": "pron_no_tones; full train-split denominator; withheld outputs remain empty",
            "tone_reference": "pron_with_tones; tones parsed into the five explicitly documented MekongPhon contour categories",
            "tone_category_scoring": "only after exact segmental agreement; unknown/misaligned outputs count as unresolved, never guessed",
            "limitations": [
                "The train split is used for development and rule discovery, so these scores are not held-out generalization estimates.",
                "MekongPhon labels are an external reference derived from its published lexicon workflow, not ClippyFirst independent expert-adjudicated gold.",
                "MekongPhon and ClippyFirst tone conventions may differ; categorical comparisons are diagnostic and disagreements require linguistic review.",
            ],
        },
        "segmental": {
            "n": len(rows),
            "coverage": segmental_covered / len(rows),
            "exact_matches": segmental_exact,
            "exact_match_rate_full_denominator": segmental_exact / len(rows),
            "cer_full_denominator": edits / reference_chars if reference_chars else None,
            "reference_codepoints": reference_chars,
            "mean_latency_ms": round(statistics.mean(segmental_durations) * 1000, 3),
            "throughput_items_per_second": round(len(segmental_durations) / sum(segmental_durations), 3) if sum(segmental_durations) else None,
        },
        "tone_categories": {
            "reference_words_with_tonal_labels": total_tone_words,
            "reference_categories": tone_reference_categories,
            "covered_categories_on_segmental_exact_words": tone_category_covered,
            "coverage": tone_category_covered / tone_reference_categories if tone_reference_categories else 0.0,
            "category_error_rate_on_covered": tone_category_errors / tone_category_covered if tone_category_covered else None,
            "complete_words": tone_category_complete_words,
            "exact_complete_words": tone_category_exact_words,
            "unresolved_categories": tone_category_unresolved,
            "word_length_mismatches": tone_category_word_length_mismatches,
            "reference_alignment_failures": tone_category_alignment_failures,
        },
        "diagnostics": {
            "status_counts": dict(sorted(status_counts.items())),
            "warning_counts": dict(sorted(warning_counts.items())),
            "partial_parse_shapes": [
                {"context": key, "count": count} for key, count in partial_shapes.most_common(50)
            ],
            "tone_context_counts": [
                {"context": key, "count": count} for key, count in tone_contexts.most_common(100)
            ],
            "tone_mismatch_contexts": [
                {"context": key, "count": count} for key, count in tone_mismatches.most_common(100)
            ],
            "runtime_errors_by_exception_class": dict(sorted(runtime_errors.items())),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "dataset_sha256": dataset_sha,
        "rows": len(rows),
        "segmental": report["segmental"],
        "tone_categories": report["tone_categories"],
        "status_counts": report["diagnostics"]["status_counts"],
        "warning_counts": report["diagnostics"]["warning_counts"],
        "report": str(args.output),
    }, ensure_ascii=False, indent=2))
    return 1 if runtime_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
