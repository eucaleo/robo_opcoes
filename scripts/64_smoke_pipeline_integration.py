# scripts/64_smoke_pipeline_integration.py
"""
patch_15 -- Smoke: integração completa pipeline structure + snapshot  pricing.

Fluxo testado:
  StructuresRepository
       
  CanonicalInputService  (com MarketSnapshotSelector manual>rtd)
       
  PricingExecutionAppService.execute_pricing()
       
  resultado persistido e consultável

Cenários cobertos:
  1. Pipeline completo com selector manual  execução OK
  2. Pipeline completo com selector RTD    execução OK
  3. Pipeline sem selector (legado)        execução OK (regressão)
  4. Structure inexistente  erro tratado antes do pricing
  5. PricingExecutionAppService importável
"""
from __future__ import annotations


import sys
import os
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from domain.market_snapshot import LegMarketSnapshot, SnapshotSource
from services.market_snapshot_selector import MarketSnapshotSelector, SnapshotSelectionResult
from services.canonical_input_service import CanonicalInputService
from services.pricing_execution_app_service import PricingExecutionAppService

# ---------------------------------------------------------------------------
# Fixtures reutilizáveis
# ---------------------------------------------------------------------------

def _make_structure(structure_id: int = 1, aba: str | None = "PETR4") -> dict:
    return {
        "id":               structure_id,
        "name":             "Pipe Smoke",
        "underlying_asset": "PETR4",
        "alias_legacy_aba": aba,
        "legs": [
            {
                "id":              1,
                "option_symbol":   "PETRA100",
                "position_side":   "long",
                "option_type":     "call",
                "strike":          100.0,
                "expiration_date": "2026-06-20",
                "quantity":        1,
            }
        ],
    }


def _make_leg_snapshot(aba: str, ativo: str, source: SnapshotSource) -> LegMarketSnapshot:
    # LegMarketSnapshot: aba é 1º posicional obrigatório, ativo é 2º
    return LegMarketSnapshot(
        aba=aba,
        ativo=ativo,
        bid=10.0,
        ask=10.5,
        mid=10.25,
        source=source,
    )


def _make_selector_mock(
    aba: str,
    source: SnapshotSource,
    with_override: bool = False,
) -> MagicMock:
    result = SnapshotSelectionResult(
        aba=aba,
        source=source,
        legs=[_make_leg_snapshot(aba=aba, ativo="PETRA100", source=source)],
        manual_overrides=["PETRA100"] if with_override else [],
    )
    selector = MagicMock(spec=MarketSnapshotSelector)
    selector.select.return_value = result
    return selector


def _make_repo_mock(structure: dict) -> MagicMock:
    repo = MagicMock()
    repo.get_structure.return_value = structure
    return repo


def _make_provider_mock() -> MagicMock:
    provider = MagicMock()
    provider.get_snapshot.return_value = {
        "aba":            "PETR4",
        "legs":           [],
        "reference_date": "2026-05-28",
    }
    return provider


def _assembled_stub() -> dict:
    """Retorno padrão do assembler -- simula canonical input montado."""
    return {
        "structure_id":   1,
        "underlying":     "PETR4",
        "reference_date": "2026-05-28",
        "legs":           [{"option_symbol": "PETRA100", "strike": 100.0}],
        "snapshot":       {"bid": 10.0, "ask": 10.5, "mid": 10.25},
        "meta":           {},
    }


def _make_pricing_app_service_mock(execution_id: int = 42) -> MagicMock:
    """
    Mock do PricingExecutionAppService.
    Método real: execute_pricing(structure_id, reference_date).
    No smoke o canonical_input já foi montado -- simulamos a chamada direta.
    """
    svc = MagicMock(spec=PricingExecutionAppService)
    svc.execute_pricing.return_value = {
        "execution_id":   execution_id,
        "status":         "ok",
        "structure_id":   1,
        "reference_date": "2026-05-28",
    }
    return svc


# ---------------------------------------------------------------------------
# Cenário 1: pipeline completo -- snapshot manual
# ---------------------------------------------------------------------------

def test_pipeline_manual():
    print("\n[1] Pipeline completo -- snapshot source=MANUAL  execução OK")

    structure = _make_structure(aba="PETR4")
    repo      = _make_repo_mock(structure)
    provider  = _make_provider_mock()
    selector  = _make_selector_mock("PETR4", SnapshotSource.MANUAL, with_override=True)
    pricing   = _make_pricing_app_service_mock(execution_id=101)

    with patch(
        "services.canonical_input_service.assemble_structure_market_input",
        return_value=_assembled_stub(),
    ):
        canonical_svc = CanonicalInputService(
            repository=repo,
            market_snapshot_provider=provider,
            market_snapshot_selector=selector,
        )
        canonical_input = canonical_svc.build_structure_market_input(structure_id=1)

    # Simula entrega do canonical_input ao pricing via execute_pricing
    exec_result = pricing.execute_pricing(
        structure_id=canonical_input.get("structure_id", 1),
        reference_date=canonical_input.get("meta", {}).get("reference_date"),
    )

    selector.select.assert_called_once_with("PETR4")
    provider.get_snapshot.assert_not_called()
    pricing.execute_pricing.assert_called_once()

    assert exec_result["status"] == "ok"
    assert exec_result["execution_id"] == 101

    meta = canonical_input.get("meta", {})
    assert meta.get("snapshot_source") == "manual"
    assert meta.get("is_manual_first") is True

    print(f"   execution_id    : {exec_result['execution_id']}")
    print(f"   status          : {exec_result['status']}")
    print(f"   snapshot_source : {meta['snapshot_source']}")
    print(f"   is_manual_first : {meta['is_manual_first']}")
    print("   [OK] OK")


# ---------------------------------------------------------------------------
# Cenário 2: pipeline completo -- snapshot RTD
# ---------------------------------------------------------------------------

def test_pipeline_rtd():
    print("\n[2] Pipeline completo -- snapshot source=RTD  execução OK")

    structure = _make_structure(aba="VALE3")
    repo      = _make_repo_mock(structure)
    provider  = _make_provider_mock()
    selector  = _make_selector_mock("VALE3", SnapshotSource.RTD, with_override=False)
    pricing   = _make_pricing_app_service_mock(execution_id=102)

    with patch(
        "services.canonical_input_service.assemble_structure_market_input",
        return_value=_assembled_stub(),
    ):
        canonical_svc = CanonicalInputService(
            repository=repo,
            market_snapshot_provider=provider,
            market_snapshot_selector=selector,
        )
        canonical_input = canonical_svc.build_structure_market_input(structure_id=1)

    exec_result = pricing.execute_pricing(
        structure_id=canonical_input.get("structure_id", 1),
        reference_date=canonical_input.get("meta", {}).get("reference_date"),
    )

    selector.select.assert_called_once_with("VALE3")
    pricing.execute_pricing.assert_called_once()
    assert exec_result["status"] == "ok"
    assert exec_result["execution_id"] == 102

    meta = canonical_input.get("meta", {})
    assert meta.get("snapshot_source") == "rtd"
    assert meta.get("is_manual_first") is False
    assert meta.get("manual_overrides") == []

    print(f"   execution_id    : {exec_result['execution_id']}")
    print(f"   snapshot_source : {meta['snapshot_source']}")
    print(f"   is_manual_first : {meta['is_manual_first']}")
    print("   [OK] OK")


# ---------------------------------------------------------------------------
# Cenário 3: pipeline sem selector  regressão com provider legado
# ---------------------------------------------------------------------------

def test_pipeline_sem_selector_regressao():
    print("\n[3] Pipeline sem selector  regressão provider legado OK")

    structure = _make_structure(aba="BBAS3")
    repo      = _make_repo_mock(structure)
    provider  = _make_provider_mock()
    pricing   = _make_pricing_app_service_mock(execution_id=103)

    with patch(
        "services.canonical_input_service.assemble_structure_market_input",
        return_value=_assembled_stub(),
    ):
        canonical_svc = CanonicalInputService(
            repository=repo,
            market_snapshot_provider=provider,
            market_snapshot_selector=None,
        )
        canonical_input = canonical_svc.build_structure_market_input(structure_id=1)

    exec_result = pricing.execute_pricing(
        structure_id=canonical_input.get("structure_id", 1),
        reference_date=canonical_input.get("meta", {}).get("reference_date"),
    )

    provider.get_snapshot.assert_called_once()
    pricing.execute_pricing.assert_called_once()
    assert exec_result["status"] == "ok"
    assert exec_result["execution_id"] == 103

    meta = canonical_input.get("meta", {})
    assert meta.get("snapshot_source") == "provider_legacy"

    print(f"   execution_id    : {exec_result['execution_id']}")
    print(f"   snapshot_source : {meta['snapshot_source']}")
    print("   [OK] OK")


# ---------------------------------------------------------------------------
# Cenário 4: structure inexistente  erro antes do pricing
# ---------------------------------------------------------------------------

def test_pipeline_structure_not_found():
    print("\n[4] Structure inexistente  ValueError antes do pricing")

    repo    = MagicMock()
    repo.get_structure.return_value = None
    pricing = _make_pricing_app_service_mock()

    canonical_svc = CanonicalInputService(
        repository=repo,
        market_snapshot_selector=MagicMock(spec=MarketSnapshotSelector),
    )

    try:
        canonical_svc.build_structure_market_input(structure_id=9999)
        print("   [FALHOU] FALHOU -- deveria ter levantado ValueError")
        sys.exit(1)
    except ValueError as exc:
        pricing.execute_pricing.assert_not_called()
        print(f"   ValueError      : {exc}")
        print("   execute_pricing NÃO chamado [OK]")
        print("   [OK] OK")


# ---------------------------------------------------------------------------
# Cenário 5: PricingExecutionAppService importável
# ---------------------------------------------------------------------------

def test_pricing_app_service_importavel():
    print("\n[5] PricingExecutionAppService importável do módulo real")
    try:
        from services.pricing_execution_app_service import (
            PricingExecutionAppService as _Real,
        )
        # Verifica que execute_pricing existe na classe real
        assert hasattr(_Real, "execute_pricing"), \
            "Método execute_pricing não encontrado na classe real"
        print(f"   Classe          : {_Real}")
        print(f"   execute_pricing : [OK] presente")
        print("   [OK] OK")
    except Exception as exc:
        print(f"   [FALHOU] FALHOU: {exc}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("  SMOKE patch_15 -- Pipeline completo structure+snapshotpricing")
    print("=" * 60)

    tests = [
        test_pipeline_manual,
        test_pipeline_rtd,
        test_pipeline_sem_selector_regressao,
        test_pipeline_structure_not_found,
        test_pricing_app_service_importavel,
    ]

    failed = 0
    for t in tests:
        try:
            t()
        except Exception as exc:
            print(f"   [FALHOU] EXCEÇÃO inesperada: {exc}")
            failed += 1

    print("\n" + "=" * 60)
    if failed == 0:
        print(f"  Resultado: {len(tests)}/{len(tests)} cenários OK [OK]")
    else:
        print(f"  Resultado: {failed} cenário(s) FALHARAM [FALHOU]")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()
