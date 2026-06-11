from __future__ import annotations

# Testes de integracao do editor de estruturas
"""
Testes de integração: StructureEditorDialog x MainWindow.
"""

import ast
import os
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch


# ===========================================================================
# Stubs de tkinter + matplotlib
# ===========================================================================

def _inject_stubs():
    import unittest.mock as _umock

    _tk_mock = _umock.MagicMock()
    _tk_mock.__name__    = "tkinter"
    _tk_mock.__spec__    = None
    _tk_mock.__path__    = []
    _tk_mock.__package__ = "tkinter"

    # Constantes
    _tk_mock.END        = "end"
    _tk_mock.BOTH       = "both"
    _tk_mock.YES        = True
    _tk_mock.LEFT       = "left"
    _tk_mock.RIGHT      = "right"
    _tk_mock.TOP        = "top"
    _tk_mock.BOTTOM     = "bottom"
    _tk_mock.X          = "x"
    _tk_mock.Y          = "y"
    _tk_mock.W          = "w"
    _tk_mock.E          = "e"
    _tk_mock.N          = "n"
    _tk_mock.S          = "s"
    _tk_mock.NW         = "nw"
    _tk_mock.NE         = "ne"
    _tk_mock.SW         = "sw"
    _tk_mock.SE         = "se"
    _tk_mock.NSEW       = "nsew"
    _tk_mock.CENTER     = "center"
    _tk_mock.NORMAL     = "normal"
    _tk_mock.DISABLED   = "disabled"
    _tk_mock.WORD       = "word"
    _tk_mock.VERTICAL   = "vertical"
    _tk_mock.HORIZONTAL = "horizontal"
    _tk_mock.FLAT       = "flat"
    _tk_mock.RAISED     = "raised"
    _tk_mock.SUNKEN     = "sunken"
    _tk_mock.GROOVE     = "groove"
    _tk_mock.RIDGE      = "ridge"
    _tk_mock.LAST       = "last"
    _tk_mock.FIRST      = "first"
    _tk_mock.ACTIVE     = "active"
    _tk_mock.HIDDEN     = "hidden"
    _tk_mock.CASCADE    = "cascade"
    _tk_mock.CHECKBUTTON = "checkbutton"
    _tk_mock.RADIOBUTTON = "radiobutton"
    _tk_mock.SEPARATOR  = "separator"
    _tk_mock.ANCHOR     = "anchor"
    _tk_mock.INSERT     = "insert"
    _tk_mock.SEL        = "sel"
    _tk_mock.SEL_FIRST  = "sel.first"
    _tk_mock.SEL_LAST   = "sel.last"

    # StringVar com comportamento real
    class _StringVar:
        def __init__(self, value="", *a, **kw): self._v = value
        def get(self): return self._v
        def set(self, v): self._v = v
        def trace_add(self, *a, **kw): pass
        def trace_variable(self, *a, **kw): pass

    class _BoolVar:
        def __init__(self, value=False, *a, **kw): self._v = value
        def get(self): return self._v
        def set(self, v): self._v = v

    class _IntVar:
        def __init__(self, value=0, *a, **kw): self._v = value
        def get(self): return self._v
        def set(self, v): self._v = v

    _tk_mock.StringVar  = _StringVar
    _tk_mock.BooleanVar = _BoolVar
    _tk_mock.IntVar     = _IntVar

    # ---------------------------------------------------------------
    # CORREÇÃO PRINCIPAL: Toplevel e Widget como classes reais
    # object.__new__() só funciona com tipos Python reais, não MagicMock
    # ---------------------------------------------------------------
    class _Widget:
        """Stub genérico para widgets Tk — absorve pack/grid/bind/etc."""
        def __init__(self, *a, **kw): pass
        def pack(self, *a, **kw): pass
        def grid(self, *a, **kw): pass
        def configure(self, *a, **kw): pass
        def config(self, *a, **kw): pass
        def bind(self, *a, **kw): pass
        def get(self, *a, **kw): return ""
        def set(self, *a, **kw): pass
        def delete(self, *a, **kw): pass
        def insert(self, *a, **kw): pass
        def selection_set(self, *a, **kw): pass
        def get_children(self, *a, **kw): return []
        def selection(self, *a, **kw): return []
        def heading(self, *a, **kw): pass
        def column(self, *a, **kw): pass
        def yview(self, *a, **kw): pass
        def columnconfigure(self, *a, **kw): pass
        def rowconfigure(self, *a, **kw): pass

    class _Toplevel(_Widget):
        """
        Stub de tk.Toplevel.
        Precisa ser uma classe Python real para que object.__new__()
        funcione em subclasses (StructureEditorDialog).
        """
        def title(self, *a, **kw): pass
        def transient(self, *a, **kw): pass
        def grab_set(self, *a, **kw): pass
        def resizable(self, *a, **kw): pass
        def minsize(self, *a, **kw): pass
        def destroy(self, *a, **kw): pass
        def withdraw(self, *a, **kw): pass
        def deiconify(self, *a, **kw): pass
        def wait_window(self, *a, **kw): pass

    _tk_mock.Toplevel = _Toplevel
    _tk_mock.Widget   = _Widget
    _tk_mock.Frame    = _Widget

    sys.modules["tkinter"] = _tk_mock

    # Submódulos de tkinter
    for _sub_name in ("font", "messagebox", "ttk", "filedialog",
                      "simpledialog", "colorchooser", "scrolledtext"):
        _key = f"tkinter.{_sub_name}"
        _sub_mock = _umock.MagicMock()
        _sub_mock.__name__ = _key
        _sub_mock.__spec__ = None

        if _sub_name == "messagebox":
            _sub_mock.showerror   = lambda *a, **kw: None
            _sub_mock.showwarning = lambda *a, **kw: None
            _sub_mock.showinfo    = lambda *a, **kw: None
            _sub_mock.askyesno    = lambda *a, **kw: True

        if _sub_name == "ttk":
            # CORREÇÃO: ttk widgets também precisam ser classes reais
            _sub_mock.Combobox   = _Widget
            _sub_mock.Entry      = _Widget
            _sub_mock.Label      = _Widget
            _sub_mock.Button     = _Widget
            _sub_mock.Frame      = _Widget
            _sub_mock.LabelFrame = _Widget
            _sub_mock.Treeview   = _Widget
            _sub_mock.Scrollbar  = _Widget

        sys.modules[_key] = _sub_mock
        setattr(_tk_mock, _sub_name, _sub_mock)

    # Matplotlib stubs (inalterado)
    _MPL_SUBS = [
        "matplotlib",
        "matplotlib.backends",
        "matplotlib.backends.backend_tkagg",
        "matplotlib.backends._backend_tk",
        "matplotlib.figure",
        "matplotlib.pyplot",
        "matplotlib.axes",
        "matplotlib.axes._axes",
        "matplotlib.ticker",
        "matplotlib.lines",
        "matplotlib.patches",
        "matplotlib.colors",
        "matplotlib.collections",
        "matplotlib.legend",
        "matplotlib.text",
        "matplotlib.artist",
        "matplotlib.font_manager",
        "matplotlib.image",
        "matplotlib.cm",
        "matplotlib.transforms",
        "matplotlib.path",
        "matplotlib.widgets",
        "matplotlib.gridspec",
        "matplotlib.style",
    ]
    for _mod_name in _MPL_SUBS:
        sys.modules[_mod_name] = types.ModuleType(_mod_name)

    _mpl_full = _umock.MagicMock()
    _mpl_full.__name__  = "matplotlib"
    _mpl_full.__spec__  = None
    _mpl_full.rcParams  = {}
    sys.modules["matplotlib"] = _mpl_full

    for _sub in ("ticker", "figure", "pyplot", "lines", "patches",
                 "colors", "cm", "transforms", "path", "widgets",
                 "gridspec", "style", "font_manager", "backends"):
        _child = sys.modules.get(f"matplotlib.{_sub}", types.ModuleType(f"matplotlib.{_sub}"))
        sys.modules[f"matplotlib.{_sub}"] = _child
        setattr(_mpl_full, _sub, _child)

    _mpl_stub = sys.modules["matplotlib"]
    _mpl_stub.use             = MagicMock()
    _mpl_stub.rcParams        = {}
    _mpl_stub.rcParamsDefault = {}
    _mpl_stub.get_backend     = MagicMock(return_value="TkAgg")
    _mpl_stub.is_interactive  = MagicMock(return_value=False)

    mpl_tk = sys.modules["matplotlib.backends.backend_tkagg"]
    if not hasattr(mpl_tk, "FigureCanvasTkAgg"):
        mpl_tk.FigureCanvasTkAgg    = MagicMock
        mpl_tk.NavigationToolbar2Tk = MagicMock

    fig_mod = sys.modules["matplotlib.figure"]
    if not hasattr(fig_mod, "Figure"):
        fig_mod.Figure = MagicMock

    ticker = sys.modules["matplotlib.ticker"]
    if not hasattr(ticker, "FuncFormatter"):
        ticker.FuncFormatter   = MagicMock
        ticker.MaxNLocator     = MagicMock
        ticker.AutoLocator     = MagicMock
        ticker.MultipleLocator = MagicMock

    mpl = sys.modules["matplotlib"]
    for _sub in ("ticker", "figure", "pyplot", "lines", "patches",
                 "colors", "cm", "transforms", "path", "widgets",
                 "gridspec", "style", "font_manager"):
        if not hasattr(mpl, _sub):
            setattr(mpl, _sub, sys.modules.get(f"matplotlib.{_sub}",
                                               types.ModuleType(f"matplotlib.{_sub}")))


_inject_stubs()


# ===========================================================================
# Helpers de fábrica  (inalterados)
# ===========================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _read_source(rel_path: str) -> str:
    return (PROJECT_ROOT / rel_path).read_text(encoding="utf-8")


def _reload_ui():
    _inject_stubs()
    for key in list(sys.modules.keys()):
        if key == "UI" or key.startswith("UI."):
            del sys.modules[key]
    import UI.main_window as mw_mod
    return mw_mod


def _make_dialog(structure_id=None, db_path="fake.db"):
    _inject_stubs()
    for key in list(sys.modules.keys()):
        if key == "UI" or key.startswith("UI."):
            del sys.modules[key]

    from UI.components.structure_editor_dialog import StructureEditorDialog

    dlg = object.__new__(StructureEditorDialog)
    dlg._structure_id = structure_id
    dlg.saved         = False
    dlg._legs_rows    = []
    dlg._db_path      = db_path
    dlg._repo         = MagicMock()

    class _FakeVar:
        def __init__(self, value=""):
            self._v = value
        def get(self):
            return self._v
        def set(self, v):
            self._v = v

    dlg._f_name       = _FakeVar()
    dlg._f_underlying = _FakeVar()
    dlg._f_alias      = _FakeVar()
    dlg._f_status     = _FakeVar("active")
    dlg._f_notes      = _FakeVar()

    dlg.destroy   = MagicMock()
    dlg.title     = MagicMock()
    dlg.transient = MagicMock()
    dlg.grab_set  = MagicMock()

    return dlg


def _make_main_window():
    mw_mod = _reload_ui()
    mw = object.__new__(mw_mod.MainWindow)
    mw._db_path        = "fake.db"
    mw.root            = MagicMock()
    mw.structures_list = MagicMock()
    mw.status_bar      = MagicMock()
    mw.withdraw        = MagicMock()
    mw.deiconify       = MagicMock()
    return mw, mw_mod


# ===========================================================================
# 1–6. Classes de teste (inalteradas)
# ===========================================================================

class TestStructureEditorIntegrationStaticChecks(unittest.TestCase):

    def test_main_window_arquivo_existe(self):
        self.assertTrue(
            (PROJECT_ROOT / "UI" / "main_window.py").exists(),
            "UI/main_window.py não encontrado",
        )

    def test_structure_editor_dialog_arquivo_existe(self):
        self.assertTrue(
            (PROJECT_ROOT / "UI" / "components" / "structure_editor_dialog.py").exists(),
            "UI/components/structure_editor_dialog.py não encontrado",
        )

    def test_main_window_nao_importa_sqlite3_diretamente(self):
        source = _read_source("UI/main_window.py")
        tree   = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = (
                    [a.name for a in node.names]
                    if isinstance(node, ast.Import)
                    else ([node.module] if node.module else [])
                )
                for name in names:
                    self.assertFalse(
                        name == "sqlite3" or (name or "").startswith("sqlite3"),
                        "main_window.py não deve importar sqlite3 diretamente",
                    )

    def test_main_window_importa_structure_editor_dialog(self):
        source = _read_source("UI/main_window.py")
        self.assertIn("StructureEditorDialog", source)

    def test_main_window_tem_metodo_on_structure_edit_request(self):
        source = _read_source("UI/main_window.py")
        self.assertIn("_on_structure_edit_request", source)

    def test_leg_order_comeca_em_1(self):
        dlg = _make_dialog()
        dlg._legs_rows = [
            {"position_side": "LONG", "option_type": "CALL",
             "strike": "10.00", "expiration_date": "2025-01-17",
             "quantity": 1, "premium": None, "multiplier": 1.0,
             "leg_order": 99, "symbol": None, "notes": None},
        ]
        payload = dlg._build_legs_payload()
        self.assertEqual(payload[0]["leg_order"], 1)


class TestOnStructureEditRequestCriar(unittest.TestCase):

    def test_dialog_instanciado_com_structure_id_none(self):
        mw, mw_mod = _make_main_window()
        fake_dlg = _make_dialog(structure_id=None)
        fake_dlg.saved = False
        with patch.object(mw_mod, "StructureEditorDialog", return_value=fake_dlg) as mock_cls:
            mw._on_structure_edit_request(structure_id=None)
        mock_cls.assert_called_once()
        args, kwargs = mock_cls.call_args
        sid = kwargs.get("structure_id", args[1] if len(args) > 1 else None)
        self.assertIsNone(sid)

    def test_load_nao_chamado_se_saved_false(self):
        mw, mw_mod = _make_main_window()
        dlg = _make_dialog(); dlg.saved = False
        with patch.object(mw_mod, "StructureEditorDialog", return_value=dlg):
            mw._on_structure_edit_request(structure_id=None)
        mw.structures_list.load.assert_not_called()

    def test_load_chamado_se_saved_true(self):
        mw, mw_mod = _make_main_window()
        dlg = _make_dialog(); dlg.saved = True
        with patch.object(mw_mod, "StructureEditorDialog", return_value=dlg):
            mw._on_structure_edit_request(structure_id=None)
        mw.structures_list.load.assert_called_once()

    def test_db_path_repassado_ao_dialog(self):
        mw, mw_mod = _make_main_window()
        mw._db_path = "dados/derived.db"
        dlg = _make_dialog(); dlg.saved = False
        with patch.object(mw_mod, "StructureEditorDialog", return_value=dlg) as mock_cls:
            mw._on_structure_edit_request(structure_id=None)
        _, kwargs = mock_cls.call_args
        self.assertEqual(kwargs.get("db_path"), "dados/derived.db")


class TestOnStructureEditRequestEditar(unittest.TestCase):

    def test_dialog_instanciado_com_structure_id_correto(self):
        mw, mw_mod = _make_main_window()
        dlg = _make_dialog(structure_id=7); dlg.saved = False
        with patch.object(mw_mod, "StructureEditorDialog", return_value=dlg) as mock_cls:
            mw._on_structure_edit_request(structure_id=7)
        args, kwargs = mock_cls.call_args
        sid = kwargs.get("structure_id", args[1] if len(args) > 1 else None)
        self.assertEqual(sid, 7)

    def test_load_chamado_apos_edicao_bem_sucedida(self):
        mw, mw_mod = _make_main_window()
        dlg = _make_dialog(structure_id=7); dlg.saved = True
        with patch.object(mw_mod, "StructureEditorDialog", return_value=dlg):
            mw._on_structure_edit_request(structure_id=7)
        mw.structures_list.load.assert_called_once()

    def test_load_nao_chamado_se_edicao_cancelada(self):
        mw, mw_mod = _make_main_window()
        dlg = _make_dialog(structure_id=7); dlg.saved = False
        with patch.object(mw_mod, "StructureEditorDialog", return_value=dlg):
            mw._on_structure_edit_request(structure_id=7)
        mw.structures_list.load.assert_not_called()




class TestCmdSave(unittest.TestCase):

    def _dlg(self, structure_id=None, name="Iron Fly", underlying="BBAS3"):
        dlg = _make_dialog(structure_id=structure_id)
        dlg._f_name.set(name)
        dlg._f_underlying.set(underlying)
        dlg._f_alias.set("")
        dlg._f_status.set("active")
        dlg._f_notes.set("")
        return dlg

    def test_saved_true_apos_criar(self):
        dlg = self._dlg(structure_id=None)
        dlg._repo.create_structure.return_value = 10
        dlg._cmd_save()
        self.assertTrue(dlg.saved)

    def test_saved_true_apos_editar(self):
        dlg = self._dlg(structure_id=55)
        dlg._cmd_save()
        self.assertTrue(dlg.saved)

    def test_destroy_chamado_apos_salvar(self):
        dlg = self._dlg(structure_id=None)
        dlg._repo.create_structure.return_value = 20
        dlg._cmd_save()
        dlg.destroy.assert_called_once()

    def test_create_nao_chamado_no_modo_edicao(self):
        dlg = self._dlg(structure_id=33)
        dlg._cmd_save()
        dlg._repo.create_structure.assert_not_called()

    def test_update_nao_chamado_no_modo_criacao(self):
        dlg = self._dlg(structure_id=None)
        dlg._repo.create_structure.return_value = 99
        dlg._cmd_save()
        dlg._repo.update_structure.assert_not_called()

    def test_replace_legs_sid_correto_criacao(self):
        dlg = self._dlg(structure_id=None)
        dlg._repo.create_structure.return_value = 77
        dlg._cmd_save()
        dlg._repo.replace_legs.assert_called_once_with(77, [])

    def test_replace_legs_sid_correto_edicao(self):
        dlg = self._dlg(structure_id=88)
        dlg._cmd_save()
        dlg._repo.replace_legs.assert_called_once_with(88, [])

    def test_saved_false_se_name_vazio(self):
        dlg = self._dlg(name="")
        with patch("tkinter.messagebox.showwarning"):
            dlg._cmd_save()
        self.assertFalse(dlg.saved)

    def test_saved_false_se_underlying_vazio(self):
        dlg = self._dlg(underlying="")
        with patch("tkinter.messagebox.showwarning"):
            dlg._cmd_save()
        self.assertFalse(dlg.saved)

    def test_exception_nao_propaga(self):
        dlg = self._dlg(structure_id=None)
        dlg._repo.create_structure.side_effect = Exception("DB offline")
        with patch("tkinter.messagebox.showerror"):
            dlg._cmd_save()
        self.assertFalse(dlg.saved)


class TestIntegracaoLegs(unittest.TestCase):

    def _dlg_com_legs(self, structure_id=None):
        dlg = _make_dialog(structure_id=structure_id)
        dlg._f_name.set("Spread")
        dlg._f_underlying.set("WEGE3")
        dlg._f_alias.set("")
        dlg._f_status.set("active")
        dlg._f_notes.set("")
        dlg._legs_rows = [
            {"position_side": "LONG",  "option_type": "CALL",
             "strike": "25.00", "expiration_date": "2025-03-21",
             "quantity": 1, "premium": None, "multiplier": 1.0,
             "leg_order": 1, "symbol": None, "notes": None},
            {"position_side": "SHORT", "option_type": "CALL",
             "strike": "27.00", "expiration_date": "2025-03-21",
             "quantity": 1, "premium": None, "multiplier": 1.0,
             "leg_order": 2, "symbol": None, "notes": None},
        ]
        return dlg

    def test_replace_legs_recebe_2_legs(self):
        dlg = self._dlg_com_legs(structure_id=None)
        dlg._repo.create_structure.return_value = 5
        dlg._cmd_save()
        _, legs_arg = dlg._repo.replace_legs.call_args[0]
        self.assertEqual(len(legs_arg), 2)

    def test_legs_payload_tem_leg_order_sequencial(self):
        dlg = self._dlg_com_legs()
        payload = dlg._build_legs_payload()
        self.assertEqual(payload[0]["leg_order"], 1)
        self.assertEqual(payload[1]["leg_order"], 2)

    def test_legs_payload_preserva_position_side(self):
        dlg = self._dlg_com_legs()
        payload = dlg._build_legs_payload()
        self.assertEqual(payload[0]["position_side"], "LONG")
        self.assertEqual(payload[1]["position_side"], "SHORT")


if __name__ == "__main__":
    unittest.main(verbosity=2)
