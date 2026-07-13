# Fase 6.4 - Regra explicita de cobertura entre historico bruto e candles

Marcador inicio: INICIO_AUDITORIA_FASE6_4_REGRA_EXPLICITA_COBERTURA_20260713

Data: 13/07/2026

## Natureza

Fase de validacao nao destrutiva da frente RTD Excel BTG Online.

Esta etapa transforma o mapeamento da Fase 6.3 em uma regra explicita de cobertura, ainda sem qualquer remocao real.

## Regra escolhida

Com base na Fase 6.3, o par estrutural correto de chave e:

- `rtd_option_quotes_intraday_history.codigo_opcao`
- `rtd_option_quotes_intraday_candles.symbol`

A regra temporal candidata e:

- `rtd_option_quotes_intraday_candles.bucket_start`
- calculado a partir de `rtd_option_quotes_intraday_history.captured_at`
- usando `rtd_option_quotes_intraday_candles.interval_minutes`

## Guardrails

- Banco aberto em modo somente leitura.
- Nenhum registro removido.
- Nenhum schema alterado.
- Nenhuma compactacao realizada.
- Nenhuma limpeza real autorizada.
- Regra validada nao equivale a autorizacao de remocao.

## Criterio de aceite

A Fase 6.4 e considerada valida se:

- o script read-only for executado com sucesso;
- o relatorio da regra explicita for gerado;
- o relatorio mostrar cobertura por intervalo de candle;
- o relatorio declarar explicitamente que limpeza real nao esta aprovada;
- o teste automatizado da Fase 6.4 passar.

## Decisao

A limpeza real permanece bloqueada.

A proxima fase podera consolidar uma proposta operacional de limpeza, ainda em modo simulado ou com aprovacao explicita separada.

Marcador fim: FIM_AUDITORIA_FASE6_4_REGRA_EXPLICITA_COBERTURA_20260713
