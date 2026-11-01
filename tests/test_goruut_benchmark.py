import importlib.util
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "benchmark_goruut.py"
SPEC = importlib.util.spec_from_file_location("goruut_probe", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_extracts_raw_phonetic_words_without_rewriting():
    assert MODULE.extract_phonetics({
        "Words": [
            {"Linguistic": "ຂາ", "Phonetic": "kʰaː˩˧"},
            {"Linguistic": "ຄົນ", "Phonetic": "kʰon"},
        ]
    }) == ["kʰaː˩˧", "kʰon"]


def test_rejects_empty_and_unexpected_response_shapes():
    try:
        MODULE.extract_phonetics({"words": []})
    except ValueError as exc:
        assert "Words array" in str(exc)
    else:
        raise AssertionError("unexpected API shape must be rejected")
    for payload in ({"Words": []}, {"Words": [{"Linguistic": "word", "Phonetic": ""}]}):
        try:
            MODULE.extract_phonetics(payload)
        except ValueError:
            pass
        else:
            raise AssertionError("empty phonetic response must be rejected")


def test_csv_loader_keeps_source_attested_ipa_separate(tmp_path):
    path = tmp_path / "mekongphon.csv"
    path.write_text("orth,pron_with_tones\nຂາ,kʰaː˩˧\n", encoding="utf-8")
    rows = MODULE.load_inputs(path, input_format="csv", text_column="orth", expected_column="pron_with_tones")
    assert rows == [{"text": "ຂາ", "source_attested_ipa": "kʰaː˩˧"}]


def test_report_never_scores_runtime_output_as_accuracy(tmp_path):
    fixture = tmp_path / "probes.txt"
    fixture.write_text("ຂາ\n", encoding="utf-8")
    records = [{
        "input": "ຂາ", "status": "OK",
        "raw_response": '{"Words":[{"Linguistic":"ຂາ","Phonetic":"kʰaː"}]}',
        "phonetic_tokens": ["kʰaː"], "source_coverage_complete": True, "error": None,
    }]
    report = MODULE.build_report(
        ["ຂາ"], records, language="Lao", engine_commit="b224bde",
        input_path=fixture, input_sha256="fixture-sha", base_url="http://127.0.0.1:18080",
        config_path=fixture, config_sha256="config-sha", runtime_version="go version go1.23",
    )
    assert report["successful_outputs"] == 1
    assert report["independent_gold_count"] == 0
    assert report["accuracy"] is None
    assert report["score_status"] == "NOT_SCORED_NO_INDEPENDENT_GOLD"
    assert "not an accuracy benchmark" in report["purpose"]
    assert report["records"][0]["phonetic_tokens"] == ["kʰaː"]
    assert report["effective_config_sha256"] == "config-sha"
    assert report["go_runtime_version"] == "go version go1.23"
    assert report["source_attested_diagnostic"] is None
    assert report["failed_outputs"] == 0


def test_empty_words_response_is_preserved_as_a_probe_failure():
    raw = '{"Words":[]}'
    try:
        MODULE.extract_phonetics(__import__("json").loads(raw))
    except ValueError as exc:
        assert "must not be empty" in str(exc)
    else:
        raise AssertionError("empty response must be detected")


def test_source_attested_concordance_is_not_gold_or_accuracy(tmp_path):
    fixture = tmp_path / "source.csv"
    fixture.write_text("orth,ipa\nword,kʰaː\n", encoding="utf-8")
    inputs = MODULE.load_inputs(fixture, input_format="csv", text_column="orth", expected_column="ipa")
    records = [{
        "input": "word", "status": "OK", "raw_response": "{}",
        "phonetic_tokens": ["kʰaː"], "source_coverage_complete": True, "error": None,
    }]
    report = MODULE.build_report(
        inputs, records, language="Lao", engine_commit="test",
        input_path=fixture, input_sha256="sha", base_url="http://127.0.0.1:18080",
        config_path=fixture, config_sha256="config", runtime_version="go test",
    )
    assert report["source_attested_diagnostic"]["exact_matches"] == 1
    assert report["source_attested_diagnostic"]["status"] == "SOURCE_ATTESTED_CONCORDANCE_ONLY_NOT_GOLD"
    assert report["independent_gold_count"] == 0
    assert report["accuracy"] is None


def test_missing_model_assets_are_recorded_from_server_log(tmp_path):
    fixture = tmp_path / "probes.txt"
    fixture.write_text("word\n", encoding="utf-8")
    log = tmp_path / "server.log"
    log.write_text('level=error msg="open weights9.bin.zlib: file does not exist"\n', encoding="utf-8")
    report = MODULE.build_report(
        ["word"], [{
            "input": "word", "status": "OK", "raw_response": "{}",
            "phonetic_tokens": ["wɜːd"], "error": None,
        }],
        language="Lao", engine_commit="test", input_path=fixture,
        input_sha256="sha", base_url="http://127.0.0.1:18080",
        config_path=fixture, config_sha256="config", runtime_version="go test",
        server_log_path=log,
    )
    assert report["server_log_sha256"]
    assert len(report["model_asset_warnings"]) == 1
    assert "weights9.bin.zlib" in report["model_asset_warnings"][0]


def test_repeated_requests_detect_nondeterministic_outputs():
    outputs = [
        '{"Words":[{"Linguistic":"word","Phonetic":"kʰaː˩˧"}]}',
        '{"Words":[{"Linguistic":"word","Phonetic":"kʰaː˥˧˧"}]}',
        '{"Words":[{"Linguistic":"word","Phonetic":"kʰaː˩˧"}]}',
    ]
    with patch.object(MODULE, "request_raw_response", side_effect=outputs):
        record = MODULE.run_probe(
            "http://127.0.0.1:18080", "Lao", "word", 1.0, 1, repeat_count=3,
        )
    assert record["status"] == "OK"
    assert record["successful_repetitions"] == 3
    assert record["unstable"] is True
    assert record["reproducible"] is False
    assert len(record["repetitions"]) == 3


def test_notation_diagnostic_preserves_tone_length_aspiration_and_tie_bars():
    key = MODULE.notation_comparison_key
    assert key("/pʰiə.saː/") == key("pʰiəsaː")
    assert key("/tʰaː˥/") != key("taː˥")
    assert key("/taː˥/") != key("ta˥")
    assert key("/ta˥/") != key("ta˩")
    assert key("/t͡ɕi/") != key("tɕi")


def test_stable_three_repeat_source_match_remains_non_gold(tmp_path):
    raw = '{"Words":[{"Linguistic":"word","CleanWord":"word","PrePunct":"","PostPunct":"","Phonetic":"kʰaː"}]}'
    with patch.object(MODULE, "request_raw_response", side_effect=[raw, raw, raw]):
        record = MODULE.run_probe(
            "http://127.0.0.1:18080", "Lao", "word", 1.0, 1, repeat_count=3,
        )
    fixture = tmp_path / "source.csv"
    fixture.write_text("orth,ipa\nword,kʰaː\n", encoding="utf-8")
    report = MODULE.build_report(
        [{"text": "word", "source_attested_ipa": "kʰaː"}], [record],
        language="Lao", engine_commit="test", input_path=fixture,
        input_sha256="sha", base_url="http://127.0.0.1:18080",
        config_path=fixture, config_sha256="config", runtime_version="go test",
    )
    assert record["reproducible"] is True
    assert report["source_attested_diagnostic"]["exact_matches"] == 1
    assert report["source_attested_diagnostic"]["notation_normalized_matches"] == 1
    assert report["accuracy"] is None
    assert report["independent_gold_count"] == 0


def test_probe_preserves_upstream_dictionary_randomization_metadata():
    raw = '{"Words":[{"Linguistic":"word","Phonetic":"kʰaː˩˧"}],"RandomizationWordsCount":1,"RandomizationWordsChoices":2}'
    with patch.object(MODULE, "request_raw_response", side_effect=[raw, raw, raw]):
        record = MODULE.run_probe(
            "http://127.0.0.1:18080", "Lao", "word", 1.0, 1, repeat_count=3,
        )
    assert record["randomization_words_count_max"] == 1
    assert record["randomization_words_choices_max"] == 2
    assert record["randomized_repetitions"] == 3
    assert record["ambiguous_dictionary_selection"] is True
    assert record["repetitions"][0]["randomization_words_count"] == 1
    assert record["repetitions"][0]["randomization_words_choices"] == 2


def test_report_counts_randomized_inputs_without_scoring_accuracy(tmp_path):
    fixture = tmp_path / "probes.txt"
    fixture.write_text("word\\n", encoding="utf-8")
    record = {
        "input": "word", "status": "OK", "raw_response": "{}",
        "phonetic_tokens": ["wɜːd"], "error": None,
        "repetitions": [{
            "repeat": 1, "status": "OK", "phonetic_tokens": ["wɜːd"],
            "randomization_words_count": 1, "randomization_words_choices": 2,
        }],
        "randomization_words_count_max": 1,
        "randomization_words_choices_max": 2,
        "randomized_repetitions": 1,
        "ambiguous_dictionary_selection": True,
        "unstable": False, "reproducible": True,
    }
    report = MODULE.build_report(
        ["word"], [record], language="Lao", engine_commit="test",
        input_path=fixture, input_sha256="sha", base_url="http://127.0.0.1:18080",
        config_path=fixture, config_sha256="config", runtime_version="go test",
    )
    assert report["randomized_input_count"] == 1
    assert report["randomized_repetition_count"] == 1
    assert report["unstable_randomized_input_count"] == 0
    assert report["accuracy"] is None


def test_source_coverage_flags_letters_left_in_punctuation_fields():
    payload = {
        "Words": [{
            "CleanWord": "ទ", "PrePunct": "បេះបិ", "PostPunct": "", "Phonetic": "t",
        }]
    }
    coverage = MODULE.analyze_source_coverage(payload, "បេះបិទ")
    assert coverage["source_reconstruction_matches_input"] is True
    assert coverage["source_coverage_complete"] is False
    assert coverage["unphonemized_source_fragments"] == [
        {"word_index": 0, "field": "PrePunct", "text": "បេះបិ"}
    ]


def test_source_coverage_detects_silently_dropped_source_characters():
    payload = {
        "Words": [{
            "CleanWord": "ກິ", "PrePunct": "", "PostPunct": "", "Phonetic": "ki",
        }]
    }
    coverage = MODULE.analyze_source_coverage(payload, "ເກິ")
    assert coverage["source_reconstruction_matches_input"] is False
    assert coverage["source_coverage_complete"] is False


def test_source_coverage_accepts_punctuation_but_not_unphonemized_letters():
    payload = {
        "Words": [{
            "CleanWord": "ကေ", "PrePunct": "", "PostPunct": "၊။", "Phonetic": "ke",
        }]
    }
    coverage = MODULE.analyze_source_coverage(payload, "ကေ၊။")
    assert coverage["source_reconstruction_matches_input"] is True
    assert coverage["source_coverage_complete"] is True
    assert coverage["unphonemized_source_fragments"] == []


def test_probe_and_report_separate_complete_from_partial_source_coverage(tmp_path):
    partial = '{"Words":[{"CleanWord":"ទ","PrePunct":"បេះបិ","PostPunct":"","Phonetic":"t"}]}'
    with patch.object(MODULE, "request_raw_response", side_effect=[partial, partial, partial]):
        record = MODULE.run_probe(
            "http://127.0.0.1:18080", "KhmerCentral", "បេះបិទ", 1.0, 1, repeat_count=3,
        )
    assert record["source_coverage_status"] == "PARTIAL"
    assert record["source_coverage_complete"] is False
    assert record["unphonemized_source_fragments"] == [
        {"word_index": 0, "field": "PrePunct", "text": "បេះបិ"}
    ]
    fixture = tmp_path / "probes.txt"
    fixture.write_text("បេះបិទ\\n", encoding="utf-8")
    report = MODULE.build_report(
        ["បេះបិទ"], [record], language="Khmer", engine_commit="test",
        input_path=fixture, input_sha256="sha", base_url="http://127.0.0.1:18080",
        config_path=fixture, config_sha256="config", runtime_version="go test",
    )
    assert report["source_coverage_complete_outputs"] == 0
    assert report["source_coverage_partial_outputs"] == 1
    assert report["source_coverage_unknown_outputs"] == 0
    assert report["unphonemized_source_fragment_count"] == 1
    assert report["accuracy"] is None


def test_source_coverage_flags_empty_phonetic_word_inside_nonempty_response():
    payload = {
        "Words": [
            {"CleanWord": "ក", "PrePunct": "", "PostPunct": "", "Phonetic": ""},
            {"CleanWord": "េ", "PrePunct": "", "PostPunct": "", "Phonetic": "e"},
        ]
    }
    coverage = MODULE.analyze_source_coverage(payload, "កេ")
    assert coverage["source_reconstruction_matches_input"] is True
    assert coverage["source_coverage_complete"] is False
    assert coverage["empty_phonetic_word_indices"] == [0]


def test_source_attested_match_is_rejected_when_response_only_covers_a_suffix(tmp_path):
    raw = '{"Words":[{"CleanWord":"ទ","PrePunct":"បេះបិ","PostPunct":"","Phonetic":"t"}]}'
    with patch.object(MODULE, "request_raw_response", side_effect=[raw, raw, raw]):
        record = MODULE.run_probe(
            "http://127.0.0.1:18080", "KhmerCentral", "បេះបិទ", 1.0, 1, repeat_count=3,
        )
    fixture = tmp_path / "source.csv"
    fixture.write_text("orth,ipa\\nបេះបិទ,t\\n", encoding="utf-8")
    inputs = MODULE.load_inputs(fixture, input_format="csv", text_column="orth", expected_column="ipa")
    report = MODULE.build_report(
        inputs, [record], language="Khmer", engine_commit="test",
        input_path=fixture, input_sha256="sha", base_url="http://127.0.0.1:18080",
        config_path=fixture, config_sha256="config", runtime_version="go test",
    )
    assert record["source_coverage_status"] == "PARTIAL"
    assert report["source_attested_diagnostic"]["exact_matches"] == 0
    assert report["source_attested_diagnostic"]["any_repeat_exact_matches"] == 0
