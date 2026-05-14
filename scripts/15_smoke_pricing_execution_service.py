from services.pricing_execution_service import PricingExecutionService
from _smoke_context import require_context_value


class FakePricingInputService:
    def build_pricing_payload(self, structure_id: int, reference_date: str | None = None):
        return {
            "structure_id": structure_id,
            "structure_name": "BOVA11 Condor Maio/2026 - Smoke",
            "underlying_asset": "BOVA11",
            "alias_legacy_aba": "BOVA11",
            "reference_date": reference_date or "2026-05-14",
            "spot_price": 198.35,
            "interest_rate": 0.1175,
            "volatility": 0.22,
            "legs": [
                {
                    "quantity": 1,
                },
                {
                    "quantity": 2,
                },
            ],
        }


def main():
    structure_id = require_context_value("structure_id")

    service = PricingExecutionService(
        pricing_input_service=FakePricingInputService(),
    )

    response = service.execute(
        structure_id=structure_id,
        reference_date="2026-05-14",
    )

    if response["pricing_payload"]["structure_id"] != structure_id:
        raise RuntimeError("execution pricing_payload structure_id should match smoke context structure_id")

    if response["result"]["structure_id"] != structure_id:
        raise RuntimeError("execution result structure_id should match smoke context structure_id")

    if response["result"]["metrics"]["number_of_legs"] != 2:
        raise RuntimeError("execution result number_of_legs should be 2")

    if response["result"]["metrics"]["total_quantity"] != 3:
        raise RuntimeError("execution result total_quantity should be 3")

    print("PRICING EXECUTION:", response)
    print("PRICING EXECUTION SERVICE SMOKE OK")


if __name__ == "__main__":
    main()
