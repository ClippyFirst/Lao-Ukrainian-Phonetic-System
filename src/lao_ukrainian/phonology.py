from .data import load_registry

MARKS={"່":"mai_ek","້":"mai_tho","໊":"mai_ti","໋":"mai_catawa",None:"none"}

def classify_syllable_type(vowel, coda):
    """Classify live/dead from the phonological rhyme.

    In the Vientiane reference model, a final stop/glottal makes a syllable
    checked/dead.  Open long-vowel syllables and syllables ending in a
    sonorant/glide are live.  A short vowel without a written coda is treated
    as checked because the short-vowel/glottal realization is phonologically
    relevant in the standard description.
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

def determine_tone(onset, vowel, coda, tone_mark):
    r=load_registry(); cr=r["consonants"].get(onset or "")
    if not cr or not vowel: return (None,"ANALYSIS DEPENDENT",[])
    st=classify_syllable_type(vowel,coda); mark=MARKS.get(tone_mark,"unknown")
    key=(cr["class"],st,vowel["length"],mark)
    # Live syllables do not need the short/long distinction in the standard
    # tone chart when the final is a sonorant; fall back to ANY length.
    for candidate in (key, (cr["class"],st,"*",mark)):
        for rule in r["tone_rules"]:
            if (rule["class"],rule["syllable_type"],rule["length"],rule["tone_mark"])==candidate:
                return rule["tone"],rule["status"],[rule["rule_id"]]
    return None,"ANALYSIS DEPENDENT",["TONE-NOT-ESTABLISHED-FOR-COMBINATION"]

def phonologize(parsed):
    r=load_registry(); o=r["consonants"].get(parsed["onset"] or ""); v=parsed["vowel"]
    if not o or not v: return None,[],"ANALYSIS DEPENDENT",None
    coda=parsed["coda"]
    coda_ipa=(r["consonants"].get(coda,{}).get("ipa_final") or "") if coda else ""

    # ອ is a middle-class vowel carrier.  With an overt vowel it contributes
    # tone-class information but normally not an independent /ʔ/ onset.
    onset_ipa="" if parsed["onset"]=="ອ" else (o["ipa_initial"] or "")
    tone,status,rules=determine_tone(parsed["onset"],v,coda,parsed["tone_mark"])
    ipa=onset_ipa+v["ipa"]+coda_ipa
    return ipa,rules+([f"TONE:{tone}"] if tone else []),status,tone
