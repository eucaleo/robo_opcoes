from __future__ import annotations

import shutil
import sqlite3
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
APP_DB = ROOT / "dados" / "app.db"
DERIVED_DB = ROOT / "dados" / "derived.db"
EVID_DIR = ROOT / "FRENTE_BD_UNICO_APPDB" / "evidencias"
BACKUP_DIR = ROOT / "FRENTE_BD_UNICO_APPDB" / "backups"

OUT = EVID_DIR / "25_phase1c_structure_decisions_migration.txt"


DERIVED_DECISION_COLUMNS = {
    "timestamp": "TEXT",
    "aba": "TEXT",
    "level": "INTEGER",
    "pl_atual": "REAL",
    "pl_max": "REAL",
    "pl_pct_of_max": "REAL",
    "dte_min": "INTEGER",
    "why_json": "TEXT",
    "spot_ref": "REAL",
    "meta_json": "TEXT",
    "why": "TEXT",
}


def qident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def connect(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path))
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


def count(conn: sqlite3.Connection, table: str) -> int:
    return int(conn.execute(f"SELECT COUNT(*) FROM {qident(table)}").fetchone()[0])


def scalar(conn: sqlite3.Connection, sql: str):
    try:
        row = conn.execute(sql).fetchone()
        return row[0] if row else None
    except Exception as exc:
        return f"ERRO: {exc}"


def dump_table_state(conn: sqlite3.Connection, label: str, fh) -> None:
    print(f"===== {label} =====", file=fh)

    if not table_exists(conn, "structure_decisions"):
        print("structure_decisions: AUSENTE", file=fh)
        print(file=fh)
        return

    cols = columns(conn, "structure_decisions")
    print(f"columns: {cols}", file=fh)
    print(f"count: {count(conn, 'structure_decisions')}", file=fh)

    if "timestamp" in cols:
        print(
            "timestamp_null_or_empty:",
            scalar(
                conn,
                """
                SELECT COUNT(*)
                FROM structure_decisions
                WHERE timestamp IS NULL OR TRIM(CAST(timestamp AS TEXT)) = ''
                """,
            ),
            file=fh,
        )

    if "aba" in cols:
        print(
            "aba_null_or_empty:",
            scalar(
                conn,
                """
                SELECT COUNT(*)
                FROM structure_decisions
                WHERE aba IS NULL OR TRIM(CAST(aba AS TEXT)) = ''
                """,
            ),
            file=fh,
        )

    if "structure_id" in cols:
        print(
            "structure_id_null:",
            scalar(
                conn,
                """
                SELECT COUNT(*)
                FROM structure_decisions
                WHERE structure_id IS NULL
                """,
            ),
            file=fh,
        )

    print("sample:", file=fh)
    for row in conn.execute(
        """
        SELECT *
        FROM structure_decisions
        ORDER BY id
        LIMIT 10
        """
    ):
        print(dict(row), file=fh)

    print(file=fh)


def backup_app(fh) -> None:
    if not APP_DB.exists():
        print("[ERRO] dados/app.db nao existe.", file=fh)
        raise SystemExit(1)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = BACKUP_DIR / f"app_pre_phase1c_{stamp}.db"
    shutil.copy2(APP_DB, backup)
    print(f"[OK] backup criado: {backup}", file=fh)


def add_missing_columns(conn: sqlite3.Connection, fh) -> None:
    existing = set(columns(conn, "structure_decisions"))

    for col, typ in DERIVED_DECISION_COLUMNS.items():
        if col not in existing:
            conn.execute(
                f"ALTER TABLE structure_decisions ADD COLUMN {qident(col)} {typ}"
            )
            print(f"[OK] coluna adicionada: structure_decisions.{col} {typ}", file=fh)
        else:
            print(f"[SKIP] coluna ja existe: structure_decisions.{col}", file=fh)

    conn.commit()


def merge_from_derived(app: sqlite3.Connection, fh) -> None:
    if not DERIVED_DB.exists():
        print("[WARN] dados/derived.db nao existe; merge por origem ignorado.", file=fh)
        return

    src = connect(DERIVED_DB)

    try:
        if not table_exists(src, "structure_decisions"):
            print("[WARN] derived.db nao possui structure_decisions.", file=fh)
            return

        src_cols = set(columns(src, "structure_decisions"))
        app_cols = set(columns(app, "structure_decisions"))

        common = [
            c
            for c in [
                "timestamp",
                "aba",
                "decision",
                "level",
                "pl_atual",
                "pl_max",
                "pl_pct_of_max",
                "dte_min",
                "why_json",
                "spot_ref",
                "meta_json",
                "created_at",
                "why",
                "structure_id",
            ]
            if c in src_cols and c in app_cols
        ]

        print(f"[INFO] colunas comuns para merge: {common}", file=fh)

        app.execute("ATTACH DATABASE ? AS src", (str(DERIVED_DB),))

        # Atualiza linhas existentes por id.
        set_sql = ", ".join(
            f"{qident(c)} = (SELECT {qident(c)} FROM src.structure_decisions s WHERE s.id = structure_decisions.id)"
            for c in common
            if c != "id"
        )

        if set_sql:
            app.execute(
                f"""
                UPDATE structure_decisions
                SET {set_sql}
                WHERE id IN (
                    SELECT id
                    FROM src.structure_decisions
                )
                """
            )
            print("[OK] linhas existentes atualizadas por id a partir do derived.db", file=fh)

        # Insere linhas que existem no derived.db e nao existem no app.db.
        insert_cols = ["id"] + common
        insert_cols = []
        for c in ["id"] + common:
            if c in src_cols and c in app_cols and c not in insert_cols:
                insert_cols.append(c)

        if insert_cols:
            col_sql = ", ".join(qident(c) for c in insert_cols)
            app.execute(
                f"""
                INSERT OR IGNORE INTO structure_decisions ({col_sql})
                SELECT {col_sql}
                FROM src.structure_decisions
                """
            )
            print("[OK] linhas ausentes inseridas a partir do derived.db", file=fh)

        app.commit()

    finally:
        try:
            app.execute("DETACH DATABASE src")
        except Exception:
            pass
        src.close()


def fill_fallbacks(app: sqlite3.Connection, fh) -> None:
    cols = set(columns(app, "structure_decisions"))

    if "timestamp" in cols:
        before = scalar(
            app,
            """
            SELECT COUNT(*)
            FROM structure_decisions
            WHERE timestamp IS NULL OR TRIM(CAST(timestamp AS TEXT)) = ''
            """,
        )

        app.execute(
            """
            UPDATE structure_decisions
            SET timestamp = COALESCE(
                NULLIF(TRIM(CAST(timestamp AS TEXT)), ''),
                NULLIF(TRIM(CAST(created_at AS TEXT)), ''),
                datetime('now', 'localtime')
            )
            WHERE timestamp IS NULL OR TRIM(CAST(timestamp AS TEXT)) = ''
            """
        )

        after = scalar(
            app,
            """
            SELECT COUNT(*)
            FROM structure_decisions
            WHERE timestamp IS NULL OR TRIM(CAST(timestamp AS TEXT)) = ''
            """,
        )

        print(f"[OK] fallback timestamp: antes={before}, depois={after}", file=fh)

    if "aba" in cols:
        before = scalar(
            app,
            """
            SELECT COUNT(*)
            FROM structure_decisions
            WHERE aba IS NULL OR TRIM(CAST(aba AS TEXT)) = ''
            """,
        )

        if "structure_id" in cols:
            app.execute(
                """
                UPDATE structure_decisions
                SET aba = CAST(structure_id AS TEXT)
                WHERE aba IS NULL OR TRIM(CAST(aba AS TEXT)) = ''
                """
            )
        else:
            app.execute(
                """
                UPDATE structure_decisions
                SET aba = '0'
                WHERE aba IS NULL OR TRIM(CAST(aba AS TEXT)) = ''
                """
            )

        after = scalar(
            app,
            """
            SELECT COUNT(*)
            FROM structure_decisions
            WHERE aba IS NULL OR TRIM(CAST(aba AS TEXT)) = ''
            """,
        )

        print(f"[OK] fallback aba: antes={before}, depois={after}", file=fh)

    if "level" in cols:
        app.execute(
            """
            UPDATE structure_decisions
            SET level = COALESCE(level, 0)
            WHERE level IS NULL
            """
        )
        print("[OK] fallback level aplicado", file=fh)

    app.commit()


def create_indexes(app: sqlite3.Connection, fh) -> None:
    cols = set(columns(app, "structure_decisions"))

    if {"structure_id", "timestamp"}.issubset(cols):
        app.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_structure_decisions_sid_ts
            ON structure_decisions (structure_id, timestamp)
            """
        )
        print("[OK] indice idx_structure_decisions_sid_ts garantido", file=fh)

    if {"aba", "timestamp"}.issubset(cols):
        app.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_structure_decisions_aba_ts
            ON structure_decisions (aba, timestamp)
            """
        )
        print("[OK] indice idx_structure_decisions_aba_ts garantido", file=fh)

    app.commit()


def main() -> int:
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    with OUT.open("w", encoding="utf-8") as fh:
        print("===== DATA =====", file=fh)
        print(datetime.now().isoformat(sep=" ", timespec="seconds"), file=fh)
        print(file=fh)

        backup_app(fh)

        app = connect(APP_DB)

        try:
            print("===== PRE =====", file=fh)
            dump_table_state(app, "APP structure_decisions PRE", fh)

            if not table_exists(app, "structure_decisions"):
                print("[ERRO] app.db nao possui structure_decisions.", file=fh)
                return 1

            print("===== ALTER TABLE =====", file=fh)
            add_missing_columns(app, fh)

            print(file=fh)
            print("===== MERGE DERIVED -> APP =====", file=fh)
            merge_from_derived(app, fh)

            print(file=fh)
            print("===== FALLBACKS =====", file=fh)
            fill_fallbacks(app, fh)

            print(file=fh)
            print("===== INDEXES =====", file=fh)
            create_indexes(app, fh)

            print(file=fh)
            print("===== POS =====", file=fh)
            dump_table_state(app, "APP structure_decisions POS", fh)

        finally:
            app.close()

    print(f"[OK] evidencia gerada: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
