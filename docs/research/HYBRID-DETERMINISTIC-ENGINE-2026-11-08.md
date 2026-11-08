# Hybrid deterministic Lao IPA engine — 2026-11-08

## Scope and status

This continuation adds a third, explicitly selected deterministic profile:

`hybrid-deterministic`

It does not replace the Vientiane default, change the neural CLI default, merge existing PRs, or make any linguistic-accuracy claim. The profile combines the Vientiane rule engine as the base phonological analysis with the existing MekongPhon-reference aggregate correspondences through a deterministic rule selector.

## Execution design

Pipeline remains:

`Lao orthography → structural syllable parser → Vientiane phonological baseline → evidence-scoped hybrid rule selection → typed IPA → Ukrainian adapter`

The selector:
- evaluates parsed onset, onset class, vowel ID/length, coda and tone-mark context;
- ranks applicable rules by explicit priority and then condition specificity;
- does not depend on declaration order;
- raises a conflict error if equally ranked applicable rules disagree;
- preserves baseline IPA when no evidence-backed rule matches;
- records both the legacy profile provenance and a stable `HYBRID-RULE:<rule_id>` trace.

The Python selector is in `src/lao_ukrainian/hybrid_rules.py`; the profile rule registry and adapter are in `src/lao_ukrainian/mekongphon_reference_profile.py`. The browser implementation has the same profile contract and matching behavior in `web/engine.js`.

## Evidence boundary

The first hybrid rule set deliberately reuses only the nine vowel-structure and two onset correspondences already transferred from the pinned MekongPhon training split (6,219 rows). It does not introduce new IPA values or claim new contextual exceptions. Current evidence supports aggregate correspondences, but does not yet justify narrowing each one to a specific onset/coda/tone environment. The selector supports richer conditions so that later rules can be added only when the context counts and provenance are available.

`mekongphon-reference` remains available as a compatibility profile. `vientiane` remains the default. The new `hybrid-deterministic` profile is opt-in in the Python API, CLI and browser engine API. No neural dependency or fallback is added.

## Verification added

- Python regression coverage for baseline preservation, hybrid output/provenance, unchanged tone, CLI selection, rule specificity independent of declaration order, and equal-rank conflict rejection.
- Browser regression coverage for output/provenance parity, Vientiane fallthrough, uncertain /r/ status and invalid-profile rejection.
- The 100-entry held-out MekongPhon benchmark and HVULao 1k sentence stress benchmark now include the hybrid profile as a separate engine.
- Benchmarks remain reference-relative or coverage/runtime stress only. They do not establish independent phonetic accuracy.

## Remaining work

1. Run exact-head Python, Node, Chromium, data-audit, clean-install and build gates; fix any failures and rerun.
2. Run both frozen benchmarks with the hybrid engine and compare exact outputs, coverage, rejection counts and latency.
3. Add context-conditioned IPA rules only from inspectable aggregate evidence with separate training/evaluation splits and explicit support thresholds; do not promote a rule from count alone.
4. Investigate the 399 structurally withheld MekongPhon train rows and HVULao unresolved syllables using primary orthographic/phonological evidence. Keep ambiguous forms withheld.
5. Add independently adjudicated Vientiane IPA gold before claiming Neural-level phonetic accuracy. Current independent gold remains 0.

## Readiness

**PARTIAL / engineering implementation under verification.** This branch is not release-ready. Existing Vientiane and MekongPhon-reference profiles are preserved, and the production default remains unchanged.


## First hosted held-out result

The updated MekongPhon 100-entry workflow completed successfully on branch checkpoint `4afd51964532dd1f95b57eaeac36aea852b85228`:

- Run [42507131648](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42507131648), artifact [13628190784](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42507131648/artifacts/13628190784), SHA-256 `7de8665161308fcaaa422c5c3534e181916c1958f59e88786c3521215d7f8c86d`.
- Dataset: pinned 100-row `lao_eval.csv`, reference `pron_no_tones`; neural comparator is the pinned non-tonal checkpoint.

| Engine | Exact / 100 | CER / 100 | Coverage | Mean latency |
|---|---:|---:|---:|---:|
| Vientiane rules | 69 | 11.46% | 97% | 1.79 ms |
| MekongPhon-reference | 90 | 6.64% | 97% | 1.40 ms |
| Hybrid deterministic | **90** | **6.64%** | 97% | **1.41 ms** |
| MekongPhon Neural | 82 | 6.64% | 100% | 60.51 ms |

On the identical 97-word coverage subset, hybrid and MekongPhon-reference each achieved 90/97 exact matches and CER 1.40%; Neural achieved 81/97 and CER 5.79%. Hybrid runtime errors: 0. The three withheld cases and warning categories are unchanged.

This establishes that the new selector preserves the earlier profile's measured output on this held-out set and adds negligible overhead. It does **not** show that new contextual generalization has been learned: the hybrid intentionally uses the same eleven mappings, and the reference is dictionary-seeded, non-tonal and not independently adjudicated gold. Hybrid coverage remains 3 percentage points below Neural on this test.


## Exact-head engineering verification and 1k stress result — 2026-11-08

Final implementation checkpoint before this documentation update: `c705cf8ad782246c2d72c0d789a5e44e5196eca6`.

- Exact-head Verify [#42508759262 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42508759262): 280 Python tests, 134 Node tests and 17 Chromium tests passed. Corpus validation, evidence/data audit, optional external-G2P CLI checks, clean locked browser dependency install, browser build, generated-data reproducibility and built-site checks passed.
- Exact-head HVULao 1k benchmark [#42508759241 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42508759241), artifact [13628229661](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42508759241/artifacts/13628229661), SHA-256 `145966638988265a8f255163288e48de4fa8a0293941f0ec26643c7211fe7149`.
- Vientiane, MekongPhon-reference and hybrid each completed 669/1,000 sentences (66.9%), with 97.85% IPA construction across Lao syllables and zero runtime errors.
- Hybrid all-attempt latency: mean 16.28 ms, median 15.31 ms, p95 30.32 ms. Neural completed 930/1,000 (93.0%) with all-attempt mean 375.98 ms and p95 725.19 ms.
- The updated explicit passthrough policy preserves common ASCII and observed punctuation unchanged and excludes those units from IPA-coverage denominators. This improves mixed-text acceptance; it does not assign IPA to punctuation or explain the remaining 331 incomplete rows.
- The hybrid selector still does not increase structural coverage over the Vientiane baseline. It provides a deterministic route to the same 100-entry held-out reference-relative result previously recorded above, but no independent gold or tonal validation exists.

### Current conclusion

**Engineering implementation is verified; Neural-level coverage and linguistic accuracy are not achieved.** The next legitimate implementation work is to resolve parser-withheld orthographic structures using primary Lao orthography/phonology evidence and independent regression examples. The documented warning families remain fail-closed; do not lower parser safeguards or add exceptions solely to increase the 66.9% score.
