from __future__ import annotations

import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


DIRECT_RETENTION_POLICIES: dict[str, tuple[str, ...]] = {
    "payoff_curve_points": ("timestamp", "created_at"),
    "pricing_executions": ("created_at", "reference_date"),
    "structure_snapshots": ("created_at", "reference_date"),
}


OUT_OF_SCOPE_TABLES: dict[str, str] = {
    "rtd_option_quotes": "cotacoes atuais ou ultimo estado conhecido",
    "rtd_underlying_quotes": "cotacoes atuais ou ultimo estado conhecido",
    "structure_audit_log": "sem criterio temporal seguro na politica inicial",
    "structure_decisions": "decisoes operacionais exigem auditoria semantica",
    "structure_events": "fora da primeira rotina",
    "structure_legs": "tabela mestre de pernas",
    "structures": "tabela mestre de estruturas",
}


DEPENDENT_TABLE = "structure_leg_snapshots"
DEPENDENT_PARENT_TABLE = "structure_snapshots"
DEPENDENT_JOIN_COLUMN = "snapshot_id"
PARENT_ID_COLUMN = "id"


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _normalize_today(today: date | datetime | str | None) -> date:
    if today is None:
        return date.today()

    if isinstance(today, datetime):
        return today.date()

    if isinstance(today, date):
        return today

    return date.fromisoformat(str(today)[:10])


def _table_exists(connection: sqlite3.Connection, table_name: str) -> bool:
    row = connection.execute(
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


def _column_names(connection: sqlite3.Connection, table_name: str) -> set[str]:
    rows = connection.execute(
        f"PRAGMA table_info({_quote_identifier(table_name)})"
    ).fetchall()

    return {row["name"] for row in rows}


def _choose_existing_column(
    columns: set[str],
    candidates: tuple[str, ...],
) -> str | None:
    for candidate in candidates:
        if candidate in columns:
            return candidate

    return None


def _count_table_rows(connection: sqlite3.Connection, table_name: str) -> int:
    row = connection.execute(
        f"SELECT COUNT(*) AS total FROM {_quote_identifier(table_name)}"
    ).fetchone()

    return int(row["total"])


def _count_direct_candidates(
    connection: sqlite3.Connection,
    table_name: str,
    criterion_column: str,
    cutoff_iso: str,
) -> int:
    row = connection.execute(
        f"""
        SELECT COUNT(*) AS total
        FROM {_quote_identifier(table_name)}
        WHERE {_quote_identifier(criterion_column)} IS NOT NULL
          AND datetime({_quote_identifier(criterion_column)}) < datetime(?)
        """,
        (cutoff_iso,),
    ).fetchone()

    return int(row["total"])


def _count_dependent_candidates(
    connection: sqlite3.Connection,
    parent_criterion_column: str,
    cutoff_iso: str,
) -> int:
    row = connection.execute(
        f"""
        SELECT COUNT(*) AS total
        FROM {_quote_identifier(DEPENDENT_TABLE)} child
        WHERE child.{_quote_identifier(DEPENDENT_JOIN_COLUMN)} IN (
            SELECT parent.{_quote_identifier(PARENT_ID_COLUMN)}
            FROM {_quote_identifier(DEPENDENT_PARENT_TABLE)} parent
            WHERE parent.{_quote_identifier(parent_criterion_column)} IS NOT NULL
              AND datetime(parent.{_quote_identifier(parent_criterion_column)}) < datetime(?)
        )
        """,
        (cutoff_iso,),
    ).fetchone()

    return int(row["total"])


def simulate_database_retention(
    db_path: str | Path,
    retention_days: int = 365,
    today: date | datetime | str | None = None,
) -> dict[str, Any]:
    path = Path(db_path)
    normalized_today = _normalize_today(today)
    cutoff_date = normalized_today - timedelta(days=retention_days)
    cutoff_iso = cutoff_date.isoformat()

    report: dict[str, Any] = {
        "database_path": str(path),
        "exists": path.exists(),
        "mode": "simulated",
        "retention_days": retention_days,
        "today": normalized_today.isoformat(),
        "cutoff_date": cutoff_iso,
        "total_candidates": 0,
        "tables": [],
    }

    if not path.exists():
        return report

    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row

    try:
        connection.execute("PRAGMA query_only = ON")

        for table_name, candidate_columns in DIRECT_RETENTION_POLICIES.items():
            if not _table_exists(connection, table_name):
                report["tables"].append(
                    {
                        "name": table_name,
                        "status": "missing_table",
                        "scope": "candidate",
                        "criterion_column": None,
                        "row_count": 0,
                        "candidate_count": 0,
                    }
                )
                continue

            columns = _column_names(connection, table_name)
            criterion_column = _choose_existing_column(columns, candidate_columns)
            row_count = _count_table_rows(connection, table_name)

            if criterion_column is None:
                report["tables"].append(
                    {
                        "name": table_name,
                        "status": "missing_criterion_column",
                        "scope": "candidate",
                        "criterion_column": None,
                        "row_count": row_count,
                        "candidate_count": 0,
                    }
                )
                continue

            candidate_count = _count_direct_candidates(
                connection,
                table_name,
                criterion_column,
                cutoff_iso,
            )

            report["tables"].append(
                {
                    "name": table_name,
                    "status": "simulated",
                    "scope": "candidate",
                    "criterion_column": criterion_column,
                    "row_count": row_count,
                    "candidate_count": candidate_count,
                }
            )
            report["total_candidates"] += candidate_count

        report["tables"].append(
            _simulate_dependent_table(connection, cutoff_iso)
        )
        report["total_candidates"] += report["tables"][-1]["candidate_count"]

        for table_name, reason in OUT_OF_SCOPE_TABLES.items():
            if _table_exists(connection, table_name):
                row_count = _count_table_rows(connection, table_name)
            else:
                row_count = 0

            report["tables"].append(
                {
                    "name": table_name,
                    "status": "out_of_scope",
                    "scope": "ignored",
                    "criterion_column": None,
                    "row_count": row_count,
                    "candidate_count": 0,
                    "reason": reason,
                }
            )

        return report

    finally:
        connection.close()


def _simulate_dependent_table(
    connection: sqlite3.Connection,
    cutoff_iso: str,
) -> dict[str, Any]:
    if not _table_exists(connection, DEPENDENT_TABLE):
        return {
            "name": DEPENDENT_TABLE,
            "status": "missing_table",
            "scope": "dependent_candidate",
            "criterion_column": None,
            "row_count": 0,
            "candidate_count": 0,
            "depends_on": DEPENDENT_PARENT_TABLE,
        }

    row_count = _count_table_rows(connection, DEPENDENT_TABLE)

    if not _table_exists(connection, DEPENDENT_PARENT_TABLE):
        return {
            "name": DEPENDENT_TABLE,
            "status": "missing_parent_table",
            "scope": "dependent_candidate",
            "criterion_column": None,
            "row_count": row_count,
            "candidate_count": 0,
            "depends_on": DEPENDENT_PARENT_TABLE,
        }

    child_columns = _column_names(connection, DEPENDENT_TABLE)
    parent_columns = _column_names(connection, DEPENDENT_PARENT_TABLE)

    if DEPENDENT_JOIN_COLUMN not in child_columns:
        return {
            "name": DEPENDENT_TABLE,
            "status": "missing_join_column",
            "scope": "dependent_candidate",
            "criterion_column": None,
            "row_count": row_count,
            "candidate_count": 0,
            "depends_on": DEPENDENT_PARENT_TABLE,
        }

    if PARENT_ID_COLUMN not in parent_columns:
        return {
            "name": DEPENDENT_TABLE,
            "status": "missing_parent_id_column",
            "scope": "dependent_candidate",
            "criterion_column": None,
            "row_count": row_count,
            "candidate_count": 0,
            "depends_on": DEPENDENT_PARENT_TABLE,
        }

    parent_criterion_column = _choose_existing_column(
        parent_columns,
        DIRECT_RETENTION_POLICIES[DEPENDENT_PARENT_TABLE],
    )

    if parent_criterion_column is None:
        return {
            "name": DEPENDENT_TABLE,
            "status": "missing_parent_criterion_column",
            "scope": "dependent_candidate",
            "criterion_column": None,
            "row_count": row_count,
            "candidate_count": 0,
            "depends_on": DEPENDENT_PARENT_TABLE,
        }

    candidate_count = _count_dependent_candidates(
        connection,
        parent_criterion_column,
        cutoff_iso,
    )

    return {
        "name": DEPENDENT_TABLE,
        "status": "simulated_dependent",
        "scope": "dependent_candidate",
        "criterion_column": parent_criterion_column,
        "row_count": row_count,
        "candidate_count": candidate_count,
        "depends_on": DEPENDENT_PARENT_TABLE,
        "join_column": DEPENDENT_JOIN_COLUMN,
    }


def format_database_retention_simulation(report: dict[str, Any]) -> str:
    lines = [
        "Simulacao de retencao do banco",
        f"Banco: {report['database_path']}",
        f"Existe: {'sim' if report['exists'] else 'nao'}",
        f"Modo: {report['mode']}",
        f"Janela em dias: {report['retention_days']}",
        f"Data de referencia: {report['today']}",
        f"Data limite: {report['cutoff_date']}",
        f"Total de candidatos: {report['total_candidates']}",
    ]

    for table in report["tables"]:
        lines.extend(
            [
                "",
                f"Tabela: {table['name']}",
                f"Status: {table['status']}",
                f"Escopo: {table['scope']}",
                f"Registros: {table['row_count']}",
                f"Candidatos: {table['candidate_count']}",
                f"Criterio: {table['criterion_column'] or 'nenhum'}",
            ]
        )

        if table.get("depends_on"):
            lines.append(f"Depende de: {table['depends_on']}")

        if table.get("reason"):
            lines.append(f"Motivo: {table['reason']}")

    return "\n".join(lines)
