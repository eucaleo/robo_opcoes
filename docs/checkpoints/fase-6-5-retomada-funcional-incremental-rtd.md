# Fase 6.5 — Retomada funcional incremental pós-proteção do contrato RTD

## Objetivo

Executar uma retomada funcional incremental e controlada sobre o fluxo de canonical pricing após a proteção do contrato de leitura RTD.

A microfatia desta fase concentrou-se em proteger o comportamento de fallback quando uma quote RTD é encontrada, possui preço válido, mas pertence a ativo-base divergente do ativo esperado.

## Escopo executado

- Proteção integrada do fallback RTD por asset mismatch.
- Validação do comportamento em services/canonical_pricing_facade.py por meio de teste de integração.
- Preservação do snapshot como preço efetivo quando a quote RTD não pertence ao ativo-base esperado.
- Preservação dos metadados RTD no payload enviado ao engine e no payload persistido.
- Nenhuma alteração em UI ou API.
- Excel mantido apenas como gateway RTD.

## Arquivo funcional/teste envolvido

- ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py

## Teste adicionado

- test_execute_pricing_falls_back_to_snapshot_when_rtd_option_quote_asset_mismatches

## Comportamento protegido

- Quote RTD encontrada para ABCD11.
- Quote possui preço válido.
- Quote pertence ao ativo_base WXYZ.
- underlying_asset esperado é ABCD.
- O preço efetivo volta para snapshot.
- price_resolution_status = rtd_asset_mismatch.
- rtd_validation_status = error.
- rtd_quote_found = True.
- Metadados RTD permanecem presentes no payload do engine e no payload persistido.

## Validações executadas

- python -m pytest ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py -q
  - Resultado: 5 passed

- python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py ATT/tests/test_rtd_option_quotes_repository_contract.py -q
  - Resultado: 32 passed

- git diff --check
  - Resultado: sem saída, sem problemas de whitespace

## Evidência complementar

- EVIDENCIAS_FASE_6_5_RTD.md

## Commits relacionados

- 82c75c7 test: cover RTD asset mismatch fallback in pricing execution
- 58889f1 docs: add RTD asset mismatch fallback evidence
- fe570fc docs: organize RTD evidence heading

## Resultado consolidado

A Fase 6.5 avançou a retomada funcional incremental do RTD com uma proteção adicional no canonical pricing.

O fluxo agora possui cobertura integrada para o caso em que a quote RTD existe e tem preço válido, mas é rejeitada por divergência de ativo-base.

O comportamento esperado é manter o preço de snapshot e registrar status de resolução/validação compatíveis com o fallback por asset mismatch.

