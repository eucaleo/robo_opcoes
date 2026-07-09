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

OUT = EVID_DIR / "36_phase1e_remove_legacy_derived_db.txt"


PY_COMPILE_FILES = [
    "ATT/checks/check_end_to_end.py",
    "ATT/checks/check_structures.py",
    "ATT/tests/conftest.py",
    "ATT/tests/test_structure_editor_integration.py",
    "ATT/tests/test_ui_data_migration.py",
    "UI/components/details_panel.py",
    "UI/components/structure_editor_dialog.py",
    "UI/models/ui_data.py",
    "db/config.py",
    "db/derived_repo.py",
    "db/migrations/add_structure_id_to_payoff_curve_points.py",
    "db/reader.py",
    "db/writer.py",
    "domain/payoff_features.py",
    "repositories/rtd_option_quotes_repository.py",
    "scripts/purge_derived_snapshots.py",
    "scripts/repair_derived_db_consistency.py",
    "scripts/validate_derived_db.py",
]

PYTEST_CMD = [
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


def connect_app() -> sqlite3.Connection:
    conn = sqlite3.connect(str(APP_DB))
    conn.row_factory = sqlite3.Row
    return conn


def table_exists(conn: sqlite3.Connection, table: str) -> bool:
    return conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    ).fetchone() is not None


def columns(conn: sqlite3.Connection, table: str) -> list[str]:
    if not table_exists(conn, table):
        return []
    return [r["name"] for r in conn.execute(f"PRAGMA table_info({qident(table)})")]


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

    required_tables = [
        "structures",
        "structure_legs",
        "structure_decisions",
        "payoff_curve_points",
        "rtd_option_quotes",
    ]

    ok = True

    conn = connect_app()
    try:
        for table in required_tables:
            exists = table_exists(conn, table)
            print(f"{table}.exists: {exists}", file=fh)

            if not exists:
                ok = False
                continue

            cols = columns(conn, table)
            print(f"{table}.columns: {cols}", file=fh)
            print(
                f"{table}.count:",
                scalar(conn, f"SELECT COUNT(*) FROM {qident(table)}"),
                file=fh,
            )

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

                if table in {"structure_decisions", "payoff_curve_points", "structure_legs"} and nulls != 0:
                    ok = False

            print(file=fh)

    finally:
        conn.close()

    print(f"appdb_ok: {ok}", file=fh)
    return ok


def run_cmd(cmd: list[str], fh, title: str) -> int:
    print(file=fh)
    print(f"===== {title} =====", file=fh)
    print("cmd:", " ".join(cmd), file=fh)

    proc = subprocess.run(
        cmd,
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    print(proc.stdout, file=fh)
    print(f"returncode: {proc.returncode}", file=fh)
    return proc.returncode


def main() -> int:
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    copied_backup = BACKUP_DIR / f"derived_legacy_backup_pre_phase1e_{stamp}.db"
    removed_target = BACKUP_DIR / f"derived_legacy_removed_phase1e_{stamp}.db"

    moved = False

    with OUT.open("w", encoding="utf-8") as fh:
        print("===== DATA =====", file=fh)
        print(datetime.now().isoformat(sep=" ", timespec="seconds"), file=fh)
        print(file=fh)

        app_ok = validate_appdb(fh)

        print(file=fh)
        print("===== REMOCAO CONTROLADA app.db =====", file=fh)
        print(f"DERIVED_DB: {DERIVED_DB}", file=fh)
        print(f"exists_pre: {DERIVED_DB.exists()}", file=fh)

        if DERIVED_DB.exists():
            shutil.copy2(DERIVED_DB, copied_backup)
            print(f"[OK] backup copiado: {copied_backup}", file=fh)

            shutil.move(str(DERIVED_DB), str(removed_target))
            moved = True
            print(f"[OK] app.db movido para backup: {removed_target}", file=fh)
        else:
            print("[INFO] dados/app.db ja nao existe.", file=fh)

        print(f"exists_after_move: {DERIVED_DB.exists()}", file=fh)

        try:
            compile_cmd = [sys.executable, "-m", "py_compile"] + PY_COMPILE_FILES
            compile_rc = run_cmd(compile_cmd, fh, "PY_COMPILE SEM app.db")

            pytest_rc = run_cmd(PYTEST_CMD, fh, "PYTEST DIRECIONADO SEM app.db")

            print(file=fh)
            print("===== DECISAO =====", file=fh)

            if app_ok and compile_rc == 0 and pytest_rc == 0 and not DERIVED_DB.exists():
                print("[OK] Fase 1E aprovada.", file=fh)
                print("[OK] dados/app.db permanece removido do caminho operacional.", file=fh)
                print(f"[OK] copia legado preservada em: {removed_target}", file=fh)
                return 0

            print("[ERRO] Fase 1E falhou. Restaurando dados/app.db.", file=fh)

            if moved and removed_target.exists():
                shutil.move(str(removed_target), str(DERIVED_DB))
                print("[OK] app.db restaurado.", file=fh)

            return 1

        except Exception as exc:
            print(file=fh)
            print("===== EXCEPTION =====", file=fh)
            print(f"{type(exc).__name__}: {exc}", file=fh)

            if moved and removed_target.exists() and not DERIVED_DB.exists():
                shutil.move(str(removed_target), str(DERIVED_DB))
                print("[OK] app.db restaurado apos exception.", file=fh)

            return 1

        finally:
            print(file=fh)
            print("===== ESTADO FINAL =====", file=fh)
            print(f"derived_db_exists_final: {DERIVED_DB.exists()}", file=fh)
            print(f"backup_copy_exists: {copied_backup.exists()}", file=fh)
            print(f"removed_target_exists: {removed_target.exists()}", file=fh)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
