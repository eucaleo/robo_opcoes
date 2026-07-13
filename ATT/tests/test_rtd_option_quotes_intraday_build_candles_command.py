import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory

from repositories.rtd_option_quotes_intraday_candle_repository import (
    RtdOptionQuotesIntradayCandleRepository,
)
from scripts.rtd_option_quotes_intraday_build_candles import main


def criar_historico(db_path: Path) -> None:
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        create table rtd_option_quotes_intraday_history (
            captured_at text,
            symbol text,
            ultimo_preco real,
            bid real,
            ask real,
            vwap real,
            volume real
        )
        """
    )
    conn.executemany(
        """
        insert into rtd_option_quotes_intraday_history (
            captured_at, symbol, ultimo_preco, bid, ask, vwap, volume
        ) values (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            ("2026-07-10T10:15:05", "PETRA300", 10.0, 9.9, 10.1, 9.95, 100),
            ("2026-07-10T10:15:50", "PETRA300", 11.0, 10.9, 11.1, 10.50, 150),
        ],
    )
    conn.commit()
    conn.close()


def test_dry_run_nao_grava(capsys):
    with TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "dry_run.sqlite"
        criar_historico(db_path)

        result = main(["--db", str(db_path), "--dry-run"])
        out = capsys.readouterr().out

        assert result == 0
        assert "candles_calculados=1" in out
        assert "dry_run=sim" in out

        repo = RtdOptionQuotesIntradayCandleRepository(db_path)
        assert repo.list_candles() == []


def test_comando_grava_candle(capsys):
    with TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "persist.sqlite"
        criar_historico(db_path)

        result = main(["--db", str(db_path), "--interval-minutes", "1"])
        out = capsys.readouterr().out

        assert result == 0
        assert "candles_calculados=1" in out
        assert "candles_gravados=1" in out

        repo = RtdOptionQuotesIntradayCandleRepository(db_path)
        rows = repo.list_candles("PETRA300", 1)

        assert len(rows) == 1
        assert rows[0]["open_price"] == 10.0
        assert rows[0]["close_price"] == 11.0
