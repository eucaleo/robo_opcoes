# ATT/patches/patch_29_add_structure_id_to_decisions.py
"""
patch_29 — Adiciona structure_id em structure_decisions (derived.db)

Operações:
  1. ALTER TABLE structure_decisions ADD COLUMN structure_id INTEGER
  2. CREATE INDEX idx_decisions_structure_id
  3. Backfill: resolve aba → structures.id via app.db e atualiza derived.db
  4. Relatório final de cobertura

Política:
  - Idempotente: pode rodar N vezes sem efeito colateral
  - Não remove dados existentes
  - Não cria FK real (bancos separados — soft FK intencional)
  - Rollback disponível via BAK/ criado antes de qualquer alteração

Reversão manual:
  sqlite3 dados/derived.db "ALTER TABLE structure_decisions RENAME TO structure_decisions_bak_29"
  (ou restaurar de BAK/)
"""

import sqlite3
import shutil
from datetime import datetime
from pathlib import Path

# ──────────────────────────────────────────────
# Configuração
# ──────────────────────────────────────────────

DERIVED_DB  = Path("dados/derived.db")
APP_DB      = Path("dados/app.db")
BAK_DIR     = Path("BAK")
PATCH_NAME  = "patch_29"


# ──────────────────────────────────────────────
# Utilitários
# ──────────────────────────────────────────────

def _backup(path: Path) -> Path:
    """Cria cópia de segurança antes de qualquer alteração."""
    BAK_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = BAK_DIR / f"{path.stem}__{PATCH_NAME}__{ts}{path.suffix}"
    shutil.copy2(path, dest)
    print(f"  [bak] {path} → {dest}")
    return dest


def _table_columns(conn: sqlite3.Connection, table: str) -> list[str]:
    cur = conn.execute(f"PRAGMA table_info({table})")
    return [row[1] for row in cur.fetchall()]


def _index_names(conn: sqlite3.Connection, table: str) -> list[str]:
    cur = conn.execute(f"PRAGMA index_list({table})")
    return [row[1] for row in cur.fetchall()]


# ──────────────────────────────────────────────
# Passo 1 — Adicionar coluna
# ──────────────────────────────────────────────

def step_add_column(conn: sqlite3.Connection) -> None:
    print("\n[step 1] Verificando coluna structure_id ...")

    cols = _table_columns(conn, "structure_decisions")

    if "structure_id" in cols:
        print("  [skip] Coluna structure_id já existe.")
        return

    conn.execute(
        "ALTER TABLE structure_decisions ADD COLUMN structure_id INTEGER"
    )
    conn.commit()
    print("  [ok] Coluna structure_id adicionada (nullable INTEGER).")


# ──────────────────────────────────────────────
# Passo 2 — Criar índice
# ──────────────────────────────────────────────

def step_create_index(conn: sqlite3.Connection) -> None:
    print("\n[step 2] Verificando índice idx_decisions_structure_id ...")

    indexes = _index_names(conn, "structure_decisions")

    if "idx_decisions_structure_id" in indexes:
        print("  [skip] Índice já existe.")
        return

    conn.execute("""
        CREATE INDEX idx_decisions_structure_id
        ON structure_decisions (structure_id)
    """)
    conn.commit()
    print("  [ok] Índice idx_decisions_structure_id criado.")


# ──────────────────────────────────────────────
# Passo 3 — Backfill via app.db
# ──────────────────────────────────────────────

def step_backfill(conn_derived: sqlite3.Connection) -> dict:
    """
    Lê structures.alias_legacy_aba do app.db e faz UPDATE em derived.db.

    Mapeamento:
      structures.alias_legacy_aba  →  structure_decisions.aba
      structures.id                →  structure_decisions.structure_id
    """
    print("\n[step 3] Backfill structure_id ...")

    if not APP_DB.exists():
        print(f"  [warn] app.db não encontrado em {APP_DB}. Backfill ignorado.")
        return {"mapped": 0, "skipped": 0, "not_found": []}

    # Carrega mapeamento aba → structure_id do app.db
    conn_app = sqlite3.connect(APP_DB)
    try:
        cur = conn_app.execute("""
            SELECT id, alias_legacy_aba, name
            FROM structures
            WHERE alias_legacy_aba IS NOT NULL
              AND alias_legacy_aba != ''
        """)
        rows = cur.fetchall()
    finally:
        conn_app.close()

    if not rows:
        print("  [warn] Nenhuma structure com alias_legacy_aba encontrada em app.db.")
        return {"mapped": 0, "skipped": 0, "not_found": []}

    aba_to_id: dict[str, int] = {row[1]: row[0] for row in rows}
    print(f"  [info] {len(aba_to_id)} mapeamentos carregados do app.db:")
    for aba, sid in sorted(aba_to_id.items()):
        print(f"         {aba!r:20s} → structure_id={sid}")

    # Abas distintas em structure_decisions que ainda não têm structure_id
    cur2 = conn_derived.execute("""
        SELECT DISTINCT aba
        FROM structure_decisions
        WHERE structure_id IS NULL
    """)
    abas_pendentes = [row[0] for row in cur2.fetchall()]

    if not abas_pendentes:
        print("  [skip] Nenhum registro sem structure_id. Backfill desnecessário.")
        return {"mapped": 0, "skipped": 0, "not_found": []}

    print(f"  [info] {len(abas_pendentes)} aba(s) com structure_id NULL: {abas_pendentes}")

    mapped    = 0
    skipped   = 0
    not_found = []

    for aba in abas_pendentes:
        sid = aba_to_id.get(aba)

        if sid is None:
            print(f"  [warn] aba={aba!r} não encontrada em structures. Mantendo NULL.")
            not_found.append(aba)
            skipped += 1
            continue

        cur3 = conn_derived.execute("""
            UPDATE structure_decisions
            SET structure_id = ?
            WHERE aba = ?
              AND structure_id IS NULL
        """, (sid, aba))

        affected = cur3.rowcount
        mapped  += affected
        print(f"  [ok] aba={aba!r} → structure_id={sid} ({affected} linha(s) atualizada(s))")

    conn_derived.commit()
    return {"mapped": mapped, "skipped": skipped, "not_found": not_found}


# ──────────────────────────────────────────────
# Passo 4 — Relatório de cobertura
# ──────────────────────────────────────────────

def step_report(conn: sqlite3.Connection, backfill_result: dict) -> None:
    print("\n[step 4] Relatório de cobertura ...")

    cur = conn.execute("SELECT COUNT(*) FROM structure_decisions")
    total = cur.fetchone()[0]

    cur = conn.execute(
        "SELECT COUNT(*) FROM structure_decisions WHERE structure_id IS NOT NULL"
    )
    with_id = cur.fetchone()[0]

    cur = conn.execute(
        "SELECT COUNT(*) FROM structure_decisions WHERE structure_id IS NULL"
    )
    without_id = cur.fetchone()[0]

    pct = (with_id / total * 100) if total else 0

    print(f"\n  {'─'*45}")
    print(f"  Total de decisões              : {total:>6}")
    print(f"  Com    structure_id preenchido : {with_id:>6}  ({pct:.1f}%)")
    print(f"  Sem    structure_id (NULL)     : {without_id:>6}")
    print(f"  Abas não mapeadas (app.db)     : {backfill_result['not_found']}")
    print(f"  {'─'*45}")

    # Distribuição por aba
    cur = conn.execute("""
        SELECT aba, structure_id, COUNT(*) as n
        FROM structure_decisions
        GROUP BY aba, structure_id
        ORDER BY aba
    """)
    print(f"\n  {'ABA':<20} {'structure_id':>12}  {'registros':>10}")
    print(f"  {'─'*45}")
    for row in cur.fetchall():
        sid_str = str(row[1]) if row[1] is not None else "NULL ⚠"
        print(f"  {row[0]:<20} {sid_str:>12}  {row[2]:>10}")

    print()

    if without_id == 0:
        print("  ✅ patch_29 concluído — cobertura 100%")
    else:
        print(f"  ⚠️  patch_29 concluído — {without_id} linha(s) sem structure_id")
        print("     → Abas não mapeadas precisam de entrada manual em structures")
        print("       ou serão resolvidas pelo patch_30 (enriquecimento na escrita)")


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main() -> None:
    print(f"{'='*50}")
    print(f"  {PATCH_NAME} — add structure_id to structure_decisions")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")

    # Pré-checks
    if not DERIVED_DB.exists():
        raise FileNotFoundError(f"derived.db não encontrado: {DERIVED_DB}")

    # Backup antes de qualquer alteração
    print("\n[bak] Criando backups ...")
    _backup(DERIVED_DB)
    if APP_DB.exists():
        _backup(APP_DB)

    # Executa passos
    with sqlite3.connect(DERIVED_DB) as conn:
        step_add_column(conn)
        step_create_index(conn)
        backfill_result = step_backfill(conn)
        step_report(conn, backfill_result)

    print(f"\n{'='*50}")
    print(f"  Patch finalizado.")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
