import unittest
from types import SimpleNamespace

from scripts.benchmark_ipa_contract import accepted_phonetic_ipa


class BenchmarkIpaConfidenceGateTests(unittest.TestCase):
    def test_supported_ipa_is_eligible(self):
        self.assertTrue(accepted_phonetic_ipa(SimpleNamespace(status="SUPPORTED", phonemic_ipa="kʰaː")))

    def test_uncertain_but_explicit_ipa_is_eligible(self):
        self.assertTrue(accepted_phonetic_ipa(SimpleNamespace(status="UNCERTAIN", phonemic_ipa="kʰaː")))

    def test_provisional_hint_is_never_scored_as_ipa(self):
        self.assertFalse(accepted_phonetic_ipa(SimpleNamespace(status="PROVISIONAL", phonemic_ipa="kʰaː")))

    def test_unsupported_or_missing_ipa_is_not_eligible(self):
        self.assertFalse(accepted_phonetic_ipa(SimpleNamespace(status="UNSUPPORTED", phonemic_ipa=None)))
        self.assertFalse(accepted_phonetic_ipa(SimpleNamespace(status="SUPPORTED", phonemic_ipa=None)))
        self.assertFalse(accepted_phonetic_ipa(None))


if __name__ == "__main__":
    unittest.main()
