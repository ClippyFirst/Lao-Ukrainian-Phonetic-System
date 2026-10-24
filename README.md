# Lao → Ukrainian Phonetic-Graphemic Correspondence System

Research-oriented, machine-readable system for deriving a practical Ukrainian representation from Lao through graphemic analysis, phonology and IPA.

## What this project is

This repository develops a **project-specific Ukrainian practical transcription / phonetic-graphemic correspondence system** for contemporary Standard Lao, using a Vientiane-oriented reference model where the evidence supports it.

It is deliberately **not**:

- Lao-character → Ukrainian-character substitution;
- Lao → romanization → Ukrainian;
- a claim to be an official Ukrainian national standard;
- a universal transcription system for every Lao dialect;
- a lexical word-segmentation engine.

## Research pipeline

**Lao Unicode → graphemic structure → syllable analysis → consonant class → vowel/quantity → live/dead → tone → phonology → IPA → Ukrainian target → practical Ukrainian orthography**

The IPA layer is the main audit boundary between source-language analysis and Ukrainian adaptation.

## Comparative methodology

Russian Lao practical transcription is retained as a genuine historical/practical comparator. It is **not** the source of the Ukrainian output.

Serbian and Bulgarian material is used only as a target-script control where it demonstrates a relevant adaptation principle; the repository does not invent Serbian- or Bulgarian-specific Lao transcription standards where none were established.

Important current project decisions include:

- /kʰ pʰ tʰ/ → Ukrainian к п т rather than Russian кх пх тх;
- /h/ → Ukrainian г as a project-specific practical approximation (not a claim of phonetic identity);
- /ŋ/ → нг;
- /tɕ/ → ч;
- /ɯ/ → и;
- source vowel quantity remains explicit in analysis but is normally neutralized in practical Ukrainian output.

These are **project decisions**, not official Ukrainian orthographic rules.

## Repository structure

- src/lao_ukrainian/ — implementation;
- data/lao/ — authoritative Lao registries;
- data/comparative/ — Cyrillic comparison;
- data/evidence/ — claims and source provenance;
- docs/ — methodology, specification, implementation, limitations and decisions;
- schemas/ — machine-readable output schemas;
- tests/ — regression and structural tests.

## Scope and limitations

The core model covers modern Lao consonant classes, source vowel quantity, major orthographic vowel structures, codas, Vientiane-oriented live/dead tone logic, IPA, and a separate Ukrainian target layer.

Known limitations remain explicit: automatic segmentation of unspaced multi-syllable text, restricted initial clusters, full tonal treatment of ໜ/ໝ, Pali/Sanskrit output, lexical exceptions/conventional names, and empirical accuracy against an adjudicated gold corpus.

## Reproducibility

Run the test suite with:

    PYTHONPATH=src python -m unittest discover -s tests -v

For an installed package:

    pip install -e .
    lao-ua "ຂາ"
    lao-ua "ໄກ່" --json

## Documentation

- docs/methodology.md
- docs/system-specification.md
- docs/comparative-cyrillic.md
- docs/decision-log.md
- docs/implementation.md
- docs/limitations.md
- docs/validation.md
- docs/sources-and-evidence.md
- docs/ukrainian-target.md
- docs/unicode.md

## Web service

The repository also contains a two-page local-first web instrument:

- `index.html` — Lao input, Ukrainian practical output, IPA and per-syllable explanation;
- `system.html` — the methodology, decisions, comparisons and limitations.

**Live site:** https://clippyfirst.github.io/Lao-Ukrainian-Phonetic-System/  
**Methodology:** https://clippyfirst.github.io/Lao-Ukrainian-Phonetic-System/system.html

The browser artifact is generated from the canonical Lao CSV registries. It does not upload user text or require a runtime API. GitHub Pages deployment is automated by `.github/workflows/pages.yml`; the multi-page static build uses relative paths and works under the repository project URL. The latest deployment of commit `007c6a7e0bce0ca72cda3ddda3054c69492ca3b8` succeeded in [workflow run 39597989697](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39597989697).

Release verification:

    python scripts/audit.py
    PYTHONPATH=src python -m unittest discover -s tests -v
    npm install --no-audit --no-fund
    npm test
    npm run build

The web layer is intentionally conservative and does not claim to replace the research core or provide empirical accuracy without a versioned gold corpus.

## Status

**🟡 Research MVP; the static web instrument is deployed.** Phonological source adjudication, an independently reviewed gold corpus, external G2P comparison, and full dialect/cluster coverage remain incomplete; deployment does not imply linguistic validation.

The repository is a research foundation with explicit provenance and deterministic tests. It is not yet publication-ready: a larger syllable corpus, fuller cluster/ligature analysis, independent gold examples and expert adjudication are still required.


## External IPA renderers and G2P candidates

The research registry records external pronunciation engines, IPA dictionaries, and Unicode IPA display fonts without treating unvalidated output as ground truth. See [`docs/external-ipa-renderers.md`](docs/external-ipa-renderers.md) and the machine-readable [`data/external-ipa-renderers.json`](data/external-ipa-renderers.json). These are candidate inventories only; no third-party engine is enabled by default, and the ClippyFirst IPA → Ukrainian adapter remains the sole target adaptation boundary.
