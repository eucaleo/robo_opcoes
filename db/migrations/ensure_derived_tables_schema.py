from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path
from typing import Any

try:
    from db.config import APP_DB_PATH
except Exception:  # pragma: no cover
    APP_DB_PATH = Path("dados") / "app.db"


PAYOFF_CURVE_SUMMARY_CREATE_SQL = """
CREATE TABLE IF NOT EXISTS payoff_curve_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    structure_id INTEGER,
    aba TEXT,
    timestamp TEXT,
    spot_ref REAL,
    total_premium REAL,
    payoff_at_spot REAL,
    max_profit REAL,
    max_loss REAL,
    breakeven_points TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
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


def column_exists(conn: sqlite3.Connection, table_name: str, column_name: str) -> bool:
    return column_name in table_columns(conn, table_name)


def add_column_if_missing(
    conn: sqlite3.Connection,
    table_name: str,
    column_name: str,
    column_type: str,
) -> bool:
    if column_exists(conn, table_name, column_name):
        return False

    quoted_table = _quote_identifier(table_name)
    quoted_column = _quote_identifier(column_name)
    conn.execute(f"ALTER TABLE {quoted_table} ADD COLUMN {quoted_column} {column_type}")
    return True


def ensure_structure_decisions_schema(conn: sqlite3.Connection) -> dict[str, Any]:
    table = "structure_decisions"

    if not table_exists(conn, table):
        return {
            "table": table,
            "status": "skipped_table_missing",
            "added_columns": [],
        }

    added_columns: list[str] = []

    if add_column_if_missing(conn, table, "structure_id", "INTEGER"):
        added_columns.append("structure_id")

    return {
        "table": table,
        "status": "ok",
        "added_columns": added_columns,
    }


def ensure_payoff_curve_points_schema(conn: sqlite3.Connection) -> dict[str, Any]:
    table = "payoff_curve_points"

    if not table_exists(conn, table):
        return {
            "table": table,
            "status": "skipped_table_missing",
            "added_columns": [],
        }

    added_columns: list[str] = []

    if add_column_if_missing(conn, table, "structure_id", "INTEGER"):
        added_columns.append("structure_id")

    return {
        "table": table,
        "status": "ok",
        "added_columns": added_columns,
    }


def ensure_payoff_curve_summary_schema(conn: sqlite3.Connection) -> dict[str, Any]:
    table = "payoff_curve_summary"
    existed_before = table_exists(conn, table)

    conn.execute(PAYOFF_CURVE_SUMMARY_CREATE_SQL)

    added_columns: list[str] = []

    if existed_before and add_column_if_missing(conn, table, "structure_id", "INTEGER"):
        added_columns.append("structure_id")

    return {
        "table": table,
        "status": "ok",
        "created": not existed_before,
        "added_columns": added_columns,
    }


def ensure_derived_tables_schema(
    conn: sqlite3.Connection | None = None,
    db_path: str | Path | None = None,
) -> dict[str, Any]:
    """
    Frente 15 — schema minimo canonico das tabelas derivadas.

    Contrato:
    - structure_decisions deve aceitar structure_id, se a tabela existir.
    - payoff_curve_points deve aceitar structure_id, se a tabela existir.
    - payoff_curve_summary passa a ser tabela derivada oficial minima.
    - A execucao e idempotente.
    - A execucao nao usa operacao destrutiva.
    """
    owns_connection = conn is None

    if conn is None:
        conn = connect(db_path)

    try:
        result = {
            "structure_decisions": ensure_structure_decisions_schema(conn),
            "payoff_curve_points": ensure_payoff_curve_points_schema(conn),
            "payoff_curve_summary": ensure_payoff_curve_summary_schema(conn),
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
        description="Frente 15: garante schema minimo canonico das tabelas derivadas."
    )
    parser.add_argument(
        "--db",
        dest="db_path",
        default=None,
        help="Caminho opcional do SQLite. Default: db.config.APP_DB_PATH.",
    )
    args = parser.parse_args()

    result = ensure_derived_tables_schema(db_path=args.db_path)

    for key, value in result.items():
        print(f"[OK] {key}: {value}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
