# Mapeamento automação opções RTD — ROTA_MESTRE_2 Fase 1

Gerado em: `2026-06-13T20:17:04`

## Escopo

Mapeamento amplo de RTD, Excel, bridge, opções, persistência, serviços e UI.

Nenhuma alteração funcional foi realizada.

## Resumo

- Total de achados: `200`
- Candidatos fortes: `152`
- Candidatos médios: `33`
- Candidatos baixos: `15`

## Candidatos fortes

### `dados/pricing_executions.json`

- Papel provável: `dados_local`
- Pontuação: `821`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'calculo': 1}`
- Hits no conteúdo: `{'opcoes': 502, 'ui': 2, 'calculo': 314}`

### `docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md`

- Papel provável: `docs`
- Pontuação: `565`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'rtd': 1, 'opcoes': 1}`
- Hits no conteúdo: `{'rtd': 84, 'excel': 74, 'bridge': 87, 'opcoes': 35, 'persistencia': 45, 'servicos': 71, 'ui': 125, 'calculo': 38}`

### `docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md`

- Papel provável: `docs`
- Pontuação: `454`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'excel': 1}`
- Hits no conteúdo: `{'rtd': 40, 'excel': 136, 'bridge': 168, 'opcoes': 10, 'persistencia': 51, 'servicos': 12, 'ui': 27, 'calculo': 7}`

### `ATT/tests/test_structure_analysis_service.py`

- Papel provável: `outros`
- Pontuação: `282`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 1}`
- Hits no conteúdo: `{'opcoes': 8, 'servicos': 143, 'ui': 4, 'calculo': 124}`

### `ATT/tests/test_structures_archive_wiring.py`

- Papel provável: `outros`
- Pontuação: `226`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'opcoes': 2, 'persistencia': 33, 'ui': 191}`

### `docs/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md`

- Papel provável: `docs`
- Pontuação: `218`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 25, 'excel': 32, 'bridge': 15, 'opcoes': 8, 'persistencia': 46, 'servicos': 30, 'ui': 52, 'calculo': 10}`

### `ATT/tests/test_pricing_execution_query_service.py`

- Papel provável: `outros`
- Pontuação: `208`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 1, 'calculo': 1}`
- Hits no conteúdo: `{'persistencia': 48, 'servicos': 73, 'calculo': 81}`

### `docs/fase_8_banco_fonte_verdade_auditoria.md`

- Papel provável: `docs`
- Pontuação: `202`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 67, 'excel': 36, 'bridge': 3, 'opcoes': 24, 'persistencia': 11, 'servicos': 7, 'ui': 26, 'calculo': 28}`

### `docs/validacoes/fase-17-mapa-pastas-arquivos.md`

- Papel provável: `docs`
- Pontuação: `195`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'ui': 1}`
- Hits no conteúdo: `{'rtd': 6, 'excel': 28, 'bridge': 32, 'opcoes': 3, 'persistencia': 19, 'servicos': 20, 'ui': 64, 'calculo': 20}`

### `services/calculation_orchestrator.py`

- Papel provável: `services`
- Pontuação: `178`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 2, 'calculo': 1}`
- Hits no conteúdo: `{'rtd': 13, 'opcoes': 45, 'persistencia': 8, 'servicos': 2, 'ui': 11, 'calculo': 90}`

### `docs/baseline_v1.md`

- Papel provável: `docs`
- Pontuação: `176`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 9, 'excel': 31, 'bridge': 5, 'opcoes': 13, 'persistencia': 45, 'servicos': 14, 'ui': 30, 'calculo': 29}`

### `docs/MAPA_MODULOS_FUNCOES.md`

- Papel provável: `docs`
- Pontuação: `175`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 17, 'excel': 15, 'bridge': 3, 'persistencia': 29, 'servicos': 12, 'ui': 31, 'calculo': 68}`

### `docs/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md`

- Papel provável: `docs`
- Pontuação: `173`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'excel': 1, 'bridge': 1}`
- Hits no conteúdo: `{'rtd': 25, 'excel': 45, 'bridge': 61, 'opcoes': 3, 'persistencia': 11, 'servicos': 5, 'ui': 15, 'calculo': 2}`

### `docs/FASE_6_CAMADA_CANONICA_LEITURA.md`

- Papel provável: `docs`
- Pontuação: `169`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 49, 'excel': 16, 'bridge': 22, 'opcoes': 5, 'persistencia': 25, 'servicos': 27, 'ui': 20, 'calculo': 5}`

### `services/canonical_input_service.py`

- Papel provável: `services`
- Pontuação: `165`
- Nota: Prioritário para auditoria de input canônico.
- Hits no caminho: `{'servicos': 3}`
- Hits no conteúdo: `{'rtd': 3, 'bridge': 1, 'opcoes': 4, 'persistencia': 16, 'servicos': 75, 'ui': 4, 'calculo': 33}`

### `db/derived_repo.py`

- Papel provável: `db_infra`
- Pontuação: `150`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'opcoes': 35, 'persistencia': 54, 'calculo': 61}`

### `UI/main_window.py`

- Papel provável: `ui`
- Pontuação: `145`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'ui': 2}`
- Hits no conteúdo: `{'rtd': 1, 'excel': 1, 'bridge': 11, 'opcoes': 8, 'persistencia': 2, 'ui': 68, 'calculo': 48}`

### `ATT/tests/test_pricing_execution_persistence_service.py`

- Papel provável: `outros`
- Pontuação: `141`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 1, 'calculo': 1}`
- Hits no conteúdo: `{'opcoes': 2, 'persistencia': 52, 'servicos': 25, 'calculo': 56}`

### `ATT/tests/test_pricing_execution_controller.py`

- Papel provável: `outros`
- Pontuação: `137`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'calculo': 1}`
- Hits no conteúdo: `{'servicos': 83, 'ui': 12, 'calculo': 39}`

### `ATT/tests/test_pricing_execution_app_service.py`

- Papel provável: `outros`
- Pontuação: `127`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 1, 'calculo': 1}`
- Hits no conteúdo: `{'servicos': 72, 'calculo': 49}`

### `docs/executed_v1.md`

- Papel provável: `docs`
- Pontuação: `123`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 13, 'excel': 12, 'bridge': 12, 'opcoes': 14, 'persistencia': 16, 'servicos': 3, 'ui': 9, 'calculo': 44}`

### `docs/baseline_v1a.md`

- Papel provável: `docs`
- Pontuação: `121`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 24, 'excel': 19, 'bridge': 39, 'persistencia': 15, 'servicos': 4, 'ui': 7, 'calculo': 13}`

### `UI/models/ui_data.py`

- Papel provável: `ui`
- Pontuação: `118`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'ui': 2}`
- Hits no conteúdo: `{'bridge': 4, 'opcoes': 7, 'persistencia': 15, 'ui': 22, 'calculo': 64}`

### `scripts/mapear_automacao_opcoes_rtd.py`

- Papel provável: `scripts`
- Pontuação: `118`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'rtd': 1, 'opcoes': 1}`
- Hits no conteúdo: `{'rtd': 15, 'excel': 10, 'bridge': 15, 'opcoes': 14, 'persistencia': 16, 'servicos': 22, 'ui': 11, 'calculo': 9}`

### `UI/components/details_panel.py`

- Papel provável: `ui`
- Pontuação: `112`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'ui': 3}`
- Hits no conteúdo: `{'opcoes': 5, 'persistencia': 33, 'servicos': 10, 'ui': 16, 'calculo': 39}`

### `ATT/tests/test_pricing_input_service.py`

- Papel provável: `outros`
- Pontuação: `108`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 1, 'calculo': 1}`
- Hits no conteúdo: `{'servicos': 54, 'ui': 11, 'calculo': 37}`

### `services/canonical_pricing_facade.py`

- Papel provável: `services`
- Pontuação: `108`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 2, 'calculo': 1}`
- Hits no conteúdo: `{'rtd': 1, 'opcoes': 5, 'persistencia': 15, 'servicos': 33, 'ui': 3, 'calculo': 42}`

### `docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md`

- Papel provável: `docs`
- Pontuação: `107`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 13, 'excel': 25, 'bridge': 20, 'opcoes': 4, 'persistencia': 10, 'servicos': 13, 'ui': 17, 'calculo': 5}`

### `scripts/patch_derived_payoff_timestamp_consistency.sh`

- Papel provável: `scripts`
- Pontuação: `106`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'calculo': 1}`
- Hits no conteúdo: `{'servicos': 8, 'ui': 13, 'calculo': 82}`

### `services/pricing_execution_persistence_service.py`

- Papel provável: `services`
- Pontuação: `106`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 3, 'calculo': 1}`
- Hits no conteúdo: `{'persistencia': 19, 'servicos': 6, 'ui': 5, 'calculo': 64}`

### `docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md`

- Papel provável: `docs`
- Pontuação: `103`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 13, 'excel': 44, 'bridge': 4, 'opcoes': 3, 'persistencia': 19, 'servicos': 2, 'ui': 14, 'calculo': 4}`

### `services/derived_payoff_persistence.py`

- Papel provável: `services`
- Pontuação: `97`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 2, 'calculo': 1}`
- Hits no conteúdo: `{'servicos': 6, 'ui': 2, 'calculo': 80}`

### `ATT/tests/test_structure_editor_dialog.py`

- Papel provável: `outros`
- Pontuação: `90`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'ui': 1}`
- Hits no conteúdo: `{'opcoes': 19, 'persistencia': 4, 'ui': 64}`

### `ATT/tests/test_structure_editor_integration.py`

- Papel provável: `outros`
- Pontuação: `88`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'opcoes': 6, 'persistencia': 7, 'ui': 75}`

### `bridge_ingest_csv.py`

- Papel provável: `outros`
- Pontuação: `88`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'bridge': 3}`
- Hits no conteúdo: `{'rtd': 8, 'excel': 6, 'bridge': 54, 'persistencia': 6, 'ui': 5}`

### `services/derived_service.py`

- Papel provável: `services`
- Pontuação: `87`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 3}`
- Hits no conteúdo: `{'opcoes': 17, 'persistencia': 7, 'servicos': 6, 'ui': 1, 'calculo': 47}`

### `ATT/tests/test_canonical_input_service.py`

- Papel provável: `outros`
- Pontuação: `84`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 1}`
- Hits no conteúdo: `{'opcoes': 8, 'persistencia': 13, 'servicos': 48, 'ui': 5, 'calculo': 7}`

### `services/pricing_execution_orchestration_service.py`

- Papel provável: `services`
- Pontuação: `84`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 3, 'calculo': 1}`
- Hits no conteúdo: `{'persistencia': 5, 'servicos': 33, 'calculo': 34}`

### `repositories/rtd_option_quotes_repository.py`

- Papel provável: `repositories`
- Pontuação: `82`
- Nota: Prioritário para auditoria de persistência RTD.
- Hits no caminho: `{'rtd': 2, 'opcoes': 1, 'persistencia': 2}`
- Hits no conteúdo: `{'rtd': 14, 'bridge': 1, 'opcoes': 25, 'persistencia': 7}`

### `ATT/tests/test_orchestrator_run_methods.py`

- Papel provável: `outros`
- Pontuação: `81`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 1, 'opcoes': 13, 'servicos': 20, 'calculo': 47}`

### `ATT/tests/test_pricing_execution_orchestration_service.py`

- Papel provável: `outros`
- Pontuação: `75`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 1, 'calculo': 1}`
- Hits no conteúdo: `{'servicos': 39, 'ui': 1, 'calculo': 29}`

### `repositories/market_snapshot_repository.py`

- Papel provável: `repositories`
- Pontuação: `75`
- Nota: Prioritário para auditoria de persistência de snapshot.
- Hits no caminho: `{'persistencia': 2}`
- Hits no conteúdo: `{'rtd': 20, 'excel': 5, 'opcoes': 15, 'persistencia': 9}`

### `ATT/tests/test_robo_legs_repository.py`

- Papel provável: `outros`
- Pontuação: `74`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'persistencia': 1}`
- Hits no conteúdo: `{'rtd': 8, 'excel': 11, 'opcoes': 22, 'persistencia': 30}`

### `mapear_repositorio.sh`

- Papel provável: `outros`
- Pontuação: `70`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 5, 'excel': 8, 'bridge': 12, 'opcoes': 2, 'persistencia': 2, 'ui': 41}`

### `ATT/tests/test_legacy_structure_legs_importer_integration.py`

- Papel provável: `outros`
- Pontuação: `66`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 8, 'excel': 4, 'opcoes': 14, 'persistencia': 35, 'servicos': 4, 'ui': 1}`

### `repositories/structures_repository.py`

- Papel provável: `repositories`
- Pontuação: `66`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'persistencia': 2}`
- Hits no conteúdo: `{'opcoes': 32, 'persistencia': 22, 'ui': 6}`

### `services/structure_analysis_service.py`

- Papel provável: `services`
- Pontuação: `66`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 3}`
- Hits no conteúdo: `{'opcoes': 5, 'servicos': 8, 'ui': 2, 'calculo': 42}`

### `ATT/tests/test_structure_events_api.py`

- Papel provável: `outros`
- Pontuação: `64`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'servicos': 64}`

### `dados/audit_domain_coupling_patch24.json`

- Papel provável: `dados_local`
- Pontuação: `62`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 6, 'excel': 3, 'opcoes': 3, 'persistencia': 18, 'ui': 3, 'calculo': 29}`

### `logs/audit_cleanup_20260602_1203.txt`

- Papel provável: `outros`
- Pontuação: `62`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'persistencia': 6, 'servicos': 12, 'ui': 6, 'calculo': 38}`

### `services/pricing_execution_app_service.py`

- Papel provável: `services`
- Pontuação: `61`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 3, 'calculo': 1}`
- Hits no conteúdo: `{'rtd': 1, 'servicos': 20, 'ui': 1, 'calculo': 27}`

### `UI/components/structure_editor_dialog.py`

- Papel provável: `ui`
- Pontuação: `59`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'ui': 3}`
- Hits no conteúdo: `{'opcoes': 19, 'persistencia': 6, 'ui': 25}`

### `ATT/tests/test_pricing_execution_service.py`

- Papel provável: `outros`
- Pontuação: `57`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 1, 'calculo': 1}`
- Hits no conteúdo: `{'servicos': 17, 'ui': 2, 'calculo': 32}`

### `UI/components/payoff_chart.py`

- Papel provável: `ui`
- Pontuação: `57`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'ui': 2, 'calculo': 1}`
- Hits no conteúdo: `{'opcoes': 10, 'persistencia': 1, 'ui': 11, 'calculo': 26}`

### `ATT/tests/test_system_snapshots_repository.py`

- Papel provável: `outros`
- Pontuação: `56`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'persistencia': 1}`
- Hits no conteúdo: `{'opcoes': 12, 'persistencia': 28, 'ui': 1, 'calculo': 12}`

### `services/market_snapshot_selector.py`

- Papel provável: `services`
- Pontuação: `52`
- Nota: Prioritário para auditoria de seleção de snapshot.
- Hits no caminho: `{'servicos': 3}`
- Hits no conteúdo: `{'rtd': 13, 'persistencia': 6, 'servicos': 4}`

### `ATT/tests/test_legacy_structure_legs_reader.py`

- Papel provável: `outros`
- Pontuação: `50`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 3, 'excel': 3, 'opcoes': 18, 'persistencia': 24, 'servicos': 2}`

### `docs/validacoes/plano-testes-ciclo-2.md`

- Papel provável: `docs`
- Pontuação: `50`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'bridge': 3, 'persistencia': 8, 'servicos': 15, 'ui': 9, 'calculo': 15}`

### `domain/calculation_request.py`

- Papel provável: `outros`
- Pontuação: `50`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'calculo': 1}`
- Hits no conteúdo: `{'rtd': 4, 'bridge': 1, 'opcoes': 26, 'ui': 11, 'calculo': 5}`

### `infra/bootstrap_structures_schema.py`

- Papel provável: `db_infra`
- Pontuação: `50`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'persistencia': 1}`
- Hits no conteúdo: `{'opcoes': 4, 'persistencia': 7, 'calculo': 36}`

### `services/pricing_execution_service.py`

- Papel provável: `services`
- Pontuação: `50`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 3, 'calculo': 1}`
- Hits no conteúdo: `{'servicos': 13, 'ui': 1, 'calculo': 24}`

### `ATT/tests/test_pricing_executions_repository.py`

- Papel provável: `outros`
- Pontuação: `49`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'persistencia': 1, 'calculo': 1}`
- Hits no conteúdo: `{'persistencia': 24, 'ui': 1, 'calculo': 18}`

### `ATT/tests/test_payoff_chart.py`

- Papel provável: `outros`
- Pontuação: `48`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'calculo': 1}`
- Hits no conteúdo: `{'persistencia': 1, 'ui': 17, 'calculo': 27}`

### `ATT/tests/test_robo_legs_status_service.py`

- Papel provável: `outros`
- Pontuação: `47`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 1}`
- Hits no conteúdo: `{'rtd': 22, 'servicos': 22}`

### `repositories/system_snapshots_repository.py`

- Papel provável: `repositories`
- Pontuação: `47`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'persistencia': 2}`
- Hits no conteúdo: `{'opcoes': 4, 'persistencia': 16, 'calculo': 21}`

### `services/pricing_execution_query_service.py`

- Papel provável: `services`
- Pontuação: `47`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 3, 'calculo': 1}`
- Hits no conteúdo: `{'persistencia': 12, 'servicos': 1, 'calculo': 22}`

### `repositories/robo_legs_repository.py`

- Papel provável: `repositories`
- Pontuação: `46`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'persistencia': 2}`
- Hits no conteúdo: `{'rtd': 10, 'excel': 9, 'opcoes': 11, 'persistencia': 10}`

### `docs/SQL_SURFACE_MAP_v2.md`

- Papel provável: `docs`
- Pontuação: `45`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 3, 'excel': 2, 'persistencia': 8, 'servicos': 9, 'ui': 14, 'calculo': 9}`

### `ATT/tests/test_structure_events_service.py`

- Papel provável: `outros`
- Pontuação: `44`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 1}`
- Hits no conteúdo: `{'persistencia': 4, 'servicos': 36, 'ui': 1}`

### `UI/components/structures_list_panel.py`

- Papel provável: `ui`
- Pontuação: `44`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'ui': 3}`
- Hits no conteúdo: `{'opcoes': 5, 'persistencia': 5, 'ui': 25}`

### `scripts/apply_fase9_atomic_create.py`

- Papel provável: `scripts`
- Pontuação: `44`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'opcoes': 4, 'persistencia': 11, 'ui': 29}`

### `db/migrations/add_structure_id_to_payoff_curve_points.py`

- Papel provável: `db_infra`
- Pontuação: `43`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'persistencia': 1, 'calculo': 1}`
- Hits no conteúdo: `{'persistencia': 9, 'calculo': 28}`

### `domain/market_snapshot.py`

- Papel provável: `outros`
- Pontuação: `42`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 5, 'opcoes': 34, 'calculo': 3}`

### `ATT/tests/test_legacy_structure_legs_importer.py`

- Papel provável: `outros`
- Pontuação: `39`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'opcoes': 10, 'persistencia': 27, 'servicos': 2}`

### `ATT/tests/test_structure_events_effective_state.py`

- Papel provável: `outros`
- Pontuação: `39`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'opcoes': 4, 'persistencia': 13, 'servicos': 22}`

### `ATT/tests/test_structure_metrics.py`

- Papel provável: `outros`
- Pontuação: `39`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'calculo': 2}`
- Hits no conteúdo: `{'opcoes': 8, 'calculo': 25}`

### `repositories/pricing_executions_repository.py`

- Papel provável: `repositories`
- Pontuação: `38`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'persistencia': 2, 'calculo': 1}`
- Hits no conteúdo: `{'opcoes': 1, 'persistencia': 8, 'ui': 1, 'calculo': 19}`

### `services/pricing_input_service.py`

- Papel provável: `services`
- Pontuação: `36`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 3, 'calculo': 1}`
- Hits no conteúdo: `{'servicos': 13, 'ui': 4, 'calculo': 7}`

### `repositories/structure_events_repository.py`

- Papel provável: `repositories`
- Pontuação: `35`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'persistencia': 2}`
- Hits no conteúdo: `{'rtd': 2, 'opcoes': 4, 'persistencia': 21, 'ui': 2}`

### `services/market_snapshot_provider.py`

- Papel provável: `services`
- Pontuação: `35`
- Nota: Prioritário para auditoria de snapshot.
- Hits no caminho: `{'servicos': 3}`
- Hits no conteúdo: `{'servicos': 5, 'ui': 1}`

### `services/structure_events_service.py`

- Papel provável: `services`
- Pontuação: `35`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 3}`
- Hits no conteúdo: `{'opcoes': 10, 'persistencia': 14, 'servicos': 1, 'ui': 1}`

### `docs/auditoria_fase_9_cadastro_estruturas.md`

- Papel provável: `docs`
- Pontuação: `34`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'excel': 2, 'persistencia': 15, 'servicos': 5, 'ui': 12}`

### `services/robo_legs_status_service.py`

- Papel provável: `services`
- Pontuação: `34`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 3}`
- Hits no conteúdo: `{'rtd': 8, 'opcoes': 5, 'persistencia': 10, 'servicos': 2}`

### `services/structure_market_input_assembler.py`

- Papel provável: `services`
- Pontuação: `34`
- Nota: Prioritário para auditoria de input de mercado.
- Hits no caminho: `{'servicos': 3}`
- Hits no conteúdo: `{'servicos': 3, 'ui': 2}`

### `db/writer.py`

- Papel provável: `db_infra`
- Pontuação: `33`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'opcoes': 11, 'persistencia': 13, 'calculo': 9}`

### `dados/RTD_LINKS.csv`

- Papel provável: `dados_local`
- Pontuação: `32`
- Nota: Prioritário para auditoria do contrato RTD/Excel.
- Hits no caminho: `{'rtd': 2, 'bridge': 1}`
- Hits no conteúdo: `{'opcoes': 3}`

### `utils/leg_normalizers.py`

- Papel provável: `outros`
- Pontuação: `32`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 4, 'excel': 12, 'opcoes': 15, 'ui': 1}`

### `ATT/checks/check_structures.py`

- Papel provável: `outros`
- Pontuação: `30`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'excel': 4, 'bridge': 11, 'opcoes': 2, 'persistencia': 3, 'ui': 7, 'calculo': 3}`

### `ATT/tests/test_robo_legs_status_repository.py`

- Papel provável: `outros`
- Pontuação: `30`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'persistencia': 1}`
- Hits no conteúdo: `{'rtd': 8, 'excel': 7, 'persistencia': 12}`

### `ATT/tests/test_system_snapshots_schema.py`

- Papel provável: `outros`
- Pontuação: `30`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'persistencia': 1}`
- Hits no conteúdo: `{'opcoes': 2, 'persistencia': 16, 'calculo': 9}`

### `ATT/tests/test_ui_data_migration.py`

- Papel provável: `outros`
- Pontuação: `30`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'persistencia': 1, 'ui': 1}`
- Hits no conteúdo: `{'persistencia': 2, 'ui': 9, 'calculo': 13}`

### `api/structures_controller.py`

- Papel provável: `outros`
- Pontuação: `30`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'opcoes': 2, 'persistencia': 9, 'servicos': 13, 'ui': 5, 'calculo': 1}`

### `ATT/checks/check_end_to_end.py`

- Papel provável: `outros`
- Pontuação: `29`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'excel': 4, 'bridge': 9, 'opcoes': 2, 'persistencia': 3, 'ui': 8, 'calculo': 3}`

### `ATT/checks/check_legs.py`

- Papel provável: `outros`
- Pontuação: `29`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'excel': 2, 'bridge': 26, 'ui': 1}`

### `api/pricing_execution_controller.py`

- Papel provável: `outros`
- Pontuação: `29`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'calculo': 1}`
- Hits no conteúdo: `{'servicos': 10, 'calculo': 16}`

### `domain/payoff_features.py`

- Papel provável: `outros`
- Pontuação: `29`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'calculo': 1}`
- Hits no conteúdo: `{'rtd': 1, 'opcoes': 10, 'persistencia': 13, 'calculo': 2}`

### `ATT/tests/test_structures_repository.py`

- Papel provável: `outros`
- Pontuação: `28`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'persistencia': 1}`
- Hits no conteúdo: `{'opcoes': 16, 'persistencia': 7, 'ui': 2}`

### `docs/AUDITORIA_ROTA_MESTRE_2.md`

- Papel provável: `docs`
- Pontuação: `28`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 6, 'bridge': 3, 'opcoes': 6, 'ui': 13}`

### `domain/payoff.py`

- Papel provável: `outros`
- Pontuação: `28`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'calculo': 1}`
- Hits no conteúdo: `{'opcoes': 16, 'calculo': 9}`

### `domain/decision.py`

- Papel provável: `outros`
- Pontuação: `27`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'opcoes': 8, 'calculo': 19}`

### `repositories/robo_legs_status_repository.py`

- Papel provável: `repositories`
- Pontuação: `26`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'persistencia': 2}`
- Hits no conteúdo: `{'rtd': 3, 'excel': 2, 'opcoes': 6, 'persistencia': 9}`

### `ATT/tests/test_market_snapshot_provider.py`

- Papel provável: `outros`
- Pontuação: `25`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 1}`
- Hits no conteúdo: `{'servicos': 21, 'ui': 1}`

### `scripts/check_rota_desenvolvimento.py`

- Papel provável: `scripts`
- Pontuação: `25`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'excel': 4, 'bridge': 5, 'persistencia': 9, 'ui': 7}`

### `scripts/import_legacy_structure_legs.py`

- Papel provável: `scripts`
- Pontuação: `25`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 1, 'persistencia': 16, 'servicos': 4, 'ui': 4}`

### `services/legacy_robo_legs_fallback.py`

- Papel provável: `services`
- Pontuação: `25`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 2}`
- Hits no conteúdo: `{'opcoes': 9, 'servicos': 10}`

### `services/pricing_engine_stub.py`

- Papel provável: `services`
- Pontuação: `25`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 2, 'calculo': 1}`
- Hits no conteúdo: `{'ui': 2, 'calculo': 14}`

### `ATT/tests/test_pricing_engine_stub.py`

- Papel provável: `outros`
- Pontuação: `23`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'calculo': 1}`
- Hits no conteúdo: `{'servicos': 2, 'ui': 2, 'calculo': 16}`

### `debug_bridge_writer.py`

- Papel provável: `outros`
- Pontuação: `22`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'bridge': 1}`
- Hits no conteúdo: `{'rtd': 1, 'excel': 6, 'bridge': 9, 'persistencia': 2, 'ui': 1}`

### `docs/baseline_v2.md`

- Papel provável: `docs`
- Pontuação: `22`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 5, 'excel': 5, 'bridge': 4, 'persistencia': 2, 'ui': 2, 'calculo': 4}`

### `services/pricing_payload_adapter.py`

- Papel provável: `services`
- Pontuação: `22`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 2, 'calculo': 1}`
- Hits no conteúdo: `{'opcoes': 5, 'ui': 4, 'calculo': 4}`

### `ATT/tests/test_structures_api.py`

- Papel provável: `outros`
- Pontuação: `21`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'opcoes': 10, 'persistencia': 7, 'ui': 4}`

### `db/schema.py`

- Papel provável: `db_infra`
- Pontuação: `21`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'persistencia': 1}`
- Hits no conteúdo: `{'persistencia': 4, 'calculo': 14}`

### `debug_bridge_mainwindow.py`

- Papel provável: `outros`
- Pontuação: `21`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'bridge': 1}`
- Hits no conteúdo: `{'excel': 4, 'bridge': 7, 'persistencia': 2, 'ui': 5}`

### `docs/FASE_7_ISOLAMENTO_NOMES_FISICOS_LEGADOS.md`

- Papel provável: `docs`
- Pontuação: `21`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 4, 'excel': 1, 'bridge': 3, 'persistencia': 1, 'servicos': 6, 'ui': 4, 'calculo': 2}`

### `domain/structure_metrics.py`

- Papel provável: `outros`
- Pontuação: `21`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'calculo': 2}`
- Hits no conteúdo: `{'opcoes': 1, 'calculo': 14}`

### `scripts/apply_fase9_update_tests_atomic_create.py`

- Papel provável: `scripts`
- Pontuação: `21`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'opcoes': 4, 'ui': 17}`

### `services/robo_legs_service.py`

- Papel provável: `services`
- Pontuação: `21`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 3}`
- Hits no conteúdo: `{'rtd': 1, 'opcoes': 2, 'persistencia': 5, 'servicos': 4}`

### `ATT/tests/test_robo_legs_service.py`

- Papel provável: `outros`
- Pontuação: `20`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 1}`
- Hits no conteúdo: `{'opcoes': 4, 'servicos': 13}`

### `repositories/ui_data_table_candidates.py`

- Papel provável: `repositories`
- Pontuação: `20`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'persistencia': 1, 'ui': 1}`
- Hits no conteúdo: `{'rtd': 6, 'persistencia': 1, 'ui': 2, 'calculo': 5}`

### `services/legacy_structure_legs_importer.py`

- Papel provável: `services`
- Pontuação: `20`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 2}`
- Hits no conteúdo: `{'persistencia': 12, 'servicos': 2}`

### `services/legacy_structure_legs_reader.py`

- Papel provável: `services`
- Pontuação: `20`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 2}`
- Hits no conteúdo: `{'rtd': 1, 'excel': 1, 'persistencia': 10, 'servicos': 2}`

### `ATT/tests/test_robo_leg_mapper.py`

- Papel provável: `outros`
- Pontuação: `19`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'opcoes': 17, 'servicos': 2}`

### `ATT/tests/test_structure_events_repository.py`

- Papel provável: `outros`
- Pontuação: `19`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'persistencia': 1}`
- Hits no conteúdo: `{'opcoes': 3, 'persistencia': 12, 'ui': 1}`

### `db/import_excel.py`

- Papel provável: `db_infra`
- Pontuação: `19`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'excel': 1}`
- Hits no conteúdo: `{'excel': 9, 'opcoes': 5, 'persistencia': 2}`

### `services/robo_leg_mapper.py`

- Papel provável: `services`
- Pontuação: `19`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 2}`
- Hits no conteúdo: `{'opcoes': 13}`

### `ATT/tests/conftest.py`

- Papel provável: `outros`
- Pontuação: `18`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'opcoes': 1, 'persistencia': 7, 'ui': 10}`

### `ATT/tests/test_legacy_robo_legs_fallback.py`

- Papel provável: `outros`
- Pontuação: `18`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'opcoes': 4, 'servicos': 14}`

### `ATT/tests/test_pricing_payload_adapter.py`

- Papel provável: `outros`
- Pontuação: `18`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'calculo': 1}`
- Hits no conteúdo: `{'opcoes': 6, 'servicos': 2, 'calculo': 7}`

### `docs/roteiro_v2.md`

- Papel provável: `docs`
- Pontuação: `18`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 3, 'excel': 4, 'bridge': 5, 'ui': 4, 'calculo': 2}`

### `ATT/checks/check_api_routes.py`

- Papel provável: `outros`
- Pontuação: `17`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'excel': 13, 'opcoes': 3, 'ui': 1}`

### `ATT/checks/check_cleanup_residuals.py`

- Papel provável: `outros`
- Pontuação: `17`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'persistencia': 1, 'ui': 12, 'calculo': 4}`

### `UI/debug_utils.py`

- Papel provável: `ui`
- Pontuação: `17`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'ui': 1}`
- Hits no conteúdo: `{'ui': 8, 'calculo': 6}`

### `db/init_excel_schema.py`

- Papel provável: `db_infra`
- Pontuação: `17`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'excel': 1, 'persistencia': 1}`
- Hits no conteúdo: `{'excel': 5, 'persistencia': 6}`

### `limpar_repositorio_seguro.sh`

- Papel provável: `outros`
- Pontuação: `17`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'excel': 12, 'bridge': 1, 'opcoes': 3, 'ui': 1}`

### `db/schema_excel.py`

- Papel provável: `db_infra`
- Pontuação: `16`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'excel': 1, 'persistencia': 1}`
- Hits no conteúdo: `{'excel': 5, 'opcoes': 2, 'persistencia': 2, 'calculo': 1}`

### `docs/validacoes/fechamento-rota-mestre-v1.md`

- Papel provável: `docs`
- Pontuação: `16`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 3, 'excel': 1, 'bridge': 3, 'ui': 9}`

### `services/payoff_persistence_port.py`

- Papel provável: `services`
- Pontuação: `16`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 2, 'calculo': 1}`
- Hits no conteúdo: `{'servicos': 2, 'calculo': 5}`

### `UI/components/decisions_grid.py`

- Papel provável: `ui`
- Pontuação: `15`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'ui': 2}`
- Hits no conteúdo: `{'opcoes': 6, 'persistencia': 1, 'ui': 2}`

### `UI/components/filters_panel.py`

- Papel provável: `ui`
- Pontuação: `15`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'ui': 3}`
- Hits no conteúdo: `{'opcoes': 1, 'ui': 5}`

### `dados/migrations/004_pricing_executions_new_columns.sql`

- Papel provável: `dados_local`
- Pontuação: `15`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'persistencia': 1, 'calculo': 1}`
- Hits no conteúdo: `{'calculo': 9}`

### `repositories/_aba_resolver_mixin.py`

- Papel provável: `repositories`
- Pontuação: `15`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'persistencia': 1}`
- Hits no conteúdo: `{'opcoes': 2, 'persistencia': 9, 'ui': 1}`

### `docs/3B_CLOSURE_REPORT.md`

- Papel provável: `docs`
- Pontuação: `14`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'opcoes': 6, 'servicos': 3, 'ui': 2, 'calculo': 3}`

### `dto/robo_leg_dto.py`

- Papel provável: `outros`
- Pontuação: `14`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'rtd': 2, 'opcoes': 12}`

### `db/reader.py`

- Papel provável: `db_infra`
- Pontuação: `13`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'opcoes': 2, 'persistencia': 4, 'calculo': 7}`

### `debug_bridge_check_after_vba.py`

- Papel provável: `outros`
- Pontuação: `13`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'bridge': 1}`
- Hits no conteúdo: `{'excel': 1, 'bridge': 7, 'ui': 2}`

### `docs/EVOLUCAO_PRICING_PAYOFF.md`

- Papel provável: `docs`
- Pontuação: `13`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'calculo': 2}`
- Hits no conteúdo: `{'calculo': 7}`

### `domain/canonical_validators.py`

- Papel provável: `outros`
- Pontuação: `13`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'opcoes': 4, 'ui': 9}`

### `services/structure_input_mapper.py`

- Papel provável: `services`
- Pontuação: `13`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 2}`
- Hits no conteúdo: `{'opcoes': 6, 'ui': 1}`

### `ATT/tests/test_structure_market_input_assembler.py`

- Papel provável: `outros`
- Pontuação: `12`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'servicos': 1}`
- Hits no conteúdo: `{'opcoes': 2, 'servicos': 5, 'ui': 2}`

### `ATT/tests/test_structures_legs_endpoints.py`

- Papel provável: `outros`
- Pontuação: `12`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'opcoes': 10, 'persistencia': 1, 'ui': 1}`

### `infra/sqlite_conn.py`

- Papel provável: `db_infra`
- Pontuação: `12`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{'persistencia': 1}`
- Hits no conteúdo: `{'opcoes': 2, 'persistencia': 7}`

### `scripts/repair_derived_db_consistency.py`

- Papel provável: `scripts`
- Pontuação: `12`
- Nota: Classificado por frequência de referências.
- Hits no caminho: `{}`
- Hits no conteúdo: `{'persistencia': 4, 'calculo': 8}`

## Candidatos médios

- `ATT/tests/test_derived_service.py` — `outros` — score `11`
- `bridge/analise_robo_legs.csv` — `bridge` — score `11`
- `find_structure.sh` — `outros` — score `11`
- `scripts/run_derived_pipeline.py` — `scripts` — score `11`
- `domain/contracts.py` — `outros` — score `10`
- `ATT/tests/test_decision.py` — `outros` — score `9`
- `ATT/tests/test_payoff_canonical.py` — `outros` — score `9`
- `bridge/analise_robo.csv` — `bridge` — score `9`
- `bridge/hist_robo.csv` — `bridge` — score `9`
- `create_payoff_summary_table.py` — `outros` — score `9`
- `docs/decisions/structure_ref_created_at.md` — `docs` — score `9`
- `src/domain/refs/structure_ref.py` — `outros` — score `9`
- `db/sqlite.py` — `db_infra` — score `7`
- `scripts/apply_fase9_atomic_create.sh` — `scripts` — score `7`
- `scripts/purge_derived_snapshots.py` — `scripts` — score `7`
- `scripts/validate_derived_db.py` — `scripts` — score `7`
- `LISTA_RTD.xlsx` — `outros` — score `6`
- `LISTA_RTD.xlsm` — `outros` — score `6`
- `UI/components/__init__.py` — `ui` — score `6`
- `bridge/analise_raiox.csv` — `bridge` — score `6`
- `bridge/configuracoes.csv` — `bridge` — score `6`
- `bridge/consolidacoes.csv` — `bridge` — score `6`
- `bridge/encerramentos_manuais.csv` — `bridge` — score `6`
- `bridge/rolls_detectados.csv` — `bridge` — score `6`
- `docs/migracoes/fase-14-migracao-dados-legados.md` — `docs` — score `6`
- `docs/validacoes/fase-15-validacao-integrada.md` — `docs` — score `6`
- `dto/robo_legs_status_dto.py` — `outros` — score `6`
- `run_ui.py` — `outros` — score `6`
- `services/__init__.py` — `services` — score `6`
- `ATT/tests/test_structure_input_mapper.py` — `outros` — score `5`
- `db/config.py` — `db_infra` — score `5`
- `validators/leg_validator.py` — `outros` — score `5`
- `validators/validators__init__.py` — `outros` — score `5`

## Candidatos baixos

- `db/init_db.py` — `db_infra` — score `4`
- `docs/3A_CONSOLIDADO.md` — `docs` — score `4`
- `docs/DATABASE_LOCATOR.md` — `docs` — score `4`
- `docs/DB_PATHS.md` — `docs` — score `4`
- `docs/validacoes/fase-16-limpeza-versionamento-release.md` — `docs` — score `4`
- `ATT/tests/test_canonical_validators.py` — `outros` — score `3`
- `UI/__init__.py` — `ui` — score `3`
- `UI/models/__init__.py` — `ui` — score `3`
- `bridge/last_export.txt` — `bridge` — score `3`
- `main.py` — `outros` — score `3`
- `repositories/__init__.py` — `repositories` — score `3`
- `ATT/tests/test_contracts.py` — `outros` — score `2`
- `docs/AUDITORIA_FASE_11_SNAPSHOTS_HISTORICO.md` — `docs` — score `2`
- `validate_db.py` — `outros` — score `2`
- `docs/changelog.md` — `docs` — score `1`

## Decisão

Este relatório serve como base para as próximas fases da ROTA_MESTRE_2.
A Fase 1 não altera UI, banco, schema, cálculo, ingestão ou dados operacionais.