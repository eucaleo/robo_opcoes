# tests/test_patch10_ui_integration.py
"""
Teste de integração UI patch_10.
Requer display (Tk). Roda em ambiente local com tela.
Executar: python ATT/tests/test_patch10_ui_integration.py
"""
import sys
import os
import gc
import time
import sqlite3
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import tkinter as tk
from tkinter import ttk


@unittest.skip("Requer display Tk (headless nao suportado) -- rodar manualmente")
class TestStructuresListPanelUI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Banco temporário em diretório temporário (mais seguro no Windows)
        cls._tmpdir = tempfile.TemporaryDirectory()
        cls._db_path = os.path.join(cls._tmpdir.name, "test.db")

        conn = sqlite3.connect(cls._db_path)
        conn.executescript("""
            CREATE TABLE structures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL, underlying_asset TEXT NOT NULL,
                alias_legacy_aba TEXT, status TEXT NOT NULL DEFAULT 'active',
                notes TEXT, created_at TEXT, updated_at TEXT
            );
            CREATE TABLE structure_legs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                structure_id INTEGER NOT NULL, leg_order INTEGER DEFAULT 1,
                position_side TEXT NOT NULL, option_type TEXT NOT NULL,
                symbol TEXT, strike REAL NOT NULL, expiration_date TEXT NOT NULL,
                quantity INTEGER NOT NULL, premium REAL, multiplier REAL DEFAULT 1,
                notes TEXT, created_at TEXT, updated_at TEXT
            );
        """)
        # Seed
        conn.execute("""
            INSERT INTO structures (name, underlying_asset, status, created_at, updated_at)
            VALUES ('Trava Alta PETR4','PETR4','active',
                    datetime('now'), datetime('now'))
        """)
        conn.execute("""
            INSERT INTO structures (name, underlying_asset, status, created_at, updated_at)
            VALUES ('Borboleta VALE3','VALE3','archived',
                    datetime('now'), datetime('now'))
        """)
        conn.commit()
        conn.close()

        cls._root = tk.Tk()
        cls._root.withdraw()  # janela invisível

    @classmethod
    def tearDownClass(cls):
        cls._root.destroy()

        # Força GC para fechar conexões SQLite pendentes antes do cleanup
        gc.collect()

        # Retry: Windows pode segurar o handle por um tick
        for _ in range(5):
            try:
                cls._tmpdir.cleanup()
                break
            except PermissionError:
                time.sleep(0.3)

    def test_panel_cria_sem_erro(self):
        from UI.components.structures_list_panel import StructuresListPanel
        panel = StructuresListPanel(
            self._root,
            on_structure_selected=lambda s: None,
            on_request_edit=lambda i: None,
            db_path=self._db_path,
        )
        self.assertIsNotNone(panel)
        panel.destroy()

    def test_panel_carrega_dados_active(self):
        from UI.components.structures_list_panel import StructuresListPanel

        selected = []
        panel = StructuresListPanel(
            self._root,
            on_structure_selected=lambda s: selected.append(s),
            on_request_edit=lambda i: None,
            db_path=self._db_path,
        )
        # Verifica que a tree tem pelo menos 1 item (status=active)
        items = panel._tree.get_children()
        self.assertGreaterEqual(len(items), 1)

        # Verifica que item arquivado NÃO aparece com filtro default
        values_list = [panel._tree.item(i)["values"] for i in items]
        statuses = [v[4] for v in values_list]  # coluna status
        self.assertNotIn("archived", statuses)

        panel.destroy()

    def test_panel_filtro_all_mostra_archived(self):
        from UI.components.structures_list_panel import StructuresListPanel

        panel = StructuresListPanel(
            self._root,
            on_structure_selected=lambda s: None,
            on_request_edit=lambda i: None,
            db_path=self._db_path,
        )
        panel._status_var.set("all")
        panel.load()

        items = panel._tree.get_children()
        values_list = [panel._tree.item(i)["values"] for i in items]
        statuses = [v[4] for v in values_list]
        self.assertIn("archived", statuses)

        panel.destroy()

    def test_editor_dialog_abre_sem_erro(self):
        from UI.components.structure_editor_dialog import StructureEditorDialog
        dlg = StructureEditorDialog(
            self._root,
            structure_id=None,
            db_path=self._db_path,
        )
        self.assertFalse(dlg.saved)
        dlg.destroy()

    def test_editor_dialog_carrega_existente(self):
        from UI.components.structure_editor_dialog import StructureEditorDialog

        # Pega ID 1 do seed
        dlg = StructureEditorDialog(
            self._root,
            structure_id=1,
            db_path=self._db_path,
        )
        # Nome deve ter sido carregado
        self.assertEqual(dlg._f_name.get(), "Trava Alta PETR4")
        self.assertEqual(dlg._f_underlying.get(), "PETR4")
        dlg.destroy()

    def test_editor_salva_nova_estrutura(self):
        from UI.components.structure_editor_dialog import StructureEditorDialog
        from repositories.structures_repository import StructuresRepository

        dlg = StructureEditorDialog(
            self._root,
            structure_id=None,
            db_path=self._db_path,
        )
        dlg._f_name.set("Condor Teste")
        dlg._f_underlying.set("IBOV")
        dlg._cmd_save()

        self.assertTrue(dlg.saved)

        repo = StructuresRepository(self._db_path)
        rows = repo.list_structures(include_archived=True)
        names = [r["name"] for r in rows]
        self.assertIn("Condor Teste", names)


if __name__ == "__main__":
    unittest.main(verbosity=2)
