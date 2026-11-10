# MekongPhon neural G2P integration

**Status: optional inference adapter implemented; rule-based engine remains the default.** MekongPhon rights are recorded as `DONE_VERIFIED (owner-confirmed)` for the authorized project use; independent project IPA gold remains 0.

## Models and upstream contract

ClippyFirst integrates the two Lao checkpoints published by BYU MATRIX Lab:

- [Lao IPA (Tonal)](https://huggingface.co/byumatrixlab/lao-ipa-tonal) — predicts IPA with tone markers.
- [Lao IPA (Non-tonal)](https://huggingface.co/byumatrixlab/lao-ipa-nontonal) — predicts segmental IPA without tone markers.

Both model cards declare Apache-2.0 for the model artifacts and document an EncoderDecoderModel with separate character-level encoder and decoder tokenizers in encoder_tokenizer/ and decoder_tokenizer/. ClippyFirst follows the model-card inference interface and does not vendor the weights or copy the MekongPhon corpus into this repository.

The model cards' Apache-2.0 declaration is treated as the upstream license for the model artifacts as published by BYU MATRIX Lab. It is not a license grant for MekongPhon's training corpus, source lexicon, OPUS components or the upstream MekongPhon repository code. See [the component rights review](../audits/current/MEKONGPHON-DATA-RIGHTS-REVIEW-2026-11-07.md). This implementation uses published model artifacts; it does not download, retain or redistribute training data.

## Installation and use

Install the optional dependency extra:

    pip install -e '.[neural]'

CPU inference:

    lao-ua 'ສະບາຍດີ' --engine mekongphon-tonal --device cpu --json

Non-tonal IPA:

    lao-ua 'ສະບາຍດີ' --engine mekongphon-nontonal --device auto

The Python API exposes the source-side IPA stage independently from Ukrainian adaptation:

```python
from lao_ukrainian import transcribe_ipa, transcribe_lao

ipa = transcribe_ipa("ສະບາຍດີ", device="cpu")
print(ipa.raw_ipa, ipa.phonetic_result, ipa.model_revision)

# Explicitly run both stages: typed IPA → Ukrainian target adapter.
result = transcribe_lao("ສະບາຍດີ", device="cpu")
print(result.raw_ipa, result.ukrainian)
```

MekongPhonEngine.transcribe_ipa() and transcribe_ipa() stop after the typed IPA result. They preserve the untouched decoded string, typed segments, tone metadata, model revision and warnings, and never call the Ukrainian adapter. MekongPhonEngine.transcribe() / transcribe_lao() explicitly run both stages. This API addition does not change the deterministic CLI/API default, and the website remains browser-native deterministic JavaScript.

The adapter defaults to immutable revisions: tonal `e02608cfcb18abfe6b1916f5f4774bfac9ac788d` and non-tonal `d6ea20cb73eaab8f3adc4eb044e61bdb9bef3f5b`. The loaded model config revision is checked against the requested SHA when available. You may explicitly override it with `--revision`; a non-SHA revision is marked `MODEL-REVISION-NOT-IMMUTABLE`. The resolved revision is included in JSON output. First use downloads the model files into the normal Hugging Face cache; no model weights are checked into Git.

The published models accept at most 128 input tokens. ClippyFirst disables truncation and rejects over-limit input rather than silently dropping text. Use an explicit input chunking strategy only when the user intends separate inference units; automatic phrase segmentation is not claimed.

## Pipeline and fail-closed behavior

Lao input → MekongPhon neural model → raw IPA → typed external-IPA adapter → Ukrainian correspondence registry → Ukrainian practical output

- The original decoded string is retained as raw_ipa and phonetic_result.external_ipa.
- The adapter tokenizes only symbols in ClippyFirst's explicit IPA inventory. Unknown phones, brackets and unsupported diacritics make the result IPA_UNSUPPORTED; partial IPA is never mapped to Ukrainian.
- IPA tone letters are preserved as typed tone segments in their original order and in raw_ipa. The aggregate tone_contour_ipa field is diagnostic only; the adapter does not infer per-syllable tone alignment from a flat output string.
- The Ukrainian practical layer currently neutralizes tone. The target adapter therefore excludes only the explicitly typed tone segments while adapting supported segmental IPA; tone data remains inspectable in the typed result and raw output.
- Ukrainian output is generated only through the existing IPA-to-Ukrainian correspondence registry. If the complete predicted segment sequence has no supported mapping, output is withheld as TARGET_MAPPING_UNAVAILABLE.
- Neural output is not written into rule provenance, rule tables, the independent gold corpus or the default analyze() result. It is explicitly labelled MEKONGPHON.
- Inference errors are surfaced; the engine never silently falls back to rules or a different model.

## Evaluation and limitations

The existing 100-entry held-out benchmark is comparative evidence, not independently adjudicated project gold. It showed MekongPhon ahead of ClippyFirst and Lao2IPA on that particular split, but the sample is dictionary-derived and does not establish broad dialect coverage or universal correctness. Independent project IPA gold remains separate and must be annotated/adjudicated independently.

The model card describes the training data as MekongPhon. The repository owner confirms that the project's MekongPhon rights were fully resolved in the prior project conversation. This owner confirmation is not a new independent legal opinion. The 100-word benchmark remains a secondary reference set, not independently adjudicated project gold.

## Tests

The adapter tests are offline and do not download weights. They cover in-word tone-token preservation, unknown-symbol rejection, segmental adaptation with tone retained, model revision provenance and the no-partial-Ukrainian-output contract. Actual model inference remains an opt-in smoke test because it requires PyTorch, Transformers, network access and a model download.


## Hosted verification checkpoint

On commit 2a9a54f4c3961d030e757d9d4e919c6d6f760f46, Verify run [42367579457](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42367579457) reported the repository Python test step SUCCESS, which includes these offline adapter tests. The full workflow remains FAILURE because the browser engine step has the same three previously recorded regressions (modern Lao ຣ context-dependent reading, uncertain IPA withholding and incomplete IPA withholding). Build, generated-data reproducibility and Chromium UI steps were skipped by the workflow dependency. Actual model downloads/inference against the two checkpoints remain unverified.
