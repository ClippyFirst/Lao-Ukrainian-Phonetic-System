import { PreTrainedTokenizer, env } from "@huggingface/transformers";
import * as ort from "onnxruntime-web/wasm";
import { combineNeuralTones } from "./hybrid-v2.js";

const DEFAULT_BEAM_SIZE = 5;
const DEFAULT_MAX_LENGTH = 128;
const MODEL_SUBDIRECTORY = "hybrid-v2";
const PASSTHROUGH_PUNCTUATION = new Set([",", "!", "?", ";", ":", "(", ")", "[", "]", "{", "}", "\"", "“", "”", "&", "%", "–", "…", "#", "/", "`", "+", "•", "ຯ"]);

function trailingSlash(value) {
  return value.endsWith("/") ? value : value + "/";
}

function flattenTensor(value) {
  if (value && typeof value.tolist === "function") {
    return value.tolist().flat(Infinity).map(Number);
  }
  if (value && value.data) return Array.from(value.data, Number);
  if (Array.isArray(value)) return value.flat(Infinity).map(Number);
  return Array.from(value, Number);
}

function int64Tensor(values, shape) {
  return new ort.Tensor(
    "int64",
    BigInt64Array.from(values, (value) => BigInt(value)),
    shape,
  );
}

function normalizeModelInput(value) {
  return String(value ?? "").normalize("NFC");
}

function validateModelInput(value, maxLength = DEFAULT_MAX_LENGTH) {
  const normalized = normalizeModelInput(value);
  if (!normalized.trim()) throw new RangeError("Lao input must be a non-empty string.");
  const codepoints = Array.from(normalized);
  if (codepoints.length > maxLength) {
    throw new RangeError(`Input is ${codepoints.length} code points; model limit is ${maxLength}. Automatic truncation is disabled.`);
  }
  for (const character of codepoints) {
    const cp = character.codePointAt(0);
    if ((cp < 0x20 && !["\n", "\t", "\r"].includes(character)) || (cp >= 0x7f && cp <= 0x9f)) {
      throw new RangeError("Input contains a control character.");
    }
    if (cp === 0x200b || (cp >= 0x0e80 && cp <= 0x0eff) ||
        /\s/u.test(character) || cp < 0x80 || PASSTHROUGH_PUNCTUATION.has(character)) {
      continue;
    }
    throw new RangeError(`Unsupported non-Lao character U+${cp.toString(16).toUpperCase().padStart(4, "0")}`);
  }
  return normalized;
}

async function fetchJson(url, label) {
  const response = await fetch(url, { cache: "force-cache" });
  if (!response.ok) throw new Error(`Не вдалося завантажити ${label}: HTTP ${response.status}`);
  return response.json();
}

async function loadStaticTokenizer(modelRoot, directory, supplied) {
  if (supplied) return supplied;
  const base = trailingSlash(modelRoot);
  const directoryUrl = base.startsWith("http://") || base.startsWith("https://") || base.startsWith("file:")
    ? new URL(directory + "/", base).href
    : base + directory + "/";
  const [tokenizerJson, tokenizerConfig] = await Promise.all([
    fetchJson(new URL("tokenizer.json", directoryUrl), `${directory}/tokenizer.json`),
    fetchJson(new URL("tokenizer_config.json", directoryUrl), `${directory}/tokenizer_config.json`),
  ]);
  return new PreTrainedTokenizer(tokenizerJson, tokenizerConfig);
}

async function fetchBytes(url, onProgress, label) {
  const response = await fetch(url, { cache: "force-cache" });
  if (!response.ok) throw new Error(`Не вдалося завантажити ${label}: HTTP ${response.status}`);
  const total = Number(response.headers.get("content-length")) || 0;
  if (!response.body?.getReader) {
    const bytes = new Uint8Array(await response.arrayBuffer());
    onProgress?.({ phase: "download", label, loaded: bytes.byteLength, total: total || bytes.byteLength });
    return bytes;
  }
  const reader = response.body.getReader();
  const chunks = [];
  let loaded = 0;
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(value);
    loaded += value.byteLength;
    onProgress?.({ phase: "download", label, loaded, total });
  }
  const bytes = new Uint8Array(loaded);
  let offset = 0;
  for (const chunk of chunks) {
    bytes.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return bytes;
}

function topK(logits, offset, vocabSize, k) {
  const best = [];
  for (let token = 0; token < vocabSize; token += 1) {
    const score = logits[offset + token];
    if (best.length < k) {
      best.push({ token, score });
      best.sort((a, b) => b.score - a.score || a.token - b.token);
      continue;
    }
    const tail = best[best.length - 1];
    if (score < tail.score || (score === tail.score && token > tail.token)) continue;
    best.pop();
    best.push({ token, score });
    best.sort((a, b) => b.score - a.score || a.token - b.token);
  }
  return best;
}

function normalizedBeamScore(beam) {
  return beam.score / Math.max(1, beam.generatedLength);
}

async function generateBeamSearch({
  encoderSession,
  decoderSession,
  encoderHidden,
  encoderAttentionMask,
  decoderStartTokenId,
  eosTokenId,
  maxLength = DEFAULT_MAX_LENGTH,
  beamSize = DEFAULT_BEAM_SIZE,
}) {
  const sourceLength = encoderAttentionMask.length;
  const hiddenSize = encoderHidden.dims[2];
  const hiddenData = encoderHidden.data;
  let active = Array.from({ length: beamSize }, (_, index) => ({
    ids: [decoderStartTokenId],
    score: index === 0 ? 0 : -1e9,
  }));
  const completed = [];

  for (let step = 1; step < maxLength && active.length; step += 1) {
    const batch = active.length;
    const targetLength = active[0].ids.length;
    const decoderIds = new Array(batch * targetLength);
    const decoderMask = new Array(batch * targetLength).fill(1);
    const repeatedHidden = new Float32Array(batch * sourceLength * hiddenSize);
    const repeatedEncoderMask = new Array(batch * sourceLength);
    active.forEach((beam, index) => {
      const start = index * targetLength;
      for (let position = 0; position < targetLength; position += 1) {
        decoderIds[start + position] = beam.ids[position];
      }
      repeatedHidden.set(
        hiddenData,
        index * sourceLength * hiddenSize,
      );
      for (let position = 0; position < sourceLength; position += 1) {
        repeatedEncoderMask[index * sourceLength + position] = encoderAttentionMask[position];
      }
    });

    const outputs = await decoderSession.run({
      decoder_input_ids: int64Tensor(decoderIds, [batch, targetLength]),
      decoder_attention_mask: int64Tensor(decoderMask, [batch, targetLength]),
      encoder_hidden_states: new ort.Tensor(
        "float32",
        repeatedHidden,
        [batch, sourceLength, hiddenSize],
      ),
      encoder_attention_mask: int64Tensor(
        repeatedEncoderMask,
        [batch, sourceLength],
      ),
    });
    const logits = outputs.logits.data;
    const vocabSize = outputs.logits.dims[2];
    const candidates = [];
    for (let beamIndex = 0; beamIndex < batch; beamIndex += 1) {
      const offset = (beamIndex * targetLength + targetLength - 1) * vocabSize;
      let maxLogit = Number.NEGATIVE_INFINITY;
      for (let token = 0; token < vocabSize; token += 1) {
        if (logits[offset + token] > maxLogit) maxLogit = logits[offset + token];
      }
      let expSum = 0;
      for (let token = 0; token < vocabSize; token += 1) {
        expSum += Math.exp(logits[offset + token] - maxLogit);
      }
      const logNormalizer = maxLogit + Math.log(expSum);
      const tokenCandidates = topK(logits, offset, vocabSize, 2 * beamSize);
      for (const candidate of tokenCandidates) {
        candidates.push({
          parent: beamIndex,
          token: candidate.token,
          score: active[beamIndex].score + candidate.score - logNormalizer,
        });
      }
    }
    candidates.sort((a, b) =>
      b.score - a.score || a.parent - b.parent || a.token - b.token,
    );

    const nextActive = [];
    for (let rank = 0; rank < Math.min(2 * beamSize, candidates.length); rank += 1) {
      const candidate = candidates[rank];
      const parent = active[candidate.parent];
      if (candidate.token === eosTokenId) {
        if (rank < beamSize) {
          completed.push({
            ids: parent.ids,
            score: candidate.score,
            generatedLength: parent.ids.length - 1,
          });
        }
      } else {
        nextActive.push({
          ids: [...parent.ids, candidate.token],
          score: candidate.score,
        });
        if (nextActive.length === beamSize) break;
      }
    }
    active = nextActive;
    if (completed.length >= beamSize) break;
  }

  for (const beam of active) {
    completed.push({
      ids: beam.ids,
      score: beam.score,
      generatedLength: beam.ids.length - 1,
    });
  }
  if (!completed.length) throw new Error("Neural beam search returned no candidate.");
  completed.sort((a, b) =>
    normalizedBeamScore(b) - normalizedBeamScore(a),
  );
  return [...completed[0].ids, eosTokenId];
}

export function createHybridV2Inference({
  modelRoot = new URL(`../models/${MODEL_SUBDIRECTORY}/`, import.meta.url).href,
  wasmRoot = new URL("./vendor/", import.meta.url).href,
  manifest: suppliedManifest = null,
  encoderModelBytes = null,
  decoderModelBytes = null,
  encoderTokenizer: suppliedEncoderTokenizer = null,
  decoderTokenizer: suppliedDecoderTokenizer = null,
  onProgress = null,
} = {}) {
  let loading = null;
  let state = null;

  async function load() {
    if (state) return state;
    if (loading) return loading;
    loading = (async () => {
      env.allowRemoteModels = false;
      env.backends.onnx.wasm.wasmPaths = trailingSlash(wasmRoot);
      env.backends.onnx.wasm.numThreads = 1;
      ort.env.wasm.wasmPaths = trailingSlash(wasmRoot);
      ort.env.wasm.numThreads = 1;

      const manifest = suppliedManifest ?? await fetch(
        new URL("manifest.json", trailingSlash(modelRoot)),
        { cache: "force-cache" },
      ).then((response) => {
        if (!response.ok) throw new Error(`Не вдалося завантажити маніфест моделі: HTTP ${response.status}`);
        return response.json();
      });
      if (manifest.model_id !== "byumatrixlab/lao-ipa-tonal" ||
          manifest.model_revision !== "e02608cfcb18abfe6b1916f5f4774bfac9ac788d") {
        throw new Error("Невідповідна або неперевірена версія моделі Hybrid v2.");
      }
      onProgress?.({ phase: "tokenizer", label: "Завантаження токенізаторів" });
      // Transformers.js resolves local tokenizer IDs relative to env.localModelPath.
      // Pass the subdirectory IDs (as in the parity harness), not absolute URLs:
      // AutoTokenizer treats URL-shaped model IDs as Hub IDs and misses tokenizer_config.json.
      const [encoderTokenizer, decoderTokenizer] = await Promise.all([
        AutoTokenizer.from_pretrained("encoder_tokenizer"),
        AutoTokenizer.from_pretrained("decoder_tokenizer"),
      ]);
      const [encoderBytes, decoderBytes] = await Promise.all([
        encoderModelBytes ?? fetchBytes(
          new URL("encoder.int8.onnx", trailingSlash(modelRoot)),
          onProgress,
          "encoder.int8.onnx",
        ),
        decoderModelBytes ?? fetchBytes(
          new URL("decoder.int8.onnx", trailingSlash(modelRoot)),
          onProgress,
          "decoder.int8.onnx",
        ),
      ]);
      onProgress?.({ phase: "runtime", label: "Ініціалізація локального WASM-рушія" });
      const sessionOptions = {
        executionProviders: ["wasm"],
        graphOptimizationLevel: "disabled",
      };
      const [encoderSession, decoderSession] = await Promise.all([
        ort.InferenceSession.create(encoderBytes, sessionOptions),
        ort.InferenceSession.create(decoderBytes, sessionOptions),
      ]);
      state = {
        manifest,
        encoderTokenizer,
        decoderTokenizer,
        encoderSession,
        decoderSession,
      };
      onProgress?.({ phase: "ready", label: "Нейромодель готова" });
      return state;
    })().catch((error) => {
      loading = null;
      throw error;
    });
    return loading;
  }

  async function transcribeRaw(text) {
    const normalized = validateModelInput(text);
    const loaded = await load();
    const encoded = loaded.encoderTokenizer(normalized);
    const inputIds = flattenTensor(encoded.input_ids);
    const attentionMask = flattenTensor(encoded.attention_mask);
    const tokenTypeIds = encoded.token_type_ids
      ? flattenTensor(encoded.token_type_ids)
      : inputIds.map(() => 0);
    if (inputIds.length > loaded.manifest.max_sequence_length) {
      throw new RangeError(
        `Токенізований ввід перевищує ліміт моделі: ${inputIds.length}/${loaded.manifest.max_sequence_length}; обрізання вимкнено.`,
      );
    }
    const encoderOutputs = await loaded.encoderSession.run({
      input_ids: int64Tensor(inputIds, [1, inputIds.length]),
      attention_mask: int64Tensor(attentionMask, [1, attentionMask.length]),
      token_type_ids: int64Tensor(tokenTypeIds, [1, tokenTypeIds.length]),
    });
    const generatedIds = await generateBeamSearch({
      encoderSession: loaded.encoderSession,
      decoderSession: loaded.decoderSession,
      encoderHidden: encoderOutputs.last_hidden_state,
      encoderAttentionMask: attentionMask,
      decoderStartTokenId: loaded.manifest.decoder_start_token_id,
      eosTokenId: loaded.manifest.eos_token_id,
      maxLength: loaded.manifest.max_sequence_length,
      beamSize: DEFAULT_BEAM_SIZE,
    });
    const rawIpa = loaded.decoderTokenizer.decode(
      generatedIds,
      { skip_special_tokens: true },
    );
    return {
      rawIpa,
      generatedIds,
      sourceTokenCount: inputIds.length,
      modelId: loaded.manifest.model_id,
      modelRevision: loaded.manifest.model_revision,
      numBeams: DEFAULT_BEAM_SIZE,
    };
  }

  async function run(deterministicAnalysis, text) {
    const neural = await transcribeRaw(text);
    const combined = combineNeuralTones(
      deterministicAnalysis,
      neural.rawIpa,
      { modelId: neural.modelId, modelRevision: neural.modelRevision },
    );
    return {
      ...combined,
      numBeams: neural.numBeams,
      sourceTokenCount: neural.sourceTokenCount,
    };
  }

  async function release() {
    if (!state) return;
    await Promise.all([
      state.encoderSession.release(),
      state.decoderSession.release(),
    ]);
    state = null;
    loading = null;
  }

  return { load, transcribeRaw, run, release };
}
