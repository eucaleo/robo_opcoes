# tests/test_regression_aba_compat.py
import pytest
from tests.paths import DB_PATH, PROJECT_ROOT
from UI.models.ui_data import UIDataModel


@pytest.fixture(scope="module")
def model():
    assert DB_PATH.exists(), (
        f"\n\nBanco não encontrado!\n"
        f"  Esperado     : {DB_PATH}\n"
        f"  PROJECT_ROOT : {PROJECT_ROOT}\n"
    )
    m = UIDataModel(derived_db_path=str(DB_PATH))
    m.refresh()
    return m


# ──────────────────────────────────────────────
# Smoke
# ──────────────────────────────────────────────

def test_db_existe():
    assert DB_PATH.exists(), f"Banco não encontrado: {DB_PATH}"


# ──────────────────────────────────────────────
# APIs legadas ainda existem
# ──────────────────────────────────────────────

def test_get_abas_existe(model):
    assert hasattr(model, "get_abas"), "get_abas() sumiu — quebraria código legado"


def test_get_abas_callable(model):
    assert callable(model.get_abas), "get_abas() não é callable"


def test_get_abas_retorna_lista(model):
    result = model.get_abas()
    assert isinstance(result, list), (
        f"get_abas() deve retornar list, retornou {type(result)}"
    )


def test_get_structures_existe(model):
    assert hasattr(model, "get_structures"), "get_structures() não encontrado"


def test_get_structures_callable(model):
    assert callable(model.get_structures), "get_structures() não é callable"


# ──────────────────────────────────────────────
# Coexistência de 'aba' e 'structure_id'
# ──────────────────────────────────────────────

def test_decisions_tem_ambos_campos(model):
    decisions = model.get_decisions()
    assert len(decisions) > 0, "Sem decisões para testar regressão"
    for d in decisions:
        assert "aba" in d, f"'aba' desapareceu: {d}"
        assert "structure_id" in d, f"'structure_id' não adicionado: {d}"


def test_aba_e_structure_id_identicos(model):
    """
    patch_3a: structure_id e int canonico; aba e ticker legado (ex: 'SBSP3').
    Nao sao mais identicos — esse e o comportamento correto apos o patch_34.
    Verificamos apenas que ambos existem e sao nao-nulos.
    """
    decisions = model.get_decisions()
    for d in decisions:
        assert d["aba"] is not None, f"'aba' nao pode ser None: {d}"
        assert d["structure_id"] is not None, f"'structure_id' nao pode ser None: {d}"
        assert isinstance(d["structure_id"], int), (
            f"structure_id deve ser int, recebido {type(d['structure_id'])}: {d}"
        )
        assert isinstance(d["aba"], str), (
            f"aba deve ser str (ticker), recebido {type(d['aba'])}: {d}"
        )


# ──────────────────────────────────────────────
# Filtros legados não quebram
# ──────────────────────────────────────────────

def test_filtro_aba_nao_quebra(model):
    decisions = model.get_decisions()
    if not decisions:
        pytest.skip("Sem decisões para testar filtro")
    sid = decisions[0]["aba"]
    try:
        result = model.get_decisions(filters={"aba": sid})
        assert isinstance(result, list)
    except Exception as e:
        pytest.fail(f"Filtro 'aba' lançou exceção: {e}")


def test_filtro_structure_id_nao_quebra(model):
    decisions = model.get_decisions()
    if not decisions:
        pytest.skip("Sem decisões para testar filtro")
    sid = decisions[0]["structure_id"]
    try:
        result = model.get_decisions(filters={"structure_id": sid})
        assert isinstance(result, list)
    except Exception as e:
        pytest.fail(f"Filtro 'structure_id' lançou exceção: {e}")


# ──────────────────────────────────────────────
# get_payoff_curve_info() não quebra
# ──────────────────────────────────────────────

def test_payoff_curve_info_nao_quebra_com_structure_id(model):
    decisions = model.get_decisions()
    if not decisions:
        pytest.skip("Sem decisões")
    d0 = decisions[0]
    try:
        pts, info = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"])
        assert pts is not None
        assert info is not None
    except Exception as e:
        pytest.fail(f"get_payoff_curve_info() quebrou com structure_id: {e}")


def test_payoff_curve_info_nao_quebra_com_aba(model):
    """
    patch_3a: get_payoff_curve_info() recebe structure_id (int) — nao mais aba ticker.
    Teste atualizado para usar structure_id canonico.
    Aba como chave de lookup foi removida no patch_34.
    """
    decisions = model.get_decisions()
    if not decisions:
        pytest.skip("Sem decisoes")
    d0 = decisions[0]
    try:
        pts, info = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"])
        assert pts is not None
        assert info is not None
    except Exception as e:
        pytest.fail(f"get_payoff_curve_info() quebrou com structure_id (canonico): {e}")
