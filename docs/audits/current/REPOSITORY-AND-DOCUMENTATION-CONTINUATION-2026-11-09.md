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
| `GRAPHEME-RECOGNITION-001` | DONE_VERIFIED when exact-head Verify succeeds | Python and browser tests iterate all 83 inventory entries; require a typed role or explicit passthrough. |
| `GLIDE-VOWEL-COVERAGE-001` | DONE_VERIFIED when exact-head Verify succeeds | Six new source-backed forms have shared fixtures and Python/browser tests; registry IDs and parser structures are checked. |
| `LAO-ELLIPSIS-PASSTHROUGH-001` | DONE_VERIFIED when exact-head Verify succeeds | Python/browser tests assert punctuation is preserved, not treated as phonetic material. |
| `REPETITION-MARK-EXPANSION-001` | DEFERRED | Requires word/phrase scope resolution; current engine does not claim lexical word segmentation. Acceptance: preserve meaning of U+0EC6 by repeating the correctly scoped Ukrainian unit, with mixed-phrase regressions. |
| `PALI-PRONUNCIATION-PROFILE-001` | DEFERRED | Outside contemporary Lao profile; requires Pali phonological rules, orthographic conventions and independent review. |
| `KHMu-PRONUNCIATION-PROFILE-001` | DEFERRED | Khmu is a distinct language; requires a separate language profile and evidence. |
| Independent expert IPA gold | BLOCKED | No adjudicated records; requires rights-cleared audio/text and qualified independent annotation/adjudication. |

### Verification history and current head

- Earlier Verify runs failed while the new browser matcher and test controls were being reconciled. Those failures were investigated; they are not presented as passes.
- The final exact-head Verify result must be recorded below after it completes; no test result is inferred from an in-progress run.
- Local shell tests were not run in this connector-only session. All claimed verification must cite the exact GitHub Actions run and SHA.
