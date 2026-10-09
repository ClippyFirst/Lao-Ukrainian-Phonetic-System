# Web architecture

The static service has exactly two public pages: `index.html` and `system.html`. Vite builds both pages into `dist/` with relative asset URLs so the site works at the GitHub Pages project path as well as at a custom domain.

## Data flow

Canonical CSV registries in `data/lao/` remain the source of truth. `scripts/generate_web_data.py` deterministically produces `web/data.js`, a checked-in browser artifact. The browser engine imports that artifact; it does not maintain a second hand-authored linguistic registry.

```
canonical CSV
  ↓
generate_web_data.py
  ↓
web/data.js
  ↓
web/engine.js
  ↓
web/app.js
```

No runtime network request is required for conversion.

## Research boundary

The browser engine is deliberately conservative. It exposes IPA, structural features, tone status and warnings. It must not silently turn unresolved linguistic cases into authoritative-looking output.

The current static MVP still treats whitespace as the reliable segmentation boundary. Full lexical/unspaced segmentation belongs to the research core and future corpus-backed releases.

## Release checks

1. Validate canonical data and Python tests.
2. Regenerate `web/data.js`.
3. Run `npm test`.
4. Run `npm run build` (or `npm run check:release`).
5. Perform browser/manual checks for input, example, clear, copy, navigation, keyboard focus, responsive layout and uncertainty states.
6. Inspect the generated diff and ensure no duplicate hand-maintained linguistic registry was introduced.

The project intentionally does not publish empirical accuracy percentages without a versioned expert gold corpus.
