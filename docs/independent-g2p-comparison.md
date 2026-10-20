# Independent Lao-to-IPA comparison (experimental)

## Purpose and current status

This procedure compares the project's IPA output with the independently maintained `lao2ipa` package. It is a **comparative diagnostic**, not an accuracy benchmark: neither implementation is presumed correct, and the current vowel fixture is an engineering regression set rather than an expert-adjudicated lexical corpus.

External implementation:
- Project: https://github.com/byu-matrix-lab/lao2ipa
- Version: `1.0.0`
- License: Apache-2.0
- API: `from lao2ipa import transliterate`, with `output="ipa"`
- The upstream README specifically flags tone assignment and vowel clusters as areas where heuristics may need refinement.

No comparison result is committed yet. Run this only in an environment that can install the dependency, then preserve the JSON report as a review artifact. Do not report the exact-match rate as linguistic accuracy.

## Reproduce

From the repository root, in a clean Python environment:

```bash
python -m pip install -e .
python -m pip install lao2ipa==1.0.0
python scripts/compare_external_g2p.py
```

The script reads `tests/fixtures/vowel_precedence_cases.json`, runs each surface form through both systems, normalizes both outputs to Unicode NFC, and writes `artifacts/external-g2p-comparison.json`.

The harness compares each implementation's default IPA output. It deliberately does not expose the external package's `ignore_tones` option: using it while leaving the project's tonal output unchanged would make exact-match rates systematically misleading. Tone/convention disagreements remain visible in raw outputs and must be reviewed manually. The script does not silently remove tone marks, length marks, separators, or other IPA characters. Mismatches are left unclassified for manual review instead of assigning speculative phonological causes.

## What to record in a reviewed report

- Python version, operating system, package versions, fixture revision and commit SHA.
- Whether each input is a lexical item, a synthetic structure, or a proper name; record source and dialect when known.
- Whether outputs differ because of transcription conventions, tone, vowel quality/length, onset/coda, syllabification, or unsupported input.
- Which differences are actual errors versus plausible dialect/convention differences, and who adjudicated them.
- The exact denominator, failures, exclusions, and reason for every exclusion.

## Interpretation limits

The current fixture contains synthetic forms designed to isolate spelling structures. It is useful for regression diagnostics but cannot support a representative corpus-level accuracy estimate. An exact match means only that two outputs agree after NFC normalization. Disagreement does not by itself show which system is wrong. A defensible accuracy claim requires a versioned, redistributable, dialect-labelled corpus and independent expert adjudication.
