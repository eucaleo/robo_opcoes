#!/usr/bin/env bash
set -u

OUT="docs/checkpoints/evidencias/fase-4-contexto-cirurgico-codigo.md"

{
  echo "# Fase 4 - Contexto cirurgico para alteracao de codigo"
  echo
  echo "Data: $(date)"
  echo "Branch: $(git branch --show-current 2>/dev/null || true)"
  echo "HEAD: $(git rev-parse --short HEAD 2>/dev/null || true)"
  echo

  echo "## Status git"
  git status --short || true
  echo

  echo "## Objetivo tecnico da Fase 4"
  cat <<'EOF'
Encerrar a Fase 4 com alteracao real de codigo:
- payoff e decisao devem operar por structure_id;
- get_payoff_by_aba nao deve voltar como interface publica;
- persistencia deve gravar e consultar dados por structure_id quando disponivel;
- UI deve renderizar payoff/decisao por structure_id;
- alias/aba legado pode existir somente como compatibilidade historica ou fonte RTD legada.
EOF
  echo

  echo "## Ocorrencias criticas em codigo produtivo - payoff/decision/persistencia/UI"
  git grep -n -i \
    -e "payoff" \
    -e "decision" \
    -e "decisao" \
    -e "decisão" \
    -e "structure_id" \
    -e "aba" \
    -e "alias_legacy_aba" \
    -e "get_payoff" \
    -e "save_payoff" \
    -e "insert_structure_decision" \
    -e "payoff_curve_points" \
    -e "system_snapshots" \
    -- \
    services/derived_service.py \
    services/derived_payoff_persistence.py \
    services/payoff_persistence_port.py \
    services/payoff_pricing_engine.py \
    services/structure_analysis_service.py \
    services/pricing_execution_persistence_service.py \
    services/pricing_execution_app_service.py \
    services/pricing_execution_orchestration_service.py \
    services/pricing_execution_query_service.py \
    domain/payoff.py \
    domain/decision.py \
    domain/payoff_features.py \
    domain/structure_metrics.py \
    repositories/system_snapshots_repository.py \
    repositories/ui_data_table_candidates.py \
    UI/models/ui_data.py \
    UI/components/details_panel.py \
    UI/components/decisions_grid.py \
    UI/components/payoff_chart.py \
    UI/main_window.py \
    2>/dev/null || true
  echo

  echo "## Ocorrencias criticas em testes Fase 4"
  git grep -n -i \
    -e "payoff" \
    -e "decision" \
    -e "decisao" \
    -e "decisão" \
    -e "structure_id" \
    -e "aba" \
    -e "alias_legacy_aba" \
    -- \
    ATT/tests/test_decision.py \
    ATT/tests/test_payoff_canonical.py \
    ATT/tests/test_payoff_chart.py \
    ATT/tests/test_payoff_pricing_engine.py \
    ATT/tests/test_structure_analysis_service.py \
    ATT/tests/test_derived_service.py \
    ATT/tests/test_orchestrator_run_methods.py \
    ATT/tests/test_pricing_execution_persistence_service.py \
    ATT/tests/test_pricing_execution_app_service.py \
    ATT/tests/test_pricing_execution_orchestration_service.py \
    ATT/tests/test_pricing_execution_query_service.py \
    ATT/tests/test_ui_data_migration.py \
    ATT/tests/test_system_snapshots_repository.py \
    2>/dev/null || true
  echo

  echo "## Arquivos completos com numeracao - Fase 4"
  for f in \
    services/derived_service.py \
    services/derived_payoff_persistence.py \
    services/payoff_persistence_port.py \
    services/payoff_pricing_engine.py \
    services/structure_analysis_service.py \
    services/pricing_execution_persistence_service.py \
    services/pricing_execution_app_service.py \
    services/pricing_execution_orchestration_service.py \
    services/pricing_execution_query_service.py \
    domain/payoff.py \
    domain/decision.py \
    domain/payoff_features.py \
    domain/structure_metrics.py \
    repositories/system_snapshots_repository.py \
    repositories/ui_data_table_candidates.py \
    UI/models/ui_data.py \
    UI/components/details_panel.py \
    UI/components/decisions_grid.py \
    UI/components/payoff_chart.py \
    UI/main_window.py \
    ATT/tests/test_decision.py \
    ATT/tests/test_payoff_canonical.py \
    ATT/tests/test_payoff_chart.py \
    ATT/tests/test_payoff_pricing_engine.py \
    ATT/tests/test_structure_analysis_service.py \
    ATT/tests/test_derived_service.py \
    ATT/tests/test_orchestrator_run_methods.py \
    ATT/tests/test_pricing_execution_persistence_service.py \
    ATT/tests/test_pricing_execution_app_service.py \
    ATT/tests/test_pricing_execution_orchestration_service.py \
    ATT/tests/test_pricing_execution_query_service.py \
    ATT/tests/test_ui_data_migration.py \
    ATT/tests/test_system_snapshots_repository.py
  do
    if [ -f "$f" ]; then
      echo
      echo "## FILE: $f"
      echo '```python'
      nl -ba "$f"
      echo '```'
    else
      echo
      echo "## FILE AUSENTE: $f"
    fi
  done

  echo
  echo "## Coleta dos testes Fase 4"
  python -m pytest ATT/tests -k "payoff or decision or decisao or decisoes or pricing_execution" --collect-only -q 2>&1 || true

  echo
  echo "## Execucao dos testes Fase 4"
  python -m pytest ATT/tests -k "payoff or decision or decisao or decisoes or pricing_execution" -q 2>&1 || true

} > "$OUT"

echo "Contexto cirurgico Fase 4 gerado em: $OUT"
