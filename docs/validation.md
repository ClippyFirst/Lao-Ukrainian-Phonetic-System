# Validation

## Deterministic structural validation

The test suite covers:

- NFC normalization and mixed-script rejection;
- ordinary consonant and vowel mappings;
- consonant-class-dependent Vientiane tones;
- live/dead classification;
- final-stop neutralization;
- preposed long/short vowel structures;
- special-vowel handling for ໄ/ໃ;
- structural handling of ຳ and Niggahita-related forms;
- the vowel-carrier behavior of ອ;
- Russian-versus-Ukrainian comparative decisions.

A repository-level audit script additionally checks registry uniqueness and Lao code-point ranges:

    python scripts/audit.py

Derived correspondence data can be regenerated from the canonical mapping:

    python scripts/generate_derived.py

## Test status

Fresh GitHub Actions verification for the current work-branch head `afa168c19a60d5d8efce24f0ebeae47246897eb0` passed in [run 39489040363](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39489040363) on 2026-10-20. The branch also includes an optional independent-G2P comparison harness; that external comparison has not yet been executed.

- Python unit tests: **45 passed**.
- Browser engine tests: **34 passed**.
- Canonical browser data regeneration: passed.
- Generated-data reproducibility check: passed.
- Built-page and relative-asset check: passed.

This is evidence for the work branch only. It does not imply that these changes are already present on `main`, and it is not an expert linguistic adjudication.

## Empirical validation

No empirical accuracy percentage is claimed until a versioned Lao gold corpus with an explicit denominator and expert adjudication exists. Shared regression fixtures are not an independent gold corpus.


## Independent G2P comparison harness

The optional comparison procedure is documented in [independent-g2p-comparison.md](independent-g2p-comparison.md). It uses `scripts/compare_external_g2p.py` with `lao2ipa==1.0.0`, compares IPA outputs after NFC normalization only, and emits a per-case JSON report. Mismatches are intentionally not treated as a correctness verdict. No empirical result is claimed until the script has run and mismatches have been reviewed.
