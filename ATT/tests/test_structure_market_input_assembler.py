import pytest

from services.structure_market_input_assembler import assemble_structure_market_input


def test_assemble_structure_market_input_returns_structure_market_and_meta(monkeypatch):
    structure = {
        "structure_id": 123,
        "name": "Fence BOVA11",
        "underlying_asset": "BOVA11",
        "alias_legacy_aba": "BOVA11",
        "legs": [],
    }

    market_snapshot = {
        "reference_date": "2026-05-16",
        "underlying_asset": "BOVA11",
        "spot_price": 198.35,
        "interest_rate": 0.1175,
        "volatility": 0.22,
    }

    def fake_to_structure_input(value):
        return {
            "structure_id": value["structure_id"],
            "name": value["name"],
            "underlying_asset": value["underlying_asset"],
            "alias_legacy_aba": value["alias_legacy_aba"],
            "legs": value["legs"],
        }

    monkeypatch.setattr(
        "services.structure_market_input_assembler.to_structure_input",
        fake_to_structure_input,
    )

    result = assemble_structure_market_input(structure, market_snapshot)

    assert result == {
        "structure": {
            "structure_id": 123,
            "name": "Fence BOVA11",
            "underlying_asset": "BOVA11",
            "alias_legacy_aba": "BOVA11",
            "legs": [],
        },
        "market": {
            "reference_date": "2026-05-16",
            "underlying_asset": "BOVA11",
            "spot_price": 198.35,
            "interest_rate": 0.1175,
            "volatility": 0.22,
        },
        "meta": {
            "input_source": "structure_market_input_assembler",
        },
    }


def test_assemble_structure_market_input_raises_when_structure_missing():
    with pytest.raises(ValueError, match="structure is required"):
        assemble_structure_market_input({}, {"underlying_asset": "BOVA11"})


def test_assemble_structure_market_input_raises_when_market_snapshot_missing():
    with pytest.raises(ValueError, match="market_snapshot is required"):
        assemble_structure_market_input({"structure_id": 1}, {})


def test_assemble_structure_market_input_raises_on_underlying_asset_mismatch(monkeypatch):
    structure = {
        "structure_id": 123,
        "name": "Fence BOVA11",
        "underlying_asset": "BOVA11",
        "legs": [],
    }

    market_snapshot = {
        "reference_date": "2026-05-16",
        "underlying_asset": "PETR4",
        "spot_price": 37.42,
        "interest_rate": 0.1175,
        "volatility": 0.31,
    }

    def fake_to_structure_input(value):
        return {
            "structure_id": value["structure_id"],
            "name": value["name"],
            "underlying_asset": value["underlying_asset"],
            "legs": value["legs"],
        }

    monkeypatch.setattr(
        "services.structure_market_input_assembler.to_structure_input",
        fake_to_structure_input,
    )

    with pytest.raises(
        ValueError,
        match="underlying_asset mismatch: structure=BOVA11 market=PETR4",
    ):
        assemble_structure_market_input(structure, market_snapshot)
