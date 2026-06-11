# Testes dos endpoints de legs de estruturas
"""
PATCH_63 — Testes dos endpoints de legs na API de estruturas.

Cobre:
    POST   /structures/{id}/legs           — add_leg
    PUT    /structures/{id}/legs           — replace_legs (atômico)
    DELETE /structures/{id}/legs/{leg_id}  — remove_leg

    Fix validado: leg_order >= 0 (era >= 1, rejeitava leg_order=0).
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# ---------------------------------------------------------------------------
# Payloads reutilizáveis
# ---------------------------------------------------------------------------

FAKE_LEG_PAYLOAD = {
    "position_side":   "LONG",
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

FAKE_STRUCTURE = {
    "id":                1,
    "name":              "Bull Call Spread",
    "underlying_asset":  "PETR4",
    "alias_legacy_aba":  None,
    "status":            "active",
    "notes":             None,
    "created_at":        "2026-01-01T00:00:00+00:00",
    "updated_at":        "2026-01-01T00:00:00+00:00",
    "legs":              [],
}


# ---------------------------------------------------------------------------
# Fixture base — mock_repo
# ---------------------------------------------------------------------------

@pytest.fixture()
def mock_repo():
    repo = MagicMock()
    repo.get_structure.return_value = FAKE_STRUCTURE
    repo.add_leg.return_value = 10
    repo.replace_legs.return_value = None
    return repo


# ---------------------------------------------------------------------------
# Fixture de client — injeta mock_repo no controller
# ---------------------------------------------------------------------------

@pytest.fixture()
def client_legs(mock_repo):
    """TestClient com repositório completamente mockado."""
    with patch("api.structures_controller._repo", mock_repo):
        from api.structures_controller import router

        app = FastAPI()
        app.include_router(router)
        yield TestClient(app), mock_repo


# ---------------------------------------------------------------------------
# POST /structures/{id}/legs
# ---------------------------------------------------------------------------

class TestAddLeg:
    """12 casos para o endpoint de adição de perna."""

    def test_add_leg_retorna_201(self, client_legs):
        tc, _ = client_legs
        resp = tc.post("/structures/1/legs", json=FAKE_LEG_PAYLOAD)
        assert resp.status_code == 201

    def test_add_leg_retorna_leg_id(self, client_legs):
        tc, _ = client_legs
        resp = tc.post("/structures/1/legs", json=FAKE_LEG_PAYLOAD)
        assert resp.json() == {"leg_id": 10}

    def test_add_leg_repo_chamado_com_structure_id_correto(self, client_legs):
        tc, repo = client_legs
        tc.post("/structures/1/legs", json=FAKE_LEG_PAYLOAD)
        args = repo.add_leg.call_args[0]
        assert args[0] == 1

    def test_add_leg_repo_chamado_com_payload_correto(self, client_legs):
        tc, repo = client_legs
        tc.post("/structures/1/legs", json=FAKE_LEG_PAYLOAD)
        args = repo.add_leg.call_args[0]
        assert args[1]["strike"] == 38.0
        assert args[1]["position_side"] == "LONG"

    def test_add_leg_404_estrutura_inexistente(self, client_legs):
        tc, repo = client_legs
        repo.get_structure.return_value = None
        resp = tc.post("/structures/999/legs", json=FAKE_LEG_PAYLOAD)
        assert resp.status_code == 404

    def test_add_leg_400_quando_repo_levanta_value_error(self, client_legs):
        tc, repo = client_legs
        repo.add_leg.side_effect = ValueError("leg inválida")
        resp = tc.post("/structures/1/legs", json=FAKE_LEG_PAYLOAD)
        assert resp.status_code == 400
        assert "leg inválida" in resp.json()["detail"]

    def test_add_leg_422_position_side_invalido(self, client_legs):
        tc, _ = client_legs
        payload = {**FAKE_LEG_PAYLOAD, "position_side": "BUY"}
        resp = tc.post("/structures/1/legs", json=payload)
        assert resp.status_code == 422

    def test_add_leg_422_option_type_invalido(self, client_legs):
        tc, _ = client_legs
        payload = {**FAKE_LEG_PAYLOAD, "option_type": "FUTURES"}
        resp = tc.post("/structures/1/legs", json=payload)
        assert resp.status_code == 422

    def test_add_leg_422_strike_zero(self, client_legs):
        tc, _ = client_legs
        payload = {**FAKE_LEG_PAYLOAD, "strike": 0}
        resp = tc.post("/structures/1/legs", json=payload)
        assert resp.status_code == 422

    def test_add_leg_422_quantity_zero(self, client_legs):
        tc, _ = client_legs
        payload = {**FAKE_LEG_PAYLOAD, "quantity": 0}
        resp = tc.post("/structures/1/legs", json=payload)
        assert resp.status_code == 422

    def test_add_leg_aceita_leg_order_zero(self, client_legs):
        """patch_63 FIX principal: leg_order=0 deve ser aceito."""
        tc, _ = client_legs
        payload = {**FAKE_LEG_PAYLOAD, "leg_order": 0}
        resp = tc.post("/structures/1/legs", json=payload)
        assert resp.status_code == 201

    def test_add_leg_422_leg_order_negativo(self, client_legs):
        tc, _ = client_legs
        payload = {**FAKE_LEG_PAYLOAD, "leg_order": -1}
        resp = tc.post("/structures/1/legs", json=payload)
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# PUT /structures/{id}/legs
# ---------------------------------------------------------------------------

class TestReplaceLegs:
    """10 casos para o endpoint de substituição atômica de pernas."""

    def test_replace_legs_retorna_204(self, client_legs):
        tc, _ = client_legs
        resp = tc.put("/structures/1/legs", json=REPLACE_LEGS_PAYLOAD)
        assert resp.status_code == 204

    def test_replace_legs_sem_body_na_resposta(self, client_legs):
        tc, _ = client_legs
        resp = tc.put("/structures/1/legs", json=REPLACE_LEGS_PAYLOAD)
        assert resp.content == b""

    def test_replace_legs_repo_chamado_com_structure_id_correto(self, client_legs):
        tc, repo = client_legs
        tc.put("/structures/1/legs", json=REPLACE_LEGS_PAYLOAD)
        args = repo.replace_legs.call_args[0]
        assert args[0] == 1

    def test_replace_legs_repo_recebe_lista_com_um_item(self, client_legs):
        tc, repo = client_legs
        tc.put("/structures/1/legs", json=REPLACE_LEGS_PAYLOAD)
        args = repo.replace_legs.call_args[0]
        assert len(args[1]) == 1

    def test_replace_legs_repo_recebe_dados_corretos(self, client_legs):
        tc, repo = client_legs
        tc.put("/structures/1/legs", json=REPLACE_LEGS_PAYLOAD)
        leg = repo.replace_legs.call_args[0][1][0]
        assert leg["strike"] == 38.0
        assert leg["option_type"] == "CALL"

    def test_replace_legs_404_estrutura_inexistente(self, client_legs):
        tc, repo = client_legs
        repo.get_structure.return_value = None
        resp = tc.put("/structures/999/legs", json=REPLACE_LEGS_PAYLOAD)
        assert resp.status_code == 404

    def test_replace_legs_400_quando_repo_levanta_value_error(self, client_legs):
        tc, repo = client_legs
        repo.replace_legs.side_effect = ValueError("leg inválida no replace")
        resp = tc.put("/structures/1/legs", json=REPLACE_LEGS_PAYLOAD)
        assert resp.status_code == 400

    def test_replace_legs_422_lista_vazia(self, client_legs):
        """Lista vazia viola min_length=1 do schema ReplaceLegRequest."""
        tc, _ = client_legs
        resp = tc.put("/structures/1/legs", json={"legs": []})
        assert resp.status_code == 422

    def test_replace_legs_aceita_leg_order_zero(self, client_legs):
        """patch_63 FIX: leg_order=0 deve ser aceito no replace também."""
        tc, _ = client_legs
        payload = {"legs": [{**FAKE_LEG_PAYLOAD, "leg_order": 0}]}
        resp = tc.put("/structures/1/legs", json=payload)
        assert resp.status_code == 204

    def test_replace_legs_aceita_multiplas_legs(self, client_legs):
        """Garante que lista com N > 1 pernas é aceita."""
        tc, repo = client_legs
        payload = {
            "legs": [
                {**FAKE_LEG_PAYLOAD, "leg_order": 0},
                {**FAKE_LEG_PAYLOAD, "leg_order": 1, "option_type": "PUT",
                 "position_side": "SHORT"},
            ]
        }
        resp = tc.put("/structures/1/legs", json=payload)
        assert resp.status_code == 204
        args = repo.replace_legs.call_args[0]
        assert len(args[1]) == 2


# ---------------------------------------------------------------------------
# DELETE /structures/{id}/legs/{leg_id}
# ---------------------------------------------------------------------------

class TestRemoveLeg:
    """4 casos para o endpoint de remoção de perna individual."""

    def _mock_conn_with_leg(self, repo, leg_found: bool):
        """Helper: configura mock_conn simulando leg existente ou não."""
        mock_conn = MagicMock()
        fetchone_return = {"id": 10} if leg_found else None
        mock_conn.execute.return_value.fetchone.return_value = fetchone_return
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        repo._connect = MagicMock(return_value=mock_conn)
        return mock_conn

    def test_remove_leg_retorna_204(self, client_legs):
        tc, repo = client_legs
        self._mock_conn_with_leg(repo, leg_found=True)
        resp = tc.delete("/structures/1/legs/10")
        assert resp.status_code == 204

    def test_remove_leg_404_estrutura_inexistente(self, client_legs):
        tc, repo = client_legs
        repo.get_structure.return_value = None
        resp = tc.delete("/structures/999/legs/10")
        assert resp.status_code == 404

    def test_remove_leg_404_leg_inexistente(self, client_legs):
        tc, repo = client_legs
        self._mock_conn_with_leg(repo, leg_found=False)
        resp = tc.delete("/structures/1/legs/999")
        assert resp.status_code == 404

    def test_remove_leg_404_detalhe_contem_leg_id(self, client_legs):
        tc, repo = client_legs
        self._mock_conn_with_leg(repo, leg_found=False)
        resp = tc.delete("/structures/1/legs/999")
        assert "999" in resp.json()["detail"]
