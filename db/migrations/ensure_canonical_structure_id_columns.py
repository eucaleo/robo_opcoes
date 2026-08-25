from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from db.config import APP_DB_PATH
except Exception:  # pragma: no cover
    APP_DB_PATH = PROJECT_ROOT / "dados" / "app.db"


CANONICAL_COLUMNS = (
    ("structure_decisions", "structure_id", "INTEGER"),
    ("payoff_curve_points", "structure_id", "INTEGER"),
    ("payoff_curve_summary", "structure_id", "INTEGER"),
)


CANONICAL_INDEXES = (
    (
        "structure_decisions",
        "structure_id",
        "CREATE INDEX IF NOT EXISTS idx_structure_decisions_sid_ts "
        "ON structure_decisions (structure_id, timestamp)",
    ),
    (
        "payoff_curve_points",
        "structure_id",
        "CREATE INDEX IF NOT EXISTS idx_payoff_points_sid_ts "
        "ON payoff_curve_points (structure_id, timestamp)",
    ),
    (
        "payoff_curve_summary",
        "structure_id",
        "CREATE INDEX IF NOT EXISTS idx_payoff_summary_sid_ref "
        "ON payoff_curve_summary (structure_id, reference_date)",
    ),
)


def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    row = conn.execute(
        """
        SELECT 1
          FROM sqlite_master
         WHERE type = 'table'
           AND name = ?
         LIMIT 1
        """,
        (table_name,),
    ).fetchone()
    return row is not None


def column_exists(conn: sqlite3.Connection, table_name: str, column_name: str) -> bool:
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return any(str(row[1]) == column_name for row in rows)


def ensure_column(
    conn: sqlite3.Connection,
    table_name: str,
    column_name: str,
    column_definition: str,
) -> str:
    if not table_exists(conn, table_name):
        return "missing_table"

    if column_exists(conn, table_name, column_name):
        return "already_exists"

    conn.execute(
        f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}"
    )
    return "added"


def ensure_indexes(conn: sqlite3.Connection) -> dict[str, str]:
    result: dict[str, str] = {}

    for table_name, column_name, ddl in CANONICAL_INDEXES:
        key = f"{table_name}.{column_name}"

        if not table_exists(conn, table_name):
            result[key] = "missing_table"
            continue

        if not column_exists(conn, table_name, column_name):
            result[key] = "missing_column"
            continue

        conn.execute(ddl)
        result[key] = "ensured"

    return result


def run(db_path: str | Path = APP_DB_PATH) -> dict[str, Any]:
    resolved_db_path = Path(db_path).resolve()
    resolved_db_path.parent.mkdir(parents=True, exist_ok=True)

    report: dict[str, Any] = {
        "db_path": str(resolved_db_path),
        "columns": {},
        "indexes": {},
    }

    conn = sqlite3.connect(str(resolved_db_path))
    try:
        conn.execute("PRAGMA journal_mode=WAL")

        for table_name, column_name, column_definition in CANONICAL_COLUMNS:
            key = f"{table_name}.{column_name}"
            report["columns"][key] = ensure_column(
                conn,
                table_name,
                column_name,
                column_definition,
            )

        report["indexes"] = ensure_indexes(conn)

        conn.commit()
        return report
    finally:
        conn.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Garante colunas canônicas structure_id em tabelas derivadas."
    )
    parser.add_argument(
        "--db",
        default=str(APP_DB_PATH),
        help="Caminho do app.db. Default: db.config.APP_DB_PATH.",
    )

    args = parser.parse_args(argv)
    report = run(args.db)

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
