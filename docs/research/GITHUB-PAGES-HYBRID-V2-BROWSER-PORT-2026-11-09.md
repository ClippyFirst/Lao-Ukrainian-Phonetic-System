# GitHub Pages Hybrid v2 browser port — 2026-11-09

## Scope and exact starting point

- Repository: `ClippyFirst/Lao-Ukrainian-Phonetic-System`.
- Reviewed default-branch head: `673e36fddcbed7f073a448bf54cd1edf44a6b10f`.
- Implementation branch: `feat/pages-hybrid-v2-browser`, based directly on that head.
- Hosting constraint: GitHub Pages only; no API, server-side inference, hosted inference provider or external runtime service.
- Runtime target: browser JavaScript with WebAssembly / WebGPU acceleration where supported. This is not a Java applet port; JavaScript/WASM is the deployable browser-native route.

## What is already deployed

The current Pages site is a static, local-first application. `web/app.js` calls `web/engine.js`, whose default profile is `hybrid-deterministic`. The Python Hybrid v2 model is not part of the deployed browser runtime. The Pages workflow currently builds the static files, runs Node and Chromium tests, and deploys the `dist/` directory. No ONNX model, tokenizer bundle, ONNX Runtime Web package or model weights are currently included in the site.

Do not describe the current deployed site as running the full Hybrid v2.

## Hybrid v2 contract to preserve

The Python implementation in `src/lao_ukrainian/hybrid_v2.py` defines two separate lanes:

1. Deterministic segmental IPA and Ukrainian output remain authoritative.
2. The pinned MekongPhon tonal model output is preserved unchanged in a separate tonal-IPA lane.
3. Tone contours are associated with deterministic syllables only if the parsed contour stream has exactly one decomposition matching the deterministic syllable count.
4. Every model-derived tone remains `UNCERTAIN`; no synthetic IPA fusion or silent deterministic fallback is allowed.

The model is `byumatrixlab/lao-ipa-tonal`, immutable revision `e02608cfcb18abfe6b1916f5f4774bfac9ac788d`, with a 128-token limit and a BERT encoder–decoder architecture. The upstream model card declares Apache-2.0 and 33.6M parameters. See [model card](https://huggingface.co/byumatrixlab/lao-ipa-tonal) and the pinned [model repository revision](https://huggingface.co/byumatrixlab/lao-ipa-tonal/tree/e02608cfcb18abfe6b1916f5f4774bfac9ac788d).

## Work completed in this continuation branch

- **PARTIAL:** added `web/hybrid-v2.js`, a browser-side port of the external IPA parsing, unique tone-contour decomposition, conservative association, provenance and `UNCERTAIN` status contract.
- **PARTIAL:** added `web/hybrid-v2.test.js` and included it in `npm test`.
- The browser combiner requires a caller-supplied raw neural IPA string and immutable model provenance. It does not load model weights or perform inference.
- The explicit `unavailableHybridV2` result reports `NEURAL_UNAVAILABLE`; it does not claim that deterministic-only execution is full Hybrid v2.
- These files are on `feat/pages-hybrid-v2-browser`; they are not on `main` and have not been deployed.

## Verified benchmark evidence and current parser gap

The latest 1,000-row Hybrid v2 workflow on `673e36f...` completed successfully: [run #42680434577](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42680434577), artifact [13701914558](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42680434577/artifacts/13701914558).

The artifact reports:
- 1,000/1,000 deterministic Ukrainian rendering rows (100% rendering coverage);
- 934/1,000 neural raw IPA outputs;
- 228/1,000 neural IPA outputs parsed as supported by the current external IPA adapter;
- 706 outputs rejected by that parser as containing unsupported external IPA symbols;
- 10 fully order-aligned rows and 4 partial tone-association rows;
- 0 unexpected runtime errors.

HVULao supplies no IPA reference. These are coverage / parser / alignment diagnostics, not phonetic accuracy. The 100% Ukrainian rendering result is not a claim of 100% neural or IPA coverage.

## Browser inference feasibility and exact engineering gap

The upstream checkpoint is modest enough to investigate a browser deployment, but it is not directly consumable by the current site. The upstream Python adapter loads `EncoderDecoderModel` plus two independent tokenizers through PyTorch/Transformers. Transformers.js documents browser inference through ONNX Runtime Web and supports text-to-text generation generally, but its published architecture list does not establish out-of-the-box compatibility with this specific BERT `EncoderDecoderModel`. A custom ONNX export/runtime path therefore needs to be proven rather than assumed.

Useful upstream references:
- [Transformers.js runtime and browser configuration](https://github.com/huggingface/transformers.js#readme)
- [Transformers.js supported tasks and architectures](https://github.com/huggingface/transformers.js#supported-tasksmodels)
- [Optimum ONNX encoder–decoder export guidance](https://huggingface.co/docs/optimum-onnx/onnx/usage_guides/export_a_model)

The next implementation batch must:
1. Export the exact pinned tonal checkpoint into encoder and decoder ONNX graphs, including the exact tokenizer vocabularies and special-token IDs.
2. Prove output parity against the Python `MekongPhonEngine` on fixed fixtures before quantization.
3. Quantize only after parity is measured; record model byte size and SHA-256.
4. Implement browser-local autoregressive decoding / beam search and tokenizer behavior without network inference. Keep all runtime files and model assets inside the GitHub Pages deployment artifact.
5. Support CPU/WASM as the baseline and optional WebGPU only as an acceleration path; test both where available.
6. Keep raw neural IPA, parse status, unknown symbols, tone alignment and provenance inspectable. Never promote model tones beyond `UNCERTAIN`.
7. Add Python-vs-browser parity tests, long-input / 128-token rejection tests, cold-load and warm-inference latency, memory/load checks, and a clean Pages deployment smoke test.

Acceptance is **not** “the ONNX file exists”. It requires:
- exact model revision and tokenizer provenance;
- reproducible ONNX export and checksum;
- Python/browser decoded-IPA parity on pinned fixtures (including EOS / special-token behavior);
- exact Hybrid v2 tone-alignment parity on synthetic and real fixtures;
- no silent truncation or fallback;
- local-only network audit (model and runtime assets served by Pages; inference requests remain in-browser);
- Pages artifact size and browser memory/latency within documented limits;
- full Python, Node, Chromium and deployed-site checks.

## Task ledger

| Task | Status | Acceptance / blocker |
|---|---|---|
| Current Pages runtime identified | DONE_VERIFIED | `index.html` → `web/app.js` → `web/engine.js`; deterministic hybrid only |
| Browser Hybrid v2 IPA parser / tone combiner | PARTIAL | Implemented in branch; CI and Python/browser parity still required |
| Neural checkpoint ONNX export | TODO | Need a reproducible custom encoder–decoder export and parity proof |
| Browser-local tokenizer and autoregressive inference | TODO | No model runtime or ONNX graphs currently bundled |
| Pages-hosted model/runtime assets | TODO | Must be generated and included in `dist/`; exact size and license manifest required |
| Full browser Hybrid v2 UI integration | TODO | Must expose separate raw tonal IPA, parse status, alignment and `UNCERTAIN` predictions |
| Full exact-head / deployment verification | TODO | Run after integration; no deployment is claimed by this document |

**Current readiness:** existing GitHub Pages site remains an engineering-verified deterministic hybrid research prototype. Full neural Hybrid v2 is **not yet hosted**. This branch is an implementation increment, not a completed deployment.
