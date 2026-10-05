# Product Requirements — Lao → Ukrainian Web Service

## 1. Product definition

A local-first, research-oriented web interface for the Lao → Ukrainian Phonetic-Graphemic Correspondence System.

The product has exactly two main pages:

1. **Service** — paste Lao text and receive the project's practical Ukrainian representation with IPA and explainability.
2. **Author's system** — methodological documentation of the project's own Lao → Ukrainian system.

This is a transcription/correspondence instrument, not a translation service.

## 2. Linguistic pipeline

Lao Unicode → graphemic structure → syllable analysis → consonant class → vowel/length → live/dead → tone → phonology → IPA → Ukrainian target → practical Ukrainian orthography.

The primary method must not be Lao → Latin romanization → Ukrainian.

## 3. Service requirements

- Lao input with example and clear controls.
- Primary result labelled **Український запис**.
- IPA shown as an analytical layer.
- Per-syllable explanation: onset, consonant class, vowel, syllable type, tone, mapping.
- Warnings for unresolved or analysis-dependent cases.
- Copy controls.
- No invented certainty.
- Local processing; no account, database, analytics, telemetry, ads, or user-text upload.
- Keyboard-accessible and usable on mobile and zoomed layouts.

## 4. Author-system page

Explain, in order:

1. What the system is.
2. Why direct letter substitution is inadequate.
3. Lao script and structural order.
4. Consonant classes.
5. Vowels and quantity.
6. Live/dead syllables.
7. Tone.
8. IPA as the central analytical layer.
9. Ukrainian target rules.
10. Differences from Russian practical tradition.
11. Worked examples.
12. Scope and limitations.

Explicitly label project decisions as **PROJECT-POLICY** rather than an official Ukrainian national standard.

## 5. Visual requirements

The design follows the Chinese project's functional, data-first philosophy while establishing a distinct Lao identity:

- deep Lao red as structural accent;
- dark Lao blue as primary navigation/interaction accent;
- white and warm neutral paper surfaces;
- typography and hierarchy before decoration;
- restrained borders and tables;
- no gradients, glowing AI cards, tourism imagery, flags-as-decoration, dashboards, pricing, login or marketing sections.

## 6. Technical requirements

- Static Vite frontend.
- Deterministic client-side conversion for the documented web subset.
- Linguistic rules kept in a dedicated module, not scattered through UI code.
- Stable analysis object shape suitable for later connection to the Python core/API.
- Unit tests for analyzer helpers.
- Browser tests for the two-page flow, conversion, copy, clear, example, keyboard navigation and responsive structure.
- Production build must succeed.

## 7. Definition of done

The repository must contain the two-page web product, documented design and architecture decisions, a working local-first service, methodology content, tests, build/release documentation, and no claims of empirical accuracy beyond the available evidence.
