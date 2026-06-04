"""
test_patch54 -- 18 checks cobrindo:
  - migração de schema (idempotência)
  - StructureRef.from_aba() com e sem lookup
  - StructureRef.from_id()
  - StructureRef.db_column() / db_value() / db_pair()
  - backfill de structure_id
  - ausência de regressão no legado aba
"""

import os
import sqlite3
import tempfile
import unittest

#  Ajuste de path para encontrar src/ 
import sys
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _ROOT)

from src.domain.refs.structure_ref import StructureRef
from scripts.patch54_migrate_derived_schema import (
    run_migrations,
    run_backfill,
    _column_exists,
    _table_exists,
)


#  Helpers 

def _make_derived_db(path: str, with_structure_id: bool = False) -> None:
    """Cria derived.db mínimo para testes."""
    conn = sqlite3.connect(path)
    sid_col = ", structure_id INTEGER NULL" if with_structure_id else ""
    conn.executescript(f"""
        CREATE TABLE IF NOT EXISTS payoff_curve_points (
            id INTEGER PRIMARY KEY,
            aba TEXT,
            timestamp TEXT,
            point_spot REAL,
            point_pl REAL
            {sid_col}
        );
        CREATE TABLE IF NOT EXISTS structure_decisions (
            id INTEGER PRIMARY KEY,
            aba TEXT,
            timestamp TEXT,
            level TEXT
            {sid_col}
        );
    """)
    conn.commit()
    conn.close()


def _make_app_db(path: str) -> None:
    """Cria app.db mínimo com tabela structures."""
    conn = sqlite3.connect(path)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS structures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            underlying_asset TEXT NOT NULL,
            alias_legacy_aba TEXT NULL,
            status TEXT NOT NULL DEFAULT 'active',
            created_at TEXT NOT NULL DEFAULT '2026-01-01T00:00:00',
            updated_at TEXT NOT NULL DEFAULT '2026-01-01T00:00:00'
        );
        INSERT INTO structures (name, underlying_asset, alias_legacy_aba)
        VALUES ('BOVA11 Condor', 'BOVA11', 'BOVA11');
        INSERT INTO structures (name, underlying_asset, alias_legacy_aba)
        VALUES ('PRIO3 Trava', 'PRIO3', 'PRIO3');
    """)
    conn.commit()
    conn.close()


# 
class TestPatch54SchemaMigration(unittest.TestCase):
    """Testa ADD COLUMN idempotente em derived.db."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.derived = os.path.join(self.tmp, "derived.db")
        _make_derived_db(self.derived)

    # P54-01
    def test_add_column_structure_id_payoff(self):
        conn = sqlite3.connect(self.derived)
        self.assertFalse(_column_exists(conn, "payoff_curve_points", "structure_id"))
        conn.close()

        run_migrations(self.derived)

        conn = sqlite3.connect(self.derived)
        self.assertTrue(_column_exists(conn, "payoff_curve_points", "structure_id"))
        conn.close()

    # P54-02
    def test_add_column_structure_id_decisions(self):
        run_migrations(self.derived)
        conn = sqlite3.connect(self.derived)
        self.assertTrue(_column_exists(conn, "structure_decisions", "structure_id"))
        conn.close()

    # P54-03
    def test_migration_idempotente(self):
        """Executar 3x não lança erro."""
        for _ in range(3):
            report = run_migrations(self.derived)
            statuses = [m["status"] for m in report["migrations"]]
            self.assertTrue(
                all(s in ("ADDED", "ALREADY_EXISTS") for s in statuses),
                f"status inesperado: {statuses}",
            )

    # P54-04
    def test_migration_preserva_dados_existentes(self):
        conn = sqlite3.connect(self.derived)
        conn.execute(
            "INSERT INTO payoff_curve_points (aba, timestamp, point_spot, point_pl) "
            "VALUES ('BOVA11', '2026-01-01T10:00:00', 100.0, 5.0)"
        )
        conn.commit()
        conn.close()

        run_migrations(self.derived)

        conn = sqlite3.connect(self.derived)
        rows = conn.execute("SELECT aba, point_spot FROM payoff_curve_points").fetchall()
        conn.close()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], "BOVA11")
        self.assertAlmostEqual(rows[0][1], 100.0)

    # P54-05
    def test_migration_tabela_inexistente_nao_quebra(self):
        """Se tabela não existe, status deve ser SKIPPED_TABLE_NOT_FOUND."""
        empty_db = os.path.join(self.tmp, "empty.db")
        sqlite3.connect(empty_db).close()
        report = run_migrations(empty_db)
        statuses = [m["status"] for m in report["migrations"]]
        self.assertTrue(all(s == "SKIPPED_TABLE_NOT_FOUND" for s in statuses))

    # P54-06
    def test_indice_criado_apos_migration(self):
        run_migrations(self.derived)
        conn = sqlite3.connect(self.derived)
        indices = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='index'"
        ).fetchall()
        nomes = [i[0] for i in indices]
        conn.close()
        self.assertIn("idx_payoff_structure_id", nomes)
        self.assertIn("idx_decisions_structure_id", nomes)


# 
class TestPatch54Backfill(unittest.TestCase):
    """Testa backfill structure_id a partir de alias_legacy_aba."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.derived = os.path.join(self.tmp, "derived.db")
        self.app    = os.path.join(self.tmp, "app.db")
        _make_derived_db(self.derived)
        _make_app_db(self.app)
        run_migrations(self.derived)

        # Insere dados legados no derived.db
        conn = sqlite3.connect(self.derived)
        conn.executescript("""
            INSERT INTO payoff_curve_points (aba, timestamp, point_spot, point_pl)
            VALUES ('BOVA11', '2026-01-01T10:00:00', 100.0, 5.0);
            INSERT INTO payoff_curve_points (aba, timestamp, point_spot, point_pl)
            VALUES ('PRIO3', '2026-01-01T10:00:00', 50.0, 2.0);
            INSERT INTO payoff_curve_points (aba, timestamp, point_spot, point_pl)
            VALUES ('unknown', '2026-01-01T10:00:00', 0.0, 0.0);
        """)
        conn.commit()
        conn.close()

    # P54-07
    def test_backfill_preenche_structure_id(self):
        result = run_backfill(self.derived, self.app)
        self.assertGreater(result["payoff_curve_points"], 0)

    # P54-08
    def test_backfill_nao_preenche_unknown(self):
        run_backfill(self.derived, self.app)
        conn = sqlite3.connect(self.derived)
        row = conn.execute(
            "SELECT structure_id FROM payoff_curve_points WHERE aba='unknown'"
        ).fetchone()
        conn.close()
        self.assertIsNone(row[0])

    # P54-09
    def test_backfill_idempotente(self):
        run_backfill(self.derived, self.app)
        run_backfill(self.derived, self.app)
        conn = sqlite3.connect(self.derived)
        rows = conn.execute(
            "SELECT structure_id FROM payoff_curve_points WHERE aba='BOVA11'"
        ).fetchall()
        conn.close()
        ids = [r[0] for r in rows]
        # Todos devem ser iguais (não duplicar nem sobrescrever com None)
        self.assertTrue(all(i == ids[0] for i in ids))
        self.assertIsNotNone(ids[0])

    # P54-10
    def test_backfill_sem_app_db_nao_quebra(self):
        result = run_backfill(self.derived, "/nao/existe/app.db")
        # Deve retornar sem lançar exceção
        self.assertIn("payoff_curve_points", result)


# 
class TestPatch54StructureRef(unittest.TestCase):
    """Testa StructureRef -- factories, db_column, db_value."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.app = os.path.join(self.tmp, "app.db")
        _make_app_db(self.app)

    # P54-11
    def test_from_id_canônico(self):
        ref = StructureRef.from_id(42)
        self.assertEqual(ref.structure_id, 42)
        self.assertIsNone(ref.aba)
        self.assertTrue(ref.is_canonical())

    # P54-12
    def test_from_aba_resolve_structure_id(self):
        ref = StructureRef.from_aba("BOVA11", app_db=self.app)
        self.assertIsNotNone(ref.structure_id)
        self.assertEqual(ref.aba, "BOVA11")
        self.assertTrue(ref.is_canonical())

    # P54-13
    def test_from_aba_sem_match_nao_quebra(self):
        ref = StructureRef.from_aba("ABA_INEXISTENTE", app_db=self.app)
        self.assertIsNone(ref.structure_id)
        self.assertEqual(ref.aba, "ABA_INEXISTENTE")
        self.assertFalse(ref.is_canonical())

    # P54-14
    def test_db_column_com_structure_id(self):
        ref = StructureRef.from_id(1)
        self.assertEqual(ref.db_column(), "structure_id")

    # P54-15
    def test_db_column_sem_structure_id(self):
        ref = StructureRef(aba="BOVA11")
        self.assertEqual(ref.db_column(), "aba")

    # P54-16
    def test_db_pair_retorna_tupla_correta(self):
        ref = StructureRef.from_id(7)
        col, val = ref.db_pair()
        self.assertEqual(col, "structure_id")
        self.assertEqual(val, 7)

    # P54-17
    def test_from_aba_vazia_levanta_value_error(self):
        with self.assertRaises(ValueError):
            StructureRef.from_aba("", app_db=self.app)

    # P54-18
    def test_sem_id_nem_aba_levanta_value_error(self):
        with self.assertRaises(ValueError):
            StructureRef()


if __name__ == "__main__":
    unittest.main(verbosity=2)
