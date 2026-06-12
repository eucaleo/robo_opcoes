import sqlite3
from pathlib import Path

from infra.bootstrap_structures_schema import ensure_structures_schema


def _columns(conn: sqlite3.Connection, table_name: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {row[1] for row in rows}


def _indexes(conn: sqlite3.Connection, table_name: str) -> set[str]:
    rows = conn.execute(f"PRAGMA index_list({table_name})").fetchall()
    return {row[1] for row in rows}


def _foreign_keys(conn: sqlite3.Connection, table_name: str) -> set[tuple[str, str, str, str]]:
    rows = conn.execute(f"PRAGMA foreign_key_list({table_name})").fetchall()
    return {
        (
            row[2],  # referenced table
            row[3],  # from column
            row[4],  # to column
            row[6],  # on delete
        )
        for row in rows
    }


def test_ensure_structures_schema_creates_system_snapshot_tables(tmp_path: Path):
    db_path = tmp_path / "app.db"

    ensure_structures_schema(db_path)

    with sqlite3.connect(db_path) as conn:
        tables = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }

    assert "structure_snapshots" in tables
    assert "structure_leg_snapshots" in tables


def test_structure_snapshots_schema_columns_indexes_and_foreign_keys(tmp_path: Path):
    db_path = tmp_path / "app.db"

    ensure_structures_schema(db_path)

    with sqlite3.connect(db_path) as conn:
        cols = _columns(conn, "structure_snapshots")
        indexes = _indexes(conn, "structure_snapshots")
        foreign_keys = _foreign_keys(conn, "structure_snapshots")

    assert {
        "id",
        "created_at",
        "structure_id",
        "pricing_execution_id",
        "underlying_asset",
        "reference_date",
        "snapshot_source",
        "structure_json",
        "market_json",
        "metrics_json",
        "payoff_json",
        "decision_json",
        "alerts_json",
        "operation_state_json",
    }.issubset(cols)

    assert {
        "idx_structure_snapshots_structure_id",
        "idx_structure_snapshots_created_at",
        "idx_structure_snapshots_structure_created",
        "idx_structure_snapshots_reference_date",
        "idx_structure_snapshots_pricing_execution_id",
    }.issubset(indexes)

    assert ("structures", "structure_id", "id", "NO ACTION") in foreign_keys
    assert ("pricing_executions", "pricing_execution_id", "id", "NO ACTION") in foreign_keys


def test_structure_leg_snapshots_schema_columns_indexes_and_foreign_keys(tmp_path: Path):
    db_path = tmp_path / "app.db"

    ensure_structures_schema(db_path)

    with sqlite3.connect(db_path) as conn:
        cols = _columns(conn, "structure_leg_snapshots")
        indexes = _indexes(conn, "structure_leg_snapshots")
        foreign_keys = _foreign_keys(conn, "structure_leg_snapshots")

    assert {
        "id",
        "snapshot_id",
        "structure_id",
        "leg_id",
        "leg_order",
        "position_side",
        "option_type",
        "symbol",
        "strike",
        "expiration_date",
        "quantity",
        "premium",
        "multiplier",
        "metrics_json",
        "market_json",
        "raw_json",
    }.issubset(cols)

    assert {
        "idx_structure_leg_snapshots_snapshot_id",
        "idx_structure_leg_snapshots_structure_id",
        "idx_structure_leg_snapshots_leg_id",
    }.issubset(indexes)

    assert ("structure_snapshots", "snapshot_id", "id", "CASCADE") in foreign_keys
    assert ("structures", "structure_id", "id", "NO ACTION") in foreign_keys
    assert ("structure_legs", "leg_id", "id", "NO ACTION") in foreign_keys
