#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path


TABLES = [
    "payoff_curve_points",
    "structure_decisions",
    "payoff_curve_summary",
]


def table_exists(con: sqlite3.Connection, table: str) -> bool:
    row = con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    ).fetchone()
    return row is not None


def count_table(con: sqlite3.Connection, table: str) -> int | None:
    if not table_exists(con, table):
        return None
    return int(con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Remove snapshots derivados antigos/inválidos do derived.db"
    )
    parser.add_argument(
        "--db",
        default="dados/app.db",
        help="Caminho do derived.db. Default: dados/app.db",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Remove todos os snapshots derivados.",
    )
    parser.add_argument(
        "--older-than-hours",
        type=float,
        default=None,
        help="Remove snapshots com timestamp mais antigo que N horas.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Aplica alterações. Sem isso roda em dry-run.",
    )
    args = parser.parse_args()

    if not args.all and args.older_than_hours is None:
        parser.error("use --all ou --older-than-hours N")

    db = Path(args.db)

    print("=== PURGE DERIVED SNAPSHOTS ===")
    print(f"[INFO] DB: {db.resolve()}")
    print(f"[INFO] Existe: {db.exists()}")

    if not db.exists():
        print("[ERROR] Banco não encontrado.")
        return 2

    if args.apply:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = db.with_suffix(db.suffix + f".bak-purge-{stamp}")
        shutil.copy2(db, backup)
        print(f"[INFO] Backup criado: {backup}")
    else:
        print("[DRY-RUN] Nenhuma alteração será aplicada.")

    cutoff = None
    if args.older_than_hours is not None:
        cutoff_dt = datetime.now(timezone.utc) - timedelta(hours=args.older_than_hours)
        cutoff = cutoff_dt.isoformat()
        print(f"[INFO] Cutoff UTC: {cutoff}")

    con = sqlite3.connect(str(db))
    try:
        print()
        print("=== CONTAGEM ANTES ===")
        before = {}
        for table in TABLES:
            n = count_table(con, table)
            before[table] = n
            if n is None:
                print(f"[SKIP] {table}: tabela inexistente")
            else:
                print(f"[INFO] {table}: {n}")

        deleted = {}

        if args.apply:
            with con:
                for table in TABLES:
                    if not table_exists(con, table):
                        continue

                    if args.all:
                        cur = con.execute(f"DELETE FROM {table}")
                    else:
                        cols = [
                            r[1]
                            for r in con.execute(f"PRAGMA table_info({table})").fetchall()
                        ]
                        if "timestamp" not in cols:
                            print(f"[SKIP] {table}: sem coluna timestamp")
                            continue
                        cur = con.execute(
                            f"DELETE FROM {table} WHERE timestamp < ?",
                            (cutoff,),
                        )

                    deleted[table] = cur.rowcount
        else:
            for table in TABLES:
                if not table_exists(con, table):
                    continue

                if args.all:
                    n = count_table(con, table) or 0
                else:
                    cols = [
                        r[1]
                        for r in con.execute(f"PRAGMA table_info({table})").fetchall()
                    ]
                    if "timestamp" not in cols:
                        continue
                    n = int(
                        con.execute(
                            f"SELECT COUNT(*) FROM {table} WHERE timestamp < ?",
                            (cutoff,),
                        ).fetchone()[0]
                    )

                deleted[table] = n

        print()
        print("=== REMOÇÕES ===")
        for table in TABLES:
            if table in deleted:
                prefix = "[APPLY]" if args.apply else "[DRY-RUN]"
                print(f"{prefix} {table}: {deleted[table]}")

        print()
        print("=== CONTAGEM DEPOIS ===")
        for table in TABLES:
            n = count_table(con, table)
            if n is None:
                print(f"[SKIP] {table}: tabela inexistente")
            else:
                print(f"[INFO] {table}: {n}")

        print()
        if args.apply:
            print("[OK] Purge aplicado.")
        else:
            print("[OK] Dry-run concluído.")

        return 0

    finally:
        con.close()


if __name__ == "__main__":
    raise SystemExit(main())
