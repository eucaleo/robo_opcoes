import sqlite3

from ATT.database_retention_simulation_service import (
    format_database_retention_simulation,
    simulate_database_retention,
)


def _table(report, name):
    return next(table for table in report["tables"] if table["name"] == name)


def test_simulation_counts_old_rows_for_direct_candidate_tables(tmp_path):
    db_path = tmp_path / "app.db"
    connection = sqlite3.connect(db_path)
    connection.execute(
        """
        CREATE TABLE payoff_curve_points (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            created_at TEXT
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE pricing_executions (
            id INTEGER PRIMARY KEY,
            created_at TEXT,
            reference_date TEXT
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE structure_snapshots (
            id INTEGER PRIMARY KEY,
            created_at TEXT,
            reference_date TEXT
        )
        """
    )
    connection.executemany(
        "INSERT INTO payoff_curve_points (timestamp, created_at) VALUES (?, ?)",
        [
            ("2024-01-01 10:00:00", "2024-01-01 10:00:00"),
            ("2026-07-01 10:00:00", "2026-07-01 10:00:00"),
        ],
    )
    connection.executemany(
        "INSERT INTO pricing_executions (created_at, reference_date) VALUES (?, ?)",
        [
            ("2024-02-01 10:00:00", "2024-02-01"),
            ("2026-07-01 10:00:00", "2026-07-01"),
        ],
    )
    connection.executemany(
        "INSERT INTO structure_snapshots (created_at, reference_date) VALUES (?, ?)",
        [
            ("2024-03-01 10:00:00", "2024-03-01"),
            ("2026-07-01 10:00:00", "2026-07-01"),
        ],
    )
    connection.commit()
    connection.close()

    report = simulate_database_retention(
        db_path,
        retention_days=365,
        today="2026-07-10",
    )

    assert _table(report, "payoff_curve_points")["candidate_count"] == 1
    assert _table(report, "pricing_executions")["candidate_count"] == 1
    assert _table(report, "structure_snapshots")["candidate_count"] == 1
    assert report["total_candidates"] == 3


def test_simulation_keeps_out_of_scope_tables_without_candidates(tmp_path):
    db_path = tmp_path / "app.db"
    connection = sqlite3.connect(db_path)
    connection.execute(
        """
        CREATE TABLE rtd_option_quotes (
            id INTEGER PRIMARY KEY,
            updated_at TEXT,
            created_at TEXT
        )
        """
    )
    connection.execute(
        "INSERT INTO rtd_option_quotes (updated_at, created_at) VALUES (?, ?)",
        ("2020-01-01 10:00:00", "2020-01-01 10:00:00"),
    )
    connection.commit()
    connection.close()

    report = simulate_database_retention(
        db_path,
        retention_days=365,
        today="2026-07-10",
    )

    table = _table(report, "rtd_option_quotes")
    assert table["status"] == "out_of_scope"
    assert table["candidate_count"] == 0
    assert table["row_count"] == 1


def test_simulation_does_not_create_missing_database(tmp_path):
    db_path = tmp_path / "missing.db"

    report = simulate_database_retention(
        db_path,
        retention_days=365,
        today="2026-07-10",
    )

    assert report["exists"] is False
    assert report["tables"] == []
    assert report["total_candidates"] == 0
    assert not db_path.exists()


def test_simulation_does_not_remove_rows(tmp_path):
    db_path = tmp_path / "app.db"
    connection = sqlite3.connect(db_path)
    connection.execute(
        """
        CREATE TABLE payoff_curve_points (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            created_at TEXT
        )
        """
    )
    connection.executemany(
        "INSERT INTO payoff_curve_points (timestamp, created_at) VALUES (?, ?)",
        [
            ("2024-01-01 10:00:00", "2024-01-01 10:00:00"),
            ("2026-07-01 10:00:00", "2026-07-01 10:00:00"),
        ],
    )
    connection.commit()
    before = connection.execute(
        "SELECT COUNT(*) FROM payoff_curve_points"
    ).fetchone()[0]
    connection.close()

    report = simulate_database_retention(
        db_path,
        retention_days=365,
        today="2026-07-10",
    )

    connection = sqlite3.connect(db_path)
    after = connection.execute(
        "SELECT COUNT(*) FROM payoff_curve_points"
    ).fetchone()[0]
    connection.close()

    assert _table(report, "payoff_curve_points")["candidate_count"] == 1
    assert before == 2
    assert after == 2


def test_simulation_does_not_use_false_temporal_columns(tmp_path):
    db_path = tmp_path / "app.db"
    connection = sqlite3.connect(db_path)
    connection.execute(
        """
        CREATE TABLE structure_snapshots (
            id INTEGER PRIMARY KEY,
            snapshot_source TEXT,
            alerts_json TEXT
        )
        """
    )
    connection.execute(
        """
        INSERT INTO structure_snapshots (snapshot_source, alerts_json)
        VALUES (?, ?)
        """,
        ("2020-01-01", "2020-01-01"),
    )
    connection.commit()
    connection.close()

    report = simulate_database_retention(
        db_path,
        retention_days=365,
        today="2026-07-10",
    )

    table = _table(report, "structure_snapshots")
    assert table["status"] == "missing_criterion_column"
    assert table["criterion_column"] is None
    assert table["candidate_count"] == 0


def test_structure_leg_snapshots_uses_parent_snapshot_not_expiration_date(tmp_path):
    db_path = tmp_path / "app.db"
    connection = sqlite3.connect(db_path)
    connection.execute(
        """
        CREATE TABLE structure_snapshots (
            id INTEGER PRIMARY KEY,
            created_at TEXT,
            reference_date TEXT
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE structure_leg_snapshots (
            id INTEGER PRIMARY KEY,
            snapshot_id INTEGER,
            expiration_date TEXT
        )
        """
    )
    connection.executemany(
        "INSERT INTO structure_snapshots (id, created_at, reference_date) VALUES (?, ?, ?)",
        [
            (1, "2024-01-01 10:00:00", "2024-01-01"),
            (2, "2026-07-01 10:00:00", "2026-07-01"),
        ],
    )
    connection.executemany(
        "INSERT INTO structure_leg_snapshots (snapshot_id, expiration_date) VALUES (?, ?)",
        [
            (1, "2030-01-01"),
            (2, "2020-01-01"),
        ],
    )
    connection.commit()
    connection.close()

    report = simulate_database_retention(
        db_path,
        retention_days=365,
        today="2026-07-10",
    )

    table = _table(report, "structure_leg_snapshots")
    assert table["status"] == "simulated_dependent"
    assert table["criterion_column"] == "created_at"
    assert table["candidate_count"] == 1


def test_format_database_retention_simulation_returns_readable_summary(tmp_path):
    db_path = tmp_path / "app.db"
    connection = sqlite3.connect(db_path)
    connection.execute(
        """
        CREATE TABLE payoff_curve_points (
            id INTEGER PRIMARY KEY,
            timestamp TEXT
        )
        """
    )
    connection.execute(
        "INSERT INTO payoff_curve_points (timestamp) VALUES (?)",
        ("2024-01-01 10:00:00",),
    )
    connection.commit()
    connection.close()

    report = simulate_database_retention(
        db_path,
        retention_days=365,
        today="2026-07-10",
    )
    text = format_database_retention_simulation(report)

    assert "Simulacao de retencao do banco" in text
    assert "Tabela: payoff_curve_points" in text
    assert "Candidatos: 1" in text
