# Implementation

## Architecture

- `normalize.py` — NFC normalization and mixed-script validation.
- `parser.py` — Lao graphemic syllable parsing and structural vowel recognition.
- `phonology.py` — live/dead classification, tone lookup and IPA construction.
- `target.py` — IPA-to-Ukrainian correspondence layer.
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
