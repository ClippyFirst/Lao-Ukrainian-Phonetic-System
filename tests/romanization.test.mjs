import { readFileSync } from "node:fs";
import { test } from "node:test";
import assert from "node:assert/strict";
import { romanizeLao } from "../web/romanization.js";
import { analyze } from "../web/engine.js";

test("CLDR Lao-Latin keeps whitespace and punctuation and maps supported syllable letters",()=>{
 const r=romanizeLao("ຂາ, ຊາ!");
 assert.equal(r.output,"kha, xa!");
 assert.equal(r.source,"CLDR Lao-Latin (provisional; BGN/PCGN-aligned subset)");
});

test("the short Lao mixed-text sample preserves ASCII digits and punctuation",()=>{
 const result=romanizeLao("ສະບາຍດີ 123! ພາສາລາວ.");
 assert.ok(/[a-z]/iu.test(result.output));
 assert.ok(result.output.includes("123"));
 assert.ok(result.output.includes(" "));
 assert.ok(result.output.includes("!"));
 assert.ok(result.output.includes("."));
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
 const sourceAware = analyzeRomanization("ékhôa-niav",{
  sourceSyllableGroups:[
   [{onset:"ຂ",coda:"",vowelId:"AW_LONG"}],
   [{onset:"ໜ",coda:"ວ",vowelId:"IA_LONG"}],
  ],
 });
 assert.equal(sourceAware.status,"OK");
 assert.equal(sourceAware.output,"к'ао-ніао");
});


test("Lao source grapheme cross-check selects aspiration for ຂ instead of literal h",()=>{
 const lao="ຂາ";
 const latin=romanizeLao(lao);
 const source=analyze(lao);
 const adapted=analyzeRomanization(latin.output,{sourceSyllableGroups:[source.syllables.map(s=>({
   onset:s.onset,
   vowelId:s.rules?.find(rule=>rule.startsWith("VOWEL:"))?.slice(6)??null,
   coda:s.coda==="—"?"":s.coda,
  }))]});
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
 const result=romanizationToUkrainian("kha",{sourceSyllableGroups:[[{onset:"ຂ",coda:""}]]});
 assert.equal(result.output,"к'а");
 assert.equal(result.syllables[0].crosswalk,"LAO_SYLLABLE_STRUCTURE↔CLDR_ROMANIZATION↔UKRAINIAN");
});

test("the UI passes the parsed Lao onsets into romanization analysis and copy",()=>{
 const app=readFileSync(new URL("../web/app.js",import.meta.url),"utf8");
 assert.match(app,/function sourceSyllableGroupsForCrosswalk\(sourceText\)/u);
 assert.match(app,/sourceSyllableGroups:\s*sourceSyllableGroupsForCrosswalk\(input\.value\)/u);
 assert.match(app,/onsetForm:\s*syllable\.onsetForm/u);
 assert.match(app,/vowelId:\s*syllable\.rules\?\.find/u);
 assert.match(app,/romanization-syllable-engine\.js\?v=20261031-source-vowel-crosswalk/u);
 assert.ok(app.includes("Лаоська голосна структура"));
 assert.equal(app.includes("sourceOnsetsForCrosswalk"),false);
 assert.equal(app.includes("sourceOnsetGroupsForCrosswalk"),false);
 assert.ok(app.includes("Лаоська початкова графема"));
 assert.ok(app.includes("Лаоська фінальна графема"));
 assert.ok(app.includes("Звірка джерельної структури"));
});


test("full Lao source keeps an independent h onset distinct from aspirated kh",()=>{
 const examples=[
  ["ຂາ","к'а"],
  ["ຄາ","к'а"],
  ["ຮາ","га"],
  ["ຫາ","га"],
  ["ຊາ","са"],
 ];
 for(const [lao,expected] of examples){
  const latin=romanizeLao(lao);
  const source=analyze(lao);
  const adapted=analyzeRomanization(latin.output,{sourceSyllableGroups:[source.syllables.map(s=>({
   onset:s.onset,
   vowelId:s.rules?.find(rule=>rule.startsWith("VOWEL:"))?.slice(6)??null,
   coda:s.coda==="—"?"":s.coda,
  }))]});
  assert.equal(adapted.status,"OK",JSON.stringify({lao,latin:latin.output,source:source.syllables.map(s=>({surface:s.surface,onset:s.onset,coda:s.coda,vowel:s.vowel,status:s.status})),adapted:adapted.syllables,warnings:adapted.warnings}));
  assert.equal(adapted.output,expected,lao);
 }
});

test("a Lao k syllable followed by a real h-onset syllable is preserved as two units",()=>{
 const lao="ກາຮາ";
 const latin=romanizeLao(lao);
 const source=analyze(lao);
 const adapted=analyzeRomanization(latin.output,{sourceSyllableGroups:[source.syllables.map(s=>({
   onset:s.onset,
   vowelId:s.rules?.find(rule=>rule.startsWith("VOWEL:"))?.slice(6)??null,
   coda:s.coda==="—"?"":s.coda,
  }))]});
 assert.equal(latin.output,"kaha");
 assert.deepEqual(source.syllables.map(s=>s.onset),["ກ","ຮ"]);
 assert.equal(adapted.status,"OK");
 assert.equal(adapted.output,"кага");
});


test("source coda graphemes are checked against CLDR output before Ukrainian coda adaptation",()=>{
 const examples=[
  ["ກັດ","kad","кат"],
  ["ກັບ","kab","кап"],
  ["ກາງ","kang","канг"],
  ["ການ","kan","кан"],
  ["ກາມ","kam","кам"],
  ["ກຳ","kam","кам"],
  ["ກາຍ","kagn","кай"],
  ["ກາວ","kav","као"],
 ];
 for(const [lao,expectedLatin,expectedUkrainian] of examples){
  const latin=romanizeLao(lao);
  const source=analyze(lao);
  const adapted=analyzeRomanization(latin.output,{
   sourceSyllableGroups:[source.syllables.map(s=>({
    onset:s.onset,
    vowelId:s.rules?.find(rule=>rule.startsWith("VOWEL:"))?.slice(6)??null,
    coda:s.coda==="—"?"":s.coda??null,
   }))],
  });
  assert.equal(latin.output,expectedLatin,lao);
  assert.equal(adapted.status,"OK",JSON.stringify({lao,latin:latin.output,source:source.syllables.map(s=>({surface:s.surface,onset:s.onset,coda:s.coda,vowel:s.vowel,status:s.status})),adapted:adapted.syllables,warnings:adapted.warnings}));
  assert.equal(adapted.output,expectedUkrainian,lao);
 }
});

test("the full Lao source resolves concatenated CLDR syllables with source onset, vowel and coda evidence",()=>{
 const lao="ເຂົ້າໜຽວ";
 const latin=romanizeLao(lao);
 const source=analyze(lao);
 const sourceSyllableGroups=[source.syllables.map(s=>({
  onset:s.onset,
  vowelId:s.rules?.find(rule=>rule.startsWith("VOWEL:"))?.slice(6)??null,
  coda:s.coda==="—"?"":s.coda??null,
 }))];
 const adapted=analyzeRomanization(latin.output,{sourceSyllableGroups});
 assert.equal(latin.output,"ékhôaniav");
 assert.equal(source.syllables.length,2,JSON.stringify(source.syllables));
 assert.equal(adapted.status,"OK",JSON.stringify({source:sourceSyllableGroups,adapted:adapted.syllables,warnings:adapted.warnings}));
 assert.equal(adapted.output,"к'аоніао");
});

test("BGN silent-hoa spellings romanize sonorants without an audible h",()=>{
 const examples=[
  ["ຫງາ","nga","нга"],
  ["ຫຍາ","gna","ньа"],
  ["ຫນາ","na","на"],
  ["ຫມາ","ma","ма"],
  ["ຫລາ","la","ла"],
  ["ຫຼາ","la","ла"],
  ["ຫວາງ","vang","ванг"],
 ];
 for(const [lao,expectedLatin,expectedUkrainian] of examples){
  const latin=romanizeLao(lao);
  const source=analyze(lao);
  const sourceSyllableGroups=[source.syllables.map(s=>({
   onset:s.onset,
   onsetForm:s.onsetForm||s.onset,
   vowelId:s.rules?.find(rule=>rule.startsWith("VOWEL:"))?.slice(6)??null,
   coda:s.coda==="—"?"":s.coda??null,
  }))];
  const adapted=analyzeRomanization(latin.output,{sourceSyllableGroups});
  assert.equal(latin.output,expectedLatin,lao);
  assert.equal(adapted.status,"OK",JSON.stringify({lao,sourceSyllableGroups,adapted:adapted.syllables,warnings:adapted.warnings}));
  assert.equal(adapted.output,expectedUkrainian,lao);
  assert.equal(adapted.syllables[0].sourceOnset,source.syllables[0].onsetForm||source.syllables[0].onset);
 }
});


test("the full Lao greeting sentence traverses CLDR romanization and the source-aware Ukrainian crosswalk",()=>{
 const sentence="ສະບາຍດີ! ຂ້ອຍຊື່ ນາລີ. ຂ້ອຍມາຈາກປະເທດລາວ ແລະມັກຮຽນພາສາໃໝ່.";
 const separators=/^(\s+|[,.!?;:()[\]{}"“”]+|-+)$/u;
 const sourceSyllableGroups=sentence.split(/(\s+|[,.!?;:()[\]{}"“”]+|-+)/u).filter(Boolean)
  .filter(part=>!separators.test(part)&&!/^[0-9]+$/u.test(part))
  .map(part=>analyze(part).syllables.filter(s=>!s.passthrough).map(s=>({
   onset:s.onset||null,
   onsetForm:s.onsetForm||s.onset||null,
   vowelId:s.rules?.find(rule=>rule.startsWith("VOWEL:"))?.slice(6)??null,
   coda:s.coda==="—"?"":s.coda??null,
  })));
 const latin=romanizeLao(sentence);
 assert.ok(/[a-z]/iu.test(latin.output));
 assert.ok(latin.output.includes(" "));
 assert.ok(latin.output.includes("!"));
 assert.ok(latin.output.includes("."));
 const adapted=analyzeRomanization(latin.output,{sourceSyllableGroups});
 assert.ok(["OK","PARTIAL"].includes(adapted.status));
 assert.ok(adapted.output.length>0);
 assert.ok(adapted.output.includes(" "));
 assert.ok(adapted.output.includes("!"));
 assert.ok(adapted.output.includes("."));
});


test("CLDR Lao-Latin preserves Lao numerals, ASCII numbers, mixed Latin text and punctuation",()=>{
 const source="ຂາ ໒໐໒໖, ABC-42!";
 const result=romanizeLao(source);
 assert.equal(result.output,"kha ໒໐໒໖, ABC-42!");
 assert.equal(result.status,"PARTIAL","Lao numerals remain visible rather than being guessed or discarded");
});


test("full Lao mixed-script multiline text preserves separators, native numerals and foreign text",()=>{
 const input="ຂາ\tABC-42\r\n໑໒໓, ខ្មែរ 😀!";
 const result=romanizeLao(input);
 assert.equal(result.output,"kha\tABC-42\r\n໑໒໓, ខ្មែរ 😀!");
 assert.equal(result.status,"PROVISIONAL");
});
