# Fase 6.3 - Mapeamento de schema para cobertura de candles

Marcador inicio: INICIO_AUDITORIA_FASE6_3_MAPEAMENTO_SCHEMA_COBERTURA_20260713

Data: 13/07/2026

## Natureza

Fase de mapeamento nao destrutivo da frente RTD Excel BTG Online.

Esta etapa existe porque a Fase 6.2 retornou cobertura nao conclusiva por ausencia de comparacao objetiva de chaves.

## Objetivo

Mapear colunas, cardinalidades e pares candidatos entre:

- `rtd_option_quotes_intraday_history`
- `rtd_option_quotes_intraday_candles`

## Guardrails

- Banco aberto em modo somente leitura.
- Nenhum registro removido.
- Nenhum schema alterado.
- Nenhuma compactacao realizada.
- Nenhuma limpeza real autorizada.
- O mapeamento automatico nao equivale a autorizacao de remocao.

## Critério de aceite

A Fase 6.3 e considerada valida se:

- o script read-only for executado com sucesso;
- o relatorio de schema for gerado;
- o relatorio listar colunas e pares candidatos, quando existirem;
- o relatorio declarar explicitamente que limpeza real nao esta aprovada;
- o teste automatizado da Fase 6.3 passar.

## Decisão

A limpeza real permanece bloqueada.

A proxima fase devera transformar o mapeamento em uma regra explicita de cobertura, ainda sem remocao real.

Marcador fim: FIM_AUDITORIA_FASE6_3_MAPEAMENTO_SCHEMA_COBERTURA_20260713
