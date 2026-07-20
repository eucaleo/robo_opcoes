from domain.contracts import CanonicalStructureMarketInput


def test_canonical_structure_market_input_from_dict_and_to_dict_without_alias_legacy_aba():
    payload = {
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
                    "quantity": 5000,
                    "premium": None,
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
            "legacy_timestamp": None,
            "input_source": "test",
        },
    }

    canonical_input = CanonicalStructureMarketInput.from_dict(payload)
    result = canonical_input.to_dict()

    assert result["structure"]["structure_id"] == 7
    assert result["structure"]["name"] == "BOVA11 Condor Maio/2026"
    assert result["structure"]["underlying_asset"] == "BOVA11"
    assert "alias_legacy_aba" not in result["structure"]
    assert result["meta"]["legs_source"] == "canonical"
    assert "legacy_timestamp" in result["meta"]
