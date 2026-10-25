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
        short_vowel_missing_coda = any(
            warning.startswith("SHORT_VOWEL_REQUIRES_CODA:")
            for warning in local_warnings
        )
        multiple_tone_marks = "MULTIPLE_TONE_MARKS" in local_warnings
        structural_uncertainty = unconsumed or short_vowel_missing_coda
        if structural_uncertainty or multiple_tone_marks:
            # Once the written unit is structurally uncertain, a previously
            # matched tone rule is not evidence for this malformed surface.
            tone_rule_ids = {row["rule_id"] for row in registry["tone_rules"]}
            rules = [rule for rule in rules
                     if rule not in tone_rule_ids and not rule.startswith("TONE:")]
            if "TONE-NOT-ESTABLISHED-FOR-COMBINATION" not in rules:
                rules = [*rules, "TONE-NOT-ESTABLISHED-FOR-COMBINATION"]
            ipa = None
            tone = None
            tone_status = "analysis-dependent"
        if structural_uncertainty:
            # A parsed prefix is not enough to establish either the full IPA
            # or tone: the missing coda changes the realization of short
            # vowels and can change the live/dead tone classification.
            rules = [*rules, "PHON-IPA-WITHHELD-STRUCTURAL-UNCERTAINTY",
                     "PHON-TONE-WITHHELD-STRUCTURAL-UNCERTAINTY"]
            if unconsumed:
                rules.append("PHON-IPA-WITHHELD-UNCONSUMED-ORTHOGRAPHY")
            if short_vowel_missing_coda:
                rules.append("PHON-IPA-WITHHELD-SHORT-VOWEL-CODA-REQUIRED")
        if multiple_tone_marks:
            rules = [*rules, "PHON-IPA-WITHHELD-MULTIPLE-TONE-MARKS",
                     "PHON-TONE-WITHHELD-MULTIPLE-TONE-MARKS"]

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
        if structural_uncertainty or multiple_tone_marks:
            status = "EVIDENCE LIMITED"

        # Even if an IPA string is computable, malformed/unconsumed source
        # material must prevent an ESTABLISHED status.
        if local_warnings and status == "ESTABLISHED":
            status = "EVIDENCE LIMITED"
        tone_contour = next(
            (row["contour"] for row in registry["tone_rules"]
             if tone is not None and row["rule_id"] in rules),
            None,
        )
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
                tone_contour=tone_contour,
            )
        )

    overall = "OK" if syllables and all(s.status == "ESTABLISHED" for s in syllables) else "PARTIAL"
    return Analysis(text, normalized, syllables, overall, warnings + analysis_warnings)
