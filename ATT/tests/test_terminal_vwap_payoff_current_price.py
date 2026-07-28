from services.terminal_vwap_payoff_viewmodel_service import (
    TerminalVWAPPayoffViewModelService,
)


def test_viewmodel_prioriza_current_price_sem_alterar_premium():
    service = TerminalVWAPPayoffViewModelService()

    result = service._build_leg_viewmodel(
        {
            "symbol": "PETRA123",
            "premium": 2.15,
            "current_price": 3.40,
            "ultimo_preco": 3.10,
            "last_price": 3.00,
            "price": 2.90,
        },
        index=1,
    )

    assert result["premium"] == 2.15
    assert result["current_price"] == 3.40
