from typing import Any

from services.structure_input_mapper import to_structure_input


def assemble_structure_market_input(
    structure: dict[str, Any],
    market_snapshot: dict[str, Any],
) -> dict[str, Any]:
    if not structure:
        raise ValueError("structure is required")

    if not market_snapshot:
        raise ValueError("market_snapshot is required")

    structure_input = to_structure_input(structure)
    structure_asset = structure_input["underlying_asset"]
    market_asset = market_snapshot.get("underlying_asset")

    if structure_asset != market_asset:
        raise ValueError(
            f"underlying_asset mismatch: structure={structure_asset} market={market_asset}"
        )

    return {
        "structure": structure_input,
        "market": {
            "reference_date": market_snapshot["reference_date"],
            "underlying_asset": market_snapshot["underlying_asset"],
            "spot_price": market_snapshot["spot_price"],
            "interest_rate": market_snapshot["interest_rate"],
            "volatility": market_snapshot["volatility"],
        },
        "meta": {
            "input_source": "structure_market_input_assembler",
        },
    }
