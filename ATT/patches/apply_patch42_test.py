# apply_patch42_test.py
"""
patch_42 — cria ATT/tests/test_patch42.py
"""

from pathlib import Path

TEST_FILE = Path("ATT/tests/test_patch42.py")

CONTENT = '''\
# ATT/tests/test_patch42.py
# Testes formais do patch_42
# get_structure_by_alias e get_structure_id_by_alias no StructuresRepository

import os
import sys
import sqlite3
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

REPO_FILE = os.path.join(ROOT, "repositories", "structures_repository.py")


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _make_tmp_db() -> str:
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
            status           TEXT    NOT NULL DEFAULT \'active\',
            notes            TEXT,
            created_at       TEXT    NOT NULL,
            updated_at       TEXT    NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS structure_legs (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            structure_id     INTEGER NOT NULL,
            position_side    TEXT    NOT NULL,
            option_type      TEXT    NOT NULL,
            symbol           TEXT,
            strike           REAL    NOT NULL,
            expiration_date  TEXT    NOT NULL,
            quantity         INTEGER NOT NULL,
            premium          REAL,
            multiplier       REAL    NOT NULL DEFAULT 1,
            leg_order        INTEGER NOT NULL,
            notes            TEXT,
            created_at       TEXT    NOT NULL,
            updated_at       TEXT    NOT NULL,
            FOREIGN KEY (structure_id) REFERENCES structures(id) ON DELETE CASCADE
        )
        """
    )
    conn.commit()
    conn.close()
    return tmp_path


class TestPatch42RepoFileExists(unittest.TestCase):
    """Check 1 — arquivo existe"""

    def test_repo_file_existe(self):
        self.assertTrue(
            os.path.isfile(REPO_FILE),
            "repositories/structures_repository.py nao encontrado",
        )


class TestPatch42MetodosPresentes(unittest.TestCase):
    """Checks 2 e 3 — metodos adicionados"""

    @classmethod
    def setUpClass(cls):
        cls.src = _read(REPO_FILE)

    def test_get_structure_by_alias_presente(self):
        self.assertIn(
            "def get_structure_by_alias",
            self.src,
            "get_structure_by_alias nao encontrado em structures_repository.py",
        )

    def test_get_structure_id_by_alias_presente(self):
        self.assertIn(
            "def get_structure_id_by_alias",
            self.src,
            "get_structure_id_by_alias nao encontrado em structures_repository.py",
        )


class TestPatch42SemAbaComoChave(unittest.TestCase):
    """Check 4 — lookup usa alias_legacy_aba, nao aba diretamente"""

    @classmethod
    def setUpClass(cls):
        cls.src = _read(REPO_FILE)

    def test_usa_alias_legacy_aba_no_where(self):
        self.assertIn(
            "alias_legacy_aba = ?",
            self.src,
            "WHERE alias_legacy_aba = ? nao encontrado — verificar implementacao",
        )


class TestPatch42PatchNotaNoHeader(unittest.TestCase):
    """Check 5 — PATCH_42 registrado no header do arquivo"""

    @classmethod
    def setUpClass(cls):
        cls.src = _read(REPO_FILE)

    def test_patch42_no_header(self):
        self.assertIn(
            "PATCH_42",
            self.src,
            "PATCH_42 nao registrado no header de structures_repository.py",
        )


class TestPatch42FuncionalAliasInexistente(unittest.TestCase):
    """Check 6 — alias inexistente retorna None sem lancar excecao"""

    def setUp(self):
        self.tmp_path = _make_tmp_db()

    def tearDown(self):
        os.unlink(self.tmp_path)

    def test_alias_inexistente_retorna_none(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp_path)
        result = repo.get_structure_by_alias("ALIAS_INEXISTENTE")
        self.assertIsNone(result)

    def test_id_alias_inexistente_retorna_none(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp_path)
        result = repo.get_structure_id_by_alias("ALIAS_INEXISTENTE")
        self.assertIsNone(result)


class TestPatch42FuncionalAliasVazio(unittest.TestCase):
    """Check 7 — alias vazio/None retorna None sem bater no banco"""

    def setUp(self):
        self.tmp_path = _make_tmp_db()

    def tearDown(self):
        os.unlink(self.tmp_path)

    def test_alias_string_vazia(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp_path)
        self.assertIsNone(repo.get_structure_by_alias(""))

    def test_alias_espacos(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp_path)
        self.assertIsNone(repo.get_structure_by_alias("   "))

    def test_alias_none(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp_path)
        self.assertIsNone(repo.get_structure_by_alias(None))


class TestPatch42FuncionalAliasEncontrado(unittest.TestCase):
    """Check 8 — alias existente retorna estrutura correta"""

    def setUp(self):
        self.tmp_path = _make_tmp_db()
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp_path)
        self.structure_id = repo.create_structure({
            "name": "Trava de Alta",
            "underlying_asset": "PETR4",
            "alias_legacy_aba": "PETR4_TRAVA",
            "status": "active",
        })

    def tearDown(self):
        os.unlink(self.tmp_path)

    def test_get_structure_by_alias_retorna_dict(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp_path)
        result = repo.get_structure_by_alias("PETR4_TRAVA")
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], self.structure_id)
        self.assertEqual(result["alias_legacy_aba"], "PETR4_TRAVA")
        self.assertIn("legs", result)

    def test_get_structure_id_by_alias_retorna_int(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp_path)
        result = repo.get_structure_id_by_alias("PETR4_TRAVA")
        self.assertIsNotNone(result)
        self.assertEqual(result, self.structure_id)
        self.assertIsInstance(result, int)


class TestPatch42ArchivedNaoRetornado(unittest.TestCase):
    """Check 9 — estrutura archived nao retornada por get_structure_by_alias"""

    def setUp(self):
        self.tmp_path = _make_tmp_db()
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp_path)
        sid = repo.create_structure({
            "name": "Estrutura Arquivada",
            "underlying_asset": "VALE3",
            "alias_legacy_aba": "VALE3_OLD",
            "status": "active",
        })
        repo.archive_structure(sid)

    def tearDown(self):
        os.unlink(self.tmp_path)

    def test_archived_nao_retornado(self):
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(db_path=self.tmp_path)
        result = repo.get_structure_by_alias("VALE3_OLD")
        self.assertIsNone(
            result,
            "get_structure_by_alias nao deve retornar estrutura com status=archived",
        )


if __name__ == "__main__":
    unittest.main()
'''


def main():
    TEST_FILE.parent.mkdir(parents=True, exist_ok=True)

    if TEST_FILE.exists():
        print(f"[AVISO] {TEST_FILE} ja existe — sobrescrevendo")

    TEST_FILE.write_text(CONTENT, encoding="utf-8")
    print(f"[OK] {TEST_FILE} criado com 9 checks do patch_42")


if __name__ == "__main__":
    main()
