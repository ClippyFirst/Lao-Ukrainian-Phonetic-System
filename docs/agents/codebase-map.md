# Codebase map — Lao → Ukrainian

**Audit basis:** current main `c0d7218da907dbe0bae6cadb42824ca0cd09b83a` plus open PRs #146/#147 and the hybrid deterministic continuation branch. This is a navigation map of implemented engineering boundaries, not a claim of full Lao phonological coverage or accuracy.

## User-facing entry points

- Python API: `src/lao_ukrainian/__init__.py`; orchestration in `src/lao_ukrainian/core.py`.
- CLI: `src/lao_ukrainian/cli.py`; deterministic rules are the default engine.
- Optional neural provider: `src/lao_ukrainian/mekongphon.py`; explicit tonal/non-tonal model selection, immutable model revisions, bounded input, raw IPA provenance and fail-closed unknown-symbol handling. It is not a silent fallback or a replacement for the deterministic engine.
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
                     quantity, tone, provenance, uncertainty)
                      └─ SUPPORTED-only Ukrainian target adapter
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

## Provisional grapheme hints and hybrid fallback

`grapheme_preview.py` produces a diagnostic `PROVISIONAL` segmental hint from registered positional onset/cluster values and parser-confirmed vowel/coda structures. The primary hybrid may wrap those hints as a separate typed `PROVISIONAL` `PhoneticResult`, append explicit unknown segments for unresolved graphemes, and send that typed result through the ordinary Ukrainian IPA adapter. This is not direct grapheme-to-Ukrainian mapping: provisional IPA runs remain visibly low-confidence, unknown segments render `?`, and none is promoted to `SUPPORTED` IPA. Tone is never inferred by the preview. Browser parity lives in `web/engine.js`; both runtimes preserve known vowel length when available.

Canonical codepoint inventory: `data/lao/grapheme_inventory.csv` (83 assigned code points in the Unicode 18 Lao block). Unicode character identity does not itself establish a pronunciation.

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
- `scripts/compare_external_g2p.py`, `scripts/benchmark_ipa.py` — external comparator and gold scorer.
- `scripts/audit.py` — canonical registry, schema and evidence integrity checks.

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
