# Laonetics same-set research benchmark — 2026-11-10

## Result

Laonetics 0.4.3 was evaluated on the exact pinned 100-entry MekongPhon Lao held-out lexicon used by the repository's current comparison benchmark.

| Metric | Laonetics |
|---|---:|
| Segmental exact matches | 47/100 |
| Segmental CER | 13.95% |
| Output coverage | 100/100 |
| Tonal score | Not available |

- Workflow: [#42828308429 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42828205219)
- Artifact: [laonetics-mekongphon-100](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42828205219/artifacts/13768874616)
- Branch: `benchmark/laonetics-same-set-20261110`
- Benchmark commit: `bf7402b75b0bef4f98c1c19d0444ec28fca7b5ab`
- Dataset revision: `f80f6c1840c4818b51e05f2e00cded4701a5b662`
- Dataset SHA-256: `5351af5ed545f68886a99f0e8d88c91fdbdf46c4df885d40e166b8a3b32cd241`

## Comparison and interpretation

The latest same-set schema 8.0 benchmark reports ClippyFirst Hybrid v2 at 90/100 exact and 6.15% segmental CER, MekongPhon Neural at 82/100 and 6.64%, Lao2IPA at 68/100 and 8.97%, and Epitran at 71/100 and 10.96%. Laonetics is therefore behind all four on segmental reference concordance, although its output coverage is complete.

Laonetics is an older rule-based karaoke/romanization package. Its `ph` output is described by the upstream project as IPA phonetics, but this probe treats it conservatively as IPA-like segmental output; no tonal evaluation is available. The result is reference concordance, not independently adjudicated pronunciation accuracy. The repository's independent expert-adjudicated Lao IPA gold remains 0.

## Provenance and licensing

- Upstream: https://github.com/ltruchot/laonetics
- Package: `laonetics@0.4.3`
- Upstream commit: `eeab0c4ead4c1f67599573eb9e5cba56506260e3`
- License declared by upstream: CC-BY-NC-4.0
- The package source is old and the repository's last upstream push is from 2017. The package is unsuitable for commercial redistribution/use without separate rights. It was installed only ephemerally in CI; neither its code nor weights were imported into the product.

## Task ledger

| Item | Status | Evidence |
|---|---|---|
| Pin upstream package and source revision | DONE_VERIFIED | npm package 0.4.3 and upstream commit recorded |
| Run same 100-word segmental benchmark | DONE_VERIFIED | Workflow #42828205219 SUCCESS; aggregate artifact uploaded |
| Score tone | DEFERRED | Candidate emits no separate tonal lane |
| Promote to production | DEFERRED | Lower segmental concordance than Hybrid v2 and restrictive non-commercial license |
| Independent accuracy validation | BLOCKED | Independent adjudicated gold remains 0 |

No production engine, website, default profile, or licensed data was changed.
