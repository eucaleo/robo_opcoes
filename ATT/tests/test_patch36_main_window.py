# tests/test_patch36_main_window.py
"""
Testes Patch_36 -- main_window.py
Verifica que MainWindow opera por structure_id (sem fallback aba).
"""
import sys
import types
import threading
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, call

#  1. RAIZ DO PROJETO 
RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

#  2. PURGA cache 
for _m in list(sys.modules):
    if _m.startswith(("tkinter", "UI.main_window", "UI.components", "UI.dialogs")):
        sys.modules.pop(_m, None)


#  3. FAKE TKINTER 

class _W:
    def __init__(self, *a, **kw): pass
    def __call__(self, *a, **kw): return self
    def grid(self, **kw): return self
    def pack(self, **kw): return self
    def config(self, **kw): return self
    def configure(self, **kw): return self
    def bind(self, *a, **kw): return self
    def winfo_exists(self): return True
    def winfo_screenwidth(self): return 1920
    def winfo_screenheight(self): return 1080
    def winfo_width(self): return 800
    def winfo_height(self): return 600
    def grid_rowconfigure(self, *a, **kw): return self
    def grid_columnconfigure(self, *a, **kw): return self
    def columnconfigure(self, *a, **kw): return self
    def rowconfigure(self, *a, **kw): return self
    def title(self, *a, **kw): return self
    def geometry(self, *a, **kw): return self
    def protocol(self, *a, **kw): return self
    def resizable(self, *a, **kw): return self
    def minsize(self, *a, **kw): return self
    def after(self, *a, **kw): return self
    def destroy(self, *a, **kw): return self
    def mainloop(self, *a, **kw): return self
    def withdraw(self, *a, **kw): return self
    def deiconify(self, *a, **kw): return self
    def update_idletasks(self, *a, **kw): return self
    def get(self): return ""
    def insert(self, *a, **kw): return self
    def delete(self, *a, **kw): return self
    def see(self, *a, **kw): return self
    def yview(self, *a, **kw): return self
    def xview(self, *a, **kw): return self
    def set(self, *a, **kw): return self
    def tag_configure(self, *a, **kw): return self
    def heading(self, *a, **kw): return self
    def column(self, *a, **kw): return self
    def selection(self): return []
    def item(self, *a, **kw): return {}
    def get_children(self): return []


class _FakeStringVar:
    def __init__(self, *a, **kw): self._v = ""
    def get(self): return self._v
    def set(self, v): self._v = v
    def trace_add(self, *a, **kw): pass

class _FakeBooleanVar:
    def __init__(self, *a, **kw): self._v = False
    def get(self): return self._v
    def set(self, v): self._v = v

class _FakeIntVar:
    def __init__(self, *a, **kw): self._v = 0
    def get(self): return self._v
    def set(self, v): self._v = v


def _install_fake_tk():
    tk = types.ModuleType("tkinter")
    fd = types.ModuleType("tkinter.filedialog")
    fd.askopenfilename  = lambda *a, **kw: None
    fd.asksaveasfilename = lambda *a, **kw: None
    fd.askdirectory     = lambda *a, **kw: None
    for name in (
        "WORD","END","DISABLED","NORMAL","W","E","N","S",
        "LEFT","RIGHT","BOTH","X","Y","TOP","BOTTOM",
        "HORIZONTAL","VERTICAL","FLAT","SUNKEN","RAISED",
        "GROOVE","RIDGE","NSEW","NS","EW","BROWSE",
        "EXTENDED","MULTIPLE","SINGLE","ACTIVE","HIDDEN","TRUE","FALSE",
        "CENTER","ANCHOR","BASELINE","MIDDLE","NONE","ROUND","BUTT",
        "PROJECTING","BEVEL","MITER","ARC","CHORD","PIESLICE",
        "FIRST","LAST","SOLID","DASH","DOTDASH","INSERT","SEL",
        "SEL_FIRST","SEL_LAST","ALL","CURRENT","READABLE","WRITABLE",
        "EXECUTABLE","CASCADE","CHECKBUTTON","COMMAND","RADIOBUTTON",
        "SEPARATOR","TEAROFF","NUMERIC","ALPHA","ALPHANUMERIC",
        "NO","YES","ON","OFF","AT","PIXELS","UNITS","PAGES",
        "MOVETO","SCROLL","NW","NE","SW","SE",
    ):
        setattr(tk, name, name.lower())

    tk.StringVar   = _FakeStringVar
    tk.BooleanVar  = _FakeBooleanVar
    tk.IntVar      = _FakeIntVar

    for cls_name in (
        "Frame","Label","Button","Entry","Text","Canvas","Menu",
        "Menubutton","LabelFrame","Scrollbar","Listbox","Checkbutton",
        "Radiobutton","Scale","Spinbox","OptionMenu","PanedWindow",
        "Tk","Toplevel","PhotoImage",
    ):
        setattr(tk, cls_name, _W)

    fnt = types.ModuleType("tkinter.font")
    fnt.Font = _W
    fnt.families = lambda: []
    fnt.nametofont = lambda *a, **kw: _W()
    tk.font = fnt

    ttk = types.ModuleType("tkinter.ttk")
    for cls_name in (
        "Frame","LabelFrame","Label","Button","Entry","Scrollbar",
        "Combobox","Treeview","Notebook","Spinbox","Scale",
        "Separator","Progressbar","PanedWindow","Checkbutton",
        "Radiobutton","Style",
    ):
        setattr(ttk, cls_name, _W)

    st = types.ModuleType("tkinter.scrolledtext")
    st.ScrolledText = _W

    mb = types.ModuleType("tkinter.messagebox")
    mb.showerror   = lambda *a, **kw: None
    mb.showinfo    = lambda *a, **kw: None
    mb.showwarning = lambda *a, **kw: None
    mb.askyesno    = lambda *a, **kw: False
    mb.askokcancel = lambda *a, **kw: False

    sd = types.ModuleType("tkinter.simpledialog")
    sd.askstring  = lambda *a, **kw: None
    sd.askinteger = lambda *a, **kw: None
    sd.askfloat   = lambda *a, **kw: None

    class _SimpleDialog:
        def __init__(self, *a, **kw): pass
        def go(self): return None
        def return_event(self, event=None): pass
        def wm_delete_window(self): pass
        def body(self, master): pass

    sd.SimpleDialog = _SimpleDialog
    sd.Dialog       = _SimpleDialog

    tk.ttk          = ttk
    tk.scrolledtext = st
    tk.messagebox   = mb
    tk.simpledialog = sd
    tk.filedialog   = fd

    # fake matplotlib backends -- impede import da extensao C _tkagg
    _mpl_btk = types.ModuleType("matplotlib.backends._backend_tk")
    _mpl_btk.FigureCanvasTk          = _W
    _mpl_btk.FigureManagerTk         = _W
    _mpl_btk.NavigationToolbar2Tk    = _W
    _mpl_btk.blit                    = lambda *a, **kw: None

    _mpl_tkagg = types.ModuleType("matplotlib.backends.backend_tkagg")
    _mpl_tkagg.FigureCanvasTkAgg     = _W
    _mpl_tkagg.FigureManagerTkAgg    = _W
    _mpl_tkagg.NavigationToolbar2Tk  = _W

    _mpl_tkagg2 = types.ModuleType("matplotlib.backends._tkagg")

    for mod_name, mod in [
        ("tkinter",                          tk),
        ("tkinter.ttk",                      ttk),
        ("tkinter.scrolledtext",             st),
        ("tkinter.messagebox",               mb),
        ("tkinter.simpledialog",             sd),
        ("tkinter.font",                     fnt),
        ("tkinter.filedialog",               fd),
        ("matplotlib.backends._tkagg",       _mpl_tkagg2),
        ("matplotlib.backends._backend_tk",  _mpl_btk),
        ("matplotlib.backends.backend_tkagg",_mpl_tkagg),
    ]:
        sys.modules[mod_name] = mod


_install_fake_tk()


# #  4. PRÉ-IMPORTA UI.main_window 
_PATCH_TARGETS = [
    "UIDataModel", "FiltersPanel", "DecisionsGrid",
    "DetailsPanel", "PayoffChart", "StructuresListPanel",
    "StructureEditorDialog",
]

try:
    import UI.main_window as _mw_mod
except Exception as _exc:
    _mw_stub = types.ModuleType("UI.main_window")
    _mw_stub.MainWindow = type("MainWindow", (), {})
    sys.modules["UI.main_window"] = _mw_stub
    import UI as _ui_pkg
    _ui_pkg.main_window = _mw_stub
    _mw_mod = _mw_stub


#  5. HELPER: descobre o nome real de um método 

def _find_method(cls, *candidates):
    """
    Retorna o primeiro nome de método que existe na classe.
    Se nenhum existir, retorna o primeiro candidato (o preferido pelo patch_36).
    """
    for name in candidates:
        if callable(getattr(cls, name, None)):
            return name
    return candidates[0]  # nome preferido -- o teste vai falhar com mensagem clara


#  6. FIXTURE 

@pytest.fixture
def win():
    import importlib

    #  Limpa qualquer resíduo de fake-tkinter de outros testes 
    # patch35 injeta fakes sem _W; patch36 precisa dos seus próprios fakes
    _mw_key = "UI.main_window"
    _current = sys.modules.get(_mw_key)
    if _current is not None:
        _cls = getattr(_current, "MainWindow", None)
        # Se MainWindow não tem os métodos reais, é um stub contaminado
        _is_stub = not callable(getattr(_cls, "recalculate_structure", None))
        if _is_stub:
            # Remove o módulo e suas dependências UI para forçar re-import
            for _k in [k for k in sys.modules if k.startswith("UI.")]:
                sys.modules.pop(_k, None)

    #  Garante fake tkinter do patch36 (reinstala se patch35 sobrescreveu) 
    _install_fake_tk()

    #  Agora importa o módulo real 
    import UI.main_window
    from UI.main_window import MainWindow

    patches = [
        patch(f"UI.main_window.{t}", MagicMock(), create=True)
        for t in _PATCH_TARGETS
    ]
    for p in patches:
        p.start()

    w = MainWindow.__new__(MainWindow)
    w.root = MagicMock()

    #  estado interno 
    w._recalc_in_progress          = False
    w._payoff_worker_id            = 0
    w._loading_payoff              = False
    w._loading_animation_active    = False
    w._loading_animation_chars     = []
    w._loading_animation_index     = 0
    w.last_selected_decision       = None

    #  componentes mock 
    w.data_model     = MagicMock()
    w.filters_panel  = MagicMock()
    w.decisions_grid = MagicMock()
    w.details_panel  = MagicMock()
    w.payoff_chart   = MagicMock()
    w.status_bar     = MagicMock()

    #  descobre nomes reais dos métodos 
    cls = type(w)
    w._method_map = {
        "recalculate_structure": _find_method(
            cls, "recalculate_structure", "recalculate"
        ),
        "refresh_data": _find_method(
            cls, "refresh_data", "refresh", "update_data"
        ),
        "on_decision_selected": _find_method(
            cls, "on_decision_selected", "on_selection_changed", "select_decision"
        ),
        "_start_payoff_load": _find_method(
            cls, "_start_payoff_load", "_load_payoff", "_update_payoff"
        ),
    }

    yield w

    for p in patches:
        p.stop()

    #  Teardown: limpa UI.main_window para não vazar para próximos testes 
    for _k in [k for k in sys.modules if k.startswith("UI.")]:
        sys.modules.pop(_k, None)

def _call(obj, logical_name, *args, **kwargs):
    """Chama o método real usando o mapa de nomes."""
    real = obj._method_map[logical_name]
    return getattr(obj, real)(*args, **kwargs)


def _patch_method(obj, logical_name):
    """patch.object usando o nome real."""
    real = obj._method_map[logical_name]
    return patch.object(obj, real, create=True)


# ===========================================================================
# 1. recalculate_aba removido
# ===========================================================================

class TestRecalculateAbaRemovido:

    def test_metodo_nao_existe(self, win):
        """patch_36: recalculate_aba deve ter sido removido da MainWindow."""
        assert not hasattr(win, "recalculate_aba"), (
            "recalculate_aba() ainda existe -- deve ser removido no patch_36"
        )


# ===========================================================================
# 2. recalculate_structure
# ===========================================================================

class TestRecalculateStructure:

    def test_ignora_se_recalc_em_andamento(self, win):
        win._recalc_in_progress = True
        with patch("threading.Thread") as MockThread:
            _call(win, "recalculate_structure", "5")
            MockThread.assert_not_called()

    def test_inicia_thread_worker(self, win):
        win._recalc_in_progress = False
        win.payoff_chart.fix_current_curve = MagicMock()
        with patch("threading.Thread") as MockThread:
            MockThread.return_value.start = MagicMock()
            _call(win, "recalculate_structure", 5)
        MockThread.assert_called_once()
        assert MockThread.return_value.start.called

    def test_seta_recalc_in_progress(self, win):
        win._recalc_in_progress = False
        win.payoff_chart.fix_current_curve = MagicMock()
        with patch("threading.Thread") as MockThread:
            MockThread.return_value.start = MagicMock()
            _call(win, "recalculate_structure", 7)
        assert win._recalc_in_progress is True

    def test_status_bar_atualizado(self, win):
        win._recalc_in_progress = False
        win.payoff_chart.fix_current_curve = MagicMock()
        with patch("threading.Thread") as MockThread:
            MockThread.return_value.start = MagicMock()
            _call(win, "recalculate_structure", 3)
        win.status_bar.config.assert_called_with(text="Recalculando 3...")

    def test_aceita_structure_id_inteiro(self, win):
        win._recalc_in_progress = False
        win.payoff_chart.fix_current_curve = MagicMock()
        with patch("threading.Thread") as MockThread:
            MockThread.return_value.start = MagicMock()
            _call(win, "recalculate_structure", 42)
        win.status_bar.config.assert_any_call(text="Recalculando 42...")


# ===========================================================================
# 3. refresh_data -- sem fallback aba
# ===========================================================================

class TestRefreshDataSemAba:

    def _setup(self, win, decisions=None):
        win.data_model.refresh              = MagicMock()
        win.data_model.get_structures       = MagicMock(return_value=[])
        win.data_model.get_decisions        = MagicMock(return_value=decisions or [])
        win.filters_panel.update_structures = MagicMock()
        win.filters_panel.reset_filters     = MagicMock()
        win.decisions_grid.update_data      = MagicMock()
        win.decisions_grid.select_by_key    = MagicMock()
        win.details_panel.update_decision   = MagicMock()
        win.details_panel.clear             = MagicMock()
        win.payoff_chart.clear              = MagicMock()

    def test_preserva_por_structure_id(self, win):
        self._setup(win)
        win.last_selected_decision = {"structure_id": 5, "timestamp": "2025-01-01"}
        with _patch_method(win, "_start_payoff_load"):
            _call(win, "refresh_data")
        win.decisions_grid.select_by_key.assert_called_with(5, "2025-01-01")

    def test_nao_usa_aba_para_select(self, win):
        """patch_36: aba isolada não deve disparar select_by_key."""
        self._setup(win)
        win.last_selected_decision = {"aba": "WING", "timestamp": "2025-01-01"}
        with _patch_method(win, "_start_payoff_load"):
            _call(win, "refresh_data")
        win.decisions_grid.select_by_key.assert_not_called()

    def test_nao_inicia_payoff_sem_structure_id(self, win):
        self._setup(win)
        win.last_selected_decision = {"aba": "WING", "timestamp": "2025-01-01"}
        with _patch_method(win, "_start_payoff_load") as mock_payoff:
            _call(win, "refresh_data")
        mock_payoff.assert_not_called()

    def test_limpa_paineis_sem_preserved(self, win):
        self._setup(win)
        win.last_selected_decision = None
        _call(win, "refresh_data")
        win.details_panel.clear.assert_called()
        win.payoff_chart.clear.assert_called()

    def test_status_bar_final(self, win):
        self._setup(win, decisions=[{}, {}, {}])
        win.last_selected_decision = None
        _call(win, "refresh_data")
        win.status_bar.config.assert_called_with(
            text="Dados atualizados - 3 decisões"
        )


# ===========================================================================
# 4. on_decision_selected -- sem fallback aba
# ===========================================================================

class TestOnDecisionSelectedSemAba:

    def test_usa_structure_id_para_payoff(self, win):
        with _patch_method(win, "_start_payoff_load") as mock_payoff:
            _call(win, "on_decision_selected",
                  {"structure_id": 10, "timestamp": "2025-01-01"})
        mock_payoff.assert_called_once()
        assert mock_payoff.call_args[0][0] == 10

    def test_nao_usa_aba_para_payoff(self, win):
        """patch_36: sem structure_id  payoff não deve ser carregado."""
        with _patch_method(win, "_start_payoff_load") as mock_payoff:
            _call(win, "on_decision_selected",
                  {"aba": "WING", "timestamp": "2025-01-01"})
        mock_payoff.assert_not_called()

    def test_limpa_chart_sem_structure_id(self, win):
        _call(win, "on_decision_selected",
              {"aba": "WING", "timestamp": "2025-01-01"})
        win.payoff_chart.clear.assert_called()

    def test_ignora_decision_none(self, win):
        _call(win, "on_decision_selected", None)
        win.details_panel.update_decision.assert_not_called()

    def test_preserva_last_selected(self, win):
        data = {"structure_id": 7, "timestamp": "2025-01-01"}
        with _patch_method(win, "_start_payoff_load"):
            _call(win, "on_decision_selected", data)
        assert win.last_selected_decision["structure_id"] == 7
