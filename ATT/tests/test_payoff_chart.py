# C:/users/eucal/projeto/ATT/tests/test_payoff_chart.py
"""
Testes unitários para UI/components/payoff_chart.py
Cobertura:
  - _fmt_number_br / _fmt_currency_br / _brl_abbrev
  - _find_breakevens
  - _interp_y_at_x
  - _extract_xy (tuple, dict, objeto)
  - PayoffChart.clear()
  - PayoffChart.update_chart()
  - PayoffChart.fix_current_curve() / clear_comparison()
  - PayoffChart.get_last_overlays()
"""

import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Raiz do projeto: C:/users/eucal/projeto
# tests/ está em ATT/tests/, então subimos UM nível para chegar em ATT/
# e mais UM para chegar na raiz C:/users/eucal/projeto
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
    # ATT/tests/ -> ATT/ -> projeto/
)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ---------------------------------------------------------------------------
# Stub de módulos que exigem display ou infra real
# ---------------------------------------------------------------------------
_STUBS = {
    "matplotlib":                        MagicMock(),
    "matplotlib.use":                    MagicMock(),
    "matplotlib.figure":                 MagicMock(),
    "matplotlib.ticker":                 MagicMock(),
    "matplotlib.backends":               MagicMock(),
    "matplotlib.backends.backend_tkagg": MagicMock(),
    "UI.debug_utils":                    MagicMock(),
}
for _mod, _stub in _STUBS.items():
    sys.modules.setdefault(_mod, _stub)

# FuncFormatter precisa ser chamável
sys.modules["matplotlib.ticker"].FuncFormatter = lambda f: f

# Importa DEPOIS dos stubs
from UI.components.payoff_chart import (  # noqa: E402
    PayoffChart,
    _fmt_number_br,
    _fmt_currency_br,
    _brl_abbrev,
)


# ---------------------------------------------------------------------------
# Fixture: instância de PayoffChart com Tk fake
# ---------------------------------------------------------------------------

def _make_chart() -> PayoffChart:
    """Cria PayoffChart com dependências Tk mockadas."""
    with patch("UI.components.payoff_chart.FigureCanvasTkAgg"), \
         patch("UI.components.payoff_chart.NavigationToolbar2Tk"), \
         patch("UI.components.payoff_chart.Figure") as MockFig, \
         patch("UI.components.payoff_chart.ttk.Frame.__init__", return_value=None), \
         patch("UI.components.payoff_chart.ttk.Frame.pack",     return_value=None), \
         patch("UI.components.payoff_chart.ttk.Frame.bind",     return_value=None):

        mock_fig = MagicMock()
        mock_ax  = MagicMock()
        mock_fig.add_subplot.return_value = mock_ax
        MockFig.return_value = mock_fig

        chart = PayoffChart.__new__(PayoffChart)
        chart.fig     = mock_fig
        chart.ax      = mock_ax
        chart.canvas  = MagicMock()
        chart.toolbar = MagicMock()
        chart._last_breakevens     = []
        chart._last_pl_at_spot_ref = None
        chart._last_points         = []
        chart._last_decision_data  = {}
        chart._fixed_curve         = None

    return chart


# ---------------------------------------------------------------------------
# Sample data helpers
# ---------------------------------------------------------------------------

def _linear_points(n: int = 20, x_start=90.0, x_end=110.0,
                   y_start=-1000.0, y_end=1000.0):
    """Gera pontos lineares cruzando zero."""
    points = []
    for i in range(n):
        t = i / (n - 1)
        x = x_start + t * (x_end - x_start)
        y = y_start + t * (y_end - y_start)
        points.append({"spot": x, "pl": y})
    return points


def _flat_points(n: int = 10, x_start=90.0, x_end=110.0, y=500.0):
    """Pontos com PL constante (sem breakeven)."""
    return [
        {"spot": x_start + i * (x_end - x_start) / (n - 1), "pl": y}
        for i in range(n)
    ]


# ===========================================================================
# Testes de Formatação
# ===========================================================================

class TestFormatters(unittest.TestCase):

    def test_fmt_number_br_basic(self):
        self.assertEqual(_fmt_number_br(1234.56), "1.234,56")

    def test_fmt_number_br_zero(self):
        self.assertEqual(_fmt_number_br(0), "0,00")

    def test_fmt_number_br_negative(self):
        self.assertEqual(_fmt_number_br(-1500.0), "-1.500,00")

    def test_fmt_number_br_million(self):
        self.assertEqual(_fmt_number_br(1_000_000), "1.000.000,00")

    def test_fmt_number_br_custom_decimals(self):
        self.assertEqual(_fmt_number_br(100.1, 0), "100")

    def test_fmt_currency_br_basic(self):
        self.assertEqual(_fmt_currency_br(500.0), "R$ 500,00")

    def test_fmt_currency_br_negative(self):
        self.assertTrue(_fmt_currency_br(-200.5).startswith("R$"))

    def test_brl_abbrev_below_1k(self):
        self.assertIn("500", _brl_abbrev(500))

    def test_brl_abbrev_thousands(self):
        self.assertIn("k", _brl_abbrev(1500))

    def test_brl_abbrev_millions(self):
        self.assertIn("M", _brl_abbrev(2_500_000))

    def test_brl_abbrev_billions(self):
        self.assertIn("B", _brl_abbrev(3_000_000_000))

    def test_brl_abbrev_negative(self):
        result = _brl_abbrev(-5000)
        self.assertIn("-", result)
        self.assertIn("k", result)

    def test_brl_abbrev_invalid(self):
        result = _brl_abbrev("NaN")
        self.assertIn("R$", result)


# ===========================================================================
# Testes de _find_breakevens
# ===========================================================================

class TestFindBreakevens(unittest.TestCase):

    def _be(self, spots, pls):
        return PayoffChart._find_breakevens(spots, pls)

    def test_single_crossing_zero(self):
        spots = [90.0, 95.0, 100.0, 105.0, 110.0]
        pls   = [-200, -100, 0, 100, 200]
        bks   = self._be(spots, pls)
        self.assertEqual(len(bks), 1)
        self.assertAlmostEqual(bks[0], 100.0, places=5)

    def test_interpolated_crossing(self):
        spots = [98.0, 102.0]
        pls   = [-100.0, 100.0]
        bks   = self._be(spots, pls)
        self.assertEqual(len(bks), 1)
        self.assertAlmostEqual(bks[0], 100.0, places=5)

    def test_no_crossing(self):
        spots = [90.0, 100.0, 110.0]
        pls   = [100.0, 200.0, 300.0]
        bks   = self._be(spots, pls)
        self.assertEqual(bks, [])

    def test_two_crossings(self):
        spots = [80.0, 90.0, 100.0, 110.0, 120.0]
        pls   = [100.0, -50.0, -100.0, -50.0, 100.0]
        bks   = self._be(spots, pls)
        self.assertEqual(len(bks), 2)

    def test_touching_zero_without_crossing(self):
        spots = [95.0, 100.0, 105.0]
        pls   = [100.0, 0.0, 100.0]
        bks   = self._be(spots, pls)
        self.assertIn(100.0, bks)

    def test_empty_inputs(self):
        self.assertEqual(self._be([], []), [])

    def test_mismatched_lengths(self):
        self.assertEqual(self._be([1, 2], [1]), [])

    def test_deduplication(self):
        spots = [99.9999, 100.0, 100.0001]
        pls   = [-1e-10, 0.0, 1e-10]
        bks   = self._be(spots, pls)
        self.assertLessEqual(len(bks), 2)


# ===========================================================================
# Testes de _interp_y_at_x
# ===========================================================================

class TestInterpYAtX(unittest.TestCase):

    def _interp(self, xs, ys, x):
        return PayoffChart._interp_y_at_x(xs, ys, x)

    def test_exact_point(self):
        xs = [90.0, 100.0, 110.0]
        ys = [0.0,  500.0, 1000.0]
        self.assertAlmostEqual(self._interp(xs, ys, 100.0), 500.0)

    def test_midpoint_interpolation(self):
        xs = [0.0, 10.0]
        ys = [0.0, 100.0]
        self.assertAlmostEqual(self._interp(xs, ys, 5.0), 50.0)

    def test_out_of_range_returns_none(self):
        xs = [90.0, 110.0]
        ys = [0.0, 100.0]
        self.assertIsNone(self._interp(xs, ys, 200.0))

    def test_empty_returns_none(self):
        self.assertIsNone(self._interp([], [], 100.0))

    def test_mismatched_returns_none(self):
        self.assertIsNone(self._interp([1, 2, 3], [1, 2], 1.5))

    def test_negative_ys(self):
        xs = [0.0, 10.0]
        ys = [-100.0, 100.0]
        self.assertAlmostEqual(self._interp(xs, ys, 5.0), 0.0)

    def test_single_segment_boundary_right(self):
        xs = [10.0, 20.0]
        ys = [0.0, 10.0]
        self.assertAlmostEqual(self._interp(xs, ys, 20.0), 10.0)


# ===========================================================================
# Testes de _extract_xy
# ===========================================================================

class TestExtractXY(unittest.TestCase):

    def _ex(self, p):
        return _make_chart()._extract_xy(p)

    def test_tuple_format(self):
        x, y = self._ex((100.0, 500.0))
        self.assertAlmostEqual(x, 100.0)
        self.assertAlmostEqual(y, 500.0)

    def test_list_format(self):
        x, y = self._ex([95.0, -200.0])
        self.assertAlmostEqual(x, 95.0)
        self.assertAlmostEqual(y, -200.0)

    def test_dict_spot_pl(self):
        x, y = self._ex({"spot": 100.5, "pl": 300.0})
        self.assertAlmostEqual(x, 100.5)
        self.assertAlmostEqual(y, 300.0)

    def test_dict_point_spot_point_pl(self):
        x, y = self._ex({"point_spot": 99.0, "point_pl": -50.0})
        self.assertAlmostEqual(x, 99.0)
        self.assertAlmostEqual(y, -50.0)

    def test_dict_x_y(self):
        x, y = self._ex({"x": 50.0, "y": 1000.0})
        self.assertAlmostEqual(x, 50.0)
        self.assertAlmostEqual(y, 1000.0)

    def test_dict_pnl(self):
        x, y = self._ex({"spot": 105.0, "pnl": 750.0})
        self.assertAlmostEqual(x, 105.0)
        self.assertAlmostEqual(y, 750.0)

    def test_unknown_format_returns_none(self):
        x, y = self._ex({})
        self.assertIsNone(x)
        self.assertIsNone(y)


# ===========================================================================
# Testes de PayoffChart (estado e lógica)
# ===========================================================================

class TestPayoffChartState(unittest.TestCase):

    def setUp(self):
        self.chart = _make_chart()

    def test_clear_resets_state(self):
        self.chart._last_breakevens     = [100.0]
        self.chart._last_pl_at_spot_ref = 500.0
        self.chart._last_points         = [{"spot": 100.0, "pl": 0.0}]
        self.chart.clear()
        self.assertEqual(self.chart._last_breakevens, [])
        self.assertIsNone(self.chart._last_pl_at_spot_ref)
        self.assertEqual(self.chart._last_points, [])

    def test_update_chart_empty_returns_dict(self):
        result = self.chart.update_chart([])
        self.assertIn("breakevens", result)
        self.assertIn("pl_at_spot_ref", result)

    def test_update_chart_saves_points(self):
        pts = _linear_points()
        self.chart.update_chart(pts)
        self.assertEqual(len(self.chart._last_points), len(pts))

    def test_update_chart_saves_decision_data(self):
        pts = _linear_points()
        dd  = {"structure_id": "collar_1", "decision": "BUY", "spot_ref": 100.0}
        self.chart.update_chart(pts, decision_data=dd)
        self.assertEqual(self.chart._last_decision_data["structure_id"], "collar_1")

    def test_update_chart_finds_breakeven(self):
        pts    = _linear_points(n=200, x_start=90, x_end=110,
                                y_start=-1000, y_end=1000)
        result = self.chart.update_chart(pts)
        self.assertGreater(len(result["breakevens"]), 0)
        self.assertAlmostEqual(result["breakevens"][0], 100.0, delta=0.2)

    def test_update_chart_no_breakeven_flat(self):
        result = self.chart.update_chart(_flat_points(y=500.0))
        self.assertEqual(result["breakevens"], [])

    def test_update_chart_pl_at_spot_ref(self):
        pts    = _linear_points(n=200, x_start=90, x_end=110,
                                y_start=-1000, y_end=1000)
        result = self.chart.update_chart(pts, decision_data={"spot_ref": 100.0})
        self.assertIsNotNone(result["pl_at_spot_ref"])
        self.assertAlmostEqual(result["pl_at_spot_ref"], 0.0, delta=20.0)

    def test_update_chart_spot_ref_none_when_missing(self):
        result = self.chart.update_chart(_linear_points(), decision_data={})
        self.assertIsNone(result["pl_at_spot_ref"])

    def test_fix_current_curve_sets_fixed(self):
        self.chart._last_points = _linear_points()
        self.chart.fix_current_curve()
        self.assertIsNotNone(self.chart._fixed_curve)
        self.assertIn("points", self.chart._fixed_curve)

    def test_fix_empty_clears_fixed(self):
        self.chart._last_points = []
        self.chart.fix_current_curve()
        self.assertIsNone(self.chart._fixed_curve)

    def test_fix_curve_label(self):
        self.chart._last_points = _linear_points()
        self.chart.fix_current_curve()
        self.assertIn("Curva A", self.chart._fixed_curve["label"])

    def test_fix_curve_color_is_red(self):
        self.chart._last_points = _linear_points()
        self.chart.fix_current_curve()
        self.assertEqual(self.chart._fixed_curve["color"], "red")

    def test_clear_comparison_removes_fixed(self):
        self.chart._last_points = _linear_points()
        self.chart.fix_current_curve()
        self.chart.clear_comparison()
        self.assertIsNone(self.chart._fixed_curve)

    def test_get_last_overlays_structure(self):
        ov = self.chart.get_last_overlays()
        self.assertIn("breakevens", ov)
        self.assertIn("pl_at_spot_ref", ov)
        self.assertIsInstance(ov["breakevens"], list)

    def test_title_uses_structure_id(self):
        pts = _linear_points()
        dd  = {"structure_id": "strangle_X", "aba": "old_aba", "decision": "BUY"}
        self.chart.update_chart(pts, decision_data=dd)
        calls = [str(c) for c in self.chart.ax.set_title.call_args_list]
        self.assertTrue(any("strangle_X" in c for c in calls))

    def test_title_fallback_to_aba(self):
        pts = _linear_points()
        dd  = {"aba": "straddle_Y", "decision": "SELL"}
        self.chart.update_chart(pts, decision_data=dd)
        calls = [str(c) for c in self.chart.ax.set_title.call_args_list]
        self.assertTrue(any("straddle_Y" in c for c in calls))

    def test_update_chart_with_tuple_points(self):
        pts    = [(90 + i, -500 + i * 100) for i in range(11)]
        result = self.chart.update_chart(pts)
        self.assertIsInstance(result["breakevens"], list)

    def test_update_chart_with_list_points(self):
        pts    = [[90 + i, -500 + i * 100] for i in range(11)]
        result = self.chart.update_chart(pts)
        self.assertIsInstance(result["breakevens"], list)


# ===========================================================================
# Testes de robustez / edge cases
# ===========================================================================

class TestPayoffChartRobustness(unittest.TestCase):

    def setUp(self):
        self.chart = _make_chart()

    def test_update_chart_none_decision_data(self):
        result = self.chart.update_chart(_linear_points(), decision_data=None)
        self.assertIsNotNone(result)

    def test_update_chart_single_point(self):
        try:
            self.chart.update_chart([{"spot": 100.0, "pl": 0.0}])
        except Exception as e:
            self.fail(f"Lançou exceção com 1 ponto: {e}")

    def test_update_chart_all_zero_pl(self):
        pts    = [{"spot": 90 + i, "pl": 0.0} for i in range(10)]
        result = self.chart.update_chart(pts)
        self.assertIsNotNone(result)

    def test_update_chart_invalid_pl_skipped(self):
        pts = [
            {"spot": 90.0,  "pl": "invalid"},
            {"spot": 100.0, "pl": 500.0},
            {"spot": 110.0, "pl": 1000.0},
        ]
        try:
            result = self.chart.update_chart(pts)
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"Lançou exceção com pl inválido: {e}")

    def test_find_breakevens_constant_positive(self):
        self.assertEqual(
            PayoffChart._find_breakevens(list(range(10)), [100.0] * 10), []
        )

    def test_find_breakevens_single_point(self):
        self.assertEqual(PayoffChart._find_breakevens([100.0], [0.0]), [])

    def test_interp_same_x_values(self):
        result = PayoffChart._interp_y_at_x([100.0, 100.0], [0.0, 500.0], 100.0)
        self.assertIsNone(result)

    def test_fix_and_update_keeps_fixed_curve(self):
        self.chart._last_points = _linear_points()
        self.chart.fix_current_curve()
        fixed_before = self.chart._fixed_curve

        self.chart.update_chart(_linear_points(x_start=85, x_end=115))
        self.assertEqual(self.chart._fixed_curve, fixed_before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
