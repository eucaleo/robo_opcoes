"""
Testes do patch_45 -- CalculationRequest canônico.
"""
import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)

from domain.calculation_request import (
    CalculationRequest,
    MarketSnapshotInput,
    StructureInput,
    StructureLegInput,
)
from services.calculation_orchestrator import build_calculation_request


def _make_leg(**kwargs) -> StructureLegInput:
    defaults = dict(
        position_side="LONG",
        option_type="CALL",
        strike=100.0,
        expiration_date="2026-07-18",
        quantity=1000,
    )
    defaults.update(kwargs)
    return StructureLegInput(**defaults)


def _make_structure(**kwargs) -> StructureInput:
    defaults = dict(
        structure_id=1,
        underlying_asset="BOVA11",
        legs=[_make_leg()],
    )
    defaults.update(kwargs)
    return StructureInput(**defaults)


def _make_snapshot(**kwargs) -> MarketSnapshotInput:
    defaults = dict(
        snapshot_timestamp="2026-06-02T20:00:00",
        underlying_asset="BOVA11",
        spot_price=100.0,
        source="rtd",
    )
    defaults.update(kwargs)
    return MarketSnapshotInput(**defaults)


class TestPatch45ContratoDomain(unittest.TestCase):
    """Valida criação e imutabilidade dos DTOs do domínio."""

    def test_structure_leg_input_valido(self):
        leg = _make_leg()
        self.assertEqual(leg.position_side, "LONG")
        self.assertEqual(leg.option_type, "CALL")
        self.assertEqual(leg.strike, 100.0)
        self.assertEqual(leg.quantity, 1000)

    def test_structure_input_valido(self):
        s = _make_structure()
        self.assertEqual(s.structure_id, 1)
        self.assertEqual(len(s.legs), 1)

    def test_market_snapshot_valido(self):
        sn = _make_snapshot()
        self.assertEqual(sn.spot_price, 100.0)
        self.assertEqual(sn.source, "rtd")

    def test_calculation_request_valido(self):
        req = CalculationRequest(structure=_make_structure(), market_snapshot=_make_snapshot())
        self.assertEqual(req.structure.structure_id, 1)
        self.assertAlmostEqual(req.market_snapshot.spot_price, 100.0)

    def test_underlying_divergente_levanta_value_error(self):
        with self.assertRaises(ValueError):
            CalculationRequest(
                structure=_make_structure(underlying_asset="BOVA11"),
                market_snapshot=_make_snapshot(underlying_asset="PETR4"),
            )

    def test_position_side_invalido(self):
        with self.assertRaises(ValueError):
            _make_leg(position_side="COMPRA")

    def test_option_type_invalido(self):
        with self.assertRaises(ValueError):
            _make_leg(option_type="OPCAO")

    def test_strike_zero_invalido(self):
        with self.assertRaises(ValueError):
            _make_leg(strike=0.0)

    def test_quantity_zero_invalido(self):
        with self.assertRaises(ValueError):
            _make_leg(quantity=0)

    def test_expiration_date_formato_errado(self):
        with self.assertRaises(ValueError):
            _make_leg(expiration_date="18/07/2026")

    def test_dto_e_imutavel(self):
        """frozen=True -- atribuição deve levantar FrozenInstanceError."""
        leg = _make_leg()
        with self.assertRaises(Exception):
            leg.strike = 999.0  # type: ignore


class TestPatch45OrchestratorBuildsDTO(unittest.TestCase):
    """Valida build_calculation_request com dados vindos do repositório."""

    def _structure_row(self):
        return {"id": 10, "underlying_asset": "PETR4", "name": "Trava", "alias_legacy_aba": "PETR4"}

    def _legs_rows(self):
        return [
            {"position_side": "LONG",  "option_type": "CALL", "strike": 38.0,
             "expiration_date": "2026-07-18", "quantity": 1000, "leg_order": 0},
            {"cv": "V", "call_put": "PUT", "strike": 40.0,
             "expiration_date": "2026-07-18", "quantity": 1000, "leg_order": 1},
        ]

    def _snapshot_row(self):
        return {"snapshot_timestamp": "2026-06-02T20:00:00",
                "underlying_asset": "PETR4", "spot_price": 37.5, "source": "rtd"}

    def test_build_retorna_calculation_request(self):
        req = build_calculation_request(self._structure_row(), self._legs_rows(), self._snapshot_row())
        self.assertIsInstance(req, CalculationRequest)

    def test_build_normaliza_cv_legado(self):
        req = build_calculation_request(self._structure_row(), self._legs_rows(), self._snapshot_row())
        self.assertEqual(req.structure.legs[1].position_side, "SHORT")

    def test_build_normaliza_call_put_legado(self):
        req = build_calculation_request(self._structure_row(), self._legs_rows(), self._snapshot_row())
        self.assertEqual(req.structure.legs[1].option_type, "PUT")

    def test_build_structure_id_correto(self):
        req = build_calculation_request(self._structure_row(), self._legs_rows(), self._snapshot_row())
        self.assertEqual(req.structure.structure_id, 10)

    def test_build_legs_vazias_levanta_error(self):
        with self.assertRaises(ValueError):
            build_calculation_request(self._structure_row(), [], self._snapshot_row())


class TestPatch45SemAcessoRawDB(unittest.TestCase):
    """Garante que o contrato de domínio não importa módulos de DB."""

    def test_calculation_request_nao_importa_sqlite3(self):
        import domain.calculation_request as mod
        import inspect
        src = inspect.getsource(mod)
        self.assertNotIn("import sqlite3", src)
        self.assertNotIn("get_app_db_connection", src)

    def test_orchestrator_nao_acessa_db_diretamente(self):
        import services.calculation_orchestrator as mod
        import inspect
        src = inspect.getsource(mod)
        self.assertNotIn("sqlite3.connect", src)
        self.assertNotIn("get_app_db_connection", src)

    def test_script_smoke_existe(self):
        path = os.path.join(ROOT, "scripts", "45_smoke_calculation_request.py")
        self.assertTrue(os.path.isfile(path), f"smoke script não encontrado: {path}")


if __name__ == "__main__":
    unittest.main()
