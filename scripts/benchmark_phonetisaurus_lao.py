#!/usr/bin/env python3
"""Ephemeral Phonetisaurus Lao FST probe; never stores model or predictions."""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import platform
import statistics
import subprocess
import tempfile
import time
import unicodedata
import urllib.request
from pathlib import Path

DATA_URL = (
    "https://raw.githubusercontent.com/byu-matrix-lab/MekongPhon/"
    "f80f6c1840c4818b51e05f2e00cded4701a5b662/data/splits/lao_eval.csv"
)
MODEL_URL = (
    "https://raw.githubusercontent.com/uiuc-sst/g2ps/"
    "ce8d8d83d46da10909e2ee4227e89a70ceaa7a7c/models/lao_2_2_2.fst.gz"
)
MODEL_REPOSITORY_REVISION = "ce8d8d83d46da10909e2ee4227e89a70ceaa7a7c"
MODEL_GIT_BLOB_SHA1 = "8b598b3587adbc65107ca86b700200f20ccaea26"
DOCKER_IMAGE = "phonetisaurus/phonetisaurus@sha256:6b1f0dce451bc84841c639cf0263b3d4d2232d221fef2c07b1837a8aec955fd2"


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


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "ClippyFirst-Lao-G2P-benchmark/1.0"})
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.read()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    started = time.perf_counter()
    status = "BLOCKED"
    error = None
    metrics = None
    model_sha256 = None
    model_size = 0
    row_count = 0

    try:
        payload = download(DATA_URL)
        data_sha256 = hashlib.sha256(payload).hexdigest()
        rows = list(csv.DictReader(payload.decode("utf-8-sig").splitlines()))
        required = {"orth", "pron_no_tones", "pron_with_tones"}
        if len(rows) != 100 or not rows or not required.issubset(rows[0]):
            raise ValueError("Unexpected MekongPhon held-out dataset schema or row count")
        if len({row["orth"] for row in rows}) != 100:
            raise ValueError("Duplicate orthographies in held-out split")
        row_count = len(rows)

        compressed = download(MODEL_URL)
        blob_sha1 = hashlib.sha1(
            f"blob {len(compressed)}\0".encode("ascii") + compressed
        ).hexdigest()
        if blob_sha1 != MODEL_GIT_BLOB_SHA1:
            raise ValueError(f"LanguageNet model Git blob SHA mismatch: {blob_sha1}")
        model = gzip.decompress(compressed)
        model_sha256 = hashlib.sha256(model).hexdigest()
        model_size = len(model)

        with tempfile.TemporaryDirectory(prefix="phonetisaurus-lao-") as tmp:
            root = Path(tmp)
            (root / "lao.fst").write_bytes(model)
            (root / "words.txt").write_text(
                "\n".join(row["orth"] for row in rows) + "\n", encoding="utf-8"
            )
            command = [
                "docker", "run", "--rm",
                "-v", f"{root}:/work",
                "-w", "/work",
                DOCKER_IMAGE,
                "phonetisaurus-apply",
                "--model", "/work/lao.fst",
                "--word_list", "/work/words.txt",
                "--nbest", "1",
            ]
            result = subprocess.run(
                command, check=False, capture_output=True, text=True, timeout=300
            )
            if result.returncode != 0:
                raise RuntimeError(
                    f"Phonetisaurus exited {result.returncode}: "
                    f"{(result.stderr or result.stdout)[-2500:]}"
                )
            predictions: dict[str, str] = {}
            for line in result.stdout.splitlines():
                parts = line.strip().split()
                if len(parts) < 2:
                    continue
                word = parts[0]
                phone_parts = parts[1:]
                if phone_parts and _is_float(phone_parts[0]):
                    phone_parts = phone_parts[1:]
                if word in {row["orth"] for row in rows} and phone_parts:
                    predictions[word] = nfc("".join(phone_parts))

        references = [nfc(row["pron_no_tones"]) for row in rows]
        outputs = [predictions.get(row["orth"], "") for row in rows]
        edits = sum(levenshtein(ref, pred) for ref, pred in zip(references, outputs))
        ref_chars = sum(len(ref) for ref in references)
        exact = sum(ref == pred for ref, pred in zip(references, outputs))
        covered = sum(bool(pred) for pred in outputs)
        covered_pairs = [(ref, pred) for ref, pred in zip(references, outputs) if pred]
        covered_edits = sum(levenshtein(ref, pred) for ref, pred in covered_pairs)
        covered_chars = sum(len(ref) for ref, _ in covered_pairs)
        elapsed_ms = (time.perf_counter() - started) * 1000
        metrics = {
            "reference": "pron_no_tones",
            "n": len(rows),
            "exact": exact,
            "exact_rate": exact / len(rows),
            "cer_full_denominator": edits / ref_chars if ref_chars else None,
            "coverage": covered / len(rows),
            "missing": len(rows) - covered,
            "covered_subset_cer": covered_edits / covered_chars if covered_chars else None,
            "batch_elapsed_ms_including_download_and_docker_start": elapsed_ms,
            "mean_elapsed_ms_per_input_including_startup": elapsed_ms / len(rows),
            "output_lines_parsed": len(predictions),
        }
        status = "OK"
        data_sha = data_sha256
    except Exception as exc:
        status = "BLOCKED"
        error = f"{type(exc).__name__}: {exc}"
        data_sha = None

    report = {
        "schema_version": "1.0",
        "engine": "LanguageNet Phonetisaurus Lao FST",
        "status": status,
        "accuracy_claim": None,
        "tonal_score": None,
        "interpretation": (
            "The LanguageNet model is an untuned, segmental G2P comparator. "
            "MekongPhon references are dictionary-seeded source-attested IPA, not independent expert gold. "
            "The model is downloaded and decompressed in a temporary directory; neither model nor predictions are retained."
        ),
        "provenance": {
            "dataset_url": DATA_URL,
            "dataset_revision": "f80f6c1840c4818b51e05f2e00cded4701a5b662",
            "dataset_sha256": data_sha,
            "rows": row_count,
            "model_url": MODEL_URL,
            "model_repository_revision": MODEL_REPOSITORY_REVISION,
            "model_git_blob_sha1": MODEL_GIT_BLOB_SHA1,
            "decompressed_model_sha256": model_sha256,
            "decompressed_model_bytes": model_size,
            "docker_image": DOCKER_IMAGE,
            "python": platform.python_version(),
        },
        "segmental": metrics,
        "error": error,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    args.output.write_text(encoded, encoding="utf-8")
    digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
    args.output.with_suffix(args.output.suffix + ".sha256").write_text(
        f"{digest}  {args.output.name}\n", encoding="utf-8"
    )
    print(encoded)
    return 0 if status == "OK" else 0


def _is_float(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    raise SystemExit(main())
