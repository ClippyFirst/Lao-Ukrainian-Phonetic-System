import { analyze } from "./engine.js";
import { romanizeLao } from "./romanization.js";
import { romanizationToUkrainian } from "./romanization-ukrainian.js";

const input = document.querySelector("#lao-input");
const output = document.querySelector("#output");
const ipa = document.querySelector("#ipa");
const romanization = document.querySelector("#romanization");
const rows = document.querySelector("#rows");
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

function currentUkrainianOutput() {
  const result = analyze(input.value);
  if (outputMode === "phonetic") return result.output;
  if (result.status === "INVALID") return "";
  const roman = romanizeLao(input.value);
  return romanizationToUkrainian(roman.output).output;
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
  const roman = romanizeLao(input.value);
  const romanized = result.status === "INVALID"
    ? { output: "", status: "PARTIAL" }
    : romanizationToUkrainian(roman.output);
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
    copy.disabled = true;
    outputMethodNote.textContent = outputMode === "phonetic"
      ? "Фонетичний режим: IPA → українська практична адаптація."
      : "Режим за романізацією: латинський запис → українська графічна адаптація; вимова не перевіряється.";
    copyRomanization.disabled = true;
    copyIpa.disabled = true;
    copyFeedback.textContent = "";
    return;
  }

  const fallbackBlocked = outputMode === "romanization" && result.status === "INVALID";
  const activeOutput = outputMode === "phonetic" ? result.output : (fallbackBlocked ? "" : romanized.output);
  output.textContent = activeOutput || (outputMode === "phonetic"
    ? "Фонетичний результат не встановлено. Спробуйте режим за романізацією."
    : (fallbackBlocked
      ? "Романізаційний результат не сформовано для некоректного вхідного тексту."
      : "Немає доступного романізованого запису для адаптації."));
  output.className = activeOutput ? "result-body output" : "result-body output muted";
  outputMethodNote.textContent = outputMode === "phonetic"
    ? (result.output
      ? "Фонетичний режим: результат побудовано через IPA → українську практичну адаптацію."
      : "Фонетичний аналіз не сформував надійного українського результату. Режим за романізацією доступний як менш точна графічна альтернатива.")
    : fallbackBlocked
      ? "Романізаційний режим недоступний: виправте вхідний текст, який не пройшов перевірку."
      : "За романізацією: CLDR Lao-Latin/UNGEGN → українська графічна адаптація. " +
      (roman.status === "PARTIAL" || romanized.status === "PARTIAL"
        ? "Покриття часткове; непідтримані символи збережено."
        : "Запис відтворює латинську форму, а не встановлену вимову.");
  romanization.textContent = roman.output;
  romanization.className = "output";
  ipa.textContent = result.syllables.map((syllable) => syllable.ipa || "—").join(" ");

  copy.disabled = !activeOutput;
  copyRomanization.disabled = !roman.output;
  copyIpa.disabled = !ipa.textContent;
  emptyState.hidden = true;
  results.hidden = false;
  section.classList.remove("hidden");

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
      ["Український", syllable.ukrainian || "—"],
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
