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


## Auditoria incremental — RTD válido em integração

### Lacuna identificada

A auditoria inicial mostrou que o cenário de RTD válido já possuía cobertura unitária completa em `_resolve_effective_leg_price`, incluindo:

- `price_resolution_status = ok`;
- `rtd_quote_found = True`;
- `rtd_validation_status = ok`;
- metadados de quote RTD.

Porém, o teste de integração `test_execute_pricing_uses_persisted_rtd_option_quote_price` validava no payload enviado ao engine e no payload persistido apenas os campos de preço e alguns metadados da quote RTD, sem validar explicitamente:

- `price_resolution_status`;
- `rtd_quote_found`;
- `rtd_validation_status`.

### Ação executada

Foi adicionada cobertura no teste de integração para garantir que o payload enviado ao engine e o payload persistido preservam os metadados RTD principais no cenário válido.

Commit:

    e8dda71 test: cobre metadados rtd validos na integracao

### Validação executada

    python -m pytest ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py -q
    5 passed in 1.48s

    python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py ATT/tests/test_rtd_option_quotes_repository_contract.py -q
    32 passed in 1.65s

### Resultado

A lacuna de rastreabilidade do cenário RTD válido em integração foi fechada sem alteração funcional.

## Auditoria incremental — erro no repositório RTD

### Lacuna identificada

O cenário unitário de falha no repositório RTD já validava que `_resolve_effective_leg_price` preservava o preço original do snapshot e retornava `price_source = snapshot`.

Porém, o teste não validava explicitamente os metadados de rastreabilidade retornados no `traceability`, deixando sem contrato documentado o comportamento atual quando a consulta ao repositório falha.

### Ação executada

Foi adicionada cobertura unitária para garantir que, no comportamento atual, uma falha de consulta no repositório RTD é normalizada como quote RTD não encontrada, preservando:

- `price_resolution_status = missing_rtd_quote`;
- `rtd_quote_found = False`;
- `rtd_validation_status = error`;
- mensagem contendo a ausência da quote RTD e o código da opção.

Commit:

    a82a370 test: cobre metadados rtd em erro de repositorio

### Validação executada

    python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py -q
    21 passed in 1.24s

    python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py ATT/tests/test_rtd_option_quotes_repository_contract.py -q
    32 passed in 1.70s

### Resultado

A lacuna de rastreabilidade do cenário de erro no repositório RTD foi fechada sem alteração funcional.

## Auditoria incremental — divergência de ativo-base RTD

### Lacuna identificada

O cenário unitário de divergência entre o ativo-base esperado e o ativo-base retornado pela quote RTD já validava o fallback para o preço original do snapshot e os metadados principais de erro.

Porém, o teste ainda não validava explicitamente o código da opção retornado na quote RTD, deixando incompleta a rastreabilidade do registro RTD efetivamente encontrado no cenário de divergência.

### Ação executada

Foi adicionada cobertura unitária para garantir que, no comportamento atual, uma quote RTD encontrada com ativo-base divergente preserva:

- `price_resolution_status = rtd_asset_mismatch`;
- `rtd_quote_found = True`;
- `rtd_validation_status = error`;
- `rtd_quote_codigo_opcao`;
- `rtd_quote_ativo_base`;
- mensagem indicando divergência.

Commit:

    17a21e1 test: cobre codigo opcao em divergencia ativo rtd

### Validação executada

    python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py -q
    21 passed in 1.26s

    python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py ATT/tests/test_rtd_option_quotes_repository_contract.py -q
    32 passed in 1.69s

    git diff --check

### Resultado

A lacuna de rastreabilidade do cenário de divergência de ativo-base RTD foi fechada sem alteração funcional.

## Auditoria incremental — quote RTD vencida

### Lacuna identificada

O cenário unitário de quote RTD vencida já validava o fallback para o preço original do snapshot, o status `stale_rtd_quote`, a presença de quote RTD e a classificação de validação como alerta.

Porém, o teste ainda não validava explicitamente os metadados preservados da quote RTD encontrada, deixando incompleta a rastreabilidade do registro RTD efetivamente consultado no cenário de vencimento.

### Ação executada

Foi adicionada cobertura unitária para garantir que, no comportamento atual, uma quote RTD encontrada, porém vencida, preserva:

- `price_resolution_status = stale_rtd_quote`;
- `rtd_quote_found = True`;
- `rtd_validation_status = warn`;
- `rtd_quote_codigo_opcao`;
- `rtd_quote_ativo_base`;
- `rtd_price_source`;
- `rtd_price_updated_at`;
- `rtd_price_created_at`;
- mensagem indicando quote vencida.

Commit:

    c2f6850 test: cobre metadados rtd em quote vencida

### Validação executada

    python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py -q
    21 passed in 1.16s

    python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py ATT/tests/test_rtd_option_quotes_repository_contract.py -q
    32 passed in 1.66s

    git diff --check

### Resultado

A lacuna de rastreabilidade do cenário de quote RTD vencida foi fechada sem alteração funcional.

## Microfatia — Diagnóstico neutro para preço manual

Commit:

- `852d9be test: valida diagnostico neutro em preco manual`

Objetivo:

- Garantir que preço manual explícito seja preservado no canonical pricing sem consulta ao RTD.

Contrato validado:

1. `price` e `premium` preservam o valor manual.
2. `price_source` permanece como `manual`.
3. `price_resolution_status` permanece `ok`.
4. `rtd_quote_found` permanece `None`.
5. `rtd_validation_status` permanece `not_applicable`.
6. `rtd_validation_message` informa que o RTD não foi consultado.
7. Metadados concretos da quote RTD não vazam para a perna manual.
8. O repositório RTD não é chamado.

Evidência:

- `docs/checkpoints/evidencias/fase-6-6-pytest-metadados-rtd-canonical-manual-price.txt`
