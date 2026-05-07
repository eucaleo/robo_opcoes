#!/usr/bin/env bash
set -euo pipefail

DB_RAW="data/app.db"
fail=0

echo "[INFO] Snapshot canonicality checks (raw DB)"

if [[ ! -f "$DB_RAW" ]]; then
  echo "[FAIL] Raw DB não encontrado: $DB_RAW"
  exit 2
fi

tables="$(sqlite3 "$DB_RAW" ".tables")"

need_table() {
  local name="$1"
  if echo "$tables" | tr ' ' '\n' | grep -Fx -- "$name" >/dev/null 2>&1; then
    echo "[OK]   Tabela existe: $name"
  else
    echo "[FAIL] Tabela ausente: $name"
    fail=1
  fi
}

echo ""
need_table "rtd_analise_robo"
need_table "rtd_analise_robo_legs"

echo ""
echo "[INFO] (Opcional) Tabelas snapshot versionadas (melhor base para C6)"
if echo "$tables" | tr ' ' '\n' | grep -Fx -- "robo_snapshot" >/dev/null 2>&1; then
  echo "[OK]   robo_snapshot existe"
else
  echo "[WARN] robo_snapshot não existe"
fi
if echo "$tables" | tr ' ' '\n' | grep -Fx -- "robo_legs_snapshot" >/dev/null 2>&1; then
  echo "[OK]   robo_legs_snapshot existe"
else
  echo "[WARN] robo_legs_snapshot não existe"
fi

echo ""
echo "[INFO] Verificando se legs têm timestamp preenchido (amostra)"
sqlite3 "$DB_RAW" "SELECT COUNT(*) AS n_total, SUM(CASE WHEN timestamp IS NULL OR timestamp='' THEN 1 ELSE 0 END) AS n_sem_ts FROM rtd_analise_robo_legs;" || {
  echo "[FAIL] Query falhou em rtd_analise_robo_legs"
  fail=1
}

echo ""
if [[ "$fail" -eq 0 ]]; then
  echo "[PASS] Snapshot canonicality OK"
  exit 0
else
  echo "[FAIL] Snapshot canonicality FAILED"
  exit 1
fi
