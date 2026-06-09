# scripts/backfill_payoff_structure_id.py
import sqlite3
import os
import sys

# Garante que o path base é sempre a raiz do projeto
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DB    = os.path.join(PROJECT_ROOT, "dados", "app.db")
DERIVED_DB = os.path.join(PROJECT_ROOT, "dados", "derived.db")

def main():
    print(f"[backfill] APP_DB    : {APP_DB}")
    print(f"[backfill] DERIVED_DB: {DERIVED_DB}")

    if not os.path.exists(APP_DB):
        print(f"[backfill] ERRO: app.db não encontrado em {APP_DB}")
        sys.exit(1)
    if not os.path.exists(DERIVED_DB):
        print(f"[backfill] ERRO: derived.db não encontrado em {DERIVED_DB}")
        sys.exit(1)

    # 1. Lê mapeamento aba -> structure_id do app.db
    app_conn = sqlite3.connect(APP_DB)
    rows = app_conn.execute(
        "SELECT id, alias_legacy_aba FROM structures WHERE alias_legacy_aba IS NOT NULL"
    ).fetchall()
    app_conn.close()

    mapping = {alias.strip(): sid for sid, alias in rows}
    print(f"[backfill] Mapeamentos encontrados: {mapping}")

    if not mapping:
        print("[backfill] Nenhum mapeamento encontrado. Abortando.")
        sys.exit(1)

    # 2. Aplica no derived.db com URI mode para garantir write
    der_conn = sqlite3.connect(f"file:{DERIVED_DB}?mode=rwc", uri=True)
    der_conn.isolation_level = None  # autocommit OFF — controle manual

    total_payoff    = 0
    total_decisions = 0

    try:
        der_conn.execute("BEGIN")

        for aba, structure_id in mapping.items():
            # Diagnóstico por aba
            count_before = der_conn.execute(
                "SELECT COUNT(*) FROM payoff_curve_points WHERE aba = ?", (aba,)
            ).fetchone()[0]
            null_before = der_conn.execute(
                "SELECT COUNT(*) FROM payoff_curve_points WHERE aba = ? AND structure_id IS NULL",
                (aba,)
            ).fetchone()[0]
            print(f"[backfill] {aba}: total={count_before}, structure_id NULL={null_before}")

            # UPDATE payoff
            cur = der_conn.execute(
                "UPDATE payoff_curve_points SET structure_id = ? WHERE aba = ?",
                (structure_id, aba)
            )
            total_payoff += cur.rowcount

            # UPDATE decisions (opcional)
            try:
                cur2 = der_conn.execute(
                    "UPDATE structure_decisions SET structure_id = ? WHERE aba = ? AND structure_id IS NULL",
                    (structure_id, aba)
                )
                total_decisions += cur2.rowcount
            except sqlite3.OperationalError:
                pass

        der_conn.execute("COMMIT")

    except Exception as e:
        der_conn.execute("ROLLBACK")
        print(f"[backfill] ERRO: {e}")
        sys.exit(1)
    finally:
        der_conn.close()

    print(f"\n[backfill] payoff_curve_points atualizados : {total_payoff}")
    print(f"[backfill] structure_decisions  atualizados : {total_decisions}")
    print("[backfill] Concluído.")

if __name__ == "__main__":
    main()
