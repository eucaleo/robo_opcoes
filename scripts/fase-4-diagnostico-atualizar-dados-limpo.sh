#!/usr/bin/env bash
set -u

EVID="docs/checkpoints/evidencias/fase-4-diagnostico-atualizar-dados-limpo.txt"

mkdir -p docs/checkpoints/evidencias

{
  echo "============================================================"
  echo "FASE 4 - DIAGNOSTICO LIMPO ATUALIZAR DADOS"
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

  echo "== UI/main_window.py menus e handlers principais =="
  grep -n "Atualizar Dados\|Executar Pipeline\|def refresh_data\|def run_pipeline\|Pipeline executado\|status_bar.config" UI/main_window.py || true
  echo

  echo "== scripts/run_derived_pipeline.py pontos principais =="
  grep -n "def main\|print\|run\|pipeline\|payoff\|decision\|summary\|count\|return" scripts/run_derived_pipeline.py || true
  echo

  echo "== services/calculation_orchestrator.py pontos principais =="
  grep -n "def run_full_pipeline\|def run_full_pipeline_from_db\|payoff\|decision\|return" services/calculation_orchestrator.py || true
  echo

  echo "== Trecho UI/main_window.py 110-160 =="
  sed -n '110,160p' UI/main_window.py
  echo

  echo "== Trecho UI/main_window.py 260-315 =="
  sed -n '260,315p' UI/main_window.py
  echo

  echo "== Trecho UI/main_window.py 380-490 =="
  sed -n '380,490p' UI/main_window.py
  echo

  echo "== Trecho scripts/run_derived_pipeline.py 1-180 =="
  sed -n '1,180p' scripts/run_derived_pipeline.py
  echo

  echo "============================================================"
  echo "FIM DIAGNOSTICO LIMPO FASE 4"
  echo "============================================================"

} > "$EVID" 2>&1

echo "Diagnostico limpo gerado em:"
echo "$EVID"
