from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from infra.bootstrap_structures_schema import DB_PATH, ensure_structures_schema


_JSON_COLUMNS_SNAPSHOT = {
    "structure_json",
    "market_json",
    "metrics_json",
    "payoff_json",
    "decision_json",
    "alerts_json",
    "operation_state_json",
}

_JSON_COLUMNS_LEG = {
    "metrics_json",
    "market_json",
    "raw_json",
}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _to_json(value: Any) -> str | None:
    if value is None:
        return None

    if isinstance(value, str):
        return value

    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _from_json(value: Any) -> Any:
    if value is None:
        return None

    if not isinstance(value, str):
        return value

    value = value.strip()

    if value == "":
        return None

    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return {key: row[key] for key in row.keys()}


class SystemSnapshotsRepository:
    """Persistência do histórico operacional oficial gerado pelo sistema."""

    def __init__(self, db_path: str | Path = DB_PATH) -> None:
        self.db_path = Path(db_path)
        ensure_structures_schema(self.db_path)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def create_snapshot(
        self,
        *,
        structure_id: int,
        structure_json: dict[str, Any],
        legs: list[dict[str, Any]] | None = None,
        pricing_execution_id: int | None = None,
        underlying_asset: str | None = None,
        reference_date: str | None = None,
        snapshot_source: str = "system",
        market_json: dict[str, Any] | list[Any] | None = None,
        metrics_json: dict[str, Any] | list[Any] | None = None,
        payoff_json: dict[str, Any] | list[Any] | None = None,
        decision_json: dict[str, Any] | list[Any] | None = None,
        alerts_json: dict[str, Any] | list[Any] | None = None,
        operation_state_json: dict[str, Any] | list[Any] | None = None,
        created_at: str | None = None,
    ) -> int:
        """Cria um snapshot e suas pernas associadas.

        Retorna o id gerado em structure_snapshots.
        """

        if not structure_id:
            raise ValueError("structure_id é obrigatório")

        if not structure_json:
            raise ValueError("structure_json é obrigatório")

        created_at = created_at or _utc_now_iso()
        legs = legs or []

        with self._connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO structure_snapshots (
                    created_at,
                    structure_id,
                    pricing_execution_id,
                    underlying_asset,
                    reference_date,
                    snapshot_source,
                    structure_json,
                    market_json,
                    metrics_json,
                    payoff_json,
                    decision_json,
                    alerts_json,
                    operation_state_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    created_at,
                    structure_id,
                    pricing_execution_id,
                    underlying_asset,
                    reference_date,
                    snapshot_source,
                    _to_json(structure_json),
                    _to_json(market_json),
                    _to_json(metrics_json),
                    _to_json(payoff_json),
                    _to_json(decision_json),
                    _to_json(alerts_json),
                    _to_json(operation_state_json),
                ),
            )

            snapshot_id = int(cur.lastrowid)

            for index, leg in enumerate(legs, start=1):
                self._insert_leg_snapshot(
                    conn=conn,
                    snapshot_id=snapshot_id,
                    structure_id=structure_id,
                    leg=leg,
                    default_leg_order=index,
                )

            return snapshot_id

    def _insert_leg_snapshot(
        self,
        *,
        conn: sqlite3.Connection,
        snapshot_id: int,
        structure_id: int,
        leg: dict[str, Any],
        default_leg_order: int,
    ) -> None:
        conn.execute(
            """
            INSERT INTO structure_leg_snapshots (
                snapshot_id,
                structure_id,
                leg_id,
                leg_order,
                position_side,
                option_type,
                symbol,
                strike,
                expiration_date,
                quantity,
                premium,
                multiplier,
                metrics_json,
                market_json,
                raw_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                snapshot_id,
                structure_id,
                leg.get("leg_id") or leg.get("id"),
                leg.get("leg_order", default_leg_order),
                leg.get("position_side"),
                leg.get("option_type"),
                leg.get("symbol"),
                leg.get("strike"),
                leg.get("expiration_date"),
                leg.get("quantity"),
                leg.get("premium"),
                leg.get("multiplier"),
                _to_json(leg.get("metrics_json")),
                _to_json(leg.get("market_json")),
                _to_json(leg.get("raw_json", leg)),
            ),
        )

    def get_snapshot(self, snapshot_id: int) -> dict[str, Any] | None:
        """Retorna um snapshot com suas pernas, ou None se não existir."""

        with self._connect() as conn:
            snapshot_row = conn.execute(
                """
                SELECT *
                FROM structure_snapshots
                WHERE id = ?
                """,
                (snapshot_id,),
            ).fetchone()

            if snapshot_row is None:
                return None

            snapshot = self._decode_snapshot_row(snapshot_row)

            leg_rows = conn.execute(
                """
                SELECT *
                FROM structure_leg_snapshots
                WHERE snapshot_id = ?
                ORDER BY leg_order, id
                """,
                (snapshot_id,),
            ).fetchall()

            snapshot["legs"] = [self._decode_leg_row(row) for row in leg_rows]

            return snapshot

    def list_snapshots_for_structure(
        self,
        structure_id: int,
        *,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """Lista snapshots de uma estrutura, do mais recente para o mais antigo."""

        if limit <= 0:
            raise ValueError("limit deve ser maior que zero")

        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT *
                FROM structure_snapshots
                WHERE structure_id = ?
                ORDER BY created_at DESC, id DESC
                LIMIT ?
                """,
                (structure_id, limit),
            ).fetchall()

        return [self._decode_snapshot_row(row) for row in rows]

    def get_latest_snapshot_for_structure(
        self,
        structure_id: int,
    ) -> dict[str, Any] | None:
        """Retorna o snapshot mais recente de uma estrutura."""

        snapshots = self.list_snapshots_for_structure(structure_id, limit=1)

        if not snapshots:
            return None

        return self.get_snapshot(int(snapshots[0]["id"]))

    def _decode_snapshot_row(self, row: sqlite3.Row) -> dict[str, Any]:
        data = _row_to_dict(row)

        for column in _JSON_COLUMNS_SNAPSHOT:
            data[column] = _from_json(data.get(column))

        return data

    def _decode_leg_row(self, row: sqlite3.Row) -> dict[str, Any]:
        data = _row_to_dict(row)

        for column in _JSON_COLUMNS_LEG:
            data[column] = _from_json(data.get(column))

        return data
