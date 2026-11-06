#!/usr/bin/env python3
"""Run a three-engine Lao G2P comparison on MekongPhon held-out lexicon entries.

The upstream 100-entry lexicon holdout is downloaded at runtime and is not
committed or included in the report. This is a word-level diagnostic, not the
paper's 13,442-sentence test and not a replacement for independent adjudication.
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
MODEL_ID = "byumatrixlab/lao-ipa-tonal"
MODEL_REVISION = "main"


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
    request = urllib.request.Request(DATA_URL, headers={"User-Agent": "LaoG2P-benchmark/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = response.read()
    digest = hashlib.sha256(payload).hexdigest()
    rows = list(csv.DictReader(payload.decode("utf-8-sig").splitlines()))
    required = {"orth", "pron_no_tones", "pron_with_tones"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("MekongPhon held-out CSV is empty or has an unexpected schema")
    if len(rows) != 100:
        raise ValueError(f"Expected the published 100-entry lexicon holdout, received {len(rows)}")
    if any(not row["orth"].strip() or not row["pron_with_tones"].strip() for row in rows):
        raise ValueError("Held-out set contains an empty orthographic form or tonal reference")
    if len({row["orth"] for row in rows}) != len(rows):
        raise ValueError("Held-out set contains duplicate orthographic forms")
    return rows, digest


def load_project():
    from lao_ukrainian.core import analyze

    def predict(text: str) -> tuple[str, str]:
        analysis = analyze(text)
        values = [syllable.phonemic_ipa for syllable in analysis.syllables]
        if not values or any(value is None for value in values):
            return "", analysis.status
        return nfc("".join(values)), analysis.status

    return predict


def load_lao2ipa():
    from lao2ipa import transliterate

    def predict(text: str) -> tuple[str, str]:
        value = transliterate(text, output="ipa")
        if not isinstance(value, str):
            raise TypeError(f"lao2ipa returned {type(value).__name__}, expected str")
        return nfc(value), "RETURNED"

    return predict


def load_neural():
    import torch
    from transformers import AutoTokenizer, EncoderDecoderModel
    from huggingface_hub import model_info

    torch.set_num_threads(min(2, os.cpu_count() or 1))
    info = model_info(MODEL_ID, revision=MODEL_REVISION)
    model = EncoderDecoderModel.from_pretrained(MODEL_ID, revision=info.sha)
    encoder = AutoTokenizer.from_pretrained(
        MODEL_ID, subfolder="encoder_tokenizer", revision=info.sha
    )
    decoder = AutoTokenizer.from_pretrained(
        MODEL_ID, subfolder="decoder_tokenizer", revision=info.sha
    )
    model.eval()

    def predict(text: str) -> tuple[str, str]:
        inputs = encoder(text, return_tensors="pt", truncation=True, max_length=128)
        with torch.inference_mode():
            output_ids = model.generate(
                **inputs, max_length=128, num_beams=5, early_stopping=True
            )
        return nfc(decoder.decode(output_ids[0], skip_special_tokens=True)), "RETURNED"

    return predict, info.sha


def score(references: list[str], predictions: list[str]) -> dict[str, object]:
    import sacrebleu

    edits = sum(levenshtein(ref, pred) for ref, pred in zip(references, predictions))
    chars = sum(len(ref) for ref in references)
    chrf = sacrebleu.metrics.CHRF(word_order=2).corpus_score(predictions, [references])
    return {
        "n": len(references),
        "exact_matches": sum(ref == pred for ref, pred in zip(references, predictions)),
        "exact_match_rate": sum(ref == pred for ref, pred in zip(references, predictions)) / len(references),
        "cer": edits / chars if chars else None,
        "chrf++": chrf.score,
        "coverage": sum(bool(pred) for pred in predictions) / len(predictions),
        "missing_or_withheld": sum(not bool(pred) for pred in predictions),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("artifacts/mekongphon-100-word-benchmark.json"))
    args = parser.parse_args()
    rows, dataset_sha = load_dataset()
    sources = [nfc(row["orth"]) for row in rows]
    references = [nfc(row["pron_with_tones"]) for row in rows]

    project_predict = load_project()
    lao2ipa_predict = load_lao2ipa()
    neural_predict, neural_revision = load_neural()

    engines = {
        "clippyfirst_rule_engine": (project_predict, "repository source"),
        "lao2ipa": (lao2ipa_predict, importlib.metadata.version("lao2ipa")),
        "mekongphon_neural": (neural_predict, neural_revision),
    }
    results: dict[str, object] = {}
    for name, (predict, version) in engines.items():
        outputs: list[str] = []
        statuses: dict[str, int] = {}
        durations: list[float] = []
        errors = 0
        for source in sources:
            started = time.perf_counter()
            try:
                output, status = predict(source)
            except Exception as exc:
                output, status = "", f"ERROR:{type(exc).__name__}"
                errors += 1
            durations.append(time.perf_counter() - started)
            outputs.append(nfc(output))
            statuses[status] = statuses.get(status, 0) + 1
        summary = score(references, outputs)
        summary.update({
            "version_or_revision": version,
            "runtime_errors": errors,
            "status_counts": statuses,
            "total_inference_seconds": round(sum(durations), 4),
            "mean_latency_ms": round(statistics.mean(durations) * 1000, 3),
            "p95_latency_ms": round(sorted(durations)[max(0, int(0.95 * len(durations)) - 1)] * 1000, 3),
            "throughput_items_per_second": round(len(durations) / sum(durations), 3) if sum(durations) else None,
        })
        results[name] = summary

    report = {
        "schema_version": "1.0",
        "benchmark": "MekongPhon held-out Lao lexicon, 100 words",
        "dataset": {
            "url": DATA_URL,
            "source_revision": "f80f6c1840c4818b51e05f2e00cded4701a5b662",
            "sha256": dataset_sha,
            "n": len(rows),
            "reference_column": "pron_with_tones",
            "profile": "Lao, Vientiane tone convention as described in MekongPhon",
            "redistribution": "No source rows, references or per-item predictions are included in this report.",
        },
        "method": {
            "normalization": "Unicode NFC and outer whitespace trim only",
            "cer": "Unicode code-point Levenshtein distance summed over all items, divided by total reference code points",
            "chrf++": "SacreBLEU CHRF with word_order=2, corpus-level",
            "exact_match": "strict full-string IPA comparison; tone and length marks retained",
            "missing_output": "empty output remains in the denominator and incurs full reference deletion cost",
            "latency": "per-item inference only; model/package loading excluded; CPU runner, sequential items",
            "scope_warning": "This is the 100 held-out seed-lexicon word set, not the paper's 13,442-sentence test. It measures isolated lexical generalization and cannot be compared numerically with the paper's sentence-level Table 4.",
            "gold_warning": "The source paper describes the seed lexicon as derived from human-annotated IPA in Kerr (1972), with a 500-entry manual review; it also reports 14/500 Lao inaccuracies. This benchmark is therefore a published reference set, not independently re-adjudicated gold for this project.",
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
            name: {key: result[key] for key in (
                "n", "cer", "chrf++", "exact_match_rate", "coverage",
                "runtime_errors", "mean_latency_ms", "throughput_items_per_second"
            )}
            for name, result in results.items()
        },
        "report": str(args.output),
    }, ensure_ascii=False, indent=2))
    return 1 if any(result["runtime_errors"] for result in results.values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
