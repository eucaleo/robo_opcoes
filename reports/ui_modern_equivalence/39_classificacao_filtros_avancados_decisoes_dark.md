# Frente 39 - Classificacao tecnica dos filtros avancados de decisoes no modo dark

## 1. Objetivo

Classificar tecnicamente os filtros avancados de decisoes antes de qualquer patch funcional no modo dark.

Esta frente deriva do inventario aberto em:

- reports/ui_modern_equivalence/38_inventario_filtros_avancados_decisoes_dark.md

## 2. Arquivos inspecionados

- UI\components\decisions_dark_panel.py
- UI\modern\dark_window.py
- UI\modern\main_window.py
- UI\components\filters_panel.py
- UI\components\decisions_grid.py
- UI\components\details_panel.py

## 3. Resumo por arquivo

### 3.x. UI\components\decisions_dark_panel.py

Status: arquivo encontrado com 827 linhas.

Classes e metodos localizados:

- Linha 25: class DecisionsDarkPanel(ctk.CTkFrame):
- Linha 30: def __init__(
- Linha 55: def _status(self, message: str) -> None:
- Linha 59: def _build_layout(self) -> None:
- Linha 170: def reload_decisions(self) -> None:
- Linha 212: def _render_rows(self) -> None:
- Linha 255: def _on_search_changed(self, _event=None) -> None:
- Linha 258: def _clear_search(self) -> None:
- Linha 262: def _refresh_structure_index(self) -> None:
- Linha 303: def _is_active_structure(self, structure: Dict[str, Any]) -> bool:
- Linha 350: def _apply_filter(self, render: bool = True) -> None:
- Linha 389: def _decision_matches_filter(self, decision: Dict[str, Any], terms: List[str]) -> bool:
- Linha 393: def _decision_structure_id(self, decision: Dict[str, Any]) -> str:
- Linha 399: def _decision_search_blob(self, decision: Dict[str, Any]) -> str:
- Linha 429: def _load_selected_structure(self) -> None:
- Linha 451: def _select_decision(self, index: int) -> None:
- Linha 483: def _copy_selected_detail(self) -> None:
- Linha 497: def _export_filtered_csv(self) -> None:
- Linha 560: def _decision_export_row(self, decision: Dict[str, Any], index: int) -> Dict[str, Any]:
- Linha 585: def _csv_value(self, value: Any) -> str:
- Linha 594: def _structure_name(self, structure_id: Any) -> str:
- Linha 615: def _format_row(self, decision: Dict[str, Any], index: int) -> str:
- Linha 630: def _structure_display_name(self, structure_id: Any) -> str:
- Linha 651: def _structure_status_label(self, structure_id: Any) -> str:
- Linha 664: def _format_money_value(self, value: Any) -> str:
- Linha 676: def _format_percent_value(self, value: Any) -> str:
- Linha 688: def _format_number_value(self, value: Any) -> str:
- Linha 700: def _detail_value(self, decision: Dict[str, Any], *keys: str) -> Any:
- Linha 707: def _format_detail_header(self, decision: Dict[str, Any]) -> str:
- Linha 747: def _format_detail(self, decision: Dict[str, Any]) -> str:
- Linha 805: def _format_json_like(self, value: Any) -> str:
- Linha 819: def _set_detail_text(self, text: str) -> None:

Chaves/campos acessados por get ou indice textual:

- 1.0
- aba
- created_at
- decision
- dte_min
- id
- level
- pl_atual
- pl_max
- pl_pct_of_max
- rationale
- situacao
- situação
- spot_ref
- spot_reference
- state
- status
- structure_id
- timestamp
- why
- why_json

Ocorrencias relevantes:

- Linha 1: # UI/components/decisions_dark_panel.py
- Linha 3: Painel DARK minimo para listagem global de decisoes.
- Linha 6: - usa UIDataModel.get_decisions();
- Linha 7: - lista decisoes em CustomTkinter;
- Linha 14: from __future__ import annotations
- Linha 16: import csv
- Linha 18: from datetime import datetime
- Linha 19: from typing import Any, Callable, Dict, List, Optional
- Linha 20: from tkinter import filedialog, messagebox
- Linha 22: import customtkinter as ctk
- Linha 25: class DecisionsDarkPanel(ctk.CTkFrame):
- Linha 27: Listagem global minima de decisoes para o modo dark.
- Linha 33: data_model,
- Linha 35: on_load_structure: Optional[Callable[[Any], None]] = None,
- Linha 36: get_structures: Optional[Callable[[], List[Dict[str, Any]]]] = None,
- Linha 40: self.data_model = data_model
- Linha 42: self.on_load_structure = on_load_structure
- Linha 43: self.get_structures = get_structures
- Linha 44: self.decisions: List[Dict[str, Any]] = []
- Linha 45: self.filtered_decisions: List[Dict[str, Any]] = []
- Linha 46: self.structure_index: Dict[str, Dict[str, Any]] = {}
- Linha 47: self.active_structure_ids: set[str] = set()
- Linha 49: self._row_buttons: List[ctk.CTkButton] = []
- Linha 53: self.after(100, self.reload_decisions)
- Linha 73: text="Decisões globais",
- Linha 79: self.load_structure_btn = ctk.CTkButton(
- Linha 81: text="Carregar estrutura no Terminal",
- Linha 84: command=self._load_selected_structure,
- Linha 86: self.load_structure_btn.grid(row=0, column=1, sticky="e", padx=(8, 4), pady=10)
- Linha 88: export_csv_btn = ctk.CTkButton(
- Linha 90: text="Exportar CSV",
- Linha 94: command=self._export_filtered_csv,
- Linha 96: export_csv_btn.grid(row=0, column=2, sticky="e", padx=(4, 4), pady=10)
- Linha 98: refresh_btn = ctk.CTkButton(
- Linha 102: command=self.reload_decisions,
- Linha 106: self.search_entry = ctk.CTkEntry(
- Linha 108: placeholder_text="Buscar por ID ou nome da estrutura ativa...",
- Linha 111: self.search_entry.grid(row=1, column=0, columnspan=3, sticky="ew", padx=(12, 4), pady=(0, 10))
- Linha 112: self.search_entry.bind("<KeyRelease>", self._on_search_changed)
- Linha 114: clear_search_btn = ctk.CTkButton(
- Linha 116: text="Limpar",
- Linha 121: command=self._clear_search,
- Linha 123: clear_search_btn.grid(row=1, column=3, sticky="e", padx=(4, 12), pady=(0, 10))
- Linha 141: text="Detalhe da decisão selecionada",
- Linha 147: self.copy_detail_btn = ctk.CTkButton(
- Linha 168: self._set_detail_text("Nenhuma decisão selecionada.")
- Linha 170: def reload_decisions(self) -> None:
- Linha 172: if hasattr(self.data_model, "refresh"):
- Linha 173: self.data_model.refresh()
- Linha 175: decisions = self.data_model.get_decisions()
- Linha 176: self.decisions = list(decisions or [])
- Linha 178: self._refresh_structure_index()
- Linha 179: self._apply_filter(render=False)
- Linha 183: if self.filtered_decisions:
- Linha 184: self._select_decision(0)
- Linha 185: if len(self.filtered_decisions) == len(self.decisions):
- Linha 186: self._status(f"{len(self.decisions)} decisões carregadas no modo dark")
- Linha 189: f"{len(self.filtered_decisions)} de {len(self.decisions)} decisões exibidas"
- Linha 191: elif self.decisions:
- Linha 192: self.load_structure_btn.configure(state="disabled")
- Linha 193: self._set_detail_text("Nenhuma decisão encontrada para o filtro atual.")
- Linha 195: f"Filtro sem resultados: 0 de {len(self.decisions)} decisões exibidas"
- Linha 198: self.load_structure_btn.configure(state="disabled")
- Linha 199: self._set_detail_text("Nenhuma decisão encontrada.")
- Linha 200: self._status("Nenhuma decisão encontrada no modo dark")
- Linha 203: self.decisions = []
- Linha 204: self.filtered_decisions = []
- Linha 205: self.structure_index = {}
- Linha 206: self.active_structure_ids = set()
- Linha 209: self._set_detail_text(f"Erro ao carregar decisões:\n\n{exc}")
- Linha 210: self._status(f"Erro ao carregar decisões: {exc}")
- Linha 216: self._row_buttons = []
- Linha 218: if not self.filtered_decisions:
- Linha 219: empty_text = "Nenhuma decisão disponível."
- Linha 220: if self.decisions:
- Linha 221: empty_text = "Nenhuma decisão encontrada para o filtro atual."
- Linha 231: visible = self.filtered_decisions[:300]
- Linha 233: for index, decision in enumerate(visible):
- Linha 234: btn = ctk.CTkButton(
- Linha 236: text=self._format_row(decision, index),
- Linha 242: command=lambda i=index: self._select_decision(i),
- Linha 245: self._row_buttons.append(btn)
- Linha 247: if len(self.filtered_decisions) > len(visible):
- Linha 250: text=f"Exibindo 300 de {len(self.filtered_decisions)} decisões filtradas.",
- Linha 255: def _on_search_changed(self, _event=None) -> None:
- Linha 256: self._apply_filter(render=True)
- Linha 258: def _clear_search(self) -> None:
- Linha 259: self.search_entry.delete(0, "end")
- Linha 260: self._apply_filter(render=True)
- Linha 262: def _refresh_structure_index(self) -> None:
- Linha 264: Monta indice local de estruturas para:
- Linha 265: - filtrar somente decisoes de estruturas ativas;
- Linha 266: - permitir busca por ID ou nome da estrutura.
- Linha 268: structures: List[Dict[str, Any]] = []
- Linha 270: if self.get_structures:
- Linha 272: structures = list(self.get_structures() or [])
- Linha 274: self._status(f"Erro ao carregar estruturas para filtro de decisões: {exc}")
- Linha 275: structures = []
- Linha 277: self.structure_index = {}
- Linha 278: self.active_structure_ids = set()
- Linha 280: for structure in structures:
- Linha 281: structure_id = structure.get("id")
- Linha 282: if structure_id is None:
- Linha 283: structure_id = structure.get("structure_id") or structure.get("aba")
- Linha 285: if structure_id is None:
- Linha 288: key = str(structure_id)
- Linha 289: self.structure_index[key] = structure
- Linha 291: if self._is_active_structure(structure):
- Linha 292: self.active_structure_ids.add(key)
- Linha 294: # Fallback seguro: se nao houver informacao de estruturas, nao bloqueia a lista.
- Linha 295: if not structures:
- Linha 297: str(decision.get("structure_id") or decision.get("aba"))
- Linha 298: for decision in self.decisions
- Linha 299: if decision.get("structure_id") is not None or decision.get("aba") is not None
- Linha 301: self.active_structure_ids = ids
- Linha 303: def _is_active_structure(self, structure: Dict[str, Any]) -> bool:
- Linha 305: Heuristica defensiva para identificar estrutura ativa sem depender
- Linha 309: if key in structure:
- Linha 310: value = structure.get(key)
- Linha 316: structure.get("status")
- Demais ocorrencias omitidas no resumo: 199

### 3.x. UI\modern\dark_window.py

Status: arquivo encontrado com 201 linhas.

Classes e metodos localizados:

- Linha 29: class ModernDarkWindow:
- Linha 34: def __init__(self) -> None:
- Linha 49: def _build_menu(self) -> None:
- Linha 65: def _build_layout(self) -> None:
- Linha 95: def set_status(self, message: str) -> None:
- Linha 99: def _reload_panel(self) -> None:
- Linha 120: def _get_structures_for_decisions(self):
- Linha 136: def _load_structure_from_decision(self, structure_id) -> None:
- Linha 183: def _show_about(self) -> None:
- Linha 191: def run(self) -> None:
- Linha 195: def main() -> None:

Chaves/campos acessados por get ou indice textual:

- id

Ocorrencias relevantes:

- Linha 10: from __future__ import annotations
- Linha 13: from pathlib import Path
- Linha 14: from tkinter import messagebox
- Linha 16: import customtkinter as ctk
- Linha 18: from UI.modern.theme import CUSTOMTKINTER_APPEARANCE_MODE, CUSTOMTKINTER_COLOR_THEME
- Linha 20: from UI.components.terminal_vwap_payoff_dark_panel import TerminalVWAPPayoffDarkPanel
- Linha 21: from UI.components.decisions_dark_panel import DecisionsDarkPanel
- Linha 22: from UI.models.ui_data import UIDataModel
- Linha 31: Janela desktop paralela baseada no painel DARK existente.
- Linha 35: ctk.set_appearance_mode(CUSTOMTKINTER_APPEARANCE_MODE)
- Linha 36: ctk.set_default_color_theme(CUSTOMTKINTER_COLOR_THEME)
- Linha 44: self.data_model = UIDataModel()
- Linha 54: app_menu.add_separator()
- Linha 77: decisions_tab = self.tabs.add("Decisões")
- Linha 86: self.decisions_panel = DecisionsDarkPanel(
- Linha 87: parent=decisions_tab,
- Linha 88: data_model=self.data_model,
- Linha 90: on_load_structure=self._load_structure_from_decision,
- Linha 91: get_structures=self._get_structures_for_decisions,
- Linha 93: self.decisions_panel.pack(fill="both", expand=True)
- Linha 103: if hasattr(self.panel, "reload_structures"):
- Linha 104: self.panel.reload_structures()
- Linha 107: if hasattr(self, "decisions_panel") and hasattr(self.decisions_panel, "reload_decisions"):
- Linha 108: self.decisions_panel.reload_decisions()
- Linha 120: def _get_structures_for_decisions(self):
- Linha 122: Fornece as estruturas carregadas no Terminal VWAP para a aba Decisões.
- Linha 123: Usado para restringir a busca a ID/nome e somente estruturas ativas.
- Linha 125: structures = getattr(self.panel, "structures", None)
- Linha 127: if structures is None:
- Linha 128: structures = []
- Linha 130: if not structures and hasattr(self.panel, "reload_structures"):
- Linha 131: self.panel.reload_structures()
- Linha 132: structures = getattr(self.panel, "structures", []) or []
- Linha 134: return list(structures or [])
- Linha 136: def _load_structure_from_decision(self, structure_id) -> None:
- Linha 138: Carrega no Terminal VWAP a estrutura associada a uma decisão selecionada.
- Linha 141: target = str(structure_id)
- Linha 143: structures = getattr(self.panel, "structures", None)
- Linha 144: if structures is None:
- Linha 145: structures = []
- Linha 147: if not structures and hasattr(self.panel, "reload_structures"):
- Linha 148: self.panel.reload_structures()
- Linha 149: structures = getattr(self.panel, "structures", []) or []
- Linha 152: for structure in structures:
- Linha 153: if str(structure.get("id")) == target:
- Linha 154: selected = structure
- Linha 158: self.set_status(f"Estrutura {structure_id} não encontrada no Terminal VWAP")
- Linha 160: "Estrutura não encontrada",
- Linha 161: f"Estrutura {structure_id} não foi encontrada na lista do Terminal VWAP.",
- Linha 166: self.panel.select_structure(selected)
- Linha 173: self.set_status(f"Estrutura {structure_id} carregada a partir da decisão")
- Linha 176: self.set_status(f"Erro ao carregar estrutura da decisão: {exc}")
- Linha 178: "Erro ao carregar estrutura",

### 3.x. UI\modern\main_window.py

Status: arquivo encontrado com 776 linhas.

Classes e metodos localizados:

- Linha 33: class ModernMainWindow:
- Linha 44: def __init__(self):
- Linha 70: def _setup_style(self) -> None:
- Linha 107: def _setup_layout(self) -> None:
- Linha 130: def _build_header(self, parent: tk.Widget) -> None:
- Linha 148: def _build_sidebar(self, parent: tk.Widget) -> None:
- Linha 178: def _side_button(self, parent: tk.Widget, text: str, command) -> None:
- Linha 182: def _build_workspace(self, parent: tk.Widget) -> None:
- Linha 193: def _build_analysis_tab(self, notebook: ttk.Notebook) -> None:
- Linha 237: def _build_structures_tab(self, notebook: ttk.Notebook) -> None:
- Linha 267: def _build_terminal_tab(self, notebook: ttk.Notebook) -> None:
- Linha 310: def _bind_events(self) -> None:
- Linha 318: def set_status(self, message: str) -> None:
- Linha 325: def on_filter_change(self, filters: Dict) -> None:
- Linha 336: def on_decision_selected(self, decision_data: Dict) -> None:
- Linha 356: def _start_payoff_load(
- Linha 370: def worker() -> None:
- Linha 430: def _finish_payoff_load(
- Linha 477: def _handle_payoff_error(self, error_msg: str, worker_id: int) -> None:
- Linha 491: def refresh_data(self) -> None:
- Linha 557: def export_csv(self) -> None:
- Linha 575: def run_pipeline(self) -> None:
- Linha 625: def recalculate_structure(self, structure_id: str) -> None:
- Linha 639: def finish(ok: bool, msg: str) -> None:
- Linha 653: def worker() -> None:
- Linha 693: def check_databases(self) -> None:
- Linha 702: def clear_cache(self) -> None:
- Linha 711: def _on_structure_selected(self, structure: Optional[Dict]) -> None:
- Linha 749: def _on_structure_edit_request(self, structure_id: Optional[int]) -> None:
- Linha 766: def run(self) -> None:
- Linha 770: def main() -> None:

Chaves/campos acessados por get ou indice textual:

- alias_legacy_aba
- breakevens
- count_points
- created_at
- expiration_date
- id
- legs
- multiplier
- name
- notes
- option_type
- p
- pl
- pl_at_spot_ref
- point_pl
- point_spot
- position_side
- premium
- quantity
- s
- source_table
- spot
- status
- strike
- structure_id
- symbol
- timestamp
- underlying_asset
- updated_at
- used_timestamp
- x
- y

Ocorrencias relevantes:

- Linha 3: Novo shell desktop paralelo da UI.
- Linha 10: from __future__ import annotations
- Linha 16: from pathlib import Path
- Linha 17: from tkinter import filedialog, messagebox, ttk
- Linha 18: from typing import Dict, List, Optional
- Linha 20: from UI.components.decisions_grid import DecisionsGrid
- Linha 21: from UI.components.details_panel import DetailsPanel
- Linha 22: from UI.components.filters_panel import FiltersPanel
- Linha 23: from UI.components.payoff_chart import PayoffChart
- Linha 24: from UI.components.structure_editor_dialog import StructureEditorDialog
- Linha 25: from UI.components.structures_list_panel import StructuresListPanel
- Linha 26: from UI.models.ui_data import UIDataModel
- Linha 27: from UI.debug_utils import debug
- Linha 35: Shell desktop novo, em paralelo à MainWindow legado.
- Linha 46: self.root.title("Sistema de Derivados - Novo Layout Desktop")
- Linha 50: self.data_model = UIDataModel()
- Linha 56: self.last_selected_decision: Optional[Dict] = None
- Linha 64: self.refresh_data()
- Linha 128: status.pack(side="bottom", fill="x")
- Linha 143: text="Novo layout desktop paralelo · UI antiga preservada",
- Linha 159: self._side_button(sidebar, "Atualizar dados", self.refresh_data)
- Linha 160: self._side_button(sidebar, "Exportar CSV", self.export_csv)
- Linha 161: self._side_button(sidebar, "Executar pipeline", self.run_pipeline)
- Linha 162: self._side_button(sidebar, "Verificar bancos", self.check_databases)
- Linha 163: self._side_button(sidebar, "Limpar cache", self.clear_cache)
- Linha 165: ttk.Separator(sidebar).pack(fill="x", pady=14)
- Linha 176: self._side_button(sidebar, "Sair", self.root.quit)
- Linha 178: def _side_button(self, parent: tk.Widget, text: str, command) -> None:
- Linha 179: btn = ttk.Button(parent, text=text, command=command)
- Linha 190: self._build_structures_tab(self.main_notebook)
- Linha 206: self.filters_panel = FiltersPanel(
- Linha 208: on_filter_change=self.on_filter_change,
- Linha 210: self.filters_panel.pack(fill="x", padx=4, pady=(0, 6))
- Linha 212: self.decisions_grid = DecisionsGrid(
- Linha 214: on_selection_change=self.on_decision_selected,
- Linha 216: self.decisions_grid.pack(fill="both", expand=True, padx=4, pady=4)
- Linha 222: detail_notebook.add(details_frame, text="Detalhes da decisão")
- Linha 226: on_recalculate=self.recalculate_structure,
- Linha 237: def _build_structures_tab(self, notebook: ttk.Notebook) -> None:
- Linha 239: notebook.add(tab, text="Estruturas")
- Linha 250: self.structures_list = StructuresListPanel(
- Linha 252: on_structure_selected=self._on_structure_selected,
- Linha 253: on_request_edit=self._on_structure_edit_request,
- Linha 256: self.structures_list.pack(fill="both", expand=True)
- Linha 272: from controllers.terminal_vwap_payoff_controller import (
- Linha 275: from repositories.structures_repository import StructuresRepository
- Linha 276: from services.terminal_vwap_payoff_app_service import (
- Linha 279: from UI.components.terminal_vwap_payoff_panel import TerminalVWAPPayoffPanel
- Linha 281: repository = StructuresRepository(self._db_path)
- Linha 283: structure_repository=repository,
- Linha 311: self.root.bind("<F5>", lambda _e: self.refresh_data())
- Linha 322: # Decisões / filtros / payoff
- Linha 325: def on_filter_change(self, filters: Dict) -> None:
- Linha 326: self.set_status("Aplicando filtros...")
- Linha 329: filtered_data = self.data_model.get_decisions(filters)
- Linha 330: self.decisions_grid.update_data(filtered_data)
- Linha 331: self.set_status(f"{len(filtered_data)} decisões encontradas")
- Linha 333: messagebox.showerror("Erro", f"Erro ao aplicar filtros: {exc}")
- Linha 334: self.set_status("Erro nos filtros")
- Linha 336: def on_decision_selected(self, decision_data: Dict) -> None:
- Linha 337: if not decision_data:
- Linha 340: self.last_selected_decision = dict(decision_data)
- Linha 343: self.details_panel.update_decision(decision_data)
- Linha 347: structure_id = decision_data.get("structure_id")
- Linha 348: timestamp = decision_data.get("timestamp")
- Linha 350: if structure_id is not None:
- Linha 351: self._start_payoff_load(structure_id, timestamp, decision_data)
- Linha 353: self.payoff_chart.clear()
- Linha 358: structure_id,
- Linha 359: timestamp=None,
- Linha 360: decision_data=None,
- Linha 362: if decision_data is None:
- Linha 363: decision_data = {"structure_id": structure_id}
- Linha 372: points, info_dict = self.data_model.get_payoff_curve_info(
- Linha 373: structure_id,
- Linha 374: timestamp,
- Linha 379: f"[ModernUI] payoff structure_id={structure_id} "
- Linha 380: f"timestamp={timestamp} n={len(points or [])}"
- Linha 415: decision_data,
- Linha 434: decision_data: Dict,
- Linha 444: overlays = self.payoff_chart.update_chart(points, decision_data)
- Linha 447: self.details_panel.update_breakevens(
- Linha 455: self.details_panel.update_audit_info(info_dict or {})
- Linha 459: used_ts = (info_dict or {}).get("used_timestamp") or decision_data.get(
- Linha 460: "timestamp"
- Linha 465: msg = f"{count} pontos carregados ({source})"
- Linha 466: if used_ts and used_ts != decision_data.get("timestamp"):
- Linha 471: self.payoff_chart.clear()
- Linha 484: self.payoff_chart.clear()
- Linha 491: def refresh_data(self) -> None:
- Linha 495: self.data_model.refresh()
- Linha 498: self.filters_panel.update_structures(
- Linha 499: self.data_model.get_structures()
- Linha 505: self.filters_panel.reset_filters()
- Linha 509: decisions = self.data_model.get_decisions()
- Linha 510: self.decisions_grid.update_data(decisions)
- Linha 513: previous = self.last_selected_decision
- Linha 516: structure_id = previous.get("structure_id")
- Linha 517: timestamp = previous.get("timestamp")
- Linha 519: if structure_id is not None:
- Linha 521: self.decisions_grid.select_by_key(structure_id, timestamp)
- Linha 526: self.details_panel.update_decision(previous)
- Linha 531: self._start_payoff_load(structure_id, timestamp, previous)
- Linha 538: self.details_panel.clear()
- Linha 543: self.payoff_chart.clear()
- Linha 547: self.set_status(f"Dados atualizados - {len(decisions)} decisões")
- Linha 557: def export_csv(self) -> None:
- Linha 559: defaultextension=".csv",
- Linha 560: filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
- Linha 567: current_data = self.decisions_grid.get_current_data()
- Linha 568: self.data_model.export_to_csv(current_data, filename)
- Linha 570: self.set_status(f"CSV exportado: {filename}")
- Linha 573: self.set_status("Erro ao exportar CSV")
- Linha 610: self.refresh_data()
- Linha 625: def recalculate_structure(self, structure_id: str) -> None:
- Linha 627: self.set_status(f"Recálculo já em andamento; ignorando {structure_id}")
- Linha 637: self.set_status(f"Recalculando {structure_id}...")
- Linha 646: structure_id,
- Linha 673: self.root.after(0, self.refresh_data)
- Linha 676: lambda: finish(True, f"OK: {structure_id} recalculado"),
- Demais ocorrencias omitidas no resumo: 23

### 3.x. UI\components\filters_panel.py

Status: arquivo encontrado com 158 linhas.

Classes e metodos localizados:

- Linha 7: class FiltersPanel(ttk.LabelFrame):
- Linha 8: def __init__(self, parent, on_filter_change: Callable[[Dict], None]):
- Linha 15: def _setup_widgets(self):
- Linha 96: def _bind_events(self):
- Linha 103: def _apply_filters(self):
- Linha 137: def reset_filters(self):
- Linha 151: def update_structures(self, structures: List[str]):

Chaves/campos acessados por get ou indice textual:

- date_from
- date_to
- decision
- dte_max
- level_min
- structure_id

Ocorrencias relevantes:

- Linha 1: # UI/components/filters_panel.py
- Linha 3: from tkinter import ttk
- Linha 4: from typing import Dict, List, Optional, Callable
- Linha 5: from datetime import datetime, timedelta
- Linha 7: class FiltersPanel(ttk.LabelFrame):
- Linha 8: def __init__(self, parent, on_filter_change: Callable[[Dict], None]):
- Linha 9: super().__init__(parent, text="Filtros", padding=10)
- Linha 11: self.on_filter_change = on_filter_change
- Linha 22: self.date_from_var = tk.StringVar()
- Linha 23: self.date_to_var = tk.StringVar()
- Linha 26: today = datetime.now()
- Linha 27: month_ago = today - timedelta(days=30)
- Linha 28: self.date_from_var.set(month_ago.strftime("%Y-%m-%d"))
- Linha 29: self.date_to_var.set(today.strftime("%Y-%m-%d"))
- Linha 32: self.date_from_entry = ttk.Entry(row1, textvariable=self.date_from_var, width=12)
- Linha 33: self.date_from_entry.pack(side="left")
- Linha 36: self.date_to_entry = ttk.Entry(row1, textvariable=self.date_to_var, width=12)
- Linha 37: self.date_to_entry.pack(side="left")
- Linha 39: # Linha 2: Estrutura e Decisão
- Linha 43: ttk.Label(row2, text="Estrutura:", width=10).pack(side="left")
- Linha 44: self.structure_var = tk.StringVar()
- Linha 45: self.structure_combo = ttk.Combobox(
- Linha 47: textvariable=self.structure_var,
- Linha 51: self.structure_combo.pack(side="left", padx=(0, 10))
- Linha 53: ttk.Label(row2, text="Decisão:").pack(side="left")
- Linha 54: self.decision_var = tk.StringVar()
- Linha 55: self.decision_combo = ttk.Combobox(
- Linha 57: textvariable=self.decision_var,
- Linha 62: self.decision_combo.pack(side="left", padx=(5, 0))
- Linha 64: # Linha 3: Level e DTE
- Linha 68: ttk.Label(row3, text="Level >=:", width=10).pack(side="left")
- Linha 69: self.level_var = tk.StringVar()
- Linha 70: self.level_entry = ttk.Entry(row3, textvariable=self.level_var, width=5)
- Linha 71: self.level_entry.pack(side="left", padx=(0, 10))
- Linha 73: ttk.Label(row3, text="DTE <=:").pack(side="left")
- Linha 74: self.dte_var = tk.StringVar()
- Linha 75: self.dte_entry = ttk.Entry(row3, textvariable=self.dte_var, width=5)
- Linha 76: self.dte_entry.pack(side="left", padx=(5, 10))
- Linha 82: self.apply_btn = ttk.Button(
- Linha 83: btn_frame, text="Aplicar", command=self._apply_filters
- Linha 85: self.apply_btn.pack(side="left", padx=(0, 5))
- Linha 87: self.reset_btn = ttk.Button(
- Linha 88: btn_frame, text="Limpar", command=self.reset_filters
- Linha 93: self.status_label = ttk.Label(self, text="Filtros prontos", foreground="green")
- Linha 97: for w in [self.date_from_entry, self.date_to_entry, self.level_entry, self.dte_entry]:
- Linha 98: w.bind("<Return>", lambda e: self._apply_filters())
- Linha 100: self.structure_combo.bind("<<ComboboxSelected>>", lambda e: self._apply_filters())
- Linha 101: self.decision_combo.bind("<<ComboboxSelected>>", lambda e: self._apply_filters())
- Linha 103: def _apply_filters(self):
- Linha 104: filters: Dict = {}
- Linha 106: if self.date_from_var.get().strip():
- Linha 107: filters["date_from"] = self.date_from_var.get().strip()
- Linha 109: if self.date_to_var.get().strip():
- Linha 110: filters["date_to"] = self.date_to_var.get().strip()
- Linha 112: if self.structure_var.get().strip():
- Linha 113: # Envia como "structure_id"; ui_data aceita os dois
- Linha 114: filters["structure_id"] = self.structure_var.get().strip()
- Linha 116: if self.decision_var.get().strip():
- Linha 117: filters["decision"] = self.decision_var.get().strip()
- Linha 119: if self.level_var.get().strip():
- Linha 121: filters["level_min"] = int(self.level_var.get().strip())
- Linha 125: if self.dte_var.get().strip():
- Linha 127: filters["dte_max"] = int(self.dte_var.get().strip())
- Linha 132: text=f"Filtros aplicados ({len(filters)} ativos)",
- Linha 135: self.on_filter_change(filters)
- Linha 137: def reset_filters(self):
- Linha 138: self.structure_var.set("")
- Linha 139: self.decision_var.set("")
- Linha 140: self.level_var.set("")
- Linha 141: self.dte_var.set("")
- Linha 143: today = datetime.now()
- Linha 144: month_ago = today - timedelta(days=30)
- Linha 145: self.date_from_var.set(month_ago.strftime("%Y-%m-%d"))
- Linha 146: self.date_to_var.set(today.strftime("%Y-%m-%d"))
- Linha 148: self.status_label.config(text="Filtros limpos", foreground="green")
- Linha 149: self._apply_filters()
- Linha 151: def update_structures(self, structures: List[str]):
- Linha 152: """Atualiza lista de estruturas no combo (novo método)."""
- Linha 153: current = self.structure_var.get()
- Linha 154: values = [""] + sorted(structures)
- Linha 155: self.structure_combo.config(values=values)
- Linha 157: self.structure_var.set("")

### 3.x. UI\components\decisions_grid.py

Status: arquivo encontrado com 215 linhas.

Classes e metodos localizados:

- Linha 9: class DecisionsGrid(ttk.LabelFrame):
- Linha 10: def __init__(
- Linha 23: def _setup_treeview(self):
- Linha 72: def _setup_scrollbars(self):
- Linha 86: def _on_tree_select(self, event):
- Linha 100: def update_data(self, decisions: List[Dict]):
- Linha 143: def _format_timestamp(self, timestamp_str: Optional[str]) -> str:
- Linha 158: def _format_ratio(self, ratio: Optional[float]) -> str:
- Linha 166: def _format_currency(self, value: Optional[float]) -> str:
- Linha 177: def get_current_data(self) -> List[Dict]:
- Linha 181: def get_selected_decision(self) -> Optional[Dict]:
- Linha 194: def select_by_key(self, structure_id: str, timestamp: str) -> bool:

Chaves/campos acessados por get ou indice textual:

- aba
- decision
- dte_min
- level
- pl_atual
- pl_max
- pl_pct_of_max
- structure_id
- timestamp

Ocorrencias relevantes:

- Linha 1: # UI/components/decisions_grid.py
- Linha 2: from src.domain.refs.structure_ref import StructureRef
- Linha 4: from tkinter import ttk
- Linha 5: from typing import Dict, List, Optional, Callable
- Linha 9: class DecisionsGrid(ttk.LabelFrame):
- Linha 15: super().__init__(parent, text="Decisões", padding=5)
- Linha 18: self.current_data: List[Dict] = []
- Linha 25: "timestamp",
- Linha 26: "structure_id",
- Linha 27: "decision",
- Linha 28: "level",
- Linha 30: "dte",
- Linha 43: self.tree.heading("timestamp", text="Data/Hora")
- Linha 44: self.tree.heading("structure_id", text="Estrutura")
- Linha 45: self.tree.heading("decision", text="Decisão")
- Linha 46: self.tree.heading("level", text="Nível")
- Linha 48: self.tree.heading("dte", text="DTE")
- Linha 53: self.tree.column("timestamp", width=140, anchor="center")
- Linha 54: self.tree.column("structure_id", width=100, anchor="center")
- Linha 55: self.tree.column("decision", width=100, anchor="center")
- Linha 56: self.tree.column("level", width=50, anchor="center")
- Linha 58: self.tree.column("dte", width=50, anchor="center")
- Linha 62: # Evento de seleção
- Linha 65: # Tags de cor por decisão
- Linha 95: if 0 <= index < len(self.current_data):
- Linha 96: self.on_selection_change(self.current_data[index])
- Linha 100: def update_data(self, decisions: List[Dict]):
- Linha 101: """Atualiza grid com nova lista de decisões."""
- Linha 102: self.current_data = decisions.copy()
- Linha 107: for i, decision in enumerate(decisions, 1):
- Linha 108: timestamp = self._format_timestamp(decision.get("timestamp"))
- Linha 109: # Exibe structure_id; fallback para aba (compat)
- Linha 110: structure_id = (
- Linha 111: decision.get("structure_id") or decision.get("aba") or "N/A"
- Linha 113: decision_text = decision.get("decision", "N/A")
- Linha 114: level = decision.get("level", "")
- Linha 115: ratio = self._format_ratio(decision.get("pl_pct_of_max"))
- Linha 116: dte = decision.get("dte_min", "")
- Linha 117: pl_atual = self._format_currency(decision.get("pl_atual"))
- Linha 118: pl_max = self._format_currency(decision.get("pl_max"))
- Linha 121: decision_text
- Linha 122: if decision_text in ["HOLD", "PREPARE_ROLL", "CLOSE_REOPEN", "ROLL", "ENTER"]
- Linha 131: timestamp,
- Linha 132: structure_id,
- Linha 133: decision_text,
- Linha 134: level,
- Linha 136: dte,
- Linha 143: def _format_timestamp(self, timestamp_str: Optional[str]) -> str:
- Linha 144: if not timestamp_str:
- Linha 149: from datetime import datetime
- Linha 150: dt = datetime.strptime(timestamp_str, fmt)
- Linha 154: return timestamp_str[:16] if len(timestamp_str) > 16 else timestamp_str
- Linha 177: def get_current_data(self) -> List[Dict]:
- Linha 178: """Retorna dados atualmente exibidos (para export)."""
- Linha 179: return self.current_data.copy()
- Linha 181: def get_selected_decision(self) -> Optional[Dict]:
- Linha 182: """Retorna decisão atualmente selecionada."""
- Linha 188: if 0 <= index < len(self.current_data):
- Linha 189: return self.current_data[index]
- Linha 194: def select_by_key(self, structure_id: str, timestamp: str) -> bool:
- Linha 196: Seleciona a linha cujo (structure_id, timestamp) bate no dataset.
- Linha 197: Aceita tanto 'structure_id' quanto 'aba' nos dicts (compat).
- Linha 198: Retorna True se encontrou.
- Linha 200: if not structure_id or not timestamp:
- Linha 203: for idx, row in enumerate(self.current_data):
- Linha 204: row_sid = row.get("structure_id") or row.get("aba")
- Linha 205: if row_sid == structure_id and row.get("timestamp") == timestamp:

### 3.x. UI\components\details_panel.py

Status: arquivo encontrado com 1098 linhas.

Classes e metodos localizados:

- Linha 10: class DetailsPanel(ttk.LabelFrame):
- Linha 11: def __init__(self, parent, on_recalculate=None, app_db_path=None):
- Linha 30: def _set_recalc_ui_state(self, in_progress: bool, msg: str = "", color: str = "gray"):
- Linha 50: def _derived_db_path(self) -> Path:
- Linha 72: def _operational_app_db_path(self) -> Path:
- Linha 90: def _resolve_structure_key(self, structure_id) -> int:
- Linha 107: def _get_latest_snapshot_timestamp_for_structure(self, structure_id):
- Linha 122: def _safe_path(value):
- Linha 137: def _looks_like_db_path(name, path):
- Linha 279: def q(identifier):
- Linha 282: def table_names(cur):
- Linha 293: def columns_for(cur, table):
- Linha 297: def looks_like_structure_col(col):
- Linha 308: def timestamp_score(col):
- Linha 345: def latest_in_table(cur, table):
- Linha 443: def _compute_recalc_signature(self, structure_id):
- Linha 453: def _setup_widgets(self):
- Linha 641: def update_decision(self, decision_data: Dict):
- Linha 696: def update_breakevens(self, breakevens, pl_at_spot_ref):
- Linha 707: def update_audit_info(self, info: Dict):
- Linha 719: def clear(self):
- Linha 734: def on_recalc_finished(self, structure_id, ok: bool, message: str = ""):
- Linha 755: def _clear_operational_state(self):
- Linha 765: def update_operational_state(self, effective_structure: Dict[str, Any]):
- Linha 817: def _fetch_effective_structure_local(self, structure_id) -> Optional[Dict[str, Any]]:
- Linha 854: def _refresh_operational_state_for_structure(self, structure_id):
- Linha 865: def _format_currency_label(self, label: ttk.Label, value):
- Linha 878: def _fetch_latest_decision_from_derived(
- Linha 920: def _fetch_payoff_points_from_derived(self, structure_id):
- Linha 948: def _fetch_audit_info_from_derived(self, structure_id) -> Dict[str, Any]:
- Linha 988: def _compute_breakevens_from_points(self, pts):
- Linha 1009: def _compute_pl_at_spot(self, pts, spot_ref: Optional[float]) -> Optional[float]:
- Linha 1023: def _refresh_current_from_derived(self, structure_id):
- Linha 1046: def _on_recalculate_click(self):

Chaves/campos acessados por get ou indice textual:

- applied_events
- count_points
- created_at
- decision
- dte_min
- events_applied
- events_ignored_cancelled
- fallback
- ignored_events
- is_closed
- level
- n
- operational_state
- pl_atual
- pl_max
- pl_pct_of_max
- point_pl
- point_spot
- points_count
- source_table
- spot_ref
- spot_reference
- structure_id
- timestamp
- why
- why_json

Ocorrencias relevantes:

- Linha 3: from tkinter import ttk, scrolledtext
- Linha 4: from typing import Dict, Optional, Any
- Linha 7: from pathlib import Path
- Linha 17: self._current_decision = None
- Linha 55: - se o painel tiver db_path/_db_path explícito, usa esse arquivo;
- Linha 57: - fallback final: raiz do projeto inferida pelo arquivo atual.
- Linha 59: for attr in ("db_path", "_db_path", "database_path", "_database_path"):
- Linha 77: esse atributo como caminho do derived.db em testes/compatibilidade.
- Linha 90: def _resolve_structure_key(self, structure_id) -> int:
- Linha 92: structure_id é sempre INTEGER no DB.
- Linha 96: return int(structure_id)
- Linha 99: f"structure_id inválido: {structure_id!r}. "
- Linha 101: ) from exc
- Linha 107: def _get_latest_snapshot_timestamp_for_structure(self, structure_id):
- Linha 109: Retorna o timestamp mais recente de snapshot para uma estrutura.
- Linha 112: - se a instância recebeu um caminho explícito de DB, usa somente ele;
- Linha 113: - se esse DB explícito não existe, retorna None;
- Linha 114: - só usa fallback em bancos default quando não há DB explícito na instância.
- Linha 117: from pathlib import Path
- Linha 119: sid = self._resolve_structure_key(structure_id)
- Linha 147: or "database" in low_name
- Linha 151: candidates = []
- Linha 158: # se existe raw/app DB explícito, usa SOMENTE ele.
- Linha 169: "_database_path",
- Linha 170: "database_path",
- Linha 212: candidates = primary_explicit
- Linha 214: candidates = derived_explicit
- Linha 216: # 2) Sem DB explícito na instância: agora sim pode usar defaults.
- Linha 217: class_level_names = [
- Linha 226: "_database_path",
- Linha 227: "database_path",
- Linha 234: for name in class_level_names:
- Linha 242: candidates.append(p)
- Linha 250: candidates.extend(
- Linha 263: candidates.extend(sorted(base.glob("*.db")))
- Linha 270: for p in candidates:
- Linha 286: FROM sqlite_master
- Linha 297: def looks_like_structure_col(col):
- Linha 300: low == "structure_id"
- Linha 301: or low == "id_structure"
- Linha 302: or low == "estrutura_id"
- Linha 303: or low == "id_estrutura"
- Linha 304: or low.endswith("_structure_id")
- Linha 305: or low.endswith("_estrutura_id")
- Linha 308: def timestamp_score(col):
- Linha 312: "timestamp": 100,
- Linha 313: "snapshot_timestamp": 99,
- Linha 316: "updated_at": 96,
- Linha 318: "datetime": 94,
- Linha 319: "date": 93,
- Linha 320: "data_hora": 92,
- Linha 326: if "timestamp" in low:
- Linha 328: if "snapshot" in low and ("time" in low or "date" in low or "ts" in low):
- Linha 334: if "updated" in low:
- Linha 338: if "date" in low:
- Linha 340: if "data" in low:
- Linha 350: structure_cols = [c for c in cols if looks_like_structure_col(c)]
- Linha 352: if not structure_cols:
- Linha 355: if low in {"structure", "estrutura"}:
- Linha 356: structure_cols.append(c)
- Linha 358: if not structure_cols:
- Linha 362: [c for c in cols if timestamp_score(c) > 0],
- Linha 363: key=timestamp_score,
- Linha 368: ignored = {str(c).lower() for c in structure_cols}
- Linha 369: ignored.update(
- Linha 372: "structure_id",
- Linha 373: "id_structure",
- Linha 374: "estrutura_id",
- Linha 375: "id_estrutura",
- Linha 382: for s_col in structure_cols:
- Linha 388: FROM {q(table)}
- Linha 409: "structure_snapshots",
- Linha 410: "structure_decisions",
- Linha 443: def _compute_recalc_signature(self, structure_id):
- Linha 445: structure_id,
- Linha 446: self._get_latest_snapshot_timestamp_for_structure(structure_id),
- Linha 463: ttk.Label(basic_frame, text="Timestamp:").grid(
- Linha 466: self.timestamp_label = ttk.Label(
- Linha 469: self.timestamp_label.grid(row=0, column=1, sticky="ew", padx=(0, 10))
- Linha 471: ttk.Label(basic_frame, text="Estrutura:").grid(
- Linha 474: self.structure_label = ttk.Label(
- Linha 477: self.structure_label.grid(row=0, column=3, sticky="ew")
- Linha 479: ttk.Label(basic_frame, text="Decisão:").grid(
- Linha 482: self.decision_label = ttk.Label(
- Linha 485: self.decision_label.grid(row=1, column=1, sticky="ew", padx=(0, 10))
- Linha 490: self.level_label = ttk.Label(
- Linha 493: self.level_label.grid(row=1, column=3, sticky="ew")
- Linha 525: ttk.Label(metrics_frame, text="DTE Mín:").grid(
- Linha 528: self.dte_label = ttk.Label(
- Linha 531: self.dte_label.grid(row=1, column=3, sticky="ew")
- Linha 555: ttk.Label(operational_frame, text="Eventos aplicados:").grid(
- Linha 585: # Rationale JSON
- Linha 586: json_frame = ttk.LabelFrame(self, text="Rationale / Why JSON", padding=5)
- Linha 591: self.why_text = scrolledtext.ScrolledText(
- Linha 598: self.why_text.grid(row=0, column=0, sticky="nsew")
- Linha 600: # Auditoria & Ações
- Linha 601: audit_frame = ttk.LabelFrame(self, text="Auditoria & Ações", padding=5)
- Linha 625: self.btn_recalculate = ttk.Button(
- Linha 627: text="Recalcular esta estrutura",
- Linha 641: def update_decision(self, decision_data: Dict):
- Linha 642: self._current_decision = dict(decision_data) if decision_data else None
- Linha 644: self.timestamp_label.config(text=decision_data.get("timestamp", "N/A"))
- Linha 646: # alteracao_36: structure_id é autoritativo; aba removido
- Linha 647: structure_id = decision_data.get("structure_id") or "N/A"
- Linha 648: self.structure_label.config(text=str(structure_id))
- Linha 650: self.decision_label.config(text=decision_data.get("decision", "N/A"))
- Linha 651: self.level_label.config(text=str(decision_data.get("level", "N/A")))
- Linha 653: self._format_currency_label(self.pl_atual_label, decision_data.get("pl_atual"))
- Linha 654: self._format_currency_label(self.pl_max_label, decision_data.get("pl_max"))
- Linha 656: ratio = decision_data.get("pl_pct_of_max")
- Linha 661: self.dte_label.config(text=str(decision_data.get("dte_min", "N/A")))
- Linha 663: spot_ref = decision_data.get("spot_reference") or decision_data.get("spot_ref")
- Linha 672: why_payload = decision_data.get("why") or decision_data.get("why_json")
- Linha 673: self.why_text.delete("1.0", tk.END)
- Linha 674: if why_payload:
- Linha 676: if isinstance(why_payload, str):
- Linha 678: json.loads(why_payload), indent=2, ensure_ascii=False
- Linha 681: formatted = json.dumps(why_payload, indent=2, ensure_ascii=False)
- Linha 682: self.why_text.insert("1.0", formatted)
- Linha 684: self.why_text.insert("1.0", str(why_payload))
- Demais ocorrencias omitidas no resumo: 102

## 4. Classificacao inicial das lacunas

### 4.1. Filtros da UI atual

A UI atual auditada possui os seguintes filtros e controles:

- Periodo De/Ate
- Estrutura
- Decisao
- Level >=
- DTE <=
- Aplicar
- Limpar
- Indicador de filtros aplicados

### 4.2. Estado esperado do modo dark antes do patch

O modo dark ja possui busca textual por estrutura ativa, listagem filtrada, selecao, detalhe, copia de detalhe, exportacao CSV e carregamento da estrutura no Terminal VWAP.

Os filtros avancados ainda precisam ser classificados contra os campos efetivamente disponiveis em cada registro de decisao.

### 4.3. Filtros candidatos para menor patch seguro

Candidatos de menor risco:

- filtro por decisao, se o campo decision estiver disponivel na listagem carregada
- filtro por level minimo, se level estiver disponivel e for numerico ou conversivel
- filtro por DTE maximo, se dte, dte_min ou campo equivalente estiver disponivel
- filtro por estrutura usando o indice ja existente de estruturas ativas
- botao Limpar para zerar busca e filtros avancados
- indicador textual de quantidade filtrada

Candidatos que exigem cuidado adicional:

- periodo De/Ate, pois depende de padronizacao do campo timestamp/data
- botao Aplicar, pois hoje a busca textual pode operar em tempo real
- interacao entre busca textual, filtros avancados e exportacao CSV

## 5. Decisao tecnica preliminar

A implementacao futura deve preferir filtragem em memoria sobre a lista ja carregada por UIDataModel.get_decisions(), desde que os campos necessarios estejam presentes.

Nao deve haver alteracao de banco, repositories, services, controllers ou contratos canonicos nesta rodada.

## 6. Menor patch seguro recomendado

Patch funcional recomendado para a proxima frente, apos revisao deste relatorio:

1. adicionar controles visuais discretos na aba Decisoes dark para decisao, level minimo e DTE maximo;
2. preservar a busca textual por estrutura ativa;
3. aplicar todos os filtros sobre filtered_decisions ou pipeline equivalente em memoria;
4. manter a exportacao CSV respeitando a listagem final exibida;
5. manter a selecao e o botao Carregar estrutura no Terminal funcionando apos filtragem;
6. adicionar indicador textual de quantidade exibida versus total elegivel;
7. deixar periodo De/Ate para subetapa posterior se o parsing de data exigir normalizacao adicional.

## 7. Restricoes preservadas

Esta frente nao altera:

- codigo funcional
- layout operacional
- callbacks
- banco
- schema
- services
- controllers
- repositories
- regra de negocio
- contratos canonicos
- entrypoint principal
- UI atual legada

## 8. Proximo passo

Revisar este relatorio e, se confirmado, abrir a frente de patch minimo para filtros avancados simples na aba Decisoes dark.
