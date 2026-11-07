# MekongPhon dataset rights review — 2026-11-07

## Decision

**Status: PARTIAL — limited internal non-commercial research use is reasonably supported by the authors' stated release purpose; redistribution, derivative corpus publication and broader training/reuse remain BLOCKED pending explicit component-level terms.**

Proceed only with a narrow, non-commercial, non-redistributive research evaluation of the published 100-entry Lao held-out seed-lexicon split, using an ephemeral CI download and aggregate-only output. The authors explicitly state that the data are publicly released to support future research, and the paper cites SEAlang's general Creative Commons reuse statement. The existing PR #137 benchmark follows this narrow pattern: it downloads the 100-word evaluation file at run time, retains no source rows or per-item predictions in the repository/artifact, and publishes aggregate metrics only.

Do not copy source rows into the repository, retain or republish the full corpus, publish per-item predictions/examples, create a derivative dataset, train or release a new model on the corpus, or use it commercially until the exact dataset/component terms are confirmed. Do not admit its labels as independent IPA gold.

This is an evidence-qualified interpretation of the authors' stated research-release intent, not a definitive legal opinion or a substitute for a specific license grant. The repository's machine-readable license registry should continue to treat the dataset license as UNKNOWN until a license identifier or written permission is obtained.

## Primary artifacts inspected

- Upstream repository: [byu-matrix-lab/MekongPhon](https://github.com/byu-matrix-lab/MekongPhon).
- Upstream default branch: **main**.
- Inspected upstream tree commit: **f80f6c1840c4818b51e05f2e00cded4701a5b662**.
- Upstream GitHub repository metadata reports **license: null**.
- The tracked root tree contains README.md, data/, pipeline/, training/ and models/; no root LICENSE or COPYING file is present.
- The upstream README describes the corpus, repository structure and citation, but contains no dataset license grant.
- The repository's public status and the paper's statement that resources are publicly released do not, by themselves, specify the legal permissions applicable to each corpus component.
- The paper: [MekongPhon: A Large-Scale Parallel IPA Corpus for Lao and Khmer](https://doi.org/10.63317/4bb9rvdshu4z), LREC 2026, pp. 1650–1658. The official proceedings page states that LREC proceedings are licensed under CC BY-NC 4.0. Its abstract says the data, code and pretrained models are publicly released to support future research. The paper itself also quotes the SEAlang homepage as saying that all results are freely available for reuse under a “Creative Commons open license.” This is positive evidence that the authors intended the resources to be available for research and that the seed-dictionary source presents a reuse statement. However, neither the paper nor the SEAlang page identifies a specific Creative Commons license version or its conditions. The proceedings license is a license for the proceedings publication; neither it nor the upstream README identifies a dataset-specific license for the separately hosted MekongPhon corpus, source dictionaries, OPUS-derived sentence pairs or model artifacts. Public release for research should not be silently expanded into a blanket redistribution or derivative-work grant.

## Scope of the research use already performed

The benchmark in [PR #137](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/137) reads the 100-entry file at the pinned upstream revision and SHA-256 recorded in its report. The file is the held-out seed lexicon split (orthography plus tonal/non-tonal IPA references), not the sentence-level OPUS-expanded corpus. The workflow computes aggregate metrics and source-free error-context counts; it does not write the input rows or per-item predictions to the report/artifact. The exact-head benchmark workflow [42358468909](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42358468909) completed SUCCESS. This is the narrow research activity that is considered reasonable to proceed with under the stated research-release intent.

## Component-by-component rights boundary

| Component | Evidence observed | Disposition |
|---|---|---|
| MekongPhon repository code | Public repository; no root license identified in inspected snapshot | Do not copy/relicense code without a clear license; independently written analysis is separate |
| Lao/Khmer lexicon CSVs | No dataset-specific license in root README or repository metadata | Rights unknown; do not copy or redistribute |
| Scraped dictionary material | Pipeline describes SEAlang/Kerr dictionary sourcing | Requires source terms and item-level provenance review; upstream repository visibility does not clear source rights |
| OPUS-derived sentence data | The paper describes NLLB, ParaCrawl and OpenSubtitles. The checked-in Lao download script actually downloads NLLB v1 and ParaCrawl-Bonus v9; the Khmer script additionally downloads OpenSubtitles v2024. | Not part of the 100-word lexicon benchmark. Review each component and its upstream source terms before any full sentence-corpus reuse or redistribution |
| Derived orthography–IPA pairs | Rights may depend on source material, transcription contribution and dataset terms | No blanket derivative-use permission established |
| Neural model artifacts | Hugging Face model cards for the Lao tonal and non-tonal models declare Apache-2.0 | This applies to those model artifacts as declared by their cards, not automatically to training data or source corpora |
| LREC paper/proceedings | Proceedings are separately published and licensed | Cite the paper; do not transfer its proceedings license to the dataset |

## Research-use question

The evidence indicates that the authors intend MekongPhon to be available for research: the paper says the resources are publicly released to support future research, and it quotes SEAlang's general reuse statement. On that basis, the existing narrow internal benchmark on the 100-entry seed-lexicon holdout is treated as within the stated research purpose, subject to the strict non-redistribution boundary above. The paper's 100-entry lexicon holdout is not the full 13,442-sentence evaluation set and does not contain the OPUS sentence corpus. The applicable CC version and scope are still unidentified, so this does not establish a blanket license for the full dataset, adaptations, derivative publication or commercial use. A non-commercial purpose alone does not create a license or eliminate applicable copyright/database rights.

Before expanding beyond the narrow ephemeral 100-entry research benchmark—especially for retention, adaptation, full-corpus processing, training, redistribution or publication of examples—obtain one of:

1. A dataset-specific license from the rights-holder that clearly covers the intended acts; or
2. Written permission from the rights-holder specifying the dataset version, components, research use, retention, publication of aggregate results, and whether derived data or excerpts may be shared.

If permission covers analysis but not redistribution, keep source rows and per-item predictions outside the public repository and CI artifacts. Publish only aggregate results that do not reproduce protected expression or confidential material, subject to the permission's terms.

## Methodological status is separate from legal status

Even if rights are later cleared, MekongPhon is not independent project gold. The Lao seed lexicon is derived from the 1972 Kerr dictionary hosted through SEAlang; the paper quotes SEAlang's unspecified Creative Commons reuse statement. Sentence-level IPA is expanded through longest-match lexicon lookup over OPUS text. The paper's prose lists NLLB, Paracrawl and OpenSubtitles, but the checked-in Lao downloader uses NLLB v1 and ParaCrawl-Bonus v9; OpenSubtitles v2024 appears in the Khmer downloader, not the Lao downloader. This paper/code source-list mismatch should be resolved before any full sentence-corpus reuse. The 100-word held-out seed-lexicon evaluation is distinct from that sentence corpus. The paper's 500-entry qualitative review was performed by two authors whom it describes as highly proficient second-language speakers rather than native speakers; 14/500 Lao entries were judged inaccurate (reported 97.2%). This is useful quality-control evidence, but not independent project adjudication of the target Vientiane profile. The paper's evaluation protocol and held-out figures must not be conflated with blind expert annotation.

The 100-word benchmark described in [PR #137](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/137) is a diagnostic comparison only. Its implementation stores aggregate metrics rather than source rows or per-item predictions. Its success does not change the rights status or create independent gold.

## Conditions to reopen

- [ ] Identify the rights-holder(s) for each source component.
- [ ] Obtain the exact dataset version and component-level license/permission.
- [x] Record the authors' public research-release statement and SEAlang's generic reuse notice as the evidence basis for the narrow 100-entry aggregate-only diagnostic.
- [ ] Obtain explicit confirmation of the precise Creative Commons license/version and the scope of its grant.
- [ ] Confirm permission, if any, to publish aggregate metrics and derived examples.
- [ ] Confirm whether derivative datasets, excerpts, or model outputs may be redistributed.
- [ ] Reconcile the paper's OPUS source list with the checked-in Lao/Khmer download scripts and record exact upstream component versions/licenses.
- [ ] Record the grant, date, scope, restrictions and evidence locator in the canonical source/license registry.
- [ ] Re-run item-level provenance validation before any row is admitted to a project corpus.

## References

- [MekongPhon repository](https://github.com/byu-matrix-lab/MekongPhon)
- [MekongPhon upstream inspected tree](https://github.com/byu-matrix-lab/MekongPhon/tree/f80f6c1840c4818b51e05f2e00cded4701a5b662)
- [LREC 2026 paper and proceedings record](https://lrec.elra.info/lrec2026-main-129) — page states proceedings CC BY-NC 4.0 and public release of resources for research, but does not state a dataset-specific license.
- [LREC 2026 full paper PDF](https://aclanthology.org/2026.lrec-1.129.pdf) — Section 3.1 quotes SEAlang's generic reuse statement and Section 3.2 identifies the OPUS source collections.
- [SEAlang homepage](https://www.sealang.net/) — states that project results are freely available for reuse under a “Creative Commons open license”, without identifying a version in the inspected text.
- [Lao tonal model card](https://huggingface.co/byumatrixlab/lao-ipa-tonal)
- [Lao non-tonal model card](https://huggingface.co/byumatrixlab/lao-ipa-nontonal)

*Review date: 2026-11-07. This is a repository evidence assessment, not jurisdiction-specific legal advice.*
