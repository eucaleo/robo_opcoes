# scripts/03_aba_timestamp_inventory.py
from __future__ import annotations

import sqlite3
from pathlib import Path

APP_DB = Path("./dados/app.db")

def main() -> int:
    if not APP_DB.exists():
        raise SystemExit("ERRO: ./dados/app.db não encontrado")

    with sqlite3.connect(APP_DB) as conn:
        conn.row_factory = sqlite3.Row

        print("== MANUAL: abas e últimos timestamps ==")
        rows = conn.execute("""
            SELECT aba, MAX(timestamp) AS latest_ts, COUNT(*) AS n
            FROM manual_analise_robo_legs
            GROUP BY aba
            ORDER BY latest_ts DESC
            LIMIT 50
        """).fetchall()
        for r in rows:
            print(f"{r['aba']:<15} latest={r['latest_ts']} rows={r['n']}")

        print("\n== RTD: abas e últimos timestamps ==")
        rows = conn.execute("""
            SELECT aba, MAX(timestamp) AS latest_ts, COUNT(*) AS n
            FROM rtd_analise_robo_legs
            GROUP BY aba
            ORDER BY latest_ts DESC
            LIMIT 50
        """).fetchall()
        for r in rows:
            print(f"{r['aba']:<15} latest={r['latest_ts']} rows={r['n']}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
