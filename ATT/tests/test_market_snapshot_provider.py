from datetime import date

import pytest

from services.market_snapshot_provider import MarketSnapshotProvider


def test_get_snapshot_normalizes_asset_and_uses_explicit_reference_date():
    provider = MarketSnapshotProvider(
        market_by_asset={
            "BOVA11": {
                "spot_price": 198.35,
                "interest_rate": 0.1175,
                "volatility": 0.22,
            }
        }
    )

    snapshot = provider.get_snapshot("  bova11  ", reference_date="2026-05-16")

    assert snapshot == {
        "reference_date": "2026-05-16",
        "underlying_asset": "BOVA11",
        "spot_price": 198.35,
        "interest_rate": 0.1175,
        "volatility": 0.22,
    }


def test_get_snapshot_uses_today_provider_when_reference_date_is_none():
    provider = MarketSnapshotProvider(
        market_by_asset={
            "PETR4": {
                "spot_price": 37.42,
                "interest_rate": 0.1175,
                "volatility": 0.31,
            }
        },
        today_provider=lambda: date(2026, 5, 16),
    )

    snapshot = provider.get_snapshot("PETR4")

    assert snapshot["reference_date"] == "2026-05-16"
    assert snapshot["underlying_asset"] == "PETR4"
    assert snapshot["spot_price"] == 37.42
    assert snapshot["interest_rate"] == 0.1175
    assert snapshot["volatility"] == 0.31


def test_get_snapshot_raises_when_underlying_asset_is_missing():
    provider = MarketSnapshotProvider(
        market_by_asset={
            "VALE3": {
                "spot_price": 61.80,
                "interest_rate": 0.1175,
                "volatility": 0.28,
            }
        }
    )

    with pytest.raises(ValueError, match="underlying_asset is required"):
        provider.get_snapshot("   ")


def test_get_snapshot_raises_when_asset_not_found():
    provider = MarketSnapshotProvider(
        market_by_asset={
            "VALE3": {
                "spot_price": 61.80,
                "interest_rate": 0.1175,
                "volatility": 0.28,
            }
        }
    )

    with pytest.raises(ValueError, match="market snapshot not found for asset: BOVA11"):
        provider.get_snapshot("BOVA11")


def test_get_snapshot_casts_numeric_fields_to_float():
    provider = MarketSnapshotProvider(
        market_by_asset={
            "BOVA11": {
                "spot_price": "198.35",
                "interest_rate": "0.1175",
                "volatility": "0.22",
            }
        }
    )

    snapshot = provider.get_snapshot("BOVA11", reference_date="2026-05-16")

    assert snapshot["spot_price"] == 198.35
    assert snapshot["interest_rate"] == 0.1175
    assert snapshot["volatility"] == 0.22
    assert isinstance(snapshot["spot_price"], float)
    assert isinstance(snapshot["interest_rate"], float)
    assert isinstance(snapshot["volatility"], float)
