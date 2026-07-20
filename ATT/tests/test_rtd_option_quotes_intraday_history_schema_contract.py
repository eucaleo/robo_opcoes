import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from repositories.rtd_option_quotes_intraday_history_repository import (
    RtdOptionQuotesIntradayHistoryRepository,
)


def test_rtd_option_quotes_intraday_history_schema_contract(tmp_path):
    db_path = tmp_path / "app.db"
    repo = RtdOptionQuotesIntradayHistoryRepository(db_path)

    repo.ensure_schema()

    with sqlite3.connect(db_path) as conn:
        columns = {
            row[1]
            for row in conn.execute(
                "PRAGMA table_info(rtd_option_quotes_intraday_history)"
            ).fetchall()
        }

        indexes = {
            row[1]
            for row in conn.execute(
                "PRAGMA index_list(rtd_option_quotes_intraday_history)"
            ).fetchall()
        }

    assert {
        "id",
        "captured_at",
        "codigo_opcao",
        "bid",
        "ask",
        "last",
        "vwap",
        "volume",
        "source_updated_at",
        "raw_payload_json",
        "created_at",
    }.issubset(columns)

    assert "idx_rtd_option_quotes_intraday_history_codigo_captured_at" in indexes
    assert "idx_rtd_option_quotes_intraday_history_captured_at" in indexes
