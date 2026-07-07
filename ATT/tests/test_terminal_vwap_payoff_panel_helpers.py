from UI.components import terminal_vwap_payoff_panel as panel


def test_summarize_viewmodel_tolerates_non_mapping_input():
    summary = panel._summarize_viewmodel("entrada invalida")

    assert summary["structure_id"] == "N/A"
    assert summary["name"] == "N/A"
    assert summary["current_price"] == "N/A"
    assert summary["break_even_points"] == "N/A"


def test_extract_leg_rows_skips_malformed_items():
    viewmodel = {
        "legs": [
            None,
            "ignorar",
            {
                "leg_order": 1,
                "symbol": "PETR4C30",
                "position_side": "BUY",
                "option_type": "CALL",
                "strike": "30,50",
                "expiration_date": "2026-08-21",
                "quantity": 100,
                "premium": "1,25",
            },
        ]
    }

    rows = panel._extract_leg_table_rows(viewmodel)

    assert rows == [
        (
            "1",
            "PETR4C30",
            "BUY",
            "CALL",
            "30,50",
            "2026-08-21",
            "100",
            "R$ 1,25",
        )
    ]


def test_extract_payoff_rows_tolerates_invalid_points_and_limit():
    viewmodel = {
        "payoff": {
            "points": [
                None,
                {"underlying_price": "29,5", "result": "-1000,25"},
                {"underlying_price": 31, "result": 250.5},
            ]
        }
    }

    rows = panel._extract_payoff_table_rows(viewmodel, limit=1)

    assert rows == [("29,50", "R$ -1.000,25")]


def test_extract_payoff_rows_tolerates_non_mapping_payoff():
    assert panel._extract_payoff_table_rows({"payoff": "indisponivel"}) == []


def test_formatters_keep_safe_fallbacks():
    assert panel._format_number_br(None) == "N/A"
    assert panel._format_currency_br("abc") == "N/A"
    assert panel._format_percent_br("") == "N/A"
    assert panel._safe_text("  ") == "N/A"


def test_iter_mappings_rejects_strings_and_plain_mappings():
    assert panel._iter_mappings("abc") == []
    assert panel._iter_mappings({"a": 1}) == []
    assert panel._iter_mappings([{"a": 1}, "x", None, {"b": 2}]) == [
        {"a": 1},
        {"b": 2},
    ]
