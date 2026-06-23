# Diagnostico funcional real - Fases 3 e 4

Data: Tue Jun 23 20:10:34     2026
Branch: reinicio-normalizacao-idioma-ptbr
HEAD: 545f4e6

## Status git
 M UI/components/structure_editor_dialog.py
 M repositories/rtd_option_quotes_repository.py
 M services/structure_leg_rtd_enrichment_service.py
?? docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_3_CADASTRO_ASSISTIDO.md
?? docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_4_PAYOFF_DECISOES.md
?? docs/checkpoints/evidencias/fase-3-4-alvos-provaveis-correcao.txt
?? docs/checkpoints/evidencias/fase-3-4-diagnostico-bugs-provaveis.md
?? docs/checkpoints/evidencias/fase-3-4-fluxo-manual-real-diagnostico.md
?? docs/checkpoints/evidencias/fase-3-contexto-cirurgico-codigo.md
?? docs/checkpoints/evidencias/fase-3-correcao-codigo-inventario.txt
?? docs/checkpoints/evidencias/fase-4-contexto-cirurgico-codigo.md
?? docs/checkpoints/evidencias/fase-4-correcao-codigo-inventario.txt
?? tools/

## Fase 3 - Cadastro assistido por simbolo
Objetivo:
- usuario informa nome da estrutura e dados minimos da leg;
- sistema reconhece simbolo da opcao;
- sistema preenche ativo objeto, strike, vencimento, multiplicador e metadados;
- divergencia entre tipo informado e tipo detectado deve bloquear ou pedir confirmacao;
- estrutura so deve ser funcional se tiver dados minimos para payoff e decisoes.

## Fase 4 - Estrutura manual integrada a payoff e decisoes
Objetivo:
- estrutura manual/assistida valida deve gerar curva de payoff;
- estrutura manual/assistida valida deve gerar decisao;
- structure_decisions deve receber linhas ou registrar rejeicao clara;
- payoff_curve_points deve receber pontos ou registrar rejeicao clara;
- logs devem indicar estruturas lidas, processadas, ignoradas e rejeitadas.

## Grep - simbolo/opcao/strike/vencimento/multiplicador
ATT/tests/test_audit_rtd_option_quotes.py:28:    unique_sql = ", UNIQUE(codigo_opcao)" if unique else ""
ATT/tests/test_audit_rtd_option_quotes.py:35:                codigo_opcao TEXT NOT NULL,
ATT/tests/test_audit_rtd_option_quotes.py:36:                ativo_base TEXT,
ATT/tests/test_audit_rtd_option_quotes.py:37:                call_put TEXT,
ATT/tests/test_audit_rtd_option_quotes.py:38:                strike REAL,
ATT/tests/test_audit_rtd_option_quotes.py:39:                vencimento TEXT,
ATT/tests/test_audit_rtd_option_quotes.py:62:    codigo_opcao: str,
ATT/tests/test_audit_rtd_option_quotes.py:67:        params = (codigo_opcao,)
ATT/tests/test_audit_rtd_option_quotes.py:70:        params = (codigo_opcao, updated_at)
ATT/tests/test_audit_rtd_option_quotes.py:76:                codigo_opcao,
ATT/tests/test_audit_rtd_option_quotes.py:77:                ativo_base,
ATT/tests/test_audit_rtd_option_quotes.py:78:                call_put,
ATT/tests/test_audit_rtd_option_quotes.py:79:                strike,
ATT/tests/test_audit_rtd_option_quotes.py:152:                codigo_opcao TEXT NOT NULL
ATT/tests/test_audit_rtd_option_quotes.py:160:    assert "ativo_base" in result["missing_columns"]
ATT/tests/test_audit_rtd_option_quotes.py:164:def test_audit_reports_error_for_duplicated_codigo_opcao(tmp_path: Path):
ATT/tests/test_audit_rtd_option_quotes.py:176:    assert "duplicated codigo_opcao groups: 1" in result["errors"]
ATT/tests/test_canonical_input_service.py:17:    def get_snapshot(self, underlying_asset, reference_date=None):
ATT/tests/test_canonical_input_service.py:20:            "underlying_asset": underlying_asset,
ATT/tests/test_canonical_input_service.py:72:            "underlying_asset": "BOVA11",
ATT/tests/test_canonical_input_service.py:78:                    "symbol": "BOVAE195",
ATT/tests/test_canonical_input_service.py:79:                    "strike": 195.0,
ATT/tests/test_canonical_input_service.py:80:                    "expiration_date": "2026-05-15",
ATT/tests/test_canonical_input_service.py:83:                    "multiplier": 1.0,
ATT/tests/test_canonical_input_service.py:107:        self.assertEqual(result["structure"]["legs"][0]["symbol"], "BOVAE195")
ATT/tests/test_canonical_input_service.py:114:            "underlying_asset": "BOVA11",
ATT/tests/test_canonical_input_service.py:128:                        "symbol": "BOVAE195",
ATT/tests/test_canonical_input_service.py:129:                        "strike": 195.0,
ATT/tests/test_canonical_input_service.py:130:                        "expiration_date": "2026-05-15",
ATT/tests/test_canonical_input_service.py:133:                        "multiplier": 1.0,
ATT/tests/test_canonical_input_service.py:150:        self.assertEqual(result["structure"]["legs"][0]["symbol"], "BOVAE195")
ATT/tests/test_canonical_input_service.py:157:            "underlying_asset": "BOVA11",
ATT/tests/test_canonical_input_service.py:187:            "underlying_asset": "BOVA11",
ATT/tests/test_canonical_input_service.py:217:            "underlying_asset": "BOVA11",
ATT/tests/test_canonical_input_service.py:223:                    "symbol": "BOVAM190",
ATT/tests/test_canonical_input_service.py:224:                    "strike": 190.0,
ATT/tests/test_canonical_input_service.py:225:                    "expiration_date": "2026-05-20",
ATT/tests/test_canonical_input_service.py:234:                    "multiplier": 1.0,
ATT/tests/test_canonical_input_service.py:239:                    "symbol": "BOVAM185",
ATT/tests/test_canonical_input_service.py:240:                    "strike": 185.0,
ATT/tests/test_canonical_input_service.py:241:                    "expiration_date": "2026-05-17",
ATT/tests/test_canonical_input_service.py:250:                    "multiplier": 1.0,
ATT/tests/test_canonical_input_service.py:287:            "underlying_asset": "BOVA11",
ATT/tests/test_canonical_pricing_facade.py:14:        "aba": "ABA_LEGADA_NAO_E_UNDERLYING",
ATT/tests/test_canonical_pricing_facade.py:43:                    "strike": raw_numeric,
ATT/tests/test_canonical_pricing_facade.py:48:        underlying_asset="ABCD11",
ATT/tests/test_canonical_pricing_facade.py:58:    assert leg["strike"] == pytest.approx(expected)
ATT/tests/test_canonical_pricing_facade.py:61:def test_snapshot_result_to_payload_uses_explicit_underlying_asset_not_legacy_aba(tmp_path):
ATT/tests/test_canonical_pricing_facade.py:70:                "strike": "100,00",
ATT/tests/test_canonical_pricing_facade.py:82:        underlying_asset="SMAL11",
ATT/tests/test_canonical_pricing_facade.py:88:    assert payload["underlying_asset"] == "SMAL11"
ATT/tests/test_canonical_pricing_facade.py:101:    assert leg["symbol"] == "SMALF100"
ATT/tests/test_canonical_pricing_facade.py:104:    assert leg["strike"] == 100.0
ATT/tests/test_canonical_pricing_facade.py:106:    assert leg["expiration_date"] == "2026-07-17"
ATT/tests/test_canonical_pricing_facade.py:125:        underlying_asset="ABCD11",
ATT/tests/test_canonical_pricing_facade.py:139:        conn.execute("CREATE TABLE market_prices (underlying_asset TEXT, spot REAL)")
ATT/tests/test_canonical_pricing_facade.py:141:            "INSERT INTO market_prices (underlying_asset, spot) VALUES (?, ?)",
ATT/tests/test_canonical_pricing_facade.py:149:        underlying_asset="SMAL11",
ATT/tests/test_canonical_pricing_facade.py:164:            underlying_asset="SMAL11",
ATT/tests/test_canonical_pricing_facade.py:169:    assert "spot_price inválido ou ausente para underlying_asset=SMAL11" in str(exc.value)
ATT/tests/test_canonical_pricing_facade_manual_without_alias.py:11:            "underlying_asset": "BOVA11",
ATT/tests/test_canonical_validators.py:9:            "underlying_asset": "BOVA11",
ATT/tests/test_canonical_validators.py:14:                    "symbol": "BOVAE195",
ATT/tests/test_canonical_validators.py:15:                    "strike": 195.0,
ATT/tests/test_canonical_validators.py:16:                    "expiration_date": "2026-05-15",
ATT/tests/test_canonical_validators.py:19:                    "multiplier": 1.0,
ATT/tests/test_canonical_validators.py:25:            "underlying_asset": "BOVA11",
ATT/tests/test_contracts.py:9:            "underlying_asset": "BOVA11",
ATT/tests/test_contracts.py:14:                    "symbol": "BOVAE195",
ATT/tests/test_contracts.py:15:                    "strike": 195.0,
ATT/tests/test_contracts.py:16:                    "expiration_date": "2026-05-15",
ATT/tests/test_contracts.py:19:                    "multiplier": 1.0,
ATT/tests/test_contracts.py:25:            "underlying_asset": "BOVA11",
ATT/tests/test_contracts.py:43:    assert result["structure"]["underlying_asset"] == "BOVA11"
ATT/tests/test_derived_service.py:18:        underlying_asset="BOVA11",
ATT/tests/test_derived_service.py:29:        underlying_asset="BOVA11",
ATT/tests/test_derived_service.py:40:        underlying_asset="PETR4",
ATT/tests/test_derived_service.py:46:def test_resolve_storage_key_should_use_underlying_asset_as_last_named_key():
ATT/tests/test_derived_service.py:51:        underlying_asset="PETR4",
ATT/tests/test_derived_service.py:62:        underlying_asset=None,
ATT/tests/test_derived_service.py:73:        underlying_asset="BOVA11",
ATT/tests/test_derived_service.py:81:    assert result["underlying_asset"] == "BOVA11"
ATT/tests/test_derived_service.py:102:        "underlying_asset": "PETR4",
ATT/tests/test_derived_service.py:119:    assert captured["meta"]["underlying_asset"] == "PETR4"
ATT/tests/test_derived_service.py:145:        underlying_asset="VALE3",
ATT/tests/test_derived_service.py:154:    assert captured["decision"]["meta"]["underlying_asset"] == "VALE3"
ATT/tests/test_import_rtd_links_to_option_quotes.py:33:                codigo_opcao TEXT NOT NULL,
ATT/tests/test_import_rtd_links_to_option_quotes.py:34:                ativo_base TEXT,
ATT/tests/test_import_rtd_links_to_option_quotes.py:36:                call_put TEXT,
ATT/tests/test_import_rtd_links_to_option_quotes.py:37:                strike REAL,
ATT/tests/test_import_rtd_links_to_option_quotes.py:38:                vencimento TEXT,
ATT/tests/test_import_rtd_links_to_option_quotes.py:59:                UNIQUE(codigo_opcao)
ATT/tests/test_import_rtd_links_to_option_quotes.py:73:                "codigo_opcao",
ATT/tests/test_import_rtd_links_to_option_quotes.py:74:                "ativo_base",
ATT/tests/test_import_rtd_links_to_option_quotes.py:83:def fetch_option(db_path: Path, codigo_opcao: str) -> sqlite3.Row | None:
ATT/tests/test_import_rtd_links_to_option_quotes.py:91:                codigo_opcao,
ATT/tests/test_import_rtd_links_to_option_quotes.py:92:                ativo_base,
ATT/tests/test_import_rtd_links_to_option_quotes.py:93:                call_put,
ATT/tests/test_import_rtd_links_to_option_quotes.py:94:                strike,
ATT/tests/test_import_rtd_links_to_option_quotes.py:95:                vencimento,
ATT/tests/test_import_rtd_links_to_option_quotes.py:104:            WHERE codigo_opcao = ?
ATT/tests/test_import_rtd_links_to_option_quotes.py:106:            (codigo_opcao,),
ATT/tests/test_import_rtd_links_to_option_quotes.py:131:def test_normalize_call_put_accepts_aliases():
ATT/tests/test_import_rtd_links_to_option_quotes.py:132:    assert importer.normalize_call_put("CALL") == "CALL"
ATT/tests/test_import_rtd_links_to_option_quotes.py:133:    assert importer.normalize_call_put("c") == "CALL"
ATT/tests/test_import_rtd_links_to_option_quotes.py:134:    assert importer.normalize_call_put("compra") == "CALL"
ATT/tests/test_import_rtd_links_to_option_quotes.py:136:    assert importer.normalize_call_put("PUT") == "PUT"
ATT/tests/test_import_rtd_links_to_option_quotes.py:137:    assert importer.normalize_call_put("p") == "PUT"
ATT/tests/test_import_rtd_links_to_option_quotes.py:138:    assert importer.normalize_call_put("venda") == "PUT"
ATT/tests/test_import_rtd_links_to_option_quotes.py:140:    assert importer.normalize_call_put("") is None
ATT/tests/test_import_rtd_links_to_option_quotes.py:149:            ["PETRA123", "PETR4", "call_put", "CALL", "2026-06-06 17:50:00"],
ATT/tests/test_import_rtd_links_to_option_quotes.py:150:            ["PETRA123", "PETR4", "strike", "32.50", "2026-06-06 17:50:00"],
ATT/tests/test_import_rtd_links_to_option_quotes.py:151:            ["PETRA123", "PETR4", "vencimento", "2026-07-19", "2026-06-06 17:50:00"],
ATT/tests/test_import_rtd_links_to_option_quotes.py:167:    assert record["codigo_opcao"] == "PETRA123"
ATT/tests/test_import_rtd_links_to_option_quotes.py:168:    assert record["ativo_base"] == "PETR4"
ATT/tests/test_import_rtd_links_to_option_quotes.py:169:    assert record["call_put"] == "CALL"
ATT/tests/test_import_rtd_links_to_option_quotes.py:170:    assert record["strike"] == pytest.approx(32.50)
ATT/tests/test_import_rtd_links_to_option_quotes.py:171:    assert record["vencimento"] == "2026-07-19"
ATT/tests/test_import_rtd_links_to_option_quotes.py:190:            ["PETRA123", "PETR4", "call_put", "CALL", "2026-06-06 17:50:00"],
ATT/tests/test_import_rtd_links_to_option_quotes.py:191:            ["PETRA123", "PETR4", "strike", "32.50", "2026-06-06 17:50:00"],
ATT/tests/test_import_rtd_links_to_option_quotes.py:218:            ["PETRA123", "PETR4", "call_put", "CALL", "2026-06-06 17:50:00"],
ATT/tests/test_import_rtd_links_to_option_quotes.py:219:            ["PETRA123", "PETR4", "strike", "32.50", "2026-06-06 17:50:00"],
ATT/tests/test_import_rtd_links_to_option_quotes.py:238:            ["PETRA123", "PETR4", "call_put", "CALL", "2026-06-06 18:00:00"],
ATT/tests/test_import_rtd_links_to_option_quotes.py:239:            ["PETRA123", "PETR4", "strike", "32.50", "2026-06-06 18:00:00"],
ATT/tests/test_import_rtd_links_to_option_quotes.py:258:    assert option["codigo_opcao"] == "PETRA123"
ATT/tests/test_import_rtd_links_to_option_quotes.py:259:    assert option["ativo_base"] == "PETR4"
ATT/tests/test_import_rtd_links_to_option_quotes.py:260:    assert option["call_put"] == "CALL"
ATT/tests/test_import_rtd_links_to_option_quotes.py:261:    assert option["strike"] == pytest.approx(32.50)
ATT/tests/test_legacy_robo_legs_fallback.py:93:                "call_put": "CALL",
ATT/tests/test_legacy_robo_legs_fallback.py:94:                "ativo": "PETR4",
ATT/tests/test_legacy_robo_legs_fallback.py:95:                "strike": 100,
ATT/tests/test_legacy_robo_legs_fallback.py:96:                "vencimento": "2026-06-20",
ATT/tests/test_legacy_robo_legs_fallback.py:112:    assert legs[0]["symbol"] == "PETR4"
ATT/tests/test_legacy_robo_legs_fallback.py:113:    assert legs[0]["strike"] == 100.0
ATT/tests/test_legacy_structure_legs_importer.py:17:            underlying_asset TEXT NOT NULL,
ATT/tests/test_legacy_structure_legs_importer.py:32:            symbol TEXT,
ATT/tests/test_legacy_structure_legs_importer.py:33:            strike REAL NOT NULL,
ATT/tests/test_legacy_structure_legs_importer.py:34:            expiration_date TEXT NOT NULL,
ATT/tests/test_legacy_structure_legs_importer.py:37:            multiplier REAL NOT NULL DEFAULT 1,
ATT/tests/test_legacy_structure_legs_importer.py:57:            id, name, underlying_asset, alias_legacy_aba,
ATT/tests/test_legacy_structure_legs_importer.py:74:            structure_id, position_side, option_type, symbol,
ATT/tests/test_legacy_structure_legs_importer.py:75:            strike, expiration_date, quantity, premium,
ATT/tests/test_legacy_structure_legs_importer.py:76:            multiplier, leg_order, notes, created_at, updated_at
ATT/tests/test_legacy_structure_legs_importer.py:117:            "symbol": "BOVAE195",
ATT/tests/test_legacy_structure_legs_importer.py:118:            "strike": 195.0,
ATT/tests/test_legacy_structure_legs_importer.py:119:            "expiration_date": "2026-06-20",
ATT/tests/test_legacy_structure_legs_importer.py:122:            "multiplier": 1.0,
ATT/tests/test_legacy_structure_legs_importer.py:128:            "symbol": "BOVAE200",
ATT/tests/test_legacy_structure_legs_importer.py:129:            "strike": 200.0,
ATT/tests/test_legacy_structure_legs_importer.py:130:            "expiration_date": "2026-06-20",
ATT/tests/test_legacy_structure_legs_importer.py:133:            "multiplier": 1.0,
ATT/tests/test_legacy_structure_legs_importer.py:166:    assert [leg["symbol"] for leg in legs] == ["BOVAE195", "BOVAE200"]
ATT/tests/test_legacy_structure_legs_importer.py:202:    assert repo.get_structure(123)["legs"][0]["symbol"] == "OLDLEG"
ATT/tests/test_legacy_structure_legs_importer.py:215:            "symbol": "BOVAE195",
ATT/tests/test_legacy_structure_legs_importer.py:216:            "strike": 195.0,
ATT/tests/test_legacy_structure_legs_importer.py:217:            "expiration_date": "2026-06-20",
ATT/tests/test_legacy_structure_legs_importer.py:220:            "multiplier": 1.0,
ATT/tests/test_legacy_structure_legs_importer_integration.py:20:            underlying_asset TEXT NOT NULL,
ATT/tests/test_legacy_structure_legs_importer_integration.py:35:            symbol TEXT,
ATT/tests/test_legacy_structure_legs_importer_integration.py:36:            strike REAL NOT NULL,
ATT/tests/test_legacy_structure_legs_importer_integration.py:37:            expiration_date TEXT NOT NULL,
ATT/tests/test_legacy_structure_legs_importer_integration.py:40:            multiplier REAL NOT NULL DEFAULT 1,
ATT/tests/test_legacy_structure_legs_importer_integration.py:55:            call_put TEXT,
ATT/tests/test_legacy_structure_legs_importer_integration.py:56:            strike REAL,
ATT/tests/test_legacy_structure_legs_importer_integration.py:58:            ativo TEXT,
ATT/tests/test_legacy_structure_legs_importer_integration.py:59:            vencimento TEXT,
ATT/tests/test_legacy_structure_legs_importer_integration.py:70:            call_put TEXT,
ATT/tests/test_legacy_structure_legs_importer_integration.py:71:            strike REAL,
ATT/tests/test_legacy_structure_legs_importer_integration.py:73:            ativo TEXT,
ATT/tests/test_legacy_structure_legs_importer_integration.py:74:            vencimento TEXT,
ATT/tests/test_legacy_structure_legs_importer_integration.py:91:            id, name, underlying_asset, alias_legacy_aba,
ATT/tests/test_legacy_structure_legs_importer_integration.py:111:            structure_id, position_side, option_type, symbol,
ATT/tests/test_legacy_structure_legs_importer_integration.py:112:            strike, expiration_date, quantity, premium,
ATT/tests/test_legacy_structure_legs_importer_integration.py:113:            multiplier, leg_order, notes, created_at, updated_at
ATT/tests/test_legacy_structure_legs_importer_integration.py:133:            id, aba, timestamp, cv, call_put,
ATT/tests/test_legacy_structure_legs_importer_integration.py:134:            strike, quant, ativo, vencimento, preco
ATT/tests/test_legacy_structure_legs_importer_integration.py:152:            id, aba, timestamp, cv, call_put,
ATT/tests/test_legacy_structure_legs_importer_integration.py:153:            strike, quant, ativo, vencimento, preco
ATT/tests/test_legacy_structure_legs_importer_integration.py:218:    assert imported_leg["symbol"] == "MANUALPUT185"
ATT/tests/test_legacy_structure_legs_importer_integration.py:219:    assert imported_leg["strike"] == 185.0
ATT/tests/test_legacy_structure_legs_importer_integration.py:220:    assert imported_leg["expiration_date"] == "2026-06-20"
ATT/tests/test_legacy_structure_legs_importer_integration.py:223:    assert imported_leg["multiplier"] == 1.0
ATT/tests/test_legacy_structure_legs_importer_integration.py:228:    assert imported_leg["symbol"] != "OLDLEG"
ATT/tests/test_legacy_structure_legs_importer_integration.py:229:    assert imported_leg["symbol"] != "RTDLEG190"
ATT/tests/test_legacy_structure_legs_reader.py:28:            call_put="CALL",
ATT/tests/test_legacy_structure_legs_reader.py:29:            ativo=" bovae195 ",
ATT/tests/test_legacy_structure_legs_reader.py:30:            strike=195.0,
ATT/tests/test_legacy_structure_legs_reader.py:31:            vencimento=datetime(2026, 5, 15),
ATT/tests/test_legacy_structure_legs_reader.py:37:            call_put="PUT",
ATT/tests/test_legacy_structure_legs_reader.py:38:            ativo=" bovao185 ",
ATT/tests/test_legacy_structure_legs_reader.py:39:            strike=185.0,
ATT/tests/test_legacy_structure_legs_reader.py:40:            vencimento=datetime(2026, 5, 15),
ATT/tests/test_legacy_structure_legs_reader.py:65:            "symbol": "BOVAE195",
ATT/tests/test_legacy_structure_legs_reader.py:66:            "strike": 195.0,
ATT/tests/test_legacy_structure_legs_reader.py:67:            "expiration_date": "2026-05-15",
ATT/tests/test_legacy_structure_legs_reader.py:70:            "multiplier": 1.0,
ATT/tests/test_legacy_structure_legs_reader.py:76:            "symbol": "BOVAO185",
ATT/tests/test_legacy_structure_legs_reader.py:77:            "strike": 185.0,
ATT/tests/test_legacy_structure_legs_reader.py:78:            "expiration_date": "2026-05-15",
ATT/tests/test_legacy_structure_legs_reader.py:81:            "multiplier": 1.0,
ATT/tests/test_legacy_structure_legs_reader.py:91:            call_put="CALL",
ATT/tests/test_legacy_structure_legs_reader.py:92:            ativo="BOVAE195",
ATT/tests/test_legacy_structure_legs_reader.py:93:            strike=195.0,
ATT/tests/test_legacy_structure_legs_reader.py:94:            vencimento=datetime(2026, 5, 15),
ATT/tests/test_legacy_structure_legs_reader.py:120:            underlying_asset TEXT,
ATT/tests/test_legacy_structure_legs_reader.py:132:            call_put TEXT,
ATT/tests/test_legacy_structure_legs_reader.py:133:            strike REAL,
ATT/tests/test_legacy_structure_legs_reader.py:135:            ativo TEXT,
ATT/tests/test_legacy_structure_legs_reader.py:136:            vencimento TEXT,
ATT/tests/test_legacy_structure_legs_reader.py:147:            call_put TEXT,
ATT/tests/test_legacy_structure_legs_reader.py:148:            strike REAL,
ATT/tests/test_legacy_structure_legs_reader.py:150:            ativo TEXT,
ATT/tests/test_legacy_structure_legs_reader.py:151:            vencimento TEXT,
ATT/tests/test_legacy_structure_legs_reader.py:175:        (id, name, underlying_asset, alias_legacy_aba, status)
ATT/tests/test_legacy_structure_legs_reader.py:181:        (id, aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco)
ATT/tests/test_legacy_structure_legs_reader.py:213:            "symbol": "BOVAE195",
ATT/tests/test_legacy_structure_legs_reader.py:214:            "strike": 195.0,
ATT/tests/test_legacy_structure_legs_reader.py:215:            "expiration_date": "2026-06-20",
ATT/tests/test_legacy_structure_legs_reader.py:218:            "multiplier": 1.0,
ATT/tests/test_legacy_structure_legs_reader.py:238:        (id, name, underlying_asset, alias_legacy_aba, status)
ATT/tests/test_market_snapshot_provider.py:23:        "underlying_asset": "BOVA11",
ATT/tests/test_market_snapshot_provider.py:45:    assert snapshot["underlying_asset"] == "PETR4"
ATT/tests/test_market_snapshot_provider.py:51:def test_get_snapshot_raises_when_underlying_asset_is_missing():
ATT/tests/test_market_snapshot_provider.py:62:    with pytest.raises(ValueError, match="underlying_asset is required"):
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:14:            ativo TEXT,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:16:            call_put TEXT,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:28:            strike TEXT,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:29:            vencimento TEXT,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:41:            codigo_opcao TEXT,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:42:            ativo_base TEXT,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:43:            call_put TEXT,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:44:            strike TEXT,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:45:            vencimento TEXT,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:71:            ativo,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:73:            call_put,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:85:            strike,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:86:            vencimento,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:128:                codigo_opcao,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:129:                ativo_base,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:130:                call_put,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:131:                strike,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:132:                vencimento,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:184:    assert leg.ativo == "BOVAE195"
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:192:    assert leg.call_put == "CALL"
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:197:    assert leg.strike == 195.0
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:198:    assert leg.vencimento == "2026-05-15"
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:223:    codigo_opcao="BOVAE195",
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:224:    ativo_base="BOVA11",
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:225:    call_put="CALL",
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:226:    strike="195,00",
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:227:    vencimento="2026-05-15",
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:241:            codigo_opcao,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:242:            ativo_base,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:243:            call_put,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:244:            strike,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:245:            vencimento,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:264:            codigo_opcao,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:265:            ativo_base,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:266:            call_put,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:267:            strike,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:268:            vencimento,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:296:            codigo_opcao="BOVAE195",
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:297:            ativo_base="BOVA11",
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:321:            codigo_opcao="BOVAE195",
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:322:            ativo_base="BOVA11",
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:336:            codigo_opcao="BOVAE195",
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:337:            ativo_base="BOVA11",
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:360:    assert leg.ativo == "BOVAE195"
ATT/tests/test_market_snapshot_selector.py:7:def _leg(ativo, source, valor_executado):
ATT/tests/test_market_snapshot_selector.py:9:        ativo=ativo,
ATT/tests/test_orchestrator_run_methods.py:30:        strike=100.0,
ATT/tests/test_orchestrator_run_methods.py:31:        expiration_date="2026-12-19",
ATT/tests/test_orchestrator_run_methods.py:33:        symbol="PETR4C100",
ATT/tests/test_orchestrator_run_methods.py:35:        multiplier=100,
ATT/tests/test_orchestrator_run_methods.py:43:def _make_request(*, spot=50.0, underlying="PETR4", legs=None):
ATT/tests/test_orchestrator_run_methods.py:49:        underlying_asset=underlying,
ATT/tests/test_orchestrator_run_methods.py:55:        underlying_asset=underlying,
ATT/tests/test_orchestrator_run_methods.py:75:        req = _make_request(underlying="VALE3")
ATT/tests/test_orchestrator_run_methods.py:78:        assert s["underlying_asset"] == "VALE3"
ATT/tests/test_orchestrator_run_methods.py:84:        leg = _make_leg(strike=110.0, option_type="put", position_side="short")
ATT/tests/test_orchestrator_run_methods.py:87:        assert legs[0]["strike"] == 110.0
ATT/tests/test_orchestrator_run_methods.py:95:        assert m["underlying_asset"] == "PETR4"
ATT/tests/test_orchestrator_run_methods.py:110:            _make_leg(strike=100.0, leg_order=0),
ATT/tests/test_orchestrator_run_methods.py:111:            _make_leg(strike=110.0, option_type="put", leg_order=1),
ATT/tests/test_orchestrator_run_methods.py:116:        assert result_legs[1]["strike"] == 110.0
ATT/tests/test_orchestrator_run_methods.py:249:            strike=50.0,
ATT/tests/test_orchestrator_run_methods.py:254:            multiplier=100,
ATT/tests/test_orchestrator_run_methods.py:255:            expiration_date="2026-12-19",
ATT/tests/test_payoff_canonical.py:9:            "underlying_asset": "BOVA11",
ATT/tests/test_payoff_canonical.py:14:                    "symbol": "BOVAE195",
ATT/tests/test_payoff_canonical.py:15:                    "strike": 195.0,
ATT/tests/test_payoff_canonical.py:16:                    "expiration_date": "2026-05-15",
ATT/tests/test_payoff_canonical.py:19:                    "multiplier": 1.0,
ATT/tests/test_payoff_canonical.py:25:            "underlying_asset": "BOVA11",
ATT/tests/test_payoff_canonical.py:41:    assert result["underlying_asset"] == "BOVA11"
ATT/tests/test_payoff_pricing_engine.py:11:        "underlying_asset": "BOVA11",
ATT/tests/test_payoff_pricing_engine.py:20:                "strike": 100.0,
ATT/tests/test_payoff_pricing_engine.py:22:                "multiplier": 100,
ATT/tests/test_payoff_pricing_engine.py:33:    assert result["underlying_asset"] == "BOVA11"
ATT/tests/test_payoff_pricing_engine.py:60:        "underlying_asset": "BOVA11",
ATT/tests/test_payoff_pricing_engine.py:69:                "strike": 100.0,
ATT/tests/test_payoff_pricing_engine.py:71:                "multiplier": 100,
ATT/tests/test_payoff_pricing_engine.py:95:        "underlying_asset": "BOVA11",
ATT/tests/test_payoff_pricing_engine.py:112:        "underlying_asset": "BOVA11",
ATT/tests/test_payoff_pricing_engine.py:121:                "strike": 100.0,
ATT/tests/test_payoff_pricing_engine.py:123:                "multiplier": 100,
ATT/tests/test_pricing_execution_app_service.py:18:    def list_execution_summaries(self, structure_id=None, underlying_asset=None,
ATT/tests/test_pricing_execution_app_service.py:21:            "structure_id": structure_id, "underlying_asset": underlying_asset,
ATT/tests/test_pricing_execution_app_service.py:26:    def get_latest_execution_summary(self, structure_id=None, underlying_asset=None,
ATT/tests/test_pricing_execution_app_service.py:29:            "structure_id": structure_id, "underlying_asset": underlying_asset,
ATT/tests/test_pricing_execution_app_service.py:38:    def paginate_execution_summaries(self, structure_id=None, underlying_asset=None,
ATT/tests/test_pricing_execution_app_service.py:42:            "structure_id": structure_id, "underlying_asset": underlying_asset,
ATT/tests/test_pricing_execution_app_service.py:126:        structure_id=1, underlying_asset="PETR4",
ATT/tests/test_pricing_execution_app_service.py:131:        "structure_id": 1, "underlying_asset": "PETR4",
ATT/tests/test_pricing_execution_app_service.py:140:        structure_id=2, underlying_asset="VALE3",
ATT/tests/test_pricing_execution_app_service.py:145:        "structure_id": 2, "underlying_asset": "VALE3",
ATT/tests/test_pricing_execution_app_service.py:162:        structure_id=1, underlying_asset="PETR4",
ATT/tests/test_pricing_execution_app_service.py:169:        "structure_id": 1, "underlying_asset": "PETR4",
ATT/tests/test_pricing_execution_controller.py:47:        underlying_asset=None,
ATT/tests/test_pricing_execution_controller.py:58:                    "underlying_asset": underlying_asset,
ATT/tests/test_pricing_execution_controller.py:73:        underlying_asset=None,
ATT/tests/test_pricing_execution_controller.py:82:                    "underlying_asset": underlying_asset,
ATT/tests/test_pricing_execution_controller.py:188:                "underlying_asset": "PETR4",
ATT/tests/test_pricing_execution_controller.py:208:                "underlying_asset": "PETR4",
ATT/tests/test_pricing_execution_controller.py:243:                "underlying_asset": "PETR4",
ATT/tests/test_pricing_execution_controller.py:255:                "underlying_asset": "PETR4",
ATT/tests/test_pricing_execution_persistence_service.py:188:        "underlying_asset": "PETR4",
ATT/tests/test_pricing_execution_persistence_service.py:202:                "symbol": "PETR4C360",
ATT/tests/test_pricing_execution_persistence_service.py:203:                "strike": 36.0,
ATT/tests/test_pricing_execution_persistence_service.py:249:    assert call["underlying_asset"] == "PETR4"
ATT/tests/test_pricing_execution_persistence_service.py:317:            "underlying_asset": "PETR4",
ATT/tests/test_pricing_execution_persistence_service.py:353:            "underlying_asset": "PETR4",
ATT/tests/test_pricing_execution_query_service.py:21:    underlying_asset: str = "PETR4",
ATT/tests/test_pricing_execution_query_service.py:38:        "underlying_asset": underlying_asset,
ATT/tests/test_pricing_execution_query_service.py:49:            "underlying_asset": underlying_asset,
ATT/tests/test_pricing_execution_query_service.py:163:def test_list_execution_summaries_filters_by_underlying_asset():
ATT/tests/test_pricing_execution_query_service.py:165:        make_execution(1, underlying_asset="PETR4"),
ATT/tests/test_pricing_execution_query_service.py:166:        make_execution(2, underlying_asset="VALE3"),
ATT/tests/test_pricing_execution_query_service.py:172:    summaries = service.list_execution_summaries(underlying_asset="VALE3")
ATT/tests/test_pricing_execution_query_service.py:175:    assert summaries[0]["underlying_asset"] == "VALE3"
ATT/tests/test_pricing_execution_query_service.py:223:def test_list_execution_summaries_rejects_empty_underlying_asset():
ATT/tests/test_pricing_execution_query_service.py:229:        service.list_execution_summaries(underlying_asset="   ")
ATT/tests/test_pricing_execution_query_service.py:232:        assert str(exc) == "underlying_asset must not be empty"
ATT/tests/test_pricing_executions_repository.py:18:            underlying_asset   TEXT,
ATT/tests/test_pricing_executions_repository.py:41:        "underlying_asset": "BOVA11",
ATT/tests/test_pricing_executions_repository.py:65:    assert record["underlying_asset"] == "BOVA11"
ATT/tests/test_pricing_executions_repository.py:98:    assert record["underlying_asset"] is None
ATT/tests/test_pricing_executions_repository.py:121:            "underlying_asset": "PETR4",
ATT/tests/test_pricing_executions_repository.py:129:            "underlying_asset": "VALE3",
ATT/tests/test_pricing_executions_repository.py:150:    assert record["underlying_asset"] == "VALE3"
ATT/tests/test_pricing_input_service.py:31:            "underlying_asset": "BOVA11",
ATT/tests/test_pricing_input_service.py:36:            "underlying_asset": "BOVA11",
ATT/tests/test_pricing_payload_adapter.py:12:                "underlying_asset": "BOVA11",
ATT/tests/test_pricing_payload_adapter.py:18:                        "symbol": "BOVAE195",
ATT/tests/test_pricing_payload_adapter.py:19:                        "strike": 195.0,
ATT/tests/test_pricing_payload_adapter.py:20:                        "expiration_date": "2026-05-15",
ATT/tests/test_pricing_payload_adapter.py:23:                        "multiplier": 1.0,
ATT/tests/test_pricing_payload_adapter.py:38:        self.assertEqual(payload["underlying_asset"], "BOVA11")
ATT/tests/test_pricing_payload_adapter.py:46:                "underlying_asset": "BOVA11",
ATT/tests/test_pricing_payload_adapter.py:51:                        "symbol": "bovaq195",
ATT/tests/test_pricing_payload_adapter.py:52:                        "strike": 195,
ATT/tests/test_pricing_payload_adapter.py:53:                        "expiration_date": "2026-05-15",
ATT/tests/test_pricing_payload_adapter.py:56:                        "multiplier": 1,
ATT/tests/test_pricing_payload_adapter.py:73:        self.assertEqual(payload["legs"][0]["symbol"], "BOVAQ195")
ATT/tests/test_pricing_payload_adapter.py:93:                        "underlying_asset": "BOVA11",
ATT/tests/test_pricing_payload_adapter.py:98:                                "symbol": "BOVAE195",
ATT/tests/test_pricing_payload_adapter.py:99:                                "strike": 195.0,
ATT/tests/test_pricing_payload_adapter.py:100:                                "expiration_date": "2026-05-15",
ATT/tests/test_pricing_payload_adapter.py:103:                                "multiplier": 1.0,
ATT/tests/test_robo_leg_mapper.py:11:        "call_put": "CALL",
ATT/tests/test_robo_leg_mapper.py:12:        "ativo": " bovae195 ",
ATT/tests/test_robo_leg_mapper.py:13:        "strike": 195.0,
ATT/tests/test_robo_leg_mapper.py:14:        "vencimento": datetime(2026, 5, 15),
ATT/tests/test_robo_leg_mapper.py:23:    assert result["symbol"] == "BOVAE195"
ATT/tests/test_robo_leg_mapper.py:24:    assert result["strike"] == 195.0
ATT/tests/test_robo_leg_mapper.py:25:    assert result["expiration_date"] == "2026-05-15"
ATT/tests/test_robo_leg_mapper.py:28:    assert result["multiplier"] == 1.0
ATT/tests/test_robo_leg_mapper.py:34:        "call_put": "PUT",
ATT/tests/test_robo_leg_mapper.py:35:        "ativo": " bovao185 ",
ATT/tests/test_robo_leg_mapper.py:36:        "strike": 185.0,
ATT/tests/test_robo_leg_mapper.py:37:        "vencimento": datetime(2026, 5, 15),
ATT/tests/test_robo_leg_mapper.py:46:    assert result["symbol"] == "BOVAO185"
ATT/tests/test_robo_leg_mapper.py:47:    assert result["expiration_date"] == "2026-05-15"
ATT/tests/test_robo_leg_mapper.py:53:        "call_put": "CALL",
ATT/tests/test_robo_leg_mapper.py:54:        "ativo": "BOVAE195",
ATT/tests/test_robo_leg_mapper.py:55:        "strike": 195.0,
ATT/tests/test_robo_leg_mapper.py:56:        "vencimento": datetime(2026, 5, 15),
ATT/tests/test_robo_leg_mapper.py:65:def test_to_canonical_leg_should_raise_for_invalid_call_put():
ATT/tests/test_robo_leg_mapper.py:68:        "call_put": "XXX",
ATT/tests/test_robo_leg_mapper.py:69:        "ativo": "BOVAE195",
ATT/tests/test_robo_leg_mapper.py:70:        "strike": 195.0,
ATT/tests/test_robo_leg_mapper.py:71:        "vencimento": datetime(2026, 5, 15),
ATT/tests/test_robo_leg_mapper.py:76:    with pytest.raises(ValueError, match=r"invalid call_put: XXX"):
ATT/tests/test_robo_leg_mapper.py:80:def test_to_canonical_leg_should_raise_for_invalid_strike():
ATT/tests/test_robo_leg_mapper.py:83:        "call_put": "CALL",
ATT/tests/test_robo_leg_mapper.py:84:        "ativo": "BOVAE195",
ATT/tests/test_robo_leg_mapper.py:85:        "strike": "abc",
ATT/tests/test_robo_leg_mapper.py:86:        "vencimento": datetime(2026, 5, 15),
ATT/tests/test_robo_leg_mapper.py:91:    with pytest.raises(ValueError, match=r"invalid strike: abc"):
ATT/tests/test_robo_leg_mapper.py:98:        "call_put": "CALL",
ATT/tests/test_robo_leg_mapper.py:99:        "ativo": "BOVAE195",
ATT/tests/test_robo_leg_mapper.py:100:        "strike": 195.0,
ATT/tests/test_robo_leg_mapper.py:101:        "vencimento": datetime(2026, 5, 15),
ATT/tests/test_robo_legs_repository.py:16:            call_put TEXT,
ATT/tests/test_robo_legs_repository.py:17:            strike REAL,
ATT/tests/test_robo_legs_repository.py:19:            ativo TEXT,
ATT/tests/test_robo_legs_repository.py:20:            vencimento TEXT,
ATT/tests/test_robo_legs_repository.py:30:            call_put TEXT,
ATT/tests/test_robo_legs_repository.py:31:            strike REAL,
ATT/tests/test_robo_legs_repository.py:33:            ativo TEXT,
ATT/tests/test_robo_legs_repository.py:34:            vencimento TEXT,
ATT/tests/test_robo_legs_repository.py:50:        (id, aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco)
ATT/tests/test_robo_legs_repository.py:55:        (id, aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco)
ATT/tests/test_robo_legs_repository.py:68:    assert legs[0].call_put == "CALL"
ATT/tests/test_robo_legs_repository.py:69:    assert legs[0].ativo == "PETR4"
ATT/tests/test_robo_legs_repository.py:80:        (id, aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco)
ATT/tests/test_robo_legs_repository.py:92:    assert legs[0].call_put == "PUT"
ATT/tests/test_robo_legs_repository.py:93:    assert legs[0].ativo == "VALE3"
ATT/tests/test_robo_legs_repository.py:104:        (id, aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco)
ATT/tests/test_robo_legs_repository.py:124:        (id, aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco)
ATT/tests/test_robo_legs_repository.py:129:        (id, aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco)
ATT/tests/test_robo_legs_repository.py:134:        (id, aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco)
ATT/tests/test_robo_legs_repository.py:154:        (id, aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco)
ATT/tests/test_robo_legs_repository.py:159:        (id, aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco)
ATT/tests/test_robo_legs_service.py:22:        call_put="CALL",
ATT/tests/test_robo_legs_service.py:23:        strike=120.0,
ATT/tests/test_robo_legs_service.py:25:        ativo="BOVA11C120",
ATT/tests/test_robo_legs_service.py:26:        vencimento=datetime(2026, 6, 20),
ATT/tests/test_robo_legs_service.py:55:        call_put="CALL",
ATT/tests/test_robo_legs_service.py:56:        strike=120.0,
ATT/tests/test_robo_legs_service.py:58:        ativo="BOVA11C120",
ATT/tests/test_robo_legs_service.py:59:        vencimento=datetime(2026, 6, 20),
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:16:    def get_snapshot(self, underlying_asset, reference_date=None):
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:19:            "underlying_asset": underlying_asset,
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:39:                "call_put": "C",
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:40:                "ativo": "bovae195",
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:41:                "strike": 195.0,
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:42:                "vencimento": "2026-05-15",
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:45:                "multiplier": 1.0,
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:55:        "underlying_asset": "BOVA11",
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:82:    assert canonical_leg["symbol"] == "BOVAE195"
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:95:    assert pricing_payload["underlying_asset"] == "BOVA11"
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:105:            "symbol": "BOVAE195",
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:106:            "strike": 195.0,
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:107:            "expiration_date": "2026-05-15",
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:110:            "multiplier": 1.0,
ATT/tests/test_rtd_option_quotes_repository_contract.py:15:                codigo_opcao TEXT,
ATT/tests/test_rtd_option_quotes_repository_contract.py:16:                ativo_base TEXT,
ATT/tests/test_rtd_option_quotes_repository_contract.py:17:                call_put TEXT,
ATT/tests/test_rtd_option_quotes_repository_contract.py:18:                strike REAL,
ATT/tests/test_rtd_option_quotes_repository_contract.py:19:                vencimento TEXT,
ATT/tests/test_rtd_option_quotes_repository_contract.py:47:                codigo_opcao,
ATT/tests/test_rtd_option_quotes_repository_contract.py:48:                ativo_base,
ATT/tests/test_rtd_option_quotes_repository_contract.py:49:                call_put,
ATT/tests/test_rtd_option_quotes_repository_contract.py:50:                strike,
ATT/tests/test_rtd_option_quotes_repository_contract.py:51:                vencimento,
ATT/tests/test_rtd_option_quotes_repository_contract.py:97:    assert quote["codigo_opcao"] == "PETRA123"
ATT/tests/test_rtd_option_quotes_repository_contract.py:98:    assert quote["ativo_base"] == "PETR4"
ATT/tests/test_rtd_option_quotes_repository_contract.py:123:                codigo_opcao,
ATT/tests/test_rtd_option_quotes_repository_contract.py:124:                ativo_base,
ATT/tests/test_rtd_option_quotes_repository_contract.py:125:                call_put,
ATT/tests/test_rtd_option_quotes_repository_contract.py:126:                strike,
ATT/tests/test_rtd_option_quotes_repository_contract.py:127:                vencimento,
ATT/tests/test_rtd_option_quotes_repository_contract.py:164:def test_list_by_ativo_base_returns_ordered_quotes_for_asset(tmp_path):
ATT/tests/test_rtd_option_quotes_repository_contract.py:178:                codigo_opcao,
ATT/tests/test_rtd_option_quotes_repository_contract.py:179:                ativo_base,
ATT/tests/test_rtd_option_quotes_repository_contract.py:180:                call_put,
ATT/tests/test_rtd_option_quotes_repository_contract.py:181:                strike,
ATT/tests/test_rtd_option_quotes_repository_contract.py:182:                vencimento,
ATT/tests/test_rtd_option_quotes_repository_contract.py:195:    quotes = repository.list_by_ativo_base("PETR4")
ATT/tests/test_rtd_option_quotes_repository_contract.py:197:    assert [quote["codigo_opcao"] for quote in quotes] == ["PETRA123", "PETRB123"]
ATT/tests/test_rtd_option_quotes_repository_contract.py:198:    assert all(quote["ativo_base"] == "PETR4" for quote in quotes)
ATT/tests/test_rtd_option_quotes_repository_contract.py:214:                codigo_opcao,
ATT/tests/test_rtd_option_quotes_repository_contract.py:215:                ativo_base,
ATT/tests/test_rtd_option_quotes_repository_contract.py:216:                call_put,
ATT/tests/test_rtd_option_quotes_repository_contract.py:217:                strike,
ATT/tests/test_rtd_option_quotes_repository_contract.py:218:                vencimento,
ATT/tests/test_rtd_option_quotes_repository_contract.py:233:    assert [quote["codigo_opcao"] for quote in quotes] == ["PETRA123", "VALEA123"]
ATT/tests/test_run_derived_pipeline_rtd_integration.py:66:        "codigo_opcao;ativo_base\nPRIOG800;PRIO3\n",
ATT/tests/test_structure_analysis_service.py:30:                "underlying_asset": "BOVA11",
ATT/tests/test_structure_analysis_service.py:36:                        "symbol": "BOVAM190",
ATT/tests/test_structure_analysis_service.py:37:                        "strike": 190.0,
ATT/tests/test_structure_analysis_service.py:38:                        "expiration_date": "2026-05-15",
ATT/tests/test_structure_analysis_service.py:41:                        "multiplier": 1.0,
ATT/tests/test_structure_analysis_service.py:46:                        "symbol": "BOVAM185",
ATT/tests/test_structure_analysis_service.py:47:                        "strike": 185.0,
ATT/tests/test_structure_analysis_service.py:48:                        "expiration_date": "2026-05-15",
ATT/tests/test_structure_analysis_service.py:51:                        "multiplier": 1.0,
ATT/tests/test_structure_analysis_service.py:57:                "underlying_asset": "BOVA11",
ATT/tests/test_structure_analysis_service.py:91:                "underlying_asset": "BOVA11",
ATT/tests/test_structure_analysis_service.py:97:                "underlying_asset": "BOVA11",
ATT/tests/test_structure_analysis_service.py:444:                "underlying_asset": "BOVA11",
ATT/tests/test_structure_analysis_service.py:450:                        "symbol": "BOVAM190",
ATT/tests/test_structure_analysis_service.py:451:                        "strike": 190.0,
ATT/tests/test_structure_analysis_service.py:452:                        "expiration_date": "2026-05-20",
ATT/tests/test_structure_analysis_service.py:461:                        "multiplier": 1.0,
ATT/tests/test_structure_analysis_service.py:466:                        "symbol": "BOVAM185",
ATT/tests/test_structure_analysis_service.py:467:                        "strike": 185.0,
ATT/tests/test_structure_analysis_service.py:468:                        "expiration_date": "2026-05-17",
ATT/tests/test_structure_analysis_service.py:477:                        "multiplier": 1.0,
ATT/tests/test_structure_analysis_service.py:483:                "underlying_asset": "BOVA11",
ATT/tests/test_structure_editor_dialog.py:88:        r = self._dialog([{"strike": 100.0}])._build_legs_payload()
ATT/tests/test_structure_editor_dialog.py:92:        legs = [{"strike": 100.0}, {"strike": 110.0}, {"strike": 90.0}]
ATT/tests/test_structure_editor_dialog.py:98:            "position_side": "VENDIDO", "option_type": "CALL", "strike": 195.0,
ATT/tests/test_structure_editor_dialog.py:99:            "expiration_date": "2026-05-15", "quantity": 5000,
ATT/tests/test_structure_editor_dialog.py:100:            "premium": None, "multiplier": 1,
ATT/tests/test_structure_editor_dialog.py:104:        self.assertEqual(r["strike"], 195.0)
ATT/tests/test_structure_editor_dialog.py:108:        legs = [{"strike": 100.0}]
ATT/tests/test_structure_editor_dialog.py:114:        legs = [{"strike": 100.0}, {"strike": 110.0}]
ATT/tests/test_structure_editor_dialog.py:118:        self.assertEqual(r[0]["strike"], 100.0)
ATT/tests/test_structure_editor_dialog.py:119:        self.assertEqual(r[1]["strike"], 110.0)
ATT/tests/test_structure_editor_dialog.py:153:            "id": 1, "name": "BOVA11 Condor", "underlying_asset": "BOVA11",
ATT/tests/test_structure_editor_dialog.py:159:        self.assertEqual(dlg._f_underlying.get(), "BOVA11")
ATT/tests/test_structure_editor_dialog.py:166:            "position_side": "COMPRADO", "option_type": "CALL", "strike": 195.0,
ATT/tests/test_structure_editor_dialog.py:167:            "expiration_date": "2026-05-15", "quantity": 5000,
ATT/tests/test_structure_editor_dialog.py:168:            "premium": None, "multiplier": 1,
ATT/tests/test_structure_editor_dialog.py:171:            "id": 1, "name": "X", "underlying_asset": "X",
ATT/tests/test_structure_editor_dialog.py:177:        self.assertEqual(dlg._legs_rows[0]["strike"], 195.0)
ATT/tests/test_structure_editor_dialog.py:225:        dlg._f_underlying.set("PRIO3")
ATT/tests/test_structure_editor_dialog.py:238:        self.assertEqual(structure_arg["underlying_asset"], "PRIO3")
ATT/tests/test_structure_editor_dialog.py:247:        dlg._f_underlying.set("Y")
ATT/tests/test_structure_editor_dialog.py:250:            "position_side": "COMPRADO", "option_type": "CALL", "strike": 100.0,
ATT/tests/test_structure_editor_dialog.py:251:            "expiration_date": "2026-05-15", "quantity": 1000,
ATT/tests/test_structure_editor_dialog.py:252:            "premium": None, "multiplier": 1, "symbol": None,
ATT/tests/test_structure_editor_dialog.py:264:        self.assertEqual(structure_arg["underlying_asset"], "Y")
ATT/tests/test_structure_editor_dialog.py:268:        self.assertEqual(legs_arg[0]["strike"], 100.0)
ATT/tests/test_structure_editor_dialog.py:273:        dlg._f_underlying.set("Y")
ATT/tests/test_structure_editor_dialog.py:282:        dlg._f_underlying.set("BOVA11")
ATT/tests/test_structure_editor_dialog.py:288:    def test_underlying_vazio_nao_chama_create(self):
ATT/tests/test_structure_editor_dialog.py:291:        dlg._f_underlying.set("")
ATT/tests/test_structure_editor_dialog.py:322:            "id": structure_id, "name": "Original", "underlying_asset": "ORIG",
ATT/tests/test_structure_editor_dialog.py:336:        dlg._f_underlying.set("BOVA11")
ATT/tests/test_structure_editor_dialog.py:348:        dlg._f_underlying.set("Y")
ATT/tests/test_structure_editor_dialog.py:358:        dlg._f_underlying.set("Y")
ATT/tests/test_structure_editor_dialog.py:442:            "strike": 100.0,
ATT/tests/test_structure_editor_dialog.py:443:            "expiration_date": "2026-12-18",
ATT/tests/test_structure_editor_dialog.py:446:            "multiplier": 1,
ATT/tests/test_structure_editor_dialog.py:447:            "symbol": "TESTC100",
ATT/tests/test_structure_editor_dialog.py:453:            "strike": 90.0,
ATT/tests/test_structure_editor_dialog.py:454:            "expiration_date": "2026-12-18",
ATT/tests/test_structure_editor_dialog.py:457:            "multiplier": 1,
ATT/tests/test_structure_editor_dialog.py:458:            "symbol": "TESTP90",
ATT/tests/test_structure_editor_dialog.py:470:def test_build_legs_payload_normaliza_strike_com_virgula_para_float():
ATT/tests/test_structure_editor_dialog.py:476:            "strike": "100,00",
ATT/tests/test_structure_editor_dialog.py:477:            "expiration_date": "2026-12-18",
ATT/tests/test_structure_editor_dialog.py:480:            "multiplier": 1,
ATT/tests/test_structure_editor_dialog.py:481:            "symbol": "TESTC100",
ATT/tests/test_structure_editor_dialog.py:488:    assert payload[0]["strike"] == 100.0
ATT/tests/test_structure_editor_dialog.py:489:    assert isinstance(payload[0]["strike"], float)
ATT/tests/test_structure_editor_dialog.py:492:def test_build_legs_payload_normaliza_strike_com_ponto_para_float():
ATT/tests/test_structure_editor_dialog.py:498:            "strike": "100.50",
ATT/tests/test_structure_editor_dialog.py:499:            "expiration_date": "2026-12-18",
ATT/tests/test_structure_editor_dialog.py:502:            "multiplier": 1,
ATT/tests/test_structure_editor_dialog.py:503:            "symbol": "TESTC100",
ATT/tests/test_structure_editor_dialog.py:510:    assert payload[0]["strike"] == 100.50
ATT/tests/test_structure_editor_dialog.py:511:    assert isinstance(payload[0]["strike"], float)
ATT/tests/test_structure_editor_dialog.py:514:def test_build_legs_payload_nao_modifica_strike_original_ao_normalizar():
ATT/tests/test_structure_editor_dialog.py:519:        "strike": "100,00",
ATT/tests/test_structure_editor_dialog.py:520:        "expiration_date": "2026-12-18",
ATT/tests/test_structure_editor_dialog.py:523:        "multiplier": 1,
ATT/tests/test_structure_editor_dialog.py:524:        "symbol": "TESTC100",
ATT/tests/test_structure_editor_dialog.py:531:    assert payload[0]["strike"] == 100.0
ATT/tests/test_structure_editor_dialog.py:532:    assert original_leg["strike"] == "100,00"
ATT/tests/test_structure_editor_dialog.py:542:            "strike": "100,00",
ATT/tests/test_structure_editor_dialog.py:543:            "expiration_date": "2026-12-18",
ATT/tests/test_structure_editor_dialog.py:546:            "multiplier": 1,
ATT/tests/test_structure_editor_dialog.py:547:            "symbol": "TESTC100",
ATT/tests/test_structure_editor_dialog.py:558:def test_build_legs_payload_normaliza_multiplier_com_virgula_para_float():
ATT/tests/test_structure_editor_dialog.py:564:            "strike": "100,00",
ATT/tests/test_structure_editor_dialog.py:565:            "expiration_date": "2026-12-18",
ATT/tests/test_structure_editor_dialog.py:568:            "multiplier": "100,0",
ATT/tests/test_structure_editor_dialog.py:569:            "symbol": "TESTC100",
ATT/tests/test_structure_editor_dialog.py:576:    assert payload[0]["multiplier"] == 100.0
ATT/tests/test_structure_editor_dialog.py:577:    assert isinstance(payload[0]["multiplier"], float)
ATT/tests/test_structure_editor_dialog.py:586:            "strike": "100,00",
ATT/tests/test_structure_editor_dialog.py:587:            "expiration_date": "2026-12-18",
ATT/tests/test_structure_editor_dialog.py:590:            "multiplier": 1,
ATT/tests/test_structure_editor_dialog.py:591:            "symbol": "TESTC100",
ATT/tests/test_structure_editor_dialog.py:611:            "strike": "100,00",
ATT/tests/test_structure_editor_dialog.py:612:            "expiration_date": "2026-12-18",
ATT/tests/test_structure_editor_dialog.py:615:            "multiplier": 1,
ATT/tests/test_structure_editor_dialog.py:616:            "symbol": "TESTC100",
ATT/tests/test_structure_editor_integration.py:293:    dlg._f_underlying = _FakeVar()
ATT/tests/test_structure_editor_integration.py:364:             "strike": "10.00", "expiration_date": "2025-01-17",
ATT/tests/test_structure_editor_integration.py:365:             "quantity": 1, "premium": None, "multiplier": 1.0,
ATT/tests/test_structure_editor_integration.py:366:             "leg_order": 99, "symbol": None, "notes": None},
ATT/tests/test_structure_editor_integration.py:439:    def _dlg(self, structure_id=None, name="Iron Fly", underlying="BBAS3"):
ATT/tests/test_structure_editor_integration.py:442:        dlg._f_underlying.set(underlying)
ATT/tests/test_structure_editor_integration.py:504:    def test_saved_false_se_underlying_vazio(self):
ATT/tests/test_structure_editor_integration.py:505:        dlg = self._dlg(underlying="")
ATT/tests/test_structure_editor_integration.py:523:        dlg._f_underlying.set("WEGE3")
ATT/tests/test_structure_editor_integration.py:529:             "strike": "25.00", "expiration_date": "2025-03-21",
ATT/tests/test_structure_editor_integration.py:530:             "quantity": 1, "premium": None, "multiplier": 1.0,
ATT/tests/test_structure_editor_integration.py:531:             "leg_order": 1, "symbol": None, "notes": None},
ATT/tests/test_structure_editor_integration.py:533:             "strike": "27.00", "expiration_date": "2025-03-21",
ATT/tests/test_structure_editor_integration.py:534:             "quantity": 1, "premium": None, "multiplier": 1.0,
ATT/tests/test_structure_editor_integration.py:535:             "leg_order": 2, "symbol": None, "notes": None},
ATT/tests/test_structure_events_api.py:13:    "underlying_asset": "PETR4",
ATT/tests/test_structure_events_api.py:31:    "symbol": "PETR4",
ATT/tests/test_structure_events_api.py:64:    "symbol": "PETR4",
ATT/tests/test_structure_events_effective_state.py:23:        "underlying_asset": "BOVA11",
ATT/tests/test_structure_events_effective_state.py:30:                "symbol": "BOVAM190",
ATT/tests/test_structure_events_effective_state.py:31:                "strike": 190.0,
ATT/tests/test_structure_events_effective_state.py:32:                "expiration_date": "2026-05-15",
ATT/tests/test_structure_events_effective_state.py:35:                "multiplier": 1.0,
ATT/tests/test_structure_events_effective_state.py:41:                "symbol": "BOVAM185",
ATT/tests/test_structure_events_effective_state.py:42:                "strike": 185.0,
ATT/tests/test_structure_events_effective_state.py:43:                "expiration_date": "2026-05-15",
ATT/tests/test_structure_events_effective_state.py:46:                "multiplier": 1.0,
ATT/tests/test_structure_events_repository.py:30:        "underlying_asset": "bova11",
ATT/tests/test_structure_events_repository.py:41:        "symbol": "BOVA11C120",
ATT/tests/test_structure_events_repository.py:42:        "strike": 120.0,
ATT/tests/test_structure_events_repository.py:43:        "expiration_date": "2026-06-20",
ATT/tests/test_structure_events_repository.py:46:        "multiplier": 100,
ATT/tests/test_structure_events_repository.py:71:            "symbol": "BOVA11C120",
ATT/tests/test_structure_events_repository.py:91:    assert event["symbol"] == "BOVA11C120"
ATT/tests/test_structure_events_repository.py:233:                "exit_symbol": "BOVA11C120",
ATT/tests/test_structure_events_repository.py:234:                "entry_symbol": "BOVA11C125",
ATT/tests/test_structure_events_repository.py:269:            "underlying_asset": "PETR4",
ATT/tests/test_structure_events_repository.py:275:        valid_leg_payload(symbol="PETR4C40", strike=40.0),
ATT/tests/test_structure_events_service.py:96:        symbol="  PETRA100  ",
ATT/tests/test_structure_events_service.py:110:    assert record["symbol"] == "PETRA100"
ATT/tests/test_structure_events_service.py:141:        symbol="PETRA100",
ATT/tests/test_structure_events_service.py:153:    assert record["symbol"] == "PETRA100"
ATT/tests/test_structure_input_mapper.py:8:        "underlying_asset": " bova11 ",
ATT/tests/test_structure_input_mapper.py:14:                "symbol": " bovae195 ",
ATT/tests/test_structure_input_mapper.py:15:                "strike": 195.0,
ATT/tests/test_structure_input_mapper.py:16:                "expiration_date": " 2026-05-15 ",
ATT/tests/test_structure_input_mapper.py:19:                "multiplier": 1.0,
ATT/tests/test_structure_input_mapper.py:28:    assert result["underlying_asset"] == "BOVA11"
ATT/tests/test_structure_input_mapper.py:33:    assert result["legs"][0]["symbol"] == "BOVAE195"
ATT/tests/test_structure_leg_rtd_enrichment_service.py:13:    def get_by_codigo(self, codigo_opcao):
ATT/tests/test_structure_leg_rtd_enrichment_service.py:14:        self.requested_codigo = codigo_opcao
ATT/tests/test_structure_leg_rtd_enrichment_service.py:15:        return self.rows.get(codigo_opcao)
ATT/tests/test_structure_leg_rtd_enrichment_service.py:18:def test_enrich_leg_from_symbol_uses_rtd_quote_and_returns_canonical_leg():
ATT/tests/test_structure_leg_rtd_enrichment_service.py:22:                "codigo_opcao": "BOVA11C130",
ATT/tests/test_structure_leg_rtd_enrichment_service.py:23:                "ativo_base": "BOVA11",
ATT/tests/test_structure_leg_rtd_enrichment_service.py:24:                "call_put": "CALL",
ATT/tests/test_structure_leg_rtd_enrichment_service.py:25:                "strike": 130.0,
ATT/tests/test_structure_leg_rtd_enrichment_service.py:26:                "vencimento": "2026-07-17",
ATT/tests/test_structure_leg_rtd_enrichment_service.py:34:            "symbol": " bova11c130 ",
ATT/tests/test_structure_leg_rtd_enrichment_service.py:39:            "notes": "entrada via simbolo",
ATT/tests/test_structure_leg_rtd_enrichment_service.py:45:        "symbol": "BOVA11C130",
ATT/tests/test_structure_leg_rtd_enrichment_service.py:48:        "strike": 130.0,
ATT/tests/test_structure_leg_rtd_enrichment_service.py:49:        "expiration_date": "2026-07-17",
ATT/tests/test_structure_leg_rtd_enrichment_service.py:52:        "multiplier": 100.0,
ATT/tests/test_structure_leg_rtd_enrichment_service.py:54:        "notes": "entrada via simbolo",
ATT/tests/test_structure_leg_rtd_enrichment_service.py:55:        "underlying_asset": "BOVA11",
ATT/tests/test_structure_leg_rtd_enrichment_service.py:59:def test_enrich_leg_accepts_codigo_opcao_as_symbol_alias():
ATT/tests/test_structure_leg_rtd_enrichment_service.py:63:                "codigo_opcao": "PETR4P2800",
ATT/tests/test_structure_leg_rtd_enrichment_service.py:64:                "ativo_base": "PETR4",
ATT/tests/test_structure_leg_rtd_enrichment_service.py:65:                "call_put": "PUT",
ATT/tests/test_structure_leg_rtd_enrichment_service.py:66:                "strike": 28.0,
ATT/tests/test_structure_leg_rtd_enrichment_service.py:67:                "vencimento": "2026-08-21",
ATT/tests/test_structure_leg_rtd_enrichment_service.py:75:            "codigo_opcao": "PETR4P2800",
ATT/tests/test_structure_leg_rtd_enrichment_service.py:81:    assert leg["symbol"] == "PETR4P2800"
ATT/tests/test_structure_leg_rtd_enrichment_service.py:84:    assert leg["strike"] == 28.0
ATT/tests/test_structure_leg_rtd_enrichment_service.py:85:    assert leg["expiration_date"] == "2026-08-21"
ATT/tests/test_structure_leg_rtd_enrichment_service.py:88:    assert leg["multiplier"] == 100.0
ATT/tests/test_structure_leg_rtd_enrichment_service.py:91:    assert leg["underlying_asset"] == "PETR4"
ATT/tests/test_structure_leg_rtd_enrichment_service.py:94:def test_enrich_leg_raises_value_error_when_symbol_is_missing():
ATT/tests/test_structure_leg_rtd_enrichment_service.py:99:    with pytest.raises(ValueError, match="symbol is required"):
ATT/tests/test_structure_leg_rtd_enrichment_service.py:116:                "symbol": "BOVA11C999",
ATT/tests/test_structure_leg_rtd_enrichment_service.py:128:                    "codigo_opcao": "BOVA11C130",
ATT/tests/test_structure_leg_rtd_enrichment_service.py:129:                    "ativo_base": "BOVA11",
ATT/tests/test_structure_leg_rtd_enrichment_service.py:130:                    "call_put": "CALL",
ATT/tests/test_structure_leg_rtd_enrichment_service.py:131:                    "strike": 130.0,
ATT/tests/test_structure_leg_rtd_enrichment_service.py:140:                "symbol": "BOVA11C130",
ATT/tests/test_structure_market_input_assembler.py:11:            "underlying_asset": "BOVA11",
ATT/tests/test_structure_market_input_assembler.py:17:                    "symbol": "BOVAE195",
ATT/tests/test_structure_market_input_assembler.py:18:                    "strike": 195.0,
ATT/tests/test_structure_market_input_assembler.py:19:                    "expiration_date": "2026-05-15",
ATT/tests/test_structure_market_input_assembler.py:22:                    "multiplier": 1.0,
ATT/tests/test_structure_market_input_assembler.py:29:            "underlying_asset": "BOVA11",
ATT/tests/test_structure_market_input_assembler.py:41:        self.assertEqual(result["structure"]["underlying_asset"], "BOVA11")
ATT/tests/test_structure_market_input_assembler.py:42:        self.assertEqual(result["market"]["underlying_asset"], "BOVA11")
ATT/tests/test_structure_market_input_assembler.py:46:    def test_should_raise_when_underlying_asset_mismatches(self):
ATT/tests/test_structure_market_input_assembler.py:50:            "underlying_asset": "BOVA11",
ATT/tests/test_structure_market_input_assembler.py:56:            "underlying_asset": "PETR4",
ATT/tests/test_structure_market_input_assembler.py:65:        self.assertIn("underlying_asset mismatch", str(ctx.exception))
ATT/tests/test_structure_market_input_assembler.py:70:            "underlying_asset": "BOVA11",
ATT/tests/test_structure_market_input_assembler.py:85:            "underlying_asset": "BOVA11",
ATT/tests/test_structure_metrics.py:38:            "underlying_asset": "BOVA11",
ATT/tests/test_structure_metrics.py:43:                    "strike": 190.0,
ATT/tests/test_structure_metrics.py:44:                    "expiration_date": "2026-05-20",
ATT/tests/test_structure_metrics.py:50:                    "strike": 185.0,
ATT/tests/test_structure_metrics.py:51:                    "expiration_date": "2026-05-17",
ATT/tests/test_structure_metrics.py:137:        "vencimento": "2026-05-20",
ATT/tests/test_structure_metrics.py:167:        "vencimento": "2026-05-17",
ATT/tests/test_structure_metrics.py:198:            "vencimento": "2026-05-20",
ATT/tests/test_structure_metrics.py:210:            "vencimento": "2026-05-17",
ATT/tests/test_structure_metrics.py:232:            "underlying_asset": "BOVA11",
ATT/tests/test_structure_metrics.py:241:                    "expiration_date": "2026-05-20",
ATT/tests/test_structure_metrics.py:250:                    "expiration_date": "2026-05-17",
ATT/tests/test_structures_api.py:12:  - TestUpdateStructure  : underlying_asset; alias; merge parcial; value_error -> 400
ATT/tests/test_structures_api.py:32:    "underlying_asset": "PETR4",
ATT/tests/test_structures_api.py:44:            "symbol": "PETRJ240",
ATT/tests/test_structures_api.py:45:            "strike": 38.0,
ATT/tests/test_structures_api.py:46:            "expiration_date": "2026-07-18",
ATT/tests/test_structures_api.py:49:            "multiplier": 100.0,
ATT/tests/test_structures_api.py:67:    "strike":          38.0,
ATT/tests/test_structures_api.py:68:    "expiration_date": "2026-07-18",
ATT/tests/test_structures_api.py:70:    "multiplier":      100.0,
ATT/tests/test_structures_api.py:72:    "symbol":          "PETRJ240",
ATT/tests/test_structures_api.py:135:            "underlying_asset": "PETR4",
ATT/tests/test_structures_api.py:145:            "underlying_asset": "VALE3",
ATT/tests/test_structures_api.py:155:            "underlying_asset": "BBAS3",
ATT/tests/test_structures_api.py:166:            "underlying_asset": "PETR4",
ATT/tests/test_structures_api.py:178:            "underlying_asset": "Y",
ATT/tests/test_structures_api.py:186:            "underlying_asset": "PETR4",
ATT/tests/test_structures_api.py:190:        assert payload["underlying_asset"] == "PETR4"
ATT/tests/test_structures_api.py:197:            "underlying_asset": "Y",
ATT/tests/test_structures_api.py:204:        repo.create_structure.side_effect = ValueError("underlying_asset inválido")
ATT/tests/test_structures_api.py:207:            "underlying_asset": "???",
ATT/tests/test_structures_api.py:209:        assert "underlying_asset inválido" in resp.json()["detail"]
ATT/tests/test_structures_api.py:211:    def test_422_sem_campo_obrigatorio_underlying_asset(self, client):
ATT/tests/test_structures_api.py:213:        resp = tc.post("/structures", json={"name": "Sem ativo"})
ATT/tests/test_structures_api.py:218:        resp = tc.post("/structures", json={"underlying_asset": "PETR4"})
ATT/tests/test_structures_api.py:226:            "underlying_asset": "PETR4",
ATT/tests/test_structures_api.py:230:    def test_422_underlying_asset_vazio(self, client):
ATT/tests/test_structures_api.py:234:            "underlying_asset": "",
ATT/tests/test_structures_api.py:270:        for campo in ("id", "name", "underlying_asset", "status", "created_at", "updated_at"):
ATT/tests/test_structures_api.py:340:        for campo in ("id", "name", "underlying_asset", "status", "legs", "created_at", "updated_at"):
ATT/tests/test_structures_api.py:376:        for campo in ("id", "structure_id", "position_side", "option_type", "strike",
ATT/tests/test_structures_api.py:377:                      "expiration_date", "quantity", "multiplier", "leg_order"):
ATT/tests/test_structures_api.py:417:    def test_atualiza_underlying_asset(self, client):
ATT/tests/test_structures_api.py:419:        tc.patch("/structures/1", json={"underlying_asset": "VALE3"})
ATT/tests/test_structures_api.py:421:        assert args[1]["underlying_asset"] == "VALE3"
ATT/tests/test_structures_api.py:448:        assert "underlying_asset" not in payload
ATT/tests/test_structures_api.py:561:            "underlying_asset": "PETR4",
ATT/tests/test_structures_api.py:565:    def test_list_response_underlying_asset_em_maiusculas(self, client):
ATT/tests/test_structures_api.py:566:        """underlying_asset deve ser armazenado em uppercase (normalização do repo)."""
ATT/tests/test_structures_api.py:569:        assert resp.json()[0]["underlying_asset"] == "PETR4"
ATT/tests/test_structures_api.py:586:    def test_detail_leg_strike_e_float(self, client):
ATT/tests/test_structures_api.py:590:        assert isinstance(leg["strike"], float)
ATT/tests/test_structures_archive_wiring.py:537:                "(id INTEGER PRIMARY KEY, name TEXT, underlying_asset TEXT, "
ATT/tests/test_structures_archive_wiring.py:544:                " position_side TEXT, option_type TEXT, symbol TEXT, "
ATT/tests/test_structures_archive_wiring.py:545:                " strike REAL, expiration_date TEXT, quantity INTEGER, "
ATT/tests/test_structures_archive_wiring.py:546:                " premium REAL, multiplier REAL DEFAULT 1, leg_order INTEGER, "
ATT/tests/test_structures_archive_wiring.py:574:                "(id INTEGER PRIMARY KEY, name TEXT, underlying_asset TEXT, "
ATT/tests/test_structures_legs_endpoints.py:27:    "strike":          38.0,
ATT/tests/test_structures_legs_endpoints.py:28:    "expiration_date": "2026-07-18",
ATT/tests/test_structures_legs_endpoints.py:30:    "multiplier":      100.0,
ATT/tests/test_structures_legs_endpoints.py:32:    "symbol":          "PETRJ240",
ATT/tests/test_structures_legs_endpoints.py:44:    "underlying_asset":  "PETR4",
ATT/tests/test_structures_legs_endpoints.py:109:        assert args[1]["strike"] == 38.0
ATT/tests/test_structures_legs_endpoints.py:137:    def test_add_leg_422_strike_zero(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:139:        payload = {**FAKE_LEG_PAYLOAD, "strike": 0}
ATT/tests/test_structures_legs_endpoints.py:156:    def test_add_leg_422_leg_order_negativo(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:196:        assert leg["strike"] == 38.0
ATT/tests/test_structures_repository.py:17:        "underlying_asset": "bova11",
ATT/tests/test_structures_repository.py:28:        "symbol": "BOVA11C120",
ATT/tests/test_structures_repository.py:29:        "strike": 120.0,
ATT/tests/test_structures_repository.py:30:        "expiration_date": "2026-06-20",
ATT/tests/test_structures_repository.py:33:        "multiplier": 100,
ATT/tests/test_structures_repository.py:41:def test_create_structure_normalizes_underlying_asset(repo):
ATT/tests/test_structures_repository.py:48:    assert structure["underlying_asset"] == "BOVA11"
ATT/tests/test_structures_repository.py:61:def test_create_structure_raises_when_underlying_asset_missing(repo):
ATT/tests/test_structures_repository.py:63:    payload["underlying_asset"] = "   "
ATT/tests/test_structures_repository.py:65:    with pytest.raises(ValueError, match="underlying_asset is required"):
ATT/tests/test_structures_repository.py:82:            "underlying_asset": "PETR4",
ATT/tests/test_structures_repository.py:98:            "underlying_asset": "PETR4",
ATT/tests/test_structures_repository.py:113:    repo.add_leg(structure_id, valid_leg_payload(leg_order=2, symbol="BOVA11C130", strike=130.0))
ATT/tests/test_structures_repository.py:119:            symbol="BOVA11P110",
ATT/tests/test_structures_repository.py:120:            strike=110.0,
ATT/tests/test_structures_repository.py:128:    assert [leg["symbol"] for leg in structure["legs"]] == ["BOVA11P110", "BOVA11C130"]
ATT/tests/test_structures_repository.py:145:    assert structure["underlying_asset"] == "BOVA11"
ATT/tests/test_structures_repository.py:187:        ("strike", "abc", "strike must be numeric"),
ATT/tests/test_structures_repository.py:190:        ("multiplier", "abc", "multiplier must be numeric"),
ATT/tests/test_structures_repository.py:191:        ("multiplier", 0, "multiplier must be > 0"),
ATT/tests/test_structures_repository.py:193:        ("expiration_date", "20-06-2026", "expiration_date must be a valid date in YYYY-MM-DD format"),
ATT/tests/test_structures_repository.py:212:    repo.add_leg(structure_id, valid_leg_payload(leg_order=1, symbol="BOVA11C120", strike=120))
ATT/tests/test_structures_repository.py:213:    repo.add_leg(structure_id, valid_leg_payload(leg_order=2, symbol="BOVA11P110", strike=110, option_type="PUT"))
ATT/tests/test_structures_repository.py:222:                symbol="BOVA11P100",
ATT/tests/test_structures_repository.py:223:                strike=100,
ATT/tests/test_structures_repository.py:231:    assert structure["legs"][0]["symbol"] == "BOVA11P100"
ATT/tests/test_system_snapshots_repository.py:17:            underlying_asset,
ATT/tests/test_system_snapshots_repository.py:44:    symbol: str,
ATT/tests/test_system_snapshots_repository.py:45:    strike: float,
ATT/tests/test_system_snapshots_repository.py:53:            symbol,
ATT/tests/test_system_snapshots_repository.py:54:            strike,
ATT/tests/test_system_snapshots_repository.py:55:            expiration_date,
ATT/tests/test_system_snapshots_repository.py:58:            multiplier,
ATT/tests/test_system_snapshots_repository.py:70:            symbol,
ATT/tests/test_system_snapshots_repository.py:71:            strike,
ATT/tests/test_system_snapshots_repository.py:95:            symbol="PETRA10",
ATT/tests/test_system_snapshots_repository.py:96:            strike=10.0,
ATT/tests/test_system_snapshots_repository.py:102:            symbol="PETRA12",
ATT/tests/test_system_snapshots_repository.py:103:            strike=12.0,
ATT/tests/test_system_snapshots_repository.py:110:        underlying_asset="PETR4",
ATT/tests/test_system_snapshots_repository.py:116:            "underlying_asset": "PETR4",
ATT/tests/test_system_snapshots_repository.py:130:                "symbol": "PETRA10",
ATT/tests/test_system_snapshots_repository.py:131:                "strike": 10.0,
ATT/tests/test_system_snapshots_repository.py:132:                "expiration_date": "2026-12-18",
ATT/tests/test_system_snapshots_repository.py:135:                "multiplier": 1,
ATT/tests/test_system_snapshots_repository.py:144:                "symbol": "PETRA12",
ATT/tests/test_system_snapshots_repository.py:145:                "strike": 12.0,
ATT/tests/test_system_snapshots_repository.py:146:                "expiration_date": "2026-12-18",
ATT/tests/test_system_snapshots_repository.py:149:                "multiplier": 1,
ATT/tests/test_system_snapshots_repository.py:161:    assert snapshot["underlying_asset"] == "PETR4"
ATT/tests/test_system_snapshots_repository.py:174:    assert snapshot["legs"][0]["symbol"] == "PETRA10"
ATT/tests/test_system_snapshots_repository.py:177:    assert snapshot["legs"][1]["symbol"] == "PETRA12"
ATT/tests/test_system_snapshots_repository.py:232:                "symbol": "PETRM30",
ATT/tests/test_system_snapshots_repository.py:233:                "strike": 30.0,
ATT/tests/test_system_snapshots_repository.py:234:                "expiration_date": "2026-12-18",
ATT/tests/test_system_snapshots_repository.py:237:                "multiplier": 1,
ATT/tests/test_system_snapshots_repository.py:248:    assert latest["legs"][0]["symbol"] == "PETRM30"
ATT/tests/test_system_snapshots_schema.py:62:        "underlying_asset",
ATT/tests/test_system_snapshots_schema.py:104:        "symbol",
ATT/tests/test_system_snapshots_schema.py:105:        "strike",
ATT/tests/test_system_snapshots_schema.py:106:        "expiration_date",
ATT/tests/test_system_snapshots_schema.py:109:        "multiplier",
UI/components/details_panel.py:646:        # alteracao_36: structure_id é autoritativo; aba removido
UI/components/filters_panel.py:132:            text=f"Filtros aplicados ({len(filters)} ativos)",
UI/components/payoff_chart.py:450:            p, ["point_spot", "spot", "x", "underlying", "price", "underlying_spot"]
UI/components/structure_editor_dialog.py:18:    _f_underlying   tk.StringVar
UI/components/structure_editor_dialog.py:93:        self._f_underlying = tk.StringVar()
UI/components/structure_editor_dialog.py:123:            ("Ativo *",        self._f_underlying, "entry", None),
UI/components/structure_editor_dialog.py:160:        leg_cols   = ("order", "side", "type", "strike", "expiry", "qty", "premium", "mult", "symbol")
UI/components/structure_editor_dialog.py:161:        leg_hdrs   = ["#", "Lado", "Tipo", "Strike", "Vencimento", "Qtde", "Premio", "Mult", "Simbolo"]
UI/components/structure_editor_dialog.py:198:        self._lf_strike  = tk.StringVar()
UI/components/structure_editor_dialog.py:203:        self._lf_symbol  = tk.StringVar()
UI/components/structure_editor_dialog.py:219:            ("Strike",              self._lf_strike),
UI/components/structure_editor_dialog.py:232:            ("Simbolo", self._lf_symbol),
UI/components/structure_editor_dialog.py:243:            text="Auto preencher por simbolo",
UI/components/structure_editor_dialog.py:274:        self._f_underlying.set(data.get("underlying_asset", ""))
UI/components/structure_editor_dialog.py:293:                leg.get("strike", ""),
UI/components/structure_editor_dialog.py:294:                leg.get("expiration_date", ""),
UI/components/structure_editor_dialog.py:297:                leg.get("multiplier", 1),
UI/components/structure_editor_dialog.py:298:                leg.get("symbol") or "",
UI/components/structure_editor_dialog.py:322:        self._lf_strike.set(str(leg.get("strike", "")))
UI/components/structure_editor_dialog.py:323:        self._lf_expiry.set(str(leg.get("expiration_date", "")))
UI/components/structure_editor_dialog.py:326:        self._lf_mult.set(str(leg.get("multiplier", 1)))
UI/components/structure_editor_dialog.py:327:        self._lf_symbol.set(str(leg.get("symbol") or ""))
UI/components/structure_editor_dialog.py:334:            "strike":          "",
UI/components/structure_editor_dialog.py:335:            "expiration_date": "",
UI/components/structure_editor_dialog.py:338:            "multiplier":      1.0,
UI/components/structure_editor_dialog.py:340:            "symbol":          None,
UI/components/structure_editor_dialog.py:385:        """Cria/lê o service de enriquecimento por símbolo sob demanda."""
UI/components/structure_editor_dialog.py:398:            for key in ("option_type", "strike", "expiration_date")
UI/components/structure_editor_dialog.py:401:    def _enrich_leg_data_from_symbol(
UI/components/structure_editor_dialog.py:407:        """Enriquece uma leg por symbol/codigo_opcao quando informado.
UI/components/structure_editor_dialog.py:410:            usado no botao/aplicar leg; symbol invalido bloqueia.
UI/components/structure_editor_dialog.py:416:        symbol = str(leg_data.get("symbol") or leg_data.get("codigo_opcao") or "").strip()
UI/components/structure_editor_dialog.py:417:        if not symbol:
UI/components/structure_editor_dialog.py:431:    def _sync_underlying_from_enriched_leg(self, enriched: dict) -> None:
UI/components/structure_editor_dialog.py:432:        """Preenche/valida o ativo objeto da estrutura a partir da opção."""
UI/components/structure_editor_dialog.py:433:        underlying = str(enriched.get("underlying_asset") or "").strip().upper()
UI/components/structure_editor_dialog.py:434:        if not underlying:
UI/components/structure_editor_dialog.py:437:        current = self._f_underlying.get().strip().upper()
UI/components/structure_editor_dialog.py:438:        if current and current != underlying:
UI/components/structure_editor_dialog.py:440:                "Ativo objeto divergente do símbolo informado: "
UI/components/structure_editor_dialog.py:441:                f"estrutura={current}, detectado={underlying}, "
UI/components/structure_editor_dialog.py:442:                f"symbol={enriched.get('symbol')}"
UI/components/structure_editor_dialog.py:446:            self._f_underlying.set(underlying)
UI/components/structure_editor_dialog.py:452:            "strike":          self._lf_strike.get(),
UI/components/structure_editor_dialog.py:453:            "expiration_date": self._lf_expiry.get(),
UI/components/structure_editor_dialog.py:456:            "multiplier":      self._lf_mult.get() or 1,
UI/components/structure_editor_dialog.py:458:            "symbol":          self._lf_symbol.get() or None,
UI/components/structure_editor_dialog.py:466:        if enriched.get("strike") is not None:
UI/components/structure_editor_dialog.py:467:            self._lf_strike.set(str(enriched["strike"]))
UI/components/structure_editor_dialog.py:468:        if enriched.get("expiration_date"):
UI/components/structure_editor_dialog.py:469:            self._lf_expiry.set(str(enriched["expiration_date"]))
UI/components/structure_editor_dialog.py:470:        if enriched.get("multiplier") is not None:
UI/components/structure_editor_dialog.py:471:            self._lf_mult.set(str(enriched["multiplier"]))
UI/components/structure_editor_dialog.py:472:        if enriched.get("symbol"):
UI/components/structure_editor_dialog.py:473:            self._lf_symbol.set(str(enriched["symbol"]).upper())
UI/components/structure_editor_dialog.py:476:        """Botao: auto preenche leg usando symbol/codigo_opcao."""
UI/components/structure_editor_dialog.py:488:            enriched = self._enrich_leg_data_from_symbol(
UI/components/structure_editor_dialog.py:492:            self._sync_underlying_from_enriched_leg(enriched)
UI/components/structure_editor_dialog.py:511:            # Fase 3: se houver simbolo, tenta reconhecer a opcao e preencher
UI/components/structure_editor_dialog.py:512:            # ativo, tipo, strike, vencimento e multiplicador.
UI/components/structure_editor_dialog.py:513:            if leg_data.get("symbol"):
UI/components/structure_editor_dialog.py:514:                leg_data = self._enrich_leg_data_from_symbol(
UI/components/structure_editor_dialog.py:518:                self._sync_underlying_from_enriched_leg(leg_data)
UI/components/structure_editor_dialog.py:539:        - Aceita decimal pt-BR com vírgula em strike, premium e multiplier.
UI/components/structure_editor_dialog.py:591:                row = self._enrich_leg_data_from_symbol(
UI/components/structure_editor_dialog.py:601:            row["strike"] = _parse_decimal(row.get("strike"), "strike")
UI/components/structure_editor_dialog.py:611:            multiplier_raw = row.get("multiplier")
UI/components/structure_editor_dialog.py:612:            row["multiplier"] = (
UI/components/structure_editor_dialog.py:614:                if multiplier_raw in (None, "")
UI/components/structure_editor_dialog.py:615:                else _parse_decimal(multiplier_raw, "multiplier")
UI/components/structure_editor_dialog.py:625:        underlying = self._f_underlying.get().strip()
UI/components/structure_editor_dialog.py:637:        if not underlying:
UI/components/structure_editor_dialog.py:639:                str(leg.get("underlying_asset") or "").strip().upper()
UI/components/structure_editor_dialog.py:641:                if str(leg.get("underlying_asset") or "").strip()
UI/components/structure_editor_dialog.py:644:                underlying = detected_assets[0]
UI/components/structure_editor_dialog.py:645:                self._f_underlying.set(underlying)
UI/components/structure_editor_dialog.py:649:                    "As legs possuem ativos objeto diferentes: "
UI/components/structure_editor_dialog.py:655:        if not underlying:
UI/components/structure_editor_dialog.py:656:            messagebox.showwarning("Salvar", "O campo 'Ativo' e obrigatorio.", parent=self)
UI/components/structure_editor_dialog.py:661:            "underlying_asset": underlying,
UI/components/structures_list_panel.py:35:_COLUMNS = ("id", "name", "underlying_asset", "alias", "status", "legs")
UI/components/structures_list_panel.py:39:    "underlying_asset": ("Ativo",     80,  "center"),
UI/components/structures_list_panel.py:181:                or term in r.get("underlying_asset", "").lower()
UI/components/structures_list_panel.py:196:                    row["underlying_asset"],
UI/components/structures_list_panel.py:286:                "underlying_asset": src["underlying_asset"],
UI/debug_utils.py:25:    """Log de payoff chart apenas se debug ativo"""
UI/main_window.py:847:                f"Ativo      : {structure.get('underlying_asset')}",
UI/main_window.py:859:                    f"         Strike : {leg.get('strike')}  Venc: {leg.get('expiration_date')}",
UI/main_window.py:860:                    f"         Qtde   : {leg.get('quantity')}  Símbolo: {leg.get('symbol') or '--'}",
UI/main_window.py:861:                    f"         Prêmio : {leg.get('premium')}  Mult: {leg.get('multiplier')}",
UI/models/ui_data.py:39:    "spot":      ["point_spot", "spot", "underlying", "x", "s_t"],
UI/models/ui_data.py:654:            f"Filtro de estrutura ativo: {filter_info}"    #  alteracao_33
api/pricing_execution_controller.py:31:    underlying_asset: str | None = None,
api/pricing_execution_controller.py:40:            underlying_asset=underlying_asset,
api/pricing_execution_controller.py:53:    underlying_asset: str | None = None,
api/pricing_execution_controller.py:60:            underlying_asset=underlying_asset,
api/structures_controller.py:32:    underlying_asset: str = Field(..., min_length=1, max_length=50)
api/structures_controller.py:39:    underlying_asset: str | None = Field(default=None, min_length=1, max_length=50)
api/structures_controller.py:53:    strike: float        = Field(..., gt=0)
api/structures_controller.py:54:    expiration_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
api/structures_controller.py:56:    multiplier: float    = Field(default=1.0, gt=0)
api/structures_controller.py:59:    symbol: str | None   = None
api/structures_controller.py:85:    underlying_asset: str
api/structures_controller.py:280:    "expiration",
api/structures_controller.py:304:    symbol: str | None = None
db/derived_repo.py:6:Contrato canônico payoff: point_spot / point_pl (opção B).
db/import_excel.py:30:        "ATIVO": "ativo",
db/import_excel.py:32:        "CALL_/_PUT": "call_put",
db/import_excel.py:44:        "STRIKE": "strike",
db/import_excel.py:45:        "VENCIMENTO": "vencimento",
db/schema.py:58:    underlying_price REAL NOT NULL,
db/schema.py:80:    symbol         TEXT,
db/schema_excel.py:42:  ativo TEXT,
db/schema_excel.py:44:  call_put TEXT,                 -- CALL/PUT
db/schema_excel.py:56:  strike REAL,
db/schema_excel.py:57:  vencimento TEXT,
db/schema_excel.py:65:CREATE INDEX IF NOT EXISTS ix_robo_legs_snapshot_ativo ON robo_legs_snapshot(ativo);
db/schema_excel.py:72:  ativo TEXT,
domain/calculation_request.py:75:    strike        : decimal positivo
domain/calculation_request.py:76:    expiration_date: YYYY-MM-DD
domain/calculation_request.py:78:    symbol        : código da opção (ex.: BOVAE195) -- opcional
domain/calculation_request.py:80:    multiplier    : padrão 1.0
domain/calculation_request.py:85:    strike:          float
domain/calculation_request.py:86:    expiration_date: str
domain/calculation_request.py:89:    symbol:      Optional[str]   = None
domain/calculation_request.py:91:    multiplier:  float           = 1.0
domain/calculation_request.py:116:        # strike deve ser positivo
domain/calculation_request.py:117:        object.__setattr__(self, "strike", _require_positive(self.strike, "strike"))
domain/calculation_request.py:121:        # expiration_date: formato canônico
domain/calculation_request.py:123:            self, "expiration_date",
domain/calculation_request.py:124:            _require_date_str(self.expiration_date, "expiration_date")
domain/calculation_request.py:126:        # multiplier
domain/calculation_request.py:127:        if self.multiplier <= 0:
domain/calculation_request.py:128:            raise ValueError(f"multiplier deve ser positivo, recebeu: {self.multiplier}")
domain/calculation_request.py:140:    underlying_asset  : ativo base (ex.: BOVA11)
domain/calculation_request.py:146:    underlying_asset: str
domain/calculation_request.py:157:        _require_nonempty(self.underlying_asset, "underlying_asset")
domain/calculation_request.py:176:    underlying_asset   : deve coincidir com StructureInput.underlying_asset
domain/calculation_request.py:182:    underlying_asset:   str
domain/calculation_request.py:187:    option_quotes:       Optional[dict]  = None   # bid/ask por símbolo
domain/calculation_request.py:193:        _require_nonempty(self.underlying_asset,   "underlying_asset")
domain/calculation_request.py:227:        if self.structure.underlying_asset != self.market_snapshot.underlying_asset:
domain/calculation_request.py:229:                f"underlying_asset diverge entre structure "
domain/calculation_request.py:230:                f"({self.structure.underlying_asset!r}) "
domain/calculation_request.py:231:                f"e market_snapshot ({self.market_snapshot.underlying_asset!r})"
domain/canonical_validators.py:13:    if not structure.get("underlying_asset"):
domain/canonical_validators.py:14:        errors.append("structure.underlying_asset is required")
domain/canonical_validators.py:25:        if leg.get("strike") is None:
domain/canonical_validators.py:26:            errors.append(f"structure.legs[{index}].strike is required")
domain/canonical_validators.py:29:        if leg.get("expiration_date") is None:
domain/canonical_validators.py:30:            errors.append(f"structure.legs[{index}].expiration_date is required")
domain/contracts.py:9:    symbol: str | None
domain/contracts.py:10:    strike: float
domain/contracts.py:11:    expiration_date: str | None
domain/contracts.py:14:    multiplier: float = 1.0
domain/contracts.py:21:    underlying_asset: str
domain/contracts.py:28:    underlying_asset: str
domain/contracts.py:58:                symbol=leg.get("symbol"),
domain/contracts.py:59:                strike=float(leg.get("strike")),
domain/contracts.py:60:                expiration_date=leg.get("expiration_date"),
domain/contracts.py:63:                multiplier=float(leg.get("multiplier", 1.0)),
domain/contracts.py:71:            underlying_asset=structure_raw.get("underlying_asset"),
domain/contracts.py:77:            underlying_asset=market_raw.get("underlying_asset"),
domain/contracts.py:101:                "underlying_asset": self.structure.underlying_asset,
domain/contracts.py:106:                        "symbol": leg.symbol,
domain/contracts.py:107:                        "strike": leg.strike,
domain/contracts.py:108:                        "expiration_date": leg.expiration_date,
domain/contracts.py:111:                        "multiplier": leg.multiplier,
domain/contracts.py:118:                "underlying_asset": self.market.underlying_asset,
domain/market_snapshot.py:30:    ativo           : str
domain/market_snapshot.py:32:    call_put        : Optional[str]   = None
domain/market_snapshot.py:45:    strike          : Optional[float] = None
domain/market_snapshot.py:46:    vencimento      : Optional[str]   = None
domain/payoff.py:19:def _intrinsic_value(option_type: str, strike: float, spot_at_expiration: float) -> float:
domain/payoff.py:21:        return max(spot_at_expiration - strike, 0.0)
domain/payoff.py:23:        return max(strike - spot_at_expiration, 0.0)
domain/payoff.py:27:def _compute_leg_payoff_at_expiration(leg: dict[str, Any], spot_at_expiration: float) -> float:
domain/payoff.py:31:    strike = float(leg.get("strike") or 0.0)
domain/payoff.py:33:    multiplier = float(leg.get("multiplier") or 1.0)
domain/payoff.py:39:        strike=strike,
domain/payoff.py:40:        spot_at_expiration=spot_at_expiration,
domain/payoff.py:48:    return payoff_unit * quantity * multiplier
domain/payoff.py:90:            pl_total += _compute_leg_payoff_at_expiration(
domain/payoff.py:92:                spot_at_expiration=s_t,
domain/payoff.py:146:            "underlying_asset": (
domain/payoff.py:147:                market.get("underlying_asset")
domain/payoff.py:148:                or structure.get("underlying_asset")
domain/payoff.py:169:        "underlying_asset": (
domain/payoff.py:170:            market.get("underlying_asset")
domain/payoff.py:171:            or structure.get("underlying_asset")
domain/structure_metrics.py:73:def compute_dte(reference_date: str | None, expiration_date: str | None) -> int | None:
domain/structure_metrics.py:75:    exp = _parse_date(expiration_date)
domain/structure_metrics.py:92:        expiration_date = leg.get("expiration_date")
domain/structure_metrics.py:93:        dte = compute_dte(reference_date, expiration_date)
domain/structure_metrics.py:160:def position_multiplier(leg: dict[str, Any]) -> int:
domain/structure_metrics.py:239:    return (realistic_price - entry_price) * quantity * position_multiplier(leg)
domain/structure_metrics.py:248:    return greek_value * quantity * position_multiplier(leg)
domain/structure_metrics.py:274:        expiration_date = _first_value(
domain/structure_metrics.py:277:                "expiration_date",
domain/structure_metrics.py:278:                "vencimento",
domain/structure_metrics.py:279:                "maturity_date",
domain/structure_metrics.py:283:        dte = compute_dte(reference_date, expiration_date)
infra/bootstrap_rtd_option_quotes_schema.py:12:    "codigo_opcao",
infra/bootstrap_rtd_option_quotes_schema.py:13:    "ativo_base",
infra/bootstrap_rtd_option_quotes_schema.py:14:    "call_put",
infra/bootstrap_rtd_option_quotes_schema.py:15:    "strike",
infra/bootstrap_rtd_option_quotes_schema.py:16:    "vencimento",
infra/bootstrap_rtd_option_quotes_schema.py:38:    codigo_opcao TEXT NOT NULL,
infra/bootstrap_rtd_option_quotes_schema.py:39:    ativo_base TEXT,
infra/bootstrap_rtd_option_quotes_schema.py:41:    call_put TEXT,
infra/bootstrap_rtd_option_quotes_schema.py:42:    strike REAL,
infra/bootstrap_rtd_option_quotes_schema.py:43:    vencimento TEXT,
infra/bootstrap_rtd_option_quotes_schema.py:64:    UNIQUE(codigo_opcao)
infra/bootstrap_structures_schema.py:36:                underlying_asset TEXT    NOT NULL,
infra/bootstrap_structures_schema.py:56:                symbol          TEXT,
infra/bootstrap_structures_schema.py:57:                strike          REAL    NOT NULL,
infra/bootstrap_structures_schema.py:58:                expiration_date TEXT    NOT NULL,
infra/bootstrap_structures_schema.py:61:                multiplier      REAL    NOT NULL DEFAULT 1,
infra/bootstrap_structures_schema.py:80:                underlying_asset  TEXT,
infra/bootstrap_structures_schema.py:132:                underlying_asset      TEXT,
infra/bootstrap_structures_schema.py:162:                symbol           TEXT,
infra/bootstrap_structures_schema.py:163:                strike           REAL,
infra/bootstrap_structures_schema.py:164:                expiration_date  TEXT,
infra/bootstrap_structures_schema.py:167:                multiplier       REAL,
infra/bootstrap_structures_schema.py:183:            CREATE INDEX IF NOT EXISTS idx_structures_underlying_asset
infra/bootstrap_structures_schema.py:184:            ON structures(underlying_asset)
repositories/market_snapshot_repository.py:36:        ativo,
repositories/market_snapshot_repository.py:38:        call_put,
repositories/market_snapshot_repository.py:50:        strike,
repositories/market_snapshot_repository.py:51:        vencimento,
repositories/market_snapshot_repository.py:63:        ativo,
repositories/market_snapshot_repository.py:65:        call_put,
repositories/market_snapshot_repository.py:77:        strike,
repositories/market_snapshot_repository.py:78:        vencimento,
repositories/market_snapshot_repository.py:167:        ativo=row["ativo"],
repositories/market_snapshot_repository.py:169:        call_put=row["call_put"],
repositories/market_snapshot_repository.py:182:        strike=_parse_br_float(row["strike"]),
repositories/market_snapshot_repository.py:183:        vencimento=row["vencimento"],
repositories/market_snapshot_repository.py:214:    ativo = _first_text(quote_row["codigo_opcao"], base_leg.ativo)
repositories/market_snapshot_repository.py:218:        ativo=ativo,
repositories/market_snapshot_repository.py:220:        call_put=_first_text(quote_row["call_put"], base_leg.call_put),
repositories/market_snapshot_repository.py:233:        strike=_first_float(quote_row["strike"], base_leg.strike),
repositories/market_snapshot_repository.py:234:        vencimento=_first_text(quote_row["vencimento"], base_leg.vencimento),
repositories/market_snapshot_repository.py:283:        A composição da estrutura vem de rtd_analise_robo_legs. Para cada ativo
repositories/market_snapshot_repository.py:284:        dessa composição, se houver cotação em rtd_option_quotes.codigo_opcao,
repositories/market_snapshot_repository.py:285:        preço/greeks/strike/vencimento passam a vir da cotação centralizada.
repositories/market_snapshot_repository.py:291:        ativos = sorted({
repositories/market_snapshot_repository.py:292:            str(leg.ativo).strip().upper()
repositories/market_snapshot_repository.py:294:            if leg.ativo and str(leg.ativo).strip()
repositories/market_snapshot_repository.py:296:        if not ativos:
repositories/market_snapshot_repository.py:299:        placeholders = ", ".join("?" for _ in ativos)
repositories/market_snapshot_repository.py:302:                codigo_opcao,
repositories/market_snapshot_repository.py:303:                ativo_base,
repositories/market_snapshot_repository.py:304:                call_put,
repositories/market_snapshot_repository.py:305:                strike,
repositories/market_snapshot_repository.py:306:                vencimento,
repositories/market_snapshot_repository.py:322:            WHERE UPPER(codigo_opcao) IN ({placeholders})
repositories/market_snapshot_repository.py:328:                rows = conn.execute(sql, ativos).fetchall()
repositories/market_snapshot_repository.py:336:            codigo = str(row["codigo_opcao"]).strip().upper()
repositories/market_snapshot_repository.py:342:            codigo = str(base_leg.ativo).strip().upper() if base_leg.ativo else ""
repositories/pricing_executions_repository.py:47:        underlying_asset = pricing_payload.get("underlying_asset") if pricing_payload else None
repositories/pricing_executions_repository.py:59:                    created_at, structure_id, underlying_asset, reference_date,
repositories/pricing_executions_repository.py:66:                    created_at, structure_id, underlying_asset, reference_date,
repositories/pricing_executions_repository.py:81:            "underlying_asset": underlying_asset,
repositories/robo_legs_repository.py:18:from utils.leg_normalizers import parse_timestamp, parse_vencimento
repositories/robo_legs_repository.py:170:        call_put  = pick("call_put", "cp", "tipo", "callput")
repositories/robo_legs_repository.py:171:        strike    = pick("strike", "k", "preco_exercicio")
repositories/robo_legs_repository.py:173:        ativo     = pick("ativo", "ticker", "cod_ativo")
repositories/robo_legs_repository.py:174:        venc      = pick("vencimento", "vcto", "expiry", "expiracao")
repositories/robo_legs_repository.py:179:        cp_raw  = str(call_put).upper().strip() if call_put  is not None else ""
repositories/robo_legs_repository.py:183:        call_put_norm = "CALL" if cp_raw in ["CALL", "C"] else "PUT"
repositories/robo_legs_repository.py:189:            call_put=call_put_norm,
repositories/robo_legs_repository.py:190:            strike=float(strike)       if strike  is not None else 0.0,
repositories/robo_legs_repository.py:192:            ativo=str(ativo).strip().upper() if ativo is not None else "",
repositories/robo_legs_repository.py:193:            vencimento=parse_vencimento(venc) if venc is not None else None,
repositories/rtd_option_quotes_repository.py:6:- codigo_opcao/symbol;
repositories/rtd_option_quotes_repository.py:7:- ativo_base;
repositories/rtd_option_quotes_repository.py:8:- call_put;
repositories/rtd_option_quotes_repository.py:9:- strike;
repositories/rtd_option_quotes_repository.py:10:- vencimento.
repositories/rtd_option_quotes_repository.py:29:    def get_by_codigo(self, codigo_opcao: str) -> dict[str, Any] | None:
repositories/rtd_option_quotes_repository.py:30:        codigo = str(codigo_opcao or "").strip().upper()
repositories/rtd_option_quotes_repository.py:37:            WHERE UPPER(codigo_opcao) = ?
repositories/structure_events_repository.py:39:        "expiration",
repositories/structure_events_repository.py:163:        "symbol": _normalize_optional_text(data.get("symbol")),
repositories/structure_events_repository.py:208:                symbol         TEXT,
repositories/structure_events_repository.py:330:                    symbol,
repositories/structure_events_repository.py:346:                    event["symbol"],
repositories/structures_repository.py:44:def _validate_expiration_date(value: str) -> str:
repositories/structures_repository.py:46:        raise ValueError("expiration_date is required")
repositories/structures_repository.py:54:            "expiration_date must be a valid date in YYYY-MM-DD format"
repositories/structures_repository.py:62:    underlying_asset = str(data.get("underlying_asset", "")).strip().upper()
repositories/structures_repository.py:70:    if not underlying_asset:
repositories/structures_repository.py:71:        raise ValueError("underlying_asset is required")
repositories/structures_repository.py:84:        "underlying_asset": underlying_asset,
repositories/structures_repository.py:94:    strike          = leg.get("strike")
repositories/structures_repository.py:95:    expiration_date = _validate_expiration_date(leg.get("expiration_date"))
repositories/structures_repository.py:97:    multiplier      = leg.get("multiplier", 1)
repositories/structures_repository.py:98:    symbol          = leg.get("symbol")
repositories/structures_repository.py:108:        strike = float(strike)
repositories/structures_repository.py:110:        raise ValueError("strike must be numeric") from exc
repositories/structures_repository.py:112:    if strike <= 0:
repositories/structures_repository.py:113:        raise ValueError("strike must be > 0")
repositories/structures_repository.py:124:        multiplier = float(multiplier)
repositories/structures_repository.py:126:        raise ValueError("multiplier must be numeric") from exc
repositories/structures_repository.py:128:    if multiplier <= 0:
repositories/structures_repository.py:129:        raise ValueError("multiplier must be > 0")
repositories/structures_repository.py:146:    if symbol is not None:
repositories/structures_repository.py:147:        symbol = str(symbol).strip() or None
repositories/structures_repository.py:155:        "symbol":          symbol,
repositories/structures_repository.py:156:        "strike":          strike,
repositories/structures_repository.py:157:        "expiration_date": expiration_date,
repositories/structures_repository.py:160:        "multiplier":      multiplier,
repositories/structures_repository.py:199:                id, structure_id, position_side, option_type, symbol,
repositories/structures_repository.py:200:                strike, expiration_date, quantity, premium, multiplier,
repositories/structures_repository.py:315:                    name, underlying_asset, alias_legacy_aba,
repositories/structures_repository.py:320:                    payload["name"], payload["underlying_asset"],
repositories/structures_repository.py:369:                    name, underlying_asset, alias_legacy_aba,
repositories/structures_repository.py:375:                    payload["underlying_asset"],
repositories/structures_repository.py:402:                        structure_id, position_side, option_type, symbol,
repositories/structures_repository.py:403:                        strike, expiration_date, quantity, premium,
repositories/structures_repository.py:404:                        multiplier, leg_order, notes, created_at, updated_at
repositories/structures_repository.py:411:                        leg["symbol"],
repositories/structures_repository.py:412:                        leg["strike"],
repositories/structures_repository.py:413:                        leg["expiration_date"],
repositories/structures_repository.py:416:                        leg["multiplier"],
repositories/structures_repository.py:452:            SELECT id, name, underlying_asset, alias_legacy_aba,
repositories/structures_repository.py:476:                SELECT id, name, underlying_asset, alias_legacy_aba,
repositories/structures_repository.py:506:            "underlying_asset": data.get("underlying_asset", current["underlying_asset"]),
repositories/structures_repository.py:519:                SET name=?, underlying_asset=?, alias_legacy_aba=?,
repositories/structures_repository.py:524:                    payload["name"], payload["underlying_asset"],
repositories/structures_repository.py:597:                    structure_id, position_side, option_type, symbol,
repositories/structures_repository.py:598:                    strike, expiration_date, quantity, premium,
repositories/structures_repository.py:599:                    multiplier, leg_order, notes, created_at, updated_at
repositories/structures_repository.py:604:                    leg["symbol"], leg["strike"], leg["expiration_date"],
repositories/structures_repository.py:605:                    leg["quantity"], leg["premium"], leg["multiplier"],
repositories/structures_repository.py:651:                        structure_id, position_side, option_type, symbol,
repositories/structures_repository.py:652:                        strike, expiration_date, quantity, premium,
repositories/structures_repository.py:653:                        multiplier, leg_order, notes, created_at, updated_at
repositories/structures_repository.py:658:                        leg["symbol"], leg["strike"], leg["expiration_date"],
repositories/structures_repository.py:659:                        leg["quantity"], leg["premium"], leg["multiplier"],
repositories/structures_repository.py:713:                SELECT id, name, underlying_asset, alias_legacy_aba,
repositories/system_snapshots_repository.py:85:        underlying_asset: str | None = None,
repositories/system_snapshots_repository.py:117:                    underlying_asset,
repositories/system_snapshots_repository.py:134:                    underlying_asset,
repositories/system_snapshots_repository.py:178:                symbol,
repositories/system_snapshots_repository.py:179:                strike,
repositories/system_snapshots_repository.py:180:                expiration_date,
repositories/system_snapshots_repository.py:183:                multiplier,
repositories/system_snapshots_repository.py:197:                leg.get("symbol"),
repositories/system_snapshots_repository.py:198:                leg.get("strike"),
repositories/system_snapshots_repository.py:199:                leg.get("expiration_date"),
repositories/system_snapshots_repository.py:202:                leg.get("multiplier"),
services/calculation_orchestrator.py:4:# alteracao_47: run_full_pipeline, multiplier fix (1.0), run_decision auto-extract
services/calculation_orchestrator.py:70:                    row.get("option_type") or row.get("call_put", "")
services/calculation_orchestrator.py:72:                strike=float(row["strike"]),
services/calculation_orchestrator.py:73:                expiration_date=str(row["expiration_date"]),
services/calculation_orchestrator.py:75:                symbol=row.get("symbol"),
services/calculation_orchestrator.py:77:                multiplier=float(row.get("multiplier") or 1.0),
services/calculation_orchestrator.py:87:        underlying_asset=str(structure_row["underlying_asset"]),
services/calculation_orchestrator.py:95:        underlying_asset=str(snapshot_row["underlying_asset"]),
services/calculation_orchestrator.py:115:    """alteracao_47: multiplier usa leg.multiplier com fallback 1.0."""
services/calculation_orchestrator.py:121:            "strike":          leg.strike,
services/calculation_orchestrator.py:122:            "expiration_date": leg.expiration_date,
services/calculation_orchestrator.py:124:            "symbol":          getattr(leg, "symbol",      None),
services/calculation_orchestrator.py:126:            "multiplier":      getattr(leg, "multiplier",  1.0),
services/calculation_orchestrator.py:134:            "underlying_asset": request.structure.underlying_asset,
services/calculation_orchestrator.py:140:            "underlying_asset": request.market_snapshot.underlying_asset,
services/calculation_orchestrator.py:219:        "underlying_asset": request.structure.underlying_asset,
services/calculation_orchestrator.py:265:                        leg.get("option_type") or leg.get("call_put", "CALL")
services/calculation_orchestrator.py:267:                    strike=float(leg["strike"]),
services/calculation_orchestrator.py:268:                    expiration_date=str(leg["expiration_date"]),
services/calculation_orchestrator.py:270:                    symbol=leg.get("symbol"),
services/calculation_orchestrator.py:272:                    multiplier=float(leg.get("multiplier") or 1.0),
services/calculation_orchestrator.py:281:            underlying_asset=str(structure_dict.get("underlying_asset", "")),
services/calculation_orchestrator.py:289:            underlying_asset=str(market_snapshot_dict.get("underlying_asset", "")),
services/calculation_orchestrator.py:310:                "strike":          leg.strike,
services/calculation_orchestrator.py:311:                "expiration_date": leg.expiration_date,
services/calculation_orchestrator.py:313:                "symbol":          getattr(leg, "symbol",     None),
services/calculation_orchestrator.py:315:                "multiplier":      getattr(leg, "multiplier", 1.0),
services/calculation_orchestrator.py:323:                "underlying_asset": request.structure.underlying_asset,
services/calculation_orchestrator.py:329:                "underlying_asset": request.market_snapshot.underlying_asset,
services/calculation_orchestrator.py:401:            "underlying_asset": request.structure.underlying_asset,
services/calculation_orchestrator.py:451:        underlying = structure.get("underlying_asset", "")
services/calculation_orchestrator.py:453:            underlying_asset=underlying,
services/calculation_orchestrator.py:458:                f"Snapshot nao encontrado para underlying_asset='{underlying}' "
services/calculation_orchestrator.py:466:            "underlying_asset": underlying,
services/calculation_orchestrator.py:472:                    "strike":          leg["strike"],
services/calculation_orchestrator.py:473:                    "expiration_date": leg["expiration_date"],
services/calculation_orchestrator.py:475:                    "symbol":          leg.get("symbol"),
services/calculation_orchestrator.py:477:                    "multiplier":      leg.get("multiplier", 1.0),
services/calculation_orchestrator.py:488:            "underlying_asset":   snapshot.get("underlying_asset", underlying),
services/canonical_input_service.py:8:  - _resolve_legs            → MarketSnapshotSelector (manual > rtd por ativo)
services/canonical_input_service.py:14:    "underlying_asset":   str,
services/canonical_input_service.py:101:            "underlying_asset":  self._clean_text(structure.get("underlying_asset")),
services/canonical_input_service.py:153:        underlying_asset = structure["underlying_asset"]
services/canonical_input_service.py:158:            underlying_asset,
services/canonical_input_service.py:174:            **base_snapshot,            # reference_date, underlying_asset, spot_price,
services/canonical_input_service.py:208:                "ativo":            leg.ativo,
services/canonical_input_service.py:212:                "call_put":         leg.call_put,
services/canonical_input_service.py:228:                "strike":           leg.strike,
services/canonical_input_service.py:229:                "vencimento":       leg.vencimento,
services/canonical_pricing_facade.py:6:alteracao_41 -- Corrige underlying_asset no pricing_payload.
services/canonical_pricing_facade.py:10:      busca alias_legacy_aba E underlying_asset em uma única query.
services/canonical_pricing_facade.py:11:  C7: _snapshot_result_to_payload() recebe underlying_asset explícito --
services/canonical_pricing_facade.py:12:      elimina uso de selection_result.aba como underlying_asset
services/canonical_pricing_facade.py:13:      (aba legada  ativo subjacente real).
services/canonical_pricing_facade.py:14:  C8: execute_pricing() passa underlying_asset para o payload builder.
services/canonical_pricing_facade.py:43:#  C6: substitui _get_alias_legacy_aba -- busca aba + underlying em 1 query 
services/canonical_pricing_facade.py:47:    Retorna (alias_legacy_aba, underlying_asset) para a estrutura.
services/canonical_pricing_facade.py:56:            "SELECT alias_legacy_aba, underlying_asset FROM structures WHERE id = ?",
services/canonical_pricing_facade.py:67:    underlying_asset = row["underlying_asset"]  # NOT NULL -- sempre presente
services/canonical_pricing_facade.py:69:    return aba, underlying_asset
services/canonical_pricing_facade.py:72:#  C7: recebe underlying_asset explícito -- não usa selection_result.aba 
services/canonical_pricing_facade.py:110:def _normalize_expiration_date(value: Any) -> str | None:
services/canonical_pricing_facade.py:144:def _lookup_spot_price(db_path: Path, underlying_asset: str) -> float:
services/canonical_pricing_facade.py:152:    if not underlying_asset:
services/canonical_pricing_facade.py:155:    symbol_candidates = {
services/canonical_pricing_facade.py:157:        "ativo",
services/canonical_pricing_facade.py:159:        "symbol",
services/canonical_pricing_facade.py:161:        "underlying_asset",
services/canonical_pricing_facade.py:169:        "underlying_price",
services/canonical_pricing_facade.py:195:                symbol_cols = [
services/canonical_pricing_facade.py:197:                    for name in symbol_candidates
services/canonical_pricing_facade.py:207:                if not symbol_cols or not price_cols:
services/canonical_pricing_facade.py:210:                for symbol_col in symbol_cols:
services/canonical_pricing_facade.py:215:                            f"WHERE UPPER(CAST({_quote_ident(symbol_col)} AS TEXT)) = UPPER(?) "
services/canonical_pricing_facade.py:221:                            rows = conn.execute(query, (underlying_asset,)).fetchall()
services/canonical_pricing_facade.py:238:    underlying_asset: str,
services/canonical_pricing_facade.py:250:        raw_asset = _pick(d, "symbol", "asset", "ativo")
services/canonical_pricing_facade.py:251:        raw_expiry = _pick(d, "expiration_date", "expiry", "vencimento")
services/canonical_pricing_facade.py:262:            "option_type": _pick(d, "option_type", "call_put"),
services/canonical_pricing_facade.py:263:            "strike":      _to_float(_pick(d, "strike"), 0.0),
services/canonical_pricing_facade.py:273:            "symbol":          raw_asset,
services/canonical_pricing_facade.py:275:            "expiration_date": _normalize_expiration_date(raw_expiry),
services/canonical_pricing_facade.py:276:            "multiplier":      1.0,
services/canonical_pricing_facade.py:286:        or getattr(selection_result, "underlying_price", None)
services/canonical_pricing_facade.py:295:            underlying_asset=underlying_asset,
services/canonical_pricing_facade.py:300:            f"spot_price inválido ou ausente para underlying_asset={underlying_asset}. "
services/canonical_pricing_facade.py:306:        "underlying_asset": underlying_asset,
services/canonical_pricing_facade.py:326:             alias_legacy_aba + underlying_asset  (query em structures)
services/canonical_pricing_facade.py:328:                             pricing_payload  (underlying_asset = ativo real)
services/canonical_pricing_facade.py:369:                aba, underlying_asset = _get_structure_info(
services/canonical_pricing_facade.py:379:                    underlying_asset=underlying_asset,
services/derived_payoff_persistence.py:153:                    "underlying_asset": pricing_payload.get("underlying_asset"),
services/derived_payoff_persistence.py:162:                underlying_asset=pricing_payload.get("underlying_asset"),
services/derived_payoff_persistence.py:268:        if "symbol" not in data:
services/derived_payoff_persistence.py:269:            data["symbol"] = data.get("asset") or data.get("ativo")
services/derived_payoff_persistence.py:323:        underlying     = pricing_payload.get("underlying_asset")
services/derived_payoff_persistence.py:337:                "underlying_asset": underlying,
services/derived_payoff_persistence.py:345:                "underlying_asset": underlying,
services/derived_service.py:93:    underlying_asset: Any = None,
services/derived_service.py:115:    # 3. fallbacks por nome/ativo
services/derived_service.py:120:    resolved_underlying_asset = _safe_str(underlying_asset)
services/derived_service.py:121:    if resolved_underlying_asset:
services/derived_service.py:122:        return resolved_underlying_asset
services/derived_service.py:131:    underlying_asset: Any = None,
services/derived_service.py:140:        "underlying_asset": underlying_asset,
services/derived_service.py:221:        underlying_asset=payoff.get("underlying_asset"),
services/derived_service.py:235:        underlying_asset=payoff.get("underlying_asset"),
services/derived_service.py:326:    underlying_asset: Any = None,
services/derived_service.py:336:        underlying_asset=underlying_asset,
services/derived_service.py:352:            "underlying_asset": underlying_asset,
services/legacy_robo_legs_fallback.py:213:            data.get("call_put") or data.get("option_type")
services/legacy_robo_legs_fallback.py:216:        expiration_date = (
services/legacy_robo_legs_fallback.py:217:            data.get("expiration_date")
services/legacy_robo_legs_fallback.py:218:            or data.get("vencimento")
services/legacy_robo_legs_fallback.py:223:        if expiration_date is not None:
services/legacy_robo_legs_fallback.py:224:            expiration_date = str(expiration_date)
services/legacy_robo_legs_fallback.py:229:            "symbol": self._clean_upper_text(
services/legacy_robo_legs_fallback.py:230:                data.get("ativo") or data.get("symbol") or data.get("ticker")
services/legacy_robo_legs_fallback.py:232:            "strike": float(data.get("strike") or 0.0),
services/legacy_robo_legs_fallback.py:233:            "expiration_date": expiration_date,
services/legacy_robo_legs_fallback.py:238:            "multiplier": float(data.get("multiplier") or 1.0),
services/legacy_structure_legs_reader.py:32:        multiplier: float = 1.0,
services/legacy_structure_legs_reader.py:44:                multiplier=multiplier,
services/market_snapshot_provider.py:53:    def get_snapshot(self, underlying_asset: str, reference_date: str | None = None) -> dict[str, Any]:
services/market_snapshot_provider.py:54:        asset = str(underlying_asset or "").strip().upper()
services/market_snapshot_provider.py:56:            raise ValueError("underlying_asset is required")
services/market_snapshot_provider.py:66:            "underlying_asset": asset,
services/market_snapshot_selector.py:6:  - Se existir snapshot manual para o ativo, usa manual
services/market_snapshot_selector.py:88:        # por ativo, que tende a ser a mais recente.
services/market_snapshot_selector.py:90:        manual_by_ativo: dict[str, LegMarketSnapshot] = {}
services/market_snapshot_selector.py:92:            if leg.ativo and leg.ativo not in manual_by_ativo:
services/market_snapshot_selector.py:93:                manual_by_ativo[leg.ativo] = leg
services/market_snapshot_selector.py:95:        rtd_option_quote_by_ativo: dict[str, LegMarketSnapshot] = {}
services/market_snapshot_selector.py:97:            if leg.ativo and leg.ativo not in rtd_option_quote_by_ativo:
services/market_snapshot_selector.py:98:                rtd_option_quote_by_ativo[leg.ativo] = leg
services/market_snapshot_selector.py:100:        rtd_by_ativo: dict[str, LegMarketSnapshot] = {}
services/market_snapshot_selector.py:102:            if leg.ativo and leg.ativo not in rtd_by_ativo:
services/market_snapshot_selector.py:103:                rtd_by_ativo[leg.ativo] = leg
services/market_snapshot_selector.py:105:        todos_ativos = sorted(
services/market_snapshot_selector.py:106:            set(manual_by_ativo)
services/market_snapshot_selector.py:107:            | set(rtd_option_quote_by_ativo)
services/market_snapshot_selector.py:108:            | set(rtd_by_ativo)
services/market_snapshot_selector.py:114:        for ativo in todos_ativos:
services/market_snapshot_selector.py:115:            if ativo in manual_by_ativo:
services/market_snapshot_selector.py:116:                legs_selected.append(manual_by_ativo[ativo])
services/market_snapshot_selector.py:117:                if ativo in rtd_option_quote_by_ativo or ativo in rtd_by_ativo:
services/market_snapshot_selector.py:118:                    overrides.append(ativo)
services/market_snapshot_selector.py:119:            elif ativo in rtd_option_quote_by_ativo:
services/market_snapshot_selector.py:120:                legs_selected.append(rtd_option_quote_by_ativo[ativo])
services/market_snapshot_selector.py:122:                legs_selected.append(rtd_by_ativo[ativo])
services/payoff_pricing_engine.py:64:            "underlying_asset": pricing_payload.get("underlying_asset"),
services/payoff_pricing_engine.py:85:                "method": "expiration_payoff_grid",
services/payoff_pricing_engine.py:108:        normalized["strike"] = float(normalized.get("strike") or 0.0)
services/payoff_pricing_engine.py:110:        normalized["multiplier"] = float(normalized.get("multiplier") or 1.0)
services/payoff_pricing_engine.py:129:    def _intrinsic_value(option_type: str, strike: float, spot: float) -> float:
services/payoff_pricing_engine.py:131:            return max(spot - strike, 0.0)
services/payoff_pricing_engine.py:133:            return max(strike - spot, 0.0)
services/payoff_pricing_engine.py:146:                strike=float(leg.get("strike") or 0.0),
services/payoff_pricing_engine.py:152:            multiplier = float(leg.get("multiplier") or 1.0)
services/payoff_pricing_engine.py:159:            total += unit_pl * quantity * multiplier
services/payoff_pricing_engine.py:170:            multiplier = float(leg.get("multiplier") or 1.0)
services/payoff_pricing_engine.py:172:            amount = premium * quantity * multiplier
services/pricing_execution_app_service.py:72:        underlying_asset: str | None = None,
services/pricing_execution_app_service.py:79:            underlying_asset=underlying_asset,
services/pricing_execution_app_service.py:88:        underlying_asset: str | None = None,
services/pricing_execution_app_service.py:94:            underlying_asset=underlying_asset,
services/pricing_execution_app_service.py:105:        underlying_asset: str | None = None,
services/pricing_execution_app_service.py:114:            underlying_asset=underlying_asset,
services/pricing_execution_persistence_service.py:117:                underlying_asset=pricing_payload.get("underlying_asset"),
services/pricing_execution_persistence_service.py:145:            "underlying_asset": pricing_payload.get("underlying_asset"),
services/pricing_execution_query_service.py:19:        underlying_asset: str | None = None,
services/pricing_execution_query_service.py:26:        if underlying_asset is not None and not underlying_asset.strip():
services/pricing_execution_query_service.py:27:            raise ValueError("underlying_asset must not be empty")
services/pricing_execution_query_service.py:78:        underlying_asset: str | None = None,
services/pricing_execution_query_service.py:85:            underlying_asset=underlying_asset,
services/pricing_execution_query_service.py:111:                "underlying_asset": execution["underlying_asset"],
services/pricing_execution_query_service.py:137:            if underlying_asset is not None:
services/pricing_execution_query_service.py:138:                if str(summary["underlying_asset"]).upper() != underlying_asset.upper():
services/pricing_execution_query_service.py:155:        underlying_asset: str | None = None,
services/pricing_execution_query_service.py:164:            underlying_asset=underlying_asset,
services/pricing_execution_query_service.py:177:            underlying_asset=underlying_asset,
services/pricing_execution_query_service.py:203:        underlying_asset: str | None = None,
services/pricing_execution_query_service.py:209:            underlying_asset=underlying_asset,
services/pricing_execution_query_service.py:216:            underlying_asset=underlying_asset,
services/pricing_payload_adapter.py:43:                "symbol": _clean_upper_text(leg.get("symbol")),
services/pricing_payload_adapter.py:44:                "strike": float(leg["strike"]),
services/pricing_payload_adapter.py:45:                "expiration_date": _clean_text(leg["expiration_date"]),
services/pricing_payload_adapter.py:48:                "multiplier": float(leg["multiplier"]),
services/pricing_payload_adapter.py:55:        "underlying_asset": _clean_upper_text(structure["underlying_asset"]),
services/robo_leg_mapper.py:43:def to_canonical_leg(leg: Any, multiplier: float = 1.0) -> dict[str, Any]:
services/robo_leg_mapper.py:45:    call_put = _enum_value(_read_attr(leg, "call_put"))
services/robo_leg_mapper.py:46:    ativo = _read_attr(leg, "ativo")
services/robo_leg_mapper.py:47:    strike = _read_attr(leg, "strike")
services/robo_leg_mapper.py:48:    vencimento = _read_attr(leg, "vencimento")
services/robo_leg_mapper.py:53:    call_put_str = str(call_put).upper().strip() if call_put is not None else ""
services/robo_leg_mapper.py:60:    if call_put_str == "CALL":
services/robo_leg_mapper.py:62:    elif call_put_str == "PUT":
services/robo_leg_mapper.py:65:        raise ValueError(f"invalid call_put: {call_put}")
services/robo_leg_mapper.py:70:        "symbol": _safe_upper_text(ativo),
services/robo_leg_mapper.py:71:        "strike": _to_float(strike, "strike"),
services/robo_leg_mapper.py:72:        "expiration_date": vencimento.strftime("%Y-%m-%d") if vencimento else None,
services/robo_leg_mapper.py:75:        "multiplier": float(multiplier),
services/structure_events_service.py:20:        "expiration",
services/structure_events_service.py:117:        symbol: str | None = None,
services/structure_events_service.py:139:            "symbol": self._normalize_optional_text(symbol),
services/structure_events_service.py:170:        symbol: str | None = None,
services/structure_events_service.py:181:            symbol=symbol,
services/structure_events_service.py:304:        - assignment, exercise e expiration zeram a perna alvo ou estrutura.
services/structure_events_service.py:377:            if event_type in {"assignment", "exercise", "expiration"}:
services/structure_events_service.py:436:        symbol = self._normalize_optional_text(event.get("symbol"))
services/structure_events_service.py:438:        if leg_id is None and symbol is None:
services/structure_events_service.py:453:            if symbol is not None:
services/structure_events_service.py:454:                leg_symbol = self._normalize_optional_text(leg.get("symbol"))
services/structure_events_service.py:455:                if leg_symbol == symbol:
services/structure_input_mapper.py:55:        "symbol": _clean_upper_text(leg.get("symbol")),
services/structure_input_mapper.py:56:        "strike": leg["strike"],
services/structure_input_mapper.py:57:        "expiration_date": _clean_text(leg["expiration_date"]),
services/structure_input_mapper.py:60:        "multiplier": leg.get("multiplier", 1.0),
services/structure_input_mapper.py:94:        "underlying_asset": _clean_upper_text(structure["underlying_asset"]),
services/structure_leg_rtd_enrichment_service.py:4:- receber entrada minima baseada em simbolo/codigo da opcao;
services/structure_leg_rtd_enrichment_service.py:5:- consultar rtd_option_quotes por codigo_opcao;
services/structure_leg_rtd_enrichment_service.py:24:        """Retorna uma leg canonica enriquecida a partir do simbolo da opcao.
services/structure_leg_rtd_enrichment_service.py:27:        - symbol ou codigo_opcao;
services/structure_leg_rtd_enrichment_service.py:32:        - underlying_asset;
services/structure_leg_rtd_enrichment_service.py:34:        - strike;
services/structure_leg_rtd_enrichment_service.py:35:        - expiration_date.
services/structure_leg_rtd_enrichment_service.py:38:        symbol = self._normalize_symbol(
services/structure_leg_rtd_enrichment_service.py:39:            leg_data.get("symbol") or leg_data.get("codigo_opcao")
services/structure_leg_rtd_enrichment_service.py:41:        if not symbol:
services/structure_leg_rtd_enrichment_service.py:42:            raise ValueError("symbol is required for RTD leg enrichment")
services/structure_leg_rtd_enrichment_service.py:44:        quote = self._repo.get_by_codigo(symbol)
services/structure_leg_rtd_enrichment_service.py:46:            raise ValueError(f"option quote not found for symbol: {symbol}")
services/structure_leg_rtd_enrichment_service.py:50:            required=("ativo_base", "call_put", "strike", "vencimento"),
services/structure_leg_rtd_enrichment_service.py:53:        detected_option_type = self._normalize_option_type(quote.get("call_put"))
services/structure_leg_rtd_enrichment_service.py:60:                    "option_type divergente do símbolo informado: "
services/structure_leg_rtd_enrichment_service.py:63:                    f"symbol={symbol}"
services/structure_leg_rtd_enrichment_service.py:67:            "symbol": symbol,
services/structure_leg_rtd_enrichment_service.py:70:            "strike": self._to_float(quote.get("strike"), "strike"),
services/structure_leg_rtd_enrichment_service.py:71:            "expiration_date": str(quote.get("vencimento")).strip(),
services/structure_leg_rtd_enrichment_service.py:74:            "multiplier": self._to_float(
services/structure_leg_rtd_enrichment_service.py:75:                leg_data.get("multiplier", 1.0),
services/structure_leg_rtd_enrichment_service.py:76:                "multiplier",
services/structure_leg_rtd_enrichment_service.py:80:            "underlying_asset": self._normalize_required_text(
services/structure_leg_rtd_enrichment_service.py:81:                quote.get("ativo_base"),
services/structure_leg_rtd_enrichment_service.py:82:                "ativo_base",
services/structure_leg_rtd_enrichment_service.py:87:    def _normalize_symbol(value: Any) -> str:
services/structure_leg_rtd_enrichment_service.py:114:            raise ValueError(f"invalid option_type/call_put: {value!r}")
services/structure_market_input_assembler.py:17:    structure_asset = structure_input["underlying_asset"]
services/structure_market_input_assembler.py:18:    market_asset = market_snapshot.get("underlying_asset")
services/structure_market_input_assembler.py:22:            f"underlying_asset mismatch: structure={structure_asset} market={market_asset}"
services/structure_market_input_assembler.py:29:            "underlying_asset": market_snapshot["underlying_asset"],

## Grep - cadastro/editor/legs
ATT/tests/conftest.py:267:    fd.asksaveasfilename = MagicMock(return_value="")
ATT/tests/test_canonical_input_service.py:40:class FakeRoboLegsService:
ATT/tests/test_canonical_input_service.py:41:    def __init__(self, timestamps=None, legs=None):
ATT/tests/test_canonical_input_service.py:44:        self._legs = legs or []
ATT/tests/test_canonical_input_service.py:51:    def get_legs(self, aba, timestamp, validate=False):
ATT/tests/test_canonical_input_service.py:54:        return self._legs
ATT/tests/test_canonical_input_service.py:59:    def __init__(self, legs, meta):
ATT/tests/test_canonical_input_service.py:60:        self._legs = legs
ATT/tests/test_canonical_input_service.py:64:        return self._legs, self._meta
ATT/tests/test_canonical_input_service.py:68:    def test_should_always_prefer_canonical_legs_when_structure_already_has_legs(self):
ATT/tests/test_canonical_input_service.py:74:            "legs": [
ATT/tests/test_canonical_input_service.py:91:            robo_legs_service=FakeRoboLegsService(
ATT/tests/test_canonical_input_service.py:93:                legs=[{"any": "value"}],
ATT/tests/test_canonical_input_service.py:95:            prefer_canonical_legs=True,
ATT/tests/test_canonical_input_service.py:96:            enable_legacy_legs_fallback=True,
ATT/tests/test_canonical_input_service.py:104:        self.assertEqual(result["meta"]["legs_source"], "canonical")
ATT/tests/test_canonical_input_service.py:106:        self.assertEqual(len(result["structure"]["legs"]), 1)
ATT/tests/test_canonical_input_service.py:107:        self.assertEqual(result["structure"]["legs"][0]["symbol"], "BOVAE195")
ATT/tests/test_canonical_input_service.py:110:    def test_should_use_legacy_robo_only_when_no_canonical_legs_exist(self):
ATT/tests/test_canonical_input_service.py:116:            "legs": [],
ATT/tests/test_canonical_input_service.py:122:            robo_legs_service=FakeRoboLegsService(
ATT/tests/test_canonical_input_service.py:124:                legs=[
ATT/tests/test_canonical_input_service.py:137:            enable_legacy_legs_fallback=True,
ATT/tests/test_canonical_input_service.py:145:        self.assertEqual(result["meta"]["legs_source"], "legacy_fallback")
ATT/tests/test_canonical_input_service.py:149:        self.assertEqual(len(result["structure"]["legs"]), 1)
ATT/tests/test_canonical_input_service.py:150:        self.assertEqual(result["structure"]["legs"][0]["symbol"], "BOVAE195")
ATT/tests/test_canonical_input_service.py:153:    def test_should_return_empty_when_no_canonical_legs_and_fallback_disabled(self):
ATT/tests/test_canonical_input_service.py:159:            "legs": [],
ATT/tests/test_canonical_input_service.py:165:            robo_legs_service=FakeRoboLegsService(
ATT/tests/test_canonical_input_service.py:167:                legs=[],
ATT/tests/test_canonical_input_service.py:169:            enable_legacy_legs_fallback=False,
ATT/tests/test_canonical_input_service.py:177:        self.assertEqual(result["meta"]["legs_source"], "empty")
ATT/tests/test_canonical_input_service.py:179:        self.assertEqual(result["structure"]["legs"], [])
ATT/tests/test_canonical_input_service.py:183:    def test_should_return_empty_when_legacy_fallback_returns_no_legs(self):
ATT/tests/test_canonical_input_service.py:189:            "legs": [],
ATT/tests/test_canonical_input_service.py:195:            prefer_canonical_legs=True,
ATT/tests/test_canonical_input_service.py:196:            enable_legacy_legs_fallback=True,
ATT/tests/test_canonical_input_service.py:199:        service.legacy_robo_legs_fallback = FakeLegacyFallback(
ATT/tests/test_canonical_input_service.py:200:            legs=[],
ATT/tests/test_canonical_input_service.py:201:            meta={"fallback_reason": "no_legacy_legs_found"},
ATT/tests/test_canonical_input_service.py:204:        enriched, meta = service._enrich_structure_with_legs(
ATT/tests/test_canonical_input_service.py:209:        self.assertEqual(enriched["legs"], [])
ATT/tests/test_canonical_input_service.py:210:        self.assertEqual(meta["legs_source"], "empty")
ATT/tests/test_canonical_input_service.py:211:        self.assertEqual(meta["fallback_reason"], "no_legacy_legs_found")
ATT/tests/test_canonical_input_service.py:219:            "legs": [
ATT/tests/test_canonical_input_service.py:258:            robo_legs_service=FakeRoboLegsService(),
ATT/tests/test_canonical_input_service.py:259:            prefer_canonical_legs=True,
ATT/tests/test_canonical_input_service.py:260:            enable_legacy_legs_fallback=True,
ATT/tests/test_canonical_input_service.py:283:    def test_should_keep_internal_metric_fields_as_none_when_no_legs(self):
ATT/tests/test_canonical_input_service.py:289:            "legs": [],
ATT/tests/test_canonical_input_service.py:295:            robo_legs_service=FakeRoboLegsService(),
ATT/tests/test_canonical_input_service.py:296:            prefer_canonical_legs=True,
ATT/tests/test_canonical_input_service.py:297:            enable_legacy_legs_fallback=False,
ATT/tests/test_canonical_pricing_facade.py:11:        "legs": [],
ATT/tests/test_canonical_pricing_facade.py:38:            legs=[
ATT/tests/test_canonical_pricing_facade.py:55:    leg = payload["legs"][0]
ATT/tests/test_canonical_pricing_facade.py:64:        legs=[
ATT/tests/test_canonical_pricing_facade.py:96:        "legs_count": 1,
ATT/tests/test_canonical_pricing_facade.py:99:    leg = payload["legs"][0]
ATT/tests/test_canonical_pricing_facade.py:123:        selection_result=_selection(legs=[leg_input]),
ATT/tests/test_canonical_pricing_facade.py:130:    leg = payload["legs"][0]
ATT/tests/test_canonical_pricing_facade.py:147:        selection_result=_selection(spot_price=0, legs=[]),
ATT/tests/test_canonical_pricing_facade.py:155:    assert payload["legs"] == []
ATT/tests/test_canonical_pricing_facade.py:156:    assert payload["meta"]["legs_count"] == 0
ATT/tests/test_canonical_pricing_facade.py:162:            selection_result=_selection(spot_price=0, legs=[]),
ATT/tests/test_canonical_pricing_facade_manual_without_alias.py:16:            "legs": [],
ATT/tests/test_canonical_validators.py:10:            "legs": [
ATT/tests/test_contracts.py:10:            "legs": [
ATT/tests/test_contracts.py:32:            "legs_source": "canonical",
ATT/tests/test_contracts.py:45:    assert result["meta"]["legs_source"] == "canonical"
ATT/tests/test_derived_service.py:75:        input_meta={"legs_source": "canonical"},
ATT/tests/test_derived_service.py:83:    assert result["input_meta"]["legs_source"] == "canonical"
ATT/tests/test_derived_service.py:86:def test_save_payoff_from_canonical_payload_should_use_resolved_storage_key(monkeypatch):
ATT/tests/test_derived_service.py:89:    def fake_save_payoff_curve(ref, points, spot_ref=None, meta=None, timestamp=None):
ATT/tests/test_derived_service.py:97:    monkeypatch.setattr(ds, "save_payoff_curve", fake_save_payoff_curve)
ATT/tests/test_derived_service.py:110:    result = ds.save_payoff_from_canonical_payload(payload)
ATT/tests/test_derived_service.py:125:def test_save_decision_from_canonical_payload_should_enrich_meta(monkeypatch):
ATT/tests/test_derived_service.py:128:    def fake_save_decision(ref, decision, timestamp=None):
ATT/tests/test_derived_service.py:134:    monkeypatch.setattr(ds, "save_decision", fake_save_decision)
ATT/tests/test_derived_service.py:141:    result = ds.save_decision_from_canonical_payload(
ATT/tests/test_derived_service.py:159:def test_save_decision_preserva_structure_id_explicito_sem_alias(monkeypatch):
ATT/tests/test_derived_service.py:182:    result = svc.save_decision(
ATT/tests/test_legacy_robo_legs_fallback.py:1:from services.legacy_robo_legs_fallback import LegacyRoboLegsFallback
ATT/tests/test_legacy_robo_legs_fallback.py:9:class DummyRoboLegsService:
ATT/tests/test_legacy_robo_legs_fallback.py:10:    def __init__(self, chosen_ts="2026-05-19 10:00:00", legs=None):
ATT/tests/test_legacy_robo_legs_fallback.py:12:        self._legs = legs or []
ATT/tests/test_legacy_robo_legs_fallback.py:17:    def get_legs(self, aba, timestamp):
ATT/tests/test_legacy_robo_legs_fallback.py:18:        return self._legs
ATT/tests/test_legacy_robo_legs_fallback.py:22:    svc = LegacyRoboLegsFallback(robo_legs_service=None, allow_name_fallback=False)
ATT/tests/test_legacy_robo_legs_fallback.py:35:    svc = LegacyRoboLegsFallback(robo_legs_service=None, allow_name_fallback=False)
ATT/tests/test_legacy_robo_legs_fallback.py:48:    svc = LegacyRoboLegsFallback(robo_legs_service=None, allow_name_fallback=True)
ATT/tests/test_legacy_robo_legs_fallback.py:61:    svc = LegacyRoboLegsFallback(robo_legs_service=None, allow_name_fallback=False)
ATT/tests/test_legacy_robo_legs_fallback.py:63:    legs, meta = svc.load(
ATT/tests/test_legacy_robo_legs_fallback.py:68:    assert legs == []
ATT/tests/test_legacy_robo_legs_fallback.py:69:    assert meta["legs_source"] == "empty"
ATT/tests/test_legacy_robo_legs_fallback.py:75:    svc = LegacyRoboLegsFallback(robo_legs_service=None, allow_name_fallback=False)
ATT/tests/test_legacy_robo_legs_fallback.py:77:    legs, meta = svc.load(
ATT/tests/test_legacy_robo_legs_fallback.py:82:    assert legs == []
ATT/tests/test_legacy_robo_legs_fallback.py:84:    assert meta["fallback_reason"] == "robo_legs_service_unavailable"
ATT/tests/test_legacy_robo_legs_fallback.py:88:    robo_service = DummyRoboLegsService(
ATT/tests/test_legacy_robo_legs_fallback.py:90:        legs=[
ATT/tests/test_legacy_robo_legs_fallback.py:102:    svc = LegacyRoboLegsFallback(robo_legs_service=robo_service, allow_name_fallback=False)
ATT/tests/test_legacy_robo_legs_fallback.py:104:    legs, meta = svc.load(
ATT/tests/test_legacy_robo_legs_fallback.py:109:    assert len(legs) == 1
ATT/tests/test_legacy_robo_legs_fallback.py:110:    assert legs[0]["position_side"] == "COMPRADO"
ATT/tests/test_legacy_robo_legs_fallback.py:111:    assert legs[0]["option_type"] == "CALL"
ATT/tests/test_legacy_robo_legs_fallback.py:112:    assert legs[0]["symbol"] == "PETR4"
ATT/tests/test_legacy_robo_legs_fallback.py:113:    assert legs[0]["strike"] == 100.0
ATT/tests/test_legacy_robo_legs_fallback.py:114:    assert legs[0]["quantity"] == 2
ATT/tests/test_legacy_robo_legs_fallback.py:115:    assert meta["legs_source"] == "legacy_fallback"
ATT/tests/test_legacy_structure_legs_importer.py:7:from services.legacy_structure_legs_importer import LegacyStructureLegsImporter
ATT/tests/test_legacy_structure_legs_importer.py:27:        CREATE TABLE structure_legs (
ATT/tests/test_legacy_structure_legs_importer.py:73:        INSERT INTO structure_legs (
ATT/tests/test_legacy_structure_legs_importer.py:90:class FakeLegacyStructureLegsReader:
ATT/tests/test_legacy_structure_legs_importer.py:91:    def __init__(self, legs):
ATT/tests/test_legacy_structure_legs_importer.py:92:        self.legs = legs
ATT/tests/test_legacy_structure_legs_importer.py:102:        return self.legs
ATT/tests/test_legacy_structure_legs_importer.py:105:def test_import_by_structure_id_replaces_legs_and_writes_audit_log(tmp_path):
ATT/tests/test_legacy_structure_legs_importer.py:113:    reader = FakeLegacyStructureLegsReader([
ATT/tests/test_legacy_structure_legs_importer.py:138:    importer = LegacyStructureLegsImporter(
ATT/tests/test_legacy_structure_legs_importer.py:151:        "legs_count": 2,
ATT/tests/test_legacy_structure_legs_importer.py:165:    legs = structure["legs"]
ATT/tests/test_legacy_structure_legs_importer.py:166:    assert [leg["symbol"] for leg in legs] == ["BOVAE195", "BOVAE200"]
ATT/tests/test_legacy_structure_legs_importer.py:167:    assert [leg["leg_order"] for leg in legs] == [1, 2]
ATT/tests/test_legacy_structure_legs_importer.py:168:    assert repo.count_legs(123) == 2
ATT/tests/test_legacy_structure_legs_importer.py:171:    assert audit[0]["action"] == "REPLACE_LEGS"
ATT/tests/test_legacy_structure_legs_importer.py:174:    assert after["legs_count"] == 2
ATT/tests/test_legacy_structure_legs_importer.py:178:def test_import_by_structure_id_raises_when_reader_returns_no_legs(tmp_path):
ATT/tests/test_legacy_structure_legs_importer.py:185:    reader = FakeLegacyStructureLegsReader([])
ATT/tests/test_legacy_structure_legs_importer.py:187:    importer = LegacyStructureLegsImporter(
ATT/tests/test_legacy_structure_legs_importer.py:194:        match=r"structure_id=123 sem legs legadas para importar",
ATT/tests/test_legacy_structure_legs_importer.py:201:    assert repo.count_legs(123) == 1
ATT/tests/test_legacy_structure_legs_importer.py:202:    assert repo.get_structure(123)["legs"][0]["symbol"] == "OLDLEG"
ATT/tests/test_legacy_structure_legs_importer.py:211:    reader = FakeLegacyStructureLegsReader([
ATT/tests/test_legacy_structure_legs_importer.py:225:    importer = LegacyStructureLegsImporter(
ATT/tests/test_legacy_structure_legs_importer_integration.py:4:from repositories.robo_legs_repository import (
ATT/tests/test_legacy_structure_legs_importer_integration.py:5:    RoboLegsRepoConfig,
ATT/tests/test_legacy_structure_legs_importer_integration.py:6:    RoboLegsRepository,
ATT/tests/test_legacy_structure_legs_importer_integration.py:9:from services.legacy_structure_legs_importer import LegacyStructureLegsImporter
ATT/tests/test_legacy_structure_legs_importer_integration.py:10:from services.legacy_structure_legs_reader import LegacyStructureLegsReader
ATT/tests/test_legacy_structure_legs_importer_integration.py:30:        CREATE TABLE structure_legs (
ATT/tests/test_legacy_structure_legs_importer_integration.py:50:        CREATE TABLE manual_analise_robo_legs (
ATT/tests/test_legacy_structure_legs_importer_integration.py:65:        CREATE TABLE rtd_analise_robo_legs (
ATT/tests/test_legacy_structure_legs_importer_integration.py:110:        INSERT INTO structure_legs (
ATT/tests/test_legacy_structure_legs_importer_integration.py:132:        INSERT INTO rtd_analise_robo_legs (
ATT/tests/test_legacy_structure_legs_importer_integration.py:151:        INSERT INTO manual_analise_robo_legs (
ATT/tests/test_legacy_structure_legs_importer_integration.py:176:    # RoboLegsRepository deve preferir MANUAL.
ATT/tests/test_legacy_structure_legs_importer_integration.py:182:    robo_legs_repo = RoboLegsRepository(
ATT/tests/test_legacy_structure_legs_importer_integration.py:183:        RoboLegsRepoConfig(app_db_path=str(db_path))
ATT/tests/test_legacy_structure_legs_importer_integration.py:186:    reader = LegacyStructureLegsReader(
ATT/tests/test_legacy_structure_legs_importer_integration.py:187:        robo_legs_repository=robo_legs_repo,
ATT/tests/test_legacy_structure_legs_importer_integration.py:190:    importer = LegacyStructureLegsImporter(
ATT/tests/test_legacy_structure_legs_importer_integration.py:203:        "legs_count": 1,
ATT/tests/test_legacy_structure_legs_importer_integration.py:210:    legs = structure["legs"]
ATT/tests/test_legacy_structure_legs_importer_integration.py:212:    assert len(legs) == 1
ATT/tests/test_legacy_structure_legs_importer_integration.py:214:    imported_leg = legs[0]
ATT/tests/test_legacy_structure_legs_importer_integration.py:231:    assert structures_repo.count_legs(123) == 1
ATT/tests/test_legacy_structure_legs_importer_integration.py:236:    assert audit[0]["action"] == "REPLACE_LEGS"
ATT/tests/test_legacy_structure_legs_importer_integration.py:240:    assert after["legs_count"] == 1
ATT/tests/test_legacy_structure_legs_reader.py:6:from services.legacy_structure_legs_reader import LegacyStructureLegsReader
ATT/tests/test_legacy_structure_legs_reader.py:9:class FakeRoboLegsRepository:
ATT/tests/test_legacy_structure_legs_reader.py:10:    def __init__(self, legs):
ATT/tests/test_legacy_structure_legs_reader.py:11:        self.legs = legs
ATT/tests/test_legacy_structure_legs_reader.py:14:    def get_legs_by_structure_id(self, structure_id, timestamp):
ATT/tests/test_legacy_structure_legs_reader.py:21:        return self.legs
ATT/tests/test_legacy_structure_legs_reader.py:24:def test_read_by_structure_id_maps_legacy_legs_to_structure_legs_payload():
ATT/tests/test_legacy_structure_legs_reader.py:25:    legacy_legs = [
ATT/tests/test_legacy_structure_legs_reader.py:46:    repo = FakeRoboLegsRepository(legacy_legs)
ATT/tests/test_legacy_structure_legs_reader.py:47:    reader = LegacyStructureLegsReader(robo_legs_repository=repo)
ATT/tests/test_legacy_structure_legs_reader.py:88:    legacy_legs = [
ATT/tests/test_legacy_structure_legs_reader.py:100:    reader = LegacyStructureLegsReader(
ATT/tests/test_legacy_structure_legs_reader.py:101:        robo_legs_repository=FakeRoboLegsRepository(legacy_legs)
ATT/tests/test_legacy_structure_legs_reader.py:127:        CREATE TABLE manual_analise_robo_legs (
ATT/tests/test_legacy_structure_legs_reader.py:142:        CREATE TABLE rtd_analise_robo_legs (
ATT/tests/test_legacy_structure_legs_reader.py:160:def test_read_by_structure_id_integrates_structure_alias_with_rtd_legs(tmp_path):
ATT/tests/test_legacy_structure_legs_reader.py:161:    from repositories.robo_legs_repository import (
ATT/tests/test_legacy_structure_legs_reader.py:162:        RoboLegsRepoConfig,
ATT/tests/test_legacy_structure_legs_reader.py:163:        RoboLegsRepository,
ATT/tests/test_legacy_structure_legs_reader.py:180:        INSERT INTO rtd_analise_robo_legs
ATT/tests/test_legacy_structure_legs_reader.py:199:    repo = RoboLegsRepository(
ATT/tests/test_legacy_structure_legs_reader.py:200:        RoboLegsRepoConfig(app_db_path=str(db_path))
ATT/tests/test_legacy_structure_legs_reader.py:202:    reader = LegacyStructureLegsReader(robo_legs_repository=repo)
ATT/tests/test_legacy_structure_legs_reader.py:225:    from repositories.robo_legs_repository import (
ATT/tests/test_legacy_structure_legs_reader.py:226:        RoboLegsRepoConfig,
ATT/tests/test_legacy_structure_legs_reader.py:227:        RoboLegsRepository,
ATT/tests/test_legacy_structure_legs_reader.py:244:    repo = RoboLegsRepository(
ATT/tests/test_legacy_structure_legs_reader.py:245:        RoboLegsRepoConfig(app_db_path=str(db_path))
ATT/tests/test_legacy_structure_legs_reader.py:247:    reader = LegacyStructureLegsReader(robo_legs_repository=repo)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:8:def _create_rtd_legs_table(conn):
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:11:        CREATE TABLE rtd_analise_robo_legs (
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:68:        INSERT INTO rtd_analise_robo_legs (
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:117:def test_get_rtd_option_quote_legs_enriches_base_rtd_leg_with_quote_cache(tmp_path):
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:121:        _create_rtd_legs_table(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:176:    legs = repo.get_rtd_option_quote_legs("BOVA11")
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:178:    assert len(legs) == 1
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:180:    leg = legs[0]
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:207:def test_get_rtd_option_quote_legs_returns_empty_list_when_cache_table_is_missing(tmp_path):
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:211:        _create_rtd_legs_table(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:217:    assert repo.get_rtd_option_quote_legs("BOVA11") == []
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:287:def test_get_rtd_option_quote_legs_ignores_orphan_quote_without_structural_leg(tmp_path):
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:291:        _create_rtd_legs_table(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:308:    assert repo.get_rtd_option_quote_legs("BOVA11") == []
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:311:def test_get_rtd_option_quote_legs_uses_latest_quote_when_cache_has_duplicates(tmp_path):
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:315:        _create_rtd_legs_table(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:353:    legs = repo.get_rtd_option_quote_legs("BOVA11")
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:355:    assert len(legs) == 1
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:357:    leg = legs[0]
ATT/tests/test_market_snapshot_selector.py:21:    def get_manual_legs(self, ref):
ATT/tests/test_market_snapshot_selector.py:24:    def get_rtd_option_quote_legs(self, ref):
ATT/tests/test_market_snapshot_selector.py:27:    def get_rtd_legs(self, ref):
ATT/tests/test_market_snapshot_selector.py:46:    assert result.legs == [quote_leg]
ATT/tests/test_market_snapshot_selector.py:67:    assert result.legs == [manual_leg]
ATT/tests/test_orchestrator_run_methods.py:43:def _make_request(*, spot=50.0, underlying="PETR4", legs=None):
ATT/tests/test_orchestrator_run_methods.py:44:    if legs is None:
ATT/tests/test_orchestrator_run_methods.py:45:        legs = [_make_leg()]
ATT/tests/test_orchestrator_run_methods.py:51:        legs=legs,
ATT/tests/test_orchestrator_run_methods.py:80:        assert isinstance(s["legs"], list)
ATT/tests/test_orchestrator_run_methods.py:81:        assert len(s["legs"]) == 1
ATT/tests/test_orchestrator_run_methods.py:85:        req = _make_request(legs=[leg])
ATT/tests/test_orchestrator_run_methods.py:86:        legs = _request_to_payoff_dict(req)["structure"]["legs"]
ATT/tests/test_orchestrator_run_methods.py:87:        assert legs[0]["strike"] == 110.0
ATT/tests/test_orchestrator_run_methods.py:88:        assert legs[0]["option_type"] == "put"
ATT/tests/test_orchestrator_run_methods.py:89:        assert legs[0]["position_side"] == "short"
ATT/tests/test_orchestrator_run_methods.py:108:    def test_multiplas_legs(self):
ATT/tests/test_orchestrator_run_methods.py:109:        legs = [
ATT/tests/test_orchestrator_run_methods.py:113:        req = _make_request(legs=legs)
ATT/tests/test_orchestrator_run_methods.py:114:        result_legs = _request_to_payoff_dict(req)["structure"]["legs"]
ATT/tests/test_orchestrator_run_methods.py:115:        assert len(result_legs) == 2
ATT/tests/test_orchestrator_run_methods.py:116:        assert result_legs[1]["strike"] == 110.0
ATT/tests/test_orchestrator_run_methods.py:257:        req = _make_request(spot=50.0, legs=[leg])
ATT/tests/test_payoff_canonical.py:10:            "legs": [
ATT/tests/test_payoff_canonical.py:32:            "legs_source": "canonical",
ATT/tests/test_payoff_canonical.py:43:    assert result["input_meta"]["legs_source"] == "canonical"
ATT/tests/test_payoff_chart.py:327:    def test_update_chart_saves_points(self):
ATT/tests/test_payoff_chart.py:332:    def test_update_chart_saves_decision_data(self):
ATT/tests/test_payoff_pricing_engine.py:16:        "legs": [
ATT/tests/test_payoff_pricing_engine.py:36:    assert result["metrics"]["number_of_legs"] == 1
ATT/tests/test_payoff_pricing_engine.py:65:        "legs": [
ATT/tests/test_payoff_pricing_engine.py:90:def test_run_raises_when_legs_are_missing():
ATT/tests/test_payoff_pricing_engine.py:100:        "legs": [],
ATT/tests/test_payoff_pricing_engine.py:103:    with pytest.raises(ValueError, match="pricing_payload.legs is required"):
ATT/tests/test_payoff_pricing_engine.py:117:        "legs": [
ATT/tests/test_pricing_execution_persistence_service.py:10:    def save_execution(
ATT/tests/test_pricing_execution_persistence_service.py:18:        number_of_legs,
ATT/tests/test_pricing_execution_persistence_service.py:30:                "number_of_legs": number_of_legs,
ATT/tests/test_pricing_execution_persistence_service.py:42:def test_persist_execution_extracts_fields_and_saves_record():
ATT/tests/test_pricing_execution_persistence_service.py:57:                "number_of_legs": 2,
ATT/tests/test_pricing_execution_persistence_service.py:80:            "number_of_legs": 2,
ATT/tests/test_pricing_execution_persistence_service.py:125:            "number_of_legs": None,
ATT/tests/test_pricing_execution_persistence_service.py:195:            "legs_count": 2,
ATT/tests/test_pricing_execution_persistence_service.py:197:        "legs": [
ATT/tests/test_pricing_execution_persistence_service.py:214:                "number_of_legs": 1,
ATT/tests/test_pricing_execution_persistence_service.py:255:        "number_of_legs": 1,
ATT/tests/test_pricing_execution_persistence_service.py:270:    assert call["legs"] == pricing_payload["legs"]
ATT/tests/test_pricing_execution_persistence_service.py:319:            "legs": [],
ATT/tests/test_pricing_execution_persistence_service.py:356:            "legs": [],
ATT/tests/test_pricing_execution_query_service.py:27:    number_of_legs=None,
ATT/tests/test_pricing_execution_query_service.py:30:    nested_number_of_legs: int = 2,
ATT/tests/test_pricing_execution_query_service.py:44:        "number_of_legs": number_of_legs,
ATT/tests/test_pricing_execution_query_service.py:55:                    "number_of_legs": nested_number_of_legs,
ATT/tests/test_pricing_execution_query_service.py:103:            number_of_legs=9,
ATT/tests/test_pricing_execution_query_service.py:106:            nested_number_of_legs=2,
ATT/tests/test_pricing_execution_query_service.py:118:    assert summaries[0]["number_of_legs"] == 9
ATT/tests/test_pricing_execution_query_service.py:127:            number_of_legs=None,
ATT/tests/test_pricing_execution_query_service.py:130:            nested_number_of_legs=4,
ATT/tests/test_pricing_execution_query_service.py:142:    assert summaries[0]["number_of_legs"] == 4
ATT/tests/test_pricing_execution_service.py:33:        "legs": [],
ATT/tests/test_pricing_execution_service.py:39:        "metrics": {"number_of_legs": 0, "total_quantity": 0},
ATT/tests/test_pricing_execution_service.py:69:        "legs": [{"side": "LONG"}],
ATT/tests/test_pricing_executions_repository.py:24:            number_of_legs     INTEGER,
ATT/tests/test_pricing_executions_repository.py:36:def test_save_execution_persists_record_with_payload_and_result(tmp_path):
ATT/tests/test_pricing_executions_repository.py:43:        "legs": [],
ATT/tests/test_pricing_executions_repository.py:52:    record = repository.save_execution(
ATT/tests/test_pricing_executions_repository.py:58:        number_of_legs=0,
ATT/tests/test_pricing_executions_repository.py:70:    assert record["number_of_legs"] == 0
ATT/tests/test_pricing_executions_repository.py:78:def test_save_execution_accepts_none_pricing_payload(tmp_path):
ATT/tests/test_pricing_executions_repository.py:88:    record = repository.save_execution(
ATT/tests/test_pricing_executions_repository.py:105:def test_save_execution_raises_when_result_is_missing(tmp_path):
ATT/tests/test_pricing_executions_repository.py:109:        repository.save_execution(
ATT/tests/test_pricing_executions_repository.py:118:    repository.save_execution(
ATT/tests/test_pricing_executions_repository.py:126:    repository.save_execution(
ATT/tests/test_pricing_input_service.py:32:            "legs": [],
ATT/tests/test_pricing_payload_adapter.py:14:                "legs": [
ATT/tests/test_pricing_payload_adapter.py:41:    def test_should_map_legs_to_pricing_shape(self):
ATT/tests/test_pricing_payload_adapter.py:47:                "legs": [
ATT/tests/test_pricing_payload_adapter.py:70:        self.assertEqual(len(payload["legs"]), 1)
ATT/tests/test_pricing_payload_adapter.py:71:        self.assertEqual(payload["legs"][0]["side"], "SHORT")
ATT/tests/test_pricing_payload_adapter.py:72:        self.assertEqual(payload["legs"][0]["option_type"], "PUT")
ATT/tests/test_pricing_payload_adapter.py:73:        self.assertEqual(payload["legs"][0]["symbol"], "BOVAQ195")
ATT/tests/test_pricing_payload_adapter.py:74:        self.assertEqual(payload["legs"][0]["instrument_type"], "OPTION")
ATT/tests/test_pricing_payload_adapter.py:94:                        "legs": [
ATT/tests/test_pricing_payload_adapter.py:117:                self.assertEqual(payload["legs"][0]["side"], expected_side)
ATT/tests/test_robo_legs_repository.py:3:from repositories.robo_legs_repository import RoboLegsRepoConfig, RoboLegsRepository
ATT/tests/test_robo_legs_repository.py:11:        CREATE TABLE manual_analise_robo_legs (
ATT/tests/test_robo_legs_repository.py:25:        CREATE TABLE rtd_analise_robo_legs (
ATT/tests/test_robo_legs_repository.py:42:def test_get_legs_prefers_manual_over_rtd(tmp_path):
ATT/tests/test_robo_legs_repository.py:49:        INSERT INTO manual_analise_robo_legs
ATT/tests/test_robo_legs_repository.py:54:        INSERT INTO rtd_analise_robo_legs
ATT/tests/test_robo_legs_repository.py:61:    repo = RoboLegsRepository(RoboLegsRepoConfig(app_db_path=str(db_path)))
ATT/tests/test_robo_legs_repository.py:62:    legs = repo.get_legs("AB1", "2026-05-19 10:00:00")
ATT/tests/test_robo_legs_repository.py:64:    assert len(legs) == 1
ATT/tests/test_robo_legs_repository.py:65:    assert legs[0].id == 1
ATT/tests/test_robo_legs_repository.py:66:    assert legs[0].aba == "AB1"
ATT/tests/test_robo_legs_repository.py:67:    assert legs[0].cv == "C"
ATT/tests/test_robo_legs_repository.py:68:    assert legs[0].call_put == "CALL"
ATT/tests/test_robo_legs_repository.py:69:    assert legs[0].ativo == "PETR4"
ATT/tests/test_robo_legs_repository.py:72:def test_get_legs_falls_back_to_rtd_when_manual_empty(tmp_path):
ATT/tests/test_robo_legs_repository.py:79:        INSERT INTO rtd_analise_robo_legs
ATT/tests/test_robo_legs_repository.py:86:    repo = RoboLegsRepository(RoboLegsRepoConfig(app_db_path=str(db_path)))
ATT/tests/test_robo_legs_repository.py:87:    legs = repo.get_legs("AB2", "2026-05-19 10:00:00")
ATT/tests/test_robo_legs_repository.py:89:    assert len(legs) == 1
ATT/tests/test_robo_legs_repository.py:90:    assert legs[0].id == 2
ATT/tests/test_robo_legs_repository.py:91:    assert legs[0].cv == "V"
ATT/tests/test_robo_legs_repository.py:92:    assert legs[0].call_put == "PUT"
ATT/tests/test_robo_legs_repository.py:93:    assert legs[0].ativo == "VALE3"
ATT/tests/test_robo_legs_repository.py:103:        INSERT INTO manual_analise_robo_legs
ATT/tests/test_robo_legs_repository.py:110:    repo = RoboLegsRepository(RoboLegsRepoConfig(app_db_path=str(db_path)))
ATT/tests/test_robo_legs_repository.py:123:        INSERT INTO manual_analise_robo_legs
ATT/tests/test_robo_legs_repository.py:128:        INSERT INTO manual_analise_robo_legs
ATT/tests/test_robo_legs_repository.py:133:        INSERT INTO rtd_analise_robo_legs
ATT/tests/test_robo_legs_repository.py:140:    repo = RoboLegsRepository(RoboLegsRepoConfig(app_db_path=str(db_path)))
ATT/tests/test_robo_legs_repository.py:153:        INSERT INTO manual_analise_robo_legs
ATT/tests/test_robo_legs_repository.py:158:        INSERT INTO rtd_analise_robo_legs
ATT/tests/test_robo_legs_repository.py:165:    repo = RoboLegsRepository(RoboLegsRepoConfig(app_db_path=str(db_path)))
ATT/tests/test_robo_legs_repository.py:172:    repo = RoboLegsRepository()
ATT/tests/test_robo_legs_service.py:6:from services.robo_legs_service import RoboLegsService
ATT/tests/test_robo_legs_service.py:10:    def __init__(self, legs):
ATT/tests/test_robo_legs_service.py:11:        self._legs = legs
ATT/tests/test_robo_legs_service.py:13:    def get_legs(self, aba, timestamp):
ATT/tests/test_robo_legs_service.py:14:        return self._legs
ATT/tests/test_robo_legs_service.py:32:def test_get_legs_returns_repo_legs_when_validation_disabled():
ATT/tests/test_robo_legs_service.py:33:    legs = [make_valid_leg()]
ATT/tests/test_robo_legs_service.py:34:    service = RoboLegsService(repo=FakeRepo(legs))
ATT/tests/test_robo_legs_service.py:36:    result = service.get_legs("BOVA11", datetime(2026, 5, 16, 10, 0, 0), validate=False)
ATT/tests/test_robo_legs_service.py:38:    assert result == legs
ATT/tests/test_robo_legs_service.py:41:def test_get_legs_returns_repo_legs_when_validation_passes():
ATT/tests/test_robo_legs_service.py:42:    legs = [make_valid_leg()]
ATT/tests/test_robo_legs_service.py:43:    service = RoboLegsService(repo=FakeRepo(legs))
ATT/tests/test_robo_legs_service.py:45:    result = service.get_legs("BOVA11", datetime(2026, 5, 16, 10, 0, 0), validate=True)
ATT/tests/test_robo_legs_service.py:47:    assert result == legs
ATT/tests/test_robo_legs_service.py:50:def test_get_legs_raises_value_error_when_validation_fails():
ATT/tests/test_robo_legs_service.py:63:    service = RoboLegsService(repo=FakeRepo([invalid_leg]))
ATT/tests/test_robo_legs_service.py:65:    with pytest.raises(ValueError, match=r"Legs inválidas: invalid_cv field=cv aba=BOVA11"):
ATT/tests/test_robo_legs_service.py:66:        service.get_legs("BOVA11", datetime(2026, 5, 16, 10, 0, 0), validate=True)
ATT/tests/test_robo_legs_status_repository.py:3:from repositories.robo_legs_status_repository import (
ATT/tests/test_robo_legs_status_repository.py:4:    RoboLegsStatusRepoConfig,
ATT/tests/test_robo_legs_status_repository.py:5:    RoboLegsStatusRepository,
ATT/tests/test_robo_legs_status_repository.py:14:    conn.execute("CREATE TABLE manual_analise_robo_legs (aba TEXT, timestamp TEXT)")
ATT/tests/test_robo_legs_status_repository.py:15:    conn.execute("CREATE TABLE rtd_analise_robo_legs (aba TEXT, timestamp TEXT)")
ATT/tests/test_robo_legs_status_repository.py:18:        "INSERT INTO manual_analise_robo_legs (aba, timestamp) VALUES (?, ?)",
ATT/tests/test_robo_legs_status_repository.py:22:        "INSERT INTO manual_analise_robo_legs (aba, timestamp) VALUES (?, ?)",
ATT/tests/test_robo_legs_status_repository.py:26:        "INSERT INTO rtd_analise_robo_legs (aba, timestamp) VALUES (?, ?)",
ATT/tests/test_robo_legs_status_repository.py:32:    repo = RoboLegsStatusRepository(
ATT/tests/test_robo_legs_status_repository.py:33:        RoboLegsStatusRepoConfig(app_db_path=str(db_path))
ATT/tests/test_robo_legs_status_repository.py:47:    conn.execute("CREATE TABLE manual_analise_robo_legs (aba TEXT, timestamp TEXT)")
ATT/tests/test_robo_legs_status_repository.py:48:    conn.execute("CREATE TABLE rtd_analise_robo_legs (aba TEXT, timestamp TEXT)")
ATT/tests/test_robo_legs_status_repository.py:52:    repo = RoboLegsStatusRepository(
ATT/tests/test_robo_legs_status_repository.py:53:        RoboLegsStatusRepoConfig(app_db_path=str(db_path))
ATT/tests/test_robo_legs_status_service.py:6:from dto.robo_legs_status_dto import DataFreshness
ATT/tests/test_robo_legs_status_service.py:7:from services.robo_legs_status_service import (
ATT/tests/test_robo_legs_status_service.py:8:    RoboLegsFreshnessConfig,
ATT/tests/test_robo_legs_status_service.py:9:    RoboLegsStatusService,
ATT/tests/test_robo_legs_status_service.py:29:    service = RoboLegsStatusService(
ATT/tests/test_robo_legs_status_service.py:32:        freshness=RoboLegsFreshnessConfig(default_ttl_seconds=120),
ATT/tests/test_robo_legs_status_service.py:52:    service = RoboLegsStatusService(
ATT/tests/test_robo_legs_status_service.py:71:    service = RoboLegsStatusService(
ATT/tests/test_robo_legs_status_service.py:90:    service = RoboLegsStatusService(
ATT/tests/test_robo_legs_status_service.py:106:    service = RoboLegsStatusService(
ATT/tests/test_robo_legs_status_service.py:121:    service = RoboLegsStatusService(
ATT/tests/test_robo_legs_status_service.py:124:        freshness=RoboLegsFreshnessConfig(default_ttl_seconds=30),
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:31:class FakeRtdRoboLegsService:
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:35:    def get_legs(self, aba, timestamp):
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:51:def test_rtd_legacy_fallback_can_feed_pricing_payload_when_no_canonical_legs_exist():
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:57:        "legs": [],
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:63:        robo_legs_service=FakeRtdRoboLegsService(),
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:64:        prefer_canonical_legs=True,
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:65:        enable_legacy_legs_fallback=True,
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:73:    assert canonical_input["meta"]["legs_source"] == "legacy_fallback"
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:79:    canonical_leg = canonical_input["structure"]["legs"][0]
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:100:    assert pricing_payload["legs"] == [
ATT/tests/test_structure_analysis_service.py:32:                "legs": [
ATT/tests/test_structure_analysis_service.py:64:                "legs_source": "canonical",
ATT/tests/test_structure_analysis_service.py:93:                "legs": [],
ATT/tests/test_structure_analysis_service.py:104:                "legs_source": "canonical",
ATT/tests/test_structure_analysis_service.py:446:                "legs": [
ATT/tests/test_structure_analysis_service.py:490:                "legs_source": "canonical",
ATT/tests/test_structure_analysis_service.py:637:    assert len(structure_metrics["legs"]) == 2
ATT/tests/test_structure_editor_dialog.py:3:Testes unitarios de StructureEditorDialog
ATT/tests/test_structure_editor_dialog.py:21:    from UI.components.structure_editor_dialog import StructureEditorDialog
ATT/tests/test_structure_editor_dialog.py:42:        p = patch.object(StructureEditorDialog, name, lambda *a, **kw: None, create=True)
ATT/tests/test_structure_editor_dialog.py:56:def _make_bare_dialog() -> "StructureEditorDialog":
ATT/tests/test_structure_editor_dialog.py:58:    obj = object.__new__(StructureEditorDialog)
ATT/tests/test_structure_editor_dialog.py:59:    obj._legs_rows = []
ATT/tests/test_structure_editor_dialog.py:61:    obj.saved = False
ATT/tests/test_structure_editor_dialog.py:68:    repo.create_structure.return_value = create_return
ATT/tests/test_structure_editor_dialog.py:76:@unittest.skipUnless(_IMPORT_OK, "StructureEditorDialog nao importavel")
ATT/tests/test_structure_editor_dialog.py:77:class TestBuildLegsPayload(unittest.TestCase):
ATT/tests/test_structure_editor_dialog.py:79:    def _dialog(self, legs):
ATT/tests/test_structure_editor_dialog.py:81:        d._legs_rows = legs
ATT/tests/test_structure_editor_dialog.py:85:        self.assertEqual(self._dialog([])._build_legs_payload(), [])
ATT/tests/test_structure_editor_dialog.py:88:        r = self._dialog([{"strike": 100.0}])._build_legs_payload()
ATT/tests/test_structure_editor_dialog.py:92:        legs = [{"strike": 100.0}, {"strike": 110.0}, {"strike": 90.0}]
ATT/tests/test_structure_editor_dialog.py:93:        ordens = [r["leg_order"] for r in self._dialog(legs)._build_legs_payload()]
ATT/tests/test_structure_editor_dialog.py:97:        legs = [{
ATT/tests/test_structure_editor_dialog.py:102:        r = self._dialog(legs)._build_legs_payload()[0]
ATT/tests/test_structure_editor_dialog.py:107:    def test_nao_modifica_legs_rows_original(self):
ATT/tests/test_structure_editor_dialog.py:108:        legs = [{"strike": 100.0}]
ATT/tests/test_structure_editor_dialog.py:109:        d = self._dialog(legs)
ATT/tests/test_structure_editor_dialog.py:110:        d._build_legs_payload()
ATT/tests/test_structure_editor_dialog.py:111:        self.assertNotIn("leg_order", d._legs_rows[0])
ATT/tests/test_structure_editor_dialog.py:113:    def test_duas_legs_sem_contaminar_indices(self):
ATT/tests/test_structure_editor_dialog.py:114:        legs = [{"strike": 100.0}, {"strike": 110.0}]
ATT/tests/test_structure_editor_dialog.py:115:        r = self._dialog(legs)._build_legs_payload()
ATT/tests/test_structure_editor_dialog.py:126:@unittest.skipUnless(_IMPORT_OK, "StructureEditorDialog nao importavel")
ATT/tests/test_structure_editor_dialog.py:144:        return StructureEditorDialog(
ATT/tests/test_structure_editor_dialog.py:155:            "notes": "teste", "legs": [],
ATT/tests/test_structure_editor_dialog.py:164:    def test_carrega_legs_em_legs_rows(self):
ATT/tests/test_structure_editor_dialog.py:173:            "legs": [leg],
ATT/tests/test_structure_editor_dialog.py:176:        self.assertEqual(len(dlg._legs_rows), 1)
ATT/tests/test_structure_editor_dialog.py:177:        self.assertEqual(dlg._legs_rows[0]["strike"], 195.0)
ATT/tests/test_structure_editor_dialog.py:182:            StructureEditorDialog(
ATT/tests/test_structure_editor_dialog.py:192:# Bloco 3 -- TestCmdSaveCreate
ATT/tests/test_structure_editor_dialog.py:195:@unittest.skipUnless(_IMPORT_OK, "StructureEditorDialog nao importavel")
ATT/tests/test_structure_editor_dialog.py:196:class TestCmdSaveCreate(unittest.TestCase):
ATT/tests/test_structure_editor_dialog.py:214:        return StructureEditorDialog(
ATT/tests/test_structure_editor_dialog.py:222:    def test_create_structure_chamado_com_campos_corretos(self):
ATT/tests/test_structure_editor_dialog.py:230:        dlg._cmd_save()
ATT/tests/test_structure_editor_dialog.py:232:        self.mock_repo.create_structure_with_legs.assert_called_once()
ATT/tests/test_structure_editor_dialog.py:233:        args, _kwargs = self.mock_repo.create_structure_with_legs.call_args
ATT/tests/test_structure_editor_dialog.py:244:    def test_replace_legs_chamado_apos_create(self):
ATT/tests/test_structure_editor_dialog.py:249:        dlg._legs_rows = [{
ATT/tests/test_structure_editor_dialog.py:255:        dlg._cmd_save()
ATT/tests/test_structure_editor_dialog.py:257:        self.mock_repo.create_structure_with_legs.assert_called_once()
ATT/tests/test_structure_editor_dialog.py:258:        args, _kwargs = self.mock_repo.create_structure_with_legs.call_args
ATT/tests/test_structure_editor_dialog.py:261:        legs_arg = args[1]
ATT/tests/test_structure_editor_dialog.py:265:        self.assertEqual(len(legs_arg), 1)
ATT/tests/test_structure_editor_dialog.py:266:        self.assertEqual(legs_arg[0]["position_side"], "COMPRADO")
ATT/tests/test_structure_editor_dialog.py:267:        self.assertEqual(legs_arg[0]["option_type"], "CALL")
ATT/tests/test_structure_editor_dialog.py:268:        self.assertEqual(legs_arg[0]["strike"], 100.0)
ATT/tests/test_structure_editor_dialog.py:270:    def test_saved_true_apos_sucesso(self):
ATT/tests/test_structure_editor_dialog.py:275:        self.assertFalse(dlg.saved)
ATT/tests/test_structure_editor_dialog.py:276:        dlg._cmd_save()
ATT/tests/test_structure_editor_dialog.py:277:        self.assertTrue(dlg.saved)
ATT/tests/test_structure_editor_dialog.py:284:            dlg._cmd_save()
ATT/tests/test_structure_editor_dialog.py:285:        self.mock_repo.create_structure.assert_not_called()
ATT/tests/test_structure_editor_dialog.py:286:        self.assertFalse(dlg.saved)
ATT/tests/test_structure_editor_dialog.py:293:            dlg._cmd_save()
ATT/tests/test_structure_editor_dialog.py:294:        self.mock_repo.create_structure.assert_not_called()
ATT/tests/test_structure_editor_dialog.py:295:        self.assertFalse(dlg.saved)
ATT/tests/test_structure_editor_dialog.py:299:# Bloco 4 -- TestCmdSaveUpdate
ATT/tests/test_structure_editor_dialog.py:302:@unittest.skipUnless(_IMPORT_OK, "StructureEditorDialog nao importavel")
ATT/tests/test_structure_editor_dialog.py:303:class TestCmdSaveUpdate(unittest.TestCase):
ATT/tests/test_structure_editor_dialog.py:324:            "legs": [],
ATT/tests/test_structure_editor_dialog.py:326:        return StructureEditorDialog(
ATT/tests/test_structure_editor_dialog.py:333:    def test_update_structure_chamado_com_structure_id_correto(self):
ATT/tests/test_structure_editor_dialog.py:339:        dlg._cmd_save()
ATT/tests/test_structure_editor_dialog.py:341:        self.mock_repo.update_structure.assert_called_once()
ATT/tests/test_structure_editor_dialog.py:342:        sid_arg = self.mock_repo.update_structure.call_args[0][0]
ATT/tests/test_structure_editor_dialog.py:351:        dlg._cmd_save()
ATT/tests/test_structure_editor_dialog.py:353:        self.mock_repo.create_structure.assert_not_called()
ATT/tests/test_structure_editor_dialog.py:355:    def test_replace_legs_usa_structure_id_existente(self):
ATT/tests/test_structure_editor_dialog.py:360:        dlg._legs_rows = []
ATT/tests/test_structure_editor_dialog.py:362:        dlg._cmd_save()
ATT/tests/test_structure_editor_dialog.py:364:        self.mock_repo.replace_legs.assert_called_once_with(7, [])
ATT/tests/test_structure_editor_dialog.py:371:class TestStructureEditorDialogStaticChecks(unittest.TestCase):
ATT/tests/test_structure_editor_dialog.py:376:            "..", "..", "UI", "components", "structure_editor_dialog.py"
ATT/tests/test_structure_editor_dialog.py:388:        for metodo in ("_cmd_save", "_load_existing", "_build_legs_payload", "_build_ui"):
ATT/tests/test_structure_editor_dialog.py:390:                hasattr(StructureEditorDialog, metodo),
ATT/tests/test_structure_editor_dialog.py:391:                f"{metodo} ausente em StructureEditorDialog"
ATT/tests/test_structure_editor_dialog.py:397:        sig = inspect.signature(StructureEditorDialog.__init__)
ATT/tests/test_structure_editor_dialog.py:406:        sig = inspect.signature(StructureEditorDialog.__init__)
ATT/tests/test_structure_editor_dialog.py:409:            "StructureEditorDialog.__init__ deve aceitar _repo=None para injecao de dependencia"
ATT/tests/test_structure_editor_dialog.py:416:            "..", "..", "UI", "components", "structure_editor_dialog.py"
ATT/tests/test_structure_editor_dialog.py:436:def test_build_legs_payload_normaliza_position_side_legado_long_short():
ATT/tests/test_structure_editor_dialog.py:437:    dlg = object.__new__(StructureEditorDialog)
ATT/tests/test_structure_editor_dialog.py:438:    dlg._legs_rows = [
ATT/tests/test_structure_editor_dialog.py:463:    payload = dlg._build_legs_payload()
ATT/tests/test_structure_editor_dialog.py:470:def test_build_legs_payload_normaliza_strike_com_virgula_para_float():
ATT/tests/test_structure_editor_dialog.py:471:    dlg = object.__new__(StructureEditorDialog)
ATT/tests/test_structure_editor_dialog.py:472:    dlg._legs_rows = [
ATT/tests/test_structure_editor_dialog.py:486:    payload = dlg._build_legs_payload()
ATT/tests/test_structure_editor_dialog.py:492:def test_build_legs_payload_normaliza_strike_com_ponto_para_float():
ATT/tests/test_structure_editor_dialog.py:493:    dlg = object.__new__(StructureEditorDialog)
ATT/tests/test_structure_editor_dialog.py:494:    dlg._legs_rows = [
ATT/tests/test_structure_editor_dialog.py:508:    payload = dlg._build_legs_payload()
ATT/tests/test_structure_editor_dialog.py:514:def test_build_legs_payload_nao_modifica_strike_original_ao_normalizar():
ATT/tests/test_structure_editor_dialog.py:515:    dlg = object.__new__(StructureEditorDialog)
ATT/tests/test_structure_editor_dialog.py:527:    dlg._legs_rows = [original_leg]
ATT/tests/test_structure_editor_dialog.py:529:    payload = dlg._build_legs_payload()
ATT/tests/test_structure_editor_dialog.py:534:# FASE_3A4_TESTS_STRUCTURE_EDITOR_DIALOG
ATT/tests/test_structure_editor_dialog.py:536:def test_build_legs_payload_normaliza_premium_com_virgula_para_float():
ATT/tests/test_structure_editor_dialog.py:537:    dlg = object.__new__(StructureEditorDialog)
ATT/tests/test_structure_editor_dialog.py:538:    dlg._legs_rows = [
ATT/tests/test_structure_editor_dialog.py:552:    payload = dlg._build_legs_payload()
ATT/tests/test_structure_editor_dialog.py:558:def test_build_legs_payload_normaliza_multiplier_com_virgula_para_float():
ATT/tests/test_structure_editor_dialog.py:559:    dlg = object.__new__(StructureEditorDialog)
ATT/tests/test_structure_editor_dialog.py:560:    dlg._legs_rows = [
ATT/tests/test_structure_editor_dialog.py:574:    payload = dlg._build_legs_payload()
ATT/tests/test_structure_editor_dialog.py:580:def test_build_legs_payload_preserva_premium_none():
ATT/tests/test_structure_editor_dialog.py:581:    dlg = object.__new__(StructureEditorDialog)
ATT/tests/test_structure_editor_dialog.py:582:    dlg._legs_rows = [
ATT/tests/test_structure_editor_dialog.py:596:    payload = dlg._build_legs_payload()
ATT/tests/test_structure_editor_dialog.py:606:    dlg = object.__new__(StructureEditorDialog)
ATT/tests/test_structure_editor_dialog.py:607:    dlg._legs_rows = [
ATT/tests/test_structure_editor_dialog.py:624:def test_build_legs_payload_normaliza_quantity_inteiro_valido(quantity_value):
ATT/tests/test_structure_editor_dialog.py:627:    payload = dlg._build_legs_payload()
ATT/tests/test_structure_editor_dialog.py:634:def test_build_legs_payload_rejeita_quantity_invalido(quantity_value):
ATT/tests/test_structure_editor_dialog.py:641:        dlg._build_legs_payload()
ATT/tests/test_structure_editor_integration.py:5:Testes de integração: StructureEditorDialog x MainWindow.
ATT/tests/test_structure_editor_integration.py:125:        funcione em subclasses (StructureEditorDialog).
ATT/tests/test_structure_editor_integration.py:275:    from UI.components.structure_editor_dialog import StructureEditorDialog
ATT/tests/test_structure_editor_integration.py:277:    dlg = object.__new__(StructureEditorDialog)
ATT/tests/test_structure_editor_integration.py:279:    dlg.saved         = False
ATT/tests/test_structure_editor_integration.py:280:    dlg._legs_rows    = []
ATT/tests/test_structure_editor_integration.py:330:    def test_structure_editor_dialog_arquivo_existe(self):
ATT/tests/test_structure_editor_integration.py:332:            (PROJECT_ROOT / "UI" / "components" / "structure_editor_dialog.py").exists(),
ATT/tests/test_structure_editor_integration.py:333:            "UI/components/structure_editor_dialog.py não encontrado",
ATT/tests/test_structure_editor_integration.py:352:    def test_main_window_importa_structure_editor_dialog(self):
ATT/tests/test_structure_editor_integration.py:354:        self.assertIn("StructureEditorDialog", source)
ATT/tests/test_structure_editor_integration.py:362:        dlg._legs_rows = [
ATT/tests/test_structure_editor_integration.py:368:        payload = dlg._build_legs_payload()
ATT/tests/test_structure_editor_integration.py:377:        fake_dlg.saved = False
ATT/tests/test_structure_editor_integration.py:378:        with patch.object(mw_mod, "StructureEditorDialog", return_value=fake_dlg) as mock_cls:
ATT/tests/test_structure_editor_integration.py:385:    def test_load_nao_chamado_se_saved_false(self):
ATT/tests/test_structure_editor_integration.py:387:        dlg = _make_dialog(); dlg.saved = False
ATT/tests/test_structure_editor_integration.py:388:        with patch.object(mw_mod, "StructureEditorDialog", return_value=dlg):
ATT/tests/test_structure_editor_integration.py:392:    def test_load_chamado_se_saved_true(self):
ATT/tests/test_structure_editor_integration.py:394:        dlg = _make_dialog(); dlg.saved = True
ATT/tests/test_structure_editor_integration.py:395:        with patch.object(mw_mod, "StructureEditorDialog", return_value=dlg):
ATT/tests/test_structure_editor_integration.py:402:        dlg = _make_dialog(); dlg.saved = False
ATT/tests/test_structure_editor_integration.py:403:        with patch.object(mw_mod, "StructureEditorDialog", return_value=dlg) as mock_cls:
ATT/tests/test_structure_editor_integration.py:413:        dlg = _make_dialog(structure_id=7); dlg.saved = False
ATT/tests/test_structure_editor_integration.py:414:        with patch.object(mw_mod, "StructureEditorDialog", return_value=dlg) as mock_cls:
ATT/tests/test_structure_editor_integration.py:422:        dlg = _make_dialog(structure_id=7); dlg.saved = True
ATT/tests/test_structure_editor_integration.py:423:        with patch.object(mw_mod, "StructureEditorDialog", return_value=dlg):
ATT/tests/test_structure_editor_integration.py:429:        dlg = _make_dialog(structure_id=7); dlg.saved = False
ATT/tests/test_structure_editor_integration.py:430:        with patch.object(mw_mod, "StructureEditorDialog", return_value=dlg):
ATT/tests/test_structure_editor_integration.py:437:class TestCmdSave(unittest.TestCase):
ATT/tests/test_structure_editor_integration.py:448:    def test_saved_true_apos_criar(self):
ATT/tests/test_structure_editor_integration.py:450:        dlg._repo.create_structure.return_value = 10
ATT/tests/test_structure_editor_integration.py:451:        dlg._cmd_save()
ATT/tests/test_structure_editor_integration.py:452:        self.assertTrue(dlg.saved)
ATT/tests/test_structure_editor_integration.py:454:    def test_saved_true_apos_editar(self):
ATT/tests/test_structure_editor_integration.py:456:        dlg._cmd_save()
ATT/tests/test_structure_editor_integration.py:457:        self.assertTrue(dlg.saved)
ATT/tests/test_structure_editor_integration.py:461:        dlg._repo.create_structure.return_value = 20
ATT/tests/test_structure_editor_integration.py:462:        dlg._cmd_save()
ATT/tests/test_structure_editor_integration.py:467:        dlg._cmd_save()
ATT/tests/test_structure_editor_integration.py:468:        dlg._repo.create_structure.assert_not_called()
ATT/tests/test_structure_editor_integration.py:472:        dlg._repo.create_structure.return_value = 99
ATT/tests/test_structure_editor_integration.py:473:        dlg._cmd_save()
ATT/tests/test_structure_editor_integration.py:474:        dlg._repo.update_structure.assert_not_called()
ATT/tests/test_structure_editor_integration.py:477:    def test_replace_legs_sid_correto_criacao(self):
ATT/tests/test_structure_editor_integration.py:479:        dlg._repo.create_structure_with_legs.return_value = 77
ATT/tests/test_structure_editor_integration.py:481:        dlg._cmd_save()
ATT/tests/test_structure_editor_integration.py:483:        dlg._repo.create_structure_with_legs.assert_called_once()
ATT/tests/test_structure_editor_integration.py:484:        args, _kwargs = dlg._repo.create_structure_with_legs.call_args
ATT/tests/test_structure_editor_integration.py:490:        dlg._repo.create_structure.assert_not_called()
ATT/tests/test_structure_editor_integration.py:491:        dlg._repo.replace_legs.assert_not_called()
ATT/tests/test_structure_editor_integration.py:493:    def test_replace_legs_sid_correto_edicao(self):
ATT/tests/test_structure_editor_integration.py:495:        dlg._cmd_save()
ATT/tests/test_structure_editor_integration.py:496:        dlg._repo.replace_legs.assert_called_once_with(88, [])
ATT/tests/test_structure_editor_integration.py:498:    def test_saved_false_se_name_vazio(self):
ATT/tests/test_structure_editor_integration.py:501:            dlg._cmd_save()
ATT/tests/test_structure_editor_integration.py:502:        self.assertFalse(dlg.saved)
ATT/tests/test_structure_editor_integration.py:504:    def test_saved_false_se_underlying_vazio(self):
ATT/tests/test_structure_editor_integration.py:507:            dlg._cmd_save()
ATT/tests/test_structure_editor_integration.py:508:        self.assertFalse(dlg.saved)
ATT/tests/test_structure_editor_integration.py:513:        dlg._repo.create_structure_with_legs.side_effect = Exception("DB offline")
ATT/tests/test_structure_editor_integration.py:515:            dlg._cmd_save()
ATT/tests/test_structure_editor_integration.py:516:        self.assertFalse(dlg.saved)
ATT/tests/test_structure_editor_integration.py:518:class TestIntegracaoLegs(unittest.TestCase):
ATT/tests/test_structure_editor_integration.py:520:    def _dlg_com_legs(self, structure_id=None):
ATT/tests/test_structure_editor_integration.py:527:        dlg._legs_rows = [
ATT/tests/test_structure_editor_integration.py:540:    def test_replace_legs_recebe_2_legs(self):
ATT/tests/test_structure_editor_integration.py:541:        dlg = self._dlg_com_legs(structure_id=None)
ATT/tests/test_structure_editor_integration.py:542:        dlg._repo.create_structure_with_legs.return_value = 5
ATT/tests/test_structure_editor_integration.py:544:        dlg._cmd_save()
ATT/tests/test_structure_editor_integration.py:546:        dlg._repo.create_structure_with_legs.assert_called_once()
ATT/tests/test_structure_editor_integration.py:547:        args, _kwargs = dlg._repo.create_structure_with_legs.call_args
ATT/tests/test_structure_editor_integration.py:549:        legs_arg = args[1]
ATT/tests/test_structure_editor_integration.py:551:        self.assertEqual(len(legs_arg), 2)
ATT/tests/test_structure_editor_integration.py:553:    def test_legs_payload_tem_leg_order_sequencial(self):
ATT/tests/test_structure_editor_integration.py:554:        dlg = self._dlg_com_legs()
ATT/tests/test_structure_editor_integration.py:555:        payload = dlg._build_legs_payload()
ATT/tests/test_structure_editor_integration.py:559:    def test_legs_payload_preserva_position_side(self):
ATT/tests/test_structure_editor_integration.py:560:        dlg = self._dlg_com_legs()
ATT/tests/test_structure_editor_integration.py:561:        payload = dlg._build_legs_payload()
ATT/tests/test_structure_events_api.py:19:    "legs": [],
ATT/tests/test_structure_events_effective_state.py:25:        "legs": [
ATT/tests/test_structure_events_effective_state.py:71:    assert result["legs"][0]["quantity"] == 60
ATT/tests/test_structure_events_effective_state.py:72:    assert result["legs"][1]["quantity"] == 100
ATT/tests/test_structure_events_effective_state.py:73:    assert result["legs"][0]["_original_quantity"] == 100
ATT/tests/test_structure_events_effective_state.py:78:def test_apply_events_full_close_without_leg_id_zeros_all_legs():
ATT/tests/test_structure_events_effective_state.py:97:    assert result["legs"][0]["quantity"] == 0
ATT/tests/test_structure_events_effective_state.py:98:    assert result["legs"][1]["quantity"] == 0
ATT/tests/test_structure_events_effective_state.py:99:    assert result["legs"][0]["operational_status"] == "closed"
ATT/tests/test_structure_events_effective_state.py:100:    assert result["legs"][1]["operational_status"] == "closed"
ATT/tests/test_structure_events_effective_state.py:123:    assert result["legs"][0]["quantity"] == 100
ATT/tests/test_structure_events_effective_state.py:124:    assert result["legs"][1]["quantity"] == 100
ATT/tests/test_structure_events_effective_state.py:148:    assert result["legs"][0]["quantity"] == 100
ATT/tests/test_structure_events_effective_state.py:149:    assert result["legs"][1]["quantity"] == 75
ATT/tests/test_structure_events_effective_state.py:171:    assert result["legs"][0]["quantity"] == 100
ATT/tests/test_structure_events_effective_state.py:172:    assert result["legs"][1]["quantity"] == 0
ATT/tests/test_structure_events_effective_state.py:201:    assert result["legs"][0]["quantity"] == 100
ATT/tests/test_structure_events_effective_state.py:202:    assert result["legs"][1]["quantity"] == 100
ATT/tests/test_structure_events_repository.py:54:def create_structure_with_leg(structures_repo):
ATT/tests/test_structure_events_repository.py:55:    structure_id = structures_repo.create_structure(valid_structure_payload())
ATT/tests/test_structure_events_repository.py:61:    structure_id, leg_id = create_structure_with_leg(structures_repo)
ATT/tests/test_structure_events_repository.py:100:    structure_id = structures_repo.create_structure(valid_structure_payload())
ATT/tests/test_structure_events_repository.py:123:    structure_id, leg_id = create_structure_with_leg(structures_repo)
ATT/tests/test_structure_events_repository.py:150:    structure_id, leg_id = create_structure_with_leg(structures_repo)
ATT/tests/test_structure_events_repository.py:192:    structure_id, leg_id = create_structure_with_leg(structures_repo)
ATT/tests/test_structure_events_repository.py:214:    structure_id, leg_id = create_structure_with_leg(structures_repo)
ATT/tests/test_structure_events_repository.py:265:    first_structure_id, _first_leg_id = create_structure_with_leg(structures_repo)
ATT/tests/test_structure_events_repository.py:266:    second_structure_id = structures_repo.create_structure(
ATT/tests/test_structure_events_repository.py:310:    structure_id, leg_id = create_structure_with_leg(structures_repo)
ATT/tests/test_structure_input_mapper.py:10:        "legs": [
ATT/tests/test_structure_input_mapper.py:30:    assert len(result["legs"]) == 1
ATT/tests/test_structure_input_mapper.py:31:    assert result["legs"][0]["position_side"] == "COMPRADO"
ATT/tests/test_structure_input_mapper.py:32:    assert result["legs"][0]["option_type"] == "CALL"
ATT/tests/test_structure_input_mapper.py:33:    assert result["legs"][0]["symbol"] == "BOVAE195"
ATT/tests/test_structure_market_input_assembler.py:13:            "legs": [
ATT/tests/test_structure_market_input_assembler.py:51:            "legs": [],
ATT/tests/test_structure_market_input_assembler.py:86:            "legs": [],
ATT/tests/test_structure_metrics.py:39:            "legs": [
ATT/tests/test_structure_metrics.py:186:def test_compute_structure_metrics_should_aggregate_legs():
ATT/tests/test_structure_metrics.py:187:    legs = [
ATT/tests/test_structure_metrics.py:214:    result = compute_structure_metrics(legs, reference_date="2026-05-15")
ATT/tests/test_structure_metrics.py:225:    assert len(result["legs"]) == 2
ATT/tests/test_structure_metrics.py:233:            "legs": [
ATT/tests/test_structures_api.py:11:  - TestGetStructure     : campos obrigatórios na resposta; legs presente e é lista
ATT/tests/test_structures_api.py:38:    "legs": [
ATT/tests/test_structures_api.py:58:FAKE_SUMMARY = {k: v for k, v in FAKE_STRUCTURE.items() if k != "legs"}
ATT/tests/test_structures_api.py:61:# Testes dos endpoints de legs
ATT/tests/test_structures_api.py:77:REPLACE_LEGS_PAYLOAD = {
ATT/tests/test_structures_api.py:78:    "legs": [FAKE_LEG_PAYLOAD]
ATT/tests/test_structures_api.py:83:def client_legs(mock_repo):
ATT/tests/test_structures_api.py:84:    """Client com add_leg e replace_legs mockados."""
ATT/tests/test_structures_api.py:86:    mock_repo.replace_legs.return_value = None
ATT/tests/test_structures_api.py:105:    repo.create_structure.return_value = 1
ATT/tests/test_structures_api.py:108:    repo.update_structure.return_value = None
ATT/tests/test_structures_api.py:142:        repo.create_structure.return_value = 42
ATT/tests/test_structures_api.py:158:        payload = repo.create_structure.call_args[0][0]
ATT/tests/test_structures_api.py:170:        payload = repo.create_structure.call_args[0][0]
ATT/tests/test_structures_api.py:180:        repo.create_structure.assert_called_once()
ATT/tests/test_structures_api.py:188:        payload = repo.create_structure.call_args[0][0]
ATT/tests/test_structures_api.py:194:        repo.create_structure.side_effect = ValueError("nome duplicado")
ATT/tests/test_structures_api.py:204:        repo.create_structure.side_effect = ValueError("underlying_asset inválido")
ATT/tests/test_structures_api.py:273:    def test_summary_nao_contem_legs(self, client):
ATT/tests/test_structures_api.py:274:        """Listagem não deve retornar legs (otimização de payload)."""
ATT/tests/test_structures_api.py:277:        assert "legs" not in resp.json()[0]
ATT/tests/test_structures_api.py:321:    def test_campo_legs_presente(self, client):
ATT/tests/test_structures_api.py:324:        assert "legs" in resp.json()
ATT/tests/test_structures_api.py:326:    def test_legs_e_lista(self, client):
ATT/tests/test_structures_api.py:329:        assert isinstance(resp.json()["legs"], list)
ATT/tests/test_structures_api.py:331:    def test_legs_com_um_item(self, client):
ATT/tests/test_structures_api.py:334:        assert len(resp.json()["legs"]) == 1
ATT/tests/test_structures_api.py:340:        for campo in ("id", "name", "underlying_asset", "status", "legs", "created_at", "updated_at"):
ATT/tests/test_structures_api.py:375:        leg = resp.json()["legs"][0]
ATT/tests/test_structures_api.py:402:        args = repo.update_structure.call_args[0]
ATT/tests/test_structures_api.py:408:        args = repo.update_structure.call_args[0]
ATT/tests/test_structures_api.py:414:        args = repo.update_structure.call_args[0]
ATT/tests/test_structures_api.py:420:        args = repo.update_structure.call_args[0]
ATT/tests/test_structures_api.py:426:        args = repo.update_structure.call_args[0]
ATT/tests/test_structures_api.py:433:        args = repo.update_structure.call_args[0]
ATT/tests/test_structures_api.py:445:        payload = repo.update_structure.call_args[0][1]
ATT/tests/test_structures_api.py:469:        repo.update_structure.side_effect = ValueError("invalid status")
ATT/tests/test_structures_api.py:589:        leg = resp.json()["legs"][0]
ATT/tests/test_structures_api.py:595:        leg = resp.json()["legs"][0]
ATT/tests/test_structures_api.py:601:        leg = resp.json()["legs"][0]
ATT/tests/test_structures_archive_wiring.py:147:    def test_structure_editor_dialog_importado(self):
ATT/tests/test_structures_archive_wiring.py:148:        self.assertIn("StructureEditorDialog", _src(MAIN_WINDOW))
ATT/tests/test_structures_archive_wiring.py:156:    def test_dlg_saved_verificado(self):
ATT/tests/test_structures_archive_wiring.py:157:        self.assertIn("dlg.saved", _src(MAIN_WINDOW))
ATT/tests/test_structures_archive_wiring.py:542:                "CREATE TABLE IF NOT EXISTS structure_legs "
ATT/tests/test_structures_archive_wiring.py:579:                "CREATE TABLE IF NOT EXISTS structure_legs "
ATT/tests/test_structures_legs_endpoints.py:1:# Testes dos endpoints de legs de estruturas
ATT/tests/test_structures_legs_endpoints.py:3:Testes dos endpoints de legs na API de estruturas.
ATT/tests/test_structures_legs_endpoints.py:6:    POST   /structures/{id}/legs           — add_leg
ATT/tests/test_structures_legs_endpoints.py:7:    PUT    /structures/{id}/legs           — replace_legs (atômico)
ATT/tests/test_structures_legs_endpoints.py:8:    DELETE /structures/{id}/legs/{leg_id}  — remove_leg
ATT/tests/test_structures_legs_endpoints.py:37:REPLACE_LEGS_PAYLOAD = {
ATT/tests/test_structures_legs_endpoints.py:38:    "legs": [FAKE_LEG_PAYLOAD]
ATT/tests/test_structures_legs_endpoints.py:50:    "legs":              [],
ATT/tests/test_structures_legs_endpoints.py:63:    repo.replace_legs.return_value = None
ATT/tests/test_structures_legs_endpoints.py:72:def client_legs(mock_repo):
ATT/tests/test_structures_legs_endpoints.py:83:# POST /structures/{id}/legs
ATT/tests/test_structures_legs_endpoints.py:89:    def test_add_leg_retorna_201(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:90:        tc, _ = client_legs
ATT/tests/test_structures_legs_endpoints.py:91:        resp = tc.post("/structures/1/legs", json=FAKE_LEG_PAYLOAD)
ATT/tests/test_structures_legs_endpoints.py:94:    def test_add_leg_retorna_leg_id(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:95:        tc, _ = client_legs
ATT/tests/test_structures_legs_endpoints.py:96:        resp = tc.post("/structures/1/legs", json=FAKE_LEG_PAYLOAD)
ATT/tests/test_structures_legs_endpoints.py:99:    def test_add_leg_repo_chamado_com_structure_id_correto(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:100:        tc, repo = client_legs
ATT/tests/test_structures_legs_endpoints.py:101:        tc.post("/structures/1/legs", json=FAKE_LEG_PAYLOAD)
ATT/tests/test_structures_legs_endpoints.py:105:    def test_add_leg_repo_chamado_com_payload_correto(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:106:        tc, repo = client_legs
ATT/tests/test_structures_legs_endpoints.py:107:        tc.post("/structures/1/legs", json=FAKE_LEG_PAYLOAD)
ATT/tests/test_structures_legs_endpoints.py:112:    def test_add_leg_404_estrutura_inexistente(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:113:        tc, repo = client_legs
ATT/tests/test_structures_legs_endpoints.py:115:        resp = tc.post("/structures/999/legs", json=FAKE_LEG_PAYLOAD)
ATT/tests/test_structures_legs_endpoints.py:118:    def test_add_leg_400_quando_repo_levanta_value_error(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:119:        tc, repo = client_legs
ATT/tests/test_structures_legs_endpoints.py:121:        resp = tc.post("/structures/1/legs", json=FAKE_LEG_PAYLOAD)
ATT/tests/test_structures_legs_endpoints.py:125:    def test_add_leg_422_position_side_invalido(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:126:        tc, _ = client_legs
ATT/tests/test_structures_legs_endpoints.py:128:        resp = tc.post("/structures/1/legs", json=payload)
ATT/tests/test_structures_legs_endpoints.py:131:    def test_add_leg_422_option_type_invalido(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:132:        tc, _ = client_legs
ATT/tests/test_structures_legs_endpoints.py:134:        resp = tc.post("/structures/1/legs", json=payload)
ATT/tests/test_structures_legs_endpoints.py:137:    def test_add_leg_422_strike_zero(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:138:        tc, _ = client_legs
ATT/tests/test_structures_legs_endpoints.py:140:        resp = tc.post("/structures/1/legs", json=payload)
ATT/tests/test_structures_legs_endpoints.py:143:    def test_add_leg_422_quantity_zero(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:144:        tc, _ = client_legs
ATT/tests/test_structures_legs_endpoints.py:146:        resp = tc.post("/structures/1/legs", json=payload)
ATT/tests/test_structures_legs_endpoints.py:149:    def test_add_leg_aceita_leg_order_zero(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:151:        tc, _ = client_legs
ATT/tests/test_structures_legs_endpoints.py:153:        resp = tc.post("/structures/1/legs", json=payload)
ATT/tests/test_structures_legs_endpoints.py:156:    def test_add_leg_422_leg_order_negativo(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:157:        tc, _ = client_legs
ATT/tests/test_structures_legs_endpoints.py:159:        resp = tc.post("/structures/1/legs", json=payload)
ATT/tests/test_structures_legs_endpoints.py:164:# PUT /structures/{id}/legs
ATT/tests/test_structures_legs_endpoints.py:167:class TestReplaceLegs:
ATT/tests/test_structures_legs_endpoints.py:170:    def test_replace_legs_retorna_204(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:171:        tc, _ = client_legs
ATT/tests/test_structures_legs_endpoints.py:172:        resp = tc.put("/structures/1/legs", json=REPLACE_LEGS_PAYLOAD)
ATT/tests/test_structures_legs_endpoints.py:175:    def test_replace_legs_sem_body_na_resposta(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:176:        tc, _ = client_legs
ATT/tests/test_structures_legs_endpoints.py:177:        resp = tc.put("/structures/1/legs", json=REPLACE_LEGS_PAYLOAD)
ATT/tests/test_structures_legs_endpoints.py:180:    def test_replace_legs_repo_chamado_com_structure_id_correto(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:181:        tc, repo = client_legs
ATT/tests/test_structures_legs_endpoints.py:182:        tc.put("/structures/1/legs", json=REPLACE_LEGS_PAYLOAD)
ATT/tests/test_structures_legs_endpoints.py:183:        args = repo.replace_legs.call_args[0]
ATT/tests/test_structures_legs_endpoints.py:186:    def test_replace_legs_repo_recebe_lista_com_um_item(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:187:        tc, repo = client_legs
ATT/tests/test_structures_legs_endpoints.py:188:        tc.put("/structures/1/legs", json=REPLACE_LEGS_PAYLOAD)
ATT/tests/test_structures_legs_endpoints.py:189:        args = repo.replace_legs.call_args[0]
ATT/tests/test_structures_legs_endpoints.py:192:    def test_replace_legs_repo_recebe_dados_corretos(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:193:        tc, repo = client_legs
ATT/tests/test_structures_legs_endpoints.py:194:        tc.put("/structures/1/legs", json=REPLACE_LEGS_PAYLOAD)
ATT/tests/test_structures_legs_endpoints.py:195:        leg = repo.replace_legs.call_args[0][1][0]
ATT/tests/test_structures_legs_endpoints.py:199:    def test_replace_legs_404_estrutura_inexistente(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:200:        tc, repo = client_legs
ATT/tests/test_structures_legs_endpoints.py:202:        resp = tc.put("/structures/999/legs", json=REPLACE_LEGS_PAYLOAD)
ATT/tests/test_structures_legs_endpoints.py:205:    def test_replace_legs_400_quando_repo_levanta_value_error(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:206:        tc, repo = client_legs
ATT/tests/test_structures_legs_endpoints.py:207:        repo.replace_legs.side_effect = ValueError("leg inválida no replace")
ATT/tests/test_structures_legs_endpoints.py:208:        resp = tc.put("/structures/1/legs", json=REPLACE_LEGS_PAYLOAD)
ATT/tests/test_structures_legs_endpoints.py:211:    def test_replace_legs_422_lista_vazia(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:213:        tc, _ = client_legs
ATT/tests/test_structures_legs_endpoints.py:214:        resp = tc.put("/structures/1/legs", json={"legs": []})
ATT/tests/test_structures_legs_endpoints.py:217:    def test_replace_legs_aceita_leg_order_zero(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:219:        tc, _ = client_legs
ATT/tests/test_structures_legs_endpoints.py:220:        payload = {"legs": [{**FAKE_LEG_PAYLOAD, "leg_order": 0}]}
ATT/tests/test_structures_legs_endpoints.py:221:        resp = tc.put("/structures/1/legs", json=payload)
ATT/tests/test_structures_legs_endpoints.py:224:    def test_replace_legs_aceita_multiplas_legs(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:226:        tc, repo = client_legs
ATT/tests/test_structures_legs_endpoints.py:228:            "legs": [
ATT/tests/test_structures_legs_endpoints.py:234:        resp = tc.put("/structures/1/legs", json=payload)
ATT/tests/test_structures_legs_endpoints.py:236:        args = repo.replace_legs.call_args[0]
ATT/tests/test_structures_legs_endpoints.py:241:# DELETE /structures/{id}/legs/{leg_id}
ATT/tests/test_structures_legs_endpoints.py:257:    def test_remove_leg_retorna_204(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:258:        tc, repo = client_legs
ATT/tests/test_structures_legs_endpoints.py:260:        resp = tc.delete("/structures/1/legs/10")
ATT/tests/test_structures_legs_endpoints.py:263:    def test_remove_leg_404_estrutura_inexistente(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:264:        tc, repo = client_legs
ATT/tests/test_structures_legs_endpoints.py:266:        resp = tc.delete("/structures/999/legs/10")
ATT/tests/test_structures_legs_endpoints.py:269:    def test_remove_leg_404_leg_inexistente(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:270:        tc, repo = client_legs
ATT/tests/test_structures_legs_endpoints.py:272:        resp = tc.delete("/structures/1/legs/999")
ATT/tests/test_structures_legs_endpoints.py:275:    def test_remove_leg_404_detalhe_contem_leg_id(self, client_legs):
ATT/tests/test_structures_legs_endpoints.py:276:        tc, repo = client_legs
ATT/tests/test_structures_legs_endpoints.py:278:        resp = tc.delete("/structures/1/legs/999")
ATT/tests/test_structures_repository.py:41:def test_create_structure_normalizes_underlying_asset(repo):
ATT/tests/test_structures_repository.py:42:    structure_id = repo.create_structure(valid_structure_payload())
ATT/tests/test_structures_repository.py:50:    assert structure["legs"] == []
ATT/tests/test_structures_repository.py:53:def test_create_structure_raises_when_name_missing(repo):
ATT/tests/test_structures_repository.py:58:        repo.create_structure(payload)
ATT/tests/test_structures_repository.py:61:def test_create_structure_raises_when_underlying_asset_missing(repo):
ATT/tests/test_structures_repository.py:66:        repo.create_structure(payload)
ATT/tests/test_structures_repository.py:69:def test_create_structure_raises_when_status_invalid(repo):
ATT/tests/test_structures_repository.py:74:        repo.create_structure(payload)
ATT/tests/test_structures_repository.py:78:    active_id = repo.create_structure(valid_structure_payload())
ATT/tests/test_structures_repository.py:79:    archived_id = repo.create_structure(
ATT/tests/test_structures_repository.py:94:    first_id = repo.create_structure(valid_structure_payload())
ATT/tests/test_structures_repository.py:95:    second_id = repo.create_structure(
ATT/tests/test_structures_repository.py:110:def test_get_structure_returns_legs_ordered_by_leg_order(repo):
ATT/tests/test_structures_repository.py:111:    structure_id = repo.create_structure(valid_structure_payload())
ATT/tests/test_structures_repository.py:127:    assert [leg["leg_order"] for leg in structure["legs"]] == [1, 2]
ATT/tests/test_structures_repository.py:128:    assert [leg["symbol"] for leg in structure["legs"]] == ["BOVA11P110", "BOVA11C130"]
ATT/tests/test_structures_repository.py:131:def test_update_structure_updates_fields_and_keeps_missing_ones(repo):
ATT/tests/test_structures_repository.py:132:    structure_id = repo.create_structure(valid_structure_payload())
ATT/tests/test_structures_repository.py:134:    repo.update_structure(
ATT/tests/test_structures_repository.py:150:def test_update_structure_raises_when_structure_not_found(repo):
ATT/tests/test_structures_repository.py:152:        repo.update_structure(999, {"name": "x"})
ATT/tests/test_structures_repository.py:156:    structure_id = repo.create_structure(valid_structure_payload())
ATT/tests/test_structures_repository.py:170:    structure_id = repo.create_structure(valid_structure_payload())
ATT/tests/test_structures_repository.py:177:    assert len(structure["legs"]) == 1
ATT/tests/test_structures_repository.py:178:    assert structure["legs"][0]["position_side"] == "COMPRADO"
ATT/tests/test_structures_repository.py:179:    assert structure["legs"][0]["option_type"] == "CALL"
ATT/tests/test_structures_repository.py:197:    structure_id = repo.create_structure(valid_structure_payload())
ATT/tests/test_structures_repository.py:209:def test_replace_legs_replaces_existing_legs(repo):
ATT/tests/test_structures_repository.py:210:    structure_id = repo.create_structure(valid_structure_payload())
ATT/tests/test_structures_repository.py:215:    repo.replace_legs(
ATT/tests/test_structures_repository.py:230:    assert len(structure["legs"]) == 1
ATT/tests/test_structures_repository.py:231:    assert structure["legs"][0]["symbol"] == "BOVA11P100"
ATT/tests/test_structures_repository.py:232:    assert structure["legs"][0]["position_side"] == "VENDIDO"
ATT/tests/test_structures_repository.py:233:    assert structure["legs"][0]["option_type"] == "PUT"
ATT/tests/test_structures_repository.py:236:def test_replace_legs_raises_when_structure_not_found(repo):
ATT/tests/test_structures_repository.py:238:        repo.replace_legs(999, [valid_leg_payload()])
ATT/tests/test_system_snapshots_repository.py:49:        INSERT INTO structure_legs (
ATT/tests/test_system_snapshots_repository.py:85:def test_create_snapshot_persists_snapshot_and_legs(tmp_path: Path):
ATT/tests/test_system_snapshots_repository.py:124:        legs=[
ATT/tests/test_system_snapshots_repository.py:172:    assert len(snapshot["legs"]) == 2
ATT/tests/test_system_snapshots_repository.py:173:    assert snapshot["legs"][0]["leg_id"] == leg_1_id
ATT/tests/test_system_snapshots_repository.py:174:    assert snapshot["legs"][0]["symbol"] == "PETRA10"
ATT/tests/test_system_snapshots_repository.py:175:    assert snapshot["legs"][0]["metrics_json"] == {"delta": 0.55}
ATT/tests/test_system_snapshots_repository.py:176:    assert snapshot["legs"][1]["leg_id"] == leg_2_id
ATT/tests/test_system_snapshots_repository.py:177:    assert snapshot["legs"][1]["symbol"] == "PETRA12"
ATT/tests/test_system_snapshots_repository.py:178:    assert snapshot["legs"][1]["market_json"] == {"bid": 0.9, "ask": 1.0}
ATT/tests/test_system_snapshots_repository.py:208:def test_get_latest_snapshot_for_structure_returns_snapshot_with_legs(tmp_path: Path):
ATT/tests/test_system_snapshots_repository.py:227:        legs=[
ATT/tests/test_system_snapshots_repository.py:247:    assert len(latest["legs"]) == 1
ATT/tests/test_system_snapshots_repository.py:248:    assert latest["legs"][0]["symbol"] == "PETRM30"
ATT/tests/test_system_snapshots_schema.py:123:    assert ("structure_legs", "leg_id", "id", "NO ACTION") in foreign_keys
UI/components/details_panel.py:405:            "robo_legs_snapshot",
UI/components/details_panel.py:771:            "legs": [...],
UI/components/filters_panel.py:151:    def update_structures(self, structures: List[str]):
UI/components/payoff_chart.py:223:        file_path = filedialog.asksaveasfilename(
UI/components/payoff_chart.py:231:            self.fig.savefig(file_path, dpi=150, bbox_inches="tight")
UI/components/structure_editor_dialog.py:1:# UI/components/structure_editor_dialog.py
UI/components/structure_editor_dialog.py:3:StructureEditorDialog -- alteracao_10 / Fase 5
UI/components/structure_editor_dialog.py:4:Dialog modal para criar / editar uma estrutura com suas legs.
UI/components/structure_editor_dialog.py:7:    dlg = StructureEditorDialog(
UI/components/structure_editor_dialog.py:13:    if dlg.saved: ...               # True se o usuario clicou Salvar com sucesso
UI/components/structure_editor_dialog.py:16:    saved           bool
UI/components/structure_editor_dialog.py:22:    _legs_rows      list[dict]
UI/components/structure_editor_dialog.py:25:    _cmd_save()     metodo que executa a logica de salvar
UI/components/structure_editor_dialog.py:27:    _build_legs_payload()  logica pura, testavel sem display
UI/components/structure_editor_dialog.py:61:class StructureEditorDialog(tk.Toplevel):
UI/components/structure_editor_dialog.py:77:        self.saved         = False
UI/components/structure_editor_dialog.py:78:        self.saved_structure_id = None
UI/components/structure_editor_dialog.py:79:        self._legs_rows: list[dict] = []
UI/components/structure_editor_dialog.py:144:        # === Legs ===
UI/components/structure_editor_dialog.py:145:        legs_outer = ttk.LabelFrame(self, text="Legs", padding=8)
UI/components/structure_editor_dialog.py:146:        legs_outer.pack(fill="both", expand=True, padx=8, pady=4)
UI/components/structure_editor_dialog.py:148:        # Toolbar de legs
UI/components/structure_editor_dialog.py:149:        leg_toolbar = ttk.Frame(legs_outer)
UI/components/structure_editor_dialog.py:156:        # Treeview de legs
UI/components/structure_editor_dialog.py:157:        leg_frame = ttk.Frame(legs_outer)
UI/components/structure_editor_dialog.py:182:        self._build_leg_form(legs_outer)
UI/components/structure_editor_dialog.py:189:        ttk.Button(btn_bar, text="[SAVE] Salvar", command=self._cmd_save).pack(side="right", padx=4)
UI/components/structure_editor_dialog.py:192:        """Formulario colapsavel para editar / adicionar uma leg."""
UI/components/structure_editor_dialog.py:259:        Carrega campos e legs de uma estrutura existente via repositorio.
UI/components/structure_editor_dialog.py:279:        self._legs_rows = list(data.get("legs", []))
UI/components/structure_editor_dialog.py:288:        for i, leg in enumerate(self._legs_rows, 1):
UI/components/structure_editor_dialog.py:311:    # Callbacks de legs
UI/components/structure_editor_dialog.py:319:        leg = self._legs_rows[idx]
UI/components/structure_editor_dialog.py:339:            "leg_order":       len(self._legs_rows) + 1,
UI/components/structure_editor_dialog.py:343:        self._legs_rows.append(new_leg)
UI/components/structure_editor_dialog.py:345:        new_iid = str(len(self._legs_rows) - 1)
UI/components/structure_editor_dialog.py:357:            hasattr(StructureEditorDialog, '_add_leg_row')
UI/components/structure_editor_dialog.py:366:        self._legs_rows.pop(idx)
UI/components/structure_editor_dialog.py:374:        if new_idx < 0 or new_idx >= len(self._legs_rows):
UI/components/structure_editor_dialog.py:376:        self._legs_rows[idx], self._legs_rows[new_idx] = (
UI/components/structure_editor_dialog.py:377:            self._legs_rows[new_idx],
UI/components/structure_editor_dialog.py:378:            self._legs_rows[idx],
UI/components/structure_editor_dialog.py:413:            usado no save/build payload; se a leg manual ja esta completa e a
UI/components/structure_editor_dialog.py:494:            self._legs_rows[idx] = enriched
UI/components/structure_editor_dialog.py:521:            self._legs_rows[idx] = leg_data
UI/components/structure_editor_dialog.py:532:    def _build_legs_payload(self) -> list[dict]:
UI/components/structure_editor_dialog.py:534:        Constrói lista de legs com leg_order sequencial a partir de 1.
UI/components/structure_editor_dialog.py:537:        - Não modifica self._legs_rows.
UI/components/structure_editor_dialog.py:587:        for index, leg in enumerate(self._legs_rows, start=1):
UI/components/structure_editor_dialog.py:623:    def _cmd_save(self):
UI/components/structure_editor_dialog.py:632:            legs_payload = self._build_legs_payload()
UI/components/structure_editor_dialog.py:640:                for leg in legs_payload
UI/components/structure_editor_dialog.py:649:                    "As legs possuem ativos objeto diferentes: "
UI/components/structure_editor_dialog.py:670:                sid = self._repo.create_structure_with_legs(
UI/components/structure_editor_dialog.py:672:                    legs_payload,
UI/components/structure_editor_dialog.py:677:                self._repo.update_structure(sid, structure_data)
UI/components/structure_editor_dialog.py:678:                self._repo.replace_legs(sid, legs_payload)
UI/components/structure_editor_dialog.py:682:                    self.saved_structure_id = int(self._structure_id)
UI/components/structure_editor_dialog.py:684:                    _candidate_saved_structure_id = (
UI/components/structure_editor_dialog.py:692:                    self.saved_structure_id = (
UI/components/structure_editor_dialog.py:693:                        int(_candidate_saved_structure_id)
UI/components/structure_editor_dialog.py:694:                        if _candidate_saved_structure_id is not None
UI/components/structure_editor_dialog.py:698:                self.saved_structure_id = getattr(self, "_structure_id", None)
UI/components/structure_editor_dialog.py:699:            self.saved = True
UI/components/structures_list_panel.py:35:_COLUMNS = ("id", "name", "underlying_asset", "alias", "status", "legs")
UI/components/structures_list_panel.py:42:    "legs":             ("Legs",      45,  "center"),
UI/components/structures_list_panel.py:189:            n_legs = row.get("n_legs", 0)
UI/components/structures_list_panel.py:199:                    n_legs if n_legs else "--",
UI/components/structures_list_panel.py:222:        """Busca estrutura completa (com legs) pelo repositorio."""
UI/components/structures_list_panel.py:284:            new_id = self._repo.create_structure({
UI/components/structures_list_panel.py:291:            legs_copy = [
UI/components/structures_list_panel.py:294:                for leg in src.get("legs", [])
UI/components/structures_list_panel.py:296:            if legs_copy:
UI/components/structures_list_panel.py:297:                self._repo.replace_legs(new_id, legs_copy)
UI/main_window.py:13:from UI.components.structure_editor_dialog import StructureEditorDialog
UI/main_window.py:293:                self.filters_panel.update_structures(
UI/main_window.py:433:        filename = filedialog.asksaveasfilename(
UI/main_window.py:843:            legs = structure.get("legs", [])
UI/main_window.py:854:                f" {len(legs)} Leg(s) ",
UI/main_window.py:856:            for i, leg in enumerate(legs, 1):
UI/main_window.py:870:        dlg = StructureEditorDialog(
UI/main_window.py:876:        if dlg.saved:
UI/main_window.py:877:            saved_structure_id = getattr(dlg, "saved_structure_id", None) or structure_id
UI/main_window.py:886:            if saved_structure_id is not None:
UI/main_window.py:887:                self._reprice_structure_after_save(int(saved_structure_id))
UI/main_window.py:890:    def _reprice_structure_after_save(self, structure_id: int) -> None:
api/structures_controller.py:4:alteracao_63 -- Endpoints de legs:
api/structures_controller.py:5:    POST   /structures/{id}/legs            adiciona uma perna
api/structures_controller.py:6:    PUT    /structures/{id}/legs            substitui todas as pernas (atômico)
api/structures_controller.py:7:    DELETE /structures/{id}/legs/{leg_id}   remove perna individual
api/structures_controller.py:46:# Schemas de entrada — legs  (alteracao_63)
api/structures_controller.py:70:    """Payload para PUT /structures/{id}/legs — lista de legs completa."""
api/structures_controller.py:71:    legs: list[LegRequest] = Field(..., min_length=1)
api/structures_controller.py:94:    legs: list[dict[str, Any]]
api/structures_controller.py:120:def create_structure(request: CreateStructureRequest) -> CreateStructureResponse:
api/structures_controller.py:122:        structure_id = _repo.create_structure(request.model_dump())
api/structures_controller.py:143:def update_structure(structure_id: int, request: UpdateStructureRequest) -> None:
api/structures_controller.py:151:        _repo.update_structure(structure_id, data)
api/structures_controller.py:170:# Endpoints — legs  (alteracao_63)
api/structures_controller.py:174:    "/structures/{structure_id}/legs",
api/structures_controller.py:193:@router.put("/structures/{structure_id}/legs", status_code=204)
api/structures_controller.py:194:def replace_legs(structure_id: int, request: ReplaceLegRequest) -> None:
api/structures_controller.py:202:        _repo.replace_legs(
api/structures_controller.py:204:            [leg.model_dump() for leg in request.legs],
api/structures_controller.py:210:@router.delete("/structures/{structure_id}/legs/{leg_id}", status_code=204)
api/structures_controller.py:221:            "SELECT id FROM structure_legs WHERE id=? AND structure_id=?",
api/structures_controller.py:235:            "DELETE FROM structure_legs WHERE id=?",
api/structures_controller.py:400:    Não persiste alterações nas legs. Apenas calcula o estado efetivo:
repositories/_aba_resolver_mixin.py:16:    alteracao_40 -- método criado em robo_legs_repository e robo_legs_status_repository
repositories/market_snapshot_repository.py:5:Le legs RTD (rtd_analise_robo_legs), cotações RTD de opções
repositories/market_snapshot_repository.py:6:(rtd_option_quotes) e manuais (manual_analise_robo_legs), normaliza os campos
repositories/market_snapshot_repository.py:32:_SQL_RTD_LEGS = """
repositories/market_snapshot_repository.py:54:    FROM rtd_analise_robo_legs
repositories/market_snapshot_repository.py:59:_SQL_MANUAL_LEGS = """
repositories/market_snapshot_repository.py:83:    FROM manual_analise_robo_legs
repositories/market_snapshot_repository.py:201:    em rtd_analise_robo_legs.
repositories/market_snapshot_repository.py:254:      get_rtd_legs(aba)                -> lista de LegMarketSnapshot source=RTD
repositories/market_snapshot_repository.py:255:      get_rtd_option_quote_legs(aba)   -> lista enriquecida source=rtd_option_quotes
repositories/market_snapshot_repository.py:256:      get_manual_legs(aba)             -> lista de LegMarketSnapshot source=MANUAL
repositories/market_snapshot_repository.py:273:    def get_rtd_legs(self, ref: StructureRef | str) -> list[LegMarketSnapshot]:
repositories/market_snapshot_repository.py:276:            rows = conn.execute(_SQL_RTD_LEGS, (aba,)).fetchall()
repositories/market_snapshot_repository.py:279:    def get_rtd_option_quote_legs(self, ref: StructureRef | str) -> list[LegMarketSnapshot]:
repositories/market_snapshot_repository.py:281:        Retorna legs RTD enriquecidas com rtd_option_quotes.
repositories/market_snapshot_repository.py:283:        A composição da estrutura vem de rtd_analise_robo_legs. Para cada ativo
repositories/market_snapshot_repository.py:287:        base_legs = self.get_rtd_legs(ref)
repositories/market_snapshot_repository.py:288:        if not base_legs:
repositories/market_snapshot_repository.py:293:            for leg in base_legs
repositories/market_snapshot_repository.py:341:        for base_leg in base_legs:
repositories/market_snapshot_repository.py:359:    def get_manual_legs(self, ref: StructureRef | str) -> list[LegMarketSnapshot]:
repositories/market_snapshot_repository.py:362:            rows = conn.execute(_SQL_MANUAL_LEGS, (aba,)).fetchall()
repositories/market_snapshot_repository.py:375:            legs = self.get_rtd_legs(ref)
repositories/market_snapshot_repository.py:378:            legs = self.get_manual_legs(ref)
repositories/market_snapshot_repository.py:390:            legs=legs,
repositories/pricing_executions_repository.py:30:    def save_execution(
repositories/pricing_executions_repository.py:38:        number_of_legs: int | None = None,
repositories/pricing_executions_repository.py:61:                    duration_ms, number_of_legs, total_quantity, theoretical_value,
repositories/pricing_executions_repository.py:68:                    duration_ms, number_of_legs, total_quantity, theoretical_value,
repositories/pricing_executions_repository.py:87:            "number_of_legs": number_of_legs,
repositories/robo_legs_repository.py:1:# repositories/robo_legs_repository.py
repositories/robo_legs_repository.py:5:             (elimina duplicação com robo_legs_status_repository)
repositories/robo_legs_repository.py:29:class RoboLegsRepoConfig:
repositories/robo_legs_repository.py:33:class RoboLegsRepository(AbaResolverMixin):
repositories/robo_legs_repository.py:36:      manual_analise_robo_legs > rtd_analise_robo_legs
repositories/robo_legs_repository.py:50:    def __init__(self, config: Optional[RoboLegsRepoConfig] = None):
repositories/robo_legs_repository.py:51:        self.config = config or RoboLegsRepoConfig()
repositories/robo_legs_repository.py:53:    def get_legs(self, ref: StructureRef, timestamp: Any) -> List[RoboLegDTO]:
repositories/robo_legs_repository.py:55:        Retorna legs para uma aba e um timestamp exatos.
repositories/robo_legs_repository.py:63:        manual = self._query_legs(
repositories/robo_legs_repository.py:64:            table="manual_analise_robo_legs",
repositories/robo_legs_repository.py:72:        rtd = self._query_legs(
repositories/robo_legs_repository.py:73:            table="rtd_analise_robo_legs",
repositories/robo_legs_repository.py:88:            FROM manual_analise_robo_legs
repositories/robo_legs_repository.py:110:                    SELECT timestamp FROM manual_analise_robo_legs WHERE aba = ?
repositories/robo_legs_repository.py:112:                    SELECT timestamp FROM rtd_analise_robo_legs WHERE aba = ?
repositories/robo_legs_repository.py:120:                "SELECT DISTINCT timestamp FROM manual_analise_robo_legs "
repositories/robo_legs_repository.py:128:                "SELECT DISTINCT timestamp FROM rtd_analise_robo_legs "
repositories/robo_legs_repository.py:134:    def _query_legs(
repositories/robo_legs_repository.py:235:    def get_legs_by_structure_id(
repositories/robo_legs_repository.py:242:        delega para get_legs() existente.
repositories/robo_legs_repository.py:252:        return self.get_legs(ref=ref, timestamp=timestamp)
repositories/robo_legs_status_repository.py:1:# repositories/robo_legs_status_repository.py
repositories/robo_legs_status_repository.py:5:             (elimina duplicação com robo_legs_repository)
repositories/robo_legs_status_repository.py:27:class RoboLegsStatusRepoConfig:
repositories/robo_legs_status_repository.py:31:class RoboLegsStatusRepository(AbaResolverMixin):
repositories/robo_legs_status_repository.py:33:    Repository de status de legs do robô.
repositories/robo_legs_status_repository.py:39:    def __init__(self, config: Optional[RoboLegsStatusRepoConfig] = None):
repositories/robo_legs_status_repository.py:40:        self.config = config or RoboLegsStatusRepoConfig()
repositories/robo_legs_status_repository.py:53:                "SELECT MAX(timestamp) AS ts FROM manual_analise_robo_legs WHERE aba = ?",
repositories/robo_legs_status_repository.py:57:                "SELECT MAX(timestamp) AS ts FROM rtd_analise_robo_legs WHERE aba = ?",
repositories/structure_events_repository.py:215:                FOREIGN KEY (leg_id) REFERENCES structure_legs(id) ON DELETE SET NULL
repositories/structure_events_repository.py:290:            FROM structure_legs
repositories/structures_repository.py:3:Repositório canônico de estruturas e suas pernas (legs).
repositories/structures_repository.py:32:    {"CREATE", "UPDATE", "ARCHIVE", "ADD_LEG", "REPLACE_LEGS"}
repositories/structures_repository.py:193:    def _fetch_legs(
repositories/structures_repository.py:202:            FROM structure_legs
repositories/structures_repository.py:306:    def create_structure(self, data: dict[str, Any]) -> int:
repositories/structures_repository.py:345:    def create_structure_with_legs(
repositories/structures_repository.py:348:        legs: list[dict[str, Any]],
repositories/structures_repository.py:351:        Cria uma estrutura e suas legs em uma única transação.
repositories/structures_repository.py:353:        Garante que não exista estrutura persistida sem legs caso a gravação
repositories/structures_repository.py:357:        validated_legs = [_validate_leg(leg) for leg in legs]
repositories/structures_repository.py:359:        if not validated_legs:
repositories/structures_repository.py:398:            for leg in validated_legs:
repositories/structures_repository.py:401:                    INSERT INTO structure_legs (
repositories/structures_repository.py:427:                action="REPLACE_LEGS",
repositories/structures_repository.py:430:                    "legs_count": len(validated_legs),
repositories/structures_repository.py:487:            structure["legs"] = self._fetch_legs(conn, structure_id)
repositories/structures_repository.py:496:    def update_structure(self, structure_id: int, data: dict[str, Any]) -> None:
repositories/structures_repository.py:501:        # snapshot antes da mudanca (sem legs para manter log enxuto)
repositories/structures_repository.py:502:        before_snap = {k: v for k, v in current.items() if k != "legs"}
repositories/structures_repository.py:555:        before_snap = {k: v for k, v in current.items() if k != "legs"}
repositories/structures_repository.py:583:    # LEGS
repositories/structures_repository.py:596:                INSERT INTO structure_legs (
repositories/structures_repository.py:632:    def replace_legs(
repositories/structures_repository.py:633:        self, structure_id: int, legs: list[dict[str, Any]]
repositories/structures_repository.py:635:        validated_legs = [_validate_leg(leg) for leg in legs]
repositories/structures_repository.py:643:                "DELETE FROM structure_legs WHERE structure_id=?",
repositories/structures_repository.py:647:            for leg in validated_legs:
repositories/structures_repository.py:650:                    INSERT INTO structure_legs (
repositories/structures_repository.py:669:            # alteracao_72: registrar substituicao de legs no audit log
repositories/structures_repository.py:673:                action="REPLACE_LEGS",
repositories/structures_repository.py:674:                after={"legs_count": len(validated_legs), "replaced_at": now},
repositories/structures_repository.py:688:    def count_legs(self, structure_id: int) -> int:
repositories/structures_repository.py:692:                "SELECT COUNT(*) AS n FROM structure_legs WHERE structure_id=?",
repositories/structures_repository.py:726:            structure["legs"] = self._fetch_legs(conn, structure["id"])
repositories/system_snapshots_repository.py:83:        legs: list[dict[str, Any]] | None = None,
repositories/system_snapshots_repository.py:108:        legs = legs or []
repositories/system_snapshots_repository.py:149:            for index, leg in enumerate(legs, start=1):
repositories/system_snapshots_repository.py:237:            snapshot["legs"] = [self._decode_leg_row(row) for row in leg_rows]
services/calculation_orchestrator.py:52:    legs_rows: list,
services/calculation_orchestrator.py:59:    if not isinstance(legs_rows, list) or len(legs_rows) == 0:
services/calculation_orchestrator.py:60:        raise ValueError("legs_rows nao pode ser vazio")
services/calculation_orchestrator.py:62:    legs = []
services/calculation_orchestrator.py:63:    for i, row in enumerate(legs_rows):
services/calculation_orchestrator.py:83:        legs.append(leg)
services/calculation_orchestrator.py:88:        legs=legs,
services/calculation_orchestrator.py:116:    legs = []
services/calculation_orchestrator.py:117:    for leg in request.structure.legs:
services/calculation_orchestrator.py:118:        legs.append({
services/calculation_orchestrator.py:136:            "legs":             legs,
services/calculation_orchestrator.py:257:        legs = []
services/calculation_orchestrator.py:258:        for i, leg in enumerate(structure_dict.get("legs", [])):
services/calculation_orchestrator.py:259:            legs.append(
services/calculation_orchestrator.py:283:            legs=legs,
services/calculation_orchestrator.py:305:        legs = []
services/calculation_orchestrator.py:306:        for leg in request.structure.legs:
services/calculation_orchestrator.py:307:            legs.append({
services/calculation_orchestrator.py:325:                "legs":             legs,
services/calculation_orchestrator.py:418:            ValueError  : se estrutura nao encontrada, arquivada ou sem legs
services/calculation_orchestrator.py:444:        legs_raw = structure.get("legs", [])
services/calculation_orchestrator.py:445:        if not legs_raw:
services/calculation_orchestrator.py:447:                f"Estrutura sem legs: structure_id={structure_id}"
services/calculation_orchestrator.py:468:            "legs": [
services/calculation_orchestrator.py:481:                for leg in legs_raw
services/canonical_input_service.py:8:  - _resolve_legs            → MarketSnapshotSelector (manual > rtd por ativo)
services/canonical_input_service.py:18:    "legs":               list[dict],   # campo extra, assembler ignora mas outros consomem
services/canonical_input_service.py:29:from services.legacy_robo_legs_fallback import LegacyRoboLegsFallback
services/canonical_input_service.py:42:        robo_legs_service: Any | None = None,  # injeção explícita
services/canonical_input_service.py:44:        prefer_canonical_legs: bool = True,
services/canonical_input_service.py:45:        enable_legacy_legs_fallback: bool = True,
services/canonical_input_service.py:52:        self.prefer_canonical_legs       = prefer_canonical_legs
services/canonical_input_service.py:53:        self.enable_legacy_legs_fallback = enable_legacy_legs_fallback
services/canonical_input_service.py:56:        if robo_legs_service is not None:
services/canonical_input_service.py:58:            self.robo_legs_service = robo_legs_service
services/canonical_input_service.py:60:            # BRIDGE LEGADO: import dinamico de robo_legs_service para compatibilidade
services/canonical_input_service.py:63:                from services.robo_legs_service import RoboLegsService  # noqa: PLC0415
services/canonical_input_service.py:64:                self.robo_legs_service = RoboLegsService()
services/canonical_input_service.py:66:                self.robo_legs_service = None
services/canonical_input_service.py:68:        # LegacyRoboLegsFallback sempre inicializado, independente da origem do robo_legs_service
services/canonical_input_service.py:69:        self.legacy_robo_legs_fallback = LegacyRoboLegsFallback(
services/canonical_input_service.py:70:            robo_legs_service=self.robo_legs_service,
services/canonical_input_service.py:112:        enriched_structure, enrichment_meta = self._enrich_structure_with_legs(
services/canonical_input_service.py:151:        legs pelo resultado do selector (manual > rtd).
services/canonical_input_service.py:162:        # 2. Legs — via selector se disponível, senão mantém o que o provider trouxe
services/canonical_input_service.py:165:            legs_list, legs_meta = self._resolve_legs_via_selector(ref)
services/canonical_input_service.py:166:            snapshot_source = legs_meta["snapshot_source"]
services/canonical_input_service.py:168:            legs_list  = base_snapshot.get("legs", [])
services/canonical_input_service.py:169:            legs_meta  = {}
services/canonical_input_service.py:177:            "legs": legs_list,
services/canonical_input_service.py:182:            **legs_meta,
services/canonical_input_service.py:188:    # Legs via selector (manual > rtd)
services/canonical_input_service.py:191:    def _resolve_legs_via_selector(
services/canonical_input_service.py:196:        Delega ao MarketSnapshotSelector e serializa legs completas.
services/canonical_input_service.py:204:        legs_as_dict = [
services/canonical_input_service.py:235:            for leg in result.legs
services/canonical_input_service.py:239:        reference_date = self._reference_date_from_legs(result.legs)
services/canonical_input_service.py:246:            "legs_reference_date": reference_date,
services/canonical_input_service.py:249:        return legs_as_dict, meta
services/canonical_input_service.py:252:    def _reference_date_from_legs(legs) -> str | None:
services/canonical_input_service.py:253:        """Extrai a data (YYYY-MM-DD) do timestamp mais recente entre as legs."""
services/canonical_input_service.py:254:        timestamps = [leg.timestamp for leg in legs if leg.timestamp]
services/canonical_input_service.py:261:    # Enriquecimento de legs canônicas / fallback (inalterado do alteracao_13)
services/canonical_input_service.py:266:        legs_source: str,
services/canonical_input_service.py:272:        meta: dict[str, Any] = {"legs_source": legs_source}
services/canonical_input_service.py:279:    def _base_legs_response(
services/canonical_input_service.py:282:        existing_legs: list[dict[str, Any]],
services/canonical_input_service.py:283:        legs_source: str,
services/canonical_input_service.py:287:            {**structure, "legs": existing_legs},
services/canonical_input_service.py:288:            self._build_meta(legs_source=legs_source, fallback_reason=fallback_reason),
services/canonical_input_service.py:291:    def _enrich_structure_with_legs(
services/canonical_input_service.py:296:        existing_legs = structure.get("legs", []) or []
services/canonical_input_service.py:298:        if self.prefer_canonical_legs and existing_legs:
services/canonical_input_service.py:299:            return self._base_legs_response(
services/canonical_input_service.py:301:                existing_legs=existing_legs,
services/canonical_input_service.py:302:                legs_source="canonical",
services/canonical_input_service.py:305:        if not self.enable_legacy_legs_fallback:
services/canonical_input_service.py:306:            return self._base_legs_response(
services/canonical_input_service.py:308:                existing_legs=existing_legs,
services/canonical_input_service.py:309:                legs_source="empty",
services/canonical_input_service.py:313:        fallback_legs, fallback_meta = self.legacy_robo_legs_fallback.load(
services/canonical_input_service.py:318:        if fallback_legs:
services/canonical_input_service.py:320:                {**structure, "legs": fallback_legs},
services/canonical_input_service.py:322:                    "legs_source":       fallback_meta.get("legs_source", "legacy_fallback"),
services/canonical_input_service.py:330:        if existing_legs:
services/canonical_input_service.py:331:            return self._base_legs_response(
services/canonical_input_service.py:333:                existing_legs=existing_legs,
services/canonical_input_service.py:334:                legs_source="canonical",
services/canonical_input_service.py:335:                fallback_reason="canonical_legs_retained_after_empty_fallback",
services/canonical_input_service.py:338:        return self._base_legs_response(
services/canonical_input_service.py:340:            existing_legs=existing_legs,
services/canonical_input_service.py:341:            legs_source="empty",
services/canonical_input_service.py:343:                fallback_meta.get("fallback_reason") if fallback_meta else "no_legs_available"
services/canonical_pricing_facade.py:242:    legs_data = []
services/canonical_pricing_facade.py:244:    for leg in selection_result.legs:
services/canonical_pricing_facade.py:281:        legs_data.append(canonical_leg)
services/canonical_pricing_facade.py:311:        "legs":             legs_data,
services/canonical_pricing_facade.py:316:            "legs_count":       len(legs_data),
services/derived_payoff_persistence.py:7:from services.derived_service import save_payoff_from_canonical_payload, save_decision_from_canonical_payload
services/derived_payoff_persistence.py:49:        payoff_saved = self._persist_payoff(pricing_payload, result, snapshot_ts)
services/derived_payoff_persistence.py:50:        if not payoff_saved:
services/derived_payoff_persistence.py:57:        decision_saved = self._persist_decision(pricing_payload, result, snapshot_ts)
services/derived_payoff_persistence.py:58:        if not decision_saved:
services/derived_payoff_persistence.py:86:            save_payoff_from_canonical_payload(payoff_result, timestamp=snapshot_ts)
services/derived_payoff_persistence.py:158:            save_decision_from_canonical_payload(
services/derived_payoff_persistence.py:278:        Retorna uma cópia rasa do canonical_input com legs normalizadas para payoff.
services/derived_payoff_persistence.py:286:        legs = structure.get("legs") or []
services/derived_payoff_persistence.py:287:        structure["legs"] = [
services/derived_payoff_persistence.py:289:            for leg in legs
services/derived_payoff_persistence.py:310:          A) já canônico: { structure: { legs, ... }, market: { spot_price, ... } }
services/derived_payoff_persistence.py:311:          B) flat:        { legs: [...], spot_price: ..., structure_id: ..., ... }
services/derived_payoff_persistence.py:326:        legs           = pricing_payload.get("legs") or []
services/derived_payoff_persistence.py:338:                "legs": [
services/derived_payoff_persistence.py:340:                    for leg in legs
services/derived_service.py:160:def save_payoff_curve(
services/derived_service.py:210:def save_payoff_from_canonical_payload(
services/derived_service.py:242:        sig = inspect.signature(save_payoff_curve)
services/derived_service.py:254:        return save_payoff_curve(
services/derived_service.py:263:    return save_payoff_curve(
services/derived_service.py:273:def save_decision(
services/derived_service.py:322:def save_decision_from_canonical_payload(
services/derived_service.py:357:    return save_decision(
services/derived_service.py:550:    def save_payoff_curve(self, *args, **kwargs):
services/derived_service.py:551:        return save_payoff_curve(*args, **kwargs)
services/derived_service.py:553:    def save_decision(self, *args, **kwargs):
services/derived_service.py:554:        return save_decision(*args, **kwargs)
services/legacy_robo_legs_fallback.py:7:class LegacyRoboLegsFallback:
services/legacy_robo_legs_fallback.py:10:        robo_legs_service: Any | None = None,
services/legacy_robo_legs_fallback.py:13:        self.robo_legs_service = robo_legs_service
services/legacy_robo_legs_fallback.py:25:                "legs_source": "empty",
services/legacy_robo_legs_fallback.py:32:        if self.robo_legs_service is None:
services/legacy_robo_legs_fallback.py:34:                "legs_source": "empty",
services/legacy_robo_legs_fallback.py:38:                "fallback_reason": "robo_legs_service_unavailable",
services/legacy_robo_legs_fallback.py:48:                "legs_source": "empty",
services/legacy_robo_legs_fallback.py:55:        legacy_legs = self._load_legacy_legs(
services/legacy_robo_legs_fallback.py:60:        if not legacy_legs:
services/legacy_robo_legs_fallback.py:62:                "legs_source": "empty",
services/legacy_robo_legs_fallback.py:66:                "fallback_reason": "no_legacy_legs_found",
services/legacy_robo_legs_fallback.py:69:        canonical_legs = []
services/legacy_robo_legs_fallback.py:70:        for leg in legacy_legs:
services/legacy_robo_legs_fallback.py:73:                canonical_legs.append(adapted)
services/legacy_robo_legs_fallback.py:75:        if not canonical_legs:
services/legacy_robo_legs_fallback.py:77:                "legs_source": "empty",
services/legacy_robo_legs_fallback.py:81:                "fallback_reason": "legacy_legs_not_convertible",
services/legacy_robo_legs_fallback.py:84:        return canonical_legs, {
services/legacy_robo_legs_fallback.py:85:            "legs_source": "legacy_fallback",
services/legacy_robo_legs_fallback.py:114:        if self.robo_legs_service is None:
services/legacy_robo_legs_fallback.py:126:            method = getattr(self.robo_legs_service, method_name, None)
services/legacy_robo_legs_fallback.py:144:            method = getattr(self.robo_legs_service, method_name, None)
services/legacy_robo_legs_fallback.py:168:    def _load_legacy_legs(
services/legacy_robo_legs_fallback.py:173:        if self.robo_legs_service is None:
services/legacy_robo_legs_fallback.py:177:            "get_legs",
services/legacy_robo_legs_fallback.py:178:            "load_legs",
services/legacy_robo_legs_fallback.py:179:            "fetch_legs",
services/legacy_robo_legs_fallback.py:180:            "read_legs",
services/legacy_robo_legs_fallback.py:184:            method = getattr(self.robo_legs_service, method_name, None)
services/legacy_structure_legs_importer.py:1:# services/legacy_structure_legs_importer.py
services/legacy_structure_legs_importer.py:3:LegacyStructureLegsImporter
services/legacy_structure_legs_importer.py:6:Importa pernas legadas ja normalizadas pelo LegacyStructureLegsReader
services/legacy_structure_legs_importer.py:7:para a tabela canonica structure_legs.
services/legacy_structure_legs_importer.py:12:      -> LegacyStructureLegsReader.read_by_structure_id(...)
services/legacy_structure_legs_importer.py:13:      -> payload canonico de legs
services/legacy_structure_legs_importer.py:14:      -> StructuresRepository.replace_legs(...)
services/legacy_structure_legs_importer.py:19:    - Reaproveita o audit trail ja existente em StructuresRepository.replace_legs,
services/legacy_structure_legs_importer.py:20:      que registra action="REPLACE_LEGS".
services/legacy_structure_legs_importer.py:30:class LegacyStructureLegsReaderProtocol(Protocol):
services/legacy_structure_legs_importer.py:39:class LegacyStructureLegsImporter:
services/legacy_structure_legs_importer.py:41:    Orquestra a importacao das legs legadas para structure_legs.
services/legacy_structure_legs_importer.py:45:            Objeto compatível com LegacyStructureLegsReaderProtocol.
services/legacy_structure_legs_importer.py:48:            Repositório canônico de structures/structure_legs.
services/legacy_structure_legs_importer.py:54:        reader: LegacyStructureLegsReaderProtocol,
services/legacy_structure_legs_importer.py:67:        Importa legs legadas para uma estrutura canonica.
services/legacy_structure_legs_importer.py:74:                "legs_count": 2,
services/legacy_structure_legs_importer.py:81:                - se o reader nao encontrar legs para importar.
services/legacy_structure_legs_importer.py:87:        legs = self.reader.read_by_structure_id(
services/legacy_structure_legs_importer.py:92:        if not legs:
services/legacy_structure_legs_importer.py:94:                f"structure_id={structure_id} sem legs legadas para importar"
services/legacy_structure_legs_importer.py:97:        self.structures_repository.replace_legs(
services/legacy_structure_legs_importer.py:99:            legs=legs,
services/legacy_structure_legs_importer.py:105:            "legs_count": len(legs),
services/legacy_structure_legs_reader.py:5:from repositories.robo_legs_repository import RoboLegsRepository
services/legacy_structure_legs_reader.py:9:class LegacyStructureLegsReader:
services/legacy_structure_legs_reader.py:15:      - resolver alias_legacy_aba via RoboLegsRepository;
services/legacy_structure_legs_reader.py:17:      - converter para payload compatível com structure_legs;
services/legacy_structure_legs_reader.py:18:      - NÃO gravar em structure_legs.
services/legacy_structure_legs_reader.py:21:      structures.alias_legacy_aba -> *_analise_robo_legs.aba
services/legacy_structure_legs_reader.py:24:    def __init__(self, robo_legs_repository: RoboLegsRepository | None = None):
services/legacy_structure_legs_reader.py:25:        self.robo_legs_repository = robo_legs_repository or RoboLegsRepository()
services/legacy_structure_legs_reader.py:34:        legacy_legs = self.robo_legs_repository.get_legs_by_structure_id(
services/legacy_structure_legs_reader.py:39:        canonical_legs: list[dict[str, Any]] = []
services/legacy_structure_legs_reader.py:41:        for index, legacy_leg in enumerate(legacy_legs, start=1):
services/legacy_structure_legs_reader.py:47:            canonical_legs.append(canonical_leg)
services/legacy_structure_legs_reader.py:49:        return canonical_legs
services/market_snapshot_selector.py:8:  - Caso contrário, usa rtd_analise_robo_legs
services/market_snapshot_selector.py:37:    legs: list[LegMarketSnapshot] = field(default_factory=list)
services/market_snapshot_selector.py:60:        Seleciona as legs canônicas para a estrutura informada.
services/market_snapshot_selector.py:74:        manual_legs = self._repo.get_manual_legs(effective_ref)
services/market_snapshot_selector.py:75:        rtd_legs = self._repo.get_rtd_legs(effective_ref)
services/market_snapshot_selector.py:77:        get_rtd_option_quote_legs = getattr(
services/market_snapshot_selector.py:79:            "get_rtd_option_quote_legs",
services/market_snapshot_selector.py:82:        if callable(get_rtd_option_quote_legs):
services/market_snapshot_selector.py:83:            rtd_option_quote_legs = get_rtd_option_quote_legs(effective_ref)
services/market_snapshot_selector.py:85:            rtd_option_quote_legs = []
services/market_snapshot_selector.py:91:        for leg in manual_legs:
services/market_snapshot_selector.py:96:        for leg in rtd_option_quote_legs:
services/market_snapshot_selector.py:101:        for leg in rtd_legs:
services/market_snapshot_selector.py:111:        legs_selected: list[LegMarketSnapshot] = []
services/market_snapshot_selector.py:116:                legs_selected.append(manual_by_ativo[ativo])
services/market_snapshot_selector.py:120:                legs_selected.append(rtd_option_quote_by_ativo[ativo])
services/market_snapshot_selector.py:122:                legs_selected.append(rtd_by_ativo[ativo])
services/market_snapshot_selector.py:124:        if manual_legs:
services/market_snapshot_selector.py:126:        elif rtd_option_quote_legs:
services/market_snapshot_selector.py:134:            legs=legs_selected,
services/payoff_pricing_engine.py:3:from domain.payoff import compute_payoff_curve_from_canonical_legs
services/payoff_pricing_engine.py:24:        legs = pricing_payload.get("legs") or []
services/payoff_pricing_engine.py:25:        if not legs:
services/payoff_pricing_engine.py:26:            raise ValueError("pricing_payload.legs is required")
services/payoff_pricing_engine.py:32:        normalized_legs = [self._normalize_leg(leg) for leg in legs]
services/payoff_pricing_engine.py:36:            for leg in normalized_legs
services/payoff_pricing_engine.py:38:        number_of_legs = len(normalized_legs)
services/payoff_pricing_engine.py:40:        payoff = compute_payoff_curve_from_canonical_legs(
services/payoff_pricing_engine.py:41:            legs=normalized_legs,
services/payoff_pricing_engine.py:51:            legs=normalized_legs,
services/payoff_pricing_engine.py:55:        premium_paid = self._compute_net_premium_paid(normalized_legs)
services/payoff_pricing_engine.py:67:                "number_of_legs": number_of_legs,
services/payoff_pricing_engine.py:138:        legs: list[dict[str, Any]],
services/payoff_pricing_engine.py:143:        for leg in legs:
services/payoff_pricing_engine.py:164:    def _compute_net_premium_paid(legs: list[dict[str, Any]]) -> float:
services/payoff_pricing_engine.py:167:        for leg in legs:
services/pricing_execution_persistence_service.py:42:        number_of_legs = metrics.get("number_of_legs")
services/pricing_execution_persistence_service.py:46:        record = self.pricing_executions_repository.save_execution(
services/pricing_execution_persistence_service.py:53:            number_of_legs=number_of_legs,
services/pricing_execution_persistence_service.py:121:                legs=pricing_payload.get("legs") or [],
services/pricing_execution_query_service.py:98:            persisted_number_of_legs = execution.get("number_of_legs")
services/pricing_execution_query_service.py:117:                "number_of_legs": (
services/pricing_execution_query_service.py:118:                    persisted_number_of_legs
services/pricing_execution_query_service.py:119:                    if persisted_number_of_legs is not None
services/pricing_execution_query_service.py:120:                    else metrics.get("number_of_legs")
services/pricing_payload_adapter.py:31:    legs = structure.get("legs", [])
services/pricing_payload_adapter.py:32:    pricing_legs = []
services/pricing_payload_adapter.py:34:    for index, leg in enumerate(legs):
services/pricing_payload_adapter.py:36:            raise ValueError(f"canonical_input.structure.legs[{index}] is required")
services/pricing_payload_adapter.py:38:        pricing_legs.append(
services/pricing_payload_adapter.py:60:        "legs": pricing_legs,
services/robo_legs_service.py:2:# services/robo_legs_service.py
services/robo_legs_service.py:4:alteracao_40 -- get_legs_by_structure_id() como ponto de entrada canonico.
services/robo_legs_service.py:7:  - get_legs(): parametro renomeado para ref: StructureRef; aba extraida de ref
services/robo_legs_service.py:9:  get_legs(aba, timestamp).
services/robo_legs_service.py:15:from repositories.robo_legs_repository import RoboLegsRepository, RoboLegsRepoConfig
services/robo_legs_service.py:17:from validators.leg_validator import validate_legs
services/robo_legs_service.py:20:class RoboLegsService:
services/robo_legs_service.py:23:      - obtém legs com regra manual > rtd
services/robo_legs_service.py:27:    def __init__(self, repo: Optional[RoboLegsRepository] = None):
services/robo_legs_service.py:28:        self.repo = repo or RoboLegsRepository(RoboLegsRepoConfig())
services/robo_legs_service.py:30:    def get_legs(
services/robo_legs_service.py:40:        get_legs(ref=..., timestamp=...). Se o repo/fake for legado, usa
services/robo_legs_service.py:41:        get_legs(aba, timestamp).
services/robo_legs_service.py:46:            legs = self.repo.get_legs(ref=ref, timestamp=timestamp)
services/robo_legs_service.py:50:            legs = self.repo.get_legs(aba, timestamp)
services/robo_legs_service.py:53:            report = validate_legs(legs)
services/robo_legs_service.py:57:                    f"Legs inválidas: {first.code} field={first.field} aba={aba}"
services/robo_legs_service.py:59:        return legs
services/robo_legs_service.py:61:    def get_legs_by_structure_id(
services/robo_legs_service.py:69:        Delega para repo.get_legs_by_structure_id() e valida.
services/robo_legs_service.py:71:        legs = self.repo.get_legs_by_structure_id(
services/robo_legs_service.py:76:            report = validate_legs(legs)
services/robo_legs_service.py:80:                    f"Legs inválidas: {first.code} field={first.field} "
services/robo_legs_service.py:83:        return legs
services/robo_legs_status_service.py:3:alteracao_57c -- RoboLegsStatusService.
services/robo_legs_status_service.py:15:from dto.robo_legs_status_dto import DataFreshness, RoboLegsStatusDTO
services/robo_legs_status_service.py:16:from repositories.robo_legs_repository import RoboLegsRepository
services/robo_legs_status_service.py:17:from repositories.robo_legs_status_repository import (
services/robo_legs_status_service.py:18:    RoboLegsStatusRepository,
services/robo_legs_status_service.py:19:    RoboLegsStatusRepoConfig,
services/robo_legs_status_service.py:26:class RoboLegsFreshnessConfig:
services/robo_legs_status_service.py:30:class RoboLegsStatusService:
services/robo_legs_status_service.py:33:        repo: Optional[RoboLegsRepository] = None,
services/robo_legs_status_service.py:34:        status_repo: Optional[RoboLegsStatusRepository] = None,
services/robo_legs_status_service.py:35:        freshness: Optional[RoboLegsFreshnessConfig] = None,
services/robo_legs_status_service.py:37:        self.repo = repo or RoboLegsRepository()
services/robo_legs_status_service.py:38:        self.status_repo = status_repo or RoboLegsStatusRepository(
services/robo_legs_status_service.py:39:            RoboLegsStatusRepoConfig()
services/robo_legs_status_service.py:41:        self.freshness = freshness or RoboLegsFreshnessConfig()
services/robo_legs_status_service.py:48:    ) -> RoboLegsStatusDTO:
services/robo_legs_status_service.py:78:            return RoboLegsStatusDTO(
services/robo_legs_status_service.py:99:        return RoboLegsStatusDTO(
services/structure_events_service.py:296:        com quantidades efetivas nas legs.
services/structure_events_service.py:320:            "legs": [
services/structure_events_service.py:325:                for leg in (structure.get("legs") or [])
services/structure_events_service.py:353:            target_legs = self._target_legs_for_event(effective["legs"], event)
services/structure_events_service.py:355:            if not target_legs:
services/structure_events_service.py:360:                self._reduce_target_legs(target_legs, event.get("quantity"))
services/structure_events_service.py:365:                self._zero_target_legs(target_legs)
services/structure_events_service.py:371:                    self._zero_target_legs(target_legs)
services/structure_events_service.py:373:                    self._reduce_target_legs(target_legs, event.get("quantity"))
services/structure_events_service.py:378:                self._zero_target_legs(target_legs)
services/structure_events_service.py:384:            for leg in effective.get("legs", [])
services/structure_events_service.py:385:        ) if effective.get("legs") else False
services/structure_events_service.py:430:    def _target_legs_for_event(
services/structure_events_service.py:432:        legs: list[dict[str, Any]],
services/structure_events_service.py:439:            return legs
services/structure_events_service.py:443:        for leg in legs:
services/structure_events_service.py:460:    def _reduce_target_legs(
services/structure_events_service.py:462:        target_legs: list[dict[str, Any]],
services/structure_events_service.py:476:        for leg in target_legs:
services/structure_events_service.py:483:    def _zero_target_legs(self, target_legs: list[dict[str, Any]]) -> None:
services/structure_events_service.py:484:        for leg in target_legs:
services/structure_input_mapper.py:89:    legs = structure.get("legs", [])
services/structure_input_mapper.py:95:        "legs": [
services/structure_input_mapper.py:97:            for leg in legs
services/structure_leg_rtd_enrichment_service.py:1:"""Service de enriquecimento de legs de estruturas via RTD.

## Grep - payoff/decisao/rejeicao/logs
ATT/tests/conftest.py:172:        "HIDDEN": "hidden", "ACTIVE": "active",
ATT/tests/test_canonical_input_service.py:3:from services.canonical_input_service import CanonicalInputService
ATT/tests/test_canonical_input_service.py:67:class CanonicalInputServiceTests(unittest.TestCase):
ATT/tests/test_canonical_input_service.py:68:    def test_should_always_prefer_canonical_legs_when_structure_already_has_legs(self):
ATT/tests/test_canonical_input_service.py:88:        service = CanonicalInputService(
ATT/tests/test_canonical_input_service.py:95:            prefer_canonical_legs=True,
ATT/tests/test_canonical_input_service.py:104:        self.assertEqual(result["meta"]["legs_source"], "canonical")
ATT/tests/test_canonical_input_service.py:110:    def test_should_use_legacy_robo_only_when_no_canonical_legs_exist(self):
ATT/tests/test_canonical_input_service.py:119:        service = CanonicalInputService(
ATT/tests/test_canonical_input_service.py:153:    def test_should_return_empty_when_no_canonical_legs_and_fallback_disabled(self):
ATT/tests/test_canonical_input_service.py:162:        service = CanonicalInputService(
ATT/tests/test_canonical_input_service.py:192:        service = CanonicalInputService(
ATT/tests/test_canonical_input_service.py:195:            prefer_canonical_legs=True,
ATT/tests/test_canonical_input_service.py:255:        service = CanonicalInputService(
ATT/tests/test_canonical_input_service.py:259:            prefer_canonical_legs=True,
ATT/tests/test_canonical_input_service.py:292:        service = CanonicalInputService(
ATT/tests/test_canonical_input_service.py:296:            prefer_canonical_legs=True,
ATT/tests/test_canonical_pricing_facade.py:6:from services.canonical_pricing_facade import _snapshot_result_to_payload
ATT/tests/test_canonical_pricing_facade.py:15:        "manual_overrides": [],
ATT/tests/test_canonical_pricing_facade.py:76:        manual_overrides=["price"],
ATT/tests/test_canonical_pricing_facade.py:95:        "manual_overrides": ["price"],
ATT/tests/test_canonical_pricing_facade.py:159:def test_snapshot_result_to_payload_rejects_missing_or_invalid_spot(tmp_path):
ATT/tests/test_canonical_pricing_facade_manual_without_alias.py:1:import services.canonical_pricing_facade as facade_module
ATT/tests/test_canonical_pricing_facade_manual_without_alias.py:82:    facade = facade_module.CanonicalPricingFacade(
ATT/tests/test_canonical_pricing_facade_manual_without_alias.py:96:    assert response["pricing_payload"]["meta"]["snapshot_source"] == "canonical_manual_without_alias"
ATT/tests/test_canonical_validators.py:1:from domain.canonical_validators import validate_canonical_input
ATT/tests/test_canonical_validators.py:4:def test_validate_canonical_input_should_not_require_alias_legacy_aba():
ATT/tests/test_canonical_validators.py:5:    canonical_input = {
ATT/tests/test_canonical_validators.py:30:    errors = validate_canonical_input(canonical_input)
ATT/tests/test_contracts.py:1:from domain.contracts import CanonicalStructureMarketInput
ATT/tests/test_contracts.py:4:def test_canonical_structure_market_input_from_dict_and_to_dict_without_alias_legacy_aba():
ATT/tests/test_contracts.py:32:            "legs_source": "canonical",
ATT/tests/test_contracts.py:38:    canonical_input = CanonicalStructureMarketInput.from_dict(payload)
ATT/tests/test_contracts.py:39:    result = canonical_input.to_dict()
ATT/tests/test_contracts.py:45:    assert result["meta"]["legs_source"] == "canonical"
ATT/tests/test_decision.py:1:from domain.decision import compute_decision_from_payoff
ATT/tests/test_decision.py:4:def test_compute_decision_from_payoff_should_work_without_alias_legacy_aba():
ATT/tests/test_decision.py:6:    Garante que compute_decision_from_payoff funciona com payoff canônico
ATT/tests/test_decision.py:17:    result = compute_decision_from_payoff(
ATT/tests/test_decision.py:22:    assert "decision" in result
ATT/tests/test_decision.py:24:    assert result["decision"] in ("HOLD", "WATCH", "PREPARE", "PREPARE_ROLL", "CLOSE_REOPEN", "CLOSE")
ATT/tests/test_decision.py:26:    # com dte_min=12 > dte_gate=7 não há gate, decisão depende do ratio
ATT/tests/test_derived_service.py:68:def test_merge_meta_should_enrich_with_canonical_identity():
ATT/tests/test_derived_service.py:75:        input_meta={"legs_source": "canonical"},
ATT/tests/test_derived_service.py:83:    assert result["input_meta"]["legs_source"] == "canonical"
ATT/tests/test_derived_service.py:86:def test_save_payoff_from_canonical_payload_should_use_resolved_storage_key(monkeypatch):
ATT/tests/test_derived_service.py:110:    result = ds.save_payoff_from_canonical_payload(payload)
ATT/tests/test_derived_service.py:125:def test_save_decision_from_canonical_payload_should_enrich_meta(monkeypatch):
ATT/tests/test_derived_service.py:128:    def fake_save_decision(ref, decision, timestamp=None):
ATT/tests/test_derived_service.py:130:        captured["decision"] = decision
ATT/tests/test_derived_service.py:134:    monkeypatch.setattr(ds, "save_decision", fake_save_decision)
ATT/tests/test_derived_service.py:141:    result = ds.save_decision_from_canonical_payload(
ATT/tests/test_derived_service.py:142:        decision=payload,
ATT/tests/test_derived_service.py:151:    assert captured["decision"]["meta"]["origin"] == "test"
ATT/tests/test_derived_service.py:152:    assert captured["decision"]["meta"]["structure_id"] == 321
ATT/tests/test_derived_service.py:153:    assert captured["decision"]["meta"]["structure_name"] == "Fence"
ATT/tests/test_derived_service.py:154:    assert captured["decision"]["meta"]["underlying_asset"] == "VALE3"
ATT/tests/test_derived_service.py:155:    assert captured["decision"]["meta"]["storage_key"] == "structure:321"
ATT/tests/test_derived_service.py:159:def test_save_decision_preserva_structure_id_explicito_sem_alias(monkeypatch):
ATT/tests/test_derived_service.py:171:    def fake_insert_structure_decision(conn, timestamp, aba, decision_dict):
ATT/tests/test_derived_service.py:174:        captured["decision_dict"] = decision_dict
ATT/tests/test_derived_service.py:180:    monkeypatch.setattr(svc, "insert_structure_decision", fake_insert_structure_decision)
ATT/tests/test_derived_service.py:182:    result = svc.save_decision(
ATT/tests/test_derived_service.py:184:        decision={
ATT/tests/test_derived_service.py:186:            "decision": "hold",
ATT/tests/test_derived_service.py:194:    assert captured["decision_dict"]["structure_id"] == 7
ATT/tests/test_derived_service.py:195:    assert captured["decision_dict"]["meta"]["structure_id"] == 7
ATT/tests/test_derived_service.py:196:    assert captured["decision_dict"]["meta"]["storage_key"] == "structure:7"
ATT/tests/test_import_rtd_links_to_option_quotes.py:162:    assert stats.rows_ignored == 0
ATT/tests/test_legacy_structure_legs_importer.py:19:            status TEXT NOT NULL DEFAULT 'active',
ATT/tests/test_legacy_structure_legs_importer.py:62:            'active', NULL, '2026-05-19T10:00:00+00:00',
ATT/tests/test_legacy_structure_legs_importer_integration.py:22:            status TEXT NOT NULL DEFAULT 'active',
ATT/tests/test_legacy_structure_legs_importer_integration.py:50:        CREATE TABLE manual_analise_robo_legs (
ATT/tests/test_legacy_structure_legs_importer_integration.py:96:            'active', NULL,
ATT/tests/test_legacy_structure_legs_importer_integration.py:106:def _insert_existing_canonical_leg(db_path, structure_id=123):
ATT/tests/test_legacy_structure_legs_importer_integration.py:147:def _insert_legacy_manual_leg(db_path):
ATT/tests/test_legacy_structure_legs_importer_integration.py:151:        INSERT INTO manual_analise_robo_legs (
ATT/tests/test_legacy_structure_legs_importer_integration.py:158:            185.0, 5000, 'manualput185', '2026-06-20', 1.23
ATT/tests/test_legacy_structure_legs_importer_integration.py:173:    _insert_existing_canonical_leg(db_path)
ATT/tests/test_legacy_structure_legs_importer_integration.py:175:    # Insere RTD e MANUAL no mesmo timestamp.
ATT/tests/test_legacy_structure_legs_importer_integration.py:176:    # RoboLegsRepository deve preferir MANUAL.
ATT/tests/test_legacy_structure_legs_importer_integration.py:178:    _insert_legacy_manual_leg(db_path)
ATT/tests/test_legacy_structure_legs_importer_integration.py:218:    assert imported_leg["symbol"] == "MANUALPUT185"
ATT/tests/test_legacy_structure_legs_importer_integration.py:227:    # quando havia MANUAL disponivel.
ATT/tests/test_legacy_structure_legs_reader.py:127:        CREATE TABLE manual_analise_robo_legs (
ATT/tests/test_legacy_structure_legs_reader.py:176:        VALUES (123, 'BOVA teste', 'BOVA11', 'BOVA_ALIAS', 'active')
ATT/tests/test_legacy_structure_legs_reader.py:239:        VALUES (123, 'BOVA teste', 'BOVA11', NULL, 'active')
ATT/tests/test_market_snapshot_selector.py:16:    def __init__(self, *, manual=None, rtd_option_quotes=None, rtd=None):
ATT/tests/test_market_snapshot_selector.py:17:        self.manual = manual or []
ATT/tests/test_market_snapshot_selector.py:21:    def get_manual_legs(self, ref):
ATT/tests/test_market_snapshot_selector.py:22:        return self.manual
ATT/tests/test_market_snapshot_selector.py:31:def test_selector_prioritizes_rtd_option_quotes_over_legacy_rtd_when_no_manual_exists():
ATT/tests/test_market_snapshot_selector.py:47:    assert result.manual_overrides == []
ATT/tests/test_market_snapshot_selector.py:50:def test_selector_keeps_manual_leg_ahead_of_rtd_option_quotes():
ATT/tests/test_market_snapshot_selector.py:51:    manual_leg = _leg("BOVAE195", "manual", 1.30)
ATT/tests/test_market_snapshot_selector.py:57:            manual=[manual_leg],
ATT/tests/test_market_snapshot_selector.py:66:    assert result.source == SnapshotSource.MANUAL
ATT/tests/test_market_snapshot_selector.py:67:    assert result.legs == [manual_leg]
ATT/tests/test_market_snapshot_selector.py:68:    assert result.manual_overrides == ["BOVAE195"]
ATT/tests/test_orchestrator_run_methods.py:2:Testes para os métodos run_payoff e run_decision
ATT/tests/test_orchestrator_run_methods.py:17:    run_decision,
ATT/tests/test_orchestrator_run_methods.py:125:    @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input")
ATT/tests/test_orchestrator_run_methods.py:133:        canonical = mock_compute.call_args[0][0]
ATT/tests/test_orchestrator_run_methods.py:134:        assert canonical["structure"]["structure_id"] == "struct-001"
ATT/tests/test_orchestrator_run_methods.py:135:        assert canonical["market"]["spot_price"] == 50.0
ATT/tests/test_orchestrator_run_methods.py:138:    @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input")
ATT/tests/test_orchestrator_run_methods.py:150:    @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input")
ATT/tests/test_orchestrator_run_methods.py:157:        canonical = mock_compute.call_args[0][0]
ATT/tests/test_orchestrator_run_methods.py:158:        assert canonical["meta"] == {"tag": "ci"}
ATT/tests/test_orchestrator_run_methods.py:160:    @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input")
ATT/tests/test_orchestrator_run_methods.py:172:# Testes: run_decision
ATT/tests/test_orchestrator_run_methods.py:175:class TestRunDecision:
ATT/tests/test_orchestrator_run_methods.py:177:    @patch("services.calculation_orchestrator.compute_decision_from_contract")
ATT/tests/test_orchestrator_run_methods.py:179:        mock_decide.return_value = {"decision": "hold", "score": 0.7}
ATT/tests/test_orchestrator_run_methods.py:182:        result = run_decision(req, pl_atual=200.0, pl_max=500.0, dte_min=10)
ATT/tests/test_orchestrator_run_methods.py:189:        assert result == {"decision": "hold", "score": 0.7}
ATT/tests/test_orchestrator_run_methods.py:191:    @patch("services.calculation_orchestrator.compute_decision_from_contract")
ATT/tests/test_orchestrator_run_methods.py:197:        run_decision(req, payoff=payoff, pl_max=600.0, pl_atual=100.0)
ATT/tests/test_orchestrator_run_methods.py:202:    @patch("services.calculation_orchestrator.compute_decision_from_contract")
ATT/tests/test_orchestrator_run_methods.py:207:        run_decision(req)
ATT/tests/test_orchestrator_run_methods.py:214:    @patch("services.calculation_orchestrator.compute_decision_from_contract")
ATT/tests/test_orchestrator_run_methods.py:219:        run_decision(req, pl_max=300.0)
ATT/tests/test_orchestrator_run_methods.py:224:    @patch("services.calculation_orchestrator.compute_decision_from_contract")
ATT/tests/test_orchestrator_run_methods.py:226:        expected = {"decision": "close", "reason": "dte_gate"}
ATT/tests/test_orchestrator_run_methods.py:230:        result = run_decision(req, pl_max=100.0, pl_atual=80.0, dte_min=2)
ATT/tests/test_orchestrator_run_methods.py:246:        pytest.importorskip("domain.payoff")
ATT/tests/test_orchestrator_run_methods.py:263:            pytest.skip(f"Dominio indisponivel ou mal configurado: {exc}")
ATT/tests/test_payoff_canonical.py:1:from domain.payoff import compute_payoff_from_canonical_input
ATT/tests/test_payoff_canonical.py:4:def test_compute_payoff_from_canonical_input_should_preserve_canonical_metadata():
ATT/tests/test_payoff_canonical.py:5:    canonical_input = {
ATT/tests/test_payoff_canonical.py:32:            "legs_source": "canonical",
ATT/tests/test_payoff_canonical.py:37:    result = compute_payoff_from_canonical_input(canonical_input)
ATT/tests/test_payoff_canonical.py:43:    assert result["input_meta"]["legs_source"] == "canonical"
ATT/tests/test_payoff_chart.py:85:        chart._last_decision_data  = {}
ATT/tests/test_payoff_chart.py:332:    def test_update_chart_saves_decision_data(self):
ATT/tests/test_payoff_chart.py:334:        dd  = {"structure_id": "collar_1", "decision": "BUY", "spot_ref": 100.0}
ATT/tests/test_payoff_chart.py:335:        self.chart.update_chart(pts, decision_data=dd)
ATT/tests/test_payoff_chart.py:336:        self.assertEqual(self.chart._last_decision_data["structure_id"], "collar_1")
ATT/tests/test_payoff_chart.py:352:        result = self.chart.update_chart(pts, decision_data={"spot_ref": 100.0})
ATT/tests/test_payoff_chart.py:357:        result = self.chart.update_chart(_linear_points(), decision_data={})
ATT/tests/test_payoff_chart.py:395:        dd  = {"structure_id": "strangle_X", "aba": "old_aba", "decision": "BUY"}
ATT/tests/test_payoff_chart.py:396:        self.chart.update_chart(pts, decision_data=dd)
ATT/tests/test_payoff_chart.py:402:        dd  = {"aba": "straddle_Y", "decision": "SELL"}
ATT/tests/test_payoff_chart.py:403:        self.chart.update_chart(pts, decision_data=dd)
ATT/tests/test_payoff_chart.py:427:    def test_update_chart_none_decision_data(self):
ATT/tests/test_payoff_chart.py:428:        result = self.chart.update_chart(_linear_points(), decision_data=None)
ATT/tests/test_payoff_chart.py:442:    def test_update_chart_invalid_pl_skipped(self):
ATT/tests/test_position_side.py:47:def test_normalize_position_side_rejects_invalid_values(raw):
ATT/tests/test_pricing_execution_app_service.py:4:class FakeCanonicalPricingFacade:
ATT/tests/test_pricing_execution_app_service.py:52:        canonical_pricing_facade=FakeCanonicalPricingFacade(response),
ATT/tests/test_pricing_execution_app_service.py:58:    facade = FakeCanonicalPricingFacade(response={
ATT/tests/test_pricing_execution_app_service.py:62:        canonical_pricing_facade=facade,
ATT/tests/test_pricing_execution_app_service.py:72:    facade = FakeCanonicalPricingFacade(response=raw_response)
ATT/tests/test_pricing_execution_app_service.py:74:        canonical_pricing_facade=facade,
ATT/tests/test_pricing_execution_app_service.py:81:def test_execute_pricing_rejects_invalid_structure_id():
ATT/tests/test_pricing_execution_app_service.py:82:    facade = FakeCanonicalPricingFacade(response={})
ATT/tests/test_pricing_execution_app_service.py:84:        canonical_pricing_facade=facade,
ATT/tests/test_pricing_execution_app_service.py:95:def test_execute_pricing_rejects_invalid_reference_date():
ATT/tests/test_pricing_execution_app_service.py:96:    facade = FakeCanonicalPricingFacade(response={})
ATT/tests/test_pricing_execution_app_service.py:98:        canonical_pricing_facade=facade,
ATT/tests/test_pricing_execution_app_service.py:110:    facade = FakeCanonicalPricingFacade(
ATT/tests/test_pricing_execution_app_service.py:114:        canonical_pricing_facade=facade,
ATT/tests/test_pricing_execution_persistence_service.py:194:            "snapshot_source": "manual",
ATT/tests/test_pricing_execution_persistence_service.py:223:            "decision": {
ATT/tests/test_pricing_execution_persistence_service.py:261:    assert call["decision_json"] == {
ATT/tests/test_pricing_execution_query_service.py:211:def test_list_execution_summaries_rejects_invalid_structure_id():
ATT/tests/test_pricing_execution_query_service.py:223:def test_list_execution_summaries_rejects_empty_underlying_asset():
ATT/tests/test_pricing_execution_query_service.py:235:def test_list_execution_summaries_rejects_invalid_status():
ATT/tests/test_pricing_execution_query_service.py:247:def test_list_execution_summaries_rejects_invalid_reference_date():
ATT/tests/test_pricing_execution_query_service.py:295:def test_paginate_execution_summaries_rejects_invalid_page():
ATT/tests/test_pricing_execution_query_service.py:307:def test_paginate_execution_summaries_rejects_invalid_page_size():
ATT/tests/test_pricing_execution_query_service.py:358:def test_get_execution_rejects_invalid_execution_id():
ATT/tests/test_pricing_input_service.py:6:class FakeCanonicalInputService:
ATT/tests/test_pricing_input_service.py:7:    def __init__(self, canonical_input=None, error=None):
ATT/tests/test_pricing_input_service.py:8:        self.canonical_input = canonical_input
ATT/tests/test_pricing_input_service.py:23:        return self.canonical_input
ATT/tests/test_pricing_input_service.py:26:def test_build_pricing_payload_calls_canonical_input_service(monkeypatch):
ATT/tests/test_pricing_input_service.py:27:    canonical_input = {
ATT/tests/test_pricing_input_service.py:43:    fake_canonical_service = FakeCanonicalInputService(canonical_input)
ATT/tests/test_pricing_input_service.py:57:    service = PricingInputService(canonical_input_service=fake_canonical_service)
ATT/tests/test_pricing_input_service.py:64:    assert fake_canonical_service.calls == [
ATT/tests/test_pricing_input_service.py:77:def test_build_pricing_payload_from_canonical_input_delegates_to_adapter(monkeypatch):
ATT/tests/test_pricing_input_service.py:78:    canonical_input = {
ATT/tests/test_pricing_input_service.py:94:    service = PricingInputService(canonical_input_service=None)
ATT/tests/test_pricing_input_service.py:96:    result = service.build_pricing_payload_from_canonical_input(canonical_input)
ATT/tests/test_pricing_input_service.py:98:    assert calls == [canonical_input]
ATT/tests/test_pricing_input_service.py:103:    canonical_input = {
ATT/tests/test_pricing_input_service.py:108:    fake_canonical_service = FakeCanonicalInputService(canonical_input)
ATT/tests/test_pricing_input_service.py:121:    service = PricingInputService(canonical_input_service=fake_canonical_service)
ATT/tests/test_pricing_input_service.py:125:    assert fake_canonical_service.calls == [
ATT/tests/test_pricing_input_service.py:137:def test_build_pricing_payload_propagates_canonical_input_service_error(monkeypatch):
ATT/tests/test_pricing_input_service.py:138:    fake_canonical_service = FakeCanonicalInputService(
ATT/tests/test_pricing_input_service.py:153:    service = PricingInputService(canonical_input_service=fake_canonical_service)
ATT/tests/test_pricing_input_service.py:158:    assert fake_canonical_service.calls == [
ATT/tests/test_pricing_input_service.py:167:def test_build_pricing_payload_from_canonical_input_propagates_adapter_error(monkeypatch):
ATT/tests/test_pricing_input_service.py:168:    canonical_input = {
ATT/tests/test_pricing_input_service.py:174:        raise ValueError("invalid canonical input")
ATT/tests/test_pricing_input_service.py:181:    service = PricingInputService(canonical_input_service=None)
ATT/tests/test_pricing_input_service.py:183:    with pytest.raises(ValueError, match="invalid canonical input"):
ATT/tests/test_pricing_input_service.py:184:        service.build_pricing_payload_from_canonical_input(canonical_input)
ATT/tests/test_pricing_payload_adapter.py:8:        canonical_input = {
ATT/tests/test_pricing_payload_adapter.py:35:        payload = to_pricing_payload(canonical_input)
ATT/tests/test_pricing_payload_adapter.py:42:        canonical_input = {
ATT/tests/test_pricing_payload_adapter.py:68:        payload = to_pricing_payload(canonical_input)
ATT/tests/test_pricing_payload_adapter.py:89:                canonical_input = {
ATT/tests/test_pricing_payload_adapter.py:115:                payload = to_pricing_payload(canonical_input)
ATT/tests/test_robo_leg_mapper.py:5:from services.robo_leg_mapper import to_canonical_leg
ATT/tests/test_robo_leg_mapper.py:8:def test_to_canonical_leg_should_map_long_call():
ATT/tests/test_robo_leg_mapper.py:19:    result = to_canonical_leg(leg)
ATT/tests/test_robo_leg_mapper.py:31:def test_to_canonical_leg_should_map_short_put():
ATT/tests/test_robo_leg_mapper.py:42:    result = to_canonical_leg(leg)
ATT/tests/test_robo_leg_mapper.py:50:def test_to_canonical_leg_should_raise_for_invalid_cv():
ATT/tests/test_robo_leg_mapper.py:62:        to_canonical_leg(leg)
ATT/tests/test_robo_leg_mapper.py:65:def test_to_canonical_leg_should_raise_for_invalid_call_put():
ATT/tests/test_robo_leg_mapper.py:77:        to_canonical_leg(leg)
ATT/tests/test_robo_leg_mapper.py:80:def test_to_canonical_leg_should_raise_for_invalid_strike():
ATT/tests/test_robo_leg_mapper.py:92:        to_canonical_leg(leg)
ATT/tests/test_robo_leg_mapper.py:95:def test_to_canonical_leg_should_raise_for_invalid_quant():
ATT/tests/test_robo_leg_mapper.py:107:        to_canonical_leg(leg)
ATT/tests/test_robo_legs_repository.py:11:        CREATE TABLE manual_analise_robo_legs (
ATT/tests/test_robo_legs_repository.py:42:def test_get_legs_prefers_manual_over_rtd(tmp_path):
ATT/tests/test_robo_legs_repository.py:49:        INSERT INTO manual_analise_robo_legs
ATT/tests/test_robo_legs_repository.py:72:def test_get_legs_falls_back_to_rtd_when_manual_empty(tmp_path):
ATT/tests/test_robo_legs_repository.py:96:def test_has_manual_detects_existing_row(tmp_path):
ATT/tests/test_robo_legs_repository.py:103:        INSERT INTO manual_analise_robo_legs
ATT/tests/test_robo_legs_repository.py:112:    assert repo.has_manual("AB3", "2026-05-19 10:00:00") is True
ATT/tests/test_robo_legs_repository.py:113:    assert repo.has_manual("AB3", "2026-05-19 11:00:00") is False
ATT/tests/test_robo_legs_repository.py:116:def test_list_timestamps_prefers_manual_then_rtd(tmp_path):
ATT/tests/test_robo_legs_repository.py:123:        INSERT INTO manual_analise_robo_legs
ATT/tests/test_robo_legs_repository.py:128:        INSERT INTO manual_analise_robo_legs
ATT/tests/test_robo_legs_repository.py:153:        INSERT INTO manual_analise_robo_legs
ATT/tests/test_robo_legs_service.py:27:        fonte=FonteType.MANUAL,
ATT/tests/test_robo_legs_service.py:60:        fonte=FonteType.MANUAL,
ATT/tests/test_robo_legs_status_repository.py:9:def test_latest_timestamps_returns_parsed_manual_and_rtd(tmp_path):
ATT/tests/test_robo_legs_status_repository.py:14:    conn.execute("CREATE TABLE manual_analise_robo_legs (aba TEXT, timestamp TEXT)")
ATT/tests/test_robo_legs_status_repository.py:18:        "INSERT INTO manual_analise_robo_legs (aba, timestamp) VALUES (?, ?)",
ATT/tests/test_robo_legs_status_repository.py:22:        "INSERT INTO manual_analise_robo_legs (aba, timestamp) VALUES (?, ?)",
ATT/tests/test_robo_legs_status_repository.py:36:    manual_latest, rtd_latest = repo.latest_timestamps("TESTE")
ATT/tests/test_robo_legs_status_repository.py:38:    assert manual_latest == datetime(2026, 5, 19, 11, 0, 0)
ATT/tests/test_robo_legs_status_repository.py:47:    conn.execute("CREATE TABLE manual_analise_robo_legs (aba TEXT, timestamp TEXT)")
ATT/tests/test_robo_legs_status_repository.py:56:    manual_latest, rtd_latest = repo.latest_timestamps("INEXISTENTE")
ATT/tests/test_robo_legs_status_repository.py:58:    assert manual_latest is None
ATT/tests/test_robo_legs_status_service.py:14:    def __init__(self, manual_latest=None, rtd_latest=None):
ATT/tests/test_robo_legs_status_service.py:15:        self._manual_latest = manual_latest
ATT/tests/test_robo_legs_status_service.py:21:        return self._manual_latest, self._rtd_latest
ATT/tests/test_robo_legs_status_service.py:31:        status_repo=DummyStatusRepo(manual_latest=None, rtd_latest=None),
ATT/tests/test_robo_legs_status_service.py:42:    assert result.manual_latest_ts is None
ATT/tests/test_robo_legs_status_service.py:48:def test_status_prefers_manual_when_manual_exists():
ATT/tests/test_robo_legs_status_service.py:49:    manual_latest = datetime(2026, 5, 19, 10, 0, 0)
ATT/tests/test_robo_legs_status_service.py:54:        status_repo=DummyStatusRepo(manual_latest=manual_latest, rtd_latest=rtd_latest),
ATT/tests/test_robo_legs_status_service.py:60:    assert result.chosen_fonte == FonteType.MANUAL
ATT/tests/test_robo_legs_status_service.py:61:    assert result.chosen_ts == manual_latest
ATT/tests/test_robo_legs_status_service.py:62:    assert result.manual_latest_ts == manual_latest
ATT/tests/test_robo_legs_status_service.py:68:def test_status_uses_rtd_when_manual_missing():
ATT/tests/test_robo_legs_status_service.py:73:        status_repo=DummyStatusRepo(manual_latest=None, rtd_latest=rtd_latest),
ATT/tests/test_robo_legs_status_service.py:81:    assert result.manual_latest_ts is None
ATT/tests/test_robo_legs_status_service.py:88:    manual_latest = datetime(2026, 5, 19, 10, 0, 0)
ATT/tests/test_robo_legs_status_service.py:92:        status_repo=DummyStatusRepo(manual_latest=manual_latest, rtd_latest=None),
ATT/tests/test_robo_legs_status_service.py:98:    assert result.chosen_fonte == FonteType.MANUAL
ATT/tests/test_robo_legs_status_service.py:104:    manual_latest = datetime(2026, 5, 19, 10, 5, 0)
ATT/tests/test_robo_legs_status_service.py:108:        status_repo=DummyStatusRepo(manual_latest=manual_latest, rtd_latest=None),
ATT/tests/test_robo_legs_status_service.py:119:    manual_latest = datetime(2026, 5, 19, 10, 0, 0)
ATT/tests/test_robo_legs_status_service.py:123:        status_repo=DummyStatusRepo(manual_latest=manual_latest, rtd_latest=None),
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:1:from services.canonical_input_service import CanonicalInputService
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:51:def test_rtd_legacy_fallback_can_feed_pricing_payload_when_no_canonical_legs_exist():
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:60:    canonical_service = CanonicalInputService(
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:64:        prefer_canonical_legs=True,
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:68:    canonical_input = canonical_service.build_structure_market_input(
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:73:    assert canonical_input["meta"]["legs_source"] == "legacy_fallback"
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:74:    assert canonical_input["meta"]["legacy_timestamp"] == "2026-05-18 10:00:00"
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:75:    assert canonical_input["meta"]["legacy_aba"] == "BOVA11"
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:76:    assert canonical_input["meta"]["legacy_key_source"] == "alias_legacy_aba"
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:77:    assert "alias_legacy_aba" not in canonical_input["structure"]
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:79:    canonical_leg = canonical_input["structure"]["legs"][0]
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:80:    assert canonical_leg["position_side"] == "COMPRADO"
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:81:    assert canonical_leg["option_type"] == "CALL"
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:82:    assert canonical_leg["symbol"] == "BOVAE195"
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:85:        canonical_input_service=canonical_service,
ATT/tests/test_run_derived_pipeline_rtd_integration.py:30:skipped: 0
ATT/tests/test_run_derived_pipeline_rtd_integration.py:38:        "skipped": 0,
ATT/tests/test_run_derived_pipeline_rtd_integration.py:83:            stdout="input_rows: 1\ninserted: 0\nupdated: 1\nskipped: 0\n",
ATT/tests/test_run_derived_pipeline_rtd_integration.py:87:    monkeypatch.setattr(module.subprocess, "run", fake_run)
ATT/tests/test_run_derived_pipeline_rtd_integration.py:99:    assert result["skipped"] == 0
ATT/tests/test_run_rtd_option_quotes_pipeline.py:128:def test_run_pipeline_dry_run_skips_audit(monkeypatch):
ATT/tests/test_structure_analysis_service.py:6:class FakeCanonicalInputService:
ATT/tests/test_structure_analysis_service.py:64:                "legs_source": "canonical",
ATT/tests/test_structure_analysis_service.py:71:class FakeInvalidCanonicalInputService:
ATT/tests/test_structure_analysis_service.py:104:                "legs_source": "canonical",
ATT/tests/test_structure_analysis_service.py:113:        canonical_input_service=FakeCanonicalInputService()
ATT/tests/test_structure_analysis_service.py:122:    assert "canonical_input" in result
ATT/tests/test_structure_analysis_service.py:125:    assert "decision" in result
ATT/tests/test_structure_analysis_service.py:127:    assert result["canonical_input"]["structure"]["structure_id"] == 1
ATT/tests/test_structure_analysis_service.py:128:    assert result["canonical_input"]["market"]["reference_date"] == "2026-05-15"
ATT/tests/test_structure_analysis_service.py:141:    decision = result["decision"]
ATT/tests/test_structure_analysis_service.py:142:    assert decision is not None
ATT/tests/test_structure_analysis_service.py:143:    assert decision["decision"] == "HOLD"
ATT/tests/test_structure_analysis_service.py:144:    assert decision["dte_min"] == 0
ATT/tests/test_structure_analysis_service.py:145:    assert "why" in decision
ATT/tests/test_structure_analysis_service.py:146:    assert "why_json" in decision
ATT/tests/test_structure_analysis_service.py:147:    assert isinstance(decision["why"], dict)
ATT/tests/test_structure_analysis_service.py:148:    assert "reasons" in decision["why"]
ATT/tests/test_structure_analysis_service.py:149:    assert "alternatives" in decision["why"]
ATT/tests/test_structure_analysis_service.py:154:        canonical_input_service=FakeCanonicalInputService()
ATT/tests/test_structure_analysis_service.py:166:    assert result["decision"]["dte_min"] == 9
ATT/tests/test_structure_analysis_service.py:169:def test_structure_analysis_service_analyze_returns_structured_decision_for_invalid_payoff():
ATT/tests/test_structure_analysis_service.py:171:        canonical_input_service=FakeInvalidCanonicalInputService()
ATT/tests/test_structure_analysis_service.py:180:    assert "decision" in result
ATT/tests/test_structure_analysis_service.py:181:    assert result["decision"] is not None
ATT/tests/test_structure_analysis_service.py:182:    assert result["decision"]["decision"] == "HOLD"
ATT/tests/test_structure_analysis_service.py:183:    assert result["decision"]["level"] == 0
ATT/tests/test_structure_analysis_service.py:184:    assert result["decision"]["why"]["error"] == "payoff is required"
ATT/tests/test_structure_analysis_service.py:185:    assert "validation_errors" in result["decision"]["why"]
ATT/tests/test_structure_analysis_service.py:190:        canonical_input_service=FakeCanonicalInputService()
ATT/tests/test_structure_analysis_service.py:206:    decision = result["decision"]
ATT/tests/test_structure_analysis_service.py:208:    assert decision is not None
ATT/tests/test_structure_analysis_service.py:209:    assert "why" in decision
ATT/tests/test_structure_analysis_service.py:210:    assert decision["why"]["thresholds_used"] == thresholds
ATT/tests/test_structure_analysis_service.py:211:    assert decision["why"]["dte_gate"] == 10
ATT/tests/test_structure_analysis_service.py:216:        canonical_input_service=FakeCanonicalInputService()
ATT/tests/test_structure_analysis_service.py:227:        for alternative in result["decision"]["why"]["alternatives"]
ATT/tests/test_structure_analysis_service.py:231:def test_structure_analysis_service_forwards_reference_date_to_canonical_service():
ATT/tests/test_structure_analysis_service.py:232:    fake_canonical_service = FakeCanonicalInputService()
ATT/tests/test_structure_analysis_service.py:234:        canonical_input_service=fake_canonical_service
ATT/tests/test_structure_analysis_service.py:242:    assert fake_canonical_service.calls == [
ATT/tests/test_structure_analysis_service.py:250:def test_structure_analysis_service_propagates_canonical_input_service_error():
ATT/tests/test_structure_analysis_service.py:251:    fake_canonical_service = FakeCanonicalInputService(
ATT/tests/test_structure_analysis_service.py:255:        canonical_input_service=fake_canonical_service
ATT/tests/test_structure_analysis_service.py:262:def test_structure_analysis_service_passes_effective_dte_to_decision(monkeypatch):
ATT/tests/test_structure_analysis_service.py:263:    fake_canonical_service = FakeCanonicalInputService()
ATT/tests/test_structure_analysis_service.py:265:        canonical_input_service=fake_canonical_service
ATT/tests/test_structure_analysis_service.py:270:    def fake_compute_dte_min_from_canonical_input(canonical_input):
ATT/tests/test_structure_analysis_service.py:273:    def fake_compute_payoff_from_canonical_input(canonical_input):
ATT/tests/test_structure_analysis_service.py:276:    def fake_compute_decision_from_payoff(
ATT/tests/test_structure_analysis_service.py:289:            "decision": "HOLD",
ATT/tests/test_structure_analysis_service.py:296:        "services.structure_analysis_service.compute_dte_min_from_canonical_input",
ATT/tests/test_structure_analysis_service.py:297:        fake_compute_dte_min_from_canonical_input,
ATT/tests/test_structure_analysis_service.py:300:        "services.structure_analysis_service.compute_payoff_from_canonical_input",
ATT/tests/test_structure_analysis_service.py:301:        fake_compute_payoff_from_canonical_input,
ATT/tests/test_structure_analysis_service.py:304:        "services.structure_analysis_service.compute_decision_from_payoff",
ATT/tests/test_structure_analysis_service.py:305:        fake_compute_decision_from_payoff,
ATT/tests/test_structure_analysis_service.py:324:    assert result["decision"]["dte_min"] == 3
ATT/tests/test_structure_analysis_service.py:328:    fake_canonical_service = FakeCanonicalInputService()
ATT/tests/test_structure_analysis_service.py:330:        canonical_input_service=fake_canonical_service
ATT/tests/test_structure_analysis_service.py:333:    def fake_compute_dte_min_from_canonical_input(canonical_input):
ATT/tests/test_structure_analysis_service.py:336:    def fake_compute_payoff_from_canonical_input(canonical_input):
ATT/tests/test_structure_analysis_service.py:339:    def fake_compute_decision_from_payoff(
ATT/tests/test_structure_analysis_service.py:347:            "decision": "HOLD",
ATT/tests/test_structure_analysis_service.py:354:        "services.structure_analysis_service.compute_dte_min_from_canonical_input",
ATT/tests/test_structure_analysis_service.py:355:        fake_compute_dte_min_from_canonical_input,
ATT/tests/test_structure_analysis_service.py:358:        "services.structure_analysis_service.compute_payoff_from_canonical_input",
ATT/tests/test_structure_analysis_service.py:359:        fake_compute_payoff_from_canonical_input,
ATT/tests/test_structure_analysis_service.py:362:        "services.structure_analysis_service.compute_decision_from_payoff",
ATT/tests/test_structure_analysis_service.py:363:        fake_compute_decision_from_payoff,
ATT/tests/test_structure_analysis_service.py:370:    assert result["decision"]["dte_min"] == 0
ATT/tests/test_structure_analysis_service.py:374:    fake_canonical_service = FakeCanonicalInputService()
ATT/tests/test_structure_analysis_service.py:376:        canonical_input_service=fake_canonical_service
ATT/tests/test_structure_analysis_service.py:381:    def fake_compute_dte_min_from_canonical_input(canonical_input):
ATT/tests/test_structure_analysis_service.py:384:    def fake_compute_payoff_from_canonical_input(canonical_input):
ATT/tests/test_structure_analysis_service.py:387:    def fake_compute_decision_from_payoff(
ATT/tests/test_structure_analysis_service.py:396:            "decision": "HOLD",
ATT/tests/test_structure_analysis_service.py:403:        "services.structure_analysis_service.compute_dte_min_from_canonical_input",
ATT/tests/test_structure_analysis_service.py:404:        fake_compute_dte_min_from_canonical_input,
ATT/tests/test_structure_analysis_service.py:407:        "services.structure_analysis_service.compute_payoff_from_canonical_input",
ATT/tests/test_structure_analysis_service.py:408:        fake_compute_payoff_from_canonical_input,
ATT/tests/test_structure_analysis_service.py:411:        "services.structure_analysis_service.compute_decision_from_payoff",
ATT/tests/test_structure_analysis_service.py:412:        fake_compute_decision_from_payoff,
ATT/tests/test_structure_analysis_service.py:423:    assert result["decision"]["dte_min"] == 9
ATT/tests/test_structure_analysis_service.py:424:class FakeCanonicalInputServiceWithMarketMetrics:
ATT/tests/test_structure_analysis_service.py:490:                "legs_source": "canonical",
ATT/tests/test_structure_analysis_service.py:499:        canonical_input_service=FakeCanonicalInputServiceWithMarketMetrics()
ATT/tests/test_structure_analysis_service.py:504:    def fake_compute_payoff_from_canonical_input(canonical_input):
ATT/tests/test_structure_analysis_service.py:507:    def fake_compute_decision_from_payoff(
ATT/tests/test_structure_analysis_service.py:516:            "decision": "HOLD",
ATT/tests/test_structure_analysis_service.py:523:        "services.structure_analysis_service.compute_payoff_from_canonical_input",
ATT/tests/test_structure_analysis_service.py:524:        fake_compute_payoff_from_canonical_input,
ATT/tests/test_structure_analysis_service.py:527:        "services.structure_analysis_service.compute_decision_from_payoff",
ATT/tests/test_structure_analysis_service.py:528:        fake_compute_decision_from_payoff,
ATT/tests/test_structure_analysis_service.py:545:        canonical_input_service=FakeCanonicalInputServiceWithMarketMetrics()
ATT/tests/test_structure_analysis_service.py:550:    def fake_compute_payoff_from_canonical_input(canonical_input):
ATT/tests/test_structure_analysis_service.py:553:    def fake_compute_decision_from_payoff(
ATT/tests/test_structure_analysis_service.py:562:            "decision": "HOLD",
ATT/tests/test_structure_analysis_service.py:569:        "services.structure_analysis_service.compute_payoff_from_canonical_input",
ATT/tests/test_structure_analysis_service.py:570:        fake_compute_payoff_from_canonical_input,
ATT/tests/test_structure_analysis_service.py:573:        "services.structure_analysis_service.compute_decision_from_payoff",
ATT/tests/test_structure_analysis_service.py:574:        fake_compute_decision_from_payoff,
ATT/tests/test_structure_analysis_service.py:594:        canonical_input_service=FakeCanonicalInputServiceWithMarketMetrics()
ATT/tests/test_structure_analysis_service.py:597:    def fake_compute_payoff_from_canonical_input(canonical_input):
ATT/tests/test_structure_analysis_service.py:600:    def fake_compute_decision_from_payoff(
ATT/tests/test_structure_analysis_service.py:608:            "decision": "HOLD",
ATT/tests/test_structure_analysis_service.py:615:        "services.structure_analysis_service.compute_payoff_from_canonical_input",
ATT/tests/test_structure_analysis_service.py:616:        fake_compute_payoff_from_canonical_input,
ATT/tests/test_structure_analysis_service.py:619:        "services.structure_analysis_service.compute_decision_from_payoff",
ATT/tests/test_structure_analysis_service.py:620:        fake_compute_decision_from_payoff,
ATT/tests/test_structure_editor_dialog.py:76:@unittest.skipUnless(_IMPORT_OK, "StructureEditorDialog nao importavel")
ATT/tests/test_structure_editor_dialog.py:126:@unittest.skipUnless(_IMPORT_OK, "StructureEditorDialog nao importavel")
ATT/tests/test_structure_editor_dialog.py:154:            "alias_legacy_aba": "BOVA11", "status": "active",
ATT/tests/test_structure_editor_dialog.py:161:        self.assertEqual(dlg._f_status.get(),     "active")
ATT/tests/test_structure_editor_dialog.py:172:            "alias_legacy_aba": None, "status": "active", "notes": None,
ATT/tests/test_structure_editor_dialog.py:195:@unittest.skipUnless(_IMPORT_OK, "StructureEditorDialog nao importavel")
ATT/tests/test_structure_editor_dialog.py:227:        dlg._f_status.set("active")
ATT/tests/test_structure_editor_dialog.py:240:        self.assertEqual(structure_arg["status"], "active")
ATT/tests/test_structure_editor_dialog.py:248:        dlg._f_status.set("active")
ATT/tests/test_structure_editor_dialog.py:274:        dlg._f_status.set("active")
ATT/tests/test_structure_editor_dialog.py:302:@unittest.skipUnless(_IMPORT_OK, "StructureEditorDialog nao importavel")
ATT/tests/test_structure_editor_dialog.py:323:            "alias_legacy_aba": None, "status": "active", "notes": None,
ATT/tests/test_structure_editor_dialog.py:337:        dlg._f_status.set("active")
ATT/tests/test_structure_editor_dialog.py:349:        dlg._f_status.set("active")
ATT/tests/test_structure_editor_dialog.py:359:        dlg._f_status.set("active")
ATT/tests/test_structure_editor_dialog.py:382:            self.skipTest(f"Import falhou: {_IMPORT_ERROR}")
ATT/tests/test_structure_editor_dialog.py:387:            self.skipTest("Modulo nao importavel")
ATT/tests/test_structure_editor_dialog.py:396:            self.skipTest("Modulo nao importavel")
ATT/tests/test_structure_editor_dialog.py:405:            self.skipTest("Modulo nao importavel")
ATT/tests/test_structure_editor_dialog.py:419:            self.skipTest("arquivo nao encontrado")
ATT/tests/test_structure_editor_dialog.py:634:def test_build_legs_payload_rejeita_quantity_invalido(quantity_value):
ATT/tests/test_structure_editor_integration.py:62:    _tk_mock.ACTIVE     = "active"
ATT/tests/test_structure_editor_integration.py:219:    _mpl_stub.is_interactive  = MagicMock(return_value=False)
ATT/tests/test_structure_editor_integration.py:295:    dlg._f_status     = _FakeVar("active")
ATT/tests/test_structure_editor_integration.py:444:        dlg._f_status.set("active")
ATT/tests/test_structure_editor_integration.py:525:        dlg._f_status.set("active")
ATT/tests/test_structure_events_api.py:15:    "status": "active",
ATT/tests/test_structure_events_api.py:32:    "source": "manual",
ATT/tests/test_structure_events_api.py:42:    "structure_status": "active",
ATT/tests/test_structure_events_api.py:56:    "ignored_events": [],
ATT/tests/test_structure_events_api.py:65:    "source": "manual",
ATT/tests/test_structure_events_effective_state.py:24:        "status": "active",
ATT/tests/test_structure_events_effective_state.py:104:def test_apply_events_cancelled_event_is_ignored():
ATT/tests/test_structure_events_effective_state.py:126:    assert result["operational_state"]["events_ignored_cancelled"] == 1
ATT/tests/test_structure_events_effective_state.py:129:def test_apply_events_manual_close_with_quantity_reduces_leg():
ATT/tests/test_structure_events_effective_state.py:137:                    "event_type": "manual_close",
ATT/tests/test_structure_events_effective_state.py:152:def test_apply_events_manual_close_without_quantity_zeros_leg():
ATT/tests/test_structure_events_effective_state.py:160:                    "event_type": "manual_close",
ATT/tests/test_structure_events_repository.py:32:        "status": "active",
ATT/tests/test_structure_events_repository.py:72:            "source": "manual",
ATT/tests/test_structure_events_repository.py:92:    assert event["source"] == "manual"
ATT/tests/test_structure_events_repository.py:131:            "source": "manual",
ATT/tests/test_structure_events_repository.py:167:            "source": "manual",
ATT/tests/test_structure_events_repository.py:198:            "event_type": "manual_close",
ATT/tests/test_structure_events_repository.py:200:            "source": "manual",
ATT/tests/test_structure_events_repository.py:222:            "source": "manual",
ATT/tests/test_structure_events_repository.py:231:            "source": "manual",
ATT/tests/test_structure_events_repository.py:270:            "status": "active",
ATT/tests/test_structure_events_repository.py:317:        "source": "manual",
ATT/tests/test_structure_events_service.py:97:        source="manual",
ATT/tests/test_structure_events_service.py:111:    assert record["source"] == "manual"
ATT/tests/test_structure_events_service.py:158:def test_register_manual_close_forces_manual_source(service):
ATT/tests/test_structure_events_service.py:159:    record = service.register_manual_close(
ATT/tests/test_structure_events_service.py:164:        notes="encerramento manual",
ATT/tests/test_structure_events_service.py:167:    assert record["event_type"] == "manual_close"
ATT/tests/test_structure_events_service.py:168:    assert record["source"] == "manual"
ATT/tests/test_structure_events_service.py:261:        "source": "manual",
ATT/tests/test_structure_events_service.py:280:def test_cancel_event_rejects_invalid_id(service):
ATT/tests/test_structure_leg_rtd_enrichment_service.py:18:def test_enrich_leg_from_symbol_uses_rtd_quote_and_returns_canonical_leg():
ATT/tests/test_structure_metrics.py:5:    compute_dte_min_from_canonical_input,
ATT/tests/test_structure_metrics.py:13:    compute_structure_metrics_from_canonical_input,
ATT/tests/test_structure_metrics.py:34:def test_compute_dte_min_from_canonical_input():
ATT/tests/test_structure_metrics.py:35:    canonical_input = {
ATT/tests/test_structure_metrics.py:62:    assert compute_dte_min_from_canonical_input(canonical_input) == 2
ATT/tests/test_structure_metrics.py:228:def test_compute_structure_metrics_from_canonical_input():
ATT/tests/test_structure_metrics.py:229:    canonical_input = {
ATT/tests/test_structure_metrics.py:260:    result = compute_structure_metrics_from_canonical_input(canonical_input)
ATT/tests/test_structures_api.py:34:    "status": "active",
ATT/tests/test_structures_api.py:436:    def test_atualiza_status_para_active(self, client):
ATT/tests/test_structures_api.py:438:        resp = tc.patch("/structures/1", json={"status": "active"})
ATT/tests/test_structures_api.py:474:        """Status fora de {active, archived} deve ser rejeitado pelo schema."""
ATT/tests/test_structures_api.py:584:        assert resp.json()["status"] in ("active", "archived")
ATT/tests/test_structures_archive_wiring.py:8:@unittest.skip("Requer display Tkinter -- headless nao suportado").
ATT/tests/test_structures_archive_wiring.py:185:        structure = {"id": selected_id, "name": "BOVA11 Condor", "status": "active"}
ATT/tests/test_structures_archive_wiring.py:261:            structure={"id": 7, "name": "PETR4 Trava", "status": "active"},
ATT/tests/test_structures_archive_wiring.py:298:            structure={"id": 3, "name": "BOVA11 Condor", "status": "active"},
ATT/tests/test_structures_archive_wiring.py:324:            structure={"id": 5, "name": "VALE3 Spread", "status": "active"},
ATT/tests/test_structures_archive_wiring.py:507:# 5. Testes Tk-dependentes (skip em headless)
ATT/tests/test_structures_archive_wiring.py:510:@unittest.skip("Requer display Tkinter -- headless nao suportado")
ATT/tests/test_structures_archive_wiring.py:514:    Executar manualmente em ambiente com display disponivel.
ATT/tests/test_structures_archive_wiring.py:538:                " alias_legacy_aba TEXT, status TEXT DEFAULT 'active', "
ATT/tests/test_structures_archive_wiring.py:575:                " alias_legacy_aba TEXT, status TEXT DEFAULT 'active', "
ATT/tests/test_structures_legs_endpoints.py:10:    Fix validado: leg_order >= 0 (era >= 1, rejeitava leg_order=0).
ATT/tests/test_structures_legs_endpoints.py:46:    "status":            "active",
ATT/tests/test_structures_repository.py:19:        "status": "active",
ATT/tests/test_structures_repository.py:49:    assert structure["status"] == "active"
ATT/tests/test_structures_repository.py:78:    active_id = repo.create_structure(valid_structure_payload())
ATT/tests/test_structures_repository.py:83:            "status": "active",
ATT/tests/test_structures_repository.py:90:    assert [item["id"] for item in result] == [active_id]
ATT/tests/test_structures_repository.py:99:            "status": "active",
ATT/tests/test_system_snapshots_repository.py:30:            "active",
ATT/tests/test_system_snapshots_repository.py:121:        decision_json={"action": "hold"},
ATT/tests/test_system_snapshots_repository.py:123:        operation_state_json={"state": "active"},
ATT/tests/test_system_snapshots_repository.py:168:    assert snapshot["decision_json"] == {"action": "hold"}
ATT/tests/test_system_snapshots_repository.py:170:    assert snapshot["operation_state_json"] == {"state": "active"}
ATT/tests/test_system_snapshots_schema.py:69:        "decision_json",
ATT/tests/test_ui_data_migration.py:27:def decisions(model):
ATT/tests/test_ui_data_migration.py:28:    return model.get_decisions()
ATT/tests/test_ui_data_migration.py:41:        pytest.skip("Sem estruturas no banco de migração")
ATT/tests/test_ui_data_migration.py:46:def non_empty_decisions(decisions):
ATT/tests/test_ui_data_migration.py:47:    if not decisions:
ATT/tests/test_ui_data_migration.py:48:        pytest.skip("Sem decisões no banco de migração")
ATT/tests/test_ui_data_migration.py:49:    return decisions
ATT/tests/test_ui_data_migration.py:86:# Nível 2 -- get_decisions() com structure_id
ATT/tests/test_ui_data_migration.py:89:def test_decisions_nao_vazia(non_empty_decisions):
ATT/tests/test_ui_data_migration.py:90:    assert len(non_empty_decisions) > 0, "Deve haver ao menos uma decisão no banco"
ATT/tests/test_ui_data_migration.py:93:def test_decisions_tem_structure_id(decisions):
ATT/tests/test_ui_data_migration.py:94:    for d in decisions:
ATT/tests/test_ui_data_migration.py:98:def test_decisions_tem_aba(decisions):
ATT/tests/test_ui_data_migration.py:99:    for d in decisions:
ATT/tests/test_ui_data_migration.py:103:def test_structure_id_igual_a_aba(decisions):
ATT/tests/test_ui_data_migration.py:108:    for d in decisions:
ATT/tests/test_ui_data_migration.py:120:def test_decisions_tem_timestamp(decisions):
ATT/tests/test_ui_data_migration.py:121:    for d in decisions:
ATT/tests/test_ui_data_migration.py:137:    filtered = model.get_decisions(filters={"structure_id": sid_str})
ATT/tests/test_ui_data_migration.py:142:            f"Decisao filtrada com structure_id errado: {d['structure_id']!r} != {sid_int}"
ATT/tests/test_ui_data_migration.py:146:def test_filtro_por_aba_continuidade(model, decisions):
ATT/tests/test_ui_data_migration.py:149:    Verificamos que filtrar por aba de uma decisao real retorna >= 1 resultado
ATT/tests/test_ui_data_migration.py:152:    if not decisions:
ATT/tests/test_ui_data_migration.py:153:        pytest.skip("Sem decisoes para testar filtro por aba")
ATT/tests/test_ui_data_migration.py:154:    aba_real = decisions[0]["aba"]        # ex: 'SBSP3'
ATT/tests/test_ui_data_migration.py:155:    filtered_aba = model.get_decisions(filters={"aba": aba_real})
ATT/tests/test_ui_data_migration.py:162:            f"Decisao com aba errada: esperado '{aba_real}', recebido '{d['aba']}'"
ATT/tests/test_ui_data_migration.py:170:def test_payoff_curve_info_retorna_dados(model, non_empty_decisions):
ATT/tests/test_ui_data_migration.py:171:    d0 = non_empty_decisions[0]
ATT/tests/test_ui_data_migration.py:177:def test_payoff_curve_info_tem_structure_id(model, non_empty_decisions):
ATT/tests/test_ui_data_migration.py:178:    d0 = non_empty_decisions[0]
ATT/tests/test_ui_data_migration.py:183:def test_payoff_curve_info_aba_continuidade(model, non_empty_decisions):
ATT/tests/test_ui_data_migration.py:184:    d0 = non_empty_decisions[0]
ATT/tests/test_ui_data_migration.py:192:def test_payoff_curve_info_pontos_validos(model, non_empty_decisions):
ATT/tests/test_ui_data_migration.py:193:    d0 = non_empty_decisions[0]
UI/components/decisions_grid.py:1:# UI/components/decisions_grid.py
UI/components/decisions_grid.py:9:class DecisionsGrid(ttk.LabelFrame):
UI/components/decisions_grid.py:27:            "decision",
UI/components/decisions_grid.py:45:        self.tree.heading("decision", text="Decisão")
UI/components/decisions_grid.py:55:        self.tree.column("decision", width=100, anchor="center")
UI/components/decisions_grid.py:65:        # Tags de cor por decisão
UI/components/decisions_grid.py:100:    def update_data(self, decisions: List[Dict]):
UI/components/decisions_grid.py:102:        self.current_data = decisions.copy()
UI/components/decisions_grid.py:107:        for i, decision in enumerate(decisions, 1):
UI/components/decisions_grid.py:108:            timestamp = self._format_timestamp(decision.get("timestamp"))
UI/components/decisions_grid.py:111:                decision.get("structure_id") or decision.get("aba") or "N/A"
UI/components/decisions_grid.py:113:            decision_text = decision.get("decision", "N/A")
UI/components/decisions_grid.py:114:            level = decision.get("level", "")
UI/components/decisions_grid.py:115:            ratio = self._format_ratio(decision.get("pl_pct_of_max"))
UI/components/decisions_grid.py:116:            dte = decision.get("dte_min", "")
UI/components/decisions_grid.py:117:            pl_atual = self._format_currency(decision.get("pl_atual"))
UI/components/decisions_grid.py:118:            pl_max = self._format_currency(decision.get("pl_max"))
UI/components/decisions_grid.py:121:                decision_text
UI/components/decisions_grid.py:122:                if decision_text in ["HOLD", "PREPARE_ROLL", "CLOSE_REOPEN", "ROLL", "ENTER"]
UI/components/decisions_grid.py:133:                    decision_text,
UI/components/decisions_grid.py:181:    def get_selected_decision(self) -> Optional[Dict]:
UI/components/decisions_grid.py:182:        """Retorna decisão atualmente selecionada."""
UI/components/details_panel.py:17:        self._current_decision = None
UI/components/details_panel.py:368:                ignored = {str(c).lower() for c in structure_cols}
UI/components/details_panel.py:369:                ignored.update(
UI/components/details_panel.py:378:                ts_cols = [c for c in cols if str(c).lower() not in ignored]
UI/components/details_panel.py:410:            "structure_decisions",
UI/components/details_panel.py:411:            "payoff_curve_points",
UI/components/details_panel.py:479:        ttk.Label(basic_frame, text="Decisão:").grid(
UI/components/details_panel.py:482:        self.decision_label = ttk.Label(
UI/components/details_panel.py:485:        self.decision_label.grid(row=1, column=1, sticky="ew", padx=(0, 10))
UI/components/details_panel.py:565:        ttk.Label(operational_frame, text="Cancelados ignorados:").grid(
UI/components/details_panel.py:568:        self.operational_cancelled_ignored_label = ttk.Label(
UI/components/details_panel.py:571:        self.operational_cancelled_ignored_label.grid(
UI/components/details_panel.py:641:    def update_decision(self, decision_data: Dict):
UI/components/details_panel.py:642:        self._current_decision = dict(decision_data) if decision_data else None
UI/components/details_panel.py:644:        self.timestamp_label.config(text=decision_data.get("timestamp", "N/A"))
UI/components/details_panel.py:647:        structure_id = decision_data.get("structure_id") or "N/A"
UI/components/details_panel.py:650:        self.decision_label.config(text=decision_data.get("decision", "N/A"))
UI/components/details_panel.py:651:        self.level_label.config(text=str(decision_data.get("level", "N/A")))
UI/components/details_panel.py:653:        self._format_currency_label(self.pl_atual_label, decision_data.get("pl_atual"))
UI/components/details_panel.py:654:        self._format_currency_label(self.pl_max_label, decision_data.get("pl_max"))
UI/components/details_panel.py:656:        ratio = decision_data.get("pl_pct_of_max")
UI/components/details_panel.py:661:        self.dte_label.config(text=str(decision_data.get("dte_min", "N/A")))
UI/components/details_panel.py:663:        spot_ref = decision_data.get("spot_reference") or decision_data.get("spot_ref")
UI/components/details_panel.py:672:        why_payload = decision_data.get("why") or decision_data.get("why_json")
UI/components/details_panel.py:720:        self._current_decision = None
UI/components/details_panel.py:722:            self.timestamp_label, self.structure_label, self.decision_label,
UI/components/details_panel.py:727:            self.operational_cancelled_ignored_label,
UI/components/details_panel.py:735:        """Chamado pelo MainWindow ao finalizar o subprocess do pipeline."""
UI/components/details_panel.py:758:            "operational_cancelled_ignored_label",
UI/components/details_panel.py:774:                "events_ignored_cancelled": int,
UI/components/details_panel.py:782:        - ignored_events.
UI/components/details_panel.py:796:        ignored = state.get("events_ignored_cancelled")
UI/components/details_panel.py:797:        if ignored is None and isinstance(effective_structure.get("ignored_events"), list):
UI/components/details_panel.py:798:            ignored = len(effective_structure.get("ignored_events") or [])
UI/components/details_panel.py:812:        self.operational_cancelled_ignored_label.config(
UI/components/details_panel.py:813:            text=str(ignored) if ignored is not None else "N/A"
UI/components/details_panel.py:878:    def _fetch_latest_decision_from_derived(
UI/components/details_panel.py:882:        alteracao_36: filtra por structure_id (INTEGER) em structure_decisions.
UI/components/details_panel.py:892:                "structure_id", "timestamp", "decision", "level",
UI/components/details_panel.py:900:                FROM structure_decisions
UI/components/details_panel.py:922:        alteracao_36: filtra por structure_id (INTEGER) em payoff_curve_points.
UI/components/details_panel.py:934:                FROM payoff_curve_points
UI/components/details_panel.py:962:                FROM structure_decisions
UI/components/details_panel.py:975:                "SELECT COUNT(*) AS n FROM payoff_curve_points WHERE structure_id = ?",
UI/components/details_panel.py:980:                "source_table": "derived.db:structure_decisions / payoff_curve_points",
UI/components/details_panel.py:1025:        decision = self._fetch_latest_decision_from_derived(structure_id)
UI/components/details_panel.py:1026:        if decision:
UI/components/details_panel.py:1027:            self.update_decision(decision)
UI/components/details_panel.py:1033:        if decision:
UI/components/details_panel.py:1034:            spot_ref = decision.get("spot_reference")
UI/components/details_panel.py:1047:        decision = self._current_decision
UI/components/details_panel.py:1048:        if not decision:
UI/components/details_panel.py:1050:                text="Nenhuma decisão selecionada", foreground="red"
UI/components/details_panel.py:1055:        structure_id = decision.get("structure_id")
UI/components/details_panel.py:1070:        # Botão manual: deve recalcular sempre que o usuário clicar.
UI/components/filters_panel.py:39:        # Linha 2: Estrutura e Decisão
UI/components/filters_panel.py:53:        ttk.Label(row2, text="Decisão:").pack(side="left")
UI/components/filters_panel.py:54:        self.decision_var = tk.StringVar()
UI/components/filters_panel.py:55:        self.decision_combo = ttk.Combobox(
UI/components/filters_panel.py:57:            textvariable=self.decision_var,
UI/components/filters_panel.py:62:        self.decision_combo.pack(side="left", padx=(5, 0))
UI/components/filters_panel.py:101:        self.decision_combo.bind("<<ComboboxSelected>>", lambda e: self._apply_filters())
UI/components/filters_panel.py:116:        if self.decision_var.get().strip():
UI/components/filters_panel.py:117:            filters["decision"] = self.decision_var.get().strip()
UI/components/filters_panel.py:139:        self.decision_var.set("")
UI/components/payoff_chart.py:66:        self._last_decision_data: Dict = {}
UI/components/payoff_chart.py:164:        self._last_decision_data = {}
UI/components/payoff_chart.py:171:        decision_data: Optional[Dict] = None,
UI/components/payoff_chart.py:179:        self._last_decision_data = dict(decision_data) if decision_data else {}
UI/components/payoff_chart.py:182:            payoff_points, decision_data, overlay_curve=self._fixed_curve
UI/components/payoff_chart.py:248:        """Redesenha com os dados salvos em _last_points/_last_decision_data."""
UI/components/payoff_chart.py:252:                self._last_decision_data or {},
UI/components/payoff_chart.py:259:        decision_data: Optional[Dict],
UI/components/payoff_chart.py:307:        if overlay_curve and decision_data:
UI/components/payoff_chart.py:309:                decision_data.get("structure_id")
UI/components/payoff_chart.py:310:                or decision_data.get("aba", "")
UI/components/payoff_chart.py:351:        if decision_data:
UI/components/payoff_chart.py:352:            raw = decision_data.get("spot_ref") or decision_data.get("spot_reference")
UI/components/payoff_chart.py:416:        if decision_data:
UI/components/payoff_chart.py:418:                decision_data.get("structure_id")
UI/components/payoff_chart.py:419:                or decision_data.get("aba", "")
UI/components/payoff_chart.py:421:            dec = decision_data.get("decision", "")
UI/components/structure_editor_dialog.py:95:        self._f_status     = tk.StringVar(value="active")
UI/components/structure_editor_dialog.py:125:            ("Status",         self._f_status,     "combo", ["active", "archived"]),
UI/components/structure_editor_dialog.py:276:        self._f_status.set(data.get("status", "active"))
UI/components/structure_editor_dialog.py:394:    def _leg_has_manual_required_fields(leg_data: dict) -> bool:
UI/components/structure_editor_dialog.py:395:        """Compatibilidade: permite leg manual completa mesmo sem cotacao RTD."""
UI/components/structure_editor_dialog.py:413:            usado no save/build payload; se a leg manual ja esta completa e a
UI/components/structure_editor_dialog.py:423:            if not require_quote and self._leg_has_manual_required_fields(leg_data):
UI/components/structures_list_panel.py:19:    _status_var     tk.StringVar  ("active" | "all")
UI/components/structures_list_panel.py:82:        self._status_var = tk.StringVar(value="active")
UI/components/structures_list_panel.py:86:            values=["active", "all"],
UI/components/structures_list_panel.py:134:        self._tree.tag_configure("active",   foreground="#1a1a1a")
UI/components/structures_list_panel.py:288:                "status":           "active",
UI/main_window.py:10:from UI.components.decisions_grid import DecisionsGrid
UI/main_window.py:43:        self._loading_animation_active = False
UI/main_window.py:49:        # Última decisão selecionada (preservada entre refreshes)
UI/main_window.py:50:        self.last_selected_decision: Optional[Dict] = None
UI/main_window.py:95:        self.decisions_grid = DecisionsGrid(
UI/main_window.py:97:            on_selection_change=self.on_decision_selected,
UI/main_window.py:99:        self.decisions_grid.pack(fill="both", expand=True, padx=5, pady=5)
UI/main_window.py:105:        # Aba 1: Detalhes da Decisão
UI/main_window.py:107:        right_notebook.add(details_frame, text="Detalhes da Decisão")
UI/main_window.py:176:            filtered_data = self.data_model.get_decisions(filters)
UI/main_window.py:177:            self.decisions_grid.update_data(filtered_data)
UI/main_window.py:184:    def on_decision_selected(self, decision_data: Dict):
UI/main_window.py:185:        """Callback quando uma decisão é selecionada no grid.
UI/main_window.py:188:        if not decision_data:
UI/main_window.py:191:        self.last_selected_decision = dict(decision_data)
UI/main_window.py:195:            self.details_panel.update_decision(decision_data)
UI/main_window.py:200:        structure_id = decision_data.get("structure_id")
UI/main_window.py:201:        timestamp = decision_data.get("timestamp")  # opcional
UI/main_window.py:204:            self._start_payoff_load(structure_id, timestamp, decision_data)
UI/main_window.py:213:        decision_data=None,   # alteracao_36: opcional
UI/main_window.py:218:        if decision_data is None:
UI/main_window.py:219:            decision_data = {"structure_id": structure_id}
UI/main_window.py:269:                    decision_data,
UI/main_window.py:304:            decisions = self.data_model.get_decisions()
UI/main_window.py:305:            self.decisions_grid.update_data(decisions)
UI/main_window.py:308:            d = self.last_selected_decision
UI/main_window.py:317:                        self.decisions_grid.select_by_key(target_sid, target_ts)
UI/main_window.py:322:                        self.details_panel.update_decision(d)
UI/main_window.py:343:                text=f"Dados atualizados - {len(decisions)} decisões"
UI/main_window.py:439:                current_data = self.decisions_grid.get_current_data()
UI/main_window.py:451:        - Ele recalcula somente a estrutura selecionada via CanonicalPricingFacade.
UI/main_window.py:512:                from services.canonical_pricing_facade import CanonicalPricingFacade
UI/main_window.py:514:                facade = CanonicalPricingFacade(db_path=self._db_path)
UI/main_window.py:597:            f"- Decisões: {self._format_pipeline_value(summary.get('decisions'))}",
UI/main_window.py:613:        decisions = self._format_pipeline_value(summary.get("decisions"))
UI/main_window.py:618:            f"Pipeline OK: decisões={decisions}; "
UI/main_window.py:645:            import subprocess
UI/main_window.py:648:            res = subprocess.run(
UI/main_window.py:668:        except subprocess.CalledProcessError as e:
UI/main_window.py:718:        decision_data: Dict,
UI/main_window.py:730:                overlays = self.payoff_chart.update_chart(points, decision_data)
UI/main_window.py:745:                used_ts = (info_dict or {}).get("used_timestamp") or decision_data.get(
UI/main_window.py:748:                src = (info_dict or {}).get("source_table", "payoff_curve_points")
UI/main_window.py:751:                if used_ts and used_ts != decision_data.get("timestamp"):
UI/main_window.py:779:        self._loading_animation_active = True
UI/main_window.py:783:            if not self._loading_animation_active:
UI/main_window.py:795:        self._loading_animation_active = False
UI/main_window.py:892:        Recalcula pricing/payoff/decisão após criação ou edição manual.
UI/main_window.py:916:                from services.canonical_pricing_facade import CanonicalPricingFacade
UI/main_window.py:918:                facade = CanonicalPricingFacade(db_path=self._db_path)
UI/models/ui_data.py:24:    "decision":      ["decision", "decisao", "action"],
UI/models/ui_data.py:132:        if self._payoff_table == "payoff_curve_points":
UI/models/ui_data.py:247:    def get_decisions(self, filters: Optional[Dict] = None) -> List[Dict]:
UI/models/ui_data.py:274:            "timestamp", "structure_id", "aba", "decision", "level",
UI/models/ui_data.py:336:            if filters.get("decision"):
UI/models/ui_data.py:337:                where.append("t.decision = ?")
UI/models/ui_data.py:338:                params.append(filters["decision"])
UI/models/ui_data.py:351:                t.timestamp, t.structure_id, t.aba, t.decision, t.level,
UI/models/ui_data.py:524:            if self._payoff_table == "payoff_curve_points":
UI/models/ui_data.py:527:                if "meta_json" in self._inspect_columns("payoff_curve_points"):
UI/models/ui_data.py:532:                    f"FROM payoff_curve_points "
UI/models/ui_data.py:541:                        f"SELECT timestamp FROM payoff_curve_points "
UI/models/ui_data.py:603:                "timestamp", "structure_id", "aba", "decision", "level",
UI/models/ui_data.py:645:            filter_info = f"{filter_col} (mode=canonical)"  # alteracao_34: sempre canonico
domain/calculation_request.py:28:VALID_SOURCES        = {"rtd", "manual", "ui"}
domain/calculation_request.py:178:    source             : 'rtd' | 'manual' | 'ui'
domain/calculation_request.py:217:    Contrato canônico de entrada para qualquer cálculo de payoff/decisão.
domain/calculation_request.py:220:    e o domínio (payoff, decision) recebe SOMENTE este objeto -- sem
domain/canonical_validators.py:4:def validate_canonical_input(canonical_input: dict[str, Any]) -> list[str]:
domain/canonical_validators.py:7:    structure = canonical_input.get("structure") or {}
domain/canonical_validators.py:8:    market = canonical_input.get("market") or {}
domain/contracts.py:6:class CanonicalLeg:
domain/contracts.py:18:class CanonicalStructure:
domain/contracts.py:22:    legs: list[CanonicalLeg] = field(default_factory=list)
domain/contracts.py:26:class CanonicalMarket:
domain/contracts.py:35:class CanonicalMeta:
domain/contracts.py:43:class CanonicalStructureMarketInput:
domain/contracts.py:44:    structure: CanonicalStructure
domain/contracts.py:45:    market: CanonicalMarket
domain/contracts.py:46:    meta: CanonicalMeta | None = None
domain/contracts.py:49:    def from_dict(cls, payload: dict[str, Any]) -> "CanonicalStructureMarketInput":
domain/contracts.py:55:            CanonicalLeg(
domain/contracts.py:68:        structure = CanonicalStructure(
domain/contracts.py:75:        market = CanonicalMarket(
domain/contracts.py:83:        meta = CanonicalMeta(
domain/decision.py:3:Domain: Decision logic (30/60/80 thresholds + DTE gate) from real data.
domain/decision.py:6:Funcoes canonicas: compute_decision_from_inputs, compute_decision_from_payoff,
domain/decision.py:7:compute_decision_from_contract.
domain/decision.py:15:from domain.contracts import CanonicalStructureMarketInput
domain/decision.py:19:# Constantes de decisão
domain/decision.py:55:# Mapeamento decision  level
domain/decision.py:56:_DECISION_LEVEL = {
domain/decision.py:58:    "WATCH":        1,   # nível interno, mapeado para decision="HOLD" level=1
domain/decision.py:68:def compute_decision_from_inputs(
domain/decision.py:114:    decision = "HOLD" if _internal == "WATCH" else _internal
domain/decision.py:129:        "decision":      decision,
domain/decision.py:139:def compute_decision_from_payoff(
domain/decision.py:153:            "decision":      "HOLD",
domain/decision.py:174:            "decision":      "HOLD",
domain/decision.py:183:    return compute_decision_from_inputs(
domain/decision.py:193:def compute_decision_from_contract(
domain/decision.py:194:    contract: CanonicalStructureMarketInput,
domain/decision.py:197:    """Entrada canônica via CanonicalStructureMarketInput."""
domain/decision.py:202:        return compute_decision_from_payoff(payoff=payoff, dte_min=dte_min)
domain/decision.py:209:    return compute_decision_from_inputs(
domain/market_snapshot.py:20:    MANUAL = "manual"
domain/market_snapshot.py:60:    Atributos do cabeçalho (todos opcionais -- podem vir de RTD ou manual):
domain/payoff.py:3:from domain.canonical_validators import validate_canonical_input
domain/payoff.py:51:def compute_payoff_curve_from_canonical_legs(
domain/payoff.py:66:                "input_type": "canonical_legs",
domain/payoff.py:113:            "input_type": "canonical_legs",
domain/payoff.py:123:def compute_payoff_from_canonical_input(
domain/payoff.py:124:    canonical_input: dict[str, Any],
domain/payoff.py:129:    structure = canonical_input.get("structure") or {}
domain/payoff.py:130:    market = canonical_input.get("market") or {}
domain/payoff.py:131:    input_meta = canonical_input.get("meta") or {}
domain/payoff.py:133:    errors = validate_canonical_input(canonical_input)
domain/payoff.py:141:                "input_type": "canonical_legs",
domain/payoff.py:157:    result = compute_payoff_curve_from_canonical_legs(
domain/position_side.py:17:CANONICAL_POSITION_SIDES: frozenset[str] = frozenset({
domain/position_side.py:45:    canonical = _POSITION_SIDE_ALIASES.get(text)
domain/position_side.py:46:    if canonical is None:
domain/position_side.py:51:    return canonical
domain/position_side.py:56:    canonical = normalize_position_side(value)
domain/position_side.py:60:    }[canonical]
domain/structure_metrics.py:83:def compute_dte_min_from_canonical_input(canonical_input: dict[str, Any]) -> int | None:
domain/structure_metrics.py:84:    structure = canonical_input.get("structure") or {}
domain/structure_metrics.py:85:    market = canonical_input.get("market") or {}
domain/structure_metrics.py:343:def compute_structure_metrics_from_canonical_input(
domain/structure_metrics.py:344:    canonical_input: dict[str, Any],
domain/structure_metrics.py:346:    structure = canonical_input.get("structure") or {}
domain/structure_metrics.py:347:    market = canonical_input.get("market") or {}
repositories/market_snapshot_repository.py:6:(rtd_option_quotes) e manuais (manual_analise_robo_legs), normaliza os campos
repositories/market_snapshot_repository.py:59:_SQL_MANUAL_LEGS = """
repositories/market_snapshot_repository.py:83:    FROM manual_analise_robo_legs
repositories/market_snapshot_repository.py:256:      get_manual_legs(aba)             -> lista de LegMarketSnapshot source=MANUAL
repositories/market_snapshot_repository.py:357:    # -- Manual ---------------------------------------------------------------
repositories/market_snapshot_repository.py:359:    def get_manual_legs(self, ref: StructureRef | str) -> list[LegMarketSnapshot]:
repositories/market_snapshot_repository.py:362:            rows = conn.execute(_SQL_MANUAL_LEGS, (aba,)).fetchall()
repositories/market_snapshot_repository.py:363:        return [_row_to_leg(r, SnapshotSource.MANUAL) for r in rows]
repositories/market_snapshot_repository.py:378:            legs = self.get_manual_legs(ref)
repositories/robo_legs_repository.py:36:      manual_analise_robo_legs > rtd_analise_robo_legs
repositories/robo_legs_repository.py:56:        - Primeiro tenta MANUAL
repositories/robo_legs_repository.py:63:        manual = self._query_legs(
repositories/robo_legs_repository.py:64:            table="manual_analise_robo_legs",
repositories/robo_legs_repository.py:67:            fonte=FonteType.MANUAL,
repositories/robo_legs_repository.py:69:        if manual:
repositories/robo_legs_repository.py:70:            return manual
repositories/robo_legs_repository.py:80:    def has_manual(self, ref: StructureRef, timestamp: Any) -> bool:
repositories/robo_legs_repository.py:88:            FROM manual_analise_robo_legs
repositories/robo_legs_repository.py:101:        prefer: str = "manual_then_rtd",
repositories/robo_legs_repository.py:110:                    SELECT timestamp FROM manual_analise_robo_legs WHERE aba = ?
repositories/robo_legs_repository.py:120:                "SELECT DISTINCT timestamp FROM manual_analise_robo_legs "
repositories/robo_legs_repository.py:181:        canonical_side = normalize_position_side(cv_raw)
repositories/robo_legs_repository.py:182:        cv_norm       = "C" if canonical_side == "COMPRADO" else "V"
repositories/robo_legs_repository.py:254:    def has_manual_by_structure_id(
repositories/robo_legs_repository.py:259:        """Versão canônica de has_manual() por structure_id."""
repositories/robo_legs_repository.py:263:        return self.has_manual(
repositories/robo_legs_repository.py:271:        prefer: str = "manual_then_rtd",
repositories/robo_legs_status_repository.py:47:        Retorna (manual_latest_ts, rtd_latest_ts) para a aba.
repositories/robo_legs_status_repository.py:53:                "SELECT MAX(timestamp) AS ts FROM manual_analise_robo_legs WHERE aba = ?",
repositories/robo_legs_status_repository.py:76:        Retorna (manual_latest_ts, rtd_latest_ts).
repositories/structure_events_repository.py:11:- encerramento manual
repositories/structure_events_repository.py:35:        "manual_close",
repositories/structure_events_repository.py:59:        "manual",
repositories/structure_events_repository.py:144:    source = str(data.get("source", "manual")).strip().lower()
repositories/structure_events_repository.py:209:                source         TEXT    NOT NULL DEFAULT 'manual',
repositories/structures_repository.py:23:from domain.position_side import CANONICAL_POSITION_SIDES, normalize_position_side
repositories/structures_repository.py:26:VALID_POSITION_SIDES: frozenset[str] = CANONICAL_POSITION_SIDES
repositories/structures_repository.py:28:VALID_STRUCTURE_STATUS: frozenset[str] = frozenset({"active", "archived"})
repositories/structures_repository.py:64:    status = str(data.get("status", "active")).strip().lower()
repositories/structures_repository.py:460:            params = ("active",)
repositories/structures_repository.py:716:                WHERE alias_legacy_aba = ? AND status = 'active'
repositories/system_snapshots_repository.py:17:    "decision_json",
repositories/system_snapshots_repository.py:91:        decision_json: dict[str, Any] | list[Any] | None = None,
repositories/system_snapshots_repository.py:124:                    decision_json,
repositories/system_snapshots_repository.py:141:                    _to_json(decision_json),
repositories/ui_data_table_candidates.py:12:    "structure_decisions",
repositories/ui_data_table_candidates.py:15:    "decisions",
repositories/ui_data_table_candidates.py:16:    "rtd_decisions",
repositories/ui_data_table_candidates.py:20:    "payoff_curve_points",
services/calculation_orchestrator.py:3:# alteracao_46: _request_to_payoff_dict, run_payoff, run_decision
services/calculation_orchestrator.py:4:# alteracao_47: run_full_pipeline, multiplier fix (1.0), run_decision auto-extract
services/calculation_orchestrator.py:20:from domain.payoff import compute_payoff_from_canonical_input
services/calculation_orchestrator.py:21:from domain.decision import compute_decision_from_contract
services/calculation_orchestrator.py:157:    canonical = _request_to_payoff_dict(request, extra_meta=extra_meta)
services/calculation_orchestrator.py:158:    return compute_payoff_from_canonical_input(
services/calculation_orchestrator.py:159:        canonical,
services/calculation_orchestrator.py:166:def run_decision(
services/calculation_orchestrator.py:195:    return compute_decision_from_contract(contract, payoff=payoff)
services/calculation_orchestrator.py:205:    """alteracao_47: pipeline completo payoff + decision."""
services/calculation_orchestrator.py:213:    decision_result = run_decision(request, payoff=payoff_result)
services/calculation_orchestrator.py:217:        "decision":         decision_result,
services/calculation_orchestrator.py:233:    - Executar payoff e decisao sem acessar raw DB diretamente
services/calculation_orchestrator.py:248:    # Construcao manual do CalculationRequest
services/calculation_orchestrator.py:338:    # run_payoff / run_decision / run_full_pipeline
services/calculation_orchestrator.py:348:        canonical = self._request_to_payoff_dict(request)
services/calculation_orchestrator.py:349:        return compute_payoff_from_canonical_input(
services/calculation_orchestrator.py:350:            canonical,
services/calculation_orchestrator.py:356:    def run_decision(
services/calculation_orchestrator.py:384:        return compute_decision_from_contract(contract, payoff=payoff_result)
services/calculation_orchestrator.py:393:        """Executa run_payoff -> run_decision em sequencia."""
services/calculation_orchestrator.py:395:        decision_result = self.run_decision(request, payoff_result=payoff_result)
services/calculation_orchestrator.py:399:            "decision":         decision_result,
services/calculation_orchestrator.py:506:        Retorna dict com chaves: structure_id, payoff, decision.
services/calculation_orchestrator.py:517:            "decision":     pipeline_result["decision"],
services/canonical_input_service.py:2:from domain.structure_metrics import compute_structure_metrics_from_canonical_input
services/canonical_input_service.py:4:# services/canonical_input_service.py
services/canonical_input_service.py:8:  - _resolve_legs            → MarketSnapshotSelector (manual > rtd por ativo)
services/canonical_input_service.py:36:class CanonicalInputService:
services/canonical_input_service.py:44:        prefer_canonical_legs: bool = True,
services/canonical_input_service.py:52:        self.prefer_canonical_legs       = prefer_canonical_legs
services/canonical_input_service.py:151:        legs pelo resultado do selector (manual > rtd).
services/canonical_input_service.py:188:    # Legs via selector (manual > rtd)
services/canonical_input_service.py:244:            "manual_overrides": result.manual_overrides,
services/canonical_input_service.py:245:            "is_manual_first":  result.is_manual_first,
services/canonical_input_service.py:298:        if self.prefer_canonical_legs and existing_legs:
services/canonical_input_service.py:302:                legs_source="canonical",
services/canonical_input_service.py:334:                legs_source="canonical",
services/canonical_input_service.py:335:                fallback_reason="canonical_legs_retained_after_empty_fallback",
services/canonical_input_service.py:371:            "structure_events_ignored_cancelled": operational_state.get(
services/canonical_input_service.py:372:                "events_ignored_cancelled",
services/canonical_input_service.py:393:        structure_metrics = compute_structure_metrics_from_canonical_input(assembled)
services/canonical_pricing_facade.py:1:# services/canonical_pricing_facade.py
services/canonical_pricing_facade.py:257:        canonical_leg = {
services/canonical_pricing_facade.py:281:        legs_data.append(canonical_leg)
services/canonical_pricing_facade.py:315:            "manual_overrides": getattr(selection_result, "manual_overrides", None) or [],
services/canonical_pricing_facade.py:321:class CanonicalPricingFacade:
services/canonical_pricing_facade.py:364:            # Caminho B - manual canônico:
services/canonical_pricing_facade.py:367:            # O caminho B corrige estruturas cadastradas manualmente pela UI.
services/canonical_pricing_facade.py:420:                meta.setdefault("snapshot_source", "canonical_manual_without_alias")
services/canonical_pricing_facade.py:444:                "canonical_input": pricing_payload,
services/canonical_pricing_facade.py:468:                "canonical_input": None,
services/derived_payoff_persistence.py:6:from domain.payoff import compute_payoff_from_canonical_input
services/derived_payoff_persistence.py:7:from services.derived_service import save_payoff_from_canonical_payload, save_decision_from_canonical_payload
services/derived_payoff_persistence.py:17:      1. Montar o canonical_input a partir do pricing_payload
services/derived_payoff_persistence.py:20:      4. Persistir decisão básica derivada do resultado do engine
services/derived_payoff_persistence.py:33:            logger.debug("derived_payoff_persistence: pricing_payload vazio, skip.")
services/derived_payoff_persistence.py:40:                "derived_payoff_persistence: status=%r não elegível para payoff, skip.",
services/derived_payoff_persistence.py:45:        # Timestamp único para payoff + decisão.
services/derived_payoff_persistence.py:52:                "derived_payoff_persistence: decisão não gravada porque payoff não foi salvo -- structure_id=%s",
services/derived_payoff_persistence.py:57:        decision_saved = self._persist_decision(pricing_payload, result, snapshot_ts)
services/derived_payoff_persistence.py:58:        if not decision_saved:
services/derived_payoff_persistence.py:60:                "derived_payoff_persistence: payoff salvo, mas decisão falhou -- structure_id=%s timestamp=%s",
services/derived_payoff_persistence.py:76:            canonical_input = self._build_canonical_input(pricing_payload, result)
services/derived_payoff_persistence.py:77:            payoff_result = compute_payoff_from_canonical_input(canonical_input)
services/derived_payoff_persistence.py:86:            save_payoff_from_canonical_payload(payoff_result, timestamp=snapshot_ts)
services/derived_payoff_persistence.py:102:    #  decisão                                                         #
services/derived_payoff_persistence.py:105:    def _persist_decision(
services/derived_payoff_persistence.py:136:            decision_dict = {
services/derived_payoff_persistence.py:137:                "decision":      "HOLD",
services/derived_payoff_persistence.py:158:            save_decision_from_canonical_payload(
services/derived_payoff_persistence.py:159:                decision=decision_dict,
services/derived_payoff_persistence.py:166:                "derived_payoff_persistence: decisão gravada -- structure_id=%s",
services/derived_payoff_persistence.py:173:                "derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s",
services/derived_payoff_persistence.py:189:        Payloads vindos da UI/manual podem vir com leg["side"].
services/derived_payoff_persistence.py:224:        esperado por domain.compute_payoff_from_canonical_input().
services/derived_payoff_persistence.py:274:    def _normalize_canonical_input_for_payoff(
services/derived_payoff_persistence.py:275:        canonical_input: dict[str, Any],
services/derived_payoff_persistence.py:278:        Retorna uma cópia rasa do canonical_input com legs normalizadas para payoff.
services/derived_payoff_persistence.py:280:        normalized = dict(canonical_input)
services/derived_payoff_persistence.py:302:    def _build_canonical_input(
services/derived_payoff_persistence.py:307:        Monta o canonical_input esperado por compute_payoff_from_canonical_input().
services/derived_payoff_persistence.py:316:            return DerivedPayoffPersistence._normalize_canonical_input_for_payoff(
services/derived_payoff_persistence.py:333:        canonical_input = {
services/derived_payoff_persistence.py:351:        return canonical_input
services/derived_service.py:17:    cleanup_old_decisions,
services/derived_service.py:21:    insert_structure_decision,
services/derived_service.py:210:def save_payoff_from_canonical_payload(
services/derived_service.py:273:def save_decision(
services/derived_service.py:275:    decision: Dict[str, Any],
services/derived_service.py:292:        explicit_sid = decision.get("structure_id")
services/derived_service.py:294:        explicit_sid = (decision.get("meta") or {}).get("structure_id")
services/derived_service.py:302:    enriched_decision = {
services/derived_service.py:303:        **decision,
services/derived_service.py:306:            **(decision.get("meta") or {}),
services/derived_service.py:314:        return insert_structure_decision(
services/derived_service.py:318:            decision_dict=enriched_decision,
services/derived_service.py:322:def save_decision_from_canonical_payload(
services/derived_service.py:323:    decision: Dict[str, Any],
services/derived_service.py:345:    enriched_decision = {
services/derived_service.py:346:        **decision,
services/derived_service.py:349:            **(decision.get("meta") or {}),
services/derived_service.py:357:    return save_decision(
services/derived_service.py:359:        decision=enriched_decision,
services/derived_service.py:372:        deleted_dec    = cleanup_old_decisions(conn, days_to_keep=days_to_keep)
services/derived_service.py:373:        return {"payoff_deleted": deleted_payoff, "decisions_deleted": deleted_dec}
services/derived_service.py:385:            FROM payoff_curve_points
services/derived_service.py:405:    Importante: payoff_curve_points mantém histórico por timestamp.
services/derived_service.py:416:              FROM payoff_curve_points
services/derived_service.py:420:                      FROM payoff_curve_points
services/derived_service.py:439:def get_recent_decisions():
services/derived_service.py:447:                "PRAGMA table_info(structure_decisions)"
services/derived_service.py:452:            "timestamp", "aba", "decision", "level",
services/derived_service.py:465:            FROM structure_decisions
services/derived_service.py:470:        decisions = []
services/derived_service.py:505:            decisions.append(item)
services/derived_service.py:507:        return decisions
services/derived_service.py:540:    get_payoff_by_aba() ausente por decisao de design (alteracao_65): interface simplificada.
services/derived_service.py:553:    def save_decision(self, *args, **kwargs):
services/derived_service.py:554:        return save_decision(*args, **kwargs)
services/legacy_robo_legs_fallback.py:69:        canonical_legs = []
services/legacy_robo_legs_fallback.py:71:            adapted = self._adapt_legacy_leg_to_canonical(leg)
services/legacy_robo_legs_fallback.py:73:                canonical_legs.append(adapted)
services/legacy_robo_legs_fallback.py:75:        if not canonical_legs:
services/legacy_robo_legs_fallback.py:84:        return canonical_legs, {
services/legacy_robo_legs_fallback.py:201:    def _adapt_legacy_leg_to_canonical(
services/legacy_structure_legs_reader.py:6:from services.robo_leg_mapper import to_canonical_leg
services/legacy_structure_legs_reader.py:16:      - ler pernas legadas manual/rtd;
services/legacy_structure_legs_reader.py:39:        canonical_legs: list[dict[str, Any]] = []
services/legacy_structure_legs_reader.py:42:            canonical_leg = to_canonical_leg(
services/legacy_structure_legs_reader.py:46:            canonical_leg["leg_order"] = index
services/legacy_structure_legs_reader.py:47:            canonical_legs.append(canonical_leg)
services/legacy_structure_legs_reader.py:49:        return canonical_legs
services/market_snapshot_selector.py:3:Política de precedência de snapshots: manual > rtd_option_quotes > rtd.
services/market_snapshot_selector.py:6:  - Se existir snapshot manual para o ativo, usa manual
services/market_snapshot_selector.py:38:    manual_overrides: list[str] = field(default_factory=list)
services/market_snapshot_selector.py:41:    def is_manual_first(self) -> bool:
services/market_snapshot_selector.py:42:        return self.source == SnapshotSource.MANUAL or bool(self.manual_overrides)
services/market_snapshot_selector.py:47:    Aplica a política manual > rtd_option_quotes > rtd para selecionar o snapshot canônico.
services/market_snapshot_selector.py:74:        manual_legs = self._repo.get_manual_legs(effective_ref)
services/market_snapshot_selector.py:90:        manual_by_ativo: dict[str, LegMarketSnapshot] = {}
services/market_snapshot_selector.py:91:        for leg in manual_legs:
services/market_snapshot_selector.py:92:            if leg.ativo and leg.ativo not in manual_by_ativo:
services/market_snapshot_selector.py:93:                manual_by_ativo[leg.ativo] = leg
services/market_snapshot_selector.py:106:            set(manual_by_ativo)
services/market_snapshot_selector.py:115:            if ativo in manual_by_ativo:
services/market_snapshot_selector.py:116:                legs_selected.append(manual_by_ativo[ativo])
services/market_snapshot_selector.py:124:        if manual_legs:
services/market_snapshot_selector.py:125:            source: SnapshotSource | str = SnapshotSource.MANUAL
services/market_snapshot_selector.py:135:            manual_overrides=overrides,
services/payoff_persistence_port.py:7:    Contrato de persistência derivada (payoff + decisão).
services/payoff_pricing_engine.py:3:from domain.payoff import compute_payoff_curve_from_canonical_legs
services/payoff_pricing_engine.py:40:        payoff = compute_payoff_curve_from_canonical_legs(
services/pricing_execution_app_service.py:3:alteracao_18 -- execute_pricing() delegado para CanonicalPricingFacade.
services/pricing_execution_app_service.py:6:  - execute_pricing() agora usa CanonicalPricingFacade (manual > rtd, caminho canônico)
services/pricing_execution_app_service.py:16:from services.canonical_pricing_facade import CanonicalPricingFacade
services/pricing_execution_app_service.py:25:        canonical_pricing_facade: CanonicalPricingFacade | None = None,
services/pricing_execution_app_service.py:29:        self._facade = canonical_pricing_facade or CanonicalPricingFacade(
services/pricing_execution_persistence_service.py:67:        #  alteracao_21 -- persistência derivada (payoff + decisão)           #
services/pricing_execution_persistence_service.py:125:                decision_json=self._extract_result_field(inner, "decision"),
services/pricing_input_service.py:3:from services.canonical_input_service import CanonicalInputService
services/pricing_input_service.py:10:        canonical_input_service: CanonicalInputService | None = None,
services/pricing_input_service.py:12:        self.canonical_input_service = canonical_input_service or CanonicalInputService()
services/pricing_input_service.py:19:        canonical_input = self.canonical_input_service.build_structure_market_input(
services/pricing_input_service.py:24:        return self.build_pricing_payload_from_canonical_input(canonical_input)
services/pricing_input_service.py:26:    def build_pricing_payload_from_canonical_input(
services/pricing_input_service.py:28:        canonical_input: dict[str, Any],
services/pricing_input_service.py:30:        return to_pricing_payload(canonical_input)
services/pricing_payload_adapter.py:18:def to_pricing_payload(canonical_input: dict[str, Any]) -> dict[str, Any]:
services/pricing_payload_adapter.py:19:    if not canonical_input:
services/pricing_payload_adapter.py:20:        raise ValueError("canonical_input is required")
services/pricing_payload_adapter.py:22:    structure = canonical_input.get("structure")
services/pricing_payload_adapter.py:23:    market = canonical_input.get("market")
services/pricing_payload_adapter.py:26:        raise ValueError("canonical_input.structure is required")
services/pricing_payload_adapter.py:29:        raise ValueError("canonical_input.market is required")
services/pricing_payload_adapter.py:36:            raise ValueError(f"canonical_input.structure.legs[{index}] is required")
services/robo_leg_mapper.py:43:def to_canonical_leg(leg: Any, multiplier: float = 1.0) -> dict[str, Any]:
services/robo_legs_service.py:23:      - obtém legs com regra manual > rtd
services/robo_legs_status_service.py:65:            manual_latest, rtd_latest = self.status_repo.latest_timestamps(ref=ref)
services/robo_legs_status_service.py:69:            manual_latest, rtd_latest = self.status_repo.latest_timestamps(aba)
services/robo_legs_status_service.py:71:        if manual_latest is not None:
services/robo_legs_status_service.py:72:            chosen_fonte = FonteType.MANUAL
services/robo_legs_status_service.py:73:            chosen_ts = manual_latest
services/robo_legs_status_service.py:84:                manual_latest_ts=None,
services/robo_legs_status_service.py:105:            manual_latest_ts=manual_latest,
services/structure_analysis_service.py:6:from domain.decision import compute_decision_from_payoff
services/structure_analysis_service.py:7:from domain.payoff import compute_payoff_from_canonical_input
services/structure_analysis_service.py:9:    compute_dte_min_from_canonical_input,
services/structure_analysis_service.py:10:    compute_structure_metrics_from_canonical_input,
services/structure_analysis_service.py:15:    def __init__(self, canonical_input_service):
services/structure_analysis_service.py:16:        self._canonical_input_service = canonical_input_service
services/structure_analysis_service.py:29:        canonical_input = self._canonical_input_service.build_structure_market_input(
services/structure_analysis_service.py:35:        structure_metrics = compute_structure_metrics_from_canonical_input(canonical_input)
services/structure_analysis_service.py:39:        # Mantemos compute_dte_min_from_canonical_input como fonte explícita do
services/structure_analysis_service.py:43:        dte_min_inferred = compute_dte_min_from_canonical_input(canonical_input)
services/structure_analysis_service.py:62:        payoff = compute_payoff_from_canonical_input(canonical_input)
services/structure_analysis_service.py:72:            decision = {
services/structure_analysis_service.py:73:                "decision":      "HOLD",
services/structure_analysis_service.py:83:                "canonical_input": canonical_input,
services/structure_analysis_service.py:92:                "decision": decision,
services/structure_analysis_service.py:95:        # 8. Computa decisão -- passa TODOS os parâmetros como keyword
services/structure_analysis_service.py:96:        decision = compute_decision_from_payoff(
services/structure_analysis_service.py:105:        decision["dte_min"] = dte_min_effective
services/structure_analysis_service.py:108:        decision["why"]["dte_gate"] = dte_gate
services/structure_analysis_service.py:111:            "canonical_input": canonical_input,
services/structure_analysis_service.py:120:            "decision": decision,
services/structure_events_service.py:16:        "manual_close",
services/structure_events_service.py:30:        "manual",
services/structure_events_service.py:118:        source: str = "manual",
services/structure_events_service.py:162:    def register_manual_close(
services/structure_events_service.py:177:            event_type="manual_close",
services/structure_events_service.py:182:            source="manual",
services/structure_events_service.py:193:        source: str = "manual",
services/structure_events_service.py:299:        - Eventos cancelados são ignorados.
services/structure_events_service.py:303:        - manual_close reduz se quantity foi informado; senão zera.
services/structure_events_service.py:338:        ignored_cancelled_count = 0
services/structure_events_service.py:344:                ignored_cancelled_count += 1
services/structure_events_service.py:369:            if event_type == "manual_close":
services/structure_events_service.py:389:            "events_ignored_cancelled": ignored_cancelled_count,

## Possiveis schemas/migrations
./ATT/tests/__pycache__/test_system_snapshots_schema.cpython-313-pytest-9.0.3.pyc
./ATT/tests/__pycache__/test_ui_data_migration.cpython-313-pytest-9.0.3.pyc
./ATT/tests/test_system_snapshots_schema.py
./ATT/tests/test_ui_data_migration.py
./_resgate_db/estado_schema_atual/app_schema_atual_vazio.db
./_resgate_db/estado_schema_atual/derived_schema_atual_vazio.db
./backups/app_fase12_rtd_option_quotes_ok.sql
./db/init_db.py
./db/init_excel_schema.py
./db/schema.py
./db/schema_excel.py
./docs/checkpoints/evidencias/fase-3b-diagnostico-schema-canonico-estruturas.txt
./infra/__pycache__/bootstrap_structures_schema.cpython-313.pyc
./infra/bootstrap_rtd_option_quotes_schema.py
./infra/bootstrap_structures_schema.py
./scripts/fase-3b-diagnostico-schema-canonico-estruturas.sh
./scripts/repair_derived_db_consistency.py
./scripts/validate_derived_db.py
./validate_db.py

## Arquivos provaveis completos com numeracao

## FILE: UI/components/structure_editor_dialog.py
```python
     1	# UI/components/structure_editor_dialog.py
     2	"""
     3	StructureEditorDialog -- alteracao_10 / Fase 5
     4	Dialog modal para criar / editar uma estrutura com suas legs.
     5	
     6	Contrato com main_window.py:
     7	    dlg = StructureEditorDialog(
     8	        parent,
     9	        structure_id: int | None,   # None -> nova estrutura
    10	        db_path: str,
    11	    )
    12	    root.wait_window(dlg)
    13	    if dlg.saved: ...               # True se o usuario clicou Salvar com sucesso
    14	
    15	Atributos publicos esperados pelos testes de integracao:
    16	    saved           bool
    17	    _f_name         tk.StringVar
    18	    _f_underlying   tk.StringVar
    19	    _f_alias        tk.StringVar
    20	    _f_status       tk.StringVar
    21	    _f_notes        tk.StringVar
    22	    _legs_rows      list[dict]
    23	    _structure_id   int | None
    24	    _repo           StructuresRepository
    25	    _cmd_save()     metodo que executa a logica de salvar
    26	    _load_existing()       sem argumento -- usa self._structure_id
    27	    _build_legs_payload()  logica pura, testavel sem display
    28	    _build_ui()     constroi todos os widgets
    29	    _add_leg_row()  alias publico de _cmd_add_leg (exigido por checks estaticos)
    30	"""
    31	from __future__ import annotations
    32	
    33	import tkinter as tk
    34	from tkinter import ttk, messagebox
    35	from typing import Optional
    36	
    37	from repositories.structures_repository import StructuresRepository
    38	from repositories.rtd_option_quotes_repository import RtdOptionQuotesRepository
    39	from services.structure_leg_rtd_enrichment_service import StructureLegRtdEnrichmentService
    40	from domain.position_side import normalize_position_side
    41	
    42	
    43	def _parse_decimal(value, field_name: str) -> float:
    44	    if value is None:
    45	        raise ValueError(f"{field_name} is required")
    46	
    47	    if isinstance(value, str):
    48	        value = value.strip()
    49	        if not value:
    50	            raise ValueError(f"{field_name} is required")
    51	
    52	        if "," in value:
    53	            value = value.replace(".", "").replace(",", ".")
    54	
    55	    try:
    56	        return float(value)
    57	    except Exception as exc:
    58	        raise ValueError(f"{field_name} must be numeric") from exc
    59	
    60	
    61	class StructureEditorDialog(tk.Toplevel):
    62	    """Dialog modal de criacao / edicao de estrutura."""
    63	
    64	    def __init__(
    65	        self,
    66	        parent: tk.Widget,
    67	        structure_id: Optional[int] = None,
    68	        db_path: str = "dados/app.db",
    69	        *,
    70	        _repo=None,                          # <-- injecao de dependencia (testes)
    71	        _leg_enrichment_service=None,        # <-- injecao opcional para testes
    72	    ):
    73	        super().__init__(parent)
    74	
    75	        self._structure_id = structure_id
    76	        self._db_path      = db_path
    77	        self.saved         = False
    78	        self.saved_structure_id = None
    79	        self._legs_rows: list[dict] = []
    80	
    81	        # Injeta repositorio mockado em testes, ou cria o real em producao
    82	        if _repo is not None:
    83	            self._repo = _repo
    84	        else:
    85	            self._repo = StructuresRepository(db_path)
    86	
    87	        self._leg_enrichment_service = _leg_enrichment_service
    88	
    89	        # Variaveis de formulario -- inicializadas ANTES de _build_ui
    90	        # para que _load_existing() possa fazer .set() mesmo se chamado
    91	        # antes do mainloop (cenario de teste headless via object.__new__)
    92	        self._f_name       = tk.StringVar()
    93	        self._f_underlying = tk.StringVar()
    94	        self._f_alias      = tk.StringVar()
    95	        self._f_status     = tk.StringVar(value="active")
    96	        self._f_notes      = tk.StringVar()
    97	
    98	        self._build_ui()
    99	
   100	        if structure_id is not None:
   101	            self._load_existing()
   102	
   103	        # Comportamento modal
   104	        self.transient(parent)
   105	        self.grab_set()
   106	        self.resizable(True, True)
   107	        self.minsize(640, 480)
   108	
   109	    # ------------------------------------------------------------------
   110	    # Construcao da UI
   111	    # ------------------------------------------------------------------
   112	
   113	    def _build_ui(self):
   114	        title = "Nova Estrutura" if self._structure_id is None else "Editar Estrutura"
   115	        self.title(title)
   116	
   117	        # === Cabecalho ===
   118	        hdr = ttk.LabelFrame(self, text="Dados Gerais", padding=8)
   119	        hdr.pack(fill="x", padx=8, pady=(8, 4))
   120	
   121	        fields = [
   122	            ("Nome *",         self._f_name,       "entry", None),
   123	            ("Ativo *",        self._f_underlying, "entry", None),
   124	            ("Aba / Alias",    self._f_alias,      "entry", None),
   125	            ("Status",         self._f_status,     "combo", ["active", "archived"]),
   126	            ("Observacoes",    self._f_notes,      "entry", None),
   127	        ]
   128	
   129	        for row_idx, (label, var, widget_type, opts) in enumerate(fields):
   130	            ttk.Label(hdr, text=label, anchor="e", width=14).grid(
   131	                row=row_idx, column=0, sticky="e", padx=(0, 6), pady=2
   132	            )
   133	            if widget_type == "combo":
   134	                w = ttk.Combobox(
   135	                    hdr, textvariable=var, values=opts,
   136	                    state="readonly", width=14,
   137	                )
   138	            else:
   139	                w = ttk.Entry(hdr, textvariable=var, width=40)
   140	            w.grid(row=row_idx, column=1, sticky="ew", pady=2)
   141	
   142	        hdr.columnconfigure(1, weight=1)
   143	
   144	        # === Legs ===
   145	        legs_outer = ttk.LabelFrame(self, text="Legs", padding=8)
   146	        legs_outer.pack(fill="both", expand=True, padx=8, pady=4)
   147	
   148	        # Toolbar de legs
   149	        leg_toolbar = ttk.Frame(legs_outer)
   150	        leg_toolbar.pack(fill="x", pady=(0, 4))
   151	        ttk.Button(leg_toolbar, text="+ Leg",    command=self._cmd_add_leg).pack(side="left", padx=2)
   152	        ttk.Button(leg_toolbar, text="Remover",  command=self._cmd_remove_leg).pack(side="left", padx=2)
   153	        ttk.Button(leg_toolbar, text="▲",        command=lambda: self._cmd_move_leg(-1)).pack(side="left", padx=1)
   154	        ttk.Button(leg_toolbar, text="▼",        command=lambda: self._cmd_move_leg(+1)).pack(side="left", padx=1)
   155	
   156	        # Treeview de legs
   157	        leg_frame = ttk.Frame(legs_outer)
   158	        leg_frame.pack(fill="both", expand=True)
   159	
   160	        leg_cols   = ("order", "side", "type", "strike", "expiry", "qty", "premium", "mult", "symbol")
   161	        leg_hdrs   = ["#", "Lado", "Tipo", "Strike", "Vencimento", "Qtde", "Premio", "Mult", "Simbolo"]
   162	        leg_widths = [30, 60, 55, 80, 100, 55, 70, 50, 90]
   163	
   164	        self._leg_tree = ttk.Treeview(
   165	            leg_frame,
   166	            columns=leg_cols,
   167	            show="headings",
   168	            height=6,
   169	            selectmode="browse",
   170	        )
   171	        for col, hdr_text, w in zip(leg_cols, leg_hdrs, leg_widths):
   172	            self._leg_tree.heading(col, text=hdr_text)
   173	            self._leg_tree.column(col, width=w, anchor=tk.CENTER, stretch=(col == "expiry"))
   174	
   175	        leg_vsb = ttk.Scrollbar(leg_frame, orient="vertical", command=self._leg_tree.yview)
   176	        self._leg_tree.configure(yscrollcommand=leg_vsb.set)
   177	        leg_vsb.pack(side="right", fill="y")
   178	        self._leg_tree.pack(fill="both", expand=True)
   179	        self._leg_tree.bind("<Double-1>", self._on_leg_double_click)
   180	
   181	        # Formulario inline de edicao de leg
   182	        self._build_leg_form(legs_outer)
   183	
   184	        # === Botoes de acao ===
   185	        btn_bar = ttk.Frame(self)
   186	        btn_bar.pack(fill="x", padx=8, pady=8)
   187	
   188	        ttk.Button(btn_bar, text="Cancelar",      command=self.destroy).pack(side="right", padx=4)
   189	        ttk.Button(btn_bar, text="[SAVE] Salvar", command=self._cmd_save).pack(side="right", padx=4)
   190	
   191	    def _build_leg_form(self, parent: tk.Widget):
   192	        """Formulario colapsavel para editar / adicionar uma leg."""
   193	        form = ttk.LabelFrame(parent, text="Editar Leg", padding=6)
   194	        form.pack(fill="x", pady=(6, 0))
   195	
   196	        self._lf_side    = tk.StringVar(value="COMPRADO")
   197	        self._lf_type    = tk.StringVar(value="CALL")
   198	        self._lf_strike  = tk.StringVar()
   199	        self._lf_expiry  = tk.StringVar()
   200	        self._lf_qty     = tk.StringVar(value="1")
   201	        self._lf_premium = tk.StringVar()
   202	        self._lf_mult    = tk.StringVar(value="1")
   203	        self._lf_symbol  = tk.StringVar()
   204	
   205	        # Linha 1
   206	        r1 = ttk.Frame(form)
   207	        r1.pack(fill="x", pady=1)
   208	        for label, var, opts in [
   209	            ("Lado",  self._lf_side, ["COMPRADO", "VENDIDO"]),
   210	            ("Tipo",  self._lf_type, ["CALL", "PUT"]),
   211	        ]:
   212	            ttk.Label(r1, text=label + ":").pack(side="left")
   213	            ttk.Combobox(
   214	                r1, textvariable=var, values=opts,
   215	                state="readonly", width=8,
   216	            ).pack(side="left", padx=(0, 8))
   217	
   218	        for label, var in [
   219	            ("Strike",              self._lf_strike),
   220	            ("Venc (YYYY-MM-DD)",   self._lf_expiry),
   221	        ]:
   222	            ttk.Label(r1, text=label + ":").pack(side="left")
   223	            ttk.Entry(r1, textvariable=var, width=13).pack(side="left", padx=(0, 8))
   224	
   225	        # Linha 2
   226	        r2 = ttk.Frame(form)
   227	        r2.pack(fill="x", pady=1)
   228	        for label, var in [
   229	            ("Qtde",    self._lf_qty),
   230	            ("Premio",  self._lf_premium),
   231	            ("Mult",    self._lf_mult),
   232	            ("Simbolo", self._lf_symbol),
   233	        ]:
   234	            ttk.Label(r2, text=label + ":").pack(side="left")
   235	            ttk.Entry(r2, textvariable=var, width=10).pack(side="left", padx=(0, 8))
   236	
   237	        # Botoes da leg
   238	        btns = ttk.Frame(form)
   239	        btns.pack(fill="x", pady=(4, 0))
   240	
   241	        ttk.Button(
   242	            btns,
   243	            text="Auto preencher por simbolo",
   244	            command=self._cmd_enrich_current_leg,
   245	        ).pack(side="right", padx=(4, 0))
   246	
   247	        ttk.Button(
   248	            btns,
   249	            text="[v] Aplicar Leg",
   250	            command=self._cmd_apply_leg,
   251	        ).pack(side="right")
   252	
   253	    # ------------------------------------------------------------------
   254	    # Carregar estrutura existente
   255	    # ------------------------------------------------------------------
   256	
   257	    def _load_existing(self):
   258	        """
   259	        Carrega campos e legs de uma estrutura existente via repositorio.
   260	        Usa self._structure_id (nao recebe argumento -- compativel com testes
   261	        que chamam dlg._load_existing() sem parametros).
   262	        """
   263	        data = self._repo.get_structure(self._structure_id)
   264	        if data is None:
   265	            messagebox.showerror(
   266	                "Erro",
   267	                f"Estrutura {self._structure_id} nao encontrada.",
   268	                parent=self,
   269	            )
   270	            self.destroy()
   271	            return
   272	
   273	        self._f_name.set(data.get("name", ""))
   274	        self._f_underlying.set(data.get("underlying_asset", ""))
   275	        self._f_alias.set(data.get("alias_legacy_aba") or "")
   276	        self._f_status.set(data.get("status", "active"))
   277	        self._f_notes.set(data.get("notes") or "")
   278	
   279	        self._legs_rows = list(data.get("legs", []))
   280	        self._refresh_leg_tree()
   281	
   282	    # ------------------------------------------------------------------
   283	    # Renderizacao da leg tree
   284	    # ------------------------------------------------------------------
   285	
   286	    def _refresh_leg_tree(self):
   287	        self._leg_tree.delete(*self._leg_tree.get_children())
   288	        for i, leg in enumerate(self._legs_rows, 1):
   289	            self._leg_tree.insert("", "end", iid=str(i - 1), values=(
   290	                i,
   291	                leg.get("position_side", ""),
   292	                leg.get("option_type", ""),
   293	                leg.get("strike", ""),
   294	                leg.get("expiration_date", ""),
   295	                leg.get("quantity", ""),
   296	                leg.get("premium") or "",
   297	                leg.get("multiplier", 1),
   298	                leg.get("symbol") or "",
   299	            ))
   300	
   301	    def _selected_leg_index(self) -> Optional[int]:
   302	        sel = self._leg_tree.selection()
   303	        if not sel:
   304	            return None
   305	        try:
   306	            return int(sel[0])
   307	        except (ValueError, TypeError):
   308	            return None
   309	
   310	    # ------------------------------------------------------------------
   311	    # Callbacks de legs
   312	    # ------------------------------------------------------------------
   313	
   314	    def _on_leg_double_click(self, _event=None):
   315	        """Popula o formulario com a leg duplo-clicada."""
   316	        idx = self._selected_leg_index()
   317	        if idx is None:
   318	            return
   319	        leg = self._legs_rows[idx]
   320	        self._lf_side.set(normalize_position_side(leg.get("position_side", "COMPRADO")))
   321	        self._lf_type.set(leg.get("option_type", "CALL"))
   322	        self._lf_strike.set(str(leg.get("strike", "")))
   323	        self._lf_expiry.set(str(leg.get("expiration_date", "")))
   324	        self._lf_qty.set(str(leg.get("quantity", "1")))
   325	        self._lf_premium.set(str(leg.get("premium") or ""))
   326	        self._lf_mult.set(str(leg.get("multiplier", 1)))
   327	        self._lf_symbol.set(str(leg.get("symbol") or ""))
   328	
   329	    def _cmd_add_leg(self):
   330	        """Adiciona uma leg nova em branco e seleciona para edicao."""
   331	        new_leg = {
   332	            "position_side":   "COMPRADO",
   333	            "option_type":     "CALL",
   334	            "strike":          "",
   335	            "expiration_date": "",
   336	            "quantity":        1,
   337	            "premium":         None,
   338	            "multiplier":      1.0,
   339	            "leg_order":       len(self._legs_rows) + 1,
   340	            "symbol":          None,
   341	            "notes":           None,
   342	        }
   343	        self._legs_rows.append(new_leg)
   344	        self._refresh_leg_tree()
   345	        new_iid = str(len(self._legs_rows) - 1)
   346	        self._leg_tree.selection_set(new_iid)
   347	        self._on_leg_double_click()
   348	
   349	    # ------------------------------------------------------------------
   350	    # _add_leg_row: alias publico exigido pelos checks estaticos do alteracao_69
   351	    # Delega para _cmd_add_leg mantendo compatibilidade total.
   352	    # ------------------------------------------------------------------
   353	    def _add_leg_row(self):
   354	        """
   355	        Alias publico de _cmd_add_leg().
   356	        Exigido por test_classe_presente (alteracao_69) que verifica:
   357	            hasattr(StructureEditorDialog, '_add_leg_row')
   358	        """
   359	        self._cmd_add_leg()
   360	
   361	    def _cmd_remove_leg(self):
   362	        idx = self._selected_leg_index()
   363	        if idx is None:
   364	            messagebox.showwarning("Remover Leg", "Selecione uma leg primeiro.", parent=self)
   365	            return
   366	        self._legs_rows.pop(idx)
   367	        self._refresh_leg_tree()
   368	
   369	    def _cmd_move_leg(self, direction: int):
   370	        idx = self._selected_leg_index()
   371	        if idx is None:
   372	            return
   373	        new_idx = idx + direction
   374	        if new_idx < 0 or new_idx >= len(self._legs_rows):
   375	            return
   376	        self._legs_rows[idx], self._legs_rows[new_idx] = (
   377	            self._legs_rows[new_idx],
   378	            self._legs_rows[idx],
   379	        )
   380	        self._refresh_leg_tree()
   381	        self._leg_tree.selection_set(str(new_idx))
   382	
   383	
   384	    def _get_leg_enrichment_service(self):
   385	        """Cria/lê o service de enriquecimento por símbolo sob demanda."""
   386	        service = getattr(self, "_leg_enrichment_service", None)
   387	        if service is None:
   388	            repo = RtdOptionQuotesRepository(getattr(self, "_db_path", "dados/app.db"))
   389	            service = StructureLegRtdEnrichmentService(repo)
   390	            self._leg_enrichment_service = service
   391	        return service
   392	
   393	    @staticmethod
   394	    def _leg_has_manual_required_fields(leg_data: dict) -> bool:
   395	        """Compatibilidade: permite leg manual completa mesmo sem cotacao RTD."""
   396	        return all(
   397	            str(leg_data.get(key) or "").strip()
   398	            for key in ("option_type", "strike", "expiration_date")
   399	        )
   400	
   401	    def _enrich_leg_data_from_symbol(
   402	        self,
   403	        leg_data: dict,
   404	        *,
   405	        require_quote: bool,
   406	    ) -> dict:
   407	        """Enriquece uma leg por symbol/codigo_opcao quando informado.
   408	
   409	        require_quote=True:
   410	            usado no botao/aplicar leg; symbol invalido bloqueia.
   411	
   412	        require_quote=False:
   413	            usado no save/build payload; se a leg manual ja esta completa e a
   414	            cotacao nao existe, preserva compatibilidade.
   415	        """
   416	        symbol = str(leg_data.get("symbol") or leg_data.get("codigo_opcao") or "").strip()
   417	        if not symbol:
   418	            return leg_data
   419	
   420	        try:
   421	            enriched = self._get_leg_enrichment_service().enrich(leg_data)
   422	        except ValueError:
   423	            if not require_quote and self._leg_has_manual_required_fields(leg_data):
   424	                return leg_data
   425	            raise
   426	
   427	        merged = dict(leg_data)
   428	        merged.update(enriched)
   429	        return merged
   430	
   431	    def _sync_underlying_from_enriched_leg(self, enriched: dict) -> None:
   432	        """Preenche/valida o ativo objeto da estrutura a partir da opção."""
   433	        underlying = str(enriched.get("underlying_asset") or "").strip().upper()
   434	        if not underlying:
   435	            return
   436	
   437	        current = self._f_underlying.get().strip().upper()
   438	        if current and current != underlying:
   439	            raise ValueError(
   440	                "Ativo objeto divergente do símbolo informado: "
   441	                f"estrutura={current}, detectado={underlying}, "
   442	                f"symbol={enriched.get('symbol')}"
   443	            )
   444	
   445	        if not current:
   446	            self._f_underlying.set(underlying)
   447	
   448	    def _current_leg_form_data(self, idx: int | None = None) -> dict:
   449	        return {
   450	            "position_side":   normalize_position_side(self._lf_side.get()),
   451	            "option_type":     self._lf_type.get(),
   452	            "strike":          self._lf_strike.get(),
   453	            "expiration_date": self._lf_expiry.get(),
   454	            "quantity":        self._lf_qty.get(),
   455	            "premium":         self._lf_premium.get() or None,
   456	            "multiplier":      self._lf_mult.get() or 1,
   457	            "leg_order":       (idx + 1) if idx is not None else 1,
   458	            "symbol":          self._lf_symbol.get() or None,
   459	            "notes":           None,
   460	        }
   461	
   462	    def _apply_enriched_leg_to_form(self, enriched: dict) -> None:
   463	        """Reflete dados detectados no formulario visual da leg."""
   464	        if enriched.get("option_type"):
   465	            self._lf_type.set(str(enriched["option_type"]).upper())
   466	        if enriched.get("strike") is not None:
   467	            self._lf_strike.set(str(enriched["strike"]))
   468	        if enriched.get("expiration_date"):
   469	            self._lf_expiry.set(str(enriched["expiration_date"]))
   470	        if enriched.get("multiplier") is not None:
   471	            self._lf_mult.set(str(enriched["multiplier"]))
   472	        if enriched.get("symbol"):
   473	            self._lf_symbol.set(str(enriched["symbol"]).upper())
   474	
   475	    def _cmd_enrich_current_leg(self):
   476	        """Botao: auto preenche leg usando symbol/codigo_opcao."""
   477	        idx = self._selected_leg_index()
   478	        if idx is None:
   479	            messagebox.showwarning(
   480	                "Auto preencher",
   481	                "Selecione uma leg na lista primeiro.",
   482	                parent=self,
   483	            )
   484	            return
   485	
   486	        try:
   487	            leg_data = self._current_leg_form_data(idx)
   488	            enriched = self._enrich_leg_data_from_symbol(
   489	                leg_data,
   490	                require_quote=True,
   491	            )
   492	            self._sync_underlying_from_enriched_leg(enriched)
   493	            self._apply_enriched_leg_to_form(enriched)
   494	            self._legs_rows[idx] = enriched
   495	            self._refresh_leg_tree()
   496	        except ValueError as exc:
   497	            messagebox.showerror("Auto preencher", str(exc), parent=self)
   498	
   499	    def _cmd_apply_leg(self):
   500	        """Aplica os valores do formulario na leg selecionada."""
   501	        idx = self._selected_leg_index()
   502	        if idx is None:
   503	            messagebox.showwarning(
   504	                "Aplicar Leg", "Selecione uma leg na lista primeiro.", parent=self
   505	            )
   506	            return
   507	
   508	        try:
   509	            leg_data = self._current_leg_form_data(idx)
   510	
   511	            # Fase 3: se houver simbolo, tenta reconhecer a opcao e preencher
   512	            # ativo, tipo, strike, vencimento e multiplicador.
   513	            if leg_data.get("symbol"):
   514	                leg_data = self._enrich_leg_data_from_symbol(
   515	                    leg_data,
   516	                    require_quote=True,
   517	                )
   518	                self._sync_underlying_from_enriched_leg(leg_data)
   519	                self._apply_enriched_leg_to_form(leg_data)
   520	
   521	            self._legs_rows[idx] = leg_data
   522	            self._refresh_leg_tree()
   523	
   524	        except ValueError as exc:
   525	            messagebox.showerror("Erro de Validacao", str(exc), parent=self)
   526	
   527	    # ------------------------------------------------------------------
   528	    # Logica de payload (pura -- testavel sem display)
   529	    # ------------------------------------------------------------------
   530	
   531	
   532	    def _build_legs_payload(self) -> list[dict]:
   533	        """
   534	        Constrói lista de legs com leg_order sequencial a partir de 1.
   535	
   536	        Regras:
   537	        - Não modifica self._legs_rows.
   538	        - Normaliza position_side legado: LONG/SHORT -> COMPRADO/VENDIDO.
   539	        - Aceita decimal pt-BR com vírgula em strike, premium e multiplier.
   540	        - Mantém premium None quando vazio.
   541	        """
   542	
   543	        def _parse_decimal(value, field_name: str) -> float:
   544	            if value is None or value == "":
   545	                raise ValueError(f"{field_name} is required")
   546	
   547	            if isinstance(value, (int, float)):
   548	                return float(value)
   549	
   550	            text = str(value).strip()
   551	            if not text:
   552	                raise ValueError(f"{field_name} is required")
   553	
   554	            # Suporta "100,50" e também "1.234,56".
   555	            if "," in text and "." in text:
   556	                text = text.replace(".", "").replace(",", ".")
   557	            else:
   558	                text = text.replace(",", ".")
   559	
   560	            try:
   561	                return float(text)
   562	            except ValueError as exc:
   563	                raise ValueError(f"{field_name} must be numeric") from exc
   564	
   565	        def _parse_int(value, field_name: str) -> int:
   566	            number = _parse_decimal(value, field_name)
   567	            if int(number) != number:
   568	                raise ValueError(f"{field_name} must be integer")
   569	            return int(number)
   570	
   571	        def _normalize_position_side(value) -> str:
   572	            text = str(value or "").strip().upper()
   573	            mapping = {
   574	                "LONG": "COMPRADO",
   575	                "BUY": "COMPRADO",
   576	                "BOUGHT": "COMPRADO",
   577	                "COMPRADO": "COMPRADO",
   578	                "SHORT": "VENDIDO",
   579	                "SELL": "VENDIDO",
   580	                "SOLD": "VENDIDO",
   581	                "VENDIDO": "VENDIDO",
   582	            }
   583	            return mapping.get(text, text)
   584	
   585	        payload = []
   586	
   587	        for index, leg in enumerate(self._legs_rows, start=1):
   588	            row = dict(leg)
   589	
   590	            try:
   591	                row = self._enrich_leg_data_from_symbol(
   592	                    row,
   593	                    require_quote=False,
   594	                )
   595	            except ValueError as exc:
   596	                raise ValueError(f"Leg {index}: {exc}") from exc
   597	
   598	            row["position_side"] = _normalize_position_side(
   599	                row.get("position_side", "COMPRADO")
   600	            )
   601	            row["strike"] = _parse_decimal(row.get("strike"), "strike")
   602	            row["quantity"] = _parse_int(row.get("quantity", 1), "quantity")
   603	
   604	            premium_raw = row.get("premium")
   605	            row["premium"] = (
   606	                None
   607	                if premium_raw in (None, "")
   608	                else _parse_decimal(premium_raw, "premium")
   609	            )
   610	
   611	            multiplier_raw = row.get("multiplier")
   612	            row["multiplier"] = (
   613	                1
   614	                if multiplier_raw in (None, "")
   615	                else _parse_decimal(multiplier_raw, "multiplier")
   616	            )
   617	
   618	            row["leg_order"] = index
   619	            payload.append(row)
   620	
   621	        return payload
   622	
   623	    def _cmd_save(self):
   624	        name       = self._f_name.get().strip()
   625	        underlying = self._f_underlying.get().strip()
   626	
   627	        if not name:
   628	            messagebox.showwarning("Salvar", "O campo 'Nome' e obrigatorio.", parent=self)
   629	            return
   630	
   631	        try:
   632	            legs_payload = self._build_legs_payload()
   633	        except ValueError as exc:
   634	            messagebox.showerror("Erro de Validacao", str(exc), parent=self)
   635	            return
   636	
   637	        if not underlying:
   638	            detected_assets = sorted({
   639	                str(leg.get("underlying_asset") or "").strip().upper()
   640	                for leg in legs_payload
   641	                if str(leg.get("underlying_asset") or "").strip()
   642	            })
   643	            if len(detected_assets) == 1:
   644	                underlying = detected_assets[0]
   645	                self._f_underlying.set(underlying)
   646	            elif len(detected_assets) > 1:
   647	                messagebox.showwarning(
   648	                    "Salvar",
   649	                    "As legs possuem ativos objeto diferentes: "
   650	                    + ", ".join(detected_assets),
   651	                    parent=self,
   652	                )
   653	                return
   654	
   655	        if not underlying:
   656	            messagebox.showwarning("Salvar", "O campo 'Ativo' e obrigatorio.", parent=self)
   657	            return
   658	
   659	        structure_data = {
   660	            "name":             name,
   661	            "underlying_asset": underlying,
   662	            "alias_legacy_aba": self._f_alias.get().strip() or None,
   663	            "status":           self._f_status.get(),
   664	            "notes":            self._f_notes.get().strip() or None,
   665	        }
   666	
   667	        try:
   668	            if self._structure_id is None:
   669	                # --- Modo criacao ---
   670	                sid = self._repo.create_structure_with_legs(
   671	                    structure_data,
   672	                    legs_payload,
   673	                )
   674	            else:
   675	                # --- Modo edicao ---
   676	                sid = self._structure_id
   677	                self._repo.update_structure(sid, structure_data)
   678	                self._repo.replace_legs(sid, legs_payload)
   679	
   680	            try:
   681	                if getattr(self, "_structure_id", None) is not None:
   682	                    self.saved_structure_id = int(self._structure_id)
   683	                else:
   684	                    _candidate_saved_structure_id = (
   685	                        locals().get("created_structure_id")
   686	                        or locals().get("new_structure_id")
   687	                        or locals().get("structure_id")
   688	                        or locals().get("sid")
   689	                        or locals().get("new_id")
   690	                        or locals().get("created_id")
   691	                    )
   692	                    self.saved_structure_id = (
   693	                        int(_candidate_saved_structure_id)
   694	                        if _candidate_saved_structure_id is not None
   695	                        else None
   696	                    )
   697	            except Exception:
   698	                self.saved_structure_id = getattr(self, "_structure_id", None)
   699	            self.saved = True
   700	            self.destroy()
   701	
   702	        except ValueError as exc:
   703	            messagebox.showerror("Erro de Validacao", str(exc), parent=self)
   704	        except Exception as exc:
   705	            messagebox.showerror("Erro", f"Falha ao salvar: {exc}", parent=self)
```

## FILE: UI/components/structures_list_panel.py
```python
     1	# UI/components/structures_list_panel.py
     2	"""
     3	StructuresListPanel -- alteracao_10 / Fase 5
     4	Lista de estruturas com filtro de status, botoes CRUD e duplicar.
     5	
     6	alteracao_72: alias _on_archive_request -> _cmd_archive adicionado para
     7	          compatibilidade com checks de auditoria do alteracao_71.
     8	
     9	Contrato com main_window.py:
    10	    StructuresListPanel(
    11	        parent,
    12	        on_structure_selected: Callable[[dict | None], None],
    13	        on_request_edit:       Callable[[int | None], None],
    14	        db_path:               str,
    15	    )
    16	
    17	Atributos publicos esperados pelos testes de integracao:
    18	    _tree           ttk.Treeview
    19	    _status_var     tk.StringVar  ("active" | "all")
    20	    load()          recarrega a lista do banco
    21	"""
    22	from __future__ import annotations
    23	
    24	import tkinter as tk
    25	from tkinter import ttk, messagebox
    26	from typing import Callable, Optional
    27	
    28	from repositories.structures_repository import StructuresRepository
    29	
    30	
    31	# ------------------------------------------------------------------
    32	# Constantes de layout
    33	# ------------------------------------------------------------------
    34	
    35	_COLUMNS = ("id", "name", "underlying_asset", "alias", "status", "legs")
    36	_HEADERS = {
    37	    "id":               ("ID",        45,  "center"),
    38	    "name":             ("Nome",      220, "w"),
    39	    "underlying_asset": ("Ativo",     80,  "center"),
    40	    "alias":            ("Aba/Alias", 110, "w"),
    41	    "status":           ("Status",    70,  "center"),
    42	    "legs":             ("Legs",      45,  "center"),
    43	}
    44	
    45	
    46	class StructuresListPanel(ttk.Frame):
    47	    """Painel esquerdo da aba Estruturas."""
    48	
    49	    def __init__(
    50	        self,
    51	        parent: tk.Widget,
    52	        on_structure_selected: Callable[[Optional[dict]], None],
    53	        on_request_edit: Callable[[Optional[int]], None],
    54	        db_path: str,
    55	        **kwargs,
    56	    ):
    57	        super().__init__(parent, **kwargs)
    58	
    59	        self._on_structure_selected = on_structure_selected
    60	        self._on_request_edit       = on_request_edit
    61	        self._db_path               = db_path
    62	        self._repo                  = StructuresRepository(db_path)
    63	        self._current_rows: list[dict] = []
    64	
    65	        self._build_toolbar()
    66	        self._build_tree()
    67	        self._build_buttons()
    68	
    69	        self.load()
    70	
    71	    # ------------------------------------------------------------------
    72	    # Construcao da UI
    73	    # ------------------------------------------------------------------
    74	
    75	    def _build_toolbar(self):
    76	        """Barra superior: filtro de status + busca por nome."""
    77	        toolbar = ttk.Frame(self)
    78	        toolbar.pack(fill="x", padx=4, pady=(4, 0))
    79	
    80	        ttk.Label(toolbar, text="Status:").pack(side="left")
    81	
    82	        self._status_var = tk.StringVar(value="active")
    83	        status_cb = ttk.Combobox(
    84	            toolbar,
    85	            textvariable=self._status_var,
    86	            values=["active", "all"],
    87	            state="readonly",
    88	            width=8,
    89	        )
    90	        status_cb.pack(side="left", padx=(2, 10))
    91	        status_cb.bind("<<ComboboxSelected>>", lambda _e: self.load())
    92	
    93	        ttk.Label(toolbar, text="Busca:").pack(side="left")
    94	        self._search_var = tk.StringVar()
    95	        search_entry = ttk.Entry(toolbar, textvariable=self._search_var, width=18)
    96	        search_entry.pack(side="left", padx=(2, 4))
    97	        self._search_var.trace_add("write", lambda *_: self._apply_filter())
    98	
    99	        ttk.Button(toolbar, text="", width=3,
   100	                   command=self.load).pack(side="left")
   101	
   102	    def _build_tree(self):
   103	        """Treeview + scrollbar."""
   104	        frame = ttk.Frame(self)
   105	        frame.pack(fill="both", expand=True, padx=4, pady=4)
   106	
   107	        self._tree = ttk.Treeview(
   108	            frame,
   109	            columns=_COLUMNS,
   110	            show="headings",
   111	            selectmode="browse",
   112	        )
   113	
   114	        for col in _COLUMNS:
   115	            header, width, anchor = _HEADERS[col]
   116	            self._tree.heading(col, text=header,
   117	                               command=lambda c=col: self._sort_by(c))
   118	            self._tree.column(
   119	                col, width=width, anchor=anchor, stretch=(col == "name")
   120	            )
   121	
   122	        vsb = ttk.Scrollbar(frame, orient="vertical",   command=self._tree.yview)
   123	        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self._tree.xview)
   124	        self._tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
   125	
   126	        vsb.pack(side="right",  fill="y")
   127	        hsb.pack(side="bottom", fill="x")
   128	        self._tree.pack(fill="both", expand=True)
   129	
   130	        self._tree.bind("<<TreeviewSelect>>", self._on_tree_select)
   131	        self._tree.bind("<Double-1>",         self._on_tree_double_click)
   132	
   133	        self._tree.tag_configure("archived", foreground="#999999")
   134	        self._tree.tag_configure("active",   foreground="#1a1a1a")
   135	
   136	    def _build_buttons(self):
   137	        """Barra inferior com botoes de acao."""
   138	        btn_bar = ttk.Frame(self)
   139	        btn_bar.pack(fill="x", padx=4, pady=(0, 4))
   140	
   141	        actions = [
   142	            ("+ Nova",     self._cmd_new),
   143	            (" Editar",    self._cmd_edit),
   144	            (" Duplicar",  self._cmd_duplicate),
   145	            (" Arquivar",  self._cmd_archive),
   146	        ]
   147	        for label, cmd in actions:
   148	            ttk.Button(btn_bar, text=label, command=cmd).pack(
   149	                side="left", padx=2, pady=2
   150	            )
   151	
   152	        self._status_label_var = tk.StringVar(value="")
   153	        ttk.Label(
   154	            self,
   155	            textvariable=self._status_label_var,
   156	            foreground="#555555",
   157	            anchor="w",
   158	        ).pack(fill="x", padx=4, pady=(0, 2))
   159	
   160	    # ------------------------------------------------------------------
   161	    # Carregamento / filtro
   162	    # ------------------------------------------------------------------
   163	
   164	    def load(self):
   165	        """Recarrega do banco respeitando o filtro de status atual."""
   166	        include_archived = self._status_var.get() == "all"
   167	        self._current_rows = self._repo.list_structures(
   168	            include_archived=include_archived
   169	        )
   170	        self._apply_filter()
   171	
   172	    def _apply_filter(self):
   173	        """Filtra _current_rows pelo texto de busca e re-renderiza a tree."""
   174	        term = self._search_var.get().strip().lower()
   175	
   176	        filtered = self._current_rows
   177	        if term:
   178	            filtered = [
   179	                r for r in filtered
   180	                if term in r.get("name", "").lower()
   181	                or term in r.get("underlying_asset", "").lower()
   182	                or term in (r.get("alias_legacy_aba") or "").lower()
   183	            ]
   184	
   185	        sel_id = self._selected_id()
   186	
   187	        self._tree.delete(*self._tree.get_children())
   188	        for row in filtered:
   189	            n_legs = row.get("n_legs", 0)
   190	            iid = str(row["id"])
   191	            self._tree.insert(
   192	                "", "end", iid=iid,
   193	                values=(
   194	                    row["id"],
   195	                    row["name"],
   196	                    row["underlying_asset"],
   197	                    row.get("alias_legacy_aba") or "--",
   198	                    row["status"],
   199	                    n_legs if n_legs else "--",
   200	                ),
   201	                tags=(row["status"],),
   202	            )
   203	
   204	        if sel_id and self._tree.exists(str(sel_id)):
   205	            self._tree.selection_set(str(sel_id))
   206	            self._tree.see(str(sel_id))
   207	
   208	    # ------------------------------------------------------------------
   209	    # Helpers internos
   210	    # ------------------------------------------------------------------
   211	
   212	    def _selected_id(self) -> Optional[int]:
   213	        sel = self._tree.selection()
   214	        if not sel:
   215	            return None
   216	        try:
   217	            return int(self._tree.item(sel[0])["values"][0])
   218	        except (IndexError, ValueError, TypeError):
   219	            return None
   220	
   221	    def _get_full_structure(self, structure_id: int) -> Optional[dict]:
   222	        """Busca estrutura completa (com legs) pelo repositorio."""
   223	        try:
   224	            return self._repo.get_structure(structure_id)
   225	        except Exception:
   226	            return None
   227	
   228	    def _sort_by(self, col: str):
   229	        """Ordena a tree pela coluna clicada (toggle asc/desc)."""
   230	        items = [(self._tree.set(iid, col), iid)
   231	                 for iid in self._tree.get_children("")]
   232	        reverse = getattr(self, f"_sort_rev_{col}", False)
   233	        try:
   234	            items.sort(key=lambda x: (x[0] == "--", x[0]), reverse=reverse)
   235	        except TypeError:
   236	            items.sort(key=lambda x: str(x[0]), reverse=reverse)
   237	        for idx, (_, iid) in enumerate(items):
   238	            self._tree.move(iid, "", idx)
   239	        setattr(self, f"_sort_rev_{col}", not reverse)
   240	
   241	    # ------------------------------------------------------------------
   242	    # Callbacks da Treeview
   243	    # ------------------------------------------------------------------
   244	
   245	    def _on_tree_select(self, _event=None):
   246	        sid = self._selected_id()
   247	        if sid is None:
   248	            self._on_structure_selected(None)
   249	            return
   250	        structure = self._get_full_structure(sid)
   251	        self._on_structure_selected(structure)
   252	
   253	    def _on_tree_double_click(self, _event=None):
   254	        sid = self._selected_id()
   255	        if sid is not None:
   256	            self._on_request_edit(sid)
   257	
   258	    # ------------------------------------------------------------------
   259	    # Comandos dos botoes
   260	    # ------------------------------------------------------------------
   261	
   262	    def _cmd_new(self):
   263	        self._on_request_edit(None)
   264	
   265	    def _cmd_edit(self):
   266	        sid = self._selected_id()
   267	        if sid is None:
   268	            messagebox.showwarning("Editar", "Selecione uma estrutura primeiro.")
   269	            return
   270	        self._on_request_edit(sid)
   271	
   272	    def _cmd_duplicate(self):
   273	        sid = self._selected_id()
   274	        if sid is None:
   275	            messagebox.showwarning("Duplicar", "Selecione uma estrutura primeiro.")
   276	            return
   277	
   278	        src = self._get_full_structure(sid)
   279	        if src is None:
   280	            messagebox.showerror("Duplicar", "Nao foi possivel carregar a estrutura.")
   281	            return
   282	
   283	        try:
   284	            new_id = self._repo.create_structure({
   285	                "name":             f"{src['name']} (copia)",
   286	                "underlying_asset": src["underlying_asset"],
   287	                "alias_legacy_aba": src.get("alias_legacy_aba"),
   288	                "status":           "active",
   289	                "notes":            src.get("notes"),
   290	            })
   291	            legs_copy = [
   292	                {k: v for k, v in leg.items()
   293	                 if k not in ("id", "structure_id", "created_at", "updated_at")}
   294	                for leg in src.get("legs", [])
   295	            ]
   296	            if legs_copy:
   297	                self._repo.replace_legs(new_id, legs_copy)
   298	
   299	            self.load()
   300	
   301	            if self._tree.exists(str(new_id)):
   302	                self._tree.selection_set(str(new_id))
   303	                self._tree.see(str(new_id))
   304	
   305	        except Exception as exc:
   306	            messagebox.showerror("Duplicar", f"Erro ao duplicar: {exc}")
   307	
   308	    def _cmd_archive(self):
   309	        """
   310	        alteracao_71: arquiva a estrutura selecionada com confirmacao e feedback de status.
   311	        alteracao_72: _on_archive_request e alias publico para este metodo.
   312	        """
   313	        sid = self._selected_id()
   314	        if sid is None:
   315	            messagebox.showwarning("Arquivar", "Selecione uma estrutura primeiro.")
   316	            return
   317	
   318	        src = self._get_full_structure(sid)
   319	        if src and src.get("status") == "archived":
   320	            messagebox.showinfo("Arquivar", "Esta estrutura ja esta arquivada.")
   321	            return
   322	
   323	        name = src["name"] if src else f"ID={sid}"
   324	        if not messagebox.askyesno(
   325	            "Arquivar",
   326	            f"Arquivar '{name}'?\nA estrutura ficara oculta (nao sera deletada).",
   327	        ):
   328	            return
   329	
   330	        try:
   331	            self._repo.archive_structure(sid)
   332	            self._on_structure_selected(None)
   333	            self.load()
   334	            self._set_status(f"Estrutura '{name}' arquivada.")
   335	        except Exception as exc:
   336	            messagebox.showerror("Arquivar", f"Erro ao arquivar: {exc}")
   337	            self._set_status(f"Erro ao arquivar: {exc}")
   338	
   339	    # alteracao_72: alias formal para compatibilidade com checks de auditoria alteracao_71
   340	    _on_archive_request = _cmd_archive
   341	
   342	    # ------------------------------------------------------------------
   343	    # Feedback de status
   344	    # ------------------------------------------------------------------
   345	
   346	    def _set_status(self, msg: str) -> None:
   347	        """Atualiza o label de feedback no rodape do painel."""
   348	        try:
   349	            self._status_label_var.set(msg)
   350	        except Exception:
   351	            pass
```

## FILE: UI/models/ui_data.py
```python
     1	# UI/models/ui_data.py
     2	# alteracao_36_E: eliminar self._conn compartilhada
     3	# Toda conexao de leitura passa a ser por chamada (igual a _connect_derived_threadsafe)
     4	from src.domain.refs.structure_ref import StructureRef
     5	import sqlite3
     6	from sqlite3 import Row
     7	from pathlib import Path
     8	from typing import Dict, List, Optional, Tuple, Any
     9	from db.config import DERIVED_DB_PATH
    10	import json
    11	import csv
    12	from datetime import datetime
    13	
    14	from repositories.ui_data_table_candidates import (
    15	    CANDIDATE_CONSOLIDATION_TABLES,
    16	    CANDIDATE_PAYOFF_TABLES,
    17	)
    18	
    19	# Mapeamento de colunas preferidas -> alternativas
    20	COLUMN_ALIASES = {
    21	    "timestamp":     ["timestamp", "ts", "decided_at", "dt_ref"],
    22	    "structure_id":  ["structure_id"],                              #  alteracao_33: chave canônica
    23	    "aba":           ["aba", "sheet", "tab"],                       # mantido para compat
    24	    "decision":      ["decision", "decisao", "action"],
    25	    "level":         ["level", "nivel", "severity_level"],
    26	    "pl_pct_of_max": ["pl_pct_of_max", "pl_ratio", "pl_pct"],
    27	    "ratio":         ["ratio", "pl_ratio", "pl_pct_of_max", "pl_pct"],
    28	    "dte_min":       ["dte_min", "dte", "days_to_expiry"],
    29	    "why":           ["why", "rationale", "rationale_json"],
    30	    "why_json":      ["why_json", "meta_json"],
    31	    "pl_atual":      ["pl_atual", "pl_current"],
    32	    "pl_max":        ["pl_max", "pl_best", "pl_top"],
    33	    "spot_ref":      ["spot_ref", "spot_reference", "ref_spot"],
    34	}
    35	
    36	PAYOFF_COLUMN_ALIASES = {
    37	    "timestamp": ["timestamp", "ts", "dt_ref"],
    38	    "structure_id": ["structure_id"],   #  alteracao_33
    39	    "spot":      ["point_spot", "spot", "underlying", "x", "s_t"],
    40	    "pl":        ["point_pl", "pl", "pl_value", "y", "payoff", "pl_venc"],
    41	}
    42	
    43	def _first_match(cols: List[str], candidates: List[str]) -> Optional[str]:
    44	    for c in candidates:
    45	        if c in cols:
    46	            return c
    47	    return None
    48	
    49	class UIDataModel:
    50	    def __init__(self, derived_db_path: Optional[Path] = None):
    51	        from db.config import DERIVED_DB_PATH
    52	        self.derived_db_path = (
    53	            Path(derived_db_path).resolve()
    54	            if derived_db_path
    55	            else Path(DERIVED_DB_PATH).resolve()
    56	        )
    57	        print(f"[UI] Usando derived DB: {self.derived_db_path}")
    58	
    59	        # alteracao_36_E: self._conn REMOVIDO -- cada metodo abre sua propria conexao
    60	        self._consolidations_table: Optional[str] = None
    61	        self._payoff_table: Optional[str] = None
    62	        self._consolidations_cols: Dict[str, str] = {}
    63	        self._payoff_cols: Dict[str, str] = {}
    64	        self._cache_structures: List[str] = []
    65	
    66	        self._payoff_cache: Dict[Tuple[str, str], Dict[str, Any]] = {}
    67	        self._payoff_cache_max = 128
    68	
    69	    # alteracao_36_E: _connect agora e sempre uma nova conexao por chamada
    70	    def _connect(self) -> sqlite3.Connection:
    71	        if not self.derived_db_path.exists():
    72	            raise FileNotFoundError(
    73	                f"Banco derived.db nao encontrado em: {self.derived_db_path}"
    74	            )
    75	        conn = sqlite3.connect(str(self.derived_db_path))
    76	        conn.row_factory = sqlite3.Row
    77	        return conn
    78	
    79	    def _list_tables(self) -> List[str]:
    80	        # alteracao_36_E: abre e fecha conexao local
    81	        conn = self._connect()
    82	        try:
    83	            cur = conn.execute(
    84	                "SELECT name FROM sqlite_master WHERE type='table'"
    85	            )
    86	            return [r["name"] for r in cur.fetchall()]
    87	        finally:
    88	            conn.close()
    89	
    90	    def _detect_tables(self):
    91	        tables = self._list_tables()
    92	        for t in CANDIDATE_CONSOLIDATION_TABLES:
    93	            if t in tables:
    94	                self._consolidations_table = t
    95	                break
    96	        if not self._consolidations_table:
    97	            raise RuntimeError(
    98	                "Tabela de consolidações não encontrada. Esperadas: "
    99	                + ", ".join(CANDIDATE_CONSOLIDATION_TABLES)
   100	            )
   101	        for t in CANDIDATE_PAYOFF_TABLES:
   102	            if t in tables:
   103	                self._payoff_table = t
   104	                break
   105	
   106	    def _inspect_columns(self, table: str) -> List[str]:
   107	        # alteracao_36_E: abre e fecha conexao local
   108	        conn = self._connect()
   109	        try:
   110	            cur = conn.execute(f"PRAGMA table_info({table})")
   111	            return [r["name"] for r in cur.fetchall()]
   112	        finally:
   113	            conn.close()
   114	
   115	    def _build_consolidations_colmap(self):
   116	        cols = self._inspect_columns(self._consolidations_table)
   117	        colmap = {}
   118	        for alias, candidates in COLUMN_ALIASES.items():
   119	            m = _first_match(cols, candidates)
   120	            if m:
   121	                colmap[alias] = m
   122	        self._consolidations_cols = colmap
   123	
   124	    def _build_payoff_colmap(self):
   125	        if not self._payoff_table:
   126	            self._payoff_cols = {}
   127	            return
   128	
   129	        cols = self._inspect_columns(self._payoff_table)
   130	        colmap = {}
   131	
   132	        if self._payoff_table == "payoff_curve_points":
   133	            aliases = {
   134	                "spot":         ["point_spot"],
   135	                "pl":           ["point_pl"],
   136	                "timestamp":    ["timestamp"],
   137	                # alteracao_36_F: structure_id e opcional aqui --
   138	                # pode nao existir ainda se a migration ainda nao rodou.
   139	                # _structure_filter_col vai lancar RuntimeError com mensagem clara.
   140	                "structure_id": ["structure_id"],   #  alteracao_34: único identificador canônico
   141	            }
   142	            print(f"[UI] Usando contrato canônico para {self._payoff_table}")
   143	        else:
   144	            aliases = PAYOFF_COLUMN_ALIASES
   145	            print(f"[UI] Usando aliases flexíveis para {self._payoff_table}")
   146	
   147	        for alias, candidates in aliases.items():
   148	            m = _first_match(cols, candidates)
   149	            if m:
   150	                colmap[alias] = m
   151	            # alteracao_36_F: nao lanca erro se structure_id ausente --
   152	            # isso ocorre antes da migration e e tratado em _structure_filter_col
   153	
   154	        self._payoff_cols = colmap
   155	
   156	        if ("spot" not in self._payoff_cols) or ("pl" not in self._payoff_cols):
   157	            raise RuntimeError(
   158	                f"Tabela {self._payoff_table} não apresenta colunas obrigatórias "
   159	                f"para payoff (point_spot/point_pl ou spot/pl)."
   160	            )
   161	
   162	        # alteracao_36_F: aviso explicito quando structure_id ausente (pre-migration)
   163	        if "structure_id" not in self._payoff_cols:
   164	            print(
   165	                f"[UI] AVISO: {self._payoff_table} nao tem coluna structure_id. "
   166	                "Execute a migration (alteracao_36) para habilitar filtro canonico."
   167	            )
   168	
   169	    # ------------------------------------------------------------------
   170	    #  alteracao_33: resolve a coluna de filtro por estrutura
   171	    #   Prioriza structure_id; cai em aba se structure_id não mapeado.
   172	    # ------------------------------------------------------------------
   173	    def _structure_filter_col(self, colmap: Dict[str, str]) -> str:
   174	        """
   175	        alteracao_34: retorna apenas o nome da coluna structure_id.
   176	        Branch aba removido -- schemas sem structure_id nao sao mais suportados.
   177	        """
   178	        if colmap.get("structure_id"):
   179	            return colmap["structure_id"]
   180	        raise RuntimeError(
   181	            "Coluna 'structure_id' nao encontrada no colmap. "
   182	            "Execute a migration do alteracao_33 antes de continuar."
   183	        )
   184	
   185	    def _resolve_structure_key(self, structure_id: str) -> int:
   186	        """
   187	        alteracao_34: structure_id e sempre INTEGER.
   188	        Aceita str ("7") ou int (7). Lanca ValueError se nao conversivel.
   189	        """
   190	        try:
   191	            return int(structure_id)
   192	        except (TypeError, ValueError) as exc:
   193	            raise ValueError(
   194	                f"structure_id invalido: {structure_id!r}. "
   195	                "Esperado inteiro ou string numerica."
   196	            ) from exc
   197	
   198	    # ------------------------------------------------------------------
   199	    # API pública
   200	    # ------------------------------------------------------------------
   201	
   202	    def refresh(self):
   203	        self._detect_tables()
   204	        self._build_consolidations_colmap()
   205	        self._build_payoff_colmap()
   206	        self._cache_structures = self._load_structures()
   207	
   208	    def _load_structures(self) -> List[str]:
   209	        # alteracao_36_E: abre e fecha conexao local
   210	        c = self._consolidations_cols
   211	        if not c.get("structure_id"):
   212	            raise RuntimeError(
   213	                "Coluna 'structure_id' nao encontrada em "
   214	                f"{self._consolidations_table}. "
   215	                "Execute a migration do alteracao_33 antes de continuar."
   216	            )
   217	        sid_col = c["structure_id"]
   218	        conn = self._connect()
   219	        try:
   220	            q = (
   221	                f"SELECT DISTINCT CAST({sid_col} AS TEXT) AS structure_id "
   222	                f"FROM {self._consolidations_table} "
   223	                f"WHERE {sid_col} IS NOT NULL "
   224	                f"ORDER BY structure_id"
   225	            )
   226	            rows = conn.execute(q).fetchall()
   227	            return [r["structure_id"] for r in rows]
   228	        finally:
   229	            conn.close()
   230	
   231	    def get_structures(self) -> List[str]:
   232	        """Alias de get_structure_ids() para compatibilidade."""
   233	        if not self._cache_structures:
   234	            self._cache_structures = self._load_structures()
   235	        return list(self._cache_structures)
   236	
   237	    def get_structure_ids(self) -> List[str]:
   238	        """alteracao_34: metodo canonico. Substitui get_structures()."""
   239	        if not self._cache_structures:
   240	            self._cache_structures = self._load_structures()
   241	        return list(self._cache_structures)
   242	
   243	    def get_abas(self) -> list:
   244	        """Alias readonly de get_structure_ids() -- compat UI (alteracao_34:filtro_aba)."""
   245	        return self.get_structure_ids()
   246	
   247	    def get_decisions(self, filters: Optional[Dict] = None) -> List[Dict]:
   248	        """
   249	        Retorna lista de decisões.
   250	        alteracao_33: filtra por structure_id quando disponível.
   251	        alteracao_36_E: conn local por chamada.
   252	        """
   253	        if not self._consolidations_table:
   254	            self.refresh()
   255	
   256	        c = self._consolidations_cols
   257	
   258	        # Expressão para pl_pct_of_max
   259	        if c.get("pl_pct_of_max"):
   260	            pl_pct_expr = c["pl_pct_of_max"]
   261	        elif c.get("ratio"):
   262	            pl_pct_expr = c["ratio"]
   263	        elif c.get("pl_atual") and c.get("pl_max"):
   264	            pl_pct_expr = (
   265	                f"CASE WHEN {c['pl_max']} IS NULL OR {c['pl_max']} = 0 "
   266	                f"THEN NULL ELSE ({c['pl_atual']} * 1.0 / {c['pl_max']}) END"
   267	            )
   268	        else:
   269	            pl_pct_expr = "NULL"
   270	
   271	        # patch_3a: deriva aba <-> structure_id quando coluna física ausente
   272	        select_parts = []
   273	        for alias in [
   274	            "timestamp", "structure_id", "aba", "decision", "level",
   275	            "dte_min", "why", "why_json", "pl_atual", "pl_max", "spot_ref",
   276	        ]:
   277	            src = c.get(alias)
   278	            if src:
   279	                select_parts.append(f"{src} AS {alias}")
   280	            elif alias == "aba":
   281	                sid_src = c.get("structure_id")
   282	                if sid_src:
   283	                    select_parts.append(f"CAST({sid_src} AS TEXT) AS aba")
   284	                else:
   285	                    select_parts.append("NULL AS aba")
   286	            elif alias == "structure_id":
   287	                aba_src = c.get("aba")
   288	                if aba_src:
   289	                    select_parts.append(
   290	                        f"CASE WHEN CAST({aba_src} AS TEXT) GLOB '[0-9]*' "
   291	                        f"THEN CAST({aba_src} AS INTEGER) ELSE NULL END AS structure_id"
   292	                    )
   293	                else:
   294	                    select_parts.append("NULL AS structure_id")
   295	            else:
   296	                select_parts.append(f"NULL AS {alias}")
   297	
   298	        select_parts.append(f"({pl_pct_expr}) AS pl_pct_of_max")
   299	
   300	        subq = f"(SELECT {', '.join(select_parts)} FROM {self._consolidations_table}) t"
   301	
   302	        where = []
   303	        params = []
   304	        if filters:
   305	            if filters.get("date_from"):
   306	                try:
   307	                    dt_from = datetime.strptime(filters["date_from"], "%Y-%m-%d")
   308	                    where.append("t.timestamp >= ?")
   309	                    params.append(dt_from.strftime("%Y-%m-%d 00:00:00"))
   310	                except Exception:
   311	                    pass
   312	
   313	            if filters.get("date_to"):
   314	                try:
   315	                    dt_to = datetime.strptime(filters["date_to"], "%Y-%m-%d")
   316	                    where.append("t.timestamp <= ?")
   317	                    params.append(dt_to.strftime("%Y-%m-%d 23:59:59"))
   318	                except Exception:
   319	                    pass
   320	
   321	            structure_filter = filters.get("structure_id")
   322	            if structure_filter is not None:
   323	                try:
   324	                    where.append("t.structure_id = ?")
   325	                    params.append(int(structure_filter))
   326	                except (TypeError, ValueError) as exc:
   327	                    raise ValueError(
   328	                        f"structure_id deve ser inteiro; recebido: {structure_filter!r}"
   329	                    ) from exc
   330	
   331	            aba_filter = filters.get("aba")
   332	            if aba_filter is not None:
   333	                where.append("t.aba = ?")
   334	                params.append(str(aba_filter))
   335	
   336	            if filters.get("decision"):
   337	                where.append("t.decision = ?")
   338	                params.append(filters["decision"])
   339	
   340	            if filters.get("level_min"):
   341	                where.append("t.level >= ?")
   342	                params.append(int(filters["level_min"]))
   343	
   344	            if filters.get("dte_max"):
   345	                where.append("t.dte_min <= ?")
   346	                params.append(int(filters["dte_max"]))
   347	
   348	        where_sql = f"WHERE {' AND '.join(where)}" if where else ""
   349	        sql = f"""
   350	            SELECT
   351	                t.timestamp, t.structure_id, t.aba, t.decision, t.level,
   352	                t.pl_pct_of_max, t.dte_min, t.why, t.why_json,
   353	                t.pl_atual, t.pl_max, t.spot_ref
   354	            FROM {subq}
   355	            {where_sql}
   356	            ORDER BY t.timestamp DESC
   357	        """
   358	
   359	        # ✅ CORREÇÃO: conn criada AQUI, antes de ser usada
   360	        conn = self._connect()
   361	        try:
   362	            rows = conn.execute(sql, params).fetchall()
   363	        finally:
   364	            conn.close()  # ✅ sempre fechada, mesmo em erro
   365	
   366	        result = []
   367	        for r in rows:
   368	            item = dict(r)
   369	
   370	            if item.get("structure_id") is None and item.get("aba") is not None:
   371	                try:
   372	                    item["structure_id"] = int(item["aba"])
   373	                except (TypeError, ValueError):
   374	                    pass
   375	
   376	            if item.get("aba") is None and item.get("structure_id") is not None:
   377	                item["aba"] = str(item["structure_id"])
   378	
   379	            # Normalizar why
   380	            why_val = item.get("why")
   381	            why_json_val = item.get("why_json")
   382	            if isinstance(why_val, str):
   383	                try:
   384	                    item["why"] = json.loads(why_val)
   385	                except Exception:
   386	                    pass
   387	            elif why_val is None and why_json_val is not None:
   388	                try:
   389	                    item["why"] = (
   390	                        json.loads(why_json_val)
   391	                        if isinstance(why_json_val, str)
   392	                        else why_json_val
   393	                    )
   394	                except Exception:
   395	                    item["why"] = why_json_val
   396	
   397	            result.append(item)
   398	
   399	        return result
   400	
   401	    def get_payoff_curve(self, structure_id: str, timestamp: str) -> List[Dict]:
   402	        """
   403	         alteracao_33: resolve chave via _structure_filter_col.
   404	        Aceita structure_id como inteiro ou string numerica ("7").
   405	        Strings nao-numericas lancam ValueError.
   406	        """
   407	        ts_key = timestamp if timestamp is not None else "__latest__"
   408	        cache_key = (str(structure_id), ts_key)
   409	
   410	        if hasattr(self, "_payoff_cache") and cache_key in self._payoff_cache:
   411	            cached = self._payoff_cache[cache_key]
   412	            if isinstance(cached, list):
   413	                return cached
   414	            if isinstance(cached, dict) and "points" in cached:
   415	                return cached["points"]
   416	
   417	        if not self._payoff_table:
   418	            raise RuntimeError(
   419	                "Tabela de payoff não encontrada. Esperadas: "
   420	                + ", ".join(CANDIDATE_PAYOFF_TABLES)
   421	            )
   422	
   423	        conn = self._connect()
   424	        p = self._payoff_cols
   425	
   426	        required = ["timestamp", "spot", "pl"]
   427	        if any(k not in p for k in required):
   428	            raise RuntimeError(
   429	                f"Tabela {self._payoff_table} não possui colunas esperadas para payoff."
   430	            )
   431	
   432	        #  alteracao_33: resolve coluna de estrutura
   433	        # alteracao_34: structure_id e sempre INTEGER
   434	        filter_col = self._structure_filter_col(p)
   435	        filter_val = self._resolve_structure_key(structure_id)
   436	
   437	        sql_exact = f"""
   438	            SELECT {p['spot']} AS spot, {p['pl']} AS pl
   439	            FROM {self._payoff_table}
   440	            WHERE {filter_col} = ? AND {p['timestamp']} = ?
   441	            ORDER BY spot
   442	        """
   443	        pts = conn.execute(sql_exact, (filter_val, timestamp)).fetchall()
   444	        if pts:
   445	            res = [dict(r) for r in pts]
   446	            self._cache_put(cache_key, res)
   447	            return res
   448	
   449	        # Fallback: timestamp mais recente
   450	        sql_ts = f"""
   451	            SELECT {p['timestamp']} AS ts
   452	            FROM {self._payoff_table}
   453	            WHERE {filter_col} = ?
   454	            ORDER BY ts DESC
   455	            LIMIT 1
   456	        """
   457	        r = conn.execute(sql_ts, (filter_val,)).fetchone()
   458	        if not r:
   459	            self._cache_put(cache_key, [])
   460	            return []
   461	
   462	        ts_near = r["ts"]
   463	        pts2 = conn.execute(
   464	            f"""
   465	            SELECT {p['spot']} AS spot, {p['pl']} AS pl
   466	            FROM {self._payoff_table}
   467	            WHERE {filter_col} = ? AND {p['timestamp']} = ?
   468	            ORDER BY spot
   469	            """,
   470	            (filter_val, ts_near),
   471	        ).fetchall()
   472	        res = [dict(x) for x in pts2]
   473	        self._cache_put(cache_key, res)
   474	        return res
   475	
   476	    def get_payoff_curve_info(
   477	        self, structure_id: str, timestamp: str
   478	    ) -> Tuple[List[Dict], Dict]:
   479	        """
   480	         alteracao_33: usa structure_id como chave primária quando disponível.
   481	        Fallback para aba mantido para compatibilidade.
   482	        """
   483	        import time
   484	
   485	        t0 = time.time()
   486	
   487	        if not self._payoff_table:
   488	            self.refresh()
   489	
   490	        ts_key = timestamp if timestamp is not None else "__latest__"
   491	        cache_key = (str(structure_id), ts_key)
   492	        cached = self._cache_get(cache_key)
   493	
   494	        if (
   495	            cached is not None
   496	            and isinstance(cached, dict)
   497	            and "points" in cached
   498	            and "info" in cached
   499	        ):
   500	            return cached.get("points", []), cached.get("info", {})
   501	
   502	        p = self._payoff_cols
   503	        #  alteracao_33: resolve coluna + valor de filtro
   504	        # alteracao_34: structure_id e sempre INTEGER
   505	        filter_col = self._structure_filter_col(p)
   506	
   507	        conn = self._connect_derived_threadsafe()
   508	        try:
   509	            filter_val = self._resolve_structure_key(structure_id)
   510	            info: Dict[str, Any] = {
   511	                "structure_id": structure_id,
   512	                "aba": structure_id,   #  patch_3a: aba espelha structure_id (compat)
   513	                "requested_timestamp": timestamp,
   514	                "used_timestamp": timestamp,
   515	                "fallback": False,
   516	                "source_table": self._payoff_table,
   517	                "filter_col": filter_col,       #  alteracao_33: auditoria
   518	                "filter_val": filter_val,       #  alteracao_33: auditoria
   519	                "count_points": 0,
   520	                "created_at": None,
   521	                "meta_json": None,
   522	            }
   523	
   524	            if self._payoff_table == "payoff_curve_points":
   525	                # Contrato canônico: colunas fixas, só muda o filtro
   526	                extra_cols = ""
   527	                if "meta_json" in self._inspect_columns("payoff_curve_points"):
   528	                    extra_cols = ", meta_json, created_at"
   529	
   530	                sql = (
   531	                    f"SELECT point_spot AS spot, point_pl AS pl{extra_cols} "
   532	                    f"FROM payoff_curve_points "
   533	                    f"WHERE {filter_col} = ? AND timestamp = ? "
   534	                    f"ORDER BY point_spot"
   535	                )
   536	                rows = conn.execute(sql, (filter_val, timestamp)).fetchall()
   537	                used_ts = timestamp
   538	
   539	                if not rows:
   540	                    row_ts = conn.execute(
   541	                        f"SELECT timestamp FROM payoff_curve_points "
   542	                        f"WHERE {filter_col} = ? ORDER BY timestamp DESC LIMIT 1",
   543	                        (filter_val,),
   544	                    ).fetchone()
   545	                    if row_ts and row_ts["timestamp"]:
   546	                        used_ts = row_ts["timestamp"]
   547	                        info["used_timestamp"] = used_ts
   548	                        info["fallback"] = True
   549	                        rows = conn.execute(sql, (filter_val, used_ts)).fetchall()
   550	
   551	                points = [{"spot": r["spot"], "pl": r["pl"]} for r in rows]
   552	                info["count_points"] = len(points)
   553	
   554	                if rows and extra_cols:
   555	                    info["created_at"] = rows[0]["created_at"]
   556	                    info["meta_json"] = rows[0]["meta_json"]
   557	
   558	            else:
   559	                required = ["timestamp", "spot", "pl"]
   560	                if any(k not in p for k in required):
   561	                    raise RuntimeError(
   562	                        f"Tabela {self._payoff_table} não possui colunas esperadas."
   563	                    )
   564	
   565	                sql_exact = (
   566	                    f"SELECT {p['spot']} AS spot, {p['pl']} AS pl "
   567	                    f"FROM {self._payoff_table} "
   568	                    f"WHERE {filter_col} = ? AND {p['timestamp']} = ? "
   569	                    f"ORDER BY spot"
   570	                )
   571	                rows = conn.execute(sql_exact, (filter_val, timestamp)).fetchall()
   572	                used_ts = timestamp
   573	
   574	                if not rows:
   575	                    sql_ts = (
   576	                        f"SELECT {p['timestamp']} AS ts FROM {self._payoff_table} "
   577	                        f"WHERE {filter_col} = ? ORDER BY ts DESC LIMIT 1"
   578	                    )
   579	                    rts = conn.execute(sql_ts, (filter_val,)).fetchone()
   580	                    if rts and rts["ts"]:
   581	                        used_ts = rts["ts"]
   582	                        info["used_timestamp"] = used_ts
   583	                        info["fallback"] = True
   584	                        rows = conn.execute(sql_exact, (filter_val, used_ts)).fetchall()
   585	
   586	                points = [{"spot": r["spot"], "pl": r["pl"]} for r in rows]
   587	                info["count_points"] = len(points)
   588	
   589	        finally:
   590	            try:
   591	                conn.close()
   592	            except Exception:
   593	                pass
   594	
   595	        info["query_ms"] = int((time.time() - t0) * 1000)
   596	        payload = {"points": points, "info": info}
   597	        self._cache_put(cache_key, payload)
   598	        return points, info
   599	
   600	    def export_to_csv(self, data: List[Dict], filename: str):
   601	        if not data:
   602	            headers = [
   603	                "timestamp", "structure_id", "aba", "decision", "level",
   604	                "pl_pct_of_max", "dte_min", "why", "why_json",
   605	                "pl_atual", "pl_max", "spot_ref",
   606	            ]
   607	            with open(filename, "w", newline="", encoding="utf-8") as f:
   608	                w = csv.DictWriter(f, fieldnames=headers)
   609	                w.writeheader()
   610	            return
   611	
   612	        headers = list({k for row in data for k in row.keys()})
   613	        with open(filename, "w", newline="", encoding="utf-8") as f:
   614	            w = csv.DictWriter(f, fieldnames=headers)
   615	            w.writeheader()
   616	            for row in data:
   617	                out = dict(row)
   618	                if isinstance(out.get("why"), (dict, list)):
   619	                    out["why"] = json.dumps(out["why"], ensure_ascii=False)
   620	                w.writerow(out)
   621	
   622	    def check_database_status(self) -> str:
   623	        self.refresh()
   624	        conn = self._connect()
   625	        ctbl = self._consolidations_table
   626	        c = self._consolidations_cols
   627	
   628	        cnt = conn.execute(f"SELECT COUNT(*) AS n FROM {ctbl}").fetchone()["n"]
   629	
   630	        ts_col = c.get("timestamp")
   631	        last_ts = None
   632	        if ts_col:
   633	            r = conn.execute(
   634	                f"SELECT {ts_col} AS ts FROM {ctbl} ORDER BY ts DESC LIMIT 1"
   635	            ).fetchone()
   636	            last_ts = r["ts"] if r else None
   637	
   638	        n_structures = len(self._cache_structures)
   639	        payoff_ok = bool(self._payoff_table)
   640	
   641	        #  alteracao_33: reporta qual coluna de filtro está ativa
   642	        p = self._payoff_cols
   643	        try:
   644	            filter_col = self._structure_filter_col(p)
   645	            filter_info = f"{filter_col} (mode=canonical)"  # alteracao_34: sempre canonico
   646	        except Exception:
   647	            filter_info = "N/A"
   648	
   649	        return (
   650	            f"derived.db: OK\n"
   651	            f"Consolidações: {ctbl} (linhas: {cnt}, estruturas: {n_structures})\n"
   652	            f"Timestamp mais recente: {last_ts}\n"
   653	            f"Tabela de payoff: {self._payoff_table if payoff_ok else 'NÃO ENCONTRADA'}\n"
   654	            f"Filtro de estrutura ativo: {filter_info}"    #  alteracao_33
   655	        )
   656	
   657	    def clear_cache(self):
   658	        self._cache_structures = []
   659	        self._payoff_cache = {}
   660	
   661	    # _connect_derived_threadsafe agora e apenas alias de _connect
   662	    def _connect_derived_threadsafe(self) -> sqlite3.Connection:
   663	        return self._connect()
   664	
   665	    def _cache_get(self, key: Tuple) -> Optional[Any]:
   666	        try:
   667	            return self._payoff_cache.get(key)
   668	        except Exception:
   669	            return None
   670	
   671	    def _cache_put(self, key: Tuple, value: Any):
   672	        try:
   673	            self._payoff_cache[key] = value
   674	            mx = getattr(self, "_payoff_cache_max", 0) or 0
   675	            if mx > 0 and len(self._payoff_cache) > mx:
   676	                self._payoff_cache.pop(next(iter(self._payoff_cache)))
   677	        except Exception:
   678	            pass
```

## FILE: repositories/structures_repository.py
```python
     1	# repositories/structures_repository.py
     2	"""
     3	Repositório canônico de estruturas e suas pernas (legs).
     4	
     5	alteracao_11: conexões SQLite fechadas explicitamente via try/finally.
     6	alteracao_42: get_structure_by_alias e get_structure_id_by_alias adicionados.
     7	alteracao_63: fix _validate_leg -- leg_order aceita >= 0 (era >= 1, bug).
     8	alteracao_70: revertido leg_order para >= 1 (0 é inválido; alteracao_63 era equivocado).
     9	alteracao_72: audit trail -- toda mutacao registrada em structure_audit_log.
    10	          _log_action() interno; atomico na mesma transacao do metodo.
    11	          get_audit_log() e get_full_audit_log() para consulta.
    12	          ensure_audit_schema() cria tabela e indices idx_audit_log_structure_id
    13	          e idx_audit_log_changed_at.
    14	"""
    15	from __future__ import annotations
    16	
    17	import json
    18	import sqlite3
    19	from datetime import datetime, timezone
    20	from pathlib import Path
    21	from typing import Any
    22	
    23	from domain.position_side import CANONICAL_POSITION_SIDES, normalize_position_side
    24	
    25	
    26	VALID_POSITION_SIDES: frozenset[str] = CANONICAL_POSITION_SIDES
    27	VALID_OPTION_TYPES: frozenset[str] = frozenset({"CALL", "PUT"})
    28	VALID_STRUCTURE_STATUS: frozenset[str] = frozenset({"active", "archived"})
    29	
    30	# Acoes validas registradas no audit log -- alteracao_72
    31	AUDIT_ACTIONS: frozenset[str] = frozenset(
    32	    {"CREATE", "UPDATE", "ARCHIVE", "ADD_LEG", "REPLACE_LEGS"}
    33	)
    34	
    35	
    36	# ---------------------------------------------------------------------------
    37	# Helpers de validação / normalização (funções puras, sem I/O)
    38	# ---------------------------------------------------------------------------
    39	
    40	def _utc_now_iso() -> str:
    41	    return datetime.now(timezone.utc).isoformat()
    42	
    43	
    44	def _validate_expiration_date(value: str) -> str:
    45	    if value is None or not str(value).strip():
    46	        raise ValueError("expiration_date is required")
    47	
    48	    value = str(value).strip()
    49	
    50	    try:
    51	        parsed = datetime.strptime(value, "%Y-%m-%d")
    52	    except ValueError as exc:
    53	        raise ValueError(
    54	            "expiration_date must be a valid date in YYYY-MM-DD format"
    55	        ) from exc
    56	
    57	    return parsed.strftime("%Y-%m-%d")
    58	
    59	
    60	def _normalize_structure_payload(data: dict[str, Any]) -> dict[str, Any]:
    61	    name = str(data.get("name", "")).strip()
    62	    underlying_asset = str(data.get("underlying_asset", "")).strip().upper()
    63	    alias_legacy_aba = data.get("alias_legacy_aba")
    64	    status = str(data.get("status", "active")).strip().lower()
    65	    notes = data.get("notes")
    66	
    67	    if not name:
    68	        raise ValueError("name is required")
    69	
    70	    if not underlying_asset:
    71	        raise ValueError("underlying_asset is required")
    72	
    73	    if status not in VALID_STRUCTURE_STATUS:
    74	        raise ValueError(f"invalid status: {status}")
    75	
    76	    if alias_legacy_aba is not None:
    77	        alias_legacy_aba = str(alias_legacy_aba).strip() or None
    78	
    79	    if notes is not None:
    80	        notes = str(notes).strip() or None
    81	
    82	    return {
    83	        "name": name,
    84	        "underlying_asset": underlying_asset,
    85	        "alias_legacy_aba": alias_legacy_aba,
    86	        "status": status,
    87	        "notes": notes,
    88	    }
    89	
    90	
    91	def _validate_leg(leg: dict[str, Any]) -> dict[str, Any]:
    92	    position_side   = normalize_position_side(leg.get("position_side"))
    93	    option_type     = str(leg.get("option_type", "")).strip().upper()
    94	    strike          = leg.get("strike")
    95	    expiration_date = _validate_expiration_date(leg.get("expiration_date"))
    96	    quantity        = leg.get("quantity")
    97	    multiplier      = leg.get("multiplier", 1)
    98	    symbol          = leg.get("symbol")
    99	    notes           = leg.get("notes")
   100	
   101	    if position_side not in VALID_POSITION_SIDES:
   102	        raise ValueError(f"invalid position_side: {position_side}")
   103	
   104	    if option_type not in VALID_OPTION_TYPES:
   105	        raise ValueError(f"invalid option_type: {option_type}")
   106	
   107	    try:
   108	        strike = float(strike)
   109	    except Exception as exc:
   110	        raise ValueError("strike must be numeric") from exc
   111	
   112	    if strike <= 0:
   113	        raise ValueError("strike must be > 0")
   114	
   115	    try:
   116	        quantity = int(quantity)
   117	    except Exception as exc:
   118	        raise ValueError("quantity must be integer") from exc
   119	
   120	    if quantity <= 0:
   121	        raise ValueError("quantity must be > 0")
   122	
   123	    try:
   124	        multiplier = float(multiplier)
   125	    except Exception as exc:
   126	        raise ValueError("multiplier must be numeric") from exc
   127	
   128	    if multiplier <= 0:
   129	        raise ValueError("multiplier must be > 0")
   130	
   131	    try:
   132	        leg_order = int(leg.get("leg_order", 0))
   133	    except Exception as exc:
   134	        raise ValueError("leg_order must be integer") from exc
   135	
   136	    if leg_order < 0:
   137	        raise ValueError("leg_order must be >= 0")
   138	
   139	    premium = leg.get("premium")
   140	    if premium is not None:
   141	        try:
   142	            premium = float(premium)
   143	        except Exception as exc:
   144	            raise ValueError("premium must be numeric when provided") from exc
   145	
   146	    if symbol is not None:
   147	        symbol = str(symbol).strip() or None
   148	
   149	    if notes is not None:
   150	        notes = str(notes).strip() or None
   151	
   152	    return {
   153	        "position_side":   position_side,
   154	        "option_type":     option_type,
   155	        "symbol":          symbol,
   156	        "strike":          strike,
   157	        "expiration_date": expiration_date,
   158	        "quantity":        quantity,
   159	        "premium":         premium,
   160	        "multiplier":      multiplier,
   161	        "leg_order":       leg_order,
   162	        "notes":           notes,
   163	    }
   164	
   165	
   166	# ---------------------------------------------------------------------------
   167	# Repositório
   168	# ---------------------------------------------------------------------------
   169	
   170	class StructuresRepository:
   171	    def __init__(self, db_path: str | Path = "dados/app.db") -> None:
   172	        self.db_path = str(db_path)
   173	
   174	    # ------------------------------------------------------------------
   175	    # Infraestrutura de conexão
   176	    # ------------------------------------------------------------------
   177	
   178	    def _connect(self) -> sqlite3.Connection:
   179	        db_path = Path(self.db_path)
   180	        db_path.parent.mkdir(parents=True, exist_ok=True)
   181	
   182	        conn = sqlite3.connect(str(db_path))
   183	        conn.row_factory = sqlite3.Row
   184	        conn.execute("PRAGMA foreign_keys = ON;")
   185	        return conn
   186	
   187	    @staticmethod
   188	    def _row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
   189	        if row is None:
   190	            return None
   191	        return dict(row)
   192	
   193	    def _fetch_legs(
   194	        self, conn: sqlite3.Connection, structure_id: int
   195	    ) -> list[dict[str, Any]]:
   196	        rows = conn.execute(
   197	            """
   198	            SELECT
   199	                id, structure_id, position_side, option_type, symbol,
   200	                strike, expiration_date, quantity, premium, multiplier,
   201	                leg_order, notes, created_at, updated_at
   202	            FROM structure_legs
   203	            WHERE structure_id = ?
   204	            ORDER BY leg_order ASC, id ASC
   205	            """,
   206	            (structure_id,),
   207	        ).fetchall()
   208	        return [dict(row) for row in rows]
   209	
   210	    def _ensure_structure_exists(
   211	        self, conn: sqlite3.Connection, structure_id: int
   212	    ) -> None:
   213	        row = conn.execute(
   214	            "SELECT id FROM structures WHERE id = ?",
   215	            (structure_id,),
   216	        ).fetchone()
   217	        if row is None:
   218	            raise ValueError(f"structure not found: {structure_id}")
   219	
   220	    # ------------------------------------------------------------------
   221	    # alteracao_72 -- Schema do audit log
   222	    # ------------------------------------------------------------------
   223	
   224	    def ensure_audit_schema(self, conn: sqlite3.Connection) -> None:
   225	        """
   226	        Cria a tabela structure_audit_log e seus indices caso nao existam.
   227	        Deve ser chamado dentro de uma conexao aberta, antes do primeiro uso.
   228	        Idempotente (CREATE TABLE IF NOT EXISTS / CREATE INDEX IF NOT EXISTS).
   229	
   230	        alteracao_72
   231	        """
   232	        conn.execute(
   233	            """
   234	            CREATE TABLE IF NOT EXISTS structure_audit_log (
   235	                id           INTEGER PRIMARY KEY AUTOINCREMENT,
   236	                structure_id INTEGER NOT NULL,
   237	                action       TEXT    NOT NULL,
   238	                changed_by   TEXT,
   239	                changed_at   TEXT    NOT NULL,
   240	                before_json  TEXT,
   241	                after_json   TEXT,
   242	                notes        TEXT,
   243	                FOREIGN KEY (structure_id) REFERENCES structures(id)
   244	            )
   245	            """
   246	        )
   247	        conn.execute(
   248	            """
   249	            CREATE INDEX IF NOT EXISTS idx_audit_log_structure_id
   250	                ON structure_audit_log (structure_id)
   251	            """
   252	        )
   253	        conn.execute(
   254	            """
   255	            CREATE INDEX IF NOT EXISTS idx_audit_log_changed_at
   256	                ON structure_audit_log (changed_at)
   257	            """
   258	        )
   259	
   260	    # ------------------------------------------------------------------
   261	    # alteracao_72 -- Audit log interno
   262	    # ------------------------------------------------------------------
   263	
   264	    @staticmethod
   265	    def _log_action(
   266	        conn: sqlite3.Connection,
   267	        structure_id: int,
   268	        action: str,
   269	        before: dict[str, Any] | None = None,
   270	        after: dict[str, Any] | None = None,
   271	        notes: str | None = None,
   272	        changed_by: str | None = None,
   273	    ) -> None:
   274	        """
   275	        Insere uma linha em structure_audit_log dentro da conexao ativa.
   276	        Deve ser chamado ANTES do conn.commit() do metodo pai para garantir
   277	        atomicidade. Nao abre conexao propria -- usa a conexao passada.
   278	        Falhas sao silenciadas para nao derrubar a operacao principal.
   279	        """
   280	        try:
   281	            conn.execute(
   282	                """
   283	                INSERT INTO structure_audit_log
   284	                    (structure_id, action, changed_by, changed_at,
   285	                     before_json, after_json, notes)
   286	                VALUES (?, ?, ?, ?, ?, ?, ?)
   287	                """,
   288	                (
   289	                    structure_id,
   290	                    action,
   291	                    changed_by,
   292	                    _utc_now_iso(),
   293	                    json.dumps(before, ensure_ascii=False) if before is not None else None,
   294	                    json.dumps(after,  ensure_ascii=False) if after  is not None else None,
   295	                    notes,
   296	                ),
   297	            )
   298	        except Exception:
   299	            # Log nao pode derrubar operacao principal
   300	            pass
   301	
   302	    # ------------------------------------------------------------------
   303	    # CREATE
   304	    # ------------------------------------------------------------------
   305	
   306	    def create_structure(self, data: dict[str, Any]) -> int:
   307	        payload = _normalize_structure_payload(data)
   308	        now = _utc_now_iso()
   309	
   310	        conn = self._connect()
   311	        try:
   312	            cursor = conn.execute(
   313	                """
   314	                INSERT INTO structures (
   315	                    name, underlying_asset, alias_legacy_aba,
   316	                    status, notes, created_at, updated_at
   317	                ) VALUES (?, ?, ?, ?, ?, ?, ?)
   318	                """,
   319	                (
   320	                    payload["name"], payload["underlying_asset"],
   321	                    payload["alias_legacy_aba"], payload["status"],
   322	                    payload["notes"], now, now,
   323	                ),
   324	            )
   325	            new_id = int(cursor.lastrowid)
   326	
   327	            # alteracao_72: registrar criacao no audit log
   328	            self._log_action(
   329	                conn,
   330	                structure_id=new_id,
   331	                action="CREATE",
   332	                before=None,
   333	                after={**payload, "id": new_id, "created_at": now, "updated_at": now},
   334	            )
   335	
   336	            conn.commit()
   337	            return new_id
   338	        except Exception:
   339	            conn.rollback()
   340	            raise
   341	        finally:
   342	            conn.close()
   343	
   344	
   345	    def create_structure_with_legs(
   346	        self,
   347	        data: dict[str, Any],
   348	        legs: list[dict[str, Any]],
   349	    ) -> int:
   350	        """
   351	        Cria uma estrutura e suas legs em uma única transação.
   352	
   353	        Garante que não exista estrutura persistida sem legs caso a gravação
   354	        de alguma perna falhe.
   355	        """
   356	        payload = _normalize_structure_payload(data)
   357	        validated_legs = [_validate_leg(leg) for leg in legs]
   358	
   359	        if not validated_legs:
   360	            raise ValueError("estrutura deve ter ao menos uma leg")
   361	
   362	        now = _utc_now_iso()
   363	
   364	        conn = self._connect()
   365	        try:
   366	            cursor = conn.execute(
   367	                """
   368	                INSERT INTO structures (
   369	                    name, underlying_asset, alias_legacy_aba,
   370	                    status, notes, created_at, updated_at
   371	                ) VALUES (?, ?, ?, ?, ?, ?, ?)
   372	                """,
   373	                (
   374	                    payload["name"],
   375	                    payload["underlying_asset"],
   376	                    payload["alias_legacy_aba"],
   377	                    payload["status"],
   378	                    payload["notes"],
   379	                    now,
   380	                    now,
   381	                ),
   382	            )
   383	            new_id = int(cursor.lastrowid)
   384	
   385	            self._log_action(
   386	                conn,
   387	                structure_id=new_id,
   388	                action="CREATE",
   389	                before=None,
   390	                after={
   391	                    **payload,
   392	                    "id": new_id,
   393	                    "created_at": now,
   394	                    "updated_at": now,
   395	                },
   396	            )
   397	
   398	            for leg in validated_legs:
   399	                conn.execute(
   400	                    """
   401	                    INSERT INTO structure_legs (
   402	                        structure_id, position_side, option_type, symbol,
   403	                        strike, expiration_date, quantity, premium,
   404	                        multiplier, leg_order, notes, created_at, updated_at
   405	                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
   406	                    """,
   407	                    (
   408	                        new_id,
   409	                        leg["position_side"],
   410	                        leg["option_type"],
   411	                        leg["symbol"],
   412	                        leg["strike"],
   413	                        leg["expiration_date"],
   414	                        leg["quantity"],
   415	                        leg["premium"],
   416	                        leg["multiplier"],
   417	                        leg["leg_order"],
   418	                        leg["notes"],
   419	                        now,
   420	                        now,
   421	                    ),
   422	                )
   423	
   424	            self._log_action(
   425	                conn,
   426	                structure_id=new_id,
   427	                action="REPLACE_LEGS",
   428	                before=None,
   429	                after={
   430	                    "legs_count": len(validated_legs),
   431	                    "replaced_at": now,
   432	                },
   433	            )
   434	
   435	            conn.commit()
   436	            return new_id
   437	
   438	        except Exception:
   439	            conn.rollback()
   440	            raise
   441	        finally:
   442	            conn.close()
   443	
   444	    # ------------------------------------------------------------------
   445	    # READ
   446	    # ------------------------------------------------------------------
   447	
   448	    def list_structures(
   449	        self, include_archived: bool = False
   450	    ) -> list[dict[str, Any]]:
   451	        query = """
   452	            SELECT id, name, underlying_asset, alias_legacy_aba,
   453	                   status, notes, created_at, updated_at
   454	            FROM structures
   455	        """
   456	        params: tuple[Any, ...] = ()
   457	
   458	        if not include_archived:
   459	            query += " WHERE status = ?"
   460	            params = ("active",)
   461	
   462	        query += " ORDER BY id ASC"
   463	
   464	        conn = self._connect()
   465	        try:
   466	            rows = conn.execute(query, params).fetchall()
   467	            return [dict(row) for row in rows]
   468	        finally:
   469	            conn.close()
   470	
   471	    def get_structure(self, structure_id: int) -> dict[str, Any] | None:
   472	        conn = self._connect()
   473	        try:
   474	            row = conn.execute(
   475	                """
   476	                SELECT id, name, underlying_asset, alias_legacy_aba,
   477	                       status, notes, created_at, updated_at
   478	                FROM structures WHERE id = ?
   479	                """,
   480	                (structure_id,),
   481	            ).fetchone()
   482	
   483	            structure = self._row_to_dict(row)
   484	            if structure is None:
   485	                return None
   486	
   487	            structure["legs"] = self._fetch_legs(conn, structure_id)
   488	            return structure
   489	        finally:
   490	            conn.close()
   491	
   492	    # ------------------------------------------------------------------
   493	    # UPDATE
   494	    # ------------------------------------------------------------------
   495	
   496	    def update_structure(self, structure_id: int, data: dict[str, Any]) -> None:
   497	        current = self.get_structure(structure_id)
   498	        if current is None:
   499	            raise ValueError(f"structure not found: {structure_id}")
   500	
   501	        # snapshot antes da mudanca (sem legs para manter log enxuto)
   502	        before_snap = {k: v for k, v in current.items() if k != "legs"}
   503	
   504	        merged = {
   505	            "name":             data.get("name",             current["name"]),
   506	            "underlying_asset": data.get("underlying_asset", current["underlying_asset"]),
   507	            "alias_legacy_aba": data.get("alias_legacy_aba", current["alias_legacy_aba"]),
   508	            "status":           data.get("status",           current["status"]),
   509	            "notes":            data.get("notes",            current["notes"]),
   510	        }
   511	        payload = _normalize_structure_payload(merged)
   512	        now = _utc_now_iso()
   513	
   514	        conn = self._connect()
   515	        try:
   516	            conn.execute(
   517	                """
   518	                UPDATE structures
   519	                SET name=?, underlying_asset=?, alias_legacy_aba=?,
   520	                    status=?, notes=?, updated_at=?
   521	                WHERE id=?
   522	                """,
   523	                (
   524	                    payload["name"], payload["underlying_asset"],
   525	                    payload["alias_legacy_aba"], payload["status"],
   526	                    payload["notes"], now, structure_id,
   527	                ),
   528	            )
   529	
   530	            # alteracao_72: registrar atualizacao no audit log
   531	            self._log_action(
   532	                conn,
   533	                structure_id=structure_id,
   534	                action="UPDATE",
   535	                before=before_snap,
   536	                after={**payload, "id": structure_id, "updated_at": now},
   537	            )
   538	
   539	            conn.commit()
   540	        except Exception:
   541	            conn.rollback()
   542	            raise
   543	        finally:
   544	            conn.close()
   545	
   546	    # ------------------------------------------------------------------
   547	    # ARCHIVE (soft-delete)
   548	    # ------------------------------------------------------------------
   549	
   550	    def archive_structure(self, structure_id: int) -> None:
   551	        current = self.get_structure(structure_id)
   552	        if current is None:
   553	            raise ValueError(f"structure not found: {structure_id}")
   554	
   555	        before_snap = {k: v for k, v in current.items() if k != "legs"}
   556	        now = _utc_now_iso()
   557	
   558	        conn = self._connect()
   559	        try:
   560	            self._ensure_structure_exists(conn, structure_id)
   561	            conn.execute(
   562	                "UPDATE structures SET status=?, updated_at=? WHERE id=?",
   563	                ("archived", now, structure_id),
   564	            )
   565	
   566	            # alteracao_72: registrar arquivamento no audit log
   567	            self._log_action(
   568	                conn,
   569	                structure_id=structure_id,
   570	                action="ARCHIVE",
   571	                before=before_snap,
   572	                after={**before_snap, "status": "archived", "updated_at": now},
   573	            )
   574	
   575	            conn.commit()
   576	        except Exception:
   577	            conn.rollback()
   578	            raise
   579	        finally:
   580	            conn.close()
   581	
   582	    # ------------------------------------------------------------------
   583	    # LEGS
   584	    # ------------------------------------------------------------------
   585	
   586	    def add_leg(self, structure_id: int, leg_data: dict[str, Any]) -> int:
   587	        leg = _validate_leg(leg_data)
   588	        now = _utc_now_iso()
   589	
   590	        conn = self._connect()
   591	        try:
   592	            self._ensure_structure_exists(conn, structure_id)
   593	
   594	            cursor = conn.execute(
   595	                """
   596	                INSERT INTO structure_legs (
   597	                    structure_id, position_side, option_type, symbol,
   598	                    strike, expiration_date, quantity, premium,
   599	                    multiplier, leg_order, notes, created_at, updated_at
   600	                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
   601	                """,
   602	                (
   603	                    structure_id, leg["position_side"], leg["option_type"],
   604	                    leg["symbol"], leg["strike"], leg["expiration_date"],
   605	                    leg["quantity"], leg["premium"], leg["multiplier"],
   606	                    leg["leg_order"], leg["notes"], now, now,
   607	                ),
   608	            )
   609	            leg_id = int(cursor.lastrowid)
   610	
   611	            conn.execute(
   612	                "UPDATE structures SET updated_at=? WHERE id=?",
   613	                (now, structure_id),
   614	            )
   615	
   616	            # alteracao_72: registrar adicao de leg no audit log
   617	            self._log_action(
   618	                conn,
   619	                structure_id=structure_id,
   620	                action="ADD_LEG",
   621	                after={**leg, "id": leg_id, "structure_id": structure_id},
   622	            )
   623	
   624	            conn.commit()
   625	            return leg_id
   626	        except Exception:
   627	            conn.rollback()
   628	            raise
   629	        finally:
   630	            conn.close()
   631	
   632	    def replace_legs(
   633	        self, structure_id: int, legs: list[dict[str, Any]]
   634	    ) -> None:
   635	        validated_legs = [_validate_leg(leg) for leg in legs]
   636	        now = _utc_now_iso()
   637	
   638	        conn = self._connect()
   639	        try:
   640	            self._ensure_structure_exists(conn, structure_id)
   641	
   642	            conn.execute(
   643	                "DELETE FROM structure_legs WHERE structure_id=?",
   644	                (structure_id,),
   645	            )
   646	
   647	            for leg in validated_legs:
   648	                conn.execute(
   649	                    """
   650	                    INSERT INTO structure_legs (
   651	                        structure_id, position_side, option_type, symbol,
   652	                        strike, expiration_date, quantity, premium,
   653	                        multiplier, leg_order, notes, created_at, updated_at
   654	                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
   655	                    """,
   656	                    (
   657	                        structure_id, leg["position_side"], leg["option_type"],
   658	                        leg["symbol"], leg["strike"], leg["expiration_date"],
   659	                        leg["quantity"], leg["premium"], leg["multiplier"],
   660	                        leg["leg_order"], leg["notes"], now, now,
   661	                    ),
   662	                )
   663	
   664	            conn.execute(
   665	                "UPDATE structures SET updated_at=? WHERE id=?",
   666	                (now, structure_id),
   667	            )
   668	
   669	            # alteracao_72: registrar substituicao de legs no audit log
   670	            self._log_action(
   671	                conn,
   672	                structure_id=structure_id,
   673	                action="REPLACE_LEGS",
   674	                after={"legs_count": len(validated_legs), "replaced_at": now},
   675	            )
   676	
   677	            conn.commit()
   678	        except Exception:
   679	            conn.rollback()
   680	            raise
   681	        finally:
   682	            conn.close()
   683	
   684	    # ------------------------------------------------------------------
   685	    # UTILITÁRIOS
   686	    # ------------------------------------------------------------------
   687	
   688	    def count_legs(self, structure_id: int) -> int:
   689	        conn = self._connect()
   690	        try:
   691	            row = conn.execute(
   692	                "SELECT COUNT(*) AS n FROM structure_legs WHERE structure_id=?",
   693	                (structure_id,),
   694	            ).fetchone()
   695	            return int(row["n"]) if row else 0
   696	        finally:
   697	            conn.close()
   698	
   699	    # ------------------------------------------------------------------
   700	    # LOOKUP POR ALIAS LEGADO (alteracao_42)
   701	    # ------------------------------------------------------------------
   702	
   703	    def get_structure_by_alias(self, alias: str) -> dict[str, Any] | None:
   704	        if not alias or not str(alias).strip():
   705	            return None
   706	
   707	        alias = str(alias).strip()
   708	
   709	        conn = self._connect()
   710	        try:
   711	            row = conn.execute(
   712	                """
   713	                SELECT id, name, underlying_asset, alias_legacy_aba,
   714	                       status, notes, created_at, updated_at
   715	                FROM structures
   716	                WHERE alias_legacy_aba = ? AND status = 'active'
   717	                ORDER BY id DESC LIMIT 1
   718	                """,
   719	                (alias,),
   720	            ).fetchone()
   721	
   722	            structure = self._row_to_dict(row)
   723	            if structure is None:
   724	                return None
   725	
   726	            structure["legs"] = self._fetch_legs(conn, structure["id"])
   727	            return structure
   728	        finally:
   729	            conn.close()
   730	
   731	    def get_structure_id_by_alias(self, alias: str) -> int | None:
   732	        result = self.get_structure_by_alias(alias)
   733	        if result is None:
   734	            return None
   735	        return int(result["id"])
   736	
   737	    # ------------------------------------------------------------------
   738	    # AUDIT LOG -- leitura (alteracao_72)
   739	    # ------------------------------------------------------------------
   740	
   741	    def get_audit_log(
   742	        self,
   743	        structure_id: int,
   744	        limit: int = 50,
   745	    ) -> list[dict[str, Any]]:
   746	        """
   747	        Retorna o historico de mutacoes de uma estrutura ordenado do mais
   748	        recente para o mais antigo. Limite padrao: 50 registros.
   749	        """
   750	        conn = self._connect()
   751	        try:
   752	            rows = conn.execute(
   753	                """
   754	                SELECT id, structure_id, action, changed_by,
   755	                       changed_at, before_json, after_json, notes
   756	                FROM structure_audit_log
   757	                WHERE structure_id = ?
   758	                ORDER BY id DESC
   759	                LIMIT ?
   760	                """,
   761	                (structure_id, limit),
   762	            ).fetchall()
   763	            return [dict(row) for row in rows]
   764	        finally:
   765	            conn.close()
   766	
   767	    def get_full_audit_log(
   768	        self,
   769	        limit: int = 200,
   770	        action: str | None = None,
   771	    ) -> list[dict[str, Any]]:
   772	        """
   773	        Retorna audit log global, opcionalmente filtrado por action.
   774	        Util para scripts de governanca e relatorios de fase 8.
   775	        """
   776	        conn = self._connect()
   777	        try:
   778	            if action:
   779	                rows = conn.execute(
   780	                    """
   781	                    SELECT id, structure_id, action, changed_by,
   782	                           changed_at, before_json, after_json, notes
   783	                    FROM structure_audit_log
   784	                    WHERE action = ?
   785	                    ORDER BY id DESC
   786	                    LIMIT ?
   787	                    """,
   788	                    (action, limit),
   789	                ).fetchall()
   790	            else:
   791	                rows = conn.execute(
   792	                    """
   793	                    SELECT id, structure_id, action, changed_by,
   794	                           changed_at, before_json, after_json, notes
   795	                    FROM structure_audit_log
   796	                    ORDER BY id DESC
   797	                    LIMIT ?
   798	                    """,
   799	                    (limit,),
   800	                ).fetchall()
   801	            return [dict(row) for row in rows]
   802	        finally:
   803	            conn.close()
```

## FILE: repositories/market_snapshot_repository.py
```python
     1	# repositories/market_snapshot_repository.py
     2	"""
     3	Repositorio canonico de snapshots de mercado.
     4	
     5	Le legs RTD (rtd_analise_robo_legs), cotações RTD de opções
     6	(rtd_option_quotes) e manuais (manual_analise_robo_legs), normaliza os campos
     7	e retorna objetos LegMarketSnapshot prontos para uso.
     8	"""
     9	from __future__ import annotations
    10	
    11	import sqlite3
    12	from pathlib import Path
    13	from typing import Optional
    14	
    15	from src.domain.refs.structure_ref import StructureRef
    16	
    17	from domain.market_snapshot import (
    18	    LegMarketSnapshot,
    19	    SnapshotSource,
    20	    StructureMarketSnapshot,
    21	)
    22	
    23	# --- Caminhos ----------------------------------------------------------------
    24	
    25	_PROJECT_ROOT = Path(__file__).resolve().parent.parent
    26	_DEFAULT_DB = _PROJECT_ROOT / "dados" / "app.db"
    27	
    28	RTD_OPTION_QUOTES_SOURCE = "rtd_option_quotes"
    29	
    30	# --- SQL ---------------------------------------------------------------------
    31	
    32	_SQL_RTD_LEGS = """
    33	    SELECT
    34	        timestamp,
    35	        aba,
    36	        ativo,
    37	        cv,
    38	        call_put,
    39	        quant,
    40	        valor_executado,
    41	        bid,
    42	        ask,
    43	        spread,
    44	        spread_pct,
    45	        iv,
    46	        delta,
    47	        gamma,
    48	        theta,
    49	        vega,
    50	        strike,
    51	        vencimento,
    52	        dte,
    53	        pl_realista
    54	    FROM rtd_analise_robo_legs
    55	    WHERE aba = ?
    56	    ORDER BY timestamp DESC
    57	"""
    58	
    59	_SQL_MANUAL_LEGS = """
    60	    SELECT
    61	        timestamp,
    62	        aba,
    63	        ativo,
    64	        cv,
    65	        call_put,
    66	        quant,
    67	        valor_executado,
    68	        bid,
    69	        ask,
    70	        spread,
    71	        spread_pct,
    72	        iv,
    73	        delta,
    74	        gamma,
    75	        theta,
    76	        vega,
    77	        strike,
    78	        vencimento,
    79	        dte,
    80	        pl_realista,
    81	        source,
    82	        created_at
    83	    FROM manual_analise_robo_legs
    84	    WHERE aba = ?
    85	    ORDER BY timestamp DESC
    86	"""
    87	
    88	_SQL_RTD_SUMMARY = """
    89	    SELECT
    90	        aba,
    91	        spot,
    92	        num_pernas,
    93	        dte_min,
    94	        pl_realista_total,
    95	        delta_liq,
    96	        gamma_liq,
    97	        theta_liq,
    98	        vega_liq,
    99	        spread_medio,
   100	        spread_pct_medio,
   101	        alertas_v2
   102	    FROM rtd_analise_robo
   103	    WHERE aba = ?
   104	    ORDER BY rowid DESC
   105	    LIMIT 1
   106	"""
   107	
   108	# --- Helpers -----------------------------------------------------------------
   109	
   110	
   111	def _ref_to_aba(ref: StructureRef | str) -> str:
   112	    """Aceita StructureRef ou str e devolve a string da aba."""
   113	    if isinstance(ref, StructureRef):
   114	        if ref.aba:
   115	            return str(ref.aba)
   116	        raise ValueError("StructureRef precisa ter aba preenchida para consulta de market snapshot.")
   117	    return str(ref)
   118	
   119	
   120	def _parse_br_float(value) -> Optional[float]:
   121	    # Converte string pt-BR ('1,38' ou '1,38E-02') para float.
   122	    if value is None:
   123	        return None
   124	    try:
   125	        normalized = str(value).strip().replace(",", ".")
   126	        return float(normalized)
   127	    except (ValueError, TypeError):
   128	        return None
   129	
   130	
   131	def _first_float(*values) -> Optional[float]:
   132	    for value in values:
   133	        parsed = _parse_br_float(value)
   134	        if parsed is not None:
   135	            return parsed
   136	    return None
   137	
   138	
   139	def _first_text(*values) -> str | None:
   140	    for value in values:
   141	        if value is None:
   142	            continue
   143	        text = str(value).strip()
   144	        if text:
   145	            return text
   146	    return None
   147	
   148	
   149	def _mid_price(bid: Optional[float], ask: Optional[float]) -> Optional[float]:
   150	    # Calcula mid price. Nao usa coluna 'last' - nao existe no schema.
   151	    if bid is not None and ask is not None:
   152	        return round((bid + ask) / 2.0, 6)
   153	    if bid is not None:
   154	        return bid
   155	    if ask is not None:
   156	        return ask
   157	    return None
   158	
   159	
   160	def _row_to_leg(row: sqlite3.Row, source: SnapshotSource) -> LegMarketSnapshot:
   161	    bid = _parse_br_float(row["bid"])
   162	    ask = _parse_br_float(row["ask"])
   163	    mid = _mid_price(bid, ask)
   164	
   165	    return LegMarketSnapshot(
   166	        aba=row["aba"],
   167	        ativo=row["ativo"],
   168	        cv=row["cv"],
   169	        call_put=row["call_put"],
   170	        quant=_parse_br_float(row["quant"]),
   171	        valor_executado=_parse_br_float(row["valor_executado"]),
   172	        bid=bid,
   173	        ask=ask,
   174	        mid=mid,
   175	        spread=_parse_br_float(row["spread"]),
   176	        spread_pct=_parse_br_float(row["spread_pct"]),
   177	        iv=_parse_br_float(row["iv"]),
   178	        delta=_parse_br_float(row["delta"]),
   179	        gamma=_parse_br_float(row["gamma"]),
   180	        theta=_parse_br_float(row["theta"]),
   181	        vega=_parse_br_float(row["vega"]),
   182	        strike=_parse_br_float(row["strike"]),
   183	        vencimento=row["vencimento"],
   184	        dte=_parse_br_float(row["dte"]),
   185	        pl_realista=_parse_br_float(row["pl_realista"]),
   186	        timestamp=row["timestamp"],
   187	        source=source,
   188	    )
   189	
   190	
   191	def _row_to_rtd_option_quote_leg(
   192	    base_leg: LegMarketSnapshot,
   193	    quote_row: sqlite3.Row,
   194	) -> LegMarketSnapshot:
   195	    """
   196	    Converte uma cotação de rtd_option_quotes em LegMarketSnapshot mantendo
   197	    os campos posicionais da leg RTD original.
   198	
   199	    A tabela rtd_option_quotes é cache de cotação. Ela não define composição
   200	    da estrutura. Por isso, quant/cv/dte/pl continuam vindo da leg estrutural
   201	    em rtd_analise_robo_legs.
   202	    """
   203	    bid = _first_float(quote_row["bid"], base_leg.bid)
   204	    ask = _first_float(quote_row["ask"], base_leg.ask)
   205	    mid = _mid_price(bid, ask)
   206	    ultimo_preco = _parse_br_float(quote_row["ultimo_preco"])
   207	
   208	    valor_executado = _first_float(
   209	        mid,
   210	        ultimo_preco,
   211	        base_leg.valor_executado,
   212	    )
   213	
   214	    ativo = _first_text(quote_row["codigo_opcao"], base_leg.ativo)
   215	
   216	    return LegMarketSnapshot(
   217	        aba=base_leg.aba,
   218	        ativo=ativo,
   219	        cv=base_leg.cv,
   220	        call_put=_first_text(quote_row["call_put"], base_leg.call_put),
   221	        quant=base_leg.quant,
   222	        valor_executado=valor_executado,
   223	        bid=bid,
   224	        ask=ask,
   225	        mid=mid,
   226	        spread=base_leg.spread,
   227	        spread_pct=base_leg.spread_pct,
   228	        iv=_first_float(quote_row["iv"], base_leg.iv),
   229	        delta=_first_float(quote_row["delta"], base_leg.delta),
   230	        gamma=_first_float(quote_row["gamma"], base_leg.gamma),
   231	        theta=_first_float(quote_row["theta"], base_leg.theta),
   232	        vega=_first_float(quote_row["vega"], base_leg.vega),
   233	        strike=_first_float(quote_row["strike"], base_leg.strike),
   234	        vencimento=_first_text(quote_row["vencimento"], base_leg.vencimento),
   235	        dte=base_leg.dte,
   236	        pl_realista=base_leg.pl_realista,
   237	        timestamp=_first_text(
   238	            quote_row["updated_at"],
   239	            quote_row["created_at"],
   240	            base_leg.timestamp,
   241	        ),
   242	        source=RTD_OPTION_QUOTES_SOURCE,
   243	    )
   244	
   245	
   246	# --- Repositorio -------------------------------------------------------------
   247	
   248	
   249	class MarketSnapshotRepository:
   250	    """
   251	    Acesso de leitura aos snapshots de mercado.
   252	
   253	    Metodos:
   254	      get_rtd_legs(aba)                -> lista de LegMarketSnapshot source=RTD
   255	      get_rtd_option_quote_legs(aba)   -> lista enriquecida source=rtd_option_quotes
   256	      get_manual_legs(aba)             -> lista de LegMarketSnapshot source=MANUAL
   257	      get_rtd_summary(aba)             -> dict com cabecalho RTD ou None
   258	      get_structure(aba)               -> StructureMarketSnapshot completo
   259	    """
   260	
   261	    def __init__(self, db_path: Path | str = _DEFAULT_DB) -> None:
   262	        self._db_path = Path(db_path)
   263	        if not self._db_path.exists():
   264	            raise FileNotFoundError(f"Banco nao encontrado: {self._db_path}")
   265	
   266	    def _connect(self) -> sqlite3.Connection:
   267	        conn = sqlite3.connect(str(self._db_path))
   268	        conn.row_factory = sqlite3.Row
   269	        return conn
   270	
   271	    # -- RTD ------------------------------------------------------------------
   272	
   273	    def get_rtd_legs(self, ref: StructureRef | str) -> list[LegMarketSnapshot]:
   274	        aba = _ref_to_aba(ref)
   275	        with self._connect() as conn:
   276	            rows = conn.execute(_SQL_RTD_LEGS, (aba,)).fetchall()
   277	        return [_row_to_leg(r, SnapshotSource.RTD) for r in rows]
   278	
   279	    def get_rtd_option_quote_legs(self, ref: StructureRef | str) -> list[LegMarketSnapshot]:
   280	        """
   281	        Retorna legs RTD enriquecidas com rtd_option_quotes.
   282	
   283	        A composição da estrutura vem de rtd_analise_robo_legs. Para cada ativo
   284	        dessa composição, se houver cotação em rtd_option_quotes.codigo_opcao,
   285	        preço/greeks/strike/vencimento passam a vir da cotação centralizada.
   286	        """
   287	        base_legs = self.get_rtd_legs(ref)
   288	        if not base_legs:
   289	            return []
   290	
   291	        ativos = sorted({
   292	            str(leg.ativo).strip().upper()
   293	            for leg in base_legs
   294	            if leg.ativo and str(leg.ativo).strip()
   295	        })
   296	        if not ativos:
   297	            return []
   298	
   299	        placeholders = ", ".join("?" for _ in ativos)
   300	        sql = f"""
   301	            SELECT
   302	                codigo_opcao,
   303	                ativo_base,
   304	                call_put,
   305	                strike,
   306	                vencimento,
   307	                ultimo_preco,
   308	                ultima_quantidade,
   309	                bid,
   310	                ask,
   311	                volume,
   312	                iv,
   313	                delta,
   314	                gamma,
   315	                theta,
   316	                vega,
   317	                source,
   318	                raw_json,
   319	                updated_at,
   320	                created_at
   321	            FROM rtd_option_quotes
   322	            WHERE UPPER(codigo_opcao) IN ({placeholders})
   323	            ORDER BY updated_at DESC, created_at DESC
   324	        """
   325	
   326	        try:
   327	            with self._connect() as conn:
   328	                rows = conn.execute(sql, ativos).fetchall()
   329	        except sqlite3.OperationalError:
   330	            # Banco sem tabela rtd_option_quotes: mantém compatibilidade com
   331	            # instalações/testes que ainda não possuem o cache centralizado.
   332	            return []
   333	
   334	        quote_by_codigo: dict[str, sqlite3.Row] = {}
   335	        for row in rows:
   336	            codigo = str(row["codigo_opcao"]).strip().upper()
   337	            if codigo and codigo not in quote_by_codigo:
   338	                quote_by_codigo[codigo] = row
   339	
   340	        enriched: list[LegMarketSnapshot] = []
   341	        for base_leg in base_legs:
   342	            codigo = str(base_leg.ativo).strip().upper() if base_leg.ativo else ""
   343	            quote_row = quote_by_codigo.get(codigo)
   344	            if quote_row is not None:
   345	                enriched.append(_row_to_rtd_option_quote_leg(base_leg, quote_row))
   346	
   347	        return enriched
   348	
   349	    def get_rtd_summary(self, ref: StructureRef | str) -> Optional[dict]:
   350	        aba = _ref_to_aba(ref)
   351	        with self._connect() as conn:
   352	            row = conn.execute(_SQL_RTD_SUMMARY, (aba,)).fetchone()
   353	        if row is None:
   354	            return None
   355	        return dict(row)
   356	
   357	    # -- Manual ---------------------------------------------------------------
   358	
   359	    def get_manual_legs(self, ref: StructureRef | str) -> list[LegMarketSnapshot]:
   360	        aba = _ref_to_aba(ref)
   361	        with self._connect() as conn:
   362	            rows = conn.execute(_SQL_MANUAL_LEGS, (aba,)).fetchall()
   363	        return [_row_to_leg(r, SnapshotSource.MANUAL) for r in rows]
   364	
   365	    # -- Estrutura completa ---------------------------------------------------
   366	
   367	    def get_structure(
   368	        self,
   369	        ref: StructureRef | str,
   370	        source: SnapshotSource = SnapshotSource.RTD,
   371	    ) -> StructureMarketSnapshot:
   372	        aba = _ref_to_aba(ref)
   373	
   374	        if source == SnapshotSource.RTD:
   375	            legs = self.get_rtd_legs(ref)
   376	            summary = self.get_rtd_summary(ref)
   377	        else:
   378	            legs = self.get_manual_legs(ref)
   379	            summary = None
   380	
   381	        def _f(key: str) -> Optional[float]:
   382	            return (
   383	                _parse_br_float(summary[key])
   384	                if summary and summary.get(key) is not None
   385	                else None
   386	            )
   387	
   388	        return StructureMarketSnapshot(
   389	            aba=aba,
   390	            legs=legs,
   391	            source=source,
   392	            spot=_f("spot"),
   393	            num_pernas=int(_f("num_pernas")) if _f("num_pernas") is not None else None,
   394	            dte_min=int(_f("dte_min")) if _f("dte_min") is not None else None,
   395	            pl_realista_total=_f("pl_realista_total"),
   396	            delta_liq=_f("delta_liq"),
   397	            gamma_liq=_f("gamma_liq"),
   398	            theta_liq=_f("theta_liq"),
   399	            vega_liq=_f("vega_liq"),
   400	            spread_medio=_f("spread_medio"),
   401	            spread_pct_medio=_f("spread_pct_medio"),
   402	            alertas_v2=summary.get("alertas_v2") if summary else None,
   403	        )
```

## FILE: repositories/robo_legs_repository.py
```python
     1	# repositories/robo_legs_repository.py
     2	"""
     3	alteracao_40 -- métodos canônicos por structure_id adicionados
     4	alteracao_62 -- _resolve_aba_from_structure_id movido para AbaResolverMixin
     5	             (elimina duplicação com robo_legs_status_repository)
     6	"""
     7	from __future__ import annotations
     8	
     9	from dataclasses import dataclass
    10	from datetime import datetime
    11	from typing import Any, Dict, List, Optional
    12	
    13	from domain.position_side import normalize_position_side
    14	from dto.robo_leg_dto import FonteType, RoboLegDTO
    15	from infra.sqlite_conn import sqlite_conn
    16	from repositories._aba_resolver_mixin import AbaResolverMixin
    17	from src.domain.refs.structure_ref import StructureRef
    18	from utils.leg_normalizers import parse_timestamp, parse_vencimento
    19	
    20	
    21	def _to_aba(ref) -> str:
    22	    """Aceita StructureRef ou str e devolve a string da aba."""
    23	    if isinstance(ref, str):
    24	        return ref
    25	    return ref.aba  # StructureRef.aba (alteracao_53)
    26	
    27	
    28	@dataclass(frozen=True)
    29	class RoboLegsRepoConfig:
    30	    app_db_path: str = "./dados/app.db"
    31	
    32	
    33	class RoboLegsRepository(AbaResolverMixin):
    34	    """
    35	    Leitura canônica por (aba, timestamp) com regra:
    36	      manual_analise_robo_legs > rtd_analise_robo_legs
    37	
    38	    Observação importante:
    39	    O banco legado pode armazenar timestamp como texto em formatos diferentes,
    40	    principalmente:
    41	    - ISO: YYYY-MM-DD HH:MM:SS
    42	    - BR : DD/MM/YYYY HH:MM:SS
    43	
    44	    Portanto a leitura precisa ser tolerante a ambas as representações.
    45	
    46	    alteracao_62: herda AbaResolverMixin -- _resolve_aba_from_structure_id
    47	              não é mais definido localmente.
    48	    """
    49	
    50	    def __init__(self, config: Optional[RoboLegsRepoConfig] = None):
    51	        self.config = config or RoboLegsRepoConfig()
    52	
    53	    def get_legs(self, ref: StructureRef, timestamp: Any) -> List[RoboLegDTO]:
    54	        """
    55	        Retorna legs para uma aba e um timestamp exatos.
    56	        - Primeiro tenta MANUAL
    57	        - Se vazio, tenta RTD
    58	        """
    59	        aba = _to_aba(ref)
    60	        ts = parse_timestamp(timestamp)
    61	        ts_candidates = self._timestamp_candidates(timestamp, ts)
    62	
    63	        manual = self._query_legs(
    64	            table="manual_analise_robo_legs",
    65	            aba=aba,
    66	            ts_candidates=ts_candidates,
    67	            fonte=FonteType.MANUAL,
    68	        )
    69	        if manual:
    70	            return manual
    71	
    72	        rtd = self._query_legs(
    73	            table="rtd_analise_robo_legs",
    74	            aba=aba,
    75	            ts_candidates=ts_candidates,
    76	            fonte=FonteType.RTD,
    77	        )
    78	        return rtd
    79	
    80	    def has_manual(self, ref: StructureRef, timestamp: Any) -> bool:
    81	        aba = _to_aba(ref)
    82	        ts = parse_timestamp(timestamp)
    83	        ts_candidates = self._timestamp_candidates(timestamp, ts)
    84	
    85	        placeholders = ",".join("?" for _ in ts_candidates)
    86	        sql = f"""
    87	            SELECT 1
    88	            FROM manual_analise_robo_legs
    89	            WHERE aba = ?
    90	              AND timestamp IN ({placeholders})
    91	            LIMIT 1
    92	        """
    93	
    94	        with sqlite_conn(self.config.app_db_path) as conn:
    95	            cur = conn.execute(sql, (aba, *ts_candidates))
    96	            return cur.fetchone() is not None
    97	
    98	    def list_timestamps(
    99	        self,
   100	        ref: StructureRef,
   101	        prefer: str = "manual_then_rtd",
   102	    ) -> List[str]:
   103	        """Lista timestamps disponíveis para a aba."""
   104	        aba = _to_aba(ref)
   105	        prefer = (prefer or "").strip().lower()
   106	        with sqlite_conn(self.config.app_db_path) as conn:
   107	            if prefer == "all":
   108	                rows = conn.execute(
   109	                    """
   110	                    SELECT timestamp FROM manual_analise_robo_legs WHERE aba = ?
   111	                    UNION
   112	                    SELECT timestamp FROM rtd_analise_robo_legs WHERE aba = ?
   113	                    ORDER BY timestamp
   114	                    """,
   115	                    (aba, aba),
   116	                ).fetchall()
   117	                return [r["timestamp"] for r in rows]
   118	
   119	            rows_m = conn.execute(
   120	                "SELECT DISTINCT timestamp FROM manual_analise_robo_legs "
   121	                "WHERE aba = ? ORDER BY timestamp",
   122	                (aba,),
   123	            ).fetchall()
   124	            if rows_m:
   125	                return [r["timestamp"] for r in rows_m]
   126	
   127	            rows_r = conn.execute(
   128	                "SELECT DISTINCT timestamp FROM rtd_analise_robo_legs "
   129	                "WHERE aba = ? ORDER BY timestamp",
   130	                (aba,),
   131	            ).fetchall()
   132	            return [r["timestamp"] for r in rows_r]
   133	
   134	    def _query_legs(
   135	        self,
   136	        table: str,
   137	        aba: str,
   138	        ts_candidates: List[str],
   139	        fonte: FonteType,
   140	    ) -> List[RoboLegDTO]:
   141	        placeholders = ",".join("?" for _ in ts_candidates)
   142	        sql = f"""
   143	            SELECT *
   144	            FROM {table}
   145	            WHERE aba = ?
   146	              AND timestamp IN ({placeholders})
   147	        """
   148	
   149	        with sqlite_conn(self.config.app_db_path) as conn:
   150	            rows = conn.execute(sql, (aba, *ts_candidates)).fetchall()
   151	
   152	        out: List[RoboLegDTO] = []
   153	        for r in rows:
   154	            data = dict(r)
   155	            out.append(self._row_to_dto(data, fonte=fonte))
   156	        return out
   157	
   158	    def _row_to_dto(self, row: Dict[str, Any], fonte: FonteType) -> RoboLegDTO:
   159	        """Mapeia colunas -> DTO com normalização simples."""
   160	
   161	        def pick(*keys: str, default=None):
   162	            for k in keys:
   163	                if k in row and row[k] is not None:
   164	                    return row[k]
   165	            return default
   166	
   167	        aba       = pick("aba")
   168	        timestamp = pick("timestamp")
   169	        cv        = pick("cv", "lado", "c_v")
   170	        call_put  = pick("call_put", "cp", "tipo", "callput")
   171	        strike    = pick("strike", "k", "preco_exercicio")
   172	        quant     = pick("quant", "qty", "qtd", "quantidade")
   173	        ativo     = pick("ativo", "ticker", "cod_ativo")
   174	        venc      = pick("vencimento", "vcto", "expiry", "expiracao")
   175	        preco     = pick("preco", "price", "premium")
   176	        leg_id    = pick("id", "leg_id")
   177	
   178	        cv_raw  = str(cv).upper().strip()       if cv        is not None else ""
   179	        cp_raw  = str(call_put).upper().strip() if call_put  is not None else ""
   180	
   181	        canonical_side = normalize_position_side(cv_raw)
   182	        cv_norm       = "C" if canonical_side == "COMPRADO" else "V"
   183	        call_put_norm = "CALL" if cp_raw in ["CALL", "C"] else "PUT"
   184	
   185	        return RoboLegDTO(
   186	            aba=str(aba).strip(),
   187	            timestamp=parse_timestamp(timestamp),
   188	            cv=cv_norm,
   189	            call_put=call_put_norm,
   190	            strike=float(strike)       if strike  is not None else 0.0,
   191	            quant=int(quant)           if quant   is not None else 0,
   192	            ativo=str(ativo).strip().upper() if ativo is not None else "",
   193	            vencimento=parse_vencimento(venc) if venc is not None else None,
   194	            fonte=fonte,
   195	            id=int(leg_id)             if leg_id  is not None else None,
   196	            preco=float(preco)         if preco   is not None else None,
   197	            created_at=None,
   198	            updated_at=None,
   199	        )
   200	
   201	    @staticmethod
   202	    def _timestamp_candidates(original: Any, ts: datetime) -> List[str]:
   203	        """
   204	        Gera representações aceitas para comparar com o banco legado.
   205	        Ordem:
   206	        1. valor original (se string)
   207	        2. ISO datetime
   208	        3. BR datetime
   209	        4. ISO date
   210	        5. BR date
   211	        """
   212	        candidates: List[str] = []
   213	
   214	        if isinstance(original, str):
   215	            raw = original.strip()
   216	            if raw:
   217	                candidates.append(raw)
   218	
   219	        iso_dt = ts.replace(microsecond=0).isoformat(sep=" ")
   220	        br_dt  = ts.strftime("%d/%m/%Y %H:%M:%S")
   221	        iso_d  = ts.strftime("%Y-%m-%d")
   222	        br_d   = ts.strftime("%d/%m/%Y")
   223	
   224	        for v in [iso_dt, br_dt, iso_d, br_d]:
   225	            if v not in candidates:
   226	                candidates.append(v)
   227	
   228	        return candidates
   229	
   230	    # ------------------------------------------------------------------ #
   231	    # alteracao_40: métodos canônicos por structure_id                        #
   232	    # alteracao_62: _resolve_aba_from_structure_id herdado de AbaResolverMixin#
   233	    # ------------------------------------------------------------------ #
   234	
   235	    def get_legs_by_structure_id(
   236	        self,
   237	        structure_id: int,
   238	        timestamp: Any,
   239	    ) -> List[RoboLegDTO]:
   240	        """
   241	        Ponto de entrada canônico: recebe structure_id, resolve para aba,
   242	        delega para get_legs() existente.
   243	        Levanta ValueError se structure_id não mapeado.
   244	        """
   245	        aba = self._resolve_aba_from_structure_id(structure_id)
   246	        if aba is None:
   247	            raise ValueError(
   248	                f"structure_id={structure_id} sem alias_legacy_aba em structures"
   249	            )
   250	        # alteracao_62: passa StructureRef em vez de str nua -- semântica explícita
   251	        ref = StructureRef(aba=aba, structure_id=structure_id)
   252	        return self.get_legs(ref=ref, timestamp=timestamp)
   253	
   254	    def has_manual_by_structure_id(
   255	        self,
   256	        structure_id: int,
   257	        timestamp: Any,
   258	    ) -> bool:
   259	        """Versão canônica de has_manual() por structure_id."""
   260	        aba = self._resolve_aba_from_structure_id(structure_id)
   261	        if aba is None:
   262	            return False
   263	        return self.has_manual(
   264	            ref=StructureRef(aba=aba, structure_id=structure_id),
   265	            timestamp=timestamp,
   266	        )
   267	
   268	    def list_timestamps_by_structure_id(
   269	        self,
   270	        structure_id: int,
   271	        prefer: str = "manual_then_rtd",
   272	    ) -> List[str]:
   273	        """Versão canônica de list_timestamps() por structure_id."""
   274	        aba = self._resolve_aba_from_structure_id(structure_id)
   275	        if aba is None:
   276	            raise ValueError(
   277	                f"structure_id={structure_id} sem alias_legacy_aba em structures"
   278	            )
   279	        return self.list_timestamps(
   280	            ref=StructureRef(aba=aba, structure_id=structure_id),
   281	            prefer=prefer,
   282	        )
```

## FILE: services/structure_leg_rtd_enrichment_service.py
```python
     1	"""Service de enriquecimento de legs de estruturas via RTD.
     2	
     3	Objetivo:
     4	- receber entrada minima baseada em simbolo/codigo da opcao;
     5	- consultar rtd_option_quotes por codigo_opcao;
     6	- devolver payload canonico de leg para o repository de structures;
     7	- validar divergencia entre tipo informado e tipo detectado.
     8	"""
     9	
    10	from __future__ import annotations
    11	
    12	from typing import Any
    13	
    14	from domain.position_side import normalize_position_side
    15	
    16	
    17	class StructureLegRtdEnrichmentService:
    18	    """Enriquece uma leg de estrutura usando dados de rtd_option_quotes."""
    19	
    20	    def __init__(self, rtd_option_quotes_repository: Any) -> None:
    21	        self._repo = rtd_option_quotes_repository
    22	
    23	    def enrich(self, leg_data: dict[str, Any]) -> dict[str, Any]:
    24	        """Retorna uma leg canonica enriquecida a partir do simbolo da opcao.
    25	
    26	        Entrada minima esperada:
    27	        - symbol ou codigo_opcao;
    28	        - position_side;
    29	        - quantity.
    30	
    31	        Campos enriquecidos via RTD:
    32	        - underlying_asset;
    33	        - option_type;
    34	        - strike;
    35	        - expiration_date.
    36	        """
    37	
    38	        symbol = self._normalize_symbol(
    39	            leg_data.get("symbol") or leg_data.get("codigo_opcao")
    40	        )
    41	        if not symbol:
    42	            raise ValueError("symbol is required for RTD leg enrichment")
    43	
    44	        quote = self._repo.get_by_codigo(symbol)
    45	        if quote is None:
    46	            raise ValueError(f"option quote not found for symbol: {symbol}")
    47	
    48	        self._ensure_required_quote_fields(
    49	            quote,
    50	            required=("ativo_base", "call_put", "strike", "vencimento"),
    51	        )
    52	
    53	        detected_option_type = self._normalize_option_type(quote.get("call_put"))
    54	
    55	        informed_option_type_raw = leg_data.get("option_type")
    56	        if informed_option_type_raw not in (None, ""):
    57	            informed_option_type = self._normalize_option_type(informed_option_type_raw)
    58	            if informed_option_type != detected_option_type:
    59	                raise ValueError(
    60	                    "option_type divergente do símbolo informado: "
    61	                    f"informado={informed_option_type}, "
    62	                    f"detectado={detected_option_type}, "
    63	                    f"symbol={symbol}"
    64	                )
    65	
    66	        return {
    67	            "symbol": symbol,
    68	            "position_side": normalize_position_side(leg_data.get("position_side")),
    69	            "option_type": detected_option_type,
    70	            "strike": self._to_float(quote.get("strike"), "strike"),
    71	            "expiration_date": str(quote.get("vencimento")).strip(),
    72	            "quantity": self._to_int(leg_data.get("quantity", 1), "quantity"),
    73	            "premium": self._to_optional_float(leg_data.get("premium"), "premium"),
    74	            "multiplier": self._to_float(
    75	                leg_data.get("multiplier", 1.0),
    76	                "multiplier",
    77	            ),
    78	            "leg_order": self._to_int(leg_data.get("leg_order", 1), "leg_order"),
    79	            "notes": leg_data.get("notes"),
    80	            "underlying_asset": self._normalize_required_text(
    81	                quote.get("ativo_base"),
    82	                "ativo_base",
    83	            ),
    84	        }
    85	
    86	    @staticmethod
    87	    def _normalize_symbol(value: Any) -> str:
    88	        if value is None:
    89	            return ""
    90	        return str(value).strip().upper()
    91	
    92	    @staticmethod
    93	    def _normalize_required_text(value: Any, field_name: str) -> str:
    94	        if value is None:
    95	            raise ValueError(f"{field_name} is required")
    96	        normalized = str(value).strip().upper()
    97	        if not normalized:
    98	            raise ValueError(f"{field_name} is required")
    99	        return normalized
   100	
   101	    @classmethod
   102	    def _normalize_option_type(cls, value: Any) -> str:
   103	        text = cls._normalize_required_text(value, "option_type")
   104	        mapping = {
   105	            "C": "CALL",
   106	            "CALL": "CALL",
   107	            "COMPRA": "CALL",
   108	            "P": "PUT",
   109	            "PUT": "PUT",
   110	            "VENDA": "PUT",
   111	        }
   112	        normalized = mapping.get(text)
   113	        if normalized is None:
   114	            raise ValueError(f"invalid option_type/call_put: {value!r}")
   115	        return normalized
   116	
   117	    @staticmethod
   118	    def _to_float(value: Any, field_name: str) -> float:
   119	        if value is None or str(value).strip() == "":
   120	            raise ValueError(f"{field_name} is required")
   121	
   122	        text = str(value).strip()
   123	        if "," in text and "." in text:
   124	            text = text.replace(".", "").replace(",", ".")
   125	        else:
   126	            text = text.replace(",", ".")
   127	
   128	        try:
   129	            return float(text)
   130	        except (TypeError, ValueError) as exc:
   131	            raise ValueError(f"{field_name} must be numeric") from exc
   132	
   133	    @classmethod
   134	    def _to_optional_float(cls, value: Any, field_name: str) -> float | None:
   135	        if value is None or str(value).strip() == "":
   136	            return None
   137	        return cls._to_float(value, field_name)
   138	
   139	    @classmethod
   140	    def _to_int(cls, value: Any, field_name: str) -> int:
   141	        number = cls._to_float(value, field_name)
   142	        if int(number) != number:
   143	            raise ValueError(f"{field_name} must be integer")
   144	        return int(number)
   145	
   146	    @staticmethod
   147	    def _ensure_required_quote_fields(
   148	        quote: dict[str, Any],
   149	        required: tuple[str, ...],
   150	    ) -> None:
   151	        for field in required:
   152	            value = quote.get(field)
   153	            if value is None or str(value).strip() == "":
   154	                raise ValueError(f"missing required RTD field: {field}")
```

## FILE: services/structure_market_input_assembler.py
```python
     1	from typing import Any
     2	
     3	from services.structure_input_mapper import to_structure_input
     4	
     5	
     6	def assemble_structure_market_input(
     7	    structure: dict[str, Any],
     8	    market_snapshot: dict[str, Any],
     9	) -> dict[str, Any]:
    10	    if not structure:
    11	        raise ValueError("structure is required")
    12	
    13	    if not market_snapshot:
    14	        raise ValueError("market_snapshot is required")
    15	
    16	    structure_input = to_structure_input(structure)
    17	    structure_asset = structure_input["underlying_asset"]
    18	    market_asset = market_snapshot.get("underlying_asset")
    19	
    20	    if structure_asset != market_asset:
    21	        raise ValueError(
    22	            f"underlying_asset mismatch: structure={structure_asset} market={market_asset}"
    23	        )
    24	
    25	    return {
    26	        "structure": structure_input,
    27	        "market": {
    28	            "reference_date": market_snapshot["reference_date"],
    29	            "underlying_asset": market_snapshot["underlying_asset"],
    30	            "spot_price": market_snapshot["spot_price"],
    31	            "interest_rate": market_snapshot["interest_rate"],
    32	            "volatility": market_snapshot["volatility"],
    33	        },
    34	        "meta": {
    35	            "input_source": "structure_market_input_assembler",
    36	        },
    37	    }
```

## FILE: services/structure_input_mapper.py
```python
     1	from typing import Any
     2	
     3	from domain.position_side import normalize_position_side
     4	
     5	
     6	def _clean_text(value: Any) -> str | None:
     7	    if value is None:
     8	        return None
     9	    text = str(value).strip()
    10	    return text or None
    11	
    12	
    13	def _clean_upper_text(value: Any) -> str | None:
    14	    text = _clean_text(value)
    15	    return text.upper() if text is not None else None
    16	
    17	
    18	def _to_float_or_none(value: Any) -> float | None:
    19	    if value is None:
    20	        return None
    21	
    22	    try:
    23	        return float(value)
    24	    except (TypeError, ValueError):
    25	        return None
    26	
    27	
    28	def _enrich_bid_ask_derived_fields(mapped_leg: dict[str, Any]) -> None:
    29	    bid = _to_float_or_none(mapped_leg.get("bid"))
    30	    ask = _to_float_or_none(mapped_leg.get("ask"))
    31	
    32	    if bid is None or ask is None:
    33	        return
    34	
    35	    spread = ask - bid
    36	    mid = (bid + ask) / 2
    37	
    38	    if "spread" not in mapped_leg or mapped_leg.get("spread") is None:
    39	        mapped_leg["spread"] = spread
    40	
    41	    if "mid" not in mapped_leg or mapped_leg.get("mid") is None:
    42	        mapped_leg["mid"] = mid
    43	
    44	    if (
    45	        ("spread_pct" not in mapped_leg or mapped_leg.get("spread_pct") is None)
    46	        and mid
    47	    ):
    48	        mapped_leg["spread_pct"] = spread / mid
    49	
    50	
    51	def _map_leg_to_structure_input(leg: dict[str, Any]) -> dict[str, Any]:
    52	    mapped_leg = {
    53	        "position_side": normalize_position_side(leg["position_side"]),
    54	        "option_type": _clean_upper_text(leg["option_type"]),
    55	        "symbol": _clean_upper_text(leg.get("symbol")),
    56	        "strike": leg["strike"],
    57	        "expiration_date": _clean_text(leg["expiration_date"]),
    58	        "quantity": leg["quantity"],
    59	        "premium": leg.get("premium"),
    60	        "multiplier": leg.get("multiplier", 1.0),
    61	    }
    62	
    63	    optional_market_fields = (
    64	        "bid",
    65	        "ask",
    66	        "mid",
    67	        "spread",
    68	        "spread_pct",
    69	        "iv",
    70	        "delta",
    71	        "gamma",
    72	        "theta",
    73	        "vega",
    74	    )
    75	
    76	    for field in optional_market_fields:
    77	        if field in leg:
    78	            mapped_leg[field] = leg[field]
    79	
    80	    _enrich_bid_ask_derived_fields(mapped_leg)
    81	
    82	    return mapped_leg
    83	
    84	
    85	def to_structure_input(structure: dict[str, Any]) -> dict[str, Any]:
    86	    if not structure:
    87	        raise ValueError("structure is required")
    88	
    89	    legs = structure.get("legs", [])
    90	
    91	    return {
    92	        "structure_id": structure["id"],
    93	        "name": _clean_text(structure["name"]),
    94	        "underlying_asset": _clean_upper_text(structure["underlying_asset"]),
    95	        "legs": [
    96	            _map_leg_to_structure_input(leg)
    97	            for leg in legs
    98	        ],
    99	    }
```

## FILE: services/structure_analysis_service.py
```python
     1	# services/structure_analysis_service.py
     2	from __future__ import annotations
     3	
     4	from typing import Any, Dict, Optional
     5	
     6	from domain.decision import compute_decision_from_payoff
     7	from domain.payoff import compute_payoff_from_canonical_input
     8	from domain.structure_metrics import (
     9	    compute_dte_min_from_canonical_input,
    10	    compute_structure_metrics_from_canonical_input,
    11	)
    12	
    13	
    14	class StructureAnalysisService:
    15	    def __init__(self, canonical_input_service):
    16	        self._canonical_input_service = canonical_input_service
    17	
    18	    def analyze(
    19	        self,
    20	        structure_id: int,
    21	        reference_date: Optional[str] = None,
    22	        dte_min: Optional[int] = None,
    23	        spread_pct_medio: Optional[float] = None,
    24	        thresholds: Optional[Dict[str, float]] = None,
    25	        dte_gate: int = 7,
    26	    ) -> Dict[str, Any]:
    27	
    28	        # 1. Busca input canônico
    29	        canonical_input = self._canonical_input_service.build_structure_market_input(
    30	            structure_id=structure_id,
    31	            reference_date=reference_date,
    32	        )
    33	
    34	        # 2. Calcula métricas internas da estrutura
    35	        structure_metrics = compute_structure_metrics_from_canonical_input(canonical_input)
    36	
    37	        # 3. Calcula DTE inferido preservando o contrato legado
    38	        #
    39	        # Mantemos compute_dte_min_from_canonical_input como fonte explícita do
    40	        # dte_min_inferred para compatibilidade com testes e integrações já
    41	        # existentes. O motor novo também calcula dte_min, mas nesta etapa ele é
    42	        # exposto dentro de structure_metrics.
    43	        dte_min_inferred = compute_dte_min_from_canonical_input(canonical_input)
    44	
    45	        # 4. DTE efetivo: explícito > inferido > 0
    46	        if dte_min is not None:
    47	            dte_min_effective = dte_min
    48	        elif dte_min_inferred is not None:
    49	            dte_min_effective = dte_min_inferred
    50	        else:
    51	            dte_min_effective = 0
    52	
    53	        # 5. Spread efetivo: explícito > calculado internamente
    54	        spread_pct_medio_inferred = structure_metrics.get("spread_pct_medio")
    55	
    56	        if spread_pct_medio is not None:
    57	            spread_pct_medio_effective = spread_pct_medio
    58	        else:
    59	            spread_pct_medio_effective = spread_pct_medio_inferred
    60	
    61	        # 6. Calcula payoff
    62	        payoff = compute_payoff_from_canonical_input(canonical_input)
    63	
    64	        # 7. Valida payoff -- se inválido, retorna HOLD com erro estruturado
    65	        if not payoff or not payoff.get("pl_max"):
    66	            why_dict = {
    67	                "error": "payoff is required",
    68	                "validation_errors": ["pl_max ausente ou zero"],
    69	                "reasons": ["invalid_payoff"],
    70	                "alternatives": [],
    71	            }
    72	            decision = {
    73	                "decision":      "HOLD",
    74	                "level":         0,
    75	                "ratio":         0.0,
    76	                "pl_pct_of_max": 0.0,
    77	                "dte_min":       dte_min_effective,
    78	                "why":           why_dict,
    79	                "why_json":      "{}",
    80	                "alternatives":  [],
    81	            }
    82	            return {
    83	                "canonical_input": canonical_input,
    84	                "metrics": {
    85	                    "dte_min_inferred":             dte_min_inferred,
    86	                    "dte_min_effective":            dte_min_effective,
    87	                    "spread_pct_medio":             spread_pct_medio_effective,
    88	                    "spread_pct_medio_inferred":    spread_pct_medio_inferred,
    89	                    "structure_metrics":            structure_metrics,
    90	                },
    91	                "payoff":   payoff,
    92	                "decision": decision,
    93	            }
    94	
    95	        # 8. Computa decisão -- passa TODOS os parâmetros como keyword
    96	        decision = compute_decision_from_payoff(
    97	            payoff=payoff,
    98	            dte_min=dte_min_effective,
    99	            spread_pct_medio=spread_pct_medio_effective,
   100	            thresholds=thresholds,
   101	            dte_gate=dte_gate,
   102	        )
   103	
   104	        # 9. Injeta dte_min no retorno (esperado pelos testes)
   105	        decision["dte_min"] = dte_min_effective
   106	
   107	        # 10. Injeta dte_gate em why (esperado por test_propagates_custom_thresholds_and_dte_gate)
   108	        decision["why"]["dte_gate"] = dte_gate
   109	
   110	        return {
   111	            "canonical_input": canonical_input,
   112	            "metrics": {
   113	                "dte_min_inferred":             dte_min_inferred,
   114	                "dte_min_effective":            dte_min_effective,
   115	                "spread_pct_medio":             spread_pct_medio_effective,
   116	                "spread_pct_medio_inferred":    spread_pct_medio_inferred,
   117	                "structure_metrics":            structure_metrics,
   118	            },
   119	            "payoff":   payoff,
   120	            "decision": decision,
   121	        }
```

## FILE: services/calculation_orchestrator.py
```python
     1	# services/calculation_orchestrator.py
     2	# alteracao_45: CalculationRequest contract + build_calculation_request
     3	# alteracao_46: _request_to_payoff_dict, run_payoff, run_decision
     4	# alteracao_47: run_full_pipeline, multiplier fix (1.0), run_decision auto-extract
     5	# alteracao_48: CalculationOrchestrator class, build_calculation_request_from_db,
     6	#           run_full_pipeline_from_db
     7	
     8	from __future__ import annotations
     9	
    10	import logging
    11	from types import SimpleNamespace
    12	from typing import Optional, Dict, Any, List
    13	
    14	from domain.calculation_request import (
    15	    CalculationRequest,
    16	    MarketSnapshotInput,
    17	    StructureInput,
    18	    StructureLegInput,
    19	)
    20	from domain.payoff import compute_payoff_from_canonical_input
    21	from domain.decision import compute_decision_from_contract
    22	from domain.position_side import to_pricing_engine_side
    23	
    24	logger = logging.getLogger(__name__)
    25	
    26	# ---------------------------------------------------------------------------
    27	# Mapeamento legado -> contrato tecnico de calculo
    28	# ---------------------------------------------------------------------------
    29	_CP_NORM = {"CALL": "CALL", "PUT": "PUT", "C": "CALL", "P": "PUT"}
    30	
    31	
    32	def _normalize_position_side(raw: str) -> str:
    33	    try:
    34	        return to_pricing_engine_side(raw)
    35	    except ValueError as exc:
    36	        raise ValueError(f"position_side desconhecido: {raw!r}") from exc
    37	
    38	
    39	def _normalize_option_type(raw: str) -> str:
    40	    v = str(raw).strip().upper()
    41	    if v not in _CP_NORM:
    42	        raise ValueError(f"option_type desconhecido: {raw!r}")
    43	    return _CP_NORM[v]
    44	
    45	
    46	# ---------------------------------------------------------------------------
    47	# Funcao legada build_calculation_request (alteracao_45 -- mantida para
    48	# retrocompatibilidade com testes anteriores)
    49	# ---------------------------------------------------------------------------
    50	def build_calculation_request(
    51	    structure_row: dict,
    52	    legs_rows: list,
    53	    snapshot_row: dict,
    54	) -> CalculationRequest:
    55	    """
    56	    Monta um CalculationRequest a partir de dicts vindos do repositorio.
    57	    Mantida para retrocompatibilidade (alteracao_45).
    58	    """
    59	    if not isinstance(legs_rows, list) or len(legs_rows) == 0:
    60	        raise ValueError("legs_rows nao pode ser vazio")
    61	
    62	    legs = []
    63	    for i, row in enumerate(legs_rows):
    64	        try:
    65	            leg = StructureLegInput(
    66	                position_side=_normalize_position_side(
    67	                    row.get("position_side") or row.get("cv", "")
    68	                ),
    69	                option_type=_normalize_option_type(
    70	                    row.get("option_type") or row.get("call_put", "")
    71	                ),
    72	                strike=float(row["strike"]),
    73	                expiration_date=str(row["expiration_date"]),
    74	                quantity=int(row["quantity"]),
    75	                symbol=row.get("symbol"),
    76	                premium=float(row["premium"]) if row.get("premium") is not None else None,
    77	                multiplier=float(row.get("multiplier") or 1.0),
    78	                leg_order=int(row.get("leg_order") or i),
    79	                notes=row.get("notes"),
    80	            )
    81	        except (KeyError, TypeError, ValueError) as exc:
    82	            raise ValueError(f"Erro ao montar leg[{i}]: {exc}") from exc
    83	        legs.append(leg)
    84	
    85	    structure = StructureInput(
    86	        structure_id=int(structure_row["id"]),
    87	        underlying_asset=str(structure_row["underlying_asset"]),
    88	        legs=legs,
    89	        name=structure_row.get("name"),
    90	        alias_legacy_aba=structure_row.get("alias_legacy_aba"),
    91	    )
    92	
    93	    snapshot = MarketSnapshotInput(
    94	        snapshot_timestamp=str(snapshot_row["snapshot_timestamp"]),
    95	        underlying_asset=str(snapshot_row["underlying_asset"]),
    96	        spot_price=float(snapshot_row["spot_price"]),
    97	        source=str(snapshot_row.get("source", "rtd")),
    98	        snapshot_id=snapshot_row.get("snapshot_id") or snapshot_row.get("id"),
    99	        option_quotes=snapshot_row.get("option_quotes"),
   100	        greeks=snapshot_row.get("greeks"),
   101	        volatility_context=snapshot_row.get("volatility_context"),
   102	    )
   103	
   104	    return CalculationRequest(structure=structure, market_snapshot=snapshot)
   105	
   106	
   107	# ---------------------------------------------------------------------------
   108	# Funcoes legadas de pipeline (alteracao_46/47 -- mantidas para
   109	# retrocompatibilidade com testes anteriores)
   110	# ---------------------------------------------------------------------------
   111	def _request_to_payoff_dict(
   112	    request: CalculationRequest,
   113	    extra_meta: Optional[dict] = None,
   114	) -> dict:
   115	    """alteracao_47: multiplier usa leg.multiplier com fallback 1.0."""
   116	    legs = []
   117	    for leg in request.structure.legs:
   118	        legs.append({
   119	            "position_side":   leg.position_side,
   120	            "option_type":     leg.option_type,
   121	            "strike":          leg.strike,
   122	            "expiration_date": leg.expiration_date,
   123	            "quantity":        leg.quantity,
   124	            "symbol":          getattr(leg, "symbol",      None),
   125	            "premium":         getattr(leg, "premium",     None),
   126	            "multiplier":      getattr(leg, "multiplier",  1.0),
   127	            "leg_order":       getattr(leg, "leg_order",   0),
   128	            "notes":           getattr(leg, "notes",       None),
   129	        })
   130	
   131	    return {
   132	        "structure": {
   133	            "structure_id":     request.structure.structure_id,
   134	            "underlying_asset": request.structure.underlying_asset,
   135	            "name":             getattr(request.structure, "name", None),
   136	            "legs":             legs,
   137	        },
   138	        "market": {
   139	            "spot_price":       request.market_snapshot.spot_price,
   140	            "underlying_asset": request.market_snapshot.underlying_asset,
   141	            "reference_date":   getattr(request.market_snapshot, "snapshot_timestamp", None),
   142	            "option_quotes":    getattr(request.market_snapshot, "option_quotes",      {}),
   143	            "greeks":           getattr(request.market_snapshot, "greeks",             {}),
   144	        },
   145	        "meta": extra_meta or {},
   146	    }
   147	
   148	
   149	def run_payoff(
   150	    request: CalculationRequest,
   151	    low_pct: float = 0.5,
   152	    high_pct: float = 1.5,
   153	    step_pct: float = 0.01,
   154	    extra_meta: Optional[dict] = None,
   155	) -> dict:
   156	    """Executa calculo de payoff a partir de um CalculationRequest."""
   157	    canonical = _request_to_payoff_dict(request, extra_meta=extra_meta)
   158	    return compute_payoff_from_canonical_input(
   159	        canonical,
   160	        low_pct=low_pct,
   161	        high_pct=high_pct,
   162	        step_pct=step_pct,
   163	    )
   164	
   165	
   166	def run_decision(
   167	    request: CalculationRequest,
   168	    payoff: Optional[dict] = None,
   169	    pl_atual: Optional[float] = None,
   170	    pl_max: Optional[float] = None,
   171	    dte_min: Optional[int] = None,
   172	) -> dict:
   173	    """alteracao_47: extrai pl_max/pl_atual/dte_min automaticamente."""
   174	    _pl_max = pl_max
   175	    if _pl_max is None and payoff:
   176	        _pl_max = float(payoff.get("pl_max") or 0.0)
   177	    if _pl_max is None:
   178	        _pl_max = 0.0
   179	
   180	    _pl_atual = pl_atual
   181	    if _pl_atual is None and payoff:
   182	        _pl_atual = float(payoff.get("pl_atual") or payoff.get("pl_now") or 0.0)
   183	    if _pl_atual is None:
   184	        _pl_atual = 0.0
   185	
   186	    _dte_min = dte_min
   187	    if _dte_min is None:
   188	        _dte_min = getattr(request.market_snapshot, "dte_min", None)
   189	
   190	    contract = SimpleNamespace(
   191	        pl_max=_pl_max,
   192	        pl_atual=_pl_atual,
   193	        dte_min=_dte_min,
   194	    )
   195	    return compute_decision_from_contract(contract, payoff=payoff)
   196	
   197	
   198	def run_full_pipeline(
   199	    request: CalculationRequest,
   200	    low_pct: float = 0.5,
   201	    high_pct: float = 1.5,
   202	    step_pct: float = 0.01,
   203	    extra_meta: Optional[dict] = None,
   204	) -> dict:
   205	    """alteracao_47: pipeline completo payoff + decision."""
   206	    payoff_result = run_payoff(
   207	        request,
   208	        low_pct=low_pct,
   209	        high_pct=high_pct,
   210	        step_pct=step_pct,
   211	        extra_meta=extra_meta,
   212	    )
   213	    decision_result = run_decision(request, payoff=payoff_result)
   214	
   215	    return {
   216	        "payoff":           payoff_result,
   217	        "decision":         decision_result,
   218	        "structure_id":     request.structure.structure_id,
   219	        "underlying_asset": request.structure.underlying_asset,
   220	    }
   221	
   222	
   223	# ===========================================================================
   224	# alteracao_48 -- CalculationOrchestrator (classe canonica)
   225	# ===========================================================================
   226	
   227	class CalculationOrchestrator:
   228	    """
   229	    Orquestrador canonico de calculo.
   230	
   231	    Responsabilidades:
   232	    - Montar CalculationRequest a partir de dicts ja normalizados
   233	    - Executar payoff e decisao sem acessar raw DB diretamente
   234	    - Montar CalculationRequest a partir dos repositorios canonicos (alteracao_48)
   235	
   236	    via repositórios injetados.
   237	    """
   238	
   239	    def __init__(
   240	        self,
   241	        structures_repository=None,
   242	        market_snapshot_repository=None,
   243	    ):
   244	        self._structures_repo = structures_repository
   245	        self._snapshot_repo   = market_snapshot_repository
   246	
   247	    # ------------------------------------------------------------------
   248	    # Construcao manual do CalculationRequest
   249	    # ------------------------------------------------------------------
   250	
   251	    def build_calculation_request(
   252	        self,
   253	        structure_dict: Dict[str, Any],
   254	        market_snapshot_dict: Dict[str, Any],
   255	    ) -> CalculationRequest:
   256	        """Monta CalculationRequest a partir de dicts ja normalizados."""
   257	        legs = []
   258	        for i, leg in enumerate(structure_dict.get("legs", [])):
   259	            legs.append(
   260	                StructureLegInput(
   261	                    position_side=_normalize_position_side(
   262	                        leg.get("position_side") or leg.get("cv", "")
   263	                    ),
   264	                    option_type=_normalize_option_type(
   265	                        leg.get("option_type") or leg.get("call_put", "CALL")
   266	                    ),
   267	                    strike=float(leg["strike"]),
   268	                    expiration_date=str(leg["expiration_date"]),
   269	                    quantity=int(leg["quantity"]),
   270	                    symbol=leg.get("symbol"),
   271	                    premium=float(leg["premium"]) if leg.get("premium") is not None else None,
   272	                    multiplier=float(leg.get("multiplier") or 1.0),
   273	                    leg_order=int(leg.get("leg_order") or i),
   274	                    notes=leg.get("notes"),
   275	                )
   276	            )
   277	
   278	        structure = StructureInput(
   279	            structure_id=int(structure_dict["structure_id"]),
   280	            name=structure_dict.get("name", ""),
   281	            underlying_asset=str(structure_dict.get("underlying_asset", "")),
   282	            alias_legacy_aba=structure_dict.get("alias_legacy_aba"),
   283	            legs=legs,
   284	        )
   285	
   286	        snapshot = MarketSnapshotInput(
   287	            snapshot_id=market_snapshot_dict.get("snapshot_id"),
   288	            snapshot_timestamp=str(market_snapshot_dict.get("snapshot_timestamp", "")),
   289	            underlying_asset=str(market_snapshot_dict.get("underlying_asset", "")),
   290	            spot_price=float(market_snapshot_dict.get("spot_price", 0.0)),
   291	            source=str(market_snapshot_dict.get("source", "rtd")),
   292	            option_quotes=market_snapshot_dict.get("option_quotes"),
   293	            greeks=market_snapshot_dict.get("greeks"),
   294	            volatility_context=market_snapshot_dict.get("volatility_context"),
   295	        )
   296	
   297	        return CalculationRequest(structure=structure, market_snapshot=snapshot)
   298	
   299	    # ------------------------------------------------------------------
   300	    # Adaptacao interna
   301	    # ------------------------------------------------------------------
   302	
   303	    def _request_to_payoff_dict(self, request: CalculationRequest) -> Dict[str, Any]:
   304	        """Converte CalculationRequest para o dict de payoff."""
   305	        legs = []
   306	        for leg in request.structure.legs:
   307	            legs.append({
   308	                "position_side":   leg.position_side,
   309	                "option_type":     leg.option_type,
   310	                "strike":          leg.strike,
   311	                "expiration_date": leg.expiration_date,
   312	                "quantity":        leg.quantity,
   313	                "symbol":          getattr(leg, "symbol",     None),
   314	                "premium":         getattr(leg, "premium",    None),
   315	                "multiplier":      getattr(leg, "multiplier", 1.0),
   316	                "leg_order":       getattr(leg, "leg_order",  0),
   317	                "notes":           getattr(leg, "notes",      None),
   318	            })
   319	
   320	        return {
   321	            "structure": {
   322	                "structure_id":     request.structure.structure_id,
   323	                "underlying_asset": request.structure.underlying_asset,
   324	                "name":             getattr(request.structure, "name", None),
   325	                "legs":             legs,
   326	            },
   327	            "market": {
   328	                "spot_price":       request.market_snapshot.spot_price,
   329	                "underlying_asset": request.market_snapshot.underlying_asset,
   330	                "reference_date":   getattr(request.market_snapshot, "snapshot_timestamp", None),
   331	                "option_quotes":    getattr(request.market_snapshot, "option_quotes", {}),
   332	                "greeks":           getattr(request.market_snapshot, "greeks",        {}),
   333	            },
   334	            "meta": {},
   335	        }
   336	
   337	    # ------------------------------------------------------------------
   338	    # run_payoff / run_decision / run_full_pipeline
   339	    # ------------------------------------------------------------------
   340	
   341	    def run_payoff(
   342	        self,
   343	        request: CalculationRequest,
   344	        low_pct: float = 0.5,
   345	        high_pct: float = 1.5,
   346	        step_pct: float = 0.01,
   347	    ) -> Dict[str, Any]:
   348	        canonical = self._request_to_payoff_dict(request)
   349	        return compute_payoff_from_canonical_input(
   350	            canonical,
   351	            low_pct=low_pct,
   352	            high_pct=high_pct,
   353	            step_pct=step_pct,
   354	        )
   355	
   356	    def run_decision(
   357	        self,
   358	        request: CalculationRequest,
   359	        payoff_result: Optional[Dict[str, Any]] = None,
   360	    ) -> Dict[str, Any]:
   361	        if payoff_result is None:
   362	            payoff_result = self.run_payoff(request)
   363	
   364	        _pl_max = float(
   365	            payoff_result.get("pl_max") or payoff_result.get("max_profit") or 0.0
   366	        )
   367	        _pl_atual = float(
   368	            payoff_result.get("pl_atual")
   369	            or payoff_result.get("current_pl")
   370	            or payoff_result.get("pl_now")
   371	            or 0.0
   372	        )
   373	        _dte_min = (
   374	            payoff_result.get("dte_min")
   375	            or getattr(request.market_snapshot, "dte_min", None)
   376	            or 0
   377	        )
   378	
   379	        contract = SimpleNamespace(
   380	            pl_max=_pl_max,
   381	            pl_atual=_pl_atual,
   382	            dte_min=_dte_min,
   383	        )
   384	        return compute_decision_from_contract(contract, payoff=payoff_result)
   385	
   386	    def run_full_pipeline(
   387	        self,
   388	        request: CalculationRequest,
   389	        low_pct: float = 0.5,
   390	        high_pct: float = 1.5,
   391	        step_pct: float = 0.01,
   392	    ) -> Dict[str, Any]:
   393	        """Executa run_payoff -> run_decision em sequencia."""
   394	        payoff_result   = self.run_payoff(request, low_pct=low_pct, high_pct=high_pct, step_pct=step_pct)
   395	        decision_result = self.run_decision(request, payoff_result=payoff_result)
   396	
   397	        return {
   398	            "payoff":           payoff_result,
   399	            "decision":         decision_result,
   400	            "structure_id":     request.structure.structure_id,
   401	            "underlying_asset": request.structure.underlying_asset,
   402	        }
   403	
   404	    # ------------------------------------------------------------------
   405	    # alteracao_48 -- resolucao via repositorios canonicos
   406	    # ------------------------------------------------------------------
   407	
   408	    def build_calculation_request_from_db(
   409	        self,
   410	        structure_id: int,
   411	        snapshot_timestamp: Optional[str] = None,
   412	    ) -> CalculationRequest:
   413	        """
   414	        Monta CalculationRequest buscando dados dos repositorios canonicos.
   415	
   416	        Raises:
   417	            RuntimeError: se repositorios nao foram injetados
   418	            ValueError  : se estrutura nao encontrada, arquivada ou sem legs
   419	            ValueError  : se snapshot nao encontrado
   420	        """
   421	        if self._structures_repo is None:
   422	            raise RuntimeError(
   423	                "StructuresRepository nao foi injetado no orquestrador. "
   424	                "Passe structures_repository= no construtor."
   425	            )
   426	        if self._snapshot_repo is None:
   427	            raise RuntimeError(
   428	                "MarketSnapshotRepository nao foi injetado no orquestrador. "
   429	                "Passe market_snapshot_repository= no construtor."
   430	            )
   431	
   432	        # 1. Busca estrutura
   433	        structure = self._structures_repo.get_structure(structure_id)
   434	        if structure is None:
   435	            raise ValueError(
   436	                f"Estrutura nao encontrada: structure_id={structure_id}"
   437	            )
   438	        if structure.get("status") == "archived":
   439	            raise ValueError(
   440	                f"Estrutura arquivada nao pode ser recalculada: "
   441	                f"structure_id={structure_id}"
   442	            )
   443	
   444	        legs_raw = structure.get("legs", [])
   445	        if not legs_raw:
   446	            raise ValueError(
   447	                f"Estrutura sem legs: structure_id={structure_id}"
   448	            )
   449	
   450	        # 2. Busca snapshot
   451	        underlying = structure.get("underlying_asset", "")
   452	        snapshot = self._snapshot_repo.get_snapshot(
   453	            underlying_asset=underlying,
   454	            timestamp=snapshot_timestamp,
   455	        )
   456	        if snapshot is None:
   457	            raise ValueError(
   458	                f"Snapshot nao encontrado para underlying_asset='{underlying}' "
   459	                f"timestamp={snapshot_timestamp!r}"
   460	            )
   461	
   462	        # 3. Monta dicts e delega para build_calculation_request
   463	        structure_dict = {
   464	            "structure_id":    structure["id"],
   465	            "name":            structure.get("name", ""),
   466	            "underlying_asset": underlying,
   467	            "alias_legacy_aba": structure.get("alias_legacy_aba"),
   468	            "legs": [
   469	                {
   470	                    "position_side":   leg["position_side"],
   471	                    "option_type":     leg["option_type"],
   472	                    "strike":          leg["strike"],
   473	                    "expiration_date": leg["expiration_date"],
   474	                    "quantity":        leg["quantity"],
   475	                    "symbol":          leg.get("symbol"),
   476	                    "premium":         leg.get("premium"),
   477	                    "multiplier":      leg.get("multiplier", 1.0),
   478	                    "leg_order":       leg.get("leg_order", 0),
   479	                    "notes":           leg.get("notes"),
   480	                }
   481	                for leg in legs_raw
   482	            ],
   483	        }
   484	
   485	        market_snapshot_dict = {
   486	            "snapshot_id":        snapshot.get("id"),
   487	            "snapshot_timestamp": snapshot.get("snapshot_timestamp", ""),
   488	            "underlying_asset":   snapshot.get("underlying_asset", underlying),
   489	            "spot_price":         snapshot.get("spot_price", 0.0),
   490	            "source":             snapshot.get("source", "rtd"),
   491	            "option_quotes":      snapshot.get("option_quotes"),
   492	            "greeks":             snapshot.get("greeks"),
   493	            "volatility_context": snapshot.get("volatility_context"),
   494	        }
   495	
   496	        return self.build_calculation_request(structure_dict, market_snapshot_dict)
   497	
   498	    def run_full_pipeline_from_db(
   499	        self,
   500	        structure_id: int,
   501	        snapshot_timestamp: Optional[str] = None,
   502	    ) -> Dict[str, Any]:
   503	        """
   504	        Pipeline completo resolvendo estrutura e snapshot pelos repositorios.
   505	
   506	        Retorna dict com chaves: structure_id, payoff, decision.
   507	        """
   508	        request        = self.build_calculation_request_from_db(
   509	            structure_id=structure_id,
   510	            snapshot_timestamp=snapshot_timestamp,
   511	        )
   512	        pipeline_result = self.run_full_pipeline(request)
   513	
   514	        return {
   515	            "structure_id": structure_id,
   516	            "payoff":       pipeline_result["payoff"],
   517	            "decision":     pipeline_result["decision"],
   518	        }
```

## FILE: services/derived_service.py
```python
     1	from __future__ import annotations
     2	# services/derived_service.py
     3	"""
     4	alteracao_30/alteracao_57c -- Servico de persistencia de dados derivados (payoff + decisoes).
     5	alteracao_62           -- AbaResolverMixin extraído para repositories/_aba_resolver_mixin.py.
     6	alteracao_65           -- get_payoff_by_aba() removida da interface pública (standalone).
     7	"""
     8	
     9	import inspect
    10	import json
    11	import sqlite3
    12	from datetime import datetime, timezone
    13	from typing import Any, Dict, List, Optional, Tuple, Union
    14	
    15	from db.config import connect_app, connect_derived
    16	from db.derived_repo import (
    17	    cleanup_old_decisions,
    18	    cleanup_old_payoff_data,
    19	    ensure_derived_tables,
    20	    insert_payoff_points,
    21	    insert_structure_decision,
    22	)
    23	from src.domain.refs.structure_ref import StructureRef
    24	
    25	
    26	# ------------------------------------------------------------------
    27	# Cache modulo-level: aba -> structure_id
    28	# ------------------------------------------------------------------
    29	
    30	_ABA_TO_STRUCTURE_ID: Dict[str, int] = {}
    31	_ABA_CACHE_LOADED: bool = False
    32	
    33	
    34	def _load_aba_cache() -> None:
    35	    global _ABA_TO_STRUCTURE_ID, _ABA_CACHE_LOADED
    36	    try:
    37	        with connect_app() as conn:
    38	            cur = conn.execute("""
    39	                SELECT id, alias_legacy_aba
    40	                FROM structures
    41	                WHERE alias_legacy_aba IS NOT NULL
    42	                  AND alias_legacy_aba != ''
    43	            """)
    44	            _ABA_TO_STRUCTURE_ID = {row[1]: row[0] for row in cur.fetchall()}
    45	    except Exception:
    46	        _ABA_TO_STRUCTURE_ID = {}
    47	    finally:
    48	        _ABA_CACHE_LOADED = True
    49	
    50	
    51	def _resolve_structure_id(aba: Optional[str]) -> Optional[int]:
    52	    if not _ABA_CACHE_LOADED:
    53	        _load_aba_cache()
    54	    if not aba:
    55	        return None
    56	    return _ABA_TO_STRUCTURE_ID.get(aba)
    57	
    58	
    59	def invalidate_aba_cache() -> None:
    60	    global _ABA_CACHE_LOADED
    61	    _ABA_CACHE_LOADED = False
    62	
    63	
    64	# ------------------------------------------------------------------
    65	# Helpers internos
    66	# ------------------------------------------------------------------
    67	
    68	def _now_iso() -> str:
    69	    return datetime.now(timezone.utc).isoformat()
    70	
    71	
    72	def _safe_str(value: Any) -> Optional[str]:
    73	    if value is None:
    74	        return None
    75	    text = str(value).strip()
    76	    return text or None
    77	
    78	
    79	def _unwrap_ref(ref: Any) -> Optional[str]:
    80	    """
    81	    alteracao_57: extrai string aba de StructureRef ou passa str diretamente.
    82	    Equivalente a _unwrap_aba do derived_repo, mas para a camada de servico.
    83	    """
    84	    if isinstance(ref, StructureRef):
    85	        return ref.aba
    86	    return _safe_str(ref)
    87	
    88	
    89	def _resolve_storage_key(
    90	    aba: Optional[str] = None,
    91	    structure_id: Any = None,
    92	    structure_name: Any = None,
    93	    underlying_asset: Any = None,
    94	) -> str:
    95	    # 1. aba explícita tem prioridade máxima
    96	    resolved_aba = _safe_str(aba)
    97	    if resolved_aba:
    98	        return resolved_aba
    99	
   100	    # 2. structure_id → resolver alias_legacy_aba via cache (FIX alteracao_66)
   101	    resolved_sid = _safe_str(structure_id)
   102	    if resolved_sid:
   103	        try:
   104	            sid_int = int(resolved_sid)
   105	            if not _ABA_CACHE_LOADED:
   106	                _load_aba_cache()
   107	            id_to_aba = {v: k for k, v in _ABA_TO_STRUCTURE_ID.items()}
   108	            alias = id_to_aba.get(sid_int)
   109	            if alias:
   110	                return alias  # "BOVA11" em vez de "structure:7"
   111	        except (ValueError, TypeError):
   112	            pass
   113	        return f"structure:{resolved_sid}"  # fallback sem alias
   114	
   115	    # 3. fallbacks por nome/ativo
   116	    resolved_structure_name = _safe_str(structure_name)
   117	    if resolved_structure_name:
   118	        return resolved_structure_name
   119	
   120	    resolved_underlying_asset = _safe_str(underlying_asset)
   121	    if resolved_underlying_asset:
   122	        return resolved_underlying_asset
   123	
   124	    return "unknown"
   125	
   126	
   127	def _merge_meta(
   128	    meta: Optional[Dict[str, Any]] = None,
   129	    structure_id: Any = None,
   130	    structure_name: Any = None,
   131	    underlying_asset: Any = None,
   132	    reference_date: Any = None,
   133	    input_meta: Optional[Dict[str, Any]] = None,
   134	    storage_key: Optional[str] = None,
   135	) -> Dict[str, Any]:
   136	    return {
   137	        **(meta or {}),
   138	        "structure_id":     structure_id,
   139	        "structure_name":   structure_name,
   140	        "underlying_asset": underlying_asset,
   141	        "reference_date":   reference_date,
   142	        "input_meta":       input_meta or {},
   143	        "storage_key":      storage_key,
   144	    }
   145	
   146	
   147	# ------------------------------------------------------------------
   148	# Init
   149	# ------------------------------------------------------------------
   150	
   151	def init_db():
   152	    with connect_derived() as conn:
   153	        ensure_derived_tables(conn)
   154	
   155	
   156	# ------------------------------------------------------------------
   157	# Payoff
   158	# ------------------------------------------------------------------
   159	
   160	def save_payoff_curve(
   161	    ref: Any,
   162	    points: List[Union[Tuple[float, float], Dict[str, float]]],
   163	    spot_ref: Optional[float] = None,
   164	    meta: Optional[Dict[str, Any]] = None,
   165	    timestamp: Optional[str] = None,
   166	    structure_id: Any = None,
   167	) -> int:
   168	    """
   169	    alteracao_57: 'ref' aceita StructureRef, str ou None.
   170	    _unwrap_ref() extrai a string aba de forma segura.
   171	    """
   172	    ts           = timestamp or _now_iso()
   173	    storage_key  = _unwrap_ref(ref) or "unknown"
   174	    resolved_sid = (
   175	        int(structure_id)
   176	        if structure_id is not None
   177	        else _resolve_structure_id(storage_key)
   178	    )
   179	
   180	    norm_points: List[Tuple[float, float]] = []
   181	    for p in points or []:
   182	        if isinstance(p, (tuple, list)) and len(p) == 2:
   183	            norm_points.append((float(p[0]), float(p[1])))
   184	        elif isinstance(p, dict):
   185	            x = p.get("point_spot") or p.get("s_t")
   186	            y = p.get("point_pl")   or p.get("pl_venc")
   187	            if x is None or y is None:
   188	                continue
   189	            norm_points.append((float(x), float(y)))
   190	
   191	    effective_meta = {
   192	        **(meta or {}),
   193	        "storage_key":  storage_key,
   194	        "structure_id": resolved_sid,
   195	    }
   196	
   197	    with connect_derived() as conn:
   198	        ensure_derived_tables(conn)
   199	        return insert_payoff_points(
   200	            conn=conn,
   201	            timestamp=ts,
   202	            aba=storage_key,
   203	            points=norm_points,
   204	            spot_ref=spot_ref,
   205	            meta=effective_meta,
   206	            structure_id=resolved_sid,
   207	        )
   208	
   209	
   210	def save_payoff_from_canonical_payload(
   211	    payoff: Dict[str, Any],
   212	    aba: Optional[str] = None,
   213	    timestamp: Optional[str] = None,
   214	) -> int:
   215	    ts = timestamp or _now_iso()
   216	
   217	    storage_key = _resolve_storage_key(
   218	        aba=aba,
   219	        structure_id=payoff.get("structure_id"),
   220	        structure_name=payoff.get("structure_name"),
   221	        underlying_asset=payoff.get("underlying_asset"),
   222	    )
   223	
   224	    sid_from_payload = payoff.get("structure_id")
   225	    resolved_sid = (
   226	        int(sid_from_payload)
   227	        if sid_from_payload is not None
   228	        else _resolve_structure_id(storage_key)
   229	    )
   230	
   231	    meta = _merge_meta(
   232	        meta=payoff.get("meta"),
   233	        structure_id=resolved_sid,
   234	        structure_name=payoff.get("structure_name"),
   235	        underlying_asset=payoff.get("underlying_asset"),
   236	        reference_date=payoff.get("reference_date"),
   237	        input_meta=payoff.get("input_meta"),
   238	        storage_key=storage_key,
   239	    )
   240	
   241	    try:
   242	        sig = inspect.signature(save_payoff_curve)
   243	        accepts_structure_id = (
   244	            "structure_id" in sig.parameters
   245	            or any(
   246	                p.kind == inspect.Parameter.VAR_KEYWORD
   247	                for p in sig.parameters.values()
   248	            )
   249	        )
   250	    except (TypeError, ValueError):
   251	        accepts_structure_id = True
   252	
   253	    if accepts_structure_id:
   254	        return save_payoff_curve(
   255	            ref=storage_key,
   256	            points=payoff.get("points", []),
   257	            spot_ref=payoff.get("spot_ref"),
   258	            meta=meta,
   259	            timestamp=ts,
   260	            structure_id=resolved_sid,
   261	        )
   262	
   263	    return save_payoff_curve(
   264	        ref=storage_key,
   265	        points=payoff.get("points", []),
   266	        spot_ref=payoff.get("spot_ref"),
   267	        meta=meta,
   268	        timestamp=ts,
   269	    )
   270	
   271	
   272	
   273	def save_decision(
   274	    ref: Any,
   275	    decision: Dict[str, Any],
   276	    timestamp: Optional[str] = None,
   277	    structure_id: Any = None,
   278	) -> int:
   279	    """
   280	    alteracao_57: 'ref' aceita StructureRef, str ou None.
   281	
   282	    Fase 3A.4:
   283	    - Preserva structure_id explícito recebido por argumento, pelo payload
   284	      ou pelo meta.
   285	    - Só tenta resolver por storage_key/alias quando não há structure_id explícito.
   286	    """
   287	    ts = timestamp or _now_iso()
   288	    storage_key = _unwrap_ref(ref) or "unknown"
   289	
   290	    explicit_sid = structure_id
   291	    if explicit_sid is None:
   292	        explicit_sid = decision.get("structure_id")
   293	    if explicit_sid is None:
   294	        explicit_sid = (decision.get("meta") or {}).get("structure_id")
   295	
   296	    resolved_sid = (
   297	        int(explicit_sid)
   298	        if explicit_sid is not None
   299	        else _resolve_structure_id(storage_key)
   300	    )
   301	
   302	    enriched_decision = {
   303	        **decision,
   304	        "structure_id": resolved_sid,
   305	        "meta": {
   306	            **(decision.get("meta") or {}),
   307	            "storage_key": storage_key,
   308	            "structure_id": resolved_sid,
   309	        },
   310	    }
   311	
   312	    with connect_derived() as conn:
   313	        ensure_derived_tables(conn)
   314	        return insert_structure_decision(
   315	            conn=conn,
   316	            timestamp=ts,
   317	            aba=storage_key,
   318	            decision_dict=enriched_decision,
   319	        )
   320	
   321	
   322	def save_decision_from_canonical_payload(
   323	    decision: Dict[str, Any],
   324	    structure_id: Any = None,
   325	    structure_name: Any = None,
   326	    underlying_asset: Any = None,
   327	    aba: Optional[str] = None,
   328	    timestamp: Optional[str] = None,
   329	) -> int:
   330	    ts = timestamp or _now_iso()
   331	
   332	    storage_key = _resolve_storage_key(
   333	        aba=aba,
   334	        structure_id=structure_id,
   335	        structure_name=structure_name,
   336	        underlying_asset=underlying_asset,
   337	    )
   338	
   339	    resolved_sid = (
   340	        int(structure_id)
   341	        if structure_id is not None
   342	        else _resolve_structure_id(storage_key)
   343	    )
   344	
   345	    enriched_decision = {
   346	        **decision,
   347	        "structure_id": resolved_sid,
   348	        "meta": {
   349	            **(decision.get("meta") or {}),
   350	            "structure_id":     resolved_sid,
   351	            "structure_name":   structure_name,
   352	            "underlying_asset": underlying_asset,
   353	            "storage_key":      storage_key,
   354	        },
   355	    }
   356	
   357	    return save_decision(
   358	        ref=storage_key,
   359	        decision=enriched_decision,
   360	        timestamp=ts,
   361	    )
   362	
   363	
   364	# ------------------------------------------------------------------
   365	# Cleanup
   366	# ------------------------------------------------------------------
   367	
   368	def cleanup_derived(days_to_keep: int = 30) -> Dict[str, int]:
   369	    with connect_derived() as conn:
   370	        ensure_derived_tables(conn)
   371	        deleted_payoff = cleanup_old_payoff_data(conn, days_to_keep=days_to_keep)
   372	        deleted_dec    = cleanup_old_decisions(conn, days_to_keep=days_to_keep)
   373	        return {"payoff_deleted": deleted_payoff, "decisions_deleted": deleted_dec}
   374	
   375	
   376	# ------------------------------------------------------------------
   377	# Leituras
   378	# ------------------------------------------------------------------
   379	
   380	def get_all_payoff_curves():
   381	    with connect_derived() as conn:
   382	        cursor = conn.cursor()
   383	        cursor.execute("""
   384	            SELECT timestamp, aba, point_spot, point_pl, meta_json
   385	            FROM payoff_curve_points
   386	            ORDER BY timestamp DESC, point_spot
   387	        """)
   388	        return [
   389	            {
   390	                "timestamp":  row[0],
   391	                "aba":        row[1],
   392	                "point_spot": row[2],
   393	                "point_pl":   row[3],
   394	                "meta_json":  json.loads(row[4]) if row[4] else None,
   395	            }
   396	            for row in cursor.fetchall()
   397	        ]
   398	
   399	
   400	def get_payoff_by_structure_id(structure_id: int):
   401	    """
   402	    alteracao_56/alteracao_65: único ponto de entrada canônico para leitura de payoff.
   403	
   404	    Retorna somente a curva mais recente da estrutura.
   405	    Importante: payoff_curve_points mantém histórico por timestamp.
   406	    Sem filtrar MAX(timestamp), a UI pode misturar curvas antigas e novas.
   407	    """
   408	    ref = StructureRef.from_id(structure_id)
   409	    col, val = ref.db_pair()
   410	
   411	    with connect_derived() as conn:
   412	        cursor = conn.cursor()
   413	        cursor.execute(
   414	            f"""
   415	            SELECT timestamp, point_spot, point_pl, meta_json
   416	              FROM payoff_curve_points
   417	             WHERE {col} = ?
   418	               AND timestamp = (
   419	                    SELECT MAX(timestamp)
   420	                      FROM payoff_curve_points
   421	                     WHERE {col} = ?
   422	               )
   423	             ORDER BY point_spot
   424	            """,
   425	            (val, val),
   426	        )
   427	        return [
   428	            {
   429	                "timestamp":  row[0],
   430	                "point_spot": row[1],
   431	                "point_pl":   row[2],
   432	                "meta_json":  json.loads(row[3]) if row[3] else None,
   433	            }
   434	            for row in cursor.fetchall()
   435	        ]
   436	
   437	
   438	
   439	def get_recent_decisions():
   440	    with connect_derived() as conn:
   441	        conn.row_factory = sqlite3.Row
   442	        cursor = conn.cursor()
   443	
   444	        cols = [
   445	            row["name"]
   446	            for row in cursor.execute(
   447	                "PRAGMA table_info(structure_decisions)"
   448	            ).fetchall()
   449	        ]
   450	
   451	        select_cols = [
   452	            "timestamp", "aba", "decision", "level",
   453	            "pl_atual", "pl_max", "pl_pct_of_max", "dte_min",
   454	            "spot_ref", "meta_json", "created_at",
   455	        ]
   456	        if "structure_id" in cols:
   457	            select_cols.append("structure_id")
   458	        if "why" in cols:
   459	            select_cols.append("why")
   460	        if "why_json" in cols:
   461	            select_cols.append("why_json")
   462	
   463	        cursor.execute(f"""
   464	            SELECT {", ".join(select_cols)}
   465	            FROM structure_decisions
   466	            ORDER BY timestamp DESC
   467	            LIMIT 50
   468	        """)
   469	
   470	        decisions = []
   471	        for row in cursor.fetchall():
   472	            item = dict(row)
   473	            why_val      = item.get("why")
   474	            why_json_val = item.get("why_json")
   475	
   476	            if isinstance(why_val, str):
   477	                try:
   478	                    item["why"] = json.loads(why_val)
   479	                except Exception:
   480	                    pass
   481	            elif why_val is None and why_json_val is not None:
   482	                try:
   483	                    item["why"] = (
   484	                        json.loads(why_json_val)
   485	                        if isinstance(why_json_val, str)
   486	                        else why_json_val
   487	                    )
   488	                except Exception:
   489	                    item["why"] = why_json_val
   490	
   491	            if item.get("structure_id") is None:
   492	                for src_key in ("why_json", "meta_json"):
   493	                    raw = item.get(src_key)
   494	                    if not raw:
   495	                        continue
   496	                    try:
   497	                        parsed = json.loads(raw) if isinstance(raw, str) else raw
   498	                        sid = parsed.get("structure_id")
   499	                        if sid is not None:
   500	                            item["structure_id"] = sid
   501	                            break
   502	                    except Exception:
   503	                        pass
   504	
   505	            decisions.append(item)
   506	
   507	        return decisions
   508	
   509	
   510	# ---------------------------------------------------------------------------
   511	# alteracao_59 -- format_report + snapshot_aba (surface canônica)
   512	# ---------------------------------------------------------------------------
   513	
   514	def format_report(entries) -> str:
   515	    """Formata relatório de auditoria de surface ABA em texto legível."""
   516	    lines: list[str] = []
   517	    for e in entries:
   518	        aba_str = getattr(e, "aba_str", str(getattr(e, "structure_id", "")))
   519	        sid     = getattr(e, "structure_id", "?")
   520	        ref     = getattr(e, "reference_date", "?")
   521	        lines.append(f"{sid} | {ref} | {aba_str}")
   522	    return "\n".join(lines)
   523	
   524	
   525	def snapshot_aba(ref: "StructureRef") -> str:
   526	    """Retorna aba_str canônico a partir de um StructureRef."""
   527	    aba_str = ref.aba if hasattr(ref, "aba") and ref.aba else str(ref.structure_id)
   528	    return aba_str
   529	
   530	
   531	# ------------------------------------------------------------------
   532	# alteracao_65 -- DerivedService: fachada orientada a objetos
   533	# get_payoff_by_aba() removida da interface pública.
   534	# get_payoff_by_structure_id() é o único ponto de entrada canônico.
   535	# ------------------------------------------------------------------
   536	
   537	class DerivedService:
   538	    """Fachada OO sobre as funcoes standalone do derived_service.
   539	    alteracao_65: get_payoff_by_aba() nao exposta -- use get_payoff_by_structure_id().
   540	    get_payoff_by_aba() ausente por decisao de design (alteracao_65): interface simplificada.
   541	    """
   542	
   543	    # alteracao_65: get_payoff_by_aba() deliberadamente nao implementada nesta classe.
   544	    # Chamadores legados devem migrar para get_payoff_by_structure_id().
   545	
   546	    def get_payoff_by_structure_id(self, structure_id: int):
   547	        """Retorna pontos de payoff para a estrutura informada."""
   548	        return get_payoff_by_structure_id(structure_id)
   549	
   550	    def save_payoff_curve(self, *args, **kwargs):
   551	        return save_payoff_curve(*args, **kwargs)
   552	
   553	    def save_decision(self, *args, **kwargs):
   554	        return save_decision(*args, **kwargs)
   555	
   556	    def cleanup_derived(self, days_to_keep: int = 30):
   557	        return cleanup_derived(days_to_keep)
```

## FILE: services/derived_payoff_persistence.py
```python
     1	# services/derived_payoff_persistence.py
     2	import logging
     3	from datetime import datetime, timezone
     4	from typing import Any
     5	
     6	from domain.payoff import compute_payoff_from_canonical_input
     7	from services.derived_service import save_payoff_from_canonical_payload, save_decision_from_canonical_payload
     8	
     9	logger = logging.getLogger(__name__)
    10	
    11	
    12	class DerivedPayoffPersistence:
    13	    """
    14	    Implementação concreta de PayoffPersistencePort.
    15	
    16	    Responsabilidades:
    17	      1. Montar o canonical_input a partir do pricing_payload
    18	      2. Calcular a curva de payoff via domain/payoff.py
    19	      3. Persistir pontos no derived.db via derived_service
    20	      4. Persistir decisão básica derivada do resultado do engine
    21	    """
    22	
    23	    # -------------------------------------------------------------- #
    24	    #  PayoffPersistencePort.persist()                                 #
    25	    # -------------------------------------------------------------- #
    26	
    27	    def persist(
    28	        self,
    29	        pricing_payload: dict[str, Any] | None,
    30	        result: dict[str, Any],
    31	    ) -> None:
    32	        if not pricing_payload:
    33	            logger.debug("derived_payoff_persistence: pricing_payload vazio, skip.")
    34	            return
    35	
    36	        inner = result.get("result", result) if isinstance(result, dict) else{}
    37	        status = inner.get("status", "")
    38	        if status not in ("success", "ok", "completed"):
    39	            logger.debug(
    40	                "derived_payoff_persistence: status=%r não elegível para payoff, skip.",
    41	                status,
    42	            )
    43	            return
    44	
    45	        # Timestamp único para payoff + decisão.
    46	        # Evita snapshots inconsistentes por diferença de milissegundos entre gravações.
    47	        snapshot_ts = datetime.now(timezone.utc).isoformat()
    48	
    49	        payoff_saved = self._persist_payoff(pricing_payload, result, snapshot_ts)
    50	        if not payoff_saved:
    51	            logger.warning(
    52	                "derived_payoff_persistence: decisão não gravada porque payoff não foi salvo -- structure_id=%s",
    53	                pricing_payload.get("structure_id"),
    54	            )
    55	            return
    56	
    57	        decision_saved = self._persist_decision(pricing_payload, result, snapshot_ts)
    58	        if not decision_saved:
    59	            logger.error(
    60	                "derived_payoff_persistence: payoff salvo, mas decisão falhou -- structure_id=%s timestamp=%s",
    61	                pricing_payload.get("structure_id"),
    62	                snapshot_ts,
    63	            )
    64	
    65	    # -------------------------------------------------------------- #
    66	    #  payoff                                                          #
    67	    # -------------------------------------------------------------- #
    68	
    69	    def _persist_payoff(
    70	        self,
    71	        pricing_payload: dict[str, Any],
    72	        result: dict[str, Any],
    73	        snapshot_ts: str,
    74	    ) -> bool:
    75	        try:
    76	            canonical_input = self._build_canonical_input(pricing_payload, result)
    77	            payoff_result = compute_payoff_from_canonical_input(canonical_input)
    78	
    79	            if not payoff_result.get("points"):
    80	                logger.warning(
    81	                    "derived_payoff_persistence: payoff sem pontos para structure_id=%s",
    82	                    pricing_payload.get("structure_id"),
    83	                )
    84	                return False
    85	
    86	            save_payoff_from_canonical_payload(payoff_result, timestamp=snapshot_ts)
    87	            logger.info(
    88	                "derived_payoff_persistence: %d pontos gravados -- structure_id=%s",
    89	                len(payoff_result["points"]),
    90	                pricing_payload.get("structure_id"),
    91	            )
    92	            return True
    93	
    94	        except Exception:
    95	            logger.exception(
    96	                "derived_payoff_persistence: erro ao gravar payoff -- structure_id=%s",
    97	                pricing_payload.get("structure_id"),
    98	            )
    99	            return False
   100	
   101	    # -------------------------------------------------------------- #
   102	    #  decisão                                                         #
   103	    # -------------------------------------------------------------- #
   104	
   105	    def _persist_decision(
   106	        self,
   107	        pricing_payload: dict[str, Any],
   108	        result: dict[str, Any],
   109	        snapshot_ts: str,
   110	    ) -> bool:
   111	        try:
   112	            if not isinstance(result, dict):
   113	                inner = {}
   114	            else:
   115	                inner = result.get("result") or result
   116	
   117	            valuation = inner.get("valuation") or {}
   118	            metrics   = inner.get("metrics")   or {}
   119	
   120	            theoretical_value = valuation.get("theoretical_value")
   121	            pl_max            = valuation.get("pl_max")
   122	            pl_atual          = valuation.get("pl_atual") or theoretical_value
   123	            dte_min           = metrics.get("dte_min")
   124	            spot_ref          = pricing_payload.get("spot_price")
   125	            
   126	            if spot_ref is None:
   127	                spot_ref = (pricing_payload.get("market") or {}).get("spot_price")
   128	
   129	            pl_pct_of_max = None
   130	            if pl_max and pl_atual is not None:
   131	                try:
   132	                    pl_pct_of_max = round(float(pl_atual) / float(pl_max), 6)
   133	                except (ZeroDivisionError, TypeError, ValueError):
   134	                    pass
   135	
   136	            decision_dict = {
   137	                "decision":      "HOLD",
   138	                "level":         0,
   139	                "pl_atual":      pl_atual,
   140	                "pl_max":        pl_max,
   141	                "pl_pct_of_max": pl_pct_of_max,
   142	                "dte_min":       dte_min,
   143	                "spot_ref":      spot_ref,
   144	                "why": {
   145	                    "source":           "pricing_engine",
   146	                    "engine":           inner.get("engine"),
   147	                    "execution_status": inner.get("status"),
   148	                    "theoretical_value": theoretical_value,
   149	                },
   150	                "meta": {
   151	                    "structure_id":    pricing_payload.get("structure_id"),
   152	                    "structure_name":  pricing_payload.get("structure_name"),
   153	                    "underlying_asset": pricing_payload.get("underlying_asset"),
   154	                    "reference_date":  pricing_payload.get("reference_date"),
   155	                },
   156	            }
   157	
   158	            save_decision_from_canonical_payload(
   159	                decision=decision_dict,
   160	                structure_id=pricing_payload.get("structure_id"),
   161	                structure_name=pricing_payload.get("structure_name"),
   162	                underlying_asset=pricing_payload.get("underlying_asset"),
   163	                timestamp=snapshot_ts,
   164	            )
   165	            logger.info(
   166	                "derived_payoff_persistence: decisão gravada -- structure_id=%s",
   167	                pricing_payload.get("structure_id"),
   168	            )
   169	            return True
   170	
   171	        except Exception:
   172	            logger.exception(
   173	                "derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s",
   174	                pricing_payload.get("structure_id"),
   175	            )
   176	            return False
   177	
   178	    # -------------------------------------------------------------- #
   179	    #  helpers                                                         #
   180	    # -------------------------------------------------------------- #
   181	
   182	
   183	    @staticmethod
   184	    def _normalize_position_side(value: Any, quantity: Any = None) -> str | None:
   185	        """
   186	        Normaliza aliases de direção para o contrato canônico de payoff.
   187	
   188	        domain/payoff.py exige leg["position_side"].
   189	        Payloads vindos da UI/manual podem vir com leg["side"].
   190	        """
   191	        raw = "" if value is None else str(value).strip().upper()
   192	
   193	        aliases = {
   194	            "BUY": "LONG",
   195	            "BOUGHT": "LONG",
   196	            "COMPRA": "LONG",
   197	            "COMPRADO": "LONG",
   198	            "LONG": "LONG",
   199	            "SELL": "SHORT",
   200	            "SOLD": "SHORT",
   201	            "VENDA": "SHORT",
   202	            "VENDIDO": "SHORT",
   203	            "SHORT": "SHORT",
   204	        }
   205	
   206	        if raw in aliases:
   207	            return aliases[raw]
   208	
   209	        try:
   210	            q = float(quantity)
   211	            if q < 0:
   212	                return "SHORT"
   213	            if q > 0:
   214	                return "LONG"
   215	        except (TypeError, ValueError):
   216	            pass
   217	
   218	        return None
   219	
   220	    @staticmethod
   221	    def _normalize_leg_for_payoff(leg: Any) -> dict[str, Any]:
   222	        """
   223	        Adapta uma leg recebida de fontes legadas/manuais para o contrato
   224	        esperado por domain.compute_payoff_from_canonical_input().
   225	
   226	        Correção principal da Fase 3F Fix1:
   227	          side -> position_side
   228	
   229	        Também mantém aliases úteis sem remover os campos originais.
   230	        """
   231	        data = dict(leg) if isinstance(leg, dict) else dict(vars(leg))
   232	
   233	        quantity = data.get("quantity", data.get("quant"))
   234	        position_side = data.get("position_side") or data.get("side")
   235	
   236	        normalized_side = DerivedPayoffPersistence._normalize_position_side(
   237	            position_side,
   238	            quantity,
   239	        )
   240	
   241	        if normalized_side:
   242	            data["position_side"] = normalized_side
   243	            data.setdefault("side", normalized_side)
   244	
   245	        if quantity is not None:
   246	            try:
   247	                # No contrato canônico, a direção fica em position_side.
   248	                # A quantidade deve ser magnitude positiva.
   249	                data["quantity"] = abs(float(quantity))
   250	            except (TypeError, ValueError):
   251	                data["quantity"] = quantity
   252	
   253	        option_type = data.get("option_type")
   254	        if option_type is not None:
   255	            data["option_type"] = str(option_type).strip().upper()
   256	
   257	        instrument_type = data.get("instrument_type")
   258	        if instrument_type is not None:
   259	            data["instrument_type"] = str(instrument_type).strip().upper()
   260	
   261	        # Aliases defensivos para eventuais payloads de outras origens.
   262	        if "premium" not in data and "price" in data:
   263	            data["premium"] = data.get("price")
   264	
   265	        if "price" not in data and "premium" in data:
   266	            data["price"] = data.get("premium")
   267	
   268	        if "symbol" not in data:
   269	            data["symbol"] = data.get("asset") or data.get("ativo")
   270	
   271	        return data
   272	
   273	    @staticmethod
   274	    def _normalize_canonical_input_for_payoff(
   275	        canonical_input: dict[str, Any],
   276	    ) -> dict[str, Any]:
   277	        """
   278	        Retorna uma cópia rasa do canonical_input com legs normalizadas para payoff.
   279	        """
   280	        normalized = dict(canonical_input)
   281	
   282	        structure = dict(normalized.get("structure") or {})
   283	        market = dict(normalized.get("market") or {})
   284	        meta = dict(normalized.get("meta") or {})
   285	
   286	        legs = structure.get("legs") or []
   287	        structure["legs"] = [
   288	            DerivedPayoffPersistence._normalize_leg_for_payoff(leg)
   289	            for leg in legs
   290	        ]
   291	
   292	        meta.setdefault("payoff_leg_normalization", "fase_3f_fix1_position_side_from_side")
   293	
   294	        normalized["structure"] = structure
   295	        normalized["market"] = market
   296	        normalized["meta"] = meta
   297	
   298	        return normalized
   299	
   300	
   301	    @staticmethod
   302	    def _build_canonical_input(
   303	        pricing_payload: dict[str, Any],
   304	        result: dict[str, Any],
   305	    ) -> dict[str, Any]:
   306	        """
   307	        Monta o canonical_input esperado por compute_payoff_from_canonical_input().
   308	
   309	        Suporta dois formatos de pricing_payload:
   310	          A) já canônico: { structure: { legs, ... }, market: { spot_price, ... } }
   311	          B) flat:        { legs: [...], spot_price: ..., structure_id: ..., ... }
   312	        """
   313	        # Formato A -- já canônico, mas ainda assim normalizado para o contrato
   314	        # estrito de domain/payoff.py.
   315	        if "structure" in pricing_payload and "market" in pricing_payload:
   316	            return DerivedPayoffPersistence._normalize_canonical_input_for_payoff(
   317	                pricing_payload
   318	            )
   319	
   320	        # Formato B -- flat  montar canônico
   321	        structure_id   = pricing_payload.get("structure_id")
   322	        structure_name = pricing_payload.get("structure_name")
   323	        underlying     = pricing_payload.get("underlying_asset")
   324	        spot_price     = pricing_payload.get("spot_price") or 0.0
   325	        reference_date = pricing_payload.get("reference_date")
   326	        legs           = pricing_payload.get("legs") or []
   327	
   328	        payload_meta = pricing_payload.get("meta")
   329	        meta = dict(payload_meta) if isinstance(payload_meta, dict) else {}
   330	        meta.setdefault("source", "pricing_execution_persistence")
   331	        meta.setdefault("payoff_leg_normalization", "fase_3f_fix1_position_side_from_side")
   332	
   333	        canonical_input = {
   334	            "structure": {
   335	                "structure_id":    structure_id,
   336	                "name":            structure_name,
   337	                "underlying_asset": underlying,
   338	                "legs": [
   339	                    DerivedPayoffPersistence._normalize_leg_for_payoff(leg)
   340	                    for leg in legs
   341	                ],
   342	            },
   343	            "market": {
   344	                "spot_price":       spot_price,
   345	                "underlying_asset": underlying,
   346	                "reference_date":   reference_date,
   347	            },
   348	            "meta": meta,
   349	        }
   350	
   351	        return canonical_input
```

## FILE: domain/payoff.py
```python
     1	from typing import Any
     2	
     3	from domain.canonical_validators import validate_canonical_input
     4	from domain.position_side import to_pricing_engine_side
     5	
     6	
     7	def _round_money(value: float, digits: int = 6) -> float:
     8	    return round(float(value), digits)
     9	
    10	
    11	def _normalize_side(value: Any) -> str:
    12	    return to_pricing_engine_side(value)
    13	
    14	
    15	def _normalize_option_type(value: Any) -> str:
    16	    return str(value or "").strip().upper()
    17	
    18	
    19	def _intrinsic_value(option_type: str, strike: float, spot_at_expiration: float) -> float:
    20	    if option_type == "CALL":
    21	        return max(spot_at_expiration - strike, 0.0)
    22	    if option_type == "PUT":
    23	        return max(strike - spot_at_expiration, 0.0)
    24	    return 0.0
    25	
    26	
    27	def _compute_leg_payoff_at_expiration(leg: dict[str, Any], spot_at_expiration: float) -> float:
    28	    position_side = _normalize_side(leg.get("position_side"))
    29	    option_type = _normalize_option_type(leg.get("option_type"))
    30	
    31	    strike = float(leg.get("strike") or 0.0)
    32	    quantity = float(leg.get("quantity") or 0.0)
    33	    multiplier = float(leg.get("multiplier") or 1.0)
    34	    premium = leg.get("premium")
    35	    premium_value = float(premium) if premium is not None else 0.0
    36	
    37	    intrinsic = _intrinsic_value(
    38	        option_type=option_type,
    39	        strike=strike,
    40	        spot_at_expiration=spot_at_expiration,
    41	    )
    42	
    43	    payoff_unit = intrinsic - premium_value
    44	
    45	    if position_side == "SHORT":
    46	        payoff_unit = -payoff_unit
    47	
    48	    return payoff_unit * quantity * multiplier
    49	
    50	
    51	def compute_payoff_curve_from_canonical_legs(
    52	    legs: list[dict[str, Any]],
    53	    spot_ref: float,
    54	    low_pct: float = 0.5,
    55	    high_pct: float = 1.5,
    56	    step_pct: float = 0.01,
    57	) -> dict[str, Any]:
    58	    if not legs:
    59	        return {
    60	            "points": [],
    61	            "pl_max": 0.0,
    62	            "pl_min": 0.0,
    63	            "spot_ref": _round_money(spot_ref, 6),
    64	            "meta": {
    65	                "legs_count": 0,
    66	                "input_type": "canonical_legs",
    67	                "grid_params": {
    68	                    "low_pct": low_pct,
    69	                    "high_pct": high_pct,
    70	                    "step_pct": step_pct,
    71	                },
    72	            },
    73	        }
    74	
    75	    s_min = float(spot_ref) * float(low_pct)
    76	    s_max = float(spot_ref) * float(high_pct)
    77	    step = float(spot_ref) * float(step_pct)
    78	
    79	    if step <= 0:
    80	        step = 1.0
    81	
    82	    points: list[tuple[float, float]] = []
    83	    pl_values: list[float] = []
    84	
    85	    s_t = s_min
    86	    while s_t <= s_max + (step / 2):
    87	        pl_total = 0.0
    88	
    89	        for leg in legs:
    90	            pl_total += _compute_leg_payoff_at_expiration(
    91	                leg=leg,
    92	                spot_at_expiration=s_t,
    93	            )
    94	
    95	        s_t_rounded = _round_money(s_t, 6)
    96	        pl_total_rounded = _round_money(pl_total, 6)
    97	
    98	        points.append((s_t_rounded, pl_total_rounded))
    99	        pl_values.append(pl_total_rounded)
   100	
   101	        s_t += step
   102	
   103	    pl_max = _round_money(max(pl_values), 6) if pl_values else 0.0
   104	    pl_min = _round_money(min(pl_values), 6) if pl_values else 0.0
   105	
   106	    return {
   107	        "points": points,
   108	        "pl_max": pl_max,
   109	        "pl_min": pl_min,
   110	        "spot_ref": _round_money(spot_ref, 6),
   111	        "meta": {
   112	            "legs_count": len(legs),
   113	            "input_type": "canonical_legs",
   114	            "grid_params": {
   115	                "low_pct": low_pct,
   116	                "high_pct": high_pct,
   117	                "step_pct": step_pct,
   118	            },
   119	        },
   120	    }
   121	
   122	
   123	def compute_payoff_from_canonical_input(
   124	    canonical_input: dict[str, Any],
   125	    low_pct: float = 0.5,
   126	    high_pct: float = 1.5,
   127	    step_pct: float = 0.01,
   128	) -> dict[str, Any]:
   129	    structure = canonical_input.get("structure") or {}
   130	    market = canonical_input.get("market") or {}
   131	    input_meta = canonical_input.get("meta") or {}
   132	
   133	    errors = validate_canonical_input(canonical_input)
   134	    if errors:
   135	        return {
   136	            "points": [],
   137	            "pl_max": 0.0,
   138	            "pl_min": 0.0,
   139	            "spot_ref": float(market.get("spot_price") or 0.0),
   140	            "meta": {
   141	                "input_type": "canonical_legs",
   142	                "validation_errors": errors,
   143	            },
   144	            "structure_id": structure.get("structure_id"),
   145	            "structure_name": structure.get("name"),
   146	            "underlying_asset": (
   147	                market.get("underlying_asset")
   148	                or structure.get("underlying_asset")
   149	            ),
   150	            "reference_date": market.get("reference_date") or input_meta.get("reference_date"),
   151	            "input_meta": input_meta,
   152	        }
   153	
   154	    legs = structure.get("legs") or []
   155	    spot_ref = float(market.get("spot_price") or 0.0)
   156	
   157	    result = compute_payoff_curve_from_canonical_legs(
   158	        legs=legs,
   159	        spot_ref=spot_ref,
   160	        low_pct=low_pct,
   161	        high_pct=high_pct,
   162	        step_pct=step_pct,
   163	    )
   164	
   165	    return {
   166	        **result,
   167	        "structure_id": structure.get("structure_id"),
   168	        "structure_name": structure.get("name"),
   169	        "underlying_asset": (
   170	            market.get("underlying_asset")
   171	            or structure.get("underlying_asset")
   172	        ),
   173	        "reference_date": market.get("reference_date") or input_meta.get("reference_date"),
   174	        "input_meta": input_meta,
   175	    }
```

## FILE: domain/decision.py
```python
     1	#!/usr/bin/env python3
     2	"""
     3	Domain: Decision logic (30/60/80 thresholds + DTE gate) from real data.
     4	
     5	Codigo legado removido neste modulo.
     6	Funcoes canonicas: compute_decision_from_inputs, compute_decision_from_payoff,
     7	compute_decision_from_contract.
     8	"""
     9	from __future__ import annotations
    10	
    11	import json
    12	import math
    13	from typing import Any, Dict, List, Optional, Tuple
    14	
    15	from domain.contracts import CanonicalStructureMarketInput
    16	
    17	
    18	# ---------------------------------------------------------------------------
    19	# Constantes de decisão
    20	# ---------------------------------------------------------------------------
    21	THRESHOLD_CLOSE   = 0.80
    22	THRESHOLD_PREPARE = 0.60
    23	THRESHOLD_WATCH   = 0.30
    24	
    25	DTE_GATE_DEFAULT  = 7
    26	
    27	
    28	# ---------------------------------------------------------------------------
    29	# Helpers internos (exportados para testes de interpolação)
    30	# ---------------------------------------------------------------------------
    31	
    32	def _interp_payoff(points: List[Tuple[float, float]], spot: float) -> float:
    33	    """Interpola P&L no spot dado a partir dos pontos da curva."""
    34	    if not points:
    35	        return 0.0
    36	    xs = [p[0] for p in points]
    37	    ys = [p[1] for p in points]
    38	    if spot <= xs[0]:
    39	        return ys[0]
    40	    if spot >= xs[-1]:
    41	        return ys[-1]
    42	    for i in range(len(xs) - 1):
    43	        if xs[i] <= spot <= xs[i + 1]:
    44	            t = (spot - xs[i]) / (xs[i + 1] - xs[i])
    45	            return ys[i] + t * (ys[i + 1] - ys[i])
    46	    return 0.0
    47	
    48	
    49	def _ratio(numerator: float, denominator: float) -> float:
    50	    if denominator == 0.0:
    51	        return 0.0
    52	    return numerator / denominator
    53	
    54	
    55	# Mapeamento decision  level
    56	_DECISION_LEVEL = {
    57	    "HOLD":         0,
    58	    "WATCH":        1,   # nível interno, mapeado para decision="HOLD" level=1
    59	    "PREPARE_ROLL": 2,
    60	    "CLOSE_REOPEN": 3,
    61	}
    62	
    63	
    64	# ---------------------------------------------------------------------------
    65	# API pública
    66	# ---------------------------------------------------------------------------
    67	
    68	def compute_decision_from_inputs(
    69	    pl_atual: float,
    70	    pl_max: float,
    71	    dte_min: Optional[int] = None,
    72	    dte_gate: int = DTE_GATE_DEFAULT,
    73	    spread_pct_medio: Optional[float] = None,
    74	    thresholds: Optional[Dict[str, float]] = None,
    75	) -> Dict[str, Any]:
    76	    _t_close   = (thresholds or {}).get("close",   THRESHOLD_CLOSE)
    77	    _t_prepare = (thresholds or {}).get("prepare", THRESHOLD_PREPARE)
    78	    _t_watch   = (thresholds or {}).get("watch",   THRESHOLD_WATCH)
    79	
    80	    ratio = _ratio(pl_atual, pl_max)
    81	    alts: List[str] = []
    82	
    83	    if spread_pct_medio is not None and spread_pct_medio > 0.015:
    84	        alts.append("Spread alto -- aguardar execução")
    85	
    86	    # [OK] Gate só dispara se dte_min foi fornecido E é > 0
    87	    #    dte_min=0 significa "expirado/sem DTE real" -- não aciona gate
    88	    if dte_min is not None and dte_min > 0 and dte_min <= dte_gate:
    89	        _internal = "CLOSE_REOPEN"
    90	        level = 3
    91	        reason = "DTE gate"
    92	        extra: Dict[str, Any] = {"dte_min": dte_min, "dte_gate": dte_gate}
    93	    elif ratio >= _t_close:
    94	        _internal = "CLOSE_REOPEN"
    95	        level = 3
    96	        reason = "threshold_close"
    97	        extra = {}
    98	    elif ratio >= _t_prepare:
    99	        _internal = "PREPARE_ROLL"
   100	        level = 2
   101	        reason = "threshold_prepare"
   102	        extra = {}
   103	    elif ratio >= _t_watch:
   104	        _internal = "WATCH"
   105	        level = 1
   106	        reason = "threshold_watch"
   107	        extra = {}
   108	    else:
   109	        _internal = "HOLD"
   110	        level = 0
   111	        reason = "below_watch"
   112	        extra = {}
   113	
   114	    decision = "HOLD" if _internal == "WATCH" else _internal
   115	
   116	    why_dict: Dict[str, Any] = {
   117	        "reasons":        [reason],
   118	        "ratio":          round(ratio, 4),
   119	        "alternatives":   alts,
   120	        "thresholds_used": {
   121	            "watch":   _t_watch,
   122	            "prepare": _t_prepare,
   123	            "close":   _t_close,
   124	        },
   125	        **extra,
   126	    }
   127	
   128	    return {
   129	        "decision":      decision,
   130	        "level":         level,
   131	        "ratio":         round(ratio, 4),
   132	        "pl_pct_of_max": round(ratio, 4),
   133	        "why_json":      json.dumps(why_dict),
   134	        "why":           why_dict,
   135	        "alternatives":  alts,
   136	    }
   137	
   138	
   139	def compute_decision_from_payoff(
   140	    payoff: Dict[str, Any],
   141	    dte_min: Optional[int] = None,
   142	    dte_gate: int = DTE_GATE_DEFAULT,
   143	    spread_pct_medio: Optional[float] = None,
   144	    thresholds: Optional[Dict[str, float]] = None,
   145	) -> Dict[str, Any]:
   146	    """
   147	    Decide a partir de um dict de payoff.
   148	    Payoff vazio ou inválido  HOLD com 'error' em why_json.
   149	    """
   150	    if not payoff:
   151	        why_dict = {"error": "payoff vazio ou invalido", "reason": "invalid_input"}
   152	        return {
   153	            "decision":      "HOLD",
   154	            "level":         0,
   155	            "ratio":         0.0,
   156	            "pl_pct_of_max": 0.0,
   157	            "why_json":      json.dumps(why_dict),
   158	            "why":           why_dict,
   159	            "alternatives":  [],
   160	        }
   161	
   162	    pl_atual = payoff.get("pl_atual") or payoff.get("pl_now") or 0.0
   163	    pl_max   = payoff.get("pl_max") or 0.0
   164	
   165	    # Interpolação via points + spot, se disponíveis
   166	    points = payoff.get("points") or []
   167	    spot   = payoff.get("spot")
   168	    if points and spot is not None and pl_atual == 0.0:
   169	        pl_atual = _interp_payoff(points, float(spot))
   170	
   171	    if not math.isfinite(float(pl_max)):
   172	        why_dict = {"error": "pl_max invalido", "reason": "invalid_pl_max"}
   173	        return {
   174	            "decision":      "HOLD",
   175	            "level":         0,
   176	            "ratio":         0.0,
   177	            "pl_pct_of_max": 0.0,
   178	            "why_json":      json.dumps(why_dict),
   179	            "why":           why_dict,
   180	            "alternatives":  [],
   181	        }
   182	
   183	    return compute_decision_from_inputs(
   184	        pl_atual=float(pl_atual),
   185	        pl_max=float(pl_max),
   186	        dte_min=dte_min,
   187	        dte_gate=dte_gate,
   188	        spread_pct_medio=spread_pct_medio,
   189	        thresholds=thresholds,
   190	    )
   191	
   192	
   193	def compute_decision_from_contract(
   194	    contract: CanonicalStructureMarketInput,
   195	    payoff: Optional[Dict[str, Any]] = None,
   196	) -> Dict[str, Any]:
   197	    """Entrada canônica via CanonicalStructureMarketInput."""
   198	    pl_max  = float(getattr(contract, "pl_max",  None) or 0.0)
   199	    dte_min = getattr(contract, "dte_min", None)
   200	
   201	    if payoff:
   202	        return compute_decision_from_payoff(payoff=payoff, dte_min=dte_min)
   203	
   204	    pl_atual = float(
   205	        getattr(contract, "pl_atual", None)
   206	        or getattr(contract, "pl_now", None)
   207	        or 0.0
   208	    )
   209	    return compute_decision_from_inputs(
   210	        pl_atual=pl_atual,
   211	        pl_max=pl_max,
   212	        dte_min=dte_min,
   213	    )
```

## FILE: domain/structure_metrics.py
```python
     1	from datetime import date, datetime
     2	from typing import Any, Iterable
     3	
     4	from domain.position_side import to_pricing_engine_side
     5	
     6	
     7	def _parse_date(value: str | None) -> date | None:
     8	    if not value:
     9	        return None
    10	
    11	    value = str(value).strip()
    12	    if not value:
    13	        return None
    14	
    15	    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
    16	        try:
    17	            return datetime.strptime(value, fmt).date()
    18	        except ValueError:
    19	            continue
    20	
    21	    return None
    22	
    23	
    24	def _to_float(value: Any) -> float | None:
    25	    if value is None:
    26	        return None
    27	
    28	    if isinstance(value, bool):
    29	        return None
    30	
    31	    if isinstance(value, int | float):
    32	        return float(value)
    33	
    34	    text = str(value).strip()
    35	    if not text:
    36	        return None
    37	
    38	    text = text.replace(".", "").replace(",", ".") if "," in text else text
    39	
    40	    try:
    41	        return float(text)
    42	    except ValueError:
    43	        return None
    44	
    45	
    46	def _first_value(source: dict[str, Any], keys: Iterable[str]) -> Any:
    47	    for key in keys:
    48	        value = source.get(key)
    49	        if value is not None and str(value).strip() != "":
    50	            return value
    51	
    52	    return None
    53	
    54	
    55	def _first_float(source: dict[str, Any], keys: Iterable[str]) -> float | None:
    56	    for key in keys:
    57	        value = _to_float(source.get(key))
    58	        if value is not None:
    59	            return value
    60	
    61	    return None
    62	
    63	
    64	def _average(values: Iterable[float | None]) -> float | None:
    65	    valid_values = [value for value in values if value is not None]
    66	
    67	    if not valid_values:
    68	        return None
    69	
    70	    return sum(valid_values) / len(valid_values)
    71	
    72	
    73	def compute_dte(reference_date: str | None, expiration_date: str | None) -> int | None:
    74	    ref = _parse_date(reference_date)
    75	    exp = _parse_date(expiration_date)
    76	
    77	    if ref is None or exp is None:
    78	        return None
    79	
    80	    return (exp - ref).days
    81	
    82	
    83	def compute_dte_min_from_canonical_input(canonical_input: dict[str, Any]) -> int | None:
    84	    structure = canonical_input.get("structure") or {}
    85	    market = canonical_input.get("market") or {}
    86	
    87	    reference_date = market.get("reference_date")
    88	    legs = structure.get("legs", [])
    89	
    90	    dtes = []
    91	    for leg in legs:
    92	        expiration_date = leg.get("expiration_date")
    93	        dte = compute_dte(reference_date, expiration_date)
    94	        if dte is not None:
    95	            dtes.append(dte)
    96	
    97	    if not dtes:
    98	        return None
    99	
   100	    return min(dtes)
   101	
   102	
   103	def compute_mid(bid: Any, ask: Any) -> float | None:
   104	    bid_value = _to_float(bid)
   105	    ask_value = _to_float(ask)
   106	
   107	    if bid_value is None or ask_value is None:
   108	        return None
   109	
   110	    return (bid_value + ask_value) / 2
   111	
   112	
   113	def compute_spread(bid: Any, ask: Any) -> float | None:
   114	    bid_value = _to_float(bid)
   115	    ask_value = _to_float(ask)
   116	
   117	    if bid_value is None or ask_value is None:
   118	        return None
   119	
   120	    return ask_value - bid_value
   121	
   122	
   123	def compute_spread_pct(bid: Any, ask: Any, mid: Any = None) -> float | None:
   124	    spread = compute_spread(bid, ask)
   125	    mid_value = _to_float(mid)
   126	
   127	    if mid_value is None:
   128	        mid_value = compute_mid(bid, ask)
   129	
   130	    if spread is None or mid_value is None or mid_value == 0:
   131	        return None
   132	
   133	    return spread / mid_value
   134	
   135	
   136	def normalize_position_side(leg: dict[str, Any]) -> str | None:
   137	    side = _first_value(
   138	        leg,
   139	        (
   140	            "position_side",
   141	            "side",
   142	            "cv",
   143	            "compra_venda",
   144	            "buy_sell",
   145	        ),
   146	    )
   147	
   148	    if side is None:
   149	        quantity = _first_float(leg, ("quantity", "quant", "qty", "qtd"))
   150	        if quantity is None:
   151	            return None
   152	        return "SHORT" if quantity < 0 else "LONG"
   153	
   154	    try:
   155	        return to_pricing_engine_side(side)
   156	    except ValueError:
   157	        return None
   158	
   159	
   160	def position_multiplier(leg: dict[str, Any]) -> int:
   161	    side = normalize_position_side(leg)
   162	
   163	    if side == "SHORT":
   164	        return -1
   165	
   166	    return 1
   167	
   168	
   169	def leg_quantity(leg: dict[str, Any]) -> float | None:
   170	    quantity = _first_float(leg, ("quantity", "quant", "qty", "qtd"))
   171	
   172	    if quantity is None:
   173	        return None
   174	
   175	    return abs(quantity)
   176	
   177	
   178	def compute_realistic_price(leg: dict[str, Any]) -> float | None:
   179	    side = normalize_position_side(leg)
   180	
   181	    bid = _first_float(leg, ("bid",))
   182	    ask = _first_float(leg, ("ask",))
   183	    mid = _first_float(leg, ("mid",))
   184	    last = _first_float(leg, ("last", "ultimo", "último", "preco", "price"))
   185	
   186	    if mid is None:
   187	        mid = compute_mid(bid, ask)
   188	
   189	    if side == "SHORT":
   190	        for value in (ask, mid, bid, last):
   191	            if value is not None:
   192	                return value
   193	
   194	        return None
   195	
   196	    for value in (bid, mid, ask, last):
   197	        if value is not None:
   198	            return value
   199	
   200	    return None
   201	
   202	def compute_pl_realista(leg: dict[str, Any]) -> float | None:
   203	    quantity = leg_quantity(leg)
   204	
   205	    entry_price = _first_float(
   206	        leg,
   207	        (
   208	            "valor_executado",
   209	            "execution_price",
   210	            "entry_price",
   211	            "preco_execucao",
   212	            "preço_execução",
   213	            "preco_entrada",
   214	            "preço_entrada",
   215	        ),
   216	    )
   217	
   218	    realistic_price = compute_realistic_price(leg)
   219	
   220	    if entry_price is None:
   221	        premium = _first_float(leg, ("premium", "premio", "prêmio"))
   222	
   223	        if premium is not None:
   224	            entry_price = premium
   225	
   226	            bid = _first_float(leg, ("bid",))
   227	            ask = _first_float(leg, ("ask",))
   228	            mid = _first_float(leg, ("mid",))
   229	
   230	            if mid is None:
   231	                mid = compute_mid(bid, ask)
   232	
   233	            if mid is not None:
   234	                realistic_price = mid
   235	
   236	    if quantity is None or entry_price is None or realistic_price is None:
   237	        return _first_float(leg, ("pl_realista",))
   238	
   239	    return (realistic_price - entry_price) * quantity * position_multiplier(leg)
   240	
   241	def compute_greek_exposure(leg: dict[str, Any], greek_name: str) -> float | None:
   242	    greek_value = _first_float(leg, (greek_name,))
   243	    quantity = leg_quantity(leg)
   244	
   245	    if greek_value is None or quantity is None:
   246	        return None
   247	
   248	    return greek_value * quantity * position_multiplier(leg)
   249	
   250	
   251	def compute_leg_metrics(
   252	    leg: dict[str, Any],
   253	    reference_date: str | None = None,
   254	) -> dict[str, Any]:
   255	    bid = _first_float(leg, ("bid",))
   256	    ask = _first_float(leg, ("ask",))
   257	
   258	    mid = compute_mid(bid, ask)
   259	    if mid is None:
   260	        mid = _first_float(leg, ("mid",))
   261	
   262	    spread = compute_spread(bid, ask)
   263	    if spread is None:
   264	        spread = _first_float(leg, ("spread",))
   265	
   266	    spread_pct = compute_spread_pct(bid, ask, mid)
   267	    if spread_pct is None:
   268	        spread_pct = _first_float(leg, ("spread_pct",))
   269	
   270	    dte = _first_float(leg, ("dte",))
   271	    if dte is not None:
   272	        dte = int(dte)
   273	    else:
   274	        expiration_date = _first_value(
   275	            leg,
   276	            (
   277	                "expiration_date",
   278	                "vencimento",
   279	                "maturity_date",
   280	                "expiry",
   281	            ),
   282	        )
   283	        dte = compute_dte(reference_date, expiration_date)
   284	
   285	    return {
   286	        "side": normalize_position_side(leg),
   287	        "quantity": leg_quantity(leg),
   288	        "mid": mid,
   289	        "spread": spread,
   290	        "spread_pct": spread_pct,
   291	        "preco_realista": compute_realistic_price(leg),
   292	        "pl_realista": compute_pl_realista(leg),
   293	        "delta_exposto": compute_greek_exposure(leg, "delta"),
   294	        "gamma_exposto": compute_greek_exposure(leg, "gamma"),
   295	        "theta_exposto": compute_greek_exposure(leg, "theta"),
   296	        "vega_exposto": compute_greek_exposure(leg, "vega"),
   297	        "dte": dte,
   298	    }
   299	
   300	
   301	def compute_structure_metrics(
   302	    legs: list[dict[str, Any]],
   303	    reference_date: str | None = None,
   304	) -> dict[str, Any]:
   305	    computed_legs = []
   306	
   307	    for leg in legs:
   308	        leg_metrics = compute_leg_metrics(leg, reference_date=reference_date)
   309	        computed_legs.append(
   310	            {
   311	                **leg,
   312	                **leg_metrics,
   313	            }
   314	        )
   315	
   316	    pl_values = [leg.get("pl_realista") for leg in computed_legs]
   317	    delta_values = [leg.get("delta_exposto") for leg in computed_legs]
   318	    gamma_values = [leg.get("gamma_exposto") for leg in computed_legs]
   319	    theta_values = [leg.get("theta_exposto") for leg in computed_legs]
   320	    vega_values = [leg.get("vega_exposto") for leg in computed_legs]
   321	    dte_values = [leg.get("dte") for leg in computed_legs if leg.get("dte") is not None]
   322	
   323	    valid_pl_values = [value for value in pl_values if value is not None]
   324	    valid_delta_values = [value for value in delta_values if value is not None]
   325	    valid_gamma_values = [value for value in gamma_values if value is not None]
   326	    valid_theta_values = [value for value in theta_values if value is not None]
   327	    valid_vega_values = [value for value in vega_values if value is not None]
   328	
   329	    return {
   330	        "num_pernas": len(computed_legs),
   331	        "legs": computed_legs,
   332	        "pl_realista_total": sum(valid_pl_values) if valid_pl_values else None,
   333	        "delta_liq": sum(valid_delta_values) if valid_delta_values else None,
   334	        "gamma_liq": sum(valid_gamma_values) if valid_gamma_values else None,
   335	        "theta_liq": sum(valid_theta_values) if valid_theta_values else None,
   336	        "vega_liq": sum(valid_vega_values) if valid_vega_values else None,
   337	        "spread_medio": _average(leg.get("spread") for leg in computed_legs),
   338	        "spread_pct_medio": _average(leg.get("spread_pct") for leg in computed_legs),
   339	        "dte_min": min(dte_values) if dte_values else None,
   340	    }
   341	
   342	
   343	def compute_structure_metrics_from_canonical_input(
   344	    canonical_input: dict[str, Any],
   345	) -> dict[str, Any]:
   346	    structure = canonical_input.get("structure") or {}
   347	    market = canonical_input.get("market") or {}
   348	
   349	    reference_date = market.get("reference_date")
   350	    legs = structure.get("legs", [])
   351	
   352	    return compute_structure_metrics(legs, reference_date=reference_date)
```

## FILE: ATT/tests/test_structure_editor_dialog.py
```python
     1	# Testes do dialogo de edicao de estruturas
     2	"""
     3	Testes unitarios de StructureEditorDialog
     4	
     5	Estrategia: injecao direta de _repo via parametro de construtor.
     6	Nao depende de patch de namespace, funciona independentemente
     7	de como o dialog importa StructuresRepository.
     8	"""
     9	from __future__ import annotations
    10	
    11	import inspect
    12	import os
    13	import unittest
    14	from unittest.mock import MagicMock, patch
    15	
    16	
    17	# ---------------------------------------------------------------------------
    18	# Guard de importacao
    19	# ---------------------------------------------------------------------------
    20	try:
    21	    from UI.components.structure_editor_dialog import StructureEditorDialog
    22	    _IMPORT_OK = True
    23	    _IMPORT_ERROR = ""
    24	except Exception as exc:
    25	    _IMPORT_OK = False
    26	    _IMPORT_ERROR = str(exc)
    27	
    28	
    29	# ---------------------------------------------------------------------------
    30	# Helpers Tk
    31	# ---------------------------------------------------------------------------
    32	_TK_MODAL_METHODS = ["transient", "grab_set", "wait_window", "focus_set"]
    33	
    34	
    35	def _start_tk_patches() -> list:
    36	    """
    37	    Mocka metodos modais herdados de tk.Toplevel.
    38	    create=True necessario pois nao estao no __dict__ da subclasse.
    39	    """
    40	    patchers = []
    41	    for name in _TK_MODAL_METHODS:
    42	        p = patch.object(StructureEditorDialog, name, lambda *a, **kw: None, create=True)
    43	        p.start()
    44	        patchers.append(p)
    45	    return patchers
    46	
    47	
    48	def _stop_patches(patchers: list) -> None:
    49	    for p in patchers:
    50	        try:
    51	            p.stop()
    52	        except RuntimeError:
    53	            pass
    54	
    55	
    56	def _make_bare_dialog() -> "StructureEditorDialog":
    57	    """Cria instancia sem __init__ para testes de logica pura."""
    58	    obj = object.__new__(StructureEditorDialog)
    59	    obj._legs_rows = []
    60	    obj._structure_id = None
    61	    obj.saved = False
    62	    return obj
    63	
    64	
    65	def _make_mock_repo(get_return=None, create_return=42) -> MagicMock:
    66	    repo = MagicMock()
    67	    repo.get_structure.return_value = get_return
    68	    repo.create_structure.return_value = create_return
    69	    return repo
    70	
    71	
    72	# ===========================================================================
    73	# Bloco 1 -- Logica pura (sem Tk, sem repositorio)
    74	# ===========================================================================
    75	
    76	@unittest.skipUnless(_IMPORT_OK, "StructureEditorDialog nao importavel")
    77	class TestBuildLegsPayload(unittest.TestCase):
    78	
    79	    def _dialog(self, legs):
    80	        d = _make_bare_dialog()
    81	        d._legs_rows = legs
    82	        return d
    83	
    84	    def test_lista_vazia_retorna_lista_vazia(self):
    85	        self.assertEqual(self._dialog([])._build_legs_payload(), [])
    86	
    87	    def test_leg_order_comeca_em_1(self):
    88	        r = self._dialog([{"strike": 100.0}])._build_legs_payload()
    89	        self.assertEqual(r[0]["leg_order"], 1)
    90	
    91	    def test_leg_order_sequencial(self):
    92	        legs = [{"strike": 100.0}, {"strike": 110.0}, {"strike": 90.0}]
    93	        ordens = [r["leg_order"] for r in self._dialog(legs)._build_legs_payload()]
    94	        self.assertEqual(ordens, [1, 2, 3])
    95	
    96	    def test_campos_originais_preservados(self):
    97	        legs = [{
    98	            "position_side": "VENDIDO", "option_type": "CALL", "strike": 195.0,
    99	            "expiration_date": "2026-05-15", "quantity": 5000,
   100	            "premium": None, "multiplier": 1,
   101	        }]
   102	        r = self._dialog(legs)._build_legs_payload()[0]
   103	        self.assertEqual(r["position_side"], "VENDIDO")
   104	        self.assertEqual(r["strike"], 195.0)
   105	        self.assertEqual(r["leg_order"], 1)
   106	
   107	    def test_nao_modifica_legs_rows_original(self):
   108	        legs = [{"strike": 100.0}]
   109	        d = self._dialog(legs)
   110	        d._build_legs_payload()
   111	        self.assertNotIn("leg_order", d._legs_rows[0])
   112	
   113	    def test_duas_legs_sem_contaminar_indices(self):
   114	        legs = [{"strike": 100.0}, {"strike": 110.0}]
   115	        r = self._dialog(legs)._build_legs_payload()
   116	        self.assertEqual(r[0]["leg_order"], 1)
   117	        self.assertEqual(r[1]["leg_order"], 2)
   118	        self.assertEqual(r[0]["strike"], 100.0)
   119	        self.assertEqual(r[1]["strike"], 110.0)
   120	
   121	
   122	# ===========================================================================
   123	# Bloco 2 -- TestLoadExisting  (injecao direta de _repo)
   124	# ===========================================================================
   125	
   126	@unittest.skipUnless(_IMPORT_OK, "StructureEditorDialog nao importavel")
   127	class TestLoadExisting(unittest.TestCase):
   128	
   129	    def setUp(self):
   130	        import tkinter as Tk
   131	        self.root = Tk.Tk()
   132	        self.root.withdraw()
   133	        self._tk_patchers = _start_tk_patches()
   134	
   135	    def tearDown(self):
   136	        _stop_patches(self._tk_patchers)
   137	        try:
   138	            self.root.destroy()
   139	        except Exception:
   140	            pass
   141	
   142	    def _make_dialog(self, structure_id, repo_data):
   143	        mock_repo = _make_mock_repo(get_return=repo_data)
   144	        return StructureEditorDialog(
   145	            parent=self.root,
   146	            structure_id=structure_id,
   147	            db_path=":memory:",
   148	            _repo=mock_repo,        # <-- injecao direta
   149	        ), mock_repo
   150	
   151	    def test_carrega_campos_do_repositorio(self):
   152	        dados = {
   153	            "id": 1, "name": "BOVA11 Condor", "underlying_asset": "BOVA11",
   154	            "alias_legacy_aba": "BOVA11", "status": "active",
   155	            "notes": "teste", "legs": [],
   156	        }
   157	        dlg, _ = self._make_dialog(1, dados)
   158	        self.assertEqual(dlg._f_name.get(),       "BOVA11 Condor")
   159	        self.assertEqual(dlg._f_underlying.get(), "BOVA11")
   160	        self.assertEqual(dlg._f_alias.get(),      "BOVA11")
   161	        self.assertEqual(dlg._f_status.get(),     "active")
   162	        self.assertEqual(dlg._f_notes.get(),      "teste")
   163	
   164	    def test_carrega_legs_em_legs_rows(self):
   165	        leg = {
   166	            "position_side": "COMPRADO", "option_type": "CALL", "strike": 195.0,
   167	            "expiration_date": "2026-05-15", "quantity": 5000,
   168	            "premium": None, "multiplier": 1,
   169	        }
   170	        dados = {
   171	            "id": 1, "name": "X", "underlying_asset": "X",
   172	            "alias_legacy_aba": None, "status": "active", "notes": None,
   173	            "legs": [leg],
   174	        }
   175	        dlg, _ = self._make_dialog(1, dados)
   176	        self.assertEqual(len(dlg._legs_rows), 1)
   177	        self.assertEqual(dlg._legs_rows[0]["strike"], 195.0)
   178	
   179	    def test_destroi_se_estrutura_nao_encontrada(self):
   180	        mock_repo = _make_mock_repo(get_return=None)
   181	        with patch("tkinter.messagebox.showerror"):
   182	            StructureEditorDialog(
   183	                parent=self.root,
   184	                structure_id=99,
   185	                db_path=":memory:",
   186	                _repo=mock_repo,
   187	            )
   188	        mock_repo.get_structure.assert_called_once_with(99)
   189	
   190	
   191	# ===========================================================================
   192	# Bloco 3 -- TestCmdSaveCreate
   193	# ===========================================================================
   194	
   195	@unittest.skipUnless(_IMPORT_OK, "StructureEditorDialog nao importavel")
   196	class TestCmdSaveCreate(unittest.TestCase):
   197	
   198	    def setUp(self):
   199	        import tkinter as tk
   200	        self.root = tk.Tk()
   201	        self.root.withdraw()
   202	        self._tk_patchers = _start_tk_patches()
   203	        self.mock_repo = _make_mock_repo(get_return=None, create_return=42)
   204	
   205	    def tearDown(self):
   206	        _stop_patches(self._tk_patchers)
   207	        try:
   208	            self.root.destroy()
   209	        except Exception:
   210	            pass
   211	
   212	    def _make_dialog(self):
   213	        """Modo criacao: structure_id=None."""
   214	        return StructureEditorDialog(
   215	            parent=self.root,
   216	            structure_id=None,
   217	            db_path=":memory:",
   218	            _repo=self.mock_repo,   # <-- injecao direta
   219	        )
   220	
   221	
   222	    def test_create_structure_chamado_com_campos_corretos(self):
   223	        dlg = self._make_dialog()
   224	        dlg._f_name.set("PRIO3 Trava")
   225	        dlg._f_underlying.set("PRIO3")
   226	        dlg._f_alias.set("PRIO3")
   227	        dlg._f_status.set("active")
   228	        dlg._f_notes.set("")
   229	
   230	        dlg._cmd_save()
   231	
   232	        self.mock_repo.create_structure_with_legs.assert_called_once()
   233	        args, _kwargs = self.mock_repo.create_structure_with_legs.call_args
   234	
   235	        structure_arg = args[0]
   236	
   237	        self.assertEqual(structure_arg["name"], "PRIO3 Trava")
   238	        self.assertEqual(structure_arg["underlying_asset"], "PRIO3")
   239	        self.assertEqual(structure_arg["alias_legacy_aba"], "PRIO3")
   240	        self.assertEqual(structure_arg["status"], "active")
   241	        self.assertIsNone(structure_arg["notes"])
   242	
   243	
   244	    def test_replace_legs_chamado_apos_create(self):
   245	        dlg = self._make_dialog()
   246	        dlg._f_name.set("X")
   247	        dlg._f_underlying.set("Y")
   248	        dlg._f_status.set("active")
   249	        dlg._legs_rows = [{
   250	            "position_side": "COMPRADO", "option_type": "CALL", "strike": 100.0,
   251	            "expiration_date": "2026-05-15", "quantity": 1000,
   252	            "premium": None, "multiplier": 1, "symbol": None,
   253	        }]
   254	
   255	        dlg._cmd_save()
   256	
   257	        self.mock_repo.create_structure_with_legs.assert_called_once()
   258	        args, _kwargs = self.mock_repo.create_structure_with_legs.call_args
   259	
   260	        structure_arg = args[0]
   261	        legs_arg = args[1]
   262	
   263	        self.assertEqual(structure_arg["name"], "X")
   264	        self.assertEqual(structure_arg["underlying_asset"], "Y")
   265	        self.assertEqual(len(legs_arg), 1)
   266	        self.assertEqual(legs_arg[0]["position_side"], "COMPRADO")
   267	        self.assertEqual(legs_arg[0]["option_type"], "CALL")
   268	        self.assertEqual(legs_arg[0]["strike"], 100.0)
   269	
   270	    def test_saved_true_apos_sucesso(self):
   271	        dlg = self._make_dialog()
   272	        dlg._f_name.set("X")
   273	        dlg._f_underlying.set("Y")
   274	        dlg._f_status.set("active")
   275	        self.assertFalse(dlg.saved)
   276	        dlg._cmd_save()
   277	        self.assertTrue(dlg.saved)
   278	
   279	    def test_name_vazio_nao_chama_create(self):
   280	        dlg = self._make_dialog()
   281	        dlg._f_name.set("")
   282	        dlg._f_underlying.set("BOVA11")
   283	        with patch("tkinter.messagebox.showwarning"):
   284	            dlg._cmd_save()
   285	        self.mock_repo.create_structure.assert_not_called()
   286	        self.assertFalse(dlg.saved)
   287	
   288	    def test_underlying_vazio_nao_chama_create(self):
   289	        dlg = self._make_dialog()
   290	        dlg._f_name.set("Estrutura X")
   291	        dlg._f_underlying.set("")
   292	        with patch("tkinter.messagebox.showwarning"):
   293	            dlg._cmd_save()
   294	        self.mock_repo.create_structure.assert_not_called()
   295	        self.assertFalse(dlg.saved)
   296	
   297	
   298	# ===========================================================================
   299	# Bloco 4 -- TestCmdSaveUpdate
   300	# ===========================================================================
   301	
   302	@unittest.skipUnless(_IMPORT_OK, "StructureEditorDialog nao importavel")
   303	class TestCmdSaveUpdate(unittest.TestCase):
   304	
   305	    def setUp(self):
   306	        import tkinter as tk
   307	        self.root = tk.Tk()
   308	        self.root.withdraw()
   309	        self._tk_patchers = _start_tk_patches()
   310	        self.mock_repo = _make_mock_repo()
   311	
   312	    def tearDown(self):
   313	        _stop_patches(self._tk_patchers)
   314	        try:
   315	            self.root.destroy()
   316	        except Exception:
   317	            pass
   318	
   319	    def _make_edit_dialog(self, structure_id: int):
   320	        """Modo edicao: repo retorna dados validos."""
   321	        self.mock_repo.get_structure.return_value = {
   322	            "id": structure_id, "name": "Original", "underlying_asset": "ORIG",
   323	            "alias_legacy_aba": None, "status": "active", "notes": None,
   324	            "legs": [],
   325	        }
   326	        return StructureEditorDialog(
   327	            parent=self.root,
   328	            structure_id=structure_id,
   329	            db_path=":memory:",
   330	            _repo=self.mock_repo,   # <-- injecao direta
   331	        )
   332	
   333	    def test_update_structure_chamado_com_structure_id_correto(self):
   334	        dlg = self._make_edit_dialog(7)
   335	        dlg._f_name.set("Nome Atualizado")
   336	        dlg._f_underlying.set("BOVA11")
   337	        dlg._f_status.set("active")
   338	
   339	        dlg._cmd_save()
   340	
   341	        self.mock_repo.update_structure.assert_called_once()
   342	        sid_arg = self.mock_repo.update_structure.call_args[0][0]
   343	        self.assertEqual(sid_arg, 7)
   344	
   345	    def test_create_nao_e_chamado_no_modo_edicao(self):
   346	        dlg = self._make_edit_dialog(7)
   347	        dlg._f_name.set("X")
   348	        dlg._f_underlying.set("Y")
   349	        dlg._f_status.set("active")
   350	
   351	        dlg._cmd_save()
   352	
   353	        self.mock_repo.create_structure.assert_not_called()
   354	
   355	    def test_replace_legs_usa_structure_id_existente(self):
   356	        dlg = self._make_edit_dialog(7)
   357	        dlg._f_name.set("X")
   358	        dlg._f_underlying.set("Y")
   359	        dlg._f_status.set("active")
   360	        dlg._legs_rows = []
   361	
   362	        dlg._cmd_save()
   363	
   364	        self.mock_repo.replace_legs.assert_called_once_with(7, [])
   365	
   366	
   367	# ===========================================================================
   368	# Bloco 5 -- Verificacoes estaticas
   369	# ===========================================================================
   370	
   371	class TestStructureEditorDialogStaticChecks(unittest.TestCase):
   372	
   373	    def test_arquivo_existe(self):
   374	        path = os.path.join(
   375	            os.path.dirname(__file__),
   376	            "..", "..", "UI", "components", "structure_editor_dialog.py"
   377	        )
   378	        self.assertTrue(os.path.isfile(path))
   379	
   380	    def test_importavel(self):
   381	        if not _IMPORT_OK:
   382	            self.skipTest(f"Import falhou: {_IMPORT_ERROR}")
   383	        self.assertTrue(_IMPORT_OK)
   384	
   385	    def test_classe_presente(self):
   386	        if not _IMPORT_OK:
   387	            self.skipTest("Modulo nao importavel")
   388	        for metodo in ("_cmd_save", "_load_existing", "_build_legs_payload", "_build_ui"):
   389	            self.assertTrue(
   390	                hasattr(StructureEditorDialog, metodo),
   391	                f"{metodo} ausente em StructureEditorDialog"
   392	            )
   393	
   394	    def test_construtor_aceita_db_path(self):
   395	        if not _IMPORT_OK:
   396	            self.skipTest("Modulo nao importavel")
   397	        sig = inspect.signature(StructureEditorDialog.__init__)
   398	        params = list(sig.parameters.keys())
   399	        self.assertIn("db_path",      params)
   400	        self.assertIn("structure_id", params)
   401	
   402	    def test_construtor_aceita_repo_injetado(self):
   403	        """Confirma que o construtor aceita _repo para injecao em testes."""
   404	        if not _IMPORT_OK:
   405	            self.skipTest("Modulo nao importavel")
   406	        sig = inspect.signature(StructureEditorDialog.__init__)
   407	        self.assertIn(
   408	            "_repo", sig.parameters,
   409	            "StructureEditorDialog.__init__ deve aceitar _repo=None para injecao de dependencia"
   410	        )
   411	
   412	    def test_nao_importa_sqlite3_diretamente(self):
   413	        import ast
   414	        path = os.path.join(
   415	            os.path.dirname(__file__),
   416	            "..", "..", "UI", "components", "structure_editor_dialog.py"
   417	        )
   418	        if not os.path.isfile(path):
   419	            self.skipTest("arquivo nao encontrado")
   420	        with open(path, encoding="utf-8") as f:
   421	            tree = ast.parse(f.read())
   422	        imports = [
   423	            n.names[0].name for n in ast.walk(tree) if isinstance(n, ast.Import)
   424	        ]
   425	        import_froms = [
   426	            n.module for n in ast.walk(tree)
   427	            if isinstance(n, ast.ImportFrom) and n.module
   428	        ]
   429	        self.assertNotIn("sqlite3", imports)
   430	        self.assertNotIn("sqlite3", import_froms)
   431	
   432	
   433	if __name__ == "__main__":
   434	    unittest.main()
   435	
   436	def test_build_legs_payload_normaliza_position_side_legado_long_short():
   437	    dlg = object.__new__(StructureEditorDialog)
   438	    dlg._legs_rows = [
   439	        {
   440	            "position_side": "LONG",
   441	            "option_type": "CALL",
   442	            "strike": 100.0,
   443	            "expiration_date": "2026-12-18",
   444	            "quantity": 1,
   445	            "premium": None,
   446	            "multiplier": 1,
   447	            "symbol": "TESTC100",
   448	            "notes": None,
   449	        },
   450	        {
   451	            "position_side": "SHORT",
   452	            "option_type": "PUT",
   453	            "strike": 90.0,
   454	            "expiration_date": "2026-12-18",
   455	            "quantity": 2,
   456	            "premium": None,
   457	            "multiplier": 1,
   458	            "symbol": "TESTP90",
   459	            "notes": None,
   460	        },
   461	    ]
   462	
   463	    payload = dlg._build_legs_payload()
   464	
   465	    assert payload[0]["position_side"] == "COMPRADO"
   466	    assert payload[0]["leg_order"] == 1
   467	    assert payload[1]["position_side"] == "VENDIDO"
   468	    assert payload[1]["leg_order"] == 2
   469	
   470	def test_build_legs_payload_normaliza_strike_com_virgula_para_float():
   471	    dlg = object.__new__(StructureEditorDialog)
   472	    dlg._legs_rows = [
   473	        {
   474	            "position_side": "COMPRADO",
   475	            "option_type": "CALL",
   476	            "strike": "100,00",
   477	            "expiration_date": "2026-12-18",
   478	            "quantity": 1,
   479	            "premium": None,
   480	            "multiplier": 1,
   481	            "symbol": "TESTC100",
   482	            "notes": None,
   483	        }
   484	    ]
   485	
   486	    payload = dlg._build_legs_payload()
   487	
   488	    assert payload[0]["strike"] == 100.0
   489	    assert isinstance(payload[0]["strike"], float)
   490	
   491	
   492	def test_build_legs_payload_normaliza_strike_com_ponto_para_float():
   493	    dlg = object.__new__(StructureEditorDialog)
   494	    dlg._legs_rows = [
   495	        {
   496	            "position_side": "COMPRADO",
   497	            "option_type": "CALL",
   498	            "strike": "100.50",
   499	            "expiration_date": "2026-12-18",
   500	            "quantity": 1,
   501	            "premium": None,
   502	            "multiplier": 1,
   503	            "symbol": "TESTC100",
   504	            "notes": None,
   505	        }
   506	    ]
   507	
   508	    payload = dlg._build_legs_payload()
   509	
   510	    assert payload[0]["strike"] == 100.50
   511	    assert isinstance(payload[0]["strike"], float)
   512	
   513	
   514	def test_build_legs_payload_nao_modifica_strike_original_ao_normalizar():
   515	    dlg = object.__new__(StructureEditorDialog)
   516	    original_leg = {
   517	        "position_side": "COMPRADO",
   518	        "option_type": "CALL",
   519	        "strike": "100,00",
   520	        "expiration_date": "2026-12-18",
   521	        "quantity": 1,
   522	        "premium": None,
   523	        "multiplier": 1,
   524	        "symbol": "TESTC100",
   525	        "notes": None,
   526	    }
   527	    dlg._legs_rows = [original_leg]
   528	
   529	    payload = dlg._build_legs_payload()
   530	
   531	    assert payload[0]["strike"] == 100.0
   532	    assert original_leg["strike"] == "100,00"
   533	
   534	# FASE_3A4_TESTS_STRUCTURE_EDITOR_DIALOG
   535	
   536	def test_build_legs_payload_normaliza_premium_com_virgula_para_float():
   537	    dlg = object.__new__(StructureEditorDialog)
   538	    dlg._legs_rows = [
   539	        {
   540	            "position_side": "COMPRADO",
   541	            "option_type": "CALL",
   542	            "strike": "100,00",
   543	            "expiration_date": "2026-12-18",
   544	            "quantity": 1,
   545	            "premium": "1,25",
   546	            "multiplier": 1,
   547	            "symbol": "TESTC100",
   548	            "notes": None,
   549	        }
   550	    ]
   551	
   552	    payload = dlg._build_legs_payload()
   553	
   554	    assert payload[0]["premium"] == 1.25
   555	    assert isinstance(payload[0]["premium"], float)
   556	
   557	
   558	def test_build_legs_payload_normaliza_multiplier_com_virgula_para_float():
   559	    dlg = object.__new__(StructureEditorDialog)
   560	    dlg._legs_rows = [
   561	        {
   562	            "position_side": "COMPRADO",
   563	            "option_type": "CALL",
   564	            "strike": "100,00",
   565	            "expiration_date": "2026-12-18",
   566	            "quantity": 1,
   567	            "premium": None,
   568	            "multiplier": "100,0",
   569	            "symbol": "TESTC100",
   570	            "notes": None,
   571	        }
   572	    ]
   573	
   574	    payload = dlg._build_legs_payload()
   575	
   576	    assert payload[0]["multiplier"] == 100.0
   577	    assert isinstance(payload[0]["multiplier"], float)
   578	
   579	
   580	def test_build_legs_payload_preserva_premium_none():
   581	    dlg = object.__new__(StructureEditorDialog)
   582	    dlg._legs_rows = [
   583	        {
   584	            "position_side": "COMPRADO",
   585	            "option_type": "CALL",
   586	            "strike": "100,00",
   587	            "expiration_date": "2026-12-18",
   588	            "quantity": 1,
   589	            "premium": None,
   590	            "multiplier": 1,
   591	            "symbol": "TESTC100",
   592	            "notes": None,
   593	        }
   594	    ]
   595	
   596	    payload = dlg._build_legs_payload()
   597	
   598	    assert payload[0]["premium"] is None
   599	
   600	
   601	# FASE_2B_QUANTITY_NORMALIZATION_TESTS
   602	import pytest
   603	
   604	
   605	def _dlg_com_quantity_para_teste(quantity_value):
   606	    dlg = object.__new__(StructureEditorDialog)
   607	    dlg._legs_rows = [
   608	        {
   609	            "position_side": "COMPRADO",
   610	            "option_type": "CALL",
   611	            "strike": "100,00",
   612	            "expiration_date": "2026-12-18",
   613	            "quantity": quantity_value,
   614	            "premium": None,
   615	            "multiplier": 1,
   616	            "symbol": "TESTC100",
   617	            "notes": None,
   618	        }
   619	    ]
   620	    return dlg
   621	
   622	
   623	@pytest.mark.parametrize("quantity_value", ["1", "1,0", "1.0"])
   624	def test_build_legs_payload_normaliza_quantity_inteiro_valido(quantity_value):
   625	    dlg = _dlg_com_quantity_para_teste(quantity_value)
   626	
   627	    payload = dlg._build_legs_payload()
   628	
   629	    assert payload[0]["quantity"] == 1
   630	    assert isinstance(payload[0]["quantity"], int)
   631	
   632	
   633	@pytest.mark.parametrize("quantity_value", ["1,5", "abc"])
   634	def test_build_legs_payload_rejeita_quantity_invalido(quantity_value):
   635	    dlg = _dlg_com_quantity_para_teste(quantity_value)
   636	
   637	    with pytest.raises(
   638	        (ValueError, TypeError),
   639	        match=r"(?i)(quantity|quantidade|inteiro|integer|invalid|inv[aá]lid)",
   640	    ):
   641	        dlg._build_legs_payload()
```

## FILE: ATT/tests/test_structure_market_input_assembler.py
```python
     1	import unittest
     2	
     3	from services.structure_market_input_assembler import assemble_structure_market_input
     4	
     5	
     6	class StructureMarketInputAssemblerTests(unittest.TestCase):
     7	    def test_should_assemble_structure_and_market_input(self):
     8	        structure = {
     9	            "id": 7,
    10	            "name": "BOVA11 Condor Maio/2026",
    11	            "underlying_asset": "BOVA11",
    12	            "alias_legacy_aba": "BOVA11",
    13	            "legs": [
    14	                {
    15	                    "position_side": "LONG",
    16	                    "option_type": "CALL",
    17	                    "symbol": "BOVAE195",
    18	                    "strike": 195.0,
    19	                    "expiration_date": "2026-05-15",
    20	                    "quantity": 5000,
    21	                    "premium": None,
    22	                    "multiplier": 1.0,
    23	                }
    24	            ],
    25	        }
    26	
    27	        market_snapshot = {
    28	            "reference_date": "2026-05-18",
    29	            "underlying_asset": "BOVA11",
    30	            "spot_price": 198.35,
    31	            "interest_rate": 0.1175,
    32	            "volatility": 0.22,
    33	        }
    34	
    35	        result = assemble_structure_market_input(structure, market_snapshot)
    36	
    37	        self.assertIn("structure", result)
    38	        self.assertIn("market", result)
    39	        self.assertIn("meta", result)
    40	
    41	        self.assertEqual(result["structure"]["underlying_asset"], "BOVA11")
    42	        self.assertEqual(result["market"]["underlying_asset"], "BOVA11")
    43	        self.assertEqual(result["market"]["reference_date"], "2026-05-18")
    44	        self.assertEqual(result["meta"]["input_source"], "structure_market_input_assembler")
    45	
    46	    def test_should_raise_when_underlying_asset_mismatches(self):
    47	        structure = {
    48	            "id": 7,
    49	            "name": "BOVA11 Condor Maio/2026",
    50	            "underlying_asset": "BOVA11",
    51	            "legs": [],
    52	        }
    53	
    54	        market_snapshot = {
    55	            "reference_date": "2026-05-18",
    56	            "underlying_asset": "PETR4",
    57	            "spot_price": 198.35,
    58	            "interest_rate": 0.1175,
    59	            "volatility": 0.22,
    60	        }
    61	
    62	        with self.assertRaises(ValueError) as ctx:
    63	            assemble_structure_market_input(structure, market_snapshot)
    64	
    65	        self.assertIn("underlying_asset mismatch", str(ctx.exception))
    66	
    67	    def test_should_raise_when_structure_is_missing(self):
    68	        market_snapshot = {
    69	            "reference_date": "2026-05-18",
    70	            "underlying_asset": "BOVA11",
    71	            "spot_price": 198.35,
    72	            "interest_rate": 0.1175,
    73	            "volatility": 0.22,
    74	        }
    75	
    76	        with self.assertRaises(ValueError) as ctx:
    77	            assemble_structure_market_input({}, market_snapshot)
    78	
    79	        self.assertIn("structure is required", str(ctx.exception))
    80	
    81	    def test_should_raise_when_market_snapshot_is_missing(self):
    82	        structure = {
    83	            "id": 7,
    84	            "name": "BOVA11 Condor Maio/2026",
    85	            "underlying_asset": "BOVA11",
    86	            "legs": [],
    87	        }
    88	
    89	        with self.assertRaises(ValueError) as ctx:
    90	            assemble_structure_market_input(structure, {})
    91	
    92	        self.assertIn("market_snapshot is required", str(ctx.exception))
    93	
    94	
    95	if __name__ == "__main__":
    96	    unittest.main()
```

## FILE: ATT/tests/test_structure_analysis_service.py
```python
     1	import pytest
     2	
     3	from services.structure_analysis_service import StructureAnalysisService
     4	
     5	
     6	class FakeCanonicalInputService:
     7	    def __init__(self, error=None):
     8	        self.error = error
     9	        self.calls = []
    10	
    11	    def build_structure_market_input(
    12	        self,
    13	        structure_id: int,
    14	        reference_date: str | None = None,
    15	    ):
    16	        self.calls.append(
    17	            {
    18	                "structure_id": structure_id,
    19	                "reference_date": reference_date,
    20	            }
    21	        )
    22	
    23	        if self.error is not None:
    24	            raise self.error
    25	
    26	        return {
    27	            "structure": {
    28	                "structure_id": structure_id,
    29	                "name": "BOVA11 Condor Maio/2026 - Atualizada",
    30	                "underlying_asset": "BOVA11",
    31	                "alias_legacy_aba": "BOVA11",
    32	                "legs": [
    33	                    {
    34	                        "position_side": "LONG",
    35	                        "option_type": "PUT",
    36	                        "symbol": "BOVAM190",
    37	                        "strike": 190.0,
    38	                        "expiration_date": "2026-05-15",
    39	                        "quantity": 2000,
    40	                        "premium": None,
    41	                        "multiplier": 1.0,
    42	                    },
    43	                    {
    44	                        "position_side": "SHORT",
    45	                        "option_type": "PUT",
    46	                        "symbol": "BOVAM185",
    47	                        "strike": 185.0,
    48	                        "expiration_date": "2026-05-15",
    49	                        "quantity": 2000,
    50	                        "premium": None,
    51	                        "multiplier": 1.0,
    52	                    },
    53	                ],
    54	            },
    55	            "market": {
    56	                "reference_date": reference_date or "2026-05-15",
    57	                "underlying_asset": "BOVA11",
    58	                "spot_price": 198.35,
    59	                "interest_rate": 0.1175,
    60	                "volatility": 0.22,
    61	            },
    62	            "meta": {
    63	                "reference_date": reference_date or "2026-05-15",
    64	                "legs_source": "canonical",
    65	                "legacy_aba": "BOVA11",
    66	                "legacy_timestamp": None,
    67	            },
    68	        }
    69	
    70	
    71	class FakeInvalidCanonicalInputService:
    72	    def __init__(self):
    73	        self.calls = []
    74	
    75	    def build_structure_market_input(
    76	        self,
    77	        structure_id: int,
    78	        reference_date: str | None = None,
    79	    ):
    80	        self.calls.append(
    81	            {
    82	                "structure_id": structure_id,
    83	                "reference_date": reference_date,
    84	            }
    85	        )
    86	
    87	        return {
    88	            "structure": {
    89	                "structure_id": structure_id,
    90	                "name": "Estrutura inválida",
    91	                "underlying_asset": "BOVA11",
    92	                "alias_legacy_aba": "BOVA11",
    93	                "legs": [],
    94	            },
    95	            "market": {
    96	                "reference_date": reference_date or "2026-05-15",
    97	                "underlying_asset": "BOVA11",
    98	                "spot_price": 198.35,
    99	                "interest_rate": 0.1175,
   100	                "volatility": 0.22,
   101	            },
   102	            "meta": {
   103	                "reference_date": reference_date or "2026-05-15",
   104	                "legs_source": "canonical",
   105	                "legacy_aba": "BOVA11",
   106	                "legacy_timestamp": None,
   107	            },
   108	        }
   109	
   110	
   111	def test_structure_analysis_service_analyze_returns_full_pipeline():
   112	    service = StructureAnalysisService(
   113	        canonical_input_service=FakeCanonicalInputService()
   114	    )
   115	
   116	    result = service.analyze(
   117	        structure_id=1,
   118	        reference_date="2026-05-15",
   119	        spread_pct_medio=0.02,
   120	    )
   121	
   122	    assert "canonical_input" in result
   123	    assert "metrics" in result
   124	    assert "payoff" in result
   125	    assert "decision" in result
   126	
   127	    assert result["canonical_input"]["structure"]["structure_id"] == 1
   128	    assert result["canonical_input"]["market"]["reference_date"] == "2026-05-15"
   129	
   130	    assert result["metrics"]["dte_min_inferred"] == 0
   131	    assert result["metrics"]["dte_min_effective"] == 0
   132	    assert result["metrics"]["spread_pct_medio"] == 0.02
   133	
   134	    payoff = result["payoff"]
   135	    assert payoff is not None
   136	    assert payoff["pl_max"] == 10000.0
   137	    assert payoff["spot_ref"] == 198.35
   138	    assert "points" in payoff
   139	    assert len(payoff["points"]) > 0
   140	
   141	    decision = result["decision"]
   142	    assert decision is not None
   143	    assert decision["decision"] == "HOLD"
   144	    assert decision["dte_min"] == 0
   145	    assert "why" in decision
   146	    assert "why_json" in decision
   147	    assert isinstance(decision["why"], dict)
   148	    assert "reasons" in decision["why"]
   149	    assert "alternatives" in decision["why"]
   150	
   151	
   152	def test_structure_analysis_service_analyze_uses_explicit_dte_min_over_inferred():
   153	    service = StructureAnalysisService(
   154	        canonical_input_service=FakeCanonicalInputService()
   155	    )
   156	
   157	    result = service.analyze(
   158	        structure_id=1,
   159	        reference_date="2026-05-15",
   160	        dte_min=9,
   161	        spread_pct_medio=0.02,
   162	    )
   163	
   164	    assert result["metrics"]["dte_min_inferred"] == 0
   165	    assert result["metrics"]["dte_min_effective"] == 9
   166	    assert result["decision"]["dte_min"] == 9
   167	
   168	
   169	def test_structure_analysis_service_analyze_returns_structured_decision_for_invalid_payoff():
   170	    service = StructureAnalysisService(
   171	        canonical_input_service=FakeInvalidCanonicalInputService()
   172	    )
   173	
   174	    result = service.analyze(
   175	        structure_id=999,
   176	        reference_date="2026-05-15",
   177	    )
   178	
   179	    assert "payoff" in result
   180	    assert "decision" in result
   181	    assert result["decision"] is not None
   182	    assert result["decision"]["decision"] == "HOLD"
   183	    assert result["decision"]["level"] == 0
   184	    assert result["decision"]["why"]["error"] == "payoff is required"
   185	    assert "validation_errors" in result["decision"]["why"]
   186	
   187	
   188	def test_structure_analysis_service_analyze_propagates_custom_thresholds_and_dte_gate():
   189	    service = StructureAnalysisService(
   190	        canonical_input_service=FakeCanonicalInputService()
   191	    )
   192	
   193	    thresholds = {
   194	        "watch": 0.10,
   195	        "prepare": 0.20,
   196	        "close": 0.30,
   197	    }
   198	
   199	    result = service.analyze(
   200	        structure_id=1,
   201	        reference_date="2026-05-15",
   202	        thresholds=thresholds,
   203	        dte_gate=10,
   204	    )
   205	
   206	    decision = result["decision"]
   207	
   208	    assert decision is not None
   209	    assert "why" in decision
   210	    assert decision["why"]["thresholds_used"] == thresholds
   211	    assert decision["why"]["dte_gate"] == 10
   212	
   213	
   214	def test_structure_analysis_service_analyze_propagates_spread_warning():
   215	    service = StructureAnalysisService(
   216	        canonical_input_service=FakeCanonicalInputService()
   217	    )
   218	
   219	    result = service.analyze(
   220	        structure_id=1,
   221	        reference_date="2026-05-15",
   222	        spread_pct_medio=0.02,
   223	    )
   224	
   225	    assert any(
   226	        "Spread alto" in alternative
   227	        for alternative in result["decision"]["why"]["alternatives"]
   228	    )
   229	
   230	
   231	def test_structure_analysis_service_forwards_reference_date_to_canonical_service():
   232	    fake_canonical_service = FakeCanonicalInputService()
   233	    service = StructureAnalysisService(
   234	        canonical_input_service=fake_canonical_service
   235	    )
   236	
   237	    service.analyze(
   238	        structure_id=77,
   239	        reference_date="2026-06-01",
   240	    )
   241	
   242	    assert fake_canonical_service.calls == [
   243	        {
   244	            "structure_id": 77,
   245	            "reference_date": "2026-06-01",
   246	        }
   247	    ]
   248	
   249	
   250	def test_structure_analysis_service_propagates_canonical_input_service_error():
   251	    fake_canonical_service = FakeCanonicalInputService(
   252	        error=ValueError("structure not found: 404")
   253	    )
   254	    service = StructureAnalysisService(
   255	        canonical_input_service=fake_canonical_service
   256	    )
   257	
   258	    with pytest.raises(ValueError, match="structure not found: 404"):
   259	        service.analyze(structure_id=404)
   260	
   261	
   262	def test_structure_analysis_service_passes_effective_dte_to_decision(monkeypatch):
   263	    fake_canonical_service = FakeCanonicalInputService()
   264	    service = StructureAnalysisService(
   265	        canonical_input_service=fake_canonical_service
   266	    )
   267	
   268	    captured = {}
   269	
   270	    def fake_compute_dte_min_from_canonical_input(canonical_input):
   271	        return 3
   272	
   273	    def fake_compute_payoff_from_canonical_input(canonical_input):
   274	        return {"pl_max": 1.0, "spot_ref": 198.35, "points": []}
   275	
   276	    def fake_compute_decision_from_payoff(
   277	        payoff,
   278	        dte_min,
   279	        spread_pct_medio,
   280	        thresholds,
   281	        dte_gate,
   282	    ):
   283	        captured["payoff"] = payoff
   284	        captured["dte_min"] = dte_min
   285	        captured["spread_pct_medio"] = spread_pct_medio
   286	        captured["thresholds"] = thresholds
   287	        captured["dte_gate"] = dte_gate
   288	        return {
   289	            "decision": "HOLD",
   290	            "dte_min": dte_min,
   291	            "why": {},
   292	            "why_json": "{}",
   293	        }
   294	
   295	    monkeypatch.setattr(
   296	        "services.structure_analysis_service.compute_dte_min_from_canonical_input",
   297	        fake_compute_dte_min_from_canonical_input,
   298	    )
   299	    monkeypatch.setattr(
   300	        "services.structure_analysis_service.compute_payoff_from_canonical_input",
   301	        fake_compute_payoff_from_canonical_input,
   302	    )
   303	    monkeypatch.setattr(
   304	        "services.structure_analysis_service.compute_decision_from_payoff",
   305	        fake_compute_decision_from_payoff,
   306	    )
   307	
   308	    result = service.analyze(
   309	        structure_id=1,
   310	        spread_pct_medio=0.015,
   311	        thresholds={"watch": 0.1},
   312	        dte_gate=5,
   313	    )
   314	
   315	    assert captured == {
   316	        "payoff": {"pl_max": 1.0, "spot_ref": 198.35, "points": []},
   317	        "dte_min": 3,
   318	        "spread_pct_medio": 0.015,
   319	        "thresholds": {"watch": 0.1},
   320	        "dte_gate": 5,
   321	    }
   322	    assert result["metrics"]["dte_min_inferred"] == 3
   323	    assert result["metrics"]["dte_min_effective"] == 3
   324	    assert result["decision"]["dte_min"] == 3
   325	
   326	
   327	def test_structure_analysis_service_uses_zero_when_inferred_dte_is_none(monkeypatch):
   328	    fake_canonical_service = FakeCanonicalInputService()
   329	    service = StructureAnalysisService(
   330	        canonical_input_service=fake_canonical_service
   331	    )
   332	
   333	    def fake_compute_dte_min_from_canonical_input(canonical_input):
   334	        return None
   335	
   336	    def fake_compute_payoff_from_canonical_input(canonical_input):
   337	        return {"pl_max": 1.0, "spot_ref": 198.35, "points": []}
   338	
   339	    def fake_compute_decision_from_payoff(
   340	        payoff,
   341	        dte_min,
   342	        spread_pct_medio,
   343	        thresholds,
   344	        dte_gate,
   345	    ):
   346	        return {
   347	            "decision": "HOLD",
   348	            "dte_min": dte_min,
   349	            "why": {},
   350	            "why_json": "{}",
   351	        }
   352	
   353	    monkeypatch.setattr(
   354	        "services.structure_analysis_service.compute_dte_min_from_canonical_input",
   355	        fake_compute_dte_min_from_canonical_input,
   356	    )
   357	    monkeypatch.setattr(
   358	        "services.structure_analysis_service.compute_payoff_from_canonical_input",
   359	        fake_compute_payoff_from_canonical_input,
   360	    )
   361	    monkeypatch.setattr(
   362	        "services.structure_analysis_service.compute_decision_from_payoff",
   363	        fake_compute_decision_from_payoff,
   364	    )
   365	
   366	    result = service.analyze(structure_id=1)
   367	
   368	    assert result["metrics"]["dte_min_inferred"] is None
   369	    assert result["metrics"]["dte_min_effective"] == 0
   370	    assert result["decision"]["dte_min"] == 0
   371	
   372	
   373	def test_structure_analysis_service_explicit_dte_overrides_inferred_value(monkeypatch):
   374	    fake_canonical_service = FakeCanonicalInputService()
   375	    service = StructureAnalysisService(
   376	        canonical_input_service=fake_canonical_service
   377	    )
   378	
   379	    captured = {}
   380	
   381	    def fake_compute_dte_min_from_canonical_input(canonical_input):
   382	        return 2
   383	
   384	    def fake_compute_payoff_from_canonical_input(canonical_input):
   385	        return {"pl_max": 1.0, "spot_ref": 198.35, "points": []}
   386	
   387	    def fake_compute_decision_from_payoff(
   388	        payoff,
   389	        dte_min,
   390	        spread_pct_medio,
   391	        thresholds,
   392	        dte_gate,
   393	    ):
   394	        captured["dte_min"] = dte_min
   395	        return {
   396	            "decision": "HOLD",
   397	            "dte_min": dte_min,
   398	            "why": {},
   399	            "why_json": "{}",
   400	        }
   401	
   402	    monkeypatch.setattr(
   403	        "services.structure_analysis_service.compute_dte_min_from_canonical_input",
   404	        fake_compute_dte_min_from_canonical_input,
   405	    )
   406	    monkeypatch.setattr(
   407	        "services.structure_analysis_service.compute_payoff_from_canonical_input",
   408	        fake_compute_payoff_from_canonical_input,
   409	    )
   410	    monkeypatch.setattr(
   411	        "services.structure_analysis_service.compute_decision_from_payoff",
   412	        fake_compute_decision_from_payoff,
   413	    )
   414	
   415	    result = service.analyze(
   416	        structure_id=1,
   417	        dte_min=9,
   418	    )
   419	
   420	    assert captured["dte_min"] == 9
   421	    assert result["metrics"]["dte_min_inferred"] == 2
   422	    assert result["metrics"]["dte_min_effective"] == 9
   423	    assert result["decision"]["dte_min"] == 9
   424	class FakeCanonicalInputServiceWithMarketMetrics:
   425	    def __init__(self):
   426	        self.calls = []
   427	
   428	    def build_structure_market_input(
   429	        self,
   430	        structure_id: int,
   431	        reference_date: str | None = None,
   432	    ):
   433	        self.calls.append(
   434	            {
   435	                "structure_id": structure_id,
   436	                "reference_date": reference_date,
   437	            }
   438	        )
   439	
   440	        return {
   441	            "structure": {
   442	                "structure_id": structure_id,
   443	                "name": "BOVA11 Condor com Mercado",
   444	                "underlying_asset": "BOVA11",
   445	                "alias_legacy_aba": "BOVA11",
   446	                "legs": [
   447	                    {
   448	                        "position_side": "LONG",
   449	                        "option_type": "PUT",
   450	                        "symbol": "BOVAM190",
   451	                        "strike": 190.0,
   452	                        "expiration_date": "2026-05-20",
   453	                        "quantity": 10,
   454	                        "execution_price": 1.00,
   455	                        "bid": 1.20,
   456	                        "ask": 1.40,
   457	                        "delta": 0.40,
   458	                        "gamma": 0.01,
   459	                        "theta": -0.02,
   460	                        "vega": 0.03,
   461	                        "multiplier": 1.0,
   462	                    },
   463	                    {
   464	                        "position_side": "SHORT",
   465	                        "option_type": "PUT",
   466	                        "symbol": "BOVAM185",
   467	                        "strike": 185.0,
   468	                        "expiration_date": "2026-05-17",
   469	                        "quantity": 10,
   470	                        "execution_price": 1.00,
   471	                        "bid": 0.70,
   472	                        "ask": 0.80,
   473	                        "delta": 0.40,
   474	                        "gamma": 0.01,
   475	                        "theta": -0.02,
   476	                        "vega": 0.03,
   477	                        "multiplier": 1.0,
   478	                    },
   479	                ],
   480	            },
   481	            "market": {
   482	                "reference_date": reference_date or "2026-05-15",
   483	                "underlying_asset": "BOVA11",
   484	                "spot_price": 198.35,
   485	                "interest_rate": 0.1175,
   486	                "volatility": 0.22,
   487	            },
   488	            "meta": {
   489	                "reference_date": reference_date or "2026-05-15",
   490	                "legs_source": "canonical",
   491	                "legacy_aba": "BOVA11",
   492	                "legacy_timestamp": None,
   493	            },
   494	        }
   495	
   496	
   497	def test_structure_analysis_service_infers_spread_pct_medio_from_internal_metrics(monkeypatch):
   498	    service = StructureAnalysisService(
   499	        canonical_input_service=FakeCanonicalInputServiceWithMarketMetrics()
   500	    )
   501	
   502	    captured = {}
   503	
   504	    def fake_compute_payoff_from_canonical_input(canonical_input):
   505	        return {"pl_max": 1.0, "spot_ref": 198.35, "points": []}
   506	
   507	    def fake_compute_decision_from_payoff(
   508	        payoff,
   509	        dte_min,
   510	        spread_pct_medio,
   511	        thresholds,
   512	        dte_gate,
   513	    ):
   514	        captured["spread_pct_medio"] = spread_pct_medio
   515	        return {
   516	            "decision": "HOLD",
   517	            "dte_min": dte_min,
   518	            "why": {},
   519	            "why_json": "{}",
   520	        }
   521	
   522	    monkeypatch.setattr(
   523	        "services.structure_analysis_service.compute_payoff_from_canonical_input",
   524	        fake_compute_payoff_from_canonical_input,
   525	    )
   526	    monkeypatch.setattr(
   527	        "services.structure_analysis_service.compute_decision_from_payoff",
   528	        fake_compute_decision_from_payoff,
   529	    )
   530	
   531	    result = service.analyze(
   532	        structure_id=1,
   533	        reference_date="2026-05-15",
   534	    )
   535	
   536	    expected_spread_pct_medio = ((0.20 / 1.30) + (0.10 / 0.75)) / 2
   537	
   538	    assert result["metrics"]["spread_pct_medio"] == pytest.approx(expected_spread_pct_medio)
   539	    assert result["metrics"]["spread_pct_medio_inferred"] == pytest.approx(expected_spread_pct_medio)
   540	    assert captured["spread_pct_medio"] == pytest.approx(expected_spread_pct_medio)
   541	
   542	
   543	def test_structure_analysis_service_explicit_spread_pct_overrides_internal_metrics(monkeypatch):
   544	    service = StructureAnalysisService(
   545	        canonical_input_service=FakeCanonicalInputServiceWithMarketMetrics()
   546	    )
   547	
   548	    captured = {}
   549	
   550	    def fake_compute_payoff_from_canonical_input(canonical_input):
   551	        return {"pl_max": 1.0, "spot_ref": 198.35, "points": []}
   552	
   553	    def fake_compute_decision_from_payoff(
   554	        payoff,
   555	        dte_min,
   556	        spread_pct_medio,
   557	        thresholds,
   558	        dte_gate,
   559	    ):
   560	        captured["spread_pct_medio"] = spread_pct_medio
   561	        return {
   562	            "decision": "HOLD",
   563	            "dte_min": dte_min,
   564	            "why": {},
   565	            "why_json": "{}",
   566	        }
   567	
   568	    monkeypatch.setattr(
   569	        "services.structure_analysis_service.compute_payoff_from_canonical_input",
   570	        fake_compute_payoff_from_canonical_input,
   571	    )
   572	    monkeypatch.setattr(
   573	        "services.structure_analysis_service.compute_decision_from_payoff",
   574	        fake_compute_decision_from_payoff,
   575	    )
   576	
   577	    result = service.analyze(
   578	        structure_id=1,
   579	        reference_date="2026-05-15",
   580	        spread_pct_medio=0.015,
   581	    )
   582	
   583	    expected_spread_pct_medio_inferred = ((0.20 / 1.30) + (0.10 / 0.75)) / 2
   584	
   585	    assert result["metrics"]["spread_pct_medio"] == 0.015
   586	    assert result["metrics"]["spread_pct_medio_inferred"] == pytest.approx(
   587	        expected_spread_pct_medio_inferred
   588	    )
   589	    assert captured["spread_pct_medio"] == 0.015
   590	
   591	
   592	def test_structure_analysis_service_exposes_internal_structure_metrics(monkeypatch):
   593	    service = StructureAnalysisService(
   594	        canonical_input_service=FakeCanonicalInputServiceWithMarketMetrics()
   595	    )
   596	
   597	    def fake_compute_payoff_from_canonical_input(canonical_input):
   598	        return {"pl_max": 1.0, "spot_ref": 198.35, "points": []}
   599	
   600	    def fake_compute_decision_from_payoff(
   601	        payoff,
   602	        dte_min,
   603	        spread_pct_medio,
   604	        thresholds,
   605	        dte_gate,
   606	    ):
   607	        return {
   608	            "decision": "HOLD",
   609	            "dte_min": dte_min,
   610	            "why": {},
   611	            "why_json": "{}",
   612	        }
   613	
   614	    monkeypatch.setattr(
   615	        "services.structure_analysis_service.compute_payoff_from_canonical_input",
   616	        fake_compute_payoff_from_canonical_input,
   617	    )
   618	    monkeypatch.setattr(
   619	        "services.structure_analysis_service.compute_decision_from_payoff",
   620	        fake_compute_decision_from_payoff,
   621	    )
   622	
   623	    result = service.analyze(
   624	        structure_id=1,
   625	        reference_date="2026-05-15",
   626	    )
   627	
   628	    structure_metrics = result["metrics"]["structure_metrics"]
   629	
   630	    assert structure_metrics["num_pernas"] == 2
   631	    assert structure_metrics["pl_realista_total"] == pytest.approx(4.0)
   632	    assert structure_metrics["delta_liq"] == pytest.approx(0.0)
   633	    assert structure_metrics["gamma_liq"] == pytest.approx(0.0)
   634	    assert structure_metrics["theta_liq"] == pytest.approx(0.0)
   635	    assert structure_metrics["vega_liq"] == pytest.approx(0.0)
   636	    assert structure_metrics["dte_min"] == 2
   637	    assert len(structure_metrics["legs"]) == 2
```

## FILE: ATT/tests/test_derived_service.py
```python
     1	from datetime import datetime
     2	
     3	import services.derived_service as ds
     4	
     5	
     6	def test_now_iso_should_be_parseable_and_timezone_aware():
     7	    value = ds._now_iso()
     8	    parsed = datetime.fromisoformat(value)
     9	
    10	    assert parsed.tzinfo is not None
    11	
    12	
    13	def test_resolve_storage_key_should_prefer_aba_when_present():
    14	    result = ds._resolve_storage_key(
    15	        aba="BOVA11",
    16	        structure_id=7,
    17	        structure_name="BOVA11 Condor Maio/2026",
    18	        underlying_asset="BOVA11",
    19	    )
    20	
    21	    assert result == "BOVA11"
    22	
    23	
    24	def test_resolve_storage_key_should_fallback_to_structure_id():
    25	    result = ds._resolve_storage_key(
    26	        aba=None,
    27	        structure_id=7,
    28	        structure_name="BOVA11 Condor Maio/2026",
    29	        underlying_asset="BOVA11",
    30	    )
    31	
    32	    assert result == "structure:7"
    33	
    34	
    35	def test_resolve_storage_key_should_use_structure_name_when_id_missing():
    36	    result = ds._resolve_storage_key(
    37	        aba=None,
    38	        structure_id=None,
    39	        structure_name="Trava XYZ",
    40	        underlying_asset="PETR4",
    41	    )
    42	
    43	    assert result == "Trava XYZ"
    44	
    45	
    46	def test_resolve_storage_key_should_use_underlying_asset_as_last_named_key():
    47	    result = ds._resolve_storage_key(
    48	        aba=None,
    49	        structure_id=None,
    50	        structure_name=None,
    51	        underlying_asset="PETR4",
    52	    )
    53	
    54	    assert result == "PETR4"
    55	
    56	
    57	def test_resolve_storage_key_should_return_unknown_when_all_missing():
    58	    result = ds._resolve_storage_key(
    59	        aba=None,
    60	        structure_id=None,
    61	        structure_name=None,
    62	        underlying_asset=None,
    63	    )
    64	
    65	    assert result == "unknown"
    66	
    67	
    68	def test_merge_meta_should_enrich_with_canonical_identity():
    69	    result = ds._merge_meta(
    70	        meta={"origin": "test"},
    71	        structure_id=7,
    72	        structure_name="BOVA11 Condor Maio/2026",
    73	        underlying_asset="BOVA11",
    74	        reference_date="2026-05-18",
    75	        input_meta={"legs_source": "canonical"},
    76	    )
    77	
    78	    assert result["origin"] == "test"
    79	    assert result["structure_id"] == 7
    80	    assert result["structure_name"] == "BOVA11 Condor Maio/2026"
    81	    assert result["underlying_asset"] == "BOVA11"
    82	    assert result["reference_date"] == "2026-05-18"
    83	    assert result["input_meta"]["legs_source"] == "canonical"
    84	
    85	
    86	def test_save_payoff_from_canonical_payload_should_use_resolved_storage_key(monkeypatch):
    87	    captured = {}
    88	
    89	    def fake_save_payoff_curve(ref, points, spot_ref=None, meta=None, timestamp=None):
    90	        captured["aba"] = ref
    91	        captured["points"] = points
    92	        captured["spot_ref"] = spot_ref
    93	        captured["meta"] = meta
    94	        captured["timestamp"] = timestamp
    95	        return 777
    96	
    97	    monkeypatch.setattr(ds, "save_payoff_curve", fake_save_payoff_curve)
    98	
    99	    payload = {
   100	        "structure_id": 99,
   101	        "structure_name": "Iron Condor",
   102	        "underlying_asset": "PETR4",
   103	        "reference_date": "2026-05-19",
   104	        "input_meta": {"x": 1},
   105	        "meta": {"source": "test"},
   106	        "points": [{"point_spot": 10, "point_pl": 20}],
   107	        "spot_ref": 11.5,
   108	    }
   109	
   110	    result = ds.save_payoff_from_canonical_payload(payload)
   111	
   112	    assert result == 777
   113	    assert captured["aba"] == "structure:99"
   114	    assert captured["points"] == [{"point_spot": 10, "point_pl": 20}]
   115	    assert captured["spot_ref"] == 11.5
   116	    assert captured["meta"]["source"] == "test"
   117	    assert captured["meta"]["structure_id"] == 99
   118	    assert captured["meta"]["structure_name"] == "Iron Condor"
   119	    assert captured["meta"]["underlying_asset"] == "PETR4"
   120	    assert captured["meta"]["reference_date"] == "2026-05-19"
   121	    assert captured["meta"]["input_meta"] == {"x": 1}
   122	    assert captured["meta"]["storage_key"] == "structure:99"
   123	
   124	
   125	def test_save_decision_from_canonical_payload_should_enrich_meta(monkeypatch):
   126	    captured = {}
   127	
   128	    def fake_save_decision(ref, decision, timestamp=None):
   129	        captured["aba"] = ref
   130	        captured["decision"] = decision
   131	        captured["timestamp"] = timestamp
   132	        return 888
   133	
   134	    monkeypatch.setattr(ds, "save_decision", fake_save_decision)
   135	
   136	    payload = {
   137	        "action": "hold",
   138	        "meta": {"origin": "test"},
   139	    }
   140	
   141	    result = ds.save_decision_from_canonical_payload(
   142	        decision=payload,
   143	        structure_id=321,
   144	        structure_name="Fence",
   145	        underlying_asset="VALE3",
   146	        aba=None,
   147	    )
   148	
   149	    assert result == 888
   150	    assert captured["aba"] == "structure:321"
   151	    assert captured["decision"]["meta"]["origin"] == "test"
   152	    assert captured["decision"]["meta"]["structure_id"] == 321
   153	    assert captured["decision"]["meta"]["structure_name"] == "Fence"
   154	    assert captured["decision"]["meta"]["underlying_asset"] == "VALE3"
   155	    assert captured["decision"]["meta"]["storage_key"] == "structure:321"
   156	
   157	# FASE_3A4_TESTS_DERIVED_SERVICE
   158	
   159	def test_save_decision_preserva_structure_id_explicito_sem_alias(monkeypatch):
   160	    import services.derived_service as svc
   161	
   162	    captured = {}
   163	
   164	    class FakeConn:
   165	        def __enter__(self):
   166	            return self
   167	
   168	        def __exit__(self, exc_type, exc, tb):
   169	            return False
   170	
   171	    def fake_insert_structure_decision(conn, timestamp, aba, decision_dict):
   172	        captured["timestamp"] = timestamp
   173	        captured["aba"] = aba
   174	        captured["decision_dict"] = decision_dict
   175	        return 1
   176	
   177	    monkeypatch.setattr(svc, "connect_derived", lambda: FakeConn())
   178	    monkeypatch.setattr(svc, "ensure_derived_tables", lambda conn: None)
   179	    monkeypatch.setattr(svc, "_resolve_structure_id", lambda storage_key: None)
   180	    monkeypatch.setattr(svc, "insert_structure_decision", fake_insert_structure_decision)
   181	
   182	    result = svc.save_decision(
   183	        ref="structure:7",
   184	        decision={
   185	            "structure_id": 7,
   186	            "decision": "hold",
   187	            "meta": {"source": "test"},
   188	        },
   189	        timestamp="2026-06-21T00:00:00+00:00",
   190	    )
   191	
   192	    assert result == 1
   193	    assert captured["aba"] == "structure:7"
   194	    assert captured["decision_dict"]["structure_id"] == 7
   195	    assert captured["decision_dict"]["meta"]["structure_id"] == 7
   196	    assert captured["decision_dict"]["meta"]["storage_key"] == "structure:7"
```

## FILE: ATT/tests/test_payoff_canonical.py
```python
     1	from domain.payoff import compute_payoff_from_canonical_input
     2	
     3	
     4	def test_compute_payoff_from_canonical_input_should_preserve_canonical_metadata():
     5	    canonical_input = {
     6	        "structure": {
     7	            "structure_id": 7,
     8	            "name": "BOVA11 Condor Maio/2026",
     9	            "underlying_asset": "BOVA11",
    10	            "legs": [
    11	                {
    12	                    "position_side": "LONG",
    13	                    "option_type": "CALL",
    14	                    "symbol": "BOVAE195",
    15	                    "strike": 195.0,
    16	                    "expiration_date": "2026-05-15",
    17	                    "quantity": 1,
    18	                    "premium": 2.0,
    19	                    "multiplier": 1.0,
    20	                }
    21	            ],
    22	        },
    23	        "market": {
    24	            "reference_date": "2026-05-18",
    25	            "underlying_asset": "BOVA11",
    26	            "spot_price": 198.35,
    27	            "interest_rate": 0.1175,
    28	            "volatility": 0.22,
    29	        },
    30	        "meta": {
    31	            "reference_date": "2026-05-18",
    32	            "legs_source": "canonical",
    33	            "input_source": "test",
    34	        },
    35	    }
    36	
    37	    result = compute_payoff_from_canonical_input(canonical_input)
    38	
    39	    assert result["structure_id"] == 7
    40	    assert result["structure_name"] == "BOVA11 Condor Maio/2026"
    41	    assert result["underlying_asset"] == "BOVA11"
    42	    assert result["reference_date"] == "2026-05-18"
    43	    assert result["input_meta"]["legs_source"] == "canonical"
```

## FILE: ATT/tests/test_decision.py
```python
     1	from domain.decision import compute_decision_from_payoff
     2	
     3	
     4	def test_compute_decision_from_payoff_should_work_without_alias_legacy_aba():
     5	    """
     6	    Garante que compute_decision_from_payoff funciona com payoff canônico
     7	    que não carrega alias_legacy_aba -- substitui o teste de contract com dict.
     8	    """
     9	    payoff = {
    10	        "pl_atual": 120.0,
    11	        "pl_max":   200.0,
    12	        "pl_min":   -50.0,
    13	        "points":   [],
    14	        "spot":     198.35,
    15	    }
    16	
    17	    result = compute_decision_from_payoff(
    18	        payoff=payoff,
    19	        dte_min=12,
    20	    )
    21	
    22	    assert "decision" in result
    23	    assert "why" in result
    24	    assert result["decision"] in ("HOLD", "WATCH", "PREPARE", "PREPARE_ROLL", "CLOSE_REOPEN", "CLOSE")
    25	    # dte_min é registrado no why quando DTE gate é ativado
    26	    # com dte_min=12 > dte_gate=7 não há gate, decisão depende do ratio
    27	    assert isinstance(result.get("why"), dict)
```

## Testes focalizados existentes
.......................FFFFFFFFFFFF.............................         [100%]
================================== FAILURES ===================================
______ test_build_legs_payload_normaliza_position_side_legado_long_short ______

    def test_build_legs_payload_normaliza_position_side_legado_long_short():
        dlg = object.__new__(StructureEditorDialog)
        dlg._legs_rows = [
            {
                "position_side": "LONG",
                "option_type": "CALL",
                "strike": 100.0,
                "expiration_date": "2026-12-18",
                "quantity": 1,
                "premium": None,
                "multiplier": 1,
                "symbol": "TESTC100",
                "notes": None,
            },
            {
                "position_side": "SHORT",
                "option_type": "PUT",
                "strike": 90.0,
                "expiration_date": "2026-12-18",
                "quantity": 2,
                "premium": None,
                "multiplier": 1,
                "symbol": "TESTP90",
                "notes": None,
            },
        ]
    
>       payload = dlg._build_legs_payload()
                  ^^^^^^^^^^^^^^^^^^^^^^^^^

ATT\tests\test_structure_editor_dialog.py:463: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
UI\components\structure_editor_dialog.py:591: in _build_legs_payload
    row = self._enrich_leg_data_from_symbol(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <UI.components.structure_editor_dialog.StructureEditorDialog object at 0x0000024239198490>
leg_data = {'expiration_date': '2026-12-18', 'multiplier': 1, 'notes': None, 'option_type': 'CALL', ...}

    def _enrich_leg_data_from_symbol(
        self,
        leg_data: dict,
        *,
        require_quote: bool,
    ) -> dict:
        """Enriquece uma leg por symbol/codigo_opcao quando informado.
    
        require_quote=True:
            usado no botao/aplicar leg; symbol invalido bloqueia.
    
        require_quote=False:
            usado no save/build payload; se a leg manual ja esta completa e a
            cotacao nao existe, preserva compatibilidade.
        """
        symbol = str(leg_data.get("symbol") or leg_data.get("codigo_opcao") or "").strip()
        if not symbol:
            return leg_data
    
        try:
>           enriched = self._get_leg_enrichment_service().enrich(leg_data)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           AttributeError: 'function' object has no attribute 'enrich'

UI\components\structure_editor_dialog.py:421: AttributeError
_______ test_build_legs_payload_normaliza_strike_com_virgula_para_float _______

    def test_build_legs_payload_normaliza_strike_com_virgula_para_float():
        dlg = object.__new__(StructureEditorDialog)
        dlg._legs_rows = [
            {
                "position_side": "COMPRADO",
                "option_type": "CALL",
                "strike": "100,00",
                "expiration_date": "2026-12-18",
                "quantity": 1,
                "premium": None,
                "multiplier": 1,
                "symbol": "TESTC100",
                "notes": None,
            }
        ]
    
>       payload = dlg._build_legs_payload()
                  ^^^^^^^^^^^^^^^^^^^^^^^^^

ATT\tests\test_structure_editor_dialog.py:486: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
UI\components\structure_editor_dialog.py:591: in _build_legs_payload
    row = self._enrich_leg_data_from_symbol(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <UI.components.structure_editor_dialog.StructureEditorDialog object at 0x0000024239198AF0>
leg_data = {'expiration_date': '2026-12-18', 'multiplier': 1, 'notes': None, 'option_type': 'CALL', ...}

    def _enrich_leg_data_from_symbol(
        self,
        leg_data: dict,
        *,
        require_quote: bool,
    ) -> dict:
        """Enriquece uma leg por symbol/codigo_opcao quando informado.
    
        require_quote=True:
            usado no botao/aplicar leg; symbol invalido bloqueia.
    
        require_quote=False:
            usado no save/build payload; se a leg manual ja esta completa e a
            cotacao nao existe, preserva compatibilidade.
        """
        symbol = str(leg_data.get("symbol") or leg_data.get("codigo_opcao") or "").strip()
        if not symbol:
            return leg_data
    
        try:
>           enriched = self._get_leg_enrichment_service().enrich(leg_data)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           AttributeError: 'function' object has no attribute 'enrich'

UI\components\structure_editor_dialog.py:421: AttributeError
________ test_build_legs_payload_normaliza_strike_com_ponto_para_float ________

    def test_build_legs_payload_normaliza_strike_com_ponto_para_float():
        dlg = object.__new__(StructureEditorDialog)
        dlg._legs_rows = [
            {
                "position_side": "COMPRADO",
                "option_type": "CALL",
                "strike": "100.50",
                "expiration_date": "2026-12-18",
                "quantity": 1,
                "premium": None,
                "multiplier": 1,
                "symbol": "TESTC100",
                "notes": None,
            }
        ]
    
>       payload = dlg._build_legs_payload()
                  ^^^^^^^^^^^^^^^^^^^^^^^^^

ATT\tests\test_structure_editor_dialog.py:508: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
UI\components\structure_editor_dialog.py:591: in _build_legs_payload
    row = self._enrich_leg_data_from_symbol(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <UI.components.structure_editor_dialog.StructureEditorDialog object at 0x00000242391989E0>
leg_data = {'expiration_date': '2026-12-18', 'multiplier': 1, 'notes': None, 'option_type': 'CALL', ...}

    def _enrich_leg_data_from_symbol(
        self,
        leg_data: dict,
        *,
        require_quote: bool,
    ) -> dict:
        """Enriquece uma leg por symbol/codigo_opcao quando informado.
    
        require_quote=True:
            usado no botao/aplicar leg; symbol invalido bloqueia.
    
        require_quote=False:
            usado no save/build payload; se a leg manual ja esta completa e a
            cotacao nao existe, preserva compatibilidade.
        """
        symbol = str(leg_data.get("symbol") or leg_data.get("codigo_opcao") or "").strip()
        if not symbol:
            return leg_data
    
        try:
>           enriched = self._get_leg_enrichment_service().enrich(leg_data)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           AttributeError: 'function' object has no attribute 'enrich'

UI\components\structure_editor_dialog.py:421: AttributeError
_____ test_build_legs_payload_nao_modifica_strike_original_ao_normalizar ______

    def test_build_legs_payload_nao_modifica_strike_original_ao_normalizar():
        dlg = object.__new__(StructureEditorDialog)
        original_leg = {
            "position_side": "COMPRADO",
            "option_type": "CALL",
            "strike": "100,00",
            "expiration_date": "2026-12-18",
            "quantity": 1,
            "premium": None,
            "multiplier": 1,
            "symbol": "TESTC100",
            "notes": None,
        }
        dlg._legs_rows = [original_leg]
    
>       payload = dlg._build_legs_payload()
                  ^^^^^^^^^^^^^^^^^^^^^^^^^

ATT\tests\test_structure_editor_dialog.py:529: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
UI\components\structure_editor_dialog.py:591: in _build_legs_payload
    row = self._enrich_leg_data_from_symbol(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <UI.components.structure_editor_dialog.StructureEditorDialog object at 0x0000024239199040>
leg_data = {'expiration_date': '2026-12-18', 'multiplier': 1, 'notes': None, 'option_type': 'CALL', ...}

    def _enrich_leg_data_from_symbol(
        self,
        leg_data: dict,
        *,
        require_quote: bool,
    ) -> dict:
        """Enriquece uma leg por symbol/codigo_opcao quando informado.
    
        require_quote=True:
            usado no botao/aplicar leg; symbol invalido bloqueia.
    
        require_quote=False:
            usado no save/build payload; se a leg manual ja esta completa e a
            cotacao nao existe, preserva compatibilidade.
        """
        symbol = str(leg_data.get("symbol") or leg_data.get("codigo_opcao") or "").strip()
        if not symbol:
            return leg_data
    
        try:
>           enriched = self._get_leg_enrichment_service().enrich(leg_data)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           AttributeError: 'function' object has no attribute 'enrich'

UI\components\structure_editor_dialog.py:421: AttributeError
______ test_build_legs_payload_normaliza_premium_com_virgula_para_float _______

    def test_build_legs_payload_normaliza_premium_com_virgula_para_float():
        dlg = object.__new__(StructureEditorDialog)
        dlg._legs_rows = [
            {
                "position_side": "COMPRADO",
                "option_type": "CALL",
                "strike": "100,00",
                "expiration_date": "2026-12-18",
                "quantity": 1,
                "premium": "1,25",
                "multiplier": 1,
                "symbol": "TESTC100",
                "notes": None,
            }
        ]
    
>       payload = dlg._build_legs_payload()
                  ^^^^^^^^^^^^^^^^^^^^^^^^^

ATT\tests\test_structure_editor_dialog.py:552: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
UI\components\structure_editor_dialog.py:591: in _build_legs_payload
    row = self._enrich_leg_data_from_symbol(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <UI.components.structure_editor_dialog.StructureEditorDialog object at 0x0000024238F9E250>
leg_data = {'expiration_date': '2026-12-18', 'multiplier': 1, 'notes': None, 'option_type': 'CALL', ...}

    def _enrich_leg_data_from_symbol(
        self,
        leg_data: dict,
        *,
        require_quote: bool,
    ) -> dict:
        """Enriquece uma leg por symbol/codigo_opcao quando informado.
    
        require_quote=True:
            usado no botao/aplicar leg; symbol invalido bloqueia.
    
        require_quote=False:
            usado no save/build payload; se a leg manual ja esta completa e a
            cotacao nao existe, preserva compatibilidade.
        """
        symbol = str(leg_data.get("symbol") or leg_data.get("codigo_opcao") or "").strip()
        if not symbol:
            return leg_data
    
        try:
>           enriched = self._get_leg_enrichment_service().enrich(leg_data)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           AttributeError: 'function' object has no attribute 'enrich'

UI\components\structure_editor_dialog.py:421: AttributeError
_____ test_build_legs_payload_normaliza_multiplier_com_virgula_para_float _____

    def test_build_legs_payload_normaliza_multiplier_com_virgula_para_float():
        dlg = object.__new__(StructureEditorDialog)
        dlg._legs_rows = [
            {
                "position_side": "COMPRADO",
                "option_type": "CALL",
                "strike": "100,00",
                "expiration_date": "2026-12-18",
                "quantity": 1,
                "premium": None,
                "multiplier": "100,0",
                "symbol": "TESTC100",
                "notes": None,
            }
        ]
    
>       payload = dlg._build_legs_payload()
                  ^^^^^^^^^^^^^^^^^^^^^^^^^

ATT\tests\test_structure_editor_dialog.py:574: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
UI\components\structure_editor_dialog.py:591: in _build_legs_payload
    row = self._enrich_leg_data_from_symbol(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <UI.components.structure_editor_dialog.StructureEditorDialog object at 0x0000024239199370>
leg_data = {'expiration_date': '2026-12-18', 'multiplier': '100,0', 'notes': None, 'option_type': 'CALL', ...}

    def _enrich_leg_data_from_symbol(
        self,
        leg_data: dict,
        *,
        require_quote: bool,
    ) -> dict:
        """Enriquece uma leg por symbol/codigo_opcao quando informado.
    
        require_quote=True:
            usado no botao/aplicar leg; symbol invalido bloqueia.
    
        require_quote=False:
            usado no save/build payload; se a leg manual ja esta completa e a
            cotacao nao existe, preserva compatibilidade.
        """
        symbol = str(leg_data.get("symbol") or leg_data.get("codigo_opcao") or "").strip()
        if not symbol:
            return leg_data
    
        try:
>           enriched = self._get_leg_enrichment_service().enrich(leg_data)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           AttributeError: 'function' object has no attribute 'enrich'

UI\components\structure_editor_dialog.py:421: AttributeError
________________ test_build_legs_payload_preserva_premium_none ________________

    def test_build_legs_payload_preserva_premium_none():
        dlg = object.__new__(StructureEditorDialog)
        dlg._legs_rows = [
            {
                "position_side": "COMPRADO",
                "option_type": "CALL",
                "strike": "100,00",
                "expiration_date": "2026-12-18",
                "quantity": 1,
                "premium": None,
                "multiplier": 1,
                "symbol": "TESTC100",
                "notes": None,
            }
        ]
    
>       payload = dlg._build_legs_payload()
                  ^^^^^^^^^^^^^^^^^^^^^^^^^

ATT\tests\test_structure_editor_dialog.py:596: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
UI\components\structure_editor_dialog.py:591: in _build_legs_payload
    row = self._enrich_leg_data_from_symbol(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <UI.components.structure_editor_dialog.StructureEditorDialog object at 0x00000242391996A0>
leg_data = {'expiration_date': '2026-12-18', 'multiplier': 1, 'notes': None, 'option_type': 'CALL', ...}

    def _enrich_leg_data_from_symbol(
        self,
        leg_data: dict,
        *,
        require_quote: bool,
    ) -> dict:
        """Enriquece uma leg por symbol/codigo_opcao quando informado.
    
        require_quote=True:
            usado no botao/aplicar leg; symbol invalido bloqueia.
    
        require_quote=False:
            usado no save/build payload; se a leg manual ja esta completa e a
            cotacao nao existe, preserva compatibilidade.
        """
        symbol = str(leg_data.get("symbol") or leg_data.get("codigo_opcao") or "").strip()
        if not symbol:
            return leg_data
    
        try:
>           enriched = self._get_leg_enrichment_service().enrich(leg_data)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           AttributeError: 'function' object has no attribute 'enrich'

UI\components\structure_editor_dialog.py:421: AttributeError
________ test_build_legs_payload_normaliza_quantity_inteiro_valido[1] _________

quantity_value = '1'

    @pytest.mark.parametrize("quantity_value", ["1", "1,0", "1.0"])
    def test_build_legs_payload_normaliza_quantity_inteiro_valido(quantity_value):
        dlg = _dlg_com_quantity_para_teste(quantity_value)
    
>       payload = dlg._build_legs_payload()
                  ^^^^^^^^^^^^^^^^^^^^^^^^^

ATT\tests\test_structure_editor_dialog.py:627: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
UI\components\structure_editor_dialog.py:591: in _build_legs_payload
    row = self._enrich_leg_data_from_symbol(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <UI.components.structure_editor_dialog.StructureEditorDialog object at 0x0000024239199D00>
leg_data = {'expiration_date': '2026-12-18', 'multiplier': 1, 'notes': None, 'option_type': 'CALL', ...}

    def _enrich_leg_data_from_symbol(
        self,
        leg_data: dict,
        *,
        require_quote: bool,
    ) -> dict:
        """Enriquece uma leg por symbol/codigo_opcao quando informado.
    
        require_quote=True:
            usado no botao/aplicar leg; symbol invalido bloqueia.
    
        require_quote=False:
            usado no save/build payload; se a leg manual ja esta completa e a
            cotacao nao existe, preserva compatibilidade.
        """
        symbol = str(leg_data.get("symbol") or leg_data.get("codigo_opcao") or "").strip()
        if not symbol:
            return leg_data
    
        try:
>           enriched = self._get_leg_enrichment_service().enrich(leg_data)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           AttributeError: 'function' object has no attribute 'enrich'

UI\components\structure_editor_dialog.py:421: AttributeError
_______ test_build_legs_payload_normaliza_quantity_inteiro_valido[1,0] ________

quantity_value = '1,0'

    @pytest.mark.parametrize("quantity_value", ["1", "1,0", "1.0"])
    def test_build_legs_payload_normaliza_quantity_inteiro_valido(quantity_value):
        dlg = _dlg_com_quantity_para_teste(quantity_value)
    
>       payload = dlg._build_legs_payload()
                  ^^^^^^^^^^^^^^^^^^^^^^^^^

ATT\tests\test_structure_editor_dialog.py:627: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
UI\components\structure_editor_dialog.py:591: in _build_legs_payload
    row = self._enrich_leg_data_from_symbol(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <UI.components.structure_editor_dialog.StructureEditorDialog object at 0x000002423919A360>
leg_data = {'expiration_date': '2026-12-18', 'multiplier': 1, 'notes': None, 'option_type': 'CALL', ...}

    def _enrich_leg_data_from_symbol(
        self,
        leg_data: dict,
        *,
        require_quote: bool,
    ) -> dict:
        """Enriquece uma leg por symbol/codigo_opcao quando informado.
    
        require_quote=True:
            usado no botao/aplicar leg; symbol invalido bloqueia.
    
        require_quote=False:
            usado no save/build payload; se a leg manual ja esta completa e a
            cotacao nao existe, preserva compatibilidade.
        """
        symbol = str(leg_data.get("symbol") or leg_data.get("codigo_opcao") or "").strip()
        if not symbol:
            return leg_data
    
        try:
>           enriched = self._get_leg_enrichment_service().enrich(leg_data)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           AttributeError: 'function' object has no attribute 'enrich'

UI\components\structure_editor_dialog.py:421: AttributeError
_______ test_build_legs_payload_normaliza_quantity_inteiro_valido[1.0] ________

quantity_value = '1.0'

    @pytest.mark.parametrize("quantity_value", ["1", "1,0", "1.0"])
    def test_build_legs_payload_normaliza_quantity_inteiro_valido(quantity_value):
        dlg = _dlg_com_quantity_para_teste(quantity_value)
    
>       payload = dlg._build_legs_payload()
                  ^^^^^^^^^^^^^^^^^^^^^^^^^

ATT\tests\test_structure_editor_dialog.py:627: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
UI\components\structure_editor_dialog.py:591: in _build_legs_payload
    row = self._enrich_leg_data_from_symbol(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <UI.components.structure_editor_dialog.StructureEditorDialog object at 0x0000024239199BF0>
leg_data = {'expiration_date': '2026-12-18', 'multiplier': 1, 'notes': None, 'option_type': 'CALL', ...}

    def _enrich_leg_data_from_symbol(
        self,
        leg_data: dict,
        *,
        require_quote: bool,
    ) -> dict:
        """Enriquece uma leg por symbol/codigo_opcao quando informado.
    
        require_quote=True:
            usado no botao/aplicar leg; symbol invalido bloqueia.
    
        require_quote=False:
            usado no save/build payload; se a leg manual ja esta completa e a
            cotacao nao existe, preserva compatibilidade.
        """
        symbol = str(leg_data.get("symbol") or leg_data.get("codigo_opcao") or "").strip()
        if not symbol:
            return leg_data
    
        try:
>           enriched = self._get_leg_enrichment_service().enrich(leg_data)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           AttributeError: 'function' object has no attribute 'enrich'

UI\components\structure_editor_dialog.py:421: AttributeError
___________ test_build_legs_payload_rejeita_quantity_invalido[1,5] ____________

quantity_value = '1,5'

    @pytest.mark.parametrize("quantity_value", ["1,5", "abc"])
    def test_build_legs_payload_rejeita_quantity_invalido(quantity_value):
        dlg = _dlg_com_quantity_para_teste(quantity_value)
    
        with pytest.raises(
            (ValueError, TypeError),
            match=r"(?i)(quantity|quantidade|inteiro|integer|invalid|inv[a�]lid)",
        ):
>           dlg._build_legs_payload()

ATT\tests\test_structure_editor_dialog.py:641: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
UI\components\structure_editor_dialog.py:591: in _build_legs_payload
    row = self._enrich_leg_data_from_symbol(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <UI.components.structure_editor_dialog.StructureEditorDialog object at 0x000002423919A030>
leg_data = {'expiration_date': '2026-12-18', 'multiplier': 1, 'notes': None, 'option_type': 'CALL', ...}

    def _enrich_leg_data_from_symbol(
        self,
        leg_data: dict,
        *,
        require_quote: bool,
    ) -> dict:
        """Enriquece uma leg por symbol/codigo_opcao quando informado.
    
        require_quote=True:
            usado no botao/aplicar leg; symbol invalido bloqueia.
    
        require_quote=False:
            usado no save/build payload; se a leg manual ja esta completa e a
            cotacao nao existe, preserva compatibilidade.
        """
        symbol = str(leg_data.get("symbol") or leg_data.get("codigo_opcao") or "").strip()
        if not symbol:
            return leg_data
    
        try:
>           enriched = self._get_leg_enrichment_service().enrich(leg_data)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           AttributeError: 'function' object has no attribute 'enrich'

UI\components\structure_editor_dialog.py:421: AttributeError
___________ test_build_legs_payload_rejeita_quantity_invalido[abc] ____________

quantity_value = 'abc'

    @pytest.mark.parametrize("quantity_value", ["1,5", "abc"])
    def test_build_legs_payload_rejeita_quantity_invalido(quantity_value):
        dlg = _dlg_com_quantity_para_teste(quantity_value)
    
        with pytest.raises(
            (ValueError, TypeError),
            match=r"(?i)(quantity|quantidade|inteiro|integer|invalid|inv[a�]lid)",
        ):
>           dlg._build_legs_payload()

ATT\tests\test_structure_editor_dialog.py:641: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
UI\components\structure_editor_dialog.py:591: in _build_legs_payload
    row = self._enrich_leg_data_from_symbol(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <UI.components.structure_editor_dialog.StructureEditorDialog object at 0x00000242391998C0>
leg_data = {'expiration_date': '2026-12-18', 'multiplier': 1, 'notes': None, 'option_type': 'CALL', ...}

    def _enrich_leg_data_from_symbol(
        self,
        leg_data: dict,
        *,
        require_quote: bool,
    ) -> dict:
        """Enriquece uma leg por symbol/codigo_opcao quando informado.
    
        require_quote=True:
            usado no botao/aplicar leg; symbol invalido bloqueia.
    
        require_quote=False:
            usado no save/build payload; se a leg manual ja esta completa e a
            cotacao nao existe, preserva compatibilidade.
        """
        symbol = str(leg_data.get("symbol") or leg_data.get("codigo_opcao") or "").strip()
        if not symbol:
            return leg_data
    
        try:
>           enriched = self._get_leg_enrichment_service().enrich(leg_data)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           AttributeError: 'function' object has no attribute 'enrich'

UI\components\structure_editor_dialog.py:421: AttributeError
=========================== short test summary info ===========================
FAILED ATT/tests/test_structure_editor_dialog.py::test_build_legs_payload_normaliza_position_side_legado_long_short
FAILED ATT/tests/test_structure_editor_dialog.py::test_build_legs_payload_normaliza_strike_com_virgula_para_float
FAILED ATT/tests/test_structure_editor_dialog.py::test_build_legs_payload_normaliza_strike_com_ponto_para_float
FAILED ATT/tests/test_structure_editor_dialog.py::test_build_legs_payload_nao_modifica_strike_original_ao_normalizar
FAILED ATT/tests/test_structure_editor_dialog.py::test_build_legs_payload_normaliza_premium_com_virgula_para_float
FAILED ATT/tests/test_structure_editor_dialog.py::test_build_legs_payload_normaliza_multiplier_com_virgula_para_float
FAILED ATT/tests/test_structure_editor_dialog.py::test_build_legs_payload_preserva_premium_none
FAILED ATT/tests/test_structure_editor_dialog.py::test_build_legs_payload_normaliza_quantity_inteiro_valido[1]
FAILED ATT/tests/test_structure_editor_dialog.py::test_build_legs_payload_normaliza_quantity_inteiro_valido[1,0]
FAILED ATT/tests/test_structure_editor_dialog.py::test_build_legs_payload_normaliza_quantity_inteiro_valido[1.0]
FAILED ATT/tests/test_structure_editor_dialog.py::test_build_legs_payload_rejeita_quantity_invalido[1,5]
FAILED ATT/tests/test_structure_editor_dialog.py::test_build_legs_payload_rejeita_quantity_invalido[abc]
12 failed, 52 passed in 1.16s
