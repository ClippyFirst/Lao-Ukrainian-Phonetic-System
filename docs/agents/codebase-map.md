# Codebase map — Lao → Ukrainian

**Audit basis:** current `main` commit `20a44ab4c3730434bd0176a699853b796fa8fd1d` (PR #165 merged); exact-main Verify [#42863119435](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42863119435) passed **349 Python, 152 Node and 22 Chromium tests**. The same mainline commit passed the MekongPhon three-engine, deterministic-profile, external-G2P, HVULao 1k and Hybrid v2 HVULao 1k workflows (#42863119499, #42863119522, #42863119460, #42863119212, #42863119174). The static site remains deployed by the previously verified Pages workflow [#42847422106](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42847422106); PR #164 fixed research CLI line breaks and PR #165 added the standalone typed MekongPhon IPA API. PR #145 remains open and unmerged because its neural-first default conflicts with the current deterministic default. This is a navigation map of implemented engineering boundaries, not a claim of full Lao phonological coverage or accuracy. PR #157 is merged; PR #156 is closed unmerged after selective benchmark port; PRs #146 and #147 are closed unmerged as superseded by updated mainline implementations. PR #148 is closed unmerged after a selective methodology-pin port; PR #145 remains open and unmerged. This is a navigation map of implemented engineering boundaries, not a claim of full Lao phonological coverage or accuracy.

## User-facing entry points

- Python API: `src/lao_ukrainian/__init__.py`; orchestration in `src/lao_ukrainian/core.py`.
- CLI: `src/lao_ukrainian/cli.py`; hybrid-deterministic is the default engine; Vientiane and MekongPhon-reference remain explicit compatibility profiles.
- Optional neural provider: `src/lao_ukrainian/mekongphon.py`; `transcribe_ipa()` / `MekongPhonEngine.transcribe_ipa()` return `MekongPhonIPAResult` at the source IPA boundary, while `transcribe_lao()` / `.transcribe()` explicitly continue through Ukrainian adaptation. Tonal/non-tonal models use immutable revisions, bounded input and raw IPA provenance; unknown symbols fail closed. This is opt-in Python research tooling, not the deterministic default or browser runtime.
- Browser instrument: `index.html`, `web/app.js`, `web/engine.js`; methodology page: `system.html`.
- Optional romanization method: `web/romanization.js` and `web/romanization-syllable-engine.js`; separate from the phonetic route.
- Static build: `scripts/build_web.py`; native browser ES modules, no Vite/Webpack bundler.

## Primary phonetic flow

```text
Lao source text
  └─ normalize / Unicode validation
      └─ structural dynamic syllable segmentation (not lexical word segmentation)
          └─ parse onset, vowel structure, coda, tone-mark position
              └─ source-language phonology and tone/rhyme analysis
                  └─ typed PhoneticResult (IPA, segments, boundaries,
                     quantity, tone, provenance, confidence)
                      └─ typed Ukrainian adapter (SUPPORTED / UNCERTAIN IPA;
                         explicitly PROVISIONAL fallback remains labelled)
                          └─ practical Ukrainian orthography
```

Python implementation:
- `normalize.py` — NFC normalization and Unicode/input validation.
- `parser.py` — orthographic syllable parsing, dynamic segmentation, tone-mark storage-order checks, onset/coda and vowel structures.
- `phonology.py` — rhyme/live-dead classification and source-scoped tone selection.
- `mekongphon_reference_profile.py` — Vientiane baseline, MekongPhon compatibility and default hybrid deterministic profile definitions.
- `hybrid_rules.py` — deterministic rule selection by priority and context specificity; equal-rank conflicting outputs fail closed.
- `phonetic_result.py` — source IPA inventory, typed IPA tokenization, and `from_provisional_preview()` for evidence-labelled grapheme hints plus explicit unknown segments.
- `target.py` — typed IPA → Ukrainian adaptation; initial yodation and target-specific sequence matching.
- `core.py` — public orchestration, uncertainty handling, and the `ipa_profile` selector (default `hybrid-deterministic`; explicit `vientiane` baseline and `mekongphon-reference` compatibility profiles).
- `model.py` / `data.py` — result types and canonical registry loading.

The browser engine is a separately maintained implementation using generated canonical data. Its API and visible UI default to `hybrid-deterministic`, matching Python. Explicit `vientiane` and `mekongphon-reference` profiles remain frozen for compatibility only; future engine development targets hybrid. Python and browser implementations both retain the baseline fallback and record applied hybrid rule IDs in IPA provenance. Shared fixtures and CI test the explicitly shared contracts; do not assume every phrase-level normalization or segmentation detail is identical across runtimes.

## Optional neural IPA stage

The optional BYU MATRIX Lab provider is a separate source-G2P route, not an alternate implementation of the deterministic parser and not a website dependency:

```text
Lao orthography
  → pinned MekongPhon tonal / non-tonal checkpoint
  → untouched raw IPA + model revision
  → typed MekongPhonIPAResult / PhoneticResult
  → (only for transcribe() / transcribe_lao()) Ukrainian target adapter
```

- `MekongPhonEngine.transcribe_ipa()` and package-level `transcribe_ipa()` stop after stage 1; they do not call `adapt_phonetic_result()`.
- `MekongPhonEngine.transcribe()` and `transcribe_lao()` explicitly run both stages.
- The public package exports `MekongPhonIPAResult`, `MekongPhonResult`, `transcribe_ipa` and `transcribe_lao` from `src/lao_ukrainian/__init__.py`.
- Offline boundary and provenance regressions live in `tests/test_mekongphon_adapter.py`; CLI-stage tests live in `tests/test_mekongphon_cli.py`. Actual pinned-model execution is separately exercised by the MekongPhon benchmark workflow.
- Neural dependencies and weights are opt-in. No silent deterministic fallback is performed, and the static GitHub Pages service remains browser-native deterministic JavaScript.

## Provisional grapheme hints and hybrid fallback

`grapheme_preview.py` produces a diagnostic `PROVISIONAL` segmental hint from registered positional onset/cluster values and parser-confirmed vowel/coda structures. The primary hybrid may wrap those hints as a separate typed `PROVISIONAL` `PhoneticResult`, append explicit unknown segments for unresolved graphemes, and send that typed result through the ordinary Ukrainian IPA adapter. This is not direct grapheme-to-Ukrainian mapping: provisional IPA runs remain visibly low-confidence, unknown segments render `?`, and none is promoted to `SUPPORTED` IPA. The adapter preserves confidence labels; benchmark accuracy metrics score only `SUPPORTED` / `UNCERTAIN`, never `PROVISIONAL`. Tone is never inferred by the preview. Browser parity lives in `web/engine.js`; both runtimes preserve known vowel length when available.

Canonical codepoint inventory: `data/lao/grapheme_inventory.csv` (83 assigned code points in the Unicode 18 Lao block). Unicode character identity does not itself establish a pronunciation.

## Non-authoritative lexical-boundary hints

- `src/lao_ukrainian/lexical_hints.py` is an optional diagnostic helper; it is not imported by the production parser or G2P path.
- `data/lao/lexical-hints/Lao-Dictionary.txt` is the attributed LaoNLP orthographic word list (11,208 entries) with its original BSD-style notice. Its authors describe it as a word-wrapping resource and say compounds were mostly reduced to parts.
- `data/lao/lexical-hints/LaoNLP-MIT-LaoWord.txt` is a filtered 34,937-entry derivative of the separate MIT CSV: NFC-normalized unique Lao-block strings only, with the full file-specific MIT notice embedded. The raw 2.86 MB CSV is not bundled.
- The matcher reports every contiguous multi-syllable match, retains overlaps, and labels each result `SOFT_HINT_ONLY`. It never selects a segmentation, supplies IPA, changes Ukrainian output, or enters the browser bundle.
- Focused tests live in `tests/test_lexical_boundary_hints.py`; the published LaoNLP syllabification example is tested in both Python and browser suites. The MIT-derived list is loaded only when explicitly passed to the helper. These are software/structural checks, not lexical or pronunciation gold.

## Separate orthographic romanization route

The optional CLDR/BGN-oriented romanization method is lower-information and source-aware. It checks the romanized syllable's onset, nucleus and supported coda against the Lao source. It cannot reconstruct tone or pronunciation absent from romanization and is not a fallback for failed IPA analysis.

## Data and generated-artifact ownership

- Canonical Lao registries: `data/lao/*.csv` — including consonants, onset clusters, vowels, codas, tone rules, special tone rules, Ukrainian correspondences and grapheme inventory.
- Source/claim provenance: `data/evidence/sources.csv`, `data/evidence/claims.csv`.
- Generated browser mirror: `web/data.js`; regenerate with `scripts/generate_web_data.py`, never hand-edit.
- Machine-readable contracts: `schemas/`.
- Independent IPA gold lifecycle: `scripts/ipa_gold_corpus.py`, `data/benchmark/`; current data files are structurally valid but contain no adjudicated gold items.

## Research and benchmark tooling

- `scripts/benchmark_mekongphon_three_engines.py` — pinned ClippyFirst/Lao2IPA/MekongPhon comparison; aggregates only.
- `scripts/diagnose_mekongphon_train_split.py` and `scripts/analyze_mekongphon_grapheme_contexts.py` — aggregate training-split diagnostics, not accuracy labels.
- `scripts/compare_external_g2p.py`, `scripts/benchmark_ipa.py`, `scripts/benchmark_additional_lao_g2p.py` — external comparator and gold scorer; all external engines remain research-only.
- `scripts/audit.py` — canonical registry, schema and evidence integrity checks.
- `scripts/audit_laonlp_dictionary.py` — offline, Git-blob-pinned CSV audit; separates exact repeated headers, malformed header-like rows and ID-only placeholders. The raw CSV is supplied by the operator and is never bundled.
- `scripts/benchmark_ipa_contract.py` — shared typed IPA confidence gate for benchmark metrics.

## High-risk seams

1. Tone-mark storage order and per-syllable selector eligibility: parser + shared fixtures + Python/browser tests.
2. Vowel nucleus × coda classification: live/dead affects tone; do not infer it from the length label alone.
3. Ambiguous onset clusters and unconsumed suffixes: preserve the fail-closed parser contract.
4. Typed IPA → Ukrainian boundary: only supported typed IPA may produce accepted target output.
5. Provisional fallback: allow typed PROVISIONAL IPA hints through the ordinary adapter, but never promote them to SUPPORTED or infer tone.
6. External G2P: pin versions/revisions, preserve raw output and provenance; inter-engine agreement is not accuracy.
7. Gold ingestion: only independent, adjudicated, rights-eligible, held-out records may enter accuracy denominators.
8. Python/browser parity: shared source data and fixtures do not eliminate runtime-specific edge cases.

## Verification

```bash
python scripts/ipa_gold_corpus.py validate --language lao
python scripts/audit.py
PYTHONPATH=src python -m unittest discover -s tests -v
npm ci --no-audit --no-fund
npm test
npm run build
git diff --exit-code -- web/data.js
npx playwright install --with-deps chromium
npm run test:browser
```

A green engineering suite verifies the configured software contracts. It does not prove expert phonetic correctness, independent gold accuracy, manual screen-reader conformance, physical-device behavior or release readiness.