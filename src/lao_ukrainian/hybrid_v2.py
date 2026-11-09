"""Second evidence-gated Lao G2P hybrid.

The deterministic ClippyFirst engine remains authoritative for segmental IPA
and Ukrainian rendering. The pinned MekongPhon tonal model contributes only a
syllable-aligned tone contour. No neural segmental output is substituted into
the deterministic IPA stream.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, replace
from typing import Any

from .core import analyze
from .mekongphon import MekongPhonEngine
from .model import Analysis
from .phonetic_result import from_external_ipa

MEKONG_CONTOUR_TO_CATEGORY = {
    "˩˧": "low-rising",
    "˧˥": "high-rising",
    "˧": "high-mid",
    "˧˩": "low-falling",
    "˥˨": "high-falling",
}
_ACCEPTED_SEGMENTAL_STATUSES = frozenset({"SUPPORTED", "UNCERTAIN"})


def _unique_tone_sequence(symbols: str, syllable_count: int) -> tuple[str, ...] | None:
    """Split an ordered tone-symbol stream into one unique contour per syllable."""
    contours = tuple(sorted(MEKONG_CONTOUR_TO_CATEGORY, key=lambda value: (-len(value), value)))
    solutions: list[tuple[str, ...]] = []

    def visit(offset: int, remaining: int, chosen: tuple[str, ...]) -> None:
        if len(solutions) > 1:
            return
        if remaining == 0:
            if offset == len(symbols):
                solutions.append(chosen)
            return
        for contour in contours:
            if symbols.startswith(contour, offset):
                visit(offset + len(contour), remaining - 1, (*chosen, contour))

    if syllable_count < 1 or not symbols:
        return None
    visit(0, syllable_count, ())
    return solutions[0] if len(solutions) == 1 else None


@dataclass(frozen=True)
class HybridV2Result:
    """Inspectable result with independent provenance for both stages."""

    analysis: Analysis
    model_id: str
    model_revision: str
    neural_raw_ipa: str
    tone_alignment_status: str
    aligned_syllables: int
    tone_overlays: int
    skipped_tone_units: int
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def combine_neural_tones(
    deterministic_analysis: Analysis,
    neural_raw_ipa: str,
    *,
    model_id: str,
    model_revision: str,
) -> HybridV2Result:
    """Overlay only recognized neural tone contours with exact syllable alignment.

    The neural model's segmental phones are deliberately ignored. A contour is
    accepted only when the whole neural IPA string is parseable, the number of
    dot/space-delimited neural syllables exactly matches the deterministic
    parser, and that syllable contains one registered MekongPhon contour.
    Potential minor syllables with unresolved deterministic tone are not
    assigned a neural tone from orthography alone.
    """
    analysis = deepcopy(deterministic_analysis)
    trace = (
        "HYBRID-V2",
        "TONE-SOURCE:MEKONGPHON-TONAL",
        f"MODEL:{model_id}",
        f"MODEL-REVISION:{model_revision}",
    )
    parsed = from_external_ipa(neural_raw_ipa, provenance=trace)
    phonetic_syllables = [
        item for item in analysis.syllables if item.status != "PASSTHROUGH"
    ]
    tone_symbols = "".join(
        segment.ipa for segment in parsed.segments if segment.kind == "tone"
    )

    warnings: list[str] = []
    if parsed.status != "SUPPORTED":
        warnings.append("NEURAL-IPA-UNSUPPORTED; tone overlay withheld")
        return HybridV2Result(
            analysis, model_id, model_revision, neural_raw_ipa,
            "NOT_ALIGNED", 0, 0, len(phonetic_syllables), tuple(warnings),
        )
    contours = _unique_tone_sequence(tone_symbols, len(phonetic_syllables))
    if contours is None:
        warnings.append(
            "NEURAL-TONE-SEQUENCE-NOT-UNIQUELY-ALIGNED; tone overlay withheld "
            f"({len(tone_symbols)} tone symbols for {len(phonetic_syllables)} deterministic syllables)"
        )
        return HybridV2Result(
            analysis, model_id, model_revision, neural_raw_ipa,
            "NOT_ALIGNED", 0, 0, len(phonetic_syllables), tuple(warnings),
        )
    warnings.append("NEURAL-TONE-SEQUENCE-ALIGNED-BY-ORDER; no explicit syllable delimiters required")

    overlays = 0
    skipped = 0
    for syllable, contour in zip(phonetic_syllables, contours):
        category = MEKONG_CONTOUR_TO_CATEGORY.get(contour)
        current = syllable.phonetic_result
        if (
            category is None
            or current is None
            or current.status not in _ACCEPTED_SEGMENTAL_STATUSES
            or current.tone_category is None
        ):
            skipped += 1
            continue

        uncertainty = list(current.uncertainty)
        uncertainty.append("NEURAL-TONE-PREDICTION-NOT-INDEPENDENTLY-ADJUDICATED")
        uncertainty.append("NEURAL-TONE-SEQUENCE-ALIGNED-BY-ORDER")
        if current.tone_category != category:
            uncertainty.append(
                f"DETERMINISTIC-NEURAL-TONE-DISAGREEMENT:{current.tone_category}->{category}"
            )
        tone_segments = tuple(
            replace(segment, provenance=tuple(dict.fromkeys((*segment.provenance, *trace))))
            for segment in neural_segments if segment.kind == "tone"
        )
        syllable.phonetic_result = replace(
            current,
            segments=(*current.segments, *tone_segments),
            syllable_boundaries=(0, len(current.segments) + len(tone_segments)),
            tone_category=category,
            tone_contour_ipa=contour,
            provenance=tuple(dict.fromkeys((*current.provenance, *trace))),
            uncertainty=tuple(dict.fromkeys(uncertainty)),
        )
        syllable.tone = category
        syllable.tone_contour = contour
        syllable.rules = [
            *syllable.rules,
            "HYBRID-V2:DETERMINISTIC-SEGMENTAL+NEURAL-TONE",
        ]
        overlays += 1

    if skipped:
        warnings.append(f"NEURAL-TONE-UNUSED-OR-UNRESOLVED:{skipped}")
    status = "ORDER_ALIGNED" if skipped == 0 else "PARTIAL"
    return HybridV2Result(
        analysis, model_id, model_revision, neural_raw_ipa,
        status, len(spans), overlays, skipped, tuple(warnings),
    )


def run_hybrid_v2(
    text: str,
    *,
    revision: str | None = None,
    device: str = "auto",
    num_beams: int = 5,
) -> HybridV2Result:
    """Run deterministic segmental analysis plus the pinned tonal model.

    Model/dependency/input failures are intentionally surfaced. This function
    never silently falls back to the first hybrid.
    """
    deterministic = analyze(text)
    engine = MekongPhonEngine(
        tonal=True, revision=revision, device=device, num_beams=num_beams
    )
    neural = engine.transcribe(text)
    return combine_neural_tones(
        deterministic,
        neural.raw_ipa,
        model_id=neural.model_id,
        model_revision=neural.model_revision,
    )
