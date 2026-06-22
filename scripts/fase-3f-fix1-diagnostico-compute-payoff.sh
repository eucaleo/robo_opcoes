#!/usr/bin/env bash
set -u

EVID="docs/checkpoints/evidencias/fase-3f-fix1-diagnostico-compute-payoff.txt"
AUDIT="docs/checkpoints/auditoria-revisao-funcional-pos-uso-real.md"

mkdir -p docs/checkpoints/evidencias
mkdir -p scripts

{
  echo "============================================================"
  echo "FASE 3F FIX1 - DIAGNOSTICO COMPUTE PAYOFF"
  echo "Data:"
  date
  echo "Branch:"
  git branch --show-current
  echo "Commit atual:"
  git rev-parse --short HEAD
  echo "============================================================"
  echo

  echo "== Status git =="
  git status --short
  echo

  echo "== Arquivo domain/payoff.py =="
  sed -n '1,420p' domain/payoff.py
  echo

  echo "== Arquivo services/derived_service.py =="
  sed -n '1,520p' services/derived_service.py
  echo

  echo "== Execucao isolada: pricing_payload -> canonical_input -> compute_payoff =="
  python - <<'PY'
from pathlib import Path
import json
import traceback

try:
    from services.pricing_input_service import PricingInputService
    from services.derived_payoff_persistence import DerivedPayoffPersistence
    from domain.payoff import compute_payoff_from_canonical_input

    service = PricingInputService(db_path=Path("dados/app.db"))
    payload = service.build_pricing_payload(structure_id=2)

    print("PAYLOAD_KEYS:", sorted(payload.keys()))
    print("PAYLOAD:")
    print(json.dumps(payload, ensure_ascii=False, default=str, indent=2))

    canonical_input = DerivedPayoffPersistence._build_canonical_input(
        pricing_payload=payload,
        result={
            "engine": "stub",
            "status": "ok",
            "structure_id": 2,
            "metrics": {},
            "valuation": {},
        },
    )

    print()
    print("CANONICAL_INPUT_KEYS:", sorted(canonical_input.keys()))
    print("CANONICAL_INPUT:")
    print(json.dumps(canonical_input, ensure_ascii=False, default=str, indent=2))

    payoff = compute_payoff_from_canonical_input(canonical_input)

    print()
    print("PAYOFF_TYPE:", type(payoff).__name__)
    if isinstance(payoff, dict):
        print("PAYOFF_KEYS:", sorted(payoff.keys()))
        for key, value in payoff.items():
            if isinstance(value, list):
                print(f"{key}: list len={len(value)}")
                print(json.dumps(value[:10], ensure_ascii=False, default=str, indent=2))
            elif isinstance(value, dict):
                print(f"{key}: dict keys={sorted(value.keys())}")
                print(json.dumps(value, ensure_ascii=False, default=str, indent=2)[:4000])
            else:
                print(f"{key}: {value!r}")
    else:
        print(repr(payoff))

except Exception:
    traceback.print_exc()
PY
  echo

  echo "== Execucao isolada: DerivedPayoffPersistence.persist() =="
  python - <<'PY'
from pathlib import Path
import sqlite3
import traceback

try:
    from services.pricing_input_service import PricingInputService
    from services.derived_payoff_persistence import DerivedPayoffPersistence

    service = PricingInputService(db_path=Path("dados/app.db"))
    payload = service.build_pricing_payload(structure_id=2)

    before = None
    conn = sqlite3.connect("dados/derived.db")
    before = conn.execute(
        "select count(*) from payoff_curve_points where structure_id=?",
        (2,),
    ).fetchone()[0]
    conn.close()

    print("Antes payoff_curve_points structure_id=2:", before)

    port = DerivedPayoffPersistence()
    result = {
        "engine": "stub",
        "status": "ok",
        "structure_id": 2,
        "metrics": {
            "number_of_legs": len(payload.get("legs") or []),
            "spot_price": payload.get("spot_price"),
        },
        "valuation": {
            "theoretical_value": 0.0,
        },
    }

    ret = port.persist(pricing_payload=payload, result=result)
    print("Retorno persist:", ret)

    conn = sqlite3.connect("dados/derived.db")
    after = conn.execute(
        "select count(*) from payoff_curve_points where structure_id=?",
        (2,),
    ).fetchone()[0]
    decisions = conn.execute(
        "select count(*) from structure_decisions where structure_id=?",
        (2,),
    ).fetchone()[0]
    conn.close()

    print("Depois payoff_curve_points structure_id=2:", after)
    print("Depois structure_decisions structure_id=2:", decisions)

except Exception:
    traceback.print_exc()
PY
  echo

  echo "============================================================"
  echo "FIM DIAGNOSTICO COMPUTE PAYOFF"
  echo "============================================================"

} > "$EVID" 2>&1

cat >> "$AUDIT" <<MD

## Fase 3F Fix1 - Diagnostico compute payoff

Data: $(date)

Branch: $(git branch --show-current)

Commit base: $(git rev-parse --short HEAD)

Objetivo:
Executar isoladamente PricingInputService, DerivedPayoffPersistence._build_canonical_input(),
compute_payoff_from_canonical_input() e DerivedPayoffPersistence.persist() para identificar
onde a geração/persistência do payoff falha.

Evidencia gerada:
docs/checkpoints/evidencias/fase-3f-fix1-diagnostico-compute-payoff.txt

Status:
Diagnostico executado. Proxima etapa: patch corretivo no contrato de payoff.

MD

echo "Diagnostico compute payoff gerado em:"
echo "$EVID"
echo
echo "Auditoria atualizada em:"
echo "$AUDIT"
