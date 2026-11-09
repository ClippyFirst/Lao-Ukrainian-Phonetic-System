"""Second evidence-gated Lao G2P hybrid with separate best-in-class lanes.

ClippyFirst remains authoritative for segmental IPA and Ukrainian rendering.
The pinned MekongPhon tonal model supplies an untouched full tonal IPA stream.
Tone contours are associated with deterministic syllables only when a unique
ordered contour decomposition matches the deterministic syllable count.
No artificial mixed IPA string is constructed.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
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
class NeuralTonePrediction:
    """A model-supplied contour associated with one deterministic syllable."""

    syllable_index: int
    source_surface: str
    contour: str
    category: str
    certainty: str = "UNCERTAIN"
    provenance: tuple[str, ...] = ()


@dataclass(frozen=True)
class HybridV2Result:
    """Two independent IPA lanes plus optional order-aligned tone metadata."""

    analysis: Analysis
    model_id: str
    model_revision: str
    neural_raw_ipa: str
    tone_alignment_status: str
    aligned_syllables: int
    tone_predictions: tuple[NeuralTonePrediction, ...]
    skipped_tone_units: int
    warnings: tuple[str, ...] = ()

    @property
    def tonal_ipa(self) -> str:
        """Return the neural tonal IPA unchanged; never rebuild it from phones."""
        return self.neural_raw_ipa

    @property
    def ukrainian(self) -> str:
        return "".join(item.practical_ukrainian or "?" for item in self.analysis.syllables)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["tonal_ipa"] = self.tonal_ipa
        payload["ukrainian"] = self.ukrainian
        return payload


def combine_neural_tones(
    deterministic_analysis: Analysis,
    neural_raw_ipa: str,
    *,
    model_id: str,
    model_revision: str,
) -> HybridV2Result:
    """Keep deterministic output intact and attach uniquely aligned tone predictions.

    The neural model's segmental phones and their positions are never used to
    rewrite deterministic IPA. Its raw tonal IPA is preserved byte-for-byte
    (after the adapter's NFC parse only for diagnostics). A tone sequence is
    associated with syllables only if it has exactly one decomposition into
    registered MekongPhon contours matching the deterministic syllable count.
    Potential minor syllables with unresolved deterministic tone are not
    assigned a neural category from orthography alone.
    """
    trace = (
        "HYBRID-V2",
        "TONE-SOURCE:MEKONGPHON-TONAL",
        f"MODEL:{model_id}",
        f"MODEL-REVISION:{model_revision}",
    )
    parsed = from_external_ipa(neural_raw_ipa, provenance=trace)
    phonetic_syllables = [
        item for item in deterministic_analysis.syllables
        if item.status != "PASSTHROUGH"
    ]
    tone_symbols = "".join(
        segment.ipa for segment in parsed.segments if segment.kind == "tone"
    )
    warnings: list[str] = []
    if parsed.status != "SUPPORTED":
        warnings.append("NEURAL-IPA-UNSUPPORTED; raw tonal IPA preserved; tone association withheld")
        return HybridV2Result(
            deterministic_analysis, model_id, model_revision, neural_raw_ipa,
            "NOT_ALIGNED", 0, (), len(phonetic_syllables), tuple(warnings),
        )

    contours = _unique_tone_sequence(tone_symbols, len(phonetic_syllables))
    if contours is None:
        warnings.append(
            "NEURAL-TONE-SEQUENCE-NOT-UNIQUELY-ALIGNED; raw tonal IPA preserved; "
            "syllable-level association withheld "
            f"({len(tone_symbols)} tone symbols for {len(phonetic_syllables)} deterministic syllables)"
        )
        return HybridV2Result(
            deterministic_analysis, model_id, model_revision, neural_raw_ipa,
            "NOT_ALIGNED", 0, (), len(phonetic_syllables), tuple(warnings),
        )

    warnings.append(
        "NEURAL-TONE-SEQUENCE-ALIGNED-BY-ORDER; raw tonal IPA remains a separate lane"
    )
    predictions: list[NeuralTonePrediction] = []
    skipped = 0
    for index, (syllable, contour) in enumerate(zip(phonetic_syllables, contours)):
        current = syllable.phonetic_result
        category = MEKONG_CONTOUR_TO_CATEGORY[contour]
        if (
            current is None
            or current.status not in _ACCEPTED_SEGMENTAL_STATUSES
            or current.tone_category is None
        ):
            skipped += 1
            continue
        predictions.append(NeuralTonePrediction(
            syllable_index=index,
            source_surface=syllable.surface,
            contour=contour,
            category=category,
            certainty="UNCERTAIN",
            provenance=trace + ("ALIGNMENT:ORDER-ONLY",),
        ))
        if current.tone_category != category:
            warnings.append(
                f"DETERMINISTIC-NEURAL-TONE-DISAGREEMENT:{index}:"
                f"{current.tone_category}->{category}"
            )

    if skipped:
        warnings.append(f"NEURAL-TONE-UNASSOCIATED-UNRESOLVED-SYLLABLES:{skipped}")
    status = "ORDER_ALIGNED" if skipped == 0 else "PARTIAL"
    return HybridV2Result(
        deterministic_analysis, model_id, model_revision, neural_raw_ipa,
        status, len(contours), tuple(predictions), skipped, tuple(warnings),
    )


def run_hybrid_v2(
    text: str,
    *,
    revision: str | None = None,
    device: str = "auto",
    num_beams: int = 5,
) -> HybridV2Result:
    """Run deterministic segmental analysis plus the pinned tonal model.

    Expected model/dependency/length failures preserve the deterministic
    Ukrainian lane and return NEURAL_UNAVAILABLE with an explicit warning.
    Unexpected programming errors still propagate; no fallback is silent.
    """
    deterministic = analyze(text)
    engine = MekongPhonEngine(
        tonal=True, revision=revision, device=device, num_beams=num_beams
    )
    if deterministic.status == "INVALID":
        return HybridV2Result(
            deterministic, engine.model_id, engine.revision, "",
            "INVALID_INPUT", 0, (), 0,
            ("DETERMINISTIC-INPUT-INVALID", *deterministic.warnings),
        )
    try:
        neural = engine.transcribe(text)
    except (ValueError, RuntimeError, OSError) as exc:
        phonetic_syllables = [
            item for item in deterministic.syllables if item.status != "PASSTHROUGH"
        ]
        return HybridV2Result(
            deterministic, engine.model_id, engine.revision, "",
            "NEURAL_UNAVAILABLE", 0, (), len(phonetic_syllables),
            (f"NEURAL-INFERENCE-UNAVAILABLE:{type(exc).__name__}:{exc}",),
        )
    return combine_neural_tones(
        deterministic,
        neural.raw_ipa,
        model_id=neural.model_id,
        model_revision=neural.model_revision,
    )
