from typing import Any


def _clean_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _clean_upper_text(value: Any) -> str | None:
    text = _clean_text(value)
    return text.upper() if text is not None else None


def to_structure_input(structure: dict[str, Any]) -> dict[str, Any]:
    if not structure:
        raise ValueError("structure is required")

    legs = structure.get("legs", [])

    return {
        "structure_id": structure["id"],
        "name": _clean_text(structure["name"]),
        "underlying_asset": _clean_upper_text(structure["underlying_asset"]),
        "alias_legacy_aba": _clean_text(structure.get("alias_legacy_aba")),
        "legs": [
            {
                "position_side": _clean_upper_text(leg["position_side"]),
                "option_type": _clean_upper_text(leg["option_type"]),
                "symbol": _clean_upper_text(leg.get("symbol")),
                "strike": leg["strike"],
                "expiration_date": _clean_text(leg["expiration_date"]),
                "quantity": leg["quantity"],
                "premium": leg.get("premium"),
                "multiplier": leg["multiplier"],
            }
            for leg in legs
        ],
    }
