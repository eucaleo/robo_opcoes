# Evidências - Fase 6.5 RTD

## Microfatia: cobertura integrada para fallback RTD por asset mismatch

Arquivo alterado:
- ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py

Teste adicionado:
- test_execute_pricing_falls_back_to_snapshot_when_rtd_option_quote_asset_mismatches

Cenário coberto:
- Quote RTD encontrada para ABCD11.
- Quote possui preço válido.
- Quote pertence ao ativo_base WXYZ, divergente do underlying_asset ABCD.
- Preço efetivo volta para snapshot.
- price_resolution_status = rtd_asset_mismatch.
- rtd_validation_status = error.
- rtd_quote_found = True.
- Metadados RTD preservados no payload do engine e no payload persistido.

Validações executadas:
- python -m pytest ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py -q
  Resultado: 5 passed

- python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py ATT/tests/test_rtd_option_quotes_repository_contract.py -q
  Resultado: 32 passed
