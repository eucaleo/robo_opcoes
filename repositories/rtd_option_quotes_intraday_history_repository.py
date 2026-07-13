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
