from __future__ import annotations

import sqlite3
import inspect
from pathlib import Path
from typing import Any
from services.pricing_execution_app_service import PricingExecutionAppService


# Boundary SQLite extraido da Frente 60.
# Este modulo concentra acesso direto ao SQLite antes existente no command service.

def _PayoffRefreshCommandService__latest_snapshot_id(self, structure_id: int) -> int | None:
    if not self.db_path.exists():
        return None

    queries = [
        """
        SELECT id
        FROM structure_snapshots
        WHERE structure_id = ?
        ORDER BY created_at DESC
        LIMIT 1
        """,
        """
        SELECT snapshot_id
        FROM structure_snapshots
        WHERE structure_id = ?
        ORDER BY created_at DESC
        LIMIT 1
        """,
    ]

    for query in queries:
        try:
            with self._connect() as conn:
                row = conn.execute(query, (structure_id,)).fetchone()
            if row:
                return int(row[0])
        except sqlite3.Error:
            continue

    return None

def _PayoffRefreshCommandService__decision_exists(self, structure_id: int, timestamp: str | None) -> bool:
    if not timestamp or not self.db_path.exists():
        return False

    queries = [
        (
            """
            SELECT COUNT(*)
            FROM structure_decisions
            WHERE structure_id = ?
              AND timestamp = ?
            """,
            (structure_id, timestamp),
        ),
        (
            """
            SELECT COUNT(*)
            FROM structure_decisions
            WHERE timestamp = ?
            """,
            (timestamp,),
        ),
    ]

    for query, params in queries:
        try:
            with self._connect() as conn:
                count = conn.execute(query, params).fetchone()[0]
            return int(count) > 0
        except sqlite3.Error:
            continue

    return False

def _PayoffRefreshCommandService__latest_payoff_summary(self, structure_id: int) -> dict[str, Any]:
    if not self.db_path.exists():
        return {
            "latest_payoff_timestamp": None,
            "payoff_points_count": 0,
        }

    query = """
        SELECT timestamp, COUNT(*) AS n
        FROM payoff_curve_points
        WHERE structure_id = ?
        GROUP BY timestamp
        ORDER BY timestamp DESC
        LIMIT 1
    """

    try:
        with self._connect() as conn:
            row = conn.execute(query, (structure_id,)).fetchone()
    except sqlite3.Error:
        return {
            "latest_payoff_timestamp": None,
            "payoff_points_count": 0,
        }

    if not row:
        return {
            "latest_payoff_timestamp": None,
            "payoff_points_count": 0,
        }

    return {
        "latest_payoff_timestamp": row[0],
        "payoff_points_count": row[1],
    }

def _PayoffRefreshCommandService__connect(self) -> sqlite3.Connection:
    return sqlite3.connect(str(self.db_path))

def _PayoffRefreshCommandService__ensure_active_structure(self, structure_id: int) -> None:
    """
    Bloqueia refresh/reprecificação para estruturas não ativas.

    Regra operacional:
      - apenas structures.status == 'active' pode gerar novo payoff/decisão;
      - archived/inactive não deve consumir processamento nem persistir derivados.
    """
    if not self.db_path.exists():
        raise ValueError(f"app.db não encontrado: {self.db_path}")

    with self._connect() as conn:
        cols = {row[1] for row in conn.execute("PRAGMA table_info(structures)").fetchall()}
        if "status" not in cols:
            raise ValueError("coluna structures.status não encontrada; validação de estrutura ativa impossível")

        row = conn.execute(
            """
            SELECT status
              FROM structures
             WHERE id = ?
             LIMIT 1
            """,
            (structure_id,),
        ).fetchone()

    if not row:
        raise ValueError(f"structure not found: {structure_id}")

    status = str(row[0] or "").strip().lower()
    if status != "active":
        raise ValueError(
            f"estrutura inativa/arquivada não pode gerar payoff: "
            f"structure_id={structure_id}, status={status!r}"
        )
