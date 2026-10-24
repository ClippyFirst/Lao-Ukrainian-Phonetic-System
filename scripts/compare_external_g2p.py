#!/usr/bin/env python3
"""Compare this project's Lao→IPA output with lao2ipa and fixture expectations.

Run from the repository root after installing the project and lao2ipa==1.0.0:
    python -m pip install -e .
    python -m pip install lao2ipa==1.0.0
    python scripts/compare_external_g2p.py

This is a comparative diagnostic, not a gold-standard accuracy evaluation.
"""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import sys
import unicodedata
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE = ROOT / "tests" / "fixtures" / "vowel_precedence_cases.json"
DEFAULT_OUTPUT = ROOT / "artifacts" / "external-g2p-comparison.json"


def nfc(value: str | None) -> str | None:
    """Normalize Unicode canonically without deleting IPA marks or separators."""
    if value is None:
        return None
    return unicodedata.normalize("NFC", value)



def build_summary(results: list[dict[str, Any]], expected_count: int) -> dict[str, Any]:
    """Summarize diagnostic agreement without presenting it as accuracy."""
    matches = sum(row.get("exact_match") is True for row in results)
    project_fixture_matches = sum(row.get("project_matches_fixture") is True for row in results)
    external_fixture_matches = sum(row.get("external_matches_fixture") is True for row in results)
    runtime_errors = sum(row.get("mismatch_category") == "RUNTIME_ERROR" for row in results)
    cases = len(results)
    return {
        "cases": cases,
        "expected_ipa_cases": expected_count,
        "project_fixture_matches": project_fixture_matches,
        "external_fixture_matches": external_fixture_matches,
        "exact_matches_between_implementations": matches,
        "implementation_mismatches": sum(
            row.get("exact_match") is False and row.get("mismatch_category") != "RUNTIME_ERROR"
            for row in results
        ),
        "runtime_errors": runtime_errors,
        "implementation_agreement_rate": matches / cases if cases else None,
        "independent_gold_count": 0,
        "accuracy": None,
        "score_status": "NOT_SCORED_NO_INDEPENDENT_GOLD",
        "note": (
            "Implementation agreement and fixture matches are diagnostic only. "
            "The engineering fixture is not independent gold; accuracy is null."
        ),
    }


def project_ipa(surface: str) -> str | None:
    # Import locally so --help can run without the project installed.
    from lao_ukrainian.core import analyze

    result = analyze(surface)
    if not result.syllables:
        return None
    values = [item.phonemic_ipa for item in result.syllables]
    if any(value is None for value in values):
        return None
    return " ".join(str(value) for value in values)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    try:
        from lao2ipa import transliterate
    except ImportError:
        print(
            "Missing optional dependency. Install with: python -m pip install lao2ipa==1.0.0",
            file=sys.stderr,
        )
        return 2

    fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
    cases = fixture.get("cases")
    if not isinstance(cases, list) or not cases:
        parser.error(f"Fixture contains no cases: {args.fixture}")

    results: list[dict[str, Any]] = []
    for case in cases:
        surface = case["surface"]
        expected = nfc(case.get("phonemic_ipa"))
        row: dict[str, Any] = {
            "id": case.get("id"),
            "surface": surface,
            "fixture_expected_ipa": expected,
        }
        try:
            local_raw = project_ipa(surface)
            external_raw = transliterate(surface, output="ipa")
            if not isinstance(external_raw, str):
                raise TypeError(
                    f"lao2ipa returned {type(external_raw).__name__}, expected str"
                )
            local = nfc(local_raw)
            external = nfc(external_raw)
            row.update(
                {
                    "project_ipa_raw": local_raw,
                    "external_ipa_raw": external_raw,
                    "project_ipa_nfc": local,
                    "external_ipa_nfc": external,
                    "project_matches_fixture": expected is not None and local == expected,
                    "external_matches_fixture": expected is not None and external == expected,
                    "exact_match": local == external,
                    "mismatch_category": None if local == external else "UNCLASSIFIED_REQUIRES_REVIEW",
                }
            )
        except Exception as exc:  # keep per-case failures visible in the artifact
            row.update(
                {
                    "project_ipa_raw": None,
                    "external_ipa_raw": None,
                    "project_ipa_nfc": None,
                    "external_ipa_nfc": None,
                    "project_matches_fixture": False,
                    "external_matches_fixture": False,
                    "exact_match": False,
                    "mismatch_category": "RUNTIME_ERROR",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
        results.append(row)

    try:
        external_version = importlib.metadata.version("lao2ipa")
    except importlib.metadata.PackageNotFoundError:
        external_version = "unknown"

    expected_count = sum(row.get("fixture_expected_ipa") is not None for row in results)
    summary = build_summary(results, expected_count)
    report = {
        "schema_version": 3,
        "purpose": "Comparative diagnostic only; neither implementation nor the engineering fixture is treated as an independent gold standard.",
        "independent_gold_count": 0,
        "accuracy": None,
        "score_status": "NOT_SCORED_NO_INDEPENDENT_GOLD",
        "fixture_path": str(args.fixture.relative_to(ROOT)) if args.fixture.is_relative_to(ROOT) else str(args.fixture),
        "fixture_schema_version": fixture.get("schema_version"),
        "fixture_purpose": fixture.get("purpose"),
        "unicode_normalization": "NFC only; no IPA marks, tone marks, length marks, or separators are removed.",
        "project": {
            "name": "Lao-Ukrainian-Phonetic-System",
            "ipa_source": "lao_ukrainian.core.analyze(...).syllables[].phonemic_ipa",
            "tone_handling": "project default",
        },
        "external": {
            "name": "lao2ipa",
            "version": external_version,
            "source": "https://github.com/byu-matrix-lab/lao2ipa",
            "license": "Apache-2.0",
            "output": "ipa",
            "tone_handling": "external package default",
        },
        "summary": summary,
        "results": results,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report["summary"], indent=2))
    print(f"Report written to: {args.output}")
    print("Review fixture disagreements and every cross-implementation mismatch.")
    # A phonological disagreement is data to inspect, not a program failure.
    # Runtime errors still signal that the comparison could not be completed.
    return 2 if summary["runtime_errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
