from domain.payoff import compute_payoff_from_canonical_input


def test_compute_payoff_from_canonical_input_ok():
    canonical_input = {
        "structure": {
            "structure_id": 1,
            "name": "Teste",
            "underlying_asset": "BOVA11",
            "legs": [
                {
                    "position_side": "LONG",
                    "option_type": "PUT",
                    "symbol": "X",
                    "strike": 190.0,
                    "expiration_date": "2026-05-15",
                    "quantity": 2000,
                    "premium": None,
                    "multiplier": 1.0,
                },
                {
                    "position_side": "SHORT",
                    "option_type": "PUT",
                    "symbol": "Y",
                    "strike": 185.0,
                    "expiration_date": "2026-05-15",
                    "quantity": 2000,
                    "premium": None,
                    "multiplier": 1.0,
                },
            ],
        },
        "market": {
            "reference_date": "2026-05-15",
            "underlying_asset": "BOVA11",
            "spot_price": 198.35,
            "interest_rate": 0.1175,
            "volatility": 0.22,
        },
        "meta": {
            "reference_date": "2026-05-15",
            "legs_source": "canonical",
        },
    }

    payoff = compute_payoff_from_canonical_input(canonical_input)

    assert payoff is not None
    assert payoff["pl_max"] == 10000.0
    assert payoff["pl_min"] == 0.0
    assert payoff["spot_ref"] == 198.35


def test_compute_payoff_from_canonical_input_validation_error():
    canonical_input = {
        "structure": {
            "structure_id": 1,
            "underlying_asset": "BOVA11",
            "legs": [],
        },
        "market": {
            "reference_date": "2026-05-15",
            "spot_price": 198.35,
        },
    }

    payoff = compute_payoff_from_canonical_input(canonical_input)

    assert payoff["pl_max"] == 0.0
    assert payoff["pl_min"] == 0.0
    assert payoff["meta"]["validation_errors"] == ["structure.legs must not be empty"]
