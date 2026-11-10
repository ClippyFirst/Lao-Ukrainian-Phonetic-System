# Lao visual culture research notes for the public-site redesign

**Date:** 2026-11-10

## Evidence-backed visual references

### Lao textile construction

- UNESCO/KPL reports that Naga motifs are woven directly into Lao textiles on a traditional wooden loom, rather than embroidered or printed afterwards. The weaving practice and motifs are transmitted through families and communities.  
  Source: https://kpl.gov.la/EN/detail.aspx?id=80924
- The UNESCO nomination document describes supplementary weft and discontinuous supplementary weft as key techniques, and identifies traditional materials and dyes used in the motif.  
  Source: https://ich.unesco.org/doc/src/49323-EN.pdf
- Asia InCH documents the variety of Lao textile techniques and motifs, including sinh mi, sinh chok, and sinh khid, and cautions that meanings and arrangements vary by community and region.  
  Source: https://asiainch.org/craft/textiles-of-laos/
- The Asian Art Museum's ceremonial cloth example shows indigo ground, silk/cotton construction, repeated mirrored motifs, and a palette using white with green, yellow, and blue accents. This is one specific object, not a universal Lao palette.  
  Source: https://artsandculture.google.com/asset/ceremonial-cloth/WQHJ18f1B7p_1g?hl=en

### Contemporary identity reference

- The Visit Laos 2024 visual identity guide documents a Lao-script type choice (PB Warnjai Bold) alongside a separate Latin-script display face. This supports treating Lao script as a typographic voice rather than as a decorative glyph.  
  Source: https://laos-dmn.com/wp-content/uploads/2023/11/Visit-Laos-Year-2024-Visual-Identity_English.pdf

## Design decisions derived from the research

1. Translate the loom's *construction logic* into a restrained CSS weave band: repeated crossings, ordered rhythm, and layered lines.
2. Use an earthy material palette: paper/silk ground, indigo, deep green, and a controlled warm red accent. These are design choices informed by examples, not claims that every Lao community uses the same palette.
3. Make Lao script prominent and correctly typeset, paired with Ukrainian interface text and an IPA-specific technical face.
4. Keep the Naga motif out of generic UI decoration. UNESCO describes it as a culturally meaningful motif woven into specific garments and practices; reproducing it as a logo, badge, or wallpaper would flatten that context.
5. Do not use Hmong, Tai Dam, or other ethnic textile motifs as generic stand-ins for Lao identity. The site is specifically about the Lao language; any further use should identify the community and provenance.

## Contemporary web-design principles applied

- Strong editorial type hierarchy and asymmetry, but keep the task surface immediately usable.
- Real product UI and real text as the visual content; no generic stock photography or decorative mock dashboard.
- One coherent token system, one signature graphic device, minimal motion, accessible controls, and responsive layouts.
- Performance first: static HTML/CSS, no animation library, no WebGL, no additional runtime dependency.

## Limitations

- The research references are secondary descriptions and selected objects; they do not replace consultation with Lao textile practitioners or designers.
- The palette and CSS pattern are original design interpretations, not a reconstruction of a specific traditional textile.
