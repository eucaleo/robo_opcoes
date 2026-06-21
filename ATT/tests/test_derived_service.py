from datetime import datetime

import services.derived_service as ds


def test_now_iso_should_be_parseable_and_timezone_aware():
    value = ds._now_iso()
    parsed = datetime.fromisoformat(value)

    assert parsed.tzinfo is not None


def test_resolve_storage_key_should_prefer_aba_when_present():
    result = ds._resolve_storage_key(
        aba="BOVA11",
        structure_id=7,
        structure_name="BOVA11 Condor Maio/2026",
        underlying_asset="BOVA11",
    )

    assert result == "BOVA11"


def test_resolve_storage_key_should_fallback_to_structure_id():
    result = ds._resolve_storage_key(
        aba=None,
        structure_id=7,
        structure_name="BOVA11 Condor Maio/2026",
        underlying_asset="BOVA11",
    )

    assert result == "structure:7"


def test_resolve_storage_key_should_use_structure_name_when_id_missing():
    result = ds._resolve_storage_key(
        aba=None,
        structure_id=None,
        structure_name="Trava XYZ",
        underlying_asset="PETR4",
    )

    assert result == "Trava XYZ"


def test_resolve_storage_key_should_use_underlying_asset_as_last_named_key():
    result = ds._resolve_storage_key(
        aba=None,
        structure_id=None,
        structure_name=None,
        underlying_asset="PETR4",
    )

    assert result == "PETR4"


def test_resolve_storage_key_should_return_unknown_when_all_missing():
    result = ds._resolve_storage_key(
        aba=None,
        structure_id=None,
        structure_name=None,
        underlying_asset=None,
    )

    assert result == "unknown"


def test_merge_meta_should_enrich_with_canonical_identity():
    result = ds._merge_meta(
        meta={"origin": "test"},
        structure_id=7,
        structure_name="BOVA11 Condor Maio/2026",
        underlying_asset="BOVA11",
        reference_date="2026-05-18",
        input_meta={"legs_source": "canonical"},
    )

    assert result["origin"] == "test"
    assert result["structure_id"] == 7
    assert result["structure_name"] == "BOVA11 Condor Maio/2026"
    assert result["underlying_asset"] == "BOVA11"
    assert result["reference_date"] == "2026-05-18"
    assert result["input_meta"]["legs_source"] == "canonical"


def test_save_payoff_from_canonical_payload_should_use_resolved_storage_key(monkeypatch):
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
    assert captured["points"] == [{"point_spot": 10, "point_pl": 20}]
    assert captured["spot_ref"] == 11.5
    assert captured["meta"]["source"] == "test"
    assert captured["meta"]["structure_id"] == 99
    assert captured["meta"]["structure_name"] == "Iron Condor"
    assert captured["meta"]["underlying_asset"] == "PETR4"
    assert captured["meta"]["reference_date"] == "2026-05-19"
    assert captured["meta"]["input_meta"] == {"x": 1}
    assert captured["meta"]["storage_key"] == "structure:99"


def test_save_decision_from_canonical_payload_should_enrich_meta(monkeypatch):
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

# FASE_3A4_TESTS_DERIVED_SERVICE

def test_save_decision_preserva_structure_id_explicito_sem_alias(monkeypatch):
    import services.derived_service as svc

    captured = {}

    class FakeConn:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    def fake_insert_structure_decision(conn, timestamp, aba, decision_dict):
        captured["timestamp"] = timestamp
        captured["aba"] = aba
        captured["decision_dict"] = decision_dict
        return 1

    monkeypatch.setattr(svc, "connect_derived", lambda: FakeConn())
    monkeypatch.setattr(svc, "ensure_derived_tables", lambda conn: None)
    monkeypatch.setattr(svc, "_resolve_structure_id", lambda storage_key: None)
    monkeypatch.setattr(svc, "insert_structure_decision", fake_insert_structure_decision)

    result = svc.save_decision(
        ref="structure:7",
        decision={
            "structure_id": 7,
            "decision": "hold",
            "meta": {"source": "test"},
        },
        timestamp="2026-06-21T00:00:00+00:00",
    )

    assert result == 1
    assert captured["aba"] == "structure:7"
    assert captured["decision_dict"]["structure_id"] == 7
    assert captured["decision_dict"]["meta"]["structure_id"] == 7
    assert captured["decision_dict"]["meta"]["storage_key"] == "structure:7"
