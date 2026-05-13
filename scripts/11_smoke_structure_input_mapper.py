from repositories.structures_repository import StructuresRepository
from services.structure_input_mapper import to_structure_input


def main():
    repo = StructuresRepository()

    structures = repo.list_structures(include_archived=True)
    if not structures:
        raise RuntimeError("no structures found for mapper smoke test")

    structure_id = structures[0]["id"]
    structure = repo.get_structure(structure_id)
    if structure is None:
        raise RuntimeError(f"structure not found: {structure_id}")

    structure_input = to_structure_input(structure)

    print("STRUCTURE INPUT:", structure_input)
    print("MAPPER SMOKE OK")


if __name__ == "__main__":
    main()
