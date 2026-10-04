from .data import load_registry

def rank_ukrainian_candidates(ipa: str):
    r=load_registry(); exact=r["correspondences"].get(ipa)
    if exact:
        vals=exact["candidates"].split("|")
        return [(v,float(exact["preferred_score"])-i*0.1,exact["rationale"]) for i,v in enumerate(vals)]
    return []

def practical_from_ipa(ipa: str) -> str | None:
    r=load_registry(); keys=sorted(r["correspondences"],key=len,reverse=True)
    out=[]; i=0
    while i<len(ipa):
        hit=next((k for k in keys if ipa.startswith(k,i)),None)
        if not hit: return None
        out.append(r["correspondences"][hit]["candidates"].split("|")[0]); i+=len(hit)
    return ''.join(out)
