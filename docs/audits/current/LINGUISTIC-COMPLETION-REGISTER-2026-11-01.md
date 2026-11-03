# Lao linguistic completion register — 2026-11-01

**Baseline code commit:** `7743513495beb1f9c222e6ff14151eb21657fa45` (PR base snapshot; subsequent benchmark and handoff changes are on the review branch).
**Latest exact-main evidence:** verify [41649936775](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41649936775) SUCCESS; Pages/deployed smoke [41647974321](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41647974321) SUCCESS.
**Open pull requests at this checkpoint:** implementation PR #113; documentation-only PR #112 is superseded by the equivalent handoff/register correction on the implementation branch.
**Latest exact-main engineering evidence:** verify [41326457758](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41326457758) succeeded.
**Scope:** continue the existing master handoff; this register does not replace it.

## Evidence-based task ledger

| ID | Status | Work remaining | Acceptance |
|---|---|---|---|
| LAO-GOLD-001 | BLOCKED | No independent expert-adjudicated lexical IPA gold exists; `data/benchmark/gold.tsv` contains only its header. | At least two independent qualified annotators, adjudication, dialect/profile and IPA convention fixed, source/audio locators retained; held-out split frozen before scoring. |
| LAO-PHON-001 | PARTIAL | Validate complete tone/rhyme interactions, multi-syllable segmentation and remaining uncertain grapheme combinations against primary sources and experts. | Every supported rule has scoped primary evidence, counterexamples and shared Python/browser fixtures; unresolved cases fail closed. |
| LAO-LAB-001 | PARTIAL | Labialized onsets are structurally represented but lack justified Ukrainian correspondences. | Expert-reviewed IPA inventory and target policy; otherwise remain IPA-only/unsupported, never guessed. |
| LAO-ROM-001 | PARTIAL | CLDR/BGN-derived crosswalk is provisional and does not cover every source structure; BGN `ຫຣ` remains unsupported. | Source-located full inventory, context rules, round-trip/ambiguity tests and explicit non-reversibility; separate from phonetic mode. |
| LAO-G2P-001 | DONE_VERIFIED (diagnostic harness only) | Goruut remains unsuitable for production. | Do not promote on comparator concordance; any new claim requires independent gold and repeatable full coverage. |
| LAO-UI-001 | TODO | Manual visual, keyboard, assistive-technology and mobile QA is not established by CI. | Recorded test matrix and results on deployed site. |
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
| IPA-GOLD-SPLIT-001 | DONE_VERIFIED | Deterministic hash-based group split; one frozen seed/version is enforced across the entire manifest, including distinct lexeme groups; new groups inherit the existing identity and conflicting overrides are rejected |
| IPA-GOLD-EXPORT-001 | DONE_VERIFIED | Rights-filtered typed IPA export retaining source/license/evidence locators |
| IPA-TYPED-BENCHMARK-001 | DONE_VERIFIED | Different or missing IPA kind cannot count as an exact match |
| IPA-GOLD-RELEASE-GATE-001 | PARTIAL | Tag/manual workflow requires 100/25/25 adjudicated train/dev/test; owner must require the check in release rulesets/procedure |

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


## IPA-GOLD-SPLIT-MANIFEST-IDENTITY-001 — 2026-11-03

**Status: DONE_VERIFIED (runtime validator and split generator).** Root cause: the previous cross-file validator checked seed/version consistency only within each `lexeme_group_id`, allowing distinct groups in one corpus manifest to carry different seeds or versions. The split generator could also add a new group under a newly supplied seed while preserving older groups, silently creating a mixed manifest.

- Added regression coverage for mixed seeds and mixed versions across distinct groups, plus conflicting seed override when extending an existing manifest.
- The tests-only commits failed for the intended three behaviors: 41612954045. The implementation and assertion correction are on branch head `839b59b08d5b`.
- Exact-head CI: [41613340163](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41613340163) SUCCESS — 149 Python tests; the full repository workflow also completed successfully.
- New invariant: a single manifest has one `(seed, version)` pair globally; existing manifests retain that identity when extended; explicit conflicting overrides fail closed. A new corpus split design requires a separate versioned manifest.
- This is an engineering reproducibility fix only. It creates no linguistic labels and does not change gold count (0) or accuracy (`null`).

- Follow-up strictness regression: explicit empty `--seed` and `--version` must fail instead of falling through to defaults. Tests-only CI failed on both behaviours (41615374874); the corrected conditional default resolution passed exact-head CI 41615556868.


## Separate-manifest creation acceptance — 2026-11-03

**Status: DONE_VERIFIED on the dedicated PR branch; merge to main remains pending.** Added an acceptance test proving a genuinely new seed/version can be used when the caller supplies a separate empty JSONL input via `--splits`, while the existing frozen manifest remains untouched. Corrected the operator instructions: changing only `--output` does not reset the input manifest; the new-manifest workflow must use a new empty `--splits` file and a distinct `--output` file.

- PR [#101](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/101), final documentation head `b008b824fb5c95861f4e3d8766c8307515df0c02`; code/test checkpoint `e8ab5545d554b09d3c3ba742d7b5aa58aafbdb44` (the three subsequent commits are docs-only).
- Exact-head CI [41638528514](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41638528514) SUCCESS — 152 unittest tests; exact-head workflow success.
- No linguistic gold rows were added; independent gold remains 0 and empirical accuracy remains `null`.


## Split-manifest integration checkpoint — 2026-11-03

**Lao PR #101: DONE_VERIFIED on main.** Merged as `ccb6ba44d9448858091306d606a7bba50f19a5de`. The global manifest identity invariant and separate-manifest creation acceptance are now in the default branch. Exact-main workflow [41643375975](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41643375975) succeeded. No gold rows were added; adjudicated gold remains 0 and empirical accuracy remains `null`.


## Source-citation reconciliation — 2026-11-03

**Status: PARTIAL pending exact-head verification.** MekongPhon is added to the Lao source registry and author–year citation. Its 367,000 Lao pairs and under-2% held-out CER are attributed to the paper; dialect/IPA compatibility and corpus redistribution rights remain unresolved.

- This clean port is based on the latest main after the split-manifest integration; superseded PR #102 is not used as a merge candidate.
- No pronunciation labels or corpus records imported; rights remain source-specific; independent gold remains 0 and accuracy remains `null`.


## LAO-UI-001 — built-site browser regression coverage — 2026-11-03

**Status: PARTIAL pending exact-head CI and manual QA.** Added Playwright tests for visible IPA/Ukrainian output, mixed-script fail-closed behavior, clear/reset and romanization/IPA-first separation; CI and Pages build workflows now run them against the built site.

- Browser test dependency is pinned to `@playwright/test 1.63.0`, but no lockfile is committed; transitive dependency reproducibility remains a follow-up improvement.
- Manual visual, keyboard, screen-reader and mobile QA remain TODO. Automated browser success cannot substitute for those checks.
- No linguistic rules or gold labels changed; adjudicated IPA gold remains 0 and accuracy remains `null`.


## Continuation status sync — 2026-11-03

- Current main: `ecd61a110a4ca8b25535570e0baab79c0e567436`; exact-main checks: verify 41647974181 SUCCESS; Pages 41647974321 SUCCESS.
- PR #100 is closed without merge; its browser/quality portions have been ported to main. No open PRs were returned by the current open-PR query.
- Engineering improvements on main are verified at the stated commit; this does not promote linguistic validation or manual accessibility tasks to DONE.
- IPA gold remains 0; empirical accuracy remains null. Annotation staffing, convention approval, rights clearance, blind intake and adjudication remain BLOCKED on external human/evidence dependencies.


## LAO-METHOD-REFRESH-001 — upstream methodology snapshots — 2026-11-03

**Status: DONE_VERIFIED (reference audit).** Superpowers v7.0.1 current main: `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`; mattpocock/skills v1.3.2 release: `d1478fcb140db0b93c0c8df17bcfd311844749d0`, current main snapshot: `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`; Ponytail v5.3.3 release: `7801d061243d7b753bad0e0b3c057cd250b11755`, current main: `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846` (README-only post-pin change).

- Release pins and current-main snapshots are distinguished. No third-party runtime or skill files imported.

## 2026-11-03 — held-out benchmark split enforcement

| Task | Status | Evidence / remaining acceptance |
|---|---|---|
| IPA-BENCH-SPLIT-001 | DONE_VERIFIED (engineering contract) | Export preserves the frozen group-safe split; scorer defaults to test and requires explicit selection for train/dev/all. Exact-head verify [41651864836](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41651864836) SUCCESS on `7d2c37f8ceb9dd77aea2d40a8340a919d66c5b33`. This fixes the evaluation boundary, not linguistic gold. |

Independent gold remains 0 and accuracy remains null. No data labels were fabricated. The split-aware benchmark documentation is in `docs/benchmarking-and-external-ipa.md`.

## Frozen split manifest provenance — 2026-11-03

The export and benchmark now preserve and validate the complete frozen split identity, not only the bucket name: `split`, `split_seed`, and `split_version`. Every adjudicated row must carry non-empty seed/version metadata, and the benchmark rejects a TSV that mixes manifest identities. The report exposes the manifest seed/version and selected scoring split. This makes the evaluated test partition traceable to one exact manifest; it does not create linguistic gold or change the current zero-row accuracy status.


## 2026-11-03 — empty benchmark prediction input

| Task | Status | Evidence / remaining acceptance |
|---|---|---|
| IPA-BENCH-EMPTY-PREDICTIONS-001 | DONE_VERIFIED (engineering guard) | Header-only prediction TSV previously exited 0 and produced an empty `engines` object. Test-first regression failed on all three language repositories; the scorer now rejects an empty prediction dataset after checking gold and frozen split provenance. Missing individual predictions within a named engine remain denominator-counted. RED: [41655160456](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41655160456). Final exact-head verify: [41655452782](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41655452782) SUCCESS. |


## 2026-11-03 — benchmark identifier validation

| Task | Status | Evidence / acceptance |
|---|---|---|
| IPA-BENCH-IDENTIFIERS-001 | DONE_VERIFIED (engineering guard) | Reject whitespace-only gold IDs, prediction IDs and engine names while preserving non-empty identifiers exactly. Test-first RED: gold-ID run 41660752360; prediction-ID/engine run 41662058993. Final exact-code-head CI: 41662219515 SUCCESS (159 Python tests and 4 built-site browser tests passed).  No linguistic labels or accuracy claims were added. |