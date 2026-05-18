from services.canonical_input_service import CanonicalInputService


class FakeRepository:
    def __init__(self, structure):
        self.structure = structure

    def get_structure(self, structure_id: int):
        if structure_id == self.structure["id"]:
            return self.structure
        return None


class FakeMarketSnapshotProvider:
    def __init__(self, snapshot):
        self.snapshot = snapshot
        self.calls = []

    def get_snapshot(self, underlying_asset: str, reference_date: str | None = None):
        self.calls.append(
            {
                "underlying_asset": underlying_asset,
                "reference_date": reference_date,
            }
        )
        return self.snapshot


class FakeRoboRepo:
    def __init__(self, timestamps):
        self.timestamps = timestamps

    def list_timestamps(self, aba: str):
        return self.timestamps


class FakeRoboLegsService:
    def __init__(self, timestamps, legs):
        self.repo = FakeRoboRepo(timestamps)
        self.legs = legs
        self.calls = []

    def get_legs(self, aba: str, timestamp: str, validate: bool = False):
        self.calls.append(
            {
                "aba": aba,
                "timestamp": timestamp,
                "validate": validate,
            }
        )
        return self.legs


def fake_assemble_structure_market_input(structure, snapshot):
    return {
        "structure": structure,
        "market": snapshot,
        "meta": {
            "assembled_by": "fake_assembler",
            "reference_date": "from_assembler",
        },
    }


def test_build_structure_market_input_prefers_canonical_legs(monkeypatch):
    structure = {
        "id": 1,
        "name": "  Estrutura Teste  ",
        "underlying_asset": "  BOVA11 ",
        "alias_legacy_aba": "  ABA_BOVA11 ",
        "legs": [
            {
                "position_side": "LONG",
                "option_type": "PUT",
                "symbol": "P1",
                "strike": 100.0,
                "expiration_date": "2026-05-15",
                "quantity": 1,
                "premium": None,
                "multiplier": 1.0,
            }
        ],
    }

    snapshot = {
        "reference_date": "2026-05-15",
        "underlying_asset": "BOVA11",
        "spot_price": 198.35,
    }

    monkeypatch.setattr(
        "services.canonical_input_service.assemble_structure_market_input",
        fake_assemble_structure_market_input,
    )

    service = CanonicalInputService(
        repository=FakeRepository(structure),
        market_snapshot_provider=FakeMarketSnapshotProvider(snapshot),
        robo_legs_service=None,
        prefer_canonical_legs=True,
        enable_legacy_legs_fallback=True,
    )

    result = service.build_structure_market_input(structure_id=1)

    assert result["structure"]["name"] == "Estrutura Teste"
    assert result["structure"]["underlying_asset"] == "BOVA11"
    assert result["structure"]["alias_legacy_aba"] == "ABA_BOVA11"
    assert result["structure"]["legs"] == structure["legs"]

    assert result["meta"]["assembled_by"] == "fake_assembler"
    assert result["meta"]["reference_date"] == "2026-05-15"
    assert result["meta"]["legs_source"] == "canonical"
    assert result["meta"]["legacy_aba"] == "ABA_BOVA11"
    assert result["meta"]["legacy_timestamp"] is None


def test_build_structure_market_input_falls_back_to_legacy_robo(monkeypatch):
    structure = {
        "id": 2,
        "name": "Estrutura Sem Legs",
        "underlying_asset": "BOVA11",
        "alias_legacy_aba": "BOVA11",
        "legs": [],
    }

    snapshot = {
        "reference_date": "2026-05-15",
        "underlying_asset": "BOVA11",
        "spot_price": 198.35,
    }

    robo_legs = [
        {
            "position_side": "long",
            "option_type": "put",
            "symbol": "BOVAM190",
            "strike": 190.0,
            "expiration_date": "2026-05-15",
            "quantity": 2000,
            "premium": None,
            "multiplier": 1.0,
        }
    ]

    def fake_to_canonical_leg(leg):
        return {
            "position_side": str(leg["position_side"]).upper(),
            "option_type": str(leg["option_type"]).upper(),
            "symbol": leg["symbol"],
            "strike": leg["strike"],
            "expiration_date": leg["expiration_date"],
            "quantity": leg["quantity"],
            "premium": leg["premium"],
            "multiplier": leg["multiplier"],
        }

    monkeypatch.setattr(
        "services.canonical_input_service.assemble_structure_market_input",
        fake_assemble_structure_market_input,
    )
    monkeypatch.setattr(
        "services.canonical_input_service.to_canonical_leg",
        fake_to_canonical_leg,
    )

    fake_robo_service = FakeRoboLegsService(
        timestamps=["2026-05-15T10:00:00", "2026-05-14T10:00:00"],
        legs=robo_legs,
    )

    service = CanonicalInputService(
        repository=FakeRepository(structure),
        market_snapshot_provider=FakeMarketSnapshotProvider(snapshot),
        robo_legs_service=fake_robo_service,
        prefer_canonical_legs=True,
        enable_legacy_legs_fallback=True,
    )

    result = service.build_structure_market_input(structure_id=2)

    assert len(result["structure"]["legs"]) == 1
    assert result["structure"]["legs"][0]["position_side"] == "LONG"
    assert result["structure"]["legs"][0]["option_type"] == "PUT"

    assert result["meta"]["legs_source"] == "legacy_robo"
    assert result["meta"]["legacy_aba"] == "BOVA11"
    assert result["meta"]["legacy_timestamp"] == "2026-05-15T10:00:00"


def test_build_structure_market_input_uses_explicit_reference_date(monkeypatch):
    structure = {
        "id": 3,
        "name": "Estrutura Ref Date",
        "underlying_asset": "BOVA11",
        "alias_legacy_aba": "BOVA11",
        "legs": [],
    }

    snapshot = {
        "reference_date": "2026-05-15",
        "underlying_asset": "BOVA11",
        "spot_price": 198.35,
    }

    market_provider = FakeMarketSnapshotProvider(snapshot)

    monkeypatch.setattr(
        "services.canonical_input_service.assemble_structure_market_input",
        fake_assemble_structure_market_input,
    )

    fake_robo_service = FakeRoboLegsService(
        timestamps=["2026-05-12T15:00:00", "2026-05-11T15:00:00"],
        legs=[],
    )

    service = CanonicalInputService(
        repository=FakeRepository(structure),
        market_snapshot_provider=market_provider,
        robo_legs_service=fake_robo_service,
        prefer_canonical_legs=False,
        enable_legacy_legs_fallback=True,
    )

    result = service.build_structure_market_input(
        structure_id=3,
        reference_date="2026-05-12",
    )

    assert market_provider.calls[0]["reference_date"] == "2026-05-12"
    assert result["meta"]["reference_date"] == "2026-05-12"
    assert result["meta"]["legacy_timestamp"] == "2026-05-12T15:00:00"


def test_build_structure_market_input_uses_name_as_legacy_aba_fallback(monkeypatch):
    structure = {
        "id": 4,
        "name": "  Minha Estrutura Legada  ",
        "underlying_asset": "BOVA11",
        "alias_legacy_aba": None,
        "legs": [],
    }

    snapshot = {
        "reference_date": "2026-05-15",
        "underlying_asset": "BOVA11",
        "spot_price": 198.35,
    }

    monkeypatch.setattr(
        "services.canonical_input_service.assemble_structure_market_input",
        fake_assemble_structure_market_input,
    )

    fake_robo_service = FakeRoboLegsService(
        timestamps=["2026-05-15T11:00:00"],
        legs=[],
    )

    service = CanonicalInputService(
        repository=FakeRepository(structure),
        market_snapshot_provider=FakeMarketSnapshotProvider(snapshot),
        robo_legs_service=fake_robo_service,
        prefer_canonical_legs=False,
        enable_legacy_legs_fallback=True,
    )

    result = service.build_structure_market_input(structure_id=4)

    assert fake_robo_service.calls[0]["aba"] == "Minha Estrutura Legada"
    assert result["meta"]["legacy_aba"] == "Minha Estrutura Legada"
    assert result["meta"]["legacy_timestamp"] == "2026-05-15T11:00:00"
    assert result["meta"]["legs_source"] == "empty"


def test_build_structure_market_input_returns_empty_when_no_legacy_timestamps(monkeypatch):
    structure = {
        "id": 5,
        "name": "Estrutura Sem Timestamp",
        "underlying_asset": "BOVA11",
        "alias_legacy_aba": "ABA_SEM_TIMESTAMP",
        "legs": [],
    }

    snapshot = {
        "reference_date": "2026-05-15",
        "underlying_asset": "BOVA11",
        "spot_price": 198.35,
    }

    monkeypatch.setattr(
        "services.canonical_input_service.assemble_structure_market_input",
        fake_assemble_structure_market_input,
    )

    fake_robo_service = FakeRoboLegsService(
        timestamps=[],
        legs=[],
    )

    service = CanonicalInputService(
        repository=FakeRepository(structure),
        market_snapshot_provider=FakeMarketSnapshotProvider(snapshot),
        robo_legs_service=fake_robo_service,
        prefer_canonical_legs=False,
        enable_legacy_legs_fallback=True,
    )

    result = service.build_structure_market_input(structure_id=5)

    assert result["structure"]["legs"] == []
    assert result["meta"]["legs_source"] == "empty"
    assert result["meta"]["legacy_aba"] == "ABA_SEM_TIMESTAMP"
    assert result["meta"]["legacy_timestamp"] is None
    assert fake_robo_service.calls == []


def test_build_structure_market_input_returns_canonical_when_fallback_disabled(monkeypatch):
    structure = {
        "id": 6,
        "name": "Estrutura Sem Fallback",
        "underlying_asset": "BOVA11",
        "alias_legacy_aba": "ABA_SEM_FALLBACK",
        "legs": [],
    }

    snapshot = {
        "reference_date": "2026-05-15",
        "underlying_asset": "BOVA11",
        "spot_price": 198.35,
    }

    monkeypatch.setattr(
        "services.canonical_input_service.assemble_structure_market_input",
        fake_assemble_structure_market_input,
    )

    fake_robo_service = FakeRoboLegsService(
        timestamps=["2026-05-15T11:00:00"],
        legs=[
            {
                "position_side": "long",
                "option_type": "put",
                "symbol": "BOVAM190",
                "strike": 190.0,
                "expiration_date": "2026-05-15",
                "quantity": 2000,
                "premium": None,
                "multiplier": 1.0,
            }
        ],
    )

    service = CanonicalInputService(
        repository=FakeRepository(structure),
        market_snapshot_provider=FakeMarketSnapshotProvider(snapshot),
        robo_legs_service=fake_robo_service,
        prefer_canonical_legs=False,
        enable_legacy_legs_fallback=False,
    )

    result = service.build_structure_market_input(structure_id=6)

    assert result["structure"]["legs"] == []
    assert result["meta"]["legs_source"] == "empty"
    assert result["meta"]["legacy_aba"] == "ABA_SEM_FALLBACK"
    assert result["meta"]["legacy_timestamp"] is None
    assert fake_robo_service.calls == []


def test_build_structure_market_input_returns_empty_when_robo_service_is_unavailable(monkeypatch):
    structure = {
        "id": 7,
        "name": "Estrutura Sem Robo",
        "underlying_asset": "BOVA11",
        "alias_legacy_aba": "ABA_SEM_ROBO",
        "legs": [],
    }

    snapshot = {
        "reference_date": "2026-05-15",
        "underlying_asset": "BOVA11",
        "spot_price": 198.35,
    }

    monkeypatch.setattr(
        "services.canonical_input_service.assemble_structure_market_input",
        fake_assemble_structure_market_input,
    )

    service = CanonicalInputService(
        repository=FakeRepository(structure),
        market_snapshot_provider=FakeMarketSnapshotProvider(snapshot),
        robo_legs_service=None,
        prefer_canonical_legs=False,
        enable_legacy_legs_fallback=True,
    )

    service.robo_legs_service = None

    result = service.build_structure_market_input(structure_id=7)

    assert result["structure"]["legs"] == []
    assert result["meta"]["legs_source"] == "empty"
    assert result["meta"]["legacy_aba"] == "ABA_SEM_ROBO"
    assert result["meta"]["legacy_timestamp"] is None
