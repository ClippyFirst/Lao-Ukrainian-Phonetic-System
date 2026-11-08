import { CONSONANTS, ONSET_CLUSTERS, VOWELS, CODAS, CORRESPONDENCES, TONE_MARKS, TONE_RULES, SPECIAL_TONE_RULES, GRAPHEME_INVENTORY } from "./data.js";

const TONE_MARK_SET = new Set(Object.keys(TONE_MARKS));
const POTENTIAL_MINOR_TONE_RULE = SPECIAL_TONE_RULES.find(
  ([ruleId]) => ruleId === "VNT-POTENTIAL-MINOR-OPEN-A-UNRESOLVED"
);
const MINOR_C0_EXCLUDED_ONSETS = new Set(["ງ", "ຍ"]);
const HIGH_DIGRAPHS = new Map([
  ["ຫງ", "ງ"], ["ຫຍ", "ຍ"], ["ຫນ", "ນ"], ["ຫມ", "ມ"],
  ["ຫລ", "ລ"], ["ຫຼ", "ລ"], ["ຫວ", "ວ"],
]);
const VOWEL_COMBINING_MARKS = new Set(["ັ", "ິ", "ີ", "ຶ", "ື", "ຸ", "ູ", "ົ", "ໍ"]);
const sortedIpa = () => Object.keys(CORRESPONDENCES).sort((a, b) => b.length - a.length);

function vowelById(id) { return VOWELS.find((v) => v[0] === id) || null; }

function matchVowel(before, after) {
  const push = (id, consumed = "") => {
    const v = vowelById(id);
    return v ? { v, consumed } : null;
  };
  if (before === "" && after.startsWith("ຽ")) return push("IA_LONG", "ຽ");
  if (before.endsWith("ເ")) {
    if (after.startsWith("ັຽ")) return push("IA_LONG", "ັຽ");
    if (after.startsWith("ັຍ")) return push("IA", "ັຍ");
    // ເ◌ຽ is not an established preposed IA spelling in the cited
    // orthography reference. Leave it unconsumed rather than guessing.
    if (after.startsWith("ຍ")) return push("IA_LONG", "ຍ");
    if (after.startsWith("ຶອ")) return push("UA", "ຶອ");
    if (after.startsWith("ືອ")) return push("UA_LONG", "ືອ");
    if (after.startsWith("ົາ")) return push("AW_LONG", "ົາ");
    if (after.startsWith("າະ")) return push("AW", "າະ");
    if (after.startsWith("ິ")) return push("OE", "ິ");
    if (after.startsWith("ີ")) return push("OEE", "ີ");
    if (after.startsWith("ະ")) return push("E", "ະ");
    if (after.startsWith("ັ")) return push("E", "ັ");
    return push("EE");
  }
  if (before.endsWith("ແ")) {
    if (after.startsWith("ະ")) return push("AE", "ະ");
    if (after.startsWith("ັ")) return push("AE", "ັ");
    return push("AEE");
  }
  if (before.endsWith("ໂ")) {
    if (after.startsWith("ະ")) return push("O", "ະ");
    if (after.startsWith("ົ")) return push("O", "ົ");
    return push("OO");
  }
  if (before.endsWith("ໄ")) return push("AI");
  if (before.endsWith("ໃ")) return push("AI2");
  if (after.startsWith("ັວ")) return push("UO_SHORT_ALT", "ັວ");
  if (after.startsWith("ົວະ")) return push("UO", "ົວະ");
  if (after.startsWith("ົວ")) return push("UO_LONG", "ົວ");
  if (after.startsWith("ວາ")) return push("UO_LONG_OPEN", "ວາ");
  if (after.startsWith("ວ")) return push("UO_LONG_ALT", "ວ");
  if (after.startsWith("ຳ")) return push("AM", "ຳ");
  if (after.startsWith("ໍ")) return push("AWW", "ໍ");
  if (after.startsWith("ັອ")) return push("AWW_SHORT_ALT", "ັອ");
  if (after.startsWith("ອ")) return push("AWW_MEDIAL", "ອ");
  if (after.startsWith("ົ")) return push("O", "ົ");
  if (after.startsWith("ະ")) return push("A", "ະ");
  if (after.startsWith("ັ")) return push("A2", "ັ");
  if (after.startsWith("າ")) return push("AA", "າ");
  if (after.startsWith("ິ")) return push("I", "ິ");
  if (after.startsWith("ີ")) return push("II", "ີ");
  if (after.startsWith("ຶ")) return push("Y", "ຶ");
  if (after.startsWith("ື")) return push("YY", "ື");
  if (after.startsWith("ຸ")) return push("U", "ຸ");
  if (after.startsWith("ູ")) return push("UU", "ູ");
  return null;
}

function classify(coda, vowel) {
  if (coda) {
    const final = CODAS[coda];
    if (["p", "t", "k", "ʔ"].includes(final)) return "dead";
    if (["m", "n", "ŋ", "w", "j", "l", "r"].includes(final)) return "live";
  }
  if (vowel?.[6] === "diphthong" || vowel?.[7] === "nasal") return "live";
  return vowel?.[3] === "long" ? "live" : "dead";
}

function toneFor(cls, syllableType, length, mark) {
  const markName = mark ? (TONE_MARKS[mark] || "unknown") : "none";
  const row = TONE_RULES.find((r) => r[0] === cls &&
    (r[1] === "*" || r[1] === syllableType) &&
    (r[2] === "*" || r[2] === length) &&
    r[3] === markName);
  return row ? { name: row[4], contour: row[5], status: "ESTABLISHED", ruleId: row[6] }
    : { name: null, contour: null, status: "ANALYSIS DEPENDENT", ruleId: "TONE-NOT-ESTABLISHED-FOR-COMBINATION" };
}

const IPA_SYMBOLS = [
  "t͡ɕ", "t͡ʃ", "t͡s", "d͡z", "d͡ʒ", "d͡ʑ", "tɕʰ", "tɕ", "dʑ", "ɲ",
  "kʰ", "pʰ", "tʰ", "nʲ", "lʲ", "rʲ", "tʲ", "dʲ",
  "aː", "iː", "ɯː", "uː", "eː", "ɛː", "oː", "ɔː", "ɤː", "əː", "ə̯",
  "k", "p", "t", "d", "b", "ŋ", "m", "n", "s", "f",
  "h", "ɡ", "g", "x", "ɦ", "r", "l", "j", "ʋ", "w", "ʔ",
  "ʃ", "ʒ", "a", "i", "ɯ", "u", "e", "ɛ", "o", "ɔ", "ɤ", "ə",
];
const IPA_VOWELS = new Set([
  "aː", "iː", "ɯː", "uː", "eː", "ɛː", "oː", "ɔː", "ɤː", "əː", "ə̯",
  "a", "i", "ɯ", "u", "e", "ɛ", "o", "ɔ", "ɤ", "ə",
]);

function createPhoneticResult(ipa, metadata = {}) {
  const base = {
    phonemicIpa: ipa || null,
    broadSurfaceIpa: null,
    externalIpa: null,
    segments: [],
    syllableBoundaries: [0],
    vowelLength: metadata.vowelLength || null,
    toneCategory: metadata.toneCategory || null,
    toneContourIpa: metadata.toneContourIpa || null,
    status: ipa ? (metadata.status || "SUPPORTED") : "UNSUPPORTED",
    provenance: [...(metadata.provenance || [])],
    uncertainty: [...(metadata.uncertainty || [])],
  };
  if (!ipa) return base;
  const symbols = [...IPA_SYMBOLS].sort((left, right) => right.length - left.length);
  let i = 0;
  let unsupported = false;
  while (i < ipa.length) {
    const symbol = symbols.find((candidate) => ipa.startsWith(candidate, i));
    if (!symbol) {
      unsupported = true;
      base.segments.push({ ipa: ipa[i], kind: "unknown", provenance: base.provenance, certainty: "UNSUPPORTED" });
      i += 1;
      continue;
    }
    base.segments.push({
      ipa: symbol,
      kind: IPA_VOWELS.has(symbol) ? "vowel" : "consonant",
      provenance: base.provenance,
      certainty: "SUPPORTED",
    });
    i += symbol.length;
  }
  base.syllableBoundaries = [0, base.segments.length];
  if (unsupported) {
    base.status = "UNSUPPORTED";
    base.uncertainty.push("UNSUPPORTED-IPA-SEGMENT");
  }
  return base;
}

function adaptPhoneticResult(result, { allowUncertain = false } = {}) {
  if (!result || typeof result !== "object" || !Array.isArray(result.segments)) {
    throw new TypeError("Ukrainian adaptation requires a typed PhoneticResult");
  }
  if (result.status === "PROVISIONAL") {
    if (!result.segments.length) return "?";
    let output = "";
    let provisionalRun = [];
    const flushRun = () => {
      if (!provisionalRun.length) return;
      const run = provisionalRun;
      provisionalRun = [];
      const mapped = adaptPhoneticResult({
        ...result,
        segments: run,
        syllableBoundaries: [0, run.length],
        status: "SUPPORTED",
      });
      output += mapped ?? "?";
    };
    for (const segment of result.segments) {
      if (segment?.kind === "unknown") {
        flushRun();
        if (segment.ipa !== "?" || segment.certainty !== "PROVISIONAL") return null;
        output += "?";
      } else if (["vowel", "consonant"].includes(segment?.kind) &&
          segment.certainty === "PROVISIONAL") {
        provisionalRun.push({ ...segment, certainty: "SUPPORTED" });
      } else {
        return null;
      }
    }
    flushRun();
    return output || "?";
  }
  if (!(result.status === "SUPPORTED" || (allowUncertain && result.status === "UNCERTAIN")) || result.segments.length === 0 ||
      result.segments.some((segment) => segment?.certainty !== "SUPPORTED")) return null;
  const ipa = result.segments.map((segment) => segment.ipa).join("");
  const keys = sortedIpa();
  let output = "";
  let i = 0;

  // Yodated Ukrainian letters are used only for syllable-initial /j/
  // followed by a monophthong; a vowel sequence remains explicit.
  const initialYodated = {
    a: "я", "aː": "я",
    e: "є", "eː": "є", ɛ: "є", "ɛː": "є",
    i: "ї", "iː": "ї",
    o: "йо", "oː": "йо", ɔ: "йо", "ɔː": "йо",
    u: "ю", "uː": "ю",
    ɯ: "йи", "ɯː": "йи",
    ɤ: "йе", "ɤː": "йе",
  };
  if (result.segments.length >= 2 &&
      result.segments[0].ipa === "j" &&
      result.segments[1].kind === "vowel" &&
      Object.hasOwn(initialYodated, result.segments[1].ipa) &&
      (result.segments.length === 2 || result.segments[2].kind !== "vowel")) {
    output += initialYodated[result.segments[1].ipa];
    i = result.segments[0].ipa.length + result.segments[1].ipa.length;
  }
  while (i < ipa.length) {
    const key = keys.find((candidate) => ipa.startsWith(candidate, i));
    if (!key) return null;
    output += CORRESPONDENCES[key];
    i += key.length;
  }
  return output;
}

const PREVIEW_VOWEL_GRAPHEMES = new Set("ະັາິີຶືຸູົຽອໍຳເແໂໃໄ");
const PREVIEW_STRUCTURAL_ONLY = new Set([
  "PALI_ONLY", "NON_CORE_NO_MODERN_IPA", "OUT_OF_SCOPE_KHMU",
  "NOT_USED_MODERN_LAO", "NONPHONOLOGICAL", "ORTHOGRAPHIC_ONLY"
]);

function previewFromGraphemes(surface, parsed) {
  const chars = [...surface];
  const roles = new Map();
  const ipaParts = [];
  const unresolved = [];
  const warnings = [];
  for (let i = 0; i < chars.length; i++) {
    if (Object.hasOwn(TONE_MARKS, chars[i])) {
      roles.set(i, { grapheme: chars[i], role: "tone-mark", ipaHint: null, certainty: "STRUCTURAL_ONLY" });
    }
  }

  const onsetForm = parsed.onsetForm || parsed.onset;
  const onsetIndex = onsetForm ? surface.indexOf(onsetForm) : -1;
  const onsetLength = onsetIndex >= 0 ? [...onsetForm].length : 0;
  let onsetIpa = null;
  if (onsetIndex >= 0 && onsetLength) {
    if (Object.hasOwn(ONSET_CLUSTERS, onsetForm)) {
      onsetIpa = ONSET_CLUSTERS[onsetForm][1];
      roles.set(onsetIndex, { grapheme: chars[onsetIndex], role: "labialized-onset-unit", ipaHint: onsetIpa, certainty: "PROVISIONAL", structuralUnit: onsetForm });
      for (let i = onsetIndex + 1; i < onsetIndex + onsetLength; i++) {
        roles.set(i, { grapheme: chars[i], role: "labialization-component", ipaHint: null, certainty: "PROVISIONAL", structuralUnit: onsetForm });
      }
    } else if (HIGH_DIGRAPHS.has(onsetForm)) {
      const base = HIGH_DIGRAPHS.get(onsetForm);
      onsetIpa = CONSONANTS[base]?.[1] || null;
      roles.set(onsetIndex, { grapheme: chars[onsetIndex], role: "silent-high-class-modifier", ipaHint: null, certainty: "STRUCTURAL_ONLY", structuralUnit: onsetForm });
      roles.set(onsetIndex + 1, { grapheme: chars[onsetIndex + 1], role: "high-class-onset", ipaHint: onsetIpa, certainty: "PROVISIONAL", structuralUnit: onsetForm });
    } else {
      onsetIpa = parsed.onset === "ອ" ? "" : (CONSONANTS[parsed.onset]?.[1] || null);
      const role = parsed.onset === "ອ" ? "vowel-carrier" : "syllable-onset";
      roles.set(onsetIndex, { grapheme: chars[onsetIndex], role, ipaHint: onsetIpa || null, certainty: "PROVISIONAL", structuralUnit: onsetForm });
    }
    if (onsetIpa) ipaParts.push(onsetIpa);
  }

  const vowel = VOWELS.find((row) => row[0] === parsed.vowelId);
  if (vowel?.[2]) {
    ipaParts.push(vowel[2]);
    const vowelIndices = chars.map((ch, i) => PREVIEW_VOWEL_GRAPHEMES.has(ch) && !roles.has(i) ? i : -1).filter((i) => i >= 0);
    const unit = vowelIndices.map((i) => chars[i]).join("");
    vowelIndices.forEach((i, offset) => roles.set(i, {
      grapheme: chars[i], role: "vowel-structure-component",
      ipaHint: offset === 0 ? vowel[2] : null, certainty: "PROVISIONAL",
      structuralUnit: unit || null
    }));
  }

  const coda = parsed.coda && parsed.coda !== "—" ? parsed.coda : null;
  if (coda) {
    const i = chars.map((ch, index) => ch === coda && !roles.has(index) ? index : -1).filter((index) => index >= 0).at(-1) ?? -1;
    const codaIpa = CODAS[coda];
    if (codaIpa && i >= 0) {
      ipaParts.push(codaIpa);
      roles.set(i, { grapheme: chars[i], role: "syllable-coda", ipaHint: codaIpa, certainty: "PROVISIONAL", structuralUnit: coda });
    }
  }

  for (let i = 0; i < chars.length; i++) {
    if (roles.has(i)) continue;
    const ch = chars[i];
    const inventory = GRAPHEME_INVENTORY[ch];
    const role = inventory?.structuralRole || (CONSONANTS[ch] ? "unresolved-consonant-position" : PREVIEW_VOWEL_GRAPHEMES.has(ch) ? "unresolved-vowel-component" : "unregistered-grapheme");
    const certainty = inventory && PREVIEW_STRUCTURAL_ONLY.has(inventory.engineStatus) ? "STRUCTURAL_ONLY" : "UNRESOLVED";
    roles.set(i, { grapheme: ch, role, ipaHint: null, certainty });
    unresolved.push(ch);
  }

  if (!ipaParts.length) warnings.push("NO_CONFIDENT_SEGMENTAL_HINT");
  if (unresolved.length) warnings.push("UNRESOLVED_GRAPHEME_OR_POSITION");
  warnings.push(...(parsed.warnings || []), "TONE_NOT_INFERRED_BY_GRAPHEME_PREVIEW");
  const uniqueWarnings = [...new Set(warnings)];
  const ipaPreview = ipaParts.join("") || null;
  let phoneticResult = null;
  if (ipaPreview) {
    phoneticResult = createPhoneticResult(ipaPreview, {
      vowelLength: vowel?.[3] || null,
      status: "PROVISIONAL",
      provenance: ["GRAPHEME-POSITION-PREVIEW"],
      uncertainty: uniqueWarnings
    });
    phoneticResult.segments = phoneticResult.segments.map((segment) => ({ ...segment, certainty: "PROVISIONAL" }));
  }
  return {
    ipaPreview,
    status: ipaPreview ? "PROVISIONAL" : "UNRESOLVED",
    graphemes: chars.map((_, index) => roles.get(index)),
    unresolvedGraphemes: unresolved,
    warnings: uniqueWarnings,
    phoneticResult
  };
}

const PASSTHROUGH_PUNCTUATION = new Set(Array.from(",!?;:()[]{}\"“”&%–…#/`+•"));

function isPassthroughChar(ch) {
  if (PASSTHROUGH_PUNCTUATION.has(ch) || /^[0-9A-Za-z.'-]$/u.test(ch) || /^[\\u0ED0-\\u0ED9]$/u.test(ch)) return true;
  const cp = ch.codePointAt(0);
  // Hybrid preserves foreign-script letters, typographic punctuation,
  // symbols and combining marks as visible passthrough units. They are never
  // reinterpreted as Lao phonemes and do not invalidate neighbouring Lao.
  return cp > 0x7F && !(cp >= 0x0E80 && cp <= 0x0EFF) &&
    !/\\s/u.test(ch) && !/[\\u0000-\\u001F\\u007F-\\u009F\\uFEFF]/u.test(ch);
}

function validateInput(text) {
  const warnings = [];
  for (const ch of text) {
    const cp = ch.codePointAt(0);
    if ((cp < 0x20 && !["\n", "\t", "\r"].includes(ch)) || (cp >= 0x7F && cp <= 0x9F)) {
      warnings.push("Вхід містить керівний символ.");
      continue;
    }
    if (cp === 0x200B) continue; // Lao word-boundary zero-width space.
    if (cp >= 0x0E80 && cp <= 0x0EFF) continue;
    if ((ch !== "\uFEFF" && /\s/.test(ch)) || cp < 0x80 || PASSTHROUGH_PUNCTUATION.has(ch)) continue;
    if (cp > 0x7F) warnings.push("Непідтримуваний символ поза лаоським Unicode-діапазоном.");
  }
  return [...new Set(warnings)];
}

function findOnset(clean) {
  for (let index = 0; index < clean.length; index++) {
    for (const [form, target] of HIGH_DIGRAPHS) {
      if (clean.startsWith(form, index)) {
        return { onsetKey: target, onsetIndex: index, onsetLength: [...form].length, onsetClass: "high", onsetForm: form };
      }
    }
    const onsetKey = clean[index];
    if (Object.hasOwn(CONSONANTS, onsetKey)) {
      return { onsetKey, onsetIndex: index, onsetLength: 1, onsetClass: CONSONANTS[onsetKey][0], onsetForm: onsetKey };
    }
  }
  return null;
}

function parseVowelCandidate(clean, before, onsetIndex, onsetLength) {
  const after = clean.slice(onsetIndex + onsetLength);
  const matched = matchVowel(before, after);
  if (!matched) return null;
  const remainder = after.slice(matched.consumed.length);
  const finalChar = [...remainder].at(-1);
  const coda = finalChar && Object.hasOwn(CODAS, finalChar) ? finalChar : null;
  const unconsumed = coda ? remainder.slice(0, -1) : remainder;
  const warnings = [];
  if (unconsumed) warnings.push("Невикористана частина структури складу: " + unconsumed);
  if (!coda && ["A2", "AWW_SHORT_ALT"].includes(matched.v[0])) {
    warnings.push("SHORT_VOWEL_REQUIRES_CODA:" + matched.v[0]);
  }
  return {
    matched, coda, warnings, complete: warnings.length === 0,
    rounded: ["u", "o", "ɔ"].some((prefix) => matched.v[2].startsWith(prefix)),
  };
}

function toneMarkOrderError(chars, clean, found) {
  const positions = chars.map((ch, index) => TONE_MARK_SET.has(ch) ? index : -1).filter((index) => index >= 0);
  if (positions.length !== 1) return null;
  const markIndex = positions[0];
  if (!found) return "MALFORMED_TONE_MARK_POSITION";
  const cleanMarkIndex = chars.slice(0, markIndex).filter((ch) => !TONE_MARK_SET.has(ch)).length;
  const onsetBoundary = found.onsetIndex + found.onsetLength;
  const cleanChars = [...clean];
  const afterOnset = cleanMarkIndex === onsetBoundary;
  const afterLabializedSecond = cleanMarkIndex === onsetBoundary + 1 &&
    cleanChars[onsetBoundary] === "ວ" && Object.values(ONSET_CLUSTERS).some((row) => row[0] === found.onsetKey);
  const afterCombiningVowel = markIndex > 0 && VOWEL_COMBINING_MARKS.has(chars[markIndex - 1]);
  if (chars.slice(markIndex + 1).some((ch) => VOWEL_COMBINING_MARKS.has(ch))) {
    return "MALFORMED_TONE_MARK_ORDER";
  }
  return afterOnset || afterLabializedSecond || afterCombiningVowel
    ? null : "MALFORMED_TONE_MARK_POSITION";
}


const HYBRID_RULES = [
  ...Object.entries({
    AW_LONG: "ao", UA_LONG: "ɯːə̯", IA_LONG: "iaː", OEE: "əː",
    AI: "aj", UO_LONG: "uaː", UO_LONG_ALT: "uaː", AI2: "aj", OE: "ə",
  }).map(([id, value]) => ({
    ruleId: "HYB-MPH-VOWEL-" + id, target: "vowel",
    conditions: { vowelId: id }, value, priority: 0,
    provenance: "IPA-PROFILE-MEKONGPHON-VOWEL:" + id,
  })),
  ...Object.entries({ "ວ": "w", "ຣ": "r" }).map(([onset, value]) => ({
    ruleId: "HYB-MPH-ONSET-" + onset, target: "onset",
    conditions: { onset }, value, priority: 0,
    provenance: "IPA-PROFILE-MEKONGPHON-ONSET:" + onset,
  })),
];

function selectHybridRule(target, context) {
  const matches = HYBRID_RULES.filter((rule) =>
    rule.target === target &&
    Object.entries(rule.conditions).every(([key, expected]) => context[key] === expected)
  );
  if (!matches.length) return null;
  const rank = (rule) => [rule.priority, Object.keys(rule.conditions).length];
  const bestRank = matches.map(rank).sort((a, b) => b[0] - a[0] || b[1] - a[1])[0];
  const best = matches.filter((rule) => {
    const r = rank(rule);
    return r[0] === bestRank[0] && r[1] === bestRank[1];
  });
  if (new Set(best.map((rule) => rule.value)).size > 1) {
    throw new RangeError("Conflicting hybrid IPA rules: " + best.map((rule) => rule.ruleId).sort().join(", "));
  }
  return best.sort((a, b) => a.ruleId.localeCompare(b.ruleId))[0];
}

function analyzeToken(surface, ipaProfile = "hybrid-deterministic") {
  const chars = [...surface];
  const toneMarkCount = chars.filter((ch) => TONE_MARK_SET.has(ch)).length;
  if (toneMarkCount > 1) {
    return { surface, status: "EVIDENCE LIMITED", warnings: ["MULTIPLE_TONE_MARKS: phonetic output withheld."], ipa: null, ukrainian: null, tone: null };
  }
  const mark = chars.find((ch) => TONE_MARK_SET.has(ch)) || null;
  const clean = chars.filter((ch) => !TONE_MARK_SET.has(ch)).join("");
  const found = findOnset(clean);
  const markOrderError = toneMarkOrderError(chars, clean, found);
  if (markOrderError) {
    return { surface, status: "EVIDENCE LIMITED", warnings: [markOrderError + ": phonetic output withheld."], ipa: null, ukrainian: null, tone: null };
  }
  if (!found) return { surface, status: "EVIDENCE LIMITED", warnings: ["Не знайдено сучасний початковий приголосний у реєстрі."], ipa: null, ukrainian: null, tone: null, toneContour: null };

  const { onsetKey, onsetIndex, onsetLength, onsetClass } = found;
  const onset = CONSONANTS[onsetKey];
  const before = clean.slice(0, onsetIndex);
  const allowedPreposed = new Set(["", "ເ", "ແ", "ໂ", "ໃ", "ໄ"]);
  if (!allowedPreposed.has(before)) return { surface, status: "EVIDENCE LIMITED", warnings: ["Непідтримуваний фрагмент перед початковим приголосним: " + before], ipa: null, ukrainian: null, tone: null, toneContour: null };

  let selectedLength = onsetLength;
  let onsetForm = found.onsetForm;
  let onsetIpaOverride = null;
  let candidate = parseVowelCandidate(clean, before, onsetIndex, onsetLength);
  const clusterRow = onsetLength === 1 ? ONSET_CLUSTERS[clean.slice(onsetIndex, onsetIndex + 2)] : null;
  if (clusterRow) {
    const baseCandidate = candidate;
    const clusterCandidate = parseVowelCandidate(clean, before, onsetIndex, 2);
    if (clusterCandidate?.rounded) {
      if (!baseCandidate?.complete) {
        return { surface, onset: onsetKey, status: "EVIDENCE LIMITED",
          warnings: ["LABIALIZED_ONSET_BEFORE_ROUNDED_VOWEL: phonetic output withheld."],
          ukrainian: null, ipa: null, tone: null };
      }
    } else if (baseCandidate?.complete && clusterCandidate?.complete) {
      return { surface, onset: onsetKey, status: "EVIDENCE LIMITED",
        warnings: ["AMBIGUOUS_LABIALIZED_ONSET_VOWEL_BOUNDARY: phonetic output withheld."],
        ukrainian: null, ipa: null, tone: null };
    } else if (clusterCandidate?.complete || (!baseCandidate && clusterCandidate)) {
      candidate = clusterCandidate;
      selectedLength = 2;
      onsetForm = clean.slice(onsetIndex, onsetIndex + 2);
      onsetIpaOverride = clusterRow[1];
    } else if (!baseCandidate && clusterCandidate) {
      candidate = clusterCandidate;
      selectedLength = 2;
      onsetForm = clean.slice(onsetIndex, onsetIndex + 2);
      onsetIpaOverride = clusterRow[1];
    }
  }

  if (!candidate) return { surface, onset: onsetKey, status: "EVIDENCE LIMITED", warnings: ["Не вдалося надійно визначити голосний комплекс."], ukrainian: null, ipa: null, tone: null, toneContour: null };
  const matched = candidate.matched;
  const coda = candidate.coda;
  const warnings = [...candidate.warnings];
  const syllableType = classify(coda, matched.v);
  const tone = toneFor(onsetClass, syllableType, matched.v[3], mark);
  const structuralWarning = warnings.some((w) => w.startsWith("SHORT_VOWEL_REQUIRES_CODA") || w.startsWith("Невикористана частина"));
  const resolvedTone = structuralWarning
    ? { name: null, contour: null, status: "ANALYSIS DEPENDENT", ruleId: "TONE-NOT-ESTABLISHED-FOR-COMBINATION" }
    : tone;
  const codaIpa = coda ? CODAS[coda] : "";
  let onsetIpa = onsetIpaOverride ?? (onsetKey === "ອ" ? "" : onset[1]);
  let vowelIpa = matched.v[2];
  const profileRules = [];
  if (ipaProfile === "mekongphon-reference") {
    const onsetOverride = { "ວ": "w", "ຣ": "r" }[onsetKey];
    const vowelOverride = {
      AW_LONG: "ao", UA_LONG: "ɯːə̯", IA_LONG: "iaː", OEE: "əː",
      AI: "aj", UO_LONG: "uaː", UO_LONG_ALT: "uaː", AI2: "aj", OE: "ə",
    }[matched.v[0]];
    if (onsetOverride && onsetOverride !== onsetIpa) {
      onsetIpa = onsetOverride;
      profileRules.push("IPA-PROFILE-MEKONGPHON-ONSET:" + onsetKey);
    }
    if (vowelOverride && vowelOverride !== vowelIpa) {
      vowelIpa = vowelOverride;
      profileRules.push("IPA-PROFILE-MEKONGPHON-VOWEL:" + matched.v[0]);
    }
  } else if (ipaProfile === "hybrid-deterministic") {
    const context = {
      onset: onsetKey, onsetClass, vowelId: matched.v[0],
      vowelLength: matched.v[3], coda, toneMark: mark,
    };
    const onsetRule = selectHybridRule("onset", context);
    const vowelRule = selectHybridRule("vowel", context);
    if (onsetRule && onsetRule.value !== onsetIpa) {
      onsetIpa = onsetRule.value;
      profileRules.push(onsetRule.provenance, "HYBRID-RULE:" + onsetRule.ruleId);
    }
    if (vowelRule && vowelRule.value !== vowelIpa) {
      vowelIpa = vowelRule.value;
      profileRules.push(vowelRule.provenance, "HYBRID-RULE:" + vowelRule.ruleId);
    }
  }
  const ipa = structuralWarning ? null : onsetIpa + vowelIpa + codaIpa;
  const adapterStatus = ipa && !structuralWarning &&
    onset[2] === "core" && warnings.length === 0
    ? "SUPPORTED" : ipa ? "UNCERTAIN" : "UNSUPPORTED";
  const phoneticResult = createPhoneticResult(ipa, {
    vowelLength: matched.v[3],
    toneCategory: resolvedTone.name,
    toneContourIpa: resolvedTone.contour,
    status: adapterStatus,
    provenance: ["INITIAL:" + onsetClass, "VOWEL:" + matched.v[0],
      "SYLLABLE:" + syllableType, ...profileRules, resolvedTone.ruleId || "TONE:UNRESOLVED"],
    uncertainty: [...warnings, ...(resolvedTone.status === "ESTABLISHED" ? [] : ["TONE-UNRESOLVED"])],
  });
  const ukrainian = adaptPhoneticResult(phoneticResult, { allowUncertain: ipaProfile === "hybrid-deterministic" });

  if (onsetForm !== onsetKey && !onsetIpaOverride) warnings.push(onsetForm + " має нульовий /h/; він змінює лише тоновий клас.");
  if (onsetIpaOverride) warnings.push("ONSET-LABIALIZED:" + onsetForm);
  if (onsetKey === "ຣ") warnings.push(ipaProfile !== "vientiane" ? "Reference-compatible deterministic profile uses /r/ for ຣ; this reading remains analysis-dependent." : "ຣ має сучасне /l/-читання за замовчуванням; /r/ зберігається для іншомовних/історичних випадків.");
  if (structuralWarning) warnings.push("PHON-IPA-WITHHELD-STRUCTURAL-UNCERTAINTY: повний склад не встановлено.");
  if (resolvedTone.status !== "ESTABLISHED") warnings.push("Тон для цієї комбінації не встановлено в канонічному наборі правил.");

  const status = structuralWarning || phoneticResult.status === "UNSUPPORTED" ? "EVIDENCE LIMITED"
    : phoneticResult.status === "UNCERTAIN" || resolvedTone.status !== "ESTABLISHED"
      ? "ANALYSIS DEPENDENT" : "ESTABLISHED";
  return { surface, onset: onsetKey, onsetForm, class: onsetClass, vowel: matched.v[2], vowelId: matched.v[0],
    length: matched.v[3], nucleusType: matched.v[6], coda: coda || "—", toneMark: mark,
    syllableType, tone: resolvedTone.name, toneContour: resolvedTone.contour, toneStatus: resolvedTone.status, ipa, ukrainian, phoneticResult, status,
    rules: ["INITIAL:" + onsetClass, ...(onsetIpaOverride ? ["ONSET-CLUSTER:" + onsetForm] : []),
      "VOWEL:" + matched.v[0], "SYLLABLE:" + syllableType, ...profileRules, resolvedTone.ruleId ? "TONE-RULE:" + resolvedTone.ruleId : "TONE:UNRESOLVED"],
    warnings };
}

function isStructurallyComplete(s) {
  // Syllable segmentation is a source-phonology concern. Do not make it
  // depend on whether the separate Ukrainian target adapter has a mapping.
  return Boolean(s.ipa) && ["SUPPORTED", "UNCERTAIN"].includes(s.phoneticResult?.status) &&
    !(s.warnings || []).some((w) => w.startsWith("Невикористана частина") || w.startsWith("Не вдалося надійно") || w.startsWith("Не знайдено") || w.startsWith("SHORT_VOWEL_REQUIRES_CODA") || w.startsWith("MALFORMED_TONE_MARK_"));
}

function analyzeWord(word, ipaProfile = "hybrid-deterministic") {
  const chars = [...word];
  // Tone-mark placement and multiplicity are syllable-local properties.
  // Candidate syllables validate their own marks below; a mark that cannot be
  // consumed by any complete candidate keeps the whole token unresolved.
  // Do not let dynamic segmentation rescue a malformed prefix by dropping
  // characters before the first Lao onset (e.g. xເເກ -> x + ເເ + ເກ).
  // A token may have at most one recognized preposed vowel before its first
  // consonant; all other material must remain visible as one unresolved unit.
  const firstOnsetIndex = chars.findIndex((ch) => Object.hasOwn(CONSONANTS, ch));
  if (firstOnsetIndex >= 0) {
    const prefix = chars.slice(0, firstOnsetIndex).join("");
    const allowedPreposed = new Set(["", "ເ", "ແ", "ໂ", "ໃ", "ໄ"]);
    if (!allowedPreposed.has(prefix) && ![...prefix].every(isPassthroughChar)) {
      const prefixWarnings = [
        ...(chars.slice(0, firstOnsetIndex).some((ch) => TONE_MARK_SET.has(ch))
          ? ["MALFORMED_TONE_MARK_POSITION: tone mark precedes the syllable onset."]
          : []),
        "Непідтримуваний фрагмент перед початковим приголосним: " + prefix,
      ];
      return [{
        surface: word,
        status: "EVIDENCE LIMITED",
        warnings: prefixWarnings,
        ukrainian: null,
        ipa: null,
        tone: null,
        toneContour: null,
      }];
    }
  }
  // The unlisted preposed sequence ເ + onset + ຽ must remain one
  // unresolved token. Without this guard, dynamic segmentation can salvage
  // ເ+onset as long /eː/ and leave ຽ behind, leaking a misleading IPA prefix.
  const cleanWord = chars.filter((ch) => !TONE_MARK_SET.has(ch)).join("");
  const iaOnset = findOnset(cleanWord);
  if (iaOnset && iaOnset.onsetIndex !== null && iaOnset.onsetLength !== null &&
      cleanWord.slice(0, iaOnset.onsetIndex) === "ເ" &&
      cleanWord.slice(iaOnset.onsetIndex + iaOnset.onsetLength) === "ຽ") {
    return [{
      surface: word,
      status: "EVIDENCE LIMITED",
      warnings: ["ເ◌ຽ is not an established preposed IA spelling; phonetic output withheld."],
      ukrainian: null,
      ipa: null,
      tone: null,
      toneContour: null,
    }];
  }

  // A short-vowel spelling that requires a coda is a single incomplete
  // orthographic unit. Do not let the fallback segmenter split off the vowel
  // sign and make the malformed token look like multiple independent syllables.
  const wholeCandidate = analyzeToken(word, ipaProfile);
  // Keep a fully parsed but analysis-dependent source reading intact. The
  // target adapter may withhold Ukrainian output without invalidating the
  // source-side IPA parse (e.g. modern/loan-dependent ຣ).
  const hasUnconsumedSuffix = (wholeCandidate.warnings || []).some((warning) =>
    warning.startsWith("Невикористана частина структури складу: ")
  );
  if (wholeCandidate.ipa && wholeCandidate.phoneticResult?.status === "UNCERTAIN" && !hasUnconsumedSuffix) {
    return [wholeCandidate];
  }
  if (wholeCandidate.onsetForm && wholeCandidate.onsetForm !== wholeCandidate.onset) {
    return [wholeCandidate];
  }
  // A trailing unsupported Lao consonant is not a separate recoverable syllable.
  const unconsumedWarning = (wholeCandidate.warnings || []).find((warning) =>
    warning.startsWith("Невикористана частина структури складу: "));
  const unconsumedTail = unconsumedWarning?.slice("Невикористана частина структури складу: ".length);
  if (unconsumedTail && [...unconsumedTail].length === 1 &&
      Object.hasOwn(CONSONANTS, unconsumedTail)) {
    return [wholeCandidate];
  }
  if ((wholeCandidate.warnings || []).some((w) => w.startsWith("AMBIGUOUS_LABIALIZED_ONSET_VOWEL_BOUNDARY") ||
      w.startsWith("LABIALIZED_ONSET_BEFORE_ROUNDED_VOWEL") ||
      w.startsWith("ONSET-LABIALIZED:"))) {
    return [wholeCandidate];
  }

  const n = chars.length;
  const best = Array(n + 1);
  best[n] = { score: 0, parts: [] };

  // Lao orthography does not reliably mark word boundaries. Segment a token into
  // the longest fully parsed syllables, but retain every unparsed code point.
  for (let i = n - 1; i >= 0; i--) {
    const ch = chars[i];
    const passthrough = isPassthroughChar(ch);
    const fallback = passthrough
      ? { surface: ch, status: "PASSTHROUGH", ukrainian: ch, ipa: "", warnings: [], passthrough: true }
      : { surface: ch, status: "EVIDENCE LIMITED", warnings: ["Не вдалося надійно проаналізувати фрагмент: " + ch], ukrainian: null, ipa: null };
    best[i] = { score: best[i + 1].score - 100, parts: [fallback, ...best[i + 1].parts] };

    for (let j = i + 1; j <= Math.min(n, i + 12); j++) {
      const candidate = analyzeToken(chars.slice(i, j).join(""), ipaProfile);
      if (!isStructurallyComplete(candidate)) continue;
      const length = j - i;
      const nextChar = chars[j] || "";
      const codaStartsNextSyllable = Boolean(candidate.coda && ["ະ", "ັ", "ິ", "ີ", "ຶ", "ື", "ຸ", "ູ"].includes(nextChar));
      // Prefer a boundary before a consonant followed by its own vowel sign;
      // otherwise greedy longest-match merges ພະນະ into the false syllable ພະນ.
      const score = best[j].score + length - (codaStartsNextSyllable ? 3 : 0);
      const candidateParts = [candidate, ...best[j].parts];
      // If two parses consume the same number of code points, prefer the
      // parse with fewer syllable fragments. Without this tie-break, a valid
      // complex vowel such as ກົວະ can lose to the equally-scored split ກົ|ວະ.
      if (score > best[i].score ||
          (score === best[i].score && candidateParts.length < best[i].parts.length)) {
        best[i] = { score, parts: candidateParts };
      }
    }
  }
  const parts = best[0].parts;
  // Do not let an unattached or malformed tone mark disappear as a fallback
  // fragment. Multiple marks in different syllables are valid; multiple or
  // misplaced marks within one syllable remain visible as one unresolved unit.
  if (parts.some((part) => TONE_MARK_SET.has(part.surface))) {
    return [wholeCandidate];
  }
  // A2 short vowels can be valid inside a closed syllable. Check their coda
  // within each candidate, and withhold only if DP strands a recognized Lao
  // consonant or vowel sign as an independent fallback fragment.
  const vowelGraphemes = new Set([...VOWEL_COMBINING_MARKS, "ະ", "າ", "ຽ", "ຳ", "ເ", "ແ", "ໂ", "ໃ", "ໄ", "ວ", "ອ", "ຍ"]);
  if (parts.some((part) => [...part.surface].length === 1 &&
      (vowelGraphemes.has(part.surface) ||
       ["core", "analysis-dependent"].includes(CONSONANTS[part.surface]?.[2])))) {
    return [wholeCandidate];
  }

  // Mirror the conservative Python selector: an initial, unmarked, short
  // open /a/ before a major-weighted syllable may be a minor C0V0. Keep its
  // segmental IPA and Ukrainian adaptation, but do not claim an independent
  // tone from orthographic shape alone.
  const first = parts[0];
  const following = parts[1];
  const followingMajorWeighted = following && (
    following.length === "long" ||
    following.nucleusType === "diphthong" ||
    (following.coda && following.coda !== "—")
  );
  const followingOnsetSupported = following &&
    CONSONANTS[following.onset]?.[2] === "core" &&
    following.phoneticResult?.status === "SUPPORTED";
  if (POTENTIAL_MINOR_TONE_RULE?.[4] === "analysis-dependent" && first && followingMajorWeighted &&
      first.vowelId === "A" && first.length === "short" &&
      first.coda === "—" && !first.toneMark && first.ipa &&
      first.phoneticResult?.status === "SUPPORTED" &&
      !MINOR_C0_EXCLUDED_ONSETS.has(first.onset) &&
      followingOnsetSupported) {
    first.tone = null;
    first.toneContour = null;
    first.toneStatus = POTENTIAL_MINOR_TONE_RULE[4].toUpperCase().replaceAll("-", " ");
    first.status = "ANALYSIS DEPENDENT";
    first.rules = (first.rules || []).filter((rule) =>
      !rule.startsWith("TONE-RULE:") && !rule.startsWith("TONE:")
    );
    first.rules.push(
      "TONE-RULE:" + POTENTIAL_MINOR_TONE_RULE[0],
      "TONE-POTENTIAL-MINOR-SYLLABLE-UNRESOLVED"
    );
    first.phoneticResult.toneCategory = null;
    first.phoneticResult.toneContourIpa = null;
    first.phoneticResult.provenance = [
      ...new Set([
        ...(first.phoneticResult.provenance || []).filter((rule) =>
          !rule.startsWith("VNT-") && !rule.startsWith("TONE:")
        ),
        POTENTIAL_MINOR_TONE_RULE[0],
        "TONE-POTENTIAL-MINOR-SYLLABLE-UNRESOLVED",
      ])
    ];
    first.phoneticResult.uncertainty = [
      ...new Set([...(first.phoneticResult.uncertainty || []), "TONE-UNRESOLVED"])
    ];
    first.warnings = [
      ...(first.warnings || []),
      "POTENTIAL_MINOR_SYLLABLE_TONE_UNRESOLVED: segmental IPA retained."
    ];
  }
  return parts;
}

export function analyze(text, options = {}) {
  const input = String(text ?? "");
  const ipaProfile = options?.ipaProfile ?? "hybrid-deterministic";
  if (!["vientiane", "mekongphon-reference", "hybrid-deterministic"].includes(ipaProfile)) {
    throw new RangeError("Unknown IPA profile: " + ipaProfile);
  }
  const normalized = input.normalize("NFC").replace(/^\uFEFF/, "").trim();
  if (!normalized) return { input, normalized, status: "EMPTY", output: "", syllables: [], warnings: [] };
  const inputWarnings = validateInput(normalized);
  // Frozen compatibility profiles retain strict historical validation. The
  // default hybrid profile is coverage-first: unsupported visible characters
  // pass through unchanged while Lao spans are analysed independently.
  const hasUnsafeControls = [...normalized].some((ch) => {
    const cp = ch.codePointAt(0);
    return (cp < 0x20 && !["\n", "\t", "\r"].includes(ch)) ||
      (cp >= 0x7F && cp <= 0x9F) || cp === 0xFEFF;
  });
