from __future__ import annotations

import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
APP_DB = ROOT / "dados" / "app.db"
DERIVED_DB = ROOT / "dados" / "app.db"
EVID_DIR = ROOT / "FRENTE_BD_UNICO_APPDB" / "evidencias"
BACKUP_DIR = ROOT / "FRENTE_BD_UNICO_APPDB" / "backups"

PRE_EVID = EVID_DIR / "18_phase1b_schema_pre.txt"
OUT_EVID = EVID_DIR / "19_phase1b_bootstrap_output.txt"
POST_EVID = EVID_DIR / "20_phase1b_schema_pos.txt"


KEY_TABLES = [
    "structure_decisions",
    "payoff_curve_points",
    "payoff_curve_summary",
    "option_quotes",
    "rtd_option_quotes",
]


def qident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    return conn


def table_exists(conn: sqlite3.Connection, table: str) -> bool:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    ).fetchone()
    return row is not None


def table_sql(conn: sqlite3.Connection, table: str) -> str | None:
    row = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    ).fetchone()
    return row["sql"] if row else None


def columns(conn: sqlite3.Connection, table: str) -> list[str]:
    if not table_exists(conn, table):
        return []
    return [r["name"] for r in conn.execute(f"PRAGMA table_info({qident(table)})")]


def count_rows(conn: sqlite3.Connection, table: str) -> int | None:
    if not table_exists(conn, table):
        return None
    return int(conn.execute(f"SELECT COUNT(*) AS n FROM {qident(table)}").fetchone()["n"])


def safe_scalar(conn: sqlite3.Connection, sql: str) -> object:
    try:
        row = conn.execute(sql).fetchone()
        if row is None:
            return None
        return list(row)[0]
    except Exception as exc:
        return f"ERRO: {exc}"


def dump_db(path: Path, label: str, fh) -> None:
    print(f"===== {label} =====", file=fh)
    print(f"path: {path}", file=fh)
    print(f"exists: {path.exists()}", file=fh)

    if not path.exists():
        print(file=fh)
        return

    conn = connect(path)
    try:
        tables = [
            r["name"]
            for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
        ]

        print(f"tables_count: {len(tables)}", file=fh)
        print("tables:", file=fh)
        for t in tables:
            print(f"  - {t}", file=fh)

        print(file=fh)
        print("===== KEY TABLES =====", file=fh)

        for table in KEY_TABLES:
            print(file=fh)
            print(f"--- {table} ---", file=fh)
            print(f"exists: {table_exists(conn, table)}", file=fh)

            if not table_exists(conn, table):
                continue

            cols = columns(conn, table)
            print(f"columns: {cols}", file=fh)
            print(f"count: {count_rows(conn, table)}", file=fh)

            if "timestamp" in cols:
                print(
                    "timestamp_null_or_empty:",
                    safe_scalar(
                        conn,
                        f"""
                        SELECT COUNT(*)
                        FROM {qident(table)}
                        WHERE timestamp IS NULL OR TRIM(CAST(timestamp AS TEXT)) = ''
                        """,
                    ),
                    file=fh,
                )

            if "structure_id" in cols:
                print(
                    "structure_id_null:",
                    safe_scalar(
                        conn,
                        f"""
                        SELECT COUNT(*)
                        FROM {qident(table)}
                        WHERE structure_id IS NULL
                        """,
                    ),
                    file=fh,
                )

            print("ddl:", file=fh)
            print(table_sql(conn, table), file=fh)
    finally:
        conn.close()

    print(file=fh)


def backup_app_db(fh) -> None:
    if not APP_DB.exists():
        print("[INFO] app.db ainda nao existe; nenhum backup criado.", file=fh)
        return

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = BACKUP_DIR / f"app_pre_phase1b_{stamp}.db"
    shutil.copy2(APP_DB, backup)
    print(f"[OK] backup criado: {backup}", file=fh)


def bootstrap_via_derived_repo(fh) -> None:
    print("===== BOOTSTRAP VIA db.derived_repo.DerivedRepo =====", file=fh)

    try:
        from db.derived_repo import DerivedRepo

        DerivedRepo(db_path=str(APP_DB))
        print("[OK] DerivedRepo bootstrap executado em dados/app.db", file=fh)
    except Exception as exc:
        print(f"[WARN] DerivedRepo bootstrap falhou: {type(exc).__name__}: {exc}", file=fh)


def run_structure_id_migration(fh) -> None:
    print(file=fh)
    print("===== MIGRATION structure_id EM payoff_curve_points =====", file=fh)

    try:
        from db.migrations.add_structure_id_to_payoff_curve_points import run

        run(APP_DB)
        print("[OK] migration add_structure_id_to_payoff_curve_points executada em dados/app.db", file=fh)
    except Exception as exc:
        print(f"[WARN] migration falhou: {type(exc).__name__}: {exc}", file=fh)


def create_table_from_source_if_needed(
    dst: sqlite3.Connection,
    src: sqlite3.Connection,
    table: str,
    fh,
) -> None:
    if table_exists(dst, table):
        return

    sql = table_sql(src, table)
    if not sql:
        print(f"[SKIP] sem DDL de origem para {table}", file=fh)
        return

    dst.execute(sql)
    print(f"[OK] tabela criada no app.db a partir do app.db: {table}", file=fh)


def copy_table_intersection(
    dst: sqlite3.Connection,
    src: sqlite3.Connection,
    table: str,
    fh,
) -> None:
    if not table_exists(src, table):
        print(f"[SKIP] origem nao possui tabela: {table}", file=fh)
        return

    create_table_from_source_if_needed(dst, src, table, fh)

    if not table_exists(dst, table):
        print(f"[SKIP] destino nao possui tabela apos tentativa de criacao: {table}", file=fh)
        return

    src_cols = columns(src, table)
    dst_cols = columns(dst, table)
    common = [c for c in src_cols if c in dst_cols]

    if not common:
        print(f"[SKIP] sem colunas comuns para copiar: {table}", file=fh)
        return

    col_sql = ", ".join(qident(c) for c in common)

    before = count_rows(dst, table)

    dst.execute("PRAGMA foreign_keys = OFF")

    dst.execute(
        f"""
        INSERT OR IGNORE INTO {qident(table)} ({col_sql})
        SELECT {col_sql}
        FROM src.{qident(table)}
        """
    )

    after = count_rows(dst, table)
    print(
        f"[OK] copia {table}: antes={before}, depois={after}, colunas={common}",
        file=fh,
    )


def import_from_derived_db(fh) -> None:
    print(file=fh)
    print("===== IMPORTANDO TABELAS DO app.db PARA app.db =====", file=fh)

    if not DERIVED_DB.exists():
        print("[WARN] dados/app.db nao existe; importacao ignorada.", file=fh)
        return

    dst = connect(APP_DB)
    src = connect(DERIVED_DB)

    try:
        dst.execute(f"ATTACH DATABASE ? AS src", (str(DERIVED_DB),))

        src_tables = [
            r["name"]
            for r in src.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
        ]

        candidate_tables = [t for t in KEY_TABLES if t in src_tables]

        print(f"[INFO] tabelas candidatas origem: {candidate_tables}", file=fh)

        for table in candidate_tables:
            copy_table_intersection(dst, src, table, fh)

        dst.commit()
    finally:
        try:
            dst.execute("DETACH DATABASE src")
        except Exception:
            pass
        dst.close()
        src.close()


def cleanup_invalid_derived_rows_in_app(fh) -> None:
    print(file=fh)
    print("===== LIMPEZA DE LINHAS DERIVADAS INVALIDAS NO app.db =====", file=fh)

    conn = connect(APP_DB)

    try:
        for table in ["structure_decisions", "payoff_curve_points"]:
            if not table_exists(conn, table):
                print(f"[SKIP] tabela ausente: {table}", file=fh)
                continue

            cols = columns(conn, table)

            if "timestamp" in cols:
                before = count_rows(conn, table)
                conn.execute(
                    f"""
                    DELETE FROM {qident(table)}
                    WHERE timestamp IS NULL OR TRIM(CAST(timestamp AS TEXT)) = ''
                    """
                )
                after = count_rows(conn, table)
                print(
                    f"[OK] limpeza timestamp {table}: antes={before}, depois={after}",
                    file=fh,
                )

        conn.commit()
    finally:
        conn.close()


def main() -> int:
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    with PRE_EVID.open("w", encoding="utf-8") as fh:
        print("===== DATA =====", file=fh)
        print(datetime.now().isoformat(sep=" ", timespec="seconds"), file=fh)
        print(file=fh)
        dump_db(APP_DB, "APP_DB PRE", fh)
        dump_db(DERIVED_DB, "DERIVED_DB PRE", fh)

    with OUT_EVID.open("w", encoding="utf-8") as fh:
        print("===== DATA =====", file=fh)
        print(datetime.now().isoformat(sep=" ", timespec="seconds"), file=fh)
        print(file=fh)

        backup_app_db(fh)
        bootstrap_via_derived_repo(fh)
        import_from_derived_db(fh)
        run_structure_id_migration(fh)
        cleanup_invalid_derived_rows_in_app(fh)

    with POST_EVID.open("w", encoding="utf-8") as fh:
        print("===== DATA =====", file=fh)
        print(datetime.now().isoformat(sep=" ", timespec="seconds"), file=fh)
        print(file=fh)
        dump_db(APP_DB, "APP_DB POS", fh)
        dump_db(DERIVED_DB, "DERIVED_DB POS", fh)

    print(f"[OK] evidencias geradas:")
    print(f"  - {PRE_EVID}")
    print(f"  - {OUT_EVID}")
    print(f"  - {POST_EVID}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
