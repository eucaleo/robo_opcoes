# scripts/67_smoke_patch18_app_service.py
"""
patch_18 | smoke: PricingExecutionAppService.execute_pricing() via fachada canônica
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from services.pricing_execution_app_service import PricingExecutionAppService

STRUCTURE_ID = 1
SEP = "=" * 65

def check(label: str, condition: bool, detail: str = "") -> bool:
    mark = "✅ PASS" if condition else "❌ FAIL"
    print(f"{mark}  {label}")
    if detail:
        print(f"        {detail}")
    return condition

def main() -> None:
    print(SEP)
    print("patch_18 | smoke: PricingExecutionAppService via fachada")
    print(SEP)

    svc = PricingExecutionAppService()
    results = []

    # S1 — execute_pricing retorna dict
    try:
        record = svc.execute_pricing(structure_id=STRUCTURE_ID)
        results.append(check("S1 execute_pricing retorna dict", isinstance(record, dict),
                              f"keys={list(record.keys())}"))
    except Exception as exc:
        results.append(check("S1 execute_pricing retorna dict", False, str(exc)))
        record = {}

    # S2 — execution_status presente e = 'ok'
    status = record.get("execution_status")
    results.append(check("S2 execution_status='ok'", status == "ok",
                          f"execution_status={status!r}"))

    # S3 — execution_engine presente
    engine = record.get("execution_engine")
    results.append(check("S3 execution_engine gravado", engine is not None,
                          f"execution_engine={engine!r}"))

    # S4 — structure_id correto
    sid = record.get("structure_id")
    results.append(check("S4 structure_id correto", sid == STRUCTURE_ID,
                          f"structure_id={sid}"))

    # S5 — number_of_legs gravado
    nol = record.get("number_of_legs")
    results.append(check("S5 number_of_legs gravado", nol is not None,
                          f"number_of_legs={nol}"))

    # S6 — structure_id inválido levanta ValueError
    try:
        svc.execute_pricing(structure_id=0)
        results.append(check("S6 structure_id=0 levanta ValueError", False,
                              "nenhuma exceção levantada"))
    except ValueError as exc:
        results.append(check("S6 structure_id=0 levanta ValueError", True, str(exc)))

    # S7 — reference_date inválida levanta ValueError
    try:
        svc.execute_pricing(structure_id=STRUCTURE_ID, reference_date="28/05/2026")
        results.append(check("S7 reference_date inválida levanta ValueError", False,
                              "nenhuma exceção levantada"))
    except ValueError as exc:
        results.append(check("S7 reference_date inválida levanta ValueError", True, str(exc)))

    # S8 — structure_id inexistente levanta ValueError
    try:
        svc.execute_pricing(structure_id=999999)
        results.append(check("S8 structure inexistente levanta ValueError", False,
                              "nenhuma exceção levantada"))
    except ValueError as exc:
        results.append(check("S8 structure inexistente levanta ValueError", True, str(exc)))

    total = len(results)
    passed = sum(results)
    print(SEP)
    print(f"Resultado: {passed}/{total} OK")
    print(SEP)
    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()
