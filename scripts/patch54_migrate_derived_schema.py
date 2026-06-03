"""
patch_54: migração de schema — ADD COLUMN structure_id nas tabelas do derived.db

Idempotente: pode ser executado N vezes sem erro.
Não destrói dados existentes.
Não altera coluna 'aba' (mantém retrocompatibilidade para leitura legada).

Tabelas afetadas:
  - payoff_curve_points      → ADD structure_id INTEGER NULL
  - structure_decisions      → ADD structure_id INTEGER NULL

Índices criados:
  - idx_payoff_structure_id
  - idx_decisions_structure_id

Pós-migração:
  - Backfill structure_id a partir de structures.alias_legacy_aba (app.db)
    para linhas onde aba != 'unknown' e structure_id IS NULL
"""

import sqlite3
import os
import sys
from datetime import datetime, timezone

# ── Paths canônicos (conforme rota_v2b.pdf + git) ─────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DERIVED_DB  = os.path.join(BASE_DIR, "dados", "derived.db")
APP_DB      = os.path.join(BASE_DIR, "dados", "app.db")
REPORT_PATH = os.path.join(BASE_DIR, "ATT", "reports", "patch54_migration_report.json")

# ── Colunas a adicionar por tabela ─────────────────────────────────────────────
MIGRATIONS = [
    {
        "table":  "payoff_curve_points",
        "column": "structure_id",
        "ddl":    "ALTER TABLE payoff_curve_points ADD COLUMN structure_id INTEGER NULL",
        "index":  "CREATE INDEX IF NOT EXISTS idx_payoff_structure_id "
                  "ON payoff_curve_points(structure_id)",
    },
    {
        "table":  "structure_decisions",
        "column": "structure_id",
        "ddl":    "ALTER TABLE structure_decisions ADD COLUMN structure_id INTEGER NULL",
        "index":  "CREATE INDEX IF NOT EXISTS idx_decisions_structure_id "
                  "ON structure_decisions(structure_id)",
    },
]


def _column_exists(conn: sqlite3.Connection, table: str, column: str) -> bool:
    """Verifica se coluna já existe — workaround para ausência de IF NOT EXISTS no SQLite."""
    cur = conn.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cur.fetchall())


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,)
    )
    return cur.fetchone() is not None


def run_migrations(derived_db: str = DERIVED_DB) -> dict:
    """
    Executa ADD COLUMN idempotente em derived.db.
    Retorna relatório com status por tabela.
    """
    if not os.path.exists(derived_db):
        raise FileNotFoundError(f"derived.db não encontrado: {derived_db}")

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "derived_db": derived_db,
        "migrations": [],
    }

    conn = sqlite3.connect(derived_db)
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")

        for m in MIGRATIONS:
            entry = {"table": m["table"], "column": m["column"]}

            if not _table_exists(conn, m["table"]):
                entry["status"] = "SKIPPED_TABLE_NOT_FOUND"
                report["migrations"].append(entry)
                print(f"  [SKIP]  tabela '{m['table']}' não existe ainda")
                continue

            if _column_exists(conn, m["table"], m["column"]):
                entry["status"] = "ALREADY_EXISTS"
                report["migrations"].append(entry)
                print(f"  [OK]    {m['table']}.{m['column']} já existe — noop")
            else:
                conn.execute(m["ddl"])
                conn.commit()
                entry["status"] = "ADDED"
                report["migrations"].append(entry)
                print(f"  [ADD]   {m['table']}.{m['column']} adicionada")

            # Índice sempre com IF NOT EXISTS — seguro repetir
            conn.execute(m["index"])
            conn.commit()
            print(f"  [IDX]   índice em {m['table']}.{m['column']} garantido")

    finally:
        conn.close()

    return report


def run_backfill(derived_db: str = DERIVED_DB, app_db: str = APP_DB) -> dict:
    """
    Backfill: para linhas onde aba != 'unknown' e structure_id IS NULL,
    tenta resolver structure_id via structures.alias_legacy_aba em app.db.

    Seguro: UPDATE nunca sobrescreve structure_id já preenchido.
    """
    backfill = {"payoff_curve_points": 0, "structure_decisions": 0, "no_match": []}

    if not os.path.exists(app_db):
        print(f"  [WARN]  app.db não encontrado ({app_db}) — backfill pulado")
        return backfill

    app_conn     = sqlite3.connect(app_db)
    derived_conn = sqlite3.connect(derived_db)

    try:
        # Monta dicionário alias → structure_id a partir de app.db
        alias_map: dict[str, int] = {}
        try:
            rows = app_conn.execute(
                "SELECT id, alias_legacy_aba FROM structures "
                "WHERE alias_legacy_aba IS NOT NULL AND alias_legacy_aba != ''"
            ).fetchall()
            alias_map = {row[1]: row[0] for row in rows}
        except sqlite3.OperationalError:
            print("  [WARN]  tabela structures não existe em app.db — backfill parcial")

        if not alias_map:
            print("  [INFO]  nenhum alias_legacy_aba encontrado — backfill vazio")
            return backfill

        for table in ("payoff_curve_points", "structure_decisions"):
            if not _table_exists(derived_conn, table):
                continue
            if not _column_exists(derived_conn, table, "structure_id"):
                continue

            rows_to_fill = derived_conn.execute(
                f"SELECT DISTINCT aba FROM {table} "
                f"WHERE structure_id IS NULL AND aba != 'unknown' AND aba IS NOT NULL"
            ).fetchall()

            updated = 0
            no_match = []

            for (aba,) in rows_to_fill:
                sid = alias_map.get(aba)
                if sid is not None:
                    derived_conn.execute(
                        f"UPDATE {table} SET structure_id = ? "
                        f"WHERE aba = ? AND structure_id IS NULL",
                        (sid, aba),
                    )
                    updated += derived_conn.execute(
                        "SELECT changes()"
                    ).fetchone()[0]
                else:
                    no_match.append(aba)

            derived_conn.commit()
            backfill[table] = updated
            backfill["no_match"] = list(set(backfill["no_match"] + no_match))
            print(f"  [FILL]  {table}: {updated} linhas atualizadas")
            if no_match:
                print(f"  [WARN]  {table}: sem match para abas: {no_match}")

    finally:
        app_conn.close()
        derived_conn.close()

    return backfill


def save_report(report: dict, path: str = REPORT_PATH) -> None:
    import json
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"  [RPT]   relatório salvo em {path}")


if __name__ == "__main__":
    print("=" * 60)
    print("patch_54 — migração de schema derived.db")
    print("=" * 60)

    print("\n[1/3] Executando ADD COLUMN...")
    report = run_migrations()

    print("\n[2/3] Executando backfill structure_id...")
    backfill = run_backfill()
    report["backfill"] = backfill

    print("\n[3/3] Salvando relatório...")
    save_report(report)

    print("\n✓ patch_54 concluído.")

    # Exit code não-zero se alguma migration falhou
    failed = [m for m in report["migrations"] if m["status"] not in
              ("ADDED", "ALREADY_EXISTS", "SKIPPED_TABLE_NOT_FOUND")]
    sys.exit(1 if failed else 0)
