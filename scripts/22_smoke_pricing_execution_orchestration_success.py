from services.pricing_execution_orchestration_service import PricingExecutionOrchestrationService
from services.pricing_execution_service import PricingExecutionService
from _smoke_context import require_context_value, update_context


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
                {"quantity": 1},
                {"quantity": 2},
            ],
        }


def main():
    structure_id = require_context_value("structure_id")

    fake_input_service = FakePricingInputService()

    service = PricingExecutionOrchestrationService(
        pricing_input_service=fake_input_service,
        pricing_execution_service=PricingExecutionService(
            pricing_input_service=fake_input_service,
        ),
    )

    response = service.execute_and_persist(
        structure_id=structure_id,
        reference_date="2026-05-14",
    )

    if response["pricing_payload"]["structure_id"] != structure_id:
        raise RuntimeError("orchestration pricing_payload structure_id should match smoke context structure_id")

    record = response["persisted"]["record"]
    update_context(execution_id=record["id"])

    if record["structure_id"] != structure_id:
        raise RuntimeError("orchestration persisted record structure_id should match smoke context structure_id")

    if record["execution_status"] != "ok":
        raise RuntimeError("orchestration persisted execution_status should be ok")

    if record["execution_engine"] != "stub":
        raise RuntimeError("orchestration persisted execution_engine should be stub")

    print("ORCHESTRATED SUCCESS RESPONSE:", response)
    print("PRICING EXECUTION ORCHESTRATION SUCCESS SMOKE OK")


if __name__ == "__main__":
    main()
