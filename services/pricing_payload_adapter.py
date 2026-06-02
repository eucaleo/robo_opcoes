from typing import Any


def _clean_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _clean_upper_text(value: Any) -> str | None:
    text = _clean_text(value)
    return text.upper() if text is not None else None


def to_pricing_payload(canonical_input: dict[str, Any]) -> dict[str, Any]:
    if not canonical_input:
        raise ValueError("canonical_input is required")

    structure = canonical_input.get("structure")
    market = canonical_input.get("market")

    if not structure:
        raise ValueError("canonical_input.structure is required")

    if not market:
        raise ValueError("canonical_input.market is required")

    legs = structure.get("legs", [])
    pricing_legs = []

    for index, leg in enumerate(legs):
        if not leg:
            raise ValueError(f"canonical_input.structure.legs[{index}] is required")

        pricing_legs.append(
            {
                "side": _clean_upper_text(leg["position_side"]),
                "instrument_type": "OPTION",
                "option_type": _clean_upper_text(leg["option_type"]),
                "symbol": _clean_upper_text(leg.get("symbol")),
                "strike": float(leg["strike"]),
                "expiration_date": _clean_text(leg["expiration_date"]),
                "quantity": int(leg["quantity"]),
                "premium": float(leg["premium"]) if leg.get("premium") is not None else None,
                "multiplier": float(leg["multiplier"]),
            }
        )

    return {
        "structure_id": structure["structure_id"],
        "structure_name": _clean_text(structure["name"]),
        "underlying_asset": _clean_upper_text(structure["underlying_asset"]),
        "reference_date": _clean_text(market["reference_date"]),
        "spot_price": float(market["spot_price"]),
        "interest_rate": float(market["interest_rate"]),
        "volatility": float(market["volatility"]),
        "legs": pricing_legs,
    }
