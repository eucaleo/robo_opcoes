# Classificacao das lacunas de decisoes no modo dark

Data de referencia: 2026-07-02

## 1. Objetivo

Classificar as lacunas encontradas no inventario dirigido de decisoes, filtros e tabela no modo dark.

Relatorio base:

- reports/ui_modern_equivalence/11_inventario_decisoes_filtros_tabela_dark.md

## 2. Restricoes

- esta etapa nao altera codigo funcional
- esta etapa nao altera banco
- esta etapa nao altera regra de negocio
- esta etapa nao troca entrypoint
- a UI atual permanece preservada
- o modo dark permanece paralelo

## 3. Matriz de presenca tecnica

| Funcao/Componente | dark_window | modern_shell | UI atual | dark_panel | Componente dedicado |
|---|---:|---:|---:|---:|---:|
| FiltersPanel | nao | sim | sim | nao | sim |
| DecisionsGrid | nao | sim | sim | nao | sim |
| DetailsPanel | nao | sim | sim | nao | sim |
| get_decisions | nao | sim | sim | nao | sim |
| on_decision_selected | nao | sim | sim | nao | sim |
| rationale_why | nao | nao | nao | nao | sim |
| payoff_por_decisao | sim | sim | sim | sim | sim |
| recalcular | nao | sim | sim | sim | sim |

## 4. Classificacao funcional

| Item obrigatorio da auditoria | Status no modo dark | Evidencia | Decisao |
|---|---|---|---|
| filtros de decisoes | ausente | dark_window nao possui FiltersPanel nem termos de filtro | reaproveitar FiltersPanel existente |
| tabela/listagem de decisoes | ausente | dark_window nao possui DecisionsGrid nem tabela de decisoes | reaproveitar DecisionsGrid existente |
| selecao de decisoes | ausente | dark_window nao possui on_decision_selected | reaproveitar fluxo do modern_shell |
| detalhamento de decisao | ausente | dark_window nao possui DetailsPanel | reaproveitar DetailsPanel existente |
| rationale/why JSON | ausente no dark | evidencias concentradas fora do dark_window | reaproveitar painel de detalhes existente |
| payoff por decisao | ausente como fluxo de decisao no dark | payoff existe no terminal/painel, mas nao por selecao de decisao | integrar depois de filtros/tabela/detalhe |
| recalcular estrutura a partir de decisao | ausente no dark | fluxo existe no shell/UI atual | nao implementar nesta primeira fatia se aumentar risco |

## 5. Componentes candidatos a reaproveitamento

### 5.x. UI\components\decisions_grid.py

Classes:

- DecisionsGrid

Metodos:

- __init__
- _setup_treeview
- _setup_scrollbars
- _on_tree_select
- update_data
- _format_timestamp
- _format_ratio
- _format_currency
- get_current_data
- get_selected_decision
- select_by_key

### 5.x. UI\components\filters_panel.py

Classes:

- FiltersPanel

Metodos:

- __init__
- _setup_widgets
- _bind_events
- _apply_filters
- reset_filters
- update_structures

### 5.x. UI\components\details_panel.py

Classes:

- DetailsPanel

Metodos:

- __init__
- _set_recalc_ui_state
- _derived_db_path
- _operational_app_db_path
- _resolve_structure_key
- _get_latest_snapshot_timestamp_for_structure
- _compute_recalc_signature
- _setup_widgets
- update_decision
- update_breakevens
- update_audit_info
- clear
- on_recalc_finished
- _clear_operational_state
- update_operational_state
- _fetch_effective_structure_local
- _refresh_operational_state_for_structure
- _format_currency_label
- _fetch_latest_decision_from_derived
- _fetch_payoff_points_from_derived
- _fetch_audit_info_from_derived
- _compute_breakevens_from_points
- _compute_pl_at_spot
- _refresh_current_from_derived
- _on_recalculate_click
- _safe_path
- _looks_like_db_path
- q
- table_names
- columns_for
- looks_like_structure_col
- timestamp_score
- latest_in_table


## 6. Evidencias principais no shell moderno

### 6.x. FiltersPanel

- L22: from UI.components.filters_panel import FiltersPanel
- L206: self.filters_panel = FiltersPanel(

### 6.x. DecisionsGrid

- L20: from UI.components.decisions_grid import DecisionsGrid
- L212: self.decisions_grid = DecisionsGrid(

### 6.x. DetailsPanel

- L21: from UI.components.details_panel import DetailsPanel
- L224: self.details_panel = DetailsPanel(
- L343: self.details_panel.update_decision(decision_data)
- L526: self.details_panel.update_decision(previous)

### 6.x. get_decisions

- L329: filtered_data = self.data_model.get_decisions(filters)
- L509: decisions = self.data_model.get_decisions()

### 6.x. on_decision_selected

- L214: on_selection_change=self.on_decision_selected,
- L336: def on_decision_selected(self, decision_data: Dict) -> None:

### 6.x. payoff_por_decisao

- L23: from UI.components.payoff_chart import PayoffChart
- L53: self._payoff_worker_id = 0
- L54: self._loading_payoff = False
- L232: detail_notebook.add(chart_frame, text="Curva de payoff")
- L234: self.payoff_chart = PayoffChart(chart_frame)
- L235: self.payoff_chart.pack(fill="both", expand=True, padx=4, pady=4)
- L269: notebook.add(tab, text="Terminal VWAP Payoff")
- L272: from controllers.terminal_vwap_payoff_controller import (
- L273: TerminalVWAPPayoffController,
- L276: from services.terminal_vwap_payoff_app_service import (
- L277: TerminalVWAPPayoffAppService,
- L279: from UI.components.terminal_vwap_payoff_panel import TerminalVWAPPayoffPanel
- L282: app_service = TerminalVWAPPayoffAppService(
- L285: controller = TerminalVWAPPayoffController(app_service)
- L287: self.terminal_vwap_payoff_panel = TerminalVWAPPayoffPanel(
- L292: self.terminal_vwap_payoff_panel.pack(
- L303: "Terminal VWAP Payoff indisponível neste shell.\n\n"
- L322: # Decisões / filtros / payoff
- L351: self._start_payoff_load(structure_id, timestamp, decision_data)
- L353: self.payoff_chart.clear()
- L354: self.set_status("Dados insuficientes para carregar payoff")
- L356: def _start_payoff_load(
- L365: self._payoff_worker_id += 1
- L366: worker_id = self._payoff_worker_id
- L367: self._loading_payoff = True


## 7. Menor patch seguro recomendado

Patch recomendado em fatia unica pequena:

- adicionar uma area de decisoes no modo dark sem substituir a UI atual
- reaproveitar FiltersPanel, DecisionsGrid e DetailsPanel se compativeis com o container atual
- consumir o mesmo data_model ou contrato usado pelo modern_shell
- carregar lista inicial de decisoes
- aplicar filtros via get_decisions(filters)
- ao selecionar decisao, preencher DetailsPanel
- manter payoff por decisao fora da primeira fatia se a integracao exigir alteracao maior

## 8. Arquivos alvo provaveis

Arquivos provaveis para a primeira fatia:

- UI/modern/dark_window.py
- possivelmente UI/modern/theme.py apenas se houver necessidade visual

Arquivos a evitar nesta primeira fatia:

- repositories
- services
- controllers
- scripts de banco
- contratos canonicos

## 9. Validacoes obrigatorias apos patch futuro

- python -m py_compile UI/modern/__main__.py UI/modern/app.py UI/modern/theme.py UI/modern/dark_window.py UI/components/terminal_vwap_payoff_dark_panel.py
- python -m UI.modern --info
- python -m UI.modern
- validacao manual de filtros, tabela, selecao e detalhe de decisao

## 10. Decisao

O modo dark ainda nao possui equivalencia funcional de decisoes.

A proxima etapa autorizada pode ser um patch funcional minimo para adicionar filtros, tabela e detalhe de decisoes no modo dark, reaproveitando componentes existentes e sem criar regra de negocio nova.
