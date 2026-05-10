import sqlite3
from pathlib import Path

DB_PATH = Path("dados/app.db")


def ensure_structures_schema(db_path: Path = DB_PATH) -> None:
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS structures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                underlying_asset TEXT NOT NULL,
                alias_legacy_aba TEXT,
                status TEXT NOT NULL DEFAULT 'active',
                notes TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS structure_legs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                structure_id INTEGER NOT NULL,
                position_side TEXT NOT NULL,
                option_type TEXT NOT NULL,
                symbol TEXT,
                strike REAL NOT NULL,
                expiration_date TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                premium REAL,
                multiplier REAL NOT NULL DEFAULT 1,
                leg_order INTEGER NOT NULL,
                notes TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (structure_id) REFERENCES structures(id) ON DELETE CASCADE
            )
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_structures_underlying_asset
            ON structures(underlying_asset)
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_structures_alias_legacy_aba
            ON structures(alias_legacy_aba)
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_structure_legs_structure_id
            ON structure_legs(structure_id)
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_structure_legs_structure_id_leg_order
            ON structure_legs(structure_id, leg_order)
            """
        )

        conn.commit()
