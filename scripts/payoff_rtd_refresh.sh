#!/usr/bin/env bash
set -euo pipefail

DB="${DB:-dados/app.db}"

if [ "$#" -gt 0 ]; then
  IDS="$*"
else
  IDS="${PAYOFF_IDS:-2 3}"
fi

LOG_DIR="${LOG_DIR:-logs}"
mkdir -p "$LOG_DIR"

STAMP="$(date +%Y%m%d-%H%M%S)"
LOG_FILE="$LOG_DIR/payoff-rtd-refresh-$STAMP.log"

exec > >(tee -a "$LOG_FILE") 2>&1

echo "[payoff-refresh] início"
echo "[payoff-refresh] db=$DB"
echo "[payoff-refresh] ids=$IDS"
echo "[payoff-refresh] log=$LOG_FILE"
echo ""

python -m py_compile \
  scripts/recalculate_payoff_curve_points_once.py \
  scripts/diagnose_payoff_curve_points.py \
  scripts/payoff_rtd_batch.py \
  scripts/validate_payoff_rtd_latest.py

python scripts/payoff_rtd_batch.py \
  --db "$DB" \
  --structure-ids $IDS \
  --diagnose

python scripts/validate_payoff_rtd_latest.py \
  --db "$DB" \
  --structure-ids $IDS \
  --print-legs

echo ""
echo "[payoff-refresh] finalizado com sucesso."
