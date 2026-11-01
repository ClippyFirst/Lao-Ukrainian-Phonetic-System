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


## Exact-head three-repeat runtime evidence — 2026-11-01 (supersedes prior counts)

The exact current PR #96 head `bca9d4a802be0e873bef34618da78bd73cd6eb79` was executed in GitHub Actions, including a clean pinned-source Go build and three HTTP requests per input.

- Runtime workflow: [41310804516](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41310804516); artifact [13085003615](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41310804516/artifacts/13085003615); ZIP SHA-256 `025e5444d0a096ca07c39cbf9297ef4229275937ff487d38548fd3a551269612`.
- Engine `b224bde02151f8f86d0fe260804e4ca743bda620`, Go `1.23.12`, language `Lao`, effective config SHA-256 `afdab11396e77d171fd4683c8692dbe8513edfe6ed02aa3a20bac9db9f11c44c`.
- Engineering probes: 18/23 had usable output; 5/23 returned no phonetic output. Of the 18, 8 were identical across all three repeats and 10 were unstable.
- MekongPhon `lao_eval.csv`: 81/100 had usable output; 19/100 returned no output. 68 were identical across all three repeats; 13 were unstable.
- Strict source-attested concordance requiring all three repeats to match: **2/100 (2%)**. At least one repeat matched for 9/100. No limited-notation normalization increased the strict count. These are source-attested concordance diagnostics, emphatically not accuracy or gold agreement.
- Examples of variability include `ຂາ` alternating between `kʰaː˥˧˧` and `kʰaː˩˧`, and `ຄົນ` returning both `kʰon˧˥` and `kʰon˩˨`. Tone is not discarded or normalized away.
- The server logs `weights9.bin.zlib: file does not exist`; the pinned tree has `weights8.bin.zlib` but no `weights9.bin.zlib`. The loader path and causal relation to empty/unstable outputs remain unproven.

This exact-head run supersedes earlier 4%, 5%, and 8% figures in this audit. **Disposition remains: reject Goruut for production use; retain only as an optional raw-output research comparator.** Independent adjudicated Lao gold remains 0.


## Upstream cause of nondeterministic dictionary selection — Lao

Pinned Goruut source explains the instability signal. In [parts_of_speech_selector_service.go](https://github.com/neurlang/goruut/blob/b224bde02151f8f86d0fe260804e4ca743bda620/repo/services/parts_of_speech_selector_service.go#L168-L205), `SelectE` counts multiple dictionary pronunciations for a word; when more than one exists it increments the escape counters. If the homograph selector has not marked a `preferred` pronunciation, the fallback loop iterates the dictionary mapping and selects a dictionary pronunciation; the upstream source comment explicitly describes this as random selection when no homograph model is available. The [sentence use case](https://github.com/neurlang/goruut/blob/b224bde02151f8f86d0fe260804e4ca743bda620/usecases/phonemize_usecase.go#L84-L85) exposes those counters as `RandomizationWordsCount` and `RandomizationWordsChoices` in the HTTP response.

Across the latest artifact, all 10/10 unstable engineering inputs and all 13/13 unstable MekongPhon-eval inputs carried Goruut's RandomizationWordsCount / RandomizationWordsChoices metadata. Metadata appeared on 11/23 engineering inputs and 17/100 eval inputs; not every ambiguous input changed across the three samples. The response metadata is therefore a direct upstream signal for the observed instability, not an inference from output differences alone.

This gives a source-level explanation for the observed unstable cases. It does **not** establish that the separate `weights9.bin.zlib` warning causes the selection behavior; that warning remains independently unresolved. The project does not patch Goruut or choose a random pronunciation as acceptable output. Any result carrying these ambiguity counters should remain flagged as non-deterministic/ambiguous for downstream use.


## Source-coverage re-analysis of the exact-head artifact — 2026-11-01

A second inspection of the saved raw JSON used the API's `PrePunct`, `CleanWord`, and `PostPunct` fields, not just its non-empty `Phonetic` field. Coverage was counted complete only when (a) the concatenated source fields reconstructed the input after NFC and whitespace removal and (b) no letters, combining marks, or numbers appeared in PrePunct/PostPunct. This is a conservative source-coverage check, not phonetic correctness.

- MekongPhon eval: of 100 inputs, 81 had a phonetic response and 19 had none. Only **47/100** had complete source coverage; **34/100** had partial source coverage; 19/100 had no output. The 13 unstable cases were among the 47 complete-coverage outputs and all 13 carried Goruut's randomization counters. The 34 partial cases were stable but had dropped/relegated source characters.
- Engineering probes: 18 responses, 5 no-output; 13 complete coverage and 5 partial coverage. Ten complete-coverage cases were unstable; all ten carried randomization counters.
- This re-analysis shows that response count alone overstated usable coverage. The benchmark harness is being extended to report source coverage separately from response availability and IPA concordance.

Raw artifact: [13085003615](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41310804516/artifacts/13085003615), ZIP SHA-256 `025e5444d0a096ca07c39cbf9297ef4229275937ff487d38548fd3a551269612`.


## Independent repeated CI run — source-coverage and randomization variability

A second three-repeat run on the same pinned engine, same 100-row MekongPhon input SHA `5351af5ed545f68886a99f0e8d88c91fdbdf46c4df885d40e166b8a3b32cd241`, and same config SHA `afdab11396e77d171fd4683c8692dbe8513edfe6ed02aa3a20bac9db9f11c44c` produced a different phonetic result profile:

- Run [41312511636](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41312511636), artifact [13085893546](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41312511636/artifacts/13085893546), ZIP SHA-256 `76fba836abbafcc6ffe9c153da46e895f9b97a2dd8677b070a59c1b5857225d7`.
- 81/100 responses; 19 no output. Source coverage: 47 complete, 34 partial, 19 unknown/no output (same coverage split as prior run).
- Reproducibility changed: 66 stable, 15 unstable (prior run: 68 stable, 13 unstable). 17/100 inputs carried dictionary-randomization metadata across 51 repeat responses; all 15 unstable cases were flagged.
- Strict all-repeat source-attested concordance changed from 2/100 in the prior artifact to **3/100**; at-least-one-repeat matches changed from 9/100 to **10/100**. Neither is accuracy; this run-to-run movement is itself evidence that the random homograph fallback makes the comparator unsuitable for stable scoring.
- Engineering probes: 13/23 complete coverage, 5/23 partial coverage, 5/23 no output; 7/18 returned outputs were unstable and all 7 had randomization metadata.

The new report contract therefore correctly separates response availability, source coverage, randomization ambiguity, repeat stability and source concordance. No score is promoted to accuracy.


## Final exact-head verification — 2026-11-01

The final PR #96 head `168bb118d69c3ddc4c9c406f517cd2a93857dda0` completed both required workflows:

- Repository verification [41313419948](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41313419948): PASS. The job completed the repository data/evidence audit, Python tests, optional external-G2P harness syntax/CLI checks, browser engine tests, canonical browser-data build/regeneration, generated-data drift check and built-page/relative-asset checks.
- Pinned Goruut runtime [41313419967](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41313419967): PASS. It built pinned Goruut commit `b224bde02151f8f86d0fe260804e4ca743bda620` with Go 1.23.12, explicitly enabled Lao and captured three repeats per input.
- Artifact [13085974013](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41313419967/artifacts/13085974013), ZIP SHA-256 `c0e61794e98941be9a2e6449fc5f2052f9f5ead20abf366ea09d98881b45c850`; downloaded archive hash independently recomputed and matched GitHub's artifact digest. Input SHA-256 `5351af5ed545f68886a99f0e8d88c91fdbdf46c4df885d40e166b8a3b32cd241`; effective config SHA-256 `afdab11396e77d171fd4683c8692dbe8513edfe6ed02aa3a20bac9db9f11c44c`.

The final 100-row MekongPhon diagnostic produced 81 responses and 19 no-output cases. Source coverage was 47 complete, 34 partial and 19 unknown/no-output. Repeats were 68 stable and 13 unstable; 17 inputs carried dictionary-randomization metadata across 51 responses, and all 13 unstable inputs carried that metadata. Strict all-repeat source-attested concordance was 3/100; at least one repeat matched for 9/100. These are source-attested diagnostics, not accuracy; independent expert gold remains 0 and `accuracy` remains null.

The 23 engineering probes produced 18 responses (13 complete-coverage, 5 partial-coverage) and 5 no-output cases. Of the 18 returned outputs, 12 were stable and 6 unstable; 11 inputs carried randomization metadata and all 6 unstable inputs were flagged. The `weights9.bin.zlib` warning persists; its causal relationship to output failures is unproven.

**Disposition:** the exact-head code and optional experiment are verified; Goruut remains rejected for production. The benchmark harness/source-coverage gate is implemented and CI-tested. Expert-adjudicated Lao IPA gold, dialect-scoped accuracy, root-cause investigation of the model warning and phonetic remediation remain PARTIAL/BLOCKED.
