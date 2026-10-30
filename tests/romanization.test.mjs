import { readFileSync } from "node:fs";
import { test } from "node:test";
import assert from "node:assert/strict";
import { romanizeLao } from "../web/romanization.js";
import { analyze } from "../web/engine.js";

test("CLDR Lao-Latin keeps whitespace and punctuation and maps supported syllable letters",()=>{
 const r=romanizeLao("ຂາ, ຊາ!");
 assert.equal(r.output,"kha, xa!");
 assert.equal(r.source,"CLDR Lao-Latin (provisional; BGN alias)");
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
import { analyzeRomanization } from "../web/romanization-syllable-engine.js";

test("romanization fallback maps CLDR Latin spelling independently of phonetic IPA",()=>{
 const result=romanizationToUkrainian("kha, xa!");
 assert.equal(result.output,"к'а, са!");
 assert.equal(result.status,"OK");
 assert.match(result.source,/romanization/i);
});

test("romanization fallback applies explicit Latin digraph and diacritic rules",()=>{
 assert.equal(romanizationToUkrainian("cha nga pha tha éka").output,"ча нга п'а т'а ке");
});

test("romanization fallback preserves unsupported characters and reports partial coverage",()=>{
 const result=romanizationToUkrainian("kha ໞ");
 assert.equal(result.output,"к'а ⟦ໞ⟧");
 assert.equal(result.status,"PARTIAL");
});


test("romanization-to-Ukrainian independently agrees with the IPA-first aspirated-stop specimen",()=>{
 const lao="ຂາ";
 const latin=romanizeLao(lao);
 const fallback=romanizationToUkrainian(latin.output);
 assert.equal(latin.output,"kha");
 assert.equal(fallback.output,"к'а");
 assert.equal(analyze(lao).output,"к'а");
});


test("romanization h is adapted by phonological function, not as a universal letter rule",()=>{
 assert.equal(romanizationToUkrainian("ha kha tha pha").output,"га к'а т'а п'а");
});

test("CLDR palatal nasal spelling maps to the project's Ukrainian palatal nasal",()=>{
 const latin=romanizeLao("ຍາ");
 assert.equal(latin.output,["g","n","a"].join(""));
 assert.equal(romanizationToUkrainian(latin.output).output,"ньа");
});

test("CLDR output for a multi-syllable Lao example feeds the independent syllable engine",()=>{
 const latin=romanizeLao("ເຂົ້າໜຽວ");
 assert.equal(latin.output,"ékhôaniav");
 const adapted=analyzeRomanization(latin.output);
 assert.equal(adapted.status,"PARTIAL");
 assert.equal(adapted.output,"⟦ékhôaniav⟧");
 assert.equal(analyzeRomanization("ékhôa-niav").output,"к'ао-ніао");
});


test("Lao source grapheme cross-check selects aspiration for ຂ instead of literal h",()=>{
 const lao="ຂາ";
 const latin=romanizeLao(lao);
 const source=analyze(lao);
 const adapted=analyzeRomanization(latin.output,{sourceOnsets:source.syllables.map(s=>s.onset)});
 assert.equal(latin.output,"kha");
 assert.equal(adapted.output,"к'а");
 assert.equal(adapted.status,"OK");
 assert.equal(adapted.syllables[0].sourceOnset,"ຂ");
});

test("source grapheme cross-check does not allow kh to impersonate k",()=>{
 const result=analyzeRomanization("kha",{sourceOnsets:["ກ"]});
 assert.equal(result.status,"PARTIAL");
 assert.equal(result.output,"⟦kha⟧");
});


test("the compatibility API accepts source-onset evidence for the three-way crosswalk",()=>{
 const result=romanizationToUkrainian("kha",{sourceOnsets:["ຂ"]});
 assert.equal(result.output,"к'а");
 assert.equal(result.syllables[0].crosswalk,"LAO_GRAPHEME↔BGN_ROMANIZATION↔UKRAINIAN");
});

test("the UI passes the parsed Lao onsets into romanization analysis and copy",()=>{
 const app=readFileSync(new URL("../web/app.js",import.meta.url),"utf8");
 assert.match(app,/function sourceOnsetGroupsForCrosswalk\(sourceText\)/u);
 assert.match(app,/sourceOnsetGroups:\s*sourceOnsetGroupsForCrosswalk\(input\.value\)/u);
 assert.equal(app.includes("sourceOnsetsForCrosswalk"),false);
 assert.ok(app.includes("Лаоська початкова графема"));
 assert.ok(app.includes("Звірка графеми"));
});
