import { readFileSync } from "node:fs";
import { test } from "node:test";
import assert from "node:assert/strict";
import { romanizeLao } from "../web/romanization.js";

test("CLDR Lao-Latin keeps whitespace and punctuation and maps supported syllable letters",()=>{
 const r=romanizeLao("ຂາ, ຊາ!");
 assert.equal(r.output,"kha, xa!");
 assert.equal(r.source,"CLDR Lao-Latin/UNGEGN (provisional)");
});

test("CLDR Lao-Latin does not silently delete unsupported Lao code points",()=>{
 const r=romanizeLao("ຂາໞ");
 assert.equal(r.status,"PARTIAL");
 assert.match(r.output,/ໞ/u);
});

test("GitHub Pages navigation stays inside the repository site",()=>{
 const service=readFileSync(new URL("../index.html",import.meta.url),"utf8");
 const system=readFileSync(new URL("../system.html",import.meta.url),"utf8");
 for (const html of [service,system]) {
  assert.ok(html.includes('href="./">Сервіс</a>'));
  assert.equal(html.includes('href="/">Сервіс</a>'),false);
 }
 assert.ok(system.includes('aria-current="page" href="./system.html"'));
});

import { romanizationToUkrainian } from "../web/romanization-ukrainian.js";

test("romanization fallback maps CLDR Latin spelling independently of phonetic IPA",()=>{
 const result=romanizationToUkrainian("kha, xa!");
 assert.equal(result.output,"кха, кса!");
 assert.equal(result.status,"OK");
 assert.match(result.source,/romanization/i);
});

test("romanization fallback applies explicit Latin digraph and diacritic rules",()=>{
 assert.equal(romanizationToUkrainian("ch ng ph th é è ô").output,"ч нг пх тх е е о");
});

test("romanization fallback preserves unsupported characters and reports partial coverage",()=>{
 const result=romanizationToUkrainian("kha ໞ");
 assert.equal(result.output,"кха ໞ");
 assert.equal(result.status,"PARTIAL");
});
