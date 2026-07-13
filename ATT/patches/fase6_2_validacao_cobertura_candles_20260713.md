# Fase 6.2 - Validação de cobertura dos candles antes de limpeza real

Marcador inicio: INICIO_AUDITORIA_FASE6_2_VALIDACAO_COBERTURA_CANDLES_20260713

Data: 13/07/2026

## Natureza

Fase de validação não destrutiva da frente RTD Excel BTG Online.

Esta etapa avalia a cobertura entre o histórico intraday bruto e os candles consolidados antes de qualquer hipótese de limpeza real.

## Objetivo

Verificar se existem evidências mínimas de cobertura dos dados brutos por candles consolidados.

## Escopo

Tabelas avaliadas:

- `rtd_option_quotes_intraday_history`
- `rtd_option_quotes_intraday_candles`

## Guardrails

- Banco aberto em modo somente leitura.
- Nenhum dado removido.
- Nenhum schema alterado.
- Nenhuma compactação realizada.
- Nenhuma limpeza real autorizada.
- A validação de cobertura não equivale a autorização de remoção.

## Critério de aceite

A Fase 6.2 é considerada válida se:

- o script read-only for executado com sucesso;
- o relatório de cobertura for gerado;
- o relatório declarar explicitamente que limpeza real não está aprovada;
- o teste automatizado da Fase 6.2 passar;
- o commit registrar o caráter bloqueante da fase.

## Decisão

Mesmo que a cobertura não indique lacunas evidentes, a limpeza real permanece bloqueada.

Qualquer remoção futura deverá ser tratada apenas em fase posterior, com aprovação explícita.

Marcador fim: FIM_AUDITORIA_FASE6_2_VALIDACAO_COBERTURA_CANDLES_20260713
