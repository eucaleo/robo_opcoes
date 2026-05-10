from typing import Any


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

    for leg in legs:
        pricing_legs.append(
            {
                "side": leg["position_side"],
                "instrument_type": "OPTION",
                "option_type": leg["option_type"],
                "symbol": leg.get("symbol"),
                "strike": float(leg["strike"]),
                "expiration_date": leg["expiration_date"],
                "quantity": int(leg["quantity"]),
                "premium": leg.get("premium"),
                "multiplier": float(leg["multiplier"]),
            }
        )

    return {
        "structure_id": structure["structure_id"],
        "structure_name": structure["name"],
        "underlying_asset": structure["underlying_asset"],
        "alias_legacy_aba": structure.get("alias_legacy_aba"),
        "reference_date": market["reference_date"],
        "spot_price": float(market["spot_price"]),
        "interest_rate": float(market["interest_rate"]),
        "volatility": float(market["volatility"]),
        "legs": pricing_legs,
    }
