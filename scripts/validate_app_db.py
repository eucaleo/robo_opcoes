from __future__ import annotations

import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_DB_PATH = PROJECT_ROOT / "dados" / "app.db"


REQUIRED_TABLES = {
    "structures",
    "structure_legs",
    "structure_snapshots",
    "structure_leg_snapshots",
    "structure_audit_log",
    "pricing_executions",
}


def table_exists(conn: sqlite3.Connection, table: str) -> bool:
    row = conn.execute(
        """
        SELECT 1
        FROM sqlite_master
        WHERE type = 'table'
          AND name = ?
        LIMIT 1
        """,
        (table,),
    ).fetchone()
    return row is not None


def table_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    rows = conn.execute(f'PRAGMA table_info("{table}")').fetchall()
    return {row[1] for row in rows}


def count_rows(conn: sqlite3.Connection, table: str) -> int:
    return conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]


def validate_required_tables(conn: sqlite3.Connection) -> list[str]:
    errors: list[str] = []

    for table in sorted(REQUIRED_TABLES):
        if not table_exists(conn, table):
            errors.append(f"Tabela obrigatoria ausente: {table}")

    return errors


def validate_minimal_columns(conn: sqlite3.Connection) -> list[str]:
    errors: list[str] = []

    expected_columns: dict[str, set[str]] = {
        "structures": {
            "id",
        },
        "structure_legs": {
            "id",
            "structure_id",
        },
        "structure_snapshots": {
            "id",
            "structure_id",
        },
        "structure_leg_snapshots": {
            "id",
        },
        "structure_audit_log": {
            "id",
        },
        "pricing_executions": {
            "id",
        },
    }

    for table, required_columns in expected_columns.items():
        if not table_exists(conn, table):
            continue

        existing = table_columns(conn, table)
        missing = sorted(required_columns - existing)

        if missing:
            errors.append(
                f"Tabela {table} sem coluna(s) obrigatoria(s): {', '.join(missing)}"
            )

    return errors


def validate_basic_foreign_consistency(conn: sqlite3.Connection) -> list[str]:
    errors: list[str] = []

    if table_exists(conn, "structure_legs") and table_exists(conn, "structures"):
        orphan_legs = conn.execute(
            """
            SELECT COUNT(*)
            FROM structure_legs l
            LEFT JOIN structures s ON s.id = l.structure_id
            WHERE l.structure_id IS NOT NULL
              AND s.id IS NULL
            """
        ).fetchone()[0]

        if orphan_legs:
            errors.append(
                f"Existem {orphan_legs} legs em structure_legs sem structure correspondente"
            )

    if table_exists(conn, "structure_snapshots") and table_exists(conn, "structures"):
        orphan_snapshots = conn.execute(
            """
            SELECT COUNT(*)
            FROM structure_snapshots ss
            LEFT JOIN structures s ON s.id = ss.structure_id
            WHERE ss.structure_id IS NOT NULL
              AND s.id IS NULL
            """
        ).fetchone()[0]

        if orphan_snapshots:
            errors.append(
                f"Existem {orphan_snapshots} snapshots sem structure correspondente"
            )

    return errors


def main() -> int:
    print("=== VALIDACAO DO BANCO APP.DB ===")
    print(f"[INFO] Usando app.db em: {APP_DB_PATH}")

    if not APP_DB_PATH.exists():
        print("[ERROR] app.db nao encontrado.")
        return 1

    errors: list[str] = []

    with sqlite3.connect(str(APP_DB_PATH)) as conn:
        errors.extend(validate_required_tables(conn))
        errors.extend(validate_minimal_columns(conn))
        errors.extend(validate_basic_foreign_consistency(conn))

        print("[INFO] Contagem de registros:")

        existing_tables = sorted(
            row[0]
            for row in conn.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                ORDER BY name
                """
            ).fetchall()
            if not row[0].startswith("sqlite_")
        )

        for table in existing_tables:
            print(f"  - {table}: {count_rows(conn, table)}")

    if errors:
        print("[ERROR] app.db possui inconsistencias:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("[OK] APP.DB ESTA CONSISTENTE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
