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


---

## Continuation update — browser ONNX/WASM implementation (2026-11-09)

The implementation has progressed beyond the initial TODO list above. This section supersedes the earlier task statuses where it conflicts.

### Implemented on `feat/pages-hybrid-v2-browser`

- **DONE_VERIFIED — pinned model export:** `scripts/export_hybrid_v2_browser_onnx.py` exports the immutable BERT encoder–decoder checkpoint into separate FP32 encoder/decoder ONNX graphs and dynamic per-channel INT8 graphs. It verifies the upstream weight SHA-256 and immutable revision, saves both tokenizers, and checks Python-vs-ONNX greedy token parity. Export workflow [#42696469630](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42696469630) completed successfully and uploaded artifact [13709122743](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42696469630/artifacts/13709122743).
- **DONE_VERIFIED — browser tokenizer / WASM beam-five parity:** Transformers.js 4.3.2 tokenizers and ONNX Runtime Web 1.31.1 WASM were tested against three pinned Lao fixtures. Encoder input IDs, attention masks and token-type IDs match; decoded beam-five output token IDs and IPA match Python for FP32 and INT8 graphs. The test writes `browser-runtime-parity.json` as evidence. This is implementation parity on three fixtures, not a linguistic accuracy claim.
- **DONE_VERIFIED — typed browser adapter:** `web/hybrid-v2.js` and its tests preserve raw neural IPA, parser warnings, unique tone alignment and UNCERTAIN model-derived predictions. The deterministic Ukrainian output is unchanged.
- **PARTIAL — browser UI and local runtime:** `web/hybrid-v2-inference.js` implements lazy local tokenizer loading, pinned model validation, ONNX Runtime Web WASM, beam-five decoding, and no network inference. `index.html` / `web/app.js` expose a separate on-demand Hybrid v2 panel. The static build bundles ONNX Runtime Web and places WASM assets under `web/vendor/`; `scripts/prepare_pages_model.py` only copies the pinned INT8 weights and tokenizers after the browser parity evidence gate.
- **DONE_VERIFIED — non-deploying Pages preview pipeline:** `.github/workflows/pages-hybrid-v2-preview.yml` builds the actual static artifact, runs Python/Node/Chromium checks, verifies model/runtime files and the 1 GB Pages artifact ceiling, and uploads a short-lived preview artifact. It does not deploy or modify GitHub Pages.

### Browser integration defect found and corrected

The first full Chromium inference attempt (preview run [#42696469101](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42696469101)) passed the existing 19 UI tests but failed the new model test because `AutoTokenizer.from_pretrained` was given absolute tokenizer URLs. Transformers.js resolves local tokenizer IDs relative to `env.localModelPath`; URL-shaped IDs were treated as Hub IDs and the loader could not find `tokenizer_class`. The runtime now passes the local subdirectory IDs `encoder_tokenizer` and `decoder_tokenizer`, matching the successful parity harness. Correction commit: `54063e92b52a476185c09a69947f54fb14afe756`.

The exact-head preview after this correction is [run #42696777234](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42696777234); at the time of this update it was still running its reproducible model export and full Chromium inference test. Do not mark the UI integration or deployment DONE_VERIFIED until this run passes.

### Current ledger

| Task | Status | Evidence / acceptance still required |
|---|---|---|
| Pinned FP32/INT8 ONNX export and Python greedy parity | DONE_VERIFIED | Export run #42696469630; pinned model revision and upstream weight hash enforced |
| Transformers.js tokenizer and ONNX Runtime Web WASM beam-five parity | DONE_VERIFIED | Three fixed fixtures; exact encoder tensors and decoded FP32/INT8 beam-five token IDs |
| Browser IPA parser and conservative tone association | DONE_VERIFIED | `web/hybrid-v2.test.js` and exact Python/browser fixture parity |
| Browser-local runtime and separate UI panel | PARTIAL | Chromium model test failed once on local tokenizer resolution; fix is in 54063e9; latest preview #42696777234 must pass |
| Pages runtime/model asset packaging | PARTIAL | Build and manifest gates implemented; exact preview artifact checks and live Pages deployment still required |
| Production GitHub Pages deployment | TODO | Requires merge to main after full exact-head tests, then successful Pages workflow and live asset/model smoke test |
| WebGPU acceleration | DEFERRED | WASM is the portable baseline; WebGPU is optional and not required for this first browser release |
| Phonetic accuracy / independent IPA gold | BLOCKED | No independent expert-adjudicated IPA gold; three parity fixtures validate implementation equivalence only |

### Deployment boundary

The branch is not yet live on GitHub Pages. The workflow changes are designed so that main-branch Pages deployment rebuilds the exact pinned model, validates browser parity, packages only INT8 model weights plus tokenizers, and deploys them as static assets. Inference stays in the user's browser; there is no API, external inference service or server-side runtime. The model and WASM assets are downloaded from the same Pages origin on first use and cached by the browser.

**Readiness at this checkpoint:** model export and browser-runtime parity are verified; full browser UI/deployment remains pending the latest preview. This is not yet a production deployment.


## Verification and packaging update — 2026-11-09, 21:07 UTC

### End-to-end browser proof

- **DONE_VERIFIED — full local inference on Chromium:** Pages preview [#42699110323](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42699110323) completed SUCCESS on head `e74602ef10ed55a0d6225d4914669c8de979d9f8`. It ran the Python export, FP32/INT8 tokenizer and beam-five parity, model preparation including Apache license/NOTICE, Chromium model inference, artifact checks and upload.
- Browser measurement for `ຂາ`: cold local-server run 1,272 ms; warm run 177 ms; output `kʰaː˩˧`; alignment `ORDER_ALIGNED`; parser `SUPPORTED`; external network requests: zero. These timings are CI/local-server measurements, not a guarantee for every user's download speed or device.
- **DONE_VERIFIED — static artifact size:** preview artifact [13709754651](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42698861280/artifacts/13709754651) is 40,377,012 bytes compressed and 56,452,048 bytes uncompressed. It contains 30 files, including only the required `ort-wasm-simd-threaded.mjs` and `ort-wasm-simd-threaded.wasm` WASM assets, 39.8 MB total INT8 model weights, tokenizer files, attribution NOTICE and Apache LICENSE. This removes unused WebGPU/JSEP, JSPI and Asyncify runtime variants.
- **DONE_VERIFIED — browser regression suite:** 20 Chromium tests passed on the completed preview run. The dedicated Hybrid v2 test checks cold/warm inference, model revision, beam=5, local-only requests, and tone alignment.
- **DONE_VERIFIED — package install reliability:** browser workflows install runtime packages with npm lifecycle scripts disabled. The app uses browser WASM, not the native Node ONNX backend; this avoids the unused native `onnxruntime-node` NuGet download that previously caused transient ETIMEDOUT failures. The exact-head Verify workflow passed after this change.

### Final test expansion and current branch state

The final browser test was expanded to submit `ສະບາຍດີ` after the aligned short example and assert that raw IPA `sa˧˥baːɲiː˧˥diː` remains visible while alignment is `NOT_ALIGNED` and no tone predictions are fabricated. Current PR head is `057fa8b5c819a022b24469e494684ec34436dbbc`. Exact-head preview [#42699464033](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42699464033) and Verify [#42699475181](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42699475181) were running at the time of this note; check their terminal results before merging.

The main Pages workflow now also smoke-tests the deployed Hybrid v2 UI, model manifest, both ONNX weights, both tokenizer JSONs, the exact WASM loader and binary, attribution NOTICE and Apache LICENSE. The PR is still not live on GitHub Pages. Production deployment remains TODO until exact-head gates pass, PR #158 is merged, the main Pages deployment succeeds, and its live smoke test passes.

### Current acceptance ledger

| Task | Status | Evidence / next acceptance |
|---|---|---|
| Pinned FP32/INT8 export and Python parity | DONE_VERIFIED | Export workflow #42696469630 |
| Transformers.js + WASM tokenizer and beam-five parity | DONE_VERIFIED | Three pinned fixtures; exact FP32/INT8 token parity |
| Browser-local Hybrid v2 inference | DONE_VERIFIED | Preview #42699110323; 1.272 s cold / 177 ms warm local run; zero external requests |
| Minimal static model/runtime package and notices | DONE_VERIFIED | Artifact #13709754651; 40.4 MB ZIP / 56.5 MB unpacked |
| Multi-syllable NOT_ALIGNED UI guard | PARTIAL | New exact-head preview #42699464033 must pass |
| Production GitHub Pages deployment | TODO | Merge after exact-head tests; verify live same-origin assets and inference |
| Independent phonetic accuracy | BLOCKED | No adjudicated IPA gold; runtime parity is not linguistic accuracy |

