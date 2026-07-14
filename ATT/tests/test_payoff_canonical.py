from domain.payoff import compute_payoff_from_canonical_input


def test_compute_payoff_from_canonical_input_should_preserve_canonical_metadata():
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
                    "expiration_date": "2026-05-15",
                    "quantity": 1,
                    "premium": 2.0,
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

    result = compute_payoff_from_canonical_input(canonical_input)

    assert result["structure_id"] == 7
    assert result["structure_name"] == "BOVA11 Condor Maio/2026"
    assert result["underlying_asset"] == "BOVA11"
    assert result["reference_date"] == "2026-05-18"
    assert result["input_meta"]["legs_source"] == "canonical"
