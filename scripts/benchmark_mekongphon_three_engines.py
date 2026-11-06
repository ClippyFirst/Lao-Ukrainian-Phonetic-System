#!/usr/bin/env python3
"""Compare Lao G2P engines on the MekongPhon held-out lexicon.

Segmental IPA and tonal IPA are scored separately. This matters because
ClippyFirst preserves tone contours as typed metadata rather than appending
them to its segmental phonemic_ipa string.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import os
import platform
import statistics
import sys
import time
import unicodedata
import urllib.request
from pathlib import Path

DATA_URL = (
    "https://raw.githubusercontent.com/byu-matrix-lab/MekongPhon/"
    "f80f6c1840c4818b51e05f2e00cded4701a5b662/data/splits/lao_eval.csv"
)
TONAL_MODEL_ID = "byumatrixlab/lao-ipa-tonal"
SEGMENTAL_MODEL_ID = "byumatrixlab/lao-ipa-nontonal"


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


def load_dataset() -> tuple[list[dict[str, str]], str]:
    request = urllib.request.Request(DATA_URL, headers={"User-Agent": "LaoG2P-benchmark/2.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = response.read()
    digest = hashlib.sha256(payload).hexdigest()
    rows = list(csv.DictReader(payload.decode("utf-8-sig").splitlines()))
    required = {"orth", "pron_no_tones", "pron_with_tones"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("MekongPhon held-out CSV is empty or has an unexpected schema")
    if len(rows) != 100:
        raise ValueError(f"Expected the published 100-entry lexicon holdout, received {len(rows)}")
    if any(not row["orth"].strip() or not row["pron_no_tones"].strip()
           or not row["pron_with_tones"].strip() for row in rows):
        raise ValueError("Held-out set contains an empty source or IPA reference")
    if len({row["orth"] for row in rows}) != len(rows):
        raise ValueError("Held-out set contains duplicate orthographic forms")
    return rows, digest


def load_project():
    from lao_ukrainian.core import analyze

    def predict(text: str) -> dict[str, str | float]:
        started = time.perf_counter()
        analysis = analyze(text)
        segmental_elapsed = time.perf_counter() - started

        syllables = analysis.syllables
        segmental_complete = bool(syllables) and all(
            item.phonetic_result and item.phonetic_result.phonemic_ipa
            for item in syllables
        )
        tonal_complete = segmental_complete and all(
            item.phonetic_result.tone_contour_ipa
            for item in syllables
        )
        segmental = (
            nfc("".join(item.phonetic_result.phonemic_ipa for item in syllables))
            if segmental_complete else ""
        )
        tonal = (
            nfc("".join(
                item.phonetic_result.phonemic_ipa + item.phonetic_result.tone_contour_ipa
                for item in syllables
            ))
            if tonal_complete else ""
        )
        return {
            "segmental": segmental,
            "tonal": tonal,
            "status": analysis.status,
            "warnings": [
                warning
                for item in syllables
                for warning in item.warnings
            ],
            "segmental_seconds": segmental_elapsed,
            "tonal_seconds": 0.0,
        }

    return predict


def load_lao2ipa():
    from lao2ipa import transliterate

    def predict(text: str) -> dict[str, str | float]:
        started = time.perf_counter()
        segmental = transliterate(text, output="ipa", ignore_tones=True)
        segmental_elapsed = time.perf_counter() - started
        started = time.perf_counter()
        tonal = transliterate(text, output="ipa", ignore_tones=False)
        tonal_elapsed = time.perf_counter() - started
        if not isinstance(segmental, str) or not isinstance(tonal, str):
            raise TypeError("lao2ipa must return strings for both output modes")
        return {
            "segmental": nfc(segmental),
            "tonal": nfc(tonal),
            "status": "RETURNED",
            "segmental_seconds": segmental_elapsed,
            "tonal_seconds": tonal_elapsed,
        }

    return predict


def load_neural():
    import torch
    from transformers import AutoTokenizer, EncoderDecoderModel
    from huggingface_hub import model_info

    torch.set_num_threads(min(2, os.cpu_count() or 1))

    def load_one(model_id: str):
        info = model_info(model_id)
        revision = info.sha
        model = EncoderDecoderModel.from_pretrained(model_id, revision=revision)
        encoder = AutoTokenizer.from_pretrained(
            model_id, subfolder="encoder_tokenizer", revision=revision
        )
        decoder = AutoTokenizer.from_pretrained(
            model_id, subfolder="decoder_tokenizer", revision=revision
        )
        model.eval()

        def generate(text: str) -> str:
            inputs = encoder(text, return_tensors="pt", truncation=True, max_length=128)
            with torch.inference_mode():
                output_ids = model.generate(
                    **inputs, max_length=128, num_beams=5, early_stopping=True
                )
            return nfc(decoder.decode(output_ids[0], skip_special_tokens=True))

        return generate, revision

    tonal_generate, tonal_revision = load_one(TONAL_MODEL_ID)
    segmental_generate, segmental_revision = load_one(SEGMENTAL_MODEL_ID)

    def predict(text: str) -> dict[str, str | float]:
        started = time.perf_counter()
        segmental = segmental_generate(text)
        segmental_elapsed = time.perf_counter() - started
        started = time.perf_counter()
        tonal = tonal_generate(text)
        tonal_elapsed = time.perf_counter() - started
        return {
            "segmental": segmental,
            "tonal": tonal,
            "status": "RETURNED",
            "segmental_seconds": segmental_elapsed,
            "tonal_seconds": tonal_elapsed,
        }

    return predict, {
        "segmental_model": SEGMENTAL_MODEL_ID,
        "segmental_revision": segmental_revision,
        "tonal_model": TONAL_MODEL_ID,
        "tonal_revision": tonal_revision,
    }


def score(references: list[str], predictions: list[str]) -> dict[str, object]:
    import sacrebleu

    def metrics(refs: list[str], preds: list[str]) -> dict[str, object]:
        edits = sum(levenshtein(ref, pred) for ref, pred in zip(refs, preds))
        chars = sum(len(ref) for ref in refs)
        exact = sum(ref == pred for ref, pred in zip(refs, preds))
        chrf = sacrebleu.metrics.CHRF(word_order=2).corpus_score(preds, [refs])
        return {
            "n": len(refs),
            "exact_matches": exact,
            "exact_match_rate": exact / len(refs) if refs else None,
            "cer": edits / chars if chars else None,
            "chrf++": chrf.score,
        }

    covered = [(ref, pred) for ref, pred in zip(references, predictions) if pred]
    return {
        **metrics(references, predictions),
        "coverage": len(covered) / len(references) if references else 0.0,
        "missing_or_withheld": len(references) - len(covered),
        "covered_subset": metrics(
            [pair[0] for pair in covered],
            [pair[1] for pair in covered],
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path,
        default=Path("artifacts/mekongphon-100-word-benchmark.json"),
    )
    args = parser.parse_args()

    rows, dataset_sha = load_dataset()
    sources = [nfc(row["orth"]) for row in rows]
    segmental_references = [nfc(row["pron_no_tones"]) for row in rows]
    tonal_references = [nfc(row["pron_with_tones"]) for row in rows]

    neural_predict, neural_provenance = load_neural()
    engines = {
        "clippyfirst_rule_engine": (load_project(), "repository source"),
        "lao2ipa": (load_lao2ipa(), importlib.metadata.version("lao2ipa")),
        "mekongphon_neural": (neural_predict, neural_provenance),
    }

    results: dict[str, object] = {}
    for name, (predict, version) in engines.items():
        segmental_outputs: list[str] = []
        tonal_outputs: list[str] = []
        statuses: dict[str, int] = {}
        segmental_durations: list[float] = []
        tonal_durations: list[float] = []
        errors = 0
        warning_counts: dict[str, int] = {}
        segmental_withheld = 0
        tonal_withheld = 0

        for source in sources:
            try:
                output = predict(source)
                segmental = nfc(str(output["segmental"]))
                tonal = nfc(str(output["tonal"]))
                status = str(output["status"])
                for warning in output.get("warnings", []):
                    warning = str(warning)
                    warning_code, _, detail = warning.partition(":")
                    if warning_code == "SHORT_VOWEL_REQUIRES_CODA":
                        warning_code = f"{warning_code}:{detail}"
                    elif warning_code == "UNCONSUMED_AFTER_VOWEL":
                        tail = detail
                        if any(ch in "່້໊໋" for ch in tail):
                            shape = "contains-tone-mark"
                        elif tail.startswith(("ເ", "ແ", "ໂ", "ໃ", "ໄ")):
                            shape = "starts-preposed-vowel"
                        elif len(tail) == 1:
                            shape = "single-grapheme"
                        elif any(ch in "ະັາິີຶືຸູົຽໍຳວອຍ" for ch in tail):
                            shape = "contains-vowel-material"
                        else:
                            shape = "other-multigrapheme"
                        warning_code = f"{warning_code}:{shape}"
                    warning_counts[warning_code] = warning_counts.get(warning_code, 0) + 1
                segmental_durations.append(float(output["segmental_seconds"]))
                tonal_durations.append(float(output["tonal_seconds"]))
            except Exception as exc:
                segmental = ""
                tonal = ""
                status = f"ERROR:{type(exc).__name__}"
                segmental_durations.append(0.0)
                tonal_durations.append(0.0)
                errors += 1
            segmental_outputs.append(segmental)
            tonal_outputs.append(tonal)
            segmental_withheld += not bool(segmental)
            tonal_withheld += not bool(tonal)
            statuses[status] = statuses.get(status, 0) + 1

        segmental_metrics = score(segmental_references, segmental_outputs)
        tonal_metrics = score(tonal_references, tonal_outputs)
        results[name] = {
            "version_or_revision": version,
            "segmental_vs_pron_no_tones": segmental_metrics,
            "tonal_vs_pron_with_tones": tonal_metrics,
            "runtime_errors": errors,
            "status_counts": statuses,
            "segmental_withheld_items": segmental_withheld,
            "tonal_withheld_items": tonal_withheld,
            "warning_counts": dict(sorted(warning_counts.items())),
            "segmental_mean_latency_ms": round(statistics.mean(segmental_durations) * 1000, 3),
            "tonal_mean_latency_ms": round(statistics.mean(tonal_durations) * 1000, 3),
            "segmental_throughput_items_per_second": (
                round(len(segmental_durations) / sum(segmental_durations), 3)
                if sum(segmental_durations) else None
            ),
            "tonal_throughput_items_per_second": (
                round(len(tonal_durations) / sum(tonal_durations), 3)
                if sum(tonal_durations) else None
            ),
        }

    report = {
        "schema_version": "2.0",
        "benchmark": "MekongPhon held-out Lao lexicon, 100 words",
        "dataset": {
            "url": DATA_URL,
            "source_revision": "f80f6c1840c4818b51e05f2e00cded4701a5b662",
            "sha256": dataset_sha,
            "n": len(rows),
            "segmental_reference_column": "pron_no_tones",
            "tonal_reference_column": "pron_with_tones",
            "profile": "Lao, Vientiane tone convention as described in MekongPhon",
            "redistribution": "No source rows, references or per-item predictions are included in this report.",
        },
        "method": {
            "normalization": "Unicode NFC and outer whitespace trim only",
            "segmental_comparison": "phonemic segments and vowel length against pron_no_tones",
            "tonal_comparison": "segmental IPA plus per-syllable tone contour against pron_with_tones",
            "cer": "Unicode code-point Levenshtein distance summed over all items, divided by total reference code points",
            "chrf++": "SacreBLEU CHRF with word_order=2, corpus-level",
            "exact_match": "strict full-string IPA comparison",
            "missing_output": "empty output remains in the denominator and incurs full reference deletion cost",
            "clippyfirst_tone_contract": "tone contour is stored separately in typed PhoneticResult metadata; tonal score composes it after each syllable's segmental IPA",
            "latency": "per-item inference; model loading excluded; CPU runner, sequential items",
            "scope_warning": "This is the 100 held-out seed-lexicon word set, not the paper's 13,442-sentence test. It cannot be compared numerically with the paper's sentence-level Table 4.",
            "gold_warning": "The source paper describes the seed lexicon as derived from human-annotated IPA in Kerr (1972), with a 500-entry manual review; it also reports 14/500 Lao inaccuracies. This benchmark is not independently re-adjudicated gold for this project.",
            "historical_note": "Schema 1.0 compared ClippyFirst segmental IPA to the tonal reference and therefore mixed output contracts. Schema 2.0 separates segmental and tonal scoring; do not interpret old and new CER values as directly comparable.",
        },
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "torch": importlib.metadata.version("torch"),
            "transformers": importlib.metadata.version("transformers"),
            "sacrebleu": importlib.metadata.version("sacrebleu"),
        },
        "engines": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "benchmark": report["benchmark"],
        "dataset_sha256": dataset_sha,
        "engines": {
            name: {
                "segmental_cer": result["segmental_vs_pron_no_tones"]["cer"],
                "segmental_coverage": result["segmental_vs_pron_no_tones"]["coverage"],
                "tonal_cer": result["tonal_vs_pron_with_tones"]["cer"],
                "tonal_coverage": result["tonal_vs_pron_with_tones"]["coverage"],
                "runtime_errors": result["runtime_errors"],
            }
            for name, result in results.items()
        },
        "report": str(args.output),
    }, ensure_ascii=False, indent=2))
    return 1 if any(result["runtime_errors"] for result in results.values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
