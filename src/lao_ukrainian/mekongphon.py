"""Primary neural Lao-to-IPA adapter for BYU MATRIX Lab's MekongPhon models.

Model weights are downloaded from Hugging Face at runtime and are not bundled
with ClippyFirst. The deterministic rule engine remains available explicitly
as an independent diagnostic/alternative, never as a silent fallback.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import re
import unicodedata
from typing import Any

from .normalize import normalize_lao, validate_unicode
from .phonetic_result import from_external_ipa
from .model import PhoneticResult
from .target import adapt_phonetic_result

MODEL_IDS = {
    "tonal": "byumatrixlab/lao-ipa-tonal",
    "nontonal": "byumatrixlab/lao-ipa-nontonal",
}
MODEL_REVISIONS = {
    "tonal": "e02608cfcb18abfe6b1916f5f4774bfac9ac788d",
    "nontonal": "d6ea20cb73eaab8f3adc4eb044e61bdb9bef3f5b",
}
MAX_SEQUENCE_LENGTH = 128
_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class MekongPhonUnavailableError(RuntimeError):
    """Raised when optional neural dependencies are not installed."""


@dataclass(frozen=True)
class MekongPhonIPAResult:
    """Output of stage 1 only: Lao orthography to typed IPA."""

    input: str
    normalized_input: str
    model_id: str
    model_revision: str
    tonal: bool
    num_beams: int
    raw_ipa: str
    phonetic_result: PhoneticResult
    status: str
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MekongPhonResult:
    input: str
    normalized_input: str
    model_id: str
    model_revision: str
    tonal: bool
    num_beams: int
    raw_ipa: str
    phonetic_result: PhoneticResult
    ukrainian: str | None
    status: str
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_result(
    text: str,
    raw_ipa: str,
    *,
    model_id: str,
    model_revision: str,
    tonal: bool,
    num_beams: int = 5,
) -> MekongPhonResult:
    """Pure result assembly, separated from model loading for testability."""
    normalized = normalize_lao(text)
    provenance = ("MEKONGPHON", model_id, f"MODEL-REVISION:{model_revision}")
    phonetic = from_external_ipa(raw_ipa, provenance=provenance)
    ukrainian = adapt_phonetic_result(phonetic)
    warnings: list[str] = []
    if not _SHA_RE.fullmatch(model_revision):
        warnings.append("MODEL-REVISION-NOT-IMMUTABLE")
    if phonetic.status != "SUPPORTED":
        status = "IPA_UNSUPPORTED"
    elif ukrainian is None:
        status = "TARGET_MAPPING_UNAVAILABLE"
        warnings.append("NO_COMPLETE_UKRAINIAN_MAPPING")
    else:
        status = "OK"
    return MekongPhonResult(
        input=text,
        normalized_input=normalized,
        model_id=model_id,
        model_revision=model_revision,
        tonal=tonal,
        num_beams=num_beams,
        raw_ipa=raw_ipa,
        phonetic_result=phonetic,
        ukrainian=ukrainian,
        status=status,
        warnings=tuple(warnings),
    )


class MekongPhonEngine:
    """Lazy CPU/CUDA inference wrapper around the upstream EncoderDecoderModel."""

    def __init__(
        self,
        *,
        tonal: bool = True,
        revision: str | None = None,
        device: str = "auto",
        num_beams: int = 5,
    ) -> None:
        if num_beams < 1 or num_beams > 8:
            raise ValueError("num_beams must be between 1 and 8")
        if device not in {"auto", "cpu", "cuda"}:
            raise ValueError("device must be auto, cpu or cuda")
        self.tonal = tonal
        model_key = "tonal" if tonal else "nontonal"
        self.model_id = MODEL_IDS[model_key]
        self.revision = revision or MODEL_REVISIONS[model_key]
        self.device_name = device
        self.num_beams = num_beams
        self._loaded = None

    def _load(self):
        if self._loaded is not None:
            return self._loaded
        try:
            import torch
            from transformers import AutoTokenizer, EncoderDecoderModel
        except ImportError as exc:
            raise MekongPhonUnavailableError(
                "Install optional neural dependencies with pip install -e '.[neural]'."
            ) from exc

        if self.device_name == "cuda" and not torch.cuda.is_available():
            raise RuntimeError("CUDA was requested but is not available")
        device = (
            "cuda" if self.device_name == "cuda"
            else "cpu" if self.device_name == "cpu"
            else "cuda" if torch.cuda.is_available()
            else "cpu"
        )
        kwargs = {"revision": self.revision} if self.revision else {}
        model = EncoderDecoderModel.from_pretrained(
            self.model_id, trust_remote_code=False, **kwargs
        )
        encoder_tokenizer = AutoTokenizer.from_pretrained(
            self.model_id, subfolder="encoder_tokenizer",
            trust_remote_code=False, **kwargs
        )
        decoder_tokenizer = AutoTokenizer.from_pretrained(
            self.model_id, subfolder="decoder_tokenizer",
            trust_remote_code=False, **kwargs
        )
        model.to(device)
        model.eval()
        config_revision = getattr(model.config, "_commit_hash", None)
        if config_revision and self.revision and config_revision != self.revision:
            raise RuntimeError(
                f"Loaded {self.model_id} at {config_revision}, expected {self.revision}"
            )
        resolved_revision = (
            config_revision
            or getattr(model.config, "revision", None)
            or self.revision
            or "unresolved"
        )
        self._loaded = (
            torch, model, encoder_tokenizer, decoder_tokenizer,
            device, str(resolved_revision),
        )
        return self._loaded

    def _validated_input(self, text: str) -> str:
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Lao input must be a non-empty string")
        normalized = unicodedata.normalize("NFC", text)
        problems = validate_unicode(normalized)
        if problems:
            raise ValueError("Input contains unsupported characters: " + "; ".join(problems))
        if len(normalized) > MAX_SEQUENCE_LENGTH:
            raise ValueError(
                f"Input is {len(normalized)} code points; model limit is "
                f"{MAX_SEQUENCE_LENGTH}. Split it explicitly; automatic truncation is disabled."
            )
        return normalized

    def _generate_raw_ipa(self, normalized: str) -> str:
        torch, model, encoder_tokenizer, decoder_tokenizer, device, _ = self._load()
        encoded = encoder_tokenizer(
            normalized, return_tensors="pt", truncation=False, padding=False,
        )
        if encoded["input_ids"].shape[-1] > MAX_SEQUENCE_LENGTH:
            raise ValueError(
                "Tokenized input exceeds the model's 128-token limit; "
                "automatic truncation is disabled."
            )
        encoded = encoded.to(device)
        with torch.inference_mode():
            output_ids = model.generate(
                **encoded,
                max_length=MAX_SEQUENCE_LENGTH,
                num_beams=self.num_beams,
                early_stopping=True,
            )
        return decoder_tokenizer.decode(output_ids[0], skip_special_tokens=True)

    def predict_raw_ipa(self, text: str) -> str:
        """Run the pinned model and return its untouched decoded IPA string."""
        return self._generate_raw_ipa(self._validated_input(text))

    def transcribe_ipa(self, text: str) -> MekongPhonIPAResult:
        """Run stage 1 and stop at typed IPA; do not invoke Ukrainian mapping."""
        normalized = self._validated_input(text)
        raw_ipa = self._generate_raw_ipa(normalized)
        *_, resolved_revision = self._load()
        provenance = (
            "MEKONGPHON", self.model_id, f"MODEL-REVISION:{resolved_revision}"
        )
        phonetic = from_external_ipa(raw_ipa, provenance=provenance)
        warnings: list[str] = []
        if not _SHA_RE.fullmatch(resolved_revision):
            warnings.append("MODEL-REVISION-NOT-IMMUTABLE")
        status = "OK" if phonetic.status == "SUPPORTED" else "IPA_UNSUPPORTED"
        return MekongPhonIPAResult(
            input=text,
            normalized_input=normalized,
            model_id=self.model_id,
            model_revision=resolved_revision,
            tonal=self.tonal,
            num_beams=self.num_beams,
            raw_ipa=raw_ipa,
            phonetic_result=phonetic,
            status=status,
            warnings=tuple(warnings),
        )

    def transcribe(self, text: str) -> MekongPhonResult:
        """Run both stages: Lao → MekongPhon IPA → Ukrainian adaptation."""
        ipa = self.transcribe_ipa(text)
        return build_result(
            ipa.normalized_input, ipa.raw_ipa,
            model_id=ipa.model_id,
            model_revision=ipa.model_revision,
            tonal=ipa.tonal,
            num_beams=ipa.num_beams,
        )


def transcribe_ipa(
    text: str,
    *,
    tonal: bool = True,
    revision: str | None = None,
    device: str = "auto",
    num_beams: int = 5,
) -> MekongPhonIPAResult:
    """Convenience API for stage 1 only: Lao orthography → typed IPA."""
    return MekongPhonEngine(
        tonal=tonal, revision=revision, device=device, num_beams=num_beams
    ).transcribe_ipa(text)


def transcribe_lao(
    text: str,
    *,
    tonal: bool = True,
    revision: str | None = None,
    device: str = "auto",
    num_beams: int = 5,
) -> MekongPhonResult:
    """Convenience API; no model or neural dependency is loaded until called."""
    return MekongPhonEngine(
        tonal=tonal, revision=revision, device=device, num_beams=num_beams
    ).transcribe(text)
