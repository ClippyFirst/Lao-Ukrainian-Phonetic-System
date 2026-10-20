# Master execution plan and chat handoff

Last reviewed: 2026-10-20
Repository: https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System
Baseline branch: `main`
Baseline commit: `763b67892838929ef7ca46d6f540cf21d66fc4e5`
Work branch: `fix/python-vowel-pattern-priority-20261020`
Work branch latest shared coda test commit: `01c712b201b231d42419279783a387db5e57d3ba`; full CI passed in [run 39484876447](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39484876447). Shared coda fixtures also passed in Python [run 39484867250](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39484867250). Evidence registry latest commit: `a19eb1e2d97ec89a67a7542ce89e9dca1ba145d6`.

## Status vocabulary
Use only: `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE_VERIFIED`, `DEFERRED`, `NOT_APPLICABLE`.
Do not mark code changes `DONE_VERIFIED` until the current commit's relevant checks have actually passed.

## Current audit summary

The project has separate Python and browser engines, canonical Lao consonant/vowel/coda/tone registries, Ukrainian correspondences, source/claim CSVs, tests, and methodology/limitations/audit documentation. The last visible `main` verification run was successful for commit `763b67892838929ef7ca46d6f540cf21d66fc4e5` (2026-10-09). This is historical evidence only; it does not verify any later branch changes.

Audit found and fixed: (1) Python vowel-pattern precedence; (2) parser warnings incorrectly coexisting with an `ESTABLISHED` status; (3) missing Python structures for short /o/ in closed syllables and standalone ຽ; (4) a browser segmentation tie where `ກົວະ` was split as `ກົ|ວະ`; (5) missing closed-coda constraints for the short A2 and AWW_SHORT_ALT spelling forms. Shared fixtures are consumed by both engines. Full Python, browser, build, data regeneration, reproducibility and built-page checks passed for the 36-case vowel fixture suite in [run 39484094983](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39484094983); the newest short-vowel constraint tests are pending current-head CI. The shared fixtures are engineering regression cases, not an independently adjudicated gold corpus.

## Execution register

| ID | Priority | Status | Scope / evidence | Acceptance criteria / dependencies |
|---|---|---|---|---|
| LAO-AUD-001 | P0 | DONE_VERIFIED | Repository tree and key Python/browser engines, registries, tests, workflows, audit/methodology/limitations docs inspected on 2026-10-20 | Current tracked files and key modules identified; no claim that every row of every registry has been scientifically adjudicated |
| LAO-PY-001 | P0 | DONE_VERIFIED | `src/lao_ukrainian/parser.py`; generic empty-suffix patterns could precede specific vowel patterns | Python tests and new regression tests passed at code commit `3695815dfbc3f48d8bd6a4e4395aa46f44e8e5e3`; run [39482443085](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39482443085) |
| LAO-PY-002 | P0 | DONE_VERIFIED | `tests/test_structural_vowels.py`; added OE, OEE and IA_LONG precedence regressions | New tests and full Python + JS + build/reproducibility workflow passed at code commit `3695815dfbc3f48d8bd6a4e4395aa46f44e8e5e3`; run [39482443085](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39482443085) |
| LAO-STATUS-001 | P0 | DONE_VERIFIED | `src/lao_ukrainian/core.py` downgrades `ESTABLISHED` when parser warnings exist; regression test in `tests/test_core.py` | CI run [39482633937](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39482633937) passed for test commit `ca0e8d39493bad65918e39e13ba79776438ac0b1` |
| LAO-PARSER-001 | P0 | IN_PROGRESS | Python coda finder previously accepted any legal final anywhere in the remaining material; now only accepts the last grapheme. Shared tests check that malformed trailing material is not silently consumed | Current CI run [39484575636](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39484575636); differential corpus still required |
| LAO-TONE-001 | P0 | TODO | `data/lao/tone_rules.csv`, `src/lao_ukrainian/phonology.py`, `web/engine.js` | Every implemented tone rule has source, defined conditions, examples and tests; phonological categories distinguished from measured contours |
| LAO-VOWEL-001 | P0 | IN_PROGRESS | Inventory has 34 vowel IDs in `vowels.csv`, 21 generalized rows in `vowel_structures.csv`, and separate Python/JS pattern logic; the CSVs do not encode all parser spellings (e.g. several alternative UO spellings and explicit onset placeholders) | Reconcile registry, structures and both parsers; source each pattern; add full positive/negative fixture coverage; do not infer evidence from implementation output |
| LAO-CODA-001 | P0 | IN_PROGRESS | `data/lao/codas.csv`, `data/lao/consonants.csv`; Python coda detection requires the last grapheme; `tests/fixtures/coda_cases.json` covers 9 currently registered final graphemes | Shared Python/browser coda fixtures and invalid-final test pass CI; still requires source-level review of the coda inventory and exhaustive invalid-final variants |
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
| Vowels and length | 34 vowel IDs; 21 generalized structure rows; shared cross-engine fixtures cover the core vowel set and known precedence/segmentation edge cases | Partial; registry-to-Python coverage test and regression fixtures pass CI, but not all spellings have independent source adjudication | Expand negative/alternative spellings and attach exact source passages to each rule |
| Syllable structure | Syllable parser and browser segmentation tests | Partial; no complete lexical segmentation claim | Expand legal/illegal structure corpus and clusters |
| Codas | Shared fixture covers 9 registered final graphemes; tests reject a coda before unconsumed trailing material and reject unregistered final ສ | Partial; shared Python/browser coda fixtures passed CI; phonological inventory still needs independent review | Add broader invalid-final and coda-position cases; reconcile coda registry with the ʔ entry and actual orthographic representation |
| Tone marks | Four marks and CSV rule table | Partial | Cross-product coverage by class, live/dead, length and mark; validate restricted mark conditions |
| Tone categories | Vientiane-oriented matrix | Partial | Source-level review and independent expected examples |
| Surface tone contours | Contours in data | Not fully empirically verified | Treat contours as descriptive conventions unless supported by phonetic measurements |
| IPA | Generated from graphemic/phonological tables | Partial | Independent expected IPA corpus, segment-by-segment review |
| Ukrainian adaptation | Canonical correspondence table | Partial; project policy, not national standard | Independent review and target-specific examples |
| Exceptions/names | Limitations documented | Incomplete | Add named/loan/ambiguous examples and preserve unresolved statuses |
| Browser/Python parity | Shared fixture `tests/fixtures/vowel_precedence_cases.json` is consumed by both `tests/test_structural_vowels.py` and `web/engine.test.js`; the fixture suite includes 36 expected-IPA cases | Vowel fixtures and full CI passed in run [39484094983](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39484094983); full status/coda/tone/target-output parity remains unverified | Extend shared fixtures to status, coda, tone and Ukrainian output where semantics align |
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
- `src/lao_ukrainian/parser.py`: sorts structural vowel patterns by specificity; added missing standalone short-/o/ pattern (`ົ`) and standalone long IA sign (`ຽ`); marks A2 and AWW_SHORT_ALT without a coda as evidence-limited; only accepts a coda if it is the last remaining grapheme.
- `src/lao_ukrainian/core.py` and `tests/test_core.py`: analyses with parser warnings are downgraded from `ESTABLISHED`.
- `web/engine.js`: equal-score segmentation now prefers fewer fragments, fixing a demonstrated complex-vowel split; A2 and AWW_SHORT_ALT spellings without a coda are flagged and not treated as complete. Browser test rejects a parsed coda when trailing material remains.
- `tests/fixtures/vowel_precedence_cases.json`: 36 shared expected-IPA regression cases; explicitly labelled as engineering fixtures, not a gold corpus.
- `tests/test_structural_vowels.py` and `web/engine.test.js`: consume the shared fixture and assert one-syllable boundaries and expected IPA.
- `data/lao/vowel_structures.csv`: corrected short/long IA, UA and UO labels and /aw/ IPA; added explicit long-form rows.
- `data/evidence/sources.csv` and `data/evidence/claims.csv`: added Ishida's Lao Orthography Notes and source-linked claims for OE, short O, IA, UA, UO, /aw/, /am/, long /ɔː/, and short-vowel closed-syllable constraints. Exact source-passage review for every vowel row remains open.

### Commands and results
- Repository and current branch were inspected through the GitHub connector; tests were run by the repository's GitHub Actions workflow, not locally.
- CI for the 36-case shared fixture commit [39484094983](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39484094983) passed all steps: Python tests, browser engine tests, build/data regeneration, reproducibility and built-page checks.
- Two earlier fixture-expansion CI runs failed because the browser segmentation algorithm preferred a split parse on a tie. The issue was reproduced from logs, fixed in `web/engine.js`, and the expanded fixture suite then passed. Keep this failure/fix in the audit trail; do not report those earlier runs as green.
- CI run [39484690202](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39484690202) passed Python tests, browser tests, data regeneration, reproducibility and built-page checks for the coda-position regression using malformed trailing material `ກາງເ`. An earlier test using `ກາງະ` failed because the browser could validly segment it as separate syllables; the fixture was changed to avoid that ambiguity.\n- Added `tests/fixtures/coda_cases.json` for 9 registered coda graphemes and made both engines consume it; also added a negative test for unregistered final ສ. The Python and browser fixture commits passed runs [39484867250](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39484867250) and [39484876447](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39484876447). This does not independently validate the phonological coda inventory.

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
Check CI for the current handoff commit. Continue LAO-CODA-001 with additional invalid-final and boundary cases, and investigate why the phonological coda registry includes /ʔ/ while no dedicated final grapheme appears in the current orthographic registry. Then return to LAO-VOWEL-001 for negative/invalid spelling fixtures and exact source-passage audits; next move to the tone-mark cross-product. Do not treat CI success as scientific validation.


## Reconciliation checkpoint — 2026-10-20

- Fresh branch inventory confirmed `main` at `763b67892838929ef7ca46d6f540cf21d66fc4e5` and the work branch at `15848394978243e3b17e595cc3623f2ef0984231` before the latest test/documentation commits. The work branch was 50 commits ahead and 0 behind; the compare view showed 12 changed files. Do not merge the whole branch by name alone; review the file diff and CI first.
- Current branch additions: `docs/vowel-template-coverage.md` lists all 41 Python `STRUCTURES` templates; `tests/test_structural_vowels.py` now includes a generated positive and near-miss negative control for each template plus 11 near-neighbour contrasts and malformed-material controls.
- First generated negative-control attempt failed on five empty-suffix templates because those forms are valid by definition. The test was corrected to substitute a different preposed vowel sign for empty-suffix templates. The corrected commits are `62e08a25698b8fd8ba4c8317947a8e0ae1c415c6` and `5b422b0b51bd3fd59cb58508b946246ed33abbb1`; their CI runs were queued at handoff update time. Do not mark the new per-template test gate verified until the newest run completes successfully.
- `src/lao_ukrainian/target.py` confirms the Python target adapter consumes phonemic IPA and maps it through the canonical correspondence registry. The browser engine also builds IPA first and calls `mapIpa`; it is a separate implementation, not a hidden Ukrainian-only direct mapping. Methodology documents this as a project-level practical correspondence system, not an official Ukrainian national standard.
- `CITATION.cff` is present and declares MIT; `LICENSE` is MIT. Existing `docs/methodology.md` documents the IPA-first pipeline. `docs/validation.md` on main is stale: it says the updated branch could not be freshly run. Replace that historical note only after CI is confirmed, and never report a corpus accuracy percentage without an independently adjudicated gold corpus.
- Independent corpus/G2P comparison remains NOT VERIFIED. No external G2P was adopted in this checkpoint; any future comparison must first establish supported dialect, phonemic vs phonetic IPA convention, licensing, and redistribution conditions.
- Remaining risk: the browser matcher duplicates Python logic rather than importing a shared declarative matcher. Shared expected-IPA fixtures help consistency but cannot independently establish correctness; tone/class rules, initial clusters, Unicode ligatures, segmentation and conventional names still need separate evidence and tests.


## PR and external comparator update — 2026-10-20

- Opened review PR [#8](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/8), base `main`, head `fix/python-vowel-pattern-priority-20261020`, head commit `df55ba326c8ec80f88fd2163ea12afc3b1215c48`. No merge performed. The PR is 14 changed files; reviewers should inspect the diff and not infer safety from the branch name.
- Full push-triggered CI passed at head `df55ba326c8ec80f88fd2163ea12afc3b1215c48` in [run 39487919164](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39487919164): 45 Python tests, 34 browser tests, browser-data regeneration, reproducibility and built-page/asset checks. PR-triggered run [39487973350](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39487973350) was queued at this update.
- Relevant sibling branches were compared too: `fix/lao-vowel-ia-segmentation-20261009`, `fix/lao-multisyllable-h-to-h-20261009`, and `audit/finalize-research-grade` are diverged from current `main`; none was merged. Their diffs include older web/target/docs changes and are not a safer direct integration base than the branch being reviewed against live `main`.
- External comparator candidate: [`lao2ipa` 1.0.0](https://github.com/byu-matrix-lab/lao2ipa), also listed on [PyPI](https://pypi.org/project/lao2ipa/1.0.0/). Its published metadata states Apache-2.0 and an IPA output mode; its README specifically flags tone assignment and vowel clusters as heuristic areas. This is suitable as an independent *candidate implementation*, not a gold standard. The runtime could not be fetched/executed in the current environment (network resolution/download unavailable), so no output-to-output comparison is claimed. Next valid step is to run it in a network-enabled reproducible environment against a frozen corpus and report disagreements, not majority-vote them away.
- Do not merge until the PR check is green and a reviewer has considered the independent comparator/corpus limitation. Existing green CI establishes deterministic engineering consistency, not phonological truth.


## Handoff update — external G2P harness added (2026-10-20)

- PR: [#8](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/8), still open and unmerged.
- Independent-comparison tracking: [issue #9](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/issues/9).
- Added `scripts/compare_external_g2p.py` and `docs/independent-g2p-comparison.md`. The harness calls the documented `lao2ipa.transliterate(..., output="ipa")` API, captures per-case output, normalizes to NFC only, and writes JSON. Phonological mismatches remain review data; runtime failures are surfaced separately.
- Updated `docs/validation.md` to record the current green run and the status of the independent comparator.
- Latest completed full CI before the validation-doc-only commit: [run 39489040363](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39489040363), head `afa168c19a60d5d8efce24f0ebeae47246897eb0`; passed Python, browser, regeneration, reproducibility, and build/asset checks.
- The comparison harness has **not** been run against the external package in this environment. No comparison rate or independent accuracy claim exists. Run the documented command in a network-enabled clean environment, preserve the JSON artifact, and manually review every mismatch.
- Latest commits after the cited run are documentation-only. Verify CI on the current branch head before claiming current-head green or merging.
