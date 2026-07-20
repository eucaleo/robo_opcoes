from services.pricing_execution_service import PricingExecutionService


class FakePricingInputService:
    def __init__(self, pricing_payload):
        self.pricing_payload = pricing_payload
        self.calls = []

    def build_pricing_payload(self, structure_id: int, reference_date: str | None = None):
        self.calls.append(
            {
                "structure_id": structure_id,
                "reference_date": reference_date,
            }
        )
        return self.pricing_payload


class FakePricingEngine:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def run(self, pricing_payload):
        self.calls.append(pricing_payload)
        return self.result


def test_execute_builds_payload_and_runs_engine():
    pricing_payload = {
        "structure_id": 123,
        "reference_date": "2026-05-16",
        "legs": [],
    }
    engine_result = {
        "engine": "stub",
        "status": "ok",
        "valuation": {"theoretical_value": 10.5},
        "metrics": {"number_of_legs": 0, "total_quantity": 0},
    }

    fake_input_service = FakePricingInputService(pricing_payload)
    fake_engine = FakePricingEngine(engine_result)

    service = PricingExecutionService(
        pricing_input_service=fake_input_service,
        pricing_engine=fake_engine,
    )

    result = service.execute(structure_id=123, reference_date="2026-05-16")

    assert fake_input_service.calls == [
        {
            "structure_id": 123,
            "reference_date": "2026-05-16",
        }
    ]
    assert fake_engine.calls == [pricing_payload]
    assert result == {
        "pricing_payload": pricing_payload,
        "result": engine_result,
    }


def test_execute_payload_runs_engine_and_returns_wrapped_result():
    pricing_payload = {
        "structure_id": 999,
        "reference_date": "2026-05-17",
        "legs": [{"side": "LONG"}],
    }
    engine_result = {
        "engine": "stub",
        "status": "ok",
    }

    fake_engine = FakePricingEngine(engine_result)

    service = PricingExecutionService(
        pricing_input_service=None,
        pricing_engine=fake_engine,
    )

    result = service.execute_payload(pricing_payload)

    assert fake_engine.calls == [pricing_payload]
    assert result == {
        "pricing_payload": pricing_payload,
        "result": engine_result,
    }
