# Fase 6.7 — Consolidação do diagnóstico RTD no canonical pricing

## Objetivo

Consolidar o diagnóstico funcional do canonical pricing para os cenários RTD já protegidos após a retomada controlada da Fase 6.

Esta microfatia não altera UI/API e mantém o Excel apenas como gateway RTD.

## Escopo

Cenários cobertos no recorte atual:

1. preço manual explícito;
2. quote RTD válida;
3. quote RTD ausente;
4. quote RTD vencida/stale;
5. quote RTD com ativo-base divergente;
6. quote RTD com preço inválido;
7. fallback para snapshot;
8. preservação dos metadados RTD no payload calculado e persistido.

## Arquivos funcionais envolvidos

- services/canonical_pricing_facade.py
- repositories/rtd_option_quotes_repository.py

## Testes envolvidos

- ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py
- ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py
- ATT/tests/test_rtd_option_quotes_repository_contract.py
- ATT/tests/test_run_rtd_option_quotes_pipeline.py
- ATT/tests/test_audit_rtd_option_quotes.py
- ATT/tests/test_canonical_pricing_facade_rtd_db_path.py

## Evidências registradas

- docs/checkpoints/evidencias/fase-6-7-inventario-diagnostico-rtd-canonical.txt
- docs/checkpoints/evidencias/fase-6-7-recorte-funcional-rtd-canonical.txt
- docs/checkpoints/evidencias/fase-6-7-pytest-baseline-canonical-rtd.txt
- docs/checkpoints/evidencias/fase-6-7-pytest-baseline-rtd-option-quotes.txt

## Baseline validado

Comando executado:

    python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py

Resultado registrado:

    26 passed in 1.44s

Comando executado:

    python -m pytest ATT/tests -k "rtd_option_quotes"

Resultado registrado:

    25 passed, 634 deselected in 3.06s

## Diagnóstico consolidado

A inspeção e os testes confirmam que o canonical pricing já cobre os principais estados de diagnóstico RTD no recorte atual.

### Preço manual explícito

Comportamento esperado:

- price_source permanece manual;
- price_resolution_status permanece ok;
- rtd_quote_found permanece None;
- rtd_validation_status permanece not_applicable;
- rtd_validation_message informa que o RTD não foi consultado;
- rtd_price_source não é propagado para a leg manual.

### Quote RTD válida

Comportamento esperado:

- price_source passa a rtd_option_quotes;
- price_resolution_status permanece ok;
- rtd_quote_found é True;
- rtd_validation_status é ok;
- rtd_validation_message é None;
- metadados RTD são preservados no payload e na persistência.

### Quote RTD ausente

Comportamento esperado:

- fallback para snapshot quando houver preço original válido;
- price_source permanece snapshot;
- price_resolution_status é missing_rtd_quote;
- rtd_quote_found é False;
- rtd_validation_status é error;
- rtd_validation_message informa que a quote RTD não foi encontrada.

### Quote RTD vencida/stale

Comportamento esperado:

- fallback para snapshot quando houver preço original válido;
- price_source permanece snapshot;
- price_resolution_status é stale_rtd_quote;
- rtd_quote_found é True;
- rtd_validation_status é warn;
- rtd_validation_message informa que a quote RTD está vencida;
- metadados de origem RTD são preservados para rastreabilidade.

### Ativo-base divergente

Comportamento esperado:

- fallback para snapshot quando houver preço original válido;
- price_source permanece snapshot;
- price_resolution_status é rtd_asset_mismatch;
- rtd_quote_found é True;
- rtd_validation_status é error;
- rtd_validation_message informa divergência entre ativo esperado e ativo da quote RTD;
- metadados RTD são preservados para diagnóstico.

### Preço RTD inválido

Comportamento esperado:

- fallback para snapshot quando houver preço original válido;
- price_source permanece snapshot;
- price_resolution_status é invalid_rtd_price;
- rtd_quote_found é True;
- rtd_validation_status é error;
- rtd_validation_message informa ausência de preço RTD utilizável;
- metadados RTD são preservados para diagnóstico.

### Fallback sem repository RTD disponível

Comportamento esperado:

- fallback seguro para snapshot quando houver preço original válido;
- fallback para missing quando não houver preço original válido;
- rtd_quote_found permanece None;
- rtd_validation_status permanece not_applicable;
- rtd_validation_message informa que o repository RTD não está disponível.

## Decisão da microfatia

A Fase 6.7 consolida o diagnóstico funcional RTD no canonical pricing sem mudança funcional ampla.

A base atual está verde e protegida pelos testes focados de canonical pricing e pelo recorte rtd_option_quotes.

## Restrições mantidas

1. nenhuma alteração em UI/API;
2. nenhum banco local versionado;
3. Excel permanece apenas como gateway RTD;
4. scripts legados permanecem congelados até decisão explícita;
5. alterações funcionais futuras devem ser precedidas por teste e evidência;
6. esta microfatia permanece restrita ao diagnóstico RTD/canonical pricing.

## Próxima recomendação

A próxima decisão pode seguir por uma das opções:

1. fechar a Fase 6.7 como consolidação documental e baseline verde;
2. adicionar um teste guardrail de matriz de diagnóstico RTD;
3. avançar para a próxima microfatia funcional controlada.
