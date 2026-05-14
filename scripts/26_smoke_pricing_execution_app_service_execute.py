from services.pricing_execution_app_service import PricingExecutionAppService
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

    orchestration_service = PricingExecutionOrchestrationService(
        pricing_input_service=fake_input_service,
        pricing_execution_service=PricingExecutionService(
            pricing_input_service=fake_input_service,
        ),
    )

    service = PricingExecutionAppService(
        pricing_execution_orchestration_service=orchestration_service,
    )

    record = service.execute_pricing(
        structure_id=structure_id,
        reference_date="2026-05-14",
    )
    update_context(execution_id=record["id"])

    if record.get("structure_id") != structure_id:
        raise RuntimeError("app service record structure_id should match smoke context structure_id")

    if record.get("execution_status") != "ok":
        raise RuntimeError("app service execution_status should be ok")

    if record.get("execution_engine") != "stub":
        raise RuntimeError("app service execution_engine should be stub")

    if record.get("duration_ms") is None:
        raise RuntimeError("app service duration_ms should not be None")

    if record.get("number_of_legs") != 2:
        raise RuntimeError("app service number_of_legs should be 2")

    if record.get("total_quantity") != 3:
        raise RuntimeError("app service total_quantity should be 3")

    print("APP SERVICE EXECUTE RESPONSE:", record)
    print("PRICING EXECUTION APP SERVICE EXECUTE SMOKE OK")


if __name__ == "__main__":
    main()
