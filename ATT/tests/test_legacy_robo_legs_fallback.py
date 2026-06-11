from services.legacy_robo_legs_fallback import LegacyRoboLegsFallback


class DummyStatus:
    def __init__(self, chosen_ts):
        self.chosen_ts = chosen_ts


class DummyRoboLegsService:
    def __init__(self, chosen_ts="2026-05-19 10:00:00", legs=None):
        self._chosen_ts = chosen_ts
        self._legs = legs or []

    def status(self, aba, requested_timestamp):
        return DummyStatus(self._chosen_ts)

    def get_legs(self, aba, timestamp):
        return self._legs


def test_resolve_legacy_aba_prefers_alias():
    svc = LegacyRoboLegsFallback(robo_legs_service=None, allow_name_fallback=False)

    aba, key_source, reason = svc._resolve_legacy_aba({
        "alias_legacy_aba": "ABA_CANON",
        "name": "Nome Estrutura",
    })

    assert aba == "ABA_CANON"
    assert key_source == "alias_legacy_aba"
    assert reason is None


def test_resolve_legacy_aba_blocks_name_when_disabled():
    svc = LegacyRoboLegsFallback(robo_legs_service=None, allow_name_fallback=False)

    aba, key_source, reason = svc._resolve_legacy_aba({
        "alias_legacy_aba": None,
        "name": "Nome Estrutura",
    })

    assert aba is None
    assert key_source == "name_fallback_disabled"
    assert reason == "alias_missing_name_fallback_disabled"


def test_resolve_legacy_aba_uses_name_when_enabled():
    svc = LegacyRoboLegsFallback(robo_legs_service=None, allow_name_fallback=True)

    aba, key_source, reason = svc._resolve_legacy_aba({
        "alias_legacy_aba": None,
        "name": "Nome Estrutura",
    })

    assert aba == "Nome Estrutura"
    assert key_source == "structure_name_fallback"
    assert reason == "alias_missing_name_fallback_used"


def test_load_returns_empty_when_missing_key():
    svc = LegacyRoboLegsFallback(robo_legs_service=None, allow_name_fallback=False)

    legs, meta = svc.load(
        structure={"alias_legacy_aba": None, "name": None},
        reference_date="2026-05-19",
    )

    assert legs == []
    assert meta["legs_source"] == "empty"
    assert meta["legacy_aba"] is None
    assert meta["fallback_reason"] == "alias_and_name_missing"


def test_load_returns_empty_when_service_missing():
    svc = LegacyRoboLegsFallback(robo_legs_service=None, allow_name_fallback=False)

    legs, meta = svc.load(
        structure={"alias_legacy_aba": "ABA1", "name": "Nome"},
        reference_date="2026-05-19",
    )

    assert legs == []
    assert meta["legacy_aba"] == "ABA1"
    assert meta["fallback_reason"] == "robo_legs_service_unavailable"


def test_load_returns_legacy_fallback_with_meta():
    robo_service = DummyRoboLegsService(
        chosen_ts="2026-05-19 10:00:00",
        legs=[
            {
                "cv": "C",
                "call_put": "CALL",
                "ativo": "PETR4",
                "strike": 100,
                "vencimento": "2026-06-20",
                "quant": 2,
                "preco": 1.5,
            }
        ],
    )
    svc = LegacyRoboLegsFallback(robo_legs_service=robo_service, allow_name_fallback=False)

    legs, meta = svc.load(
        structure={"alias_legacy_aba": "ABA1", "name": "Nome"},
        reference_date="2026-05-19",
    )

    assert len(legs) == 1
    assert legs[0]["position_side"] == "LONG"
    assert legs[0]["option_type"] == "CALL"
    assert legs[0]["symbol"] == "PETR4"
    assert legs[0]["strike"] == 100.0
    assert legs[0]["quantity"] == 2
    assert meta["legs_source"] == "legacy_fallback"
    assert meta["legacy_aba"] == "ABA1"
    assert meta["legacy_key_source"] == "alias_legacy_aba"
