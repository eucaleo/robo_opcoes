# Fase 6.7 - Diagnostico de coortes temporais de cobertura

Marcador inicio: INICIO_AUDITORIA_FASE6_7_DIAGNOSTICO_COORTES_TEMPORAIS_COBERTURA_20260713

Data: 13/07/2026

## Natureza

Fase de diagnostico nao destrutivo da frente RTD Excel BTG Online.

Esta etapa classifica cada linha do historico bruto pelo offset temporal que permite encontrar candle correspondente.

## Contexto

A Fase 6.6 confirmou que o offset `-3h` melhora substancialmente a cobertura, mas ainda deixa 10 linhas sem cobertura.

As lacunas restantes indicam a possibilidade de coortes temporais distintas no historico:

- uma coorte que exige offset `-3h`;
- uma coorte que exige offset `0h`;
- diferenca entre timestamps com timezone explicito e timestamps sem timezone explicito.

## Guardrails

- Banco aberto em modo somente leitura.
- Nenhum registro removido.
- Nenhum schema alterado.
- Nenhuma compactacao realizada.
- Nenhuma limpeza real autorizada.
- Classificacao por coorte nao equivale a autorizacao de remocao.

## Criterio de aceite

A Fase 6.7 e considerada valida se:

- o script read-only for executado com sucesso;
- o relatorio de coortes temporais for gerado;
- o relatorio classificar linhas por offset;
- o relatorio informar distribuicao por timezone explicito;
- o relatorio declarar explicitamente que limpeza real nao esta aprovada;
- o teste automatizado da Fase 6.7 passar.

## Decisao

A limpeza real permanece bloqueada.

A proxima fase podera propor uma regra normalizada de cobertura por coortes, ainda em modo dry-run.

Marcador fim: FIM_AUDITORIA_FASE6_7_DIAGNOSTICO_COORTES_TEMPORAIS_COBERTURA_20260713
