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
  assert.match(html, /<details class="trace-panel trace-disclosure">\s*<summary[^>]*>.*?Поскладовий розбір/s);
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
