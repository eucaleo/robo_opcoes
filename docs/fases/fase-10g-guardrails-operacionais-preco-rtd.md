# Fase 10g — Guardrails Operacionais do Preço RTD

Status: **Em desenvolvimento**

## Objetivo

Endurecer o fluxo operacional de precificação usando RTD para evitar uso silencioso de preços ausentes, inválidos ou inconsistentes.

## Contexto

A fase 10f validou com sucesso o fluxo E2E real:

RTD Excel -> rtd_option_quotes -> CanonicalPricingFacade -> pricing_executions

A fase 10g existe para garantir que falhas operacionais no uso do preço RTD sejam rastreáveis no pricing_payload e não sejam mascaradas como precificação válida.

## Escopo

Esta fase deve tratar principalmente:

- quote RTD ausente;
- preço RTD nulo;
- preço RTD zero ou inválido;
- ativo_base divergente entre estrutura e quote RTD;
- fallback manual ou snapshot sem diagnóstico explícito;
- preservação da rastreabilidade em pricing_payload e pricing_executions.

## Arquivos relevantes

Arquivos mapeados como centrais:

- services/canonical_pricing_facade.py
- repositories/rtd_option_quotes_repository.py
- ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py
- ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py
- ATT/tests/test_pricing_execution_price_source_persistence.py

## Contrato esperado por leg

Cada leg do pricing_payload deve carregar diagnóstico suficiente para auditar a origem do preço.

Campos esperados ou desejáveis:

- price_source
- price_resolution_status
- rtd_quote_found
- rtd_price_field
- rtd_quote_codigo_opcao
- rtd_quote_ativo_base
- rtd_price_source
- rtd_validation_status
- rtd_validation_message

## Regras operacionais

### RTD válido

Quando a quote RTD existir e o preço for válido:

- price_source = rtd_option_quotes
- price_resolution_status = ok
- rtd_quote_found = true
- rtd_validation_status = ok
- rtd_validation_message = null

### Quote RTD ausente

Quando não existir quote RTD para o código da opção:

- rtd_quote_found = false
- price_resolution_status = missing_rtd_quote
- rtd_validation_status = error
- rtd_validation_message deve explicar que a quote RTD não foi encontrada.

O sistema não deve tratar esse cenário como sucesso silencioso.

### Preço RTD inválido

Quando a quote existir, mas o preço não puder ser usado:

- rtd_quote_found = true
- price_resolution_status = invalid_rtd_price
- rtd_validation_status = error
- rtd_validation_message deve explicar que o preço RTD está ausente ou inválido.

Exemplos:

- ultimo_preco nulo;
- ultimo_preco zero sem fallback rastreável;
- preço não numérico;
- bid e ask inválidos quando forem usados como alternativa.

### Ativo base divergente

Quando a quote RTD existir, mas o ativo_base da quote divergir do underlying_asset da estrutura:

- rtd_quote_found = true
- price_resolution_status = rtd_asset_mismatch
- rtd_validation_status = error
- rtd_validation_message deve explicar a divergência.

### Fallback explícito

Quando houver fallback para preço manual ou snapshot, ele deve ser explícito:

- price_source = manual ou snapshot
- price_resolution_status = fallback_manual, fallback_snapshot ou ok

Se o fallback ocorrer porque o RTD falhou, o diagnóstico RTD deve continuar preservado na leg.

## Testes esperados

A fase deve cobrir:

- RTD válido continua funcionando;
- quote RTD ausente é diagnosticada;
- ultimo_preco nulo é diagnosticado;
- preço RTD inválido é diagnosticado;
- ativo_base divergente é diagnosticado;
- fallback manual ou snapshot não apaga diagnóstico RTD;
- pricing_payload preserva diagnóstico operacional por leg;
- persistência preserva campos de guardrail.

## Comandos de validação previstos

- python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py -v
- python -m pytest ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py -v
- python -m pytest ATT/tests/test_pricing_execution_price_source_persistence.py -v
- python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py ATT/tests/test_pricing_execution_price_source_persistence.py -v

## Critério de aceite

A fase será considerada concluída quando:

- falhas RTD forem diagnosticáveis no pricing_payload;
- o fluxo válido da fase 10f continuar passando;
- testes automatizados cobrirem os cenários principais;
- não houver perda de rastreabilidade do preço efetivo;
- não houver fallback silencioso sem status explícito.

## Status final esperado

fase-10g-guardrails-operacionais-preco-rtd: VALIDADA

FIM_DO_DOCUMENTO
