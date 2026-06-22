#!/usr/bin/env bash
set -u

EVID="docs/checkpoints/evidencias/fase-3f-fix1-diagnostico-compute-payoff-v2.txt"
AUDIT="docs/checkpoints/auditoria-revisao-funcional-pos-uso-real.md"

mkdir -p docs/checkpoints/evidencias
mkdir -p scripts

{
  echo "============================================================"
  echo "FASE 3F FIX1 - DIAGNOSTICO COMPUTE PAYOFF V2"
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

  echo "== Trechos essenciais domain/payoff.py =="
  grep -n "def validate_canonical_input\|def _compute_leg_payoff_at_expiration\|def compute_payoff_curve_from_canonical_legs\|def compute_payoff_from_canonical_input" domain/payoff.py || true
  echo
  sed -n '1,230p' domain/payoff.py
  echo

  echo "== Trechos essenciais services/derived_service.py =="
  grep -n "def insert_payoff_points\|def save_payoff_curve\|def save_payoff_from_canonical_payload\|def save_decision_from_canonical_payload" services/derived_service.py || true
  echo
  sed -n '357,470p' services/derived_service.py
  echo
  sed -n '470,560p' services/derived_service.py
  echo

  echo "== Execucao isolada corrigida: pricing_payload -> canonical_input -> compute_payoff =="
  python - <<'PY'
from pathlib import Path
import json
import traceback

def make_pricing_input_service():
    from services.pricing_input_service import PricingInputService

    try:
        return PricingInputService(db_path=Path("dados/app.db"))
    except TypeError:
        return PricingInputService()

def build_payload(service, structure_id):
    try:
        return service.build_pricing_payload(
            structure_id=structure_id,
            reference_date="2026-06-21",
        )
    except TypeError:
        return service.build_pricing_payload(structure_id=structure_id)

try:
    from services.derived_payoff_persistence import DerivedPayoffPersistence
    from domain.payoff import compute_payoff_from_canonical_input, validate_canonical_input

    service = make_pricing_input_service()
    payload = build_payload(service, 2)

    print("PAYLOAD_KEYS:", sorted(payload.keys()))
    print("PAYLOAD_LEGS_COUNT:", len(payload.get("legs") or []))
    print("PAYLOAD_LEGS:")
    print(json.dumps(payload.get("legs") or [], ensure_ascii=False, default=str, indent=2))

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
    print("CANONICAL_INPUT:")
    print(json.dumps(canonical_input, ensure_ascii=False, default=str, indent=2))

    print()
    print("VALIDATION_ERRORS:")
    print(json.dumps(validate_canonical_input(canonical_input), ensure_ascii=False, default=str, indent=2))

    payoff = compute_payoff_from_canonical_input(canonical_input)

    print()
    print("PAYOFF_TYPE:", type(payoff).__name__)
    if isinstance(payoff, dict):
        print("PAYOFF_KEYS:", sorted(payoff.keys()))
        print("PAYOFF_POINTS_LEN:", len(payoff.get("points") or []))
        print("PAYOFF_META:")
        print(json.dumps(payoff.get("meta"), ensure_ascii=False, default=str, indent=2))
        print("PAYOFF_FIRST_POINTS:")
        print(json.dumps((payoff.get("points") or [])[:10], ensure_ascii=False, default=str, indent=2))
        print("PAYOFF_SUMMARY:")
        print(json.dumps({
            "structure_id": payoff.get("structure_id"),
            "structure_name": payoff.get("structure_name"),
            "underlying_asset": payoff.get("underlying_asset"),
            "spot_ref": payoff.get("spot_ref"),
            "pl_min": payoff.get("pl_min"),
            "pl_max": payoff.get("pl_max"),
        }, ensure_ascii=False, default=str, indent=2))
    else:
        print(repr(payoff))

except Exception:
    traceback.print_exc()
PY
  echo

  echo "== Execucao isolada corrigida: DerivedPayoffPersistence.persist() =="
  python - <<'PY'
from pathlib import Path
import sqlite3
import traceback

def make_pricing_input_service():
    from services.pricing_input_service import PricingInputService

    try:
        return PricingInputService(db_path=Path("dados/app.db"))
    except TypeError:
        return PricingInputService()

def build_payload(service, structure_id):
    try:
        return service.build_pricing_payload(
            structure_id=structure_id,
            reference_date="2026-06-21",
        )
    except TypeError:
        return service.build_pricing_payload(structure_id=structure_id)

try:
    from services.derived_payoff_persistence import DerivedPayoffPersistence

    service = make_pricing_input_service()
    payload = build_payload(service, 2)

    conn = sqlite3.connect("dados/derived.db")
    before_payoff = conn.execute(
        "select count(*) from payoff_curve_points where structure_id=?",
        (2,),
    ).fetchone()[0]
    before_decisions = conn.execute(
        "select count(*) from structure_decisions where structure_id=?",
        (2,),
    ).fetchone()[0]
    conn.close()

    print("Antes payoff_curve_points structure_id=2:", before_payoff)
    print("Antes structure_decisions structure_id=2:", before_decisions)

    port = DerivedPayoffPersistence()
    result = {
        "engine": "stub",
        "status": "ok",
        "structure_id": 2,
        "underlying_asset": payload.get("underlying_asset"),
        "reference_date": payload.get("reference_date"),
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
    after_payoff = conn.execute(
        "select count(*) from payoff_curve_points where structure_id=?",
        (2,),
    ).fetchone()[0]
    after_decisions = conn.execute(
        "select count(*) from structure_decisions where structure_id=?",
        (2,),
    ).fetchone()[0]

    print("Depois payoff_curve_points structure_id=2:", after_payoff)
    print("Depois structure_decisions structure_id=2:", after_decisions)

    print()
    print("Ultimos pontos structure_id=2:")
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        select timestamp, aba, structure_id, spot_ref, point_spot, point_pl, meta_json
          from payoff_curve_points
         where structure_id=?
         order by timestamp desc, point_spot asc
         limit 10
        """,
        (2,),
    ).fetchall()
    for row in rows:
        print(dict(row))

    print()
    print("Ultimas decisoes structure_id=2:")
    rows = conn.execute(
        """
        select id, timestamp, aba, decision, level, pl_atual, pl_max, spot_ref, structure_id, meta_json, why
          from structure_decisions
         where structure_id=?
         order by id desc
         limit 5
        """,
        (2,),
    ).fetchall()
    for row in rows:
        print(dict(row))

    conn.close()

except Exception:
    traceback.print_exc()
PY
  echo

  echo "============================================================"
  echo "FIM DIAGNOSTICO COMPUTE PAYOFF V2"
  echo "============================================================"

} > "$EVID" 2>&1

cat >> "$AUDIT" <<MD

## Fase 3F Fix1 - Diagnostico compute payoff V2

Data: $(date)

Branch: $(git branch --show-current)

Commit base: $(git rev-parse --short HEAD)

Objetivo:
Reexecutar o diagnostico isolado usando fallback de construtor do PricingInputService,
igual ao comportamento da CanonicalPricingFacade.

Evidencia gerada:
docs/checkpoints/evidencias/fase-3f-fix1-diagnostico-compute-payoff-v2.txt

Status:
Diagnostico V2 executado. Proxima etapa: patch corretivo no contrato de payoff, se necessario.

MD

echo "Diagnostico compute payoff V2 gerado em:"
echo "$EVID"
echo
echo "Auditoria atualizada em:"
echo "$AUDIT"
