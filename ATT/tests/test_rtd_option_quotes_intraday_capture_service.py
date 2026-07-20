import inspect
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from repositories.rtd_option_quotes_intraday_history_repository import (
    RtdOptionQuotesIntradayHistoryRepository,
)
from services import rtd_option_quotes_intraday_history_service
from services.rtd_option_quotes_intraday_history_service import (
    RtdOptionQuotesIntradayHistoryService,
)


def test_intraday_capture_service_captures_from_rtd_option_quotes_snapshot(tmp_path):
    db_path = tmp_path / "app.db"

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE rtd_option_quotes (
                codigo_opcao TEXT NOT NULL,
                bid REAL,
                ask REAL,
                last REAL,
                vwap REAL,
                volume REAL,
                updated_at TEXT
            )
            """
        )
        conn.execute(
            """
            INSERT INTO rtd_option_quotes (
                codigo_opcao, bid, ask, last, vwap, volume, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "PETRA123",
                1.10,
                1.20,
                1.15,
                1.14,
                100,
                "2026-07-10T09:59:59-03:00",
            ),
        )
        conn.execute(
            """
            INSERT INTO rtd_option_quotes (
                codigo_opcao, bid, ask, last, vwap, volume, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "VALEA456",
                2.10,
                2.20,
                2.15,
                2.14,
                200,
                "2026-07-10T09:59:59-03:00",
            ),
        )

    repo = RtdOptionQuotesIntradayHistoryRepository(db_path)
    service = RtdOptionQuotesIntradayHistoryService(
        db_path=db_path,
        history_repository=repo,
    )

    captured_count = service.capture_snapshot(
        captured_at="2026-07-10T10:00:00-03:00"
    )

    assert captured_count == 2

    petra_rows = repo.list_by_codigo_opcao("PETRA123")

    assert len(petra_rows) == 1
    assert petra_rows[0]["captured_at"] == "2026-07-10T10:00:00-03:00"
    assert petra_rows[0]["bid"] == 1.10
    assert petra_rows[0]["ask"] == 1.20
    assert petra_rows[0]["last"] == 1.15
    assert petra_rows[0]["vwap"] == 1.14
    assert petra_rows[0]["volume"] == 100


def test_intraday_capture_service_returns_zero_when_snapshot_table_is_missing(tmp_path):
    db_path = tmp_path / "app.db"

    service = RtdOptionQuotesIntradayHistoryService(db_path=db_path)

    assert service.capture_snapshot(captured_at="2026-07-10T10:00:00-03:00") == 0


def test_intraday_capture_service_has_no_excel_or_external_process_dependency():
    source = inspect.getsource(rtd_option_quotes_intraday_history_service).lower()

    forbidden_terms = [
        "sub" + "process",
        "win32" + "com",
        "xl" + "wings",
        "." + "work" + "books",
        "." + "sheets",
    ]

    for term in forbidden_terms:
        assert term not in source
