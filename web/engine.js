import { CONSONANTS, VOWELS, CODAS, CORRESPONDENCES, TONE_MARKS, TONE_RULES } from "./data.js";

const TONE_MARK_SET = new Set(Object.keys(TONE_MARKS));
const HIGH_DIGRAPHS = new Map([
  ["ຫງ", "ງ"], ["ຫຍ", "ຍ"], ["ຫນ", "ນ"], ["ຫມ", "ມ"],
  ["ຫລ", "ລ"], ["ຫຼ", "ລ"], ["ຫວ", "ວ"],
]);
const sortedIpa = () => Object.keys(CORRESPONDENCES).sort((a, b) => b.length - a.length);

function vowelById(id) { return VOWELS.find((v) => v[0] === id) || null; }

function matchVowel(before, after) {
  const push = (id, consumed = "") => {
    const v = vowelById(id);
    return v ? { v, consumed } : null;
  };
  if (before.endsWith("ເ")) {
    if (after.startsWith("ັຽ")) return push("IA", "ັຽ");
    if (after.startsWith("ັຍ")) return push("IA", "ັຍ");
    if (after.startsWith("ຽ")) return push("IA_LONG", "ຽ");
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
    if (cp < 0x20 && !["\n", "\t", "\r"].includes(ch)) warnings.push("Вхід містить керівний символ.");
    if (cp >= 0x0E80 && cp <= 0x0EFF) continue;
    if (/\s/.test(ch) || (cp < 0x80 && /[-'.]/.test(ch))) continue;
    if (cp > 0x7F) warnings.push("Непідтримуваний символ поза лаоським Unicode-діапазоном.");
  }
  return [...new Set(warnings)];
}

function findOnset(clean) {
  for (const [form, target] of HIGH_DIGRAPHS) {
    if (clean.startsWith(form)) return { onsetKey: target, onsetIndex: 0, onsetLength: [...form].length, onsetClass: "high", onsetForm: form };
  }
  const onsetKey = [...clean].find((ch) => Object.hasOwn(CONSONANTS, ch)) || null;
  return onsetKey ? { onsetKey, onsetIndex: clean.indexOf(onsetKey), onsetLength: 1, onsetClass: CONSONANTS[onsetKey][0], onsetForm: onsetKey } : null;
}

function analyzeToken(surface) {
  const chars = [...surface];
  const mark = chars.find((ch) => TONE_MARK_SET.has(ch)) || null;
  const clean = chars.filter((ch) => !TONE_MARK_SET.has(ch)).join("");
  const found = findOnset(clean);
  if (!found) return { surface, status: "EVIDENCE LIMITED", warnings: ["Не знайдено сучасний початковий приголосний у реєстрі."] };

  const { onsetKey, onsetIndex, onsetLength, onsetClass, onsetForm } = found;
  const onset = CONSONANTS[onsetKey];
  const before = clean.slice(0, onsetIndex);
  const after = clean.slice(onsetIndex + onsetLength);
  const matched = matchVowel(before, after);
  if (!matched) return { surface, onset: onsetKey, status: "EVIDENCE LIMITED", warnings: ["Не вдалося надійно визначити голосний комплекс."] };

  const remainder = after.slice(matched.consumed.length);
  const finalChar = [...remainder].at(-1);
  const coda = finalChar && Object.hasOwn(CODAS, finalChar) ? finalChar : null;

  const unconsumed = coda ? remainder.replace(coda, "") : remainder;
  const warnings = [];
  if (unconsumed) warnings.push("Невикористана частина структури складу: " + unconsumed);

  const syllableType = classify(coda, matched.v);
  const tone = toneFor(onsetClass, syllableType, matched.v[3], mark);
  const codaIpa = coda ? CODAS[coda] : "";
  const onsetIpa = onsetKey === "ອ" ? "" : onset[1];
  const ipa = onsetIpa + matched.v[2] + codaIpa;
  const ukrainian = mapIpa(ipa);

  if (onsetForm !== onsetKey) warnings.push(onsetForm + " має нульовий /h/; він змінює лише тоновий клас.");
  if (onsetKey === "ຣ") warnings.push("ຣ має сучасне /l/-читання за замовчуванням; /r/ зберігається для іншомовних/історичних випадків.");
  if (tone.status !== "ESTABLISHED") warnings.push("Тон для цієї комбінації не встановлено в канонічному наборі правил.");

  const status = ukrainian && tone.status === "ESTABLISHED" && onset[2] === "core" ? "ESTABLISHED" : "ANALYSIS DEPENDENT";
  return { surface, onset: onsetKey, onsetForm, class: onsetClass, vowel: matched.v[2], length: matched.v[3],
    coda: coda || "—", syllableType, tone: tone.name, toneContour: tone.contour, ipa, ukrainian, status,
    rules: ["INITIAL:" + onsetClass, "VOWEL:" + matched.v[0], "SYLLABLE:" + syllableType, tone.ruleId ? "TONE-RULE:" + tone.ruleId : "TONE:UNRESOLVED"],
    warnings };
}

function isStructurallyComplete(s) {
  return Boolean(s.ipa && s.ukrainian) &&
    !(s.warnings || []).some((w) => w.startsWith("Невикористана частина") || w.startsWith("Не вдалося надійно") || w.startsWith("Не знайдено"));
}

function analyzeWord(word) {
  const chars = [...word];
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
      const score = best[j].score + length * length;
      if (score > best[i].score) best[i] = { score, parts: [candidate, ...best[j].parts] };
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
