# Testes da API de estruturas
"""
Testes de contrato da API REST de estruturas.

Usa TestClient do FastAPI (repositório mockado via unittest.mock).
Cobertura: POST / GET (lista) / GET (detalhe) / PATCH / DELETE

Adições vs versão anterior:
  - TestCreateStructure  : alias_legacy_aba + notes opcionais; status_code correto
  - TestListStructures   : serialização dos campos do summary
  - TestGetStructure     : campos obrigatórios na resposta; legs presente e é lista
  - TestUpdateStructure  : underlying_asset; alias; merge parcial; value_error -> 400
  - TestArchiveStructure : idempotência de chamada; value_error -> 400
  - TestSchemas          : validações de schema Pydantic (422) para campos inválidos
"""
from __future__ import annotations

from unittest.mock import MagicMock, call, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Dados de fixture
# ---------------------------------------------------------------------------

FAKE_STRUCTURE = {
    "id": 1,
    "name": "Trava Alta PETR4",
    "underlying_asset": "PETR4",
    "alias_legacy_aba": "PETR4_TRAVA",
    "status": "active",
    "notes": "estrutura de teste",
    "created_at": "2026-06-01T00:00:00+00:00",
    "updated_at": "2026-06-01T00:00:00+00:00",
    "legs": [
        {
            "id": 10,
            "structure_id": 1,
            "position_side": "COMPRADO",
            "option_type": "CALL",
            "symbol": "PETRJ240",
            "strike": 38.0,
            "expiration_date": "2026-07-18",
            "quantity": 1,
            "premium": 1.25,
            "multiplier": 100.0,
            "leg_order": 1,
            "notes": None,
            "created_at": "2026-06-01T00:00:00+00:00",
            "updated_at": "2026-06-01T00:00:00+00:00",
        }
    ],
}

FAKE_SUMMARY = {k: v for k, v in FAKE_STRUCTURE.items() if k != "legs"}

# ---------------------------------------------------------------------------
# Testes dos endpoints de legs
# ---------------------------------------------------------------------------

FAKE_LEG_PAYLOAD = {
    "position_side":   "COMPRADO",
    "option_type":     "CALL",
    "strike":          38.0,
    "expiration_date": "2026-07-18",
    "quantity":        1,
    "multiplier":      100.0,
    "leg_order":       1,
    "symbol":          "PETRJ240",
    "premium":         1.25,
    "notes":           None,
}

REPLACE_LEGS_PAYLOAD = {
    "legs": [FAKE_LEG_PAYLOAD]
}


@pytest.fixture()
def client_legs(mock_repo):
    """Client com add_leg e replace_legs mockados."""
    mock_repo.add_leg.return_value = 10
    mock_repo.replace_legs.return_value = None

    with patch("api.structures_controller._repo", mock_repo):
        from api.structures_controller import router

        app = FastAPI()
        app.include_router(router)
        yield TestClient(app), mock_repo




# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

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
    """Cria TestClient com repositório mockado injetado no controller."""
    with patch("api.structures_controller._repo", mock_repo):
        from api.structures_controller import router

        app = FastAPI()
        app.include_router(router)
        yield TestClient(app), mock_repo


# ---------------------------------------------------------------------------
# POST /structures
# ---------------------------------------------------------------------------

class TestCreateStructure:
    """Testes do endpoint POST /structures."""

    def test_cria_e_retorna_201(self, client):
        tc, _ = client
        resp = tc.post("/structures", json={
            "name": "Trava Alta PETR4",
            "underlying_asset": "PETR4",
        })
        assert resp.status_code == 201
        assert resp.json() == {"structure_id": 1}

    def test_retorna_structure_id_correto(self, client):
        tc, repo = client
        repo.create_structure.return_value = 42
        resp = tc.post("/structures", json={
            "name": "Qualquer",
            "underlying_asset": "VALE3",
        })
        assert resp.status_code == 201
        assert resp.json()["structure_id"] == 42

    def test_payload_minimo_sem_opcionais(self, client):
        """Campos opcionais ausentes não devem gerar erro."""
        tc, repo = client
        resp = tc.post("/structures", json={
            "name": "Estrutura Mínima",
            "underlying_asset": "BBAS3",
        })
        assert resp.status_code == 201
        payload = repo.create_structure.call_args[0][0]
        assert "alias_legacy_aba" in payload
        assert "notes" in payload

    def test_payload_completo_com_alias_e_notes(self, client):
        tc, repo = client
        tc.post("/structures", json={
            "name": "Trava Alta PETR4",
            "underlying_asset": "PETR4",
            "alias_legacy_aba": "PETR4_TRAVA",
            "notes": "estrutura legada migrada",
        })
        payload = repo.create_structure.call_args[0][0]
        assert payload["alias_legacy_aba"] == "PETR4_TRAVA"
        assert payload["notes"] == "estrutura legada migrada"

    def test_repo_chamado_exatamente_uma_vez(self, client):
        tc, repo = client
        tc.post("/structures", json={
            "name": "X",
            "underlying_asset": "Y",
        })
        repo.create_structure.assert_called_once()

    def test_repo_chamado_com_name_correto(self, client):
        tc, repo = client
        tc.post("/structures", json={
            "name": "Trava Alta PETR4",
            "underlying_asset": "PETR4",
        })
        payload = repo.create_structure.call_args[0][0]
        assert payload["name"] == "Trava Alta PETR4"
        assert payload["underlying_asset"] == "PETR4"

    def test_400_quando_repo_levanta_value_error(self, client):
        tc, repo = client
        repo.create_structure.side_effect = ValueError("nome duplicado")
        resp = tc.post("/structures", json={
            "name": "X",
            "underlying_asset": "Y",
        })
        assert resp.status_code == 400
        assert "nome duplicado" in resp.json()["detail"]

    def test_400_mensagem_de_erro_propagada(self, client):
        tc, repo = client
        repo.create_structure.side_effect = ValueError("underlying_asset inválido")
        resp = tc.post("/structures", json={
            "name": "Teste",
            "underlying_asset": "???",
        })
        assert "underlying_asset inválido" in resp.json()["detail"]

    def test_422_sem_campo_obrigatorio_underlying_asset(self, client):
        tc, _ = client
        resp = tc.post("/structures", json={"name": "Sem ativo"})
        assert resp.status_code == 422

    def test_422_sem_campo_obrigatorio_name(self, client):
        tc, _ = client
        resp = tc.post("/structures", json={"underlying_asset": "PETR4"})
        assert resp.status_code == 422

    def test_422_name_vazio(self, client):
        """name com string vazia deve violar min_length=1."""
        tc, _ = client
        resp = tc.post("/structures", json={
            "name": "",
            "underlying_asset": "PETR4",
        })
        assert resp.status_code == 422

    def test_422_underlying_asset_vazio(self, client):
        tc, _ = client
        resp = tc.post("/structures", json={
            "name": "Válido",
            "underlying_asset": "",
        })
        assert resp.status_code == 422

    def test_422_body_ausente(self, client):
        tc, _ = client
        resp = tc.post("/structures")
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# GET /structures
# ---------------------------------------------------------------------------

class TestListStructures:
    """Testes do endpoint GET /structures."""

    def test_retorna_200(self, client):
        tc, _ = client
        resp = tc.get("/structures")
        assert resp.status_code == 200

    def test_retorna_lista(self, client):
        tc, _ = client
        resp = tc.get("/structures")
        assert isinstance(resp.json(), list)

    def test_lista_com_um_item(self, client):
        tc, _ = client
        resp = tc.get("/structures")
        assert len(resp.json()) == 1

    def test_campos_obrigatorios_no_summary(self, client):
        tc, _ = client
        resp = tc.get("/structures")
        item = resp.json()[0]
        for campo in ("id", "name", "underlying_asset", "status", "created_at", "updated_at"):
            assert campo in item, f"campo ausente no summary: {campo}"

    def test_summary_nao_contem_legs(self, client):
        """Listagem não deve retornar legs (otimização de payload)."""
        tc, _ = client
        resp = tc.get("/structures")
        assert "legs" not in resp.json()[0]

    def test_include_archived_false_por_padrao(self, client):
        tc, repo = client
        tc.get("/structures")
        repo.list_structures.assert_called_once_with(include_archived=False)

    def test_include_archived_true_quando_passado(self, client):
        tc, repo = client
        tc.get("/structures?include_archived=true")
        repo.list_structures.assert_called_once_with(include_archived=True)

    def test_include_archived_false_explicito(self, client):
        tc, repo = client
        tc.get("/structures?include_archived=false")
        repo.list_structures.assert_called_once_with(include_archived=False)

    def test_lista_vazia_retorna_200(self, client):
        tc, repo = client
        repo.list_structures.return_value = []
        resp = tc.get("/structures")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_lista_com_multiplos_itens(self, client):
        tc, repo = client
        segundo = {**FAKE_SUMMARY, "id": 2, "name": "Outra Estrutura"}
        repo.list_structures.return_value = [FAKE_SUMMARY, segundo]
        resp = tc.get("/structures")
        assert len(resp.json()) == 2


# ---------------------------------------------------------------------------
# GET /structures/{id}
# ---------------------------------------------------------------------------

class TestGetStructure:
    """Testes do endpoint GET /structures/{id}."""

    def test_retorna_200(self, client):
        tc, _ = client
        resp = tc.get("/structures/1")
        assert resp.status_code == 200

    def test_campo_legs_presente(self, client):
        tc, _ = client
        resp = tc.get("/structures/1")
        assert "legs" in resp.json()

    def test_legs_e_lista(self, client):
        tc, _ = client
        resp = tc.get("/structures/1")
        assert isinstance(resp.json()["legs"], list)

    def test_legs_com_um_item(self, client):
        tc, _ = client
        resp = tc.get("/structures/1")
        assert len(resp.json()["legs"]) == 1

    def test_campos_obrigatorios_no_detalhe(self, client):
        tc, _ = client
        resp = tc.get("/structures/1")
        body = resp.json()
        for campo in ("id", "name", "underlying_asset", "status", "legs", "created_at", "updated_at"):
            assert campo in body, f"campo ausente no detalhe: {campo}"

    def test_id_correto_na_resposta(self, client):
        tc, _ = client
        resp = tc.get("/structures/1")
        assert resp.json()["id"] == 1

    def test_repo_chamado_com_id_correto(self, client):
        tc, repo = client
        tc.get("/structures/7")
        repo.get_structure.assert_called_once_with(7)

    def test_404_quando_nao_encontrado(self, client):
        tc, repo = client
        repo.get_structure.return_value = None
        resp = tc.get("/structures/999")
        assert resp.status_code == 404

    def test_404_detalhe_contem_id(self, client):
        tc, repo = client
        repo.get_structure.return_value = None
        resp = tc.get("/structures/999")
        assert "999" in resp.json()["detail"]

    def test_404_id_zero(self, client):
        """ID 0 deve resultar em 404 (inexistente)."""
        tc, repo = client
        repo.get_structure.return_value = None
        resp = tc.get("/structures/0")
        assert resp.status_code == 404

    def test_leg_campos_obrigatorios(self, client):
        tc, _ = client
        resp = tc.get("/structures/1")
        leg = resp.json()["legs"][0]
        for campo in ("id", "structure_id", "position_side", "option_type", "strike",
                      "expiration_date", "quantity", "multiplier", "leg_order"):
            assert campo in leg, f"campo ausente na leg: {campo}"


# ---------------------------------------------------------------------------
# PATCH /structures/{id}
# ---------------------------------------------------------------------------

class TestUpdateStructure:
    """Testes do endpoint PATCH /structures/{id}."""

    def test_retorna_204(self, client):
        tc, _ = client
        resp = tc.patch("/structures/1", json={"notes": "atualizado"})
        assert resp.status_code == 204

    def test_sem_body_na_resposta_204(self, client):
        """204 No Content não deve retornar body."""
        tc, _ = client
        resp = tc.patch("/structures/1", json={"notes": "x"})
        assert resp.content == b""

    def test_repo_update_chamado_com_id_correto(self, client):
        tc, repo = client
        tc.patch("/structures/1", json={"notes": "nova nota"})
        args = repo.update_structure.call_args[0]
        assert args[0] == 1

    def test_repo_update_chamado_com_notes(self, client):
        tc, repo = client
        tc.patch("/structures/1", json={"notes": "nova nota"})
        args = repo.update_structure.call_args[0]
        assert args[1]["notes"] == "nova nota"

    def test_atualiza_name(self, client):
        tc, repo = client
        tc.patch("/structures/1", json={"name": "Novo Nome"})
        args = repo.update_structure.call_args[0]
        assert args[1]["name"] == "Novo Nome"

    def test_atualiza_underlying_asset(self, client):
        tc, repo = client
        tc.patch("/structures/1", json={"underlying_asset": "VALE3"})
        args = repo.update_structure.call_args[0]
        assert args[1]["underlying_asset"] == "VALE3"

    def test_atualiza_alias_legacy_aba(self, client):
        tc, repo = client
        tc.patch("/structures/1", json={"alias_legacy_aba": "NOVO_ALIAS"})
        args = repo.update_structure.call_args[0]
        assert args[1]["alias_legacy_aba"] == "NOVO_ALIAS"

    def test_atualiza_status_para_archived(self, client):
        tc, repo = client
        resp = tc.patch("/structures/1", json={"status": "archived"})
        assert resp.status_code == 204
        args = repo.update_structure.call_args[0]
        assert args[1]["status"] == "archived"

    def test_atualiza_status_para_active(self, client):
        tc, repo = client
        resp = tc.patch("/structures/1", json={"status": "active"})
        assert resp.status_code == 204

    def test_merge_parcial_so_envia_campos_presentes(self, client):
        """PATCH não deve enviar campos None como parte do payload."""
        tc, repo = client
        tc.patch("/structures/1", json={"notes": "apenas notes"})
        payload = repo.update_structure.call_args[0][1]
        # campos não enviados não devem estar no payload filtrado
        assert "name" not in payload
        assert "underlying_asset" not in payload

    def test_400_sem_campos(self, client):
        tc, _ = client
        resp = tc.patch("/structures/1", json={})
        assert resp.status_code == 400

    def test_400_mensagem_no_fields(self, client):
        tc, _ = client
        resp = tc.patch("/structures/1", json={})
        assert resp.status_code == 400
        assert resp.json()["detail"]  # garante que detail existe e não é vazio

    def test_404_quando_nao_encontrado(self, client):
        tc, repo = client
        repo.get_structure.return_value = None
        resp = tc.patch("/structures/999", json={"notes": "x"})
        assert resp.status_code == 404

    def test_400_quando_repo_levanta_value_error(self, client):
        tc, repo = client
        repo.update_structure.side_effect = ValueError("invalid status")
        resp = tc.patch("/structures/1", json={"notes": "x"})
        assert resp.status_code == 400

    def test_422_status_invalido(self, client):
        """Status fora de {active, archived} deve ser rejeitado pelo schema."""
        tc, _ = client
        resp = tc.patch("/structures/1", json={"status": "deletado"})
        assert resp.status_code == 422

    def test_422_name_vazio(self, client):
        tc, _ = client
        resp = tc.patch("/structures/1", json={"name": ""})
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# DELETE /structures/{id}
# ---------------------------------------------------------------------------

class TestArchiveStructure:
    """Testes do endpoint DELETE /structures/{id} (soft-delete / archive)."""

    def test_retorna_204(self, client):
        tc, _ = client
        resp = tc.delete("/structures/1")
        assert resp.status_code == 204

    def test_sem_body_na_resposta_204(self, client):
        tc, _ = client
        resp = tc.delete("/structures/1")
        assert resp.content == b""

    def test_repo_archive_chamado_com_id_correto(self, client):
        tc, repo = client
        tc.delete("/structures/1")
        repo.archive_structure.assert_called_once_with(1)

    def test_repo_archive_chamado_exatamente_uma_vez(self, client):
        tc, repo = client
        tc.delete("/structures/1")
        assert repo.archive_structure.call_count == 1

    def test_repo_get_chamado_antes_do_archive(self, client):
        """Controller deve verificar existência antes de arquivar."""
        tc, repo = client
        tc.delete("/structures/1")
        repo.get_structure.assert_called_once_with(1)

    def test_404_quando_nao_encontrado(self, client):
        tc, repo = client
        repo.get_structure.return_value = None
        resp = tc.delete("/structures/999")
        assert resp.status_code == 404

    def test_404_detalhe_contem_id(self, client):
        tc, repo = client
        repo.get_structure.return_value = None
        resp = tc.delete("/structures/999")
        assert "999" in resp.json()["detail"]

    def test_404_nao_chama_archive_se_nao_encontrado(self, client):
        """Não deve chamar archive_structure se a estrutura não existe."""
        tc, repo = client
        repo.get_structure.return_value = None
        tc.delete("/structures/999")
        repo.archive_structure.assert_not_called()

    def test_400_quando_repo_levanta_value_error(self, client):
        tc, repo = client
        repo.archive_structure.side_effect = ValueError("já arquivada")
        resp = tc.delete("/structures/1")
        assert resp.status_code == 400

    def test_400_mensagem_propagada(self, client):
        tc, repo = client
        repo.archive_structure.side_effect = ValueError("já arquivada")
        resp = tc.delete("/structures/1")
        assert "já arquivada" in resp.json()["detail"]


# ---------------------------------------------------------------------------
# Testes de schema / contrato de resposta
# ---------------------------------------------------------------------------

class TestResponseSchema:
    """Verifica integridade dos schemas de resposta (campos e tipos)."""

    def test_create_response_tem_structure_id_inteiro(self, client):
        tc, _ = client
        resp = tc.post("/structures", json={
            "name": "Schema Test",
            "underlying_asset": "PETR4",
        })
        assert isinstance(resp.json()["structure_id"], int)

    def test_list_response_underlying_asset_em_maiusculas(self, client):
        """underlying_asset deve ser armazenado em uppercase (normalização do repo)."""
        tc, _ = client
        resp = tc.get("/structures")
        assert resp.json()[0]["underlying_asset"] == "PETR4"

    def test_detail_alias_legacy_aba_presente(self, client):
        tc, _ = client
        resp = tc.get("/structures/1")
        assert resp.json()["alias_legacy_aba"] == "PETR4_TRAVA"

    def test_detail_status_e_string(self, client):
        tc, _ = client
        resp = tc.get("/structures/1")
        assert isinstance(resp.json()["status"], str)

    def test_detail_status_valor_valido(self, client):
        tc, _ = client
        resp = tc.get("/structures/1")
        assert resp.json()["status"] in ("active", "archived")

    def test_detail_leg_strike_e_float(self, client):
        tc, _ = client
        resp = tc.get("/structures/1")
        leg = resp.json()["legs"][0]
        assert isinstance(leg["strike"], float)

    def test_detail_leg_position_side_valido(self, client):
        tc, _ = client
        resp = tc.get("/structures/1")
        leg = resp.json()["legs"][0]
        assert leg["position_side"] in ("COMPRADO", "VENDIDO")

    def test_detail_leg_option_type_valido(self, client):
        tc, _ = client
        resp = tc.get("/structures/1")
        leg = resp.json()["legs"][0]
        assert leg["option_type"] in ("CALL", "PUT")
