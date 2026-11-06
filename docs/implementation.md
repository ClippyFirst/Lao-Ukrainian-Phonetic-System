# Implementation

## Architecture

- `normalize.py` — NFC normalization and mixed-script validation.
- `parser.py` — Lao graphemic syllable parsing and structural vowel recognition.
- `phonology.py` — live/dead classification, tone lookup and phonemic IPA construction.
- `phonetic_result.py` — typed `PhoneticResult` boundary: IPA segments, syllable offsets, length, tone, provenance and uncertainty.
- `target.py` — typed-result-only IPA-to-Ukrainian adapter and candidate ranking.
- `core.py` — public analysis orchestration.
- `model.py` — serializable analysis dataclasses.
- `data.py` — registry loading.
- `cli.py` — command-line entry point.

## Reproducibility

- Run: `PYTHONPATH=src python -m unittest discover -s tests -v`
- The package metadata also exposes a `lao-ua` console entry point when installed in an environment with the declared build dependency.

## Important boundary

The current parser is a syllable parser, not a lexical word segmenter. Lao spaces are phrase-level rather than reliable word boundaries. A future unspaced-text segmenter must therefore be tested independently rather than silently inferred from whitespace.

## Failure discipline

Unknown Unicode, unknown vowel structures, and unsupported phonological combinations produce explicit status/warning information rather than silently inventing a correspondence.


## Browser romanization fallback

- `web/romanization.js` — constrained provisional CLDR Lao-Latin/UNGEGN conversion.
- `web/romanization-syllable-engine.js` — parser for romanized syllable onset, nucleus and coda, with a source-Lao onset, vowel-ID and coda crosswalk that distinguishes aspirated digraphs from independent /h/, preserves written onset forms, applies the supported silent-hoa sonorant rule, validates supported CLDR vowel/coda aliases, and withholds mismatched structures before Ukrainian syllable assembly; ambiguous or mismatched parses are withheld.
- `web/romanization-ukrainian.js` — compatibility export for the syllable engine; it no longer contains a letter-by-letter mapping.
- `web/app.js` — the Ukrainian result selector, selected-result copy action, and method-specific disclosure.

The phonetic engine remains the default. Its Ukrainian output is produced only from the typed `PhoneticResult`; uncertain or unsupported results are withheld. The second method uses an independent romanized-syllable parser and is not a pronunciation analysis. See [methodology](methodology.md#optional-romanization-to-ukrainian-mode) for the grapheme/romanization/target crosswalk, aspiration policy, and information-loss boundary.

See [the typed IPA → Ukrainian adapter contract](ipa-to-ukrainian-adapter.md) for the executable boundary, status semantics and verification.

## Ukrainian IPA target sequence handling

The canonical IPA correspondence registry is shared by the Python target adapter and generated browser engine. Longest-match selection maps the exact Ukrainian sequence /ʃt͡ʃ/ to щ before considering the shorter /ʃ/ → ш and /t͡ʃ/ → ч entries. This does not merge arbitrary consonants: the exact ordered sequence is a documented target orthographic unit. The remaining distinctions /h, ɦ/ → г, /ɡ/ → ґ, /x/ → х, /d͡ʒ/ → дж, /d͡z/ → дз and /t͡s/ → ц are preserved in the same canonical table.

## Static web build clarification — 2026-11-06

The current web implementation is framework-free: index.html and system.html load native ES modules from web/. scripts/generate_web_data.py writes the canonical CSV mirror web/data.js; scripts/build_web.py copies both pages and the runtime into dist/. There is no Vite dependency or bundler in package.json. Node tooling is used for tests and Playwright, not for bundling the application. See [web architecture](web-architecture.md).
