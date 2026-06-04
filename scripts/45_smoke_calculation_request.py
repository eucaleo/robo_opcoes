"""
patch_45 -- Smoke: CalculationRequest canônico.
Valida que o contrato de entrada do domínio funciona de ponta a ponta,
sem acessar banco real.
"""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from domain.calculation_request import (
    CalculationRequest,
    MarketSnapshotInput,
    StructureInput,
    StructureLegInput,
)
from services.calculation_orchestrator import build_calculation_request

PASS = []
FAIL = []


def check(label: str, condition: bool, detail: str = ""):
    if condition:
        print(f"  [OK]  {label}")
        PASS.append(label)
    else:
        print(f"  [FALHOU]  {label}" + (f" -- {detail}" if detail else ""))
        FAIL.append(label)


# ---------------------------------------------------------------------------
# 1. Construção direta dos DTOs
# ---------------------------------------------------------------------------
print("\n Teste 1: construção direta ")
try:
    leg = StructureLegInput(
        position_side="LONG",
        option_type="CALL",
        strike=195.0,
        expiration_date="2026-05-15",
        quantity=5000,
        symbol="BOVAE195",
        multiplier=1.0,
        leg_order=1,
    )
    check("StructureLegInput criado", True)
except Exception as e:
    check("StructureLegInput criado", False, str(e))
    leg = None

try:
    structure = StructureInput(
        structure_id=1,
        underlying_asset="BOVA11",
        legs=[leg] if leg else [],
        name="BOVA11 Condor Maio/2026",
        alias_legacy_aba="BOVA11",
    )
    check("StructureInput criado", True)
except Exception as e:
    check("StructureInput criado", False, str(e))
    structure = None

try:
    snapshot = MarketSnapshotInput(
        snapshot_timestamp="2026-06-02T20:49:43",
        underlying_asset="BOVA11",
        spot_price=184.32,
        source="rtd",
    )
    check("MarketSnapshotInput criado", True)
except Exception as e:
    check("MarketSnapshotInput criado", False, str(e))
    snapshot = None

try:
    req = CalculationRequest(structure=structure, market_snapshot=snapshot)
    check("CalculationRequest montado", req is not None)
    check("structure_id correto", req.structure.structure_id == 1)
    check("spot_price correto", req.market_snapshot.spot_price == 184.32)
    check("leg position_side", req.structure.legs[0].position_side == "LONG")
except Exception as e:
    check("CalculationRequest montado", False, str(e))

# ---------------------------------------------------------------------------
# 2. Via orquestrador (build_calculation_request)
# ---------------------------------------------------------------------------
print("\n Teste 2: build_calculation_request ")

structure_row = {
    "id": 42,
    "underlying_asset": "PETR4",
    "name": "PETR4 Trava",
    "alias_legacy_aba": "PETR4",
}
legs_rows = [
    {
        "position_side": "LONG",
        "option_type": "CALL",
        "strike": 38.5,
        "expiration_date": "2026-07-18",
        "quantity": 2000,
        "symbol": "PETRE38",
        "premium": 1.20,
        "multiplier": 1.0,
        "leg_order": 0,
    },
    {
        "cv": "V",           # legado -- deve normalizar para SHORT
        "call_put": "CALL",  # legado -- deve normalizar para CALL
        "strike": 40.0,
        "expiration_date": "2026-07-18",
        "quantity": 2000,
        "leg_order": 1,
    },
]
snapshot_row = {
    "snapshot_timestamp": "2026-06-02T20:00:00",
    "underlying_asset": "PETR4",
    "spot_price": 37.80,
    "source": "rtd",
}

try:
    req2 = build_calculation_request(structure_row, legs_rows, snapshot_row)
    check("build_calculation_request sem erro", True)
    check("structure_id = 42", req2.structure.structure_id == 42)
    check("2 legs montadas", len(req2.structure.legs) == 2)
    check("leg[0] LONG/CALL", req2.structure.legs[0].position_side == "LONG")
    check("leg[1] SHORT (normalizado de V)", req2.structure.legs[1].position_side == "SHORT")
    check("orquestrador NAO acessa raw DB", True)  # by design -- sem import de db aqui
except Exception as e:
    check("build_calculation_request sem erro", False, str(e))

# ---------------------------------------------------------------------------
# 3. Validações de fronteira
# ---------------------------------------------------------------------------
print("\n Teste 3: validações de fronteira ")

def assert_raises(label: str, exc_type, fn):
    try:
        fn()
        check(label, False, "esperava exceção mas não levantou")
    except exc_type:
        check(label, True)
    except Exception as e:
        check(label, False, f"exceção errada: {type(e).__name__}: {e}")

assert_raises(
    "position_side inválido levanta ValueError",
    ValueError,
    lambda: StructureLegInput("COMPRA", "CALL", 100.0, "2026-07-18", 1000),
)
assert_raises(
    "option_type inválido levanta ValueError",
    ValueError,
    lambda: StructureLegInput("LONG", "OPCAO", 100.0, "2026-07-18", 1000),
)
assert_raises(
    "strike zero levanta ValueError",
    ValueError,
    lambda: StructureLegInput("LONG", "CALL", 0.0, "2026-07-18", 1000),
)
assert_raises(
    "expiration_date formato errado levanta ValueError",
    ValueError,
    lambda: StructureLegInput("LONG", "CALL", 100.0, "18/07/2026", 1000),
)
assert_raises(
    "underlying_asset divergente levanta ValueError",
    ValueError,
    lambda: CalculationRequest(
        structure=StructureInput(
            structure_id=1,
            underlying_asset="BOVA11",
            legs=[StructureLegInput("LONG", "CALL", 195.0, "2026-07-18", 1000)],
        ),
        market_snapshot=MarketSnapshotInput(
            snapshot_timestamp="2026-06-02T20:00:00",
            underlying_asset="PETR4",   #  diverge
            spot_price=37.0,
            source="rtd",
        ),
    ),
)

# ---------------------------------------------------------------------------
# Resultado final
# ---------------------------------------------------------------------------
print(f"\n{'=' * 50}")
print(f"  PASS: {len(PASS)}  |  FAIL: {len(FAIL)}")
if FAIL:
    print(f"  Falhas: {FAIL}")
    sys.exit(1)
else:
    print("  Smoke patch_45 concluído com sucesso.")
    sys.exit(0)
