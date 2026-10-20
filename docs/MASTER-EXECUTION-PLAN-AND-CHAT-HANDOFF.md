# Master execution plan and chat handoff

Last reviewed: 2026-10-20
Repository: https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System
Baseline branch: `main`
Baseline commit: `763b67892838929ef7ca46d6f540cf21d66fc4e5`
Work branch: `fix/python-vowel-pattern-priority-20261020`
Work branch latest verified code/test commit at handoff: `ca0e8d39493bad65918e39e13ba79776438ac0b1`; current shared-fixture test commit: `1f8b5239f070d7eca6b3d119fd512fba9afd598d` (CI pending at last update)

## Status vocabulary
Use only: `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE_VERIFIED`, `DEFERRED`, `NOT_APPLICABLE`.
Do not mark code changes `DONE_VERIFIED` until the current commit's relevant checks have actually passed.

## Current audit summary

The project has separate Python and browser engines, canonical Lao consonant/vowel/coda/tone registries, Ukrainian correspondences, source/claim CSVs, tests, and methodology/limitations/audit documentation. The last visible `main` verification run was successful for commit `763b67892838929ef7ca46d6f540cf21d66fc4e5` (2026-10-09). This is historical evidence only; it does not verify any later branch changes.

Static source inspection identified and fixed a Python vowel-matching precedence risk: generic preposed vowel patterns with empty suffixes could shadow more specific patterns. Regression tests for OE, OEE and IA_LONG pass in run 39482443085. A second issue was found and patched: Python status propagation now downgrades analyses that contain parser warnings. The parser-warning status regression test in `ca0e8d39493bad65918e39e13ba79776438ac0b1` was verified by successful run 39482633937. The subsequent handoff-documentation commit `5191d0ca49714f313ff1f859048b015c63c193b5` also passed run 39482716944. Browser regressions for OE/OEE/IA_LONG were then added in `476a334102d2fc04c91868c39ab9fdbd2e648705`; verify its CI before marking browser parity coverage complete.

## Execution register

| ID | Priority | Status | Scope / evidence | Acceptance criteria / dependencies |
|---|---|---|---|---|
| LAO-AUD-001 | P0 | DONE_VERIFIED | Repository tree and key Python/browser engines, registries, tests, workflows, audit/methodology/limitations docs inspected on 2026-10-20 | Current tracked files and key modules identified; no claim that every row of every registry has been scientifically adjudicated |
| LAO-PY-001 | P0 | DONE_VERIFIED | `src/lao_ukrainian/parser.py`; generic empty-suffix patterns could precede specific vowel patterns | Python tests and new regression tests passed at code commit `3695815dfbc3f48d8bd6a4e4395aa46f44e8e5e3`; run [39482443085](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39482443085) |
| LAO-PY-002 | P0 | DONE_VERIFIED | `tests/test_structural_vowels.py`; added OE, OEE and IA_LONG precedence regressions | New tests and full Python + JS + build/reproducibility workflow passed at code commit `3695815dfbc3f48d8bd6a4e4395aa46f44e8e5e3`; run [39482443085](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39482443085) |
| LAO-STATUS-001 | P0 | DONE_VERIFIED | `src/lao_ukrainian/core.py` downgrades `ESTABLISHED` when parser warnings exist; regression test in `tests/test_core.py` | CI run [39482633937](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39482633937) passed for test commit `ca0e8d39493bad65918e39e13ba79776438ac0b1` |
| LAO-PARSER-001 | P0 | TODO | Python parser and browser parser are separate implementations | Differential corpus demonstrates agreement where the engines claim the same supported scope |
| LAO-TONE-001 | P0 | TODO | `data/lao/tone_rules.csv`, `src/lao_ukrainian/phonology.py`, `web/engine.js` | Every implemented tone rule has source, defined conditions, examples and tests; phonological categories distinguished from measured contours |
| LAO-VOWEL-001 | P0 | IN_PROGRESS | Inventory has 37 vowel IDs in `vowels.csv`, 16 generalized rows in `vowel_structures.csv`, and separate Python/JS pattern logic; the CSVs do not encode all parser spellings (e.g. several alternative UO spellings and explicit onset placeholders) | Reconcile registry, structures and both parsers; source each pattern; add full positive/negative fixture coverage; do not infer evidence from implementation output |
| LAO-CODA-001 | P0 | TODO | `data/lao/codas.csv`, `data/lao/consonants.csv` | Legal codas and invalid-final handling exhaustively tested; no arbitrary final accepted silently |
| LAO-CLUSTER-001 | P0 | TODO | `docs/limitations.md` explicitly says initial-cluster model is incomplete | Dedicated grammar/tests for valid clusters, high-class silent digraphs and boundary ambiguities |
| LAO-UNICODE-001 | P1 | TODO | `src/lao_ukrainian/normalize.py`, `web/engine.js` | NFC, mixed script, malformed marks, controls, ZWSP and whitespace behavior aligned and tested |
| LAO-UKR-001 | P1 | TODO | `data/lao/ukrainian_correspondences.csv`, `src/lao_ukrainian/target.py` | Target adaptation independently reviewed; policy decisions distinguished from Lao facts |
| LAO-CORPUS-001 | P0 | TODO | No expert-adjudicated gold corpus or accuracy denominator is claimed in current docs | Versioned independent corpus includes all major classes and edge cases, with sources and expected layer-by-layer outputs |
| LAO-EVIDENCE-001 | P1 | TODO | `data/evidence/sources.csv`, `data/evidence/claims.csv` | Every material rule linked to a precise source and relevant passage/page/section; conflicts and dialect scope recorded |
| LAO-DOCS-001 | P1 | TODO | Existing methodology, validation, limitations, final audit | Docs match actual code and do not overclaim; final audit updated after CI and corpus results |
| LAO-RELEASE-001 | P2 | TODO | `CITATION.cff` and `LICENSE` already exist | Verify metadata/license consistency; create tagged release and Zenodo archive only after P0 acceptance gates |
| LAO-DEPLOY-001 | P1 | TODO | GitHub Pages workflow exists | Verify live site and generated artifacts against current commit; deployment success is not phonetic validation |

## Coverage matrix (initial; not yet a scientific completeness claim)

| Domain | Current evidence | Coverage judgment | Next action |
|---|---|---|---|
| Unicode/NFC | Python and JS normalization/validation tests | Partial | Add malformed ordering, control, ZWSP and cross-engine parity tests |
| Initial consonant classes | Consonant registry + basic class tests | Partial | Check all modern consonants and class exceptions against independent sources |
| Vowels and length | Vowel registry + limited structural tests | Partial; Python precedence issue under repair | Test every vowel structure and short/long contrast |
| Syllable structure | Syllable parser and browser segmentation tests | Partial; no complete lexical segmentation claim | Expand legal/illegal structure corpus and clusters |
| Codas | Coda/consonant registries + checked-coda test | Partial | Exhaustive allowed/forbidden final tests |
| Tone marks | Four marks and CSV rule table | Partial | Cross-product coverage by class, live/dead, length and mark; validate restricted mark conditions |
| Tone categories | Vientiane-oriented matrix | Partial | Source-level review and independent expected examples |
| Surface tone contours | Contours in data | Not fully empirically verified | Treat contours as descriptive conventions unless supported by phonetic measurements |
| IPA | Generated from graphemic/phonological tables | Partial | Independent expected IPA corpus, segment-by-segment review |
| Ukrainian adaptation | Canonical correspondence table | Partial; project policy, not national standard | Independent review and target-specific examples |
| Exceptions/names | Limitations documented | Incomplete | Add named/loan/ambiguous examples and preserve unresolved statuses |
| Browser/Python parity | Shared fixture `tests/fixtures/vowel_precedence_cases.json` is now consumed by both `tests/test_structural_vowels.py` and `web/engine.test.js` (commits `9556062`, `57e07f2`, `1f8b523`) | Partial; shared IPA fixture CI pending | Expand fixtures beyond the three precedence regressions and compare status, coda, tone and Ukrainian output where semantics align |
| CI/build/deployment | Workflow exists; baseline main run succeeded 2026-10-09 | Historical baseline only | Check current work-branch run and live deployment |
| Sources and reproducibility | Sources/claims registries and generation scripts | Partial | Audit each claim, citation metadata and generated artifacts |

## Handoff — 2026-10-20

### Inspected
- `docs/PHONOLOGY-AUDIT.md`
- `docs/final-audit.md`
- `docs/validation.md`
- `docs/methodology.md`
- `docs/system-specification.md`
- `docs/limitations.md`
- `src/lao_ukrainian/parser.py`, `phonology.py`, `core.py`, `model.py`, `normalize.py`, `target.py`
- `data/lao/consonants.csv`, `vowels.csv`, `codas.csv`, `tone_rules.csv`
- `tests/test_core.py`, `tests/test_unicode.py`, `tests/test_structural_vowels.py`
- `web/engine.js`, `web/engine.test.js`
- `.github/workflows/verify.yml`

### Changes made on work branch
- `src/lao_ukrainian/parser.py`: prioritizes specific vowel patterns with longer suffixes before generic empty-suffix patterns.
- `tests/test_structural_vowels.py`: added regressions for preposed OE, OEE and IA_LONG patterns.
- `src/lao_ukrainian/core.py`: parser warnings now downgrade otherwise `ESTABLISHED` results to `EVIDENCE LIMITED`.
- `tests/test_core.py`: added a regression for a syllable with an unconsumed grapheme; this test has not yet been confirmed by CI on the commit containing it.

### Commands and results
- GitHub tree/file/API inspection performed.
- Baseline `main` verification run for `763b67892838929ef7ca46d6f540cf21d66fc4e5`: success, run 125. This is not a test result for the work branch.
- No local test command was executed in this session.
- Work-branch CI result: success for code/test commit `3695815dfbc3f48d8bd6a4e4395aa46f44e8e5e3`, [run 39482443085](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39482443085). All workflow steps passed: Python tests, browser engine tests, build/data regeneration, reproducibility and built-page checks.
- Second run [39482622038](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39482622038) for `7d6e5f85fb324c83e110cf3220d08ba28b2650f3`: Python tests, browser engine tests, build/data regeneration, reproducibility and built-page checks all reported success. Important: this run predates test commit `ca0e8d39493bad65918e39e13ba79776438ac0b1`; it does not verify the newly added warning-status regression.

### Open scientific questions
- Complete coverage of the Lao vowel inventory and orthographic combinations.
- Exact scope and conditions for tone-mark rules, including restricted marks.
- Initial clusters, silent high-class sequences, and syllable boundaries.
- Whether current tone contour labels represent phonological categories or measured phonetic realizations.
- Independent verification of Ukrainian output mappings.
- Lack of a versioned, expert-adjudicated gold corpus.

### Blockers
- Full local execution was unavailable through the connected GitHub interface; use the branch CI as the immediate execution environment.
- Scientific completion is blocked on rule-by-rule source verification and an independent corpus, not on documentation volume.

### One next step
Trigger/check CI for the current branch head containing commit `ca0e8d39493bad65918e39e13ba79776438ac0b1`. If it passes, mark the warning-status fix verified; then continue the full vowel/coda/tone coverage audit (LAO-VOWEL-001 / LAO-CODA-001 / LAO-TONE-001). Do not treat CI success as scientific validation.
