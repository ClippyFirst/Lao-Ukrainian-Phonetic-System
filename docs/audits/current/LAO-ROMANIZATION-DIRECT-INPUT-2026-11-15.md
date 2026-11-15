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
