from pathlib import Path
from tempfile import TemporaryDirectory

from repositories.rtd_option_quotes_intraday_candle_repository import (
    RtdOptionQuotesIntradayCandleRepository,
)


def test_schema():
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "candles.sqlite"
        repo = RtdOptionQuotesIntradayCandleRepository(path)

        columns = repo.schema_columns()

        expected = [
            "id",
            "interval_minutes",
            "bucket_start",
            "symbol",
            "open_price",
            "high_price",
            "low_price",
            "close_price",
            "vwap",
            "bid",
            "ask",
            "spread",
            "volume_delta",
            "updates_count",
            "price_source",
            "created_at",
            "updated_at",
        ]

        assert all(column in columns for column in expected)


def test_upsert_idempotente():
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "candles.sqlite"
        repo = RtdOptionQuotesIntradayCandleRepository(path)

        candle = {
            "interval_minutes": 1,
            "bucket_start": "2026-07-10T10:15:00",
            "symbol": "PETRA300",
            "open_price": 1.0,
            "high_price": 1.2,
            "low_price": 0.9,
            "close_price": 1.1,
            "vwap": 1.05,
            "bid": 1.0,
            "ask": 1.2,
            "spread": 0.2,
            "volume_delta": 100.0,
            "updates_count": 3,
            "price_source": "last_trade",
        }

        repo.upsert_many([candle])
        repo.upsert_many([{**candle, "close_price": 1.15}])

        rows = repo.list_candles("PETRA300", 1)

        assert len(rows) == 1
        assert rows[0]["close_price"] == 1.15
