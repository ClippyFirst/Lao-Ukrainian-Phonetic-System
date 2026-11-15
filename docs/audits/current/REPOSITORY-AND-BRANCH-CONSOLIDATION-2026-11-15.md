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
| Identify canonical branch and exact starting head | DONE_VERIFIED | `main`; compare `main` with `4197d4212a935ee59216b1a7f9bdd112dceabb6e` returned identical |
| Inventory branch refs | DONE_VERIFIED | GitHub branch search returned 37 refs including `main` |
| Compare all non-main branch refs with main | DONE_VERIFIED | 36 compare operations completed in batches; all were divergent or behind, none was ahead-only |
| Reconcile recent merged PRs #163–#170 | DONE_VERIFIED | GitHub merged-PR search confirms #163, #164, #165, #167, #168, #169 and #170 merged; #166 is closed unmerged duplicate |
| Identify open PR conflict | DONE_VERIFIED | Open-PR search identifies #145; proposal conflicts with deterministic-default contract |
| Preserve historical branches and PRs | DONE_VERIFIED | No branch deletion, force update, PR closure or blind merge performed |
| Preserve and clarify documentation architecture | DONE_VERIFIED | Existing structure guide retained; current audit and navigation pointers added |
| Integrate every historical branch's unique file delta | PARTIAL | Branch metadata comparison is complete; not every old branch's full file-level diff and test behavior has been independently reviewed. Acceptance: a concrete missing requirement is identified, diff reviewed, ported to the single integration line, and exact-head checks pass |
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
- A fresh open-PR inventory leaves only PR #145. It remains BLOCKED pending an owner-level neural-first CLI/Python architecture decision; no rebase or merge was performed.

The new profile-specific ALA-LC source crosswalk is DONE_VERIFIED for the scoped LOC Notes 1, 2 and 4 behavior. Full contextual ALA-LC conformance remains PARTIAL; unsupported initial `ʻ`, medial `w` clusters, other vowel sequences, word/loanword boundaries and specialist review remain outstanding.

**Current main:** `72e9677b0dd4fc863c90d4cec773731fb451109a`.  
**Readiness:** engineering-verified partial research prototype; not a linguistically validated universal converter. Independent adjudicated IPA gold remains 0.
