#!/usr/bin/env bash
set -u

OUT="docs/checkpoints/evidencias/fase-4-correcao-codigo-inventario.txt"

{
  echo "# Inventario tecnico para correcao de codigo - Fase 4"
  echo
  echo "Data: $(date)"
  echo "Branch: $(git branch --show-current 2>/dev/null || true)"
  echo "HEAD: $(git rev-parse --short HEAD 2>/dev/null || true)"
  echo

  echo "## Status git"
  git status --short || true
  echo

  echo "## Arquivos candidatos - payoff, decisao, pricing engine, persistencia, UI"
  find . \
    -path './.git' -prune -o \
    -path './.pytest_cache' -prune -o \
    -path './__pycache__' -prune -o \
    -type f \( \
      -iname '*payoff*' -o \
      -iname '*decision*' -o \
      -iname '*decisao*' -o \
      -iname '*decisoes*' -o \
      -iname '*pricing*' -o \
      -iname '*derived*' -o \
      -iname '*snapshot*' \
    \) -print | sort
  echo

  echo "## Git log dos arquivos provaveis da Fase 4"
  git log --oneline -- \
    domain/payoff.py \
    domain/decision.py \
    domain/payoff_features.py \
    domain/structure_metrics.py \
    services/calculation_orchestrator.py \
    services/derived_payoff_persistence.py \
    services/payoff_persistence_port.py \
    services/payoff_pricing_engine.py \
    services/derived_service.py \
    services/structure_analysis_service.py \
    services/pricing_execution_persistence_service.py \
    services/pricing_execution_service.py \
    repositories/system_snapshots_repository.py \
    repositories/ui_data_table_candidates.py \
    infra/bootstrap_structures_schema.py \
    db/migrations/add_structure_id_to_payoff_curve_points.py \
    UI/components/decisions_grid.py \
    UI/components/details_panel.py \
    UI/components/payoff_chart.py \
    UI/main_window.py \
    UI/models/ui_data.py \
    ATT/tests/test_decision.py \
    ATT/tests/test_payoff_canonical.py \
    ATT/tests/test_payoff_chart.py \
    ATT/tests/test_payoff_pricing_engine.py \
    ATT/tests/test_structure_analysis_service.py \
    ATT/tests/test_derived_service.py \
    ATT/tests/test_orchestrator_run_methods.py \
    ATT/tests/test_pricing_execution_persistence_service.py \
    ATT/tests/test_ui_data_migration.py \
    ATT/tests/test_system_snapshots_repository.py \
    2>/dev/null || true
  echo

  echo "## Ocorrencias importantes - payoff/decisoes"
  git grep -n -i \
    -e "payoff" \
    -e "decision" \
    -e "decisao" \
    -e "decisão" \
    -e "decisoes" \
    -e "decisões" \
    -e "payoff_curve" \
    -e "curve_points" \
    -e "breakeven" \
    -e "pnl" \
    -e "pl_at" \
    -e "CLOSE_REOPEN" \
    -e "KEEP" \
    -e "OPEN" \
    -- \
    services domain repositories UI ATT/tests infra db \
    2>/dev/null || true
  echo

  echo "## Persistencia e leitura de payoff/decisao"
  git grep -n -i \
    -e "save_payoff" \
    -e "save_decision" \
    -e "write_payoff" \
    -e "write_decision" \
    -e "get_payoff" \
    -e "get_decision" \
    -e "payoff_curve_points" \
    -e "decisions" \
    -e "system_snapshots" \
    -- \
    services repositories UI domain infra db ATT/tests \
    2>/dev/null || true
  echo

  echo "## Possiveis acoplamentos legados ainda ativos na Fase 4"
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

  echo "## Definicoes Python candidatas - domain"
  grep -RniE "^(class|def) " domain \
    --include='*.py' 2>/dev/null | grep -Ei "payoff|decision|decisao|pricing|metric|feature" || true
  echo

  echo "## Definicoes Python candidatas - services"
  grep -RniE "^(class|def) " services \
    --include='*.py' 2>/dev/null | grep -Ei "payoff|decision|decisao|pricing|derived|snapshot|analysis" || true
  echo

  echo "## Definicoes Python candidatas - UI"
  grep -RniE "^(class|def) " UI \
    --include='*.py' 2>/dev/null | grep -Ei "payoff|decision|decisao|decisoes|chart|grid|details" || true
  echo

  echo "## Testes candidatos existentes da Fase 4"
  find ATT/tests -type f \( \
    -iname '*payoff*' -o \
    -iname '*decision*' -o \
    -iname '*decisao*' -o \
    -iname '*decisoes*' -o \
    -iname '*pricing*' -o \
    -iname '*snapshot*' \
  \) -print | sort
  echo

  echo "## Coleta pytest direcionada - Fase 4"
  python -m pytest ATT/tests -k "payoff or decision or decisao or decisoes" --collect-only -q 2>&1 || true
  echo

  echo "## Execucao pytest direcionada - Fase 4"
  python -m pytest ATT/tests -k "payoff or decision or decisao or decisoes" -q 2>&1 || true
  echo

  echo "## Compileall candidatos - Fase 4"
  python -m compileall services domain repositories UI ATT/tests 2>&1 || true

} > "$OUT"

echo "Inventario Fase 4 gerado em: $OUT"
