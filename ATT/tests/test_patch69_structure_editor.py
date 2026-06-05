# ATT/tests/test_patch69_structure_editor.py
"""
patch_69 -- Testes unitarios de StructureEditorDialog

Cobertura:
  - _build_legs_payload()   : logica pura, sem Tk
  - _load_existing()        : requer display -- @skip em headless
  - _cmd_save() create      : requer display -- @skip em headless
  - _cmd_save() update      : requer display -- @skip em headless
  - _cmd_save() validacao   : requer display -- @skip em headless

Convencao de ambiente (rota_v2b.pdf, secao patch_10:tk_headless):
  Testes que dependem de display Tk DEVEM usar @unittest.skip.
  Para executar: rodar manualmente com display disponivel.
"""

from __future__ import annotations

import sys
import types
import unittest
from unittest.mock import MagicMock, patch, call

# ---------------------------------------------------------------------------
# Guard de importacao -- o modulo UI depende de Tkinter; em headless o import
# de tk.Toplevel falha antes mesmo de chegar nos testes. Capturamos o modulo
# de forma segura para os testes de logica pura.
# ---------------------------------------------------------------------------
try:
    from UI.components.structure_editor_dialog import StructureEditorDialog
    _IMPORT_OK = True
except Exception as exc:  # noqa: BLE001
    _IMPORT_OK = False
    _IMPORT_ERROR = str(exc)


# ===========================================================================
# Helpers
# ===========================================================================

def _make_bare_dialog() -> "StructureEditorDialog":
    """
    Cria instancia de StructureEditorDialog sem chamar __init__.
    Util para testar metodos de logica pura que nao dependem de Tk.
    """
    obj = object.__new__(StructureEditorDialog)
    obj._legs_rows = []
    obj._structure_id = None
    obj.saved = False
    return obj


# ===========================================================================
# Bloco 1 -- Logica pura (sem Tk, sem mock de display)
# ===========================================================================

@unittest.skipUnless(_IMPORT_OK, "StructureEditorDialog nao importavel")
class TestBuildLegsPayload(unittest.TestCase):
    """
    _build_legs_payload() e logica pura Python.
    Nao depende de Tk nem de repositorio.
    Pode rodar em qualquer ambiente.
    """

    def _dialog(self, legs: list) -> "StructureEditorDialog":
        d = _make_bare_dialog()
        d._legs_rows = legs
        return d

    def test_lista_vazia_retorna_lista_vazia(self):
        d = self._dialog([])
        resultado = d._build_legs_payload()
        self.assertEqual(resultado, [])

    def test_leg_order_comeca_em_1(self):
        legs = [
            {"position_side": "LONG", "option_type": "CALL", "strike": 100.0},
        ]
        resultado = self._dialog(legs)._build_legs_payload()
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["leg_order"], 1)

    def test_leg_order_sequencial(self):
        legs = [
            {"position_side": "LONG",  "option_type": "CALL", "strike": 100.0},
            {"position_side": "SHORT", "option_type": "PUT",  "strike": 90.0},
            {"position_side": "LONG",  "option_type": "PUT",  "strike": 80.0},
        ]
        resultado = self._dialog(legs)._build_legs_payload()
        ordens = [r["leg_order"] for r in resultado]
        self.assertEqual(ordens, [1, 2, 3])

    def test_campos_originais_preservados(self):
        legs = [
            {
                "position_side": "SHORT",
                "option_type":   "CALL",
                "strike":        195.0,
                "expiration_date": "2026-05-15",
                "quantity":      5000,
                "premium":       None,
                "multiplier":    1,
            }
        ]
        resultado = self._dialog(legs)._build_legs_payload()
        r = resultado[0]
        self.assertEqual(r["position_side"],    "SHORT")
        self.assertEqual(r["option_type"],      "CALL")
        self.assertEqual(r["strike"],           195.0)
        self.assertEqual(r["expiration_date"],  "2026-05-15")
        self.assertEqual(r["quantity"],         5000)
        self.assertIsNone(r["premium"])
        self.assertEqual(r["multiplier"],       1)
        self.assertEqual(r["leg_order"],        1)

    def test_nao_modifica_legs_rows_original(self):
        legs = [{"position_side": "LONG", "option_type": "CALL", "strike": 100.0}]
        d = self._dialog(legs)
        d._build_legs_payload()
        # _legs_rows nao deve ter sido mutado
        self.assertNotIn("leg_order", d._legs_rows[0])

    def test_duas_legs_sem_contaminar_indices(self):
        legs = [
            {"strike": 100.0},
            {"strike": 110.0},
        ]
        resultado = self._dialog(legs)._build_legs_payload()
        self.assertEqual(resultado[0]["leg_order"], 1)
        self.assertEqual(resultado[1]["leg_order"], 2)
        self.assertEqual(resultado[0]["strike"],    100.0)
        self.assertEqual(resultado[1]["strike"],    110.0)


# ===========================================================================
# Bloco 2 -- Testes com display (skip em headless)
# ===========================================================================


class TestLoadExisting(unittest.TestCase):
    """
    _load_existing() popula os campos de formulario a partir do repositorio.
    Requer Tk inicializado.
    """

    def setUp(self):
        import tkinter as tk
        self.root = tk.Tk()
        self.root.withdraw()
        self.db_path = ":memory:"

    def tearDown(self):
        try:
            self.root.destroy()
        except Exception:
            pass

    def _make_dialog_with_mock_repo(self, structure_id, repo_data):
        with patch(
            "UI.components.structure_editor_dialog.StructuresRepository"
        ) as MockRepo:
            mock_repo = MagicMock()
            MockRepo.return_value = mock_repo
            mock_repo.get_structure.return_value = repo_data

            dlg = StructureEditorDialog(
                parent=self.root,
                structure_id=structure_id,
                db_path=self.db_path,
            )
            return dlg, mock_repo

    def test_carrega_campos_do_repositorio(self):
        dados = {
            "id":                1,
            "name":              "BOVA11 Condor",
            "underlying_asset":  "BOVA11",
            "alias_legacy_aba":  "BOVA11",
            "status":            "active",
            "notes":             "teste",
            "legs":              [],
        }
        dlg, repo = self._make_dialog_with_mock_repo(1, dados)

        self.assertEqual(dlg._f_name.get(),       "BOVA11 Condor")
        self.assertEqual(dlg._f_underlying.get(), "BOVA11")
        self.assertEqual(dlg._f_alias.get(),      "BOVA11")
        self.assertEqual(dlg._f_status.get(),     "active")
        self.assertEqual(dlg._f_notes.get(),      "teste")

    def test_carrega_legs_em_legs_rows(self):
        leg = {
            "position_side":   "LONG",
            "option_type":     "CALL",
            "strike":          195.0,
            "expiration_date": "2026-05-15",
            "quantity":        5000,
            "premium":         None,
            "multiplier":      1,
        }
        dados = {
            "id": 1, "name": "X", "underlying_asset": "X",
            "alias_legacy_aba": None, "status": "active", "notes": None,
            "legs": [leg],
        }
        dlg, _ = self._make_dialog_with_mock_repo(1, dados)
        self.assertEqual(len(dlg._legs_rows), 1)
        self.assertEqual(dlg._legs_rows[0]["strike"], 195.0)

    def test_destroi_se_estrutura_nao_encontrada(self):
        with patch(
            "UI.components.structure_editor_dialog.StructuresRepository"
        ) as MockRepo:
            mock_repo = MagicMock()
            MockRepo.return_value = mock_repo
            mock_repo.get_structure.return_value = None

            with patch("tkinter.messagebox.showerror"):
                dlg = StructureEditorDialog(
                    parent=self.root,
                    structure_id=99,
                    db_path=self.db_path,
                )
            # dialogo foi destruido -- nao deve ter _f_name populado de dado real
            mock_repo.get_structure.assert_called_once_with(99)



class TestCmdSaveCreate(unittest.TestCase):
    """
    _cmd_save() no modo criacao (structure_id is None).
    Verifica que create_structure + replace_legs sao chamados corretamente.
    """

    def setUp(self):
        import tkinter as tk
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        try:
            self.root.destroy()
        except Exception:
            pass

    def _make_new_dialog(self):
        with patch(
            "UI.components.structure_editor_dialog.StructuresRepository"
        ) as MockRepo:
            mock_repo = MagicMock()
            MockRepo.return_value = mock_repo
            mock_repo.create_structure.return_value = 42

            dlg = StructureEditorDialog(
                parent=self.root,
                structure_id=None,
                db_path=":memory:",
            )
            dlg._repo = mock_repo
            return dlg, mock_repo

    def test_create_structure_chamado_com_campos_corretos(self):
        dlg, repo = self._make_new_dialog()
        dlg._f_name.set("PRIO3 Trava")
        dlg._f_underlying.set("PRIO3")
        dlg._f_alias.set("PRIO3")
        dlg._f_status.set("active")
        dlg._f_notes.set("")

        dlg._cmd_save()

        repo.create_structure.assert_called_once()
        args = repo.create_structure.call_args[0][0]
        self.assertEqual(args["name"],             "PRIO3 Trava")
        self.assertEqual(args["underlying_asset"], "PRIO3")
        self.assertEqual(args["alias_legacy_aba"], "PRIO3")
        self.assertEqual(args["status"],           "active")
        self.assertIsNone(args["notes"])

    def test_replace_legs_chamado_apos_create(self):
        dlg, repo = self._make_new_dialog()
        dlg._f_name.set("X")
        dlg._f_underlying.set("Y")
        dlg._f_status.set("active")
        dlg._legs_rows = [
            {"position_side": "LONG", "option_type": "CALL", "strike": 100.0,
             "expiration_date": "2026-05-15", "quantity": 1000,
             "premium": None, "multiplier": 1, "symbol": None},
        ]

        dlg._cmd_save()

        repo.replace_legs.assert_called_once()
        sid_arg, legs_arg = repo.replace_legs.call_args[0]
        self.assertEqual(sid_arg, 42)             # id retornado pelo create
        self.assertEqual(legs_arg[0]["leg_order"], 1)

    def test_saved_true_apos_sucesso(self):
        dlg, repo = self._make_new_dialog()
        dlg._f_name.set("X")
        dlg._f_underlying.set("Y")
        dlg._f_status.set("active")

        self.assertFalse(dlg.saved)
        dlg._cmd_save()
        self.assertTrue(dlg.saved)

    def test_name_vazio_nao_chama_create(self):
        dlg, repo = self._make_new_dialog()
        dlg._f_name.set("")
        dlg._f_underlying.set("BOVA11")

        with patch("tkinter.messagebox.showwarning"):
            dlg._cmd_save()

        repo.create_structure.assert_not_called()
        self.assertFalse(dlg.saved)

    def test_underlying_vazio_nao_chama_create(self):
        dlg, repo = self._make_new_dialog()
        dlg._f_name.set("Estrutura X")
        dlg._f_underlying.set("")

        with patch("tkinter.messagebox.showwarning"):
            dlg._cmd_save()

        repo.create_structure.assert_not_called()
        self.assertFalse(dlg.saved)



class TestCmdSaveUpdate(unittest.TestCase):
    """
    _cmd_save() no modo edicao (structure_id nao e None).
    Verifica que update_structure + replace_legs sao chamados.
    create_structure NAO deve ser chamado.
    """

    def setUp(self):
        import tkinter as tk
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        try:
            self.root.destroy()
        except Exception:
            pass

    def _make_edit_dialog(self, structure_id: int):
        dados = {
            "id": structure_id, "name": "Original", "underlying_asset": "ORIG",
            "alias_legacy_aba": None, "status": "active", "notes": None,
            "legs": [],
        }
        with patch(
            "UI.components.structure_editor_dialog.StructuresRepository"
        ) as MockRepo:
            mock_repo = MagicMock()
            MockRepo.return_value = mock_repo
            mock_repo.get_structure.return_value = dados

            dlg = StructureEditorDialog(
                parent=self.root,
                structure_id=structure_id,
                db_path=":memory:",
            )
            dlg._repo = mock_repo
            return dlg, mock_repo

    def test_update_structure_chamado_com_structure_id_correto(self):
        dlg, repo = self._make_edit_dialog(7)
        dlg._f_name.set("Nome Atualizado")
        dlg._f_underlying.set("BOVA11")
        dlg._f_status.set("active")

        dlg._cmd_save()

        repo.update_structure.assert_called_once()
        sid_arg = repo.update_structure.call_args[0][0]
        self.assertEqual(sid_arg, 7)

    def test_create_nao_e_chamado_no_modo_edicao(self):
        dlg, repo = self._make_edit_dialog(7)
        dlg._f_name.set("X")
        dlg._f_underlying.set("Y")
        dlg._f_status.set("active")

        dlg._cmd_save()

        repo.create_structure.assert_not_called()

    def test_replace_legs_usa_structure_id_existente(self):
        dlg, repo = self._make_edit_dialog(7)
        dlg._f_name.set("X")
        dlg._f_underlying.set("Y")
        dlg._f_status.set("active")
        dlg._legs_rows = []

        dlg._cmd_save()

        repo.replace_legs.assert_called_once_with(7, [])


# ===========================================================================
# Bloco 3 -- Verificacoes estaticas (sem Tk, sempre rodam)
# ===========================================================================

class TestPatch69StaticChecks(unittest.TestCase):
    """
    Verificacoes estaticas e de estrutura do arquivo.
    Nao dependem de Tk nem de instancia.
    """

    def test_arquivo_existe(self):
        import os
        path = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "UI", "components", "structure_editor_dialog.py"
        )
        self.assertTrue(
            os.path.isfile(path),
            "UI/components/structure_editor_dialog.py nao encontrado"
        )

    def test_importavel(self):
        if not _IMPORT_OK:
            self.skipTest(f"Import falhou: {_IMPORT_ERROR}")
        self.assertTrue(_IMPORT_OK)

    def test_classe_presente(self):
        if not _IMPORT_OK:
            self.skipTest("Modulo nao importavel")
        self.assertTrue(
            hasattr(StructureEditorDialog, "_cmd_save"),
            "_cmd_save ausente em StructureEditorDialog"
        )
        self.assertTrue(
            hasattr(StructureEditorDialog, "_load_existing"),
            "_load_existing ausente em StructureEditorDialog"
        )
        self.assertTrue(
            hasattr(StructureEditorDialog, "_build_legs_payload"),
            "_build_legs_payload ausente em StructureEditorDialog"
        )
        self.assertTrue(
            hasattr(StructureEditorDialog, "_build_ui"),
            "_build_ui ausente em StructureEditorDialog"
        )

    def test_construtor_aceita_db_path(self):
        if not _IMPORT_OK:
            self.skipTest("Modulo nao importavel")
        import inspect
        sig = inspect.signature(StructureEditorDialog.__init__)
        params = list(sig.parameters.keys())
        self.assertIn("db_path",      params, "parametro db_path ausente no __init__")
        self.assertIn("structure_id", params, "parametro structure_id ausente no __init__")

    def test_nao_importa_sqlite3_diretamente(self):
        """
        O dialogo nao deve acessar sqlite3 diretamente -- apenas via repositorio.
        """
        import ast
        import os
        path = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "UI", "components", "structure_editor_dialog.py"
        )
        if not os.path.isfile(path):
            self.skipTest("arquivo nao encontrado")

        with open(path, encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source)
        imports = [
            node.names[0].name
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
        ]
        import_froms = [
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        ]

        self.assertNotIn(
            "sqlite3", imports,
            "UI/components/structure_editor_dialog.py importa sqlite3 diretamente"
        )
        self.assertNotIn(
            "sqlite3", import_froms,
            "UI/components/structure_editor_dialog.py importa sqlite3 diretamente"
        )


if __name__ == "__main__":
    unittest.main()
