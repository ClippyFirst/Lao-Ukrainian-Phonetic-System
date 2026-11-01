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


def test_rejects_unexpected_response_shape():
    try:
        MODULE.extract_phonetics({"words": []})
    except ValueError as exc:
        assert "Words array" in str(exc)
    else:
        raise AssertionError("unexpected API shape must be rejected")


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
    )
    assert report["successful_outputs"] == 1
    assert report["independent_gold_count"] == 0
    assert report["accuracy"] is None
    assert report["score_status"] == "NOT_SCORED_NO_INDEPENDENT_GOLD"
    assert "not an accuracy benchmark" in report["purpose"]
    assert report["records"][0]["phonetic_tokens"] == ["kʰaː"]
