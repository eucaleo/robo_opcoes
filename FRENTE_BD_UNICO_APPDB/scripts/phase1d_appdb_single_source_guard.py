from __future__ import annotations

import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
APP_DB = ROOT / "dados" / "app.db"
DERIVED_DB = ROOT / "dados" / "app.db"
EVID_DIR = ROOT / "FRENTE_BD_UNICO_APPDB" / "evidencias"
BACKUP_DIR = ROOT / "FRENTE_BD_UNICO_APPDB" / "backups"

OUT = EVID_DIR / "31_phase1d_appdb_single_source_guard.txt"


TEST_CMD = [
    sys.executable,
    "-m",
    "pytest",
    "ATT/tests/test_ui_data_migration.py",
    "ATT/tests/test_structure_editor_integration.py",
    "ATT/tests/test_derived_service.py",
    "-q",
]


def qident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def table_exists(conn: sqlite3.Connection, table: str) -> bool:
    return conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    ).fetchone() is not None


def columns(conn: sqlite3.Connection, table: str) -> list[str]:
    if not table_exists(conn, table):
        return []
    return [r[1] for r in conn.execute(f"PRAGMA table_info({qident(table)})")]


def scalar(conn: sqlite3.Connection, sql: str):
    try:
        row = conn.execute(sql).fetchone()
        return row[0] if row else None
    except Exception as exc:
        return f"ERRO: {type(exc).__name__}: {exc}"


def validate_appdb(fh) -> bool:
    print("===== VALIDACAO APPDB =====", file=fh)
    print(f"APP_DB: {APP_DB}", file=fh)
    print(f"exists: {APP_DB.exists()}", file=fh)

    if not APP_DB.exists():
        print("[ERRO] dados/app.db nao existe.", file=fh)
        return False

    conn = sqlite3.connect(str(APP_DB))

    try:
        ok = True

        required_tables = [
            "structures",
            "structure_legs",
            "structure_decisions",
            "payoff_curve_points",
            "rtd_option_quotes",
        ]

        for table in required_tables:
            exists = table_exists(conn, table)
            print(f"{table}.exists: {exists}", file=fh)
            if not exists:
                ok = False
                continue

            print(
                f"{table}.count:",
                scalar(conn, f"SELECT COUNT(*) FROM {qident(table)}"),
                file=fh,
            )

            cols = columns(conn, table)
            print(f"{table}.columns: {cols}", file=fh)

            if "timestamp" in cols:
                nulls = scalar(
                    conn,
                    f"""
                    SELECT COUNT(*)
                    FROM {qident(table)}
                    WHERE timestamp IS NULL OR TRIM(CAST(timestamp AS TEXT)) = ''
                    """,
                )
                print(f"{table}.timestamp_null_or_empty: {nulls}", file=fh)
                if nulls != 0:
                    ok = False

            if "structure_id" in cols:
                nulls = scalar(
                    conn,
                    f"""
                    SELECT COUNT(*)
                    FROM {qident(table)}
                    WHERE structure_id IS NULL
                    """,
                )
                print(f"{table}.structure_id_null: {nulls}", file=fh)
                if table in {"structure_decisions", "payoff_curve_points"} and nulls != 0:
                    ok = False

            print(file=fh)

        return ok

    finally:
        conn.close()


def main() -> int:
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    quarantine = ROOT / "dados" / f"app.db.quarantine_phase1d_{stamp}"

    with OUT.open("w", encoding="utf-8") as fh:
        print("===== DATA =====", file=fh)
        print(datetime.now().isoformat(sep=" ", timespec="seconds"), file=fh)
        print(file=fh)

        app_ok = validate_appdb(fh)

        print("===== QUARENTENA app.db =====", file=fh)
        print(f"DERIVED_DB: {DERIVED_DB}", file=fh)
        print(f"exists_pre: {DERIVED_DB.exists()}", file=fh)

        moved = False

        if DERIVED_DB.exists():
            shutil.move(str(DERIVED_DB), str(quarantine))
            moved = True
            print(f"[OK] app.db movido temporariamente para: {quarantine}", file=fh)
        else:
            print("[INFO] app.db ja nao existia.", file=fh)

        try:
            print(file=fh)
            print("===== PYTEST SEM app.db =====", file=fh)
            print("cmd:", " ".join(TEST_CMD), file=fh)

            proc = subprocess.run(
                TEST_CMD,
                cwd=str(ROOT),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )

            print(proc.stdout, file=fh)
            print(f"returncode: {proc.returncode}", file=fh)

            if proc.returncode == 0 and app_ok:
                print("[OK] APPDB validado como fonte unica para testes direcionados.", file=fh)
                result = 0
            else:
                print("[ERRO] Guard falhou. Ainda ha dependencia ou inconsistencia.", file=fh)
                result = 1

        finally:
            print(file=fh)
            print("===== RESTAURANDO app.db =====", file=fh)

            if moved and quarantine.exists():
                shutil.move(str(quarantine), str(DERIVED_DB))
                print("[OK] app.db restaurado apos teste.", file=fh)
            else:
                print("[INFO] nada a restaurar.", file=fh)

            print(f"exists_pos: {DERIVED_DB.exists()}", file=fh)

    print(f"[OK] evidencia gerada: {OUT}")
    return result


if __name__ == "__main__":
    raise SystemExit(main())
