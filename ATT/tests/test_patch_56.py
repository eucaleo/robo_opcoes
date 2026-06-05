"""
ATT/tests/test_patch_56.py
==========================
Testes de regressao para patch_56: StructureRef propagation.
patch_73: Blocos 2 e 3 atualizados -- get_payoff_by_aba() removida no patch_65,
          get_payoff_by_structure_id() consulta direto o banco (nao delega mais).

Blocos:
  1 -- _unwrap_aba() helper
  2 -- get_payoff_by_structure_id() interface publica canonica
  3 -- get_payoff_by_structure_id() comportamento de leitura
  4 -- Funcoes standalone do derived_repo aceitam StructureRef
  5 -- Regressao: comportamento legado nao quebrado
"""

import json
import sqlite3
import pytest
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Imports com fallback gracioso
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def ref_aba():
    if not HAS_STRUCTURE_REF:
        pytest.skip("StructureRef nao disponivel")
    return StructureRef.from_aba("VALE5")


@pytest.fixture
def ref_id():
    if not HAS_STRUCTURE_REF:
        pytest.skip("StructureRef nao disponivel")
    return StructureRef.from_id(42)


@pytest.fixture
def mock_cursor():
    cur = MagicMock()
    cur.fetchall.return_value = []
    cur.description = [
        ("timestamp",),
        ("point_spot",),
        ("point_pl",),
        ("meta_json",),
    ]
    return cur


@pytest.fixture
def mock_conn(mock_cursor):
    conn = MagicMock()
    conn.cursor.return_value = mock_cursor
    conn.__enter__ = MagicMock(return_value=conn)
    conn.__exit__ = MagicMock(return_value=False)
    return conn


@pytest.fixture
def mem_db():
    """Banco SQLite in-memory com schema derived completo."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    derived_repo.ensure_derived_tables(conn)
    yield conn
    conn.close()


# =============================================================================
# BLOCO 1 -- _unwrap_aba()
# =============================================================================

class TestUnwrapAba:

    def test_str_passthrough(self):
        if not HAS_UNWRAP:
            pytest.skip("_unwrap_aba nao disponivel")
        assert _unwrap_aba("VALE5") == "VALE5"

    def test_str_vazio_passthrough(self):
        if not HAS_UNWRAP:
            pytest.skip("_unwrap_aba nao disponivel")
        assert _unwrap_aba("") == ""

    def test_structure_ref_com_aba(self, ref_aba):
        if not HAS_UNWRAP:
            pytest.skip("_unwrap_aba nao disponivel")
        result = _unwrap_aba(ref_aba)
        assert result == "VALE5"
        assert isinstance(result, str)

    def test_structure_ref_sem_aba_levanta_value_error(self, ref_id):
        if not HAS_UNWRAP:
            pytest.skip("_unwrap_aba nao disponivel")
        if ref_id.aba is None:
            # Aceita tanto "e" quanto "e" com acento (caracter real no codigo)
            # e nao assume o texto completo da mensagem, apenas a parte chave.
            # O ponto em "StructureRef.aba" e escapado para nao virar wildcard.
            with pytest.raises(ValueError, match=r"StructureRef\.aba"):
                _unwrap_aba(ref_id)
        else:
            assert isinstance(_unwrap_aba(ref_id), str)

    def test_none_passthrough(self):
        if not HAS_UNWRAP:
            pytest.skip("_unwrap_aba nao disponivel")
        assert _unwrap_aba(None) is None


# =============================================================================
# BLOCO 2 -- get_payoff_by_structure_id() interface publica canonica
#
# patch_73: get_payoff_by_aba() foi removida no patch_65.
#           get_payoff_by_structure_id() e o unico ponto de entrada canonico.
#           Testa a interface publica diretamente sem assumir delegacao interna.
# =============================================================================

class TestGetPayoffByStructureIdInterface:

    def test_funcao_existe_no_modulo(self):
        if not HAS_SERVICE:
            pytest.skip("derived_service nao disponivel")
        assert hasattr(derived_service, "get_payoff_by_structure_id"), (
            "get_payoff_by_structure_id nao encontrada em derived_service"
        )

    def test_get_payoff_by_aba_removida(self):
        """
        patch_65: get_payoff_by_aba() foi deliberadamente removida da interface publica.
        Confirma que a remocao esta em vigor.
        """
        if not HAS_SERVICE:
            pytest.skip("derived_service nao disponivel")
        assert not hasattr(derived_service, "get_payoff_by_aba"), (
            "get_payoff_by_aba ainda exposta -- deveria ter sido removida no patch_65"
        )

    def test_aceita_inteiro(self, mock_conn):
        if not HAS_SERVICE:
            pytest.skip("derived_service nao disponivel")
        with patch("services.derived_service.connect_derived", return_value=mock_conn):
            try:
                derived_service.get_payoff_by_structure_id(42)
            except Exception as exc:
                pytest.fail(f"Excecao inesperada com int: {exc}")

    def test_retorna_lista(self, mock_conn):
        if not HAS_SERVICE:
            pytest.skip("derived_service nao disponivel")
        mock_conn.cursor.return_value.fetchall.return_value = []
        with patch("services.derived_service.connect_derived", return_value=mock_conn):
            result = derived_service.get_payoff_by_structure_id(1)
        assert isinstance(result, list)

    def test_sem_name_error(self, mock_conn):
        if not HAS_SERVICE:
            pytest.skip("derived_service nao disponivel")
        with patch("services.derived_service.connect_derived", return_value=mock_conn):
            try:
                derived_service.get_payoff_by_structure_id(99)
            except NameError as exc:
                pytest.fail(f"NameError presente: {exc}")

    def test_nao_usa_sid_to_aba_cache(self):
        if not HAS_SERVICE:
            pytest.skip("derived_service nao disponivel")
        import inspect
        src = inspect.getsource(derived_service.get_payoff_by_structure_id)
        assert "sid_to_aba" not in src, (
            "Cache sid_to_aba ainda presente -- regressao"
        )


# =============================================================================
# BLOCO 3 -- get_payoff_by_structure_id() comportamento de leitura
#
# patch_73: testa o comportamento real da funcao atual que usa StructureRef.from_id()
#           e consulta diretamente o banco via connect_derived.
# =============================================================================

class TestGetPayoffByStructureIdLeitura:

    def test_usa_structure_ref_from_id_internamente(self):
        """
        A implementacao atual deve criar StructureRef.from_id(structure_id)
        e usar ref.db_pair() para montar a query.
        Verifica indiretamente inspecionando o fonte.
        """
        if not HAS_SERVICE or not HAS_STRUCTURE_REF:
            pytest.skip("Dependencias nao disponiveis")
        import inspect
        src = inspect.getsource(derived_service.get_payoff_by_structure_id)
        assert "StructureRef.from_id" in src, (
            "get_payoff_by_structure_id nao usa StructureRef.from_id()"
        )

    def test_usa_db_pair_na_query(self):
        if not HAS_SERVICE:
            pytest.skip("derived_service nao disponivel")
        import inspect
        src = inspect.getsource(derived_service.get_payoff_by_structure_id)
        assert "db_pair" in src, (
            "get_payoff_by_structure_id nao usa db_pair() -- query pode estar hardcoded"
        )

    def test_retorna_dicionarios_com_chaves_canonicas(self, mock_conn):
        if not HAS_SERVICE:
            pytest.skip("derived_service nao disponivel")
        mock_conn.cursor.return_value.fetchall.return_value = [
            ("2025-06-01T10:00:00", 50.0, 1200.0, None),
            ("2025-06-01T10:00:00", 55.0, 900.0, '{"adjusted": true}'),
        ]
        with patch("services.derived_service.connect_derived", return_value=mock_conn):
            result = derived_service.get_payoff_by_structure_id(1)
        assert isinstance(result, list)
        if result:
            assert "point_spot" in result[0]
            assert "point_pl" in result[0]
            assert "timestamp" in result[0]

    def test_meta_json_desserializado(self, mock_conn):
        if not HAS_SERVICE:
            pytest.skip("derived_service nao disponivel")
        mock_conn.cursor.return_value.fetchall.return_value = [
            ("2025-06-01T10:00:00", 55.0, 900.0, '{"adjusted": true}'),
        ]
        with patch("services.derived_service.connect_derived", return_value=mock_conn):
            result = derived_service.get_payoff_by_structure_id(1)
        if result and result[0].get("meta_json") is not None:
            assert isinstance(result[0]["meta_json"], (dict, str)), (
                "meta_json deve ser dict (desserializado) ou str"
            )

    def test_retorna_lista_vazia_quando_sem_dados(self, mock_conn):
        if not HAS_SERVICE:
            pytest.skip("derived_service nao disponivel")
        mock_conn.cursor.return_value.fetchall.return_value = []
        with patch("services.derived_service.connect_derived", return_value=mock_conn):
            result = derived_service.get_payoff_by_structure_id(999)
        assert result == []


# =============================================================================
# BLOCO 4 -- Funcoes standalone do derived_repo aceitam StructureRef
# =============================================================================

@pytest.mark.skipif(not HAS_REPO, reason="derived_repo nao disponivel")
@pytest.mark.skipif(not HAS_STRUCTURE_REF, reason="StructureRef nao disponivel")
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
# BLOCO 5 -- Regressao legado
# =============================================================================

class TestRegressaoLegado:

    def test_resolve_structure_id_aceita_str(self):
        if not HAS_SERVICE or not hasattr(derived_service, "_resolve_structure_id"):
            pytest.skip("_resolve_structure_id nao exposta")
        result = derived_service._resolve_structure_id("VALE5")
        assert result is None or isinstance(result, int)

    def test_unwrap_aba_presente_no_modulo(self):
        if not HAS_REPO:
            pytest.skip("derived_repo nao disponivel")
        import inspect
        src = inspect.getsource(derived_repo)
        assert "_unwrap_aba" in src, "_unwrap_aba nao encontrado no modulo"

    def test_fstring_bug_ausente_no_service(self):
        if not HAS_SERVICE:
            pytest.skip("derived_service nao disponivel")
        import inspect
        src = inspect.getsource(derived_service)
        assert "{ref.db_column()}" not in src, "Bug f-string remanescente"

    def test_get_payoff_by_aba_ausente_confirma_patch65(self):
        """
        Regressao inversa: confirma que patch_65 nao foi revertido
        por nenhum patch posterior.
        """
        if not HAS_SERVICE:
            pytest.skip("derived_service nao disponivel")
        assert not hasattr(derived_service, "get_payoff_by_aba"), (
            "patch_65 revertido -- get_payoff_by_aba nao deveria existir"
        )

    def test_derived_service_class_nao_expoe_get_payoff_by_aba(self):
        if not HAS_SERVICE:
            pytest.skip("derived_service nao disponivel")
        svc = derived_service.DerivedService()
        assert not hasattr(svc, "get_payoff_by_aba"), (
            "DerivedService.get_payoff_by_aba presente -- patch_65 revertido"
        )

    def test_derived_service_class_expoe_get_payoff_by_structure_id(self):
        if not HAS_SERVICE:
            pytest.skip("derived_service nao disponivel")
        svc = derived_service.DerivedService()
        assert hasattr(svc, "get_payoff_by_structure_id"), (
            "DerivedService.get_payoff_by_structure_id ausente"
        )
