# MekongPhon neural G2P integration

**Status: optional inference adapter implemented; rule-based engine remains the default.**

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

For reproducible experiments, pass a 40-character Hugging Face model commit SHA with --revision. Without it, Hugging Face's default revision is used and the result includes MODEL-REVISION-NOT-IMMUTABLE. The actual resolved revision is included in JSON output whenever the Transformers model config exposes it. First use downloads the model files into the normal Hugging Face cache; no model weights are checked into Git.

The published models accept at most 128 input tokens. ClippyFirst disables truncation and rejects over-limit input rather than silently dropping text. Use an explicit input chunking strategy only when the user intends separate inference units; automatic phrase segmentation is not claimed.

## Pipeline and fail-closed behavior

Lao input → MekongPhon neural model → raw IPA → typed external-IPA adapter → Ukrainian correspondence registry → Ukrainian practical output

- The original decoded string is retained as raw_ipa and phonetic_result.external_ipa.
- The adapter tokenizes only symbols in ClippyFirst's explicit IPA inventory. Unknown symbols, internal tone marks, brackets and unsupported diacritics make the result IPA_UNSUPPORTED; partial IPA is never mapped to Ukrainian.
- A terminal sequence of IPA tone letters is retained separately as tone_contour_ipa. No tone category is inferred from the neural output, and Ukrainian adaptation does not currently encode tone.
- Ukrainian output is generated only through the existing IPA-to-Ukrainian correspondence registry. If the complete predicted segment sequence has no supported mapping, output is withheld as TARGET_MAPPING_UNAVAILABLE.
- Neural output is not written into rule provenance, rule tables, the independent gold corpus or the default analyze() result. It is explicitly labelled MEKONGPHON.
- Inference errors are surfaced; the engine never silently falls back to rules or a different model.

## Evaluation and limitations

The existing 100-entry held-out benchmark is comparative evidence, not independently adjudicated project gold. It showed MekongPhon ahead of ClippyFirst and Lao2IPA on that particular split, but the sample is dictionary-derived and does not establish broad dialect coverage or universal correctness. Independent project IPA gold remains separate and must be annotated/adjudicated independently.

The model card describes the training data as MekongPhon. The dataset's component-level rights and exact Creative Commons grant remain unresolved. This code integrates the separately published model artifacts under their model-card declaration; it does not claim blanket permission to reuse, redistribute, retrain on or publish the underlying corpus.

## Tests

The adapter tests are offline and do not download weights. They cover terminal tone preservation, unknown-symbol rejection, internal tone fail-closed behavior, model revision provenance and the no-partial-Ukrainian-output contract. Actual model inference remains an opt-in smoke test because it requires PyTorch, Transformers, network access and a model download.
