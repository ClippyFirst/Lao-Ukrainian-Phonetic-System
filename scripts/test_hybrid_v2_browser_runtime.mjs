#!/usr/bin/env node
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { AutoTokenizer, env } from "@huggingface/transformers";
import { createHybridV2Inference } from "../web/hybrid-v2-inference.js";
import { analyze } from "../web/engine.js";
import { combineNeuralTones } from "../web/hybrid-v2.js";

const modelRoot = path.resolve(process.argv[2] ?? "artifacts/hybrid-v2-browser");
const manifest = JSON.parse(await fs.readFile(path.join(modelRoot, "manifest.json"), "utf8"));
env.localModelPath = `${modelRoot}${path.sep}`;
env.allowLocalModels = true;
env.allowRemoteModels = false;
const wasmDirectory = path.resolve("node_modules/onnxruntime-web/dist") + path.sep;
const wasmRoot = pathToFileURL(wasmDirectory).href;

const encoderTokenizer = await AutoTokenizer.from_pretrained(path.join(modelRoot, "encoder_tokenizer"));
const decoderTokenizer = await AutoTokenizer.from_pretrained(path.join(modelRoot, "decoder_tokenizer"));
for (const fixture of manifest.parity_fixtures) {
  const encoded = encoderTokenizer(fixture.input);
  const inputIds = encoded.input_ids.tolist().flat(Infinity).map(Number);
  const attentionMask = encoded.attention_mask.tolist().flat(Infinity).map(Number);
  const tokenTypeIds = encoded.token_type_ids
    ? encoded.token_type_ids.tolist().flat(Infinity).map(Number)
    : inputIds.map(() => 0);
  assert.deepEqual(inputIds, fixture.encoder_input_ids, `encoder tokenizer IDs differ for ${fixture.input}`);
  assert.deepEqual(attentionMask, fixture.encoder_attention_mask, `encoder attention mask differs for ${fixture.input}`);
  assert.deepEqual(tokenTypeIds, fixture.encoder_token_type_ids, `encoder token types differ for ${fixture.input}`);
  const decoded = decoderTokenizer.decode(fixture.expected_ids, { skip_special_tokens: true });
  assert.equal(decoded, fixture.decoded, `decoder tokenizer output differs for ${fixture.input}`);
}

async function verifyPair(encoderName, decoderName, label) {
  const runner = createHybridV2Inference({
    modelRoot,
    wasmRoot,
    manifest,
    encoderModelBytes: new Uint8Array(await fs.readFile(path.join(modelRoot, encoderName))),
    decoderModelBytes: new Uint8Array(await fs.readFile(path.join(modelRoot, decoderName))),
  });
  const rows = [];
  for (const fixture of manifest.parity_fixtures) {
    const neural = await runner.transcribeRaw(fixture.input);
    assert.deepEqual(
      neural.generatedIds,
      fixture.beam5_expected_ids,
      `${label}: beam-five ONNX output IDs differ for ${fixture.input}`,
    );
    assert.equal(neural.rawIpa, fixture.beam5_decoded, `${label}: decoded IPA differs for ${fixture.input}`);
    const deterministic = analyze(fixture.input);
    const hybrid = combineNeuralTones(
      deterministic,
      neural.rawIpa,
      { modelId: neural.modelId, modelRevision: neural.modelRevision },
    );
    assert.equal(hybrid.neuralRawIpa, neural.rawIpa);
    assert.equal(hybrid.ukrainian, deterministic.output);
    assert.ok(hybrid.tonePredictions.every((prediction) => prediction.certainty === "UNCERTAIN"));
    rows.push({
      input: fixture.input,
      sourceTokenCount: neural.sourceTokenCount,
      generatedTokenCount: neural.generatedIds.length,
      rawIpa: neural.rawIpa,
      alignment: hybrid.toneAlignmentStatus,
      alignedSyllables: hybrid.alignedSyllables,
    });
  }
  await runner.release();
  return rows;
}

const fp32 = await verifyPair("encoder.onnx", "decoder.onnx", "FP32");
const int8 = await verifyPair("encoder.int8.onnx", "decoder.int8.onnx", "INT8");
assert.equal(manifest.int8_exact_token_parity, true, "Python INT8 greedy parity gate was not passed");
const report = {
  status: "TRANSFORMERS_JS_TOKENIZER_AND_ONNX_RUNTIME_WEB_WASM_BEAM5_PARITY_VERIFIED",
  transformersJsVersion: "4.3.2",
  onnxRuntimeWebVersion: "1.31.1",
  modelRevision: manifest.model_revision,
  beamSize: 5,
  fixtures: manifest.parity_fixtures.length,
  fp32,
  int8,
};
await fs.writeFile(
  path.join(modelRoot, "browser-runtime-parity.json"),
  JSON.stringify(report, null, 2) + "\n",
  "utf8",
);
console.log(JSON.stringify(report, null, 2));
