# Final scientific audit

## Reconstructed state

The repository is now one coherent Lao → Ukrainian research project. The active architecture contains implementation, canonical Lao registries, a canonical Ukrainian correspondence registry, comparative evidence, provenance data, tests, and explicit research documentation.

No obsolete/foreign/temporary files were identified in the inspected tree. The repository did not contain a separate historical research corpus that required destructive deletion; therefore no research evidence was archived or deleted during this pass.

## Corrective work

- Replaced the initial substring-based vowel detection with explicit structural Lao vowel patterns.
- Corrected the distinction between short and long preposed vowels such as ເກະ vs ເກ.
- Corrected long /ɔː/ representation through ກໍ / the Niggahita-based pattern.
- Added a Vientiane live-syllable tone fallback independent of short/long vowel length when a sonorant coda is present.
- Treated ອ as a tone-class vowel carrier rather than automatically inserting an IPA /ʔ/ before every overt vowel.
- Added deterministic repository auditing and derived-data generation scripts.
- Expanded public documentation and explicit limitations.
- Strengthened source provenance with Unicode, W3C Lao layout guidance and Ueda's DOI.

## Not claimed

- an official Ukrainian national standard;
- complete automatic segmentation of unspaced Lao text;
- complete initial-cluster analysis;
- complete independent tonal rules for every use of ໜ/ໝ;
- a full Pali/Sanskrit transcription system;
- calibrated probabilities or empirical accuracy percentages;
- a complete lexical corpus or expert-adjudicated gold standard.

The Russian system remains a comparator, not an intermediate representation. Serbian and Bulgarian remain target-script controls rather than invented Lao-specific standards.

## Current quality judgement

**🟡 Usable but needs finalization.**

The repository is substantially more defensible and reproducible than the initial research foundation, but publication-grade status requires a representative corpus, fuller syllable/cluster grammar, independent verification of edge cases, and expert adjudication of the Ukrainian target correspondences.


## External IPA and benchmark audit — 2026-10-24

- The external comparator `lao2ipa 1.0.0` has a reproducible 36-probe smoke run with 0 runtime errors. Latest categorized artifact: [run 40122329060](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40122329060), SHA-256 `2b7f3c5e3c02814413e42b9f2031849c21630fba9958a7e6a38de92f7a63ff55`.
- Strict raw IPA agreement is 0/36. A separate tone-letter-stripped diagnostic matches 29/36 (80.6%), leaving 7 tone/length/segmental/offglide cases for review. This is a string-difference diagnostic, not accuracy; Lao tone can be contrastive and must not be stripped from production IPA.
- The benchmark gold-provenance guard is merged: every ADJUDICATED row requires non-empty IPA, source_id and profile. The independent gold corpus remains empty, so accuracy is null.
- External systems remain optional. Epitran (`lao-Laoo`) and Goruut are upstream support candidates only, not yet executed in this repository. Remaining acceptance criteria: expert-adjudicated lexical IPA, documented tone convention, and source-based review of the seven non-tone/format cases.


## Ukrainian target-policy audit — 2026-10-30

**Scoped status: DONE_VERIFIED.** The IPA-to-Ukrainian correspondence registry, Python adapter, generated browser data and tests now preserve aspiration and distinguish the requested Ukrainian consonants.

- Aspiration: /kʰ tʰ pʰ/ → к' т' п'; source IPA retains the aspiration feature.
- Distinctions: /h/ → г, /ɡ/ → ґ, /x/ → х.
- Affricates: /t͡s/ → ц, /d͡z/ → дз, /t͡ʃ/ → ч, /d͡ʒ/ → дж; Lao /tɕ/ and documented alveolo-palatal aliases map to ч/дж as explicit approximations.
- Palatalized consonants use Ukrainian soft-sign sequences only when the source analysis establishes palatalization. /ʔ/ is not aspiration.
- Canonical CSV → generated browser-data parity was checked; exact-head workflow [41075912762](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41075912762) passed.
- Changes are in draft PR #56; no merge or deployment was performed.

This does not establish a normative Ukrainian transcription standard or improve the independent Lao pronunciation gold set. The research corpus still has no independently adjudicated lexical IPA gold and accuracy remains unmeasured. The broader limitations listed above remain open.


## Optional romanization-to-Ukrainian result mode — 2026-10-30

- Added a two-method selector inside the primary Ukrainian result card. The IPA-first phonetic output remains the default and is unchanged.
- The first revision used a character-level Latin adapter. That revision is **superseded** after user review; do not treat its mapping table as the current implementation.
- Current implementation uses `web/romanization-syllable-engine.js`: it parses romanized onset, vowel nucleus and coda, validates each onset against the original Lao consonant grapheme, validates the nucleus against the source vowel ID, checks supported coda graphemes against CLDR forms, applies position-sensitive coda correspondences, and assembles Ukrainian syllables. The compatibility file `web/romanization-ukrainian.js` re-exports this engine and no longer implements character-by-character substitution.
- Corrected source-aware policy: BGN/PCGN `kh/th/ph` spell aspirated Lao stops and map to `к'/т'/п'`; standalone Lao `h` (/h/, ຫ/ຮ) maps to `г`. The BGN `x` spelling for ຊ maps to `с`, not `кс`; final `h` is rejected because it is not a supported Lao coda. BGN/PCGN note 5 explicitly says silent ຫ is omitted before sonorants and that ໜ/ໝ are abbreviated forms of ຫນ/ຫມ. The adapter applies this to supported written forms ຫງ/ຫຍ/ຫນ/ຫມ/ຫລ/ຫຼ/ຫວ and atomic ໜ/ໝ, retaining the underlying sonorant rather than an audible `h`; BGN's /r/ case is still unsupported by the structural parser. Ambiguous, mismatched or unsupported syllable segmentation is retained in visible brackets and marked partial.
- Evidence sources for the romanization layer are registered in `data/evidence/sources.csv`: the provisional CLDR transform and the EKI/UNGEGN report for BGN/PCGN 1966. The report states that Lao has no UN-approved romanization system and no national romanization system. The CLDR transform itself leaves special final-consonant handling as TODO.
- The earlier engineering verification at commit `753b82c89076b2e23fbbcd937df45bf4289b7dfc` remains historical evidence for the prior adapter only. The corrected source-vowel and nasal-ligature crosswalk is verified at implementation head `d0b9a585a3edf2ad0c89ba9f9b10fcbc35aa62e6` by [workflow 41137893545](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41137893545): repository audit passed (43 consonant rows, 34 vowel rows, 17 tone rules, 69 Ukrainian mappings, 20 evidence sources and 44 claims; all references resolved); Python 92; browser engine 46; romanization integration 19; syllable crosswalk 27; web layout 5; external-G2P harness syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks all passed. The workflow assertion for the versioned app module URL was updated to accept the cache-busting query string; the built relative path remains verified.
- This verifies deterministic behavior for the implemented subset, not linguistic accuracy or full CLDR coverage. It does not change the independent IPA gold-corpus count (still zero). Manual visual/keyboard QA remains open; PR #65 remains unmerged and the feature has not been deployed.


### Source-vowel and high-class nasal crosswalk — 2026-10-31

- Added `LAO_VOWEL_TO_CLDR` source mapping for the implemented vowel subset. The browser app passes the IPA-first structural parser's `VOWEL:<ID>` rule identity as evidence; the romanization result itself is still generated independently from CLDR syllable parsing and does not consume IPA.
- The crosswalk checks source onset, source vowel ID and supported source coda. It resolves homographic `kam` from source structure (A + coda m versus AM nucleus), and resolves `niav` as ໜ + IA_LONG + final ວ only when the Lao syllable evidence is available. Without that evidence, ambiguous parses remain PARTIAL.
- Added the official UK government BGN/PCGN 1966 agreement to the evidence registry. Its note 5 establishes silent-`h` omission and the abbreviated ligature forms ໜ/ໝ; these are now correctly treated as n/m, not as h+n/h+m.
- Added explicit tests for source vowel mismatch, nasal ligature mapping, source-resolved `niav`, and the full `ເຂົ້າໜຽວ` source. The exact-head workflow above passes all gates.
- This remains a bounded romanization adapter, not an accuracy-certified transcription standard. The romanization collapses vowel length and does not preserve tone; unsupported source vowel patterns remain partial. Manual visual/keyboard QA and an independently adjudicated linguistic gold corpus remain open.

## Ukrainian target sequence completion — 2026-10-31

- Added the exact IPA sequence mapping /ʃt͡ʃ/ → щ to the canonical target correspondence registry. The Python adapter and browser mirror use longest-match selection, so this sequence is handled as the Ukrainian orthographic unit while isolated /ʃ/ → ш and /t͡ʃ/ → ч remain separate.
- Added source records for the Encyclopedia of Modern Ukraine article “Щ” (2025) and the Journal of the International Phonetic Association description of Ukrainian (2016), plus the source-linked claim `CLM-UA-SHCH-SEQUENCE`.
- Added regression coverage for the sequence and the individual postalveolar fricatives, retaining explicit tests for /h/ → г, /ɦ/ → г, /ɡ/ → ґ, /x/ → х, /t͡s/ → ц, /d͡z/ → дз, /t͡ʃ/ → ч and /d͡ʒ/ → дж.
- This is a target-language orthographic crosswalk decision. It does not assert that Lao contains /ʃt͡ʃ/ or alter Lao source phonology.

### Exact-head verification — Ukrainian target sequence extension

The implementation in 3d0d71cc505695eb9e7e0dc5b60f40227cc79565 passed [workflow 41140937597](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41140937597). The audit reported 43 consonant rows, 34 vowel rows, 17 tone rules, 70 Ukrainian mappings, 22 evidence sources and 45 claims; all claim/source references resolved. Python 94, browser engine 47, romanization integration 19, syllable crosswalk 27 and web layout 5 passed. External-G2P harness syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks passed. The test-first failure is retained in workflow [41140800731](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41140800731).

## Reconciliation audit — 2026-10-31

- Current base: `main` at `d64e201f6d417c71e3437daccfa465ddb77e224f`. UI PRs #61–#64 and shared Ukrainian target PR #56 are merged; their changes are already present in the base. The previously open PR #56 branch has no additional target-registry or target-spec changes to port. No duplicate work was added.
- Active feature: PR #65, `feat/romanization-ukrainian-mode-20261030`, remains open and unmerged. Its current exact head `fdd1ddacedc5a82890431384877182e00af3aba3` passed the push-triggered `verify` workflow [41142627085](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41142627085): audit, Python 94, browser 47, romanization integration 19, syllable crosswalk 27, web layout 5, optional G2P harness syntax/CLI, build, generated-data reproducibility, and built-page/relative-asset checks.
- Current `main` head `d64e201f6d417c71e3437daccfa465ddb77e224f` passed its own Pages deployment workflow [41117044318](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41117044318); both build and deploy jobs succeeded. This does not deploy the unmerged PR #65 branch.
- The target mapping extension `/ʃt͡ʃ/ → щ` is verified as a longest-match target orthography sequence; it does not claim a single source affricate. The IPA-first route remains the default, and the romanization route remains explicitly provisional and bounded.
- Release/readiness judgement remains **research MVP / partial prototype**. Green engineering CI and Pages deployment do not close independent gold-corpus, expert target review, source adjudication, cluster grammar, full CLDR/ICU coverage, or visual/keyboard QA gates. No accuracy score is justified.


## Post-merge final audit — 2026-10-31

- PR #65 merged the source-aware syllable-level romanization-to-Ukrainian mode and exact Ukrainian `/ʃt͡ʃ/ → щ` target mapping to `main` at `b2e1187629829b4242aa2430a9901d264910eea1`. Main CI passed at [41142746494](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41142746494): Python 94, browser 47, romanization integration 19, syllable crosswalk 27, web layout 5, data/evidence audit, optional harness syntax/CLI, build and reproducibility.
- The initial Pages deployment failure at [41142746466](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41142746466) was an obsolete script-URL grep, not a build or browser regression. PR #66 aligned the Pages assertion with the already-correct `verify.yml` assertion; fix merged at `a001046462de564dd2cb89e9237caa221624163c`.
- Exact-main verification [41142874231](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41142874231) and exact-main Pages deployment [41142874311](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41142874311) both passed. Pages build, artifact assertions, upload and deploy succeeded.
- PRs #56, #61–#65 and #66 are merged. Relevant changes from the earlier target-policy and interface branches were already in main; no duplicate code was introduced. No force-push or branch deletion occurred.
- Remaining release blockers are scientific and manual, not CI: independent expert review of the full Ukrainian target inventory; source-by-source Lao vowel/tone/coda/cluster adjudication; a licensed, versioned, expert-adjudicated IPA gold corpus (currently 0 rows); complete CLDR/ICU romanization coverage including unsupported `ຫຣ`; and real-browser visual/keyboard QA at 1440px, 768px and 390px.
- Quality judgement: **research MVP / partial prototype, deployed but not publication-grade or production-ready**. The test suite verifies implementation contracts and reproducibility; it does not prove phonological accuracy. No empirical accuracy percentage is reported.

## Public status reconciliation — 2026-10-31

The homepage and methodology were corrected to match the merged implementation and latest verified deployment. The stale status date and broad wording about `ໜ/ໝ` were corrected: the romanization adapter supports a bounded subset of silent-`ຫ` and ligature spellings, while complete phonological/tone analysis remains open. The homepage now explicitly names the Ukrainian `/ʃt͡ʃ/ → щ` target sequence and the separate source-aware romanization method.

Exact-head workflow [41183960495](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183960495) passed the full repository audit, Python 94, browser 47, romanization integration 19, syllable crosswalk 27 and web-layout 6 tests, plus harness syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks. Test-first stale-copy failure is preserved in [41183451808](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183451808).

Quality status remains **deployed Research MVP / partial prototype**. Independent expert-reviewed Lao IPA gold remains 0 and accuracy remains unmeasured/null. Real-browser visual/keyboard QA, expert target review, source adjudication and complete CLDR/ICU coverage remain open. This documentation update is not evidence of phonological accuracy.
## Post-merge exact-main verification and Pages deployment — 2026-10-31

PR #68 merged as `6293f52848b675ff53c2a1d191cdcbca3cb034b4`. Exact-main verification [41183960495](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183960495) passed: repository audit (43 consonants, 34 vowels, 17 tone rules, 70 Ukrainian mappings, 22 sources, 45 claims); Python 94; browser engine 47; romanization integration 19; syllable crosswalk 27; web layout/status 6; optional external-G2P harness syntax/CLI; production build; generated-data reproducibility; built-page and relative-asset checks.

GitHub Pages deployment [41183960573](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183960573) passed both build and deploy jobs. This confirms the updated public status copy is deployed. It does not complete visual screenshots, keyboard-only QA, or phonological adjudication. Independent gold remains 0 and accuracy remains null.
## PR #69 post-merge verification and deployment — 2026-10-31

PR #69 merged as `8664d800c683af28b2af840027844d53471d25d3`. Its exact-head verification [41183931581](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183931581) passed. Exact-main verification [41183960495](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183960495) passed the full audit, Python 94, browser engine 47, romanization integration 19, syllable crosswalk 27, web layout/status 6, optional external-G2P harness syntax/CLI, production build, generated-data reproducibility and built-page/relative-asset checks.

Pages deployment [41183960573](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183960573) passed both build and deploy jobs. README now points to stable workflow histories, avoiding a run-specific 'latest deployment' claim. No phonological or romanization runtime behavior changed; gold remains 0 and accuracy remains null.


## Agent workflow and CI hygiene — 2026-10-31

- Added the root `AGENTS.md` as the project-specific operating guide. It keeps the existing master handoff canonical, records the Lao→IPA→Ukrainian invariants, test/evidence rules, branch hygiene, and links the requested external engineering references at pinned commits.
- The selected practices were inspected from Superpowers (test-first development, systematic debugging, verification before completion), Matt Pocock's skills (deep modules, public test seams, behavior-oriented tests, source-backed research), and Ponytail (smallest complete diff, reuse before new dependencies, connected-code review, explicit debt tracking). No third-party skill source was copied into the repository or added as a runtime dependency.
- Removed empty npm dependency metadata and the no-op `prepare` script, and removed `npm install` from both workflows. The current JavaScript tests use Node built-ins; the web build uses Python. The workflow now proves this path works without installing npm packages.
- Updated `verify.yml` to actions/checkout v5, setup-python v6 and setup-node v5, matching the already-updated Pages workflow. This removed the previous Node 20 action-runtime deprecation warning. The npm CLI still emits a separate Node `DEP0040` punycode deprecation warning during npm commands; the job succeeds, and the available log does not attribute it to project source code.
- Exact PR-head verification [41188217991](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41188217991) passed on `e2b0effdfb2091a3f9ca1450d32b6f0e110d29ba`: data/evidence audit (43 consonants, 34 vowels, 17 tone rules, 70 Ukrainian mappings, 22 sources, 45 claims); Python 94; browser 47; romanization integration 19; syllable crosswalk 27; web layout 6; build, generated-data reproducibility and built-page/relative-asset checks. Total: 193 tests. No external G2P comparison or linguistic gold-corpus evaluation was run.
- This change improves engineering workflow consistency and removes unnecessary dependency installation. It does not change or validate Lao phonology, Ukrainian target correctness, empirical accuracy, visual QA or keyboard accessibility.

## GitHub Actions Node 24 migration — 2026-10-31

- PR #71 merged project-specific agent guidance, removed the empty npm dependency manifest entries and no-op installs, and aligned `verify.yml` to checkout v5 / setup-python v6 / setup-node v5. Main verify [41188440566](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41188440566) passed; Pages [41188440580](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41188440580) also passed but exposed Node 20 warnings from its remaining v4 artifact/deploy actions.
- PR #72 upgraded Pages to `actions/upload-pages-artifact@v5` and `actions/deploy-pages@v5`. Upstream official metadata was checked: upload-pages-artifact v5.0.0 invokes upload-artifact v7.0.0, whose action metadata declares `node24`; deploy-pages v5.0.1 also declares `node24`.
- PR #72 merged as `649973f320a8eb0e6cf2d927c9b90add5cdcdd68`. Exact-main verify [41188708711](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41188708711) passed. Pages build and deploy [41188708689](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41188708689) passed, and its logs contain no Node 20 action-runtime deprecation warning.
- The full verify run reports 43 consonants, 34 vowels, 17 tone rules, 70 Ukrainian mappings, 22 evidence sources and 45 claims; Python 94, browser 47, romanization integration 19, syllable crosswalk 27 and web layout 6 (193 total); build, generated-data reproducibility and built-page checks passed.
- npm itself still emits non-fatal Node `DEP0040` punycode deprecation warnings during npm commands. No external G2P comparison or linguistic gold-corpus evaluation was run. These CI changes do not validate phonological correctness or complete visual/keyboard QA.

## Tone-mark syllable-domain correction — 2026-10-31

- Source review found that the canonical tone-rule registry used `syllable_type=*` for every marked selector. The Python and browser selectors therefore assigned tones to marked dead syllables, even though the cited Vientiane reference charts place tone-mark rules in the live/open domain.
- Appen Butler Hill's *Language Specific Peculiarities Document for Lao as Spoken in Laos* (2017), p. 14, explicitly says tone marks are used with open syllables. It further states that `໊` and `໋` are rare in modern writing, are used with middle-class consonants, and indicate high-falling and low-rising tones respectively. SEAsite's Vientiane chart independently places its two common tone-mark columns under live syllables.
- The canonical CSV now limits all eight marked selectors to `live`, retains wildcard vowel length for live syllables, and gives the rules explicit `LIVE` IDs. The rare `mai ti` and `mai catawa` rules retain middle-class-only selectors and have their own source-linked claim. The generated browser mirror is synchronized with the CSV.
- Added direct selector tests, a shared Python/browser tone fixture for all three onset classes × four marks × short/long dead contexts, and repository-audit assertions. These are deterministic behavior tests, not independent Lao pronunciation gold.
- Test-first evidence: PR #73 test-only run [41189555009](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41189555009) failed in the new regression with 16 expected dead-syllable cases receiving a tone under the old wildcard selectors. The first data correction exposed a separate open-diphthong classification issue, and a subsequent fixture correction fixed an onset-class expectation. The final exact-head verification [41190189983](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190189983) passed the audit, Python 97, browser 47, romanization integration 19, syllable crosswalk 27, web layout 6, build, generated-data reproducibility, and built-page/relative-asset checks.

### Final verification — PR #73

The final PR #73 head `13b4aee52fb7249cceceb8e494f00dcf907ce7d3` passed [workflow 41190189983](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190189983): audit (43 consonants, 34 vowels, 17 tone rules, 70 Ukrainian mappings, 23 sources, 47 claims); Python **97**; browser **47**; romanization integration **19**; syllable crosswalk **27**; web layout **6**; external-G2P harness syntax/CLI; production build; generated-data reproducibility; built-page and relative-asset checks. Total: **196 deterministic engineering tests passed**.

The same shared 37-case tone fixture is consumed by Python and browser tests. It covers all three onset classes × four tone marks × short/long dead contexts, plus open short diphthongs and the nasal-final AM rhyme. The rule registry now limits marked selectors to live syllables; the vowel registry distinguishes monophthong/diphthong nucleus type and preserves the nasal coda property. This verifies the implementation contract, not acoustic contour measurements or independent lexical IPA accuracy.

### Final documentation-state verification — 2026-10-31

The final PR #73 branch head `803d1346b6278c3b25260063931bf72dc4e10457`, including the updated handoff and audit records, passed exact-head verification [41190275031](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190275031). Repository audit, Python 97, browser 47, romanization 19, syllable crosswalk 27, web layout 6, optional G2P harness syntax/CLI, production build, generated-data reproducibility and built-page/relative-asset checks all passed. Total: 196 deterministic engineering tests. A post-merge exact-main run and Pages deployment are still required.

## PR #73 merge and deployment verification — 2026-10-31

PR #73 merged to `main` as `0b99fd451507717664a0190dbc3bcfb7069ce15c`. Its final PR-head workflow [41190329422](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190329422) passed 196 deterministic tests, repository audit, build, generated-data reproducibility and built-page/relative-asset checks.

Post-merge `main` verification and Pages deployment are **unconfirmed**, not failed: the available GitHub connector only exposes PR-triggered workflow runs; the combined classic commit status had no entries; Firecrawl reported insufficient credits; and the public Pages URL could not be fetched through the available web reader. The prior Pages deployment run [41188708689](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41188708689) predates the new browser/rhyme data and cannot verify this update. Acceptance remains: confirm main verify, Pages build+deploy, and the public `index.html`/`system.html` content.

### PR #74 hygiene and handoff verification

PR #74 removes two unused imports left by the fixture-test refactor and reconciles the master handoff with PR #73's merge. Exact-head workflow [41190577692](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190577692) passed on `56436f6f980bf7eceb148b9d7d32f935f6325d3f`: repository audit, Python 97, browser 47, romanization 19, syllable crosswalk 27, web layout 6, optional G2P harness syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks. This is PR-head verification, not post-merge `main`/Pages evidence.
