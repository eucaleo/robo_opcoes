# repositories/rtd_option_quotes_repository.py

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class RtdOptionQuotesRepository:
    """
    Leitura da tabela rtd_option_quotes.

    Essa tabela é alimentada pelo CSV exportado da aba RTD_LINKS
    e funciona como cache centralizado das cotações RTD de opções.
    """

    def __init__(self, db_path: str | Path = "dados/app.db") -> None:
        self.db_path = Path(db_path)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def get_by_codigo(self, codigo_opcao: str) -> dict[str, Any] | None:
        sql = """
            SELECT
                codigo_opcao,
                ativo_base,
                call_put,
                strike,
                vencimento,
                ultimo_preco,
                ultima_quantidade,
                bid,
                ask,
                volume,
                iv,
                delta,
                gamma,
                theta,
                vega,
                source,
                raw_json,
                updated_at,
                created_at
            FROM rtd_option_quotes
            WHERE codigo_opcao = ?
            LIMIT 1
        """

        with self._connect() as conn:
            row = conn.execute(sql, (codigo_opcao,)).fetchone()

        return dict(row) if row else None

    def list_by_ativo_base(self, ativo_base: str) -> list[dict[str, Any]]:
        sql = """
            SELECT
                codigo_opcao,
                ativo_base,
                call_put,
                strike,
                vencimento,
                ultimo_preco,
                ultima_quantidade,
                bid,
                ask,
                volume,
                iv,
                delta,
                gamma,
                theta,
                vega,
                source,
                raw_json,
                updated_at,
                created_at
            FROM rtd_option_quotes
            WHERE ativo_base = ?
            ORDER BY vencimento, call_put, strike, codigo_opcao
        """

        with self._connect() as conn:
            rows = conn.execute(sql, (ativo_base,)).fetchall()

        return [dict(row) for row in rows]

    def list_all(self) -> list[dict[str, Any]]:
        sql = """
            SELECT
                codigo_opcao,
                ativo_base,
                call_put,
                strike,
                vencimento,
                ultimo_preco,
                ultima_quantidade,
                bid,
                ask,
                volume,
                iv,
                delta,
                gamma,
                theta,
                vega,
                source,
                raw_json,
                updated_at,
                created_at
            FROM rtd_option_quotes
            ORDER BY ativo_base, vencimento, call_put, strike, codigo_opcao
        """

        with self._connect() as conn:
            rows = conn.execute(sql).fetchall()

        return [dict(row) for row in rows]
