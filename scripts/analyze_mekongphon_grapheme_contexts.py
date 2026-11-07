#!/usr/bin/env python3
"""Aggregate Lao grapheme-to-sound discovery from MekongPhon train data.

The parser identifies syllable structure first. IPA references are aligned to
onset, joint vowel-structure and coda units. Multi-grapheme vowel spellings
remain joint units; the report never invents independent phonemes for signs.
Only aggregate contexts are written, never source words or per-item outputs.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, unicodedata, urllib.request
from collections import Counter
from pathlib import Path
from lao_ukrainian.data import load_registry
from lao_ukrainian.parser import HIGH_DIGRAPHS, TONE_MARKS, parse_syllable, segment_syllables
from lao_ukrainian.phonetic_result import IPA_SYMBOLS
from lao_ukrainian.phonology import classify_syllable_type

DATA_URL = "https://raw.githubusercontent.com/byu-matrix-lab/MekongPhon/f80f6c1840c4818b51e05f2e00cded4701a5b662/data/splits/lao_train.csv"
DATA_REVISION = "f80f6c1840c4818b51e05f2e00cded4701a5b662"
EXPECTED_ROWS = 6219
EXPECTED_SHA256 = "2d0f68989009620980ced3386f11a640e6167404308eeb6a79efc52bc8e40ee0"
SYMBOLS = tuple(sorted(IPA_SYMBOLS, key=len, reverse=True))
VOWEL_ABOVE, VOWEL_BELOW = set("ິີຶືໍ"), set("ຸູ")
VOWEL_POSTPOSED, VOWEL_PREPOSED = set("ະັາົອຳວຽ"), set("ເແໂໃໄ")

def nfc(s): return unicodedata.normalize("NFC", s.strip())

def tokenize_ipa(value):
    out=[]; i=0
    while i<len(value):
        token=next((s for s in SYMBOLS if value.startswith(s,i)),None)
        if token is None: out.append(value[i]); i+=1
        else: out.append(token); i+=len(token)
    return out

def align_tokens(predicted, reference):
    n,m=len(predicted),len(reference); dp=[[0]*(m+1) for _ in range(n+1)]
    for i in range(n+1): dp[i][0]=i
    for j in range(m+1): dp[0][j]=j
    for i in range(1,n+1):
        for j in range(1,m+1):
            dp[i][j]=min(dp[i-1][j]+1,dp[i][j-1]+1,dp[i-1][j-1]+(predicted[i-1]!=reference[j-1]))
    mapping={}; insertions=0; i,j=n,m
    while i or j:
        if i and j and predicted[i-1]==reference[j-1] and dp[i][j]==dp[i-1][j-1]:
            mapping[i-1]=reference[j-1]; i-=1; j-=1
        elif i and j and dp[i][j]==dp[i-1][j-1]+1:
            mapping[i-1]=reference[j-1]; i-=1; j-=1
        elif i and dp[i][j]==dp[i-1][j]+1:
            mapping[i-1]=None; i-=1
        else: insertions+=1; j-=1
    return mapping,dp[n][m],insertions

def grapheme_units(surface):
    out=[]; i=0
    while i<len(surface):
        start=i; i+=1
        while i<len(surface) and unicodedata.category(surface[i]) in {"Mn","Mc"}: i+=1
        out.append((surface[start:i],start,i))
    return out

def structural_components(surface, parsed, registry):
    tone_indices=[i for i,ch in enumerate(surface) if ch in TONE_MARKS]
    clean="".join(ch for ch in surface if ch not in TONE_MARKS)
    onset_form=parsed.get("onset_form") or parsed.get("onset") or ""
    onset_start=clean.find(onset_form) if onset_form else -1
    if onset_start<0: return None
    onset_idx=list(range(onset_start,onset_start+len(onset_form)))
    coda=parsed.get("coda"); coda_idx=len(clean)-1 if coda and clean.endswith(coda) else None
    excluded=set(onset_idx)
    if coda_idx is not None: excluded.add(coda_idx)
    vowel_idx=[i for i in range(len(clean)) if i not in excluded]
    if not vowel_idx: return None
    onset=parsed.get("onset") or ""; cluster=registry["onset_clusters"].get(onset_form)
    high=onset_form in HIGH_DIGRAPHS
    if cluster: onset_ipa=cluster.get("ipa_initial") or ""
    else:
        row=registry["consonants"].get(onset,{})
        onset_ipa="" if onset=="ອ" else (row.get("ipa_initial") or "")
    vowel=parsed.get("vowel") or {}
    coda_ipa=registry["consonants"].get(coda or "",{}).get("ipa_final") or ""
    clean_to_surface=[i for i,ch in enumerate(surface) if ch not in TONE_MARKS]
    onset_si=[clean_to_surface[i] for i in onset_idx]
    vowel_si=[clean_to_surface[i] for i in vowel_idx]
    coda_si=[clean_to_surface[coda_idx]] if coda_idx is not None else []
    vowel_pattern="".join(clean[i] for i in vowel_idx)
    components=[
        {"surface":onset_form,"role":"onset","ipa":onset_ipa},
        {"surface":vowel_pattern,"role":"vowel_structure","ipa":vowel.get("ipa") or ""},
    ]
    if coda_si: components.append({"surface":coda,"role":"coda","ipa":coda_ipa})
    return {"components":components,"tone_indices":tone_indices,"onset_indices":onset_si,
        "vowel_indices":vowel_si,"coda_indices":coda_si,"onset":onset,
        "onset_form":onset_form,"onset_ipa":onset_ipa,"vowel":vowel,"coda":coda,"high_digraph":high,"cluster":bool(cluster)}

def role_for_index(index, structure, surface):
    if index in structure["tone_indices"]: return "tone_mark","tone_only_not_segmental"
    if index in structure["onset_indices"]:
        indices=structure["onset_indices"]
        if structure["high_digraph"] and index==indices[0]: return "high_class_modifier","silent_tone_class_modifier"
        if structure["cluster"] and index==indices[-1]: return "labialization_modifier","joint_onset_unit"
        return "onset_base","onset_unit"
    if index in structure["coda_indices"]: return "coda","coda_unit"
    ch=surface[index]
    if ch in VOWEL_PREPOSED: return "preposed_vowel_sign","joint_vowel_structure"
    if ch in VOWEL_ABOVE: return "vowel_sign_above","joint_vowel_structure"
    if ch in VOWEL_BELOW: return "vowel_sign_below","joint_vowel_structure"
    if ch in VOWEL_POSTPOSED: return "vowel_sign_postposed","joint_vowel_structure"
    return "vowel_component","joint_vowel_structure"

def analyze_rows(rows, registry):
    sound=Counter(); contexts=Counter(); units=Counter(); tone=Counter(); warnings=Counter()
    parsed_words=skipped=syllable_total=exact=edits_total=ref_total=insertions_total=0
    for row in rows:
        orth,reference=nfc(row["orth"]),nfc(row["pron_no_tones"])
        syllables=segment_syllables(orth,registry)
        parsed=[parse_syllable(s,registry) for s in syllables]
        if not syllables or any(p.get("vowel") is None or p.get("warnings") for p in parsed):
            skipped+=1
            for p in parsed:
                for warning in p.get("warnings",[]): warnings[str(warning).split(":",1)[0]]+=1
            continue
        structures=[structural_components(s,p,registry) for s,p in zip(syllables,parsed)]
        if any(x is None for x in structures): skipped+=1; continue
        components=[c for st in structures for c in st["components"]]
        predicted="".join(c["ipa"] for c in components)
        pred_tokens,ref_tokens=tokenize_ipa(predicted),tokenize_ipa(reference)
        mapping,edits,insertions=align_tokens(pred_tokens,ref_tokens)
        parsed_words+=1; syllable_total+=len(syllables); edits_total+=edits
        ref_total+=len(ref_tokens); insertions_total+=insertions
        exact+=predicted==reference
        offsets=[]; off=0
        for st in structures:
            offsets.append(off); off+=sum(len(tokenize_ipa(c["ipa"])) for c in st["components"])
        for si,(surface,p,st,offset) in enumerate(zip(syllables,parsed,structures,offsets)):
            pos="initial" if si==0 else "final" if si==len(syllables)-1 else "medial"
            vowel=p["vowel"]; stype=classify_syllable_type(vowel,st["coda"],registry) or "unknown"
            onset_class=p.get("onset_class") or registry["consonants"].get(p.get("onset") or "",{}).get("class","unknown")
            mark=p.get("tone_mark") or "none"; component_offset=offset; observed={}
            for comp in st["components"]:
                toks=tokenize_ipa(comp["ipa"])
                aligned=[mapping.get(component_offset+k) for k in range(len(toks))]
                actual="".join(x for x in aligned if x is not None)
                observed[comp["role"]]=actual
                units[(comp["role"],comp["surface"],comp["ipa"],actual,pos,actual==comp["ipa"])]+=1
                component_offset+=len(toks)
            graphemes=grapheme_units(surface)
            for gi,(unit,start,end) in enumerate(graphemes):
                for idx in range(start,end):
                    role,scope=role_for_index(idx,st,surface)
                    if role=="tone_mark": actual=""; pattern=surface[idx]
                    elif role=="high_class_modifier":
                        actual=""; pattern=st["onset_form"]
                    elif role in {"onset_base","labialization_modifier"}:
                        actual=observed.get("onset",""); pattern=st["onset_form"]
                    elif role=="coda": actual=observed.get("coda",""); pattern=st["coda"] or ""
                    else:
                        actual=observed.get("vowel_structure","")
                        pattern=vowel.get("pattern") or "".join(surface[j] for j in st["vowel_indices"])
                    prev=graphemes[gi-1][0] if gi else "^"
                    nxt=graphemes[gi+1][0] if gi+1<len(graphemes) else "$"
                    sound[(unit,role,pos,pattern,actual,scope)]+=1
                    contexts[(unit,role,pos,prev,nxt,onset_class,vowel.get("id",""),stype,st["coda"] or "open",mark,scope)]+=1
                    if role=="tone_mark": tone[(unit,pos,onset_class,stype,vowel.get("id",""),st["coda"] or "open")]+=1
    rule_groups=Counter()
    for (grapheme,role,pos,pattern,actual,scope),count in sound.items():
        rule_groups[(grapheme,role,pos,pattern,scope)] += count
    distributions={}
    for key in rule_groups:
        grapheme,role,pos,pattern,scope=key
        outcomes=[{"ipa":ipa,"count":count} for (g,r,p,pat,ipa,sc),count in sound.items()
                  if (g,r,p,pat,sc)==key]
        outcomes.sort(key=lambda item:(-item["count"],item["ipa"]))
        total=rule_groups[key]
        distributions[key]={
            "grapheme":grapheme,"role":role,"word_position":pos,
            "orthographic_unit":pattern,"sound_scope":scope,"observations":total,
            "realizations":[{**item,"share":item["count"]/total} for item in outcomes],
            "consistency":outcomes[0]["count"]/total if outcomes else None,
            "evidence_tier":"high-frequency" if total>=100 else "medium-frequency" if total>=30 else "low-frequency",
        }
    return {
      "method":{"alignment":"Longest-match IPA inventory plus Levenshtein; deterministic backtrace",
        "unit":"parser-derived onset, joint vowel structure and coda",
        "vowels":"A multi-grapheme vowel spelling maps jointly to its nucleus; individual signs are not assigned fictitious independent phonemes",
        "consonants":"Onset bases, silent high-class modifiers, labialization modifiers and codas are distinct roles",
        "positions":"Initial/medial/final syllable within parser-segmented whitespace token",
        "limitation":"Reference alignment is conditional on ClippyFirst structural parsing; skipped or mis-segmented words are reported, not guessed",
        "gold":"MekongPhon train split is development evidence, not independent expert gold"},
      "source":{"repository":"byu-matrix-lab/MekongPhon","revision":DATA_REVISION,"train_sha256":EXPECTED_SHA256,"rows_expected":EXPECTED_ROWS},
      "summary":{"rows_received":len(rows),"fully_structured_words":parsed_words,"skipped_words":skipped,
        "parsed_syllables":syllable_total,"exact_structural_ipa_words":exact,
        "structural_word_exact_rate":exact/parsed_words if parsed_words else None,
        "reference_ipa_tokens":ref_total,"alignment_edits":edits_total,"alignment_insertions":insertions_total,
        "parser_warning_codes":dict(warnings.most_common())},
      "candidate_contextual_rules":sorted(distributions.values(),key=lambda x:(-x["observations"],x["grapheme"],x["role"])),
      "grapheme_sound_contexts":[{"grapheme":k[0],"role":k[1],"word_position":k[2],"orthographic_unit":k[3],
        "observed_ipa_at_unit_scope":k[4],"sound_scope":k[5],"count":v} for k,v in sound.most_common(1500)],
      "grapheme_context_features":[{"grapheme":k[0],"role":k[1],"word_position":k[2],"previous_grapheme":k[3],
        "next_grapheme":k[4],"onset_class":k[5],"vowel_id":k[6],"syllable_type":k[7],
        "coda":k[8],"tone_mark":k[9],"sound_scope":k[10],"count":v} for k,v in contexts.most_common(3000)],
      "structural_unit_alignments":[{"role":k[0],"orthographic_unit":k[1],"engine_ipa":k[2],
        "reference_aligned_ipa":k[3],"word_position":k[4],"exact_unit_match":k[5],"count":v}
        for k,v in units.most_common(3000)],
      "tone_mark_contexts":[{"tone_mark":k[0],"word_position":k[1],"onset_class":k[2],
        "syllable_type":k[3],"vowel_id":k[4],"coda":k[5],"count":v} for k,v in tone.most_common(500)]
    }

def load_train():
    with urllib.request.urlopen(DATA_URL,timeout=60) as response: raw=response.read()
    digest=hashlib.sha256(raw).hexdigest()
    if digest!=EXPECTED_SHA256: raise SystemExit(f"Train SHA-256 mismatch: {digest}")
    rows=list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
    if len(rows)!=EXPECTED_ROWS: raise SystemExit(f"Expected {EXPECTED_ROWS} rows, got {len(rows)}")
    return rows

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=Path("artifacts/mekongphon-grapheme-contexts.json"))
    args=parser.parse_args(); result=analyze_rows(load_train(),load_registry())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")
    print(json.dumps(result["summary"],ensure_ascii=False,sort_keys=True))

if __name__=="__main__": main()
