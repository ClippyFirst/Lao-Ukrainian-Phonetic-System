#!/usr/bin/env python3
"""Run additional independent Lao G2P comparators on the pinned MekongPhon holdout.

This is a source-attested diagnostic, not an independent-gold accuracy test.
Only aggregate metrics and source/package hashes are persisted.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import platform
import re
import statistics
import time
import unicodedata
import urllib.request
from pathlib import Path

DATA_URL = (
    "https://raw.githubusercontent.com/byu-matrix-lab/MekongPhon/"
    "f80f6c1840c4818b51e05f2e00cded4701a5b662/data/splits/lao_eval.csv"
)
O2I_COMMIT = "32b66b0b1a4b66f7267790d7ec1f346460f8d814"
TONES = re.compile(r"[˩˨˧˦˥]+")


def nfc(value: str) -> str:
    return unicodedata.normalize("NFC", value.strip())


def no_tones(value: str) -> str:
    return nfc(TONES.sub("", value))


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


def load_rows() -> tuple[list[dict[str, str]], str]:
    request = urllib.request.Request(DATA_URL, headers={"User-Agent": "ClippyFirst-Lao-G2P-benchmark/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = response.read()
    digest = hashlib.sha256(payload).hexdigest()
    rows = list(csv.DictReader(payload.decode("utf-8-sig").splitlines()))
    required = {"orth", "pron_no_tones", "pron_with_tones"}
    if len(rows) != 100 or not required.issubset(rows[0]):
        raise ValueError("Expected exact 100-row MekongPhon held-out schema")
    if len({row["orth"] for row in rows}) != 100:
        raise ValueError("Duplicate orthographies in held-out split")
    if any(not row[key].strip() for row in rows for key in required):
        raise ValueError("Empty source or reference in held-out split")
    return rows, digest


def package_file_sha256(package: str, relative_path: str) -> str:
    from importlib.resources import files
    payload = files(package).joinpath(relative_path).read_bytes()
    return hashlib.sha256(payload).hexdigest()


def renderable_external_prediction(value: str | None) -> str:
    """Keep every benchmark input visible without treating ? as a phone."""
    return nfc(value or "") or "?"


def run_engine(name: str, predict, rows: list[dict[str, str]]) -> dict[str, object]:
    raw_segmental_predictions: list[str] = []
    raw_tonal_predictions: list[str] = []
    segmental_times: list[float] = []
    tonal_times: list[float] = []
    errors = 0

    for row in rows:
        try:
            segmental, tonal, segmental_ms, tonal_ms = predict(row["orth"])
            raw_segmental_predictions.append(nfc(segmental))
            raw_tonal_predictions.append(nfc(tonal))
            segmental_times.append(segmental_ms)
            tonal_times.append(tonal_ms)
        except Exception:
            errors += 1
            raw_segmental_predictions.append("")
            raw_tonal_predictions.append("")

    segmental_predictions = [
        renderable_external_prediction(value) for value in raw_segmental_predictions
    ]
    tonal_predictions = [
        renderable_external_prediction(value) for value in raw_tonal_predictions
    ]

    def metrics(reference_key: str, predictions: list[str], raw_predictions: list[str]) -> dict[str, object]:
        refs = [nfc(row[reference_key]) for row in rows]
        edits = sum(levenshtein(ref, pred) for ref, pred in zip(refs, predictions))
        chars = sum(len(ref) for ref in refs)
        covered = sum(bool(value) for value in predictions)
        exact = sum(ref == pred for ref, pred in zip(refs, predictions))
        covered_pairs = [(ref, pred) for ref, pred in zip(refs, predictions) if pred]
        covered_edits = sum(levenshtein(ref, pred) for ref, pred in covered_pairs)
        covered_chars = sum(len(ref) for ref, _ in covered_pairs)
        return {
            "reference": reference_key,
            "n": len(refs),
            "exact": exact,
            "exact_rate": exact / len(refs),
            "cer_full_denominator": edits / chars if chars else None,
            "output_coverage": covered / len(refs),
            "engine_success_coverage": sum(bool(value) for value in raw_predictions) / len(refs),
            "explicit_unknown_markers": sum(value == "?" for value in predictions),
            "covered_subset_cer": covered_edits / covered_chars if covered_chars else None,
            "missing": len(refs) - covered,
        }

    return {
        "engine": name,
        "segmental": metrics("pron_no_tones", segmental_predictions, raw_segmental_predictions),
        "tonal": metrics("pron_with_tones", tonal_predictions, raw_tonal_predictions),
        "unexpected_errors": errors,
        "latency_ms": {
            "segmental_mean": statistics.mean(segmental_times) if segmental_times else None,
            "segmental_p95": sorted(segmental_times)[min(len(segmental_times)-1, int(0.95 * len(segmental_times)))] if segmental_times else None,
            "tonal_mean": statistics.mean(tonal_times) if tonal_times else None,
            "tonal_p95": sorted(tonal_times)[min(len(tonal_times)-1, int(0.95 * len(tonal_times)))] if tonal_times else None,
        },
    }


def has_runtime_errors(results: list[dict[str, object]]) -> bool:
    """Make unexpected per-input comparator failures fail the benchmark job."""
    return any(int(result.get("unexpected_errors", 0)) > 0 for result in results)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows, data_sha = load_rows()
    results: list[dict[str, object]] = []

    import epitran
    epi_segmental = epitran.Epitran("lao-Laoo", tones=False)
    epi_tonal = epitran.Epitran("lao-Laoo", tones=True)

    def epitran_predict(text: str):
        started = time.perf_counter()
        segmental = epi_segmental.transliterate(text)
        segmental_ms = (time.perf_counter() - started) * 1000
        started = time.perf_counter()
        tonal = epi_tonal.transliterate(text)
        tonal_ms = (time.perf_counter() - started) * 1000
        return segmental, tonal, segmental_ms, tonal_ms

    results.append(run_engine("Epitran lao-Laoo (tones=False/True)", epitran_predict, rows))

    import orthography2ipa
    def o2i_predict(text: str):
        started = time.perf_counter()
        tonal = orthography2ipa.transcribe(text, "lo")
        elapsed = (time.perf_counter() - started) * 1000
        if not isinstance(tonal, str):
            raise TypeError("orthography2ipa.transcribe did not return a string")
        return no_tones(tonal), tonal, elapsed, elapsed

    results.append(run_engine("orthography2ipa lo spec", o2i_predict, rows))

    # Transphone is a multilingual supervised G2P model. Lao (ISO 639-3: lao)
    # is explicitly listed in its supervised evaluation table. Use the model
    # directly, not its lexicon tokenizer, to avoid lexical leakage.
    from transphone.g2p import read_g2p
    transphone_model = read_g2p(model_name="latest", device="cpu")
    if "lao" not in transphone_model.supervised_langs:
        raise RuntimeError("Transphone model does not contain supervised Lao; refusing zero-shot fallback")
    transphone_checkpoint_sha256 = hashlib.sha256(
        Path(transphone_model.checkpoint).read_bytes()
    ).hexdigest()

    def transphone_predict(text: str):
        started = time.perf_counter()
        phones = transphone_model.inference_word_batch(
            text, lang_id="lao", num_lang=1, force_approximate=False
        )
        elapsed = (time.perf_counter() - started) * 1000
        if not phones:
            raise ValueError("Transphone returned an empty IPA sequence")
        tonal = "".join(phones)
        return no_tones(tonal), tonal, elapsed, elapsed

    results.append(run_engine("Transphone 1.5.3 supervised Lao G2P", transphone_predict, rows))

    report = {
        "schema_version": "1.0",
        "benchmark": "MekongPhon 100-entry held-out lexicon, source-attested comparison only",
        "accuracy_claim": None,
        "independent_expert_gold_count": 0,
        "provenance": {
            "dataset_url": DATA_URL,
            "dataset_revision": "f80f6c1840c4818b51e05f2e00cded4701a5b662",
            "dataset_sha256": data_sha,
            "rows": len(rows),
            "python": platform.python_version(),
            "epitran_version": importlib.metadata.version("epitran"),
            "epitran_lao_map_sha256": package_file_sha256("epitran", "data/map/lao-Laoo.csv"),
            "orthography2ipa_version": importlib.metadata.version("orthography2ipa"),
            "orthography2ipa_commit": O2I_COMMIT,
            "orthography2ipa_lo_spec_sha256": package_file_sha256("orthography2ipa", "data/lo.json"),
            "transphone_version": importlib.metadata.version("transphone"),
            "transphone_upstream_commit": "7769dec083b90dab072fc7e4c592744592a35736",
            "transphone_model_release": "v1.0/latest.tar.gz",
            "transphone_checkpoint_sha256": transphone_checkpoint_sha256,
            "transphone_language_mode": "supervised Lao; zero-shot fallback explicitly rejected",
            "normalization": "NFC; trim outer whitespace only; no tone/length/tie-bar normalization for tonal score",
        },
        "results": results,
        "interpretation": (
            "All scores are concordance with the pinned MekongPhon dictionary-seeded reference, "
            "not accuracy or independent gold. Segmental and tonal references are scored separately. "
            "The external comparators are research baselines only; none is promoted to production."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
    args.output.with_suffix(args.output.suffix + ".sha256").write_text(
        f"{digest}  {args.output.name}\n", encoding="utf-8"
    )
    print(json.dumps({
        "output": str(args.output),
        "sha256": digest,
        "results": results,
        "accuracy_claim": None,
    }, ensure_ascii=False, indent=2))
    return 1 if has_runtime_errors(results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
