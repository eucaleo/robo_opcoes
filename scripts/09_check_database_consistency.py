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


KEY_CANDIDATES = ["id", "uuid", "snapshot_id", "record_id", "external_id"]

TABLE_RULES = {
    "rtd_encerramentos_manuais": {
        "allow_empty": True,
        "empty_severity": "warning",
    },
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


def get_columns(conn: sqlite3.Connection, table: str) -> list[str]:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return [r[1] for r in rows]


def main() -> int:
    if not DB_PATH.exists():
        print(f"ERRO: banco não encontrado em: {DB_PATH}", file=sys.stderr)
        return 2

    conn = sqlite3.connect(DB_PATH)
    report: dict[str, Any] = {
        "database": str(DB_PATH),
        "issues": [],
    }
    has_error = False

    try:
        for table in get_tables(conn):
            columns = get_columns(conn, table)
            total_rows = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            rules = TABLE_RULES.get(table, {})
            allow_empty = rules.get("allow_empty", False)
            empty_severity = rules.get("empty_severity", "error")

            if total_rows == 0 and not allow_empty:
                report["issues"].append({
                    "table": table,
                    "type": "empty_table",
                    "severity": "error",
                    "details": "Tabela vazia.",
                })
                has_error = True
            elif total_rows == 0 and allow_empty:
                report["issues"].append({
                    "table": table,
                    "type": "empty_table",
                    "severity": empty_severity,
                    "details": "Tabela vazia, mas permitida pela regra configurada.",
                })

            for key in KEY_CANDIDATES:
                if key in columns:
                    total, non_null, distinct = conn.execute(
                        f"""
                        SELECT COUNT(*), COUNT({key}), COUNT(DISTINCT {key})
                        FROM {table}
                        """
                    ).fetchone()

                    if non_null < total:
                        report["issues"].append({
                            "table": table,
                            "type": "null_key_values",
                            "severity": "error",
                            "column": key,
                            "details": f"{total - non_null} chaves nulas.",
                        })
                        has_error = True

                    if distinct < non_null:
                        report["issues"].append({
                            "table": table,
                            "type": "duplicate_key_values",
                            "severity": "error",
                            "column": key,
                            "details": f"{non_null - distinct} chaves duplicadas.",
                        })
                        has_error = True

    finally:
        conn.close()

    output_file = OUTPUT_DIR / "database_consistency.json"
    output_file.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Relatório salvo em: {output_file}")
    print(f"Issues encontradas: {len(report['issues'])}")

    return 1 if has_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
