# ATT/tests/test_patch62.py
"""Testes unitários do patch_62."""

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
# TestGetPayoffByAbaDeprecation                                       #
# ------------------------------------------------------------------ #

class TestGetPayoffByAbaDeprecation:

    def test_emite_deprecation_warning(self):
        from services import derived_service

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            try:
                derived_service.get_payoff_by_aba(MagicMock())
            except Exception:
                pass  # ignora erros de lógica interna
            msgs = [str(w.message) for w in caught if issubclass(w.category, DeprecationWarning)]
            assert any(
                "patch_62" in m or "get_payoff_by_aba" in m for m in msgs
            ), f"DeprecationWarning não emitido. Capturado: {msgs}"


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
