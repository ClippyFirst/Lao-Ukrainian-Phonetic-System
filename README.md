# Lao → Ukrainian Phonetic-Graphemic Correspondence System

Research-oriented, machine-readable system for deriving a practical Ukrainian representation from Lao through phonology and IPA.

## Central principle

**Lao Unicode → graphemic structure → syllable analysis → consonant class → vowel/length → live/dead → tone → phonology → IPA → Ukrainian target → practical Ukrainian orthography**

This is not Lao-character → Ukrainian-character substitution and not Lao → romanization → Ukrainian.

## Comparative Cyrillic layer

The repository explicitly compares the Lao Russian practical tradition with Ukrainian and uses Serbian/Bulgarian materials as target-script controls.

Main project-level divergences:

- /kʰ pʰ tʰ/ → Ukrainian к п т rather than Russian кх пх тх;
- /h/ → Ukrainian г rather than Russian х;
- /ŋ/ → нг;
- /tɕ/ → ч rather than Russian ть;
- /ɯ/ → и rather than Russian ы;
- vowel quantity remains analytical rather than automatically doubling vowels.

These are project policies, not an official Ukrainian national standard.

## Repository

- src/lao_ukrainian/ — parser, phonology, tone and target pipeline;
- data/lao/ — Lao registries;
- data/comparative/ — Russian/Serbian/Bulgarian/Ukrainian comparison;
- data/evidence/ — sources and claims;
- docs/ — methodology and audit;
- tests/ — regression tests.

## Scope

Primary reference: contemporary Standard Lao with a Vientiane-oriented analysis where supported. Regional and historical varieties remain source-specific.

## Canonical Ukrainian target

ClippyFirst/Ukrainian-Phonetic-Inventory is the canonical Ukrainian inventory. This repository does not duplicate it.

## Status discipline

The system distinguishes ESTABLISHED, PROJECT-POLICY, ANALYSIS DEPENDENT, EVIDENCE LIMITED and TRADITIONAL. It does not invent calibrated probabilities or empirical accuracy percentages without a versioned gold corpus.

## Usage

    pip install -e .
    lao-ua "ຂາ"
    lao-ua "ໄກ່" --json
