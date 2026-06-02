# Auditoria de Wiring da UI — patch_32
Gerado em: 2026-05-29 16:42:03

## Resumo por arquivo

| Arquivo | Classificação | Legado | Canônico | Derived DB |
|---------|--------------|--------|----------|------------|
| `UI\__init__.py` | ⚪ NEUTRO | 0 | 0 | 0 |
| `UI\components\__init__.py` | ⚪ NEUTRO | 0 | 0 | 0 |
| `UI\components\decisions_grid.py` | 🟡 MISTO | 4 | 13 | 0 |
| `UI\components\details_panel.py` | 🟡 MISTO | 21 | 33 | 10 |
| `UI\components\filters_panel.py` | 🟡 MISTO | 2 | 2 | 0 |
| `UI\components\payoff_chart.py` | 🟡 MISTO | 2 | 2 | 0 |
| `UI\components\structure_editor_dialog.py` | 🟡 MISTO | 2 | 14 | 0 |
| `UI\components\structures_list_panel.py` | 🟡 MISTO | 4 | 6 | 0 |
| `UI\debug_utils.py` | ⚪ NEUTRO | 0 | 0 | 0 |
| `UI\main_window.py` | 🟡 MISTO | 10 | 16 | 3 |
| `UI\models\__init__.py` | ⚪ NEUTRO | 0 | 0 | 0 |
| `UI\models\ui_data.py` | 🟡 MISTO | 40 | 49 | 9 |

---

## Detalhes por arquivo

### `UI\components\decisions_grid.py` — MISTO

**Imports detectados:**
- `datetime`
- `json`
- `tkinter`
- `typing`

**⚠️ Acoplamentos LEGADO:**
- L108 `aba` → `# Exibe structure_id; fallback para aba (compat)`
- L110 `aba` → `decision.get("structure_id") or decision.get("aba") or "N/A"`
- L196 `aba` → `Aceita tanto 'structure_id' quanto 'aba' nos dicts (compat).`
- L203 `aba` → `row_sid = row.get("structure_id") or row.get("aba")`

**✅ Referências CANÔNICAS:**
- L25 `structure_id` → `"structure_id",`
- L43 `structure_id` → `self.tree.heading("structure_id", text="Estrutura")`
- L53 `structure_id` → `self.tree.column("structure_id", width=100, anchor="center")`
- L108 `structure_id` → `# Exibe structure_id; fallback para aba (compat)`
- L109 `structure_id` → `structure_id = (`
- L110 `structure_id` → `decision.get("structure_id") or decision.get("aba") or "N/A"`
- L131 `structure_id` → `structure_id,`
- L193 `structure_id` → `def select_by_key(self, structure_id: str, timestamp: str) -> bool:`
- L195 `structure_id` → `Seleciona a linha cujo (structure_id, timestamp) bate no dataset.`
- L196 `structure_id` → `Aceita tanto 'structure_id' quanto 'aba' nos dicts (compat).`
- L199 `structure_id` → `if not structure_id or not timestamp:`
- L203 `structure_id` → `row_sid = row.get("structure_id") or row.get("aba")`
- L204 `structure_id` → `if row_sid == structure_id and row.get("timestamp") == timestamp:`

### `UI\components\details_panel.py` — MISTO

**Imports detectados:**
- `json`
- `pathlib`
- `sqlite3`
- `tkinter`
- `typing`

**⚠️ Acoplamentos LEGADO:**
- L80 `rtd_analise_robo` → `for table in ("robo_legs_snapshot", "robo_snapshot", "rtd_analise_robo_legs"):`
- L80 `rtd_analise_robo_legs` → `for table in ("robo_legs_snapshot", "robo_snapshot", "rtd_analise_robo_legs"):`
- L83 `aba` → `f"SELECT MAX(timestamp) FROM {table} WHERE aba=?",`
- L260 `aba` → `# Exibe structure_id; fallback para aba (compat)`
- L262 `aba` → `decision_data.get("structure_id") or decision_data.get("aba") or "N/A"`
- L383 `aba` → `Ponto de isolamento: toda query ao DB que usa 'aba' passa por aqui.`
- L384 `aba` → `structure_id == aba no DB (por ora 1:1).`
- L391 `aba` → `aba = self._query_by_structure(structure_id)`
- L405 `aba` → `"timestamp", "aba", "decision", "level",`
- L418 `aba` → `WHERE aba = ?`
- L422 `aba` → `(aba,),`
- L433 `aba` → `d["structure_id"] = d.get("aba")`
- L440 `aba` → `aba = self._query_by_structure(structure_id)`
- L450 `aba` → `WHERE aba = ?`
- L453 `aba` → `(aba,),`
- L464 `aba` → `aba = self._query_by_structure(structure_id)`
- L474 `aba` → `WHERE aba = ?`
- L478 `aba` → `(aba,),`
- L486 `aba` → `"SELECT COUNT(*) AS n FROM payoff_curve_points WHERE aba = ?",`
- L487 `aba` → `(aba,),`
- L565 `aba` → `structure_id = decision.get("structure_id") or decision.get("aba")`

**✅ Referências CANÔNICAS:**
- L62 `structure_id` → `self, structure_id: str`
- L84 `structure_id` → `(structure_id,),`
- L93 `structure_id` → `def _compute_recalc_signature(self, structure_id: str):`
- L95 `structure_id` → `structure_id,`
- L96 `structure_id` → `self._get_latest_snapshot_timestamp_for_structure(structure_id),`
- L260 `structure_id` → `# Exibe structure_id; fallback para aba (compat)`
- L261 `structure_id` → `structure_id = (`
- L262 `structure_id` → `decision_data.get("structure_id") or decision_data.get("aba") or "N/A"`
- L264 `structure_id` → `self.structure_label.config(text=structure_id)`
- L343 `structure_id` → `def on_recalc_finished(self, structure_id: str, ok: bool, message: str = ""):`
- L348 `structure_id` → `structure_id`
- L352 `structure_id` → `msg=message or f"OK: {structure_id} recalculado",`
- L381 `structure_id` → `def _query_by_structure(self, structure_id: str):`
- L384 `structure_id` → `structure_id == aba no DB (por ora 1:1).`
- L386 `structure_id` → `return structure_id  # adapter — futuramente pode virar lookup`
- L389 `structure_id` → `self, structure_id: str`
- L391 `structure_id` → `aba = self._query_by_structure(structure_id)`
- L432 `structure_id` → `# Adapter: expõe structure_id`
- L433 `structure_id` → `d["structure_id"] = d.get("aba")`
- L439 `structure_id` → `def _fetch_payoff_points_from_derived(self, structure_id: str):`
- L440 `structure_id` → `aba = self._query_by_structure(structure_id)`
- L463 `structure_id` → `def _fetch_audit_info_from_derived(self, structure_id: str) -> Dict[str, Any]:`
- L464 `structure_id` → `aba = self._query_by_structure(structure_id)`
- L534 `structure_id` → `def _refresh_current_from_derived(self, structure_id: str):`
- L536 `structure_id` → `decision = self._fetch_latest_decision_from_derived(structure_id)`
- L540 `structure_id` → `pts = self._fetch_payoff_points_from_derived(structure_id)`
- L550 `structure_id` → `audit = self._fetch_audit_info_from_derived(structure_id)`
- L565 `structure_id` → `structure_id = decision.get("structure_id") or decision.get("aba")`
- L566 `structure_id` → `if not structure_id:`
- L575 `structure_id` → `msg=f"Recalc já em andamento ({structure_id})",`
- L580 `structure_id` → `sig = self._compute_recalc_signature(structure_id)`
- L592 `structure_id` → `msg=f"Recalculando {structure_id}...",`
- L596 `structure_id` → `self._on_recalculate_cb(structure_id)`

**📦 Referências derived.db:**
- L55 `derived.db` → `return project_root / "dados" / "derived.db"`
- L400 `structure_decisions` → `"PRAGMA table_info(structure_decisions)"`
- L417 `structure_decisions` → `FROM structure_decisions`
- L449 `payoff_curve_points` → `FROM payoff_curve_points`
- L473 `structure_decisions` → `FROM structure_decisions`
- L486 `payoff_curve_points` → `"SELECT COUNT(*) AS n FROM payoff_curve_points WHERE aba = ?",`
- L491 `derived.db` → `"source_table": "derived.db:structure_decisions / payoff_curve_points",`
- L491 `payoff_curve_points` → `"source_table": "derived.db:structure_decisions / payoff_curve_points",`
- L491 `structure_decisions` → `"source_table": "derived.db:structure_decisions / payoff_curve_points",`
- L535 `derived.db` → `"""Recarrega somente a estrutura atual do derived.db e atualiza widgets."""`

### `UI\components\filters_panel.py` — MISTO

**Imports detectados:**
- `datetime`
- `tkinter`
- `typing`

**⚠️ Acoplamentos LEGADO:**
- L160 `aba` → `def update_abas(self, abas: List[str]):`
- L162 `aba` → `self.update_structures(abas)`

**✅ Referências CANÔNICAS:**
- L114 `structure_id` → `# Envia como "structure_id"; ui_data aceita os dois`
- L115 `structure_id` → `filters["structure_id"] = self.structure_var.get().strip()`

### `UI\components\payoff_chart.py` — MISTO

**Imports detectados:**
- `UI.debug_utils`
- `json`
- `matplotlib`
- `matplotlib.backends.backend_tkagg`
- `matplotlib.figure`
- `matplotlib.ticker`
- `tkinter`
- `typing`

**⚠️ Acoplamentos LEGADO:**
- L309 `aba` → `or decision_data.get("aba", "")`
- L418 `aba` → `or decision_data.get("aba", "")`

**✅ Referências CANÔNICAS:**
- L308 `structure_id` → `decision_data.get("structure_id")`
- L417 `structure_id` → `decision_data.get("structure_id")`

### `UI\components\structure_editor_dialog.py` — MISTO

**Imports detectados:**
- `__future__`
- `repositories.structures_repository`
- `tkinter`
- `typing`

**⚠️ Acoplamentos LEGADO:**
- L208 `aba` → `self._f_alias.set(data.get("alias_legacy_aba") or "")`
- L344 `aba` → `"alias_legacy_aba": self._f_alias.get().strip() or None,`

**✅ Referências CANÔNICAS:**
- L9 `structure_id` → `structure_id: int | None,   # None → nova estrutura`
- L28 `StructuresRepository` → `from repositories.structures_repository import StructuresRepository`
- L28 `structures_repository` → `from repositories.structures_repository import StructuresRepository`
- L38 `structure_id` → `structure_id: Optional[int],`
- L43 `StructuresRepository` → `self._repo         = StructuresRepository(db_path)`
- L44 `structure_id` → `self._structure_id = structure_id`
- L51 `structure_id` → `if structure_id is not None:`
- L52 `structure_id` → `self._load_existing(structure_id)`
- L65 `structure_id` → `title = "Nova Estrutura" if self._structure_id is None else "Editar Estrutura"`
- L199 `structure_id` → `def _load_existing(self, structure_id: int):`
- L200 `structure_id` → `data = self._repo.get_structure(structure_id)`
- L202 `structure_id` → `messagebox.showerror("Erro", f"Estrutura {structure_id} não encontrada.")`
- L355 `structure_id` → `if self._structure_id is None:`
- L358 `structure_id` → `sid = self._structure_id`

### `UI\components\structures_list_panel.py` — MISTO

**Imports detectados:**
- `__future__`
- `repositories.structures_repository`
- `tkinter`
- `typing`

**⚠️ Acoplamentos LEGADO:**
- L44 `aba` → `"""Painel esquerdo da aba Estruturas."""`
- L169 `aba` → `or term in (r.get("alias_legacy_aba") or "").lower()`
- L185 `aba` → `row.get("alias_legacy_aba") or "—",`
- L276 `aba` → `"alias_legacy_aba": src.get("alias_legacy_aba"),`

**✅ Referências CANÔNICAS:**
- L26 `StructuresRepository` → `from repositories.structures_repository import StructuresRepository`
- L26 `structures_repository` → `from repositories.structures_repository import StructuresRepository`
- L58 `StructuresRepository` → `self._repo                  = StructuresRepository(db_path)`
- L210 `structure_id` → `def _get_full_structure(self, structure_id: int) -> Optional[dict]:`
- L213 `structure_id` → `return self._repo.get_structure(structure_id)`
- L282 `structure_id` → `if k not in ("id", "structure_id", "created_at", "updated_at")}`

### `UI\main_window.py` — MISTO

**Imports detectados:**
- `UI.components.decisions_grid`
- `UI.components.details_panel`
- `UI.components.filters_panel`
- `UI.components.payoff_chart`
- `UI.components.structure_editor_dialog`
- `UI.components.structures_list_panel`
- `UI.debug_utils`
- `UI.models.ui_data`
- `datetime`
- `matplotlib.backends.backend_tkagg`
- `matplotlib.pyplot`
- `pathlib`
- `sqlite3`
- `subprocess`
- `sys`
- `threading`
- `time`
- `tkinter`
- `traceback`
- `typing`

**⚠️ Acoplamentos LEGADO:**
- L72 `aba` → `# Painel direito: notebook com abas`
- L140 `aba` → `tools_menu.add_command(label="Verificar Bancos", command=self.check_databases)`
- L272 `aba` → `self.filters_panel.update_abas(self.data_model.get_abas())`
- L289 `aba` → `target_sid = d.get("structure_id") or d.get("aba")`
- L302 `aba` → `sid = d.get("structure_id") or d.get("aba")`
- L425 `aba` → `def recalculate_aba(self, aba: str):`
- L427 `aba` → `self.recalculate_structure(aba)`
- L483 `aba` → `def check_databases(self):`
- L486 `aba` → `status = self.data_model.check_database_status()`
- L650 `aba` → `f"Aba legado : {structure.get('alias_legacy_aba') or '—'}",`

**✅ Referências CANÔNICAS:**
- L184 `structure_id` → `structure_id = decision_data.get("structure_id")`
- L187 `structure_id` → `if structure_id and timestamp:`
- L188 `structure_id` → `self._start_payoff_load(structure_id, timestamp, decision_data)`
- L194 `structure_id` → `self, structure_id: str, timestamp: str, decision_data: Dict`
- L210 `structure_id` → `structure_id, timestamp`
- L214 `structure_id` → `f"payoff structure_id={structure_id} ts_req={timestamp} "`
- L289 `structure_id` → `target_sid = d.get("structure_id") or d.get("aba")`
- L302 `structure_id` → `sid = d.get("structure_id") or d.get("aba")`
- L344 `structure_id` → `def recalculate_structure(self, structure_id: str):`
- L346 `structure_id` → `Recalcula a estrutura identificada por structure_id e atualiza a UI.`
- L351 `structure_id` → `text=f"Recalc já em andamento; ignorando ({structure_id})"`
- L367 `structure_id` → `self.status_bar.config(text=f"Recalculando {structure_id}...")`
- L380 `structure_id` → `structure_id, ok=ok, message=msg`
- L408 `structure_id` → `0, lambda: finish(True, f"OK: {structure_id} recalculado")`
- L670 `structure_id` → `def _on_structure_edit_request(self, structure_id: Optional[int]):`
- L674 `structure_id` → `structure_id=structure_id,`

**📦 Referências derived.db:**
- L5 `derived.db` → `Carrega dados de derived.db e app.db para exibir decisões e payoffs`
- L506 `derived.db` → `• Domain Layer → derived.db`
- L550 `payoff_curve_points` → `src = (info_dict or {}).get("source_table", "payoff_curve_points")`

### `UI\models\ui_data.py` — MISTO

**Imports detectados:**
- `csv`
- `datetime`
- `db.config`
- `json`
- `pathlib`
- `sqlite3`
- `time`
- `typing`

**⚠️ Acoplamentos LEGADO:**
- L29 `aba` → `"aba":           ["aba", "sheet", "tab"],                       # mantido para compat`
- L45 `aba` → `"aba":       ["aba", "sheet", "tab"],`
- L79 `aba` → `# Compatibilidade: _cache_abas continua funcionando (alias)`
- L82 `aba` → `def _cache_abas(self) -> List[str]:`
- L85 `aba` → `@_cache_abas.setter`
- L86 `aba` → `def _cache_abas(self, value: List[str]):`
- L148 `aba` → `"aba":          ["aba"],             # fallback`
- L169 `aba` → `#   Prioriza structure_id; cai em aba se structure_id não mapeado.`
- L173 `aba` → `Retorna (col_name, key_type) onde key_type é 'id' ou 'aba'.`
- L178 `aba` → `if colmap.get("aba"):`
- L179 `aba` → `return colmap["aba"], "aba"`
- L190 `aba` → `Se key_type == 'aba': retorna structure_id como-está (é o aba).`
- L195 `aba` → `return structure_id  # aba mode`
- L211 `aba` → `fallback para aba (esquemas antigos).`
- L219 `aba` → `aba_col = c.get("aba", "NULL")`
- L230 `aba` → `# Fallback: aba`
- L231 `aba` → `aba_col = c.get("aba")`
- L232 `aba` → `if not aba_col:`
- L235 `aba` → `f"SELECT DISTINCT {aba_col} AS structure_id "`
- L244 `aba` → `def get_abas(self) -> List[str]:`
- L252 `aba` → `fallback transparente para aba.`
- L274 `aba` → `"timestamp", "structure_id", "aba", "decision", "level",`
- L303 `aba` → `# ◄ patch_33: filtro por structure_id ou aba (compat)`
- L304 `aba` → `structure_filter = filters.get("structure_id") or filters.get("aba")`
- L312 `aba` → `# Veio como aba-string; resolve via subquery`
- L314 `aba` → `"t.aba = ? OR CAST(t.structure_id AS TEXT) = ?"`
- L318 `aba` → `# Schema antigo: só tem aba`
- L319 `aba` → `where.append("t.aba = ?")`
- L337 `aba` → `t.timestamp, t.structure_id, t.aba, t.decision, t.level,`
- L351 `aba` → `# ◄ patch_3a: structure_id é autoritativo (int); aba espelha o mesmo valor`
- L353 `aba` → `raw_aba = item.get("aba")`
- L355 `aba` → `item["structure_id"] = int(raw_aba) if raw_aba is not None else None`
- L357 `aba` → `item["structure_id"] = raw_aba`
- L358 `aba` → `if item.get("aba") is None or item.get("aba") != item.get("structure_id"):`
- L359 `aba` → `item["aba"] = item.get("structure_id")`
- L386 `aba` → `Aceita structure_id como int-string ("7") ou aba ("BOVA11").`
- L461 `aba` → `Fallback para aba mantido para compatibilidade.`
- L492 `aba` → `"aba": structure_id,   # ◄ patch_3a: aba espelha structure_id (compat)`
- L583 `aba` → `"timestamp", "structure_id", "aba", "decision", "level",`
- L602 `aba` → `def check_database_status(self) -> str:`

**✅ Referências CANÔNICAS:**
- L28 `structure_id` → `"structure_id":  ["structure_id"],                              # ◄ patch_33: chave canônica`
- L44 `structure_id` → `"structure_id": ["structure_id"],   # ◄ patch_33`
- L147 `structure_id` → `"structure_id": ["structure_id"],   # ◄ patch_33: preferido`
- L169 `structure_id` → `#   Prioriza structure_id; cai em aba se structure_id não mapeado.`
- L176 `structure_id` → `if colmap.get("structure_id"):`
- L177 `structure_id` → `return colmap["structure_id"], "id"`
- L184 `structure_id` → `structure_id: str,`
- L189 `structure_id` → `Se key_type == 'id': converte structure_id (str/int) para INTEGER.`
- L190 `structure_id` → `Se key_type == 'aba': retorna structure_id como-está (é o aba).`
- L193 `structure_id` → `# structure_id pode vir como str ("7") ou int (7)`
- L194 `structure_id` → `return int(structure_id)`
- L195 `structure_id` → `return structure_id  # aba mode`
- L209 `structure_id` → `Carrega lista de structure_ids distintos.`
- L210 `structure_id` → `◄ patch_33: usa structure_id diretamente se disponível;`
- L216 `structure_id` → `# ◄ patch_33: preferir structure_id`
- L217 `structure_id` → `if c.get("structure_id"):`
- L218 `structure_id` → `sid_col = c["structure_id"]`
- L221 `structure_id` → `f"SELECT DISTINCT CAST({sid_col} AS TEXT) AS structure_id "`
- L224 `structure_id` → `f"ORDER BY structure_id"`
- L228 `structure_id` → `return [r["structure_id"] for r in rows]`
- L235 `structure_id` → `f"SELECT DISTINCT {aba_col} AS structure_id "`
- L237 `structure_id` → `f"ORDER BY structure_id"`
- L239 `structure_id` → `return [r["structure_id"] for r in conn.execute(q).fetchall()]`
- L251 `structure_id` → `◄ patch_33: filtra por structure_id quando disponível;`
- L274 `structure_id` → `"timestamp", "structure_id", "aba", "decision", "level",`
- L303 `structure_id` → `# ◄ patch_33: filtro por structure_id ou aba (compat)`
- L304 `structure_id` → `structure_filter = filters.get("structure_id") or filters.get("aba")`
- L306 `structure_id` → `if c.get("structure_id"):`
- L307 `structure_id` → `# Tenta filtrar por INTEGER structure_id`
- L309 `structure_id` → `where.append("t.structure_id = ?")`
- L314 `structure_id` → `"t.aba = ? OR CAST(t.structure_id AS TEXT) = ?"`
- L337 `structure_id` → `t.timestamp, t.structure_id, t.aba, t.decision, t.level,`
- L351 `structure_id` → `# ◄ patch_3a: structure_id é autoritativo (int); aba espelha o mesmo valor`
- L352 `structure_id` → `if item.get("structure_id") is None:`
- L355 `structure_id` → `item["structure_id"] = int(raw_aba) if raw_aba is not None else None`
- L357 `structure_id` → `item["structure_id"] = raw_aba`
- L358 `structure_id` → `if item.get("aba") is None or item.get("aba") != item.get("structure_id"):`
- L359 `structure_id` → `item["aba"] = item.get("structure_id")`
- L383 `structure_id` → `def get_payoff_curve(self, structure_id: str, timestamp: str) -> List[Dict]:`
- L386 `structure_id` → `Aceita structure_id como int-string ("7") ou aba ("BOVA11").`
- L389 `structure_id` → `cache_key = (str(structure_id), ts_key)`
- L415 `structure_id` → `filter_val = self._resolve_structure_key(structure_id, key_type, conn)`
- L457 `structure_id` → `self, structure_id: str, timestamp: str`
- L460 `structure_id` → `◄ patch_33: usa structure_id como chave primária quando disponível.`
- L471 `structure_id` → `cache_key = (str(structure_id), ts_key)`
- L488 `structure_id` → `filter_val = self._resolve_structure_key(structure_id, key_type, conn)`
- L491 `structure_id` → `"structure_id": structure_id,`
- L492 `structure_id` → `"aba": structure_id,   # ◄ patch_3a: aba espelha structure_id (compat)`
- L583 `structure_id` → `"timestamp", "structure_id", "aba", "decision", "level",`

**📦 Referências derived.db:**
- L12 `structure_decisions` → `"structure_decisions",`
- L19 `payoff_curve_points` → `"payoff_curve_points",`
- L93 `derived.db` → `f"Banco derived.db não encontrado em: {self.derived_db_path}"`
- L142 `payoff_curve_points` → `if self._payoff_table == "payoff_curve_points":`
- L504 `payoff_curve_points` → `if self._payoff_table == "payoff_curve_points":`
- L507 `payoff_curve_points` → `if "meta_json" in self._inspect_columns("payoff_curve_points"):`
- L512 `payoff_curve_points` → `f"FROM payoff_curve_points "`
- L521 `payoff_curve_points` → `f"SELECT timestamp FROM payoff_curve_points "`
- L630 `derived.db` → `f"derived.db: OK\n"`

---

## Sumário final

- 🔴 LEGADO_PURO : 0 arquivo(s)
- 🟡 MISTO       : 8 arquivo(s)
- 🟢 CANÔNICO    : 0 arquivo(s)
- ⚪ NEUTRO      : 4 arquivo(s)

### Ação recomendada
- LEGADO_PURO → migrar para domínio canônico no patch_33
- MISTO       → avaliar caso a caso; priorizar remoção do legado
- CANÔNICO    → manter; validar no smoke
