
## Lao external G2P mismatch taxonomy — 2026-10-24

- Branch `research/lao-g2p-diagnostic-categories-rebased-20261024` updates the existing comparator instead of adding a parallel runner.
- Categorized pinned run [40121272427](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40121272427): 36 engineering cases, 0 runtime errors, 0/36 exact implementation agreement, independent gold=0, accuracy=null. Categories: 29 tone-suffix-only, 2 offglide-convention, 4 segmental/vowel-sequence, 1 tone+length. Durable report: `data/benchmark/runs/external-g2p-smoke-2026-10-24.json`; artifact ZIP SHA-256 `a2fea18c48e337ce37b070b2da9ff2e5236b51295f80100d2ebae06a4478d4b8`.
- The category labels are heuristic review hints only. Lao tone may be contrastive, so tone-suffix differences are not automatically harmless. Prioritize source-located adjudication of tone convention and the four segmental/vowel-sequence cases.
- Unit tests for the classifier passed on the previous branch head; full current-branch CI and optional comparison are required before merge. No accuracy or engine winner is claimed.
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
| LAO-G2P-001 | P1 | DONE_VERIFIED | Pinned lao2ipa==1.0.0 workflow [40092430175](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40092430175) completed; artifact inspected: 36 cases, 0 runtime errors, 0 external fixture matches and 0 exact cross-engine matches; verification suite [40092430173](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40092430173) passed | Preserve the diagnostic artifact and manually classify output conventions; do not interpret engineering-fixture disagreement as accuracy. Accuracy remains blocked by LAO-CORPUS-001 |
| LAO-G2P-002 | P1 | DONE_VERIFIED | Schema-v3 metric hardening verified in [workflow 40093370619](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40093370619); artifact inspected and no ambiguous exact_match_rate key remains | Report includes implementation_agreement_rate, independent_gold_count=0, accuracy=null, score_status=NOT_SCORED_NO_INDEPENDENT_GOLD; verification suite [40093370613](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40093370613) passed || LAO-EVIDENCE-001 | P1 | TODO | `data/evidence/sources.csv`, `data/evidence/claims.csv` | Every material rule linked to a precise source and relevant passage/page/section; conflicts and dialect scope recorded |
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


## Execution checkpoint — 2026-10-21

### Reconciled branch and PR state

- `main` baseline remains `763b67892838929ef7ca46d6f540cf21d66fc4e5`.
- PR [#8](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/8) remains open and unmerged. Its current head at audit time is `04c54bb7d27c3bccc268a7dbca2b037b84e9a9f7`; comparison with `main` reports 63 commits ahead, 0 behind, and 17 changed files. Do not merge blindly; review the complete PR diff.
- The named branch `fix/python-vowel-pattern-priority-20261020` exists. The PR is the reviewable workstream for its relevant changes; preserve sibling branches unless a fresh diff proves their unique work is needed.
- Current-head PR workflow run [39489155729](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39489155729) completed successfully. The repository's documented workflow verifies Python tests (45), browser tests (34), canonical browser-data generation, generated-data reproducibility, and static built-page/relative-asset checks. These results are CI evidence for the recorded head, not a local rerun or linguistic accuracy evidence.
- Local clone/test execution was attempted but blocked before checkout because this environment could not resolve `github.com`. No local command results are claimed.

### Task ledger reconciliation

| ID | Status | Current evidence / remaining acceptance criterion |
|---|---|---|
| LAO-AUD-001 | DONE_VERIFIED | Current PR file list, baseline comparison, existing matrices, validation/limitations/implementation docs, evidence registries, parser, target adapter, phonology, audit/generator scripts and Pages workflow inspected. This is not an exhaustive expert review of every registry row. |
| LAO-PY-001 | DONE_VERIFIED | Specific vowel-pattern matching precedes generic empty-suffix patterns; current-head CI is green. |
| LAO-PY-002 | DONE_VERIFIED | 41 Python structures have positive/negative synthetic controls; 36 shared vowel cases are consumed by Python and browser tests. Fixtures remain regression controls, not gold data. |
| LAO-STATUS-001 | DONE_VERIFIED | Parser warnings downgrade result status; covered by regression tests and current-head CI. |
| LAO-PARSER-001 | PARTIAL | Coda must be the final remaining grapheme; malformed trailing material is tested. Broader lexical segmentation and source-backed syllable boundaries remain unverified. |
| LAO-VOWEL-001 | PARTIAL | Structure registry and parser tests expanded; source claims added. Exact source-passage verification for every spelling, carrier context, ຳ/Niggahita variants, and alternative forms remains open. |
| LAO-CODA-001 | PARTIAL | Shared fixtures cover nine registered coda graphemes and reject an unregistered final. Independently verify the inventory and resolve the documented glottal-stop/orthographic representation question. |
| LAO-TONE-001 | IN_PROGRESS | Added `tests/test_tone_rule_registry.py`: unique selector keys, declared field values, reachability of all 17 rules, and conservative fallback for an unlisted class/mark combination. CI passes. Still requires the full onset-class × live/dead × quantity × tone-mark cross-product, source-by-source audit, restricted-mark review, and contour-convention review. |
| LAO-CLUSTER-001 | TODO | Add evidence-backed rules and adversarial cases for legal initial clusters, silent/high-class sequences, and boundary ambiguities. |
| LAO-UNICODE-001 | IN_PROGRESS | Python/browser CRLF behavior is aligned; tests reject unsupported C0 controls and U+200B in both runtimes. Final merged code commit `007c6a7e0bce0ca72cda3ddda3054c69492ca3b8` passed CI. Malformed-mark ordering, full format-control inventory, and broader analysis parity remain open. |
| LAO-UKR-001 | IN_PROGRESS | Python `target.py` and browser engine both map from IPA; shared nine-case `tests/fixtures/target_output_cases.json` verifies both runtimes. Final merged code commit `007c6a7e0bce0ca72cda3ddda3054c69492ca3b8` passed CI. Independent review of target-policy choices remains open. |
| LAO-EVIDENCE-001 | PARTIAL | Claims and sources were expanded for vowel families; exact passage/page/section locators and conflict/dialect scope must be checked rule by rule. |
| LAO-CORPUS-001 | BLOCKED | No versioned independently adjudicated Lao gold corpus. Acceptance requires a licensed/source-attributed corpus, explicit dialect and IPA conventions, denominator, expert adjudication and reproducible layer-level expected outputs. |
| LAO-DEPLOY-001 | DONE_VERIFIED | GitHub Pages deployment of merged commit `007c6a7e0bce0ca72cda3ddda3054c69492ca3b8` succeeded in [run 39597989697](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39597989697). Workflow reported `https://clippyfirst.github.io/Lao-Ukrainian-Phonetic-System/` as the environment URL. This verifies the Pages deployment job; direct HTTP fetch from this session was blocked by DNS resolution failure. |
| LAO-DOCS-001 | PARTIAL | Validation, limitations, vowel coverage, comparison protocol and this handoff describe known status. Complete source audit and tone/cluster/corpus work before publication claims. |
| LAO-RELEASE-001 | DEFERRED | Do not tag/publish while P0 evidence and corpus gates remain open. Existing MIT metadata/license are not a substitute for phonological validation. |

### Commands and results actually available

- `git clone https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System.git`: BLOCKED — DNS resolution failure for `github.com` before checkout.
- Repository-defined `python scripts/audit.py`, `PYTHONPATH=src python -m unittest discover -s tests -v`, `npm test`, `npm run build`, and generated-file drift check: NOT RUN locally in this session.
- CI run [39489155729](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39489155729): PASS at recorded head; 45 Python tests, 34 browser tests, data regeneration, reproducibility and built-page checks as documented in `docs/validation.md`.
- External comparison `lao2ipa==1.0.0`: NOT RUN; dependency/network access unavailable. Do not report a match rate.
- GitHub Pages deployment: PASS — [run 39597989697](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39597989697), deploy job completed successfully and emitted the live environment URL.

### Release-readiness conclusion

Status remains **research MVP / partial prototype**, not research-complete or release-ready. Deterministic engineering CI is green at the recorded PR head. The main blockers are independent source adjudication of vowel/tone/cluster rules, broader lexical and syllable controls, external comparison, a versioned expert-adjudicated gold corpus, and explicit Pages deployment evidence. No empirical accuracy percentage is justified.


## Execution checkpoint — 2026-10-21 (continued)

### Tone-rule engineering coverage

- Added `tests/test_tone_rule_registry.py` on the existing work branch; no parallel phonology implementation was introduced.
- The tests assert unique rule IDs and exact selector keys, valid registry field values, reachability of all 17 declared tone rules through `determine_tone`, conservative fallback for an unlisted combination, and all 60 onset-class × live/dead × vowel-quantity × tone-mark selector combinations.
- CI run [39570205114](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39570205114) passed at code commit `4b06606fb7db474a68734396752bcb0e32352398`: Python **50 passed**, browser **34 passed**, optional comparator harness syntax/CLI check passed, browser-data regeneration/reproducibility passed, and built-page/relative-asset checks passed.
- Validation documentation was updated in commit `5ece54d0967afc05cd6415c5ec0f0811857e9a10` to record the verified 50/34 results. This handoff update itself is a later documentation commit and needs its own CI result before the final branch head can be called verified.
- These tests validate rule-table integrity and selector behavior only. They do not establish that the recorded tone categories or contours are linguistically correct.
- The tone audit remains `IN_PROGRESS`: next acceptance work is rule-by-rule primary-source verification, scrutiny of restricted marks and contour conventions, and independent expected examples. The code cross-product is now covered; it is not a scientific cross-product adjudication. Do not infer source correctness from a self-consistent registry.


## Execution checkpoint — 2026-10-21 (Unicode validation)

- Fixed a Python/browser input-validation mismatch: Python previously rejected carriage return while the browser explicitly accepted it as line whitespace. `src/lao_ukrainian/normalize.py` now permits CR alongside LF and tab.
- Added Python tests for CRLF acceptance, rejection of another C0 control, and rejection of U+200B. Added browser regressions confirming CRLF input is accepted as whitespace and U+200B is rejected rather than silently removed.
- CI run [39570439908](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39570439908) passed at code commit `04f60bfa4fe015307899b889fbafcc77963876f9`: Python **53 passed**, browser **36 passed**, optional comparator harness syntax/CLI check passed, generated-data reproducibility passed, and built-page/relative-asset checks passed.
- Updated `docs/unicode.md` and `docs/validation.md` to describe the behavior and evidence. The handoff itself is being updated after the code-head run; its new documentation commit still needs its own CI result.
- Scope limitation: this is a targeted parity repair, not full Unicode conformance. Malformed combining-mark order, format-control policy, and complete cross-engine behavior remain open.


## Evidence-source spot check — tone references (2026-10-21)

- Opened Richard Ishida's [Lao Orthography Notes](https://r12a.github.io/scripts/laoo/lo), updated 2026-04-28. Its tone discussion says published descriptions of Vientiane tones differ, shows three comparison tables (including different assignments/labels), states that tone marks are normally used only on open syllables, and identifies two marks as restricted to one consonant class. This supports keeping the implementation explicitly dialect-/analysis-scoped; it does not by itself validate every project rule.
- The current `SRC-SEASITE` URL (`https://seasite.niu.edu/lao/`) rendered only a frames-required landing page in this source check, so the exact chart passage used by the implementation was not independently inspectable from that URL. The source registry needs a direct, stable chart/page or a more precise bibliographic locator before that reference can satisfy rule-by-rule evidence acceptance.
- Follow-up for `LAO-TONE-001` / `LAO-EVIDENCE-001`: audit the exact mapping of high/middle/low classes to the selected table; verify tone-mark restrictions in the source's actual rule environment; distinguish tone-category labels from measured contour notation; and record why the chosen Vientiane-oriented model is preferred where the cited tables disagree. Do not silently normalize away those disagreements.


## Execution checkpoint — 2026-10-21 (IPA target boundary)

- Added `tests/fixtures/target_output_cases.json` with nine shared cases covering aspirated onset adaptation, /ŋ/, checked codas, open/closed /uːə/, medial /ɔː/, vowel-carrier behavior, and standalone ຽ in ວຽງ. Each fixture records both expected phonemic IPA and the project-defined Ukrainian output.
- Added Python and browser tests that consume the same fixture. This verifies that the IPA-first boundary is exercised in both runtimes and that both adapters agree on the selected project policy; it does not independently validate Lao pronunciations or make the Ukrainian choices official.
- CI run [39570654272](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39570654272) passed at code commit `cff8f949ae4d26455895c2e9824f43c22bf9981d`: Python **54 passed**, browser **37 passed**, optional comparator harness syntax/CLI passed, generated-data reproducibility passed, and built-page/relative-asset checks passed.
- `docs/validation.md` was updated in commit `0a4f9f0c7f545f406bbe03dc760e103f4a636214`. The subsequent handoff checkpoint at `b1acf1c1d161711fe97e86b9707826ecb0a74c0d` also passed current-head CI in [run 39570806681](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39570806681).
- The target policy remains an independent review task: inspect correspondence choices, ambiguity handling and unsupported IPA segments; do not conflate runtime parity with phonetic correctness.


## Final execution checkpoint — merged and deployed (2026-10-21)

- PR [#8](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/8) was squash-merged into `main`; merge commit: `007c6a7e0bce0ca72cda3ddda3054c69492ca3b8`. The merged PR included the vowel precedence/structural validation work, the shared coda/vowel/target fixtures, tone-rule selector tests, Unicode parity fix, external comparison harness (not executed), and in-place audit/handoff updates.
- Post-merge verification [run 39597989767](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39597989767) passed on `main`.
- The GitHub Pages build and artifact checks passed, then deployment succeeded in [run 39597989697](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39597989697). The workflow emitted the environment URL `https://clippyfirst.github.io/Lao-Ukrainian-Phonetic-System/`; `system.html` is published under the same path. Direct HTTP verification from this session could not run because DNS resolution for GitHub Pages failed in the local network, so deployment success is evidenced by the official workflow result rather than a local browser fetch.
- Latest merged code CI evidence: Python **54 passed**, browser **37 passed**, external-G2P harness syntax/CLI passed, canonical browser-data generation and reproducibility passed, built-page/relative-asset checks passed.
- README was updated to link the live pages and to state clearly that the site is a deployed research MVP, not a validated official standard.
- Final status: deployment gate `DONE_VERIFIED`; repository remains **research MVP / partial prototype**, not research-complete or release-ready. Remaining genuine blockers: rule-by-rule primary-source adjudication (especially tones and composite vowels), independent expert-adjudicated gold corpus, actual external `lao2ipa` comparison, broader clusters/segmentation/Unicode edge cases, and independent review of the Ukrainian target policy. No empirical accuracy percentage is claimed.


## Handoff update — reproducible external G2P execution workflow (2026-10-24)

- Added .github/workflows/optional-external-g2p.yml on branch feat/external-g2p-benchmark-harness-2026-10-24. It installs the project and exact comparator version lao2ipa==1.0.0, runs the existing diagnostic harness, and uploads artifacts/external-g2p-comparison.json for 30 days. The workflow is manually dispatchable and also runs when its harness/fixture/workflow changes.
- Added tests/test_external_g2p_harness.py, using the repository's unittest discovery convention. It guards NFC-only normalization and rejects stripping tone/length or treating the engineering fixture as independent gold.
- These changes do not enable the external engine in production and do not change the IPA→Ukrainian adapter. The comparator's outputs and exact-match rates remain diagnostic only.
- Status at handoff edit time: IN_PROGRESS pending PR CI and inspection of the workflow artifact. Do not claim an external comparison was run until a successful workflow artifact is available. The expert-adjudicated gold-corpus task remains TODO.


## Handoff update — Lao external G2P smoke result (2026-10-24)

- **DONE_VERIFIED — reproducible run:** [optional comparator workflow 40092430175](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40092430175) succeeded with pinned `lao2ipa==1.0.0`; main verification suite [40092430173](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40092430173) passed. Artifact `lao-external-g2p-comparison` SHA-256: `ff669bf3c772cd250cf4524b740cbf8f52682e6ac0f3627c038a86047c7713a9`.
- 36 engineering fixtures were run, 0 runtime errors. Project IPA matched the fixture's expected IPA 36/36; external output matched it 0/36; project/external exact match 0/36. Example `ເກິ`: project `kɤ`, external `kɤ˧˥`; `ເກຽ`: project `kiːə`, external `keː˩˧iːə`. The candidate adds tone contours in many cases and has material differences in some synthetic structures. These are diagnostic only; no correctness winner can be inferred from non-gold engineering fixtures.
- The task for reproducible smoke execution is DONE_VERIFIED. The external candidate is not integrated. Empirical accuracy and source-adjudicated phonology remain blocked by the missing independent gold corpus; no percentage should be reported.


## Handoff update — Lao G2P metric-schema hardening (2026-10-24)

- The first artifact (workflow [40092430175](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40092430175)) used schema v2 and called 0/36 exact cross-engine matches an `exact_match_rate`. This was implementation agreement over engineering fixtures, not accuracy, but the field name was too ambiguous.
- New branch `fix/label-lao-g2p-diagnostic-metrics-2026-10-24` changes the report to schema v3: `implementation_agreement_rate`, `independent_gold_count: 0`, `accuracy: null`, `score_status: NOT_SCORED_NO_INDEPENDENT_GOLD`; implementation mismatches and runtime errors are separated. A unittest locks this contract.
- Pending current-head CI and optional workflow. Do not merge until green. Preserve previous artifact as historical schema-v2 evidence; new workflow artifact will establish the schema-v3 result. Gold corpus remains TODO.


### Schema-v3 follow-up fix — 2026-10-24

The first schema-v3 optional workflow [40093135298](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40093135298) produced the report but exited with `NameError: runtime_errors` because the return statement still referenced the removed local summary variable. Fixed to use `summary["runtime_errors"]` and added a regression assertion. The artifact from this failed run confirms the schema-v3 metrics themselves were emitted correctly (0 independent gold, accuracy null, implementation agreement 0.0); the workflow remains IN_PROGRESS until a fresh run and verification suite both pass.


## Final checkpoint — Lao diagnostic schema v3 verified (2026-10-24)

- Branch head tested: `8656f6a45f3d8fd16e647fc4a600645213caaaf5`; PR #14 merged as 5f003928c495e82a97f3077729ea4ec50af044ba.
- Verification suite [40093370613](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40093370613) passed. Optional comparison [40093370619](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40093370619) passed and artifact was inspected.
- Artifact SHA-256: `91e77bc29bddc76a1a598eeb3f8eeb775fb0677a3ac86a507400edb675111d02`. Schema version 3, 36 cases, 0 runtime errors, implementation agreement 0.0, independent gold count 0, accuracy null, score status NOT_SCORED_NO_INDEPENDENT_GOLD, and no `exact_match_rate` key.
- First schema-v3 attempt [40093135298](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40093135298) exposed a stale `runtime_errors` reference in the exit-status path; fixed and regression-tested. The corrected run and full verification now pass.
- Smoke task DONE_VERIFIED; linguistic accuracy remains unmeasured because engineering fixtures are not independent gold. Keep lao2ipa disabled in production.


## Final merge checkpoint — Lao metric-schema hardening (2026-10-24)

- PR [#14](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/14) merged to main at `5f003928c495e82a97f3077729ea4ec50af044ba`.
- Final branch verification [40093508377](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40093508377) and optional schema-v3 comparison [40093508384](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40093508384) passed. The artifact was inspected: schema v3, 36 cases, zero runtime errors, implementation agreement 0.0, independent gold count 0, accuracy null, and no ambiguous `exact_match_rate` key.
- Earlier exit-status bug from run 40093135298 is fixed and covered by a regression test. The run is reproducible; phonological accuracy remains unmeasured until an independent gold corpus exists.


Authoritative readiness checkpoint — 2026-10-24 12:38 UTC

This section supersedes historical workflow-status statements above where they conflict with current evidence.

- Current main HEAD: 4b2e6e881951f633a32b3d21e761666f642201b6.
- Current-main verification: DONE_VERIFIED. Run 40093704069 succeeded after schema-v3 changes. Pages deploy 40091223724 succeeded on code-equivalent site sources before optional benchmark/docs changes; no later site-source change was made.
- External G2P diagnostic: DONE_VERIFIED as execution only. Schema-v3 artifact SHA-256 91e77bc29bddc76a1a598eeb3f8eeb775fb0677a3ac86a507400edb675111d02; 36 cases, zero runtime errors, implementation agreement 0.0, independent gold count 0, accuracy null, status NOT_SCORED_NO_INDEPENDENT_GOLD.
- Remaining TODO/BLOCKED: source-adjudicated lexical IPA gold corpus; source-backed tone contours and rule environments; complete vowel/coda/context coverage; differential review of the 36 engineering fixtures. Do not infer external output is wrong merely because it differs from engineering fixtures.
- Readiness: current engineering verification is green; linguistic completeness and accuracy remain unproven. This is a research prototype, not release-ready general-purpose transcription software.


## Fail-closed handling of unconsumed Lao orthography — 2026-10-24

### Finding
The parser already emitted `UNCONSUMED_AFTER_VOWEL:<suffix>` when a source suffix was not recognized. The core pipeline downgraded confidence but still retained the IPA and Ukrainian target derived from the recognized prefix. For a malformed or unsupported whole syllable, this could expose a partial prefix transcription as though it represented the entire source unit.

### Change prepared
- When this exact parser warning is present, clear the whole-unit IPA before candidate generation, so both candidate and practical Ukrainian outputs remain empty.
- Add rule trace `PHON-IPA-WITHHELD-UNCONSUMED-ORTHOGRAPHY` and set status to `EVIDENCE LIMITED`.
- Strengthen the existing regression case for `ກາລ` to assert IPA, practical output, and candidates are withheld while the parser warning remains visible.

### Verification boundary
- PR is [#17](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/17), based on main `e209fb73579032ea07bc08ca03b96db6bffe0c40`.
- First PR-head CI run [40112919607](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40112919607) executed the full Python suite: 61 tests passed and one new regression test errored because it used non-existent model attribute names (`candidates` and `rules_applied`). The test was corrected to use the actual dataclass fields (`ukrainian_candidates` and `rules`); this was a test-harness error, not a failed linguistic assertion. Corrected-head run [40112992134](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40112992134) passed on `b785011f39e3a5b6d37901cc3ea0fabc0899fa5d`. PR #17 was then merged as `af65215f606dc69df7d4d81c20781d53398f62ae`; post-merge `main` verification [40113408058](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40113408058) passed.
- This is a fail-closed integrity fix, not a phonological expansion. Existing tone rules and IPA correspondences are unchanged; empirical accuracy remains unmeasured until an independent gold corpus is adjudicated.


## IPA benchmark harness and external engine protocol — 2026-10-24

- Added `scripts/benchmark_ipa.py`, a standard-library-only harness with strict Unicode NFC exact match, code-point Levenshtein CER (diagnostic only), and explicit missing-prediction accounting. Every independently adjudicated gold row remains in each engine's denominator; omitted outputs cannot inflate accuracy.
- Added `data/benchmark/gold.tsv` and `data/benchmark/predictions.tsv` header templates plus `tests/test_benchmark_ipa.py` covering no-gold behavior, adjudication gating, diacritic preservation, missing rows, and mismatches.
- Added `docs/benchmarking-and-external-ipa.md`; linked the existing `data/external-ipa-renderers.json` inventory to the benchmark protocol. External candidates remain optional and disabled by default.
- PR is open; current CI is queued / not yet verified. Do not merge until hosted tests pass. Local GitHub access is unavailable from the current container due network/DNS failure.
- No adjudicated gold corpus was added and no accuracy score is claimed. Candidate engine language support, actual IPA semantics, exact versions, and model/data licensing still require verification. Registry presence and smoke execution are not evidence of accuracy.
- Required next acceptance: run the repository test suite including the new harness tests; inspect all generated-artifact checks; then populate the gold set only with source-located, independently adjudicated pronunciations and rerun all engines against the same held-out set.


## External IPA/G2P and benchmark continuation — 2026-10-24

- Registry and per-language evidence notes: `data/external-ipa-renderers.json` and `docs/benchmarking-and-external-ipa.md`.
- External outputs are diagnostics only unless compared against a versioned, independently adjudicated gold set. Engineering fixtures and source-attested dictionary entries are not automatically gold.
- Shared harness: `scripts/benchmark_ipa.py`; empty templates at `data/benchmark/gold.tsv` and `data/benchmark/predictions.tsv`; tests at `tests/test_benchmark_ipa.py`.
- New research branch: `research/third-party-ipa-systems-20261024`. PR and workflow outcomes must be checked before this work is considered integrated.
- Keep IPA adaptation boundary: source spelling → structural parse → source phonology → typed IPA → Ukrainian adapter. Third-party candidates remain optional and disabled in production.
- Current true blocker: a source-located, independently adjudicated language-specific gold corpus with a documented dialect and IPA convention. Do not report accuracy until it exists.


### Verified status as of 2026-10-24

PR #20 merged as `210f673867bfe107e5d6ad8f85b284699defca9b`. Latest main verification and external comparison passed; 66 Python tests passed. `lao2ipa 1.0.0` smoke: 36 inputs, 0 runtime errors, 0/36 implementation agreement, independent gold=0, accuracy=null. Durable examples: `data/benchmark/runs/external-g2p-smoke-2026-10-24.json`; full artifact: https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40119990663/artifacts/12569454564.

- Keep IPA adaptation boundary: source spelling → structural parse → source phonology → typed IPA → Ukrainian adapter. Third-party candidates remain optional and disabled in production.
- Current true blocker: a source-located, independently adjudicated language-specific gold corpus with a documented dialect and IPA convention. Do not report accuracy until it exists.


## Tone-only decomposition follow-up — 2026-10-24

- Branch `research/lao-tone-decomposition-rebased-20261024` ports the tone-only diagnostic onto the current main while preserving the detailed mismatch classifier from PR #26.
- The comparator reports strict exact match and detailed mismatch categories unchanged, plus separate `tone_stripped_*_diagnostic_only` counts computed after removing only IPA tone letters from derived copies. Raw IPA, length marks, separators and production output are untouched.
- Unit tests cover tone-only vs non-tone mismatches and the `accuracy: null` gate. The earlier categorized artifact gave 29/36 tone-suffix-only cases and 7 non-tone/format cases, but this is a diagnostic decomposition—not accuracy or proof tone is dispensable.
- Acceptance: current-head unit tests and optional `lao2ipa` workflow. Independent gold remains absent.


### Latest Lao external-G2P diagnostic — 2026-10-24

- Latest comparator run [40122001269](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40122001269) passed: 36 probes, 0 runtime errors, strict exact agreement 0/36. A separate tone-letter-stripped diagnostic matched 29/36 (80.6%) and left 7 tone-plus-length/segmental/offglide cases for review. This is not accuracy: independent gold count is 0 and tone remains contrastive. Artifact ZIP SHA-256: `63833a43fd2c9309505dcf8a96bb7dc46052993f3834307e77524b586e020816`.


### Benchmark gold provenance guard — 2026-10-24

- Benchmark scoring now fails closed if an ADJUDICATED row lacks non-empty IPA, a source locator, or a profile. The regression tests are included in PR #31; do not merge until current-head CI passes.
- The independent gold corpus is empty. Strict agreement remains 0/36; tone-stripped diagnostic agreement is 29/36 (80.6%) and is not accuracy. Seven other mismatches require review; tone remains contrastive.
