#!/usr/bin/env node
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { AutoTokenizer, env } from "@huggingface/transformers";
import * as ort from "onnxruntime-web/wasm";

const modelRoot = path.resolve(process.argv[2] ?? "artifacts/hybrid-v2-browser");
const manifest = JSON.parse(await fs.readFile(path.join(modelRoot, "manifest.json"), "utf8"));
env.localModelPath = `${modelRoot}${path.sep}`;
env.allowRemoteModels = false;
env.backends.onnx.wasm.wasmPaths = pathToFileURL(
  path.join(path.dirname(new URL(import.meta.url).pathname), "../node_modules/onnxruntime-web/dist") + path.sep,
).href;
env.backends.onnx.wasm.numThreads = 1;

function values(value) {
  if (value && typeof value.tolist === "function") return value.tolist().flat(Infinity).map(Number);
  if (value && value.data) return Array.from(value.data, Number);
  if (Array.isArray(value)) return value.flat(Infinity).map(Number);
  return Array.from(value, Number);
}

function int64(valuesArray, shape) {
  return new ort.Tensor("int64", BigInt64Array.from(valuesArray, (value) => BigInt(value)), shape);
}

async function runGraphPair(encoderPath, decoderPath, encoderTokenizer, fixtures, label) {
  const encoderSession = await ort.InferenceSession.create(
    await fs.readFile(encoderPath),
    { executionProviders: ["wasm"], graphOptimizationLevel: "disabled" },
  );
  const decoderSession = await ort.InferenceSession.create(
    await fs.readFile(decoderPath),
    { executionProviders: ["wasm"], graphOptimizationLevel: "disabled" },
  );
  const results = [];
  for (const fixture of fixtures) {
    const encoded = encoderTokenizer(fixture.input);
    const inputIds = values(encoded.input_ids);
    const attentionMask = values(encoded.attention_mask);
    const tokenTypeIds = encoded.token_type_ids
      ? values(encoded.token_type_ids)
      : inputIds.map(() => 0);
    assert.deepEqual(inputIds, fixture.encoder_input_ids, `${label}: encoder tokenizer IDs differ for ${fixture.input}`);
    assert.deepEqual(attentionMask, fixture.encoder_attention_mask, `${label}: encoder attention mask differs for ${fixture.input}`);
    assert.deepEqual(tokenTypeIds, fixture.encoder_token_type_ids, `${label}: encoder token types differ for ${fixture.input}`);
    const sourceLength = inputIds.length;
    assert.ok(sourceLength <= manifest.max_sequence_length, "encoder sequence exceeds the pinned model limit");

    const encoderOutputs = await encoderSession.run({
      input_ids: int64(inputIds, [1, sourceLength]),
      attention_mask: int64(attentionMask, [1, sourceLength]),
      token_type_ids: int64(tokenTypeIds, [1, sourceLength]),
    });
    const hidden = encoderOutputs.last_hidden_state;
    const generated = [manifest.decoder_start_token_id];
    while (generated.length < manifest.max_sequence_length) {
      const targetLength = generated.length;
      const decoderOutputs = await decoderSession.run({
        decoder_input_ids: int64(generated, [1, targetLength]),
        decoder_attention_mask: int64(generated.map(() => 1), [1, targetLength]),
        encoder_hidden_states: new ort.Tensor("float32", new Float32Array(hidden.data), hidden.dims),
        encoder_attention_mask: int64(attentionMask, [1, sourceLength]),
      });
      const logits = decoderOutputs.logits;
      const vocabSize = logits.dims.at(-1);
      const offset = (targetLength - 1) * vocabSize;
      let bestToken = 0;
      let bestScore = Number.NEGATIVE_INFINITY;
      for (let token = 0; token < vocabSize; token += 1) {
        const score = logits.data[offset + token];
        if (score > bestScore) {
          bestScore = score;
          bestToken = token;
        }
      }
      generated.push(bestToken);
      if (bestToken === manifest.eos_token_id) break;
    }
    assert.deepEqual(generated, fixture.expected_ids, `${label}: ONNX Runtime Web output IDs differ for ${fixture.input}`);
    results.push({ input: fixture.input, generated_ids: generated });
  }
  await encoderSession.release();
  await decoderSession.release();
  return results;
}

const encoderTokenizer = await AutoTokenizer.from_pretrained("encoder_tokenizer");
const decoderTokenizer = await AutoTokenizer.from_pretrained("decoder_tokenizer");
for (const fixture of manifest.parity_fixtures) {
  const decoded = decoderTokenizer.decode(fixture.expected_ids, { skip_special_tokens: true });
  assert.equal(decoded, fixture.decoded, `decoder tokenizer output differs for ${fixture.input}`);
}
const fp32 = await runGraphPair(
  path.join(modelRoot, "encoder.onnx"),
  path.join(modelRoot, "decoder.onnx"),
  encoderTokenizer,
  manifest.parity_fixtures,
  "FP32",
);
const int8 = await runGraphPair(
  path.join(modelRoot, "encoder.int8.onnx"),
  path.join(modelRoot, "decoder.int8.onnx"),
  encoderTokenizer,
  manifest.parity_fixtures,
  "INT8",
);
assert.equal(manifest.int8_exact_token_parity, true, "Python INT8 parity gate was not passed");
console.log(JSON.stringify({
  status: "ONNX_RUNTIME_WEB_WASM_AND_TOKENIZER_PARITY_VERIFIED",
  transformersJsVersion: "4.3.2",
  onnxRuntimeWebVersion: "1.31.1",
  fixtures: manifest.parity_fixtures.length,
  fp32,
  int8,
}, null, 2));
