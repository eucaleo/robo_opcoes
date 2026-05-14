from services.pricing_execution_persistence_service import PricingExecutionPersistenceService
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

    execution_service = PricingExecutionService(
        pricing_input_service=FakePricingInputService(),
    )
    persistence_service = PricingExecutionPersistenceService()

    execution_response = execution_service.execute(
        structure_id=structure_id,
        reference_date="2026-05-14",
    )

    persisted = persistence_service.persist_execution(
        pricing_payload=execution_response["pricing_payload"],
        result=execution_response,
        duration_ms=1,
    )

    record = persisted["record"]
    update_context(execution_id=record["id"])

    if record["structure_id"] != structure_id:
        raise RuntimeError("persisted record structure_id should match smoke context structure_id")

    if record["execution_status"] != "ok":
        raise RuntimeError("persisted execution_status should be ok")

    if record["execution_engine"] != "stub":
        raise RuntimeError("persisted execution_engine should be stub")

    if record["number_of_legs"] != 2:
        raise RuntimeError("persisted number_of_legs should be 2")

    if record["total_quantity"] != 3:
        raise RuntimeError("persisted total_quantity should be 3")

    print("PERSISTED EXECUTION:", persisted)
    print("PRICING EXECUTION PERSISTENCE SMOKE OK")


if __name__ == "__main__":
    main()
