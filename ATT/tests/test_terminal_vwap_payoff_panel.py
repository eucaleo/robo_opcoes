from UI.components.terminal_vwap_payoff_panel import (
    _extract_leg_table_rows,
    _extract_payoff_table_rows,
    _format_currency_br,
    _format_number_br,
    _format_percent_br,
    _summarize_viewmodel,
)


def _viewmodel():
    return {
        "structure": {
            "structure_id": 7,
            "name": "Trava BOVA11",
            "underlying_asset": "BOVA11",
            "status": "active",
        },
        "market": {
            "current_price": 11,
            "vwap": 10,
            "price_vs_vwap_percent": 10,
            "source": "teste",
            "timestamp": "2026-06-29 12:00:00",
        },
        "legs": [
            {
                "leg_order": 1,
                "symbol": "BOVAE195",
                "position_side": "COMPRADO",
                "option_type": "CALL",
                "strike": 195,
                "expiration_date": "2026-07-17",
                "quantity": 1000,
                "premium": 1.25,
            }
        ],
        "payoff": {
            "points": [
                {"underlying_price": 9, "result": -100},
                {"underlying_price": 10, "result": 0},
                {"underlying_price": 11, "result": 100},
            ],
            "points_count": 3,
            "min_result": -100,
            "max_result": 100,
            "break_even_points": [10],
        },
        "meta": {
            "warnings": [],
        },
    }


def test_terminal_panel_formatters_use_pt_br_conventions():
    assert _format_number_br(1234.5, 2) == "1.234,50"
    assert _format_currency_br(-1000, 2) == "R$ -1.000,00"
    assert _format_percent_br(10, 2) == "10,00%"
    assert _format_number_br(None, 2) == "N/A"


def test_terminal_panel_summarizes_viewmodel_for_ui_labels():
    summary = _summarize_viewmodel(_viewmodel())

    assert summary["structure_id"] == "7"
    assert summary["name"] == "Trava BOVA11"
    assert summary["underlying_asset"] == "BOVA11"
    assert summary["current_price"] == "11,00"
    assert summary["vwap"] == "10,00"
    assert summary["price_vs_vwap_percent"] == "10,00%"
    assert summary["min_result"] == "R$ -100,00"
    assert summary["max_result"] == "R$ 100,00"
    assert summary["break_even_points"] == "10,00"


def test_terminal_panel_extracts_leg_rows_without_tk_display():
    rows = _extract_leg_table_rows(_viewmodel())

    assert rows == [
        (
            "1",
            "BOVAE195",
            "COMPRADO",
            "CALL",
            "195,00",
            "2026-07-17",
            "1.000",
            "R$ 1,25",
        )
    ]


def test_terminal_panel_extracts_payoff_rows_without_tk_display():
    rows = _extract_payoff_table_rows(_viewmodel())

    assert rows == [
        ("9,00", "R$ -100,00"),
        ("10,00", "R$ 0,00"),
        ("11,00", "R$ 100,00"),
    ]


def test_terminal_panel_extracts_limited_payoff_rows():
    rows = _extract_payoff_table_rows(_viewmodel(), limit=2)

    assert rows == [
        ("9,00", "R$ -100,00"),
        ("10,00", "R$ 0,00"),
    ]
