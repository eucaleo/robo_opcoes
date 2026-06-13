# Lista priorizada — automação opções RTD

Documento de encerramento da Fase 1 da `ROTA_MESTRE_2`.

Baseado no relatório automatizado:

- `docs/mapeamento_automacao_opcoes_rtd.md`
- `docs/mapeamento_automacao_opcoes_rtd.json`

## Critério

O relatório bruto identificou muitos candidatos fortes, incluindo documentação, testes e arquivos derivados.

Esta lista reduz o escopo para arquivos operacionais prováveis de:

- RTD/Excel
- bridge/ingestão
- persistência
- snapshot de mercado
- entrada canônica
- cálculo/análise
- UI apenas como consumidora

Nenhuma alteração funcional foi realizada.

## Prioridade P0 — obrigatórios para próximas fases

### `dados/RTD_LINKS.csv`

- Papel provável: `dados_local`
- Score no mapeamento: `32`
- Motivo: Contrato local RTD/Excel. Base para Fase 2.
- Hits no caminho: `{'rtd': 2, 'bridge': 1}`
- Hits no conteúdo: `{'opcoes': 3}`

### `repositories/rtd_option_quotes_repository.py`

- Papel provável: `repositories`
- Score no mapeamento: `82`
- Motivo: Persistência de cotações RTD/opções. Base para Fase 3.
- Hits no caminho: `{'rtd': 2, 'opcoes': 1, 'persistencia': 2}`
- Hits no conteúdo: `{'rtd': 14, 'bridge': 1, 'opcoes': 25, 'persistencia': 7}`

### `services/market_snapshot_provider.py`

- Papel provável: `services`
- Score no mapeamento: `35`
- Motivo: Fornecimento de snapshot de mercado. Base para Fase 4.
- Hits no caminho: `{'servicos': 3}`
- Hits no conteúdo: `{'servicos': 5, 'ui': 1}`

### `services/market_snapshot_selector.py`

- Papel provável: `services`
- Score no mapeamento: `52`
- Motivo: Seleção/fallback de snapshot. Base para Fase 4.
- Hits no caminho: `{'servicos': 3}`
- Hits no conteúdo: `{'rtd': 13, 'persistencia': 6, 'servicos': 4}`

### `repositories/market_snapshot_repository.py`

- Papel provável: `repositories`
- Score no mapeamento: `75`
- Motivo: Persistência de snapshots. Base para Fase 4.
- Hits no caminho: `{'persistencia': 2}`
- Hits no conteúdo: `{'rtd': 20, 'excel': 5, 'opcoes': 15, 'persistencia': 9}`

### `services/structure_market_input_assembler.py`

- Papel provável: `services`
- Score no mapeamento: `34`
- Motivo: Montagem de input de mercado para estruturas. Base para Fase 4.
- Hits no caminho: `{'servicos': 3}`
- Hits no conteúdo: `{'servicos': 3, 'ui': 2}`

### `services/canonical_input_service.py`

- Papel provável: `services`
- Score no mapeamento: `165`
- Motivo: Entrada canônica para cálculo/análise. Base para Fase 4.
- Hits no caminho: `{'servicos': 3}`
- Hits no conteúdo: `{'rtd': 3, 'bridge': 1, 'opcoes': 4, 'persistencia': 16, 'servicos': 75, 'ui': 4, 'calculo': 33}`

## Prioridade P1 — operacionais fortes

- `services/calculation_orchestrator.py` — `services` — score `178`
- `db/derived_repo.py` — `db_infra` — score `150`
- `UI/main_window.py` — `ui` — score `145`
- `UI/models/ui_data.py` — `ui` — score `118`
- `UI/components/details_panel.py` — `ui` — score `112`
- `services/canonical_pricing_facade.py` — `services` — score `108`
- `services/pricing_execution_persistence_service.py` — `services` — score `106`
- `services/derived_payoff_persistence.py` — `services` — score `97`
- `services/derived_service.py` — `services` — score `87`
- `services/pricing_execution_orchestration_service.py` — `services` — score `84`
- `repositories/structures_repository.py` — `repositories` — score `66`
- `services/structure_analysis_service.py` — `services` — score `66`
- `services/pricing_execution_app_service.py` — `services` — score `61`
- `UI/components/structure_editor_dialog.py` — `ui` — score `59`
- `UI/components/payoff_chart.py` — `ui` — score `57`
- `domain/calculation_request.py` — `outros` — score `50`
- `infra/bootstrap_structures_schema.py` — `db_infra` — score `50`
- `services/pricing_execution_service.py` — `services` — score `50`
- `repositories/system_snapshots_repository.py` — `repositories` — score `47`
- `services/pricing_execution_query_service.py` — `services` — score `47`
- `repositories/robo_legs_repository.py` — `repositories` — score `46`
- `UI/components/structures_list_panel.py` — `ui` — score `44`
- `db/migrations/add_structure_id_to_payoff_curve_points.py` — `db_infra` — score `43`
- `domain/market_snapshot.py` — `outros` — score `42`
- `repositories/pricing_executions_repository.py` — `repositories` — score `38`
- `services/pricing_input_service.py` — `services` — score `36`
- `repositories/structure_events_repository.py` — `repositories` — score `35`
- `services/structure_events_service.py` — `services` — score `35`
- `services/robo_legs_status_service.py` — `services` — score `34`
- `db/writer.py` — `db_infra` — score `33`
- `utils/leg_normalizers.py` — `outros` — score `32`
- `domain/payoff_features.py` — `outros` — score `29`
- `domain/payoff.py` — `outros` — score `28`
- `domain/decision.py` — `outros` — score `27`
- `repositories/robo_legs_status_repository.py` — `repositories` — score `26`
- `services/legacy_robo_legs_fallback.py` — `services` — score `25`
- `services/pricing_engine_stub.py` — `services` — score `25`
- `services/pricing_payload_adapter.py` — `services` — score `22`
- `db/schema.py` — `db_infra` — score `21`
- `domain/structure_metrics.py` — `outros` — score `21`
- `services/robo_legs_service.py` — `services` — score `21`
- `repositories/ui_data_table_candidates.py` — `repositories` — score `20`
- `services/legacy_structure_legs_importer.py` — `services` — score `20`
- `services/legacy_structure_legs_reader.py` — `services` — score `20`
- `db/import_excel.py` — `db_infra` — score `19`
- `services/robo_leg_mapper.py` — `services` — score `19`
- `UI/debug_utils.py` — `ui` — score `17`
- `db/init_excel_schema.py` — `db_infra` — score `17`
- `db/schema_excel.py` — `db_infra` — score `16`
- `services/payoff_persistence_port.py` — `services` — score `16`
- `UI/components/decisions_grid.py` — `ui` — score `15`
- `UI/components/filters_panel.py` — `ui` — score `15`
- `repositories/_aba_resolver_mixin.py` — `repositories` — score `15`
- `dto/robo_leg_dto.py` — `outros` — score `14`
- `db/reader.py` — `db_infra` — score `13`
- `domain/canonical_validators.py` — `outros` — score `13`
- `services/structure_input_mapper.py` — `services` — score `13`
- `infra/sqlite_conn.py` — `db_infra` — score `12`

## Prioridade P2 — operacionais médios

- `bridge/analise_robo_legs.csv` — `bridge` — score `11`
- `domain/contracts.py` — `outros` — score `10`
- `bridge/analise_robo.csv` — `bridge` — score `9`
- `bridge/hist_robo.csv` — `bridge` — score `9`
- `db/sqlite.py` — `db_infra` — score `7`
- `UI/components/__init__.py` — `ui` — score `6`
- `bridge/analise_raiox.csv` — `bridge` — score `6`
- `bridge/configuracoes.csv` — `bridge` — score `6`
- `bridge/consolidacoes.csv` — `bridge` — score `6`
- `bridge/encerramentos_manuais.csv` — `bridge` — score `6`
- `bridge/rolls_detectados.csv` — `bridge` — score `6`
- `dto/robo_legs_status_dto.py` — `outros` — score `6`
- `services/__init__.py` — `services` — score `6`
- `db/config.py` — `db_infra` — score `5`
- `validators/leg_validator.py` — `outros` — score `5`
- `validators/validators__init__.py` — `outros` — score `5`

## Arquivos tratados como ruído nesta fase

Foram considerados ruído para priorização operacional:

- documentação histórica em `docs/`
- testes em `ATT/tests/` e `tests/`
- relatórios temporários
- arquivos derivados ou volumosos sem papel claro no fluxo RTD

Esses arquivos continuam disponíveis no mapeamento bruto, mas não direcionam as próximas fases.

## Decisão de encerramento da Fase 1

A Fase 1 fica encerrada com a seguinte orientação:

1. Fase 2 deve auditar o contrato RTD/Excel e arquivos de entrada.
2. Fase 3 deve auditar persistência de cotações RTD/opções.
3. Fase 4 deve auditar snapshot, seleção de fonte, entrada canônica e consumo pela UI.

Nenhuma mudança funcional está autorizada por este documento.