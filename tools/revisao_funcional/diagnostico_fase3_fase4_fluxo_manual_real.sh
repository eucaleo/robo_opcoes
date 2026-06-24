#!/usr/bin/env bash
set -u

OUT="docs/checkpoints/evidencias/fase-3-4-fluxo-manual-real-diagnostico.md"

{
  echo "# Diagnostico funcional real - Fases 3 e 4"
  echo
  echo "Data: $(date)"
  echo "Branch: $(git branch --show-current 2>/dev/null || true)"
  echo "HEAD: $(git rev-parse --short HEAD 2>/dev/null || true)"
  echo

  echo "## Status git"
  git status --short || true
  echo

  echo "## Fase 3 - Cadastro assistido por simbolo"
  cat <<'EOF'
Objetivo:
- usuario informa nome da estrutura e dados minimos da leg;
- sistema reconhece simbolo da opcao;
- sistema preenche ativo objeto, strike, vencimento, multiplicador e metadados;
- divergencia entre tipo informado e tipo detectado deve bloquear ou pedir confirmacao;
- estrutura so deve ser funcional se tiver dados minimos para payoff e decisoes.
EOF
  echo

  echo "## Fase 4 - Estrutura manual integrada a payoff e decisoes"
  cat <<'EOF'
Objetivo:
- estrutura manual/assistida valida deve gerar curva de payoff;
- estrutura manual/assistida valida deve gerar decisao;
- structure_decisions deve receber linhas ou registrar rejeicao clara;
- payoff_curve_points deve receber pontos ou registrar rejeicao clara;
- logs devem indicar estruturas lidas, processadas, ignoradas e rejeitadas.
EOF
  echo

  echo "## Grep - simbolo/opcao/strike/vencimento/multiplicador"
  git grep -n -i \
    -e "symbol" \
    -e "símbolo" \
    -e "simbolo" \
    -e "codigo_opcao" \
    -e "opcao" \
    -e "opção" \
    -e "strike" \
    -e "vencimento" \
    -e "expiration" \
    -e "maturity" \
    -e "multiplicador" \
    -e "multiplier" \
    -e "call_put" \
    -e "ativo" \
    -e "underlying" \
    -- services domain repositories UI ATT/tests api db infra 2>/dev/null || true
  echo

  echo "## Grep - cadastro/editor/legs"
  git grep -n -i \
    -e "StructureEditorDialog" \
    -e "structure_editor" \
    -e "legs" \
    -e "create_structure" \
    -e "update_structure" \
    -e "save" \
    -e "_cmd_save" \
    -e "_build_legs_payload" \
    -e "structures_legs" \
    -e "structure_legs" \
    -- UI services repositories api ATT/tests 2>/dev/null || true
  echo

  echo "## Grep - payoff/decisao/rejeicao/logs"
  git grep -n -i \
    -e "payoff_curve_points" \
    -e "structure_decisions" \
    -e "decision" \
    -e "decisao" \
    -e "decisão" \
    -e "reject" \
    -e "rejeit" \
    -e "ignored" \
    -e "ignorado" \
    -e "skip" \
    -e "process" \
    -e "active" \
    -e "canonical" \
    -e "manual" \
    -- services domain repositories UI ATT/tests 2>/dev/null || true
  echo

  echo "## Possiveis schemas/migrations"
  find . -maxdepth 4 -type f \( \
    -iname "*schema*" -o \
    -iname "*migration*" -o \
    -iname "*.sql" -o \
    -iname "*db*.py" \
  \) | sort
  echo

  echo "## Arquivos provaveis completos com numeracao"
  for f in \
    UI/components/structure_editor_dialog.py \
    UI/components/structures_list_panel.py \
    UI/models/ui_data.py \
    repositories/structures_repository.py \
    repositories/market_snapshot_repository.py \
    repositories/robo_legs_repository.py \
    services/structure_leg_rtd_enrichment_service.py \
    services/structure_market_input_assembler.py \
    services/structure_input_mapper.py \
    services/structure_analysis_service.py \
    services/calculation_orchestrator.py \
    services/derived_service.py \
    services/derived_payoff_persistence.py \
    domain/payoff.py \
    domain/decision.py \
    domain/structure_metrics.py \
    ATT/tests/test_structure_editor_dialog.py \
    ATT/tests/test_structure_market_input_assembler.py \
    ATT/tests/test_structure_analysis_service.py \
    ATT/tests/test_derived_service.py \
    ATT/tests/test_payoff_canonical.py \
    ATT/tests/test_decision.py
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
  echo "## Testes focalizados existentes"
  python -m pytest \
    ATT/tests/test_structure_editor_dialog.py \
    ATT/tests/test_structure_market_input_assembler.py \
    ATT/tests/test_structure_analysis_service.py \
    ATT/tests/test_derived_service.py \
    ATT/tests/test_payoff_canonical.py \
    ATT/tests/test_decision.py \
    -q 2>&1 || true

} > "$OUT"

echo "Diagnostico funcional real gerado em: $OUT"
