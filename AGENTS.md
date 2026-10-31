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
- [mattpocock/skills](https://github.com/mattpocock/skills/tree/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa): deep modules and clear interfaces, test seams, behavior-focused tests, and source-backed research.
- [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail/tree/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846): smallest complete diff, reuse before invention, review of connected code rather than diff alone, and explicit deferred-work accounting.

When these references conflict with this file, the existing project requirements, or the user's explicit instructions, follow the project requirements and user instructions. Do not import or install these repositories as project dependencies merely to follow their methods.
