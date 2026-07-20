from services.terminal_vwap_payoff_viewmodel_service import (
    TerminalVWAPPayoffViewModelService,
)


def test_build_terminal_vwap_payoff_viewmodel_with_vwap_and_payoff_points():
    service = TerminalVWAPPayoffViewModelService()

    result = service.build(
        structure={
            "id": 7,
            "name": "Estrutura BOVA11",
            "underlying_asset": "BOVA11",
            "status": "active",
            "legs": [
                {
                    "symbol": "BOVAE195",
                    "position_side": "SHORT",
                    "option_type": "CALL",
                    "quantity": 1000,
                    "premium": "1,25",
                    "strike": "195,00",
                    "expiration_date": "2026-07-17",
                    "source": "canonical",
                }
            ],
        },
        market_snapshot={
            "spot_price": 11.0,
            "vwap": 10.0,
            "source": "rtd_option_quotes",
            "timestamp": "2026-06-29 09:15:00",
        },
        payoff_points=[
            {"underlying_price": 9.0, "result": -100.0},
            {"underlying_price": 10.0, "result": 0.0},
            {"underlying_price": 11.0, "result": 100.0},
        ],
        meta={"test": True},
    )

    assert result["terminal"]["name"] == "ui-terminal-vwap-payoff"
    assert result["terminal"]["ready"] is True

    assert result["structure"]["structure_id"] == 7
    assert result["structure"]["underlying_asset"] == "BOVA11"

    assert len(result["legs"]) == 1
    assert result["legs"][0]["symbol"] == "BOVAE195"
    assert result["legs"][0]["premium"] == 1.25
    assert result["legs"][0]["strike"] == 195.0

    assert result["market"]["current_price"] == 11.0
    assert result["market"]["vwap"] == 10.0
    assert result["market"]["status_vwap"] == "available"
    assert result["market"]["price_vs_vwap_percent"] == 10.0

    assert result["payoff"]["points_count"] == 3
    assert result["payoff"]["min_result"] == -100.0
    assert result["payoff"]["max_result"] == 100.0
    assert result["payoff"]["break_even_points"] == [10.0]

    assert result["meta"]["input_meta"] == {"test": True}
    assert result["meta"]["warnings"] == []


def test_build_terminal_vwap_payoff_viewmodel_handles_missing_vwap_and_empty_payoff():
    service = TerminalVWAPPayoffViewModelService()

    result = service.build(
        structure={
            "structure_id": 99,
            "name": "Estrutura sem VWAP",
            "legs": [],
        },
        market_snapshot={
            "current_price": "12,50",
            "source": "manual",
        },
        payoff_points=[],
    )

    assert result["structure"]["structure_id"] == 99
    assert result["market"]["current_price"] == 12.5
    assert result["market"]["vwap"] is None
    assert result["market"]["price_vs_vwap_percent"] is None
    assert result["market"]["status_vwap"] == "unavailable"

    assert result["payoff"]["points_count"] == 0
    assert result["payoff"]["break_even_points"] == []

    assert "estrutura sem legs" in result["meta"]["warnings"]
    assert "vwap ausente" in result["meta"]["warnings"]
    assert "payoff sem pontos" in result["meta"]["warnings"]


def test_build_terminal_vwap_payoff_viewmodel_estimates_interpolated_break_even():
    service = TerminalVWAPPayoffViewModelService()

    result = service.build(
        structure={
            "structure_id": 123,
            "legs": [{"symbol": "TESTE123"}],
        },
        market_snapshot={
            "current_price": 100,
            "vwap": 100,
        },
        payoff_points=[
            {"underlying_price": 90, "result": -50},
            {"underlying_price": 110, "result": 50},
        ],
    )

    assert result["payoff"]["break_even_points"] == [100.0]
