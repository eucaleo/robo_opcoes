from domain.contracts import CanonicalStructureMarketInput
from domain.decision import (
    compute_decision_for_aba,
    compute_decision_from_contract,
    compute_decision_from_inputs,
    compute_decision_from_payoff,
)


def test_compute_decision_includes_why_and_why_json():
    payoff = {
        "pl_max": 10000.0,
        "pl_min": 0.0,
        "spot_ref": 198.35,
        "points": [
            (190.0, 10000.0),
            (198.35, 0.0),
            (210.0, 0.0),
        ],
        "structure_id": 1,
        "structure_name": "Teste",
        "underlying_asset": "BOVA11",
        "reference_date": "2026-05-15",
        "input_meta": {"legs_source": "canonical"},
    }

    result = compute_decision_from_payoff(
        payoff=payoff,
        dte_min=0,
        spread_pct_medio=0.02,
    )

    assert result["decision"] == "HOLD"
    assert "why" in result
    assert "why_json" in result
    assert isinstance(result["why"], dict)
    assert "reasons" in result["why"]
    assert "alternatives" in result["why"]
    assert result["why"]["thresholds_used"]["watch"] == 0.30


def test_compute_decision_from_inputs_watch_level():
    result = compute_decision_from_inputs(
        pl_atual=35.0,
        pl_max=100.0,
        dte_min=20,
    )

    assert result["decision"] == "HOLD"
    assert result["level"] == 1
    assert result["pl_pct_of_max"] == 0.35


def test_compute_decision_from_inputs_prepare_roll():
    result = compute_decision_from_inputs(
        pl_atual=65.0,
        pl_max=100.0,
        dte_min=20,
    )

    assert result["decision"] == "PREPARE_ROLL"
    assert result["level"] == 2
    assert result["pl_pct_of_max"] == 0.65


def test_compute_decision_from_inputs_close_reopen_by_threshold():
    result = compute_decision_from_inputs(
        pl_atual=85.0,
        pl_max=100.0,
        dte_min=20,
    )

    assert result["decision"] == "CLOSE_REOPEN"
    assert result["level"] == 3
    assert result["pl_pct_of_max"] == 0.85


def test_compute_decision_from_inputs_close_reopen_by_dte_gate():
    result = compute_decision_from_inputs(
        pl_atual=65.0,
        pl_max=100.0,
        dte_min=5,
        dte_gate=7,
    )

    assert result["decision"] == "CLOSE_REOPEN"
    assert result["level"] == 3
    assert any("Gate DTE" in reason for reason in result["why"]["reasons"])


def test_compute_decision_from_inputs_adds_spread_warning():
    result = compute_decision_from_inputs(
        pl_atual=20.0,
        pl_max=100.0,
        dte_min=20,
        spread_pct_medio=0.02,
    )

    assert any("Spread alto" in alt for alt in result["why"]["alternatives"])


def test_compute_decision_from_payoff_returns_error_for_invalid_payoff():
    payoff = {
        "points": [],
        "pl_max": 0.0,
        "meta": {
            "validation_errors": ["missing structure legs"],
        },
        "structure_id": 10,
        "structure_name": "Estrutura inválida",
        "underlying_asset": "BOVA11",
        "reference_date": "2026-05-15",
    }

    result = compute_decision_from_payoff(
        payoff=payoff,
        dte_min=12,
    )

    assert result["decision"] == "HOLD"
    assert result["level"] == 0
    assert result["why"]["error"] == "payoff is required"
    assert result["why"]["validation_errors"] == ["missing structure legs"]


def test_compute_decision_from_contract_with_dict():
    contract = {
        "structure": {
            "structure_id": 1,
            "name": "Teste",
            "underlying_asset": "BOVA11",
            "legs": [
                {
                    "position_side": "SHORT",
                    "option_type": "PUT",
                    "symbol": "BOVAP1",
                    "strike": 100.0,
                    "expiration_date": "2026-06-20",
                    "quantity": 1,
                    "premium": 5.0,
                    "multiplier": 1.0,
                }
            ],
        },
        "market": {
            "reference_date": "2026-05-15",
            "underlying_asset": "BOVA11",
            "spot_price": 100.0,
        },
        "meta": {
            "reference_date": "2026-05-15",
            "legs_source": "canonical",
        },
    }

    result = compute_decision_from_contract(
        contract=contract,
        dte_min=15,
    )

    assert "decision" in result
    assert "why" in result
    assert result["why"]["extra_info"]["structure_id"] == 1
    assert result["dte_min"] == 15


def test_compute_decision_from_contract_infers_dte_min_when_not_provided():
    contract = {
        "structure": {
            "structure_id": 3,
            "name": "Teste DTE Inferido",
            "underlying_asset": "BOVA11",
            "legs": [
                {
                    "position_side": "LONG",
                    "option_type": "PUT",
                    "symbol": "BOVAP1",
                    "strike": 100.0,
                    "expiration_date": "2026-05-20",
                    "quantity": 1,
                    "premium": 1.0,
                    "multiplier": 1.0,
                },
                {
                    "position_side": "SHORT",
                    "option_type": "PUT",
                    "symbol": "BOVAP2",
                    "strike": 95.0,
                    "expiration_date": "2026-05-17",
                    "quantity": 1,
                    "premium": 0.5,
                    "multiplier": 1.0,
                },
            ],
        },
        "market": {
            "reference_date": "2026-05-15",
            "underlying_asset": "BOVA11",
            "spot_price": 100.0,
        },
        "meta": {
            "reference_date": "2026-05-15",
            "legs_source": "canonical",
        },
    }

    result = compute_decision_from_contract(
        contract=contract,
    )

    assert "decision" in result
    assert "why" in result
    assert result["why"]["extra_info"]["structure_id"] == 3
    assert result["dte_min"] == 2


def test_compute_decision_from_contract_with_dataclass():
    contract = CanonicalStructureMarketInput.from_dict(
        {
            "structure": {
                "structure_id": 2,
                "name": "Teste Dataclass",
                "underlying_asset": "BOVA11",
                "legs": [
                    {
                        "position_side": "LONG",
                        "option_type": "CALL",
                        "symbol": "BOVAC1",
                        "strike": 90.0,
                        "expiration_date": "2026-06-20",
                        "quantity": 1,
                        "premium": 2.0,
                        "multiplier": 1.0,
                    }
                ],
            },
            "market": {
                "reference_date": "2026-05-15",
                "underlying_asset": "BOVA11",
                "spot_price": 100.0,
            },
            "meta": {
                "reference_date": "2026-05-15",
                "legs_source": "canonical",
            },
        }
    )

    result = compute_decision_from_contract(
        contract=contract,
        dte_min=15,
    )

    assert "decision" in result
    assert "why" in result
    assert result["why"]["extra_info"]["structure_id"] == 2


def test_compute_decision_for_aba_returns_structured_error_when_legacy_path_unavailable():
    result = compute_decision_for_aba(
        aba="ABA_TESTE",
        pl_max=1000.0,
    )

    assert result["decision"] == "HOLD"
    assert result["level"] == 0
    assert result["why"]["error"] == "legacy aba decision path unavailable"
    assert result["why"]["aba"] == "ABA_TESTE"
