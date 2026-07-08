from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def import_terminal_vwap_panel_module():
    path = ROOT / "UI/components/terminal_vwap_payoff_panel.py"
    spec = importlib.util.spec_from_file_location(
        "terminal_vwap_payoff_panel_contract",
        path,
    )
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_m9_wiring_test_infrastructure_is_really_present():
    source = read_text("ATT/tests/test_ui_modern_dark_window_terminal_vwap_wiring.py")

    assert "FakeUIDataModel" in source
    assert "patch_window_dependencies" in source

    assert (
        "test_modern_dark_window_load_structure_from_decision_is_idempotent_when_already_selected"
        in source
    )
    assert (
        "test_modern_dark_window_load_structure_from_decision_keeps_valid_selection_after_missing_structure"
        in source
    )


def test_m9_is_not_documented_as_functional_closure():
    source = read_text("docs/auditoria/UI_TERMINAL_VWAP_M10_RECONCILIACAO_ROTA.md")

    assert "A M9 nao implementou novo fluxo funcional macro" in source
    assert "A M9 nao validou integralmente" in source

    expected_open_items = [
        "fluxo completo de estruturas",
        "fluxo completo de pernas",
        "estados vazios visuais",
        "mensagens de status em execucao real",
        "KPIs",
        "graficos",
        "matriz final de equivalencia",
        "validacao manual assistida",
        "equivalencia funcional completa contra UI canonica",
    ]

    missing = [item for item in expected_open_items if item not in source]
    assert not missing, f"Itens abertos ausentes da M10: {missing}"


def test_m11_is_documental_and_does_not_claim_functional_validation():
    source = read_text("docs/auditoria/UI_TERMINAL_VWAP_M11_VALIDACAO_ASSISTIDA.md")

    assert "Esta M11 e exclusivamente documental" in source
    assert "Esta M11 nao afirma que o Terminal VWAP moderno esta funcionalmente validado" in source
    assert "M11-01" in source
    assert "M11-14" in source


def test_terminal_vwap_panel_helpers_tolerate_malformed_viewmodel_payloads():
    module = import_terminal_vwap_panel_module()

    viewmodel = {
        "structure": "estrutura-malformada",
        "market": ["mercado-malformado"],
        "payoff": {
            "points": [
                None,
                "ponto-malformado",
                {
                    "underlying_price": "10,50",
                    "result": "-1.234,50",
                },
            ],
            "break_even_points": ["10,00", None, "abc"],
        },
        "legs": [
            None,
            "leg-malformada",
            {
                "leg_order": 1,
                "symbol": "PETR4",
                "position_side": "LONG",
                "option_type": "CALL",
                "strike": "30,50",
                "expiration_date": "2026-08-21",
                "quantity": "100",
                "premium": "1,25",
            },
        ],
        "meta": "meta-malformada",
    }

    summary = module._summarize_viewmodel(viewmodel)
    assert summary["structure_id"] == "N/A"
    assert summary["name"] == "N/A"
    assert summary["current_price"] == "N/A"
    assert summary["vwap"] == "N/A"

    legs = module._extract_leg_table_rows(viewmodel)
    assert legs == [
        (
            "1",
            "PETR4",
            "LONG",
            "CALL",
            "30,50",
            "2026-08-21",
            "100",
            "R$ 1,25",
        )
    ]

    payoff_rows = module._extract_payoff_table_rows(viewmodel)
    assert payoff_rows == [
        ("10,50", "R$ -1.234,50"),
    ]


def test_terminal_vwap_panel_empty_viewmodel_has_safe_summary_defaults():
    module = import_terminal_vwap_panel_module()

    summary = module._summarize_viewmodel({})

    assert summary == {
        "structure_id": "N/A",
        "name": "N/A",
        "underlying_asset": "N/A",
        "status": "N/A",
        "current_price": "N/A",
        "vwap": "N/A",
        "price_vs_vwap_percent": "N/A",
        "market_source": "N/A",
        "market_timestamp": "N/A",
        "points_count": "N/A",
        "min_result": "N/A",
        "max_result": "N/A",
        "break_even_points": "N/A",
    }


def test_existing_wiring_tests_include_required_behavioral_regression_terms():
    source = read_text("ATT/tests/test_ui_modern_dark_window_terminal_vwap_wiring.py").lower()

    required_terms = [
        "missing_structure",
        "idempotent",
        "invalid",
        "zero",
        "selection",
        "load_structure",
    ]

    missing = [term for term in required_terms if term not in source]
    assert not missing, f"Cobertura esperada ausente no wiring Terminal VWAP: {missing}"
