# Web Architecture

## Pages

- `/` — service.
- `/system.html` — author's system.

No third main page is introduced.

## Modules

- `web/app.js` — UI orchestration only.
- `web/engine.js` — deterministic browser analysis and correspondence rules.
- `web/styles.css` — design system.
- `web/index.html` — service shell.
- `web/system.html` — methodology shell.

The UI does not own linguistic rules.

## Browser analysis

The browser engine mirrors the repository's conceptual pipeline for the documented web subset. It is deliberately conservative: when a sequence cannot be parsed confidently, it returns an explicit warning rather than fabricating a Ukrainian output.

The Python package remains the research authority. The web engine is a presentation/runtime layer and should converge with the package through shared generated data or a future stable API.

## Data contract

The engine returns:

```js
{
  input,
  normalized,
  status,
  output,
  syllables: [
    {
      surface,
      onset,
      class,
      vowel,
      syllableType,
      tone,
      toneContour,
      ipa,
      ukrainian,
      status,
      rules
    }
  ],
  warnings
}
```

## Privacy

No network request is required to analyze text. User input remains in the browser.
