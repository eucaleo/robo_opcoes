from services.pricing_execution_orchestration_service import (
    PricingExecutionOrchestrationService,
)
from services.pricing_execution_service import PricingExecutionService


class FailingPricingEngineStub:
    def run(self, pricing_payload):
        raise RuntimeError("forced orchestration failure")


def main():
    execution_service = PricingExecutionService(
        pricing_engine=FailingPricingEngineStub()
    )
    service = PricingExecutionOrchestrationService(
        pricing_execution_service=execution_service
    )

    response = service.execute_and_persist(structure_id=1)

    persisted = response["persisted"]["record"]

    if persisted["execution_status"] != "error":
        raise RuntimeError("orchestrated persisted execution_status should be error")

    if persisted["execution_engine"] != "stub":
        raise RuntimeError("orchestrated persisted execution_engine should be stub")

    if persisted["error_message"] != "forced orchestration failure":
        raise RuntimeError("orchestrated persisted error_message does not match expected value")

    if persisted["duration_ms"] is None:
        raise RuntimeError("orchestrated persisted duration_ms should not be None")

    print("ORCHESTRATED ERROR RESPONSE:", response)
    print("PRICING EXECUTION ORCHESTRATION ERROR SMOKE OK")


if __name__ == "__main__":
    main()
