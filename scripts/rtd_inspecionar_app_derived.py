from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]

for db_name in ["dados/app.db", "dados/derived.db"]:
    db_path = ROOT / db_name
    print("=" * 80)
    print(db_name)
    print("=" * 80)

    if not db_path.exists():
        print("NAO ENCONTRADO")
        continue

    con = sqlite3.connect(str(db_path))
    cur = con.cursor()

    tables = [
        r[0]
        for r in cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
    ]

    for table in tables:
        print(f"- {table}")

    print()
    for table in tables:
        if any(k in table.lower() for k in ["rtd", "underlying", "quote", "market", "vwap"]):
            print(f"SCHEMA {table}")
            for row in cur.execute(f"PRAGMA table_info({table})").fetchall():
                print(" ", row)
            try:
                count = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                print(" linhas:", count)
            except Exception as exc:
                print(" erro count:", exc)
            print()

    con.close()
