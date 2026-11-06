# Codebase map — Lao → Ukrainian

**Audit basis: current main after manifest-wide split fix and source-citation reconciliation; navigation map, not a claim of full linguistic coverage.

## User-facing entry points

- Python package API: src/lao_ukrainian/__init__.py exports analyze, normalization, parsing, phonology and target helpers.
- CLI: src/lao_ukrainian/cli.py calls core.analyze(text) and renders a text or JSON result.
- Browser instrument: index.html / web/engine.js; canonical CSV registries are mirrored into web/data.js by scripts/generate_web_data.py.
- Static build: scripts/build_web.py copies index.html, system.html, and web/ into dist/; this repository does not use Vite or a bundler.
- Browser UI orchestration: web/app.js; optional romanization route: web/romanization.js and web/romanization-syllable-engine.js.

## Primary phonetic flow

~~~text
CLI / Python API ─┐
                  ├─> core.analyze
Browser engine ───┘      │
                         ├─ normalize + Unicode validation
                         ├─ parser.segment_syllables / parse_syllable
                         ├─ phonology.phonologize
                         │    └─ rhyme/live-dead + tone-rule registry
                         ├─ phonetic_result.from_phonology
                         │    └─ typed PhoneticResult (IPA, boundaries, tone, length, provenance, uncertainty)
                         ├─ target.adapt_phonetic_result
                         └─ Analysis / per-syllable status and warnings
~~~

The browser runtime is a separately maintained implementation backed by generated canonical data; it constructs the same typed IPA boundary and applies its typed-result-only target adapter. Parity is tested rather than assumed. Neither target adapter accepts Lao graphemes or a raw IPA string.

## Separate orthographic route

The optional romanization adapter is deliberately lower-information and source-aware. It is not a fallback for failed IPA and cannot reconstruct tone. Keep its tests and evidence separate from phonetic accuracy tests.

## Data and generated-artifact ownership

- Canonical linguistic registries: data/lao/*.csv.
- Evidence and rule provenance: data/evidence/ and docs/audits/current/.
- Generated browser data: web/data.js; regenerate, never hand-edit.
- Gold lifecycle/scorer: scripts/ipa_gold_corpus.py, scripts/benchmark_ipa.py, data/benchmark/.

## High-risk seams

1. Tone-mark order and selector eligibility: parser + shared tone fixtures + Python/browser parity.
2. Vowel nucleus × coda classification: live/dead affects tone; do not infer from the length field alone.
3. Ambiguous onset clusters and preposed vowels: preserve the fail-closed parser contract.
4. Typed IPA → Ukrainian boundary: only SUPPORTED PhoneticResult values may produce output; unknown or uncertain IPA must be withheld.
5. External G2P: pin versions and preserve raw output; comparator agreement is not accuracy.
6. Gold ingestion: only independent adjudicated, rights-eligible, held-out records may enter the accuracy denominator.

## Verification

- Python: python scripts/audit.py; PYTHONPATH=src python -m unittest discover -s tests -v.
- Browser: npm test; build: npm run build; verify generated-data drift with git diff --exit-code -- web/data.js.
- A green engineering suite does not prove expert phonetic adjudication, gold accuracy or manual accessibility QA.
