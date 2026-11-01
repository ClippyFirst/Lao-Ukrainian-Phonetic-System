# Goruut language-asset provenance and license gate — 2026-11-01

## Decision

**Status: BLOCKED for benchmark execution until language-asset licensing is clarified; research-only comparator, not production-approved.** The upstream code license is not sufficient to clear the phonetic lexicon and trained model assets.

## Verified upstream facts

- Goruut source repository: https://github.com/neurlang/goruut
- Inspected source commit: `b224bde02151f8f86d0fe260804e4ca743bda620`.
- The pinned source tree contains language-specific embedded model/configuration files for **Lao** under `dicts/lao/`. The source tree also registers this language in `dicts/dicts.go`; for Khmer, the registered display identifier is `Khmer Central`.
- Goruut's own `dicts/README.md` describes `lexicon.tsv` as word-to-IPA training data and explains that language grammar/model files (including `weights*.zlib`) are produced from that data and embedded in the Go package.
- The separate upstream lexicon repository is https://github.com/neurlang/dataset. Its inspected default-branch tree was `3bd40eeb2f9149a91393fcbaf5e5d8980e794397` (2026-09-24). The corresponding lexicon directory is `lao/`.
- The dataset repository API reports `license: null`, and its root tree has no LICENSE/COPYING file. Its README describes several licenses for selected subsets, but does not assign a license or provenance statement to the Lao directory. The README therefore does **not** establish a usable license for this language's lexicon or the derived Goruut model.
- Goruut's source repository has an MIT LICENSE. That covers the source-code repository as stated there; it does not, by itself, establish the rights to third-party lexicon content or derived trained model weights.

## Consequence

Do not vendor the language lexicon/model, publish raw derived benchmark artifacts, enable Goruut in production, or claim it is a verified comparator on the strength of the MIT source license. Even a successful local execution would establish only that the software runs, not that the data are licensed for this project's intended use or that its output is linguistically accurate.

## Acceptance criteria to unblock

1. Obtain a written per-language license/provenance statement from the dataset maintainer or identify the original upstream sources and verify their applicable licenses.
2. Establish whether the derived `dicts/lao/` model files are covered by the same permissions, and whether the project may download, execute, cache, and retain benchmark outputs.
3. Record an owner-approved usage decision if terms are non-commercial, share-alike, attribution-bound, or otherwise conditional.
4. Only then run the pinned Goruut commit in an isolated optional job; retain version, language identifier, raw output, errors, input hash and artifact digest.
5. Keep the candidate out of the production IPA→Ukrainian path until independent expert-adjudicated gold and phonological review are available.

## Evidence links

- Pinned source tree: https://github.com/neurlang/goruut/tree/b224bde02151f8f86d0fe260804e4ca743bda620/dicts
- Language registration: https://github.com/neurlang/goruut/blob/b224bde02151f8f86d0fe260804e4ca743bda620/dicts/dicts.go
- Goruut data/model preparation instructions: https://github.com/neurlang/goruut/blob/b224bde02151f8f86d0fe260804e4ca743bda620/dicts/README.md
- Dataset lexicon directory: https://github.com/neurlang/dataset/tree/master/lao
- Dataset README and partial licensing notes: https://github.com/neurlang/dataset/blob/master/README.md
- Dataset repository metadata (no declared repository license): https://api.github.com/repos/neurlang/dataset

No runtime execution, pronunciation validation, or accuracy measurement is claimed by this audit.
