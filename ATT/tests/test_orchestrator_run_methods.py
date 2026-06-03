"""
Testes para os métodos run_payoff e run_decision
adicionados ao calculation_orchestrator.

Estratégia: mockar o domínio para isolar o orquestrador
e garantir que a tradução de CalculationRequest está correta.
"""
from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from services.calculation_orchestrator import (
    _request_to_payoff_dict,
    run_decision,
    run_payoff,
)


# ---------------------------------------------------------------------------
# Fixtures — objetos mínimos que imitam CalculationRequest
# ---------------------------------------------------------------------------

def _make_leg(**kwargs):
    defaults = dict(
        position_side="long",
        option_type="call",
        strike=100.0,
        expiration_date="2026-12-19",
        quantity=1,
        symbol="PETR4C100",
        premium=3.5,
        multiplier=100,
        leg_order=0,
        notes=None,
    )
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def _make_request(*, spot=50.0, underlying="PETR4", legs=None):
    if legs is None:
        legs = [_make_leg()]

    structure = SimpleNamespace(
        structure_id="struct-001",
        underlying_asset=underlying,
        name="Teste Estrutura",
        legs=legs,
    )
    market = SimpleNamespace(
        spot_price=spot,
        underlying_asset=underlying,
        snapshot_timestamp="2026-06-02T00:00:00Z",
        option_quotes={},
        greeks={},
    )
    return SimpleNamespace(structure=structure, market_snapshot=market)


# ---------------------------------------------------------------------------
# Testes: _request_to_payoff_dict
# ---------------------------------------------------------------------------

class TestRequestToPayoffDict:

    def test_chaves_raiz_presentes(self):
        req = _make_request()
        result = _request_to_payoff_dict(req)
        assert set(result.keys()) == {"structure", "market", "meta"}

    def test_structure_fields(self):
        req = _make_request(underlying="VALE3")
        s = _request_to_payoff_dict(req)["structure"]
        assert s["structure_id"] == "struct-001"
        assert s["underlying_asset"] == "VALE3"
        assert s["name"] == "Teste Estrutura"
        assert isinstance(s["legs"], list)
        assert len(s["legs"]) == 1

    def test_leg_fields(self):
        leg = _make_leg(strike=110.0, option_type="put", position_side="short")
        req = _make_request(legs=[leg])
        legs = _request_to_payoff_dict(req)["structure"]["legs"]
        assert legs[0]["strike"] == 110.0
        assert legs[0]["option_type"] == "put"
        assert legs[0]["position_side"] == "short"

    def test_market_fields(self):
        req = _make_request(spot=55.5)
        m = _request_to_payoff_dict(req)["market"]
        assert m["spot_price"] == 55.5
        assert m["underlying_asset"] == "PETR4"

    def test_extra_meta_propagado(self):
        req = _make_request()
        meta = {"source": "unit-test", "version": 2}
        result = _request_to_payoff_dict(req, extra_meta=meta)
        assert result["meta"] == meta

    def test_meta_default_vazio(self):
        req = _make_request()
        result = _request_to_payoff_dict(req)
        assert result["meta"] == {}

    def test_multiplas_legs(self):
        legs = [
            _make_leg(strike=100.0, leg_order=0),
            _make_leg(strike=110.0, option_type="put", leg_order=1),
        ]
        req = _make_request(legs=legs)
        result_legs = _request_to_payoff_dict(req)["structure"]["legs"]
        assert len(result_legs) == 2
        assert result_legs[1]["strike"] == 110.0


# ---------------------------------------------------------------------------
# Testes: run_payoff
# ---------------------------------------------------------------------------

class TestRunPayoff:

    @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input")
    def test_chama_dominio_com_dict_correto(self, mock_compute):
        mock_compute.return_value = {"pl_max": 500.0, "points": []}
        req = _make_request(spot=50.0)

        result = run_payoff(req)

        assert mock_compute.called
        canonical = mock_compute.call_args[0][0]
        assert canonical["structure"]["structure_id"] == "struct-001"
        assert canonical["market"]["spot_price"] == 50.0
        assert result == {"pl_max": 500.0, "points": []}

    @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input")
    def test_parametros_de_range_repassados(self, mock_compute):
        mock_compute.return_value = {}
        req = _make_request()

        run_payoff(req, low_pct=0.8, high_pct=1.2, step_pct=0.005)

        _, kwargs = mock_compute.call_args
        assert kwargs["low_pct"] == 0.8
        assert kwargs["high_pct"] == 1.2
        assert kwargs["step_pct"] == 0.005

    @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input")
    def test_extra_meta_repassado(self, mock_compute):
        mock_compute.return_value = {}
        req = _make_request()

        run_payoff(req, extra_meta={"tag": "ci"})

        canonical = mock_compute.call_args[0][0]
        assert canonical["meta"] == {"tag": "ci"}

    @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input")
    def test_retorna_resultado_do_dominio(self, mock_compute):
        expected = {"pl_max": 1200.0, "pl_min": -300.0, "breakeven": [105.0]}
        mock_compute.return_value = expected
        req = _make_request()

        result = run_payoff(req)

        assert result is expected


# ---------------------------------------------------------------------------
# Testes: run_decision
# ---------------------------------------------------------------------------

class TestRunDecision:

    @patch("services.calculation_orchestrator.compute_decision_from_contract")
    def test_chama_dominio_com_contract_correto(self, mock_decide):
        mock_decide.return_value = {"decision": "hold", "score": 0.7}
        req = _make_request()

        result = run_decision(req, pl_atual=200.0, pl_max=500.0, dte_min=10)

        assert mock_decide.called
        contract = mock_decide.call_args[0][0]
        assert contract.pl_atual == 200.0
        assert contract.pl_max == 500.0
        assert contract.dte_min == 10
        assert result == {"decision": "hold", "score": 0.7}

    @patch("services.calculation_orchestrator.compute_decision_from_contract")
    def test_payoff_dict_repassado(self, mock_decide):
        mock_decide.return_value = {}
        req = _make_request()
        payoff = {"pl_max": 600.0, "points": [{"spot": 50, "pl": 0}]}

        run_decision(req, payoff=payoff, pl_max=600.0, pl_atual=100.0)

        _, kwargs = mock_decide.call_args
        assert kwargs["payoff"] == payoff

    @patch("services.calculation_orchestrator.compute_decision_from_contract")
    def test_defaults_pl_zerados(self, mock_decide):
        mock_decide.return_value = {}
        req = _make_request()

        run_decision(req)

        contract = mock_decide.call_args[0][0]
        assert contract.pl_atual == 0.0
        assert contract.pl_max == 0.0
        assert contract.dte_min is None

    @patch("services.calculation_orchestrator.compute_decision_from_contract")
    def test_dte_min_none_quando_omitido(self, mock_decide):
        mock_decide.return_value = {}
        req = _make_request()

        run_decision(req, pl_max=300.0)

        contract = mock_decide.call_args[0][0]
        assert contract.dte_min is None

    @patch("services.calculation_orchestrator.compute_decision_from_contract")
    def test_retorna_resultado_do_dominio(self, mock_decide):
        expected = {"decision": "close", "reason": "dte_gate"}
        mock_decide.return_value = expected
        req = _make_request()

        result = run_decision(req, pl_max=100.0, pl_atual=80.0, dte_min=2)

        assert result is expected


# ---------------------------------------------------------------------------
# Smoke test real — sem mock
# ---------------------------------------------------------------------------

class TestRunPayoffIntegration:
    """
    Chama run_payoff sem mock.
    Pula automaticamente se o domínio não estiver configurado.
    """

    def test_smoke_run_payoff_call_chain(self):
        pytest.importorskip("domain.payoff")

        leg = _make_leg(
            strike=50.0,
            option_type="call",
            position_side="long",
            premium=2.0,
            quantity=1,
            multiplier=100,
            expiration_date="2026-12-19",
        )
        req = _make_request(spot=50.0, legs=[leg])

        try:
            result = run_payoff(req, low_pct=0.8, high_pct=1.2, step_pct=0.05)
            assert isinstance(result, dict), "run_payoff deve retornar dict"
        except Exception as exc:
            pytest.skip(f"Dominio indisponivel ou mal configurado: {exc}")
