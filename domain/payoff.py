from typing import Any

from domain.canonical_validators import validate_canonical_input
from domain.position_side import to_pricing_engine_side


def _round_money(value: float, digits: int = 6) -> float:
    return round(float(value), digits)


def _normalize_side(value: Any) -> str:
    return to_pricing_engine_side(value)


def _normalize_option_type(value: Any) -> str:
    return str(value or "").strip().upper()


def _intrinsic_value(option_type: str, strike: float, spot_at_expiration: float) -> float:
    if option_type == "CALL":
        return max(spot_at_expiration - strike, 0.0)
    if option_type == "PUT":
        return max(strike - spot_at_expiration, 0.0)
    return 0.0


def _compute_leg_payoff_at_expiration(leg: dict[str, Any], spot_at_expiration: float) -> float:
    position_side = _normalize_side(leg.get("position_side"))
    option_type = _normalize_option_type(leg.get("option_type"))

    strike = float(leg.get("strike") or 0.0)
    quantity = float(leg.get("quantity") or 0.0)
    multiplier = float(leg.get("multiplier") or 100.0)
    premium = leg.get("premium")
    premium_value = float(premium) if premium is not None else 0.0

    intrinsic = _intrinsic_value(
        option_type=option_type,
        strike=strike,
        spot_at_expiration=spot_at_expiration,
    )

    payoff_unit = intrinsic - premium_value

    if position_side == "SHORT":
        payoff_unit = -payoff_unit

    return payoff_unit * quantity * multiplier


def compute_payoff_curve_from_canonical_legs(
    legs: list[dict[str, Any]],
    spot_ref: float,
    low_pct: float = 0.5,
    high_pct: float = 1.5,
    step_pct: float = 0.01,
) -> dict[str, Any]:
    if not legs:
        return {
            "points": [],
            "pl_max": 0.0,
            "pl_min": 0.0,
            "spot_ref": _round_money(spot_ref, 6),
            "meta": {
                "legs_count": 0,
                "input_type": "canonical_legs",
                "grid_params": {
                    "low_pct": low_pct,
                    "high_pct": high_pct,
                    "step_pct": step_pct,
                },
            },
        }

    s_min = float(spot_ref) * float(low_pct)
    s_max = float(spot_ref) * float(high_pct)
    step = float(spot_ref) * float(step_pct)

    if step <= 0:
        step = 1.0

    points: list[tuple[float, float]] = []
    pl_values: list[float] = []

    s_t = s_min
    while s_t <= s_max + (step / 2):
        pl_total = 0.0

        for leg in legs:
            pl_total += _compute_leg_payoff_at_expiration(
                leg=leg,
                spot_at_expiration=s_t,
            )

        s_t_rounded = _round_money(s_t, 6)
        pl_total_rounded = _round_money(pl_total, 6)

        points.append((s_t_rounded, pl_total_rounded))
        pl_values.append(pl_total_rounded)

        s_t += step

    pl_max = _round_money(max(pl_values), 6) if pl_values else 0.0
    pl_min = _round_money(min(pl_values), 6) if pl_values else 0.0

    return {
        "points": points,
        "pl_max": pl_max,
        "pl_min": pl_min,
        "spot_ref": _round_money(spot_ref, 6),
        "meta": {
            "legs_count": len(legs),
            "input_type": "canonical_legs",
            "grid_params": {
                "low_pct": low_pct,
                "high_pct": high_pct,
                "step_pct": step_pct,
            },
        },
    }


def compute_payoff_from_canonical_input(
    canonical_input: dict[str, Any],
    low_pct: float = 0.5,
    high_pct: float = 1.5,
    step_pct: float = 0.01,
) -> dict[str, Any]:
    structure = canonical_input.get("structure") or {}
    market = canonical_input.get("market") or {}
    input_meta = canonical_input.get("meta") or {}

    errors = validate_canonical_input(canonical_input)
    if errors:
        return {
            "points": [],
            "pl_max": 0.0,
            "pl_min": 0.0,
            "spot_ref": float(market.get("spot_price") or 0.0),
            "meta": {
                "input_type": "canonical_legs",
                "validation_errors": errors,
            },
            "structure_id": structure.get("structure_id"),
            "structure_name": structure.get("name"),
            "underlying_asset": (
                market.get("underlying_asset")
                or structure.get("underlying_asset")
            ),
            "reference_date": market.get("reference_date") or input_meta.get("reference_date"),
            "input_meta": input_meta,
        }

    legs = structure.get("legs") or []
    spot_ref = float(market.get("spot_price") or 0.0)

    result = compute_payoff_curve_from_canonical_legs(
        legs=legs,
        spot_ref=spot_ref,
        low_pct=low_pct,
        high_pct=high_pct,
        step_pct=step_pct,
    )

    return {
        **result,
        "structure_id": structure.get("structure_id"),
        "structure_name": structure.get("name"),
        "underlying_asset": (
            market.get("underlying_asset")
            or structure.get("underlying_asset")
        ),
        "reference_date": market.get("reference_date") or input_meta.get("reference_date"),
        "input_meta": input_meta,
    }
