from services.structure_input_mapper import to_structure_input


def test_to_structure_input_normalizes_top_level_and_legs_fields():
    structure = {
        "id": 10,
        "name": "  Fence BOVA11  ",
        "underlying_asset": "\n bova11 ",
        "alias_legacy_aba": "  aba_bova11  ",
        "legs": [
            {
                "position_side": " long ",
                "option_type": " put ",
                "symbol": " bovam190 ",
                "strike": 190,
                "expiration_date": " 2026-05-15 ",
                "quantity": 2,
                "premium": None,
                "multiplier": 1,
            }
        ],
    }

    result = to_structure_input(structure)

    assert result == {
        "structure_id": 10,
        "name": "Fence BOVA11",
        "underlying_asset": "BOVA11",
        "alias_legacy_aba": "aba_bova11",
        "legs": [
            {
                "position_side": "LONG",
                "option_type": "PUT",
                "symbol": "BOVAM190",
                "strike": 190,
                "expiration_date": "2026-05-15",
                "quantity": 2,
                "premium": None,
                "multiplier": 1,
            }
        ],
    }


def test_to_structure_input_keeps_symbol_as_none_when_missing():
    structure = {
        "id": 11,
        "name": "Estrutura",
        "underlying_asset": "BOVA11",
        "legs": [
            {
                "position_side": "SHORT",
                "option_type": "CALL",
                "symbol": None,
                "strike": 210.0,
                "expiration_date": "2026-06-19",
                "quantity": 1,
                "premium": 3.5,
                "multiplier": 1.0,
            }
        ],
    }

    result = to_structure_input(structure)

    assert result["legs"][0]["symbol"] is None
