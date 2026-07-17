# Relatório 32.3 - Contexto para correção backend payoff

## 1. Git

```text
fix/payoff-centro-verdade-32
A  AUDITORIA_POS_PATCH_32/RELATORIO_32_1_AUDITORIA_POS_PATCH.md
A  AUDITORIA_POS_PATCH_32/RELATORIO_32_1_TESTE_BACKEND_PAYOFF_FLOW.json
A  AUDITORIA_POS_PATCH_32/RELATORIO_32_2_DIAGNOSE_PAYOFF_PERSISTENCE_GAP.json
A  AUDITORIA_POS_PATCH_32/RELATORIO_32_2_DIAGNOSE_PAYOFF_PERSISTENCE_GAP.md
A  scripts/audit/auditoria_pos_patch_32.py
A  scripts/audit/collect_backend_fix_context_32_3.py
A  scripts/audit/diagnose_payoff_persistence_gap_32_2.py
A  scripts/audit/run_pos_patch_32.sh
A  scripts/audit/run_pos_patch_32_2.sh
A  scripts/audit/test_backend_payoff_flow_32.py
?? AUDITORIA_POS_PATCH_32/RELATORIO_32_3_CONTEXTO_CORRECAO_BACKEND.md
?? FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI/
?? FRENTE_RTD_EXCEL_BTG_ONLINE/solicitacao_auditoria_payoff_20260717_192927/
?? scripts/verificar_docs_removidos_hoje.py
```

## 2. Arquivos backend analisados

## Arquivo `services/pricing_execution_app_service.py`

### 2.1 Classes e métodos

```text
class PricingExecutionAppService @ L22
  def __init__(self, canonical_pricing_facade, pricing_execution_orchestration_service, pricing_execution_query_service, db_path) @ L23
  def execute_pricing(self, structure_id, reference_date) @ L46
  def list_execution_summaries(self, structure_id, underlying_asset, status, reference_date, descending) @ L92
  def get_latest_execution_summary(self, structure_id, underlying_asset, status, reference_date) @ L108
  def get_execution(self, execution_id) @ L122
  def paginate_execution_summaries(self, structure_id, underlying_asset, status, reference_date, descending, page, page_size) @ L125
  def _validate_structure_id(self, structure_id) @ L149
  def _validate_reference_date(self, reference_date) @ L153
```

### 2.2 Linhas relevantes

```text
L3: execute_pricing() delegado para PricingExecutionOrchestrationService.
L6:   - execute_pricing() agora usa PricingExecutionOrchestrationService no app.db consolidado
L16: from services.pricing_execution_orchestration_service import PricingExecutionOrchestrationService
L22: class PricingExecutionAppService:
L26:         pricing_execution_orchestration_service: PricingExecutionOrchestrationService | None = None,
L36:             or PricingExecutionOrchestrationService()
L46:     def execute_pricing(
L54:         response = self._orchestration.execute_and_persist(
L80:         persisted = response.get("persisted")
L81:         if isinstance(persisted, dict):
L82:             record = persisted.get("record")
```

### 2.3 Contextos de persistência/payoff

#### Contexto 1

```python
0001: # services/pricing_execution_app_service.py
0002: """
0003: execute_pricing() delegado para PricingExecutionOrchestrationService.
0004: 
0005: Alterações:
0006:   - execute_pricing() agora usa PricingExecutionOrchestrationService no app.db consolidado
0007:   - CanonicalPricingFacade removido do caminho de execução para evitar dependência legada
0008:   - Todos os métodos de query (list, get, paginate, latest) inalterados
0009:   - Validações _validate_structure_id / _validate_reference_date mantidas
0010: """
0011: 
0012: from datetime import datetime
0013: from pathlib import Path
0014: from typing import Any
0015: 
0016: from services.pricing_execution_orchestration_service import PricingExecutionOrchestrationService
0017: from services.pricing_execution_query_service import PricingExecutionQueryService
0018: 
0019: _DEFAULT_DB = Path("dados/app.db")
0020: 
0021: 
0022: class PricingExecutionAppService:
0023:     def __init__(
0024:         self,
0025:         canonical_pricing_facade: Any | None = None,
0026:         pricing_execution_orchestration_service: PricingExecutionOrchestrationService | None = None,
0027:         pricing_execution_query_service: PricingExecutionQueryService | None = None,
0028:         db_path: Path | str = _DEFAULT_DB,
0029:     ):
0030:         # canonical_pricing_facade e db_path mantidos na assinatura por compatibilidade
0031:         # com callers antigos, mas o fluxo atual usa app.db consolidado via orchestration.
```

#### Contexto 2

```python
0018: 
0019: _DEFAULT_DB = Path("dados/app.db")
0020: 
0021: 
0022: class PricingExecutionAppService:
0023:     def __init__(
0024:         self,
0025:         canonical_pricing_facade: Any | None = None,
0026:         pricing_execution_orchestration_service: PricingExecutionOrchestrationService | None = None,
0027:         pricing_execution_query_service: PricingExecutionQueryService | None = None,
0028:         db_path: Path | str = _DEFAULT_DB,
0029:     ):
0030:         # canonical_pricing_facade e db_path mantidos na assinatura por compatibilidade
0031:         # com callers antigos, mas o fluxo atual usa app.db consolidado via orchestration.
0032:         _ = (canonical_pricing_facade, db_path)
0033: 
0034:         self._orchestration = (
0035:             pricing_execution_orchestration_service
0036:             or PricingExecutionOrchestrationService()
0037:         )
0038:         self.pricing_execution_query_service = (
0039:             pricing_execution_query_service or PricingExecutionQueryService()
0040:         )
0041: 
0042:     # ------------------------------------------------------------------
0043:     # Execução
0044:     # ------------------------------------------------------------------
0045: 
0046:     def execute_pricing(
0047:         self,
0048:         structure_id: int,
0049:         reference_date: str | None = None,
0050:     ) -> dict[str, Any]:
0051:         self._validate_structure_id(structure_id)
0052:         self._validate_reference_date(reference_date)
0053: 
0054:         response = self._orchestration.execute_and_persist(
0055:             structure_id=structure_id,
0056:             reference_date=reference_date,
0057:         )
0058: 
0059:         # propaga erros como ValueError para manter contrato com callers existentes
0060:         execution_result = response.get("result")
0061:         inner_result = (
0062:             execution_result.get("result")
0063:             if isinstance(execution_result, dict)
0064:             else None
0065:         )
0066: 
0067:         status = response.get("status")
0068:         error_message = response.get("error_message")
0069: 
0070:         if isinstance(inner_result, dict):
0071:             status = inner_result.get("status", status)
0072:             error_message = inner_result.get("error_message", error_message)
0073:         elif isinstance(execution_result, dict):
0074:             status = execution_result.get("status", status)
```

## Arquivo `services/pricing_execution_orchestration_service.py`

### 2.1 Classes e métodos

```text
class PricingExecutionOrchestrationService @ L12
  def __init__(self, pricing_input_service, pricing_execution_service, pricing_execution_persistence_service) @ L13
  def execute_and_persist(self, structure_id, reference_date) @ L30
```

### 2.2 Linhas relevantes

```text
L5: from services.pricing_execution_persistence_service import (
L6:     PricingExecutionPersistenceService,
L12: class PricingExecutionOrchestrationService:
L17:         pricing_execution_persistence_service: PricingExecutionPersistenceService | None = None,
L23:         self.pricing_execution_persistence_service = (
L24:             pricing_execution_persistence_service
L25:             or PricingExecutionPersistenceService(
L30:     def execute_and_persist(
L44:             persisted = self.pricing_execution_persistence_service.persist_execution(
L54:                 "persisted": persisted,
L70:             persisted = self.pricing_execution_persistence_service.persist_execution(
L80:                 "persisted": persisted,
```

### 2.3 Contextos de persistência/payoff

Sem contextos relevantes.

## Arquivo `services/pricing_execution_persistence_service.py`

### 2.1 Classes e métodos

```text
class PricingExecutionPersistenceService @ L12
  def __init__(self, pricing_executions_repository, payoff_persistence_port, system_snapshots_repository) @ L13
  def persist_execution(self, pricing_payload, result, duration_ms, error_message) @ L25
  def _create_system_snapshot_if_applicable(self) @ L91
  def _build_structure_json(pricing_payload) @ L141
  def _build_market_json(pricing_payload) @ L151
  def _extract_result_field(inner, field) @ L159
```

### 2.2 Linhas relevantes

```text
L1: # services/pricing_execution_persistence_service.py
L7: from services.payoff_persistence_port import PayoffPersistencePort
L12: class PricingExecutionPersistenceService:
L16:         payoff_persistence_port: PayoffPersistencePort | None = None,
L22:         self._payoff_port = payoff_persistence_port
L25:     def persist_execution(
L39:         persisted_error_message = error_message or (
L46:         record = self.pricing_executions_repository.save_execution(
L51:             error_message=persisted_error_message,
L67:         #  alteracao_21 -- persistência derivada (payoff + decisão)           #
L72:                 self._payoff_port.persist(
L78:                     "payoff_persistence_port.persist() falhou -- execução id=%s não afetada",
L125:                 decision_json=self._extract_result_field(inner, "decision"),
```

### 2.3 Contextos de persistência/payoff

#### Contexto 1

```python
0001: # services/pricing_execution_persistence_service.py
0002: import logging
0003: from typing import Any
0004: 
0005: from repositories.pricing_executions_repository import PricingExecutionsRepository
0006: from repositories.system_snapshots_repository import SystemSnapshotsRepository
0007: from services.payoff_persistence_port import PayoffPersistencePort
0008: 
0009: logger = logging.getLogger(__name__)
0010: 
0011: 
0012: class PricingExecutionPersistenceService:
0013:     def __init__(
0014:         self,
0015:         pricing_executions_repository: PricingExecutionsRepository | None = None,
0016:         payoff_persistence_port: PayoffPersistencePort | None = None,
0017:         system_snapshots_repository: SystemSnapshotsRepository | None = None,
0018:     ):
0019:         self.pricing_executions_repository = (
0020:             pricing_executions_repository or PricingExecutionsRepository()
0021:         )
0022:         self._payoff_port = payoff_persistence_port
0023:         self._system_snapshots_repository = system_snapshots_repository
0024: 
0025:     def persist_execution(
0026:         self,
0027:         pricing_payload: dict[str, Any] | None,
0028:         result: dict[str, Any],
0029:         duration_ms: int | None = None,
0030:         error_message: str | None = None,
0031:     ) -> dict[str, Any]:
0032:         # result pode chegar como wrapper {"result": {...}} ou já desempacotado
0033:         inner = result.get("result", result) if isinstance(result, dict) else result
0034:         metrics = inner.get("metrics", {}) if isinstance(inner, dict) else {}
0035:         valuation = inner.get("valuation", {}) if isinstance(inner, dict) else {}
```

#### Contexto 2

```python
0050:             execution_engine=execution_engine,
0051:             error_message=persisted_error_message,
0052:             duration_ms=duration_ms,
0053:             number_of_legs=number_of_legs,
0054:             total_quantity=total_quantity,
0055:             theoretical_value=theoretical_value,
0056:         )
0057: 
0058:         snapshot_id = self._create_system_snapshot_if_applicable(
0059:             record=record,
0060:             pricing_payload=pricing_payload,
0061:             result=result,
0062:             inner=inner,
0063:             execution_status=execution_status,
0064:         )
0065: 
0066:         # ------------------------------------------------------------------ #
0067:         #  alteracao_21 -- persistência derivada (payoff + decisão)           #
0068:         #  Fire-and-forget: falha aqui nunca derruba a execução principal.    #
0069:         # ------------------------------------------------------------------ #
0070:         if self._payoff_port is not None:
0071:             try:
0072:                 self._payoff_port.persist(
0073:                     pricing_payload=pricing_payload,
0074:                     result=result,
0075:                 )
0076:             except Exception:
0077:                 logger.exception(
0078:                     "payoff_persistence_port.persist() falhou -- execução id=%s não afetada",
0079:                     record.get("id"),
0080:                 )
0081: 
0082:         response = {
0083:             "record": record,
0084:         }
0085: 
0086:         if snapshot_id is not None:
0087:             response["snapshot_id"] = snapshot_id
0088: 
0089:         return response
0090: 
0091:     def _create_system_snapshot_if_applicable(
0092:         self,
0093:         *,
0094:         record: dict[str, Any],
0095:         pricing_payload: dict[str, Any] | None,
0096:         result: dict[str, Any],
0097:         inner: Any,
0098:         execution_status: str | None,
0099:     ) -> int | None:
0100:         if self._system_snapshots_repository is None:
0101:             return None
0102: 
0103:         if not pricing_payload:
0104:             return None
0105: 
0106:         if execution_status != "ok":
```

## Arquivo `services/derived_payoff_persistence.py`

### 2.1 Classes e métodos

```text
class DerivedPayoffPersistence @ L15
  def persist(self, pricing_payload, result) @ L30
  def _persist_payoff(self, pricing_payload, result, snapshot_ts) @ L87
  def _persist_decision(self, pricing_payload, result, snapshot_ts) @ L123
  def _extract_structure_id(pricing_payload) @ L230
  def _default_db_path() @ L249
  def _is_active_structure(cls, structure_id) @ L258
  def _build_canonical_input(pricing_payload, result) @ L307
def normalize_leg_for_canonical(leg) @ L325
def normalize_legs(legs) @ L350
```

### 2.2 Linhas relevantes

```text
L1: # services/derived_payoff_persistence.py
L10: from services.derived_service import save_payoff_from_canonical_payload, save_decision_from_canonical_payload
L15: class DerivedPayoffPersistence:
L17:     Implementação concreta de PayoffPersistencePort.
L22:       3. Persistir pontos no app.db via derived_service
L23:       4. Persistir decisão básica derivada do resultado do engine
L27:     #  PayoffPersistencePort.persist()                                 #
L30:     def persist(
L36:             logger.debug("derived_payoff_persistence: pricing_payload vazio, skip.")
L43:                 "derived_payoff_persistence: status=%r não elegível para payoff, skip.",
L51:                 "derived_payoff_persistence: structure_id ausente; persistência bloqueada."
L57:                 "derived_payoff_persistence: estrutura inativa/arquivada; "
L67:         payoff_saved = self._persist_payoff(pricing_payload, result, snapshot_ts)
L68:         if not payoff_saved:
L70:                 "derived_payoff_persistence: decisão não gravada porque payoff não foi salvo -- structure_id=%s",
L75:         decision_saved = self._persist_decision(pricing_payload, result, snapshot_ts)
L76:         if not decision_saved:
L78:                 "derived_payoff_persistence: payoff salvo, mas decisão falhou -- structure_id=%s timestamp=%s",
L87:     def _persist_payoff(
L99:                     "derived_payoff_persistence: payoff sem pontos para structure_id=%s",
L104:             save_payoff_from_canonical_payload(payoff_result, timestamp=snapshot_ts)
L106:                 "derived_payoff_persistence: %d pontos gravados -- structure_id=%s",
L114:                 "derived_payoff_persistence: erro ao gravar payoff -- structure_id=%s",
L123:     def _persist_decision(
L180:             decision_dict = {
L181:                 "decision":      "HOLD",
L205:             save_decision_from_canonical_payload(
L206:                 decision=decision_dict,
L213:                 "derived_payoff_persistence: decisão gravada -- structure_id=%s",
L220:                 "derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s",
L254:         # services/derived_payoff_persistence.py -> raiz do projeto -> dados/app.db
L260:         Barreira de segurança na camada de persistência.
L270:                     "derived_payoff_persistence: app.db não encontrado para validar structure_id=%s -- db_path=%s",
L291:                     "derived_payoff_persistence: structure_id=%s não encontrada; persistência bloqueada.",
L301:                 "derived_payoff_persistence: falha ao validar status da estrutura -- structure_id=%s",
L386:                 "source": "pricing_execution_persistence",
```

### 2.3 Contextos de persistência/payoff

#### Contexto 1

```python
0001: # services/derived_payoff_persistence.py
0002: import logging
0003: import os
0004: import sqlite3
0005: from datetime import datetime, timezone
0006: from pathlib import Path
0007: from typing import Any
0008: 
0009: from domain.payoff import compute_payoff_from_canonical_input
0010: from services.derived_service import save_payoff_from_canonical_payload, save_decision_from_canonical_payload
0011: 
0012: logger = logging.getLogger(__name__)
0013: 
0014: 
0015: class DerivedPayoffPersistence:
0016:     """
0017:     Implementação concreta de PayoffPersistencePort.
0018: 
0019:     Responsabilidades:
0020:       1. Montar o canonical_input a partir do pricing_payload
0021:       2. Calcular a curva de payoff via domain/payoff.py
0022:       3. Persistir pontos no app.db via derived_service
0023:       4. Persistir decisão básica derivada do resultado do engine
0024:     """
0025: 
0026:     # -------------------------------------------------------------- #
0027:     #  PayoffPersistencePort.persist()                                 #
0028:     # -------------------------------------------------------------- #
0029: 
0030:     def persist(
0031:         self,
0032:         pricing_payload: dict[str, Any] | None,
0033:         result: dict[str, Any],
0034:     ) -> None:
0035:         if not pricing_payload:
0036:             logger.debug("derived_payoff_persistence: pricing_payload vazio, skip.")
0037:             return
0038: 
0039:         inner = result.get("result", result) if isinstance(result, dict) else{}
0040:         status = inner.get("status", "")
0041:         if status not in ("success", "ok", "completed"):
0042:             logger.debug(
0043:                 "derived_payoff_persistence: status=%r não elegível para payoff, skip.",
```

## Arquivo `services/derived_service.py`

### 2.1 Classes e métodos

```text
def _load_aba_cache() @ L34
def _resolve_structure_id(aba) @ L51
def invalidate_aba_cache() @ L59
def _now_iso() @ L68
def _safe_str(value) @ L72
def _unwrap_ref(ref) @ L79
def _resolve_storage_key(aba, structure_id, structure_name, underlying_asset) @ L89
def _merge_meta(meta, structure_id, structure_name, underlying_asset, reference_date, input_meta, storage_key) @ L127
def init_db() @ L151
def save_payoff_curve(ref, points, spot_ref, meta, timestamp, structure_id) @ L160
def save_payoff_from_canonical_payload(payoff, aba, timestamp) @ L210
def save_decision(ref, decision, timestamp) @ L272
def save_decision_from_canonical_payload(decision, structure_id, structure_name, underlying_asset, aba, timestamp) @ L304
def cleanup_derived(days_to_keep) @ L350
def get_all_payoff_curves() @ L362
def get_payoff_by_structure_id(structure_id) @ L382
def get_recent_decisions() @ L411
def format_report(entries) @ L486
def snapshot_aba(ref) @ L497
class DerivedService @ L509
  def get_payoff_by_structure_id(self, structure_id) @ L518
  def save_payoff_curve(self) @ L522
  def save_decision(self) @ L525
  def cleanup_derived(self, days_to_keep) @ L528
```

### 2.2 Linhas relevantes

```text
L4: alteracao_30/alteracao_57c -- Servico de persistencia de dados consolidados (payoff + decisoes).
L17:     cleanup_old_decisions,
L20:     insert_payoff_points,
L21:     insert_structure_decision,
L160: def save_payoff_curve(
L199:         return insert_payoff_points(
L210: def save_payoff_from_canonical_payload(
L242:         sig = inspect.signature(save_payoff_curve)
L254:         return save_payoff_curve(
L263:     return save_payoff_curve(
L272: def save_decision(
L274:     decision: Dict[str, Any],
L284:     enriched_decision = {
L285:         **decision,
L288:             **(decision.get("meta") or {}),
L296:         return insert_structure_decision(
L300:             decision_dict=enriched_decision,
L304: def save_decision_from_canonical_payload(
L305:     decision: Dict[str, Any],
L327:     enriched_decision = {
L328:         **decision,
L331:             **(decision.get("meta") or {}),
L339:     return save_decision(
L341:         decision=enriched_decision,
L354:         deleted_dec    = cleanup_old_decisions(conn, days_to_keep=days_to_keep)
L355:         return {"payoff_deleted": deleted_payoff, "decisions_deleted": deleted_dec}
L362: def get_all_payoff_curves():
L367:             FROM payoff_curve_points
L394:               FROM payoff_curve_points
L411: def get_recent_decisions():
L419:                 "PRAGMA table_info(structure_decisions)"
L424:             "timestamp", "aba", "decision", "level",
L437:             FROM structure_decisions
L442:         decisions = []
L477:             decisions.append(item)
L479:         return decisions
L522:     def save_payoff_curve(self, *args, **kwargs):
L523:         return save_payoff_curve(*args, **kwargs)
L525:     def save_decision(self, *args, **kwargs):
L526:         return save_decision(*args, **kwargs)
```

### 2.3 Contextos de persistência/payoff

#### Contexto 1

```python
0001: from __future__ import annotations
0002: # services/derived_service.py
0003: """
0004: alteracao_30/alteracao_57c -- Servico de persistencia de dados consolidados (payoff + decisoes).
0005: alteracao_62           -- AbaResolverMixin extraído para repositories/_aba_resolver_mixin.py.
0006: alteracao_65           -- get_payoff_by_aba() removida da interface pública (standalone).
0007: """
0008: 
0009: import inspect
0010: import json
0011: import sqlite3
0012: from datetime import datetime, timezone
0013: from typing import Any, Dict, List, Optional, Tuple, Union
0014: 
0015: from db.config import connect_app
0016: from db.derived_repo import (
0017:     cleanup_old_decisions,
0018:     cleanup_old_payoff_data,
0019:     ensure_derived_tables,
0020:     insert_payoff_points,
0021:     insert_structure_decision,
0022: )
0023: from domain.refs.structure_ref import StructureRef
0024: 
0025: 
0026: # ------------------------------------------------------------------
0027: # Cache modulo-level: aba -> structure_id
0028: # ------------------------------------------------------------------
0029: 
0030: _ABA_TO_STRUCTURE_ID: Dict[str, int] = {}
0031: _ABA_CACHE_LOADED: bool = False
0032: 
0033: 
0034: def _load_aba_cache() -> None:
0035:     global _ABA_TO_STRUCTURE_ID, _ABA_CACHE_LOADED
0036:     try:
0037:         with connect_app() as conn:
0038:             cur = conn.execute("""
0039:                 SELECT id, alias_legacy_aba
0040:                 FROM structures
0041:                 WHERE alias_legacy_aba IS NOT NULL
0042:                   AND alias_legacy_aba != ''
0043:             """)
0044:             _ABA_TO_STRUCTURE_ID = {row[1]: row[0] for row in cur.fetchall()}
0045:     except Exception:
0046:         _ABA_TO_STRUCTURE_ID = {}
0047:     finally:
0048:         _ABA_CACHE_LOADED = True
```

#### Contexto 2

```python
0171:     """
0172:     ts           = timestamp or _now_iso()
0173:     storage_key  = _unwrap_ref(ref) or "unknown"
0174:     resolved_sid = (
0175:         int(structure_id)
0176:         if structure_id is not None
0177:         else _resolve_structure_id(storage_key)
0178:     )
0179: 
0180:     norm_points: List[Tuple[float, float]] = []
0181:     for p in points or []:
0182:         if isinstance(p, (tuple, list)) and len(p) == 2:
0183:             norm_points.append((float(p[0]), float(p[1])))
0184:         elif isinstance(p, dict):
0185:             x = p.get("point_spot") or p.get("s_t")
0186:             y = p.get("point_pl")   or p.get("pl_venc")
0187:             if x is None or y is None:
0188:                 continue
0189:             norm_points.append((float(x), float(y)))
0190: 
0191:     effective_meta = {
0192:         **(meta or {}),
0193:         "storage_key":  storage_key,
0194:         "structure_id": resolved_sid,
0195:     }
0196: 
0197:     with connect_app() as conn:
0198:         ensure_derived_tables(conn)
0199:         return insert_payoff_points(
0200:             conn=conn,
0201:             timestamp=ts,
0202:             aba=storage_key,
0203:             points=norm_points,
0204:             spot_ref=spot_ref,
0205:             meta=effective_meta,
0206:             structure_id=resolved_sid,
0207:         )
0208: 
0209: 
0210: def save_payoff_from_canonical_payload(
0211:     payoff: Dict[str, Any],
0212:     aba: Optional[str] = None,
0213:     timestamp: Optional[str] = None,
0214: ) -> int:
0215:     ts = timestamp or _now_iso()
0216: 
0217:     storage_key = _resolve_storage_key(
0218:         aba=aba,
0219:         structure_id=payoff.get("structure_id"),
0220:         structure_name=payoff.get("structure_name"),
0221:         underlying_asset=payoff.get("underlying_asset"),
0222:     )
0223: 
0224:     sid_from_payload = payoff.get("structure_id")
0225:     resolved_sid = (
0226:         int(sid_from_payload)
0227:         if sid_from_payload is not None
```

#### Contexto 3

```python
0339:     return save_decision(
0340:         ref=storage_key,
0341:         decision=enriched_decision,
0342:         timestamp=ts,
0343:     )
0344: 
0345: 
0346: # ------------------------------------------------------------------
0347: # Cleanup
0348: # ------------------------------------------------------------------
0349: 
0350: def cleanup_derived(days_to_keep: int = 30) -> Dict[str, int]:
0351:     with connect_app() as conn:
0352:         ensure_derived_tables(conn)
0353:         deleted_payoff = cleanup_old_payoff_data(conn, days_to_keep=days_to_keep)
0354:         deleted_dec    = cleanup_old_decisions(conn, days_to_keep=days_to_keep)
0355:         return {"payoff_deleted": deleted_payoff, "decisions_deleted": deleted_dec}
0356: 
0357: 
0358: # ------------------------------------------------------------------
0359: # Leituras
0360: # ------------------------------------------------------------------
0361: 
0362: def get_all_payoff_curves():
0363:     with connect_app() as conn:
0364:         cursor = conn.cursor()
0365:         cursor.execute("""
0366:             SELECT timestamp, aba, point_spot, point_pl, meta_json
0367:             FROM payoff_curve_points
0368:             ORDER BY timestamp DESC, point_spot
0369:         """)
0370:         return [
0371:             {
0372:                 "timestamp":  row[0],
0373:                 "aba":        row[1],
0374:                 "point_spot": row[2],
0375:                 "point_pl":   row[3],
0376:                 "meta_json":  json.loads(row[4]) if row[4] else None,
0377:             }
0378:             for row in cursor.fetchall()
0379:         ]
0380: 
0381: 
0382: def get_payoff_by_structure_id(structure_id: int):
0383:     """
0384:     alteracao_56/alteracao_65: único ponto de entrada canônico para leitura de payoff.
0385:     get_payoff_by_aba() removida da interface pública (alteracao_65).
0386:     """
0387:     ref = StructureRef.from_id(structure_id)
0388:     col, val = ref.db_pair()
0389:     with connect_app() as conn:
0390:         cursor = conn.cursor()
0391:         cursor.execute(
0392:             f"""
0393:             SELECT timestamp, point_spot, point_pl, meta_json
0394:               FROM payoff_curve_points
0395:              WHERE {col} = ?
```

#### Contexto 4

```python
0391:         cursor.execute(
0392:             f"""
0393:             SELECT timestamp, point_spot, point_pl, meta_json
0394:               FROM payoff_curve_points
0395:              WHERE {col} = ?
0396:              ORDER BY point_spot
0397:             """,
0398:             (val,),
0399:         )
0400:         return [
0401:             {
0402:                 "timestamp":  row[0],
0403:                 "point_spot": row[1],
0404:                 "point_pl":   row[2],
0405:                 "meta_json":  json.loads(row[3]) if row[3] else None,
0406:             }
0407:             for row in cursor.fetchall()
0408:         ]
0409: 
0410: 
0411: def get_recent_decisions():
0412:     with connect_app() as conn:
0413:         conn.row_factory = sqlite3.Row
0414:         cursor = conn.cursor()
0415: 
0416:         cols = [
0417:             row["name"]
0418:             for row in cursor.execute(
0419:                 "PRAGMA table_info(structure_decisions)"
0420:             ).fetchall()
0421:         ]
0422: 
0423:         select_cols = [
0424:             "timestamp", "aba", "decision", "level",
0425:             "pl_atual", "pl_max", "pl_pct_of_max", "dte_min",
0426:             "spot_ref", "meta_json", "created_at",
0427:         ]
0428:         if "structure_id" in cols:
0429:             select_cols.append("structure_id")
0430:         if "why" in cols:
0431:             select_cols.append("why")
0432:         if "why_json" in cols:
0433:             select_cols.append("why_json")
0434: 
0435:         cursor.execute(f"""
0436:             SELECT {", ".join(select_cols)}
0437:             FROM structure_decisions
0438:             ORDER BY timestamp DESC
0439:             LIMIT 50
0440:         """)
0441: 
0442:         decisions = []
0443:         for row in cursor.fetchall():
0444:             item = dict(row)
0445:             why_val      = item.get("why")
0446:             why_json_val = item.get("why_json")
0447: 
```

## Arquivo `services/canonical_pricing_facade.py`

### 2.1 Classes e métodos

```text
def _get_structure_info(structure_id, db_path) @ L44
def _to_float(value, default) @ L75
def _normalize_expiration_date(value) @ L109
def _pick(data) @ L131
def _quote_ident(name) @ L139
def _lookup_spot_price(db_path, underlying_asset) @ L143
def _snapshot_result_to_payload(selection_result, structure_id, underlying_asset, reference_date, db_path) @ L234
class CanonicalPricingFacade @ L320
  def __init__(self, db_path, pricing_execution_service, persistence_service) @ L334
  def execute_pricing(self, structure_id, reference_date) @ L350
```

### 2.2 Linhas relevantes

```text
L4: alteracao_21 -- Wiring do PayoffPersistencePort (DerivedPayoffPersistence) injetado
L5:            no PricingExecutionPersistenceService.
L14:   C8: execute_pricing() passa underlying_asset para o payload builder.
L20:   C4: engine_result extraído do wrapper antes de passar ao persister
L21:   C5: DerivedPayoffPersistence injetado como payoff_persistence_port
L34: from services.derived_payoff_persistence import DerivedPayoffPersistence
L36: from services.pricing_execution_persistence_service import PricingExecutionPersistenceService
L300:             "Não persistir execução OK com spot_price <= 0."
L329:                                              PricingExecutionPersistenceService.persist()
L330:                                                      DerivedPayoffPersistence.persist()
L338:         persistence_service: PricingExecutionPersistenceService | None = None,
L345:         self._persister = persistence_service or PricingExecutionPersistenceService(
L346:             payoff_persistence_port=DerivedPayoffPersistence(),
L350:     def execute_pricing(
L385:             #  5. Persiste no app.db via port
L386:             persisted = self._persister.persist_execution(
L398:                 "persisted":       persisted,
L408:                 self._persister.persist_execution(
L422:                 "persisted":       None,
```

### 2.3 Contextos de persistência/payoff

#### Contexto 1

```python
0001: # services/canonical_pricing_facade.py
0002: """
0003: alteracao_17 -- Fachada canônica corrigida.
0004: alteracao_21 -- Wiring do PayoffPersistencePort (DerivedPayoffPersistence) injetado
0005:            no PricingExecutionPersistenceService.
0006: alteracao_41 -- Corrige underlying_asset no pricing_payload.
0007: 
0008: Correções alteracao_41:
0009:   C6: _get_alias_legacy_aba() substituído por _get_structure_info() --
0010:       busca alias_legacy_aba E underlying_asset em uma única query.
0011:   C7: _snapshot_result_to_payload() recebe underlying_asset explícito --
0012:       elimina uso de selection_result.aba como underlying_asset
0013:       (aba legada  ativo subjacente real).
0014:   C8: execute_pricing() passa underlying_asset para o payload builder.
0015: 
0016: Correções anteriores mantidas:
0017:   C1: sel.select(aba=...) -- parâmetro correto
0018:   C2: alias_legacy_aba buscado via query antes de chamar o selector
0019:   C3: orquestração direta repo  selector  execute_payload()
0020:   C4: engine_result extraído do wrapper antes de passar ao persister
0021:   C5: DerivedPayoffPersistence injetado como payoff_persistence_port
0022: """
0023: from __future__ import annotations
0024: 
0025: 
0026: import sqlite3
0027: import time
0028: from datetime import datetime
0029: from pathlib import Path
0030: from typing import Any
0031: 
0032: from repositories.market_snapshot_repository import MarketSnapshotRepository
```

#### Contexto 2

```python
0006: alteracao_41 -- Corrige underlying_asset no pricing_payload.
0007: 
0008: Correções alteracao_41:
0009:   C6: _get_alias_legacy_aba() substituído por _get_structure_info() --
0010:       busca alias_legacy_aba E underlying_asset em uma única query.
0011:   C7: _snapshot_result_to_payload() recebe underlying_asset explícito --
0012:       elimina uso de selection_result.aba como underlying_asset
0013:       (aba legada  ativo subjacente real).
0014:   C8: execute_pricing() passa underlying_asset para o payload builder.
0015: 
0016: Correções anteriores mantidas:
0017:   C1: sel.select(aba=...) -- parâmetro correto
0018:   C2: alias_legacy_aba buscado via query antes de chamar o selector
0019:   C3: orquestração direta repo  selector  execute_payload()
0020:   C4: engine_result extraído do wrapper antes de passar ao persister
0021:   C5: DerivedPayoffPersistence injetado como payoff_persistence_port
0022: """
0023: from __future__ import annotations
0024: 
0025: 
0026: import sqlite3
0027: import time
0028: from datetime import datetime
0029: from pathlib import Path
0030: from typing import Any
0031: 
0032: from repositories.market_snapshot_repository import MarketSnapshotRepository
0033: from repositories.system_snapshots_repository import SystemSnapshotsRepository
0034: from services.derived_payoff_persistence import DerivedPayoffPersistence
0035: from services.market_snapshot_selector import MarketSnapshotSelector
0036: from services.pricing_execution_persistence_service import PricingExecutionPersistenceService
0037: from services.pricing_execution_service import PricingExecutionService
0038: 
0039: _DEFAULT_DB = Path("dados/app.db")
0040: 
0041: 
0042: #  C6: substitui _get_alias_legacy_aba -- busca aba + underlying em 1 query 
0043: 
0044: def _get_structure_info(structure_id: int, db_path: Path) -> tuple[str, str]:
0045:     """
0046:     Retorna (alias_legacy_aba, underlying_asset) para a estrutura.
0047: 
0048:     Raises ValueError se:
0049:       - estrutura não existir
0050:       - alias_legacy_aba for nulo (sem aba legada mapeada)
0051:     """
0052:     with sqlite3.connect(str(db_path)) as conn:
0053:         conn.row_factory = sqlite3.Row
0054:         row = conn.execute(
0055:             "SELECT alias_legacy_aba, underlying_asset FROM structures WHERE id = ?",
0056:             (structure_id,),
0057:         ).fetchone()
0058: 
0059:     if row is None:
0060:         raise ValueError(f"structure not found: {structure_id}")
0061: 
0062:     aba = row["alias_legacy_aba"]
```

#### Contexto 3

```python
0302: 
0303:     return {
0304:         "structure_id":     structure_id,
0305:         "underlying_asset": underlying_asset,
0306:         "reference_date":   reference_date,
0307:         "spot_price":       spot_price,
0308:         "interest_rate":    0.0,
0309:         "volatility":       0.0,
0310:         "legs":             legs_data,
0311:         "meta": {
0312:             "snapshot_source":  str(selection_result.source),
0313:             "snapshot_aba":     selection_result.aba,
0314:             "manual_overrides": getattr(selection_result, "manual_overrides", None) or [],
0315:             "legs_count":       len(legs_data),
0316:         },
0317:     }
0318: 
0319: 
0320: class CanonicalPricingFacade:
0321:     """
0322:     Orquestra o pipeline canônico ponta a ponta:
0323: 
0324:         structure_id
0325:              alias_legacy_aba + underlying_asset  (query em structures)
0326:                      MarketSnapshotSelector.select(aba=...)
0327:                              pricing_payload  (underlying_asset = ativo real)
0328:                                      PricingExecutionService.execute_payload()
0329:                                              PricingExecutionPersistenceService.persist()
0330:                                                      DerivedPayoffPersistence.persist()
0331:                                                              app.db
0332:     """
0333: 
0334:     def __init__(
0335:         self,
0336:         db_path: Path | str = _DEFAULT_DB,
0337:         pricing_execution_service: PricingExecutionService | None = None,
0338:         persistence_service: PricingExecutionPersistenceService | None = None,
0339:     ) -> None:
0340:         self._db_path  = Path(db_path)
0341:         self._repo     = MarketSnapshotRepository(db_path=self._db_path)
0342:         self._selector = MarketSnapshotSelector(repository=self._repo)
0343:         self._engine   = pricing_execution_service or PricingExecutionService()
0344: 
0345:         self._persister = persistence_service or PricingExecutionPersistenceService(
0346:             payoff_persistence_port=DerivedPayoffPersistence(),
0347:             system_snapshots_repository=SystemSnapshotsRepository(db_path=self._db_path),
0348:         )
0349: 
0350:     def execute_pricing(
0351:         self,
0352:         structure_id: int,
0353:         reference_date: str | None = None,
0354:     ) -> dict[str, Any]:
0355:         started_at = time.perf_counter()
0356: 
0357:         try:
0358:             #  1. Resolve aba + underlying_asset 
```

## Arquivo `services/payoff_refresh_command_service.py`

### 2.1 Classes e métodos

```text
class PayoffRefreshCommandService @ L11
  def __init__(self, pricing_app_service, db_path) @ L23
  def refresh_payoff_for_structure(self, structure_id, reference_date) @ L31
  def _execute_pricing(self, structure_id, reference_date) @ L126
  def _validate_structure_id(self, structure_id) @ L141
  def _ensure_active_structure(self, structure_id) @ L154
  def _connect(self) @ L190
  def _latest_payoff_timestamp(self, structure_id) @ L193
  def _latest_payoff_summary(self, structure_id) @ L196
  def _decision_exists(self, structure_id, timestamp) @ L232
  def _latest_snapshot_id(self, structure_id) @ L266
  def _extract_status(self, result) @ L298
  def _extract_pricing_execution_id(self, result) @ L306
```

### 2.2 Linhas relevantes

```text
L8: from services.pricing_execution_app_service import PricingExecutionAppService
L18:     - Este serviço chama PricingExecutionAppService.
L19:     - A persistência derivada deve acontecer no wiring oficial.
L20:     - Após a execução, este serviço valida se houve payoff persistido.
L25:         pricing_app_service: PricingExecutionAppService | None = None,
L28:         self.pricing_app_service = pricing_app_service or PricingExecutionAppService()
L41:             pricing_result = self._execute_pricing(structure_id, reference_date)
L49:                 "payoff_points_count": 0,
L51:                 "decision_found": False,
L65:                 "payoff_points_count": 0,
L67:                 "decision_found": False,
L74:         points_count = int(payoff_summary.get("payoff_points_count") or 0)
L76:         decision_found = self._decision_exists(structure_id, after_ts)
L86:                 "payoff_points_count": 0,
L88:                 "decision_found": decision_found,
L90:                     "Pricing executado, mas nenhum payoff persistido foi encontrado. "
L91:                     "Verifique o wiring de DerivedPayoffPersistence."
L103:                 "payoff_points_count": points_count,
L105:                 "decision_found": decision_found,
L108:                     "Pode haver persistência antiga, deduplicação ou falha silenciosa."
L119:             "payoff_points_count": points_count,
L121:             "decision_found": decision_found,
L126:     def _execute_pricing(
L131:         method = self.pricing_app_service.execute_pricing
L160:           - archived/inactive não deve consumir processamento nem persistir derivados.
L200:                 "payoff_points_count": 0,
L205:             FROM payoff_curve_points
L218:                 "payoff_points_count": 0,
L224:                 "payoff_points_count": 0,
L229:             "payoff_points_count": row[1],
L232:     def _decision_exists(self, structure_id: int, timestamp: str | None) -> bool:
L240:                 FROM structure_decisions
L249:                 FROM structure_decisions
```

### 2.3 Contextos de persistência/payoff

#### Contexto 1

```python
0013:     Serviço oficial para refresh operacional de payoff.
0014: 
0015:     Regra arquitetural:
0016:     - UI não calcula payoff.
0017:     - UI chama este serviço.
0018:     - Este serviço chama PricingExecutionAppService.
0019:     - A persistência derivada deve acontecer no wiring oficial.
0020:     - Após a execução, este serviço valida se houve payoff persistido.
0021:     """
0022: 
0023:     def __init__(
0024:         self,
0025:         pricing_app_service: PricingExecutionAppService | None = None,
0026:         db_path: str | Path | None = None,
0027:     ) -> None:
0028:         self.pricing_app_service = pricing_app_service or PricingExecutionAppService()
0029:         self.db_path = Path(db_path or "dados/app.db")
0030: 
0031:     def refresh_payoff_for_structure(
0032:         self,
0033:         structure_id: int,
0034:         reference_date: str | None = None,
0035:     ) -> dict[str, Any]:
0036:         structure_id = self._validate_structure_id(structure_id)
0037: 
0038:         before_ts = self._latest_payoff_timestamp(structure_id)
0039: 
0040:         try:
0041:             pricing_result = self._execute_pricing(structure_id, reference_date)
0042:         except Exception as exc:
0043:             return {
0044:                 "status": "error",
0045:                 "structure_id": structure_id,
0046:                 "reference_date": reference_date,
0047:                 "pricing_execution_id": None,
0048:                 "snapshot_id": None,
0049:                 "payoff_points_count": 0,
0050:                 "latest_payoff_timestamp": before_ts,
0051:                 "decision_found": False,
0052:                 "message": f"Erro ao executar pricing: {exc}",
0053:             }
0054: 
0055:         pricing_status = self._extract_status(pricing_result)
0056:         pricing_execution_id = self._extract_pricing_execution_id(pricing_result)
0057: 
0058:         if pricing_status in {"error", "failed", "fail"}:
0059:             return {
0060:                 "status": "error",
0061:                 "structure_id": structure_id,
0062:                 "reference_date": reference_date,
0063:                 "pricing_execution_id": pricing_execution_id,
0064:                 "snapshot_id": None,
0065:                 "payoff_points_count": 0,
0066:                 "latest_payoff_timestamp": before_ts,
0067:                 "decision_found": False,
0068:                 "message": "Pricing retornou erro. Payoff não será considerado atualizado.",
0069:                 "pricing_result": pricing_result,
```

#### Contexto 2

```python
0046:                 "reference_date": reference_date,
0047:                 "pricing_execution_id": None,
0048:                 "snapshot_id": None,
0049:                 "payoff_points_count": 0,
0050:                 "latest_payoff_timestamp": before_ts,
0051:                 "decision_found": False,
0052:                 "message": f"Erro ao executar pricing: {exc}",
0053:             }
0054: 
0055:         pricing_status = self._extract_status(pricing_result)
0056:         pricing_execution_id = self._extract_pricing_execution_id(pricing_result)
0057: 
0058:         if pricing_status in {"error", "failed", "fail"}:
0059:             return {
0060:                 "status": "error",
0061:                 "structure_id": structure_id,
0062:                 "reference_date": reference_date,
0063:                 "pricing_execution_id": pricing_execution_id,
0064:                 "snapshot_id": None,
0065:                 "payoff_points_count": 0,
0066:                 "latest_payoff_timestamp": before_ts,
0067:                 "decision_found": False,
0068:                 "message": "Pricing retornou erro. Payoff não será considerado atualizado.",
0069:                 "pricing_result": pricing_result,
0070:             }
0071: 
0072:         payoff_summary = self._latest_payoff_summary(structure_id)
0073:         after_ts = payoff_summary.get("latest_payoff_timestamp")
0074:         points_count = int(payoff_summary.get("payoff_points_count") or 0)
0075: 
0076:         decision_found = self._decision_exists(structure_id, after_ts)
0077:         snapshot_id = self._latest_snapshot_id(structure_id)
0078: 
0079:         if points_count <= 0:
0080:             return {
0081:                 "status": "error",
0082:                 "structure_id": structure_id,
0083:                 "reference_date": reference_date,
0084:                 "pricing_execution_id": pricing_execution_id,
0085:                 "snapshot_id": snapshot_id,
0086:                 "payoff_points_count": 0,
0087:                 "latest_payoff_timestamp": after_ts,
0088:                 "decision_found": decision_found,
0089:                 "message": (
0090:                     "Pricing executado, mas nenhum payoff persistido foi encontrado. "
0091:                     "Verifique o wiring de DerivedPayoffPersistence."
0092:                 ),
0093:                 "pricing_result": pricing_result,
0094:             }
0095: 
0096:         if before_ts == after_ts:
0097:             return {
0098:                 "status": "warning",
0099:                 "structure_id": structure_id,
0100:                 "reference_date": reference_date,
0101:                 "pricing_execution_id": pricing_execution_id,
0102:                 "snapshot_id": snapshot_id,
```

#### Contexto 3

```python
0075: 
0076:         decision_found = self._decision_exists(structure_id, after_ts)
0077:         snapshot_id = self._latest_snapshot_id(structure_id)
0078: 
0079:         if points_count <= 0:
0080:             return {
0081:                 "status": "error",
0082:                 "structure_id": structure_id,
0083:                 "reference_date": reference_date,
0084:                 "pricing_execution_id": pricing_execution_id,
0085:                 "snapshot_id": snapshot_id,
0086:                 "payoff_points_count": 0,
0087:                 "latest_payoff_timestamp": after_ts,
0088:                 "decision_found": decision_found,
0089:                 "message": (
0090:                     "Pricing executado, mas nenhum payoff persistido foi encontrado. "
0091:                     "Verifique o wiring de DerivedPayoffPersistence."
0092:                 ),
0093:                 "pricing_result": pricing_result,
0094:             }
0095: 
0096:         if before_ts == after_ts:
0097:             return {
0098:                 "status": "warning",
0099:                 "structure_id": structure_id,
0100:                 "reference_date": reference_date,
0101:                 "pricing_execution_id": pricing_execution_id,
0102:                 "snapshot_id": snapshot_id,
0103:                 "payoff_points_count": points_count,
0104:                 "latest_payoff_timestamp": after_ts,
0105:                 "decision_found": decision_found,
0106:                 "message": (
0107:                     "Pricing executado, mas o timestamp do payoff não mudou. "
0108:                     "Pode haver persistência antiga, deduplicação ou falha silenciosa."
0109:                 ),
0110:                 "pricing_result": pricing_result,
0111:             }
0112: 
0113:         return {
0114:             "status": "ok",
0115:             "structure_id": structure_id,
0116:             "reference_date": reference_date,
0117:             "pricing_execution_id": pricing_execution_id,
0118:             "snapshot_id": snapshot_id,
0119:             "payoff_points_count": points_count,
0120:             "latest_payoff_timestamp": after_ts,
0121:             "decision_found": decision_found,
0122:             "message": "Payoff atualizado com sucesso.",
0123:             "pricing_result": pricing_result,
0124:         }
0125: 
0126:     def _execute_pricing(
0127:         self,
0128:         structure_id: int,
0129:         reference_date: str | None,
0130:     ) -> Any:
0131:         method = self.pricing_app_service.execute_pricing
```

#### Contexto 4

```python
0172:                 SELECT status
0173:                   FROM structures
0174:                  WHERE id = ?
0175:                  LIMIT 1
0176:                 """,
0177:                 (structure_id,),
0178:             ).fetchone()
0179: 
0180:         if not row:
0181:             raise ValueError(f"structure not found: {structure_id}")
0182: 
0183:         status = str(row[0] or "").strip().lower()
0184:         if status != "active":
0185:             raise ValueError(
0186:                 f"estrutura inativa/arquivada não pode gerar payoff: "
0187:                 f"structure_id={structure_id}, status={status!r}"
0188:             )
0189: 
0190:     def _connect(self) -> sqlite3.Connection:
0191:         return sqlite3.connect(str(self.db_path))
0192: 
0193:     def _latest_payoff_timestamp(self, structure_id: int) -> str | None:
0194:         return self._latest_payoff_summary(structure_id).get("latest_payoff_timestamp")
0195: 
0196:     def _latest_payoff_summary(self, structure_id: int) -> dict[str, Any]:
0197:         if not self.db_path.exists():
0198:             return {
0199:                 "latest_payoff_timestamp": None,
0200:                 "payoff_points_count": 0,
0201:             }
0202: 
0203:         query = """
0204:             SELECT timestamp, COUNT(*) AS n
0205:             FROM payoff_curve_points
0206:             WHERE structure_id = ?
0207:             GROUP BY timestamp
0208:             ORDER BY timestamp DESC
0209:             LIMIT 1
0210:         """
0211: 
0212:         try:
0213:             with self._connect() as conn:
0214:                 row = conn.execute(query, (structure_id,)).fetchone()
0215:         except sqlite3.Error:
0216:             return {
0217:                 "latest_payoff_timestamp": None,
0218:                 "payoff_points_count": 0,
0219:             }
0220: 
0221:         if not row:
0222:             return {
0223:                 "latest_payoff_timestamp": None,
0224:                 "payoff_points_count": 0,
0225:             }
0226: 
0227:         return {
0228:             "latest_payoff_timestamp": row[0],
```

#### Contexto 5

```python
0201:             }
0202: 
0203:         query = """
0204:             SELECT timestamp, COUNT(*) AS n
0205:             FROM payoff_curve_points
0206:             WHERE structure_id = ?
0207:             GROUP BY timestamp
0208:             ORDER BY timestamp DESC
0209:             LIMIT 1
0210:         """
0211: 
0212:         try:
0213:             with self._connect() as conn:
0214:                 row = conn.execute(query, (structure_id,)).fetchone()
0215:         except sqlite3.Error:
0216:             return {
0217:                 "latest_payoff_timestamp": None,
0218:                 "payoff_points_count": 0,
0219:             }
0220: 
0221:         if not row:
0222:             return {
0223:                 "latest_payoff_timestamp": None,
0224:                 "payoff_points_count": 0,
0225:             }
0226: 
0227:         return {
0228:             "latest_payoff_timestamp": row[0],
0229:             "payoff_points_count": row[1],
0230:         }
0231: 
0232:     def _decision_exists(self, structure_id: int, timestamp: str | None) -> bool:
0233:         if not timestamp or not self.db_path.exists():
0234:             return False
0235: 
0236:         queries = [
0237:             (
0238:                 """
0239:                 SELECT COUNT(*)
0240:                 FROM structure_decisions
0241:                 WHERE structure_id = ?
0242:                   AND timestamp = ?
0243:                 """,
0244:                 (structure_id, timestamp),
0245:             ),
0246:             (
0247:                 """
0248:                 SELECT COUNT(*)
0249:                 FROM structure_decisions
0250:                 WHERE timestamp = ?
0251:                 """,
0252:                 (timestamp,),
0253:             ),
0254:         ]
0255: 
0256:         for query, params in queries:
0257:             try:
```

## 3. Schema do banco

### `pricing_executions`

| cid | name | type | notnull | pk |
|---:|---|---|---:|---:|
| 0 | id | INTEGER | 0 | 1 |
| 1 | created_at | TEXT | 1 | 0 |
| 2 | structure_id | INTEGER | 0 | 0 |
| 3 | underlying_asset | TEXT | 0 | 0 |
| 4 | reference_date | TEXT | 0 | 0 |
| 5 | execution_status | TEXT | 0 | 0 |
| 6 | execution_engine | TEXT | 0 | 0 |
| 7 | error_message | TEXT | 0 | 0 |
| 8 | duration_ms | INTEGER | 0 | 0 |
| 9 | number_of_legs | INTEGER | 0 | 0 |
| 10 | total_quantity | INTEGER | 0 | 0 |
| 11 | theoretical_value | REAL | 0 | 0 |
| 12 | pricing_payload | TEXT | 0 | 0 |
| 13 | result | TEXT | 0 | 0 |

Total de linhas: `141`

### `structure_snapshots`

| cid | name | type | notnull | pk |
|---:|---|---|---:|---:|
| 0 | id | INTEGER | 0 | 1 |
| 1 | created_at | TEXT | 1 | 0 |
| 2 | structure_id | INTEGER | 1 | 0 |
| 3 | pricing_execution_id | INTEGER | 0 | 0 |
| 4 | underlying_asset | TEXT | 0 | 0 |
| 5 | reference_date | TEXT | 0 | 0 |
| 6 | snapshot_source | TEXT | 1 | 0 |
| 7 | structure_json | TEXT | 1 | 0 |
| 8 | market_json | TEXT | 0 | 0 |
| 9 | metrics_json | TEXT | 0 | 0 |
| 10 | payoff_json | TEXT | 0 | 0 |
| 11 | decision_json | TEXT | 0 | 0 |
| 12 | alerts_json | TEXT | 0 | 0 |
| 13 | operation_state_json | TEXT | 0 | 0 |

Total de linhas: `171`

### `system_snapshots`

Tabela ausente.

### `payoff_curve_points`

| cid | name | type | notnull | pk |
|---:|---|---|---:|---:|
| 0 | timestamp | TEXT | 1 | 0 |
| 1 | aba | TEXT | 1 | 0 |
| 2 | structure_id | INTEGER | 0 | 0 |
| 3 | spot_ref | REAL | 0 | 0 |
| 4 | point_spot | REAL | 1 | 0 |
| 5 | point_pl | REAL | 1 | 0 |
| 6 | meta_json | TEXT | 0 | 0 |
| 7 | created_at | TEXT | 0 | 0 |

Total de linhas: `2727`

### `structure_decisions`

| cid | name | type | notnull | pk |
|---:|---|---|---:|---:|
| 0 | id | INTEGER | 0 | 1 |
| 1 | structure_id | INTEGER | 1 | 0 |
| 2 | decision | TEXT | 1 | 0 |
| 3 | label | TEXT | 0 | 0 |
| 4 | note | TEXT | 0 | 0 |
| 5 | created_at | TEXT | 1 | 0 |
| 6 | timestamp | TEXT | 0 | 0 |
| 7 | aba | TEXT | 0 | 0 |
| 8 | level | INTEGER | 0 | 0 |
| 9 | pl_atual | REAL | 0 | 0 |
| 10 | pl_max | REAL | 0 | 0 |
| 11 | pl_pct_of_max | REAL | 0 | 0 |
| 12 | dte_min | INTEGER | 0 | 0 |
| 13 | why_json | TEXT | 0 | 0 |
| 14 | spot_ref | REAL | 0 | 0 |
| 15 | meta_json | TEXT | 0 | 0 |
| 16 | why | TEXT | 0 | 0 |

Total de linhas: `11`

### `structures`

| cid | name | type | notnull | pk |
|---:|---|---|---:|---:|
| 0 | id | INTEGER | 0 | 1 |
| 1 | name | TEXT | 1 | 0 |
| 2 | underlying_asset | TEXT | 1 | 0 |
| 3 | alias_legacy_aba | TEXT | 0 | 0 |
| 4 | status | TEXT | 1 | 0 |
| 5 | notes | TEXT | 0 | 0 |
| 6 | created_at | TEXT | 1 | 0 |
| 7 | updated_at | TEXT | 1 | 0 |

Total de linhas: `9`

### `structure_legs`

| cid | name | type | notnull | pk |
|---:|---|---|---:|---:|
| 0 | id | INTEGER | 0 | 1 |
| 1 | structure_id | INTEGER | 1 | 0 |
| 2 | position_side | TEXT | 1 | 0 |
| 3 | option_type | TEXT | 1 | 0 |
| 4 | symbol | TEXT | 0 | 0 |
| 5 | strike | REAL | 1 | 0 |
| 6 | expiration_date | TEXT | 1 | 0 |
| 7 | quantity | INTEGER | 1 | 0 |
| 8 | premium | REAL | 0 | 0 |
| 9 | multiplier | REAL | 1 | 0 |
| 10 | leg_order | INTEGER | 1 | 0 |
| 11 | notes | TEXT | 0 | 0 |
| 12 | created_at | TEXT | 1 | 0 |
| 13 | updated_at | TEXT | 1 | 0 |

Total de linhas: `24`

### `rtd_option_quotes`

| cid | name | type | notnull | pk |
|---:|---|---|---:|---:|
| 0 | id | INTEGER | 0 | 1 |
| 1 | codigo_opcao | TEXT | 1 | 0 |
| 2 | ativo_base | TEXT | 0 | 0 |
| 3 | call_put | TEXT | 0 | 0 |
| 4 | strike | REAL | 0 | 0 |
| 5 | vencimento | TEXT | 0 | 0 |
| 6 | ultimo_preco | REAL | 0 | 0 |
| 7 | ultima_quantidade | REAL | 0 | 0 |
| 8 | bid | REAL | 0 | 0 |
| 9 | ask | REAL | 0 | 0 |
| 10 | volume | REAL | 0 | 0 |
| 11 | iv | REAL | 0 | 0 |
| 12 | delta | REAL | 0 | 0 |
| 13 | gamma | REAL | 0 | 0 |
| 14 | theta | REAL | 0 | 0 |
| 15 | vega | REAL | 0 | 0 |
| 16 | source | TEXT | 1 | 0 |
| 17 | raw_json | TEXT | 0 | 0 |
| 18 | updated_at | TEXT | 1 | 0 |
| 19 | created_at | TEXT | 1 | 0 |
| 20 | vwap | REAL | 0 | 0 |

Total de linhas: `10`

### `rtd_underlying_quotes`

| cid | name | type | notnull | pk |
|---:|---|---|---:|---:|
| 0 | id | INTEGER | 0 | 1 |
| 1 | ativo | TEXT | 1 | 0 |
| 2 | ultimo_preco | REAL | 0 | 0 |
| 3 | bid | REAL | 0 | 0 |
| 4 | ask | REAL | 0 | 0 |
| 5 | close_price | REAL | 0 | 0 |
| 6 | prev_close | REAL | 0 | 0 |
| 7 | open_price | REAL | 0 | 0 |
| 8 | high_price | REAL | 0 | 0 |
| 9 | low_price | REAL | 0 | 0 |
| 10 | volume | REAL | 0 | 0 |
| 11 | change_percent | REAL | 0 | 0 |
| 12 | source | TEXT | 0 | 0 |
| 13 | updated_at | TEXT | 0 | 0 |
| 14 | created_at | TEXT | 0 | 0 |
| 15 | vwap | REAL | 0 | 0 |

Total de linhas: `2`

