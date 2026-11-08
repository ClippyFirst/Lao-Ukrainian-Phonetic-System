#!/usr/bin/env python3
"""Independent Lao sentence-domain stress benchmark; not an IPA accuracy test."""
from __future__ import annotations

import argparse
import base64
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
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def load_dataset() -> tuple[list[str], str, int]:
    url = f"https://api.github.com/repos/{SOURCE_REPO}/git/blobs/{SOURCE_GIT_BLOB_SHA1}"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "ClippyFirst-HVULao-1k-benchmark/1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        blob = json.loads(response.read().decode("utf-8"))
    if blob.get("sha") != SOURCE_GIT_BLOB_SHA1 or blob.get("encoding") != "base64":
        raise ValueError("GitHub did not return the expected pinned HVULao_NLP blob")
    payload = base64.b64decode(blob["content"], validate=False)
    digest = git_blob_sha1(payload)
    if digest != SOURCE_GIT_BLOB_SHA1:
        raise ValueError(f"Pinned HVULao_NLP Git blob changed: {digest}")
    lines = [nfc(line) for line in payload.decode("utf-8-sig").splitlines()]
    lines = [line for line in lines if line]
    if len(lines) != SOURCE_ROWS:
        raise ValueError(f"Expected {SOURCE_ROWS} non-empty rows, got {len(lines)}")
    lao_rows = sum(
        any("\u0e80" <= ch <= "\u0eff" for ch in line) for line in lines
    )
    if lao_rows == 0:
        raise ValueError("Pinned corpus contains no Lao-block characters")
    # Preserve all source rows: punctuation/Latin-only fragments are part of the
    # supplied text split and must not be silently discarded or rewritten.
    return lines, digest, SOURCE_ROWS - lao_rows


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


def classify_input_rejection(exc: ValueError) -> str | None:
    message = str(exc)
    if message.startswith("Input is ") and "code points; model limit is" in message:
        return "source_codepoint_limit"
    if "Tokenized input exceeds the model" in message:
        return "tokenized_sequence_limit"
    if message.startswith("Input contains unsupported characters:"):
        return "unsupported_characters"
    if message == "Lao input must be a non-empty string":
        return "empty_input"
    return None


def latency_summary(values: list[float]) -> dict:
    if not values:
        return {"mean_ms": None, "median_ms": None, "p95_ms": None, "total_s": None}
    ordered = sorted(values)
    p95 = ordered[min(len(ordered) - 1, int(0.95 * len(ordered)))]
    return {
        "n": len(values),
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

    rows, blob_sha, rows_without_lao = load_dataset()
    from lao_ukrainian.core import analyze
    from lao_ukrainian.mekongphon import MekongPhonEngine

    neural = MekongPhonEngine(
        tonal=False, revision=MODEL_REVISION, device="cpu", num_beams=NUM_BEAMS
    )
    smoke = neural.transcribe("ຂາ")
    if smoke.model_id != MODEL_ID or smoke.model_revision != MODEL_REVISION:
        raise RuntimeError("MekongPhon smoke inference did not resolve the pinned model")

    stages = {
        "vientiane_rules": {
            "predictions": [], "times": [], "attempt_times": [], "errors": Counter(),
            "withheld": Counter(), "syllables": Counter(),
            "syllable_total": 0, "syllable_with_ipa": 0,
        },
        "mekongphon_reference_rules": {
            "predictions": [], "times": [], "errors": Counter(),
            "withheld": Counter(), "syllables": Counter(),
            "syllable_total": 0, "syllable_with_ipa": 0,
        },
        "mekongphon_neural": {
            "predictions": [], "times": [], "attempt_times": [], "errors": Counter(),
            "input_rejections": Counter(),
        },
    }

    for source in rows:
        for key, profile in (
            ("vientiane_rules", None),
            ("mekongphon_reference_rules", "mekongphon-reference"),
        ):
            stage = stages[key]
            try:
                started = time.perf_counter()
                result = analyze(source) if profile is None else analyze(
                    source, ipa_profile=profile
                )
                stage["times"].append(time.perf_counter() - started)
                prediction = complete_rule_ipa(result)
                stage["predictions"].append(prediction)
                stage["syllables"].update(item.status for item in result.syllables)
                stage["syllable_total"] += len(result.syllables)
                stage["syllable_with_ipa"] += sum(bool(item.phonemic_ipa) for item in result.syllables)
                if not prediction:
                    for item in result.syllables:
                        stage["withheld"].update(
                            str(w).split(":", 1)[0] for w in item.warnings
                        )
            except Exception as exc:
                stage["errors"][type(exc).__name__] += 1
                stage["predictions"].append("")
            finally:
                stage["attempt_times"].append(time.perf_counter() - started)

        stage = stages["mekongphon_neural"]
        try:
            started = time.perf_counter()
            prediction = neural.predict_raw_ipa(source)
            stage["times"].append(time.perf_counter() - started)
            stage["predictions"].append(compact_ipa(prediction))
        except ValueError as exc:
            rejection = classify_input_rejection(exc)
            if rejection:
                stage["input_rejections"][rejection] += 1
            else:
                stage["errors"][type(exc).__name__] += 1
            stage["predictions"].append("")
        except Exception as exc:
            stage["errors"][type(exc).__name__] += 1
            stage["predictions"].append("")
        finally:
            stage["attempt_times"].append(time.perf_counter() - started)

    summaries = {}
    for key, stage in stages.items():
        predictions = stage["predictions"]
        summaries[key] = {
            "sentence_coverage": sum(bool(value) for value in predictions) / len(rows),
            "complete_outputs": sum(bool(value) for value in predictions),
            "withheld_or_failed": sum(not bool(value) for value in predictions),
            "runtime_errors_by_type": dict(sorted(stage["errors"].items())),
            "successful_inference_latency": latency_summary(stage["times"]),
            "all_attempt_latency": latency_summary(stage["attempt_times"]),
        }
        if "input_rejections" in stage:
            summaries[key]["input_rejections_by_reason"] = dict(sorted(stage["input_rejections"].items()))
        if "syllables" in stage:
            summaries[key]["syllable_count"] = stage["syllable_total"]
            summaries[key]["syllables_with_ipa"] = stage["syllable_with_ipa"]
            summaries[key]["syllable_ipa_coverage"] = (
                stage["syllable_with_ipa"] / stage["syllable_total"]
                if stage["syllable_total"] else None
            )
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
        "schema_version": "1.1",
        "status": "independent_text_domain_stress_test_not_ipa_accuracy",
        "benchmark": {
            "name": "HVULao_NLP 1k raw-sentence test split",
            "repository": SOURCE_REPO,
            "revision": SOURCE_REVISION,
            "path": SOURCE_PATH,
            "rows": len(rows),
            "rows_without_lao_block_characters": rows_without_lao,
            "git_blob_sha1": blob_sha,
            "dataset_license": "CC-BY-4.0 (Mendeley Data version 2)",
            "input_kind": "raw Lao sentences; paired segmentation reference is not IPA",
            "limitations": [
                "No IPA reference is supplied; gold IPA CER is not measurable.",
                "Pairwise output disagreement is not accuracy and cannot identify the correct engine.",
                "This is a sentence-domain stress test, not an adjudicated phonetic benchmark.",
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
            "One hosted CPU run; model load and initial smoke inference excluded from both latency measures.",
            "successful_inference_latency covers only completed inference calls; all_attempt_latency covers all 1,000 calls including explicit input rejections and unexpected errors.",
            "Whitespace is removed for pairwise IPA comparison; tone and length marks are retained.",
            "No source sentences or per-sentence IPA predictions are persisted.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["runtime_errors"]:
        raise RuntimeError(f"Runtime errors: {report['runtime_errors']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
