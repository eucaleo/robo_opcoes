# tests/test_ui_data_migration.py
import pytest
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DB_PATH = PROJECT_ROOT / "dados" / "derived.db"
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


@pytest.fixture(scope="module")
def decisions(model):
    return model.get_decisions()


@pytest.fixture(scope="module")
def structures(model):
    return model.get_structures()




@pytest.fixture(scope="module")
def non_empty_structures(structures):
    if not structures:
        pytest.skip("Sem estruturas no banco de migração")
    return structures


@pytest.fixture(scope="module")
def non_empty_decisions(decisions):
    if not decisions:
        pytest.skip("Sem decisões no banco de migração")
    return decisions

# 
# Sanidade -- banco acessível
# 

def test_db_existe():
    assert DB_PATH.exists(), f"Banco não encontrado: {DB_PATH}"


def test_db_project_root_correto():
    assert (PROJECT_ROOT / "dados").exists(), (
        f"Pasta 'dados/' não encontrada em: {PROJECT_ROOT}"
    )


# 
# Nível 1 -- get_structures / get_abas
# 

def test_get_structures_retorna_lista(structures):
    assert isinstance(structures, list), "get_structures() deve retornar lista"


def test_get_structures_nao_vazia(non_empty_structures):
    assert len(non_empty_structures) > 0, "Deve haver ao menos uma estrutura cadastrada"


def test_get_abas_alias_de_get_structures(model, structures):
    assert hasattr(model, "get_abas"), "get_abas() deve existir para continuidade operacional"
    assert callable(model.get_abas), "get_abas() deve ser callable"
    assert model.get_abas() == structures, (
        "get_abas() deve retornar o mesmo que get_structures()"
    )


# 
# Nível 2 -- get_decisions() com structure_id
# 

def test_decisions_nao_vazia(non_empty_decisions):
    assert len(non_empty_decisions) > 0, "Deve haver ao menos uma decisão no banco"


def test_decisions_tem_structure_id(decisions):
    for d in decisions:
        assert "structure_id" in d, f"Faltou 'structure_id' no dict: {d}"


def test_decisions_tem_aba(decisions):
    for d in decisions:
        assert "aba" in d, f"Campo 'aba' desapareceu do dict: {d}"


def test_structure_id_igual_a_aba(decisions):
    """
    migração structure_id: structure_id (int) e aba (ticker str) sao campos distintos.
    Verificamos que structure_id e int positivo e aba e str nao-vazia.
    """
    for d in decisions:
        assert isinstance(d["structure_id"], int), (
            f"structure_id deve ser int: {d['structure_id']!r}"
        )
        assert d["structure_id"] > 0, (
            f"structure_id deve ser positivo: {d['structure_id']}"
        )
        assert isinstance(d["aba"], str) and d["aba"].strip(), (
            f"aba deve ser str nao-vazia: {d['aba']!r}"
        )


def test_decisions_tem_timestamp(decisions):
    for d in decisions:
        assert "timestamp" in d, f"Faltou 'timestamp' no dict: {d}"
        assert d["timestamp"], "timestamp não pode ser vazio ou None"


# 
# Nível 3 -- Filtros
# 

def test_filtro_por_structure_id(model, non_empty_structures):
    """
    migração structure_id: structures retorna lista de str numericas; converte para int
    antes de comparar com d["structure_id"] que e sempre int canonico.
    """
    sid_str = non_empty_structures[0]          # ex: '36'
    sid_int = int(sid_str)           # 36
    filtered = model.get_decisions(filters={"structure_id": sid_str})
    assert isinstance(filtered, list), "Filtro deve retornar lista"
    assert len(filtered) > 0, f"Filtro structure_id='{sid_str}' retornou vazio"
    for d in filtered:
        assert d["structure_id"] == sid_int, (
            f"Decisao filtrada com structure_id errado: {d['structure_id']!r} != {sid_int}"
        )


def test_filtro_por_aba_continuidade(model, decisions):
    """
    migração structure_id: filtro por 'aba' usa ticker (ex: 'SBSP3'), nao id numerico.
    Verificamos que filtrar por aba de uma decisao real retorna >= 1 resultado
    e que todos os resultados tem a aba correspondente.
    """
    if not decisions:
        pytest.skip("Sem decisoes para testar filtro por aba")
    aba_real = decisions[0]["aba"]        # ex: 'SBSP3'
    filtered_aba = model.get_decisions(filters={"aba": aba_real})
    assert isinstance(filtered_aba, list), "Filtro aba deve retornar lista"
    assert len(filtered_aba) >= 1, (
        f"Filtro aba='{aba_real}' retornou vazio"
    )
    for d in filtered_aba:
        assert d["aba"] == aba_real, (
            f"Decisao com aba errada: esperado '{aba_real}', recebido '{d['aba']}'"
        )


# 
# Nível 4 -- get_payoff_curve_info()
# 

def test_payoff_curve_info_retorna_dados(model, non_empty_decisions):
    d0 = non_empty_decisions[0]
    pts, info = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"])
    assert isinstance(pts, list), "Pontos do payoff devem ser uma lista"
    assert isinstance(info, dict), "info do payoff deve ser dict"


def test_payoff_curve_info_tem_structure_id(model, non_empty_decisions):
    d0 = non_empty_decisions[0]
    _, info = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"])
    assert "structure_id" in info, "info do payoff deve conter 'structure_id'"


def test_payoff_curve_info_aba_continuidade(model, non_empty_decisions):
    d0 = non_empty_decisions[0]
    _, info = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"])
    assert "aba" in info, "info do payoff deve ainda conter 'aba' (continuidade)"
    assert info["aba"] == d0["structure_id"], (
        f"info['aba']='{info['aba']}' != structure_id='{d0['structure_id']}'"
    )


def test_payoff_curve_info_pontos_validos(model, non_empty_decisions):
    d0 = non_empty_decisions[0]
    pts, _ = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"])
    for pt in pts:
        assert isinstance(pt, dict), f"Ponto deve ser dict: {pt}"
        assert "spot" in pt, f"Faltou chave 'spot' no ponto: {pt}"
        assert "pl" in pt, f"Faltou chave 'pl' no ponto: {pt}"
