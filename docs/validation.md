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

The work-branch head `a9e616563d306155751390e6ac13cbd273038633` passed GitHub Actions verification on 2026-10-21 in [run 39570058551](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39570058551).

- Python unit tests: **49 passed**, including four new tone-rule registry checks.
- Browser engine tests: **34 passed**.
- Optional external-G2P harness syntax and `--help` check: passed; the external package comparison itself was not run.
- Canonical browser data regeneration: passed.
- Generated-data reproducibility check: passed.
- Built-page and relative-asset check: passed.

These runs verify the work branch, not `main`. CI success demonstrates deterministic engineering consistency; it is not an expert linguistic adjudication or evidence of corpus-level phonological accuracy. The tone-rule tests check table integrity, selector reachability and conservative fallback only; they do not independently validate the Vientiane tone model.

## Empirical validation

No empirical accuracy percentage is claimed until a versioned Lao gold corpus with an explicit denominator and expert adjudication exists. Shared regression fixtures are engineering regression cases, not an independent gold corpus.

## Independent G2P comparison harness

The optional comparison procedure is documented in [independent-g2p-comparison.md](independent-g2p-comparison.md). It uses `scripts/compare_external_g2p.py` with `lao2ipa==1.0.0`, compares IPA outputs after NFC normalization only, and emits a per-case JSON report. Mismatches are intentionally not treated as a correctness verdict. The external comparison has not yet been executed, so no match rate or independent accuracy claim is made.
