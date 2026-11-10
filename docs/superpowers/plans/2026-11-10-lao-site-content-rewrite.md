# Lao website content rewrite — 2026-11-10

## Intent

Rewrite every user-facing text passage on the two-page GitHub Pages site so that the product contract, linguistic method, uncertainty policy, and Lao-inspired visual concept are clear in Ukrainian. The service should read like a useful language instrument, not a generic AI landing page. The methodology should work as a self-contained explanation and reference.

## Audience and outcome

Primary readers are Ukrainian speakers who need to read Lao words or passages and want to understand how the system reached its result. Secondary readers are linguists, reviewers, and contributors evaluating the method.

A first-time visitor should understand what to paste, what the Ukrainian output represents, how IPA and romanization differ, what a low-confidence result means, and why the interface uses a woven editorial visual language.

## Approaches considered

1. **Minimal copy polish:** retain existing headings and paragraph order, only improve phrasing. Rejected because the existing text mixes implementation terminology, stale dates, and explanations that assume prior project knowledge.
2. **Marketing-led rewrite:** prioritize a short product pitch and reduce technical detail. Rejected because it would hide important caveats and weaken trust in a research instrument.
3. **Editorial, evidence-led rewrite (selected):** make the service page action-first and the methodology page a structured, plain-language guide. Preserve inspectable technical detail, explicit uncertainty, source links, and the current design system. This best fits a language tool whose credibility depends on showing its reasoning and limits.

## Scope

- Rewrite all visible copy and page metadata in `index.html` and `system.html`, including runtime-generated labels, trace rows, confidence notes and errors in `web/app.js`.
- Preserve every JavaScript-facing element ID, form control, output panel, result order, live region, and interaction contract.
- Keep the deterministic IPA-first path as the public default and romanization as a separate method.
- Explain typed provisional IPA fallback: known fragments still pass through the IPA-to-Ukrainian adapter; unresolved positions use `?`; confidence remains low; tone is not guessed.
- Refresh stale public research dates and describe benchmark results only as dictionary-seeded concordance, not independent phonetic accuracy.
- Add a fourteenth methodology section explaining the Woven Editorial concept, the cultural limits of visual borrowing, palette/type roles, and design-source links.
- Update accessible-name and static content tests to match the revised copy.
- Record the outcome in README and the canonical handoff/audit.

## Non-goals

- No change to phonological rules, IPA output, target adaptation, romanization engine, benchmark methodology, model, source data, or generated artifacts.
- No new JavaScript dependencies, external API, image generation, remote inference, or Work mode.
- No claim that the site is an official standard or linguistically validated production system.

## Content principles

- Ukrainian is the explanatory language; Lao and IPA remain in their own scripts.
- Prefer user-facing language over internal implementation names except where a technical term is necessary and explained.
- Separate established source facts, project conventions, and unresolved research.
- Never call a provisional IPA hint a confirmed pronunciation.
- Explain that Lao whitespace generally separates phrases rather than individual words.
- Cite W3C Lao Script Resources, Vientiane phonology literature, CLDR/BGN-PCGN and the repository's own research records where relevant.
- Describe Woven Editorial as an abstraction of weaving's rhythm and layered structure, not as a universal Lao pattern. Avoid flattening distinct communities and textile traditions into one motif.

## Acceptance criteria

- Both HTML pages have coherent, complete Ukrainian copy and updated metadata.
- All interactive IDs and result panel order are unchanged.
- The service still works with the deterministic engine; no neural model panel or download is reintroduced.
- All 14 methodology sections are reachable from the reading rail.
- Exactly three methodology tables remain; the two horizontally scrollable tables retain keyboard focus and accessible names.
- Browser tests continue to cover result rendering, quick examples, clear action, keyboard navigation, screen-reader names, responsive overflow, reduced motion, and 44px touch targets.
- New static tests assert the uncertainty contract and design rationale.
- Exact-branch GitHub Actions Verify and Pages deployment pass before merge.

## External skill research

Reviewed current guidance from:
- [Anthropic frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design): subject-grounded design, purposeful copy, distinctive but restrained decisions, accessibility and reduced motion.
- [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill): accessibility-first priorities, clear touch targets, responsive layout, typography and interaction checks.
- [Impeccable](https://github.com/pbakaus/impeccable): deliberate motion and interaction feedback; no animation without a user-facing purpose.
- [Emil Kowalski design engineering](https://github.com/emilkowalski/skills): interaction quality and restraint.
- [taste-skill](https://github.com/Leonxlnx/taste-skill): specific, non-template voice and a consistent visual system.

Process guidance: Superpowers brainstorming, writing-plans, TDD, executing-plans and verification-before-completion; Product Design get-context. Implementation remains in the repository and does not invoke image generation or Work mode.

## Research references used in the copy

- W3C, [Lao Script Resources](https://www.w3.org/TR/laoo-lreq/): writing direction, spacing, tone-class interaction, and spatial composition of vowel signs.
- Ueda (1994), [The Phonology of the Vientiane Dialect of Lao](https://www.jstage.jst.go.jp/article/gengo1939/1994/106/1994_106_95/_article): central Vientiane phonology.
- Global InCH, [Weaving of Laos](https://www.globalinch.org/craft/textiles-of-laos/): distinct textile techniques and regional/community variation.
- Repository research: `docs/research/LAO-VISUAL-CULTURE-AND-WEB-DESIGN-REFERENCES-2026-11-10.md`, `DESIGN.md`, and schema-8 engine inventory.

## Implementation record

- `index.html`: rewritten service copy and metadata; retained all engine-facing IDs; updated app script cache key.
- `web/app.js`: rewrote runtime-generated status notes, empty/error states, romanization explanation, trace labels and low-confidence disclosure without changing engine logic.
- `system.html`: rewritten all 13 methodological topics in plain Ukrainian and added section 14 on design rationale.
- `tests/browser/site.spec.js`: updated accessible names for revised action labels and the methodology heading.
- `tests/web-layout.test.mjs`: updated current-date assertions, 14-section check, and added content/uncertainty/design-concept checks.
- Verification and deployment status will be added after exact-branch CI completes.


## Final verification and publication

- **PR #168:** merged by squash on 2026-11-10.
- **Merge commit:** `a052b5b97fe2518497cddda8a45c76d80cb864a0`.
- **Exact-PR-head Verify:** [#42875206898 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42875206898): 350 Python tests, 155 Node tests, 22 Chromium tests; repository data/evidence audit, IPA gold schema validation, external-G2P syntax/CLI checks, build, generated-data reproducibility and built-page/asset checks passed.
- **Exact-main Verify:** [#42875399018 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42875399018): 350 Python tests, 155 Node tests, 22 Chromium tests and all repository verification gates passed on the merge commit.
- **GitHub Pages:** [#42875399023 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42875399023). Build, 155 Node tests, 22 Chromium tests, deterministic-only artifact checks, artifact upload, Pages deployment and live smoke test of the public home page, methodology page, app bundle and stylesheet passed.
- **Published service:** https://clippyfirst.github.io/Lao-Ukrainian-Phonetic-System/
- **Manual QA limitation:** no physical-device or dedicated screen-reader review was performed in this run. Automated checks cover the tested viewports, zoom, keyboard, touch, focus, reduced-motion and accessible-name contracts, but do not certify every assistive-technology combination.
- **Linguistic evidence limitation:** independent expert-adjudicated IPA gold remains 0. The copy makes no independent phonetic-accuracy claim.
