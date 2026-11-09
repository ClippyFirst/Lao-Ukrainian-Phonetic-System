# Current exact-head continuation — 2026-11-09 (authoritative addendum)

**Repository / branch:** `ClippyFirst/Lao-Ukrainian-Phonetic-System`, `main` only. This addendum supersedes the older checkpoint summaries below wherever their commit, CI or metric values differ.

- **Starting checkpoint reviewed:** `1df6fbf362f051de7433913c7c718662bbf193d8` (current main HEAD at inspection; parent `d6aa703bf0637d65c4a8245ba6cf4d103ae34072`).
- **Exact-head Verify:** [#42636160154 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42636160154), exact SHA `1df6fbf362f051de7433913c7c718662bbf193d8`. The single job completed successfully: IPA-gold structure validation, repository evidence audit, Python tests, external-G2P harness syntax/CLI, locked npm install, browser-engine tests, generated-data regeneration/drift check, Chromium UI tests, and built-page/relative-asset checks. The preceding exact-head report records 319 Python, 147 Node/browser-engine and 19 Chromium tests; this workflow is engineering verification only.
- **Current PR state:** only PR #145 is open; it proposes neural-first production and remains unmerged because it conflicts with the adopted deterministic hybrid. The 22 existing branches are preserved; no branch was deleted or rewritten. No PR was merged or closed during this documentation-only continuation.

## Corrected coverage and benchmark interpretation

The phrase “100% coverage” must always name its denominator and output class. The repository has several distinct measures:

| Measure | Latest observed result | What it means / does not mean |
|---|---:|---|
| Assigned Lao Unicode codepoint handling | 83/83 (100%) | Each assigned codepoint has a typed role or explicit orthographic/numeric passthrough. Not full phonology. |
| HVULao sentence rendering | 1,000/1,000 (100%) | Every benchmark input receives a visible Ukrainian-side rendering; provisional/unknown markers and passthrough are included. Not 100% IPA. |
| HVULao analyzed-unit rendering | 21,534/21,534 (100%) | Visible rendering of analyzed units; not all units have supported IPA. |
| HVULao hybrid IPA-complete sentences | 346/1,000 (34.6%) | A sentence is complete only when all required Lao phonetic units meet the benchmark's typed IPA confidence gate. |
| HVULao syllable IPA coverage | 94.21% | Syllable-level typed IPA construction; the corpus has no IPA gold and this is not accuracy. |
| 100-word dictionary-seeded hybrid typed IPA coverage | 91% segmental; 86% tonal | Missing/withheld outputs remain in the full denominator. |
| 100-word hybrid concordance | 14.45% segmental CER; 34.06% tonal CER | Reference-relative error, not independently adjudicated phonetic accuracy. |

On the same 100-word reference split, Lao2IPA measured 8.97% segmental and 11.97% tonal CER at 100% coverage; MekongPhon Neural measured 6.64% and 8.29% at 100% coverage. ClippyFirst therefore has materially worse measured concordance on this split and lower typed IPA coverage. The split is dictionary-seeded, not project-certified gold; the held-out vocabulary also contributed to validation-sentence generation/checkpoint selection. These results are diagnostic and cannot establish which system is linguistically correct.

The latest HVULao confidence-gated report supersedes earlier 66.9% / 67.6% complete-sentence figures that counted provisional preview values as accepted IPA. The corrected hybrid result is **34.6% IPA-complete sentences**, **94.21% syllable IPA coverage**, and **100% visible rendering**. Earlier 97.85% syllable coverage is also superseded by the current confidence-gated hybrid report. The difference is a stricter typed-confidence denominator, not a regression in visible rendering.

## Documentation and upstream-methodology reconciliation

The documentation architecture remains intentionally singular:

1. Root `README.md`: user-facing orientation, accurate current status and quick start.
2. `docs/README.md`: task-oriented documentation routes and subject index.
3. `docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md`: one canonical chronological execution ledger.
4. `docs/audits/README.md`: current/historical audit navigation.
5. `docs/audits/current/`: dated evidence snapshots; never competing specifications.
6. `docs/agents/codebase-map.md`: implementation/data-flow map.
7. `AGENTS.md` and `CONTRIBUTING.md`: agent and contributor execution rules.

The five supplied repositories (Unlazy, UI UX Pro Max, Superpowers, Matt Pocock Skills, Ponytail) are methodology references only. Their useful patterns are adapted as repository-local practices: explicit acceptance evidence and honest handoffs; scoped plans and red/green/refactor; shared glossary and clear decision records; review beyond the diff; accessibility, responsive and interaction checks. No external skill bundle, code, hook, CLI, dataset, asset or runtime dependency is copied or installed. Upstream license files do not automatically license every embedded asset or dataset.

## Current task ledger

| Workstream | Status | Acceptance / blocker |
|---|---|---|
| Mainline engineering verification at exact SHA | DONE_VERIFIED | Verify #42636160154 SUCCESS on `1df6fbf...`; counts and gates above. |
| README and documentation navigation correction | DONE_VERIFIED after exact-head CI | Explicitly distinguish rendering, typed IPA coverage and concordance; remove duplicate navigation entry. |
| Independent expert-adjudicated IPA gold | BLOCKED | Current corpus has 0 adjudicated items; requires rights-cleared Lao source material, qualified independent annotators and adjudication. |
| Lexical word-boundary gold | PARTIAL | Orthographic lists are hints only; acceptance requires contextual Lao text with independently annotated lexical boundaries and adjudication. |
| Whole-Kaikki per-value IPA provenance | PARTIAL | 100-page source-revision sample is verified; whole-corpus per-sound origin and complete transitive Lua dependency closure remain unproven. |
| Acoustic/prosodic validation | BLOCKED | Requires suitable audio, speaker/dialect metadata, alignment and qualified phonetic evaluation. |
| Manual accessibility QA | PARTIAL | Automated Chromium checks pass; screen-reader, physical-device, real zoom and human contrast review remain unperformed. |
| Neural-first PR #145 | DEFERRED | Requires a separate owner architecture decision and independent validation; not silently adopted. |

**Readiness:** engineering-verified research prototype; **not linguistically release-ready**. The poor benchmark results are reported rather than hidden. A 100% rendering target is met on the named stress sets; a 100% supported-IPA, phonetic-accuracy or universal-Lao-coverage claim is not met and must not appear in user-facing claims.

## Final documentation-head verification — 2026-11-09

The documentation-navigation correction and restored practical-transcription link were committed on `main` at `651d83079f9e141a961530d92613a479c53cfa16`. Exact-head Verify [#42641288101 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42641288101) completed successfully. Repository evidence audit, 319 Python tests, external-G2P harness syntax/CLI, 147 Node/browser-engine tests, locked dependency install, generated-data regeneration/reproducibility, 19 Chromium UI tests and built-page/relative-asset checks all passed. No linguistic accuracy claim follows from this engineering result.

The current documentation set retains one root README, one documentation index, one master execution ledger, one audit index and dated current/historical audit records. The five supplied upstream repositories remain methodology references only. The repository was not split into additional working branches; this continuation used `main` as requested. The latest PR inventory still shows only PR #145 open and unmerged.

---

# Repository and documentation continuation audit — 2026-11-09

## Latest verified repository head — 2026-11-09

The complete documentation continuation (README status correction, task-oriented docs index, audit register synchronization, current audit addendum and master handoff) is present on `main` through commit `28556d4cab596b4dc96085d3d709a9bef44f20e2`. Exact-head Verify [#42641467759 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42641467759) passed on that SHA. Job log confirms 319 Python tests, 147 Node/browser-engine tests and 19 Chromium UI tests, plus corpus structure, repository evidence, external harness syntax/CLI, locked install, generated-data reproducibility, and built-page/asset checks. This is the latest fully verified checkpoint before this audit-register synchronization.


# Historical mainline continuation checkpoint — 2026-11-09 (superseded by the current exact-head addendum above)

**Current mainline:** `main` is at `dd0a22857b126a00404350dc59be7bb99ab83334` (2026-11-09). This includes the selective benchmark integration, the PR #157 written-evidence and diagnostic lexical-hint work, the filtered 34,937-entry LaoNLP MIT derivative, and the deterministic 100-page Kaikki source-wikitext manifest. No user branch was deleted or rewritten.

**Latest exact-head engineering verification:** [Verify #42635460479 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42635460479) on exact main SHA `dd0a22857b126a00404350dc59be7bb99ab83334`. The job log records 319 Python tests, 147 Node/browser-engine tests and 19 Chromium UI tests. The configured run also completed IPA-gold schema validation, repository data/evidence audit, external-G2P harness syntax/CLI validation, locked browser dependency installation, build, generated browser-data reproducibility/drift checks and built-page/relative-asset checks. This verifies engineering contracts, not independent phonetic accuracy.

PR #157 adds written-source/claim records, the published LaoNLP syllabification regression in Python and browser suites, an attributed 11,208-entry BSD-style orthographic word list, and an optional matcher returning overlapping SOFT_HINT_ONLY spans. A later selective continuation added a filtered 34,937-entry derivative from the separate MIT CSV, plus an offline Git-blob-pinned audit utility. Neither list selects lexical boundaries or enters production parsing, IPA/G2P, Ukrainian adaptation or the browser engine. The raw 2.86 MB MIT CSV is excluded from the repository.

The Kaikki sample was independently rechecked against exact MediaWiki API source revisions in two batches: all 100 manifest titles, page IDs, revision IDs, timestamps and source-text lengths matched; all 100 revisions predate the 2026-10-01 dump date; and all 100 **Lao language sections** contain a direct `{{lo-pron}}` call. Three pages also invoke `lo-pronoun`; one page has an additional `{{IPA}}` call in its Khmu section, not its Lao section. The manifest's FNV-1a values are now recomputed in the regression suite. This is sample-level generated provenance only; Kaikki's post-processing may merge sources and its normalized sound objects do not preserve per-value origin.

**Current PR disposition (2026-11-09):**

| PR | Current state | Disposition |
|---|---|---|
| #157 | Merged to main | Integrated; exact merge-head Verify passed. |
| #156 | Closed unmerged | Useful benchmark scripts, confidence gate, comparator workflows and tests were selectively ported; exact mainline runs and Verify passed. Branch preserved. |
| #148 | Closed unmerged | Stale documentation branch superseded by current mainline docs; the useful UI UX Pro Max pin was selectively ported in commit 5666766a71855929a9f179a95c9587249d81de6f. Branch preserved. |
| #145 | Open, not mergeable | Neural-first proposal conflicts with the adopted deterministic hybrid mainline; not an approved production direction. |
| #146 | Closed unmerged | Deterministic reference-profile implementation and benchmark are superseded by newer mainline versions; mainline benchmark #42591871633 passed. Branch preserved. |
| #147 | Closed unmerged | HVULao 1k script/workflow and documentation superseded by mainline implementation; exact-mainline run #42591871473 passed. Branch preserved. |
| #137–#142 | Closed unmerged | Each stack was compared with main: all changed file paths exist on main; representative code/tests are either byte-identical or superseded by newer integrated implementations. Branches preserved. |
| #149–#155 (excluding #156) | Merged | Their accepted hybrid, mixed-script, numeral, arbitration and grapheme-preview changes are already in main. |

PRs #146 and #147 were closed unmerged only after confirming their benchmark/profile implementations already exist on main in updated forms; closure comments link exact mainline benchmark and Verify evidence. No branch was deleted or rewritten. PR #148 was closed unmerged after selectively porting its only still-useful methodology pin; PRs #137–#142 were closed unmerged after file-path and representative implementation reconciliation; PR #145 remains open and unmerged.

**Five upstream methodology references revalidated:** current upstream `main` commits are Unlazy `16671491f6679ad9378f52604d3bc2415b4120c7`, UI UX Pro Max `4f2dbb67e64969a9a30ab00742f2d55d66ddec2b`, Superpowers `22f0b463e7a5e579904dd6211a520321035526f7`, Matt Pocock Skills `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`, and Ponytail `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846`. All five inspected root `LICENSE` files are MIT. This does not blanket-license embedded assets or third-party data. The project adopts selected workflow, testing, code-review and web-accessibility practices only; no upstream code, skill tree, CLI, dataset, hook or runtime dependency was copied or installed. See `AGENTS.md` for the pinned methodology policy.

**Documentation authority remains singular:** root `README.md` orients users; `docs/README.md` is the documentation index; `docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md` is the canonical execution ledger/handoff; `docs/audits/README.md` indexes current and historical audits; `docs/agents/codebase-map.md` maps implementation. Dated audits are snapshots, not competing specifications. No duplicate master plan or parallel documentation tree was created.

**Remaining blockers:** independent expert-adjudicated IPA gold remains 0; acoustic/prosodic accuracy and linguistic sign-off are not established. Manual screen-reader, physical-device, real zoom and human visual/contrast QA remain PARTIAL. The MIT CSV has been inspected and is used only through a filtered SOFT_HINT_ONLY derivative; lexical boundaries remain unsolved. Kaikki/Wiktionary sample-level generated provenance is verified for 100 pinned pages (all Lao sections call lo-pron), while whole-corpus per-sound provenance remains PARTIAL; the transitive Lua dependency closure below `Module:IPA` and `Module:rhymes` is not fully pinned. No pronunciation dataset has been promoted to gold.

---


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


### Soft lexical-boundary hint prototype — 2026-11-09

- **DONE_VERIFIED — exact-head Verify passed on `4637aeabd2d2d8b317ccdfe736f8185c9dcad966`; documentation-only follow-up below still needs exact-head Verify.** retained the complete upstream BSD notice and attribution with the LaoNLP word list at `data/lao/lexical-hints/Lao-Dictionary.txt`.
- Added optional diagnostic `src/lao_ukrainian/lexical_hints.py`; it reports every multi-syllable lexicon match, preserves overlapping alternatives and labels them `SOFT_HINT_ONLY`. It does not alter syllable segmentation, IPA, Ukrainian rendering, production parser behavior or browser artifacts.
- Added focused unit tests for list loading/deduplication, overlap preservation, default minimum span, input immutability and invalid arguments; exact-head CI remains the acceptance gate.
- This is a candidate-boundary aid only. The source says it was made for line wrapping and compounds are mostly reduced to parts; it is not word-boundary gold.
- The distinct 2.73 MB MIT CSV remains **BLOCKED** pending a complete reproducible fetch, schema review, field-level provenance and independent decision on its intended use.


### Exact-head verification blocker — lexical hint commit

- Branch HEAD: `c67a0b17f917f2c718044757ea6d6904b0db1e4d` (CI trigger-path adjustment included).
- The `verify.yml` push filter now includes `research/**`, but the GitHub connector's ref updates did not create a workflow run; `fetch_commit_workflow_runs` returned an empty list for the exact head. No workflow-dispatch action is available through the connected GitHub tools.
- Exact-head Verify [#42585140497 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42585140497): 298 Python tests, 147 Node/browser-engine tests and 19 Chromium UI tests passed; IPA-gold schema validation, repository data/evidence audit, external-G2P harness syntax/CLI, locked npm install, build, generated-data reproducibility/drift and built-page/relative-asset checks passed.
- Five isolated behavioral checks also passed before CI; repository CI is the authoritative acceptance evidence.
- A related deterministic-profile benchmark workflow [#42585140448 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42585140448) completed with no runtime errors and retained the previously documented held-out comparison profile (not independent accuracy).
- Code batch is DONE_VERIFIED for the exact head above. Any subsequent documentation-only commit still needs its own exact-head Verify.


### Exact-head completion — lexical hint prototype

- Code head `4637aeabd2d2d8b317ccdfe736f8185c9dcad966` passed Verify #42585140497 — SUCCESS: 298 Python, 147 Node/browser-engine and 19 Chromium UI tests; data/evidence audit, IPA-gold schema, external-G2P harness, locked install, build, generated-data drift and built-page checks all passed.
- Deterministic-profile benchmark #42585140448 also passed; no runtime errors. Its 100-row held-out scores are comparative concordance, not independent phonetic accuracy.
- The code batch is DONE_VERIFIED. This audit update itself is documentation-only and will receive a new exact-head Verify.

## PR-stack comparison and documentation exact-head closeout — 2026-11-09

### Branch comparison against main

The following comparisons use the current mainline after the PR #157 merge and the documentation refresh. Ahead/behind counts are Git commit-graph comparisons, not an assessment that every changed commit should be ported.

| PR | Compare status | Ahead / behind | Changed files | Finding |
|---|---:|---:|---:|---|
| #148 | Diverged | 7 / 96 | 7 | Documentation-only refresh based on old main; its audit/code-map/handoff snapshot is superseded by current main docs. |
| #156 | Diverged | 93 / 89 | 16 | Additional benchmark scripts/workflows and reports; substantial overlap with the older benchmark stack. Keep Draft and reconcile selectively. |
| #145 | Diverged | 24 / 96 | 13 | Neural-first runtime/CLI proposal; conflicts with the deterministic hybrid direction already on main. |
| #146 | Diverged | 43 / 96 | 17 | Deterministic reference-profile stack; non-mergeable and not needed to restore main's current hybrid. |
| #147 | Diverged | 81 / 96 | 7 | Stacked on #146, not a standalone mainline change; despite GitHub's mergeable flag, retain the dependency review gate. |
| #137 | Diverged | 79 / 98 | 21 | Older parser/tone/benchmark stack; substantial overlap with later mainline work. |
| #138 | Diverged | 88 / 98 | 22 | Older neural-provider and rights audit stack; based on an older benchmark branch. |
| #139 | Diverged | 84 / 98 | 5 | Immutable-model benchmark stack based on #137. |
| #140 | Diverged | 294 / 98 | 44 | Large stacked rule-engine diagnostics/tone changes; not safe to merge as a standalone PR. |
| #141 | Diverged | 317 / 98 | 19 | Stacked target/transcription work on #140. |
| #142 | Diverged | 337 / 98 | 18 | Stacked grapheme-preview work on #141; later mainline work includes newer successors. |

The older PRs #137–#142 remain untouched because they are heavily stacked and diverged, and later merged work has superseded parts of their scope. Any future reuse should be a narrowly scoped port with current tests and evidence, not a wholesale merge. PRs #148, #145, #146, #147 and #156 likewise remain open and unmodified.

### Documentation refresh and verification

- Documentation reconciliation commit: `416e1c0e5bc4a984a78b32e98cc309432c7abdd6`.
- Updated `AGENTS.md` with the revalidated upstream methodology snapshots and root-license caveat; clarified README lexical-hint scope and current audit navigation; updated the docs index, audit index, codebase map, this audit and the canonical master handoff.
- Exact-head Verify [#42586638191 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42586638191) on that documentation commit: 298 Python, 147 Node/browser-engine and 19 Chromium UI tests; IPA-gold schema, repository data/evidence audit, external-G2P harness syntax/CLI, locked install, build, generated-data reproducibility/drift and built-page/relative-asset checks all passed.
- A local-path Markdown-link integrity scan over the seven updated Markdown files against the complete 208-entry recursive main tree found **0 missing local targets**. External URLs and every heading-anchor target were not exhaustively crawled.
- GitHub Pages deployment for the PR #157 merge commit succeeded: [#42586199760 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42586199760). The documentation-only refresh does not alter generated browser assets.
- No local checkout, shell commands or local browser run are claimed; verification was hosted GitHub Actions plus the repository-tree link scan above.

### Final status

The repository's documentation hierarchy is coherent and discoverable without a second master plan or directory-wide migration. The latest mainline is engineering-verified and research-ready as a prototype. It is not linguistically release-ready: independent adjudicated IPA gold remains 0, expert linguistic sign-off is absent, and manual accessibility QA remains partial. The lexical list improves optional research diagnostics only; lexical word segmentation remains unsolved.

## Completion-register and glossary synchronization — 2026-11-09

- Commit `114c64bfd4222b0ad19283919d7cacdab7399a85` updates `GLOSSARY.md` with `Orthographic lexical hint` and `SOFT_HINT_ONLY`, and appends the written-evidence/lexical-hint acceptance rows to `docs/audits/current/LINGUISTIC-COMPLETION-REGISTER-2026-11-01.md`.
- Exact-head Verify [#42587148792 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42587148792) on that commit: 298 Python, 147 Node/browser-engine and 19 Chromium UI tests; all configured IPA-gold schema, repository data/evidence, external-G2P harness, locked install, build, generated-data and built-page checks passed.
- The register now distinguishes completed source registration, structural segmentation fixtures and diagnostic-only lexical hints from unresolved lexical word segmentation, the inaccessible MIT CSV, unclassified Kaikki/Wiktionary IPA provenance and independent IPA gold (0).
- This synchronization changes documentation only; no runtime, canonical phonological registry or generated browser asset changed.


## Mainline continuation update — 2026-11-09 (latest)

### LaoNLP dictionary and audit utility

The MIT dictionary body was retrieved from immutable LaoNLP commit a914f64e38ff24d67d32e37db40dad5c368ea602; its file-specific 2015 MIT notice and Git blob SHA-1 ded14c7770becfd5c6946c6c1ce75a7dfc4d564c were verified. The raw CSV is not committed. A filtered 34,937-entry Lao-only derivative is committed at data/lao/lexical-hints/LaoNLP-MIT-LaoWord.txt with the full notice embedded; it is only an optional SOFT_HINT_ONLY source for the diagnostic matcher.

A quote-aware source audit found 51,257 records after the first header: 21 exact repeated headers, 3 malformed header-like rows, 3 ID-only rows, 35,078 distinct non-header LaoWord forms, 11,195 forms occurring multiple times, 36 non-header blank Type values (33 usable records plus 3 ID-only), and 7 blank Pronunciation values (4 usable plus 3 ID-only). The Pronunciation field is Latin romanization, not IPA. The offline script scripts/audit_laonlp_dictionary.py verifies the Git object hash and now distinguishes exact repeated headers from malformed header-like rows; regression tests cover both cases.

### Wiktionary provenance

Four exact raw source revisions invoke the lo-pron template: ກະດານ (66396667), ການແປ (66459544), ຂໍກະແຈ (68829138), and ຝົນ (85069045). The Lua generator is pinned to Module:lo-pron oldid 88555975, the wrapper to Template:lo-pron oldid 79053402, and its documentation to oldid 76254409. For these four examples the IPA is generated, not manually typed. This is sample evidence only; whole-corpus Kaikki provenance remains PARTIAL because extracted sounds records do not preserve source invocation metadata or all dependency revisions.

### Current PR reconciliation

- #156: closed unmerged after selective benchmark port; branch preserved.
- #146: closed unmerged as superseded by updated mainline deterministic-profile code and benchmark evidence; branch preserved.
- #147: closed unmerged as superseded by updated mainline HVULao 1k implementation and exact-mainline run; branch preserved.
- #148: open, stale documentation branch; not merged.
- #145: open, neural-first proposal not adopted; the deterministic hybrid remains the production default.
- #137–#142: open, stacked/diverged; not modified.

### Exact-head verification

Verify #42611861847 — SUCCESS on main SHA 1c0ad1a5ac4455830f87a177b13f6ddbb3d0de31: 316 Python, 147 Node/browser and 19 Chromium tests; all configured schema, repository data/evidence, external harness, locked install, build, generated-data reproducibility and built-page checks passed. Two earlier attempts at the audit utility's new regression test exposed fixture/header-classification errors; both were corrected and this final exact-head run is green.

Readiness remains research-ready engineering prototype, not linguistically release-ready. Independent expert IPA gold remains 0; manual accessibility acceptance remains PARTIAL; contextual lexical segmentation and corpus-wide Wiktionary provenance remain unresolved.


### Documentation branch reconciliation — PR #148

PR #148's seven-file diff was compared against current main. Its README, audit index, validation page, codebase map and handoff were stale snapshots superseded by newer mainline documentation. The one useful upstream UI UX Pro Max commit pin (4f2dbb67e64969a9a30ab00742f2d55d66ddec2b) was selectively ported to AGENTS.md in commit 5666766a71855929a9f179a95c9587249d81de6f. PR #148 was then closed unmerged with an explanation; its branch remains preserved.


### Older PR-stack closeout — #137–#142

The six older stacked PRs were reconciled against current main. Their changed file paths all exist in main. Representative checks found the current MekongPhon grapheme-context diagnostic and tone-rule test files byte-identical to main; benchmark, model-adapter, parser, target and grapheme-preview files are maintained on main in newer forms and covered by the current exact-head suite. Each PR was closed unmerged with an individual explanation; no branch was deleted or rewritten. PR #145 remains open because it proposes a distinct neural-first architecture that has not been adopted.


### Expanded Kaikki source-wikitext sample — 2026-11-09

The Kaikki Lao JSONL contains 2,751 records, 2,378 unique word forms and 2,320 unique forms with IPA. A deterministic 100-form sample (32-bit FNV-1a ordering over Unicode code points) was checked against exact raw Wiktionary source revisions. All 100 pages existed, all 100 selected revisions predate the 2026-10-01 dump date, and all 100 contain a direct lo-pron call. The page/revision manifest is committed in data/evidence/kaikki_lao_ipa_provenance_sample_2026-11-09.csv. This is stronger sample-level evidence, not whole-corpus classification: Kaikki says post-processing may merge additional sources, and the sounds records do not preserve per-value source provenance. The whole-corpus task remains PARTIAL.


## Exact-head and source-provenance closeout — 2026-11-09

- Main: `d6591f2e49ebf84f48c2fc705e33846c30c2e724`.
- Exact-head Verify: [#42614988384 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42614988384): 318 Python, 147 Node/browser and 19 Chromium tests. Configured schema, evidence, external-harness, locked-install, build, generated-data and built-asset checks passed.
- Kaikki source sample: all 100 exact raw Wiktionary revisions were retrieved and compared with the committed manifest. Titles, page IDs, revision IDs, timestamps and source-text character counts match 100/100; all revisions predate the 2026-10-01 extraction dump; all 100 Lao sections directly invoke `{{lo-pron}}`. Three pages also call `lo-pronoun`; one has an additional Khmu-section `{{IPA}}` template, not a Lao pronunciation source. The test now recomputes each code-point FNV-1a sample key.
- Whole-corpus Kaikki provenance remains PARTIAL: the processed JSONL does not retain source origin per sound value and the index documents additional-source merging. No IPA gold claim is made.
- Benchmark schema v5 adds model-weight SHA-256 checks, train/eval lexicon disjointness, word-final coda and vowel-length marker diagnostics, and an explicit warning that the 100 held-out seed-lexicon forms also contributed to validation-sentence generation / checkpoint selection. The paper's 6,039-entry seed-lexicon count differs from the repository split's 6,316 unique forms by 277. Thus this comparison is reproducible and useful diagnostically, but not an independent model-selection-free accuracy estimate.
- Open PRs at this checkpoint: #145 only. Its neural-first proposal remains unmerged because it conflicts with the adopted hybrid-deterministic production route; no approval to change architecture was inferred.
- Readiness remains engineering-verified research prototype, not linguistically release-ready. Independent adjudicated IPA gold remains 0; lexical boundary gold and corpus-wide source provenance are absent; manual accessibility acceptance remains PARTIAL.


## LaoNLP audit precision follow-up — 2026-11-09

A final review found that `audit_laonlp_dictionary.py` correctly skipped malformed-width CSV rows during field-level analysis but did not subtract those rows from `usable_records`. The count now excludes malformed-width rows, and `test_malformed_width_rows_are_excluded_from_usable_count` covers the regression. The first run of the new test exposed a fixture-escaping mistake (literal backslash-n sequences); that fixture was corrected. Exact-head Verify [#42635460479 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42635460479) on `dd0a22857b126a00404350dc59be7bb99ab83334`: 319 Python, 147 Node/browser and 19 Chromium tests passed; all configured schema, repository-data, external-harness, locked-install, build, generated-data and built-page checks passed.

The `lo-pron` source registry now pins its direct and first-level data dependencies as of the 2026-10-01 Kaikki dump cutoff. The transitive closure below `Module:IPA` and `Module:rhymes` remains incomplete, so a fully reproducible Lua execution snapshot is still not claimed.


## Final implementation verification and evidence closeout — 2026-11-09

- Latest verified implementation head: `d6aa703bf0637d65c4a8245ba6cf4d103ae34072`.
- Exact-head Verify [#42635842846 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42635842846): 319 Python, 147 Node/browser-engine and 19 Chromium UI tests; all configured IPA-gold schema, repository evidence, external-G2P harness, locked install, build, generated-data reproducibility and built-page checks passed.
- LaoNLP audit utility: malformed-width rows are now excluded from `usable_records`; a regression test covers this. The first test attempt failed because the fixture used literal escaped newline text; the fixture was corrected and the exact-head suite passed.
- Wiktionary: all 100 exact page revisions and source lengths match the manifest; all 100 Lao sections call `lo-pron`. Direct and first-level dependencies are pinned as of the dump cutoff; the full transitive Lua module closure remains PARTIAL.
- Benchmark v5: pinned model weights and train/eval disjointness are verified, but the 100-word held-out vocabulary was also used for validation-sentence generation/checkpoint selection. The 100-word result is not independent model-selection-free accuracy.
- Current open PR: #145 only; not merged because the neural-first proposal conflicts with the adopted hybrid-deterministic architecture.

## Coverage-quality objective and diagnostic instrumentation — 2026-11-09

The product objective is 100% practical rendering coverage on supported real-world inputs and best-in-class measured transcription quality against competing Lao G2P engines on identical inputs. These must not be conflated: provisional placeholders/passthrough can satisfy a rendering contract but never count as accepted IPA or phonetic accuracy.

The HVULao 1k benchmark has been upgraded to schema 1.4. It now aggregates every syllable withheld from accepted IPA (including withheld syllables inside otherwise partially successful sentences), typed IPA-result status, and parser/phonology uncertainty categories. Aggregates only are retained; source sentences and per-item predictions remain unpersisted. Regression tests cover accepted IPA, provisional/unsupported IPA, passthrough and missing typed results.

- Implementation: scripts/benchmark_hvulao_1k_three_engines.py.
- Tests: tests/test_hvulao_coverage_diagnostics.py.
- Verification on intermediate commit 2434cb946ec54e71a4763ec9c2a8c6a1286ddf2b: Verify #42647429908 SUCCESS; 319 Python tests and 19 Chromium tests passed.
- Benchmark schema 1.4 exact-head run and latest Verify are pending at the time of this audit update. No coverage improvement or quality gain is claimed from diagnostics alone.
- Next acceptance: inspect the aggregate failure distribution, prioritize source-grounded fixes for the largest categories, add regression cases, and rerun the same pinned corpus plus the three-engine identical-item comparisons. Independent IPA gold is still required for an accuracy claim.


## Benchmark diagnostic regression fix — 2026-11-09

The first schema-1.4 HVULao benchmark runs exposed a bookkeeping defect in the new diagnostics: the Vientiane stage initialized `withheld_statuses`, but the MekongPhon-reference and hybrid stage dictionaries did not. Each sentence was fully analyzed and most metrics were computed, but aggregation then raised `KeyError` once per row in those two profiles. This was a benchmark instrumentation failure, not a linguistic-engine exception or a valid comparison result.

The correction centralizes all deterministic stage counters in `new_rule_stage()`, including independent `withheld_statuses` and `withheld` counters, and exports the typed status distribution alongside warning categories. A regression test verifies the fields exist and that profile counters do not leak between instances.

- Fix commit: `3becf3b3859d1223953d426c34f6bd232a0041d6`.
- Counter-factory refactor: `bdbe085a030ec54350077f20bcf9b103bca4f077`.
- Regression test: `60969af2f55d6d83e12bbb0a3d0ec5d37c56119f`.
- Exact-head Verify [#42649144346 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42649144346): 323 Python tests, 147 browser-engine tests, 19 Chromium tests; repository evidence/schema checks, external-G2P syntax/CLI, locked install, build, generated-data reproducibility and built-page checks passed.
- Corrected schema-1.4 HVULao run [#42649110626](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42649110626) was still running when this note was written. The earlier run #42649047666 also remained in progress; neither result is accepted until the benchmark job completes and its zero-runtime-error gate passes.

No engine phonology was changed in this fix. No improvement in IPA coverage or linguistic accuracy is claimed. The prior 34.6% hybrid IPA-complete / 94.21% syllable IPA baseline remains the last accepted benchmark baseline until the corrected run is complete.


## IPA / Ukrainian-target boundary correction and updated comparative evidence — 2026-11-09

The successful schema-1.4 diagnostic run [#42649047666](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42649047666) (commit `3becf3b3859d1223953d426c34f6bd232a0041d6`) completed with **0 runtime errors**. It reported 1,005 provisional hybrid units, including 607 tagged `UKRAINIAN-TARGET-UNMAPPED` and 398 genuinely provisional/unknown IPA hints. This exposed a pipeline defect: `core.analyze()` replaced a supported `PhoneticResult` with an unknown PROVISIONAL result whenever the Ukrainian target adapter lacked a correspondence. That incorrectly made a target-side mapping gap look like source-side phonetic uncertainty and reduced accepted IPA coverage.

The core now preserves the accepted typed source IPA and its provenance, emits a target-only `?` marker when the Ukrainian mapping is absent, and marks the syllable `EVIDENCE LIMITED`. It does not invent a Ukrainian correspondence. Regression test: `ເກີ` retains `/kəː/` with `PhoneticResult.status=SUPPORTED`, while Ukrainian output is `?` and the syllable records `UKRAINIAN-TARGET-UNMAPPED`. The compatibility Vientiane profile continues to withhold uncertain IPA as before; target fallback applies only to the default hybrid.

The schema-1.5 HVULao benchmark now reports target-mapping gaps separately from IPA-withheld statuses. It is running at [#42650543096](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42650543096) on `444ef7c832150ba92119245b05ae9b8f61c795f9`; no updated 1k coverage figures are accepted until that run completes with zero runtime errors and passes the 100% rendering gate.

### New completed 100-word comparison

The exact pinned 100-word MekongPhon held-out run [#42650433708 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42650433708) on `74748de4684ddb02ba8b95db442ec3079e3893db` completed with zero runtime errors. On the same dictionary-seeded reference split:

| Engine | Segmental CER | Segmental coverage | Tonal CER | Tonal coverage |
|---|---:|---:|---:|---:|
| ClippyFirst hybrid | 6.64% | 97% | 29.23% | 91% |
| MekongPhon Neural | 6.64% | 100% | 8.29% | 100% |
| Lao2IPA | 8.97% | 100% | 11.97% | 100% |

ClippyFirst is tied for the lowest segmental CER on this split, but has lower segmental coverage and substantially worse tonal CER/coverage than both external systems. The benchmark also reports a 3.81% tone-category error rate on covered categories, with 83.33% tone-category coverage; this does not negate the tonal IPA CER result. The 100-word vocabulary is dictionary-seeded, not independently adjudicated gold, and contributed to validation-sentence generation/checkpoint selection. These are diagnostic concordance measures, not independent accuracy.

### Verification and current ledger

- Exact-head Verify [#42650543260 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42650543260) on `444ef7c832150ba92119245b05ae9b8f61c795f9`: 324 Python tests, 147 browser-engine tests, 19 Chromium UI tests; all configured evidence/schema, external-G2P syntax/CLI, locked-install, build, generated-data and built-site checks passed.
- The subsequent README refresh records the 100-word comparison and clarifies that a target-side mapping failure does not erase supported source IPA. Exact-head verification of that documentation update is pending.
- Main remains the only work branch; no branch was created, deleted or rewritten. PR #145 remains open and unmerged because its neural-first architecture conflicts with the adopted hybrid deterministic route. Current branch inventory is 22 branches including `main`.
- Independent expert-adjudicated IPA gold: BLOCKED (0 records). Contextual lexical-boundary gold, full Kaikki source provenance, acoustic/prosodic evaluation and manual accessibility QA remain PARTIAL/BLOCKED as recorded above.

**Readiness:** engineering-verified research prototype, not linguistically release-ready. The measured segmental result is competitive on one dictionary-seeded split; tonal quality and full coverage still trail competitors, and no independent gold establishes phonetic accuracy.


## Non-blocking low-confidence output and schema 6.0 — 2026-11-09

Owner requirement clarified: 97% segmental / 91% tonal must not be presented as output coverage. Low-confidence results must remain visible, with uncertainty marked. The 100-word benchmark now separates output coverage from confidence coverage and includes explicit provisional/unknown output in full-set CER scoring.

- The hybrid target adapter now returns an explicit target-side ? whenever a typed IPA/provisional sequence cannot be fully adapted. It never suppresses a valid source unit merely because target mapping is unavailable; source IPA and confidence metadata remain intact.
- Benchmark helper renderable_segmental_ipa() emits accepted IPA, provisional grapheme hints and explicit ? unknown positions. renderable_tonal_ipa() emits the contour or a ? marker. render_mekong_tonal() no longer returns an empty result for unresolved tone categories; it renders an explicit ?.
- Schema 6.0 100-word run [#42654328706 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42654328706) verifies 100/100 inputs and 169/169 syllable units with segmental and tonal outputs. Confidence remains separately measured at 97/100 inputs for accepted segmental IPA and 91/100 for accepted tone contours; 160/169 syllables have a tone contour, and the rest are explicitly marked unknown rather than omitted.

| Engine | Segmental CER | Segmental output coverage | Tonal CER | Tonal output coverage |
|---|---:|---:|---:|---:|
| ClippyFirst hybrid | 6.15% | 100% | 22.90% native / 11.39% Mekong convention | 100% |
| MekongPhon Neural | 6.64% | 100% | 8.29% | 100% |
| Lao2IPA | 8.97% | 100% | 11.97% | 100% |

The provisional/unknown markers are included in the full-set CER; they are not treated as correct IPA. ClippyFirst leads this split on segmental CER, but its tonal CER still trails MekongPhon Neural. Mekong-convention tonal CER is slightly better than Lao2IPA. Tone-category error is 3.81% among covered categories (105/126, 83.33% coverage). The dictionary-seeded reference split is not independently re-adjudicated gold; independent project IPA gold remains 0.

Exact-head Verify [#42654358111 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42654358111) on ef58962bd5228ff96acacf8b63c4a6593ca12440 passed 327 Python tests, 147 Node tests and 19 Chromium tests, plus configured build, evidence, data and built-site checks. The subsequent README and benchmark-report documentation updates require exact-head verification.

**Task ledger update:**
- 100% visible output for the 100-word set — DONE_VERIFIED (100/100 inputs, 169/169 units; schema 6.0 artifact).
- Explicit low-confidence/unknown tone output — DONE_VERIFIED (tone output 100%; 160/169 units have contours, missing contours marked ?).
- 100% accepted IPA / tone confidence — not an output gate; remains PARTIAL (97/100 segmental and 91/100 tonal confidence-complete inputs).
- 1,000-row HVULao schema-1.5 post-fallback benchmark — PARTIAL, still running as [#42653641804](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42653641804); prior accepted schema-1.5 run #42650543096 already verified 1,000/1,000 hybrid renderings and 21,534/21,534 analyzed units.

**Readiness:** engineering-verified research prototype. Output coverage is complete on the named 100-word set; segmental concordance is competitive, but tonal quality and independent phonetic validation remain incomplete. No claim of universal-Lao 100% phonetic accuracy is made.


### HVULao schema 1.5 completed — 2026-11-09

The previously pending post-fallback 1k run is now complete: [#42653641804 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42653641804), artifact [#13691297821](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42653641804/artifacts/13691297821). It processed 1,000/1,000 rows with 0 runtime errors. Hybrid visible rendering is 1,000/1,000 inputs and 21,534/21,534 analyzed units (100%). Source IPA completeness is separately 661/1,000 sentences (66.1%) and 97.71% syllable IPA coverage. The hybrid has 16,936 SUPPORTED, 19 UNCERTAIN and 398 PROVISIONAL units; 607 target correspondences are unavailable and now remain visible as target-side ?. These are not source-IPA omissions.

The neural comparator completed IPA for 934/1,000 sentences (93.4%), but 66 inputs were rejected by its source-length/character limits. The HVULao corpus has no IPA gold, so these are completeness and rendering metrics only. The 100-word schema-6 comparison separately confirms 100% segmental/tonal output coverage while keeping confidence rates at 97%/91%.



## Full external-engine benchmark rerun and output-contract closeout — 2026-11-09

- External same-split suite [#42662067748 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42662067748), artifact [#13695780763](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42662067748/artifacts/13695780763).
- LanguageNet Phonetisaurus sub-job SUCCESS, artifact [#13694282552](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42662067748/artifacts/13694282552).
- All seven same-split engines (ClippyFirst, MekongPhon Neural, Lao2IPA, Epitran, orthography2ipa, Transphone, Phonetisaurus) produced 100/100 outputs. External comparators now preserve failed/empty results as explicit `?` and separately report `output_coverage` vs `engine_success_coverage`; unexpected runtime errors still fail the workflow. No unknown fallback was required in this successful run.
- Segmental CER leadership on this 100-word split: ClippyFirst 6.15% (90/100 exact), MekongPhon Neural 6.64% (82/100), Lao2IPA 8.97%, Epitran 10.96%, orthography2ipa 19.60%, Transphone 24.25%, Phonetisaurus 78.90%.
- Tonal CER leadership remains MekongPhon Neural 8.29% (74/100 exact); Lao2IPA 11.97%; ClippyFirst 22.90% native contour / 11.39% under the evaluation-only Mekong contour convention (25/100 native exact, 69/100 convention exact); Epitran 36.94%, orthography2ipa 37.51%, Transphone 46.49%. Phonetisaurus has no tonal model.
- Exact-head Verify on the code/test changes [#42662095956 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42662095956), commit `ccc0209b27298b82a898269e5063a20c66c4b3e3`. Documentation-only continuation commit follows and requires its own exact-head Verify.
- Existing independent 1k HVULao coverage result remains 100% rendering. FLORES+, HPLT Lao, FLEURS and Common Voice remain TODO/BLOCKED pending immutable extraction, license/provenance validation and dedicated coverage-only harnesses; none is claimed passed.
- Readiness remains research prototype: 100% visible output on tested sets is verified, segmental concordance is competitive on one dictionary-seeded split, tonal concordance trails MekongPhon Neural, and project-adjudicated independent IPA gold remains absent.


## Hybrid v2 implementation continuation — 2026-11-09

- Starting main head: `da4940cea6d1470faf89026d737b03c90a6e2ca0`.
- Added opt-in `hybrid-v2`: deterministic hybrid remains the source of segmental IPA and Ukrainian rendering; pinned MekongPhon tonal output is used only for tone contours after clean IPA parsing and exact syllable-count alignment.
- Added explicit mapping for the five MekongPhon contours to tone categories, preserving neural model revision, raw output, provenance, and disagreement notes. Unknown/unsupported contours, unresolved minor syllables, and count mismatches are withheld.
- Added tests for one-/two-syllable alignment, segmental/target invariance, malformed IPA, unknown contours, count mismatch, and no input mutation.
- Status before CI: implementation PARTIAL; exact-head Verify and same-split benchmark pending. Not promoted to default or browser UI.


### Hybrid v2 alignment correction

The first schema-7.0 run exposed that MekongPhon often emits multi-syllable IPA without explicit dot delimiters. The original parser-boundary gate therefore withheld tones on 51/100 words and scored worse than the deterministic baseline (tonal CER 19.91%, 46/100 exact versus 11.39%, 69/100 for the baseline's Mekong-convention contours). The v2 aligner now extracts the ordered tone-symbol stream and accepts it only when there is exactly one decomposition into registered MekongPhon contours matching the deterministic syllable count. Multiple/no decompositions remain withheld. This is order-based syllable alignment, not an acoustic or expert-adjudicated boundary claim. New same-split benchmark pending.


## Hybrid v2 dual-lane correction — 2026-11-09

The order-aligned synthetic-string benchmark was still worse than the original hybrid (14.96% tonal CER, 62/100 exact versus 11.39%, 69/100). The reason is that tone-symbol order can be associated with syllables, but neural tone placement relative to segmental phones is not recoverable from that count alone. Hybrid v2 has therefore been corrected to preserve two separate lanes: ClippyFirst segmental IPA/Ukrainian output and untouched MekongPhon full tonal IPA. Unique contour decomposition is used only for optional per-syllable metadata, explicitly UNCERTAIN; no artificial merged IPA is generated. The new same-split benchmark reports the best measured per-field results independently.


## Hybrid v2 fallback gate — 2026-11-09

Expected model/dependency/128-token-limit failures now return the deterministic Ukrainian output with explicit `NEURAL_UNAVAILABLE` status and warning; they do not silently fall back or fabricate tone. Invalid input is rejected separately. A regression test mocks the model length-limit error and verifies the deterministic target output remains available.


### Hybrid v2 same-split results — 2026-11-09

The dual-lane v2 benchmark completed successfully on the pinned MekongPhon 100-word split: [Verify #42673479442 SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42673479442) and [benchmark #42673479457 SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42673479457), aggregate artifact [#13698843728](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42673479457/artifacts/13698843728). Benchmark code commit: `dd425ae5458ed1ed840fd7eaa13c373e80073cfa`.

| Hybrid v2 lane | CER | Exact | Coverage |
|---|---:|---:|---:|
| Segmental IPA — ClippyFirst hybrid | **6.15%** | **90/100** | 100/100 |
| Tonal IPA — untouched MekongPhon Neural output | **8.29%** | **74/100** | 100/100 |
| Ukrainian rendering — deterministic IPA adapter | n/a | n/a | **100/100 inputs; 169/169 units** |

The previous deterministic hybrid's Mekong-convention tonal CER was 11.39% (69/100 exact), so v2 improves the selected tonal lane while preserving the best segmental lane. The model's full tonal IPA remains separate; no artificial segmental+tone string is synthesized. Ordered tone contours could be associated with 112/169 syllable units (66.27%); those per-syllable predictions remain UNCERTAIN. Accepted project-adjudicated tonal confidence is 0 because the project has no independent tone gold. Runtime errors: 0. The dictionary-seeded 100-word benchmark is not independent expert gold and must not be described as whole-language accuracy.

**Task ledger:** same-split dual-lane comparison DONE_VERIFIED; explicit neural-unavailable fallback regression test DONE_VERIFIED; 1k sentence-domain v2 stress benchmark TODO (existing HVULao 1k results apply to the prior deterministic hybrid and neural comparator, not v2); browser integration DEFERRED pending a separately deployed inference backend. Hybrid v2 remains opt-in and does not replace the browser/default engine.
