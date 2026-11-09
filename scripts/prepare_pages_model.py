#!/usr/bin/env python3
"""Prepare the minimal, evidence-gated static model payload for GitHub Pages."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    destination = args.destination.resolve()
    export_manifest = json.loads((source / "manifest.json").read_text(encoding="utf-8"))
    runtime_report = json.loads(
        (source / "browser-runtime-parity.json").read_text(encoding="utf-8")
    )

    if export_manifest.get("model_id") != "byumatrixlab/lao-ipa-tonal":
        raise SystemExit("Unexpected model id; refusing to publish model assets")
    if export_manifest.get("model_revision") != "e02608cfcb18abfe6b1916f5f4774bfac9ac788d":
        raise SystemExit("Unexpected model revision; refusing to publish model assets")
    if not export_manifest.get("int8_exact_token_parity"):
        raise SystemExit("INT8 Python parity is not exact; refusing to publish quantized weights")
    if runtime_report.get("status") != "TRANSFORMERS_JS_TOKENIZER_AND_ONNX_RUNTIME_WEB_WASM_BEAM5_PARITY_VERIFIED":
        raise SystemExit("Browser WASM beam-five parity is not verified")
    if runtime_report.get("modelRevision") != export_manifest["model_revision"]:
        raise SystemExit("Browser parity report model revision does not match the export")
    if runtime_report.get("beamSize") != 5 or runtime_report.get("fixtures") < 3:
        raise SystemExit("Browser parity evidence does not meet the minimum fixture gate")

    files = {
        "encoder.int8.onnx": export_manifest["int8_encoder_onnx_sha256"],
        "decoder.int8.onnx": export_manifest["int8_decoder_onnx_sha256"],
    }
    for filename, expected_hash in files.items():
        path = source / filename
        if not path.is_file() or sha256(path) != expected_hash:
            raise SystemExit(f"Missing or corrupt model asset: {filename}")

    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    for filename in files:
        shutil.copy2(source / filename, destination / filename)
    for directory in ("encoder_tokenizer", "decoder_tokenizer"):
        shutil.copytree(source / directory, destination / directory)
    for filename in ("config.json", "generation_config.json"):
        if (source / filename).is_file():
            shutil.copy2(source / filename, destination / filename)
    shutil.copy2(source / "browser-runtime-parity.json", destination / "browser-runtime-parity.json")

    manifest = {
        "schema_version": "1.0",
        "model_id": export_manifest["model_id"],
        "model_revision": export_manifest["model_revision"],
        "model_weight_sha256": export_manifest["model_weight_sha256"],
        "architecture": export_manifest["architecture"],
        "license": "apache-2.0",
        "model_card_url": "https://huggingface.co/byumatrixlab/lao-ipa-tonal",
        "max_sequence_length": export_manifest["max_sequence_length"],
        "decoder_start_token_id": export_manifest["decoder_start_token_id"],
        "eos_token_id": export_manifest["eos_token_id"],
        "pad_token_id": export_manifest["pad_token_id"],
        "num_beams": 5,
        "length_penalty": 1.0,
        "early_stopping": True,
        "inference": "browser-local ONNX Runtime Web WASM; no network inference",
        "quantization": {
            "method": "ONNX Runtime dynamic per-channel INT8",
            "weight_type": "QInt8",
            "per_channel": True,
            "op_types": ["MatMul", "Gemm"],
            "exact_python_token_parity": export_manifest["int8_exact_token_parity"],
            "files": {
                filename: {
                    "bytes": (destination / filename).stat().st_size,
                    "sha256": sha256(destination / filename),
                }
                for filename in files
            },
        },
        "tokenizers": {
            "encoder_class": export_manifest["encoder_tokenizer_class"],
            "decoder_class": export_manifest["decoder_tokenizer_class"],
            "directories": ["encoder_tokenizer", "decoder_tokenizer"],
        },
        "browser_runtime_parity": runtime_report,
    }
    (destination / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    total_bytes = sum(path.stat().st_size for path in destination.rglob("*") if path.is_file())
    print(json.dumps({
        "status": "PAGES_MODEL_ASSETS_PREPARED",
        "destination": str(destination),
        "total_bytes": total_bytes,
        "files": manifest["quantization"]["files"],
        "model_revision": manifest["model_revision"],
        "browser_parity": runtime_report["status"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
