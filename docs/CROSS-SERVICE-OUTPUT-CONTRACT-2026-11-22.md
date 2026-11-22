# Cross-service output contract matrix — 2026-11-22

This is the canonical cross-repository status snapshot for the six language services. It records actual implementation and CI/Pages evidence, not linguistic accuracy. Mode labels are standardized only where distinct inclusion rules already exist.

## Shared contract

- **Final Ukrainian UI placeholder:** `???` for an unresolved final target run/unit. It is a display marker, not an IPA token, source transliteration or confidence score.
- **Internal IPA unknown:** remains typed and diagnostic; it must not be replaced by the Ukrainian display marker.
- **Confirmed vs candidate:** a research candidate must never silently replace a confirmed result. Candidate status, uncertainty, source/provenance and explanations remain inspectable.
- **API representation:** structured runtimes should keep unavailable results as `null` / `None` plus status/reason/trace. Render `???` at the user-facing result boundary rather than corrupting the machine-readable API type.
- **Strictness levels:** names represent evidence/inclusion policies, not accuracy grades. Soft and Super-soft are not mandatory when the repository has no distinct, defensible broader rule set.

## Repository ledger

| Service | Strictness decision | Final UI marker | Candidate / diagnostic boundary | Runtime verification | GitHub Pages |
|---|---|---|---|---|---|
| [Lao](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System) | Strict-only; phonetic vs romanization is a separate route, not a confidence level | `???` per contiguous unresolved target run, merged PR #276 | Typed IPA unknown remains distinct; Python and browser target adapters share the marker | DONE_VERIFIED: PR #276 exact-head workflow [45002639491](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/45002639491) passed Python/browser/Chromium checks | DONE_VERIFIED: [45002868618](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/45002868618) succeeded; runtime commit deployed. Later docs-only commit does not change site assets |
| [Burmese](https://github.com/ClippyFirst/Burmese-Ukrainian-Phonetic-System-) | Strict / Soft / Super-soft map to existing `strict` / `balanced` / `exploratory`; phonetic vs MLCTS and A–D evidence tiers stay separate | Main already has `???`; branch PR #202 aligns provisional/candidate paths | Canonical output, provider candidates and confidence tiers remain separate | DONE_VERIFIED: PR #202 merged as `9a6bd1062e0bdd7bcb513d82aef4683fab2cb241`; main Python/Node/build/Playwright tests [45003648762](https://github.com/ClippyFirst/Burmese-Ukrainian-Phonetic-System-/actions/runs/45003648762) SUCCESS | DONE_VERIFIED: post-merge Pages deployment [45003648702](https://github.com/ClippyFirst/Burmese-Ukrainian-Phonetic-System-/actions/runs/45003648702) SUCCESS on runtime merge commit `9a6bd1062e0bdd7bcb513d82aef4683fab2cb241` |
| [Khmer](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-) | Strict / Soft / Super-soft map to existing `strict` / `balanced` / `exploratory`; labels merged PR #509 | `???` | Per-unit `PROPOSED`/unresolved status and research hints stay distinct; Super-soft hints are not confirmed pronunciation | DONE_VERIFIED: PR #509 exact-head quality and browser checks passed [45002160320](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/45002160320) and [45002160358](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/45002160358) | DONE_VERIFIED: [45003349245](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/45003349245) succeeded on current main |
| [Sinhala](https://github.com/ClippyFirst/Sinhala-Ukrainian-Phonetic-System-) | Strict-only; Soft/Super-soft deferred until contextual phonology and evidence rules exist | `???` | Exact segment-level matches are listed separately from whole-input research candidate; diagnostic confidence is categorical and bounded | PARTIAL: Python and browser checks pass separately; direct semantic parity fixtures are not yet established | BLOCKED: repository is private; Pages run [45002246748](https://github.com/ClippyFirst/Sinhala-Ukrainian-Phonetic-System-/actions/runs/45002246748) fails `configure-pages` with 404 because no Pages site is configured |
| [Thai](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System) | Strict-only IPA adapter; `allowProvisional` is a research candidate control, not a full Soft level; Super-soft deferred | PR #236 adds `???` UI fallback; API remains typed null | External FastThaiG2P candidate remains visibly provisional; typed IPA keeps tone, vowel length, provenance and uncertainty | PARTIAL → PR #236 API/site/static checks passed; full CI still running at snapshot | DONE_VERIFIED: post-merge Pages deployment [45003654498](https://github.com/ClippyFirst/Thai-Ukrainian-Phonetic-System/actions/runs/45003654498) SUCCESS on runtime merge commit `785fa05bf91b5200585e9271a6ca671165e7ddee` |
| [Korean](https://github.com/ClippyFirst/Korean-Ukrainian-Phonetic-System) | Strict / Soft / Super-soft already have distinct Korean-specific inclusion rules; PR #497 aligns visible names | PR #497 changes unavailable primary UI output to `???`; API remains typed null | Confirmed result and research candidate have separate UI states; IPA token mapping, source, rules and confidence trace remain inspectable | PARTIAL → Python 3.11/3.12/3.13 passed; browser tests rerunning after label expectations updated; optional editorial/G2P jobs are separate | DONE_VERIFIED on main: [43391779118](https://github.com/ClippyFirst/Korean-Ukrainian-Phonetic-System/actions/runs/43391779118) succeeded on current main |

## Branches and pull requests

- Merged: Lao PR #276 (runtime marker) and #277 (handoff); Burmese PR #202 (shared levels/marker) and #203 (handoff); Khmer PR #509 (level labels) and #510 (handoff); Sinhala PR #24 (candidate separation and Strict-only contract); Thai PR #236 (UI marker) and #237 (handoff).
- Open at this snapshot: Korean PR #497. Do not call its branch changes part of main until post-merge CI/Pages are verified.
- Earlier Sinhala PRs #20–#22 remain untouched; they are not silently included.

## Acceptance gates still open

1. **Sinhala Pages:** owner enables GitHub Pages for the private repository through repository/plan settings. No visibility or billing setting is changed by this work.
2. **Sinhala runtime parity:** shared fixtures must compare source spans, typed IPA, target output, uncertainty, provenance and explanations across Python/browser before parity can be claimed.
3. **PR #202 / #236 / #497:** merge only after exact-head checks pass; then verify main CI and production Pages deployments.
4. **Linguistic evidence:** no mode expansion, source rule, accuracy score or IPA gold item may be invented to make a gate green. Expert/adjudicated evidence remains a separate research release gate.

**Overall status:** shared display semantics are implemented or in active PRs across all six services; engineering maturity remains mixed. Sinhala is a partial prototype and is not publicly deployed. No repository should be described as linguistically expert-validated solely because its software CI or Pages workflow passes.
