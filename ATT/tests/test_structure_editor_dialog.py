# Testes do dialogo de edicao de estruturas
"""
Testes unitarios de StructureEditorDialog

Estrategia: injecao direta de _repo via parametro de construtor.
Nao depende de patch de namespace, funciona independentemente
de como o dialog importa StructuresRepository.
"""
from __future__ import annotations

import inspect
import os
import unittest
from unittest.mock import MagicMock, patch


# ---------------------------------------------------------------------------
# Guard de importacao
# ---------------------------------------------------------------------------
try:
    from UI.components.structure_editor_dialog import StructureEditorDialog
    _IMPORT_OK = True
    _IMPORT_ERROR = ""
except Exception as exc:
    _IMPORT_OK = False
    _IMPORT_ERROR = str(exc)


# ---------------------------------------------------------------------------
# Helpers Tk
# ---------------------------------------------------------------------------
_TK_MODAL_METHODS = ["transient", "grab_set", "wait_window", "focus_set"]


def _start_tk_patches() -> list:
    """
    Mocka metodos modais herdados de tk.Toplevel.
    create=True necessario pois nao estao no __dict__ da subclasse.
    """
    patchers = []
    for name in _TK_MODAL_METHODS:
        p = patch.object(StructureEditorDialog, name, lambda *a, **kw: None, create=True)
        p.start()
        patchers.append(p)
    return patchers


def _stop_patches(patchers: list) -> None:
    for p in patchers:
        try:
            p.stop()
        except RuntimeError:
            pass


def _make_bare_dialog() -> "StructureEditorDialog":
    """Cria instancia sem __init__ para testes de logica pura."""
    obj = object.__new__(StructureEditorDialog)
    obj._legs_rows = []
    obj._structure_id = None
    obj.saved = False
    return obj


def _make_mock_repo(get_return=None, create_return=42) -> MagicMock:
    repo = MagicMock()
    repo.get_structure.return_value = get_return
    repo.create_structure.return_value = create_return
    return repo


# ===========================================================================
# Bloco 1 -- Logica pura (sem Tk, sem repositorio)
# ===========================================================================

@unittest.skipUnless(_IMPORT_OK, "StructureEditorDialog nao importavel")
class TestBuildLegsPayload(unittest.TestCase):

    def _dialog(self, legs):
        d = _make_bare_dialog()
        d._legs_rows = legs
        return d

    def test_lista_vazia_retorna_lista_vazia(self):
        self.assertEqual(self._dialog([])._build_legs_payload(), [])

    def test_leg_order_comeca_em_1(self):
        r = self._dialog([{"strike": 100.0}])._build_legs_payload()
        self.assertEqual(r[0]["leg_order"], 1)

    def test_leg_order_sequencial(self):
        legs = [{"strike": 100.0}, {"strike": 110.0}, {"strike": 90.0}]
        ordens = [r["leg_order"] for r in self._dialog(legs)._build_legs_payload()]
        self.assertEqual(ordens, [1, 2, 3])

    def test_campos_originais_preservados(self):
        legs = [{
            "position_side": "VENDIDO", "option_type": "CALL", "strike": 195.0,
            "expiration_date": "2026-05-15", "quantity": 5000,
            "premium": None, "multiplier": 1,
        }]
        r = self._dialog(legs)._build_legs_payload()[0]
        self.assertEqual(r["position_side"], "VENDIDO")
        self.assertEqual(r["strike"], 195.0)
        self.assertEqual(r["leg_order"], 1)

    def test_nao_modifica_legs_rows_original(self):
        legs = [{"strike": 100.0}]
        d = self._dialog(legs)
        d._build_legs_payload()
        self.assertNotIn("leg_order", d._legs_rows[0])

    def test_duas_legs_sem_contaminar_indices(self):
        legs = [{"strike": 100.0}, {"strike": 110.0}]
        r = self._dialog(legs)._build_legs_payload()
        self.assertEqual(r[0]["leg_order"], 1)
        self.assertEqual(r[1]["leg_order"], 2)
        self.assertEqual(r[0]["strike"], 100.0)
        self.assertEqual(r[1]["strike"], 110.0)


# ===========================================================================
# Bloco 2 -- TestLoadExisting  (injecao direta de _repo)
# ===========================================================================

@unittest.skipUnless(_IMPORT_OK, "StructureEditorDialog nao importavel")
class TestLoadExisting(unittest.TestCase):

    def setUp(self):
        import tkinter as Tk
        self.root = Tk.Tk()
        self.root.withdraw()
        self._tk_patchers = _start_tk_patches()

    def tearDown(self):
        _stop_patches(self._tk_patchers)
        try:
            self.root.destroy()
        except Exception:
            pass

    def _make_dialog(self, structure_id, repo_data):
        mock_repo = _make_mock_repo(get_return=repo_data)
        return StructureEditorDialog(
            parent=self.root,
            structure_id=structure_id,
            db_path=":memory:",
            _repo=mock_repo,        # <-- injecao direta
        ), mock_repo

    def test_carrega_campos_do_repositorio(self):
        dados = {
            "id": 1, "name": "BOVA11 Condor", "underlying_asset": "BOVA11",
            "alias_legacy_aba": "BOVA11", "status": "active",
            "notes": "teste", "legs": [],
        }
        dlg, _ = self._make_dialog(1, dados)
        self.assertEqual(dlg._f_name.get(),       "BOVA11 Condor")
        self.assertEqual(dlg._f_underlying.get(), "BOVA11")
        self.assertEqual(dlg._f_alias.get(),      "BOVA11")
        self.assertEqual(dlg._f_status.get(),     "active")
        self.assertEqual(dlg._f_notes.get(),      "teste")

    def test_carrega_legs_em_legs_rows(self):
        leg = {
            "position_side": "COMPRADO", "option_type": "CALL", "strike": 195.0,
            "expiration_date": "2026-05-15", "quantity": 5000,
            "premium": None, "multiplier": 1,
        }
        dados = {
            "id": 1, "name": "X", "underlying_asset": "X",
            "alias_legacy_aba": None, "status": "active", "notes": None,
            "legs": [leg],
        }
        dlg, _ = self._make_dialog(1, dados)
        self.assertEqual(len(dlg._legs_rows), 1)
        self.assertEqual(dlg._legs_rows[0]["strike"], 195.0)

    def test_destroi_se_estrutura_nao_encontrada(self):
        mock_repo = _make_mock_repo(get_return=None)
        with patch("tkinter.messagebox.showerror"):
            StructureEditorDialog(
                parent=self.root,
                structure_id=99,
                db_path=":memory:",
                _repo=mock_repo,
            )
        mock_repo.get_structure.assert_called_once_with(99)


# ===========================================================================
# Bloco 3 -- TestCmdSaveCreate
# ===========================================================================

@unittest.skipUnless(_IMPORT_OK, "StructureEditorDialog nao importavel")
class TestCmdSaveCreate(unittest.TestCase):

    def setUp(self):
        import tkinter as tk
        self.root = tk.Tk()
        self.root.withdraw()
        self._tk_patchers = _start_tk_patches()
        self.mock_repo = _make_mock_repo(get_return=None, create_return=42)

    def tearDown(self):
        _stop_patches(self._tk_patchers)
        try:
            self.root.destroy()
        except Exception:
            pass

    def _make_dialog(self):
        """Modo criacao: structure_id=None."""
        return StructureEditorDialog(
            parent=self.root,
            structure_id=None,
            db_path=":memory:",
            _repo=self.mock_repo,   # <-- injecao direta
        )


    def test_create_structure_chamado_com_campos_corretos(self):
        dlg = self._make_dialog()
        dlg._f_name.set("PRIO3 Trava")
        dlg._f_underlying.set("PRIO3")
        dlg._f_alias.set("PRIO3")
        dlg._f_status.set("active")
        dlg._f_notes.set("")

        dlg._cmd_save()

        self.mock_repo.create_structure_with_legs.assert_called_once()
        args, _kwargs = self.mock_repo.create_structure_with_legs.call_args

        structure_arg = args[0]

        self.assertEqual(structure_arg["name"], "PRIO3 Trava")
        self.assertEqual(structure_arg["underlying_asset"], "PRIO3")
        self.assertEqual(structure_arg["alias_legacy_aba"], "PRIO3")
        self.assertEqual(structure_arg["status"], "active")
        self.assertIsNone(structure_arg["notes"])


    def test_replace_legs_chamado_apos_create(self):
        dlg = self._make_dialog()
        dlg._f_name.set("X")
        dlg._f_underlying.set("Y")
        dlg._f_status.set("active")
        dlg._legs_rows = [{
            "position_side": "COMPRADO", "option_type": "CALL", "strike": 100.0,
            "expiration_date": "2026-05-15", "quantity": 1000,
            "premium": None, "multiplier": 1, "symbol": None,
        }]

        dlg._cmd_save()

        self.mock_repo.create_structure_with_legs.assert_called_once()
        args, _kwargs = self.mock_repo.create_structure_with_legs.call_args

        structure_arg = args[0]
        legs_arg = args[1]

        self.assertEqual(structure_arg["name"], "X")
        self.assertEqual(structure_arg["underlying_asset"], "Y")
        self.assertEqual(len(legs_arg), 1)
        self.assertEqual(legs_arg[0]["position_side"], "COMPRADO")
        self.assertEqual(legs_arg[0]["option_type"], "CALL")
        self.assertEqual(legs_arg[0]["strike"], 100.0)

    def test_saved_true_apos_sucesso(self):
        dlg = self._make_dialog()
        dlg._f_name.set("X")
        dlg._f_underlying.set("Y")
        dlg._f_status.set("active")
        self.assertFalse(dlg.saved)
        dlg._cmd_save()
        self.assertTrue(dlg.saved)

    def test_name_vazio_nao_chama_create(self):
        dlg = self._make_dialog()
        dlg._f_name.set("")
        dlg._f_underlying.set("BOVA11")
        with patch("tkinter.messagebox.showwarning"):
            dlg._cmd_save()
        self.mock_repo.create_structure.assert_not_called()
        self.assertFalse(dlg.saved)

    def test_underlying_vazio_nao_chama_create(self):
        dlg = self._make_dialog()
        dlg._f_name.set("Estrutura X")
        dlg._f_underlying.set("")
        with patch("tkinter.messagebox.showwarning"):
            dlg._cmd_save()
        self.mock_repo.create_structure.assert_not_called()
        self.assertFalse(dlg.saved)


# ===========================================================================
# Bloco 4 -- TestCmdSaveUpdate
# ===========================================================================

@unittest.skipUnless(_IMPORT_OK, "StructureEditorDialog nao importavel")
class TestCmdSaveUpdate(unittest.TestCase):

    def setUp(self):
        import tkinter as tk
        self.root = tk.Tk()
        self.root.withdraw()
        self._tk_patchers = _start_tk_patches()
        self.mock_repo = _make_mock_repo()

    def tearDown(self):
        _stop_patches(self._tk_patchers)
        try:
            self.root.destroy()
        except Exception:
            pass

    def _make_edit_dialog(self, structure_id: int):
        """Modo edicao: repo retorna dados validos."""
        self.mock_repo.get_structure.return_value = {
            "id": structure_id, "name": "Original", "underlying_asset": "ORIG",
            "alias_legacy_aba": None, "status": "active", "notes": None,
            "legs": [],
        }
        return StructureEditorDialog(
            parent=self.root,
            structure_id=structure_id,
            db_path=":memory:",
            _repo=self.mock_repo,   # <-- injecao direta
        )

    def test_update_structure_chamado_com_structure_id_correto(self):
        dlg = self._make_edit_dialog(7)
        dlg._f_name.set("Nome Atualizado")
        dlg._f_underlying.set("BOVA11")
        dlg._f_status.set("active")

        dlg._cmd_save()

        self.mock_repo.update_structure.assert_called_once()
        sid_arg = self.mock_repo.update_structure.call_args[0][0]
        self.assertEqual(sid_arg, 7)

    def test_create_nao_e_chamado_no_modo_edicao(self):
        dlg = self._make_edit_dialog(7)
        dlg._f_name.set("X")
        dlg._f_underlying.set("Y")
        dlg._f_status.set("active")

        dlg._cmd_save()

        self.mock_repo.create_structure.assert_not_called()

    def test_replace_legs_usa_structure_id_existente(self):
        dlg = self._make_edit_dialog(7)
        dlg._f_name.set("X")
        dlg._f_underlying.set("Y")
        dlg._f_status.set("active")
        dlg._legs_rows = []

        dlg._cmd_save()

        self.mock_repo.replace_legs.assert_called_once_with(7, [])


# ===========================================================================
# Bloco 5 -- Verificacoes estaticas
# ===========================================================================

class TestStructureEditorDialogStaticChecks(unittest.TestCase):

    def test_arquivo_existe(self):
        path = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "UI", "components", "structure_editor_dialog.py"
        )
        self.assertTrue(os.path.isfile(path))

    def test_importavel(self):
        if not _IMPORT_OK:
            self.skipTest(f"Import falhou: {_IMPORT_ERROR}")
        self.assertTrue(_IMPORT_OK)

    def test_classe_presente(self):
        if not _IMPORT_OK:
            self.skipTest("Modulo nao importavel")
        for metodo in ("_cmd_save", "_load_existing", "_build_legs_payload", "_build_ui"):
            self.assertTrue(
                hasattr(StructureEditorDialog, metodo),
                f"{metodo} ausente em StructureEditorDialog"
            )

    def test_construtor_aceita_db_path(self):
        if not _IMPORT_OK:
            self.skipTest("Modulo nao importavel")
        sig = inspect.signature(StructureEditorDialog.__init__)
        params = list(sig.parameters.keys())
        self.assertIn("db_path",      params)
        self.assertIn("structure_id", params)

    def test_construtor_aceita_repo_injetado(self):
        """Confirma que o construtor aceita _repo para injecao em testes."""
        if not _IMPORT_OK:
            self.skipTest("Modulo nao importavel")
        sig = inspect.signature(StructureEditorDialog.__init__)
        self.assertIn(
            "_repo", sig.parameters,
            "StructureEditorDialog.__init__ deve aceitar _repo=None para injecao de dependencia"
        )

    def test_nao_importa_sqlite3_diretamente(self):
        import ast
        path = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "UI", "components", "structure_editor_dialog.py"
        )
        if not os.path.isfile(path):
            self.skipTest("arquivo nao encontrado")
        with open(path, encoding="utf-8") as f:
            tree = ast.parse(f.read())
        imports = [
            n.names[0].name for n in ast.walk(tree) if isinstance(n, ast.Import)
        ]
        import_froms = [
            n.module for n in ast.walk(tree)
            if isinstance(n, ast.ImportFrom) and n.module
        ]
        self.assertNotIn("sqlite3", imports)
        self.assertNotIn("sqlite3", import_froms)


if __name__ == "__main__":
    unittest.main()

def test_build_legs_payload_normaliza_position_side_legado_long_short():
    dlg = object.__new__(StructureEditorDialog)
    dlg._legs_rows = [
        {
            "position_side": "LONG",
            "option_type": "CALL",
            "strike": 100.0,
            "expiration_date": "2026-12-18",
            "quantity": 1,
            "premium": None,
            "multiplier": 1,
            "symbol": "TESTC100",
            "notes": None,
        },
        {
            "position_side": "SHORT",
            "option_type": "PUT",
            "strike": 90.0,
            "expiration_date": "2026-12-18",
            "quantity": 2,
            "premium": None,
            "multiplier": 1,
            "symbol": "TESTP90",
            "notes": None,
        },
    ]

    payload = dlg._build_legs_payload()

    assert payload[0]["position_side"] == "COMPRADO"
    assert payload[0]["leg_order"] == 1
    assert payload[1]["position_side"] == "VENDIDO"
    assert payload[1]["leg_order"] == 2

def test_build_legs_payload_normaliza_strike_com_virgula_para_float():
    dlg = object.__new__(StructureEditorDialog)
    dlg._legs_rows = [
        {
            "position_side": "COMPRADO",
            "option_type": "CALL",
            "strike": "100,00",
            "expiration_date": "2026-12-18",
            "quantity": 1,
            "premium": None,
            "multiplier": 1,
            "symbol": "TESTC100",
            "notes": None,
        }
    ]

    payload = dlg._build_legs_payload()

    assert payload[0]["strike"] == 100.0
    assert isinstance(payload[0]["strike"], float)


def test_build_legs_payload_normaliza_strike_com_ponto_para_float():
    dlg = object.__new__(StructureEditorDialog)
    dlg._legs_rows = [
        {
            "position_side": "COMPRADO",
            "option_type": "CALL",
            "strike": "100.50",
            "expiration_date": "2026-12-18",
            "quantity": 1,
            "premium": None,
            "multiplier": 1,
            "symbol": "TESTC100",
            "notes": None,
        }
    ]

    payload = dlg._build_legs_payload()

    assert payload[0]["strike"] == 100.50
    assert isinstance(payload[0]["strike"], float)


def test_build_legs_payload_nao_modifica_strike_original_ao_normalizar():
    dlg = object.__new__(StructureEditorDialog)
    original_leg = {
        "position_side": "COMPRADO",
        "option_type": "CALL",
        "strike": "100,00",
        "expiration_date": "2026-12-18",
        "quantity": 1,
        "premium": None,
        "multiplier": 1,
        "symbol": "TESTC100",
        "notes": None,
    }
    dlg._legs_rows = [original_leg]

    payload = dlg._build_legs_payload()

    assert payload[0]["strike"] == 100.0
    assert original_leg["strike"] == "100,00"

# FASE_3A4_TESTS_STRUCTURE_EDITOR_DIALOG

def test_build_legs_payload_normaliza_premium_com_virgula_para_float():
    dlg = object.__new__(StructureEditorDialog)
    dlg._legs_rows = [
        {
            "position_side": "COMPRADO",
            "option_type": "CALL",
            "strike": "100,00",
            "expiration_date": "2026-12-18",
            "quantity": 1,
            "premium": "1,25",
            "multiplier": 1,
            "symbol": "TESTC100",
            "notes": None,
        }
    ]

    payload = dlg._build_legs_payload()

    assert payload[0]["premium"] == 1.25
    assert isinstance(payload[0]["premium"], float)


def test_build_legs_payload_normaliza_multiplier_com_virgula_para_float():
    dlg = object.__new__(StructureEditorDialog)
    dlg._legs_rows = [
        {
            "position_side": "COMPRADO",
            "option_type": "CALL",
            "strike": "100,00",
            "expiration_date": "2026-12-18",
            "quantity": 1,
            "premium": None,
            "multiplier": "100,0",
            "symbol": "TESTC100",
            "notes": None,
        }
    ]

    payload = dlg._build_legs_payload()

    assert payload[0]["multiplier"] == 100.0
    assert isinstance(payload[0]["multiplier"], float)


def test_build_legs_payload_preserva_premium_none():
    dlg = object.__new__(StructureEditorDialog)
    dlg._legs_rows = [
        {
            "position_side": "COMPRADO",
            "option_type": "CALL",
            "strike": "100,00",
            "expiration_date": "2026-12-18",
            "quantity": 1,
            "premium": None,
            "multiplier": 1,
            "symbol": "TESTC100",
            "notes": None,
        }
    ]

    payload = dlg._build_legs_payload()

    assert payload[0]["premium"] is None
