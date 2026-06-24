#!/usr/bin/env bash
set -u

OUT="docs/checkpoints/evidencias/fase-3-4-diagnostico-bugs-provaveis.md"

{
  echo "# Diagnostico de bugs provaveis - Fases 3 e 4"
  echo
  echo "Data: $(date)"
  echo "Branch: $(git branch --show-current 2>/dev/null || true)"
  echo "HEAD: $(git rev-parse --short HEAD 2>/dev/null || true)"
  echo

  echo "## Status git"
  git status --short || true
  echo

  echo "## Regra de classificacao"
  cat <<'EOF'
TOLERADO:
- alias_legacy_aba em repositories/structures_repository.py;
- alias_legacy_aba em UI de cadastro/lista como campo informativo/editavel;
- aba em repositórios legados de RTD/robo legs;
- testes que garantem que alias_legacy_aba NAO entra no payload canonical.

CANDIDATO A BUG FASE 3:
- qualquer fluxo manual/canonical que falhe por alias_legacy_aba nulo;
- qualquer payload de pricing que exija ou exponha alias_legacy_aba;
- qualquer montagem de input que perca structure_id;
- qualquer fallback manual tratado como excecao inesperada.

CANDIDATO A BUG FASE 4:
- payoff/decisao consultados primariamente por aba;
- persistencia de payoff/decisao sem structure_id quando ele existe;
- UI que selecione payoff/decisao por aba quando tem structure_id;
- reintroducao de get_payoff_by_aba como API publica.
EOF
  echo

  echo "## Candidatos a bug Fase 3 - raise/erro relacionado a alias"
  git grep -n -i \
    -e "raise .*alias_legacy_aba" \
    -e "alias_legacy_aba is null" \
    -e "sem alias_legacy_aba" \
    -e "requires.*alias" \
    -e "missing.*alias" \
    -- services repositories domain UI ATT/tests 2>/dev/null || true
  echo

  echo "## Candidatos a bug Fase 3 - payload canonical expondo alias"
  git grep -n -i \
    -e '"alias_legacy_aba"' \
    -e "'alias_legacy_aba'" \
    -- \
    services/pricing_payload_adapter.py \
    services/pricing_input_service.py \
    services/canonical_input_service.py \
    services/canonical_pricing_facade.py \
    services/structure_input_mapper.py \
    services/structure_market_input_assembler.py \
    domain/calculation_request.py \
    2>/dev/null || true
  echo

  echo "## Candidatos a bug Fase 3 - perda de structure_id em payload/input"
  git grep -n -i \
    -e "structure_id" \
    -e "structure_ref" \
    -e "to_structure_input" \
    -e "build_pricing_payload" \
    -- \
    services/pricing_input_service.py \
    services/canonical_input_service.py \
    services/canonical_pricing_facade.py \
    services/structure_input_mapper.py \
    services/structure_market_input_assembler.py \
    services/calculation_orchestrator.py \
    2>/dev/null || true
  echo

  echo "## Candidatos a bug Fase 4 - API publica por aba"
  git grep -n -i \
    -e "def get_payoff_by_aba" \
    -e "def get_decision_by_aba" \
    -e "get_payoff_by_aba(" \
    -e "get_decision_by_aba(" \
    -e "by_aba" \
    -- services repositories domain UI ATT/tests 2>/dev/null || true
  echo

  echo "## Candidatos a bug Fase 4 - payoff/decision usando aba na UI"
  git grep -n -i \
    -e "get_payoff" \
    -e "get_decision" \
    -e "payoff" \
    -e "decision" \
    -e "aba" \
    -e "structure_id" \
    -- \
    UI/models/ui_data.py \
    UI/components/details_panel.py \
    UI/components/decisions_grid.py \
    UI/components/payoff_chart.py \
    UI/main_window.py \
    2>/dev/null || true
  echo

  echo "## Candidatos a bug Fase 4 - persistencia sem structure_id"
  git grep -n -i \
    -e "INSERT INTO payoff" \
    -e "INSERT INTO decision" \
    -e "INSERT INTO decisions" \
    -e "payoff_curve_points" \
    -e "structure_id" \
    -e "aba" \
    -- \
    services/derived_payoff_persistence.py \
    services/derived_service.py \
    services/pricing_execution_persistence_service.py \
    repositories/system_snapshots_repository.py \
    db infra \
    2>/dev/null || true
  echo

  echo "## Testes direcionados - resultado compacto"
  echo
  echo "### Fase 3"
  python -m pytest \
    ATT/tests/test_canonical_pricing_facade_manual_without_alias.py \
    ATT/tests/test_canonical_input_service.py \
    ATT/tests/test_pricing_input_service.py \
    ATT/tests/test_pricing_payload_adapter.py \
    ATT/tests/test_structure_input_mapper.py \
    ATT/tests/test_structure_market_input_assembler.py \
    -q 2>&1 || true

  echo
  echo "### Fase 4"
  python -m pytest ATT/tests -k "payoff or decision or decisao or decisoes or pricing_execution" -q 2>&1 || true

  echo
  echo "### Compileall"
  python -m compileall services domain repositories UI ATT/tests 2>&1 || true

} > "$OUT"

echo "Diagnostico gerado em: $OUT"
