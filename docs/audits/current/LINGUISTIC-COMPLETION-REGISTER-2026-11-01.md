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
