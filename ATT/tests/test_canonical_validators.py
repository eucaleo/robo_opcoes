from domain.canonical_validators import validate_canonical_input


def test_validate_canonical_input_should_not_require_alias_legacy_aba():
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
                    "premium": None,
                    "multiplier": 1.0,
                }
            ],
        },
        "market": {
            "reference_date": "2026-05-18",
            "underlying_asset": "BOVA11",
            "spot_price": 198.35,
        },
    }

    errors = validate_canonical_input(canonical_input)

    assert errors == []
