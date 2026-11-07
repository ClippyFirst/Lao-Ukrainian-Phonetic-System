# Lao → Ukrainian Phonetic-Graphemic Correspondence System

- [Romanization → Ukrainian matrix](docs/romanization-to-ukrainian-matrix.md) — BGN/PCGN 1966 / CLDR Lao-Latin profile and syllable-level crosswalk.

Research-oriented, machine-readable system for deriving a practical Ukrainian representation from Lao through graphemic analysis, phonology and IPA.

## What this project is

This repository develops a **project-specific Ukrainian practical transcription / phonetic-graphemic correspondence system** for contemporary Standard Lao, using a Vientiane-oriented reference model where the evidence supports it.

It is deliberately **not**:

- Lao-character → Ukrainian-character substitution;
- treating romanization as the primary phonetic method (the optional fallback is separate and explicitly lower-information);
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

- /kʰ pʰ tʰ/ → Ukrainian к' п' т' rather than Russian кх пх тх; aspiration remains explicit in IPA and is marked with an apostrophe in practical output;
- Lao /h/ and IPA /ɦ/ both map to Ukrainian г but remain distinct source values; /ɡ/ → ґ; genuine /x/ → х. The /h/ → г choice is a project-specific practical approximation, not a claim of phonetic identity;
- in the romanization method, Lao onset spelling, source vowel ID and supported coda are checked against CLDR romanization before Ukrainian output; `kh/th/ph` map as aspirated `к'/т'/п'`, independent /h/ from ຫ/ຮ maps to `г`, and supported silent-hoa spellings map their underlying sonorant without inserting an `h` sound;
- /ŋ/ → нг;
- /tɕ/ → ч; /t͡s/ → ц; /d͡z/ → дз; /t͡ʃ/ → ч; /d͡ʒ/ → дж; /ʃ/ → ш; /ʒ/ → ж;
- the exact Ukrainian sequence /ʃt͡ʃ/ → щ is matched as a target orthographic unit; isolated /ʃ/ and /t͡ʃ/ remain ш and ч;
- /ɯ/ → и;
- source vowel quantity remains explicit in analysis but is normally neutralized in practical Ukrainian output.

These are **project decisions**, not official Ukrainian orthographic rules. The shared target policy also distinguishes affricates from consonant sequences, preserves supported palatalization, and does not use the aspiration apostrophe for /ʔ/. See [the canonical foreign IPA → Ukrainian adaptation policy](https://github.com/ClippyFirst/Ukrainian-Phonetic-Inventory/blob/main/docs/foreign-target-adaptation.md).

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

## Quick start and verification

**Requirements:** Python 3.10 or newer; Node.js 22.14 or newer for browser test/build commands.

Run the complete configured engineering checks from the repository root (commands are shown in the contribution guide).

- Validate IPA corpus structure: python scripts/ipa_gold_corpus.py validate --language lao
- Validate canonical data/evidence: python scripts/audit.py
- Run Python tests: PYTHONPATH=src python -m unittest discover -s tests -v
- Install Node test dependencies: npm install --no-audit --no-fund
- Run Node/browser-engine suites: npm test
- Build the static site: npm run build
- Check generated-data drift: git diff --exit-code -- web/data.js
- Run built-site browser tests: npm run test:browser

The browser tests require Playwright Chromium. In a fresh environment, install it with npx playwright install --with-deps chromium.

For an installed Python package, run pip install -e . and then use lao-ua "ຂາ" or lao-ua "ໄກ່" --json.

The web build regenerates the checked-in browser data mirror and copies the two static pages plus the web runtime into dist/. This is a small custom Python build, not a Vite/Webpack bundling pipeline. See [web architecture](docs/web-architecture.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

## Documentation

Start at the [documentation index](docs/README.md). It identifies the canonical specification, evidence, audit registers, implementation map and historical records. For development and review conventions, see [CONTRIBUTING.md](CONTRIBUTING.md). The canonical execution ledger remains [MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md](docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md).

## Web service

The repository also contains a two-page local-first web instrument:

- `index.html` — Lao input, Ukrainian practical output, IPA and per-syllable explanation;
- `system.html` — the methodology, decisions, comparisons and limitations.

**Live site:** https://clippyfirst.github.io/Lao-Ukrainian-Phonetic-System/  
**Methodology:** https://clippyfirst.github.io/Lao-Ukrainian-Phonetic-System/system.html

The browser artifact is generated from the canonical Lao CSV registries. It does not upload user text or require a runtime API. The Ukrainian result has two selectable methods: the default IPA-first phonetic adaptation and a separate syllable-level adapter for the provisional CLDR Lao-Latin/BGN romanization. The latter parses onset, vowel nucleus and coda rather than replacing Latin characters one by one, and cross-checks each romanized onset, source vowel ID and supported coda against the original Lao syllable analysis. The `h` in `kh/th/ph` marks aspiration, while standalone `h` from ຫ/ຮ represents /h/ and maps to `г`; the aspirated stops map to `к'/т'/п'`. The high-class nasal ligatures ໜ/ໝ and their expanded spellings ຫນ/ຫມ are checked as /n/ and /m/, not audible /h+n/ or /h+m/. The same source-aware silent-hoa handling covers the implemented forms ຫງ, ຫຍ, ຫລ/ຫຼ and ຫວ. Source vowel IDs also disambiguate romanizations such as `kam` (A + final m versus the AM nucleus). Ambiguous or mismatched syllables are withheld as partial rather than guessed. It cannot reconstruct tone or pronunciation absent from romanization and is not a phonetic equivalent. See [the methodology](docs/methodology.md#optional-romanization-to-ukrainian-mode). GitHub Pages deployment is automated by `.github/workflows/pages.yml`; the multi-page static build uses relative paths and works under the repository project URL. Deployment history is available in the [GitHub Pages workflow](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/workflows/pages.yml); exact-main engineering checks are recorded in the [verification workflow](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/workflows/verify.yml).

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

## Independent IPA gold corpus

The project uses a provenance-backed, double-annotated IPA gold workflow. See [the corpus protocol](docs/ipa-gold-corpus.md) and [the language-specific phonology research workpack](docs/audits/current/PHONOLOGY-RESEARCH-WORKPACK-2026-11-01.md). The corpus is currently empty by design; no phonetic accuracy claim is available until expert adjudication is complete.


## Runtime segmentation contract

The Python package and browser instrument intentionally expose different input contracts; their results must not be treated as interchangeable for unspaced multi-syllable input:

- **Python API:** phrase-input oriented. Within each whitespace-delimited or U+200B-delimited token, it attempts conservative dynamic segmentation into complete orthographic syllables. This is a structural parser, not a lexical word segmenter; it retains unresolved material and withholds unsupported phonetic output rather than guessing. Explicit whitespace and U+200B are boundaries between input fragments.
- **Browser instrument:** phrase-input oriented. Within each whitespace-delimited token, it attempts conservative dynamic segmentation into complete orthographic syllables. This is a UI convenience, not a lexical word segmenter; it retains unresolved material and withholds unsupported phonetic output rather than guessing. Explicit whitespace remains a boundary between input fragments.
- **Boundary differences:** browser validation and Python normalization/parsing are separate runtime paths. In particular, do not assume U+200B, punctuation, mixed-script passthrough, malformed fragments, or aggregate status behave identically across them. Consumers must select the documented runtime contract and must not compare the two outputs as a parity oracle.

Both runtimes attempt conservative within-token syllable segmentation; neither claims to solve Lao lexical word segmentation. Shared phonological and IPA-to-Ukrainian rules should remain aligned where both runtimes support the same complete syllable, but phrase-level segmentation and all input-normalization behavior are not a blanket parity guarantee. Changes to either contract require runtime-specific regression tests and an explicit update to this section.
