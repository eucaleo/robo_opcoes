#!/usr/bin/env bash
set -u

EVID="docs/checkpoints/evidencias/fase-3f-fix1-evidencia-final.txt"
AUDIT="docs/checkpoints/auditoria-revisao-funcional-pos-uso-real.md"

mkdir -p docs/checkpoints/evidencias

{
  echo "============================================================"
  echo "FASE 3F FIX1 - EVIDENCIA FINAL"
  echo "Data:"
  date
  echo "Branch:"
  git branch --show-current
  echo "Commit atual:"
  git rev-parse --short HEAD
  echo "============================================================"
  echo

  echo "== Git status =="
  git status --short
  echo

  echo "== Diff services/derived_payoff_persistence.py =="
  git diff -- services/derived_payoff_persistence.py
  echo

  echo "== Validação compute payoff V2 - resumo =="
  grep -n "VALIDATION_ERRORS\|PAYOFF_POINTS_LEN\|PAYOFF_META\|Antes payoff\|Depois payoff\|Traceback\|TypeError\|ValueError\|warning\|erro" -A20 -B10 \
    docs/checkpoints/evidencias/fase-3f-fix1-diagnostico-compute-payoff-v2.txt || true
  echo

  echo "== Contagens finais derived.db =="
  python - <<'PY'
import sqlite3

conn = sqlite3.connect("dados/derived.db")
for table in ["payoff_curve_points", "structure_decisions"]:
    count = conn.execute(
        f"select count(*) from {table} where structure_id=?",
        (2,),
    ).fetchone()[0]
    print(table, "structure_id=2:", count)

rows = conn.execute(
    """
    select timestamp, aba, structure_id, spot_ref, point_spot, point_pl
      from payoff_curve_points
     where structure_id=?
     order by timestamp desc, point_spot asc
     limit 10
    """,
    (2,),
).fetchall()

print()
print("Amostra payoff:")
for row in rows:
    print(row)

conn.close()
PY

  echo
  echo "============================================================"
  echo "FIM EVIDENCIA FINAL"
  echo "============================================================"

} > "$EVID" 2>&1

cat >> "$AUDIT" <<MD

## Fase 3F Fix1 - Evidencia final

Data: $(date)

Branch: $(git branch --show-current)

Commit base: $(git rev-parse --short HEAD)

Correção aplicada:
Normalização das legs em services/derived_payoff_persistence.py para preencher
position_side a partir de side antes de chamar domain.compute_payoff_from_canonical_input().

Motivo:
O payoff canônico validava structure.legs[n].position_side como obrigatório, enquanto
payloads manuais gerados pela UI vinham com side=LONG/SHORT.

Evidencia gerada:
docs/checkpoints/evidencias/fase-3f-fix1-evidencia-final.txt

Status:
Patch aplicado e validado por diagnóstico de geração/persistência de payoff.

MD

echo "Evidencia final gerada em:"
echo "$EVID"
echo
echo "Auditoria atualizada em:"
echo "$AUDIT"
