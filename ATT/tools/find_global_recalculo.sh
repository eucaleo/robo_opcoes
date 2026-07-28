#!/usr/bin/env bash
set -euo pipefail

mkdir -p tools/reports

{
  echo "== Busca por Recalculo Global =="
  echo ""

  echo "## Ocorrências textuais"
  grep -RIn --exclude-dir=.git --exclude-dir=__pycache__ \
    "Recalculo\|Recalcular\|recalculo\|recalcular\|Atualizar sistema\|atualizar sistema\|refresh all\|recalculate all" \
    . 2>/dev/null || true

  echo ""
  echo "## Possíveis serviços globais"
  grep -RIn --exclude-dir=.git --exclude-dir=__pycache__ \
    "PayoffRefreshCommandService\|refresh_all\|recalculate_all\|global_refresh\|system_refresh\|run_all\|update_all" \
    . 2>/dev/null || true

  echo ""
  echo "## Callbacks de recalculo"
  grep -RIn --exclude-dir=.git --exclude-dir=__pycache__ \
    "on_recalculate\|_on_recalculate_cb\|recalculate_selected_structure\|recalculate_structure\|refresh_selected" \
    . 2>/dev/null || true
} > tools/reports/global_recalculo_audit.txt

echo "Relatório gerado em tools/reports/global_recalculo_audit.txt"
