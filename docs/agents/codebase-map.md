# Codebase map — Lao → Ukrainian

**Verified baseline:** `main` at `c0d7218da907dbe0bae6cadb42824ca0cd09b83a` (2026-11-08).  
**Purpose:** navigation map of implemented boundaries and ownership. It is not a claim of complete Lao coverage or empirical accuracy.

## 1. Product surfaces and entry points

| Surface | Entry point | Current contract on `main` |
|---|---|---|
| Python package | `src/lao_ukrainian/__init__.py` | Public analysis API and optional neural adapter exports |
| Python orchestration | `src/lao_ukrainian/core.py` | Deterministic rule analysis via `analyze()` |
| CLI | `src/lao_ukrainian/cli.py` | `--engine rules` is the default; tonal/non-tonal MekongPhon are explicit optional choices |
| Neural adapter | `src/lao_ukrainian/mekongphon.py` | Explicit model inference, immutable default revisions, raw IPA provenance; not the default and no silent rules fallback |
| Browser application | `index.html`, `web/app.js`, `web/engine.js` | Browser-native deterministic engine; local-first, no Python/PyTorch runtime |
| Methodology page | `system.html` | Static explanation and project decisions |
| Romanization mode | `web/romanization.js`, `web/romanization-syllable-engine.js` | Separate, lower-information orthographic path; not a phonetic fallback |
| Static build | `scripts/build_web.py` | Copies two HTML pages and native ES modules into `dist/` |

**Pending proposal distinction:** PR #145 proposes making the Python/CLI source G2P stage neural-first. That proposal is not part of this `main` snapshot. Its branch does not make the GitHub Pages application neural; the browser UI would still require a separately deployed inference backend.

## 2. Canonical phonetic flow

The accepted deterministic route on `main` is:

```text
Lao source text
  -> normalization / Unicode validation
  -> conservative structural syllable segmentation
  -> onset + complete vowel structure + coda + tone-mark position
  -> source phonology and tone/rhyme analysis
  -> typed IPA result (segments, boundaries, length, tone, provenance, uncertainty)
  -> supported-only Ukrainian target adaptation
  -> practical Ukrainian orthography
```

The IPA representation is the inspectable adapter boundary. It is not a parallel diagnostic string while the Ukrainian result is independently generated from source graphemes.

### Python modules

- `normalize.py` — NFC normalization and source-character/input validation.
- `parser.py` — orthographic syllable parsing, conservative within-token segmentation, onset/coda/vowel structures and tone-mark storage-order validation.
- `phonology.py` — rhyme/live-dead classification and source-scoped tone selection.
- `phonetic_result.py` — source IPA inventory and typed tokenization independent of Ukrainian target mappings.
- `target.py` — typed IPA → Ukrainian adaptation and target-specific longest-sequence matching.
- `core.py` — deterministic orchestration, warnings, status and uncertainty handling.
- `model.py`, `data.py` — result contracts and canonical registry loading.
- `mekongphon.py` — optional external neural inference; preserves raw IPA/model provenance and rejects unsupported symbols rather than silently guessing.

### Browser modules

- `web/engine.js` — browser-side deterministic parser/phonology/IPA/target route.
- `web/app.js` — user interface and result presentation.
- `web/data.js` — generated mirror of canonical registries; do not edit by hand.
- `web/romanization*.js` — separate source-aware romanization adapter.
- `web/styles.css` — design system implementation, responsive and interaction states.

The Python and browser implementations are separately maintained runtimes. Shared data/fixtures protect selected common contracts; they do not imply blanket parity for normalization, phrase segmentation, punctuation or all error/status aggregation.

## 3. Separate non-equivalent diagnostic paths

1. **Optional neural inference:** a distinct model-backed G2P path with pinned model revisions and typed IPA validation. Current `main` requires explicit engine selection. Model output is comparator evidence, not project gold.
2. **Grapheme preview:** `grapheme_preview.py` and browser counterpart may expose provisional segmental hints when full phonology withholds output. It is `PROVISIONAL`, tone-free and excluded from accepted Ukrainian adaptation.
3. **Romanization adapter:** CLDR/BGN-oriented and lower-information. It cannot reconstruct tone or distinctions absent from romanization; it must not be used as fallback for failed phonetic analysis.

## 4. Data, evidence and generated-artifact ownership

| Path | Ownership rule |
|---|---|
| `data/lao/*.csv` | Canonical consonant, onset-cluster, vowel, coda, tone, grapheme and Ukrainian-correspondence registries |
| `data/evidence/sources.csv` | Source metadata and provenance |
| `data/evidence/claims.csv` | Claim-to-source links and evidence scope |
| `data/derived/` | Generated/derived correspondence material; regenerate from canonical inputs |
| `data/benchmark/` | IPA-gold lifecycle and benchmark projections; JSONL is archival source of truth |
| `schemas/` | Analysis, IPA-gold, licensing, split and comparator contracts |
| `web/data.js` | Generated browser mirror; regenerate with `scripts/generate_web_data.py` |
| `dist/` | Build output; do not hand-author or commit unless the deployment contract explicitly requires it |

The four IPA-gold JSONL files are intentionally empty on the audited mainline; `gold.tsv` is header-only. A valid empty corpus is a research state, not a successful accuracy benchmark.

## 5. Scripts and test ownership

- `scripts/audit.py` — canonical registry, codepoint, evidence and claim integrity.
- `scripts/ipa_gold_corpus.py` — gold corpus validation, split assignment, export and engineering gate.
- `scripts/generate_derived.py`, `scripts/generate_web_data.py` — derived/browser data generation.
- `scripts/build_web.py` — static-site build.
- `scripts/benchmark_ipa.py`, `scripts/compare_external_g2p.py` — evaluation/comparator tooling.
- `scripts/benchmark_mekongphon_three_engines.py`, `scripts/diagnose_mekongphon_train_split.py`, `scripts/analyze_mekongphon_grapheme_contexts.py` — pinned aggregate-only model/engine diagnostics.
- `tests/` — Python unittest contracts, fixtures and CLI/API behavior.
- `web/engine.test.js`, `tests/*.mjs` — Node/browser-engine and layout contracts.
- `tests/browser/site.spec.js` — Playwright Chromium UI and built-site tests.

## 6. High-risk seams

1. Tone-mark storage order and selector eligibility: parser + shared fixtures + Python/browser tests.
2. Vowel nucleus × coda classification: live/dead affects tone; never infer it from length alone.
3. Ambiguous onset clusters, overlapping vowel structures and unconsumed suffixes: preserve source material and fail closed.
4. Typed IPA → Ukrainian boundary: only supported typed IPA may produce accepted target output.
5. Provisional preview: never promote provisional segments or infer tone.
6. External G2P: pin revisions, retain raw IPA/provenance, separate rejection from runtime error; agreement is not correctness.
7. Gold ingestion: only rights-eligible, independently double-annotated, adjudicated and held-out records enter accuracy denominators.
8. Generated data: canonical CSV → generator → `web/data.js`; never hand-edit generated output.
9. Python/browser differences: test each runtime contract explicitly rather than assuming parity.

## 7. Current PR integration context (2026-11-08)

- PR #143 is merged into `main`; do not replay its integrated implementation.
- PR #145 (`feat/mekongphon-first-stage`) is open against `main` and proposes neural-first Python/CLI behavior.
- PR #146 (`feat/deterministic-mekongphon-reference-profile-20261108`) is open against `main` and adds an opt-in deterministic reference profile.
- PR #147 (`benchmark/hvulao-1k-three-engine-20261108`) is stacked on PR #146; it is not independently based on `main`.
- PRs #137–#142 remain open as older stacked branches whose work was consolidated through #143. They should not be blindly merged or replayed.

See the [current repository-wide audit](../audits/current/REPOSITORY-WIDE-AUDIT-2026-11-08.md) for exact SHAs, CI evidence and dispositions.

## 8. Verification

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

A green engineering suite proves only the configured software contracts. It does not prove expert phonetic correctness, independent-gold accuracy, manual screen-reader conformance, physical-device behavior or release readiness.
