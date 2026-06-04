# scripts/66_smoke_patch17_persistence.py
"""
patch_17 -- Smoke: verificação de persistência real no JSON.

Cenários (8/8):
  S1  nova execução gravada no JSON        contador +1
  S2  persisted.record retornado           id presente na resposta
  S3  execution_status='ok' gravado        não None, não 'error'
  S4  number_of_legs gravado               não None
  S5  total_quantity gravado               não None
  S6  execution_engine='stub' gravado      valor correto
  S7  structure_id gravado                 bate com o input
  S8  execução erro  status='error'       gravado corretamente
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.canonical_pricing_facade import CanonicalPricingFacade
from repositories.pricing_executions_repository import PricingExecutionsRepository

#  Configuração 
VALID_STRUCTURE_ID   = 1
INVALID_STRUCTURE_ID = -99

PASS = "[OK] PASS"
FAIL = "[FALHOU] FAIL"

results: list[tuple[str, str, str]] = []


def check(label: str, condition: bool, detail: str = "") -> None:
    results.append((label, PASS if condition else FAIL, detail))


#  Instâncias 
facade = CanonicalPricingFacade()
repo   = PricingExecutionsRepository()

#  Execução válida 
executions_before = len(repo.list_executions())
response          = facade.execute_pricing(structure_id=VALID_STRUCTURE_ID)
executions_after  = len(repo.list_executions())
all_records       = repo.list_executions()
last_record       = all_records[-1]
persisted_record  = (response.get("persisted") or {}).get("record", {})

# S1 -- nova linha gravada
check(
    "S1 nova execução gravada no JSON",
    executions_after == executions_before + 1,
    f"antes={executions_before} depois={executions_after}",
)

# S2 -- persisted.record retornado na resposta
check(
    "S2 persisted.record retornado na resposta",
    bool(persisted_record) and persisted_record.get("id") is not None,
    f"id={persisted_record.get('id')}",
)

# S3 -- execution_status = "ok"
check(
    "S3 execution_status='ok' gravado",
    last_record.get("execution_status") == "ok",
    f"execution_status={last_record.get('execution_status')!r}",
)

# S4 -- number_of_legs não é None
check(
    "S4 number_of_legs gravado (não None)",
    last_record.get("number_of_legs") is not None,
    f"number_of_legs={last_record.get('number_of_legs')}",
)

# S5 -- total_quantity não é None
check(
    "S5 total_quantity gravado (não None)",
    last_record.get("total_quantity") is not None,
    f"total_quantity={last_record.get('total_quantity')}",
)

# S6 -- execution_engine = "stub"
check(
    "S6 execution_engine='stub' gravado",
    last_record.get("execution_engine") == "stub",
    f"execution_engine={last_record.get('execution_engine')!r}",
)

# S7 -- structure_id bate com o input
check(
    "S7 structure_id gravado corretamente",
    last_record.get("structure_id") == VALID_STRUCTURE_ID,
    f"structure_id={last_record.get('structure_id')}",
)

#  Execução com erro 
response_err = facade.execute_pricing(structure_id=INVALID_STRUCTURE_ID)
all_records  = repo.list_executions()
err_record   = all_records[-1]

# S8 -- erro  execution_status = "error"
check(
    "S8 execução com erro  execution_status='error' gravado",
    err_record.get("execution_status") == "error",
    f"execution_status={err_record.get('execution_status')!r}",
)

#  Relatório 
print("\n" + "=" * 65)
print("patch_17 | smoke: persistência real ponta a ponta")
print("=" * 65)

passed = 0
for label, status, detail in results:
    print(f"{status}  {label}")
    print(f"        {detail}")
    if status == PASS:
        passed += 1

total = len(results)
print("=" * 65)
print(f"Resultado: {passed}/{total} {'OK' if passed == total else 'FALHOU'}")
print("=" * 65)

sys.exit(0 if passed == total else 1)
