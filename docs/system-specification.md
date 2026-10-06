# Lao → Ukrainian system specification

## Scope

The active model is contemporary Standard Lao with a Vientiane-oriented phonological reference model. It is not a universal model of every Lao variety.

## Processing layers

1. Unicode normalization and script validation.
2. Graphemic syllable parsing.
3. Consonant-class identification.
4. Vowel structure and quantity.
5. Coda and live/dead classification.
6. Vientiane tone determination.
7. Phonemic IPA representation.
8. Ukrainian practical rendering.

The Russian, Serbian and Bulgarian layers are comparative controls. They are never hidden intermediate representations.

## Canonical data

The active Lao registries are under `data/lao/`. The Ukrainian correspondence registry is `data/lao/ukrainian_correspondences.csv`. Comparative evidence is under `data/comparative/`; source/claim provenance is under `data/evidence/`.

## Core Lao contrasts

The current registry represents the modern consonant classes High, Middle and Low; positional onset/final values; the nine monophthongal vowel qualities with short/long contrasts; the three core centering diphthongs; and the special orthographic patterns `ໄ/ໃ`, `ເ◌ົາ`, and `ຳ`.

## Tone

Tone is a separate field. The Vientiane reference model has five tones. Tone is derived from consonant class, live/dead syllable type, vowel quantity where relevant, and written tone mark. Exact phonetic contours are analysis-dependent across descriptions and are therefore not treated as universally fixed surface measurements.

## Ukrainian output

The practical layer deliberately neutralizes several source-language distinctions that Ukrainian orthography does not naturally preserve:

- aspiration of /kʰ pʰ tʰ/ is retained in IPA but not represented as `х`;
- /h/ is approximated by `г`, explicitly as a project decision rather than phonemic identity;
- /ɯ/ is approximated by `и`;
- /tɕ/ is represented by `ч`;
- vowel length is not automatically doubled.

These are project decisions, not an official Ukrainian national standard.
