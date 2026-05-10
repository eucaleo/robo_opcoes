from services.pricing_execution_persistence_service import (
    PricingExecutionPersistenceService,
)
from services.pricing_execution_service import PricingExecutionService
from services.pricing_input_service import PricingInputService


def main():
    pricing_input_service = PricingInputService()
    execution_service = PricingExecutionService()
    persistence_service = PricingExecutionPersistenceService()

    pricing_payload = pricing_input_service.build_pricing_payload(structure_id=1)
    result = execution_service.execute(structure_id=1)

    persisted = persistence_service.persist_execution(
        pricing_payload=pricing_payload,
        result=result,
        duration_ms=12,
        error_message=None,
    )

    record = persisted["record"]

    if record["structure_id"] != pricing_payload["structure_id"]:
        raise RuntimeError("persisted structure_id does not match pricing payload")

    if record["pricing_payload"]["structure_id"] != pricing_payload["structure_id"]:
        raise RuntimeError("persisted pricing_payload does not match input payload")

    if record["result"] != result:
        raise RuntimeError("persisted result does not match execution result")

    if record["execution_engine"] != "stub":
        raise RuntimeError("persisted execution_engine does not match expected value")

    if record["execution_status"] != "ok":
        raise RuntimeError("persisted execution_status does not match expected value")

    if record["duration_ms"] != 12:
        raise RuntimeError("persisted duration_ms does not match expected value")

    if record["error_message"] is not None:
        raise RuntimeError("persisted error_message should be None")

    if record["number_of_legs"] != 2:
        raise RuntimeError("persisted number_of_legs does not match expected value")

    if record["total_quantity"] != 4000:
        raise RuntimeError("persisted total_quantity does not match expected value")

    if record["theoretical_value"] != 0.0:
        raise RuntimeError("persisted theoretical_value does not match expected value")

    print("PERSISTED EXECUTION:", persisted)
    print("PRICING EXECUTION PERSISTENCE SMOKE OK")


if __name__ == "__main__":
    main()
