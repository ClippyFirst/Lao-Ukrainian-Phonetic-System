# Changelog

## Unreleased — provisional IPA fallback visibility

- Show the available typed provisional IPA hint in the main IPA summary when full structural parsing cannot establish a complete reading.
- Bound long unresolved fallback spans to at most three question marks in the Ukrainian practical output while retaining low-confidence status and provenance.
- Add Python, browser-engine and Chromium regressions for `ພຣະຣາຊອານາຈັກຣ໌ລາວ`; this verifies rendering behavior, not an independently adjudicated pronunciation.

## 0.1.0 — research foundation

- Added Lao Unicode-aware parser and Vientiane-oriented phonological pipeline.
- Added consonant classes, vowels, codas, tone rules and IPA layer.
- Added Russian practical-transcription comparison.
- Added Serbian and Bulgarian target-script control evidence.
- Added Ukrainian-specific practical target policy based on IPA and the external Ukrainian Phonetic Inventory.
- Added structural-vowel, Unicode, comparison and target regression tests.
- Added evidence/claims registries and methodological documentation.
