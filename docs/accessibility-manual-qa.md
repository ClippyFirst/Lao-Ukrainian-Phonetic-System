# Manual accessibility QA protocol

## Purpose and status

This document is the execution record template for human accessibility review of the deployed Lao → Ukrainian service. Automated Chromium assertions are useful regression guards, but they do not substitute for assistive-technology sessions, real touch hardware, actual browser zoom, or a human visual review. The 200% and 400% cases in this file are viewport/CSS-zoom emulations only.

**Current status: NOT RUN / evidence not supplied.** No manual test is claimed complete by this document.

## Required environment record

For every session, record:

- Date and tester.
- Deployment URL and commit SHA tested.
- Operating system and version.
- Browser and exact version.
- Assistive technology and exact version, where applicable.
- Device model, screen size, orientation and input method.
- Pass/fail/blocked for each case, plus reproducible observations.

## Test matrix

| ID | Platform and assistive technology | Required checks |
|---|---|---|
| SR-01 | Windows 11 + NVDA + Firefox or Chrome | Navigate landmarks, headings, textarea label/help, quick examples, output status, copy feedback, mode state, analysis disclosures. |
| SR-02 | macOS + VoiceOver + Safari | Repeat SR-01; verify rotor landmarks/headings and announcement order during live updates. |
| SR-03 | iOS + VoiceOver + Safari, physical iPhone/iPad | Touch exploration, text entry, quick examples, method switch, copy feedback, disclosure controls, portrait/landscape. |
| SR-04 | Android + TalkBack + Chrome, physical device | Repeat SR-03; verify swipe navigation and focus remains visible and predictable. |
| KB-01 | Desktop keyboard only, no mouse | Tab/Shift+Tab through skip link, navigation, textarea, examples, clear, mode buttons, copy controls and disclosures; Enter/Space activate; no keyboard trap. |
| MOB-01 | Physical phone and tablet | Portrait/landscape, on-screen keyboard, touch targets, no clipped controls or horizontal page scrolling at 320–390 CSS px. |
| ZOOM-01 | Desktop browser zoom at 200% | Input, results, navigation and analysis remain readable and operable; no loss of content or two-dimensional page scrolling. |
| ZOOM-02 | Desktop browser zoom at 400% | Reflow equivalent to 320 CSS px; all essential content remains available without horizontal page scrolling. |
| VIS-01 | Windows High Contrast / forced-colors | Focus indicator, links, controls, status and boundaries remain distinguishable. |
| VIS-02 | Any supported desktop browser | Check contrast, text resizing, focus visibility, content order, clipping, and the reading order at 200% and 400%. |
| TGT-01 | Chromium responsive regression at 320, 390, 768 and 1280 CSS px | Verify primary navigation links, skip link, visible buttons and disclosure summaries have at least 44×44 CSS-pixel hit areas. |

## Execution steps

### Screen readers

1. Load the deployed service with an empty input.
2. Navigate by landmarks and headings; confirm one clear page-level heading, named primary navigation and main landmark.
3. Focus the Lao textarea; confirm its accessible name and help description.
4. Enter `ຂາ`; confirm that the result and analysis status are announced once, coherently, without reading the entire page repeatedly.
5. Switch between phonetic and romanization modes; confirm pressed state is announced.
6. Open and close the syllable analysis disclosure; confirm expanded/collapsed state and that its contents are reachable.
7. Trigger copy; confirm success/failure feedback is announced without relying on color alone.
8. Repeat with unsupported input and partial output; confirm uncertainty and warnings are announced clearly.

### Keyboard

1. Reload with focus at the browser chrome and press Tab.
2. Confirm the skip link is first and moves focus to the tool input.
3. Continue through every interactive control in a logical order; reverse with Shift+Tab.
4. Operate buttons with Enter and Space; operate disclosures with Space/Enter.
5. Confirm visible focus at all times and no keyboard trap.

### Mobile and zoom

1. Use physical devices, not only desktop device emulation.
2. Test portrait and landscape with the on-screen keyboard both open and closed.
3. Test browser zoom at 200% and 400%; do not substitute CSS transforms or device emulation for the browser's actual zoom setting.
4. Confirm the page reflows without horizontal scrolling and that controls remain reachable and readable.

## Results log

| ID | Status | Environment / versions | Findings / evidence |
|---|---|---|---|
| SR-01 | NOT RUN | — | — |
| SR-02 | NOT RUN | — | — |
| SR-03 | NOT RUN | — | — |
| SR-04 | NOT RUN | — | — |
| KB-01 | AUTOMATED PARTIAL | Chromium CI; exact run linked from master handoff | Automated keyboard and focus regression tests pass; deployed keyboard-only human walkthrough remains outstanding. |
| MOB-01 | AUTOMATED PARTIAL | Chromium touch emulation; 390×844 | Emulation passes; physical devices remain outstanding. |
| ZOOM-01 | AUTOMATED PARTIAL | Chromium CSS zoom emulation | 200% equivalent test passes; actual browser zoom remains outstanding. |
| ZOOM-02 | AUTOMATED PARTIAL | Chromium CSS zoom emulation | 400% equivalent regression test added; exact-head CI pending. |
| VIS-01 | AUTOMATED PARTIAL | Chromium forced-colors emulation | CSS focus/link/border regression passes; Windows High Contrast human review remains outstanding. |
| VIS-02 | NOT RUN | — | Human contrast and visual review outstanding. |
| TGT-01 | AUTOMATED PASS | GitHub Actions Verify [42460222889](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42460222889); Chromium | All visible primary navigation links, skip link, buttons and disclosure summaries meet 44×44 CSS-pixel minimum at 320/390/768/1280 CSS px. Brand link receives a 44px minimum height. This does not replace physical-device validation. |

## Acceptance rule

UI-001 may be marked DONE_VERIFIED only after the required human sessions are recorded with versions, outcomes, and any defects fixed and retested. CI success alone is insufficient.


## Automated regression update — 2026-11-08

- Added a 44×44 CSS-pixel hit-area assertion for the visible primary navigation links, skip link, buttons and disclosure summaries at 320, 390, 768 and 1280 CSS-pixel viewports.
- Raised the brand link's minimum height to 44px so its interactive hit area meets the same design-system floor.
- Exact-head Verify [42460222889 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42460222889): all 17 Chromium tests passed, alongside the existing Python/Node/build/npm-ci gates.
- TGT-01 is automated PASS. UI-001 remains PARTIAL: the screen-reader, physical-device, real-browser-zoom and human visual sessions below remain NOT RUN until performed and recorded by a human tester.
