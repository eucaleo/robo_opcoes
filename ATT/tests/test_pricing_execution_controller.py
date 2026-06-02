from fastapi.testclient import TestClient

import api.pricing_execution_controller as controller
from main import app


class FakePricingExecutionAppService:
    def __init__(self):
        self.calls = []
        self.execute_pricing_response = {
            "id": 1,
            "structure_id": 10,
            "reference_date": "2026-05-16",
        }
        self.paginate_execution_summaries_response = {
            "items": [{"id": 1}, {"id": 2}],
            "page": 1,
            "page_size": 10,
            "total_items": 2,
            "total_pages": 1,
        }
        self.get_latest_execution_summary_response = {"id": 2}
        self.get_execution_response = {"id": 1}

        self.execute_pricing_exception = None
        self.paginate_execution_summaries_exception = None
        self.get_latest_execution_summary_exception = None
        self.get_execution_exception = None

    def execute_pricing(self, structure_id: int, reference_date: str):
        self.calls.append(
            (
                "execute_pricing",
                {
                    "structure_id": structure_id,
                    "reference_date": reference_date,
                },
            )
        )
        if self.execute_pricing_exception:
            raise self.execute_pricing_exception
        return self.execute_pricing_response

    def paginate_execution_summaries(
        self,
        structure_id=None,
        underlying_asset=None,
        status=None,
        reference_date=None,
        page=1,
        page_size=10,
    ):
        self.calls.append(
            (
                "paginate_execution_summaries",
                {
                    "structure_id": structure_id,
                    "underlying_asset": underlying_asset,
                    "status": status,
                    "reference_date": reference_date,
                    "page": page,
                    "page_size": page_size,
                },
            )
        )
        if self.paginate_execution_summaries_exception:
            raise self.paginate_execution_summaries_exception
        return self.paginate_execution_summaries_response

    def get_latest_execution_summary(
        self,
        structure_id=None,
        underlying_asset=None,
        status=None,
        reference_date=None,
    ):
        self.calls.append(
            (
                "get_latest_execution_summary",
                {
                    "structure_id": structure_id,
                    "underlying_asset": underlying_asset,
                    "status": status,
                    "reference_date": reference_date,
                },
            )
        )
        if self.get_latest_execution_summary_exception:
            raise self.get_latest_execution_summary_exception
        return self.get_latest_execution_summary_response

    def get_execution(self, execution_id: int):
        self.calls.append(("get_execution", {"execution_id": execution_id}))
        if self.get_execution_exception:
            raise self.get_execution_exception
        return self.get_execution_response


def build_client_with_fake_service():
    fake_service = FakePricingExecutionAppService()
    original_service = controller.service
    controller.service = fake_service
    client = TestClient(app)
    return client, fake_service, original_service


def restore_service(original_service):
    controller.service = original_service


def test_create_pricing_execution_returns_200_and_payload():
    client, fake_service, original_service = build_client_with_fake_service()
    try:
        response = client.post(
            "/pricing-executions",
            json={
                "structure_id": 10,
                "reference_date": "2026-05-16",
            },
        )

        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "structure_id": 10,
            "reference_date": "2026-05-16",
        }
        assert fake_service.calls[0] == (
            "execute_pricing",
            {
                "structure_id": 10,
                "reference_date": "2026-05-16",
            },
        )
    finally:
        restore_service(original_service)


def test_create_pricing_execution_returns_404_when_value_error_contains_not_found():
    client, fake_service, original_service = build_client_with_fake_service()
    fake_service.execute_pricing_exception = ValueError("structure 999 not found")

    try:
        response = client.post(
            "/pricing-executions",
            json={
                "structure_id": 999,
                "reference_date": "2026-05-16",
            },
        )

        assert response.status_code == 404
        assert response.json() == {"detail": "structure 999 not found"}
    finally:
        restore_service(original_service)


def test_create_pricing_execution_returns_400_for_generic_value_error():
    client, fake_service, original_service = build_client_with_fake_service()
    fake_service.execute_pricing_exception = ValueError(
        "reference_date must be in YYYY-MM-DD format"
    )

    try:
        response = client.post(
            "/pricing-executions",
            json={
                "structure_id": 10,
                "reference_date": "16-05-2026",
            },
        )

        assert response.status_code == 400
        assert response.json() == {
            "detail": "reference_date must be in YYYY-MM-DD format"
        }
    finally:
        restore_service(original_service)


def test_list_pricing_executions_returns_paginated_response():
    client, fake_service, original_service = build_client_with_fake_service()
    try:
        response = client.get(
            "/pricing-executions",
            params={
                "structure_id": 10,
                "underlying_asset": "PETR4",
                "status": "ok",
                "reference_date": "2026-05-16",
                "page": 2,
                "page_size": 5,
            },
        )

        assert response.status_code == 200
        assert response.json() == {
            "items": [{"id": 1}, {"id": 2}],
            "page": 1,
            "page_size": 10,
            "total_items": 2,
            "total_pages": 1,
        }
        assert fake_service.calls[0] == (
            "paginate_execution_summaries",
            {
                "structure_id": 10,
                "underlying_asset": "PETR4",
                "status": "ok",
                "reference_date": "2026-05-16",
                "page": 2,
                "page_size": 5,
            },
        )
    finally:
        restore_service(original_service)


def test_list_pricing_executions_returns_400_on_service_value_error():
    client, fake_service, original_service = build_client_with_fake_service()
    fake_service.paginate_execution_summaries_exception = ValueError(
        "status must be either 'ok' or 'error'"
    )

    try:
        response = client.get("/pricing-executions", params={"status": "running"})

        assert response.status_code == 400
        assert response.json() == {"detail": "status must be either 'ok' or 'error'"}
    finally:
        restore_service(original_service)


def test_get_latest_pricing_execution_returns_200():
    client, fake_service, original_service = build_client_with_fake_service()
    fake_service.get_latest_execution_summary_response = {"id": 5, "execution_status": "ok"}

    try:
        response = client.get(
            "/pricing-executions/latest",
            params={
                "structure_id": 10,
                "underlying_asset": "PETR4",
                "status": "ok",
                "reference_date": "2026-05-16",
            },
        )

        assert response.status_code == 200
        assert response.json() == {"id": 5, "execution_status": "ok"}
        assert fake_service.calls[0] == (
            "get_latest_execution_summary",
            {
                "structure_id": 10,
                "underlying_asset": "PETR4",
                "status": "ok",
                "reference_date": "2026-05-16",
            },
        )
    finally:
        restore_service(original_service)


def test_get_latest_pricing_execution_returns_404_when_no_summary_found():
    client, fake_service, original_service = build_client_with_fake_service()
    fake_service.get_latest_execution_summary_exception = ValueError(
        "no pricing execution summaries found"
    )

    try:
        response = client.get("/pricing-executions/latest")

        assert response.status_code == 404
        assert response.json() == {"detail": "no pricing execution summaries found"}
    finally:
        restore_service(original_service)


def test_get_latest_pricing_execution_returns_400_for_generic_value_error():
    client, fake_service, original_service = build_client_with_fake_service()
    fake_service.get_latest_execution_summary_exception = ValueError(
        "reference_date must be in YYYY-MM-DD format"
    )

    try:
        response = client.get(
            "/pricing-executions/latest",
            params={"reference_date": "16-05-2026"},
        )

        assert response.status_code == 400
        assert response.json() == {
            "detail": "reference_date must be in YYYY-MM-DD format"
        }
    finally:
        restore_service(original_service)


def test_get_pricing_execution_returns_200():
    client, fake_service, original_service = build_client_with_fake_service()
    fake_service.get_execution_response = {"id": 8, "execution_status": "ok"}

    try:
        response = client.get("/pricing-executions/8")

        assert response.status_code == 200
        assert response.json() == {"id": 8, "execution_status": "ok"}
        assert fake_service.calls[0] == ("get_execution", {"execution_id": 8})
    finally:
        restore_service(original_service)


def test_get_pricing_execution_returns_404_when_not_found():
    client, fake_service, original_service = build_client_with_fake_service()
    fake_service.get_execution_exception = ValueError("pricing execution 8 not found")

    try:
        response = client.get("/pricing-executions/8")

        assert response.status_code == 404
        assert response.json() == {"detail": "pricing execution 8 not found"}
    finally:
        restore_service(original_service)


def test_get_pricing_execution_returns_400_for_generic_value_error():
    client, fake_service, original_service = build_client_with_fake_service()
    fake_service.get_execution_exception = ValueError(
        "execution_id must be greater than zero"
    )

    try:
        response = client.get("/pricing-executions/0")

        assert response.status_code == 400
        assert response.json() == {"detail": "execution_id must be greater than zero"}
    finally:
        restore_service(original_service)
