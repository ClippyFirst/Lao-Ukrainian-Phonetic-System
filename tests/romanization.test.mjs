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

test("romanization fallback maps CLDR Latin spelling independently of phonetic IPA",()=>{
 const result=romanizationToUkrainian("kha, xa!");
 assert.equal(result.output,"кга, кса!");
 assert.equal(result.status,"OK");
 assert.match(result.source,/romanization/i);
});

test("romanization fallback applies explicit Latin digraph and diacritic rules",()=>{
 assert.equal(romanizationToUkrainian("cha nga pha tha éka").output,"ча нга пга тга ке");
});

test("romanization fallback preserves unsupported characters and reports partial coverage",()=>{
 const result=romanizationToUkrainian("kha ໞ");
 assert.equal(result.output,"кга ⟦ໞ⟧");
 assert.equal(result.status,"PARTIAL");
});


test("romanization-to-Ukrainian remains distinct from the IPA-first result",()=>{
 const lao="ຂາ";
 const latin=romanizeLao(lao);
 const fallback=romanizationToUkrainian(latin.output);
 assert.equal(latin.output,"kha");
 assert.equal(fallback.output,"кга");
 assert.equal(analyze(lao).output,"к'а");
});


test("romanization h is always adapted as Ukrainian г",()=>{
 assert.equal(romanizationToUkrainian("ha kha tha pha").output,"га кга тга пга");
});

test("CLDR palatal nasal spelling maps to the project's Ukrainian palatal nasal",()=>{
 const latin=romanizeLao("ຍາ");
 assert.equal(latin.output,["g","n","a"].join(""));
 assert.equal(romanizationToUkrainian(latin.output).output,"ньа");
});
