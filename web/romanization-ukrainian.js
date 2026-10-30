// Orthographic adaptation of the provisional CLDR Lao-Latin/UNGEGN string.
// This is deliberately independent from the IPA → Ukrainian phonetic adapter.
// It transliterates the Latin spelling; it does not reconstruct Lao pronunciation.
const SEQUENCES = new Map([
  ["kh", "кх"],
  ["th", "тх"],
  ["ph", "пх"],
  ["ch", "ч"],
  ["ng", "нг"]
]);

const LETTERS = new Map(Object.entries({
  a:"а", b:"б", c:"к", d:"д", e:"е", f:"ф", g:"ґ", h:"г",
  i:"і", j:"дж", k:"к", l:"л", m:"м", n:"н", o:"о", p:"п",
  q:"к", r:"р", s:"с", t:"т", u:"у", v:"в", w:"в", x:"кс",
  y:"й", z:"з", "é":"е", "è":"е", "ô":"о"
}));

const SUPPORTED_PASSTHROUGH = /[\s\p{P}\p{N}]/u;

function applyCase(value, source) {
  return source === source.toUpperCase() ? value.toUpperCase() : value;
}

export function romanizationToUkrainian(input) {
  const source = String(input ?? "").normalize("NFC");
  const chars = [...source];
  let output = "";
  let partial = false;

  for (let i = 0; i < chars.length;) {
    const pair = (chars[i] + (chars[i + 1] || "")).toLowerCase();
    if (SEQUENCES.has(pair)) {
      output += applyCase(SEQUENCES.get(pair), chars[i] + chars[i + 1]);
      i += 2;
      continue;
    }

    const char = chars[i];
    const lower = char.toLowerCase();
    if (LETTERS.has(lower)) {
      output += applyCase(LETTERS.get(lower), char);
    } else {
      output += char;
      if (!SUPPORTED_PASSTHROUGH.test(char)) partial = true;
    }
    i += 1;
  }

  return {
    output,
    status: partial ? "PARTIAL" : "OK",
    source: "CLDR Lao-Latin/UNGEGN romanization → Ukrainian orthographic adaptation (project policy)"
  };
}
