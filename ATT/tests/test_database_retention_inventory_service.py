import sqlite3

from ATT.database_retention_inventory_service import (
    build_database_retention_inventory,
    format_database_retention_inventory,
)


def test_build_database_retention_inventory_lists_tables_columns_and_counts(tmp_path):
    db_path = tmp_path / "app.db"

    connection = sqlite3.connect(db_path)
    connection.execute(
        """
        CREATE TABLE rtd_option_quotes_snapshot (
            id INTEGER PRIMARY KEY,
            symbol TEXT NOT NULL,
            captured_at TEXT NOT NULL,
            price REAL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE operational_notes (
            id INTEGER PRIMARY KEY,
            description TEXT
        )
        """
    )
    connection.executemany(
        """
        INSERT INTO rtd_option_quotes_snapshot (symbol, captured_at, price)
        VALUES (?, ?, ?)
        """,
        [
            ("PETR4", "2026-07-10 10:00:00", 30.5),
            ("VALE3", "2026-07-10 10:01:00", 61.2),
        ],
    )
    connection.execute(
        "INSERT INTO operational_notes (description) VALUES (?)",
        ("nota",),
    )
    connection.commit()
    connection.close()

    inventory = build_database_retention_inventory(db_path)

    assert inventory["exists"] is True
    assert inventory["table_count"] == 2

    tables = {table["name"]: table for table in inventory["tables"]}

    snapshot = tables["rtd_option_quotes_snapshot"]
    assert snapshot["row_count"] == 2
    assert snapshot["column_count"] == 4
    assert "captured_at" in snapshot["temporal_columns"]

    notes = tables["operational_notes"]
    assert notes["row_count"] == 1
    assert notes["temporal_columns"] == []


def test_build_database_retention_inventory_does_not_create_missing_database(tmp_path):
    db_path = tmp_path / "missing.db"

    inventory = build_database_retention_inventory(db_path)

    assert inventory["exists"] is False
    assert inventory["table_count"] == 0
    assert inventory["tables"] == []
    assert not db_path.exists()


def test_format_database_retention_inventory_returns_readable_summary(tmp_path):
    db_path = tmp_path / "app.db"

    connection = sqlite3.connect(db_path)
    connection.execute(
        """
        CREATE TABLE intraday_history (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            trade_time TEXT
        )
        """
    )
    connection.commit()
    connection.close()

    inventory = build_database_retention_inventory(db_path)
    text = format_database_retention_inventory(inventory)

    assert "Inventario tecnico do banco" in text
    assert "Tabela: intraday_history" in text
    assert "Colunas temporais candidatas: trade_time" in text
