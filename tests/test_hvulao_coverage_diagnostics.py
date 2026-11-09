"""HVULao coverage diagnostics must count every withheld syllable, not only failed rows."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "benchmark_hvulao_1k_three_engines.py"
SPEC = importlib.util.spec_from_file_location("hvulao_benchmark", SCRIPT)
BENCHMARK = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(BENCHMARK)


def item(status, ipa_status=None, warnings=(), uncertainty=(), ipa=None):
    result = None if ipa_status is None else SimpleNamespace(
        status=ipa_status, uncertainty=uncertainty, phonemic_ipa=ipa
    )
    return SimpleNamespace(
        status=status, warnings=list(warnings), phonetic_result=result
    )


class TestWithheldIpaDiagnostics(unittest.TestCase):
    def test_counts_all_withheld_syllables_even_when_sentence_has_other_ipa(self):
        statuses, reasons = BENCHMARK.withheld_ipa_diagnostics([
            item("OK", "SUPPORTED", ipa="kaː"),
            item("EVIDENCE LIMITED", "UNSUPPORTED", ["UNCONSUMED_AFTER_VOWEL:ລ"], ["TONE-UNRESOLVED"]),
            item("PARTIAL", "PROVISIONAL", ["SHORT_VOWEL_REQUIRES_CODA:A2"]),
            item("PASSTHROUGH"),
        ])
        self.assertEqual(statuses, {"UNSUPPORTED": 1, "PROVISIONAL": 1})
        self.assertEqual(reasons, {
            "UNCONSUMED_AFTER_VOWEL": 1,
            "TONE-UNRESOLVED": 1,
            "SHORT_VOWEL_REQUIRES_CODA": 1,
        })

    def test_missing_typed_result_has_explicit_reason(self):
        statuses, reasons = BENCHMARK.withheld_ipa_diagnostics([
            item("EVIDENCE LIMITED"),
        ])
        self.assertEqual(statuses, {"MISSING_RESULT": 1})
        self.assertEqual(reasons, {"NO_STRUCTURED_REASON": 1})

    def test_accepted_ipa_and_passthrough_are_not_withheld(self):
        statuses, reasons = BENCHMARK.withheld_ipa_diagnostics([
            item("OK", "SUPPORTED", ipa="kaː"),
            item("PASSTHROUGH"),
        ])
        self.assertEqual(statuses, {})
        self.assertEqual(reasons, {})


if __name__ == "__main__":
    unittest.main()
