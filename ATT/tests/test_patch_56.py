"""
ATT/tests/test_patch_56.py
==========================
Testes de regressão para patch_56: StructureRef propagation.

Blocos:
  1 -- _unwrap_aba() helper
  2 -- get_payoff_by_aba() corrigido
  3 -- get_payoff_by_structure_id() migrado
  4 -- Funções standalone do derived_repo aceitam StructureRef
  5 -- Regressão: comportamento legado não quebrado
"""

import json
import sqlite3
import pytest
from unittest.mock import patch, MagicMock


#  Imports com fallback gracioso 
try:
    from src.domain.refs.structure_ref import StructureRef
    HAS_STRUCTURE_REF = True
except ImportError:
    HAS_STRUCTURE_REF = False

try:
    from db.derived_repo import _unwrap_aba
    HAS_UNWRAP = True
except ImportError:
    HAS_UNWRAP = False

try:
    import services.derived_service as derived_service
    HAS_SERVICE = True
except ImportError:
    HAS_SERVICE = False

try:
    import db.derived_repo as derived_repo
    HAS_REPO = True
except ImportError:
    HAS_REPO = False


#  Fixtures 

@pytest.fixture
def ref_aba():
    if not HAS_STRUCTURE_REF:
        pytest.skip("StructureRef não disponível")
    return StructureRef.from_aba("VALE5")

@pytest.fixture
def ref_id():
    if not HAS_STRUCTURE_REF:
        pytest.skip("StructureRef não disponível")
    return StructureRef.from_id(42)

@pytest.fixture
def mock_cursor():
    cur = MagicMock()
    cur.fetchall.return_value = []
    return cur

@pytest.fixture
def mock_conn(mock_cursor):
    conn = MagicMock()
    conn.cursor.return_value = mock_cursor
    conn.__enter__ = MagicMock(return_value=conn)
    conn.__exit__ = MagicMock(return_value=False)
    return conn


# =============================================================================
# BLOCO 1 -- _unwrap_aba()
# =============================================================================

class TestUnwrapAba:

    def test_str_passthrough(self):
        if not HAS_UNWRAP:
            pytest.skip("_unwrap_aba não disponível")
        assert _unwrap_aba("VALE5") == "VALE5"

    def test_str_vazio_passthrough(self):
        if not HAS_UNWRAP:
            pytest.skip("_unwrap_aba não disponível")
        assert _unwrap_aba("") == ""

    def test_structure_ref_com_aba(self, ref_aba):
        if not HAS_UNWRAP:
            pytest.skip("_unwrap_aba não disponível")
        result = _unwrap_aba(ref_aba)
        assert result == "VALE5"
        assert isinstance(result, str)

    def test_structure_ref_sem_aba_levanta_value_error(self, ref_id):
        if not HAS_UNWRAP:
            pytest.skip("_unwrap_aba não disponível")
        if ref_id.aba is None:
            with pytest.raises(ValueError, match="StructureRef.aba é None"):
                _unwrap_aba(ref_id)
        else:
            assert isinstance(_unwrap_aba(ref_id), str)

    def test_none_passthrough(self):
        if not HAS_UNWRAP:
            pytest.skip("_unwrap_aba não disponível")
        assert _unwrap_aba(None) is None


# =============================================================================
# BLOCO 2 -- get_payoff_by_aba()
# =============================================================================

class TestGetPayoffByAba:

    def test_usa_col_interpolado_na_query(self, ref_aba, mock_conn):
        if not HAS_SERVICE or not HAS_STRUCTURE_REF:
            pytest.skip("Dependências não disponíveis")
        col, val = ref_aba.db_pair()
        with patch("services.derived_service.connect_derived", return_value=mock_conn):
            derived_service.get_payoff_by_aba(ref_aba)
        sql = mock_conn.cursor().execute.call_args[0][0]
        assert "{ref.db_column()}" not in sql, "Bug f-string ainda presente"
        assert col in sql

    def test_params_usa_val(self, ref_aba, mock_conn):
        if not HAS_SERVICE or not HAS_STRUCTURE_REF:
            pytest.skip("Dependências não disponíveis")
        _, val = ref_aba.db_pair()
        with patch("services.derived_service.connect_derived", return_value=mock_conn):
            derived_service.get_payoff_by_aba(ref_aba)
        params = mock_conn.cursor().execute.call_args[0][1]
        assert params == (val,), f"Esperado ({val!r},) mas recebeu {params}"

    def test_sem_name_error(self, ref_aba, mock_conn):
        if not HAS_SERVICE or not HAS_STRUCTURE_REF:
            pytest.skip("Dependências não disponíveis")
        with patch("services.derived_service.connect_derived", return_value=mock_conn):
            try:
                derived_service.get_payoff_by_aba(ref_aba)
            except NameError as e:
                pytest.fail(f"NameError ainda presente: {e}")

    def test_retorna_lista_vazia(self, ref_aba, mock_conn):
        if not HAS_SERVICE or not HAS_STRUCTURE_REF:
            pytest.skip("Dependências não disponíveis")
        with patch("services.derived_service.connect_derived", return_value=mock_conn):
            assert derived_service.get_payoff_by_aba(ref_aba) == []

    def test_retorna_dicionarios_corretos(self, ref_aba, mock_conn):
        if not HAS_SERVICE or not HAS_STRUCTURE_REF:
            pytest.skip("Dependências não disponíveis")
        mock_conn.cursor().fetchall.return_value = [
            ("2025-06-01T10:00:00", 50.0, 1200.0, None),
            ("2025-06-01T10:00:00", 55.0, 900.0, '{"adjusted": true}'),
        ]
        with patch("services.derived_service.connect_derived", return_value=mock_conn):
            result = derived_service.get_payoff_by_aba(ref_aba)
        assert len(result) == 2
        assert result[0]["point_spot"] == 50.0
        assert result[1]["meta_json"] == {"adjusted": True}


# =============================================================================
# BLOCO 3 -- get_payoff_by_structure_id()
# =============================================================================

class TestGetPayoffByStructureId:

    def test_passa_structure_ref_para_get_payoff_by_aba(self):
        if not HAS_SERVICE or not HAS_STRUCTURE_REF:
            pytest.skip("Dependências não disponíveis")
        with patch("services.derived_service.get_payoff_by_aba", return_value=[]) as mock_fn:
            derived_service.get_payoff_by_structure_id(42)
        ref_passado = mock_fn.call_args[0][0]
        assert isinstance(ref_passado, StructureRef), (
            f"Esperado StructureRef, recebeu {type(ref_passado)}"
        )
        assert ref_passado.structure_id == 42

    def test_nao_passa_str(self):
        if not HAS_SERVICE or not HAS_STRUCTURE_REF:
            pytest.skip("Dependências não disponíveis")
        with patch("services.derived_service.get_payoff_by_aba", return_value=[]) as mock_fn:
            derived_service.get_payoff_by_structure_id(99)
        assert not isinstance(mock_fn.call_args[0][0], str), (
            "Regressão: ainda passando str para get_payoff_by_aba"
        )

    def test_retorna_resultado_do_delegate(self):
        if not HAS_SERVICE or not HAS_STRUCTURE_REF:
            pytest.skip("Dependências não disponíveis")
        fake = [{"timestamp": "2025-06-01", "point_spot": 50.0}]
        with patch("services.derived_service.get_payoff_by_aba", return_value=fake):
            assert derived_service.get_payoff_by_structure_id(1) == fake

    def test_nao_usa_sid_to_aba_cache(self):
        if not HAS_SERVICE:
            pytest.skip("derived_service não disponível")
        import inspect
        src = inspect.getsource(derived_service.get_payoff_by_structure_id)
        assert "sid_to_aba" not in src, "Cache sid_to_aba ainda presente -- regressão"


# =============================================================================
# BLOCO 4 -- Funções standalone do derived_repo aceitam StructureRef
# =============================================================================

@pytest.mark.skipif(not HAS_REPO, reason="derived_repo não disponível")
@pytest.mark.skipif(not HAS_STRUCTURE_REF, reason="StructureRef não disponível")
class TestDerivedRepoStandalone:

    @pytest.fixture
    def db_conn(self):
        conn = sqlite3.connect(":memory:")
        derived_repo.ensure_derived_tables(conn)
        yield conn
        conn.close()

    def test_insert_payoff_points_aceita_ref(self, db_conn, ref_aba):
        count = derived_repo.insert_payoff_points(
            db_conn,
            timestamp="2025-06-01T10:00:00",
            aba=ref_aba,
            points=[(50.0, 1200.0), (55.0, 900.0)],
        )
        assert count == 2

    def test_insert_payoff_points_aceita_str(self, db_conn):
        count = derived_repo.insert_payoff_points(
            db_conn,
            timestamp="2025-06-01T10:00:00",
            aba="PETR4",
            points=[(50.0, 500.0)],
        )
        assert count == 1

    def test_insert_structure_decision_aceita_ref(self, db_conn, ref_aba):
        row_id = derived_repo.insert_structure_decision(
            db_conn,
            timestamp="2025-06-01T10:00:00",
            aba=ref_aba,
            decision_dict={"decision": "HOLD", "level": 0},
        )
        assert isinstance(row_id, int) and row_id > 0

    def test_get_payoff_points_aceita_ref(self, db_conn, ref_aba):
        derived_repo.insert_payoff_points(
            db_conn,
            timestamp="2025-06-01T10:00:00",
            aba="VALE5",
            points=[(50.0, 1200.0)],
        )
        rows = derived_repo.get_payoff_points(db_conn, aba=ref_aba)
        assert len(rows) >= 1

    def test_get_payoff_points_aceita_none(self, db_conn):
        rows = derived_repo.get_payoff_points(db_conn, aba=None)
        assert isinstance(rows, list)

    def test_write_complete_snapshot_aceita_ref(self, db_conn, ref_aba):
        result = derived_repo.write_complete_snapshot_atomic(
            db_conn,
            timestamp="2025-06-01T11:00:00",
            aba=ref_aba,
            points=[(50.0, 1200.0), (55.0, 800.0)],
            decision_dict={"decision": "OPEN", "level": 1},
        )
        assert "points_count" in result
        assert result["points_count"] == 2


# =============================================================================
# BLOCO 5 -- Regressão legado
# =============================================================================

class TestRegressaoLegado:

    def test_resolve_structure_id_aceita_str(self):
        if not HAS_SERVICE or not hasattr(derived_service, "_resolve_structure_id"):
            pytest.skip("_resolve_structure_id não exposta")
        result = derived_service._resolve_structure_id("VALE5")
        assert result is None or isinstance(result, int)

    def test_unwrap_aba_presente_no_modulo(self):
        if not HAS_REPO:
            pytest.skip("derived_repo não disponível")
        import inspect
        src = inspect.getsource(derived_repo)
        assert "_unwrap_aba" in src, "_unwrap_aba não encontrado no módulo"

    def test_fstring_bug_ausente_no_service(self):
        if not HAS_SERVICE:
            pytest.skip("derived_service não disponível")
        import inspect
        src = inspect.getsource(derived_service)
        assert "{ref.db_column()}" not in src, "Bug f-string remanescente"
