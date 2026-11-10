import { analyze } from "./engine.js?v=20261110-grapheme-confidence-2";
import { romanizeLao } from "./romanization.js";
import { analyzeRomanization } from "./romanization-syllable-engine.js?v=20261031-source-vowel-crosswalk";

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
const runHybridV2Button = document.querySelector("#run-hybrid-v2");
const hybridV2Status = document.querySelector("#hybrid-v2-status");
const hybridV2Ipa = document.querySelector("#hybrid-v2-ipa");
const hybridV2Alignment = document.querySelector("#hybrid-v2-alignment");
const hybridV2Meta = document.querySelector("#hybrid-v2-meta");
const hybridV2Predictions = document.querySelector("#hybrid-v2-predictions");
const hybridV2Warnings = document.querySelector("#hybrid-v2-warnings");
const copyHybridV2Ipa = document.querySelector("#copy-hybrid-v2-ipa");
let hybridV2Runner = null;
let hybridV2Running = false;
let hybridV2Input = null;

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
  const result = analyze(input.value, { ipaProfile: "hybrid-deterministic" });
  if (outputMode === "phonetic") return result.output;
  if (result.status === "INVALID") return "";
  const roman = romanizeLao(input.value);
  return analyzeRomanization(roman.output, {
    sourceSyllableGroups: sourceSyllableGroupsForCrosswalk(input.value),
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

function resetHybridV2Panel() {
  hybridV2Input = null;
  hybridV2Ipa.textContent = "";
  hybridV2Alignment.textContent = "";
  hybridV2Meta.textContent = "";
  hybridV2Predictions.replaceChildren();
  hybridV2Warnings.replaceChildren();
  hybridV2Status.textContent = "Не запускалося. Перший запуск завантажить приблизно 40 МБ ваг моделі та 15 МБ WASM-рушія з GitHub Pages; інференс виконується локально у браузері.";
  runHybridV2Button.textContent = "Завантажити й запустити Hybrid v2";
  copyHybridV2Ipa.disabled = true;
}

async function runHybridV2() {
  const submittedText = input.value;
  const deterministic = analyze(submittedText, { ipaProfile: "hybrid-deterministic" });
  if (!submittedText.trim() || deterministic.status === "INVALID") return;
  hybridV2Running = true;
  runHybridV2Button.disabled = true;
  hybridV2Status.textContent = "Підготовка локальної нейромережі…";
  try {
    if (!hybridV2Runner) {
      const { createHybridV2Inference } = await import("./hybrid-v2-inference.bundle.js");
      hybridV2Runner = createHybridV2Inference({
        onProgress(progress) {
          if (input.value !== submittedText) return;
          if (progress.phase === "download") {
            const loaded = (progress.loaded / 1048576).toFixed(1);
            const total = progress.total ? (progress.total / 1048576).toFixed(1) : "?";
            hybridV2Status.textContent = `Завантаження ${progress.label}: ${loaded}/${total} МБ…`;
          } else {
            hybridV2Status.textContent = progress.label || "Підготовка моделі…";
          }
        },
      });
    }
    const result = await hybridV2Runner.run(deterministic, submittedText);
    if (input.value !== submittedText) return;
    hybridV2Input = submittedText;
    hybridV2Ipa.textContent = result.neuralRawIpa || "—";
    hybridV2Alignment.textContent =
      "Вирівнювання тонів: " + result.toneAlignmentStatus +
      " · розбір зовнішнього IPA: " + (result.neuralIpaParse?.status || "невідомо") + ".";
    hybridV2Meta.textContent =
      result.modelId + "@" + result.modelRevision +
      " · beam=" + (result.numBeams || 5) +
      " · токенів у вході: " + (result.sourceTokenCount ?? "—") +
      " · усі тонові прогнози залишаються UNCERTAIN.";
    hybridV2Status.textContent = result.toneAlignmentStatus === "ORDER_ALIGNED"
      ? "Hybrid v2 завершив аналіз; тонові послідовності вирівняно за порядком."
      : result.toneAlignmentStatus === "PARTIAL"
        ? "Hybrid v2 завершив аналіз із частковим вирівнюванням."
        : "Сирий нейромережевий IPA збережено; тонове зіставлення не підтверджено.";
    hybridV2Predictions.replaceChildren();
    result.tonePredictions.forEach((prediction) => {
      const paragraph = document.createElement("p");
      paragraph.className = "hybrid-v2-prediction";
      paragraph.textContent =
        "Склад " + (prediction.syllableIndex + 1) + " (" + prediction.sourceSurface + "): " +
        prediction.contour + " → " + prediction.category + " · UNCERTAIN";
      hybridV2Predictions.append(paragraph);
    });
    hybridV2Warnings.replaceChildren();
    result.warnings.forEach((warning) => {
      const paragraph = document.createElement("p");
      paragraph.className = "warning";
      paragraph.textContent = warning;
      hybridV2Warnings.append(paragraph);
    });
    copyHybridV2Ipa.disabled = !result.neuralRawIpa;
    runHybridV2Button.textContent = "Оновити Hybrid v2";
  } catch (error) {
    if (input.value === submittedText) {
      hybridV2Status.textContent = "Нейромережевий канал не запустився: " + (error?.message || String(error));
      hybridV2Alignment.textContent = "Детермінований результат не змінено; мовчазного fallback немає.";
      hybridV2Ipa.textContent = "";
      hybridV2Meta.textContent = "";
      hybridV2Predictions.replaceChildren();
      hybridV2Warnings.replaceChildren();
      copyHybridV2Ipa.disabled = true;
    }
  } finally {
    hybridV2Running = false;
    if (input.value !== submittedText) render();
    else runHybridV2Button.disabled = analyze(input.value, { ipaProfile: "hybrid-deterministic" }).status === "INVALID";
  }
}

function render() {
  const result = analyze(input.value, { ipaProfile: "hybrid-deterministic" });
  const roman = result.status === "INVALID" ? { output: "", status: "PARTIAL" } : romanizeLao(input.value);
  const romanized = result.status === "INVALID"
    ? { output: "", status: "PARTIAL", warnings: [], syllables: [] }
    : analyzeRomanization(roman.output, {
      sourceSyllableGroups: sourceSyllableGroupsForCrosswalk(input.value),
    });
  count.textContent = [...input.value].length + " символів";
  if (hybridV2Input !== input.value && !hybridV2Running) resetHybridV2Panel();
  runHybridV2Button.disabled = !input.value.trim() || result.status === "INVALID" || hybridV2Running;

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
      : "Режим за романізацією: складовий аналіз зі звіркою початкової графеми, голосної структури й підтримуваної фіналі; придихове h відрізняється від окремого /h/.";
    copyRomanization.disabled = true;
    copyIpa.disabled = true;
    runHybridV2Button.disabled = true;
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
      : "За романізацією: CLDR Lao-Latin (provisional; BGN/PCGN basis) → звірка початку, голосного комплексу й підтримуваної фіналі з лаоським складом → складовий рушій. kh/th/ph передають придиховість, окреме h — /h/ → г, а ໜ/ໝ — беззвучний висококласовий маркер перед /n,m/. " +
      (roman.status === "PARTIAL" || romanized.status === "PARTIAL"
        ? "Частину запису не вдалося розібрати однозначно; вона позначена в дужках."
        : "Український результат формується за структурою романізованого складу, а не побуквеною заміною.");
  romanization.textContent = roman.output;
  romanization.className = "output";
  // IPA contains only phonetic units: omit explicit passthrough (digits,
  // punctuation, foreign-script text) and show a visible unknown marker for
  // unresolved Lao units instead of a misleading dash run.
  ipa.textContent = result.syllables
    .filter((syllable) => !syllable.passthrough)
    .map((syllable) => syllable.ipa || "?")
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
      ["Лаоська початкова графема", syllable.sourceOnset || "—"],
      ["Лаоська голосна структура", syllable.sourceVowelId || "—"],
      ["Лаоська фінальна графема", syllable.sourceCoda || "—"],
      ["Романізований склад", syllable.surface],
      ["Звірка джерельної структури", syllable.crosswalk ? "Підтверджено" : "Не підтверджено"],
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
    if (syllable.graphemePreview) {
      const preview = document.createElement("p");
      preview.className = "grapheme-preview";
      preview.setAttribute("role", "note");
      const label = document.createElement("strong");
      label.textContent = "Попередній IPA (PROVISIONAL; низька впевненість; вимова не підтверджена): ";
      const value = document.createElement("code");
      value.textContent = syllable.graphemePreview.ipaPreview || "—";
      const unresolved = document.createElement("span");
      unresolved.textContent = " · Невизначені графеми: " + (syllable.graphemePreview.unresolvedGraphemes.join("") || "немає");
      preview.append(label, value, unresolved);
      element.append(preview);

      const confidence = document.createElement("p");
      confidence.className = "grapheme-confidence";
      confidence.setAttribute("role", "note");
      confidence.textContent =
        "Низька впевненість: український результат сформовано за доступними графемними підказками; " +
        "невирішені позиції позначено «?». Тон не виводився.";
      element.append(confidence);
    }
    rows.append(element);
  });
}

input.addEventListener("input", render);
runHybridV2Button.addEventListener("click", runHybridV2);
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

copyHybridV2Ipa.addEventListener("click", () => {
  const value = hybridV2Ipa.textContent;
  if (value) copyWithFeedback(copyHybridV2Ipa, value);
});

render();
