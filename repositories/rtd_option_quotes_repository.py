# repositories/rtd_option_quotes_repository.py
"""
Repositorio para consulta de cotações de opções em rtd_option_quotes.

Contrato:
- get_by_codigo usa match EXATO de codigo_opcao, sem upper no WHERE;
- erros sqlite3.OperationalError propagam;
- retorna dicts;
- expõe list_by_ativo_base e list_all.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class RtdOptionQuotesRepository:
    def __init__(self, db_path: str | Path = "dados/app.db") -> None:
        self.db_path = str(db_path)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_by_codigo(self, codigo_opcao: str) -> dict[str, Any] | None:
        codigo = str(codigo_opcao or "").strip()
        if not codigo:
            return None

        sql = """
            SELECT *
            FROM rtd_option_quotes
            WHERE codigo_opcao = ?
            ORDER BY
                COALESCE(updated_at, created_at, '') DESC,
                rowid DESC
            LIMIT 1
        """

        with self._connect() as conn:
            row = conn.execute(sql, (codigo,)).fetchone()

        return dict(row) if row is not None else None

    def list_by_ativo_base(self, ativo_base: str) -> list[dict[str, Any]]:
        ativo = str(ativo_base or "").strip()
        if not ativo:
            return []

        sql = """
            SELECT *
            FROM rtd_option_quotes
            WHERE ativo_base = ?
            ORDER BY vencimento ASC, strike ASC, codigo_opcao ASC
        """

        with self._connect() as conn:
            rows = conn.execute(sql, (ativo,)).fetchall()

        return [dict(row) for row in rows]

    def list_all(self) -> list[dict[str, Any]]:
        sql = """
            SELECT *
            FROM rtd_option_quotes
            ORDER BY ativo_base ASC, vencimento ASC, strike ASC, codigo_opcao ASC
        """

        with self._connect() as conn:
            rows = conn.execute(sql).fetchall()

        return [dict(row) for row in rows]
