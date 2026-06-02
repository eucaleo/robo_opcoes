from services.pricing_execution_app_service import PricingExecutionAppService


class FakeCanonicalPricingFacade:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def execute_pricing(self, structure_id: int, reference_date: str | None = None):
        self.calls.append({"structure_id": structure_id, "reference_date": reference_date})
        return self.response


class FakePricingExecutionQueryService:
    def __init__(self):
        self.calls = []

    def list_execution_summaries(self, structure_id=None, underlying_asset=None,
                                  status=None, reference_date=None, descending=True):
        self.calls.append(("list_execution_summaries", {
            "structure_id": structure_id, "underlying_asset": underlying_asset,
            "status": status, "reference_date": reference_date, "descending": descending,
        }))
        return [{"id": 1}, {"id": 2}]

    def get_latest_execution_summary(self, structure_id=None, underlying_asset=None,
                                      status=None, reference_date=None):
        self.calls.append(("get_latest_execution_summary", {
            "structure_id": structure_id, "underlying_asset": underlying_asset,
            "status": status, "reference_date": reference_date,
        }))
        return {"id": 99}

    def get_execution(self, execution_id: int):
        self.calls.append(("get_execution", {"execution_id": execution_id}))
        return {"id": execution_id}

    def paginate_execution_summaries(self, structure_id=None, underlying_asset=None,
                                      status=None, reference_date=None, descending=True,
                                      page=1, page_size=10):
        self.calls.append(("paginate_execution_summaries", {
            "structure_id": structure_id, "underlying_asset": underlying_asset,
            "status": status, "reference_date": reference_date,
            "descending": descending, "page": page, "page_size": page_size,
        }))
        return {"items": [{"id": 10}], "page": page, "page_size": page_size,
                "total_items": 1, "total_pages": 1}


def _make_service(response, query_service=None):
    return PricingExecutionAppService(
        canonical_pricing_facade=FakeCanonicalPricingFacade(response),
        pricing_execution_query_service=query_service or FakePricingExecutionQueryService(),
    )


def test_execute_pricing_returns_persisted_record_when_present():
    facade = FakeCanonicalPricingFacade(response={
        "persisted": {"record": {"id": 123, "structure_id": 10, "reference_date": "2026-05-16"}}
    })
    service = PricingExecutionAppService(
        canonical_pricing_facade=facade,
        pricing_execution_query_service=FakePricingExecutionQueryService(),
    )
    result = service.execute_pricing(structure_id=10, reference_date="2026-05-16")
    assert result == {"id": 123, "structure_id": 10, "reference_date": "2026-05-16"}
    assert facade.calls == [{"structure_id": 10, "reference_date": "2026-05-16"}]


def test_execute_pricing_returns_raw_response_when_persisted_record_is_missing():
    raw_response = {"execution": {"status": "ok"}, "persisted": {"something_else": True}}
    facade = FakeCanonicalPricingFacade(response=raw_response)
    service = PricingExecutionAppService(
        canonical_pricing_facade=facade,
        pricing_execution_query_service=FakePricingExecutionQueryService(),
    )
    result = service.execute_pricing(structure_id=11, reference_date="2026-05-16")
    assert result == raw_response


def test_execute_pricing_rejects_invalid_structure_id():
    facade = FakeCanonicalPricingFacade(response={})
    service = PricingExecutionAppService(
        canonical_pricing_facade=facade,
        pricing_execution_query_service=FakePricingExecutionQueryService(),
    )
    try:
        service.execute_pricing(structure_id=0, reference_date="2026-05-16")
        assert False, "expected ValueError"
    except ValueError as exc:
        assert str(exc) == "structure_id must be greater than zero"
    assert facade.calls == []


def test_execute_pricing_rejects_invalid_reference_date():
    facade = FakeCanonicalPricingFacade(response={})
    service = PricingExecutionAppService(
        canonical_pricing_facade=facade,
        pricing_execution_query_service=FakePricingExecutionQueryService(),
    )
    try:
        service.execute_pricing(structure_id=10, reference_date="16-05-2026")
        assert False, "expected ValueError"
    except ValueError as exc:
        assert str(exc) == "reference_date must be in YYYY-MM-DD format"
    assert facade.calls == []


def test_execute_pricing_accepts_none_reference_date():
    facade = FakeCanonicalPricingFacade(
        response={"persisted": {"record": {"id": 55}}}
    )
    service = PricingExecutionAppService(
        canonical_pricing_facade=facade,
        pricing_execution_query_service=FakePricingExecutionQueryService(),
    )
    result = service.execute_pricing(structure_id=10, reference_date=None)
    assert result == {"id": 55}
    assert facade.calls == [{"structure_id": 10, "reference_date": None}]


def test_list_execution_summaries_delegates_to_query_service():
    query_service = FakePricingExecutionQueryService()
    service = _make_service(response={}, query_service=query_service)
    result = service.list_execution_summaries(
        structure_id=1, underlying_asset="PETR4",
        status="ok", reference_date="2026-05-16", descending=False,
    )
    assert result == [{"id": 1}, {"id": 2}]
    assert query_service.calls[0] == ("list_execution_summaries", {
        "structure_id": 1, "underlying_asset": "PETR4",
        "status": "ok", "reference_date": "2026-05-16", "descending": False,
    })


def test_get_latest_execution_summary_delegates_to_query_service():
    query_service = FakePricingExecutionQueryService()
    service = _make_service(response={}, query_service=query_service)
    result = service.get_latest_execution_summary(
        structure_id=2, underlying_asset="VALE3",
        status="error", reference_date="2026-05-15",
    )
    assert result == {"id": 99}
    assert query_service.calls[0] == ("get_latest_execution_summary", {
        "structure_id": 2, "underlying_asset": "VALE3",
        "status": "error", "reference_date": "2026-05-15",
    })


def test_get_execution_delegates_to_query_service():
    query_service = FakePricingExecutionQueryService()
    service = _make_service(response={}, query_service=query_service)
    result = service.get_execution(88)
    assert result == {"id": 88}
    assert query_service.calls[0] == ("get_execution", {"execution_id": 88})


def test_paginate_execution_summaries_delegates_to_query_service():
    query_service = FakePricingExecutionQueryService()
    service = _make_service(response={}, query_service=query_service)
    result = service.paginate_execution_summaries(
        structure_id=1, underlying_asset="PETR4",
        status="ok", reference_date="2026-05-16",
        descending=False, page=2, page_size=5,
    )
    assert result == {"items": [{"id": 10}], "page": 2, "page_size": 5,
                      "total_items": 1, "total_pages": 1}
    assert query_service.calls[0] == ("paginate_execution_summaries", {
        "structure_id": 1, "underlying_asset": "PETR4",
        "status": "ok", "reference_date": "2026-05-16",
        "descending": False, "page": 2, "page_size": 5,
    })
