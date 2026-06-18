# Fase 6.5 — Retomada funcional incremental RTD

## Status

Microfatia 6.5.1 concluída.

## Resumo

Foi adicionada cobertura integrada para CanonicalPricingFacade.execute_pricing quando a quote RTD existe em rtd_option_quotes, mas não possui preço utilizável.

Cenário: ABCD11 com ultimo_preco=0, bid=0 e ask=0.

Resultado esperado: fallback para snapshot, mantendo price=5.55, premium=5.55, price_source=snapshot e price_resolution_status=invalid_rtd_price.

A rastreabilidade RTD foi preservada no payload do motor e no payload de persistência.

## Evidências

Arquivo de evidência: docs/checkpoints/evidencias/fase-6-5-pytest-rtd-canonical-invalid-price-integrado.txt

Resultado registrado: 36 passed in 2.02s.

Validação focada posterior: 1 passed in 1.25s.

## Commit relacionado

c030684 test: cobre fallback quando preco rtd integrado e invalido

## Observação

Nenhuma alteração em UI/API foi realizada. O Excel permanece apenas como gateway RTD.
