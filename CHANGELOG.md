# Changelog

## Unreleased — branch research consolidation

- Integrated the opt-in Python Meta-Hybrid v3 comparator and tests; it reports cross-engine agreement without voting or changing deterministic Ukrainian output.
- Added the pinned Laonetics 0.4.3 same-set research benchmark and explicitly documented its CC-BY-NC-4.0 restriction; it is not a production dependency.
- Enabled external G2P research workflow runs on benchmark branches while keeping all comparator dependencies out of the public website.

## Unreleased — remove neural inference from public web service

- Removed the Hybrid v2 neural tonal IPA panel and its first-run download/run controls from the public website.
- Removed browser-only ONNX export, tokenizer/WASM runtime packaging, model assets and preview workflows from the Pages build; deployment now contains only the deterministic browser engine and static data.
- Kept Python Hybrid v2/MekongPhon research and CLI implementations intact; this change does not delete benchmark evidence or alter the deterministic IPA → Ukrainian production path.
- Added a Chromium regression asserting that no neural model download or run panel is exposed by the public service.

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
