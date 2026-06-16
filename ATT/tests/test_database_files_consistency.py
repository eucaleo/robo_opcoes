from __future__ import annotations

import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

APP_DB = PROJECT_ROOT / "dados" / "app.db"
DERIVED_DB = PROJECT_ROOT / "dados" / "derived.db"


def _tables(conn: sqlite3.Connection) -> set[str]:
    return {
        row[0]
        for row in conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        ).fetchall()
    }


def _columns(conn: sqlite3.Connection, table: str) -> set[str]:
    return {row[1] for row in conn.execute(f'PRAGMA table_info("{table}")').fetchall()}


def test_app_db_file_exists_and_has_required_tables():
    assert APP_DB.exists(), f"app.db nao encontrado em {APP_DB}"

    required_tables = {
        "structures",
        "structure_legs",
        "structure_snapshots",
        "structure_leg_snapshots",
        "structure_audit_log",
        "pricing_executions",
    }

    with sqlite3.connect(str(APP_DB)) as conn:
        existing = _tables(conn)

    assert required_tables <= existing


def test_derived_db_file_exists_and_has_required_tables():
    assert DERIVED_DB.exists(), f"derived.db nao encontrado em {DERIVED_DB}"

    required_tables = {
        "payoff_curve_points",
        "structure_decisions",
    }

    with sqlite3.connect(str(DERIVED_DB)) as conn:
        existing = _tables(conn)

    assert required_tables <= existing


def test_app_db_minimal_columns_exist():
    expected = {
        "structures": {"id"},
        "structure_legs": {"id", "structure_id"},
        "structure_snapshots": {"id", "structure_id"},
        "structure_leg_snapshots": {"id"},
        "structure_audit_log": {"id"},
        "pricing_executions": {"id"},
    }

    with sqlite3.connect(str(APP_DB)) as conn:
        for table, required_columns in expected.items():
            existing_columns = _columns(conn, table)
            assert required_columns <= existing_columns, (
                table,
                required_columns - existing_columns,
            )


def test_derived_db_minimal_columns_exist():
    expected = {
        "payoff_curve_points": set(),
        "structure_decisions": set(),
    }

    with sqlite3.connect(str(DERIVED_DB)) as conn:
        for table, required_columns in expected.items():
            existing_columns = _columns(conn, table)
            assert required_columns <= existing_columns, (
                table,
                required_columns - existing_columns,
            )


def test_app_db_has_no_orphan_structure_legs():
    with sqlite3.connect(str(APP_DB)) as conn:
        orphan_count = conn.execute(
            """
            SELECT COUNT(*)
            FROM structure_legs l
            LEFT JOIN structures s ON s.id = l.structure_id
            WHERE l.structure_id IS NOT NULL
              AND s.id IS NULL
            """
        ).fetchone()[0]

    assert orphan_count == 0


def test_app_db_has_no_orphan_structure_snapshots():
    with sqlite3.connect(str(APP_DB)) as conn:
        orphan_count = conn.execute(
            """
            SELECT COUNT(*)
            FROM structure_snapshots ss
            LEFT JOIN structures s ON s.id = ss.structure_id
            WHERE ss.structure_id IS NOT NULL
              AND s.id IS NULL
            """
        ).fetchone()[0]

    assert orphan_count == 0
