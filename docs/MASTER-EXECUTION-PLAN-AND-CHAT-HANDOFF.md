
## Lao external G2P mismatch taxonomy — 2026-10-24

- Branch `research/lao-g2p-diagnostic-categories-rebased-20261024` updates the existing comparator instead of adding a parallel runner.
- Categorized pinned run [40121272427](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40121272427): 36 engineering cases, 0 runtime errors, 0/36 exact implementation agreement, independent gold=0, accuracy=null. Categories: 29 tone-suffix-only, 2 offglide-convention, 4 segmental/vowel-sequence, 1 tone+length. Durable report: `data/benchmark/runs/external-g2p-smoke-2026-10-24.json`; artifact ZIP SHA-256 `a2fea18c48e337ce37b070b2da9ff2e5236b51295f80100d2ebae06a4478d4b8`.
- The category labels are heuristic review hints only. Lao tone may be contrastive, so tone-suffix differences are not automatically harmless. Prioritize source-located adjudication of tone convention and the four segmental/vowel-sequence cases.
- Unit tests for the classifier passed on the previous branch head; full current-branch CI and optional comparison are required before merge. No accuracy or engine winner is claimed.
# Master execution plan and chat handoff

Last reviewed: 2026-10-31
Repository: https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System
Baseline branch: `main`
Baseline commit: `0b99fd451507717664a0190dbc3bcfb7069ce15c` (PR #73 squash merge into `main`)
Work branch: `chore/postmerge-handoff-20261031` (PR #74; exact-head run 41190577692 passed)
Current implementation baseline: PR #73 is merged as `0b99fd451507717664a0190dbc3bcfb7069ce15c`; its final PR-head verification [41190329422](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190329422) passed on `e952f91d1df6678d1c1c91552fcf46a3de9301fa`. Post-merge `main` verification and Pages deployment are not yet independently confirmed; see `LAO-POSTMERGE-VERIFY-001`.

## Status vocabulary
Use: `TODO`, `IN_PROGRESS`, `PARTIAL`, `BLOCKED`, `DONE_VERIFIED`, `DEFERRED`, `NOT_APPLICABLE`. `PARTIAL` means implementation exists but at least one acceptance criterion remains open.
Do not mark code changes `DONE_VERIFIED` until the current commit's relevant checks have actually passed.

## Current audit summary

The project has separate Python and browser engines, canonical Lao consonant/vowel/coda/tone registries, Ukrainian correspondences, source/claim CSVs, regression suites, and methodology/limitations/audit documentation. Current main includes the source-aware romanization mode, Ukrainian `/ʃt͡ʃ/ → щ` mapping, vertical service layout, and public research-status reconciliation. PR #73 is merged to main at `0b99fd451507717664a0190dbc3bcfb7069ce15c`; its exact PR-head run [41190329422](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190329422) passed 196 deterministic tests and the repository audit/build gates. The prior exact-main run [41188910015](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41188910015) and prior Pages deployment [41188708689](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41188708689) predate PR #73. Post-merge verification for the new main head is unconfirmed; PR #74's exact-head run [41190577692](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190577692) reran the full verification suite on the merged code plus hygiene/documentation changes.

Audit found and fixed: (1) Python vowel-pattern precedence; (2) parser warnings incorrectly coexisting with an `ESTABLISHED` status; (3) missing Python structures for short /o/ in closed syllables and standalone ຽ; (4) a browser segmentation tie where `ກົວະ` was split as `ກົ|ວະ`; (5) missing closed-coda constraints for the short A2 and AWW_SHORT_ALT spelling forms. Shared fixtures are consumed by both engines. Full Python, browser, build, data regeneration, reproducibility and built-page checks passed for the 36-case vowel fixture suite in [run 39484094983](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39484094983). The tone/rhyme correction then passed the final PR-head workflow [41190329422](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190329422): Python 97, browser 47, romanization 19, syllable crosswalk 27, web layout 6, audit, build, generated-data reproducibility and built-page/asset checks. The shared fixtures are engineering regression cases, not an independently adjudicated gold corpus.

## Agent methodology and repository hygiene — 2026-10-31

- Added root `AGENTS.md` as the project-specific entry point for future coding agents. It preserves this handoff as the canonical execution register and distills selected practices from Superpowers, Matt Pocock's engineering skills, and Ponytail. The external repositories are linked at pinned commits; their files are not copied into this repository and no plugin/runtime dependency was added.
- The current ChatGPT environment already exposes Superpowers skills. The other two repositories were located and their relevant source instructions were read through GitHub. This is method adoption, not an installation of third-party runtime code.
- A Ponytail-style dependency audit found that both CI workflows ran `npm install` although `package.json` had no runtime or development dependencies and the test/build scripts use Node built-ins plus Python. The empty `devDependencies` and no-op `prepare` entries, plus both no-op install steps, are removed. The verify workflow's checkout/setup-python/setup-node actions are also aligned to v5/v6/v5, matching the already-updated Pages workflow and avoiding the Node 20 deprecation warning seen on the first PR run. Exact-head CI must verify the resulting dependency-free, Node 24-compatible workflow before this task is closed.
- GitHub inventory at this checkpoint: 71 branches including `main` and this new work branch; 69 historical PRs, none open, 58 merged and 11 closed without merge. The 69 pre-existing non-main branches were compared with current `main`. The unmerged PRs were confirmed as superseded, duplicates, or temporary validation work: #42 by #43; #33 by #34; #32/#30/#29/#25 by the merged gold-provenance chain (#31 and follow-up #34); #27 by #28; #23 by #26; #21 by #22; #3 by the finalized web implementation; and #4 was temporary CI validation only. No unique code was ported from these stale-base branches. All existing branches were preserved; no branch was deleted or force-updated.
- The API-backed GitHub workflow was used because this execution environment has no local repository checkout and its container has no outbound network. Consequently, local `git` and test commands could not be run here; the exact PR-head GitHub Actions run is the verification gate.


## Pages action runtime follow-up — 2026-10-31

- The successful Pages run 41188440580 emitted Node 20 deprecation warnings from the nested upload-artifact action and deploy-pages action, although both jobs passed.
- Official upstream metadata confirms upload-pages-artifact v5 uses upload-artifact v7 (node24), and deploy-pages v5 declares node24. The Pages workflow now references upload-pages-artifact@v5 and deploy-pages@v5.
- Exact Pages build/deploy verification is required before this task is closed. This is CI maintenance only and does not alter site content or linguistic behavior.


## Pages action runtime follow-up — verified 2026-10-31

- PR #72 merged as `649973f320a8eb0e6cf2d927c9b90add5cdcdd68`, upgrading `actions/upload-pages-artifact@v5` and `actions/deploy-pages@v5` after the prior Pages run exposed nested Node 20 warnings.
- Official upstream metadata was checked at the pinned release tags: upload-pages-artifact v5.0.0 invokes upload-artifact v7.0.0 (`runs.using: node24`); deploy-pages v5.0.1 also declares `runs.using: node24`.
- Exact-main verify [41188708711](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41188708711) passed. Pages build and deploy [41188708689](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41188708689) passed; no Node 20 action-runtime warning appears in the Pages logs. npm CLI still emits a separate non-fatal `DEP0040` punycode warning.
- No site content or linguistic behavior changed. This closes CI action runtime maintenance only; it does not close manual visual QA or linguistic evidence gates.

## Execution register

| ID | Priority | Status | Scope / evidence | Acceptance criteria / dependencies |
|---|---|---|---|---|
| LAO-AUD-001 | P0 | DONE_VERIFIED | Repository tree and key Python/browser engines, registries, tests, workflows, audit/methodology/limitations docs inspected on 2026-10-20 | Current tracked files and key modules identified; no claim that every row of every registry has been scientifically adjudicated |
| LAO-PY-001 | P0 | DONE_VERIFIED | `src/lao_ukrainian/parser.py`; generic empty-suffix patterns could precede specific vowel patterns | Python tests and new regression tests passed at code commit `3695815dfbc3f48d8bd6a4e4395aa46f44e8e5e3`; run [39482443085](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39482443085) |
| LAO-PY-002 | P0 | DONE_VERIFIED | `tests/test_structural_vowels.py`; added OE, OEE and IA_LONG precedence regressions | New tests and full Python + JS + build/reproducibility workflow passed at code commit `3695815dfbc3f48d8bd6a4e4395aa46f44e8e5e3`; run [39482443085](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39482443085) |
| LAO-STATUS-001 | P0 | DONE_VERIFIED | `src/lao_ukrainian/core.py` downgrades `ESTABLISHED` when parser warnings exist; regression test in `tests/test_core.py` | CI run [39482633937](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39482633937) passed for test commit `ca0e8d39493bad65918e39e13ba79776438ac0b1` |
| LAO-RESULT-002 | P0 | DONE_VERIFIED | PR #53 merged as `58385a0f36953c970d936123cb67192600510067`; incomplete short-vowel syllables now withhold IPA, Ukrainian candidates/output, tone and contour; Python/browser share `tests/fixtures/tone_contour_cases.json`. Exact-head test run [40221383984](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40221383984) passed. | This closes a result-contract integrity gap only. It does not adjudicate the missing-coda phonetics or establish acoustic tone contours; independent gold remains 0. |
| LAO-PARSER-001 | P0 | IN_PROGRESS | PR #40 merged the strict coda-final-grapheme guard; PR #43 then aligned Python/browser handling of unconsumed material before a preposed vowel and closed a segmentation bypass that could rescue a substring from malformed `xເເກ` input. The whole malformed token now remains unresolved, with IPA and Ukrainian output withheld. | Exact-head CI [40208462464](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40208462464) passed Python and browser tests after the regression was corrected; PR #43 merged as `0336419ad612072b61e12b9e92b6bb6b67ff9284`. Differential corpus and source-level coda review remain open. |
| LAO-TONE-001 | P0 | IN_PROGRESS | Tone rules are explicitly scoped to a Vientiane-oriented reference matrix and link to `CLM-LAO-VIENTIANE-TONE-MATRIX`; PR #46 merged as `4a01b1bf37ee0fae6579430a3ada33680e4debb9`. Exact-head CI [40209554020](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40209554020) passed rule-ID, enum, claim/source linkage and unique-winner tests across the declared class × live/dead × length × mark combinations. | Source-level review of examples and dialect scope remains required; distinguish phonological tone categories from measured surface contours. Contract coverage is not acoustic validation. |
| LAO-TONE-MARK-DOMAIN-001 | P0 | DONE_VERIFIED | PR #73 merged to `main` as `0b99fd451507717664a0190dbc3bcfb7069ce15c`; final PR-head run [41190329422](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190329422) passed Python 97, browser 47, integration 19, syllable 27, layout 6, audit, build and generated-data reproducibility. | This closes the marked-syllable selector domain and rare-mark implementation contract only. Broader tone-category/source adjudication and empirical contour validation remain under LAO-TONE-001. |
| LAO-POSTMERGE-VERIFY-001 | P1 | BLOCKED | PR #73 is merged, and exact PR-head verification [41190329422](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190329422) passed. The available GitHub connector's workflow-run endpoint only returns PR-triggered runs; the post-merge `push` run IDs and Pages deployment run could not be retrieved. Firecrawl also returned an insufficient-credits error, so no external-page fetch was possible. | Verify exact `main` commit `0b99fd451507717664a0190dbc3bcfb7069ce15c` on the `verify` workflow, verify Pages build+deploy after PR #73, and inspect the public pages. Do not infer success from PR CI or the previous Pages deployment. |
| LAO-VOWEL-001 | P0 | IN_PROGRESS | Inventory has 34 vowel IDs in `vowels.csv`, 21 generalized rows in `vowel_structures.csv`, and separate Python/JS pattern logic; the CSVs do not encode all parser spellings (e.g. several alternative UO spellings and explicit onset placeholders) | Reconcile registry, structures and both parsers; source each pattern; add full positive/negative fixture coverage; do not infer evidence from implementation output |
| LAO-CODA-001 | P0 | IN_PROGRESS | `data/lao/codas.csv`, `data/lao/consonants.csv`; Python coda detection requires the last grapheme; `tests/fixtures/coda_cases.json` covers 9 currently registered final graphemes | Shared Python/browser coda fixtures and invalid-final test pass CI; still requires source-level review of the coda inventory and exhaustive invalid-final variants |
| LAO-CLUSTER-001 | P0 | TODO | `docs/limitations.md` explicitly says initial-cluster model is incomplete | Dedicated grammar/tests for valid clusters, high-class silent digraphs and boundary ambiguities |
| LAO-UNICODE-001 | P1 | IN_PROGRESS | Python and browser now reject C0 controls other than explicit line whitespace, DEL U+007F and C1 U+0080–U+009F; tests cover DEL/C1 and preserve CRLF. PR #44 merged as `5353e737a8e47136fc1442a695dbd2b5724cdfc1`; exact-head CI [40208623562](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40208623562) passed. | Complete malformed-mark, normalization, mixed-script and status/output parity matrix; keep unsupported characters visible and never infer pronunciation from Unicode recognition alone. |
| LAO-UKR-001 | P1 | PARTIAL | `data/lao/ukrainian_correspondences.csv`, `src/lao_ukrainian/target.py`, `tests/test_target.py`, `tests/fixtures/target_output_cases.json` | The IPA adapter and browser mirror preserve aspiration, /h/ vs /ɡ/ vs /x/, postalveolar fricatives, affricates, palatalization and the Ukrainian /ʃt͡ʃ/→щ sequence. Remaining acceptance: independent expert review of all target choices and a broader adjudicated IPA target corpus. |
| LAO-UA-SHCH-001 | P1 | DONE_VERIFIED | data/lao/ukrainian_correspondences.csv maps exact /ʃt͡ʃ/ to щ; Python longest-match adapter and generated browser correspondence map consume the same canonical row. Source claim CLM-UA-SHCH-SEQUENCE cites the Encyclopedia of Modern Ukraine and the Journal of the IPA. | Test-first regression observed шча instead of щ before implementation; exact-head CI [41140937597](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41140937597) passed Python 94, browser 47, integration 19, syllable crosswalk 27, layout 5, audit (70 UA mappings, 22 sources, 45 claims), build and generated-data reproducibility. |
| LAO-CORPUS-001 | P0 | BLOCKED | No expert-adjudicated Lao IPA gold corpus exists; independent gold count remains 0 and accuracy is null. The repository cannot manufacture this evidence from its own regression fixtures or from another engine's output. | Requires a licensed/source-attributed corpus, explicit dialect and IPA conventions, a qualified Lao phonetics reviewer, adjudicated layer-by-layer expected outputs, and a declared denominator. |
| LAO-G2P-001 | P1 | DONE_VERIFIED | Pinned lao2ipa==1.0.0 workflow [40092430175](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40092430175) completed; artifact inspected: 36 cases, 0 runtime errors, 0 external fixture matches and 0 exact cross-engine matches; verification suite [40092430173](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40092430173) passed | Preserve the diagnostic artifact and manually classify output conventions; do not interpret engineering-fixture disagreement as accuracy. Accuracy remains blocked by LAO-CORPUS-001 |
| LAO-G2P-002 | P1 | DONE_VERIFIED | Schema-v3 metric hardening verified in [workflow 40093370619](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40093370619); artifact inspected and no ambiguous exact_match_rate key remains | Report includes implementation_agreement_rate, independent_gold_count=0, accuracy=null, score_status=NOT_SCORED_NO_INDEPENDENT_GOLD; verification suite [40093370613](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40093370613) passed || LAO-EVIDENCE-001 | P1 | PARTIAL | Evidence registries now include CLDR, BGN/PCGN, Ukrainian щ and source-aware romanization claims; audit script resolves all source IDs. | Rule-by-rule exact passage/page/section review, conflict handling, dialect scope and licensing/redistribution checks remain open. |
| LAO-STATUS-PUBLIC-001 | P1 | DONE_VERIFIED | Public `index.html` and `system.html` now report the 2026-10-31 merged implementation, correct the supported-subset wording for ໜ/ໝ, state the exact `/ʃt͡ʃ/ → щ` target sequence, link exact-main CI/Pages evidence, and keep gold=0/accuracy=null explicit. TDD red run [41183451808](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183451808) failed on the stale copy as expected; exact-head run [41183689662](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183689662) passed Python 94, browser engine 47, romanization integration 19, syllable crosswalk 27, web layout 6, audit, harness syntax/CLI, build, generated-data reproducibility and built-page/asset checks. | Public research claims match merged implementation and evidence without overstating linguistic validation; automated regression protects the status text. |
| LAO-DOCS-001 | P1 | PARTIAL | README, methodology, limitations, validation, final audit and handoff now reflect the merged source-aware romanization mode and exact-head CI. | Full scientific source audit, expert review and visual QA must be completed before publication-grade documentation status. |
| LAO-RELEASE-001 | P2 | DEFERRED | `CITATION.cff` and MIT `LICENSE` are present; no tag or archive was created. | Release publication remains deferred until P0 linguistic evidence gates are closed and the owner explicitly authorizes publication. |
| LAO-AGENT-WORKFLOW-001 | P1 | DONE_VERIFIED | Root `AGENTS.md` links pinned Superpowers, Matt Pocock and Ponytail source commits and records project-specific linguistic, testing, branch and evidence invariants. Exact PR-head verification [41188217991](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41188217991) passed on `e2b0effdfb2091a3f9ca1450d32b6f0e110d29ba`. | Method references are pinned and synthesized rather than copied; guidance complements the existing canonical handoff. |
| LAO-CI-DEPS-001 | P2 | DONE_VERIFIED | Removed empty npm dependency metadata, no-op `prepare`, and both no-op `npm install` steps; aligned verify action versions to Pages (checkout v5, setup-python v6, setup-node v5). Exact PR-head run [41188217991](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41188217991) passed without npm installs or Node 20 action-runtime warnings; generated data remained reproducible. | No JS dependency installation is needed for the current built-in Node test runner and Python build. A separate npm CLI `DEP0040` warning remains non-fatal and is not attributed to project code by the available log. |
| LAO-PAGES-ACTIONS-001 | P2 | DONE_VERIFIED | PR #72 merged as `649973f320a8eb0e6cf2d927c9b90add5cdcdd68`; Pages run [41188708689](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41188708689) passed build and deploy using `upload-pages-artifact@v5` and `deploy-pages@v5`. Logs contain no Node 20 action-runtime deprecation warning. | Exact main Pages build and deploy passed. A separate npm CLI `DEP0040` warning remains non-fatal. |
| LAO-DEPLOY-001 | P1 | DONE_VERIFIED | Main commit `649973f320a8eb0e6cf2d927c9b90add5cdcdd68` passed Pages build and deploy in [run 41188708689](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41188708689); the Pages actions now use Node 24-compatible v5 majors. | Workflow and deployment artifact checks passed. Manual visual/browser and keyboard review remain under LAO-UI-001; deployment is not phonetic validation. |
| LAO-UI-001 | P1 | IN_PROGRESS | UI PRs #61–#64 and the romanization selector in PR #65 are merged and deployed; responsive and accessibility assertions pass CI. | Complete actual visual QA with screenshots at 1440px, 768px and 390px, keyboard-only interaction review and copy-flow verification in a real browser; do not mark complete from CI alone. |
| LAO-ROM-UA-001 | P1 | DONE_VERIFIED | PR #65 merged to main as `b2e1187629829b4242aa2430a9901d264910eea1`; exact-head main verification [41142746494](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41142746494) passed. The source-aware romanization branch validates onset, source vowel ID and supported coda against the CLDR/BGN syllable parse. In addition to kh/th/ph → к'/т'/п' and standalone h → г, it supports the BGN/PCGN silent-hoa rule for ຫງ/ຫຍ/ຫນ/ຫມ/ຫລ/ຫຼ/ຫວ and atomic ໜ/ໝ, preserving the underlying sonorant rather than an audible /h/. Source vowel IDs are extracted from the IPA-first structural parser's `VOWEL:<ID>` rule trace; a nucleus mismatch is withheld. This resolves `kam` using source evidence: ກາມ = A + coda ມ, while ກຳ = AM nucleus, even though both romanize to `kam`; without Lao evidence, `kam` remains ambiguous. `niav` likewise remains ambiguous alone but can be resolved by the source syllable ໜ + IA_LONG + coda ວ. The UI trace now shows source onset, vowel ID and coda plus the romanized parse, and labels the complete source-structure cross-check. New evidence claims/source and tests cover silent nasal ligatures, vowel mismatches and source-resolved ambiguities. | Exact-head CI [41137893545](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41137893545) passed at d0b9a585a3edf2ad0c89ba9f9b10fcbc35aa62e6: audit, Python 92, browser engine 46, romanization integration 19, syllable crosswalk 27, layout 5, external-G2P harness syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks. The tests include source-chain cases ຂາ→kha→к'а, ຮາ→ha→га, ກາຮາ→kaha→кага, ໜຽວ→niav→ніао, ໝາ→ma→ма, and ກາມ vs ກຳ→kam with different source analyses. Manual visual/keyboard QA, expert review of remaining consonant/lexical cases and full CLDR coverage remain separate gates. |

## Coverage matrix (initial; not yet a scientific completeness claim)

| Domain | Current evidence | Coverage judgment | Next action |
|---|---|---|---|
| Unicode/NFC | Python and JS normalization/validation tests | Partial | Add malformed ordering, control, ZWSP and cross-engine parity tests |
| Initial consonant classes | Consonant registry + basic class tests | Partial | Check all modern consonants and class exceptions against independent sources |
| Vowels and length | 34 vowel IDs; 21 generalized structure rows; shared cross-engine fixtures cover the core vowel set and known precedence/segmentation edge cases | Partial; registry-to-Python coverage test and regression fixtures pass CI, but not all spellings have independent source adjudication | Expand negative/alternative spellings and attach exact source passages to each rule |
| Syllable structure | Syllable parser and browser segmentation tests | Partial; no complete lexical segmentation claim | Expand legal/illegal structure corpus and clusters |
| Codas | Shared fixture covers 9 registered final graphemes; tests reject a coda before unconsumed trailing material and reject unregistered final ສ | Partial; shared Python/browser coda fixtures passed CI; phonological inventory still needs independent review | Add broader invalid-final and coda-position cases; reconcile coda registry with the ʔ entry and actual orthographic representation |
| Tone marks | 17-rule Vientiane matrix; all eight marked selectors require `live`; `mai ti`/`mai catawa` are middle-class-only and source-linked to Appen Butler Hill p.14; shared fixture has 37 cases | Selector-domain implementation and Python/browser parity fixture verified in PR #73 exact-head run 41190189983; source-level contour and dialect adjudication remain partial | Continue source-by-source tone-category review and independent acoustic contour validation; do not infer accuracy from selector tests |
| Tone categories | Vientiane-oriented matrix | Partial | Source-level review and independent expected examples |
| Surface tone contours | Contours in data | Not fully empirically verified | Treat contours as descriptive conventions unless supported by phonetic measurements |
| IPA | Generated from graphemic/phonological tables | Partial | Independent expected IPA corpus, segment-by-segment review |
| Ukrainian adaptation | Canonical correspondence table | Partial; project policy, not national standard | Independent review and target-specific examples |
| Exceptions/names | Limitations documented | Incomplete | Add named/loan/ambiguous examples and preserve unresolved statuses |
| Browser/Python parity | Shared vowel fixture has 36 expected-IPA cases; shared tone fixture has 37 cases and is consumed by Python and browser suites | Vowel fixture and tone status/contour/output parity for the declared cases passed PR #73 run [41190189983](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190189983); full lexical status/coda/target-output parity remains unverified | Extend source-adjudicated cross-engine fixtures beyond the bounded declared cases |
| CI/build/deployment | Main verify and Pages deploy both passed for `a001046462de564dd2cb89e9237caa221624163c` in runs [41142874231](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41142874231) and [41142874311](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41142874311) | Engineering and deployment gates verified; no manual visual QA | Perform 1440/768/390px screenshots and keyboard-only browser QA |
| Sources and reproducibility | 23 evidence sources, 47 claims; canonical CSV-to-browser generation and drift checks | Audit and reproducibility checks passed in PR #73 run [41190189983](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190189983); full source-by-source adjudication remains partial | Continue exact passage/page/section review, dialect scope and licensing/redistribution checks |

## Current continuation — 2026-10-30 (interface design)

- Current default-branch baseline: `main` at `08e4d0c0daa8cf7eb758b93a75520d30fa2cd16b`.
- Reused the already-open, directly relevant PR #61 and its branch `design/lao-layout-20261030`, based on the current default branch. No competing PR was merged or closed.
- Latest commit: `21729be93cb5390d2c377d66e4618fd396a4e6b3`. The branch is 10 commits ahead of `main`, 0 behind. PR #61 remains open and mergeable.
- Implemented a Lao-script wordmark and a real `ຂາ → kʰaː → к'а` specimen; retained the established red/blue palette and the romanization → IPA → Ukrainian output order; improved responsive composition, focus/skip navigation, methodology navigation semantics and copy feedback for all three output layers.
- Adapted React Bits micro-interaction principles in native CSS/JavaScript. No React runtime or third-party component source was added because this repository is a vanilla HTML/CSS/JavaScript service.
- Updated `docs/DESIGN-SYSTEM.md` and added CI assertions for the new UI/accessibility contract.
- Verification: GitHub Actions verify run [41110855525](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41110855525) completed successfully for the exact latest commit. The workflow runs Python tests, external-G2P harness syntax/CLI checks, Node/browser engine tests, build/data regeneration, generated-data drift checks and built-page/asset/UI assertions.
- Remaining acceptance gate: visual browser review at 1440px, 768px and 390px, including keyboard-only use and confirmation against a live Pages deployment. A browser screenshot/preview runtime was not available in this session, so the design task remains `IN_PROGRESS`, not `DONE_VERIFIED`.

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
| LAO-UKR-001 | PARTIAL | Python target.py and browser engine both map from the canonical IPA correspondence registry; shared target fixtures and direct consonant-policy tests cover the implemented subset. The target policy remains project-specific and needs independent expert review and broader adjudicated coverage. |
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


## Tone-only decomposition follow-up — merged 2026-10-24

- PR #28 merged the diagnostic classifier and tone-stripped comparison. Raw IPA and strict exact-match results remain unchanged; tone stripping is diagnostic-only and never used for production output.
- Latest successful categorized run is [40122329060](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40122329060): 36 inputs, 0 runtime errors, 0/36 strict exact matches; 29/36 tone-only string matches after diagnostic stripping (80.6%), with 7 other mismatches requiring review. Independent gold remains 0, so accuracy is null.

## IPA gold provenance gate — merged 2026-10-24

- PR #31 merged the fail-closed benchmark validation. Every row marked `ADJUDICATED` must have non-empty `gold_ipa`, `source_id`, and `profile`; otherwise scoring stops with an error rather than silently changing the denominator.
- Regression tests passed on the merged head. This validates metadata completeness, not the truth of a pronunciation label. Independent Lao gold remains absent.

## Lao tone-stripped diagnostic results — 2026-10-24

- Latest categorized artifact [workflow 40122329060](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40122329060): 36 inputs, 0 runtime errors, strict implementation agreement 0/36, tone-stripped agreement 29/36 (80.6%) diagnostic-only, 7/36 remaining non-tone/format/length mismatches, independent gold=0, accuracy=null.
- Detailed categories remain: 29 tone-suffix-only, 2 offglide convention, 4 segmental/vowel-sequence, 1 tone+length. The tone-stripped diagnostic does not change raw outputs or strict scoring; tone can be contrastive and must not be removed from production IPA.
- Durable summary: `data/benchmark/runs/external-g2p-smoke-2026-10-24.json`; artifact SHA-256 `2b7f3c5e3c02814413e42b9f2031849c21630fba9958a7e6a38de92f7a63ff55`.

## Authoritative current-head checkpoint — 2026-10-25

This checkpoint supersedes earlier notes that referred to an older main SHA or described the schema-v3 smoke as still pending.

- Current `main`: `649c4bb51b51dbc99bfe83a7fce19d0eff2b18fa`.
- Current-main verification [40124496409](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40124496409): `success`.
- Latest categorized comparator evidence [40122329060](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40122329060): 36 inputs, 0 runtime errors, strict string agreement 0/36, tone-stripped agreement 29/36 (diagnostic only), 7 remaining non-tone/format/length mismatches. Independent gold remains 0; accuracy null. Tone stripping is never a production normalization.
- Engineering smoke/CI is DONE_VERIFIED. Source-by-source tone and composite-vowel adjudication, malformed/unsupported input coverage, coda representation review, target-policy review and independent Lao IPA gold remain PARTIAL/BLOCKED. The external engine is not promoted to production and no accuracy percentage is justified.


## Conservative parser contract regression — 2026-10-25

- PR #39: https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/39
- Added `tests/test_conservative_parse_contracts.py` to assert that a legal coda is accepted only at the end of the remaining syllable material and that trailing vowel structure is surfaced as unconsumed rather than silently discarded.
- Verification: `verify` workflow run [40192520398](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40192520398) completed successfully on commit `444d64d30e79dee48b7c98ed1094bb2ff4a1af97`.
- These are parser invariants, not source-adjudicated IPA gold. The independent gold count remains 0 and accuracy remains null; tone/composite-vowel adjudication remains blocked by source-located evidence and expert review.


## Parser fail-closed follow-up — 2026-10-25

- Branch: `fix/reject-lao-unconsumed-before-coda-20261025`.
- Structural defect fixed in `src/lao_ukrainian/parser.py`: the coda finder previously accepted any remaining string whose last character was a legal coda, so an input such as `ກາກງ` could be treated as if the preceding `ກ` did not exist. A coda is now accepted only when it is the sole remaining grapheme; otherwise the full remainder is marked `UNCONSUMED_AFTER_VOWEL` and downstream IPA/target output is withheld.
- Test-discovery defect found and fixed: `tests/test_conservative_parse_contracts.py` used bare pytest-style functions, while `.github/workflows/verify.yml` runs `python -m unittest discover -s tests -v`. Those three functions were therefore not collected by the configured CI command. Converted them into a `unittest.TestCase`, preserving the existing two controls and adding the malformed-prefix-before-coda regression.
- Verification: current branch run [40195428537](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40195428537) **passed**. The log confirms all three `ConservativeParseContracts` tests were executed and reports `Ran 75 tests ... OK`; browser tests, build/regeneration, reproducibility, and built-page/asset checks also passed. This is structural correctness evidence, not phonetic accuracy evidence.
- PR: [#40](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/40). Not merged in this pass.
- Still blocked for scientific completion: independent adjudicated Lao IPA gold remains 0; the existing 36-case external G2P comparison has 0/36 strict string matches and 7 non-tone/format/length mismatches after a tone-only diagnostic. Do not convert the new structural fix into a higher accuracy claim.

- End-to-end guard added in `tests/test_core.py::test_unconsumed_material_before_legal_final_withholds_full_output`: the malformed example now must have `EVIDENCE LIMITED`, no phonemic IPA, no practical Ukrainian output, no candidates, and a retained unconsumed-material warning.
- Latest exact-head verification after the end-to-end test: [run 40195680085](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40195680085) **passed**, `Ran 75 tests ... OK`, browser engine tests, build/regeneration, generated-data reproducibility, and built-page asset checks. Independent gold remains 0.


## Tone-rule provenance hardening — 2026-10-25

- Added the exact SEAsite / Northern Illinois University Vientiane tone-chart URL as `SRC-SEASITE-TONECHART` and registered a scoped claim with Ueda's peer-reviewed Vientiane phonology paper.
- Each canonical `data/lao/tone_rules.csv` row now declares `profile=Vientiane` and `evidence_id=CLM-LAO-VIENTIANE-TONE-MATRIX`. A new test resolves every row's claim and source IDs against the existing evidence registries.
- The citation supports the five-tone Vientiane-oriented class/live-dead/length/tone-mark matrix. It does **not** validate the repository's exact IPA contour symbols acoustically, nor does it justify generalizing to every Lao variety. The 2020 Nam Pua study and the W3C/R12A notes demonstrate why dialect and contour convention must remain explicit.
- Acceptance: exact branch-head CI must pass Python, browser, generated-data/reproducibility and build checks. The generator intentionally exports only runtime columns, so this evidence metadata must not change browser output.
- Still open: source passage/page-level audit for each tone rule, adjudicated acoustic contours, full cluster/coda coverage, and independent lexical gold. No accuracy claim is made.


## Pre-onset source-material guard — 2026-10-25

- Found a Python/browser contract gap: the browser already required all material before the onset to be empty or exactly one recognized preposed vowel, but Python only checked `before.endswith(pre)`. Malformed `xເເກ` could match the long-`ເ` template and silently discard the extra prefix.
- Python now applies the same allowed-prefix contract as the browser. Parser/core and browser tests assert that malformed input has no IPA or Ukrainian target output and records `UNCONSUMED_BEFORE_ONSET`.
- Exact-head `verify.yml` must pass Python tests, browser tests, generated-data reproducibility and build checks.
- This is parser integrity, not a phonological mapping. Lao cluster coverage and independent gold remain open.


- Test-first note: the first browser regression expected `null`, but the browser's existing unresolved-result contract represents missing IPA/target as an empty string. The implementation already withheld both outputs; the test now checks absence rather than requiring a specific null representation. Python still asserts `None` through its typed model.


## Lao malformed-prefix segmentation follow-up — 2026-10-25

- The first PR #43 CI run exposed a real browser defect: the per-syllable parser rejected `xເເກ`, but the word segmenter could split the malformed token and retain a plausible substring. This is an implementation bug, not merely an assertion mismatch.
- `analyzeWord` now checks material before the first Lao onset before dynamic segmentation. If it is not empty or exactly one recognized preposed vowel, the entire token is retained as one unresolved unit with no IPA or Ukrainian output.
- The browser regression asserts whole-token preservation, withheld outputs, and a diagnostic. Exact-head CI must pass before PR #43 is eligible for merge.


## Unicode control-character parity — 2026-10-25

- Found a validation gap in both runtimes: C0 controls were rejected (except line whitespace), but DEL U+007F and C1 controls U+0080–U+009F were not classified as controls consistently with Unicode control semantics.
- Python `validate_unicode` and browser `validateInput` now reject DEL/C1 controls; tests cover U+007F, U+0085 and U+009F while preserving accepted CRLF behavior.
- This is an input-integrity fix, not a phonological rule. Full branch-head CI must pass before merge.


## Post-merge reconciliation — 2026-10-25

- PR #40 strict coda guard is merged; PR #41 tone provenance is merged; PR #43 pre-onset guard and whole-token segmentation fix is merged as `0336419ad612072b61e12b9e92b6bb6b67ff9284`.
- PR #43's exact-head CI [40208462464](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40208462464) passed the complete workflow, including Python, browser, G2P harness syntax/CLI, build, generated-data reproducibility and page/asset checks.
- PR #44 added DEL/C1 control rejection in both runtimes and merged as `5353e737a8e47136fc1442a695dbd2b5724cdfc1`; exact-head CI [40208623562](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40208623562) passed.
- These are parser/input-integrity verifications. Lao IPA accuracy remains unmeasured: independent adjudicated gold count is still 0, and the external G2P diagnostic is not gold.


## Lao tone-rule matrix integrity gate — 2026-10-25

- Added a unittest contract for the existing `tone_rules.csv`: unique rule IDs, legal condition/value domains, source-claim linkage, and no ambiguous winner at the resolver's declared specificity levels across consonant class × live/dead × short/long × tone-mark combinations.
- This validates the implementation/data contract only. The rules remain scoped to a Vientiane-oriented five-tone reference matrix; no acoustic F0 contour validation or universal Lao dialect claim is made.
- Exact-head CI must pass the full Python/browser/build/reproducibility/page workflow before merge.


- Post-merge evidence: PR #46 is merged as `4a01b1bf37ee0fae6579430a3ada33680e4debb9`; exact-head workflow [40209554020](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40209554020) passed. LAO-TONE-001 remains IN_PROGRESS because matrix integrity does not adjudicate acoustic contours or all dialect-specific examples.


## IA spelling and length correction — 2026-10-25

- A direct source review of Richard Ishida's *Lao Orthography Notes* (updated 28-Apr-2026, “Diphthongs, triphthongs, and rhymes”) identified an error in the existing vowel registry and engineering fixture: `ເ◌ັຽ` was labelled short IA, `ເ◌ັຍ` was also labelled short, and unsupported preposed `ເ◌ຽ` was labelled long IA.
- Corrected the Python parser, browser engine, canonical vowel registry, structural-vowel table, evidence claims, generated browser data, and shared positive/negative fixtures. Long IA is now `ເ◌ັຽ` or `ເ◌ຍ`; short IA is `ເ◌ັຍ`; standalone/medial `◌ຽ` remains separately supported where structurally applicable. The unestablished preposed `ເ◌ຽ` sequence must withhold IPA and Ukrainian output.
- Source: https://r12a.github.io/scripts/laoo/lo.html, updated 28-Apr-2026, lines 593–607. This is a correction to an orthographic pattern claim and test fixture, not an independent lexical gold label.
- Implementation branch `fix/lao-ia-vowel-length-evidence-20261025` was merged through PR #48 as `585891afdf85e00ff4ec5a7c95e13b6eb4570634` (squash). Exact-head verification on branch commit `8f19d6fd26cb707f1dd292f1ac3ec57cca47bef9` passed in workflow [40214418105](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40214418105): all Python tests, optional harness syntax/CLI checks, browser engine tests, build, generated-data drift, and built-page/relative-asset checks. The optional external G2P diagnostic also passed on the same code state in [40214418066](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40214418066); it remains a comparison, not an accuracy score.
- Regression evidence retained: the initial run [40214219757](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40214219757) exposed that an empty-prefix template could match a postposed `◌ຽ` despite a preposed `ເ`. Both vowel matching and suffix consumption now require the exact preposed context, and the negative test checks that `ເ◌ຽ` remains unconsumed with no IPA/Ukrainian output. The later exact-head suite passed.
- Local `git clone`/test execution was unavailable because the environment could not resolve `github.com`; remote CI supplied the test evidence. Accuracy remains unmeasured (independent gold count 0).


- Follow-up adversarial review caught a browser-only segmentation hazard: after correctly rejecting `ເ◌ຽ` as a vowel pattern, dynamic word segmentation could still salvage `ເ+onset` as /eː/ and leave `ຽ` as an unresolved suffix. The whole-token guard and browser regression were merged in PR #43 as `0336419ad612072b61e12b9e92b6bb6b67ff9284`; exact-head workflow [40208462464](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40208462464) passed Python, browser, harness syntax/CLI, build, generated-data reproducibility and built-page/asset checks. This item is verified; do not retain the old instruction that CI is pending.


## Multiple Lao tone-mark fail-closed guard — 2026-10-25

- Found a parser integrity gap in both Python and browser engines: a syllable containing more than one tone mark selected the first mark, stripped all marks before structural parsing, and could still emit IPA/Ukrainian output as if the orthography were valid.
- Python now emits `MULTIPLE_TONE_MARKS`; the core withholds IPA, tone, candidates, and practical Ukrainian output and records `PHON-IPA-WITHHELD-MULTIPLE-TONE-MARKS`. Browser analysis rejects a token with multiple tone marks and prevents dynamic segmentation from rescuing adjacent duplicate marks.
- Added Python and browser regression tests for `ກ່້າ`. This is an input-integrity correction, not a phonological expansion or accuracy claim.
- Acceptance: exact-head `verify.yml` must pass Python unittest discovery, browser tests, generated-data drift, build, and built-page/asset checks. Independent adjudicated Lao IPA gold remains 0; accuracy remains unmeasured.


## Post-merge current-head checkpoint — 2026-10-25

- Multiple-tone-mark fail-closed fix merged as `316dab931ca4cc842b4e3dcb5869546761b50b9d` via [PR #51](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/51).
- Exact PR-head verification [40216312547](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40216312547) passed; post-merge `main` verification [40216376688](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40216376688) and Pages deployment [40216376751](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40216376751) also passed.
- Python/browser regressions require multiple tone marks to withhold IPA, tone, candidates and practical Ukrainian output. This remains input-integrity evidence, not linguistic accuracy evidence. Independent adjudicated gold remains 0; tone/cluster/lexical source adjudication remains open.


## Structural uncertainty and tone-contour contract — 2026-10-25

- PR [#53](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/53) merged as `58385a0f36953c970d936123cb67192600510067`.
- Python and browser now withhold IPA, Ukrainian output, tone and contour for short-vowel structures that require a coda when no coda was parsed. A partially parsed prefix no longer carries a tone inferred from an incomplete syllable.
- Python's `SyllableAnalysis.tone_contour` now exposes the matched rule's registered contour, consistent with browser `toneContour`. Shared fixture `tests/fixtures/tone_contour_cases.json` checks two existing Vientiane-scoped tone rules and two unresolved short-vowel cases across runtimes.
- Exact-head CI [40221383984](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40221383984) passed. Post-merge main verification [40221658071](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40221658071) and Pages deployment [40221658065](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40221658065) passed.
- The shared fixture is an implementation contract, not independent phonetic gold. Exact acoustic contours, the dialect scope of tone rules, full initial clusters, and an independently adjudicated lexical corpus remain open.


## Romanization → IPA → Ukrainian result order — 2026-10-29

- Open draft PR [#55](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/55) adds a distinct Lao-Latin romanization panel ahead of IPA and Ukrainian practical transcription, with independent copy actions.
- Profile: ordered literal-rule subset from Unicode CLDR `common/transforms/Lao-Latin.xml`, transform variant UNGEGN, marked provisional by upstream. This is not a full ICU transform interpreter. Upstream explicitly notes final-consonant handling remains incomplete. Unmapped Lao code points are preserved and make the output partial.
- Exact-head CI for `63802e6b81300998f7b04ec57e540a248fb36c37`: [verification run 40780941839](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40780941839) **passed**. Python tests, browser engine tests, generated data reproducibility and built-page asset checks passed; the new romanization unit tests also passed.
- Status: UI/engine integration **PARTIAL / CI-PASS**. Romanization must not be confused with IPA or with the existing Ukrainian candidate pipeline; tone metadata in IPA remains independent.
- Next acceptance gates: implement/verify the full ICU context rules or explicitly constrain coverage further; add sourced word/sentence fixtures including coda-sensitive cases; manual browser/mobile and copy-action QA; independent review of the provisional UNGEGN scope. Keep PR draft until reviewed.


## Publication checkpoint — 2026-10-29

This checkpoint supersedes earlier notes in this handoff saying the romanization PR was open/draft.

- PR #55 was merged to main as fdd8e788344cbfd57cddf71034117b4ac0dae9b5.
- Exact post-merge verification [40782820596](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40782820596) passed.
- Exact post-merge GitHub Pages deployment [40782820604](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40782820604) passed and reported URL: https://clippyfirst.github.io/Lao-Ukrainian-Phonetic-System/
- Published output order: Lao romanization → IPA → Ukrainian practical transcription. The current CLDR/UNGEGN implementation remains a constrained provisional subset; see the limitations above.
- Remaining acceptance gates include coda-sensitive sourced fixtures, full transform-context handling or stricter coverage bounds, and manual browser/mobile/copy QA. Publication does not mean linguistic completeness.


## Shared Ukrainian target adaptation checkpoint — 2026-10-30

- Draft PR #56, branch `fix/shared-ukrainian-phonetics-2026-10-30`, applies the shared target policy after Lao phonology and IPA.
- Aspirated /kʰ tʰ pʰ/ now produce к' т' п' in practical output. IPA continues to carry aspiration. /ʔ/ remains distinct and does not trigger the apostrophe.
- /h/ → г, /ɡ/ → ґ, genuine /x/ → х. Affricates include /tɕ/ and /t͡ɕ/ → ч, /dʑ/ and /d͡ʑ/ → дж, /t͡s/ → ц, /d͡z/ → дз, /t͡ʃ/ → ч, /d͡ʒ/ → дж; /ʃ ʒ/ → ш ж. Supported palatalization is represented explicitly.
- Updated Python and browser regressions and compound examples for the resulting aspiration marker. Regenerated `web/data.js` from canonical CSV; independently reconstructed generator output matched the committed artifact byte-for-byte.
- Exact-head verification [41075912762](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41075912762) passed the complete `verify` workflow. Verified branch head: `ed252abd34cb6b20c908234e75873e0b02a89762`.
- PR #56 remains draft and unmerged. Previously merged PR #55 and the published romanization layer were preserved.

The mapping changes are project-level Ukrainian practical decisions, not an official standard and not independent Lao pronunciation gold. The research gold corpus remains empty and measured accuracy remains unreported. Existing segmentation, cluster, tone-scope and lexical adjudication blockers are unchanged.


## Continuation — GitHub Pages release path · 2026-10-30

- Deployment target confirmed by the owner: **GitHub Pages only**; Vercel is not part of this release path.
- Existing `.github/workflows/pages.yml` deploys only from `main` and uses the official Pages artifact/deploy actions. Its asset assertion expected the unversioned CSS URL and would reject the new cache-busted stylesheet URL. Updated the assertion to accept the versioned relative asset path and extended the artifact gate to check the editorial specimen, copy-feedback live region, skip links and methodology navigation.
- Pages workflow correction commit: `a175669427ba6ffbe6c11a05fca3817d3531027a`. Verify workflow run [41111527416](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41111527416) was queued when this handoff entry was written; do not treat it as passed until completed.
- The Pages workflow cannot publish from the feature branch by its normal push trigger. Publication requires the reviewed PR to land on `main`; then the existing push trigger builds and deploys the static `dist/` artifact. No Vercel configuration or project was created or changed.
- `LAO-UI-001` remains `IN_PROGRESS` until actual browser QA is completed at 1440px, 768px and 390px, including keyboard operation. CI assertions are not a visual review.
- `LAO-DEPLOY-001` remains `TODO` until the post-merge Pages workflow succeeds and both public URLs serve the new build.
- Latest branch head at this checkpoint: `a175669427ba6ffbe6c11a05fca3817d3531027a`; branch `design/lao-layout-20261030`; PR #61 remains open. No release tag created.


## Post-merge checkpoint — 2026-10-30

- PR #61 was squash-merged into `main`: https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/61
- Main merge commit: `10faed6e0012935f4001932aada1f9ed68a65eb2` (source branch `design/lao-layout-20261030`, head `8aff9cca546c2cd86e24d7dc1c5231eefab4eb44`).
- The GitHub Pages workflow is configured to run on pushes to `main` when the site or Pages workflow files change. This merge includes `index.html`, `system.html`, `web/**` and `.github/workflows/pages.yml`, so it matches the deploy trigger. The workflow uses only GitHub Pages; no Vercel target is configured.
- The latest exact-head `verify` run [41111609245](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41111609245) remained queued when checked. Do not report it as passed. An earlier UI implementation commit passed verify run [41110855525](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41110855525).
- Deployment and visual acceptance are not yet marked complete: the available GitHub connector did not expose the push-triggered Pages run status, the public Pages URL could not be fetched in this session, and browser screenshot review was unavailable because the browser service had exhausted its credits. `LAO-DEPLOY-001` remains `TODO`; `LAO-UI-001` remains `IN_PROGRESS` until visual QA at 1440px, 768px and 390px plus keyboard interaction review.
- No linguistic engine, source registry, phonetic mappings, or research accuracy claims were changed by this design/deployment batch. Research corpus and phonological adjudication blockers remain as previously documented.


## Pages deployment gate update — 2026-10-30

- Post-merge Pages workflow: [41111967539](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41111967539), commit `10faed6e0012935f4001932aada1f9ed68a65eb2`.
- At the time of the initial check, the deploy job was `waiting` at the `github-pages` environment. This wait later resolved automatically; no owner approval or environment-setting change was required. See the final deployment confirmation below.


## Final Pages deployment confirmation — 2026-10-30

- GitHub Pages run [41111967539](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41111967539) for main commit `10faed6e0012935f4001932aada1f9ed68a65eb2` completed with conclusion `success`.
- Both jobs succeeded: `build` (including browser regression tests, `npm run build`, artifact checks and Pages artifact upload) and `deploy` (`actions/deploy-pages@v4`). The environment wait resolved without an approval action from this session.
- `LAO-DEPLOY-001` is now **DONE_VERIFIED** at the workflow/deployment level. Public URL HTTP smoke-check could not be performed: web fetch rejected the Pages host and container DNS/network access was unavailable. URLs remain the configured Pages target: https://clippyfirst.github.io/Lao-Ukrainian-Phonetic-System/ and https://clippyfirst.github.io/Lao-Ukrainian-Phonetic-System/system.html.
- `LAO-UI-001` remains **IN_PROGRESS** pending actual visual browser QA at 1440px, 768px and 390px and keyboard-only review. Do not equate passing CI assertions with visual QA.
- The deployment completion was documented in the subsequent main-branch handoff commit; no product code change was needed after the successful Pages deployment.


## Continuation — selectable romanization-to-Ukrainian mode · 2026-10-30

- Baseline: `main` at `d64e201f6d417c71e3437daccfa465ddb77e224f`; dedicated branch: `feat/romanization-ukrainian-mode-20261030`. No open PRs existed at branch start. Previously merged PR #55 (provisional CLDR romanization panel) and PR #64 (vertical full-width service layout) were preserved.
- User selected a **two-mode selector** in the Ukrainian result card. Phonetic mode remains the default. The optional romanization mode consumes the output of the existing CLDR subset and never changes the IPA-first phonetic path.
- Added `web/romanization-ukrainian.js`, selector markup and state in `index.html`/`web/app.js`, responsive selector styles, regression tests, and methodology/requirements/decision/limitations/README/final-audit updates.
- The new adapter maps CLDR romanized spelling through a project-defined orthographic table, retains punctuation/whitespace/digits, preserves unsupported characters and reports `PARTIAL`. It does not restore tone, vowel length or pronunciation absent from the romanization.
- TDD evidence: test-only commit `ee43e4fd0a0a7a5e484edb39f0a47f42cb8e9194` failed in verify run [41118552977](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41118552977) at browser tests with `ERR_MODULE_NOT_FOUND` for the not-yet-implemented adapter; all 46 existing engine tests passed. This was the expected RED result.
- Current branch head at handoff update: `efd3de18296b2b09440f8ca0e554ae567ddf6e21`; exact-head verify run [41119097168](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41119097168) was in progress when this entry was written. Do not mark LAO-ROM-UA-001 complete until this and a final post-documentation verification pass.
- Local clone and local command execution were unavailable because container DNS could not resolve `github.com`; GitHub Actions is the execution environment for the repository-defined suite. Manual browser screenshots/keyboard QA were not available here; LAO-UI-001 remains IN_PROGRESS.
- No PR was opened or merged yet. The independent Lao IPA gold corpus remains empty; no empirical phonetic accuracy claim is added.


## Final engineering verification — selectable romanization mode · 2026-10-30

- `LAO-ROM-UA-001`: **DONE_VERIFIED** for the implementation contract at commit `cfa95799c47eb683e590b061e4f40b6b4f154737`. Exact-head GitHub Actions verify run [41119525542](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41119525542) succeeded: 92 Python tests, 46 browser engine tests, 7 romanization tests, 5 web-layout tests, optional external-G2P harness syntax/CLI, browser data generation, no generated-data drift, and built-page/relative-asset checks.
- TDD history: test-only commit `ee43e4fd0a0a7a5e484edb39f0a47f42cb8e9194` failed as expected because the new adapter module was absent. The first implementation run then caught a provenance-label assertion mismatch; the label was corrected and the exact-head suite passed. Both failed runs were reviewed, not hidden.
- Branch remains based directly on `main` at `d64e201f6d417c71e3437daccfa465ddb77e224f`; all changes are confined to the dedicated feature branch. No existing PR or unrelated branch was reused or modified.
- The existing CLDR romanizer remains provisional and incomplete. The new Ukrainian adapter is a deterministic orthographic project policy, not phonetic transcription. It cannot restore tone, length, or pronunciation distinctions absent from the romanized string.
- Local clone/test execution remains blocked by container DNS failure for `github.com`; the complete repository verification ran on GitHub Actions. Manual screenshot/keyboard review at 1440px, 768px and 390px remains unavailable; `LAO-UI-001` stays IN_PROGRESS. GitHub Pages deploy remains a post-merge action; this branch was not published or merged.
- Independent adjudicated Lao IPA gold remains 0. The feature does not improve or validate phonological accuracy.


## User correction and syllable-engine implementation — 2026-10-30

- Historical interpretation of the user's clarification at that checkpoint: the romanization method must translate **syllables**, not substitute Latin letters one by one. The then-applied blanket h → г rule inside kh/th/ph was subsequently corrected by source review and is superseded by D-008; standalone Lao /h/ still maps to г.
- Replaced the character-level adapter with `web/romanization-syllable-engine.js`. The parser models onset, vowel nucleus and coda, recognizes the CLDR preposed-vowel order, applies documented position-sensitive final forms, and assembles Ukrainian syllables. The later source-grapheme crosswalk correction is recorded below and is the current policy.
- The primary Ukrainian card still has the two-method selector. The romanization method now has its own visible syllable trace (romanized syllable, onset, nucleus, coda, Ukrainian result and status); the IPA/phonetic trace remains separately labelled.
- Ambiguous concatenated romanization is not guessed. For example, the engine withholds an ambiguous continuous parse and marks it partial; unsupported fragments remain visible in brackets.
- Added evidence sources/claims for the provisional CLDR Lao-Latin transform and the EKI/UNGEGN BGN/PCGN 1966 report. The report explicitly says Lao has no UN-approved romanization system and no national romanization system; CLDR marks its transform provisional and leaves special final-consonant handling as TODO.
- Exact-head workflow [41123400527](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41123400527), commit `9a4841c53705fa245f23f5c060e53cb146d8a185`: Python 92, browser engine 46, romanization 9, syllable-engine 9, web-layout 5; external-G2P harness syntax/CLI, browser build, generated-data reproducibility and built-page/relative-asset checks all passed.
- The subsequent commits update validation/audit/handoff documentation only. Final documentation-head verification is still required. PR #65 remains open and unmerged; no deployment was performed. Manual visual/keyboard QA remains open; independent Lao IPA gold count remains 0.


## Final verification checkpoint — 2026-10-30

- Exact implementation/evidence commit `02dd2bfe24e09a10fdb08265a4074aedbce97c8c` passed workflow [41123807011](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41123807011). Repository audit passed with 43 consonant rows, 34 vowel rows, 17 tone rules, 69 Ukrainian mappings, 19 evidence sources and 33 claims; all claim-to-source references resolved. Python 92, browser engine 46, romanization 9, syllable engine 9, web layout 5, external-G2P harness syntax/CLI, build, generated-data reproducibility and built-page/asset checks passed.
- A pre-existing CSV defect was discovered by the new audit: one evidence claim contained unquoted commas, shifting CSV columns. The claim text was quoted correctly; the audit then passed. The verify workflow now runs `python scripts/audit.py` before the test suite.
- Branch remains based on `main` at `d64e201f6d417c71e3437daccfa465ddb77e224f`, with no commits behind main. PR #65 is open, mergeable, and intentionally unmerged. No deployment was performed.
- The current method is syllable-based, not letter-by-letter. BGN aspirate digraphs kh/th/ph map to к'/т'/п'; independent Lao /h/ maps to г. The primary IPA-first method is unchanged. This supersedes the blanket h rule recorded in earlier historical checkpoints.
- Remaining non-code acceptance: manual visual and keyboard QA at 1440px, 768px and 390px; expert review of project-specific romanization-to-Ukrainian syllable correspondences; full CLDR/ICU transform coverage and lexical segmentation. No independent IPA gold corpus exists (count 0), so empirical pronunciation accuracy remains unmeasured.


## Final syllable-parser verification checkpoint — 2026-10-30

- Exact implementation commit `753b82c89076b2e23fbbcd937df45bf4289b7dfc` passed [workflow 41124439725](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41124439725): repository data/evidence audit (43 consonants, 34 vowels, 17 tone rules, 69 UA mappings, 19 evidence sources, 33 claims with all references resolved); Python 92; browser engine 46; romanization transform/compatibility 10; syllable engine 12; web layout 5; external-G2P harness syntax/CLI; build; generated-data reproducibility; built-page/relative-asset checks.
- The syllable parser now resolves CLDR preposed-marker/postposed-nucleus sequences, uses longest-match onset/coda tokens, and detects competing segmentations. The joined example `ékhôaniav` is deliberately partial because the boundary between `ékhôa` and `niav` is ambiguous; explicit `ékhôa-niav` parses deterministically.
- The next commits update documentation and PR metadata only; exact final documentation-head verification remains pending. PR #65 remains open, mergeable, unmerged and undeployed.


## Source-grapheme / romanization / Ukrainian crosswalk correction — 2026-10-30

- User requested an explicit check between Lao letters, their Latin romanization and Ukrainian output so aspirated forms are not confused with an actual /h/ sound.
- Primary evidence reviewed: Richard Ishida, *Lao Orthography Notes*, consonant inventory and “Consonant sounds to characters” (the reference separates aspirated /kʰ tʰ pʰ/ from /h/ and maps them to ຂ/ຄ, ຖ/ທ, ຜ/ພ versus ຫ/ຮ); the same reference describes the limited onset-cluster model. The EKI/UNGEGN BGN/PCGN 1966 report provides the Latin spellings kh, th, ph, h, x.
- Corrected policy: kh → к', th → т', ph → п' for the source consonant letters ຂ/ຄ, ຖ/ທ, ຜ/ພ; standalone h → г only when sourced from ຫ/ຮ. BGN x from ຊ is /s/ and maps to с, not кс. Final h is not a valid Lao coda and is withheld. The adapter checks romanization against the original Lao onset and marks mismatches or non-1:1 alignment PARTIAL.
- The current crosswalk validates source onset and supported coda graphemes against CLDR romanized forms; the visible trace displays both source positions and their verification status. Existing phonetic IPA-first engine and its output path remain unchanged. This is a source-aware orthographic crosswalk, not a claim that the romanization preserves tone or all phonetic information.
- TDD red evidence: test-only commit a9c71713d5caa31a2f19273df172eb782a8ff622 triggered [workflow 41131862367](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41131862367); audit and Python tests passed, and the browser tests failed as intended on the new crosswalk expectations.
- Intermediate implementation run [41133435559](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41133435559) passed audit, Python tests and external-G2P harness but failed one pre-existing provenance-label assertion because the updated source string omitted the word “romanization”. Corrected in commit fc5d5eba43b890aa3bc4126f4c3af11ae59c6e69; this is a test-contract wording repair, not a change to the phonological mapping. Latest exact-head CI is still required.


## Source-vowel and high-class nasal romanization crosswalk — 2026-10-31

- The official UK government copy of the BGN/PCGN 1966 Agreement was checked alongside the EKI/UNGEGN report. Note 5 explicitly states that silent ຫ is generally omitted before sonorants and that ໜ/ໝ are abbreviated forms of ຫນ/ຫມ. These ligatures are therefore romanized n/m, not h+n/h+m; the adapter now maps them to Ukrainian н/м when source syllable structure confirms the correspondence.
- The source-aware crosswalk now checks three positions: onset grapheme ↔ romanized onset, source vowel-structure ID ↔ romanized nucleus, and supported coda grapheme ↔ romanized coda. The app extracts vowel identity from the IPA-first parser's `VOWEL:<ID>` rule trace; it does not use the IPA output to generate this romanization result.
- Source vowel evidence resolves homographic romanizations. `ກາມ` parses as A + final ມ, while `ກຳ` parses as the AM nucleus; both may yield `kam`, but source-aware output can select the correct syllable structure. Without source evidence, the engine withholds ambiguous `kam`.
- Source syllable evidence similarly resolves `niav` as ໜ + IA_LONG + final ວ. Without the source, `niav` has competing parses and remains PARTIAL. The full `ເຂົ້າໜຽວ` source can now be segmented from source evidence rather than relying on an invented hyphen.
- New evidence records: `CLM-LAO-ROM-HIGH-NASAL-LIGATURES`, `CLM-LAO-ROM-VOWEL-CROSSWALK`, and `CLM-LAO-ROM-KAM-DISAMBIGUATION`; new source `SRC-PCGN-LAO-1966`.
- Code/test changes are on the existing PR #65 branch. Exact-head CI now passes at 7fef1a326c8d1f7c5dfc0cb3c2cb41a4ee9b4140 (workflow 41137160734); LAO-ROM-UA-001 is DONE_VERIFIED for the implemented subset. Manual visual/keyboard QA, expert linguistic review of uncovered cases and gold-corpus evaluation remain outstanding.


## Exact-head verification update — 2026-10-31

- Task ledger: `LAO-ROM-UA-001` = **DONE_VERIFIED** for the implemented source-aware romanization subset. Verified implementation head `d0b9a585a3edf2ad0c89ba9f9b10fcbc35aa62e6` passed workflow [41137893545](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41137893545).
- Audit: 43 consonant rows, 34 vowel rows, 17 tone rules, 69 Ukrainian mappings, 20 evidence sources, 44 evidence claims; all evidence references resolved.
- Tests: Python 92; browser engine 46; romanization integration 19; syllable crosswalk 27; web layout 5. External-G2P harness syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks all passed.
- New official source: UK government copy of the BGN/PCGN 1966 agreement. Note 5 supports silent ຫ omission before sonorants and abbreviated ໜ/ໝ forms; the implementation covers the supported written digraphs and ligatures, while the BGN /r/ case remains unsupported by the structural parser. The engine now checks written onset form, source vowel ID and supported coda; it applies the silent-hoa rule to the implemented expanded forms, and does not generate this route from IPA. BGN's /r/ case remains unsupported by the source parser.
- Remaining separate work: manual screenshots at 1440/768/390px, keyboard-only review, live Pages verification, expert review of uncovered romanization/vowel patterns, full CLDR/ICU coverage and independent gold corpus. No merge or deployment was performed.

## Ukrainian target sequence extension — 2026-10-31

- User requirement reaffirmed that Ukrainian consonant distinctions must be preserved, not approximated by a generic Cyrillic substitution.
- Research check: the 2025 Encyclopedia of Modern Ukraine entry “Щ” describes the letter as the combination of [ш] and [ч]; the Journal of the International Phonetic Association's Ukrainian description identifies it as [ʃ] plus an affricate [t͡ʃ]. These sources are now registered as SRC-ESU-SHCH and SRC-JIPA-UKRAINIAN, linked through CLM-UA-SHCH-SEQUENCE.
- Added exact sequence mapping /ʃt͡ʃ/ → щ to the canonical IPA correspondence CSV. The adapter's existing longest-match algorithm chooses this longer sequence before /ʃ/ and /t͡ʃ/; isolated /ʃ/ remains ш and isolated /t͡ʃ/ remains ч. This is an orthographic target mapping, not a claim that the sequence is one affricate or a Lao phoneme.
- Test-first evidence: test-only commit 1411af39ef9c5fdaa805ef1ff5689d75c5bc0ca9 failed as expected (ʃt͡ʃa produced шча instead of щ) in workflow [41140800731](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41140800731). The expanded Python/browser target test commit d796200c77c1fb24a7022fad3bd21a29e431d720 likewise exposed the missing target sequence before implementation in [41140863656](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41140863656).
- Implementation and generated browser data updated in 3d0d71cc505695eb9e7e0dc5b60f40227cc79565. Exact-head workflow [41140937597](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41140937597) passed: audit 43 consonants, 34 vowels, 17 tone rules, 70 Ukrainian mappings, 22 sources, 45 claims; Python 94; browser engine 47; romanization integration 19; syllable crosswalk 27; web layout 5; external-G2P harness syntax/CLI; production build; generated-data reproducibility; built-page and relative-asset checks.
- Updated PR #65 description to remove the obsolete blanket h → г statement and document the actual source-aware aspiration and Ukrainian target rules. PR remains open and unmerged; no deployment was triggered from the feature branch.
- Remaining blockers: independent expert review of the full target mapping inventory; representative adjudicated Lao IPA gold corpus (currently 0); visual/keyboard QA at 1440px, 768px and 390px; full CLDR/ICU romanization coverage; cluster and lexical segmentation coverage. These are not satisfied by deterministic CI.

- Final target inventory review also made the /h/ versus /ɦ/ relationship explicit in the README and Ukrainian target specification: both map to г in this target policy, but they remain distinct source values; /ɡ/ maps to ґ and /x/ to х. This documentation-only clarification is verified by the subsequent exact-head workflow and is included in the final branch tip.


## Repository reconciliation and exact-head verification — 2026-10-31 (continued)

- Re-read the current default branch and PR inventory. `main` is `d64e201f6d417c71e3437daccfa465ddb77e224f`; the active feature branch `feat/romanization-ukrainian-mode-20261030` is based on that commit and compares 263 commits ahead, 0 behind. This is inherited branch history, not 263 commits created in this continuation.
- PRs #61, #62, #63 and #64 are closed as merged. Their merge commits are respectively `10faed6e0012935f4001932aada1f9ed68a65eb2`, `2e6fa9b18f0ab7b9057e1ccb84577c6c29ed1941`, `1f7ae5291db88c1150137d75225bcdf88dea5b0e` and `d64e201f6d417c71e3437daccfa465ddb77e224f`. Their responsive/interface work is therefore already in the current base; no cherry-pick or duplicate implementation was made.
- PR #56 is also closed as merged at `f59caa5b3a965fb18f14bdf23b4e0c72ec156152`. The formerly open branch `fix/shared-ukrainian-phonetics-2026-10-30` was compared with current `main`: its canonical correspondence CSV and Ukrainian target specification are byte-identical to main, and its target fixtures/tests contain no additional unmerged change. The branch is historical/diverged; no port is needed. The old PR #56 draft/unmerged wording in earlier chronological notes is superseded by this reconciliation.
- PR #65 remains open, base `main`, head `bd2b0b05e00c884d20818dce914603b4a0b09cc3`. No merge, branch deletion or force-push was performed.
- Exact-head workflow [41141316134](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41141316134) completed successfully for `bd2b0b05e00c884d20818dce914603b4a0b09cc3`. Verified steps: repository data/evidence audit; Python 94; browser engine 47; romanization integration 19; syllable crosswalk 27; web layout 5; external-G2P harness syntax/CLI; canonical browser-data build/regeneration; generated-data reproducibility; built-page and relative-asset checks. This is engineering verification, not linguistic adjudication.
- Deployment evidence: Pages workflow [41117044318](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41117044318) successfully built and deployed the exact current `main` commit `d64e201f6d417c71e3437daccfa465ddb77e224f`; both `build` and `deploy` jobs completed successfully. This supersedes the earlier 10faed6 deployment checkpoint. Direct visual/HTTP smoke verification remains separate from workflow deployment success.
- Remaining gates are unchanged: independent expert review of Ukrainian target mappings; licensed, versioned and expert-adjudicated Lao IPA gold corpus; source-by-source vowel/tone/coda/cluster adjudication; full CLDR/ICU romanization coverage (including unsupported `ຫຣ`); and visual/keyboard QA at 1440px, 768px and 390px. Do not infer linguistic readiness from green CI.


## Post-merge completion checkpoint — 2026-10-31

- PR #65 (`feat: add syllable-based romanization-to-Ukrainian mode`) was squash-merged to `main` as `b2e1187629829b4242aa2430a9901d264910eea1`. It preserves the IPA-first default and adds the bounded, source-aware CLDR/BGN romanization syllable adapter, source registries, Ukrainian `/ʃt͡ʃ/ → щ` longest-match mapping, UI selector, and regression coverage.
- Main verification for the merge commit passed in [run 41142746494](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41142746494): Python 94; browser engine 47; romanization integration 19; syllable crosswalk 27; web layout 5; data/evidence audit; external-G2P harness syntax/CLI; build; generated-data reproducibility; built-page/relative-asset checks.
- The first Pages deployment attempt [41142746466](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41142746466) failed only because `pages.yml` still required the exact unversioned app script URL. PR #66 fixed the stale assertion; it was squash-merged as `a001046462de564dd2cb89e9237caa221624163c`.
- Exact-main verification [41142874231](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41142874231) and Pages deployment [41142874311](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41142874311) both passed on `a001046462de564dd2cb89e9237caa221624163c`. Pages build, artifact assertions, upload and deploy all succeeded.
- `LAO-DEPLOY-001` is now `DONE_VERIFIED` at the workflow/deployment level. `LAO-UI-001` remains `IN_PROGRESS` because real-browser visual screenshots and keyboard-only QA were not available. `LAO-CORPUS-001` is `BLOCKED` pending a licensed independently adjudicated gold corpus and qualified Lao linguistic review. `LAO-UKR-001` remains `PARTIAL` pending independent expert review of the complete target inventory. Release remains deferred.
- PR #56 and PRs #61–#64 were already merged in the base and were reused, not reimplemented. PR #65 and the focused Pages workflow fix PR #66 are now merged. No user branches were deleted or force-pushed.


## Public research-status reconciliation — 2026-10-31

- Reconciled the service homepage and methodology status with the actual merged main state: the IPA-first method remains default; the optional source-aware romanization syllable adapter is available for a bounded subset; the exact Ukrainian target sequence `/ʃt͡ʃ/ → щ` is explicit; and the silent-`ຫ`/`ໜ`/`ໝ` support is described as a subset rather than full phonological/tone coverage.
- Corrected stale wording that implied all `ໜ/ໝ` forms were unimplemented. The remaining gap is complete phonological and tonal adjudication, not the already implemented romanization crosswalk subset.
- Added a public-status regression test. Test-first failure on the old copy: [41183451808](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183451808), browser suite 5 passed / 1 failed at the intended stale-status assertion. Corrected exact-head verification: [41183689662](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183689662), audit passed (43 consonants, 34 vowels, 17 tone rules, 70 UA mappings, 22 sources, 45 claims); Python 94; browser engine 47; romanization integration 19; syllable crosswalk 27; web layout 6; optional external-G2P harness syntax/CLI; production build; generated-data reproducibility; built-page and relative-asset checks all passed.
- Task `LAO-STATUS-PUBLIC-001`: `DONE_VERIFIED` for the public status copy and automated regression only. `LAO-DOCS-001` remains `PARTIAL`; `LAO-UI-001` remains `IN_PROGRESS`; independent gold corpus remains 0 and accuracy null. Real-browser visual/keyboard QA, expert linguistic review and corpus work remain blocked by external/manual evidence, not by this documentation change.
- PR #68 merged as `6293f52848b675ff53c2a1d191cdcbca3cb034b4`. Exact-main verification [41183960495](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183960495) and Pages deployment [41183960573](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183960573) both passed on that commit. No application phonology, romanization behavior, canonical data, or generated artifacts were changed.

## Post-merge exact-main verification and deployment — 2026-10-31

- PR #68 merged as `6293f52848b675ff53c2a1d191cdcbca3cb034b4`; the homepage, methodology, master handoff, validation and final audit now describe the deployed state.
- Exact-main verification [41183960495](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183960495) passed: audit (43 consonant rows, 34 vowel rows, 17 tone rules, 70 Ukrainian mappings, 22 sources, 45 claims); Python 94; browser engine 47; romanization integration 19; syllable crosswalk 27; web layout/status 6; external-G2P harness syntax/CLI; build; generated-data reproducibility; built-page and relative-asset checks.
- GitHub Pages workflow [41183960573](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183960573) passed both build and deploy jobs. This is deployment evidence, not visual or linguistic validation.
- `LAO-DEPLOY-001` remains `DONE_VERIFIED`; `LAO-UI-001` remains `IN_PROGRESS` pending real-browser screenshots and keyboard-only QA. Gold corpus remains 0; accuracy remains null. No external G2P comparison was rerun.

## Post-merge evidence reconciliation — PR #69 — 2026-10-31

- PR #69 merged as `8664d800c683af28b2af840027844d53471d25d3`. README now links to stable workflow histories rather than calling a fixed run the latest deployment.
- PR #69 exact-head verification [41183931581](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183931581) passed; its changes were documentation and public wording only.
- Exact-main verification [41183960495](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183960495) passed: audit (43 consonants, 34 vowels, 17 tone rules, 70 Ukrainian mappings, 22 sources, 45 claims); Python 94; browser engine 47; romanization integration 19; syllable crosswalk 27; web layout/status 6; optional external-G2P harness syntax/CLI; build; generated-data reproducibility; built-page and relative-asset checks.
- Pages deployment [41183960573](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183960573) passed both build and deploy jobs on the merged commit.
- No application behavior or linguistic evidence changed. Visual QA and keyboard-only review remain uncompleted; gold corpus remains 0 and accuracy remains null.

## Tone-mark domain correction — 2026-10-31

- Primary source: Appen Butler Hill, *Language Specific Peculiarities Document for Lao as Spoken in Laos* (LDC2017S08), p. 14. It states that Lao tone marks are used with open syllables; `໊` (`mai ti`) and `໋` (`mai catawa`) are rare in modern writing, are used with middle-class consonants, and indicate high-falling and low-rising tones respectively. SEAsite's Vientiane chart places its common `mai ek` and `mai tho` columns under live/smooth syllables.
- Root cause: every marked row in the previous `tone_rules.csv` used `syllable_type=*`. Both engines therefore returned tones for dead syllables, including short-vowel checked syllables and long-vowel stop-final syllables.
- PR #73 changes all eight marked rows to `live`, renames their IDs to expose that selector condition, adds a source-linked rare-mark claim, updates the generated browser mirror, and adds repository-audit checks. Unmarked dead-syllable rules are unchanged.
- The shared `tone_contour_cases.json` now includes 24 dead-syllable cases (3 onset classes × 4 marks × 2 dead-rime shapes); Python core and browser engine consume the same fixture. Additional Python selector tests assert the full matrix and rare-mark restrictions.
- Test-first RED: [41189555009](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41189555009) failed exactly on the new regression (16 failing subcases), confirming the old wildcard behavior. Post-fix exact-head verification is pending. Do not mark this task DONE_VERIFIED until the full workflow passes.

## Tone-mark and rhyme-class correction — 2026-10-31

- Test-first RED run [41189555009](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41189555009) reproduced 16 failures: wildcard tone-mark selectors assigned tones to dead syllables. The source basis is Appen Butler Hill, *Language Specific Peculiarities Document for Lao as Spoken in Laos* (2017), p. 14, plus the SEAsite Vientiane chart.
- A first correction then exposed a separate classification issue: the engine treated every short-labelled nucleus without a coda as dead. This misclassified open diphthongs and the AM rhyme. Ueda (1994, pp. 96–97) describes VV rhymes (long vowels or diphthongs) as permitting an absent final consonant, while short monophthongal rhymes generally require one. The classifier now reads canonical `nucleus_type` and `coda_class` separately from phonetic vowel length.
- The canonical `vowels.csv` now distinguishes monophthong/diphthong nucleus type; Python and browser classifiers preserve the original IPA and use that structural metadata for live/dead assignment. The generated browser registry includes the metadata, and the generator reproduces it.
- Shared `tone_contour_cases.json` now has 37 cases: 24 marked dead-syllable cases across three onset classes × four marks × two dead-rime types, plus open short-diphthong and nasal-final cases. Both engines consume the same fixture.
- The final exact-head workflow [41190189983](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190189983) passed: audit (43 consonants, 34 vowels, 17 tone rules, 70 UA mappings, 23 sources, 47 claims); Python 97; browser 47; romanization integration 19; syllable crosswalk 27; web layout 6; optional external-G2P harness syntax/CLI; production build; generated-data reproducibility; built-page/relative-asset checks. Total: **196 tests passed**.
- Intermediate failures were retained as evidence: [41189875486](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41189875486) exposed the open-AI classifier issue; [41190146649](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190146649) exposed an incorrect fixture expectation (the onset in `ໄກ` is middle-class `ກ`, not high-class). Both were corrected before the final passing run.
- This closes the selector/rhyme implementation contract only. It does not resolve all dialect-specific tone analyses, establish acoustic contours, create an independent gold corpus, or certify pronunciation accuracy.

### Final branch-head verification — 2026-10-31

The final branch head `803d1346b6278c3b25260063931bf72dc4e10457`, including the updated master handoff, final audit and validation records, passed exact-head workflow [41190275031](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190275031). All steps passed: repository audit; Python 97; browser 47; romanization integration 19; syllable crosswalk 27; web layout 6; optional external-G2P harness syntax/CLI; production build; generated-data reproducibility; built-page and relative-asset checks. Total: **196 tests passed**. PR #73 was subsequently merged as `0b99fd451507717664a0190dbc3bcfb7069ce15c`; post-merge main/Pages verification remains unconfirmed and is tracked in `LAO-POSTMERGE-VERIFY-001`.

## PR #73 merge and post-merge evidence — 2026-10-31

- PR #73 merged by squash as `0b99fd451507717664a0190dbc3bcfb7069ce15c`. The merged code is the same tree that passed final PR-head workflow [41190329422](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190329422), including 196 deterministic tests and build/data reproducibility.
- The merge changes `data/lao/vowels.csv`, `data/lao/tone_rules.csv`, `src/lao_ukrainian/phonology.py`, `web/engine.js`, `web/data.js`, the generator, evidence registries, shared fixtures and documentation. Therefore a new Pages deployment is expected from the main-branch push.
- Post-merge main verify and Pages deployment are **not confirmed** in this run. The GitHub connector's `fetch_commit_workflow_runs` currently returns only pull-request-triggered runs; `get_commit_combined_status` returned no classic status entries for the merge commit. The Firecrawl fetch attempt failed with an insufficient-credits response, and the public Pages URL was inaccessible through the web fetcher. These are evidence-access blockers, not evidence that the workflows failed or succeeded.
- `tests/test_core.py` had two unused imports left from a discarded duplicate fixture-test attempt; PR #74 removes them. This is a hygiene-only correction.
- Acceptance criteria for `LAO-POSTMERGE-VERIFY-001`: retrieve the exact-main verify run for `0b99fd451507717664a0190dbc3bcfb7069ce15c`; retrieve the Pages build and deploy runs triggered by PR #73; verify the public `index.html` and `system.html` reflect the generated build. Until then, keep the deployment evidence blocked/unconfirmed.

### PR #74 exact-head verification — 2026-10-31

PR #74 exact-head workflow [41190577692](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190577692) passed on `56436f6f980bf7eceb148b9d7d32f935f6325d3f`: audit (43 consonants, 34 vowels, 17 tone rules, 70 UA mappings, 23 sources, 47 claims); Python 97; browser 47; romanization 19; syllable crosswalk 27; web layout 6; optional external-G2P harness syntax/CLI; build; generated-data reproducibility; built-page/relative-asset checks. Total: **196 tests passed**. The PR only removes unused imports and updates handoff/audit records. Post-merge push and Pages runs remain unconfirmed for the evidence-access reasons above.
