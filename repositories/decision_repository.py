"""Repositório de decisões da tabela structure_decisions."""

from __future__ import annotations

import sqlite3
from typing import Any


class DecisionRepository:
    """Acessa structure_decisions com filtro opcional por structure_id."""

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def list_decisions(
        self,
        structure_id: int | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """Decisões ordenadas por timestamp DESC.

        Args:
            structure_id: Filtro opcional. Se None, retorna de todas.
            limit: Máximo de registros (default 50).
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cols = [
            row["name"]
            for row in cursor.execute(
                "PRAGMA table_info(structure_decisions)"
            ).fetchall()
        ]

        select_cols = [
            "timestamp", "aba", "decision", "level",
            "pl_atual", "pl_max", "pl_pct_of_max", "dte_min",
            "spot_ref", "meta_json", "created_at",
        ]
        if "structure_id" in cols:
            select_cols.append("structure_id")
        if "why" in cols:
            select_cols.append("why")
        if "why_json" in cols:
            select_cols.append("why_json")

        where_clause = ""
        params: list[Any] = []
        if structure_id is not None and "structure_id" in cols:
            where_clause = "WHERE structure_id = ?"
            params.append(structure_id)

        cursor.execute(
            f"""
            SELECT {", ".join(select_cols)}
            FROM structure_decisions
            {where_clause}
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            params + [limit],
        )

        decisions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return decisions
