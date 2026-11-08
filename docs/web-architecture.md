# Web architecture

## Runtime shape

The public service has exactly two HTML entry pages: index.html (the converter) and system.html (the author's methodology page). The browser runtime uses native ES modules in web/; there is no Vite, Webpack, or other frontend bundler in the current implementation.

scripts/build_web.py creates dist/ by copying the two HTML pages and the web/ directory. The build is intentionally small and preserves relative asset paths for the GitHub Pages project URL. package.json provides Node test scripts and the pinned Playwright test dependency; it is not a frontend bundler configuration.

## Canonical data flow

Canonical Lao CSV registries in data/lao/ are the source of truth. scripts/generate_web_data.py deterministically produces the checked-in browser mirror web/data.js. Do not edit that generated file by hand.

    data/lao/*.csv
          |
          v
    scripts/generate_web_data.py
          |
          v
    web/data.js
          |
          v
    web/engine.js -----> web/app.js -----> index.html

    system.html is an independent static methodology page.

The Python package is a separate runtime implementation:

    CLI / Python API
          |
          v
    src/lao_ukrainian/core.py
          |
          +--> normalize.py
          +--> parser.py
          +--> phonology.py
          +--> target.py
          +--> model.py / data.py

The browser engine and Python package share canonical linguistic data and regression fixtures where applicable, but they are separately maintained implementations. Cross-runtime parity is tested only for explicitly shared contracts; the documented phrase-segmentation behavior is not identical.

## Phonetic and romanization routes

- **Phonetic (default):** Lao orthography → structural parsing → phonology → IPA → Ukrainian target adapter.
- **By romanization (optional):** Lao orthography → provisional CLDR/BGN-oriented romanization → source-aware romanized syllable parser → Ukrainian orthographic output.

The second route is lower-information, does not reconstruct tone, and is not a fallback when the IPA route is unresolved. See [methodology](methodology.md#optional-romanization-to-ukrainian-mode).

## Deployment

The Pages workflow builds the two public pages and local web/ runtime into dist/, uploads that directory, deploys it, and smoke-tests the deployed HTML and runtime assets. Asset and navigation URLs are relative so the project site works under the repository path. The workflow requires Pages to be enabled in repository settings with GitHub Actions as the source; repository settings are not changed by code commits.

## Verification

The configured CI sequence is:

1. Validate the independent IPA-gold corpus structure.
2. Run the repository data/evidence audit and Python unittest suite.
3. Validate the optional external-G2P harness CLI.
4. Run browser engine and romanization tests.
5. Regenerate browser data and require a clean generated-data diff.
6. Build the static site.
7. Run Playwright/Chromium tests against the built site and inspect required assets/accessibility hooks.

For matching local commands and prerequisites, see [CONTRIBUTING.md](../CONTRIBUTING.md). Manual keyboard, screen-reader, mobile and visual QA remains a separate acceptance item. A green engineering suite does not establish expert phonetic accuracy or linguistic release readiness.


## Integrated preview and accessibility contracts — 2026-11-08

The browser engine now exposes a separate grapheme-level preview for cases where accepted IPA is withheld. The UI labels it `PROVISIONAL`, shows unresolved graphemes, does not infer tone and does not replace the accepted IPA/Ukrainian result. Its canonical inventory is generated from `data/lao/grapheme_inventory.csv` into `web/data.js`; never hand-edit the generated mirror.

The current exact-head Verify [42460320528](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42460320528) passed 17 Chromium tests, including accessible names/landmarks/live regions, keyboard navigation/disclosures, touch emulation, responsive reflow, forced-colors/reduced-motion, 44×44 CSS-pixel target checks and 400%-equivalent 320 CSS-pixel layout. These are automated regression checks only. Actual screen-reader sessions, physical mobile devices, real browser zoom and human visual review remain separate manual gates in [the accessibility QA log](accessibility-manual-qa.md).

The lockfile is committed and Verify installs with `npm ci --no-audit --no-fund`. The clean-install and full engineering results apply to the open PR #143 branch, not to unchanged `main`.
