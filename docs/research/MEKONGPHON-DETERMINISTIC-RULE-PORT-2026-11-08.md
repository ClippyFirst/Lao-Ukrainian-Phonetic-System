# Deterministic MekongPhon-reference IPA profile — 2026-11-08

## Purpose

This is a **deterministic compatibility experiment**, not a neural-network port and not a new universal description of Lao phonology.

MekongPhon is a character-level encoder-decoder model. Its learned weights and sequence-level behavior cannot be converted into a finite list of linguistic rules without loss. What can be transferred is a subset of stable, repeated orthography/context-to-IPA correspondences visible in its separate training split.

ClippyFirst therefore keeps its existing Vientiane-oriented deterministic rules as the default and adds an explicit opt-in profile:

`analyze(text, ipa_profile="mekongphon-reference")`

CLI:

```bash
lao-ua "ດວງ" --engine rules --ipa-profile mekongphon-reference --json
```

The profile still follows the same architecture:

`Lao orthography → structural analysis → deterministic source IPA → typed IPA → Ukrainian adaptation`

It does not invoke PyTorch, download model weights, call the neural adapter, or fall back to a neural model.

## Training evidence and extraction

- Source: BYU MATRIX Lab MekongPhon, immutable repository revision `f80f6c1840c4818b51e05f2e00cded4701a5b662`.
- Split: `data/splits/lao_train.csv`, 6,219 word-level records.
- SHA-256: `2d0f68989009620980ced3386f11a640e6167404308eeb6a79efc52bc8e40ee0`.
- Aggregate grapheme/context diagnostic: [run 42390734319](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42390734319), artifact SHA-256 `7d51559fc9d5ef7d173850d9237cbd62577c2b7b890e96d1e73a6f113d46938a`.
- No raw training words, IPA reference rows, or per-item predictions are committed by this profile.

The profile takes only high-frequency correspondences that recur across the separate train split. It does not use the 100-row evaluation split to select or tune any mapping.

## Transferred correspondences

The following are reference-convention differences observed in the training split. Counts are aggregate aligned contexts, not independent human judgments.

| Structural unit | Existing ClippyFirst IPA | MekongPhon reference IPA | Train observations |
|---|---|---|---:|
| `AW_LONG` | `aw` | `ao` | 534 |
| `UA_LONG` | `ɯːə` | `ɯːə̯` | 459 |
| `IA_LONG` | `iːə` | `iaː` | 275 |
| `OEE` | `ɤː` | `əː` | 212 |
| `AI` | `ai` | `aj` | 205 |
| `UO_LONG` | `uːə` | `uaː` | 184 |
| `UO_LONG_ALT` | `uːə` | `uaː` | 180 |
| `AI2` | `ai` | `aj` | 158 |
| `OE` | `ɤ` | `ə` | 86 |
| Onset `ວ` | `ʋ` | `w` | recurrent across contexts |
| Onset `ຣ` | `l` | `r` | recurrent across contexts |

These mappings are applied only when the user explicitly selects the reference profile. In particular, the `ຣ` difference may involve lexical/loanword or transcription conventions, and the `ວ` difference is a phonetic-profile distinction; neither is silently promoted to the default Vientiane rule set.

The profile leaves tone selection, live/dead classification, syllable segmentation, unsupported-material handling and uncertainty policy unchanged. It records every applied override in the per-syllable provenance list.

## Held-out evaluation

A separate hosted workflow compares three outputs on the frozen 100-entry `lao_eval.csv` split:

1. Default ClippyFirst Vientiane rules.
2. ClippyFirst deterministic `mekongphon-reference` profile.
3. MekongPhon non-tonal model at immutable revision `d6ea20cb73eaab8f3adc4eb044e61bdb9bef3f5b`, beam width 5.

The benchmark reports full-denominator CER, exact matches, coverage, identical-coverage metrics and profile-vs-neural IPA CER. It stores aggregate metrics only.

- Held-out split SHA-256: `5351af5ed545f68886a99f0e8d88c91fdbdf46c4df885d40e166b8a3b32cd241`.
- Script: `scripts/benchmark_mekongphon_deterministic_profile.py`.
- Workflow: `.github/workflows/mekongphon-deterministic-profile-benchmark.yml`.

This held-out set is dictionary-seeded secondary reference material, not independently adjudicated project gold. Its scores measure agreement with that reference, not universal phonetic accuracy.

## Limitations and acceptance boundary

- The profile is a finite deterministic approximation of a subset of repeated reference conventions; it cannot reproduce the neural model's learned sequence-level generalization.
- Contexts not covered by an explicit override retain the ordinary ClippyFirst rule result.
- The default `vientiane` profile is unchanged.
- Tone remains the existing source-scoped deterministic rule matrix; no tone override is inferred from the 100-row evaluation set.
- Ukrainian target adaptation remains a separate IPA-consuming stage and can still withhold IPA symbols without an approved target correspondence.
- Independent adjudicated Lao IPA gold remains 0. No empirical accuracy or production-readiness claim follows from this experiment.

Promotion criterion: retain this profile as an opt-in compatibility mode unless the held-out benchmark shows a repeatable improvement without reducing IPA validity/coverage, and do not replace the default dialect profile without qualified Lao phonetics review.
