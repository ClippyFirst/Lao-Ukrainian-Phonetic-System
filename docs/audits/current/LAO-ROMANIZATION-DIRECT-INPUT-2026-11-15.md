# Direct Lao romanization input — implementation audit (2026-11-15)

## Summary

A direct Latin-script input route is present in the Lao → Ukrainian service. A follow-up audit corrected the bounded ALA-LC 2012 normalizer against the complete Library of Congress table text and notes.

**Base main:** 5717c2fd95c467c48b3909c86252fba5deca0695  
**Working branch:** fix/ala-lc-2012-conformance-20261115  
**Verified PR head:** 92d90a3a5dc8cc1f174a52475df2213d29538d00
**Merged main commit:** 3f4e2df2193ffbfad10a68bbdde30dc4f9f8c8f2  
**PR #173:** https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/173 — merged.

## Implementation

- Separate input mode for Lao script vs romanized Latin text.
- Explicit profile selector for automatic, BGN/PCGN 1966 / CLDR Lao-Latin, and bounded ALA-LC 2012 normalization.
- Existing onset/nucleus/coda parser reused for standalone romanization.
- Strict BGN/PCGN direct-input mode enforces note 4: an onsetless syllable inside a word must be hyphenated. The official Viangchan example is supported.
- ALA-LC normalization now follows the LOC table's vowel spellings in the implemented subset: u/ū, uʼ/ūʼ, e/ē, æ/ǣ, oe/ōe, ia/īa, ua/ūa, ai/āi, ao, and am.
- ALA-LC ny is retained as its own palatal-nasal onset, not rewritten to BGN/PCGN gn.
- ALA-LC uses a separate onset/coda inventory. Supported final spellings are k, ng, t, p, n, m; final ວ may be written o after a vowel. s, v, r, and l are not accepted as final spellings.
- Short u is no longer incorrectly normalized to long ū.
- Automatic profile detection recognizes ALA-LC modifier-apostrophe vowels and oe in addition to distinctive diacritics and ny before a vowel.
- Unsupported/ambiguous strings remain visible as ⟦…⟧; no IPA is invented from romanization-only input.
- būak remains PARTIAL when the direct string admits multiple syllable divisions without source boundaries.
- Initial ʻ has no project-approved Ukrainian target; medial w clusters, contextual ວ alternations and wider loanword/boundary conventions remain partial.

## Evidence and standards

- Library of Congress, ALA-LC Lao Romanization Table (2012), SRC-ALA-LC-LAO-2012, especially consonant initial/final columns and notes 1–10.
- PCGN BGN/PCGN 1966 agreement and 2023 Laos Toponymic Factfile ground the provisional BGN/PCGN-derived profile and the Viangchan example.
- LDC Language Specific Peculiarities Document for Lao, section 5, lists BGN/PCGN, RTGS and ALA-LC among schemes used for Lao. It does not supply a complete normative Lao-specific RTGS table in the cited section.
- ALA-LC support remains a bounded subset, not full conformance.

## Task ledger

| Task | Status | Acceptance evidence |
|---|---|---|
| Direct romanization input control and UI state | DONE_VERIFIED | Exact-head Chromium workflow passed |
| Standalone BGN/PCGN syllable conversion | DONE_VERIFIED | Unit/browser fixtures, including Viangchan |
| ALA-LC vowel and positional subset | DONE_VERIFIED | LOC-derived vowel tokens, ny, final spellings, vat and ambiguous būak fixtures |
| Full ALA-LC contextual conformance | PARTIAL | Initial ʻ, medial w clusters, contextual ວ, loanword and word-boundary behavior incomplete |
| Auto profile detection | PARTIAL | Heuristic fixture; no broad real-world corpus |
| Preserve ambiguous and unsupported text | DONE_VERIFIED | Parser emits visible unresolved brackets and PARTIAL status |
| Prevent invented IPA from romanization | DONE_VERIFIED | IPA panel hidden in direct input mode; no phonetic engine call |
| RTGS-for-Lao | BLOCKED | Needs a stable Lao-specific adaptation table and reviewed examples |
| Informal/French-style/Karaoke variants | DEFERRED | Conventions vary; define scope and evidence before implementation |
| Exact PR-head and post-merge CI | DONE_VERIFIED | PR Verify #4080 / run 43697779828 and main Verify #4082 / run 43697882695 both SUCCESS |
| Independent linguistic accuracy validation | BLOCKED | Needs rights-cleared, expert-adjudicated reference examples and Lao specialist review |
| Manual physical-device and screen-reader QA | BLOCKED | Human review remains outstanding |

## Verification

PR-head Verify #4080, run 43697779828, on 92d90a3a5dc8cc1f174a52475df2213d29538d00: **SUCCESS**. Post-merge main Verify #4082, run 43697882695, on 3f4e2df2193ffbfad10a68bbdde30dc4f9f8c8f2: **SUCCESS**. Pages deployment #96, run 43697882717: **SUCCESS**, including live smoke test.

- Python: 350 passed.
- Node: 182 passed, 0 failed.
- Post-merge main repeated the same 350 Python, 182 Node and 28 Chromium test passes.
- Chromium browser: 28 passed.
- IPA-gold schema validation, repository data/evidence audit, external-G2P syntax/CLI, locked dependency install, build, generated-data reproducibility, built-page and relative-asset checks all passed.

A local clone attempt failed because the execution environment could not resolve github.com. No local test execution is claimed.

## Readiness

**Engineering-verified partial prototype, not release-ready as a universal romanization converter.** BGN/PCGN direct input is tested; the ALA-LC subset now follows the actual LOC 2012 vowel and position spellings more accurately. Full ALA-LC context, RTGS, informal variants, independent gold, specialist review and manual accessibility QA remain outstanding.


## Follow-up guard — 2026-11-15

A second pass over the complete LOC 2012 table identified additional ALA-LC vowel forms outside the normalizer's supported subset: `ư`, `ư̄`, `œ`, `œ̄`, `ǫ`, `ǭ`, `ưa`, `ư̄a`, `iu`, `īu` and `īeo`. LOC Note 4 also documents medial-`ວ` spellings `w`, `ūa`, and the specific `iu`/`īu`/`īeo` forms.

The generic syllable parser can potentially interpret some adjacent-vowel spellings as multiple syllables when no boundary is supplied. To prevent an apparently complete but unsupported parse, the direct ALA-LC route now recognizes these unimplemented LOC forms and withholds the complete fragment as `PARTIAL`. This does not add a Ukrainian mapping or claim support. Regression fixtures cover every listed unsupported form and the LOC examples `khwā`, `khwǣng`, and `būak`.

Acceptance: exact-head Verify #4092 and post-merge Verify #4094 passed the new Node regressions, existing Python/Node/Chromium suites, repository evidence audit, build, generated-data reproducibility and built-page checks. Independent target-language review remains required before any of these forms can be promoted to supported.


## Post-merge verification — PR #176

PR [#176](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/176) merged as `05f2eb231e1bdbda7e12362383122c8f4fb50c70`. Exact-head Verify #4092 / run [43709710488](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43709710488) succeeded, including all Python and Node tests, Chromium UI, repository/evidence audits, external-G2P harness, build, generated-data reproducibility and built-page checks. Post-merge main Verify #4094 / run [43709787347](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43709787347) also succeeded. Pages deployment #97 / run [43709787334](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43709787334) and the deployed-service smoke test succeeded.

The fail-closed guard is now `DONE_VERIFIED` for the enumerated unsupported LOC forms: they remain explicitly PARTIAL instead of being misparsed. This does not promote those forms to supported, nor does it change the broader `PARTIAL` status for full contextual ALA-LC conformance.


## Documentation checkpoint reconciliation — PR #177

PR [#177](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/177) merged as `de9c2516d973f2cd721667e5505e86693cff453d`. Its exact-head Verify #4095 / run [43709949777](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43709949777) and post-merge main Verify #4096 / run [43710037579](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43710037579) succeeded. The workflow passed IPA-gold schema validation, repository data/evidence audit, Python tests, external-G2P syntax/CLI, Node/browser-engine tests, build, generated-data reproducibility, Chromium UI and built-page checks. Exact test counts were not extracted from the latest run and are intentionally not inferred.

PR #177 was documentation-only. The last runtime deployment remains Pages deployment #97 / run [43709787334](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43709787334), which passed its live smoke test on the PR #176 runtime commit `05f2eb231e1bdbda7e12362383122c8f4fb50c70`. Latest repository `main` is the documentation commit `de9c2516d973f2cd721667e5505e86693cff453d`; it must not be confused with a new runtime deployment.

The independent adjudicated IPA gold corpus remains empty (0 examples). This verification is engineering/CI evidence, not independent linguistic accuracy validation.


## PR #192 — unknown profile fail-closed validation (2026-11-15)

The public `analyzeRomanization` API previously mapped every unrecognized explicit `profile` value to `bgn-pcgn`. This could return a plausible result under the wrong convention when a caller misspelled or mis-cased the requested profile.

The implementation now accepts only `auto`, `bgn-pcgn`, and `ala-lc`. Any other explicit value returns:
- overall `PARTIAL`;
- syllable status `UNSUPPORTED_PROFILE`;
- the original input in visible `⟦…⟧` brackets;
- a warning naming the accepted values;
- no romanization parsing or Ukrainian adaptation.

An omitted or null profile continues to use automatic detection. Regression tests cover misspelled, case-mismatched and empty-string values, plus null preserving automatic detection.

**PR:** [#192](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/192), branch `fix/reject-unknown-romanization-profile-20261115`.  
**Exact-head Verify #4158:** [run 43725765654 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43725765654).  
**Merged:** `6bca3d2b899ebdffde02e1b4aa2454f3df1dc06e`. Exact-head Verify #4163 / [run 43725967264 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43725967264); post-merge Verify #4164 / [run 43726041995 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43726041995); Pages #99 / [run 43726042017 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43726042017). This is API validation, not a new linguistic mapping or profile-conformance claim.


## CrossAsia DLLM romanisation profile discovery — 2026-11-15

A source review identified a documented collection-specific Lao romanisation in the Digital Library of Lao Manuscripts (DLLM), hosted by CrossAsia. CrossAsia says it closely follows the revised Royal Thai General System of Transcription for Central Thai but changes three Lao initial consonants: ວ is `v` rather than `w`, ຍ is `ny` for [ɲ], and ຈ is `c` rather than `ch`. It is broad/phonetic and does not mark vowel length or tone. A one-page consonant/vowel table is published separately.

This refines, but does not invalidate, the RTGS blocker: DLLM is a specific library-catalogue convention, not evidence of a generally accepted or national Lao RTGS standard. It must not be merged into BGN/PCGN or ALA-LC. The source page says Lao has no official romanisation and explains that DLLM prioritizes discoverability of manuscript titles; some Indic loanword spellings retain historical forms. The CrossAsia site carries a copyright notice and no explicit open-data licence was identified, so the table was not copied into repository data.

**Disposition:** research candidate only, NOT SUPPORTED. A separate `dllm` profile would require a complete checked transcription of its table, reuse/licensing determination, Ukrainian target policy for all units, regression examples and Lao-specialist review. No runtime code or mappings changed.

Sources: CrossAsia [DLLM romanisation description](https://digital.crossasia.org/digital-library-of-lao-manuscripts-about-dllm-collection/?lang=en), [published consonant/vowel table](https://digital.crossasia.org/wp-content/uploads/2021/10/DLLM_laoromanisation.pdf); LDC [Lao Language Specific Peculiarities Document](https://catalog.ldc.upenn.edu/docs/LDC2017S08/LSP_203_final.pdf).


## UNGEGN 2025 update — Lao national romanization draft status

The UNGEGN Working Group on Romanization Systems' 2025 report adds a material update beyond the 2023 PCGN Factfile. It records that WGRS had been invited to review a draft Lao Romanization System prepared by the National Geographic Department of Lao PDR, had made recommendations, and that as of July 2024 Lao PDR was finalising a draft of toponymy guidelines. WGRS hoped the system would be submitted for consideration at the 2027 UNGEGN session.

This is a draft-development signal, not adoption. It does not establish the final table, a national implementation date, or UN endorsement. The operational profile remains provisional BGN/PCGN-derived CLDR until the draft or subsequent decision is published and reviewed. Do not claim that no work is underway; equally, do not claim the draft is already an official standard.

Source: [UNGEGN WGRS, GEGN.2/2025/26/CRP.26](https://unstats.un.org/unsd/ungegn/sessions/4th_session_2025/documents/GEGN.2_2025_26_CRP26_item5c.pdf), Lao section under “Progress on romanization systems”.


## Source-aware Lao → CLDR → Ukrainian integration regression — 2026-11-15

The direct Latin-only input contract and the source-aware Lao → CLDR → Ukrainian contract must remain distinct. The full official Lao PDR motto was added as a Lao-script regression fixture:

`ສັນຕິພາບ ເອກະລາດ ປະຊາທິປະໄຕ ເອກະພາບ ວັດທະນາຖາວອນ`

The exact provisional CLDR output is `santiphab é-kalad paxathipaait é-kaphab vadthanathav-n`. The fixture covers two different integration conditions:

1. Internal `é-` boundaries mark medial onsetless syllables inside one whitespace-delimited Lao source token. PR #214 fixed the crosswalk cursor so these hyphens do not advance the source-word group.
2. The final `ວອນ` source syllable is represented by CLDR as `v-n`, with the medial `AWW_MEDIAL` vowel omitted. PR #218 restores the vowel only when the original Lao syllable provides an exact onset, unique vowel-ID mapping and coda match. The restored analysis unit carries `sourceRestoredVowel` provenance.

The direct Latin-only form `vadthanathav-n` remains PARTIAL: without the Lao source, the omitted vowel is not recoverable and must not be guessed. This is not a change to the declared direct-input profile and does not recover tone or quantity.

- PR #214 merged as `afc7dc9ed3890dbac2bbf05b253367a459e8367a` (hyphen/source-group alignment).
- PR #218 merged as `fe435317dcb69cd43f0409ca85e9b617b334a584` (full-motto regression and source-backed AWW_MEDIAL recovery).
- Exact-head Verify #4265 / [run 43753154383](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43753154383) passed: 350 Python, 191 Node and 28 Chromium tests plus corpus/data audits, build and generated-data checks.
- GitHub Pages deployment #101 / [run 43753235467](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43753235467) passed both build/Chromium and deployed-service smoke-test jobs for runtime SHA `fe435317dcb69cd43f0409ca85e9b617b334a584`.

### Updated task ledger

| Task | Status | Acceptance boundary |
|---|---|---|
| Source-aware internal-hyphen alignment | DONE_VERIFIED | Full source-word group retained across CLDR medial onsetless hyphens; regression in official motto fixture |
| Source-aware recovery of CLDR-elided AWW_MEDIAL | DONE_VERIFIED (scoped orthographic recovery) | Restore only on exact source onset/vowel/coda match; trace provenance; no direct Latin-only guess |
| Direct BGN/PCGN romanization-only input | DONE_VERIFIED (implemented profile subset) | Preserve conservative parser, ambiguity and unsupported diagnostics |
| Direct ALA-LC 2012 input | PARTIAL | LOC subset and fail-closed unsupported forms verified; full contextual Notes 1–10 not implemented |
| Automatic profile selection | PARTIAL | Heuristic only; broad real-world corpus and false-selection rate unmeasured |
| RTGS/DLLM and informal variants | BLOCKED / DEFERRED | No authoritative complete Lao RTGS adaptation table; DLLM rights/table review and informal-convention scope unresolved |
| Independent phonetic accuracy | BLOCKED | Gold remains 0; romanization route is not IPA evidence |
| Manual device/screen-reader QA | BLOCKED | Requires human review on actual devices and assistive technologies |

**Readiness remains:** engineering-verified partial research prototype, not a universal or linguistically validated romanization converter.


## Explicit fail-closed diagnostics for uncovered core source vowel IDs — 2026-11-15

The source registry contains seven core vowel IDs that are not yet represented by a confirmed CLDR Lao-Latin crosswalk: `UO_LONG_ALT`, `UO_LONG_OPEN`, `OEY`, `OOY`, `AEW`, `AOY` and `AAJ`. The source-aware adapter now preserves the exact ID in the analysis trace and returns a specific PARTIAL warning rather than a generic onset/nucleus/coda mismatch. Seven regression cases exercise this behavior; direct Latin-only parsing is unchanged.

No romanization or Ukrainian mapping was added. The upstream CLDR transform remains provisional and includes context-sensitive rules plus a TODO for final-consonant handling. A new mapping requires exact source-attested CLDR output and specialist review. The full crosswalk remains PARTIAL.


## PR #220 and current deployment reconciliation — 2026-11-15

Seven core source vowel IDs in `data/lao/vowels.csv` still lack a confirmed CLDR Lao-Latin crosswalk: `UO_LONG_ALT`, `UO_LONG_OPEN`, `OEY`, `OOY`, `AEW`, `AOY`, `AAJ`. PR [#220](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/220) now retains the exact ID in the trace and emits a specific PARTIAL warning. All seven are covered by regression tests; no mapping is added. Exact-head Verify #4280 / [run 43755451075](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43755451075) passed 350 Python, 192 Node and 28 Chromium tests. PR #220 merged as `fe1c4a0b8966155b5f22e6cc58ebcb3a33d5bbf9`; main Verify #4281 / [run 43755557872](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43755557872) and Pages deployment #102 / [run 43755557855](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43755557855) both passed. The Pages artifact is deliberately deterministic-only; browser neural Hybrid v2 was retired by explicit owner decision on 2026-11-10 and must not be restored without a new decision.


## Upstream CLDR rule-level check for the seven uncovered source vowels — 2026-11-15

The current upstream Unicode CLDR source was fetched directly from `unicode-org/cldr/common/transforms/Lao-Latin.xml`, blob [`abbf1914a169f334dd43b3f00fce186360950b1e`](https://github.com/unicode-org/cldr/blob/abbf1914a169f334dd43b3f00fce186360950b1e/common/transforms/Lao-Latin.xml). The transform declares `draft="provisional"`, uses the BGN alias, and retains the TODO “handle consonants at the end of words specially”. Its active rule for `ວ` is `v`; the alternative `#ວ → oua` is commented out. The transform also contains individual rules such as `ຍ → gn`, `ຽ → ia`, `ເີ → eu`, `ໂ → ô` and `ແ → è`, but no explicit compound mapping that establishes the intended nucleus-plus-glide decomposition for the seven source IDs below.

| Source ID | Registered source pattern | Why literal CLDR output is not promoted |
|---|---|---|
| `UO_LONG_ALT` | `ວ` | Active CLDR `ວ → v` treats it as a consonant; the vowel candidate `#ວ → oua` is commented out. |
| `UO_LONG_OPEN` | `ວາ` | No explicit `ວາ` compound vowel rule; active character rules do not establish a long /uːə/ nucleus. |
| `OEY` | `ເ◌ີຍ` | Separate `ເີ` and `ຍ` rules do not establish the intended /ɤːj/ compound. |
| `OOY` | `ໂ◌ຍ` | Separate `ໂ` and `ຍ` rules do not establish the intended /oːj/ compound. |
| `AEW` | `ແ◌ວ` | Separate `ແ` and `ວ` rules do not establish the intended /ɛːw/ compound. |
| `AOY` | `◌ອຍ` | The carrier `ອ` is context-sensitive/empty in the transform; no explicit /ɔːj/ compound rule is given. |
| `AAJ` | `◌າຽ` | Separate `າ` and `ຽ` rules do not establish the intended /aːj/ compound. |

This inspection strengthens the evidence for keeping the seven IDs fail-closed; it does not prove that no other romanization standard can represent them. No mapping was added, and no hypothetical concatenated output was treated as a CLDR test result. Acceptance still requires a source-attested exact transform output in the selected profile, source syllable/coda validation, an explicit Ukrainian target decision, positive and negative fixtures, and Lao-specialist review.


## ALA-LC 2012 Note 4 contextual regression checkpoint — 2026-11-16

The Library of Congress Note 4 distinguishes four contexts for Lao ວ: initial `v`; medial before a vowel as a `w` cluster with the initial consonant; medial before a final consonant as `ūa`; and final after a vowel as `o`. It additionally lists `iú`, `īu` and `īeo` forms. The continuation branch adds focused regression tests for the two contexts already supported by the bounded adapter: `būak` (source-aware `UO` nucleus plus final ກ) and `nāo` (source-aware `AA` nucleus plus final ວ). It also asserts that `khwā` and `khwāng` remain PARTIAL rather than being split or assigned an unreviewed Ukrainian cluster output. These tests protect the implementation boundary; they do not complete Note 4 or establish independent linguistic validation.

**Primary source:** [Library of Congress, ALA-LC Lao Romanization Table (2012), Note 4, page 3](https://www.loc.gov/catdir/cpso/romanization/lao.pdf). The rendered PDF confirms the examples `khwā`, `khwāng`, `būak`, `dūai`, `nāo` and `kǣo`, and the additional `iú`, `īu`, `īeo` spellings. The exact target-side handling of medial `w` clusters remains unresolved; no Ukrainian output was invented.

**Continuation branch:** `test/ala-lc-note4-context-regressions-20261116`; PR [#223](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/223) merged as `05644cbece3395122c18fb390aceba80013104cb`. Exact-head Verify #4291 / [run 43825286216](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43825286216) and post-merge main Verify #4292 / [run 43825396272](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43825396272) passed 350 Python, 195 Node and 28 Chromium tests plus repository/evidence audit, build and generated-data reproducibility. The regression batch is DONE_VERIFIED as engineering coverage only; it does not establish full ALA-LC conformance or independent linguistic accuracy.


## PR #223 verification and merge — 2026-11-16

PR [#223](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/223) merged as `05644cbece3395122c18fb390aceba80013104cb`. Exact-head Verify #4291 / [run 43825286216](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43825286216) and post-merge main Verify #4292 / [run 43825396272](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43825396272) both passed 350 Python, 195 Node and 28 Chromium tests, IPA-gold schema validation, repository/evidence audit, external-G2P harness syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks. No runtime assets changed; Pages redeployment was not required.

The test findings are intentionally asymmetric: source-aware `būak` and `nāo` are accepted when Lao syllable structure disambiguates them; the same Latin-only strings remain PARTIAL because competing syllable parses exist. `khwā` and `khwāng` remain PARTIAL pending a reviewed Ukrainian medial-`w` cluster adapter. ALA-LC remains a bounded subset.

## ALA-LC Notes 5–10 contextual regression continuation — 2026-11-16

The official LOC 2012 table was re-read through Note 10. PR candidate `test/ala-lc-notes5-7-regressions-20261116` adds focused source-aware tests for Note 5's six silent-hoa sonorant spellings (using underlying onset plus original expanded `onsetForm`) and Note 7's consonant-before-vowel romanization order. It also asserts the romanization adapter does not expose reconstructed IPA or tone fields. These are engineering fixtures, not expert-validated Ukrainian pronunciation labels.

Notes 6, 8, 9 and 10 are classified explicitly in `docs/romanization-to-ukrainian-matrix.md`: initial `ʻ` and the relevant LOC vowel forms remain fail-closed; numerals are passthrough; lexical word/loanword segmentation and tone omission cannot be reversed; the double-function consonant rule remains partial pending source-segmented examples and a reviewed cross-syllable adapter. No new Ukrainian mapping or IPA claim was introduced.

Primary source: [Library of Congress, ALA-LC Lao Romanization Table (2012)](https://www.loc.gov/catdir/cpso/romanization/lao.pdf), Notes 5–10. Verification is pending exact-head CI; no test result is claimed in this audit entry until CI reports it.

## Verification reconciliation — PR #225 merged (2026-11-16)

PR [#225](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/225) merged by squash as `66224de02f76453555dac805cad560a35fb2b925`. Exact-head Verify #4295 / [run 43840762990](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43840762990) and post-merge main Verify #4296 / [run 43840888440](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43840888440) both succeeded. Each run passed 350 Python tests, 198 Node tests and 28 Chromium tests, plus IPA-gold schema validation, repository/evidence audit, external-G2P harness syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks.

The six Note 5 source-aware fixtures and Note 7 order fixture are now DONE_VERIFIED as engineering regressions. This does not establish expert-reviewed Ukrainian pronunciation or full ALA-LC conformance. Notes 6, 9 and 10 remain partial/unsupported as scoped in the romanization matrix. The branch is test/documentation-only; no Pages deployment was required.

## ALA-LC Notes 6 and 10 source-aware regression — 2026-11-16

PR [#228](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/228) adds:
- A Note 6 source-aware initial-ayn trace: `ʻ` is parsed as the LOC romanization marker for initial Lao `ອ`, with source vowel/coda provenance retained, but the result remains `UNSUPPORTED_ALA_LC_INITIAL_AYN` / PARTIAL because no Ukrainian target value has been approved. Latin-only initial ayn remains withheld.
- A synthetic source-role crosswalk regression using the preferred LOC 2012 Word-source example `khitsatīan`: the fixture explicitly supplies `ສ` as final `t` in one syllable and onset `s` in the next. A negative case without the coda role is withheld. This tests the crosswalk only; it does not assert the exact source-script syllabification of the LOC example.

The positive/negative Note 10 unit fixtures verify the position-specific source crosswalk only; they do **not** verify automatic Lao source segmentation. The browser regression that uses `ຄິຼສຕຽນ` is only a mode-separation check: Lao script is rejected when the direct romanization mode expects Latin text. That string is not the LOC Note 10 example. Full Note 10 conformance therefore remains PARTIAL. No new Ukrainian phonological value, IPA result, or lexical boundary was inferred.

Exact-head Verify #4309 / [run 43848574433](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43848574433) passed 350 Python, 201 Node and 28 Chromium tests (0 failures), plus the workflow's IPA-gold schema, repository/evidence audit, external-G2P harness, build, generated-data reproducibility and built-page/relative-asset checks. This run was on the pre-documentation head `4aa6d7ff3770ae7cb28a8edc3da248a7b2adf1b8`; documentation changes are being verified separately on the final PR head.

Primary source: [Library of Congress, ALA-LC Lao Romanization Table (2012), Notes 6 and 10](https://www.loc.gov/catdir/cpso/romanization/lao.pdf). The LOC table establishes orthographic romanization behavior, not Ukrainian target correspondences.

## PR #228 merged and deployed — final verification (2026-11-16)

PR [#228](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/228) merged by squash as `44b5fa2ebc4380bd9fa4b201e8c8eb52a7ccd900`.

- Exact-head Verify #4313 / [run 43849117284](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43849117284) succeeded on `03fe0bd6956376bf36c106abdfa7d3066f4ec3c6).
- Post-merge main Verify #4314 / [run 43849485259](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43849485259) succeeded on `44b5fa2ebc4380bd9fa4b201e8c8eb52a7ccd900`.
- Both runs passed 350 Python, 201 Node and 28 Chromium tests, with 0 failures; schema, repository/evidence audit, external-G2P harness syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks also passed.
- Pages Deploy #103 / [run 43849485210](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43849485210) succeeded and published the same runtime SHA. Its built-site Chromium suite passed 28 tests; the post-deployment smoke test successfully fetched the published index, methodology page, app.js, data.js, engine.js and styles.css.

**Final disposition:** Note 6 initial-ayn source recognition/provenance is DONE_VERIFIED as an engineering trace only; its Ukrainian target remains intentionally unsupported. Note 10's synthetic source-role crosswalk fixture is DONE_VERIFIED; automatic upstream Lao segmentation of the LOC example remains PARTIAL. The earlier attribution of `ຄິຼສຕຽນ` as the LOC example is corrected below. Full ALA-LC conformance and Note 9 lexical/loanword boundaries remain PARTIAL. No IPA, tone, target correspondence or lexical boundary was inferred. The published site is current at Pages #106 / [run 43932522626 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43932522626); independent IPA gold remains 0 and specialist review remains open.

## Direct-romanization mode-separation guard (2026-11-16)

The Lao-script string `ຄິຼສຕຽນ` was entered into the Latin direct-romanization mode. The browser regression in `tests/browser/site.spec.js` asserts a visible PARTIAL result with unresolved brackets rather than accepting Lao-script characters as Latin romanization. This is a mode-separation guard only; it does not exercise the Lao source parser or LOC Note 10's double-function example.

- PR [#231](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/231), exact-head Verify #4319 / [run 43865169001](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43865169001): SUCCESS.
- Browser suite: 29 passed, including the new direct-romanization mode-separation guard.
- Python tests, Node engine tests, IPA-gold schema validation, repository/evidence audit, external-G2P harness syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks also passed.
- The test input happens to contain U+0EBC LAO SEMIVOWEL SIGN LO (`ຼ`), but this is unrelated to LOC Note 10. The test confirms only that Latin direct-romanization mode withholds Lao-script input; it does not test U+0EBC parsing, LOC syllabification or the repeated coda/onset role.
- Existing Note 10 unit tests are explicitly source-role-supplied synthetic crosswalk fixtures. Automatic LOC lexical/syllabic segmentation is still PARTIAL/BLOCKED pending a reviewed orthographic parser and Lao-specialist source-role policy.

No runtime code, IPA, tone, lexical boundary or Ukrainian mapping changed.

### Post-merge evidence — 2026-11-16

PR [#231](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/231) merged by squash as `e6b1d564a20b88945dc0277b8db38efcd5834c8e`. Exact-head Verify #4323 / [run 43865438811](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43865438811) and post-merge main Verify #4324 / [run 43865719407](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43865719407) both succeeded: 350 Python, 201 Node and 29 Chromium tests, including the direct-romanization mode-separation browser regression. Pages Deploy #104 / [run 43865719450](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43865719450) also succeeded and deployed commit `e6b1d564`; its built-site Chromium suite passed 29 tests and the deployed-service smoke test passed.

The engineering acceptance is complete for the fail-closed integration guard only. Automatic LOC syllabification remains PARTIAL; no linguistic capability is promoted.

## ALA-LC Notes 8–9 route and evidence boundary — 2026-11-16

A closer reading of the LOC 2012 Notes 8–9 clarifies two different implementation gaps:

- **Note 8:** the current browser Lao-source route preserves Lao numerals as visible passthrough because it is a phonetic output path, not a full ALA-LC source romanizer. The direct ALA-LC mode starts from Latin romanization; its handling of Arabic digits cannot be counted as support for converting Lao numerals ໐–໙ to 0–9. Mark Note 8 PARTIAL for ALA-LC conformance. No runtime change was made because there is no ALA-LC Lao-source romanizer path to extend.
- **Note 9:** no Lao lexical word segmenter or reviewed loanword boundary resolver exists in the current browser parser. It cannot implement the shortest written form that can stand alone as a word, Pali/Sanskrit shortest-form handling, or original-language boundaries for other loanwords without a rights-cleared lexicon and specialist-reviewed policy. Keep PARTIAL/BLOCKED; do not infer boundaries from arbitrary syllable segmentation.

Primary evidence: LOC ALA-LC Lao Romanization Table (2012), Notes 8–9: https://www.loc.gov/catdir/cpso/romanization/lao.pdf. No source lexical boundary or numeral mapping has been invented.

## LaoNLP candidate review for ALA-LC Notes 9–10 — 2026-11-16

Pinned upstream commit: [wannaphong/LaoNLP @ a914f64e38ff24d67d32e37db40dad5c368ea602](https://github.com/wannaphong/LaoNLP/tree/a914f64e38ff24d67d32e37db40dad5c368ea602).

The candidate was inspected at code and data-file level rather than adopted:

- `syllable_tokenize` is a regex model based on Phissamay et al. for orthographic syllabification/line breaking. Its semivowel class includes U+0EBC, but that does not establish phonological source-role overlap or LOC Note 10's coda/onset duplication.
- `word_tokenize` uses PyThaiNLP's Trie and maximum matching. Its `lao_words()` dictionary is the union of four separate sources: `Lao-Dictionary.txt`, `lo_spellcheck_dict.txt`, `lao-wannaphong.txt` and `wiktionary-20210720.txt`. Maximum matching is not the LOC Note 9 shortest-written-form-that-can-stand-alone rule and does not itself implement the Pali/Sanskrit and original-language loanword clauses.
- Per-file licensing is heterogeneous: Lao-Dictionary has a BSD-style notice in its own header; the Google spellcheck list states Apache-2.0; Wiktionary list states CC BY-SA 3.0; the 379-byte Wannaphong supplemental list had no file-specific license notice in the inspected pinned blob. The separate Lao-English CSV has an explicit MIT notice but is not part of `lao_words()`.
- The Lao-Dictionary header says it was created for word wrapping and that compound words have mostly been reduced to their parts. It is not lexical-boundary gold or IPA evidence.

Existing source-registry rows were expanded and separate per-file data/license rows and a methodology claim were added. No package code or data was imported into ClippyFirst. Note 9 remains PARTIAL/BLOCKED; Note 10 automatic source segmentation remains PARTIAL/fail-closed.

### Post-merge evidence — PR #234

PR [#234](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/234) merged as `271bde493c2ee11e50498c06e6c3263f0ea08308`. Exact-head Verify #4330 / [run 43867454851](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43867454851) and post-merge main Verify #4331 / [run 43867656132](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43867656132) both succeeded: 350 Python, 201 Node and 29 Chromium tests, with repository/evidence and IPA-gold schema checks, external-G2P harness syntax/CLI, build, reproducibility and built-page checks. Documentation/source-registry only; no Pages deployment was required.

The source/license review establishes that LaoNLP is a candidate reference, not a LOC Note 9/10 implementation. No runtime dependency or corpus data was imported.
## HVULao_NLP candidate review for ALA-LC Note 9 — 2026-11-16

A second candidate was assessed after the pinned LaoNLP review: **HVULao_NLP v2** (Mendeley DOI `10.17632/5zwym7kwn8.2`, article DOI `10.31449/inf.v49i27.11195`). It is materially stronger than LaoNLP as a source of candidate word boundaries because the paper publishes an explicit annotation guideline and reports native-Lao annotator review plus a senior linguist adjudicator.

### What the published guideline supports

- Annotation unit: word-level minimal orthographic units carrying lexical or grammatical meaning.
- Minimality and consistency: prefer the smallest segmentation consistent across the corpus.
- Context sensitivity: resolve ambiguity from sentence context, not frequency alone.
- Function words and particles are separate; productive morphemes are split when syntactic, but lexicalized forms remain fused.
- Orthographically fused lexicalized compounds remain one token; otherwise segment components. The stated decision test asks whether a component can be modified or replaced independently.
- The paper reports 10,000 training and 1,000 test sentences; trained native annotators reviewed the corpus, a native linguist adjudicated disagreements, and 5% (500 sentences) were double annotated (reported segmentation F1 0.80).

### Why this is still not an LOC Note 9 implementation

The guideline's “minimal orthographic unit” and smallest-consistent-segmentation principles are relevant to LOC's shortest written form that can stand alone as a word. They are not interchangeable: the corpus is a general NLP tokenization convention, and the published guideline does not specify LOC's Pali/Sanskrit shortest-form treatment or original-language boundaries for other loanwords. Its rules for lexicalized compounds, bound morphemes, particles, and named entities may produce decisions that need explicit reconciliation with the LOC romanization convention. Do not use the model's F1 or the corpus's “gold test” label as evidence of LOC conformance or pronunciation accuracy.

### Rights and integration decision

Mendeley Data version 2 lists CC BY 4.0 for the dataset. The journal article's publication page separately states CC BY 3.0 for articles; that licence applies to the article, not automatically to the dataset or its upstream texts. The paper's ethical statement says the source websites explicitly allowed text reuse for research and non-commercial purposes. Table 2 reports seven source domains and aggregate sentence counts, but does not provide item-level sentence-to-URL permission mapping. These are distinct rights scopes: neither the article's CC BY 3.0 nor the dataset's CC BY 4.0 label alone establishes commercial redistribution rights in the underlying government/news/institutional source texts. Require item-level source locators and rights review before importing examples, especially for commercial use. The project therefore records the corpus as a **research candidate only**; no HVULao text, model, or dependency is imported into the runtime or gold corpus.

### Disposition

- LaoNLP remains rejected as a drop-in resolver (maximum-match tokenizer; mixed-license wordlist).
- HVULao_NLP is accepted as a better **comparative segmentation candidate** and future source for an adversarial review set, subject to item-level rights and Lao-specialist review.
- Note 9 remains `PARTIAL / BLOCKED`. Acceptance requires a versioned LOC-specific policy, rights-cleared examples covering native compounds, productive morphology, function words, Pali/Sanskrit and other loans, and adjudicated LOC boundary decisions. Preserve ambiguity where the available evidence does not decide the boundary.

Primary sources: [HVULao_NLP article, Appendix B (segmentation guidelines)](https://www.informatica.si/index.php/informatica/article/download/11195/5975); [Mendeley Data v2](https://data.mendeley.com/datasets/5zwym7kwn8/2); [ALA-LC Lao Romanization Table (2012)](https://www.loc.gov/catdir/cpso/romanization/lao.pdf).
### Additional orthographic evidence for loanword classification

The LDC Language Specific Peculiarities document says that modern Lao spelling conventions distinguish Pali/Sanskrit borrowings from more recent foreign loans: it describes `ຣ` as reintroduced for recent foreign words, while Pali/Sanskrit borrowings use `ລ` in its place. It also warns that foreign-loan spelling remains variable. This supports recording a curated lexeme-origin field; it does **not** justify inferring origin from `ຣ`/`ລ` alone.

The CrossAsia Digital Library of Lao Manuscripts (DLLM) describes a collection-specific cataloguing convention that preserves historical Indic consonant values in some loanword titles (e.g. `ນິພພານ` from Pali *nibbāna*, `ສູຕ` from Sanskrit *sūtra*), but uses modern Lao pronunciations for some commonly used loans (e.g. `ນະຄອນ`, `ທັມມາດ`). This is useful evidence of lexicalization and source-history variation, not a general Lao standard or LOC segmentation gold. CrossAsia carries a copyright notice and no open-data licence was identified; no table or corpus was copied.

**Resolver implication:** any future Note 9 lexeme record needs separately reviewed fields for source-language origin, current Lao lexicalization status, the relevant source-language orthographic division, the LOC romanization unit(s), exact source locator, and reviewer/adjudication provenance. Do not infer Pali/Sanskrit status solely from a grapheme, and do not infer original-language token boundaries from LaoNLP/HVULao segmentation alone.

Sources: [LDC Lao Language Specific Peculiarities, §§3–4](https://catalog.ldc.upenn.edu/docs/LDC2017S08/LSP_203_final.pdf); [CrossAsia DLLM, Lao Orthography and Romanisation](https://digital.crossasia.org/digital-library-of-lao-manuscripts-about-dllm-collection/?lang=en).
## PR #243 merge and verification — 2026-11-16

PR [#243](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/243) merged by squash as `fccff4bae4a4bbc0c7a4d2d9837a874ed72059bd` from exact tested head `6c6d54077361014f8c31d1875cbb8967c5c447bd`. Exact-head Verify #4391 / [run 43930231174 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43930231174) passed 350 Python, 204 Node and 30 Chromium tests; IPA-gold schema, repository/evidence audit, external-G2P syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks passed. Documentation/evidence only; no runtime or deployment files changed. Pages #104 remains the runtime checkpoint.

The available GitHub integration did not expose the push-triggered main workflow run after merge, so post-merge main verification is not claimed. This does not invalidate the successful exact-head run; it is a visibility limitation for the separate push-triggered event.

## ICU Lao word-break baseline against HVULao_NLP v2 — 2026-11-16

This follow-up adds a reproducible, offline exploratory benchmark; it does **not** promote the ICU word-break dictionary or HVULao annotations to ALA-LC Note 9 gold.

### Pinned inputs and provenance

- HVULao_NLP GitHub snapshot: `HaHVU/HVULao_NLP@ec8be4f1a541f3a5c76b4ebda39a9b2795d5c568`.
  - Raw test sentences `Datatest1k/testorgin1000.txt`: Git blob SHA-1 `947448807484bb994877ae5d32cba1cfdd5e2d9b`.
  - Segmented test sentences `Datatest1k/testsegsent_1000.txt`: Git blob SHA-1 `46254839d798fa7140d627fdef440109be9f4285`.
  - Mendeley V2 identifies the dataset as CC BY 4.0. The paper says source texts came from government/news/institutional websites and notes source websites permitted research/non-commercial reuse; per-item source rights must still be checked before redistribution or commercial reuse. No corpus text is copied into this repository.
- ICU Lao word-break dictionary: `unicode-org/icu@bf835bad36a09828051dd8cc6f58bb62bac93fde`, `icu4c/source/data/brkitr/dictionaries/laodict.txt`, Git blob SHA-1 `8eb43185e9ab6d00afe0f80e17891e33af976f06`. It contains 30,550 unique entries (maximum 32 code points) and carries Unicode/IBM notices plus a BSD-style redistribution notice. Its stated purpose is word wrapping, not LOC lexical segmentation.
- Safety/provenance note: the referenced mutable `rober42539/lao-dictionary` repository now displays takeover/defacement content, and its current `LICENSE.txt` content redirects to an unrelated site. Do not fetch from that mutable upstream. The experiment used only the pinned ICU vendor copy with its own embedded notices.

### Exploratory method and result

A local offline harness, `scripts/benchmark_lao_word_boundaries.py`, compares two simple left-to-right greedy prefix strategies using the same ICU word list. Unknown Lao code points fall back one code point. Raw sentences are NFC-normalized and whitespace is removed; only sentence pairs whose resulting character streams exactly match the concatenated segmented tokens are scored. Boundary positions are counted only between adjacent code points in the Lao Unicode block; punctuation and mixed-script boundaries are excluded.

| Measure | Greedy longest prefix | Greedy shortest prefix |
|---|---:|---:|
| Aligned sentence pairs | 839 / 1,000 | 839 / 1,000 |
| Unaligned pairs excluded | 161 | 161 |
| Within-Lao candidate boundary positions | 49,608 | 49,608 |
| True positives | 8,464 | 9,454 |
| False positives | 1,669 | 17,946 |
| False negatives | 1,004 | 14 |
| Precision | 0.8353 | 0.3450 |
| Recall | 0.8940 | 0.9985 |
| Micro F1 | 0.8636 | 0.5129 |

The 161 unaligned sentence pairs were excluded, not silently corrected; their differences were not classified in this experiment. The reported scores are therefore a filtered exploratory comparison, not a corpus-wide result and **not comparable** to the paper's reported 0.75 F1 model score, which uses a different evaluation protocol. The high recall/low precision of the naive shortest-prefix variant shows why LOC's phrase “shortest written form which can stand alone as a word” must not be implemented as a context-free shortest-prefix heuristic.

### Reproducibility and disposition

The script accepts local copies of the three pinned files and can verify their Git blob SHA-1 values. Example:

```bash
python scripts/benchmark_lao_word_boundaries.py \
  --raw /path/to/testorgin1000.txt \
  --segmented /path/to/testsegsent_1000.txt \
  --dictionary /path/to/laodict.txt \
  --raw-blob-sha1 947448807484bb994877ae5d32cba1cfdd5e2d9b \
  --segmented-blob-sha1 46254839d798fa7140d627fdef440109be9f4285 \
  --dictionary-blob-sha1 8eb43185e9ab6d00afe0f80e17891e33af976f06
```

Unit tests cover longest/shortest strategy divergence, exact alignment filtering, line-count rejection and fail-closed hash checks. The script is a research comparator only: no dictionary, corpus text, model or runtime dependency was imported. Note 9 remains `PARTIAL / BLOCKED`; acceptance still requires LOC-specific policy, rights-cleared/source-located examples, and Lao-specialist adjudication of native compounds, productive morphology, Pali/Sanskrit and other loans.

## Correction to ALA-LC Note 10 example attribution — 2026-11-16

The earlier repository wording incorrectly identified `ຄິຼສຕຽນ` as the LOC Note 10 source example and called its browser regression an automatic Note 10 test. This is corrected:

- The preferred LOC 2012 Word source gives `ຄຼິສຕຽນ (khitsatīan)` in Notes 3 and 10. The separately published PDF gives a conflicting example `ຫຼັກສາດ (khitsatān)`; LOC's source-document index explicitly says to copy from Word rather than PDF, so the discrepancy is recorded and the Word source is used for the current-table example. The historical 1997 PDF text layer exposes `khitsatian`, but its Lao glyphs are corrupted in extraction and no exact 1997 script form is asserted.
- The positive/negative unit crosswalk tests now use the preferred Word-source romanization `khitsatīan`, but the source syllable roles are manually supplied. The `ສ` final-`t` / onset-`s` assignment is a synthetic crosswalk fixture, not a claim that the code has parsed the LOC source word.
- The browser test with `ຄິຼສຕຽນ` is retained under an accurate name as a mode-separation test: Lao script entered in Latin romanization mode is withheld. It is not LOC Note 10 evidence.
- Acceptance remains PARTIAL until a Lao specialist confirms the source syllable/role analysis and the upstream Lao parser derives those roles without manual injection. The printed 2012 text-layer form is now identified, but this is not a substitute for linguistic adjudication.

Sources: [LOC ALA-LC Lao table (2012), Notes 3 and 10](https://www.loc.gov/catdir/cpso/romanization/lao.pdf); [LOC ALA-LC Lao table (1997)](https://www.loc.gov/catdir/cpso/romanization/lao-1997.pdf) (image-only in the available text extraction; exact glyph form not asserted).

## LOC source-version authority check — 2026-11-16

The current [LOC ALA-LC Romanization Tables index](https://www.loc.gov/catdir/cpso/roman) lists Lao (2012) as the current table and 1997 only as an earlier version. LOC explicitly says earlier versions are for reference only and are not to be used in current cataloging; it also instructs users to use the source documents rather than PDF versions when copying data. This independently confirms the repository's decision to use the 2012 table as its primary standard and retain the 1997 file only as historical context. Note 9's three-way policy remains explicit in the 2012 source: ordinary Lao forms use the shortest written form that can stand alone; Pali/Sanskrit loans follow that same rule; other loans follow division in their original language. This is a rule-level requirement, not a general instruction to run a generic Lao word segmenter.

Source: [LOC ALA-LC Romanization Tables index](https://www.loc.gov/catdir/cpso/roman); [LOC Lao Romanization Table (2012), Notes 9–10](https://www.loc.gov/catdir/cpso/romanization/lao.pdf).

### Source-document retrieval limitation

LOC's [Source Documents for Romanization Tables](https://www.loc.gov/catdir/cpso/romansource.html) page says the tables are created from Microsoft Word source files and explicitly instructs users to copy from those source documents rather than the PDFs. Its Lao entry links to [lao.doc](https://www.loc.gov/catdir/cpso/romanization/lao.doc). The linked legacy `.doc` file was retrieved with HTTP 200 (`application/msword`) and inspected through a content-aware document reader on 2026-11-17. Its Note 3/10 example is `ຄຼິສຕຽນ (khitsatīan)`, which differs from the PDF's `ຫຼັກສາດ (khitsatān)`. LOC explicitly instructs users to copy from Word rather than PDF, so this audit uses the Word example and preserves the published PDF discrepancy.

## Lao national / UN romanization status evidence — updated 2026-11-16

A newer primary source refines the chronology but does not justify importing a Lao-specific RTGS layer:

- The current [UNGEGN Romanization Systems index](https://unstats.un.org/unsd/ungegn/romanization/) lists Lao version 4.0 dated 2013-09-24 under "Other languages/scripts", not among the 30 systems recommended by the United Nations. The index is the current UN status listing; it is not a complete national language policy.
- The 2023 UNGEGN Working Group minutes record that the Lao National Geographic Department had drafted Toponymic Guidelines in two parts (general writing systems and romanization), sought ministry feedback, and planned to submit a final draft to the government for approval.
- The 2025 UNGEGN Working Group report (GEGN.2/2025/26/CRP.26, dated 13 January 2025) says that, as of July 2024, Lao PDR was finalizing a draft of toponymy guidelines; the Working Group hoped the romanization system would be put forward for consideration at the 2027 UNGEGN Session. This is a reported expectation, not evidence that the draft was finalized, submitted, approved, or implemented.
- The 2025 UNGEGN country-name document still identifies BGN/PCGN 1966 as the romanization used for the Lao PDR formal name. That is evidence for this UN country-name record only; it is not a complete Lao transcription standard.
- The 2023 UK Government / PCGN Laos Toponymic Factfile states that no official romanization system was in use in Laos for current Lao orthography at that time and that PCGN continued using BGN/PCGN 1966 while work with Lao authorities proceeded. Keep this statement explicitly time-bounded to 2023.

The registry records these scopes as `SRC-UNGEGN-APPROVAL-PROCESS-2026`, `SRC-UNGEGN-ROMANIZATION-STATUS`, `SRC-UNGEGN-LAO-DRAFT-2023`, `SRC-UNGEGN-LAO-MINUTES-2023`, `SRC-UNGEGN-LAO-STATUS-2025`, `SRC-UNGEGN-LAO-NAME-2025` and `SRC-PCGN-LAO-FACTFILE-2023`, with synthesis claim `CLM-LAO-ROMANIZATION-STATUS-2025`. **Disposition remains BLOCKED:** no complete authoritative Lao-specific RTGS table or approved Ukrainian target adaptation has been established. Do not substitute Thai RTGS or treat BGN/PCGN 1966 as a universal phonetic transcription.
The current UNGEGN approval-process document (WG-reviewed 28 May 2026) clarifies the acceptance path for geographical-name romanization: national development, local implementation, formal submission, WG-RS review, plenary presentation and adoption. A proposal is expected to include a conversion table and evidence of national implementation. This defines future evidence needed; it does not establish that Lao has progressed beyond the 2025 status report.


## LOC Word source retrieval recheck — 2026-11-16

The official [LOC source-document index](https://www.loc.gov/catdir/cpso/romansource.html) identifies the Lao Word file and explicitly instructs users to use Word rather than PDF when copying table data. The linked `lao.doc` was retrieved with HTTP 200 (`application/msword`) and inspected on 2026-11-17. It gives `ຄຼິສຕຽນ (khitsatīan)` in Notes 3 and 10. The PDF differs (`ຫຼັກສາດ (khitsatān)`); preserve this source discrepancy.

**Acceptance to unblock:** obtain the exact official LOC `lao.doc` file through a compatible document-capable environment or user-supplied copy, inspect its table/notes, and reconcile any differences before changing source-derived claims or fixtures. No linguistic inference or runtime change is justified by the failed retrieval.


## Ueda (1994) full-text phonology review — 2026-11-16

A full-text review of Reiko Ueda, *The Phonology of the Vientiane Dialect of Lao* (1994), adds a material constraint for source-side analysis. Ueda explicitly reports no phonological consonant clusters in the described Vientiane spoken dialect despite consonant-letter sequences in Lao spelling. In the examples in §2.3 (printed pp. 100–101), written `w` can correspond to spoken /ua/ or have no independent spoken segment. The paper also lists positional onset and coda inventories (§§2.1, 3.2), with some consonants occurring in both positions.

This is **phonological evidence**, not an orthographic segmentation specification. It does not provide a deterministic grapheme-to-syllable algorithm and does not verify LOC Note 10's exact Lao glyph sequence. It reinforces the requirement that written grapheme grouping and spoken onset/rhyme/coda analysis remain separate, typed stages. A parser must not infer a spoken onset cluster from adjacent consonant letters alone.

Ueda also describes exceptional non-final light syllables and a five-tone baseline alongside a disputed six-tone analysis. These observations are scoped to the described central Vientiane variety and one informant; they must not be generalized to all Lao dialects or used to silently normalize five- and six-tone references.

**Disposition:** improve the evidence basis for the Vientiane phonological layer; keep orthographic syllabification and LOC Note 10 automatic role derivation `PARTIAL/TODO`. No runtime rule, corpus item, or IPA gold example is added.

Source: Ueda (1994), DOI [10.11435/GENGO1939.1994.106_95](https://doi.org/10.11435/GENGO1939.1994.106_95); full-text reading notes preserved in [the Undermind research workspace](https://app.undermind.ai/projects/5603c8d1-3260-4f39-b0d5-8fd6ffa3a081?path=/research/orthographic-parsing-boundaries-2026-11-16.md).


## Historical Lao orthographic syllable grammar — Berment (2004) and Del Vigna & Berment (2003) — 2026-11-17

A direct Lao orthographic grammar and ambiguity model have now been located in the full text of Berment's 2004 thesis, *Méthodes pour informatiser des langues et des groupes de langues « peu dotées »* (Part III §§III.2.3–III.2.6; Annexes A.11/A.14), and Del Vigna & Berment (2003), *Ambiguïtés irréductibles dans les monoïdes de mots*. Sources/claims are registered as `SRC-BERMENT-THESIS-2004`, `SRC-DEL-VIGNA-BERMENT-2003`, `CLM-LAO-HISTORICAL-ORTHOGRAPHIC-SYLLABLE-GRAMMAR`, `CLM-LAO-SYLLABLE-AMBIGUITY-LATTICE`, `CLM-LAO-HISTORICAL-GRAMMAR-VALIDATION-LIMITS`, and `CLM-LAO-IRREDUCIBLE-SYLLABLE-AMBIGUITIES`.

Berment describes a historical non-recursive grammar over initial consonants/consonant groups, positional multi-grapheme vowel patterns, optional accent and restricted codas. Vowel components may occur before, after, above or below the initial consonant; they cannot safely be treated as a contiguous vowel token. The thesis reports 56,670 generated candidate syllables and a 33-state/480-transition minimal automaton (historical experiment attributed to Yeu 2003). It explicitly warns that the grammar admits theoretical unattested strings (e.g. `ມວອ`) and simplifies accent placement. OCR loses some Lao terminal glyphs in the printed grammar; exact productions must be transcribed from page images/Prolog appendix before any implementation.

The thesis models segmentation as a graph: candidate syllables are edges between text offsets; complete segmentations are paths; candidates that cannot belong to a complete path are dead branches; common convergence points delimit ambiguous regions. Its longest-candidate selection is a local text-selection/UI heuristic with user cycling, not a validated global linguistic resolver. Del Vigna & Berment's separate 2003 formal-language study reports a historical Lao dictionary/automaton and a finite language of irreducible ambiguous strings. Its counts are independent of the thesis's 56,670 grammar-generated strings and are not repository benchmarks.

**Disposition:** this closes the research question “does a historical explicit Lao orthographic grammar exist?” but not current parser acceptance. Keep the runtime unchanged. Candidate next engineering stage: transcribe the exact historical productions and Prolog appendix into a review artifact; reconcile Unicode 18/Lew 2014/current spelling and tone rules; build a candidate-lattice prototype with dead-branch pruning and explicit ambiguity output; validate against attested/adversarial examples and Lao-specialist review. Do not copy the historical code absent a license. Ueda's phonological evidence remains a separate downstream layer: written adjacency is not an IPA cluster. LOC Note 10's exact glyph sequence and automatic double-role derivation remain unresolved.

Full research note: [Undermind workspace](https://app.undermind.ai/projects/5603c8d1-3260-4f39-b0d5-8fd6ffa3a081?path=/research/orthographic-parsing-boundaries-2026-11-16.md). Primary sources: [Berment 2004 thesis PDF](https://www.tagmatica.fr/doc/these-vincent-berment.pdf); [Del Vigna & Berment 2003](https://doi.org/10.36045/bbms/1074791326).


## Modern Lao grapheme-structure evidence — ICANN RZ-LGR-6 (2025), Lao Generation Panel (2017), and W3C Group Note Draft (2026-03-20)

### Primary evidence

The Lao Script Generation Panel's *Proposal for a Lao Script Root Zone LGR*, version 3.1 (31 January 2017), describes a grapheme-cluster template `C V (T) (Cf) (S+)` and makes clear that the vowel is phonologically after the onset even when its written components surround the main consonant. It specifies the main consonant cluster, optional final consonant, vowel-before/after/above/below categories, tone-mark placement, and special diphthong constructions. The proposal's normal-syllable onset description includes restricted two-consonant sequences, a special three-consonant sequence `ຫງວ`, and U+0EBC after a consonant; it separately allows arbitrary consonant sequences for acronyms. It lists a restricted coda set and at most one final consonant for the normal syllable model.

The 2017 proposal explicitly says its root-zone label rules simplify spelling constraints: allowed consonant combinations are listed but not coded, and some diphthong restrictions are not implemented to avoid complexity. Therefore the formal template and WLE rules are **not a complete Lao syllable grammar or spell-checker**. They are a strong source for positional grapheme facts and scoped structural checks, not for rejecting every nonstandard string or deciding a lexical syllable boundary.

The current ICANN Root Zone LGR-6 Lao page (23 September 2025) is scoped to DNS root-zone labels and Unicode 16.0; it reports 51 code points plus one sequence. This is a maintained technical repertoire/ruleset, not an exhaustive inventory for arbitrary Lao text. The 2017 proposal remains its explanatory source.

The W3C Lao Layout Requirements Group Note Draft (20 March 2026) describes Lao as an alphabet with explicit vowels; says there are no conjuncts except the subjoined-consonant case with HA; distinguishes spacing pre-base vowel glyphs from combining above/below vowel marks; and notes multipart vowels can involve up to four glyphs plus a tone mark around the base consonant on up to three sides. **The W3C document is a Group Note Draft and explicitly not endorsed by W3C or its Members**, so use it as current technical layout guidance, not a normative spelling standard.

### Structural facts suitable for candidate-parser invariants

- U+0EBC LAO SEMIVOWEL SIGN LO follows a consonant in the ICANN ordering rules; do not treat it as an independent consonant letter.
- A vowel-before character precedes the main consonant cluster; above/below vowel marks follow the main consonant; a vowel-after component follows the main consonant, a tone mark or an above-vowel according to the scoped WLE rules.
- A tone mark is optional and the 2017 proposal's syllable model permits at most one; it follows the main consonant or an above/below vowel. This is a model constraint, not a dialect-independent phonological tone parser.
- The proposal's coda inventory and maximum-one-coda rule are useful candidate constraints, but acronym, foreign-word, Pali/Sanskrit and historical spellings need separate handling.
- U+0EC6 LAO KO LA is a repetition sign, not a phonological segment. ICANN's root-zone policy limits its position/count for domain labels; the language itself can use it elsewhere in a sequence, as the proposal explicitly notes.
- The W3C draft and Unicode 18.0 confirm that visual/typing order, Unicode storage order and phonological order must not be conflated. Pre-base vowels are spacing characters; only above/below components are combining marks in the described model.

### Reconciliation with Berment (2004) and architecture

Berment supplies a historical generative syllable grammar and candidate segmentation graph, but its exact production listing is partly lost in OCR and its grammar accepts unattested forms and simplifies accent placement. The 2017 Lao Generation Panel proposal and 2025 ICANN LGR provide a much more recent, code-point-explicit description of grapheme placement and context order, but deliberately omit important spelling constraints. The 2026 W3C draft adds typographic/encoding distinctions but is not an endorsed linguistic standard. These sources are complementary, not interchangeable.

**Architecture decision:** implement a low-level grapheme-structure analyzer first (code-point classes, pre-base/above/below/after placement, U+0EBC order, tone-mark placement, sign handling), then a separately versioned candidate syllable grammar/lattice. Keep candidate recognition distinct from lexical well-formedness and spoken phonology. Never let the ICANN acronym-permissive `Consonant1+` simplification become a general onset grammar; never treat W3C's draft statements as final linguistic adjudication. Ueda's dialect-scoped phonology remains downstream of orthographic candidates.

### Status

- MODERN_LAO_GRAPHEME_PLACEMENT_EVIDENCE: DONE_VERIFIED (scoped source review).
- ICANN_ROOT_ZONE_RULESET_AS_GENERAL_SPELLCHECKER: DEFERRED / not applicable; explicit scope mismatch.
- LOW_LEVEL_LAO_GRAPHEME_STRUCTURE_ANALYZER: TODO — acceptance: code-point class inventory; order/context tests for pre-base, above/below, tone, U+0EBC, U+0ECC and U+0EC6; malformed/reordered mark fixtures; exact Unicode 16/18 reconciliation.
- CURRENT_LAO_SYLLABLE_GRAMMAR: PARTIAL / TODO — acceptance: combine source-backed grapheme constraints with lexically/linguistically reviewed spelling rules, separate acronym/loan/Indic profiles, candidate lattice, ambiguity preservation and specialist review.

Registry additions: `SRC-ICANN-LAO-PROPOSAL-2017`, `SRC-ICANN-RZ-LGR6-LAO-2025`; claims `CLM-LAO-ICANN-WLE-ORDERING`, `CLM-LAO-ICANN-LGR-NOT-SPELLCHECKER`, `CLM-LAO-ICANN-ROOT-ZONE-SCOPE`, `CLM-LAO-W3C-DRAFT-ORTHOGRAPHY-STRUCTURE`.

Sources: [ICANN Lao proposal v3.1 (2017)](https://www.icann.org/en/system/files/files/proposal-lao-lgr-31jan17-en.pdf); [ICANN RZ-LGR-6 Lao (2025)](https://www.icann.org/sites/default/files/packages/lgr/rz-lgr-6-lao-script-23sep25-en.htm); [W3C Lao Layout Requirements, Group Note Draft (2026-03-20)](https://www.w3.org/TR/2026/DNOTE-laoo-lreq-20260320/); [Unicode 18.0 Chapter 16](https://www.unicode.org/versions/Unicode18.0.0/core-spec/chapter-16/).


## Modern Lao syllable vs word segmentation — Ishida (2026-04-28) — 2026-11-17

Richard Ishida's *Lao Orthography Notes* (updated 28 April 2026) provides the most directly useful current descriptive account located so far: [https://r12a.github.io/scripts/laoo/lo.html](https://r12a.github.io/scripts/laoo/lo.html). It is linked by the W3C Lao Layout Requirements resource and describes modern printed Lao and Unicode use.

### Findings that refine the earlier Berment/ICANN model

- Lao is alphabetic and writes vowels explicitly. Ishida says this makes individual syllable boundaries comparatively straightforward to detect because the syllable-final consonant inventory is restricted; he lists nine coda letters: `ບ, ດ, ກ, ມ, ນ, ຣ, ງ, ວ, ຍ`. The rhyme `-am` can also be represented by U+0EB3. Coda sound can differ from the same letter's onset value.
- This is **syllable segmentation, not lexical word segmentation**. Lao spaces mark phrases/sentences. Multi-syllabic lexical words such as `ປະເທດ` may need a dictionary to keep their syllables together for word-based selection; ZWSP U+200B may be supplied as an explicit boundary by source text/software.
- Modern Lao has one audible onset-cluster type in the description: an onset consonant labialized by following `ວ`. Separate written high-class onsets use `ຫ` plus a following consonant, including `ຫຼ` with subjoined U+0EBC. Both classes must be kept together as syllable onsets. Ishida explicitly leaves “What about kw etc?” as an open question; do not infer a universal rule for every visually similar sequence.
- Pre-base vowel letters are stored before the **entire onset**, not merely before the consonant that carries the phonological vowel. Tone marks and post-base vowel signs attach to the latter. The source examples `ໃຫຍ່` and `ເຫຼືອງ` make this distinction concrete.
- Unicode grapheme clusters are not Lao syllables. Combining marks attach to a base consonant, but pre-base and post-base spacing components and other consonants in composite vowels can form parts of the same orthographic syllable. Do not use generic grapheme-cluster boundaries as syllable boundaries.
- Ishida distinguishes modern coda phonology from the broader ICANN root-zone final-consonant repertoire. The nine-letter coda list should not be overwritten by the ICANN list of allowed domain-label characters.

### Regression coverage added

Added source-backed syllable-boundary cases to `tests/test_multisyllable_segmentation.py`:
- `ໃຫຍ່` remains one syllable with pre-base vowel before the high-class onset digraph;
- `ເຫຼືອງ` remains one syllable with pre-base vowel before HA + subjoined LO;
- `ປະເທດ` segments as `ປະ | ເທດ`, while the test explicitly does not claim a lexical word boundary.

These are orthographic segmentation controls, **not IPA/pronunciation gold**. Verify #4517 / run 43971181584 on test commit `cb7950065c310c9376f7075fe7688059475c0a19` has passed Python tests, evidence audit, external-G2P, browser engine, build and generated-data reproducibility; Chromium UI and built-page checks were still running at the last poll.

### Architecture/status refinement

Berment's candidate graph and irreducible-ambiguity work remain valuable for genuinely ambiguous or lexically segmented input, but should not be made the default assumption that ordinary Lao syllable boundaries are generally irreducible. Baseline should be a deterministic, source-backed orthographic syllable parser using explicit vowels, restricted codas and the two onset families; preserve an ambiguity/candidate path for cases where multiple parses remain. Word segmentation is a separate dictionary-backed layer and is not implied by syllable segmentation.

- MODERN_LAO_SYLLABLE_BOUNDARY_EVIDENCE: DONE_VERIFIED (source review).
- ISHIDA_EXAMPLE_REGRESSIONS: PARTIAL pending full exact-head CI; Python step passed on test commit.
- GENERAL_WORD_SEGMENTATION: PARTIAL / TODO — dictionary or explicit ZWSP required for lexical word boundaries; choose dictionaries by language, not merely by script.
- Coda inventory reconciliation: TODO — distinguish modern phonological coda inventory from ICANN DNS repertoire, Indic/loanword extensions and historical spellings.

Registry: `SRC-ISHIDA-ORTHO-2026`; claims `CLM-LAO-ISHIDA-EXPLICIT-VOWELS-SYLLABLE-BOUNDARIES`, `CLM-LAO-ISHIDA-ONSET-CLUSTER-PROFILE`, `CLM-LAO-ISHIDA-PREBASE-ONSET-ANCHOR`, `CLM-LAO-UNICODE-GRAPHEME-IS-NOT-SYLLABLE`, `CLM-LAO-ISHIDA-CODA-INVENTORY`.


## Ishida coda inventory reconciliation — 2026-11-17

A closer line-by-line reading of [Ishida, Lao Orthography Notes (28 April 2026)](https://r12a.github.io/scripts/laoo/lo.html) found an **internal source discrepancy**:

- The explicit final-position list at lines 816–821 enumerates nine graphemes: ບ ດ ກ ມ ນ ຣ ງ ວ ຍ; it then notes U+0EB3 as a special -am rhyme.
- The consonant-class chart at lines 727–729 also places ຢ in its coda row, making ten chart entries.
- The IPA correspondence table at lines 1038–1042 maps onset /j/ to ຢ, but identifies the final /j/ coda as ຍ. It does not provide a final value for ຢ.

**Disposition:** retain the nine explicitly enumerated spellings and their existing source-aware mappings (ບ→p, ດ→t, ກ→k, ມ→m, ນ→n, ຣ→n, ງ→ŋ, ວ→w, ຍ→j). Do not add ຢ as a coda until the discrepancy is resolved by an independent source or Lao specialist. The parser already fails closed for ກາຢ; a regression now protects that boundary.

This also clarifies the separate data/lao/codas.csv layer: it is a phoneme-category table (including /ʔ/ and analysis-dependent /l,r/), not an orthographic grapheme lookup. The parser's actual final-grapheme recognition uses consonants.csv and its ipa_final field. The phonological /ʔ/ may occur after short vowels, but this source note does not establish a universal orthographic grapheme mapping or whether the runtime should emit it categorically; keep that realization question evidence-limited. U+0EB3 remains a special rhyme representation containing /m/, not an ordinary final consonant grapheme.

**Task ledger:** nine listed coda spellings and current mappings = DONE_VERIFIED as source-to-registry consistency (not independent IPA gold); ຢ coda = BLOCKED / source-internal conflict; implicit /ʔ/ realization = PARTIAL / needs dialect-specific phonetic adjudication; abstract codas.csv semantics = PARTIAL / not an orthographic recognizer. No runtime mappings were broadened.

Registry: SRC-ISHIDA-ORTHO-2026; claims CLM-LAO-ISHIDA-CODA-INVENTORY and CLM-LAO-ISHIDA-CODA-CHART-CONFLICT.

## LOC Note 10 — official Word-source verification (2026-11-17)

The official Library of Congress [Source Documents for Romanization Tables](https://www.loc.gov/catdir/cpso/romansource.html) index links the Lao Word source at [lao.doc](https://www.loc.gov/catdir/cpso/romanization/lao.doc) and explicitly instructs users to use Word sources rather than PDFs when copying table data. The .doc endpoint was retrieved successfully (HTTP 200, application/msword) and its document text inspected on 2026-11-17.

The preferred Word source gives the exact Note 3 and Note 10 example **ຄຼິສຕຽນ (khitsatīan)**. Note 3 identifies ຼ as the combining form of ລ and says it is not romanized except when subscript to ຫ; in this example it is not romanized. Note 10 repeats the same form and states that one consonant can serve as coda of one syllable and onset of the next, so it is romanized twice. Cross-referencing Note 1, ສ has initial s and final loanword (t), explaining the t + s sequence. The published PDF instead gives **ຫຼັກສາດ (khitsatān)** in its Note 3/10 text; LOC's source-document index says to use Word, so the mismatch is recorded.

This resolves the preferred LOC source example but does not erase the published PDF discrepancy. It does **not** establish automatic source-script syllabification in ClippyFirst: current positive/negative fixtures still supply the ສ coda/onset roles manually. The browser test containing ຄິຼສຕຽນ remains only a Latin-mode separation test and is not the LOC example; the exact source spelling is ຄຼິສຕຽນ.

**Disposition:** exact Note 10 source example = DONE_VERIFIED; source-role crosswalk fixture = DONE_VERIFIED (manual roles only); automatic Lao source parsing and full Note 10 conformance = PARTIAL/BLOCKED pending an independently reviewed orthographic syllabifier and Lao-specialist adjudication. No runtime phonological rule or IPA gold is inferred.

## Historical LOC 1997 Note 10 example — edition distinction (2026-11-17)

The official LOC 1997 PDF's text extraction exposes the historical romanized Note 3/10 example **khitsatian**. Its Lao-script glyphs are corrupted in extraction and were not independently verified from a page image; no exact historical Lao spelling is asserted.

The current 2012 Word source gives **ຄຼິສຕຽນ (khitsatīan)**. The 1997 PDF text layer gives **khitsatian**, but the source-script glyphs cannot be certified from the extracted text. The 2012 Word-source example is the current-table source for the project's ALA-LC profile. Neither example by itself demonstrates automatic source-role derivation in ClippyFirst.

Registry: expanded SRC-ALA-LC-LAO-1997 with the inspected historical form and added CLM-LAO-ALA-LC-NOTE10-HISTORICAL-1997.