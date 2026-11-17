import unittest

from lao_ukrainian.orthographic_lattice import (
    _build_candidate_lattice,
    analyze_orthographic_word,
)


class CandidateLatticeGraphTests(unittest.TestCase):
    @staticmethod
    def parser_for(valid_spans):
        def parse(surface, _registry):
            return {
                "vowel": {"id": "TEST"} if surface in valid_spans else None,
                "warnings": [],
                "onset": None,
                "coda": None,
            }
        return parse

    def test_dead_candidate_is_pruned_when_it_cannot_reach_word_end(self):
        result = _build_candidate_lattice(
            "abc", self.parser_for({"a", "ab", "bc"}), {}
        )
        self.assertEqual(result["status"], "UNIQUE")
        self.assertEqual(result["complete_path_count_capped"], 1)
        self.assertEqual(
            [edge["surface"] for edge in result["unique_path"]], ["a", "bc"]
        )
        self.assertEqual(
            [edge["surface"] for edge in result["dead_candidates"]], ["ab"]
        )
        self.assertEqual(result["convergence_offsets"], [0, 1, 3])
        self.assertEqual(result["ambiguity_eyes"], [])

    def test_multiple_complete_paths_are_preserved_as_ambiguous(self):
        result = _build_candidate_lattice(
            "abc", self.parser_for({"a", "ab", "b", "bc", "c"}), {}
        )
        self.assertEqual(result["status"], "AMBIGUOUS")
        self.assertEqual(result["complete_path_count_capped"], 2)
        self.assertIsNone(result["unique_path"])
        self.assertEqual(result["dead_candidate_count"], 0)
        self.assertEqual(result["convergence_offsets"], [0, 3])
        self.assertEqual(len(result["ambiguity_eyes"]), 1)
        self.assertEqual(result["ambiguity_eyes"][0]["surface"], "abc")
        self.assertEqual(
            result["ambiguity_eyes"][0]["complete_path_count_capped"], 2
        )

    def test_unsegmentable_word_has_no_complete_path(self):
        result = _build_candidate_lattice(
            "abc", self.parser_for({"ab"}), {}
        )
        self.assertEqual(result["status"], "NO_COMPLETE_PATH")
        self.assertEqual(result["complete_path_count_capped"], 0)
        self.assertIsNone(result["unique_path"])

    def test_two_ambiguity_regions_are_separated_by_a_convergence_point(self):
        # The first and last two-character regions are ambiguous; offset 2
        # is traversed by every complete path and separates the two eyes.
        result = _build_candidate_lattice(
            "abcd", self.parser_for({"a", "ab", "b", "c", "cd", "d"}), {}
        )
        self.assertEqual(result["convergence_offsets"], [0, 2, 4])
        self.assertEqual(
            [eye["surface"] for eye in result["ambiguity_eyes"]], ["ab", "cd"]
        )

    def test_path_count_is_saturated_at_two(self):
        # Three possible paths exist: a+bc, ab+c, and a+b+c.
        result = _build_candidate_lattice(
            "abc", self.parser_for({"a", "ab", "b", "bc", "c"}), {}
        )
        self.assertEqual(result["complete_path_count_capped"], 2)


class LaoCandidateLatticeTests(unittest.TestCase):
    def test_known_multisyllable_word_has_a_complete_candidate_path(self):
        result = analyze_orthographic_word("ສະບາຍດີ")
        self.assertIn(result["status"], {"UNIQUE", "AMBIGUOUS"})
        self.assertGreater(result["live_candidate_count"], 0)

    def test_exact_loc_note10_word_remains_unresolved(self):
        result = analyze_orthographic_word("ຄຼິສຕຽນ")
        self.assertEqual(result["status"], "NO_COMPLETE_PATH")
        self.assertIsNone(result["unique_path"])

    def test_one_token_contract_rejects_whitespace(self):
        with self.assertRaisesRegex(ValueError, "one whitespace-delimited token"):
            analyze_orthographic_word("ສະ ບາຍ")

    def test_offsets_require_nfc_input(self):
        with self.assertRaisesRegex(ValueError, "NFC-normalized"):
            analyze_orthographic_word("e\u0301")


if __name__ == "__main__":
    unittest.main()
