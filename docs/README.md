# Documentation index

This directory is the documentation home for the Lao → Ukrainian project. Start with the route below that matches your task, then use the canonical document in the index. Dated audits are evidence snapshots, not live specifications; the master execution plan is the single chronological task ledger.

## Start here

| Need | Canonical document |
|---|---|
| Current work, task status, handoff and blockers | [Master execution plan and chat handoff](MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md) |
| Latest repository and documentation continuation | [Repository and documentation audit — 2026-11-09](audits/current/REPOSITORY-AND-DOCUMENTATION-CONTINUATION-2026-11-09.md) |
| Latest integrated engineering audit (historical checkpoint) | [Repository-wide audit — 2026-11-08](audits/current/REPOSITORY-WIDE-AUDIT-2026-11-08.md) |
| Terms and status vocabulary | [Project glossary](../GLOSSARY.md) |
| Product scope and user-visible requirements | [Product requirements](PRODUCT-REQUIREMENTS.md) |
| Linguistic pipeline and evidence distinctions | [Methodology](methodology.md) |
| Normative processing contract | [System specification](system-specification.md) |
| Actual implementation entry points | [Codebase map](agents/codebase-map.md) |
| Known unsupported or uncertain cases | [Limitations](limitations.md) |
| How to run checks | [Validation guide](validation.md) |
| Source provenance and claim registry | [Sources and evidence](sources-and-evidence.md) |
| Engineering decisions | [Decision log](decision-log.md) |
| Current and historical audits | [Audit index](audits/README.md) |

## Read by task

- **I am new to the project:** read the root [README](../README.md), then [product requirements](PRODUCT-REQUIREMENTS.md), [methodology](methodology.md), and [system specification](system-specification.md).
- **I need to change code:** read [agent instructions](../AGENTS.md), [contributing guide](../CONTRIBUTING.md), and [codebase map](agents/codebase-map.md); trace the relevant callers, data, tests, generated artifacts, and workflow.
- **I need to understand a pronunciation result:** follow [methodology](methodology.md), [typed IPA adapter](ipa-to-ukrainian-adapter.md), [Ukrainian target policy](ukrainian-target.md), and [known limitations](limitations.md).
- **I need to evaluate coverage or accuracy:** read [benchmark methodology](benchmarking-and-external-ipa.md), the [current engine/dataset inventory](research/LAO-G2P-ENGINE-AND-DATASET-INVENTORY-2026-11-08.md), and the [HVULao stress report](research/HVULAO-1K-THREE-ENGINE-STRESS-2026-11-08.md). Never treat rendering coverage as IPA coverage or accuracy.
- **I need the latest status:** read the [current continuation audit](audits/current/REPOSITORY-AND-DOCUMENTATION-CONTINUATION-2026-11-09.md), then the [master execution ledger](MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md).

## Documentation by subject

### Product and interface
- [Design system](DESIGN-SYSTEM.md)
- [Web architecture](web-architecture.md)
- [Author's system page content contract](SYSTEM-PAGE.md)
- [Romanization → Ukrainian matrix](romanization-to-ukrainian-matrix.md)
- [Ukrainian target policy](ukrainian-target.md)
- [Grapheme-level provisional IPA preview](lao-grapheme-ipa-preview.md)
- [Unicode handling](unicode.md)

### Linguistics and implementation
- [System specification](system-specification.md)
- [Methodology](methodology.md)
- [Implementation map](implementation.md)
- [Phonology audit notes](PHONOLOGY-AUDIT.md)
- [Vowel-template coverage](vowel-template-coverage.md)
- [Comparative Cyrillic analysis](comparative-cyrillic.md)
- [Attributed LaoNLP lexical-hint list and limitations](../data/lao/lexical-hints/README.md) — orthographic soft hints only; not a segmentation gold set or IPA source.

### IPA, corpora and evaluation
- [Typed IPA → Ukrainian adapter contract](ipa-to-ukrainian-adapter.md)
- [Lao → Ukrainian practical transcription guide](lao-ukrainian-practical-transcription.md)
- [Independent IPA gold corpus contract](ipa-gold-corpus.md)
- [Controlled IPA gold collection playbook](ipa-gold-collection-playbook.md)
- [Benchmarking and external IPA](benchmarking-and-external-ipa.md)
- [External IPA renderers](external-ipa-renderers.md)
- [Independent G2P comparison](independent-g2p-comparison.md)
- [Lao G2P engine and dataset inventory — confidence-gated comparison, Transphone and corpus fitness](research/LAO-G2P-ENGINE-AND-DATASET-INVENTORY-2026-11-08.md)
- [External Lao G2P benchmark workflow](../.github/workflows/external-lao-g2p-benchmarks.yml) — pinned comparators, confidence-gated IPA scoring and aggregate-only artifacts.
- [External G2P research](research/external-g2p-benchmark-and-engine-coverage-2026-11-02.md)
- [MekongPhon neural integration guide](research/MEKONGPHON-NEURAL-INTEGRATION.md)
- [Deterministic MekongPhon-reference IPA rule port](research/MEKONGPHON-DETERMINISTIC-RULE-PORT-2026-11-08.md)
- [Hybrid deterministic Lao IPA engine](research/HYBRID-DETERMINISTIC-ENGINE-2026-11-08.md)
- [HVULao 1k three-engine sentence-domain stress benchmark](research/HVULAO-1K-THREE-ENGINE-STRESS-2026-11-08.md)
- [MekongPhon rights review](audits/current/MEKONGPHON-DATA-RIGHTS-REVIEW-2026-11-07.md)
- [MekongPhon grapheme-context analysis](audits/current/MEKONGPHON-GRAPHEME-CONTEXT-ANALYSIS-2026-11-07.md)

### Agent and maintainer context
- [Agent instructions and pinned external methodology references](../AGENTS.md)
- [Codebase map](agents/codebase-map.md)
- [Issue tracker conventions](agents/issue-tracker.md)
- [Superpowers corpus plan](superpowers/plans/2026-11-01-independent-ipa-gold-corpus.md)

## Accessibility QA

- [Manual accessibility QA protocol and results log](accessibility-manual-qa.md) — screen readers, keyboard-only operation, physical mobile devices, real browser zoom, high contrast and visual review.

## Source-of-truth and precedence

When documents appear to conflict, use this order:

1. Current executable behavior, canonical registries and schemas establish what the repository actually implements.
2. Product requirements and system specification establish intended public behavior and constraints.
3. Methodology, source/claim registries and decision log establish the evidence basis and explicit project policy.
4. The master execution plan and linguistic completion register establish current task status and acceptance evidence.
5. Dated audit records preserve historical findings; they do not silently override newer code or current status documents.

The CSV files in `data/lao/` are the authoritative phonological registries. The separate `data/lao/lexical-hints/` list is an attributed orthographic research aid and must not be treated as a phonological registry, lexical-boundary gold, or IPA source.

A passing engineering test is not evidence of expert phonetic accuracy. The independent IPA gold corpus remains a separate, rights- and human-review-gated process. At the 2026-11-09 mainline checkpoint, hybrid rendering was 100% on the 1k sentence stress set, while IPA completeness was 34.6% of sentences and 94.21% of syllables; the 100-word reference benchmark showed 91% segmental and 86% tonal IPA coverage. Consult the linked reports for denominators and limitations.