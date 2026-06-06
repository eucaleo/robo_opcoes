# ATT/tests/test_patch72.py
"""
Testes formais do patch_72.
Audit trail de mutacoes em structures via structure_audit_log.
"""
from __future__ import annotations

import json
import os
import sqlite3
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

REPO_FILE       = os.path.join(ROOT, "repositories", "structures_repository.py")
BOOTSTRAP_FILE  = os.path.join(ROOT, "infra", "bootstrap_structures_schema.py")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def _make_tmp_db() -> str:
    """Cria banco temporario com schema completo incluindo audit_log."""
    f = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp_path = f.name
    f.close()

    conn = sqlite3.connect(tmp_path)
    conn.execute("PRAGMA foreign_keys = ON;")

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS structures (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            name             TEXT    NOT NULL,
            underlying_asset TEXT    NOT NULL,
            alias_legacy_aba TEXT,
            status           TEXT    NOT NULL DEFAULT 'active',
            notes            TEXT,
            created_at       TEXT    NOT NULL,
            updated_at       TEXT    NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS structure_legs (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            structure_id    INTEGER NOT NULL,
            position_side   TEXT    NOT NULL,
            option_type     TEXT    NOT NULL,
            symbol          TEXT,
            strike          REAL    NOT NULL,
            expiration_date TEXT    NOT NULL,
            quantity        INTEGER NOT NULL,
            premium         REAL,
            multiplier      REAL    NOT NULL DEFAULT 1,
            leg_order       INTEGER NOT NULL,
            notes           TEXT,
            created_at      TEXT    NOT NULL,
            updated_at      TEXT    NOT NULL,
            FOREIGN KEY (structure_id) REFERENCES structures(id) ON DELETE CASCADE
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS structure_audit_log (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            structure_id INTEGER NOT NULL,
            action       TEXT    NOT NULL,
            changed_by   TEXT,
            changed_at   TEXT    NOT NULL,
            before_json  TEXT,
            after_json   TEXT,
            notes        TEXT,
            FOREIGN KEY (structure_id) REFERENCES structures(id)
        )
        """
    )
    conn.commit()
    conn.close()
    return tmp_path


def _leg_payload(leg_order: int = 1) -> dict:
    return {
        "position_side":   "LONG",
        "option_type":     "CALL",
        "strike":          100.0,
        "expiration_date": "2027-01-15",
        "quantity":        1000,
        "multiplier":      1.0,
        "leg_order":       leg_order,
    }


# ---------------------------------------------------------------------------
# Checks estaticos
# ---------------------------------------------------------------------------

class TestPatch72ArquivosExistem(unittest.TestCase):
    def test_repo_existe(self):
        self.assertTrue(os.path.isfile(REPO_FILE))

    def test_bootstrap_existe(self):
        self.assertTrue(os.path.isfile(BOOTSTRAP_FILE))


class TestPatch72EstaticoRepo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src = _read(REPO_FILE)

    def test_patch72_no_header(self):
        self.assertIn("PATCH_72", self.src)

    def test_tabela_structure_audit_log_referenciada(self):
        self.assertIn("structure_audit_log", self.src)

    def test_log_action_definido(self):
        self.assertIn("def _log_action", self.src)

    def test_get_audit_log_definido(self):
        self.assertIn("def get_audit_log", self.src)

    def test_get_full_audit_log_definido(self):
        self.assertIn("def get_full_audit_log", self.src)

    def test_audit_actions_definido(self):
        self.assertIn("AUDIT_ACTIONS", self.src)

    def test_create_registra_log(self):
        self.assertIn('"CREATE"', self.src)

    def test_update_registra_log(self):
        self.assertIn('"UPDATE"', self.src)

    def test_archive_registra_log(self):
        self.assertIn('"ARCHIVE"', self.src)

    def test_add_leg_registra_log(self):
        self.assertIn('"ADD_LEG"', self.src)

    def test_replace_legs_registra_log(self):
        self.assertIn('"REPLACE_LEGS"', self.src)

    def test_nao_importa_sqlite3_legado(self):
        # _log_action nao deve abrir conexao propria via sqlite3.connect
        body_after_log = self.src.split("def _log_action")[1].split("def ")[0]
        self.assertNotIn("sqlite3.connect", body_after_log)


class TestPatch72EstaticoBootstrap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src = _read(BOOTSTRAP_FILE)

    def test_tabela_structure_audit_log_no_bootstrap(self):
        self.assertIn("structure_audit_log", self.src)

    def test_idx_audit_log_structure_id(self):
        self.assertIn("idx_audit_log_structure_id", self.src)

    def test_idx_audit_log_changed_at(self):
        self.assertIn("idx_audit_log_changed_at", self.src)

    def test_patch72_no_bootstrap(self):
        self.assertIn("PATCH_72", self.src)


# ---------------------------------------------------------------------------
# Checks funcionais
# ---------------------------------------------------------------------------

class TestPatch72LogCreate(unittest.TestCase):
    def setUp(self):
        self.tmp = _make_tmp_db()

    def tearDown(self):
        os.unlink(self.tmp)

    def test_create_gera_uma_entrada_no_log(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        sid = repo.create_structure({
            "name": "Condor BOVA11",
            "underlying_asset": "BOVA11",
        })
        log = repo.get_audit_log(sid)
        self.assertEqual(len(log), 1)
        self.assertEqual(log[0]["action"], "CREATE")

    def test_create_log_before_json_e_none(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        sid = repo.create_structure({
            "name": "Trava PETR4",
            "underlying_asset": "PETR4",
        })
        log = repo.get_audit_log(sid)
        self.assertIsNone(log[0]["before_json"])

    def test_create_log_after_json_contem_name(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        sid = repo.create_structure({
            "name": "Borboleta VALE3",
            "underlying_asset": "VALE3",
        })
        log = repo.get_audit_log(sid)
        after = json.loads(log[0]["after_json"])
        self.assertEqual(after["name"], "Borboleta VALE3")

    def test_create_log_structure_id_correto(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        sid = repo.create_structure({
            "name": "Iron Condor",
            "underlying_asset": "IBOV",
        })
        log = repo.get_audit_log(sid)
        self.assertEqual(log[0]["structure_id"], sid)


class TestPatch72LogUpdate(unittest.TestCase):
    def setUp(self):
        self.tmp = _make_tmp_db()
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        self.sid = repo.create_structure({
            "name": "Original",
            "underlying_asset": "PETR4",
        })

    def tearDown(self):
        os.unlink(self.tmp)

    def test_update_gera_entrada_update_no_log(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        repo.update_structure(self.sid, {"name": "Atualizado"})
        log = repo.get_audit_log(self.sid)
        actions = [e["action"] for e in log]
        self.assertIn("UPDATE", actions)

    def test_update_log_before_json_contem_nome_anterior(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        repo.update_structure(self.sid, {"name": "Novo Nome"})
        log = repo.get_audit_log(self.sid)
        entry = next(e for e in log if e["action"] == "UPDATE")
        before = json.loads(entry["before_json"])
        self.assertEqual(before["name"], "Original")

    def test_update_log_after_json_contem_nome_novo(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        repo.update_structure(self.sid, {"name": "Nome Novo"})
        log = repo.get_audit_log(self.sid)
        entry = next(e for e in log if e["action"] == "UPDATE")
        after = json.loads(entry["after_json"])
        self.assertEqual(after["name"], "Nome Novo")

    def test_dois_updates_geram_dois_logs(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        repo.update_structure(self.sid, {"name": "V2"})
        repo.update_structure(self.sid, {"name": "V3"})
        log = repo.get_audit_log(self.sid)
        updates = [e for e in log if e["action"] == "UPDATE"]
        self.assertEqual(len(updates), 2)


class TestPatch72LogArchive(unittest.TestCase):
    def setUp(self):
        self.tmp = _make_tmp_db()
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        self.sid = repo.create_structure({
            "name": "Para Arquivar",
            "underlying_asset": "VALE3",
        })

    def tearDown(self):
        os.unlink(self.tmp)

    def test_archive_gera_entrada_archive_no_log(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        repo.archive_structure(self.sid)
        log = repo.get_audit_log(self.sid)
        actions = [e["action"] for e in log]
        self.assertIn("ARCHIVE", actions)

    def test_archive_log_before_status_active(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        repo.archive_structure(self.sid)
        log = repo.get_audit_log(self.sid)
        entry = next(e for e in log if e["action"] == "ARCHIVE")
        before = json.loads(entry["before_json"])
        self.assertEqual(before["status"], "active")

    def test_archive_log_after_status_archived(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        repo.archive_structure(self.sid)
        log = repo.get_audit_log(self.sid)
        entry = next(e for e in log if e["action"] == "ARCHIVE")
        after = json.loads(entry["after_json"])
        self.assertEqual(after["status"], "archived")


class TestPatch72LogLegs(unittest.TestCase):
    def setUp(self):
        self.tmp = _make_tmp_db()
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        self.sid = repo.create_structure({
            "name": "Estrutura com Legs",
            "underlying_asset": "BOVA11",
        })

    def tearDown(self):
        os.unlink(self.tmp)

    def test_add_leg_gera_entrada_add_leg_no_log(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        repo.add_leg(self.sid, _leg_payload(1))
        log = repo.get_audit_log(self.sid)
        actions = [e["action"] for e in log]
        self.assertIn("ADD_LEG", actions)

    def test_replace_legs_gera_entrada_replace_legs_no_log(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        repo.replace_legs(self.sid, [_leg_payload(1), _leg_payload(2)])
        log = repo.get_audit_log(self.sid)
        actions = [e["action"] for e in log]
        self.assertIn("REPLACE_LEGS", actions)

    def test_replace_legs_log_after_contem_legs_count(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        repo.replace_legs(self.sid, [_leg_payload(1), _leg_payload(2)])
        log = repo.get_audit_log(self.sid)
        entry = next(e for e in log if e["action"] == "REPLACE_LEGS")
        after = json.loads(entry["after_json"])
        self.assertEqual(after["legs_count"], 2)


class TestPatch72GetFullAuditLog(unittest.TestCase):
    def setUp(self):
        self.tmp = _make_tmp_db()
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        self.s1 = repo.create_structure({"name": "S1", "underlying_asset": "A1"})
        self.s2 = repo.create_structure({"name": "S2", "underlying_asset": "A2"})
        repo.update_structure(self.s1, {"name": "S1v2"})
        repo.archive_structure(self.s2)

    def tearDown(self):
        os.unlink(self.tmp)

    def test_full_log_retorna_todas_entradas(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        log = repo.get_full_audit_log()
        self.assertGreaterEqual(len(log), 4)

    def test_full_log_filtrado_por_action(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        creates = repo.get_full_audit_log(action="CREATE")
        self.assertTrue(all(e["action"] == "CREATE" for e in creates))

    def test_full_log_limit_respeitado(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        log = repo.get_full_audit_log(limit=2)
        self.assertLessEqual(len(log), 2)


class TestPatch72Atomicidade(unittest.TestCase):
    """Garante que falha na operacao principal nao grava log parcial."""

    def setUp(self):
        self.tmp = _make_tmp_db()

    def tearDown(self):
        os.unlink(self.tmp)

    def test_create_invalido_nao_grava_log(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        with self.assertRaises(ValueError):
            repo.create_structure({"name": "", "underlying_asset": "X"})

        conn = sqlite3.connect(self.tmp)
        count = conn.execute(
            "SELECT COUNT(*) FROM structure_audit_log"
        ).fetchone()[0]
        conn.close()
        self.assertEqual(count, 0)

    def test_update_estrutura_inexistente_nao_grava_log(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp)
        with self.assertRaises(ValueError):
            repo.update_structure(9999, {"name": "Fantasma"})

        conn = sqlite3.connect(self.tmp)
        count = conn.execute(
            "SELECT COUNT(*) FROM structure_audit_log"
        ).fetchone()[0]
        conn.close()
        self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()
