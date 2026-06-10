from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path


DB_PATH = Path("dados/app.db")


def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    row = conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name = ?
        """,
        (table_name,),
    ).fetchone()
    return row is not None


def get_columns(conn: sqlite3.Connection, table_name: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {row[1] for row in rows}


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Banco não encontrado: {DB_PATH}")

    with sqlite3.connect(str(DB_PATH)) as conn:
        conn.row_factory = sqlite3.Row

        if not table_exists(conn, "rtd_analise_robo_legs"):
            raise RuntimeError("Tabela rtd_analise_robo_legs não encontrada.")

        if not table_exists(conn, "structures"):
            raise RuntimeError("Tabela structures não encontrada.")

        structure_columns = get_columns(conn, "structures")

        abas = conn.execute(
            """
            SELECT
                TRIM(aba) AS aba,
                COUNT(*) AS legs_count
            FROM rtd_analise_robo_legs
            WHERE aba IS NOT NULL
              AND TRIM(aba) <> ''
            GROUP BY TRIM(aba)
            ORDER BY TRIM(aba)
            """
        ).fetchall()

        inserted = 0
        skipped = 0
        now = datetime.now(timezone.utc).isoformat()

        for row in abas:
            aba = row["aba"]

            existing = conn.execute(
                """
                SELECT id
                FROM structures
                WHERE underlying_asset = ?
                   OR alias_legacy_aba = ?
                LIMIT 1
                """,
                (aba, aba),
            ).fetchone()

            if existing:
                print(f"SKIP  {aba}: já existe structure_id={existing['id']}")
                skipped += 1
                continue

            values_by_column = {
                "underlying_asset": aba,
                "alias_legacy_aba": aba,
                "name": aba,
                "structure_name": aba,
                "description": f"Seed automático a partir da aba RTD {aba}",
                "source": "RTD",
                "status": "active",
                "is_active": 1,
                "active": 1,
                "created_at": now,
                "updated_at": now,
            }

            insert_values = {
                column: value
                for column, value in values_by_column.items()
                if column in structure_columns
            }

            if "underlying_asset" not in insert_values:
                raise RuntimeError("Coluna obrigatória structures.underlying_asset não encontrada.")

            columns_sql = ", ".join(insert_values.keys())
            placeholders_sql = ", ".join("?" for _ in insert_values)

            conn.execute(
                f"""
                INSERT INTO structures ({columns_sql})
                VALUES ({placeholders_sql})
                """,
                tuple(insert_values.values()),
            )

            print(f"INSERT {aba}: {row['legs_count']} legs RTD")
            inserted += 1

        conn.commit()

    print()
    print("Seed finalizado.")
    print(f"Inseridos: {inserted}")
    print(f"Ignorados: {skipped}")


if __name__ == "__main__":
    main()
