# Fase 6.8 - Validacao da regra canonica de timezone local

Marcador inicio: INICIO_AUDITORIA_FASE6_8_VALIDACAO_REGRA_CANONICA_TIMEZONE_LOCAL_20260713

Data: 13/07/2026

## Natureza

Fase de validacao nao destrutiva da frente RTD Excel BTG Online.

Esta etapa formaliza a regra canonica de timezone local para comparar historico bruto e candles.

## Contexto

A Fase 6.7 confirmou cobertura de 60/60 quando cada linha e classificada pelo offset aplicavel:

- 50 linhas cobertas com equivalencia de conversao UTC para local;
- 10 linhas cobertas sem ajuste adicional porque ja estavam em `-03:00`.

A conclusao operacional e que a regra correta nao e aplicar `-3h` fixo em todos os registros, mas normalizar cada timestamp para `America/Sao_Paulo`.

## Regra canonica

- Se `history.captured_at` tem timezone explicito, converter para `America/Sao_Paulo`.
- Se `history.captured_at` nao tem timezone explicito, assumir que ja esta em `America/Sao_Paulo`.
- Tratar `candles.bucket_start` como horario local operacional.
- Comparar por `codigo_opcao/symbol` e bucket local arredondado pelo intervalo do candle.

## Guardrails

- Banco aberto em modo somente leitura.
- Nenhum registro removido.
- Nenhum schema alterado.
- Nenhuma compactacao realizada.
- Nenhuma limpeza real autorizada.
- Validacao de regra canonica nao equivale a autorizacao de remocao.

## Criterio de aceite

A Fase 6.8 e considerada valida se:

- o script read-only for executado com sucesso;
- o relatorio da regra canonica local for gerado;
- o relatorio informar cobertura pela normalizacao `America/Sao_Paulo`;
- o relatorio declarar explicitamente que limpeza real nao esta aprovada;
- o teste automatizado da Fase 6.8 passar.

## Decisao

A limpeza real permanece bloqueada.

A proxima fase podera consolidar o contrato de dry-run usando esta regra canonica.

Marcador fim: FIM_AUDITORIA_FASE6_8_VALIDACAO_REGRA_CANONICA_TIMEZONE_LOCAL_20260713
