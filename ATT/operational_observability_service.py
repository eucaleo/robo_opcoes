from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import quote


DEFAULT_CRITICAL_TABLES = (
    "structures",
    "structure_legs",
    "pricing_executions",
    "payoff_curve_points",
    "structure_snapshots",
    "structure_leg_snapshots",
)


@dataclass(frozen=True)
class OperationalObservabilitySummary:
    database_path: str
    database_exists: bool
    table_count: int
    total_record_count: int
    critical_tables_present: dict[str, bool] = field(default_factory=dict)
    retention_status: str = "not_available"
    retention_total_candidates: int = 0
    health: str = "unknown"
    message: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "database_path": self.database_path,
            "database_exists": self.database_exists,
            "table_count": self.table_count,
            "total_record_count": self.total_record_count,
            "critical_tables_present": dict(self.critical_tables_present),
            "retention_status": self.retention_status,
            "retention_total_candidates": self.retention_total_candidates,
            "health": self.health,
            "message": self.message,
        }


def build_operational_observability_summary(
    database_path: str | Path = "dados/app.db",
    *,
    critical_tables: tuple[str, ...] = DEFAULT_CRITICAL_TABLES,
    include_retention_simulation: bool = True,
    retention_days: int = 365,
    retention_today: str | None = None,
) -> OperationalObservabilitySummary:
    path = Path(database_path)

    if not path.exists():
        present = {name: False for name in critical_tables}
        return OperationalObservabilitySummary(
            database_path=str(database_path),
            database_exists=False,
            table_count=0,
            total_record_count=0,
            critical_tables_present=present,
            retention_status="not_available",
            retention_total_candidates=0,
            health="warning",
            message="Banco local nao encontrado.",
        )

    table_names = _list_tables_read_only(path)
    table_count = len(table_names)
    total_record_count = _count_total_records_read_only(path, table_names)
    present = {name: name in table_names for name in critical_tables}

    retention_status = "not_requested"
    retention_total_candidates = 0

    if include_retention_simulation:
        retention_status, retention_total_candidates = _simulate_retention_read_only(
            path,
            retention_days=retention_days,
            retention_today=retention_today,
        )

    health = _resolve_health(
        database_exists=True,
        critical_tables_present=present,
        retention_total_candidates=retention_total_candidates,
    )

    message = _build_message(
        database_exists=True,
        table_count=table_count,
        total_record_count=total_record_count,
        retention_status=retention_status,
        retention_total_candidates=retention_total_candidates,
        health=health,
    )

    return OperationalObservabilitySummary(
        database_path=str(database_path),
        database_exists=True,
        table_count=table_count,
        total_record_count=total_record_count,
        critical_tables_present=present,
        retention_status=retention_status,
        retention_total_candidates=retention_total_candidates,
        health=health,
        message=message,
    )


def format_operational_observability_summary(
    summary: OperationalObservabilitySummary,
) -> str:
    lines = [
        "Resumo de observabilidade operacional",
        f"Banco: {summary.database_path}",
        f"Existe: {_yes_no(summary.database_exists)}",
        f"Tabelas observadas: {summary.table_count}",
        f"Registros observados: {summary.total_record_count}",
        f"Retencao: {summary.retention_status}",
        f"Candidatos de retencao: {summary.retention_total_candidates}",
        f"Saude: {summary.health}",
        f"Mensagem: {summary.message}",
        "",
        "Tabelas criticas:",
    ]

    for table_name, is_present in sorted(summary.critical_tables_present.items()):
        lines.append(f"- {table_name}: {_yes_no(is_present)}")

    return "\n".join(lines)


def _connect_read_only(path: Path) -> sqlite3.Connection:
    resolved = path.resolve().as_posix()
    uri = "file:" + quote(resolved, safe="/:") + "?mode=ro"
    return sqlite3.connect(uri, uri=True)


def _list_tables_read_only(path: Path) -> list[str]:
    with _connect_read_only(path) as connection:
        cursor = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        )
        return [row[0] for row in cursor.fetchall()]


def _count_total_records_read_only(path: Path, table_names: list[str]) -> int:
    total = 0

    with _connect_read_only(path) as connection:
        for table_name in table_names:
            cursor = connection.execute(
                f"SELECT COUNT(*) FROM {_quote_identifier(table_name)}"
            )
            total += int(cursor.fetchone()[0])

    return total


def _simulate_retention_read_only(
    path: Path,
    *,
    retention_days: int,
    retention_today: str | None,
) -> tuple[str, int]:
    try:
        from ATT.database_retention_simulation_service import (
            simulate_database_retention,
        )

        kwargs: dict[str, Any] = {
            "retention_days": retention_days,
        }

        if retention_today is not None:
            kwargs["today"] = retention_today

        report = simulate_database_retention(str(path), **kwargs)
        return "simulated", _extract_total_candidates(report)
    except Exception:
        return "unavailable", 0


def _extract_total_candidates(report: Any) -> int:
    if isinstance(report, dict):
        value = report.get("total_candidates", 0)
        return int(value or 0)

    value = getattr(report, "total_candidates", None)

    if value is not None:
        return int(value or 0)

    value = getattr(report, "total_candidate_count", None)

    if value is not None:
        return int(value or 0)

    return 0


def _resolve_health(
    *,
    database_exists: bool,
    critical_tables_present: dict[str, bool],
    retention_total_candidates: int,
) -> str:
    if not database_exists:
        return "warning"

    if retention_total_candidates > 0:
        return "attention"

    if not all(critical_tables_present.values()):
        return "attention"

    return "ok"


def _build_message(
    *,
    database_exists: bool,
    table_count: int,
    total_record_count: int,
    retention_status: str,
    retention_total_candidates: int,
    health: str,
) -> str:
    if not database_exists:
        return "Banco local nao encontrado."

    return (
        "Banco observado com "
        f"{table_count} tabelas, "
        f"{total_record_count} registros, "
        f"retencao {retention_status}, "
        f"{retention_total_candidates} candidatos e saude {health}."
    )


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _yes_no(value: bool) -> str:
    return "sim" if value else "nao"
