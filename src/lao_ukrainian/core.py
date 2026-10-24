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

    registry = load_registry()
    syllables = []
    analysis_warnings = []
    for surface in segment_syllables(normalized):
        parsed = parse_syllable(surface)
        local_warnings = list(parsed.get("warnings", []))
        ipa, rules, tone_status, tone = phonologize(parsed)

        # An unconsumed source suffix means the parser did not establish the
        # whole orthographic unit. Never let a valid onset/vowel prefix become
        # a complete-looking IPA or Ukrainian form for the full input.
        unconsumed = any(
            warning.startswith("UNCONSUMED_AFTER_VOWEL:")
            for warning in local_warnings
        )
        if unconsumed:
            ipa = None
            rules = [*rules, "PHON-IPA-WITHHELD-UNCONSUMED-ORTHOGRAPHY"]

        candidates = []
        if ipa:
            for value, score, why in rank_ukrainian_candidates(ipa):
                candidates.append(Candidate(value, score, [why]))

        practical = practical_from_ipa(ipa) if ipa else None
        syllable_type = classify_syllable_type(parsed.get("vowel"), parsed.get("coda"))
        consonant_class = parsed.get("onset_class")
        if consonant_class is None and parsed.get("onset"):
            consonant_class = registry["consonants"].get(parsed["onset"], {}).get("class")

        onset_status = registry["consonants"].get(parsed.get("onset") or "", {}).get("status")
        status = (
            "ESTABLISHED"
            if ipa and practical and tone_status in ESTABLISHED_TONE_STATUSES and onset_status in {"core", "analysis-dependent"}
            else tone_status
        )
        if onset_status == "analysis-dependent" and ipa and practical and tone_status in ESTABLISHED_TONE_STATUSES:
            status = "ANALYSIS DEPENDENT"
            analysis_warnings.append(f"ONSET-ANALYSIS-DEPENDENT:{parsed.get('onset')}")

        if practical is None and ipa:
            status = "EVIDENCE LIMITED"
        if unconsumed:
            status = "EVIDENCE LIMITED"

        # Even if an IPA string is computable, malformed/unconsumed source
        # material must prevent an ESTABLISHED status.
        if local_warnings and status == "ESTABLISHED":
            status = "EVIDENCE LIMITED"
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
