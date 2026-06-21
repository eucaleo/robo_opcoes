from typing import Any


def validate_canonical_input(canonical_input: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    structure = canonical_input.get("structure") or {}
    market = canonical_input.get("market") or {}

    if not structure.get("structure_id"):
        errors.append("structure.structure_id is required")

    if not structure.get("underlying_asset"):
        errors.append("structure.underlying_asset is required")

    legs = structure.get("legs") or []
    if not legs:
        errors.append("structure.legs must not be empty")

    for index, leg in enumerate(legs):
        if not leg.get("position_side"):
            errors.append(f"structure.legs[{index}].position_side is required")
        if not leg.get("option_type"):
            errors.append(f"structure.legs[{index}].option_type is required")
        if leg.get("strike") is None:
            errors.append(f"structure.legs[{index}].strike is required")
        if leg.get("quantity") is None:
            errors.append(f"structure.legs[{index}].quantity is required")
        if leg.get("expiration_date") is None:
            errors.append(f"structure.legs[{index}].expiration_date is required")

    if market.get("spot_price") is None:
        errors.append("market.spot_price is required")

    if not market.get("reference_date"):
        errors.append("market.reference_date is required")

    return errors
