"""Repositório de decisões da tabela structure_decisions."""

from __future__ import annotations

import sqlite3
from typing import Any


class DecisionRepository:
    """Acessa structure_decisions com filtro opcional por structure_id."""

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def insert_decision(self, structure_id, decision=None, **kwargs):
        """Registra decisao de estrutura pelo contrato oficial do repository.

        Este endpoint e usado pela ponte operacional do Terminal VWAP Payoff.
        Ele nao cria schema, nao executa migration e usa apenas colunas ja
        existentes em structure_decisions.
        """
        import json
        import sqlite3
        from datetime import datetime

        try:
            structure_id_int = int(structure_id)
        except (TypeError, ValueError) as exc:
            raise ValueError("structure_id invalido para insert_decision") from exc

        decision_value = (
            decision
            or kwargs.get("decision")
            or kwargs.get("decision_label")
            or kwargs.get("action")
        )
        decision_text = str(decision_value or "").strip().upper()
        if not decision_text:
            raise ValueError("decision vazia para insert_decision")

        source = str(
            kwargs.get("source")
            or kwargs.get("origin")
            or "terminal_vwap_payoff_dark_panel"
        ).strip()

        notes = str(
            kwargs.get("notes")
            or kwargs.get("comment")
            or kwargs.get("reason")
            or ""
        ).strip()

        metadata = kwargs.get("metadata")
        if metadata is None:
            metadata = kwargs.get("payload")
        if metadata is None:
            metadata = {}

        try:
            metadata_json = json.dumps(metadata, ensure_ascii=False, sort_keys=True)
        except TypeError:
            metadata_json = json.dumps(str(metadata), ensure_ascii=False)

        created_at = datetime.now().isoformat(timespec="seconds")

        conn = sqlite3.connect(str(self.db_path))
        try:
            cur = conn.cursor()
            cur.execute("PRAGMA table_info(structure_decisions)")
            table_info = cur.fetchall()
            columns = [row[1] for row in table_info]

            if not columns:
                raise RuntimeError("structure_decisions ausente para insert_decision")

            values_by_column = {
                "structure_id": structure_id_int,
                "decision": decision_text,
                "decision_label": decision_text,
                "action": decision_text,
                "source": source,
                "origin": source,
                "notes": notes,
                "comment": notes,
                "metadata_json": metadata_json,
                "payload_json": metadata_json,
                "created_at": created_at,
                "registered_at": created_at,
                "timestamp": created_at,
                "updated_at": created_at,
            }

            insert_columns = [
                column
                for column in columns
                if column in values_by_column
            ]

            if "structure_id" not in insert_columns:
                raise RuntimeError("structure_decisions sem structure_id para insert_decision")

            if not any(
                column in insert_columns
                for column in ("decision", "decision_label", "action")
            ):
                raise RuntimeError("structure_decisions sem coluna de decisao para insert_decision")

            placeholders = ", ".join("?" for _ in insert_columns)
            column_sql = ", ".join(insert_columns)
            values = [values_by_column[column] for column in insert_columns]

            cur.execute(
                f"INSERT INTO structure_decisions ({column_sql}) VALUES ({placeholders})",
                values,
            )
            conn.commit()
            return int(cur.lastrowid or 0)
        finally:
            conn.close()

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
