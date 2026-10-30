import { analyze } from "./engine.js";
import { romanizeLao } from "./romanization.js";
import { analyzeRomanization } from "./romanization-syllable-engine.js";

const input = document.querySelector("#lao-input");
const output = document.querySelector("#output");
const ipa = document.querySelector("#ipa");
const romanization = document.querySelector("#romanization");
const rows = document.querySelector("#rows");
const romanizationTrace = document.querySelector("#romanization-trace");
const romanizationRows = document.querySelector("#romanization-rows");
const romanizationWarnings = document.querySelector("#romanization-warnings");
const romanizationStatus = document.querySelector("#romanization-analysis-status");
const warnings = document.querySelector("#warnings");
const section = document.querySelector("#analysis-section");
const emptyState = document.querySelector("#empty-state");
const results = document.querySelector("#results");
const copy = document.querySelector("#copy");
const copyRomanization = document.querySelector("#copy-romanization");
const copyIpa = document.querySelector("#copy-ipa");
const modePhonetic = document.querySelector("#mode-phonetic");
const modeRomanization = document.querySelector("#mode-romanization");
const outputMethodNote = document.querySelector("#output-method-note");
let outputMode = "phonetic";
const copyFeedback = document.querySelector("#copy-feedback");
const count = document.querySelector("#count");
const status = document.querySelector("#analysis-status");

async function copyWithFeedback(button, value) {
  const defaultLabel = button.dataset.defaultLabel || button.textContent;
  button.dataset.defaultLabel = defaultLabel;

  try {
    await navigator.clipboard.writeText(value);
    button.textContent = "Скопійовано";
    button.classList.add("is-copied");
    copyFeedback.textContent = defaultLabel + ": скопійовано";
  } catch {
    button.textContent = "Не вдалося";
    button.classList.remove("is-copied");
    copyFeedback.textContent = defaultLabel + ": не вдалося скопіювати";
  }

  window.clearTimeout(button.feedbackTimer);
  button.feedbackTimer = window.setTimeout(() => {
    button.textContent = defaultLabel;
    button.classList.remove("is-copied");
  }, 1400);
}

function sourceOnsetGroupsForCrosswalk(sourceText) {
  const parts = String(sourceText ?? "")
    .split(/(\s+|[,.!?;:()[\]{}"“”]+|-+)/u)
    .filter(Boolean);
  return parts
    .filter((part) => !/^(\s+|[,.!?;:()[\]{}"“”]+|-+)$/u.test(part) && !/^[0-9]+$/u.test(part))
    .map((part) => analyze(part).syllables
      .filter((syllable) => !syllable.passthrough)
      .map((syllable) => syllable.onset || null));
}

function currentUkrainianOutput() {
  const result = analyze(input.value);
  if (outputMode === "phonetic") return result.output;
  if (result.status === "INVALID") return "";
  const roman = romanizeLao(input.value);
  return analyzeRomanization(roman.output, {
    sourceOnsetGroups: sourceOnsetGroupsForCrosswalk(input.value),
  }).output;
}

function setOutputMode(mode) {
  if (mode !== "phonetic" && mode !== "romanization") return;
  outputMode = mode;
  modePhonetic.setAttribute("aria-pressed", String(mode === "phonetic"));
  modeRomanization.setAttribute("aria-pressed", String(mode === "romanization"));
  modePhonetic.classList.toggle("is-active", mode === "phonetic");
  modeRomanization.classList.toggle("is-active", mode === "romanization");
  render();
}

function render() {
  const result = analyze(input.value);
  const roman = result.status === "INVALID" ? { output: "", status: "PARTIAL" } : romanizeLao(input.value);
  const romanized = result.status === "INVALID"
    ? { output: "", status: "PARTIAL", warnings: [], syllables: [] }
    : analyzeRomanization(roman.output, {
      sourceOnsetGroups: sourceOnsetGroupsForCrosswalk(input.value),
    });
  count.textContent = [...input.value].length + " символів";

  if (!input.value.trim()) {
    output.textContent = "Введіть лаоський текст, щоб отримати аналіз.";
    output.className = "output muted";
    ipa.textContent = "";
    romanization.textContent = "Введіть лаоський текст, щоб отримати романізацію.";
    romanization.className = "output muted";
    emptyState.hidden = false;
    results.hidden = true;
    section.classList.add("hidden");
    romanizationTrace.hidden = true;
    romanizationRows.replaceChildren();
    romanizationWarnings.replaceChildren();
    romanizationStatus.textContent = "";
    copy.disabled = true;
    outputMethodNote.textContent = outputMode === "phonetic"
      ? "Фонетичний режим: IPA → українська практична адаптація."
      : "Режим за романізацією: складовий аналіз із перевіркою початкової лаоської графеми; придихове h не читається як /h/.";
    copyRomanization.disabled = true;
    copyIpa.disabled = true;
    copyFeedback.textContent = "";
    return;
  }

  const fallbackBlocked = outputMode === "romanization" && result.status === "INVALID";
  const activeOutput = outputMode === "phonetic" ? result.output : (fallbackBlocked ? "" : romanized.output);
  output.textContent = activeOutput || (outputMode === "phonetic"
    ? (result.status === "INVALID"
      ? "Вхідний текст не пройшов перевірку. Виправте його перед повторним аналізом."
      : "Фонетичний результат не встановлено. Спробуйте режим за романізацією.")
    : (fallbackBlocked
      ? "Романізаційний результат не сформовано для некоректного вхідного тексту."
      : "Немає доступного романізованого запису для адаптації."));
  output.className = activeOutput ? "result-body output" : "result-body output muted";
  outputMethodNote.textContent = outputMode === "phonetic"
    ? (result.output
      ? "Фонетичний режим: результат побудовано через IPA → українську практичну адаптацію."
      : (result.status === "INVALID"
        ? "Вхідний текст не пройшов перевірку. Спочатку виправте його; романізаційний режим для такого вводу недоступний."
        : "Фонетичний аналіз не сформував надійного українського результату. Режим за романізацією доступний як менш точна графічна альтернатива."))
    : fallbackBlocked
      ? "Романізаційний режим недоступний: виправте вхідний текст, який не пройшов перевірку."
      : "За романізацією: CLDR Lao-Latin (provisional; BGN/PCGN basis) → звірка лаоської початкової графеми → складовий рушій. kh/th/ph передають придиховість, а окреме h — звук /h/ → г. " +
      (roman.status === "PARTIAL" || romanized.status === "PARTIAL"
        ? "Частину запису не вдалося розібрати однозначно; вона позначена в дужках."
        : "Український результат формується за структурою романізованого складу, а не побуквеною заміною.");
  romanization.textContent = roman.output;
  romanization.className = "output";
  ipa.textContent = result.syllables.map((syllable) => syllable.ipa || "—").join(" ");

  copy.disabled = !activeOutput;
  copyRomanization.disabled = !roman.output;
  copyIpa.disabled = !ipa.textContent;
  emptyState.hidden = true;
  results.hidden = false;
  section.classList.remove("hidden");
  romanizationTrace.hidden = outputMode !== "romanization";

  status.textContent =
    result.status === "OK"
      ? "ГОТОВО"
      : result.status === "PARTIAL"
        ? "ЧАСТКОВИЙ АНАЛІЗ"
        : "НЕ ВСТАНОВЛЕНО";
  status.dataset.state = result.status;

  warnings.replaceChildren();
  result.warnings.forEach((warning) => {
    const paragraph = document.createElement("p");
    paragraph.className = "warning";
    paragraph.textContent = warning;
    warnings.append(paragraph);
  });

  romanizationStatus.textContent = romanized.status === "OK" ? "ГОТОВО" : "ЧАСТКОВИЙ АНАЛІЗ";
  romanizationStatus.dataset.state = romanized.status === "OK" ? "OK" : "PARTIAL";
  romanizationWarnings.replaceChildren();
  romanized.warnings.forEach((warning) => {
    const paragraph = document.createElement("p");
    paragraph.className = "warning";
    paragraph.textContent = warning;
    romanizationWarnings.append(paragraph);
  });
  romanizationRows.replaceChildren();
  romanized.syllables.forEach((syllable) => {
    const element = document.createElement("article");
    element.className = "analysis-row";
    const grid = document.createElement("div");
    grid.className = "analysis-grid";
    [
      ["Романізований склад", syllable.surface],
      ["Початковий елемент", syllable.onset || "∅"],
      ["Голосний комплекс", syllable.nucleus || "—"],
      ["Фіналь", syllable.coda || "∅"],
      ["Український склад", syllable.ukrainian],
      ["Статус", syllable.status],
    ].forEach(([label, value]) => {
      const cell = document.createElement("div");
      const caption = document.createElement("small");
      const strong = document.createElement("strong");
      caption.textContent = label;
      strong.textContent = value;
      cell.append(caption, strong);
      grid.append(cell);
    });
    element.append(grid);
    if (syllable.warning) {
      const note = document.createElement("p");
      note.className = "rules";
      note.textContent = syllable.warning;
      element.append(note);
    }
    romanizationRows.append(element);
  });

  rows.replaceChildren();
  result.syllables.forEach((syllable) => {
    const element = document.createElement("article");
    element.className = "analysis-row";

    const grid = document.createElement("div");
    grid.className = "analysis-grid";
    [
      ["Лао", syllable.surface],
      ["IPA", syllable.ipa || "—"],
      ["Клас", syllable.class || "—"],
      ["Голосний", syllable.vowel || "—"],
      ["Тип складу", syllable.syllableType || "—"],
      ["Тон", syllable.tone ? syllable.tone + " " + syllable.toneContour : "—"],
      ["Український · фонетичний", syllable.ukrainian || "—"],
      ["Статус", syllable.status],
    ].forEach(([label, value]) => {
      const cell = document.createElement("div");
      const caption = document.createElement("small");
      const strong = document.createElement("strong");
      caption.textContent = label;
      strong.textContent = value;
      cell.append(caption, strong);
      grid.append(cell);
    });

    element.append(grid);
    const rules = document.createElement("p");
    rules.className = "rules";
    rules.textContent = (syllable.rules || []).join(" · ");
    element.append(rules);
    rows.append(element);
  });
}

input.addEventListener("input", render);
modePhonetic.addEventListener("click", () => setOutputMode("phonetic"));
modeRomanization.addEventListener("click", () => setOutputMode("romanization"));

document.querySelector("#example").addEventListener("click", () => {
  input.value = "ຂາ";
  render();
  input.focus();
});

document.querySelector("#example-complex").addEventListener("click", () => {
  input.value = "ເຂົ້າໜຽວ";
  render();
  input.focus();
});

document.querySelector("#clear").addEventListener("click", () => {
  input.value = "";
  render();
  input.focus();
});

copy.addEventListener("click", () => {
  const value = currentUkrainianOutput();
  if (value) copyWithFeedback(copy, value);
});

copyRomanization.addEventListener("click", () => {
  const value = romanizeLao(input.value).output;
  if (value) copyWithFeedback(copyRomanization, value);
});

copyIpa.addEventListener("click", () => {
  const value = ipa.textContent;
  if (value) copyWithFeedback(copyIpa, value);
});

render();
