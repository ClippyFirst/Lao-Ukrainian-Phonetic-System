## Unified Lao → IPA hybrid arbitration contract — 2026-11-08

The current `main` branch already has `hybrid-deterministic` as the default engine. This entry reconciles what “combine all engines” can mean without conflating IPA transcription, orthographic romanization, and model diagnostics.

### Existing implementation and verified coverage

- The production path is one deterministic engine: Lao Unicode → structural syllable parsing → Vientiane phonological baseline → evidence-gated MekongPhon-derived hybrid rules → typed IPA → Ukrainian adapter.
- The current hybrid rule registry contains nine aggregate vowel correspondences and two onset correspondences from the pinned MekongPhon training-split diagnostics. Selection is deterministic by priority/specificity; declaration order is irrelevant and equal-rank conflicting outputs raise a conflict.
- Hybrid rendering coverage is already `DONE_VERIFIED`: 1,000/1,000 HVULao inputs and 21,680/21,680 units; 100/100 held-out MekongPhon inputs and 169/169 units. The distribution includes SUPPORTED, UNCERTAIN, PROVISIONAL and passthrough units. This is not 100% supported IPA and not 100% phonetic accuracy.
- The merged hybrid default and the latest mixed-script / Lao-numeral rendering fixes remain in main. Frozen Vientiane and MekongPhon-reference profiles are compatibility profiles, not additional runtime voters.

### Engine integration matrix

| Engine / route | Role in the unified system | Why it is / is not a live IPA voter |
|---|---|---|
| Vientiane deterministic rules | Phonological baseline: syllable structure, segmental IPA and tone | Primary deterministic source; retained |
| MekongPhon-reference deterministic profile | Aggregate, train-split-derived IPA convention overrides | Already integrated into hybrid through 11 explicit rules; no model inference |
| MekongPhon tonal neural model | Optional external tonal IPA comparator | Not blindly merged: its flat output lacks trusted per-syllable alignment in the adapter; model disagreement is not proof of correctness |
| MekongPhon non-tonal neural model | Optional segmental IPA comparator | Cannot supply lexical tone; its non-tonal outputs must never overwrite or infer tone |
| Lao2IPA | External G2P comparator | Useful for differential diagnostics; not independent gold and not a source of automatic production exceptions |
| CLDR Lao-Latin / BGN-PCGN-aligned route | Separate orthographic romanization route | Not IPA; it omits phonological/tone information and must not vote on IPA or act as a fallback for phonetic uncertainty |
| Grapheme-position preview | Last-resort typed provisional hint source | Already used only through PROVISIONAL IPA-typed segments and UNKNOWN markers; never promoted to supported IPA |

### Deterministic arbitration policy

1. Parse the Lao source once and preserve source syllable boundaries, grapheme provenance and passthrough units.
2. Generate the default IPA from the Vientiane phonological baseline.
3. Apply only the 11 existing hybrid overrides whose provenance is recorded. A future override needs context-level evidence, a pinned source, a held-out comparison and a regression fixture; a frequency count alone is insufficient.
4. Treat neural and external G2P outputs as diagnostics unless a future adapter can prove source alignment, tone scope, model revision, and independent evaluation. Non-tonal engines may corroborate segmental phones only; they cannot decide tone.
5. Route only typed IPA / typed provisional segments through the Ukrainian adapter. Keep romanization outside this path.
6. If evidence conflicts or a structural parse is unsupported, preserve a deterministic visible result with UNCERTAIN / PROVISIONAL / UNKNOWN status. Do not hide the unit, guess a tone, or present an unresolved choice as certain.

This removes *algorithmic* ambiguity (same normalized input and same engine/data revision yield the same selected output). It cannot honestly remove *linguistic* ambiguity where sources disagree or evidence is absent. No majority vote can establish truth without an adjudicated reference.

### Task ledger

| Task | Status | Acceptance / blocker |
|---|---|---|
| One default deterministic hybrid path | DONE_VERIFIED | Default API / CLI / browser use `hybrid-deterministic`; typed IPA-first adapter boundary |
| 100% valid-input rendering | DONE_VERIFIED | HVULao 1,000/1,000 and 21,680/21,680 units; MekongPhon holdout 100/100 and 169/169 |
| Vientiane + MekongPhon aggregate hybridization | DONE_VERIFIED | 11 evidence-traced overrides; deterministic conflict rejection |
| Neural / Lao2IPA diagnostic comparison | PARTIAL | Existing optional adapters and benchmark evidence; no independent adjudicated IPA gold |
| Automatic multi-model voting into production IPA | DEFERRED | Unsafe without aligned per-syllable candidates, tone scope and independent adjudication |
| Zero linguistic ambiguity / guaranteed correct IPA | BLOCKED | Independent expert-adjudicated IPA gold remains 0; requires qualified Lao phonetics review |
| User-supplied long-text regression | BLOCKED | The supplied material contains generated outputs, not the original Lao source string; exact end-to-end reproduction is not possible from output text alone |

**Readiness:** engineering-verified research prototype. Rendering coverage is complete for the tested valid-input domain; phonetic accuracy and full-language structural coverage remain unverified.

---

## Final 1,000-row rendering-coverage acceptance — 2026-11-08

The BOM-normalized HVULao rerun passed the hard gate across the entire pinned dataset:

- Run [42518802702 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42518802702), artifact [13632219380](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42518802702/artifacts/13632219380), SHA-256 `75497805cc3e536a2fcc42b30501da140abc8a78f6a128001f8e7b109f55fef1`.
- Hybrid rendered **1,000/1,000 inputs (100%)** and **21,680/21,680 analyzed units (100%)**. There were zero invalid rows, zero unrendered inputs and zero runtime errors.
- Unit distribution: 16,452 SUPPORTED IPA, 19 UNCERTAIN IPA, 1,025 PROVISIONAL fallback units, plus 4,184 explicit passthrough units.
- IPA completeness remains separate: 17,120/17,496 phonetic syllables (97.8509%) and 676/1,000 complete IPA sentences (67.6%). The neural comparator completed IPA on 934/1,000 rows (93.4%); this does not compare like-for-like with hybrid rendering coverage.
- Hybrid mean all-attempt latency was 10.23 ms and p95 19.06 ms on this hosted CPU run.
- Leading U+FEFF BOM stripping converted the five formerly rejected rows into valid input; embedded BOMs remain rejected.

**HYBRID-RENDER-COVERAGE-001 is now DONE_VERIFIED** for the documented valid Lao-input domain, supported by both the held-out 100-entry and full 1,000-row coverage gates. This is not a phonetic-accuracy claim; HVULao supplies no IPA reference and independent adjudicated IPA gold remains 0.

## HVULao 1k rendering-coverage acceptance result — 2026-11-08

The first hard-gated 1k run passed **100% of valid inputs**:

- Run [42518022050 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42518022050), artifact [13632605494](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42518022050/artifacts/13632605494), SHA-256 `a90401fcd7e57a419a91f4a4baad48f19b38252af3134e10c41523d927bd432c`.
- Hybrid rendered **995/995 valid inputs (100%)** and **21,601/21,601 units**. Whole-dataset coverage was 99.5% because five rows contained a leading U+FEFF text-stream BOM and were rejected by the then-current normalizer.
- Hybrid unit counts: 16,410 SUPPORTED IPA, 19 UNCERTAIN IPA, 1,020 PROVISIONAL units; zero runtime errors.
- IPA completeness: 17,076/17,449 phonetic syllables (97.8623%); 673/1,000 complete IPA sentences (67.3%). These remain distinct from rendering coverage.
- Neural comparison completed 934/1,000 inputs (93.4% IPA-complete); its metric is not directly comparable to hybrid rendering coverage.
- The five BOM-prefixed rows were inspected: U+FEFF occurred only at the start of each row, as a text-stream marker. The normalizer now strips one leading BOM and still rejects embedded BOMs. A final 1,000/1,000 rerun is pending.

No IPA reference is supplied by HVULao; this is a text-domain coverage/runtime stress test, not phonetic accuracy. Independent adjudicated IPA gold remains 0.

## 100-entry rendering-coverage acceptance result — 2026-11-08

The held-out MekongPhon 100-entry workflow passed the new hybrid rendering-coverage gate on exact head `da9ec77bf9a203b4b86d36aefd6a5de8ec65a750`:

- Run [42518333013 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42518333013), artifact [13631884430](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42518333013/artifacts/13631884430), SHA-256 `0c91d91cff8f9e8fea99e2713e17ee4e2490fbb89a98cabc0ee803f471831b8f `.
- Hybrid rendering coverage: **100/100 inputs (100%)**, **169/169 units rendered**.
- Hybrid unit distribution: 159 SUPPORTED IPA units, 1 UNCERTAIN IPA unit, 9 PROVISIONAL placeholder units; zero runtime errors.
- Compatibility rendering coverage remains lower: Vientiane 95/100 and MekongPhon-reference 90/100. The hybrid-only fallback is responsible for the complete rendering coverage.
- IPA benchmark is unchanged in scope: 97/100 IPA-complete inputs (97%), 90/100 exact matches, CER 6.6445% against the pinned non-tonal dictionary reference. This is reference-relative, not independent accuracy or gold.
- On this benchmark, all 9 provisional units are included in rendering coverage but excluded from canonical IPA coverage and phonetic accuracy.

This verifies 100% rendering coverage on this 100-entry held-out set. It does **not** establish 100% coverage across all Lao text; the independent HVULao 1k stress gate remains in progress. Independent adjudicated IPA gold remains 0.

## Owner acceptance update — 2026-11-08: 100% rendering coverage

The owner clarified that the primary hybrid must cover **100% of valid input**, even when the result is low-confidence. Coverage means every accepted input unit receives a visible Ukrainian-side rendering; it does not mean every unit receives known IPA or correct pronunciation.

The hybrid distinguishes:
- SUPPORTED: evidence-backed IPA and ordinary Ukrainian adaptation.
- UNCERTAIN: a structurally complete IPA reading that can be rendered by the hybrid adapter, while remaining explicitly analysis-dependent.
- PROVISIONAL: no defensible IPA is available; registered grapheme-position hints, if available, are wrapped as PROVISIONAL IPA segments and unresolved graphemes become typed unknown markers. The same Ukrainian adapter maps the provisional IPA runs and renders ? at unknown positions. The original Lao surface, warnings and provenance remain available on the analysis record.

This is not a direct grapheme-to-Ukrainian bypass. The placeholder is not an IPA phone, is not included in IPA coverage, and must never be scored as a phonetic prediction. The frozen Vientiane and MekongPhon-reference profiles retain their prior withholding behavior. Invalid Unicode/script input remains rejected; the 100% target applies to the documented valid-input domain.

Benchmarks must report separately: (1) rendering coverage, (2) evidence-backed IPA coverage, (3) uncertain/provisional fallback shares, and (4) phonetic accuracy only against independent adjudicated gold. A complete rendering can coexist with low or unknown phonetic accuracy.

# Hybrid deterministic Lao IPA engine — 2026-11-08

## Scope and status

This continuation adds a third, explicitly selected deterministic profile:

`hybrid-deterministic`

It does not replace the Vientiane default, change the neural CLI default, merge existing PRs, or make any linguistic-accuracy claim. The profile combines the Vientiane rule engine as the base phonological analysis with the existing MekongPhon-reference aggregate correspondences through a deterministic rule selector.

## Execution design

Pipeline remains:

`Lao orthography → structural syllable parser → Vientiane phonological baseline → evidence-scoped hybrid rule selection → typed IPA → Ukrainian adapter`

The selector:
- evaluates parsed onset, onset class, vowel ID/length, coda and tone-mark context;
- ranks applicable rules by explicit priority and then condition specificity;
- does not depend on declaration order;
- raises a conflict error if equally ranked applicable rules disagree;
- preserves baseline IPA when no evidence-backed rule matches;
- records both the legacy profile provenance and a stable `HYBRID-RULE:<rule_id>` trace.

The Python selector is in `src/lao_ukrainian/hybrid_rules.py`; the profile rule registry and adapter are in `src/lao_ukrainian/mekongphon_reference_profile.py`. The browser implementation has the same profile contract and matching behavior in `web/engine.js`.

## Evidence boundary

The first hybrid rule set deliberately reuses only the nine vowel-structure and two onset correspondences already transferred from the pinned MekongPhon training split (6,219 rows). It does not introduce new IPA values or claim new contextual exceptions. Current evidence supports aggregate correspondences, but does not yet justify narrowing each one to a specific onset/coda/tone environment. The selector supports richer conditions so that later rules can be added only when the context counts and provenance are available.

`mekongphon-reference` remains available as a compatibility profile. `vientiane` remains the default. The new `hybrid-deterministic` profile is opt-in in the Python API, CLI and browser engine API. No neural dependency or fallback is added.

## Verification added

- Python regression coverage for baseline preservation, hybrid output/provenance, unchanged tone, CLI selection, rule specificity independent of declaration order, and equal-rank conflict rejection.
- Browser regression coverage for output/provenance parity, Vientiane fallthrough, uncertain /r/ status and invalid-profile rejection.
- The 100-entry held-out MekongPhon benchmark and HVULao 1k sentence stress benchmark now include the hybrid profile as a separate engine.
- Benchmarks remain reference-relative or coverage/runtime stress only. They do not establish independent phonetic accuracy.

## Remaining work

1. Run exact-head Python, Node, Chromium, data-audit, clean-install and build gates; fix any failures and rerun.
2. Run both frozen benchmarks with the hybrid engine and compare exact outputs, coverage, rejection counts and latency.
3. Add context-conditioned IPA rules only from inspectable aggregate evidence with separate training/evaluation splits and explicit support thresholds; do not promote a rule from count alone.
4. Investigate the 399 structurally withheld MekongPhon train rows and HVULao unresolved syllables using primary orthographic/phonological evidence. Keep ambiguous forms withheld.
5. Add independently adjudicated Vientiane IPA gold before claiming Neural-level phonetic accuracy. Current independent gold remains 0.

## Readiness

**PARTIAL / engineering implementation under verification.** This branch is not release-ready. Existing Vientiane and MekongPhon-reference profiles are preserved, and the production default remains unchanged.


## First hosted held-out result

The updated MekongPhon 100-entry workflow completed successfully on branch checkpoint `4afd51964532dd1f95b57eaeac36aea852b85228`:

- Run [42507131648](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42507131648), artifact [13628190784](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42507131648/artifacts/13628190784), SHA-256 `7de8665161308fcaaa422c5c3534e181916c1958f59e88786c3521215d7f8c86d`.
- Dataset: pinned 100-row `lao_eval.csv`, reference `pron_no_tones`; neural comparator is the pinned non-tonal checkpoint.

| Engine | Exact / 100 | CER / 100 | Coverage | Mean latency |
|---|---:|---:|---:|---:|
| Vientiane rules | 69 | 11.46% | 97% | 1.79 ms |
| MekongPhon-reference | 90 | 6.64% | 97% | 1.40 ms |
| Hybrid deterministic | **90** | **6.64%** | 97% | **1.41 ms** |
| MekongPhon Neural | 82 | 6.64% | 100% | 60.51 ms |

On the identical 97-word coverage subset, hybrid and MekongPhon-reference each achieved 90/97 exact matches and CER 1.40%; Neural achieved 81/97 and CER 5.79%. Hybrid runtime errors: 0. The three withheld cases and warning categories are unchanged.

This establishes that the new selector preserves the earlier profile's measured output on this held-out set and adds negligible overhead. It does **not** show that new contextual generalization has been learned: the hybrid intentionally uses the same eleven mappings, and the reference is dictionary-seeded, non-tonal and not independently adjudicated gold. Hybrid IPA-complete coverage remains 3 percentage points below Neural on this test; the later 100-entry rendering-coverage acceptance result is reported separately below.


## Exact-head engineering verification and 1k stress result — 2026-11-08

Final implementation checkpoint before this documentation update: `c705cf8ad782246c2d72c0d789a5e44e5196eca6`.

- Exact-head Verify [#42508759262 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42508759262): 280 Python tests, 134 Node tests and 17 Chromium tests passed. Corpus validation, evidence/data audit, optional external-G2P CLI checks, clean locked browser dependency install, browser build, generated-data reproducibility and built-site checks passed.
- Exact-head HVULao 1k benchmark [#42508759241 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42508759241), artifact [13628229661](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42508759241/artifacts/13628229661), SHA-256 `145966638988265a8f255163288e48de4fa8a0293941f0ec26643c7211fe7149`.
- Vientiane, MekongPhon-reference and hybrid each completed 669/1,000 sentences (66.9%), with 97.85% IPA construction across Lao syllables and zero runtime errors.
- Hybrid all-attempt latency: mean 16.28 ms, median 15.31 ms, p95 30.32 ms. Neural completed 930/1,000 (93.0%) with all-attempt mean 375.98 ms and p95 725.19 ms.
- The updated explicit passthrough policy preserves common ASCII and observed punctuation unchanged and excludes those units from IPA-coverage denominators. This improves mixed-text acceptance; it does not assign IPA to punctuation or explain the remaining 331 incomplete rows.
- The hybrid selector still does not increase structural coverage over the Vientiane baseline. It provides a deterministic route to the same 100-entry held-out reference-relative result previously recorded above, but no independent gold or tonal validation exists.

### Current conclusion

**Engineering implementation is verified.** Evidence-backed IPA coverage remains below Neural on the HVULao stress set and linguistic accuracy is not independently validated; the separate 100-entry rendering-coverage acceptance result is 100% via explicitly PROVISIONAL fallbacks. The next legitimate implementation work is to resolve parser-withheld orthographic structures using primary Lao orthography/phonology evidence and independent regression examples. The documented warning families remain fail-closed; do not lower parser safeguards or add exceptions solely to increase the 66.9% score.


## Source-backed parser work queue — 2026-11-08

This section records external linguistic/script evidence used to scope the next deterministic parser improvements. It does not treat these sources as new IPA gold or automatically authorize phonological mappings.

1. **Lao Script Resources, W3C Internationalization Working Group, Group Note Draft (20 March 2026).** The overview states that spaces separate phrases rather than words; multipart vowels may combine up to four glyphs plus a tone mark and can surround base consonants on multiple sides; vowels may be written differently in open and closed syllables; Lao native digits are commonly used. [W3C source](https://www.w3.org/TR/laoo-lreq/). This supports preserving Lao digits as explicit non-IPA passthrough and reinforces that parser logic must operate on grapheme structure, not whitespace-delimited words. It does not provide a Vientiane IPA mapping table.

2. **N. J. Enfield, A Grammar of Lao (2007), Chapter 3, Phonotactics.** The described word template is `C0 V0 C1 V1 V2 C2`; if the minor-syllable slots C0/V0 occur, both are realized, and the minor syllable is unstressed without an independent distinctive tone. The same chapter restricts minor-syllable onset and vowel inventories. [Publisher-hosted preview](https://api.pageplace.de/preview/DT0400.9783110207538_A19080877/preview-9783110207538_A19080877.pdf), pp. 33–34. Important limitation: the book's stated empirical basis is everyday semi-rural speech, not a dedicated contemporary Standard Vientiane reading corpus. Treat this as a parser research hypothesis, not a production rule.

3. **Reiko Ueda, “The Phonology of the Vientiane Dialect of Lao” (1994), J-STAGE.** The abstract describes the central Vientiane consonant/rhyme/tone structure and notes an exceptional unstressed, tone-neutral /a/ syllable without a final consonant in non-final position in a polysyllabic word. [J-STAGE record](https://www.jstage.jst.go.jp/article/gengo1939/1994/106/1994_106_95/_article). This is a stronger dialect match for investigating the minor-syllable exception, but the abstract alone is insufficient to implement all graphemic conditions.

### Implementation decisions

- **DONE_VERIFIED:** Lao native digits U+0ED0–U+0ED9 are now preserved unchanged as explicit `PASSTHROUGH` units in Python and browser runtimes. They receive no IPA and do not enter the Ukrainian IPA adapter. Dedicated regression tests were added in both runtimes.
- **PARTIAL / evidence-limited:** the full Ueda article has now been inspected. Its p. 112 describes a restricted non-final CV- light syllable in polysyllabic Vientiane words, with short open /a/, no coda, reduced stress and no distinctive lexical tone contour. The engine already has a deliberately narrow initial open-/a/ candidate guard (`VNT-POTENTIAL-MINOR-OPEN-A-UNRESOLVED`) and withholds the independent tone rather than assigning a guessed neutral contour. Do not broaden this to medial syllables or arbitrary open short vowels until the exact orthographic environments are grounded in the full study and hand-reviewed Vientiane fixtures. Enfield's C0V0 template is corroborating structural evidence but comes from a different, semi-rural speech corpus.
- **TODO / evidence-limited:** review all multi-part vowel patterns against the W3C script model and the project's canonical vowel registry. W3C confirms orthographic complexity but is not itself a phonological reference; each IPA mapping still needs a Vientiane phonological source.
