from __future__ import annotations

from pathlib import Path

from UI.modern import app as modern_app


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def read_project_file(relative_path: str) -> str:
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def test_modern_ui_launcher_keeps_payoff_modes_opt_in() -> None:
    parser = modern_app.build_parser()
    args = parser.parse_args([])

    assert args.mode == "dark"
    assert modern_app.MODES["dark"] == "UI.modern.dark_window"
    assert modern_app.MODES["shell"] == "UI.modern.main_window"


def test_dark_mode_exposes_terminal_vwap_payoff_panel_without_replacing_legacy_ui() -> None:
    source = read_project_file("UI/modern/dark_window.py")

    assert "TerminalVWAPPayoffDarkPanel" in source
    assert "from UI.components.terminal_vwap_payoff_dark_panel import TerminalVWAPPayoffDarkPanel" in source
    assert "self.panel = TerminalVWAPPayoffDarkPanel(" in source
    assert "Este módulo NÃO substitui UI/main_window.py." in source


def test_shell_mode_exposes_payoff_chart_contract() -> None:
    source = read_project_file("UI/modern/main_window.py")

    assert "from UI.components.payoff_chart import PayoffChart" in source
    assert 'detail_notebook.add(chart_frame, text="Curva de payoff")' in source
    assert "self.payoff_chart = PayoffChart(chart_frame)" in source
    assert "self.data_model.get_payoff_curve_info(" in source
    assert "self.payoff_chart.update_chart(points, decision_data)" in source
    assert "Este módulo NÃO substitui UI/main_window.py." in source


def test_modern_payoff_contract_preserves_parallel_ui_route() -> None:
    dark_source = read_project_file("UI/modern/dark_window.py")
    shell_source = read_project_file("UI/modern/main_window.py")

    assert "Este módulo NÃO substitui UI/main_window.py." in dark_source
    assert "Este módulo NÃO substitui UI/main_window.py." in shell_source
    assert "A UI antiga permanece preservada." in dark_source
    assert "UI antiga preservada" in shell_source


def test_modern_payoff_contract_does_not_claim_global_ui_equivalence() -> None:
    app_source = read_project_file("UI/modern/app.py")
    dark_source = read_project_file("UI/modern/dark_window.py")
    shell_source = read_project_file("UI/modern/main_window.py")

    combined = "\n".join([app_source, dark_source, shell_source]).lower()

    forbidden_claims = [
        "equivalência completa",
        "equivalencia completa",
        "equivalência global",
        "equivalencia global",
        "passa a substituir",
        "substitui o entrypoint principal",
        "remove a ui antiga",
        "elimina a ui antiga",
    ]

    for claim in forbidden_claims:
        assert claim not in combined
