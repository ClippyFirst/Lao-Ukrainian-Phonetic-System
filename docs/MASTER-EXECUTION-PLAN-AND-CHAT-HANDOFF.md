# Master execution plan and chat handoff

Last reviewed: 2026-10-20
Repository: https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System
Baseline branch: `main`
Baseline commit: `763b67892838929ef7ca46d6f540cf21d66fc4e5`
Work branch: `fix/python-vowel-pattern-priority-20261020`
Work branch latest parser/coda regression test commit: `43d1d4ec4c11e368e0b9202a37e9b141545bb7c1`; full CI passed in [run 39484690202](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39484690202). Evidence registry latest commit: `a19eb1e2d97ec89a67a7542ce89e9dca1ba145d6`.

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
| LAO-CODA-001 | P0 | IN_PROGRESS | `data/lao/codas.csv`, `data/lao/consonants.csv`; Python coda detection now requires a legal coda to be the last grapheme in the remainder | One malformed trailing-grapheme regression added; exhaustive legal/illegal final cross-product remains open |
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
| Codas | Coda/consonant registries, checked-coda tests, and a new regression preventing a legal coda from being accepted before trailing unconsumed graphemes | Partial; targeted CI passed, exhaustive inventory still pending | Add all legal codas and representative illegal/trailing combinations to shared Python/browser fixtures |
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
- CI run [39484690202](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39484690202) passed Python tests, browser tests, data regeneration, reproducibility and built-page checks for the coda-position regression using malformed trailing material `ກາງເ`. An earlier test using `ກາງະ` failed because the browser could validly segment it as separate syllables; the fixture was changed to avoid that ambiguity. This does not exhaustively validate all coda combinations.

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
Check CI for the current handoff commit. Continue LAO-CODA-001 by adding shared fixtures for every legal coda and malformed trailing material, then return to LAO-VOWEL-001 for negative/invalid spelling fixtures and a rule-by-rule source-passage audit. After those, move to the tone-mark cross-product. Do not treat CI success as scientific validation.
