# Goruut runtime evaluation — Lao — 2026-11-01

## Execution

- Upstream: [neurlang/goruut](https://github.com/neurlang/goruut), pinned commit `b224bde02151f8f86d0fe260804e4ca743bda620`.
- Language identifier: `Lao`; explicitly enabled in `BuiltinDictLanguages` (the upstream sample config enables only Czech and Slovak).
- Runtime: Go 1.23.12, HTTP `POST /tts/phonemize/sentence`.
- Test-only checkout; no model/dictionary assets copied into this repository or production bundle.
- Effective config SHA-256: `afdab11396e77d171fd4683c8692dbe8513edfe6ed02aa3a20bac9db9f11c44c`.

## Results

1. Existing engineering probes: 23 requests, 18 usable phonetic responses, 5 empty `Words` responses. These are parser/coverage probes, not a representative lexical corpus.
2. MekongPhon evaluation split: pinned project commit `f80f6c1840c4818b51e05f2e00cded4701a5b662`, `data/splits/lao_eval.csv`, 100 rows. Goruut returned 81 usable outputs and 19 no-output responses.
3. Strict NFC/outer-whitespace-only concordance with the split's `pron_with_tones`: 8/100 exact (8%). This is **source-attested concordance only, not accuracy**: MekongPhon sentence IPA is dictionary-generated, the underlying project has no declared corpus license, and its 100-row lexical split is not an independently adjudicated expert gold set.
4. Heuristic decomposition of the 100 comparisons (diagnostic only): 8 exact; 13 become equal after removing tone letters only; 1 after removing tone/length; 59 segmental/format differences; 19 no output. Tone stripping is not an accepted score and tonal distinctions remain significant.
5. Example: `ຂາ` — MekongPhon `kʰaː˩˧`; Goruut `kʰaː˥˧˧`. This is a tone disagreement, not a harmless normalization.
6. The Goruut server log repeatedly reports `weights9.bin.zlib: file does not exist`. This suggests an unresolved model-asset/runtime path issue; the response count alone must not be interpreted as full G2P coverage.

## Interpretation

**Do not integrate Goruut as the Lao production phonology provider.** It is useful as an optional raw-output comparator and currently demonstrates some lexical coverage, but the 8% source-attested strict concordance, 19% missing outputs, tone differences and missing-weight warning are substantial blockers. The source-attested corpus itself is not gold, so neither 8% nor the diagnostic categories are an accuracy estimate.

## Evidence and artifacts

- Optional runtime workflow: [41307986513](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41307986513) (initial completed runtime comparison); latest exact-head run is tracked by PR #96.
- Artifact contains both engineering and MekongPhon reports plus the server log; retention is 30 days.
- Current independent, project-owned, expert-adjudicated Lao gold remains 0.
