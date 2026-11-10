# Current exact-head continuation — 2026-11-10 (authoritative addendum)

**Repository:** `ClippyFirst/Lao-Ukrainian-Phonetic-System`.  
**Starting main SHA:** `0a91bb62d48a6110d5129460fae4efee580863f2`.  
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

The browser detail panel and text CLI are being made explicit about:
- low confidence / provisional reading;
- the Ukrainian output actually produced;
- unresolved graphemes or positions and visible `?` markers;
- the fact that tone was not inferred.

The browser regression is updated to expect a Ukrainian provisional result for `ກາລ`, not an empty/withheld result. This change does not modify canonical Lao rules or the target correspondence table.

## Task ledger

| Work item | Status | Acceptance / blocker |
|---|---|---|
| Python provisional IPA → ordinary Ukrainian adapter fallback | DONE_VERIFIED (existing mainline) | Source modules and tests exist; exact starting-main Verify #42776630426 passed |
| Browser provisional IPA → ordinary Ukrainian adapter fallback | DONE_VERIFIED (existing mainline) | Browser engine and tests exist; exact starting-main Verify #42776630426 passed |
| Browser and CLI low-confidence details | PARTIAL pending branch CI | Updated UI/CLI and corresponding tests must pass on exact branch head |
| Canonical fallback documentation/navigation | PARTIAL pending branch CI | Conflicting preview-only wording replaced; exact branch-head CI required |
| Independent pronunciation accuracy | BLOCKED / evidence-limited | Independent adjudicated IPA gold remains 0; qualified annotators and adjudication required |
| Non-core Indic/Khmu graphemes | DEFERRED from modern-Lao phonetic scope | Preserve/mark unknown; do not invent a modern-Lao reading |

## Branch and PR state

- Working branch: `fix/provisional-grapheme-output-docs-20261110`, created from `0a91bb62d48a6110d5129460fae4efee580863f2`.
- Existing branches are preserved; no force-push or branch deletion.
- PR #145 remains open and untouched because it proposes a distinct production architecture.
- Exact branch-head Verify and PR state will be appended after CI; the starting-main success is not evidence for untested edits.

**Readiness:** engineering-verified research prototype. The fallback rendering contract is implemented; linguistic accuracy remains unvalidated. A visible low-confidence answer must not be marketed as a confirmed pronunciation.

---
