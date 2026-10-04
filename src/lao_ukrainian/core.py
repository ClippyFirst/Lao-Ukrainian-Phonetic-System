from .normalize import normalize_lao, validate_unicode
from .parser import segment_syllables, parse_syllable
from .phonology import phonologize
from .target import rank_ukrainian_candidates, practical_from_ipa
from .model import Analysis, SyllableAnalysis, Candidate

def analyze(text: str) -> Analysis:
    normalized=normalize_lao(text); warnings=validate_unicode(normalized)
    if warnings: return Analysis(text,normalized,[],"INVALID",warnings)
    syllables=[]
    for surface in segment_syllables(normalized):
        p=parse_syllable(surface); ipa,rules,status,tone=phonologize(p)
        candidates=[]
        if ipa:
            for val,score,why in rank_ukrainian_candidates(ipa):
                candidates.append(Candidate(val,score,[why]))
        practical=practical_from_ipa(ipa) if ipa else None
        st="ESTABLISHED" if ipa and practical and status=="core" else status
        if practical is None: st="EVIDENCE LIMITED"
        syllables.append(SyllableAnalysis(surface,p["onset"],p["vowel"]["id"] if p["vowel"] else None,p["coda"],p["tone_mark"],None,None,tone,ipa,candidates,practical,st,rules,[]))
    return Analysis(text,normalized,syllables,"OK",warnings)
