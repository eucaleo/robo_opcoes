from pathlib import Path
import sqlite3
import sys


ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from services.rtd_option_quotes_intraday_history_service import (
    RtdOptionQuotesIntradayHistoryService,
)
from services.rtd_option_quotes_intraday_candle_service import (
    RtdOptionQuotesIntradayCandleService,
)


def test_capture_maps_ultimo_preco_to_history_last(tmp_path):
    db_path = tmp_path / "app.db"

    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        create table rtd_option_quotes (
            codigo_opcao text,
            ultimo_preco real,
            bid real,
            ask real,
            vwap real,
            volume real,
            updated_at text
        )
        """
    )
    conn.execute(
        """
        insert into rtd_option_quotes (
            codigo_opcao,
            ultimo_preco,
            bid,
            ask,
            vwap,
            volume,
            updated_at
        ) values (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "BOVAT158",
            0.59,
            0.58,
            0.60,
            0.65,
            52621.8,
            "2026-06-29 16:24:50",
        ),
    )
    conn.commit()
    conn.close()

    service = RtdOptionQuotesIntradayHistoryService(db_path=db_path)

    captured = service.capture_snapshot(
        captured_at="2026-07-11T21:00:00+00:00"
    )

    assert captured == 1

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        """
        select codigo_opcao, last, bid, ask, vwap, volume, source_updated_at
        from rtd_option_quotes_intraday_history
        """
    ).fetchone()
    conn.close()

    assert row["codigo_opcao"] == "BOVAT158"
    assert row["last"] == 0.59
    assert row["bid"] == 0.58
    assert row["ask"] == 0.60
    assert row["vwap"] == 0.65
    assert row["volume"] == 52621.8
    assert row["source_updated_at"] == "2026-06-29 16:24:50"


def test_candle_service_uses_history_last_before_mid_price():
    service = RtdOptionQuotesIntradayCandleService()

    candles = service.aggregate_points(
        [
            {
                "codigo_opcao": "BOVAT158",
                "captured_at": "2026-07-11T21:00:05+00:00",
                "last": 0.59,
                "bid": 0.50,
                "ask": 0.70,
                "vwap": 0.65,
                "volume": 100.0,
            }
        ],
        interval_minutes=1,
    )

    assert len(candles) == 1

    candle = candles[0]

    assert candle["symbol"] == "BOVAT158"
    assert candle["open_price"] == 0.59
    assert candle["high_price"] == 0.59
    assert candle["low_price"] == 0.59
    assert candle["close_price"] == 0.59
    assert candle["price_source"] == "last_trade"


def test_capture_default_captured_at_uses_sao_paulo_timezone(tmp_path):
    db_path = tmp_path / "app.db"

    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        create table rtd_option_quotes (
            codigo_opcao text,
            ultimo_preco real,
            bid real,
            ask real,
            vwap real,
            volume real,
            updated_at text
        )
        """
    )
    conn.execute(
        """
        insert into rtd_option_quotes (
            codigo_opcao,
            ultimo_preco,
            bid,
            ask,
            vwap,
            volume,
            updated_at
        ) values (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "PRIOT690",
            11.88,
            0.0,
            0.0,
            0.0,
            0.0,
            "2026-07-11T18:14:15",
        ),
    )
    conn.commit()
    conn.close()

    service = RtdOptionQuotesIntradayHistoryService(db_path=db_path)

    captured = service.capture_snapshot()

    assert captured == 1

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        """
        select captured_at, codigo_opcao, last, source_updated_at
        from rtd_option_quotes_intraday_history
        """
    ).fetchone()
    conn.close()

    assert row["codigo_opcao"] == "PRIOT690"
    assert row["last"] == 11.88
    assert row["source_updated_at"] == "2026-07-11T18:14:15"
    assert row["captured_at"].endswith("-03:00")
