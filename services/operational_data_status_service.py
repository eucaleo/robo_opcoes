from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

from repositories.operational_data_status_service_sql_boundary import build_operational_data_status as _boundary_build_operational_data_status
from repositories.operational_data_status_service_sql_boundary import _table_names as _boundary__table_names
from repositories.operational_data_status_service_sql_boundary import _column_names as _boundary__column_names
from repositories.operational_data_status_service_sql_boundary import _count_rows as _boundary__count_rows
from repositories.operational_data_status_service_sql_boundary import _count_distinct as _boundary__count_distinct
from repositories.operational_data_status_service_sql_boundary import _max_text as _boundary__max_text

def _coerce_operational_data_status(value):
    if isinstance(value, OperationalDataStatus):
        return value
    if hasattr(value, "__dataclass_fields__"):
        payload = {
            name: getattr(value, name)
            for name in value.__dataclass_fields__
            if hasattr(value, name)
        }
        return OperationalDataStatus(**payload)
    if isinstance(value, dict):
        return OperationalDataStatus(**value)
    return value


def build_operational_data_status(db_path):
    return _coerce_operational_data_status(
        _boundary_build_operational_data_status(db_path)
    )


def _table_names(conn):
    return _boundary__table_names(conn)


def _column_names(conn, table_name):
    return _boundary__column_names(conn, table_name)


def _count_rows(conn, table_name):
    return _boundary__count_rows(conn, table_name)


def _count_distinct(conn, table_name, column_name):
    return _boundary__count_distinct(conn, table_name, column_name)


def _max_text(conn, table_name, column_name):
    return _boundary__max_text(conn, table_name, column_name)



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


__all__ = [
    "OperationalDataStatus",
    "OperationalDataStatusService",
    "build_operational_data_status",
]
