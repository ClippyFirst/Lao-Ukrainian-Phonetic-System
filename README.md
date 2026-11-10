# Lao → Ukrainian Phonetic-Graphemic Correspondence System

- **[Відкрити вебрушій на GitHub Pages](https://clippyfirst.github.io/Lao-Ukrainian-Phonetic-System/)** — детермінований IPA-first рушій і практичний український результат без завантаження нейромережевої моделі.

- [Romanization → Ukrainian matrix](docs/romanization-to-ukrainian-matrix.md) — BGN/PCGN 1966 / CLDR Lao-Latin profile and syllable-level crosswalk.
- [Лаосько-українська практична транскрипція](docs/lao-ukrainian-practical-transcription.md) — target orthography conventions.
- [Графемний fallback і низька впевненість](docs/lao-grapheme-ipa-preview.md) — typed provisional IPA → Ukrainian adapter behavior, unresolved `?` markers and confidence disclosure.
- [Візуальна система сайту](DESIGN.md) — Lao Woven Editorial design tokens and interaction rules.
- [Дослідження лаоської візуальної культури](docs/research/LAO-VISUAL-CULTURE-AND-WEB-DESIGN-REFERENCES-2026-11-10.md) — sourced textile and visual-identity references.

Research-oriented, machine-readable system for deriving a practical Ukrainian representation from Lao through graphemic analysis, phonology and IPA.

**Current status (2026-11-10):** the static web application is live on [GitHub Pages](https://clippyfirst.github.io/Lao-Ukrainian-Phonetic-System/) and runs the deterministic `hybrid-deterministic` IPA-first pipeline. The public service intentionally does not ship or download neural model weights, ONNX graphs, tokenizers or a WASM inference runtime. The optional neural models, Hybrid v2 and Meta-Hybrid v3 comparison remain Python research/CLI functionality only; they are not part of the website. The browser Hybrid v2 panel and its 40 MB model / 15 MB WASM first-run download were removed. Pages deployment [#42839499385 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42839499385) passed build, 148 Node tests, 21 Chromium tests, deterministic-only artifact checks, deployment and live same-origin smoke-test; the compressed artifact is 48,002 bytes versus 40,375,698 bytes for the prior browser-model deployment. Exact-main Verify [#42840912136 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42840912136) passed 344 Python, 148 Node and 21 Chromium tests, repository data/evidence audit, IPA-gold schema validation, generated-data reproducibility and built-page checks. When full structural parsing cannot establish a complete reading, the main IPA field exposes the available typed `PROVISIONAL` grapheme-position IPA hint and labels it low-confidence; the same IPA → Ukrainian adapter is used, and unresolved positions are summarized with at most three question marks per fallback unit. Independent adjudicated IPA gold remains 0, so this is an engineering-verified research prototype, not a linguistically validated production standard. See the [current continuation audit](docs/audits/current/REPOSITORY-AND-DOCUMENTATION-CONTINUATION-2026-11-10.md).

## Website visual direction

The complete visual redesign was merged in [PR #163](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/163) as commit `9254bd4ecf014a6a5634ac05cebf0d227077977d` and deployed to GitHub Pages by [run #42847422106](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42847422106). The selected direction is a restrained Lao woven-editorial system: paper and silk grounds, Mekong green, indigo, a controlled lac-red accent, Lao-script typography, and an abstract woven rule. It changes presentation only; the deterministic IPA-first engine and separate romanization method remain untouched.

## What this project is

This repository develops a **project-specific Ukrainian practical transcription / phonetic-graphemic correspondence system** for contemporary Standard Lao, using a Vientiane-oriented reference model where the evidence supports it.

It is deliberately **not**:

- Lao-character → Ukrainian-character substitution;
- treating romanization as the primary phonetic method; the optional romanization method is separate, lower-information, and never a fallback when phonetic analysis is unresolved;
- a claim to be an official Ukrainian national standard;
- a universal transcription system for every Lao dialect;
- a lexical word-segmentation engine.

## Research pipeline

**Lao Unicode → graphemic structure → syllable analysis → consonant class → vowel/quantity → live/dead → tone → phonology → IPA → Ukrainian target → practical Ukrainian orthography**

The IPA layer is the main audit boundary between source-language analysis and Ukrainian adaptation. The primary hybrid aims for 100% rendering coverage on valid input: supported IPA is rendered normally, complete but uncertain IPA is rendered with its uncertainty preserved, and unresolved graphemes receive provisional IPA hints plus explicit ? markers through the same typed adapter. A missing Ukrainian correspondence is a target-adapter limitation, not a reason to erase an otherwise accepted source IPA result; the target side receives an explicit ? marker while source IPA provenance is preserved. A placeholder is not a pronunciation prediction or an accuracy claim.

**Unicode coverage:** the canonical Unicode 18 Lao-block inventory contains 83 assigned codepoints; Python and browser tests require typed recognition for all 83 (a grapheme role or explicit orthographic/numeric passthrough). This is 100% codepoint handling, not 100% independent IPA: Pali/Sanskrit and Khmu extensions, obsolete marks, and context-dependent signs remain explicitly scoped rather than assigned invented modern-Lao sounds. Six additional source-attested glide-bearing vowel spellings are handled in both runtimes; see [grapheme preview and coverage policy](docs/lao-grapheme-ipa-preview.md) and [vowel-template matrix](docs/vowel-template-coverage.md).

## Context-sensitive grapheme-to-sound rules

ClippyFirst does **not** store word → IPA dictionary correspondences. It resolves each parsed syllable structurally:

- consonant graphemes use different onset and coda values where the language requires it;
- preposed, above, below and postposed vowel signs are interpreted as parts of a complete vowel structure, not isolated character substitutions;
- documented multi-grapheme onsets are treated as joint consonant units;
- tone is selected from consonant class, rhyme type, vowel length and tone mark;
- only the resulting typed IPA is passed to the Ukrainian adapter.

Thus the same Lao character can have different realizations by role: for example, `ວ` is /ʋ/ as an onset and /w/ as a coda; `ດ` is /d/ as an onset and /t/ as a coda. The vowel sign `ເ` likewise participates in short /e/ and long /eː/ structures depending on the complete spelling.

The pinned [MekongPhon grapheme-context study](docs/audits/current/MEKONGPHON-GRAPHEME-CONTEXT-ANALYSIS-2026-11-07.md) aggregates grapheme, position, neighbouring signs, onset class, vowel ID, rhyme and tone-mark environments. The default Vientiane engine does not turn dictionary words into lexical lookup rules. An additional opt-in [MekongPhon-reference IPA profile](docs/research/MEKONGPHON-DETERMINISTIC-RULE-PORT-2026-11-08.md) applies a small set of high-frequency aggregate correspondences as deterministic convention overrides; it is experimental, does not use model weights, and is not independent gold.

An optional [orthographic lexical-hint diagnostic](src/lao_ukrainian/lexical_hints.py) checks contiguous syllable spans against the attributed [LaoNLP word-wrapping list](data/lao/lexical-hints/README.md). It preserves overlapping matches and labels them `SOFT_HINT_ONLY`. The source explicitly says compounds were mostly reduced to parts, so this is not lexical word-boundary gold. The helper is not called by the production parser, IPA/G2P pipeline, Ukrainian adapter, or browser engine.

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
- data/lao/*.csv — authoritative Lao phonological registries;
- data/lao/lexical-hints/ — separately attributed orthographic reference lists, not pronunciation registries;
- data/comparative/ — Cyrillic comparison;
- data/evidence/ — claims and source provenance;
- docs/ — methodology, specification, implementation, limitations, decisions and evidence-backed audits; see the [repository structure and documentation contract](docs/REPOSITORY-STRUCTURE.md);
- AGENTS.md — project-specific agent rules and pinned external methodology references;
- schemas/ — machine-readable output schemas;
- tests/ — regression and structural tests.

## Scope and limitations

The core model covers modern Lao consonant classes, source vowel quantity, major orthographic vowel structures, codas, Vientiane-oriented live/dead tone logic, IPA, and a separate Ukrainian target layer. The default ClippyFirst engine is the deterministic hybrid profile: Vientiane phonology remains its baseline, with only evidence-gated MekongPhon aggregate correspondences selected by deterministic contextual rules. Explicit `vientiane` and `mekongphon-reference` profiles remain frozen for compatibility only; future engine development targets hybrid.

**Latest completed benchmark evidence (2026-11-09, schema 6.0):** output coverage is now explicitly separated from confidence-gated IPA coverage. On the 100-word dictionary-seeded comparison, ClippyFirst emitted segmental and tonal output for **100/100 inputs**, covering all **169/169 syllable units**. The 3 provisional units retain grapheme-derived hints and explicit unknown positions; missing tone contours are emitted as `?`, not silently withheld. Confidence remains separately visible: 97/100 inputs have fully accepted segmental IPA and 91/100 have fully accepted tone contours. Against the full reference denominator (including the cost of `?` markers), ClippyFirst scored 6.15% segmental CER (90/100 exact), 22.90% native-contour tonal CER, and 11.39% when contours are re-rendered in the MekongPhon evaluation convention (69/100 exact). MekongPhon Neural scored 6.64% / 8.29% at 100% output coverage; Lao2IPA scored 8.97% / 11.97% at 100%. Thus ClippyFirst leads this split on segmental CER and beats Lao2IPA on the Mekong-convention tonal score, but still trails MekongPhon Neural on tonal CER. Tone-category error is 3.81% on covered categories (105/126; 83.33% category coverage). These are reference-relative concordance results, not independent expert accuracy; the held-out vocabulary also influenced validation-sentence generation/checkpoint selection. Independent adjudicated IPA gold remains 0. The latest HVULao schema-1.5 run [#42653641804](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42653641804) completed with zero runtime errors: hybrid rendering is 1,000/1,000 inputs and 21,534/21,534 analyzed units; 661/1,000 sentences (66.1%) have complete accepted IPA and syllable IPA coverage is 97.71%. The 607 unavailable Ukrainian target correspondences and 398 provisional IPA units remain visible as marked output, not omissions. See the [confidence-gated engine inventory](docs/research/LAO-G2P-ENGINE-AND-DATASET-INVENTORY-2026-11-08.md) and [benchmark report](docs/research/LAO-G2P-THREE-ENGINE-BENCHMARK-2026-11-07.md).

Known limitations remain explicit: lexical word-boundary detection (the parser can structurally segment supported syllables within a token but does not infer lexical words), low-confidence fallback for unresolved structures, restricted initial clusters, full tonal treatment of ໜ/ໝ, Pali/Sanskrit output, lexical exceptions/conventional names, and empirical accuracy against an adjudicated gold corpus. Rendering coverage, typed IPA coverage and phonetic accuracy are reported separately. The current 100% rendering figure means every tested input receives a visible output, not that every unit has supported IPA or a verified pronunciation.

## Quick start and verification

**Requirements:** Python 3.10 or newer; Node.js 22.14 or newer for browser test/build commands.

Run the complete configured engineering checks from the repository root (commands are shown in the contribution guide).

- Validate IPA corpus structure: python scripts/ipa_gold_corpus.py validate --language lao
- Validate canonical data/evidence: python scripts/audit.py
- Run Python tests: PYTHONPATH=src python -m unittest discover -s tests -v
- Install Node test dependencies: npm ci --no-audit --no-fund
- Run Node/browser-engine suites: npm test
- Build the static site: npm run build
- Check generated-data drift: git diff --exit-code -- web/data.js
- Run built-site browser tests: npm run test:browser

The browser tests require Playwright Chromium. In a fresh environment, install it with npx playwright install --with-deps chromium.

For an installed Python package, run pip install -e . and then use lao-ua "ຂາ" or lao-ua "ໄກ່" --json. The primary default is hybrid-deterministic; explicit `vientiane` and `mekongphon-reference` profiles are frozen for compatibility. The hybrid keeps Vientiane phonology as its base and applies existing MekongPhon-derived correspondences through a deterministic priority/specificity selector. On unresolved valid input, it returns a visibly provisional Ukrainian-side rendering rather than silently omitting the unit. The browser module exposes the same default and explicit compatibility profiles. See [the hybrid-engine design note](docs/research/HYBRID-DETERMINISTIC-ENGINE-2026-11-08.md).

The web build regenerates the checked-in browser data mirror and copies the two static pages plus the web runtime into dist/. This is a small custom Python build, not a Vite/Webpack bundling pipeline. See [web architecture](docs/web-architecture.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

## Documentation

Start at the [documentation index](docs/README.md). The latest [repository and documentation continuation audit](docs/audits/current/REPOSITORY-AND-DOCUMENTATION-CONTINUATION-2026-11-10.md) records the current mainline, PR reconciliation, documentation authority, verification evidence and blockers. The [codebase map](docs/agents/codebase-map.md) traces implementation entry points and data ownership. The index identifies the canonical specification, evidence, audit registers, implementation map and historical records. For development and review conventions, see [CONTRIBUTING.md](CONTRIBUTING.md). The canonical execution ledger remains [MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md](docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md). The [Ukrainian practical transcription guide](docs/lao-ukrainian-practical-transcription.md) documents the IPA-conditioned target conventions.

## Web service

The repository also contains a two-page local-first web instrument:

- `index.html` — Lao input, Ukrainian practical output, IPA and per-syllable explanation;
- `system.html` — the methodology, decisions, comparisons and limitations.

**Live site:** https://clippyfirst.github.io/Lao-Ukrainian-Phonetic-System/  
**Methodology:** https://clippyfirst.github.io/Lao-Ukrainian-Phonetic-System/system.html

The browser artifact is generated from the canonical Lao CSV registries. It does not upload user text or require a runtime API. Its default phonetic route uses the same `hybrid-deterministic` profile as the Python API and CLI. The Ukrainian result has two selectable methods: the default IPA-first phonetic adaptation and a separate syllable-level adapter for the provisional CLDR Lao-Latin/BGN romanization. The latter parses onset, vowel nucleus and coda rather than replacing Latin characters one by one, and cross-checks each romanized onset, source vowel ID and supported coda against the original Lao syllable analysis. The `h` in `kh/th/ph` marks aspiration, while standalone `h` from ຫ/ຮ represents /h/ and maps to `г`; the aspirated stops map to `к'/т'/п'`. The high-class nasal ligatures ໜ/ໝ and their expanded spellings ຫນ/ຫມ are checked as /n/ and /m/, not audible /h+n/ or /h+m/. The same source-aware silent-hoa handling covers the implemented forms ຫງ, ຫຍ, ຫລ/ຫຼ and ຫວ. Source vowel IDs also disambiguate romanizations such as `kam` (A + final m versus the AM nucleus). Ambiguous or mismatched syllables are withheld as partial rather than guessed. It cannot reconstruct tone or pronunciation absent from romanization and is not a phonetic equivalent. See [the methodology](docs/methodology.md#optional-romanization-to-ukrainian-mode). GitHub Pages deployment is automated by `.github/workflows/pages.yml`; the multi-page static build uses relative paths and works under the repository project URL. Deployment history is available in the [GitHub Pages workflow](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/workflows/pages.yml); exact-main engineering checks are recorded in the [verification workflow](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/workflows/verify.yml).

Release verification:

    python scripts/audit.py
    PYTHONPATH=src python -m unittest discover -s tests -v
    npm ci --no-audit --no-fund
    npm test
    npm run build

The web layer is intentionally conservative and does not claim to replace the research core or provide empirical accuracy without a versioned gold corpus.

## Optional MekongPhon neural inference

The deterministic rule engine remains the default. Optional tonal and non-tonal neural inference is available through the separately published BYU MATRIX Lab model artifacts for Python research/CLI use only; weights are downloaded at first use and are not committed to this repository. The public web service does not download or execute these models.

Install the optional dependencies and select a model explicitly:

```bash
pip install -e '.[neural]'
lao-ua 'ສະບາຍດີ' --engine mekongphon-tonal --device cpu --json
lao-ua 'ສະບາຍດີ' --engine mekongphon-nontonal --device cpu --json
lao-ua 'ຂາ' --engine meta-hybrid-v3 --device cpu --json
```

Both engines default to immutable model revisions recorded in [the integration guide](docs/research/MEKONGPHON-NEURAL-INTEGRATION.md). The raw model IPA and typed tone segments are preserved; unknown IPA symbols or incomplete Ukrainian mappings fail closed. Neural inference never silently replaces or falls back to the deterministic result. MekongPhon project rights are owner-confirmed as resolved; independent adjudicated Lao IPA gold remains 0.

## Status

**🟡 Engineering-verified research prototype on `main`; the static web instrument is deployed through GitHub Pages.** Phonological source adjudication, an independently reviewed gold corpus and full dialect/cluster coverage remain incomplete; comparative external G2P benchmarking is available, but deployment does not imply linguistic validation.

The repository is a research foundation with explicit provenance and deterministic tests. It is not yet publication-ready: a larger syllable corpus, fuller cluster/ligature analysis, independent gold examples and expert adjudication are still required.


## External IPA renderers and G2P candidates

The research registry records external pronunciation engines, IPA dictionaries, and Unicode IPA display fonts without treating unvalidated output as ground truth. See [`docs/external-ipa-renderers.md`](docs/external-ipa-renderers.md) and the machine-readable [`data/external-ipa-renderers.json`](data/external-ipa-renderers.json). These are candidate inventories only; no third-party engine is enabled by default, and the ClippyFirst IPA → Ukrainian adapter remains the sole target adaptation boundary.

The confidence-gated external benchmark harness can be rerun through the [External Lao G2P research benchmark workflow](.github/workflows/external-lao-g2p-benchmarks.yml). It records aggregate-only reports; the shared [IPA confidence gate](scripts/benchmark_ipa_contract.py) excludes provisional grapheme previews from IPA accuracy. The deterministic-profile and HVULao 1k text-domain workflows are also available from GitHub Actions. All external engines remain research comparators, not production dependencies.

## Independent IPA gold corpus

The project uses a provenance-backed, double-annotated IPA gold workflow. See [the corpus protocol](docs/ipa-gold-corpus.md) and [the language-specific phonology research workpack](docs/audits/current/PHONOLOGY-RESEARCH-WORKPACK-2026-11-01.md). The corpus is currently empty by design; no phonetic accuracy claim is available until expert adjudication is complete.


## Runtime segmentation contract

The Python package and browser instrument intentionally expose different input contracts; their results must not be treated as interchangeable for unspaced multi-syllable input:

- **Python API:** phrase-input oriented. Within each whitespace-delimited token, it attempts conservative dynamic segmentation into complete orthographic syllables. This is a structural parser, not a lexical word segmenter; it retains unresolved material and withholds unsupported phonetic output rather than guessing. Explicit whitespace is a boundary between input fragments; U+200B is rejected by Unicode validation.
- **Browser instrument:** phrase-input oriented. Within each whitespace-delimited token, it attempts conservative dynamic segmentation into complete orthographic syllables. This is a UI convenience, not a lexical word segmenter; unresolved Lao material remains visible through the hybrid's typed provisional/unknown fallback. Visible non-Lao scripts, punctuation, symbols, emoji and timestamps are preserved verbatim while Lao spans are analysed; the result is marked PARTIAL with a warning rather than rejecting the whole message. This passthrough is not a phonetic transcription of the foreign-script material. Explicit whitespace and U+200B remain boundaries between input fragments; unsafe control characters are rejected.
- **Boundary differences:** browser validation and Python normalization/parsing are separate runtime paths. In particular, do not assume U+200B, punctuation, mixed-script passthrough, malformed fragments, or aggregate status behave identically across them. Consumers must select the documented runtime contract and must not compare the two outputs as a parity oracle.

Both runtimes attempt conservative within-token syllable segmentation; Python rejects U+200B, while the browser uses it as a boundary. Neither claims to solve Lao lexical word segmentation. Shared phonological and IPA-to-Ukrainian rules should remain aligned where both runtimes support the same complete syllable, but phrase-level segmentation and all input-normalization behavior are not a blanket parity guarantee. Changes to either contract require runtime-specific regression tests and an explicit update to this section.


## Hybrid mixed-script partial-rendering fix — 2026-11-08

- PR [#150](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/150) merged into `main` at `d0688d325c7450515ef42345ff1f7dec8d14f718`.
- The default browser hybrid now preserves visible non-Lao characters and continues processing supported Lao spans. Such input is labelled PARTIAL with an explicit warning; unsafe controls remain rejected and frozen compatibility profiles remain strict.
- PR Verify [42521697622](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42521697622): 289 Python, 143 Node and 17 Chromium tests passed. Main Verify [42521799243](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42521799243) and Pages deployment [42521799240](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42521799240) succeeded. Live Pages engine fetch returned HTTP 200.
- Rendering coverage does not establish phonetic accuracy; the independent IPA gold corpus remains empty.

## Post-merge publication checkpoint — 2026-11-08

- PR [#143](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/143) was squash-merged into `main`.
- Mainline merge commit: `c3ba58c0e0e6ba64821abe4c9d46c75ff559b2b4`.
- GitHub Pages workflow [42463361038](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42463361038): **SUCCESS**. Browser regression tests, static build, built-site Chromium tests, deployment artifact checks, Pages deployment and deployed-asset smoke tests all passed.
- Live site: https://clippyfirst.github.io/Lao-Ukrainian-Phonetic-System/ — checked after deployment; HTTP 200.
- The site is an engineering-verified research prototype, not a linguistically validated production release. Independent adjudicated IPA gold remains 0; manual assistive-technology and physical-device accessibility QA remains partial.

## Hybrid v2 — deterministic segmentals + neural tones (2026-11-09)

A second hybrid candidate is now implemented as an explicit Python/CLI mode, `--engine hybrid-v2`:

- The existing evidence-aware ClippyFirst hybrid remains authoritative for segmental IPA and Ukrainian practical rendering. Neural segmental phones are never substituted.
- The pinned MekongPhon tonal checkpoint contributes only a registered tone contour, and only when the external IPA parses cleanly and the ordered tone-symbol stream has one unique decomposition into exactly the deterministic parser's syllable count of registered contours.
- Each accepted contour is converted to the corresponding MekongPhon tone category. The original deterministic category disagreement, model ID/revision, raw neural IPA, and overlay provenance remain inspectable.
- Unresolved potential-minor syllables, unknown contours, unsupported IPA, and syllable-count mismatches are withheld rather than guessed. Neural dependency/model failures are surfaced; there is no silent fallback.
- The Ukrainian target output remains the deterministic adapter's output. This is an experimental Python mode; it is not yet the browser default or production default.

Initial acceptance tests cover exact one-/two-syllable alignment, preservation of deterministic segmentals and Ukrainian output, unsupported IPA, unknown contours, count mismatches, and input immutability. The mode is not promoted to the default until same-split benchmark and exact-head CI demonstrate that it improves tonal results without regressing segmental CER or rendering coverage. Independent expert IPA gold remains unavailable.


## Hybrid v2 measured result

On the pinned 100-word MekongPhon split, the opt-in dual-lane hybrid combines the best measured fields: ClippyFirst segmental IPA CER **6.15% (90/100 exact)** and MekongPhon Neural tonal IPA CER **8.29% (74/100 exact)**, while deterministic Ukrainian rendering remains **100/100 inputs and 169/169 units**. The tonal stream is preserved separately rather than forced into a synthetic fused IPA string. Per-syllable neural tone associations are marked uncertain. This is dictionary-seeded concordance, not independent expert validation. See the engine inventory for the full methodology and caveats.


### Hybrid v2 HVULao 1k stress result

On the pinned 1,000-row HVULao sentence split, Hybrid v2 achieved **100% Ukrainian rendering (1,000/1,000 rows; 21,534/21,534 units)**, **66.1% complete segmental IPA sentences**, **97.706% segmental IPA unit coverage**, and **22.8% parseable tonal IPA rows**. Only 10 rows were fully order-aligned for syllable-level tone association and 4 partially aligned; 200 tone predictions were emitted and remain UNCERTAIN. There were zero unexpected runtime errors. This is engineering coverage, not phonetic accuracy; HVULao has no IPA gold. Exact run and artifact details are recorded in the research inventory.


## Meta-Hybrid v3 — opt-in research comparator (2026-11-10)

The Python/CLI-only Meta-Hybrid v3 orchestrator runs the deterministic engine alongside the pinned MekongPhon non-tonal and tonal models. It reports exact segmental agreement/disagreement, preserves the raw tonal lane separately, and reuses the conservative tone-alignment gate. It never votes, rewrites raw IPA, or changes the selected Ukrainian result: the deterministic IPA → Ukrainian lane remains authoritative. Cross-engine agreement is concordance, not accuracy. The public GitHub Pages service does not load this module, model weights, ONNX or WASM assets. Exact branch verification passed in [#42822261651](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42822261651); the external comparator workflow [#42822253479](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42822253479) also passed. Independent expert IPA gold remains 0.
