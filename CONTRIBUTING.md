# Contributing

This guide describes the current repository contract. It complements [AGENTS.md](AGENTS.md), the [project glossary](GLOSSARY.md), and the [documentation index](docs/README.md).

## Before changing code or data

1. Read [the master execution plan and handoff](docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md) and check whether the task is already implemented or blocked.
2. Read [the codebase map](docs/agents/codebase-map.md) and the relevant product, methodology, specification, limitation and evidence documents.
3. Trace the complete caller → implementation → consumer → tests/fixtures → generated artifacts → workflows → documentation path.
4. Preserve the status vocabulary: DONE_VERIFIED, PARTIAL, TODO, BLOCKED, DEFERRED.

## Development requirements

- Python 3.10+ for the package and repository scripts.
- Node.js 22.14+ for the Node/browser test tooling.
- Playwright Chromium for the built-site browser tests.
- No frontend bundler is currently used. The site consists of two static HTML pages and native browser ES modules.

Install the exact browser-test dependency graph from `package-lock.json`, then install Chromium:

    npm ci --no-audit --no-fund
    npx playwright install --with-deps chromium

## Verification commands

Run the relevant focused test while developing, then run the complete applicable suite before declaring GREEN.

    python scripts/ipa_gold_corpus.py validate --language lao
    python scripts/audit.py
    PYTHONPATH=src python -m unittest discover -s tests -v
    npm test
    npm run build
    git diff --exit-code -- web/data.js
    npm run test:browser

For a compact web release sequence, npm run check:release runs the Node suites, static build and Playwright browser suite. It does not replace the Python/data checks above or human linguistic and accessibility review.

The build creates dist/ from index.html, system.html and web/. It regenerates web/data.js from canonical CSV data first. Inspect the generated diff; never hand-edit generated browser data.

## Data and linguistic evidence

- Canonical Lao registries are data/lao/*.csv.
- Source and claim provenance belongs in data/evidence/sources.csv and data/evidence/claims.csv.
- Schemas in schemas/ define machine-readable contracts.
- Extend shared regression fixtures when changing supported structures or cross-runtime behavior.
- Distinguish established facts, project policy, hypotheses and unsupported cases.
- Do not fabricate IPA, source locators, licenses, gold records or benchmark scores.
- External G2P output, romanization and dictionary entries are comparators/leads, not independent IPA gold.
- Keep accuracy null until rights-cleared, independently annotated and adjudicated held-out gold exists.
- Preserve the pipeline: Lao orthography → structural analysis → phonology → typed IPA → Ukrainian adaptation.
- Keep romanization as a separate, lower-information orthographic mode.

## Privacy, licensing and generated artifacts

- Do not commit speaker names, contact details, private audio or personal data.
- Check item-level permissions before copying, redistributing or publishing third-party source material.
- Do not infer redistribution rights from public availability or from a registry row alone.
- Do not edit web/data.js directly; regenerate it from canonical data.
- Do not add runtime dependencies for methodology references or generic skill bundles.

## Reviews and releases

- Keep changes focused and test observable public behavior.
- Use regression tests for behavior changes; ensure a RED result fails for the intended reason.
- Re-run relevant checks on the exact final commit.
- Inspect open/recent PRs and relevant branches before porting or merging work.
- Do not force-push, delete user branches, change repository settings, or publish releases without owner authorization.
- Record external blockers with the exact evidence and acceptance criterion. A green engineering workflow is not linguistic release approval.
