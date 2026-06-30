# Mapa compacto de alvos RTD - Fase 0.2

Data: 30/06/2026 16:09:19
Raiz: C:/Users/eucal/projeto

## 1. Git

### Branch

```text
patch-side-actions-structures
```

### Status

```text
M UI/components/terminal_vwap_payoff_dark_panel.py
 M UI/components/terminal_vwap_payoff_panel.py
 M UI/main_window.py
?? ATT/patches/
?? UI/components/structure_editor_dialog.py.bak_rtd_fill_20260629_225017
?? UI/components/terminal_vwap_payoff_dark_panel.py.bak_fix_justify_20260629_191010
?? UI/components/terminal_vwap_payoff_dark_panel.py.bak_side_actions_fix
?? UI/components/terminal_vwap_payoff_dark_panel.py.bak_vwap_underlying
?? UI/main_window.py.bak_dark_layout_20260629_190807
?? UI/main_window.py.bak_terminal_operacional_20260629_185045
?? docs/AUDITORIA_RTD_EXCEL_VIVO.md
?? docs/PLANO_RTD_EXCEL_VIVO.md
?? docs/levantamentos/
?? scripts/refresh_rtd_option_quotes_excel.ps1
?? scripts/rtd_auditoria_fase0.sh
?? scripts/rtd_consulta_projeto.sh
?? scripts/rtd_mapa_alvos_fase0.py
?? scripts/rtd_mapa_alvos_fase0.sh
?? scripts/rtd_rodar_fase0.sh
```

### Ultimo commit

```text
5c6ae78 feat: integra preenchimento de legs com cache RTD de opcoes
```

## 2. Arquivos-chave esperados

- `scripts/refresh_rtd_option_quotes_excel.ps1`: existe; 167 linhas
- `scripts/refresh_rtd_symbol_to_option_quotes.py`: existe; 329 linhas
- `scripts/refresh_rtd_symbol_to_option_quotes_fallback.py`: existe; 163 linhas
- `scripts/import_rtd_option_quotes_wide_csv.py`: existe; 342 linhas
- `scripts/run_derived_pipeline.py`: existe; 74 linhas
- `repositories/rtd_option_quotes_repository.py`: existe; 127 linhas
- `repositories/market_snapshot_repository.py`: existe; 403 linhas
- `services/market_snapshot_provider.py`: existe; 70 linhas
- `services/market_snapshot_selector.py`: existe; 136 linhas
- `services/structure_leg_rtd_enrichment_service.py`: existe; 123 linhas
- `services/structure_market_input_assembler.py`: existe; 37 linhas
- `services/pricing_input_service.py`: existe; 30 linhas
- `services/canonical_input_service.py`: existe; 425 linhas
- `services/canonical_pricing_facade.py`: existe; 426 linhas
- `infra/bootstrap_rtd_option_quotes_schema.py`: existe; 184 linhas
- `UI/components/structure_editor_dialog.py`: existe; 646 linhas
- `UI/components/terminal_vwap_payoff_dark_panel.py`: existe; 1485 linhas
- `UI/components/terminal_vwap_payoff_panel.py`: existe; 666 linhas
- `UI/main_window.py`: existe; 118 linhas
- `controllers/terminal_vwap_payoff_controller.py`: existe; 153 linhas
- `services/terminal_vwap_payoff_app_service.py`: existe; 369 linhas

## 3. Banco derived.db

Banco encontrado: dados/derived.db

### Tabelas

- payoff_curve_points
- pricing_executions
- rtd_option_quotes
- sqlite_sequence
- structure_audit_log
- structure_decisions
- structure_leg_snapshots
- structure_legs
- structure_snapshots
- structures

### Tabelas focadas

- payoff_curve_points
- rtd_option_quotes
- structure_decisions
- structure_leg_snapshots
- structure_snapshots

### Schema tabela `payoff_curve_points`

```text
(0, 'timestamp', 'TEXT', 1, None, 0)
(1, 'aba', 'TEXT', 1, None, 0)
(2, 'structure_id', 'INTEGER', 0, None, 0)
(3, 'spot_ref', 'REAL', 0, None, 0)
(4, 'point_spot', 'REAL', 1, None, 0)
(5, 'point_pl', 'REAL', 1, None, 0)
(6, 'meta_json', 'TEXT', 0, None, 0)
(7, 'created_at', 'TEXT', 0, "datetime('now')", 0)
```

### Indices tabela `payoff_curve_points`

```text
(0, 'ix_payoff_structure_id', 0, 'c', 0)
(1, 'ux_payoff_snapshot', 1, 'c', 0)
```

Total de linhas em `payoff_curve_points`: 808

### Schema tabela `rtd_option_quotes`

```text
(0, 'id', 'INTEGER', 0, None, 1)
(1, 'codigo_opcao', 'TEXT', 1, None, 0)
(2, 'ativo_base', 'TEXT', 0, None, 0)
(3, 'call_put', 'TEXT', 0, None, 0)
(4, 'strike', 'REAL', 0, None, 0)
(5, 'vencimento', 'TEXT', 0, None, 0)
(6, 'ultimo_preco', 'REAL', 0, None, 0)
(7, 'ultima_quantidade', 'REAL', 0, None, 0)
(8, 'bid', 'REAL', 0, None, 0)
(9, 'ask', 'REAL', 0, None, 0)
(10, 'volume', 'REAL', 0, None, 0)
(11, 'iv', 'REAL', 0, None, 0)
(12, 'delta', 'REAL', 0, None, 0)
(13, 'gamma', 'REAL', 0, None, 0)
(14, 'theta', 'REAL', 0, None, 0)
(15, 'vega', 'REAL', 0, None, 0)
(16, 'source', 'TEXT', 1, "'rtd_links'", 0)
(17, 'raw_json', 'TEXT', 0, None, 0)
(18, 'updated_at', 'TEXT', 1, 'CURRENT_TIMESTAMP', 0)
(19, 'created_at', 'TEXT', 1, 'CURRENT_TIMESTAMP', 0)
(20, 'vwap', 'REAL', 0, None, 0)
```

### Indices tabela `rtd_option_quotes`

```text
(0, 'idx_rtd_option_quotes_codigo_opcao', 0, 'c', 0)
(1, 'sqlite_autoindex_rtd_option_quotes_1', 1, 'u', 0)
```

Total de linhas em `rtd_option_quotes`: 11

### Amostra `rtd_option_quotes`

```text
colunas: id, codigo_opcao, ativo_base, call_put, strike, vencimento, ultimo_preco, ultima_quantidade, bid, ask, volume, iv, delta, gamma, theta, vega, source, raw_json, updated_at, created_at, vwap
(1, 'PRIOG800', 'PRIO3', 'CALL', 80.0, '2026-07-17', 0.02, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0085, 0.0027, -0.0069, 0.3012, 'BTG_RTD_EXCEL', '{"codigo_opcao": "PRIOG800", "ativo_base": "PRIO3", "call_put": "Call", "strike": "80", "vencimento": "46220,125", "ultimo_preco": "0,02", "ultima_quantidade": "0", "bid": "0", "ask": "0", "volume": "0", "iv": "0", "delta": "0,0085", "gamma": "0,0027", "theta": "-0,0069", "vega": "0,3012"}', '2026-06-27 14:07:04', '2026-06-18 08:47:20', None)
(2, 'PRIOH515', 'PRIO3', 'CALL', 51.5, '2026-08-21', 5.03, 0.0, 4.74, 4.8, 0.0, 0.0, 0.7026, 0.0446, -0.0512, 7.5124, 'BTG_RTD_EXCEL', '{"codigo_opcao": "PRIOH515", "ativo_base": "PRIO3", "call_put": "Call", "strike": "51,5", "vencimento": "46255,125", "ultimo_preco": "5,03", "ultima_quantidade": "0", "bid": "4,74", "ask": "4,8", "volume": "0", "iv": "0", "delta": "0,7026", "gamma": "0,0446", "theta": "-0,0512", "vega": "7,5124"}', '2026-06-25 10:22:27', '2026-06-18 08:47:20', None)
(3, 'PRIOS525', 'PRIO3', 'PUT', 52.5, '2026-07-17', 1.05, 400.0, 0.05, 1.99, 51855.6, 0.0, -0.3706, 0.0961, -0.0378, 4.9032, 'BTG_RTD_EXCEL', '{"codigo_opcao": "PRIOS525", "ativo_base": "PRIO3", "call_put": "Put", "strike": "52,5", "vencimento": "46220,125", "ultimo_preco": "1,05", "ultima_quantidade": "400", "bid": "0,05", "ask": "1,99", "volume": "51855,6", "iv": "0", "delta": "-0,3706", "gamma": "0,0961", "theta": "-0,0378", "vega": "4,9032"}', '2026-06-27 14:07:04', '2026-06-18 08:47:20', None)
(4, 'PRIOT700', 'PRIO3', 'PUT', 70.0, '2026-08-21', 12.03, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0384, 0.0, 'BTG_RTD_EXCEL', '{"codigo_opcao": "PRIOT700", "ativo_base": "PRIO3", "call_put": "Put", "strike": "70", "vencimento": "46255,125", "ultimo_preco": "12,03", "ultima_quantidade": "0", "bid": "0", "ask": "0", "volume": "0", "iv": "0", "delta": "-1", "gamma": "0", "theta": "0,0384", "vega": "0"}', '2026-06-27 14:07:04', '2026-06-18 08:47:20', None)
(5, 'PRIOH505', 'PRIO3', 'CALL', 50.5, '2026-08-21', 4.97, 6300.0, 0.0, 0.0, 66035.2, 0.0, 0.7398, 0.0473, -0.0471, 6.8781, 'BTG_RTD_EXCEL', '{"codigo_opcao": "PRIOH505", "ativo_base": "PRIO3", "call_put": "Call", "strike": "50,5", "vencimento": "46255,125", "ultimo_preco": "4,97", "ultima_quantidade": "6300", "bid": "0", "ask": "0", "volume": "66035,2", "iv": "0", "delta": "0,7398", "gamma": "0,0473", "theta": "-0,0471", "vega": "6,8781"}', '2026-06-27 14:07:04', '2026-06-25 11:36:35', None)
(6, 'BOVAH186', 'BOVA11', 'CALL', 186.0, '2026-08-21', 1.12, 10.0, 0.5, 1.42, 92937.2, 0.0, 0.1823, 0.0227, -0.0553, 17.9731, 'BTG_RTD_EXCEL', '{"codigo_opcao": "BOVAH186", "ativo_base": "BOVA11", "call_put": "Call", "strike": "186", "vencimento": "46255,125", "ultimo_preco": "1,12", "ultima_quantidade": "10", "bid": "0,5", "ask": "1,42", "volume": "92937,2", "iv": "0", "delta": "0,1823", "gamma": "0,0227", "theta": "-0,0553", "vega": "17,9731"}', '2026-06-27 14:07:04', '2026-06-25 11:36:35', None)
(7, 'BOVAG34', 'BOVA11', 'CALL', 157.0, '2026-07-17', 14.64, 1.0, 9.75, 0.0, 229439.48, 0.0, 1.0, 0.0, -0.0874, 0.0, 'BTG_RTD_EXCEL', '{"codigo_opcao": "BOVAG34", "ativo_base": "BOVA11", "call_put": "Call", "strike": "157", "vencimento": "46220,125", "ultimo_preco": "14,64", "ultima_quantidade": "1", "bid": "9,75", "ask": "0", "volume": "229439,48", "iv": "0", "delta": "1", "gamma": "0", "theta": "-0,0874", "vega": "0"}', '2026-06-27 14:07:04', '2026-06-25 11:36:35', None)
(8, 'BOVAS61', 'BOVA11', 'PUT', 184.0, '2026-07-17', 12.32, 60.0, 11.9, 0.0, 66076.15, 0.0, -0.8991, 0.02, 0.041, 7.3509, 'BTG_RTD_EXCEL', '{"codigo_opcao": "BOVAS61", "ativo_base": "BOVA11", "call_put": "Put", "strike": "184", "vencimento": "46220,125", "ultimo_preco": "12,32", "ultima_quantidade": "60", "bid": "11,9", "ask": "0", "volume": "66076,15", "iv": "0", "delta": "-0,8991", "gamma": "0,02", "theta": "0,041", "vega": "7,3509"}', '2026-06-27 14:07:04', '2026-06-25 11:36:35', None)
(9, 'BOVAT158', 'BOVA11', 'PUT', 158.0, '2026-08-21', 0.63, 300.0, 0.59, 2.03, 22295.67, 0.0, -0.0965, 0.0128, -0.019, 11.6163, 'BTG_RTD_EXCEL', '{"codigo_opcao": "BOVAT158", "ativo_base": "BOVA11", "call_put": "Put", "strike": "158", "vencimento": "46255,125", "ultimo_preco": "0,63", "ultima_quantidade": "300", "bid": "0,59", "ask": "2,03", "volume": "22295,67", "iv": "0", "delta": "-0,0965", "gamma": "0,0128", "theta": "-0,019", "vega": "11,6163"}', '2026-06-27 14:07:04', '2026-06-25 11:36:35', None)
(10, 'BOVAK900', 'BOVA11', 'CALL', 90.0, '2026-11-19', 82.93, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, -0.0475, 0.0, 'BTG_RTD_EXCEL', '{"codigo_opcao": "BOVAK900", "ativo_base": "BOVA11", "call_put": "Call", "strike": "90", "vencimento": "46345,125", "ultimo_preco": "82,93", "ultima_quantidade": "0", "bid": "0", "ask": "0", "volume": "0", "iv": "0", "delta": "1", "gamma": "0", "theta": "-0,0475", "vega": "0", "vwap": "0"}', '2026-06-30 14:21:21', '2026-06-30 11:33:37', 0.0)
```

### Schema tabela `structure_decisions`

```text
(0, 'id', 'INTEGER', 0, None, 1)
(1, 'timestamp', 'TEXT', 1, None, 0)
(2, 'aba', 'TEXT', 1, None, 0)
(3, 'decision', 'TEXT', 1, None, 0)
(4, 'level', 'INTEGER', 1, None, 0)
(5, 'pl_atual', 'REAL', 0, None, 0)
(6, 'pl_max', 'REAL', 0, None, 0)
(7, 'pl_pct_of_max', 'REAL', 0, None, 0)
(8, 'dte_min', 'INTEGER', 0, None, 0)
(9, 'why_json', 'TEXT', 0, None, 0)
(10, 'spot_ref', 'REAL', 0, None, 0)
(11, 'meta_json', 'TEXT', 0, None, 0)
(12, 'created_at', 'TEXT', 0, 'CURRENT_TIMESTAMP', 0)
(13, 'why', 'TEXT', 0, None, 0)
(14, 'structure_id', 'INTEGER', 0, None, 0)
```

### Indices tabela `structure_decisions`

```text
(0, 'idx_decisions_ts', 0, 'c', 0)
(1, 'idx_decisions_aba_ts', 0, 'c', 0)
(2, 'ux_decision_snapshot', 1, 'c', 0)
```

Total de linhas em `structure_decisions`: 8

### Schema tabela `structure_leg_snapshots`

```text
(0, 'id', 'INTEGER', 0, None, 1)
(1, 'snapshot_id', 'INTEGER', 1, None, 0)
(2, 'structure_id', 'INTEGER', 1, None, 0)
(3, 'leg_id', 'INTEGER', 0, None, 0)
(4, 'leg_order', 'INTEGER', 0, None, 0)
(5, 'position_side', 'TEXT', 0, None, 0)
(6, 'option_type', 'TEXT', 0, None, 0)
(7, 'symbol', 'TEXT', 0, None, 0)
(8, 'strike', 'REAL', 0, None, 0)
(9, 'expiration_date', 'TEXT', 0, None, 0)
(10, 'quantity', 'INTEGER', 0, None, 0)
(11, 'premium', 'REAL', 0, None, 0)
(12, 'multiplier', 'REAL', 0, None, 0)
(13, 'metrics_json', 'TEXT', 0, None, 0)
(14, 'market_json', 'TEXT', 0, None, 0)
(15, 'raw_json', 'TEXT', 0, None, 0)
```

### Indices tabela `structure_leg_snapshots`

```text
(0, 'idx_structure_leg_snapshots_leg_id', 0, 'c', 0)
(1, 'idx_structure_leg_snapshots_structure_id', 0, 'c', 0)
(2, 'idx_structure_leg_snapshots_snapshot_id', 0, 'c', 0)
```

Total de linhas em `structure_leg_snapshots`: 0

### Schema tabela `structure_snapshots`

```text
(0, 'id', 'INTEGER', 0, None, 1)
(1, 'created_at', 'TEXT', 1, None, 0)
(2, 'structure_id', 'INTEGER', 1, None, 0)
(3, 'pricing_execution_id', 'INTEGER', 0, None, 0)
(4, 'underlying_asset', 'TEXT', 0, None, 0)
(5, 'reference_date', 'TEXT', 0, None, 0)
(6, 'snapshot_source', 'TEXT', 1, "'system'", 0)
(7, 'structure_json', 'TEXT', 1, None, 0)
(8, 'market_json', 'TEXT', 0, None, 0)
(9, 'metrics_json', 'TEXT', 0, None, 0)
(10, 'payoff_json', 'TEXT', 0, None, 0)
(11, 'decision_json', 'TEXT', 0, None, 0)
(12, 'alerts_json', 'TEXT', 0, None, 0)
(13, 'operation_state_json', 'TEXT', 0, None, 0)
```

### Indices tabela `structure_snapshots`

```text
(0, 'idx_structure_snapshots_pricing_execution_id', 0, 'c', 0)
(1, 'idx_structure_snapshots_reference_date', 0, 'c', 0)
(2, 'idx_structure_snapshots_structure_created', 0, 'c', 0)
(3, 'idx_structure_snapshots_created_at', 0, 'c', 0)
(4, 'idx_structure_snapshots_structure_id', 0, 'c', 0)
```

Total de linhas em `structure_snapshots`: 0

## 4. Arquivos candidatos por nome

- `.tmp/contexto_ui_payoff.txt`
- `ATT/checks/check_structures.py`
- `ATT/patches/pre_correct_rtd_derived_db_20260630_status.txt`
- `ATT/patches/pre_rtd_on_demand_restore_20260630_status.txt`
- `ATT/tests/test_canonical_pricing_facade.py`
- `ATT/tests/test_derived_service.py`
- `ATT/tests/test_legacy_structure_legs_importer.py`
- `ATT/tests/test_legacy_structure_legs_importer_integration.py`
- `ATT/tests/test_legacy_structure_legs_reader.py`
- `ATT/tests/test_market_snapshot_provider.py`
- `ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py`
- `ATT/tests/test_market_snapshot_selector.py`
- `ATT/tests/test_payoff_canonical.py`
- `ATT/tests/test_payoff_chart.py`
- `ATT/tests/test_pricing_engine_stub.py`
- `ATT/tests/test_pricing_execution_app_service.py`
- `ATT/tests/test_pricing_execution_controller.py`
- `ATT/tests/test_pricing_execution_orchestration_service.py`
- `ATT/tests/test_pricing_execution_persistence_service.py`
- `ATT/tests/test_pricing_execution_query_service.py`
- `ATT/tests/test_pricing_execution_service.py`
- `ATT/tests/test_pricing_executions_repository.py`
- `ATT/tests/test_pricing_input_service.py`
- `ATT/tests/test_pricing_payload_adapter.py`
- `ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py`
- `ATT/tests/test_structure_analysis_service.py`
- `ATT/tests/test_structure_editor_dialog.py`
- `ATT/tests/test_structure_editor_integration.py`
- `ATT/tests/test_structure_events_api.py`
- `ATT/tests/test_structure_events_effective_state.py`
- `ATT/tests/test_structure_events_repository.py`
- `ATT/tests/test_structure_events_service.py`
- `ATT/tests/test_structure_input_mapper.py`
- `ATT/tests/test_structure_leg_rtd_enrichment_service.py`
- `ATT/tests/test_structure_market_input_assembler.py`
- `ATT/tests/test_structure_metrics.py`
- `ATT/tests/test_structures_api.py`
- `ATT/tests/test_structures_archive_wiring.py`
- `ATT/tests/test_structures_legs_endpoints.py`
- `ATT/tests/test_structures_repository.py`
- `ATT/tests/test_system_snapshots_repository.py`
- `ATT/tests/test_system_snapshots_schema.py`
- `ATT/tests/test_terminal_vwap_payoff_app_service.py`
- `ATT/tests/test_terminal_vwap_payoff_controller.py`
- `ATT/tests/test_terminal_vwap_payoff_panel.py`
- `ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py`
- `UI/components/payoff_chart.py`
- `UI/components/structure_editor_dialog.py`
- `UI/components/structures_list_panel.py`
- `UI/components/terminal_vwap_payoff_dark_panel.py`
- `UI/components/terminal_vwap_payoff_panel.py`
- `UI/main_window.py`
- `_local_scripts_fase7/atualizar_docs_vwap_payoff_premissas.sh`
- `_local_scripts_fase7/commit_docs_vwap_payoff.sh`
- `_local_scripts_fase7/commit_incremento2_terminal_vwap_payoff_app_service.sh`
- `_local_scripts_fase7/conferir_base_terminal_vwap_payoff.sh`
- `_local_scripts_fase7/corrigir_on_structure_selected_fase7.py`
- `_local_scripts_fase7/corrigir_on_structure_selected_fase7.sh`
- `_local_scripts_fase7/criar_incremento2_terminal_vwap_payoff_app_service.sh`
- `_local_scripts_fase7/criar_incremento_viewmodel_terminal_vwap_payoff.sh`
- `_local_scripts_fase7/detectar_testes_terminal_vwap_payoff.sh`
- `_local_scripts_fase7/diagnostico_incremento3_terminal_vwap_payoff.sh`
- `_local_scripts_fase7/incremento3_controller_terminal_vwap_payoff.sh`
- `_local_scripts_fase7/mapear_alvos_implementacao_terminal_vwap_payoff.sh`
- `_local_scripts_fase7/mapear_fontes_incremento2_terminal_vwap_payoff.sh`
- `_local_scripts_fase7/registrar_incremento2_docs_terminal_vwap_payoff.sh`
- `_local_scripts_fase7/resumir_conferencias_terminal_vwap_payoff.sh`
- `_local_scripts_fase7/validar_commit_incremento_viewmodel_terminal_vwap_payoff.sh`
- `_local_scripts_fase7/validar_docs_terminal_vwap_payoff.sh`
- `api/pricing_execution_controller.py`
- `api/structures_controller.py`
- `backups/app_fase12_rtd_option_quotes_ok.sql`
- `controllers/terminal_vwap_payoff_controller.py`
- `create_payoff_summary_table.py`
- `dados/rtd_symbols.strict.tmp.txt`
- `dados/rtd_symbols.txt`
- `dados/rtd_symbols_probe.txt`
- `dados/rtd_underlying_symbols.txt`
- `db/derived_repo.py`
- `db/import_excel.py`
- `db/init_excel_schema.py`
- `db/migrations/add_structure_id_to_payoff_curve_points.py`
- `db/schema_excel.py`
- `docs/AUDITORIA_RTD_EXCEL_VIVO.md`
- `docs/PLANO_RTD_EXCEL_VIVO.md`
- `docs/auditoria_rtd_nova_ui_bovak900.md`
- `docs/auditoria_ui_terminal_vwap_payoff.md`
- `docs/checkpoints/evidencias/fase-1-mapa-payoff-codigo-atual.txt`
- `docs/checkpoints/evidencias/fase-1-mapa-payoff-runtime-codigo-atual.txt`
- `docs/checkpoints/evidencias/fase-1-mapa-rtd-codigo-atual.txt`
- `docs/checkpoints/evidencias/fase-1-mapa-rtd-runtime-codigo-atual.txt`
- `docs/checkpoints/evidencias/fase-1-trechos-payoff-decisoes-runtime.txt`
- `docs/checkpoints/evidencias/fase-1-trechos-rtd-runtime.txt`
- `docs/checkpoints/evidencias/fase-10-abertura-auditoria-pricing-position-side.md`
- `docs/checkpoints/evidencias/fase-6-11-analise-estatica-testes-rtd-historicos.txt`
- `docs/checkpoints/evidencias/fase-6-11-auditoria-testes-rtd-historicos-git.txt`
- `docs/checkpoints/evidencias/fase-6-11-datas-exclusao-testes-rtd-historicos.txt`
- `docs/checkpoints/evidencias/fase-6-11-decisao-final-testes-rtd-historicos.txt`
- `docs/checkpoints/evidencias/fase-6-11-estado-atual-rtd-db-scripts-testes.txt`
- `docs/checkpoints/evidencias/fase-6-11-evidencia-fechamento-rtd-option-quotes-pricing-runtime.txt`
- `docs/checkpoints/evidencias/fase-6-11-evidencia-guardrails-rtd-option-quotes-repository.txt`
- `docs/checkpoints/evidencias/fase-6-11-evidencia-integracao-rtd-option-quotes-pricing-runtime.txt`
- `docs/checkpoints/evidencias/fase-6-11-evidencia-pr-rtd-option-quotes-pricing-runtime.txt`
- `docs/checkpoints/evidencias/fase-6-11-evidencia-repository-rtd-option-quotes.txt`
- `docs/checkpoints/evidencias/fase-6-11-importabilidade-testes-rtd-historicos-sanitizados.txt`
- `docs/checkpoints/evidencias/fase-6-11-inventario-testes-rtd-option-canonical.txt`
- `docs/checkpoints/evidencias/fase-6-11-mapa-impacto-integracao-rtd-option-quotes-pricing-runtime.txt`
- `docs/checkpoints/evidencias/fase-6-11-mapa-runtime-leitura-rtd-pricing.txt`
- `docs/checkpoints/evidencias/fase-6-11-matriz-compatibilidade-testes-rtd-historicos.txt`
- `docs/checkpoints/evidencias/fase-6-11-pytest-canonical-pricing-facade-baseline.txt`
- `docs/checkpoints/evidencias/fase-6-11-pytest-collect-only-testes-rtd-historicos-sanitizados.txt`
- `docs/checkpoints/evidencias/fase-6-11-pytest-collect-only-testes-rtd-historicos.txt`
- `docs/checkpoints/evidencias/fase-6-11-pytest-pricing-execution-baseline.txt`
- `docs/checkpoints/evidencias/fase-6-11-pytest-rtd-canonical-pricing-input-baseline.txt`
- `docs/checkpoints/evidencias/fase-6-11-pytest-rtd-canonical-pricing-input-guardrail.txt`
- `docs/checkpoints/evidencias/fase-6-11-recorte-rtd-canonical-pricing-input.txt`
- `docs/checkpoints/evidencias/fase-6-11-regressao-disponivel-rtd-canonical-pricing.txt`
- `docs/checkpoints/evidencias/fase-6-11-simbolos-atuais-rtd-pricing.txt`
- `docs/checkpoints/evidencias/fase-6-11-sintaxe-testes-rtd-historicos.txt`
- `docs/checkpoints/evidencias/fase-6-11-testes-rtd-historicos-ausentes.txt`
- `docs/checkpoints/evidencias/fase-6-7-inventario-diagnostico-rtd-canonical.txt`
- `docs/checkpoints/evidencias/fase-6-7-pytest-baseline-canonical-rtd.txt`
- `docs/checkpoints/evidencias/fase-6-7-pytest-baseline-rtd-option-quotes.txt`
- `docs/checkpoints/evidencias/fase-6-7-recorte-funcional-rtd-canonical.txt`
- `docs/checkpoints/evidencias/fase-6-8-pytest-guardrail-matriz-diagnostico-rtd.txt`
- `docs/checkpoints/evidencias/fase-6-9-pytest-canonical-pricing-rtd-number-formats.txt`
- `docs/checkpoints/evidencias/fase-6-9-pytest-pricing-execution-services.txt`
- `docs/checkpoints/evidencias/fase-7-execucao-testes-rtd-vigentes.txt`
- `docs/checkpoints/evidencias/fase-7-fechamento-validacao-regressiva-rtd-vigente.txt`
- `docs/checkpoints/evidencias/fase-7-validacao-regressiva-rtd-vigente.txt`
- `docs/checkpoints/evidencias/fase-9-encerramento-enriquecimento-legs-rtd-e-position-side.md`
- `docs/checkpoints/evidencias/fase-9-implementacao-enriquecimento-legs-rtd.txt`
- `docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_canonical_pricing_facade_execute_pricing_rtd_integration_from_b492f16.py.txt`
- `docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_canonical_pricing_facade_rtd_db_path_from_bcb6ddb.py.txt`
- `docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_canonical_pricing_facade_rtd_price_resolution_from_0c7e123.py.txt`
- `docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_fase_11_rtd_integrated_flow_from_9009a40.py.txt`
- `docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_pricing_execution_price_source_persistence_from_d3a9dcc.py.txt`
- `docs/checkpoints/evidencias/rtd_historico_preview/test_canonical_pricing_facade_execute_pricing_rtd_integration.from-b492f16.py.txt`
- `docs/checkpoints/evidencias/rtd_historico_preview/test_canonical_pricing_facade_rtd_db_path.from-bcb6ddb.py.txt`
- `docs/checkpoints/evidencias/rtd_historico_preview/test_canonical_pricing_facade_rtd_price_resolution.from-0c7e123.py.txt`
- `docs/checkpoints/evidencias/rtd_historico_preview/test_fase_11_rtd_integrated_flow.from-9009a40.py.txt`
- `docs/checkpoints/evidencias/rtd_historico_preview/test_pricing_execution_price_source_persistence.from-d3a9dcc.py.txt`
- `docs/checkpoints/fase-6-7-consolidacao-diagnostico-rtd-canonical.md`
- `docs/checkpoints/fase-6-8-guardrail-matriz-diagnostico-rtd.md`
- `docs/checkpoints/fase-6-9-ajuste-rtd-canonical-pricing.md`
- `docs/decisions/structure_ref_created_at.md`
- `docs/evolucoes de fases/AUDITORIA_FASE_11_SNAPSHOTS_HISTORICO.md`
- `docs/evolucoes de fases/EVOLUCAO_PRICING_PAYOFF.md`
- `docs/evolucoes de fases/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md`
- `docs/evolucoes de fases/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md`
- `docs/ui_terminal_vwap_payoff_plano.md`
- `domain/market_snapshot.py`
- `domain/payoff.py`
- `domain/payoff_features.py`
- `domain/structure_metrics.py`
- `find_structure.sh`
- `infra/bootstrap_rtd_option_quotes_schema.py`
- `infra/bootstrap_structures_schema.py`
- `reports/payoff_conferencia/arquivos_candidatos_ui_payoff_20260627_123456.txt`
- `reports/payoff_conferencia/auditoria_completude_ui_payoff_20260627_123519.txt`
- `reports/payoff_conferencia/buscas_git_payoff_20260627_094738.txt`
- `reports/payoff_conferencia/buscas_git_payoff_20260627_101102.txt`
- `reports/payoff_conferencia/buscas_git_payoff_20260627_103217.txt`
- `reports/payoff_conferencia/buscas_git_payoff_20260627_103723.txt`
- `reports/payoff_conferencia/buscas_git_payoff_20260627_113317.txt`
- `reports/payoff_conferencia/buscas_git_payoff_20260627_113705.txt`
- `reports/payoff_conferencia/buscas_git_payoff_20260627_113954.txt`
- `reports/payoff_conferencia/buscas_git_payoff_20260627_122610.txt`
- `reports/payoff_conferencia/buscas_git_payoff_20260627_122956.txt`
- `reports/payoff_conferencia/classificacao_nomenclatura_preco_payoff_20260627.txt`
- `reports/payoff_conferencia/classificacao_nomenclatura_preco_payoff_20260627_121505.txt`
- `reports/payoff_conferencia/classificacao_nomenclatura_preco_payoff_20260627_121620.txt`
- `reports/payoff_conferencia/classificacao_nomenclatura_preco_payoff_20260627_122223.txt`
- `reports/payoff_conferencia/classificacao_nomenclatura_preco_payoff_20260627_122608.txt`
- `reports/payoff_conferencia/classificacao_nomenclatura_preco_payoff_20260627_122955.txt`
- `reports/payoff_conferencia/conferencia_db_payoff_20260627_094741.txt`
- `reports/payoff_conferencia/conferencia_db_payoff_20260627_101105.txt`
- `reports/payoff_conferencia/conferencia_db_payoff_20260627_103221.txt`
- `reports/payoff_conferencia/conferencia_db_payoff_20260627_103726.txt`
- `reports/payoff_conferencia/conferencia_db_payoff_20260627_113320.txt`
- `reports/payoff_conferencia/conferencia_db_payoff_20260627_113708.txt`
- `reports/payoff_conferencia/conferencia_db_payoff_20260627_113957.txt`
- `reports/payoff_conferencia/conferencia_db_payoff_20260627_122613.txt`
- `reports/payoff_conferencia/conferencia_db_payoff_20260627_122959.txt`
- `reports/payoff_conferencia/db_path_ui_snapshots_20260627_125228.txt`
- `reports/payoff_conferencia/fontes_snapshot_metricas_perna_20260627_124640.txt`
- `reports/payoff_conferencia/labels_ui_payoff_completude_20260627_124459.txt`
- `reports/payoff_conferencia/orfaos_structure_leg_snapshots_20260627_125813.txt`
- `reports/payoff_conferencia/payoff_ui_analitica.json`
- `reports/payoff_conferencia/schema_real_snapshots_20260627_125139.txt`
- `reports/payoff_conferencia/schema_snapshot_metricas_perna_20260627_124651.txt`
- `reports/payoff_conferencia/trechos_ui_payoff_completude_20260627_124348.txt`
- `reports/payoff_runtime_focado/runtime_focado_payoff_20260627_095522.txt`
- `reports/payoff_runtime_focado/runtime_focado_payoff_20260627_095938.txt`
- `reports/payoff_runtime_focado/runtime_focado_payoff_20260627_100419.txt`
- `reports/payoff_runtime_focado/runtime_focado_payoff_20260627_101106.txt`
- `reports/payoff_runtime_focado/runtime_focado_payoff_20260627_103222.txt`
- `reports/payoff_runtime_focado/runtime_focado_payoff_20260627_103728.txt`
- `reports/payoff_runtime_focado/runtime_focado_payoff_20260627_113322.txt`
- `reports/payoff_runtime_focado/runtime_focado_payoff_20260627_113709.txt`
- `reports/payoff_runtime_focado/runtime_focado_payoff_20260627_113958.txt`
- `reports/payoff_runtime_focado/runtime_focado_payoff_20260627_122614.txt`
- `reports/payoff_runtime_focado/runtime_focado_payoff_20260627_123000.txt`
- `reports/payoff_runtime_focado/scan_db_tokens_payoff_20260627_095625.txt`
- `reports/payoff_runtime_focado/scan_db_tokens_payoff_20260627_100421.txt`
- `reports/payoff_runtime_focado/scan_db_tokens_payoff_20260627_101108.txt`
- `reports/payoff_runtime_focado/scan_db_tokens_payoff_20260627_103224.txt`
- `reports/payoff_runtime_focado/scan_db_tokens_payoff_20260627_103730.txt`
- `reports/payoff_runtime_focado/scan_db_tokens_payoff_20260627_113324.txt`
- `reports/payoff_runtime_focado/scan_db_tokens_payoff_20260627_113712.txt`
- `reports/payoff_runtime_focado/scan_db_tokens_payoff_20260627_114001.txt`
- `reports/payoff_runtime_focado/scan_db_tokens_payoff_20260627_122617.txt`
- `reports/rtd_vwap_audit/csv_rtd_links_vwap_audit.json`
- `reports/rtd_vwap_audit/workbook_rtd_vwap_audit.json`
- `reports/ui_terminal_vwap_payoff/commit_incremento_viewmodel_terminal_vwap_payoff_20260629_092259.txt`
- `reports/ui_terminal_vwap_payoff/commit_incremento_viewmodel_terminal_vwap_payoff_20260629_092344.txt`
- `reports/ui_terminal_vwap_payoff/incremento_viewmodel_terminal_vwap_payoff_20260629_091736.txt`
- `reports/ui_terminal_vwap_payoff/mapa_fontes_incremento2_terminal_vwap_payoff_20260629_092829.txt`
- `repositories/market_snapshot_repository.py`
- `repositories/pricing_executions_repository.py`
- `repositories/rtd_option_quotes_repository.py`
- `repositories/structure_events_repository.py`
- `repositories/structures_repository.py`
- `repositories/system_snapshots_repository.py`
- `scripts/import_legacy_structure_legs.py`
- `scripts/import_rtd_option_quotes_wide_csv.py`
- `scripts/patch_derived_payoff_timestamp_consistency.sh`
- `scripts/purge_derived_snapshots.py`
- `scripts/refresh_rtd_option_quotes_excel.ps1`
- `scripts/refresh_rtd_symbol_to_option_quotes.py`
- `scripts/refresh_rtd_symbol_to_option_quotes_fallback.py`
- `scripts/repair_derived_db_consistency.py`
- `scripts/rtd_auditoria_fase0.sh`
- `scripts/rtd_consulta_projeto.sh`
- `scripts/rtd_mapa_alvos_fase0.py`
- `scripts/rtd_mapa_alvos_fase0.sh`
- `scripts/rtd_rodar_fase0.sh`
- `scripts/run_derived_pipeline.py`
- `scripts/validate_derived_db.py`
- `services/canonical_input_service.py`
- `services/canonical_pricing_facade.py`
- `services/derived_payoff_persistence.py`
- `services/derived_service.py`
- `services/legacy_structure_legs_importer.py`
- `services/legacy_structure_legs_reader.py`
- `services/market_snapshot_provider.py`
- `services/market_snapshot_selector.py`
- `services/payoff_persistence_port.py`
- `services/pricing_engine_stub.py`
- `services/pricing_execution_app_service.py`
- `services/pricing_execution_orchestration_service.py`
- `services/pricing_execution_persistence_service.py`
- `services/pricing_execution_query_service.py`
- `services/pricing_execution_service.py`
- `services/pricing_input_service.py`
- `services/pricing_payload_adapter.py`
- `services/structure_analysis_service.py`
- `services/structure_events_service.py`
- `services/structure_input_mapper.py`
- `services/structure_leg_rtd_enrichment_service.py`
- `services/structure_market_input_assembler.py`
- `services/terminal_vwap_payoff_app_service.py`
- `services/terminal_vwap_payoff_viewmodel_service.py`
- `src/domain/refs/structure_ref.py`
- `tools/audit_rtd_ui_flow.py`
- `tools/fix_structure_side_panel_patch.py`
- `tools/patch_structure_side_panel.py`

## 5. Trechos focados dos arquivos-chave

### `scripts/refresh_rtd_option_quotes_excel.ps1`

```text
1: param(
2:     [string]$WorkbookPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "LISTA_RTD.xlsm"),
3:     [string]$SymbolsPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "dados\rtd_symbols.txt"),
4:     [string]$CsvPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "dados\RTD_LINKS.csv"),
---
5:     [int]$WaitSeconds = 20,
---
6:     [switch]$Visible
---
31: 
32: if (!(Test-Path $SymbolsPath)) {
33:     throw "Arquivo de símbolos não encontrado: $SymbolsPath"
34: }
35: 
---
45: Write-Host "Símbolos carregados:" $symbols.Count
46: 
47: $excel = New-Object -ComObject Excel.Application
48: $excel.Visible = [bool]$Visible
49: $excel.DisplayAlerts = $false
---
50: $excel.EnableEvents = $false
---
51: 
---
52: # xlCalculationAutomatic = -4105
---
53: try {
54:     $excel.Calculation = -4105
55: } catch {
56:     Write-Host ("Aviso: não foi possível alterar o modo de cálculo do Excel. Continuando. Detalhe: " + $_.Exception.Message)
---
57: }
58: try {
---
59:     $wb = Invoke-WithRetry { $excel.Workbooks.Open($WorkbookPath) }
60: 
61:     $sheetName = "RTD_OPTION_QUOTES"
---
62: 
63:     $ws = $null
---
78:     $headers = @(
79:         "codigo_opcao",
80:         "ativo_base",
81:         "call_put",
82:         "strike",
---
84:         "ultimo_preco",
85:         "ultima_quantidade",
86:         "bid",
87:         "ask",
88:         "volume",
---
89:         "iv",
---
90:         "delta",
---
91:         "gamma",
---
92:         "theta",
---
93:         "vega",
---
94:         "vwap"
---
95:     )
---
96: 
---
104:         "QUOTE.STRIKE_PRICE",
105:         "QUOTE.MATURITYDATE",
106:         "QUOTE.LAST_TRADE_PRICE",
107:         "QUOTE.LAST_TRADE_QUANTITY",
108:         "QUOTE.BID_PRICE",
---
109:         "QUOTE.ASK_PRICE",
---
110:         "QUOTE.VOLUME",
---
111:         "QUOTE.IMPLIED_VOLATILITY",
---
112:         "QUOTE.DELTA",
---
113:         "QUOTE.GAMMA",
114:         "QUOTE.THETA",
---
115:         "QUOTE.VEGA",
---
116:         "QUOTE.VWAP"
---
117:     )
---
118: 
---
125:             $col = $i + 2
126:             $field = $fields[$i]
127:             $formula = '=RTD("btg_pro_rtd";"";"' + $field + '";$A' + $row + ')'
128:             $ws.Cells.Item($row, $col).FormulaLocal = $formula
129:         }
---
132:     }
133: 
134:     $lastRow = $symbols.Count + 1
135:     $lastCol = $headers.Count
136: 
---
137:     Invoke-WithRetry { $ws.Range($ws.Cells.Item(1,1), $ws.Cells.Item($lastRow,$lastCol)).Columns.AutoFit() | Out-Null }
---
138: 
139:     Write-Host "Aba RTD_OPTION_QUOTES preenchida. Linhas:" $symbols.Count
---
140:     Write-Host "Recalculando Excel/RTD..."
141: 
---
142:     Invoke-WithRetry { $excel.CalculateFullRebuild() | Out-Null }
---
143: 
144:     Start-Sleep -Seconds $WaitSeconds
---
150:     }
151: 
152:     # Copia somente a aba RTD_OPTION_QUOTES para novo workbook e salva como CSV UTF-8.
153:     Invoke-WithRetry { $ws.Copy() | Out-Null }
154:     $csvWb = $excel.ActiveWorkbook
---
155: 
156:     # 62 = xlCSVUTF8
---
164: }
165: finally {
166:     $excel.Quit() | Out-Null
167: }
---
```

### `scripts/refresh_rtd_symbol_to_option_quotes.py`

```text
1: #!/usr/bin/env python
2: """
3: Atualiza uma opção avulsa via RTD Excel e importa para rtd_option_quotes.
4: 
5: Fluxo:
---
6:     symbol -> arquivo temporário de símbolos -> refresh_rtd_option_quotes_excel.ps1
7:     -> CSV temporário -> import_rtd_option_quotes_wide_csv.py -> SQLite
8: 
---
9: Exemplo:
---
10:     python scripts/refresh_rtd_symbol_to_option_quotes.py --symbol PETRS424 --db dados/app.db --visible --json
11: """
12: 
---
16: import json
17: import sqlite3
18: import subprocess
19: import sys
20: from pathlib import Path
---
24: PROJECT_ROOT = Path(__file__).resolve().parents[1]
25: 
26: PS1_SCRIPT = PROJECT_ROOT / "scripts" / "refresh_rtd_option_quotes_excel.ps1"
27: IMPORT_SCRIPT = PROJECT_ROOT / "scripts" / "import_rtd_option_quotes_wide_csv.py"
28: 
---
29: 
---
30: def run_command(command: list[str], *, cwd: Path, timeout_seconds: int = 45) -> dict[str, Any]:
31:     try:
32:         completed = subprocess.run(
33:             command,
34:             cwd=str(cwd),
---
40:             check=False,
41:         )
42:     except subprocess.TimeoutExpired as exc:
43:         return {
44:             "command": command,
---
85:             """
86:             SELECT *
87:             FROM rtd_option_quotes
88:             WHERE UPPER(TRIM(codigo_opcao)) = UPPER(TRIM(?))
89:             ORDER BY updated_at DESC, id DESC
---
101: def build_parser() -> argparse.ArgumentParser:
102:     parser = argparse.ArgumentParser(
103:         description="Atualiza uma opção avulsa via RTD Excel e importa para rtd_option_quotes."
104:     )
105: 
---
118:     parser.add_argument(
119:         "--workbook",
120:         default="LISTA_RTD.xlsm",
121:         help="Caminho do workbook RTD. Padrão: LISTA_RTD.xlsm",
122:     )
---
123: 
---
126:         type=int,
127:         default=10,
128:         help="Timeout/espera do RTD. Padrão: 10.",
129:     )
130: 
---
132:         "--visible",
133:         action="store_true",
134:         help="Deixa o Excel visível durante o refresh.",
135:     )
136: 
---
139:         type=int,
140:         default=45,
141:         help="Timeout máximo do processo PowerShell/Excel. Padrão: 45.",
142:     )
143: 
---
145:         "--keep-files",
146:         action="store_true",
147:         help="Não remove os arquivos temporários de símbolo/CSV.",
148:     )
149: 
---
175:     tmp_dir.mkdir(parents=True, exist_ok=True)
176: 
177:     symbols_path = tmp_dir / f"rtd_symbols_probe_{symbol}.txt"
178:     csv_path = tmp_dir / f"RTD_LINKS_probe_{symbol}.csv"
179: 
---
180:     result: dict[str, Any] = {
---
188:         "visible": bool(args.visible),
189:         "steps": {
190:             "refresh_excel": None,
191:             "import_csv": None,
192:         },
---
238:             timeout_seconds=int(args.timeout_seconds),
239:         )
240:         result["steps"]["refresh_excel"] = refresh_result
241: 
242:         if not refresh_result["ok"]:
---
243:             result["status"] = "error"
244:             result["errors"].append("refresh_excel step failed")
245:             raise RuntimeError("refresh_excel step failed")
246: 
---
247:         import_command = [
---
285:             print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
286:         else:
287:             print("Refresh RTD symbol -> rtd_option_quotes")
288:             print(f"Status: {result['status']}")
289:             print(f"Symbol: {symbol}")
---
310:         print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
311:     else:
312:         print("Refresh RTD symbol -> rtd_option_quotes")
313:         print("Status: ok")
314:         print(f"Symbol: {symbol}")
---
317: 
318:         if quote:
319:             print(f"Ativo base: {quote.get('ativo_base')}")
320:             print(f"Tipo: {quote.get('call_put')}")
321:             print(f"Strike: {quote.get('strike')}")
---
```

### `scripts/refresh_rtd_symbol_to_option_quotes_fallback.py`

```text
2: 
3: import json
4: import subprocess
5: import sys
6: from pathlib import Path
---
8: 
9: ROOT = Path(__file__).resolve().parents[1]
10: BASE_SCRIPT = Path(__file__).resolve().with_name("refresh_rtd_symbol_to_option_quotes.py")
11: 
12: 
---
58:     ]
59: 
60:     cp = subprocess.run(
61:         cmd,
62:         cwd=str(ROOT),
---
108:         data = attempt["json"] or {
109:             "status": "error",
110:             "errors": ["Falha ao executar tentativa visível."],
111:             "stdout": attempt["stdout"],
112:             "stderr": attempt["stderr"],
---
123:         return 0 if attempt["ok"] else 1
124: 
125:     # 1) Primeira tentativa: invisível/silenciosa.
126:     first = run_attempt(original_args, visible=False)
127: 
---
136:         return 0
137: 
138:     # 2) Segunda tentativa: visível.
139:     second = run_attempt(original_args, visible=True)
140: 
---
141:     data = second["json"] or {
142:         "status": "error",
143:         "errors": ["Tentativa invisível falhou e tentativa visível também não retornou JSON válido."],
144:         "visible_attempt_stdout": second["stdout"],
145:         "visible_attempt_stderr": second["stderr"],
---
```

### `scripts/import_rtd_option_quotes_wide_csv.py`

```text
4: import sqlite3
5: import sys
6: from datetime import datetime, timedelta
7: from pathlib import Path
8: 
---
12:     sys.path.insert(0, str(PROJECT_ROOT))
13: 
14: from infra.bootstrap_rtd_option_quotes_schema import ensure_rtd_option_quotes_schema
15: 
16: 
---
19:     "ultimo_preco",
20:     "ultima_quantidade",
21:     "bid",
22:     "ask",
23:     "volume",
---
24:     "vwap",
---
25:     "iv",
---
26:     "delta",
---
27:     "gamma",
---
28:     "theta",
---
29:     "vega",
---
30: }
---
31: 
---
33: EXPECTED_COLUMNS = [
34:     "codigo_opcao",
35:     "ativo_base",
36:     "call_put",
37:     "strike",
---
39:     "ultimo_preco",
40:     "ultima_quantidade",
41:     "bid",
42:     "ask",
43:     "volume",
---
44:     "vwap",
---
45:     "iv",
---
46:     "delta",
---
47:     "gamma",
---
48:     "theta",
---
49:     "vega",
---
50: ]
---
51: 
---
72:         "#NAME?",
73:         "#NOME?",
74:         "#DIV/0!",
75:         "N/A",
76:         "NA",
---
95: 
96: 
97: def parse_excel_date(value):
98:     if value is None:
99:         return None
---
116:         return None
117: 
118:     # Excel usa 1899-12-30 como base para compatibilidade histórica.
119:     days = int(serial)
120:     dt = datetime(1899, 12, 30) + timedelta(days=days)
---
121:     return dt.strftime("%Y-%m-%d")
122: 
---
152:         return csv.Sniffer().sniff(sample, delimiters=";,")
153:     except csv.Error:
154:         class Dialect(csv.excel):
155:             delimiter = ";"
156: 
---
183:             record = {
184:                 "codigo_opcao": codigo.upper(),
185:                 "ativo_base": clean_text(raw.get("ativo_base")),
186:                 "call_put": normalize_call_put(raw.get("call_put")),
187:                 "strike": parse_number(raw.get("strike")),
---
188:                 "vencimento": parse_excel_date(raw.get("vencimento")),
189:                 "ultimo_preco": parse_number(raw.get("ultimo_preco")),
190:                 "ultima_quantidade": parse_number(raw.get("ultima_quantidade")),
---
191:                 "bid": parse_number(raw.get("bid")),
192:                 "ask": parse_number(raw.get("ask")),
193:                 "volume": parse_number(raw.get("volume")),
---
194:                 "vwap": parse_number(raw.get("vwap")),
---
195:                 "iv": parse_number(raw.get("iv")),
---
196:                 "delta": parse_number(raw.get("delta")),
---
197:                 "gamma": parse_number(raw.get("gamma")),
---
198:                 "theta": parse_number(raw.get("theta")),
---
199:                 "vega": parse_number(raw.get("vega")),
---
200:                 "source": "BTG_RTD_EXCEL",
---
201:                 "raw_json": json.dumps(raw, ensure_ascii=False),
---
202:             }
---
209: def ensure_index(con):
210:     con.execute("""
211:         CREATE INDEX IF NOT EXISTS idx_rtd_option_quotes_codigo_opcao
212:         ON rtd_option_quotes(codigo_opcao)
213:     """)
---
214: 
---
228:         return stats
229: 
230:     ensure_rtd_option_quotes_schema(db_path)
231: 
232:     quote_columns = [
---
233:         "codigo_opcao",
234:         "ativo_base",
235:         "call_put",
236:         "strike",
---
238:         "ultimo_preco",
239:         "ultima_quantidade",
240:         "bid",
241:         "ask",
242:         "volume",
---
243:         "vwap",
---
244:         "iv",
---
245:         "delta",
---
246:         "gamma",
---
247:         "theta",
---
248:         "vega",
---
249:         "source",
---
250:         "raw_json",
---
269: 
270:             existing = con.execute(
271:                 "SELECT id FROM rtd_option_quotes WHERE codigo_opcao = ? ORDER BY id DESC LIMIT 1",
272:                 (codigo,),
273:             ).fetchone()
---
291: 
292:                 con.execute(
293:                     f"UPDATE rtd_option_quotes SET {set_clause} WHERE id = ?",
294:                     params,
295:                 )
---
305: 
306:                 con.execute(
307:                     f"INSERT INTO rtd_option_quotes ({columns_sql}) VALUES ({placeholders})",
308:                     params,
309:                 )
---
331:         print(json.dumps(stats, ensure_ascii=False, indent=2))
332:     else:
333:         print("Importação RTD wide CSV")
334:         print("-----------------------")
335:         for k, v in stats.items():
---
```

### `scripts/run_derived_pipeline.py`

```text
21: def validate_final_consistency() -> bool:
22:     """Valida consistência dos snapshots após processamento."""
23:     from db.config import connect_derived
24:     from db.derived_repo import validate_snapshot_consistency
25:     
---
26:     conn = connect_derived()
---
27:     try:
28:         return validate_snapshot_consistency(conn)
---
42: 
43: def main(argv=None) -> int:
44:     parser = argparse.ArgumentParser(description="Run derived pipeline")
45:     parser.add_argument(
46:         "--no-cleanup",
---
47:         action="store_true",
48:         help="Não executar cleanup do derived.db antes de validar",
49:     )
50:     args = parser.parse_args(argv)
---
51: 
52:     # Imports internos (mantidos aqui para respeitar sys.path/bootstrap)
53:     from services.derived_service import cleanup_derived
54: 
55:     if not args.no_cleanup:
---
56:         cleanup_derived(days_to_keep=30)
57: 
58:     # (Opcional) build summaries
---
```

### `repositories/rtd_option_quotes_repository.py`

```text
1: # repositories/rtd_option_quotes_repository.py
2: 
3: from __future__ import annotations
---
8: 
9: 
10: class RtdOptionQuotesRepository:
11:     """
12:     Leitura da tabela rtd_option_quotes.
---
13: 
14:     Essa tabela e alimentada pelo CSV exportado da aba RTD_LINKS
---
15:     e funciona como cache centralizado das cotacoes RTD de opcoes.
16: 
---
17:     Arquitetura:
---
18:     - dados/app.db: dados persistentes da aplicacao/estruturas
19:     - dados/derived.db: cache RTD e dados derivados
20:     """
21: 
---
22:     def __init__(self, db_path: str | Path = "dados/derived.db") -> None:
23:         self.db_path = Path(db_path)
24: 
---
32:             SELECT
33:                 codigo_opcao,
34:                 ativo_base,
35:                 call_put,
36:                 strike,
---
38:                 ultimo_preco,
39:                 ultima_quantidade,
40:                 bid,
41:                 ask,
42:                 volume,
---
43:                 vwap,
---
44:                 iv,
---
45:                 delta,
---
46:                 gamma,
---
47:                 theta,
---
48:                 vega,
---
49:                 source,
---
50:                 raw_json,
---
51:                 updated_at,
52:                 created_at
53:             FROM rtd_option_quotes
54:             WHERE UPPER(TRIM(codigo_opcao)) = UPPER(TRIM(?))
55:             ORDER BY updated_at DESC, id DESC
---
62:         return dict(row) if row else None
63: 
64:     def list_by_ativo_base(self, ativo_base: str) -> list[dict[str, Any]]:
65:         sql = """
66:             SELECT
---
67:                 codigo_opcao,
68:                 ativo_base,
69:                 call_put,
70:                 strike,
---
72:                 ultimo_preco,
73:                 ultima_quantidade,
74:                 bid,
75:                 ask,
76:                 volume,
---
77:                 vwap,
---
78:                 iv,
---
79:                 delta,
---
80:                 gamma,
---
81:                 theta,
---
82:                 vega,
---
83:                 source,
---
84:                 raw_json,
---
85:                 updated_at,
86:                 created_at
87:             FROM rtd_option_quotes
88:             WHERE UPPER(TRIM(ativo_base)) = UPPER(TRIM(?))
89:             ORDER BY vencimento, call_put, strike, codigo_opcao
---
90:         """
---
91: 
92:         with self._connect() as conn:
93:             rows = conn.execute(sql, (ativo_base,)).fetchall()
94: 
95:         return [dict(row) for row in rows]
---
99:             SELECT
100:                 codigo_opcao,
101:                 ativo_base,
102:                 call_put,
103:                 strike,
---
105:                 ultimo_preco,
106:                 ultima_quantidade,
107:                 bid,
108:                 ask,
109:                 volume,
---
110:                 vwap,
---
111:                 iv,
---
112:                 delta,
---
113:                 gamma,
---
114:                 theta,
---
115:                 vega,
---
116:                 source,
---
117:                 raw_json,
---
118:                 updated_at,
119:                 created_at
120:             FROM rtd_option_quotes
121:             ORDER BY ativo_base, vencimento, call_put, strike, codigo_opcao
122:         """
---
123: 
---
```

### `repositories/market_snapshot_repository.py`

```text
3: Repositorio canonico de snapshots de mercado.
4: 
5: Le legs RTD (rtd_analise_robo_legs), cotações RTD de opções
6: (rtd_option_quotes) e manuais (manual_analise_robo_legs), normaliza os campos
7: e retorna objetos LegMarketSnapshot prontos para uso.
---
8: """
---
26: _DEFAULT_DB = _PROJECT_ROOT / "dados" / "app.db"
27: 
28: RTD_OPTION_QUOTES_SOURCE = "rtd_option_quotes"
29: 
30: # --- SQL ---------------------------------------------------------------------
---
31: 
32: _SQL_RTD_LEGS = """
33:     SELECT
34:         timestamp,
---
35:         aba,
36:         ativo,
37:         cv,
38:         call_put,
---
39:         quant,
40:         valor_executado,
41:         bid,
42:         ask,
43:         spread,
---
44:         spread_pct,
---
45:         iv,
46:         delta,
47:         gamma,
---
48:         theta,
---
49:         vega,
---
50:         strike,
---
51:         vencimento,
---
52:         dte,
53:         pl_realista
54:     FROM rtd_analise_robo_legs
55:     WHERE aba = ?
56:     ORDER BY timestamp DESC
---
61:         timestamp,
62:         aba,
63:         ativo,
64:         cv,
65:         call_put,
---
66:         quant,
67:         valor_executado,
68:         bid,
69:         ask,
70:         spread,
---
71:         spread_pct,
---
72:         iv,
73:         delta,
74:         gamma,
---
75:         theta,
---
76:         vega,
---
77:         strike,
---
78:         vencimento,
---
86: """
87: 
88: _SQL_RTD_SUMMARY = """
89:     SELECT
90:         aba,
---
93:         dte_min,
94:         pl_realista_total,
95:         delta_liq,
96:         gamma_liq,
97:         theta_liq,
---
98:         vega_liq,
---
99:         spread_medio,
---
100:         spread_pct_medio,
---
101:         alertas_v2
102:     FROM rtd_analise_robo
103:     WHERE aba = ?
104:     ORDER BY rowid DESC
---
147: 
148: 
149: def _mid_price(bid: Optional[float], ask: Optional[float]) -> Optional[float]:
150:     # Calcula mid price. Nao usa coluna 'last' - nao existe no schema.
151:     if bid is not None and ask is not None:
---
152:         return round((bid + ask) / 2.0, 6)
---
153:     if bid is not None:
---
154:         return bid
---
155:     if ask is not None:
---
156:         return ask
---
157:     return None
---
158: 
---
159: 
160: def _row_to_leg(row: sqlite3.Row, source: SnapshotSource) -> LegMarketSnapshot:
161:     bid = _parse_br_float(row["bid"])
162:     ask = _parse_br_float(row["ask"])
163:     mid = _mid_price(bid, ask)
---
164: 
---
165:     return LegMarketSnapshot(
---
166:         aba=row["aba"],
167:         ativo=row["ativo"],
168:         cv=row["cv"],
169:         call_put=row["call_put"],
---
170:         quant=_parse_br_float(row["quant"]),
171:         valor_executado=_parse_br_float(row["valor_executado"]),
172:         bid=bid,
173:         ask=ask,
174:         mid=mid,
---
175:         spread=_parse_br_float(row["spread"]),
---
176:         spread_pct=_parse_br_float(row["spread_pct"]),
177:         iv=_parse_br_float(row["iv"]),
178:         delta=_parse_br_float(row["delta"]),
179:         gamma=_parse_br_float(row["gamma"]),
---
180:         theta=_parse_br_float(row["theta"]),
---
181:         vega=_parse_br_float(row["vega"]),
---
182:         strike=_parse_br_float(row["strike"]),
---
183:         vencimento=row["vencimento"],
---
189: 
190: 
191: def _row_to_rtd_option_quote_leg(
192:     base_leg: LegMarketSnapshot,
193:     quote_row: sqlite3.Row,
---
194: ) -> LegMarketSnapshot:
195:     """
196:     Converte uma cotação de rtd_option_quotes em LegMarketSnapshot mantendo
197:     os campos posicionais da leg RTD original.
198: 
---
199:     A tabela rtd_option_quotes é cache de cotação. Ela não define composição
---
200:     da estrutura. Por isso, quant/cv/dte/pl continuam vindo da leg estrutural
201:     em rtd_analise_robo_legs.
---
202:     """
203:     bid = _first_float(quote_row["bid"], base_leg.bid)
---
204:     ask = _first_float(quote_row["ask"], base_leg.ask)
205:     mid = _mid_price(bid, ask)
---
206:     ultimo_preco = _parse_br_float(quote_row["ultimo_preco"])
---
207: 
---
212:     )
213: 
214:     ativo = _first_text(quote_row["codigo_opcao"], base_leg.ativo)
215: 
216:     return LegMarketSnapshot(
---
217:         aba=base_leg.aba,
218:         ativo=ativo,
219:         cv=base_leg.cv,
220:         call_put=_first_text(quote_row["call_put"], base_leg.call_put),
---
221:         quant=base_leg.quant,
222:         valor_executado=valor_executado,
223:         bid=bid,
224:         ask=ask,
225:         mid=mid,
---
226:         spread=base_leg.spread,
---
227:         spread_pct=base_leg.spread_pct,
228:         iv=_first_float(quote_row["iv"], base_leg.iv),
229:         delta=_first_float(quote_row["delta"], base_leg.delta),
230:         gamma=_first_float(quote_row["gamma"], base_leg.gamma),
---
231:         theta=_first_float(quote_row["theta"], base_leg.theta),
---
LIMITE_DE_TRECHOS_ATINGIDO
```

### `services/market_snapshot_provider.py`

```text
60:             raise ValueError(f"market snapshot not found for asset: {asset}")
61: 
62:         effective_reference_date = reference_date or self.today_provider().isoformat()
63: 
64:         return {
---
65:             "reference_date": effective_reference_date,
66:             "underlying_asset": asset,
67:             "spot_price": float(market["spot_price"]),
---
```

### `services/market_snapshot_selector.py`

```text
1: # services/market_snapshot_selector.py
2: """
3: Política de precedência de snapshots: manual > rtd_option_quotes > rtd.
4: 
5: Para cada aba:
---
6:   - Se existir snapshot manual para o ativo, usa manual
7:   - Caso contrário, se existir cotação em rtd_option_quotes para a leg RTD, usa rtd_option_quotes
8:   - Caso contrário, usa rtd_analise_robo_legs
---
9: """
---
10: from __future__ import annotations
---
17: 
18: 
19: RTD_OPTION_QUOTES_SOURCE = "rtd_option_quotes"
20: 
21: 
---
45: class MarketSnapshotSelector:
46:     """
47:     Aplica a política manual > rtd_option_quotes > rtd para selecionar o snapshot canônico.
48:     """
49: 
---
69:             raise ValueError("Informe ref ou aba para selecionar snapshot.")
70: 
71:         effective_ref: StructureRef | str = ref if ref is not None else aba
72:         aba_str = _ref_to_aba(effective_ref)
73: 
---
74:         manual_legs = self._repo.get_manual_legs(effective_ref)
---
75:         rtd_legs = self._repo.get_rtd_legs(effective_ref)
76: 
---
77:         get_rtd_option_quote_legs = getattr(
---
78:             self._repo,
79:             "get_rtd_option_quote_legs",
---
80:             None,
81:         )
---
82:         if callable(get_rtd_option_quote_legs):
83:             rtd_option_quote_legs = get_rtd_option_quote_legs(effective_ref)
84:         else:
---
85:             rtd_option_quote_legs = []
---
86: 
87:         # Como as consultas vêm em timestamp DESC, preserva a primeira ocorrência
---
88:         # por ativo, que tende a ser a mais recente.
89: 
90:         manual_by_ativo: dict[str, LegMarketSnapshot] = {}
---
91:         for leg in manual_legs:
92:             if leg.ativo and leg.ativo not in manual_by_ativo:
---
93:                 manual_by_ativo[leg.ativo] = leg
94: 
---
95:         rtd_option_quote_by_ativo: dict[str, LegMarketSnapshot] = {}
---
96:         for leg in rtd_option_quote_legs:
97:             if leg.ativo and leg.ativo not in rtd_option_quote_by_ativo:
---
98:                 rtd_option_quote_by_ativo[leg.ativo] = leg
---
