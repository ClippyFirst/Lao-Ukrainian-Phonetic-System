import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def test_unicode_18_lao_block_assigned_codepoints_are_in_inventory():
    with (ROOT / "data/lao/grapheme_inventory.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    cps = [int(r["codepoint"][2:], 16) for r in rows]
    assert len(cps) == len(set(cps)) == len(rows)
    assert len({r["grapheme"] for r in rows}) == len(rows)
    assert all(ord(r["grapheme"]) == cp for r, cp in zip(rows, cps))
    assert cps == [3713,3714,3716,3718,3719,3720,3721,3722,3724,3725,3726,3727,3728,3729,3730,3731,3732,3733,3734,3735,3736,3737,3738,3739,3740,3741,3742,3743,3744,3745,3746,3747,3749,3751,3752,3753,3754,3755,3756,3757,3758,3759,3760,3761,3762,3763,3764,3765,3766,3767,3768,3769,3770,3771,3772,3773,3776,3777,3778,3779,3780,3782,3784,3785,3786,3787,3788,3789,3790,3792,3793,3794,3795,3796,3797,3798,3799,3800,3801,3804,3805,3806,3807]

def test_inventory_distinguishes_core_extensions_and_nonphonological_items():
    with (ROOT / "data/lao/grapheme_inventory.csv").open(encoding="utf-8", newline="") as f:
        rows = {r["grapheme"]: r for r in csv.DictReader(f)}
    assert rows["ກ"]["engine_status"] == "CORE_POSITIONAL"
    assert rows["ຣ"]["engine_status"] == "ANALYSIS_DEPENDENT"
    assert rows["ຆ"]["engine_status"] == "NON_CORE_NO_MODERN_IPA"
    assert rows["ຨ"]["engine_status"] == "NON_CORE_NO_MODERN_IPA"
    assert rows["ໞ"]["engine_status"] == "OUT_OF_SCOPE_KHMU"
    assert rows["່"]["engine_status"] == "TONE_ONLY"
    assert rows["໐"]["engine_status"] == "NONPHONOLOGICAL"
