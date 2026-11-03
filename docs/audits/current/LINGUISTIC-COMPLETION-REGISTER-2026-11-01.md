# Lao linguistic completion register — 2026-11-01

**Baseline:** `main` `33ac5615b13fec717ce59ee55229b9d11f04893d`.
**Latest exact-main engineering evidence:** verify [41418528760](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41418528760) and Pages/deployed smoke [41417298476](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41417298476) succeeded.
**Scope:** continue the existing master handoff; this register does not replace it.

## Evidence-based task ledger

| ID | Status | Work remaining | Acceptance |
|---|---|---|---|
| LAO-GOLD-001 | BLOCKED | No independent expert-adjudicated lexical IPA gold exists; `data/benchmark/gold.tsv` contains only its header. | At least two independent qualified annotators, adjudication, dialect/profile and IPA convention fixed, source/audio locators retained; held-out split frozen before scoring. |
| LAO-PHON-001 | PARTIAL | Validate complete tone/rhyme interactions, multi-syllable segmentation and remaining uncertain grapheme combinations against primary sources and experts. | Every supported rule has scoped primary evidence, counterexamples and shared Python/browser fixtures; unresolved cases fail closed. |
| LAO-LAB-001 | PARTIAL | Labialized onsets are structurally represented but lack justified Ukrainian correspondences. | Expert-reviewed IPA inventory and target policy; otherwise remain IPA-only/unsupported, never guessed. |
| LAO-ROM-001 | PARTIAL | CLDR/BGN-derived crosswalk is provisional and does not cover every source structure; BGN `ຫຣ` remains unsupported. | Source-located full inventory, context rules, round-trip/ambiguity tests and explicit non-reversibility; separate from phonetic mode. |
| LAO-G2P-001 | DONE_VERIFIED (diagnostic harness only) | Goruut remains unsuitable for production. | Do not promote on comparator concordance; any new claim requires independent gold and repeatable full coverage. |
| LAO-UI-001 | PARTIAL | Exact-head Playwright Chromium tests now cover visible IPA/Ukrainian output, mixed-script withholding, clear/reset and separation of phonetic vs romanization modes (4/4). Manual visual, keyboard, assistive-technology, mobile and external public-URL interaction QA remain open. | Run the browser suite against the deployed Pages URL; record human keyboard, screen-reader and mobile results. |
| LAO-REL-001 | PARTIAL | Production readiness blocked by gold, dialect adjudication and external asset rights if bundled. | All release gates in README/limitations met; no external asset shipped without rights clearance. |

## Current diagnostic evidence

The latest recorded 100-row MekongPhon/Goruut diagnostic is 81 outputs, 19 none; 47 complete, 34 partial, 19 unknown/no output; 68 stable and 13 unstable; 17 inputs had randomization metadata. These are source-coverage/repeatability diagnostics, not accuracy. The 37-row lao2ipa comparison had 0 exact implementation matches (31 tone-suffix-only, 2 offglide, 4 segmental/vowel-sequence differences). Independent gold remains 0 and accuracy must remain null. MekongPhon/Goruut are not imported as product gold or runtime assets.

## Execution order

1. Keep current fail-closed behavior; do not weaken output withholding to improve coverage.
2. Commission an independently annotated, dialect-scoped audio/lexical sample; freeze annotation instructions before collection.
3. Resolve tone/rhyme and segmental disagreements against source-located evidence; add only adjudicated records to the gold split.
4. Complete the labialized-onset Ukrainian policy only if expert evidence supports a useful Ukrainian rendering.
5. Complete the CLDR/BGN contextual matrix independently of IPA.
6. Perform deployed UI/accessibility QA and a release/asset-rights review.

## External dependencies / blockers

- Qualified Lao phonologist and independent IPA annotators; no such human review can be fabricated by CI.
- Per-resource permission for any external dictionary/model/corpus redistribution.
- No local checkout was available to this execution; exact-main GitHub Actions are the engineering evidence. Run the repository's documented local release commands in a clean checkout before release.

## Method constraints

Preserve `Lao orthography → structural analysis → Lao phonology → typed IPA → Ukrainian adaptation`. Romanization remains a separate, lower-information orthographic mode. Engineering fixtures and source-attested comparator labels are not gold.


## Independent IPA gold corpus implementation — 2026-11-01

| Task | Status | Evidence / remaining acceptance |
|---|---|---|
| IPA-GOLD-SCHEMA-001 | DONE_VERIFIED | Record, annotation, adjudication, split and license schemas plus cross-file validator |
| IPA-GOLD-DOUBLE-ANNOTATION-001 | PARTIAL | Two distinct annotators enforced; blind intake requires external controlled collection |
| IPA-GOLD-ADJUDICATION-001 | PARTIAL | Agreement/resolved/unresolved logic and feature-complete IPA comparison; no real adjudicated rows |
| IPA-GOLD-RIGHTS-001 | DONE_VERIFIED (mechanism) | Allowlisted licenses, required rights evidence and rejection of unregistered/non-redistributable licenses; source-by-source legal review still required |
| IPA-GOLD-SPLIT-001 | DONE_VERIFIED | Deterministic hash-based, frozen lexeme-group split and leakage checks |
| IPA-GOLD-EXPORT-001 | DONE_VERIFIED | Rights-filtered typed IPA export retaining source/license/evidence locators |
| IPA-TYPED-BENCHMARK-001 | DONE_VERIFIED | Different or missing IPA kind cannot count as an exact match |
| IPA-GOLD-RELEASE-GATE-001 | PARTIAL | Numeric tag/manual gate checks 100/25/25 adjudicated train/dev/test, rights and frozen splits; it does not calculate language-specific contrast coverage. Owner must require the check in release rulesets/procedure and obtain separate expert sign-off on a versioned feature-coverage matrix. |

**Current gold:** zero independent expert-adjudicated records; `gold.tsv` remains header-only; accuracy=null. The new schemas, fixtures and source-attested literature are not gold labels. No phonetic data was invented.


**Research evidence artifact:** [Lao tone–rhyme evidence matrix](LAO-TONE-RHYME-EVIDENCE-MATRIX-2026-11-01.md). It records Ueda's central Vientiane five-tone baseline and explicitly marks all unverified tone × rhyme cells; Erickson's labialized consonants remain separate from the Vientiane tone profile.


**Source correction:** Erickson's paper is bibliographically 1996 (the SEA-language PDF filename says 2001). Its adopted six-tone/coda analysis is kept separate from Ueda's five-tone central Vientiane baseline. The proposed historical origin of labialized consonants remains tentative.


**Full-text evidence update:** Ueda (1994) pp. 96, 100–108, 110–112 now provides a speaker-specific Vientiane tone × rhyme matrix: plain rhymes allow five tones; long checked rhymes allow [21]/[52]; short checked rhymes allow [34]/[33]. A restricted [22] variant overlaps with [24] in some onsets/connected contexts. Ueda's one-informant sample and its conflict with Erickson's labialized-phoneme analysis remain explicit limitations.


**2026-11-01 closeout:** PR [#98](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/98) is the comprehensive implementation and research-matrix change. Its PR CI passed 134 Python tests and all four Node/browser suites (107 total). Main remains at 6f607d7. Gold remains 0; release readiness remains blocked on expert annotation, full feature coverage and owner-enforced release rules.


## 2026-11-01 final IPA-kind consistency verification

- Added fail-closed cross-annotation consistency: both independent annotations for one record must use the same `ipa.kind`, and a `RESOLVED` adjudicated result must preserve that kind. This prevents phonemic-vs-phonetic representation differences from being misclassified as pronunciation disagreements.
- Regression evidence: both new tests failed against the pre-fix validator on the test-only commit, then passed after the validator change.
- New task `IPA-GOLD-REPRESENTATION-KIND-001`: **DONE_VERIFIED** (mechanism and exact-head CI). Blindness, annotator qualifications and independent adjudicator competence remain external operational evidence, not properties CI can prove.
- Final PR head: `0b348d191e93e15b543d95538daccf8490e8239c`; CI run [41338456936](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41338456936) SUCCESS — 137 Python tests; Node/browser suites 50 + 23 + 27 + 7; data/evidence audit, generated-data reproducibility and production build passed.
- The Lao evidence matrix remains bounded to central/Vientiane source analyses; no automatic labialized-onset Ukrainian mapping was added.
- Gold remains zero; `gold.tsv` remains header-only; empirical accuracy remains null. No IPA labels were generated.


## IPA gold split-manifest runtime/schema parity — 2026-11-01

| ID | Priority | Status | Scope / evidence | Acceptance criteria / dependencies |
|---|---|---|---|---|
| LAO-IPA-SPLIT-STRICT-001 | P1 | DONE_VERIFIED | RED test on commit `945c81b4b4ddb4f48517549353f5a3e14b26bcad` failed as expected; GREEN code commit `af97613ae959b59825d1cb6c863ad85b3b5a44d2`; exact-head CI [41340390805](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41340390805) passed | The split generator and corpus validator share the closed split-field contract; unknown prior-manifest properties are rejected rather than silently dropped. No expert gold is created by this change. |


## Product-corpus license eligibility — 2026-11-01

| ID | Priority | Status | Scope / evidence | Acceptance criteria / dependencies |
|---|---|---|---|---|
| LAO-IPA-LICENSE-ELIGIBILITY-001 | P1 | DONE_VERIFIED | RED tests on `74b2349e7054950078f8d875103a30972b9bd7be`; GREEN code/schema commit `9d3cae33d742f86b9b9e741669da892504ef3dee`; exact-head CI [41340903259](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41340903259) passed | Registry and schema fail closed unless a redistributable product-corpus license explicitly permits commercial use and defines attribution/share-alike obligations. Human source-by-source rights review remains required. |


## Release-gate threshold validation — 2026-11-01

| ID | Priority | Status | Scope / evidence | Acceptance criteria / dependencies |
|---|---|---|---|---|
| LAO-IPA-RELEASE-THRESHOLDS-001 | P1 | DONE_VERIFIED | RED test on `5e34cf8cbce93ba1cc1bdc82b2de260c88b403de`; GREEN code commit `44c9de1804f9de47a72f297aa5ed544d90d3629e`; exact-head CI [41341723054](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41341723054) passed | All split minimums reject zero and negative values; threshold errors aggregate with other release-gate findings. Default minimums remain 100/25/25. |


## Audio-source review update — 2026-11-01

A current, small Lao audio candidate is now documented in `docs/ipa-gold-collection-playbook.md`: Common Voice Scripted Speech v27.0 (locale `lo`, catalogued CC0-1.0, MP3 archive 8.93 MB; official catalog https://commonvoice.allizom.org/en/datasets; release documentation https://github.com/common-voice/cv-dataset/tree/main/datasets/scripted-speech). The archive size is not a clip count. The v27.0 manifest still needs inspection for validated clips, speaker count, transcript coverage and dialect metadata. Common Voice supplies sentence audio/transcripts, not IPA.

**Ruling:** treat this as supplementary contextual audio and candidate discovery, not as the 30-item citation-form lexical gold source. The catalog does not prove Vientiane variety. Citation-form gold should use consented recordings from confirmed target-variety speakers unless manifest review establishes a suitable sample. Keep source clip IDs and time locators; do not infer IPA from transcripts or model output.

Status remains `LAO-GOLD-001 = BLOCKED`: no annotations, annotators or adjudications have been created. Independent gold remains 0 and accuracy remains null.


## Common Voice v27.0 manifest verified — 2026-11-01

The official release manifest `cv-corpus-27.0-2026-09-11.json` has been inspected (https://github.com/common-voice/cv-dataset/blob/main/datasets/scripted-speech/cv-corpus-27.0-2026-09-11.json). Lao metadata: 223 clips, 193 validated clips, 16 contributor IDs, 0.35 validated hours (0.40 total). No named accent or variant category is supplied. Gender metadata is 88.79% male / 11.21% unspecified. Locale checksum in the manifest: `3fe87d019e65ac7e97806390698804bb60dec02444cba372706739dd8fb260b6`.

This confirms the archive is small and profile metadata is insufficient to establish Vientiane speech. Common Voice remains a supplementary contextual source, not citation-form lexical IPA gold. The 30-item pilot can use it only if 30 suitable tokens are found and a specialist accepts the profile; otherwise use controlled elicitation. No data imported; `LAO-GOLD-001` remains `BLOCKED`, gold 0, accuracy null.


## Final exact-head verification — 2026-11-01

Branch `feat/ipa-gold-corpus-20261101-review`, source-audit content commit `440975c82c5005a24952ce883cea269aa3cb3198`. Lao exact-head CI: verify [41345121935](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41345121935) SUCCESS; optional Goruut [41345121928](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41345121928) SUCCESS; optional external G2P [41345121943](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41345121943) SUCCESS. Core job passed corpus structure validation, repository data/evidence audit, Python tests, browser engine tests, browser data generation/reproducibility, and built-pages/relative-asset checks.

These checks validate the committed repository and its automated engineering contracts. They do **not** validate the linguistic correctness of future human annotations, create gold labels, or change the release blocker. Gold remains empty and accuracy remains null.


## Follow-up handoff-head CI — 2026-11-01

The subsequent documentation-only handoff/register state at commit `072713627185ec5a3d0eaa2eb29fc23aa0cca77f` was also checked on its exact head: verify [41345372448](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41345372448) SUCCESS; optional Goruut [41345372474](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41345372474) SUCCESS; optional external G2P [41345372469](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41345372469) SUCCESS. These runs validate the updated documentation and existing automated checks, not future IPA annotations. Any later branch update must be checked again on its new exact head.


## Open-rights redistributability invariant — 2026-11-01

| Task | Status | Evidence / acceptance |
|---|---|---|
| LAO-IPA-RIGHTS-OPEN-001 | DONE_VERIFIED | A test-first regression rejected a source with `rights_status=OPEN` and `redistributable=false`; the runtime validator and record JSON Schema now both require `redistributable=true` for OPEN. Test-only RED commit: `f50619febaf7b75d5d1c65973a6cb1b1ba241973`. Fix/schema code head: `4e4327e7bfdf0789c6a67b99a2b53e2bdbbc772b`; exact-head CI run [41347942661](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41347942661) passed: 142 Python tests; Node/browser suites 50 + 23 + 27 + 7; data/evidence audit, generated-data reproducibility and production build passed; optional Goruut and external G2P passed. |

This is a consistency/eligibility invariant, not a new legal determination. It does not change source licenses, rights evidence, gold labels or measured accuracy. Independent adjudicated gold remains 0; accuracy remains null.

## Exact current-head engineering checkpoint — 2026-11-01

- Current code checkpoint: `5e5f3de73fa96696e8087220c24c5d245f38797d`; exact-head core CI [41348202260](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41348202260) **SUCCESS**. 142 Python tests; Node/browser suites 50 + 23 + 27 + 7; repository data/evidence audit, generated-data reproducibility and production build passed. Optional Goruut and external Lao G2P diagnostics passed.
- The `OPEN` / `redistributable` consistency regression is present in runtime validation, JSON Schema and tests.
- Independent expert gold remains 0 and accuracy remains null. Human annotation/profile/convention gates remain open; CI is not linguistic validation.

 
## Nested IPA record contract closure — 2026-11-01

| Task | Status | Evidence / acceptance |
|---|---|---|
| IPA-GOLD-NESTED-STRICT-001 | DONE_VERIFIED (engineering contract) | Test-first RED: [run 41352928328](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41352928328); GREEN exact-code-head CI: [run 41353028676](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41353028676). Runtime validator and JSON Schema both reject undeclared fields in `orthography`, `profile`, `source` and `source.rights_evidence`. 144 Python unittest tests passed; repository CI checks passed. |

This closes only the nested-object shape contract. It does not establish the truth of source metadata, rights determinations, speaker profiles, IPA, or expert adjudication. Independent gold remains 0 and accuracy remains null.


## Validator duplicate-call cleanup — 2026-11-01

| Task | Status | Evidence / acceptance |
|---|---|---|
| IPA-GOLD-DUPLICATE-VALIDATION-001 | DONE_VERIFIED | Removed four consecutive duplicate `reject_unknown_properties` calls from nested `orthography`, `profile`, `source`, and `source.rights_evidence` validation. Code commit: `7eea774803654372e7d400cd1fde7c9079c23a64`; Git blob SHA: `a072297e320b4b91a36c59fc90328b6ff98d2a5f`. - Core PR CI: https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41354242607 (SUCCESS); core push CI: https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41354237853 (SUCCESS); optional language diagnostics: https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41354242594, https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41354242625 (SUCCESS). |

This is dead-code cleanup only: each contract check remains once; no validation rule, schema, IPA value, phonology rule, or corpus row changed. The shared validator remains identical across Lao, Khmer and Burmese. Hosted CI only; no local checkout or local test command is claimed. Independent expert-adjudicated gold remains 0 and empirical accuracy remains null.


## Methodology source refresh — 2026-11-02

| ID | Status | Evidence / acceptance |
|---|---|---|
| ENGINEERING-METHOD-REFRESH-001 | DONE_VERIFIED | Updated `AGENTS.md` and canonical handoff to pin Superpowers 7.0.1, mattpocock/skills current main, and Ponytail 5.3.3. Exact-head CI on methodology commit `748b84d7c2af7e26191e5d1e12bf875800148a13`: [PR verify 41356347659](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41356347659) and [push verify 41356342591](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41356342591) SUCCESS; 144 Python tests, Node/browser suites 50 + 23 + 27 + 7; [Goruut 41356347649](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41356347649) and [external G2P 41356347662](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41356347662) SUCCESS. No runtime dependencies or copied skill bundles were added. |



## Methodology source refresh follow-up — 2026-11-02

| ENGINEERING-METHOD-REFRESH-002 | DONE_VERIFIED | Updated `AGENTS.md` and canonical handoff to mattpocock/skills v1.3.2 (`d1478fcb140db0b93c0c8df17bcfd311844749d0`); added two-axis review, genuine-RED evidence, template/ownership, and safe worktree-cleanup guidance. Verified documentation checkpoint `d964db76a4228f2a7f84138ef69cbe1ae8cb7086`: [verify 41358587062](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41358587062) SUCCESS; optional [41358587063](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41358587063) and [41358587151](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41358587151) SUCCESS. | No third-party code, data, skill bundle, or runtime dependency copied. |

## IPA gold adjudication required-field parity — 2026-11-02

| ID | Priority | Status | Scope / evidence | Acceptance criteria / dependencies |
|---|---|---|---|---|
| IPA-GOLD-ADJUDICATION-FINAL-IPA-001 | P1 | DONE_VERIFIED | A test-first regression demonstrated that an `UNRESOLVED` adjudication with the `final_ipa` property omitted was accepted by the Python runtime even though the JSON Schema requires the property (nullable). Test-only RED commit `2750382302a6f769be951f96587b04502d9900c6`; failing exact-head PR CI [41407007210](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41407007210). Runtime fix commit `7c0e758776262c8415116d6a404626d061642657`; exact-head PR CI [41407108435](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41407108435) SUCCESS. 145 Python unittest tests; browser engine tests, generated-data reproducibility, evidence audit and production build passed. |

The validator now requires the `final_ipa` key to be present for every adjudication. `UNRESOLVED` must supply explicit JSON `null`; `AGREEMENT` and `RESOLVED` still require a typed IPA object. No phonology rules, corpus labels, source data or benchmark scores changed. Optional diagnostic runs: [41407108369](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41407108369), [41407108418](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41407108418). Gold remains 0 and empirical accuracy remains null.


### Unresolved adjudication explicit-null positive-path coverage — 2026-11-02

The regression suite now also proves the valid complementary case: `decision=UNRESOLVED` with an explicitly present `final_ipa: null` is accepted and remains excluded from adjudicated gold. Test commit `dbbac42d4a4879d0bf340027037a3edba60063d2`; exact-head PR CI [41407386614](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41407386614) SUCCESS. 146 Python unittest tests; browser engine tests, generated-data reproducibility, repository evidence audit and production build passed. Optional diagnostics: [41407386667](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41407386667), [41407387018](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41407387018) SUCCESS. This does not create IPA labels or change the gold count (still 0) or accuracy (still null).

## External G2P engine coverage audit — 2026-11-02

- **PARTIAL (DONE_VERIFIED diagnostic execution):** `lao2ipa==1.0.0` ran 37 engineering fixtures: 0/37 external fixture matches; 31 tone-only heuristic differences and 6 segmental/offglide differences. Goruut source snapshot `b224bde` ran 100 source-attested cases: 4/100 exact matches, 19 failed outputs, 14 unstable engineering outputs, 47 complete / 34 partial / 19 unknown coverage. See `docs/research/external-g2p-benchmark-and-engine-coverage-2026-11-02.md` and Actions runs 41409083914 / 41409083978.
- **NOT SCORED:** independent expert-adjudicated IPA gold remains 0; no accuracy score is valid. Tone-stripped agreement is not an accuracy metric.
- **TODO:** inspect six non-tone Lao2IPA mismatches and all tone disagreements with qualified Lao reviewers; record upstream Goruut language-bundle absence of `weights9.bin.zlib` as BLOCKED pending upstream clarification or asset publication; benchmark MekongPhon Lao model on a profile-compatible held-out set.


## Goruut language-bundle asset status correction — 2026-11-02

The previous TODO wording suggesting that this repository can simply recover or fix `weights9.bin.zlib` is superseded. Inspection of the exact upstream Goruut source tree at `b224bde02151f8f86d0fe260804e4ca743bda620` shows no `weights9.bin.zlib` in `dicts/lao/`, `dicts/khmer/central/`, or `dicts/burmese/`; the earlier `weights7` and `weights8` assets are present. This is an upstream language-bundle omission in the pinned snapshot, not a missing project-owned file. Status: **BLOCKED (upstream dependency)**. Acceptance: upstream publishes the asset or documents the expected model-tier fallback, and a controlled same-input comparison plus independent expert IPA gold establishes whether the asset changes relevant language coverage. Do not synthesize weights, download unpinned substitutes, or treat the warning as a failed workflow. See the external-engine research audit and canonical handoff for the evidence.


## Additional MekongPhon transformer baseline inventory — 2026-11-02

| ID | Priority | Status | Evidence / acceptance |
|---|---|---|---|
| LAO-MEKONGPHON-TRANSFORMER-001 | P1 | TODO | Published tonal and non-tonal 33.6M-parameter BERT encoder–decoder models exist at [lao-ipa-tonal](https://huggingface.co/byumatrixlab/lao-ipa-tonal) and [lao-ipa-nontonal](https://huggingface.co/byumatrixlab/lao-ipa-nontonal). The non-tonal model explicitly omits tone and is not a complete comparator for this project's tonal target. Pin immutable revisions/checksums, verify dialect/IPA convention/split, and run a reproducible same-input held-out diagnostic with tone, segmental, length, coda and boundary metrics. Do not score against source-attested labels as independent gold. |


## Main publication reconciliation — 2026-11-02

Supersedes earlier handoff statements that the review branch was still ahead of `main` and unmerged: PR [#98](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/98) was merged into `main` as `ed36e7030df4ec8c1b70b50fdcfd6e47e5770d52`; this was the repository's current `main` tip at reconciliation. Exact-head engineering workflows on the PR head passed: verify [41413902679](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41413902679), Goruut [41413902653](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41413902653), and lao2ipa [41413902805](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41413902805). The Pages workflow is configured to deploy from `main`; the public site and post-merge deployment run could not be independently inspected from this session, so deployment status remains **BLOCKED (external verification/network access)**, not claimed successful. No UI/runtime files were changed by this PR. Independent expert-adjudicated gold remains 0 and accuracy remains null; the project is still a research prototype.


## Quality/profile review update — 2026-11-02

- Current main: `33ac5615b13fec717ce59ee55229b9d11f04893d`; exact-main verify [41418528760](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41418528760) and Pages [41417298476](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41417298476) SUCCESS.
- Overall judgement: PARTIAL research prototype; no empirical IPA or Ukrainian accuracy is available (independent gold=0, accuracy=null).
- External diagnostics: Goruut latest 100-row raw-output diagnostic (run 41409083978): 81 outputs / 19 none, 47 complete / 34 partial / 19 unknown, 14 unstable, 4/100 source-attested exact matches; a previous three-repeat artifact reported 3/100 all-repeat and 9/100 any-repeat matches. lao2ipa 37-case mismatch taxonomy is diagnostic only. None of these figures is accuracy or selects a production winner.
- Tone convention, expert adjudication, six non-tone mismatch reviews, MekongPhon rights/profile/split verification, upstream weights9 asset blocker, and manual accessibility QA remain open.



## Execution handoff checkpoint — 2026-11-02

- Review PR: [#100](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/100), branch `research/lao-quality-review-20261102`, based on main `33ac5615b13fec717ce59ee55229b9d11f04893d`.
- Canonical handoff update commit: `4d8b0a9cef92553c1ad187710567f3558b510aae`.
- Immediately preceding exact-head verification: [41458000116](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41458000116) SUCCESS — 146 Python tests, browser suites 50 + 23 + 27 + 7, data/evidence audit, generated-data reproducibility and built-page checks.
- The remaining work is evidence-limited, not a CI failure: independent expert IPA gold=0; tone and segmental disagreements need qualified Lao review; Goruut is not a production candidate; MekongPhon tonal-model comparison remains unverified.
- PR #100 is open and mergeable. This register update is documentation-only and is intended to trigger a fresh exact-head verification.


## Pilot profile decision — 2026-11-02

| ID | Status | Decision / evidence | Remaining acceptance |
|---|---|---|---|
| LAO-PROFILE-001 | DONE_VERIFIED (pilot-scope decision only) | Contemporary central Vientiane Lao, careful citation forms; project-local ID `lao-vientiane-careful-citation-v1`. Ueda (1994) describes central Vientiane; Enfield (2007) supports the documented Vientiane-oriented reference scope. Issue #99 and canonical handoff updated. | Approve IPA convention; recruit two annotators + independent adjudicator; curate rights-cleared 30-item sample; blind dry-run and adjudicate. No claim of runtime completeness or linguistic accuracy. |


## Engineering-method integration — 2026-11-02

| ID | Status | Evidence | Remaining acceptance |
|---|---|---|---|
| ENG-METHODS-001 | DONE_VERIFIED (repository-context integration) | Added GLOSSARY.md, docs/agents/issue-tracker.md and docs/agents/codebase-map.md; linked them from AGENTS.md; refreshed exact upstream method pins. Exact-head CI before handoff closeout: [41468921762](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41468921762) SUCCESS. | Re-check these maps whenever entry points, data ownership or test commands change. This task does not establish linguistic accuracy or independent gold. |

The three references are used as methods, not runtime dependencies: Superpowers for explicit scoped execution and verification; Matt Pocock Skills for domain vocabulary, clear interfaces, source-backed research and two-axis review; Ponytail for real-flow mapping, minimal complete changes and residual-risk reporting. No production code or linguistic labels were changed by this task.


## Benchmark and corpus review — 2026-11-02

| ID | Status | Evidence | Remaining acceptance |
|---|---|---|---|
| BENCH-REVIEW-001 | PARTIAL (existing diagnostic evidence reviewed) | Reviewed fixtures, corpus files, gold lifecycle files, benchmark harnesses and external raw-output reports. Exact-head engineering CI: https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41469198646 SUCCESS. | Independent expert gold remains 0; resolve profile/convention, rights, held-out split and double-annotation/adjudication blockers before accuracy scoring. |

Comparator concordance is not accuracy. See the dated benchmark review in the canonical master handoff for language-specific results and acceptance criteria.


| BENCH-BYU-LAO-001 | PARTIAL | Inspected MekongPhon at `f80f6c1840c4818b51e05f2e00cded4701a5b662`: lexical split 6,219 train / 100 eval, 0 orthographic overlap; SEAlang `kerr72` source path and tone normalization inspected. BYU tonal model card declares Apache-2.0 weights, while MekongPhon repository license metadata is null. | Pin exact model/tokenizer revisions and weight hashes; establish corpus/lexicon rights; confirm Vientiane careful-citation IPA compatibility; run the 100 lexical OOV cases as external diagnostics only; independently adjudicate discrepancies. Not gold and not accuracy. |


**Clarification to BENCH-BYU-LAO-001:** the included `data/splits/lao_train.csv` / `lao_eval.csv` files are lexicon partitions, not demonstrated model-training manifests. MekongPhon `data/README.md` misdescribes the inspected files as OPUS sentence splits; `pipeline/convert_lao.py` references different train/full-lexicon paths. Exact checkpoint-to-split linkage is unverified. Keep the 100 items as a candidate diagnostic, not a validated model holdout.


## Upstream methodology pin reconciliation — 2026-11-02

| ID | Status | Evidence | Acceptance / limitation |
|---|---|---|---|
| ENG-METHOD-PIN-002 | DONE_VERIFIED (documentation provenance correction) | Corrected `AGENTS.md` and the canonical handoff to distinguish `mattpocock/skills` release v1.3.2 (`d1478fcb140db0b93c0c8df17bcfd311844749d0`) from the latest inspected `main` snapshot (`4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`, 2026-10-31). The newer main commit adds the `software-factory` glossary/design skill; no unrelated factory workflow was imported. | Methodology metadata only. No runtime, linguistic rules, corpus, license grants or accuracy metrics changed. Recheck upstream pins when methodology sources are intentionally refreshed. |


## Late-session verification checkpoint — 2026-11-02

| Evidence | Result |
|---|---|
| Review PR | [#100](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/100) on `research/lao-quality-review-20261102` |
| Base / exact head | `33ac5615b13fec717ce59ee55229b9d11f04893d` / `b54e00cee6af6f47534b0e1b3c547d925547e653` |
| Branch divergence | 25 ahead, 0 behind |
| Exact-head hosted workflow | [41476241049](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41476241049) — SUCCESS (`verify`) |
| GitHub review state | No submitted reviews or unresolved review threads returned |
| Local clean checkout | BLOCKED: `git clone` could not resolve `github.com`; no local test execution claimed |

This is an engineering-state recheck only. Independent expert-adjudicated IPA gold remains 0; empirical pronunciation accuracy remains null. Existing linguistic, source-rights, held-out-split, human-adjudication and manual accessibility acceptance criteria remain unchanged. No linguistic labels or runtime rules were altered by this checkpoint.


## Public website verification — 2026-11-02

Lao: DONE_VERIFIED — current-main Pages build/deploy smoke passed (run 41417298476); exact review-head engineering CI passed (41531138983). PARTIAL — output transformation is covered by Node engine regression tests, but the deployed UI has no browser-driven input/result assertion. BLOCKED — direct live-site access from this runner failed at DNS resolution; this is not evidence of a site outage. TODO — add Playwright DOM assertions for input → UA/IPA output, clear and mode switching, plus a post-deploy browser smoke. See master handoff for evidence and acceptance criteria.

## Browser interaction verification — 2026-11-02

- **DONE_VERIFIED (automated browser path):** Added pinned Playwright Chromium coverage for real built-site interactions: `ຂາ` renders Ukrainian `к'а` and IPA `kʰaː`; malformed mixed-script input is withheld; clear restores the empty state; phonetic and romanization modes remain distinct. Exact-head CI [41532309461](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41532309461) passed, including the Chromium UI step.
- **PARTIAL:** this verifies the production build in headless Chromium, not the currently deployed public URL from an external user network. Existing Pages deployment smoke checks fetch published HTML and runtime assets; manual mobile, keyboard and assistive-technology QA remains open.
- **TODO:** execute the same browser interaction suite against the deployed Pages URL and record mobile/screen-reader results. Do not treat this as linguistic gold or accuracy evidence.

## Exact-head browser test result — 2026-11-02

- Exact final UI gate: [41532837406](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41532837406) SUCCESS on the documentation-updated branch head. The four Chromium browser tests passed, including visible Ukrainian/IPA output, malformed mixed-script withholding, clear/reset and mode separation.


## Browser interaction verification — 2026-11-03

| ID | Status | Evidence | Remaining acceptance |
|---|---|---|---|
| LAO-UI-001 | PARTIAL | Exact PR-head verification [41533067192](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41533067192) SUCCESS; four Chromium tests exercise visible `ຂາ` → `kʰaː` → `к'а`, mixed-script withholding, clear/reset and mode separation against the built site. | Verify the public Pages URL after deployment and complete manual keyboard, screen-reader and mobile QA. This is UI engineering evidence, not phonetic accuracy. |


## New source-level evidence — Vientiane Lao profile (2026-11-03)

| ID | Status | New evidence | Acceptance / limitation |
|---|---|---|---|
| LAO-PROFILE-SOURCE-001 | PARTIAL | Full-text review of Ueda (1994), DOI [10.11435/GENGO1939.1994.106_95](https://doi.org/10.11435/GENGO1939.1994.106_95): one Haysok/Vientiane informant; 20 initial consonants; nine short/long vowel-quality pairs; three diphthongs; nine finals; five-tone basic analysis with a qualified variable sixth-tone discussion. | Use as a source-specific provisional profile, not a population norm or complete orthography-to-IPA mapping. Obtain additional speaker-level/primary evidence and adjudicated lexical items. |
| LAO-GOLD-PILOT-001 | BLOCKED | No new gold annotations created. The 1994 article is descriptive single-informant evidence, not a licensed, independently double-annotated project benchmark. | Freeze profile and IPA convention; select sourced lexical contrasts; two independent qualified annotators and separate adjudicator; record alternatives/uncertainty, source locators and rights. Gold remains 0; accuracy null. |

The Ukrainian transcription-method comparator Musiichuk (2022), DOI [10.36059/978-966-397-283-1-64](https://doi.org/10.36059/978-966-397-283-1-64), informs the design decision process only; Vietnamese mappings are explicitly not adopted. No runtime rule, IPA label, or benchmark score changed in this research pass.


## Follow-up corpus lead and annotation acceptance — 2026-11-03

| ID | Status | Evidence update | Acceptance / limitation |
|---|---|---|---|
| LAO-MEKONGPHON-2026-001 | BLOCKED | Shurtz et al. (2026), [MekongPhon: A Large-Scale Parallel IPA Corpus for Lao and Khmer](https://doi.org/10.63317/4bb9rvdshu4z), is a new relevant corpus lead; paper PDF/release metadata unavailable in this pass. | Verify item-level IPA convention, dialect/speaker metadata, source provenance, splits and redistribution license from primary artifacts before use. Do not treat title or model concordance as gold evidence. |
| LAO-GOLD-AGREEMENT-001 | TODO | Cucchiarini (1996), DOI [10.3109/02699209608985167](https://doi.org/10.3109/02699209608985167); Oller & Ramsdell (2006), DOI [10.1044/1092-4388(2006/100)]. | Pilot reports exact normalized and alignment-aware feature-weighted agreement; separate tone, vowel length, coda, syllable/foot boundary, alternatives and adjudication rates. Raw percent agreement is supplementary. |

No gold annotations or runtime changes resulted. Independent gold remains 0; accuracy null.


## MekongPhon artifact-level evidence — 2026-11-03

| ID | Status | Evidence update | Acceptance / limitation |
|---|---|---|---|
| LAO-MEKONGPHON-2026-001 | PARTIAL | Shurtz et al. (2026), DOI [10.63317/4bb9rvdshu4z](https://doi.org/10.63317/4bb9rvdshu4z): paper reports 367k Lao orthography–IPA pairs and under 2% held-out CER. Public repo [byu-matrix-lab/MekongPhon](https://github.com/byu-matrix-lab/MekongPhon), tree SHA f80f6c1840c4818b51e05f2e00cded4701a5b662, has no LICENSE file; scraper uses SEAlang kerr72; tracked lexicon 6,319 rows, 6,219 train + 100 eval (3 duplicate train orthographies). | External baseline candidate only. Paper proceedings CC BY-NC 4.0; separate corpus license/source rights remain unverified. Verify actual model-card commit, dialect/IPA convention and evaluation manifest before use. No import as gold. |
| LAO-MEKONGPHON-REPRO-001 | BLOCKED | Checked-in splitter emits *_train_cleaned.csv / *_eval_cleaned.csv; conversion script references different absent paths and points evaluation mapping at full lexicon. OPUS sentence corpora are downloaded externally and not tracked. | Obtain author run manifest and reproduce exact sentence/lexeme split; verify held-out lexeme disjointness before interpreting paper CER as OOV evidence. |
| LAO-MEKONGPHON-MODEL-001 | PARTIAL | [Tonal](https://huggingface.co/byumatrixlab/lao-ipa-tonal) and [non-tonal](https://huggingface.co/byumatrixlab/lao-ipa-nontonal) HF model cards declare Apache-2.0 model licenses. | Model artifact license does not clear training corpus or SEAlang source rights. Candidate external baseline only; verify profile and IPA convention, pin immutable model revision, then compare against independent gold. |

Accuracy remains null; independent adjudicated gold remains 0. The paper's reported CER is not ClippyFirst accuracy.

## External source reproducibility correction — 2026-11-03

- MekongPhon's public Lao split is recorded as 6,219 train / 100 eval with zero orthographic overlap, but the repository's converter path and split filenames do not align and evaluation mapping points to the full lexicon. Therefore the public tree does not independently demonstrate that its 100-item holdout generated the paper's reported held-out CER.
- The repository has no tracked dataset LICENSE; Apache-2.0 on the two Hugging Face model cards applies to the model artifacts, not automatically to scraped lexicon/OPUS training data. MekongPhon remains candidate-only, rights/profile/methodology unverified, and is not gold.
- Common Voice v27.0 Lao has 193 validated clips from 16 contributor IDs (0.35 validated hours), with no accent/variant metadata. It is an audio lead only, not evidence of Vientiane coverage or a suitable citation-form lexical gold set.


## Citation metadata reconciliation — 2026-11-03

| ID | Status | Work remaining | Acceptance |
|---|---|---|---|
| LAO-CITE-001 | PARTIAL | Targeted MekongPhon in-text citation normalized to Shurtz et al. (2026); broader source-to-claim and repository-wide citation completeness remains unaudited. | Every cited claim maps to a complete, source-verified record; source scope, profile, data rights and paper-vs-repository evidence are distinguished. |

The targeted citation correction is documentation-only. Current code verification remains run [41605468171](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41605468171) on `361e3c48a8216a3add5074bc0096cf545713fe18`; later documentation commits did not change code. Independent gold remains 0; accuracy null.

## Parallel open-PR reconciliation — 2026-11-03

- [PR #101](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/101) independently fixes manifest-wide IPA-gold split identity: every row across all lexeme groups must share one frozen `(seed, version)`; extending a manifest inherits it; conflicting overrides and empty explicit values fail. Exact-head verify [41615750913](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41615750913) passed. It changes `scripts/ipa_gold_corpus.py` and its tests, not the current #100 browser/research work; do not duplicate the implementation.
- [PR #102](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/102) adds structured `SRC-MEKONGPHON-2026` source-registry metadata and an external G2P benchmark audit. Exact-head verify [41615147342](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41615147342) passed. The current #100 branch normalizes the playbook citation but does not contain the source-registry entry or benchmark document; leave this as a separate, complementary PR rather than cherry-picking duplicates.
- Both #101 and #102 are open, mergeable, based on current main with zero behind commits. They also edit the canonical handoff/register, so integrate their documentation hunks deliberately if either is merged. No PR was merged in this pass.