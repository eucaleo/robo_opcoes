#!/usr/bin/env python
"""
Audita a tabela rtd_option_quotes em um banco SQLite.

Uso típico:

    python scripts/audit_rtd_option_quotes.py --db dados/app.db
    python scripts/audit_rtd_option_quotes.py --db dados/app.db --json

O script não altera o banco.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any


TABLE_NAME = "rtd_option_quotes"

REQUIRED_COLUMNS = {
    "codigo_opcao",
    "ativo_base",
    "call_put",
    "strike",
    "vencimento",
    "ultimo_preco",
    "ultima_quantidade",
    "bid",
    "ask",
    "volume",
    "iv",
    "delta",
    "gamma",
    "theta",
    "vega",
    "source",
    "raw_json",
    "updated_at",
    "created_at",
}


def connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def table_exists(conn: sqlite3.Connection, table_name: str = TABLE_NAME) -> bool:
    row = conn.execute(
        """
        SELECT 1
        FROM sqlite_master
        WHERE type = 'table'
          AND name = ?
        """,
        (table_name,),
    ).fetchone()
    return row is not None


def table_columns(conn: sqlite3.Connection, table_name: str = TABLE_NAME) -> list[str]:
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return [str(row["name"]) for row in rows]


def scalar(conn: sqlite3.Connection, sql: str, params: tuple[Any, ...] = ()) -> Any:
    row = conn.execute(sql, params).fetchone()
    if row is None:
        return None
    return row[0]


def audit_database(db_path: str | Path, max_age_minutes: int = 30) -> dict[str, Any]:
    db_path = Path(db_path)

    result: dict[str, Any] = {
        "database": str(db_path),
        "table": TABLE_NAME,
        "status": "ok",
        "errors": [],
        "warnings": [],
        "metrics": {},
        "columns": [],
        "missing_columns": [],
    }

    if not db_path.exists():
        result["status"] = "error"
        result["errors"].append("database file not found")
        return result

    with connect(db_path) as conn:
        if not table_exists(conn):
            result["status"] = "error"
            result["errors"].append(f"table not found: {TABLE_NAME}")
            return result

        columns = table_columns(conn)
        column_set = set(columns)

        result["columns"] = columns

        missing_columns = sorted(REQUIRED_COLUMNS - column_set)
        result["missing_columns"] = missing_columns

        if missing_columns:
            result["errors"].append(
                "missing required columns: " + ", ".join(missing_columns)
            )

        row_count = int(
            scalar(conn, f"SELECT COUNT(*) FROM {TABLE_NAME}") or 0
        )
        result["metrics"]["row_count"] = row_count

        if row_count == 0:
            result["warnings"].append("table is empty")

        if "codigo_opcao" in column_set:
            missing_codigo_count = int(
                scalar(
                    conn,
                    f"""
                    SELECT COUNT(*)
                    FROM {TABLE_NAME}
                    WHERE codigo_opcao IS NULL
                       OR TRIM(codigo_opcao) = ''
                    """,
                )
                or 0
            )

            distinct_codigo_count = int(
                scalar(
                    conn,
                    f"""
                    SELECT COUNT(DISTINCT codigo_opcao)
                    FROM {TABLE_NAME}
                    WHERE codigo_opcao IS NOT NULL
                      AND TRIM(codigo_opcao) <> ''
                    """,
                )
                or 0
            )

            duplicate_codigo_count = int(
                scalar(
                    conn,
                    f"""
                    SELECT COUNT(*)
                    FROM (
                        SELECT codigo_opcao
                        FROM {TABLE_NAME}
                        WHERE codigo_opcao IS NOT NULL
                          AND TRIM(codigo_opcao) <> ''
                        GROUP BY codigo_opcao
                        HAVING COUNT(*) > 1
                    ) duplicated
                    """,
                )
                or 0
            )

            result["metrics"]["missing_codigo_count"] = missing_codigo_count
            result["metrics"]["distinct_codigo_count"] = distinct_codigo_count
            result["metrics"]["duplicate_codigo_count"] = duplicate_codigo_count

            if missing_codigo_count > 0:
                result["errors"].append(
                    f"rows with missing codigo_opcao: {missing_codigo_count}"
                )

            if duplicate_codigo_count > 0:
                result["errors"].append(
                    f"duplicated codigo_opcao groups: {duplicate_codigo_count}"
                )

        if "updated_at" in column_set and max_age_minutes > 0:
            stale_rows = int(
                scalar(
                    conn,
                    f"""
                    SELECT COUNT(*)
                    FROM {TABLE_NAME}
                    WHERE updated_at IS NOT NULL
                      AND datetime(updated_at) < datetime('now', 'localtime', ?)
                    """,
                    (f"-{int(max_age_minutes)} minutes",),
                )
                or 0
            )

            result["metrics"]["stale_rows"] = stale_rows
            result["metrics"]["max_age_minutes"] = int(max_age_minutes)

            if stale_rows > 0:
                result["warnings"].append(
                    f"rows older than {int(max_age_minutes)} minutes: {stale_rows}"
                )

    if result["errors"]:
        result["status"] = "error"
    elif result["warnings"]:
        result["status"] = "warn"
    else:
        result["status"] = "ok"

    return result


def print_human_report(result: dict[str, Any]) -> None:
    print("Auditoria rtd_option_quotes")
    print(f"Banco: {result['database']}")
    print(f"Tabela: {result['table']}")
    print(f"Status: {result['status']}")

    metrics = result.get("metrics") or {}
    if metrics:
        print("")
        print("Métricas:")
        for key in sorted(metrics):
            print(f"- {key}: {metrics[key]}")

    missing_columns = result.get("missing_columns") or []
    if missing_columns:
        print("")
        print("Colunas obrigatórias ausentes:")
        for column in missing_columns:
            print(f"- {column}")

    warnings = result.get("warnings") or []
    if warnings:
        print("")
        print("Avisos:")
        for warning in warnings:
            print(f"- {warning}")

    errors = result.get("errors") or []
    if errors:
        print("")
        print("Erros:")
        for error in errors:
            print(f"- {error}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audita a tabela rtd_option_quotes em um banco SQLite."
    )
    parser.add_argument(
        "--db",
        default="dados/app.db",
        help="Caminho do banco SQLite. Padrão: dados/app.db",
    )
    parser.add_argument(
        "--max-age-minutes",
        type=int,
        default=30,
        help="Idade máxima esperada para updated_at. Use 0 para desabilitar.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Imprime relatório em JSON.",
    )
    parser.add_argument(
        "--fail-on-warn",
        action="store_true",
        help="Retorna exit code 1 também quando houver avisos.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    result = audit_database(
        db_path=args.db,
        max_age_minutes=args.max_age_minutes,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print_human_report(result)

    if result["status"] == "error":
        return 2

    if result["status"] == "warn" and args.fail_on_warn:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
