from services.pricing_execution_query_service import PricingExecutionQueryService


class FakePricingExecutionsRepository:
    def __init__(self, records=None):
        self.records = records or []

    def list_executions(self):
        return self.records

    def get_execution(self, execution_id: int):
        for record in self.records:
            if record["id"] == execution_id:
                return record
        return None


def make_execution(
    execution_id: int,
    structure_id: int = 1,
    underlying_asset: str = "PETR4",
    reference_date: str = "2026-05-16",
    execution_status: str = "ok",
    execution_engine: str = "stub-engine",
    duration_ms: int = 25,
    error_message: str | None = None,
    number_of_legs=None,
    total_quantity=None,
    theoretical_value=None,
    nested_number_of_legs: int = 2,
    nested_total_quantity: int = 200,
    nested_theoretical_value: float = 123.45,
):
    return {
        "id": execution_id,
        "created_at": f"2026-05-16T12:00:0{execution_id}Z",
        "structure_id": structure_id,
        "underlying_asset": underlying_asset,
        "reference_date": reference_date,
        "execution_engine": execution_engine,
        "execution_status": execution_status,
        "duration_ms": duration_ms,
        "error_message": error_message,
        "number_of_legs": number_of_legs,
        "total_quantity": total_quantity,
        "theoretical_value": theoretical_value,
        "pricing_payload": {
            "structure_id": structure_id,
            "underlying_asset": underlying_asset,
            "reference_date": reference_date,
        },
        "result": {
            "result": {
                "metrics": {
                    "number_of_legs": nested_number_of_legs,
                    "total_quantity": nested_total_quantity,
                },
                "valuation": {
                    "theoretical_value": nested_theoretical_value,
                },
            }
        },
    }


def test_list_executions_returns_repository_records():
    records = [make_execution(1), make_execution(2)]
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository(records)
    )

    result = service.list_executions()

    assert result == records


def test_list_execution_summaries_returns_summaries_sorted_descending_by_default():
    records = [make_execution(1), make_execution(3), make_execution(2)]
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository(records)
    )

    summaries = service.list_execution_summaries()

    assert [item["id"] for item in summaries] == [3, 2, 1]


def test_list_execution_summaries_can_sort_ascending():
    records = [make_execution(1), make_execution(3), make_execution(2)]
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository(records)
    )

    summaries = service.list_execution_summaries(descending=False)

    assert [item["id"] for item in summaries] == [1, 2, 3]


def test_list_execution_summaries_uses_persisted_metrics_when_available():
    records = [
        make_execution(
            1,
            number_of_legs=9,
            total_quantity=999,
            theoretical_value=777.77,
            nested_number_of_legs=2,
            nested_total_quantity=200,
            nested_theoretical_value=123.45,
        )
    ]
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository(records)
    )

    summaries = service.list_execution_summaries()

    assert len(summaries) == 1
    assert summaries[0]["number_of_legs"] == 9
    assert summaries[0]["total_quantity"] == 999
    assert summaries[0]["theoretical_value"] == 777.77


def test_list_execution_summaries_falls_back_to_nested_result_metrics_when_persisted_are_none():
    records = [
        make_execution(
            1,
            number_of_legs=None,
            total_quantity=None,
            theoretical_value=None,
            nested_number_of_legs=4,
            nested_total_quantity=400,
            nested_theoretical_value=456.78,
        )
    ]
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository(records)
    )

    summaries = service.list_execution_summaries()

    assert len(summaries) == 1
    assert summaries[0]["number_of_legs"] == 4
    assert summaries[0]["total_quantity"] == 400
    assert summaries[0]["theoretical_value"] == 456.78


def test_list_execution_summaries_filters_by_structure_id():
    records = [
        make_execution(1, structure_id=10),
        make_execution(2, structure_id=20),
    ]
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository(records)
    )

    summaries = service.list_execution_summaries(structure_id=20)

    assert len(summaries) == 1
    assert summaries[0]["structure_id"] == 20
    assert summaries[0]["id"] == 2


def test_list_execution_summaries_filters_by_underlying_asset():
    records = [
        make_execution(1, underlying_asset="PETR4"),
        make_execution(2, underlying_asset="VALE3"),
    ]
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository(records)
    )

    summaries = service.list_execution_summaries(underlying_asset="VALE3")

    assert len(summaries) == 1
    assert summaries[0]["underlying_asset"] == "VALE3"
    assert summaries[0]["id"] == 2


def test_list_execution_summaries_filters_by_status():
    records = [
        make_execution(1, execution_status="ok"),
        make_execution(2, execution_status="error"),
    ]
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository(records)
    )

    summaries = service.list_execution_summaries(status="error")

    assert len(summaries) == 1
    assert summaries[0]["execution_status"] == "error"
    assert summaries[0]["id"] == 2


def test_list_execution_summaries_filters_by_reference_date():
    records = [
        make_execution(1, reference_date="2026-05-15"),
        make_execution(2, reference_date="2026-05-16"),
    ]
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository(records)
    )

    summaries = service.list_execution_summaries(reference_date="2026-05-16")

    assert len(summaries) == 1
    assert summaries[0]["reference_date"] == "2026-05-16"
    assert summaries[0]["id"] == 2


def test_list_execution_summaries_rejects_invalid_structure_id():
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository([])
    )

    try:
        service.list_execution_summaries(structure_id=0)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert str(exc) == "structure_id must be greater than zero"


def test_list_execution_summaries_rejects_empty_underlying_asset():
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository([])
    )

    try:
        service.list_execution_summaries(underlying_asset="   ")
        assert False, "expected ValueError"
    except ValueError as exc:
        assert str(exc) == "underlying_asset must not be empty"


def test_list_execution_summaries_rejects_invalid_status():
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository([])
    )

    try:
        service.list_execution_summaries(status="running")
        assert False, "expected ValueError"
    except ValueError as exc:
        assert str(exc) == "status must be either 'ok' or 'error'"


def test_list_execution_summaries_rejects_invalid_reference_date():
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository([])
    )

    try:
        service.list_execution_summaries(reference_date="16-05-2026")
        assert False, "expected ValueError"
    except ValueError as exc:
        assert str(exc) == "reference_date must be in YYYY-MM-DD format"


def test_paginate_execution_summaries_returns_page_metadata_and_items():
    records = [
        make_execution(1),
        make_execution(2),
        make_execution(3),
        make_execution(4),
        make_execution(5),
    ]
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository(records)
    )

    page = service.paginate_execution_summaries(page=2, page_size=2)

    assert page["page"] == 2
    assert page["page_size"] == 2
    assert page["total_items"] == 5
    assert page["total_pages"] == 3
    assert [item["id"] for item in page["items"]] == [3, 2]


def test_paginate_execution_summaries_returns_empty_items_when_page_exceeds_total_pages():
    records = [make_execution(1), make_execution(2)]
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository(records)
    )

    page = service.paginate_execution_summaries(page=3, page_size=2)

    assert page["page"] == 3
    assert page["page_size"] == 2
    assert page["total_items"] == 2
    assert page["total_pages"] == 1
    assert page["items"] == []


def test_paginate_execution_summaries_rejects_invalid_page():
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository([])
    )

    try:
        service.paginate_execution_summaries(page=0, page_size=10)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert str(exc) == "page must be greater than zero"


def test_paginate_execution_summaries_rejects_invalid_page_size():
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository([])
    )

    try:
        service.paginate_execution_summaries(page=1, page_size=0)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert str(exc) == "page_size must be greater than zero"


def test_get_latest_execution_summary_returns_highest_id_after_filtering():
    records = [
        make_execution(1, execution_status="ok"),
        make_execution(2, execution_status="error"),
        make_execution(3, execution_status="ok"),
    ]
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository(records)
    )

    latest = service.get_latest_execution_summary(status="ok")

    assert latest["id"] == 3
    assert latest["execution_status"] == "ok"


def test_get_latest_execution_summary_raises_when_no_items_found():
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository([])
    )

    try:
        service.get_latest_execution_summary()
        assert False, "expected ValueError"
    except ValueError as exc:
        assert str(exc) == "no pricing execution summaries found"


def test_get_execution_returns_record_when_found():
    records = [make_execution(1), make_execution(2)]
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository(records)
    )

    execution = service.get_execution(2)

    assert execution["id"] == 2


def test_get_execution_rejects_invalid_execution_id():
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository([])
    )

    try:
        service.get_execution(0)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert str(exc) == "execution_id must be greater than zero"


def test_get_execution_raises_not_found_when_missing():
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository([])
    )

    try:
        service.get_execution(123)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert str(exc) == "pricing execution 123 not found"


def test_get_execution_details_delegates_to_get_execution():
    records = [make_execution(7)]
    service = PricingExecutionQueryService(
        pricing_executions_repository=FakePricingExecutionsRepository(records)
    )

    execution = service.get_execution_details(7)

    assert execution["id"] == 7
