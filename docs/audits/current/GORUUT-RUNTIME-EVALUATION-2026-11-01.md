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


## Repeatability follow-up — supersedes one-shot figures — 2026-11-01

The final diagnostic sends each input three times to the same running server. The earlier one-shot 8%/9% concordance figures are superseded by this stricter repeated-request result:

- Engineering probes: 23 inputs; 18 had at least one usable output, 5 had no output. Of the 18 with outputs, 11 were identical across all three repetitions and 7 changed between repetitions.
- MekongPhon eval: 100 inputs; 81 had at least one usable output, 19 had no output. 68 outputs were identical across all three repetitions; 13 changed between repetitions.
- Strict source-attested exact concordance across all three repetitions: 4/100 (4%). At least one of the three repetitions matched for 10/100 (10%); these are not interchangeable measures. The comparison remains non-gold and not accuracy.
- Observed variability is often tonal: e.g. `ຄົນ` returned both `kʰon˩˨` and `kʰon˧˥` in repeated requests; `ເກືອ` alternated tone contours. This is a reproducibility blocker for deterministic transcription.
- The same input can also vary across separate CI runs; e.g. `ຂາ` returned different tone contours in earlier runs.

Latest three-repeat artifact: [workflow 41309088407](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41309088407). Engineering fixture SHA-256 `a3cdf11fc00e87380787ae2fbf421c83de697cf98c66078414a2c99c81dccd19`; MekongPhon eval SHA-256 `5351af5ed545f68886a99f0e8d88c91fdbdf46c4df885d40e166b8a3b32cd241`; effective config SHA-256 `afdab11396e77d171fd4683c8692dbe8513edfe6ed02aa3a20bac9db9f11c44c`; server log SHA-256 `5c5885c2362ebdce977d7837cc1d3ce7e3fb08bdd17445ede7bda3683377e1ad`.

**Disposition remains: do not integrate as a production phonology provider.** Three-repeat output instability plus 4% strict source-attested concordance is insufficient for production use. The MekongPhon split is still not expert gold.


## Additional comparator: lao2ipa 1.0.0 — 2026-11-01

The existing optional external comparator was also executed on the 37-case engineering fixture:

- Project output matched its own engineering fixture: 37/37.
- `lao2ipa==1.0.0` output matched the project fixture: 0/37.
- Exact string agreement between project output and lao2ipa: 0/37; no runtime errors.
- Heuristic difference decomposition: 31 tone-suffix-only, 2 diphthong offglide convention, 4 segmental/vowel-sequence differences. Tone-stripped agreement is 31/37 (83.8%) diagnostic-only.
- This does not establish the project output as correct: the 37-case fixture is an engineering regression fixture, not independent expert gold. The external package's tone output differs systematically from the project's tone-less default, and six cases need segmental/convention review.

Evidence: [optional comparator workflow 41310116216](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41310116216). Package version `1.0.0`; independent gold remains 0.

## Latest three-repeat Goruut report — 2026-11-01

The most recent pinned run supersedes the earlier repeat counts: engineering probes 18/23 usable, 12 reproducible and 6 unstable; MekongPhon 81/100 usable, 70 reproducible and 11 unstable. Strict and limited-notation source-attested concordance across all three repetitions is 5/100 (5%); 10/100 matched in at least one repetition. This is still not gold or accuracy. Latest run: [41310116195](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41310116195). Server log SHA-256 `1a4b77036d9e3e2c275f5604e55f0e2c935ba755ed380e1cfcc94a292471877a` (engineering) and `90641614476946b5a8de27cd72fe480d78746d1d9b55b1b5158fdc7582c979d3` (MekongPhon).


## Model-asset warning interpretation

The runtime log warning is now more precisely classified: the pinned Goruut language module contains `weights8.bin.zlib`, while the runtime repeatedly logs an attempt to open `weights9.bin.zlib`. No `weights9.bin.zlib` asset was found in the pinned repository tree. The exact loader path and causal relation to empty outputs/tone instability have not been established; treat this as an unresolved upstream asset/version warning, not a proven root cause.
