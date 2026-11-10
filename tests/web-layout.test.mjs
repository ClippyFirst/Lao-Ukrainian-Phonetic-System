import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const html = await readFile(new URL("../index.html", import.meta.url), "utf8");
const css = await readFile(new URL("../web/styles.css", import.meta.url), "utf8");
const app = await readFile(new URL("../web/app.js", import.meta.url), "utf8");

test("service stacks the full-width input above full-width results", () => {
  assert.match(html, /class="workspace-layout"/);
  assert.ok(html.indexOf('class="workbench"') < html.indexOf('class="output-workspace"'));
  assert.match(css, /\.workspace-layout\{display:flex;flex-direction:column;gap:24px;align-items:stretch;width:100%/);
  assert.match(css, /\.workbench,\.output-workspace\{width:100%;min-width:0/);
  assert.doesNotMatch(css, /grid-template-areas:"input output"/);
});

test("result cards prioritize Ukrainian, then romanization, then IPA", () => {
  const ua = html.indexOf('data-result-panel="ukrainian"');
  const roman = html.indexOf('data-result-panel="romanization"');
  const ipa = html.indexOf('data-result-panel="ipa"');
  assert.ok(ua >= 0 && ua < roman && roman < ipa);
  assert.match(html, /class="result-card result-card-primary"/);
  assert.match(css, /\.result-card-primary\{grid-column:1\/-1/);
});

test("empty state yields to results and detailed syllable analysis is collapsed", () => {
  assert.match(html, /id="empty-state"/);
  assert.match(html, /id="results"[^>]*hidden/);
  assert.match(html, /<details class="trace-panel trace-disclosure">\s*<summary[^>]*>.*?Як побудовано читання/s);
  assert.match(app, /emptyState\.hidden = false/);
  assert.match(app, /emptyState\.hidden = true/);
  assert.match(app, /results\.hidden = false/);
});

test("layout remains usable on narrow screens and retains Lao-specific analysis", () => {
  assert.match(css, /@media\(max-width:620px\)\{[\s\S]*?\.result-grid\{grid-template-columns:1fr\}/);
  for (const id of ["lao-input", "romanization", "ipa", "output", "analysis-status", "rows", "warnings"]) {
    assert.match(html, new RegExp('id="' + id + '"'));
  }
  assert.match(app, /syllable\.tone/);
  assert.match(app, /syllable\.rules/);
});

 
test("Ukrainian result offers an accessible two-method selector in one result card",()=>{
 assert.ok(html.includes('id="mode-phonetic"'));
 assert.ok(html.includes('id="mode-romanization"'));
 assert.ok(html.includes('id="output-method-note"'));
 assert.ok(app.includes("analyzeRomanization"));
 assert.ok(html.includes('id="romanization-trace"'));
 assert.ok(html.includes('id="romanization-rows"'));
 assert.ok(app.includes("romanizationRows"));
 assert.ok(app.includes("setOutputMode"));
 assert.ok(app.includes("aria-pressed"));
 assert.ok(app.includes("currentUkrainianOutput"));
 assert.ok(app.includes("modeRomanization.addEventListener"));
 assert.ok(app.includes('result.status === "INVALID"'));
 assert.ok(css.includes(".method-switch"));
});


test("public research status reflects the merged 2026-10-31 implementation", async () => {
  const methodology = await readFile(new URL("../system.html", import.meta.url), "utf8");
  assert.match(html, /Стан дослідження · 10\.11\.2026/);
  assert.match(html, /\/ʃt͡ʃ\/.{0,80}→ щ/);
  assert.match(html, /Режим романізації окремо розбирає склади за профілем CLDR Lao-Latin \/ BGN-PCGN/);
  assert.match(methodology, /Станом на 10 листопада 2026 року/);
  assert.match(methodology, /еталонна вибірка IPA.{0,100}незалежно перевірених фахівцями прикладів — 0/i);
  assert.match(methodology, /незалежну фонетичну точність поки не виміряно/i);
});

test("methodology tables that scroll horizontally are keyboard-focusable and named", async () => {
  const methodology = await readFile(new URL("../system.html", import.meta.url), "utf8");
  const tables = [...methodology.matchAll(/<table\b([^>]*)>/g)].map((match) => match[1]);
  assert.equal(tables.length, 3);
  const scrollableTables = tables.filter((attributes) => /tabindex="0"/.test(attributes));
  assert.equal(scrollableTables.length, 2);
  assert.ok(scrollableTables.every((attributes) => /aria-label="[^"]+"/.test(attributes)));
});


test("copy and quick-example controls meet the 44px minimum target size", () => {
  for (const selector of [".copy", ".mini-button,.button", ".copy-button"]) {
    const escaped = selector.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const match = css.match(new RegExp("(?:^|\n)" + escaped + "\{([^}]*)\}"));
    assert.ok(match, "missing CSS rule for " + selector);
    assert.match(match[1], /min-height:\s*44px/, selector + " must meet the 44px target minimum");
  }
});


test("Lao editorial design system replaces the old national-flag palette with textile-grounded tokens", () => {
  assert.match(css, /--paper:\s*#F4EFE5/i);
  assert.match(css, /--mekong:\s*#173F3A/i);
  assert.match(css, /--indigo:\s*#34465C/i);
  assert.match(css, /--lac:\s*#A94735/i);
  assert.match(css, /--silk:\s*#FFFCF5/i);
  assert.match(css, /Noto Sans Lao/);
  assert.match(css, /Manrope/);
  assert.match(css, /IBM Plex Mono/);
  assert.match(css, /weave/i);
  assert.doesNotMatch(css, /--red:#ce1126/);
  assert.doesNotMatch(css, /--blue:#002868/);
});

test("service page keeps the working tool visible and exposes the new Lao editorial identity", () => {
  assert.match(html, /class="hero-service[^"]*"/);
  assert.match(html, /class="weave-band"/);
  assert.match(html, /Лаоська\s*<span[^>]*>→<\/span>\s*Українська/);
  for (const id of ["lao-input", "count", "example", "example-complex", "clear", "empty-state", "results", "output", "romanization", "ipa", "copy", "copy-romanization", "copy-ipa", "mode-phonetic", "mode-romanization", "analysis-status", "rows", "warnings"]) {
    assert.match(html, new RegExp('id="' + id + '"'));
  }
});

test("shared design system includes responsive, keyboard, and reduced-motion treatments", () => {
  assert.match(css, /@media\s*\(max-width:\s*900px\)/);
  assert.match(css, /@media\s*\(max-width:\s*620px\)/);
  assert.match(css, /@media\s*\(max-width:\s*380px\)/);
  assert.match(css, /prefers-reduced-motion:\s*reduce/);
  assert.match(css, /:focus-visible/);
  assert.match(css, /min-height:\s*44px/);
  assert.match(css, /::selection/);
});

test("methodology page uses an editorial reading rail and keeps all fourteen sections", async () => {
  const methodology = await readFile(new URL("../system.html", import.meta.url), "utf8");
  assert.match(methodology, /class="reading-rail(?:\s|")/);
  assert.match(methodology, /class="weave-band"/);
  for (let index = 1; index <= 14; index += 1) {
    assert.match(methodology, new RegExp('id="s' + index + '"'));
  }
  const visualResearch = await readFile(new URL("../docs/research/LAO-VISUAL-CULTURE-AND-WEB-DESIGN-REFERENCES-2026-11-10.md", import.meta.url), "utf8");
  assert.match(visualResearch, /Naga|наґа/i);
  assert.match(methodology, /незалежн.{0,100}еталонна вибірка IPA.{0,80}0/i);
});


test("all public site copy explains the product contract and honest uncertainty", async () => {
  const methodology = await readFile(new URL("../system.html", import.meta.url), "utf8");
  assert.match(html, /Вставте лаоське слово, фразу або уривок/);
  assert.match(html, /невідомі позиції позначаються «\?»/);
  assert.match(html, /IPA-адаптер/);
  assert.match(methodology, /Еталонна вибірка IPA ще порожня: незалежно перевірених фахівцями прикладів — 0/);
  assert.match(methodology, /романізація може втрачати тон, довготу та відмінності між голосними/i);
  assert.match(methodology, /не вибирає варіант навмання/);
});

test("methodology documents the culturally grounded Woven Editorial design rationale", async () => {
  const methodology = await readFile(new URL("../system.html", import.meta.url), "utf8");
  assert.match(methodology, /Woven Editorial/);
  assert.match(methodology, /Ми не відтворюємо конкретний етнічний візерунок/);
  assert.match(methodology, /Global InCH/);
  assert.match(methodology, /ресурси W3C щодо лаоського письма/);
  assert.match(methodology, /Noto Sans Lao/);
  assert.match(methodology, /DESIGN\.md/);
  assert.match(methodology, /id="s14"/);
});


test("dynamic service copy uses the same clear Ukrainian vocabulary as the static pages", () => {
  assert.match(app, /Початкова графема/);
  assert.match(app, /Голосний шаблон/);
  assert.match(app, /Попередня IPA-підказка/);
  assert.match(app, /Низька впевненість/);
  assert.match(app, /Зіставлення з оригіналом/);
  assert.match(app, /Тон не визначався/);
});


test("public interface keeps Ukrainian as its language and labels Lao romanization correctly", async () => {
  const methodology = await readFile(new URL("../system.html", import.meta.url), "utf8");
  assert.match(html, /Лаоська\s*<span[^>]*>→<\/span>\s*Українська/);
  assert.match(methodology, /Лаоська\s*<span[^>]*>→<\/span>\s*Українська/);
  assert.match(html, /id="romanization"[^>]*lang="lo-Latn"/);
  assert.doesNotMatch(html, /id="romanization"[^>]*lang="en"/);
  assert.doesNotMatch(html + methodology, /IPA gold corpus/i);
  assert.doesNotMatch(html + methodology, /Lao → Українська/);
  assert.doesNotMatch(html + methodology, /[А-ЯІЇЄҐ]{4,}/);
  assert.match(html, /name="lao-text" autocomplete="off"/);
  assert.match(css, /touch-action:\s*manipulation/);
});

test("visible interface labels use sentence case and explain technical terms in Ukrainian", () => {
  assert.doesNotMatch(css, /\.analysis-grid small\s*\{[^}]*text-transform:\s*uppercase/s);
  assert.doesNotMatch(app, /ГОТОВО|ЧАСТКОВИЙ АНАЛІЗ|НЕ ВСТАНОВЛЕНО/);
  assert.doesNotMatch(app, /PROVISIONAL/);
  assert.match(app, /Попередня IPA-підказка/);
  assert.match(app, /Частковий аналіз/);
  assert.match(app, /Не визначено/);
});

test("the Ukrainian editorial standard defines language, evidence, and contextual humanization rules", async () => {
  const guide = await readFile(new URL("../docs/UKRAINIAN-EDITORIAL-STYLE.md", import.meta.url), "utf8");
  assert.match(guide, /Українська — мова за замовчуванням/);
  assert.match(guide, /lang="lo-Latn"/);
  assert.match(guide, /Це редакторський список, а не автоматичний заборонний словник/);
  assert.match(guide, /Не змінюємо числа, дати, одиниці/);
});

test("public prose states the pipeline and research limits directly", async () => {
  const methodology = await readFile(new URL("../system.html", import.meta.url), "utf8");
  assert.match(html, /запише вимову в IPA/);
  assert.match(methodology, /Між лаоським аналізом і українським записом стоїть Міжнародний фонетичний алфавіт \(IPA\)/);
  assert.match(methodology, /Еталонна вибірка IPA ще порожня: незалежно перевірених фахівцями прикладів — 0/);
  assert.doesNotMatch(methodology, /Це не косметична заміна однієї традиції іншою/);
  assert.doesNotMatch(methodology, /Це поєднання культурної обережності та сучасної вебпрактики/);
  assert.doesNotMatch(methodology, /Pali\/Sanskrit|Language Standardisation in Laos|IPA gold corpus/);
  assert.match(methodology, /палійські й санскритські структури/);
  assert.match(methodology, /Мовна стандартизація в Лаосі/);
  assert.equal((methodology.match(/<p\b/g) || []).length, (methodology.match(/<\/p>/g) || []).length);
  assert.equal((html.match(/<p\b/g) || []).length, (html.match(/<\/p>/g) || []).length);
});

test("editorial copy keeps the named visual concept while avoiding unexplained English craft terms", async () => {
  const methodology = await readFile(new URL("../system.html", import.meta.url), "utf8");
  assert.match(methodology, /Woven Editorial/);
  assert.match(methodology, /додатков.{0,20}основ/i);
  assert.match(methodology, /переривчаст.{0,30}уток/i);
  assert.match(methodology, /Адаптація IPA українською/);
});
