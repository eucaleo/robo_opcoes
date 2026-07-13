# Fase 6.5 - Diagnostico das lacunas de cobertura

Marcador inicio: INICIO_AUDITORIA_FASE6_5_DIAGNOSTICO_LACUNAS_COBERTURA_20260713

Data: 13/07/2026

## Natureza

Fase de diagnostico nao destrutivo da frente RTD Excel BTG Online.

Esta etapa investiga por que a regra explicita da Fase 6.4 cobriu apenas parte do historico bruto.

## Objetivo

Diagnosticar lacunas entre:

- `rtd_option_quotes_intraday_history.codigo_opcao`
- `rtd_option_quotes_intraday_history.captured_at`
- `rtd_option_quotes_intraday_candles.symbol`
- `rtd_option_quotes_intraday_candles.bucket_start`
- `rtd_option_quotes_intraday_candles.interval_minutes`

## Guardrails

- Banco aberto em modo somente leitura.
- Nenhum registro removido.
- Nenhum schema alterado.
- Nenhuma compactacao realizada.
- Nenhuma limpeza real autorizada.
- O diagnostico nao equivale a autorizacao de remocao.

## Criterio de aceite

A Fase 6.5 e considerada valida se:

- o script read-only for executado com sucesso;
- o relatorio de lacunas for gerado;
- o relatorio comparar cobertura exata, por simbolo, por data e por proximidade temporal;
- o relatorio declarar explicitamente que limpeza real nao esta aprovada;
- o teste automatizado da Fase 6.5 passar.

## Decisao

A limpeza real permanece bloqueada.

A proxima fase devera consolidar uma interpretacao operacional das lacunas antes de qualquer simulacao de remocao.

Marcador fim: FIM_AUDITORIA_FASE6_5_DIAGNOSTICO_LACUNAS_COBERTURA_20260713
