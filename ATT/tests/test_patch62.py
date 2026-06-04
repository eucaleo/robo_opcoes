# ATT/tests/test_patch62.py
"""Testes unitários do patch_62.
patch_65: TestGetPayoffByAbaDeprecation substituída por TestGetPayoffByAbaRemovida.
"""

import sqlite3
import warnings
from contextlib import contextmanager

import pytest
from unittest.mock import MagicMock

from repositories._aba_resolver_mixin import AbaResolverMixin


# ------------------------------------------------------------------ #
# Helpers de teste                                                    #
# ------------------------------------------------------------------ #

@contextmanager
def _conn_as_context(conn: sqlite3.Connection):
    """
    Adapta uma conexão sqlite3 existente para o protocolo
    context manager esperado pelo mixin (with conn as c: ...).
    Não fecha a conexão ao sair -- ela pertence ao fixture.
    """
    yield conn


class FakeRepository(AbaResolverMixin):
    """
    Implementação mínima para testes do mixin.
    Sobrescreve _get_resolver_conn() para usar conexão injetada,
    sem depender de self.config nem de sqlite_conn().
    """

    def __init__(self, conn: sqlite3.Connection):
        self._test_conn = conn

    def _get_resolver_conn(self):
        return _conn_as_context(self._test_conn)


# ------------------------------------------------------------------ #
# Fixture                                                             #
# ------------------------------------------------------------------ #

@pytest.fixture
def db_with_structure():
    """Banco em memória com tabela structures."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE structures (
            id INTEGER PRIMARY KEY,
            alias_legacy_aba TEXT
        )
        """
    )
    conn.execute("INSERT INTO structures VALUES (1, 'PETR4')")
    conn.execute("INSERT INTO structures VALUES (2, '')")    # vazio
    conn.execute("INSERT INTO structures VALUES (3, NULL)")  # null
    conn.commit()
    yield conn
    conn.close()


# ------------------------------------------------------------------ #
# TestAbaResolverMixin                                                #
# ------------------------------------------------------------------ #

class TestAbaResolverMixin:

    def test_resolve_existente(self, db_with_structure):
        repo = FakeRepository(db_with_structure)
        assert repo._resolve_aba_from_structure_id(1) == "PETR4"

    def test_resolve_alias_vazio_retorna_none(self, db_with_structure):
        repo = FakeRepository(db_with_structure)
        assert repo._resolve_aba_from_structure_id(2) is None

    def test_resolve_alias_null_retorna_none(self, db_with_structure):
        repo = FakeRepository(db_with_structure)
        assert repo._resolve_aba_from_structure_id(3) is None

    def test_resolve_id_inexistente_retorna_none(self, db_with_structure):
        repo = FakeRepository(db_with_structure)
        assert repo._resolve_aba_from_structure_id(999) is None

    def test_resolve_structure_id_none_retorna_none(self, db_with_structure):
        repo = FakeRepository(db_with_structure)
        assert repo._resolve_aba_from_structure_id(None) is None

    def test_resolve_nao_lanca_excecao_em_falha(self):
        """Mesmo com _get_resolver_conn() lançando, não propaga exceção."""
        class BrokenRepository(AbaResolverMixin):
            def _get_resolver_conn(self):
                raise RuntimeError("db off")

        repo = BrokenRepository()
        result = repo._resolve_aba_from_structure_id(1)
        assert result is None


# ------------------------------------------------------------------ #
# TestGetPayoffByAbaRemovida  (patch_65)                             #
# Substitui TestGetPayoffByAbaDeprecation do patch_62.               #
# ------------------------------------------------------------------ #

class TestGetPayoffByAbaRemovida:
    """
    patch_65: get_payoff_by_aba() foi removida de derived_service.
    Garante que a função NÃO existe mais no módulo e que a substituta
    get_payoff_by_structure_id() está presente e acessível.
    """

    def test_get_payoff_by_aba_nao_existe_mais(self):
        """Função removida não deve mais ser encontrada no módulo."""
        from services import derived_service
        assert not hasattr(derived_service, "get_payoff_by_aba"), (
            "get_payoff_by_aba() ainda existe em derived_service — deve ser removida no patch_65"
        )

    def test_get_payoff_by_structure_id_existe(self):
        """Substituta canônica deve estar presente e ser callable."""
        from services import derived_service
        assert hasattr(derived_service, "get_payoff_by_structure_id"), (
            "get_payoff_by_structure_id() não encontrada em derived_service"
        )
        assert callable(derived_service.get_payoff_by_structure_id)

    def test_nao_ha_import_warnings_no_modulo(self):
        """
        Reimportação do módulo não deve emitir nenhum DeprecationWarning
        relacionado a get_payoff_by_aba após a remoção.
        """
        import importlib
        from services import derived_service

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            importlib.reload(derived_service)

        aba_warnings = [
            w for w in caught
            if issubclass(w.category, DeprecationWarning)
            and "get_payoff_by_aba" in str(w.message)
        ]
        assert aba_warnings == [], (
            f"DeprecationWarning de get_payoff_by_aba ainda emitido após patch_65: {aba_warnings}"
        )


# ------------------------------------------------------------------ #
# TestSemDuplicacao                                                   #
# ------------------------------------------------------------------ #

class TestSemDuplicacao:

    def test_robo_legs_nao_define_resolve_local(self):
        from repositories.robo_legs_repository import RoboLegsRepository
        assert "_resolve_aba_from_structure_id" not in RoboLegsRepository.__dict__, (
            "Método ainda definido localmente em RoboLegsRepository — remova-o"
        )

    def test_robo_legs_status_nao_define_resolve_local(self):
        from repositories.robo_legs_status_repository import RoboLegsStatusRepository
        assert "_resolve_aba_from_structure_id" not in RoboLegsStatusRepository.__dict__, (
            "Método ainda definido localmente em RoboLegsStatusRepository — remova-o"
        )

    def test_ambos_herdam_mixin(self):
        from repositories.robo_legs_repository import RoboLegsRepository
        from repositories.robo_legs_status_repository import RoboLegsStatusRepository
        assert issubclass(RoboLegsRepository, AbaResolverMixin)
        assert issubclass(RoboLegsStatusRepository, AbaResolverMixin)
