#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

OUT="docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_5_DIAGNOSTICO_ATUALIZAR_DADOS.md"
mkdir -p "docs/checkpoints"

SCAN_PATHS=()

for path in UI scripts repositories services ATT tests; do
  if [ -e "$path" ]; then
    SCAN_PATHS+=("$path")
  fi
done

if [ "${#SCAN_PATHS[@]}" -eq 0 ]; then
  SCAN_PATHS=(".")
fi

write_section() {
  local title="$1"
  echo ""
  echo "## $title"
  echo ""
}

run_grep() {
  local pattern="$1"

  grep -RInE \
    --exclude-dir=.git \
    --exclude-dir=.venv \
    --exclude-dir=venv \
    --exclude-dir=__pycache__ \
    --exclude-dir=.pytest_cache \
    --exclude-dir=node_modules \
    "$pattern" \
    "${SCAN_PATHS[@]}" 2>/dev/null || true
}

{
  echo "# DIAGNÓSTICO FASE 5 — BOTÃO ATUALIZAR DADOS"
  echo ""
  echo "## Status"
  echo ""
  echo "Diagnóstico gerado automaticamente."
  echo ""
  echo "## Diretórios analisados"
  echo ""
  for path in "${SCAN_PATHS[@]}"; do
    echo "- $path"
  done

  write_section "Candidatos de botão"
  run_grep "Atualizar Dados|atualizar dados|Atualizar|atualizar|Refresh|refresh"

  write_section "Candidatos de handler"
  run_grep "clicked.connect|command=|on_click|callback|handler|handle|atualizar|refresh"

  write_section "Candidatos de pipeline"
  run_grep "run_derived_pipeline|run_rtd_option_quotes_pipeline|run_rtd_refresh_full|payoff_curve_points|structure_decisions|RTD|rtd|payoff|decision|decisions"

  write_section "Candidatos de resumo e contadores"
  run_grep "summary|resumo|processed|processadas|ignored|ignoradas|created|generated|updated|warnings|avisos|errors|erros|nenhum dado novo|sem dados"

  write_section "Próximos passos"
  echo "- Confirmar qual ocorrência representa o botão real Atualizar Dados."
  echo "- Confirmar o handler chamado pelo clique."
  echo "- Confirmar o pipeline acionado."
  echo "- Confirmar se existe resumo estruturado."
  echo "- Confirmar se há contadores de RTD, payoff e decisões."
  echo "- Confirmar se sucesso sem dados novos é tratado diferente de sucesso com dados."
} > "$OUT"

echo "Relatório gerado: $OUT"
