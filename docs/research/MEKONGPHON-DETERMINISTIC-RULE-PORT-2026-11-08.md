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

Browser-engine API:

```js
analyze("ດວງ", { ipaProfile: "mekongphon-reference" })
```

The visible browser UI intentionally remains on the default Vientiane profile; this option is exposed by the engine API, not as a user-facing selector.

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

| Structural unit | Existing ClippyFirst IPA | MekongPhon reference IPA | Dominant train agreement |
|---|---|---|---:|
| `AW_LONG` | `aw` | `ao` | 534/549 (97.3%) |
| `UA_LONG` | `ɯːə` | `ɯːə̯` | 459/471 (97.5%) |
| `IA_LONG` | `iːə` | `iaː` | 275/281 (97.9%) |
| `OEE` | `ɤː` | `əː` | 212/234 (90.6%) |
| `AI` | `ai` | `aj` | 205/205 (100%) |
| `UO_LONG` | `uːə` | `uaː` | 184/188 (97.9%) |
| `UO_LONG_ALT` | `uːə` | `uaː` | 180/184 (97.8%) |
| `AI2` | `ai` | `aj` | 158/163 (96.9%) |
| `OE` | `ɤ` | `ə` | 86/92 (93.5%) |
| Onset `ວ` | `ʋ` | `w` | 330/333 (99.1%) |
| Onset `ຣ` | `l` | `r` | 172/175 (98.3%) |

These mappings are dominant aggregate correspondences, not exception-free laws. The profile applies them by structural vowel ID and onset grapheme; the remaining minority alignments are deliberately not turned into word-level exceptions. `OEE` and `OE` have the lowest agreement in this set (90.6% and 93.5%), so they remain opt-in. In particular, the `ຣ` difference may involve lexical/loanword or transcription conventions, and the `ວ` difference is a phonetic-profile distinction; neither is silently promoted to the default Vientiane rule set.

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
- Successful run: [workflow run 42467190935](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42467190935), code checkpoint `e46b0cafa9c1b2d47c746d4258e3b1d624e26d7c`.
- Aggregate artifact ID: `13612311669`; SHA-256 `5471b2f8d4c1d599fe881811ca8d31c326c0d79b2929b859100ca086af83a329`.

### Held-out result (one CPU run)

| Engine | CER, full 100 | Exact matches | Coverage |
|---|---:|---:|---:|
| ClippyFirst Vientiane rules | 11.46% | 69/100 | 97% |
| ClippyFirst MekongPhon-reference rules | **6.64%** | **90/100** | 97% |
| MekongPhon non-tonal neural | 6.64% | 82/100 | 100% |

On the identical 97-word coverage subset, the deterministic profile has CER **1.40%** (8 edits / 570 reference code points), versus **5.79%** (33 / 570) for MekongPhon Neural. The profile has 90 exact matches and the neural model 81 on this shared subset. The profile's predictions differ from neural predictions by 5.17% CER on those 97 words; the goal is reference agreement, not imitation of every model output.

One-run mean inference time, model load excluded: baseline rules 1.75 ms/input, reference profile 1.38 ms/input, neural 58.08 ms/input. Runtime errors: 0. These are single-run measurements, not stable performance guarantees.

The profile retains the baseline's 97% coverage. Aggregate withheld-warning counts are `UNCONSUMED_AFTER_VOWEL: 3` and `MALFORMED_TONE_MARK_ORDER: 1`; no neural fallback is used. These cases remain withheld rather than guessed. They require independent structural/orthographic evidence before any new parser rule is accepted.

This held-out set is dictionary-seeded secondary reference material, not independently adjudicated project gold. Its scores measure agreement with that reference, not universal phonetic accuracy.

## Limitations and acceptance boundary

- The profile is a finite deterministic approximation of a subset of repeated reference conventions; it cannot reproduce the neural model's learned sequence-level generalization.
- Contexts not covered by an explicit override retain the ordinary ClippyFirst rule result.
- The default `vientiane` profile is unchanged.
- Tone remains the existing source-scoped deterministic rule matrix; no tone override is inferred from the 100-row evaluation set.
- Ukrainian target adaptation remains a separate IPA-consuming stage and can still withhold IPA symbols without an approved target correspondence.
- Independent adjudicated Lao IPA gold remains 0. No empirical accuracy or production-readiness claim follows from this experiment.

Promotion criterion: retain this profile as an opt-in compatibility mode unless the held-out benchmark shows a repeatable improvement without reducing IPA validity/coverage, and do not replace the default dialect profile without qualified Lao phonetics review.
