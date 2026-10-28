# Romanization engine research — Lao

**Date:** 2026-10-28  
**Repository:** https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System  
**Status:** RESEARCH_COMPLETE / RUNTIME_INTEGRATION_TODO

## User-facing requirement

Add a separate Latin-script romanization result alongside the source text, IPA, and Ukrainian practical transcription. The result must be described as a romanization system, not as English spelling, translation, IPA, or Ukrainian transcription. It must preserve whitespace and punctuation, expose the chosen profile, and never infer pronunciation merely because a source grapheme was parsed.

## Candidate review

### Standards and reference data

- Unicode CLDR transliteration guidelines: https://cldr.unicode.org/index/cldr-spec/transliteration-guidelines
- CLDR transforms are versioned and include language/script-specific data. The CLDR release notes list the relevant transforms: https://cldr.unicode.org/downloads/cldr-43
- UNGEGN's current inventory of romanization systems: https://unstats.un.org/unsd/ungegn/romanization/
- BGN/PCGN systems are officially described as geographical-name romanization systems; they should not automatically be advertised as a universal standard for all prose: https://www.gov.uk/government/publications/romanization-systems

### Cross-language engines

1. **Aksharamukha** — broad script and romanization coverage, including Khmer, Lao, Burmese/Myanmar and Sinhala; offers readable/colloquial and scholarly romanization profiles. Upstream project declares AGPL-3.0, so it must not be bundled into this repository without a deliberate licensing compatibility decision. References: https://github.com/virtualvinodh/aksharamukha and https://github.com/paramsiddharth/aksharamukha.js
2. **inditrans** — browser/WASM, MIT-licensed, supports Khmer, Burmese and Sinhala but does not list Lao in its supported-script enum. Its ITRANS/Indlish outputs are generic romanization not a substitute for a national system. References: https://github.com/vm75/inditrans and https://github.com/vm75/inditrans/blob/main/nodejs/README.md
3. **uroman** — multilingual, context-aware universal romanizer, with documented improvements for Khmer and general South/Southeast Asian scripts. It is useful as a baseline/comparator but does not claim to implement each language's national romanization standard, and the maintained release is Python rather than a drop-in browser engine. References: https://github.com/isi-nlp/uroman and https://aclanthology.org/P18-4003/
4. **Unicode CLDR transforms** — permissively reusable, versioned rule data and the best starting point for an offline/local implementation where available. The transform must be evaluated for this language's coverage and behavior rather than assumed to be a pronunciation engine.

## Language-specific decision

**Preferred reference:** CLDR Lao→Latin transform, compared with the UNGEGN/BGN-PCGN geographical-name system. The official system's scope must be shown in the UI; a geographic-name standard is not automatically a fully phonetic rendering of running prose. Aksharamukha covers Lao but is AGPL-3.0. inditrans does not list Lao as a supported script.

The existing Lao engine preserves tone contours and may withhold incomplete syllables. Romanization must be a separate orthographic output and must not suppress, invent, or rewrite the IPA tone metadata. Source context: https://unstats.un.org/unsd/ungegn/romanization/ and https://www.gov.uk/government/publications/romanization-systems

## Required architecture

Keep the following outputs independent:

`source orthography → existing structural/phonological analysis → IPA`

and

`source orthography → selected orthographic romanization profile → Latin-script result`

The romanizer must not read IPA or the Ukrainian result as its source, and adding romanization must not change existing IPA or Ukrainian behavior. If a profile cannot handle a token, preserve the original token and mark the romanization as partial instead of silently dropping or guessing.

## Acceptance criteria before marking implementation complete

- [ ] A local/browser-compatible engine is pinned and its exact license is recorded.
- [ ] Profile name, version/source and intended scope are visible in the UI.
- [ ] Romanization is produced for sentences, mixed punctuation and spaces without destroying boundaries.
- [ ] Tests cover source-script recognition, combining marks, representative words and sentences, digits/punctuation, unknown characters, and mixed-script input.
- [ ] Reference cases are sourced and explicitly distinguished from merely plausible examples.
- [ ] Romanization changes do not alter IPA or Ukrainian results.
- [ ] Browser tests verify the output panel and copy action.
- [ ] CI and Pages deployment pass on the exact candidate commit.
- [ ] The canonical master execution plan and handoff record the implementation SHA and exact test results.

## Current truthful status

The candidate survey is complete. Runtime integration is **not** complete in this commit. No engine output, accuracy score, or passing test is claimed here. Do not mark the site as having a working romanizer until the above gates pass.
