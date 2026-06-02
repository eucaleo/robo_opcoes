from services.pricing_execution_persistence_service import (
    PricingExecutionPersistenceService,
)


class FakePricingExecutionsRepository:
    def __init__(self):
        self.calls = []

    def save_execution(
        self,
        pricing_payload,
        result,
        execution_status,
        execution_engine,
        error_message,
        duration_ms,
        number_of_legs,
        total_quantity,
        theoretical_value,
    ):
        self.calls.append(
            {
                "pricing_payload": pricing_payload,
                "result": result,
                "execution_status": execution_status,
                "execution_engine": execution_engine,
                "error_message": error_message,
                "duration_ms": duration_ms,
                "number_of_legs": number_of_legs,
                "total_quantity": total_quantity,
                "theoretical_value": theoretical_value,
            }
        )
        return {
            "id": 1,
            "execution_status": execution_status,
            "execution_engine": execution_engine,
        }


def test_persist_execution_extracts_fields_and_saves_record():
    repository = FakePricingExecutionsRepository()
    service = PricingExecutionPersistenceService(
        pricing_executions_repository=repository,
    )

    pricing_payload = {
        "structure_id": 123,
        "reference_date": "2026-05-16",
    }
    result = {
        "result": {
            "engine": "stub",
            "status": "ok",
            "metrics": {
                "number_of_legs": 2,
                "total_quantity": 2000,
            },
            "valuation": {
                "theoretical_value": 321.45,
            },
        }
    }

    persisted = service.persist_execution(
        pricing_payload=pricing_payload,
        result=result,
        duration_ms=87,
    )

    assert repository.calls == [
        {
            "pricing_payload": pricing_payload,
            "result": result,
            "execution_status": "ok",
            "execution_engine": "stub",
            "error_message": None,
            "duration_ms": 87,
            "number_of_legs": 2,
            "total_quantity": 2000,
            "theoretical_value": 321.45,
        }
    ]
    assert persisted == {
        "record": {
            "id": 1,
            "execution_status": "ok",
            "execution_engine": "stub",
        }
    }


def test_persist_execution_accepts_none_pricing_payload_and_explicit_error_message():
    repository = FakePricingExecutionsRepository()
    service = PricingExecutionPersistenceService(
        pricing_executions_repository=repository,
    )

    result = {
        "result": {
            "engine": "stub",
            "status": "error",
            "error_message": "engine internal error",
            "metrics": {},
            "valuation": {},
        }
    }

    persisted = service.persist_execution(
        pricing_payload=None,
        result=result,
        duration_ms=15,
        error_message="execution failed",
    )

    assert repository.calls == [
        {
            "pricing_payload": None,
            "result": result,
            "execution_status": "error",
            "execution_engine": "stub",
            "error_message": "execution failed",
            "duration_ms": 15,
            "number_of_legs": None,
            "total_quantity": None,
            "theoretical_value": None,
        }
    ]
    assert persisted == {
        "record": {
            "id": 1,
            "execution_status": "error",
            "execution_engine": "stub",
        }
    }


def test_persist_execution_uses_result_error_message_when_explicit_error_not_provided():
    repository = FakePricingExecutionsRepository()
    service = PricingExecutionPersistenceService(
        pricing_executions_repository=repository,
    )

    result = {
        "result": {
            "engine": "stub",
            "status": "error",
            "error_message": "engine internal error",
        }
    }

    service.persist_execution(
        pricing_payload=None,
        result=result,
        duration_ms=22,
    )

    assert repository.calls[0]["error_message"] == "engine internal error"
