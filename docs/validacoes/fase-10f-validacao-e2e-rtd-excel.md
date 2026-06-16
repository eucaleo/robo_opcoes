# Fase 10f — Validação E2E RTD Excel

Status: **OK / Validada**

## Objetivo

Validar o fluxo E2E real entre:

```text
RTD Excel -> rtd_option_quotes -> CanonicalPricingFacade -> pricing_executions
```

## Contexto

A fase 10f valida operacionalmente que o preço efetivo usado pelo motor canônico de pricing é carregado da tabela `rtd_option_quotes`, usando o campo `ultimo_preco`, e que a rastreabilidade desse preço é preservada no `pricing_payload` persistido.

## Branch validada

```text
fase-10f-validacao-e2e-rtd-excel
```

## Commit base da fase

```text
d2efc2d docs: inicia fase 10f validacao e2e rtd excel
```

## Estrutura temporária usada no E2E

```text
structure_id = 49
alias_legacy_aba = E2E_RTD_PRIO3
underlying_asset = PRIO3
reference_date = 2026-06-15
spot_price = 66.84
```

## Execução validada

```text
pricing_execution_id = 29
execution_status = ok
execution_engine = stub
legs_count = 4
```

## Quotes RTD usadas

Foram validadas as seguintes opções:

```text
PRIOG800
PRIOH515
PRIOS525
PRIOT700
```

## Preços confirmados

Os preços e prêmios das legs vieram de `rtd_option_quotes.ultimo_preco`:

```text
PRIOG800  -> price = 0.09   premium = 0.09
PRIOH515  -> price = 11.90  premium = 11.90
PRIOS525  -> price = 0.31   premium = 0.31
PRIOT700  -> price = 6.63   premium = 6.63
```

## Contrato validado no pricing_payload

Para cada leg, o payload persistido confirmou:

```text
price_source = rtd_option_quotes
rtd_price_field = ultimo_preco
rtd_quote_codigo_opcao = codigo da opção
rtd_quote_ativo_base = PRIO3
rtd_price_source = valor da coluna rtd_option_quotes.source
```

No banco real, a coluna `rtd_option_quotes.source` estava com o valor:

```text
lista_rtd_excel
```

Portanto, o valor persistido abaixo está correto:

```text
rtd_price_source = lista_rtd_excel
```

## Observação sobre rtd_price_source

O campo `rtd_price_source` não representa a tabela usada diretamente pelo pricing.

A tabela usada pelo pricing é indicada por:

```text
price_source = rtd_option_quotes
```

Já o campo `rtd_price_source` reflete a origem interna registrada na própria quote RTD:

```text
rtd_price_source = rtd_option_quotes.source
```

Por isso, no cenário real validado, o valor correto é:

```text
lista_rtd_excel
```

## Resultado da validação corrigida

A validação final confirmou:

```text
structure_id = 49
pricing_execution_id = 29
execution_status = ok
legs_count = 4

E2E OK.
price_source = rtd_option_quotes.
preço/premium vieram de rtd_option_quotes.ultimo_preco.
rtd_price_source reflete a coluna rtd_option_quotes.source.
```

## Limpeza dos dados temporários

Após a validação, os dados temporários do E2E foram removidos:

```text
structures encontradas: [49]
Dados temporários E2E removidos.
```

## Conclusão

A fase 10f está validada.

```text
fase-10f-validacao-e2e-rtd-excel: OK
E2E RTD Excel -> CanonicalPricingFacade -> pricing_executions: OK
```

## Status final

```text
VALIDADA
```
