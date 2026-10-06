import { CONSONANTS, VOWELS, CODAS, CORRESPONDENCES, TONE_MARKS, TONE_RULES } from "./data.js";

const TONE_MARK_SET = new Set(Object.keys(TONE_MARKS));
const SPECIAL_ONSETS = new Set(["ໜ", "ໝ"]);
const sortedIpa = () => Object.keys(CORRESPONDENCES).sort((a, b) => b.length - a.length);

function vowelById(id) {
  const row = VOWELS.find((v) => v[0] === id);
  return row || null;
}

function matchVowel(before, after) {
  const candidates = [];
  const push = (id, consumed = "") => {
    const v = vowelById(id);
    if (v) candidates.push({ v, consumed });
  };

  if (before.endsWith("ເ")) {
    if (after.startsWith("ັຽ")) push("IA", "ັຽ");
    else if (after.startsWith("ັຍ")) push("IA", "ັຍ");
    else if (after.startsWith("ຽ")) push("IA_LONG", "ຽ");
    else if (after.startsWith("ຍ")) push("IA_LONG", "ຍ");
    else if (after.startsWith("ຶອ")) push("UA", "ຶອ");
    else if (after.startsWith("ືອ")) push("UA_LONG", "ືອ");
    else if (after.startsWith("ົາ")) push("AW_LONG", "ົາ");
    else if (after.startsWith("າະ")) push("AW", "າະ");
    else if (after.startsWith("ິ")) push("OE", "ິ");
    else if (after.startsWith("ີ")) push("OEE", "ີ");
    else if (after.startsWith("ະ")) push("E", "ະ");
    else if (after.startsWith("ັ")) push("E", "ັ");
    else push("EE");
  } else if (before.endsWith("ແ")) {
    if (after.startsWith("ະ")) push("AE", "ະ");
    else if (after.startsWith("ັ")) push("AE", "ັ");
    else push("AEE");
  } else if (before.endsWith("ໂ")) {
    if (after.startsWith("ະ")) push("O", "ະ");
    else if (after.startsWith("ົ")) push("O", "ົ");
    else push("OO");
  } else if (before.endsWith("ໄ")) {
    push("AI");
  } else if (before.endsWith("ໃ")) {
    push("AI2");
  } else if (after.startsWith("ົວະ")) {
    push("UO", "ົວະ");
  } else if (after.startsWith("ົວ")) {
    push("UO_LONG", "ົວ");
  } else if (after.startsWith("ຳ")) {
    push("AM", "ຳ");
  } else if (after.startsWith("ໍ")) {
    push("AWW", "ໍ");
  } else if (after.startsWith("ະ")) {
    push("A", "ະ");
  } else if (after.startsWith("ັ")) {
    push("A2", "ັ");
  } else if (after.startsWith("າ")) {
    push("AA", "າ");
  } else if (after.startsWith("ິ")) {
    push("I", "ິ");
  } else if (after.startsWith("ີ")) {
    push("II", "ີ");
  } else if (after.startsWith("ຶ")) {
    push("Y", "ຶ");
  } else if (after.startsWith("ື")) {
    push("YY", "ື");
  } else if (after.startsWith("ຸ")) {
    push("U", "ຸ");
  } else if (after.startsWith("ູ")) {
    push("UU", "ູ");
  }

  return candidates[0] || null;
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
  const row = TONE_RULES.find((r) =>
    r[0] === cls &&
    (r[1] === "*" || r[1] === syllableType) &&
    (r[2] === "*" || r[2] === length) &&
    r[3] === markName
  );
  return row
    ? { name: row[4], contour: row[5], status: "ESTABLISHED", ruleId: row[6] }
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
    if (/\s/.test(ch) || (ch.codePointAt(0) < 0x80 && /[-'.]/.test(ch))) continue;
    if (cp > 0x7F) warnings.push(`Непідтримуваний символ поза лаоським Unicode-діапазоном: U+${cp.toString(16).toUpperCase().padStart(4, "0")}.`);
  }
  return [...new Set(warnings)];
}

function analyzeToken(surface) {
  const chars = [...surface];
  const mark = chars.find((ch) => TONE_MARK_SET.has(ch)) || null;
  const clean = chars.filter((ch) => !TONE_MARK_SET.has(ch)).join("");
  let onsetKey = null;
  if (clean.startsWith("ໜ") || clean.startsWith("ໝ")) onsetKey = clean.slice(0, 2);
  else onsetKey = chars.find((ch) => Object.hasOwn(CONSONANTS, ch)) || null;

  if (!onsetKey) {
    return { surface, status: "EVIDENCE LIMITED", warnings: ["Не знайдено сучасний початковий приголосний у реєстрі."] };
  }

  const onset = CONSONANTS[onsetKey];
  const onsetIndex = clean.indexOf(onsetKey);
  const before = clean.slice(0, onsetIndex);
  const after = clean.slice(onsetIndex + onsetKey.length);
  const matched = matchVowel(before, after);

  if (!matched) {
    return {
      surface,
      onset: onsetKey,
      class: onset[0],
      status: "EVIDENCE LIMITED",
      warnings: ["Не вдалося надійно визначити голосний комплекс."]
    };
  }

  const remainder = after.slice(matched.consumed.length);
  let coda = null;
  for (const ch of [...remainder].reverse()) {
    if (Object.hasOwn(CODAS, ch)) { coda = ch; break; }
  }

  const unconsumed = coda ? remainder.replace(coda, "") : remainder;
  const warnings = [];
  if (unconsumed) warnings.push(`Невикористана частина структури складу: ${unconsumed}`);
  const syllableType = classify(coda, matched.v);
  const tone = toneFor(onset[0], syllableType, matched.v[3], mark);
  const codaIpa = coda ? CODAS[coda] : "";
  const onsetIpa = onsetKey === "ອ" ? "" : onset[1];
  const ipa = onsetIpa + matched.v[2] + codaIpa;
  const ukrainian = SPECIAL_ONSETS.has(onsetKey)
    ? (onsetKey === "ໜ" ? "н" : "м") + (CORRESPONDENCES[matched.v[2]] || "")
    : mapIpa(ipa);

  if (SPECIAL_ONSETS.has(onsetKey)) {
    warnings.push("ໜ/ໝ збережено як структурні /h+n/ або /h+m/; їхню тонову поведінку не слід вважати повністю встановленою.");
  }
  if (onsetKey === "ຣ") warnings.push("ຣ має analysis-dependent статус і потребує контекстної верифікації.");
  if (tone.status !== "ESTABLISHED") warnings.push("Тон для цієї комбінації не встановлено в канонічному наборі правил.");

  const status = ukrainian && tone.status === "ESTABLISHED" ? "ESTABLISHED" : "ANALYSIS DEPENDENT";
  return {
    surface,
    onset: onsetKey,
    class: onset[0],
    vowel: matched.v[2],
    length: matched.v[3],
    coda: coda || "—",
    syllableType,
    tone: tone.name,
    toneContour: tone.contour,
    ipa,
    ukrainian,
    status,
    rules: [
      `INITIAL:${onset[0]}`,
      `VOWEL:${matched.v[0]}`,
      `SYLLABLE:${syllableType}`,
      tone.ruleId ? `TONE-RULE:${tone.ruleId}` : "TONE:UNRESOLVED"
    ],
    warnings
  };
}

export function analyze(text) {
  const input = String(text ?? "");
  const normalized = input.normalize("NFC").trim();
  if (!normalized) return { input, normalized, status: "EMPTY", output: "", syllables: [], warnings: [] };

  const inputWarnings = validateInput(normalized);
  if (inputWarnings.length) return { input, normalized, status: "INVALID", output: "", syllables: [], warnings: inputWarnings };

  const tokens = normalized.split(/\s+/).filter(Boolean);
  const syllables = tokens.map(analyzeToken);
  const warnings = [...new Set(syllables.flatMap((s) => s.warnings || []))];
  if (tokens.length > 1) warnings.push("Пробіли трактуються як межі аналізу; повна автоматична сегментація неперервного лаоського тексту залишається окремою дослідницькою задачею.");

  return {
    input,
    normalized,
    status: syllables.every((s) => s.ukrainian && s.status === "ESTABLISHED") ? "OK" : "PARTIAL",
    output: syllables.map((s) => s.ukrainian || "").filter(Boolean).join(" "),
    syllables,
    warnings: [...new Set(warnings)]
  };
}
