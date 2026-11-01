#!/usr/bin/env python3
"""Run a pinned, optional Goruut HTTP phonemizer probe.

This records raw responses only. It does not score accuracy, normalize IPA,
or treat project fixtures/source-attested transcriptions as gold.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_inputs(path: Path) -> list[str]:
    values = [
        line.rstrip("\r\n")
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not values:
        raise ValueError(f"No probe inputs found in {path}")
    return values


def extract_phonetics(payload: Any) -> list[str]:
    if not isinstance(payload, dict) or not isinstance(payload.get("Words"), list):
        raise ValueError("Response must be an object containing a Words array")
    if not payload["Words"]:
        raise ValueError("Words array must not be empty")
    phonetics: list[str] = []
    for index, word in enumerate(payload["Words"]):
        if not isinstance(word, dict) or not isinstance(word.get("Phonetic"), str):
            raise ValueError(f"Words[{index}] must contain a string Phonetic field")
        phonetics.append(word["Phonetic"])
    if not any(value.strip() for value in phonetics):
        raise ValueError("Response contains no non-empty phonetic output")
    return phonetics


def request_phonemization(base_url: str, language: str, text: str, timeout: float) -> tuple[str, list[str]]:
    body = json.dumps({"Language": language, "Sentence": text}, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        base_url.rstrip("/") + "/tts/phonemize/sentence",
        data=body,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read().decode("utf-8", errors="replace")
    payload = json.loads(raw)
    return raw, extract_phonetics(payload)


def run_probe(base_url: str, language: str, text: str, timeout: float, attempts: int) -> dict[str, Any]:
    last_error = None
    for attempt in range(attempts):
        try:
            raw, phonetics = request_phonemization(base_url, language, text, timeout)
            return {
                "input": text,
                "status": "OK",
                "raw_response": raw,
                "phonetic_tokens": phonetics,
                "error": None,
            }
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError, OSError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt + 1 < attempts:
                time.sleep(min(2 ** attempt, 8))
    return {
        "input": text,
        "status": "ERROR",
        "raw_response": None,
        "phonetic_tokens": None,
        "error": last_error,
    }


def build_report(
    inputs: list[str],
    records: list[dict[str, Any]],
    *,
    language: str,
    engine_commit: str,
    input_path: Path,
    input_sha256: str,
    base_url: str,
) -> dict[str, Any]:
    successes = sum(record["status"] == "OK" for record in records)
    failures = len(records) - successes
    return {
        "schema_version": 1,
        "purpose": "Optional runtime availability and raw-output probe; not an accuracy benchmark.",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "engine": "Goruut",
        "engine_commit": engine_commit,
        "language_identifier": language,
        "api_endpoint": base_url.rstrip("/") + "/tts/phonemize/sentence",
        "python_version": platform.python_version(),
        "input_path": str(input_path),
        "input_sha256": input_sha256,
        "input_count": len(inputs),
        "successful_outputs": successes,
        "failed_outputs": failures,
        "independent_gold_count": 0,
        "accuracy": None,
        "score_status": "NOT_SCORED_NO_INDEPENDENT_GOLD",
        "normalization": "None. Raw HTTP response and phonetic tokens are preserved; no IPA normalization is performed.",
        "interpretation": "A successful response demonstrates only that this pinned binary answered this probe. It does not validate the phonetic correctness, dialect, IPA convention, completeness, or suitability of the output.",
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--language", choices=("Lao", "KhmerCentral", "Burmese"), required=True)
    parser.add_argument("--engine-commit", required=True)
    parser.add_argument("--base-url", default="http://127.0.0.1:18080")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--attempts", type=int, default=4)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.timeout <= 0 or args.attempts < 1:
        parser.error("--timeout must be positive and --attempts must be at least 1")

    inputs = load_inputs(args.input)
    records = [
        run_probe(args.base_url, args.language, text, args.timeout, args.attempts)
        for text in inputs
    ]
    report = build_report(
        inputs,
        records,
        language=args.language,
        engine_commit=args.engine_commit,
        input_path=args.input,
        input_sha256=sha256_file(args.input),
        base_url=args.base_url,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in (
        "engine", "engine_commit", "language_identifier", "input_count",
        "successful_outputs", "failed_outputs", "independent_gold_count",
        "accuracy", "score_status"
    )}, ensure_ascii=False, indent=2))
    print(f"Raw-output report: {args.output}")
    return 0 if report["failed_outputs"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
