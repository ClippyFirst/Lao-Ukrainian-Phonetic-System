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

The latest source changes were reviewed structurally through the GitHub repository. A full local execution of the updated branch was **not available through the connected GitHub interface**, so this audit deliberately does not claim a fresh numeric pass count for the modified branch.

The pre-audit implementation had previously passed its local regression suite, but that result is not reused as proof that the newly modified branch passes unchanged.

## Empirical validation

No empirical accuracy percentage is claimed until a versioned Lao gold corpus with an explicit denominator and expert adjudication exists.
