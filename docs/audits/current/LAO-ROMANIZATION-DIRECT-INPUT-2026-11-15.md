# Direct Lao romanization input — implementation audit (2026-11-15)

## Summary

A direct Latin-script input route has been added to the existing Lao → Ukrainian service. Before this change, the UI accepted Lao Unicode only; “За романізацією” generated a CLDR Lao-Latin form internally and cross-checked it against the Lao source. Users could not paste a romanized Lao string as the source input.

**Base main:** bd16bf6eef98ac364d4bde8226187ab2c71d7fb9  
**Working branch:** feat/romanization-input-to-ukrainian-20261115  
**Tested implementation head:** 94750318c83d973b7ae1a7bcd562635a78050b8f  
**Pull request:** #172 — https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/172

## Implementation

- Separate input mode for Lao script vs romanized Latin text.
- Explicit profile selector for automatic, BGN/PCGN 1966 / CLDR Lao-Latin, and bounded ALA-LC 2012 normalization.
- Existing onset/nucleus/coda parser reused for standalone romanization.
- Strict BGN/PCGN direct-input mode enforces note 4: an onsetless syllable inside a word must be hyphenated. The official Viangchan example is supported.
- ALA-LC subset normalizes macron vowels, short/long e, selected vowel symbols/diphthongs, ny palatal-nasal spelling, final s as t, and parenthesized final r/l as n for loanword cases.
- Unsupported/ambiguous strings remain visible as ⟦…⟧; no IPA is invented from romanization-only input.
- Direct input mode hides the IPA panel and states that tone/length distinctions lost in romanization cannot be recovered.
- Added unit, static UI and browser tests and updated README, methodology, matrix, source registry and canonical handoff.

## Evidence and standards

- Library of Congress ALA-LC Lao Romanization Table (2012) supplies ALA-LC consonant and vowel correspondences; registered as SRC-ALA-LC-LAO-2012.
- LDC Language Specific Peculiarities Document for Lao, section 5, lists BGN/PCGN, RTGS and ALA-LC among schemes used for Lao. It distinguishes ALA-LC from Appen Butler Hill's separate reversible ASCII encoding.
- PCGN Laos Toponymic Factfile (2023) says there is no official romanization system currently in use in Laos and describes continued PCGN use of BGN/PCGN 1966; its Viangchan example grounds the direct-input fixture.
- RTGS is not silently treated as the BGN/PCGN route. A complete Lao-specific RTGS adaptation table was not established in the inspected primary material, so that profile remains blocked.
- ALA-LC support is a bounded normalization subset, not a claim of complete ALA-LC compliance.

## Task ledger

| Task | Status | Acceptance evidence |
|---|---|---|
| Direct romanization input control and UI state | DONE_VERIFIED | Exact-head Chromium workflow passed |
| Standalone BGN/PCGN syllable conversion | DONE_VERIFIED | Unit and browser fixtures, including Viangchan |
| Bounded ALA-LC 2012 normalization | PARTIAL | Tested macron, vowel, palatal nasal, s/r/l coda subset; contextual cases remain missing |
| Auto profile detection | PARTIAL | Heuristic fixture; no broad real-world corpus |
| Preserve ambiguous and unsupported text | DONE_VERIFIED | Parser emits visible unresolved brackets and PARTIAL status |
| Prevent invented IPA from romanization | DONE_VERIFIED | IPA panel hidden in direct input mode; no phonetic engine call |
| RTGS-for-Lao | BLOCKED | Needs a stable Lao-specific adaptation table and reviewed examples |
| Informal/French-style/Karaoke variants | DEFERRED | Conventions vary; define scope and evidence before implementation |
| Exact-head CI | DONE_VERIFIED | Verify #4054 / run 43696628872 SUCCESS |
| Independent linguistic accuracy validation | BLOCKED | Needs rights-cleared, expert-adjudicated reference examples and Lao specialist review |
| Manual physical-device and screen-reader QA | BLOCKED | Human review remains outstanding |

## Verification

Exact-head Verify #4054, run 43696628872, on tested implementation head 94750318c83d973b7ae1a7bcd562635a78050b8f: **SUCCESS**.

- Python: 350 passed.
- Node: 174 passed, 0 failed.
- Chromium browser: 27 passed.
- IPA gold corpus schema, repository data/evidence audit, external-G2P syntax/CLI, locked dependency install, build, generated-data reproducibility, built-page and relative-asset checks all passed.

A local clone attempt failed because the execution environment could not resolve github.com. No local test execution is claimed.

## Readiness

**Engineering-verified partial prototype, not release-ready as a universal romanization converter.** Direct input works for the tested BGN/PCGN route and a bounded ALA-LC subset. Independent IPA gold remains empty; RTGS, informal variants, specialist review and manual accessibility QA remain outstanding.
