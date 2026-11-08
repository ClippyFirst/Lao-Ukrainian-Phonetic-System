"""Deterministic, evidence-aware rule selection for the hybrid Lao IPA engine.

Rules are compositional transformations over parsed phonological context.
The selector never uses input order as a tie-break between conflicting outputs.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


class RuleConflictError(ValueError):
    """Raised when equally specific, equally prioritized rules disagree."""


@dataclass(frozen=True)
class RuleMatch:
    rule_id: str
    target: str
    value: str
    priority: int
    specificity: int
    provenance: str
    evidence_count: int | None = None


def _condition_matches(expected: Any, actual: Any) -> bool:
    if isinstance(expected, (tuple, list, set, frozenset)):
        return actual in expected
    return actual == expected


def select_rule(
    rules: Sequence[Mapping[str, Any]],
    context: Mapping[str, Any],
    *,
    target: str,
) -> RuleMatch | None:
    """Select the most specific applicable rule, failing on a real conflict.

    Priority is the primary ordering key and condition specificity the
    secondary key. Rule declaration order is deliberately irrelevant.
    """
    matches = []
    for rule in rules:
        if rule.get("target") != target:
            continue
        conditions = rule.get("conditions", {})
        if all(_condition_matches(expected, context.get(key)) for key, expected in conditions.items()):
            matches.append((rule, len(conditions)))

    if not matches:
        return None

    best_rank = max((int(rule.get("priority", 0)), specificity) for rule, specificity in matches)
    best = [
        (rule, specificity)
        for rule, specificity in matches
        if (int(rule.get("priority", 0)), specificity) == best_rank
    ]
    outputs = {str(rule["value"]) for rule, _ in best}
    if len(outputs) > 1:
        ids = sorted(str(rule.get("rule_id", "<unnamed>")) for rule, _ in best)
        raise RuleConflictError(
            f"Conflicting {target} rules at priority/specificity {best_rank}: {', '.join(ids)}"
        )

    rule, specificity = min(best, key=lambda item: str(item[0].get("rule_id", "")))
    return RuleMatch(
        rule_id=str(rule["rule_id"]),
        target=target,
        value=str(rule["value"]),
        priority=int(rule.get("priority", 0)),
        specificity=specificity,
        provenance=str(rule.get("provenance", rule["rule_id"])),
        evidence_count=rule.get("evidence_count"),
    )


def phonological_context(parsed: Mapping[str, Any]) -> dict[str, Any]:
    """Expose only features already established by the structural parser."""
    vowel = parsed.get("vowel") or {}
    return {
        "onset": parsed.get("onset"),
        "onset_class": parsed.get("onset_class"),
        "vowel_id": vowel.get("id"),
        "vowel_length": vowel.get("length"),
        "nucleus_type": vowel.get("nucleus_type"),
        "coda": parsed.get("coda"),
        "tone_mark": parsed.get("tone_mark"),
    }
