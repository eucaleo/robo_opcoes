#!/usr/bin/env python3
from __future__ import annotations

import json
import sqlite3
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "dados" / "app.db"
OUTPUT_DIR = BASE_DIR / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class SnapshotKeyIssue:
    table_name: str
    issue_type: str
    details: str
    severity: str = "error"


AUDIT_RULES = {
    "manual_analise_robo_legs": {
        "require_key_candidate": False,
    },
    "rtd_analise_raiox": {
        "require_key_candidate": False,
    },
    "rtd_analise_robo": {
        "require_key_candidate": False,
    },
    "rtd_analise_robo_legs": {
        "require_key_candidate": False,
    },
    "rtd_configuracoes": {
        "require_key_candidate": False,
    },
    "rtd_consolidacoes": {
        "require_key_candidate": False,
    },
    "rtd_encerramentos_manuais": {
        "require_key_candidate": False,
    },
    "rtd_hist_robo": {
        "require_key_candidate": False,
    },
    "rtd_rolls_detectados": {
        "require_key_candidate": False,
    },
    "structure_legs": {
        "require_key_candidate": False,
        "non_unique_foreign_keys": ["structure_id"],
    },
}

DEFAULT_KEY_CANDIDATES = {
    "id",
    "uuid",
    "snapshot_id",
    "record_id",
    "external_id",
    "key",
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
    return [row[0] for row in rows]


def get_table_columns(conn: sqlite3.Connection, table_name: str) -> list[str]:
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return [row[1] for row in rows]


def find_possible_key_columns(columns: list[str], table_name: str) -> list[str]:
    rules = AUDIT_RULES.get(table_name, {})
    explicit = rules.get("unique_key_candidates")
    if explicit is not None:
        return [c for c in explicit if c in columns]

    candidates = []
    for col in columns:
        lower = col.lower()
        if lower in DEFAULT_KEY_CANDIDATES or lower.endswith("_id"):
            candidates.append(col)
    return candidates


def audit_snapshot_keys(conn: sqlite3.Connection) -> dict[str, Any]:
    issues: list[SnapshotKeyIssue] = []

    for table in get_tables(conn):
        columns = get_table_columns(conn, table)
        rules = AUDIT_RULES.get(table, {})
        require_key_candidate = rules.get("require_key_candidate", True)
        non_unique_foreign_keys = set(rules.get("non_unique_foreign_keys", []))

        key_candidates = find_possible_key_columns(columns, table)

        if require_key_candidate and not key_candidates:
            issues.append(
                SnapshotKeyIssue(
                    table_name=table,
                    issue_type="missing_key_candidate",
                    details="Nenhuma coluna candidata a chave foi encontrada.",
                )
            )
            continue

        for key_col in key_candidates:
            if key_col in non_unique_foreign_keys:
                continue

            total_rows, non_null_keys, distinct_keys = conn.execute(
                f"""
                SELECT COUNT(*),
                       COUNT({key_col}),
                       COUNT(DISTINCT {key_col})
                FROM {table}
                """
            ).fetchone()

            if non_null_keys < total_rows:
                issues.append(
                    SnapshotKeyIssue(
                        table_name=table,
                        issue_type="null_keys",
                        details=(
                            f"Coluna '{key_col}' possui valores nulos: "
                            f"{total_rows - non_null_keys} de {total_rows}."
                        ),
                    )
                )

            if distinct_keys < non_null_keys:
                issues.append(
                    SnapshotKeyIssue(
                        table_name=table,
                        issue_type="duplicate_keys",
                        details=(
                            f"Coluna '{key_col}' possui duplicidades: "
                            f"{non_null_keys - distinct_keys} registros repetidos."
                        ),
                    )
                )

    return {
        "database": str(DB_PATH),
        "issues_found": len(issues),
        "issues": [asdict(issue) for issue in issues],
    }


def main() -> int:
    if not DB_PATH.exists():
        print(f"ERRO: banco não encontrado em: {DB_PATH}", file=sys.stderr)
        return 2

    conn = sqlite3.connect(DB_PATH)
    try:
        result = audit_snapshot_keys(conn)
    finally:
        conn.close()

    output_file = OUTPUT_DIR / "audit_snapshot_keys.json"
    output_file.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Relatório salvo em: {output_file}")
    print(f"Issues encontradas: {result['issues_found']}")

    has_error = any(issue.get("severity", "error") == "error" for issue in result["issues"])
    return 1 if has_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
