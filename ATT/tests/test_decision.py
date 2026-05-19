from domain.decision import compute_decision_from_contract


def test_compute_decision_from_contract_should_work_with_canonical_payload_without_alias_legacy_aba():
    canonical_input = {
        "structure": {
            "structure_id": 7,
            "name": "BOVA11 Condor Maio/2026",
            "underlying_asset": "BOVA11",
            "legs": [
                {
                    "position_side": "LONG",
                    "option_type": "CALL",
                    "symbol": "BOVAE195",
                    "strike": 195.0,
                    "expiration_date": "2026-05-30",
                    "quantity": 1,
                    "premium": 1.0,
                    "multiplier": 1.0,
                }
            ],
        },
        "market": {
            "reference_date": "2026-05-18",
            "underlying_asset": "BOVA11",
            "spot_price": 198.35,
            "interest_rate": 0.1175,
            "volatility": 0.22,
        },
        "meta": {
            "reference_date": "2026-05-18",
            "legs_source": "canonical",
            "input_source": "test",
        },
    }

    result = compute_decision_from_contract(canonical_input, dte_min=12)

    assert "decision" in result
    assert "why" in result
    assert result["dte_min"] == 12
