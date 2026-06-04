# scripts/63_smoke_canonical_with_snapshot.py
"""
patch_14 -- Smoke: CanonicalInputService consome MarketSnapshotSelector.

Cenários cobertos:
  1. Selector injetado + aba presente  snapshot via selector (manual>rtd)
  2. Selector injetado + aba ausente   fallback para provider legado
  3. Selector NÃO injetado            comportamento original (provider legado)
  4. Fonte RTD (sem manual override)
  5. structure_id inválido            ValueError
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

# ---------------------------------------------------------------------------
# Helpers de mock
# ---------------------------------------------------------------------------

def _make_structure(structure_id: int = 1, aba: str | None = "PETR4") -> dict:
    return {
        "id":               structure_id,
        "name":             "Teste Smoke",
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


def _make_selector_result(
    aba: str,
    source: SnapshotSource = SnapshotSource.MANUAL,
    with_override: bool = False,
) -> SnapshotSelectionResult:
    legs = [_make_leg_snapshot(aba=aba, ativo="PETRA100", source=source)]
    overrides = ["PETRA100"] if with_override else []
    return SnapshotSelectionResult(
        aba=aba,
        source=source,
        legs=legs,
        manual_overrides=overrides,
    )


def _make_mock_repository(structure: dict) -> MagicMock:
    repo = MagicMock()
    repo.get_structure.return_value = structure
    return repo


def _make_mock_provider() -> MagicMock:
    provider = MagicMock()
    provider.get_snapshot.return_value = {
        "aba":            "PETR4",
        "legs":           [],
        "reference_date": "2026-05-28",
    }
    return provider


def _make_mock_selector(result: SnapshotSelectionResult) -> MagicMock:
    selector = MagicMock(spec=MarketSnapshotSelector)
    selector.select.return_value = result
    return selector


def _make_assembler_patch(assembled_value: dict):
    """Patch do assembler para isolar o teste do canonical_input_service."""
    return patch(
        "services.canonical_input_service.assemble_structure_market_input",
        return_value=assembled_value,
    )


# ---------------------------------------------------------------------------
# Cenário 1: selector injetado + aba presente  snapshot via selector
# ---------------------------------------------------------------------------

def test_cenario_1_selector_com_aba():
    print("\n[1] Selector injetado + aba presente  snapshot via selector (manual>rtd)")

    structure  = _make_structure(aba="PETR4")
    sel_result = _make_selector_result("PETR4", SnapshotSource.MANUAL, with_override=True)

    repo     = _make_mock_repository(structure)
    provider = _make_mock_provider()
    selector = _make_mock_selector(sel_result)

    assembled_stub = {"inputs": {}, "meta": {"assembler": True}}

    with _make_assembler_patch(assembled_stub):
        svc = CanonicalInputService(
            repository=repo,
            market_snapshot_provider=provider,
            market_snapshot_selector=selector,
        )
        result = svc.build_structure_market_input(structure_id=1)

    selector.select.assert_called_once_with("PETR4")
    provider.get_snapshot.assert_not_called()

    meta = result.get("meta", {})
    assert meta.get("snapshot_source") == "manual", \
        f"Esperado 'manual', obtido: {meta.get('snapshot_source')}"
    assert meta.get("is_manual_first") is True, \
        "is_manual_first deveria ser True"
    assert len(meta.get("manual_overrides", [])) > 0, \
        "manual_overrides deveria ser não-vazio"

    print(f"   snapshot_source  : {meta['snapshot_source']}")
    print(f"   is_manual_first  : {meta['is_manual_first']}")
    print(f"   manual_overrides : {meta['manual_overrides']}")
    print("   [OK] OK")


# ---------------------------------------------------------------------------
# Cenário 2: selector injetado + aba AUSENTE  fallback para provider legado
# ---------------------------------------------------------------------------

def test_cenario_2_selector_sem_aba():
    print("\n[2] Selector injetado + aba ausente  fallback para provider legado")

    structure = _make_structure(aba=None)

    repo     = _make_mock_repository(structure)
    provider = _make_mock_provider()
    selector = MagicMock(spec=MarketSnapshotSelector)

    assembled_stub = {"inputs": {}, "meta": {}}

    with _make_assembler_patch(assembled_stub):
        svc = CanonicalInputService(
            repository=repo,
            market_snapshot_provider=provider,
            market_snapshot_selector=selector,
        )
        result = svc.build_structure_market_input(structure_id=1)

    selector.select.assert_not_called()
    provider.get_snapshot.assert_called_once()

    meta = result.get("meta", {})
    assert meta.get("snapshot_source") == "provider_legacy", \
        f"Esperado 'provider_legacy', obtido: {meta.get('snapshot_source')}"

    print(f"   snapshot_source : {meta['snapshot_source']}")
    print("   [OK] OK")


# ---------------------------------------------------------------------------
# Cenário 3: selector NÃO injetado  comportamento original
# ---------------------------------------------------------------------------

def test_cenario_3_sem_selector():
    print("\n[3] Selector NÃO injetado  comportamento original (provider legado)")

    structure = _make_structure(aba="PETR4")

    repo     = _make_mock_repository(structure)
    provider = _make_mock_provider()

    assembled_stub = {"inputs": {}, "meta": {}}

    with _make_assembler_patch(assembled_stub):
        svc = CanonicalInputService(
            repository=repo,
            market_snapshot_provider=provider,
            market_snapshot_selector=None,
        )
        result = svc.build_structure_market_input(structure_id=1)

    provider.get_snapshot.assert_called_once()

    meta = result.get("meta", {})
    assert meta.get("snapshot_source") == "provider_legacy", \
        f"Esperado 'provider_legacy', obtido: {meta.get('snapshot_source')}"

    print(f"   snapshot_source : {meta['snapshot_source']}")
    print("   [OK] OK")


# ---------------------------------------------------------------------------
# Cenário 4: fonte RTD (sem manual override)
# ---------------------------------------------------------------------------

def test_cenario_4_selector_fonte_rtd():
    print("\n[4] Selector injetado + fonte RTD (sem manual override)")

    structure  = _make_structure(aba="VALE3")
    sel_result = _make_selector_result("VALE3", SnapshotSource.RTD, with_override=False)

    repo     = _make_mock_repository(structure)
    provider = _make_mock_provider()
    selector = _make_mock_selector(sel_result)

    assembled_stub = {"inputs": {}, "meta": {}}

    with _make_assembler_patch(assembled_stub):
        svc = CanonicalInputService(
            repository=repo,
            market_snapshot_provider=provider,
            market_snapshot_selector=selector,
        )
        result = svc.build_structure_market_input(structure_id=1)

    meta = result.get("meta", {})
    assert meta.get("snapshot_source") == "rtd", \
        f"Esperado 'rtd', obtido: {meta.get('snapshot_source')}"
    assert meta.get("is_manual_first") is False, \
        "is_manual_first deveria ser False"
    assert meta.get("manual_overrides") == [], \
        "manual_overrides deveria ser vazio"

    print(f"   snapshot_source  : {meta['snapshot_source']}")
    print(f"   is_manual_first  : {meta['is_manual_first']}")
    print(f"   manual_overrides : {meta['manual_overrides']}")
    print("   [OK] OK")


# ---------------------------------------------------------------------------
# Cenário 5: structure not found
# ---------------------------------------------------------------------------

def test_cenario_5_structure_not_found():
    print("\n[5] structure_id inválido  ValueError")

    repo = MagicMock()
    repo.get_structure.return_value = None

    svc = CanonicalInputService(
        repository=repo,
        market_snapshot_selector=MagicMock(spec=MarketSnapshotSelector),
    )

    try:
        svc.build_structure_market_input(structure_id=9999)
        print("   [FALHOU] FALHOU -- deveria ter levantado ValueError")
        sys.exit(1)
    except ValueError as exc:
        print(f"   ValueError: {exc}")
        print("   [OK] OK")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("  SMOKE patch_14 -- CanonicalInputService + MarketSnapshotSelector")
    print("=" * 60)

    tests = [
        test_cenario_1_selector_com_aba,
        test_cenario_2_selector_sem_aba,
        test_cenario_3_sem_selector,
        test_cenario_4_selector_fonte_rtd,
        test_cenario_5_structure_not_found,
    ]

    failed = 0
    for t in tests:
        try:
            t()
        except Exception as exc:
            print(f"   [FALHOU] EXCEÇÃO: {exc}")
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
