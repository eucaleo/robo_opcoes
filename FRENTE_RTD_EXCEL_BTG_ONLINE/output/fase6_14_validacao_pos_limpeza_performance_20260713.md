# Fase 6.14 - Validacao pos-limpeza, performance e ausencia de regressao

Marcador inicio: INICIO_FASE6_14_VALIDACAO_POS_LIMPEZA_PERFORMANCE_20260713

Data de geracao: 2026-07-13T17:45:09+00:00

## Natureza

Validacao read-only do estado pos-limpeza da Fase 6.13.

Esta fase nao executa operacoes destrutivas nem modificadoras no banco.

## Referencia da Fase 6.13

- Manifesto: `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_13_execucao_real_limpeza_controlada_20260713.json`
- Limpeza real executada: True
- Regularizacao apenas documental/tecnica: True
- Registros removidos: 60
- Candles preservados: True
- Status Fase 6.13: `REGULARIZADA_POS_EXECUCAO`

## Banco

- Caminho: `dados/app.db`
- Modo de abertura: read-only
- SHA256 antes: `fa51a7602b6dcc0b66a9f998816c3377872c3131c81c7a5b6ae11f41bc6cfc74`
- SHA256 depois: `fa51a7602b6dcc0b66a9f998816c3377872c3131c81c7a5b6ae11f41bc6cfc74`
- Hash inalterado: sim
- Banco modificado nesta fase: nao
- SQLite integrity_check: `ok`

## Validacao pos-limpeza

- Tabela historica: `rtd_option_quotes_intraday_history`
- Total esperado na historica: 0
- Total detectado na historica: 0
- IDs elegiveis verificados: 60
- IDs elegiveis remanescentes: 0
- Tabela candles: `rtd_option_quotes_intraday_candles`
- Total esperado de candles: 110
- Total detectado de candles: 110

## Performance

Limite adotado por consulta: 2000.00 ms

- integrity_check_ms: 10.149
- history_total_ms: 0.085
- candles_total_ms: 0.053
- eligible_ids_remaining_ms: 0.188
- Maior tempo medido: 10.149 ms
- Performance validada: sim

## Ausencia de regressao

- Integridade ok: sim
- Historico limpo: sim
- IDs elegiveis ausentes: sim
- Candles preservados: sim
- Hash do banco inalterado durante validacao: sim
- Operacao de escrita executada: nao

## Resultado

- Status: FASE6_14_VALIDACAO_POS_LIMPEZA_PERFORMANCE_APROVADA
- Pos-limpeza validado: sim
- Performance validada: sim
- Ausencia de regressao: sim
- Banco modificado: nao
- Integridade final: ok
- Fase 6.14 encerrada tecnicamente: sim

## Decisao

A Fase 6.14 valida o estado pos-limpeza da Fase 6.13 sem modificar o banco.

Proxima etapa recomendada: Fase 6.15 - encerramento da frente e consolidacao final.

Marcador fim: FIM_FASE6_14_VALIDACAO_POS_LIMPEZA_PERFORMANCE_20260713
