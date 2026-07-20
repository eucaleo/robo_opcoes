#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sqlite3
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECALC_SCRIPT = ROOT / "scripts" / "recalculate_payoff_curve_points_once.py"
DIAG_SCRIPT = ROOT / "scripts" / "diagnose_payoff_curve_points.py"


def table_columns(conn, table_name):
    try:
        rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
        return {row[1] for row in rows}
    except sqlite3.Error:
        return set()


def table_exists(conn, table_name):
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type IN ('table', 'view') AND name = ?",
        (table_name,),
    ).fetchone()
    return row is not None


def discover_structure_ids(db_path):
    candidates = [
        ("payoff_curve_points", "structure_id"),
        ("structure_legs", "structure_id"),
        ("option_legs", "structure_id"),
        ("canonical_legs", "structure_id"),
        ("structures", "id"),
        ("payoff_structures", "id"),
        ("option_structures", "id"),
    ]

    ids = set()

    with sqlite3.connect(db_path) as conn:
        for table_name, id_column in candidates:
            if not table_exists(conn, table_name):
                continue

            columns = table_columns(conn, table_name)
            if id_column not in columns:
                continue

            query = f"""
                SELECT DISTINCT {id_column}
                FROM {table_name}
                WHERE {id_column} IS NOT NULL
                ORDER BY {id_column}
            """

            try:
                for row in conn.execute(query):
                    ids.add(int(row[0]))
            except Exception:
                continue

    return sorted(ids)


def run_command(cmd, fail_on_error=True):
    print("")
    print("[payoff-batch] executando:")
    print(" ".join(str(part) for part in cmd))

    result = subprocess.run(cmd, cwd=ROOT)

    if result.returncode != 0 and fail_on_error:
        raise SystemExit(result.returncode)

    return result.returncode


def parse_args():
    parser = argparse.ArgumentParser(
        description="Recalcula payoff_curve_points em lote usando o script RTD existente."
    )

    parser.add_argument(
        "--db",
        default="dados/app.db",
        help="Caminho do banco SQLite. Padrão: dados/app.db",
    )

    parser.add_argument(
        "--structure-ids",
        nargs="*",
        type=int,
        default=None,
        help="IDs das estruturas. Exemplo: --structure-ids 2 3",
    )

    parser.add_argument(
        "--diagnose",
        action="store_true",
        help="Executa diagnose_payoff_curve_points.py após cada recálculo.",
    )

    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continua processando mesmo se uma estrutura falhar.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    db_path = Path(args.db)
    if not db_path.is_absolute():
        db_path = ROOT / db_path

    if not db_path.exists():
        raise SystemExit(f"[payoff-batch] ERRO: banco não encontrado: {db_path}")

    if not RECALC_SCRIPT.exists():
        raise SystemExit(f"[payoff-batch] ERRO: script não encontrado: {RECALC_SCRIPT}")

    structure_ids = args.structure_ids
    if not structure_ids:
        structure_ids = discover_structure_ids(db_path)

    if not structure_ids:
        raise SystemExit("[payoff-batch] ERRO: nenhuma estrutura encontrada.")

    print(f"[payoff-batch] db={db_path}")
    print(f"[payoff-batch] estruturas={structure_ids}")

    ok = 0
    fail = 0

    for structure_id in structure_ids:
        print("")
        print(f"[payoff-batch] recalculando structure_id={structure_id}...")

        rc = run_command(
            [
                sys.executable,
                str(RECALC_SCRIPT),
                "--db",
                str(db_path),
                "--structure-id",
                str(structure_id),
            ],
            fail_on_error=not args.continue_on_error,
        )

        if rc == 0:
            ok += 1
        else:
            fail += 1
            if not args.continue_on_error:
                break

        if args.diagnose and DIAG_SCRIPT.exists():
            run_command(
                [
                    sys.executable,
                    str(DIAG_SCRIPT),
                    "--db",
                    str(db_path),
                    "--structure-id",
                    str(structure_id),
                ],
                fail_on_error=not args.continue_on_error,
            )

    print("")
    print(f"[payoff-batch] concluído. ok={ok} fail={fail}")

    if fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
