from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path
from typing import Any

try:
    from db.config import APP_DB_PATH
except Exception:  # pragma: no cover - fallback defensivo para execução isolada
    APP_DB_PATH = Path("dados") / "app.db"


PRICING_EXECUTIONS_REQUIRED_COLUMNS = {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "structure_id": "INTEGER",
    "execution_status": "TEXT",
    "pricing_payload": "TEXT",
    "result": "TEXT",
    "error_message": "TEXT",
    "created_at": "TEXT",
    "updated_at": "TEXT",
}


PRICING_EXECUTIONS_ADDABLE_COLUMNS = {
    key: value
    for key, value in PRICING_EXECUTIONS_REQUIRED_COLUMNS.items()
    if key != "id"
}


PRICING_EXECUTIONS_CREATE_SQL = """
CREATE TABLE IF NOT EXISTS pricing_executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    structure_id INTEGER,
    execution_status TEXT NOT NULL DEFAULT 'pending',
    pricing_payload TEXT,
    result TEXT,
    error_message TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
)
"""


def _safe_identifier(identifier: str) -> bool:
    text = str(identifier).strip()
    return bool(text) and all(ch.isalnum() or ch == "_" for ch in text)


def _quote_identifier(identifier: str) -> str:
    text = str(identifier).strip()
    if not _safe_identifier(text):
        raise ValueError(f"identificador sqlite invalido: {identifier!r}")
    return f'"{text}"'


def connect(db_path: str | Path | None = None) -> sqlite3.Connection:
    target = Path(db_path) if db_path is not None else Path(APP_DB_PATH)
    target.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(target))


def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table_name,),
    ).fetchone()
    return row is not None


def table_columns(conn: sqlite3.Connection, table_name: str) -> set[str]:
    quoted = _quote_identifier(table_name)
    rows = conn.execute(f"PRAGMA table_info({quoted})").fetchall()
    return {str(row[1]) for row in rows}


def add_column_if_missing(
    conn: sqlite3.Connection,
    table_name: str,
    column_name: str,
    column_type: str,
) -> bool:
    columns = table_columns(conn, table_name)
    if column_name in columns:
        return False

    quoted_table = _quote_identifier(table_name)
    quoted_column = _quote_identifier(column_name)
    conn.execute(f"ALTER TABLE {quoted_table} ADD COLUMN {quoted_column} {column_type}")
    return True


def ensure_pricing_executions_schema(
    conn: sqlite3.Connection | None = None,
    db_path: str | Path | None = None,
) -> dict[str, Any]:
    # Frente 16 — schema unico oficial de pricing_executions.
    #
    # Contrato minimo:
    # - id
    # - structure_id
    # - execution_status
    # - pricing_payload
    # - result
    # - error_message
    # - created_at
    # - updated_at
    #
    # A migration e idempotente e nao executa operacoes destrutivas.
    owns_connection = conn is None

    if conn is None:
        conn = connect(db_path)

    table = "pricing_executions"

    try:
        existed_before = table_exists(conn, table)

        if not existed_before:
            conn.execute(PRICING_EXECUTIONS_CREATE_SQL)

        added_columns: list[str] = []
        unfixable_missing_columns: list[str] = []

        existing_columns = table_columns(conn, table)

        if "id" not in existing_columns:
            unfixable_missing_columns.append("id")

        for column_name, column_type in PRICING_EXECUTIONS_ADDABLE_COLUMNS.items():
            if add_column_if_missing(conn, table, column_name, column_type):
                added_columns.append(column_name)

        final_columns = table_columns(conn, table)
        missing_columns = [
            column_name
            for column_name in PRICING_EXECUTIONS_REQUIRED_COLUMNS
            if column_name not in final_columns
        ]

        status = "ok"
        if missing_columns:
            status = "incomplete"

        result = {
            "table": table,
            "status": status,
            "created": not existed_before,
            "added_columns": added_columns,
            "required_columns": list(PRICING_EXECUTIONS_REQUIRED_COLUMNS),
            "missing_columns": missing_columns,
            "unfixable_missing_columns": unfixable_missing_columns,
        }

        conn.commit()
        return result
    except Exception:
        conn.rollback()
        raise
    finally:
        if owns_connection:
            conn.close()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Frente 16: garante schema unico oficial de pricing_executions."
    )
    parser.add_argument(
        "--db",
        dest="db_path",
        default=None,
        help="Caminho opcional do SQLite. Default: db.config.APP_DB_PATH.",
    )
    args = parser.parse_args()

    result = ensure_pricing_executions_schema(db_path=args.db_path)
    print(f"[OK] pricing_executions: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
