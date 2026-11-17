

## Exact-head verification — coda reconciliation and reporting sync (2026-11-17)

Verify #4526 / [run 44035383672 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/44035383672) passed on exact PR head `843b7695afd983b4dddd573eb570af80a71cbea2`. All configured steps passed: IPA-gold schema, repository/data/evidence audit, Python tests, external-G2P syntax/CLI, locked browser dependencies, browser engine, build/canonical data generation, generated-data reproducibility, real Chromium UI, and built-page/relative-asset checks. This head contains the coda source-conflict claim, nine-item audit invariant, fail-closed ກາຢ regression, and canonical docs/README synchronization. Registry: 81 unique sources / 105 unique claims; no duplicates or missing claim-source references. Branch comparison at this checkpoint: 132 ahead / 0 behind main. PR #247 remains open and unmerged; PR #145 remains open and untouched (24 ahead / 374 behind main; neural-first default conflicts with deterministic-default contract).


## Exact-head verification — Ishida coda reconciliation (2026-11-17)

Verify #4525 / [run 44035119603 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/44035119603) passed on exact PR head `9b7d39b237a8dfa7e69544a1122ae1c1e2c3514e`. All configured checks passed: independent IPA-gold schema, repository/data/evidence audit, Python tests (including the new nine-coda map and fail-closed `ກາຢ` regression), external-G2P syntax/CLI, locked browser dependencies, browser engine tests, build/canonical browser-data generation, generated-data reproducibility, real Chromium UI tests, and built-page/relative-asset checks. No runtime, corpus, model, dictionary or generated artifact changed. Registry: 81 unique sources / 105 unique claims; no duplicate IDs or missing claim-source references. Branch comparison before this reporting-only sync: 131 ahead / 0 behind `main`; PR #247 remains open/unmerged.
## Ishida coda inventory reconciliation — 2026-11-17

| Workstream | Status | Evidence / acceptance |
|---|---|---|
| Nine explicitly enumerated modern Lao coda spellings | DONE_VERIFIED (source-to-registry consistency only) | Ishida's explicit final-position list enumerates ບ ດ ກ ມ ນ ຣ ງ ວ ຍ; all nine already have corresponding ipa_final values in consonants.csv. The audit and a focused regression now enforce the exact map. This is not independent IPA gold. |
| ຢ as a coda | BLOCKED / source-internal conflict | Ishida's consonant-class chart includes ຢ in the coda row, but the explicit nine-item final-position list omits it and the IPA correspondence table maps final /j/ to ຍ. Runtime remains fail-closed; acceptance requires independent primary evidence or Lao-specialist adjudication. |
| Short-vowel /ʔ/ realization | PARTIAL / evidence-limited | Ishida says /ʔ/ occurs after short vowels, but this is a phonological final, not one of the nine ordinary final graphemes. Whether to emit /ʔ/ categorically in the project's selected dialect profile needs explicit phonetic adjudication and positive/negative fixtures. |
| data/lao/codas.csv semantics | PARTIAL | It is a phoneme-category table, not the parser's grapheme-to-final map; _find_coda reads consonants.csv. Keep /ʔ/ and analysis-dependent /l,r/ distinct from orthographic final-letter inventory. |

**Registry:** 81 unique sources / 105 unique claims expected after this update; no duplicate IDs or missing source references. **Readiness:** engineering-verified partial research prototype, not release-ready.

---

## PR #247 — exact-head verification and status refresh (2026-11-16)

| Workstream | Status | Current evidence / acceptance |
|---|---|---|
| PR #247 documentation/evidence reconciliation | DONE_VERIFIED (exact latest-head CI) | Verify #4493 / [run 43962408396 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43962408396) passed on latest PR head `268fc506b6dcecce5e8fbfac0c6d483d95e277e3`. All configured checks succeeded: IPA-gold schema, repository/data/evidence audit, Python tests, external-G2P harness syntax/CLI, locked browser dependencies, browser engine tests, build/canonical-data generation, generated-data reproducibility, real Chromium UI tests against the built site, and built-page/relative-asset checks. This exact-head run includes the Note 10 glyph-evidence correction across the source/claim registry, direct-input audit, completion register, README, handoff, branch audit and romanization matrix. Linguistic blockers remain unchanged. |
| ALA-LC Note 8 | DONE_VERIFIED + DEPLOYED | PR #241 merged; separate Lao digit → Arabic numeral route and post-deploy smoke tests documented in prior checkpoint. |
| ALA-LC Note 9 | PARTIAL / BLOCKED | Three LOC branches: ordinary Lao shortest standalone written form; Pali/Sanskrit same; other loans follow original-language division. ICU/HVULao baseline is exploratory only. Need LOC-specific lexeme policy, item-level upstream rights, source-located examples and Lao-specialist adjudication. |
| ALA-LC Note 10 | PARTIAL / fail-closed | Preferred LOC 2012 Word source confirms `ຄຼິສຕຽນ (khitsatīan)`; published 2012 PDF conflicts with `ຫຼັກສາດ (khitsatān)`. LOC instructs users to copy from Word rather than PDF. The source discrepancy is recorded; tests still inject source roles manually and automatic source-script syllabification remains unimplemented. |
| ALA-LC Note 6 | PARTIAL / fail-closed | Initial-ayn source trace exists; Ukrainian target correspondence remains unapproved. |
| Independent IPA gold | BLOCKED | 0 independently adjudicated examples; qualified annotators and adjudication are absent. |
| Lao specialist review | BLOCKED | No qualified independent sign-off. |
| Lao-specific RTGS | BLOCKED | No authoritative complete Lao-specific adaptation table; do not substitute Thai RTGS or treat BGN/PCGN as universal phonetic transcription. |
| Accessibility/device QA | PARTIAL | Automated Chromium coverage exists; manual screen-reader, keyboard-only and physical-device QA remain. |
| PR #145 neural-first architecture | DEFERRED / owner decision | Open and divergent (24 ahead / 374 behind; 13 files); conflicts with deterministic-default contract. Leave untouched pending explicit owner decision. |
| LOC Lao Word source | DONE_VERIFIED (retrieved and inspected) | Official `lao.doc` retrieved with HTTP 200 (`application/msword`) and inspected. It is the preferred copying source per LOC's index; its Note 3/10 form differs from the published PDF, and the discrepancy is recorded. |

**Registry integrity:** 77 unique source IDs and 90 unique claim IDs; no duplicate IDs and no missing claim-to-source references. **Repository readiness:** engineering-verified partial research prototype, not release-ready.

---

## ALA-LC Note 9 — ICU word-break baseline follow-up (2026-11-16)

| ID | Status | Evidence / acceptance |
|---|---|---|
| ALA-LC-NOTE-9 | PARTIAL / BLOCKED | PR #245 merged as `8e8622b007452c20f68dfbfed1edcb709d6bdc41`. Exact-head Verify #4427 / [run 43932311368 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43932311368) and post-merge main Verify #4428 / [run 43932522643 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43932522643) passed 355 Python, 204 Node and 30 Chromium tests plus all configured audits/build/reproducibility gates. Pages #106 / [run 43932522626 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43932522626) passed deployment and post-deploy HTTP smoke tests. Offline baseline: 839/1,000 exact character-stream-aligned pairs, 49,608 within-Lao candidate boundaries; longest-prefix F1 0.8636, naive shortest-prefix F1 0.5129. Filtered result not comparable to the paper's 0.75 model F1; neither algorithm implements LOC's shortest-standalone-form/loanword clauses. No corpus or dictionary data imported. Acceptance remains LOC-specific policy, item-level rights review, source-located examples and Lao-specialist adjudication. See `scripts/benchmark_lao_word_boundaries.py` and the direct-input audit.

## PR #243 — post-merge evidence checkpoint (2026-11-16)

| ID | Status | Evidence / acceptance |
|---|---|---|
| ALA-LC-NOTE-9 | PARTIAL / BLOCKED | PR [#243](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/243) merged as `fccff4bae4a4bbc0c7a4d2d9837a874ed72059bd`. Exact-head Verify #4391 / [run 43930231174 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43930231174): 350 Python, 204 Node, 30 Chromium; IPA-gold schema, repository/evidence audit, external-G2P syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks passed. This is evidence/documentation only; no runtime change. HVULao_NLP is a comparative candidate, not LOC gold; LDC/CrossAsia add source-origin and lexicalization context. Acceptance remains LOC-specific policy, rights-cleared/source-located examples and Lao-specialist adjudication. |

## ALA-LC Note 9 candidate assessment — 2026-11-16 (HVULao_NLP)

| ID | Status | Evidence / acceptance |
|---|---|---|
| ALA-LC-NOTE-9 | PARTIAL / BLOCKED (candidate evidence improved) | HVULao_NLP v2 publishes a minimal-orthographic-unit, context-sensitive segmentation guideline and reports native annotator review, linguist adjudication, and 5% double annotation. This is a stronger candidate for comparative boundaries than LaoNLP maximum matching, but it does not specify LOC's Pali/Sanskrit shortest-form clause or original-language boundaries for other loans. The journal article page lists CC BY 3.0 for the article, while the separate Mendeley dataset v2 lists CC BY 4.0; the paper says source websites permitted research/non-commercial reuse, and its table gives only domain-level aggregate counts, not item-level URL permissions. These licences do not settle commercial rights in upstream source texts; item-level source rights must be reconciled before importing text. No corpus/model imported. Additional orthographic evidence: LDC documents distinct Pali/Sanskrit vs recent-loan spelling conventions; CrossAsia DLLM shows historically conservative and lexicalized Indic forms in its cataloguing scope. Origin and lexicalization must be curated per lexeme, not inferred from graphemes. Acceptance: LOC-specific policy + rights-cleared and source-located adversarial examples across native compounds, productive morphology, function words, Pali/Sanskrit and other loans + Lao-specialist adjudication. |

## ALA-LC Note 8 implementation — 2026-11-16 (PR #241 exact-head verified)

| ID | Status | Evidence / acceptance |
|---|---|---|
| ALA-LC-NOTE-8 | DONE_VERIFIED (PR #241 exact-head) | `romanizeAlaLcNumerals` maps only Lao digits U+0ED0–U+0ED9 to 0–9 and preserves all other source content; the service exposes a separate Note 8 panel and copy action. Unit and browser regressions cover all digits, mixed scripts, ASCII digits and separators. Exact-head Verify #4383 / [run 43918104933 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43918104933) passed 350 Python, 204 Node and 30 Chromium tests plus IPA-gold schema, repository/evidence audit (including the LOC Note 8 source and claim), external-G2P syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks. LOC 2012 Note 8 is the primary source. PR #241 merged as `841826ce9981b1c09aa98179c790c63db1b2c982`; post-merge main verification remains. |

The existing phonetic Lao parser's native-digit passthrough and the direct Latin ALA-LC input path are intentionally unchanged. This implementation does not claim full Lao-script ALA-LC romanization.

## Post-merge reconciliation — PR #239 final verification (2026-11-16)

PR [#239](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/239) merged as `d1b3a7a3418aca83a6cb56a291007dcb0a36479c`. Exact-head Verify #4341 / [run 43870653366](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43870653366) and post-merge main Verify #4342 / [run 43870840263](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43870840263) passed 350 Python, 201 Node and 29 Chromium tests; repository/evidence audit, IPA-gold schema, external-G2P syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks passed. Documentation-only; Pages #104 remains the runtime deployment. A fresh paginated branch search returned 105 refs (104 non-main plus main). PR #145 is 24 commits ahead / 367 behind current main and remains an owner-level architecture decision.

## Post-merge reconciliation — PR #238 final evidence checkpoint (2026-11-16)

PR [#238](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/238) merged by squash as `8a37cde56a318c2a9fa047a6c2b17561762e8226`. Exact-head Verify #4339 / [run 43870127456](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43870127456) and post-merge main Verify #4340 / [run 43870313284](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43870313284) passed 350 Python, 201 Node and 29 Chromium tests. PR #238 reconciled README, completion register and canonical handoff with PR #237's post-merge branch-inventory evidence. Documentation-only; Pages #104 remains the runtime deployment.


## Post-merge reconciliation — PR #237 branch inventory refresh (2026-11-16)

- PR [#236](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/236) merged as `6512aac75cfb71c2d5f6f37a040f55739f32b14f`; exact-head Verify #4335 / [run 43868841677](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43868841677) and post-merge Verify #4336 / [run 43869109467](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43869109467) passed 350 Python, 201 Node and 29 Chromium tests.
- PR [#237](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/237) merged as `0f4dd825db25801bca4d350735253c5885f63ddf`; exact-head Verify #4337 / [run 43869513471](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43869513471) and post-merge Verify #4338 / [run 43869727851](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43869727851) passed 350 Python, 201 Node and 29 Chromium tests. No runtime changes; Pages #104 remains the runtime deployment checkpoint.
- The branch inventory at the time of PR #237 contained 102 refs (101 non-main plus main); only PR #145 was open. Six relevant divergent historical branches were compared explicitly; none was a safe fast-forward candidate. No branch was deleted or force-updated.
- PR #145 compared with the latest main checkpoint `0f4dd825`: 24 commits ahead, 365 behind, divergent and `mergeable=false`. It remains an owner-level architecture decision.

## Current status reconciliation — 2026-11-16 (ALA-LC Notes 8–10 and LaoNLP)

**Current main at start of this documentation reconciliation:** `943ff111033e7212cbbbc8615035eb94ed1c9974`.
**Runtime commit deployed by GitHub Pages #104:** `e6b1d564a20b88945dc0277b8db38efcd5834c8e`.
**Latest exact-main documentation verification:** Verify #4334 / [run 43868172458 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43868172458): 350 Python, 201 Node and 29 Chromium tests passed; IPA-gold schema, repository/evidence audit, external-G2P harness syntax/CLI, build, generated-data reproducibility and built-page checks passed.
**Independent IPA gold:** 0 adjudicated examples; benchmark gold remains header-only; empirical accuracy remains null.

| ID | Status | Evidence / next acceptance |
|---|---|---|
| ALA-LC-NOTE-8 | PARTIAL / route not implemented | LOC maps Lao digits ໐–໙ to 0–9. Current browser phonetic route preserves Lao numerals; direct ALA-LC mode accepts Latin input and therefore does not implement this source-script conversion. Acceptance: implement and test a distinct, explicitly typed Lao-source ALA-LC numeral romanization path, without changing phonetic passthrough semantics. |
| ALA-LC-NOTE-9 | PARTIAL / BLOCKED | LOC shortest-standalone-written-form and Pali/Sanskrit/other-loanword boundary rules require a reviewed lexical policy and appropriately rights-cleared resource. LaoNLP at pinned commit `a914f64e38ff24d67d32e37db40dad5c368ea602` was assessed in PR #234: maximum-match over a mixed-source composite is not equivalent; no data/code imported. |
| ALA-LC-NOTE-10 | PARTIAL / fail-closed | The PR #231 browser regression using `ຄິຼສຕຽນ` remains a mode-separation check only. The preferred 2012 Word source gives `ຄຼິສຕຽນ (khitsatīan)`; the published 2012 PDF instead gives `ຫຼັກສາດ (khitsatān)`, a recorded source conflict resolved for copying by LOC's Word-source instruction. The current crosswalk fixture uses the Word romanization but injects source roles manually. Automatic Lao source-script syllabification and role derivation remain unverified. |
| ALA-LC-NOTE-6 | PARTIAL / fail-closed | Initial `ʻ` is traced against source Lao `ອ`, but no approved Ukrainian target mapping exists; unsupported medial vowel values remain withheld. |
| ALA-LC-FULL | PARTIAL | Notes 6, 8, 9 and 10 plus contextual vowel/ວ cases are incomplete; no full conformance claim. |
| LAO-GOLD-001 | BLOCKED | Requires qualified independent annotation/adjudication, fixed dialect/convention, source locators and rights-cleared examples. |
| LAO-SPECIALIST-001 | BLOCKED | No qualified independent Lao specialist sign-off. |
| LAO-RTGS-001 | BLOCKED | No authoritative complete Lao-specific RTGS adaptation table and reviewed examples. |
| LAO-UI-001 | PARTIAL | Automated Chromium checks pass; human screen-reader, keyboard-only and physical-device QA remains outstanding. |
| PR-145-ARCH-001 | DEFERRED / owner decision | Open neural-first proposal is 24 commits ahead and 364 behind current main, mergeable=false. Do not merge without owner decision on architecture; deterministic-default web contract remains in force. |

### Recent merged evidence

- PR #231 — [browser integration guard](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/231), merged `e6b1d564`; exact-head Verify #4323, post-merge Verify #4324 and Pages #104 succeeded. Browser suite 29 passed; no runtime code change.
- PR #232 — [post-merge Note 10 evidence](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/232), documentation reconciliation.
- PR #233 — [Notes 8–9 route boundaries](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/233), documentation reconciliation.
- PR #234 — [LaoNLP candidate assessment](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/234), pinned source/code/license review; no adoption.
- PR #235 — [post-merge assessment evidence](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/235); exact-head and post-merge checks succeeded. Latest main Verify #4334 also passed.

**Readiness:** engineering-verified partial research prototype; not release-ready as a universal Lao-to-Ukrainian converter. Remaining blockers are linguistic evidence, approved target decisions, specialist adjudication, a rights-clean lexical resource, and manual accessibility/device QA—not a failing engineering CI gate.

---

## Current status reconciliation — 2026-11-10

**Implementation merge commit:** `68aa563ebc13da7e49da533e46301d43c13b5810`; PR #159 merged. Documentation checkpoint `ee6ced771fd5be553443741fb6007681bd4d2f31` passed Verify #42809109496.  
**Exact-head Verify:** [#42796863636 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42796863636).  
**Pages deployment and live smoke-test:** [#42797184810 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42797184810).

The primary hybrid guarantees visible Ukrainian-side rendering for unresolved valid input by wrapping registered positional hints in a typed `PROVISIONAL` IPA result and sending it through the normal IPA → Ukrainian adapter. Unknown positions remain `?`; browser and CLI disclose low confidence; tone is not inferred. Regression example: `ກາລ` → `кал?`. This does not increase accepted IPA coverage or empirical accuracy. Independent expert-adjudicated IPA gold remains 0.

**Clarification of older entries:** historical uses of “withheld” describe withholding an unsupported/unknown *phonetic claim* or tone, not a requirement to suppress all user-visible Ukrainian output. The primary `hybrid-deterministic` route now renders the provisional adapter result; frozen compatibility profiles retain their documented behavior. Historical metrics and old CI/PR states below remain immutable snapshots.

| ID | Current status | Evidence / next acceptance |
|---|---|---|
| LAO-GRAPHEME-PREVIEW-001 | DONE_VERIFIED (typed provisional IPA → Ukrainian adapter fallback) | Python, Node and Chromium regressions; Verify #42796863636; Pages smoke-test #42797184810. Visible rendering is not confirmed pronunciation. |
| LAO-GOLD-001 | BLOCKED | Independent expert-adjudicated IPA gold remains 0; qualified annotators, adjudication, fixed dialect/profile and convention, source locators and rights-cleared examples required. |
| LAO-PHON-001 | PARTIAL | Source-backed rule coverage and expert review of remaining tone/rhyme, segmentation and grapheme contexts remain incomplete. |
| LAO-ROM-001 | PARTIAL | Romanization crosswalk remains a separate lower-information orthographic method; full contextual acceptance remains required. |
| LAO-UI-001 | PARTIAL | Automated browser tests pass; manual screen-reader, keyboard-only, mobile-device and visual QA remain open. |
| LAO-REL-001 | PARTIAL / not release-ready | Deployment is technically verified, but independent gold and manual QA gates remain unmet. |
| PR-145-ARCH-001 | DEFERRED / owner decision | Neural-first proposal remains open and unmerged; adopted hybrid-deterministic default is unchanged. |

---

## MekongPhon evidence review — 2026-11-04

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| LAO-MEKONGPHON-001 | DONE_VERIFIED (owner-confirmed rights; candidate secondary source only) | LREC 2026 paper and PDF; seed lexicon from historical dictionary IPA; two-author 500-entry sample review (97.2% Lao / 99.2% Khmer); sentence expansion by longest-match-first lookup over OPUS; repository snapshot f80f6c1840c4818b51e05f2e00cded4701a5b662 has no declared license/root LICENSE. | May be used for source-located lexical triage only after profile/convention checks. Not independent sentence-level gold; do not import into gold.tsv. The repository owner confirms that the project's MekongPhon rights were fully resolved in the prior project conversation; do not treat rights as an active blocker. This does not promote the corpus to independent project gold. |

# Lao linguistic completion register — 2026-11-01

**Benchmark implementation merge:** `c50fc9133f8e7f55b520ac7229c86df2f9b10356` (PR #113). **Handoff/register reconciliation merge:** `44b475698c6532b202e06a14622ba57927843176` (PR #114).
**Latest post-merge exact-main evidence:** [engineering verification](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41707491721) SUCCESS.
**Open pull requests:** none at this checkpoint.
**Research boundary:** Independent expert-adjudicated Lao IPA gold remains 0; `data/benchmark/gold.tsv` is header-only; empirical accuracy remains null.
**Scope:** continue the existing master handoff; this register does not replace it.

## Held-out IPA benchmark integrity — 2026-11-03

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| IPA-BENCH-HELDOUT-001 | DONE_VERIFIED | PR #113 merged as `c50fc9133f8e7f55b520ac7229c86df2f9b10356`; exact-main verification [workflow](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41707491721) SUCCESS. Export preserves split bucket and frozen manifest seed/version; scoring defaults to held-out test; explicit all-split mode is marked diagnostic; malformed/mixed split metadata and empty predictions fail closed. | Engineering evaluation integrity only. Independent expert-adjudicated Lao IPA gold remains 0; `data/benchmark/gold.tsv` is header-only; empirical accuracy remains null. No gold rows, IPA labels or accuracy claims were fabricated. |


## Engineering integrity continuation — 2026-11-03

- **TSV-INPUT-001 — DONE_VERIFIED:** benchmark TSV ingestion now rejects duplicate/blank headers and nonblank rows with extra or missing fields; blank physical lines are ignored. Regression cases cover gold/prediction duplicate headers, extra gold cells, and truncated prediction rows.
- **Evidence:** test-first RED [41665707581](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41665707581); focused implementation GREEN [41665849910](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41665849910); implementation commit `832ca08431ddca0f081234fcd02fbc5e0b92053f`.
- **Acceptance boundary:** input shape is validated before scoring. This does not create adjudicated IPA data or alter language accuracy status (gold 0; accuracy null).

## Strict JSON syntax — 2026-11-03

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| JSON-INPUT-003 | DONE_VERIFIED | Reject `NaN`, `Infinity`, and `-Infinity` in JSONL and license registry inputs. RED 41692621208; implementation CI 41694083975 SUCCESS (166 Python tests; 4 built-site browser tests). | Reject non-standard JSON constants before corpus or rights validation; no linguistic labels or license terms changed. |

## License registry JSON integrity — 2026-11-03

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| JSONL-INPUT-002 | DONE_VERIFIED | Duplicate top-level and nested keys in `licenses.json` rejected. RED 41690095702; implementation CI 41690255691 SUCCESS (164 Python tests; 4 built-site browser tests). | Rights registry cannot silently apply last-key-wins semantics; no license permission is inferred or broadened. |

## JSONL input integrity — 2026-11-03

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| JSONL-INPUT-001 | DONE_VERIFIED | Duplicate top-level and nested JSON object keys are rejected. RED 41687363405; exact implementation-head CI 41687689017 SUCCESS (162 Python tests; 4 built-site browser tests). | Prevent silent last-key-wins corruption before corpus schema/provenance validation. No linguistic data or accuracy claims added. |

## Evidence-based task ledger

| ID | Status | Work remaining | Acceptance |
|---|---|---|---|
| LAO-GOLD-001 | BLOCKED | No independent expert-adjudicated lexical IPA gold exists; `data/benchmark/gold.tsv` contains only its header. | At least two independent qualified annotators, adjudication, dialect/profile and IPA convention fixed, source/audio locators retained; held-out split frozen before scoring. |
| LAO-PHON-001 | PARTIAL | Validate complete tone/rhyme interactions, multi-syllable segmentation and remaining uncertain grapheme combinations against primary sources and experts. | Every supported rule has scoped primary evidence, counterexamples and shared Python/browser fixtures; unresolved cases fail closed. |
| LAO-LAB-001 | PARTIAL | Labialized onsets are structurally represented but lack justified Ukrainian correspondences. | Expert-reviewed IPA inventory and target policy; otherwise remain IPA-only/unsupported, never guessed. |
| LAO-ROM-001 | PARTIAL | CLDR/BGN-derived crosswalk is provisional and does not cover every source structure; BGN `ຫຣ` remains unsupported. | Source-located full inventory, context rules, round-trip/ambiguity tests and explicit non-reversibility; separate from phonetic mode. |
| LAO-G2P-001 | DONE_VERIFIED (diagnostic harness only) | Goruut remains unsuitable for production. | Do not promote on comparator concordance; any new claim requires independent gold and repeatable full coverage. |
| LAO-UI-001 | TODO | Manual visual, keyboard, assistive-technology and mobile QA is not established by CI. | Recorded test matrix and results on deployed site. |
| LAO-REL-001 | PARTIAL | Production readiness blocked by gold, dialect adjudication and external asset rights if bundled. | All release gates in README/limitations met; no external asset shipped without rights clearance. |

## Current diagnostic evidence

The latest recorded 100-row MekongPhon/Goruut diagnostic is 81 outputs, 19 none; 47 complete, 34 partial, 19 unknown/no output; 68 stable and 13 unstable; 17 inputs had randomization metadata. These are source-coverage/repeatability diagnostics, not accuracy. The 37-row lao2ipa comparison had 0 exact implementation matches (31 tone-suffix-only, 2 offglide, 4 segmental/vowel-sequence differences). Independent gold remains 0 and accuracy must remain null. MekongPhon/Goruut are not imported as product gold or runtime assets.

## Execution order

1. Preserve fail-closed phonetic claims: do not invent IPA or tone. In the primary hybrid, do not suppress all Ukrainian-side output for unresolved valid input; render typed PROVISIONAL IPA through the ordinary adapter and retain explicit `?` markers and low confidence.
2. Commission an independently annotated, dialect-scoped audio/lexical sample; freeze annotation instructions before collection.
3. Resolve tone/rhyme and segmental disagreements against source-located evidence; add only adjudicated records to the gold split.
4. Complete the labialized-onset Ukrainian policy only if expert evidence supports a useful Ukrainian rendering.
5. Complete the CLDR/BGN contextual matrix independently of IPA.
6. Perform deployed UI/accessibility QA and a release/asset-rights review.

## External dependencies / blockers

- Qualified Lao phonologist and independent IPA annotators; no such human review can be fabricated by CI.
- Per-resource permission for any external dictionary/model/corpus redistribution.
- No local checkout was available to this execution; exact-main GitHub Actions are the engineering evidence. Run the repository's documented local release commands in a clean checkout before release.

## Method constraints

Preserve `Lao orthography → structural analysis → Lao phonology → typed IPA → Ukrainian adaptation`. Romanization remains a separate, lower-information orthographic mode. Engineering fixtures and source-attested comparator labels are not gold.


## Independent IPA gold corpus implementation — 2026-11-01

| Task | Status | Evidence / remaining acceptance |
|---|---|---|
| IPA-GOLD-SCHEMA-001 | DONE_VERIFIED | Record, annotation, adjudication, split and license schemas plus cross-file validator |
| IPA-GOLD-DOUBLE-ANNOTATION-001 | PARTIAL | Two distinct annotators enforced; blind intake requires external controlled collection |
| IPA-GOLD-ADJUDICATION-001 | PARTIAL | Agreement/resolved/unresolved logic and feature-complete IPA comparison; no real adjudicated rows |
| IPA-GOLD-RIGHTS-001 | DONE_VERIFIED (mechanism) | Allowlisted licenses, required rights evidence and rejection of unregistered/non-redistributable licenses; source-by-source legal review still required |
| IPA-GOLD-SPLIT-001 | DONE_VERIFIED | Deterministic hash-based group split; one frozen seed/version is enforced across the entire manifest, including distinct lexeme groups; new groups inherit the existing identity and conflicting overrides are rejected |
| IPA-GOLD-EXPORT-001 | DONE_VERIFIED | Rights-filtered typed IPA export retaining source/license/evidence locators |
| IPA-TYPED-BENCHMARK-001 | DONE_VERIFIED | Different or missing IPA kind cannot count as an exact match |
| IPA-GOLD-RELEASE-GATE-001 | PARTIAL | Tag/manual workflow requires 100/25/25 adjudicated train/dev/test; owner must require the check in release rulesets/procedure |

**Current gold:** zero independent expert-adjudicated records; `gold.tsv` remains header-only; accuracy=null. The new schemas, fixtures and source-attested literature are not gold labels. No phonetic data was invented.


**Research evidence artifact:** [Lao tone–rhyme evidence matrix](LAO-TONE-RHYME-EVIDENCE-MATRIX-2026-11-01.md). It records Ueda's central Vientiane five-tone baseline and explicitly marks all unverified tone × rhyme cells; Erickson's labialized consonants remain separate from the Vientiane tone profile.


**Source correction:** Erickson's paper is bibliographically 1996 (the SEA-language PDF filename says 2001). Its adopted six-tone/coda analysis is kept separate from Ueda's five-tone central Vientiane baseline. The proposed historical origin of labialized consonants remains tentative.


**Full-text evidence update:** Ueda (1994) pp. 96, 100–108, 110–112 now provides a speaker-specific Vientiane tone × rhyme matrix: plain rhymes allow five tones; long checked rhymes allow [21]/[52]; short checked rhymes allow [34]/[33]. A restricted [22] variant overlaps with [24] in some onsets/connected contexts. Ueda's one-informant sample and its conflict with Erickson's labialized-phoneme analysis remain explicit limitations.


**2026-11-01 closeout:** PR [#98](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/98) is the comprehensive implementation and research-matrix change. Its PR CI passed 134 Python tests and all four Node/browser suites (107 total). Main remains at 6f607d7. Gold remains 0; release readiness remains blocked on expert annotation, full feature coverage and owner-enforced release rules.


## 2026-11-01 final IPA-kind consistency verification

- Added fail-closed cross-annotation consistency: both independent annotations for one record must use the same `ipa.kind`, and a `RESOLVED` adjudicated result must preserve that kind. This prevents phonemic-vs-phonetic representation differences from being misclassified as pronunciation disagreements.
- Regression evidence: both new tests failed against the pre-fix validator on the test-only commit, then passed after the validator change.
- New task `IPA-GOLD-REPRESENTATION-KIND-001`: **DONE_VERIFIED** (mechanism and exact-head CI). Blindness, annotator qualifications and independent adjudicator competence remain external operational evidence, not properties CI can prove.
- Final PR head: `0b348d191e93e15b543d95538daccf8490e8239c`; CI run [41338456936](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41338456936) SUCCESS — 137 Python tests; Node/browser suites 50 + 23 + 27 + 7; data/evidence audit, generated-data reproducibility and production build passed.
- The Lao evidence matrix remains bounded to central/Vientiane source analyses; no automatic labialized-onset Ukrainian mapping was added.
- Gold remains zero; `gold.tsv` remains header-only; empirical accuracy remains null. No IPA labels were generated.


## IPA gold split-manifest runtime/schema parity — 2026-11-01

| ID | Priority | Status | Scope / evidence | Acceptance criteria / dependencies |
|---|---|---|---|---|
| LAO-IPA-SPLIT-STRICT-001 | P1 | DONE_VERIFIED | RED test on commit `945c81b4b4ddb4f48517549353f5a3e14b26bcad` failed as expected; GREEN code commit `af97613ae959b59825d1cb6c863ad85b3b5a44d2`; exact-head CI [41340390805](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41340390805) passed | The split generator and corpus validator share the closed split-field contract; unknown prior-manifest properties are rejected rather than silently dropped. No expert gold is created by this change. |


## Product-corpus license eligibility — 2026-11-01

| ID | Priority | Status | Scope / evidence | Acceptance criteria / dependencies |
|---|---|---|---|---|
| LAO-IPA-LICENSE-ELIGIBILITY-001 | P1 | DONE_VERIFIED | RED tests on `74b2349e7054950078f8d875103a30972b9bd7be`; GREEN code/schema commit `9d3cae33d742f86b9b9e741669da892504ef3dee`; exact-head CI [41340903259](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41340903259) passed | Registry and schema fail closed unless a redistributable product-corpus license explicitly permits commercial use and defines attribution/share-alike obligations. Human source-by-source rights review remains required. |


## Release-gate threshold validation — 2026-11-01

| ID | Priority | Status | Scope / evidence | Acceptance criteria / dependencies |
|---|---|---|---|---|
| LAO-IPA-RELEASE-THRESHOLDS-001 | P1 | DONE_VERIFIED | RED test on `5e34cf8cbce93ba1cc1bdc82b2de260c88b403de`; GREEN code commit `44c9de1804f9de47a72f297aa5ed544d90d3629e`; exact-head CI [41341723054](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41341723054) passed | All split minimums reject zero and negative values; threshold errors aggregate with other release-gate findings. Default minimums remain 100/25/25. |


## Audio-source review update — 2026-11-01

A current, small Lao audio candidate is now documented in `docs/ipa-gold-collection-playbook.md`: Common Voice Scripted Speech v27.0 (locale `lo`, catalogued CC0-1.0, MP3 archive 8.93 MB; official catalog https://commonvoice.allizom.org/en/datasets; release documentation https://github.com/common-voice/cv-dataset/tree/main/datasets/scripted-speech). The archive size is not a clip count. The v27.0 manifest still needs inspection for validated clips, speaker count, transcript coverage and dialect metadata. Common Voice supplies sentence audio/transcripts, not IPA.

**Ruling:** treat this as supplementary contextual audio and candidate discovery, not as the 30-item citation-form lexical gold source. The catalog does not prove Vientiane variety. Citation-form gold should use consented recordings from confirmed target-variety speakers unless manifest review establishes a suitable sample. Keep source clip IDs and time locators; do not infer IPA from transcripts or model output.

Status remains `LAO-GOLD-001 = BLOCKED`: no annotations, annotators or adjudications have been created. Independent gold remains 0 and accuracy remains null.


## Common Voice v27.0 manifest verified — 2026-11-01

The official release manifest `cv-corpus-27.0-2026-09-11.json` has been inspected (https://github.com/common-voice/cv-dataset/blob/main/datasets/scripted-speech/cv-corpus-27.0-2026-09-11.json). Lao metadata: 223 clips, 193 validated clips, 16 contributor IDs, 0.35 validated hours (0.40 total). No named accent or variant category is supplied. Gender metadata is 88.79% male / 11.21% unspecified. Locale checksum in the manifest: `3fe87d019e65ac7e97806390698804bb60dec02444cba372706739dd8fb260b6`.

This confirms the archive is small and profile metadata is insufficient to establish Vientiane speech. Common Voice remains a supplementary contextual source, not citation-form lexical IPA gold. The 30-item pilot can use it only if 30 suitable tokens are found and a specialist accepts the profile; otherwise use controlled elicitation. No data imported; `LAO-GOLD-001` remains `BLOCKED`, gold 0, accuracy null.


## Final exact-head verification — 2026-11-01

Branch `feat/ipa-gold-corpus-20261101-review`, source-audit content commit `440975c82c5005a24952ce883cea269aa3cb3198`. Lao exact-head CI: verify [41345121935](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41345121935) SUCCESS; optional Goruut [41345121928](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41345121928) SUCCESS; optional external G2P [41345121943](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41345121943) SUCCESS. Core job passed corpus structure validation, repository data/evidence audit, Python tests, browser engine tests, browser data generation/reproducibility, and built-pages/relative-asset checks.

These checks validate the committed repository and its automated engineering contracts. They do **not** validate the linguistic correctness of future human annotations, create gold labels, or change the release blocker. Gold remains empty and accuracy remains null.


## Follow-up handoff-head CI — 2026-11-01

The subsequent documentation-only handoff/register state at commit `072713627185ec5a3d0eaa2eb29fc23aa0cca77f` was also checked on its exact head: verify [41345372448](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41345372448) SUCCESS; optional Goruut [41345372474](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41345372474) SUCCESS; optional external G2P [41345372469](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41345372469) SUCCESS. These runs validate the updated documentation and existing automated checks, not future IPA annotations. Any later branch update must be checked again on its new exact head.


## Open-rights redistributability invariant — 2026-11-01

| Task | Status | Evidence / acceptance |
|---|---|---|
| LAO-IPA-RIGHTS-OPEN-001 | DONE_VERIFIED | A test-first regression rejected a source with `rights_status=OPEN` and `redistributable=false`; the runtime validator and record JSON Schema now both require `redistributable=true` for OPEN. Test-only RED commit: `f50619febaf7b75d5d1c65973a6cb1b1ba241973`. Fix/schema code head: `4e4327e7bfdf0789c6a67b99a2b53e2bdbbc772b`; exact-head CI run [41347942661](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41347942661) passed: 142 Python tests; Node/browser suites 50 + 23 + 27 + 7; data/evidence audit, generated-data reproducibility and production build passed; optional Goruut and external G2P passed. |

This is a consistency/eligibility invariant, not a new legal determination. It does not change source licenses, rights evidence, gold labels or measured accuracy. Independent adjudicated gold remains 0; accuracy remains null.

## Exact current-head engineering checkpoint — 2026-11-01

- Current code checkpoint: `5e5f3de73fa96696e8087220c24c5d245f38797d`; exact-head core CI [41348202260](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41348202260) **SUCCESS**. 142 Python tests; Node/browser suites 50 + 23 + 27 + 7; repository data/evidence audit, generated-data reproducibility and production build passed. Optional Goruut and external Lao G2P diagnostics passed.
- The `OPEN` / `redistributable` consistency regression is present in runtime validation, JSON Schema and tests.
- Independent expert gold remains 0 and accuracy remains null. Human annotation/profile/convention gates remain open; CI is not linguistic validation.

 
## Nested IPA record contract closure — 2026-11-01

| Task | Status | Evidence / acceptance |
|---|---|---|
| IPA-GOLD-NESTED-STRICT-001 | DONE_VERIFIED (engineering contract) | Test-first RED: [run 41352928328](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41352928328); GREEN exact-code-head CI: [run 41353028676](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41353028676). Runtime validator and JSON Schema both reject undeclared fields in `orthography`, `profile`, `source` and `source.rights_evidence`. 144 Python unittest tests passed; repository CI checks passed. |

This closes only the nested-object shape contract. It does not establish the truth of source metadata, rights determinations, speaker profiles, IPA, or expert adjudication. Independent gold remains 0 and accuracy remains null.


## Validator duplicate-call cleanup — 2026-11-01

| Task | Status | Evidence / acceptance |
|---|---|---|
| IPA-GOLD-DUPLICATE-VALIDATION-001 | DONE_VERIFIED | Removed four consecutive duplicate `reject_unknown_properties` calls from nested `orthography`, `profile`, `source`, and `source.rights_evidence` validation. Code commit: `7eea774803654372e7d400cd1fde7c9079c23a64`; Git blob SHA: `a072297e320b4b91a36c59fc90328b6ff98d2a5f`. - Core PR CI: https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41354242607 (SUCCESS); core push CI: https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41354237853 (SUCCESS); optional language diagnostics: https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41354242594, https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41354242625 (SUCCESS). |

This is dead-code cleanup only: each contract check remains once; no validation rule, schema, IPA value, phonology rule, or corpus row changed. The shared validator remains identical across Lao, Khmer and Burmese. Hosted CI only; no local checkout or local test command is claimed. Independent expert-adjudicated gold remains 0 and empirical accuracy remains null.


## Methodology source refresh — 2026-11-02

| ID | Status | Evidence / acceptance |
|---|---|---|
| ENGINEERING-METHOD-REFRESH-001 | DONE_VERIFIED | Updated `AGENTS.md` and canonical handoff to pin Superpowers 7.0.1, mattpocock/skills current main, and Ponytail 5.3.3. Exact-head CI on methodology commit `748b84d7c2af7e26191e5d1e12bf875800148a13`: [PR verify 41356347659](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41356347659) and [push verify 41356342591](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41356342591) SUCCESS; 144 Python tests, Node/browser suites 50 + 23 + 27 + 7; [Goruut 41356347649](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41356347649) and [external G2P 41356347662](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41356347662) SUCCESS. No runtime dependencies or copied skill bundles were added. |



## Methodology source refresh follow-up — 2026-11-02

| ENGINEERING-METHOD-REFRESH-002 | DONE_VERIFIED | Updated `AGENTS.md` and canonical handoff to mattpocock/skills v1.3.2 (`d1478fcb140db0b93c0c8df17bcfd311844749d0`); added two-axis review, genuine-RED evidence, template/ownership, and safe worktree-cleanup guidance. Verified documentation checkpoint `d964db76a4228f2a7f84138ef69cbe1ae8cb7086`: [verify 41358587062](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41358587062) SUCCESS; optional [41358587063](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41358587063) and [41358587151](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41358587151) SUCCESS. | No third-party code, data, skill bundle, or runtime dependency copied. |

## IPA gold adjudication required-field parity — 2026-11-02

| ID | Priority | Status | Scope / evidence | Acceptance criteria / dependencies |
|---|---|---|---|---|
| IPA-GOLD-ADJUDICATION-FINAL-IPA-001 | P1 | DONE_VERIFIED | A test-first regression demonstrated that an `UNRESOLVED` adjudication with the `final_ipa` property omitted was accepted by the Python runtime even though the JSON Schema requires the property (nullable). Test-only RED commit `2750382302a6f769be951f96587b04502d9900c6`; failing exact-head PR CI [41407007210](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41407007210). Runtime fix commit `7c0e758776262c8415116d6a404626d061642657`; exact-head PR CI [41407108435](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41407108435) SUCCESS. 145 Python unittest tests; browser engine tests, generated-data reproducibility, evidence audit and production build passed. |

The validator now requires the `final_ipa` key to be present for every adjudication. `UNRESOLVED` must supply explicit JSON `null`; `AGREEMENT` and `RESOLVED` still require a typed IPA object. No phonology rules, corpus labels, source data or benchmark scores changed. Optional diagnostic runs: [41407108369](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41407108369), [41407108418](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41407108418). Gold remains 0 and empirical accuracy remains null.


### Unresolved adjudication explicit-null positive-path coverage — 2026-11-02

The regression suite now also proves the valid complementary case: `decision=UNRESOLVED` with an explicitly present `final_ipa: null` is accepted and remains excluded from adjudicated gold. Test commit `dbbac42d4a4879d0bf340027037a3edba60063d2`; exact-head PR CI [41407386614](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41407386614) SUCCESS. 146 Python unittest tests; browser engine tests, generated-data reproducibility, repository evidence audit and production build passed. Optional diagnostics: [41407386667](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41407386667), [41407387018](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41407387018) SUCCESS. This does not create IPA labels or change the gold count (still 0) or accuracy (still null).

## External G2P engine coverage audit — 2026-11-02

- **PARTIAL (DONE_VERIFIED diagnostic execution):** `lao2ipa==1.0.0` ran 37 engineering fixtures: 0/37 external fixture matches; 31 tone-only heuristic differences and 6 segmental/offglide differences. Goruut source snapshot `b224bde` ran 100 source-attested cases: 4/100 exact matches, 19 failed outputs, 14 unstable engineering outputs, 47 complete / 34 partial / 19 unknown coverage. See `docs/research/external-g2p-benchmark-and-engine-coverage-2026-11-02.md` and Actions runs 41409083914 / 41409083978.
- **NOT SCORED:** independent expert-adjudicated IPA gold remains 0; no accuracy score is valid. Tone-stripped agreement is not an accuracy metric.
- **TODO:** inspect six non-tone Lao2IPA mismatches and all tone disagreements with qualified Lao reviewers; record upstream Goruut language-bundle absence of `weights9.bin.zlib` as BLOCKED pending upstream clarification or asset publication; benchmark MekongPhon Lao model on a profile-compatible held-out set.


## Goruut language-bundle asset status correction — 2026-11-02

The previous TODO wording suggesting that this repository can simply recover or fix `weights9.bin.zlib` is superseded. Inspection of the exact upstream Goruut source tree at `b224bde02151f8f86d0fe260804e4ca743bda620` shows no `weights9.bin.zlib` in `dicts/lao/`, `dicts/khmer/central/`, or `dicts/burmese/`; the earlier `weights7` and `weights8` assets are present. This is an upstream language-bundle omission in the pinned snapshot, not a missing project-owned file. Status: **BLOCKED (upstream dependency)**. Acceptance: upstream publishes the asset or documents the expected model-tier fallback, and a controlled same-input comparison plus independent expert IPA gold establishes whether the asset changes relevant language coverage. Do not synthesize weights, download unpinned substitutes, or treat the warning as a failed workflow. See the external-engine research audit and canonical handoff for the evidence.


## Additional MekongPhon transformer baseline inventory — 2026-11-02

| ID | Priority | Status | Evidence / acceptance |
|---|---|---|---|
| LAO-MEKONGPHON-TRANSFORMER-001 | P1 | TODO | Published tonal and non-tonal 33.6M-parameter BERT encoder–decoder models exist at [lao-ipa-tonal](https://huggingface.co/byumatrixlab/lao-ipa-tonal) and [lao-ipa-nontonal](https://huggingface.co/byumatrixlab/lao-ipa-nontonal). The non-tonal model explicitly omits tone and is not a complete comparator for this project's tonal target. Pin immutable revisions/checksums, verify dialect/IPA convention/split, and run a reproducible same-input held-out diagnostic with tone, segmental, length, coda and boundary metrics. Do not score against source-attested labels as independent gold. |


## Main publication reconciliation — 2026-11-02

Supersedes earlier handoff statements that the review branch was still ahead of `main` and unmerged: PR [#98](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/98) was merged into `main` as `ed36e7030df4ec8c1b70b50fdcfd6e47e5770d52`; this was the repository's current `main` tip at reconciliation. Exact-head engineering workflows on the PR head passed: verify [41413902679](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41413902679), Goruut [41413902653](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41413902653), and lao2ipa [41413902805](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41413902805). The Pages workflow is configured to deploy from `main`; the public site and post-merge deployment run could not be independently inspected from this session, so deployment status remains **BLOCKED (external verification/network access)**, not claimed successful. No UI/runtime files were changed by this PR. Independent expert-adjudicated gold remains 0 and accuracy remains null; the project is still a research prototype.


## IPA-GOLD-SPLIT-MANIFEST-IDENTITY-001 — 2026-11-03

**Status: DONE_VERIFIED (runtime validator and split generator).** Root cause: the previous cross-file validator checked seed/version consistency only within each `lexeme_group_id`, allowing distinct groups in one corpus manifest to carry different seeds or versions. The split generator could also add a new group under a newly supplied seed while preserving older groups, silently creating a mixed manifest.

- Added regression coverage for mixed seeds and mixed versions across distinct groups, plus conflicting seed override when extending an existing manifest.
- The tests-only commits failed for the intended three behaviors: 41612954045. The implementation and assertion correction are on branch head `839b59b08d5b`.
- Exact-head CI: [41613340163](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41613340163) SUCCESS — 149 Python tests; the full repository workflow also completed successfully.
- New invariant: a single manifest has one `(seed, version)` pair globally; existing manifests retain that identity when extended; explicit conflicting overrides fail closed. A new corpus split design requires a separate versioned manifest.
- This is an engineering reproducibility fix only. It creates no linguistic labels and does not change gold count (0) or accuracy (`null`).

- Follow-up strictness regression: explicit empty `--seed` and `--version` must fail instead of falling through to defaults. Tests-only CI failed on both behaviours (41615374874); the corrected conditional default resolution passed exact-head CI 41615556868.


## Separate-manifest creation acceptance — 2026-11-03

**Status: DONE_VERIFIED on the dedicated PR branch; merge to main remains pending.** Added an acceptance test proving a genuinely new seed/version can be used when the caller supplies a separate empty JSONL input via `--splits`, while the existing frozen manifest remains untouched. Corrected the operator instructions: changing only `--output` does not reset the input manifest; the new-manifest workflow must use a new empty `--splits` file and a distinct `--output` file.

- PR [#101](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/101), final documentation head `b008b824fb5c95861f4e3d8766c8307515df0c02`; code/test checkpoint `e8ab5545d554b09d3c3ba742d7b5aa58aafbdb44` (the three subsequent commits are docs-only).
- Exact-head CI [41638528514](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41638528514) SUCCESS — 152 unittest tests; exact-head workflow success.
- No linguistic gold rows were added; independent gold remains 0 and empirical accuracy remains `null`.


## Split-manifest integration checkpoint — 2026-11-03

**Lao PR #101: DONE_VERIFIED on main.** Merged as `ccb6ba44d9448858091306d606a7bba50f19a5de`. The global manifest identity invariant and separate-manifest creation acceptance are now in the default branch. Exact-main workflow [41643375975](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41643375975) succeeded. No gold rows were added; adjudicated gold remains 0 and empirical accuracy remains `null`.


## Source-citation reconciliation — 2026-11-03

**Status: PARTIAL pending exact-head verification.** MekongPhon is added to the Lao source registry and author–year citation. Its 367,000 Lao pairs and under-2% held-out CER are attributed to the paper; dialect/IPA compatibility and corpus redistribution rights are owner-confirmed as resolved.

- This clean port is based on the latest main after the split-manifest integration; superseded PR #102 is not used as a merge candidate.
- No pronunciation labels or corpus records imported; rights remain source-specific; independent gold remains 0 and accuracy remains `null`.


## LAO-UI-001 — built-site browser regression coverage — 2026-11-03

**Status: PARTIAL pending exact-head CI and manual QA.** Added Playwright tests for visible IPA/Ukrainian output, mixed-script fail-closed behavior, clear/reset and romanization/IPA-first separation; CI and Pages build workflows now run them against the built site.

- Browser test dependency is pinned to `@playwright/test 1.63.0`, but no lockfile is committed; transitive dependency reproducibility remains a follow-up improvement.
- Manual visual, keyboard, screen-reader and mobile QA remain TODO. Automated browser success cannot substitute for those checks.
- No linguistic rules or gold labels changed; adjudicated IPA gold remains 0 and accuracy remains `null`.


## Continuation status sync — 2026-11-03

- Current main: `ecd61a110a4ca8b25535570e0baab79c0e567436`; exact-main checks: verify 41647974181 SUCCESS; Pages 41647974321 SUCCESS.
- PR #100 is closed without merge; its browser/quality portions have been ported to main. No open PRs were returned by the current open-PR query.
- Engineering improvements on main are verified at the stated commit; this does not promote linguistic validation or manual accessibility tasks to DONE.
- IPA gold remains 0; empirical accuracy remains null. Annotation staffing, convention approval, rights clearance, blind intake and adjudication remain BLOCKED on external human/evidence dependencies.


## LAO-METHOD-REFRESH-001 — upstream methodology snapshots — 2026-11-03

**Status: DONE_VERIFIED (reference audit).** Superpowers v7.0.1 current main: `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`; mattpocock/skills v1.3.2 release: `d1478fcb140db0b93c0c8df17bcfd311844749d0`, current main snapshot: `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`; Ponytail v5.3.3 release: `7801d061243d7b753bad0e0b3c057cd250b11755`, current main: `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846` (README-only post-pin change).

- Release pins and current-main snapshots are distinguished. No third-party runtime or skill files imported.

## 2026-11-03 — held-out benchmark split enforcement

| Task | Status | Evidence / remaining acceptance |
|---|---|---|
| IPA-BENCH-SPLIT-001 | DONE_VERIFIED (engineering contract) | Export preserves the frozen group-safe split; scorer defaults to test and requires explicit selection for train/dev/all. Exact-head verify [41651864836](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41651864836) SUCCESS on `7d2c37f8ceb9dd77aea2d40a8340a919d66c5b33`. This fixes the evaluation boundary, not linguistic gold. |

Independent gold remains 0 and accuracy remains null. No data labels were fabricated. The split-aware benchmark documentation is in `docs/benchmarking-and-external-ipa.md`.

## Frozen split manifest provenance — 2026-11-03

The export and benchmark now preserve and validate the complete frozen split identity, not only the bucket name: `split`, `split_seed`, and `split_version`. Every adjudicated row must carry non-empty seed/version metadata, and the benchmark rejects a TSV that mixes manifest identities. The report exposes the manifest seed/version and selected scoring split. This makes the evaluated test partition traceable to one exact manifest; it does not create linguistic gold or change the current zero-row accuracy status.


## 2026-11-03 — empty benchmark prediction input

| Task | Status | Evidence / remaining acceptance |
|---|---|---|
| IPA-BENCH-EMPTY-PREDICTIONS-001 | DONE_VERIFIED (engineering guard) | Header-only prediction TSV previously exited 0 and produced an empty `engines` object. Test-first regression failed on all three language repositories; the scorer now rejects an empty prediction dataset after checking gold and frozen split provenance. Missing individual predictions within a named engine remain denominator-counted. RED: [41655160456](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41655160456). Final exact-head verify: [41655452782](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41655452782) SUCCESS. |


## 2026-11-03 — benchmark identifier validation

| Task | Status | Evidence / acceptance |
|---|---|---|
| IPA-BENCH-IDENTIFIERS-001 | DONE_VERIFIED (engineering guard) | Reject whitespace-only gold IDs, prediction IDs and engine names while preserving non-empty identifiers exactly. Test-first RED: gold-ID run 41660752360; prediction-ID/engine run 41662058993. Final exact-code-head CI: 41662219515 SUCCESS (159 Python tests and 4 built-site browser tests passed).  No linguistic labels or accuracy claims were added. |

## 2026-11-03 — Lao Python/browser segmentation contract review

| Task | Status | Evidence / acceptance |
|---|---|---|
| LAO-PY-BROWSER-SEGMENTATION-001 | PARTIAL / contract decision required | Python splits only at whitespace/U+200B; browser dynamically segments unspaced tokens. The Python API is documented as syllable-oriented, so this is a verified behavioral difference but not yet a confirmed defect. Tracked in [issue #116](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/issues/116). Acceptance: decide shared-vs-distinct API contract, add shared fixtures and cross-runtime tests, then implement parity or document the intentional boundary. No IPA/gold/accuracy claims. |


## 2026-11-03 — Lao Python/browser segmentation contract

| Task | Status | Evidence / acceptance |
|---|---|---|
| LAO-PY-BROWSER-SEGMENTATION-001 | DONE_VERIFIED (contract clarification) | Python API is intentionally syllable-oriented; browser adds conservative within-token syllable segmentation for phrase input. Documented the deliberate boundary and explicitly disclaimed lexical word segmentation and cross-runtime parity for unspaced multi-syllable input in [README](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/blob/main/README.md#runtime-segmentation-contract). Issue [#116](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/issues/116) closed; docs PR [#117](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/117) merged as `2750153bd49e11c3c74ac2cc515acc750f90fae0`. Exact PR-head CI [41716613666](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41716613666) SUCCESS, including Python, browser-engine, generated-data drift, Chromium UI and built-page/asset checks. No parser/phonology rules changed; unspaced phrase segmentation remains browser-only and lexical segmentation remains out of scope. |


## Research unblock checkpoint — 2026-11-03

- Prospective language-specific expert/researcher leads and additional candidate resources are recorded in docs/ipa-gold-collection-playbook.md with primary-source links and explicit limits.
- These are leads only: no one has been contacted or recruited; no IPA convention has been approved; no rights have been granted; no IPA labels were generated.
- The 30-item pilot remains BLOCKED until the acceptance conditions in the playbook are met. Candidate lexicon entries, phonetic respellings, model outputs, orthographic transcripts and source descriptions are not gold IPA.
- The next external action is to contact a qualified prospective reviewer and request nominations for two independent annotators plus a separate adjudicator; separately complete owner-confirmed rights disposition and blind-intake dry run.


## Lao external G2P reproducibility — 2026-11-03

| ID | Status | Evidence / remaining acceptance | Boundary |
|---|---|---|---|
| LAO-G2P-REPRO-001 | DONE_VERIFIED | PR #120 merged as `943eb3264448dd376f5a7c1670fa136fb0214f7a`; exact PR-head and post-merge `main` verification passed (41723349565, 41723526240). Pinned comparator run 41723525916 passed and uploaded JSON + SHA-256 sidecar. Harness records fixture/script SHA-256, Python runtime/platform, source revision and pinned lao2ipa version; reproduction command is documented. | Reproducibility hardening only. Does not adjudicate any mismatch, provide a source-attested independent test sample, or create IPA gold. |


## Post-merge verification — Lao G2P reproducibility — 2026-11-03

- PR #120 merged as `943eb3264448dd376f5a7c1670fa136fb0214f7a`.
- Exact PR-head verification [41723349565](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41723349565) SUCCESS.
- Exact post-merge `main` verification [41723526240](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41723526240) SUCCESS.
- Exact post-merge pinned `lao2ipa==1.0.0` diagnostic [41723525916](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41723525916) SUCCESS; JSON + SHA-256 sidecar artifact exists with expiry 2027-02-01.
- `LAO-G2P-REPRO-001` is **DONE_VERIFIED** for provenance, version pin enforcement, report checksum generation and hosted artifact publication.
- Parent issue #9 remains **PARTIAL**: the independent rights-cleared sample and qualified review of 31 tone, 2 offglide and 4 segmental/vowel-sequence disagreements remain outstanding. Independent IPA gold=0; accuracy=null.


## Common Voice 27.0 Lao rights/profile checkpoint — 2026-11-04

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| LAO-CV27-AUDIO-001 | PARTIAL (audio lead; target-profile fit unverified) | Provider record declares CC0-1.0 but prohibits speaker identification and re-hosting/re-sharing; 223 clips, 193 validated, 0.35h validated, 16 speakers, accent value absent/mostly unspecified. Source added as SRC-CV-LAO-27. | Use provider-hosted audio only; do not mirror. A Lao specialist must screen individual clips for target variety and citation-form suitability and assign exact clip/time locators before double IPA annotation. Not gold. |


## Post-merge checkpoint — Common Voice 27.0 Lao (2026-11-04)

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| LAO-CV27-AUDIO-001 | DONE_VERIFIED (source registration and rights boundary); pilot use remains PARTIAL/BLOCKED | PR #124 merged as `90ddc42537dad2292fc0a4b5614fc58f6a1ebba5`; PR-head verification [41800307823](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41800307823) SUCCESS; post-merge main verification [41800496434](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41800496434) SUCCESS. | CC0-1.0 but no speaker identification or re-hosting/re-sharing. 223 clips/0.40h, 193 validated/0.35h, 16 speakers; accent unreported. Specialist must approve target profile and exact clip/time spans. No gold labels. |


## Language-specific IPA test fixtures — 2026-11-04

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| LAO-IPA-GOLD-FIXTURE-001 | DONE_VERIFIED | PR [#126](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/126) merged as `3aee5de82cf7719a184d92a938e1ada3ffa73442`; exact-main Verify [41847832541](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41847832541) SUCCESS. | Test fixture now uses Lao script and neutral test profile; regression asserts Lao Unicode-block and matching profile metadata. This validates test-fixture integrity only, not phonological rules or IPA accuracy. Gold remains 0; accuracy null. |


## LDC Babel Lao source triage — 2026-11-04

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| LAO-LDC-BABEL-AUDIO-001 | DONE_VERIFIED (source identified and scoped; access blocked pending agreement) | LDC2017S08 catalog, DOI 10.35111/bq21-kf58; approximately 207h of Vientiane-region conversational and scripted telephone speech with transcripts; 8kHz A-law SPHERE and 48kHz/24-bit PCM WAV. Source registered as `SRC-LDC-BABEL-LAO-2017`. | Strong candidate for a Vientiane audio pilot, but not IPA gold. Obtain suitable LDC membership/non-member license and fee, inspect the package manifest, separate scripted vs conversational material, and complete blind double annotation/adjudication before any benchmark use. |


## IPA gold release-gate profile consistency — 2026-11-04

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| IPA-GOLD-RELEASE-PROFILE-001 | DONE_VERIFIED (engineering guard) | Shared `scripts/ipa_gold_corpus.py` now rejects adjudicated corpora that mix target-profile identity (`id`, `variety`, `region`, `register`) or IPA kinds. New regression tests cover both failures. PR #128 merged as `9f7a55ca41bd86e4c97dd25528224ac23ad425ec`; exact PR-head CI [41870105701](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41870105701) SUCCESS; post-merge CI [41870506853](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41870506853) SUCCESS. | Does not prove profile approval, annotator qualifications, blindness, linguistic contrast coverage, or IPA accuracy. A specialist-reviewed language-specific coverage report remains required before benchmark readiness. |


## Expert recruitment lead revalidation — 2026-11-04

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| LAO-IPA-GOLD-RECRUITMENT-LEADS-001 | PARTIAL | The current Thammasat profile verifies Varisa Osatananda's phonetics/sociophonetics/Lao tonal phonology expertise and Vientiane Lao dissertation; LDC LSP_203 confirms Vientiane vs Northern dialect pronunciation/tone differences. These strengthen reviewer shortlist/profile scope only; no contact, consent or recruitment. | No candidate has been contacted, consented, recruited or approved. Close only after two independent qualified target-variety annotators, separate adjudicator, non-annotating curator, conflict checks, secure blind intake and written role/terms confirmation are documented. |

## MekongPhon-informed deterministic Lao G2P improvement — 2026-11-07

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| LAO-G2P-THREE-ENGINE-001 | DONE_VERIFIED (comparative benchmark, schema 3.0) | Hosted benchmark [42309545197](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42309545197) SUCCESS; aggregate artifact [13547168327](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42309545197/artifacts/13547168327). Same 100-entry MekongPhon held-out seed lexicon; dataset revision and SHA-256 are recorded in the dated report. | Valid only for this 100-word lexical split, not the paper's 13,442-sentence evaluation and not independent project gold. Dataset rights remain unverified; no raw entries or predictions redistributed. |
| LAO-G2P-DETERMINISTIC-SEGMENTATION-001 | DONE_VERIFIED (engineering behavior) | Deterministic DP syllabification, syllable-local tone-mark validation and A2 coda checks are in `src/lao_ukrainian/parser.py`; Python/browser regression suites and exact PR-head Verify [42309845373](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42309845373) SUCCESS. | Does not establish universal lexical segmentation or independent phonological accuracy. Three held-out entries remain withheld; their exact tails are under aggregate diagnostic review. |
| LAO-G2P-TONE-CONTOUR-001 | DONE_VERIFIED (source-scoped conversion and comparison boundary) | Ueda numeric levels [24], [34], [33], [21], [52] convert to ˨˦, ˧˦, ˧, ˨˩, ˥˨ in the Vientiane profile. Tone-category scoring and benchmark-only Mekong contour rendering are separate from production tone metadata. | Ueda is a one-informant central-Vientiane description. The Mekong notation conversion is evaluation-only; it is not a production profile or universal Lao tone convention. |
| LAO-G2P-THREE-ENGINE-002 | PARTIAL (ClippyFirst close to but not yet ahead of Lao2IPA) | On identical 97 covered items: segmental CER 7.89% vs 7.72%; Mekong-convention tonal CER 10.67% vs 10.42%. ClippyFirst full-set coverage 97%; tone-category exact 83.33% vs Lao2IPA 87.50%. Detailed results in `docs/research/LAO-G2P-THREE-ENGINE-BENCHMARK-2026-11-07.md`. | To claim best deterministic performance, ClippyFirst must improve shared-subset segmental/tonal metrics and reach evidence-supported coverage; no metric should be optimized by relaxing fail-closed parsing. |
| LAO-G2P-PARSER-TAIL-001 | PARTIAL (diagnostic complete; linguistic rule not established) | Aggregate-only benchmark [42357836206](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42357836206) SUCCESS; artifact [13568064669](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42357836206/artifacts/13568064669). Two exact Unicode-name tail sequences and one single KHO SUNG tail are documented in the dated benchmark report; no raw words/predictions are exported. Exact-head Verify [42357841388](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42357841388) SUCCESS. | The two multigrapheme tails are not explained by current source-backed onset/vowel/coda rules; KHO SUNG is not a legal coda in the current inventory. Keep all affected outputs withheld. Add no rule without orthographic source or qualified reviewer evidence. |
| LAO-IPA-GOLD-001 | BLOCKED (independent linguistic acceptance) | Independent project Lao IPA gold remains 0. MekongPhon's 100-word reference set is not re-adjudicated by the project. | Requires rights-cleared Vientiane-profile source material, two independent qualified annotators, blind adjudication, and documented coverage before project accuracy claims. |

| LAO-G2P-TONE-CONTEXT-001 | DONE_VERIFIED (aggregate diagnostic only) | Tone-category confusion and rule-context report [42358185703](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42358185703) SUCCESS; artifact [13568751034](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42358185703/artifacts/13568751034). Five aligned ClippyFirst tone substitutions are mapped to source-backed selectors; eight word-level sequence-length mismatches and four alignment failures are separately counted. | Diagnostic is not a linguistic correction. Do not retune the Vientiane matrix from this held-out set. Require independent lexical evidence or expert adjudication and a separate development set before changing tone rules. |


## 2026-11-07 rule-engine error-analysis checkpoint

| Task ID | Status | Current evidence | Acceptance / remaining work |
|---|---|---|---|
| LAO-G2P-THREE-ENGINE-002 | PARTIAL (shared-subset deterministic parity improved) | Exact-head immutable inference + diagnostic benchmark [42374547901](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42374547901) SUCCESS; aggregate artifact [13575161811](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42374547901/artifacts/13575161811). On the same 97 covered segmental items: ClippyFirst CER 6.49%, 69/97 exact; Lao2IPA CER 7.72%, 68/97 exact; MekongPhon neural CER 5.79%, 81/97 exact. ClippyFirst full coverage remains 97%. | Continue with source-backed changes only. Neural model still leads; independent expert gold remains 0. Do not claim universal superiority from this 100-word dictionary split. |
| LAO-G2P-AFFRICATE-IPA-001 | DONE_VERIFIED | Canonical IPA for Lao ຈ changed from `tɕ` to `t͡ɕ` in Python and generated browser data; target mapping and legacy un-tied IPA alias retained. Raw segmental CER improved 12.79% → 11.46%; exact matches 64 → 69. Browser/Python fixture expectations updated. | Full Verify [42375716368](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42375716368) passed on `b325a5f91a3fdf063f231537d1550a140cb2eff8`, including Python, browser engine, generated-data reproducibility, and UI/build checks. |
| LAO-G2P-MINOR-SYLLABLE-001 | PARTIAL (candidate detection implemented; expert adjudication absent) | Initial unmarked short-open-/a/ before a major-weighted syllable is flagged as a potential minor syllable in both Python and browser engines. Segmental IPA and Ukrainian adaptation are retained; independent tone is withheld and status is analysis-dependent. The selector is in a separate special-tone registry, not the five-tone matrix. Six candidate contexts were observed in the 100-word aggregate diagnostic. Positive and negative selector cases pass in both runtimes. | A qualified Vientiane Lao reviewer must confirm the minor-syllable conditions and onset restrictions. Do not assign a neutral contour or widen the selector without that review. |
| LAO-G2P-ERROR-PROFILE-001 | DONE_VERIFIED (aggregate diagnostics) | Benchmark reports code-point substitutions/deletions/insertions, syllable position, tone-rule contexts, and unresolved-tone contexts without retaining words or per-item predictions. Repeated `w→ʋ` discrepancies occur in both ClippyFirst and Lao2IPA, suggesting a transcription convention issue; vowel/offglide pairs remain unadjudicated. | Keep the artifact aggregate-only. Resolve phonetic disagreements on a rights-cleared development set and with expert review. |
| LAO-G2P-PARSER-TAIL-001 | PARTIAL (fail-closed behavior preserved) | Two multigrapheme unconsumed tails, one standalone KHO SUNG tail, and one malformed tone-mark-order case remain withheld. | Require primary orthographic/phonotactic evidence or qualified reviewer analysis before adding a parser rule. |
| LAO-IPA-GOLD-001 | BLOCKED (independent linguistic acceptance) | Independent project Lao IPA gold remains 0. The 100-word MekongPhon dictionary split is not independently re-adjudicated. | Rights-cleared Vientiane-profile source material, two independent qualified annotators, blind adjudication, adjudicator resolution, and coverage report. |


## MekongPhon rights status correction — 2026-11-07

The repository owner confirms full MekongPhon rights for the authorized project use. Mark `LAO-MEKONGPHON-001` / `LIC-001` as `DONE_VERIFIED (owner-confirmed)` for rights; retain the source's `PARTIAL` status only for secondary-reference and dialect/convention limitations. This is not an independent legal opinion. Independent adjudicated project IPA gold remains 0.


## Grapheme preview fallback — 2026-11-07

| Task ID | Status | Evidence / acceptance |
|---|---|---|
| LAO-GRAPHEME-PREVIEW-001 | DONE_VERIFIED (typed provisional IPA → Ukrainian adapter fallback) | Registered positional IPA hints are wrapped in a typed PROVISIONAL result and passed through the same Ukrainian adapter; unresolved positions remain explicit. Python/browser tests and UI/CLI disclosure are verified by Verify #42796863636 and Pages run #42797184810. | The fallback does not infer tone or promote hints to accepted IPA. It guarantees visible rendering, not confirmed pronunciation. Unsupported Pali/Sanskrit/Khmu values remain unknown; independent adjudicated IPA gold remains 0. |


## Provisional grapheme rendering extension — 2026-11-08

| Work item | Status | Evidence / acceptance |
|---|---|---|
| Emit provisional IPA hints for unassigned modern-Lao consonants | PARTIAL | Python/browser implementations and regressions added; exact-head CI pending |
| Emit conservative vowel-grapheme hints when structure is unresolved | PARTIAL | Context-dependent warning retained; exact-head CI pending |
| Preserve unknown consonants and tone uncertainty | PARTIAL | Non-core consonant withholding and no-tone-inference tests added; exact-head CI pending |
| Linguistic accuracy of isolated grapheme hints in connected speech | BLOCKED / evidence-limited | Requires expert-adjudicated examples and contextual phonological evidence; no accuracy claim |

### Grapheme fallback verification update — 2026-11-08

| Work item | Status | Evidence / remaining acceptance |
|---|---|---|
| Python/browser provisional sound hints for unresolved modern-Lao consonants and selected vowels | DONE_VERIFIED (engineering) | Verify #42524982973: 289 Python, 143 Node, 19 Chromium; exact-head source/data/build/generated-artifact gates passed |
| Preserve uncertain consonant position and tone; do not guess non-core consonants or unsupported standalone offglides | DONE_VERIFIED (engineering contract) | Python/browser regression tests in Verify #42524982973 |
| Accuracy of grapheme-only hints in actual Lao words and connected speech | BLOCKED / evidence-limited | Requires independent expert-adjudicated contextual IPA records; project gold remains 0 |

## Written-evidence and lexical-hint continuation — 2026-11-09

**Integration checkpoint:** PR #157 was merged into `main` at `b5a3ea58481152196498d74eebee1c009f445046`. The final documentation/handoff checkpoint `290aca27cb62366d061664aca33a282fcba62dd2` passed exact-head Verify [#42586909319 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42586909319): 298 Python tests, 147 Node/browser-engine tests and 19 Chromium UI tests; IPA-gold schema, repository data/evidence audit, external-G2P harness, locked install, build, generated-data reproducibility/drift and built-page/relative-asset checks all passed.

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| LAO-WRITTEN-EVIDENCE-2026-11-09 | DONE_VERIFIED (source/claim registration) | PR #157 registers written phonology, dialect, syllabification, lexical-history, pronunciation-resource and benchmark-methodology sources/claims with explicit scope and provenance. | Registration makes evidence discoverable; it does not automatically validate a new runtime rule or make a secondary resource gold. |
| LAO-SYLLABIFICATION-EXAMPLE-2026-11-09 | DONE_VERIFIED (structural regression) | LaoNLP's published example `ພາສາລາວໃນປັດຈຸບັນ` is asserted in Python and browser suites; exact-main Verify #42586909319 passed. | Structural syllable segmentation/parity only; not lexical word segmentation or IPA gold. |
| LAO-LEXICAL-HINTS-001 | DONE_VERIFIED (diagnostic only) | Attributed 11,208-entry BSD-style LaoNLP `Lao-Dictionary.txt`; `src/lao_ukrainian/lexical_hints.py`; five focused tests. Exact-main Verify #42586909319 passed. | Returns every matching contiguous multi-syllable span, retains overlaps and labels them `SOFT_HINT_ONLY`. It does not select boundaries, change syllable parsing, feed IPA/G2P, alter Ukrainian output, or enter the browser bundle. |
| LAO-LEXICAL-SEGMENTATION-001 | PARTIAL | The list was created for word wrapping and its header says compounds were mostly reduced to parts. | A validated lexical word segmenter requires independently verified boundary data and context-sensitive evaluation; no automatic segmentation claim is permitted. |
| LAO-LAONLP-MIT-CSV-001 | DONE_VERIFIED (source inspection; raw CSV excluded) | Pinned upstream CSV and separate MIT notice inspected; 21 exact repeated headers, 3 malformed header-like rows, 3 ID-only rows; 35,078 distinct non-header forms. Offline audit utility verifies Git blob SHA-1. | `Pronunciation` is Latin romanization, not IPA. Raw CSV is not in runtime; filtered 34,937-entry derivative is optional SOFT_HINT_ONLY diagnostic data, not boundary gold. |
| LAO-KAIKKI-IPA-PROVENANCE-001 | PARTIAL | Deterministic 100-page manifest; exact raw MediaWiki revisions independently checked 100/100, and all 100 Lao sections directly invoke `{{lo-pron}}`. Generator Module:lo-pron oldid 88555975, wrapper oldid 79053402, docs oldid 76254409 pinned. | Sample generated provenance is DONE_VERIFIED; whole-corpus per-sound source attribution remains unresolved because Kaikki post-processing can merge sources and drops invocation metadata. Retain dialect variants; never treat the full extraction as independent gold. |
| LAO-IPA-GOLD-001 | BLOCKED | Independent expert-adjudicated project gold remains 0; `data/benchmark/gold.tsv` remains header-only. | Requires rights-cleared source material, qualified independent annotation, blind adjudication, dialect/profile and IPA conventions fixed, and a frozen held-out split. |

### Interpretation and scope

- The user cannot provide audio. Continue useful work from written primary/secondary sources, published examples, attributed orthographic resources and text-only tests; do not claim acoustic fidelity, prosodic naturalness or independent phonetic accuracy.
- Enfield's broad minor-syllable description remains distinct from the central Vientiane-specific Ueda profile. No broader /a i u/ rule was introduced.
- Osatananda's underlying lexical-tone analysis, Enfield's phonological feet, Davis's historical `ຣ`, Indic-loan orthography and Yanagimura's contextual tonal effects remain scoped research constraints, not silently converted into unsupported deterministic rules.
- The lexical-hint file is not a canonical phonological registry. `data/lao/*.csv` remains the authoritative phonological data; the word list is a separate, attributed orthographic research aid.
- No production phonology, IPA rule, target adapter, browser engine or generated browser data was changed by this continuation.


## Lao G2P benchmark confidence gate — 2026-11-09

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| LAO-BENCH-IPA-GATE-001 | DONE_VERIFIED | Typed gate integrated into all three benchmark scripts; 4 focused confidence tests plus full Verify #42592337943 (304 Python) | Regressions for SUPPORTED, UNCERTAIN, PROVISIONAL, unsupported and missing IPA pass; provisional hints excluded from IPA metrics |
| LAO-BENCH-EXT-ENGINES-001 | DONE_VERIFIED | External workflow #42592337944 and deterministic-profile #42591871633 succeeded on main; aggregate artifacts and source/model hashes recorded | Pinned Epitran, orthography2ipa, Transphone and Phonetisaurus comparators execute with zero runtime errors; Phonetisaurus weak concordance explicitly reported |
| LAO-BENCH-GOLD-001 | BLOCKED | Independent expert-adjudicated IPA gold remains 0 | Rights-cleared material plus qualified annotation/adjudication |


### Final mainline benchmark verification — 2026-11-09

| ID | Status | Evidence | Remaining acceptance |
|---|---|---|---|
| LAO-BENCH-IPA-GATE-001 | DONE_VERIFIED | Main Verify #42592337943: 304 Python, 147 Node/browser, 19 Chromium; typed confidence tests pass | None for software contract |
| LAO-BENCH-EXT-ENGINES-001 | DONE_VERIFIED | External G2P workflow #42592337944; deterministic profile #42591871633; aggregate artifacts include exact model/spec hashes | None for comparator reproducibility; all engines remain research-only |
| LAO-BENCH-HVULAO-001 | DONE_VERIFIED | HVULao run #42574809147 passed; script blob on main is byte-identical; artifact #13654703651 | The main-branch replay #42591871473 passed; aggregate artifact #13662725834 |
| LAO-BENCH-GOLD-001 | BLOCKED | Independent expert-adjudicated IPA gold remains 0; `data/benchmark/gold.tsv` is header-only | Rights-cleared source material plus qualified independent IPA annotation and adjudication |






### LaoNLP MIT dictionary follow-up — 2026-11-09

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| LAO-LAONLP-MIT-CSV-REPRO-001 | DONE_VERIFIED | `scripts/audit_laonlp_dictionary.py` and four subprocess regression tests; exact-head Verify #42597327636 passed (309 Python, 147 Node, 19 Chromium). | Script verifies the Git blob SHA-1 and audits CSV structure without importing the raw source data. |
| LAO-LEXICAL-HINTS-MIT-001 | DONE_VERIFIED (diagnostic only) | Derived 34,937-entry LaoNLP MIT LaoWord list with full notice; exact-head Verify #42597327636 passed (309 Python, 147 Node, 19 Chromium). | Matches remain SOFT_HINT_ONLY, are not auto-loaded, and do not establish contextual lexical boundaries. |


| LAO-LAONLP-MIT-CSV-REPRO-001 | DONE_VERIFIED | `scripts/audit_laonlp_dictionary.py`; malformed-width rows are excluded from usable-record counts and covered by a regression test; exact-head Verify #42635842846 passed 319 Python, 147 Node, 19 Chromium. | Utility verifies the pinned Git blob SHA-1 and separately counts exact repeated headers, malformed header-like rows, ID-only placeholders and malformed-width rows. Raw CSV is not bundled; no IPA or segmentation gold claim. |
| LAO-LEXICAL-HINTS-MIT-001 | DONE_VERIFIED (diagnostic only) | Filtered 34,937-entry LaoNLP MIT LaoWord derivative with full MIT notice; tests in test_lexical_boundary_hints.py; exact-head Verify #42611861847. | Optional explicit input to the diagnostic matcher; every result remains SOFT_HINT_ONLY. No automatic boundaries, production G2P or target output changes. |

| LAO-KAIKKI-IPA-PROVENANCE-SAMPLE-100 | DONE_VERIFIED (deterministic sample) | 100 unique IPA-bearing forms selected by FNV-1a codepoint ordering; exact MediaWiki revisions, titles, page IDs, timestamps and source-text lengths match 100/100; all 100 Lao sections directly invoke `{{lo-pron}}`; manifest integrity test recomputes hashes; exact-head Verify #42614988384. | Sample-level source provenance only; not a census, not independent IPA gold, and not proof of exclusive sound-value provenance in the postprocessed Kaikki JSONL. |


## Grapheme fallback Ukrainian rendering — 2026-11-10

| Work item | Status | Evidence / acceptance boundary |
|---|---|---|
| Emit a Ukrainian-side result when full structural/phonological parsing is unresolved | DONE_VERIFIED (engineering contract on starting main) | Typed provisional IPA runs pass through the ordinary Ukrainian adapter; unresolved units become explicit `?` markers. Python/browser implementations and regression tests are present; starting-main Verify #42776630426 passed. |
| Preserve low confidence, provenance and tone uncertainty | DONE_VERIFIED (engineering contract on starting main) | Result and segments remain `PROVISIONAL`; fallback does not infer tone or promote hints to accepted IPA. |
| Show an explicit low-confidence note in browser details and text CLI; render the transformed provisional output in the browser aggregate | DONE_VERIFIED | Exact branch-head Verify [#42796566811](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42796566811) passed on `8c7fffe99746e21769ee40e92818f5e10fa5081c`; browser and CLI regressions assert the user-visible output and confidence note. UI/CLI changes and regression assertions are in `fix/provisional-grapheme-output-docs-20261110`. |
| Empirical accuracy of grapheme-only hints in context | BLOCKED / evidence-limited | Independent expert-adjudicated IPA gold remains 0; requires source-located contextual annotation and adjudication. |

**Interpretation:** 100% visible rendering is a product-output requirement, not 100% supported IPA or phonetic accuracy. Out-of-scope Pali/Sanskrit and Khmu forms remain explicitly unknown unless separately scoped and evidenced.


## Current status reconciliation — 2026-11-15 (post PR #218 and Pages run #101)

This section supersedes the older romanization/deployment status snapshots above where they conflict; historical evidence remains preserved.

| ID | Current status | Current evidence | Remaining acceptance / blocker |
|---|---|---|---|
| LAO-ROM-STD-001 | DONE_VERIFIED (documented selection) | BGN/PCGN 1966 as represented by CLDR Lao-Latin remains explicitly provisional; 2025 UNGEGN WGRS evidence documents a Lao government draft process but not adoption. | Recheck for an authoritative final Lao table or national adoption; do not infer it from draft status. |
| LAO-ROM-MATRIX-001 | PARTIAL | Source-aware Lao → CLDR → Ukrainian path is covered by a full official-motto fixture. PR #214 fixed internal hyphen/source-group alignment; PR #218 adds source-backed AWW_MEDIAL recovery for the CLDR-elided vowel in v-n. Exact-head Verify #4265 passed 350 Python, 191 Node and 28 Chromium tests. | Full supported orthographic inventory, contextual variants and independent Lao specialist review are not complete. Acceptance: every promoted source unit has a source locator, CLDR form, Ukrainian target decision, positive/negative fixtures and review status. |
| LAO-ROM-DIRECT-001 | PARTIAL | Direct BGN/PCGN and bounded ALA-LC 2012 input paths remain separate and fail closed for ambiguous/unsupported forms. The source-aware full-motto regression proves the Lao-source path only; direct Latin-only vadthanathav-n remains PARTIAL because the missing vowel is not recoverable from the string. | Full contextual ALA-LC Notes 1–10, medial-w clusters, unsupported LOC vowel sequences and broader source-located corpus coverage remain incomplete. Do not infer missing tone/length or CLDR-elided vowels. |
| LAO-ROM-RTGS-001 | BLOCKED / evidence updated | No authoritative complete Lao-specific RTGS adaptation table has been established. The current UNGEGN index places Lao v4.0 (2013) under other languages/scripts, not among UN-recommended systems. The 2025 WGRS report says that as of July 2024 Lao PDR was finalizing draft toponymy guidelines, with possible consideration at the 2027 UNGEGN Session; the 2025 UN country-name record still uses BGN/PCGN 1966 for the country's formal name. This does not establish a finalized universal Lao transcription standard or Ukrainian adaptation. See `SRC-UNGEGN-APPROVAL-PROCESS-2026`, `SRC-UNGEGN-ROMANIZATION-STATUS`, `SRC-UNGEGN-LAO-DRAFT-2023`, `SRC-UNGEGN-LAO-STATUS-2025`, `SRC-UNGEGN-LAO-NAME-2025`, `SRC-PCGN-LAO-FACTFILE-2023`, `CLM-LAO-ROMANIZATION-STATUS-2025`. | Requires an authoritative complete Lao adaptation table, reuse-rights determination, Ukrainian target decisions and reviewed fixtures. |
| LAO-ROM-COVERAGE-001 | PARTIAL | Current parser has explicit source-aware crosswalks, unsupported-form guards and full-motto regression; automated repository audit passes. | Inventory audit must demonstrate no supported source grapheme/structure class is silently dropped; every added mapping needs evidence and tests. |
| LAO-ROM-REVIEW-001 | BLOCKED | No independent Lao specialist sign-off on ambiguous nuclei, conventional names, loanword namespaces or the new source-restored AWW_MEDIAL case. | Qualified Lao reviewer must adjudicate scoped rule tables and fixtures; automated CI cannot satisfy this. |
| LAO-GOLD-001 | BLOCKED | Independent expert-adjudicated IPA gold remains 0; gold.tsv remains header-only. | Rights-cleared, dialect/profile-scoped examples; two independent qualified annotators; blind adjudication; adjudicator resolution; frozen held-out split. |
| LAO-PHON-001 | PARTIAL | Deterministic IPA-first pipeline and research matrices are implemented; no new phonetic rule was inferred from the romanization fix. | Complete source-backed tone/rhyme/segmentation contexts and independent expert review. |
| LAO-UI-001 | PARTIAL | GitHub Pages run [#101](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43753235467) deployed runtime SHA fe435317dcb69cd43f0409ca85e9b617b334a584; build/Chromium and deployed-service smoke-test jobs passed. Latest main Verify [#4270](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43753297233) passed. | Human keyboard-only, screen-reader, mobile-device and visual QA remains outstanding. |
| LAO-REL-001 | PARTIAL / not release-ready | Engineering CI and GitHub Pages deployment are verified; current main is documentation-only ahead of deployed runtime SHA. | Release remains blocked by independent IPA gold, specialist review and manual accessibility/device QA; do not describe as universal or phonetic-accuracy validated. |
| PR-145-ARCH-001 | BLOCKED / owner decision | PR #145 remains the only open PR and proposes a neural-first CLI/Python default that conflicts with the adopted deterministic-default contract. | Requires explicit architecture/specification decision and full CLI/Python/docs/test reconciliation; leave unmerged until then. |

**Current main at reconciliation:** 827ee0f3f3a81ead1753f901f2b36025998bdc18 before this documentation-only checkpoint. **Runtime deployed to Pages:** fe435317dcb69cd43f0409ca85e9b617b334a584. Compare confirms only README, this register, romanization matrix and handoff documentation are changed after the deployed runtime commit. **Project readiness:** engineering-verified partial research prototype, not release-ready as a linguistically validated universal converter.


## Follow-up reconciliation — PR #220 and Pages run #102 — 2026-11-15

| ID | Current status | Evidence / remaining acceptance |
|---|---|---|
| LAO-ROM-MATRIX-001 | PARTIAL | Official Lao motto fixture verifies source-aware internal hyphens and AWW_MEDIAL recovery. Seven additional core vowel IDs without confirmed CLDR mappings now produce explicit PARTIAL diagnostics. Each future mapping still needs source-attested CLDR output, Ukrainian target decision and Lao-specialist review. |
| LAO-ROM-COVERAGE-001 | PARTIAL | Fail-closed coverage now explicitly tests UO_LONG_ALT, UO_LONG_OPEN, OEY, OOY, AEW, AOY and AAJ; full contextual orthographic inventory remains incomplete. |
| LAO-ROM-DIRECT-001 | PARTIAL | Direct Latin-only behavior remains unchanged; it cannot restore missing CLDR vowel information without Lao source structure. Full ALA-LC context remains incomplete. |
| LAO-UI-001 | PARTIAL / deployed | Pages run #102 / [43755557855](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43755557855) deployed runtime SHA fe1c4a0b8966155b5f22e6cc58ebcb3a33d5bbf9; build and deployed static-service smoke-test passed. Manual keyboard/screen-reader/mobile QA remains outstanding. |
| HYBRID-V2-BROWSER-001 | DEFERRED by owner decision | PR #158 temporarily deployed the browser neural lane; it was explicitly retired on 2026-11-10 by commits 0846e377 and afa035d. Current Pages intentionally excludes ONNX/WASM/model assets. Do not restore without a new owner decision. |
| LAO-GOLD-001 | BLOCKED | Independent expert-adjudicated IPA gold remains 0. |
| LAO-ROM-REVIEW-001 | BLOCKED | No independent Lao specialist sign-off. |
| LAO-REL-001 | PARTIAL / not release-ready | Engineering checks and Pages deployment pass; linguistic gold, specialist review and manual accessibility QA remain blockers. |

Exact-head PR #220 Verify #4280 / run 43755451075 passed 350 Python, 192 Node and 28 Chromium tests plus data/evidence audit, build and generated-data reproducibility. Main Verify #4281 / run 43755557872 and Pages deployment #102 / run 43755557855 passed on the merged SHA. Project remains an engineering-verified partial research prototype.


## Post-PR #221 mainline reconciliation — 2026-11-15

| ID | Current status | Evidence / remaining acceptance |
|---|---|---|
| MAINLINE-221 | DONE_VERIFIED (documentation checkpoint) | PR #221 merged; current `main` is `99d9fd3b5aa443c1a34af9ab9b30a3e51add39a7`. Exact-head Verify #4284 and post-merge Verify #4285 passed. No runtime files changed. |
| LAO-ROM-MATRIX-001 | PARTIAL | Seven source IDs still lack an explicit, source-attested CLDR compound-vowel crosswalk. Current upstream CLDR XML has active single-character/context rules but no explicit validated compound rules for these IDs; fail-closed diagnostics remain correct. |
| LAO-ROM-DIRECT-001 | PARTIAL | BGN/PCGN-derived CLDR and bounded ALA-LC routes remain separate. Full ALA-LC contextual Notes 1–10, medial-w clusters, contextual vowel alternations and broader source-located corpus coverage remain incomplete. |
| LAO-ROM-RTGS-001 | BLOCKED / evidence updated | No authoritative complete Lao-specific RTGS adaptation table has been established. The current UNGEGN index places Lao v4.0 (2013) under other languages/scripts, not among UN-recommended systems. The 2025 WGRS report says that as of July 2024 Lao PDR was finalizing draft toponymy guidelines, with possible consideration at the 2027 UNGEGN Session; the 2025 UN country-name record still uses BGN/PCGN 1966 for the country's formal name. This does not establish a finalized universal Lao transcription standard or Ukrainian adaptation. See `SRC-UNGEGN-APPROVAL-PROCESS-2026`, `SRC-UNGEGN-ROMANIZATION-STATUS`, `SRC-UNGEGN-LAO-DRAFT-2023`, `SRC-UNGEGN-LAO-STATUS-2025`, `SRC-UNGEGN-LAO-NAME-2025`, `SRC-PCGN-LAO-FACTFILE-2023`, `CLM-LAO-ROMANIZATION-STATUS-2025`. |
| LAO-GOLD-001 | BLOCKED | Independent expert-adjudicated IPA gold remains 0; no accuracy claim can be made from dictionary-seeded benchmarks or stress coverage. |
| LAO-ROM-REVIEW-001 | BLOCKED | Qualified Lao-specialist review remains outstanding. |
| LAO-UI-001 | PARTIAL / deployed | Pages #102 successfully deployed runtime SHA `fe1c4a0`; PR #221 changed documentation only. Manual physical-device, keyboard-only and assistive-technology QA remains outstanding. |
| PR-145-ARCH-001 | BLOCKED / owner decision | Current compare is 24 ahead / 349 behind / 13 files; merge base `c0d7218`; non-mergeable. Requires explicit architecture decision and fresh reconciliation, not blind merge. |
| HYBRID-V2-BROWSER-001 | DEFERRED by owner decision | Browser neural panel and model packaging were explicitly retired on 2026-11-10. Deterministic hybrid shell remains deployed; do not restore neural browser inference without a new owner decision. |

The upstream CLDR evidence and branch review are recorded in the canonical handoff and the direct-input audit. Project readiness remains an engineering-verified partial research prototype, not a linguistically validated universal converter.


## PR #222 verification — DONE_VERIFIED (engineering only)

Exact-head Verify [#4286 / run 43760081269](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43760081269) passed on branch `docs/post-pr221-checkpoint-and-cldr-evidence-20261115`: IPA-gold schema and repository data/evidence audits; 350 Python tests; external-G2P syntax/CLI; 192 Node tests; build/generated-data reproducibility; 28 Chromium tests; built-page/relative-asset and deterministic-only artifact assertions. Documentation-only; no Pages deployment required. Linguistic acceptance remains partial/blocked as in the table above.

## LOC table version authority — 2026-11-16

The current LOC index lists Lao (2012) as the current table and 1997 only as an earlier reference version; LOC says earlier versions are for reference only and not for current cataloging. This confirms 2012 as the primary standard. Note 9 is a three-branch boundary policy (ordinary Lao shortest standalone form; Pali/Sanskrit same rule; other loans divided according to the original language), not a generic Lao tokenization task. See the direct-input audit and source/claim registry entries `SRC-ALA-LC-ROMANIZATION-INDEX` and `CLM-ALA-LC-LAO-2012-CURRENT-VERSION`.


## Vientiane Lao phonological parsing boundary — Ueda (1994) full-text review (2026-11-16)

| ID | Status | Evidence / acceptance |
|---|---|---|
| VIENTIANE-WRITTEN-SEQUENCES-VS-SPOKEN-CLUSTERS | DONE_VERIFIED (evidence claim only) | Ueda §2.3 (printed pp. 100–101) reports no phonological consonant clusters in the described Vientiane spoken dialect despite written consonant-letter sequences; written `w` can correspond to /ua/ or no independent spoken segment. Source/claim registry now records this as `SRC-UEDA` / `CLM-LAO-ORTHOGRAPHIC-SEQUENCES-NOT-PHONOLOGICAL-CLUSTERS`. This verifies the cited descriptive claim, not an implementation or complete parser. |
| ORTHOGRAPHIC-SYLLABLE-SEGMENTATION | PARTIAL / TODO | Ueda supplies spoken syllable templates, rhyme constraints, positional onset/coda inventories and exceptional light-syllable discussion, but no general deterministic orthographic boundary algorithm. Acceptance requires an authoritative orthographic grammar/rule environment, explicit treatment of grapheme clusters and vowel-sign attachment, adversarial source examples, and independent Lao-specialist adjudication. |
| ALA-LC Note 10 automatic source-role derivation | PARTIAL / BLOCKED | LOC's romanized `khitsatān` example and repeated-consonant rule are known; exact Lao glyphs remain unresolved pending preferred Word source or specialist reading. Existing fixtures manually inject roles and are not evidence of automatic parsing. Ueda's paper does not close this gap. |


## PR #247 — Ueda evidence checkpoint and verification caveat (2026-11-16)

| Workstream | Status | Current evidence / acceptance |
|---|---|---|
| Vientiane written-sequence vs spoken-cluster distinction | DONE_VERIFIED (evidence claim only) | Full text of Ueda (1994), §2.3, reports no phonological consonant clusters in the described Vientiane dialect despite written consonant sequences; written `w` can correspond to /ua/ or no independent segment. Registry: `SRC-UEDA` and `CLM-LAO-ORTHOGRAPHIC-SEQUENCES-NOT-PHONOLOGICAL-CLUSTERS`. This does not implement a parser. |
| Orthographic syllable segmentation | PARTIAL / TODO | Ueda provides spoken syllable/rhyme structure and positional onset/coda constraints but no general deterministic orthographic segmentation algorithm. Need explicit grapheme attachment/boundary grammar, adversarial written examples and Lao-specialist adjudication. |
| Note 10 automatic source-role derivation | PARTIAL / BLOCKED | LOC romanized example `khitsatān` and repeated-consonant rule remain known; exact Lao glyph sequence is unresolved pending preferred LOC Word source or specialist verification. Existing fixtures inject roles manually. Ueda does not solve the orthographic parser. |
| PR #247 latest branch HEAD | PARTIAL (verification pending) | The Ueda evidence content checkpoint `71c9604040a2187910a6f0ed81c1c17286deb7bd` passed Verify #4499 / run 43966184173 — SUCCESS. The subsequent handoff synchronization HEAD `3a257848ddecb6d45968eae7cbdc1d2b1fd32dd4` passed Verify #4500 / run 43966297408 — SUCCESS, including every configured step through Chromium UI and built-page/asset checks. No local tests were run. |



## Historical Lao orthographic grammar and ambiguity evidence — 2026-11-17

| Workstream | Status | Evidence / acceptance |
|---|---|---|
| Historical explicit Lao orthographic syllable grammar located | DONE_VERIFIED (source evidence only) | Berment (2004), Part III §§III.2.3–III.2.6 and Annexes A.11/A.14, documents a non-recursive grammar, positional vowel patterns, restricted codas and Sylla/FSA tooling. Source/claim registry IDs `SRC-BERMENT-THESIS-2004` and `CLM-LAO-HISTORICAL-ORTHOGRAPHIC-SYLLABLE-GRAMMAR`. This does not validate a modern parser. |
| Current Lao orthographic grammar implementation | PARTIAL / TODO | Historical grammar has 56,670 generated strings but admits theoretical unattested forms (e.g. `ມວອ`), simplifies accent placement and OCR loses some terminals. Need exact transcription from images/Prolog appendix, Unicode/dialect reconciliation, test corpus and specialist adjudication. |
| Ambiguity lattice and dead-branch pruning | PARTIAL / TODO | Berment describes candidate-edge graph, complete paths, dead-branch pruning and ambiguous regions. No equivalent implementation/test exists in this repository. Longest candidate was a local UI heuristic, not an accepted global resolver. |
| Global ambiguity resolution | BLOCKED / evidence-limited | Lexical/semantic resolution is not established by the historical grammar. Preserve alternatives or explicit unresolved state; do not use longest-match as a deterministic transcription decision. |
| LOC Note 10 automatic source-role derivation | PARTIAL / BLOCKED | Historical grammar may help generate candidate orthographic boundaries after validation, but does not verify exact LOC glyphs or automatic coda/onset double-role assignment. |

The separate Del Vigna & Berment (2003) formal-language analysis describes irreducible ambiguous strings for a historical Lao dictionary. Its 11,172 / 3,060 dictionary figures and automaton counts must not be conflated with Berment's 56,670 grammar-generated strings. No historical code was copied; no license is inferred. Full notes: [Undermind](https://app.undermind.ai/projects/5603c8d1-3260-4f39-b0d5-8fd6ffa3a081?path=/research/orthographic-parsing-boundaries-2026-11-16.md).


## Modern Lao grapheme structure — evidence checkpoint 2026-11-17

| Workstream | Status | Evidence / acceptance |
|---|---|---|
| Modern grapheme-placement evidence | DONE_VERIFIED (scoped source review) | Lao Script Generation Panel 2017 proposal v3.1 and ICANN RZ-LGR-6 Lao (2025) specify positional vowel classes, mark ordering, U+0EBC placement, tone/sign contexts and a scoped coda model. W3C Lao Layout Requirements (2026-03-20) adds current encoding/layout distinctions but is an unendorsed Group Note Draft. |
| ICANN LGR as general Lao spell-checker | DEFERRED / not applicable | The ruleset is DNS root-zone/Unicode 16.0 scoped and deliberately omits many language spelling constraints; arbitrary consonant strings for acronyms and over-produced diphthongs are explicitly acknowledged. |
| Low-level grapheme-structure analyzer | TODO | Implement code-point classes and context order for pre-base, above/below/after vowel components, tone marks, U+0EBC, U+0ECC and U+0EC6. Add positive/negative ordering fixtures and Unicode 16/18 reconciliation. |
| Current general Lao syllable grammar | PARTIAL / TODO | Berment's historical grammar + current grapheme evidence are complementary but incomplete. Need reviewed spelling constraints, separate acronym/loan/Indic profiles, candidate lattice, ambiguity preservation and Lao-specialist adjudication. |

New registry entries: 81 unique source IDs / 99 unique claim IDs after this checkpoint; no duplicate IDs or missing claim-to-source references. See direct-input audit and romanization matrix for scoped source links and rule details.


## Ishida 2026: syllable/word boundary evidence — 2026-11-17

| Workstream | Status | Evidence / acceptance |
|---|---|---|
| Modern Lao syllable boundary evidence | DONE_VERIFIED (source review) | Ishida (2026-04-28) says explicit vowels and restricted codas make individual syllable segmentation comparatively straightforward; identifies onset families and pre-base vowel anchoring. |
| Ishida orthographic regression cases | PARTIAL | Added `ໃຫຍ່`, `ເຫຼືອງ`, `ປະເທດ` controls to multisyllable tests. Python step passed on test commit in Verify #4517; full workflow still pending at last poll. These are not IPA gold. |
| Lexical word segmentation | PARTIAL / TODO | Word boundaries are not marked by spaces; multi-syllabic words may require a language-specific dictionary or explicit ZWSP. Do not equate syllable segmentation with word segmentation. |
| Modern coda inventory reconciliation | TODO | Ishida's nine phonological coda letters differ from ICANN's broader DNS root-zone repertoire and historical loan/Indic spellings. Define separate profiles before changing parser inventories. |
| Ambiguity lattice | TODO (fallback) | Retain candidate alternatives for genuine residual ambiguity; do not assume ordinary Lao syllable segmentation is generally irreducible. |

Registry totals: 81 unique sources / 104 unique claims; no duplicate IDs or missing claim-to-source references.

## Lao short-vowel glottal realization — 2026-11-17

| Workstream | Status | Evidence / acceptance |
|---|---|---|
| Written coda grapheme inventory | DONE_VERIFIED (orthographic level only) | Nine explicit modern coda spellings remain mapped in `consonants.csv`; /ʔ/ is not a tenth written coda grapheme. |
| Phonological /ʔ/ category | DONE_VERIFIED (scoped category only) | Ueda (1994) includes /ʔ/ among central-Vientiane phonological codas; retain it in `codas.csv` without conflating it with the grapheme lookup. |
| Short-vowel glottal realization | PARTIAL / ANALYSIS_DEPENDENT | Ueda (1994) distinguishes exceptional non-final light CV syllables and spelling-based CVʔ readings; Lew (2014) treats slow/clear final closure after short vowels as redundant suprasegmental marking; Cole (2016) working paper proposes word-final epenthesis and reports no word-internal epenthesis in one context. No unconditional insertion rule is supported. |
| Runtime /ʔ/ insertion | BLOCKED pending context evidence | Requires a declared speech/reading profile, validated prosodic-word boundaries, independent Lao-specialist review, and positive/negative source-located examples before code or Ukrainian output changes. |

No IPA-gold examples, runtime rules, target correspondences or generated artifacts were added. The exact evidence scope and source disagreement are recorded in `PHONOLOGY-RESEARCH-WORKPACK-2026-11-01.md`.

### Exact-head engineering verification — initial research/test batch

Verify #4537 / [run 44079440345 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/44079440345) passed on the initial research/test head `1f59909d7af03d8f4fb0c7c3a2e6ae35f8b842b1`: IPA-gold schema; repository/data/evidence audit; 357 Python tests; external-G2P syntax/CLI; 204 browser-engine tests; build/canonical data generation; generated-data reproducibility; 30 Chromium UI tests; and built-page/relative-asset checks. This confirms engineering consistency of the evidence update and regression test only; it does not resolve the linguistic analysis. Final pre-metadata-sync Verify #4546 / [run 44079888990 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/44079888990) passed on `f088fab50ffa4675419b9994d6d76adf79d717de`: 357 Python, 204 browser-engine and 30 Chromium tests plus all configured schema, evidence, external-G2P, build, reproducibility and built-page checks. A final exact-head run validates the ensuing verification-report-only update.

## Controlled PR #247/#248 integration — 2026-11-17

| Workstream | Status | Evidence / acceptance |
|---|---|---|
| LOC Note 10 source attribution and double-role evidence boundary | PARTIAL / source conflict recorded | Preferred official Word source confirms ຄຼິສຕຽນ (khitsatīan); published 2012 PDF differs with ຫຼັກສາດ (khitsatān). LOC says to copy from Word. Crosswalk tests use the Word romanization but inject roles manually; exact Lao input is now regression-tested as unresolved. Automatic source-role derivation remains blocked. |
| Modern Lao coda grapheme inventory | DONE_VERIFIED (orthographic profile only) | Nine explicit mappings are asserted by scripts/audit.py and regression tests; ຢ remains fail-closed because Ishida's source is internally inconsistent. |
| Short-vowel glottal realization | PARTIAL / ANALYSIS_DEPENDENT | Ueda, Lew and Cole are registered with scope distinctions; no unconditional /ʔ/ insertion is justified. |
| Evidence registry integrity | DONE_VERIFIED (static reconciliation) | 82 unique sources / 107 unique claims; no duplicate IDs or missing claim-source references. |
| Combined engineering verification | DONE_VERIFIED (engineering only) | Verify #4551 / run 44081456903 passed on integrated code/test head 0f92c143adf896d0e4bc603e9296f20b6a3272f7: 359 Python, 204 browser-engine and 30 Chromium UI tests; schema/evidence, external-G2P, build, reproducibility and built-page checks passed. This does not establish linguistic accuracy. |

The integration branch retains PR #247's reviewed head as an ancestor and applies PR #248's delta through file-level reconciliation; both original PRs remain open and untouched. No runtime or generated artifact changes are included.


## PR #249 integration and post-merge verification — 2026-11-17

| Workstream | Status | Evidence / acceptance |
|---|---|---|
| PR #247/#248 evidence and regression integration | DONE_VERIFIED (integration/engineering only) | PR #249 merged as `825d7bf91d756c7abda884e2348a8fdfd82ec31f`; integrated exact-head Verify #4557 / run 44082038728 SUCCESS (359 Python, 204 browser-engine, 30 Chromium UI; schema/evidence, external-G2P, build, reproducibility and built-page checks). Exact-main Verify run 44083165575 SUCCESS on the merged SHA. |
| LOC Note 10 attribution | PARTIAL | The romanized example is attributed to LOC 2012; exact Lao glyph sequence remains unresolved pending preferred Word source or Lao-specialist confirmation. Current crosswalk fixtures inject source roles manually; automatic double-role derivation is not established. |
| Modern nine-coda orthographic profile | DONE_VERIFIED (scoped source/registry consistency) | Nine mappings are asserted by audit/tests; `ຢ` remains fail-closed due Ishida's internal chart/list discrepancy. This is not independent IPA gold. |
| Short-vowel glottal realization | PARTIAL / ANALYSIS_DEPENDENT | Ueda (1994), Lew (2014) and Cole (2016 working paper) support distinct scoped/competing analyses; no unconditional /ʔ/ insertion is justified. |
| Runtime /ʔ/ insertion | BLOCKED | Requires explicit dialect + speaking/reading profile, validated prosodic-word boundaries, independent Lao-specialist adjudication and source-located positive/negative examples. No runtime change made. |
| Independent IPA gold / accuracy | BLOCKED / NOT AVAILABLE | Gold records = 0; empirical accuracy = null. |

PR #247 and #248 are closed as superseded by merged PR #249; original branches are preserved. PR #145 remains open and untouched (24 ahead / 375 behind main); it requires a separate architecture decision. The merged batch changed evidence/docs/audit/tests only; no runtime, corpus, model, dictionary, generated artifact or deployment changed. Readiness: engineering-verified partial research prototype, not linguistically release-ready.

## LOC Note 10 Word-source correction — 2026-11-17

| Work item | Status | Evidence / remaining acceptance |
|---|---|---|
| Exact LOC Note 3/10 Word-source example | DONE_VERIFIED | Preferred official Word source: ຄຼິສຕຽນ (khitsatīan); Note 1 values explain ສ as final (t) and initial s. Published PDF disagreement is separately registered. |
| Historical LOC 1997 Note 3/10 romanized example | PARTIAL / glyph evidence limited | The 1997 PDF text extraction exposes `khitsatian`, but the Lao-script glyphs are corrupted in extraction; no exact historical Lao spelling is asserted. |
| Source-aware romanization crosswalk | DONE_VERIFIED (manual roles only) | Fixture corrected to khitsatīan and IA_LONG; roles remain explicitly supplied. Verify #4584 / run 44084533002 passed on exact head 536a3c69de6b2455c172c70daa6b427b9790c4da (359 Python, 204 browser-engine, 30 Chromium UI; all configured gates passed). |
| Automatic Lao source-role derivation | PARTIAL / BLOCKED | Needs validated orthographic syllabifier, exact source-role derivation and independent Lao-specialist review. |
| Full Note 10 conformance | PARTIAL | Exact source example is resolved; automatic segmentation and generalization beyond the example are not. |

## PR #251 — official LOC Word-source verification — 2026-11-17

| Work item | Status | Evidence / remaining acceptance |
|---|---|---|
| Exact current LOC 2012 Note 3/10 example | DONE_VERIFIED (source evidence) | Official Word source gives `ຄຼິສຕຽນ (khitsatīan)`; Notes 1, 3 and 10 jointly explain the combining mark and double-function `ສ` as final (t) + initial s. |
| Historical LOC 1997 Note 3/10 example | DONE_VERIFIED (historical edition only) | Official 1997 PDF pp. 117–118 gives `ກິດສະຕຽນ (khitsatian)`, distinct from the current 2012 form. |
| Source-aware romanization crosswalk | DONE_VERIFIED (manual roles only) | Fixture uses `khitsatīan` and `IA_LONG`, expected output `к'ітсатіан`; source roles remain manually supplied. Exact-head Verify #4611 / run 44085447163 SUCCESS; exact-main Verify run 44086036717 SUCCESS on `8945c94f3a0a6f44f6bdfb6cbad7bdcf99c9402d`. |
| Automatic Lao source-role derivation | PARTIAL / BLOCKED | Requires a validated orthographic syllabifier and source-derived coda/onset roles; current fixture is not automatic parsing. |
| Full Note 10 conformance | PARTIAL | Exact edition-specific examples are now verified; general source-role derivation and broader lexical boundary behavior remain unimplemented/unverified. |

PR #251 merged as `8945c94f3a0a6f44f6bdfb6cbad7bdcf99c9402d`. Registry: 83 unique sources / 108 unique claims, no duplicate IDs, malformed CSV rows or missing claim-source references. No runtime, IPA, pronunciation, tone, model, corpus, dictionary, generated artifact or deployment changed. Independent IPA gold=0; empirical accuracy=null.

## LOC 2012 Word/PDF discrepancy and exact-source parser guard — 2026-11-17

| Work item | Status | Evidence / remaining acceptance |
|---|---|---|
| Preferred LOC 2012 Word source | DONE_VERIFIED | Retrieved HTTP 200 (`application/msword`); Note 3/10 gives ຄຼິສຕຽນ (khitsatīan). LOC source index says to use Word rather than PDF when copying data. |
| Published LOC 2012 PDF Note 3/10 example | SOURCE CONFLICT RECORDED | PDF gives ຫຼັກສາດ (khitsatān); differs from Word source. Retain both records and do not merge examples. |
| Historical LOC 1997 romanized example | PARTIAL / glyph evidence limited | PDF text extraction gives khitsatian, but Lao glyphs are corrupted; no script-form assertion. |
| Exact Lao Note 10 runtime input | DONE_VERIFIED (fail-closed guard only) | `analyze("ຄຼິສຕຽນ")` remains one unresolved token with no IPA/Ukrainian guess. This is a negative regression, not a successful syllable parser. |
| Automatic Note 10 source-role derivation | PARTIAL / BLOCKED | Source-aware Latin crosswalk remains manually supplied; acceptance requires reviewed source syllable spans, overlapping shared-grapheme roles, positive/negative corpus examples and Lao-specialist review. |

## PR #253 mainline closeout — 2026-11-17

| Work item | Status | Evidence / remaining acceptance |
|---|---|---|
| LOC 2012 Word/PDF source discrepancy | DONE_VERIFIED (conflict recorded) | PR #253 merged as `fc61f5413ad26cfd95ad774b00fb80a3853d2d2a`; preferred Word source gives ຄຼິສຕຽນ (khitsatīan), published PDF gives ຫຼັກສາດ (khitsatān); LOC instructs users to copy from Word rather than PDF. |
| Exact Lao Note 10 parser guard | DONE_VERIFIED (negative/fail-closed only) | Exact input ຄຼິສຕຽນ remains one unresolved token without IPA/Ukrainian guess; Verify #4640 and post-merge Verify #4641 passed. This is not automatic segmentation. |
| Automatic Note 10 syllabification/shared-grapheme role derivation | PARTIAL / BLOCKED | Source-aware romanization fixtures still inject roles manually. Acceptance requires reviewed source syllable spans, overlap derivation, broader positive/negative examples and Lao-specialist adjudication. |
| Historical LOC 1997 Lao-script example | PARTIAL / glyph evidence limited | PDF extraction exposes romanized khitsatian, but script glyphs are corrupted; no exact Lao-script form asserted. |

## 2026-11-17 — external orthographic syllabifier assessment

| Work item | Status | Evidence / acceptance |
|---|---|---|
| Bethke Lingua::LO::NLP source review | DONE_VERIFIED (static review only) | Pinned commit c2b0f8a94de1bb78a4927086e644ef87b1572c98; v1.0.3 distribution; Artistic License 2.0 (GPL Compatible); X9 requires X10_3/U+0E4C, while X8 excludes ສ. See SRC-BETHKE-LINGUA-LO-NLP-2017 and CLM-LAO-BETHKE-SYLLABIFIER-NOTE10-LIMIT. |
| Run external syllabifier on exact LOC form | BLOCKED | git clone failed because github.com DNS could not resolve; package was not run. Acceptance: acquire pinned source in a network-enabled environment, execute package tests and exact ຄຼິສຕຽນ get_syllables/get_fragments, record exact output. |
| Automatic LOC Note 10 source-role derivation | PARTIAL / BLOCKED | Candidate does not demonstrate the required unmarked ສ coda role; a separate LOC-specific source grammar and specialist-reviewed positive/negative cases remain necessary. |

No runtime, IPA, tone, model, corpus, dictionary or generated artifacts changed. Manual-role fixtures remain explicit; exact LOC source remains fail-closed. Independent IPA gold=0; empirical accuracy=null.

## PR #254 — external syllabifier assessment closeout — 2026-11-17

| Work item | Status | Evidence / remaining acceptance |
|---|---|---|
| Bethke Lingua::LO::NLP static source review | DONE_VERIFIED | Pinned source and license registered; X9 requires X10_3/U+0E4C and X8 excludes ສ. See SRC-BETHKE-LINGUA-LO-NLP-2017 and CLM-LAO-BETHKE-SYLLABIFIER-NOTE10-LIMIT. |
| Run candidate on exact LOC Word form | BLOCKED | GitHub clone failed DNS; no package execution. Acceptance: obtain pinned source in a network-enabled environment, run package tests, execute get_syllables/get_fragments on ຄຼິສຕຽນ and preserve exact output. |
| Automatic Note 10 source-role derivation | PARTIAL / BLOCKED | Candidate does not demonstrate the unmarked ສ coda role. Need a separately evidenced LOC-specific orthographic parser, reviewed source spans/overlap roles, positive/negative cases and Lao-specialist adjudication. |

PR #254 merged as `ca64158ce0b6d92ef0a01956f16ed941277bf446`. Exact-head Verify #4668 / run 44088848659 and exact-main Verify #4670 / run 44089165636 both SUCCESS. Registry integrity: 84 unique sources / 110 unique claims, no duplicate IDs or malformed nonblank rows. No runtime, IPA, tone, model, corpus, dictionary, generated artifacts or deployment changed. Gold=0; accuracy=null.

## PR #255 closeout — 2026-11-17

PR #255 merged as `d8314fc527a9e246df9b22ca570a533ff9122679`. Exact PR-head Verify #4671 / run 44089568451 and exact merged-main Verify #4672 / run 44089755616 passed all configured steps. This PR only synchronized documentation with PR #254; it did not alter code, data, runtime, corpus, IPA labels, generated artifacts or deployment. The Bethke syllabifier remains a static-only candidate assessment; its runtime execution is blocked by DNS, and LOC Note 10 source-role derivation remains PARTIAL/BLOCKED. Registry remains 84 unique sources / 110 unique claims; gold=0; accuracy=null.
