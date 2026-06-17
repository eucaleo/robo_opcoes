# Checkpoint — Fase 6 — Mapa de impacto rtd_option_quotes

## Contexto

Este documento prepara a Fase 6 da ROTA_MESTRE_3 após a reconciliação funcional da tabela rtd_option_quotes e da ponte LISTA_RTD.xlsm -> RTD_OPTION_QUOTES -> rtd_option_quotes.

## Objetivo

Mapear impactos antes de qualquer alteração em UI, API, repository, service, scripts operacionais, testes ou documentação.

## Estado validado até a Fase 5

- Banco operacional: dados/app.db
- Tabela reconciliada: rtd_option_quotes
- Workbook oficial validado: LISTA_RTD.xlsm
- Aba tabular validada: RTD_OPTION_QUOTES
- Tickers validados: PRIOG800, PRIOH515, PRIOT700, PRIOS525

## Commits de referência

- b8a3201 fix: importa cotações RTD de opções e fecha Excel corretamente
- 3d2218e docs: registra reconciliação rtd option quotes e RTD Excel
- 7d32d79 chore: atualiza workbook RTD option quotes validado
- 1c3850d docs: adiciona evidencias da reconciliacao rtd option quotes

## Impactos por camada

### Banco de dados

- Objeto principal: rtd_option_quotes
- Riscos: schema divergente, campos inexistentes, dados stale, registros ausentes ou duplicados.

### Excel e RTD

- Objeto principal: LISTA_RTD.xlsm
- Aba operacional: RTD_OPTION_QUOTES
- Riscos: alteração manual de layout, Excel aberto, RTD sem atualização, falha COM silenciosa.

### Scripts operacionais

- Scripts relacionados: run_lista_rtd_option_quotes_pipeline.py, audit_rtd_option_quotes.py, bootstrap_rtd_option_quotes_schema.py
- Riscos: acoplamento ao nome da aba, dependência Windows/Excel, divergência entre ambiente local e CI.

### Repository

- Impacto esperado: centralizar consultas SQL de rtd_option_quotes.
- Riscos: SQL duplicado, acesso direto ao banco, falta de tratamento para dado ausente ou stale.

### Service

- Impacto esperado: expor consulta e status operacional das cotações RTD de opções.
- Riscos: misturar coleta RTD com cálculo de estratégia, mascarar ausência de dados, expor dado defasado.

### API

- Impacto esperado: possível endpoint de consulta e possível endpoint de status/auditoria.
- Riscos: contrato instável, campos internos expostos, erro inadequado para ausência de cotação.

### UI

- Impacto esperado: exibir cotações, última atualização, status stale e ausência de cotação.
- Riscos: exibir cotação sem timestamp, bloquear tela por dependência do Excel, esconder falhas de coleta.

### Testes

- Impacto esperado: testes de repository, service, auditoria e contrato de API se houver endpoint.
- Riscos: testes frágeis dependentes de Excel real e ausência de fixtures representativas.

## Termos que devem ser varridos

- rtd_option_quotes
- LISTA_RTD.xlsm
- RTD_OPTION_QUOTES
- run_lista_rtd_option_quotes_pipeline
- audit_rtd_option_quotes
- bootstrap_rtd_option_quotes_schema

## Comando recomendado de varredura

grep -RIn -e "rtd_option_quotes" -e "LISTA_RTD.xlsm" -e "RTD_OPTION_QUOTES" -e "run_lista_rtd_option_quotes_pipeline" -e "audit_rtd_option_quotes" -e "bootstrap_rtd_option_quotes_schema" . --exclude-dir=.git --exclude-dir=.venv --exclude-dir=venv --exclude-dir=__pycache__ --exclude="*.db" --exclude="*.xlsm"

## Critério de avanço

A Fase 6 só deve avançar para alteração em UI, API, repository ou service depois que o mapa de impacto estiver versionado, a varredura real tiver sido executada, os arquivos impactados tiverem sido classificados e os riscos de stale data e ausência de cotação tiverem tratamento definido.

## Decisão

A Fase 6 fica aberta como etapa de análise de impacto.

Nenhuma alteração funcional em UI, API, repository ou service deve ser feita antes da conclusão da varredura real de referências.
