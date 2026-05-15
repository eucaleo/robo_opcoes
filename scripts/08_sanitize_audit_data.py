#!/usr/bin/env python3
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "dados" / "app.db"
OUTPUT_DIR = BASE_DIR / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


TEXT_LIKE_COLUMNS = {
    "id",
    "uuid",
    "snapshot_id",
    "record_id",
    "external_id",
    "key",
    "name",
    "status",
    "type",
}


def get_tables(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
          AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """
    ).fetchall()
    return [r[0] for r in rows]


def get_columns(conn: sqlite3.Connection, table: str) -> list[tuple]:
    return conn.execute(f"PRAGMA table_info({table})").fetchall()


def sanitize_table(conn: sqlite3.Connection, table: str) -> dict[str, Any]:
    changes = {
        "table": table,
        "trim_updates": 0,
        "blank_to_null_updates": 0,
    }

    columns = get_columns(conn, table)
    for col in columns:
        col_name = col[1]
        col_type = (col[2] or "").upper()

        if "TEXT" in col_type or col_name.lower() in TEXT_LIKE_COLUMNS:
            cur = conn.execute(
                f"""
                UPDATE {table}
                SET {col_name} = TRIM({col_name})
                WHERE {col_name} IS NOT NULL
                  AND {col_name} != TRIM({col_name})
                """
            )
            changes["trim_updates"] += cur.rowcount

            cur = conn.execute(
                f"""
                UPDATE {table}
                SET {col_name} = NULL
                WHERE {col_name} IS NOT NULL
                  AND TRIM({col_name}) = ''
                """
            )
            changes["blank_to_null_updates"] += cur.rowcount

    return changes


def main() -> int:
    if not DB_PATH.exists():
        print(f"ERRO: banco não encontrado em: {DB_PATH}", file=sys.stderr)
        return 2

    conn = sqlite3.connect(DB_PATH)
    conn.isolation_level = None

    report: dict[str, Any] = {
        "database": str(DB_PATH),
        "tables": [],
        "success": True,
    }

    try:
        conn.execute("BEGIN")
        for table in get_tables(conn):
            report["tables"].append(sanitize_table(conn, table))
        conn.execute("COMMIT")
    except Exception as exc:
        conn.execute("ROLLBACK")
        report["success"] = False
        report["error"] = str(exc)
        print(f"ERRO durante saneamento: {exc}", file=sys.stderr)
        output_file = OUTPUT_DIR / "sanitize_audit_data.json"
        output_file.write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return 1
    finally:
        conn.close()

    output_file = OUTPUT_DIR / "sanitize_audit_data.json"
    output_file.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Relatório salvo em: {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
