from __future__ import annotations

from pathlib import Path

from repositories.rtd_option_quotes_intraday_candle_repository import (
    RtdOptionQuotesIntradayCandleRepository,
)
from services.rtd_option_quotes_intraday_candle_chart_service import (
    RtdOptionQuotesIntradayCandleChartService,
)


def test_intraday_candle_chart_service_returns_ordered_vwap_price_series(tmp_path: Path):
    db_path = tmp_path / "app.db"

    repo = RtdOptionQuotesIntradayCandleRepository(db_path)
    repo.upsert_many(
        [
            {
                "interval_minutes": 1,
                "bucket_start": "2026-07-12T10:01:00",
                "symbol": "PETRA100",
                "open_price": 1.10,
                "high_price": 1.20,
                "low_price": 1.05,
                "close_price": 1.15,
                "vwap": 1.13,
                "bid": 1.14,
                "ask": 1.16,
                "spread": 0.02,
                "volume_delta": None,
                "updates_count": 3,
                "price_source": "last_trade",
            },
            {
                "interval_minutes": 1,
                "bucket_start": "2026-07-12T10:00:00",
                "symbol": "PETRA100",
                "open_price": 1.00,
                "high_price": 1.08,
                "low_price": 0.98,
                "close_price": 1.05,
                "vwap": 1.03,
                "bid": 1.04,
                "ask": 1.06,
                "spread": 0.02,
                "volume_delta": None,
                "updates_count": 2,
                "price_source": "last_trade",
            },
        ]
    )

    service = RtdOptionQuotesIntradayCandleChartService(db_path)

    series = service.get_vwap_price_series(
        symbol="PETRA100",
        interval_minutes=1,
    )

    assert [point["timestamp"] for point in series] == [
        "2026-07-12T10:00:00",
        "2026-07-12T10:01:00",
    ]
    assert [point["price"] for point in series] == [1.05, 1.15]
    assert [point["vwap"] for point in series] == [1.03, 1.13]
    assert all(
        point["source_table"] == "rtd_option_quotes_intraday_candles"
        for point in series
    )


def test_dark_ui_panel_references_intraday_candle_chart_service():
    panel_path = Path("UI/components/terminal_vwap_payoff_dark_panel.py")
    text = panel_path.read_text(encoding="utf-8")

    assert "RtdOptionQuotesIntradayCandleChartService" in text
    assert "rtd_option_quotes_intraday_candles" in text
    assert "_market_with_intraday_candle_series" in text
