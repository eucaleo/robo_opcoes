from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from db.config import APP_DB_PATH
except Exception:  # pragma: no cover - fallback defensivo local
    APP_DB_PATH = Path("dados") / "app.db"


class DetailsPanelSqlBoundary:
    """Boundary local para isolar SQL direto que antes estava em UI/components/details_panel.py.

    Regras da Frente 64:
    - UI nao abre conexao SQLite diretamente.
    - UI nao consulta sqlite_master/PRAGMA diretamente.
    - Boundary fica em repositories/, mantendo execucao 100% local.
    - Sem alteracao de schema.
    - Sem alteracao de persistencia.
    """

    def __init__(self, owner: Any | None = None) -> None:
        self._owner = owner

    def __getattr__(self, name: str) -> Any:
        owner = object.__getattribute__(self, "_owner")
        if owner is not None:
            return getattr(owner, name)
        raise AttributeError(name)


    def _quote_sql_identifier(self, name: object) -> str:
        raw = str(name)
        return '"' + raw.replace('"', '""') + '"'

    def _latest_snapshot_timestamp_in_db(self, db_path, sid, sid_text):
            import sqlite3

            if not db_path.exists():
                return None

            try:
                con = sqlite3.connect(str(db_path))
                try:
                    return self._latest_snapshot_timestamp_in_connection(con, sid, sid_text)
                finally:
                    con.close()
            except sqlite3.Error:
                return None

    def _table_names(self, cur):
            rows = cur.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                  AND name NOT LIKE 'sqlite_%'
                """
            ).fetchall()
            return [row[0] for row in rows]

    def _table_columns(self, cur, table):
            rows = cur.execute(
                f"PRAGMA table_info({self._quote_sql_identifier(table)})"
            ).fetchall()
            return [row[1] for row in rows]

    def _max_timestamp_for_structure_column(
            self,
            cur,
            table,
            structure_col,
            timestamp_col,
            sid,
            sid_text,
        ):
            import sqlite3

            try:
                row = cur.execute(
                    f"""
                    SELECT MAX({self._quote_sql_identifier(timestamp_col)})
                    FROM {self._quote_sql_identifier(table)}
                    WHERE {self._quote_sql_identifier(structure_col)} = ?
                       OR CAST({self._quote_sql_identifier(structure_col)} AS TEXT) = ?
                    """,
                    (sid, sid_text),
                ).fetchone()
            except sqlite3.Error:
                return None

            if row and row[0] is not None:
                return str(row[0])

            return None
