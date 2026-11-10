# Lao Editorial Redesign Implementation Plan

> **For agentic workers:** Execute the plan task-by-task; preserve the current deterministic tool behavior and verify the full suite before deployment.

**Goal:** Replace the visual identity of both public pages with a Lao-grounded editorial design without changing the transcription engine.

**Architecture:** Keep static HTML and the existing shared stylesheet. Preserve all JavaScript-facing IDs and page routes. Add only CSS and semantic markup; no framework or runtime dependencies.

**Tech Stack:** HTML, CSS, existing Node test suite, Playwright/Chromium, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-11-10-lao-editorial-redesign.md`

## Global Constraints

- GitHub Pages remains the deployment target.
- No linguistic engine or generated data changes.
- Preserve IDs consumed by `web/app.js`.
- Keep Ukrainian, romanization, and IPA output ordering.
- No external JavaScript, model assets, or image dependencies.
- Maintain accessible labels, keyboard focus, reduced-motion behavior, and 44px targets.

## Review Focus

- Empty state and populated result states retain visibility and status announcements.
- Long Lao/IPA strings wrap without widening the page.
- Method selector and copy controls remain operable on touch and keyboard.
- Methodology tables remain accessible and horizontally scrollable on narrow screens.
- Reduced-motion users receive no movement-dependent information.

---

### Task 1: Add design regression tests

**Files:**
- Modify: `tests/web-layout.test.mjs`

- [x] Assert new design tokens, typography declarations, woven-rule treatment, and page structure.
- [x] Assert existing functional IDs remain present.
- [x] Assert mobile and reduced-motion rules exist.
- [x] Verify the new tests fail against the current visual system.

### Task 2: Document the shared design system

**Files:**
- Create: `DESIGN.md`
- Create: `docs/superpowers/specs/2026-11-10-lao-editorial-redesign.md`

- [x] Record palette, type roles, spacing, layout, motif use, motion, and accessibility rules.

### Task 3: Redesign the service page

**Files:**
- Modify: `index.html`

- [x] Replace the generic hero copy and visual hierarchy with a compact Lao editorial masthead.
- [x] Keep all JavaScript-facing IDs and the current tool/result order.
- [x] Preserve factual project-status copy and caveats.

### Task 4: Redesign the methodology page

**Files:**
- Modify: `system.html`

- [x] Retain all 13 methodology sections and their content.
- [x] Improve reading hierarchy and navigation without changing linguistic claims.
- [x] Keep tables named and keyboard-focusable.

### Task 5: Replace the shared stylesheet

**Files:**
- Modify: `web/styles.css`

- [x] Implement the Woven editorial token system and responsive page compositions.
- [x] Style input, empty/results, analysis disclosures, methodology, tables, and footer consistently.
- [x] Add restrained motion, focus, selection, and reduced-motion behavior.

### Task 6: Verify and deploy

**Files:**
- Verify: `npm test`
- Verify: `npm run build`
- Verify: `npm run test:browser`
- Verify: GitHub Actions PR checks and Pages deployment.

- [x] Confirm all tests pass and generated artifacts remain deterministic.
- [x] Confirm both pages deploy and the browser-only engine still operates.


## Completion evidence

- **Merge:** PR #163, squash commit `9254bd4ecf014a6a5634ac05cebf0d227077977d`.
- **Exact-main Verify:** [#42847422102 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42847422102): 344 Python, 152 Node, 22 Chromium tests; repository audit, IPA gold schema, optional external-G2P CLI/syntax, build, generated-data reproducibility, and built-page checks passed.
- **Pages deployment:** [#42847422106 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42847422106): 152 Node, 22 Chromium tests, deterministic-only artifact checks, upload, deployment, and live same-origin smoke-test passed.
- **Automated responsive coverage:** service at 320, 390, 640, 768, 1024, 1440px; methodology at 320, 390, 768, 1024, 1440px; 200% text zoom, keyboard, touch, reduced-motion and 44px target checks.
- **Manual QA limitation:** no human visual review on physical devices or screen-reader hardware was performed in this run. CI establishes tested layout and interaction contracts, not a subjective pixel-perfect design review.
- **Superdesign limitation:** `npx --yes @superdesign/cli@latest` preflight timed out in the local shell because public hosts could not be resolved. Per user instruction, no switch to Work mode was made; the design was implemented directly in the repository with the other supplied design skills and the documented Woven Editorial brief.
