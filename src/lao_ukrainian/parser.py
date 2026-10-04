from .data import load_registry

TONE_MARKS={"່","້","໊","໋"}

def segment_syllables(text: str) -> list[str]:
    return [x for x in text.split() if x]

def _strip_tone_marks(surface):
    return ''.join(ch for ch in surface if ch not in TONE_MARKS)

def _find_onset(s):
    r=load_registry()["consonants"]
    for i,ch in enumerate(s):
        if ch in r and r[ch]["status"] in {"core","analysis-dependent"}:
            return ch,i
    return None,None

def _choose_vowel(chars, registry):
    s=''.join(chars)
    best=None
    for row in registry["vowels"]:
        pat=row["pattern"]
        if pat and pat in s:
            if best is None or len(pat)>len(best["pattern"]): best=row
    if any(x in s for x in ("ເ","ແ","ໂ","ໃ","ໄ")):
        if "ແ" in s: key="AE"
        elif "ໂ" in s: key="O"
        elif "ໄ" in s or "ໃ" in s: key="AI"
        else: key="E"
        best=next((x for x in registry["vowels"] if x["id"]==key),best)
    return best

def parse_syllable(surface: str):
    r=load_registry(); s=_strip_tone_marks(surface)
    onset,onset_i=_find_onset(s)
    if onset is None:
        return {"surface":surface,"onset":None,"vowel":None,"coda":None,"tone_mark":next((g for g in TONE_MARKS if g in surface),None)}
    rest=s[:onset_i]+s[onset_i+1:]
    vowel=_choose_vowel(rest,r)
    coda=None
    if vowel:
        for ch in reversed(rest):
            if ch in r["consonants"] and ch != onset and ch not in TONE_MARKS:
                coda=ch; break
    tone_mark=next((g for g in TONE_MARKS if g in surface),None)
    return {"surface":surface,"onset":onset,"vowel":vowel,"coda":coda,"tone_mark":tone_mark}
