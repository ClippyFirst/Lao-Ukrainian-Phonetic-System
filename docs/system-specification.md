# Lao → Ukrainian system specification

## Scope

The active model is contemporary Standard Lao with a Vientiane-oriented phonological reference model. It is not a universal model of every Lao variety.

## Processing layers

The primary runtime keeps source G2P and target adaptation as two explicit stages:

1. Unicode normalization and Lao script validation.
2. **Stage 1 — Lao → IPA:** the pinned MekongPhon Neural tonal checkpoint (or explicitly selected non-tonal checkpoint) predicts raw IPA.
3. Preserve the untouched model output, immutable model revision and provider provenance.
4. Parse the complete prediction into typed `PhoneticResult` segments, retaining tone, length, boundaries and uncertainty; unsupported IPA is withheld.
5. **Stage 2 — IPA → Ukrainian:** only when requested, adapt the typed IPA through the Ukrainian correspondence registry.
6. Render practical Ukrainian orthography.

The deterministic ClippyFirst grapheme/phonology/tone engine remains available as an explicit independent alternative and diagnostic. It is not the primary Lao-to-IPA provider and is never a silent fallback for MekongPhon.

The Russian, Serbian and Bulgarian layers are comparative controls. They are never hidden intermediate representations.

## Canonical data

The active Lao registries are under `data/lao/`. The Ukrainian correspondence registry is `data/lao/ukrainian_correspondences.csv`. Comparative evidence is under `data/comparative/`; source/claim provenance is under `data/evidence/`.

## Core Lao contrasts

The current registry represents the modern consonant classes High, Middle and Low; positional onset/final values; the nine monophthongal vowel qualities with short/long contrasts; the three core centering diphthongs; and the special orthographic patterns `ໄ/ໃ`, `ເ◌ົາ`, and `ຳ`.

## Tone

Tone is a separate field. The Vientiane reference model has five tones. Tone is derived from consonant class, live/dead syllable type, vowel quantity where relevant, and written tone mark. Exact phonetic contours are analysis-dependent across descriptions and are therefore not treated as universally fixed surface measurements.

## Ukrainian output

The executable target boundary is a typed `PhoneticResult`; the Ukrainian adapter consumes only its registered IPA segments and metadata. `UNCERTAIN` segmental readings and `UNSUPPORTED` IPA are withheld rather than mapped from Lao spelling or partial IPA. Tone uncertainty is independent: when segmental IPA is supported, the Ukrainian form may be produced while tone remains unresolved in metadata. The current Lao engine does not claim an independent broad-surface IPA layer. See [the adapter contract](ipa-to-ukrainian-adapter.md).



The practical layer deliberately neutralizes several source-language distinctions that Ukrainian orthography does not naturally preserve:

- aspiration of /kʰ pʰ tʰ/ is retained in IPA but not represented as `х`;
- /h/ is approximated by `г`, explicitly as a project decision rather than phonemic identity;
- /ɯ/ is approximated by `и`;
- /tɕ/ is represented by `ч`;
- vowel length is not automatically doubled.

These are project decisions, not an official Ukrainian national standard.
