from services.pricing_input_service import PricingInputService
from _smoke_context import require_context_value


def main():
    service = PricingInputService()

    structure_id = require_context_value("structure_id")
    payload = service.build_pricing_payload(
        structure_id=structure_id,
        reference_date="2026-05-14",
    )

    if payload["structure_id"] != structure_id:
        raise RuntimeError("pricing payload structure_id should match smoke context structure_id")

    print("PRICING PAYLOAD:", payload)
    print("PRICING INPUT SERVICE SMOKE OK")


if __name__ == "__main__":
    main()
