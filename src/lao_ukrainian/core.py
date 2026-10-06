from .normalize import normalize_lao, validate_unicode
from .parser import segment_syllables, parse_syllable
from .phonology import phonologize, classify_syllable_type
from .target import rank_ukrainian_candidates, practical_from_ipa
from .model import Analysis, SyllableAnalysis, Candidate
from .data import load_registry

ESTABLISHED_TONE_STATUSES = {"core", "well-supported"}

def analyze(text: str) -> Analysis:
    normalized = normalize_lao(text)
    warnings = validate_unicode(normalized)
    if warnings:
        return Analysis(text, normalized, [], "INVALID", warnings)

    syllables = []
    analysis_warnings = []
    for surface in segment_syllables(normalized):
        parsed = parse_syllable(surface)
        ipa, rules, tone_status, tone = phonologize(parsed)
        candidates = []
        if ipa:
            for value, score, why in rank_ukrainian_candidates(ipa):
                candidates.append(Candidate(value, score, [why]))

        practical = practical_from_ipa(ipa) if ipa else None
        syllable_type = classify_syllable_type(parsed.get("vowel"), parsed.get("coda"))
        consonant_class = None
        if parsed.get("onset"):
            consonant_class = load_registry()["consonants"].get(parsed["onset"], {}).get("class")

        status = (
            "ESTABLISHED"
            if ipa and practical and tone_status in ESTABLISHED_TONE_STATUSES
            else tone_status
        )
        if practical is None and ipa:
            status = "EVIDENCE LIMITED"

        local_warnings = list(parsed.get("warnings", []))
        analysis_warnings.extend(local_warnings)
        syllables.append(
            SyllableAnalysis(
                surface,
                parsed.get("onset"),
                parsed["vowel"]["id"] if parsed.get("vowel") else None,
                parsed.get("coda"),
                parsed.get("tone_mark"),
                consonant_class,
                syllable_type,
                tone,
                ipa,
                candidates,
                practical,
                status,
                rules,
                local_warnings,
            )
        )

    overall = "OK" if syllables and all(s.status == "ESTABLISHED" for s in syllables) else "PARTIAL"
    return Analysis(text, normalized, syllables, overall, warnings + analysis_warnings)
