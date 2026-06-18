# Fase 6.6 — Auditoria controlada dos metadados RTD no canonical pricing

## Objetivo

Auditar de forma controlada a consistência dos metadados RTD emitidos pelo fluxo de canonical pricing após a consolidação dos fallbacks da Fase 6.5.

Esta fase não deve alterar comportamento funcional inicialmente.

## Escopo inicial

- Mapear cenários RTD já cobertos por testes.
- Verificar consistência entre:
  - price_source;
  - price_resolution_status;
  - rtd_validation_status;
  - rtd_quote_found;
  - payload enviado ao engine;
  - payload persistido.
- Identificar lacunas de cobertura sem alterar UI/API.
- Preservar Excel apenas como gateway RTD.

## Cenários a auditar

| Cenário | Fonte efetiva esperada | Status esperado | Observação |
|---|---|---|---|
| RTD válido | RTD | A confirmar | Deve usar preço RTD como efetivo |
| RTD com preço inválido | Snapshot | invalid_rtd_price | Coberto na Fase 6.5 |
| RTD stale | Snapshot | A confirmar | Coberto na Fase 6.5 |
| RTD asset mismatch | Snapshot | A confirmar | Coberto na Fase 6.5 |
| Sem quote RTD | Snapshot | A confirmar | Verificar cobertura existente |
| Fallback snapshot genérico | Snapshot | A confirmar | Verificar rastreabilidade |

## Arquivos de referência inicial

- ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py
- ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py
- ATT/tests/test_rtd_option_quotes_repository_contract.py
- services/canonical_pricing_facade.py
- docs/checkpoints/fase-6-5-retomada-funcional-incremental-rtd.md
- docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md

## Baseline herdado da Fase 6.5

Validação final executada antes da abertura desta fase:

    python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py ATT/tests/test_rtd_option_quotes_repository_contract.py -q
    32 passed in 1.72s

## Critério de avanço

A fase só deve avançar para alteração de testes ou código caso a auditoria encontre lacuna objetiva de rastreabilidade ou inconsistência entre os metadados RTD esperados e os payloads gerados.

## Restrições

- Não alterar UI.
- Não alterar API.
- Não alterar Excel como fonte funcional.
- Não trocar a semântica de fallback já protegida na Fase 6.5.
