# Fase 6.6 - Validacao de offset temporal de cobertura

Marcador inicio: INICIO_AUDITORIA_FASE6_6_VALIDACAO_OFFSET_TEMPORAL_COBERTURA_20260713

Data: 13/07/2026

## Natureza

Fase de validacao nao destrutiva da frente RTD Excel BTG Online.

Esta etapa testa se as lacunas identificadas na Fase 6.5 decorrem de diferenca de fuso/offset temporal entre `captured_at` do historico bruto e `bucket_start` dos candles.

## Hipotese

A Fase 6.5 indicou:

- cobertura por simbolo de 60/60;
- cobertura por data e simbolo de 60/60;
- cobertura exata de apenas 10/60;
- buckets do historico deslocados em relacao aos candles.

A hipotese operacional e que aplicar offset horario ao timestamp do historico antes do bucket corrige a cobertura.

## Guardrails

- Banco aberto em modo somente leitura.
- Nenhum registro removido.
- Nenhum schema alterado.
- Nenhuma compactacao realizada.
- Nenhuma limpeza real autorizada.
- Validacao de offset nao equivale a autorizacao de remocao.

## Criterio de aceite

A Fase 6.6 e considerada valida se:

- o script read-only for executado com sucesso;
- o relatorio de offset temporal for gerado;
- o relatorio ranquear offsets candidatos;
- o relatorio declarar explicitamente que limpeza real nao esta aprovada;
- o teste automatizado da Fase 6.6 passar.

## Decisao

A limpeza real permanece bloqueada.

A proxima fase podera consolidar uma proposta de regra de cobertura normalizada, ainda sem execucao destrutiva.

Marcador fim: FIM_AUDITORIA_FASE6_6_VALIDACAO_OFFSET_TEMPORAL_COBERTURA_20260713
