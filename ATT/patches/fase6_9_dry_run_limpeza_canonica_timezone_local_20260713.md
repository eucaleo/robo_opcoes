# Fase 6.9 - Dry-run de limpeza com timezone local canonico

Marcador inicio: INICIO_AUDITORIA_FASE6_9_DRY_RUN_LIMPEZA_CANONICA_TIMEZONE_LOCAL_20260713

Data: 13/07/2026

## Natureza

Fase de dry-run nao destrutivo da frente RTD Excel BTG Online.

Esta etapa simula a elegibilidade de linhas do historico bruto para limpeza, usando a regra canonica de timezone local validada na Fase 6.8.

## Contexto

A Fase 6.8 validou cobertura canonica local de 60/60:

- timestamps `+00:00` convertidos para `America/Sao_Paulo`;
- timestamps `-03:00` preservados como horario local equivalente;
- comparacao por simbolo e bucket local.

## Regra de elegibilidade simulada

Uma linha do historico bruto e considerada elegivel no dry-run se:

- possui simbolo valido;
- possui `captured_at` valido;
- o `captured_at` normalizado para `America/Sao_Paulo` gera bucket local esperado;
- existe candle com mesmo simbolo e mesmo bucket local.

## Guardrails

- Banco aberto em modo somente leitura.
- Nenhum registro removido.
- Nenhum schema alterado.
- Nenhuma compactacao realizada.
- Nenhuma limpeza real autorizada.
- Dry-run nao equivale a autorizacao de remocao.

## Criterio de aceite

A Fase 6.9 e considerada valida se:

- o script read-only for executado com sucesso;
- o relatorio de dry-run for gerado;
- o relatorio informar linhas elegiveis e bloqueadas;
- o relatorio usar explicitamente `America/Sao_Paulo`;
- o relatorio declarar explicitamente que limpeza real nao esta aprovada;
- o teste automatizado da Fase 6.9 passar.

## Decisao

A limpeza real permanece bloqueada.

A proxima fase podera preparar um plano operacional de execucao controlada com backup obrigatorio e confirmacao separada.

Marcador fim: FIM_AUDITORIA_FASE6_9_DRY_RUN_LIMPEZA_CANONICA_TIMEZONE_LOCAL_20260713
