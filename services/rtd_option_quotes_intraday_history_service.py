"""Servico de captura do historico intraday a partir do snapshot rtd_option_quotes.

Fase 3 - Historico intraday RTD Online.

Este servico:
- le apenas a tabela snapshot rtd_option_quotes;
- grava amostras em rtd_option_quotes_intraday_history;
- nao acessa Excel;
- nao executa processos externos;
- nao agrega serie temporal nesta etapa.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
from typing import Any

from repositories.rtd_option_quotes_intraday_history_repository import (
    RtdOptionQuotesIntradayHistoryRepository,
)


class RtdOptionQuotesIntradayHistoryService:
    """Captura amostras historicas a partir do snapshot rtd_option_quotes."""

    SNAPSHOT_TABLE = "rtd_option_quotes"

    CODIGO_CANDIDATES = (
        "codigo_opcao",
        "symbol",
        "ticker",
        "codigo",
        "option_symbol",
    )
    BID_CANDIDATES = ("bid", "compra", "preco_compra", "melhor_compra")
    ASK_CANDIDATES = ("ask", "venda", "preco_venda", "melhor_venda")
    LAST_CANDIDATES = (
        "last",
        "ultimo_preco",
        "ultimo",
        "ultima",
        "preco_ultimo",
        "last_price",
    )
    VWAP_CANDIDATES = ("vwap", "preco_medio", "average_price")
    VOLUME_CANDIDATES = ("volume", "qtd", "quantidade", "volume_financeiro")
    SOURCE_UPDATED_CANDIDATES = (
        "source_updated_at",
        "updated_at",
        "atualizado_em",
        "last_update",
        "timestamp",
        "data_hora",
    )

    def __init__(
        self,
        db_path: str | Path = "dados/app.db",
        history_repository: RtdOptionQuotesIntradayHistoryRepository | None = None,
    ) -> None:
        self.db_path = str(db_path)
        self.history_repository = history_repository or RtdOptionQuotesIntradayHistoryRepository(
            db_path=self.db_path
        )

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def capture_snapshot(self, captured_at: datetime | str | None = None) -> int:
        """Captura o snapshot atual e retorna a quantidade de amostras gravadas."""
        captured_at_text = self._as_text_datetime(
            captured_at or datetime.now(ZoneInfo("America/Sao_Paulo"))
        )

        self.history_repository.ensure_schema()
        rows = self._read_snapshot_rows()

        samples: list[dict[str, Any]] = []

        for row in rows:
            payload = dict(row)
            codigo_opcao = self._pick(payload, self.CODIGO_CANDIDATES)

            if not codigo_opcao:
                continue

            samples.append(
                {
                    "captured_at": captured_at_text,
                    "codigo_opcao": str(codigo_opcao).strip(),
                    "bid": self._pick(payload, self.BID_CANDIDATES),
                    "ask": self._pick(payload, self.ASK_CANDIDATES),
                    "last": self._pick(payload, self.LAST_CANDIDATES),
                    "vwap": self._pick(payload, self.VWAP_CANDIDATES),
                    "volume": self._pick(payload, self.VOLUME_CANDIDATES),
                    "source_updated_at": self._pick(
                        payload,
                        self.SOURCE_UPDATED_CANDIDATES,
                    ),
                    "raw_payload_json": json.dumps(
                        payload,
                        ensure_ascii=False,
                        sort_keys=True,
                        default=str,
                    ),
                }
            )

        return self.history_repository.insert_samples(samples)

    def _read_snapshot_rows(self) -> list[sqlite3.Row]:
        with self._connect() as conn:
            if not self._table_exists(conn, self.SNAPSHOT_TABLE):
                return []

            return conn.execute(
                f"SELECT * FROM {self.SNAPSHOT_TABLE}"
            ).fetchall()

    @staticmethod
    def _table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
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

    @staticmethod
    def _pick(payload: dict[str, Any], candidates: tuple[str, ...]) -> Any:
        lower_to_key = {str(key).lower(): key for key in payload.keys()}

        for candidate in candidates:
            key = lower_to_key.get(candidate.lower())
            if key is not None:
                value = payload.get(key)
                if value is not None and str(value).strip() != "":
                    return value

        return None

    @staticmethod
    def _as_text_datetime(value: Any) -> str:
        if isinstance(value, datetime):
            return value.isoformat()
        return str(value)


IntradayHistoryService = RtdOptionQuotesIntradayHistoryService
