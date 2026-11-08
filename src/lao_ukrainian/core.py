from .normalize import normalize_lao, validate_unicode, PASSTHROUGH_CHARACTERS, LAO_NATIVE_DIGITS
from .parser import segment_syllables, parse_syllable
from .phonology import phonologize, classify_syllable_type
from .target import rank_ukrainian_candidates, practical_from_ipa
from .phonetic_result import from_phonology
from .model import Analysis, SyllableAnalysis, Candidate
from .data import load_registry
from .grapheme_preview import preview_from_graphemes
from .mekongphon_reference_profile import DEFAULT_ENGINE_PROFILE, SUPPORTED_IPA_PROFILES

ESTABLISHED_TONE_STATUSES = {"core", "well-supported"}
MINOR_C0_EXCLUDED_ONSETS = {"ງ", "ຍ"}


def analyze(text: str, *, ipa_profile: str = DEFAULT_ENGINE_PROFILE) -> Analysis:
    if ipa_profile not in SUPPORTED_IPA_PROFILES:
        raise ValueError(f"Unknown IPA profile {ipa_profile!r}; expected one of {SUPPORTED_IPA_PROFILES}")
    normalized = normalize_lao(text)
    warnings = validate_unicode(normalized)
    if warnings:
        return Analysis(text, normalized, [], "INVALID", warnings)

    registry = load_registry()
    syllables = []
    analysis_warnings = []
    # Keep orthographic token boundaries: spaces and ZWSPs delimit the
    # parser's current word-like units. Do not infer minor-syllable relations
    # across phrase whitespace.
    syllable_groups = [
        segment_syllables(token, registry)
        for token in normalized.replace("\u200b", " ").split()
    ]
    for group in syllable_groups:
        for syllable_index, surface in enumerate(group):
            # Match the browser engine's explicit non-Lao passthrough contract:
            # preserve ASCII letters/digits and common punctuation unchanged.
            # These are not assigned IPA and never enter the Ukrainian IPA adapter.
            if len(surface) == 1 and surface in PASSTHROUGH_CHARACTERS:
                syllables.append(
                    SyllableAnalysis(
                        surface=surface,
                        onset=None,
                        vowel=None,
                        coda=None,
                        tone_mark=None,
                        consonant_class=None,
                        syllable_type=None,
                        tone=None,
                        phonemic_ipa=None,
                        ukrainian_candidates=[],
                        practical_ukrainian=surface,
                        status="PASSTHROUGH",
                        rules=["PASSTHROUGH:LAO_NATIVE_DIGIT" if surface in LAO_NATIVE_DIGITS else "PASSTHROUGH:NON_LAO_ORTHOGRAPHIC_CHARACTER"],
                        warnings=[],
                    )
                )
                continue

            parsed = parse_syllable(surface, registry)
            local_warnings = list(parsed.get("warnings", []))
            ipa, rules, tone_status, tone = phonologize(parsed, registry, ipa_profile)

            # Ueda (1994) and Enfield (2007) describe reduced/minor syllables
            # without an independent lexical tone. Orthography alone cannot
            # prove that a matching shape is minor, so flag only a narrow
            # initial short-A candidate and withhold its tone pending review.
            onset_status = registry["consonants"].get(parsed.get("onset") or "", {}).get("status")
            minor_rule = next(
                (row for row in registry["special_tone_rules"]
                 if row["rule_id"] == "VNT-POTENTIAL-MINOR-OPEN-A-UNRESOLVED"),
                None,
            )
            following = (
                parse_syllable(group[1], registry)
                if syllable_index == 0 and len(group) > 1 else {}
            )
            following_vowel = following.get("vowel") or {}
            following_onset = following.get("onset")
            following_onset_status = registry["consonants"].get(
                following_onset or "", {}
            ).get("status")
            following_ipa = (
                phonologize(following, registry, ipa_profile)[0] if following else None
            )
            following_major_weighted = (
                following_vowel.get("length") == "long"
                or following_vowel.get("nucleus_type") == "diphthong"
                or following.get("coda") is not None
            )
            potential_minor_open_a = (
                syllable_index == 0
                and len(group) > 1
                and (parsed.get("vowel") or {}).get("id") == "A"
                and parsed.get("coda") is None
                and parsed.get("tone_mark") is None
                and not local_warnings
                and ipa is not None
                and onset_status == "core"
                and parsed.get("onset") not in MINOR_C0_EXCLUDED_ONSETS
                and following_onset_status == "core"
                and following_ipa is not None
                and following_major_weighted
                and not following.get("warnings")
            )
            if minor_rule and potential_minor_open_a:
                rules = [
                    rule for rule in rules
                    if not rule.startswith("VNT-") and not rule.startswith("TONE:")
                ]
                tone = None
                tone_status = minor_rule["status"]
                rules.extend([
                    minor_rule["rule_id"],
                    "TONE-POTENTIAL-MINOR-SYLLABLE-UNRESOLVED",
                ])
            if parsed.get("onset_ipa"):
                rules = [*rules, f"ONSET-CLUSTER:{parsed.get('onset_form')}"]

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
            malformed_tone_mark_order = any(
                warning.startswith("MALFORMED_TONE_MARK_") for warning in local_warnings
            )
            onset_cluster_uncertainty = any(
                warning in {"AMBIGUOUS_LABIALIZED_ONSET_VOWEL_BOUNDARY", "LABIALIZED_ONSET_BEFORE_ROUNDED_VOWEL"}
                for warning in local_warnings
            )
            structural_uncertainty = unconsumed or short_vowel_missing_coda or onset_cluster_uncertainty
            if structural_uncertainty or multiple_tone_marks or malformed_tone_mark_order:
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
                if onset_cluster_uncertainty:
                    rules.append("PHON-IPA-WITHHELD-ONSET-CLUSTER-UNCERTAINTY")
                    rules.append("PHON-TONE-WITHHELD-ONSET-CLUSTER-UNCERTAINTY")
            if multiple_tone_marks:
                rules = [*rules, "PHON-IPA-WITHHELD-MULTIPLE-TONE-MARKS",
                         "PHON-TONE-WITHHELD-MULTIPLE-TONE-MARKS"]
            if malformed_tone_mark_order:
                rules = [*rules, "PHON-IPA-WITHHELD-MALFORMED-TONE-MARK-ORDER",
                         "PHON-TONE-WITHHELD-MALFORMED-TONE-MARK-ORDER"]

            phonetic_status = (
                "SUPPORTED"
                if ipa and onset_status == "core" and not local_warnings
                else "UNCERTAIN" if ipa else "UNSUPPORTED"
            )
            phonetic_result = from_phonology(
                ipa,
                vowel_length=parsed.get("vowel", {}).get("length") if parsed.get("vowel") else None,
                tone=tone,
                tone_contour=next(
                    (row["contour"] for row in registry["tone_rules"]
                     if tone is not None and row["rule_id"] in rules and row["contour"]),
                    None,
                ),
                status=phonetic_status,
                provenance=tuple(rules),
                uncertainty=tuple(local_warnings) + (() if tone_status in ESTABLISHED_TONE_STATUSES else ("TONE-UNRESOLVED",)),
            )
            candidates = [
                Candidate(value, score, [why])
                for value, score, why in rank_ukrainian_candidates(phonetic_result, registry)
            ]
            practical = practical_from_ipa(phonetic_result, registry)
            syllable_type = classify_syllable_type(parsed.get("vowel"), parsed.get("coda"), registry)
            consonant_class = parsed.get("onset_class")
            if consonant_class is None and parsed.get("onset"):
                consonant_class = registry["consonants"].get(parsed["onset"], {}).get("class")

            status = (
                "ESTABLISHED"
                if ipa and practical and tone_status in ESTABLISHED_TONE_STATUSES and onset_status in {"core", "analysis-dependent"}
                else tone_status
            )
            if onset_status == "analysis-dependent" and ipa and tone_status in ESTABLISHED_TONE_STATUSES:
                status = "ANALYSIS DEPENDENT"
                analysis_warnings.append(f"ONSET-ANALYSIS-DEPENDENT:{parsed.get('onset')}")

            if practical is None and ipa:
                status = "ANALYSIS DEPENDENT" if phonetic_result.status == "UNCERTAIN" else "EVIDENCE LIMITED"
            if structural_uncertainty or multiple_tone_marks or malformed_tone_mark_order:
                status = "EVIDENCE LIMITED"

            # Even if an IPA string is computable, malformed/unconsumed source
            # material must prevent an ESTABLISHED status.
            if local_warnings and status == "ESTABLISHED":
                status = "EVIDENCE LIMITED"
            tone_contour = next(
                (row["contour"] for row in registry["tone_rules"]
                 if tone is not None and row["rule_id"] in rules and row["contour"]),
                None,
            )
            # Diagnostic-only fallback: never promote partial grapheme hints to accepted IPA or Ukrainian output.
            grapheme_preview = preview_from_graphemes(surface, parsed, registry) if ipa is None else None
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
                    phonetic_result=phonetic_result,
                    grapheme_preview=grapheme_preview,
                )
            )

    overall = (
        "OK"
        if syllables and all(s.status in {"ESTABLISHED", "PASSTHROUGH"} for s in syllables)
        else "PARTIAL"
    )
    return Analysis(text, normalized, syllables, overall, warnings + analysis_warnings)
