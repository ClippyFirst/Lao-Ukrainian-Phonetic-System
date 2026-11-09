# Agent instructions

This file is the project-specific entry point for coding agents. It complements, rather than replaces, the canonical project documents.

## Agent context files

- Read [GLOSSARY.md](GLOSSARY.md) for project vocabulary before designing interfaces or naming tests.
- Read [docs/agents/issue-tracker.md](docs/agents/issue-tracker.md) before creating or updating issues.
- Read [docs/agents/codebase-map.md](docs/agents/codebase-map.md) to trace the verified entry points, data flow, high-risk seams and test commands; re-check source when code changes.

## Read before changing the project

1. Read `docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md` first. It is the canonical task ledger and handoff. Continue its unfinished work; do not create a competing plan or repeat completed work.
2. Read the relevant parts of `docs/PRODUCT-REQUIREMENTS.md`, `docs/methodology.md`, `docs/system-specification.md`, `docs/limitations.md`, `docs/decision-log.md`, `docs/sources-and-evidence.md`, and `docs/final-audit.md`.
3. Inspect the current `main` head, recent commits, open and recently closed PRs, relevant branches, and the latest workflow runs before editing. Compare old branches to current `main`; do not assume that a branch is either reusable or disposable from its name.
4. Read the complete code path being changed, including callers, consumers, tests, fixtures, generated files, workflows, and documentation.

## Engineering method

- Prefer the smallest complete change. Reuse the existing module, data structure, test seam, and project convention before adding another abstraction, dependency, option, wrapper, or configuration layer.
- Read before simplifying. A shorter diff is not better if it weakens correctness, error handling, validation, evidence, accessibility, or the user's requested behavior.
- Design around the public interface and test observable behavior at that seam. Keep expected values independent from the implementation. Avoid tests that only mirror internal code or mocks that bypass the behavior under test.
- For behavior changes and bug fixes, use test-first development: write one focused regression test, observe the expected failure, make the minimum change, then run the focused test and the full relevant suite. Configuration-only and generated-file changes may use the repository's CI contract instead.
- For bugs, reproduce the actual symptom and trace it to its source before changing code. Do not patch a downstream symptom or combine unrelated fixes.
- Review beyond the diff: callers, input/output contracts, edge cases, data flow, generated artifacts, Python/browser parity, accessibility, and expected deployment behavior.
- Do not add dependencies unless a concrete requirement cannot be met by existing code, the standard library, or the platform. Explain the need and maintenance cost before adding one.
- Record intentional limitations with an explicit status and revisit trigger. Do not turn a known unsupported case into a guessed result.


- For new or ambiguous work, establish the intended outcome, audience, why and observable success criteria before designing; inspect existing project context first. Ask only questions whose answers would materially change the deliverable. Do not add process or intermediate-approval gates when the user has explicitly authorized autonomous one-pass execution.
- At GREEN, run the repository's full project test command even if the task named only a focused test file. Report every failure observed; a focused passing test is not a green project suite.

## Linguistic and data invariants

The primary pipeline is:

`Lao source orthography → structural analysis → source-language phonology → IPA → Ukrainian target adaptation → Ukrainian practical orthography`.

- IPA is the inspectable adapter between Lao phonological analysis and Ukrainian adaptation. Do not generate the primary Ukrainian phonetic result independently from source graphemes.
- The default service method remains IPA-first. The optional romanization method is separate, lower-information, source-aware, and must not be described as phonetic equivalence.
- Preserve tone, length, syllable structure, provenance, uncertainty, warnings, and analysis status. Never silently guess unsupported pronunciations.
- Distinguish project policy from established Lao phonology and from an official Ukrainian standard. Do not invent sources, IPA, lexical examples, benchmark scores, accuracy, or licensing permissions.
- Shared regression fixtures are engineering tests, not an independently adjudicated gold corpus. Keep empirical accuracy null while independent gold is absent.
- Canonical linguistic registries live in `data/lao/*.csv`. Regenerate `web/data.js` with the project generator; do not hand-edit generated data. Keep Python and browser behavior aligned through shared fixtures and parity tests.
- In the Vientiane-oriented tone model, written tone-mark selectors apply only to live/open syllables. `mai ti` (`໊`) and `mai catawa` (`໋`) are rare and restricted to middle-class onsets in the documented reference.
- Do not infer live/dead class from the `length` label alone: use canonical `nucleus_type` and `coda_class` as well. Open diphthong rhymes and the nasal-final `AM` rhyme are live; a stop coda remains dead. Preserve phonetic IPA length independently from this structural classification.
- The shared tone fixture is consumed by both Python and browser suites. Extend it when changing tone selectors, vowel rhyme classification, or cross-runtime behavior.
- Validate tone-mark storage order before stripping marks: a mark follows the base onset or superscript vowel sign (or the second character of a documented onset sequence), follows any combining vowel sign, and precedes the spacing AM letter. Malformed positions must withhold IPA, tone, and target output in both runtimes; use the shared `tests/fixtures/tone_mark_order_cases.json` fixture.

## Verification commands

Run the checks relevant to the change. For a release-level engineering check, run all of these:

```bash
python scripts/audit.py
PYTHONPATH=src python -m unittest discover -s tests -v
npm test
npm run build
git diff --exit-code -- web/data.js
```

Inspect the built `dist/` output and relative asset paths when the web build changes. A successful CI run proves only the engineering checks it actually ran. It does not establish linguistic accuracy, expert adjudication, visual QA, or accessibility unless those checks are explicitly present.

## Branches, reviews, and handoff

- Start from the latest `main` on a clearly named task branch. Keep changes focused and commits coherent.
- Inspect open and closed PRs and compare relevant branches before porting work. Reuse merged work; do not resurrect superseded patches without a demonstrated missing behavior.
- Do not force-push, delete existing user branches, merge blindly, publish a release, or change repository settings.
- Before merging, review the full change against the originating requirement and repository standards. Fix material findings and run fresh verification on the exact final head.
- Update the existing master handoff, audit, and validation documents in place. Keep task status evidence-based: `DONE_VERIFIED` only after the required implementation and current verification evidence exist; otherwise use `PARTIAL`, `BLOCKED`, `TODO`, or `DEFERRED`.
- In the final report, state what was checked, what was not checked, exact verification evidence, unresolved blockers, and any risk that remains.

## Adopted engineering references

These are methodological references, not runtime dependencies. The project adopts selected practices, not wholesale copies of external instructions.

- [obra/superpowers](https://github.com/obra/superpowers/tree/22f0b463e7a5e579904dd6211a520321035526f7): skill-triggered workflow, explicit plans, test-first implementation, root-cause debugging, review, and evidence before completion.
- [mattpocock/skills](https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d): deep modules and clear interfaces, test seams, behavior-focused tests, and source-backed research.
- [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail/tree/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846): Ponytail current main: trace the real code path and data flow, map entry points and expected load before repository-level audit, review beyond the diff, preserve trust-boundary validation/data-loss handling/accessibility, test branching/parser/security logic, and report skipped checks and residual risk.

When these references conflict with this file, the existing project requirements, or the user's explicit instructions, follow the project requirements and user instructions. Do not import or install these repositories as project dependencies merely to follow their methods.

## Adopted UI/UX reference

- [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/b7d5353e0130feb8c5574ef1251f8a1db1873ccb): selected web-appropriate guidance for accessibility-first review, semantic controls, keyboard/focus behavior, text contrast, responsive layout, form feedback, reduced motion and target sizing. Use its web-specific quick reference; do not transfer native-only pt/dp rules to CSS pixels. The project's [DESIGN-SYSTEM.md](docs/DESIGN-SYSTEM.md) remains the source of truth and already specifies 44px control targets. Do not import the skill's search CLI, datasets or generated token system as runtime dependencies.

## Methodology source refresh — 2026-11-02

The adopted engineering references were checked against current upstream revisions without importing them as runtime dependencies:

- Superpowers 7.0.2: `obra/superpowers@22f0b463e7a5e579904dd6211a520321035526f7` — explicit plans, true RED/GREEN TDD, systematic debugging, code review, and verification-before-completion. Selected v7.0.2 refinements adopted here: run the repository's full test command at GREEN even when the task names one test file; establish intended outcome/audience/why before designing ambiguous new work; ask only questions that can change the deliverable. Do not impose intermediate approval gates when the user has explicitly authorized one-pass execution.
- mattpocock/skills release v1.3.2: `d1478fcb140db0b93c0c8df17bcfd311844749d0`; current main snapshot: `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d` — composable skills, source-backed research, test-first implementation, and two-axis review (spec compliance separately from repository standards).
- Ponytail 5.3.3: `7801d061243d7b753bad0e0b3c057cd250b11755` — codebase/data-flow audit, connected-code review, minimal complete changes, and explicit preservation of security, data integrity, and accessibility.

These references guide the method; project-specific linguistic, provenance, privacy, rights, and fail-closed requirements remain authoritative.


- Keep the restricted labialized onset inventory in `data/lao/onset_clusters.csv` and generate its browser mirror; do not hard-code a second divergent list. Preserve the superscript `ʷ` at the IPA boundary, reject clusters before rounded nuclei, and withhold overlapping `Cວາ` analyses rather than guessing between labialized-onset + AA and UO-long-open. Do not invent Ukrainian correspondences for these IPA sequences. Search for silent high-class `ຫ` digraphs after any preposed vowel, not only at token index zero. Extend `tests/fixtures/onset_cluster_cases.json` when adding a cluster or a boundary exception; Python and browser tests must consume the same cases.


## Methodology source refresh — 2026-11-04

- Rechecked all four upstream references. Unlazy remains at `16671491f6679ad9378f52604d3bc2415b4120c7`; mattpocock/skills at `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`; Ponytail at `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846`.
- Superpowers v7.0.2 was reviewed against v7.0.1. Adopted full-suite verification at GREEN and intent-first design with fewer, outcome-changing questions. Did not import harness plugins, helper scripts or the SDD runtime. The default explicit design-approval ceremony is not imposed when a user has already authorized autonomous one-pass execution.

## Whole-message adversarial benchmark requirements

Every parser, romanizer, phonetic adapter, CLI and browser change that can affect user text must be exercised at the complete-message boundary, not only with isolated syllables. Extend the existing canonical fixtures; do not create a parallel corpus.

- Include realistic mixed messages with multiple supported units, unsupported/foreign-script units adjacent to supported ones, ASCII and native numerals, punctuation, ordinary and repeated whitespace, tabs, LF/CRLF, and relevant Unicode format controls. Add script-extension characters that belong to a broader Unicode block but not to the target language inventory.
- Include malformed and ambiguous sequences, combining-mark order variants, repeated/illegal modifiers, long messages, and paired minimal contrasts. Each case must state the exact property under test and expected local/global status.
- Assert that every source unit is represented or explicitly marked unsupported; never silently delete, normalize away, reorder or merge source material. Verify reconstruction under the repository's declared normalization contract, including source spans and separator preservation where the API exposes them.
- An unsupported unit must not erase or downgrade valid neighboring units unless the public contract explicitly requires whole-input rejection. Check both local and aggregate status.
- Run the same canonical cases through Python and browser/service entry points wherever both exist. Keep runtime-specific expected shapes separate while sharing the input and semantic contract.
- Maintain separate datasets for (1) Unicode/source-integrity probes, (2) structural/phonological regression cases, and (3) independently adjudicated lexical IPA gold. Only the third may enter accuracy denominators; never infer IPA or Ukrainian output for adversarial cases without a scoped, source-located reference.
- For external G2P comparisons, pin engine/version/model/profile, retain immutable raw output and errors, record mapping/model/data hashes and license provenance, and score only on held-out independent gold. Inter-engine agreement and successful execution are diagnostics, not correctness.

Before accepting a new adversarial fixture, review whether its expected result is independent of the implementation and whether the test would fail if a source unit were dropped, a boundary changed, or uncertainty were silently converted into a confident output.


## Review and evidence refinements

- Separate final review into (1) specification/acceptance compliance and (2) repository standards, conventions, and maintainability. Read applicable `CONTRIBUTING.md`, coding-standards files, and adjacent patterns before judging style; do not let a standards review weaken explicit product or linguistic requirements.
- A RED result is valid only when the intended assertion fails for the intended reason. If using mutation-based diagnosis, inspect the diff against a pristine baseline and confirm the mutation actually changed the relevant code; a no-op edit is not evidence.
- Before filing issues or preparing PRs, follow repository templates and identify the filer accurately. Never present agent-generated text as human-authored; leave owner-authored sections for the owner.
- Do not force-remove a worktree or discard untracked files to make cleanup succeed. Inspect the files and preserve, relocate, commit, or delete them only with explicit owner direction.


## Methodology application — 2026-11-02

The repository now keeps its own domain glossary, GitHub issue-tracker instructions and source-verified codebase map under version control. Use these as context for the composable engineering skills; do not install external repositories as runtime dependencies or duplicate their whole skill trees. Apply Superpowers for scoped plans, RED/GREEN TDD and verification; apply Matt Pocock's codebase-design, research and two-axis review principles; apply Ponytail's real-flow audit, minimal complete change and residual-risk reporting. Linguistic evidence, corpus rights and fail-closed contracts always take precedence.


## Completion gates and task decomposition — 2026-11-04

The project also adopts selected completion-discipline practices from [Leonxlnx/unlazy](https://github.com/Leonxlnx/unlazy/tree/16671491f6679ad9378f52604d3bc2415b4120c7), reviewed at upstream commit `16671491f6679ad9378f52604d3bc2415b4120c7` (source reports 2.1.0; the inspected main snapshot is pinned here for reproducibility). This is a methodology reference, not an installed tool or runtime dependency.

- Before a substantial change, turn each acceptance-changing requirement into an observable ledger item. Reuse the canonical master handoff and existing completion register; do not create a competing task ledger.
- A runnable acceptance item names the exact command or hosted workflow, the expected result, and the evidence location. A manual item names the reviewer/evidence required and remains open until that evidence exists.
- Decompose only along real dependency and file-ownership boundaries. Do not parallelize overlapping writes or invent agent handles, branches, test results, or review evidence. Keep checks sequential unless independence and isolation are demonstrated.
- Re-run the relevant checks on the exact final commit, including checks previously marked complete when their inputs or dependencies changed. A previous green run is not evidence for a later tree.
- Distinguish implementation success from terminal handoff: an external blocker may be precisely documented, but it must never be represented as a successful acceptance gate.
- Review every command and script before execution. A declared command is not safe merely because it appears in a ledger; it runs with the available environment and permissions.

The existing repository status vocabulary remains authoritative: `DONE_VERIFIED`, `PARTIAL`, `TODO`, `BLOCKED`, and `DEFERRED`. Do not copy Unlazy's checker, hooks, approval store, or orchestration runtime into this project without a demonstrated need; the current GitHub Actions, canonical handoff and test infrastructure remain the source of execution evidence.


## External engineering/design reference re-check — 2026-11-07

The five user-supplied repositories were rechecked as methodology references; they are not project dependencies and their skill trees, hooks, scripts or orchestration runtimes must not be copied wholesale.

- [unlazy](https://github.com/Leonxlnx/unlazy): current source describes 2.1.0; the README says this is not identified as a tagged GitHub release. Use its acceptance-ledger, observable-oracle and re-verification ideas, but retain this repository's existing handoff/status vocabulary and do not install its checker.
- [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill): `skill.json` reports 2.15.0. Use targeted UX/accessibility guidance where relevant; the project's own `docs/DESIGN-SYSTEM.md`, product requirements and research-first visual direction remain authoritative.
- [obra/superpowers](https://github.com/obra/superpowers/releases/tag/v7.0.2): v7.0.2. Retain test-first work, root-cause debugging, code review and verification-before-completion.
- [mattpocock/skills](https://github.com/mattpocock/skills/releases/tag/v1.3.2): v1.3.2. Retain deep modules, explicit interfaces, behavior-focused tests, source-backed research and two-axis review.
- [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail/releases/tag/v5.3.3): v5.3.3. Retain codebase/data-flow mapping, connected-code review, reuse before adding abstractions and explicit residual-risk reporting.

These practices supplement, but never weaken, the project's Lao evidence, typed-IPA, source-rights, privacy, fail-closed and exact-head verification requirements. Recheck upstream versions before future adoption; mutable main-branch versions must not be treated as immutable pins.

## Upstream methodology reference revalidation — 2026-11-09

The five owner-supplied repositories were rechecked against their current upstream `main` commits and root `LICENSE` files. All five inspected root licenses are MIT at these snapshots; this does not establish rights for separately licensed datasets, embedded assets, submodules, dependencies, or third-party material.

- [Leonxlnx/unlazy](https://github.com/Leonxlnx/unlazy/tree/16671491f6679ad9378f52604d3bc2415b4120c7) — current source README targets 2.1.0 but does not identify it as a tagged GitHub release. Adopt the acceptance ledger, explicit observable gates, evidence review and re-verification discipline. Do not copy its checker, hook, approval store or orchestration runtime.
- [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/4f2dbb67e64969a9a30ab00742f2d55d66ddec2b) — current web UX reference. Use relevant accessibility, semantic-control, keyboard/focus, contrast, responsive-layout, feedback and reduced-motion guidance. Do not import its CLI, generated token system or datasets; native pt/dp guidance is not a CSS-pixel requirement.
- [obra/superpowers](https://github.com/obra/superpowers/tree/22f0b463e7a5e579904dd6211a520321035526f7) — v7.0.2 snapshot. Retain genuine RED/GREEN test-first work, systematic debugging, review and verification-before-completion.
- [mattpocock/skills](https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d) — current main snapshot. Retain composable instructions, deep modules, explicit interfaces, behavior-focused tests and source-backed research.
- [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail/tree/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846) — current main snapshot. Retain whole-flow/code-path tracing, connected-caller review, trust-boundary and data-integrity checks, and explicit residual-risk reporting.

These are methodology references only. No upstream code, skills, datasets, assets, CLI, hooks, workflow or runtime dependency was copied or installed. Project-specific linguistic evidence, typed IPA, source-rights, privacy, fail-closed and release requirements remain authoritative.
