from services.canonical_input_service import CanonicalInputService


class DummyRepository:
    def __init__(self, structure):
        self.structure = structure

    def get_structure(self, structure_id):
        return self.structure


class DummySnapshotProvider:
    def get_snapshot(self, underlying_asset, reference_date=None):
        return {
            "underlying_asset": underlying_asset,
            "reference_date": reference_date or "2026-05-19",
            "spot": 10.0,
        }


class DummyFallback:
    def __init__(self, legs, meta):
        self._legs = legs
        self._meta = meta
        self.called = False

    def load(self, structure, reference_date):
        self.called = True
        return self._legs, self._meta


def test_enrich_keeps_canonical_legs_when_present():
    service = CanonicalInputService(
        repository=DummyRepository({
            "id": 1,
            "name": "Estrutura A",
            "underlying_asset": "PETR4",
            "legs": [{"symbol": "PETR4"}],
        }),
        market_snapshot_provider=DummySnapshotProvider(),
        prefer_canonical_legs=True,
        enable_legacy_legs_fallback=True,
    )

    service.legacy_robo_legs_fallback = DummyFallback(
        legs=[{"symbol": "VALE3"}],
        meta={"legs_source": "legacy_fallback"},
    )

    enriched, meta = service._enrich_structure_with_legs(
        structure={
            "id": 1,
            "name": "Estrutura A",
            "underlying_asset": "PETR4",
            "legs": [{"symbol": "PETR4"}],
        },
        reference_date="2026-05-19",
    )

    assert enriched["legs"] == [{"symbol": "PETR4"}]
    assert meta["legs_source"] == "canonical"
    assert service.legacy_robo_legs_fallback.called is False


def test_enrich_returns_empty_when_fallback_disabled_and_no_legs():
    service = CanonicalInputService(
        repository=DummyRepository({
            "id": 1,
            "name": "Estrutura A",
            "underlying_asset": "PETR4",
            "legs": [],
        }),
        market_snapshot_provider=DummySnapshotProvider(),
        prefer_canonical_legs=True,
        enable_legacy_legs_fallback=False,
    )

    enriched, meta = service._enrich_structure_with_legs(
        structure={
            "id": 1,
            "name": "Estrutura A",
            "underlying_asset": "PETR4",
            "legs": [],
        },
        reference_date="2026-05-19",
    )

    assert enriched["legs"] == []
    assert meta["legs_source"] == "empty"
    assert meta["fallback_reason"] == "legacy_fallback_disabled"


def test_enrich_uses_legacy_fallback_when_no_canonical_legs():
    service = CanonicalInputService(
        repository=DummyRepository({
            "id": 1,
            "name": "Estrutura A",
            "underlying_asset": "PETR4",
            "legs": [],
        }),
        market_snapshot_provider=DummySnapshotProvider(),
        prefer_canonical_legs=True,
        enable_legacy_legs_fallback=True,
    )

    service.legacy_robo_legs_fallback = DummyFallback(
        legs=[{"symbol": "VALE3", "strike": 10}],
        meta={
            "legs_source": "legacy_fallback",
            "legacy_timestamp": "2026-05-19 10:00:00",
            "legacy_aba": "ABA_X",
            "legacy_key_source": "alias_legacy_aba",
            "fallback_reason": None,
        },
    )

    enriched, meta = service._enrich_structure_with_legs(
        structure={
            "id": 1,
            "name": "Estrutura A",
            "underlying_asset": "PETR4",
            "legs": [],
        },
        reference_date="2026-05-19",
    )

    assert enriched["legs"] == [{"symbol": "VALE3", "strike": 10}]
    assert meta["legs_source"] == "legacy_fallback"
    assert meta["legacy_aba"] == "ABA_X"
    assert meta["legacy_key_source"] == "alias_legacy_aba"


def test_enrich_returns_empty_when_fallback_returns_nothing():
    service = CanonicalInputService(
        repository=DummyRepository({
            "id": 1,
            "name": "Estrutura A",
            "underlying_asset": "PETR4",
            "legs": [],
        }),
        market_snapshot_provider=DummySnapshotProvider(),
        prefer_canonical_legs=True,
        enable_legacy_legs_fallback=True,
    )

    service.legacy_robo_legs_fallback = DummyFallback(
        legs=[],
        meta={"fallback_reason": "no_legacy_legs_found"},
    )

    enriched, meta = service._enrich_structure_with_legs(
        structure={
            "id": 1,
            "name": "Estrutura A",
            "underlying_asset": "PETR4",
            "legs": [],
        },
        reference_date="2026-05-19",
    )

    assert enriched["legs"] == []
    assert meta["legs_source"] == "empty"
    assert meta["fallback_reason"] == "no_legacy_legs_found"
