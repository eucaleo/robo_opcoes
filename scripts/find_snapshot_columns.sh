#!/usr/bin/env bash
# scripts/find_snapshot_columns.sh
# Descobre candidatos a colunas de timestamp/data/hora nas tabelas rtd_*.

set -euo pipefail

ROOT="${1:-.}"

DBDIR=""
if [[ -d "$ROOT/dados" ]]; then DBDIR="$ROOT/dados"; fi
if [[ -z "$DBDIR" && -d "$ROOT/data" ]]; then DBDIR="$ROOT/data"; fi
if [[ -z "$DBDIR" ]]; then
  echo "[ERRO] Não encontrei 'dados/' nem 'data/' em: $ROOT"
  exit 1
fi

APP_DB="$DBDIR/app.db"
TS="$(date +%Y%m%d_%H%M%S)"
OUT="reports/find_snapshot_columns_${TS}.txt"
mkdir -p reports

if [[ ! -f "$APP_DB" ]]; then
  echo "[ERRO] app.db não encontrado em: $APP_DB"
  exit 1
fi

{
  echo "=== FIND SNAPSHOT COLUMNS ==="
  echo "Data: $(date)"
  echo "DB: $APP_DB"
  echo ""

  TABLES=$(sqlite3 "$APP_DB" ".tables" | tr ' ' '\n' | grep -E '^rtd_' || true)
  if [[ -z "$TABLES" ]]; then
    echo "Nenhuma tabela rtd_* encontrada."
    exit 0
  fi

  for T in $TABLES; do
    echo "------------------------------"
    echo "TABLE: $T"
    echo "------------------------------"
    # imprime colunas que parecem ser timestamp/data/hora
    sqlite3 "$APP_DB" "PRAGMA table_info($T);" \
      | awk -F'|' '{
          col=$2;
          l=tolower(col);
          if (l ~ /time|data|date|dt|timestamp|hora|created|updated|snapshot/) {
            print col
          }
        }' | sort -u || true
    echo ""
  done

} > "$OUT"

echo "OK - relatório gerado: $OUT"
