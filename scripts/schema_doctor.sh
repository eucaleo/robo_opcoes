#!/usr/bin/env bash
# scripts/schema_doctor.sh
# Diagnóstico: imprime tabelas/colunas e amostras para descobrir schema real.
# NÃO altera nada.

set -euo pipefail

ROOT="${1:-.}"

# Prioridade para /dados (se existe), fallback para /data (legado)
DBDIR=""
if [[ -d "$ROOT/dados" ]]; then
  DBDIR="$ROOT/dados"
elif [[ -d "$ROOT/data" ]]; then
  DBDIR="$ROOT/data"
else
  echo "[ERRO] Não encontrei pasta 'dados/' nem 'data/' em: $ROOT"
  exit 1
fi

APP_DB="$DBDIR/app.db"
DERIVED_DB="$DBDIR/derived.db"

TS="$(date +%Y%m%d_%H%M%S)"
OUT="reports/schema_doctor_${TS}.txt"
mkdir -p reports BAK

{
  echo "=== SCHEMA DOCTOR ==="
  echo "Data: $(date)"
  echo "ROOT: $ROOT"
  echo "DBDIR: $DBDIR"
  echo "APP_DB: $APP_DB"
  echo "DERIVED_DB: $DERIVED_DB"
  echo ""

  echo "== Arquivos DB encontrados =="
  ls -la "$DBDIR"/*.db 2>/dev/null || true
  echo ""

  if [[ -f "$APP_DB" ]]; then
    echo "=============================="
    echo "RAW (app.db) - tabelas"
    echo "=============================="
    sqlite3 "$APP_DB" ".tables"
    echo ""

    echo "== Tabelas rtd_* (se existirem) =="
    sqlite3 "$APP_DB" ".tables" | tr ' ' '\n' | grep -E '^rtd_' || true
    echo ""

    echo "== Tabelas manual_* (se existirem) =="
    sqlite3 "$APP_DB" ".tables" | tr ' ' '\n' | grep -E '^manual_' || true
    echo ""

    for T in rtd_analise_robo rtd_analise_robo_legs manual_analise_robo_legs rtd_consolidacoes; do
      echo ""
      echo "------------------------------"
      echo "TABLE: $T"
      echo "------------------------------"
      sqlite3 "$APP_DB" ".schema $T" 2>/dev/null || echo "(schema não disponível; tabela pode não existir)"
      echo ""
      echo "PRAGMA table_info($T):"
      sqlite3 "$APP_DB" "PRAGMA table_info($T);" 2>/dev/null || echo "(PRAGMA falhou; tabela pode não existir)"
      echo ""
      echo "Amostra (até 3 linhas):"
      sqlite3 -header -column "$APP_DB" "SELECT * FROM $T LIMIT 3;" 2>/dev/null || echo "(SELECT falhou; tabela pode não existir)"
    done

  else
    echo "[AVISO] app.db não encontrado em $APP_DB"
  fi

  echo ""
  if [[ -f "$DERIVED_DB" ]]; then
    echo "=============================="
    echo "DERIVED (derived.db) - tabelas"
    echo "=============================="
    sqlite3 "$DERIVED_DB" ".tables"
    echo ""

    for T in payoff_curve_points structure_decisions; do
      echo ""
      echo "------------------------------"
      echo "TABLE: $T"
      echo "------------------------------"
      sqlite3 "$DERIVED_DB" ".schema $T" 2>/dev/null || echo "(schema não disponível; tabela pode não existir)"
      echo ""
      echo "PRAGMA table_info($T):"
      sqlite3 "$DERIVED_DB" "PRAGMA table_info($T);" 2>/dev/null || echo "(PRAGMA falhou; tabela pode não existir)"
      echo ""
      echo "Amostra (até 3 linhas):"
      sqlite3 -header -column "$DERIVED_DB" "SELECT * FROM $T LIMIT 3;" 2>/dev/null || echo "(SELECT falhou; tabela pode não existir)"
    done
  else
    echo "[AVISO] derived.db não encontrado em $DERIVED_DB"
  fi

} > "$OUT"

echo "OK - relatório gerado: $OUT"
echo "Dica: abra e procure pelas colunas de timestamp/snapshot nas tabelas rtd_*."
