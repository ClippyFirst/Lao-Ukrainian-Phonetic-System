import unittest
from unittest.mock import patch

import lao_ukrainian.core as core_module
from lao_ukrainian import analyze as _analyze

# Existing linguistic matrix tests pin the Vientiane baseline explicitly.
def analyze(text, *, ipa_profile="vientiane"):
    return _analyze(text, ipa_profile=ipa_profile)


class TestCore(unittest.TestCase):
    def test_analysis_loads_registry_once_for_full_pipeline(self):
        real_loader = core_module.load_registry
        with (
            patch("lao_ukrainian.core.load_registry", wraps=real_loader) as load_once,
            patch("lao_ukrainian.parser.load_registry", side_effect=AssertionError("parser reloaded registry")),
            patch("lao_ukrainian.phonology.load_registry", side_effect=AssertionError("phonology reloaded registry")),
            patch("lao_ukrainian.target.load_registry", side_effect=AssertionError("target adapter reloaded registry")),
        ):
            result = core_module.analyze("ຂາຄາ")
        self.assertEqual(len(result.syllables), 2)
        self.assertEqual(load_once.call_count, 1)

    def test_default_profile_is_hybrid_while_vientiane_remains_explicit(self):
        default = core_module.analyze("ວາ").syllables[0]
        vientiane = analyze("ວາ", ipa_profile="vientiane").syllables[0]
        self.assertEqual(default.phonemic_ipa, "waː")
        self.assertEqual(vientiane.phonemic_ipa, "ʋaː")
        self.assertIn("HYBRID-RULE:HYB-MPH-ONSET-ວ", default.rules)
        self.assertNotIn("HYBRID-RULE:HYB-MPH-ONSET-ວ", vientiane.rules)
        parsed = core_module.parse_syllable("ວາ")
        self.assertEqual(core_module.phonologize(parsed)[0], "waː")
        self.assertEqual(core_module.phonologize(parsed, ipa_profile="vientiane")[0], "ʋaː")

    def test_long_open_high_class(self):
        s = analyze("ຂາ").syllables[0]
        self.assertEqual(s.phonemic_ipa, "kʰaː")
        self.assertEqual(s.practical_ukrainian, "к\u0027а")
        self.assertEqual(s.tone, "low-rising")

    def test_tone_contour_is_preserved_from_the_matched_rule(self):
        rising = analyze("ຂາ").syllables[0]
        mid = analyze("ກ່າ").syllables[0]
        self.assertEqual(rising.tone, "low-rising")
        self.assertEqual(rising.tone_contour, "˨˦")
        self.assertEqual(mid.tone, "high-mid")
        self.assertEqual(mid.tone_contour, "˧")

    def test_middle_class_inherent_tone(self):
        self.assertEqual(analyze("ກາ").syllables[0].tone, "low-rising")

    def test_low_class_inherent_tone(self):
        self.assertEqual(analyze("ຄາ").syllables[0].tone, "high-rising")

    def test_tone_mark_matrix(self):
        self.assertEqual(analyze("ກ່າ").syllables[0].tone, "high-mid")
        self.assertEqual(analyze("ກ້າ").syllables[0].tone, "high-falling")
        self.assertEqual(analyze("ຄ້າ").syllables[0].tone, "high-falling")

    def test_tone_matrix_cross_checks_live_and_dead_rhymes(self):
        # Independent Vientiane chart: high-class live unmarked syllables
        # remain low-rising even with a short vowel plus sonorant coda.
        self.assertEqual(analyze("ຂົງ").syllables[0].tone, "low-rising")
        self.assertEqual(analyze("ຂູງ").syllables[0].tone, "low-rising")

        # Low-class short open/dead syllables and live mai-ek syllables
        # are high-mid; do not retune these from conflicting dictionary rows.
        self.assertEqual(analyze("ຄະ").syllables[0].tone, "high-mid")
        self.assertEqual(analyze("ຄີ່").syllables[0].tone, "high-mid")

    def test_initial_open_short_a_potential_minor_syllable_withholds_tone(self):
        result = analyze("ຄະຄາ")
        first, second = result.syllables
        self.assertEqual(first.phonemic_ipa, "kʰa")
        self.assertEqual(first.phonetic_result.status, "SUPPORTED")
        self.assertEqual(first.practical_ukrainian, "к'а")
        self.assertIsNone(first.tone)
        self.assertIsNone(first.tone_contour)
        self.assertIsNone(first.phonetic_result.tone_category)
        self.assertEqual(first.status, "analysis-dependent")
        self.assertIn("VNT-POTENTIAL-MINOR-OPEN-A-UNRESOLVED", first.rules)
        self.assertIn("VNT-POTENTIAL-MINOR-OPEN-A-UNRESOLVED", first.phonetic_result.provenance)
        self.assertNotIn("VNT-L-DEAD-SHORT-NONE", first.phonetic_result.provenance)
        self.assertEqual(second.tone, "high-rising")

    def test_monosyllabic_open_short_a_keeps_its_lexical_tone(self):
        self.assertEqual(analyze("ຄະ").syllables[0].tone, "high-mid")

    def test_initial_open_short_a_without_major_weight_does_not_trigger_minor_candidate(self):
        result = analyze("ຄະຄະ")
        self.assertEqual(len(result.syllables), 2)
        self.assertEqual(result.syllables[0].tone, "high-mid")

    def test_potential_minor_selector_does_not_cross_explicit_space(self):
        result = analyze("ຄະ ຄາ")
        self.assertEqual(len(result.syllables), 2)
        self.assertEqual(result.syllables[0].tone, "high-mid")
        self.assertNotIn(
            "VNT-POTENTIAL-MINOR-OPEN-A-UNRESOLVED",
            result.syllables[0].rules,
        )

    def test_zero_width_space_is_rejected_before_minor_selector(self):
        result = analyze("ຄະ\u200bຄາ")
        self.assertEqual(result.status, "INVALID")
        self.assertEqual(result.syllables, [])

    def test_potential_minor_selector_does_not_override_uncertain_onset(self):
        result = analyze("ຣະຄາ")
        first = result.syllables[0]
        self.assertEqual(first.phonetic_result.status, "UNCERTAIN")
        self.assertNotIn(
            "VNT-POTENTIAL-MINOR-OPEN-A-UNRESOLVED",
            first.rules,
        )

    def test_low_class_ng(self):
        s = analyze("ງາ").syllables[0]
        self.assertEqual(s.phonemic_ipa, "ŋaː")
        self.assertEqual(s.practical_ukrainian, "нга")
        self.assertEqual(s.tone, "high-rising")

    def test_palatal_affricate(self):
        s = analyze("ຈາ").syllables[0]
        self.assertEqual(s.phonemic_ipa, "t͡ɕaː")
        self.assertEqual(s.practical_ukrainian, "ча")

    def test_checked_coda(self):
        s = analyze("ກັບ").syllables[0]
        self.assertEqual(s.phonemic_ipa, "kap")
        self.assertEqual(s.practical_ukrainian, "кап")
        self.assertEqual(s.syllable_type, "dead")
        self.assertEqual(s.tone, "high-rising")

    def test_closed_uo_spelling(self):
        s = analyze("ດວງ").syllables[0]
        self.assertEqual(s.phonemic_ipa, "duːəŋ")
        self.assertEqual(s.practical_ukrainian, "дуанг")

    def test_open_uo_spelling(self):
        s = analyze("ດວາງ").syllables[0]
        self.assertEqual(s.phonemic_ipa, "duːəŋ")
        self.assertEqual(s.practical_ukrainian, "дуанг")

    def test_medial_o_vowel(self):
        s = analyze("ຈອກ").syllables[0]
        self.assertEqual(s.phonemic_ipa, "t͡ɕɔːk")
        self.assertEqual(s.practical_ukrainian, "чок")

    def test_ti_and_catawa_marks(self):
        self.assertEqual(analyze("ກ໊າ").syllables[0].tone, "high-falling")
        self.assertEqual(analyze("ກ໋າ").syllables[0].tone, "low-rising")

    def test_multiple_tone_marks_withhold_ipa_and_ukrainian_output(self):
        result = analyze("ກ່້າ")
        s = result.syllables[0]
        self.assertEqual(s.status, "EVIDENCE LIMITED")
        self.assertIsNone(s.phonemic_ipa)
        self.assertIsNone(s.practical_ukrainian)
        self.assertEqual(s.phonetic_result.status, "UNSUPPORTED")
        self.assertEqual(s.phonetic_result.segments, ())
        self.assertEqual(s.ukrainian_candidates, [])
        self.assertIsNone(s.tone)
        self.assertIn("PHON-IPA-WITHHELD-MULTIPLE-TONE-MARKS", s.rules)
        self.assertIn("MULTIPLE_TONE_MARKS", s.warnings)

    def test_silent_high_digraph(self):
        s = analyze("ຫນອງ").syllables[0]
        self.assertEqual(s.phonemic_ipa, "nɔːŋ")
        self.assertEqual(s.consonant_class, "high")
        self.assertEqual(s.tone, "low-rising")

    def test_ligature_high_digraph(self):
        s = analyze("ໜາ").syllables[0]
        self.assertEqual(s.phonemic_ipa, "naː")
        self.assertEqual(s.consonant_class, "high")
        self.assertEqual(s.tone, "low-rising")

    def test_r_is_analysis_dependent(self):
        s = analyze("ຣະ").syllables[0]
        self.assertEqual(s.phonemic_ipa, "la")
        self.assertEqual(s.status, "ANALYSIS DEPENDENT")

    def test_vowel_carrier(self):
        s = analyze("ອາ").syllables[0]
        self.assertEqual(s.phonemic_ipa, "aː")
        self.assertEqual(s.practical_ukrainian, "а")


    def test_unconsumed_material_before_preposed_vowel_withholds_output(self):
        s = analyze("xເເກ").syllables[0]
        self.assertEqual(s.status, "ANALYSIS DEPENDENT")
        self.assertIsNone(s.phonemic_ipa)
        self.assertIsNone(s.practical_ukrainian)
        self.assertTrue(any(w.startswith("UNCONSUMED_BEFORE_ONSET:") for w in s.warnings))

    def test_unconsumed_grapheme_withholds_whole_unit_ipa_and_target(self):
        s = analyze("ກາລ").syllables[0]
        self.assertEqual(s.status, "EVIDENCE LIMITED")
        self.assertIsNone(s.phonemic_ipa)
        self.assertIsNone(s.practical_ukrainian)
        self.assertEqual(s.ukrainian_candidates, [])
        self.assertIn("PHON-IPA-WITHHELD-UNCONSUMED-ORTHOGRAPHY", s.rules)
        self.assertTrue(any(w.startswith("UNCONSUMED_AFTER_VOWEL:") for w in s.warnings))

    def test_unconsumed_material_before_legal_final_withholds_full_output(self):
        s = analyze("ກາກງ").syllables[0]
        self.assertEqual(s.status, "EVIDENCE LIMITED")
        self.assertIsNone(s.phonemic_ipa)
        self.assertIsNone(s.practical_ukrainian)
        self.assertEqual(s.ukrainian_candidates, [])
        self.assertTrue(
            any(w.startswith("UNCONSUMED_AFTER_VOWEL:") for w in s.warnings)
        )

    def test_analysis_exposes_typed_ipa_result_as_the_adapter_boundary(self):
        syllable = analyze("ຂາ").syllables[0]
        result = syllable.phonetic_result
        self.assertIsNotNone(result)
        self.assertEqual(result.phonemic_ipa, "kʰaː")
        self.assertIsNone(result.broad_surface_ipa)
        self.assertIsNone(result.external_ipa)
        self.assertEqual([segment.ipa for segment in result.segments], ["kʰ", "aː"])
        self.assertEqual(result.syllable_boundaries, (0, 2))
        self.assertEqual(result.vowel_length, "long")
        self.assertEqual(result.tone_category, "low-rising")
        self.assertEqual(result.tone_contour_ipa, "˨˦")
        self.assertEqual(result.status, "SUPPORTED")
        self.assertEqual(syllable.practical_ukrainian, "к'а")

    def test_analysis_dependent_segmental_ipa_is_rendered_with_uncertain_status(self):
        syllable = analyze("ຣະ").syllables[0]
        self.assertEqual(syllable.phonemic_ipa, "la")
        self.assertEqual(syllable.phonetic_result.status, "UNCERTAIN")
        self.assertIsNone(syllable.practical_ukrainian)
        self.assertEqual(syllable.phonetic_result.status, "UNCERTAIN")
        self.assertEqual(syllable.status, "ANALYSIS DEPENDENT")

    def test_segmental_ipa_remains_adaptable_when_tone_is_unresolved(self):
        syllable = analyze("ຂັ່ບ").syllables[0]
        self.assertEqual(syllable.phonemic_ipa, "kʰap")
        self.assertEqual(syllable.phonetic_result.status, "SUPPORTED")
        self.assertIsNone(syllable.phonetic_result.tone_category)
        self.assertIn("TONE-UNRESOLVED", syllable.phonetic_result.uncertainty)
        self.assertEqual(syllable.practical_ukrainian, "к'ап")
        self.assertEqual(syllable.status, "ANALYSIS DEPENDENT")


    def test_hybrid_renders_unknown_lao_unit_through_typed_provisional_boundary(self):
        result = core_module.analyze("ກາລ")
        syllable = result.syllables[0]
        self.assertEqual(result.status, "PARTIAL")
        self.assertIsNone(syllable.phonemic_ipa)
        self.assertEqual(syllable.practical_ukrainian, "?")
        self.assertEqual(syllable.phonetic_result.status, "PROVISIONAL")
        self.assertEqual(len(syllable.phonetic_result.segments), 1)
        self.assertEqual(syllable.phonetic_result.segments[0].kind, "unknown")
        self.assertEqual(syllable.phonetic_result.segments[0].certainty, "PROVISIONAL")
        self.assertIn("PHONETIC-READING-UNKNOWN", syllable.phonetic_result.uncertainty)

    def test_hybrid_renders_analysis_dependent_ipa_without_promoting_confidence(self):
        syllable = core_module.analyze("ຣະ").syllables[0]
        self.assertEqual(syllable.phonemic_ipa, "ra")
        self.assertEqual(syllable.practical_ukrainian, "ра")
        self.assertEqual(syllable.phonetic_result.status, "UNCERTAIN")
        self.assertEqual(syllable.status, "ANALYSIS DEPENDENT")


class TestMinorSyllableSelectorEvidence(unittest.TestCase):
    def test_minor_candidate_requires_supported_following_onset(self):
        result = analyze("ຄະຣາ")
        self.assertTrue(result.syllables)
        self.assertNotIn("VNT-POTENTIAL-MINOR-OPEN-A-UNRESOLVED", result.syllables[0].rules)

    def test_minor_candidate_excludes_known_palatal_and_velar_nasal_onsets(self):
        for word in ("ງະຄາ", "ຍະຄາ"):
            with self.subTest(word=word):
                result = analyze(word)
                self.assertTrue(result.syllables)
                self.assertNotIn("VNT-POTENTIAL-MINOR-OPEN-A-UNRESOLVED", result.syllables[0].rules)


    def test_ascii_and_common_punctuation_are_explicit_passthrough_not_ipa(self):
        result = analyze("ຂາ, 2026! abc.&%–…#/`+•")
        passthrough = [item for item in result.syllables if item.status == "PASSTHROUGH"]
        self.assertEqual("".join(item.surface for item in passthrough), ",2026!abc.&%–…#/`+•")
        self.assertTrue(all(item.phonemic_ipa is None for item in passthrough))
        self.assertTrue(all(item.practical_ukrainian == item.surface for item in passthrough))
        self.assertTrue(all("PASSTHROUGH:NON_LAO_ORTHOGRAPHIC_CHARACTER" in item.rules for item in passthrough))
        self.assertEqual(result.syllables[0].phonemic_ipa, "kʰaː")
        self.assertEqual(result.status, "OK")

    def test_passthrough_only_input_is_preserved_without_fabricated_ipa(self):
        result = analyze("ABC-123!?")
        self.assertEqual(result.status, "OK")
        self.assertEqual("".join(item.practical_ukrainian for item in result.syllables), "ABC-123!?")
        self.assertTrue(all(item.phonemic_ipa is None for item in result.syllables))
        self.assertTrue(all(item.status == "PASSTHROUGH" for item in result.syllables))

    def test_passthrough_prefix_does_not_hide_following_lao_syllable(self):
        result = analyze("(ຂາ")
        self.assertEqual(result.syllables[0].status, "PASSTHROUGH")
        self.assertEqual(result.syllables[0].practical_ukrainian, "(")
        self.assertEqual(result.syllables[1].phonemic_ipa, "kʰaː")
        self.assertEqual(result.status, "OK")

    def test_lao_native_digits_are_preserved_as_non_ipa_passthrough(self):
        result = analyze("ຂາ໑໒໓")
        digits = [item for item in result.syllables if item.surface in "໑໒໓"]
        self.assertEqual("".join(item.surface for item in digits), "໑໒໓")
        self.assertTrue(all(item.status == "PASSTHROUGH" for item in digits))
        self.assertTrue(all(item.phonemic_ipa is None for item in digits))
        self.assertTrue(all("PASSTHROUGH:LAO_NATIVE_DIGIT" in item.rules for item in digits))
        self.assertEqual(result.syllables[0].phonemic_ipa, "kʰaː")
