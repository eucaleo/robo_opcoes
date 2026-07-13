# Fase 6.13 - Regularizacao pos-execucao da limpeza real controlada

Marcador inicio: INICIO_FASE6_13_EXECUCAO_REAL_LIMPEZA_CONTROLADA_20260713

Data de geracao: 2026-07-13T17:31:39+00:00

## Natureza

Regularizacao pos-execucao da Fase 6.13.

O diagnostico read-only indicou que a limpeza real ja havia sido executada, mas o script anterior terminou antes de gerar manifesto, relatorio, pytest log, auditoria final e commit.

Esta regularizacao **nao executou novo DELETE**.

## Evidencia de execucao anterior

- IDs elegiveis da Fase 6.12: 60
- IDs elegiveis remanescentes detectados: 0
- Registros removidos detectados: 60
- Tabela historica apos limpeza: 0
- Candles apos limpeza: 110
- SQLite integrity_check: ok

## WAL checkpoint

Foi executado checkpoint SQLite para materializar no arquivo principal a transacao previamente confirmada.

- SHA256 antes do checkpoint: `fa51a7602b6dcc0b66a9f998816c3377872c3131c81c7a5b6ae11f41bc6cfc74`
- SHA256 depois do checkpoint: `fa51a7602b6dcc0b66a9f998816c3377872c3131c81c7a5b6ae11f41bc6cfc74`
- Resultado checkpoint: `[(0, 0, 0)]`

## Banco

- Caminho: `dados/app.db`
- Banco alterado pela execucao original: sim
- Novo DELETE nesta regularizacao: nao
- Integridade final: ok

## Backup e rollback

- Backup primario Fase 6.11: `backups_local/fase6_11_backup_fisico_controlado_20260713/app_fase6_11_backup_fisico_controlado_20260713.db`
- SHA256 backup primario: `2ee46208d4e61574f93c5548c2e081c4f5d6ce052e98b40cfab8f8d046b2f026`
- Backup pre-delete Fase 6.13: `backups_local/fase6_13_pre_delete_safety_20260713/app_fase6_13_pre_delete_safety_20260713.db`
- Backup pre-delete existente: sim
- Backup pos-regularizacao: `backups_local/fase6_13_post_regularizacao_20260713/app_fase6_13_post_regularizacao_20260713.db`
- SHA256 backup pos-regularizacao: `fa51a7602b6dcc0b66a9f998816c3377872c3131c81c7a5b6ae11f41bc6cfc74`
- Integridade backup pos-regularizacao: `ok`
- Rollback disponivel: sim

## Execucao da limpeza

- Tabela alvo: `rtd_option_quotes_intraday_history`
- Coluna alvo: `id`
- IDs elegiveis antes da Fase 6.13: 60
- IDs elegiveis depois detectados: 0
- Registros removidos detectados: 60
- IDs bloqueados: 0
- Novo DELETE durante regularizacao: nao
- IDs removidos: `11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70`

## Preservacao de candles

- Tabela de candles: `rtd_option_quotes_intraday_candles`
- Linhas esperadas: 110
- Linhas detectadas: 110
- Candles modificados: nao

## Resultado

- Status: LIMPEZA_REAL_CONTROLADA_EXECUTADA_REGULARIZADA
- Limpeza real executada: sim
- Limpeza real aprovada: sim
- Regularizacao apenas documental/tecnica: sim
- Novo DELETE executado na regularizacao: nao
- Registros removidos: 60
- IDs elegiveis remanescentes: 0
- Banco alterado: sim
- Rollback documentado: sim
- Candles preservados: sim
- Integridade final: ok
- Fase 6.13 regularizada: sim
- Fase 6.13 encerrada tecnicamente: sim

## Decisao

A Fase 6.13 fica regularizada apos execucao real previamente detectada.

A proxima etapa recomendada e a Fase 6.14 - validacao pos-limpeza, performance e ausencia de regressao.

Marcador fim: FIM_FASE6_13_EXECUCAO_REAL_LIMPEZA_CONTROLADA_20260713
