from __future__ import annotations

import sqlite3
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable


SNAPSHOT_TABLE_CANDIDATES = (
    "rtd_option_quotes",
)

INTRADAY_TABLE_CANDIDATES = (
    "rtd_option_quotes_intraday_history",
    "rtd_option_quotes_intraday",
)

CANDLE_TABLE_CANDIDATES = (
    "rtd_option_quotes_intraday_candles",
    "rtd_option_quotes_intraday_candle",
    "rtd_option_quotes_candles",
)

SYMBOL_COLUMN_CANDIDATES = (
    "codigo_opcao",
    "symbol",
    "ticker",
    "option_symbol",
    "asset",
)

UPDATED_AT_COLUMN_CANDIDATES = (
    "updated_at",
    "captured_at",
    "timestamp",
    "ts",
    "datetime",
    "created_at",
    "data_hora",
    "time",
)


@dataclass(frozen=True)
class OperationalDataStatus:
    database_path: str
    database_exists: bool
    source: str
    status: str

    snapshot_table: str | None = None
    intraday_table: str | None = None
    candle_table: str | None = None

    snapshot_available: bool = False
    intraday_available: bool = False
    candles_available: bool = False

    snapshot_symbols_count: int = 0
    intraday_rows_count: int = 0
    candles_count: int = 0

    latest_snapshot_update: str | None = None
    latest_intraday_update: str | None = None
    latest_candle_update: str | None = None
    latest_update: str | None = None

    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class _TableSummary:
    table_name: str | None
    available: bool
    rows_count: int
    distinct_symbols_count: int
    latest_update: str | None


class OperationalDataStatusService:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)

    def get_status(self) -> OperationalDataStatus:
        return build_operational_data_status(self.db_path)


def build_operational_data_status(db_path: str | Path) -> OperationalDataStatus:
    path = Path(db_path)
    source = "sqlite:" + str(path)

    if not path.exists():
        return OperationalDataStatus(
            database_path=str(path),
            database_exists=False,
            source=source,
            status="database_missing",
            errors=["database_file_not_found"],
        )

    errors: list[str] = []

    try:
        with sqlite3.connect(str(path)) as conn:
            table_names = _table_names(conn)

            snapshot = _summarize_first_existing_table(
                conn=conn,
                table_names=table_names,
                candidates=SNAPSHOT_TABLE_CANDIDATES,
                count_distinct_symbols=True,
            )
            intraday = _summarize_first_existing_table(
                conn=conn,
                table_names=table_names,
                candidates=INTRADAY_TABLE_CANDIDATES,
                count_distinct_symbols=False,
            )
            candles = _summarize_first_existing_table(
                conn=conn,
                table_names=table_names,
                candidates=CANDLE_TABLE_CANDIDATES,
                count_distinct_symbols=False,
            )

    except sqlite3.Error as exc:
        return OperationalDataStatus(
            database_path=str(path),
            database_exists=True,
            source=source,
            status="sqlite_error",
            errors=[str(exc)],
        )

    latest_update = _latest_text_value(
        (
            snapshot.latest_update,
            intraday.latest_update,
            candles.latest_update,
        )
    )

    status = _overall_status(
        snapshot_available=snapshot.available,
        intraday_available=intraday.available,
        candles_available=candles.available,
    )

    return OperationalDataStatus(
        database_path=str(path),
        database_exists=True,
        source=source,
        status=status,
        snapshot_table=snapshot.table_name,
        intraday_table=intraday.table_name,
        candle_table=candles.table_name,
        snapshot_available=snapshot.available,
        intraday_available=intraday.available,
        candles_available=candles.available,
        snapshot_symbols_count=snapshot.distinct_symbols_count,
        intraday_rows_count=intraday.rows_count,
        candles_count=candles.rows_count,
        latest_snapshot_update=snapshot.latest_update,
        latest_intraday_update=intraday.latest_update,
        latest_candle_update=candles.latest_update,
        latest_update=latest_update,
        errors=errors,
    )


def _overall_status(
    *,
    snapshot_available: bool,
    intraday_available: bool,
    candles_available: bool,
) -> str:
    flags = (snapshot_available, intraday_available, candles_available)

    if all(flags):
        return "ok"

    if any(flags):
        return "partial"

    return "empty"


def _table_names(conn: sqlite3.Connection) -> set[str]:
    rows = conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        """
    ).fetchall()
    return {str(row[0]) for row in rows}


def _summarize_first_existing_table(
    *,
    conn: sqlite3.Connection,
    table_names: set[str],
    candidates: Iterable[str],
    count_distinct_symbols: bool,
) -> _TableSummary:
    table_name = _first_existing_name(table_names, candidates)

    if table_name is None:
        return _TableSummary(
            table_name=None,
            available=False,
            rows_count=0,
            distinct_symbols_count=0,
            latest_update=None,
        )

    columns = _column_names(conn, table_name)
    rows_count = _count_rows(conn, table_name)
    symbol_column = _first_existing_name(columns, SYMBOL_COLUMN_CANDIDATES)
    updated_at_column = _first_existing_name(columns, UPDATED_AT_COLUMN_CANDIDATES)

    distinct_symbols_count = rows_count
    if count_distinct_symbols and symbol_column is not None:
        distinct_symbols_count = _count_distinct(conn, table_name, symbol_column)

    latest_update = None
    if updated_at_column is not None:
        latest_update = _max_text(conn, table_name, updated_at_column)

    return _TableSummary(
        table_name=table_name,
        available=rows_count > 0,
        rows_count=rows_count,
        distinct_symbols_count=distinct_symbols_count,
        latest_update=latest_update,
    )


def _column_names(conn: sqlite3.Connection, table_name: str) -> set[str]:
    rows = conn.execute(
        "PRAGMA table_info(" + _quote_identifier(table_name) + ")"
    ).fetchall()
    return {str(row[1]) for row in rows}


def _first_existing_name(existing_names: set[str], candidates: Iterable[str]) -> str | None:
    normalized = {name.lower(): name for name in existing_names}

    for candidate in candidates:
        found = normalized.get(candidate.lower())
        if found is not None:
            return found

    return None


def _count_rows(conn: sqlite3.Connection, table_name: str) -> int:
    row = conn.execute(
        "SELECT COUNT(*) FROM " + _quote_identifier(table_name)
    ).fetchone()
    return int(row[0] or 0)


def _count_distinct(conn: sqlite3.Connection, table_name: str, column_name: str) -> int:
    row = conn.execute(
        "SELECT COUNT(DISTINCT "
        + _quote_identifier(column_name)
        + ") FROM "
        + _quote_identifier(table_name)
    ).fetchone()
    return int(row[0] or 0)


def _max_text(conn: sqlite3.Connection, table_name: str, column_name: str) -> str | None:
    row = conn.execute(
        "SELECT MAX("
        + _quote_identifier(column_name)
        + ") FROM "
        + _quote_identifier(table_name)
    ).fetchone()

    if row is None or row[0] is None:
        return None

    return str(row[0])


def _latest_text_value(values: Iterable[str | None]) -> str | None:
    available = [value for value in values if value]
    if not available:
        return None
    return max(available)


def _quote_identifier(value: str) -> str:
    return '"' + value.replace('"', '""') + '"'


__all__ = [
    "OperationalDataStatus",
    "OperationalDataStatusService",
    "build_operational_data_status",
]
