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

    if persisted["duration_ms"] != 12:
        raise RuntimeError("returned duration_ms does not match expected value")

    if persisted["error_message"] is not None:
        raise RuntimeError("returned error_message should be None")

    print("PERSISTED EXECUTION:", persisted)
    print("PRICING EXECUTION PERSISTENCE SMOKE OK")


if __name__ == "__main__":
    main()
