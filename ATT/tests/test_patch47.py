"""
patch_47 -- Testes: run_decision auto-extract + run_full_pipeline + multiplier fix.
"""
from __future__ import annotations

import unittest
from types import SimpleNamespace
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Helpers de fixture
# ---------------------------------------------------------------------------

def _make_request(pl_max_hint=1000.0, spot=100.0, multiplier=1.0):
    """Monta um CalculationRequest minimo para testes."""
    leg = SimpleNamespace(
        position_side="LONG",
        option_type="CALL",
        strike=100.0,
        expiration_date="2026-12-19",
        quantity=100,
        symbol=None,
        premium=None,
        multiplier=multiplier,
        leg_order=0,
        notes=None,
    )
    structure = SimpleNamespace(
        structure_id=1,
        underlying_asset="BOVA11",
        name="Test Structure",
        alias_legacy_aba="BOVA11",
        legs=[leg],
    )
    snapshot = SimpleNamespace(
        snapshot_timestamp="2026-06-03T07:00:00",
        underlying_asset="BOVA11",
        spot_price=spot,
        source="rtd",
        snapshot_id=None,
        option_quotes=None,
        greeks=None,
        volatility_context=None,
        dte_min=None,
    )
    return SimpleNamespace(structure=structure, market_snapshot=snapshot)


# ---------------------------------------------------------------------------
# TestPatch47ArquivoExiste
# ---------------------------------------------------------------------------

class TestPatch47ArquivoExiste(unittest.TestCase):

    def test_orchestrator_importavel(self):
        import services.calculation_orchestrator as m
        self.assertTrue(hasattr(m, "run_payoff"))
        self.assertTrue(hasattr(m, "run_decision"))
        self.assertTrue(hasattr(m, "run_full_pipeline"))

    def test_run_full_pipeline_presente(self):
        from services.calculation_orchestrator import run_full_pipeline
        self.assertTrue(callable(run_full_pipeline))


# ---------------------------------------------------------------------------
# TestMultiplierFix
# ---------------------------------------------------------------------------

class TestMultiplierFix(unittest.TestCase):
    """Garante que multiplier usa leg.multiplier sem hardcode."""

    def test_multiplier_propagado_do_leg(self):
        from services.calculation_orchestrator import _request_to_payoff_dict
        req = _make_request(multiplier=50.0)
        canonical = _request_to_payoff_dict(req)
        leg_dict = canonical["structure"]["legs"][0]
        self.assertEqual(leg_dict["multiplier"], 50.0)

    def test_multiplier_default_e_1(self):
        from services.calculation_orchestrator import _request_to_payoff_dict
        req = _make_request(multiplier=1.0)
        canonical = _request_to_payoff_dict(req)
        leg_dict = canonical["structure"]["legs"][0]
        self.assertEqual(leg_dict["multiplier"], 1.0)

    def test_multiplier_nao_e_hardcode_100(self):
        from services.calculation_orchestrator import _request_to_payoff_dict
        req = _make_request(multiplier=1.0)
        canonical = _request_to_payoff_dict(req)
        leg_dict = canonical["structure"]["legs"][0]
        self.assertNotEqual(leg_dict["multiplier"], 100)


# ---------------------------------------------------------------------------
# TestRunDecisionAutoExtract
# ---------------------------------------------------------------------------

class TestRunDecisionAutoExtract(unittest.TestCase):
    """Garante que run_decision extrai pl_max/pl_atual do payoff automaticamente."""

    def test_pl_max_extraido_do_payoff(self):
        from services.calculation_orchestrator import run_decision
        req = _make_request()
        payoff = {"pl_max": 800.0, "pl_atual": 0.0, "points": [], "pl_min": 0.0}
        result = run_decision(req, payoff=payoff)
        # Com pl_max=800 e pl_atual=0 -> ratio=0 -> HOLD
        self.assertIn("decision", result)
        self.assertEqual(result["decision"], "HOLD")

    def test_sem_hold_silencioso_quando_payoff_tem_pl_max(self):
        from services.calculation_orchestrator import run_decision
        req = _make_request()
        # pl_atual = 85% de pl_max -> deve acionar CLOSE_REOPEN
        payoff = {"pl_max": 1000.0, "pl_atual": 850.0, "points": [], "pl_min": 0.0}
        result = run_decision(req, payoff=payoff)
        self.assertEqual(result["decision"], "CLOSE_REOPEN")
        self.assertEqual(result["level"], 3)

    def test_pl_max_zero_sem_excecao(self):
        from services.calculation_orchestrator import run_decision
        req = _make_request()
        payoff = {"pl_max": 0.0, "pl_atual": 0.0, "points": [], "pl_min": 0.0}
        result = run_decision(req, payoff=payoff)
        self.assertEqual(result["decision"], "HOLD")

    def test_sem_payoff_usa_defaults_zerados(self):
        from services.calculation_orchestrator import run_decision
        req = _make_request()
        result = run_decision(req)
        self.assertEqual(result["decision"], "HOLD")
        self.assertEqual(result["level"], 0)


# ---------------------------------------------------------------------------
# TestRunFullPipeline
# ---------------------------------------------------------------------------

class TestRunFullPipeline(unittest.TestCase):
    """Garante que run_full_pipeline retorna payoff + decision coerentes."""

    def test_retorna_chaves_esperadas(self):
        from services.calculation_orchestrator import run_full_pipeline
        req = _make_request(spot=100.0)
        result = run_full_pipeline(req)
        self.assertIn("payoff",           result)
        self.assertIn("decision",         result)
        self.assertIn("structure_id",     result)
        self.assertIn("underlying_asset", result)

    def test_structure_id_correto(self):
        from services.calculation_orchestrator import run_full_pipeline
        req = _make_request()
        result = run_full_pipeline(req)
        self.assertEqual(result["structure_id"], 1)

    def test_underlying_asset_correto(self):
        from services.calculation_orchestrator import run_full_pipeline
        req = _make_request()
        result = run_full_pipeline(req)
        self.assertEqual(result["underlying_asset"], "BOVA11")

    def test_payoff_tem_points(self):
        from services.calculation_orchestrator import run_full_pipeline
        req = _make_request(spot=100.0)
        result = run_full_pipeline(req)
        self.assertIn("points", result["payoff"])

    def test_decision_tem_level(self):
        from services.calculation_orchestrator import run_full_pipeline
        req = _make_request(spot=100.0)
        result = run_full_pipeline(req)
        self.assertIn("level", result["decision"])

    def test_pipeline_sem_acesso_a_db(self):
        """Garante que run_full_pipeline nao importa sqlite3 no orchestrator."""
        import services.calculation_orchestrator as mod
        import inspect
        src = inspect.getsource(mod)
        self.assertNotIn("sqlite3", src)
        self.assertNotIn("get_app_db_connection", src)


if __name__ == "__main__":
    unittest.main()
