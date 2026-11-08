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
