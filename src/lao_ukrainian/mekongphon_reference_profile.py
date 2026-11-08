"""Deterministic IPA convention profile distilled from MekongPhon train diagnostics.

This is an explicitly selected reference-compatibility profile, not a claim
that the model's dictionary IPA is a universal or independently adjudicated
description of Vientiane Lao. The default Vientiane profile is unchanged.
"""

PROFILE_NAME = "mekongphon-reference"
DEFAULT_PROFILE = "vientiane"
SUPPORTED_IPA_PROFILES = (DEFAULT_PROFILE, PROFILE_NAME)

# Aggregate-only, high-frequency train-split correspondences. The source
# diagnostic uses the pinned 6,219-row MekongPhon training split; it is not
# derived from the 100-row evaluation split. Counts and interpretation are
# documented in docs/research/MEKONGPHON-DETERMINISTIC-RULE-PORT-2026-11-08.md.
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
