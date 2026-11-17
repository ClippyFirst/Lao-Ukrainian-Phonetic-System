# Lao → Ukrainian Phonetic-Graphemic Correspondence System

- **[Відкрити вебрушій на GitHub Pages](https://clippyfirst.github.io/Lao-Ukrainian-Phonetic-System/)** — детермінований IPA-first рушій і практичний український результат без завантаження нейромережевої моделі.

- [Romanization → Ukrainian matrix](docs/romanization-to-ukrainian-matrix.md) — BGN/PCGN 1966 / CLDR Lao-Latin profile and syllable-level crosswalk. The web tool also accepts direct romanized input (BGN/PCGN and a bounded ALA-LC profile); ambiguous forms remain marked partial.
- [Лаосько-українська практична транскрипція](docs/lao-ukrainian-practical-transcription.md) — target orthography conventions.
- [Графемний fallback і низька впевненість](docs/lao-grapheme-ipa-preview.md) — typed provisional IPA → Ukrainian adapter behavior, unresolved `?` markers and confidence disclosure.
- [Візуальна система сайту](DESIGN.md) — Lao Woven Editorial design tokens and interaction rules.
- [Дослідження лаоської візуальної культури](docs/research/LAO-VISUAL-CULTURE-AND-WEB-DESIGN-REFERENCES-2026-11-10.md) — sourced textile and visual-identity references.

Research-oriented, machine-readable system for deriving a practical Ukrainian representation from Lao through graphemic analysis, phonology and IPA.

**Current status (2026-11-17; exact current main: `899c911b2ab48b4be722757da38ea0032c55d1d8`; Verify [#44147127249](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/44147127249) SUCCESS):** PR #266 added a scoped ICANN/Lao Script Generation Panel cross-check for the role of ຢ: the DNS root-zone proposal excludes it from its 14 final graphemes and distinguishes initial /j/ ຢ from final /j/ ຍ. PR #267 then synchronized the canonical handoff, linguistic completion register and branch audit with the merge and exact-head verification. The current modern parser profile remains unchanged at nine coda mappings; this DNS-specific source does not replace the general modern Lao inventory. Exact-main engineering checks on the current head report 368 Python, 205 browser-engine and 30 Chromium UI tests passed, with IPA-gold schema, evidence/data audit (84 sources / 112 claims), external-G2P syntax/CLI, build, canonical generation, reproducibility and built-page checks passing. The only pre-existing open PR was #145, whose neural-first CLI default is deferred pending an explicit architecture decision; the present documentation reconciliation is tracked separately in PR #268. issues #9 and #99 remain blocked on rights-cleared independent comparison evidence and qualified human annotation. Independent adjudicated IPA gold remains 0 and empirical accuracy remains null. The repository is an engineering-verified research prototype, not a linguistically validated or release-ready system.

## Website copy and methodology

The site's language and editing rules are documented in the [Ukrainian editorial standard](docs/UKRAINIAN-EDITORIAL-STYLE.md). It keeps Ukrainian as the interface language while preserving exact linguistic and technical identifiers.

All visitor-facing copy on the two public pages was rewritten in Ukrainian on 2026-11-10. The service page now explains the input, the three visible representations, the separate pronunciation and romanization methods, and the meaning of a low-confidence fallback in direct user language. The methodology page is a 14-section guide covering the script, syllable structure, consonant classes, vowels, live/dead syllables, tones, IPA, Ukrainian target choices, romanization limits, benchmark interpretation and the visual concept. Its final section explains **Woven Editorial**: a restrained abstraction of weaving's layered rhythm, not a reproduction of one community's textile pattern. The public copy keeps the independent IPA gold count at zero and distinguishes dictionary-seeded benchmark concordance from independently measured accuracy. The rewrite was merged in [PR #168](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/168) as `a052b5b97fe2518497cddda8a45c76d80cb864a0` and deployed by [Pages run #42875399023](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42875399023). Exact-main verification [#42875399018](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42875399018) passed 350 Python, 155 Node and 22 Chromium tests. See [the content rewrite plan](docs/superpowers/plans/2026-11-10-lao-site-content-rewrite.md).

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

**Latest completed benchmark evidence (2026-11-10, schema 8.0):** on the pinned 100-word MekongPhon held-out lexicon, ClippyFirst deterministic and Hybrid v2 each score **90/100 segmental exact (5.48% CER; chrF++ 89.13)**; MekongPhon Neural scores 82/100 (6.64%; 87.42); Lao2IPA 1.0.0 scores 68/100 (8.97%; 72.95). Hybrid v2 and MekongPhon Neural each score 74/100 tonal exact (8.29% CER). The deterministic engine's native contour convention scores 25/100 (22.78% CER), or 69/100 (11.28%) after evaluation-only contour conversion. All four return visible output for 100/100 forms, while ClippyFirst has accepted segmental IPA for 97/100; provisional hints and unknown markers remain separate from accepted IPA. This is dictionary-seeded concordance, not independent expert accuracy; the held-out vocabulary influenced model validation/checkpoint selection. **Independent adjudicated IPA gold remains 0.** See the [schema-8 engine inventory](docs/research/LAO-G2P-ENGINE-AND-DATASET-INVENTORY-2026-11-08.md) and [benchmark run #42863119499](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42863119499).

**Latest sentence-domain stress evidence (2026-11-10):** on 1,000 HVULao sentences, the three-engine run reports 934/1,000 complete neural source-IPA outputs and 661/1,000 deterministic complete-IPA outputs; the deterministic hybrid visibly renders Ukrainian-side output for 1,000/1,000. The separate Hybrid v2 stress run also renders 1,000/1,000, with 66.1% complete segmental IPA sentences, 22.8% parseable tonal IPA rows, 10 fully and 4 partially aligned tone rows, and zero unexpected runtime errors; the model explicitly rejects 61 token-limit and 5 unsupported-character inputs rather than truncating. HVULao has no IPA reference, so these are coverage/runtime measurements, not accuracy. See [three-engine stress run #42863119212](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42863119212) and [Hybrid v2 stress run #42863119174](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42863119174).

Known limitations remain explicit: lexical word-boundary detection (the parser can structurally segment supported syllables within a token but does not infer lexical words), low-confidence fallback for unresolved structures, restricted initial clusters, full tonal treatment of ໜ/ໝ, Pali/Sanskrit output, lexical exceptions/conventional names, and empirical accuracy against an adjudicated gold corpus. Short-vowel glottal closure is also analysis-dependent: Ueda (1994), Lew (2014) and Cole (2016) describe different phonological, suprasegmental and prosodic accounts. The project therefore keeps /ʔ/ separate from the written coda-grapheme inventory and does not insert it after every short vowel. Rendering coverage, typed IPA coverage and phonetic accuracy are reported separately. The current 100% rendering figure means every tested input receives a visible output, not that every unit has supported IPA or a verified pronunciation.

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

Start at the [documentation index](docs/README.md). The latest [repository structure and branch-consolidation audit](docs/audits/current/REPOSITORY-AND-BRANCH-CONSOLIDATION-2026-11-15.md); the [10 November continuation audit](docs/audits/current/REPOSITORY-AND-DOCUMENTATION-CONTINUATION-2026-11-10.md) records the current mainline, PR reconciliation, documentation authority, verification evidence and blockers. The [codebase map](docs/agents/codebase-map.md) traces implementation entry points and data ownership. The index identifies the canonical specification, evidence, audit registers, implementation map and historical records. For development and review conventions, see [CONTRIBUTING.md](CONTRIBUTING.md). The canonical execution ledger remains [MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md](docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md). The [Ukrainian practical transcription guide](docs/lao-ukrainian-practical-transcription.md) documents the IPA-conditioned target conventions.

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

The Python package also exposes the model's source-side stage independently:

```python
from lao_ukrainian import transcribe_ipa, transcribe_lao

# Stage 1 only: Lao orthography → typed IPA; no Ukrainian mapping runs.
ipa = transcribe_ipa("ສະບາຍດີ", device="cpu")
print(ipa.raw_ipa, ipa.phonetic_result, ipa.model_revision)

# Explicit two-stage path: typed IPA → Ukrainian practical output.
result = transcribe_lao("ສະບາຍດີ", device="cpu")
print(result.raw_ipa, result.ukrainian)
```

Both entry points require the optional `.[neural]` dependencies and use the pinned model revisions by default. `transcribe_ipa()` returns `MekongPhonIPAResult`; `transcribe_lao()` continues through the existing typed IPA → Ukrainian adapter. Neither changes the deterministic `analyze()` default or the static website. See the [full integration and provenance contract](docs/research/MEKONGPHON-NEURAL-INTEGRATION.md).

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



### Browser neural Hybrid v2 deployment status

The optional browser-local neural Hybrid v2 panel was deployed temporarily by PR [#158](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/158) and Pages run [#42776069784](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42776069784). It was **retired on 2026-11-10 by explicit owner decision**. The retirement removed the ONNX export/model packaging from the Pages workflow and restored a static deterministic-only build (commits [0846e377](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/commit/0846e3773e328643740375947dc24067b3c664dd) and [afa035d](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/commit/afa035d882f2d2e4726e2da4459d467648bd9ba3)). Current Pages build asserts that no model directory, ONNX/WASM vendor bundle, Hybrid v2 inference bundle or neural UI control is present. The deterministic hybrid shell remains on the website. The Python Hybrid v2 research/CLI implementation is separate. Do not restore the retired browser neural lane without a new explicit owner decision.

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


## Research update — Lao orthographic syllable grammar (2026-11-17)

A historical Lao orthographic syllable grammar and ambiguity model have been located in Berment's 2004 thesis and Del Vigna & Berment (2003). The thesis describes a grammar over initial consonant groups, positional multi-grapheme vowel patterns, optional accent and restricted codas; it reports 56,670 generated candidate strings and a 33-state/480-transition automaton. It also warns that the grammar accepts unattested forms and simplifies accent placement. Its graph model preserves ambiguous segmentation paths and prunes dead branches; its longest-candidate choice is a local UI heuristic, not a global linguistic resolver. No historical code has been copied and no license is assumed. This is a valuable research basis, not a validated modern parser. Exact grammar terminals, Unicode/dialect reconciliation, adversarial tests and Lao-specialist review remain TODO. See [research note](https://app.undermind.ai/projects/5603c8d1-3260-4f39-b0d5-8fd6ffa3a081?path=/research/orthographic-parsing-boundaries-2026-11-16.md).


## Modern Lao orthographic structure research (2026-11-17)

New evidence from the Lao Script Generation Panel's 2017 proposal and ICANN's 2025 Root Zone LGR-6 describes Lao grapheme-cluster structure, pre-base/above/below/after vowel placement, tone-mark ordering, U+0EBC placement and special signs. These are useful constraints for a low-level grapheme analyzer, but the ICANN rules are scoped to DNS root-zone labels and deliberately omit many language spelling constraints; they are not a general Lao syllable spell-checker. The W3C Lao Layout Requirements document (2026-03-20) adds typographic guidance on spacing pre-base vowels, combining above/below marks and multipart vowels, but is an unendorsed Group Note Draft. The historical Berment grammar and these modern sources are complementary, not a complete modern grammar. No runtime code was changed pending a reviewed rule set and test corpus. See the direct-input audit and [romanization matrix](docs/romanization-to-ukrainian-matrix.md).


## Syllable segmentation vs word segmentation (Ishida, 2026-11-17)

Richard Ishida's [Lao Orthography Notes (updated 2026-04-28)](https://r12a.github.io/scripts/laoo/lo.html) says individual Lao syllable boundaries are comparatively straightforward to detect because vowels are explicit and coda letters are restricted. Lexical word boundaries are a different task: spaces mark phrases/sentences, and multi-syllabic words may require a language-specific dictionary or explicit ZWSP. The notes distinguish audible labialized onsets (`C + ວ`) from written high-class `ຫ` sequences (including `ຫຼ`), explain that pre-base vowels precede the entire onset, and warn that Unicode grapheme clusters are not syllables. Three source-backed orthographic segmentation tests were added; they are not pronunciation gold. This refines the earlier Berment ambiguity research: preserve ambiguity where it actually occurs, but do not assume ordinary Lao syllable boundaries are generally irreducible.


### Coda evidence reconciliation (2026-11-17)

The nine-item coda list in Ishida's explicit prose is consistent with the current consonants.csv final map, but the same page's consonant-class chart additionally lists ຢ. Its IPA correspondence table instead identifies ຍ as final /j/. The repository therefore does not add ຢ as a coda. An audit assertion and regression test now preserve this fail-closed boundary. codas.csv remains a phoneme-category table, not a grapheme inventory; implicit /ʔ/ after short vowels remains a separate dialect/phonetic question. No runtime mapping was changed.


## Exact-head verification — Ishida coda reconciliation (2026-11-17)

Verify #4525 / [run 44035119603 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/44035119603) passed on exact PR head `9b7d39b237a8dfa7e69544a1122ae1c1e2c3514e`. All configured checks passed: independent IPA-gold schema, repository/data/evidence audit, Python tests (including the new nine-coda map and fail-closed `ກາຢ` regression), external-G2P syntax/CLI, locked browser dependencies, browser engine tests, build/canonical browser-data generation, generated-data reproducibility, real Chromium UI tests, and built-page/relative-asset checks. No runtime, corpus, model, dictionary or generated artifact changed. Registry: 81 unique sources / 105 unique claims; no duplicate IDs or missing claim-source references. Branch comparison before this reporting-only sync: 131 ahead / 0 behind `main`; PR #247 remains open/unmerged.


## Exact-head verification — coda reconciliation and reporting sync (2026-11-17)

Verify #4526 / [run 44035383672 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/44035383672) passed on exact PR head `843b7695afd983b4dddd573eb570af80a71cbea2`. All configured steps passed: IPA-gold schema, repository/data/evidence audit, Python tests, external-G2P syntax/CLI, locked browser dependencies, browser engine, build/canonical data generation, generated-data reproducibility, real Chromium UI, and built-page/relative-asset checks. This head contains the coda source-conflict claim, nine-item audit invariant, fail-closed ກາຢ regression, and canonical docs/README synchronization. Registry: 81 unique sources / 105 unique claims; no duplicates or missing claim-source references. Branch comparison at this checkpoint: 132 ahead / 0 behind main. PR #247 remains open and unmerged; PR #145 remains open and untouched (24 ahead / 374 behind main; neural-first default conflicts with deterministic-default contract).
