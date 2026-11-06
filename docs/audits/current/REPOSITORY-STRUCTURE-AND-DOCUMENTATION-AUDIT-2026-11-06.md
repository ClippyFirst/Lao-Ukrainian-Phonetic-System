# Repository structure and documentation audit — 2026-11-06

## Executive result

**Engineering state: reproducible research prototype with a deployed static web instrument. Linguistic/release state: not independently validated and not release-ready.**

This review inspected the current main tree, repository metadata, branch list, recent commits, open/recently closed pull requests, current workflow run, README, agent instructions, product requirements, methodology, implementation map, audit registers, schemas/data layout, Python and browser entry points, build scripts and CI workflows. It also reviewed the five user-supplied engineering/design references for relevant practices.

This is a repository-state and documentation audit, not an independent Lao phonology adjudication, full UI/assistive-technology evaluation, or local clean-install run.

## Baseline and repository control

- Repository: ClippyFirst/Lao-Ukrainian-Phonetic-System.
- Default branch: main.
- Starting commit: 915db62c710bedcbbec6ac01c73cb9312ae9a03d.
- The branch listing returned only main; no other branch was listed in the inspected response.
- No open pull requests were returned.
- PR #136 was closed without merge as superseded. Its proposed language-specific IPA fixture correction was already on main; no duplicate patch was ported. Its source branch was not present in the branch listing, so this report does not claim that branch is preserved.
- Repository metadata reported the default branch as unprotected. No branch-protection or repository settings were changed.
- Latest baseline verification: GitHub Actions Verify run [41889580331](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41889580331), head 915db62c710bedcbbec6ac01c73cb9312ae9a03d, completed SUCCESS. Inspected steps passed: corpus-structure validation, repository data/evidence audit, Python tests, optional G2P CLI validation, browser engine tests, canonical browser-data regeneration/reproducibility, Chromium built-site tests and built-page/relative-asset checks.

## Architecture inventory

The repository has a clear separation of concerns and should retain it rather than undergo a broad directory reshuffle.

| Area | Canonical location | Responsibility |
|---|---|---|
| Python package | src/lao_ukrainian/ | Normalization, parsing, phonology, IPA target adaptation, analysis model and CLI |
| Canonical Lao data | data/lao/*.csv | Consonants, onset clusters, vowels, codas/tone and Ukrainian IPA correspondences |
| Evidence registry | data/evidence/ | Source metadata and claim-to-source links |
| Generated browser data | web/data.js | Deterministic mirror of canonical CSVs; never hand-edit |
| Browser runtime | web/ | Native ES-module engine, UI, and separate romanization route |
| Static pages | index.html, system.html | Converter and methodology page |
| Schemas | schemas/ | Machine-readable analysis and IPA corpus contracts |
| Tests | tests/, web/engine.test.js | Python, browser-engine, cross-runtime, corpus and UI regressions |
| Build/research scripts | scripts/ | Audit, generation, static build, benchmark and corpus validation |
| Current research evidence | docs/audits/current/ | Dated source and phonology workpacks |
| Execution history | docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md | Canonical ongoing task ledger and handoff |

The main phonetic path is Lao orthography → structural parser → source phonology → typed IPA → Ukrainian target adapter. The romanization path is a separate, explicitly lower-information orthographic mode. This architecture is coherent and must not be collapsed into character substitution or silent fallback.

## Findings and resolutions

| ID | Severity | Status | Finding | Resolution / acceptance |
|---|---|---|---|---|
| DOC-001 | P1 | DONE_VERIFIED after exact-head CI | web-architecture.md and PRODUCT-REQUIREMENTS.md described Vite, but package.json has no Vite dependency and scripts/build_web.py simply copies two HTML pages and web/ into dist/. | Corrected both documents and implementation notes to describe the actual framework-free native-ES-module build. |
| DOC-002 | P1 | DONE_VERIFIED after exact-head CI | The master handoff ended with a 2026-11-04 entry describing PR #130's Chromium check as still running, while main had advanced through later commits to #135. | Appended a current-main checkpoint with the exact starting head, verified CI evidence, branch/PR reconciliation and current blockers. |
| DOC-003 | P1 | DONE_VERIFIED after exact-head CI | final-audit.md was titled "Final scientific audit" but its early conclusions and limitations predate later implementation work. This could be mistaken for the current state. | Added a historical-record notice and links to the current audit index and live handoff. Historical content was retained, not silently rewritten. |
| DOC-004 | P2 | DONE_VERIFIED after exact-head CI | There was no central documentation landing page; README listed only a subset of the available research and engineering documents. | Added docs/README.md and replaced the partial README list with links to the index and canonical handoff. |
| DOC-005 | P2 | DONE_VERIFIED after exact-head CI | No root CONTRIBUTING.md existed, despite agent instructions asking reviewers to inspect contribution standards. | Added a concise contributor guide with environment requirements, exact test commands, data ownership, evidence and privacy rules. |
| ENG-001 | P1 | BLOCKED / owner action | The default main branch is not protected in the inspected repository metadata. A passing CI run therefore does not itself prevent direct unreviewed writes. | Repository owner should configure a ruleset requiring the Verify workflow and review for routine changes. This requires a repository-settings decision and was intentionally not changed here. |
| ENG-002 | P2 | TODO | No npm lockfile is present. The Playwright direct dependency is pinned, but transitive npm resolution is not frozen. | Generate and commit package-lock.json in a Node/npm-enabled clean checkout, switch CI to npm ci, and verify the exact lockfile on a clean runner. Not fabricated in this connector-only pass. |
| LAO-GOLD-001 | P1 | BLOCKED | Independent expert-adjudicated IPA gold remains empty; gold.tsv is header-only and empirical accuracy must remain null. | Requires a confirmed target profile/convention, lawful item-level source access, two independent qualified annotators, a separate adjudicator, blind intake and the versioned pilot acceptance described in the collection playbook. |
| LAO-UI-001 | P2 | TODO | CI covers Chromium flows and selected accessibility hooks, but does not establish manual screen-reader, keyboard-only, mobile-device or visual QA. | Record a human QA matrix with device/browser/AT versions, observed results and resolved defects. |
| LAO-TARGET-001 | P1 | PARTIAL / evidence-limited | Some IPA sequences (including registered labialized-onset values) intentionally have no Ukrainian target mapping; output is withheld rather than guessed. Other project correspondences still require expert review. | Add a target only with source-located phonetic evidence and documented Ukrainian adaptation rationale; never treat withheld output as a CI defect by itself. |

## Documentation and structure decisions

- Keep data/lao/ as the only canonical Lao linguistic registry; web/data.js remains generated.
- Keep evidence claims and sources machine-readable under data/evidence/.
- Keep the large master handoff as the canonical append-only execution ledger; do not split it into competing status files in this pass.
- Keep dated audits and workpacks under docs/audits/current/; historical audit prose remains linked but is not current authority.
- Use docs/README.md as the document map and docs/audits/README.md as the audit/evidence map.
- Do not rename/move implementation directories: the current package/data/test boundaries are understandable, referenced by workflows and already reflected in codebase-map documentation. A broad path migration would create link churn without solving a demonstrated architecture defect.

## External references reviewed

- [unlazy](https://github.com/Leonxlnx/unlazy): the project already adopted evidence-bound completion gates, observable acceptance criteria and exact-final-head verification in AGENTS.md; no runtime tool or copied framework was added.
- [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill): reviewed as a design-method reference. The repository's own docs/DESIGN-SYSTEM.md and product requirements already prescribe the relevant data-first, accessible, restrained visual direction. Its large generic style/rule catalog was not imported because it would duplicate local policy and risk steering the research instrument toward unrelated SaaS/marketing patterns.
- [Superpowers](https://github.com/obra/superpowers): existing agent instructions already adopt scoped planning, test-first implementation, root-cause debugging and verification-before-completion.
- [mattpocock/skills](https://github.com/mattpocock/skills): existing instructions already adopt composable engineering practices, behavior-focused tests, deep modules and two-axis review.
- [Ponytail](https://github.com/DietrichGebert/ponytail): existing agent instructions already adopt connected-code/data-flow review, minimal complete changes and explicit residual-risk reporting.

These references are methods, not dependencies. The repository's linguistic, source-rights, privacy and fail-closed requirements remain authoritative.

## Documentation-link integrity

A local-path scan was performed across the repository Markdown inventory. It found three broken relative links in the master handoff (IPA gold protocol, phonology workpack and tone–rhyme matrix); all three were corrected to paths relative to the handoff's docs/ directory. External URLs and heading-anchor existence were not exhaustively validated.

## Verification evidence and limits

- Baseline hosted Verify: [41889580331](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41889580331) SUCCESS on starting commit 915db62c710bedcbbec6ac01c73cb9312ae9a03d.
- This connector session did not provide a local repository checkout or a local Python/Node execution environment. No local test, benchmark, clean-install, package-lock generation or deployed manual QA is claimed.
- Exact-head Verify is the acceptance gate for the documentation changes. Read its result against the precise commit SHA shown in the workflow; the earlier baseline success is not a substitute for final-head verification.
- The external human-review, licensing and manual UI gates remain outside what repository CI can prove.

## Final readiness judgement

**Research-ready as an engineering and evidence-management prototype; not linguistically release-ready.** The architecture and automated engineering gate are coherent, but the empty expert gold corpus, unresolved target correspondences, external source/rights steps, manual accessibility QA and unprotected default branch prevent a production or publication-grade claim.
