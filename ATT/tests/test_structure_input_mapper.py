from services.structure_input_mapper import to_structure_input


def test_to_structure_input_should_not_expose_alias_legacy_aba():
    structure = {
        "id": 7,
        "name": "  BOVA11 Condor Maio/2026  ",
        "underlying_asset": " bova11 ",
        "alias_legacy_aba": "BOVA11",
        "legs": [
            {
                "position_side": "long",
                "option_type": "call",
                "symbol": " bovae195 ",
                "strike": 195.0,
                "expiration_date": " 2026-05-15 ",
                "quantity": 5000,
                "premium": None,
                "multiplier": 1.0,
            }
        ],
    }

    result = to_structure_input(structure)

    assert result["structure_id"] == 7
    assert result["name"] == "BOVA11 Condor Maio/2026"
    assert result["underlying_asset"] == "BOVA11"
    assert "alias_legacy_aba" not in result
    assert len(result["legs"]) == 1
    assert result["legs"][0]["position_side"] == "LONG"
    assert result["legs"][0]["option_type"] == "CALL"
    assert result["legs"][0]["symbol"] == "BOVAE195"
