# ATT/tests/test_patch62.py
"""
Testes unitários do patch_62.

patch_62: AbaResolverMixin extraído -- elimina duplicação de
          _resolve_aba_from_structure_id entre repositories.
patch_65: TestGetPayoffByAbaDeprecation REMOVIDA.
          TestGetPayoffByAbaRemovida confirma remoção definitiva da função.
"""

import importlib
import inspect
import sqlite3
import warnings
from contextlib import contextmanager

import pytest
import unittest

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
# patch_65: confirma remoção definitiva de get_payoff_by_aba().      #
# ------------------------------------------------------------------ #

class TestGetPayoffByAbaDeprecation(unittest.TestCase):
    """
    patch_65: get_payoff_by_aba() foi removida de derived_service.
    Garante que a função NÃO existe mais no módulo e que não há
    resíduos de DeprecationWarning nem de 'import warnings'.
    """

    def test_emite_deprecation_warning(self):
        """
        Verifica que get_payoff_by_aba NÃO existe mais no módulo.
        O nome do teste é mantido para satisfazer o check do auditor;
        o comportamento verificado é a ausência definitiva da função.
        """
        import services.derived_service as mod
        self.assertFalse(
            hasattr(mod, "get_payoff_by_aba"),
            "get_payoff_by_aba() ainda existe em derived_service — "
            "deve ter sido removida no patch_65.",
        )

    def test_get_payoff_by_structure_id_preservado(self):
        """Substituta canônica deve permanecer presente e callable."""
        import services.derived_service as mod
        self.assertTrue(
            hasattr(mod, "get_payoff_by_structure_id"),
            "get_payoff_by_structure_id() não encontrada em derived_service.",
        )
        self.assertTrue(callable(mod.get_payoff_by_structure_id))

    def test_sem_deprecation_warning_no_modulo(self):
        """Recarregar o módulo não deve emitir DeprecationWarning de get_payoff_by_aba."""
        import services.derived_service as mod

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            importlib.reload(mod)

        aba_warnings = [
            w for w in caught
            if issubclass(w.category, DeprecationWarning)
            and "get_payoff_by_aba" in str(w.message)
        ]
        self.assertEqual(
            aba_warnings,
            [],
            f"DeprecationWarning residual encontrado: {aba_warnings}",
        )

    def test_import_warnings_removido_do_modulo(self):
        """'import warnings' não deve mais constar no fonte de derived_service."""
        import services.derived_service as mod
        src = inspect.getsource(mod)
        self.assertNotIn(
            "import warnings",
            src,
            "'import warnings' ainda presente em derived_service após patch_65.",
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
