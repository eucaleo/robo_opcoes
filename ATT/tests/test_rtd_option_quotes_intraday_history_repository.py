import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from repositories.rtd_option_quotes_intraday_history_repository import (
    RtdOptionQuotesIntradayHistoryRepository,
)


def test_intraday_history_repository_appends_same_option_in_different_times(tmp_path):
    db_path = tmp_path / "app.db"
    repo = RtdOptionQuotesIntradayHistoryRepository(db_path)

    repo.insert_sample(
        {
            "captured_at": "2026-07-10T10:00:00-03:00",
            "codigo_opcao": "PETRA123",
            "bid": 1.10,
            "ask": 1.20,
            "last": 1.15,
            "vwap": 1.14,
            "volume": 100,
            "source_updated_at": "2026-07-10T09:59:59-03:00",
            "raw_payload": {"origem": "snapshot"},
        }
    )
    repo.insert_sample(
        {
            "captured_at": "2026-07-10T10:01:00-03:00",
            "codigo_opcao": "PETRA123",
            "bid": 1.11,
            "ask": 1.21,
            "last": 1.16,
            "vwap": 1.15,
            "volume": 120,
            "source_updated_at": "2026-07-10T10:00:59-03:00",
            "raw_payload": {"origem": "snapshot"},
        }
    )

    rows = repo.list_by_codigo_opcao("PETRA123")

    assert len(rows) == 2
    assert rows[0]["captured_at"] == "2026-07-10T10:00:00-03:00"
    assert rows[1]["captured_at"] == "2026-07-10T10:01:00-03:00"
    assert rows[0]["codigo_opcao"] == "PETRA123"
    assert repo.count() == 2


def test_intraday_history_repository_filters_by_interval_and_codigo(tmp_path):
    db_path = tmp_path / "app.db"
    repo = RtdOptionQuotesIntradayHistoryRepository(db_path)

    repo.insert_sample(
        {
            "captured_at": "2026-07-10T10:00:00-03:00",
            "codigo_opcao": "PETRA123",
            "last": 1.10,
        }
    )
    repo.insert_sample(
        {
            "captured_at": "2026-07-10T10:05:00-03:00",
            "codigo_opcao": "PETRA123",
            "last": 1.15,
        }
    )
    repo.insert_sample(
        {
            "captured_at": "2026-07-10T10:05:00-03:00",
            "codigo_opcao": "VALEA456",
            "last": 2.15,
        }
    )

    rows = repo.list_by_interval(
        "2026-07-10T10:01:00-03:00",
        "2026-07-10T10:06:00-03:00",
        codigo_opcao="PETRA123",
    )

    assert len(rows) == 1
    assert rows[0]["codigo_opcao"] == "PETRA123"
    assert rows[0]["last"] == 1.15
    assert json.loads(rows[0]["raw_payload_json"])["codigo_opcao"] == "PETRA123"
