from repositories.structures_repository import StructuresRepository
from services.pricing_execution_service import PricingExecutionService


def main():
    repo = StructuresRepository()
    service = PricingExecutionService()

    structures = repo.list_structures(include_archived=True)
    if not structures:
        raise RuntimeError("no structures found for pricing execution smoke test")

    structure_id = structures[0]["id"]
    execution = service.execute(
        structure_id=structure_id,
        reference_date="2026-05-10",
    )

    print("PRICING EXECUTION:", execution)
    print("PRICING EXECUTION SERVICE SMOKE OK")


if __name__ == "__main__":
    main()
