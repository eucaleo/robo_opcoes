from repositories.structures_repository import StructuresRepository
from services.pricing_input_service import PricingInputService


def main():
    repo = StructuresRepository()
    service = PricingInputService()

    structures = repo.list_structures(include_archived=True)
    if not structures:
        raise RuntimeError("no structures found for pricing input smoke test")

    structure_id = structures[0]["id"]
    payload = service.build_pricing_payload(
        structure_id=structure_id,
        reference_date="2026-05-10",
    )

    print("PRICING PAYLOAD:", payload)
    print("PRICING INPUT SERVICE SMOKE OK")


if __name__ == "__main__":
    main()
