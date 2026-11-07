# Documentation index

This directory is the documentation home for the Lao → Ukrainian project. Use this page to find the authoritative document for a question; do not treat every dated audit or historical note as a current specification.

## Start here

| Need | Canonical document |
|---|---|
| Current work, task status, handoff and blockers | [Master execution plan and chat handoff](MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md) |
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

## Documentation by subject

### Product and interface
- [Design system](DESIGN-SYSTEM.md)
- [Web architecture](web-architecture.md)
- [Author's system page content contract](SYSTEM-PAGE.md)
- [Romanization → Ukrainian matrix](romanization-to-ukrainian-matrix.md)
- [Ukrainian target policy](ukrainian-target.md)
- [Lao → Ukrainian practical transcription guide](lao-ukrainian-practical-transcription.md)
- [Grapheme-level provisional IPA preview](lao-grapheme-ipa-preview.md)
- [Unicode handling](unicode.md)

### Linguistics and implementation
- [System specification](system-specification.md)
- [Methodology](methodology.md)
- [Implementation map](implementation.md)
- [Phonology audit notes](PHONOLOGY-AUDIT.md)
- [Vowel-template coverage](vowel-template-coverage.md)
- [Comparative Cyrillic analysis](comparative-cyrillic.md)

### IPA, corpora and evaluation
- [Typed IPA → Ukrainian adapter contract](ipa-to-ukrainian-adapter.md)
- [Lao → Ukrainian practical transcription guide](lao-ukrainian-practical-transcription.md)
- [Independent IPA gold corpus contract](ipa-gold-corpus.md)
- [Controlled IPA gold collection playbook](ipa-gold-collection-playbook.md)
- [Benchmarking and external IPA](benchmarking-and-external-ipa.md)
- [External IPA renderers](external-ipa-renderers.md)
- [Independent G2P comparison](independent-g2p-comparison.md)
- [External G2P research](research/external-g2p-benchmark-and-engine-coverage-2026-11-02.md)
- [MekongPhon neural integration guide](research/MEKONGPHON-NEURAL-INTEGRATION.md)
- [MekongPhon rights review](audits/current/MEKONGPHON-DATA-RIGHTS-REVIEW-2026-11-07.md)
- [MekongPhon grapheme-context analysis](audits/current/MEKONGPHON-GRAPHEME-CONTEXT-ANALYSIS-2026-11-07.md)

### Agent and maintainer context
- [Agent instructions](../AGENTS.md)
- [Codebase map](agents/codebase-map.md)
- [Issue tracker conventions](agents/issue-tracker.md)
- [Superpowers corpus plan](superpowers/plans/2026-11-01-independent-ipa-gold-corpus.md)

## Source-of-truth and precedence

When documents appear to conflict, use this order:

1. Current executable behavior, canonical registries and schemas establish what the repository actually implements.
2. Product requirements and system specification establish intended public behavior and constraints.
3. Methodology, source/claim registries and decision log establish the evidence basis and explicit project policy.
4. The master execution plan and linguistic completion register establish current task status and acceptance evidence.
5. Dated audit records preserve historical findings; they do not silently override newer code or current status documents.

A passing engineering test is not evidence of expert phonetic accuracy. The independent IPA gold corpus remains a separate, rights- and human-review-gated process.
