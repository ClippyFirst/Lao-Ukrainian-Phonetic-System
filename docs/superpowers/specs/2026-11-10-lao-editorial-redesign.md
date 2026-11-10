# Lao Editorial Redesign — Design Brief

**Date:** 2026-11-10  
**Surface:** Static GitHub Pages website, service page `/` and methodology page `/system.html`  
**Mode:** Operate first; Read second.

## Intent

Replace the current generic red/blue technical-panel visual language with a distinct, contemporary Lao editorial identity while preserving the site as a fast, accessible, browser-only Lao-to-Ukrainian transcription tool.

## Audience and job

A visitor arrives to enter Lao text, immediately see Ukrainian practical reading, optionally inspect romanization and IPA, and open syllable-level analysis. A secondary reader wants to understand the method and its limits.

## Product truth to preserve

- The public site remains static and runs on GitHub Pages.
- The deterministic IPA-first phonetic method remains the default.
- The independent romanization method remains selectable.
- Output order remains Ukrainian, romanization, IPA.
- Syllable analysis and uncertainty/warnings remain available.
- The methodology page retains all 13 sections, source caveats, and the explicit statement that independent adjudicated IPA gold currently has zero examples.
- No neural model, download, external inference service, or new runtime dependency is introduced.

## Visual concept: Woven editorial

A contemporary editorial interface grounded in Lao textile structure, especially the logic of supplementary weft and the layered geometry of sinh/chok cloth. The design borrows the *construction principle*—repetition, interlocking, rhythm, and a strong woven border—rather than lifting sacred motifs as generic decoration.

Palette:
- Flax paper: `#F4EFE5`
- Warm silk: `#FFFCF5`
- Mekong deep green: `#173F3A`
- Indigo dye: `#34465C`
- Lac red: `#A94735`
- Natural brass: `#B58A4A`
- Ink: `#252D29`

Typography:
- Manrope for Ukrainian/Latin interface and display hierarchy.
- Noto Sans Lao for Lao script.
- IBM Plex Mono only for IPA and technical notation.
- System fallbacks remain available; no font is required for functionality.

Layout:
- A compact masthead and editorial hero lead directly into the input.
- The first screen must expose the tool quickly; no oversized marketing-only hero.
- The input is the primary working surface. Results form a clear hierarchy: Ukrainian output first, then romanization and IPA.
- Methodology becomes a calm reading layout with a sticky contents rail on wide screens and a compact horizontal contents list on mobile.
- Use a restrained woven rule/border as the signature device; no wallpaper patterns or decorative iconography.

## Approaches considered

1. **Woven editorial (selected):** textile construction logic, paper/silk palette, deep river/indigo colours, a restrained lac-red accent, strong typography. Best fit because it is Lao-specific without turning the tool into a cultural theme park.
2. **River-temple dark mode:** dark stone, brass, river green, dramatic contrast. Rejected because it over-stylizes an everyday tool and weakens long-form reading.
3. **Minimal type foundry:** near-monochrome, typography-only, no textile language. Rejected because it loses the Lao cultural grounding requested by the owner.

## Goals

- Make the interface recognizably Lao in a considered, culturally literate way.
- Make the tool feel modern, calm, trustworthy, and crafted rather than AI-templated.
- Improve visual hierarchy, reading rhythm, responsive behavior, and focus/interaction states.
- Keep pages fast, self-contained, and compatible with GitHub Pages.
- Preserve all functional IDs and JavaScript contracts.

## Non-goals and anti-goals

- No change to linguistic algorithms, output rules, IPA pipeline, or data.
- No new JavaScript framework, animation library, image CDN, or model download.
- No generic bento-card dashboard, glassmorphism, gradients, random scroll animations, parallax, or decorative emoji.
- No use of the Naga as a generic logo, repeating background, or ornamental badge.
- No invented linguistic accuracy claims or cultural attributions.

## Motion and accessibility

Use only short, purposeful transitions for hover, press, disclosure, and focus. Respect `prefers-reduced-motion`. Maintain keyboard navigation, visible focus, semantic landmarks, 44px control targets, adequate contrast, and readable Lao/IPA glyphs.

## Acceptance criteria

- Existing functional element IDs and event contracts remain unchanged.
- Both pages share one coherent design system.
- At 1440, 1024, 768, 390, and 320px there is no horizontal page overflow or overlapping content.
- The tool remains usable by keyboard and touch.
- Existing tests plus new design regression checks pass.
- GitHub Pages build and Chromium tests pass before deployment.
