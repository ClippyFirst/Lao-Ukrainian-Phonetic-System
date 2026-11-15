# Direct Lao romanization input — implementation audit (2026-11-15)

## Summary

A direct Latin-script input route has been added to the existing Lao → Ukrainian service. Before this change, the UI accepted Lao Unicode only; “За романізацією” generated a CLDR Lao-Latin form internally and cross-checked it against the Lao source. Users could not paste a romanized Lao string as the source input.

**Base main:** bd16bf6eef98ac364d4bde8226187ab2c71d7fb9  
**Working branch:** feat/romanization-input-to-ukrainian-20261115  
**Repository:** https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System

## Changes

- Separate input mode for Lao script vs romanized Latin text.
- Explicit profile selector for automatic, BGN/PCGN 1966 / CLDR Lao-Latin, and bounded ALA-LC 2012 normalization.
- Existing onset/nucleus/coda parser reused for standalone romanization.
- ALA-LC subset normalizes macron vowels, selected vowel symbols/diphthongs, ny palatal-nasal spelling and final s stop coda.
- Unsupported/ambiguous strings remain visible as ⟦…⟧; no IPA is invented from romanization-only input.
- Direct input mode hides the IPA panel and states that tone/length distinctions lost in romanization cannot be recovered.
- Added unit/static/browser tests and updated README, methodology, matrix, source registry and master handoff.

## Evidence and standards

- Library of Congress ALA-LC Lao Romanization Table (2012) supplies the ALA-LC consonant and vowel correspondences; registered as SRC-ALA-LC-LAO-2012.
- LDC Language Specific Peculiarities Document for Lao, section 5, lists BGN/PCGN, RTGS and ALA-LC among schemes used for Lao. It also distinguishes ALA-LC from Appen Butler Hill's separate reversible ASCII encoding.
- PCGN Laos Toponymic Factfile (2023) says there is no official romanization system currently in use in Laos and describes continued PCGN use of BGN/PCGN 1966.
- RTGS is not silently treated as the current BGN/PCGN route. A complete Lao-specific RTGS adaptation table was not established in the inspected primary material, so that profile remains blocked.
- ALA-LC support is a bounded normalization subset, not a claim of complete ALA-LC compliance.

## Task ledger

| Task | Status | Acceptance evidence |
|---|---|---|
| Direct romanization input control and UI state | DONE_IMPLEMENTED | index.html, web/app.js, web/styles.css |
| Standalone BGN/PCGN syllable conversion | DONE_IMPLEMENTED | web/romanization-syllable-engine.js; unit/browser fixtures |
| Bounded ALA-LC 2012 normalization | PARTIAL | macron, vowel, palatal nasal and final-s fixtures; contextual cases still missing |
| Auto profile detection | PARTIAL | heuristic and basic fixture; no broad real-world corpus |
| Preserve ambiguous and unsupported text | DONE_IMPLEMENTED | parser emits visible unresolved brackets and PARTIAL status |
| Prevent invented IPA from romanization | DONE_IMPLEMENTED | IPA panel hidden in direct input mode; no phonetic engine call |
| RTGS-for-Lao | BLOCKED | needs a stable Lao-specific adaptation table and reviewed examples |
| Informal/French-style/Karaoke variants | DEFERRED | conventions vary; define scope and evidence before implementation |
| Exact-head CI and release checks | TODO | awaiting PR workflow result |
| Independent linguistic accuracy validation | BLOCKED | needs rights-cleared, expert-adjudicated reference examples and Lao specialist review |

## Verification

At audit creation, the implementation and tests are committed to the working branch, but no exact-head CI result is yet available. Do not mark the branch release-ready until the PR Verify workflow has completed successfully. Local clone/build execution was not available through the current GitHub-only editing session.

## Readiness

**Partial prototype / engineering verification pending.** The new direct-input route is implemented for the BGN/PCGN-derived profile and a bounded ALA-LC subset. It is not yet a universal Lao romanization converter and has no independent expert accuracy measurement.
