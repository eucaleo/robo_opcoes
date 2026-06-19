# Fase 6.5 — Retomada funcional incremental pós-proteção do contrato RTD

## Objetivo

Executar uma retomada funcional incremental e controlada sobre o fluxo de canonical pricing após a proteção do contrato de leitura RTD.

A fase concentra-se em ampliar a cobertura funcional integrada do uso de RTD no canonical pricing, preservando fallback seguro para snapshot quando a quote RTD não puder ser usada como preço efetivo.

## Escopo executado

- Proteção integrada para quote RTD com preço inválido.
- Proteção integrada para quote RTD stale.
- Proteção integrada para quote RTD com asset mismatch.
- Validação do comportamento em services/canonical_pricing_facade.py por meio de testes de integração.
- Preservação do snapshot como preço efetivo nos cenários em que a quote RTD deve ser rejeitada.
- Preservação dos metadados RTD no payload enviado ao engine e no payload persistido.
- Nenhuma alteração em UI ou API.
- Excel mantido apenas como gateway RTD.

## Microfatia 6.5.1 — Fallback para preço RTD inválido

### Resumo

Foi adicionada cobertura integrada para CanonicalPricingFacade.execute_pricing quando a quote RTD existe em rtd_option_quotes, mas não possui preço utilizável.

Cenário registrado:

- ABCD11 com ultimo_preco = 0.
- bid = 0.
- ask = 0.

Resultado esperado registrado:

- fallback para snapshot.
- price = 5.55.
- premium = 5.55.
- price_source = snapshot.
- price_resolution_status = invalid_rtd_price.
- rastreabilidade RTD preservada no payload do motor e no payload de persistência.

### Evidências

- docs/checkpoints/evidencias/fase-6-5-pytest-rtd-canonical-invalid-price-integrado.txt
- Resultado registrado: 36 passed in 2.02s.
- Validação focada posterior: 1 passed in 1.25s.

### Commit relacionado

- c030684 test: cobre fallback quando preco rtd integrado e invalido

## Microfatia 6.5.2 — Fallback para quote RTD stale

### Resumo

Foi adicionada cobertura integrada para o caso em que a quote RTD está stale e, por isso, o canonical pricing deve preservar o snapshot como fonte efetiva de preço.

### Commit relacionado

- afbce51 test: cobre fallback integrado quando quote rtd esta stale

## Microfatia 6.5.3 — Fallback para asset mismatch

### Arquivo funcional/teste envolvido

- ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py

### Teste adicionado

- test_execute_pricing_falls_back_to_snapshot_when_rtd_option_quote_asset_mismatches

### Comportamento protegido

- Quote RTD encontrada para ABCD11.
- Quote possui preço válido.
- Quote pertence ao ativo_base WXYZ.
- underlying_asset esperado é ABCD.
- O preço efetivo volta para snapshot.
- price_resolution_status = rtd_asset_mismatch.
- rtd_validation_status = error.
- rtd_quote_found = True.
- Metadados RTD permanecem presentes no payload do engine e no payload persistido.

### Validações executadas

- python -m pytest ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py -q
  - Resultado: 5 passed

- python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py ATT/tests/test_rtd_option_quotes_repository_contract.py -q
  - Resultado: 32 passed

- git diff --check
  - Resultado: sem saída, sem problemas de whitespace

### Evidência complementar

- EVIDENCIAS_FASE_6_5_RTD.md

### Commits relacionados

- 82c75c7 test: cover RTD asset mismatch fallback in pricing execution
- 58889f1 docs: add RTD asset mismatch fallback evidence
- fe570fc docs: organize RTD evidence heading

## Resultado consolidado

A Fase 6.5 avançou a retomada funcional incremental do RTD com proteções adicionais no canonical pricing.

O fluxo possui cobertura integrada para rejeitar quote RTD quando o preço está inválido, quando a quote está stale e quando a quote pertence a ativo-base divergente do ativo esperado.

O comportamento esperado nesses cenários é manter o preço de snapshot e registrar status de resolução/validação compatíveis com o motivo do fallback.

Nenhuma alteração em UI/API foi realizada. O Excel permanece apenas como gateway RTD.
