# Direct Lao romanization input — implementation audit (2026-11-15)

## Summary

A direct Latin-script input route is present in the Lao → Ukrainian service. A follow-up audit corrected the bounded ALA-LC 2012 normalizer against the complete Library of Congress table text and notes.

**Base main:** 5717c2fd95c467c48b3909c86252fba5deca0695  
**Working branch:** fix/ala-lc-2012-conformance-20261115  
**Verified code/documentation head before this audit update:** 2ad9c51adf12137fc7132d8a2c490645f7f88557  
**PR:** pending creation after the final documentation commit's exact-head CI.

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
| Exact-head CI before this audit update | DONE_VERIFIED | Verify #4078 / run 43697698402 SUCCESS |
| Independent linguistic accuracy validation | BLOCKED | Needs rights-cleared, expert-adjudicated reference examples and Lao specialist review |
| Manual physical-device and screen-reader QA | BLOCKED | Human review remains outstanding |

## Verification

GitHub Actions Verify #4078, run 43697698402, on branch head 2ad9c51adf12137fc7132d8a2c490645f7f88557: **SUCCESS**.

- Python: 350 passed.
- Node: 182 passed, 0 failed.
- Chromium browser: 28 passed.
- IPA-gold schema validation, repository data/evidence audit, external-G2P syntax/CLI, locked dependency install, build, generated-data reproducibility, built-page and relative-asset checks all passed.

A local clone attempt failed because the execution environment could not resolve github.com. No local test execution is claimed.

## Readiness

**Engineering-verified partial prototype, not release-ready as a universal romanization converter.** BGN/PCGN direct input is tested; the ALA-LC subset now follows the actual LOC 2012 vowel and position spellings more accurately. Full ALA-LC context, RTGS, informal variants, independent gold, specialist review and manual accessibility QA remain outstanding.
