#!/usr/bin/env bash
set -u

EVID="docs/checkpoints/evidencias/fase-3f-fix1-inspecao-contrato-payoff.txt"
AUDIT="docs/checkpoints/auditoria-revisao-funcional-pos-uso-real.md"

mkdir -p docs/checkpoints/evidencias
mkdir -p scripts

{
  echo "============================================================"
  echo "FASE 3F FIX1 - INSPECAO CONTRATO PAYOFF"
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

  echo "== Schema payoff_curve_points em dados/derived.db =="
  python - <<'PY'
from pathlib import Path
import sqlite3

db = Path("dados/derived.db")
print("Banco:", db)

if not db.exists():
    print("derived.db nao existe")
    raise SystemExit(0)

conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row

for table in ["payoff_curve_points", "structure_decisions"]:
    print()
    print("Tabela:", table)
    exists = conn.execute(
        "select name from sqlite_master where type='table' and name=?",
        (table,),
    ).fetchone()

    if not exists:
        print("NAO_EXISTE")
        continue

    print("CREATE SQL:")
    row = conn.execute(
        "select sql from sqlite_master where type='table' and name=?",
        (table,),
    ).fetchone()
    print(row["sql"])

    print("PRAGMA table_info:")
    for r in conn.execute(f"pragma table_info({table})").fetchall():
        print(dict(r))

    print("Indices:")
    for r in conn.execute(f"pragma index_list({table})").fetchall():
        print(dict(r))

    print("Amostra geral:")
    rows = conn.execute(f"select * from {table} limit 5").fetchall()
    for item in rows:
        print(dict(item))

conn.close()
PY
  echo

  echo "== Arquivo services/canonical_pricing_facade.py =="
  sed -n '1,260p' services/canonical_pricing_facade.py
  echo

  echo "== Busca arquivos de persistencia derivada/payoff =="
  find repositories services domain UI ATT -type f 2>/dev/null | grep -Ei "payoff|derived|decision|pricing" | sort
  echo

  echo "== Referencias diretas a payoff_curve_points =="
  grep -RIn "payoff_curve_points" repositories services domain UI ATT 2>/dev/null || true
  echo

  echo "== Referencias a execute_pricing =="
  grep -RIn "execute_pricing" repositories services domain UI ATT 2>/dev/null || true
  echo

  echo "== Referencias a theoretical_value/premium_paid/max_profit/max_loss =="
  grep -RIn "theoretical_value\|premium_paid\|max_profit\|max_loss" repositories services domain UI ATT 2>/dev/null || true
  echo

  echo "== Testes atuais relacionados a pricing/payoff/canonical =="
  find ATT/tests -type f 2>/dev/null | grep -Ei "pricing|payoff|canonical|decision" | sort
  echo

  echo "============================================================"
  echo "FIM INSPECAO CONTRATO PAYOFF"
  echo "============================================================"

} > "$EVID" 2>&1

cat >> "$AUDIT" <<MD

## Fase 3F Fix1 - Inspecao contrato payoff

Data: $(date)

Branch: $(git branch --show-current)

Commit base: $(git rev-parse --short HEAD)

Objetivo:
Inspecionar schema de payoff_curve_points, codigo da CanonicalPricingFacade e referencias existentes antes de implementar geracao de payoff canonico.

Evidencia gerada:
docs/checkpoints/evidencias/fase-3f-fix1-inspecao-contrato-payoff.txt

Status:
Inspecao executada. Proxima etapa: implementar geracao e persistencia de pontos de payoff para estrutura manual canonica.

MD

echo "Inspecao Fase 3F Fix1 gerada em:"
echo "$EVID"
echo
echo "Auditoria atualizada em:"
echo "$AUDIT"
