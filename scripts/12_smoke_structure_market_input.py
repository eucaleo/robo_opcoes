from repositories.structures_repository import StructuresRepository
from services.market_snapshot_provider import MarketSnapshotProvider
from services.structure_market_input_assembler import assemble_structure_market_input


def main():
    repo = StructuresRepository()
    provider = MarketSnapshotProvider()

    structures = repo.list_structures(include_archived=True)
    if not structures:
        raise RuntimeError("no structures found for structure+market smoke test")

    structure_id = structures[0]["id"]
    structure = repo.get_structure(structure_id)
    if structure is None:
        raise RuntimeError(f"structure not found: {structure_id}")

    snapshot = provider.get_snapshot(structure["underlying_asset"])
    combined_input = assemble_structure_market_input(structure, snapshot)

    print("COMBINED INPUT:", combined_input)
    print("STRUCTURE+MARKET SMOKE OK")


if __name__ == "__main__":
    main()
