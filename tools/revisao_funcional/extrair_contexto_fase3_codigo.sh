#!/usr/bin/env bash
set -u

OUT="docs/checkpoints/evidencias/fase-3-contexto-cirurgico-codigo.md"

{
  echo "# Fase 3 - Contexto cirurgico para alteracao de codigo"
  echo
  echo "Data: $(date)"
  echo "Branch: $(git branch --show-current 2>/dev/null || true)"
  echo "HEAD: $(git rev-parse --short HEAD 2>/dev/null || true)"
  echo

  echo "## Status git"
  git status --short || true
  echo

  echo "## Objetivo tecnico da Fase 3"
  cat <<'EOF'
Encerrar a Fase 3 com alteracao real de codigo:
- cadastro/manual/assistido deve funcionar sem exigir alias_legacy_aba;
- alias_legacy_aba pode existir como compatibilidade, mas nao pode ser chave obrigatoria do fluxo canonical/manual;
- pricing payload nao deve expor alias_legacy_aba como contrato canonical;
- structure_id deve ser preservado do cadastro ate pricing/persistencia;
- fallback manual precisa ser caminho normal para estruturas sem aba legada.
EOF
  echo

  echo "## Ocorrencias criticas em codigo produtivo - alias/aba"
  git grep -n -i \
    -e "alias_legacy_aba" \
    -e "legacy_aba" \
    -e "structure_id" \
    -e "build_pricing_payload" \
    -e "fallback" \
    -- \
    services/canonical_pricing_facade.py \
    services/canonical_input_service.py \
    services/pricing_input_service.py \
    services/pricing_payload_adapter.py \
    services/structure_input_mapper.py \
    services/structure_market_input_assembler.py \
    services/calculation_orchestrator.py \
    domain/calculation_request.py \
    repositories/structures_repository.py \
    UI/components/structure_editor_dialog.py \
    UI/components/structures_list_panel.py \
    2>/dev/null || true
  echo

  echo "## Ocorrencias criticas em testes Fase 3"
  git grep -n -i \
    -e "alias_legacy_aba" \
    -e "manual_without_alias" \
    -e "build_pricing_payload" \
    -e "StructureInput" \
    -e "canonical" \
    -- \
    ATT/tests/test_canonical_pricing_facade_manual_without_alias.py \
    ATT/tests/test_canonical_pricing_facade.py \
    ATT/tests/test_canonical_input_service.py \
    ATT/tests/test_pricing_input_service.py \
    ATT/tests/test_pricing_payload_adapter.py \
    ATT/tests/test_structure_input_mapper.py \
    ATT/tests/test_structure_market_input_assembler.py \
    ATT/tests/test_structure_editor_dialog.py \
    2>/dev/null || true
  echo

  echo "## Arquivos completos com numeracao - Fase 3"
  for f in \
    services/canonical_pricing_facade.py \
    services/canonical_input_service.py \
    services/pricing_input_service.py \
    services/pricing_payload_adapter.py \
    services/structure_input_mapper.py \
    services/structure_market_input_assembler.py \
    services/calculation_orchestrator.py \
    domain/calculation_request.py \
    ATT/tests/test_canonical_pricing_facade_manual_without_alias.py \
    ATT/tests/test_canonical_pricing_facade.py \
    ATT/tests/test_canonical_input_service.py \
    ATT/tests/test_pricing_input_service.py \
    ATT/tests/test_pricing_payload_adapter.py \
    ATT/tests/test_structure_input_mapper.py \
    ATT/tests/test_structure_market_input_assembler.py
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
  echo "## Coleta dos testes Fase 3"
  python -m pytest \
    ATT/tests/test_canonical_pricing_facade_manual_without_alias.py \
    ATT/tests/test_canonical_pricing_facade.py \
    ATT/tests/test_canonical_input_service.py \
    ATT/tests/test_pricing_input_service.py \
    ATT/tests/test_pricing_payload_adapter.py \
    ATT/tests/test_structure_input_mapper.py \
    ATT/tests/test_structure_market_input_assembler.py \
    --collect-only -q 2>&1 || true

  echo
  echo "## Execucao dos testes Fase 3"
  python -m pytest \
    ATT/tests/test_canonical_pricing_facade_manual_without_alias.py \
    ATT/tests/test_canonical_pricing_facade.py \
    ATT/tests/test_canonical_input_service.py \
    ATT/tests/test_pricing_input_service.py \
    ATT/tests/test_pricing_payload_adapter.py \
    ATT/tests/test_structure_input_mapper.py \
    ATT/tests/test_structure_market_input_assembler.py \
    -q 2>&1 || true

} > "$OUT"

echo "Contexto cirurgico Fase 3 gerado em: $OUT"
