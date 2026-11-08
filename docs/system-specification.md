# Lao → Ukrainian system specification

## Scope

The active model is contemporary Standard Lao with a Vientiane-oriented phonological reference model. It is not a universal model of every Lao variety.

## Primary deterministic engine

ClippyFirst's primary Lao engine is `hybrid-deterministic`, selected by default in the Python API, rules CLI and browser runtime. It uses the Vientiane-oriented phonological analysis as its base and applies only the existing evidence-gated MekongPhon aggregate correspondences through a deterministic contextual selector. The explicit `vientiane` and `mekongphon-reference` profiles are frozen for compatibility only; future engine implementation and optimization work targets hybrid. Optional Neural inference is not part of the default transcription path. This engine-selection decision does not establish independent phonetic accuracy or linguistic release readiness.

## Processing layers

1. Unicode normalization and script validation.
2. Graphemic syllable parsing.
3. Consonant-class identification.
4. Vowel structure and quantity.
5. Coda and live/dead classification.
6. Vientiane tone determination.
7. Phonemic IPA representation.
8. Typed `PhoneticResult` adapter boundary.
9. Ukrainian adaptation from that typed IPA result.
10. Practical Ukrainian orthography.

The Russian, Serbian and Bulgarian layers are comparative controls. They are never hidden intermediate representations.

## Canonical data

The active Lao registries are under `data/lao/`. The Ukrainian correspondence registry is `data/lao/ukrainian_correspondences.csv`. Comparative evidence is under `data/comparative/`; source/claim provenance is under `data/evidence/`.

## Core Lao contrasts

The current registry represents the modern consonant classes High, Middle and Low; positional onset/final values; the nine monophthongal vowel qualities with short/long contrasts; the three core centering diphthongs; and the special orthographic patterns `ໄ/ໃ`, `ເ◌ົາ`, and `ຳ`.

## Tone

Tone is a separate field. The Vientiane reference model has five tones. Tone is derived from consonant class, live/dead syllable type, vowel quantity where relevant, and written tone mark. Exact phonetic contours are analysis-dependent across descriptions and are therefore not treated as universally fixed surface measurements.

## Ukrainian output

The executable target boundary is a typed `PhoneticResult`; the Ukrainian adapter consumes only its registered IPA segments and metadata. In the primary hybrid profile, structurally complete UNCERTAIN IPA may be adapted as a low-confidence Ukrainian rendering while its uncertainty status is preserved. When no defensible IPA can be produced, a typed PROVISIONAL unknown segment crosses the same adapter boundary and renders a visible ? placeholder; it is not IPA and is never counted as phonetic accuracy. The frozen Vientiane and MekongPhon-reference compatibility profiles retain their historical withholding behavior. Tone uncertainty is independent: when segmental IPA is supported, the Ukrainian form may be produced while tone remains unresolved in metadata. The current Lao engine does not claim an independent broad-surface IPA layer. See [the adapter contract](ipa-to-ukrainian-adapter.md).



The practical layer deliberately neutralizes several source-language distinctions that Ukrainian orthography does not naturally preserve:

- aspiration of /kʰ pʰ tʰ/ is retained in IPA but not represented as `х`;
- /h/ is approximated by `г`, explicitly as a project decision rather than phonemic identity;
- /ɯ/ is approximated by `и`;
- /tɕ/ is represented by `ч`;
- vowel length is not automatically doubled.

These are project decisions, not an official Ukrainian national standard.
