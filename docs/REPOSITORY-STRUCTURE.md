# Repository structure and documentation contract

This document defines where project material belongs, how to navigate it, and which files are authoritative. It is a placement and maintenance guide, not a second execution plan.

## Repository map

```text
.
├── README.md                 Public overview, live demo, quick start and status
├── AGENTS.md                 Mandatory instructions for coding agents
├── CONTRIBUTING.md           Human contribution and verification workflow
├── GLOSSARY.md               Canonical project terminology/status vocabulary
├── pyproject.toml             Python package metadata and tool configuration
├── package.json               Browser/Node test and build commands
├── src/lao_ukrainian/         Python engine, API, CLI and typed adapters
├── web/                       Browser engine, UI modules and generated data mirror
├── index.html                 Main Lao → Ukrainian browser instrument
├── system.html                Public methodology and limitations page
├── data/
│   ├── lao/                   Canonical Lao linguistic registries (CSV)
│   ├── evidence/               Source, claim, license and provenance registers
│   ├── benchmark/              Benchmark fixtures/manifests; gold is separately gated
│   └── comparative/            Explicitly scoped cross-script comparison data
├── schemas/                    Machine-readable public/internal data contracts
├── tests/                      Python, Node, browser and shared-fixture tests
├── scripts/                    Data generation, audits, corpus and benchmark tooling
├── docs/
│   ├── README.md               Documentation navigation index
│   ├── MASTER-EXECUTION-PLAN... Canonical chronological task ledger and handoff
│   ├── PRODUCT-REQUIREMENTS.md User-visible requirements and acceptance
│   ├── methodology.md          Research method and evidence distinctions
│   ├── system-specification.md Normative processing and adapter contract
│   ├── limitations.md           Unsupported cases and readiness boundaries
│   ├── decision-log.md          Durable project decisions
│   ├── sources-and-evidence.md Evidence interpretation and source registry guide
│   ├── agents/                  Codebase and maintainer navigation
│   ├── research/                Dated research protocols, reports and integrations
│   └── audits/
│       ├── README.md            Audit/evidence navigation
│       └── current/             Current registers and dated audit snapshots
└── .github/
    └── workflows/               CI, benchmark and GitHub Pages deployment
```

The tree is descriptive rather than exhaustive. Use the repository itself for exact paths; do not create duplicate copies of generated registries or test fixtures in documentation folders.

## Where new material belongs

| Material | Canonical location | Rule |
|---|---|---|
| Public overview, installation, current status | `README.md` | Keep concise; link to detailed canonical docs instead of duplicating them |
| Agent-specific invariants and mandatory workflow | `AGENTS.md` | Keep short and operational; point to deeper docs |
| Contribution commands and review practices | `CONTRIBUTING.md` | Commands must match package scripts and CI |
| Project terms and task statuses | `GLOSSARY.md` | Define terms once; reuse exact vocabulary |
| Product requirements and observable behavior | `docs/PRODUCT-REQUIREMENTS.md` | User-facing acceptance criteria, not implementation notes |
| Normative pipeline and typed results | `docs/system-specification.md` | Contract; changes require matching tests/schema |
| Linguistic rationale and evidence quality | `docs/methodology.md`, `docs/sources-and-evidence.md` | Separate established fact, project policy, hypothesis and unknown |
| Canonical linguistic values | `data/lao/*.csv` | Never store competing copies in Markdown or generated JS |
| Source and claim provenance | `data/evidence/` | Record exact locators, scope and rights; do not invent citations |
| Output/data interfaces | `schemas/` | Version and test machine-readable contracts |
| Implementation navigation | `docs/agents/codebase-map.md` | Paths and callers only; verify against code |
| Reproducible experiments and research | `docs/research/` | Include question, pinned inputs, method, result, limitations and artifact links |
| Current task state and next work | `docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md` | Single chronological ledger; append verified closeouts |
| Current audit snapshot | `docs/audits/current/` | Dated, evidence-backed; never imply historical snapshots are live |
| Test cases and shared contracts | `tests/` | Keep expected values independent of implementation |
| Reproducible automation | `scripts/` and `.github/workflows/` | Pin dependencies and preserve artifacts/provenance |

## Documentation precedence

When two sources disagree, resolve them in this order:

1. Current executable behavior, canonical data and schemas establish what is implemented.
2. Product requirements and system specification establish intended behavior.
3. Methodology, primary sources, source/claim registers and decision log establish why a rule is allowed.
4. The master execution plan and current completion register establish task status and acceptance evidence.
5. Current audit snapshots summarize a dated checkpoint.
6. Historical audits, benchmark reports and prior handoffs remain immutable evidence of their checkpoint; they do not override newer verified state.

A newer date alone does not make a claim authoritative. Prefer a newer exact-head CI run, current source data and explicit acceptance criteria.

## Status vocabulary

- `DONE_VERIFIED`: implementation exists and required acceptance evidence passed on the exact relevant commit.
- `PARTIAL`: implementation/evidence exists, but at least one acceptance criterion remains open.
- `TODO`: work is not implemented.
- `BLOCKED`: a named external dependency, missing rights or unavailable evidence prevents acceptance.
- `DEFERRED`: explicitly outside current scope or awaiting an owner-level decision.

Do not mark work DONE because a document or test file exists. Record the exact workflow/commit and remaining acceptance criterion.

## Updating documentation after a change

1. Identify the canonical requirement/specification, implementation map, data/source registry, tests and workflow affected.
2. Change executable behavior and tests before describing it as implemented.
3. Update the relevant subject document and codebase map.
4. Append a concise dated entry to the master handoff; do not create a competing plan.
5. Update the current audit and completion register when status, branch/PR state, deployment, evidence or blockers change.
6. Fix navigation links in `README.md`, `docs/README.md` and `docs/audits/README.md` if the canonical entry point changed.
7. Run link/path checks and exact-head CI; only then mark DONE_VERIFIED.
8. Keep older dated audits intact. Add a superseding current addendum instead of silently rewriting history.

## Lessons from the supplied repository references

- [unlazy](https://github.com/Leonxlnx/unlazy) separates concise operational README guidance from agents, references, research, scripts, templates and tests.
- [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) separates source, CLI, docs, examples/gallery, stack data and plugin metadata; localized READMEs serve distinct audiences.
- [superpowers](https://github.com/obra/superpowers) separates portable skills from host-specific integrations, hooks and tests.
- [mattpocock/skills](https://github.com/mattpocock/skills) makes agent instructions, glossary, scope and docs explicit.
- [ponytail](https://github.com/DietrichGebert/ponytail) uses host adapters/manifests alongside commands, skills, hooks, benchmarks and examples.

Adopt the transferable ideas: concise entry points, explicit scope, one agent-instruction entry, glossary, task-oriented navigation, source separation and reproducible tests. Do not copy agent-plugin marketplaces, host adapter trees, skill manifests or localized README matrices unless ClippyFirst becomes a distributed agent plugin or skill. The current language-engine architecture already has the right separation; the improvement is clearer navigation and stricter status synchronization, not more directories for their own sake.

## Review checklist

- [ ] Does every new file have one clear canonical home?
- [ ] Is the same fact duplicated in multiple places? Replace copies with links.
- [ ] Are claims tied to primary sources, code paths, schemas or exact CI runs?
- [ ] Are provisional hints, accepted IPA and accuracy kept separate?
- [ ] Do README and index links point to the current audit and canonical contract?
- [ ] Do task statuses name exact acceptance evidence and the genuine blocker?
- [ ] Are generated data and runtime assets produced by scripts rather than hand-edited?
