# db/migrations/add_structure_id_to_payoff_curve_points.py
"""
Migration: adiciona structure_id em payoff_curve_points
e payoff_curve_summary, com backfill via structure_decisions.

Uso:
    python db/migrations/add_structure_id_to_payoff_curve_points.py
    python db/migrations/add_structure_id_to_payoff_curve_points.py --db dados/derived.db
"""

import sqlite3
import argparse
import pathlib
import sys


SQL_STEPS = [
    #  payoff_curve_points 
    (
        "payoff_curve_points: verificar se structure_id já existe",
        None,  # tratado especialmente abaixo
    ),
    (
        "payoff_curve_points: ADD COLUMN structure_id",
        "ALTER TABLE payoff_curve_points ADD COLUMN structure_id INTEGER",
    ),
    (
        "payoff_curve_points: BACKFILL structure_id",
        """
        UPDATE payoff_curve_points
        SET structure_id = (
            SELECT d.structure_id
            FROM structure_decisions d
            WHERE d.aba       = payoff_curve_points.aba
              AND d.timestamp = payoff_curve_points.timestamp
            LIMIT 1
        )
        """,
    ),
    (
        "payoff_curve_points: CREATE INDEX sid+ts",
        """
        CREATE INDEX IF NOT EXISTS idx_payoff_points_sid_ts
            ON payoff_curve_points (structure_id, timestamp)
        """,
    ),
    #  payoff_curve_summary 
    (
        "payoff_curve_summary: ADD COLUMN structure_id",
        "ALTER TABLE payoff_curve_summary ADD COLUMN structure_id INTEGER",
    ),
    (
        "payoff_curve_summary: BACKFILL structure_id",
        """
        UPDATE payoff_curve_summary
        SET structure_id = (
            SELECT d.structure_id
            FROM structure_decisions d
            WHERE d.aba       = payoff_curve_summary.aba
              AND d.timestamp = payoff_curve_summary.timestamp
            LIMIT 1
        )
        """,
    ),
    (
        "payoff_curve_summary: CREATE INDEX sid+ts",
        """
        CREATE INDEX IF NOT EXISTS idx_payoff_summary_sid_ts
            ON payoff_curve_summary (structure_id, timestamp)
        """,
    ),
]


def col_exists(conn: sqlite3.Connection, table: str, col: str) -> bool:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(r[1] == col for r in rows)


def run(db_path: pathlib.Path):
    if not db_path.exists():
        print(f"[ERRO] DB não encontrado: {db_path}")
        sys.exit(1)

    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")

    try:
        with conn:
            for label, sql in SQL_STEPS:
                # Idempotência: pula ALTER TABLE se coluna já existe
                if "ADD COLUMN structure_id" in (sql or ""):
                    table = label.split(":")[0].strip()
                    if col_exists(conn, table, "structure_id"):
                        print(f"  [SKIP] {label} -- coluna já existe")
                        continue

                if sql is None:
                    continue  # step de verificação sem SQL

                print(f"  [RUN]  {label}")
                conn.execute(sql)

        # Verificação pós-migration
        print("\n Verificação ")
        for table in ("payoff_curve_points", "payoff_curve_summary"):
            rows = conn.execute(
                f"SELECT COUNT(*) AS total, "
                f"COUNT(structure_id) AS filled "
                f"FROM {table}"
            ).fetchone()
            pct = (rows[1] / rows[0] * 100) if rows[0] else 0
            print(f"  {table}: {rows[1]}/{rows[0]} linhas preenchidas ({pct:.1f}%)")

        print("\n[OK] Migration de structure_id aplicada com sucesso.")

    except Exception as e:
        print(f"[ERRO] {e}")
        conn.rollback()
        sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="dados/app.db")
    args = parser.parse_args()
    run(pathlib.Path(args.db))
