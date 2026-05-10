from repositories.structures_repository import StructuresRepository
from services.pricing_execution_persistence_service import (
    PricingExecutionPersistenceService,
)


def main():
    repo = StructuresRepository()
    service = PricingExecutionPersistenceService()

    structures = repo.list_structures(include_archived=True)
    if not structures:
        raise RuntimeError("no structures found for pricing execution persistence smoke test")

    structure_id = structures[0]["id"]
    output = service.execute_and_persist(
        structure_id=structure_id,
        reference_date="2026-05-10",
    )

    print("PERSISTED EXECUTION:", output)
    print("PRICING EXECUTION PERSISTENCE SMOKE OK")


if __name__ == "__main__":
    main()
