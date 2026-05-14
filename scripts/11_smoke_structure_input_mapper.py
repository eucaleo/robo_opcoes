from services.structure_input_mapper import to_structure_input
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

    mapped = to_structure_input(structure)

    if mapped["structure_id"] != structure_id:
        raise RuntimeError("mapped structure_id should match smoke context structure_id")

    if mapped["name"] != structure["name"]:
        raise RuntimeError("mapped name should match structure name")

    if mapped["underlying_asset"] != structure["underlying_asset"]:
        raise RuntimeError("mapped underlying_asset should match structure underlying_asset")

    if "legs" not in mapped:
        raise RuntimeError("mapped structure input should contain legs")

    print("STRUCTURE INPUT:", mapped)
    print("MAPPER SMOKE OK")


if __name__ == "__main__":
    main()
