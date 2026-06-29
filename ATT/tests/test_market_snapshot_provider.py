from datetime import date
import sqlite3

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


def test_get_snapshot_reads_rtd_underlying_quotes_with_vwap(tmp_path):
    db_path = tmp_path / "app.db"

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE rtd_underlying_quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ativo TEXT NOT NULL UNIQUE,
                ultimo_preco REAL,
                vwap REAL,
                bid REAL,
                ask REAL,
                close_price REAL,
                prev_close REAL,
                open_price REAL,
                high_price REAL,
                low_price REAL,
                volume REAL,
                change_percent REAL,
                source TEXT,
                updated_at TEXT,
                created_at TEXT
            )
            """
        )
        conn.execute(
            """
            INSERT INTO rtd_underlying_quotes (
                ativo,
                ultimo_preco,
                vwap,
                source,
                updated_at,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "PETR4",
                37.42,
                37.10,
                "btg_rtd_excel_underlying",
                "2026-06-29 16:00:00",
                "2026-06-29 16:00:00",
            ),
        )

    provider = MarketSnapshotProvider(
        db_path=db_path,
        today_provider=lambda: date(2026, 6, 29),
    )

    snapshot = provider.get_snapshot(" petr4 ")

    assert snapshot["reference_date"] == "2026-06-29"
    assert snapshot["underlying_asset"] == "PETR4"
    assert snapshot["spot_price"] == 37.42
    assert snapshot["vwap"] == 37.10
    assert snapshot["interest_rate"] == 0.1175
    assert snapshot["volatility"] == 0.31
    assert snapshot["snapshot_source"] == "rtd_underlying_quotes"
    assert snapshot["market_snapshot_source"] == "rtd_underlying_quotes"
    assert snapshot["is_static_fallback"] is False
    assert snapshot["is_current_market"] is True
    assert snapshot["snapshot_warning"] is None
    assert snapshot["market_snapshot_updated_at"] == "2026-06-29 16:00:00"
    assert snapshot["market_snapshot_rtd_source"] == "btg_rtd_excel_underlying"


def test_get_snapshot_handles_legacy_rtd_underlying_quotes_without_vwap(tmp_path):
    db_path = tmp_path / "app.db"

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE rtd_underlying_quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ativo TEXT NOT NULL UNIQUE,
                ultimo_preco REAL,
                bid REAL,
                ask REAL,
                close_price REAL,
                prev_close REAL,
                open_price REAL,
                high_price REAL,
                low_price REAL,
                volume REAL,
                change_percent REAL,
                source TEXT,
                updated_at TEXT,
                created_at TEXT
            )
            """
        )
        conn.execute(
            """
            INSERT INTO rtd_underlying_quotes (
                ativo,
                ultimo_preco,
                source,
                updated_at,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                "BOVA11",
                198.35,
                "btg_rtd_excel_underlying",
                "2026-06-29 16:00:00",
                "2026-06-29 16:00:00",
            ),
        )

    provider = MarketSnapshotProvider(
        db_path=db_path,
        today_provider=lambda: date(2026, 6, 29),
    )

    snapshot = provider.get_snapshot("BOVA11")

    assert snapshot["spot_price"] == 198.35
    assert snapshot["vwap"] is None
    assert snapshot["snapshot_source"] == "rtd_underlying_quotes"
