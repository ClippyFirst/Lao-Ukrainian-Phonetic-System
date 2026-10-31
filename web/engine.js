import { CONSONANTS, ONSET_CLUSTERS, VOWELS, CODAS, CORRESPONDENCES, TONE_MARKS, TONE_RULES } from "./data.js";

const TONE_MARK_SET = new Set(Object.keys(TONE_MARKS));
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

function mapIpa(ipa) {
  const keys = sortedIpa();
  let out = "";
  let i = 0;
  while (i < ipa.length) {
    const key = keys.find((candidate) => ipa.startsWith(candidate, i));
    if (!key) return null;
    out += CORRESPONDENCES[key];
    i += key.length;
  }
  return out;
}

function validateInput(text) {
  const warnings = [];
  for (const ch of text) {
    const cp = ch.codePointAt(0);
    if ((cp < 0x20 && !["\n", "\t", "\r"].includes(ch)) || (cp >= 0x7F && cp <= 0x9F)) {
      warnings.push("Вхід містить керівний символ.");
      continue;
    }
    if (cp >= 0x0E80 && cp <= 0x0EFF) continue;
    if (/\s/.test(ch) || (cp < 0x80 && /[-'.]/.test(ch))) continue;
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

function analyzeToken(surface) {
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
  if (!found) return { surface, status: "EVIDENCE LIMITED", warnings: ["Не знайдено сучасний початковий приголосний у реєстрі."] };

  const { onsetKey, onsetIndex, onsetLength, onsetClass } = found;
  const onset = CONSONANTS[onsetKey];
  const before = clean.slice(0, onsetIndex);
  const allowedPreposed = new Set(["", "ເ", "ແ", "ໂ", "ໃ", "ໄ"]);
  if (!allowedPreposed.has(before)) return { surface, status: "EVIDENCE LIMITED", warnings: ["Непідтримуваний фрагмент перед початковим приголосним: " + before] };

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

  if (!candidate) return { surface, onset: onsetKey, status: "EVIDENCE LIMITED", warnings: ["Не вдалося надійно визначити голосний комплекс."], ukrainian: null, ipa: null };
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
  const onsetIpa = onsetIpaOverride ?? (onsetKey === "ອ" ? "" : onset[1]);
  const ipa = structuralWarning ? null : onsetIpa + matched.v[2] + codaIpa;
  const ukrainian = ipa ? mapIpa(ipa) : null;

  if (onsetForm !== onsetKey && !onsetIpaOverride) warnings.push(onsetForm + " має нульовий /h/; він змінює лише тоновий клас.");
  if (onsetIpaOverride) warnings.push("ONSET-LABIALIZED:" + onsetForm);
  if (onsetKey === "ຣ") warnings.push("ຣ має сучасне /l/-читання за замовчуванням; /r/ зберігається для іншомовних/історичних випадків.");
  if (structuralWarning) warnings.push("PHON-IPA-WITHHELD-STRUCTURAL-UNCERTAINTY: повний склад не встановлено.");
  if (resolvedTone.status !== "ESTABLISHED") warnings.push("Тон для цієї комбінації не встановлено в канонічному наборі правил.");

  const status = structuralWarning || (ipa && !ukrainian) ? "EVIDENCE LIMITED"
    : ukrainian && resolvedTone.status === "ESTABLISHED" && onset[2] === "core" ? "ESTABLISHED" : "ANALYSIS DEPENDENT";
  return { surface, onset: onsetKey, onsetForm, class: onsetClass, vowel: matched.v[2], length: matched.v[3],
    coda: coda || "—", syllableType, tone: resolvedTone.name, toneContour: resolvedTone.contour, ipa, ukrainian, status,
    rules: ["INITIAL:" + onsetClass, ...(onsetIpaOverride ? ["ONSET-CLUSTER:" + onsetForm] : []),
      "VOWEL:" + matched.v[0], "SYLLABLE:" + syllableType, resolvedTone.ruleId ? "TONE-RULE:" + resolvedTone.ruleId : "TONE:UNRESOLVED"],
    warnings };
}

function isStructurallyComplete(s) {
  return Boolean(s.ipa && s.ukrainian) &&
    !(s.warnings || []).some((w) => w.startsWith("Невикористана частина") || w.startsWith("Не вдалося надійно") || w.startsWith("Не знайдено") || w.startsWith("SHORT_VOWEL_REQUIRES_CODA") || w.startsWith("MALFORMED_TONE_MARK_"));
}

function analyzeWord(word) {
  const chars = [...word];
  // A malformed tone-mark position belongs to the whole orthographic unit;
  // do not let dynamic segmentation salvage a plausible-looking substring.
  const cleanForMarkOrder = chars.filter((ch) => !TONE_MARK_SET.has(ch)).join("");
  const markOrderError = toneMarkOrderError(chars, cleanForMarkOrder, findOnset(cleanForMarkOrder));
  if (markOrderError) {
    return [{ surface: word, status: "EVIDENCE LIMITED", warnings: [markOrderError + ": phonetic output withheld."], ukrainian: null, ipa: null, tone: null }];
  }
  // Prevent dynamic segmentation from salvaging a valid-looking syllable
  // when adjacent tone marks make the original orthographic unit malformed.
  if (chars.some((ch, i) => TONE_MARK_SET.has(ch) && TONE_MARK_SET.has(chars[i + 1]))) {
    return [{ surface: word, status: "EVIDENCE LIMITED", warnings: ["MULTIPLE_TONE_MARKS: phonetic output withheld."], ukrainian: null, ipa: null, tone: null }];
  }
  // Do not let dynamic segmentation rescue a malformed prefix by dropping
  // characters before the first Lao onset (e.g. xເເກ -> x + ເເ + ເກ).
  // A token may have at most one recognized preposed vowel before its first
  // consonant; all other material must remain visible as one unresolved unit.
  const firstOnsetIndex = chars.findIndex((ch) => Object.hasOwn(CONSONANTS, ch));
  if (firstOnsetIndex >= 0) {
    const prefix = chars.slice(0, firstOnsetIndex).join("");
    const allowedPreposed = new Set(["", "ເ", "ແ", "ໂ", "ໃ", "ໄ"]);
    if (!allowedPreposed.has(prefix)) {
      return [{
        surface: word,
        status: "EVIDENCE LIMITED",
        warnings: ["Непідтримуваний фрагмент перед початковим приголосним: " + prefix],
        ukrainian: null,
        ipa: null,
      }];
    }
  }
  // The unlisted preposed sequence ເ + onset + ຽ must remain one
  // unresolved token. Without this guard, dynamic segmentation can salvage
  // ເ+onset as long /eː/ and leave ຽ behind, leaking a misleading IPA prefix.
  const cleanWord = chars.filter((ch) => !TONE_MARK_SET.has(ch)).join("");
  const iaOnset = findOnset(cleanWord);
  if (iaOnset &&
      cleanWord.slice(0, iaOnset.onsetIndex) === "ເ" &&
      cleanWord.slice(iaOnset.onsetIndex + iaOnset.onsetLength) === "ຽ") {
    return [{
      surface: word,
      status: "EVIDENCE LIMITED",
      warnings: ["ເ◌ຽ is not an established preposed IA spelling; phonetic output withheld."],
      ukrainian: null,
      ipa: null,
    }];
  }

  // A short-vowel spelling that requires a coda is a single incomplete
  // orthographic unit. Do not let the fallback segmenter split off the vowel
  // sign and make the malformed token look like multiple independent syllables.
  const wholeCandidate = analyzeToken(word);
  if (wholeCandidate.onsetForm && wholeCandidate.onsetForm !== wholeCandidate.onset) {
    return [wholeCandidate];
  }
  if ((wholeCandidate.warnings || []).some((w) => w.startsWith("SHORT_VOWEL_REQUIRES_CODA") ||
      w.startsWith("AMBIGUOUS_LABIALIZED_ONSET_VOWEL_BOUNDARY") ||
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
    const passthrough = /^[,!?;:()[\]{}"“”]+$/u.test(ch) || /^[0-9A-Za-z.'-]$/u.test(ch);
    const fallback = passthrough
      ? { surface: ch, status: "PASSTHROUGH", ukrainian: ch, ipa: "", warnings: [], passthrough: true }
      : { surface: ch, status: "EVIDENCE LIMITED", warnings: ["Не вдалося надійно проаналізувати фрагмент: " + ch], ukrainian: null, ipa: null };
    best[i] = { score: best[i + 1].score - 100, parts: [fallback, ...best[i + 1].parts] };

    for (let j = i + 1; j <= Math.min(n, i + 12); j++) {
      const candidate = analyzeToken(chars.slice(i, j).join(""));
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
  return best[0].parts;
}

export function analyze(text) {
  const input = String(text ?? "");
  const normalized = input.normalize("NFC").trim();
  if (!normalized) return { input, normalized, status: "EMPTY", output: "", syllables: [], warnings: [] };
  const inputWarnings = validateInput(normalized);
  if (inputWarnings.length) return { input, normalized, status: "INVALID", output: "", syllables: [], warnings: inputWarnings };

  const words = normalized.split(/\s+/).filter(Boolean).map(analyzeWord);
  const syllables = words.flat();
  const warnings = [...new Set(syllables.flatMap((s) => s.warnings || []))];
  if (words.length > 1) warnings.push("Пробіли збережено як межі введених фрагментів; у лаоському письмі пробіли не позначають кожну межу слова.");
  const complete = syllables.every((s) => s.passthrough || (s.ukrainian && s.status === "ESTABLISHED"));
  const output = words.map((word) => word.map((s) => s.ukrainian || ("⟦" + s.surface + "⟧")).join("")).join(" ");
  return { input, normalized, status: complete ? "OK" : "PARTIAL", output, syllables, warnings: [...new Set(warnings)] };
}
