from .data import load_registry

MARKS={"່":"mai_ek","້":"mai_tho","໊":"mai_ti","໋":"mai_catawa",None:"none"}

def classify_syllable_type(vowel, coda):
    """Classify live/dead from the phonological rhyme.

    In the Vientiane-oriented model, a final stop/glottal or a short vowel
    makes a syllable checked/dead. Long vowels and sonorant finals are live.
    """
    r=load_registry()
    if coda:
        cr=r["consonants"].get(coda,{})
        final=cr.get("ipa_final")
        if final in {"p","t","k","ʔ"}: return "dead"
        if final in {"m","n","ŋ","w","j","l","r"}: return "live"
    if vowel:
        return "live" if vowel["length"]=="long" else "dead"
    return None

def determine_tone(onset, vowel, coda, tone_mark, onset_class=None):
    r=load_registry()
    cr=r["consonants"].get(onset or "")
    if not cr or not vowel: return (None,"ANALYSIS DEPENDENT",[])
    st=classify_syllable_type(vowel,coda)
    mark=MARKS.get(tone_mark,"unknown")
    cls=onset_class or cr["class"]
    key=(cls,st,vowel["length"],mark)
    for candidate in (key, (cls,st,"*",mark), (cls,"*", "*",mark)):
        for rule in r["tone_rules"]:
            if (rule["class"],rule["syllable_type"],rule["length"],rule["tone_mark"])==candidate:
                return rule["tone"],rule["status"],[rule["rule_id"]]
    return None,"ANALYSIS DEPENDENT",["TONE-NOT-ESTABLISHED-FOR-COMBINATION"]

def phonologize(parsed):
    r=load_registry(); o=r["consonants"].get(parsed["onset"] or ""); v=parsed["vowel"]
    if not o or not v: return None,[],"ANALYSIS DEPENDENT",None
    coda=parsed["coda"]
    coda_ipa=(r["consonants"].get(coda,{}).get("ipa_final") or "") if coda else ""

    # ອ is a middle-class vowel carrier. With an overt vowel it is normally
    # silent; in a closed syllable the spelling ອ itself can represent /ɔː/.
    onset_ipa="" if parsed["onset"]=="ອ" else (o["ipa_initial"] or "")
    tone,status,rules=determine_tone(parsed["onset"],v,coda,parsed["tone_mark"],parsed.get("onset_class"))
    ipa=onset_ipa+v["ipa"]+coda_ipa
    return ipa,rules+([f"TONE:{tone}"] if tone else []),status,tone
