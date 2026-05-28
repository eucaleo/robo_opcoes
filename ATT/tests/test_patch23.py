# ATT/tests/test_patch23.py
"""
Testes pytest - patch_23
Valida criacao da tabela pricing_executions via bootstrap.
"""
import os
import sys
import sqlite3
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from infra.bootstrap_structures_schema import bootstrap_pricing_executions


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------

@pytest.fixture()
def tmp_conn():
    conn = sqlite3.connect(":memory:")
    yield conn
    conn.close()


@pytest.fixture()
def bootstrapped_conn(tmp_conn):
    bootstrap_pricing_executions(tmp_conn)
    return tmp_conn


# ------------------------------------------------------------------
# Testes
# ------------------------------------------------------------------

class TestPatch23Bootstrap:

    def test_patch23_table_exists(self, bootstrapped_conn):
        cur = bootstrapped_conn.cursor()
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='pricing_executions'"
        )
        assert cur.fetchone() is not None, "Tabela pricing_executions nao criada."

    def test_patch23_schema_tables_and_indexes(self, bootstrapped_conn):
        cur = bootstrapped_conn.cursor()
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='pricing_executions'"
        )
        indexes = {r[0] for r in cur.fetchall()}
        expected = {
            "idx_pricing_executions_structure_id",
            "idx_pricing_executions_reference_date",
            "idx_pricing_executions_status",
            "idx_pricing_executions_structure_date",
        }
        missing = expected - indexes
        assert not missing, f"Indices faltando: {missing}"

    def test_patch23_pricing_executions_columns(self, bootstrapped_conn):
        cur = bootstrapped_conn.cursor()
        cur.execute("PRAGMA table_info(pricing_executions)")
        cols = {r[1] for r in cur.fetchall()}
        required = {
            "id", "structure_id", "reference_date", "status",
            "canonical_input", "engine_result", "error_message",
            "executed_at", "created_at",
        }
        missing = required - cols
        assert not missing, f"Colunas faltando: {missing}"

    def test_patch23_bootstrap_is_idempotent(self, bootstrapped_conn):
        try:
            bootstrap_pricing_executions(bootstrapped_conn)
        except Exception as exc:
            pytest.fail(f"Bootstrap nao e idempotente: {exc}")

    def test_patch23_insert_and_read(self, bootstrapped_conn):
        cur = bootstrapped_conn.cursor()
        cur.execute(
            """
            INSERT INTO pricing_executions
                (structure_id, reference_date, status, executed_at, created_at)
            VALUES (1, '2026-05-28', 'ok', '2026-05-28T19:00:00', '2026-05-28T19:00:00')
            """
        )
        bootstrapped_conn.commit()
        cur.execute(
            "SELECT structure_id, status FROM pricing_executions WHERE id=1"
        )
        row = cur.fetchone()
        assert row is not None
        assert row[0] == 1
        assert row[1] == "ok"

    def test_patch23_status_default_is_ok(self, bootstrapped_conn):
        cur = bootstrapped_conn.cursor()
        cur.execute("PRAGMA table_info(pricing_executions)")
        col_info = {r[1]: r[4] for r in cur.fetchall()}
        assert col_info.get("status") == "'ok'", (
            f"Default de status esperado 'ok', encontrado: {col_info.get('status')}"
        )

    def test_patch23_app_db_has_table(self):
        db_path = os.path.join(ROOT, "dados", "app.db")
        if not os.path.isfile(db_path):
            pytest.skip("dados/app.db nao encontrado.")
        conn = sqlite3.connect(db_path)
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='pricing_executions'"
            )
            assert cur.fetchone() is not None, (
                "pricing_executions ausente em dados/app.db - rode o bootstrap primeiro."
            )
        finally:
            conn.close()
