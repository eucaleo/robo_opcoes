#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

OUT="docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_5_CONTRATO_RESUMO_PIPELINE.md"
mkdir -p "docs/checkpoints"

FILES=(
  "scripts/run_derived_pipeline.py"
  "scripts/run_rtd_option_quotes_pipeline.py"
  "scripts/run_rtd_refresh_full.py"
  "UI/components/structure_editor_dialog.py"
)

check_term() {
  local label="$1"
  local pattern="$2"
  local found="Não"

  for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
      if grep -InE "$pattern" "$file" >/dev/null 2>&1; then
        found="Sim"
      fi
    fi
  done

  echo "| $label | $found |"
}

write_occurrences() {
  local label="$1"
  local pattern="$2"

  echo ""
  echo "### $label"
  echo ""

  local any="0"

  for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
      local result
      result="$(grep -InE "$pattern" "$file" 2>/dev/null || true)"
      if [ -n "$result" ]; then
        any="1"
        echo "$result"
      fi
    fi
  done

  if [ "$any" = "0" ]; then
    echo "- Nenhuma ocorrência encontrada."
  fi
}

{
  echo "# VERIFICAÇÃO FASE 5 — CONTRATO MÍNIMO DO RESUMO DO PIPELINE"
  echo ""
  echo "## Status"
  echo ""
  echo "Verificação gerada automaticamente."
  echo ""
  echo "## Arquivos analisados"
  echo ""

  for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
      echo "- $file: existe"
    else
      echo "- $file: não encontrado"
    fi
  done

  echo ""
  echo "## Conceitos verificados"
  echo ""
  echo "| Conceito | Encontrado |"
  echo "|---|---|"

  check_term "Estruturas lidas" "structures_read|estruturas_lidas|structures|structure|estrutura"
  check_term "Estruturas processadas" "structures_processed|estruturas_processadas|processed|processadas"
  check_term "Estruturas ignoradas" "structures_ignored|estruturas_ignoradas|ignored|ignoradas"
  check_term "Pontos de payoff" "payoff_points|payoff_curve_points|pontos_payoff|pontos de payoff"
  check_term "Decisões" "decisions|structure_decisions|decisoes|decisões"
  check_term "Cotações RTD" "RTD|rtd|quotes|option_quotes|cotacoes|cotações"
  check_term "Avisos" "warnings|avisos|warning"
  check_term "Erros" "errors|erros|exception|traceback"
  check_term "Sucesso sem dados novos" "nenhum dado novo|no new data|sem dados|nothing|zero"

  echo ""
  echo "## Ocorrências"

  write_occurrences "Estruturas lidas" "structures_read|estruturas_lidas|structures|structure|estrutura"
  write_occurrences "Estruturas processadas" "structures_processed|estruturas_processadas|processed|processadas"
  write_occurrences "Estruturas ignoradas" "structures_ignored|estruturas_ignoradas|ignored|ignoradas"
  write_occurrences "Pontos de payoff" "payoff_points|payoff_curve_points|pontos_payoff|pontos de payoff"
  write_occurrences "Decisões" "decisions|structure_decisions|decisoes|decisões"
  write_occurrences "Cotações RTD" "RTD|rtd|quotes|option_quotes|cotacoes|cotações"
  write_occurrences "Avisos" "warnings|avisos|warning"
  write_occurrences "Erros" "errors|erros|exception|traceback"
  write_occurrences "Sucesso sem dados novos" "nenhum dado novo|no new data|sem dados|nothing|zero"

  echo ""
  echo "## Leitura esperada"
  echo ""
  echo "A Fase 5 deve garantir que o botão Atualizar Dados tenha retorno claro para:"
  echo ""
  echo "- estruturas lidas;"
  echo "- estruturas processadas;"
  echo "- estruturas ignoradas;"
  echo "- pontos de payoff gerados;"
  echo "- decisões geradas;"
  echo "- cotações RTD atualizadas;"
  echo "- avisos;"
  echo "- erros;"
  echo "- execução sem dados novos."
} > "$OUT"

echo "Relatório gerado: $OUT"
