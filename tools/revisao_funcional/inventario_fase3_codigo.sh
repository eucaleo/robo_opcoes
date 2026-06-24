#!/usr/bin/env bash
set -u

OUT="docs/checkpoints/evidencias/fase-3-correcao-codigo-inventario.txt"

{
  echo "# Inventario tecnico para correcao de codigo - Fase 3"
  echo
  echo "Data: $(date)"
  echo "Branch: $(git branch --show-current 2>/dev/null || true)"
  echo "HEAD: $(git rev-parse --short HEAD 2>/dev/null || true)"
  echo

  echo "## Status git"
  git status --short || true
  echo

  echo "## Arquivos candidatos - estrutura, cadastro, canonical, RTD, manual"
  find . \
    -path './.git' -prune -o \
    -path './.pytest_cache' -prune -o \
    -path './__pycache__' -prune -o \
    -type f \( \
      -iname '*structure*' -o \
      -iname '*estrutura*' -o \
      -iname '*canonical*' -o \
      -iname '*pricing*' -o \
      -iname '*rtd*' -o \
      -iname '*manual*' -o \
      -iname '*derived*' -o \
      -iname '*orchestrator*' \
    \) -print | sort
  echo

  echo "## Git log dos arquivos provaveis da Fase 3"
  git log --oneline -- \
    services/structure_leg_rtd_enrichment_service.py \
    services/canonical_pricing_facade.py \
    services/derived_payoff_persistence.py \
    services/derived_service.py \
    services/calculation_orchestrator.py \
    services/pricing_execution_service.py \
    services/pricing_execution_persistence_service.py \
    domain/structure*.py \
    repositories/*structure* \
    UI/main_window.py \
    UI/components/details_panel.py \
    UI/models/ui_data.py \
    ATT/tests/test_structure_leg_rtd_enrichment_service.py \
    ATT/tests/test_structure_input_mapper.py \
    ATT/tests/test_canonical_pricing_facade_manual_without_alias.py \
    ATT/tests/test_derived_service.py \
    ATT/tests/test_pricing_execution_persistence_service.py \
    ATT/tests/test_structure_analysis_service.py \
    2>/dev/null || true
  echo

  echo "## Ocorrencias importantes - cadastro/manual/estrutura"
  git grep -n -i \
    -e "cadastro" \
    -e "assistido" \
    -e "manual" \
    -e "estrutura" \
    -e "structure_id" \
    -e "structure input" \
    -e "StructureInput" \
    -e "canonical" \
    -e "position_side" \
    -e "rtd" \
    -- \
    services domain repositories UI ATT/tests \
    2>/dev/null || true
  echo

  echo "## Possiveis acoplamentos legados ainda ativos"
  git grep -n -i \
    -e "alias_legacy_aba" \
    -e "legacy_aba" \
    -e "aba" \
    -e "alias_leg" \
    -e "get_payoff_by_aba" \
    -e "get_decision_by_aba" \
    -- \
    services domain repositories UI ATT/tests \
    2>/dev/null || true
  echo

  echo "## Possiveis stubs, TODOs ou implementacoes incompletas"
  git grep -n -i \
    -e "TODO" \
    -e "FIXME" \
    -e "stub" \
    -e "mock" \
    -e "placeholder" \
    -e "NotImplemented" \
    -e "pass  # " \
    -- \
    services domain repositories UI ATT/tests \
    2>/dev/null || true
  echo

  echo "## Definicoes Python candidatas - services"
  grep -RniE "^(class|def) " services \
    --include='*.py' 2>/dev/null | grep -Ei "structure|canonical|pricing|rtd|manual|derived|orchestrator" || true
  echo

  echo "## Definicoes Python candidatas - domain"
  grep -RniE "^(class|def) " domain \
    --include='*.py' 2>/dev/null | grep -Ei "structure|canonical|pricing|rtd|manual|derived|orchestrator" || true
  echo

  echo "## Definicoes Python candidatas - repositories"
  grep -RniE "^(class|def) " repositories \
    --include='*.py' 2>/dev/null | grep -Ei "structure|canonical|pricing|rtd|manual|derived|orchestrator" || true
  echo

  echo "## Testes candidatos existentes da Fase 3"
  find ATT/tests -type f \( \
    -iname '*structure*' -o \
    -iname '*canonical*' -o \
    -iname '*pricing*' -o \
    -iname '*rtd*' -o \
    -iname '*manual*' -o \
    -iname '*derived*' -o \
    -iname '*orchestrator*' \
  \) -print | sort
  echo

  echo "## Coleta pytest direcionada - Fase 3"
  python -m pytest \
    ATT/tests/test_structure_leg_rtd_enrichment_service.py \
    ATT/tests/test_structure_input_mapper.py \
    ATT/tests/test_canonical_pricing_facade_manual_without_alias.py \
    ATT/tests/test_derived_service.py \
    ATT/tests/test_pricing_execution_persistence_service.py \
    ATT/tests/test_structure_analysis_service.py \
    --collect-only -q 2>&1 || true
  echo

  echo "## Execucao pytest direcionada - Fase 3"
  python -m pytest \
    ATT/tests/test_structure_leg_rtd_enrichment_service.py \
    ATT/tests/test_structure_input_mapper.py \
    ATT/tests/test_canonical_pricing_facade_manual_without_alias.py \
    ATT/tests/test_derived_service.py \
    ATT/tests/test_pricing_execution_persistence_service.py \
    ATT/tests/test_structure_analysis_service.py \
    -q 2>&1 || true
  echo

  echo "## Compileall candidatos - Fase 3"
  python -m compileall services domain repositories UI ATT/tests 2>&1 || true

} > "$OUT"

echo "Inventario Fase 3 gerado em: $OUT"
