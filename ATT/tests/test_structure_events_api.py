from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


FAKE_STRUCTURE = {
    "id": 1,
    "name": "Bull Call Spread",
    "underlying_asset": "PETR4",
    "alias_legacy_aba": None,
    "status": "active",
    "notes": None,
    "created_at": "2026-01-01T00:00:00+00:00",
    "updated_at": "2026-01-01T00:00:00+00:00",
    "legs": [],
}

FAKE_EVENT = {
    "id": 7,
    "structure_id": 1,
    "leg_id": None,
    "event_type": "opening",
    "event_status": "registered",
    "event_date": "2026-06-12",
    "quantity": 100,
    "price": 1.25,
    "symbol": "PETR4",
    "source": "manual",
    "notes": "abertura",
    "metadata": {"origin": "test"},
    "created_at": "2026-06-12T00:00:00Z",
    "updated_at": "2026-06-12T00:00:00Z",
}


FAKE_EFFECTIVE_STATE = {
    "structure_id": 1,
    "structure_status": "active",
    "is_closed": False,
    "effective_quantity_by_leg": {
        "10": 100,
        "11": -100,
    },
    "applied_events": [
        {
            "id": 7,
            "event_type": "opening",
            "event_status": "registered",
            "quantity": 100,
        }
    ],
    "ignored_events": [],
}

EVENT_PAYLOAD = {
    "event_type": "opening",
    "event_date": "2026-06-12",
    "quantity": 100,
    "price": 1.25,
    "symbol": "PETR4",
    "source": "manual",
    "notes": "abertura",
    "metadata": {"origin": "test"},
}


@pytest.fixture()
def mock_repo():
    repo = MagicMock()
    repo.get_structure.return_value = FAKE_STRUCTURE
    return repo


@pytest.fixture()
def mock_events_service():
    service = MagicMock()
    service.record_event.return_value = FAKE_EVENT
    service.list_events_for_structure.return_value = [FAKE_EVENT]
    service.list_events.return_value = [FAKE_EVENT]
    service.get_event.return_value = FAKE_EVENT
    service.cancel_event.return_value = {**FAKE_EVENT, "event_status": "cancelled"}
    service.apply_events_to_structure.return_value = FAKE_EFFECTIVE_STATE
    return service


@pytest.fixture()
def client(mock_repo, mock_events_service):
    with (
        patch("api.structures_controller._repo", mock_repo),
        patch("api.structures_controller._events_service", mock_events_service),
    ):
        from api.structures_controller import router

        app = FastAPI()
        app.include_router(router)
        yield TestClient(app), mock_repo, mock_events_service


class TestRecordStructureEvent:
    def test_record_event_retorna_201(self, client):
        tc, _, _ = client
        resp = tc.post("/structures/1/events", json=EVENT_PAYLOAD)
        assert resp.status_code == 201

    def test_record_event_retorna_evento(self, client):
        tc, _, _ = client
        resp = tc.post("/structures/1/events", json=EVENT_PAYLOAD)
        assert resp.json()["id"] == 7
        assert resp.json()["event_type"] == "opening"

    def test_record_event_chama_service_com_structure_id(self, client):
        tc, _, service = client
        tc.post("/structures/1/events", json=EVENT_PAYLOAD)
        kwargs = service.record_event.call_args.kwargs
        assert kwargs["structure_id"] == 1

    def test_record_event_chama_service_com_payload(self, client):
        tc, _, service = client
        tc.post("/structures/1/events", json=EVENT_PAYLOAD)
        kwargs = service.record_event.call_args.kwargs
        assert kwargs["event_type"] == "opening"
        assert kwargs["price"] == 1.25
        assert kwargs["metadata"] == {"origin": "test"}

    def test_record_event_404_quando_estrutura_nao_existe(self, client):
        tc, repo, service = client
        repo.get_structure.return_value = None
        resp = tc.post("/structures/999/events", json=EVENT_PAYLOAD)
        assert resp.status_code == 404
        service.record_event.assert_not_called()

    def test_record_event_400_quando_service_levanta_value_error(self, client):
        tc, _, service = client
        service.record_event.side_effect = ValueError("event_type inválido")
        resp = tc.post("/structures/1/events", json=EVENT_PAYLOAD)
        assert resp.status_code == 400
        assert "event_type inválido" in resp.json()["detail"]

    def test_record_event_404_quando_service_informa_not_found(self, client):
        tc, _, service = client
        service.record_event.side_effect = ValueError("leg not found for structure")
        resp = tc.post("/structures/1/events", json=EVENT_PAYLOAD)
        assert resp.status_code == 404

    def test_record_event_422_event_type_invalido(self, client):
        tc, _, _ = client
        payload = {**EVENT_PAYLOAD, "event_type": "invalid"}
        resp = tc.post("/structures/1/events", json=payload)
        assert resp.status_code == 422

    def test_record_event_422_event_date_invalida(self, client):
        tc, _, _ = client
        payload = {**EVENT_PAYLOAD, "event_date": "12/06/2026"}
        resp = tc.post("/structures/1/events", json=payload)
        assert resp.status_code == 422

    def test_record_event_normaliza_retorno_int_para_event_id(self, client):
        tc, _, service = client
        service.record_event.return_value = 77
        resp = tc.post("/structures/1/events", json=EVENT_PAYLOAD)
        assert resp.status_code == 201
        assert resp.json() == {"event_id": 77}


class TestListStructureEvents:
    def test_list_structure_events_retorna_200(self, client):
        tc, _, _ = client
        resp = tc.get("/structures/1/events")
        assert resp.status_code == 200

    def test_list_structure_events_retorna_lista(self, client):
        tc, _, _ = client
        resp = tc.get("/structures/1/events")
        assert resp.json()[0]["id"] == 7

    def test_list_structure_events_chama_service(self, client):
        tc, _, service = client
        tc.get("/structures/1/events?include_cancelled=true")
        service.list_events_for_structure.assert_called_once_with(
            1,
            include_cancelled=True,
        )

    def test_list_structure_events_404_estrutura_inexistente(self, client):
        tc, repo, service = client
        repo.get_structure.return_value = None
        resp = tc.get("/structures/999/events")
        assert resp.status_code == 404
        service.list_events_for_structure.assert_not_called()


class TestListEvents:
    def test_list_events_retorna_200(self, client):
        tc, _, _ = client
        resp = tc.get("/structure-events")
        assert resp.status_code == 200

    def test_list_events_repassa_filtros(self, client):
        tc, _, service = client
        tc.get(
            "/structure-events?"
            "structure_id=1&event_type=opening&event_status=registered&"
            "include_cancelled=true&limit=25&offset=5"
        )
        service.list_events.assert_called_once_with(
            structure_id=1,
            event_type="opening",
            event_status="registered",
            include_cancelled=True,
            limit=25,
            offset=5,
        )

    def test_list_events_422_limit_invalido(self, client):
        tc, _, _ = client
        resp = tc.get("/structure-events?limit=0")
        assert resp.status_code == 422

    def test_list_events_400_quando_service_levanta_value_error(self, client):
        tc, _, service = client
        service.list_events.side_effect = ValueError("event_type inválido")
        resp = tc.get("/structure-events?event_type=invalid")
        assert resp.status_code == 400


class TestGetStructureEvent:
    def test_get_event_retorna_200(self, client):
        tc, _, _ = client
        resp = tc.get("/structure-events/7")
        assert resp.status_code == 200

    def test_get_event_retorna_evento(self, client):
        tc, _, _ = client
        resp = tc.get("/structure-events/7")
        assert resp.json()["id"] == 7

    def test_get_event_chama_service(self, client):
        tc, _, service = client
        tc.get("/structure-events/7")
        service.get_event.assert_called_once_with(7)

    def test_get_event_404_quando_nao_existe(self, client):
        tc, _, service = client
        service.get_event.return_value = None
        resp = tc.get("/structure-events/999")
        assert resp.status_code == 404

    def test_get_event_400_id_invalido_no_service(self, client):
        tc, _, service = client
        service.get_event.side_effect = ValueError("event_id must be greater than zero")
        resp = tc.get("/structure-events/7")
        assert resp.status_code == 400


class TestCancelStructureEvent:
    def test_cancel_event_retorna_200(self, client):
        tc, _, _ = client
        resp = tc.post("/structure-events/7/cancel", json={"notes": "cancelado"})
        assert resp.status_code == 200

    def test_cancel_event_retorna_evento_cancelado(self, client):
        tc, _, _ = client
        resp = tc.post("/structure-events/7/cancel", json={"notes": "cancelado"})
        assert resp.json()["event_status"] == "cancelled"

    def test_cancel_event_chama_service(self, client):
        tc, _, service = client
        tc.post("/structure-events/7/cancel", json={"notes": "cancelado"})
        service.cancel_event.assert_called_once_with(7, notes="cancelado")

    def test_cancel_event_aceita_body_vazio(self, client):
        tc, _, service = client
        resp = tc.post("/structure-events/7/cancel", json={})
        assert resp.status_code == 200
        service.cancel_event.assert_called_once_with(7, notes=None)

    def test_cancel_event_404_quando_not_found(self, client):
        tc, _, service = client
        service.cancel_event.side_effect = ValueError("event not found: 999")
        resp = tc.post("/structure-events/999/cancel", json={})
        assert resp.status_code == 404

    def test_cancel_event_normaliza_retorno_int(self, client):
        tc, _, service = client
        service.cancel_event.return_value = 7
        resp = tc.post("/structure-events/7/cancel", json={})
        assert resp.json() == {"event_id": 7}


class TestGetStructureEffectiveState:
    def test_get_effective_state_retorna_200(self, client):
        tc, _, _ = client
        resp = tc.get("/structures/1/effective")
        assert resp.status_code == 200

    def test_get_effective_state_retorna_estado_efetivo(self, client):
        tc, _, _ = client
        resp = tc.get("/structures/1/effective")
        body = resp.json()
        assert body["structure_id"] == 1
        assert body["is_closed"] is False
        assert body["effective_quantity_by_leg"]["10"] == 100
        assert body["applied_events"][0]["id"] == 7

    def test_get_effective_state_chama_service(self, client):
        tc, _, service = client
        tc.get("/structures/1/effective")
        service.apply_events_to_structure.assert_called_once_with(FAKE_STRUCTURE)

    def test_get_effective_state_404_estrutura_inexistente(self, client):
        tc, repo, service = client
        repo.get_structure.return_value = None
        resp = tc.get("/structures/999/effective")
        assert resp.status_code == 404
        service.apply_events_to_structure.assert_not_called()

    def test_get_effective_state_400_quando_service_levanta_value_error(self, client):
        tc, _, service = client
        service.apply_events_to_structure.side_effect = ValueError("invalid structure_id")
        resp = tc.get("/structures/1/effective")
        assert resp.status_code == 400
        assert "invalid structure_id" in resp.json()["detail"]

