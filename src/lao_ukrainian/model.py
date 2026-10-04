from dataclasses import dataclass, field

@dataclass
class Candidate:
    value: str
    score: float
    rationale: list[str] = field(default_factory=list)

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

@dataclass
class Analysis:
    input: str
    normalized: str
    syllables: list[SyllableAnalysis]
    status: str
    warnings: list[str] = field(default_factory=list)
