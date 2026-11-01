# Agent instructions

This file is the project-specific entry point for coding agents. It complements, rather than replaces, the canonical project documents.

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

- [obra/superpowers](https://github.com/obra/superpowers/tree/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b): skill-triggered workflow, explicit plans, test-first implementation, root-cause debugging, review, and evidence before completion.
- [mattpocock/skills](https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d): deep modules and clear interfaces, test seams, behavior-focused tests, and source-backed research.
- [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail/tree/7801d061243d7b753bad0e0b3c057cd250b11755): Ponytail 5.3.3: trace the real code path and data flow, map entry points and expected load before repository-level audit, review beyond the diff, preserve trust-boundary validation/data-loss handling/accessibility, test branching/parser/security logic, and report skipped checks and residual risk.

When these references conflict with this file, the existing project requirements, or the user's explicit instructions, follow the project requirements and user instructions. Do not import or install these repositories as project dependencies merely to follow their methods.

## Methodology source refresh — 2026-11-02

The adopted engineering references were checked against current upstream revisions without importing them as runtime dependencies:

- Superpowers 7.0.1: `obra/superpowers@2ce8aa15d05bd57213e6f746f953aafb7ded7a8b` — explicit plans, true RED/GREEN TDD, systematic debugging, code review, and verification-before-completion. At GREEN, verify the project suite, not only the narrow test that first went red.
- mattpocock/skills current main: `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d` — composable skills, source-backed research, test-first implementation, and two-axis review (spec compliance separately from repository standards).
- Ponytail 5.3.3: `7801d061243d7b753bad0e0b3c057cd250b11755` — codebase/data-flow audit, connected-code review, minimal complete changes, and explicit preservation of security, data integrity, and accessibility.

These references guide the method; project-specific linguistic, provenance, privacy, rights, and fail-closed requirements remain authoritative.


- Keep the restricted labialized onset inventory in `data/lao/onset_clusters.csv` and generate its browser mirror; do not hard-code a second divergent list. Preserve the superscript `ʷ` at the IPA boundary, reject clusters before rounded nuclei, and withhold overlapping `Cວາ` analyses rather than guessing between labialized-onset + AA and UO-long-open. Do not invent Ukrainian correspondences for these IPA sequences. Search for silent high-class `ຫ` digraphs after any preposed vowel, not only at token index zero. Extend `tests/fixtures/onset_cluster_cases.json` when adding a cluster or a boundary exception; Python and browser tests must consume the same cases.


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
