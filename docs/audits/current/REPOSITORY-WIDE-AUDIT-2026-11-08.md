# Repository-wide audit and documentation/structure refresh — 2026-11-08

## Executive assessment

**The repository is an engineering-verified, published research prototype. It is not linguistically validated and is not release-ready.** The existing top-level structure is coherent; this audit therefore preserves it and corrects stale documentation/ownership descriptions rather than introducing a competing architecture or moving large numbers of files.

- Repository: `ClippyFirst/Lao-Ukrainian-Phonetic-System`
- Default branch: `main`
- Audited starting HEAD: `c0d7218da907dbe0bae6cadb42824ca0cd09b83a`
- Working branch for this refresh: `audit/docs-architecture-refresh-20261108`
- Working branch was created from the exact audited `main` SHA above.
- Exact-main Verify: [#42463921672 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42463921672), run on the same `c0d7218...` SHA.
- Mainline test counts from the workflow log: **262 Python, 126 Node, 17 Chromium**.
- GitHub Pages deployment: [#42463361038 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42463361038); the live site was checked after deployment and returned HTTP 200.
- Repository license: MIT. This applies to repository-owned material only; it does not grant rights to third-party corpora, model data or copied source material.

This is a repository/engineering/documentation/CI/reference-practice audit. It is not an expert Lao phonology adjudication, legal opinion, penetration test, or manual assistive-technology certification.

## 1. Repository structure and architecture

The current structure is intentionally retained. The project already separates implementation, canonical data, provenance, generated assets, schemas, tests, scripts, research and documentation.

| Concern | Canonical location | Responsibility |
|---|---|---|
| Python package | `src/lao_ukrainian/` | Normalization, parsing, phonology, typed IPA, Ukrainian adaptation, CLI and optional neural adapter |
| Browser implementation | `web/` | Native ES modules, deterministic engine, UI, separate romanization route and CSS |
| Public pages | `index.html`, `system.html` | Local-first converter and methodology page |
| Canonical language data | `data/lao/*.csv` | Lao grapheme/phonological registries and target correspondences |
| Provenance | `data/evidence/` | Source registry and claim evidence |
| Derived data | `data/derived/` | Reproducible derived correspondence data |
| Benchmarks and gold | `data/benchmark/` | Gold-corpus lifecycle, rights metadata, splits and aggregate benchmark records |
| Contracts | `schemas/` | Analysis, comparative and IPA-gold schemas |
| Tooling | `scripts/` | Audits, corpus validation, generators, build and benchmark diagnostics |
| Tests | `tests/`, `web/engine.test.js` | Python, Node, browser, fixtures and built-site checks |
| Documentation | `docs/`, `AGENTS.md`, `GLOSSARY.md`, `CONTRIBUTING.md` | Specification, evidence, limitations, decisions, audits, handoff and contributor/agent guidance |
| Automation | `.github/workflows/` | Verify, Pages deployment, optional external G2P and benchmark workflows |

### Architecture decision

Do not migrate the repository into an invented monorepo layout, add a frontend framework, introduce a second documentation home, or vendor complete external agent-skill trees. Those changes would add maintenance and review cost without solving an identified acceptance gap.

Keep these boundaries authoritative:

1. `data/lao/*.csv` is canonical; generated browser data is not edited by hand.
2. `data/evidence/` owns source/claim provenance.
3. `schemas/` owns machine-readable contracts.
4. `src/lao_ukrainian/` and `web/` are separate runtimes with shared semantic fixtures where justified.
5. `docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md` remains the single canonical execution ledger.
6. `docs/audits/current/` contains current snapshots; dated research reports remain immutable historical evidence.

### Accepted phonetic pipeline

`Lao orthography → structural analysis → source-language phonology → typed IPA → Ukrainian target adaptation → Ukrainian practical orthography`.

Typed IPA is the actual adapter boundary. The optional CLDR/BGN-oriented romanization route is lower-information and separate; it cannot reconstruct tone and is not a fallback for failed phonetic analysis. The grapheme preview is explicitly provisional, tone-free and excluded from accepted Ukrainian adaptation.

### Runtime state on the audited mainline

- Python CLI: deterministic `rules` is the default; MekongPhon tonal/non-tonal inference is opt-in.
- Browser Pages application: browser-native deterministic JavaScript; it does not run Python/PyTorch.
- Optional neural path: pinned model revisions, raw IPA/model provenance and fail-closed typed IPA mapping.
- A neural-first CLI/Python proposal exists in PR #145. It is not merged into the audited mainline. Even if PR #145 merges, its own scope says Pages remains deterministic until a separate inference backend exists.

## 2. Source tree and documentation quality

The tree contains distinct areas for:
- top-level project entry and contribution documents;
- canonical linguistic data and evidence registries;
- research/benchmark reports and current audits;
- schemas and corpus validation;
- Python and browser runtime code;
- unit, integration, browser and shared-fixture tests;
- CI workflows and static-site deployment.

The existing docs index already establishes document precedence. The key correction required was temporal: the prior 2026-11-08 audit and code map still described PR #143 as open and `main` as unchanged, although PR #143 had since been merged. The current audit, code map and validation header are refreshed against the actual mainline SHA and current PR topology.

No broad file move was justified. Preserve the existing `docs/research/`, `docs/audits/current/`, `docs/agents/` and `docs/superpowers/` distinctions.

## 3. Branch, PR and issue reconciliation

### Merged work

- PR #143 — [Integrate Lao G2P, IPA target adapter, grapheme preview, and repository audit](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/143) — **merged** into `main` as `c3ba58c0e0e6ba64821abe4c9d46c75ff559b2b4`.
- Pages deployment [#42463361038](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42463361038) succeeded after that merge.
- Do not re-port the work already integrated by #143.

### Open PRs

| PR | Head | Base | State/evidence | Disposition |
|---|---|---|---|---|
| [#145 neural-first G2P](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/145) | `feat/mekongphon-first-stage` at `a70769d7005e40e15b68a3df181cadbfa4cce51f` | `main` at audited baseline | Open, mergeable; exact-head Verify [#42465535231 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42465535231); neural benchmark [#42465378241 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42465378241) | Leave untouched. It changes Python/CLI default semantics; review separately. Its static Pages limitation remains explicit. |
| [#146 deterministic reference profile](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/146) | `feat/deterministic-mekongphon-reference-profile-20261108` at `ad5bf2a61480ea255a9b83ca6f662471d7606e84` | `main` | Open, draft, mergeable; Verify [#42467552887 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42467552887) on checkpoint `8e24c6516f955d201efeb21e523efc63e4fe86b6`; current head `ad5bf2a61480ea255a9b83ca6f662471d7606e84` is one workflow-only commit ahead. Held-out benchmark [#42467190935 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42467190935) ran on a separate earlier checkpoint. | Leave untouched. It adds an opt-in deterministic profile; the current head needs a fresh exact-head Verify before merge. Its benchmark is dictionary-seeded comparator evidence, not independent gold. |
| [#147 HVULao 1k three-engine stress benchmark](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/147) | `benchmark/hvulao-1k-three-engine-20261108` at `f3b8b3b7b919c3a32bd66ea8972f87461a82411e` | PR #146 branch, not `main` | Open, draft, mergeable; Verify [#42490019054 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42490019054); benchmark [#42490023554 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42490023554) | Leave untouched. It is stacked on #146 and must not be treated as a standalone mainline change. Its raw text corpus has segmentation/POS annotations, not IPA. |

PRs #145 and #146 are parallel proposals against the same `main` baseline and touch overlapping project contracts/documentation. They require an explicit integration/rebase order and a review of their combined semantics before merging. PR #147 depends on #146. Do not merge #147 directly to `main` or silently rebase/retarget any of these PRs.

PRs #137–#142 remain open as older stacked proposals. Their work was consolidated through merged PR #143. They were not deleted, closed, retargeted or force-pushed in this audit; do not blindly merge or replay them. The new documentation-only branch does not depend on these old branch heads.

### Open issues

- [#99 — recruit experts and run the first blind Lao IPA gold pilot](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/issues/99): still the real external/human dependency for independent gold.
- [#9 — compare Lao-to-IPA output against an independent G2P baseline](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/issues/9): comparator research; do not confuse baseline agreement with adjudicated accuracy.

The repository API reports 11 open issue-count items including pull requests; the current open issue collection contains these two non-PR issues.

## 4. Five supplied engineering references

All five repositories were inspected at their current upstream `main` commits on 2026-11-08. Their root `LICENSE` files declare MIT at the inspected snapshots. This confirms the stated license of those repositories, not the license of third-party material embedded in their data, examples, fonts, screenshots or transitive assets.

| Reference and inspected commit | Relevant practice | Adoption decision |
|---|---|---|
| [Leonxlnx/unlazy](https://github.com/Leonxlnx/unlazy/tree/16671491f6679ad9378f52604d3bc2415b4120c7) — `16671491f6679ad9378f52604d3bc2415b4120c7` | Acceptance ledger, observable oracles, explicit command/expectation/evidence, re-verification | Reuse the existing master ledger/status vocabulary and CI. Do not copy its checker, hooks, approval store or orchestration runtime. Upstream README describes 2.1.0 source and says it is not identified as a tagged GitHub release. |
| [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/4f2dbb67e64969a9a30ab00742f2d55d66ddec2b) — `4f2dbb67e64969a9a30ab00742f2d55d66ddec2b` | Accessibility-first audit, keyboard/focus, contrast, form feedback, responsive layout, reduced motion and platform-specific interaction | Apply web-specific checks to the existing editorial linguistic instrument. Keep `docs/DESIGN-SYSTEM.md` authoritative; do not import its CLI, datasets, generated token system or generic SaaS templates. Do not mix native pt/dp rules with CSS px/WCAG requirements. |
| [obra/superpowers](https://github.com/obra/superpowers/tree/22f0b463e7a5e579904dd6211a520321035526f7) — `22f0b463e7a5e579904dd6211a520321035526f7` | True RED/GREEN TDD, plan-before-implementation, root-cause debugging, review and verification-before-completion | Already represented in `AGENTS.md` and `CONTRIBUTING.md`; retain selectively, without adding its plugin/harness runtime. |
| [mattpocock/skills](https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d) — `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d` | Composable skills, deep modules, explicit interfaces, behavior-focused tests, source-backed research and two-axis review | Retain the existing domain glossary, codebase map and focused contributor instructions; do not copy a duplicate skill tree or force an issue-tracker setup process. |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail/tree/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846) — `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846` | Trace actual data flow, review connected code, minimize changes without cutting safety/tests, report residual risk | Apply to code/data-flow reviews and acceptance boundaries. Do not adopt benchmark marketing claims or install the runtime. |

**Result:** methodology adoption is sufficient and already mostly encoded in `AGENTS.md`. No new runtime dependency, vendored source, generated skill directory or duplicate agent framework is justified.

## 5. Build, dependency and CI contract

- Python package requires Python >=3.10; hosted Verify uses Python 3.12.
- Browser/test tooling requires Node >=22.14.0.
- `package-lock.json` pins Playwright test tooling; use `npm ci --no-audit --no-fund`, not an unconstrained `npm install`, for clean verification.
- `npm test` runs Node suites; `npm run build` regenerates browser data then builds static pages; `npm run test:browser` runs Playwright Chromium.
- `npm run check:release` is a web-only convenience sequence; it does not replace Python, corpus, source-rights or manual QA checks.
- No Vite/Webpack/frontend framework is present or required. The current site is a small static native-ES-module application.
- GitHub Pages deployment is already active and has a successful post-merge deployment.

### Exact-main engineering evidence

Verify [#42463921672](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42463921672) ran on the audited main SHA `c0d7218da907dbe0bae6cadb42824ca0cd09b83a` and succeeded.

| Gate | Result |
|---|---|
| IPA gold corpus structural validation | PASS; 0 records, status `NOT_READY_NO_ADJUDICATED_GOLD` |
| Repository data/evidence audit | PASS; 83 Lao-block graphemes, 43 consonant rows, 11 onset clusters, 34 vowel rows, 17 tone rules, 1 special tone rule, 70 Ukrainian mappings, 38 sources, 53 claims |
| Python unittest discovery | PASS — 262 |
| Optional external-G2P harness syntax/CLI | PASS |
| Locked Node install | PASS — `npm ci --no-audit --no-fund` |
| Node suites | PASS — 126 |
| Static build / generated browser data | PASS |
| Generated-data reproducibility | PASS — no `web/data.js` drift |
| Playwright Chromium | PASS — 17 |
| Built pages / relative assets | PASS |

The separate Pages run #42463361038 also passed deployment/artifact and deployed-asset smoke checks. These are engineering and publication checks, not evidence of expert phonetic accuracy or manual accessibility certification.

## 6. Evidence and linguistic status

- The primary project pipeline remains Lao orthography → structural analysis → source phonology → typed IPA → Ukrainian adaptation.
- Tone, length, syllable structure, provenance, uncertainty and warnings must remain inspectable.
- The target correspondences are project policy, not an official Ukrainian national standard.
- Romanization is separate and lower-information.
- The provisional grapheme preview is not accepted IPA and cannot produce the accepted Ukrainian result.
- MekongPhon inference is model output with its own revision/provenance; the owner has confirmed project rights for the authorized use, but this is not an independent legal opinion.
- The 100-word dictionary-seeded benchmark and the 1,000-row HVULao sentence stress test are not independent IPA gold. The latter has segmentation/POS labels only.
- The benchmark #147 result on its own stacked branch is a coverage/runtime/output-disagreement stress test. It does not provide IPA accuracy, CER against gold or correctness.

### Gold corpus

The four JSONL gold-lifecycle files are intentionally empty; `gold.tsv` is header-only. The gold corpus remains 0 adjudicated records. The release gate should continue to report `NOT_READY_NO_ADJUDICATED_GOLD`.

### Remaining acceptance blockers

1. **Independent IPA gold — BLOCKED.** Acceptance requires a source/rights-approved target variety and IPA convention, rights-eligible source-located records, two qualified independent annotators through controlled blind intake, a separate qualified adjudicator, frozen lexical-group-disjoint splits, and a specialist-reviewed contrast-coverage report.
2. **Manual accessibility — PARTIAL.** Automated 17 Chromium checks do not substitute for NVDA/JAWS/VoiceOver/TalkBack, physical iOS/Android devices, actual 200%/400% browser zoom, deployed keyboard-only walkthrough and human contrast/visual review. Record evidence in `docs/accessibility-manual-qa.md`.
3. **Linguistic review — BLOCKED / evidence-limited.** Qualified Lao specialist review remains necessary for disputed tone/rhyme rules, dialect scope, rare clusters, loanwords, conventional names, Pali/Sanskrit and Khmu.
4. **Neural-first web delivery — DEFERRED / separate deployment.** PR #145 explicitly does not provide a browser inference backend. If the owner later chooses neural inference for Pages, it needs a separately scoped service, privacy/security review, availability/cost model and UI contract; this is not silently added here.
5. **Neural-first CLI proposal — PARTIAL at repository level.** PR #145 branch implementation is exact-head verified but is not merged into `main`; acceptance for mainline requires review/integration and a new mainline exact-head Verify.
6. **Reference profile / 1k benchmark — PARTIAL at repository level.** PR #146/#147 are verified on their own branches but remain unmerged and stacked. Acceptance requires ordered integration and final combined verification; no linguistic gold claims are added.

## 7. Task ledger for this refresh

| Task | Status | Evidence / acceptance |
|---|---|---|
| Inspect mainline metadata, tree, README, docs, schemas, tests, workflows and build configuration | DONE_VERIFIED | Main SHA `c0d7218...`; recursive tree and canonical files inspected |
| Inspect recent commits and current exact-main workflow | DONE_VERIFIED | Commit history and Verify #42463921672 inspected |
| Inspect open PRs and branch dependencies | DONE_VERIFIED | PRs #137–#147 and their base/head relationships checked; #143 merge verified |
| Inspect open issues | DONE_VERIFIED | #99 blind IPA gold pilot; #9 external G2P comparison |
| Inspect five user-supplied upstream repositories | DONE_VERIFIED | Current main SHAs, README/skill references and root MIT license files checked |
| Preserve coherent repository structure | DONE_VERIFIED | No broad migration or dependency/framework added |
| Refresh codebase map and stale current audit | DONE_VERIFIED | Exact-head Verify [#42496670248 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42496670248) on `a8f6eedb33da005ecc005ea25dc729daa152baf3` — 262 Python, 126 Node, 17 Chromium; audit, corpus, clean install, build and generated-data gates passed |
| Refresh validation authority and master handoff | DONE_VERIFIED | Exact-head Verify [#42496670248 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42496670248) on `a8f6eedb33da005ecc005ea25dc729daa152baf3` — all configured repository checks passed |
| Manual accessibility QA | PARTIAL | Requires human/device sessions |
| Independent IPA gold | BLOCKED | 0 adjudicated records; specialist and blind annotation dependencies |
| Mainline neural-first CLI | PARTIAL | PR #145 not merged |
| Mainline deterministic profile and HVULao benchmark | PARTIAL | PR #146 Verify is one workflow-only commit behind its current head; #147 is verified on its own head but remains stacked on #146 |

## 8. Commands and verification performed in this audit session

This session used authenticated GitHub repository inspection and hosted workflow evidence. It did not have a local checkout or local shell, so no local Python/npm commands are claimed as executed.

Inspected:
- repository metadata, recursive `main` tree and recent commits;
- README, AGENTS, CONTRIBUTING, codebase map, docs index, audits index, validation guide, web architecture, design system, master handoff and IPA gold contract;
- Python CLI/core/neural adapter source and package/build configuration;
- open PR metadata/diffs, branch topology, open issues and workflow run/job logs;
- five upstream README and root LICENSE files; UI UX Pro Max skill and web quick-reference files.

Hosted checks actually inspected:
- main Verify #42463921672 — SUCCESS on exact main SHA, 262 Python / 126 Node / 17 Chromium;
- Pages deployment #42463361038 — SUCCESS;
- PR #145 Verify #42465535231 and neural benchmark #42465378241 — SUCCESS;
- PR #146 Verify #42467552887 and benchmark #42467190935 — SUCCESS;
- PR #147 Verify #42490019054 and benchmark #42490023554 — SUCCESS.

These PR runs are evidence for their own branch heads only. They are not evidence that their changes are merged into main. This documentation branch also passed exact-head Verify [#42496670248 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42496670248) on `a8f6eedb33da005ecc005ea25dc729daa152baf3` (262 Python, 126 Node, 17 Chromium); the resulting final handoff-only commit is checked separately by the PR status run.

## 9. Readiness

**Published engineering-verified research prototype; not release-ready or linguistically validated.** Mainline engineering and deployment checks are green. The principal blockers are still independent adjudicated IPA gold (0 records), qualified linguistic acceptance and manual accessibility/device QA. The outstanding PRs must be integrated in dependency order and verified on the resulting exact mainline head; their branch-level green checks do not replace that gate.
