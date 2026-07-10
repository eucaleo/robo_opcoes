# scripts/01_schema_dump.py
from __future__ import annotations

import sqlite3
from pathlib import Path

APP_DB = Path("./dados/app.db")

TABLES = [
    "rtd_analise_robo_legs",
    "manual_analise_robo_legs",
    "rtd_analise_robo",
]

def dump_table_schema(conn: sqlite3.Connection, table: str) -> None:
    print(f"\n== SCHEMA: {table} ==")
    cols = conn.execute(f"PRAGMA table_info({table})").fetchall()
    if not cols:
        print("(tabela não encontrada ou sem colunas)")
        return
    for cid, name, ctype, notnull, dflt_value, pk in cols:
        print(f"- {name} {ctype} notnull={notnull} pk={pk} default={dflt_value}")

def main() -> int:
    if not APP_DB.exists():
        raise SystemExit("ERRO: ./dados/app.db não encontrado")

    with sqlite3.connect(APP_DB) as conn:
        for t in TABLES:
            dump_table_schema(conn, t)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
