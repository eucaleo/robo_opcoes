# ATT/tests/test_patch65.py
"""
patch_65 -- Testes de remoção definitiva de get_payoff_by_aba().
"""
import importlib
import inspect
import unittest
import warnings


class TestGetPayoffByAbaRemovida(unittest.TestCase):
    """A função get_payoff_by_aba() não deve mais existir no módulo."""

    def test_funcao_removida_nao_existe(self):
        import services.derived_service as mod
        self.assertFalse(
            hasattr(mod.DerivedService, "get_payoff_by_aba"),
            "get_payoff_by_aba() ainda existe -- deve ter sido removida no patch_65",
        )


class TestGetPayoffByStructureIdPreservado(unittest.TestCase):
    """get_payoff_by_structure_id() deve permanecer intacta."""

    def test_get_payoff_by_structure_id_funciona(self):
        import services.derived_service as mod
        self.assertTrue(
            hasattr(mod.DerivedService, "get_payoff_by_structure_id"),
            "get_payoff_by_structure_id() foi removida acidentalmente",
        )


class TestSemWarningResidual(unittest.TestCase):
    """Nenhum resíduo de DeprecationWarning ou import warnings no módulo."""

    def test_sem_deprecation_warning(self):
        import services.derived_service as mod
        src = inspect.getsource(mod)
        self.assertNotIn(
            "DeprecationWarning",
            src,
            "DeprecationWarning residual encontrado em derived_service",
        )

    def test_import_warnings_removido(self):
        import services.derived_service as mod
        src = inspect.getsource(mod)
        self.assertNotIn(
            "import warnings",
            src,
            "import warnings residual encontrado em derived_service",
        )


if __name__ == "__main__":
    unittest.main()
