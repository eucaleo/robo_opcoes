import sqlite3
from pathlib import Path

from ATT.operational_observability_service import (
    build_operational_observability_summary,
    format_operational_observability_summary,
)


def test_build_summary_for_missing_database(tmp_path):
    database_path = tmp_path / "missing.db"

    summary = build_operational_observability_summary(
        database_path,
        include_retention_simulation=False,
    )

    assert summary.database_exists is False
    assert summary.table_count == 0
    assert summary.total_record_count == 0
    assert summary.retention_status == "not_available"
    assert summary.retention_total_candidates == 0
    assert summary.health == "warning"
    assert "Banco local nao encontrado" in summary.message


def test_build_summary_counts_tables_and_records_read_only(tmp_path):
    database_path = tmp_path / "app.db"
    _create_database(database_path)

    summary = build_operational_observability_summary(
        database_path,
        critical_tables=("structures", "pricing_executions", "missing_table"),
        include_retention_simulation=False,
    )

    assert summary.database_exists is True
    assert summary.table_count == 3
    assert summary.total_record_count == 3
    assert summary.critical_tables_present == {
        "structures": True,
        "pricing_executions": True,
        "missing_table": False,
    }
    assert summary.retention_status == "not_requested"
    assert summary.retention_total_candidates == 0
    assert summary.health == "attention"


def test_format_operational_observability_summary(tmp_path):
    database_path = tmp_path / "app.db"
    _create_database(database_path)

    summary = build_operational_observability_summary(
        database_path,
        critical_tables=("structures",),
        include_retention_simulation=False,
    )

    text = format_operational_observability_summary(summary)

    assert "Resumo de observabilidade operacional" in text
    assert "Existe: sim" in text
    assert "Tabelas observadas: 3" in text
    assert "Registros observados: 3" in text
    assert "Retencao: not_requested" in text
    assert "- structures: sim" in text


def _create_database(database_path: Path):
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            "CREATE TABLE structures (id INTEGER PRIMARY KEY, name TEXT)"
        )
        connection.execute(
            "CREATE TABLE pricing_executions (id INTEGER PRIMARY KEY, created_at TEXT)"
        )
        connection.execute(
            "CREATE TABLE payoff_curve_points (id INTEGER PRIMARY KEY, timestamp TEXT)"
        )
        connection.execute("INSERT INTO structures (name) VALUES ('A')")
        connection.execute("INSERT INTO structures (name) VALUES ('B')")
        connection.execute(
            "INSERT INTO pricing_executions (created_at) VALUES ('2026-07-10')"
        )
