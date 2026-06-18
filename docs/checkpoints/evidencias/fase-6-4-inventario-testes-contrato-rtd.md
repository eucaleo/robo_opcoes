# Fase 6.4 — Inventário de testes de contrato RTD

## Testes por função
ATT/tests/test_audit_rtd_option_quotes.py:92:def test_audit_reports_error_when_database_does_not_exist(tmp_path: Path):
ATT/tests/test_audit_rtd_option_quotes.py:101:def test_audit_reports_error_when_table_does_not_exist(tmp_path: Path):
ATT/tests/test_audit_rtd_option_quotes.py:114:def test_audit_reports_ok_for_valid_table_with_rows(tmp_path: Path):
ATT/tests/test_audit_rtd_option_quotes.py:131:def test_audit_reports_warning_for_empty_table(tmp_path: Path):
ATT/tests/test_audit_rtd_option_quotes.py:144:def test_audit_reports_error_for_missing_required_columns(tmp_path: Path):
ATT/tests/test_audit_rtd_option_quotes.py:164:def test_audit_reports_error_for_duplicated_codigo_opcao(tmp_path: Path):
ATT/tests/test_audit_rtd_option_quotes.py:179:def test_audit_reports_warning_for_stale_rows(tmp_path: Path):
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:317:def test_execute_pricing_uses_persisted_rtd_option_quote_price(tmp_path):
ATT/tests/test_canonical_pricing_facade_rtd_db_path.py:32:def test_sqlite_table_exists_returns_false_for_missing_database(tmp_path):
ATT/tests/test_canonical_pricing_facade_rtd_db_path.py:38:def test_sqlite_table_exists_detects_existing_table(tmp_path):
ATT/tests/test_canonical_pricing_facade_rtd_db_path.py:46:def test_resolve_rtd_option_quotes_db_path_prefers_app_db_when_primary_has_no_table(
ATT/tests/test_canonical_pricing_facade_rtd_db_path.py:64:def test_resolve_rtd_option_quotes_db_path_prefers_primary_when_primary_has_table(
ATT/tests/test_canonical_pricing_facade_rtd_db_path.py:82:def test_resolve_rtd_option_quotes_db_path_falls_back_to_primary_when_no_candidate_has_table(
ATT/tests/test_canonical_pricing_facade_rtd_db_path.py:100:def test_canonical_pricing_facade_initializes_rtd_repository_with_resolved_app_db(
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:26:def test_pick_rtd_option_price_prefers_ultimo_preco():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:38:def test_pick_rtd_option_price_falls_back_to_price_and_last_price():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:43:def test_pick_rtd_option_price_falls_back_to_bid_ask_mid():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:55:def test_pick_rtd_option_price_falls_back_to_bid_or_ask():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:60:def test_pick_rtd_option_price_returns_none_when_no_positive_price_exists():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:65:def test_lookup_rtd_option_quote_tries_original_and_uppercase_codigo():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:81:def test_lookup_rtd_option_quote_returns_none_when_repository_raises():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:89:def test_resolve_effective_leg_price_preserves_explicit_manual_price():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:116:def test_resolve_effective_leg_price_uses_rtd_when_source_is_not_manual():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:139:def test_resolve_effective_leg_price_falls_back_to_original_snapshot_price_when_no_rtd_quote():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:158:def test_resolve_effective_leg_price_falls_back_to_original_snapshot_price_on_repository_error():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:173:def test_snapshot_result_to_payload_uses_rtd_price_for_canonical_leg_fields(tmp_path):
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:220:def test_resolve_effective_leg_price_exposes_rtd_quote_traceability_metadata():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:258:def test_resolve_effective_leg_price_falls_back_to_snapshot_when_rtd_quote_has_no_usable_price():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:297:def test_snapshot_result_to_payload_does_not_leak_rtd_traceability_for_manual_price(tmp_path):
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:353:def test_resolve_effective_leg_price_diagnoses_missing_rtd_quote():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:373:def test_resolve_effective_leg_price_diagnoses_invalid_rtd_price():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:407:def test_resolve_effective_leg_price_diagnoses_rtd_asset_mismatch():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:437:def test_snapshot_result_to_payload_preserves_rtd_guardrails_for_valid_quote(tmp_path):
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:489:def test_snapshot_result_to_payload_preserves_rtd_guardrails_when_falling_back_to_snapshot(tmp_path):
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:529:def test_resolve_effective_leg_price_falls_back_to_snapshot_when_rtd_quote_is_stale():
ATT/tests/test_pricing_execution_price_source_persistence.py:37:def test_pricing_executions_repository_preserves_leg_price_source_on_get(tmp_path):
ATT/tests/test_pricing_execution_price_source_persistence.py:104:def test_pricing_executions_repository_preserves_leg_price_source_on_list(tmp_path):
ATT/tests/test_pricing_execution_price_source_persistence.py:196:def test_persistence_service_passes_price_source_to_system_snapshot_legs():
ATT/tests/test_pricing_execution_price_source_persistence.py:268:def test_fase_10e_pricing_executions_repository_preserves_full_rtd_traceability_on_get_and_list(tmp_path):
ATT/tests/test_pricing_execution_price_source_persistence.py:340:def test_fase_10e_persistence_service_passes_full_rtd_traceability_to_system_snapshot():
ATT/tests/test_run_rtd_option_quotes_pipeline.py:26:def test_build_import_command_uses_csv_db_and_script_path():
ATT/tests/test_run_rtd_option_quotes_pipeline.py:43:def test_build_import_command_includes_dry_run_when_requested():
ATT/tests/test_run_rtd_option_quotes_pipeline.py:55:def test_build_audit_command_uses_db_and_max_age():
ATT/tests/test_run_rtd_option_quotes_pipeline.py:73:def test_build_audit_command_includes_json_and_fail_on_warn():
ATT/tests/test_run_rtd_option_quotes_pipeline.py:87:def test_run_pipeline_stops_when_import_fails(monkeypatch):
ATT/tests/test_run_rtd_option_quotes_pipeline.py:107:def test_run_pipeline_runs_import_and_audit_when_import_succeeds(monkeypatch):
ATT/tests/test_run_rtd_option_quotes_pipeline.py:128:def test_run_pipeline_dry_run_skips_audit(monkeypatch):
ATT/tests/test_run_rtd_option_quotes_pipeline.py:150:def test_run_pipeline_returns_audit_code_when_audit_fails(monkeypatch):
ATT/tests/test_run_rtd_option_quotes_pipeline.py:171:def test_main_parses_arguments_and_runs_pipeline(monkeypatch):

## Referências a origem/preço RTD nos testes
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:86:            CREATE TABLE rtd_analise_robo_legs (
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:94:                bid TEXT,
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:95:                ask TEXT,
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:113:            INSERT INTO rtd_analise_robo_legs (
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:121:                bid,
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:122:                ask,
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:162:            CREATE TABLE manual_analise_robo_legs (
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:170:                bid TEXT,
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:171:                ask TEXT,
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:191:            CREATE TABLE rtd_analise_robo (
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:210:            INSERT INTO rtd_analise_robo (
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:243:            CREATE TABLE rtd_option_quotes (
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:249:                ultimo_preco REAL,
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:251:                bid REAL,
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:252:                ask REAL,
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:269:            INSERT INTO rtd_option_quotes (
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:275:                ultimo_preco,
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:277:                bid,
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:278:                ask,
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:307:                "rtd_option_quotes",
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:317:def test_execute_pricing_uses_persisted_rtd_option_quote_price(tmp_path):
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:347:    # O preço original do snapshot era 5.55.
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:348:    # O preço efetivo deve vir de rtd_option_quotes.ultimo_preco = 9.99.
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:353:    assert leg["price_source"] == "rtd_option_quotes"
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:354:    assert leg["rtd_price_field"] == "ultimo_preco"
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:355:    assert leg["rtd_quote_codigo_opcao"] == "ABCD11"
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:356:    assert leg["rtd_quote_ativo_base"] == "ABCD"
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:357:    assert leg["rtd_price_source"] == "rtd_option_quotes"
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:358:    assert leg["rtd_price_updated_at"] == "2026-06-15T10:01:00"
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:359:    assert leg["rtd_price_created_at"] == "2026-06-15T10:01:00"
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:366:    assert persisted_payload["legs"][0]["price_source"] == "rtd_option_quotes"
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:367:    assert persisted_payload["legs"][0]["rtd_price_field"] == "ultimo_preco"
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:368:    assert persisted_payload["legs"][0]["rtd_quote_codigo_opcao"] == "ABCD11"
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:369:    assert persisted_payload["legs"][0]["rtd_quote_ativo_base"] == "ABCD"
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:370:    assert persisted_payload["legs"][0]["rtd_price_source"] == "rtd_option_quotes"
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:371:    assert persisted_payload["legs"][0]["rtd_price_updated_at"] == "2026-06-15T10:01:00"
ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py:372:    assert persisted_payload["legs"][0]["rtd_price_created_at"] == "2026-06-15T10:01:00"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:4:    _lookup_rtd_option_quote,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:5:    _pick_rtd_option_price,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:7:    _snapshot_result_to_payload,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:26:def test_pick_rtd_option_price_prefers_ultimo_preco():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:28:        "ultimo_preco": 10.5,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:31:        "bid": 9.0,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:32:        "ask": 10.0,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:35:    assert _pick_rtd_option_price(quote) == 10.5
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:38:def test_pick_rtd_option_price_falls_back_to_price_and_last_price():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:39:    assert _pick_rtd_option_price({"ultimo_preco": 0, "price": 11.5}) == 11.5
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:40:    assert _pick_rtd_option_price({"ultimo_preco": None, "price": 0, "last_price": "12,50"}) == 12.5
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:43:def test_pick_rtd_option_price_falls_back_to_bid_ask_mid():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:45:        "ultimo_preco": None,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:48:        "bid": 2.0,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:49:        "ask": 4.0,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:52:    assert _pick_rtd_option_price(quote) == 3.0
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:55:def test_pick_rtd_option_price_falls_back_to_bid_or_ask():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:56:    assert _pick_rtd_option_price({"bid": 2.0, "ask": 0}) == 2.0
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:57:    assert _pick_rtd_option_price({"bid": 0, "ask": 4.0}) == 4.0
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:60:def test_pick_rtd_option_price_returns_none_when_no_positive_price_exists():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:61:    assert _pick_rtd_option_price({}) is None
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:62:    assert _pick_rtd_option_price({"ultimo_preco": 0, "price": 0, "bid": 0, "ask": 0}) is None
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:65:def test_lookup_rtd_option_quote_tries_original_and_uppercase_codigo():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:70:                "ultimo_preco": 1.23,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:75:    quote = _lookup_rtd_option_quote(repository, "abcd11")
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:81:def test_lookup_rtd_option_quote_returns_none_when_repository_raises():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:84:    quote = _lookup_rtd_option_quote(repository, "ABCD11")
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:89:def test_resolve_effective_leg_price_preserves_explicit_manual_price():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:94:                "ultimo_preco": 9.99,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:99:    price, price_source, traceability = _resolve_effective_leg_price(
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:102:        leg_source="manual",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:103:        rtd_option_quotes_repository=repository,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:108:    assert price_source == "manual"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:110:    assert traceability["rtd_quote_found"] is None
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:111:    assert traceability["rtd_validation_status"] == "not_applicable"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:112:    assert "manual explícito" in traceability["rtd_validation_message"]
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:116:def test_resolve_effective_leg_price_uses_rtd_when_source_is_not_manual():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:121:                "ultimo_preco": 9.99,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:126:    price, price_source, traceability = _resolve_effective_leg_price(
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:129:        leg_source="rtd",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:130:        rtd_option_quotes_repository=repository,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:135:    assert price_source == "rtd_option_quotes"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:139:def test_resolve_effective_leg_price_falls_back_to_original_snapshot_price_when_no_rtd_quote():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:142:    price, price_source, traceability = _resolve_effective_leg_price(
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:145:        leg_source="rtd",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:146:        rtd_option_quotes_repository=repository,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:151:    assert price_source == "snapshot"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:152:    assert traceability["price_resolution_status"] == "missing_rtd_quote"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:153:    assert traceability["rtd_quote_found"] is False
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:154:    assert traceability["rtd_validation_status"] == "error"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:155:    assert "não encontrada" in traceability["rtd_validation_message"]
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:158:def test_resolve_effective_leg_price_falls_back_to_original_snapshot_price_on_repository_error():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:161:    price, price_source, traceability = _resolve_effective_leg_price(
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:164:        leg_source="rtd",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:165:        rtd_option_quotes_repository=repository,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:170:    assert price_source == "snapshot"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:173:def test_snapshot_result_to_payload_uses_rtd_price_for_canonical_leg_fields(tmp_path):
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:178:                "ultimo_preco": 9.99,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:192:                "source": "rtd",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:197:        source="rtd",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:199:        manual_overrides=[],
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:202:    payload = _snapshot_result_to_payload(
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:208:        rtd_option_quotes_repository=repository,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:215:    assert leg["price_source"] == "rtd_option_quotes"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:220:def test_resolve_effective_leg_price_exposes_rtd_quote_traceability_metadata():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:226:                "ultimo_preco": 9.99,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:227:                "source": "rtd_option_quotes",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:234:    price, price_source, traceability = _resolve_effective_leg_price(
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:237:        leg_source="rtd",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:238:        rtd_option_quotes_repository=repository,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:243:    assert price_source == "rtd_option_quotes"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:246:        "rtd_quote_found": True,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:247:        "rtd_validation_status": "ok",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:248:        "rtd_validation_message": None,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:249:        "rtd_price_field": "ultimo_preco",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:250:        "rtd_quote_codigo_opcao": "ABCD11",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:251:        "rtd_quote_ativo_base": "ABCD",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:252:        "rtd_price_source": "rtd_option_quotes",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:253:        "rtd_price_updated_at": "2026-06-15T10:01:00",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:254:        "rtd_price_created_at": "2026-06-15T10:00:00",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:258:def test_resolve_effective_leg_price_falls_back_to_snapshot_when_rtd_quote_has_no_usable_price():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:264:                "ultimo_preco": 0,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:267:                "bid": 0,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:268:                "ask": 0,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:269:                "source": "rtd_option_quotes",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:276:    price, price_source, traceability = _resolve_effective_leg_price(
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:279:        leg_source="rtd",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:280:        rtd_option_quotes_repository=repository,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:285:    assert price_source == "snapshot"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:286:    assert traceability["price_resolution_status"] == "invalid_rtd_price"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:287:    assert traceability["rtd_quote_found"] is True
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:288:    assert traceability["rtd_validation_status"] == "error"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:289:    assert "sem preço utilizável" in traceability["rtd_validation_message"]
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:290:    assert traceability["rtd_quote_codigo_opcao"] == "ABCD11"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:291:    assert traceability["rtd_quote_ativo_base"] == "ABCD"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:292:    assert traceability["rtd_price_source"] == "rtd_option_quotes"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:293:    assert traceability["rtd_price_updated_at"] == "2026-06-15T10:01:00"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:294:    assert traceability["rtd_price_created_at"] == "2026-06-15T10:00:00"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:297:def test_snapshot_result_to_payload_does_not_leak_rtd_traceability_for_manual_price(tmp_path):
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:303:                "ultimo_preco": 9.99,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:304:                "source": "rtd_option_quotes",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:320:                "source": "manual",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:325:        source="manual",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:327:        manual_overrides=[],
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:330:    payload = _snapshot_result_to_payload(
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:336:        rtd_option_quotes_repository=repository,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:343:    assert leg["price_source"] == "manual"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:344:    assert "rtd_price_field" not in leg
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:345:    assert "rtd_quote_codigo_opcao" not in leg
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:346:    assert "rtd_quote_ativo_base" not in leg
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:347:    assert "rtd_price_source" not in leg
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:348:    assert "rtd_price_updated_at" not in leg
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:349:    assert "rtd_price_created_at" not in leg
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:353:def test_resolve_effective_leg_price_diagnoses_missing_rtd_quote():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:356:    price, price_source, traceability = _resolve_effective_leg_price(
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:359:        leg_source="rtd",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:360:        rtd_option_quotes_repository=repository,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:366:    assert price_source == "snapshot"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:367:    assert traceability["rtd_quote_found"] is False
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:368:    assert traceability["price_resolution_status"] == "missing_rtd_quote"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:369:    assert traceability["rtd_validation_status"] == "error"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:370:    assert "não encontrada" in traceability["rtd_validation_message"]
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:373:def test_resolve_effective_leg_price_diagnoses_invalid_rtd_price():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:379:                "ultimo_preco": 0,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:382:                "bid": 0,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:383:                "ask": 0,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:384:                "source": "rtd_option_quotes",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:389:    price, price_source, traceability = _resolve_effective_leg_price(
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:392:        leg_source="rtd",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:393:        rtd_option_quotes_repository=repository,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:399:    assert price_source == "snapshot"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:400:    assert traceability["rtd_quote_found"] is True
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:401:    assert traceability["price_resolution_status"] == "invalid_rtd_price"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:402:    assert traceability["rtd_validation_status"] == "error"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:403:    assert traceability["rtd_quote_codigo_opcao"] == "ABCD11"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:404:    assert traceability["rtd_quote_ativo_base"] == "ABCD"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:407:def test_resolve_effective_leg_price_diagnoses_rtd_asset_mismatch():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:413:                "ultimo_preco": 9.99,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:414:                "source": "rtd_option_quotes",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:419:    price, price_source, traceability = _resolve_effective_leg_price(
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:422:        leg_source="rtd",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:423:        rtd_option_quotes_repository=repository,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:429:    assert price_source == "snapshot"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:430:    assert traceability["rtd_quote_found"] is True
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:431:    assert traceability["price_resolution_status"] == "rtd_asset_mismatch"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:432:    assert traceability["rtd_validation_status"] == "error"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:433:    assert traceability["rtd_quote_ativo_base"] == "WXYZ"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:434:    assert "diverge" in traceability["rtd_validation_message"]
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:437:def test_snapshot_result_to_payload_preserves_rtd_guardrails_for_valid_quote(tmp_path):
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:443:                "ultimo_preco": 9.99,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:444:                "source": "rtd_option_quotes",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:458:                "source": "rtd",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:463:        source="rtd",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:465:        manual_overrides=[],
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:468:    payload = _snapshot_result_to_payload(
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:474:        rtd_option_quotes_repository=repository,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:479:    assert leg["price_source"] == "rtd_option_quotes"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:481:    assert leg["rtd_quote_found"] is True
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:482:    assert leg["rtd_validation_status"] == "ok"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:483:    assert leg["rtd_validation_message"] is None
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:484:    assert leg["rtd_price_field"] == "ultimo_preco"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:485:    assert leg["rtd_quote_codigo_opcao"] == "ABCD11"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:486:    assert leg["rtd_quote_ativo_base"] == "ABCD"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:489:def test_snapshot_result_to_payload_preserves_rtd_guardrails_when_falling_back_to_snapshot(tmp_path):
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:501:                "source": "rtd",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:506:        source="rtd",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:508:        manual_overrides=[],
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:511:    payload = _snapshot_result_to_payload(
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:517:        rtd_option_quotes_repository=repository,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:524:    assert leg["price_source"] == "snapshot"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:525:    assert leg["price_resolution_status"] == "missing_rtd_quote"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:526:    assert leg["rtd_quote_found"] is False
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:527:    assert leg["rtd_validation_status"] == "error"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:529:def test_resolve_effective_leg_price_falls_back_to_snapshot_when_rtd_quote_is_stale():
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:534:                "ultimo_preco": 9.99,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:535:                "bid": 9.50,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:536:                "ask": 10.50,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:542:    price, price_source, traceability = _resolve_effective_leg_price(
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:545:        leg_source="rtd",
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:546:        rtd_option_quotes_repository=repository,
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:551:    assert price_source == "snapshot"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:552:    assert traceability["price_resolution_status"] == "stale_rtd_quote"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:553:    assert traceability["rtd_quote_found"] is True
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:554:    assert traceability["rtd_validation_status"] == "warn"
ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py:555:    assert "vencida" in traceability["rtd_validation_message"]
ATT/tests/test_pricing_execution_price_source_persistence.py:37:def test_pricing_executions_repository_preserves_leg_price_source_on_get(tmp_path):
ATT/tests/test_pricing_execution_price_source_persistence.py:45:        "structure_name": "Teste RTD",
ATT/tests/test_pricing_execution_price_source_persistence.py:59:                "price_source": "rtd_option_quotes",
ATT/tests/test_pricing_execution_price_source_persistence.py:68:                "price_source": "manual",
ATT/tests/test_pricing_execution_price_source_persistence.py:100:    assert loaded["pricing_payload"]["legs"][0]["price_source"] == "rtd_option_quotes"
ATT/tests/test_pricing_execution_price_source_persistence.py:101:    assert loaded["pricing_payload"]["legs"][1]["price_source"] == "manual"
ATT/tests/test_pricing_execution_price_source_persistence.py:104:def test_pricing_executions_repository_preserves_leg_price_source_on_list(tmp_path):
ATT/tests/test_pricing_execution_price_source_persistence.py:125:                "price_source": "missing",
ATT/tests/test_pricing_execution_price_source_persistence.py:157:    assert executions[0]["pricing_payload"]["legs"][0]["price_source"] == "missing"
ATT/tests/test_pricing_execution_price_source_persistence.py:191:    def create_snapshot(self, **kwargs):
ATT/tests/test_pricing_execution_price_source_persistence.py:196:def test_persistence_service_passes_price_source_to_system_snapshot_legs():
ATT/tests/test_pricing_execution_price_source_persistence.py:198:    fake_snapshots_repository = FakeSystemSnapshotsRepository()
ATT/tests/test_pricing_execution_price_source_persistence.py:202:        system_snapshots_repository=fake_snapshots_repository,
ATT/tests/test_pricing_execution_price_source_persistence.py:222:                "price_source": "rtd_option_quotes",
ATT/tests/test_pricing_execution_price_source_persistence.py:247:    assert response["snapshot_id"] == 321
ATT/tests/test_pricing_execution_price_source_persistence.py:249:    snapshot_call = fake_snapshots_repository.calls[0]
ATT/tests/test_pricing_execution_price_source_persistence.py:251:    assert snapshot_call["legs"][0]["price_source"] == "rtd_option_quotes"
ATT/tests/test_pricing_execution_price_source_persistence.py:253:        snapshot_call["operation_state_json"]["pricing_payload"]["legs"][0]["price_source"]
ATT/tests/test_pricing_execution_price_source_persistence.py:254:        == "rtd_option_quotes"
ATT/tests/test_pricing_execution_price_source_persistence.py:258:def _assert_fase_10e_full_rtd_traceability(leg):
ATT/tests/test_pricing_execution_price_source_persistence.py:259:    assert leg["price_source"] == "rtd_option_quotes"
ATT/tests/test_pricing_execution_price_source_persistence.py:260:    assert leg["rtd_price_field"] == "ultimo_preco"
ATT/tests/test_pricing_execution_price_source_persistence.py:261:    assert leg["rtd_quote_codigo_opcao"] == "ABCD11"
ATT/tests/test_pricing_execution_price_source_persistence.py:262:    assert leg["rtd_quote_ativo_base"] == "ABCD"
ATT/tests/test_pricing_execution_price_source_persistence.py:263:    assert leg["rtd_price_source"] == "rtd_option_quotes"
ATT/tests/test_pricing_execution_price_source_persistence.py:264:    assert leg["rtd_price_updated_at"] == "2026-06-15T10:01:00"
ATT/tests/test_pricing_execution_price_source_persistence.py:265:    assert leg["rtd_price_created_at"] == "2026-06-15T10:01:00"
ATT/tests/test_pricing_execution_price_source_persistence.py:268:def test_fase_10e_pricing_executions_repository_preserves_full_rtd_traceability_on_get_and_list(tmp_path):
ATT/tests/test_pricing_execution_price_source_persistence.py:276:        "structure_name": "Teste RTD completo",
ATT/tests/test_pricing_execution_price_source_persistence.py:292:                "price_source": "rtd_option_quotes",
ATT/tests/test_pricing_execution_price_source_persistence.py:293:                "rtd_price_field": "ultimo_preco",
ATT/tests/test_pricing_execution_price_source_persistence.py:294:                "rtd_quote_codigo_opcao": "ABCD11",
ATT/tests/test_pricing_execution_price_source_persistence.py:295:                "rtd_quote_ativo_base": "ABCD",
ATT/tests/test_pricing_execution_price_source_persistence.py:296:                "rtd_price_source": "rtd_option_quotes",
ATT/tests/test_pricing_execution_price_source_persistence.py:297:                "rtd_price_updated_at": "2026-06-15T10:01:00",
ATT/tests/test_pricing_execution_price_source_persistence.py:298:                "rtd_price_created_at": "2026-06-15T10:01:00",
ATT/tests/test_pricing_execution_price_source_persistence.py:329:    _assert_fase_10e_full_rtd_traceability(
ATT/tests/test_pricing_execution_price_source_persistence.py:335:    _assert_fase_10e_full_rtd_traceability(
ATT/tests/test_pricing_execution_price_source_persistence.py:340:def test_fase_10e_persistence_service_passes_full_rtd_traceability_to_system_snapshot():
ATT/tests/test_pricing_execution_price_source_persistence.py:342:    fake_snapshots_repository = FakeSystemSnapshotsRepository()
ATT/tests/test_pricing_execution_price_source_persistence.py:346:        system_snapshots_repository=fake_snapshots_repository,
ATT/tests/test_pricing_execution_price_source_persistence.py:351:        "structure_name": "Teste Snapshot RTD completo",
ATT/tests/test_pricing_execution_price_source_persistence.py:368:                "price_source": "rtd_option_quotes",
ATT/tests/test_pricing_execution_price_source_persistence.py:369:                "rtd_price_field": "ultimo_preco",
ATT/tests/test_pricing_execution_price_source_persistence.py:370:                "rtd_quote_codigo_opcao": "ABCD11",
ATT/tests/test_pricing_execution_price_source_persistence.py:371:                "rtd_quote_ativo_base": "ABCD",
ATT/tests/test_pricing_execution_price_source_persistence.py:372:                "rtd_price_source": "rtd_option_quotes",
ATT/tests/test_pricing_execution_price_source_persistence.py:373:                "rtd_price_updated_at": "2026-06-15T10:01:00",
ATT/tests/test_pricing_execution_price_source_persistence.py:374:                "rtd_price_created_at": "2026-06-15T10:01:00",
ATT/tests/test_pricing_execution_price_source_persistence.py:399:    assert response["snapshot_id"] == 321
ATT/tests/test_pricing_execution_price_source_persistence.py:401:    snapshot_call = fake_snapshots_repository.calls[0]
ATT/tests/test_pricing_execution_price_source_persistence.py:403:    _assert_fase_10e_full_rtd_traceability(
ATT/tests/test_pricing_execution_price_source_persistence.py:404:        snapshot_call["legs"][0]
ATT/tests/test_pricing_execution_price_source_persistence.py:407:    _assert_fase_10e_full_rtd_traceability(
ATT/tests/test_pricing_execution_price_source_persistence.py:408:        snapshot_call["operation_state_json"]["pricing_payload"]["legs"][0]
