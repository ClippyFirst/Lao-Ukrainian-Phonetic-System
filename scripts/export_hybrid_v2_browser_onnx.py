#!/usr/bin/env python3
"""Export the pinned MekongPhon tonal checkpoint into browser-callable ONNX graphs.

The exporter deliberately emits separate encoder and decoder graphs. Decoder
KV-cache export is deferred: this first gate proves tokenizer and greedy-token
parity before a browser beam-search/runtime implementation is attempted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import onnxruntime as ort
import torch
from huggingface_hub import hf_hub_download
from transformers import AutoTokenizer, EncoderDecoderModel

MODEL_ID = "byumatrixlab/lao-ipa-tonal"
MODEL_REVISION = "e02608cfcb18abfe6b1916f5f4774bfac9ac788d"
MODEL_WEIGHT_SHA256 = "5cf6110fdafd9626e96db128ec580b3da705904e1c0478b727c9dc6a14a7b119"
FIXTURES = ("ສະບາຍດີ", "ຂອບໃຈ", "ຂາ")
MAX_SEQUENCE_LENGTH = 128


class EncoderGraph(torch.nn.Module):
    def __init__(self, encoder: torch.nn.Module) -> None:
        super().__init__()
        self.encoder = encoder

    def forward(self, input_ids: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        return self.encoder(
            input_ids=input_ids,
            attention_mask=attention_mask,
            return_dict=False,
        )[0]


class DecoderGraph(torch.nn.Module):
    def __init__(self, decoder: torch.nn.Module) -> None:
        super().__init__()
        self.decoder = decoder

    def forward(
        self,
        decoder_input_ids: torch.Tensor,
        decoder_attention_mask: torch.Tensor,
        encoder_hidden_states: torch.Tensor,
        encoder_attention_mask: torch.Tensor,
    ) -> torch.Tensor:
        return self.decoder(
            input_ids=decoder_input_ids,
            attention_mask=decoder_attention_mask,
            encoder_hidden_states=encoder_hidden_states,
            encoder_attention_mask=encoder_attention_mask,
            use_cache=False,
            return_dict=False,
        )[0]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def greedy_onnx(
    encoder_session: ort.InferenceSession,
    decoder_session: ort.InferenceSession,
    encoder_ids: list[int],
    encoder_mask: list[int],
    *,
    decoder_start_token_id: int,
    eos_token_id: int | None,
    max_length: int,
) -> list[int]:
    ids = torch.tensor([encoder_ids], dtype=torch.long).numpy()
    mask = torch.tensor([encoder_mask], dtype=torch.long).numpy()
    hidden = encoder_session.run(
        ["last_hidden_state"],
        {"input_ids": ids, "attention_mask": mask},
    )[0]
    generated = [decoder_start_token_id]
    for _ in range(max_length - 1):
        decoder_ids = torch.tensor([generated], dtype=torch.long).numpy()
        decoder_mask = decoder_ids * 0 + 1
        logits = decoder_session.run(
            ["logits"],
            {
                "decoder_input_ids": decoder_ids,
                "decoder_attention_mask": decoder_mask,
                "encoder_hidden_states": hidden,
                "encoder_attention_mask": mask,
            },
        )[0]
        next_token = int(logits[0, -1].argmax())
        generated.append(next_token)
        if eos_token_id is not None and next_token == eos_token_id:
            break
    return generated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    weights = Path(hf_hub_download(
        repo_id=MODEL_ID,
        filename="model.safetensors",
        revision=MODEL_REVISION,
    ))
    actual_weight_sha = sha256(weights)
    if actual_weight_sha != MODEL_WEIGHT_SHA256:
        raise SystemExit(
            f"Pinned checkpoint SHA-256 mismatch: expected {MODEL_WEIGHT_SHA256}, "
            f"received {actual_weight_sha}"
        )

    model = EncoderDecoderModel.from_pretrained(
        MODEL_ID,
        revision=MODEL_REVISION,
        trust_remote_code=False,
    ).cpu().eval()
    resolved_revision = getattr(model.config, "_commit_hash", None)
    if resolved_revision != MODEL_REVISION:
        raise SystemExit(
            f"Model revision mismatch: expected {MODEL_REVISION}, got {resolved_revision!r}"
        )

    encoder_tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID, subfolder="encoder_tokenizer", revision=MODEL_REVISION,
        trust_remote_code=False,
    )
    decoder_tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID, subfolder="decoder_tokenizer", revision=MODEL_REVISION,
        trust_remote_code=False,
    )
    encoder_tokenizer.save_pretrained(output / "encoder_tokenizer")
    decoder_tokenizer.save_pretrained(output / "decoder_tokenizer")
    model.config.save_pretrained(output)
    model.generation_config.save_pretrained(output)

    encoder = EncoderGraph(model.encoder).eval()
    decoder = DecoderGraph(model.decoder).eval()
    source = encoder_tokenizer(
        "ສະບາຍດີ", return_tensors="pt", truncation=False, padding=False,
    )
    if source["input_ids"].shape[-1] > MAX_SEQUENCE_LENGTH:
        raise SystemExit("Export fixture exceeds the pinned 128-token model limit")
    with torch.no_grad():
        hidden = encoder(source["input_ids"], source["attention_mask"])
        start_id = model.config.decoder_start_token_id
        if start_id is None:
            raise SystemExit("Model config has no decoder_start_token_id")
        decoder_ids = torch.tensor([[start_id]], dtype=torch.long)
        decoder_mask = torch.ones_like(decoder_ids)
        logits = decoder(
            decoder_ids, decoder_mask, hidden, source["attention_mask"]
        )

    torch.onnx.export(
        encoder,
        (source["input_ids"], source["attention_mask"]),
        output / "encoder.onnx",
        input_names=["input_ids", "attention_mask"],
        output_names=["last_hidden_state"],
        dynamic_axes={
            "input_ids": {0: "batch", 1: "source_sequence"},
            "attention_mask": {0: "batch", 1: "source_sequence"},
            "last_hidden_state": {0: "batch", 1: "source_sequence"},
        },
        opset_version=17,
        dynamo=False,
    )
    torch.onnx.export(
        decoder,
        (decoder_ids, decoder_mask, hidden, source["attention_mask"]),
        output / "decoder.onnx",
        input_names=[
            "decoder_input_ids",
            "decoder_attention_mask",
            "encoder_hidden_states",
            "encoder_attention_mask",
        ],
        output_names=["logits"],
        dynamic_axes={
            "decoder_input_ids": {0: "batch", 1: "target_sequence"},
            "decoder_attention_mask": {0: "batch", 1: "target_sequence"},
            "encoder_hidden_states": {0: "batch", 1: "source_sequence"},
            "encoder_attention_mask": {0: "batch", 1: "source_sequence"},
            "logits": {0: "batch", 1: "target_sequence"},
        },
        opset_version=17,
        dynamo=False,
    )

    encoder_session = ort.InferenceSession(
        str(output / "encoder.onnx"), providers=["CPUExecutionProvider"]
    )
    decoder_session = ort.InferenceSession(
        str(output / "decoder.onnx"), providers=["CPUExecutionProvider"]
    )
    parity_rows = []
    for text in FIXTURES:
        encoded = encoder_tokenizer(
            text, return_tensors="pt", truncation=False, padding=False,
        )
        token_count = int(encoded["input_ids"].shape[-1])
        if token_count > MAX_SEQUENCE_LENGTH:
            raise SystemExit(f"Fixture exceeds model token limit: {text!r}")
        with torch.no_grad():
            expected_ids = model.generate(
                **encoded,
                max_length=MAX_SEQUENCE_LENGTH,
                num_beams=1,
                early_stopping=True,
            )[0].tolist()
        actual_ids = greedy_onnx(
            encoder_session,
            decoder_session,
            encoded["input_ids"][0].tolist(),
            encoded["attention_mask"][0].tolist(),
            decoder_start_token_id=int(model.config.decoder_start_token_id),
            eos_token_id=model.config.eos_token_id,
            max_length=MAX_SEQUENCE_LENGTH,
        )
        expected_text = decoder_tokenizer.decode(expected_ids, skip_special_tokens=True)
        actual_text = decoder_tokenizer.decode(actual_ids, skip_special_tokens=True)
        if actual_ids != expected_ids:
            raise SystemExit(
                f"ONNX token parity failed for {text!r}: "
                f"PyTorch={expected_ids!r}; ONNX={actual_ids!r}"
            )
        parity_rows.append({
            "input": text,
            "token_count": token_count,
            "expected_ids": expected_ids,
            "actual_ids": actual_ids,
            "decoded": actual_text,
            "exact_token_parity": True,
            "exact_text_parity": expected_text == actual_text,
        })

    manifest = {
        "schema_version": "1.0",
        "status": "onnx_greedy_export_parity_verified",
        "model_id": MODEL_ID,
        "model_revision": MODEL_REVISION,
        "model_weight_sha256": actual_weight_sha,
        "architecture": "BERT encoder-decoder",
        "max_sequence_length": MAX_SEQUENCE_LENGTH,
        "decoder_cache": False,
        "generation_parity": "greedy only; browser beam search not implemented",
        "onnx_opset": 17,
        "torch_version": torch.__version__,
        "onnxruntime_version": ort.__version__,
        "decoder_start_token_id": model.config.decoder_start_token_id,
        "eos_token_id": model.config.eos_token_id,
        "pad_token_id": model.config.pad_token_id,
        "encoder_tokenizer_class": type(encoder_tokenizer).__name__,
        "decoder_tokenizer_class": type(decoder_tokenizer).__name__,
        "encoder_onnx_bytes": (output / "encoder.onnx").stat().st_size,
        "decoder_onnx_bytes": (output / "decoder.onnx").stat().st_size,
        "parity_fixtures": parity_rows,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
