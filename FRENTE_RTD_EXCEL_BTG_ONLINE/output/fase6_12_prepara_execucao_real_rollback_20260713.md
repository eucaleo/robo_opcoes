# Fase 6.12 - Preparacao da execucao real controlada com rollback

Marcador inicio: INICIO_FASE6_12_PREPARA_EXECUCAO_REAL_ROLLBACK_20260713

Data de geracao: 2026-07-13T17:11:48+00:00

## Natureza

Preparacao read-only da fase posterior de limpeza real controlada.

Esta fase nao remove registros, nao altera o banco e nao aprova limpeza real.

## Referencias obrigatorias

- Manifesto Fase 6.10: `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_10_manifesto_ids_elegiveis_20260713.json`
- Relatorio Fase 6.10: `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_10_plano_execucao_controlada_backup_20260713.md`
- Manifesto Fase 6.11: `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_11_backup_fisico_controlado_20260713.json`

## Banco atual

- Caminho: `dados/app.db`
- SHA256 atual: `2ee46208d4e61574f93c5548c2e081c4f5d6ce052e98b40cfab8f8d046b2f026`
- SQLite integrity_check: `ok`
- Banco alterado nesta fase: nao

## Backup fisico validado

- Caminho: `backups_local/fase6_11_backup_fisico_controlado_20260713/app_fase6_11_backup_fisico_controlado_20260713.db`
- SHA256 atual do backup: `2ee46208d4e61574f93c5548c2e081c4f5d6ce052e98b40cfab8f8d046b2f026`
- SQLite integrity_check do backup: `ok`
- Backup versionado no Git: nao

## Candidato de limpeza para fase posterior

- Tabela alvo: `rtd_option_quotes_intraday_history`
- Coluna alvo: `id`
- Total atual na tabela alvo: 60
- IDs elegiveis no plano: 60
- IDs elegiveis presentes no banco: 60
- IDs bloqueados: 0
- Menor ID elegivel: 11
- Maior ID elegivel: 70
- Lista de IDs elegiveis: `11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70`

## Preservacao de candles

- Tabela de candles existe: sim
- Linhas em candles antes da fase posterior: 110
- Candles planejados para modificacao: nao

## Plano de rollback documentado

Caso a fase posterior precise ser revertida:

1. Parar qualquer processo que escreva no banco.
2. Preservar uma copia do banco pos-execucao para auditoria, se necessario.
3. Restaurar o arquivo `dados/app.db` a partir do backup `backups_local/fase6_11_backup_fisico_controlado_20260713/app_fase6_11_backup_fisico_controlado_20260713.db`.
4. Calcular SHA256 do banco restaurado.
5. Confirmar que o SHA256 restaurado confere com o SHA256 do backup validado.
6. Executar SQLite integrity_check no banco restaurado.
7. Registrar resultado em auditoria.

## Guardrails obrigatorios para fase posterior

- Branch correta.
- Working tree limpo.
- Processos de escrita parados.
- Backup fisico existente e validado.
- SHA256 atual compativel com Fases 6.10 e 6.11.
- IDs elegiveis conferidos.
- Candles preservados.
- Rollback documentado.
- Confirmacao explicita obrigatoria para limpeza real.

## Resultado

- Status: PRE_FLIGHT_EXECUCAO_REAL_COM_ROLLBACK_PRONTO
- Pre-flight pronto: sim
- Backup validado: sim
- Rollback documentado: sim
- Limpeza real executada: nao
- Limpeza real aprovada: nao
- Registros removidos: 0
- Banco alterado: nao
- Proxima fase exige confirmacao explicita: sim

## Decisao

A Fase 6.12 prepara a execucao real controlada, mas nao executa limpeza.

A limpeza real permanece bloqueada ate a Fase 6.13, se houver confirmacao explicita.

Marcador fim: FIM_FASE6_12_PREPARA_EXECUCAO_REAL_ROLLBACK_20260713
