# Design System — Woven Editorial

## Product mode

- **Service page:** Operate — visitors enter Lao text and inspect Ukrainian, romanized, IPA, and syllable analysis results.
- **Methodology page:** Read — visitors understand the transcription method and its limitations.
- **Brand idea:** Lao textile construction translated into a contemporary editorial interface. The motif is the *logic of weaving*, not a literal sacred emblem.

## Visual principles

1. The tool is the hero. Keep the input visible quickly; do not sacrifice utility to a giant marketing banner.
2. Use the construction language of woven sinh/chok cloth: rhythm, interlocking lines, repeated structure, deliberate borders, and layered information.
3. Keep the page calm and tactile: paper, silk, ink, indigo dye, river green, and a small lac-red accent.
4. Use real content as the visual material: Lao script, IPA, Ukrainian output, and actual syllable analysis.
5. One clear result hierarchy: Ukrainian first, romanization second, IPA third.
6. Avoid generic dashboards, glass, gradient text, decorative emoji, random motion, and card grids that repeat the same shape.

## Palette

| Token | Value | Role |
|---|---|---|
| `paper` | `#F4EFE5` | Main page ground |
| `silk` | `#FFFCF5` | Input and content surfaces |
| `ink` | `#252D29` | Primary text |
| `muted` | `#68716A` | Secondary text |
| `line` | `#D8D0C2` | Dividers and borders |
| `mekong` | `#173F3A` | Primary brand/action |
| `indigo` | `#34465C` | Secondary/IPA |
| `lac` | `#A94735` | Restrained accent |
| `brass` | `#B58A4A` | Rare emphasis |

## Typography

- **Manrope:** Ukrainian/Latin interface, headings, body copy.
- **Noto Sans Lao:** all Lao script and input text.
- **IBM Plex Mono:** IPA and technical notation only.
- Use system fallbacks; external font failure must not impair function.

## Layout and components

- Content width: 1180px maximum.
- Header: compact horizontal masthead, two navigation links, active state by underline.
- Service hero: editorial title plus one real syllable specimen; short enough that the input remains close to the first viewport.
- Signature: a narrow woven band built from restrained intersecting CSS lines. No sacred figure or copied textile artwork.
- Workbench: full-width Lao input, short example actions, visible local-processing note.
- Results: Ukrainian output is the dominant panel; romanization and IPA sit beneath it in a two-column arrangement where space allows.
- Analysis: disclosure panels remain collapsed by default.
- Methodology: two-column reading grid on wide screens (sticky contents rail + article); one-column on mobile.
- Tables: readable, keyboard-focusable when horizontally scrollable.

## Motion

- Use only short color/transform transitions for controls.
- Buttons press to 0.98 scale; hover states are subtle and disabled on coarse pointers.
- No scroll-jacking, parallax, timed movement, entrance cascades, or motion-only communication.
- Respect `prefers-reduced-motion`.

## Accessibility and responsive behavior

- Maintain visible `:focus-visible` rings.
- Minimum control height: 44px.
- Text contrast: WCAG AA target (4.5:1 body, 3:1 large text).
- Preserve semantic landmarks, labels, live regions, and skip links.
- Layout breakpoints: 900px, 620px, 380px.
- No horizontal page overflow at 320px.
- Lao input and IPA use appropriate font stacks and safe wrapping.

## Protected product contracts

Do not change any JavaScript-facing IDs in `index.html`, the result order, the default phonetic mode, the romanization mode, syllable-analysis behavior, or the IPA-first pipeline as part of a visual redesign.
