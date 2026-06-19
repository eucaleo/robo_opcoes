import sqlite3

from repositories.pricing_executions_repository import PricingExecutionsRepository
from services.pricing_execution_persistence_service import (
    PricingExecutionPersistenceService,
)


def _create_pricing_executions_schema(db_path):
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            CREATE TABLE pricing_executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                structure_id INTEGER,
                underlying_asset TEXT,
                reference_date TEXT,
                execution_status TEXT,
                execution_engine TEXT,
                error_message TEXT,
                duration_ms INTEGER,
                number_of_legs INTEGER,
                total_quantity INTEGER,
                theoretical_value REAL,
                pricing_payload TEXT,
                result TEXT
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def test_pricing_executions_repository_preserves_leg_price_source_on_get(tmp_path):
    db_path = tmp_path / "app.db"
    _create_pricing_executions_schema(db_path)

    repository = PricingExecutionsRepository(db_path=db_path)

    pricing_payload = {
        "structure_id": 123,
        "structure_name": "Teste RTD",
        "underlying_asset": "ABCD",
        "reference_date": "2026-06-15",
        "spot_price": 100.0,
        "interest_rate": 0.1,
        "volatility": 0.25,
        "legs": [
            {
                "option_type": "CALL",
                "symbol": "ABCDC100",
                "strike": 100.0,
                "expiration_date": "2026-07-17",
                "quantity": 1,
                "premium": 2.35,
                "price_source": "rtd_option_quotes",
            },
            {
                "option_type": "PUT",
                "symbol": "ABCDP095",
                "strike": 95.0,
                "expiration_date": "2026-07-17",
                "quantity": -1,
                "premium": 1.2,
                "price_source": "manual",
            },
        ],
    }

    result = {
        "result": {
            "status": "ok",
            "engine": "test-engine",
            "metrics": {
                "number_of_legs": 2,
                "total_quantity": 0,
            },
            "valuation": {
                "theoretical_value": 123.45,
            },
        }
    }

    record = repository.save_execution(
        pricing_payload=pricing_payload,
        result=result,
        execution_status="ok",
        execution_engine="test-engine",
        number_of_legs=2,
        total_quantity=0,
        theoretical_value=123.45,
    )

    loaded = repository.get_execution(record["id"])

    assert loaded is not None
    assert loaded["pricing_payload"]["legs"][0]["price_source"] == "rtd_option_quotes"
    assert loaded["pricing_payload"]["legs"][1]["price_source"] == "manual"


def test_pricing_executions_repository_preserves_leg_price_source_on_list(tmp_path):
    db_path = tmp_path / "app.db"
    _create_pricing_executions_schema(db_path)

    repository = PricingExecutionsRepository(db_path=db_path)

    pricing_payload = {
        "structure_id": 456,
        "underlying_asset": "WXYZ",
        "reference_date": "2026-06-15",
        "spot_price": 50.0,
        "interest_rate": 0.1,
        "volatility": 0.3,
        "legs": [
            {
                "option_type": "CALL",
                "symbol": "WXYZC050",
                "strike": 50.0,
                "expiration_date": "2026-07-17",
                "quantity": 1,
                "premium": 0.0,
                "price_source": "missing",
            }
        ],
    }

    result = {
        "result": {
            "status": "ok",
            "engine": "test-engine",
            "metrics": {
                "number_of_legs": 1,
                "total_quantity": 1,
            },
            "valuation": {
                "theoretical_value": 0.0,
            },
        }
    }

    repository.save_execution(
        pricing_payload=pricing_payload,
        result=result,
        execution_status="ok",
        execution_engine="test-engine",
        number_of_legs=1,
        total_quantity=1,
        theoretical_value=0.0,
    )

    executions = repository.list_executions()

    assert len(executions) == 1
    assert executions[0]["pricing_payload"]["legs"][0]["price_source"] == "missing"


class FakePricingExecutionsRepository:
    def __init__(self):
        self.calls = []

    def save_execution(self, **kwargs):
        self.calls.append(kwargs)

        pricing_payload = kwargs["pricing_payload"]

        return {
            "id": 999,
            "created_at": "2026-06-15T00:00:00Z",
            "structure_id": pricing_payload.get("structure_id") if pricing_payload else None,
            "underlying_asset": pricing_payload.get("underlying_asset") if pricing_payload else None,
            "reference_date": pricing_payload.get("reference_date") if pricing_payload else None,
            "execution_status": kwargs.get("execution_status"),
            "execution_engine": kwargs.get("execution_engine"),
            "error_message": kwargs.get("error_message"),
            "duration_ms": kwargs.get("duration_ms"),
            "number_of_legs": kwargs.get("number_of_legs"),
            "total_quantity": kwargs.get("total_quantity"),
            "theoretical_value": kwargs.get("theoretical_value"),
            "pricing_payload": pricing_payload,
            "result": kwargs["result"],
        }


class FakeSystemSnapshotsRepository:
    def __init__(self):
        self.calls = []

    def create_snapshot(self, **kwargs):
        self.calls.append(kwargs)
        return 321


def test_persistence_service_passes_price_source_to_system_snapshot_legs():
    fake_repository = FakePricingExecutionsRepository()
    fake_snapshots_repository = FakeSystemSnapshotsRepository()

    service = PricingExecutionPersistenceService(
        pricing_executions_repository=fake_repository,
        system_snapshots_repository=fake_snapshots_repository,
    )

    pricing_payload = {
        "structure_id": 123,
        "structure_name": "Teste Snapshot",
        "underlying_asset": "ABCD",
        "reference_date": "2026-06-15",
        "spot_price": 100.0,
        "interest_rate": 0.1,
        "volatility": 0.25,
        "meta": {},
        "legs": [
            {
                "option_type": "CALL",
                "symbol": "ABCDC100",
                "strike": 100.0,
                "expiration_date": "2026-07-17",
                "quantity": 1,
                "premium": 2.35,
                "price_source": "rtd_option_quotes",
            }
        ],
    }

    result = {
        "result": {
            "status": "ok",
            "engine": "test-engine",
            "metrics": {
                "number_of_legs": 1,
                "total_quantity": 1,
            },
            "valuation": {
                "theoretical_value": 2.35,
            },
        }
    }

    response = service.persist_execution(
        pricing_payload=pricing_payload,
        result=result,
        duration_ms=15,
    )

    assert response["snapshot_id"] == 321

    snapshot_call = fake_snapshots_repository.calls[0]

    assert snapshot_call["legs"][0]["price_source"] == "rtd_option_quotes"
    assert (
        snapshot_call["operation_state_json"]["pricing_payload"]["legs"][0]["price_source"]
        == "rtd_option_quotes"
    )
