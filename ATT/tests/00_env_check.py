from __future__ import annotations

import os
import sqlite3
from pathlib import Path

APP_DB = Path("./dados/app.db")

REQUIRED_APP_TABLES = {
    "rtd_analise_robo_legs",
    "manual_analise_robo_legs",
    "rtd_analise_robo",
}


def list_tables(conn: sqlite3.Connection) -> set[str]:
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    return {row[0] for row in rows}


def main() -> int:
    print("== ENV CHECK ==")
    print("CWD:", os.getcwd())

    print("\n== FILES ==")
    print("app.db exists:", APP_DB.exists(), "path:", APP_DB)

    if not APP_DB.exists():
        raise SystemExit("ERRO: ./dados/app.db não encontrado")

    with sqlite3.connect(APP_DB) as conn:
        tables = list_tables(conn)

        print("\n== APP.DB TABLES ==")
        for table_name in sorted(tables):
            print("-", table_name)

        missing = REQUIRED_APP_TABLES - tables
        if missing:
            raise SystemExit(
                f"ERRO: faltam tabelas esperadas no app.db: {sorted(missing)}"
            )

    print("\nOK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
