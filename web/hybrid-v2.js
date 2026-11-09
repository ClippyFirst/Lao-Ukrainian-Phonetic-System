/**
 * Browser-side Hybrid v2 result combiner.
 *
 * The deterministic IPA/Ukrainian lane is authoritative. A tonal neural
 * inference provider may supply an untouched IPA string; this module parses
 * it for diagnostics and attaches tone metadata only when a unique ordered
 * contour decomposition matches the deterministic syllable count.
 *
 * This module does not load model weights or perform neural inference.
 */
const IPA_SYMBOLS = [
  "t͡ɕ", "t͡ʃ", "t͡s", "d͡z", "d͡ʒ", "d͡ʑ", "tɕʰ", "tɕʷ", "tɕ", "tɕ", "dʑ", "ɲ",
  "kʷʰ", "tʷʰ", "kʷ", "ʔʷ", "sʷ", "ŋʷ", "lʷ",
  "kʰ", "pʰ", "tʰ", "nʲ", "lʲ", "rʲ", "tʲ", "dʲ",
  "aː", "iː", "ɯː", "uː", "eː", "ɛː", "oː", "ɔː", "ɤː", "əː", "ə̯",
  "k", "p", "t", "d", "b", "ŋ", "m", "n", "s", "f",
  "h", "ɡ", "g", "x", "ɦ", "r", "l", "j", "ʋ", "w", "ʔ",
  "ʃ", "ʒ", "a", "i", "ɯ", "u", "e", "ɛ", "o", "ɔ", "ɤ", "ə",
];
const VOWELS = new Set([
  "aː", "iː", "ɯː", "uː", "eː", "ɛː", "oː", "ɔː", "ɤː", "əː", "ə̯",
  "a", "i", "ɯ", "u", "e", "ɛ", "o", "ɔ", "ɤ", "ə",
]);
const TONE_LETTERS = new Set(["˥", "˦", "˧", "˨", "˩"]);
const TONE_TO_CATEGORY = new Map([
  ["˩˧", "low-rising"],
  ["˧˥", "high-rising"],
  ["˧", "high-mid"],
  ["˧˩", "low-falling"],
  ["˥˨", "high-falling"],
]);
const SORTED_IPA = [...new Set(IPA_SYMBOLS)].sort((a, b) => b.length - a.length);
const SORTED_CONTOURS = [...TONE_TO_CATEGORY.keys()].sort((a, b) => b.length - a.length || a.localeCompare(b));

export function parseExternalIpa(rawIpa, { provenance = [] } = {}) {
  if (typeof rawIpa !== "string") {
    throw new TypeError("Neural IPA must be a string");
  }
  const raw = rawIpa.normalize("NFC").trim();
  if (!raw) {
    return {
      externalIpa: rawIpa, phonemicIpa: null, segments: [], syllableBoundaries: [0],
      toneContourIpa: null, status: "UNSUPPORTED", provenance: [...provenance],
      uncertainty: ["EMPTY-EXTERNAL-IPA"],
    };
  }

  const segments = [];
  const boundaries = [0];
  const toneLetters = [];
  let unsupported = false;
  for (let index = 0; index < raw.length;) {
    const char = raw[index];
    if (" .·‧".includes(char)) {
      if (boundaries.at(-1) !== segments.length) boundaries.push(segments.length);
      index += 1;
      continue;
    }
    if (TONE_LETTERS.has(char)) {
      toneLetters.push(char);
      segments.push({ ipa: char, kind: "tone", provenance: [...provenance], certainty: "SUPPORTED" });
      index += char.length;
      continue;
    }
    const symbol = SORTED_IPA.find((candidate) => raw.startsWith(candidate, index));
    if (!symbol) {
      unsupported = true;
      segments.push({ ipa: char, kind: "unknown", provenance: [...provenance], certainty: "UNSUPPORTED" });
      index += char.length;
      continue;
    }
    segments.push({
      ipa: symbol,
      kind: VOWELS.has(symbol) ? "vowel" : "consonant",
      provenance: [...provenance],
      certainty: "SUPPORTED",
    });
    index += symbol.length;
  }

  const segmentalIpa = segments.filter((segment) => segment.kind !== "tone")
    .map((segment) => segment.ipa).join("");
  if (!segmentalIpa) unsupported = true;
  if (boundaries.at(-1) !== segments.length) boundaries.push(segments.length);
  return {
    externalIpa: raw,
    phonemicIpa: segmentalIpa || null,
    segments,
    syllableBoundaries: boundaries,
    toneContourIpa: toneLetters.join("") || null,
    status: unsupported ? "UNSUPPORTED" : "SUPPORTED",
    provenance: [...provenance],
    uncertainty: unsupported ? ["UNSUPPORTED-EXTERNAL-IPA-SYMBOLS"] : [],
  };
}

function uniqueToneSequence(symbols, syllableCount) {
  if (!symbols || syllableCount < 1) return null;
  const solutions = [];
  function visit(offset, remaining, chosen) {
    if (solutions.length > 1) return;
    if (remaining === 0) {
      if (offset === symbols.length) solutions.push(chosen);
      return;
    }
    for (const contour of SORTED_CONTOURS) {
      if (symbols.startsWith(contour, offset)) {
        visit(offset + contour.length, remaining - 1, [...chosen, contour]);
      }
    }
  }
  visit(0, syllableCount, []);
  return solutions.length === 1 ? solutions[0] : null;
}

export function combineNeuralTones(
  deterministicAnalysis,
  neuralRawIpa,
  { modelId, modelRevision } = {},
) {
  if (!deterministicAnalysis || !Array.isArray(deterministicAnalysis.syllables)) {
    throw new TypeError("Hybrid v2 requires a deterministic analysis with syllables");
  }
  if (typeof modelId !== "string" || !modelId || typeof modelRevision !== "string" || !modelRevision) {
    throw new TypeError("Hybrid v2 requires an explicit model id and immutable revision");
  }

  const provenance = ["HYBRID-V2", "TONE-SOURCE:MEKONGPHON-TONAL", `MODEL:${modelId}`, `MODEL-REVISION:${modelRevision}`];
  const parsed = parseExternalIpa(neuralRawIpa, { provenance });
  const syllables = deterministicAnalysis.syllables.filter((item) => item.status !== "PASSTHROUGH" && !item.passthrough);
  const toneSymbols = parsed.segments.filter((segment) => segment.kind === "tone").map((segment) => segment.ipa).join("");
  const warnings = [];

  const base = {
    analysis: deterministicAnalysis,
    modelId,
    modelRevision,
    neuralRawIpa,
    tonalIpa: neuralRawIpa,
    toneAlignmentStatus: "NOT_ALIGNED",
    alignedSyllables: 0,
    tonePredictions: [],
    skippedToneUnits: syllables.length,
    warnings,
    ukrainian: deterministicAnalysis.output ?? syllables.map((item) => item.ukrainian || "?").join(""),
    neuralIpaParse: parsed,
  };

  if (parsed.status !== "SUPPORTED") {
    warnings.push("NEURAL-IPA-UNSUPPORTED; raw tonal IPA preserved; tone association withheld");
    return base;
  }
  const contours = uniqueToneSequence(toneSymbols, syllables.length);
  if (!contours) {
    warnings.push(
      "NEURAL-TONE-SEQUENCE-NOT-UNIQUELY-ALIGNED; raw tonal IPA preserved; " +
      `syllable-level association withheld (${toneSymbols.length} tone symbols for ${syllables.length} deterministic syllables)`,
    );
    return base;
  }

  warnings.push("NEURAL-TONE-SEQUENCE-ALIGNED-BY-ORDER; raw tonal IPA remains a separate lane");
  const predictions = [];
  let skipped = 0;
  contours.forEach((contour, index) => {
    const syllable = syllables[index];
    const current = syllable.phoneticResult;
    const category = TONE_TO_CATEGORY.get(contour);
    if (!current || !["SUPPORTED", "UNCERTAIN"].includes(current.status) || !current.toneCategory) {
      skipped += 1;
      return;
    }
    predictions.push({
      syllableIndex: index,
      sourceSurface: syllable.surface,
      contour,
      category,
      certainty: "UNCERTAIN",
      provenance: [...provenance, "ALIGNMENT:ORDER-ONLY"],
    });
    if (current.toneCategory !== category) {
      warnings.push(`DETERMINISTIC-NEURAL-TONE-DISAGREEMENT:${index}:${current.toneCategory}->${category}`);
    }
  });
  if (skipped) warnings.push(`NEURAL-TONE-UNASSOCIATED-UNRESOLVED-SYLLABLES:${skipped}`);
  return {
    ...base,
    toneAlignmentStatus: skipped === 0 ? "ORDER_ALIGNED" : "PARTIAL",
    alignedSyllables: contours.length,
    tonePredictions: predictions,
    skippedToneUnits: skipped,
  };
}

/**
 * Explicitly reports unavailable inference instead of pretending the
 * deterministic browser profile is the full neural Hybrid v2.
 */
export function unavailableHybridV2(deterministicAnalysis, reason = "NEURAL-MODEL-NOT-BUNDLED") {
  const syllables = deterministicAnalysis?.syllables?.filter(
    (item) => item.status !== "PASSTHROUGH" && !item.passthrough,
  ) ?? [];
  return {
    analysis: deterministicAnalysis,
    modelId: "byumatrixlab/lao-ipa-tonal",
    modelRevision: "e02608cfcb18abfe6b1916f5f4774bfac9ac788d",
    neuralRawIpa: "",
    tonalIpa: "",
    toneAlignmentStatus: "NEURAL_UNAVAILABLE",
    alignedSyllables: 0,
    tonePredictions: [],
    skippedToneUnits: syllables.length,
    warnings: [reason],
    ukrainian: deterministicAnalysis?.output ?? "",
  };
}
