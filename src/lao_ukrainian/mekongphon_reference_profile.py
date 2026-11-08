"""Deterministic IPA convention profile distilled from MekongPhon train diagnostics.

This is an explicitly selected reference-compatibility profile, not a claim
that the model's dictionary IPA is a universal or independently adjudicated
description of Vientiane Lao. The default Vientiane profile is unchanged.
"""

PROFILE_NAME = "mekongphon-reference"
DEFAULT_PROFILE = "vientiane"
HYBRID_PROFILE = "hybrid-deterministic"\nSUPPORTED_IPA_PROFILES = (DEFAULT_PROFILE, PROFILE_NAME, HYBRID_PROFILE)

# Aggregate-only, high-frequency train-split correspondences. The source
# diagnostic uses the pinned 6,219-row MekongPhon training split; it is not
# derived from the 100-row evaluation split. Counts and interpretation are
# documented in docs/research/MEKONGPHON-DETERMINISTIC-RULE-PORT-2026-11-08.md and claim CLM-MEKONGPHON-REFERENCE-PROFILE.
VOWEL_IPA_OVERRIDES = {
    "AW_LONG": "ao",       # engine aw -> reference ao (534 aligned contexts)
    "UA_LONG": "ɯːə̯",    # engine ɯːə -> reference ɯːə̯ (459)
    "IA_LONG": "iaː",      # engine iːə -> reference iaː (275)
    "OEE": "əː",           # engine ɤː -> reference əː (212)
    "AI": "aj",            # engine ai -> reference aj (205)
    "UO_LONG": "uaː",      # engine uːə -> reference uaː (184)
    "UO_LONG_ALT": "uaː",  # engine uːə -> reference uaː (180)
    "AI2": "aj",           # engine ai -> reference aj (158)
    "OE": "ə",             # engine ɤ -> reference ə (86)
}

ONSET_IPA_OVERRIDES = {
    "ວ": "w",  # reference /w/ vs project Vientiane /ʋ/
    "ຣ": "r",  # reference /r/ vs project provisional /l/
}


def apply_ipa_profile(parsed, onset_ipa, vowel_ipa, coda_ipa, profile=DEFAULT_PROFILE):
    """Return profile-specific segmental units and explicit provenance rules."""
    if profile == DEFAULT_PROFILE:
        return onset_ipa, vowel_ipa, coda_ipa, []
    if profile == HYBRID_PROFILE:
        return apply_hybrid_profile(parsed, onset_ipa, vowel_ipa, coda_ipa)
    if profile != PROFILE_NAME:
        raise ValueError(
            f"Unknown IPA profile {profile!r}; expected one of {SUPPORTED_IPA_PROFILES}"
        )

    rules = []
    onset = parsed.get("onset")
    if onset in ONSET_IPA_OVERRIDES and onset_ipa != ONSET_IPA_OVERRIDES[onset]:
        onset_ipa = ONSET_IPA_OVERRIDES[onset]
        rules.append(f"IPA-PROFILE-MEKONGPHON-ONSET:{onset}")

    vowel = parsed.get("vowel") or {}
    vowel_id = vowel.get("id")
    if vowel_id in VOWEL_IPA_OVERRIDES and vowel_ipa != VOWEL_IPA_OVERRIDES[vowel_id]:
        vowel_ipa = VOWEL_IPA_OVERRIDES[vowel_id]
        rules.append(f"IPA-PROFILE-MEKONGPHON-VOWEL:{vowel_id}")

    return onset_ipa, vowel_ipa, coda_ipa, rules


# The hybrid profile treats Vientiane phonology as the base system and applies
# only explicit, train-split-supported MekongPhon convention rules. These
# rules are intentionally no more specific than the evidence currently allows.
from .hybrid_rules import phonological_context, select_rule

HYBRID_RULES = tuple(
    {
        "rule_id": f"HYB-MPH-VOWEL-{vowel_id}",
        "target": "vowel",
        "conditions": {"vowel_id": vowel_id},
        "value": value,
        "priority": 0,
        "provenance": f"IPA-PROFILE-MEKONGPHON-VOWEL:{vowel_id}",
    }
    for vowel_id, value in VOWEL_IPA_OVERRIDES.items()
) + tuple(
    {
        "rule_id": f"HYB-MPH-ONSET-{grapheme}",
        "target": "onset",
        "conditions": {"onset": grapheme},
        "value": value,
        "priority": 0,
        "provenance": f"IPA-PROFILE-MEKONGPHON-ONSET:{grapheme}",
    }
    for grapheme, value in ONSET_IPA_OVERRIDES.items()
)


def apply_hybrid_profile(parsed, onset_ipa, vowel_ipa, coda_ipa):
    """Apply evidence-gated reference rules over the Vientiane IPA baseline."""
    context = phonological_context(parsed)
    rules = []
    for target, current in (("onset", onset_ipa), ("vowel", vowel_ipa)):
        match = select_rule(HYBRID_RULES, context, target=target)
        if match is None or match.value == current:
            continue
        if target == "onset":
            onset_ipa = match.value
        else:
            vowel_ipa = match.value
        rules.extend((match.provenance, f"HYBRID-RULE:{match.rule_id}"))
    return onset_ipa, vowel_ipa, coda_ipa, rules
