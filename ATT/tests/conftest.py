"""
Mocka Tk/Toplevel ANTES de qualquer import dos views,
permitindo rodar testes de dialogs sem display fisico.
"""

# tests/conftest.py
import sys
import types
from unittest.mock import MagicMock
import pytest
from pathlib import Path

# tests/ -> ATT/ -> projeto/
_TESTS_DIR   = Path(__file__).resolve().parent          # ATT/tests
_ATT_ROOT    = _TESTS_DIR.parent                        # ATT/
PROJECT_ROOT = _ATT_ROOT.parent                         # projeto/

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(_ATT_ROOT) not in sys.path:
    sys.path.insert(0, str(_ATT_ROOT))

DB_PATH = PROJECT_ROOT / "dados" / "derived.db"

print(f"\n[conftest] PROJECT_ROOT : {PROJECT_ROOT}")
print(f"[conftest] DB_PATH      : {DB_PATH}")
print(f"[conftest] DB existe?   : {DB_PATH.exists()}")


def _make_tk_mock():
    """Cria um modulo tkinter falso completo com _FakeWidget universal."""
    tk_mock = types.ModuleType("tkinter")

    # ------------------------------------------------------------------ #
    #  _FakeWidget UNIVERSAL                                               #
    #  Aceita qualquer metodo via __getattr__ retornando um callable noop  #
    # ------------------------------------------------------------------ #
    class _FakeWidget:
        def __init__(self, *a, **kw):
            self._val = kw.get("value", "")

        # metodos comuns explícitos
        def grid(self, *a, **kw):        return self
        def pack(self, *a, **kw):        return self
        def place(self, *a, **kw):       return self
        def config(self, *a, **kw):      return self
        def configure(self, *a, **kw):   return self
        def bind(self, *a, **kw):        return self
        def destroy(self):               pass
        def winfo_exists(self):          return 1
        def title(self, *a):             pass
        def geometry(self, *a):          pass
        def transient(self, *a):         pass
        def grab_set(self):              pass
        def focus_set(self):             pass
        def columnconfigure(self, *a, **kw): pass
        def rowconfigure(self, *a, **kw):    pass
        def get(self):                   return self._val
        def set(self, v):                self._val = v
        def insert(self, *a):            pass
        def delete(self, *a):            pass
        def update(self, *a, **kw):      pass
        def update_idletasks(self):      pass
        def mainloop(self):              pass
        def withdraw(self):              pass
        def deiconify(self):             pass
        def lift(self):                  pass
        def lower(self):                 pass
        def after(self, *a, **kw):       return None
        def after_cancel(self, *a):      pass
        def event_generate(self, *a, **kw): pass

        # Treeview / Listbox / Text
        def heading(self, *a, **kw):     return self
        def column(self, *a, **kw):      return self
        def insert(self, *a, **kw):      return ""
        def item(self, *a, **kw):        return {}
        def selection(self):             return ()
        def selection_set(self, *a):     pass
        def delete(self, *a):            pass
        def get_children(self, *a):      return []
        def see(self, *a):               pass
        def index(self, *a):             return 0
        def yview(self, *a):             return (0, 1)
        def xview(self, *a):             return (0, 1)

        # Canvas
        def create_line(self, *a, **kw):      return 1
        def create_rectangle(self, *a, **kw): return 1
        def create_text(self, *a, **kw):      return 1
        def create_oval(self, *a, **kw):      return 1
        def create_polygon(self, *a, **kw):   return 1
        def coords(self, *a, **kw):           return []
        def itemconfig(self, *a, **kw):       pass
        def tag_bind(self, *a, **kw):         pass

        # Scrollbar
        def set(self, *a):  pass

        # Variaveis StringVar / IntVar / BooleanVar
        def trace_add(self, *a, **kw):    pass
        def trace_variable(self, *a, **kw): pass

        # -------------------------------------------------------------- #
        #  CATCH-ALL: qualquer outro metodo desconhecido retorna noop      #
        # -------------------------------------------------------------- #
        def __getattr__(self, name):
            def _noop(*a, **kw):
                return self
            return _noop

    # Subclasses especializadas (herdam o catch-all)
    class _FakeTk(_FakeWidget):
        pass

    class _FakeToplevel(_FakeWidget):
        pass

    class _FakeStringVar(_FakeWidget):
        def __init__(self, *a, **kw):
            self._val = kw.get("value", "")
        def get(self):      return self._val
        def set(self, v):   self._val = str(v)
        def trace_add(self, *a, **kw): pass

    class _FakeIntVar(_FakeWidget):
        def __init__(self, *a, **kw):
            self._val = int(kw.get("value", 0))
        def get(self):      return self._val
        def set(self, v):   self._val = int(v)

    class _FakeBooleanVar(_FakeWidget):
        def __init__(self, *a, **kw):
            self._val = bool(kw.get("value", False))
        def get(self):      return self._val
        def set(self, v):   self._val = bool(v)

    class _FakeFrame(_FakeWidget):    pass
    class _FakeLabel(_FakeWidget):    pass
    class _FakeButton(_FakeWidget):   pass
    class _FakeEntry(_FakeWidget):    pass
    class _FakeCanvas(_FakeWidget):   pass
    class _FakeText(_FakeWidget):     pass
    class _FakeListbox(_FakeWidget):  pass

    class _FakeCombobox(_FakeWidget):
        def current(self, idx=None):
            return 0 if idx is None else None
        def state(self, *a): return ()

    class _FakeTreeview(_FakeWidget):
        def heading(self, col, **kw): return self
        def column(self, col, **kw):  return self
        def insert(self, parent, index, **kw): return f"I{id(self)}"
        def get_children(self, item=""): return []
        def item(self, iid, **kw): return {}
        def selection(self): return ()
        def delete(self, *items): pass
        def see(self, item): pass
        def tag_configure(self, *a, **kw): pass

    # Constantes
    for _k, _v in {
        "END": "end", "LEFT": "left", "RIGHT": "right",
        "TOP": "top", "BOTTOM": "bottom", "BOTH": "both",
        "X": "x", "Y": "y", "W": "w", "E": "e",
        "N": "n", "S": "s", "NW": "nw", "NE": "ne",
        "SW": "sw", "SE": "se", "NSEW": "nsew",
        "WORD": "word", "CHAR": "char",
        "NORMAL": "normal", "DISABLED": "disabled",
        "HIDDEN": "hidden", "ACTIVE": "active",
        "FLAT": "flat", "RAISED": "raised", "SUNKEN": "sunken",
        "GROOVE": "groove", "RIDGE": "ridge",
        "HORIZONTAL": "horizontal", "VERTICAL": "vertical",
        "BROWSE": "browse", "EXTENDED": "extended",
        "INSERT": "insert", "SEL": "sel", "SEL_FIRST": "sel.first",
        "SEL_LAST": "sel.last", "ANCHOR": "anchor",
        "CURRENT": "current", "ALL": "all",
        "FIRST": "first", "LAST": "last",
        "TRUE": True, "FALSE": False,
        "YES": "yes", "NO": "no",
        "CENTER": "center", "NW": "nw", "NE": "ne", "SW": "sw", "SE": "se",
    }.items():
        setattr(tk_mock, _k, _v)

    # Classes principais
    tk_mock.Tk            = _FakeTk
    tk_mock.Toplevel      = _FakeToplevel
    tk_mock.StringVar     = _FakeStringVar
    tk_mock.IntVar        = _FakeIntVar
    tk_mock.BooleanVar    = _FakeBooleanVar
    tk_mock.DoubleVar     = _FakeIntVar
    tk_mock.Frame         = _FakeFrame
    tk_mock.LabelFrame    = _FakeFrame
    tk_mock.Label         = _FakeLabel
    tk_mock.Button        = _FakeButton
    tk_mock.Entry         = _FakeEntry
    tk_mock.Text          = _FakeText
    tk_mock.Canvas        = _FakeCanvas
    tk_mock.Listbox       = _FakeListbox
    tk_mock.Scrollbar     = _FakeWidget
    tk_mock.Menu          = _FakeWidget
    tk_mock.Menubutton    = _FakeWidget
    tk_mock.OptionMenu    = _FakeWidget
    tk_mock.Checkbutton   = _FakeWidget
    tk_mock.Radiobutton   = _FakeWidget
    tk_mock.Scale         = _FakeWidget
    tk_mock.Spinbox       = _FakeEntry
    tk_mock.PanedWindow   = _FakeFrame
    tk_mock.Message       = _FakeLabel
    tk_mock.Wm            = _FakeWidget

    # Constantes de ancoragem/alinhamento
    tk_mock.CENTER = "center"
    tk_mock.N      = "n"
    tk_mock.S      = "s"
    tk_mock.E      = "e"
    tk_mock.W      = "w"
    tk_mock.NW     = "nw"
    tk_mock.NE     = "ne"
    tk_mock.SW     = "sw"
    tk_mock.SE     = "se"
    tk_mock.NSEW   = "nsew"

    # ttk
    ttk = types.ModuleType("tkinter.ttk")
    ttk.Frame         = _FakeFrame
    ttk.LabelFrame    = _FakeFrame
    ttk.Label         = _FakeLabel
    ttk.Button        = _FakeButton
    ttk.Entry         = _FakeEntry
    ttk.Combobox      = _FakeCombobox
    ttk.Treeview      = _FakeTreeview
    ttk.Scrollbar     = _FakeWidget
    ttk.Notebook      = _FakeWidget
    ttk.Separator     = _FakeWidget
    ttk.Scale         = _FakeWidget
    ttk.Spinbox       = _FakeEntry
    ttk.Progressbar   = _FakeWidget
    ttk.Panedwindow   = _FakeFrame
    ttk.Style         = _FakeWidget
    ttk.Sizegrip      = _FakeWidget
    tk_mock.ttk       = ttk

    # messagebox
    mb = types.ModuleType("tkinter.messagebox")
    mb.showerror   = MagicMock()
    mb.showinfo    = MagicMock()
    mb.showwarning = MagicMock()
    mb.askyesno    = MagicMock(return_value=True)
    mb.askokcancel = MagicMock(return_value=True)
    mb.askyesnocancel = MagicMock(return_value=True)
    tk_mock.messagebox = mb

    # simpledialog
    sd = types.ModuleType("tkinter.simpledialog")
    sd.Dialog     = _FakeWidget
    sd.askstring  = MagicMock(return_value="")
    sd.askinteger = MagicMock(return_value=0)
    sd.askfloat   = MagicMock(return_value=0.0)
    tk_mock.simpledialog = sd

    # filedialog
    fd = types.ModuleType("tkinter.filedialog")
    fd.askopenfilename  = MagicMock(return_value="")
    fd.asksaveasfilename = MagicMock(return_value="")
    fd.askdirectory     = MagicMock(return_value="")
    tk_mock.filedialog  = fd

    # colorchooser
    cc = types.ModuleType("tkinter.colorchooser")
    cc.askcolor = MagicMock(return_value=((0, 0, 0), "#000000"))
    tk_mock.colorchooser = cc

    return tk_mock, ttk, mb, sd, fd, cc


# Injeta ANTES de qualquer import dos views
_tk_mock, _ttk, _mb, _sd, _fd, _cc = _make_tk_mock()
sys.modules.setdefault("tkinter",              _tk_mock)
sys.modules.setdefault("tkinter.ttk",          _ttk)
sys.modules.setdefault("tkinter.messagebox",   _mb)
sys.modules.setdefault("tkinter.simpledialog", _sd)
sys.modules.setdefault("tkinter.filedialog",   _fd)
sys.modules.setdefault("tkinter.colorchooser", _cc)
