from domain.canonical_validators import validate_canonical_input


def test_validate_canonical_input_returns_no_errors_for_valid_payload():
    canonical_input = {
        "structure": {
            "structure_id": 1,
            "underlying_asset": "BOVA11",
            "legs": [
                {
                    "position_side": "LONG",
                    "option_type": "PUT",
                    "strike": 190.0,
                    "quantity": 2000,
                    "expiration_date": "2026-05-15",
                }
            ],
        },
        "market": {
            "spot_price": 198.35,
            "reference_date": "2026-05-15",
        },
    }

    assert validate_canonical_input(canonical_input) == []


def test_validate_canonical_input_returns_errors_for_missing_top_level_fields():
    canonical_input = {
        "structure": {
            "legs": [],
        },
        "market": {},
    }

    errors = validate_canonical_input(canonical_input)

    assert "structure.structure_id is required" in errors
    assert "structure.underlying_asset is required" in errors
    assert "structure.legs must not be empty" in errors
    assert "market.spot_price is required" in errors
    assert "market.reference_date is required" in errors


def test_validate_canonical_input_returns_errors_for_invalid_leg_fields():
    canonical_input = {
        "structure": {
            "structure_id": 1,
            "underlying_asset": "BOVA11",
            "legs": [
                {
                    "position_side": None,
                    "option_type": None,
                    "strike": None,
                    "quantity": None,
                    "expiration_date": None,
                }
            ],
        },
        "market": {
            "spot_price": 198.35,
            "reference_date": "2026-05-15",
        },
    }

    errors = validate_canonical_input(canonical_input)

    assert "structure.legs[0].position_side is required" in errors
    assert "structure.legs[0].option_type is required" in errors
    assert "structure.legs[0].strike is required" in errors
    assert "structure.legs[0].quantity is required" in errors
    assert "structure.legs[0].expiration_date is required" in errors
