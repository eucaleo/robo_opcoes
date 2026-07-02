# Inventário técnico da exportação PNG

Data de referência: 2026-07-02

Objetivo:

- localizar implementação existente de exportação PNG;
- localizar objetos de gráfico, figura e canvas usados pela UI atual e pela UI moderna;
- identificar menor ponto seguro para patch futuro;
- não alterar código funcional nesta rodada.

## Escopo

Esta rodada é somente documental.

Não altera:

- código;
- layout;
- callbacks;
- banco;
- contratos canônicos;
- regra de negócio.

## Padrões pesquisados

- png
- savefig
- FigureCanvas
- matplotlib
- filedialog
- asksaveasfilename
- export
- exportar
- salvar
- imagem
- curva
- payoff

## Ocorrências encontradas

| Arquivo | Linha | Padrões | Trecho |
|---|---:|---|---|
| ATT/checks/check_cleanup_residuals.py | 76 | payoff | "scripts/patch_derived_payoff_timestamp_consistency.sh", |
| ATT/checks/check_end_to_end.py | 21 | payoff | ROOT_DIR / "domain" / "payoff.py", |
| ATT/checks/check_end_to_end.py | 22 | payoff | ROOT_DIR / "domain" / "payoff_features.py", |
| ATT/checks/check_end_to_end.py | 36 | payoff | ROOT_DIR / "Scripts" / "build_payoff_summaries.py", |
| ATT/checks/check_structures.py | 22 | payoff | ROOT_DIR / "domain" / "payoff.py", |
| ATT/checks/check_structures.py | 23 | payoff | ROOT_DIR / "domain" / "payoff_features.py", |
| ATT/checks/check_structures.py | 33 | payoff | ROOT_DIR / "Scripts" / "build_payoff_summaries.py", |
| ATT/tests/conftest.py | 264 | filedialog | # filedialog |
| ATT/tests/conftest.py | 265 | filedialog | fd = types.ModuleType("tkinter.filedialog") |
| ATT/tests/conftest.py | 267 | asksaveasfilename | fd.asksaveasfilename = MagicMock(return_value="") |
| ATT/tests/conftest.py | 269 | filedialog | tk_mock.filedialog  = fd |
| ATT/tests/conftest.py | 285 | filedialog | sys.modules.setdefault("tkinter.filedialog",   _fd) |
| ATT/tests/test_decision.py | 1 | payoff | from domain.decision import compute_decision_from_payoff |
| ATT/tests/test_decision.py | 4 | payoff | def test_compute_decision_from_payoff_should_work_without_alias_legacy_aba(): |
| ATT/tests/test_decision.py | 6 | payoff | Garante que compute_decision_from_payoff funciona com payoff canônico |
| ATT/tests/test_decision.py | 9 | payoff | payoff = { |
| ATT/tests/test_decision.py | 17 | payoff | result = compute_decision_from_payoff( |
| ATT/tests/test_decision.py | 18 | payoff | payoff=payoff, |
| ATT/tests/test_derived_service.py | 86 | payoff | def test_save_payoff_from_canonical_payload_should_use_resolved_storage_key(monkeypatch): |
| ATT/tests/test_derived_service.py | 89 | payoff | def fake_save_payoff_curve(ref, points, spot_ref=None, meta=None, timestamp=None): |
| ATT/tests/test_derived_service.py | 97 | payoff | monkeypatch.setattr(ds, "save_payoff_curve", fake_save_payoff_curve) |
| ATT/tests/test_derived_service.py | 110 | payoff | result = ds.save_payoff_from_canonical_payload(payload) |
| ATT/tests/test_orchestrator_run_methods.py | 2 | payoff | Testes para os métodos run_payoff e run_decision |
| ATT/tests/test_orchestrator_run_methods.py | 16 | payoff | _request_to_payoff_dict, |
| ATT/tests/test_orchestrator_run_methods.py | 18 | payoff | run_payoff, |
| ATT/tests/test_orchestrator_run_methods.py | 64 | payoff | # Testes: _request_to_payoff_dict |
| ATT/tests/test_orchestrator_run_methods.py | 67 | payoff | class TestRequestToPayoffDict: |
| ATT/tests/test_orchestrator_run_methods.py | 71 | payoff | result = _request_to_payoff_dict(req) |
| ATT/tests/test_orchestrator_run_methods.py | 76 | payoff | s = _request_to_payoff_dict(req)["structure"] |
| ATT/tests/test_orchestrator_run_methods.py | 86 | payoff | legs = _request_to_payoff_dict(req)["structure"]["legs"] |
| ATT/tests/test_orchestrator_run_methods.py | 93 | payoff | m = _request_to_payoff_dict(req)["market"] |
| ATT/tests/test_orchestrator_run_methods.py | 100 | payoff | result = _request_to_payoff_dict(req, extra_meta=meta) |
| ATT/tests/test_orchestrator_run_methods.py | 105 | payoff | result = _request_to_payoff_dict(req) |
| ATT/tests/test_orchestrator_run_methods.py | 114 | payoff | result_legs = _request_to_payoff_dict(req)["structure"]["legs"] |
| ATT/tests/test_orchestrator_run_methods.py | 120 | payoff | # Testes: run_payoff |
| ATT/tests/test_orchestrator_run_methods.py | 123 | payoff | class TestRunPayoff: |
| ATT/tests/test_orchestrator_run_methods.py | 125 | payoff | @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input") |
| ATT/tests/test_orchestrator_run_methods.py | 130 | payoff | result = run_payoff(req) |
| ATT/tests/test_orchestrator_run_methods.py | 138 | payoff | @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input") |
| ATT/tests/test_orchestrator_run_methods.py | 143 | payoff | run_payoff(req, low_pct=0.8, high_pct=1.2, step_pct=0.005) |
| ATT/tests/test_orchestrator_run_methods.py | 150 | payoff | @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input") |
| ATT/tests/test_orchestrator_run_methods.py | 155 | payoff | run_payoff(req, extra_meta={"tag": "ci"}) |
| ATT/tests/test_orchestrator_run_methods.py | 160 | payoff | @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input") |
| ATT/tests/test_orchestrator_run_methods.py | 166 | payoff | result = run_payoff(req) |
| ATT/tests/test_orchestrator_run_methods.py | 192 | payoff | def test_payoff_dict_repassado(self, mock_decide): |
| ATT/tests/test_orchestrator_run_methods.py | 195 | payoff | payoff = {"pl_max": 600.0, "points": [{"spot": 50, "pl": 0}]} |
| ATT/tests/test_orchestrator_run_methods.py | 197 | payoff | run_decision(req, payoff=payoff, pl_max=600.0, pl_atual=100.0) |
| ATT/tests/test_orchestrator_run_methods.py | 200 | payoff | assert kwargs["payoff"] == payoff |
| ATT/tests/test_orchestrator_run_methods.py | 239 | payoff | class TestRunPayoffIntegration: |
| ATT/tests/test_orchestrator_run_methods.py | 241 | payoff | Chama run_payoff sem mock. |
| ATT/tests/test_orchestrator_run_methods.py | 245 | payoff | def test_sanidade_run_payoff_call_chain(self): |
| ATT/tests/test_orchestrator_run_methods.py | 246 | payoff | pytest.importorskip("domain.payoff") |
| ATT/tests/test_orchestrator_run_methods.py | 260 | payoff | result = run_payoff(req, low_pct=0.8, high_pct=1.2, step_pct=0.05) |
| ATT/tests/test_orchestrator_run_methods.py | 261 | payoff | assert isinstance(result, dict), "run_payoff deve retornar dict" |
| ATT/tests/test_payoff_canonical.py | 1 | payoff | from domain.payoff import compute_payoff_from_canonical_input |
| ATT/tests/test_payoff_canonical.py | 4 | payoff | def test_compute_payoff_from_canonical_input_should_preserve_canonical_metadata(): |
| ATT/tests/test_payoff_canonical.py | 37 | payoff | result = compute_payoff_from_canonical_input(canonical_input) |
| ATT/tests/test_payoff_chart.py | 1 | payoff | # C:/users/eucal/projeto/ATT/tests/test_payoff_chart.py |
| ATT/tests/test_payoff_chart.py | 3 | payoff | Testes unitários para UI/components/payoff_chart.py |
| ATT/tests/test_payoff_chart.py | 9 | payoff | - PayoffChart.clear() |
| ATT/tests/test_payoff_chart.py | 10 | payoff | - PayoffChart.update_chart() |
| ATT/tests/test_payoff_chart.py | 11 | payoff | - PayoffChart.fix_current_curve() / clear_comparison() |
| ATT/tests/test_payoff_chart.py | 12 | payoff | - PayoffChart.get_last_overlays() |
| ATT/tests/test_payoff_chart.py | 36 | matplotlib | "matplotlib":                        MagicMock(), |
| ATT/tests/test_payoff_chart.py | 37 | matplotlib | "matplotlib.use":                    MagicMock(), |
| ATT/tests/test_payoff_chart.py | 38 | matplotlib | "matplotlib.figure":                 MagicMock(), |
| ATT/tests/test_payoff_chart.py | 39 | matplotlib | "matplotlib.ticker":                 MagicMock(), |
| ATT/tests/test_payoff_chart.py | 40 | matplotlib | "matplotlib.backends":               MagicMock(), |
| ATT/tests/test_payoff_chart.py | 41 | matplotlib | "matplotlib.backends.backend_tkagg": MagicMock(), |
| ATT/tests/test_payoff_chart.py | 48 | matplotlib | sys.modules["matplotlib.ticker"].FuncFormatter = lambda f: f |
| ATT/tests/test_payoff_chart.py | 51 | payoff | from UI.components.payoff_chart import (  # noqa: E402 |
| ATT/tests/test_payoff_chart.py | 52 | payoff | PayoffChart, |
| ATT/tests/test_payoff_chart.py | 60 | payoff | # Fixture: instância de PayoffChart com Tk fake |
| ATT/tests/test_payoff_chart.py | 63 | payoff | def _make_chart() -> PayoffChart: |
| ATT/tests/test_payoff_chart.py | 64 | payoff | """Cria PayoffChart com dependências Tk mockadas.""" |
| ATT/tests/test_payoff_chart.py | 65 | FigureCanvas, payoff | with patch("UI.components.payoff_chart.FigureCanvasTkAgg"), \ |
| ATT/tests/test_payoff_chart.py | 66 | payoff | patch("UI.components.payoff_chart.NavigationToolbar2Tk"), \ |
| ATT/tests/test_payoff_chart.py | 67 | payoff | patch("UI.components.payoff_chart.Figure") as MockFig, \ |
| ATT/tests/test_payoff_chart.py | 68 | payoff | patch("UI.components.payoff_chart.ttk.Frame.__init__", return_value=None), \ |
| ATT/tests/test_payoff_chart.py | 69 | payoff | patch("UI.components.payoff_chart.ttk.Frame.pack",     return_value=None), \ |
| ATT/tests/test_payoff_chart.py | 70 | payoff | patch("UI.components.payoff_chart.ttk.Frame.bind",     return_value=None): |
| ATT/tests/test_payoff_chart.py | 77 | payoff | chart = PayoffChart.__new__(PayoffChart) |
| ATT/tests/test_payoff_chart.py | 171 | payoff | return PayoffChart._find_breakevens(spots, pls) |
| ATT/tests/test_payoff_chart.py | 225 | payoff | return PayoffChart._interp_y_at_x(xs, ys, x) |
| ATT/tests/test_payoff_chart.py | 305 | payoff | # Testes de PayoffChart (estado e lógica) |
| ATT/tests/test_payoff_chart.py | 308 | payoff | class TestPayoffChartState(unittest.TestCase): |
| ATT/tests/test_payoff_chart.py | 374 | curva | self.assertIn("Curva A", self.chart._fixed_curve["label"]) |
| ATT/tests/test_payoff_chart.py | 422 | payoff | class TestPayoffChartRobustness(unittest.TestCase): |
| ATT/tests/test_payoff_chart.py | 456 | payoff | PayoffChart._find_breakevens(list(range(10)), [100.0] * 10), [] |
| ATT/tests/test_payoff_chart.py | 460 | payoff | self.assertEqual(PayoffChart._find_breakevens([100.0], [0.0]), []) |
| ATT/tests/test_payoff_chart.py | 463 | payoff | result = PayoffChart._interp_y_at_x([100.0, 100.0], [0.0, 500.0], 100.0) |
| ATT/tests/test_pricing_execution_persistence_service.py | 220 | payoff | "payoff": { |
| ATT/tests/test_pricing_execution_persistence_service.py | 258 | payoff | assert call["payoff_json"] == { |
| ATT/tests/test_structure_analysis_service.py | 124 | payoff | assert "payoff" in result |
| ATT/tests/test_structure_analysis_service.py | 134 | payoff | payoff = result["payoff"] |
| ATT/tests/test_structure_analysis_service.py | 135 | payoff | assert payoff is not None |
| ATT/tests/test_structure_analysis_service.py | 136 | payoff | assert payoff["pl_max"] == 10000.0 |
| ATT/tests/test_structure_analysis_service.py | 137 | payoff | assert payoff["spot_ref"] == 198.35 |
| ATT/tests/test_structure_analysis_service.py | 138 | payoff | assert "points" in payoff |
| ATT/tests/test_structure_analysis_service.py | 139 | payoff | assert len(payoff["points"]) > 0 |
| ATT/tests/test_structure_analysis_service.py | 169 | payoff | def test_structure_analysis_service_analyze_returns_structured_decision_for_invalid_payoff(): |
| ATT/tests/test_structure_analysis_service.py | 179 | payoff | assert "payoff" in result |
| ATT/tests/test_structure_analysis_service.py | 184 | payoff | assert result["decision"]["why"]["error"] == "payoff is required" |
| ATT/tests/test_structure_analysis_service.py | 273 | payoff | def fake_compute_payoff_from_canonical_input(canonical_input): |
| ATT/tests/test_structure_analysis_service.py | 276 | payoff | def fake_compute_decision_from_payoff( |
| ATT/tests/test_structure_analysis_service.py | 277 | payoff | payoff, |
| ATT/tests/test_structure_analysis_service.py | 283 | payoff | captured["payoff"] = payoff |
| ATT/tests/test_structure_analysis_service.py | 300 | payoff | "services.structure_analysis_service.compute_payoff_from_canonical_input", |
| ATT/tests/test_structure_analysis_service.py | 301 | payoff | fake_compute_payoff_from_canonical_input, |
| ATT/tests/test_structure_analysis_service.py | 304 | payoff | "services.structure_analysis_service.compute_decision_from_payoff", |
| ATT/tests/test_structure_analysis_service.py | 305 | payoff | fake_compute_decision_from_payoff, |
| ATT/tests/test_structure_analysis_service.py | 316 | payoff | "payoff": {"pl_max": 1.0, "spot_ref": 198.35, "points": []}, |
| ATT/tests/test_structure_analysis_service.py | 336 | payoff | def fake_compute_payoff_from_canonical_input(canonical_input): |
| ATT/tests/test_structure_analysis_service.py | 339 | payoff | def fake_compute_decision_from_payoff( |
| ATT/tests/test_structure_analysis_service.py | 340 | payoff | payoff, |
| ATT/tests/test_structure_analysis_service.py | 358 | payoff | "services.structure_analysis_service.compute_payoff_from_canonical_input", |
| ATT/tests/test_structure_analysis_service.py | 359 | payoff | fake_compute_payoff_from_canonical_input, |
| ATT/tests/test_structure_analysis_service.py | 362 | payoff | "services.structure_analysis_service.compute_decision_from_payoff", |
| ATT/tests/test_structure_analysis_service.py | 363 | payoff | fake_compute_decision_from_payoff, |
| ATT/tests/test_structure_analysis_service.py | 384 | payoff | def fake_compute_payoff_from_canonical_input(canonical_input): |
| ATT/tests/test_structure_analysis_service.py | 387 | payoff | def fake_compute_decision_from_payoff( |
| ATT/tests/test_structure_analysis_service.py | 388 | payoff | payoff, |
| ATT/tests/test_structure_analysis_service.py | 407 | payoff | "services.structure_analysis_service.compute_payoff_from_canonical_input", |
| ATT/tests/test_structure_analysis_service.py | 408 | payoff | fake_compute_payoff_from_canonical_input, |
| ATT/tests/test_structure_analysis_service.py | 411 | payoff | "services.structure_analysis_service.compute_decision_from_payoff", |
| ATT/tests/test_structure_analysis_service.py | 412 | payoff | fake_compute_decision_from_payoff, |
| ATT/tests/test_structure_analysis_service.py | 504 | payoff | def fake_compute_payoff_from_canonical_input(canonical_input): |
| ATT/tests/test_structure_analysis_service.py | 507 | payoff | def fake_compute_decision_from_payoff( |
| ATT/tests/test_structure_analysis_service.py | 508 | payoff | payoff, |
| ATT/tests/test_structure_analysis_service.py | 523 | payoff | "services.structure_analysis_service.compute_payoff_from_canonical_input", |
| ATT/tests/test_structure_analysis_service.py | 524 | payoff | fake_compute_payoff_from_canonical_input, |
| ATT/tests/test_structure_analysis_service.py | 527 | payoff | "services.structure_analysis_service.compute_decision_from_payoff", |
| ATT/tests/test_structure_analysis_service.py | 528 | payoff | fake_compute_decision_from_payoff, |
| ATT/tests/test_structure_analysis_service.py | 550 | payoff | def fake_compute_payoff_from_canonical_input(canonical_input): |
| ATT/tests/test_structure_analysis_service.py | 553 | payoff | def fake_compute_decision_from_payoff( |
| ATT/tests/test_structure_analysis_service.py | 554 | payoff | payoff, |
| ATT/tests/test_structure_analysis_service.py | 569 | payoff | "services.structure_analysis_service.compute_payoff_from_canonical_input", |
| ATT/tests/test_structure_analysis_service.py | 570 | payoff | fake_compute_payoff_from_canonical_input, |
| ATT/tests/test_structure_analysis_service.py | 573 | payoff | "services.structure_analysis_service.compute_decision_from_payoff", |
| ATT/tests/test_structure_analysis_service.py | 574 | payoff | fake_compute_decision_from_payoff, |
| ATT/tests/test_structure_analysis_service.py | 597 | payoff | def fake_compute_payoff_from_canonical_input(canonical_input): |
| ATT/tests/test_structure_analysis_service.py | 600 | payoff | def fake_compute_decision_from_payoff( |
| ATT/tests/test_structure_analysis_service.py | 601 | payoff | payoff, |
| ATT/tests/test_structure_analysis_service.py | 615 | payoff | "services.structure_analysis_service.compute_payoff_from_canonical_input", |
| ATT/tests/test_structure_analysis_service.py | 616 | payoff | fake_compute_payoff_from_canonical_input, |
| ATT/tests/test_structure_analysis_service.py | 619 | payoff | "services.structure_analysis_service.compute_decision_from_payoff", |
| ATT/tests/test_structure_analysis_service.py | 620 | payoff | fake_compute_decision_from_payoff, |
| ATT/tests/test_structure_editor_integration.py | 18 | matplotlib | # Stubs de tkinter + matplotlib |
| ATT/tests/test_structure_editor_integration.py | 144 | filedialog | for _sub_name in ("font", "messagebox", "ttk", "filedialog", |
| ATT/tests/test_structure_editor_integration.py | 171 | matplotlib | # Matplotlib stubs (inalterado) |
| ATT/tests/test_structure_editor_integration.py | 173 | matplotlib | "matplotlib", |
| ATT/tests/test_structure_editor_integration.py | 174 | matplotlib | "matplotlib.backends", |
| ATT/tests/test_structure_editor_integration.py | 175 | matplotlib | "matplotlib.backends.backend_tkagg", |
| ATT/tests/test_structure_editor_integration.py | 176 | matplotlib | "matplotlib.backends._backend_tk", |
| ATT/tests/test_structure_editor_integration.py | 177 | matplotlib | "matplotlib.figure", |
| ATT/tests/test_structure_editor_integration.py | 178 | matplotlib | "matplotlib.pyplot", |
| ATT/tests/test_structure_editor_integration.py | 179 | matplotlib | "matplotlib.axes", |
| ATT/tests/test_structure_editor_integration.py | 180 | matplotlib | "matplotlib.axes._axes", |
| ATT/tests/test_structure_editor_integration.py | 181 | matplotlib | "matplotlib.ticker", |
| ATT/tests/test_structure_editor_integration.py | 182 | matplotlib | "matplotlib.lines", |
| ATT/tests/test_structure_editor_integration.py | 183 | matplotlib | "matplotlib.patches", |
| ATT/tests/test_structure_editor_integration.py | 184 | matplotlib | "matplotlib.colors", |
| ATT/tests/test_structure_editor_integration.py | 185 | matplotlib | "matplotlib.collections", |
| ATT/tests/test_structure_editor_integration.py | 186 | matplotlib | "matplotlib.legend", |
| ATT/tests/test_structure_editor_integration.py | 187 | matplotlib | "matplotlib.text", |
| ATT/tests/test_structure_editor_integration.py | 188 | matplotlib | "matplotlib.artist", |
| ATT/tests/test_structure_editor_integration.py | 189 | matplotlib | "matplotlib.font_manager", |
| ATT/tests/test_structure_editor_integration.py | 190 | matplotlib | "matplotlib.image", |
| ATT/tests/test_structure_editor_integration.py | 191 | matplotlib | "matplotlib.cm", |
| ATT/tests/test_structure_editor_integration.py | 192 | matplotlib | "matplotlib.transforms", |
| ATT/tests/test_structure_editor_integration.py | 193 | matplotlib | "matplotlib.path", |
| ATT/tests/test_structure_editor_integration.py | 194 | matplotlib | "matplotlib.widgets", |
| ATT/tests/test_structure_editor_integration.py | 195 | matplotlib | "matplotlib.gridspec", |
| ATT/tests/test_structure_editor_integration.py | 196 | matplotlib | "matplotlib.style", |
| ATT/tests/test_structure_editor_integration.py | 202 | matplotlib | _mpl_full.__name__  = "matplotlib" |
| ATT/tests/test_structure_editor_integration.py | 205 | matplotlib | sys.modules["matplotlib"] = _mpl_full |
| ATT/tests/test_structure_editor_integration.py | 210 | matplotlib | _child = sys.modules.get(f"matplotlib.{_sub}", types.ModuleType(f"matplotlib.{_sub}")) |
| ATT/tests/test_structure_editor_integration.py | 211 | matplotlib | sys.modules[f"matplotlib.{_sub}"] = _child |
| ATT/tests/test_structure_editor_integration.py | 214 | matplotlib | _mpl_stub = sys.modules["matplotlib"] |
| ATT/tests/test_structure_editor_integration.py | 221 | matplotlib | mpl_tk = sys.modules["matplotlib.backends.backend_tkagg"] |
| ATT/tests/test_structure_editor_integration.py | 222 | FigureCanvas | if not hasattr(mpl_tk, "FigureCanvasTkAgg"): |
| ATT/tests/test_structure_editor_integration.py | 223 | FigureCanvas | mpl_tk.FigureCanvasTkAgg    = MagicMock |
| ATT/tests/test_structure_editor_integration.py | 226 | matplotlib | fig_mod = sys.modules["matplotlib.figure"] |
| ATT/tests/test_structure_editor_integration.py | 230 | matplotlib | ticker = sys.modules["matplotlib.ticker"] |
| ATT/tests/test_structure_editor_integration.py | 237 | matplotlib | mpl = sys.modules["matplotlib"] |
| ATT/tests/test_structure_editor_integration.py | 242 | matplotlib | setattr(mpl, _sub, sys.modules.get(f"matplotlib.{_sub}", |
| ATT/tests/test_structure_editor_integration.py | 243 | matplotlib | types.ModuleType(f"matplotlib.{_sub}"))) |
| ATT/tests/test_structure_editor_integration.py | 459 | salvar | def test_destroy_chamado_apos_salvar(self): |
| ATT/tests/test_system_snapshots_repository.py | 120 | payoff | payoff_json={"max_gain": 1000}, |
| ATT/tests/test_system_snapshots_repository.py | 167 | payoff | assert snapshot["payoff_json"] == {"max_gain": 1000} |
| ATT/tests/test_system_snapshots_schema.py | 68 | payoff | "payoff_json", |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 3 | payoff | from services.terminal_vwap_payoff_app_service import TerminalVWAPPayoffAppService |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 35 | payoff | class FakePayoffProvider: |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 39 | payoff | def compute_payoff(self, structure, market, reference_date=None): |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 53 | payoff | "meta": {"source": "fake_payoff"}, |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 61 | payoff | def build(self, structure, market, payoff_points, payoff=None): |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 66 | payoff | "payoff_points": payoff_points, |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 67 | payoff | "payoff": payoff, |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 72 | payoff | "name": "ui-terminal-vwap-payoff", |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 77 | payoff | "payoff": { |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 78 | payoff | "points_count": len(payoff_points), |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 84 | payoff | def build_terminal_vwap_payoff_viewmodel( |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 88 | payoff | payoff_points, |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 93 | payoff | "points_count": len(payoff_points), |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 118 | payoff | def test_build_for_structure_id_orchestrates_structure_market_payoff_and_viewmodel(): |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 121 | payoff | payoff_provider = FakePayoffProvider() |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 124 | payoff | service = TerminalVWAPPayoffAppService( |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 127 | payoff | payoff_provider=payoff_provider, |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 133 | payoff | assert result["terminal"]["name"] == "ui-terminal-vwap-payoff" |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 137 | payoff | assert result["payoff"]["points_count"] == 3 |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 142 | payoff | assert payoff_provider.calls[0]["market"]["source"] == "fake_market" |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 146 | payoff | assert len(vm_call["payoff_points"]) == 3 |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 147 | payoff | assert vm_call["payoff"]["meta"]["source"] == "fake_payoff" |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 151 | payoff | service = TerminalVWAPPayoffAppService( |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 154 | payoff | payoff_provider=FakePayoffProvider(), |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 163 | payoff | service = TerminalVWAPPayoffAppService( |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 166 | payoff | payoff_provider=FakePayoffProvider(), |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | 180 | payoff | service = TerminalVWAPPayoffAppService( |
| ATT/tests/test_terminal_vwap_payoff_controller.py | 3 | payoff | from controllers.terminal_vwap_payoff_controller import ( |
| ATT/tests/test_terminal_vwap_payoff_controller.py | 4 | payoff | TerminalVWAPPayoffController, |
| ATT/tests/test_terminal_vwap_payoff_controller.py | 8 | payoff | class FakeTerminalVWAPPayoffAppService: |
| ATT/tests/test_terminal_vwap_payoff_controller.py | 32 | payoff | "name": "ui-terminal-vwap-payoff", |
| ATT/tests/test_terminal_vwap_payoff_controller.py | 45 | payoff | app_service = FakeTerminalVWAPPayoffAppService() |
| ATT/tests/test_terminal_vwap_payoff_controller.py | 46 | payoff | controller = TerminalVWAPPayoffController(app_service) |
| ATT/tests/test_terminal_vwap_payoff_controller.py | 51 | payoff | assert result["terminal"]["name"] == "ui-terminal-vwap-payoff" |
| ATT/tests/test_terminal_vwap_payoff_controller.py | 57 | payoff | app_service = FakeTerminalVWAPPayoffAppService() |
| ATT/tests/test_terminal_vwap_payoff_controller.py | 58 | payoff | controller = TerminalVWAPPayoffController(app_service) |
| ATT/tests/test_terminal_vwap_payoff_controller.py | 73 | payoff | controller = TerminalVWAPPayoffController( |
| ATT/tests/test_terminal_vwap_payoff_controller.py | 74 | payoff | FakeTerminalVWAPPayoffAppService() |
| ATT/tests/test_terminal_vwap_payoff_controller.py | 82 | payoff | controller = TerminalVWAPPayoffController( |
| ATT/tests/test_terminal_vwap_payoff_controller.py | 83 | payoff | FakeTerminalVWAPPayoffAppService() |
| ATT/tests/test_terminal_vwap_payoff_controller.py | 111 | payoff | controller = TerminalVWAPPayoffController(AppServiceWithoutListing()) |
| ATT/tests/test_terminal_vwap_payoff_controller.py | 118 | payoff | TerminalVWAPPayoffController(None) |
| ATT/tests/test_terminal_vwap_payoff_panel.py | 1 | payoff | from UI.components.terminal_vwap_payoff_panel import ( |
| ATT/tests/test_terminal_vwap_payoff_panel.py | 3 | payoff | _extract_payoff_table_rows, |
| ATT/tests/test_terminal_vwap_payoff_panel.py | 38 | payoff | "payoff": { |
| ATT/tests/test_terminal_vwap_payoff_panel.py | 93 | payoff | def test_terminal_panel_extracts_payoff_rows_without_tk_display(): |
| ATT/tests/test_terminal_vwap_payoff_panel.py | 94 | payoff | rows = _extract_payoff_table_rows(_viewmodel()) |
| ATT/tests/test_terminal_vwap_payoff_panel.py | 103 | payoff | def test_terminal_panel_extracts_limited_payoff_rows(): |
| ATT/tests/test_terminal_vwap_payoff_panel.py | 104 | payoff | rows = _extract_payoff_table_rows(_viewmodel(), limit=2) |
| ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | 1 | payoff | from services.terminal_vwap_payoff_viewmodel_service import ( |
| ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | 2 | payoff | TerminalVWAPPayoffViewModelService, |
| ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | 6 | payoff | def test_build_terminal_vwap_payoff_viewmodel_with_vwap_and_payoff_points(): |
| ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | 7 | payoff | service = TerminalVWAPPayoffViewModelService() |
| ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | 34 | payoff | payoff_points=[ |
| ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | 42 | payoff | assert result["terminal"]["name"] == "ui-terminal-vwap-payoff" |
| ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | 58 | payoff | assert result["payoff"]["points_count"] == 3 |
| ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | 59 | payoff | assert result["payoff"]["min_result"] == -100.0 |
| ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | 60 | payoff | assert result["payoff"]["max_result"] == 100.0 |
| ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | 61 | payoff | assert result["payoff"]["break_even_points"] == [10.0] |
| ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | 67 | payoff | def test_build_terminal_vwap_payoff_viewmodel_handles_missing_vwap_and_empty_payoff(): |
| ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | 68 | payoff | service = TerminalVWAPPayoffViewModelService() |
| ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | 80 | payoff | payoff_points=[], |
| ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | 89 | payoff | assert result["payoff"]["points_count"] == 0 |
| ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | 90 | payoff | assert result["payoff"]["break_even_points"] == [] |
| ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | 94 | payoff | assert "payoff sem pontos" in result["meta"]["warnings"] |
| ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | 97 | payoff | def test_build_terminal_vwap_payoff_viewmodel_estimates_interpolated_break_even(): |
| ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | 98 | payoff | service = TerminalVWAPPayoffViewModelService() |
| ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | 109 | payoff | payoff_points=[ |
| ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | 115 | payoff | assert result["payoff"]["break_even_points"] == [100.0] |
| ATT/tests/test_ui_data_migration.py | 167 | payoff | # Nível 4 -- get_payoff_curve_info() |
| ATT/tests/test_ui_data_migration.py | 170 | payoff | def test_payoff_curve_info_retorna_dados(model, non_empty_decisions): |
| ATT/tests/test_ui_data_migration.py | 172 | payoff | pts, info = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"]) |
| ATT/tests/test_ui_data_migration.py | 173 | payoff | assert isinstance(pts, list), "Pontos do payoff devem ser uma lista" |
| ATT/tests/test_ui_data_migration.py | 174 | payoff | assert isinstance(info, dict), "info do payoff deve ser dict" |
| ATT/tests/test_ui_data_migration.py | 177 | payoff | def test_payoff_curve_info_tem_structure_id(model, non_empty_decisions): |
| ATT/tests/test_ui_data_migration.py | 179 | payoff | _, info = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"]) |
| ATT/tests/test_ui_data_migration.py | 180 | payoff | assert "structure_id" in info, "info do payoff deve conter 'structure_id'" |
| ATT/tests/test_ui_data_migration.py | 183 | payoff | def test_payoff_curve_info_aba_continuidade(model, non_empty_decisions): |
| ATT/tests/test_ui_data_migration.py | 185 | payoff | _, info = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"]) |
| ATT/tests/test_ui_data_migration.py | 186 | payoff | assert "aba" in info, "info do payoff deve ainda conter 'aba' (continuidade)" |
| ATT/tests/test_ui_data_migration.py | 192 | payoff | def test_payoff_curve_info_pontos_validos(model, non_empty_decisions): |
| ATT/tests/test_ui_data_migration.py | 194 | payoff | pts, _ = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"]) |
| controllers/terminal_vwap_payoff_controller.py | 1 | payoff | """Controller do Terminal VWAP Payoff. |
| controllers/terminal_vwap_payoff_controller.py | 17 | payoff | class TerminalVWAPPayoffController: |
| controllers/terminal_vwap_payoff_controller.py | 18 | payoff | """Controller fino para seleção e carga do Terminal VWAP Payoff.""" |
| create_payoff_summary_table.py | 4 | payoff | CREATE TABLE IF NOT EXISTS payoff_curve_summary ( |
| create_payoff_summary_table.py | 23 | payoff | CREATE INDEX IF NOT EXISTS idx_payoff_curve_summary_aba_ts |
| create_payoff_summary_table.py | 24 | payoff | ON payoff_curve_summary (aba, timestamp); |
| create_payoff_summary_table.py | 28 | payoff | print("Tabela payoff_curve_summary criada.") |
| db/derived_repo.py | 3 | payoff | Repositório para operações com dados derivados (payoff e decisões). |
| db/derived_repo.py | 4 | payoff | Tabelas: payoff_curve_points, structure_decisions |
| db/derived_repo.py | 6 | payoff | Contrato canônico payoff: point_spot / point_pl (opção B). |
| db/derived_repo.py | 19 | payoff | - fix: _DDL_PAYOFF_IDX -> _DDL_PAYOFF_IDX_STRUCTURE |
| db/derived_repo.py | 20 | payoff | - fix: existing_payoff_cols -> existing_cols |
| db/derived_repo.py | 42 | payoff | PayoffPoint = Union[Tuple[float, float], Dict[str, float]] |
| db/derived_repo.py | 74 | payoff | # alteracao_36_A: adicionar structure_id ao DDL de payoff_curve_points |
| db/derived_repo.py | 76 | payoff | _DDL_PAYOFF_CURVE_POINTS = """ |
| db/derived_repo.py | 77 | payoff | CREATE TABLE IF NOT EXISTS payoff_curve_points ( |
| db/derived_repo.py | 89 | payoff | _DDL_PAYOFF_UNIQUE_IDX = """ |
| db/derived_repo.py | 90 | payoff | CREATE UNIQUE INDEX IF NOT EXISTS ux_payoff_snapshot |
| db/derived_repo.py | 91 | payoff | ON payoff_curve_points (timestamp, aba, point_spot) |
| db/derived_repo.py | 95 | payoff | _DDL_PAYOFF_IDX_STRUCTURE = """ |
| db/derived_repo.py | 96 | payoff | CREATE INDEX IF NOT EXISTS ix_payoff_structure_id |
| db/derived_repo.py | 97 | payoff | ON payoff_curve_points (structure_id, timestamp) |
| db/derived_repo.py | 136 | payoff | _PAYOFF_MIGRATIONS: Dict[str, str] = { |
| db/derived_repo.py | 138 | payoff | "ALTER TABLE payoff_curve_points ADD COLUMN structure_id INTEGER" |
| db/derived_repo.py | 173 | payoff | conn.execute(_DDL_PAYOFF_CURVE_POINTS) |
| db/derived_repo.py | 174 | payoff | conn.execute(_DDL_PAYOFF_UNIQUE_IDX) |
| db/derived_repo.py | 177 | payoff | # alteracao_36_A: migration incremental payoff_curve_points |
| db/derived_repo.py | 178 | payoff | existing_cols = _table_columns(conn, "payoff_curve_points") |
| db/derived_repo.py | 179 | payoff | for col, sql in _PAYOFF_MIGRATIONS.items(): |
| db/derived_repo.py | 186 | payoff | # alteracao_36_B: index structure_id no payoff (após migration) |
| db/derived_repo.py | 188 | payoff | conn.execute(_DDL_PAYOFF_IDX_STRUCTURE) |
| db/derived_repo.py | 218 | payoff | alteracao_56: correções de bugs em _apply_schema e INSERTs do payoff. |
| db/derived_repo.py | 329 | payoff | # Escrita -- payoff |
| db/derived_repo.py | 332 | payoff | def write_payoff_snapshot_atomic( |
| db/derived_repo.py | 334 | payoff | points: List[PayoffPoint], |
| db/derived_repo.py | 354 | payoff | "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?", |
| db/derived_repo.py | 359 | payoff | INSERT INTO payoff_curve_points |
| db/derived_repo.py | 382 | payoff | def insert_payoff_points( |
| db/derived_repo.py | 384 | payoff | points: List[PayoffPoint], |
| db/derived_repo.py | 402 | payoff | INSERT OR REPLACE INTO payoff_curve_points |
| db/derived_repo.py | 431 | payoff | points: List[PayoffPoint], |
| db/derived_repo.py | 446 | payoff | # --- payoff --- |
| db/derived_repo.py | 448 | payoff | "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?", |
| db/derived_repo.py | 453 | payoff | INSERT INTO payoff_curve_points |
| db/derived_repo.py | 488 | payoff | def get_payoff_points( |
| db/derived_repo.py | 500 | payoff | FROM payoff_curve_points |
| db/derived_repo.py | 510 | payoff | FROM payoff_curve_points |
| db/derived_repo.py | 521 | payoff | FROM payoff_curve_points |
| db/derived_repo.py | 580 | payoff | LEFT JOIN payoff_curve_points p |
| db/derived_repo.py | 588 | payoff | FROM payoff_curve_points p |
| db/derived_repo.py | 607 | payoff | def cleanup_old_payoff_data(self, days_to_keep: int = 30) -> int: |
| db/derived_repo.py | 611 | payoff | f"DELETE FROM payoff_curve_points " |
| db/derived_repo.py | 676 | payoff | def write_payoff_snapshot_atomic( |
| db/derived_repo.py | 691 | payoff | "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?", |
| db/derived_repo.py | 695 | payoff | INSERT INTO payoff_curve_points |
| db/derived_repo.py | 764 | payoff | pc  = write_payoff_snapshot_atomic(conn, timestamp, aba, points, points_meta, structure_id=decision_dict.get("structure_id")) |
| db/derived_repo.py | 769 | payoff | def insert_payoff_points( |
| db/derived_repo.py | 773 | payoff | points: List[PayoffPoint], |
| db/derived_repo.py | 785 | payoff | INSERT OR REPLACE INTO payoff_curve_points |
| db/derived_repo.py | 841 | payoff | def get_payoff_points( |
| db/derived_repo.py | 852 | payoff | FROM payoff_curve_points |
| db/derived_repo.py | 859 | payoff | FROM payoff_curve_points |
| db/derived_repo.py | 867 | payoff | FROM payoff_curve_points |
| db/derived_repo.py | 881 | payoff | LEFT JOIN payoff_curve_points p ON (d.aba = p.aba AND d.timestamp = p.timestamp) |
| db/derived_repo.py | 888 | payoff | FROM payoff_curve_points p |
| db/derived_repo.py | 905 | payoff | def cleanup_old_payoff_data(conn: sqlite3.Connection, days_to_keep: int = 30) -> int: |
| db/derived_repo.py | 909 | payoff | DELETE FROM payoff_curve_points |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 1 | payoff | # db/migrations/add_structure_id_to_payoff_curve_points.py |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 3 | payoff | Migration: adiciona structure_id em payoff_curve_points |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 4 | payoff | e payoff_curve_summary, com backfill via structure_decisions. |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 7 | payoff | python db/migrations/add_structure_id_to_payoff_curve_points.py |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 8 | payoff | python db/migrations/add_structure_id_to_payoff_curve_points.py --db dados/derived.db |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 18 | payoff | #  payoff_curve_points |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 20 | payoff | "payoff_curve_points: verificar se structure_id já existe", |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 24 | payoff | "payoff_curve_points: ADD COLUMN structure_id", |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 25 | payoff | "ALTER TABLE payoff_curve_points ADD COLUMN structure_id INTEGER", |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 28 | payoff | "payoff_curve_points: BACKFILL structure_id", |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 30 | payoff | UPDATE payoff_curve_points |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 34 | payoff | WHERE d.aba       = payoff_curve_points.aba |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 35 | payoff | AND d.timestamp = payoff_curve_points.timestamp |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 41 | payoff | "payoff_curve_points: CREATE INDEX sid+ts", |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 43 | payoff | CREATE INDEX IF NOT EXISTS idx_payoff_points_sid_ts |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 44 | payoff | ON payoff_curve_points (structure_id, timestamp) |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 47 | payoff | #  payoff_curve_summary |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 49 | payoff | "payoff_curve_summary: ADD COLUMN structure_id", |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 50 | payoff | "ALTER TABLE payoff_curve_summary ADD COLUMN structure_id INTEGER", |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 53 | payoff | "payoff_curve_summary: BACKFILL structure_id", |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 55 | payoff | UPDATE payoff_curve_summary |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 59 | payoff | WHERE d.aba       = payoff_curve_summary.aba |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 60 | payoff | AND d.timestamp = payoff_curve_summary.timestamp |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 66 | payoff | "payoff_curve_summary: CREATE INDEX sid+ts", |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 68 | payoff | CREATE INDEX IF NOT EXISTS idx_payoff_summary_sid_ts |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 69 | payoff | ON payoff_curve_summary (structure_id, timestamp) |
| db/migrations/add_structure_id_to_payoff_curve_points.py | 106 | payoff | for table in ("payoff_curve_points", "payoff_curve_summary"): |
| db/reader.py | 14 | payoff | class PayoffReader: |
| db/reader.py | 15 | payoff | """Leitor para análise de pontos do payoff curve e decisões estruturais.""" |
| db/reader.py | 42 | payoff | def get_payoff_curve(self, ref: StructureRef, timestamp: Optional[str] = None) -> pd.DataFrame: |
| db/reader.py | 44 | payoff | Retorna pontos do payoff curve como DataFrame. |
| db/reader.py | 58 | payoff | FROM payoff_curve_points |
| db/reader.py | 67 | payoff | FROM payoff_curve_points |
| db/reader.py | 69 | payoff | SELECT MAX(timestamp) FROM payoff_curve_points WHERE {ref.db_column()} = ? |
| db/schema.py | 6 | curva, payoff | -- Curva de payoff (por ponto) usada no seu projeto |
| db/schema.py | 7 | payoff | CREATE TABLE IF NOT EXISTS payoff_curve_points ( |
| db/schema.py | 18 | payoff | CREATE INDEX IF NOT EXISTS idx_payoff_timestamp_aba |
| db/schema.py | 19 | payoff | ON payoff_curve_points(timestamp, aba); |
| db/schema.py | 21 | payoff | CREATE INDEX IF NOT EXISTS idx_payoff_spot |
| db/schema.py | 22 | payoff | ON payoff_curve_points(point_spot); |
| db/schema.py | 54 | payoff | -- Compat: tabela esperada por código antigo/viewers (payoff_points) |
| db/schema.py | 55 | payoff | -- Vamos mapear para o mesmo conceito (pontos de payoff). |
| db/schema.py | 56 | payoff | CREATE TABLE IF NOT EXISTS payoff_points ( |
| db/schema.py | 59 | payoff | payoff_value REAL NOT NULL, |
| db/schema.py | 64 | payoff | CREATE INDEX IF NOT EXISTS idx_payoff_points_created_at |
| db/schema.py | 65 | payoff | ON payoff_points(created_at); |
| db/schema.py | 67 | payoff | CREATE INDEX IF NOT EXISTS idx_payoff_points_strategy |
| db/schema.py | 68 | payoff | ON payoff_points(strategy_type); |
| db/writer.py | 12 | payoff | class PayoffWriter: |
| db/writer.py | 13 | payoff | """Escritor para pontos do payoff curve e decisões estruturais.""" |
| db/writer.py | 27 | payoff | def save_payoff_points(self, |
| db/writer.py | 34 | payoff | Salva pontos do payoff curve. |
| db/writer.py | 72 | payoff | INSERT INTO payoff_curve_points |
| db/writer.py | 96 | payoff | "PayoffWriter.save_structure_decision está deprecated. " |
| db/writer.py | 138 | payoff | def get_payoff_history(self, ref: StructureRef, limit: int = 100) -> List[Dict]: |
| db/writer.py | 139 | payoff | """Retorna histórico de payoff points para uma aba.""" |
| db/writer.py | 146 | payoff | FROM payoff_curve_points |
| docs/auditoria_ui_terminal_vwap_payoff.md | 1 | payoff | # Auditoria — UI Terminal VWAP Payoff |
| docs/auditoria_ui_terminal_vwap_payoff.md | 5 | payoff | Registrar a evolução do projeto UI Terminal VWAP Payoff, mantendo histórico de: |
| docs/auditoria_ui_terminal_vwap_payoff.md | 33 | payoff | feature/ui-terminal-vwap-payoff |
| docs/auditoria_ui_terminal_vwap_payoff.md | 37 | payoff | spike/ui-terminal-vwap-payoff |
| docs/auditoria_ui_terminal_vwap_payoff.md | 50 | payoff | A branch feature/ui-terminal-vwap-payoff já existe localmente. Não deve ser criada novamente sem necessidade. |
| docs/auditoria_ui_terminal_vwap_payoff.md | 79 | payoff | Arquivos relacionados a payoff |
| docs/auditoria_ui_terminal_vwap_payoff.md | 102 | payoff | - localizar serviços existentes de estrutura, payoff, snapshot e RTD; |
| docs/auditoria_ui_terminal_vwap_payoff.md | 140 | payoff | docs/ui_terminal_vwap_payoff_plano.md |
| docs/auditoria_ui_terminal_vwap_payoff.md | 141 | payoff | docs/auditoria_ui_terminal_vwap_payoff.md |
| docs/auditoria_ui_terminal_vwap_payoff.md | 213 | payoff | - separação entre preço, VWAP, PL e payoff; |
| docs/auditoria_ui_terminal_vwap_payoff.md | 243 | payoff | payoff_curve_x |
| docs/auditoria_ui_terminal_vwap_payoff.md | 244 | payoff | payoff_curve_y |
| docs/auditoria_ui_terminal_vwap_payoff.md | 246 | payoff | payoff_no_preco_atual |
| docs/auditoria_ui_terminal_vwap_payoff.md | 375 | payoff | ## 14. Fase 8 — Payoff real no terminal |
| docs/auditoria_ui_terminal_vwap_payoff.md | 379 | payoff | Exibir payoff calculado pelo sistema. |
| docs/auditoria_ui_terminal_vwap_payoff.md | 383 | payoff | - payoff vem do ViewModel real; |
| docs/auditoria_ui_terminal_vwap_payoff.md | 384 | payoff | - UI não recalcula payoff oficial; |
| docs/auditoria_ui_terminal_vwap_payoff.md | 385 | curva | - gráfico exibe curva recebida; |
| docs/auditoria_ui_terminal_vwap_payoff.md | 387 | payoff | - PL atual e payoff no vencimento aparecem separados; |
| docs/auditoria_ui_terminal_vwap_payoff.md | 431 | payoff | payoff_no_vencimento_ao_preco_atual |
| docs/auditoria_ui_terminal_vwap_payoff.md | 496 | payoff | Payoff vem do sistema |
| docs/auditoria_ui_terminal_vwap_payoff.md | 559 | payoff | Verificação registrada para a branch feature/ui-terminal-vwap-payoff. |
| docs/auditoria_ui_terminal_vwap_payoff.md | 566 | payoff | Os documentos do terminal VWAP Payoff foram criados em docs. |
| docs/auditoria_ui_terminal_vwap_payoff.md | 591 | payoff | ## Registro de andamento — Incremento 2 do Terminal VWAP Payoff |
| docs/auditoria_ui_terminal_vwap_payoff.md | 593 | payoff | Marcador: AUDITORIA_INCREMENTO_2_TERMINAL_VWAP_PAYOFF_594057f |
| docs/auditoria_ui_terminal_vwap_payoff.md | 601 | payoff | feature/ui-terminal-vwap-payoff |
| docs/auditoria_ui_terminal_vwap_payoff.md | 605 | payoff | 594057f feat(ui): adiciona app service do terminal vwap payoff |
| docs/auditoria_ui_terminal_vwap_payoff.md | 609 | payoff | 594057f (HEAD -> feature/ui-terminal-vwap-payoff) feat(ui): adiciona app service do terminal vwap payoff |
| docs/auditoria_ui_terminal_vwap_payoff.md | 610 | payoff | 37e915f feat(ui): adiciona viewmodel do terminal vwap payoff |
| docs/auditoria_ui_terminal_vwap_payoff.md | 611 | payoff | 4610f38 docs: registra premissas rtd do terminal vwap payoff |
| docs/auditoria_ui_terminal_vwap_payoff.md | 612 | payoff | 30dbc6c docs: adiciona plano e auditoria do terminal vwap payoff |
| docs/auditoria_ui_terminal_vwap_payoff.md | 613 | payoff | 34bc73c (origin/main, spike/ui-terminal-vwap-payoff, main) docs(checkpoints): add fase 2a strike investigation evidence |
| docs/auditoria_ui_terminal_vwap_payoff.md | 617 | payoff | 594057f feat(ui): adiciona app service do terminal vwap payoff |
| docs/auditoria_ui_terminal_vwap_payoff.md | 618 | payoff | ATT/tests/test_terminal_vwap_payoff_app_service.py |
| docs/auditoria_ui_terminal_vwap_payoff.md | 619 | payoff | services/terminal_vwap_payoff_app_service.py |
| docs/auditoria_ui_terminal_vwap_payoff.md | 623 | payoff | ATT/tests/test_terminal_vwap_payoff_app_service.py |
| docs/auditoria_ui_terminal_vwap_payoff.md | 624 | payoff | services/terminal_vwap_payoff_app_service.py |
| docs/auditoria_ui_terminal_vwap_payoff.md | 628 | payoff | Comando: python -m pytest ATT/tests/test_terminal_vwap_payoff*.py |
| docs/auditoria_ui_terminal_vwap_payoff.md | 634 | payoff | App service do Terminal VWAP Payoff adicionado. |
| docs/auditoria_ui_terminal_vwap_payoff.md | 666 | payoff | feature/ui-terminal-vwap-payoff |
| docs/auditoria_ui_terminal_vwap_payoff.md | 670 | payoff | Foi identificada a necessidade de garantir que o Terminal VWAP Payoff permanecesse dentro do escopo local previsto no plano. |
| docs/auditoria_ui_terminal_vwap_payoff.md | 675 | payoff | api/terminal_vwap_payoff_controller.py ausente. |
| docs/auditoria_ui_terminal_vwap_payoff.md | 677 | payoff | controllers/terminal_vwap_payoff_controller.py sem indício de FastAPI, APIRouter, HTTPException, TestClient, include_router ou rota REST. |
| docs/auditoria_ui_terminal_vwap_payoff.md | 678 | payoff | ATT/tests/test_terminal_vwap_payoff_controller.py sem indício de FastAPI, APIRouter, HTTPException, TestClient, include_router ou rota REST. |
| docs/auditoria_ui_terminal_vwap_payoff.md | 687 | payoff | python -m pytest ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py ATT/tests/test_terminal_vwap_payoff_app_service.py ATT/tests/test_terminal_vwap_payoff_controller.py |
| docs/auditoria_ui_terminal_vwap_payoff.md | 696 | payoff | Não deve ser criado endpoint REST/API para o Terminal VWAP Payoff nesta etapa. |
| docs/auditoria_ui_terminal_vwap_payoff.md | 715 | payoff | Marcador: REGISTRO_UI_PRINCIPAL_TERMINAL_VWAP_PAYOFF_434fd1e |
| docs/auditoria_ui_terminal_vwap_payoff.md | 723 | payoff | feature/ui-terminal-vwap-payoff |
| docs/auditoria_ui_terminal_vwap_payoff.md | 727 | payoff | Foi concluída a integração do Terminal VWAP Payoff na UI principal. |
| docs/auditoria_ui_terminal_vwap_payoff.md | 735 | payoff | fb1b5d8 feat(ui): integra terminal VWAP payoff na UI principal |
| docs/auditoria_ui_terminal_vwap_payoff.md | 739 | payoff | fb1b5d8 feat(ui): integra terminal VWAP payoff na UI principal |
| docs/auditoria_ui_terminal_vwap_payoff.md | 742 | payoff | ATT/tests/test_terminal_vwap_payoff_panel.py |
| docs/auditoria_ui_terminal_vwap_payoff.md | 743 | payoff | UI/components/terminal_vwap_payoff_panel.py |
| docs/auditoria_ui_terminal_vwap_payoff.md | 745 | payoff | services/terminal_vwap_payoff_app_service.py |
| docs/auditoria_ui_terminal_vwap_payoff.md | 780 | payoff | feature/ui-terminal-vwap-payoff |
| docs/auditoria_ui_terminal_vwap_payoff.md | 786 | payoff | Branch publicada em origin/feature/ui-terminal-vwap-payoff. |
| docs/auditoria_ui_terminal_vwap_payoff.md | 791 | payoff | python -m pytest ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py ATT/tests/test_terminal_vwap_payoff_app_service.py ATT/tests/test_terminal_vwap_payoff_controller.py ATT/tests/test_terminal_vwap_payoff_panel.py |
| docs/auditoria_ui_terminal_vwap_payoff.md | 799 | payoff | python -m py_compile UI/components/terminal_vwap_payoff_panel.py UI/main_window.py services/terminal_vwap_payoff_app_service.py controllers/terminal_vwap_payoff_controller.py |
| docs/auditoria_ui_terminal_vwap_payoff.md | 853 | payoff | A etapa de integração do Terminal VWAP Payoff na UI principal está concluída. |
| docs/auditoria_ui_terminal_vwap_payoff.md | 854 | payoff | A branch feature/ui-terminal-vwap-payoff está publicada no remoto. |
| docs/auditoria_ui_terminal_vwap_payoff.md | 861 | payoff | Abrir pull request da branch feature/ui-terminal-vwap-payoff, se essa for a estratégia de integração. |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 9 | payoff | 3. Cálculo e persistência de payoff. |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 29 | payoff | fase-1-mapa-payoff-codigo-atual.txt |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 30 | payoff | fase-1-mapa-payoff-runtime-codigo-atual.txt |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 39 | payoff | fase-1-trechos-payoff-decisoes-runtime.txt |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 84 | payoff | e persistir payoff e decisões. |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 140 | payoff | ## 3. Fluxo de payoff |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 145 | payoff | domain/payoff.py |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 147 | payoff | services/derived_payoff_persistence.py |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 150 | payoff | UI/components/payoff_chart.py |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 154 | payoff | run_payoff() |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 155 | payoff | compute_payoff_from_canonical_input() |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 156 | payoff | compute_payoff_curve_from_canonical_legs() |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 157 | payoff | save_payoff_from_canonical_payload() |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 158 | payoff | DerivedRepo.write_payoff_snapshot_atomic() |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 159 | payoff | DerivedRepo.insert_payoff_points() |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 167 | payoff | services/calculation_orchestrator.py::run_payoff() |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 170 | payoff | domain/payoff.py::compute_payoff_from_canonical_input() |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 173 | payoff | services/derived_service.py / services/derived_payoff_persistence.py |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 179 | payoff | payoff_curve_points |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 182 | payoff | UIDataModel / PayoffChart |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 186 | payoff | payoff_curve_points |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 205 | payoff | services/derived_payoff_persistence.py |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 215 | payoff | compute_decision_from_payoff() |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 224 | payoff | Payoff / canonical input |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 233 | payoff | services/derived_service.py / services/derived_payoff_persistence.py |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 325 | payoff | ### H2 — Tela não reflete payoff/decisão atualizados |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 363 | payoff | UI/components/payoff_chart.py |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 365 | payoff | ### Payoff/decisão/persistência |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 368 | payoff | domain/payoff.py |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 371 | payoff | services/derived_payoff_persistence.py |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 389 | payoff | 2. Payoff e decisão convergem em db/derived_repo.py, |
| docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md | 390 | payoff | usando payoff_curve_points e structure_decisions. |
| docs/EVOLUCAO_REVISAO_FUNCIONAL_POS_USO_REAL.md | 39 | payoff | / Fase 3 / Cadastro manual, payoff e decisões / Pendente / |
| docs/EVOLUCAO_REVISAO_FUNCIONAL_POS_USO_REAL.md | 50 | payoff | / P-003 / Estrutura manual aparece, mas não gera payoff / Pendente / |
| docs/EVOLUCAO_REVISAO_FUNCIONAL_POS_USO_REAL.md | 86 | payoff | / EV-003 / Teste/print / Estrutura manual aparece, mas não gera payoff/decisões / Registrado / |
| docs/EVOLUCAO_REVISAO_FUNCIONAL_POS_USO_REAL.md | 101 | payoff | / PE-004 / Garantir geração de payoff / Alta / Pendente / |
| docs/evolucoes de fases/10.1_normalizacao_comprado_vendido.md | 22 | payoff | / Cálculo/payoff/métricas técnicas / LONG / SHORT, sempre via conversor central / |
| docs/evolucoes de fases/10.1_normalizacao_comprado_vendido.md | 86 | salvar | - Salvar payload normalizado. |
| docs/evolucoes de fases/10.1_normalizacao_comprado_vendido.md | 105 | payoff | ## 10.1.4 — Cálculo/payoff/métricas |
| docs/evolucoes de fases/10.1_normalizacao_comprado_vendido.md | 112 | payoff | domain/payoff.py |
| docs/evolucoes de fases/10.1_normalizacao_comprado_vendido.md | 142 | payoff | - Cálculo, payoff e métricas centralizados em 'domain.position_side.to_pricing_engine_side()' nas bordas técnicas. |
| docs/evolucoes de fases/10.1_normalizacao_comprado_vendido.md | 151 | payoff | - 'domain/calculation_request.py', 'domain/payoff.py', 'domain/structure_metrics.py': uso técnico interno de 'LONG' / 'SHORT' para cálculo. |
| docs/evolucoes de fases/3B_CLOSURE_REPORT.md | 116 | payoff | - payoff canônico |
| docs/evolucoes de fases/baseline_v1.md | 176 | salvar | 5.	salvar no SQLite |
| docs/evolucoes de fases/baseline_v1.md | 206 | export | *	e opcionalmente "exportadas" para o Excel se você quiser manter compatibilidade visual. |
| docs/evolucoes de fases/baseline_v1.md | 250 | salvar | pandas (opcional)	Manipulação de dados tabulares (não essencial até agora, mas útil se quiser análises mais avançadas ou salvar CSV)	pip install pandas |
| docs/evolucoes de fases/baseline_v1.md | 294 | curva | 0.4 Curva de ganho (escopo) |
| docs/evolucoes de fases/baseline_v1.md | 295 | curva, payoff | *	"Curva de ganho" = payoff no vencimento PLvenc(ST)PLvenc(ST). |
| docs/evolucoes de fases/baseline_v1.md | 301 | payoff | Campos relevantes para payoff/decisão: |
| docs/evolucoes de fases/baseline_v1.md | 315 | payoff | *	Greeks / IV (existentes; não essenciais para payoff no vencimento) |
| docs/evolucoes de fases/baseline_v1.md | 326 | curva, payoff | 2.1 Curva de ganho (payoff no vencimento) |
| docs/evolucoes de fases/baseline_v1.md | 382 | curva, payoff | *	domain/payoff.py (curva e métricas) |
| docs/evolucoes de fases/baseline_v1.md | 392 | curva, payoff | *	NOVO: domain/payoff gera curva |
| docs/evolucoes de fases/baseline_v1.md | 395 | payoff | *	payoff_curve_points |
| docs/evolucoes de fases/baseline_v1.md | 401 | payoff | 4.1 payoff_curve_points |
| docs/evolucoes de fases/baseline_v1.md | 432 | curva, payoff | da própria curva de payoff no 'spot_ref' (mesma base de 'pl_max'), e o ratio pode ser negativo. |
| docs/evolucoes de fases/baseline_v1.md | 434 | payoff | mas não são combinados com 'pl_max' do payoff sem normalização. |
| docs/evolucoes de fases/baseline_v1.md | 447 | curva | *	A curva é calculada em unidades (sem multiplicador). |
| docs/evolucoes de fases/baseline_v1.md | 454 | payoff | *	domain/payoff.py (novo) |
| docs/evolucoes de fases/baseline_v1.md | 459 | payoff | *	services/update_cycle.py (chamar payoff/decision após snapshot) |
| docs/evolucoes de fases/baseline_v1.md | 475 | salvar | *	Salvar este "Documento base atualizado" em docs/baseline_v1.md |
| docs/evolucoes de fases/baseline_v1.md | 480 | payoff | Fase 1 -- Schema SQLite (payoff + decisions) (1 commit) |
| docs/evolucoes de fases/baseline_v1.md | 483 | payoff | *	payoff_curve_points |
| docs/evolucoes de fases/baseline_v1.md | 492 | payoff | *	db: add payoff_curve_points and structure_decisions tables |
| docs/evolucoes de fases/baseline_v1.md | 496 | payoff | *	insert_payoff_points(conn, ts, aba, points, spot_ref, meta) |
| docs/evolucoes de fases/baseline_v1.md | 504 | payoff | *	db: repo inserts for payoff curve and decisions |
| docs/evolucoes de fases/baseline_v1.md | 506 | curva, payoff | Fase 3 -- Domain: Payoff (curva) (1 commit) |
| docs/evolucoes de fases/baseline_v1.md | 507 | payoff | 3.1 Criar domain/payoff.py |
| docs/evolucoes de fases/baseline_v1.md | 508 | payoff | *	compute_payoff_curve(rows, spot, grid_low_pct=0.5, grid_high_pct=1.5, step_pct=0.01) |
| docs/evolucoes de fases/baseline_v1.md | 511 | payoff | *	scripts/test_payoff_curve.py com 1 call comprada e 1 call vendida (cenários simples) |
| docs/evolucoes de fases/baseline_v1.md | 513 | curva | *	curva retorna lista de pontos |
| docs/evolucoes de fases/baseline_v1.md | 516 | payoff | *	domain: payoff curve (expiry) computation |
| docs/evolucoes de fases/baseline_v1.md | 546 | payoff | *	payoff_curve_points |
| docs/evolucoes de fases/baseline_v1.md | 552 | payoff | *	services: compute+persist payoff curve and decisions per aba |
| docs/evolucoes de fases/baseline_v1.md | 571 | payoff | *	db: read APIs for decisions and payoff curves |
| docs/evolucoes de fases/baseline_v1.md | 578 | curva | 7C) Curva simples (opcional) |
| docs/evolucoes de fases/baseline_v1.md | 579 | export | *	Gráfico pode ser fase 2 (ou export CSV primeiro) |
| docs/evolucoes de fases/baseline_v1.md | 582 | curva | *	Se faltar spot, não calcula curva (grava decisão "HOLD / data_missing") |
| docs/evolucoes de fases/baseline_v1.md | 590 | payoff | 4.	Fase 3 (payoff) |
| docs/evolucoes de fases/baseline_v1a.md | 5 | export | *	Excel: permanece como RTD bridge + exportador CSV (não mais COM direto) |
| docs/evolucoes de fases/baseline_v1a.md | 7 | payoff | *	SQLite: mantém a estrutura app.db (raw) + derived.db (payoff/decisões) |
| docs/evolucoes de fases/baseline_v1a.md | 9 | export | Excel RTD  CSV export  Python ingest  app.db (raw)  derivadores  derived.db |
| docs/evolucoes de fases/baseline_v1a.md | 16 | export | *	Excel/RTD: ativo, mas apenas como bridge/exportador |
| docs/evolucoes de fases/baseline_v1a.md | 22 | payoff | *	Tabelas derivadas (payoff_curve_points, structure_decisions) para análises |
| docs/evolucoes de fases/baseline_v1a.md | 26 | export | Responsabilidade: captura RTD + exportação CSV |
| docs/evolucoes de fases/baseline_v1a.md | 27 | export | *	Módulo: VBA BridgeExport (já implementado) |
| docs/evolucoes de fases/baseline_v1a.md | 28 | export | *	Output: pasta bridge/ com CSVs + last_export.txt |
| docs/evolucoes de fases/baseline_v1a.md | 36 | payoff | Responsabilidade: payoff + decisões a partir do raw |
| docs/evolucoes de fases/baseline_v1a.md | 38 | payoff | *	domain/payoff.py |
| docs/evolucoes de fases/baseline_v1a.md | 64 | payoff | -- Ajustado para compatibilidade com ingestor atualCREATE TABLE payoff_curve_points (    id INTEGER PRIMARY KEY AUTOINCREMENT,    timestamp TEXT NOT NULL,    aba TEXT NOT NULL,    s_t REAL NOT NULL,    pl_venc REAL NOT NULL,    spot_ref REAL,    meta_json TEXT,    created_at TEXT DEFAULT CURRENT_TIMESTAMP); |
| docs/evolucoes de fases/baseline_v1a.md | 75 | export | *	VBA exportador + bridge_ingest_csv.py |
| docs/evolucoes de fases/baseline_v1a.md | 78 | payoff | Objetivo: funções para gravar payoff/decisões |
| docs/evolucoes de fases/baseline_v1a.md | 82 | payoff | insert_payoff_points(conn, timestamp, aba, points, spot_ref)insert_structure_decision(conn, timestamp, aba, decision_dict) |
| docs/evolucoes de fases/baseline_v1a.md | 84 | payoff | Fase 3 -- Domain: Payoff (FUTURO) |
| docs/evolucoes de fases/baseline_v1a.md | 86 | payoff | *	domain/payoff.py com compute_payoff_curve() |
| docs/evolucoes de fases/baseline_v1a.md | 92 | payoff | Fase 5 -- Integração payoff/decision (FUTURO) |
| docs/evolucoes de fases/baseline_v1a.md | 95 | curva | *	Gerar curvas + decisões para todas as abas ativas |
| docs/evolucoes de fases/baseline_v1a.md | 103 | payoff | *	Payoff: calculado em unidades (sem multiplicador/lote) |
| docs/evolucoes de fases/baseline_v1a.md | 120 | payoff | Commit esperado: "feat(db): derived repo inserts for payoff + decisions" |
| docs/evolucoes de fases/baseline_v2.md | 10 | curva, payoff | / payoff_curve_points       /                  /           [v]            / Pontos da curva payoff (resultado calculado)           / |
| docs/evolucoes de fases/baseline_v2.md | 12 | payoff | / payoff_curve_summary      /                  /           ~             / Referência no código, mas não vista em derived.db      / |
| docs/evolucoes de fases/baseline_v2.md | 13 | payoff | / payoff_points             /                  /           ~             / Só referência na UI e schema, não criado por padrão    / |
| docs/evolucoes de fases/DB_PATHS.md | 6 | export | - Bridge: 'bridge/*.csv' + 'bridge/last_export.txt' |
| docs/evolucoes de fases/EVOLUCAO_PRICING_PAYOFF.md | 1 | payoff | # Evolução — Pricing / Payoff Canônico |
| docs/evolucoes de fases/EVOLUCAO_PRICING_PAYOFF.md | 5 | payoff | Evitar repetição de auditorias já encerradas e manter uma trilha objetiva do fluxo Pricing / Payoff. |
| docs/evolucoes de fases/EVOLUCAO_PRICING_PAYOFF.md | 18 | payoff | python scripts/check_pricing_payoff_evolution.py --structure-id 48 |
| docs/evolucoes de fases/executed_v1.md | 4 | payoff | *	payoff_curve_points tem as colunas: |
| docs/evolucoes de fases/executed_v1.md | 12 | payoff | *	Também existe payoff_points, mas com esquema diferente e não é a tabela alvo do pipeline (ou é legado/auxiliar). |
| docs/evolucoes de fases/executed_v1.md | 13 | payoff | Decisão: alinhar o domínio para produzir pontos compatíveis com payoff_curve_points. |
| docs/evolucoes de fases/executed_v1.md | 16 | payoff | *	Seu pipeline (função tipo save_payoff_curve) esperava pontos como: |
| docs/evolucoes de fases/executed_v1.md | 22 | payoff | 3) Revisão do domain/payoff.py enviado por você |
| docs/evolucoes de fases/executed_v1.md | 24 | payoff | *	compute_payoff_curve() já estava retornando: |
| docs/evolucoes de fases/executed_v1.md | 56 | payoff | python -c "from domain.payoff import compute_payoff_for_aba; r=compute_payoff_for_aba('SUA_ABA'); print(r['aba'], r['timestamp_used'], len(r['points']), r['points'][:3])" |
| docs/evolucoes de fases/executed_v1.md | 65 | payoff | python -c "import sqlite3; c=sqlite3.connect('dados/derived.db'); cur=c.cursor(); cur.execute('select aba, count(*) from payoff_curve_points group by aba order by count(*) desc'); print(cur.fetchall()[:10]); c.close()" |
| docs/evolucoes de fases/executed_v1.md | 69 | curva | Se ainda der "curva estranha" (pulos, formato inconsistente), o primeiro suspeito é: |
| docs/evolucoes de fases/executed_v1.md | 77 | payoff | ## Pipeline de Derivados - Correção do Módulo 'domain/payoff.py' |
| docs/evolucoes de fases/executed_v1.md | 81 | salvar, curva, payoff | ### Sintomas- Pipeline falhava ao salvar curvas de payoff no 'derived.db'- Possível KeyError/TypeError na persistência de pontos- Inconsistência entre formato esperado pela tabela 'payoff_curve_points' e dados gerados |
| docs/evolucoes de fases/executed_v1.md | 82 | payoff | ### Análise do Schema'''sql-- Tabela alvo: payoff_curve_pointsCREATE TABLE payoff_curve_points (    timestamp TEXT NOT NULL,    aba TEXT NOT NULL,    spot_ref REAL,    point_spot REAL NOT NULL,    -- coordenada X    point_pl REAL NOT NULL,      -- coordenada Y      meta_json TEXT,    created_at TEXT DEFAULT (datetime('now'))); |
| docs/evolucoes de fases/executed_v1.md | 93 | curva | Impacto: Estruturas calculadas com dados de snapshots diferentes = curvas incorretas. |
| docs/evolucoes de fases/executed_v1.md | 95 | payoff | Localização: compute_payoff_curve() linha ~150 |
| docs/evolucoes de fases/executed_v1.md | 106 | payoff | else:            print(f"[FALHOU] Não foi possível calcular payoff para '{test_aba}'")]  # <-- SOBRANDO, quebra execução direta |
| docs/evolucoes de fases/executed_v1.md | 135 | payoff | python -c "from domain.payoff import compute_payoff_for_aba; r=compute_payoff_for_aba('SUA_ABA'); print(r['aba'], r['timestamp_used'], len(r['points']), r['points'][:3])" |
| docs/evolucoes de fases/executed_v1.md | 140 | payoff | python -c "import sqlite3; c=sqlite3.connect('dados/derived.db'); cur=c.cursor(); cur.execute('select aba, count(*) from payoff_curve_points group by aba order by count(*) desc'); print(cur.fetchall()[:10]); c.close()" |
| docs/evolucoes de fases/executed_v1.md | 145 | payoff | python domain/payoff.py |
| docs/evolucoes de fases/executed_v1.md | 147 | payoff | Testando payoff com dados reais...Abas disponíveis: ['ABA1', 'ABA2', 'ABA3'][OK] Aba 'ABA1': 101 pontos, PL_max=250.75 |
| docs/evolucoes de fases/executed_v1.md | 153 | payoff | Compatibilidade com payoff_curve_points |
| docs/evolucoes de fases/executed_v1.md | 169 | curva | 3.	Se houver "curva estranha", verificar sincronia timestamp entre rtd_analise_robo e rtd_analise_robo_legs |
| docs/evolucoes de fases/executed_v1.md | 172 | payoff | *	domain/payoff.py - REESCRITO COMPLETO |
| docs/evolucoes de fases/executed_v1.md | 174 | payoff | Arquivo original salvo como domain/payoff_backup_20260420.py (recomendado). |
| docs/evolucoes de fases/executed_v1.md | 177 | payoff | ## P2 -- Domain formal (payoff + decision) -- Encerramento |
| docs/evolucoes de fases/executed_v1.md | 181 | curva, payoff | - gerar curva de payoff no vencimento por aba (points compatíveis com derived.db) |
| docs/evolucoes de fases/executed_v1.md | 186 | curva, payoff | enquanto 'pl_max' vinha da curva de payoff. Isso misturava fontes e gerava inconsistência. |
| docs/evolucoes de fases/executed_v1.md | 189 | curva, payoff | **Fix:** 'pl_atual' passou a ser calculado pela própria curva de payoff: |
| docs/evolucoes de fases/executed_v1.md | 190 | payoff | - calcula payoff via compute_payoff_for_aba(aba) |
| docs/evolucoes de fases/executed_v1.md | 204 | payoff | P2 concluído e consistente: payoff + decision usam a mesma fonte para PL e ratio. |
| docs/evolucoes de fases/executed_v1.md | 207 | payoff | ## P2 -- Domain formal (payoff + decision) -- Encerramento |
| docs/evolucoes de fases/executed_v1.md | 211 | curva, payoff | - gerar curva de payoff no vencimento por aba (points compatíveis com derived.db) |
| docs/evolucoes de fases/executed_v1.md | 216 | curva, payoff | enquanto 'pl_max' vinha da curva de payoff. Isso misturava fontes e gerava inconsistência. |
| docs/evolucoes de fases/executed_v1.md | 219 | curva, payoff | **Fix:** 'pl_atual' passou a ser calculado pela própria curva de payoff: |
| docs/evolucoes de fases/executed_v1.md | 220 | payoff | - calcula payoff via compute_payoff_for_aba(aba) |
| docs/evolucoes de fases/executed_v1.md | 234 | payoff | P2 concluído e consistente: payoff + decision usam a mesma fonte para PL e ratio. |
| docs/evolucoes de fases/executed_v1.md | 241 | payoff | Implementar processamento automático de dados derivados (payoffs e decisões de estruturas) com integração ao sistema de ingestão. |
| docs/evolucoes de fases/executed_v1.md | 246 | curva, payoff | - **Tabela 'payoff_curve_points'**: Pontos da curva de payoff por estrutura/timestamp |
| docs/evolucoes de fases/executed_v1.md | 253 | payoff | payoff_curve_points: id, timestamp, aba, s_t, pl_venc, spot_ref, meta_json |
| docs/evolucoes de fases/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md | 250 | export | CSV exportado da aba RTD_LINKS |
| docs/evolucoes de fases/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md | 333 | payoff | payoff |
| docs/evolucoes de fases/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md | 336 | curva | curvas calculadas |
| docs/evolucoes de fases/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md | 344 | payoff | services/derived_payoff_persistence.py |
| docs/evolucoes de fases/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md | 374 | payoff | ### Payoff, decisões e detalhes |
| docs/evolucoes de fases/FASE_3_CLASSIFICACAO_FONTES_DADOS.md | 53 | export | CSV exportado da aba RTD_LINKS |
| docs/evolucoes de fases/FASE_3_CLASSIFICACAO_FONTES_DADOS.md | 70 | export | Podem mudar de formato, depender de Excel, RTD, exportação manual ou captura externa. |
| docs/evolucoes de fases/FASE_3_CLASSIFICACAO_FONTES_DADOS.md | 185 | payoff | payoff calculado |
| docs/evolucoes de fases/FASE_3_CLASSIFICACAO_FONTES_DADOS.md | 193 | payoff | domain/payoff.py |
| docs/evolucoes de fases/FASE_3_CLASSIFICACAO_FONTES_DADOS.md | 194 | payoff | domain/payoff_features.py |
| docs/evolucoes de fases/FASE_3_CLASSIFICACAO_FONTES_DADOS.md | 333 | export | Cotações RTD e exportações da aba RTD_LINKS são entrada bruta. |
| docs/evolucoes de fases/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md | 122 | export | bridge_ingest_csv.py:234:    control = BRIDGE_DIR / "last_export.txt" |
| docs/evolucoes de fases/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md | 253 | export | bridge_ingest_csv.py é o principal ponto de acoplamento operacional entre arquivos CSV exportados pelo bridge e o banco dados/app.db. |
| docs/evolucoes de fases/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md | 96 | export | Ler arquivos CSV exportados pelo bridge e alimentar tabelas SQLite rtd_*. |
| docs/evolucoes de fases/FASE_6_CAMADA_CANONICA_LEITURA.md | 128 | payoff | - 'rtd_payoff_points' |
| docs/evolucoes de fases/FASE_6_CAMADA_CANONICA_LEITURA.md | 129 | curva, payoff | - 'rtd_payoff_curva' |
| docs/evolucoes de fases/fase_8_banco_fonte_verdade_auditoria.md | 68 | payoff | - payoff_curve_points |
| docs/evolucoes de fases/fase_8_banco_fonte_verdade_auditoria.md | 69 | payoff | - payoff_curve_summary |
| docs/evolucoes de fases/fase_8_banco_fonte_verdade_auditoria.md | 75 | payoff | - payoff_curve_points: 505 |
| docs/evolucoes de fases/fase_8_banco_fonte_verdade_auditoria.md | 76 | payoff | - payoff_curve_summary: 0 |
| docs/evolucoes de fases/fase_8_banco_fonte_verdade_auditoria.md | 82 | curva, payoff | - O banco derived.db concentra dados derivados, especialmente curva de payoff e decisões. |
| docs/evolucoes de fases/fase_8_banco_fonte_verdade_auditoria.md | 83 | payoff | - Existem pontos de payoff persistidos. |
| docs/evolucoes de fases/fase_8_banco_fonte_verdade_auditoria.md | 85 | payoff | - A tabela payoff_curve_summary existe, mas está vazia. |
| docs/evolucoes de fases/fase_8_banco_fonte_verdade_auditoria.md | 175 | payoff | - dados derivados de payoff |
| docs/evolucoes de fases/fase_8_banco_fonte_verdade_auditoria.md | 182 | payoff | - resumo de payoff |
| docs/evolucoes de fases/fase_8_banco_fonte_verdade_auditoria.md | 230 | payoff | - domain/payoff_features.py possui persistência SQL direta em payoff_curve_summary, ponto a ser revisado para manter domínio livre de persistência. |
| docs/evolucoes de fases/fase_8_banco_fonte_verdade_auditoria.md | 289 | payoff | - payoff_curve_points |
| docs/evolucoes de fases/fase_8_banco_fonte_verdade_auditoria.md | 290 | payoff | - payoff_curve_summary |
| docs/evolucoes de fases/fase_8_banco_fonte_verdade_auditoria.md | 446 | curva, payoff | A tabela 'payoff_curve_points' possui pontos de curva associados a 'structure_id'. |
| docs/evolucoes de fases/fase_8_banco_fonte_verdade_auditoria.md | 448 | payoff | A tabela 'payoff_curve_summary' existe, mas está vazia. |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 10 | payoff | - **create_payoff_summary_table.py** |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 11 | payoff | - linha 4: 'CREATE TABLE IF NOT EXISTS payoff_curve_summary (' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 12 | payoff | - linha 4: 'CREATE TABLE IF NOT EXISTS payoff_curve_summary (' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 14 | payoff | - linha 19: 'CREATE TABLE IF NOT EXISTS payoff_curve_points (' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 15 | payoff | - linha 19: 'CREATE TABLE IF NOT EXISTS payoff_curve_points (' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 19 | payoff | - linha 7: 'CREATE TABLE IF NOT EXISTS payoff_curve_points (' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 20 | payoff | - linha 7: 'CREATE TABLE IF NOT EXISTS payoff_curve_points (' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 23 | payoff | - linha 51: 'CREATE TABLE IF NOT EXISTS payoff_points (' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 24 | payoff | - linha 51: 'CREATE TABLE IF NOT EXISTS payoff_points (' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 78 | payoff | - linha 90: 't = ensure_import_once(t, "from UI.debug_utils import payoff_debug, payoff_info")' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 79 | payoff | - linha 90: 't = ensure_import_once(t, "from UI.debug_utils import payoff_debug, payoff_info")' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 228 | payoff | - **UI/components/payoff_chart.py** |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 234 | payoff | ## payoff_curve_points |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 237 | payoff | - linha 376: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 238 | payoff | - linha 376: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 239 | payoff | - linha 463: '"SELECT COUNT(*) AS n FROM payoff_curve_points WHERE aba = ?",' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 240 | payoff | - linha 463: '"SELECT COUNT(*) AS n FROM payoff_curve_points WHERE aba = ?",' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 242 | payoff | - linha 519: '"FROM payoff_curve_points "' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 243 | payoff | - linha 519: '"FROM payoff_curve_points "' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 244 | payoff | - linha 543: '"SELECT timestamp FROM payoff_curve_points WHERE aba = ? ORDER BY timestamp DESC LIMIT 1",' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 245 | payoff | - linha 543: '"SELECT timestamp FROM payoff_curve_points WHERE aba = ? ORDER BY timestamp DESC LIMIT 1",' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 247 | payoff | - linha 105: 'INSERT OR REPLACE INTO payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 248 | payoff | - linha 105: 'INSERT OR REPLACE INTO payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 249 | payoff | - linha 190: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 250 | payoff | - linha 190: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 251 | payoff | - linha 197: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 252 | payoff | - linha 197: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 253 | payoff | - linha 211: 'DELETE FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 254 | payoff | - linha 211: 'DELETE FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 256 | payoff | - linha 40: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 257 | payoff | - linha 40: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 258 | payoff | - linha 50: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 259 | payoff | - linha 50: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 260 | payoff | - linha 52: 'SELECT MAX(timestamp) FROM payoff_curve_points WHERE aba = ?' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 261 | payoff | - linha 52: 'SELECT MAX(timestamp) FROM payoff_curve_points WHERE aba = ?' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 262 | payoff | - linha 173: 'cursor.execute("SELECT DISTINCT aba FROM payoff_curve_points ORDER BY aba")' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 263 | payoff | - linha 173: 'cursor.execute("SELECT DISTINCT aba FROM payoff_curve_points ORDER BY aba")' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 264 | payoff | - linha 191: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 265 | payoff | - linha 191: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 267 | payoff | - linha 71: 'INSERT INTO payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 268 | payoff | - linha 71: 'INSERT INTO payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 269 | payoff | - linha 146: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 270 | payoff | - linha 146: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 271 | payoff | - **scripts/build_payoff_summaries.py** |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 272 | payoff | - linha 19: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 273 | payoff | - linha 19: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 274 | payoff | - linha 32: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 275 | payoff | - linha 32: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 277 | payoff | - linha 166: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 278 | payoff | - linha 166: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 280 | payoff | - linha 27: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 281 | payoff | - linha 27: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 283 | payoff | - linha 128: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 284 | payoff | - linha 128: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 285 | payoff | - linha 154: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 286 | payoff | - linha 154: 'FROM payoff_curve_points' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 290 | payoff | ## payoff_curve_summary |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 292 | payoff | - **domain/payoff_features.py** |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 293 | payoff | - linha 175: 'INSERT INTO payoff_curve_summary (' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 294 | payoff | - linha 175: 'INSERT INTO payoff_curve_summary (' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 298 | payoff | ## payoff_points |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 300 | payoff | - **UI/components/payoff_chart.py** |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 301 | payoff | - linha 414: '# Rebuild xs/ys from payoff_points (canonical: point_spot/point_pl)' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 302 | payoff | - linha 414: '# Rebuild xs/ys from payoff_points (canonical: point_spot/point_pl)' |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 327 | payoff | - **domain/payoff.py** |
| docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md | 340 | payoff | - **domain/payoff.py** |
| docs/evolucoes de fases/roteiro_v2.md | 4 | export | - Origem: exportação por Excel, scripts 'bridge_ingest_csv.py' |
| docs/evolucoes de fases/roteiro_v2.md | 12 | payoff | - Gera tabelas: 'payoff_curve_points', 'structure_decisions' |
| docs/evolucoes de fases/roteiro_v2.md | 20 | payoff | - Exibe e detalha: payoff_curve_points, decisions, logs/auditoria |
| docs/evolucoes de fases/SQL_SURFACE_MAP_v2.md | 5 | payoff | / rtd_analise_robo        / SELECT            / domain/decision.py, domain/payoff.py, scripts/run_derived_pipeline.py / |
| docs/evolucoes de fases/SQL_SURFACE_MAP_v2.md | 6 | payoff | / rtd_analise_robo_legs   / SELECT            / domain/payoff.py                                 / |
| docs/evolucoes de fases/SQL_SURFACE_MAP_v2.md | 8 | payoff | / payoff_curve_points     / CREATE            / db/schema.py, db/derived_repo.py                 / |
| docs/evolucoes de fases/SQL_SURFACE_MAP_v2.md | 10 | payoff | /                         / SELECT            / db/reader.py, services/derived_service.py, scripts/build_payoff_summaries.py, scripts/derived_viewer.py, UI/components/details_panel.py, UI/models/ui_data.py / |
| docs/evolucoes de fases/SQL_SURFACE_MAP_v2.md | 14 | payoff | / payoff_curve_summary    / CREATE            / create_payoff_summary_table.py                   / |
| docs/evolucoes de fases/SQL_SURFACE_MAP_v2.md | 15 | payoff | /                         / INSERT            / domain/payoff_features.py                        / |
| docs/evolucoes de fases/SQL_SURFACE_MAP_v2.md | 16 | payoff | / payoff_points           / CREATE            / db/schema.py                                     / |
| docs/evolucoes de fases/SQL_SURFACE_MAP_v2.md | 17 | payoff | /                         / (comentário na UI)/ UI/components/payoff_chart.py                    / |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 37 | curva, payoff | 3-	Estrutura incluída aparece no sistema, mas curva de payoff não funciona e busca de decisões  também não. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 38 | payoff | 4-	Ao clicar em atualizar dados, o comportamento observado é inconsistente ou insuficiente: em alguns casos há mensagem genérica de sucesso, mas sem detalhar o que foi executado, quantos registros foram processados, se houve RTD, payoff ou decisões geradas. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 98 | salvar | - A falha esta provavelmente na validacao inicial do formulario ou no comando de aplicar/salvar leg.- O dominio ou a exibicao posterior ja consegue trabalhar com valor numerico convertido.- A correcao deve ocorrer antes da validacao "must be numeric", normalizando virgula para ponto quando aplicavel. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 100 | salvar | - O botao "Aplicar Leg" deve aceitar strike e premio com virgula decimal.- O botao "Salvar" deve aceitar legs com valores digitados em formato brasileiro.- A mensagem "strike must be numeric" nao deve aparecer para valores validos como 158,00. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 111 | payoff | - Ativo objeto.- Strike.- Vencimento.- Multiplicador, quando disponivel.- Demais metadados da opcao necessarios para calculo, payoff e decisoes. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 116 | salvar | Se o usuario informar tipo CALL, mas o simbolo identificado pelo cadastro/RTD/base local for PUT, o sistema deve alertar a divergencia antes de salvar. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 118 | payoff | - Ao digitar ou aplicar o simbolo da opcao, o sistema deve buscar automaticamente os dados da opcao.- O usuario nao deve precisar digitar manualmente strike e vencimento quando o simbolo for reconhecido.- Se o simbolo nao for encontrado, o sistema deve informar claramente.- Se houver divergencia entre simbolo, tipo e ativo, o sistema deve bloquear ou pedir confirmacao.- A estrutura so deve ser salva como funcional se possuir dados minimos para payoff e decisoes. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 120 | curva, payoff | 3. Estrutura incluída aparece no sistema, mas curva de payoff não funciona e busca de decisões também não. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 131 | curva, payoff | O cadastro da estrutura fica apenas visual, mas nao funcional. Isso quebra o fluxo principal do sistema. Curva de payoff nao e gerada, busca de decisões nao retorna ou nao executa corretamente. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 140 | payoff | - Servico de payoff espera campos que nao sao preenchidos na inclusao. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 142 | salvar | - Falta recalculo apos salvar a estrutura. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 151 | curva, payoff | - Gerar curva de payoff sem erro. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 161 | payoff | - Servico de payoff. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 165 | payoff | - Testes existentes de payoff e decisoes. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 170 | curva, payoff | - A curva de payoff deve ser calculada. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 215 | payoff | Payoff provavelmente nao esta sendo gerado para estrutura manual |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 217 | payoff | Tabela de payoff: payoff_curve_points    Filtro de estrutura ativo: structure_id (mode=canonical) |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 218 | curva, payoff | Porem a curva de payoff nao funciona para a estrutura cadastrada manualmente. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 220 | payoff | A tabela de pontos de payoff existe, mas a estrutura manual provavelmente nao possui pontos gerados ou nao esta sendo localizada pelo filtro ativo. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 222 | curva, payoff | - payoff_curve_points nao recebe dados para estruturas manuais.- O gerador de payoff depende da consolidacao em structure_decisions.- O filtro por structure_id em modo canonical nao encontra a estrutura criada manualmente.- O pipeline nao chama a etapa de payoff para estruturas novas.- Existem dados suficientes para exibir as legs, mas nao para gerar curva. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 224 | payoff | - Verificar se existem registros em payoff_curve_points para a estrutura ID 2.- Verificar se o payoff usa o mesmo ID exibido na tela de estruturas.- Verificar se o modo canonical transforma ou troca o identificador da estrutura.- Adicionar mensagem quando nao houver pontos de payoff gerados.- Adicionar log com total de pontos de payoff criados por estrutura. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 226 | salvar, payoff | - Ao salvar estrutura manual valida e executar pipeline, devem ser gerados pontos em payoff_curve_points para a estrutura.- Se os pontos nao forem gerados, o sistema deve informar o motivo. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 233 | payoff | Dados de mercado podem ficar desatualizados, afetando precificacao, payoff, decisoes e confiabilidade da estrutura. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 276 | payoff | 3. Verificar se a estrutura salva gera payoff. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 293 | payoff | - quantas estruturas foram processadas;- quantas estruturas foram ignoradas;- quantas decisoes foram geradas;- quantos pontos de payoff foram criados;- se houve atualizacao RTD;- quantas cotacoes RTD foram atualizadas;- se alguma etapa falhou parcialmente. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 296 | payoff | Pipeline concluido.    Estruturas lidas: X    Estruturas processadas: Y    Estruturas ignoradas: Z    Decisoes geradas: N    Pontos de payoff gerados: M    Cotacoes RTD atualizadas: R    Avisos: A    Erros: E |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 327 | payoff | Fase 3. Revisao do cadastro de estrutura e integracao com payoff |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 331 | payoff | 1. Mapear campos obrigatorios para payoff. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 337 | salvar | 7. Adicionar validacao antes de salvar. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 339 | payoff | 9. Criar teste integrado de cadastro manual ate payoff. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 342 | payoff | - Estrutura cadastrada gera payoff. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 380 | payoff | - Dados atualizados ficam disponiveis para pricing, payoff e decisoes. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 390 | payoff | 5. Testar payoff. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 409 | payoff | / Cadastro manual funcional / Parcial / Estrutura pronta para payoff e decisoes / Pendente / |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 410 | curva, payoff | / Payoff apos cadastro / Falha / Curva gerada / Pendente / |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 427 | payoff | 3. Em seguida corrigir payoff e busca de decisoes. |
| docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md | 435 | payoff | 2. Usar a estrutura cadastrada para gerar payoff. |
| docs/ui_terminal_vwap_payoff_plano.md | 1 | payoff | # Projeto UI Terminal VWAP Payoff |
| docs/ui_terminal_vwap_payoff_plano.md | 9 | payoff | - payoff analítico; |
| docs/ui_terminal_vwap_payoff_plano.md | 24 | payoff | O sistema já possui regras, banco, RTD, payoff, ViewModels, testes e documentação. O novo terminal entra como camada visual local, consumindo serviços existentes e preservando o funcionamento atual. |
| docs/ui_terminal_vwap_payoff_plano.md | 78 | payoff | Terminal VWAP Payoff |
| docs/ui_terminal_vwap_payoff_plano.md | 101 | payoff | - payoff; |
| docs/ui_terminal_vwap_payoff_plano.md | 123 | payoff | - cálculo de payoff; |
| docs/ui_terminal_vwap_payoff_plano.md | 129 | payoff | - separação entre PL atual e payoff no vencimento; |
| docs/ui_terminal_vwap_payoff_plano.md | 227 | payoff | - gráfico de payoff vindo do sistema; |
| docs/ui_terminal_vwap_payoff_plano.md | 243 | payoff | - cálculo oficial de payoff dentro da UI. |
| docs/ui_terminal_vwap_payoff_plano.md | 249 | payoff | UI Terminal VWAP Payoff |
| docs/ui_terminal_vwap_payoff_plano.md | 250 | payoff | TerminalVwapPayoffController |
| docs/ui_terminal_vwap_payoff_plano.md | 251 | payoff | TerminalVwapPayoffViewModelBuilder |
| docs/ui_terminal_vwap_payoff_plano.md | 254 | payoff | Payoff Analítico |
| docs/ui_terminal_vwap_payoff_plano.md | 274 | payoff | - calcular payoff oficial; |
| docs/ui_terminal_vwap_payoff_plano.md | 300 | payoff | payoff_curve_x |
| docs/ui_terminal_vwap_payoff_plano.md | 301 | payoff | payoff_curve_y |
| docs/ui_terminal_vwap_payoff_plano.md | 303 | payoff | payoff_no_preco_atual |
| docs/ui_terminal_vwap_payoff_plano.md | 331 | payoff | - buscar arquivos existentes relacionados a estrutura, payoff, snapshot, RTD, ViewModel, UI e CSV; |
| docs/ui_terminal_vwap_payoff_plano.md | 345 | payoff | docs: inicia plano e auditoria do terminal vwap payoff |
| docs/ui_terminal_vwap_payoff_plano.md | 355 | payoff | - criar docs/ui_terminal_vwap_payoff_plano.md; |
| docs/ui_terminal_vwap_payoff_plano.md | 356 | payoff | - criar docs/auditoria_ui_terminal_vwap_payoff.md; |
| docs/ui_terminal_vwap_payoff_plano.md | 371 | payoff | docs: adiciona plano e auditoria do terminal vwap payoff |
| docs/ui_terminal_vwap_payoff_plano.md | 398 | payoff | spike: adiciona mockups do terminal vwap payoff |
| docs/ui_terminal_vwap_payoff_plano.md | 421 | payoff | Cards de preço, VWAP, PL e payoff |
| docs/ui_terminal_vwap_payoff_plano.md | 422 | payoff | Abas de Resumo, Payoff, VWAP, Pernas e Snapshots |
| docs/ui_terminal_vwap_payoff_plano.md | 433 | payoff | docs: registra decisao visual do terminal vwap payoff |
| docs/ui_terminal_vwap_payoff_plano.md | 444 | payoff | - localizar serviços de payoff; |
| docs/ui_terminal_vwap_payoff_plano.md | 446 | payoff | - definir TerminalVwapPayoffViewModel; |
| docs/ui_terminal_vwap_payoff_plano.md | 461 | payoff | feat: define contrato do terminal vwap payoff |
| docs/ui_terminal_vwap_payoff_plano.md | 555 | payoff | ### Fase 8 — Payoff real no novo terminal |
| docs/ui_terminal_vwap_payoff_plano.md | 559 | payoff | Exibir payoff calculado pelo sistema atual. |
| docs/ui_terminal_vwap_payoff_plano.md | 563 | payoff | - reaproveitar serviço ou ViewModel de payoff existente; |
| docs/ui_terminal_vwap_payoff_plano.md | 565 | curva | - plotar curva recebida do sistema; |
| docs/ui_terminal_vwap_payoff_plano.md | 568 | payoff | - destacar payoff no preço atual; |
| docs/ui_terminal_vwap_payoff_plano.md | 569 | payoff | - separar PL atual de payoff no vencimento. |
| docs/ui_terminal_vwap_payoff_plano.md | 573 | payoff | - gráfico usa payoff real do sistema; |
| docs/ui_terminal_vwap_payoff_plano.md | 579 | payoff | feat: exibe payoff real no terminal vwap |
| docs/ui_terminal_vwap_payoff_plano.md | 606 | payoff | payoff_no_vencimento_ao_preco_atual |
| docs/ui_terminal_vwap_payoff_plano.md | 661 | payoff | - payoff vem do sistema; |
| docs/ui_terminal_vwap_payoff_plano.md | 677 | payoff | test: valida terminal vwap payoff integrado |
| docs/ui_terminal_vwap_payoff_plano.md | 689 | payoff | - exibir payoff vindo do sistema; |
| docs/ui_terminal_vwap_payoff_plano.md | 712 | payoff | ### Risco 3 — Regressão no payoff atual |
| docs/ui_terminal_vwap_payoff_plano.md | 789 | payoff | ## Registro de evolução — Incremento 2 do Terminal VWAP Payoff |
| docs/ui_terminal_vwap_payoff_plano.md | 791 | payoff | Marcador: PLANO_INCREMENTO_2_TERMINAL_VWAP_PAYOFF_594057f |
| docs/ui_terminal_vwap_payoff_plano.md | 799 | payoff | 594057f feat(ui): adiciona app service do terminal vwap payoff |
| docs/ui_terminal_vwap_payoff_plano.md | 803 | payoff | Inclusão do app service do Terminal VWAP Payoff. |
| docs/ui_terminal_vwap_payoff_plano.md | 809 | payoff | ATT/tests/test_terminal_vwap_payoff_app_service.py |
| docs/ui_terminal_vwap_payoff_plano.md | 810 | payoff | services/terminal_vwap_payoff_app_service.py |
| docs/ui_terminal_vwap_payoff_plano.md | 835 | payoff | O Terminal VWAP Payoff permanece como camada visual local. |
| docs/ui_terminal_vwap_payoff_plano.md | 864 | payoff | Antes de novos incrementos, confirmar que main.py permanece sem router do terminal e que api/terminal_vwap_payoff_controller.py permanece ausente. |
| docs/ui_terminal_vwap_payoff_plano.md | 867 | payoff | ## Registro de evolução — Integração do Terminal VWAP Payoff na UI principal |
| docs/ui_terminal_vwap_payoff_plano.md | 869 | payoff | Marcador: REGISTRO_UI_PRINCIPAL_TERMINAL_VWAP_PAYOFF_434fd1e |
| docs/ui_terminal_vwap_payoff_plano.md | 877 | payoff | feature/ui-terminal-vwap-payoff |
| docs/ui_terminal_vwap_payoff_plano.md | 881 | payoff | fb1b5d8 feat(ui): integra terminal VWAP payoff na UI principal |
| docs/ui_terminal_vwap_payoff_plano.md | 887 | payoff | Integração do painel Terminal VWAP Payoff na UI principal. |
| docs/ui_terminal_vwap_payoff_plano.md | 897 | payoff | ATT/tests/test_terminal_vwap_payoff_panel.py |
| docs/ui_terminal_vwap_payoff_plano.md | 898 | payoff | UI/components/terminal_vwap_payoff_panel.py |
| docs/ui_terminal_vwap_payoff_plano.md | 900 | payoff | services/terminal_vwap_payoff_app_service.py |
| docs/ui_terminal_vwap_payoff_plano.md | 917 | payoff | python -m pytest ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py ATT/tests/test_terminal_vwap_payoff_app_service.py ATT/tests/test_terminal_vwap_payoff_controller.py ATT/tests/test_terminal_vwap_payoff_panel.py |
| docs/ui_terminal_vwap_payoff_plano.md | 925 | payoff | python -m py_compile UI/components/terminal_vwap_payoff_panel.py UI/main_window.py services/terminal_vwap_payoff_app_service.py controllers/terminal_vwap_payoff_controller.py |
| docs/ui_terminal_vwap_payoff_plano.md | 941 | payoff | feature/ui-terminal-vwap-payoff |
| docs/ui_terminal_vwap_payoff_plano.md | 944 | payoff | origin/feature/ui-terminal-vwap-payoff |
| docs/ui_terminal_vwap_payoff_plano.md | 961 | payoff | A integração visual principal do Terminal VWAP Payoff está concluída, testada, commitada e publicada no remoto. |
| docs/validacoes/fase-15-validacao-integrada.md | 41 | payoff | scripts/patch_derived_payoff_timestamp_consistency.sh |
| docs/validacoes/fase-17-mapa-pastas-arquivos.md | 129 | payoff | create_payoff_summary_table.py |
| docs/validacoes/fase-17-mapa-pastas-arquivos.md | 195 | export | bridge/last_export.txt |
| docs/validacoes/fase-17-mapa-pastas-arquivos.md | 216 | payoff | UI/components/payoff_chart.py |
| docs/validacoes/fase-17-mapa-pastas-arquivos.md | 238 | payoff | domain/payoff.py |
| docs/validacoes/fase-17-mapa-pastas-arquivos.md | 239 | payoff | domain/payoff_features.py |
| docs/validacoes/fase-17-mapa-pastas-arquivos.md | 246 | payoff | A camada 'services/' concentra serviços de cálculo, canonical input, pricing, payoff, eventos de estrutura, legs, status, market snapshot e integração legada. |
| docs/validacoes/fase-17-mapa-pastas-arquivos.md | 277 | payoff | db/migrations/add_structure_id_to_payoff_curve_points.py |
| docs/validacoes/fase-17-mapa-pastas-arquivos.md | 302 | payoff | A suíte cobre domínio, canonical input, pricing, payoff, estruturas, eventos, legs, repositórios, UI e snapshots. |
| domain/calculation_request.py | 217 | payoff | Contrato canônico de entrada para qualquer cálculo de payoff/decisão. |
| domain/calculation_request.py | 220 | payoff | e o domínio (payoff, decision) recebe SOMENTE este objeto -- sem |
| domain/decision.py | 6 | payoff | Funcoes canonicas: compute_decision_from_inputs, compute_decision_from_payoff, |
| domain/decision.py | 29 | export | # Helpers internos (exportados para testes de interpolação) |
| domain/decision.py | 32 | payoff | def _interp_payoff(points: List[Tuple[float, float]], spot: float) -> float: |
| domain/decision.py | 33 | curva | """Interpola P&L no spot dado a partir dos pontos da curva.""" |
| domain/decision.py | 139 | payoff | def compute_decision_from_payoff( |
| domain/decision.py | 140 | payoff | payoff: Dict[str, Any], |
| domain/decision.py | 147 | payoff | Decide a partir de um dict de payoff. |
| domain/decision.py | 148 | payoff | Payoff vazio ou inválido  HOLD com 'error' em why_json. |
| domain/decision.py | 150 | payoff | if not payoff: |
| domain/decision.py | 151 | payoff | why_dict = {"error": "payoff vazio ou invalido", "reason": "invalid_input"} |
| domain/decision.py | 162 | payoff | pl_atual = payoff.get("pl_atual") or payoff.get("pl_now") or 0.0 |
| domain/decision.py | 163 | payoff | pl_max   = payoff.get("pl_max") or 0.0 |
| domain/decision.py | 166 | payoff | points = payoff.get("points") or [] |
| domain/decision.py | 167 | payoff | spot   = payoff.get("spot") |
| domain/decision.py | 169 | payoff | pl_atual = _interp_payoff(points, float(spot)) |
| domain/decision.py | 195 | payoff | payoff: Optional[Dict[str, Any]] = None, |
| domain/decision.py | 201 | payoff | if payoff: |
| domain/decision.py | 202 | payoff | return compute_decision_from_payoff(payoff=payoff, dte_min=dte_min) |
| domain/payoff.py | 27 | payoff | def _compute_leg_payoff_at_expiration(leg: dict[str, Any], spot_at_expiration: float) -> float: |
| domain/payoff.py | 43 | payoff | payoff_unit = intrinsic - premium_value |
| domain/payoff.py | 46 | payoff | payoff_unit = -payoff_unit |
| domain/payoff.py | 48 | payoff | return payoff_unit * quantity * multiplier |
| domain/payoff.py | 51 | payoff | def compute_payoff_curve_from_canonical_legs( |
| domain/payoff.py | 90 | payoff | pl_total += _compute_leg_payoff_at_expiration( |
| domain/payoff.py | 123 | payoff | def compute_payoff_from_canonical_input( |
| domain/payoff.py | 157 | payoff | result = compute_payoff_curve_from_canonical_legs( |
| domain/payoff_features.py | 106 | curva, payoff | Computa features da curva de payoff. |
| domain/payoff_features.py | 146 | payoff | INSERT INTO payoff_curve_summary ( |
| infra/bootstrap_structures_schema.py | 138 | payoff | payoff_json           TEXT, |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 96 | payoff | - 71 arquivos relacionados à UI, view, window, dialog, panel, widget, controller, viewmodel, terminal, payoff ou structure |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 296 | payoff | - Bloco visual de Payoff |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 307 | payoff | - Dados simulados de payoff |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 332 | payoff | - Área de Payoff |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 345 | payoff | - Payoff |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 346 | payoff | - Terminal VWAP Payoff |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 398 | matplotlib | - reports/ui_visual_audit/03_matplotlib.txt |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 432 | curva, payoff | - Curva de Payoff |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 434 | payoff | - Terminal VWAP Payoff |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 436 | payoff | - Ações de payoff: |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 438 | curva | - Fixar Curva A |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 439 | png, export, exportar | - Exportar PNG |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 440 | matplotlib | - Interações padrão da toolbar Matplotlib |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 450 | payoff | - Ações do Terminal VWAP Payoff: |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 453 | payoff | - Subabas Resumo, Legs, Payoff e Avisos |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 467 | curva, payoff | - curva de payoff |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 468 | curva | - comparação por Curva A |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 469 | png, export | - exportação PNG |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 471 | payoff | - terminal VWAP Payoff |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 474 | payoff | - payoff |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 489 | payoff | - blocos para VWAP e Payoff |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 497 | payoff | - simulação de payoff |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 511 | payoff | 3. Conectar painel de payoff aos contratos existentes. |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 595 | payoff | Antes de novas alterações em layout, tema, navegação, painel lateral, payoff, VWAP, estruturas ou terminal: |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 631 | payoff | - uso do contrato canônico para payoff_curve_points. |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 669 | png, export, curva, payoff | - Preservar ou realocar filtros, tabela de decisões, payoff, comparação Curva A, exportação PNG, CRUD de estruturas e Terminal VWAP Payoff. |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 729 | curva, payoff | - curva de payoff; |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 730 | curva | - comparação Curva A; |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 731 | png, export | - exportação PNG; |
| reports/auditoria/AUDITORIA_REFACTOR_UI.md | 733 | payoff | - Terminal VWAP Payoff; |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 5 | payoff | Carrega dados de derived.db e app.db para exibir decisões e payoffs |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 8 | payoff | from UI.components.payoff_chart import PayoffChart |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 19 | matplotlib | import matplotlib.pyplot as plt |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 20 | FigureCanvas | # FigureCanvasTkAgg importado lazily em _setup_chart para evitar side-effects no import |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 40 | payoff | self._payoff_worker_id = 0 |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 46 | payoff | self._loading_payoff = False |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 57 | payoff | # Não executa pipeline e não recalcula payoff. |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 120 | payoff | # Aba 2: Gráfico de Payoff |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 122 | curva, payoff | right_notebook.add(chart_frame, text="Curva de Payoff") |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 124 | payoff | self.payoff_chart = PayoffChart(chart_frame) |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 125 | payoff | self.payoff_chart.pack(fill="both", expand=True, padx=5, pady=5) |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 149 | export, exportar | file_menu.add_command(label="Exportar CSV...", command=self.export_csv) |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 190 | payoff | alteracao_36: structure_id é suficiente para carregar payoff -- timestamp não é obrigatório. |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 203 | payoff | # Carregar payoff em background -- apenas structure_id necessário |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 208 | payoff | self._start_payoff_load(structure_id, timestamp, decision_data) |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 210 | payoff | self.payoff_chart.clear() |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 211 | payoff | self.status_bar.config(text="Dados insuficientes para payoff") |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 213 | payoff | def _start_payoff_load( |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 219 | payoff | """Inicia carregamento de payoff em thread separada. |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 225 | payoff | self._payoff_worker_id += 1 |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 226 | payoff | current_worker_id = self._payoff_worker_id |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 228 | payoff | if self._loading_payoff: |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 229 | payoff | self.status_bar.config(text="Carregando payoff... (cancelando anterior)") |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 231 | payoff | self.status_bar.config(text="Carregando payoff...") |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 233 | payoff | self._loading_payoff = True |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 237 | payoff | points, info_dict = self.data_model.get_payoff_curve_info( |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 242 | payoff | f"payoff structure_id={structure_id} ts_req={timestamp} " |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 265 | payoff | if current_worker_id != self._payoff_worker_id: |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 270 | payoff | self._finish_payoff_load, |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 277 | payoff | if current_worker_id == self._payoff_worker_id: |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 280 | payoff | self._handle_payoff_error, |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 395 | payoff | self._start_payoff_load(target_sid, fresh_ts, fresh_decision) |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 406 | payoff | self.payoff_chart.clear() |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 509 | export | def export_csv(self): |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 510 | export | """Exporta dados filtrados para CSV.""" |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 511 | filedialog | from tkinter import filedialog |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 513 | filedialog, asksaveasfilename | filename = filedialog.asksaveasfilename( |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 520 | export | self.data_model.export_to_csv(current_data, filename) |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 521 | export | messagebox.showinfo("Sucesso", f"Dados exportados para {filename}") |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 523 | export, exportar | messagebox.showerror("Erro", f"Erro ao exportar: {e}") |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 556 | payoff | self.payoff_chart.fix_current_curve() |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 692 | payoff | f"- Pontos de payoff: {self._format_pipeline_value(summary.get('payoff_points'))}", |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 693 | payoff | f"- Resumos de payoff: {self._format_pipeline_value(summary.get('payoff_summaries'))}", |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 708 | payoff | payoff_points = self._format_pipeline_value(summary.get("payoff_points")) |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 713 | payoff | f"pontos_payoff={payoff_points}; erros={errors}" |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 809 | payoff | Pipeline automático de payoff e decisões |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 821 | payoff | # Handlers de payoff (thread  main thread) |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 824 | payoff | def _finish_payoff_load( |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 831 | curva | """Executado na thread principal quando a curva chega do worker.""" |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 832 | payoff | if worker_id != self._payoff_worker_id: |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 835 | payoff | self._loading_payoff = False |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 840 | payoff | overlays = self.payoff_chart.update_chart(points, decision_data) |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 858 | payoff | src = (info_dict or {}).get("source_table", "payoff_curve_points") |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 865 | payoff | self.payoff_chart.clear() |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 866 | payoff | self.status_bar.config(text="Sem dados de payoff para esta seleção") |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 868 | payoff | self._handle_payoff_error(str(e), worker_id) |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 870 | payoff | def _handle_payoff_error(self, error_msg: str, worker_id: int): |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 871 | payoff | if worker_id != self._payoff_worker_id: |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 873 | payoff | self._loading_payoff = False |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 876 | payoff | self.payoff_chart.clear() |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 879 | payoff | self.status_bar.config(text=f"Erro ao carregar payoff: {error_msg}") |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 880 | payoff | print(f"[UI] Erro no payoff: {error_msg}") |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 1109 | payoff | Recalcula pricing/payoff/decisão após criação ou edição manual. |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 1128 | payoff | _post_status(f"Estrutura {sid} salva. Recalculando payoff...") |
| reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 1144 | payoff | _set_status(f"Estrutura {sid} salva e payoff recalculado.") |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 5 | payoff | Carrega dados de derived.db e app.db para exibir decisões e payoffs |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 8 | payoff | from UI.components.payoff_chart import PayoffChart |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 14 | payoff | from UI.components.terminal_vwap_payoff_panel import TerminalVWAPPayoffPanel |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 20 | matplotlib | import matplotlib.pyplot as plt |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 21 | FigureCanvas | # FigureCanvasTkAgg importado lazily em _setup_chart para evitar side-effects no import |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 41 | payoff | self._payoff_worker_id = 0 |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 47 | payoff | self._loading_payoff = False |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 105 | payoff | # Aba 2: Gráfico de Payoff |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 107 | curva, payoff | right_notebook.add(chart_frame, text="Curva de Payoff") |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 109 | payoff | self.payoff_chart = PayoffChart(chart_frame) |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 110 | payoff | self.payoff_chart.pack(fill="both", expand=True, padx=5, pady=5) |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 115 | payoff | self._setup_terminal_vwap_payoff_tab(right_notebook) |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 136 | export, exportar | file_menu.add_command(label="Exportar CSV...", command=self.export_csv) |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 176 | payoff | alteracao_36: structure_id é suficiente para carregar payoff -- timestamp não é obrigatório. |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 189 | payoff | # Carregar payoff em background -- apenas structure_id necessário |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 194 | payoff | self._start_payoff_load(structure_id, timestamp, decision_data) |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 196 | payoff | self.payoff_chart.clear() |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 197 | payoff | self.status_bar.config(text="Dados insuficientes para payoff") |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 199 | payoff | def _start_payoff_load( |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 205 | payoff | """Inicia carregamento de payoff em thread separada. |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 211 | payoff | self._payoff_worker_id += 1 |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 212 | payoff | current_worker_id = self._payoff_worker_id |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 214 | payoff | if self._loading_payoff: |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 215 | payoff | self.status_bar.config(text="Carregando payoff... (cancelando anterior)") |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 217 | payoff | self.status_bar.config(text="Carregando payoff...") |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 219 | payoff | self._loading_payoff = True |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 223 | payoff | points, info_dict = self.data_model.get_payoff_curve_info( |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 228 | payoff | f"payoff structure_id={structure_id} ts_req={timestamp} " |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 251 | payoff | if current_worker_id != self._payoff_worker_id: |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 256 | payoff | self._finish_payoff_load, |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 263 | payoff | if current_worker_id == self._payoff_worker_id: |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 266 | payoff | self._handle_payoff_error, |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 317 | payoff | self._start_payoff_load(target_sid, target_ts, d) |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 328 | payoff | self.payoff_chart.clear() |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 339 | export | def export_csv(self): |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 340 | export | """Exporta dados filtrados para CSV.""" |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 341 | filedialog | from tkinter import filedialog |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 343 | filedialog, asksaveasfilename | filename = filedialog.asksaveasfilename( |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 350 | export | self.data_model.export_to_csv(current_data, filename) |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 351 | export | messagebox.showinfo("Sucesso", f"Dados exportados para {filename}") |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 353 | export, exportar | messagebox.showerror("Erro", f"Erro ao exportar: {e}") |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 372 | payoff | self.payoff_chart.fix_current_curve() |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 509 | payoff | Pipeline automático de payoff e decisões |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 521 | payoff | # Handlers de payoff (thread  main thread) |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 524 | payoff | def _finish_payoff_load( |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 531 | curva | """Executado na thread principal quando a curva chega do worker.""" |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 532 | payoff | if worker_id != self._payoff_worker_id: |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 535 | payoff | self._loading_payoff = False |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 540 | payoff | overlays = self.payoff_chart.update_chart(points, decision_data) |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 558 | payoff | src = (info_dict or {}).get("source_table", "payoff_curve_points") |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 565 | payoff | self.payoff_chart.clear() |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 566 | payoff | self.status_bar.config(text="Sem dados de payoff para esta seleção") |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 568 | payoff | self._handle_payoff_error(str(e), worker_id) |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 570 | payoff | def _handle_payoff_error(self, error_msg: str, worker_id: int): |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 571 | payoff | if worker_id != self._payoff_worker_id: |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 573 | payoff | self._loading_payoff = False |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 576 | payoff | self.payoff_chart.clear() |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 579 | payoff | self.status_bar.config(text=f"Erro ao carregar payoff: {error_msg}") |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 580 | payoff | print(f"[UI] Erro no payoff: {error_msg}") |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 698 | payoff | def _setup_terminal_vwap_payoff_tab(self, notebook: ttk.Notebook): |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 699 | payoff | """Adiciona o Terminal VWAP Payoff como aba nativa da UI principal.""" |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 702 | payoff | notebook.add(terminal_frame, text="Terminal VWAP Payoff") |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 706 | payoff | from services.terminal_vwap_payoff_app_service import ( |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 707 | payoff | TerminalVWAPPayoffAppService, |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 709 | payoff | from controllers.terminal_vwap_payoff_controller import ( |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 710 | payoff | TerminalVWAPPayoffController, |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 721 | payoff | app_service = TerminalVWAPPayoffAppService( |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 724 | payoff | controller = TerminalVWAPPayoffController(app_service) |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 726 | payoff | self.terminal_vwap_payoff_panel = TerminalVWAPPayoffPanel( |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 735 | payoff | self.terminal_vwap_payoff_panel.pack( |
| reports/terminal_vwap_recovery/main_window_terminal_old.py | 745 | payoff | "Terminal VWAP Payoff indisponível.\n\n" |
| reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md | 26 | curva, payoff | / Curva de Payoff / UI/modern/main_window.py: payoff, curve, curva, payoff_curve_points; UI/modern/dark_window.py: payoff / PARCIAL - evidência no modo dark; requer validação manual / Preservar no bloco principal de Payoff. / |
| reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md | 27 | curva | / Comparação Curva A / sem ocorrência textual nos arquivos modernos analisados / PENDENTE - não evidenciado em UI.modern / Preservar ou documentar substituto funcional. / |
| reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md | 28 | png, export, exportar, payoff | / Exportação PNG / UI/modern/app.py: arquivo; UI/modern/main_window.py: exportar, arquivo / PENDENTE - evidência apenas no shell temporário ou sem confirmação no dark / Preservar como ação do bloco de Payoff. / |
| reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md | 30 | payoff | / Terminal VWAP Payoff / UI/modern/main_window.py: vwap, terminal, legs; UI/modern/dark_window.py: vwap, terminal / PARCIAL - evidência no modo dark; requer validação manual / Preservar como bloco/painel operacional. / |
| reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md | 33 | payoff | / Banco e contratos canônicos / UI/modern/main_window.py: app.db, payoff_curve_points; UI/modern/dark_window.py: app.db / PARCIAL - evidência no modo dark; requer validação manual / Não mudar nesta fase. Apenas registrar uso atual. / |
| reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md | 100 | curva, payoff | ## Curva de Payoff |
| reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md | 106 | payoff | - Preservar no bloco principal de Payoff. |
| reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md | 110 | curva, payoff | - UI/modern/main_window.py: payoff, curve, curva, payoff_curve_points |
| reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md | 111 | payoff | - UI/modern/dark_window.py: payoff |
| reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md | 113 | curva | ## Comparação Curva A |
| reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md | 125 | png, export | ## Exportação PNG |
| reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md | 131 | payoff | - Preservar como ação do bloco de Payoff. |
| reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md | 136 | export, exportar | - UI/modern/main_window.py: exportar, arquivo |
| reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md | 152 | payoff | ## Terminal VWAP Payoff |
| reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md | 203 | payoff | - UI/modern/main_window.py: app.db, payoff_curve_points |
| reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md | 58 | curva, payoff | / Curva de Payoff / PARCIAL / Presença parcial observada no modo dark. / Comparar comportamento com UI atual. / |
| reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md | 59 | curva | / Comparação Curva A / PARCIAL / Presença parcial observada no modo dark. / Validar fluxo completo de comparação. / |
| reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md | 60 | png, export | / Exportação PNG / AUSENTE / Função não localizada no modo dark. / Implementar exportação em patch isolado. / |
| reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md | 62 | payoff | / Terminal VWAP Payoff / PARCIAL / Presença parcial observada no modo dark. / Validar equivalência funcional por bloco. / |
| reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md | 76 | payoff | ### Payoff |
| reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md | 78 | payoff | - Observação: recursos de payoff foram classificados como parciais. |
| reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md | 79 | curva | - Pendência: comparar curva, recálculo e comparação Curva A contra a UI atual. |
| reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md | 81 | payoff | ### Terminal VWAP Payoff |
| reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md | 91 | export | ### Exportação |
| reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md | 93 | png, export | - Observação: exportação PNG foi classificada como ausente. |
| reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md | 94 | export | - Pendência: implementar exportação em patch isolado quando priorizado. |
| reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md | 118 | png, export | 3. exportação PNG; |
| reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md | 119 | curva | 4. comparação Curva A; |
| reports/ui_visual_audit/01_prints_visual_controls.md | 103 | payoff | - Atualizar payoff |
| reports/ui_visual_audit/01_prints_visual_controls.md | 105 | curva, payoff | - Alimentar comparação de curva/payoff |
| reports/ui_visual_audit/01_prints_visual_controls.md | 162 | curva, payoff | ## 6. Aba: Curva de Payoff |
| reports/ui_visual_audit/01_prints_visual_controls.md | 166 | matplotlib | - Toolbar Matplotlib: |
| reports/ui_visual_audit/01_prints_visual_controls.md | 175 | curva | - Botão Fixar Curva A |
| reports/ui_visual_audit/01_prints_visual_controls.md | 176 | png, export, exportar | - Botão Exportar PNG |
| reports/ui_visual_audit/01_prints_visual_controls.md | 180 | curva, payoff | - Curva de Payoff vazia |
| reports/ui_visual_audit/01_prints_visual_controls.md | 181 | payoff | - Payoff de estrutura/decisão selecionada |
| reports/ui_visual_audit/01_prints_visual_controls.md | 182 | curva | - Curva A fixada |
| reports/ui_visual_audit/01_prints_visual_controls.md | 183 | curva | - Comparação B vs Curva A |
| reports/ui_visual_audit/01_prints_visual_controls.md | 193 | payoff | - 101 pontos (payoff_curve_points) |
| reports/ui_visual_audit/01_prints_visual_controls.md | 197 | payoff | - Plotar payoff da decisão/estrutura selecionada |
| reports/ui_visual_audit/01_prints_visual_controls.md | 198 | curva | - Fixar curva A para comparação |
| reports/ui_visual_audit/01_prints_visual_controls.md | 200 | png, export, exportar, imagem | - Exportar imagem PNG |
| reports/ui_visual_audit/01_prints_visual_controls.md | 201 | matplotlib | - Navegar/interagir no gráfico via Matplotlib |
| reports/ui_visual_audit/01_prints_visual_controls.md | 207 | payoff | - Não deve recalcular payoff dentro da UI; deve consumir contrato/camada existente. |
| reports/ui_visual_audit/01_prints_visual_controls.md | 279 | payoff | - A seleção de estrutura deve alimentar payoff, VWAP e detalhes. |
| reports/ui_visual_audit/01_prints_visual_controls.md | 281 | payoff | ## 8. Aba: Terminal VWAP Payoff |
| reports/ui_visual_audit/01_prints_visual_controls.md | 292 | payoff | - Payoff |
| reports/ui_visual_audit/01_prints_visual_controls.md | 312 | payoff | ### Payoff |
| reports/ui_visual_audit/01_prints_visual_controls.md | 329 | payoff | - Estrutura 2 carregada no Terminal VWAP Payoff |
| reports/ui_visual_audit/01_prints_visual_controls.md | 337 | payoff | - Exibir payoff |
| reports/ui_visual_audit/01_prints_visual_controls.md | 339 | payoff | - Integrar VWAP e payoff por estrutura |
| reports/ui_visual_audit/01_prints_visual_controls.md | 347 | payoff | - análise payoff |
| reports/ui_visual_audit/01_prints_visual_controls.md | 362 | curva, payoff | - Curva de payoff. |
| reports/ui_visual_audit/01_prints_visual_controls.md | 363 | curva | - Fixar curva A. |
| reports/ui_visual_audit/01_prints_visual_controls.md | 365 | png, export, exportar | - Exportar PNG. |
| reports/ui_visual_audit/01_prints_visual_controls.md | 373 | payoff | - Terminal VWAP Payoff. |
| reports/ui_visual_audit/01_prints_visual_controls.md | 378 | payoff | - Payoff. |
| reports/ui_visual_audit/01_prints_visual_controls.md | 387 | curva, payoff | - Perder comparação de payoff com Curva A. |
| reports/ui_visual_audit/01_prints_visual_controls.md | 388 | png, export | - Perder exportação PNG. |
| reports/ui_visual_audit/01_prints_visual_controls.md | 393 | payoff | - Perder fluxo Terminal VWAP Payoff. |
| reports/ui_visual_audit/01_prints_visual_controls.md | 395 | payoff | - Duplicar lógica de payoff na UI nova. |
| repositories/rtd_option_quotes_repository.py | 14 | export | Essa tabela e alimentada pelo CSV exportado da aba RTD_LINKS |
| repositories/system_snapshots_repository.py | 16 | payoff | "payoff_json", |
| repositories/system_snapshots_repository.py | 90 | payoff | payoff_json: dict[str, Any] / list[Any] / None = None, |
| repositories/system_snapshots_repository.py | 123 | payoff | payoff_json, |
| repositories/system_snapshots_repository.py | 140 | payoff | _to_json(payoff_json), |
| repositories/ui_data_table_candidates.py | 19 | payoff | CANDIDATE_PAYOFF_TABLES = [ |
| repositories/ui_data_table_candidates.py | 20 | payoff | "payoff_curve_points", |
| repositories/ui_data_table_candidates.py | 21 | payoff | "rtd_payoff_points", |
| repositories/ui_data_table_candidates.py | 22 | curva, payoff | "rtd_payoff_curva", |
| repositories/ui_data_table_candidates.py | 23 | payoff | "payoff_points", |
| scripts/purge_derived_snapshots.py | 12 | payoff | "payoff_curve_points", |
| scripts/purge_derived_snapshots.py | 14 | payoff | "payoff_curve_summary", |
| scripts/repair_derived_db_consistency.py | 21 | payoff | LEFT JOIN payoff_curve_points p |
| scripts/repair_derived_db_consistency.py | 31 | payoff | FROM payoff_curve_points p |
| scripts/repair_derived_db_consistency.py | 122 | payoff | FROM payoff_curve_points |
| scripts/repair_derived_db_consistency.py | 223 | payoff | LEFT JOIN payoff_curve_points p |
| scripts/repair_derived_db_consistency.py | 255 | payoff | FROM payoff_curve_points p |
| scripts/repair_derived_db_consistency.py | 275 | payoff | DELETE FROM payoff_curve_points |
| scripts/repair_derived_db_consistency.py | 279 | payoff | WHERE d.aba = payoff_curve_points.aba |
| scripts/repair_derived_db_consistency.py | 280 | payoff | AND d.timestamp = payoff_curve_points.timestamp |
| scripts/run_derived_pipeline.py | 36 | payoff | Placeholder: Gera payoff_curve_summary a partir de payoff_curve_points. |
| scripts/validate_derived_db.py | 65 | payoff | points_count = safe_count("payoff_curve_points") |
| scripts/validate_derived_db.py | 71 | payoff | print("[WARN] Tabela payoff_curve_points nao acessivel (ou nao existe).") |
| services/calculation_orchestrator.py | 3 | payoff | # alteracao_46: _request_to_payoff_dict, run_payoff, run_decision |
| services/calculation_orchestrator.py | 20 | payoff | from domain.payoff import compute_payoff_from_canonical_input |
| services/calculation_orchestrator.py | 111 | payoff | def _request_to_payoff_dict( |
| services/calculation_orchestrator.py | 149 | payoff | def run_payoff( |
| services/calculation_orchestrator.py | 156 | payoff | """Executa calculo de payoff a partir de um CalculationRequest.""" |
| services/calculation_orchestrator.py | 157 | payoff | canonical = _request_to_payoff_dict(request, extra_meta=extra_meta) |
| services/calculation_orchestrator.py | 158 | payoff | return compute_payoff_from_canonical_input( |
| services/calculation_orchestrator.py | 168 | payoff | payoff: Optional[dict] = None, |
| services/calculation_orchestrator.py | 175 | payoff | if _pl_max is None and payoff: |
| services/calculation_orchestrator.py | 176 | payoff | _pl_max = float(payoff.get("pl_max") or 0.0) |
| services/calculation_orchestrator.py | 181 | payoff | if _pl_atual is None and payoff: |
| services/calculation_orchestrator.py | 182 | payoff | _pl_atual = float(payoff.get("pl_atual") or payoff.get("pl_now") or 0.0) |
| services/calculation_orchestrator.py | 195 | payoff | return compute_decision_from_contract(contract, payoff=payoff) |
| services/calculation_orchestrator.py | 205 | payoff | """alteracao_47: pipeline completo payoff + decision.""" |
| services/calculation_orchestrator.py | 206 | payoff | payoff_result = run_payoff( |
| services/calculation_orchestrator.py | 213 | payoff | decision_result = run_decision(request, payoff=payoff_result) |
| services/calculation_orchestrator.py | 216 | payoff | "payoff":           payoff_result, |
| services/calculation_orchestrator.py | 233 | payoff | - Executar payoff e decisao sem acessar raw DB diretamente |
| services/calculation_orchestrator.py | 303 | payoff | def _request_to_payoff_dict(self, request: CalculationRequest) -> Dict[str, Any]: |
| services/calculation_orchestrator.py | 304 | payoff | """Converte CalculationRequest para o dict de payoff.""" |
| services/calculation_orchestrator.py | 338 | payoff | # run_payoff / run_decision / run_full_pipeline |
| services/calculation_orchestrator.py | 341 | payoff | def run_payoff( |
| services/calculation_orchestrator.py | 348 | payoff | canonical = self._request_to_payoff_dict(request) |
| services/calculation_orchestrator.py | 349 | payoff | return compute_payoff_from_canonical_input( |
| services/calculation_orchestrator.py | 359 | payoff | payoff_result: Optional[Dict[str, Any]] = None, |
| services/calculation_orchestrator.py | 361 | payoff | if payoff_result is None: |
| services/calculation_orchestrator.py | 362 | payoff | payoff_result = self.run_payoff(request) |
| services/calculation_orchestrator.py | 365 | payoff | payoff_result.get("pl_max") or payoff_result.get("max_profit") or 0.0 |
| services/calculation_orchestrator.py | 368 | payoff | payoff_result.get("pl_atual") |
| services/calculation_orchestrator.py | 369 | payoff | or payoff_result.get("current_pl") |
| services/calculation_orchestrator.py | 370 | payoff | or payoff_result.get("pl_now") |
| services/calculation_orchestrator.py | 374 | payoff | payoff_result.get("dte_min") |
| services/calculation_orchestrator.py | 384 | payoff | return compute_decision_from_contract(contract, payoff=payoff_result) |
| services/calculation_orchestrator.py | 393 | payoff | """Executa run_payoff -> run_decision em sequencia.""" |
| services/calculation_orchestrator.py | 394 | payoff | payoff_result   = self.run_payoff(request, low_pct=low_pct, high_pct=high_pct, step_pct=step_pct) |
| services/calculation_orchestrator.py | 395 | payoff | decision_result = self.run_decision(request, payoff_result=payoff_result) |
| services/calculation_orchestrator.py | 398 | payoff | "payoff":           payoff_result, |
| services/calculation_orchestrator.py | 506 | payoff | Retorna dict com chaves: structure_id, payoff, decision. |
| services/calculation_orchestrator.py | 516 | payoff | "payoff":       pipeline_result["payoff"], |
| services/canonical_input_service.py | 199 | payoff | consumidores downstream (pricing, greeks, payoff) tenham os dados. |
| services/canonical_pricing_facade.py | 4 | payoff | alteracao_21 -- Wiring do PayoffPersistencePort (DerivedPayoffPersistence) injetado |
| services/canonical_pricing_facade.py | 21 | payoff | C5: DerivedPayoffPersistence injetado como payoff_persistence_port |
| services/canonical_pricing_facade.py | 34 | payoff | from services.derived_payoff_persistence import DerivedPayoffPersistence |
| services/canonical_pricing_facade.py | 271 | payoff | # campos canônicos esperados pelo fluxo pricing/payoff |
| services/canonical_pricing_facade.py | 330 | payoff | DerivedPayoffPersistence.persist() |
| services/canonical_pricing_facade.py | 346 | payoff | payoff_persistence_port=DerivedPayoffPersistence(), |
| services/derived_payoff_persistence.py | 1 | payoff | # services/derived_payoff_persistence.py |
| services/derived_payoff_persistence.py | 6 | payoff | from domain.payoff import compute_payoff_from_canonical_input |
| services/derived_payoff_persistence.py | 7 | payoff | from services.derived_service import save_payoff_from_canonical_payload, save_decision_from_canonical_payload |
| services/derived_payoff_persistence.py | 12 | payoff | class DerivedPayoffPersistence: |
| services/derived_payoff_persistence.py | 14 | payoff | Implementação concreta de PayoffPersistencePort. |
| services/derived_payoff_persistence.py | 18 | curva, payoff | 2. Calcular a curva de payoff via domain/payoff.py |
| services/derived_payoff_persistence.py | 24 | payoff | #  PayoffPersistencePort.persist()                                 # |
| services/derived_payoff_persistence.py | 33 | payoff | logger.debug("derived_payoff_persistence: pricing_payload vazio, skip.") |
| services/derived_payoff_persistence.py | 40 | payoff | "derived_payoff_persistence: status=%r não elegível para payoff, skip.", |
| services/derived_payoff_persistence.py | 45 | payoff | # Timestamp único para payoff + decisão. |
| services/derived_payoff_persistence.py | 49 | payoff | payoff_saved = self._persist_payoff(pricing_payload, result, snapshot_ts) |
| services/derived_payoff_persistence.py | 50 | payoff | if not payoff_saved: |
| services/derived_payoff_persistence.py | 52 | payoff | "derived_payoff_persistence: decisão não gravada porque payoff não foi salvo -- structure_id=%s", |
| services/derived_payoff_persistence.py | 60 | payoff | "derived_payoff_persistence: payoff salvo, mas decisão falhou -- structure_id=%s timestamp=%s", |
| services/derived_payoff_persistence.py | 66 | payoff | #  payoff                                                          # |
| services/derived_payoff_persistence.py | 69 | payoff | def _persist_payoff( |
| services/derived_payoff_persistence.py | 77 | payoff | payoff_result = compute_payoff_from_canonical_input(canonical_input) |
| services/derived_payoff_persistence.py | 79 | payoff | if not payoff_result.get("points"): |
| services/derived_payoff_persistence.py | 81 | payoff | "derived_payoff_persistence: payoff sem pontos para structure_id=%s", |
| services/derived_payoff_persistence.py | 86 | payoff | save_payoff_from_canonical_payload(payoff_result, timestamp=snapshot_ts) |
| services/derived_payoff_persistence.py | 88 | payoff | "derived_payoff_persistence: %d pontos gravados -- structure_id=%s", |
| services/derived_payoff_persistence.py | 89 | payoff | len(payoff_result["points"]), |
| services/derived_payoff_persistence.py | 96 | payoff | "derived_payoff_persistence: erro ao gravar payoff -- structure_id=%s", |
| services/derived_payoff_persistence.py | 166 | payoff | "derived_payoff_persistence: decisão gravada -- structure_id=%s", |
| services/derived_payoff_persistence.py | 173 | payoff | "derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s", |
| services/derived_payoff_persistence.py | 188 | payoff | Monta o canonical_input esperado por compute_payoff_from_canonical_input(). |
| services/derived_service.py | 4 | payoff | alteracao_30/alteracao_57c -- Servico de persistencia de dados derivados (payoff + decisoes). |
| services/derived_service.py | 6 | payoff | alteracao_65           -- get_payoff_by_aba() removida da interface pública (standalone). |
| services/derived_service.py | 18 | payoff | cleanup_old_payoff_data, |
| services/derived_service.py | 20 | payoff | insert_payoff_points, |
| services/derived_service.py | 157 | payoff | # Payoff |
| services/derived_service.py | 160 | payoff | def save_payoff_curve( |
| services/derived_service.py | 199 | payoff | return insert_payoff_points( |
| services/derived_service.py | 210 | payoff | def save_payoff_from_canonical_payload( |
| services/derived_service.py | 211 | payoff | payoff: Dict[str, Any], |
| services/derived_service.py | 219 | payoff | structure_id=payoff.get("structure_id"), |
| services/derived_service.py | 220 | payoff | structure_name=payoff.get("structure_name"), |
| services/derived_service.py | 221 | payoff | underlying_asset=payoff.get("underlying_asset"), |
| services/derived_service.py | 224 | payoff | sid_from_payload = payoff.get("structure_id") |
| services/derived_service.py | 232 | payoff | meta=payoff.get("meta"), |
| services/derived_service.py | 234 | payoff | structure_name=payoff.get("structure_name"), |
| services/derived_service.py | 235 | payoff | underlying_asset=payoff.get("underlying_asset"), |
| services/derived_service.py | 236 | payoff | reference_date=payoff.get("reference_date"), |
| services/derived_service.py | 237 | payoff | input_meta=payoff.get("input_meta"), |
| services/derived_service.py | 242 | payoff | sig = inspect.signature(save_payoff_curve) |
| services/derived_service.py | 254 | payoff | return save_payoff_curve( |
| services/derived_service.py | 256 | payoff | points=payoff.get("points", []), |
| services/derived_service.py | 257 | payoff | spot_ref=payoff.get("spot_ref"), |
| services/derived_service.py | 263 | payoff | return save_payoff_curve( |
| services/derived_service.py | 265 | payoff | points=payoff.get("points", []), |
| services/derived_service.py | 266 | payoff | spot_ref=payoff.get("spot_ref"), |
| services/derived_service.py | 353 | payoff | deleted_payoff = cleanup_old_payoff_data(conn, days_to_keep=days_to_keep) |
| services/derived_service.py | 355 | payoff | return {"payoff_deleted": deleted_payoff, "decisions_deleted": deleted_dec} |
| services/derived_service.py | 362 | payoff | def get_all_payoff_curves(): |
| services/derived_service.py | 367 | payoff | FROM payoff_curve_points |
| services/derived_service.py | 382 | payoff | def get_payoff_by_structure_id(structure_id: int): |
| services/derived_service.py | 384 | payoff | alteracao_56/alteracao_65: único ponto de entrada canônico para leitura de payoff. |
| services/derived_service.py | 385 | payoff | get_payoff_by_aba() removida da interface pública (alteracao_65). |
| services/derived_service.py | 394 | payoff | FROM payoff_curve_points |
| services/derived_service.py | 505 | payoff | # get_payoff_by_aba() removida da interface pública. |
| services/derived_service.py | 506 | payoff | # get_payoff_by_structure_id() é o único ponto de entrada canônico. |
| services/derived_service.py | 511 | payoff | alteracao_65: get_payoff_by_aba() nao exposta -- use get_payoff_by_structure_id(). |
| services/derived_service.py | 512 | payoff | get_payoff_by_aba() ausente por decisao de design (alteracao_65): interface simplificada. |
| services/derived_service.py | 515 | payoff | # alteracao_65: get_payoff_by_aba() deliberadamente nao implementada nesta classe. |
| services/derived_service.py | 516 | payoff | # Chamadores legados devem migrar para get_payoff_by_structure_id(). |
| services/derived_service.py | 518 | payoff | def get_payoff_by_structure_id(self, structure_id: int): |
| services/derived_service.py | 519 | payoff | """Retorna pontos de payoff para a estrutura informada.""" |
| services/derived_service.py | 520 | payoff | return get_payoff_by_structure_id(structure_id) |
| services/derived_service.py | 522 | payoff | def save_payoff_curve(self, *args, **kwargs): |
| services/derived_service.py | 523 | payoff | return save_payoff_curve(*args, **kwargs) |
| services/payoff_persistence_port.py | 1 | payoff | # services/payoff_persistence_port.py |
| services/payoff_persistence_port.py | 5 | payoff | class PayoffPersistencePort(Protocol): |
| services/payoff_persistence_port.py | 7 | payoff | Contrato de persistência derivada (payoff + decisão). |
| services/pricing_execution_persistence_service.py | 7 | payoff | from services.payoff_persistence_port import PayoffPersistencePort |
| services/pricing_execution_persistence_service.py | 16 | payoff | payoff_persistence_port: PayoffPersistencePort / None = None, |
| services/pricing_execution_persistence_service.py | 22 | payoff | self._payoff_port = payoff_persistence_port |
| services/pricing_execution_persistence_service.py | 67 | payoff | #  alteracao_21 -- persistência derivada (payoff + decisão)           # |
| services/pricing_execution_persistence_service.py | 70 | payoff | if self._payoff_port is not None: |
| services/pricing_execution_persistence_service.py | 72 | payoff | self._payoff_port.persist( |
| services/pricing_execution_persistence_service.py | 78 | payoff | "payoff_persistence_port.persist() falhou -- execução id=%s não afetada", |
| services/pricing_execution_persistence_service.py | 124 | payoff | payoff_json=self._extract_result_field(inner, "payoff"), |
| services/structure_analysis_service.py | 6 | payoff | from domain.decision import compute_decision_from_payoff |
| services/structure_analysis_service.py | 7 | payoff | from domain.payoff import compute_payoff_from_canonical_input |
| services/structure_analysis_service.py | 61 | payoff | # 6. Calcula payoff |
| services/structure_analysis_service.py | 62 | payoff | payoff = compute_payoff_from_canonical_input(canonical_input) |
| services/structure_analysis_service.py | 64 | payoff | # 7. Valida payoff -- se inválido, retorna HOLD com erro estruturado |
| services/structure_analysis_service.py | 65 | payoff | if not payoff or not payoff.get("pl_max"): |
| services/structure_analysis_service.py | 67 | payoff | "error": "payoff is required", |
| services/structure_analysis_service.py | 69 | payoff | "reasons": ["invalid_payoff"], |
| services/structure_analysis_service.py | 91 | payoff | "payoff":   payoff, |
| services/structure_analysis_service.py | 96 | payoff | decision = compute_decision_from_payoff( |
| services/structure_analysis_service.py | 97 | payoff | payoff=payoff, |
| services/structure_analysis_service.py | 119 | payoff | "payoff":   payoff, |
| services/terminal_vwap_payoff_app_service.py | 1 | payoff | """App service do Terminal VWAP Payoff. |
| services/terminal_vwap_payoff_app_service.py | 4 | payoff | - orquestra estrutura, mercado, payoff e ViewModel; |
| services/terminal_vwap_payoff_app_service.py | 14 | payoff | class TerminalVWAPPayoffAppService: |
| services/terminal_vwap_payoff_app_service.py | 15 | payoff | """Orquestra a montagem do ViewModel do Terminal VWAP Payoff. |
| services/terminal_vwap_payoff_app_service.py | 21 | payoff | - payoff_provider: opcional, deve expor compute_payoff(...) ou similar; |
| services/terminal_vwap_payoff_app_service.py | 22 | payoff | - viewmodel_service: opcional, por padrão usa TerminalVWAPPayoffViewModelService. |
| services/terminal_vwap_payoff_app_service.py | 33 | payoff | payoff_provider: Any / None = None, |
| services/terminal_vwap_payoff_app_service.py | 38 | payoff | self.payoff_provider = payoff_provider |
| services/terminal_vwap_payoff_app_service.py | 61 | payoff | payoff = self._compute_payoff( |
| services/terminal_vwap_payoff_app_service.py | 66 | payoff | payoff_points = self._extract_payoff_points(payoff) |
| services/terminal_vwap_payoff_app_service.py | 71 | payoff | payoff=payoff, |
| services/terminal_vwap_payoff_app_service.py | 72 | payoff | payoff_points=payoff_points, |
| services/terminal_vwap_payoff_app_service.py | 112 | payoff | from services.terminal_vwap_payoff_viewmodel_service import ( |
| services/terminal_vwap_payoff_app_service.py | 113 | payoff | TerminalVWAPPayoffViewModelService, |
| services/terminal_vwap_payoff_app_service.py | 116 | payoff | return TerminalVWAPPayoffViewModelService() |
| services/terminal_vwap_payoff_app_service.py | 171 | payoff | def _compute_payoff( |
| services/terminal_vwap_payoff_app_service.py | 178 | payoff | if self.payoff_provider is not None: |
| services/terminal_vwap_payoff_app_service.py | 180 | payoff | self.payoff_provider, |
| services/terminal_vwap_payoff_app_service.py | 182 | payoff | "compute_payoff", |
| services/terminal_vwap_payoff_app_service.py | 183 | payoff | "build_payoff", |
| services/terminal_vwap_payoff_app_service.py | 184 | payoff | "calculate_payoff", |
| services/terminal_vwap_payoff_app_service.py | 185 | payoff | "get_payoff", |
| services/terminal_vwap_payoff_app_service.py | 200 | payoff | from domain.payoff import compute_payoff_from_canonical_input |
| services/terminal_vwap_payoff_app_service.py | 203 | payoff | "structure": self._normalize_structure_for_payoff(structure), |
| services/terminal_vwap_payoff_app_service.py | 206 | payoff | "source": "terminal_vwap_payoff_app_service", |
| services/terminal_vwap_payoff_app_service.py | 211 | payoff | return compute_payoff_from_canonical_input(canonical_input) |
| services/terminal_vwap_payoff_app_service.py | 214 | payoff | def _normalize_structure_for_payoff(structure: dict[str, Any]) -> dict[str, Any]: |
| services/terminal_vwap_payoff_app_service.py | 252 | payoff | def _extract_payoff_points( |
| services/terminal_vwap_payoff_app_service.py | 253 | payoff | payoff: dict[str, Any] / list[dict[str, Any]] / None, |
| services/terminal_vwap_payoff_app_service.py | 255 | payoff | if payoff is None: |
| services/terminal_vwap_payoff_app_service.py | 258 | payoff | if isinstance(payoff, list): |
| services/terminal_vwap_payoff_app_service.py | 259 | payoff | return list(payoff) |
| services/terminal_vwap_payoff_app_service.py | 261 | payoff | if isinstance(payoff, dict): |
| services/terminal_vwap_payoff_app_service.py | 263 | payoff | payoff.get("points") |
| services/terminal_vwap_payoff_app_service.py | 264 | payoff | or payoff.get("payoff_points") |
| services/terminal_vwap_payoff_app_service.py | 265 | payoff | or payoff.get("curve") |
| services/terminal_vwap_payoff_app_service.py | 277 | payoff | payoff: dict[str, Any] / list[dict[str, Any]], |
| services/terminal_vwap_payoff_app_service.py | 278 | payoff | payoff_points: list[dict[str, Any]], |
| services/terminal_vwap_payoff_app_service.py | 285 | payoff | "build_terminal_vwap_payoff_viewmodel", |
| services/terminal_vwap_payoff_app_service.py | 303 | payoff | payoff=payoff, |
| services/terminal_vwap_payoff_app_service.py | 304 | payoff | payoff_points=payoff_points, |
| services/terminal_vwap_payoff_app_service.py | 313 | payoff | payoff: dict[str, Any] / list[dict[str, Any]], |
| services/terminal_vwap_payoff_app_service.py | 314 | payoff | payoff_points: list[dict[str, Any]], |
| services/terminal_vwap_payoff_app_service.py | 320 | payoff | payoff=payoff, |
| services/terminal_vwap_payoff_app_service.py | 321 | payoff | payoff_points=payoff_points, |
| services/terminal_vwap_payoff_app_service.py | 326 | payoff | payoff_points=payoff_points, |
| services/terminal_vwap_payoff_app_service.py | 331 | payoff | payoff_points=payoff_points, |
| services/terminal_vwap_payoff_app_service.py | 333 | payoff | lambda: method(structure, market, payoff_points), |
| services/terminal_vwap_payoff_viewmodel_service.py | 1 | payoff | """ViewModel do Terminal VWAP Payoff. |
| services/terminal_vwap_payoff_viewmodel_service.py | 3 | payoff | Este módulo monta um payload puro para a futura UI do Terminal VWAP Payoff. |
| services/terminal_vwap_payoff_viewmodel_service.py | 18 | payoff | class TerminalVWAPPayoffViewModelService: |
| services/terminal_vwap_payoff_viewmodel_service.py | 19 | payoff | """Monta o ViewModel canônico do Terminal VWAP Payoff.""" |
| services/terminal_vwap_payoff_viewmodel_service.py | 26 | payoff | payoff_points: list[Any] / None = None, |
| services/terminal_vwap_payoff_viewmodel_service.py | 34 | payoff | payoff_points: pontos de payoff já calculados. |
| services/terminal_vwap_payoff_viewmodel_service.py | 38 | payoff | dict com blocos: terminal, structure, market, legs, payoff, meta. |
| services/terminal_vwap_payoff_viewmodel_service.py | 51 | payoff | normalized_payoff = self._normalize_payoff(payoff_points or []) |
| services/terminal_vwap_payoff_viewmodel_service.py | 55 | payoff | "name": "ui-terminal-vwap-payoff", |
| services/terminal_vwap_payoff_viewmodel_service.py | 62 | payoff | "payoff": normalized_payoff, |
| services/terminal_vwap_payoff_viewmodel_service.py | 64 | payoff | "source": "terminal_vwap_payoff_viewmodel_service", |
| services/terminal_vwap_payoff_viewmodel_service.py | 70 | payoff | payoff=normalized_payoff, |
| services/terminal_vwap_payoff_viewmodel_service.py | 205 | payoff | def _normalize_payoff(self, payoff_points: list[Any]) -> dict[str, Any]: |
| services/terminal_vwap_payoff_viewmodel_service.py | 208 | payoff | for point in payoff_points: |
| services/terminal_vwap_payoff_viewmodel_service.py | 224 | payoff | "payoff", |
| services/terminal_vwap_payoff_viewmodel_service.py | 292 | payoff | payoff: dict[str, Any], |
| services/terminal_vwap_payoff_viewmodel_service.py | 308 | payoff | if payoff.get("points_count") == 0: |
| services/terminal_vwap_payoff_viewmodel_service.py | 309 | payoff | warnings.append("payoff sem pontos") |
| tools/audit_rtd_ui_flow.py | 343 | payoff | "UI/components/terminal_vwap_payoff_dark_panel.py", |
| tools/fix_structure_side_panel_patch.py | 3 | payoff | path = Path("UI/components/terminal_vwap_payoff_dark_panel.py") |
| tools/fix_structure_side_panel_patch.py | 11 | payoff | backup = Path("UI/components/terminal_vwap_payoff_dark_panel.py.bak_side_actions_fix") |
| tools/patch_structure_side_panel.py | 437 | payoff | self._side_section_title("PAYOFF") |
| tools/patch_structure_side_panel.py | 439 | payoff | text="Recalcular Payoff", |
| tools/patch_structure_side_panel.py | 631 | payoff | payoff_points = self._calculate_payoff_from_legs(legs) |
| tools/patch_structure_side_panel.py | 634 | payoff | text=f"Analise ativa: ID {sid} - {name} / Ativo: {asset} / Payoff recalculado" |
| tools/patch_structure_side_panel.py | 637 | payoff | self._update_kpis(market, payoff_points) |
| tools/patch_structure_side_panel.py | 639 | payoff | self._render_charts(market, payoff_points, asset) |
| tools/patch_structure_side_panel.py | 640 | payoff | self._render_alerts(market, payoff_points, legs) |
| tools/patch_structure_side_panel.py | 642 | payoff | self._safe_status(f"Payoff recalculado: ID {sid}") |
| tools/patch_structure_side_panel.py | 644 | payoff | messagebox.showerror("Erro ao recalcular payoff", str(exc), parent=self.winfo_toplevel()) |
| tools/patch_structure_side_panel.py | 673 | payoff | text="Selecione uma estrutura no menu lateral para carregar a VWAP e Payoff" |
| UI/components/decisions_grid.py | 178 | export | """Retorna dados atualmente exibidos (para export).""" |
| UI/components/details_panel.py | 411 | payoff | "payoff_curve_points", |
| UI/components/details_panel.py | 920 | payoff | def _fetch_payoff_points_from_derived(self, structure_id): |
| UI/components/details_panel.py | 922 | payoff | alteracao_36: filtra por structure_id (INTEGER) em payoff_curve_points. |
| UI/components/details_panel.py | 934 | payoff | FROM payoff_curve_points |
| UI/components/details_panel.py | 975 | payoff | "SELECT COUNT(*) AS n FROM payoff_curve_points WHERE structure_id = ?", |
| UI/components/details_panel.py | 980 | payoff | "source_table": "derived.db:structure_decisions / payoff_curve_points", |
| UI/components/details_panel.py | 1029 | payoff | pts = self._fetch_payoff_points_from_derived(structure_id) |
| UI/components/payoff_chart.py | 1 | payoff | # UI/components/payoff_chart.py |
| UI/components/payoff_chart.py | 3 | matplotlib | from matplotlib.ticker import FuncFormatter |
| UI/components/payoff_chart.py | 5 | matplotlib | from matplotlib.figure import Figure |
| UI/components/payoff_chart.py | 6 | FigureCanvas, matplotlib | from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk |
| UI/components/payoff_chart.py | 8 | payoff | from UI.debug_utils import payoff_debug, payoff_info |
| UI/components/payoff_chart.py | 9 | filedialog | from tkinter import filedialog, messagebox |
| UI/components/payoff_chart.py | 13 | matplotlib | import matplotlib |
| UI/components/payoff_chart.py | 14 | matplotlib | matplotlib.use("TkAgg")  # necessário para renderizar no Tkinter |
| UI/components/payoff_chart.py | 55 | payoff | class PayoffChart(ttk.Frame): |
| UI/components/payoff_chart.py | 67 | curva | # Comparação: overlay de curvas {"points": [...], "label": "...", "color": "..."} |
| UI/components/payoff_chart.py | 76 | matplotlib | # Barra superior: toolbar matplotlib + botões de ação |
| UI/components/payoff_chart.py | 80 | export | self.btn_export = ttk.Button( |
| UI/components/payoff_chart.py | 81 | png, export, exportar | top, text="Exportar PNG", command=self.export_png |
| UI/components/payoff_chart.py | 83 | export | self.btn_export.pack(side="right", padx=(6, 0)) |
| UI/components/payoff_chart.py | 86 | curva | top, text="Fixar Curva A", command=self.fix_current_curve |
| UI/components/payoff_chart.py | 95 | matplotlib | # Figure / canvas matplotlib |
| UI/components/payoff_chart.py | 99 | FigureCanvas | self.canvas = FigureCanvasTkAgg(self.fig, master=self) |
| UI/components/payoff_chart.py | 102 | matplotlib | # Toolbar do matplotlib (fica na barra superior) |
| UI/components/payoff_chart.py | 144 | curva, payoff | self.ax.set_title("Curva de Payoff") |
| UI/components/payoff_chart.py | 170 | payoff | payoff_points: List[Dict], |
| UI/components/payoff_chart.py | 174 | curva | Atualiza a curva principal. |
| UI/components/payoff_chart.py | 178 | payoff | self._last_points = list(payoff_points) if payoff_points else [] |
| UI/components/payoff_chart.py | 182 | payoff | payoff_points, decision_data, overlay_curve=self._fixed_curve |
| UI/components/payoff_chart.py | 186 | curva | """Fixa a curva atual como Curva A para comparação.""" |
| UI/components/payoff_chart.py | 187 | payoff | payoff_debug("FIX clicked -- id=", id(self)) |
| UI/components/payoff_chart.py | 208 | curva | "label": "Curva A (fixada)", |
| UI/components/payoff_chart.py | 215 | curva | """Remove a curva fixada.""" |
| UI/components/payoff_chart.py | 216 | payoff | payoff_debug("CLEAR comparison -- id=", id(self)) |
| UI/components/payoff_chart.py | 221 | png, export | def export_png(self): |
| UI/components/payoff_chart.py | 222 | png, export | """Exporta o gráfico atual para PNG.""" |
| UI/components/payoff_chart.py | 223 | filedialog, asksaveasfilename | file_path = filedialog.asksaveasfilename( |
| UI/components/payoff_chart.py | 224 | png | defaultextension=".png", |
| UI/components/payoff_chart.py | 225 | png | filetypes=[("PNG", "*.png"), ("All files", "*.*")], |
| UI/components/payoff_chart.py | 226 | png, export, exportar | title="Exportar gráfico como PNG", |
| UI/components/payoff_chart.py | 231 | savefig | self.fig.savefig(file_path, dpi=150, bbox_inches="tight") |
| UI/components/payoff_chart.py | 234 | salvar | messagebox.showerror("Erro", f"Erro ao salvar: {e}") |
| UI/components/payoff_chart.py | 258 | payoff | payoff_points: List[Dict], |
| UI/components/payoff_chart.py | 263 | curva | Núcleo de renderização: curva principal + overlay (Curva A) + |
| UI/components/payoff_chart.py | 268 | payoff | if not payoff_points: |
| UI/components/payoff_chart.py | 269 | payoff | self.ax.set_title("Sem dados de payoff") |
| UI/components/payoff_chart.py | 276 | curva | # Extrair xs / ys da curva principal |
| UI/components/payoff_chart.py | 281 | payoff | for p in payoff_points: |
| UI/components/payoff_chart.py | 290 | payoff | payoff_info("ERROR: não consegui extrair xs/ys de payoff_points.") |
| UI/components/payoff_chart.py | 291 | payoff | self.ax.set_title("Sem dados de payoff") |
| UI/components/payoff_chart.py | 297 | payoff | payoff_debug( |
| UI/components/payoff_chart.py | 300 | payoff | payoff_debug( |
| UI/components/payoff_chart.py | 305 | curva, payoff | # Label da curva principal (B quando há overlay, senão "Payoff") |
| UI/components/payoff_chart.py | 314 | payoff | main_label = "Payoff" |
| UI/components/payoff_chart.py | 319 | curva | # Curva A (overlay fixado) |
| UI/components/payoff_chart.py | 389 | curva | # Breakevens (só da curva principal) |
| UI/components/payoff_chart.py | 422 | payoff | title = f"Payoff -- {sid} [{dec}]" |
| UI/components/payoff_chart.py | 426 | curva, payoff | title = "Curva de Payoff -- Comparação" |
| UI/components/payoff_chart.py | 428 | curva, payoff | title = "Curva de Payoff" |
| UI/components/payoff_chart.py | 453 | payoff | p, ["point_pl", "pl", "y", "pnl", "payoff", "profit_loss", "pl_value"] |
| UI/components/structure_editor_dialog.py | 19 | salvar | if dlg.saved: ...               # True se o usuario clicou Salvar com sucesso |
| UI/components/structure_editor_dialog.py | 31 | salvar | _cmd_save()     metodo que executa a logica de salvar |
| UI/components/structure_editor_dialog.py | 193 | salvar | ttk.Button(btn_bar, text="[SAVE] Salvar", command=self._cmd_save).pack(side="right", padx=4) |
| UI/components/structure_editor_dialog.py | 603 | salvar | # Salvar |
| UI/components/structure_editor_dialog.py | 611 | salvar | messagebox.showwarning("Salvar", "O campo 'Nome' e obrigatorio.", parent=self) |
| UI/components/structure_editor_dialog.py | 614 | salvar | messagebox.showwarning("Salvar", "O campo 'Ativo' e obrigatorio.", parent=self) |
| UI/components/structure_editor_dialog.py | 646 | salvar | messagebox.showerror("Erro", f"Falha ao salvar: {exc}", parent=self) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1 | payoff | # UI/components/terminal_vwap_payoff_dark_panel.py |
| UI/components/terminal_vwap_payoff_dark_panel.py | 4 | payoff | Painel operacional dark para análise VWAP e Payoff. |
| UI/components/terminal_vwap_payoff_dark_panel.py | 10 | payoff | - blocos grandes para VWAP e Payoff; |
| UI/components/terminal_vwap_payoff_dark_panel.py | 15 | curva, payoff | Quando não há curva de payoff persistida, calcula uma curva estimada a partir |
| UI/components/terminal_vwap_payoff_dark_panel.py | 29 | FigureCanvas, matplotlib | from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg |
| UI/components/terminal_vwap_payoff_dark_panel.py | 30 | matplotlib | from matplotlib.figure import Figure |
| UI/components/terminal_vwap_payoff_dark_panel.py | 129 | payoff | class TerminalVWAPPayoffDarkPanel(ctk.CTkFrame): |
| UI/components/terminal_vwap_payoff_dark_panel.py | 145 | FigureCanvas | self.canvas_vwap: Optional[FigureCanvasTkAgg] = None |
| UI/components/terminal_vwap_payoff_dark_panel.py | 146 | FigureCanvas, payoff | self.canvas_payoff: Optional[FigureCanvasTkAgg] = None |
| UI/components/terminal_vwap_payoff_dark_panel.py | 280 | payoff | text="Selecione uma estrutura no menu lateral para carregar a VWAP e Payoff", |
| UI/components/terminal_vwap_payoff_dark_panel.py | 296 | payoff | self._create_kpi("pontos", "Pontos payoff", "0", 3) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 307 | payoff | self.frame_payoff = ctk.CTkFrame( |
| UI/components/terminal_vwap_payoff_dark_panel.py | 312 | payoff | self.frame_payoff.grid(row=2, column=1, sticky="nsew", padx=(10, 0), pady=5) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 584 | payoff | payoff_points = self._load_payoff_points(sid, legs) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 590 | payoff | self._update_kpis(market, payoff_points) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 592 | payoff | self._render_charts(market, payoff_points, asset) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 593 | payoff | self._render_alerts(market, payoff_points, legs) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 814 | payoff | def _load_payoff_points( |
| UI/components/terminal_vwap_payoff_dark_panel.py | 819 | payoff | persisted = self._load_persisted_payoff_points(structure_id) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 822 | payoff | return self._calculate_payoff_from_legs(legs) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 824 | payoff | def _load_persisted_payoff_points(self, structure_id: Any) -> List[Dict[str, float]]: |
| UI/components/terminal_vwap_payoff_dark_panel.py | 831 | payoff | pl_col = _first_col(cols, ["point_pl", "pl", "payoff", "result", "resultado", "y"]) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 858 | payoff | def _calculate_payoff_from_legs(self, legs: List[Dict[str, Any]]) -> List[Dict[str, float]]: |
| UI/components/terminal_vwap_payoff_dark_panel.py | 936 | payoff | payoff_points: List[Dict[str, float]], |
| UI/components/terminal_vwap_payoff_dark_panel.py | 955 | payoff | self.kpi_labels["pontos"].configure(text=str(len(payoff_points))) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 957 | payoff | if payoff_points: |
| UI/components/terminal_vwap_payoff_dark_panel.py | 958 | payoff | vals = [p["pl"] for p in payoff_points] |
| UI/components/terminal_vwap_payoff_dark_panel.py | 962 | payoff | bes = self._breakevens(payoff_points) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1003 | payoff | payoff_points: List[Dict[str, float]], |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1012 | payoff | if not payoff_points: |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1013 | payoff | alerts.append("payoff sem pontos") |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1044 | payoff | self._render_payoff_chart([]) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1049 | payoff | payoff_points: List[Dict[str, float]], |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1053 | payoff | self._render_payoff_chart(payoff_points) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1102 | FigureCanvas | self.canvas_vwap = FigureCanvasTkAgg(fig, master=self.frame_vwap) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1106 | payoff | def _render_payoff_chart(self, points: List[Dict[str, float]]) -> None: |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1107 | payoff | self._clear_canvas("canvas_payoff") |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1126 | payoff | "Payoff indisponível", |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1134 | payoff | ax.set_title("Payoff Combinado da Estrutura", color=MUTED, fontsize=10) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1138 | FigureCanvas, payoff | self.canvas_payoff = FigureCanvasTkAgg(fig, master=self.frame_payoff) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1139 | payoff | self.canvas_payoff.draw() |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1140 | payoff | self.canvas_payoff.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1231 | payoff | self._side_section_title("PAYOFF") |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1233 | payoff | text="Recalcular Payoff", |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1441 | payoff | payoff_points = self._calculate_payoff_from_legs(legs) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1444 | payoff | text=f"Analise ativa: ID {sid} - {name} / Ativo: {asset} / Payoff recalculado" |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1447 | payoff | self._update_kpis(market, payoff_points) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1449 | payoff | self._render_charts(market, payoff_points, asset) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1450 | payoff | self._render_alerts(market, payoff_points, legs) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1452 | payoff | self._safe_status(f"Payoff recalculado: ID {sid}") |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1454 | payoff | messagebox.showerror("Erro ao recalcular payoff", str(exc), parent=self.winfo_toplevel()) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1491 | payoff | text="Selecione uma estrutura no menu lateral para carregar a VWAP e Payoff" |
| UI/components/terminal_vwap_payoff_panel.py | 1 | payoff | # UI/components/terminal_vwap_payoff_panel.py |
| UI/components/terminal_vwap_payoff_panel.py | 3 | payoff | Painel nativo Tkinter do Terminal VWAP Payoff. |
| UI/components/terminal_vwap_payoff_panel.py | 10 | payoff | -> TerminalVWAPPayoffPanel |
| UI/components/terminal_vwap_payoff_panel.py | 11 | payoff | -> TerminalVWAPPayoffController |
| UI/components/terminal_vwap_payoff_panel.py | 12 | payoff | -> TerminalVWAPPayoffAppService |
| UI/components/terminal_vwap_payoff_panel.py | 14 | payoff | -> TerminalVWAPPayoffViewModelService |
| UI/components/terminal_vwap_payoff_panel.py | 100 | payoff | def _extract_payoff_table_rows( |
| UI/components/terminal_vwap_payoff_panel.py | 105 | payoff | payoff = viewmodel.get("payoff") or {} |
| UI/components/terminal_vwap_payoff_panel.py | 106 | payoff | points = payoff.get("points") or [] |
| UI/components/terminal_vwap_payoff_panel.py | 126 | payoff | payoff = viewmodel.get("payoff") or {} |
| UI/components/terminal_vwap_payoff_panel.py | 141 | payoff | "points_count": _safe_text(payoff.get("points_count")), |
| UI/components/terminal_vwap_payoff_panel.py | 142 | payoff | "min_result": _format_currency_br(payoff.get("min_result"), 2), |
| UI/components/terminal_vwap_payoff_panel.py | 143 | payoff | "max_result": _format_currency_br(payoff.get("max_result"), 2), |
| UI/components/terminal_vwap_payoff_panel.py | 146 | payoff | for item in payoff.get("break_even_points") or [] |
| UI/components/terminal_vwap_payoff_panel.py | 151 | payoff | class TerminalVWAPPayoffPanel(ttk.Frame): |
| UI/components/terminal_vwap_payoff_panel.py | 152 | payoff | """Aba nativa do Terminal VWAP Payoff na UI principal.""" |
| UI/components/terminal_vwap_payoff_panel.py | 191 | payoff | self._status_var = tk.StringVar(value="Terminal VWAP Payoff pronto") |
| UI/components/terminal_vwap_payoff_panel.py | 263 | payoff | payoff_tab = ttk.Frame(notebook, padding=6) |
| UI/components/terminal_vwap_payoff_panel.py | 268 | payoff | notebook.add(payoff_tab, text="Payoff") |
| UI/components/terminal_vwap_payoff_panel.py | 273 | payoff | self._build_payoff_tab(payoff_tab) |
| UI/components/terminal_vwap_payoff_panel.py | 300 | payoff | "Payoff", |
| UI/components/terminal_vwap_payoff_panel.py | 375 | payoff | def _build_payoff_tab(self, parent: tk.Widget) -> None: |
| UI/components/terminal_vwap_payoff_panel.py | 379 | payoff | self._payoff_summary_var = tk.StringVar(value="Payoff ainda não carregado") |
| UI/components/terminal_vwap_payoff_panel.py | 382 | payoff | textvariable=self._payoff_summary_var, |
| UI/components/terminal_vwap_payoff_panel.py | 387 | payoff | self._payoff_tree = ttk.Treeview(parent, columns=columns, show="headings") |
| UI/components/terminal_vwap_payoff_panel.py | 389 | payoff | self._payoff_tree.heading("underlying_price", text="Spot") |
| UI/components/terminal_vwap_payoff_panel.py | 390 | payoff | self._payoff_tree.heading("result", text="Resultado") |
| UI/components/terminal_vwap_payoff_panel.py | 392 | payoff | self._payoff_tree.column("underlying_price", width=120, anchor="e") |
| UI/components/terminal_vwap_payoff_panel.py | 393 | payoff | self._payoff_tree.column("result", width=140, anchor="e") |
| UI/components/terminal_vwap_payoff_panel.py | 395 | payoff | vsb = ttk.Scrollbar(parent, orient="vertical", command=self._payoff_tree.yview) |
| UI/components/terminal_vwap_payoff_panel.py | 396 | payoff | self._payoff_tree.configure(yscrollcommand=vsb.set) |
| UI/components/terminal_vwap_payoff_panel.py | 399 | payoff | self._payoff_tree.pack(fill="both", expand=True) |
| UI/components/terminal_vwap_payoff_panel.py | 416 | payoff | "Terminal VWAP Payoff", |
| UI/components/terminal_vwap_payoff_panel.py | 449 | payoff | "Terminal VWAP Payoff", |
| UI/components/terminal_vwap_payoff_panel.py | 455 | payoff | self._set_status(f"Estrutura {structure_id} carregada no Terminal VWAP Payoff") |
| UI/components/terminal_vwap_payoff_panel.py | 487 | payoff | self._render_payoff(self._current_viewmodel) |
| UI/components/terminal_vwap_payoff_panel.py | 497 | payoff | def _render_payoff(self, viewmodel: dict[str, Any]) -> None: |
| UI/components/terminal_vwap_payoff_panel.py | 498 | payoff | for item in self._payoff_tree.get_children(): |
| UI/components/terminal_vwap_payoff_panel.py | 499 | payoff | self._payoff_tree.delete(item) |
| UI/components/terminal_vwap_payoff_panel.py | 501 | payoff | rows = _extract_payoff_table_rows(viewmodel) |
| UI/components/terminal_vwap_payoff_panel.py | 503 | payoff | self._payoff_tree.insert("", "end", iid=str(index), values=row) |
| UI/components/terminal_vwap_payoff_panel.py | 505 | payoff | payoff = viewmodel.get("payoff") or {} |
| UI/components/terminal_vwap_payoff_panel.py | 506 | payoff | self._payoff_summary_var.set( |
| UI/components/terminal_vwap_payoff_panel.py | 508 | payoff | points=_safe_text(payoff.get("points_count")), |
| UI/components/terminal_vwap_payoff_panel.py | 509 | payoff | min_result=_format_currency_br(payoff.get("min_result"), 2), |
| UI/components/terminal_vwap_payoff_panel.py | 510 | payoff | max_result=_format_currency_br(payoff.get("max_result"), 2), |
| UI/components/terminal_vwap_payoff_panel.py | 513 | payoff | for item in payoff.get("break_even_points") or [] |
| UI/debug_utils.py | 24 | payoff | def payoff_debug(*args, **kwargs): |
| UI/debug_utils.py | 25 | payoff | """Log de payoff chart apenas se debug ativo""" |
| UI/debug_utils.py | 27 | payoff | print("[PayoffChart] DEBUG", *args, **kwargs) |
| UI/debug_utils.py | 29 | payoff | def payoff_info(*args, **kwargs): |
| UI/debug_utils.py | 30 | payoff | """Log de payoff sempre""" |
| UI/debug_utils.py | 31 | payoff | print("[PayoffChart]", *args, **kwargs) |
| UI/main_window.py | 5 | payoff | Carrega dados de derived.db e app.db para exibir decisões e payoffs |
| UI/main_window.py | 8 | payoff | from UI.components.payoff_chart import PayoffChart |
| UI/main_window.py | 14 | payoff | from UI.components.terminal_vwap_payoff_panel import TerminalVWAPPayoffPanel |
| UI/main_window.py | 20 | matplotlib | import matplotlib.pyplot as plt |
| UI/main_window.py | 21 | FigureCanvas | # FigureCanvasTkAgg importado lazily em _setup_chart para evitar side-effects no import |
| UI/main_window.py | 41 | payoff | self._payoff_worker_id = 0 |
| UI/main_window.py | 47 | payoff | self._loading_payoff = False |
| UI/main_window.py | 105 | payoff | # Aba 2: Gráfico de Payoff |
| UI/main_window.py | 107 | curva, payoff | right_notebook.add(chart_frame, text="Curva de Payoff") |
| UI/main_window.py | 109 | payoff | self.payoff_chart = PayoffChart(chart_frame) |
| UI/main_window.py | 110 | payoff | self.payoff_chart.pack(fill="both", expand=True, padx=5, pady=5) |
| UI/main_window.py | 115 | payoff | self._setup_terminal_vwap_payoff_tab(right_notebook) |
| UI/main_window.py | 136 | export, exportar | file_menu.add_command(label="Exportar CSV...", command=self.export_csv) |
| UI/main_window.py | 176 | payoff | alteracao_36: structure_id é suficiente para carregar payoff -- timestamp não é obrigatório. |
| UI/main_window.py | 189 | payoff | # Carregar payoff em background -- apenas structure_id necessário |
| UI/main_window.py | 194 | payoff | self._start_payoff_load(structure_id, timestamp, decision_data) |
| UI/main_window.py | 196 | payoff | self.payoff_chart.clear() |
| UI/main_window.py | 197 | payoff | self.status_bar.config(text="Dados insuficientes para payoff") |
| UI/main_window.py | 199 | payoff | def _start_payoff_load( |
| UI/main_window.py | 205 | payoff | """Inicia carregamento de payoff em thread separada. |
| UI/main_window.py | 211 | payoff | self._payoff_worker_id += 1 |
| UI/main_window.py | 212 | payoff | current_worker_id = self._payoff_worker_id |
| UI/main_window.py | 214 | payoff | if self._loading_payoff: |
| UI/main_window.py | 215 | payoff | self.status_bar.config(text="Carregando payoff... (cancelando anterior)") |
| UI/main_window.py | 217 | payoff | self.status_bar.config(text="Carregando payoff...") |
| UI/main_window.py | 219 | payoff | self._loading_payoff = True |
| UI/main_window.py | 223 | payoff | points, info_dict = self.data_model.get_payoff_curve_info( |
| UI/main_window.py | 228 | payoff | f"payoff structure_id={structure_id} ts_req={timestamp} " |
| UI/main_window.py | 251 | payoff | if current_worker_id != self._payoff_worker_id: |
| UI/main_window.py | 256 | payoff | self._finish_payoff_load, |
| UI/main_window.py | 263 | payoff | if current_worker_id == self._payoff_worker_id: |
| UI/main_window.py | 266 | payoff | self._handle_payoff_error, |
| UI/main_window.py | 317 | payoff | self._start_payoff_load(target_sid, target_ts, d) |
| UI/main_window.py | 328 | payoff | self.payoff_chart.clear() |
| UI/main_window.py | 339 | export | def export_csv(self): |
| UI/main_window.py | 340 | export | """Exporta dados filtrados para CSV.""" |
| UI/main_window.py | 341 | filedialog | from tkinter import filedialog |
| UI/main_window.py | 343 | filedialog, asksaveasfilename | filename = filedialog.asksaveasfilename( |
| UI/main_window.py | 350 | export | self.data_model.export_to_csv(current_data, filename) |
| UI/main_window.py | 351 | export | messagebox.showinfo("Sucesso", f"Dados exportados para {filename}") |
| UI/main_window.py | 353 | export, exportar | messagebox.showerror("Erro", f"Erro ao exportar: {e}") |
| UI/main_window.py | 372 | payoff | self.payoff_chart.fix_current_curve() |
| UI/main_window.py | 509 | payoff | Pipeline automático de payoff e decisões |
| UI/main_window.py | 521 | payoff | # Handlers de payoff (thread  main thread) |
| UI/main_window.py | 524 | payoff | def _finish_payoff_load( |
| UI/main_window.py | 531 | curva | """Executado na thread principal quando a curva chega do worker.""" |
| UI/main_window.py | 532 | payoff | if worker_id != self._payoff_worker_id: |
| UI/main_window.py | 535 | payoff | self._loading_payoff = False |
| UI/main_window.py | 540 | payoff | overlays = self.payoff_chart.update_chart(points, decision_data) |
| UI/main_window.py | 558 | payoff | src = (info_dict or {}).get("source_table", "payoff_curve_points") |
| UI/main_window.py | 565 | payoff | self.payoff_chart.clear() |
| UI/main_window.py | 566 | payoff | self.status_bar.config(text="Sem dados de payoff para esta seleção") |
| UI/main_window.py | 568 | payoff | self._handle_payoff_error(str(e), worker_id) |
| UI/main_window.py | 570 | payoff | def _handle_payoff_error(self, error_msg: str, worker_id: int): |
| UI/main_window.py | 571 | payoff | if worker_id != self._payoff_worker_id: |
| UI/main_window.py | 573 | payoff | self._loading_payoff = False |
| UI/main_window.py | 576 | payoff | self.payoff_chart.clear() |
| UI/main_window.py | 579 | payoff | self.status_bar.config(text=f"Erro ao carregar payoff: {error_msg}") |
| UI/main_window.py | 580 | payoff | print(f"[UI] Erro no payoff: {error_msg}") |
| UI/main_window.py | 698 | payoff | def _setup_terminal_vwap_payoff_tab(self, notebook: ttk.Notebook): |
| UI/main_window.py | 699 | payoff | """Adiciona o Terminal VWAP Payoff como aba nativa da UI principal.""" |
| UI/main_window.py | 702 | payoff | notebook.add(terminal_frame, text="Terminal VWAP Payoff") |
| UI/main_window.py | 706 | payoff | from services.terminal_vwap_payoff_app_service import ( |
| UI/main_window.py | 707 | payoff | TerminalVWAPPayoffAppService, |
| UI/main_window.py | 709 | payoff | from controllers.terminal_vwap_payoff_controller import ( |
| UI/main_window.py | 710 | payoff | TerminalVWAPPayoffController, |
| UI/main_window.py | 721 | payoff | app_service = TerminalVWAPPayoffAppService( |
| UI/main_window.py | 724 | payoff | controller = TerminalVWAPPayoffController(app_service) |
| UI/main_window.py | 726 | payoff | self.terminal_vwap_payoff_panel = TerminalVWAPPayoffPanel( |
| UI/main_window.py | 735 | payoff | self.terminal_vwap_payoff_panel.pack( |
| UI/main_window.py | 745 | payoff | "Terminal VWAP Payoff indisponível.\n\n" |
| UI/models/ui_data.py | 16 | payoff | CANDIDATE_PAYOFF_TABLES, |
| UI/models/ui_data.py | 36 | payoff | PAYOFF_COLUMN_ALIASES = { |
| UI/models/ui_data.py | 40 | payoff | "pl":        ["point_pl", "pl", "pl_value", "y", "payoff", "pl_venc"], |
| UI/models/ui_data.py | 61 | payoff | self._payoff_table: Optional[str] = None |
| UI/models/ui_data.py | 63 | payoff | self._payoff_cols: Dict[str, str] = {} |
| UI/models/ui_data.py | 66 | payoff | self._payoff_cache: Dict[Tuple[str, str], Dict[str, Any]] = {} |
| UI/models/ui_data.py | 67 | payoff | self._payoff_cache_max = 128 |
| UI/models/ui_data.py | 101 | payoff | for t in CANDIDATE_PAYOFF_TABLES: |
| UI/models/ui_data.py | 103 | payoff | self._payoff_table = t |
| UI/models/ui_data.py | 124 | payoff | def _build_payoff_colmap(self): |
| UI/models/ui_data.py | 125 | payoff | if not self._payoff_table: |
| UI/models/ui_data.py | 126 | payoff | self._payoff_cols = {} |
| UI/models/ui_data.py | 129 | payoff | cols = self._inspect_columns(self._payoff_table) |
| UI/models/ui_data.py | 132 | payoff | if self._payoff_table == "payoff_curve_points": |
| UI/models/ui_data.py | 142 | payoff | print(f"[UI] Usando contrato canônico para {self._payoff_table}") |
| UI/models/ui_data.py | 144 | payoff | aliases = PAYOFF_COLUMN_ALIASES |
| UI/models/ui_data.py | 145 | payoff | print(f"[UI] Usando aliases flexíveis para {self._payoff_table}") |
| UI/models/ui_data.py | 154 | payoff | self._payoff_cols = colmap |
| UI/models/ui_data.py | 156 | payoff | if ("spot" not in self._payoff_cols) or ("pl" not in self._payoff_cols): |
| UI/models/ui_data.py | 158 | payoff | f"Tabela {self._payoff_table} não apresenta colunas obrigatórias " |
| UI/models/ui_data.py | 159 | payoff | f"para payoff (point_spot/point_pl ou spot/pl)." |
| UI/models/ui_data.py | 163 | payoff | if "structure_id" not in self._payoff_cols: |
| UI/models/ui_data.py | 165 | payoff | f"[UI] AVISO: {self._payoff_table} nao tem coluna structure_id. " |
| UI/models/ui_data.py | 205 | payoff | self._build_payoff_colmap() |
| UI/models/ui_data.py | 401 | payoff | def get_payoff_curve(self, structure_id: str, timestamp: str) -> List[Dict]: |
| UI/models/ui_data.py | 410 | payoff | if hasattr(self, "_payoff_cache") and cache_key in self._payoff_cache: |
| UI/models/ui_data.py | 411 | payoff | cached = self._payoff_cache[cache_key] |
| UI/models/ui_data.py | 417 | payoff | if not self._payoff_table: |
| UI/models/ui_data.py | 419 | payoff | "Tabela de payoff não encontrada. Esperadas: " |
| UI/models/ui_data.py | 420 | payoff | + ", ".join(CANDIDATE_PAYOFF_TABLES) |
| UI/models/ui_data.py | 424 | payoff | p = self._payoff_cols |
| UI/models/ui_data.py | 429 | payoff | f"Tabela {self._payoff_table} não possui colunas esperadas para payoff." |
| UI/models/ui_data.py | 439 | payoff | FROM {self._payoff_table} |
| UI/models/ui_data.py | 452 | payoff | FROM {self._payoff_table} |
| UI/models/ui_data.py | 466 | payoff | FROM {self._payoff_table} |
| UI/models/ui_data.py | 476 | payoff | def get_payoff_curve_info( |
| UI/models/ui_data.py | 487 | payoff | if not self._payoff_table: |
| UI/models/ui_data.py | 502 | payoff | p = self._payoff_cols |
| UI/models/ui_data.py | 516 | payoff | "source_table": self._payoff_table, |
| UI/models/ui_data.py | 524 | payoff | if self._payoff_table == "payoff_curve_points": |
| UI/models/ui_data.py | 527 | payoff | if "meta_json" in self._inspect_columns("payoff_curve_points"): |
| UI/models/ui_data.py | 532 | payoff | f"FROM payoff_curve_points " |
| UI/models/ui_data.py | 541 | payoff | f"SELECT timestamp FROM payoff_curve_points " |
| UI/models/ui_data.py | 562 | payoff | f"Tabela {self._payoff_table} não possui colunas esperadas." |
| UI/models/ui_data.py | 567 | payoff | f"FROM {self._payoff_table} " |
| UI/models/ui_data.py | 576 | payoff | f"SELECT {p['timestamp']} AS ts FROM {self._payoff_table} " |
| UI/models/ui_data.py | 600 | export | def export_to_csv(self, data: List[Dict], filename: str): |
| UI/models/ui_data.py | 639 | payoff | payoff_ok = bool(self._payoff_table) |
| UI/models/ui_data.py | 642 | payoff | p = self._payoff_cols |
| UI/models/ui_data.py | 653 | payoff | f"Tabela de payoff: {self._payoff_table if payoff_ok else 'NÃO ENCONTRADA'}\n" |
| UI/models/ui_data.py | 659 | payoff | self._payoff_cache = {} |
| UI/models/ui_data.py | 667 | payoff | return self._payoff_cache.get(key) |
| UI/models/ui_data.py | 673 | payoff | self._payoff_cache[key] = value |
| UI/models/ui_data.py | 674 | payoff | mx = getattr(self, "_payoff_cache_max", 0) or 0 |
| UI/models/ui_data.py | 675 | payoff | if mx > 0 and len(self._payoff_cache) > mx: |
| UI/models/ui_data.py | 676 | payoff | self._payoff_cache.pop(next(iter(self._payoff_cache))) |
| UI/modern/dark_window.py | 6 | payoff | Ele abre diretamente o TerminalVWAPPayoffDarkPanel, que corresponde |
| UI/modern/dark_window.py | 20 | payoff | from UI.components.terminal_vwap_payoff_dark_panel import TerminalVWAPPayoffDarkPanel |
| UI/modern/dark_window.py | 70 | payoff | self.panel = TerminalVWAPPayoffDarkPanel( |
| UI/modern/main_window.py | 17 | filedialog | from tkinter import filedialog, messagebox, ttk |
| UI/modern/main_window.py | 23 | payoff | from UI.components.payoff_chart import PayoffChart |
| UI/modern/main_window.py | 53 | payoff | self._payoff_worker_id = 0 |
| UI/modern/main_window.py | 54 | payoff | self._loading_payoff = False |
| UI/modern/main_window.py | 160 | export, exportar | self._side_button(sidebar, "Exportar CSV", self.export_csv) |
| UI/modern/main_window.py | 232 | curva, payoff | detail_notebook.add(chart_frame, text="Curva de payoff") |
| UI/modern/main_window.py | 234 | payoff | self.payoff_chart = PayoffChart(chart_frame) |
| UI/modern/main_window.py | 235 | payoff | self.payoff_chart.pack(fill="both", expand=True, padx=4, pady=4) |
| UI/modern/main_window.py | 269 | payoff | notebook.add(tab, text="Terminal VWAP Payoff") |
| UI/modern/main_window.py | 272 | payoff | from controllers.terminal_vwap_payoff_controller import ( |
| UI/modern/main_window.py | 273 | payoff | TerminalVWAPPayoffController, |
| UI/modern/main_window.py | 276 | payoff | from services.terminal_vwap_payoff_app_service import ( |
| UI/modern/main_window.py | 277 | payoff | TerminalVWAPPayoffAppService, |
| UI/modern/main_window.py | 279 | payoff | from UI.components.terminal_vwap_payoff_panel import TerminalVWAPPayoffPanel |
| UI/modern/main_window.py | 282 | payoff | app_service = TerminalVWAPPayoffAppService( |
| UI/modern/main_window.py | 285 | payoff | controller = TerminalVWAPPayoffController(app_service) |
| UI/modern/main_window.py | 287 | payoff | self.terminal_vwap_payoff_panel = TerminalVWAPPayoffPanel( |
| UI/modern/main_window.py | 292 | payoff | self.terminal_vwap_payoff_panel.pack( |
| UI/modern/main_window.py | 303 | payoff | "Terminal VWAP Payoff indisponível neste shell.\n\n" |
| UI/modern/main_window.py | 322 | payoff | # Decisões / filtros / payoff |
| UI/modern/main_window.py | 351 | payoff | self._start_payoff_load(structure_id, timestamp, decision_data) |
| UI/modern/main_window.py | 353 | payoff | self.payoff_chart.clear() |
| UI/modern/main_window.py | 354 | payoff | self.set_status("Dados insuficientes para carregar payoff") |
| UI/modern/main_window.py | 356 | payoff | def _start_payoff_load( |
| UI/modern/main_window.py | 365 | payoff | self._payoff_worker_id += 1 |
| UI/modern/main_window.py | 366 | payoff | worker_id = self._payoff_worker_id |
| UI/modern/main_window.py | 367 | payoff | self._loading_payoff = True |
| UI/modern/main_window.py | 368 | payoff | self.set_status("Carregando payoff...") |
| UI/modern/main_window.py | 372 | payoff | points, info_dict = self.data_model.get_payoff_curve_info( |
| UI/modern/main_window.py | 379 | payoff | f"[ModernUI] payoff structure_id={structure_id} " |
| UI/modern/main_window.py | 407 | payoff | if worker_id != self._payoff_worker_id: |
| UI/modern/main_window.py | 412 | payoff | self._finish_payoff_load, |
| UI/modern/main_window.py | 420 | payoff | if worker_id == self._payoff_worker_id: |
| UI/modern/main_window.py | 423 | payoff | self._handle_payoff_error, |
| UI/modern/main_window.py | 430 | payoff | def _finish_payoff_load( |
| UI/modern/main_window.py | 437 | payoff | if worker_id != self._payoff_worker_id: |
| UI/modern/main_window.py | 440 | payoff | self._loading_payoff = False |
| UI/modern/main_window.py | 444 | payoff | overlays = self.payoff_chart.update_chart(points, decision_data) |
| UI/modern/main_window.py | 462 | payoff | source = (info_dict or {}).get("source_table", "payoff_curve_points") |
| UI/modern/main_window.py | 471 | payoff | self.payoff_chart.clear() |
| UI/modern/main_window.py | 472 | payoff | self.set_status("Sem dados de payoff para esta seleção") |
| UI/modern/main_window.py | 475 | payoff | self._handle_payoff_error(str(exc), worker_id) |
| UI/modern/main_window.py | 477 | payoff | def _handle_payoff_error(self, error_msg: str, worker_id: int) -> None: |
| UI/modern/main_window.py | 478 | payoff | if worker_id != self._payoff_worker_id: |
| UI/modern/main_window.py | 481 | payoff | self._loading_payoff = False |
| UI/modern/main_window.py | 484 | payoff | self.payoff_chart.clear() |
| UI/modern/main_window.py | 488 | payoff | self.set_status(f"Erro ao carregar payoff: {error_msg}") |
| UI/modern/main_window.py | 489 | payoff | print(f"[ModernUI] Erro no payoff: {error_msg}") |
| UI/modern/main_window.py | 531 | payoff | self._start_payoff_load(structure_id, timestamp, previous) |
| UI/modern/main_window.py | 543 | payoff | self.payoff_chart.clear() |
| UI/modern/main_window.py | 557 | export | def export_csv(self) -> None: |
| UI/modern/main_window.py | 558 | filedialog, asksaveasfilename | filename = filedialog.asksaveasfilename( |
| UI/modern/main_window.py | 568 | export | self.data_model.export_to_csv(current_data, filename) |
| UI/modern/main_window.py | 569 | export | messagebox.showinfo("Sucesso", f"Dados exportados para {filename}") |
| UI/modern/main_window.py | 570 | export | self.set_status(f"CSV exportado: {filename}") |
| UI/modern/main_window.py | 572 | export, exportar | messagebox.showerror("Erro", f"Erro ao exportar: {exc}") |
| UI/modern/main_window.py | 573 | export, exportar | self.set_status("Erro ao exportar CSV") |
| UI/modern/main_window.py | 633 | payoff | self.payoff_chart.fix_current_curve() |

## Leitura preliminar

- Exportação PNG está marcada como AUSENTE no modo dark.
- Esta rodada deve indicar se já existe função reaproveitável na UI atual.
- O patch futuro deve reaproveitar função existente sempre que possível.
- Se não houver função existente, o patch futuro deve criar exportação isolada no modo dark.

## Decisão pendente

- Definir arquivo alvo para implementação.
- Definir se o botão será adicionado em área de Payoff ou estrutura.
- Definir fonte da figura/canvas a ser exportada.
- Definir mensagem de sucesso, cancelamento e erro.
