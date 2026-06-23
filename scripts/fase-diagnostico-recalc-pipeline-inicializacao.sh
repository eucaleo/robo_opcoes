#!/usr/bin/env bash
set -euo pipefail

OUT="docs/checkpoints/evidencias/fase-diagnostico-recalc-pipeline-inicializacao.txt"
mkdir -p "$(dirname "$OUT")"

{
  echo "== Diagnóstico: recalc/pipeline em inicialização e refresh =="
  date
  echo

  echo "== Branch e últimos commits =="
  git branch --show-current
  git log --oneline -8
  echo

  echo "== Status =="
  git status --short
  echo

  echo "== Busca por chamadas de pipeline/recalc =="
  grep -RIn \
    "recalculate_structure\|_on_recalculate_cb\|on_recalculate\|_on_recalculate_click\|run_pipeline\|run_derived_pipeline\|_reprice_structure_after_save\|execute_pricing\|CanonicalPricingFacade" \
    UI services scripts repositories ATT/tests 2>/dev/null || true
  echo

  echo "== Trecho UI/main_window.py: init/menu/bind/refresh/auto-refresh/recalc =="
  sed -n '35,180p' UI/main_window.py
  echo
  sed -n '250,430p' UI/main_window.py
  echo
  sed -n '470,530p' UI/main_window.py
  echo
  sed -n '840,920p' UI/main_window.py
  echo

  echo "== Trecho UI/components/details_panel.py: botão e callback de recálculo =="
  sed -n '600,760p' UI/components/details_panel.py
  echo
  sed -n '1020,1095p' UI/components/details_panel.py
  echo

  echo "== Verificação sintática =="
  python -m py_compile UI/main_window.py UI/components/details_panel.py
  echo "py_compile OK"

} > "$OUT"

echo "OK: evidência gerada em $OUT"
