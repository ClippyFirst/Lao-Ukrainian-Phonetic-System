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
