# Fase 1 - Classificacao inicial das dependencias de derived.db

## Base analisada

Evidencias utilizadas:

- 00_estado_git.txt
- 01_bancos_e_diretorios.txt
- 02_inventario_textual_geral.txt
- 03_inventario_codigo_e_testes.txt
- 04_schema_sqlite.txt
- 05_classificacao_preliminar.txt
- 06_resumo_fase_0.txt

## Estado do repositorio

Branch:

refactor/bd-unico-appdb

HEAD:

9208ae7 Consolida CalculationOrchestrator como orquestrador canonico (#24)

Status observado:

- FRENTE_BD_UNICO_APPDB/ untracked
- docs/ untracked

Decisao:

- A pasta oficial da frente sera FRENTE_BD_UNICO_APPDB/
- A pasta docs/ criada anteriormente sera removida na proxima rodada por estar fora da frente oficial e gerar ruido de inventario

## Bancos fisicos encontrados

Foram encontrados:

- dados/app.db
- dados/derived.db
- dados/backups/app_antes_backfill_position_side_20260627_130330.db
- dados/backups/app_antes_bootstrap_structure_snapshots_20260627_125921.db
- dados/backups/app_antes_limpeza_payoff_20260627_100205.db
- dados/backups/derived_antes_limpeza_payoff_20260627_100206.db

## Diagnostico do schema

### dados/app.db

Tabelas RTD principais presentes:

- rtd_option_quotes
- rtd_underlying_quotes

Contagens observadas:

- rtd_option_quotes: 9 linhas
- rtd_underlying_quotes: 2 linhas

Tabelas de snapshots presentes:

- structure_snapshots
- structure_leg_snapshots

Campos relevantes em structure_snapshots:

- market_json
- metrics_json
- payoff_json
- decision_json
- alerts_json
- operation_state_json

Conclusao:

O app.db ja possui a base necessaria para operar como banco canonico de RTD, snapshots, pricing e payoff agregado.

### dados/derived.db

Tabelas relevantes presentes:

- payoff_curve_points
- rtd_option_quotes
- structure_decisions
- structure_snapshots
- structure_leg_snapshots
- structures
- structure_legs
- pricing_executions

Contagens observadas:

- payoff_curve_points: 808 linhas
- rtd_option_quotes: 11 linhas
- rtd_underlying_quotes: NAO_EXISTE

Conclusao:

O derived.db ainda contem dados e schema historicos. A tabela rtd_option_quotes esta duplicada em relacao ao app.db. A tabela payoff_curve_points existe apenas no derived.db pelo inventario recebido e precisa de decisao funcional antes da remocao fisica do banco.

## Ocorrencias principais

Contagens da Fase 0:

- derived.db: 653
- app.db: 1066
- rtd_option_quotes: 693
- rtd_underlying_quotes: 84

Conclusao:

A remocao deve ser feita por camadas. Nao e seguro apagar dados/derived.db antes de remover dependencias de codigo, testes e scripts.

## Classificacao inicial por grupo

### Grupo A - Migrar ou consolidar em app.db

Arquivos candidatos:

- repositories/rtd_option_quotes_repository.py
- repositories/market_snapshot_repository.py
- services/canonical_pricing_facade.py
- UI/components/terminal_vwap_payoff_dark_panel.py
- infra/bootstrap_rtd_option_quotes_schema.py

Objetivo:

Garantir que RTD de opcoes e ativo objeto sejam lidos e gravados exclusivamente em dados/app.db.

Acao esperada:

- remover qualquer referencia a derived.db
- manter app.db como caminho canonico
- garantir ausencia de fallback para derived.db

### Grupo B - Remover dependencia direta de derived.db

Arquivos candidatos:

- db/config.py
- db/derived_repo.py
- db/writer.py
- db/reader.py
- db/migrations/add_structure_id_to_payoff_curve_points.py
- domain/payoff_features.py
- services/derived_service.py
- services/derived_payoff_persistence.py
- services/payoff_persistence_port.py
- UI/main_window.py
- UI/models/ui_data.py
- UI/components/details_panel.py
- UI/components/structure_editor_dialog.py

Objetivo:

Remover ou adaptar componentes que ainda tratam derived.db como banco operacional.

Acao esperada:

- substituir conexoes para app.db quando a funcionalidade ainda for valida
- remover componentes obsoletos
- eliminar nomes derivados quando deixarem de fazer sentido
- nao criar fallback
- nao criar sincronizacao

### Grupo C - Payoff curve points

Achado:

- dados/derived.db possui payoff_curve_points com 808 linhas
- dados/app.db nao apresentou payoff_curve_points no schema analisado
- dados/app.db possui structure_snapshots.payoff_json

Decisao pendente:

Classificar payoff_curve_points como:

1. funcionalidade ainda necessaria e migrar para app.db; ou
2. artefato historico/regeneravel e remover dependencia; ou
3. substituir por structure_snapshots.payoff_json, se esse for o modelo canonico atual.

Arquivos relacionados:

- db/derived_repo.py
- db/writer.py
- db/reader.py
- services/derived_service.py
- services/derived_payoff_persistence.py
- services/payoff_persistence_port.py
- domain/payoff_features.py
- ATT/tests/test_derived_service.py

### Grupo D - Testes e checks que precisam ser ajustados

Arquivos candidatos:

- ATT/tests/conftest.py
- ATT/tests/test_derived_service.py
- ATT/tests/test_structure_editor_integration.py
- ATT/tests/test_ui_data_migration.py
- ATT/checks/check_end_to_end.py
- ATT/checks/check_structures.py

Objetivo:

Garantir que a suite de testes nao crie, leia, exija ou valide dados/derived.db.

Acao esperada:

- trocar caminhos para app.db quando aplicavel
- remover testes legados de derived.db
- criar testes guardrail garantindo ausencia de derived.db
- corrigir checks para banco unico

### Grupo E - Scripts legados candidatos a remocao

Arquivos candidatos:

- scripts/purge_derived_snapshots.py
- scripts/repair_derived_db_consistency.py
- scripts/run_derived_pipeline.py
- scripts/validate_derived_db.py

Objetivo:

Eliminar scripts que existem apenas para manter, sincronizar, reparar ou validar derived.db.

Acao esperada:

- remover se forem exclusivamente legados
- preservar apenas se forem reescritos para app.db e ainda tiverem utilidade real

### Grupo F - Documentacao/evidencias fora da frente oficial

Achado:

- docs/ aparece como untracked
- docs/auditoria/BD_UNICO_APP_DB.md apareceu no inventario
- docs/auditoria/evidencias/* apareceu no inventario

Decisao:

Remover docs/ na proxima rodada para evitar ruido e manter a frente concentrada em FRENTE_BD_UNICO_APPDB/.

## Riscos identificados

1. Apagar derived.db antes de resolver payoff_curve_points pode causar perda de funcionalidade se ainda houver leitura real dessa tabela.
2. Trocar paths de forma cega pode mascarar dependencias legadas.
3. Testes ainda apontam para derived.db, especialmente ATT/tests/conftest.py.
4. Scripts legados podem recriar derived.db se executados.
5. UI ainda possui referencias diretas ou indiretas a derived.db.

## Ordem recomendada de execucao

1. Remover docs/ untracked fora da frente oficial.
2. Criar evidencia focada apenas em ocorrencias de derived.db.
3. Ajustar configuracao central de banco para app.db.
4. Resolver RTD primeiro, pois app.db ja possui as tabelas.
5. Decidir payoff_curve_points.
6. Adaptar ou remover derived_service, derived_repo, writer e reader.
7. Ajustar UI.
8. Ajustar testes.
9. Remover scripts legados.
10. Remover arquivo fisico dados/derived.db.
11. Criar testes guardrail contra recriacao de derived.db.
12. Rodar suite completa.

## Conclusao da Fase 1 inicial

A arquitetura alvo e viavel porque app.db ja possui as estruturas centrais de RTD, snapshots, pricing e estruturas.

A remocao de derived.db deve prosseguir, mas em ordem controlada.

A proxima acao sera limpar a pasta docs/ criada anteriormente e seguir com busca focada em derived.db para preparar o primeiro patch de codigo.

