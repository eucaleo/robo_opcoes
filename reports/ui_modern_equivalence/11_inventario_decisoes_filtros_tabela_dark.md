# Inventario dirigido de decisoes, filtros e tabela no modo dark

Data de referencia: 2026-07-02

## 1. Objetivo

Mapear, antes de qualquer patch funcional, a presenca ou ausencia de funcoes relacionadas a decisoes no modo dark da UI moderna.

Funcoes verificadas:

- filtros de decisoes
- tabela ou listagem de decisoes
- selecao de decisao
- detalhe da decisao
- rationale/why JSON
- conexoes com controllers, services e repositories

## 2. Restricoes

- nenhuma alteracao funcional foi feita nesta etapa
- nenhuma regra de negocio foi alterada
- nenhum banco foi alterado
- nenhum callback foi alterado
- a UI atual permanece preservada
- o modo dark permanece como UI moderna paralela

## 3. Arquivos priorizados

- UI\modern\dark_window.py - existe
- UI\modern\main_window.py - existe
- UI\main_window.py - existe
- UI\components\terminal_vwap_payoff_dark_panel.py - existe
- UI\components\terminal_vwap_payoff_panel.py - existe

## 4. Resumo de ocorrencias por grupo nos arquivos priorizados

| Grupo | Arquivo | Ocorrencias |
|---|---:|---:|
| decisoes | UI\modern\dark_window.py | 0 |
| decisoes | UI\modern\main_window.py | 54 |
| decisoes | UI\main_window.py | 59 |
| decisoes | UI\components\terminal_vwap_payoff_dark_panel.py | 21 |
| decisoes | UI\components\terminal_vwap_payoff_panel.py | 0 |
| filtros | UI\modern\dark_window.py | 0 |
| filtros | UI\modern\main_window.py | 34 |
| filtros | UI\main_window.py | 36 |
| filtros | UI\components\terminal_vwap_payoff_dark_panel.py | 22 |
| filtros | UI\components\terminal_vwap_payoff_panel.py | 0 |
| tabela_listagem | UI\modern\dark_window.py | 0 |
| tabela_listagem | UI\modern\main_window.py | 14 |
| tabela_listagem | UI\main_window.py | 17 |
| tabela_listagem | UI\components\terminal_vwap_payoff_dark_panel.py | 104 |
| tabela_listagem | UI\components\terminal_vwap_payoff_panel.py | 34 |
| selecao | UI\modern\dark_window.py | 7 |
| selecao | UI\modern\main_window.py | 29 |
| selecao | UI\main_window.py | 63 |
| selecao | UI\components\terminal_vwap_payoff_dark_panel.py | 93 |
| selecao | UI\components\terminal_vwap_payoff_panel.py | 31 |
| detalhe_rationale_why | UI\modern\dark_window.py | 1 |
| detalhe_rationale_why | UI\modern\main_window.py | 65 |
| detalhe_rationale_why | UI\main_window.py | 76 |
| detalhe_rationale_why | UI\components\terminal_vwap_payoff_dark_panel.py | 99 |
| detalhe_rationale_why | UI\components\terminal_vwap_payoff_panel.py | 11 |
| camadas_servicos | UI\modern\dark_window.py | 0 |
| camadas_servicos | UI\modern\main_window.py | 76 |
| camadas_servicos | UI\main_window.py | 78 |
| camadas_servicos | UI\components\terminal_vwap_payoff_dark_panel.py | 38 |
| camadas_servicos | UI\components\terminal_vwap_payoff_panel.py | 20 |

## 5. Evidencias nos arquivos priorizados

### 5.x. UI\modern\dark_window.py

Classes encontradas:

- ModernDarkWindow

Metodos encontrados:

- __init__
- _build_menu
- _build_layout
- set_status
- _reload_panel
- _show_about
- run
- main

#### Grupo: decisoes

- nenhuma evidencia textual direta encontrada

#### Grupo: filtros

- nenhuma evidencia textual direta encontrada

#### Grupo: tabela_listagem

- nenhuma evidencia textual direta encontrada

#### Grupo: selecao

- L50: app_menu.add_command(label="Atualizar", command=self._reload_panel)
- L52: app_menu.add_command(label="Sair", command=self.root.quit)
- L55: help_menu.add_command(label="Sobre", command=self._show_about)
- L81: def _reload_panel(self) -> None:
- L83: if hasattr(self.panel, "reload_structures"):
- L84: self.panel.reload_structures()

#### Grupo: detalhe_rationale_why

- L57: menu_bar.add_cascade(label="Aplicação", menu=app_menu)

#### Grupo: camadas_servicos

- nenhuma evidencia textual direta encontrada

### 5.x. UI\modern\main_window.py

Classes encontradas:

- ModernMainWindow

Metodos encontrados:

- __init__
- _setup_style
- _setup_layout
- _build_header
- _build_sidebar
- _side_button
- _build_workspace
- _build_analysis_tab
- _build_structures_tab
- _build_terminal_tab
- _bind_events
- set_status
- on_filter_change
- on_decision_selected
- _start_payoff_load
- worker
- _finish_payoff_load
- _handle_payoff_error
- refresh_data
- export_csv
- run_pipeline
- recalculate_structure
- finish
- worker
- check_databases
- clear_cache
- _on_structure_selected
- _on_structure_edit_request
- run
- main

#### Grupo: decisoes

- L20: from UI.components.decisions_grid import DecisionsGrid
- L56: self.last_selected_decision: Optional[Dict] = None
- L212: self.decisions_grid = DecisionsGrid(
- L214: on_selection_change=self.on_decision_selected,
- L216: self.decisions_grid.pack(fill="both", expand=True, padx=4, pady=4)
- L222: detail_notebook.add(details_frame, text="Detalhes da decisão")
- L322: # Decisões / filtros / payoff
- L329: filtered_data = self.data_model.get_decisions(filters)
- L330: self.decisions_grid.update_data(filtered_data)
- L331: self.set_status(f"{len(filtered_data)} decisões encontradas")
- L336: def on_decision_selected(self, decision_data: Dict) -> None:
- L337: if not decision_data:
- L340: self.last_selected_decision = dict(decision_data)
- L343: self.details_panel.update_decision(decision_data)
- L347: structure_id = decision_data.get("structure_id")
- L348: timestamp = decision_data.get("timestamp")
- L351: self._start_payoff_load(structure_id, timestamp, decision_data)
- L360: decision_data=None,
- L362: if decision_data is None:
- L363: decision_data = {"structure_id": structure_id}
- L415: decision_data,
- L434: decision_data: Dict,
- L444: overlays = self.payoff_chart.update_chart(points, decision_data)
- L459: used_ts = (info_dict or {}).get("used_timestamp") or decision_data.get(
- L466: if used_ts and used_ts != decision_data.get("timestamp"):
- L509: decisions = self.data_model.get_decisions()
- L510: self.decisions_grid.update_data(decisions)
- L513: previous = self.last_selected_decision
- L521: self.decisions_grid.select_by_key(structure_id, timestamp)
- L526: self.details_panel.update_decision(previous)
- L547: self.set_status(f"Dados atualizados - {len(decisions)} decisões")
- L567: current_data = self.decisions_grid.get_current_data()

#### Grupo: filtros

- L22: from UI.components.filters_panel import FiltersPanel
- L206: self.filters_panel = FiltersPanel(
- L208: on_filter_change=self.on_filter_change,
- L210: self.filters_panel.pack(fill="x", padx=4, pady=(0, 6))
- L322: # Decisões / filtros / payoff
- L325: def on_filter_change(self, filters: Dict) -> None:
- L326: self.set_status("Aplicando filtros...")
- L329: filtered_data = self.data_model.get_decisions(filters)
- L330: self.decisions_grid.update_data(filtered_data)
- L331: self.set_status(f"{len(filtered_data)} decisões encontradas")
- L333: messagebox.showerror("Erro", f"Erro ao aplicar filtros: {exc}")
- L334: self.set_status("Erro nos filtros")
- L498: self.filters_panel.update_structures(
- L505: self.filters_panel.reset_filters()

#### Grupo: tabela_listagem

- L20: from UI.components.decisions_grid import DecisionsGrid
- L212: self.decisions_grid = DecisionsGrid(
- L216: self.decisions_grid.pack(fill="both", expand=True, padx=4, pady=4)
- L330: self.decisions_grid.update_data(filtered_data)
- L462: source = (info_dict or {}).get("source_table", "payoff_curve_points")
- L510: self.decisions_grid.update_data(decisions)
- L521: self.decisions_grid.select_by_key(structure_id, timestamp)
- L567: current_data = self.decisions_grid.get_current_data()
- L597: [sys.executable, str(script_path)],
- L660: [sys.executable, str(script_path)],
- L717: txt.insert("end", "Nenhuma estrutura selecionada.")
- L745: txt.insert("end", "\n".join(lines))

#### Grupo: selecao

- L54: self._loading_payoff = False
- L56: self.last_selected_decision: Optional[Dict] = None
- L179: btn = ttk.Button(parent, text=text, command=command)
- L214: on_selection_change=self.on_decision_selected,
- L252: on_structure_selected=self._on_structure_selected,
- L311: self.root.bind("<F5>", lambda _e: self.refresh_data())
- L312: self.root.bind("<Control-q>", lambda _e: self.root.quit())
- L336: def on_decision_selected(self, decision_data: Dict) -> None:
- L340: self.last_selected_decision = dict(decision_data)
- L351: self._start_payoff_load(structure_id, timestamp, decision_data)
- L354: self.set_status("Dados insuficientes para carregar payoff")
- L356: def _start_payoff_load(
- L367: self._loading_payoff = True
- L412: self._finish_payoff_load,
- L430: def _finish_payoff_load(
- L440: self._loading_payoff = False
- L481: self._loading_payoff = False
- L488: self.set_status(f"Erro ao carregar payoff: {error_msg}")
- L513: previous = self.last_selected_decision
- L521: self.decisions_grid.select_by_key(structure_id, timestamp)
- L531: self._start_payoff_load(structure_id, timestamp, previous)
- L550: messagebox.showerror("Erro", f"Erro ao carregar dados: {exc}")
- L551: self.set_status("Erro ao carregar dados")
- L711: def _on_structure_selected(self, structure: Optional[Dict]) -> None:
- L717: txt.insert("end", "Nenhuma estrutura selecionada.")
- L759: self.structures_list.load()

#### Grupo: detalhe_rationale_why

- L21: from UI.components.details_panel import DetailsPanel
- L218: detail_notebook = ttk.Notebook(right)
- L219: detail_notebook.pack(fill="both", expand=True, padx=4, pady=4)
- L221: details_frame = ttk.Frame(detail_notebook)
- L222: detail_notebook.add(details_frame, text="Detalhes da decisão")
- L224: self.details_panel = DetailsPanel(
- L225: details_frame,
- L229: self.details_panel.pack(fill="both", expand=True, padx=4, pady=4)
- L231: chart_frame = ttk.Frame(detail_notebook)
- L232: detail_notebook.add(chart_frame, text="Curva de payoff")
- L245: right = ttk.LabelFrame(paned, text="Detalhes", padding=8)
- L258: self._struct_detail_text = tk.Text(
- L265: self._struct_detail_text.pack(fill="both", expand=True)
- L303: "Terminal VWAP Payoff indisponível neste shell.\n\n"
- L326: self.set_status("Aplicando filtros...")
- L333: messagebox.showerror("Erro", f"Erro ao aplicar filtros: {exc}")
- L343: self.details_panel.update_decision(decision_data)
- L345: print(f"[ModernUI] Erro ao atualizar detalhes: {exc}")
- L388: if "spot" in point and "pl" in point:
- L390: {"spot": point["spot"], "pl": point["pl"]}
- L392: elif "point_spot" in point and "point_pl" in point:
- L396: "pl": point["point_pl"],
- L401: pl = point.get("y") if "y" in point else point.get("p")
- L402: if spot is not None and pl is not None:
- L403: normalized.append({"spot": spot, "pl": pl})
- L404: elif isinstance(point, (list, tuple)) and len(point) >= 2:
- L405: normalized.append({"spot": point[0], "pl": point[1]})
- L447: self.details_panel.update_breakevens(
- L449: overlays.get("pl_at_spot_ref"),
- L455: self.details_panel.update_audit_info(info_dict or {})
- L526: self.details_panel.update_decision(previous)
- L538: self.details_panel.clear()
- L644: if hasattr(self.details_panel, "on_recalc_finished"):
- L645: self.details_panel.on_recalc_finished(
- L651: print("[ModernUI] Erro notificando details_panel:", exc)
- L712: txt = self._struct_detail_text
- L738: f"  Venc.  : {leg.get('expiration_date')}",
- L742: f"  Mult.  : {leg.get('multiplier')}",

#### Grupo: camadas_servicos

- L20: from UI.components.decisions_grid import DecisionsGrid
- L56: self.last_selected_decision: Optional[Dict] = None
- L62: self._bind_events()
- L212: self.decisions_grid = DecisionsGrid(
- L214: on_selection_change=self.on_decision_selected,
- L216: self.decisions_grid.pack(fill="both", expand=True, padx=4, pady=4)
- L272: from controllers.terminal_vwap_payoff_controller import (
- L273: TerminalVWAPPayoffController,
- L275: from repositories.structures_repository import StructuresRepository
- L276: from services.terminal_vwap_payoff_app_service import (
- L277: TerminalVWAPPayoffAppService,
- L281: repository = StructuresRepository(self._db_path)
- L282: app_service = TerminalVWAPPayoffAppService(
- L283: structure_repository=repository,
- L285: controller = TerminalVWAPPayoffController(app_service)
- L289: controller=controller,
- L310: def _bind_events(self) -> None:
- L329: filtered_data = self.data_model.get_decisions(filters)
- L330: self.decisions_grid.update_data(filtered_data)
- L336: def on_decision_selected(self, decision_data: Dict) -> None:
- L337: if not decision_data:
- L340: self.last_selected_decision = dict(decision_data)
- L343: self.details_panel.update_decision(decision_data)
- L347: structure_id = decision_data.get("structure_id")
- L348: timestamp = decision_data.get("timestamp")
- L351: self._start_payoff_load(structure_id, timestamp, decision_data)
- L360: decision_data=None,
- L362: if decision_data is None:
- L363: decision_data = {"structure_id": structure_id}
- L415: decision_data,
- L434: decision_data: Dict,
- L444: overlays = self.payoff_chart.update_chart(points, decision_data)
- L459: used_ts = (info_dict or {}).get("used_timestamp") or decision_data.get(
- L466: if used_ts and used_ts != decision_data.get("timestamp"):
- L509: decisions = self.data_model.get_decisions()
- L510: self.decisions_grid.update_data(decisions)
- L513: previous = self.last_selected_decision
- L521: self.decisions_grid.select_by_key(structure_id, timestamp)
- L526: self.details_panel.update_decision(previous)
- L547: self.set_status(f"Dados atualizados - {len(decisions)} decisões")

### 5.x. UI\main_window.py

Classes encontradas:

- MainWindow

Metodos encontrados:

- __init__
- _setup_layout
- _setup_menus
- _bind_events
- on_filter_change
- on_decision_selected
- _start_payoff_load
- load_worker
- refresh_data
- export_csv
- recalculate_structure
- finish
- worker
- run_pipeline
- check_databases
- clear_cache
- show_about
- _finish_payoff_load
- _handle_payoff_error
- _start_loading_animation
- animate
- _stop_loading_animation
- _setup_structures_tab
- _on_structure_selected
- _on_structure_edit_request
- _setup_terminal_vwap_payoff_tab
- run
- main

#### Grupo: decisoes

- L5: Carrega dados de derived.db e app.db para exibir decisões e payoffs
- L10: from UI.components.decisions_grid import DecisionsGrid
- L31: self.root.title("Sistema de Derivados - Análise de Decisões")
- L50: # Última decisão selecionada (preservada entre refreshes)
- L51: self.last_selected_decision: Optional[Dict] = None
- L84: self.decisions_grid = DecisionsGrid(
- L86: on_selection_change=self.on_decision_selected,
- L88: self.decisions_grid.pack(fill="both", expand=True, padx=5, pady=5)
- L94: # Aba 1: Detalhes da Decisão
- L96: right_notebook.add(details_frame, text="Detalhes da Decisão")
- L166: filtered_data = self.data_model.get_decisions(filters)
- L167: self.decisions_grid.update_data(filtered_data)
- L169: self.status_bar.config(text=f"{count} decisões encontradas")
- L174: def on_decision_selected(self, decision_data: Dict):
- L175: """Callback quando uma decisão é selecionada no grid.
- L178: if not decision_data:
- L181: self.last_selected_decision = dict(decision_data)
- L185: self.details_panel.update_decision(decision_data)
- L190: structure_id = decision_data.get("structure_id")
- L191: timestamp = decision_data.get("timestamp")  # opcional
- L194: self._start_payoff_load(structure_id, timestamp, decision_data)
- L203: decision_data=None,   # alteracao_36: opcional
- L208: if decision_data is None:
- L209: decision_data = {"structure_id": structure_id}
- L259: decision_data,
- L294: decisions = self.data_model.get_decisions()
- L295: self.decisions_grid.update_data(decisions)
- L298: d = self.last_selected_decision
- L307: self.decisions_grid.select_by_key(target_sid, target_ts)
- L312: self.details_panel.update_decision(d)
- L333: text=f"Dados atualizados - {len(decisions)} decisões"
- L349: current_data = self.decisions_grid.get_current_data()
- L509: Pipeline automático de payoff e decisões
- L528: decision_data: Dict,
- L540: overlays = self.payoff_chart.update_chart(points, decision_data)
- L555: used_ts = (info_dict or {}).get("used_timestamp") or decision_data.get(
- L561: if used_ts and used_ts != decision_data.get("timestamp"):

#### Grupo: filtros

- L11: from UI.components.filters_panel import FiltersPanel
- L69: # Painel esquerdo: filtros + grid
- L78: self.filters_panel = FiltersPanel(
- L80: on_filter_change=self.on_filter_change,
- L82: self.filters_panel.pack(fill="x", padx=5, pady=5)
- L162: def on_filter_change(self, filters: Dict):
- L163: """Callback quando filtros mudam."""
- L164: self.status_bar.config(text="Aplicando filtros...")
- L166: filtered_data = self.data_model.get_decisions(filters)
- L167: self.decisions_grid.update_data(filtered_data)
- L168: count = len(filtered_data)
- L171: messagebox.showerror("Erro", f"Erro ao aplicar filtros: {e}")
- L172: self.status_bar.config(text="Erro nos filtros")
- L283: self.filters_panel.update_structures(
- L290: self.filters_panel.reset_filters()

#### Grupo: tabela_listagem

- L10: from UI.components.decisions_grid import DecisionsGrid
- L69: # Painel esquerdo: filtros + grid
- L84: self.decisions_grid = DecisionsGrid(
- L88: self.decisions_grid.pack(fill="both", expand=True, padx=5, pady=5)
- L167: self.decisions_grid.update_data(filtered_data)
- L175: """Callback quando uma decisão é selecionada no grid.
- L295: self.decisions_grid.update_data(decisions)
- L304: # Reselecionar na grid: structure_id é suficiente
- L307: self.decisions_grid.select_by_key(target_sid, target_ts)
- L349: current_data = self.decisions_grid.get_current_data()
- L405: [sys.executable, str(script_path)],
- L463: [sys.executable, str(script_path)],
- L558: src = (info_dict or {}).get("source_table", "payoff_curve_points")
- L651: txt.insert("end", "Nenhuma estrutura selecionada.")
- L674: txt.insert("end", "\n".join(lines))

#### Grupo: selecao

- L43: # Loading animation
- L44: self._loading_animation_active = False
- L45: self._loading_animation_chars = ["", "", "", "", "", "", "", "", "", ""]
- L46: self._loading_animation_index = 0
- L47: self._loading_payoff = False
- L48: self._stop_loading_animation()
- L50: # Última decisão selecionada (preservada entre refreshes)
- L51: self.last_selected_decision: Optional[Dict] = None
- L61: # Carregar dados iniciais
- L86: on_selection_change=self.on_decision_selected,
- L134: file_menu.add_command(label="Atualizar Dados", command=self.refresh_data)
- L136: file_menu.add_command(label="Exportar CSV...", command=self.export_csv)
- L138: file_menu.add_command(label="Sair", command=self.root.quit)
- L143: tools_menu.add_command(label="Executar Pipeline", command=self.run_pipeline)
- L144: tools_menu.add_command(label="Verificar Bancos", command=self.check_databases)
- L146: tools_menu.add_command(label="Limpar Cache", command=self.clear_cache)
- L151: help_menu.add_command(label="Sobre", command=self.show_about)
- L155: self.root.bind("<F5>", lambda e: self.refresh_data())
- L156: self.root.bind("<Control-q>", lambda e: self.root.quit())
- L174: def on_decision_selected(self, decision_data: Dict):
- L175: """Callback quando uma decisão é selecionada no grid.
- L176: alteracao_36: structure_id é suficiente para carregar payoff -- timestamp não é obrigatório.
- L181: self.last_selected_decision = dict(decision_data)
- L189: # Carregar payoff em background -- apenas structure_id necessário
- L194: self._start_payoff_load(structure_id, timestamp, decision_data)
- L199: def _start_payoff_load(
- L214: if self._loading_payoff:
- L219: self._loading_payoff = True
- L221: def load_worker():
- L256: self._finish_payoff_load,
- L271: thread = threading.Thread(target=load_worker, daemon=True)
- L298: d = self.last_selected_decision
- L304: # Reselecionar na grid: structure_id é suficiente
- L307: self.decisions_grid.select_by_key(target_sid, target_ts)
- L317: self._start_payoff_load(target_sid, target_ts, d)
- L337: messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
- L338: self.status_bar.config(text="Erro ao carregar dados")
- L524: def _finish_payoff_load(
- L535: self._loading_payoff = False
- L536: self._stop_loading_animation()

#### Grupo: detalhe_rationale_why

- L9: from UI.components.details_panel import DetailsPanel
- L20: import matplotlib.pyplot as plt
- L94: # Aba 1: Detalhes da Decisão
- L95: details_frame = ttk.Frame(right_notebook)
- L96: right_notebook.add(details_frame, text="Detalhes da Decisão")
- L98: self.details_panel = DetailsPanel(
- L99: details_frame,
- L103: self.details_panel.pack(fill="both", expand=True, padx=5, pady=5)
- L164: self.status_bar.config(text="Aplicando filtros...")
- L171: messagebox.showerror("Erro", f"Erro ao aplicar filtros: {e}")
- L183: # Atualizar painel de detalhes (síncrono, leve)
- L185: self.details_panel.update_decision(decision_data)
- L187: print(f"[UI] Erro ao atualizar detalhes: {e}")
- L238: if "spot" in p and "pl" in p:
- L239: norm.append({"spot": p["spot"], "pl": p["pl"]})
- L240: elif "point_spot" in p and "point_pl" in p:
- L241: norm.append({"spot": p["point_spot"], "pl": p["point_pl"]})
- L244: pl = p.get("y") if "y" in p else p.get("p")
- L245: if spot is not None and pl is not None:
- L246: norm.append({"spot": spot, "pl": pl})
- L247: elif isinstance(p, (list, tuple)) and len(p) >= 2:
- L248: norm.append({"spot": p[0], "pl": p[1]})
- L312: self.details_panel.update_decision(d)
- L324: self.details_panel.clear()
- L388: if hasattr(self, "details_panel") and hasattr(
- L389: self.details_panel, "on_recalc_finished"
- L391: self.details_panel.on_recalc_finished(
- L395: print("[UI] Erro notificando details_panel fim recalc:", e)
- L543: self.details_panel.update_breakevens(
- L545: overlays.get("pl_at_spot_ref"),
- L551: self.details_panel.update_audit_info(info_dict or {})
- L631: # Painel direito -- detalhes somente leitura
- L632: detail_frame = ttk.LabelFrame(paned, text="Detalhes", padding=8)
- L633: paned.add(detail_frame, weight=1)
- L635: self._struct_detail_text = tk.Text(
- L636: detail_frame,
- L642: self._struct_detail_text.pack(fill="both", expand=True)
- L645: """Exibe detalhes da estrutura selecionada no painel direito."""
- L646: txt = self._struct_detail_text
- L669: f"         Strike : {leg.get('strike')}  Venc: {leg.get('expiration_date')}",

#### Grupo: camadas_servicos

- L10: from UI.components.decisions_grid import DecisionsGrid
- L51: self.last_selected_decision: Optional[Dict] = None
- L59: self._bind_events()
- L84: self.decisions_grid = DecisionsGrid(
- L86: on_selection_change=self.on_decision_selected,
- L88: self.decisions_grid.pack(fill="both", expand=True, padx=5, pady=5)
- L153: def _bind_events(self):
- L166: filtered_data = self.data_model.get_decisions(filters)
- L167: self.decisions_grid.update_data(filtered_data)
- L174: def on_decision_selected(self, decision_data: Dict):
- L178: if not decision_data:
- L181: self.last_selected_decision = dict(decision_data)
- L185: self.details_panel.update_decision(decision_data)
- L190: structure_id = decision_data.get("structure_id")
- L191: timestamp = decision_data.get("timestamp")  # opcional
- L194: self._start_payoff_load(structure_id, timestamp, decision_data)
- L203: decision_data=None,   # alteracao_36: opcional
- L208: if decision_data is None:
- L209: decision_data = {"structure_id": structure_id}
- L259: decision_data,
- L294: decisions = self.data_model.get_decisions()
- L295: self.decisions_grid.update_data(decisions)
- L298: d = self.last_selected_decision
- L307: self.decisions_grid.select_by_key(target_sid, target_ts)
- L312: self.details_panel.update_decision(d)
- L333: text=f"Dados atualizados - {len(decisions)} decisões"
- L349: current_data = self.decisions_grid.get_current_data()
- L528: decision_data: Dict,
- L540: overlays = self.payoff_chart.update_chart(points, decision_data)
- L555: used_ts = (info_dict or {}).get("used_timestamp") or decision_data.get(
- L561: if used_ts and used_ts != decision_data.get("timestamp"):
- L705: from repositories.structures_repository import StructuresRepository
- L706: from services.terminal_vwap_payoff_app_service import (
- L707: TerminalVWAPPayoffAppService,
- L709: from controllers.terminal_vwap_payoff_controller import (
- L710: TerminalVWAPPayoffController,
- L716: or getattr(getattr(self, "repository", None), "db_path", None)
- L720: structure_repository = StructuresRepository(db_path)
- L721: app_service = TerminalVWAPPayoffAppService(
- L722: structure_repository=structure_repository,

### 5.x. UI\components\terminal_vwap_payoff_dark_panel.py

Classes encontradas:

- TerminalVWAPPayoffDarkPanel

Metodos encontrados:

- _q
- _norm
- _first_col
- _to_float
- _money
- _number
- decision_label
- __init__
- _setup_style
- _setup_layout
- _create_kpi
- toggle_structures_panel
- reload_structures
- _connect
- _tables_cols
- _find_structures_table
- _load_structures
- _render_structures_list
- select_structure
- _find_legs_table
- _load_legs
- _load_market
- _load_payoff_points
- _load_persisted_payoff_points
- _calculate_payoff_from_legs
- _breakevens
- _update_kpis
- _render_legs
- _set_alerts
- _render_alerts
- _clear_canvas
- _figure
- _render_empty_charts
- _render_charts
- _render_vwap_chart
- _render_payoff_chart
- _build_payoff_export_button
- export_payoff_png
- _safe_status
- _get_db_path
- _clear_side
- _require_selected_structure
- _side_section_title
- _side_button
- _render_structure_actions
- _render_adjust_structure_block
- new_structure
- edit_selected_structure
- duplicate_selected_structure
- recalculate_selected_structure
- archive_selected_structure
- _register_structure_decision

#### Grupo: decisoes

- L113: # BEGIN AUTO STRUCTURE DECISION HELPERS
- L114: if "DECISION_LABELS" not in globals():
- L115: DECISION_LABELS = {
- L122: def decision_label(value: Any) -> str:
- L126: return DECISION_LABELS.get(raw.upper(), raw)
- L127: # END AUTO STRUCTURE DECISION HELPERS
- L1335: self._side_section_title("DECISAO")
- L1340: command=lambda: self._register_structure_decision("HOLD"),
- L1352: command=lambda: self._register_structure_decision("CLOSE"),
- L1402: text="Modo de ajuste aberto. Edite as pernas, duplique para ajuste ou registre a decisao ADJUST.",
- L1424: text="Registrar decisao ADJUST",
- L1427: command=lambda: self._register_structure_decision("ADJUST"),
- L1659: def _register_structure_decision(self, decision: str) -> None:
- L1666: label = decision_label(decision)
- L1668: if decision == "CLOSE":
- L1689: msg = f"Decisao registrada para ID {sid}: {label} ({decision}). Estrutura encerrada."
- L1705: msg = f"Decisao registrada para ID {sid}: {label} ({decision})"

#### Grupo: filtros

- L1172: parent=self.winfo_toplevel(),
- L1181: parent=self.winfo_toplevel(),
- L1194: parent=self.winfo_toplevel(),
- L1201: parent=self.winfo_toplevel(),
- L1229: parent=self.winfo_toplevel(),
- L1442: parent=self.winfo_toplevel(),
- L1448: self.winfo_toplevel(),
- L1459: messagebox.showerror("Erro ao criar estrutura", str(exc), parent=self.winfo_toplevel())
- L1471: parent=self.winfo_toplevel(),
- L1480: self.winfo_toplevel(),
- L1500: messagebox.showerror("Erro ao editar estrutura", str(exc), parent=self.winfo_toplevel())
- L1512: parent=self.winfo_toplevel(),
- L1526: parent=self.winfo_toplevel(),
- L1565: messagebox.showerror("Erro ao duplicar estrutura", str(exc), parent=self.winfo_toplevel())
- L1596: messagebox.showerror("Erro ao recalcular payoff", str(exc), parent=self.winfo_toplevel())
- L1610: parent=self.winfo_toplevel(),
- L1623: messagebox.showinfo("Arquivar", msg, parent=self.winfo_toplevel())
- L1629: parent=self.winfo_toplevel(),
- L1651: parent=self.winfo_toplevel(),
- L1656: messagebox.showerror("Erro ao arquivar estrutura", str(exc), parent=self.winfo_toplevel())
- L1679: parent=self.winfo_toplevel(),
- L1702: messagebox.showerror("Erro ao encerrar estrutura", str(exc), parent=self.winfo_toplevel())

#### Grupo: tabela_listagem

- L11: - tabela inferior de pernas;
- L56: GRID = "#333333"
- L163: "Dark.Treeview",
- L167: bordercolor=GRID,
- L171: "Dark.Treeview.Heading",
- L177: "Dark.Treeview",
- L183: self.grid_columnconfigure(0, weight=0)
- L184: self.grid_columnconfigure(1, weight=0)
- L185: self.grid_columnconfigure(2, weight=1)
- L186: self.grid_rowconfigure(0, weight=1)
- L194: self.rail.grid(row=0, column=0, sticky="nsew")
- L195: self.rail.grid_propagate(False)
- L267: self.side.grid(row=0, column=1, sticky="nsew")
- L268: self.side.grid_propagate(False)
- L274: self.main.grid(row=0, column=2, sticky="nsew", padx=15, pady=15)
- L275: self.main.grid_columnconfigure((0, 1), weight=1)
- L276: self.main.grid_rowconfigure(2, weight=3)
- L277: self.main.grid_rowconfigure(3, weight=1)
- L285: self.header.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))
- L291: self.kpi_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 12))
- L292: self.kpi_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
- L306: self.frame_vwap.grid(row=2, column=0, sticky="nsew", padx=(0, 10), pady=5)
- L313: self.frame_payoff.grid(row=2, column=1, sticky="nsew", padx=(10, 0), pady=5)
- L320: self.bottom.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(12, 0))
- L321: self.bottom.grid_columnconfigure(0, weight=3)
- L322: self.bottom.grid_columnconfigure(1, weight=1)
- L323: self.bottom.grid_rowconfigure(1, weight=1)
- L331: self.legs_title.grid(row=0, column=0, sticky="w", padx=12, pady=(8, 4))
- L339: self.alerts_title.grid(row=0, column=1, sticky="w", padx=12, pady=(8, 4))
- L341: self.legs_table = ttk.Treeview(
- L343: columns=("n", "symbol", "side", "type", "strike", "expiration", "qty", "premium"),
- L344: show="headings",
- L345: style="Dark.Treeview",
- L369: self.legs_table.heading(col, text=title)
- L370: self.legs_table.column(col, width=widths[col], anchor="center")
- L372: self.legs_table.grid(row=1, column=0, sticky="nsew", padx=(12, 6), pady=(0, 12))
- L381: self.alerts_box.grid(row=1, column=1, sticky="nsew", padx=(6, 12), pady=(0, 12))
- L392: card.grid(row=0, column=column, sticky="ew", padx=5)
- L414: self.side.grid_remove()
- L418: self.side.grid(row=0, column=1, sticky="nsew")

#### Grupo: selecao

- L143: self.selected_structure: Optional[Dict[str, Any]] = None
- L153: self.reload_structures()
- L178: background=[("selected", BLUE)],
- L179: foreground=[("selected", TEXT)],
- L205: command=self.toggle_structures_panel,
- L209: self.btn_reload_fixed = ctk.CTkButton(
- L218: command=self.reload_structures,
- L220: self.btn_reload_fixed.pack(pady=6, padx=10)
- L231: command=self.new_structure,
- L244: command=self._render_structure_actions,
- L257: command=self.toggle_structures_panel,
- L281: text="Selecione uma estrutura no menu lateral para carregar a VWAP e Payoff",
- L382: self._set_alerts(["Nenhuma estrutura selecionada."])
- L423: def reload_structures(self) -> None:
- L424: self.structures = self._load_structures()
- L437: rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
- L468: def _load_structures(self) -> List[Dict[str, Any]]:
- L485: select_parts = [
- L492: sql = f"SELECT {', '.join(select_parts)} FROM {_q(table)} ORDER BY {_q(id_col)}"
- L519: command=self.new_structure,
- L532: btn_reload = ctk.CTkButton(
- L538: command=self.reload_structures,
- L540: btn_reload.pack(fill="x", padx=10, pady=(0, 8))
- L572: command=lambda s=structure: self.select_structure(s),
- L576: def select_structure(self, structure: Dict[str, Any]) -> None:
- L577: self.selected_structure = dict(structure)
- L583: legs = self._load_legs(sid)
- L584: market = self._load_market(asset)
- L585: payoff_points = self._load_payoff_points(sid, legs)
- L598: # Menu lateral fixo: não recolher automaticamente após carregar estrutura.
- L628: def _load_legs(self, structure_id: Any) -> List[Dict[str, Any]]:
- L650: select_parts = [
- L662: f"SELECT {', '.join(select_parts)} "
- L672: def _load_market(self, asset: Any) -> Dict[str, Any]:
- L741: select_parts = [
- L767: f"SELECT {', '.join(select_parts)} "
- L815: def _load_payoff_points(
- L820: persisted = self._load_persisted_payoff_points(structure_id)
- L825: def _load_persisted_payoff_points(self, structure_id: Any) -> List[Dict[str, float]]:
- L840: f"SELECT {_q(spot_col)} AS spot, {_q(pl_col)} AS pl "

#### Grupo: detalhe_rationale_why

- L22: from typing import Any, Dict, List, Optional, Sequence, Tuple
- L29: from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
- L30: from matplotlib.figure import Figure
- L60: return '"' + str(name).replace('"', '""') + '"'
- L85: text = text.replace("R$", "").replace(" ", "")
- L87: text = text.replace(".", "").replace(",", ".")
- L89: text = text.replace(",", ".")
- L103: return "R$ " + f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
- L110: return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
- L343: columns=("n", "symbol", "side", "type", "strike", "expiration", "qty", "premium"),
- L354: "expiration": "Vencimento",
- L364: "expiration": 100,
- L553: wraplength=210,
- L642: exp_col = _first_col(cols, ["expiration_date", "expiration", "vencimento"])
- L645: mult_col = _first_col(cols, ["multiplier", "multiplicador"])
- L655: f"{_q(exp_col)} AS expiration_date" if exp_col else "NULL AS expiration_date",
- L658: f"{_q(mult_col)} AS multiplier" if mult_col else "NULL AS multiplier",
- L832: pl_col = _first_col(cols, ["point_pl", "pl", "payoff", "result", "resultado", "y"])
- L835: if not sid_col or not spot_col or not pl_col:
- L840: f"SELECT {_q(spot_col)} AS spot, {_q(pl_col)} AS pl "
- L849: pl = _to_float(row["pl"])
- L850: if spot is not None and pl is not None:
- L851: points.append({"spot": spot, "pl": pl})
- L886: multiplier = abs(_to_float(leg.get("multiplier"), 1.0) or 1.0)
- L905: total += sign * (intrinsic - premium) * quantity * multiplier
- L907: points.append({"spot": spot, "pl": total})
- L918: y1 = prev["pl"]
- L920: y2 = curr["pl"]
- L959: vals = [p["pl"] for p in payoff_points]
- L988: leg.get("expiration_date") or "--",
- L1032: def _figure(self) -> Tuple[Figure, Any]:
- L1035: ax = fig.add_subplot(111)
- L1068: ax.plot(
- L1078: ax.plot(
- L1091: "VWAP do ativo-base indisponível no app.db",
- L1117: ys = [p["pl"] for p in points]
- L1120: ax.plot(xs, ys, color=color, linewidth=2.0)
- L1130: "Payoff indisponível",
- L1171: "Nenhum grafico de payoff disponivel para exportar.",
- L1172: parent=self.winfo_toplevel(),

#### Grupo: camadas_servicos

- L34: from repositories.structures_repository import StructuresRepository
- L36: StructuresRepository = None
- L113: # BEGIN AUTO STRUCTURE DECISION HELPERS
- L114: if "DECISION_LABELS" not in globals():
- L115: DECISION_LABELS = {
- L122: def decision_label(value: Any) -> str:
- L126: return DECISION_LABELS.get(raw.upper(), raw)
- L127: # END AUTO STRUCTURE DECISION HELPERS
- L1340: command=lambda: self._register_structure_decision("HOLD"),
- L1352: command=lambda: self._register_structure_decision("CLOSE"),
- L1427: command=lambda: self._register_structure_decision("ADJUST"),
- L1491: repo = StructuresRepository(db_path)
- L1508: if StructuresRepository is None:
- L1511: "StructuresRepository nao foi encontrado.",
- L1519: repo = StructuresRepository(self._get_db_path())
- L1606: if StructuresRepository is None:
- L1609: "StructuresRepository nao foi encontrado.",
- L1615: repo = StructuresRepository(self._get_db_path())
- L1659: def _register_structure_decision(self, decision: str) -> None:
- L1666: label = decision_label(decision)
- L1668: if decision == "CLOSE":
- L1686: repo = StructuresRepository(self._get_db_path())
- L1689: msg = f"Decisao registrada para ID {sid}: {label} ({decision}). Estrutura encerrada."
- L1705: msg = f"Decisao registrada para ID {sid}: {label} ({decision})"

### 5.x. UI\components\terminal_vwap_payoff_panel.py

Classes encontradas:

- TerminalVWAPPayoffPanel

Metodos encontrados:

- _to_float
- _safe_text
- _format_number_br
- _format_currency_br
- _format_percent_br
- _extract_leg_table_rows
- _extract_payoff_table_rows
- _summarize_viewmodel
- __init__
- _build_ui
- _build_left_panel
- _build_right_panel
- _build_summary_tab
- _build_legs_tab
- _build_payoff_tab
- _build_warnings_tab
- reload_structures
- load_selected_structure
- load_structure
- _render_structures
- render_viewmodel
- _render_legs
- _render_payoff
- _render_warnings
- _set_status

#### Grupo: decisoes

- nenhuma evidencia textual direta encontrada

#### Grupo: filtros

- nenhuma evidencia textual direta encontrada

#### Grupo: tabela_listagem

- L80: def _extract_leg_table_rows(viewmodel: dict[str, Any]) -> list[tuple[str, ...]]:
- L100: def _extract_payoff_table_rows(
- L218: columns = ("structure_id", "name", "underlying_asset", "status", "legs")
- L219: self._structures_tree = ttk.Treeview(
- L221: columns=columns,
- L222: show="headings",
- L235: for column in columns:
- L237: self._structures_tree.heading(column, text=text)
- L315: ttk.Label(group, text=f"{label}:", width=18, anchor="e").grid(
- L330: ).grid(
- L340: columns = (
- L351: self._legs_tree = ttk.Treeview(parent, columns=columns, show="headings")
- L364: for column in columns:
- L366: self._legs_tree.heading(column, text=text)
- L386: columns = ("underlying_price", "result")
- L387: self._payoff_tree = ttk.Treeview(parent, columns=columns, show="headings")
- L389: self._payoff_tree.heading("underlying_price", text="Spot")
- L390: self._payoff_tree.heading("result", text="Resultado")
- L466: self._structures_tree.insert(
- L494: for index, row in enumerate(_extract_leg_table_rows(viewmodel)):
- L495: self._legs_tree.insert("", "end", iid=str(index), values=row)
- L501: rows = _extract_payoff_table_rows(viewmodel)
- L503: self._payoff_tree.insert("", "end", iid=str(index), values=row)
- L526: self._warnings_text.insert("1.0", text)

#### Grupo: selecao

- L172: self.reload_structures()
- L209: command=self.reload_structures,
- L214: text="Carregar",
- L215: command=self.load_selected_structure,
- L223: selectmode="browse",
- L248: command=self._structures_tree.yview,
- L250: self._structures_tree.configure(yscrollcommand=vsb.set)
- L255: self._structures_tree.bind("<Double-1>", lambda _e: self.load_selected_structure())
- L369: vsb = ttk.Scrollbar(parent, orient="vertical", command=self._legs_tree.yview)
- L370: self._legs_tree.configure(yscrollcommand=vsb.set)
- L395: vsb = ttk.Scrollbar(parent, orient="vertical", command=self._payoff_tree.yview)
- L396: self._payoff_tree.configure(yscrollcommand=vsb.set)
- L410: def reload_structures(self) -> None:
- L425: def load_selected_structure(self) -> None:
- L426: selected = self._structures_tree.selection()
- L427: if not selected:
- L428: self._set_status("Selecione uma estrutura para carregar")
- L431: item_id = selected[0]
- L440: self.load_structure(structure_id)
- L442: def load_structure(self, structure_id: Any) -> None:
- L445: viewmodel = self._controller.load_structure(structure_id)
- L447: self._set_status(f"Erro ao carregar estrutura {structure_id}: {exc}")
- L450: f"Erro ao carregar estrutura {structure_id}:\n{exc}",

#### Grupo: detalhe_rationale_why

- L5: Este componente pertence à UI principal. Ele não é uma aplicação separada,
- L41: text = text.replace(".", "").replace(",", ".")
- L61: return rendered.replace(",", "X").replace(".", ",").replace("X", ".")
- L80: def _extract_leg_table_rows(viewmodel: dict[str, Any]) -> list[tuple[str, ...]]:
- L81: rows: list[tuple[str, ...]] = []
- L91: _safe_text(leg.get("expiration_date")),
- L104: ) -> list[tuple[str, str]]:
- L111: rows: list[tuple[str, str]] = []

#### Grupo: camadas_servicos

- L11: -> TerminalVWAPPayoffController
- L12: -> TerminalVWAPPayoffAppService
- L14: -> TerminalVWAPPayoffViewModelService
- L157: controller: Any,
- L163: if controller is None:
- L164: raise ValueError("controller é obrigatório")
- L166: self._controller = controller
- L412: structures = self._controller.list_structures()
- L445: viewmodel = self._controller.load_structure(structure_id)


## 6. Busca ampliada em arquivos Python

A busca ampliada localiza possiveis pontos de implementacao ou reaproveitamento fora do modo dark.

| Grupo | Arquivos com ocorrencia | Total aproximado de ocorrencias |
|---|---:|---:|
| decisoes | 40 | 1058 |
| filtros | 55 | 801 |
| tabela_listagem | 67 | 823 |
| selecao | 99 | 1501 |
| detalhe_rationale_why | 133 | 3732 |
| camadas_servicos | 118 | 5139 |

## 7. Principais arquivos candidatos por grupo

### 7.x. decisoes

- db\derived_repo.py - 173
- reports\terminal_vwap_recovery\main_window_good_85dfbcd.py - 100
- ATT\tests\test_ui_data_migration.py - 74
- scripts\repair_derived_db_consistency.py - 64
- UI\main_window.py - 59
- reports\terminal_vwap_recovery\main_window_terminal_old.py - 59
- ATT\tests\test_structure_analysis_service.py - 56
- UI\modern\main_window.py - 54
- UI\components\details_panel.py - 49
- services\derived_service.py - 40
- UI\components\decisions_grid.py - 34
- services\calculation_orchestrator.py - 23
- UI\components\payoff_chart.py - 21
- UI\components\terminal_vwap_payoff_dark_panel.py - 21
- tools\patch_structure_side_panel.py - 20
- domain\decision.py - 19
- db\schema.py - 18
- services\derived_payoff_persistence.py - 17
- ATT\tests\test_orchestrator_run_methods.py - 17
- db\writer.py - 16
- ATT\tests\test_derived_service.py - 14
- services\structure_analysis_service.py - 13
- ATT\tests\test_payoff_chart.py - 13
- scripts\validate_derived_db.py - 12
- UI\models\ui_data.py - 12
- UI\components\filters_panel.py - 11
- db\reader.py - 9
- ATT\tests\test_decision.py - 8
- repositories\ui_data_table_candidates.py - 6
- db\migrations\add_structure_id_to_payoff_curve_points.py - 6

### 7.x. filtros

- UI\models\ui_data.py - 96
- UI\components\filters_panel.py - 74
- ATT\tests\test_structure_analysis_service.py - 69
- domain\decision.py - 42
- services\structure_analysis_service.py - 39
- reports\terminal_vwap_recovery\main_window_good_85dfbcd.py - 37
- UI\main_window.py - 36
- reports\terminal_vwap_recovery\main_window_terminal_old.py - 36
- UI\modern\main_window.py - 34
- repositories\pricing_executions_repository.py - 27
- repositories\structure_events_repository.py - 26
- domain\structure_metrics.py - 25
- UI\components\terminal_vwap_payoff_dark_panel.py - 22
- ATT\tests\test_ui_data_migration.py - 22
- UI\components\details_panel.py - 18
- db\derived_repo.py - 16
- ATT\tests\test_structure_metrics.py - 16
- services\calculation_orchestrator.py - 14
- UI\components\decisions_grid.py - 13
- repositories\market_snapshot_repository.py - 11
- UI\components\structures_list_panel.py - 11
- services\pricing_execution_query_service.py - 10
- tools\patch_structure_side_panel.py - 10
- ATT\tests\test_pricing_execution_query_service.py - 9
- ATT\tests\test_orchestrator_run_methods.py - 7
- ATT\tests\test_structure_editor_integration.py - 6
- services\derived_payoff_persistence.py - 5
- ATT\tests\test_decision.py - 5
- ATT\tests\test_structure_events_repository.py - 5
- db\writer.py - 4

### 7.x. tabela_listagem

- UI\components\terminal_vwap_payoff_dark_panel.py - 104
- UI\components\details_panel.py - 81
- UI\models\ui_data.py - 60
- scripts\purge_derived_snapshots.py - 50
- infra\bootstrap_rtd_option_quotes_schema.py - 39
- db\derived_repo.py - 34
- UI\components\terminal_vwap_payoff_panel.py - 34
- UI\components\decisions_grid.py - 29
- db\import_excel.py - 22
- db\reader.py - 21
- tools\audit_rtd_ui_flow.py - 18
- ATT\tests\test_system_snapshots_schema.py - 18
- UI\main_window.py - 17
- UI\components\structures_list_panel.py - 17
- reports\terminal_vwap_recovery\main_window_terminal_old.py - 17
- scripts\import_rtd_option_quotes_wide_csv.py - 16
- reports\terminal_vwap_recovery\main_window_good_85dfbcd.py - 16
- ATT\tests\conftest.py - 16
- UI\modern\main_window.py - 14
- ATT\tests\test_market_snapshot_repository_rtd_option_quotes.py - 12
- infra\bootstrap_structures_schema.py - 11
- services\canonical_pricing_facade.py - 11
- UI\components\structure_editor_dialog.py - 11
- db\migrations\add_structure_id_to_payoff_curve_points.py - 11
- scripts\check_rota_desenvolvimento.py - 10
- repositories\pricing_executions_repository.py - 9
- ATT\tests\test_structure_editor_integration.py - 9
- validate_db.py - 7
- db\schema.py - 7
- scripts\validate_derived_db.py - 6

### 7.x. selecao

- UI\components\terminal_vwap_payoff_dark_panel.py - 93
- reports\terminal_vwap_recovery\main_window_good_85dfbcd.py - 71
- services\canonical_pricing_facade.py - 63
- UI\main_window.py - 63
- reports\terminal_vwap_recovery\main_window_terminal_old.py - 63
- tools\patch_structure_side_panel.py - 54
- ATT\tests\test_canonical_pricing_facade.py - 53
- UI\components\structures_list_panel.py - 45
- UI\components\structure_editor_dialog.py - 43
- ATT\tests\test_structures_legs_endpoints.py - 43
- UI\components\decisions_grid.py - 42
- services\derived_payoff_persistence.py - 40
- ATT\tests\test_structures_repository.py - 37
- repositories\structures_repository.py - 34
- ATT\tests\test_structure_editor_dialog.py - 32
- UI\components\terminal_vwap_payoff_panel.py - 31
- UI\models\ui_data.py - 30
- services\derived_service.py - 29
- UI\modern\main_window.py - 29
- ATT\tests\test_structures_archive_wiring.py - 29
- ATT\tests\test_structure_editor_integration.py - 28
- services\pricing_execution_persistence_service.py - 27
- ATT\tests\test_pricing_input_service.py - 27
- repositories\pricing_executions_repository.py - 20
- services\market_snapshot_selector.py - 20
- ATT\tests\test_pricing_execution_persistence_service.py - 20
- ATT\tests\test_pricing_execution_service.py - 20
- ATT\tests\test_structures_api.py - 20
- ATT\tests\test_pricing_payload_adapter.py - 19
- services\canonical_input_service.py - 18

### 7.x. detalhe_rationale_why

- db\derived_repo.py - 263
- UI\components\details_panel.py - 185
- UI\models\ui_data.py - 177
- reports\terminal_vwap_recovery\main_window_good_85dfbcd.py - 147
- ATT\tests\test_structures_api.py - 146
- repositories\system_snapshots_repository.py - 132
- domain\decision.py - 103
- UI\components\terminal_vwap_payoff_dark_panel.py - 99
- services\calculation_orchestrator.py - 91
- domain\payoff_features.py - 88
- db\reader.py - 87
- ATT\tests\test_structures_legs_endpoints.py - 86
- services\derived_service.py - 82
- ATT\tests\test_structure_editor_integration.py - 81
- UI\main_window.py - 76
- reports\terminal_vwap_recovery\main_window_terminal_old.py - 76
- ATT\tests\test_system_snapshots_repository.py - 72
- repositories\structures_repository.py - 65
- UI\modern\main_window.py - 65
- ATT\tests\test_structure_analysis_service.py - 65
- ATT\tests\test_structure_events_api.py - 60
- ATT\tests\test_payoff_chart.py - 56
- UI\components\payoff_chart.py - 53
- UI\components\structure_editor_dialog.py - 47
- ATT\tests\test_orchestrator_run_methods.py - 45
- scripts\refresh_rtd_symbol_to_option_quotes.py - 44
- UI\components\decisions_grid.py - 42
- db\writer.py - 41
- api\structures_controller.py - 40
- domain\payoff.py - 40

### 7.x. camadas_servicos

- ATT\tests\test_structure_analysis_service.py - 310
- ATT\tests\test_structure_events_api.py - 283
- ATT\tests\test_pricing_execution_query_service.py - 240
- api\structures_controller.py - 204
- ATT\tests\test_structure_events_repository.py - 200
- ATT\tests\test_structure_events_service.py - 183
- services\structure_events_service.py - 181
- ATT\tests\test_pricing_execution_controller.py - 176
- ATT\tests\test_pricing_execution_persistence_service.py - 154
- ATT\tests\test_structure_events_effective_state.py - 150
- repositories\structure_events_repository.py - 146
- ATT\tests\test_pricing_execution_app_service.py - 142
- services\canonical_input_service.py - 132
- db\derived_repo.py - 122
- UI\components\details_panel.py - 107
- ATT\tests\test_pricing_input_service.py - 96
- ATT\tests\test_canonical_input_service.py - 94
- UI\main_window.py - 78
- reports\terminal_vwap_recovery\main_window_terminal_old.py - 78
- ATT\tests\test_terminal_vwap_payoff_controller.py - 78
- UI\modern\main_window.py - 76
- ATT\tests\test_pricing_execution_orchestration_service.py - 76
- ATT\tests\test_terminal_vwap_payoff_app_service.py - 74
- services\pricing_execution_orchestration_service.py - 68
- reports\terminal_vwap_recovery\main_window_good_85dfbcd.py - 65
- services\terminal_vwap_payoff_app_service.py - 58
- services\canonical_pricing_facade.py - 56
- ATT\tests\test_structure_leg_rtd_enrichment_service.py - 48
- tools\audit_rtd_ui_flow.py - 46
- services\pricing_execution_persistence_service.py - 44


## 8. Leitura preliminar

Esta etapa deve ser interpretada como inventario tecnico, nao como validacao funcional.

A equivalencia funcional so podera ser declarada apos:

- leitura dos pontos encontrados
- comparacao com a UI atual auditada
- identificacao do arquivo alvo
- definicao do menor patch seguro
- validacao manual posterior

## 9. Lacunas a confirmar

- confirmar se o modo dark possui filtros reais de decisoes
- confirmar se o modo dark possui tabela/listagem de decisoes
- confirmar se ha selecao de decisao conectada a dados reais
- confirmar se detalhe, rationale e why JSON existem no fluxo moderno
- confirmar se ha servico/controller existente reutilizavel
- confirmar se alguma funcionalidade esta apenas na UI atual ou no shell temporario

## 10. Decisao

Nenhum patch funcional deve ser aplicado antes da leitura deste inventario.

A proxima etapa recomendada e classificar as lacunas encontradas e escolher o menor patch seguro para decisoes no modo dark.
