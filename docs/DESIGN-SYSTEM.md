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

The service keeps the existing Lao red/blue palette and the editorial-instrument direction. The service workspace follows the established Korean-service composition: input on the left and results on the right on wide screens, collapsing to one column on narrower screens. Within the result area, Ukrainian practical transcription is first and visually primary, followed by the provisional CLDR/UNGEGN romanization and then IPA. Syllable-level analysis is a collapsed disclosure below the result cards, so diagnostics remain available without competing with the main output.

## Motion and micro-interactions

Motion is limited to short control feedback and subtle hover/active transitions. Copy actions for all three output layers share the same confirmation behavior and announce the result through a polite live region. Reduced-motion preferences suppress non-essential transitions. No animation obscures, delays, or alters phonetic output.

React Bits is used as a reference for the craft of small, reusable micro-interactions, not as a runtime dependency. This repository remains a vanilla HTML/CSS/JavaScript application; no React runtime or third-party component bundle is introduced.

## Responsive and accessibility refinements

- The input and output remain side by side on wide screens and stack at tablet widths.
- The hero specimen becomes a compact two-column sample on narrow screens.
- Methodology navigation is a labelled nav element; both pages expose a keyboard skip link.
- Lao, IPA and Ukrainian output use separate typography roles and can wrap without clipping.
- Focus remains visible, controls retain a 44px minimum target, and reduced-motion preferences are respected.


## Korean-service layout parity · 2026-10-30

The Lao service intentionally shares the Korean service's information architecture without importing Korean-only functionality:

1. The input workbench occupies the left column.
2. The result workspace occupies the right column.
3. The Ukrainian practical transcription is the first, full-width result card.
4. Romanization and IPA follow as secondary cards.
5. Detailed syllable diagnostics are collapsed below the result cards and retain tone, syllable type, source form, IPA, Ukrainian mapping, rules, warnings and processing status.
6. At tablet/mobile widths, the workbench and result workspace stack; result cards become a single column on narrow screens.

The Lao service does not add Hanja, Korean G2P modes or other language-specific features merely to imitate the Korean page. The tests/web-layout.test.mjs suite protects the shared layout contract and output order.
