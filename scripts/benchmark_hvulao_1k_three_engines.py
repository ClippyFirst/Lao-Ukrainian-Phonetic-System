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

try:
    from scripts.benchmark_ipa_contract import accepted_phonetic_ipa
except ModuleNotFoundError:
    from benchmark_ipa_contract import accepted_phonetic_ipa

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
    # Non-Lao ASCII/punctuation units are preserved as passthrough.
    # PROVISIONAL grapheme hints count for rendering, never as IPA accuracy.
    syllables = [item for item in analysis.syllables if item.status != "PASSTHROUGH"]
    if not syllables or any(not accepted_phonetic_ipa(item.phonetic_result) for item in syllables):
        return ""
    return compact_ipa("".join(item.phonetic_result.phonemic_ipa for item in syllables))


def complete_rule_rendering(analysis) -> str:
    """Return a rendering only when every analyzed source unit has a target."""
    if not analysis.syllables or any(item.practical_ukrainian is None for item in analysis.syllables):
        return ""
    return "".join(item.practical_ukrainian for item in analysis.syllables)


def withheld_ipa_diagnostics(items) -> tuple[Counter, Counter]:
    """Aggregate why syllables lack accepted IPA without retaining source text."""
    statuses = Counter()
    reasons = Counter()
    for item in items:
        if item.status == "PASSTHROUGH" or accepted_phonetic_ipa(item.phonetic_result):
            continue
        result = item.phonetic_result
        statuses[getattr(result, "status", None) or "MISSING_RESULT"] += 1
        warnings = tuple(item.warnings or ()) + tuple(
            getattr(result, "uncertainty", ()) if result is not None else ()
        )
        if not warnings:
            reasons["NO_STRUCTURED_REASON"] += 1
        for warning in warnings:
            reasons[str(warning).split(":", 1)[0]] += 1
    return statuses, reasons


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


def new_rule_stage() -> dict:
    """Create independent counters for one deterministic IPA profile."""
    return {
        "predictions": [], "rendered_predictions": [], "times": [], "attempt_times": [], "errors": Counter(),
        "withheld": Counter(), "withheld_statuses": Counter(), "syllables": Counter(),
        "syllable_total": 0, "syllable_with_ipa": 0, "passthrough_total": 0,
        "unit_total": 0, "units_rendered": 0, "supported_ipa_units": 0,
        "uncertain_ipa_units": 0, "provisional_units": 0,
        "target_unmapped_units": 0,
        "analysis_statuses": Counter(), "invalid_warnings": Counter(),
        "invalid_input_rows": [], "empty_analysis_rows": [],
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
    from lao_ukrainian.hybrid_v2 import combine_neural_tones

    neural = MekongPhonEngine(
        tonal=False, revision=MODEL_REVISION, device="cpu", num_beams=NUM_BEAMS
    )
    neural_tonal = MekongPhonEngine(tonal=True, device="cpu", num_beams=NUM_BEAMS)
    smoke = neural.transcribe("ຂາ")
    tonal_smoke = neural_tonal.transcribe("ຂາ")
    if not tonal_smoke.raw_ipa:
        raise RuntimeError("Pinned tonal MekongPhon smoke inference returned empty IPA")
    if smoke.model_id != MODEL_ID or smoke.model_revision != MODEL_REVISION:
        raise RuntimeError("MekongPhon smoke inference did not resolve the pinned model")

    stages = {
        "vientiane_rules": new_rule_stage(),
        "mekongphon_reference_rules": new_rule_stage(),
        "hybrid_deterministic_rules": new_rule_stage(),
        "hybrid_v2": {
            "predictions": [], "rendered_predictions": [], "tonal_predictions": [],
            "times": [], "attempt_times": [], "errors": Counter(),
            "tone_alignment_statuses": Counter(), "tone_predictions": 0,
            "tone_units_aligned": 0, "tone_units_skipped": 0,
            "deterministic_neural_tone_disagreements": 0,
        },
        "mekongphon_neural": {
            "predictions": [], "times": [], "attempt_times": [], "errors": Counter(),
            "input_rejections": Counter(),
        },
    }

    for row_index, source in enumerate(rows, start=1):
        for key, profile in (
            ("vientiane_rules", "vientiane"),
            ("mekongphon_reference_rules", "mekongphon-reference"),
            ("hybrid_deterministic_rules", "hybrid-deterministic"),
        ):
            stage = stages[key]
            try:
                started = time.perf_counter()
                result = analyze(source, ipa_profile=profile)
                stage["analysis_statuses"].update([result.status])
                if result.status == "INVALID":
                    stage["invalid_input_rows"].append(row_index)
                    stage["invalid_warnings"].update(result.warnings)
                if not result.syllables:
                    stage["empty_analysis_rows"].append(row_index)
                stage["times"].append(time.perf_counter() - started)
                prediction = complete_rule_ipa(result)
                rendered = complete_rule_rendering(result)
                stage["predictions"].append(prediction)
                stage["rendered_predictions"].append(rendered)
                stage["syllables"].update(item.status for item in result.syllables)
                phonetic_syllables = [item for item in result.syllables if item.status != "PASSTHROUGH"]
                stage["syllable_total"] += len(phonetic_syllables)
                stage["syllable_with_ipa"] += sum(accepted_phonetic_ipa(item.phonetic_result) for item in phonetic_syllables)
                stage["passthrough_total"] += sum(item.status == "PASSTHROUGH" for item in result.syllables)
                stage["unit_total"] += len(result.syllables)
                stage["units_rendered"] += sum(item.practical_ukrainian is not None for item in result.syllables)
                stage["target_unmapped_units"] += sum("UKRAINIAN-TARGET-UNMAPPED" in item.warnings for item in result.syllables)
                stage["supported_ipa_units"] += sum(item.phonetic_result is not None and item.phonetic_result.status == "SUPPORTED" for item in phonetic_syllables)
                stage["uncertain_ipa_units"] += sum(item.phonetic_result is not None and item.phonetic_result.status == "UNCERTAIN" for item in phonetic_syllables)
                stage["provisional_units"] += sum(item.phonetic_result is not None and item.phonetic_result.status == "PROVISIONAL" for item in phonetic_syllables)
                missing_statuses, missing_reasons = withheld_ipa_diagnostics(result.syllables)
                stage["withheld_statuses"].update(missing_statuses)
                stage["withheld"].update(missing_reasons)
            except Exception as exc:
                stage["errors"][type(exc).__name__] += 1
                stage["predictions"].append("")
                stage["rendered_predictions"].append("")
            finally:
                stage["attempt_times"].append(time.perf_counter() - started)

        # Keep one persistent model instance; do not reload weights per sentence.
        stage = stages["hybrid_v2"]
        try:
            started = time.perf_counter()
            deterministic = analyze(source, ipa_profile="hybrid-deterministic")
            neural_result = neural_tonal.transcribe(source)
            combined = combine_neural_tones(
                deterministic, neural_result.raw_ipa,
                model_id=neural_result.model_id,
                model_revision=neural_result.model_revision,
            )
            stage["times"].append(time.perf_counter() - started)
            stage["predictions"].append(complete_rule_ipa(deterministic))
            stage["rendered_predictions"].append(complete_rule_rendering(deterministic))
            stage["tonal_predictions"].append(compact_ipa(combined.tonal_ipa))
            stage["tone_alignment_statuses"].update([combined.tone_alignment_status])
            stage["tone_predictions"] += len(combined.tone_predictions)
            stage["tone_units_aligned"] += combined.aligned_syllables
            stage["tone_units_skipped"] += combined.skipped_tone_units
            stage["deterministic_neural_tone_disagreements"] += sum(
                warning.startswith("DETERMINISTIC-NEURAL-TONE-DISAGREEMENT:")
                for warning in combined.warnings
            )
        except Exception as exc:
            stage["errors"][type(exc).__name__] += 1
            stage["predictions"].append("")
            stage["rendered_predictions"].append("")
            stage["tonal_predictions"].append("")
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
            "ipa_complete_sentence_coverage": sum(bool(value) for value in predictions) / len(rows),
            "ipa_complete_sentences": sum(bool(value) for value in predictions),
            "ipa_incomplete_or_failed_sentences": sum(not bool(value) for value in predictions),
            "rendering_coverage": (
                sum(bool(value) for value in stage.get("rendered_predictions", [])) /
                max(1, len(rows) - stage["analysis_statuses"].get("INVALID", 0) - stage["analysis_statuses"].get("EMPTY", 0))
                if "rendered_predictions" in stage else None
            ),
            "dataset_row_rendering_coverage": (
                sum(bool(value) for value in stage.get("rendered_predictions", [])) / len(rows)
                if "rendered_predictions" in stage else None
            ),
            "complete_renderings": sum(bool(value) for value in stage.get("rendered_predictions", [])),
            "unrendered_or_failed_inputs": (
                max(0, len(rows) - stage["analysis_statuses"].get("INVALID", 0) - stage["analysis_statuses"].get("EMPTY", 0)
                    - sum(bool(value) for value in stage.get("rendered_predictions", [])))
                if "rendered_predictions" in stage else 0
            ),
            "analysis_status_counts": dict(sorted(stage["analysis_statuses"].items())) if "analysis_statuses" in stage else {},
            "valid_input_rows": (len(rows) - stage["analysis_statuses"].get("INVALID", 0) - stage["analysis_statuses"].get("EMPTY", 0)) if "analysis_statuses" in stage else None,
            "invalid_input_count": stage["analysis_statuses"].get("INVALID", 0) if "analysis_statuses" in stage else None,
            "empty_analysis_count": stage["analysis_statuses"].get("EMPTY", 0) if "analysis_statuses" in stage else None,
            "invalid_input_rows": stage["invalid_input_rows"] if "invalid_input_rows" in stage else [],
            "invalid_input_warning_categories": dict(sorted(stage["invalid_warnings"].items())) if "invalid_warnings" in stage else {},
            "empty_analysis_rows": stage["empty_analysis_rows"] if "empty_analysis_rows" in stage else [],
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
            summaries[key]["passthrough_units"] = stage["passthrough_total"]
            summaries[key]["analyzed_units"] = stage["unit_total"]
            summaries[key]["units_with_rendering"] = stage["units_rendered"]
            summaries[key]["supported_ipa_units"] = stage["supported_ipa_units"]
            summaries[key]["uncertain_ipa_units"] = stage["uncertain_ipa_units"]
            summaries[key]["provisional_placeholder_units"] = stage["provisional_units"]
            summaries[key]["target_mapping_unavailable_units"] = stage["target_unmapped_units"]
            summaries[key]["withheld_ipa_status_counts"] = dict(sorted(stage["withheld_statuses"].items()))
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
        ("hybrid_deterministic_rules", "mekongphon_neural"),
        ("mekongphon_reference_rules", "hybrid_deterministic_rules"),
        ("hybrid_v2", "mekongphon_neural"),
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
        "schema_version": "1.6",
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
            "coverage_definition": "Rendering coverage is calculated over non-empty, non-INVALID inputs; rejected inputs and empty analyses are reported separately. Every accepted input requires a non-null Ukrainian-side rendering for every analyzed source unit, including explicit passthrough and typed PROVISIONAL placeholders. IPA-complete sentence coverage separately requires IPA for every Lao phonetic syllable; placeholders and passthrough are excluded from IPA coverage. Neither metric is phonetic accuracy.",
            "limitations": [
                "No IPA reference is supplied; gold IPA CER is not measurable.",
                "Pairwise output disagreement is not accuracy and cannot identify the correct engine.",
                "This is a sentence-domain stress test, not an adjudicated phonetic benchmark.",
            ],
        },
        "engines": {
            "vientiane_rules": {"implementation": "ClippyFirst deterministic default"},
            "mekongphon_reference_rules": {"implementation": "ClippyFirst legacy deterministic compatibility profile"},
            "hybrid_deterministic_rules": {"implementation": "Vientiane baseline plus deterministic evidence-rule selector"},
            "hybrid_v2": {
                "segmental_lane": "hybrid-deterministic ClippyFirst IPA",
                "tonal_lane_model_id": neural_tonal.model_id,
                "tonal_lane_revision": neural_tonal.revision,
                "tone_alignment": "unique ordered contour decomposition; associations remain UNCERTAIN",
            },
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
            "Hybrid v2 model loading and tonal smoke inference are excluded from per-row latency.",
            "Hybrid v2 segmental IPA and tonal IPA remain separate lanes; no fused string is constructed.",
            "No source sentences or per-sentence IPA predictions are persisted.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    hybrid_rendering = summaries["hybrid_deterministic_rules"]
    hybrid_v2_rendering = summaries["hybrid_v2"]
    if (
        hybrid_rendering["rendering_coverage"] != 1.0
        or hybrid_rendering["unrendered_or_failed_inputs"] != 0
        or hybrid_rendering["units_with_rendering"] != hybrid_rendering["analyzed_units"]
    ):
        raise RuntimeError(
            "Hybrid 100% rendering-coverage gate failed: "
            + json.dumps(hybrid_rendering, ensure_ascii=False, sort_keys=True)
        )
    if (
        hybrid_v2_rendering["dataset_row_rendering_coverage"] != 1.0
        or hybrid_v2_rendering["complete_renderings"] != len(rows)
        or hybrid_v2_rendering["runtime_errors_by_type"]
    ):
        raise RuntimeError(
            "Hybrid v2 100% rendering-coverage/runtime gate failed: "
            + json.dumps(hybrid_v2_rendering, ensure_ascii=False, sort_keys=True)
        )
    if report["runtime_errors"]:
        raise RuntimeError(f"Runtime errors: {report['runtime_errors']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
