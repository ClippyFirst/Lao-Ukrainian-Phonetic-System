# Current exact-head continuation — 2026-11-10 (authoritative addendum)

**Repository:** `ClippyFirst/Lao-Ukrainian-Phonetic-System`.  
**Starting main SHA:** `0a91bb62d48a6110d5129460fae4efee580863f2`.  
**Implementation commit verified:** `8c7fffe99746e21769ee40e92818f5e10fa5081c`.  
**Starting-main Verify:** [#42776630426 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42776630426). All listed jobs/steps completed successfully: gold-corpus structure, repository data/evidence audit, Python, external-G2P syntax/CLI, locked browser dependencies, browser engine, browser-local inference runtime install, static build, generated-data reproducibility, real Chromium UI, built pages and relative assets.

This addendum supersedes older statements below wherever they conflict with the 2026-11-10 mainline state or the fallback contract.

## Grapheme fallback: actual behavior and documentation correction

The user requirement is that valid Lao input must not disappear merely because structural segmentation or phonological confirmation fails. The primary hybrid must still return a practical Ukrainian-side rendering, while the details explicitly disclose low confidence.

The existing mainline engine already satisfies the core typed architecture:

1. The full path remains Lao orthography → structural/phonological analysis → typed IPA → Ukrainian target adapter.
2. On unresolved structures, registered grapheme-position hints are wrapped in a typed `PROVISIONAL` `PhoneticResult`; unresolved source positions receive explicit unknown segments.
3. The same target adapter maps the known provisional IPA runs and renders unknown segments as `?`. It does not read Lao graphemes directly.
4. Confidence and provenance remain provisional; this fallback is not promoted to supported IPA and does not count as accepted IPA coverage or accuracy.
5. Tone is not inferred by this fallback. Romanization remains an independent orthographic route, not a fallback for uncertain IPA.
6. Frozen compatibility profiles retain their prior abstention behavior; full-coverage provisional rendering belongs to the primary hybrid.

**Documentation defect found:** the older `docs/lao-grapheme-ipa-preview.md` said the preview was never sent to the Ukrainian adapter and that Ukrainian output was withheld. That statement was stale and contradicted the actual Python/browser engine and the master handoff. It is replaced by the typed provisional-adapter contract.

## User-facing confidence presentation

The browser detail panel and text CLI now explicitly disclose:
- low confidence / provisional reading;
- the Ukrainian output actually produced;
- unresolved graphemes or positions and visible `?` markers;
- the fact that tone was not inferred.

The browser regression asserts both the browser-native engine output and the rendered UI output `кал?` for `ກາລ`. The Python CLI regression asserts its low-confidence note. Canonical Lao rules and the target correspondence table are unchanged.

## Browser aggregate-output defect found and fixed

The first real Chromium run exposed a defect that the existing Node engine tests had not asserted: the syllable-level fallback correctly returned `ukrainian: "кал?"`, but the top-level browser `output` string was assembled from the original, pre-transformation `words` array. Consequently the details contained the provisional Ukrainian result while the visible main output remained `⟦ກາລ⟧`.

The fix transforms each word's syllable objects first, retains the transformed word groups, derives the flattened details array from those groups, and builds the final output from the transformed groups. This preserves whitespace/word boundaries and ensures the UI displays the exact adapted result. The app and engine module URLs are cache-busted together.

**Exact branch-head Verify:** [#42796566811 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42796566811), implementation commit `8c7fffe99746e21769ee40e92818f5e10fa5081c`. Python tests, Node browser-engine tests, build, generated-data reproducibility, real Chromium UI tests and built-page/relative-asset checks all passed.

## Task ledger

| Work item | Status | Acceptance / blocker |
|---|---|---|
| Python provisional IPA → ordinary Ukrainian adapter fallback | DONE_VERIFIED (existing mainline) | Source modules and tests exist; exact starting-main Verify #42776630426 passed |
| Browser provisional IPA → ordinary Ukrainian adapter fallback | DONE_VERIFIED (existing mainline) | Browser engine and tests exist; exact starting-main Verify #42776630426 passed |
| Browser aggregate output plus browser/CLI low-confidence details | DONE_VERIFIED | Updated UI/CLI and corresponding tests must pass on exact branch head |
| Canonical fallback documentation/navigation | DONE_VERIFIED | Conflicting preview-only wording replaced; exact branch-head CI required |
| Independent pronunciation accuracy | BLOCKED / evidence-limited | Independent adjudicated IPA gold remains 0; qualified annotators and adjudication required |
| Non-core Indic/Khmu graphemes | DEFERRED from modern-Lao phonetic scope | Preserve/mark unknown; do not invent a modern-Lao reading |

## Branch and PR state

- Working branch: `fix/provisional-grapheme-output-docs-20261110`, created from `0a91bb62d48a6110d5129460fae4efee580863f2`.
- Existing branches are preserved; no force-push or branch deletion.
- PR #145 remains open and untouched because it proposes a distinct production architecture.
- Exact branch-head Verify [#42796566811 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42796566811) passed on implementation commit `8c7fffe99746e21769ee40e92818f5e10fa5081c`. PR #159 remains open and unmerged; no Pages deployment is claimed.

**Readiness:** engineering-verified research prototype. The fallback rendering contract is implemented; linguistic accuracy remains unvalidated. A visible low-confidence answer must not be marketed as a confirmed pronunciation.

---
