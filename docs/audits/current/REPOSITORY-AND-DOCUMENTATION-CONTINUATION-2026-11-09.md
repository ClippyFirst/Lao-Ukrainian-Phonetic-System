# Repository and documentation continuation audit — 2026-11-09

## Executive assessment

**Current state: engineering-verified research prototype; not linguistically release-ready.** The default branch is `main` at `819c2528b1c726adfd3062be89084fedce7ad84d`. The default production route is the deterministic `hybrid-deterministic` engine, with the typed IPA-to-Ukrainian adapter retained as the only phonetic target boundary. The independent expert-adjudicated IPA gold corpus remains empty; dictionary-relative benchmark agreement and full Ukrainian rendering must not be described as phonetic accuracy.

This checkpoint focuses on repository navigation, documentation authority, research discoverability and reconciliation of the current benchmark PR with the actual default branch. It does not change linguistic rules, canonical datasets, generated browser assets or production runtime code.

## 1. Baseline and repository state

| Item | Observed state |
|---|---|
| Repository | `ClippyFirst/Lao-Ukrainian-Phonetic-System` |
| Default branch | `main` |
| Starting HEAD | `819c2528b1c726adfd3062be89084fedce7ad84d` |
| Latest main commit observed | `Add provisional grapheme sound hints to Lao hybrid` |
| Open PRs | 11 |
| Open documentation PR | [#148](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/148), based on stale main ancestor `c0d7218...`, not mergeable at inspection |
| Open benchmark PR | [#156](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/156), Draft, based directly on current main HEAD |
| PR #156 exact-head Verify | [#42576010011 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42576010011), head `0432a0a779871992c6cb95a72457c6a3e5bd2a46` |
| Current-main exact-head Verify | No run associated with commit `819c2528...` was returned by the inspected PR-workflow lookup; do not infer a fresh mainline pass from PR #156 |
| Local checkout/tests | Not available in this connector-only session; no local execution is claimed |

The PR #156 verification is valid for its own exact head and includes 293 Python, 143 Node and 19 Chromium tests plus the workflow's corpus, audit, build and generated-artifact checks. It is not evidence that a different commit or the current mainline has independently passed those checks.

## 2. Architecture and canonical ownership

The current repository structure is coherent. A broad directory migration would create link churn and test/workflow risk without solving a demonstrated defect. Preserve these ownership boundaries:

| Concern | Canonical location | Rule |
|---|---|---|
| Python runtime | `src/lao_ukrainian/` | Source implementation and CLI/API |
| Lao linguistic registries | `data/lao/*.csv` | Authoritative editable language data |
| Evidence provenance | `data/evidence/sources.csv`, `claims.csv` | Source metadata and claim links |
| Benchmark contracts and aggregates | `data/benchmark/`, `scripts/`, `tests/` | Keep raw restricted corpora and per-item outputs out of Git |
| Machine-readable contracts | `schemas/` | Versioned JSON schemas |
| Browser runtime | `web/` | Native ES modules; keep Python/browser contracts tested |
| Generated browser registry | `web/data.js` | Generated from canonical CSVs; never hand-edit |
| Static pages/build | `index.html`, `system.html`, `scripts/build_web.py` | Static, framework-free site |
| User and developer docs | Root Markdown and `docs/` | One canonical index and explicit authority |
| Current audits | `docs/audits/current/` | Dated state snapshots, not normative specs |
| Execution ledger | `docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md` | One canonical task ledger and chronological handoff |

The primary pipeline remains:

`Lao orthography → structural analysis → source phonology → typed IPA → Ukrainian target adaptation → Ukrainian practical orthography`.

The separate CLDR/BGN-oriented romanization route is orthographic and lower-information; it is not a G2P engine, not an IPA fallback and not a source of tone.

## 3. Documentation hierarchy and navigation contract

The intended navigation is:

1. Root `README.md`: concise project identity, current status, quick start and links to canonical documentation.
2. `docs/README.md`: subject-based documentation index and source-of-truth precedence.
3. `docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md`: only canonical living task ledger and chronological handoff.
4. `docs/audits/README.md`: current-vs-historical audit navigation.
5. `docs/audits/current/`: dated evidence snapshots and research workpacks.
6. `docs/agents/codebase-map.md`: implementation entry points and data flow.
7. `AGENTS.md` and `CONTRIBUTING.md`: agent/developer process, commands and invariants.

Do not create a second master plan, a parallel status spreadsheet, or a competing docs landing page. Dated audits should state their inspected commit, scope, evidence and limitations. Update indexes when a canonical document is added. Keep the root README short enough to orient a new user; detailed metrics belong in versioned research reports.

## 4. Current benchmark findings and interpretation

PR #156 adds a pinned, reproducible comparison inventory for the additional G2P candidates. Its report has been ported into the mainline documentation as `docs/research/LAO-G2P-ENGINE-AND-DATASET-INVENTORY-2026-11-08.md`; benchmark implementation/workflows remain on PR #156 until their overlap with other open PRs is reconciled.

Important confidence-gated results on the 100-row dictionary-seeded MekongPhon reference split:

| Engine | Segmental exact | CER | Typed IPA coverage |
|---|---:|---:|---:|
| MekongPhon-reference deterministic profile | 90/100 | 6.64% | 97% |
| MekongPhon Neural | 82/100 | 6.64% | 100% |
| ClippyFirst hybrid | 85/100 | 14.45% | 91% |
| Epitran | 71/100 | 10.96% | 100% |
| Vientiane baseline | 69/100 | 11.46% | 97% |
| Lao2IPA | 68/100 | 8.97% | 100% |
| orthography2ipa | 32/100 | 19.60% | 100% |
| Transphone supervised Lao | 19/100 | 24.25% | 100% |
| LanguageNet Phonetisaurus | 0/100 | 78.90% | 100% |

These are reference-relative results, not independent expert accuracy. Transphone's published PER 8.4% is from a different test split and cannot be compared directly. Full output coverage does not imply correct IPA. The hybrid's 100% Ukrainian rendering includes provisional grapheme hints; its typed IPA coverage is a separate metric.

The HVULao 1k corpus contains text but no IPA reference. It is therefore suitable for sentence-domain coverage and runtime stress, not phonetic accuracy. The confidence-gated run reports 341/1,000 hybrid IPA-complete sentences (34.1%), while Ukrainian rendering is 1,000/1,000 (100%) and syllable IPA coverage is 94.14%. MekongPhon Neural completes 934/1,000 IPA outputs (93.4%). Earlier stress figures that counted provisional hints as accepted IPA are superseded by the confidence-gated report.

## 5. PR and branch reconciliation

| PR | Subject | Current disposition |
|---|---|---|
| #156 | Additional G2P engines, Transphone, confidence-gated benchmarks and dataset inventory | Keep Draft/open; exact-head CI is green; implementation overlaps with #137–#148 benchmark scripts/workflows and master audit files |
| #148 | Documentation/architecture refresh | Keep open and do not merge blindly; based on `c0d7218...`, behind current mainline and reported non-mergeable; its docs claims need reconciliation with main's newer hybrid and #156 results |
| #147 / #146 | HVULao benchmark and deterministic MekongPhon-reference profile | Leave unchanged pending stack-level comparison |
| #145 | Neural-first production proposal | Do not treat as adopted; current owner-approved production direction is deterministic hybrid |
| #137–#142 | Earlier engine, benchmark, parser and target work | Preserve existing branches/PRs; inspect their current diffs before any merge or closure decision |

No PR was merged, closed, retargeted or force-pushed in this documentation continuation. No branch was deleted. PR #156 is the authoritative source for the benchmark implementation until its code is reconciled; only its self-contained research report was ported here.

## 6. Adopted external engineering references

The five supplied repositories are methodology references, not runtime dependencies:

- [unlazy](https://github.com/Leonxlnx/unlazy): explicit completion criteria, evidence-gated status and verified handoff discipline.
- [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill): accessibility-first web review, semantic controls, focus/keyboard behavior, contrast, responsive layouts and restrained design. The project's `docs/DESIGN-SYSTEM.md` remains authoritative.
- [obra/superpowers](https://github.com/obra/superpowers): scoped plans, genuine RED/GREEN test-first work, root-cause debugging, review and verification before completion.
- [mattpocock/skills](https://github.com/mattpocock/skills): focused reusable skills, deep modules, clear interfaces, behavioral tests and source-backed research.
- [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail): trace real code/data flow, inspect connected callers and consumers, preserve trust boundaries and data integrity, and report skipped checks/residual risk.

Selected practices are already recorded in `AGENTS.md`. Do not vendor these repositories, import their code/skills/CLIs, or add them as runtime dependencies. Avoid duplicating their generic guidance across every document; link to the canonical local policy instead.

## 7. Task ledger

| Task | Status | Acceptance / blocker |
|---|---|---|
| Preserve current repository architecture and canonical data ownership | DONE_VERIFIED | Main tree inspected; no unnecessary directory migration |
| Establish one documentation landing page and audit index | DONE_VERIFIED | `docs/README.md`, `docs/audits/README.md` |
| Make current engine and benchmark status discoverable from README/docs | DONE_VERIFIED | Links and status language updated; metrics remain in research report |
| Port the standalone additional-engine/dataset research inventory | DONE_VERIFIED (documentation port) | Report content copied from PR #156; its benchmark code is not claimed merged |
| Reconcile PR #148 documentation branch with current main | PARTIAL | Branch is stale/non-mergeable; review/retarget or close only after complete diff comparison |
| Reconcile PR #156 implementation overlap with #137–#148 | PARTIAL | Requires file-level diff and dependency-stack decision; keep Draft |
| Current-main exact-head CI evidence | BLOCKED / not observed | Need a Verify run attached to the exact main HEAD or a fresh run on a successor commit |
| Independent expert-adjudicated IPA gold | BLOCKED | 0 adjudicated records; requires lawful audio/text access, qualified independent annotators and adjudication |
| Manual accessibility acceptance | PARTIAL | Screen readers, physical devices, real 200%/400% zoom and human visual review remain outstanding |
| Linguistic production sign-off | BLOCKED | Independent gold and qualified Lao phonetics review absent |

## 8. Verification and limits

- Inspected repository metadata, recursive main tree, recent commits, all open PR summaries, branch heads, PR #148/#156 metadata and changed-file lists, current README/docs indexes, agent instructions, codebase map, canonical handoff and current audit.
- PR #156 exact-head Verify #42576010011 is SUCCESS on `0432a0a...`; the PR body records 293 Python, 143 Node and 19 Chromium tests plus repository/data/build checks.
- No local checkout, shell tests, local benchmark, full Markdown-link crawler or browser session was available in this connector-only pass.
- No exact-main Verify result was returned for `819c2528...`; this is recorded as a verification gap rather than inferred from PR checks.
- No phonetic accuracy, gold-corpus completion, manual accessibility acceptance or release approval is claimed.

## Readiness

**Research-ready as an engineering and evidence-management prototype; not linguistically release-ready.** The repository now exposes the latest comparative research and a clearer documentation authority map. The production hybrid remains unchanged. The genuine next blockers are exact-main verification, PR-stack reconciliation, independent IPA gold/adjudication and human accessibility review.


## Final exact-head verification — 2026-11-09

- Documentation continuation final head: 38498099290ede1d8ddc208e64dfcb1315e54c8b.
- Exact-head Verify [#42577920085 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42577920085) on branch main and the exact final SHA above.
- Hosted job steps passed: independent IPA-gold schema/structure validation; repository data/evidence audit; 289 Python tests; external-G2P harness compile and CLI check; locked npm ci; 143 Node/browser-engine tests; static build and canonical browser-data regeneration; generated-data drift check; 19 Chromium UI tests; built-page and relative-asset assertions.
- Separate Markdown-link integrity scan over the seven changed Markdown files against the complete 179-blob repository tree found 0 missing local link targets. This scan checked local path targets, not every external URL or heading anchor.
- The workflow was triggered by the successive direct-main documentation commits. Earlier intermediate Verify runs also completed successfully; the acceptance result above is the one attached to the final HEAD.
- No local checkout or local shell execution is claimed. CI is hosted verification; linguistic accuracy and human accessibility acceptance remain outside its scope.


## Subsequent hybrid grapheme-coverage implementation — 2026-11-09

This section supersedes the earlier statement that the 2026-11-09 continuation did not change linguistic/runtime code. The earlier documentation-only work remains intact; this is the later code/data continuation.

### Implemented

- Added five source-attested composite vowel templates to the canonical `data/lao/vowels.csv` and Python parser: `ເ◌ີຍ` /ɤːj/, `ໂ◌ຍ` /oːj/, `ແ◌ວ` /ɛːw/, `◌ອຍ` /ɔːj/, and `◌າຽ` /aːj/.
- Added medial short IA `◌ັຽ` /iə̯/ as a second spelling of the existing `IA` vowel ID. This is separate from preposed `ເ◌ັຍ` and the long IA variants.
- Mirrored the new structures in `web/engine.js` and generated `web/data.js`; added shared Python/browser fixtures and near-miss controls. The AEW regression uses `ແມວ`, avoiding a real ambiguity with a labialized onset candidate in synthetic `ແກວ`.
- Preserved Lao ellipsis `ຯ` as non-phonological passthrough in Python and browser instead of routing it through an unknown phoneme marker.
- Strengthened coverage gates: all 83 assigned codepoints in the Unicode 18 Lao block must have a typed grapheme role or explicit orthographic/numeric passthrough in Python and browser. Pali/Sanskrit and Khmu characters are recognized but are not assigned invented modern-Lao IPA.
- Added five specific evidence claims linked to the existing Richard Ishida orthography source for the five glide-vowel templates. The medial IA spelling is already covered by `CLM-LAO-VOWEL-IA-SHORT`.
- Updated `README.md`, `docs/lao-grapheme-ipa-preview.md`, `docs/vowel-template-coverage.md` and this audit.

### Coverage contract and limitations

| Dimension | Acceptance / current claim |
|---|---|
| Assigned Lao-block codepoint recognition | 83/83 assigned Unicode 18 codepoints must be typed as a grapheme role or orthographic/numeric passthrough. |
| Modern-Lao phonetic interpretation | Contextual, syllable-structure-dependent; no claim that every sign has an independent sound. |
| Composite vowel coverage | Six newly explicit glide-bearing forms added; the five additional source-attested forms plus medial short IA are regression-tested in Python and browser. |
| Pali/Sanskrit extensions | Recognized as non-core; no modern-Lao phonetic mapping. A dedicated Pali reading profile would require separate source-language rules and review. |
| Khmu U+0EDE/U+0EDF | Recognized as out of modern-Lao scope; no Lao IPA mapping. |
| Repetition mark U+0EC6 | Recognized as orthographic-only. Expansion to a repeated Ukrainian word is not claimed because lexical word segmentation is outside the current parser contract. |
| Obsolete/cancellation and Pali marks | Structurally recognized, not treated as modern-Lao phonemes. |
| Independent IPA accuracy | Still blocked by 0 expert-adjudicated gold records. |

### Task ledger

| Task | Status | Acceptance evidence |
|---|---|---|
| `GRAPHEME-RECOGNITION-001` | DONE_VERIFIED | Python and browser tests iterate all 83 inventory entries; require a typed role or explicit passthrough. |
| `GLIDE-VOWEL-COVERAGE-001` | DONE_VERIFIED | Six new source-backed forms have shared fixtures and Python/browser tests; registry IDs and parser structures are checked. |
| `LAO-ELLIPSIS-PASSTHROUGH-001` | DONE_VERIFIED | Python/browser tests assert punctuation is preserved, not treated as phonetic material. |
| `REPETITION-MARK-EXPANSION-001` | DEFERRED | Requires word/phrase scope resolution; current engine does not claim lexical word segmentation. Acceptance: preserve meaning of U+0EC6 by repeating the correctly scoped Ukrainian unit, with mixed-phrase regressions. |
| `PALI-PRONUNCIATION-PROFILE-001` | DEFERRED | Outside contemporary Lao profile; requires Pali phonological rules, orthographic conventions and independent review. |
| `KHMu-PRONUNCIATION-PROFILE-001` | DEFERRED | Khmu is a distinct language; requires a separate language profile and evidence. |
| Independent expert IPA gold | BLOCKED | No adjudicated records; requires rights-cleared audio/text and qualified independent annotation/adjudication. |

### Verification history and current head

- Earlier Verify runs failed while the new browser matcher and test controls were being reconciled. Those failures were investigated; they are not presented as passes.
- Final code-and-test HEAD `dcc363bee42e3ed53c9b1c45c31b336e8483da06`: exact-head Verify [#42579401059 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42579401059).
- Exact run passed 292 Python tests, 146 Node/browser-engine tests and 19 Chromium UI tests. Independent IPA-gold schema validation, repository data/evidence audit, external-G2P harness syntax/CLI, locked dependency install, static build, generated browser-data reproducibility and built-page/relative-asset checks all passed.
- Python and browser coverage tests both iterate all 83 assigned Unicode 18 Lao-block codepoints and require typed grapheme-role evidence or explicit passthrough. The shared vowel fixtures cover all six new forms.
- The code checkpoint was also deployed through GitHub Pages workflow [#42579237707 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42579237707) at the verified code checkpoint `523a21e8...`; deployment for the later test-only/doc continuation is separately tracked by run #42579401010.
- Local shell tests were not run in this connector-only session. CI is hosted verification; independent expert IPA gold and manual accessibility/linguistic acceptance remain outside its scope.


### Final documentation snapshot verification

- Documentation snapshot HEAD `d4d477edea541f6674353a3f459fe7f5032c40af` also passed exact-head Verify [#42579520016 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42579520016): 292 Python, 146 Node and 19 Chromium tests passed; configured data/evidence, generated-artifact, build and built-page checks passed. This confirms the final audit/handoff/index updates did not introduce regressions.

## Additional G2P literature and benchmark continuation — 2026-11-09

### Newly verified sources

- Hansakunbuntheung & Thatphithakkul (O-COCOSDA 2016; DOI 10.1109/ICSDA.2016.7919010) evaluate unsupervised many-to-many graphoneme alignment including Lao and report 91.28% Lao word accuracy on their own dictionary. The accessible paper record does not expose the exact Lao split, dictionary rights, tone convention or executable artifact. Treat this as a research candidate, not a reproduced result.
- SIGMORPHON 2021 includes Khmer in its low-resource G2P task and Vietnamese (Hanoi) in medium-resource, but not Lao. SIGMORPHON 2022 includes Thai → Eastern Lawa and nine other pairs, but not Lao. Its 100-target/1,000-transfer, 100-target-only and 1,000-target-only settings are useful for a **SIGMORPHON-inspired Lao adaptation**, not an official Lao benchmark.
- CharsiuG2P / multilingual ByT5 repository at commit `0c929390759fb94f8ecdfc05cc0bc5f2ff2dc0f4` contains a Lao WikiPron source metadata file, but a recursive inspection of the complete tree found no Lao file in `data/train`, `data/dev` or `data/test`; Khmer is present. It is not a trained/evaluated Lao baseline on that revision and is excluded from supervised Lao benchmarking.
- Ueda (1994) remains the bounded five-tone central Vientiane source. LDC Babel documentation uses a six-tone analysis because the low-tone phonemic status is disputed. Do not collapse these conventions silently.

### Repository changes

- Added source IDs `SRC-HANSAKUNBUNTHEUNG-GRAPHONEME-2016`, `SRC-SIGMORPHON-2021-G2P`, `SRC-SIGMORPHON-2022-G2P`, `SRC-CHARSUIG2P-2022` and claims for graphoneme alignment, SIGMORPHON-inspired protocol and CharsiuG2P support audit.
- Added the findings and acceptance gates to `docs/research/LAO-G2P-ENGINE-AND-DATASET-INVENTORY-2026-11-08.md`.
- Created the Undermind workspace [Lao G2P research](https://app.undermind.ai/projects/5603c8d1-3260-4f39-b0d5-8fd6ffa3a081) and durable research memo at [benchmark-and-engine-findings-2026-11-09.md](https://app.undermind.ai/projects/5603c8d1-3260-4f39-b0d5-8fd6ffa3a081?path=%2Fresearch%2Fbenchmark-and-engine-findings-2026-11-09.md). The comprehensive literature search remains in progress.

### Revised task ledger

| Task | Status | Acceptance / blocker |
|---|---|---|
| Add graphoneme paper to source and claim registries | DONE_VERIFIED (registry) | Paper-reported 91.28%; exact original dataset/split/code/licensing still unknown |
| Add SIGMORPHON 2021/2022 methodological sources | DONE_VERIFIED (registry) | No official Lao target/test set; adaptation must be explicitly labelled |
| Audit CharsiuG2P Lao model support | DONE_VERIFIED (negative result) | Inspected revision has no Lao train/dev/test split; not a supervised Lao comparator |
| Reproduce graphoneme paper result | BLOCKED | Full paper/data/split/code and rights not yet established |
| Run a SIGMORPHON-inspired Lao 100/1,000/transfer study | TODO | Needs a frozen independent test set, reproducible nested splits, and a justified donor language |
| Independent expert IPA gold and linguistic sign-off | BLOCKED | 0 adjudicated gold records; requires human annotation and adjudication |

### Verification boundary

- No runtime phonology, target adapter, production engine, benchmark outputs or generated browser assets were changed in this research continuation.
- Exact-head Verify for the first source/claim/doc commits passed; the final research correction and audit/handoff commits are awaiting their own final exact-head Verify. Do not infer a final-head pass from earlier runs.
- No local shell execution is claimed. Hosted CI is the only code verification evidence in this connector-only session.
- Readiness remains research-ready evidence/prototype, not linguistically release-ready.

### Final research-continuation exact-head Verify

- Audit and research changes at HEAD `7f4f8a61f73c5508b21276ac43ce9cfaec330b0c` passed exact-head Verify [#42582196430 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42582196430).
- Results: 292 Python tests, 146 Node/browser-engine tests, 19 Chromium UI tests; IPA gold schema, repository data/evidence audit, external-G2P harness syntax/CLI, locked npm install, build, generated browser-data reproducibility/drift and built-page/relative-asset checks all passed.
- The research-only continuation changed no runtime code, parser data or generated browser assets. This Verify is engineering/regression evidence only; it does not close the independent IPA gold or expert sign-off blockers.
- The audit/handoff update after this checkpoint is documentation-only; the final handoff commit still receives its own exact-head Verify.

## No-audio written-evidence continuation — 2026-11-09

### Decision and scope

- User cannot provide audio. Do not make audio delivery or new expert listening a prerequisite for continued engineering.
- Accepted evidence classes: primary written phonological descriptions, published IPA examples, attributed lexicons, Unicode/orthographic specifications, source-code inspection of published deterministic analyzers, and reproducible text-only tests.
- Not accepted as established by this evidence alone: acoustic fidelity, prosodic naturalness, independent IPA accuracy, or unqualified claims about all Lao dialects.

### New source findings

- Enfield (2007) §3.1 describes an optional minor C0V0 before the major syllable, with no independent tone, and V0 short /a i u/ in his sample. His preface characterizes informal semi-rural speech; do not silently transplant this whole analysis to the project's Vientiane profile.
- Ueda (1994) specifically documents the central Vientiane exceptional non-final open /a/ minor syllable. Existing conservative potential-minor-open-A withholding remains bounded to that evidence.
- Osatananda (1997) describes one Vientiane variety with five lexical tones and an underlying lexical-tone analysis rather than mechanical tone derivation. This reinforces that grapheme-class rules are an orthographic prediction profile, not a universal explanation of lexical tone.
- Phissamay et al. (2007) provide a rule-based Lao orthographic syllabification algorithm for line breaking and report >98%, but accessible material does not give enough benchmark detail to reproduce the figure.
- LaoNLP 1.3.0 code is Apache-2.0 and includes a regex syllable tokenizer based on Phissamay et al.; its bundled lao-eng-dictionary.csv has a distinct MIT license notice. The dictionary is lexical, not IPA.
- Kaikki/Wiktextract's 2026-10-01 English Wiktionary extraction includes a machine-readable Lao dictionary with IPA fields, but programmatically expanded Lua pronunciation modules are included alongside manual entries. Use only as secondary diagnostics after provenance classification; underlying Wiktionary data is CC BY-SA 4.0/GFDL.
- Wiktionary lo-pron is a generated pronunciation module, not independent IPA gold.

### Changes on dedicated branch

- Branch: research/written-evidence-phonology-2026-11-09, based on main SHA 4570c5ff4733476601e02c791517ac36944d6a46.
- Added source and claim records for the written phonology, Lao syllabification, LaoNLP, MIT dictionary, Kaikki/Wiktextract and Wiktionary lo-pron.
- Added the published LaoNLP segmentation example ພາສາລາວໃນປັດຈຸບັນ → ພາ | ສາ | ລາວ | ໃນ | ປັດ | ຈຸ | ບັນ as a Python and browser regression fixture. This is structural implementation parity, not pronunciation gold.
- Added a research inventory addendum describing the no-audio improvement path and licensing/provenance limits.
- No runtime phonology or target adaptation changes were made because the newly found sources do not justify a safe unambiguous rule change. In particular, Enfield's broader minor-syllable template is not substituted for Ueda's narrower Vientiane-specific evidence.

### Task ledger

| Task | Status | Acceptance / blocker |
|---|---|---|
| Register new written sources and evidence claims | DONE_VERIFIED (registry edits; CI pending) | Each source's dialect, scope and rights limits recorded |
| Add LaoNLP published segmentation fixture to Python and browser tests | PARTIAL | Exact-head PR Verify required; fix any failing boundary or IPA outputs |
| Expand minor-syllable tone rule from /a/ to /a i u/ | DEFERRED | Enfield sample differs in scope from central Vientiane; exact C0 onset inventory and mapping not established |
| Add LaoNLP word dictionary to production segmentation | BLOCKED pending data inspection | Need schema, size, exact word-boundary semantics, and clean reproducible import; not an IPA source |
| Use Kaikki/Wiktionary IPA as diagnostic data | TODO | Need classify manual vs Lua-generated records and record per-entry provenance/licensing |
| Add lexical pronunciation exceptions | TODO | Only with explicit reusable source, dialect/variant and IPA provenance |
| Independent acoustic validation | DEFERRED | User cannot provide audio; no claims of acoustic fidelity will be made |

### Verification

- Connector-only changes; no local shell was available.
- A draft PR will be opened to trigger the repository's PR Verify workflow because the current push trigger does not include research/**.
- No runtime data/generated browser artifact changed. Final acceptance depends on hosted CI for the exact branch head.

### Additional written evidence from completed literature review

- Added Lew (2014), Enfield (2020), Lao dialect LSP (2015), Davis (2015), Sengsoulin (2009), Yanagimura (2011) and WikiPron (2020) to the source registry and claims.
- The Vientiane LSP supports the existing same-/ai/ mapping for ໃ and ໄ in Vientiane while warning against applying it to Luang Prabang.
- Enfield (2020) supports a foot-based model: one stressed tone-bearing syllable with dependent unstressed syllables; grammatical and phonological word boundaries may differ. This argues against inferring phrase prosody from the current isolated-syllable parser.
- Davis (2015) supports treating historical ຣ as context/lexeme-sensitive (/h/ in some historical conditions, /l/ elsewhere), not as a universal phoneme mapping.
- Yanagimura (2011) documents contextual F0 effects across 25 Vientiane bitonal sequences. Current IPA tone categories remain lexical/word-level; phrase-level realization is explicitly outside this engine's current contract.
- WikiPron Lao coverage/provenance remains unverified; it is not admitted as a benchmark or gold source.
- Updated research inventory with these source findings and implementation implications.

### Verification checkpoint for first test batch

- PR #157 initial exact branch head 47d63361ec22a60bf2fb6e3fd6a4f682c86d7fdc passed Verify #42583598265 — SUCCESS: https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42583598265
- Results on that head: 293 Python tests, 147 Node/browser-engine tests, 19 Chromium UI tests; all pass. Repository data/evidence audit, IPA gold schema, external-G2P harness syntax/CLI, locked npm install, build, generated-data reproducibility/drift and built-page/relative-asset checks passed.
- Subsequent commits add only evidence registry and research documentation; they still require a fresh exact-head PR Verify.

### Final exact-head verification of written-evidence branch

- Final audit/handoff branch checkpoint `cc05c0d40954d14fd84c6a716918b3755c1436df` passed exact-head Verify [#42583884292 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42583884292).
- Results: 293 Python tests, 147 Node/browser-engine tests and 19 Chromium UI tests; all passed. IPA gold schema, repository data/evidence audit, external-G2P harness syntax/CLI, locked install, build, generated browser-data reproducibility/drift, and built-page/relative-asset checks also passed.
- No runtime phonology or target-adapter code changed. The new segmentation example is a written-source structural parity test only.
- The final handoff update that follows this audit commit is documentation-only and will receive a fresh exact-head Verify.

### LaoNLP lexical resource inspection boundary

- Inspected the 77 KB `Lao-Dictionary.txt` word list. Its own BSD-style header says it was created for word wrapping and that compounds have mostly been reduced to their parts. It has orthographic items but no IPA; it is a candidate hint list, not lexical segmentation gold.
- Confirmed a separate MIT notice for `lao-eng-dictionary.csv`, distinct from the package Apache-2.0 license. The CSV is 2.73 MB and the connector's GitHub contents endpoint did not expose its body; the connected Firecrawl account had no credits. Its schema and rows remain uninspected, so it is not integrated.
- Recorded these distinctions in the source/claim registries and research inventory. No lexical resource was copied into the production runtime.
