## Documentation closeout audit checkpoint — 2026-11-17

- Latest fully verified main before this final status-only documentation sync: `7b480dc22c82d21d57eff63513aac336cd42b087`; exact-main Verify #4649 / [run 44088320092 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/44088320092). Test totals: 359 Python, 205 browser-engine, 30 Chromium UI; all configured schema/evidence, external-G2P, build, reproducibility and built-page checks passed.
- PR #253 merged by squash as `fc61f5413ad26cfd95ad774b00fb80a3853d2d2a`; exact PR Verify #4640 / run 44087573689 and post-merge Verify #4641 / run 44087819259 both passed. Pages Deploy #107 / run 44087819410 succeeded on the merge commit.
- Current LOC evidence and Note 10 parser guard are described in the preceding checkpoint. The source-role derivation remains blocked; no runtime phonological mapping or IPA gold was added.
## Latest mainline audit checkpoint — PR #253 merged (2026-11-17)

- PR [#253](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/253) merged by squash as `fc61f5413ad26cfd95ad774b00fb80a3853d2d2a`; starting main was `aae9a7f2eb688932dc8d3bede390a1f7e4185a0e`.
- Exact PR-head Verify #4640 / [run 44087573689 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/44087573689) on `027e850247ce52b8e76af2629fa493bab8784437`; exact post-merge main Verify #4641 / [run 44087819259 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/44087819259) on the merge commit.
- Exact-head test totals: 359 Python, 205 browser-engine, 30 Chromium UI; IPA-gold schema, repository/data/evidence audit, external-G2P syntax/CLI, build, canonical data generation, generated-data reproducibility and built-page/relative-asset checks all passed.
- LOC evidence: preferred 2012 Word source gives `ຄຼິສຕຽນ (khitsatīan)`; published 2012 PDF conflicts with `ຫຼັກສາດ (khitsatān)`. LOC says to use Word rather than PDF when copying data. The 1997 PDF text layer yields romanized `khitsatian`, but not a reliable Lao-script form.
- Runtime regression confirms `analyze("ຄຼິສຕຽນ")` remains one unresolved token with no IPA/Ukrainian guess. This is a fail-closed negative test, not automatic source segmentation. Manual source roles in the Latin crosswalk remain; automatic Note 10 source-role derivation is PARTIAL/BLOCKED.
- Registry: 83 unique sources / 109 unique claims; no duplicate IDs, malformed CSV rows or missing claim-source references. No runtime phonological mapping, IPA gold, model, corpus, dictionary or generated data changed.
## Mainline audit correction — LOC 2012 Word/PDF Note 10 discrepancy (2026-11-17)

- Starting main for this continuation: `aae9a7f2eb688932dc8d3bede390a1f7e4185a0e` (PR #251 and documentation closeout PR #252 merged). Exact-main Verify #4611 / run 44086036717 succeeded on PR #251 merge commit `8945c94f3a0a6f44f6bdfb6cbad7bdcf99c9402d`; subsequent main Verify #4615 / run 44086592131 succeeded on `aae9a7f2eb688932dc8d3bede390a1f7e4185a0e`.
- The preferred official LOC 2012 Word source gives `ຄຼິສຕຽນ (khitsatīan)` in Notes 3 and 10. The published 2012 PDF gives a conflicting Note 3/10 example `ຫຼັກສາດ (khitsatān)`. LOC's source-document index explicitly says to use Word rather than PDF when copying table data; preserve the conflict in the evidence registry rather than treating the examples as equivalent.
- The historical 1997 PDF text extraction exposes romanized `khitsatian`, but its Lao glyphs are corrupted; no exact 1997 Lao-script spelling is asserted.
- Added claim `CLM-LAO-ALA-LC-NOTE10-PDF-WORD-DISCREPANCY`, updated both source rows and the preferred-source claims. Registry integrity after the update: 83 unique sources / 109 unique claims, no duplicate IDs or missing source references.
- Added a negative runtime regression for exact Word-source Lao input `ຄຼິສຕຽນ`: current Vientiane parser must withhold the whole token as unresolved, without IPA/Ukrainian guessing. This is a fail-closed guard, not a successful source parser. The Latin romanization crosswalk still supplies the `ສ` coda/onset roles manually.
- Automatic orthographic syllabification and overlapping coda/onset role derivation remain PARTIAL/BLOCKED pending reviewed source syllable spans, further positive/negative examples and Lao-specialist adjudication. No runtime phonological mapping, IPA gold, corpus, dictionary, model or generated artifact is added.
## Mainline audit continuation — LOC Note 10 Word source inspected (2026-11-17)

- Current main at start of this continuation: 72a555df57386051321f0f7707923ae61305beed (PR #249 merged as 825d7bf91d756c7abda884e2348a8fdfd82ec31f; PR #250 docs closeout merged as 72a555df57386051321f0f7707923ae61305beed). Exact-main Verify #4562 / run 44083809194 passed on 72a555df57386051321f0f7707923ae61305beed.
- Official source document index: https://www.loc.gov/catdir/cpso/romansource.html; Lao Word source: https://www.loc.gov/catdir/cpso/romanization/lao.doc. Retrieved successfully as HTTP 200 / application/msword and inspected through content-aware document extraction.
- Exact Note 3 and Note 10 example: ຄຼິສຕຽນ (khitsatīan). The published 2012 PDF conflicts with the preferred Word source, giving ຫຼັກສາດ (khitsatān); LOC instructs users to copy from Word rather than PDF. The 1997 PDF text layer exposes romanized khitsatian but its Lao glyphs are corrupted, so no exact historical Lao-script form is asserted. Note 3 identifies ຼ as the combining form of ລ and says it is not romanized here. Note 10 repeats the example and double-function rule; Note 1 supplies ສ = s initially and ສ = (t) as a final loanword value, explaining the t+s sequence.
- Corrected positive/negative romanization crosswalk fixtures from khitsatān / AA to khitsatīan / IA_LONG. Explicit ສ coda/onset roles remain manually supplied. The browser case ຄິຼສຕຽນ is still only Latin-mode separation and is not the exact LOC example ຄຼິສຕຽນ.
- Status: exact source example DONE_VERIFIED; supplied-role crosswalk DONE_VERIFIED as engineering only; automatic Lao source-role derivation and full Note 10 conformance remain PARTIAL/BLOCKED. Verify #4584 / run 44084533002 passed on exact head 536a3c69de6b2455c172c70daa6b427b9790c4da (359 Python, 204 browser-engine, 30 Chromium UI and all configured gates). No runtime, IPA or pronunciation rule inferred.
- New source registry entry: SRC-ALA-LC-LAO-2012-WORD. Updated CLM-LAO-ALA-LC-NOTE10-EXAMPLE and CLM-ALA-LC-SOURCE-DOC-PREFERRED. Exact-head CI is required for this follow-up branch.
## Current main and preserved branch review — PR #246 (2026-11-16)

- Current `main`: `390302db31b56f5842696c2d81a817689635472b`; PR #246 merged from tested head `9570180b100e06538251f96504223deaa06057fd`.
- PR #246 exact-head Verify #4439 / [run 43933464076 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43933464076); post-merge main Verify #4440 / [run 43933702934 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43933702934). Both passed 355 Python, 204 Node and 30 Chromium tests and all configured schema/audit/G2P/build/reproducibility gates.
- PR #246 is documentation/evidence-only; Pages #106 remains the current runtime deployment. No Pages deployment is expected.
- Branch inventory is 114 refs across two API pages. PR #247 is the current documentation/evidence correction; PR #145 is the only other open PR. PR #145 remains divergent, 24 ahead / 374 behind, 13 files; leave untouched pending owner-level architecture decision.
- Preserved test branches were compared against current main:
  - `test/ala-lc-note10-automatic-source-boundary-20261116`: 5 ahead / 16 behind; its only browser test still checks Lao-script rejection in Latin mode with `ຄິຼສຕຽນ`. It does not test automatic Note 10 source-role derivation and is not ported.
  - `test/ala-lc-notes6-10-source-crosswalk-20261116`: 13 ahead / 19 behind; the engine file is byte-identical to main, and its two manual double-function fixtures already exist on main in clarified synthetic form. No code port required.
  - `test/ala-lc-notes5-7-regressions-20261116`: 5 ahead / 22 behind; all added regression test names already exist on main. No port required.
  - `test/ala-lc-note4-context-regressions-20261116`: 6 ahead / 24 behind; all added regression test names already exist on main. No port required.
  - `fix/source-aware-hyphen-regression-20261115`: 8 ahead / 32 behind; contains a separate stale engine/test delta based before Note 8 and needs targeted review before any port. Preserved.
  - `research/revalidate-lao-audio-corpus-leads-20261115`: 6 ahead / 43 behind; its LDC Babel source-row simplification is superseded by the more detailed current-main source and playbook licensing caveats, so no branch content is ported.
  - `improve/rule-engine-error-analysis-20261107`: 294 ahead / 376 behind, large divergent history; no whole-branch merge or cherry-pick without commit-level reconciliation.
  - `fix/romanization-unsupported-vowel-diagnostics-20261115`: 4 ahead / 27 behind; added test names are already present on main, while the branch engine predates the current initial-ayn fail-closed handling. No port.
  - `test/source-aware-lao-hyphen-regressions-20261115`: 4 ahead / 32 behind; added regression test names are already present on main. No port.
  - `quality/ukrainian-editorial-and-design-audit-2026-11-10`: 21 ahead / 75 behind; its older UI snapshot removes current direct-romanization input and Note 8 UI paths. Preserve only as history; do not port.
  - `quality/ukrainian-editorial-audit-2026-11-10`: 72 ahead / 75 behind; likewise removes current direct-romanization input and Note 8 paths, with no unique test value over current main. No port.
  - `research/written-evidence-phonology-2026-11-09`: 0 ahead / 280 behind; no unmerged commits to port.
- No user branch was deleted, force-updated, or merged wholesale.

## Post-merge state — PR #245 and Pages #106 (2026-11-16)

- Main at PR #246 base: `8e8622b007452c20f68dfbfed1edcb709d6bdc41`; PR #245 merged by squash from tested head `199787c9e5a41071134188b01523cd25c26e2ada`.
- Exact-head Verify #4427 / [run 43932311368 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43932311368) and post-merge main Verify #4428 / [run 43932522643 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43932522643) passed 355 Python, 204 Node and 30 Chromium tests plus IPA-gold schema, repository/evidence audit, external-G2P syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks.
- Pages Deploy #106 / [run 43932522626 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43932522626) deployed current main and passed the post-deploy HTTP smoke tests. PR #245 changed research tooling/tests/docs, not production runtime logic.
- Branch search returned 113 refs (112 non-main plus main), including `research/icu-lao-wordbreak-baseline-20261116` and `docs/post-pr245-mainline-reconciliation-20261116`. No user branch was deleted or force-updated. The pre-PR #245 research branch is preserved.
- Only PR #145 was open before this post-merge reconciliation. It remains divergent, 24 ahead / 373 behind at the PR #246 base, 13 changed files; leave untouched pending owner-level neural-first architecture decision.

## Additional research and evidence correction — PR #245 (2026-11-16)

- PR #245 merged by squash as `8e8622b007452c20f68dfbfed1edcb709d6bdc41` from `research/icu-lao-wordbreak-baseline-20261116`; it adds the offline ICU/HVULao boundary baseline, source hashes, evidence records and regression tests. No production code, corpus text or dictionary data is imported.
- This PR also corrects an earlier Note 10 attribution: `ຄິຼສຕຽນ` was not the LOC example. The browser test is only a Latin-mode separation guard. LOC 2012 Note 10 gives the romanized example `khitsatān`; its exact Lao glyph sequence remains unresolved because the available PDF text extraction returns `ຂິດສະຕານ` but the rendered glyphs were not confidently read, and LOC's preferred Word source remains unavailable. The earlier attribution of `ຄິດສະຖານ` to LOC 1997 is withdrawn; that file's example glyphs were not inspected. Unit crosswalk tests use `khitsatān` with manually supplied roles and do not claim automatic source segmentation.
- The repository remains PARTIAL / BLOCKED for Note 9 and Note 10 automatic source roles; no linguistic rule was inferred from the exploratory baseline or the corrected fixture.

## Live repository state — PR #244 merged; ICU Note 9 research branch (2026-11-16)

- Current `main`: `515f95a7927b20ed9e1859660362eb3a6b1c3306`; PR [#244](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/244) merged by squash after PR #243.
- PR #244 exact-head Verify #4393 / [run 43930653255 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43930653255) and post-merge main Verify #4394 / [run 43930806933 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43930806933) passed 350 Python, 204 Node and 30 Chromium tests plus IPA-gold schema, repository/evidence audit, external-G2P syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks.
- Pages Deploy #105 / [run 43918258738 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43918258738) deployed runtime commit `841826ce9981b1c09aa98179c790c63db1b2c982` (PR #241) and passed post-deploy HTTP smoke tests. PRs #243–#244 were documentation/evidence-only; no new Pages deployment was required.
- New research branch: `research/icu-lao-wordbreak-baseline-20261116`. It adds an offline, source-hash-pinned longest/shortest prefix baseline and unit tests; no runtime code or external corpus/dictionary data is imported.
- Paginated branch search returned 112 refs (111 non-main plus `main`) including this research branch. No user branch was deleted or force-updated. The older `docs/reconcile-live-main-pages-20261116` branch was based on the pre-PR #243 main and is superseded; it is preserved but not proposed for merge.
- PR #145 remains the only previously open PR: divergent, 24 ahead / 372 behind current main, 13 changed files. Leave untouched pending the owner-level neural-first architecture decision.
- The current research PR is documentation/evidence/tooling-only and does not change deployed paths; Pages #105 remains the runtime deployment.

## Post-merge reconciliation — PR #243 (2026-11-16)

- Current `main`: `fccff4bae4a4bbc0c7a4d2d9837a874ed72059bd`; PR [#243](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/243) merged by squash from exact tested head `6c6d54077361014f8c31d1875cbb8967c5c447bd`.
- Exact-head Verify #4391 / [run 43930231174 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43930231174) passed 350 Python, 204 Node and 30 Chromium tests plus IPA-gold schema, repository/evidence audit, external-G2P syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks.
- PR #243 changed documentation and evidence registries only; no runtime code or deployed assets changed. Pages #104 remains the latest runtime deployment.
- Paginated branch search after PR #243 and creation of this reconciliation branch returned 111 refs (110 non-main plus main). All historical/user branches were preserved; no branch was deleted or force-updated.
- Open PR #145 remains the only pre-existing open PR; it is divergent 24 commits ahead / 371 behind current main with 13 changed files. Leave untouched pending the owner-level neural-first architecture decision.
- The post-merge push-triggered main Verify run was not independently retrievable through the available GitHub integration; exact PR-head Verify passed. Do not claim a post-merge run was confirmed.
- Open research issues #99 (independent IPA gold pilot) and #9 (external G2P baseline) remain unresolved; no annotators have been recruited and no independent IPA gold examples exist.

## Post-merge reconciliation — PR #241 (2026-11-16)

- Current `main`: `841826ce9981b1c09aa98179c790c63db1b2c982`; PR #241 merged by squash from exact tested head `f4be105e4c7383214f22a96f5598ddb7a81a8617`.
- Exact-head Verify #4383 / [run 43918104933 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43918104933) passed 350 Python, 204 Node and 30 Chromium tests plus IPA-gold schema, repository/evidence audit, external-G2P syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks.
- Paginated branch search returned 108 refs (107 non-main plus main); the implementation and reconciliation branches are preserved. No user branches were deleted or force-updated.
- PR #242 is the current documentation-only post-merge reconciliation. The only other open PR is #145, divergent 24 ahead / 369 behind current main with 13 changed files; leave it untouched pending owner-level neural-first architecture decision.
- Pages workflow is configured to deploy on main changes to `index.html`, `web/**` and `tests/browser/**`; this merge touched those paths. Pages #104 is still the latest deployment confirmed in repository evidence. A newer deployment and post-merge main Verify result are not yet independently confirmed here.

## Live reconciliation — PR #240 and Note 8 work branch (2026-11-16)

- Current `main` at the start of the Note 8 task: `c8ef2d8725b9e595bab2f2c4ea369517720590a8`, PR #240 merged.
- PR #240 exact-head Verify #4343 passed; the tested PR head and merge commit had identical Git tree SHA. It was documentation-only; Pages #104 remains the latest runtime deployment.
- Current paginated branch search returned 107 refs (106 non-main plus main). No existing branch was deleted or force-updated.
- Open PRs: #145 (neural-first architecture proposal; owner decision) and #241 (ALA-LC Note 8 numeral route; active implementation).
- PR #145 remains divergent: 24 ahead / 368 behind current main, 13 changed files. Leave untouched.
- PR #241 is based on current main in `feat/ala-lc-note8-lao-digit-route-20261116`; it adds a narrowly scoped numeral-only ALA-LC Note 8 route and service output. Exact-head Verify #4376 / [run 43917776932 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43917776932) passed 350 Python, 204 Node and 30 Chromium tests plus configured audits/build/reproducibility gates. Merge and post-merge verification remain.

## Live reconciliation — PR #239 and branch inventory (2026-11-16)

- Current `main`: `d1b3a7a3418aca83a6cb56a291007dcb0a36479c`; PR [#239](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/239) is merged and documentation-only.
- Exact-head Verify #4341 / [run 43870653366 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43870653366) and post-merge main Verify #4342 / [run 43870840263 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43870840263): 350 Python, 201 Node and 29 Chromium tests passed, with repository/evidence audit, IPA-gold schema, external-G2P syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks.
- A fresh paginated GitHub branch search returned 105 refs (104 non-main plus `main`). This supersedes the 102-ref inventory recorded in the PR #237 checkpoint; no branch was deleted or force-updated.
- Fresh comparison `main...feat/mekongphon-first-stage`: 24 commits ahead / 367 behind, divergent, 13 changed files. The neural-first proposal remains an owner-level architecture decision; do not merge or rebase it without approval.
- Pages #104 remains the latest runtime deployment at `e6b1d564a20b88945dc0277b8db38efcd5834c8e`; PR #239 did not change runtime code or generated assets.

**Readiness remains:** engineering-verified partial research prototype, not a linguistically validated or release-ready universal converter. The linguistic and human-QA blockers in the completion register remain open.

---

# Repository structure and branch-consolidation audit — 2026-11-15

## Executive result

The repository already has a coherent documentation architecture. This review does not introduce a second plan, duplicate source registry, copied skill framework, or new runtime dependency. The existing canonical structure is retained and made easier to navigate through this current audit and refreshed entry-point links.

**Starting main:** `4197d4212a935ee59216b1a7f9bdd112dceabb6e`  
**Working branch:** `chore/repository-structure-branch-consolidation-20261115`  
**Base:** `main`  
**Repository:** [ClippyFirst/Lao-Ukrainian-Phonetic-System](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System)

## Repository structure: assessed state

The repository already separates concerns at appropriate boundaries:

| Area | Canonical location | Responsibility |
|---|---|---|
| Public entry point | `README.md` | Overview, quick start, deployment and readiness |
| Agent operating contract | `AGENTS.md` | Mandatory invariants and agent workflow |
| Human contribution workflow | `CONTRIBUTING.md` | Setup, tests, review and contribution policy |
| Terms and statuses | `GLOSSARY.md` | Shared terminology and status vocabulary |
| Documentation navigation | `docs/README.md` | Task-oriented documentation index |
| Structure and placement policy | `docs/REPOSITORY-STRUCTURE.md` | File ownership, precedence and maintenance rules |
| Normative product behavior | `docs/PRODUCT-REQUIREMENTS.md`, `docs/system-specification.md` | Observable requirements and processing contract |
| Linguistic method and provenance | `docs/methodology.md`, `docs/sources-and-evidence.md`, `data/evidence/` | Evidence scope, claims, rights and provenance |
| Canonical Lao data | `data/lao/*.csv` | Authoritative phonological registries |
| Machine contracts | `schemas/` | Versioned typed interfaces |
| Runtime implementation | `src/lao_ukrainian/`, `web/` | Python and browser implementations |
| Verification | `tests/`, `scripts/`, `.github/workflows/` | Regression, audits, build, CI and deployment |
| Current execution ledger | `docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md` | Single chronological task and handoff record |
| Current audits | `docs/audits/current/` | Dated status and evidence snapshots |
| Research artifacts | `docs/research/`, `data/benchmark/` | Reproducible experiments and bounded conclusions |

### Structural decision

**Keep the current architecture.** Do not add a parallel `skills/`, `agents/`, `commands/`, `plugins/` or duplicated `research-data/` hierarchy merely to resemble the reference repositories. The transferable practices from Unlazy, UI/UX Pro Max, Superpowers, Matt Pocock's skills and Ponytail are already distilled into project-owned instructions and standards. The upstream repositories remain methodology references, not runtime dependencies or content to vendor wholesale.

The existing `docs/REPOSITORY-STRUCTURE.md` remains the canonical placement/maintenance guide. This audit is a dated consolidation checkpoint, not a replacement architecture specification.

## Branch inventory and consolidation decision

At inspection, GitHub returned **37 branch refs including `main`** (36 non-main refs). The current default branch was confirmed as `main`, and its head was confirmed by comparing it with the newest repository commit found:

- `main` = `4197d4212a935ee59216b1a7f9bdd112dceabb6e`
- `main` and that commit compare as **identical**.
- All 36 non-main branch names were inventoried and compared with `main`.
- No non-main branch was a simple ahead-only fast-forward candidate: the comparisons returned divergent histories or branches already behind `main`. Many old branches are hundreds of commits behind and contain large historical deltas because their work predates later integration/squash merges.

A mass merge would therefore be unsafe and would reintroduce stale snapshots, duplicated commits, superseded designs, and incompatible experimental defaults. **No branch was force-updated or deleted.** Historical refs are preserved as evidence; `main` remains the sole integration line, and this documentation consolidation uses one task branch based directly on current `main`.

### Recent branch/PR reconciliation

| Workstream | Mainline disposition | Decision |
|---|---|---|
| Public site redesign and copy | PRs #163 and #168 merged; Woven Editorial and Ukrainian copy are on `main` | Preserve; do not replay old design/copy branches |
| Ukrainian editorial and empty input | PRs #169 and #170 merged | Preserve; branch refs are historical |
| Typed MekongPhon IPA API and codebase map | PRs #165 and #167 merged | Preserve typed IPA boundary and current API documentation |
| Research CLI line-break correction | PR #164 merged; PR #166 closed unmerged as duplicate | Do not replay duplicate |
| Neural-first CLI/default proposal | PR #145 remains open and conflicts with the deterministic-default contract | Leave open and unmerged; evaluate as a separate owner-level architecture decision |
| Older hybrid, grapheme fallback, benchmarking, and audit PR stacks | Later integrated work and current mainline documentation supersede earlier branch snapshots; closed-unmerged historical PRs remain available for traceability | Do not bulk-merge; port only a demonstrated missing behavior after file-level review and tests |

The PR inventory also shows historical closed-unmerged work (including earlier prototypes and superseded audit/benchmark attempts). A closed PR is not automatically a missing feature: later merged PRs may have replaced it, and a squash merge does not preserve the source branch's commit ancestry. Reconcile by behavior, files, tests and acceptance criteria—not by ahead/behind commit counts alone.

### Outstanding PR requiring an explicit product decision

[PR #145 — Make MekongPhon Neural the primary Lao-to-IPA stage](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/145) proposes changing the CLI/Python default to neural inference and making Ukrainian adaptation opt-in. The current repository contract keeps the deterministic hybrid as default and neural inference as explicit research/CLI tooling; the static public site remains browser-native and deterministic. Merging #145 without a specification change would create conflicting defaults and claims. **Status: BLOCKED pending an explicit architecture decision and reconciliation of the normative specification, CLI contract, tests and public documentation.** The typed stage-one API itself is already present through merged work and does not require this PR.

## Task ledger

| Task | Status | Evidence / acceptance criterion |
|---|---|---|
| Identify canonical branch and exact starting head | DONE_VERIFIED | Default branch is `main`; current checkpoint SHA is `66a744f43fb31dac1d7869f6e661acc1a8bb5c70` |
| Inventory branch refs | DONE_VERIFIED | Fresh GitHub branch search before the latest continuation branch returned 60 refs including `main` |
| Compare all non-main branch refs with main | DONE_VERIFIED | After PR #194 merged, the 59 non-main refs in the 60-ref inventory were classified as 58 divergent, 2 behind-only, 0 ahead-only, 0 identical. Behind-only: `feature/meta-hybrid-v3-multiengine-20261110`, `research/written-evidence-phonology-2026-11-09`. The former ahead-only `docs/finalize-pr193-current-main-20261115` is now divergent (4 ahead / 1 behind). The new continuation branch `docs/finalize-pr194-current-main-20261115` was created after that inventory and is not included in its count. |
| Reconcile recent merged PRs #163–#170 | DONE_VERIFIED | GitHub merged-PR search confirms #163, #164, #165, #167, #168, #169 and #170 merged; #166 is closed unmerged duplicate |
| Identify open PR conflict | DONE_VERIFIED | Open-PR search identifies #145; proposal conflicts with deterministic-default contract |
| Preserve historical branches and PRs | DONE_VERIFIED | No branch deletion, force update, PR closure or blind merge performed |
| Preserve and clarify documentation architecture | DONE_VERIFIED | Existing structure guide retained; current audit and navigation pointers added |
| Integrate every historical branch's unique file delta | PARTIAL | All 59 non-main refs were classified by commit graph. Three romanization-related historical implementation branches and PR #192 were inspected at file level; their relevant supported changes are already on main. Other historical branch diffs and test behavior are not all independently reviewed. Acceptance: review each potentially unique code/data delta, port only supported requirements, and pass exact-head checks |
| Resolve PR #145 | BLOCKED | Requires explicit architecture decision; deterministic-default system specification currently contradicts proposed default |
| Independent adjudicated Lao IPA gold | BLOCKED | Corpus remains empty (0); acceptance requires rights-cleared, independently annotated and adjudicated examples with provenance |
| Manual physical-device and screen-reader QA | BLOCKED | Requires human review on actual devices and assistive technology |
| Exact-head verification for this documentation-only branch | TODO | GitHub Actions Verify must pass on the final branch head; do not infer success from earlier mainline runs |

## Verification evidence and limits

This audit used GitHub repository metadata, branch search, commit search, PR search, compare-commits, and direct reads of the README, documentation index, repository structure guide, master handoff, current audit, audit index and validation guide.

The newest commit discovered was `4197d4212a935ee59216b1a7f9bdd112dceabb6e`; it compares identical to `main`. The open-PR search performed before creating this consolidation change reported #145 as the only open PR; this audit is now tracked in [PR #171](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/171). Merged-PR search confirms the recent merges listed above; closed-unmerged search exposes historical work that must not be mistaken for currently missing code.

**Not run in this audit:** local clone, Python tests, Node tests, Chromium tests, data audit, build, generated-data drift check, Pages deployment or manual accessibility review. The existing README and handoff contain earlier successful CI evidence for earlier exact commits; that evidence is historical and does not certify this new documentation commit.

## Single-branch operating model

1. `main` is the canonical integration branch.
2. Create one short-lived task branch from the current `main` for each coherent work batch.
3. Do not merge branch refs solely to make the branch list empty.
4. For each candidate branch/PR, establish whether its behavior is already present on `main`; compare actual files and tests when not obvious.
5. Port only a missing, accepted behavior to the current task branch. Do not import an entire stale branch history.
6. Run exact-head CI and update the master handoff/current audit before merging the task branch by PR.
7. Keep historical refs until the repository owner explicitly requests branch cleanup. No refs are deleted by this workflow.

## Final disposition

The repository has a well-formed documentation and engineering structure and a single clear default branch. The correct consolidation is **one active integration line with preserved historical refs**, not a destructive merge of every divergent branch. Engineering readiness and linguistic release readiness remain separate: historical CI proves the checks on its recorded commits, while independent phonetic accuracy remains unmeasured without adjudicated IPA gold.


## Post-audit reconciliation — 2026-11-15

The original audit's PR #171 state was a point-in-time observation. PR #171 subsequently merged as `bd16bf6eef98ac364d4bde8226187ab2c71d7fb9`. The repository's current `main` then advanced through PR #172 (direct romanization input), PR #173 (ALA-LC 2012 conformance correction) and PR #174 (documentation/deployment reconciliation), ending at `ed3afe5e4f090637d0feaa49fbe2d655cea1fc9e`.

The open-PR search on 2026-11-15 returns only PR #145. It remains intentionally unmerged because its neural-first CLI default conflicts with the deterministic-default contract. The exact-main Verify #4084 / run [43698131800](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43698131800) and Pages deployment #96 / run [43697882717](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43697882717) succeeded on the final mainline. The canonical current status is maintained at the top of `docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md`; this file remains a dated audit snapshot.


## Post-audit continuation — PR #178 and current PR #145 reconciliation (2026-11-15)

The canonical branch advanced from `de9c2516d973f2cd721667e5505e86693cff453d` to `034a2db1f912cd3bc0d552678871c73446977e9c` through documentation-only PR [#178](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/178). Exact-head Verify #4097 / run [43712551810](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43712551810) and post-merge Verify #4098 / run [43719400156](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43719400156) both succeeded. No runtime deployment was required; Pages deployment #97 remains the verified runtime deployment from PR #176.

A fresh open-PR inventory still returns only PR #145. Its head `a70769d7005e40e15b68a3df181cadbfa4cce51f` is 24 commits ahead and 310 commits behind current main, with a 13-file diff. File-level comparison confirms the typed stage-one IPA result/API already exists on current main; PR #145's unresolved contract change is neural-first CLI default plus target-adaptation opt-in. The PR's historical exact-head checks #2588/#2589 and benchmark run #42465378241 succeeded on its own old head, but do not make its divergent branch safe to merge. Maintainer comments explicitly defer the change pending a production-architecture decision. Keep the PR open and unmerged; do not rebase/merge the stale branch wholesale.

No branch was deleted or force-updated. Current branch policy remains one canonical `main` integration line with historical refs preserved.


## PR #179 reconciliation — 2026-11-15

PR [#179](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/179) merged as `914575d57ee0ab9366b82704e80b5fd9aa605a64`. Exact-head Verify #4099 / run [43719676086](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43719676086) and post-merge main Verify #4100 / run [43719754394](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43719754394) succeeded. Both are documentation-only changes; Pages deployment #97 remains the latest runtime deployment.

A fresh compare of PR #145 against current `main` reports 24 commits ahead and 310 behind (13 changed files). The typed stage-one IPA API remains present on main; the unresolved delta is the neural-first CLI/Python default and target-adaptation opt-in. The PR remains the only open PR and is intentionally blocked pending an explicit architecture decision. It is not merged, rebased, closed, or otherwise modified.

The canonical handoff was refreshed after this audit checkpoint. Local tests were not run because the previous execution environment could not resolve github.com; the exact-head and post-merge GitHub Actions results above are the available verification evidence.

## Post-merge reconciliation — PR #182 and Pages deployment (2026-11-15)

The previous addendum recorded PR #182 as open while its merge was pending. It has since merged as `72e9677b0dd4fc863c90d4cec773731fb451109a`; this section supersedes that interim state.

- PR [#182](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/182) merged; source branch was `fix/ala-lc-final-crosswalk-current-main-20261115`.
- Exact-head Verify #4128 / [run 43722541781 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43722541781).
- Post-merge main Verify #4131 / [run 43722677303 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43722677303) on merge commit `72e9677b0dd4fc863c90d4cec773731fb451109a`.
- Pages deployment #98 / [run 43722677302 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43722677302). The build job, deployment job and deployed-site smoke test all succeeded; the smoke test fetched both public pages and the required JS/CSS/data assets.
- Verify #4131 passed 350 Python, 188 Node/browser-engine and 28 Chromium tests, plus schema/data audits, external-G2P harness validation, build, generated-data reproducibility and built-page checks.
- PR #181 was closed unmerged as a superseded one-commit-behind attempt. No code was merged from #181.
- A fresh open implementation-PR inventory leaves PR #145, BLOCKED pending an owner-level neural-first CLI/Python architecture decision. Documentation checkpoint PR #184 is the active reconciliation for the README, handoff, audit and romanization matrix; duplicate checkpoint PR #183 is superseded. No rebase or merge of PR #145 was performed.

The new profile-specific ALA-LC source crosswalk is DONE_VERIFIED for the scoped LOC Notes 1, 2 and 4 behavior. Full contextual ALA-LC conformance remains PARTIAL; unsupported initial `ʻ`, medial `w` clusters, other vowel sequences, word/loanword boundaries and specialist review remain outstanding.

**Current main:** `72e9677b0dd4fc863c90d4cec773731fb451109a`.  
**Readiness:** engineering-verified partial research prototype; not a linguistically validated universal converter. Independent adjudicated IPA gold remains 0.

## Final documentation reconciliation — PR #184 (2026-11-15)

The prior addendum described PR #184 as an active documentation checkpoint. It has since merged by squash as `ecc997d356d206640862097d0bff6e7da3c484e3`; this section supersedes the interim state.

- PR [#184](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/184) merged. It updates README, romanization matrix, canonical handoff and current audit only; no runtime code or generated data changed.
- Exact-head Verify #4137 / [run 43722921838 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43722921838).
- Post-merge main Verify #4138 / [run 43723008453 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43723008453) on `ecc997d356d206640862097d0bff6e7da3c484e3`.
- Pages deployment #98 / [run 43722677302 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43722677302) remains the deployed runtime from PR #182; PR #184 was docs-only and required no additional deployment.
- PR #183 was closed unmerged after a file-by-file comparison showed that its matrix change and handoff/audit checkpoint were superseded by the more complete PR #184, which includes verified post-merge and deployment evidence. PRs #185 and #186 were also closed unmerged as duplicate documentation checkpoints after their unique PR #145 divergence and verification details were reconciled; PR #181 was an earlier one-commit-behind attempt. No unique implementation or evidence was lost.
- The only open PR is #145. A fresh compare against main at `ecc997d356d206640862097d0bff6e7da3c484e3` reports 24 commits ahead and 313 behind, with 13 changed files. It remains BLOCKED pending an explicit owner-level decision on the neural-first CLI/Python default; no rebase or merge was performed.

The source-aware ALA-LC crosswalk is DONE_VERIFIED for the scoped LOC Notes 1, 2 and 4 behavior. Full contextual ALA-LC conformance remains PARTIAL. RTGS-for-Lao remains BLOCKED pending a complete Lao-specific adaptation table and reviewed examples. Independent adjudicated IPA gold remains 0 examples.

**Current main at this checkpoint:** `ecc997d356d206640862097d0bff6e7da3c484e3`.  
**Readiness:** engineering-verified partial research prototype, not a linguistically validated universal converter.


## Post-PR #187 current-main reconciliation — 2026-11-15

This addendum corrects the prior snapshot, which still named the PR #184 merge commit as current main even after PR #187 merged.

- Current default branch: `main` at `0b48ab191a9bd6b5a85a104bc8b2aba6e4543c37`.
- PR [#187](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/187) merged at that SHA. It changed only the master handoff and this audit; no runtime code, generated data or Pages deployment changed.
- Exact-head Verify #4145 / [run 43723365644 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43723365644). No separate post-merge Verify run is recorded; do not imply one.
- The last verified runtime deployment remains Pages #98 / [run 43722677302 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43722677302).
- Fresh open-PR search: only PR #145 remains open. Compare `main...feat/mekongphon-first-stage`: 24 commits ahead, 314 behind, 13 changed files; merge base `c0d7218da907dbe0bae6cadb42824ca0cd09b83a`. The typed stage-one IPA API already exists on main; the neural-first CLI/Python default remains an owner-level architecture decision. Leave #145 open and untouched.
- PR #188 is closed unmerged as a superseded documentation checkpoint. Earlier duplicate checkpoint PRs #181, #183, #185 and #186 remain closed unmerged. Historical branches were not deleted or force-updated.
- The scoped LOC Notes 1, 2 and 4 ALA-LC crosswalk remains DONE_VERIFIED. Full contextual ALA-LC conformance and automatic profile detection remain PARTIAL; RTGS and independent IPA gold remain BLOCKED; informal variants remain DEFERRED; physical-device and assistive-technology QA remain BLOCKED.

**Readiness:** engineering-verified partial research prototype, not a linguistically validated universal converter. Independent adjudicated IPA gold remains 0 examples.


## Additional historical-branch source review — 2026-11-15

Three romanization-related branch tips were compared against current `main` and their relevant files inspected:

- `feat/romanization-input-to-ukrainian-20261115`: `web/app.js` and `index.html` are byte-identical to current main; its syllable engine and tests are an older pre-guard/pre-crosswalk version. No unique runtime change remains to port.
- `fix/ala-lc-2012-conformance-20261115`: the engine predates the current LOC-specific ALA-LC source crosswalk and the fail-closed unsupported-vowel guard. Its candidate changes are superseded by current main; porting the branch wholesale would regress current behavior.
- `fix/ala-lc-unsupported-vowel-guard-20261115`: contains an earlier unsupported-sequence guard, but is behind main and lacks the final profile-specific crosswalk. Current main already includes the guard and subsequent fixes.

No branch was modified, deleted, or merged. This targeted review reduces the likely missing-work set but does not satisfy the audit's broader all-historical-branch file-level review; that item remains PARTIAL until all remaining branch deltas are reconciled or explicitly classified.

## PR #189 post-merge checkpoint — 2026-11-15

- PR [#189](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/189) merged by squash as `66a744f43fb31dac1d7869f6e661acc1a8bb5c70`.
- Exact-head Verify #4148 / [run 43724372116 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43724372116).
- Post-merge main Verify #4149 / [run 43724471274 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43724471274).
- Both workflows completed IPA-gold schema validation, repository data/evidence audit, Python tests, external-G2P harness syntax/CLI, locked dependency installation, Node/browser-engine tests, build, generated-data reproducibility, Chromium UI tests and built-page/relative-asset checks.
- PR #189 changed only the canonical handoff and current branch-consolidation audit. No runtime deployment was required.

**Readiness:** engineering-verified partial research prototype, not a linguistically validated universal converter. Independent adjudicated IPA gold remains 0 examples.


## PR #190 post-merge and current-main reconciliation — 2026-11-15

- PR [#190](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/190) merged by squash as `3f42fe0b18c7ccbd8addc316f84e9da6acf61b6a`.
- Exact-head Verify #4152 / [run 43724875673 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43724875673).
- Post-merge main Verify #4153 / [run 43724994459 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43724994459).
- A fresh open-PR search after the merge returns only PR #145. The current compare against `feat/mekongphon-first-stage` is 24 commits ahead / 316 behind / 13 changed files, with merge base `c0d7218da907dbe0bae6cadb42824ca0cd09b83a`.
- PR #190 changed only the canonical handoff and branch audit. No runtime, generated data, deployment workflow or Pages artifact changed. Pages #98 remains the last verified runtime deployment.
- The preserved PR #190 branch compares against current main as 4 commits ahead / 1 behind after the squash merge. No branch deletion or force update was performed.

**Current main:** `3f42fe0b18c7ccbd8addc316f84e9da6acf61b6a`.  
**Readiness:** engineering-verified partial research prototype; not a linguistically validated universal converter. Independent adjudicated IPA gold remains 0 examples.


## PR #192 merged — unknown romanization profile fail-closed validation (2026-11-15)

PR [#192](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/192) merged as `6bca3d2b899ebdffde02e1b4aa2454f3df1dc06e`. The API now rejects unknown explicit profile values rather than silently falling back to BGN/PCGN. Unknown values return `PARTIAL` / `UNSUPPORTED_PROFILE` and preserve the original input visibly; null or omitted profile continues to use automatic detection.

- Exact-head Verify #4163 / [run 43725967264 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43725967264).
- Post-merge main Verify #4164 / [run 43726041995 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43726041995).
- Pages #99 / [run 43726042017 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43726042017).

The change is API validation only; it adds no linguistic mappings or claims of new romanization coverage.


## PR #195 current-main checkpoint — 2026-11-15

- PR [#195](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/195) merged by squash as 7dcc65e594768c64f900586245b9f740bf3feda7.
- Exact-head Verify #4170 / [run 43727259454 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43727259454). Schema/data audit, Python, external-G2P harness, locked npm install, Node/browser-engine, build, generated-data reproducibility, Chromium UI and built-page/asset checks passed.
- PR #195 was documentation-only; no new Pages deployment was required. Last recorded runtime deployment remains Pages #99 / run 43726042017.
- Current main is 7dcc65e594768c64f900586245b9f740bf3feda7.
- Current PR #145 compare: 24 ahead / 321 behind / 13 changed files, merge base c0d7218da907dbe0bae6cadb42824ca0cd09b83a.
- Fresh branch inventory count is 61 refs including main. The earlier 60-ref classification is stale; full new classification remains PARTIAL because the connector call limit prevented all 60 comparisons from completing.
- Unknown explicit romanization profile validation is already DONE_VERIFIED via PR #192; do not duplicate.
- LOC ALA-LC Note 4 ວ alternations and Notes 2–10 remain only partially recoverable from romanization-only text. The direct-input matrix correctly withholds unsupported forms pending Ukrainian target review.

**Readiness:** engineering-verified partial research prototype; not linguistically validated or universal.


## PR #196 and fresh branch comparison — 2026-11-15

- PR [#196](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/196) merged by squash as `cce42c07f8cad67881bc422270b7c5f0f566160b`. It updates only this audit and the canonical handoff; no runtime, generated data, model, mapping or deployment configuration changed.
- Exact-head Verify #4171 / [run 43728217898 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43728217898). The documentation-only PR does not have a separately recorded post-merge main run or new Pages deployment.
- Fresh branch search returns 62 refs: `main` plus 61 historical/task branches. Commit-graph comparisons were refreshed for the current branch set. No branch was an ahead-only fast-forward candidate in the inspected results; divergent and behind-only histories are not safe bulk-merge candidates. Full file-level reconciliation of every historical branch remains PARTIAL; no branch was deleted, force-updated or merged.
- Targeted direct-romanization branch review confirms the older `feat/romanization-input-to-ukrainian-20261115`, `fix/ala-lc-2012-conformance-20261115`, `fix/ala-lc-final-crosswalk-current-main-20261115`, `fix/ala-lc-final-w-crosswalk-20261115` and `fix/ala-lc-unsupported-vowel-guard-20261115` engine/test snapshots are superseded by current main. Their unique older lines either predate fail-closed profile validation, profile-specific ALA-LC crosswalks or the current unsupported-vowel guard. No unique supported runtime change was found to port; wholesale merging would regress behavior.
- Fresh open-PR search still returns only [PR #145](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/145). Current compare: 24 commits ahead / 322 behind / 13 files changed; merge base `c0d7218da907dbe0bae6cadb42824ca0cd09b83a`. GitHub reports the PR non-mergeable. Its neural-first CLI/Python default and target-adaptation opt-in remain an owner-level architecture decision; keep it open and unmerged.
- PR #192 unknown-profile fail-closed behavior remains DONE_VERIFIED and already exists on main; no duplicate patch was introduced.

**Current main:** `cce42c07f8cad67881bc422270b7c5f0f566160b`. **Readiness:** engineering-verified partial research prototype; not linguistically validated or release-ready as a universal converter. Independent adjudicated IPA gold remains 0 examples.


## Fresh inventory after PR #198 — 2026-11-15

- Fresh branch search returns **65 refs including `main`** (64 non-main refs); this supersedes the 62-ref snapshot recorded above. The current count includes the active PR #199 branch and preserved historical branches.
- Open PR search returns [#145](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/145) and [#199](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/199). PR #145 compares at 24 ahead / 324 behind / 13 files, merge base `c0d7218da907dbe0bae6cadb42824ca0cd09b83a`; its neural-first CLI/Python defaults remain an owner-level architecture decision. PR #199 is documentation-only and pending exact-head CI.
- Full comparison of all 64 non-main refs has not been completed in this pass. Overall historical branch reconciliation remains PARTIAL; no branch was deleted or force-updated.


## PR #199 merged — UNGEGN 2025 status and fresh branch checkpoint — 2026-11-15

- PR [#199](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/199) merged by squash as `7ca8d4ec9e421ac3f845b035f1d1c5afd7249a92`.
- Exact-head Verify #4178 / [run 43731179424 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43731179424).
- Post-merge main Verify #4179 / [run 43732731628 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43732731628). Both runs passed IPA-gold structure validation, repository data/evidence audit, Python tests, external-G2P harness syntax/CLI, locked browser dependency installation, browser-engine tests, canonical browser-data build/regeneration, generated-data reproducibility, Chromium UI tests and built-page/relative-asset checks.
- PR #199 records the 2025 UNGEGN WGRS status: Lao's National Geographic Department prepared a draft Lao Romanization System, WGRS reviewed it and made recommendations, and draft toponymy guidelines were being finalised as of July 2024. A possible 2027 submission is not evidence of adoption or UN endorsement. The current BGN/PCGN-derived CLDR profile remains provisional.
- PR #198's DLLM finding remains research-only: collection-specific CrossAsia catalogue convention, not a national standard or generic RTGS profile; published table reuse rights remain undetermined. Neither PR changes runtime mappings, generated data, model assets or deployment behavior.
- Fresh branch search after creating this checkpoint branch: **66 refs including main** (65 non-main). This is a count, not a full file-level reconciliation. Full historical branch review remains PARTIAL; no branch was deleted or force-updated.
- Only open PR is [#145](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/145). Current compare: **24 ahead / 325 behind / 13 changed files**, merge base `c0d7218da907dbe0bae6cadb42824ca0cd09b83a`; GitHub reports non-mergeable. Its neural-first CLI/Python defaults remain an owner-level architecture decision; leave open and unmerged.
- The independent IPA gold corpus remains empty (0 adjudicated examples). RTGS, full contextual ALA-LC, automatic-profile accuracy, specialist linguistic validation and manual device/accessibility QA remain incomplete or blocked.

**Current main:** `7ca8d4ec9e421ac3f845b035f1d1c5afd7249a92`. **Readiness:** engineering-verified partial research prototype; not a linguistically validated universal converter.


## Lao draft chronology and UNGEGN approval-status clarification — 2026-11-15

A targeted primary-source review extends the 2025 update and prevents a category error:

- The WGRS Lao status paper (Version 4.0, September 2013) explicitly states that no Lao romanization system had been approved at UN conferences and that Laos had no national romanization system at that time; it describes BGN/PCGN 1966.
- The UNGEGN status index lists Lao under **Other languages/scripts**, separately from the 30 systems identified as recommended by the United Nations. The Lao entry links to the 2013 status paper; it is not evidence of UN approval.
- WGRS records show a long-running Lao draft: draft instruction awaiting approval (2016); WGRS review and technical recommendations (2018); continuing recommendations and Lao-government consideration (2019 and 2021); draft Toponymic Guidelines in two parts and inter-ministerial feedback (2023); and finalisation of a draft as of July 2024, with hoped-for UNGEGN plenary consideration in 2027 (2025 report).
- The formal UN process requires national development and implementation, WGRS review, UNGEGN plenary endorsement, and ECOSOC adoption. Do not infer UN standard status from an index entry.
- Project consequence: retain BGN/PCGN-derived CLDR as provisional; do not implement the Lao draft until an authoritative current table and evidence of national status are available.

Primary sources: [2013 WGRS Lao status paper](https://unstats.un.org/unsd/ungegn/working_groups/wg5/documents/wgrr4lao.pdf); [2018 WGRS report](https://arhiiv.eki.ee/wgrs/wgr18rep.htm); [2019 WGRS report](https://unstats.un.org/UNSD/geoinfo/UNGEGN/docs/1st-session/GEGN.2_2019_11_CRP.11_WG_Romanization_Systems-full-report.pdf); [2021 WGRS report](https://unstats.un.org/unsd/ungegn/sessions/2nd_session_2021/documents/GEGN.2_2021_93_CRP93_15_WGRSreport.pdf); [2023 WGRS minutes](https://unstats.un.org/unsd/ungegn/working_groups/wg5/documents/WGRS_minutes_3_May_2023.pdf); [2025 WGRS report](https://unstats.un.org/unsd/ungegn/sessions/4th_session_2025/documents/GEGN.2_2025_26_CRP26_item5c.pdf); [UNGEGN index](https://unstats.un.org/unsd/ungegn/romanization/); [UNGEGN approval process](https://unstats.un.org/unsd/ungegn/meetings/Bureau_Divisions/documents/UNGEGN_WGRS_Approval_process-WG_Reviewed_28_May_26.pdf).

**Status:** research clarification DONE_VERIFIED as documentation; the draft's current authoritative table and legal/national adoption status remain BLOCKED pending primary Lao-government evidence.


## PR #200 post-merge verification checkpoint — 2026-11-15

- PR [#200](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/200) merged by squash as `b1d2af1ac0cf2cd848b0967506bc8da13b925d08`.
- Exact-head Verify #4182 / [run 43733010873 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43733010873).
- Post-merge main Verify #4183 / [run 43733109761 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43733109761).
- Both workflows passed corpus schema validation, repository data/evidence audit, Python tests, external-G2P harness syntax/CLI, locked browser dependency installation, browser engine tests, canonical data build and reproducibility, Chromium UI tests, and built-page/relative-asset checks.
- PR #200 was documentation-only and added no runtime or mapping changes.
- Current main at this checkpoint: `b1d2af1ac0cf2cd848b0967506bc8da13b925d08`.
- Only open PR remains #145, non-mergeable; 24 ahead / 326 behind / 13 changed files, merge base `c0d7218da907dbe0bae6cadb42824ca0cd09b83a`. Keep it open pending owner architecture decision.
- Research blockers remain: empty independent IPA gold corpus, specialist review, authoritative current Lao draft and adoption evidence, RTGS-specific table, full contextual ALA-LC, manual accessibility QA and full historical branch file-level reconciliation.

**Readiness:** engineering-verified partial research prototype, not a linguistically validated universal converter.


## PR #201 / current-main and README reconciliation — 2026-11-15

- Starting main: `c9e0e2aab1f5c166def596ab5f500203a4d974f1`; latest exact-main Verify #4185 / [run 43733307259 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43733307259).
- Latest successful Pages deployment remains #99 / [run 43726042017 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43726042017), deployed from `6bca3d2b899ebdffde02e1b4aa2454f3df1dc06e`. PRs #198–#201 were documentation-only; no deployment was triggered or required.
- README's status paragraph previously cited old exact-head/post-merge verification and deployment #98, and did not clearly distinguish current Pages behavior from PR #145's proposed CLI/Python defaults. It is corrected to say the Pages app remains deterministic, report deployment #99 and Verify #4185, and identify PR #145 as open/unmerged.
- Current PR #145 comparison: 24 ahead / 327 behind / 13 files, merge base `c0d7218da907dbe0bae6cadb42824ca0cd09b83a`; GitHub marks it non-mergeable. Its neural-first default and explicit second-stage target adaptation are owner-level architecture changes. Leave it open and unmerged.
- Branch inventory: 67 refs including main (66 non-main). This is a verified count, not full file-level reconciliation. No branches deleted or force-updated.
- No runtime, mappings, generated artifacts, models or Pages output changed in this documentation refresh.

**Current readiness:** engineering-verified partial research prototype. Independent adjudicated IPA gold remains 0; specialist review, full ALA-LC/contextual coverage, authoritative current Lao draft, Lao-specific RTGS evidence, historical branch file-level reconciliation and manual accessibility/device QA remain incomplete or blocked.


## PR #202 post-merge reconciliation and stale-entrypoint correction — 2026-11-15

- Current `main` is `9d82ff4e62a97f1eaf3fbb81f87e0287fd30cc18`, the squash merge of PR [#202](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/202).
- Exact-head Verify #4186 / [run 43733767286 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43733767286); post-merge main Verify #4187 / [run 43733871453 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43733871453).
- A subsequent read of the merged `main` files showed that README and the canonical handoff still contained the PR #201 checkpoint (`c9e0e2a`, Verify #4185, PRs #198–#201), despite PR #202's title/body claiming to refresh them. The stale references are corrected in this continuation branch; this discrepancy is recorded rather than silently treating PR metadata as file evidence.
- README now distinguishes the latest source commit and Verify #4187 from the latest runtime deployment, which remains Pages #99 / [run 43726042017 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43726042017), deployed from `6bca3d2b899ebdffde02e1b4aa2454f3df1dc06e`.
- Fresh PR #145 comparison against current main: 24 ahead / 328 behind / 13 changed files; merge base `c0d7218da907dbe0bae6cadb42824ca0cd09b83a`. It remains open and non-mergeable; no review threads or submitted reviews were returned. Keep it unmerged pending the owner-level CLI/Python architecture decision.
- Historical branch inventory remains 67 refs including main before this new continuation branch; full file-level reconciliation remains PARTIAL. No historical branch was deleted or force-updated.
- No runtime, mappings, generated data, model assets or Pages artifacts changed. Readiness remains engineering-verified partial research prototype, not a linguistically validated universal converter.


## PR #203 merged — canonical entrypoint correction verified — 2026-11-15

- PR [#203](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/203) merged by squash as `2581c07a91be8659a65b3f970fd13be8fc20625f`; it corrected stale README and handoff records left after PR #202.
- Exact-head Verify #4188 / [run 43734584982 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43734584982).
- Post-merge main Verify #4189 / [run 43734692843 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43734692843).
- Both runs passed IPA-gold schema validation, repository data/evidence audit, Python tests, external-G2P harness syntax/CLI, locked browser dependency installation, browser-engine tests, browser-data regeneration/reproducibility, Chromium UI tests and built-page/relative-asset checks.
- Latest runtime deployment remains Pages #99 / run 43726042017; PR #203 was documentation-only.
- PR #145 remains the only open PR. Against this checkpoint it is 24 commits ahead / 329 behind / 13 files, merge base `c0d7218da907dbe0bae6cadb42824ca0cd09b83a`, and remains non-mergeable. Its neural-first CLI/Python default remains an owner-level architecture decision.
- Branch inventory before this new checkpoint branch: 68 refs including main (67 non-main). Full historical branch file-level reconciliation remains PARTIAL.
- No runtime or linguistic-coverage claim changed; independent adjudicated IPA gold remains 0.


## PR #204 merged — PR #203 checkpoint verification recorded — 2026-11-15

- PR [#204](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/204) merged by squash as `86b0e3f48cc363d670f852f1fcdef4ffe8d9782f`; it updates README, canonical handoff and this audit.
- Exact-head Verify #4190 / [run 43734857673 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43734857673).
- Post-merge main Verify #4191 / [run 43734956498 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43734956498).
- Both runs passed IPA-gold structure validation, repository data/evidence audit, Python tests, external-G2P harness syntax/CLI, locked browser dependency installation, browser-engine tests, browser-data regeneration/reproducibility, Chromium UI tests and built-page/relative-asset checks.
- Latest runtime deployment remains Pages #99 / run 43726042017; PR #204 was documentation-only.
- PR #145 remains the only open PR. Against this checkpoint it is 24 commits ahead / 330 behind / 13 files, merge base `c0d7218da907dbe0bae6cadb42824ca0cd09b83a`, and remains non-mergeable. Its neural-first CLI/Python default remains an owner-level architecture decision.
- Historical branch inventory has not been freshly re-enumerated since the 67-ref snapshot before PR #203/#204 continuation branches. Full file-level reconciliation remains PARTIAL.
- No runtime or linguistic-coverage claim changed; independent adjudicated IPA gold remains 0.


## Fresh historical branch inventory — 2026-11-15

- A fresh unfiltered branch search returned **71 refs including `main` (70 non-main)**; a follow-up pagination check returned no additional refs.
- This supersedes the earlier 67-ref snapshot. It is a count only; full file-level reconciliation of all 70 non-main refs remains PARTIAL.
- No historical branch was deleted, force-updated or merged as part of this inventory refresh.


## Fresh branch-graph reconciliation and Lao audio-source revalidation — 2026-11-15

**Base main:** `94cc9ed92f973bd7d6ad403cc21803dc54871302` (PR #205 merged).  
**Latest baseline Verify:** #4194 / [run 43735362383 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43735362383).  
**Branch inventory:** 71 refs including main (70 non-main). All 70 non-main refs were compared with main: **68 diverged, 2 behind-only, 0 ahead-only, 0 identical**. Behind-only: `feature/meta-hybrid-v3-multiengine-20261110` (114 behind) and `research/written-evidence-phonology-2026-11-09` (237 behind). No branch was deleted or force-updated.

### PR/branch disposition from current metadata and available discussions

- PR #145 is the only open PR; 24 ahead / 331 behind / 13 files; non-mergeable. It proposes a neural-first CLI/Python default and target-adaptation opt-in, an owner-level contract decision. Leave open and unmerged.
- PR #162's Meta-Hybrid v3 comparison orchestrator was explicitly described in its PR discussion as ported to main; its branch is superseded.
- PR #156's compatible benchmark scripts/workflows and confidence-gated comparisons were selectively ported to main; its old branch is not a missing feature.
- PRs #146/#147's deterministic reference profile and HVULao 1k benchmark were integrated in updated mainline forms; do not replay their stale branch snapshots.
- PR #148's repository docs/audit snapshot was superseded; its only unique retained change was an upstream methodology pin selectively ported to main.
- PRs #183/#186/#188 were closed unmerged as duplicate/superseded ALA-LC checkpoint work; no unique implementation or evidence was identified in their PR descriptions.
- Other merged PR branches remain historical source refs. Graph comparison and changed-file lists were obtained for all refs, but full per-file semantic review of every historical code/data/test delta is not complete. Therefore branch consolidation remains PARTIAL, not DONE_VERIFIED.

### Audio and rights research

- Common Voice Scripted Speech 27.0 Lao remains a contextual-audio candidate only: 223 clips, 193 validated, 16 contributor IDs, 0.35 validated hours, no named accent/variant and no IPA labels. Source record: `SRC-CV-LAO-27`.
- Mozilla Spontaneous Speech 5.0 (release 2026-09-16; 80 languages) was checked in the current catalogue on 2026-11-15; no Lao locale entry was found. This bounded catalogue result is recorded as `SRC-CV-SPS-5`; it does not establish that no other spontaneous Lao corpus exists.
- The IPA-gold playbook's blanket MekongPhon UNKNOWN-rights statement was inconsistent with `SRC-MEKONGPHON-2026`, which records repository-owner confirmation of full rights within authorized ClippyFirst project use. The playbook now distinguishes that owner authorization from an upstream public license, independent legal opinion, or blanket redistribution right. MekongPhon remains dictionary-seeded reference material, not independent gold.
- The independent adjudicated IPA gold corpus remains empty (0). No corpus records or IPA labels were added.

### Current task disposition

The canonical handoff and README now identify the verified baseline `94cc9ed`, PR #145's 24-ahead / 331-behind state, current branch graph classification, and the audio-source/rights evidence limits. The gold collection playbook and source registry include the Spontaneous Speech 5.0 catalogue check and corrected MekongPhon rights scope. The new research PR requires its own exact-head Verify before merge.


## PR #206 merged — audio-source and historical branch graph revalidation — 2026-11-15

- PR [#206](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/206) merged as `cab1f9a47a3ac3662aec3877e4edcf03b40d11bc`.
- Exact-head Verify #4202 / [run 43742489784 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43742489784); post-merge main Verify #4204 / [run 43742583553 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43742583553).
- The exact-head and post-merge checks passed IPA-gold structural validation, repository data/evidence audit, Python tests, external-G2P harness syntax/CLI, locked browser dependency installation, browser engine tests, canonical browser-data regeneration/reproducibility, Chromium UI tests and built-page/relative-asset checks.
- Current branch inventory after the PR: 72 refs including main (71 non-main). All 71 non-main refs compared with main: 69 diverged, 2 behind-only, 0 ahead-only, 0 identical. Behind-only refs remain `feature/meta-hybrid-v3-multiengine-20261110` and `research/written-evidence-phonology-2026-11-09`. Full semantic review of every changed file remains PARTIAL; no branches deleted or force-updated.
- PR #145 remains the only open PR, 24 ahead / 332 behind / 13 files, non-mergeable; its neural-first CLI/Python default remains an owner-level architecture decision.
- PR #206 revalidated Common Voice and MekongPhon rights evidence; it did not add corpus labels or IPA gold. Independent adjudicated gold remains 0.
- Latest Pages deployment remains #99 / run 43726042017; PR #206 was research/documentation-only.


## PR #206 merged — audio-source and branch-graph checkpoint — 2026-11-15

- PR [#206](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/206) merged by squash as `cab1f9a47a3ac3662aec3877e4edcf03b40d11bc`.
- Exact-head Verify #4202 / [run 43742489784 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43742489784).
- Post-merge main Verify #4204 / [run 43742583553 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43742583553). The post-merge workflow passed the IPA-gold structure check, repository data/evidence audit, Python tests, external-G2P harness syntax/CLI, locked browser dependency install, browser-engine tests, canonical browser-data regeneration/reproducibility, Chromium UI tests and built-page/relative-asset checks.
- Latest main at this checkpoint: `cab1f9a47a3ac3662aec3877e4edcf03b40d11bc`. Latest runtime deployment remains Pages #99 / run 43726042017; PR #206 changed no runtime assets.
- The post-merge handoff snapshot records 72 refs including main (71 non-main): 69 diverged, 2 behind-only, 0 ahead-only, 0 identical. Behind-only refs: `feature/meta-hybrid-v3-multiengine-20261110` (114 behind) and `research/written-evidence-phonology-2026-11-09` (237 behind). The later documentation checkpoint branch is not part of that base snapshot. This is graph-level classification, not complete semantic file review.
- PR #145 remains the sole open PR; against this main it is 24 commits ahead / 332 behind / 13 files, merge base `c0d7218da907dbe0bae6cadb42824ca0cd09b83a`, and GitHub marks it non-mergeable. It remains blocked on the explicit owner architecture decision.
- Audio research remains non-gold: Common Voice Scripted Speech 27.0 Lao is a contextual-audio lead (193 validated clips, 16 contributor IDs, no named accent/variant, no IPA labels); no Lao locale was found in the checked Spontaneous Speech 5.0 catalogue. MekongPhon owner authorization is scoped to authorized ClippyFirst project use, not a public upstream license or blanket redistribution permission. The independent adjudicated IPA gold corpus remains 0.
- Full file-level semantic reconciliation of historical branches remains PARTIAL; no branch was deleted or force-updated.


## PR #207 merged and stale romanization branch disposition — 2026-11-15

- PR [#207](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/207) merged as `e713f62d2c37412b52dc7a6b51004797fc283ef1`; exact-head Verify #4206 / run 43742806539 and post-merge Verify #4207 / run 43742918142 both passed.
- PR #207 was documentation-only; Pages #99 remains the latest runtime deployment.
- Reviewed `feat/romanization-input-to-ukrainian-20261115` against main: 40 ahead / 30 behind / 13 changed files; its historical PR #172 is already merged. `web/app.js` is identical. Its romanization engine/tests are an older snapshot and predate current explicit unknown-profile fail-closed behavior and ALA-LC unsupported-sequence guards. It normalizes some ambiguous spellings that main now deliberately marks PARTIAL. The current matrix also contains later route-separation and research updates.
- **Disposition: SUPERSEDED.** The supported direct romanization route from PR #172 is on main and was refined by subsequent fixes. No stale code was ported; any isolated future change must be supported by the source table and a regression fixture.
- The PR #206 graph snapshot covered 72 refs including main (71 non-main); after PR #207 and the current continuation branch were created, live search returned 74 refs including main. The two task branches are not part of that earlier classification. Full semantic review of historical branches remains PARTIAL; no branch was deleted or force-updated.
- PR #145 remains the only open PR, 24 ahead / 333 behind / 13 files against main, non-mergeable pending an explicit architecture decision.


## PR #208 merged — current branch graph and romanization/ALA-LC dispositions — 2026-11-15

- PR [#208](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/208) merged as `c5a59c8aa2a75c95a620b14f9caa9154a1030fc0`; exact-head Verify #4208 / run 43743149223 and post-merge Verify #4209 / run 43743272169 both passed.
- Fresh unfiltered branch search returned 74 refs including main (73 non-main); pagination returned no additional refs. All 73 non-main refs are graph-classified: 71 diverged, 2 behind-only, 0 ahead-only, 0 identical. Behind-only: `feature/meta-hybrid-v3-multiengine-20261110` (117 behind) and `research/written-evidence-phonology-2026-11-09` (240 behind). This classification is not full semantic file review.
- The two later task branches are now included: PR #207 source branch is 6 ahead / 2 behind; PR #208 source branch is 3 ahead / 1 behind. No branch was deleted or force-updated.
- Reviewed `feat/romanization-input-to-ukrainian-20261115` (historical PR #172): 40 ahead / 30 behind / 13 changed files; `web/app.js` identical to main; its engine/tests are superseded by current fail-closed and ALA-LC unsupported-sequence guards. No code was ported.
- ALA-LC lineage confirmed: PRs #173, #176, #182 and #192 merged; PR #181 is closed unmerged duplicate/superseded by #182. Do not replay its stale branch.
- PR #145 remains the sole open PR: 24 ahead / 334 behind / 13 files, non-mergeable, pending owner architecture decision.
- No runtime, mapping, generated-data or model assets changed; independent adjudicated IPA gold remains 0.


## PR #209 pre-merge branch inventory correction — 2026-11-15

- A fresh unfiltered search after creating the PR #209 checkpoint branch returns 75 refs including main (74 non-main); the next page is empty.
- Relative to current main, the two post-PR #206 continuation branches are diverged (PR #207 source branch 6 ahead / 2 behind; PR #208 source branch 3 ahead / 1 behind). The current PR #209 source branch is 3 ahead / 0 behind before merge.
- The resulting pre-merge graph classification is 71 diverged, 2 behind-only, 1 ahead-only, 0 identical. The ahead-only ref is this task branch; it is expected to become diverged after squash merge. Behind-only refs are `feature/meta-hybrid-v3-multiengine-20261110` (117 behind) and `research/written-evidence-phonology-2026-11-09` (240 behind).
- Full semantic file/test review remains PARTIAL. No branch was deleted or force-updated.


## PR #209 merged — canonical mainline checkpoint — 2026-11-15

- PR [#209](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/209) merged by squash as `63fd3435397af693633b5bec90aa4448aecbf9d7`.
- Exact-head Verify #4211 / [run 43743622227 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43743622227).
- Post-merge main Verify #4212 / [run 43743705285 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43743705285).
- Both runs passed IPA-gold structure validation, repository data/evidence audit, Python tests, external-G2P harness syntax/CLI, locked browser dependency install, browser-engine tests, browser-data regeneration/reproducibility, Chromium UI tests and built-page/relative-asset checks.
- Latest runtime deployment remains Pages #99 / run 43726042017; PR #209 changed no runtime assets.
- Current main: `63fd3435397af693633b5bec90aa4448aecbf9d7`. PR #145 remains the only open PR, 24 ahead / 335 behind / 13 files, non-mergeable pending owner architecture decision.
- Branch inventory at this checkpoint: 75 refs including main (74 non-main), 72 diverged and 2 behind-only; no ahead-only or identical refs. Behind-only refs: `feature/meta-hybrid-v3-multiengine-20261110` (117 behind) and `research/written-evidence-phonology-2026-11-09` (240 behind). Full semantic file review remains PARTIAL.
- No runtime, mapping, generated-data or model assets changed; independent adjudicated IPA gold remains 0.


## LDC Babel Lao audio lead — primary-source and license review — 2026-11-15

- The LDC catalogue for [LDC2017S08](https://catalog.ldc.upenn.edu/LDC2017S08) describes approximately 207 hours of conversational and scripted telephone speech collected in 2013, Vientiane dialect region, with orthographic transcripts and 8 kHz A-law / 48 kHz PCM audio.
- The [Lao LSP](https://catalog.ldc.upenn.edu/docs/LDC2017S08/LSP_203_final.pdf) says recordings are by native Lao speakers and describes a separate Appen Butler Hill codepoint romanization. It documents a 43-phoneme inventory and X-SAMPA tone notation, but the publicly exposed transcript sample is Lao script and the paired `.rom.txt` sample is ABH romanization. Per-utterance X-SAMPA labels in the delivered package are **not verified**.
- The [non-member agreement](https://catalog.ldc.upenn.edu/license/iarpa-babel-lao-agreement-non-member.pdf) restricts use to non-commercial linguistic education/research/technology development and prohibits further distribution. The for-profit member agreement operates under the LDC For-Profit Membership Agreement and also prohibits further distribution. Fees and applicable project eligibility have not been confirmed.
- LDC states portions are © 2015 U.S. Government and that the U.S. Government acquired the data from Appen. No audio or transcript files were imported. The existing `SRC-LDC-BABEL-LAO-2017` registry record is expanded with these details; the playbook classifies the resource as a licensed contextual-audio lead, not citation-form or IPA gold.
- **Disposition:** BLOCKED pending signed access terms, fees, organization eligibility and confirmation of package annotation fields. Even if access is approved, use only as contextual audio/transcript support under the agreement; independent IPA annotation and adjudication remain required.


## PR #210 merged — LDC Babel Lao licensed audio lead — 2026-11-15

- PR [#210](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/210) merged as `d2f591988e329205cb05138337657e66b73586c8`.
- Exact-head Verify #4220 / [run 43744151301 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43744151301).
- Post-merge main Verify #4221 / [run 43744244532 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43744244532).
- Both runs passed IPA-gold structure validation, repository data/evidence audit, Python tests, external-G2P harness syntax/CLI, locked browser dependency install, browser-engine tests, browser-data regeneration/reproducibility, Chromium UI tests and built-page/relative-asset checks.
- The existing `SRC-LDC-BABEL-LAO-2017` record was expanded; the LDC2017S08 lead is documented as licensed contextual audio only, not IPA gold. No dataset files were imported.
- Current main: `d2f591988e329205cb05138337657e66b73586c8`. PR #145 remains the only open PR, 24 ahead / 336 behind / 13 files, non-mergeable pending owner architecture decision.
- Branch inventory: 76 refs including main (75 non-main), 73 diverged and 2 behind-only. Behind-only refs: `feature/meta-hybrid-v3-multiengine-20261110` (119 behind) and `research/written-evidence-phonology-2026-11-09` (242 behind). Full semantic review remains PARTIAL.
- No runtime, mapping, generated-data or model assets changed; independent adjudicated IPA gold remains 0.


## PR #211 merged — LDC source and current mainline checkpoint — 2026-11-15

- PR [#211](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/211) merged as `5c932055b81a76c8bf67f6c77818f9e28f59975e`.
- Exact-head Verify #4222 / [run 43744403049 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43744403049).
- Post-merge main Verify #4223 / [run 43744509613 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43744509613).
- Both runs passed IPA-gold structure validation, repository data/evidence audit, Python tests, external-G2P harness syntax/CLI, locked browser dependency install, browser-engine tests, browser-data regeneration/reproducibility, Chromium UI tests and built-page/relative-asset checks.
- PR #211 was documentation-only. It synchronizes the README/handoff/audit with PR #210 and the LDC2017S08 research lead; no runtime or data artifacts were imported.
- Current main: `5c932055b81a76c8bf67f6c77818f9e28f59975e`. PR #145 remains the only open PR, 24 ahead / 337 behind / 13 files, non-mergeable pending owner architecture decision.
- Branch inventory: 77 refs including main (76 non-main), 74 diverged and 2 behind-only. Behind-only refs: `feature/meta-hybrid-v3-multiengine-20261110` (120 behind) and `research/written-evidence-phonology-2026-11-09` (243 behind). Full semantic review remains PARTIAL.
- No runtime, mapping, generated-data or model assets changed; independent adjudicated IPA gold remains 0.


## PR #212 merged — current mainline checkpoint — 2026-11-15

- PR [#212](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/212) merged as `2ed3b25ef8d62d511ddc46f7f087ba3c3d3133bd`.
- Exact-head Verify #4224 / [run 43744712602 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43744712602).
- Post-merge main Verify #4225 / [run 43744818594 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43744818594).
- Both runs passed IPA-gold structure validation, repository data/evidence audit, Python tests, external-G2P harness syntax/CLI, locked browser dependency install, browser-engine tests, browser-data regeneration/reproducibility, Chromium UI tests and built-page/relative-asset checks.
- PR #212 was documentation-only; it synchronizes the canonical README/handoff/audit with PR #211. No runtime, mapping, generated-data or model assets changed.
- Current main: `2ed3b25ef8d62d511ddc46f7f087ba3c3d3133bd`. PR #145 remains the only open PR, 24 ahead / 338 behind / 13 files, non-mergeable pending owner architecture decision.
- Branch inventory: 78 refs including main (77 non-main), 75 diverged and 2 behind-only. Behind-only refs: `feature/meta-hybrid-v3-multiengine-20261110` (121 behind) and `research/written-evidence-phonology-2026-11-09` (244 behind). Full semantic review remains PARTIAL.
- No runtime, mapping, generated-data or model assets changed; independent adjudicated IPA gold remains 0.


## Fresh branch-graph reconciliation after PR #220 — 2026-11-15

- Branch inventory: 87 refs total, comprising `main` plus 86 non-main branches.
- Compared the 85 pre-existing non-main branch heads with main SHA `fe1c4a0b8966155b5f22e6cc58ebcb3a33d5bbf9`: 83 `diverged`, 2 `behind` only, 0 `ahead` only, 0 identical. The current documentation PR branch is the 86th non-main ref and compares `ahead` by 5 / `behind` by 0. Behind-only refs: `feature/meta-hybrid-v3-multiengine-20261110` and `research/written-evidence-phonology-2026-11-09`.
- Targeted review of `fix/romanization-numeric-crosswalk-20261108` and `fix/empty-lao-input-window` found the relevant numeral-crosswalk and clear-to-empty browser tests already present on main; no code port required.
- `feat/pages-hybrid-v2-browser` corresponds to merged PR #158, but the browser neural panel/model/ONNX/WASM publication was explicitly retired 2026-11-10. Commits 0846e377 and afa035d make the current Pages artifact deterministic-only. This is an intentional product boundary, not an unmerged feature to recover.
- Current romanization work merged in PRs #214/#218/#220; documentation/deployment reconciliation merged in #219. PR #145 remains the only open PR and is blocked by an owner-level architecture decision.
- No branch was deleted. Graph comparison is complete; semantic review of all 83 diverged branch diffs is still PARTIAL. Do not bulk-port, merge or delete historical branches; reopen only a specific evidenced task.


## Post-PR #221 graph and semantic spot-check — 2026-11-15

- Current `main`: `99d9fd3b5aa443c1a34af9ab9b30a3e51add39a7`. Branch search returns 87 refs total (main + 86 non-main). The merged PR #221 branch is retained and now compares 8 ahead / 1 behind; it is not a reason to rewrite or delete that historical ref.
- PR #145 remains the only open PR; current comparison is 24 ahead / 349 behind / 13 files, merge base `c0d7218da907dbe0bae6cadb42824ca0cd09b83a`, status diverged/non-mergeable. It is an owner architecture decision, not a routine conflict-resolution task.
- ALA-LC candidate branches rechecked: `fix/ala-lc-2012-conformance-20261115` (21/46), `fix/ala-lc-final-crosswalk-current-main-20261115` (11/38), `fix/ala-lc-final-w-crosswalk-20261115` (9/39), `fix/ala-lc-unsupported-vowel-guard-20261115` (5/43). Their runtime snapshots predate or duplicate current main's source-aware crosswalk, ALA-LC final-`o` handling, unsupported-form guard and seven-vowel diagnostics. No unique implementation was ported; branches remain untouched.
- This is a targeted semantic review, not a full review of all divergent refs. Overall historical-branch semantic reconciliation remains PARTIAL. No branch was deleted, force-updated or mass-merged.


## PR #222 exact-head checks — 2026-11-15

PR #222 exact-head Verify [#4286 / run 43760081269](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43760081269) passed: 350 Python, 192 Node and 28 Chromium tests, IPA-gold schema validation, repository/evidence audit, external-G2P syntax/CLI, build, generated-data reproducibility and built-page/deterministic-only artifact assertions. No runtime files changed; no Pages deployment required.

## Branch inventory refresh — 2026-11-16

**Default branch:** `main`, head `6512aac75cfb71c2d5f6f37a040f55739f32b14f` (post-merge Verify #4336 passed).
**Branch refs:** GitHub API inventory returned 102 refs across two pages: 101 non-main plus `main`. No branch was deleted, force-updated or mass-merged.
**Open PR inventory:** only PR [#145](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/145) remains open. It is the neural-first MekongPhon proposal, 24 commits ahead / 364 behind current main, divergent and `mergeable=false`; leave it for explicit owner architecture decision.
**Recently merged relevant work:** PRs #231–#236 are merged. #231 added the real-browser Note 10 fail-closed guard; #232–#236 reconciled the ALA-LC Notes 8–10 and LaoNLP evidence in the matrix, source registry, audit, README and handoff. PR #236 is docs-only and post-merge Verify #4336 passed.

### Relevant divergent branch comparisons

The following potentially relevant historical branches were compared directly with current main. These are not fast-forward candidates; their commit histories diverge and current main has progressed. File lists overlap with already integrated work, so do not cherry-pick or merge them wholesale.

| Branch | Ahead | Behind | Relevant changed files | Disposition |
|---|---:|---:|---|---|
| `fix/ala-lc-2012-conformance` | 21 | 61 | ALA-LC engine, tests, matrix, audit, source registry | Historical candidate; review individual missing behavior only |
| `feat/romanization-input-to-ukrainian-20261115` | 40 | 62 | app, engine, tests, UI, matrix, README | Main already contains direct romanization input; do not replay branch |
| `fix/ala-lc-final-crosswalk-current-main-20261115` | 11 | 53 | crosswalk engine/tests, methodology, matrix | Superseded divergent snapshot; inspect only if a concrete regression is found |
| `fix/ala-lc-final-w-crosswalk-20261115` | 9 | 54 | final-`w` crosswalk and tests | Superseded divergent snapshot; no wholesale merge |
| `test/ala-lc-note4-context-regressions-20261116` | 6 | 14 | Note 4 regression/docs | Historical branch; compare individual tests if needed |
| `feat/mekongphon-first-stage` (PR #145) | 24 | 364 | neural-first API/CLI, docs, tests, benchmark workflow | Open owner-level architecture proposal; leave untouched |

The API inventory contained 102 refs; only the six directly relevant divergent candidates above were individually compared in this refresh. This is not a claim that all 101 non-main refs were individually diff-reviewed. Preserve historical refs. Any future consolidation should be an explicit, file-level, test-backed task rather than a branch cleanup operation.


## PR #247 branch and evidence checkpoint — 2026-11-16 (Ueda review)

- **Default branch:** `main` at `390302db31b56f5842696c2d81a817689635472b`.
- **Working branch:** `docs/correct-loc-note10-source-example-20261116`; at this comparison it is 89 commits ahead / 0 behind main, with eight changed files. PR #247 remains open, unmerged and mergeable; PR #145 remains open and untouched for the owner-level neural-first vs deterministic-default decision.
- **Research update:** Ueda (1994) full text was inspected through Undermind. The described Vientiane dialect has no phonological consonant clusters despite written consonant sequences; written `w` can correspond to /ua/ or no independent segment. This is phonological evidence, not a complete orthographic syllabification algorithm.
- **Evidence registry:** 77 unique source IDs and 91 unique claim IDs; no duplicate IDs detected. The new claim `CLM-LAO-ORTHOGRAPHIC-SEQUENCES-NOT-PHONOLOGICAL-CLUSTERS` is linked to existing `SRC-UEDA`.
- **Exact-head CI:** Verify #4500 / run 43966297408 passed on `3a257848ddecb6d45968eae7cbdc1d2b1fd32dd4`. The latest README/register/handoff synchronization commits are documentation-only; exact-head CI must be checked on the final branch SHA before claiming it.
- **Disposition:** preserve PR #247 and all historical branches; no merge, rebase, force-push, branch deletion or Pages deployment was performed. PR #145 remains untouched.


## Berment historical Lao grammar research checkpoint — 2026-11-17

- Full-text Berment (2004) thesis and Del Vigna & Berment (2003) paper reviewed; details are recorded in the canonical Undermind research note and repository direct-input audit/matrix/register.
- Registry now has 79 unique source IDs and 95 unique claim IDs. No duplicate IDs were detected; cross-reference integrity is checked separately below.
- PR #247 remains open, unmerged and mergeable. Branch comparison after evidence and documentation updates: 117 commits ahead / 0 behind `main`, eight changed files.
- Verify #4502 / run 43966645076 passed on pre-update evidence/docs HEAD `cb86f87fba32140c71f8f1a22ab5668d1d9ffd4b`. The Berment registry/audit/matrix/register/handoff/README changes are later commits and require exact-head CI; no runtime, corpus, model, dictionary or generated artifact changed.
- No code was copied from the historical thesis; no license is inferred. PR #145 remains untouched. No merge, force-push, branch deletion or Pages deployment performed.


## Modern Lao grapheme evidence and CI checkpoint — 2026-11-17

- Added ICANN Lao Script Generation Panel proposal v3.1 (2017), current Root Zone LGR-6 Lao (2025), and clarified the W3C 2026 Lao Layout Requirements document as an unendorsed Group Note Draft. Registry totals: 81 unique sources / 99 unique claims; no duplicate IDs or missing claim-to-source references.
- New evidence supports a separate grapheme-placement analyzer: pre-base vs above/below/after vowel components, tone-mark placement, U+0EBC after consonant, and sign handling. ICANN explicitly leaves many spelling constraints unenforced and is DNS root-zone scoped; W3C is typographic guidance and not endorsed. No runtime changes made.
- Verify #4506 / run 43968825128 completed SUCCESS on `defa2f87a0730098aad240528641cac2527ca897`; all configured steps passed, including Chromium UI and built-page/relative-asset checks. Later evidence/docs commits require exact-head CI.
- PR #247 remains open/unmerged; PR #145 remains untouched. No code, corpus, model, dictionary, generated data or Pages deployment changed.


## Final state after ICANN/W3C evidence sync — 2026-11-17

- Branch HEAD: `900f9c5d216743b4d86394dc6d6397e04f275c82`; comparison with main: 113 ahead / 0 behind; eight changed files.
- Registry: 81 unique source IDs / 99 unique claim IDs; no duplicate IDs and no missing claim-to-source references.
- Verify #4506 / run 43968825128 passed on `defa2f87a0730098aad240528641cac2527ca897`, but is not exact-head CI for the evidence/docs commits after it. Commit-run lookup currently returns no run for the final HEAD; do not mark the final HEAD verified until a matching workflow run completes.
- PR #247 remains open, mergeable and unmerged. PR #145 untouched. No runtime/code/corpus/model/dictionary/generated artifacts changed; no deployment.


## Exact-head Verify #4513 — 2026-11-17

- Verify #4513 / run 43970708960 started on exact current branch HEAD `f18250734f0b3989d02bed3d8d1d4f3611eedc18`.
- At the latest poll, schema/evidence audit, Python, external-G2P, browser engine, build and generated-data reproducibility had passed; Chromium UI was in progress and built-page/asset verification pending.
- Do not mark this exact-head run successful until all remaining steps complete.


## Current reporting-only sync and exact-head CI — 2026-11-17

- Latest docs synchronization before this checkpoint is `900f9c5d216743b4d86394dc6d6397e04f275c82`; branch is 117 commits ahead / 0 behind main, eight changed files.
- Verify #4513 / run 43970708960 passed on its exact tested SHA `f18250734f0b3989d02bed3d8d1d4f3611eedc18`; three later commits only synchronized the branch audit, handoff and README. Do not claim #4513 as exact-head verification for this reporting-only synchronization. A new exact-head run is required.


## Ishida 2026 segmentation evidence and regression tests — 2026-11-17

- Added Richard Ishida's *Lao Orthography Notes* (updated 2026-04-28) to the source registry and five scoped claims: explicit vowels/restricted codas make syllable boundaries relatively straightforward; word boundaries remain dictionary/ZWSP-dependent; pre-base vowels anchor before the entire onset; onset labialization and high-class `ຫ` sequences are distinct; Unicode grapheme clusters are not syllables; modern coda inventory differs from ICANN root-zone repertoire.
- Added three source-backed orthographic regression examples (`ໃຫຍ່`, `ເຫຼືອງ`, `ປະເທດ`) to `tests/test_multisyllable_segmentation.py`. They assert syllable segmentation only, not IPA gold.
- Verify #4517 / run 43971181584 on test commit `cb7950065c310c9376f7075fe7688059475c0a19`: Python tests, evidence audit, external-G2P, browser engine, build and reproducibility passed; Chromium UI and built-page checks were still in progress at last poll.
- Registry: 81 unique sources / 104 unique claims; no duplicate IDs or missing references. No runtime implementation, corpus, model, dictionary or generated artifacts changed.


## Exact-head verification and source-registry deduplication — 2026-11-17

- Verify #4518 / run 43971358699 completed SUCCESS on exact pre-sync HEAD `ff6b62198510fc7bb69e2b132bddcffaaa487019`. All configured steps passed, including schema/evidence, Python (including three Ishida segmentation fixtures), external-G2P, browser engine, build/reproducibility, Chromium UI and built-page/relative-asset checks.
- Reconciled the newly expanded Ishida source details into the existing `SRC-ISHIDA-ORTHO-2026` record already used by the onset/vowel registries instead of retaining a duplicate source row. Final registry: 81 unique sources / 104 unique claims; no duplicate IDs or missing source references.
- This final synchronization is registry/documentation-only; the test additions and all other evidence were included in the successful #4518 parent checkpoint. A fresh exact-head workflow is triggered by this synchronization.


## Coda inventory source discrepancy — 2026-11-17

Ishida's explicit final-position list (nine letters) and the consonant-class chart (which additionally lists ຢ) disagree; the IPA correspondence table maps final /j/ to ຍ. The project preserves the nine source-explicit mappings, keeps ຢ fail-closed, and now checks this with scripts/audit.py plus a Python regression. The phoneme-category data/lao/codas.csv is not the parser's orthographic final-letter lookup. Implicit /ʔ/ after short vowels remains an evidence-limited dialect question. No runtime mappings changed. Registry: 81 sources / 105 claims expected. Exact-head CI pending.


## Exact-head verification — Ishida coda reconciliation (2026-11-17)

Verify #4525 / [run 44035119603 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/44035119603) passed on exact PR head `9b7d39b237a8dfa7e69544a1122ae1c1e2c3514e`. All configured checks passed: independent IPA-gold schema, repository/data/evidence audit, Python tests (including the new nine-coda map and fail-closed `ກາຢ` regression), external-G2P syntax/CLI, locked browser dependencies, browser engine tests, build/canonical browser-data generation, generated-data reproducibility, real Chromium UI tests, and built-page/relative-asset checks. No runtime, corpus, model, dictionary or generated artifact changed. Registry: 81 unique sources / 105 unique claims; no duplicate IDs or missing claim-source references. Branch comparison before this reporting-only sync: 131 ahead / 0 behind `main`; PR #247 remains open/unmerged.


## Exact-head verification — coda reconciliation and reporting sync (2026-11-17)

Verify #4526 / [run 44035383672 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/44035383672) passed on exact PR head `843b7695afd983b4dddd573eb570af80a71cbea2`. All configured steps passed: IPA-gold schema, repository/data/evidence audit, Python tests, external-G2P syntax/CLI, locked browser dependencies, browser engine, build/canonical data generation, generated-data reproducibility, real Chromium UI, and built-page/relative-asset checks. This head contains the coda source-conflict claim, nine-item audit invariant, fail-closed ກາຢ regression, and canonical docs/README synchronization. Registry: 81 unique sources / 105 unique claims; no duplicates or missing claim-source references. Branch comparison at this checkpoint: 132 ahead / 0 behind main. PR #247 remains open and unmerged; PR #145 remains open and untouched (24 ahead / 374 behind main; neural-first default conflicts with deterministic-default contract).

## Research continuation branch — Lao short-vowel glottal evidence (2026-11-17)

- Created `integration/loc-note10-glottal-evidence-20261117` directly from current `main` SHA `390302db31b56f5842696c2d81a817689635472b`; it is a descendant of main fast-forwarded to PR #247's reviewed head, with PR #248's evidence delta applied and reconciled on top.
- PR #247 remains open and unmerged on `docs/correct-loc-note10-source-example-20261116` at `d84afd57bd7bdc3575271cf3d9f51066bb50a044`, 133 commits ahead / 0 behind `main`; its file changes are ported and reconciled in this integration branch while the original branch remains untouched.
- PR #145 remains open and untouched; its neural-first architecture proposal remains incompatible with the current deterministic-default contract pending owner decision.
- This branch's task is deliberately narrow: distinguish orthographic coda graphemes from phonological /ʔ/ and from prosodically conditioned glottal closure. No runtime, model, corpus, dictionary, generated artifact or deployment changes are authorized by the current evidence.
- Initial exact-head Verify #4537 / [run 44079440345 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/44079440345) passed on `1f59909d7af03d8f4fb0c7c3a2e6ae35f8b842b1`: 357 Python, 204 browser-engine and 30 Chromium tests plus all configured schema, data/evidence, external-G2P, build, reproducibility and built-page checks. Verify #4546 / [run 44079888990 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/44079888990) passed on `f088fab50ffa4675419b9994d6d76adf79d717de`: 357 Python, 204 browser-engine and 30 Chromium tests plus all configured schema, data/evidence, external-G2P, build, reproducibility and built-page checks. The final verification-report-only sync is followed by one final exact-head run. PR #247 and PR #248 remain open pending exact-head verification and review of this consolidated integration PR.

## Controlled PR #247/#248 integration branch — 2026-11-17

- integration/loc-note10-glottal-evidence-20261117 is based on the current default branch and includes the file-level changes from PR #247 and PR #248. The original PR branches remain unchanged.
- PR #247's reviewed commit history is retained as the branch ancestor; PR #248's eight-file delta was reconciled into the same branch. The six overlapping paths were handled deliberately rather than merged blindly; source/claim rows were merged by stable IDs and documentation sections were preserved.
- Registry validation on the integrated contents: 82 unique sources, 107 unique claims, no duplicate IDs and no missing claim-to-source references.
- Verify #4551 / run 44081456903 passed on integrated code/test head 0f92c143adf896d0e4bc603e9296f20b6a3272f7: 359 Python, 204 browser-engine and 30 Chromium UI tests; schema/evidence, external-G2P, build, reproducibility and built-page checks passed. Review the consolidated diff before merging either source PR.
- PR #145 remains untouched. No branch deletion, force-push, runtime change, model/corpus/dictionary change or deployment was performed.


## PR #249 integration merge — 2026-11-17

- PR #249 merged by squash to main as `825d7bf91d756c7abda884e2348a8fdfd82ec31f`. It consolidates the LOC Note 10/coda evidence and tests from PR #247 with the Ueda/Lew/Cole glottal evidence from PR #248. The 13-file diff was inspected; source/claim rows and overlapping docs were reconciled before merge.
- Exact integrated PR-head Verify #4557 / [run 44082038728](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/44082038728) SUCCESS: 359 Python, 204 browser-engine and 30 Chromium UI tests; IPA-gold schema, repository/data/evidence audit, external-G2P syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks all passed.
- Exact merged-main Verify [run 44083165575](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/44083165575) SUCCESS on the exact merge SHA. This is hosted CI evidence; no local test execution is claimed.
- PRs #247 and #248 closed as superseded with explanatory comments; their branches remain preserved. PR #145 remains open/untouched and is 24 ahead / 375 behind main; it is a separate neural-first architecture proposal, not silently integrated.
- Registry: 82 unique source IDs / 107 unique claim IDs, no duplicate IDs or missing claim-source references.
- No runtime, IPA mapping, tone rule, corpus, model, dictionary, generated artifact or Pages deployment changed. Note 10 exact Lao glyph/automatic role derivation remains unresolved; short-vowel /ʔ/ remains analysis-dependent; automatic insertion blocked; independent gold=0 and accuracy=null. Engineering status: partial research prototype, not linguistically release-ready.


## PR #251 merge — LOC Note 10 Word-source correction — 2026-11-17

- PR #251 merged by squash as `8945c94f3a0a6f44f6bdfb6cbad7bdcf99c9402d`. It verifies the official LOC 2012 Word-source example `ຄຼິສຕຽນ (khitsatīan)` and registers the historical 1997 PDF's extracted romanization `khitsatian`; the 1997 Lao-script glyphs are corrupted in extraction and no exact script form is asserted.
- Exact PR-head Verify #4611 / [run 44085447163](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/44085447163) SUCCESS: 359 Python, 204 browser-engine and 30 Chromium UI tests; schema/evidence audit, external-G2P syntax/CLI, build, generated-data reproducibility and built-page checks passed.
- Exact merged-main Verify [run 44086036717](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/44086036717) SUCCESS on the exact merge SHA. No local tests are claimed.
- Registry: 83 unique sources / 108 unique claims, no duplicates, malformed CSV rows or missing claim-source references.
- Source-example attribution is DONE_VERIFIED. The source-role crosswalk remains an explicitly supplied-role engineering fixture; automatic Lao source-role derivation and full Note 10 conformance remain PARTIAL/BLOCKED. No runtime, IPA, pronunciation, tone, model, corpus, dictionary, generated artifact or Pages deployment changed. Gold=0; accuracy=null.

## External syllabifier assessment — branch checkpoint 2026-11-17

- Starting main for this batch: 433a8c83b181fa56b679ccd0bfcf44e96069736a (after PR #253 LOC Word/PDF discrepancy reconciliation and its verification closeout).
- Working branch: research/bethke-syllabifier-note10-mainline-2026-11-17. The earlier branch research/bethke-syllabifier-note10-2026-11-17 is preserved and was not rebased or force-updated after main advanced.
- Added one pinned external software source and one bounded research claim after inspecting the upstream GitHub source, CPAN release metadata and license. No code was imported.
- The candidate's X9 class includes ສ, but the regex requires X10_3/U+0E4C; X8 excludes ສ. The current LOC Word-source token has no U+0E4C. Static inspection does not demonstrate an automatic Note 10 coda role. Exact package execution remains blocked by DNS failure.
- This branch changes only source/claim registries and research/matrix/handoff/audit documentation. It does not change runtime, generated artifacts, model, dictionary, corpus, IPA labels or deployment.
- PR #145 remains open and untouched as a separate owner-level neural-first architecture decision; issues #9 and #99 remain open. No expert outreach or gold annotation was performed.

## PR #254 merge — external Lao syllabifier evidence checkpoint — 2026-11-17

- PR #254 merged by squash as `ca64158ce0b6d92ef0a01956f16ed941277bf446`.
- Exact PR-head Verify #4668 / [run 44088848659](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/44088848659) SUCCESS; exact merged-main Verify #4670 / [run 44089165636](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/44089165636) SUCCESS. All configured workflow steps passed.
- Evidence registry now contains 84 unique source IDs / 110 unique claim IDs; no duplicate IDs or malformed nonblank rows.
- No runtime, IPA, tone, model, corpus, dictionary, generated artifacts or Pages deployment changed. The original pre-sync research branch was preserved; no force-push or branch deletion occurred. PR #145 remains open/untouched.
- The candidate package was assessed statically only; network/DNS prevented execution. Automatic LOC Note 10 source-role derivation remains PARTIAL/BLOCKED; independent gold=0; accuracy=null.

## PR #255 merge — canonical documentation synchronization — 2026-11-17

- PR #255 merged by squash as `d8314fc527a9e246df9b22ca570a533ff9122679`.
- Exact PR-head Verify #4671 / [run 44089568451](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/44089568451) SUCCESS; exact merged-main Verify #4672 / [run 44089755616](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/44089755616) SUCCESS.
- The PR reconciled README, handoff, completion register and audit with PR #254's merge and CI evidence. It changed documentation only; no runtime, source data, corpus, model, generated artifact or deployment changed.
- The repository still has one open PR (#145) and two open research/validation issues (#9, #99). PR #145 remains untouched; no force-push or branch deletion occurred.
- Current research blockers: no independently adjudicated IPA gold; no automatic LOC Note 10 source-role derivation; no executed Bethke package comparison because of DNS failure. Engineering readiness remains partial prototype, not linguistic release readiness.
