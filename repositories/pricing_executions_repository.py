import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from db.config import get_app_db_path
from typing import Any, Optional

DB_PATH = get_app_db_path()

_EXECUTION_COLUMNS = (
    "id, created_at, structure_id, underlying_asset, reference_date, "
    "execution_status, execution_engine, error_message, "
    "duration_ms, number_of_legs, total_quantity, theoretical_value, "
    "pricing_payload, result"
)


class PricingExecutionsRepository:

    def __init__(self, db_path: str | Path | None = None):
        self._db_path = Path(db_path).expanduser().resolve() if db_path is not None else get_app_db_path()
        self._db_path.parent.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ #
    #  conexão                                                             #
    # ------------------------------------------------------------------ #

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self._db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    # ------------------------------------------------------------------ #
    #  escrita                                                             #
    # ------------------------------------------------------------------ #

    def save_execution(
        self,
        pricing_payload: dict[str, Any] | None,
        result: dict[str, Any],
        execution_status: str | None = None,
        execution_engine: str | None = None,
        error_message: str | None = None,
        duration_ms: int | None = None,
        number_of_legs: int | None = None,
        total_quantity: int | None = None,
        theoretical_value: float | None = None,
    ) -> dict[str, Any]:
        if not result:
            raise ValueError("result is required")

        created_at = datetime.now(UTC).isoformat().replace("+00:00", "Z")
        structure_id = pricing_payload.get("structure_id") if pricing_payload else None
        underlying_asset = pricing_payload.get("underlying_asset") if pricing_payload else None
        reference_date = pricing_payload.get("reference_date") if pricing_payload else None

        payload_json = json.dumps(pricing_payload, ensure_ascii=False) if pricing_payload else None
        result_json = json.dumps(result, ensure_ascii=False)

        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO pricing_executions (
                    created_at, structure_id, underlying_asset, reference_date,
                    execution_status, execution_engine, error_message,
                    duration_ms, number_of_legs, total_quantity, theoretical_value,
                    pricing_payload, result
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    created_at, structure_id, underlying_asset, reference_date,
                    execution_status, execution_engine, error_message,
                    duration_ms, number_of_legs, total_quantity, theoretical_value,
                    payload_json, result_json,
                ),
            )
            conn.commit()
            row_id = cur.lastrowid
        finally:
            conn.close()

        return {
            "id": row_id,
            "created_at": created_at,
            "structure_id": structure_id,
            "underlying_asset": underlying_asset,
            "reference_date": reference_date,
            "execution_status": execution_status,
            "execution_engine": execution_engine,
            "error_message": error_message,
            "duration_ms": duration_ms,
            "number_of_legs": number_of_legs,
            "total_quantity": total_quantity,
            "theoretical_value": theoretical_value,
            "pricing_payload": pricing_payload,
            "result": result,
        }

    # ------------------------------------------------------------------ #
    #  leitura                                                             #
    # ------------------------------------------------------------------ #

    def get_execution(self, execution_id: int) -> dict[str, Any] | None:
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute(
                f"SELECT {_EXECUTION_COLUMNS} FROM pricing_executions WHERE id = ?",
                (execution_id,),
            )
            row = cur.fetchone()
            columns = [d[0] for d in cur.description] if cur.description else []
        finally:
            conn.close()

        if row is None:
            return None

        return self._deserialize(self._row_to_dict(row, columns))

    def list_executions(
        self,
        page: int = 1,
        page_size: int = 20,
        status: str | None = None,
        structure_id: int | None = None,
        reference_date: str | None = None,
    ) -> list[dict[str, Any]]:
        filters: list[str] = []
        params: list[Any] = []

        if status is not None:
            filters.append("execution_status = ?")
            params.append(status)
        if structure_id is not None:
            filters.append("structure_id = ?")
            params.append(structure_id)
        if reference_date is not None:
            filters.append("reference_date = ?")
            params.append(reference_date)

        where = ("WHERE " + " AND ".join(filters)) if filters else ""
        offset = (page - 1) * page_size
        params.extend([page_size, offset])

        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute(
                f"""
                SELECT {_EXECUTION_COLUMNS} FROM pricing_executions
                {where}
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
                """,
                params,
            )
            rows = cur.fetchall()
            columns = [d[0] for d in cur.description] if cur.description else []
        finally:
            conn.close()

        return [self._deserialize(self._row_to_dict(r, columns)) for r in rows]

    def count_executions(
        self,
        status: str | None = None,
        structure_id: int | None = None,
        reference_date: str | None = None,
    ) -> int:
        filters: list[str] = []
        params: list[Any] = []

        if status is not None:
            filters.append("execution_status = ?")
            params.append(status)
        if structure_id is not None:
            filters.append("structure_id = ?")
            params.append(structure_id)
        if reference_date is not None:
            filters.append("reference_date = ?")
            params.append(reference_date)

        where = ("WHERE " + " AND ".join(filters)) if filters else ""

        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute(
                f"SELECT COUNT(*) FROM pricing_executions {where}",
                params,
            )
            return cur.fetchone()[0]
        finally:
            conn.close()

    def get_latest_by_structure(
        self,
        structure_id: int,
        reference_date: str | None = None,
    ) -> dict[str, Any] | None:
        params: list[Any] = [structure_id]
        date_filter = ""
        if reference_date is not None:
            date_filter = "AND reference_date = ?"
            params.append(reference_date)

        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute(
                f"""
                SELECT {_EXECUTION_COLUMNS} FROM pricing_executions
                WHERE structure_id = ? {date_filter}
                ORDER BY created_at DESC
                LIMIT 1
                """,
                params,
            )
            row = cur.fetchone()
            columns = [d[0] for d in cur.description] if cur.description else []
        finally:
            conn.close()

        return self._deserialize(self._row_to_dict(row, columns)) if row else None

    # ------------------------------------------------------------------ #
    #  helpers internos                                                    #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _row_to_dict(row: Any, columns: list[str] | None = None) -> dict[str, Any]:
        """Converte sqlite3.Row *ou* tupla para dict de forma segura."""
        if isinstance(row, sqlite3.Row):
            return dict(row)
        if isinstance(row, (tuple, list)):
            if not columns:
                raise ValueError(
                    "_row_to_dict: row é tupla mas nenhuma coluna foi fornecida. "
                    "Passe cur.description ao chamar este método."
                )
            return dict(zip(columns, row))
        raise TypeError(f"Tipo de row não suportado: {type(row).__name__}")

    # ------------------------------------------------------------------ #
    #  deserialização                                                      #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _deserialize(row: dict[str, Any]) -> dict[str, Any]:
        for field in ("pricing_payload", "result"):
            val = row.get(field)
            if isinstance(val, str):
                try:
                    row[field] = json.loads(val)
                except (json.JSONDecodeError, ValueError):
                    pass
        return row
