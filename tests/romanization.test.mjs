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

test("GitHub Pages service navigation stays inside the repository site",()=>{
 const html=readFileSync(new URL("../index.html",import.meta.url),"utf8");
 assert.ok(html.includes('href="./">Сервіс</a>'));
 assert.equal(html.includes('href="/">Сервіс</a>'),false);
});
