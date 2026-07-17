# Relatório 32.2 - Diagnóstico do gap de persistência de payoff

- Gerado em: `2026-07-17T19:55:38`
- Branch: `payoff-centro-verdade-32`

## 1. Leitura do problema

O teste anterior indicou que o pricing executa e snapshot incrementa, mas `payoff_curve_points` e `structure_decisions` não aumentam.

Isso aponta para falha depois da execução do pricing e antes/durante a persistência derivada.

## 2. Arquivos encontrados por token

### `.local_artifacts/debug_tools/ui_flow_trace.py`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L91: `"rtd_option_quotes;structure_legs;payoff_curve_points;structure_snapshots;pricing_executions;structure_leg_snapshots;structure_decisions",`

### `ATT/database_retention_simulation_service.py`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L10: `"payoff_curve_points": ("timestamp", "created_at"),`
- L20: `"structure_decisions": "decisoes operacionais exigem auditoria semantica",`

### `ATT/operational_observability_service.py`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L14: `"payoff_curve_points",`

### `ATT/patches/fase6_auditoria_baseline_20260713.md`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L37: `- table: payoff_curve_points`
- L45: `- table: structure_decisions`

### `ATT/tests/check_cleanup_residuals.py`

Tokens:
- `derived_payoff`

Linhas relevantes:
- L76: `"scripts/patch_derived_payoff_timestamp_consistency.sh",`

### `ATT/tests/test_bd_unico_absorcao_funcional.py`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L18: `"payoff_curve_points",`
- L19: `"structure_decisions",`
- L48: `"payoff_curve_points": {`
- L58: `"structure_decisions": {`
- L119: `"idx_structure_decisions_sid_ts",`
- L274: `FROM payoff_curve_points`
- L283: `FROM structure_decisions`

### `ATT/tests/test_bd_unico_artifacts_in_app_db.py`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L28: `"payoff_curve_points",`
- L29: `"structure_decisions",`
- L135: `assert "payoff_curve_points" in tables, (`
- L136: `"A tabela canonica payoff_curve_points deve existir em dados/app.db."`
- L139: `cols = _sqlite_columns(APP_DB, "payoff_curve_points")`
- L143: `"payoff_curve_points em dados/app.db nao possui colunas canonicas "`
- L209: `assert "payoff_curve_points" in ui_text, (`
- L210: `"UI/models/ui_data.py deve reconhecer payoff_curve_points como tabela "`
- L223: `assert "payoff_curve_points" in details_text, (`
- L224: `"details_panel deve consultar payoff_curve_points no app.db."`

### `ATT/tests/test_database_retention_simulation_service.py`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L18: `CREATE TABLE payoff_curve_points (`
- L44: `"INSERT INTO payoff_curve_points (timestamp, created_at) VALUES (?, ?)",`
- L73: `assert _table(report, "payoff_curve_points")["candidate_count"] == 1`
- L130: `CREATE TABLE payoff_curve_points (`
- L138: `"INSERT INTO payoff_curve_points (timestamp, created_at) VALUES (?, ?)",`
- L146: `"SELECT COUNT(*) FROM payoff_curve_points"`
- L158: `"SELECT COUNT(*) FROM payoff_curve_points"`
- L162: `assert _table(report, "payoff_curve_points")["candidate_count"] == 1`
- L256: `CREATE TABLE payoff_curve_points (`
- L263: `"INSERT INTO payoff_curve_points (timestamp) VALUES (?)",`
- L277: `assert "Tabela: payoff_curve_points" in text`

### `ATT/tests/test_derived_service.py`

Tokens:
- `payoff_curve`

Linhas relevantes:
- L89: `def fake_save_payoff_curve(ref, points, spot_ref=None, meta=None, timestamp=None):`
- L97: `monkeypatch.setattr(ds, "save_payoff_curve", fake_save_payoff_curve)`

### `ATT/tests/test_operational_observability_presentation.py`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L46: `"payoff_curve_points": False,`
- L54: `("payoff_curve_points", "ausente"),`

### `ATT/tests/test_operational_observability_query.py`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L133: `"payoff_curve_points": True,`

### `ATT/tests/test_operational_observability_service.py`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L79: `"CREATE TABLE payoff_curve_points (id INTEGER PRIMARY KEY, timestamp TEXT)"`

### `ATT/tests/test_pricing_execution_app_service.py`

Tokens:
- `PricingExecutionAppService`
- `PricingExecutionOrchestrationService`
- `execute_pricing`

Linhas relevantes:
- L1: `from services.pricing_execution_app_service import PricingExecutionAppService`
- L4: `class FakePricingExecutionOrchestrationService:`
- L19: `def execute_pricing(self, structure_id: int, reference_date: str | None = None):`
- L93: `return PricingExecutionAppService(`
- L94: `pricing_execution_orchestration_service=FakePricingExecutionOrchestrationService(response),`
- L99: `def test_execute_pricing_returns_persisted_record_when_present():`
- L100: `orchestration = FakePricingExecutionOrchestrationService(response={`
- L110: `service = PricingExecutionAppService(`
- L115: `result = service.execute_pricing(structure_id=10, reference_date="2026-05-16")`
- L121: `def test_execute_pricing_returns_raw_response_when_persisted_record_is_missing():`
- L123: `orchestration = FakePricingExecutionOrchestrationService(response=raw_response)`
- L125: `service = PricingExecutionAppService(`
- L130: `result = service.execute_pricing(structure_id=11, reference_date="2026-05-16")`
- L136: `def test_execute_pricing_rejects_invalid_structure_id():`
- L137: `orchestration = FakePricingExecutionOrchestrationService(response={})`
- L139: `service = PricingExecutionAppService(`
- L145: `service.execute_pricing(structure_id=0, reference_date="2026-05-16")`
- L153: `def test_execute_pricing_rejects_invalid_reference_date():`
- L154: `orchestration = FakePricingExecutionOrchestrationService(response={})`
- L156: `service = PricingExecutionAppService(`
- L162: `service.execute_pricing(structure_id=10, reference_date="16-05-2026")`
- L170: `def test_execute_pricing_accepts_none_reference_date():`
- L171: `orchestration = FakePricingExecutionOrchestrationService(`
- L175: `service = PricingExecutionAppService(`
- L180: `result = service.execute_pricing(structure_id=10, reference_date=None)`
- L186: `def test_execute_pricing_raises_value_error_when_orchestration_returns_error_status():`
- L187: `orchestration = FakePricingExecutionOrchestrationService(`
- L191: `service = PricingExecutionAppService(`
- L197: `service.execute_pricing(structure_id=10, reference_date="2026-05-16")`
- L207: `orchestration = FakePricingExecutionOrchestrationService(`

### `ATT/tests/test_pricing_execution_orchestration_service.py`

Tokens:
- `PricingExecutionOrchestrationService`
- `PricingExecutionService`

Linhas relevantes:
- L2: `PricingExecutionOrchestrationService,`
- L15: `class FakePricingExecutionService:`
- L72: `execution_service = FakePricingExecutionService(should_raise=False)`
- L75: `service = PricingExecutionOrchestrationService(`
- L105: `execution_service = FakePricingExecutionService(should_raise=True)`
- L108: `service = PricingExecutionOrchestrationService(`

### `ATT/tests/test_pricing_execution_service.py`

Tokens:
- `PricingExecutionService`

Linhas relevantes:
- L1: `from services.pricing_execution_service import PricingExecutionService`
- L45: `service = PricingExecutionService(`
- L78: `service = PricingExecutionService(`

### `ATT/tests/test_ui_data_migration.py`

Tokens:
- `payoff_curve`

Linhas relevantes:
- L167: `# Nível 4 -- get_payoff_curve_info()`
- L170: `def test_payoff_curve_info_retorna_dados(model, non_empty_decisions):`
- L172: `pts, info = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"])`
- L177: `def test_payoff_curve_info_tem_structure_id(model, non_empty_decisions):`
- L179: `_, info = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"])`
- L183: `def test_payoff_curve_info_aba_continuidade(model, non_empty_decisions):`
- L185: `_, info = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"])`
- L192: `def test_payoff_curve_info_pontos_validos(model, non_empty_decisions):`
- L194: `pts, _ = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"])`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/04_INVENTARIO_INICIAL.md`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L59: `| `payoff_curve_points` | 808 | Pontos de payoff |`
- L60: `| `structure_decisions` | 11 | Decisões operacionais |`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/37_AUDITORIA_FASE6_2_POLITICA_MINIMA_RETENCAO.md`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L35: `- payoff_curve_points`
- L40: `- structure_decisions`
- L93: `### payoff_curve_points`
- L183: `### structure_decisions`
- L297: `- payoff_curve_points`
- L309: `- structure_decisions`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/38_IMPLEMENTACAO_FASE6_3_RETENCAO_MODO_SIMULADO.md`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L43: `- payoff_curve_points por timestamp ou created_at.`
- L64: `- structure_decisions`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/39_AUDITORIA_POS_FASE6_3_RETENCAO_MODO_SIMULADO.md`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L47: `- payoff_curve_points`
- L70: `- structure_decisions`
- L96: `- payoff_curve_points: 808 registros, 0 candidatos.`
- L103: `- structure_decisions: 11 registros, fora de escopo.`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/40_AUDITORIA_FECHAMENTO_PARCIAL_FASE6_RETENCAO_SIMULADA.md`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L75: `- payoff_curve_points`
- L80: `- structure_decisions`
- L128: `- payoff_curve_points`
- L153: `- structure_decisions`
- L177: `- payoff_curve_points: 808 registros, 0 candidatos.`
- L184: `- structure_decisions: 11 registros, fora de escopo.`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/43_IMPLEMENTACAO_FASE7_1_OBSERVABILIDADE_OPERACIONAL_BASE.md`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L97: `- payoff_curve_points`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/44_AUDITORIA_POS_FASE7_1_OBSERVABILIDADE_OPERACIONAL_BASE.md`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L77: `- payoff_curve_points`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/45_AUDITORIA_PRE_FASE7_2_CONTRATO_APRESENTACAO_OBSERVABILIDADE.md`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L47: `- payoff_curve_points`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/47_AUDITORIA_POS_FASE7_2_CONTRATO_APRESENTACAO_OBSERVABILIDADE.md`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L86: `- payoff_curve_points`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/48_AUDITORIA_PRE_FASE7_3_EXPOSICAO_CONTROLADA_OBSERVABILIDADE.md`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L50: `- payoff_curve_points`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/49_IMPLEMENTACAO_FASE7_3_EXPOSICAO_CONTROLADA_OBSERVABILIDADE.md`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L116: `- payoff_curve_points`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/50_AUDITORIA_POS_FASE7_3_EXPOSICAO_CONTROLADA_OBSERVABILIDADE.md`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L90: `- payoff_curve_points`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/51_FECHAMENTO_FASE7_OBSERVABILIDADE_OPERACIONAL.md`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L166: `- payoff_curve_points`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_FASE6_RETENCAO_LIMPEZA_BASELINE_20260713.md`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L37: `- table: payoff_curve_points`
- L45: `- table: structure_decisions`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_RTD_EXCEL_BTG_ONLINE.md`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L330: `- table: payoff_curve_points`
- L338: `- table: structure_decisions`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/01_MANIFESTO_ESCOPO_ARQUIVOS.md`

Tokens:
- `payoff_curve_points`
- `derived_payoff`
- `payoff_curve`

Linhas relevantes:
- L55: `- `db/migrations/add_structure_id_to_payoff_curve_points.py` — DB — 129 linhas`
- L140: `- `scripts/diagnose_payoff_curve_points.py` — SCRIPT — 174 linhas`
- L152: `- `scripts/recalculate_payoff_curve_points_once.py` — SCRIPT — 818 linhas`
- L153: `- `scripts/recalculate_payoff_curve_points_once_checked.py` — SCRIPT — 340 linhas`
- L174: `- `services/derived_payoff_persistence.py` — SERVICE — 221 linhas`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/02_MAPA_CLASSES_FUNCOES.md`

Tokens:
- `PricingExecutionAppService`
- `PricingExecutionOrchestrationService`
- `PricingExecutionService`
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `structure_decisions`
- `execute_pricing`
- `derived_payoff`
- `payoff_curve`

Linhas relevantes:
- L80: `## `db/migrations/add_structure_id_to_payoff_curve_points.py``
- L92: `- L42: **def** `get_payoff_curve(self, ref, timestamp)``
- L587: `## `scripts/diagnose_payoff_curve_points.py``
- L650: `## `scripts/recalculate_payoff_curve_points_once.py``
- L684: `## `scripts/recalculate_payoff_curve_points_once_checked.py``
- L861: `- L350: **def** `execute_pricing(self, structure_id, reference_date)``
- L863: `## `services/derived_payoff_persistence.py``
- L865: `- L12: **class** `DerivedPayoffPersistence``
- L882: `- L160: **def** `save_payoff_curve(ref, points, spot_ref, meta, timestamp, structure_id)``
- L887: `- L362: **def** `get_all_payoff_curves``
- L894: `- L522: **def** `save_payoff_curve(self)``
- L1036: `- L22: **class** `PricingExecutionAppService``
- L1038: `- L46: **def** `execute_pricing(self, structure_id, reference_date)``
- L1048: `- L12: **class** `PricingExecutionOrchestrationService``
- L1077: `- L7: **class** `PricingExecutionService``
- L1403: `- L702: **def** `_active_structure_decisions(self)``
- L1593: `- L317: **def** `_log_rebuilt_payoff_curve(self, xs, ys)``
- L1594: `- L325: **def** `_draw_main_payoff_curve(self, xs, ys, decision_data, overlay_curve)``
- L1756: `- L1905: **def** `_ensure_structure_decisions_table(self, conn)``
- L1758: `- L1955: **def** `_load_structure_decisions(self, sid, limit)``
- L1925: `- L475: **def** `_payoff_curve_cache_key(self, structure_id, timestamp)``
- L1926: `- L481: **def** `_get_payoff_curve_from_cache(self, cache_key)``
- L1927: `- L492: **def** `_ensure_payoff_curve_available(self)``
- L1928: `- L499: **def** `_ensure_payoff_curve_columns(self, p)``
- L1929: `- L506: **def** `_build_payoff_curve_exact_sql(self, p, filter_col)``
- L1930: `- L516: **def** `_fetch_payoff_curve_exact_rows(self, conn, p, filter_col, filter_val, timestamp)``
- L1931: `- L527: **def** `_build_payoff_curve_latest_timestamp_sql(self, p, filter_col)``
- L1932: `- L538: **def** `_fetch_payoff_curve_latest_timestamp(self, conn, p, filter_col, filter_val)``
- L1933: `- L544: **def** `_payoff_curve_rows_to_dicts(self, rows)``
- L1934: `- L547: **def** `_cache_payoff_curve_result(self, cache_key, result)``

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/03_UI_CALLBACKS_EVENTOS.md`

Tokens:
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L587: `1955:     def _load_structure_decisions(self, sid: int, limit: int = 5) -> List[Dict[str, Any]]:`
- L590: `1986:             rows = self._load_structure_decisions(int(sid), limit=5)`
- L1082: `553:     def _load_payoff_curve_fallback(`
- L1085: `575:     def _load_payoff_curve_uncached(`
- L1088: `596:         return self._load_payoff_curve_fallback(`
- L1091: `616:         return self._load_payoff_curve_uncached(`
- L1100: `664:     def _load_payoff_curve_info_points(`
- L1103: `674:             return self._load_canonical_payoff_curve_info_points(`
- L1106: `678:         return self._load_legacy_payoff_curve_info_points(`
- L1109: `726:     def _load_canonical_payoff_curve_info_points(`
- L1112: `784:     def _load_legacy_payoff_curve_info_points(`
- L1121: `819:     def _load_uncached_payoff_curve_info(`
- L1124: `833:             points = self._load_payoff_curve_info_points(`
- L1130: `862:         points, info = self._load_uncached_payoff_curve_info(`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/04_SERVICES_CONTROLLERS_API.md`

Tokens:
- `PricingExecutionAppService`
- `PricingExecutionOrchestrationService`
- `PricingExecutionService`
- `DerivedPayoffPersistence`
- `execute_pricing`
- `derived_payoff`
- `payoff_curve`

Linhas relevantes:
- L11: `- `services.pricing_execution_app_service import PricingExecutionAppService``
- L118: `- `services.derived_payoff_persistence import DerivedPayoffPersistence``
- L121: `- `services.pricing_execution_service import PricingExecutionService``
- L137: `- L350: `def execute_pricing(self, structure_id, reference_date)``
- L139: `## `services/derived_payoff_persistence.py``
- L151: `- L12: `class DerivedPayoffPersistence``
- L182: `- L160: `def save_payoff_curve(ref, points, spot_ref, meta, timestamp, structure_id)``
- L187: `- L362: `def get_all_payoff_curves``
- L194: `- L522: `def save_payoff_curve(self)``
- L438: `- `services.pricing_execution_orchestration_service import PricingExecutionOrchestrationService``
- L444: `- L22: `class PricingExecutionAppService``
- L446: `- L46: `def execute_pricing(self, structure_id, reference_date)``
- L460: `- `services.pricing_execution_service import PricingExecutionService``
- L467: `- L12: `class PricingExecutionOrchestrationService``
- L522: `- L7: `class PricingExecutionService``

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/05_BANCO_SQL_TABELAS.md`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L21: `- `payoff_curve_points`: 28 ocorrência(s)`
- L22: `- `structure_decisions`: 19 ocorrência(s)`
- L27: `83: CREATE TABLE IF NOT EXISTS payoff_curve_points (`
- L30: `107: CREATE TABLE IF NOT EXISTS structure_decisions (`
- L33: `144:         "ALTER TABLE payoff_curve_points ADD COLUMN structure_id INTEGER"`
- L36: `304:                 "DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`
- L39: `360:                 "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L42: `365:                 INSERT INTO payoff_curve_points`
- L45: `408:                 INSERT OR REPLACE INTO payoff_curve_points`
- L48: `454:                 "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L51: `459:                 INSERT INTO payoff_curve_points`
- L54: `480:                 "DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`
- L57: `506:                     FROM payoff_curve_points`
- L60: `516:                     FROM payoff_curve_points`
- L63: `527:                     FROM payoff_curve_points`
- L66: `568:                 f"SELECT * FROM structure_decisions {where} ORDER BY id DESC LIMIT ?",`
- L69: `585:                 FROM structure_decisions d`
- L72: `586:                 LEFT JOIN payoff_curve_points p`
- L75: `594:                 FROM payoff_curve_points p`
- L78: `595:                 LEFT JOIN structure_decisions d`
- L81: `617:                 f"DELETE FROM payoff_curve_points "`
- L84: `629:                 f"DELETE FROM structure_decisions "`
- L87: `697:         "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L90: `701:         INSERT INTO payoff_curve_points`
- L93: `732:         "DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`
- L96: `738:         INSERT INTO structure_decisions`
- L99: `791:         INSERT OR REPLACE INTO payoff_curve_points`
- L102: `825:         INSERT OR REPLACE INTO structure_decisions`
- L105: `858:             FROM payoff_curve_points`
- L108: `865:             FROM payoff_curve_points`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/06_FLUXO_PAYOFF.md`

Tokens:
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `structure_decisions`
- `derived_payoff`
- `payoff_curve`

Linhas relevantes:
- L35: `4: Tabelas: payoff_curve_points, structure_decisions`
- L50: `80: # alteracao_36_A: adicionar structure_id ao DDL de payoff_curve_points`
- L56: `83: CREATE TABLE IF NOT EXISTS payoff_curve_points (`
- L65: `97: ON payoff_curve_points (timestamp, aba, point_spot)`
- L74: `103: ON payoff_curve_points (structure_id, timestamp)`
- L80: `144:         "ALTER TABLE payoff_curve_points ADD COLUMN structure_id INTEGER"`
- L89: `183:     # alteracao_36_A: migration incremental payoff_curve_points`
- L92: `184:     existing_cols = _table_columns(conn, "payoff_curve_points")`
- L116: `360:                 "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L119: `365:                 INSERT INTO payoff_curve_points`
- L128: `408:                 INSERT OR REPLACE INTO payoff_curve_points`
- L137: `454:                 "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L140: `459:                 INSERT INTO payoff_curve_points`
- L146: `506:                     FROM payoff_curve_points`
- L149: `516:                     FROM payoff_curve_points`
- L152: `527:                     FROM payoff_curve_points`
- L155: `586:                 LEFT JOIN payoff_curve_points p`
- L158: `594:                 FROM payoff_curve_points p`
- L164: `617:                 f"DELETE FROM payoff_curve_points "`
- L170: `697:         "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L173: `701:         INSERT INTO payoff_curve_points`
- L185: `791:         INSERT OR REPLACE INTO payoff_curve_points`
- L191: `858:             FROM payoff_curve_points`
- L194: `865:             FROM payoff_curve_points`
- L197: `873:             FROM payoff_curve_points`
- L200: `887:         LEFT JOIN payoff_curve_points p ON (d.aba = p.aba AND d.timestamp = p.timestamp)`
- L203: `894:         FROM payoff_curve_points p`
- L209: `915:         DELETE FROM payoff_curve_points`
- L212: `## `db/migrations/add_structure_id_to_payoff_curve_points.py``
- L215: `1: # db/migrations/add_structure_id_to_payoff_curve_points.py`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/07_FLUXO_PRICING_EXECUTION.md`

Tokens:
- `PricingExecutionAppService`
- `PricingExecutionOrchestrationService`
- `PricingExecutionService`
- `payoff_curve_points`
- `execute_pricing`
- `derived_payoff`
- `payoff_curve`

Linhas relevantes:
- L8: `4: from services.pricing_execution_app_service import PricingExecutionAppService`
- L11: `7: service = PricingExecutionAppService()`
- L23: `18:         return service.execute_pricing(`
- L293: `2: from services.pricing_execution_service import PricingExecutionService`
- L296: `7:     service = PricingExecutionService()`
- L317: `4: from services.pricing_execution_service import PricingExecutionService`
- L326: `10:     execution_service = PricingExecutionService()`
- L461: `2:     PricingExecutionOrchestrationService,`
- L464: `7:     service = PricingExecutionOrchestrationService()`
- L476: `2:     PricingExecutionOrchestrationService,`
- L479: `4: from services.pricing_execution_service import PricingExecutionService`
- L491: `13:     execution_service = PricingExecutionService(`
- L497: `16:     service = PricingExecutionOrchestrationService(`
- L542: `1: from services.pricing_execution_app_service import PricingExecutionAppService`
- L545: `5:     service = PricingExecutionAppService()`
- L548: `7:     response = service.execute_pricing(structure_id=2)`
- L557: `1: from services.pricing_execution_app_service import PricingExecutionAppService`
- L560: `5:     service = PricingExecutionAppService()`
- L569: `1: from services.pricing_execution_app_service import PricingExecutionAppService`
- L572: `5:     service = PricingExecutionAppService()`
- L611: `1: from services.pricing_execution_app_service import PricingExecutionAppService`
- L614: `5:     service = PricingExecutionAppService()`
- L647: `1: from services.pricing_execution_app_service import PricingExecutionAppService`
- L650: `5:     service = PricingExecutionAppService()`
- L695: `1: from services.pricing_execution_app_service import PricingExecutionAppService`
- L698: `5:     service = PricingExecutionAppService()`
- L908: `68:     "execute_pricing",`
- L920: `480:         "execute_pricing",`
- L947: `## `scripts/recalculate_payoff_curve_points_once.py``
- L1079: `14:   C8: execute_pricing() passa underlying_asset para o payload builder.`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/08_FLUXO_RTD_VWAP_MARKET_DATA.md`

Tokens:
- `payoff_curve_points`
- `execute_pricing`
- `derived_payoff`
- `payoff_curve`

Linhas relevantes:
- L1217: `85:         description="Recalcula payoff_curve_points em lote usando o script RTD existente."`
- L1289: `## `scripts/recalculate_payoff_curve_points_once.py``
- L1292: `5: Recalcula payoff_curve_points usando cotações RTD atuais.`
- L1541: `594:         "source": "recalculate_payoff_curve_points_once.rtd",`
- L1583: `710:         description="Recalcula payoff_curve_points usando rtd_option_quotes e rtd_underlying_quotes."`
- L2342: `14:   C8: execute_pricing() passa underlying_asset para o payload builder.`
- L2447: `## `services/derived_payoff_persistence.py``

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/09_SNAPSHOTS_DERIVED_RETENCAO.md`

Tokens:
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `structure_decisions`
- `derived_payoff`
- `payoff_curve`

Linhas relevantes:
- L11: `4: Tabelas: payoff_curve_points, structure_decisions`
- L23: `107: CREATE TABLE IF NOT EXISTS structure_decisions (`
- L29: `128: ON structure_decisions (timestamp, aba)`
- L32: `133: ON structure_decisions (aba, timestamp)`
- L35: `138: ON structure_decisions (timestamp)`
- L41: `198:     # Índices de structure_decisions`
- L59: `304:                 "DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`
- L68: `360:                 "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L77: `454:                 "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L80: `480:                 "DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`
- L83: `568:                 f"SELECT * FROM structure_decisions {where} ORDER BY id DESC LIMIT ?",`
- L89: `585:                 FROM structure_decisions d`
- L92: `595:                 LEFT JOIN structure_decisions d`
- L98: `617:                 f"DELETE FROM payoff_curve_points "`
- L101: `629:                 f"DELETE FROM structure_decisions "`
- L104: `654:             {verb} INTO structure_decisions`
- L113: `697:         "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L122: `732:         "DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`
- L125: `738:         INSERT INTO structure_decisions`
- L146: `825:         INSERT OR REPLACE INTO structure_decisions`
- L158: `886:         FROM structure_decisions d`
- L161: `895:         LEFT JOIN structure_decisions d ON (p.aba = d.aba AND p.timestamp = d.timestamp)`
- L170: `915:         DELETE FROM payoff_curve_points`
- L182: `927:         DELETE FROM structure_decisions`
- L200: `## `db/migrations/add_structure_id_to_payoff_curve_points.py``
- L203: `4: e payoff_curve_summary, com backfill via structure_decisions.`
- L206: `33:             FROM structure_decisions d`
- L209: `47:     #  payoff_curve_summary`
- L212: `49:         "payoff_curve_summary: ADD COLUMN structure_id",`
- L215: `50:         "ALTER TABLE payoff_curve_summary ADD COLUMN structure_id INTEGER",`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/10_DUPLICIDADES_FALHAS_SILENCIOSAS.md`

Tokens:
- `payoff_curve_points`
- `execute_pricing`
- `derived_payoff`
- `payoff_curve`

Linhas relevantes:
- L79: `- `scripts/diagnose_payoff_curve_points.py` L14 args=(points)`
- L341: `- `scripts/recalculate_payoff_curve_points_once.py` L39 args=(db_path)`
- L342: `- `scripts/recalculate_payoff_curve_points_once_checked.py` L32 args=(db)`
- L366: `### `execute_pricing``
- L417: `### `get_payoff_curve``
- L470: `- `scripts/recalculate_payoff_curve_points_once_checked.py` L53 args=(conn, structure_ids)`
- L581: `- `scripts/diagnose_payoff_curve_points.py` L37 args=()`
- L591: `- `scripts/recalculate_payoff_curve_points_once.py` L708 args=(argv)`
- L592: `- `scripts/recalculate_payoff_curve_points_once_checked.py` L207 args=()`
- L635: `- `scripts/recalculate_payoff_curve_points_once.py` L129 args=(symbol)`
- L663: `- `services/derived_payoff_persistence.py` L27 args=(self, pricing_payload, result)`
- L689: `- `db/migrations/add_structure_id_to_payoff_curve_points.py` L80 args=(db_path)`
- L722: `### `save_payoff_curve``
- L735: `- `scripts/recalculate_payoff_curve_points_once.py` L59 args=(conn, table)`
- L742: `- `scripts/recalculate_payoff_curve_points_once.py` L45 args=(conn, table)`
- L743: `- `scripts/recalculate_payoff_curve_points_once_checked.py` L38 args=(conn, name)`
- L838: `## `db/migrations/add_structure_id_to_payoff_curve_points.py``
- L2245: `## `scripts/diagnose_payoff_curve_points.py``
- L2254: `63:             print("ERRO: tabela payoff_curve_points não existe.")`
- L2257: `66:         print("\nSchema payoff_curve_points:")`
- L2581: `## `scripts/recalculate_payoff_curve_points_once.py``
- L2641: `## `scripts/recalculate_payoff_curve_points_once_checked.py``
- L3271: `## `services/derived_payoff_persistence.py``

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/11_FONTES_METODOS_CRITICOS.md`

Tokens:
- `PricingExecutionOrchestrationService`
- `PricingExecutionService`
- `payoff_curve_points`
- `structure_decisions`
- `execute_pricing`
- `derived_payoff`
- `payoff_curve`

Linhas relevantes:
- L161: `"payoff_curve_points",`
- L191: `if table == "payoff_curve_points" and ts_col == "timestamp":`
- L818: `pricing_execution_orchestration_service: PricingExecutionOrchestrationService | None = None,`
- L828: `or PricingExecutionOrchestrationService()`
- L835: `### `execute_pricing` — L46:L86`
- L838: `def execute_pricing(`
- L889: `pricing_execution_service: PricingExecutionService | None = None,`
- L893: `self.pricing_execution_service = pricing_execution_service or PricingExecutionService(`
- L1118: `## `services/derived_payoff_persistence.py``
- L1129: `logger.debug("derived_payoff_persistence: pricing_payload vazio, skip.")`
- L1136: `"derived_payoff_persistence: status=%r não elegível para payoff, skip.",`
- L1148: `"derived_payoff_persistence: decisão não gravada porque payoff não foi salvo -- structure_id=%s",`
- L1156: `"derived_payoff_persistence: payoff salvo, mas decisão falhou -- structure_id=%s timestamp=%s",`
- L1177: `"derived_payoff_persistence: payoff sem pontos para structure_id=%s",`
- L1184: `"derived_payoff_persistence: %d pontos gravados -- structure_id=%s",`
- L1192: `"derived_payoff_persistence: erro ao gravar payoff -- structure_id=%s",`
- L1262: `"derived_payoff_persistence: decisão gravada -- structure_id=%s",`
- L1269: `"derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s",`
- L1321: `### `save_payoff_curve` — L160:L207`
- L1324: `def save_payoff_curve(`
- L1374: `### `save_payoff_curve` — L522:L523`
- L1377: `def save_payoff_curve(self, *args, **kwargs):`
- L1378: `return save_payoff_curve(*args, **kwargs)`
- L1416: `sig = inspect.signature(save_payoff_curve)`
- L1428: `return save_payoff_curve(`
- L1437: `return save_payoff_curve(`
- L1461: `FROM payoff_curve_points`
- L1524: `"DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L1528: `INSERT INTO payoff_curve_points`
- L1574: `"DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/12_CHAMADAS_RECALCULO_PAYOFF.md`

Tokens:
- `PricingExecutionAppService`
- `PricingExecutionOrchestrationService`
- `payoff_curve_points`
- `execute_pricing`
- `payoff_curve`

Linhas relevantes:
- L12: `>> 18:         return service.execute_pricing(`
- L22: `7:     service = PricingExecutionOrchestrationService()`
- L46: `5:     service = PricingExecutionAppService()`
- L48: `>> 7:     response = service.execute_pricing(structure_id=2)`
- L60: `>> 68:     "execute_pricing",`
- L68: `68:     "execute_pricing",`
- L98: `454:         "payoff_curve_points",`
- L99: `455:         "payoff_curve_summary",`
- L108: `455:         "payoff_curve_summary",`
- L120: `>> 480:         "execute_pricing",`
- L152: `>> 73:         "execute_pricing",`
- L172: `>> 109:     "scripts/recalculate_payoff_curve_points_once.py": [`
- L182: `>> 123:     "scripts/recalculate_payoff_curve_points_once_checked.py": [`
- L194: `363:         r"execute_pricing",`
- L203: `363:         r"execute_pricing",`
- L212: `>> 363:         r"execute_pricing",`
- L221: `363:         r"execute_pricing",`
- L224: `366:         r"recalculate_payoff_curve_points_once",`
- L230: `363:         r"execute_pricing",`
- L233: `366:         r"recalculate_payoff_curve_points_once",`
- L242: `>> 366:         r"recalculate_payoff_curve_points_once",`
- L251: `366:         r"recalculate_payoff_curve_points_once",`
- L260: `366:         r"recalculate_payoff_curve_points_once",`
- L282: `>> 600: - [ ] O recálculo deve passar por `PricingExecutionAppService.execute_pricing()`?`
- L283: `601: - [ ] O script `scripts/recalculate_payoff_curve_points_once.py` continuará existindo como worker externo?`
- L291: `600: - [ ] O recálculo deve passar por `PricingExecutionAppService.execute_pricing()`?`
- L292: `>> 601: - [ ] O script `scripts/recalculate_payoff_curve_points_once.py` continuará existindo como worker externo?`
- L294: `603: - [ ] A UI deve apenas ler `payoff_curve_points`?`
- L300: `603: - [ ] A UI deve apenas ler `payoff_curve_points`?`
- L406: `>> 12: RECALC_SCRIPT = ROOT / "scripts" / "recalculate_payoff_curve_points_once.py"`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/13_INVENTARIO_WRITES_DELETES_DB.md`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L22: `>> 83: CREATE TABLE IF NOT EXISTS payoff_curve_points (`
- L32: `>> 107: CREATE TABLE IF NOT EXISTS structure_decisions (`
- L52: `>> 144:         "ALTER TABLE payoff_curve_points ADD COLUMN structure_id INTEGER"`
- L84: `183:     # alteracao_36_A: migration incremental payoff_curve_points`
- L111: `198:     # Índices de structure_decisions`
- L120: `198:     # Índices de structure_decisions`
- L153: `304:                 "DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`
- L162: `>> 304:                 "DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`
- L193: `360:                 "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L202: `>> 360:                 "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L212: `>> 365:                 INSERT INTO payoff_curve_points`
- L242: `>> 408:                 INSERT OR REPLACE INTO payoff_curve_points`
- L263: `454:                 "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L272: `>> 454:                 "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L282: `>> 459:                 INSERT INTO payoff_curve_points`
- L303: `480:                 "DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`
- L312: `>> 480:                 "DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`
- L353: `568:                 f"SELECT * FROM structure_decisions {where} ORDER BY id DESC LIMIT ?",`
- L364: `585:                 FROM structure_decisions d`
- L374: `594:                 FROM payoff_curve_points p`
- L383: `617:                 f"DELETE FROM payoff_curve_points "`
- L392: `>> 617:                 f"DELETE FROM payoff_curve_points "`
- L403: `629:                 f"DELETE FROM structure_decisions "`
- L412: `>> 629:                 f"DELETE FROM structure_decisions "`
- L434: `654:             {verb} INTO structure_decisions`
- L443: `697:         "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L452: `>> 697:         "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L462: `>> 701:         INSERT INTO payoff_curve_points`
- L483: `732:         "DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`
- L492: `>> 732:         "DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/14_LEITURAS_PAYOFF_DECISIONS.md`

Tokens:
- `PricingExecutionAppService`
- `payoff_curve_points`
- `structure_decisions`
- `execute_pricing`
- `payoff_curve`

Linhas relevantes:
- L12: `>> 4: Tabelas: payoff_curve_points, structure_decisions`
- L22: `>> 80: # alteracao_36_A: adicionar structure_id ao DDL de payoff_curve_points`
- L30: `80: # alteracao_36_A: adicionar structure_id ao DDL de payoff_curve_points`
- L33: `83: CREATE TABLE IF NOT EXISTS payoff_curve_points (`
- L42: `>> 83: CREATE TABLE IF NOT EXISTS payoff_curve_points (`
- L52: `>> 97: ON payoff_curve_points (timestamp, aba, point_spot)`
- L62: `>> 103: ON payoff_curve_points (structure_id, timestamp)`
- L73: `107: CREATE TABLE IF NOT EXISTS structure_decisions (`
- L82: `>> 107: CREATE TABLE IF NOT EXISTS structure_decisions (`
- L92: `>> 128: ON structure_decisions (timestamp, aba)`
- L102: `>> 133: ON structure_decisions (aba, timestamp)`
- L112: `>> 138: ON structure_decisions (timestamp)`
- L122: `>> 144:         "ALTER TABLE payoff_curve_points ADD COLUMN structure_id INTEGER"`
- L144: `183:     # alteracao_36_A: migration incremental payoff_curve_points`
- L152: `>> 183:     # alteracao_36_A: migration incremental payoff_curve_points`
- L153: `184:     existing_cols = _table_columns(conn, "payoff_curve_points")`
- L161: `183:     # alteracao_36_A: migration incremental payoff_curve_points`
- L162: `>> 184:     existing_cols = _table_columns(conn, "payoff_curve_points")`
- L172: `>> 198:     # Índices de structure_decisions`
- L182: `>> 304:                 "DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`
- L192: `>> 360:                 "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L202: `>> 365:                 INSERT INTO payoff_curve_points`
- L212: `>> 408:                 INSERT OR REPLACE INTO payoff_curve_points`
- L222: `>> 454:                 "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L232: `>> 459:                 INSERT INTO payoff_curve_points`
- L242: `>> 480:                 "DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`
- L262: `>> 506:                     FROM payoff_curve_points`
- L272: `>> 516:                     FROM payoff_curve_points`
- L282: `>> 527:                     FROM payoff_curve_points`
- L292: `>> 568:                 f"SELECT * FROM structure_decisions {where} ORDER BY id DESC LIMIT ?",`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/15_WIRING_DEPENDENCIAS_IMPORTS.md`

Tokens:
- `PricingExecutionAppService`
- `PricingExecutionOrchestrationService`
- `PricingExecutionService`
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `execute_pricing`
- `derived_payoff`
- `payoff_curve`

Linhas relevantes:
- L12: `>> 4: from services.pricing_execution_app_service import PricingExecutionAppService`
- L22: `>> 7: service = PricingExecutionAppService()`
- L240: `2: from services.pricing_execution_service import PricingExecutionService`
- L248: `>> 2: from services.pricing_execution_service import PricingExecutionService`
- L259: `7:     service = PricingExecutionService()`
- L279: `4: from services.pricing_execution_service import PricingExecutionService`
- L287: `>> 4: from services.pricing_execution_service import PricingExecutionService`
- L296: `4: from services.pricing_execution_service import PricingExecutionService`
- L306: `10:     execution_service = PricingExecutionService()`
- L407: `2:     PricingExecutionOrchestrationService,`
- L415: `>> 2:     PricingExecutionOrchestrationService,`
- L425: `>> 7:     service = PricingExecutionOrchestrationService()`
- L436: `2:     PricingExecutionOrchestrationService,`
- L444: `>> 2:     PricingExecutionOrchestrationService,`
- L446: `4: from services.pricing_execution_service import PricingExecutionService`
- L452: `2:     PricingExecutionOrchestrationService,`
- L454: `>> 4: from services.pricing_execution_service import PricingExecutionService`
- L464: `>> 16:     service = PricingExecutionOrchestrationService(`
- L494: `>> 1: from services.pricing_execution_app_service import PricingExecutionAppService`
- L504: `>> 5:     service = PricingExecutionAppService()`
- L506: `7:     response = service.execute_pricing(structure_id=2)`
- L514: `>> 1: from services.pricing_execution_app_service import PricingExecutionAppService`
- L524: `>> 5:     service = PricingExecutionAppService()`
- L534: `>> 1: from services.pricing_execution_app_service import PricingExecutionAppService`
- L544: `>> 5:     service = PricingExecutionAppService()`
- L574: `>> 1: from services.pricing_execution_app_service import PricingExecutionAppService`
- L584: `>> 5:     service = PricingExecutionAppService()`
- L614: `>> 1: from services.pricing_execution_app_service import PricingExecutionAppService`
- L624: `>> 5:     service = PricingExecutionAppService()`
- L664: `>> 1: from services.pricing_execution_app_service import PricingExecutionAppService`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/16_RUNTIME_DB_SCHEMA_COUNTS.md`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L18: `### `payoff_curve_points``
- L96: `### `structure_decisions``

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/18_FALLBACKS_FALHAS_SILENCIOSAS_CONTEXTO.md`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `derived_payoff`
- `payoff_curve`

Linhas relevantes:
- L150: `198:     # Índices de structure_decisions`
- L267: `## `db/migrations/add_structure_id_to_payoff_curve_points.py``
- L305: `106:         for table in ("payoff_curve_points", "payoff_curve_summary"):`
- L388: `42:     def get_payoff_curve(self, ref: StructureRef, timestamp: Optional[str] = None) -> pd.DataFrame:`
- L4736: `## `scripts/diagnose_payoff_curve_points.py``
- L4762: `62:         if "payoff_curve_points" not in tables:`
- L4763: `>> 63:             print("ERRO: tabela payoff_curve_points não existe.")`
- L4773: `>> 66:         print("\nSchema payoff_curve_points:")`
- L4774: `67:         for r in con.execute("PRAGMA table_info(payoff_curve_points)").fetchall():`
- L4781: `66:         print("\nSchema payoff_curve_points:")`
- L4782: `67:         for r in con.execute("PRAGMA table_info(payoff_curve_points)").fetchall():`
- L5786: `## `scripts/recalculate_payoff_curve_points_once.py``
- L5978: `## `scripts/recalculate_payoff_curve_points_once_checked.py``
- L8064: `## `services/derived_payoff_persistence.py``
- L8072: `52:                 "derived_payoff_persistence: decisão não gravada porque payoff não foi salvo -- structure_id=%s",`
- L8082: `81:                     "derived_payoff_persistence: payoff sem pontos para structure_id=%s",`
- L8093: `96:                 "derived_payoff_persistence: erro ao gravar payoff -- structure_id=%s",`
- L8102: `96:                 "derived_payoff_persistence: erro ao gravar payoff -- structure_id=%s",`
- L8133: `173:                 "derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s",`
- L8142: `173:                 "derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s",`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/19_SCRIPTS_PATCH_MANUTENCAO_LEGADO.md`

Tokens:
- `PricingExecutionAppService`
- `PricingExecutionOrchestrationService`
- `PricingExecutionService`
- `payoff_curve_points`
- `structure_decisions`
- `execute_pricing`
- `payoff_curve`

Linhas relevantes:
- L7: `## `db/migrations/add_structure_id_to_payoff_curve_points.py``
- L10: `# db/migrations/add_structure_id_to_payoff_curve_points.py`
- L12: `Migration: adiciona structure_id em payoff_curve_points`
- L13: `e payoff_curve_summary, com backfill via structure_decisions.`
- L16: `python db/migrations/add_structure_id_to_payoff_curve_points.py`
- L17: `python db/migrations/add_structure_id_to_payoff_curve_points.py --db dados/app.db`
- L27: `#  payoff_curve_points`
- L29: `"payoff_curve_points: verificar se structure_id já existe",`
- L33: `"payoff_curve_points: ADD COLUMN structure_id",`
- L34: `"ALTER TABLE payoff_curve_points ADD COLUMN structure_id INTEGER",`
- L37: `"payoff_curve_points: BACKFILL structure_id",`
- L39: `UPDATE payoff_curve_points`
- L42: `FROM structure_decisions d`
- L43: `WHERE d.aba       = payoff_curve_points.aba`
- L44: `AND d.timestamp = payoff_curve_points.timestamp`
- L50: `"payoff_curve_points: CREATE INDEX sid+ts",`
- L53: `ON payoff_curve_points (structure_id, timestamp)`
- L56: `#  payoff_curve_summary`
- L58: `"payoff_curve_summary: ADD COLUMN structure_id",`
- L59: `"ALTER TABLE payoff_curve_summary ADD COLUMN structure_id INTEGER",`
- L62: `"payoff_curve_summary: BACKFILL structure_id",`
- L64: `UPDATE payoff_curve_summary`
- L67: `FROM structure_decisions d`
- L68: `WHERE d.aba       = payoff_curve_summary.aba`
- L69: `AND d.timestamp = payoff_curve_summary.timestamp`
- L75: `"payoff_curve_summary: CREATE INDEX sid+ts",`
- L78: `ON payoff_curve_summary (structure_id, timestamp)`
- L464: `from services.pricing_execution_service import PricingExecutionService`
- L469: `service = PricingExecutionService()`
- L495: `from services.pricing_execution_service import PricingExecutionService`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/20_CHECKLIST_REFACTOR_DECISOES.md`

Tokens:
- `PayoffRefreshCommandService`
- `PricingExecutionAppService`
- `PricingExecutionOrchestrationService`
- `PricingExecutionService`
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `execute_pricing`
- `payoff_curve`

Linhas relevantes:
- L10: `- [ ] O recálculo deve passar por `PricingExecutionAppService.execute_pricing()`?`
- L11: `- [ ] O script `scripts/recalculate_payoff_curve_points_once.py` continuará existindo como worker externo?`
- L13: `- [ ] A UI deve apenas ler `payoff_curve_points`?`
- L26: `- [ ] `payoff_curve_points` tem `structure_id` preenchido para todos os snapshots recentes?`
- L30: `- [ ] `payoff_curve_summary` ainda é usado?`
- L36: `- [ ] Caminho oficial é `PricingExecutionAppService -> PricingExecutionOrchestrationService -> PricingExecutionService -> PricingExecutionPersistenceService`?`
- L38: `- [ ] `DerivedPayoffPersistence` deve ser sempre acionado após execução OK?`
- L65: ``PayoffRefreshCommandService``

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/21_RESUMO_EXECUTIVO_DIAGNOSTICO.md`

Tokens:
- `PayoffRefreshCommandService`
- `PricingExecutionAppService`
- `PricingExecutionOrchestrationService`
- `PricingExecutionService`
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L49: `PricingExecutionAppService`
- L50: `-> PricingExecutionOrchestrationService`
- L52: `-> PricingExecutionService`
- L61: `DerivedPayoffPersistence`
- L65: `- payoff_curve_points`
- L66: `- structure_decisions`
- L68: `Porém, no fluxo atual de PricingExecutionOrchestrationService, a criação padrão de PricingExecutionPersistenceService não injeta explicitamente DerivedPayoffPersistence.`
- L76: `- payoff_curve_points com 2727 linhas;`
- L78: `- structure_decisions com 11 linhas;`
- L85: `- payoff_curve_points tem muitos snapshots;`
- L86: `- structure_decisions tem poucos registros;`
- L88: `- payoff_curve_points chegou até 2026-07-17;`
- L89: `- structure_decisions chegou até 2026-07-06.`
- L103: `5. persistir payoff_curve_points;`
- L104: `6. persistir structure_decisions;`
- L120: `PayoffRefreshCommandService`
- L134: `3. corrigir o wiring para garantir DerivedPayoffPersistence;`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/22_FLUXO_OFICIAL_RECOMENDADO.md`

Tokens:
- `PayoffRefreshCommandService`
- `PricingExecutionAppService`
- `PricingExecutionOrchestrationService`
- `PricingExecutionService`
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L13: `-> PayoffRefreshCommandService`
- L14: `-> PricingExecutionAppService`
- L15: `-> PricingExecutionOrchestrationService`
- L17: `-> PricingExecutionService`
- L21: `-> DerivedPayoffPersistence`
- L23: `-> payoff_curve_points`
- L24: `-> structure_decisions`
- L49: `### PayoffRefreshCommandService`
- L59: `### PricingExecutionAppService`
- L68: `### PricingExecutionOrchestrationService`
- L85: `### DerivedPayoffPersistence`
- L91: `- gravar payoff_curve_points;`
- L92: `- gravar structure_decisions;`
- L99: `payoff_persistence_port = DerivedPayoffPersistence()`
- L101: `Sem isso, a execução pode ser persistida sem gerar payoff_curve_points e structure_decisions.`
- L135: `scripts/recalculate_payoff_curve_points_once.py`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/23_PROBLEMAS_PRIORITARIOS.md`

Tokens:
- `PricingExecutionOrchestrationService`
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L7: `O arquivo de fontes críticas mostra que PricingExecutionOrchestrationService cria PricingExecutionPersistenceService assim:`
- L13: `Não aparece injeção explícita de DerivedPayoffPersistence nesse ponto.`
- L19: `- payoff_curve_points;`
- L20: `- structure_decisions.`
- L31: `payoff_persistence_port=DerivedPayoffPersistence(),`
- L89: `- recalculate_payoff_curve_points_once.py;`
- L90: `- recalculate_payoff_curve_points_once_checked.py;`
- L96: `Múltiplas fontes escrevendo payoff_curve_points com padrões diferentes.`
- L115: `payoff_curve_points:`
- L120: `structure_decisions:`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/24_PLANO_DE_CORRECAO_EM_FASES.md`

Tokens:
- `PayoffRefreshCommandService`
- `PricingExecutionAppService`
- `PricingExecutionOrchestrationService`
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `structure_decisions`
- `execute_pricing`
- `payoff_curve`

Linhas relevantes:
- L29: `1. alterar PricingExecutionOrchestrationService;`
- L30: `2. injetar DerivedPayoffPersistence em PricingExecutionPersistenceService;`
- L33: `5. validar payoff_curve_points e structure_decisions.`
- L40: `- pontos em payoff_curve_points;`
- L41: `- decisão em structure_decisions.`
- L43: `## Fase 3 - Criar PayoffRefreshCommandService`
- L53: `3. chamar PricingExecutionAppService.execute_pricing;`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/25_DESENHO_PAYOFF_REFRESH_COMMAND_SERVICE.md`

Tokens:
- `PayoffRefreshCommandService`
- `PricingExecutionAppService`
- `execute_pricing`

Linhas relevantes:
- L1: `﻿# 25 - Desenho do PayoffRefreshCommandService`
- L13: `PayoffRefreshCommandService`
- L27: `2. chamar PricingExecutionAppService.execute_pricing;`
- L48: `PricingExecutionAppService`
- L81: `Se execute_pricing retornar OK mas não houver payoff novo, o serviço deve falhar explicitamente ou retornar warning.`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/26_PATCH_WIRING_DERIVED_PAYOFF.md`

Tokens:
- `PayoffRefreshCommandService`
- `PricingExecutionAppService`
- `PricingExecutionOrchestrationService`
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `structure_decisions`
- `execute_pricing`
- `derived_payoff`
- `payoff_curve`

Linhas relevantes:
- L1: `﻿# 26 - Patch Recomendado para Wiring de DerivedPayoffPersistence`
- L5: `O fluxo de PricingExecutionOrchestrationService cria PricingExecutionPersistenceService sem injetar explicitamente DerivedPayoffPersistence.`
- L19: `from services.derived_payoff_persistence import DerivedPayoffPersistence`
- L37: `payoff_persistence_port=DerivedPayoffPersistence(),`
- L48: `- payoff_curve_points;`
- L49: `- structure_decisions.`
- L61: `Essa decisão pode ser mantida, mas o PayoffRefreshCommandService deve validar depois se o payoff foi realmente gerado.`
- L67: `SELECT COUNT(*) FROM payoff_curve_points;`
- L68: `SELECT COUNT(*) FROM structure_decisions;`
- L73: `PricingExecutionAppService().execute_pricing(structure_id=2)`
- L77: `4. verificar se houve aumento em payoff_curve_points e pricing_executions.`
- L79: `5. verificar se structure_decisions recebeu registro compatível.`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/27_REGRAS_UI_SEM_CALCULO.md`

Tokens:
- `PayoffRefreshCommandService`
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L25: `- gravar payoff_curve_points;`
- L42: `"Cálculo de payoff na UI é proibido. Use PayoffRefreshCommandService."`
- L61: `2. esse método chama PayoffRefreshCommandService;`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/28_VERIFICACOES_BANCO_POS_PATCH.md`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L12: `SELECT COUNT(*) FROM payoff_curve_points;`
- L13: `SELECT COUNT(*) FROM structure_decisions;`
- L21: `SELECT MAX(timestamp) FROM payoff_curve_points;`
- L22: `SELECT MAX(timestamp) FROM structure_decisions;`
- L30: `FROM payoff_curve_points`
- L42: `FROM payoff_curve_points p`
- L43: `LEFT JOIN structure_decisions d`
- L60: `FROM structure_decisions d`
- L61: `LEFT JOIN payoff_curve_points p`
- L77: `FROM payoff_curve_points`
- L90: `FROM payoff_curve_points`
- L96: `Essa verificação exige cruzar pricing_executions com payoff_curve_points por structure_id e janela temporal.`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/29_CLASSIFICACAO_SCRIPTS.md`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L27: `scripts/diagnose_payoff_curve_points.py`
- L57: `db/migrations/add_structure_id_to_payoff_curve_points.py`
- L72: `scripts/recalculate_payoff_curve_points_once.py`
- L73: `scripts/recalculate_payoff_curve_points_once_checked.py`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/30_CRITERIOS_DE_ACEITE_SOLUCAO.md`

Tokens:
- `PayoffRefreshCommandService`
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L11: `PayoffRefreshCommandService.refresh_payoff_for_structure`
- L33: `- payoff_curve_points;`
- L34: `- structure_decisions;`
- L39: `Para snapshot novo, payoff_curve_points e structure_decisions devem compartilhar:`
- L95: `- DerivedPayoffPersistence não estiver no wiring;`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/31_AUDITORIA_FRENTE_07_PERSISTENCIA_PAYOFF_20260717_130631.md`

Tokens:
- `PayoffRefreshCommandService`
- `PricingExecutionAppService`
- `PricingExecutionOrchestrationService`
- `PricingExecutionService`
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `structure_decisions`
- `execute_pricing`
- `derived_payoff`
- `payoff_curve`

Linhas relevantes:
- L9: `Investigar por que a execução de pricing grava pricing_executions e structure_snapshots, mas DerivedPayoffPersistence informa payoff sem pontos e payoff_curve_points não aumenta.`
- L14: `M scripts/recalculate_payoff_curve_points_once.py`
- L31: `diff --git a/scripts/recalculate_payoff_curve_points_once.py b/scripts/recalculate_payoff_curve_points_once.py`
- L33: `--- a/scripts/recalculate_payoff_curve_points_once.py`
- L34: `+++ b/scripts/recalculate_payoff_curve_points_once.py`
- L40: `+Recalcula payoff_curve_points usando cotações RTD atuais.`
- L48: `+- Gerar um novo snapshot econômico real em payoff_curve_points.`
- L71: `-        description="Recalcula payoff das estruturas e grava em payoff_curve_points."`
- L182: `-        row = conn.execute("SELECT COUNT(*) AS n FROM payoff_curve_points").fetchone()`
- L423: `-    from services.pricing_execution_app_service import PricingExecutionAppService`
- L650: `-    service = PricingExecutionAppService()`
- L659: `-            result = service.execute_pricing(structure_id=sid)`
- L676: `+    if not table_exists(conn, "payoff_curve_points"):`
- L679: `+    row = conn.execute("SELECT COUNT(*) AS n FROM payoff_curve_points").fetchone()`
- L686: `+        CREATE TABLE IF NOT EXISTS payoff_curve_points (`
- L727: `+        "source": "recalculate_payoff_curve_points_once.rtd",`
- L744: `+        "created_by": "scripts/recalculate_payoff_curve_points_once.py",`
- L771: `+        INSERT INTO payoff_curve_points (`
- L848: `+        description="Recalcula payoff_curve_points usando rtd_option_quotes e rtd_underlying_quotes."`
- L964: `from services.pricing_execution_service import PricingExecutionService`
- L966: `+from services.derived_payoff_persistence import DerivedPayoffPersistence`
- L969: `class PricingExecutionOrchestrationService:`
- L970: `@@ -23,6 +24,7 @@ class PricingExecutionOrchestrationService:`
- L974: `+                payoff_persistence_port=DerivedPayoffPersistence(),`
- L1056: `scripts/gerar_auditoria_frente_07_persistencia_payoff.py:300:        "mas o objeto entregue ao DerivedPayoffPersistence não contém payoff_points no "`
- L1079: `scripts/recalculate_payoff_curve_points_once.py:807:            f"payoff_points_before={before} "`
- L1080: `scripts/recalculate_payoff_curve_points_once.py:808:            f"payoff_points_after={after}"`
- L1081: `scripts/recalculate_payoff_curve_points_once_checked.py:271:    print(f"[checked] payoff_points_before={before_count}")`
- L1082: `scripts/recalculate_payoff_curve_points_once_checked.py:272:    print(f"[checked] payoff_points_after={after_count}")`
- L1083: `scripts/recalculate_payoff_curve_points_once_checked.py:326:    print(f"[checked] payoff_points_final={final_count}")`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/AUDITORIA_UI_PAYOFF_FOCADA_33_20260717_190013/12_arquivos_chave/UI__components__payoff_chart.py`

Tokens:
- `payoff_curve`

Linhas relevantes:
- L275: `self._log_rebuilt_payoff_curve(xs, ys)`
- L276: `self._draw_main_payoff_curve(xs, ys, decision_data, overlay_curve)`
- L317: `def _log_rebuilt_payoff_curve(self, xs: List[float], ys: List[float]) -> None:`
- L325: `def _draw_main_payoff_curve(`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/AUDITORIA_UI_PAYOFF_FOCADA_33_20260717_190013/12_arquivos_chave/UI__components__terminal_vwap_payoff_dark_panel.py`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L1171: `"payoff_curve_points",`
- L1201: `if table == "payoff_curve_points" and ts_col == "timestamp":`
- L1905: `def _ensure_structure_decisions_table(self, conn: sqlite3.Connection) -> None:`
- L1908: `CREATE TABLE IF NOT EXISTS structure_decisions (`
- L1920: `CREATE INDEX IF NOT EXISTS idx_structure_decisions_structure_id`
- L1921: `ON structure_decisions(structure_id)`
- L1934: `self._ensure_structure_decisions_table(conn)`
- L1937: `INSERT INTO structure_decisions (`
- L1955: `def _load_structure_decisions(self, sid: int, limit: int = 5) -> List[Dict[str, Any]]:`
- L1957: `self._ensure_structure_decisions_table(conn)`
- L1967: `FROM structure_decisions`
- L1986: `rows = self._load_structure_decisions(int(sid), limit=5)`
- L2749: `FROM payoff_curve_points`
- L2761: `FROM payoff_curve_points`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/AUDITORIA_UI_PAYOFF_FOCADA_33_20260717_190013/12_arquivos_chave/db__derived_repo.py`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L4: `Tabelas: payoff_curve_points, structure_decisions`
- L80: `# alteracao_36_A: adicionar structure_id ao DDL de payoff_curve_points`
- L83: `CREATE TABLE IF NOT EXISTS payoff_curve_points (`
- L97: `ON payoff_curve_points (timestamp, aba, point_spot)`
- L103: `ON payoff_curve_points (structure_id, timestamp)`
- L107: `CREATE TABLE IF NOT EXISTS structure_decisions (`
- L128: `ON structure_decisions (timestamp, aba)`
- L133: `ON structure_decisions (aba, timestamp)`
- L138: `ON structure_decisions (timestamp)`
- L144: `"ALTER TABLE payoff_curve_points ADD COLUMN structure_id INTEGER"`
- L183: `# alteracao_36_A: migration incremental payoff_curve_points`
- L184: `existing_cols = _table_columns(conn, "payoff_curve_points")`
- L198: `# Índices de structure_decisions`
- L304: `"DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`
- L360: `"DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L365: `INSERT INTO payoff_curve_points`
- L408: `INSERT OR REPLACE INTO payoff_curve_points`
- L454: `"DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L459: `INSERT INTO payoff_curve_points`
- L480: `"DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`
- L506: `FROM payoff_curve_points`
- L516: `FROM payoff_curve_points`
- L527: `FROM payoff_curve_points`
- L568: `f"SELECT * FROM structure_decisions {where} ORDER BY id DESC LIMIT ?",`
- L585: `FROM structure_decisions d`
- L586: `LEFT JOIN payoff_curve_points p`
- L594: `FROM payoff_curve_points p`
- L595: `LEFT JOIN structure_decisions d`
- L617: `f"DELETE FROM payoff_curve_points "`
- L629: `f"DELETE FROM structure_decisions "`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/AUDITORIA_UI_PAYOFF_FOCADA_33_20260717_190013/12_arquivos_chave/services__derived_payoff_persistence.py`

Tokens:
- `DerivedPayoffPersistence`
- `derived_payoff`

Linhas relevantes:
- L1: `# services/derived_payoff_persistence.py`
- L15: `class DerivedPayoffPersistence:`
- L36: `logger.debug("derived_payoff_persistence: pricing_payload vazio, skip.")`
- L43: `"derived_payoff_persistence: status=%r não elegível para payoff, skip.",`
- L51: `"derived_payoff_persistence: structure_id ausente; persistência bloqueada."`
- L57: `"derived_payoff_persistence: estrutura inativa/arquivada; "`
- L70: `"derived_payoff_persistence: decisão não gravada porque payoff não foi salvo -- structure_id=%s",`
- L78: `"derived_payoff_persistence: payoff salvo, mas decisão falhou -- structure_id=%s timestamp=%s",`
- L99: `"derived_payoff_persistence: payoff sem pontos para structure_id=%s",`
- L106: `"derived_payoff_persistence: %d pontos gravados -- structure_id=%s",`
- L114: `"derived_payoff_persistence: erro ao gravar payoff -- structure_id=%s",`
- L213: `"derived_payoff_persistence: decisão gravada -- structure_id=%s",`
- L220: `"derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s",`
- L254: `# services/derived_payoff_persistence.py -> raiz do projeto -> dados/app.db`
- L270: `"derived_payoff_persistence: app.db não encontrado para validar structure_id=%s -- db_path=%s",`
- L291: `"derived_payoff_persistence: structure_id=%s não encontrada; persistência bloqueada.",`
- L301: `"derived_payoff_persistence: falha ao validar status da estrutura -- structure_id=%s",`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/AUDITORIA_UI_PAYOFF_FOCADA_33_20260717_190013/12_arquivos_chave/services__payoff_refresh_command_service.py`

Tokens:
- `PayoffRefreshCommandService`
- `PricingExecutionAppService`
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `structure_decisions`
- `execute_pricing`
- `payoff_curve`

Linhas relevantes:
- L8: `from services.pricing_execution_app_service import PricingExecutionAppService`
- L11: `class PayoffRefreshCommandService:`
- L18: `- Este serviço chama PricingExecutionAppService.`
- L25: `pricing_app_service: PricingExecutionAppService | None = None,`
- L28: `self.pricing_app_service = pricing_app_service or PricingExecutionAppService()`
- L41: `pricing_result = self._execute_pricing(structure_id, reference_date)`
- L91: `"Verifique o wiring de DerivedPayoffPersistence."`
- L126: `def _execute_pricing(`
- L131: `method = self.pricing_app_service.execute_pricing`
- L205: `FROM payoff_curve_points`
- L240: `FROM structure_decisions`
- L249: `FROM structure_decisions`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/AUDITORIA_UI_PAYOFF_FOCADA_33_20260717_190013/RESUMO_AUDITORIA_UI_PAYOFF_FOCADA_33.md`

Tokens:
- `PayoffRefreshCommandService`
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `execute_pricing`
- `payoff_curve`

Linhas relevantes:
- L13: `- Referências PayoffRefreshCommandService/refresh: 2`
- L14: `- Referências DerivedPayoffPersistence: 28`
- L15: `- execute_pricing produtivo: 9`
- L16: `- execute_pricing na UI: 0`
- L17: `- SQL direto payoff_curve_points produtivo: 10`
- L18: `- SQL direto payoff_curve_points na UI: 0`
- L24: `1. 08_sql_direto_payoff_curve_points_ui.txt`
- L25: `2. 06_execute_pricing_na_ui.txt`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/RELATORIO_EVOLUCAO_RODADA_PAYOFF_20260717_130251.md`

Tokens:
- `PayoffRefreshCommandService`
- `PricingExecutionAppService`
- `PricingExecutionOrchestrationService`
- `PricingExecutionService`
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `structure_decisions`
- `execute_pricing`
- `derived_payoff`
- `payoff_curve`

Linhas relevantes:
- L15: `- 5. O cálculo de payoff passou a ser proibido na camada de UI, reforçando o uso de PayoffRefreshCommandService.`
- L17: `- 7. PricingExecutionOrchestrationService passou a injetar DerivedPayoffPersistence no PricingExecutionPersistenceService.`
- L19: `- 9. Validação de integridade executou e revelou divergência entre payoff_curve_points e structure_decisions.`
- L22: `- 12. O script recalculate_payoff_curve_points_once.py foi evoluído para recalcular payoff_curve_points usando RTD atual.`
- L29: `- A validação de integridade mostra que payoff_curve_points existe e possui structure_id preenchido.`
- L41: `- 2. Validar se DerivedPayoffPersistence está recebendo o payload correto do PricingExecutionPersistenceService.`
- L42: `- 3. Investigar por que DerivedPayoffPersistence reportou: payoff sem pontos para structure_id=2.`
- L44: `- 5. Garantir que PayoffRefreshCommandService seja o único caminho de refresh acionado pela UI.`
- L46: `- 7. Executar recalculate_payoff_curve_points_once.py somente de forma controlada, pois ele grava novos snapshots.`
- L71: `M scripts/recalculate_payoff_curve_points_once.py`
- L74: `?? DerivedPayoffPersistence`
- L76: `?? PayoffRefreshCommandService`
- L77: `?? PricingExecutionAppService`
- L78: `?? PricingExecutionOrchestrationService`
- L80: `?? PricingExecutionService`
- L85: `?? payoff_curve_points`
- L95: `?? structure_decisions`
- L124: `scripts/recalculate_payoff_curve_points_once.py    | 869 ++++++++++++++++++---`
- L145: `from services.pricing_execution_service import PricingExecutionService`
- L147: `+from services.derived_payoff_persistence import DerivedPayoffPersistence`
- L150: `class PricingExecutionOrchestrationService:`
- L151: `@@ -23,6 +24,7 @@ class PricingExecutionOrchestrationService:`
- L155: `+                payoff_persistence_port=DerivedPayoffPersistence(),`
- L199: `+            "CÃ¡lculo de payoff na UI Ã© proibido. Use PayoffRefreshCommandService."`
- L222: `+            "CÃ¡lculo de payoff na UI Ã© proibido. Use PayoffRefreshCommandService."`
- L246: `+            "CÃ¡lculo de payoff na UI Ã© proibido. Use PayoffRefreshCommandService."`
- L261: `Diff do arquivo: scripts/recalculate_payoff_curve_points_once.py`
- L266: `git diff -- scripts/recalculate_payoff_curve_points_once.py`
- L270: `diff --git a/scripts/recalculate_payoff_curve_points_once.py b/scripts/recalculate_payoff_curve_points_once.py`
- L272: `--- a/scripts/recalculate_payoff_curve_points_once.py`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/SOLICITACAO_CORRECAO_POS_AUDITORIA_33_20260717_192449/RESUMO_SOLICITACAO_CORRECAO_POS_AUDITORIA_33.md`

Tokens:
- `PayoffRefreshCommandService`
- `PricingExecutionAppService`
- `PricingExecutionOrchestrationService`
- `PricingExecutionService`
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `structure_decisions`
- `execute_pricing`
- `derived_payoff`
- `payoff_curve`

Linhas relevantes:
- L26: `-> PayoffRefreshCommandService`
- L27: `-> PricingExecutionAppService`
- L28: `-> PricingExecutionOrchestrationService`
- L29: `-> PricingExecutionService`
- L33: `-> DerivedPayoffPersistence`
- L34: `-> payoff_curve_points`
- L35: `-> structure_decisions`
- L51: `- gravar em payoff_curve_points;`
- L52: `- gravar em structure_decisions;`
- L60: `| Wiring DerivedPayoffPersistence | 31 | greps/01_wiring_derived_payoff_persistence.txt |`
- L61: `| PayoffRefresh / execute_pricing | 11 | greps/02_payoff_refresh_e_execute_pricing.txt |`
- L76: `1. DerivedPayoffPersistence está realmente conectado ao fluxo padrão?`
- L78: `3. PayoffRefreshCommandService chama PricingExecutionAppService.execute_pricing()?`
- L79: `4. O comando valida se payoff_curve_points aumentou ou se há último timestamp novo?`
- L81: `6. DerivedPayoffPersistence apenas persiste pontos prontos ou também monta/calcula o payoff derivado?`
- L89: `4. A UI escreve em payoff_curve_points ou structure_decisions?`
- L95: `1. scripts/recalculate_payoff_curve_points_once.py está sendo chamado pela UI?`
- L102: `2. Confirmar wiring de DerivedPayoffPersistence.`
- L104: `4. Consolidar PayoffRefreshCommandService.`
- L115: `- arquivos_chave/04_derived_payoff_persistence.py.txt`
- L120: `- arquivos_chave/09_recalculate_payoff_curve_points_once.py.txt`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/SOLICITACAO_CORRECAO_POS_AUDITORIA_33_20260717_192449/solicitacao/PROMPT_CORRECAO_CENTRO_DE_VERDADE.md`

Tokens:
- `PayoffRefreshCommandService`
- `PricingExecutionAppService`
- `PricingExecutionOrchestrationService`
- `PricingExecutionService`
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `structure_decisions`
- `execute_pricing`
- `payoff_curve`

Linhas relevantes:
- L22: `-> PayoffRefreshCommandService`
- L23: `-> PricingExecutionAppService`
- L24: `-> PricingExecutionOrchestrationService`
- L25: `-> PricingExecutionService`
- L29: `-> DerivedPayoffPersistence`
- L30: `-> payoff_curve_points`
- L31: `-> structure_decisions`
- L36: `1. Confirmar se o wiring de DerivedPayoffPersistence está correto.`
- L37: `2. Confirmar se PayoffRefreshCommandService é o comando oficial ou precisa ajuste.`
- L38: `3. Confirmar se execute_pricing gera e persiste payoff sem depender da UI.`
- L39: `4. Identificar se DerivedPayoffPersistence recebe payoff_points prontos ou precisa montar o derivado.`
- L42: `7. Detectar escrita direta da UI em payoff_curve_points ou structure_decisions.`
- L45: `10. Classificar scripts/recalculate_payoff_curve_points_once.py como maintenance/legacy/emergência se ele for motor paralelo.`
- L52: `- Backend executa pricing e persiste payoff_curve_points.`
- L53: `- PayoffRefreshCommandService retorna ok/warning/error sem sucesso silencioso.`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/auditoria_fase5_mapa_lacunas_ui_operacional.md`

Tokens:
- `payoff_curve_points`
- `derived_payoff`
- `payoff_curve`

Linhas relevantes:
- L472: `ATT/tests/check_cleanup_residuals.py:76:    "scripts/patch_derived_payoff_timestamp_consistency.sh",`
- L479: `ATT/tests/test_bd_unico_absorcao_funcional.py:18:    "payoff_curve_points",`
- L480: `ATT/tests/test_bd_unico_absorcao_funcional.py:48:    "payoff_curve_points": {`
- L493: `ATT/tests/test_bd_unico_absorcao_funcional.py:274:                FROM payoff_curve_points`
- L495: `ATT/tests/test_bd_unico_artifacts_in_app_db.py:28:    "payoff_curve_points",`
- L500: `ATT/tests/test_bd_unico_artifacts_in_app_db.py:135:    assert "payoff_curve_points" in tables, (`
- L501: `ATT/tests/test_bd_unico_artifacts_in_app_db.py:136:        "A tabela canonica payoff_curve_points deve existir em dados/app.db."`
- L502: `ATT/tests/test_bd_unico_artifacts_in_app_db.py:139:    cols = _sqlite_columns(APP_DB, "payoff_curve_points")`
- L504: `ATT/tests/test_bd_unico_artifacts_in_app_db.py:143:        "payoff_curve_points em dados/app.db nao possui colunas canonicas "`
- L506: `ATT/tests/test_bd_unico_artifacts_in_app_db.py:209:    assert "payoff_curve_points" in ui_text, (`
- L507: `ATT/tests/test_bd_unico_artifacts_in_app_db.py:210:        "UI/models/ui_data.py deve reconhecer payoff_curve_points como tabela "`
- L511: `ATT/tests/test_bd_unico_artifacts_in_app_db.py:223:    assert "payoff_curve_points" in details_text, (`
- L512: `ATT/tests/test_bd_unico_artifacts_in_app_db.py:224:        "details_panel deve consultar payoff_curve_points no app.db."`
- L513: `ATT/tests/test_database_retention_simulation_service.py:18:        CREATE TABLE payoff_curve_points (`
- L514: `ATT/tests/test_database_retention_simulation_service.py:44:        "INSERT INTO payoff_curve_points (timestamp, created_at) VALUES (?, ?)",`
- L515: `ATT/tests/test_database_retention_simulation_service.py:73:    assert _table(report, "payoff_curve_points")["candidate_count"] == 1`
- L516: `ATT/tests/test_database_retention_simulation_service.py:130:        CREATE TABLE payoff_curve_points (`
- L517: `ATT/tests/test_database_retention_simulation_service.py:138:        "INSERT INTO payoff_curve_points (timestamp, created_at) VALUES (?, ?)",`
- L518: `ATT/tests/test_database_retention_simulation_service.py:146:        "SELECT COUNT(*) FROM payoff_curve_points"`
- L519: `ATT/tests/test_database_retention_simulation_service.py:158:        "SELECT COUNT(*) FROM payoff_curve_points"`
- L520: `ATT/tests/test_database_retention_simulation_service.py:162:    assert _table(report, "payoff_curve_points")["candidate_count"] == 1`
- L521: `ATT/tests/test_database_retention_simulation_service.py:256:        CREATE TABLE payoff_curve_points (`
- L522: `ATT/tests/test_database_retention_simulation_service.py:263:        "INSERT INTO payoff_curve_points (timestamp) VALUES (?)",`
- L523: `ATT/tests/test_database_retention_simulation_service.py:277:    assert "Tabela: payoff_curve_points" in text`
- L531: `ATT/tests/test_derived_service.py:89:    def fake_save_payoff_curve(ref, points, spot_ref=None, meta=None, timestamp=None):`
- L532: `ATT/tests/test_derived_service.py:97:    monkeypatch.setattr(ds, "save_payoff_curve", fake_save_payoff_curve)`
- L542: `ATT/tests/test_operational_observability_presentation.py:46:            "payoff_curve_points": False,`
- L543: `ATT/tests/test_operational_observability_presentation.py:54:        ("payoff_curve_points", "ausente"),`
- L544: `ATT/tests/test_operational_observability_query.py:133:            "payoff_curve_points": True,`
- L545: `ATT/tests/test_operational_observability_service.py:79:            "CREATE TABLE payoff_curve_points (id INTEGER PRIMARY KEY, timestamp TEXT)"`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/auditoria_fase5_precheck_ui_operacional.md`

Tokens:
- `structure_decisions`
- `execute_pricing`
- `derived_payoff`

Linhas relevantes:
- L1301: `services/derived_payoff_persistence.py:46:        # Evita snapshots inconsistentes por diferença de milissegundos entre gravações.`
- L1302: `services/derived_payoff_persistence.py:47:        snapshot_ts = datetime.now(timezone.utc).isoformat()`
- L1303: `services/derived_payoff_persistence.py:49:        payoff_saved = self._persist_payoff(pricing_payload, result, snapshot_ts)`
- L1304: `services/derived_payoff_persistence.py:57:        decision_saved = self._persist_decision(pricing_payload, result, snapshot_ts)`
- L1305: `services/derived_payoff_persistence.py:62:                snapshot_ts,`
- L1306: `services/derived_payoff_persistence.py:73:        snapshot_ts: str,`
- L1307: `services/derived_payoff_persistence.py:86:            save_payoff_from_canonical_payload(payoff_result, timestamp=snapshot_ts)`
- L1308: `services/derived_payoff_persistence.py:109:        snapshot_ts: str,`
- L1309: `services/derived_payoff_persistence.py:163:                timestamp=snapshot_ts,`
- L1615: `UI/components/terminal_vwap_payoff_dark_panel.py:1606:    def _ensure_structure_decisions_table(self, conn: sqlite3.Connection) -> None:`
- L1954: `ATT/tests/test_pricing_execution_app_service.py:186:def test_execute_pricing_raises_value_error_when_orchestration_returns_error_status():`
- L2620: `services/derived_payoff_persistence.py:37:        status = inner.get("status", "")`
- L2621: `services/derived_payoff_persistence.py:38:        if status not in ("success", "ok", "completed"):`
- L2622: `services/derived_payoff_persistence.py:40:                "derived_payoff_persistence: status=%r não elegível para payoff, skip.",`
- L2623: `services/derived_payoff_persistence.py:41:                status,`
- L2624: `services/derived_payoff_persistence.py:147:                    "execution_status": inner.get("status"),`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase7_00_varredura_limpa_adiantamentos_20260713.md`

Tokens:
- `derived_payoff`

Linhas relevantes:
- L689: `### services/derived_payoff_persistence.py`
- L702: `- Linha 52 [decisao]: "derived_payoff_persistence: decisão não gravada porque payoff não foi salvo -- structure_id=%s",`
- L703: `- Linha 60 [decisao]: "derived_payoff_persistence: payoff salvo, mas decisão falhou -- structure_id=%s timestamp=%s",`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/solicitacao_auditoria_payoff_20260717_192927/00_SOLICITACAO_AUTOMATIZADA.md`

Tokens:
- `PayoffRefreshCommandService`
- `PricingExecutionAppService`
- `PricingExecutionOrchestrationService`
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `structure_decisions`
- `execute_pricing`
- `derived_payoff`
- `payoff_curve`

Linhas relevantes:
- L16: `4. A persistência derivada deve gravar pontos em `payoff_curve_points`.`
- L17: `5. A decisão deve ser persistida em `structure_decisions` com o mesmo timestamp do payoff, quando aplicável.`
- L23: `### 1. O `PayoffRefreshCommandService` está realmente ligado ao fluxo oficial?`
- L25: `Verificar se `PayoffRefreshCommandService.refresh_payoff_for_structure()` é chamado por UI, controller, script ou serviço operacional.`
- L33: `- chamadas a `PayoffRefreshCommandService`;`
- L35: `- ausência de chamadas diretas da UI para `execute_pricing()`.`
- L39: `### 2. O `PricingExecutionAppService` usa a orquestração oficial?`
- L41: `Verificar se `PricingExecutionAppService.execute_pricing()` passa por:`
- L43: `- `PricingExecutionOrchestrationService.execute_and_persist()`;`
- L55: `> O `payoff_persistence_port` recebe uma instância concreta de `DerivedPayoffPersistence` no wiring oficial?`
- L59: `### 3. O `DerivedPayoffPersistence` calcula ou apenas persiste?`
- L61: `No arquivo analisado, `DerivedPayoffPersistence` monta input canônico e chama:`
- L69: `- `services/derived_payoff_persistence.py``
- L75: `- backend calcula e `DerivedPayoffPersistence` apenas persiste?`
- L76: `- ou `DerivedPayoffPersistence` é considerado parte do backend e pode calcular?`
- L125: `- uso de `payoff_curve_points`;`
- L134: `No arquivo `DerivedPayoffPersistence`, existe `snapshot_ts` único usado para payoff e decisão.`
- L138: `- `services/derived_payoff_persistence.py``
- L144: `3. se `structure_decisions` grava o `structure_id` corretamente.`
- L152: `- `PayoffRefreshCommandService._ensure_active_structure``
- L153: `- `DerivedPayoffPersistence._is_active_structure``
- L154: `- `scripts/recalculate_payoff_curve_points_once.py``
- L178: `1. `01_chamadas_execute_pricing.txt``
- L180: `3. `03_persistencia_payoff_curve_points.txt``
- L195: `1. O fluxo oficial realmente gera `payoff_curve_points`?`
- L196: `2. O `payoff_persistence_port` está conectado ao `DerivedPayoffPersistence`?`
- L199: `5. O `DerivedPayoffPersistence` está violando ou cumprindo o contrato esperado?`
- L204: `10. O script `recalculate_payoff_curve_points_once.py` usa o fluxo oficial ou apenas contorna o problema?`
- L214: `- O `DerivedPayoffPersistence` atualmente calcula payoff a partir do payload, o que precisa ser validado contra o contrato desejado.`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/solicitacao_auditoria_payoff_20260717_192927/arquivos_chave/UI/components/details_panel.py`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L309: `"structure_decisions",`
- L310: `"payoff_curve_points",`
- L982: `alteracao_36: filtra por structure_id (INTEGER) em structure_decisions.`
- L1000: `FROM structure_decisions`
- L1022: `alteracao_36: filtra por structure_id (INTEGER) em payoff_curve_points.`
- L1034: `FROM payoff_curve_points`
- L1062: `FROM structure_decisions`
- L1075: `"SELECT COUNT(*) AS n FROM payoff_curve_points WHERE structure_id = ?",`
- L1080: `"source_table": "app.db:structure_decisions / payoff_curve_points",`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/solicitacao_auditoria_payoff_20260717_192927/arquivos_chave/UI/components/payoff_chart.py`

Tokens:
- `payoff_curve`

Linhas relevantes:
- L275: `self._log_rebuilt_payoff_curve(xs, ys)`
- L276: `self._draw_main_payoff_curve(xs, ys, decision_data, overlay_curve)`
- L317: `def _log_rebuilt_payoff_curve(self, xs: List[float], ys: List[float]) -> None:`
- L325: `def _draw_main_payoff_curve(`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/solicitacao_auditoria_payoff_20260717_192927/arquivos_chave/UI/components/terminal_vwap_payoff_dark_panel.py`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L1171: `"payoff_curve_points",`
- L1201: `if table == "payoff_curve_points" and ts_col == "timestamp":`
- L1905: `def _ensure_structure_decisions_table(self, conn: sqlite3.Connection) -> None:`
- L1908: `CREATE TABLE IF NOT EXISTS structure_decisions (`
- L1920: `CREATE INDEX IF NOT EXISTS idx_structure_decisions_structure_id`
- L1921: `ON structure_decisions(structure_id)`
- L1934: `self._ensure_structure_decisions_table(conn)`
- L1937: `INSERT INTO structure_decisions (`
- L1955: `def _load_structure_decisions(self, sid: int, limit: int = 5) -> List[Dict[str, Any]]:`
- L1957: `self._ensure_structure_decisions_table(conn)`
- L1967: `FROM structure_decisions`
- L1986: `rows = self._load_structure_decisions(int(sid), limit=5)`
- L2749: `FROM payoff_curve_points`
- L2761: `FROM payoff_curve_points`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/solicitacao_auditoria_payoff_20260717_192927/arquivos_chave/UI/main_window.py`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L223: `points, info_dict = self.data_model.get_payoff_curve_info(`
- L558: `src = (info_dict or {}).get("source_table", "payoff_curve_points")`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/solicitacao_auditoria_payoff_20260717_192927/arquivos_chave/UI/models/ui_data.py`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L131: `if self._payoff_table == "payoff_curve_points":`
- L475: `def _payoff_curve_cache_key(`
- L481: `def _get_payoff_curve_from_cache(`
- L492: `def _ensure_payoff_curve_available(self) -> None:`
- L499: `def _ensure_payoff_curve_columns(self, p: Dict[str, str]) -> None:`
- L506: `def _build_payoff_curve_exact_sql(`
- L516: `def _fetch_payoff_curve_exact_rows(`
- L524: `sql_exact = self._build_payoff_curve_exact_sql(p, filter_col)`
- L527: `def _build_payoff_curve_latest_timestamp_sql(`
- L538: `def _fetch_payoff_curve_latest_timestamp(`
- L541: `sql_ts = self._build_payoff_curve_latest_timestamp_sql(p, filter_col)`
- L544: `def _payoff_curve_rows_to_dicts(self, rows) -> List[Dict]:`
- L547: `def _cache_payoff_curve_result(`
- L553: `def _load_payoff_curve_fallback(`
- L561: `row_ts = self._fetch_payoff_curve_latest_timestamp(`
- L565: `return self._cache_payoff_curve_result(cache_key, [])`
- L568: `rows = self._fetch_payoff_curve_exact_rows(`
- L571: `return self._cache_payoff_curve_result(`
- L572: `cache_key, self._payoff_curve_rows_to_dicts(rows)`
- L575: `def _load_payoff_curve_uncached(`
- L583: `self._ensure_payoff_curve_columns(p)`
- L588: `rows = self._fetch_payoff_curve_exact_rows(`
- L592: `return self._cache_payoff_curve_result(`
- L593: `cache_key, self._payoff_curve_rows_to_dicts(rows)`
- L596: `return self._load_payoff_curve_fallback(`
- L600: `def get_payoff_curve(self, structure_id: str, timestamp: str) -> List[Dict]:`
- L606: `cache_key = self._payoff_curve_cache_key(structure_id, timestamp)`
- L607: `cached = self._get_payoff_curve_from_cache(cache_key)`
- L611: `self._ensure_payoff_curve_available()`
- L616: `return self._load_payoff_curve_uncached(`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/solicitacao_auditoria_payoff_20260717_192927/arquivos_chave/db/derived_repo.py`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L4: `Tabelas: payoff_curve_points, structure_decisions`
- L80: `# alteracao_36_A: adicionar structure_id ao DDL de payoff_curve_points`
- L83: `CREATE TABLE IF NOT EXISTS payoff_curve_points (`
- L97: `ON payoff_curve_points (timestamp, aba, point_spot)`
- L103: `ON payoff_curve_points (structure_id, timestamp)`
- L107: `CREATE TABLE IF NOT EXISTS structure_decisions (`
- L128: `ON structure_decisions (timestamp, aba)`
- L133: `ON structure_decisions (aba, timestamp)`
- L138: `ON structure_decisions (timestamp)`
- L144: `"ALTER TABLE payoff_curve_points ADD COLUMN structure_id INTEGER"`
- L183: `# alteracao_36_A: migration incremental payoff_curve_points`
- L184: `existing_cols = _table_columns(conn, "payoff_curve_points")`
- L198: `# Índices de structure_decisions`
- L304: `"DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`
- L360: `"DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L365: `INSERT INTO payoff_curve_points`
- L408: `INSERT OR REPLACE INTO payoff_curve_points`
- L454: `"DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L459: `INSERT INTO payoff_curve_points`
- L480: `"DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`
- L506: `FROM payoff_curve_points`
- L516: `FROM payoff_curve_points`
- L527: `FROM payoff_curve_points`
- L568: `f"SELECT * FROM structure_decisions {where} ORDER BY id DESC LIMIT ?",`
- L585: `FROM structure_decisions d`
- L586: `LEFT JOIN payoff_curve_points p`
- L594: `FROM payoff_curve_points p`
- L595: `LEFT JOIN structure_decisions d`
- L617: `f"DELETE FROM payoff_curve_points "`
- L629: `f"DELETE FROM structure_decisions "`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/solicitacao_auditoria_payoff_20260717_192927/arquivos_chave/domain/payoff.py`

Tokens:
- `payoff_curve`

Linhas relevantes:
- L51: `def compute_payoff_curve_from_canonical_legs(`
- L157: `result = compute_payoff_curve_from_canonical_legs(`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/solicitacao_auditoria_payoff_20260717_192927/arquivos_chave/scripts/recalculate_payoff_curve_points_once.py`

Tokens:
- `PricingExecutionAppService`
- `payoff_curve_points`
- `execute_pricing`
- `payoff_curve`

Linhas relevantes:
- L16: `description="Recalcula payoff das estruturas e grava em payoff_curve_points."`
- L115: `row = conn.execute("SELECT COUNT(*) AS n FROM payoff_curve_points").fetchone()`
- L142: `from services.pricing_execution_app_service import PricingExecutionAppService`
- L164: `service = PricingExecutionAppService()`
- L172: `result = service.execute_pricing(structure_id=sid)`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/solicitacao_auditoria_payoff_20260717_192927/arquivos_chave/services/derived_payoff_persistence.py`

Tokens:
- `DerivedPayoffPersistence`
- `derived_payoff`

Linhas relevantes:
- L1: `# services/derived_payoff_persistence.py`
- L15: `class DerivedPayoffPersistence:`
- L36: `logger.debug("derived_payoff_persistence: pricing_payload vazio, skip.")`
- L43: `"derived_payoff_persistence: status=%r não elegível para payoff, skip.",`
- L51: `"derived_payoff_persistence: structure_id ausente; persistência bloqueada."`
- L57: `"derived_payoff_persistence: estrutura inativa/arquivada; "`
- L70: `"derived_payoff_persistence: decisão não gravada porque payoff não foi salvo -- structure_id=%s",`
- L78: `"derived_payoff_persistence: payoff salvo, mas decisão falhou -- structure_id=%s timestamp=%s",`
- L99: `"derived_payoff_persistence: payoff sem pontos para structure_id=%s",`
- L106: `"derived_payoff_persistence: %d pontos gravados -- structure_id=%s",`
- L114: `"derived_payoff_persistence: erro ao gravar payoff -- structure_id=%s",`
- L213: `"derived_payoff_persistence: decisão gravada -- structure_id=%s",`
- L220: `"derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s",`
- L254: `# services/derived_payoff_persistence.py -> raiz do projeto -> dados/app.db`
- L270: `"derived_payoff_persistence: app.db não encontrado para validar structure_id=%s -- db_path=%s",`
- L291: `"derived_payoff_persistence: structure_id=%s não encontrada; persistência bloqueada.",`
- L301: `"derived_payoff_persistence: falha ao validar status da estrutura -- structure_id=%s",`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/solicitacao_auditoria_payoff_20260717_192927/arquivos_chave/services/derived_service.py`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L160: `def save_payoff_curve(`
- L242: `sig = inspect.signature(save_payoff_curve)`
- L254: `return save_payoff_curve(`
- L263: `return save_payoff_curve(`
- L362: `def get_all_payoff_curves():`
- L367: `FROM payoff_curve_points`
- L394: `FROM payoff_curve_points`
- L419: `"PRAGMA table_info(structure_decisions)"`
- L437: `FROM structure_decisions`
- L522: `def save_payoff_curve(self, *args, **kwargs):`
- L523: `return save_payoff_curve(*args, **kwargs)`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/solicitacao_auditoria_payoff_20260717_192927/arquivos_chave/services/payoff_refresh_command_service.py`

Tokens:
- `PayoffRefreshCommandService`
- `PricingExecutionAppService`
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `structure_decisions`
- `execute_pricing`
- `payoff_curve`

Linhas relevantes:
- L8: `from services.pricing_execution_app_service import PricingExecutionAppService`
- L11: `class PayoffRefreshCommandService:`
- L18: `- Este serviço chama PricingExecutionAppService.`
- L25: `pricing_app_service: PricingExecutionAppService | None = None,`
- L28: `self.pricing_app_service = pricing_app_service or PricingExecutionAppService()`
- L41: `pricing_result = self._execute_pricing(structure_id, reference_date)`
- L91: `"Verifique o wiring de DerivedPayoffPersistence."`
- L126: `def _execute_pricing(`
- L131: `method = self.pricing_app_service.execute_pricing`
- L205: `FROM payoff_curve_points`
- L240: `FROM structure_decisions`
- L249: `FROM structure_decisions`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/solicitacao_auditoria_payoff_20260717_192927/arquivos_chave/services/pricing_execution_app_service.py`

Tokens:
- `PricingExecutionAppService`
- `PricingExecutionOrchestrationService`
- `execute_pricing`

Linhas relevantes:
- L3: `execute_pricing() delegado para PricingExecutionOrchestrationService.`
- L6: `- execute_pricing() agora usa PricingExecutionOrchestrationService no app.db consolidado`
- L16: `from services.pricing_execution_orchestration_service import PricingExecutionOrchestrationService`
- L22: `class PricingExecutionAppService:`
- L26: `pricing_execution_orchestration_service: PricingExecutionOrchestrationService | None = None,`
- L36: `or PricingExecutionOrchestrationService()`
- L46: `def execute_pricing(`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/solicitacao_auditoria_payoff_20260717_192927/arquivos_chave/services/pricing_execution_orchestration_service.py`

Tokens:
- `PricingExecutionOrchestrationService`
- `PricingExecutionService`

Linhas relevantes:
- L8: `from services.pricing_execution_service import PricingExecutionService`
- L12: `class PricingExecutionOrchestrationService:`
- L16: `pricing_execution_service: PricingExecutionService | None = None,`
- L20: `self.pricing_execution_service = pricing_execution_service or PricingExecutionService(`

### `FRENTE_RTD_EXCEL_BTG_ONLINE/solicitacao_auditoria_payoff_20260717_192927/arquivos_chave/services/pricing_execution_service.py`

Tokens:
- `PricingExecutionService`

Linhas relevantes:
- L7: `class PricingExecutionService:`

### `UI/components/decisions_dark_panel.py`

Tokens:
- `structure_decisions`

Linhas relevantes:
- L702: `def _active_structure_decisions(self) -> List[Dict[str, Any]]:`
- L799: `active_decisions = self._active_structure_decisions()`

### `UI/components/details_panel.py`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L309: `"structure_decisions",`
- L310: `"payoff_curve_points",`
- L982: `alteracao_36: filtra por structure_id (INTEGER) em structure_decisions.`
- L1000: `FROM structure_decisions`
- L1022: `alteracao_36: filtra por structure_id (INTEGER) em payoff_curve_points.`
- L1034: `FROM payoff_curve_points`
- L1062: `FROM structure_decisions`
- L1075: `"SELECT COUNT(*) AS n FROM payoff_curve_points WHERE structure_id = ?",`
- L1080: `"source_table": "app.db:structure_decisions / payoff_curve_points",`

### `UI/components/payoff_chart.py`

Tokens:
- `payoff_curve`

Linhas relevantes:
- L275: `self._log_rebuilt_payoff_curve(xs, ys)`
- L276: `self._draw_main_payoff_curve(xs, ys, decision_data, overlay_curve)`
- L317: `def _log_rebuilt_payoff_curve(self, xs: List[float], ys: List[float]) -> None:`
- L325: `def _draw_main_payoff_curve(`

### `UI/components/terminal_vwap_payoff_dark_panel.py`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L1171: `"payoff_curve_points",`
- L1201: `if table == "payoff_curve_points" and ts_col == "timestamp":`
- L1905: `def _ensure_structure_decisions_table(self, conn: sqlite3.Connection) -> None:`
- L1908: `CREATE TABLE IF NOT EXISTS structure_decisions (`
- L1920: `CREATE INDEX IF NOT EXISTS idx_structure_decisions_structure_id`
- L1921: `ON structure_decisions(structure_id)`
- L1934: `self._ensure_structure_decisions_table(conn)`
- L1937: `INSERT INTO structure_decisions (`
- L1955: `def _load_structure_decisions(self, sid: int, limit: int = 5) -> List[Dict[str, Any]]:`
- L1957: `self._ensure_structure_decisions_table(conn)`
- L1967: `FROM structure_decisions`
- L1986: `rows = self._load_structure_decisions(int(sid), limit=5)`
- L2749: `FROM payoff_curve_points`
- L2761: `FROM payoff_curve_points`

### `UI/main_window.py`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L223: `points, info_dict = self.data_model.get_payoff_curve_info(`
- L558: `src = (info_dict or {}).get("source_table", "payoff_curve_points")`

### `UI/models/ui_data.py`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L131: `if self._payoff_table == "payoff_curve_points":`
- L475: `def _payoff_curve_cache_key(`
- L481: `def _get_payoff_curve_from_cache(`
- L492: `def _ensure_payoff_curve_available(self) -> None:`
- L499: `def _ensure_payoff_curve_columns(self, p: Dict[str, str]) -> None:`
- L506: `def _build_payoff_curve_exact_sql(`
- L516: `def _fetch_payoff_curve_exact_rows(`
- L524: `sql_exact = self._build_payoff_curve_exact_sql(p, filter_col)`
- L527: `def _build_payoff_curve_latest_timestamp_sql(`
- L538: `def _fetch_payoff_curve_latest_timestamp(`
- L541: `sql_ts = self._build_payoff_curve_latest_timestamp_sql(p, filter_col)`
- L544: `def _payoff_curve_rows_to_dicts(self, rows) -> List[Dict]:`
- L547: `def _cache_payoff_curve_result(`
- L553: `def _load_payoff_curve_fallback(`
- L561: `row_ts = self._fetch_payoff_curve_latest_timestamp(`
- L565: `return self._cache_payoff_curve_result(cache_key, [])`
- L568: `rows = self._fetch_payoff_curve_exact_rows(`
- L571: `return self._cache_payoff_curve_result(`
- L572: `cache_key, self._payoff_curve_rows_to_dicts(rows)`
- L575: `def _load_payoff_curve_uncached(`
- L583: `self._ensure_payoff_curve_columns(p)`
- L588: `rows = self._fetch_payoff_curve_exact_rows(`
- L592: `return self._cache_payoff_curve_result(`
- L593: `cache_key, self._payoff_curve_rows_to_dicts(rows)`
- L596: `return self._load_payoff_curve_fallback(`
- L600: `def get_payoff_curve(self, structure_id: str, timestamp: str) -> List[Dict]:`
- L606: `cache_key = self._payoff_curve_cache_key(structure_id, timestamp)`
- L607: `cached = self._get_payoff_curve_from_cache(cache_key)`
- L611: `self._ensure_payoff_curve_available()`
- L616: `return self._load_payoff_curve_uncached(`

### `api/pricing_execution_controller.py`

Tokens:
- `PricingExecutionAppService`
- `execute_pricing`

Linhas relevantes:
- L4: `from services.pricing_execution_app_service import PricingExecutionAppService`
- L7: `service = PricingExecutionAppService()`
- L18: `return service.execute_pricing(`

### `db/derived_repo.py`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L4: `Tabelas: payoff_curve_points, structure_decisions`
- L80: `# alteracao_36_A: adicionar structure_id ao DDL de payoff_curve_points`
- L83: `CREATE TABLE IF NOT EXISTS payoff_curve_points (`
- L97: `ON payoff_curve_points (timestamp, aba, point_spot)`
- L103: `ON payoff_curve_points (structure_id, timestamp)`
- L107: `CREATE TABLE IF NOT EXISTS structure_decisions (`
- L128: `ON structure_decisions (timestamp, aba)`
- L133: `ON structure_decisions (aba, timestamp)`
- L138: `ON structure_decisions (timestamp)`
- L144: `"ALTER TABLE payoff_curve_points ADD COLUMN structure_id INTEGER"`
- L183: `# alteracao_36_A: migration incremental payoff_curve_points`
- L184: `existing_cols = _table_columns(conn, "payoff_curve_points")`
- L198: `# Índices de structure_decisions`
- L304: `"DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`
- L360: `"DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L365: `INSERT INTO payoff_curve_points`
- L408: `INSERT OR REPLACE INTO payoff_curve_points`
- L454: `"DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
- L459: `INSERT INTO payoff_curve_points`
- L480: `"DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`
- L506: `FROM payoff_curve_points`
- L516: `FROM payoff_curve_points`
- L527: `FROM payoff_curve_points`
- L568: `f"SELECT * FROM structure_decisions {where} ORDER BY id DESC LIMIT ?",`
- L585: `FROM structure_decisions d`
- L586: `LEFT JOIN payoff_curve_points p`
- L594: `FROM payoff_curve_points p`
- L595: `LEFT JOIN structure_decisions d`
- L617: `f"DELETE FROM payoff_curve_points "`
- L629: `f"DELETE FROM structure_decisions "`

### `db/migrations/add_structure_id_to_payoff_curve_points.py`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L1: `# db/migrations/add_structure_id_to_payoff_curve_points.py`
- L3: `Migration: adiciona structure_id em payoff_curve_points`
- L4: `e payoff_curve_summary, com backfill via structure_decisions.`
- L7: `python db/migrations/add_structure_id_to_payoff_curve_points.py`
- L8: `python db/migrations/add_structure_id_to_payoff_curve_points.py --db dados/app.db`
- L18: `#  payoff_curve_points`
- L20: `"payoff_curve_points: verificar se structure_id já existe",`
- L24: `"payoff_curve_points: ADD COLUMN structure_id",`
- L25: `"ALTER TABLE payoff_curve_points ADD COLUMN structure_id INTEGER",`
- L28: `"payoff_curve_points: BACKFILL structure_id",`
- L30: `UPDATE payoff_curve_points`
- L33: `FROM structure_decisions d`
- L34: `WHERE d.aba       = payoff_curve_points.aba`
- L35: `AND d.timestamp = payoff_curve_points.timestamp`
- L41: `"payoff_curve_points: CREATE INDEX sid+ts",`
- L44: `ON payoff_curve_points (structure_id, timestamp)`
- L47: `#  payoff_curve_summary`
- L49: `"payoff_curve_summary: ADD COLUMN structure_id",`
- L50: `"ALTER TABLE payoff_curve_summary ADD COLUMN structure_id INTEGER",`
- L53: `"payoff_curve_summary: BACKFILL structure_id",`
- L55: `UPDATE payoff_curve_summary`
- L58: `FROM structure_decisions d`
- L59: `WHERE d.aba       = payoff_curve_summary.aba`
- L60: `AND d.timestamp = payoff_curve_summary.timestamp`
- L66: `"payoff_curve_summary: CREATE INDEX sid+ts",`
- L69: `ON payoff_curve_summary (structure_id, timestamp)`
- L106: `for table in ("payoff_curve_points", "payoff_curve_summary"):`

### `db/reader.py`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L42: `def get_payoff_curve(self, ref: StructureRef, timestamp: Optional[str] = None) -> pd.DataFrame:`
- L58: `FROM payoff_curve_points`
- L67: `FROM payoff_curve_points`
- L69: `SELECT MAX(timestamp) FROM payoff_curve_points WHERE {ref.db_column()} = ?`
- L99: `columns = self._get_table_columns(conn, "structure_decisions")`
- L129: `FROM structure_decisions`

### `db/schema.py`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L7: `CREATE TABLE IF NOT EXISTS payoff_curve_points (`
- L19: `ON payoff_curve_points(timestamp, aba);`
- L22: `ON payoff_curve_points(point_spot);`
- L25: `CREATE TABLE IF NOT EXISTS structure_decisions (`
- L46: `ON structure_decisions(timestamp, aba);`
- L49: `ON structure_decisions(decision);`
- L52: `ON structure_decisions(ratio);`

### `db/writer.py`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L72: `INSERT INTO payoff_curve_points`
- L130: `SELECT * FROM structure_decisions`
- L147: `FROM payoff_curve_points`

### `docs/fase7_01_auditoria_rebaseline_20260713.md`

Tokens:
- `derived_payoff`

Linhas relevantes:
- L68: `| services/derived_payoff_persistence.py | POSSIVEL_ADIANTAMENTO_FASE7 | APROVEITAVEL_COM_AJUSTE | Validar persistência derivada e atomicidade payoff/decisão | Útil, mas precisa garantir que não cria decisão fora do contrato validado |`

### `domain/payoff.py`

Tokens:
- `payoff_curve`

Linhas relevantes:
- L51: `def compute_payoff_curve_from_canonical_legs(`
- L157: `result = compute_payoff_curve_from_canonical_legs(`

### `domain/payoff_features.py`

Tokens:
- `payoff_curve`

Linhas relevantes:
- L146: `INSERT INTO payoff_curve_summary (`

### `repositories/ui_data_table_candidates.py`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L12: `"structure_decisions",`
- L20: `"payoff_curve_points",`

### `scripts/15_smoke_pricing_execution_service.py`

Tokens:
- `PricingExecutionService`

Linhas relevantes:
- L2: `from services.pricing_execution_service import PricingExecutionService`
- L7: `service = PricingExecutionService()`

### `scripts/16_smoke_pricing_execution_persistence.py`

Tokens:
- `PricingExecutionService`

Linhas relevantes:
- L4: `from services.pricing_execution_service import PricingExecutionService`
- L10: `execution_service = PricingExecutionService()`

### `scripts/22_smoke_pricing_execution_orchestration_success.py`

Tokens:
- `PricingExecutionOrchestrationService`

Linhas relevantes:
- L2: `PricingExecutionOrchestrationService,`
- L7: `service = PricingExecutionOrchestrationService()`

### `scripts/23_smoke_pricing_execution_orchestration_error.py`

Tokens:
- `PricingExecutionOrchestrationService`
- `PricingExecutionService`

Linhas relevantes:
- L2: `PricingExecutionOrchestrationService,`
- L4: `from services.pricing_execution_service import PricingExecutionService`
- L13: `execution_service = PricingExecutionService(`
- L16: `service = PricingExecutionOrchestrationService(`

### `scripts/26_smoke_pricing_execution_app_service_execute.py`

Tokens:
- `PricingExecutionAppService`
- `execute_pricing`

Linhas relevantes:
- L1: `from services.pricing_execution_app_service import PricingExecutionAppService`
- L5: `service = PricingExecutionAppService()`
- L7: `response = service.execute_pricing(structure_id=2)`

### `scripts/27_smoke_pricing_execution_app_service_list.py`

Tokens:
- `PricingExecutionAppService`

Linhas relevantes:
- L1: `from services.pricing_execution_app_service import PricingExecutionAppService`
- L5: `service = PricingExecutionAppService()`

### `scripts/28_smoke_pricing_execution_app_service_detail.py`

Tokens:
- `PricingExecutionAppService`

Linhas relevantes:
- L1: `from services.pricing_execution_app_service import PricingExecutionAppService`
- L5: `service = PricingExecutionAppService()`

### `scripts/31_smoke_pricing_execution_app_service_latest_summary.py`

Tokens:
- `PricingExecutionAppService`

Linhas relevantes:
- L1: `from services.pricing_execution_app_service import PricingExecutionAppService`
- L5: `service = PricingExecutionAppService()`

### `scripts/34_smoke_pricing_execution_app_service_pagination.py`

Tokens:
- `PricingExecutionAppService`

Linhas relevantes:
- L1: `from services.pricing_execution_app_service import PricingExecutionAppService`
- L5: `service = PricingExecutionAppService()`

### `scripts/38_smoke_pricing_execution_app_service_paginated_filtered.py`

Tokens:
- `PricingExecutionAppService`

Linhas relevantes:
- L1: `from services.pricing_execution_app_service import PricingExecutionAppService`
- L5: `service = PricingExecutionAppService()`

### `scripts/audit/auditoria_pos_patch_32.py`

Tokens:
- `PayoffRefreshCommandService`
- `PricingExecutionAppService`
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `structure_decisions`
- `execute_pricing`
- `derived_payoff`
- `payoff_curve`

Linhas relevantes:
- L11: `"services/derived_payoff_persistence.py",`
- L16: `"scripts/recalculate_payoff_curve_points_once.py",`
- L29: `r"INSERT\s+INTO\s+payoff_curve_points",`
- L30: `r"INSERT\s+INTO\s+structure_decisions",`
- L35: `r"PricingExecutionAppService",`
- L36: `r"execute_pricing\s*\(",`
- L37: `r"payoff_curve_points",`
- L38: `r"structure_decisions",`
- L44: `"services/derived_payoff_persistence.py": [`
- L45: `r"payoff_curve_points",`
- L46: `r"structure_decisions",`
- L47: `r"INSERT\s+INTO\s+payoff_curve_points",`
- L48: `r"INSERT\s+INTO\s+structure_decisions",`
- L53: `r"DerivedPayoffPersistence|payoff_persistence",`
- L58: `r"DerivedPayoffPersistence",`
- L192: `rel_path = "scripts/recalculate_payoff_curve_points_once.py"`
- L202: `r"payoff_curve_points",`
- L203: `r"INSERT\s+INTO\s+payoff_curve_points",`
- L282: `report.append("- Se o backend não gerar `payoff_curve_points`, corrigir contrato de persistência antes da UI.")`
- L284: `report.append("- O script `recalculate_payoff_curve_points_once.py` deve ser manutenção/legado, não fluxo oficial.")`
- L285: `report.append("- Não criar outro serviço de comando se `PayoffRefreshCommandService` já existir.")`

### `scripts/audit/diagnose_payoff_persistence_gap_32_2.py`

Tokens:
- `PayoffRefreshCommandService`
- `PricingExecutionAppService`
- `PricingExecutionOrchestrationService`
- `PricingExecutionService`
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `structure_decisions`
- `execute_pricing`
- `persist_derived`
- `derived_payoff`
- `payoff_curve`

Linhas relevantes:
- L10: `- PayoffRefreshCommandService`
- L11: `- PricingExecutionAppService`
- L12: `- PricingExecutionOrchestrationService`
- L13: `- PricingExecutionService`
- L14: `- DerivedPayoffPersistence`
- L15: `- payoff_curve_points`
- L16: `- structure_decisions`
- L17: `- execute_pricing`
- L41: `"PayoffRefreshCommandService",`
- L42: `"PricingExecutionAppService",`
- L43: `"PricingExecutionOrchestrationService",`
- L44: `"PricingExecutionService",`
- L45: `"DerivedPayoffPersistence",`
- L46: `"payoff_curve_points",`
- L47: `"structure_decisions",`
- L48: `"execute_pricing",`
- L49: `"persist_derived",`
- L50: `"derived_payoff",`
- L51: `"payoff_curve",`
- L223: `"payoff_curve_points",`
- L224: `"structure_decisions",`
- L255: `lines.append("O teste anterior indicou que o pricing executa e snapshot incrementa, mas `payoff_curve_points` e `structure_decisions` não aumentam.")`
- L304: `lines.append("Se o relatório confirmar que `DerivedPayoffPersistence` existe mas não é chamado no fluxo do comando, a correção deve conectar o resultado de `execute_pricing()` ao persistidor oficial.")`

### `scripts/audit/test_backend_payoff_flow_32.py`

Tokens:
- `PricingExecutionAppService`
- `payoff_curve_points`
- `structure_decisions`
- `execute_pricing`
- `payoff_curve`

Linhas relevantes:
- L20: `"payoff_curve_points",`
- L21: `"structure_decisions",`
- L52: `def execute_pricing(structure_id):`
- L55: `from services.pricing_execution_app_service import PricingExecutionAppService`
- L57: `service = PricingExecutionAppService()`
- L60: `lambda: service.execute_pricing(structure_id=structure_id),`
- L61: `lambda: service.execute_pricing(structure_id),`
- L89: `"execute_pricing_result": None,`
- L96: `result = execute_pricing(STRUCTURE_ID)`
- L102: `report["execute_pricing_result"] = repr(result)`
- L124: `payoff_delta = diff.get("payoff_curve_points")`
- L125: `decision_delta = diff.get("structure_decisions")`
- L128: `print("WARNING: pricing executou, mas payoff_curve_points não aumentou.")`
- L131: `print("WARNING: pricing executou, mas structure_decisions não aumentou.")`

### `scripts/debug_pricing_payoff_payload.py`

Tokens:
- `PricingExecutionAppService`
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `execute_pricing`
- `payoff_curve`

Linhas relevantes:
- L27: `row = conn.execute("SELECT COUNT(*) FROM payoff_curve_points").fetchone()`
- L38: `FROM payoff_curve_points`
- L78: `"payoff_curve",`
- L101: `print("=== RESULTADO DO execute_pricing ===")`
- L136: `from services.pricing_execution_app_service import PricingExecutionAppService`
- L138: `service = PricingExecutionAppService()`
- L143: `print(inspect.signature(service.execute_pricing))`
- L153: `print(f"payoff_curve_points={before}")`
- L167: `result = service.execute_pricing(structure_id=structure_id)`
- L169: `result = service.execute_pricing(structure_id)`
- L174: `print(f"ERRO execute_pricing structure_id={structure_id}: {type(exc).__name__}: {exc}", file=sys.stderr)`
- L184: `print(f"payoff_curve_points={after}")`
- L192: `print("CONCLUSÃO: execute_pricing não gravou novos pontos de payoff.")`
- L193: `print("Causa provável: payload entregue ao DerivedPayoffPersistence não contém payoff_points/rtd_payoff_points.")`
- L197: `print("CONCLUSÃO: execute_pricing gravou novos pontos de payoff.")`

### `scripts/diagnose_payoff_curve_points.py`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L62: `if "payoff_curve_points" not in tables:`
- L63: `print("ERRO: tabela payoff_curve_points não existe.")`
- L66: `print("\nSchema payoff_curve_points:")`
- L67: `for r in con.execute("PRAGMA table_info(payoff_curve_points)").fetchall():`
- L85: `FROM payoff_curve_points`
- L101: `FROM payoff_curve_points`
- L114: `FROM payoff_curve_points p`
- L132: `FROM payoff_curve_points`
- L148: `FROM payoff_curve_points`

### `scripts/patch_ui_payoff_refresh_architecture.py`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L81: `"payoff_curve_points",`

### `scripts/payoff_rtd_batch.py`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L12: `RECALC_SCRIPT = ROOT / "scripts" / "recalculate_payoff_curve_points_once.py"`
- L13: `DIAG_SCRIPT = ROOT / "scripts" / "diagnose_payoff_curve_points.py"`
- L34: `("payoff_curve_points", "structure_id"),`
- L85: `description="Recalcula payoff_curve_points em lote usando o script RTD existente."`
- L105: `help="Executa diagnose_payoff_curve_points.py após cada recálculo.",`

### `scripts/purge_derived_snapshots.py`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L12: `"payoff_curve_points",`
- L13: `"structure_decisions",`
- L14: `"payoff_curve_summary",`

### `scripts/recalculate_payoff_curve_points_once.py`

Tokens:
- `PricingExecutionAppService`
- `payoff_curve_points`
- `execute_pricing`
- `payoff_curve`

Linhas relevantes:
- L16: `description="Recalcula payoff das estruturas e grava em payoff_curve_points."`
- L115: `row = conn.execute("SELECT COUNT(*) AS n FROM payoff_curve_points").fetchone()`
- L142: `from services.pricing_execution_app_service import PricingExecutionAppService`
- L164: `service = PricingExecutionAppService()`
- L172: `result = service.execute_pricing(structure_id=sid)`

### `scripts/recalculate_payoff_curve_points_once_checked.py`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L47: `if not table_exists(conn, "payoff_curve_points"):`
- L49: `row = conn.execute("SELECT COUNT(*) AS n FROM payoff_curve_points").fetchone()`
- L54: `if not table_exists(conn, "payoff_curve_points"):`
- L67: `FROM payoff_curve_points`
- L116: `"reason": "recalculate_payoff_curve_points_once returned OK but did not create a new snapshot",`
- L127: `FROM payoff_curve_points`
- L140: `FROM payoff_curve_points`
- L150: `columns = [r["name"] for r in conn.execute("PRAGMA table_info(payoff_curve_points)").fetchall()]`
- L170: `f"INSERT INTO payoff_curve_points ({col_sql}) VALUES ({placeholders})",`
- L196: `str(Path("scripts") / "recalculate_payoff_curve_points_once.py"),`

### `scripts/repair_app_db_consistency.py`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L20: `FROM structure_decisions d`
- L21: `LEFT JOIN payoff_curve_points p`
- L31: `FROM payoff_curve_points p`
- L32: `LEFT JOIN structure_decisions d`
- L122: `FROM payoff_curve_points`
- L133: `FROM structure_decisions`
- L199: `UPDATE structure_decisions`
- L222: `FROM structure_decisions d`
- L223: `LEFT JOIN payoff_curve_points p`
- L244: `f"DELETE FROM structure_decisions WHERE id IN ({placeholders})",`
- L255: `FROM payoff_curve_points p`
- L256: `LEFT JOIN structure_decisions d`
- L275: `DELETE FROM payoff_curve_points`
- L278: `FROM structure_decisions d`
- L279: `WHERE d.aba = payoff_curve_points.aba`
- L280: `AND d.timestamp = payoff_curve_points.timestamp`

### `scripts/run_derived_pipeline.py`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L36: `Placeholder: Gera payoff_curve_summary a partir de payoff_curve_points.`

### `scripts/run_rtd_and_payoff_auto_refresh_loop.py`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L45: `"Comando externo que recalcula payoff e grava payoff_curve_points. "`

### `scripts/validate_payoff_rtd_latest.py`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L33: `FROM payoff_curve_points`
- L42: `FROM payoff_curve_points`
- L62: `FROM payoff_curve_points`
- L73: `FROM payoff_curve_points`
- L148: `description="Valida o último snapshot em payoff_curve_points."`

### `scripts/verify_payoff_refresh_architecture.py`

Tokens:
- `payoff_curve_points`
- `payoff_curve`

Linhas relevantes:
- L46: `'payoff_curve_points',`

### `services/canonical_pricing_facade.py`

Tokens:
- `PricingExecutionService`
- `DerivedPayoffPersistence`
- `execute_pricing`
- `derived_payoff`

Linhas relevantes:
- L4: `alteracao_21 -- Wiring do PayoffPersistencePort (DerivedPayoffPersistence) injetado`
- L14: `C8: execute_pricing() passa underlying_asset para o payload builder.`
- L21: `C5: DerivedPayoffPersistence injetado como payoff_persistence_port`
- L34: `from services.derived_payoff_persistence import DerivedPayoffPersistence`
- L37: `from services.pricing_execution_service import PricingExecutionService`
- L328: `PricingExecutionService.execute_payload()`
- L330: `DerivedPayoffPersistence.persist()`
- L337: `pricing_execution_service: PricingExecutionService | None = None,`
- L343: `self._engine   = pricing_execution_service or PricingExecutionService()`
- L346: `payoff_persistence_port=DerivedPayoffPersistence(),`
- L350: `def execute_pricing(`

### `services/derived_payoff_persistence.py`

Tokens:
- `DerivedPayoffPersistence`
- `derived_payoff`

Linhas relevantes:
- L1: `# services/derived_payoff_persistence.py`
- L15: `class DerivedPayoffPersistence:`
- L36: `logger.debug("derived_payoff_persistence: pricing_payload vazio, skip.")`
- L43: `"derived_payoff_persistence: status=%r não elegível para payoff, skip.",`
- L51: `"derived_payoff_persistence: structure_id ausente; persistência bloqueada."`
- L57: `"derived_payoff_persistence: estrutura inativa/arquivada; "`
- L70: `"derived_payoff_persistence: decisão não gravada porque payoff não foi salvo -- structure_id=%s",`
- L78: `"derived_payoff_persistence: payoff salvo, mas decisão falhou -- structure_id=%s timestamp=%s",`
- L99: `"derived_payoff_persistence: payoff sem pontos para structure_id=%s",`
- L106: `"derived_payoff_persistence: %d pontos gravados -- structure_id=%s",`
- L114: `"derived_payoff_persistence: erro ao gravar payoff -- structure_id=%s",`
- L213: `"derived_payoff_persistence: decisão gravada -- structure_id=%s",`
- L220: `"derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s",`
- L254: `# services/derived_payoff_persistence.py -> raiz do projeto -> dados/app.db`
- L270: `"derived_payoff_persistence: app.db não encontrado para validar structure_id=%s -- db_path=%s",`
- L291: `"derived_payoff_persistence: structure_id=%s não encontrada; persistência bloqueada.",`
- L301: `"derived_payoff_persistence: falha ao validar status da estrutura -- structure_id=%s",`

### `services/derived_service.py`

Tokens:
- `payoff_curve_points`
- `structure_decisions`
- `payoff_curve`

Linhas relevantes:
- L160: `def save_payoff_curve(`
- L242: `sig = inspect.signature(save_payoff_curve)`
- L254: `return save_payoff_curve(`
- L263: `return save_payoff_curve(`
- L362: `def get_all_payoff_curves():`
- L367: `FROM payoff_curve_points`
- L394: `FROM payoff_curve_points`
- L419: `"PRAGMA table_info(structure_decisions)"`
- L437: `FROM structure_decisions`
- L522: `def save_payoff_curve(self, *args, **kwargs):`
- L523: `return save_payoff_curve(*args, **kwargs)`

### `services/payoff_refresh_command_service.py`

Tokens:
- `PayoffRefreshCommandService`
- `PricingExecutionAppService`
- `DerivedPayoffPersistence`
- `payoff_curve_points`
- `structure_decisions`
- `execute_pricing`
- `payoff_curve`

Linhas relevantes:
- L8: `from services.pricing_execution_app_service import PricingExecutionAppService`
- L11: `class PayoffRefreshCommandService:`
- L18: `- Este serviço chama PricingExecutionAppService.`
- L25: `pricing_app_service: PricingExecutionAppService | None = None,`
- L28: `self.pricing_app_service = pricing_app_service or PricingExecutionAppService()`
- L41: `pricing_result = self._execute_pricing(structure_id, reference_date)`
- L91: `"Verifique o wiring de DerivedPayoffPersistence."`
- L126: `def _execute_pricing(`
- L131: `method = self.pricing_app_service.execute_pricing`
- L205: `FROM payoff_curve_points`
- L240: `FROM structure_decisions`
- L249: `FROM structure_decisions`

### `services/pricing_execution_app_service.py`

Tokens:
- `PricingExecutionAppService`
- `PricingExecutionOrchestrationService`
- `execute_pricing`

Linhas relevantes:
- L3: `execute_pricing() delegado para PricingExecutionOrchestrationService.`
- L6: `- execute_pricing() agora usa PricingExecutionOrchestrationService no app.db consolidado`
- L16: `from services.pricing_execution_orchestration_service import PricingExecutionOrchestrationService`
- L22: `class PricingExecutionAppService:`
- L26: `pricing_execution_orchestration_service: PricingExecutionOrchestrationService | None = None,`
- L36: `or PricingExecutionOrchestrationService()`
- L46: `def execute_pricing(`

### `services/pricing_execution_orchestration_service.py`

Tokens:
- `PricingExecutionOrchestrationService`
- `PricingExecutionService`

Linhas relevantes:
- L8: `from services.pricing_execution_service import PricingExecutionService`
- L12: `class PricingExecutionOrchestrationService:`
- L16: `pricing_execution_service: PricingExecutionService | None = None,`
- L20: `self.pricing_execution_service = pricing_execution_service or PricingExecutionService(`

### `services/pricing_execution_service.py`

Tokens:
- `PricingExecutionService`

Linhas relevantes:
- L7: `class PricingExecutionService:`

## 3. Inspeção do banco

- DB: `C:\Users\eucal\projeto\dados\app.db`
- STRUCTURE_ID: `2`

### `structures`

- Existe: `True`
- Total: `9`
- Total da estrutura: `None`
- Colunas: `id, name, underlying_asset, alias_legacy_aba, status, notes, created_at, updated_at`

### `pricing_executions`

- Existe: `True`
- Total: `141`
- Total da estrutura: `32`
- Colunas: `id, created_at, structure_id, underlying_asset, reference_date, execution_status, execution_engine, error_message, duration_ms, number_of_legs, total_quantity, theoretical_value, pricing_payload, result`

### `structure_snapshots`

- Existe: `True`
- Total: `171`
- Total da estrutura: `50`
- Colunas: `id, created_at, structure_id, pricing_execution_id, underlying_asset, reference_date, snapshot_source, structure_json, market_json, metrics_json, payoff_json, decision_json, alerts_json, operation_state_json`

### `system_snapshots`

- Existe: `False`
- Total: `None`
- Total da estrutura: `None`
- Colunas: ``

### `payoff_curve_points`

- Existe: `True`
- Total: `2727`
- Total da estrutura: `1212`
- Colunas: `timestamp, aba, structure_id, spot_ref, point_spot, point_pl, meta_json, created_at`

### `structure_decisions`

- Existe: `True`
- Total: `11`
- Total da estrutura: `4`
- Colunas: `id, structure_id, decision, label, note, created_at, timestamp, aba, level, pl_atual, pl_max, pl_pct_of_max, dte_min, why_json, spot_ref, meta_json, why`

## 4. Próxima correção sugerida

Se o relatório confirmar que `DerivedPayoffPersistence` existe mas não é chamado no fluxo do comando, a correção deve conectar o resultado de `execute_pricing()` ao persistidor oficial.

Se ele é chamado, mas não grava pontos, a correção deve ajustar o parser do payload retornado pelo pricing.

Não corrigir UI ainda.
