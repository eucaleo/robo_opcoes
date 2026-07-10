from repositories.structures_repository import StructuresRepository
from services.canonical_input_service import CanonicalInputService


def main():
    repo = StructuresRepository()
    service = CanonicalInputService(repository=repo)

    structures = repo.list_structures(include_archived=True)
    if not structures:
        raise RuntimeError("no structures found for canonical input smoke test")

    structure_id = structures[0]["id"]
    payload = service.build_structure_market_input(
        structure_id=structure_id,
        reference_date="2026-05-10",
    )

    print("CANONICAL INPUT PAYLOAD:", payload)
    print("CANONICAL INPUT SERVICE SMOKE OK")


if __name__ == "__main__":
    main()
