import pytest

from services.rtd_option_quotes_intraday_candle_service import (
    RtdOptionQuotesIntradayCandleService,
)


def test_aggregacao_um_minuto():
    service = RtdOptionQuotesIntradayCandleService()
    points = [
        {
            "captured_at": "2026-07-10T10:15:05",
            "symbol": "PETRA300",
            "ultimo_preco": 10.0,
            "bid": 9.9,
            "ask": 10.1,
            "vwap": 9.95,
            "volume": 100,
        },
        {
            "captured_at": "2026-07-10T10:15:30",
            "symbol": "PETRA300",
            "ultimo_preco": 12.0,
            "bid": 11.9,
            "ask": 12.1,
            "vwap": 10.50,
            "volume": 150,
        },
        {
            "captured_at": "2026-07-10T10:15:55",
            "symbol": "PETRA300",
            "ultimo_preco": 11.0,
            "bid": 10.9,
            "ask": 11.1,
            "vwap": 10.80,
            "volume": 190,
        },
    ]

    candles = service.aggregate_points(points, interval_minutes=1)

    assert len(candles) == 1
    candle = candles[0]
    assert candle["bucket_start"] == "2026-07-10T10:15:00"
    assert candle["open_price"] == 10.0
    assert candle["high_price"] == 12.0
    assert candle["low_price"] == 10.0
    assert candle["close_price"] == 11.0
    assert candle["vwap"] == 10.80
    assert candle["volume_delta"] == 90.0
    assert candle["updates_count"] == 3
    assert candle["price_source"] == "last_trade"


def test_mid_price_quando_sem_ultimo_preco():
    service = RtdOptionQuotesIntradayCandleService()
    points = [
        {
            "captured_at": "2026-07-10T10:16:05",
            "symbol": "PETRA300",
            "ultimo_preco": None,
            "bid": 9.0,
            "ask": 11.0,
            "vwap": 10.0,
            "volume": 100,
        }
    ]

    candles = service.aggregate_points(points, interval_minutes=1)

    assert len(candles) == 1
    assert candles[0]["open_price"] == 10.0
    assert candles[0]["close_price"] == 10.0
    assert candles[0]["price_source"] == "mid_price"


def test_intervalo_invalido():
    service = RtdOptionQuotesIntradayCandleService()

    with pytest.raises(ValueError):
        service.aggregate_points([], interval_minutes=2)
