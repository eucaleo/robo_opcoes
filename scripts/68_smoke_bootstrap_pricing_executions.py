# scripts/68_smoke_bootstrap_pricing_executions.py
"""
Smoke patch_23 - garante que pricing_executions existe em dados/app.db
apos rodar o bootstrap.
"""
import os
import sys
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

DB_PATH = os.path.join(ROOT, "dados", "app.db")

from infra.bootstrap_structures_schema import bootstrap_pricing_executions


def run():
    print(f"[smoke] DB: {DB_PATH}")

    # 1. Executa bootstrap (idempotente)
    conn = sqlite3.connect(DB_PATH)
    try:
        bootstrap_pricing_executions(conn)
        print("[smoke] bootstrap_pricing_executions executado com sucesso.")
    finally:
        conn.close()

    # 2. Valida existencia da tabela
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='pricing_executions'"
        )
        row = cur.fetchone()
        assert row is not None, "FALHOU: tabela pricing_executions nao encontrada!"
        print("[smoke] OK - tabela pricing_executions existe.")

        # 3. Valida colunas
        cur.execute("PRAGMA table_info(pricing_executions)")
        cols = {r[1] for r in cur.fetchall()}
        expected = {
            "id", "structure_id", "reference_date", "status",
            "canonical_input", "engine_result", "error_message",
            "executed_at", "created_at",
        }
        missing = expected - cols
        assert not missing, f"FALHOU: colunas faltando: {missing}"
        print(f"[smoke] OK - colunas: {sorted(cols)}")

        # 4. Valida indices
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='pricing_executions'"
        )
        indexes = {r[0] for r in cur.fetchall()}
        expected_idx = {
            "idx_pricing_executions_structure_id",
            "idx_pricing_executions_reference_date",
            "idx_pricing_executions_status",
            "idx_pricing_executions_structure_date",
        }
        missing_idx = expected_idx - indexes
        assert not missing_idx, f"FALHOU: indices faltando: {missing_idx}"
        print(f"[smoke] OK - indices: {sorted(indexes)}")

        # 5. Idempotencia: roda bootstrap de novo, nao pode falhar
        conn2 = sqlite3.connect(DB_PATH)
        try:
            bootstrap_pricing_executions(conn2)
            print("[smoke] OK - bootstrap idempotente confirmado.")
        finally:
            conn2.close()

    finally:
        conn.close()

    print("\n[smoke] patch_23 - TUDO OK")


if __name__ == "__main__":
    run()
