import importlib.util
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
        "phonetic_tokens": ["kʰaː"], "error": None,
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
        "phonetic_tokens": ["kʰaː"], "error": None,
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
