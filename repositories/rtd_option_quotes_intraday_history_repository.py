"""Repository do historico intraday de rtd_option_quotes.

Fase 3 - Historico intraday RTD Online.

Responsabilidades:
- manter schema separado do snapshot rtd_option_quotes;
- inserir amostras temporais;
- consultar por codigo_opcao;
- consultar por intervalo;
- nao acessar Excel;
- nao depender de automacao externa;
- nao agregar serie temporal nesta etapa.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


class RtdOptionQuotesIntradayHistoryRepository:
    """Persistencia append-only do historico intraday de option quotes."""

    TABLE_NAME = "rtd_option_quotes_intraday_history"

    def __init__(self, db_path: str | Path = "dados/app.db") -> None:
        self.db_path = str(db_path)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def ensure_schema(self) -> None:
        """Cria o schema minimo do historico intraday se ainda nao existir."""
        with self._connect() as conn:
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    captured_at TEXT NOT NULL,
                    codigo_opcao TEXT NOT NULL,
                    bid REAL,
                    ask REAL,
                    last REAL,
                    vwap REAL,
                    volume REAL,
                    source_updated_at TEXT,
                    raw_payload_json TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                f"""
                CREATE INDEX IF NOT EXISTS
                idx_{self.TABLE_NAME}_codigo_captured_at
                ON {self.TABLE_NAME} (codigo_opcao, captured_at)
                """
            )
            conn.execute(
                f"""
                CREATE INDEX IF NOT EXISTS
                idx_{self.TABLE_NAME}_captured_at
                ON {self.TABLE_NAME} (captured_at)
                """
            )

    def insert_sample(self, sample: dict[str, Any]) -> int:
        """Insere uma amostra historica e retorna o id gerado."""
        self.ensure_schema()

        captured_at = self._as_text_datetime(
            sample.get("captured_at") or datetime.now(timezone.utc)
        )
        codigo_opcao = str(sample.get("codigo_opcao") or "").strip()

        if not codigo_opcao:
            raise ValueError("codigo_opcao e obrigatorio para historico intraday")

        raw_payload_json = sample.get("raw_payload_json")
        if raw_payload_json is None:
            raw_payload_json = json.dumps(
                sample.get("raw_payload", sample),
                ensure_ascii=False,
                sort_keys=True,
                default=str,
            )

        with self._connect() as conn:
            cursor = conn.execute(
                f"""
                INSERT INTO {self.TABLE_NAME} (
                    captured_at,
                    codigo_opcao,
                    bid,
                    ask,
                    last,
                    vwap,
                    volume,
                    source_updated_at,
                    raw_payload_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    captured_at,
                    codigo_opcao,
                    self._as_float_or_none(sample.get("bid")),
                    self._as_float_or_none(sample.get("ask")),
                    self._as_float_or_none(sample.get("last")),
                    self._as_float_or_none(sample.get("vwap")),
                    self._as_float_or_none(sample.get("volume")),
                    self._as_text_or_none(sample.get("source_updated_at")),
                    raw_payload_json,
                ),
            )
            return int(cursor.lastrowid)

    def insert_samples(self, samples: Iterable[dict[str, Any]]) -> int:
        """Insere multiplas amostras e retorna a quantidade inserida."""
        count = 0
        for sample in samples:
            self.insert_sample(sample)
            count += 1
        return count

    def list_by_codigo_opcao(
        self,
        codigo_opcao: str,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """Lista historico de uma opcao ordenado pelo horario de captura."""
        self.ensure_schema()

        sql = f"""
            SELECT *
            FROM {self.TABLE_NAME}
            WHERE codigo_opcao = ?
            ORDER BY captured_at ASC, id ASC
        """
        params: list[Any] = [codigo_opcao]

        if limit is not None:
            sql += " LIMIT ?"
            params.append(int(limit))

        with self._connect() as conn:
            rows = conn.execute(sql, params).fetchall()

        return [dict(row) for row in rows]

    def list_by_interval(
        self,
        start_captured_at: str,
        end_captured_at: str,
        codigo_opcao: str | None = None,
    ) -> list[dict[str, Any]]:
        """Lista amostras em intervalo inclusivo de captured_at."""
        self.ensure_schema()

        params: list[Any] = [start_captured_at, end_captured_at]
        sql = f"""
            SELECT *
            FROM {self.TABLE_NAME}
            WHERE captured_at >= ?
              AND captured_at <= ?
        """

        if codigo_opcao:
            sql += " AND codigo_opcao = ?"
            params.append(codigo_opcao)

        sql += " ORDER BY captured_at ASC, id ASC"

        with self._connect() as conn:
            rows = conn.execute(sql, params).fetchall()

        return [dict(row) for row in rows]

    def count(self) -> int:
        self.ensure_schema()
        with self._connect() as conn:
            row = conn.execute(
                f"SELECT COUNT(*) AS total FROM {self.TABLE_NAME}"
            ).fetchone()
        return int(row["total"])

    @staticmethod
    def _as_float_or_none(value: Any) -> float | None:
        if value is None:
            return None
        if value == "":
            return None
        if isinstance(value, str):
            value = value.strip().replace(".", "").replace(",", ".") if "," in value else value.strip()
            if value == "":
                return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _as_text_or_none(value: Any) -> str | None:
        if value is None:
            return None
        text = str(value).strip()
        return text or None

    @staticmethod
    def _as_text_datetime(value: Any) -> str:
        if isinstance(value, datetime):
            return value.isoformat()
        return str(value)


IntradayHistoryRepository = RtdOptionQuotesIntradayHistoryRepository

# INICIO FRENTE 39 RTD OPTION QUOTES INTRADAY HISTORY REPOSITORY PARSER BRIDGE CONTRACT
# Ponte contratual para adocao progressiva dos parsers canonicos em repositorio intraday history.
# Esta frente apenas declara o contrato local de integracao futura.
# Sem troca de persistencia.
# Sem troca de schema.
# Sem alteracao operacional do intraday history repository.
# Regra preservada: normalizacao numerica e temporal deve convergir para utils/number_parser.py e utils/date_parser.py.

try:
    from utils.number_parser import (
        parse_float_br as _frente39_parse_float_br,
        parse_optional_float as _frente39_parse_optional_float,
        parse_positive_float as _frente39_parse_positive_float,
    )
except Exception:
    _frente39_parse_float_br = None
    _frente39_parse_optional_float = None
    _frente39_parse_positive_float = None

try:
    from utils.date_parser import (
        parse_datetime_to_iso as _frente39_parse_datetime_to_iso,
    )
except Exception:
    _frente39_parse_datetime_to_iso = None


def _frente39_intraday_history_repository_parser_bridge_contract():
    """Contrato declarativo da Frente 39.

    Nao altera persistencia, schema ou comportamento operacional.
    Serve como ponto de convergencia para refatoracao futura controlada.
    """

    return {
        "frente": 39,
        "target": "repositories/rtd_option_quotes_intraday_history_repository.py",
        "number_parser": "utils.number_parser",
        "date_parser": "utils.date_parser",
        "parse_float_br": "_frente39_parse_float_br",
        "parse_optional_float": "_frente39_parse_optional_float",
        "parse_positive_float": "_frente39_parse_positive_float",
        "parse_datetime_to_iso": "_frente39_parse_datetime_to_iso",
        "persistence_change": False,
        "schema_change": False,
        "operational_change": False,
    }


def _frente39_apply_parser_bridge(value, parser):
    """Aplica parser canonico quando disponivel, preservando fallback local."""

    if parser is not None:
        return parser(value)
    return value
# FIM FRENTE 39 RTD OPTION QUOTES INTRADAY HISTORY REPOSITORY PARSER BRIDGE CONTRACT

# BEGIN FRENTE_68_INTRADAY_CANDLE_HISTORY_REPOSITORY_BOUNDARY
def fetch_intraday_history_rows_for_candles(**kwargs):
    """Read intraday history rows for candle building through repository boundary.

    This helper intentionally keeps SQL inside repositories, not services.
    It is defensive to preserve compatibility with the service call signature:
    accepted db path keys include db_path, path and database_path.
    Optional filters accepted: symbol/symbols and start/end timestamp aliases.
    """
    import sqlite3
    from pathlib import Path

    db_path = (
        kwargs.get("db_path")
        or kwargs.get("path")
        or kwargs.get("database_path")
        or kwargs.get("database")
    )
    if db_path is None:
        self_obj = kwargs.get("self")
        if self_obj is not None:
            db_path = getattr(self_obj, "db_path", None)

    if db_path is None:
        raise ValueError("db_path/path is required to read intraday history rows")

    table_name = "rtd_option_quotes_intraday_history"
    path_str = str(Path(db_path))

    conn = sqlite3.connect(path_str)
    conn.row_factory = sqlite3.Row
    try:
        table = conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
            (table_name,),
        ).fetchone()
        if table is None:
            return []

        columns = [
            row[1]
            for row in conn.execute(f"PRAGMA table_info({table_name})").fetchall()
        ]
        if not columns:
            return []

        column_set = set(columns)
        where = []
        params = []

        symbol_col = next(
            (name for name in ("symbol", "ticker", "codigo", "code") if name in column_set),
            None,
        )
        raw_symbol = (
            kwargs.get("symbol")
            or kwargs.get("ticker")
            or kwargs.get("codigo")
            or kwargs.get("code")
        )
        raw_symbols = kwargs.get("symbols") or kwargs.get("tickers") or kwargs.get("codigos")

        if symbol_col and raw_symbol not in (None, ""):
            where.append(f"UPPER(TRIM({symbol_col})) = ?")
            params.append(str(raw_symbol).strip().upper())
        elif symbol_col and raw_symbols:
            normalized_symbols = [
                str(item).strip().upper()
                for item in raw_symbols
                if str(item).strip()
            ]
            if normalized_symbols:
                placeholders = ", ".join("?" for _ in normalized_symbols)
                where.append(f"UPPER(TRIM({symbol_col})) IN ({placeholders})")
                params.extend(normalized_symbols)

        timestamp_col = next(
            (
                name
                for name in (
                    "captured_at",
                    "timestamp",
                    "created_at",
                    "updated_at",
                    "reference_at",
                    "datetime",
                )
                if name in column_set
            ),
            None,
        )

        start_at = (
            kwargs.get("start_at")
            or kwargs.get("from_at")
            or kwargs.get("start")
            or kwargs.get("captured_from")
            or kwargs.get("from_timestamp")
        )
        end_at = (
            kwargs.get("end_at")
            or kwargs.get("to_at")
            or kwargs.get("end")
            or kwargs.get("captured_to")
            or kwargs.get("to_timestamp")
        )

        if timestamp_col and start_at not in (None, ""):
            where.append(f"{timestamp_col} >= ?")
            params.append(str(start_at))
        if timestamp_col and end_at not in (None, ""):
            where.append(f"{timestamp_col} <= ?")
            params.append(str(end_at))

        query = f"SELECT * FROM {table_name}"
        if where:
            query += " WHERE " + " AND ".join(where)
        if timestamp_col:
            query += f" ORDER BY {timestamp_col} ASC"

        return [dict(row) for row in conn.execute(query, params).fetchall()]
    finally:
        conn.close()
# END FRENTE_68_INTRADAY_CANDLE_HISTORY_REPOSITORY_BOUNDARY

# INICIO FRENTE 70 INTRADAY HISTORY SERVICE SQL BOUNDARY

def open_intraday_history_capture_connection(db_path):
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def intraday_history_snapshot_table_exists_for_capture(conn, table_name):
    row = conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name = ?
        """,
        (table_name,),
    ).fetchone()
    return row is not None


def fetch_snapshot_rows_for_intraday_history_capture(
    db_path,
    snapshot_table="rtd_option_quotes",
):
    conn = open_intraday_history_capture_connection(db_path)
    try:
        if not intraday_history_snapshot_table_exists_for_capture(conn, snapshot_table):
            return []

        rows = conn.execute(
            f"SELECT * FROM {snapshot_table}"
        ).fetchall()

        return [dict(row) for row in rows]
    finally:
        conn.close()

# FIM FRENTE 70 INTRADAY HISTORY SERVICE SQL BOUNDARY

