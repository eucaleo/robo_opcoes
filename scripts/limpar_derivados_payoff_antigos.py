from pathlib import Path
import sqlite3

TARGETS = {
    Path("dados/app.db"): [
        "structure_snapshots",
        "pricing_executions",
    ],
    Path("dados/derived.db"): [
        "payoff_curve_points",
        "structure_decisions",
        "payoff_summary",
        "payoff_features",
    ],
}

def table_exists(cur, table):
    cur.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    )
    return cur.fetchone() is not None

def count_rows(cur, table):
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    return cur.fetchone()[0]

def main():
    for db_path, tables in TARGETS.items():
        print("")
        print("=" * 60)
        print(f"Banco: {db_path}")
        print("=" * 60)

        if not db_path.exists():
            print("AUSENTE")
            continue

        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()

        for table in tables:
            if not table_exists(cur, table):
                print(f"- {table}: AUSENTE")
                continue

            before = count_rows(cur, table)
            cur.execute(f"DELETE FROM {table}")
            after = count_rows(cur, table)

            print(f"- {table}: {before} -> {after}")

        conn.commit()
        conn.close()

    print("")
    print("Limpeza concluida.")

if __name__ == "__main__":
    main()
