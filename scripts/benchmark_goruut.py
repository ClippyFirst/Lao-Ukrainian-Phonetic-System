#!/usr/bin/env python3
"""Run a pinned, optional Goruut HTTP phonemizer probe.

This records raw responses only. It does not score accuracy, normalize IPA,
or treat project fixtures/source-attested transcriptions as gold.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import time
import unicodedata
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


def load_inputs(
    path: Path,
    *,
    input_format: str = "lines",
    text_column: str = "orth",
    expected_column: str | None = None,
) -> list[dict[str, str | None]]:
    if input_format == "csv":
        with path.open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream)
            if not reader.fieldnames or text_column not in reader.fieldnames:
                raise ValueError(f"CSV is missing text column {text_column!r}")
            if expected_column and expected_column not in reader.fieldnames:
                raise ValueError(f"CSV is missing expected column {expected_column!r}")
            values = []
            for row in reader:
                text = (row.get(text_column) or "").strip()
                if not text:
                    continue
                expected = (row.get(expected_column) or "").strip() if expected_column else ""
                values.append({"text": text, "source_attested_ipa": expected or None})
    else:
        values = [
            {"text": line.rstrip("\r\n"), "source_attested_ipa": None}
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
    if not values:
        raise ValueError(f"No probe inputs found in {path}")
    return values

def notation_comparison_key(value: str) -> str:
    """Remove only outer IPA slashes, whitespace, syllable dots and stress marks.

    Phone symbols, aspiration, length, tone, diacritics and tie bars remain intact.
    This is a notation diagnostic, not a phonological normalization.
    """
    value = value.strip()
    if len(value) >= 2 and value.startswith("/") and value.endswith("/"):
        value = value[1:-1]
    value = unicodedata.normalize("NFC", value)
    return "".join(char for char in value if not char.isspace() and char not in {".", "ˈ", "ˌ"})


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


def analyze_source_coverage(payload: Any, input_text: str) -> dict[str, Any]:
    """Detect source letters left in punctuation fields or omitted from the response."""
    if not isinstance(payload, dict) or not isinstance(payload.get("Words"), list):
        raise ValueError("Response must contain Words to inspect source coverage")
    reconstructed_parts: list[str] = []
    unphonemized: list[dict[str, Any]] = []
    empty_phonetic_word_indices: list[int] = []
    for index, word in enumerate(payload["Words"]):
        if not isinstance(word, dict):
            raise ValueError(f"Words[{index}] must be an object")
        values = {}
        for field in ("PrePunct", "CleanWord", "PostPunct"):
            value = word.get(field, "")
            if value is None:
                value = ""
            if not isinstance(value, str):
                raise ValueError(f"Words[{index}].{field} must be a string")
            values[field] = value
        reconstructed_parts.append(
            values["PrePunct"] + values["CleanWord"] + values["PostPunct"]
        )
        phonetic = word.get("Phonetic")
        if isinstance(phonetic, str) and not phonetic.strip():
            empty_phonetic_word_indices.append(index)
        for field in ("PrePunct", "PostPunct"):
            value = values[field]
            if any(unicodedata.category(char)[0] in "LMN" for char in value):
                unphonemized.append({
                    "word_index": index,
                    "field": field,
                    "text": value,
                })
    reconstructed = "".join(reconstructed_parts)
    def compact_source(value: str) -> str:
        return unicodedata.normalize(
            "NFC", "".join(char for char in value if not char.isspace())
        )

    reconstruction_matches = compact_source(reconstructed) == compact_source(input_text)
    return {
        "source_reconstructed_text": reconstructed,
        "source_reconstruction_matches_input": reconstruction_matches,
        "source_coverage_complete": reconstruction_matches and not unphonemized and not empty_phonetic_word_indices,
        "unphonemized_source_fragments": unphonemized,
        "empty_phonetic_word_indices": empty_phonetic_word_indices,
        "source_coverage_error": None,
    }


def request_raw_response(base_url: str, language: str, text: str, timeout: float) -> str:
    body = json.dumps({"Language": language, "Sentence": text}, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        base_url.rstrip("/") + "/tts/phonemize/sentence",
        data=body,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read().decode("utf-8", errors="replace")
    return raw


def run_probe_once(
    base_url: str, language: str, text: str, timeout: float, attempts: int
) -> dict[str, Any]:
    last_error = None
    for attempt in range(attempts):
        try:
            raw = request_raw_response(base_url, language, text, timeout)
            try:
                payload = json.loads(raw)
                phonetics = extract_phonetics(payload)
            except (json.JSONDecodeError, ValueError) as exc:
                return {
                    "status": "NO_PHONETIC_OUTPUT",
                    "raw_response": raw,
                    "phonetic_tokens": None,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            randomization_count = payload.get("RandomizationWordsCount", 0)
            randomization_choices = payload.get("RandomizationWordsChoices", 0)
            if type(randomization_count) is not int or randomization_count < 0:
                randomization_count = None
            if type(randomization_choices) is not int or randomization_choices < 0:
                randomization_choices = None
            try:
                source_coverage = analyze_source_coverage(payload, text)
            except ValueError as exc:
                source_coverage = {
                    "source_reconstructed_text": None,
                    "source_reconstruction_matches_input": None,
                    "source_coverage_complete": None,
                    "unphonemized_source_fragments": [],
                    "source_coverage_error": f"{type(exc).__name__}: {exc}",
                }
            return {
                "status": "OK",
                "raw_response": raw,
                "phonetic_tokens": phonetics,
                "randomization_words_count": randomization_count,
                "randomization_words_choices": randomization_choices,
                **source_coverage,
                "error": None,
            }
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            return {
                "status": "HTTP_ERROR",
                "raw_response": raw,
                "phonetic_tokens": None,
                "error": f"HTTPError: {exc.code} {exc.reason}",
            }
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt + 1 < attempts:
                time.sleep(min(2 ** attempt, 8))
    return {
        "status": "TRANSPORT_ERROR",
        "raw_response": None,
        "phonetic_tokens": None,
        "error": last_error,
    }


def run_probe(
    base_url: str,
    language: str,
    text: str,
    timeout: float,
    attempts: int,
    repeat_count: int = 1,
) -> dict[str, Any]:
    repetitions = [
        run_probe_once(base_url, language, text, timeout, attempts)
        for _ in range(repeat_count)
    ]
    successful = [item for item in repetitions if item["status"] == "OK"]
    unique_outputs = {
        tuple(item["phonetic_tokens"] or [])
        for item in successful
    }
    first = successful[0] if successful else repetitions[0]
    all_successful = len(successful) == repeat_count
    reproducible = all_successful and len(unique_outputs) == 1
    unstable = len(unique_outputs) > 1
    status = "OK" if all_successful else (
        "PARTIAL_REPETITIONS" if successful else repetitions[0]["status"]
    )
    errors = [
        f"repeat {index + 1}: {item['error']}"
        for index, item in enumerate(repetitions)
        if item["error"]
    ]
    randomization_counts = [
        item.get("randomization_words_count")
        for item in repetitions
        if isinstance(item.get("randomization_words_count"), int)
        and not isinstance(item.get("randomization_words_count"), bool)
    ]
    randomization_choices = [
        item.get("randomization_words_choices")
        for item in repetitions
        if isinstance(item.get("randomization_words_choices"), int)
        and not isinstance(item.get("randomization_words_choices"), bool)
    ]
    randomized_repetitions = sum(value > 0 for value in randomization_counts)
    coverage_values = [item.get("source_coverage_complete") for item in successful]
    if not successful:
        source_coverage_status = "UNKNOWN"
    elif any(value is False for value in coverage_values) or len(successful) < repeat_count:
        source_coverage_status = "PARTIAL"
    elif all(value is True for value in coverage_values):
        source_coverage_status = "COMPLETE"
    else:
        source_coverage_status = "UNKNOWN"
    fragments_by_key = {}
    empty_phonetic_indices = set()
    for item in successful:
        for fragment in item.get("unphonemized_source_fragments", []):
            key = (fragment["word_index"], fragment["field"], fragment["text"])
            fragments_by_key[key] = fragment
        empty_phonetic_indices.update(item.get("empty_phonetic_word_indices", []))
    return {
        "input": text,
        "status": status,
        "source_coverage_status": source_coverage_status,
        "source_coverage_complete": source_coverage_status == "COMPLETE",
        "source_coverage_reconstruction_matches_input": (
            len(successful) == repeat_count
            and all(item.get("source_reconstruction_matches_input") is True for item in successful)
        ),
        "source_coverage_partial_repetitions": sum(value is False for value in coverage_values),
        "source_coverage_unknown_repetitions": repeat_count - sum(value is not None for value in coverage_values),
        "unphonemized_source_fragments": list(fragments_by_key.values()),
        "empty_phonetic_word_indices": sorted(empty_phonetic_indices),
        "randomization_words_count_max": max(randomization_counts, default=0),
        "randomization_words_choices_max": max(randomization_choices, default=0),
        "randomized_repetitions": randomized_repetitions,
        "ambiguous_dictionary_selection": randomized_repetitions > 0,
        "raw_response": first["raw_response"],
        "phonetic_tokens": first["phonetic_tokens"],
        "error": "; ".join(errors) if errors else None,
        "repetitions": [
            {"repeat": index + 1, **item}
            for index, item in enumerate(repetitions)
        ],
        "successful_repetitions": len(successful),
        "failed_repetitions": repeat_count - len(successful),
        "reproducible": reproducible,
        "unstable": unstable,
    }

def build_report(
    inputs: list[dict[str, str | None]],
    records: list[dict[str, Any]],
    *,
    language: str,
    engine_commit: str,
    input_path: Path,
    input_sha256: str,
    base_url: str,
    config_path: Path,
    config_sha256: str,
    runtime_version: str,
    server_log_path: Path | None = None,
) -> dict[str, Any]:
    normalized_inputs = [item if isinstance(item, dict) else {"text": str(item), "source_attested_ipa": None} for item in inputs]
    successes = sum(record["status"] in ("OK", "PARTIAL_REPETITIONS") for record in records)
    failures = len(records) - successes
    reproducible_outputs = sum(record.get("reproducible") is True for record in records)
    unstable_outputs = sum(record.get("unstable") is True for record in records)
    partial_repeat_cases = sum(record.get("status") == "PARTIAL_REPETITIONS" for record in records)
    repeat_count = max((len(record.get("repetitions", [])) for record in records), default=1)
    randomized_input_count = sum(record.get("ambiguous_dictionary_selection") is True for record in records)
    randomized_repetition_count = sum(record.get("randomized_repetitions", 0) or 0 for record in records)
    unstable_randomized_input_count = sum(
        record.get("unstable") is True and record.get("ambiguous_dictionary_selection") is True
        for record in records
    )
    source_coverage_complete_outputs = sum(record.get("source_coverage_status") == "COMPLETE" for record in records)
    source_coverage_partial_outputs = sum(record.get("source_coverage_status") == "PARTIAL" for record in records)
    source_coverage_unknown_outputs = sum(record.get("source_coverage_status", "UNKNOWN") == "UNKNOWN" for record in records)
    unphonemized_source_fragment_count = sum(len(record.get("unphonemized_source_fragments", [])) for record in records)
    empty_phonetic_word_count = sum(len(record.get("empty_phonetic_word_indices", [])) for record in records)
    comparisons = []
    notation_comparisons = []
    for item, record in zip(normalized_inputs, records, strict=True):
        expected = item.get("source_attested_ipa")
        repetitions = record.get("repetitions") or [{
            "status": record["status"],
            "phonetic_tokens": record.get("phonetic_tokens"),
            "source_coverage_complete": record.get("source_coverage_complete"),
        }]
        actual_outputs = [
            "".join(item.get("phonetic_tokens") or [])
            for item in repetitions
            if item.get("status") == "OK" and item.get("source_coverage_complete") is True
        ]
        actual = actual_outputs[0] if actual_outputs else None
        repeat_matches = [
            unicodedata.normalize("NFC", value.strip()) == unicodedata.normalize("NFC", expected.strip())
            for value in actual_outputs
        ] if expected is not None else []
        notation_matches = [notation_comparison_key(value) == notation_comparison_key(expected) for value in actual_outputs] if expected is not None else []
        match = bool(repeat_matches) and len(repeat_matches) == len(repetitions) and all(repeat_matches)
        notation_match = bool(notation_matches) and len(notation_matches) == len(repetitions) and all(notation_matches)
        if expected is None:
            match = None
            notation_match = None
        record["source_attested_ipa"] = expected
        record["phonetic_concatenated"] = actual
        record["source_attested_matches"] = repeat_matches
        record["source_attested_match"] = match
        record["source_attested_notation_match"] = notation_match
        if expected is not None:
            comparisons.append(match)
            notation_comparisons.append(notation_match)
    source_attested_diagnostic = None
    if comparisons:
        source_attested_diagnostic = {
            "eligible_source_attested_rows": len(comparisons),
            "exact_matches": sum(value is True for value in comparisons),
            "notation_normalized_matches": sum(value is True for value in notation_comparisons),
            "notation_normalized_match_rate": sum(value is True for value in notation_comparisons) / len(notation_comparisons),
            "any_repeat_exact_matches": sum(bool(record.get("source_attested_matches")) and any(record.get("source_attested_matches", [])) for record in records),
            "unstable_cases": unstable_outputs,
            "mismatches_or_missing_outputs": sum(value is False or value is None for value in comparisons),
            "match_rate": sum(value is True for value in comparisons) / len(comparisons),
            "status": "SOURCE_ATTESTED_CONCORDANCE_ONLY_NOT_GOLD",
            "normalization": "Strict: NFC and outer whitespace only. Secondary notation diagnostic: also removes outer /.../ wrappers, whitespace, syllable dots and ˈ/ˌ only; tone, length, phone symbols, aspiration, diacritics and tie bars remain significant.",
            "coverage_gate": "Only repetitions with complete source coverage are compared; source letters/numbers in PrePunct/PostPunct or a source reconstruction mismatch exclude that repetition.",
        }
    log_text = server_log_path.read_text(encoding="utf-8", errors="replace") if server_log_path and server_log_path.exists() else ""
    model_asset_warnings = sorted({line.strip() for line in log_text.splitlines() if "weights" in line.lower() and ("does not exist" in line.lower() or "not found" in line.lower())})
    return {
        "schema_version": 1,
        "purpose": "Optional runtime availability and raw-output probe; not an accuracy benchmark.",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "engine": "Goruut",
        "engine_commit": engine_commit,
        "language_identifier": language,
        "api_endpoint": base_url.rstrip("/") + "/tts/phonemize/sentence",
        "python_version": platform.python_version(),
        "go_runtime_version": runtime_version,
        "effective_config_path": str(config_path),
        "effective_config_sha256": config_sha256,
        "server_log_path": str(server_log_path) if server_log_path else None,
        "server_log_sha256": sha256_file(server_log_path) if server_log_path and server_log_path.exists() else None,
        "model_asset_warnings": model_asset_warnings,
        "input_path": str(input_path),
        "input_sha256": input_sha256,
        "input_count": len(inputs),
        "repeat_count": repeat_count,
        "reproducible_outputs": reproducible_outputs,
        "unstable_outputs": unstable_outputs,
        "randomized_input_count": randomized_input_count,
        "randomized_repetition_count": randomized_repetition_count,
        "unstable_randomized_input_count": unstable_randomized_input_count,
        "source_coverage_complete_outputs": source_coverage_complete_outputs,
        "source_coverage_partial_outputs": source_coverage_partial_outputs,
        "source_coverage_unknown_outputs": source_coverage_unknown_outputs,
        "unphonemized_source_fragment_count": unphonemized_source_fragment_count,
        "empty_phonetic_word_count": empty_phonetic_word_count,
        "partial_repeat_cases": partial_repeat_cases,
        "source_attested_diagnostic": source_attested_diagnostic,
        "successful_outputs": successes,
        "failed_outputs": failures,
        "independent_gold_count": 0,
        "accuracy": None,
        "score_status": "NOT_SCORED_NO_INDEPENDENT_GOLD",
        "normalization": "No IPA normalization. Source-coverage reconstruction uses NFC and ignores whitespace only; raw HTTP responses and phone strings are preserved.",
        "source_coverage_contract": "A response is complete only when PrePunct + CleanWord + PostPunct reconstructs the input after NFC/whitespace removal, no letters/marks/numbers remain in PrePunct or PostPunct, and every phonetic word token is non-empty.",
        "interpretation": "A successful response demonstrates only that this pinned binary answered this probe. It does not validate the phonetic correctness, dialect, IPA convention, completeness, or suitability of the output.",
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--input-format", choices=("lines", "csv"), default="lines")
    parser.add_argument("--text-column", default="orth")
    parser.add_argument("--expected-column", default=None)
    parser.add_argument("--language", choices=("Lao", "KhmerCentral", "Burmese"), required=True)
    parser.add_argument("--engine-commit", required=True)
    parser.add_argument("--base-url", default="http://127.0.0.1:18080")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--attempts", type=int, default=4)
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--config-file", type=Path, required=True)
    parser.add_argument("--runtime-version", required=True)
    parser.add_argument("--server-log", type=Path, default=None)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.timeout <= 0 or args.attempts < 1 or args.repeat < 1:
        parser.error("--timeout must be positive; --attempts and --repeat must be at least 1")

    inputs = load_inputs(args.input, input_format=args.input_format, text_column=args.text_column, expected_column=args.expected_column)
    records = [
        run_probe(args.base_url, args.language, str(item["text"]), args.timeout, args.attempts, args.repeat)
        for item in inputs
    ]
    report = build_report(
        inputs,
        records,
        language=args.language,
        engine_commit=args.engine_commit,
        input_path=args.input,
        input_sha256=sha256_file(args.input),
        base_url=args.base_url,
        config_path=args.config_file,
        config_sha256=sha256_file(args.config_file),
        runtime_version=args.runtime_version,
        server_log_path=args.server_log,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in (
        "engine", "engine_commit", "language_identifier", "go_runtime_version",
        "effective_config_sha256", "server_log_sha256", "model_asset_warnings",
        "input_count", "repeat_count", "reproducible_outputs", "unstable_outputs",
        "partial_repeat_cases", "source_attested_diagnostic",
        "successful_outputs", "failed_outputs", "randomized_input_count",
        "randomized_repetition_count", "unstable_randomized_input_count",
        "source_coverage_complete_outputs", "source_coverage_partial_outputs",
        "source_coverage_unknown_outputs", "unphonemized_source_fragment_count",
        "empty_phonetic_word_count", "independent_gold_count", "accuracy", "score_status"
    )}, ensure_ascii=False, indent=2))
    print(f"Raw-output report: {args.output}")
    # Partial coverage is a valid diagnostic result: failures remain explicit in the artifact.
    # Fail CI only when the engine produced no usable phonetic output at all.
    return 0 if report["successful_outputs"] > 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
