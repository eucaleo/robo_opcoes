from __future__ import annotations

import sqlite3
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

"""Boundary SQLite da Frente 59 para services.operational_data_status_service.

Este modulo concentra o acesso persistido SQLite originalmente presente no service,
sem alterar schema, persistencia ou contratos publicos.
"""


# Funcoes auxiliares copiadas para preservar comportamento local.
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

def _first_existing_name(existing_names: set[str], candidates: Iterable[str]) -> str | None:
    normalized = {name.lower(): name for name in existing_names}

    for candidate in candidates:
        found = normalized.get(candidate.lower())
        if found is not None:
            return found

    return None

def _latest_text_value(values: Iterable[str | None]) -> str | None:
    available = [value for value in values if value]
    if not available:
        return None
    return max(available)

def _quote_identifier(value: str) -> str:
    return '"' + value.replace('"', '""') + '"'



# Funcoes/metodos movidos do service.


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


def _table_names(conn: sqlite3.Connection) -> set[str]:
    rows = conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        """
    ).fetchall()
    return {str(row[0]) for row in rows}


def _column_names(conn: sqlite3.Connection, table_name: str) -> set[str]:
    rows = conn.execute(
        "PRAGMA table_info(" + _quote_identifier(table_name) + ")"
    ).fetchall()
    return {str(row[1]) for row in rows}


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
