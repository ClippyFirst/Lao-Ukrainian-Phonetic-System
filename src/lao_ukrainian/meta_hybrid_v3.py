"""Evidence-gated multi-engine comparison layer.

The deterministic hybrid remains the selected segmental/Ukrainian lane.
Pinned MekongPhon non-tonal and tonal models are run as independent
comparators; disagreement is surfaced, never resolved by an unvalidated vote.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import unicodedata
from typing import Any

from .core import analyze
from .hybrid_v2 import HybridV2Result, combine_neural_tones
from .mekongphon import MekongPhonEngine, MekongPhonResult
from .phonetic_result import from_external_ipa

SEPARATOR_CHARS = frozenset(" .·‧")


@dataclass(frozen=True)
class SegmentalComparison:
    status: str
    deterministic_ipa: str | None
    neural_ipa: str | None
    exact_agreement: bool | None
    selected_source: str
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class MetaHybridV3Result:
    """Three source-side analyses with one conservative Ukrainian output."""

    analysis: Any
    segmental_comparison: SegmentalComparison
    nontonal_result: MekongPhonResult | None
    tonal_result: MekongPhonResult | None
    tone_alignment: HybridV2Result | None
    nontonal_error: str | None = None
    tonal_error: str | None = None
    warnings: tuple[str, ...] = ()

    @property
    def ukrainian(self) -> str:
        return "".join(
            item.practical_ukrainian or "?" for item in self.analysis.syllables
        )

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["ukrainian"] = self.ukrainian
        return payload


def _compact_ipa(value: str) -> str:
    normalized = unicodedata.normalize("NFC", value)
    return "".join(char for char in normalized if char not in SEPARATOR_CHARS and not char.isspace())


def compare_segmental_lanes(analysis: Any, neural_raw_ipa: str | None) -> SegmentalComparison:
    """Compare complete accepted deterministic IPA with the non-tonal model.

    This is exact string concordance, not accuracy. It intentionally refuses
    to score provisional/unsupported deterministic units or unsupported
    external IPA, and it never changes the selected production lane.
    """
    syllables = [item for item in analysis.syllables if item.status != "PASSTHROUGH"]
    accepted = all(
        item.phonetic_result is not None
        and item.phonetic_result.status in {"SUPPORTED", "UNCERTAIN"}
        and bool(item.phonetic_result.phonemic_ipa)
        for item in syllables
    )
    deterministic = "".join(item.phonetic_result.phonemic_ipa for item in syllables) if accepted else None
    if neural_raw_ipa is None:
        return SegmentalComparison(
            "UNAVAILABLE", deterministic, None, None,
            "CLIPPYFIRST_HYBRID_DETERMINISTIC",
            ("NON-TONAL-NEURAL-LANE-UNAVAILABLE",),
        )
    parsed = from_external_ipa(neural_raw_ipa, provenance=("META-HYBRID-V3", "SEGMENTAL-COMPARATOR"))
    if not accepted or parsed.status != "SUPPORTED" or not parsed.phonemic_ipa:
        return SegmentalComparison(
            "UNSCORABLE", deterministic, parsed.phonemic_ipa, None,
            "CLIPPYFIRST_HYBRID_DETERMINISTIC",
            ("SEGMENTAL-COMPARISON-REQUIRES-COMPLETE-ACCEPTED-IPA",),
        )
    agrees = _compact_ipa(deterministic or "") == _compact_ipa(parsed.phonemic_ipa)
    return SegmentalComparison(
        "EXACT_AGREEMENT" if agrees else "DISAGREEMENT",
        deterministic,
        parsed.phonemic_ipa,
        agrees,
        "CLIPPYFIRST_HYBRID_DETERMINISTIC",
        () if agrees else ("ENGINE-DISAGREEMENT-IS-NOT-AN-ACCURACY-JUDGMENT",),
    )


def run_meta_hybrid_v3(
    text: str,
    *,
    device: str = "auto",
    num_beams: int = 5,
) -> MetaHybridV3Result:
    """Run deterministic, pinned non-tonal and pinned tonal analyses.

    Both neural lanes are optional. Each failure is recorded independently;
    deterministic Ukrainian output remains available. No majority vote,
    synthetic mixed IPA, or neural-to-Ukrainian shortcut is performed.
    """
    analysis = analyze(text)
    empty_comparison = SegmentalComparison(
        "UNAVAILABLE", None, None, None, "CLIPPYFIRST_HYBRID_DETERMINISTIC"
    )
    if analysis.status == "INVALID":
        return MetaHybridV3Result(
            analysis, empty_comparison, None, None, None,
            warnings=("DETERMINISTIC-INPUT-INVALID", *analysis.warnings),
        )

    results: dict[str, MekongPhonResult | None] = {}
    errors: dict[str, str | None] = {}
    for lane, tonal in (("nontonal", False), ("tonal", True)):
        engine = MekongPhonEngine(tonal=tonal, device=device, num_beams=num_beams)
        try:
            results[lane] = engine.transcribe(text)
            errors[lane] = None
        except (ValueError, RuntimeError, OSError) as exc:
            results[lane] = None
            errors[lane] = f"{type(exc).__name__}: {exc}"

    nontonal = results["nontonal"]
    tonal = results["tonal"]
    comparison = compare_segmental_lanes(
        analysis, nontonal.raw_ipa if nontonal is not None else None
    )
    tone_alignment = (
        combine_neural_tones(
            analysis, tonal.raw_ipa,
            model_id=tonal.model_id, model_revision=tonal.model_revision,
        )
        if tonal is not None else None
    )
    warnings = [
        "META-HYBRID-V3-IS-A-COMPARISON-ORCHESTRATOR-NOT-A-VALIDATED-VOTING-ENSEMBLE",
        "UKRAINIAN-OUTPUT-REMAINS-DETERMINISTIC-IPA-ADAPTER-RESULT",
    ]
    if errors["nontonal"]:
        warnings.append("NON-TONAL-ENGINE-FAILED")
    if errors["tonal"]:
        warnings.append("TONAL-ENGINE-FAILED")
    if comparison.status == "DISAGREEMENT":
        warnings.append("SEGMENTAL-ENGINE-DISAGREEMENT")
    if tone_alignment is not None:
        warnings.extend(tone_alignment.warnings)
    return MetaHybridV3Result(
        analysis=analysis,
        segmental_comparison=comparison,
        nontonal_result=nontonal,
        tonal_result=tonal,
        tone_alignment=tone_alignment,
        nontonal_error=errors["nontonal"],
        tonal_error=errors["tonal"],
        warnings=tuple(warnings),
    )
