# ATT/tests/test_patch48.py
# Testes do patch_48: build_calculation_request_from_db + run_full_pipeline_from_db

import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers de fixture
# ---------------------------------------------------------------------------

def _make_structure(structure_id=1, status="active", n_legs=2):
    legs = [
        {
            "id": 10 + i,
            "structure_id": structure_id,
            "position_side": "LONG" if i % 2 == 0 else "SHORT",
            "option_type": "CALL",
            "strike": 100.0 + i * 5,
            "expiration_date": "2026-12-19",
            "quantity": 100,
            "symbol": f"SYM{i}",
            "premium": None,
            "multiplier": 1.0,
        }
        for i in range(n_legs)
    ]
    return {
        "id": structure_id,
        "name": "Test Structure",
        "underlying_asset": "BOVA11",
        "alias_legacy_aba": "BOVA11",
        "status": status,
        "notes": None,
        "legs": legs,
    }


def _make_snapshot(underlying="BOVA11", ts="2026-06-03T08:00:00"):
    return {
        "id": 99,
        "underlying_asset": underlying,
        "snapshot_timestamp": ts,
        "spot_price": 130.0,
        "source": "rtd",
    }


def _make_orchestrator(structure=None, snapshot=None):
    """Cria orquestrador com repositorios mockados."""
    from services.calculation_orchestrator import CalculationOrchestrator

    structures_repo = MagicMock()
    snapshot_repo = MagicMock()

    structures_repo.get_structure.return_value = structure
    snapshot_repo.get_snapshot.return_value = snapshot

    orch = CalculationOrchestrator(
        structures_repository=structures_repo,
        market_snapshot_repository=snapshot_repo,
    )
    return orch, structures_repo, snapshot_repo


# ---------------------------------------------------------------------------
# 1. Arquivo e imports
# ---------------------------------------------------------------------------

class TestPatch48ArquivoExiste(unittest.TestCase):

    def test_orchestrator_existe(self):
        p = Path("services/calculation_orchestrator.py")
        self.assertTrue(p.exists(), "services/calculation_orchestrator.py nao existe")

    def test_test_file_existe(self):
        p = Path("ATT/tests/test_patch48.py")
        self.assertTrue(p.exists(), "ATT/tests/test_patch48.py nao existe")

    def test_import_orchestrator(self):
        from services.calculation_orchestrator import CalculationOrchestrator
        self.assertTrue(callable(CalculationOrchestrator))

    def test_metodo_build_from_db_existe(self):
        from services.calculation_orchestrator import CalculationOrchestrator
        self.assertTrue(
            hasattr(CalculationOrchestrator, "build_calculation_request_from_db")
        )

    def test_metodo_run_full_pipeline_from_db_existe(self):
        from services.calculation_orchestrator import CalculationOrchestrator
        self.assertTrue(
            hasattr(CalculationOrchestrator, "run_full_pipeline_from_db")
        )


# ---------------------------------------------------------------------------
# 2. build_calculation_request_from_db
# ---------------------------------------------------------------------------

class TestBuildRequestFromDb(unittest.TestCase):

    def test_retorna_calculation_request(self):
        from domain.calculation_request import CalculationRequest

        orch, _, _ = _make_orchestrator(
            structure=_make_structure(),
            snapshot=_make_snapshot(),
        )
        req = orch.build_calculation_request_from_db(structure_id=1)
        self.assertIsInstance(req, CalculationRequest)

    def test_structure_id_propagado(self):
        orch, _, _ = _make_orchestrator(
            structure=_make_structure(structure_id=7),
            snapshot=_make_snapshot(),
        )
        req = orch.build_calculation_request_from_db(structure_id=7)
        self.assertEqual(req.structure.structure_id, 7)

    def test_underlying_asset_propagado(self):
        orch, _, _ = _make_orchestrator(
            structure=_make_structure(),
            snapshot=_make_snapshot(underlying="BOVA11"),
        )
        req = orch.build_calculation_request_from_db(structure_id=1)
        self.assertEqual(req.structure.underlying_asset, "BOVA11")

    def test_spot_price_propagado(self):
        snap = _make_snapshot()
        snap["spot_price"] = 142.5
        orch, _, _ = _make_orchestrator(
            structure=_make_structure(),
            snapshot=snap,
        )
        req = orch.build_calculation_request_from_db(structure_id=1)
        self.assertAlmostEqual(req.market_snapshot.spot_price, 142.5)

    def test_legs_contagem(self):
        orch, _, _ = _make_orchestrator(
            structure=_make_structure(n_legs=3),
            snapshot=_make_snapshot(),
        )
        req = orch.build_calculation_request_from_db(structure_id=1)
        self.assertEqual(len(req.structure.legs), 3)

    def test_snapshot_timestamp_repassado(self):
        snap = _make_snapshot(ts="2026-06-01T10:00:00")
        orch, _, snap_repo = _make_orchestrator(
            structure=_make_structure(),
            snapshot=snap,
        )
        orch.build_calculation_request_from_db(
            structure_id=1,
            snapshot_timestamp="2026-06-01T10:00:00",
        )
        snap_repo.get_snapshot.assert_called_once_with(
            underlying_asset="BOVA11",
            timestamp="2026-06-01T10:00:00",
        )

    def test_structures_repo_chamado_com_id_correto(self):
        orch, struct_repo, _ = _make_orchestrator(
            structure=_make_structure(structure_id=42),
            snapshot=_make_snapshot(),
        )
        orch.build_calculation_request_from_db(structure_id=42)
        struct_repo.get_structure.assert_called_once_with(42)


# ---------------------------------------------------------------------------
# 3. Guards de erro em build_calculation_request_from_db
# ---------------------------------------------------------------------------

class TestBuildRequestFromDbGuards(unittest.TestCase):

    def test_sem_structures_repo_levanta_runtime_error(self):
        from services.calculation_orchestrator import CalculationOrchestrator

        orch = CalculationOrchestrator(
            structures_repository=None,
            market_snapshot_repository=MagicMock(),
        )
        with self.assertRaises(RuntimeError):
            orch.build_calculation_request_from_db(structure_id=1)

    def test_sem_snapshot_repo_levanta_runtime_error(self):
        from services.calculation_orchestrator import CalculationOrchestrator

        orch = CalculationOrchestrator(
            structures_repository=MagicMock(),
            market_snapshot_repository=None,
        )
        with self.assertRaises(RuntimeError):
            orch.build_calculation_request_from_db(structure_id=1)

    def test_estrutura_nao_encontrada_levanta_value_error(self):
        orch, _, _ = _make_orchestrator(structure=None, snapshot=_make_snapshot())
        with self.assertRaises(ValueError):
            orch.build_calculation_request_from_db(structure_id=999)

    def test_estrutura_arquivada_levanta_value_error(self):
        orch, _, _ = _make_orchestrator(
            structure=_make_structure(status="archived"),
            snapshot=_make_snapshot(),
        )
        with self.assertRaises(ValueError):
            orch.build_calculation_request_from_db(structure_id=1)

    def test_estrutura_sem_legs_levanta_value_error(self):
        structure = _make_structure(n_legs=0)
        orch, _, _ = _make_orchestrator(
            structure=structure,
            snapshot=_make_snapshot(),
        )
        with self.assertRaises(ValueError):
            orch.build_calculation_request_from_db(structure_id=1)

    def test_snapshot_nao_encontrado_levanta_value_error(self):
        orch, _, _ = _make_orchestrator(
            structure=_make_structure(),
            snapshot=None,
        )
        with self.assertRaises(ValueError):
            orch.build_calculation_request_from_db(structure_id=1)


# ---------------------------------------------------------------------------
# 4. run_full_pipeline_from_db
# ---------------------------------------------------------------------------

class TestRunFullPipelineFromDb(unittest.TestCase):

    def _orch_com_pipeline_mockado(self):
        """
        Retorna orquestrador com build_calculation_request_from_db
        e run_full_pipeline mockados para isolar a logica de composicao.
        """
        from services.calculation_orchestrator import CalculationOrchestrator
        from domain.calculation_request import (
            CalculationRequest,
            StructureInput,
            MarketSnapshotInput,
        )

        fake_request = MagicMock(spec=CalculationRequest)
        fake_pipeline = {"payoff": {"pl_max": 500.0}, "decision": {"level": "OK"}}

        orch = CalculationOrchestrator(
            structures_repository=MagicMock(),
            market_snapshot_repository=MagicMock(),
        )
        orch.build_calculation_request_from_db = MagicMock(return_value=fake_request)
        orch.run_full_pipeline = MagicMock(return_value=fake_pipeline)

        return orch, fake_request, fake_pipeline

    def test_retorna_dict_com_chaves_corretas(self):
        orch, _, _ = self._orch_com_pipeline_mockado()
        result = orch.run_full_pipeline_from_db(structure_id=5)
        self.assertIn("structure_id", result)
        self.assertIn("payoff", result)
        self.assertIn("decision", result)

    def test_structure_id_no_retorno(self):
        orch, _, _ = self._orch_com_pipeline_mockado()
        result = orch.run_full_pipeline_from_db(structure_id=5)
        self.assertEqual(result["structure_id"], 5)

    def test_payoff_e_decision_propagados(self):
        orch, _, fake_pipeline = self._orch_com_pipeline_mockado()
        result = orch.run_full_pipeline_from_db(structure_id=5)
        self.assertEqual(result["payoff"], fake_pipeline["payoff"])
        self.assertEqual(result["decision"], fake_pipeline["decision"])

    def test_build_from_db_chamado_com_structure_id(self):
        orch, _, _ = self._orch_com_pipeline_mockado()
        orch.run_full_pipeline_from_db(structure_id=9)
        orch.build_calculation_request_from_db.assert_called_once_with(
            structure_id=9, snapshot_timestamp=None
        )

    def test_build_from_db_chamado_com_timestamp(self):
        orch, _, _ = self._orch_com_pipeline_mockado()
        orch.run_full_pipeline_from_db(
            structure_id=9,
            snapshot_timestamp="2026-06-01T10:00:00",
        )
        orch.build_calculation_request_from_db.assert_called_once_with(
            structure_id=9,
            snapshot_timestamp="2026-06-01T10:00:00",
        )

    def test_run_full_pipeline_chamado_com_request(self):
        orch, fake_request, _ = self._orch_com_pipeline_mockado()
        orch.run_full_pipeline_from_db(structure_id=9)
        orch.run_full_pipeline.assert_called_once_with(fake_request)


# ---------------------------------------------------------------------------
# 5. Sem acesso direto a DB
# ---------------------------------------------------------------------------

class TestOrchestratorNaoAcessaDBDireto(unittest.TestCase):

    def test_sem_sqlite3_no_orchestrator(self):
        src = Path("services/calculation_orchestrator.py").read_text(encoding="utf-8")
        self.assertNotIn(
            "import sqlite3",
            src,
            "orchestrator nao deve importar sqlite3 diretamente",
        )

    def test_sem_get_app_db_connection(self):
        src = Path("services/calculation_orchestrator.py").read_text(encoding="utf-8")
        self.assertNotIn(
            "get_app_db_connection",
            src,
            "orchestrator nao deve chamar get_app_db_connection",
        )

    def test_repositorios_injetados_por_construtor(self):
        from services.calculation_orchestrator import CalculationOrchestrator
        import inspect

        sig = inspect.signature(CalculationOrchestrator.__init__)
        params = list(sig.parameters.keys())
        self.assertIn("structures_repository", params)
        self.assertIn("market_snapshot_repository", params)

    def test_construtor_sem_repositorios_nao_levanta(self):
        """Sem injecao de repos o construtor deve funcionar normalmente."""
        from services.calculation_orchestrator import CalculationOrchestrator

        try:
            orch = CalculationOrchestrator()
        except Exception as exc:
            self.fail(
                f"Construtor sem repositorios levantou excecao inesperada: {exc}"
            )


if __name__ == "__main__":
    unittest.main()
