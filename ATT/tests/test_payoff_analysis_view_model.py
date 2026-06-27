from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.payoff_analysis_view_model import (
    calcular_intrinseco,
    calcular_payoff_vencimento_perna,
    calcular_pl_atual_perna,
    montar_view_model_payoff_analitico,
)


def test_intrinseco_call_e_put():
    assert calcular_intrinseco("CALL", 110.0, 100.0) == 10.0
    assert calcular_intrinseco("CALL", 90.0, 100.0) == 0.0
    assert calcular_intrinseco("PUT", 90.0, 100.0) == 10.0
    assert calcular_intrinseco("PUT", 110.0, 100.0) == 0.0


def test_pl_atual_perna_comprada_e_vendida():
    assert calcular_pl_atual_perna("BUY", 2.0, 5.0, 100.0) == 300.0
    assert calcular_pl_atual_perna("SELL", 2.0, 5.0, 100.0) == -300.0


def test_payoff_vencimento_call_comprada():
    resultado = calcular_payoff_vencimento_perna(
        tipo="CALL",
        direcao="BUY",
        preco_simulado=110.0,
        strike=100.0,
        premio_entrada=2.0,
        quantidade=100.0,
    )

    assert resultado == 800.0


def test_payoff_vencimento_put_vendida():
    resultado = calcular_payoff_vencimento_perna(
        tipo="PUT",
        direcao="SELL",
        preco_simulado=90.0,
        strike=100.0,
        premio_entrada=3.0,
        quantidade=100.0,
    )

    assert resultado == -700.0


def test_view_model_payoff_analitico_com_duas_pernas():
    payload = {
        "structure_id": 10,
        "name": "Trava de alta teste",
        "underlying_asset": "BOVA11",
        "deployed_at": "2026-06-01T10:00:00",
        "calculated_at": "2026-06-27T18:00:00",
        "expiration_date": "2026-08-21",
        "underlying_price_at_deployment": 160.0,
        "current_underlying_price": 170.0,
        "market_snapshot_source": "rtd_underlying_quotes",
        "is_static_fallback": False,
        "is_current_market": True,
        "legs": [
            {
                "ticker": "BOVAG160",
                "type": "CALL",
                "side": "BUY",
                "quantity": 100,
                "strike": 160,
                "expirationDate": "2026-08-21",
                "entryPremium": 5.0,
                "currentPremium": 12.0,
            },
            {
                "ticker": "BOVAG180",
                "type": "CALL",
                "side": "SELL",
                "quantity": 100,
                "strike": 180,
                "expirationDate": "2026-08-21",
                "entryPremium": 2.0,
                "currentPremium": 4.0,
            },
        ],
    }

    vm = montar_view_model_payoff_analitico(payload)

    assert vm["validacao"]["status"] == "ok"
    assert vm["identificacao_estrutura"]["structure_id"] == 10
    assert vm["snapshot_implantacao"]["preco_base_na_implantacao"] == 160.0
    assert vm["snapshot_atual"]["preco_base_atual"] == 170.0
    assert vm["snapshot_atual"]["fonte_preco_atual"] == "rtd_underlying_quotes"
    assert len(vm["tabela_pernas"]) == 2

    primeira = vm["tabela_pernas"][0]
    segunda = vm["tabela_pernas"][1]

    assert primeira["intrinseco_atual"] == 10.0
    assert primeira["extrinseco_atual"] == 2.0
    assert primeira["pl_atual"] == 700.0

    assert segunda["intrinseco_atual"] == 0.0
    assert segunda["extrinseco_atual"] == 4.0
    assert segunda["pl_atual"] == -200.0

    assert vm["snapshot_atual"]["pl_atual_financeiro"] == 500.0
    assert vm["payoff_vencimento"]["payoff_no_vencimento_ao_preco_atual"] == 700.0


def test_view_model_bloqueia_fallback_estatico():
    payload = {
        "structure_id": 20,
        "underlying_asset": "PRIO3",
        "underlying_price_at_deployment": 50.0,
        "current_underlying_price": 53.2,
        "market_snapshot_source": "static_fallback",
        "is_static_fallback": True,
        "legs": [
            {
                "ticker": "PRIOH505",
                "type": "CALL",
                "side": "BUY",
                "quantity": 100,
                "strike": 50.5,
                "expirationDate": "2026-08-21",
                "entryPremium": 2.0,
                "currentPremium": 4.97,
            }
        ],
    }

    vm = montar_view_model_payoff_analitico(payload)

    assert vm["validacao"]["status"] == "erro"
    assert "fonte de mercado esta em fallback estatico" in vm["validacao"]["erros"]
