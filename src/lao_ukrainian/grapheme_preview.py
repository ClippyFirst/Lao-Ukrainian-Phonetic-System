"""Conservative grapheme-level IPA previews for structurally unresolved Lao."""
from dataclasses import replace

from .model import GraphemeEvidence, GraphemePreview
from .parser import HIGH_DIGRAPHS, TONE_MARKS
from .phonetic_result import from_phonology

VOWEL_GRAPHEMES = set("ະັາິີຶືຸູົຽອໍຳເແໂໃໄ")
INVENTORY_ONLY_CERTAINTY = {"PALI_ONLY", "OUT_OF_SCOPE_KHMU", "NOT_USED_MODERN_LAO", "NONPHONOLOGICAL", "ORTHOGRAPHIC_ONLY"}


def preview_from_graphemes(surface: str, parsed: dict, registry: dict) -> GraphemePreview:
    """Expose known segmental hints; retain unresolved signs and never infer tone."""
    chars = list(surface)
    roles: dict[int, GraphemeEvidence] = {}
    ipa_parts: list[str] = []
    unresolved: list[str] = []
    warnings: list[str] = []

    for i, ch in enumerate(chars):
        if ch in TONE_MARKS:
            roles[i] = GraphemeEvidence(ch, "tone-mark", None, "STRUCTURAL_ONLY")

    onset_form = parsed.get("onset_form") or parsed.get("onset")
    onset_index = surface.find(onset_form) if onset_form else -1
    onset_length = len(onset_form) if onset_index >= 0 else 0
    onset_ipa = parsed.get("onset_ipa")

    if onset_index >= 0 and onset_length:
        if onset_form in registry["onset_clusters"]:
            row = registry["onset_clusters"][onset_form]
            onset_ipa = row.get("ipa_initial") or onset_ipa
            roles[onset_index] = GraphemeEvidence(chars[onset_index], "labialized-onset-unit", onset_ipa, "PROVISIONAL", onset_form)
            for i in range(onset_index + 1, onset_index + onset_length):
                roles[i] = GraphemeEvidence(chars[i], "labialization-component", None, "PROVISIONAL", onset_form)
        elif onset_form in HIGH_DIGRAPHS:
            base = HIGH_DIGRAPHS[onset_form]
            onset_ipa = registry["consonants"].get(base, {}).get("ipa_initial") or onset_ipa
            roles[onset_index] = GraphemeEvidence(chars[onset_index], "silent-high-class-modifier", None, "STRUCTURAL_ONLY", onset_form)
            roles[onset_index + 1] = GraphemeEvidence(chars[onset_index + 1], "high-class-onset", onset_ipa, "PROVISIONAL", onset_form)
        else:
            row = registry["consonants"].get(parsed.get("onset") or "", {})
            if onset_ipa is None:
                onset_ipa = "" if parsed.get("onset") == "ອ" else row.get("ipa_initial")
            role = "vowel-carrier" if parsed.get("onset") == "ອ" else "syllable-onset"
            roles[onset_index] = GraphemeEvidence(chars[onset_index], role, onset_ipa or None, "PROVISIONAL", onset_form)
        if onset_ipa:
            ipa_parts.append(onset_ipa)

    vowel = parsed.get("vowel")
    if vowel and vowel.get("ipa"):
        ipa_parts.append(vowel["ipa"])
        vowel_indices = [i for i, ch in enumerate(chars) if i not in roles and ch in VOWEL_GRAPHEMES]
        unit = "".join(chars[i] for i in vowel_indices)
        for offset, i in enumerate(vowel_indices):
            roles[i] = GraphemeEvidence(chars[i], "vowel-structure-component", vowel["ipa"] if offset == 0 else None, "PROVISIONAL", unit or None)

    coda = parsed.get("coda")
    if coda:
        i = next((index for index in range(len(chars) - 1, -1, -1)
                  if chars[index] == coda and index not in roles), -1)
        coda_ipa = registry["consonants"].get(coda, {}).get("ipa_final")
        if coda_ipa and i >= 0:
            ipa_parts.append(coda_ipa)
            roles[i] = GraphemeEvidence(chars[i], "syllable-coda", coda_ipa, "PROVISIONAL", coda)

    for i, ch in enumerate(chars):
        if i in roles:
            continue
        inventory_row = next((row for row in registry.get("grapheme_inventory", []) if row["grapheme"] == ch), None)
        if inventory_row:
            role = inventory_row["structural_role"]
            certainty = "STRUCTURAL_ONLY" if inventory_row["engine_status"] in INVENTORY_ONLY_CERTAINTY else "UNRESOLVED"
        elif ch in registry["consonants"]:
            role, certainty = "unresolved-consonant-position", "UNRESOLVED"
        elif ch in VOWEL_GRAPHEMES:
            role, certainty = "unresolved-vowel-component", "UNRESOLVED"
        else:
            role, certainty = "unregistered-grapheme", "UNRESOLVED"
        roles[i] = GraphemeEvidence(ch, role, None, certainty)
        unresolved.append(ch)

    if not ipa_parts:
        warnings.append("NO_CONFIDENT_SEGMENTAL_HINT")
    if unresolved:
        warnings.append("UNRESOLVED_GRAPHEME_OR_POSITION")
    warnings.extend(parsed.get("warnings", []))
    warnings.append("TONE_NOT_INFERRED_BY_GRAPHEME_PREVIEW")

    ipa_preview = "".join(ipa_parts) or None
    typed = None
    if ipa_preview:
        typed = from_phonology(
            ipa_preview,
            vowel_length=vowel.get("length") if vowel else None,
            status="PROVISIONAL",
            provenance=("GRAPHEME-POSITION-PREVIEW",),
            uncertainty=tuple(dict.fromkeys(warnings)),
        )
        typed = replace(typed, segments=tuple(replace(segment, certainty="PROVISIONAL") for segment in typed.segments))

    return GraphemePreview(
        ipa_preview=ipa_preview,
        status="PROVISIONAL" if ipa_preview else "UNRESOLVED",
        graphemes=tuple(roles[i] for i in range(len(chars))),
        unresolved_graphemes=tuple(unresolved),
        warnings=tuple(dict.fromkeys(warnings)),
        phonetic_result=typed,
    )
