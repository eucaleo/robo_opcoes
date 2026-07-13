from services.rtd_option_quotes_intraday_candle_service import (
    RtdOptionQuotesIntradayCandleService,
)


def test_candles_normalizam_offsets_para_horario_sao_paulo():
    service = RtdOptionQuotesIntradayCandleService()

    points = [
        {
            "codigo_opcao": "BOVAG34",
            "captured_at": "2026-07-11T18:22:27.276118-03:00",
            "last": 10.0,
        },
        {
            "codigo_opcao": "BOVAG34",
            "captured_at": "2026-07-11T21:22:45.276118+00:00",
            "last": 12.0,
        },
    ]

    candles = service.aggregate_points(points, interval_minutes=1)

    assert len(candles) == 1
    assert candles[0]["bucket_start"] == "2026-07-11T18:22:00"
    assert candles[0]["open_price"] == 10.0
    assert candles[0]["close_price"] == 12.0
    assert candles[0]["updates_count"] == 2


def test_timestamp_z_tambem_e_convertido_para_horario_sao_paulo():
    service = RtdOptionQuotesIntradayCandleService()

    points = [
        {
            "codigo_opcao": "BOVAG34",
            "captured_at": "2026-07-11T21:05:03Z",
            "last": 10.0,
        },
    ]

    candles = service.aggregate_points(points, interval_minutes=1)

    assert len(candles) == 1
    assert candles[0]["bucket_start"] == "2026-07-11T18:05:00"
