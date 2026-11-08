from dataclasses import dataclass, field

@dataclass
class Candidate:
    value: str
    score: float
    rationale: list[str] = field(default_factory=list)

@dataclass(frozen=True)
class PhoneticSegment:
    ipa: str
    kind: str
    provenance: tuple[str, ...] = ()
    certainty: str = "SUPPORTED"


@dataclass(frozen=True)
class PhoneticResult:
    phonemic_ipa: str | None
    segments: tuple[PhoneticSegment, ...]
    syllable_boundaries: tuple[int, ...] = (0,)
    vowel_length: str | None = None
    tone_category: str | None = None
    tone_contour_ipa: str | None = None
    status: str = "SUPPORTED"
    provenance: tuple[str, ...] = ()
    uncertainty: tuple[str, ...] = ()
    broad_surface_ipa: str | None = None
    external_ipa: str | None = None


@dataclass(frozen=True)
class GraphemeEvidence:
    grapheme: str
    role: str
    ipa_hint: str | None = None
    certainty: str = "PROVISIONAL"
    structural_unit: str | None = None


@dataclass(frozen=True)
class GraphemePreview:
    ipa_preview: str | None
    status: str
    graphemes: tuple[GraphemeEvidence, ...] = ()
    unresolved_graphemes: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    phonetic_result: PhoneticResult | None = None


@dataclass
class SyllableAnalysis:
    surface: str
    onset: str | None
    vowel: str | None
    coda: str | None
    tone_mark: str | None
    consonant_class: str | None
    syllable_type: str | None
    tone: str | None
    phonemic_ipa: str | None
    ukrainian_candidates: list[Candidate]
    practical_ukrainian: str | None
    status: str
    rules: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    tone_contour: str | None = None
    phonetic_result: PhoneticResult | None = None
    grapheme_preview: GraphemePreview | None = None

@dataclass
class Analysis:
    input: str
    normalized: str
    syllables: list[SyllableAnalysis]
    status: str
    warnings: list[str] = field(default_factory=list)
