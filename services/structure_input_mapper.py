from typing import Any

from domain.position_side import normalize_position_side


def _clean_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _clean_upper_text(value: Any) -> str | None:
    text = _clean_text(value)
    return text.upper() if text is not None else None


def _to_float_or_none(value: Any) -> float | None:
    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _enrich_bid_ask_calculated_fields(mapped_leg: dict[str, Any]) -> None:
    bid = _to_float_or_none(mapped_leg.get("bid"))
    ask = _to_float_or_none(mapped_leg.get("ask"))

    if bid is None or ask is None:
        return

    spread = ask - bid
    mid = (bid + ask) / 2

    if "spread" not in mapped_leg or mapped_leg.get("spread") is None:
        mapped_leg["spread"] = spread

    if "mid" not in mapped_leg or mapped_leg.get("mid") is None:
        mapped_leg["mid"] = mid

    if (
        ("spread_pct" not in mapped_leg or mapped_leg.get("spread_pct") is None)
        and mid
    ):
        mapped_leg["spread_pct"] = spread / mid


def _map_leg_to_structure_input(leg: dict[str, Any]) -> dict[str, Any]:
    mapped_leg = {
        "position_side": normalize_position_side(leg["position_side"]),
        "option_type": _clean_upper_text(leg["option_type"]),
        "symbol": _clean_upper_text(leg.get("symbol")),
        "strike": leg["strike"],
        "expiration_date": _clean_text(leg["expiration_date"]),
        "quantity": leg["quantity"],
        "premium": leg.get("premium"),
        "multiplier": leg.get("multiplier", 1.0),
    }

    optional_market_fields = (
        "bid",
        "ask",
        "mid",
        "spread",
        "spread_pct",
        "iv",
        "delta",
        "gamma",
        "theta",
        "vega",
    )

    for field in optional_market_fields:
        if field in leg:
            mapped_leg[field] = leg[field]

    _enrich_bid_ask_calculated_fields(mapped_leg)

    return mapped_leg


def to_structure_input(structure: dict[str, Any]) -> dict[str, Any]:
    if not structure:
        raise ValueError("structure is required")

    legs = structure.get("legs", [])

    return {
        "structure_id": structure["id"],
        "name": _clean_text(structure["name"]),
        "underlying_asset": _clean_upper_text(structure["underlying_asset"]),
        "legs": [
            _map_leg_to_structure_input(leg)
            for leg in legs
        ],
    }
