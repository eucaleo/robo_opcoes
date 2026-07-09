from services.pricing_execution_persistence_service import (
    PricingExecutionPersistenceService,
)
from services.pricing_input_service import PricingInputService
from services.pricing_execution_query_service import PricingExecutionQueryService


def main():
    pricing_input_service = PricingInputService()
    persistence_service = PricingExecutionPersistenceService()
    query_service = PricingExecutionQueryService()

    pricing_payload = pricing_input_service.build_pricing_payload(structure_id=1)

    result = {
        "pricing_payload": pricing_payload,
        "result": {
            "engine": "stub",
            "status": "error",
            "error_message": "stub engine controlled failure",
        },
    }

    persisted = persistence_service.persist_execution(
        pricing_payload=pricing_payload,
        result=result,
        duration_ms=7,
        error_message="stub engine controlled failure",
    )

    record = persisted["record"]

    if record["structure_id"] != pricing_payload["structure_id"]:
        raise RuntimeError("persisted structure_id does not match pricing payload")

    if record["execution_engine"] != "stub":
        raise RuntimeError("persisted execution_engine does not match expected error value")

    if record["execution_status"] != "error":
        raise RuntimeError("persisted execution_status should be error")

    if record["duration_ms"] != 7:
        raise RuntimeError("persisted duration_ms does not match expected error value")

    if record["error_message"] != "stub engine controlled failure":
        raise RuntimeError("persisted error_message does not match expected error value")

    if record["number_of_legs"] is not None:
        raise RuntimeError("persisted number_of_legs should be None on controlled error")

    if record["total_quantity"] is not None:
        raise RuntimeError("persisted total_quantity should be None on controlled error")

    if record["theoretical_value"] is not None:
        raise RuntimeError("persisted theoretical_value should be None on controlled error")

    summaries = query_service.list_execution_summaries(status="error")
    if not summaries:
        raise RuntimeError("no error execution summaries found after controlled error persistence")

    latest_error = summaries[-1]

    if latest_error["id"] != record["id"]:
        raise RuntimeError("latest error summary does not match persisted error execution")

    if latest_error["error_message"] != "stub engine controlled failure":
        raise RuntimeError("error summary message does not match expected value")

    print("PERSISTED ERROR EXECUTION:", persisted)
    print("LATEST ERROR SUMMARY:", latest_error)
    print("PRICING EXECUTION ERROR PERSISTENCE SMOKE OK")


if __name__ == "__main__":
    main()
