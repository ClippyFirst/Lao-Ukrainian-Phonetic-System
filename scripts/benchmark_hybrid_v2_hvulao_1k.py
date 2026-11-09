#!/usr/bin/env python3
"""Hybrid v2 HVULao 1k sentence-domain stress test; not an IPA accuracy test."""
from __future__ import annotations

import argparse
from collections import Counter
import json
import time
from pathlib import Path

try:
    from scripts.benchmark_hvulao_1k_three_engines import (
        classify_input_rejection,
        compact_ipa,
        complete_rule_ipa,
        complete_rule_rendering,
        latency_summary,
        load_dataset,
    )
except ModuleNotFoundError:
    from benchmark_hvulao_1k_three_engines import (
        classify_input_rejection,
        compact_ipa,
        complete_rule_ipa,
        complete_rule_rendering,
        latency_summary,
        load_dataset,
    )

from lao_ukrainian.core import analyze
from lao_ukrainian.mekongphon import MekongPhonEngine, MODEL_IDS, MODEL_REVISIONS
from lao_ukrainian.hybrid_v2 import combine_neural_tones
from lao_ukrainian.phonetic_result import from_external_ipa

NUM_BEAMS = 5


def new_counts() -> dict:
    return {
        "errors": Counter(),
        "input_rejections": Counter(),
        "analysis_statuses": Counter(),
        "tone_alignment_statuses": Counter(),
        "tonal_ipa_parse_statuses": Counter(),
        "tonal_ipa_parse_warning_categories": Counter(),
        "tone_alignment_warning_categories": Counter(),
        "attempt_times": [],
        "deterministic_times": [],
        "neural_times": [],
        "rows_with_ukrainian_rendering": 0,
        "rows_with_complete_segmental_ipa": 0,
        "rows_with_parseable_tonal_ipa": 0,
        "rows_with_neural_output": 0,
        "rows_with_order_aligned_tones": 0,
        "rows_with_partial_tone_association": 0,
        "analyzed_units": 0,
        "rendered_units": 0,
        "segmental_ipa_units": 0,
        "supported_segmental_ipa_units": 0,
        "tone_prediction_units": 0,
        "skipped_tone_units": 0,
        "passthrough_units": 0,
        "unknown_marker_units": 0,
    }


def run(output: Path) -> dict:
    rows, blob_sha, rows_without_lao = load_dataset()
    engine = MekongPhonEngine(
        tonal=True,
        revision=MODEL_REVISIONS["tonal"],
        device="cpu",
        num_beams=NUM_BEAMS,
    )
    smoke = engine.transcribe("ຂາ")
    if smoke.model_id != MODEL_IDS["tonal"] or smoke.model_revision != MODEL_REVISIONS["tonal"]:
        raise RuntimeError("Hybrid v2 smoke inference did not resolve the pinned tonal model")

    counts = new_counts()
    for source in rows:
        attempt_started = time.perf_counter()
        analysis = None
        try:
            started = time.perf_counter()
            analysis = analyze(source)
            counts["deterministic_times"].append(time.perf_counter() - started)
            counts["analysis_statuses"].update([analysis.status])
            syllables = analysis.syllables
            phonetic = [item for item in syllables if item.status != "PASSTHROUGH"]
            counts["analyzed_units"] += len(syllables)
            counts["passthrough_units"] += sum(item.status == "PASSTHROUGH" for item in syllables)
            counts["rendered_units"] += sum(item.practical_ukrainian is not None for item in syllables)
            counts["segmental_ipa_units"] += sum(
                item.phonetic_result is not None
                and item.phonetic_result.status in {"SUPPORTED", "UNCERTAIN"}
                and bool(item.phonetic_result.phonemic_ipa)
                for item in phonetic
            )
            counts["supported_segmental_ipa_units"] += sum(
                item.phonetic_result is not None
                and item.phonetic_result.status == "SUPPORTED"
                for item in phonetic
            )
            counts["unknown_marker_units"] += sum(
                item.phonetic_result is not None
                and any(segment.kind == "unknown" for segment in item.phonetic_result.segments)
                for item in phonetic
            )
            if complete_rule_rendering(analysis):
                counts["rows_with_ukrainian_rendering"] += 1
            if complete_rule_ipa(analysis):
                counts["rows_with_complete_segmental_ipa"] += 1
        except Exception as exc:
            counts["errors"][f"DETERMINISTIC:{type(exc).__name__}"] += 1
            counts["attempt_times"].append(time.perf_counter() - attempt_started)
            continue

        try:
            started = time.perf_counter()
            neural = engine.transcribe(source)
            counts["neural_times"].append(time.perf_counter() - started)
            counts["rows_with_neural_output"] += bool(neural.raw_ipa)
            parsed = from_external_ipa(
                neural.raw_ipa,
                provenance=("HYBRID-V2", neural.model_id, f"MODEL-REVISION:{neural.model_revision}"),
            )
            counts["tonal_ipa_parse_statuses"].update([parsed.status])
            for warning in parsed.uncertainty:
                counts["tonal_ipa_parse_warning_categories"].update([str(warning).split(":", 1)[0]])
            if parsed.status == "SUPPORTED" and neural.raw_ipa.strip():
                counts["rows_with_parseable_tonal_ipa"] += 1
            combined = combine_neural_tones(
                analysis,
                neural.raw_ipa,
                model_id=neural.model_id,
                model_revision=neural.model_revision,
            )
            counts["tone_alignment_statuses"].update([combined.tone_alignment_status])
            for warning in combined.warnings:
                counts["tone_alignment_warning_categories"].update([str(warning).split(":", 1)[0]])
            counts["tone_prediction_units"] += len(combined.tone_predictions)
            counts["skipped_tone_units"] += combined.skipped_tone_units
            if combined.tone_alignment_status == "ORDER_ALIGNED":
                counts["rows_with_order_aligned_tones"] += 1
            elif combined.tone_alignment_status == "PARTIAL":
                counts["rows_with_partial_tone_association"] += 1
        except ValueError as exc:
            rejection = classify_input_rejection(exc)
            if rejection:
                counts["input_rejections"][rejection] += 1
            else:
                counts["errors"][f"NEURAL:{type(exc).__name__}"] += 1
        except (RuntimeError, OSError) as exc:
            counts["errors"][f"NEURAL:{type(exc).__name__}"] += 1
        except Exception as exc:
            counts["errors"][f"NEURAL_UNEXPECTED:{type(exc).__name__}"] += 1
        finally:
            counts["attempt_times"].append(time.perf_counter() - attempt_started)

    rows_n = len(rows)
    phonetic_units = counts["analyzed_units"] - counts["passthrough_units"]
    report = {
        "schema_version": "1.0",
        "status": "hybrid_v2_sentence_domain_stress_not_ipa_accuracy",
        "benchmark": {
            "name": "HVULao_NLP 1k raw-sentence test split",
            "repository": "HaHVU/HVULao_NLP",
            "revision": "ec8be4f1a541f3a5c76b4ebda39a9b2795d5c568",
            "path": "Datatest1k/testorgin1000.txt",
            "rows": rows_n,
            "rows_without_lao_block_characters": rows_without_lao,
            "git_blob_sha1": blob_sha,
            "dataset_license": "CC-BY-4.0 (Mendeley Data version 2)",
            "limitations": [
                "No IPA reference is supplied; gold IPA CER and phonetic accuracy are not measurable.",
                "Coverage, parseability and output disagreement are engineering metrics, not accuracy.",
                "The neural model rejects some inputs above its explicit 128-token/code-point limits or outside its Unicode contract.",
            ],
        },
        "hybrid_v2_contract": {
            "segmental_ipa_and_ukrainian": "ClippyFirst deterministic hybrid; no neural segmental substitution",
            "tonal_ipa": "Untouched pinned MekongPhon tonal model output in a separate lane",
            "syllable_tone_metadata": "Only unique ordered contour decomposition; every neural prediction remains UNCERTAIN",
            "no_synthetic_fusion": True,
            "model_id": MODEL_IDS["tonal"],
            "model_revision": MODEL_REVISIONS["tonal"],
            "num_beams": NUM_BEAMS,
            "device": "cpu",
        },
        "results": {
            "input_rows": rows_n,
            "ukrainian_rendering_rows": counts["rows_with_ukrainian_rendering"],
            "ukrainian_rendering_coverage": counts["rows_with_ukrainian_rendering"] / rows_n,
            "complete_segmental_ipa_rows": counts["rows_with_complete_segmental_ipa"],
            "complete_segmental_ipa_coverage": counts["rows_with_complete_segmental_ipa"] / rows_n,
            "neural_output_rows": counts["rows_with_neural_output"],
            "parseable_tonal_ipa_rows": counts["rows_with_parseable_tonal_ipa"],
            "parseable_tonal_ipa_coverage": counts["rows_with_parseable_tonal_ipa"] / rows_n,
            "order_aligned_tone_rows": counts["rows_with_order_aligned_tones"],
            "partial_tone_association_rows": counts["rows_with_partial_tone_association"],
            "tone_alignment_status_counts": dict(sorted(counts["tone_alignment_statuses"].items())),
            "tonal_ipa_parse_status_counts": dict(sorted(counts["tonal_ipa_parse_statuses"].items())),
            "tonal_ipa_parse_warning_categories": dict(sorted(counts["tonal_ipa_parse_warning_categories"].items())),
            "tone_alignment_warning_categories": dict(sorted(counts["tone_alignment_warning_categories"].items())),
            "analyzed_units": counts["analyzed_units"],
            "phonetic_units": phonetic_units,
            "rendered_units": counts["rendered_units"],
            "rendered_unit_coverage": counts["rendered_units"] / counts["analyzed_units"] if counts["analyzed_units"] else None,
            "segmental_ipa_units": counts["segmental_ipa_units"],
            "supported_segmental_ipa_units": counts["supported_segmental_ipa_units"],
            "segmental_ipa_unit_coverage": counts["segmental_ipa_units"] / phonetic_units if phonetic_units else None,
            "neural_tone_prediction_units": counts["tone_prediction_units"],
            "neural_tone_prediction_coverage": counts["tone_prediction_units"] / phonetic_units if phonetic_units else None,
            "skipped_tone_units": counts["skipped_tone_units"],
            "passthrough_units": counts["passthrough_units"],
            "explicit_unknown_marker_units": counts["unknown_marker_units"],
            "analysis_status_counts": dict(sorted(counts["analysis_statuses"].items())),
            "neural_input_rejections_by_reason": dict(sorted(counts["input_rejections"].items())),
            "unexpected_runtime_errors_by_type": dict(sorted(counts["errors"].items())),
            "runtime_errors": sum(counts["errors"].values()),
            "deterministic_latency": latency_summary(counts["deterministic_times"]),
            "neural_latency_successful_calls": latency_summary(counts["neural_times"]),
            "all_attempt_latency": latency_summary(counts["attempt_times"]),
        },
        "measurement_notes": [
            "One hosted CPU run; model load and initial smoke inference excluded from per-row latency.",
            "All 1,000 rows are retained in denominators; input rejections are not counted as neural successes.",
            "No source sentences, row-level IPA, or row-level Ukrainian output are persisted.",
        ],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["results"]["ukrainian_rendering_coverage"] != 1.0:
        raise RuntimeError("Hybrid v2 did not preserve 100% Ukrainian rendering coverage")
    if report["results"]["runtime_errors"]:
        raise RuntimeError("Hybrid v2 benchmark encountered unexpected runtime errors")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("artifacts/hybrid-v2-hvulao-1k.json"))
    args = parser.parse_args()
    run(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
