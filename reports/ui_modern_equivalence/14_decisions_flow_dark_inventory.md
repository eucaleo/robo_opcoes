# Inventario tecnico do fluxo de decisoes para modo dark

## 1. Objetivo

Mapear o fluxo reaproveitavel de decisoes existente na UI moderna para orientar a proxima implementacao parcial no modo dark.

Escopo analisado:

- filtros;
- tabela/listagem de decisoes;
- selecao de decisao;
- detalhe da decisao;
- conexoes entre componentes;
- pontos minimos de integracao com o dark_window.

Esta etapa e documental. Nao altera codigo funcional.


## 2. Arquivo: `UI/components/filters_panel.py`

### 2.1. Classes encontradas

- `FiltersPanel`

### 2.2. Funcoes/metodos encontrados

- `__init__`
- `_setup_widgets`
- `_bind_events`
- `_apply_filters`
- `reset_filters`
- `update_structures`

### 2.3. Sinais Qt encontrados

- Nenhum sinal Qt identificado por regex simples.

### 2.4. Imports principais

- `import tkinter as tk`
- `from tkinter import ttk`
- `from typing import Dict, List, Optional, Callable`
- `from datetime import datetime, timedelta`

### 2.5. Ocorrencias relevantes

- L1: `# UI/components/filters_panel.py`
- L7: `class FiltersPanel(ttk.LabelFrame):`
- L8: `def __init__(self, parent, on_filter_change: Callable[[Dict], None]):`
- L9: `super().__init__(parent, text="Filtros", padding=10)`
- L11: `self.on_filter_change = on_filter_change`
- L39: `# Linha 2: Estrutura e Decisão`
- L53: `ttk.Label(row2, text="Decisão:").pack(side="left")`
- L54: `self.decision_var = tk.StringVar()`
- L55: `self.decision_combo = ttk.Combobox(`
- L57: `textvariable=self.decision_var,`
- L62: `self.decision_combo.pack(side="left", padx=(5, 0))`
- L83: `btn_frame, text="Aplicar", command=self._apply_filters`
- L88: `btn_frame, text="Limpar", command=self.reset_filters`
- L93: `self.status_label = ttk.Label(self, text="Filtros prontos", foreground="green")`
- L98: `w.bind("<Return>", lambda e: self._apply_filters())`
- L100: `self.structure_combo.bind("<<ComboboxSelected>>", lambda e: self._apply_filters())`
- L101: `self.decision_combo.bind("<<ComboboxSelected>>", lambda e: self._apply_filters())`
- L103: `def _apply_filters(self):`
- L104: `filters: Dict = {}`
- L107: `filters["date_from"] = self.date_from_var.get().strip()`
- L110: `filters["date_to"] = self.date_to_var.get().strip()`
- L114: `filters["structure_id"] = self.structure_var.get().strip()`
- L116: `if self.decision_var.get().strip():`
- L117: `filters["decision"] = self.decision_var.get().strip()`
- L121: `filters["level_min"] = int(self.level_var.get().strip())`
- L127: `filters["dte_max"] = int(self.dte_var.get().strip())`
- L132: `text=f"Filtros aplicados ({len(filters)} ativos)",`
- L135: `self.on_filter_change(filters)`
- L137: `def reset_filters(self):`
- L139: `self.decision_var.set("")`
- L148: `self.status_label.config(text="Filtros limpos", foreground="green")`
- L149: `self._apply_filters()`

## 2. Arquivo: `UI/components/decisions_grid.py`

### 2.1. Classes encontradas

- `DecisionsGrid`

### 2.2. Funcoes/metodos encontrados

- `__init__`
- `_setup_treeview`
- `_setup_scrollbars`
- `_on_tree_select`
- `update_data`
- `_format_timestamp`
- `_format_ratio`
- `_format_currency`
- `get_current_data`
- `get_selected_decision`
- `select_by_key`

### 2.3. Sinais Qt encontrados

- Nenhum sinal Qt identificado por regex simples.

### 2.4. Imports principais

- `from src.domain.refs.structure_ref import StructureRef`
- `import tkinter as tk`
- `from tkinter import ttk`
- `from typing import Dict, List, Optional, Callable`
- `import json`

### 2.5. Ocorrencias relevantes

- L1: `# UI/components/decisions_grid.py`
- L9: `class DecisionsGrid(ttk.LabelFrame):`
- L13: `on_selection_change: Callable[[Optional[Dict]], None],`
- L15: `super().__init__(parent, text="Decisões", padding=5)`
- L17: `self.on_selection_change = on_selection_change`
- L27: `"decision",`
- L45: `self.tree.heading("decision", text="Decisão")`
- L55: `self.tree.column("decision", width=100, anchor="center")`
- L65: `# Tags de cor por decisão`
- L79: `self.tree.grid(row=0, column=0, sticky="nsew")`
- L80: `v_scrollbar.grid(row=0, column=1, sticky="ns")`
- L81: `h_scrollbar.grid(row=1, column=0, sticky="ew")`
- L83: `self.grid_rowconfigure(0, weight=1)`
- L84: `self.grid_columnconfigure(0, weight=1)`
- L87: `selection = self.tree.selection()`
- L88: `if not selection:`
- L89: `self.on_selection_change(None)`
- L92: `item_id = selection[0]`
- L96: `self.on_selection_change(self.current_data[index])`
- L98: `self.on_selection_change(None)`
- L100: `def update_data(self, decisions: List[Dict]):`
- L101: `"""Atualiza grid com nova lista de decisões."""`
- L102: `self.current_data = decisions.copy()`
- L107: `for i, decision in enumerate(decisions, 1):`
- L108: `timestamp = self._format_timestamp(decision.get("timestamp"))`
- L111: `decision.get("structure_id") or decision.get("aba") or "N/A"`
- L113: `decision_text = decision.get("decision", "N/A")`
- L114: `level = decision.get("level", "")`
- L115: `ratio = self._format_ratio(decision.get("pl_pct_of_max"))`
- L116: `dte = decision.get("dte_min", "")`
- L117: `pl_atual = self._format_currency(decision.get("pl_atual"))`
- L118: `pl_max = self._format_currency(decision.get("pl_max"))`
- L121: `decision_text`
- L122: `if decision_text in ["HOLD", "PREPARE_ROLL", "CLOSE_REOPEN", "ROLL", "ENTER"]`
- L133: `decision_text,`
- L181: `def get_selected_decision(self) -> Optional[Dict]:`
- L182: `"""Retorna decisão atualmente selecionada."""`
- L183: `selection = self.tree.selection()`
- L184: `if not selection:`
- L187: `index = int(selection[0]) - 1`
- L208: `self.tree.selection_set(iid)`

## 2. Arquivo: `UI/components/details_panel.py`

### 2.1. Classes encontradas

- `DetailsPanel`

### 2.2. Funcoes/metodos encontrados

- `__init__`
- `_set_recalc_ui_state`
- `_derived_db_path`
- `_operational_app_db_path`
- `_resolve_structure_key`
- `_get_latest_snapshot_timestamp_for_structure`
- `_safe_path`
- `_looks_like_db_path`
- `q`
- `table_names`
- `columns_for`
- `looks_like_structure_col`
- `timestamp_score`
- `latest_in_table`
- `_compute_recalc_signature`
- `_setup_widgets`
- `update_decision`
- `update_breakevens`
- `update_audit_info`
- `clear`
- `on_recalc_finished`
- `_clear_operational_state`
- `update_operational_state`
- `_fetch_effective_structure_local`
- `_refresh_operational_state_for_structure`
- `_format_currency_label`
- `_fetch_latest_decision_from_derived`
- `_fetch_payoff_points_from_derived`
- `_fetch_audit_info_from_derived`
- `_compute_breakevens_from_points`
- `_compute_pl_at_spot`
- `_refresh_current_from_derived`
- `_on_recalculate_click`

### 2.3. Sinais Qt encontrados

- Nenhum sinal Qt identificado por regex simples.

### 2.4. Imports principais

- `import tkinter as tk`
- `from tkinter import ttk, scrolledtext`
- `from typing import Dict, Optional, Any`
- `import json`
- `import sqlite3`
- `from pathlib import Path`

### 2.5. Ocorrencias relevantes

- L1: `# UI/components/details_panel.py`
- L10: `class DetailsPanel(ttk.LabelFrame):`
- L17: `self._current_decision = None`
- L282: `def table_names(cur):`
- L287: `WHERE type = 'table'`
- L293: `def columns_for(cur, table):`
- L294: `rows = cur.execute(f"PRAGMA table_info({q(table)})").fetchall()`
- L345: `def latest_in_table(cur, table):`
- L346: `cols = columns_for(cur, table)`
- L388: `FROM {q(table)}`
- L410: `"structure_decisions",`
- L411: `"payoff_curve_points",`
- L419: `con = sqlite3.connect(str(db_path))`
- L422: `tables = table_names(cur)`
- L426: `if t in tables and t not in ordered:`
- L428: `for t in tables:`
- L432: `for table in ordered:`
- L433: `ts = latest_in_table(cur, table)`
- L454: `self.grid_rowconfigure(3, weight=1)`
- L455: `self.grid_columnconfigure(1, weight=1)`
- L459: `basic_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 5))`
- L460: `basic_frame.grid_columnconfigure(1, weight=1)`
- L461: `basic_frame.grid_columnconfigure(3, weight=1)`
- L463: `ttk.Label(basic_frame, text="Timestamp:").grid(`
- L469: `self.timestamp_label.grid(row=0, column=1, sticky="ew", padx=(0, 10))`
- L471: `ttk.Label(basic_frame, text="Estrutura:").grid(`
- L477: `self.structure_label.grid(row=0, column=3, sticky="ew")`
- L479: `ttk.Label(basic_frame, text="Decisão:").grid(`
- L482: `self.decision_label = ttk.Label(`
- L485: `self.decision_label.grid(row=1, column=1, sticky="ew", padx=(0, 10))`
- L487: `ttk.Label(basic_frame, text="Nível:").grid(`
- L493: `self.level_label.grid(row=1, column=3, sticky="ew")`
- L497: `metrics_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)`
- L498: `metrics_frame.grid_columnconfigure(1, weight=1)`
- L499: `metrics_frame.grid_columnconfigure(3, weight=1)`
- L501: `ttk.Label(metrics_frame, text="PL Atual:").grid(`
- L507: `self.pl_atual_label.grid(row=0, column=1, sticky="ew", padx=(0, 10))`
- L509: `ttk.Label(metrics_frame, text="PL Máximo:").grid(`
- L515: `self.pl_max_label.grid(row=0, column=3, sticky="ew")`
- L517: `ttk.Label(metrics_frame, text="Ratio:").grid(`
- L523: `self.ratio_label.grid(row=1, column=1, sticky="ew", padx=(0, 10))`
- L525: `ttk.Label(metrics_frame, text="DTE Mín:").grid(`
- L531: `self.dte_label.grid(row=1, column=3, sticky="ew")`
- L533: `ttk.Label(metrics_frame, text="Spot Ref:").grid(`
- L539: `self.spot_ref_label.grid(row=2, column=1, sticky="ew", padx=(0, 10))`
- L541: `ttk.Label(metrics_frame, text="Breakevens:").grid(`
- L547: `self.breakevens_label.grid(row=2, column=3, sticky="ew")`
- L551: `operational_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)`
- L552: `operational_frame.grid_columnconfigure(1, weight=1)`
- L553: `operational_frame.grid_columnconfigure(3, weight=1)`
- L555: `ttk.Label(operational_frame, text="Eventos aplicados:").grid(`
- L561: `self.operational_events_applied_label.grid(`
- L565: `ttk.Label(operational_frame, text="Cancelados ignorados:").grid(`
- L571: `self.operational_cancelled_ignored_label.grid(`
- L575: `ttk.Label(operational_frame, text="Status:").grid(`
- L581: `self.operational_status_label.grid(`
- L587: `json_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(5, 0))`
- L588: `json_frame.grid_rowconfigure(0, weight=1)`
- L589: `json_frame.grid_columnconfigure(0, weight=1)`
- L598: `self.why_text.grid(row=0, column=0, sticky="nsew")`
- L602: `audit_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)`
- L603: `audit_frame.grid_columnconfigure(1, weight=1)`
- L604: `audit_frame.grid_columnconfigure(3, weight=1)`
- L606: `ttk.Label(audit_frame, text="Fonte:").grid(`
- L612: `self.source_label.grid(row=0, column=1, sticky="ew", padx=(0, 10))`
- L614: `ttk.Label(audit_frame, text="Created At:").grid(`
- L620: `self.created_at_label.grid(row=0, column=3, sticky="ew")`
- L623: `actions_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(5, 0))`
- L641: `def update_decision(self, decision_data: Dict):`
- L642: `self._current_decision = dict(decision_data) if decision_data else None`
- L644: `self.timestamp_label.config(text=decision_data.get("timestamp", "N/A"))`
- L647: `structure_id = decision_data.get("structure_id") or "N/A"`
- L650: `self.decision_label.config(text=decision_data.get("decision", "N/A"))`
- L651: `self.level_label.config(text=str(decision_data.get("level", "N/A")))`
- L653: `self._format_currency_label(self.pl_atual_label, decision_data.get("pl_atual"))`
- L654: `self._format_currency_label(self.pl_max_label, decision_data.get("pl_max"))`
- L656: `ratio = decision_data.get("pl_pct_of_max")`
- L661: `self.dte_label.config(text=str(decision_data.get("dte_min", "N/A")))`
- L663: `spot_ref = decision_data.get("spot_reference") or decision_data.get("spot_ref")`
- L672: `why_payload = decision_data.get("why") or decision_data.get("why_json")`
- L694: `self._refresh_operational_state_for_structure(structure_id)`
- L708: `source_table = info.get("source_table", "N/A")`
- L711: `txt = f"{source_table}{suffix}"`
- L720: `self._current_decision = None`
- L722: `self.timestamp_label, self.structure_label, self.decision_label,`
- L854: `def _refresh_operational_state_for_structure(self, structure_id):`
- L878: `def _fetch_latest_decision_from_derived(`
- L882: `alteracao_36: filtra por structure_id (INTEGER) em structure_decisions.`
- L887: `con = sqlite3.connect(str(db_path))`
- L892: `"structure_id", "timestamp", "decision", "level",`
- L900: `FROM structure_decisions`
- L920: `def _fetch_payoff_points_from_derived(self, structure_id):`
- L922: `alteracao_36: filtra por structure_id (INTEGER) em payoff_curve_points.`
- L927: `con = sqlite3.connect(str(db_path))`
- L934: `FROM payoff_curve_points`
- L955: `con = sqlite3.connect(str(db_path))`
- L962: `FROM structure_decisions`
- L975: `"SELECT COUNT(*) AS n FROM payoff_curve_points WHERE structure_id = ?",`
- L980: `"source_table": "derived.db:structure_decisions / payoff_curve_points",`
- L1023: `def _refresh_current_from_derived(self, structure_id):`
- L1025: `decision = self._fetch_latest_decision_from_derived(structure_id)`
- L1026: `if decision:`
- L1027: `self.update_decision(decision)`
- L1029: `pts = self._fetch_payoff_points_from_derived(structure_id)`
- L1033: `if decision:`
- L1034: `spot_ref = decision.get("spot_reference")`
- L1047: `decision = self._current_decision`
- L1048: `if not decision:`
- L1050: `text="Nenhuma decisão selecionada", foreground="red"`
- L1055: `structure_id = decision.get("structure_id")`

## 2. Arquivo: `UI/modern/main_window.py`

### 2.1. Classes encontradas

- `ModernMainWindow`

### 2.2. Funcoes/metodos encontrados

- `__init__`
- `_setup_style`
- `_setup_layout`
- `_build_header`
- `_build_sidebar`
- `_side_button`
- `_build_workspace`
- `_build_analysis_tab`
- `_build_structures_tab`
- `_build_terminal_tab`
- `_bind_events`
- `set_status`
- `on_filter_change`
- `on_decision_selected`
- `_start_payoff_load`
- `worker`
- `_finish_payoff_load`
- `_handle_payoff_error`
- `refresh_data`
- `export_csv`
- `run_pipeline`
- `recalculate_structure`
- `finish`
- `worker`
- `check_databases`
- `clear_cache`
- `_on_structure_selected`
- `_on_structure_edit_request`
- `run`
- `main`

### 2.3. Sinais Qt encontrados

- Nenhum sinal Qt identificado por regex simples.

### 2.4. Imports principais

- `from __future__ import annotations`
- `import subprocess`
- `import sys`
- `import threading`
- `import tkinter as tk`
- `from pathlib import Path`
- `from tkinter import filedialog, messagebox, ttk`
- `from typing import Dict, List, Optional`
- `from UI.components.decisions_grid import DecisionsGrid`
- `from UI.components.details_panel import DetailsPanel`
- `from UI.components.filters_panel import FiltersPanel`
- `from UI.components.payoff_chart import PayoffChart`
- `from UI.components.structure_editor_dialog import StructureEditorDialog`
- `from UI.components.structures_list_panel import StructuresListPanel`
- `from UI.models.ui_data import UIDataModel`
- `from UI.debug_utils import debug`

### 2.5. Ocorrencias relevantes

- L20: `from UI.components.decisions_grid import DecisionsGrid`
- L21: `from UI.components.details_panel import DetailsPanel`
- L22: `from UI.components.filters_panel import FiltersPanel`
- L23: `from UI.components.payoff_chart import PayoffChart`
- L26: `from UI.models.ui_data import UIDataModel`
- L50: `self.data_model = UIDataModel()`
- L53: `self._payoff_worker_id = 0`
- L54: `self._loading_payoff = False`
- L56: `self.last_selected_decision: Optional[Dict] = None`
- L64: `self.refresh_data()`
- L159: `self._side_button(sidebar, "Atualizar dados", self.refresh_data)`
- L206: `self.filters_panel = FiltersPanel(`
- L208: `on_filter_change=self.on_filter_change,`
- L210: `self.filters_panel.pack(fill="x", padx=4, pady=(0, 6))`
- L212: `self.decisions_grid = DecisionsGrid(`
- L214: `on_selection_change=self.on_decision_selected,`
- L216: `self.decisions_grid.pack(fill="both", expand=True, padx=4, pady=4)`
- L218: `detail_notebook = ttk.Notebook(right)`
- L219: `detail_notebook.pack(fill="both", expand=True, padx=4, pady=4)`
- L221: `details_frame = ttk.Frame(detail_notebook)`
- L222: `detail_notebook.add(details_frame, text="Detalhes da decisão")`
- L224: `self.details_panel = DetailsPanel(`
- L225: `details_frame,`
- L229: `self.details_panel.pack(fill="both", expand=True, padx=4, pady=4)`
- L231: `chart_frame = ttk.Frame(detail_notebook)`
- L232: `detail_notebook.add(chart_frame, text="Curva de payoff")`
- L234: `self.payoff_chart = PayoffChart(chart_frame)`
- L235: `self.payoff_chart.pack(fill="both", expand=True, padx=4, pady=4)`
- L252: `on_structure_selected=self._on_structure_selected,`
- L258: `self._struct_detail_text = tk.Text(`
- L265: `self._struct_detail_text.pack(fill="both", expand=True)`
- L269: `notebook.add(tab, text="Terminal VWAP Payoff")`
- L272: `from controllers.terminal_vwap_payoff_controller import (`
- L273: `TerminalVWAPPayoffController,`
- L276: `from services.terminal_vwap_payoff_app_service import (`
- L277: `TerminalVWAPPayoffAppService,`
- L279: `from UI.components.terminal_vwap_payoff_panel import TerminalVWAPPayoffPanel`
- L282: `app_service = TerminalVWAPPayoffAppService(`
- L285: `controller = TerminalVWAPPayoffController(app_service)`
- L287: `self.terminal_vwap_payoff_panel = TerminalVWAPPayoffPanel(`
- L292: `self.terminal_vwap_payoff_panel.pack(`
- L303: `"Terminal VWAP Payoff indisponível neste shell.\n\n"`
- L311: `self.root.bind("<F5>", lambda _e: self.refresh_data())`
- L322: `# Decisões / filtros / payoff`
- L325: `def on_filter_change(self, filters: Dict) -> None:`
- L326: `self.set_status("Aplicando filtros...")`
- L329: `filtered_data = self.data_model.get_decisions(filters)`
- L330: `self.decisions_grid.update_data(filtered_data)`
- L331: `self.set_status(f"{len(filtered_data)} decisões encontradas")`
- L333: `messagebox.showerror("Erro", f"Erro ao aplicar filtros: {exc}")`
- L334: `self.set_status("Erro nos filtros")`
- L336: `def on_decision_selected(self, decision_data: Dict) -> None:`
- L337: `if not decision_data:`
- L340: `self.last_selected_decision = dict(decision_data)`
- L343: `self.details_panel.update_decision(decision_data)`
- L347: `structure_id = decision_data.get("structure_id")`
- L348: `timestamp = decision_data.get("timestamp")`
- L351: `self._start_payoff_load(structure_id, timestamp, decision_data)`
- L353: `self.payoff_chart.clear()`
- L354: `self.set_status("Dados insuficientes para carregar payoff")`
- L356: `def _start_payoff_load(`
- L360: `decision_data=None,`
- L362: `if decision_data is None:`
- L363: `decision_data = {"structure_id": structure_id}`
- L365: `self._payoff_worker_id += 1`
- L366: `worker_id = self._payoff_worker_id`
- L367: `self._loading_payoff = True`
- L368: `self.set_status("Carregando payoff...")`
- L372: `points, info_dict = self.data_model.get_payoff_curve_info(`
- L379: `f"[ModernUI] payoff structure_id={structure_id} "`
- L407: `if worker_id != self._payoff_worker_id:`
- L412: `self._finish_payoff_load,`
- L415: `decision_data,`
- L420: `if worker_id == self._payoff_worker_id:`
- L423: `self._handle_payoff_error,`
- L430: `def _finish_payoff_load(`
- L434: `decision_data: Dict,`
- L437: `if worker_id != self._payoff_worker_id:`
- L440: `self._loading_payoff = False`
- L444: `overlays = self.payoff_chart.update_chart(points, decision_data)`
- L447: `self.details_panel.update_breakevens(`
- L455: `self.details_panel.update_audit_info(info_dict or {})`
- L459: `used_ts = (info_dict or {}).get("used_timestamp") or decision_data.get(`
- L462: `source = (info_dict or {}).get("source_table", "payoff_curve_points")`
- L466: `if used_ts and used_ts != decision_data.get("timestamp"):`
- L471: `self.payoff_chart.clear()`
- L472: `self.set_status("Sem dados de payoff para esta seleção")`
- L475: `self._handle_payoff_error(str(exc), worker_id)`
- L477: `def _handle_payoff_error(self, error_msg: str, worker_id: int) -> None:`
- L478: `if worker_id != self._payoff_worker_id:`
- L481: `self._loading_payoff = False`
- L484: `self.payoff_chart.clear()`
- L488: `self.set_status(f"Erro ao carregar payoff: {error_msg}")`
- L489: `print(f"[ModernUI] Erro no payoff: {error_msg}")`
- L491: `def refresh_data(self) -> None:`
- L495: `self.data_model.refresh()`
- L498: `self.filters_panel.update_structures(`
- L499: `self.data_model.get_structures()`
- L505: `self.filters_panel.reset_filters()`
- L509: `decisions = self.data_model.get_decisions()`
- L510: `self.decisions_grid.update_data(decisions)`
- L513: `previous = self.last_selected_decision`
- L521: `self.decisions_grid.select_by_key(structure_id, timestamp)`
- L526: `self.details_panel.update_decision(previous)`
- L531: `self._start_payoff_load(structure_id, timestamp, previous)`
- L538: `self.details_panel.clear()`
- L543: `self.payoff_chart.clear()`
- L547: `self.set_status(f"Dados atualizados - {len(decisions)} decisões")`
- L567: `current_data = self.decisions_grid.get_current_data()`
- L568: `self.data_model.export_to_csv(current_data, filename)`
- L597: `[sys.executable, str(script_path)],`
- L610: `self.refresh_data()`
- L633: `self.payoff_chart.fix_current_curve()`
- L644: `if hasattr(self.details_panel, "on_recalc_finished"):`
- L645: `self.details_panel.on_recalc_finished(`
- L651: `print("[ModernUI] Erro notificando details_panel:", exc)`
- L660: `[sys.executable, str(script_path)],`
- L673: `self.root.after(0, self.refresh_data)`
- L695: `status = self.data_model.check_database_status()`
- L703: `self.data_model.clear_cache()`
- L711: `def _on_structure_selected(self, structure: Optional[Dict]) -> None:`
- L712: `txt = self._struct_detail_text`

## 2. Arquivo: `UI/modern/dark_window.py`

### 2.1. Classes encontradas

- `ModernDarkWindow`

### 2.2. Funcoes/metodos encontrados

- `__init__`
- `_build_menu`
- `_build_layout`
- `set_status`
- `_reload_panel`
- `_show_about`
- `run`
- `main`

### 2.3. Sinais Qt encontrados

- Nenhum sinal Qt identificado por regex simples.

### 2.4. Imports principais

- `from __future__ import annotations`
- `import tkinter as tk`
- `from pathlib import Path`
- `from tkinter import messagebox`
- `import customtkinter as ctk`
- `from UI.modern.theme import CUSTOMTKINTER_APPEARANCE_MODE, CUSTOMTKINTER_COLOR_THEME`
- `from UI.components.terminal_vwap_payoff_dark_panel import TerminalVWAPPayoffDarkPanel`

### 2.5. Ocorrencias relevantes

- L6: `Ele abre diretamente o TerminalVWAPPayoffDarkPanel, que corresponde`
- L20: `from UI.components.terminal_vwap_payoff_dark_panel import TerminalVWAPPayoffDarkPanel`
- L50: `app_menu.add_command(label="Atualizar", command=self._reload_panel)`
- L70: `self.panel = TerminalVWAPPayoffDarkPanel(`
- L81: `def _reload_panel(self) -> None:`
- L83: `if hasattr(self.panel, "reload_structures"):`
- L84: `self.panel.reload_structures()`

## 3. Analise preliminar

Preencher apos leitura do inventario:

### 3.1. Fluxo atual na UI moderna principal

- Como filtros disparam consulta:
- Como a tabela/listagem recebe dados:
- Como a selecao de decisao e propagada:
- Como o painel de detalhes e atualizado:
- Como payoff e acionado a partir da decisao:

### 3.2. Lacunas no modo dark

- O que ja existe no dark_window:
- O que falta para listar decisoes:
- O que falta para selecionar decisao:
- O que falta para exibir detalhe:
- O que nao deve ser migrado neste primeiro patch:

### 3.3. Recorte recomendado para o primeiro patch funcional

Proposta inicial:

- adicionar area/listagem simples de decisoes no modo dark;
- conectar selecao a um detalhe textual simples;
- reaproveitar componente existente se nao exigir grande refatoracao;
- nao alterar banco;
- nao alterar entrypoint;
- nao remover UI atual;
- nao implementar filtros avancados nesta rodada.

## 4. Decisao

Status: inventario tecnico inicial gerado automaticamente.

Proxima acao: revisar manualmente os pontos de conexao em `main_window.py` e decidir se `decisions_grid.py` e `details_panel.py` podem ser usados diretamente no `dark_window.py` ou se exigem adaptador minimo.
