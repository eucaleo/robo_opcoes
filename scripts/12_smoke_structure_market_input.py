from services.structure_market_input_assembler import assemble_structure_market_input
from repositories.structures_repository import StructuresRepository
from _smoke_context import require_context_value


def _find_structure_by_id(items, structure_id):
    for item in items:
        if item["id"] == structure_id:
            return item
    return None


def main():
    repository = StructuresRepository()

    structure_id = require_context_value("structure_id")
    structures = repository.list_structures()
    structure = _find_structure_by_id(structures, structure_id)

    if structure is None:
        raise RuntimeError("structure should exist in repository list")

    market_snapshot = {
        "reference_date": "2026-05-14",
        "underlying_asset": structure["underlying_asset"],
        "spot_price": 120.50,
        "interest_rate": 0.1175,
        "volatility": 0.22,
    }

    assembled = assemble_structure_market_input(structure, market_snapshot)

    if assembled["structure"]["structure_id"] != structure_id:
        raise RuntimeError("assembled structure_id should match smoke context structure_id")

    if assembled["market"]["underlying_asset"] != structure["underlying_asset"]:
        raise RuntimeError("assembled market underlying_asset should match structure underlying_asset")

    print("STRUCTURE MARKET INPUT:", assembled)
    print("MARKET INPUT SMOKE OK")


if __name__ == "__main__":
    main()
