# ATT/tests/test_patch10_smoke.py   VERSÃO CORRIGIDA COMPLETA
"""
Smoke test patch_10 -- corrigido para Windows + path ATT/tests/
Executar: python -m pytest ATT/tests/test_patch10_smoke.py -v
"""
import sys
import os
import gc
import sqlite3
import unittest
import tempfile
import importlib
import importlib.util
from pathlib import Path

#  Path fix: sobe 2 níveis (ATT/tests  ATT  projeto raiz) 
PROJECT_ROOT = Path(__file__).resolve().parents[2]   # < era parents[1], agora parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


#  Helpers Windows-safe 
def _make_tmp_db(schema_sql: str) -> str:
    """Cria DB temporário e retorna o path. Usar _drop_tmp_db() no tearDown."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)                          # fecha o fd do mkstemp imediatamente
    conn = sqlite3.connect(path)
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
    return path


def _drop_tmp_db(path: str):
    """Fecha qualquer conexão pendente via gc e deleta (Windows-safe)."""
    gc.collect()                          # força garbage collection de conexões
    try:
        os.unlink(path)
    except PermissionError:
        pass                              # aceita falha silenciosa no CI/Windows


SCHEMA = """
    CREATE TABLE IF NOT EXISTS structures (
        id                INTEGER PRIMARY KEY AUTOINCREMENT,
        name              TEXT NOT NULL,
        underlying_asset  TEXT NOT NULL,
        alias_legacy_aba  TEXT,
        status            TEXT NOT NULL DEFAULT 'active',
        notes             TEXT,
        created_at        TEXT,
        updated_at        TEXT
    );
    CREATE TABLE IF NOT EXISTS structure_legs (
        id               INTEGER PRIMARY KEY AUTOINCREMENT,
        structure_id     INTEGER NOT NULL REFERENCES structures(id),
        leg_order        INTEGER NOT NULL DEFAULT 1,
        position_side    TEXT NOT NULL,
        option_type      TEXT NOT NULL,
        symbol           TEXT,
        strike           REAL NOT NULL,
        expiration_date  TEXT NOT NULL,
        quantity         INTEGER NOT NULL,
        premium          REAL,
        multiplier       REAL NOT NULL DEFAULT 1,
        notes            TEXT,
        created_at       TEXT,
        updated_at       TEXT
    );
"""


# 
# 1. Imports
# 
class TestImports(unittest.TestCase):

    def test_structures_repository_import(self):
        try:
            from repositories.structures_repository import StructuresRepository
        except ImportError as e:
            self.fail(f"StructuresRepository não importou: {e}")

    def test_structures_list_panel_import(self):
        try:
            from UI.components.structures_list_panel import StructuresListPanel
        except ImportError as e:
            self.fail(f"StructuresListPanel não importou: {e}")

    def test_structure_editor_dialog_import(self):
        try:
            from UI.components.structure_editor_dialog import StructureEditorDialog
        except ImportError as e:
            self.fail(f"StructureEditorDialog não importou: {e}")

    def test_main_window_import(self):
        mw_path = PROJECT_ROOT / "UI" / "main_window.py"
        self.assertTrue(mw_path.exists(),
                        f"main_window.py não encontrado em: {mw_path}")
        try:
            # exec_module executa o corpo do módulo e cria tk.Tk() como side-effect
            # no Windows isso corrompe o _default_root dos testes UI seguintes.
            # Basta validar sintaxe sem executar.
            import ast
            ast.parse(mw_path.read_text(encoding="utf-8"))
        except Exception as e:
            self.fail(f"main_window.py falhou ao importar: {e}")


# 
# 2. StructuresRepository -- CRUD
# 
class TestStructuresRepository(unittest.TestCase):

    def setUp(self):
        from repositories.structures_repository import StructuresRepository
        self._db_path = _make_tmp_db(SCHEMA)
        self._repo    = StructuresRepository(self._db_path)

    def tearDown(self):
        # Garante que o repo fecha a conexão antes de deletar
        if hasattr(self._repo, "close"):
            self._repo.close()
        del self._repo
        _drop_tmp_db(self._db_path)

    #  CREATE 
    def test_create_structure_minimal(self):
        sid = self._repo.create_structure({
            "name": "Trava de Alta",
            "underlying_asset": "PETR4",
        })
        self.assertIsInstance(sid, int)
        self.assertGreater(sid, 0)

    def test_create_structure_completo(self):
        sid = self._repo.create_structure({
            "name": "Borboleta VALE",
            "underlying_asset": "VALE3",
            "alias_legacy_aba": "butterfly_vale",
            "status": "active",
            "notes": "Teste completo",
        })
        data = self._repo.get_structure(sid)
        self.assertEqual(data["name"], "Borboleta VALE")
        self.assertEqual(data["underlying_asset"], "VALE3")
        self.assertEqual(data["alias_legacy_aba"], "butterfly_vale")
        self.assertEqual(data["status"], "active")

    #  READ 
    def test_get_structure_retorna_legs(self):
        sid = self._repo.create_structure({"name": "Spread", "underlying_asset": "IBOV"})
        self._repo.replace_legs(sid, [
            {"position_side": "LONG",  "option_type": "CALL",
             "strike": "120.00", "expiration_date": "2025-12-19",
             "quantity": "10", "leg_order": 1},
            {"position_side": "SHORT", "option_type": "CALL",
             "strike": "130.00", "expiration_date": "2025-12-19",
             "quantity": "10", "leg_order": 2},
        ])
        data = self._repo.get_structure(sid)
        self.assertIn("legs", data)
        self.assertEqual(len(data["legs"]), 2)

    def test_get_structure_inexistente_retorna_none(self):
        result = self._repo.get_structure(99999)
        self.assertIsNone(result)

    def test_list_structures_active(self):
        self._repo.create_structure({"name": "A", "underlying_asset": "X", "status": "active"})
        self._repo.create_structure({"name": "B", "underlying_asset": "X", "status": "archived"})
        result = self._repo.list_structures(include_archived=False)
        names = [r["name"] for r in result]
        self.assertIn("A", names)
        self.assertNotIn("B", names)

    def test_list_structures_with_archived(self):
        self._repo.create_structure({"name": "C", "underlying_asset": "X", "status": "active"})
        self._repo.create_structure({"name": "D", "underlying_asset": "X", "status": "archived"})
        result = self._repo.list_structures(include_archived=True)
        names = [r["name"] for r in result]
        self.assertIn("C", names)
        self.assertIn("D", names)

    #  UPDATE 
    def test_update_structure(self):
        sid = self._repo.create_structure({"name": "Old Name", "underlying_asset": "X"})
        self._repo.update_structure(sid, {"name": "New Name", "underlying_asset": "X"})
        data = self._repo.get_structure(sid)
        self.assertEqual(data["name"], "New Name")

    #  REPLACE LEGS 
    def test_replace_legs_substitui_anteriores(self):
        sid = self._repo.create_structure({"name": "Test", "underlying_asset": "X"})
        self._repo.replace_legs(sid, [
            {"position_side": "LONG", "option_type": "PUT",
             "strike": "50", "expiration_date": "2025-06-20",
             "quantity": "5", "leg_order": 1},
        ])
        self._repo.replace_legs(sid, [
            {"position_side": "LONG",  "option_type": "CALL",
             "strike": "100", "expiration_date": "2025-12-19",
             "quantity": "10", "leg_order": 1},
            {"position_side": "SHORT", "option_type": "CALL",
             "strike": "110", "expiration_date": "2025-12-19",
             "quantity": "10", "leg_order": 2},
        ])
        data = self._repo.get_structure(sid)
        self.assertEqual(len(data["legs"]), 2)
        self.assertNotEqual(data["legs"][0]["option_type"], "PUT")

    def test_replace_legs_vazia_limpa(self):
        """P1a: replace_legs([]) aceita lista vazia e limpa as legs (guard removido)."""
        sid = self._repo.create_structure({"name": "Test2", "underlying_asset": "Y"})
        self._repo.replace_legs(sid, [
            {"position_side": "LONG", "option_type": "CALL",
             "strike": "100", "expiration_date": "2025-12-19",
             "quantity": "5", "leg_order": 1},
        ])
        # P1a: lista vazia deve ser aceita sem ValueError
        self._repo.replace_legs(sid, [])
        # P1b: count_legs confirma que ficou zerado
        n = self._repo.count_legs(sid)
        assert n == 0, f"esperado 0 legs apos replace_legs([]), obtido {n}"

    #  ARCHIVE 
    def test_archive_structure(self):
        sid = self._repo.create_structure({"name": "Para Arquivar", "underlying_asset": "Z"})
        self._repo.archive_structure(sid)
        data = self._repo.get_structure(sid)
        self.assertEqual(data["status"], "archived")

    #  DUPLICATE 
    def test_duplicate_logic(self):
        sid = self._repo.create_structure({
            "name": "Original", "underlying_asset": "PETR4", "status": "active",
        })
        self._repo.replace_legs(sid, [
            {"position_side": "LONG", "option_type": "CALL",
             "strike": "35", "expiration_date": "2025-09-19",
             "quantity": "100", "leg_order": 1},
        ])
        src = self._repo.get_structure(sid)
        new_id = self._repo.create_structure({
            "name": f"{src['name']} (cópia)",
            "underlying_asset": src["underlying_asset"],
            "status": "active",
        })
        legs_copy = [
            {k: v for k, v in leg.items()
             if k not in ("id", "structure_id", "created_at", "updated_at")}
            for leg in src.get("legs", [])
        ]
        self._repo.replace_legs(new_id, legs_copy)
        copy = self._repo.get_structure(new_id)
        self.assertIn("(cópia)", copy["name"])
        self.assertEqual(len(copy["legs"]), 1)
        self.assertEqual(copy["legs"][0]["strike"], src["legs"][0]["strike"])


# 
# 3. Validação de campos obrigatórios
# 
class TestRepositoryValidation(unittest.TestCase):

    def setUp(self):
        from repositories.structures_repository import StructuresRepository
        self._db_path = _make_tmp_db(SCHEMA)
        self._repo    = StructuresRepository(self._db_path)

    def tearDown(self):
        if hasattr(self._repo, "close"):
            self._repo.close()
        del self._repo
        _drop_tmp_db(self._db_path)

    def test_create_sem_name_raise(self):
        with self.assertRaises(Exception):
            self._repo.create_structure({"underlying_asset": "X"})

    def test_create_sem_underlying_raise(self):
        with self.assertRaises(Exception):
            self._repo.create_structure({"name": "Sem ativo"})

    def test_leg_sem_strike_raise(self):
        sid = self._repo.create_structure({"name": "T", "underlying_asset": "X"})
        with self.assertRaises(Exception):
            self._repo.replace_legs(sid, [
                {"position_side": "LONG", "option_type": "CALL",
                 "expiration_date": "2025-12-19", "quantity": "5", "leg_order": 1}
            ])

    def test_leg_side_invalido_raise(self):
        sid = self._repo.create_structure({"name": "T2", "underlying_asset": "X"})
        with self.assertRaises(Exception):
            self._repo.replace_legs(sid, [
                {"position_side": "COMPRADO", "option_type": "CALL",
                 "strike": "100", "expiration_date": "2025-12-19",
                 "quantity": "5", "leg_order": 1}
            ])


# 
if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite  = unittest.TestSuite()
    for cls in [TestImports, TestStructuresRepository, TestRepositoryValidation]:
        suite.addTests(loader.loadTestsFromTestCase(cls))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
