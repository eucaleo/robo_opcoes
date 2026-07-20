from services.pricing_execution_orchestration_service import (
    PricingExecutionOrchestrationService,
)


def main():
    service = PricingExecutionOrchestrationService()

    response = service.execute_and_persist(structure_id=2)

    persisted = response["persisted"]["record"]

    if persisted["execution_status"] != "ok":
        raise RuntimeError("orchestrated persisted execution_status should be ok")

    if persisted["execution_engine"] != "stub":
        raise RuntimeError("orchestrated persisted execution_engine should be stub")

    if persisted["error_message"] is not None:
        raise RuntimeError("orchestrated persisted error_message should be None on success")

    if persisted["duration_ms"] is None:
        raise RuntimeError("orchestrated persisted duration_ms should not be None")

    print("ORCHESTRATED SUCCESS RESPONSE:", response)
    print("PRICING EXECUTION ORCHESTRATION SUCCESS SMOKE OK")


if __name__ == "__main__":
    main()
