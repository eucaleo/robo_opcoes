#!/usr/bin/env bash
set -u

OUT="docs/checkpoints/evidencias/fase-3-4-alvos-provaveis-correcao.txt"

{
  echo "# Alvos provaveis para correcao de codigo - Fases 3 e 4"
  echo
  echo "Data: $(date)"
  echo "Branch: $(git branch --show-current 2>/dev/null || true)"
  echo "HEAD: $(git rev-parse --short HEAD 2>/dev/null || true)"
  echo

  echo "## Status git"
  git status --short || true
  echo

  echo "## Alvos Fase 3 - services"
  ls services 2>/dev/null | grep -Ei "structure|canonical|pricing|rtd|manual|derived|orchestrator" || true
  echo

  echo "## Alvos Fase 3 - tests"
  ls ATT/tests 2>/dev/null | grep -Ei "structure|canonical|pricing|rtd|manual|derived|orchestrator" || true
  echo

  echo "## Alvos Fase 4 - domain"
  ls domain 2>/dev/null | grep -Ei "payoff|decision|decisao|structure|metric|feature" || true
  echo

  echo "## Alvos Fase 4 - services"
  ls services 2>/dev/null | grep -Ei "payoff|decision|decisao|pricing|derived|snapshot|analysis" || true
  echo

  echo "## Alvos Fase 4 - UI"
  find UI -type f 2>/dev/null | grep -Ei "payoff|decision|decisao|decisoes|chart|grid|details|main_window|ui_data" || true
  echo

  echo "## Pontos com alias/aba que precisam de classificacao: legado tolerado x bug"
  git grep -n -i \
    -e "alias_legacy_aba" \
    -e "legacy_aba" \
    -e "alias_leg" \
    -e "get_payoff_by_aba" \
    -e "get_decision_by_aba" \
    -e "aba" \
    -- services domain repositories UI ATT/tests 2>/dev/null || true
  echo

  echo "## Pontos com possivel comportamento incompleto"
  git grep -n -i \
    -e "TODO" \
    -e "FIXME" \
    -e "stub" \
    -e "placeholder" \
    -e "NotImplemented" \
    -- services domain repositories UI ATT/tests 2>/dev/null || true
  echo

  echo "## Testes focalizados recomendados para ciclo vermelho-verde"
  cat <<'EOF'

Fase 3:
python -m pytest \
  ATT/tests/test_structure_leg_rtd_enrichment_service.py \
  ATT/tests/test_structure_input_mapper.py \
  ATT/tests/test_canonical_pricing_facade_manual_without_alias.py \
  ATT/tests/test_derived_service.py \
  ATT/tests/test_pricing_execution_persistence_service.py \
  ATT/tests/test_structure_analysis_service.py \
  -q

Fase 4:
python -m pytest ATT/tests -k "payoff or decision or decisao or decisoes" -q

Sanidade:
python -m compileall repositories services domain UI ATT/tests

EOF

} > "$OUT"

echo "Resumo de alvos gerado em: $OUT"
