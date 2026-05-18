from services.pricing_payload_adapter import to_pricing_payload


def test_to_pricing_payload_normalizes_and_converts_fields():
    canonical_input = {
        "structure": {
            "structure_id": 123,
            "name": "  Fence BOVA11 Maio  ",
            "underlying_asset": "\n bova11 ",
            "alias_legacy_aba": "  aba_bova11  ",
            "legs": [
                {
                    "position_side": " long ",
                    "option_type": " put ",
                    "symbol": " bovam190 ",
                    "strike": "190",
                    "expiration_date": " 2026-05-15 ",
                    "quantity": "2",
                    "premium": "1.75",
                    "multiplier": "1",
                }
            ],
        },
        "market": {
            "reference_date": " 2026-05-15 ",
            "spot_price": "198.35",
            "interest_rate": "0.1175",
            "volatility": "0.22",
        },
    }

    result = to_pricing_payload(canonical_input)

    assert result == {
        "structure_id": 123,
        "structure_name": "Fence BOVA11 Maio",
        "underlying_asset": "BOVA11",
        "alias_legacy_aba": "aba_bova11",
        "reference_date": "2026-05-15",
        "spot_price": 198.35,
        "interest_rate": 0.1175,
        "volatility": 0.22,
        "legs": [
            {
                "side": "LONG",
                "instrument_type": "OPTION",
                "option_type": "PUT",
                "symbol": "BOVAM190",
                "strike": 190.0,
                "expiration_date": "2026-05-15",
                "quantity": 2,
                "premium": 1.75,
                "multiplier": 1.0,
            }
        ],
    }


def test_to_pricing_payload_keeps_optional_fields_as_none():
    canonical_input = {
        "structure": {
            "structure_id": 456,
            "name": "Estrutura",
            "underlying_asset": "BOVA11",
            "alias_legacy_aba": None,
            "legs": [
                {
                    "position_side": "SHORT",
                    "option_type": "CALL",
                    "symbol": None,
                    "strike": 210,
                    "expiration_date": "2026-06-19",
                    "quantity": 1,
                    "premium": None,
                    "multiplier": 1,
                }
            ],
        },
        "market": {
            "reference_date": "2026-06-01",
            "spot_price": 200,
            "interest_rate": 0.12,
            "volatility": 0.25,
        },
    }

    result = to_pricing_payload(canonical_input)

    assert result["alias_legacy_aba"] is None
    assert result["legs"][0]["symbol"] is None
    assert result["legs"][0]["premium"] is None
