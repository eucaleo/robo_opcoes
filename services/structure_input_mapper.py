from typing import Any


def to_structure_input(structure: dict[str, Any]) -> dict[str, Any]:
    if not structure:
        raise ValueError("structure is required")

    legs = structure.get("legs", [])

    return {
        "structure_id": structure["id"],
        "name": structure["name"],
        "underlying_asset": structure["underlying_asset"],
        "alias_legacy_aba": structure.get("alias_legacy_aba"),
        "legs": [
            {
                "position_side": leg["position_side"],
                "option_type": leg["option_type"],
                "symbol": leg.get("symbol"),
                "strike": leg["strike"],
                "expiration_date": leg["expiration_date"],
                "quantity": leg["quantity"],
                "premium": leg.get("premium"),
                "multiplier": leg["multiplier"],
            }
            for leg in legs
        ],
    }
