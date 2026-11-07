# MekongPhon dataset rights review — 2026-11-07

## Decision

**Status: BLOCKED for corpus reuse and redistribution; permitted research use is not established by the evidence inspected.**

Do not copy MekongPhon source rows into this repository, build or publish a derivative corpus from them, include raw rows or item-level predictions in CI artifacts, or use the corpus as independent IPA gold until the dataset rights-holder provides an applicable license or written permission.

This is a conservative rights decision, not a legal opinion that all private research activity is prohibited. The available public materials do not establish a clear permission for research copying, processing, adaptation, or redistribution of the dataset itself.

## Primary artifacts inspected

- Upstream repository: [byu-matrix-lab/MekongPhon](https://github.com/byu-matrix-lab/MekongPhon).
- Upstream default branch: **main**.
- Inspected upstream tree commit: **f80f6c1840c4818b51e05f2e00cded4701a5b662**.
- Upstream GitHub repository metadata reports **license: null**.
- The tracked root tree contains README.md, data/, pipeline/, training/ and models/; no root LICENSE or COPYING file is present.
- The upstream README describes the corpus, repository structure and citation, but contains no dataset license grant.
- The repository's public status and the paper's statement that resources are publicly released do not, by themselves, specify the legal permissions applicable to each corpus component.
- The paper: [MekongPhon: A Large-Scale Parallel IPA Corpus for Lao and Khmer](https://doi.org/10.63317/4bb9rvdshu4z), LREC 2026, pp. 1650–1658. The proceedings page is published by ELRA. A proceedings license is not automatically the license for separately hosted data, source dictionaries, OPUS-derived sentence pairs or model artifacts.

## Component-by-component rights boundary

| Component | Evidence observed | Disposition |
|---|---|---|
| MekongPhon repository code | Public repository; no root license identified in inspected snapshot | Do not copy/relicense code without a clear license; independently written analysis is separate |
| Lao/Khmer lexicon CSVs | No dataset-specific license in root README or repository metadata | Rights unknown; do not copy or redistribute |
| Scraped dictionary material | Pipeline describes SEAlang/Kerr dictionary sourcing | Requires source terms and item-level provenance review; upstream repository visibility does not clear source rights |
| OPUS-derived sentence data | Pipeline downloads external OPUS corpora; the repository tree does not contain a blanket license grant for every underlying corpus | Review each OPUS component and its terms separately |
| Derived orthography–IPA pairs | Rights may depend on source material, transcription contribution and dataset terms | No blanket derivative-use permission established |
| Neural model artifacts | Hugging Face model cards for the Lao tonal and non-tonal models declare Apache-2.0 | This applies to those model artifacts as declared by their cards, not automatically to training data or source corpora |
| LREC paper/proceedings | Proceedings are separately published and licensed | Cite the paper; do not transfer its proceedings license to the dataset |

## Research-use question

The question “may this be used for non-commercial research?” cannot be answered affirmatively from the materials inspected. A non-commercial purpose does not itself create a license or eliminate applicable copyright/database rights. Conversely, this review does not determine whether a narrowly scoped act of private analysis is permitted under every applicable jurisdiction's exceptions or limitations.

Before any dataset access that entails downloading, retaining, processing, adapting, or redistributing records, obtain one of:

1. A dataset-specific license from the rights-holder that clearly covers the intended acts; or
2. Written permission from the rights-holder specifying the dataset version, components, research use, retention, publication of aggregate results, and whether derived data or excerpts may be shared.

If permission covers analysis but not redistribution, keep source rows and per-item predictions outside the public repository and CI artifacts. Publish only aggregate results that do not reproduce protected expression or confidential material, subject to the permission's terms.

## Methodological status is separate from legal status

Even if rights are later cleared, MekongPhon is not independent project gold. The repository's existing triage records that the Lao seed lexicon is derived from historical dictionary IPA and that sentence-level IPA is expanded through longest-match lexicon lookup over OPUS text. The paper's evaluation protocol and its held-out figures must not be conflated with blind expert annotation of the target Vientiane citation-form profile.

The 100-word benchmark described in [PR #137](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/137) is a diagnostic comparison only. Its implementation stores aggregate metrics rather than source rows or per-item predictions. Its success does not change the rights status or create independent gold.

## Conditions to reopen

- [ ] Identify the rights-holder(s) for each source component.
- [ ] Obtain the exact dataset version and component-level license/permission.
- [ ] Confirm permission to download and process the data for non-commercial research.
- [ ] Confirm permission, if any, to publish aggregate metrics and derived examples.
- [ ] Confirm whether derivative datasets, excerpts, or model outputs may be redistributed.
- [ ] Record the grant, date, scope, restrictions and evidence locator in the canonical source/license registry.
- [ ] Re-run item-level provenance validation before any row is admitted to a project corpus.

## References

- [MekongPhon repository](https://github.com/byu-matrix-lab/MekongPhon)
- [MekongPhon upstream inspected tree](https://github.com/byu-matrix-lab/MekongPhon/tree/f80f6c1840c4818b51e05f2e00cded4701a5b662)
- [LREC 2026 paper and proceedings record](https://lrec.elra.info/lrec2026-main-129)
- [Lao tonal model card](https://huggingface.co/byumatrixlab/lao-ipa-tonal)
- [Lao non-tonal model card](https://huggingface.co/byumatrixlab/lao-ipa-nontonal)

*Review date: 2026-11-07. This is a repository evidence assessment, not jurisdiction-specific legal advice.*
