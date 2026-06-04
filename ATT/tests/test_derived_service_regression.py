from datetime import datetime

import services.derived_service as ds


def test_now_iso_is_parseable_and_timezone_aware():
    value = ds._now_iso()
    parsed = datetime.fromisoformat(value)

    assert parsed.tzinfo is not None


def test_resolve_storage_key_prefers_aba():
    key = ds._resolve_storage_key(
        aba="ABA_X",
        structure_id=123,
        structure_name="Trava XYZ",
        underlying_asset="PETR4",
    )
    assert key == "ABA_X"


def test_resolve_storage_key_uses_structure_id_when_aba_missing():
    key = ds._resolve_storage_key(
        aba=None,
        structure_id=123,
        structure_name="Trava XYZ",
        underlying_asset="PETR4",
    )
    assert key == "structure:123"


def test_resolve_storage_key_uses_structure_name_when_id_missing():
    key = ds._resolve_storage_key(
        aba=None,
        structure_id=None,
        structure_name="Trava XYZ",
        underlying_asset="PETR4",
    )
    assert key == "Trava XYZ"


def test_resolve_storage_key_uses_underlying_asset_as_last_named_key():
    key = ds._resolve_storage_key(
        aba=None,
        structure_id=None,
        structure_name=None,
        underlying_asset="PETR4",
    )
    assert key == "PETR4"


def test_resolve_storage_key_returns_unknown_when_all_missing():
    key = ds._resolve_storage_key(
        aba=None,
        structure_id=None,
        structure_name=None,
        underlying_asset=None,
    )
    assert key == "unknown"


def test_save_payoff_from_canonical_payload_uses_resolved_storage_key(monkeypatch):
    captured = {}

    def fake_save_payoff_curve(ref, points, spot_ref=None, meta=None, timestamp=None):
        captured["aba"] = ref
        captured["points"] = points
        captured["spot_ref"] = spot_ref
        captured["meta"] = meta
        captured["timestamp"] = timestamp
        return 777

    monkeypatch.setattr(ds, "save_payoff_curve", fake_save_payoff_curve)

    payload = {
        "structure_id": 99,
        "structure_name": "Iron Condor",
        "underlying_asset": "PETR4",
        "reference_date": "2026-05-19",
        "input_meta": {"x": 1},
        "meta": {"source": "test"},
        "points": [{"point_spot": 10, "point_pl": 20}],
        "spot_ref": 11.5,
    }

    result = ds.save_payoff_from_canonical_payload(payload)

    assert result == 777
    assert captured["aba"] == "structure:99"
    assert captured["spot_ref"] == 11.5
    assert captured["meta"]["structure_id"] == 99
    assert captured["meta"]["structure_name"] == "Iron Condor"
    assert captured["meta"]["underlying_asset"] == "PETR4"
    assert captured["meta"]["reference_date"] == "2026-05-19"
    assert captured["meta"]["input_meta"] == {"x": 1}
    assert captured["meta"]["storage_key"] == "structure:99"


def test_save_decision_from_canonical_payload_enriches_meta(monkeypatch):
    captured = {}

    def fake_save_decision(ref, decision, timestamp=None):
        captured["aba"] = ref
        captured["decision"] = decision
        captured["timestamp"] = timestamp
        return 888

    monkeypatch.setattr(ds, "save_decision", fake_save_decision)

    payload = {
        "action": "hold",
        "meta": {"origin": "test"},
    }

    result = ds.save_decision_from_canonical_payload(
        decision=payload,
        structure_id=321,
        structure_name="Fence",
        underlying_asset="VALE3",
        aba=None,
    )

    assert result == 888
    assert captured["aba"] == "structure:321"
    assert captured["decision"]["meta"]["origin"] == "test"
    assert captured["decision"]["meta"]["structure_id"] == 321
    assert captured["decision"]["meta"]["structure_name"] == "Fence"
    assert captured["decision"]["meta"]["underlying_asset"] == "VALE3"
    assert captured["decision"]["meta"]["storage_key"] == "structure:321"
