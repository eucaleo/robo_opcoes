"""
patch_35 — Testes de regressão para DetailsPanel (details_panel.py)
Execução:
    python ATT/tests/test_patch35_details_panel.py

Estratégia de mock headless:
  - Injetamos sys.modules com tipos Python REAIS (não MagicMock) para ttk.LabelFrame
    e demais widgets, ANTES do import de details_panel.
  - Isso garante que DetailsPanel seja uma classe type() válida para object.__new__().
  - _setup_widgets é substituído por no-op via monkeypatch na classe após o import.
"""

import sys
import sqlite3
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock

# ── 1. RAIZ DO PROJETO ────────────────────────────────────────────────────────
RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

# ── 2. FAKE WIDGETS (classes Python reais, NÃO MagicMock) ────────────────────

class _FakeWidget:
    def __init__(self, *a, **kw): pass
    def grid(self, **kw): pass
    def grid_rowconfigure(self, *a, **kw): pass
    def grid_columnconfigure(self, *a, **kw): pass
    def config(self, **kw): pass
    def configure(self, **kw): pass
    def pack(self, **kw): pass
    def bind(self, *a, **kw): pass
    def winfo_exists(self): return True

class _FakeLabelFrame(_FakeWidget): pass
class _FakeLabel(_FakeWidget): pass
class _FakeFrame(_FakeWidget): pass
class _FakeButton(_FakeWidget): pass
class _FakeEntry(_FakeWidget):
    def get(self): return ""
class _FakeScrolledText(_FakeWidget):
    def insert(self, *a, **kw): pass
    def delete(self, *a, **kw): pass
    def config(self, **kw): pass

class _FakeStringVar:
    def __init__(self, *a, **kw): self._v = ""
    def get(self): return self._v
    def set(self, v): self._v = v

class _FakeBooleanVar:
    def __init__(self, *a, **kw): self._v = False
    def get(self): return self._v
    def set(self, v): self._v = v


# ── 2b. LIMPA cache tk/UI ANTES de injetar fakes ─────────────────────────────
# Crítico: remove versões reais ou MagicMock que possam já estar em sys.modules
_TK_MODULES_TO_PURGE = [
    "tkinter",
    "tkinter.ttk",
    "tkinter.scrolledtext",
    "tkinter.messagebox",
    "tkinter.simpledialog",
    "UI.components.details_panel",  # força re-import com fakes corretos
]
for _m in _TK_MODULES_TO_PURGE:
    sys.modules.pop(_m, None)


# ── 3. MÓDULOS FAKE ───────────────────────────────────────────────────────────

def _build_tk_modules():
    tk = types.ModuleType("tkinter")
    tk.WORD       = "word"
    tk.END        = "end"
    tk.DISABLED   = "disabled"
    tk.NORMAL     = "normal"
    tk.W          = "w"
    tk.E          = "e"
    tk.N          = "n"
    tk.S          = "s"
    tk.LEFT       = "left"
    tk.RIGHT      = "right"
    tk.BOTH       = "both"
    tk.X          = "x"
    tk.Y          = "y"
    tk.TRUE       = True
    tk.FALSE      = False
    tk.StringVar  = _FakeStringVar
    tk.BooleanVar = _FakeBooleanVar
    tk.Frame      = _FakeFrame
    tk.Label      = _FakeLabel
    tk.Button     = _FakeButton
    tk.Entry      = _FakeEntry

    ttk = types.ModuleType("tkinter.ttk")
    ttk.LabelFrame = _FakeLabelFrame
    ttk.Label      = _FakeLabel
    ttk.Frame      = _FakeFrame
    ttk.Button     = _FakeButton
    ttk.Entry      = _FakeEntry
    # ✅ Widgets extras usados em type annotations no details_panel.py
    ttk.Scrollbar  = _FakeWidget
    ttk.Combobox   = _FakeWidget
    ttk.Treeview   = _FakeWidget
    ttk.Notebook   = _FakeWidget
    ttk.Spinbox    = _FakeWidget
    ttk.Scale      = _FakeWidget
    ttk.Separator  = _FakeWidget
    ttk.Progressbar = _FakeWidget
    # ✅ __getattr__ de fallback retorna _FakeWidget (type real), NÃO MagicMock
    # Assim qualquer outro widget não listado acima também funciona em anotações
    ttk.__getattr__ = lambda name: _FakeWidget

    st = types.ModuleType("tkinter.scrolledtext")
    st.ScrolledText = _FakeScrolledText

    mb = types.ModuleType("tkinter.messagebox")
    mb.showerror = lambda *a, **kw: None
    mb.showinfo  = lambda *a, **kw: None
    mb.askyesno  = lambda *a, **kw: False

    sd = types.ModuleType("tkinter.simpledialog")
    sd.askstring  = lambda *a, **kw: None
    sd.askinteger = lambda *a, **kw: None

    # ✅ Expõe ttk e scrolledtext como atributos do objeto tk
    tk.ttk          = ttk
    tk.scrolledtext = st

    return tk, ttk, st, mb, sd


_tk, _ttk, _st, _mb, _sd = _build_tk_modules()

# ── 3b. INJETA com atribuição direta (não setdefault) ─────────────────────────
for _name, _mod in [
    ("tkinter",              _tk),
    ("tkinter.ttk",          _ttk),
    ("tkinter.scrolledtext", _st),
    ("tkinter.messagebox",   _mb),
    ("tkinter.simpledialog", _sd),
]:
    sys.modules[_name] = _mod   # ← força sobrescrita


# ── 4. IMPORT DO MÓDULO-ALVO ──────────────────────────────────────────────────
from UI.components.details_panel import DetailsPanel  # noqa: E402

assert isinstance(DetailsPanel, type), (
    f"DetailsPanel não é um type real! É: {type(DetailsPanel)}. "
    "Verifique o mock de tkinter.ttk.LabelFrame."
)

# ── 5. MONKEYPATCH: _setup_widgets → no-op ────────────────────────────────────
# Feito NA CLASSE, uma vez, antes de qualquer teste.
# Isso evita que __init__ tente criar widgets reais.
_ORIGINAL_SETUP = DetailsPanel.__dict__.get("_setup_widgets")

def _noop_setup_widgets(self):
    """No-op headless: nenhum widget Tk é criado."""
    pass

DetailsPanel._setup_widgets = _noop_setup_widgets


# ── 6. FACTORY _make_panel ────────────────────────────────────────────────────

class _FakeScrolledTextInstance(_FakeScrolledText):
    """Instância dedicada para o atributo why_text."""
    pass


def _make_panel(derived_path: Path, raw_path: Path) -> DetailsPanel:
    """
    Cria DetailsPanel real sem display Tk.

    Fluxo:
      1. __init__ é chamado normalmente (chama super().__init__ → _FakeLabelFrame)
      2. _setup_widgets é no-op → nenhum widget Tk criado
      3. Injetamos atributos de widget mínimos para os métodos testados
      4. Sobrescrevemos _derived_db_path / _raw_db_path com os paths de teste
    """
    parent = _FakeFrame()          # parent real, não MagicMock
    panel  = DetailsPanel(parent=parent)

    # ── Widgets mínimos ────────────────────────────────────────────────────────
    # Qualquer atributo de widget que métodos testados tentam acessar.
    for attr in (
        "btn_recalculate",
        "lbl_recalc_status",
        "timestamp_label",
        "structure_label",
        "decision_label",
        "level_label",
        "pl_atual_label",
        "pl_max_label",
        "ratio_label",
        "dte_label",
        "spot_ref_label",
        "breakevens_label",
        "source_label",
        "created_at_label",
        "lbl_status",
    ):
        setattr(panel, attr, _FakeWidget())

    panel.why_text = _FakeScrolledTextInstance()

    # ── Sobrescreve paths de DB ────────────────────────────────────────────────
    # details_panel usa self._derived_db_path() ou self._raw_db_path()
    # como callables OU como atributos diretos. Cobrimos os dois casos:
    panel._derived_db_path = lambda: derived_path   # callable
    panel._raw_db_path     = lambda: raw_path        # callable
    # Caso seja atributo direto (Path):
    panel.derived_db_path  = derived_path
    panel.raw_db_path      = raw_path

    return panel


# ── 7. HELPERS DE BANCO ───────────────────────────────────────────────────────

def _make_derived_db(path: Path):
    con = sqlite3.connect(str(path))
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE structure_decisions (
            structure_id  INTEGER,
            timestamp     TEXT,
            decision      TEXT,
            level         INTEGER,
            pl_atual      REAL,
            pl_max        REAL,
            pl_pct_of_max REAL,
            dte_min       INTEGER,
            spot_ref      REAL,
            meta_json     TEXT,
            created_at    TEXT,
            why           TEXT,
            why_json      TEXT,
            aba           TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE payoff_curve_points (
            structure_id INTEGER,
            timestamp    TEXT,
            point_spot   REAL,
            point_pl     REAL
        )
    """)
    cur.executemany(
        "INSERT INTO structure_decisions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [
            (7,  "2025-01-10 10:00:00", "HOLD", 2,  100.0, 200.0,  0.5,  30,
             50.0, None, "2025-01-10 09:00:00", "razao hold", None, "BOVA11"),
            (99, "2025-01-09 09:00:00", "EXIT", 3,  -50.0, 200.0, -0.25, 10,
             48.0, None, "2025-01-09 08:00:00", None, None, "PETR4"),
        ],
    )
    cur.executemany(
        "INSERT INTO payoff_curve_points VALUES (?,?,?,?)",
        [
            (7, "2025-01-10 10:00:00", 45.0, -20.0),
            (7, "2025-01-10 10:00:00", 50.0,   0.0),
            (7, "2025-01-10 10:00:00", 55.0,  30.0),
            (7, "2025-01-10 10:00:00", 60.0,  50.0),
        ],
    )
    con.commit()
    con.close()


def _make_raw_db(path: Path, use_structure_id: bool = True):
    con = sqlite3.connect(str(path))
    cur = con.cursor()
    if use_structure_id:
        cur.execute("""
            CREATE TABLE robo_legs_snapshot (
                structure_id INTEGER,
                timestamp    TEXT,
                aba          TEXT
            )
        """)
        cur.executemany(
            "INSERT INTO robo_legs_snapshot VALUES (?,?,?)",
            [
                (7,  "2025-01-10 10:00:00", "BOVA11"),
                (99, "2025-01-09 09:00:00", "PETR4"),
            ],
        )
    else:
        cur.execute("""
            CREATE TABLE robo_legs_snapshot (
                aba       TEXT,
                timestamp TEXT
            )
        """)
        cur.execute(
            "INSERT INTO robo_legs_snapshot VALUES (?,?)",
            ("BOVA11", "2025-01-10 10:00:00"),
        )
    con.commit()
    con.close()


# ════════════════════════════════════════════════════════════════════════════════
# TESTES
# ════════════════════════════════════════════════════════════════════════════════

class TestResolveStructureKey(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        d = Path(tmp.name) / "derived.db"
        r = Path(tmp.name) / "app.db"
        _make_derived_db(d)
        _make_raw_db(r)
        self.panel = _make_panel(d, r)

    def test_int_passthrough(self):
        self.assertEqual(self.panel._resolve_structure_key(7), 7)

    def test_str_numerica(self):
        self.assertEqual(self.panel._resolve_structure_key("7"), 7)

    def test_str_invalida_levanta_value_error(self):
        with self.assertRaises(ValueError):
            self.panel._resolve_structure_key("BOVA11")

    def test_none_levanta_value_error(self):
        with self.assertRaises((ValueError, TypeError)):
            self.panel._resolve_structure_key(None)

    def test_float_int_aceito(self):
        """int(7.0) == 7 — comportamento do Python padrão."""
        self.assertEqual(self.panel._resolve_structure_key(7.0), 7)


class TestFetchLatestDecision(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        d = Path(tmp.name) / "derived.db"
        r = Path(tmp.name) / "app.db"
        _make_derived_db(d)
        _make_raw_db(r)
        self.panel = _make_panel(d, r)

    def test_retorna_decisao_por_structure_id_int(self):
        d = self.panel._fetch_latest_decision_from_derived(7)
        self.assertIsNotNone(d)
        self.assertEqual(d["structure_id"], 7)
        self.assertEqual(d["decision"], "HOLD")

    def test_retorna_decisao_por_structure_id_str(self):
        d = self.panel._fetch_latest_decision_from_derived("7")
        self.assertIsNotNone(d)
        self.assertEqual(d["decision"], "HOLD")

    def test_structure_inexistente_retorna_none(self):
        self.assertIsNone(self.panel._fetch_latest_decision_from_derived(999))

    def test_nao_usa_aba_como_filtro_quando_structure_id_existe(self):
        """patch_35: query deve filtrar por INTEGER, não por aba TEXT."""
        d = self.panel._fetch_latest_decision_from_derived("7")
        self.assertIsNotNone(d, "Deve encontrar via structure_id INTEGER")

    def test_spot_ref_renomeado_para_spot_reference(self):
        d = self.panel._fetch_latest_decision_from_derived(7)
        self.assertIn("spot_reference", d)
        self.assertNotIn("spot_ref", d)

    def test_structure_id_invalido_levanta_value_error(self):
        with self.assertRaises(ValueError):
            self.panel._fetch_latest_decision_from_derived("BOVA11")

    def test_why_preenchido_quando_why_json_nulo(self):
        d = self.panel._fetch_latest_decision_from_derived(7)
        self.assertEqual(d.get("why"), "razao hold")

    def test_outro_structure_id(self):
        d = self.panel._fetch_latest_decision_from_derived(99)
        self.assertIsNotNone(d)
        self.assertEqual(d["decision"], "EXIT")


class TestFetchPayoffPoints(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        d = Path(tmp.name) / "derived.db"
        r = Path(tmp.name) / "app.db"
        _make_derived_db(d)
        _make_raw_db(r)
        self.panel = _make_panel(d, r)

    def test_retorna_pontos_ordenados_por_spot(self):
        pts = self.panel._fetch_payoff_points_from_derived(7)
        spots = [p[0] for p in pts]
        self.assertEqual(spots, sorted(spots))

    def test_retorna_4_pontos(self):
        pts = self.panel._fetch_payoff_points_from_derived(7)
        self.assertEqual(len(pts), 4)

    def test_valores_sao_float(self):
        pts = self.panel._fetch_payoff_points_from_derived(7)
        self.assertTrue(all(isinstance(x, float) and isinstance(y, float) for x, y in pts))

    def test_structure_inexistente_retorna_lista_vazia(self):
        self.assertEqual(self.panel._fetch_payoff_points_from_derived(999), [])

    def test_structure_id_invalido_levanta_value_error(self):
        with self.assertRaises(ValueError):
            self.panel._fetch_payoff_points_from_derived("BOVA11")

    def test_str_numerica_aceita(self):
        pts = self.panel._fetch_payoff_points_from_derived("7")
        self.assertEqual(len(pts), 4)


class TestFetchAuditInfo(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        d = Path(tmp.name) / "derived.db"
        r = Path(tmp.name) / "app.db"
        _make_derived_db(d)
        _make_raw_db(r)
        self.panel = _make_panel(d, r)

    def test_count_points_correto(self):
        info = self.panel._fetch_audit_info_from_derived(7)
        self.assertEqual(info["count_points"], 4)

    def test_created_at_preenchido(self):
        info = self.panel._fetch_audit_info_from_derived(7)
        self.assertIsNotNone(info["created_at"])

    def test_fallback_false(self):
        info = self.panel._fetch_audit_info_from_derived(7)
        self.assertFalse(info["fallback"])

    def test_structure_inexistente_count_zero(self):
        info = self.panel._fetch_audit_info_from_derived(999)
        self.assertEqual(info["count_points"], 0)

    def test_structure_id_invalido_levanta_value_error(self):
        with self.assertRaises(ValueError):
            self.panel._fetch_audit_info_from_derived("BOVA11")

    def test_source_table_no_resultado(self):
        info = self.panel._fetch_audit_info_from_derived(7)
        self.assertIn("source_table", info)


class TestGetLatestSnapshotTimestamp(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.derived = Path(self.tmp.name) / "derived.db"
        _make_derived_db(self.derived)

    def _make(self, raw_path: Path) -> DetailsPanel:
        return _make_panel(self.derived, raw_path)

    def test_retorna_timestamp_por_structure_id(self):
        raw = Path(self.tmp.name) / "app.db"
        _make_raw_db(raw, use_structure_id=True)
        ts = self._make(raw)._get_latest_snapshot_timestamp_for_structure(7)
        self.assertIsNotNone(ts)
        self.assertIn("2025-01-10", ts)

    def test_structure_inexistente_retorna_none(self):
        raw = Path(self.tmp.name) / "app.db"
        _make_raw_db(raw, use_structure_id=True)
        ts = self._make(raw)._get_latest_snapshot_timestamp_for_structure(999)
        self.assertIsNone(ts)

    def test_db_ausente_retorna_none(self):
        raw = Path(self.tmp.name) / "nao_existe.db"
        ts = self._make(raw)._get_latest_snapshot_timestamp_for_structure(7)
        self.assertIsNone(ts)

    def test_fallback_aba_quando_sem_structure_id(self):
        raw = Path(self.tmp.name) / "app_legado.db"
        _make_raw_db(raw, use_structure_id=False)
        ts = self._make(raw)._get_latest_snapshot_timestamp_for_structure("BOVA11")
        self.assertIsNotNone(ts)

    def test_str_numerica_aceita(self):
        raw = Path(self.tmp.name) / "app2.db"
        _make_raw_db(raw, use_structure_id=True)
        ts = self._make(raw)._get_latest_snapshot_timestamp_for_structure("7")
        self.assertIsNotNone(ts)


class TestComputeBreakevens(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        d = Path(tmp.name) / "derived.db"
        r = Path(tmp.name) / "app.db"
        _make_derived_db(d)
        _make_raw_db(r)
        self.panel = _make_panel(d, r)

    def test_lista_vazia(self):
        self.assertEqual(self.panel._compute_breakevens_from_points([]), [])

    def test_ponto_unico(self):
        self.assertEqual(self.panel._compute_breakevens_from_points([(50.0, 0.0)]), [])

    def test_sem_cruzamento(self):
        pts = [(40.0, -10.0), (50.0, -5.0), (60.0, -1.0)]
        self.assertEqual(self.panel._compute_breakevens_from_points(pts), [])

    def test_cruzamento_zero_exato(self):
        pts = [(40.0, -10.0), (50.0, 0.0), (60.0, 10.0)]
        bes = self.panel._compute_breakevens_from_points(pts)
        self.assertEqual(len(bes), 1)
        self.assertAlmostEqual(bes[0], 50.0, places=4)

    def test_cruzamento_interpolado(self):
        pts = [(40.0, -10.0), (60.0, 10.0)]
        bes = self.panel._compute_breakevens_from_points(pts)
        self.assertEqual(len(bes), 1)
        self.assertAlmostEqual(bes[0], 50.0, places=4)

    def test_dois_breakevens(self):
        pts = [(40.0, -10.0), (50.0, 10.0), (60.0, -5.0)]
        bes = self.panel._compute_breakevens_from_points(pts)
        self.assertEqual(len(bes), 2)

    def test_deduplicacao(self):
        pts = [(40.0, -10.0), (50.0, 0.0), (60.0, -10.0)]
        bes = self.panel._compute_breakevens_from_points(pts)
        self.assertEqual(len(bes), 1)

    def test_breakeven_nos_dados_reais(self):
        """Com os 4 pontos do DB de teste: zero exato em spot=50.0."""
        pts = self.panel._fetch_payoff_points_from_derived(7)
        bes = self.panel._compute_breakevens_from_points(pts)
        self.assertGreater(len(bes), 0, "Deve haver pelo menos 1 breakeven")
        self.assertTrue(
            any(abs(be - 50.0) < 1e-4 for be in bes),
            f"Esperado breakeven ~50.0, obtido: {bes}",
        )


class TestComputePlAtSpot(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        d = Path(tmp.name) / "derived.db"
        r = Path(tmp.name) / "app.db"
        _make_derived_db(d)
        _make_raw_db(r)
        self.panel = _make_panel(d, r)
        self.pts   = [(40.0, -20.0), (50.0, 0.0), (60.0, 40.0)]

    def test_pts_vazio(self):
        self.assertIsNone(self.panel._compute_pl_at_spot([], 50.0))

    def test_spot_none(self):
        self.assertIsNone(self.panel._compute_pl_at_spot(self.pts, None))

    def test_ponto_exato_zero(self):
        self.assertAlmostEqual(self.panel._compute_pl_at_spot(self.pts, 50.0), 0.0)

    def test_interpolacao_linear(self):
        result = self.panel._compute_pl_at_spot(self.pts, 55.0)
        self.assertAlmostEqual(result, 20.0, places=4)

    def test_fora_range_retorna_none(self):
        self.assertIsNone(self.panel._compute_pl_at_spot(self.pts, 10.0))
        self.assertIsNone(self.panel._compute_pl_at_spot(self.pts, 99.0))

    def test_ponto_esquerdo_exato(self):
        self.assertAlmostEqual(self.panel._compute_pl_at_spot(self.pts, 40.0), -20.0)

    def test_ponto_direito_exato(self):
        self.assertAlmostEqual(self.panel._compute_pl_at_spot(self.pts, 60.0), 40.0)


class TestSetRecalcUiState(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        d = Path(tmp.name) / "derived.db"
        r = Path(tmp.name) / "app.db"
        _make_derived_db(d)
        _make_raw_db(r)
        self.panel = _make_panel(d, r)

    def test_in_progress_true(self):
        self.panel._set_recalc_ui_state(True, msg="Processando", color="blue")
        self.assertTrue(self.panel._recalc_in_progress)

    def test_in_progress_false(self):
        self.panel._set_recalc_ui_state(False, msg="OK", color="green")
        self.assertFalse(self.panel._recalc_in_progress)

    def test_sem_widgets_nao_crasha(self):
        """Se widgets não existirem, não deve levantar exceção."""
        del self.panel.btn_recalculate
        del self.panel.lbl_recalc_status
        try:
            self.panel._set_recalc_ui_state(True)
        except Exception as e:
            self.fail(f"_set_recalc_ui_state levantou exceção inesperada: {e}")


class TestComputeRecalcSignature(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.derived = Path(tmp.name) / "derived.db"
        self.raw     = Path(tmp.name) / "app.db"
        _make_derived_db(self.derived)
        _make_raw_db(self.raw)
        self.panel = _make_panel(self.derived, self.raw)

    def test_retorna_tupla(self):
        sig = self.panel._compute_recalc_signature(7)
        self.assertIsInstance(sig, tuple)
        self.assertEqual(len(sig), 2)

    def test_primeiro_elemento_eh_structure_id(self):
        sig = self.panel._compute_recalc_signature(7)
        self.assertEqual(sig[0], 7)

    def test_segunda_elemento_eh_timestamp(self):
        sig = self.panel._compute_recalc_signature(7)
        self.assertIsNotNone(sig[1])

    def test_estrutura_diferente_gera_assinatura_diferente(self):
        sig7  = self.panel._compute_recalc_signature(7)
        sig99 = self.panel._compute_recalc_signature(99)
        self.assertNotEqual(sig7, sig99)


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    unittest.main(verbosity=2)
