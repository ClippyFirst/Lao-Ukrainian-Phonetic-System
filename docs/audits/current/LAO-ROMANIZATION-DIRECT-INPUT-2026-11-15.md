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
