"""
patch_51 -- testes de contrato da API REST de estruturas.

Usa TestClient do FastAPI (sem banco real -- repositório mockado).
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

FAKE_STRUCTURE = {
    "id": 1,
    "name": "Trava Alta PETR4",
    "underlying_asset": "PETR4",
    "alias_legacy_aba": "PETR4_TRAVA",
    "status": "active",
    "notes": None,
    "created_at": "2026-06-01T00:00:00",
    "updated_at": "2026-06-01T00:00:00",
    "legs": [],
}

FAKE_SUMMARY = {k: v for k, v in FAKE_STRUCTURE.items() if k != "legs"}


@pytest.fixture()
def mock_repo():
    repo = MagicMock()
    repo.create_structure.return_value = 1
    repo.list_structures.return_value = [FAKE_SUMMARY]
    repo.get_structure.return_value = FAKE_STRUCTURE
    repo.update_structure.return_value = None
    repo.archive_structure.return_value = None
    return repo


@pytest.fixture()
def client(mock_repo):
    with patch("api.structures_controller._repo", mock_repo):
        from api.structures_controller import router
        from fastapi import FastAPI

        app = FastAPI()
        app.include_router(router)
        yield TestClient(app), mock_repo


# ---------------------------------------------------------------------------
# POST /structures
# ---------------------------------------------------------------------------

class TestCreateStructure:
    def test_cria_e_retorna_201(self, client):
        tc, repo = client
        resp = tc.post("/structures", json={
            "name": "Trava Alta PETR4",
            "underlying_asset": "PETR4",
        })
        assert resp.status_code == 201
        assert resp.json() == {"structure_id": 1}

    def test_repo_chamado_com_payload_correto(self, client):
        tc, repo = client
        tc.post("/structures", json={
            "name": "Trava Alta PETR4",
            "underlying_asset": "PETR4",
            "alias_legacy_aba": "PETR4_TRAVA",
        })
        call_data = repo.create_structure.call_args[0][0]
        assert call_data["name"] == "Trava Alta PETR4"
        assert call_data["alias_legacy_aba"] == "PETR4_TRAVA"

    def test_400_quando_repo_levanta_value_error(self, client):
        tc, repo = client
        repo.create_structure.side_effect = ValueError("nome duplicado")
        resp = tc.post("/structures", json={
            "name": "X",
            "underlying_asset": "Y",
        })
        assert resp.status_code == 400
        assert "nome duplicado" in resp.json()["detail"]

    def test_422_sem_campo_obrigatorio(self, client):
        tc, _ = client
        resp = tc.post("/structures", json={"name": "Sem ativo"})
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# GET /structures
# ---------------------------------------------------------------------------

class TestListStructures:
    def test_retorna_200_e_lista(self, client):
        tc, _ = client
        resp = tc.get("/structures")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
        assert len(resp.json()) == 1

    def test_include_archived_false_por_padrao(self, client):
        tc, repo = client
        tc.get("/structures")
        repo.list_structures.assert_called_once_with(include_archived=False)

    def test_include_archived_true_quando_passado(self, client):
        tc, repo = client
        tc.get("/structures?include_archived=true")
        repo.list_structures.assert_called_once_with(include_archived=True)


# ---------------------------------------------------------------------------
# GET /structures/{id}
# ---------------------------------------------------------------------------

class TestGetStructure:
    def test_retorna_200_com_legs(self, client):
        tc, _ = client
        resp = tc.get("/structures/1")
        assert resp.status_code == 200
        assert "legs" in resp.json()

    def test_404_quando_nao_encontrado(self, client):
        tc, repo = client
        repo.get_structure.return_value = None
        resp = tc.get("/structures/999")
        assert resp.status_code == 404
        assert "999" in resp.json()["detail"]


# ---------------------------------------------------------------------------
# PATCH /structures/{id}
# ---------------------------------------------------------------------------

class TestUpdateStructure:
    def test_retorna_204(self, client):
        tc, _ = client
        resp = tc.patch("/structures/1", json={"notes": "atualizado"})
        assert resp.status_code == 204

    def test_repo_update_chamado(self, client):
        tc, repo = client
        tc.patch("/structures/1", json={"notes": "nova nota"})
        repo.update_structure.assert_called_once()
        args = repo.update_structure.call_args[0]
        assert args[0] == 1
        assert args[1]["notes"] == "nova nota"

    def test_400_sem_campos(self, client):
        tc, _ = client
        resp = tc.patch("/structures/1", json={})
        assert resp.status_code == 400

    def test_404_quando_nao_encontrado(self, client):
        tc, repo = client
        repo.get_structure.return_value = None
        resp = tc.patch("/structures/999", json={"notes": "x"})
        assert resp.status_code == 404

    def test_422_status_invalido(self, client):
        tc, _ = client
        resp = tc.patch("/structures/1", json={"status": "deletado"})
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# DELETE /structures/{id}
# ---------------------------------------------------------------------------

class TestArchiveStructure:
    def test_retorna_204(self, client):
        tc, _ = client
        resp = tc.delete("/structures/1")
        assert resp.status_code == 204

    def test_repo_archive_chamado(self, client):
        tc, repo = client
        tc.delete("/structures/1")
        repo.archive_structure.assert_called_once_with(1)

    def test_404_quando_nao_encontrado(self, client):
        tc, repo = client
        repo.get_structure.return_value = None
        resp = tc.delete("/structures/999")
        assert resp.status_code == 404
