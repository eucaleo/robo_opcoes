import json

import pytest

from repositories.pricing_executions_repository import PricingExecutionsRepository


def test_save_execution_persists_record_with_payload_and_result(tmp_path):
    file_path = tmp_path / "pricing_executions.json"
    repository = PricingExecutionsRepository(file_path=str(file_path))

    pricing_payload = {
        "structure_id": 123,
        "underlying_asset": "BOVA11",
        "reference_date": "2026-05-16",
        "legs": [],
    }
    result = {
        "result": {
            "engine": "stub",
            "status": "ok",
        }
    }

    record = repository.save_execution(
        pricing_payload=pricing_payload,
        result=result,
        execution_status="ok",
        execution_engine="stub",
        duration_ms=12,
        number_of_legs=0,
        total_quantity=0,
        theoretical_value=0.0,
    )

    assert record["id"] == 1
    assert record["structure_id"] == 123
    assert record["underlying_asset"] == "BOVA11"
    assert record["reference_date"] == "2026-05-16"
    assert record["execution_status"] == "ok"
    assert record["execution_engine"] == "stub"
    assert record["duration_ms"] == 12
    assert record["number_of_legs"] == 0
    assert record["total_quantity"] == 0
    assert record["theoretical_value"] == 0.0
    assert record["pricing_payload"] == pricing_payload
    assert record["result"] == result
    assert record["created_at"].endswith("Z")

    saved_data = json.loads(file_path.read_text(encoding="utf-8"))
    assert len(saved_data) == 1
    assert saved_data[0]["id"] == 1


def test_save_execution_accepts_none_pricing_payload(tmp_path):
    file_path = tmp_path / "pricing_executions.json"
    repository = PricingExecutionsRepository(file_path=str(file_path))

    result = {
        "result": {
            "engine": "stub",
            "status": "error",
        }
    }

    record = repository.save_execution(
        pricing_payload=None,
        result=result,
        execution_status="error",
        execution_engine="stub",
        error_message="failed before payload",
    )

    assert record["id"] == 1
    assert record["structure_id"] is None
    assert record["underlying_asset"] is None
    assert record["reference_date"] is None
    assert record["pricing_payload"] is None
    assert record["result"] == result
    assert record["error_message"] == "failed before payload"


def test_save_execution_raises_when_result_is_missing(tmp_path):
    file_path = tmp_path / "pricing_executions.json"
    repository = PricingExecutionsRepository(file_path=str(file_path))

    with pytest.raises(ValueError, match="result is required"):
        repository.save_execution(
            pricing_payload={"structure_id": 1},
            result={},
        )


def test_list_and_get_execution_return_persisted_records(tmp_path):
    file_path = tmp_path / "pricing_executions.json"
    repository = PricingExecutionsRepository(file_path=str(file_path))

    repository.save_execution(
        pricing_payload={
            "structure_id": 1,
            "underlying_asset": "PETR4",
            "reference_date": "2026-05-16",
        },
        result={"result": {"status": "ok"}},
    )
    repository.save_execution(
        pricing_payload={
            "structure_id": 2,
            "underlying_asset": "VALE3",
            "reference_date": "2026-05-17",
        },
        result={"result": {"status": "ok"}},
    )

    records = repository.list_executions()

    assert len(records) == 2
    assert records[0]["id"] == 1
    assert records[1]["id"] == 2

    record = repository.get_execution(2)
    assert record is not None
    assert record["structure_id"] == 2
    assert record["underlying_asset"] == "VALE3"


def test_get_execution_returns_none_when_not_found(tmp_path):
    file_path = tmp_path / "pricing_executions.json"
    repository = PricingExecutionsRepository(file_path=str(file_path))

    assert repository.get_execution(999) is None


def test_read_all_raises_when_storage_is_not_a_list(tmp_path):
    file_path = tmp_path / "pricing_executions.json"
    file_path.write_text('{"invalid": true}', encoding="utf-8")

    repository = PricingExecutionsRepository(file_path=str(file_path))

    with pytest.raises(ValueError, match="pricing executions storage must contain a list"):
        repository.list_executions()
