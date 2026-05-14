from repositories.structures_repository import StructuresRepository
from _smoke_context import load_context


def _find_structure_by_id(items, structure_id):
    for item in items:
        if item["id"] == structure_id:
            return item
    return None


def main():
    context = load_context()
    structure_id = context.get("structure_id")

    if not structure_id:
        print("SMOKE CLEANUP OK")
        return

    repository = StructuresRepository()
    structures = repository.list_structures()
    structure = _find_structure_by_id(structures, structure_id)

    if structure is None:
        print("SMOKE CLEANUP OK")
        return

    if structure.get("status") != "archived":
        archived = repository.archive_structure(structure_id)
        print("ARCHIVED STRUCTURE:", archived)

    print("SMOKE CLEANUP OK")


if __name__ == "__main__":
    main()
