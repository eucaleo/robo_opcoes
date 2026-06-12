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


class FakeSystemSnapshotsRepository:
    def __init__(self):
        self.calls = []

    def create_snapshot(self, **kwargs):
        self.calls.append(kwargs)
        return 99


class RaisingSystemSnapshotsRepository:
    def create_snapshot(self, **kwargs):
        raise RuntimeError("snapshot failure")


def test_persist_execution_creates_system_snapshot_for_successful_execution():
    repository = FakePricingExecutionsRepository()
    snapshots_repository = FakeSystemSnapshotsRepository()

    service = PricingExecutionPersistenceService(
        pricing_executions_repository=repository,
        system_snapshots_repository=snapshots_repository,
    )

    pricing_payload = {
        "structure_id": 123,
        "structure_name": "Iron Condor",
        "underlying_asset": "PETR4",
        "reference_date": "2026-05-16",
        "spot_price": 35.50,
        "interest_rate": 0.0,
        "volatility": 0.0,
        "meta": {
            "snapshot_source": "manual",
            "legs_count": 2,
        },
        "legs": [
            {
                "leg_order": 1,
                "position_side": "LONG",
                "option_type": "CALL",
                "symbol": "PETR4C360",
                "strike": 36.0,
                "quantity": 100,
                "premium": 1.23,
            }
        ],
    }
    result = {
        "result": {
            "engine": "stub",
            "status": "ok",
            "metrics": {
                "number_of_legs": 1,
                "total_quantity": 100,
            },
            "valuation": {
                "theoretical_value": 123.45,
            },
            "payoff": {
                "points": [],
            },
            "decision": {
                "action": "HOLD",
            },
            "alerts": [
                {
                    "level": "info",
                    "message": "ok",
                }
            ],
        }
    }

    persisted = service.persist_execution(
        pricing_payload=pricing_payload,
        result=result,
        duration_ms=87,
    )

    assert persisted["record"]["id"] == 1
    assert persisted["snapshot_id"] == 99

    assert len(snapshots_repository.calls) == 1
    call = snapshots_repository.calls[0]

    assert call["structure_id"] == 123
    assert call["pricing_execution_id"] == 1
    assert call["underlying_asset"] == "PETR4"
    assert call["reference_date"] == "2026-05-16"
    assert call["snapshot_source"] == "system_pricing_execution"
    assert call["structure_json"]["structure_id"] == 123
    assert call["market_json"]["spot_price"] == 35.50
    assert call["metrics_json"] == {
        "number_of_legs": 1,
        "total_quantity": 100,
    }
    assert call["payoff_json"] == {
        "points": [],
    }
    assert call["decision_json"] == {
        "action": "HOLD",
    }
    assert call["alerts_json"] == [
        {
            "level": "info",
            "message": "ok",
        }
    ]
    assert call["legs"] == pricing_payload["legs"]


def test_persist_execution_does_not_create_system_snapshot_without_pricing_payload():
    repository = FakePricingExecutionsRepository()
    snapshots_repository = FakeSystemSnapshotsRepository()

    service = PricingExecutionPersistenceService(
        pricing_executions_repository=repository,
        system_snapshots_repository=snapshots_repository,
    )

    persisted = service.persist_execution(
        pricing_payload=None,
        result={
            "result": {
                "engine": "stub",
                "status": "error",
                "error_message": "failed",
            }
        },
        duration_ms=10,
        error_message="failed",
    )

    assert persisted == {
        "record": {
            "id": 1,
            "execution_status": "error",
            "execution_engine": "stub",
        }
    }
    assert snapshots_repository.calls == []


def test_persist_execution_does_not_create_system_snapshot_for_non_ok_status():
    repository = FakePricingExecutionsRepository()
    snapshots_repository = FakeSystemSnapshotsRepository()

    service = PricingExecutionPersistenceService(
        pricing_executions_repository=repository,
        system_snapshots_repository=snapshots_repository,
    )

    persisted = service.persist_execution(
        pricing_payload={
            "structure_id": 123,
            "underlying_asset": "PETR4",
            "reference_date": "2026-05-16",
            "legs": [],
        },
        result={
            "result": {
                "engine": "stub",
                "status": "error",
                "error_message": "failed",
            }
        },
        duration_ms=10,
        error_message="failed",
    )

    assert persisted == {
        "record": {
            "id": 1,
            "execution_status": "error",
            "execution_engine": "stub",
        }
    }
    assert snapshots_repository.calls == []


def test_persist_execution_ignores_system_snapshot_failure():
    repository = FakePricingExecutionsRepository()

    service = PricingExecutionPersistenceService(
        pricing_executions_repository=repository,
        system_snapshots_repository=RaisingSystemSnapshotsRepository(),
    )

    persisted = service.persist_execution(
        pricing_payload={
            "structure_id": 123,
            "underlying_asset": "PETR4",
            "reference_date": "2026-05-16",
            "spot_price": 35.50,
            "legs": [],
        },
        result={
            "result": {
                "engine": "stub",
                "status": "ok",
            }
        },
        duration_ms=10,
    )

    assert persisted == {
        "record": {
            "id": 1,
            "execution_status": "ok",
            "execution_engine": "stub",
        }
    }
