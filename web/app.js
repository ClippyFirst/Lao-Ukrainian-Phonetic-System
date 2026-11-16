import { analyze } from "./engine.js?v=20261110-provisional-ipa-fallback-1";
import { romanizeAlaLcNumerals, romanizeLao } from "./romanization.js";
import { analyzeRomanization } from "./romanization-syllable-engine.js?v=20261115-direct-romanization-input-1";

const input = document.querySelector("#lao-input");
const output = document.querySelector("#output");
const ipa = document.querySelector("#ipa");
const romanization = document.querySelector("#romanization");
const alaLcNumeralPanel = document.querySelector("#ala-lc-numeral-panel");
const alaLcNumerals = document.querySelector("#ala-lc-numerals");
const copyAlaLcNumerals = document.querySelector("#copy-ala-lc-numerals");
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
const inputKindLao = document.querySelector("#input-kind-lao");
const inputKindRomanization = document.querySelector("#input-kind-romanization");
const romanizationProfile = document.querySelector("#romanization-profile");
const romanizationProfileLabel = document.querySelector("#romanization-profile-label");
const inputHeading = document.querySelector("#input-heading");
const inputHelp = document.querySelector("#input-help");
const romanizationPanel = document.querySelector('[data-result-panel="romanization"]');
const ipaPanel = document.querySelector('[data-result-panel="ipa"]');
const romanizationHeading = document.querySelector("#romanization-heading");
const romanizationNote = document.querySelector("#romanization-note");
const outputMethodSwitch = document.querySelector(".output-method-switch");
const quickExamples = document.querySelector(".chip-row");
const resultStatus = document.querySelector("#status");
const outputMethodNote = document.querySelector("#output-method-note");
let inputKind = "lao";
let outputMode = "phonetic";
const copyFeedback = document.querySelector("#copy-feedback");
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

function sourceSyllableGroupsForCrosswalk(sourceText) {
  const parts = String(sourceText ?? "")
    .split(/(\s+|[,.!?;:()[\]{}"“”]+|-+)/u)
    .filter(Boolean);
  return parts
    .filter((part) => !/^(\s+|[,.!?;:()[\]{}"“”]+|-+)$/u.test(part) && !/^[0-9\u0ED0-\u0ED9]+$/u.test(part))
    .map((part) => analyze(part, { ipaProfile: "hybrid-deterministic" }).syllables
      .filter((syllable) => !syllable.passthrough)
      .map((syllable) => ({
        onset: syllable.onset || null,
        onsetForm: syllable.onsetForm || syllable.onset || null,
        vowelId: syllable.rules?.find((rule) => rule.startsWith("VOWEL:"))?.slice(6) ?? null,
        coda: syllable.coda === "—" ? "" : syllable.coda ?? null,
      })));
}

function currentUkrainianOutput() {
  if (inputKind === "romanization") {
    return analyzeRomanization(input.value, { profile: romanizationProfile.value, strictBoundaries: true }).output;
  }
  const result = analyze(input.value, { ipaProfile: "hybrid-deterministic" });
  if (outputMode === "phonetic") return result.output;
  if (result.status === "INVALID") return "";
  const roman = romanizeLao(input.value);
  return analyzeRomanization(roman.output, {
    sourceSyllableGroups: sourceSyllableGroupsForCrosswalk(input.value),
  }).output;
}

function setInputKind(kind) {
  if (kind !== "lao" && kind !== "romanization") return;
  inputKind = kind;
  inputKindLao.setAttribute("aria-pressed", String(kind === "lao"));
  inputKindRomanization.setAttribute("aria-pressed", String(kind === "romanization"));
  inputKindLao.classList.toggle("is-active", kind === "lao");
  inputKindRomanization.classList.toggle("is-active", kind === "romanization");
  inputHeading.textContent = kind === "lao" ? "Введіть лаоською" : "Введіть романізацію";
  input.setAttribute("lang", kind === "lao" ? "lo" : "lo-Latn");
  input.setAttribute("aria-label", kind === "lao" ? "Введення лаоського тексту" : "Введення лаоської романізації латинкою");
  input.name = kind === "lao" ? "lao-text" : "lao-romanization";
  input.placeholder = kind === "lao"
    ? "ພາສາລາວ…"
    : "Viangchan, khā, nyā…";
  inputHelp.textContent = kind === "lao"
    ? "Результат оновлюється автоматично. У поскладовому аналізі видно вихідне написання, IPA-запис, український відповідник і рівень упевненості."
    : "Вставте латинський запис лаоського слова або фрази. Профіль можна визначити автоматично або вибрати явно; неоднозначні склади буде позначено, а не вгадано.";
  romanizationProfileLabel.hidden = kind !== "romanization";
  alaLcNumeralPanel.hidden = kind !== "lao";
  outputMethodSwitch.hidden = kind !== "lao";
  quickExamples.hidden = kind !== "lao";
  modePhonetic.hidden = kind !== "lao";
  modeRomanization.hidden = kind !== "lao";
  romanizationHeading.textContent = kind === "lao" ? "Латинський запис · CLDR Lao-Latin" : "Вхідна романізація";
  romanizationNote.textContent = kind === "lao"
    ? "Режим романізації окремо розбирає склади за профілем CLDR Lao-Latin / BGN-PCGN. Він показує допоміжний запис латинкою й не бере участі у фонетичному шляху до українського результату."
    : "Вхідний латинський запис аналізується окремо від IPA. Романізація може не передавати тон, довготу голосних і частину відмінностей приголосних; ці ознаки не відновлюються навмання.";
  render();
}

function renderRomanizationInput() {
  const adapted = analyzeRomanization(input.value, { profile: romanizationProfile.value, strictBoundaries: true });
  if (!input.value.trim()) {
    output.textContent = "Введіть романізований текст, щоб побачити український запис.";
    output.className = "output muted";
    romanization.textContent = "Тут відобразиться введена романізація.";
    romanization.className = "output muted";
    alaLcNumeralPanel.hidden = true;
    copyAlaLcNumerals.disabled = true;
    ipa.textContent = "";
    emptyState.hidden = false;
    results.hidden = true;
    section.classList.add("hidden");
    copy.disabled = true;
    copyRomanization.disabled = true;
    copyIpa.disabled = true;
    copyFeedback.textContent = "";
    return;
  }

  output.textContent = adapted.output;
  output.className = adapted.output ? "result-body output" : "result-body output muted";
  const profileLabel = adapted.profile === "ala-lc" ? "ALA-LC 2012" : "BGN/PCGN 1966 / CLDR Lao-Latin";
  outputMethodNote.textContent = "Профіль: " + profileLabel + ". Вхідна романізація → розбір підтримуваної складової структури → український практичний запис. Це не IPA-транскрипція; втрачені в латинському записі тон і довгота не реконструюються.";
  romanization.textContent = input.value;
  romanization.className = "output";
  alaLcNumeralPanel.hidden = true;
  copyAlaLcNumerals.disabled = true;
  ipa.textContent = "";
  romanizationPanel.hidden = false;
  ipaPanel.hidden = true;
  emptyState.hidden = true;
  results.hidden = false;
  section.classList.remove("hidden");
  const phoneticTrace = section.querySelector(".trace-panel:not(#romanization-trace)");
  phoneticTrace.hidden = true;
  romanizationTrace.hidden = false;
  copy.disabled = !adapted.output;
  copyRomanization.disabled = false;
  copyIpa.disabled = true;
  resultStatus.textContent = adapted.status === "OK" ? "Готово" : "Частковий аналіз";
  resultStatus.dataset.state = adapted.status;
  status.textContent = adapted.status === "OK" ? "Готово" : "Частковий аналіз";
  status.dataset.state = adapted.status;
  romanizationStatus.textContent = adapted.status === "OK" ? "Готово" : "Частковий аналіз";
  romanizationStatus.dataset.state = adapted.status;
  romanizationWarnings.replaceChildren();
  adapted.warnings.forEach((warning) => {
    const paragraph = document.createElement("p");
    paragraph.className = "warning";
    paragraph.textContent = warning;
    romanizationWarnings.append(paragraph);
  });
  warnings.replaceChildren();
  romanizationRows.replaceChildren();
  adapted.syllables.forEach((syllable) => {
    const element = document.createElement("article");
    element.className = "analysis-row";
    const grid = document.createElement("div");
    grid.className = "analysis-grid";
    [
      ["Вхідний фрагмент", syllable.originalSurface || syllable.surface],
      ["Нормалізований фрагмент", syllable.surface],
      ["Початок", syllable.onset || "∅"],
      ["Голосний комплекс", syllable.nucleus || "—"],
      ["Кінцівка", syllable.coda || "∅"],
      ["Український запис", syllable.ukrainian],
      ["Стан", syllable.status],
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
}

function setOutputMode(mode) {
  if (inputKind !== "lao" || (mode !== "phonetic" && mode !== "romanization")) return;
  outputMode = mode;
  modePhonetic.setAttribute("aria-pressed", String(mode === "phonetic"));
  modeRomanization.setAttribute("aria-pressed", String(mode === "romanization"));
  modePhonetic.classList.toggle("is-active", mode === "phonetic");
  modeRomanization.classList.toggle("is-active", mode === "romanization");
  render();
}

function render() {
  if (inputKind === "romanization") {
    renderRomanizationInput();
    return;
  }
  romanizationPanel.hidden = false;
  ipaPanel.hidden = false;
  const phoneticTrace = section.querySelector(".trace-panel:not(#romanization-trace)");
  phoneticTrace.hidden = false;
  const result = analyze(input.value, { ipaProfile: "hybrid-deterministic" });
  const roman = result.status === "INVALID" ? { output: "", status: "PARTIAL" } : romanizeLao(input.value);
  const romanized = result.status === "INVALID"
    ? { output: "", status: "PARTIAL", warnings: [], syllables: [] }
    : analyzeRomanization(roman.output, {
      sourceSyllableGroups: sourceSyllableGroupsForCrosswalk(input.value),
    });

  if (!input.value.trim()) {
    output.textContent = "Введіть лаоський текст, щоб розпочати аналіз.";
    output.className = "output muted";
    ipa.textContent = "";
    romanization.textContent = "Тут з'явиться латинський запис лаоського тексту.";
    romanization.className = "output muted";
    alaLcNumeralPanel.hidden = true;
    alaLcNumerals.textContent = "";
    copyAlaLcNumerals.disabled = true;
    emptyState.hidden = false;
    results.hidden = true;
    section.classList.add("hidden");
    romanizationTrace.hidden = true;
    romanizationRows.replaceChildren();
    romanizationWarnings.replaceChildren();
    romanizationStatus.textContent = "";
    copy.disabled = true;
    outputMethodNote.textContent = outputMode === "phonetic"
      ? "Фонетичний метод: аналіз письма → IPA → українське читання."
      : "Метод за романізацією: розбір складу та звірка з лаоським написанням. Це окремий спосіб, не проміжний етап фонетичного аналізу.";
    copyRomanization.disabled = true;
    copyIpa.disabled = true;
    copyFeedback.textContent = "";
    return;
  }

  const fallbackBlocked = outputMode === "romanization" && result.status === "INVALID";
  const activeOutput = outputMode === "phonetic" ? result.output : (fallbackBlocked ? "" : romanized.output);
  output.textContent = activeOutput || (outputMode === "phonetic"
    ? (result.status === "INVALID"
      ? "У введеному тексті є непідтримувана структура. Перевірте написання й спробуйте ще раз."
      : "Не вдалося встановити фонетичний результат. Дивіться позначки невизначеності в аналізі.")
    : (fallbackBlocked
      ? "Для цього введення не вдалося побудувати романізаційний результат."
      : "Немає романізованої форми, яку можна зіставити з українською."));
  output.className = activeOutput ? "result-body output" : "result-body output muted";
  outputMethodNote.textContent = outputMode === "phonetic"
    ? (result.output
      ? (result.syllables.some((syllable) => syllable.graphemePreview?.ipaPreview)
        ? "Фонетичний метод: відомі фрагменти пройшли через IPA → український адаптер; у полі IPA також показано попередню підказку з низькою впевненістю."
        : "Фонетичний метод: результат побудовано через IPA → українську практичну адаптацію.")
      : (result.status === "INVALID"
        ? "Введення містить непідтримувану структуру. Виправте його; метод за романізацією для такого введення недоступний."
        : "Фонетичний аналіз не підтвердив повний результат. Романізацію можна переглянути окремо, але вона не замінює фонетичний метод."))
    : fallbackBlocked
      ? "Метод за романізацією недоступний: спершу виправте лаоське введення."
      : "Метод за романізацією: CLDR Lao-Latin (попередній профіль) → зіставлення початку, голосного комплексу й фіналі з лаоською структурою → український склад. kh/th/ph позначають придих; окреме h відповідає /h/; ໜ/ໝ передають /n/ та /m/ без додаткового звука h. " +
      (roman.status === "PARTIAL" || romanized.status === "PARTIAL"
        ? "Частину латинського запису не вдалося однозначно зіставити; її залишено в дужках."
        : "Український результат складається за будовою романізованого складу, а не через заміну латинських літер по одній.");
  romanization.textContent = roman.output;
  romanization.className = "output";
  const alaLcNumeralResult = romanizeAlaLcNumerals(input.value);
  alaLcNumeralPanel.hidden = false;
  alaLcNumerals.textContent = alaLcNumeralResult.output;
  copyAlaLcNumerals.disabled = alaLcNumeralResult.mappedCount === 0;
  // IPA contains only phonetic units: omit explicit passthrough (digits,
  // punctuation, foreign-script text) and show a visible unknown marker for
  // unresolved Lao units instead of a misleading dash run.
  ipa.textContent = result.syllables
    .filter((syllable) => !syllable.passthrough)
    .map((syllable) => {
      if (syllable.ipa) return syllable.ipa;
      const preview = syllable.graphemePreview;
      if (!preview?.ipaPreview) return "?";
      const unresolvedCount = preview.unresolvedGraphemes?.length || 0;
      const marker = unresolvedCount ? "?".repeat(Math.min(3, unresolvedCount)) : "";
      return preview.ipaPreview + marker;
    })
    .join(" ");

  copy.disabled = !activeOutput;
  copyRomanization.disabled = !roman.output;
  copyIpa.disabled = !ipa.textContent;
  emptyState.hidden = true;
  results.hidden = false;
  section.classList.remove("hidden");
  romanizationTrace.hidden = outputMode !== "romanization";

  status.textContent =
    result.status === "OK"
      ? "Готово"
      : result.status === "PARTIAL"
        ? "Частковий аналіз"
        : "Не визначено";
  status.dataset.state = result.status;

  warnings.replaceChildren();
  result.warnings.forEach((warning) => {
    const paragraph = document.createElement("p");
    paragraph.className = "warning";
    paragraph.textContent = warning;
    warnings.append(paragraph);
  });

  romanizationStatus.textContent = romanized.status === "OK" ? "Готово" : "Частковий аналіз";
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
      ["Початкова графема", syllable.sourceOnset || "—"],
      ["Голосний шаблон", syllable.sourceVowelId || "—"],
      ["Кінцева графема", syllable.sourceCoda || "—"],
      ["Склад у романізації", syllable.surface],
      ["Зіставлення з оригіналом", syllable.crosswalk ? "Підтверджено" : "Не підтверджено"],
      ["Початок", syllable.onset || "∅"],
      ["Голосний комплекс", syllable.nucleus || "—"],
      ["Кінцівка", syllable.coda || "∅"],
      ["Український запис складу", syllable.ukrainian],
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
      ["Лаоський склад", syllable.surface],
      ["IPA", syllable.ipa || "—"],
      ["Клас приголосного", syllable.class || "—"],
      ["Голосний", syllable.vowel || "—"],
      ["Тип складу", syllable.syllableType || "—"],
      ["Тон", syllable.tone ? syllable.tone + " " + syllable.toneContour : "—"],
      ["Український запис", syllable.ukrainian || "—"],
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
    if (syllable.graphemePreview) {
      const preview = document.createElement("p");
      preview.className = "grapheme-preview";
      preview.setAttribute("role", "note");
      const label = document.createElement("strong");
      label.textContent = "Попередня IPA-підказка (попередній результат із низькою впевненістю; вимову не підтверджено): ";
      const value = document.createElement("code");
      value.textContent = syllable.graphemePreview.ipaPreview || "—";
      const unresolved = document.createElement("span");
      unresolved.textContent = " · Графеми без підтвердженого розбору: " + (syllable.graphemePreview.unresolvedGraphemes.join("") || "немає");
      preview.append(label, value, unresolved);
      element.append(preview);

      const confidence = document.createElement("p");
      confidence.className = "grapheme-confidence";
      confidence.setAttribute("role", "note");
      confidence.textContent =
        "Низька впевненість: український запис побудовано за доступними графемними підказками; " +
        "знаки «?» позначають невизначені позиції. Тон не визначався.";
      element.append(confidence);
    }
    rows.append(element);
  });
}

input.addEventListener("input", render);
inputKindLao.addEventListener("click", () => setInputKind("lao"));
inputKindRomanization.addEventListener("click", () => setInputKind("romanization"));
romanizationProfile.addEventListener("change", render);
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

copyAlaLcNumerals.addEventListener("click", () => {
  const value = romanizeAlaLcNumerals(input.value);
  if (value.mappedCount > 0) copyWithFeedback(copyAlaLcNumerals, value.output);
});

copyRomanization.addEventListener("click", () => {
  const value = inputKind === "romanization" ? input.value : romanizeLao(input.value).output;
  if (value) copyWithFeedback(copyRomanization, value);
});

copyIpa.addEventListener("click", () => {
  const value = ipa.textContent;
  if (value) copyWithFeedback(copyIpa, value);
});

render();
