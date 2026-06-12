# repositories/structure_events_repository.py
"""
Repositório canônico de eventos operacionais de estruturas.

Fase 12 — Eventos operacionais:
- abertura
- ajuste
- roll
- encerramento parcial
- encerramento total
- encerramento manual
- observação operacional

A tabela structure_events é a fonte viva do sistema para eventos operacionais.
Tabelas legadas como rtd_encerramentos_manuais e rtd_rolls_detectados seguem
apenas como referência/importação histórica.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


VALID_EVENT_TYPES: frozenset[str] = frozenset(
    {
        "open",
        "adjustment",
        "roll",
        "partial_close",
        "total_close",
        "manual_close",
        "note",
    }
)

VALID_EVENT_STATUS: frozenset[str] = frozenset(
    {
        "registered",
        "cancelled",
    }
)

VALID_EVENT_SOURCES: frozenset[str] = frozenset(
    {
        "system",
        "manual",
        "legacy_import",
    }
)


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _normalize_optional_text(value: Any) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip()
    return normalized or None


def _json_dumps(value: dict[str, Any] | None) -> str | None:
    if value is None:
        return None
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _json_loads(value: str | None) -> dict[str, Any] | None:
    if value is None:
        return None
    return json.loads(value)


def _normalize_event_payload(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("event payload must be a dict")

    try:
        structure_id = int(data.get("structure_id"))
    except Exception as exc:
        raise ValueError("structure_id is required") from exc

    if structure_id <= 0:
        raise ValueError("structure_id must be > 0")

    leg_id_raw = data.get("leg_id")
    leg_id: int | None = None
    if leg_id_raw is not None:
        try:
            leg_id = int(leg_id_raw)
        except Exception as exc:
            raise ValueError("leg_id must be integer when provided") from exc
        if leg_id <= 0:
            raise ValueError("leg_id must be > 0 when provided")

    event_type = str(data.get("event_type", "")).strip().lower()
    if event_type not in VALID_EVENT_TYPES:
        raise ValueError(f"invalid event_type: {event_type}")

    event_status = str(data.get("event_status", "registered")).strip().lower()
    if event_status not in VALID_EVENT_STATUS:
        raise ValueError(f"invalid event_status: {event_status}")

    event_date = str(data.get("event_date", "")).strip()
    if not event_date:
        raise ValueError("event_date is required")

    quantity_raw = data.get("quantity")
    quantity: int | None = None
    if quantity_raw is not None:
        try:
            quantity = int(quantity_raw)
        except Exception as exc:
            raise ValueError("quantity must be integer when provided") from exc
        if quantity <= 0:
            raise ValueError("quantity must be > 0 when provided")

    price_raw = data.get("price")
    price: float | None = None
    if price_raw is not None:
        try:
            price = float(price_raw)
        except Exception as exc:
            raise ValueError("price must be numeric when provided") from exc

    source = str(data.get("source", "manual")).strip().lower()
    if source not in VALID_EVENT_SOURCES:
        raise ValueError(f"invalid source: {source}")

    metadata = data.get("metadata")
    if metadata is None:
        metadata = data.get("metadata_json")

    if metadata is not None and not isinstance(metadata, dict):
        raise ValueError("metadata must be a dict when provided")

    return {
        "structure_id": structure_id,
        "leg_id": leg_id,
        "event_type": event_type,
        "event_status": event_status,
        "event_date": event_date,
        "quantity": quantity,
        "price": price,
        "symbol": _normalize_optional_text(data.get("symbol")),
        "source": source,
        "notes": _normalize_optional_text(data.get("notes")),
        "metadata": metadata,
    }


class StructureEventsRepository:
    def __init__(self, db_path: str | Path = "dados/app.db") -> None:
        self.db_path = str(db_path)

    # ------------------------------------------------------------------
    # Conexão/schema
    # ------------------------------------------------------------------

    def _connect(self) -> sqlite3.Connection:
        db_path = Path(self.db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def ensure_schema(self) -> None:
        conn = self._connect()
        try:
            self.ensure_schema_on_connection(conn)
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def ensure_schema_on_connection(conn: sqlite3.Connection) -> None:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS structure_events (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                structure_id   INTEGER NOT NULL,
                leg_id         INTEGER,
                event_type     TEXT    NOT NULL,
                event_status   TEXT    NOT NULL DEFAULT 'registered',
                event_date     TEXT    NOT NULL,
                quantity       INTEGER,
                price          REAL,
                symbol         TEXT,
                source         TEXT    NOT NULL DEFAULT 'manual',
                notes          TEXT,
                metadata_json  TEXT,
                created_at     TEXT    NOT NULL,
                updated_at     TEXT    NOT NULL,
                FOREIGN KEY (structure_id) REFERENCES structures(id) ON DELETE CASCADE,
                FOREIGN KEY (leg_id) REFERENCES structure_legs(id) ON DELETE SET NULL
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_structure_events_structure_id
            ON structure_events(structure_id)
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_structure_events_leg_id
            ON structure_events(leg_id)
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_structure_events_event_type
            ON structure_events(event_type)
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_structure_events_event_status
            ON structure_events(event_status)
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_structure_events_event_date
            ON structure_events(event_date)
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_structure_events_structure_date
            ON structure_events(structure_id, event_date)
            """
        )

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------

    @staticmethod
    def _row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
        if row is None:
            return None

        data = dict(row)
        data["metadata"] = _json_loads(data.pop("metadata_json", None))
        return data

    @staticmethod
    def _ensure_structure_exists(conn: sqlite3.Connection, structure_id: int) -> None:
        row = conn.execute(
            "SELECT id FROM structures WHERE id = ?",
            (structure_id,),
        ).fetchone()
        if row is None:
            raise ValueError(f"structure not found: {structure_id}")

    @staticmethod
    def _ensure_leg_belongs_to_structure(
        conn: sqlite3.Connection,
        structure_id: int,
        leg_id: int | None,
    ) -> None:
        if leg_id is None:
            return

        row = conn.execute(
            """
            SELECT id
            FROM structure_legs
            WHERE id = ?
              AND structure_id = ?
            """,
            (leg_id, structure_id),
        ).fetchone()

        if row is None:
            raise ValueError(
                f"leg not found for structure: leg_id={leg_id}, structure_id={structure_id}"
            )

    # ------------------------------------------------------------------
    # Escrita
    # ------------------------------------------------------------------

    def create_event(self, data: dict[str, Any]) -> int:
        event = _normalize_event_payload(data)
        now = _utc_now_iso()

        conn = self._connect()
        try:
            self.ensure_schema_on_connection(conn)
            self._ensure_structure_exists(conn, event["structure_id"])
            self._ensure_leg_belongs_to_structure(
                conn,
                event["structure_id"],
                event["leg_id"],
            )

            cur = conn.execute(
                """
                INSERT INTO structure_events (
                    structure_id,
                    leg_id,
                    event_type,
                    event_status,
                    event_date,
                    quantity,
                    price,
                    symbol,
                    source,
                    notes,
                    metadata_json,
                    created_at,
                    updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event["structure_id"],
                    event["leg_id"],
                    event["event_type"],
                    event["event_status"],
                    event["event_date"],
                    event["quantity"],
                    event["price"],
                    event["symbol"],
                    event["source"],
                    event["notes"],
                    _json_dumps(event["metadata"]),
                    now,
                    now,
                ),
            )
            conn.commit()
            return int(cur.lastrowid)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def cancel_event(self, event_id: int, notes: str | None = None) -> None:
        event_id = int(event_id)
        if event_id <= 0:
            raise ValueError("event_id must be > 0")

        now = _utc_now_iso()
        normalized_notes = _normalize_optional_text(notes)

        conn = self._connect()
        try:
            self.ensure_schema_on_connection(conn)

            current = conn.execute(
                "SELECT id, notes FROM structure_events WHERE id = ?",
                (event_id,),
            ).fetchone()

            if current is None:
                raise ValueError(f"event not found: {event_id}")

            final_notes = normalized_notes if normalized_notes is not None else current["notes"]

            conn.execute(
                """
                UPDATE structure_events
                SET event_status = 'cancelled',
                    notes = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (final_notes, now, event_id),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # Leitura
    # ------------------------------------------------------------------

    def get_event(self, event_id: int) -> dict[str, Any] | None:
        event_id = int(event_id)
        if event_id <= 0:
            raise ValueError("event_id must be > 0")

        conn = self._connect()
        try:
            self.ensure_schema_on_connection(conn)
            row = conn.execute(
                """
                SELECT *
                FROM structure_events
                WHERE id = ?
                """,
                (event_id,),
            ).fetchone()
            return self._row_to_dict(row)
        finally:
            conn.close()

    def list_events(
        self,
        structure_id: int | None = None,
        event_type: str | None = None,
        event_status: str | None = None,
        include_cancelled: bool = False,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        filters: list[str] = []
        params: list[Any] = []

        if structure_id is not None:
            structure_id = int(structure_id)
            if structure_id <= 0:
                raise ValueError("structure_id must be > 0")
            filters.append("structure_id = ?")
            params.append(structure_id)

        if event_type is not None:
            event_type = str(event_type).strip().lower()
            if event_type not in VALID_EVENT_TYPES:
                raise ValueError(f"invalid event_type: {event_type}")
            filters.append("event_type = ?")
            params.append(event_type)

        if event_status is not None:
            event_status = str(event_status).strip().lower()
            if event_status not in VALID_EVENT_STATUS:
                raise ValueError(f"invalid event_status: {event_status}")
            filters.append("event_status = ?")
            params.append(event_status)
        elif not include_cancelled:
            filters.append("event_status <> 'cancelled'")

        limit = int(limit)
        offset = int(offset)

        if limit <= 0:
            raise ValueError("limit must be > 0")
        if offset < 0:
            raise ValueError("offset must be >= 0")

        where_sql = ""
        if filters:
            where_sql = "WHERE " + " AND ".join(filters)

        params.extend([limit, offset])

        conn = self._connect()
        try:
            self.ensure_schema_on_connection(conn)
            rows = conn.execute(
                f"""
                SELECT *
                FROM structure_events
                {where_sql}
                ORDER BY event_date ASC, id ASC
                LIMIT ? OFFSET ?
                """,
                params,
            ).fetchall()
            return [self._row_to_dict(row) for row in rows]
        finally:
            conn.close()

    def list_events_for_structure(
        self,
        structure_id: int,
        include_cancelled: bool = False,
    ) -> list[dict[str, Any]]:
        return self.list_events(
            structure_id=structure_id,
            include_cancelled=include_cancelled,
        )

    def count_events(
        self,
        structure_id: int | None = None,
        event_type: str | None = None,
        include_cancelled: bool = False,
    ) -> int:
        filters: list[str] = []
        params: list[Any] = []

        if structure_id is not None:
            structure_id = int(structure_id)
            if structure_id <= 0:
                raise ValueError("structure_id must be > 0")
            filters.append("structure_id = ?")
            params.append(structure_id)

        if event_type is not None:
            event_type = str(event_type).strip().lower()
            if event_type not in VALID_EVENT_TYPES:
                raise ValueError(f"invalid event_type: {event_type}")
            filters.append("event_type = ?")
            params.append(event_type)

        if not include_cancelled:
            filters.append("event_status <> 'cancelled'")

        where_sql = ""
        if filters:
            where_sql = "WHERE " + " AND ".join(filters)

        conn = self._connect()
        try:
            self.ensure_schema_on_connection(conn)
            row = conn.execute(
                f"""
                SELECT COUNT(*) AS total
                FROM structure_events
                {where_sql}
                """,
                params,
            ).fetchone()
            return int(row["total"])
        finally:
            conn.close()
