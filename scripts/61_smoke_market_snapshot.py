# scripts/61_smoke_market_snapshot.py
"""
Smoke test - patch_12 (MarketSnapshot) + patch_13 (Selector).
Uso: python scripts/61_smoke_market_snapshot.py
"""
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DB_PATH = PROJECT_ROOT / "dados" / "app.db"

# --- helpers -----------------------------------------------------------------

def ok(msg):     print(f"  [OK]  {msg}")
def info(msg):   print(f"  [--]  {msg}")
def header(msg): print(f"\n-- {msg} --")


# --- testes ------------------------------------------------------------------

def smoke_domain():
    header("domain/market_snapshot.py")

    from domain.market_snapshot import (
        LegMarketSnapshot, SnapshotSource, StructureMarketSnapshot
    )

    leg = LegMarketSnapshot(
        aba             = "C1",
        ativo           = "EMBJE868",
        cv              = "C",
        call_put        = "CALL",
        quant           = 7000.0,
        valor_executado = 1.38,
        bid             = 4.84,
        ask             = 4.93,
        mid             = round((4.84 + 4.93) / 2, 6),
        iv              = 37.78,
        delta           = 0.5909,
        gamma           = 0.039,
        theta           = 4.85,
        vega            = 10.2557,
        strike          = 86.81,
        vencimento      = "46157,125",
        dte             = 31.0,
        pl_realista     = 24220.0,
        timestamp       = "14/04/2026 17:55:51",
        source          = SnapshotSource.RTD,
    )
    assert leg.aba == "C1"
    assert leg.mid == round((4.84 + 4.93) / 2, 6)
    assert leg.source == SnapshotSource.RTD
    ok(f"LegMarketSnapshot criado: aba={leg.aba}, mid={leg.mid}, source={leg.source.value}")

    leg_manual = LegMarketSnapshot(
        aba    = "P1",
        ativo  = "BOVAE195",
        bid    = 5.69,
        ask    = 5.72,
        mid    = round((5.69 + 5.72) / 2, 6),
        source = SnapshotSource.MANUAL,
    )
    assert leg_manual.source == SnapshotSource.MANUAL
    ok(f"LegMarketSnapshot MANUAL criado: aba={leg_manual.aba}, source={leg_manual.source.value}")

    snap = StructureMarketSnapshot(
        aba        = "EMBJ3",
        legs       = [leg, leg_manual],
        source     = SnapshotSource.RTD,
        spot       = 87.37,
        num_pernas = 4,
        dte_min    = 31,
    )
    assert snap.num_legs == 2
    assert snap.has_summary
    ok(f"StructureMarketSnapshot criado: aba={snap.aba}, num_legs={snap.num_legs}, spot={snap.spot}")


def smoke_repository():
    header("repositories/market_snapshot_repository.py")

    from repositories.market_snapshot_repository import MarketSnapshotRepository

    repo = MarketSnapshotRepository(DB_PATH)
    ok(f"Repositorio instanciado: {DB_PATH.name}")

    TEST_ABA = "EMBJ3"

    rtd_legs = repo.get_rtd_legs(TEST_ABA)
    ok(f"get_rtd_legs('{TEST_ABA}') -> {len(rtd_legs)} leg(s)")
    if rtd_legs:
        l = rtd_legs[0]
        ok(f"  primeira leg: ativo={l.ativo}, bid={l.bid}, ask={l.ask}, mid={l.mid}, delta={l.delta}")

    manual_legs = repo.get_manual_legs(TEST_ABA)
    ok(f"get_manual_legs('{TEST_ABA}') -> {len(manual_legs)} leg(s)")

    summary = repo.get_rtd_summary(TEST_ABA)
    if summary:
        ok(f"get_rtd_summary('{TEST_ABA}') -> spot={summary.get('spot')}, num_pernas={summary.get('num_pernas')}")
    else:
        info(f"get_rtd_summary('{TEST_ABA}') -> None (sem dados)")

    snap = repo.get_structure(TEST_ABA)
    ok(f"get_structure('{TEST_ABA}') -> {snap.num_legs} leg(s), spot={snap.spot}, alertas={snap.alertas_v2!r}")


def smoke_selector():
    header("services/market_snapshot_selector.py")

    from repositories.market_snapshot_repository import MarketSnapshotRepository
    from services.market_snapshot_selector import MarketSnapshotSelector

    repo     = MarketSnapshotRepository(DB_PATH)
    selector = MarketSnapshotSelector(repo)
    ok("Selector instanciado")

    TEST_ABA = "EMBJ3"
    result = selector.select(TEST_ABA)
    ok(f"select('{TEST_ABA}') -> source={result.source.value}, num_legs={len(result.legs)}")
    ok(f"  manual_overrides : {result.manual_overrides}")
    ok(f"  is_manual_first  : {result.is_manual_first}")


# --- main --------------------------------------------------------------------

def main():
    print("\nSmoke - patch_12 + patch_13\n")
    try:
        smoke_domain()
        smoke_repository()
        smoke_selector()
        print("\n[PASSOU] Todos os smokes passaram.\n")
    except Exception as e:
        print(f"\n[FALHOU] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
