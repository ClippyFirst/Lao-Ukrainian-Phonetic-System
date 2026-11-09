import test from "node:test";
import assert from "node:assert/strict";
import {
  combineNeuralTones,
  parseExternalIpa,
  unavailableHybridV2,
} from "./hybrid-v2.js";

const MODEL = {
  modelId: "byumatrixlab/lao-ipa-tonal",
  modelRevision: "e02608cfcb18abfe6b1916f5f4774bfac9ac788d",
};

function deterministic(statuses = ["SUPPORTED", "SUPPORTED"]) {
  return {
    status: "OK",
    output: "к'а да",
    syllables: statuses.map((status, index) => ({
      surface: index === 0 ? "ຂາ" : "ດາ",
      status: "ESTABLISHED",
      phoneticResult: {
        status,
        toneCategory: index === 0 ? "low-rising" : "high-rising",
      },
    })),
  };
}

test("external IPA parser preserves a supported segmental and tonal stream", () => {
  const parsed = parseExternalIpa("kʰaː˩˧daː˧˥");
  assert.equal(parsed.status, "SUPPORTED");
  assert.equal(parsed.phonemicIpa, "kʰaːdaː");
  assert.equal(parsed.toneContourIpa, "˩˧˧˥");
  assert.deepEqual(parsed.syllableBoundaries, [0, 4, 8]);
});

test("external IPA parser preserves raw text and fails closed on unknown symbols", () => {
  const raw = "kʰaː˩˧☃";
  const parsed = parseExternalIpa(raw);
  assert.equal(parsed.externalIpa, raw.normalize("NFC").trim());
  assert.equal(parsed.status, "UNSUPPORTED");
  assert.equal(parsed.segments.at(-1).kind, "unknown");
  assert.ok(parsed.uncertainty.includes("UNSUPPORTED-EXTERNAL-IPA-SYMBOLS"));
});

test("Hybrid v2 attaches only unique order-aligned contours and keeps them UNCERTAIN", () => {
  const source = deterministic();
  const result = combineNeuralTones(source, "kʰaː˩˧daː˧˥", MODEL);
  assert.equal(result.toneAlignmentStatus, "ORDER_ALIGNED");
  assert.equal(result.alignedSyllables, 2);
  assert.equal(result.tonePredictions.length, 2);
  assert.deepEqual(result.tonePredictions.map((item) => item.category), ["low-rising", "high-rising"]);
  assert.ok(result.tonePredictions.every((item) => item.certainty === "UNCERTAIN"));
  assert.equal(result.tonalIpa, "kʰaː˩˧daː˧˥");
  assert.equal(result.analysis, source);
  assert.equal(result.ukrainian, source.output);
});

test("Hybrid v2 does not associate tones when neural IPA is unsupported", () => {
  const result = combineNeuralTones(deterministic(), "kʰaː˩˧☃", MODEL);
  assert.equal(result.toneAlignmentStatus, "NOT_ALIGNED");
  assert.equal(result.tonePredictions.length, 0);
  assert.ok(result.warnings.some((warning) => warning.startsWith("NEURAL-IPA-UNSUPPORTED")));
});

test("Hybrid v2 does not guess an ambiguous contour decomposition", () => {
  const result = combineNeuralTones(deterministic(), "kʰaː˧˩˧", MODEL);
  assert.equal(result.toneAlignmentStatus, "NOT_ALIGNED");
  assert.equal(result.tonePredictions.length, 0);
  assert.ok(result.warnings.some((warning) => warning.includes("NOT-UNIQUELY-ALIGNED")));
});

test("Hybrid v2 keeps partial associations and marks disagreement", () => {
  const source = deterministic(["SUPPORTED", "UNSUPPORTED"]);
  const result = combineNeuralTones(source, "kʰaː˧˥daː˧˥", MODEL);
  assert.equal(result.toneAlignmentStatus, "PARTIAL");
  assert.equal(result.tonePredictions.length, 1);
  assert.equal(result.tonePredictions[0].certainty, "UNCERTAIN");
  assert.ok(result.warnings.some((warning) => warning.includes("DISAGREEMENT:0")));
  assert.ok(result.warnings.includes("NEURAL-TONE-UNASSOCIATED-UNRESOLVED-SYLLABLES:1"));
});

test("missing browser model is explicit and never claims neural success", () => {
  const source = deterministic();
  const result = unavailableHybridV2(source);
  assert.equal(result.toneAlignmentStatus, "NEURAL_UNAVAILABLE");
  assert.equal(result.ukrainian, source.output);
  assert.equal(result.warnings[0], "NEURAL-MODEL-NOT-BUNDLED");
});

test("Hybrid v2 rejects missing model provenance", () => {
  assert.throws(() => combineNeuralTones(deterministic(), "kʰaː˩˧", {}), /model id and immutable revision/);
});
