from services.pricing_execution_orchestration_service import (
    PricingExecutionOrchestrationService,
)


class FakePricingInputService:
    def build_pricing_payload(self, structure_id: int, reference_date: str | None = None):
        return {
            "structure_id": structure_id,
            "reference_date": reference_date,
            "payload_source": "fake_input_service",
        }


class FakePricingExecutionService:
    def __init__(self, should_raise: bool = False):
        self.should_raise = should_raise
        self.calls = []

    def execute(self, structure_id: int, reference_date: str | None = None):
        self.calls.append(
            {
                "structure_id": structure_id,
                "reference_date": reference_date,
            }
        )

        if self.should_raise:
            raise RuntimeError("execution failed")

        return {
            "pricing_payload": {
                "structure_id": structure_id,
                "reference_date": reference_date,
                "payload_source": "fake_execution_service",
            },
            "result": {
                "engine": "stub",
                "status": "ok",
                "npv": 123.45,
            },
        }


class FakePricingExecutionPersistenceService:
    def __init__(self):
        self.calls = []

    def persist_execution(
        self,
        pricing_payload,
        result,
        duration_ms: int,
        error_message: str | None = None,
    ):
        self.calls.append(
            {
                "pricing_payload": pricing_payload,
                "result": result,
                "duration_ms": duration_ms,
                "error_message": error_message,
            }
        )
        return {
            "status": "persisted",
            "duration_ms": duration_ms,
            "error_message": error_message,
        }


def test_execute_and_persist_success():
    execution_service = FakePricingExecutionService(should_raise=False)
    persistence_service = FakePricingExecutionPersistenceService()

    service = PricingExecutionOrchestrationService(
        pricing_input_service=FakePricingInputService(),
        pricing_execution_service=execution_service,
        pricing_execution_persistence_service=persistence_service,
    )

    result = service.execute_and_persist(
        structure_id=123,
        reference_date="2026-05-15",
    )

    assert execution_service.calls == [
        {
            "structure_id": 123,
            "reference_date": "2026-05-15",
        }
    ]

    assert result["pricing_payload"]["structure_id"] == 123
    assert result["pricing_payload"]["reference_date"] == "2026-05-15"
    assert result["result"]["result"]["status"] == "ok"
    assert result["persisted"]["status"] == "persisted"

    persisted_call = persistence_service.calls[0]
    assert persisted_call["pricing_payload"]["structure_id"] == 123
    assert persisted_call["error_message"] is None
    assert isinstance(persisted_call["duration_ms"], int)


def test_execute_and_persist_error():
    execution_service = FakePricingExecutionService(should_raise=True)
    persistence_service = FakePricingExecutionPersistenceService()

    service = PricingExecutionOrchestrationService(
        pricing_input_service=FakePricingInputService(),
        pricing_execution_service=execution_service,
        pricing_execution_persistence_service=persistence_service,
    )

    result = service.execute_and_persist(
        structure_id=999,
        reference_date="2026-05-16",
    )

    assert execution_service.calls == [
        {
            "structure_id": 999,
            "reference_date": "2026-05-16",
        }
    ]

    assert result["pricing_payload"] is None
    assert result["result"]["result"]["status"] == "error"
    assert result["result"]["result"]["error_message"] == "execution failed"
    assert result["persisted"]["status"] == "persisted"

    persisted_call = persistence_service.calls[0]
    assert persisted_call["pricing_payload"] is None
    assert persisted_call["error_message"] == "execution failed"
    assert isinstance(persisted_call["duration_ms"], int)
