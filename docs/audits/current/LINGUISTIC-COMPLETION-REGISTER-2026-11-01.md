# Lao linguistic completion register — 2026-11-01

**Baseline:** `main` `6f607d7ab4d432fd8491a5fcee32186e4269fc32`.
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
| IPA-GOLD-SPLIT-001 | DONE_VERIFIED | Deterministic hash-based, frozen lexeme-group split and leakage checks |
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
| ENGINEERING-METHOD-REFRESH-001 | PARTIAL | Refreshed the Ponytail reference to v5.3.3 and documented the current Superpowers 7.0.1, mattpocock/skills main, and Ponytail 5.3.3 method snapshots in `AGENTS.md` and the canonical handoff. Exact-head CI for this documentation update is pending. |

