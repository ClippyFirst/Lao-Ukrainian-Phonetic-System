# Design System — Lao → Ukrainian

## Direction

**Editorial instrument, not SaaS dashboard.**

The interface should feel like a serious linguistic reference tool: generous whitespace, strong typography, visible structure, restrained color and dense but readable analytical information.

## Palette

- Lao red: #CE1126 — emphasis, active rule markers, important warnings.
- Lao blue: #002868 — navigation, primary actions, headings with strong hierarchy.
- Paper: #F7F5F0 — page background.
- White: #FFFFFF — content surfaces.
- Ink: #16181D — primary text.
- Muted: #626873 — secondary text.
- Border: #D9D7D1 — structural lines.

Use color semantically. Never make meaning depend on color alone.

## Typography

System-first sans-serif stack for Ukrainian and Lao coverage. Large editorial headings, compact labels, monospace for Lao/IPA/code-like analytical values.

## Components

- Masthead with two-link navigation.
- Input/editor block.
- Result block with copy action.
- Analysis table.
- Status badge.
- Warning/limitation notice.
- Methodology sections.
- Footer with scope/privacy statement.

Cards are structural containers, not decorative tiles.

## Interaction

- Visible keyboard focus.
- Buttons have explicit labels.
- Copy provides textual confirmation.
- Clear resets the service.
- Example inserts a known Lao sample.
- Reduced-motion preference is respected.

## Responsive behavior

Desktop: two-column service analysis where space permits.
Mobile: single-column flow, horizontally scrollable analytical tables, no clipped Lao or IPA text.

## Content style

Short labels, explicit terminology, no marketing claims. Use **system**, **correspondence**, **analysis**, **approximation**, **analysis-dependent** rather than implying official standardization.


## Visual identity refinement · 2026-10-30

The interface uses the Lao script itself as its signature visual material: a compact Lao wordmark and a real syllable specimen (ຂາ → /kʰaː/ → к'а). The specimen is a documented example, not a decorative placeholder or a simulated result.

The service keeps the existing Lao red/blue palette and the editorial-instrument direction. The result panel retains the actual pipeline order: provisional CLDR/UNGEGN romanization, IPA, then Ukrainian practical transcription. The Ukrainian layer receives the strongest typographic emphasis; provisional and analytical layers remain visibly secondary.

## Motion and micro-interactions

Motion is limited to short control feedback and subtle hover/active transitions. Copy actions for all three output layers share the same confirmation behavior and announce the result through a polite live region. Reduced-motion preferences suppress non-essential transitions. No animation obscures, delays, or alters phonetic output.

React Bits is used as a reference for the craft of small, reusable micro-interactions, not as a runtime dependency. This repository remains a vanilla HTML/CSS/JavaScript application; no React runtime or third-party component bundle is introduced.

## Responsive and accessibility refinements

- The input and output remain side by side on wide screens and stack at tablet widths.
- The hero specimen becomes a compact two-column sample on narrow screens.
- Methodology navigation is a labelled nav element; both pages expose a keyboard skip link.
- Lao, IPA and Ukrainian output use separate typography roles and can wrap without clipping.
- Focus remains visible, controls retain a 44px minimum target, and reduced-motion preferences are respected.
