# UI/components/decisions_dark_panel.py
"""
Painel DARK minimo para listagem global de decisoes.

Escopo intencionalmente pequeno:
- usa UIDataModel.get_decisions();
- lista decisoes em CustomTkinter;
- permite selecao;
- mostra detalhe textual;
- nao altera banco;
- nao substitui os componentes ttk existentes.
"""

from __future__ import annotations
from dataclasses import dataclass

import csv
import json
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from tkinter import filedialog, messagebox

import customtkinter as ctk



@dataclass(frozen=True)
class _DecisionFilterState:
    raw_search: str
    terms: List[str]
    level_min: Optional[float]
    level_min_valid: bool
    dte_max: Optional[float]
    dte_max_valid: bool

    @property
    def has_invalid_numeric_filter(self) -> bool:
        return not self.level_min_valid or not self.dte_max_valid


class DecisionsDarkPanel(ctk.CTkFrame):
    """
    Listagem global minima de decisoes para o modo dark.
    """

    def __init__(
        self,
        parent,
        data_model,
        on_status: Optional[Callable[[str], None]] = None,
        on_load_structure: Optional[Callable[[Any], None]] = None,
        get_structures: Optional[Callable[[], List[Dict[str, Any]]]] = None,
        app_service=None,
    ) -> None:
        super().__init__(parent, fg_color="#0f172a")

        self.data_model = data_model
        self.on_status = on_status
        self.on_load_structure = on_load_structure
        self.app_service = app_service
        self.get_structures = get_structures
        self.decisions: List[Dict[str, Any]] = []
        self.filtered_decisions: List[Dict[str, Any]] = []
        self.structure_index: Dict[str, Dict[str, Any]] = {}
        self.active_structure_ids: set[str] = set()
        self.selected_index: Optional[int] = None
        self._last_decision_status_text: Optional[str] = None
        self._last_filter_status_text: Optional[str] = None
        self._row_buttons: List[ctk.CTkButton] = []

        self._build_layout()

        self.after(100, self.reload_decisions)

    def _status(self, message: str) -> None:
        if self.on_status:
            self.on_status(message)

    def _build_layout(self) -> None:
        self._configure_layout_grid()
        header = self._build_header_frame()
        self._build_header_actions(header)
        self._build_search_section(header)
        self._build_filters_section(header)
        self._build_list_section()
        self._build_detail_section()

    def _configure_layout_grid(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)

    def _build_header_frame(self) -> ctk.CTkFrame:
        header = ctk.CTkFrame(self, fg_color="#111827")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 6))
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)
        header.grid_columnconfigure(2, weight=0)
        header.grid_columnconfigure(3, weight=0)

        title = ctk.CTkLabel(
            header,
            text="Decisões globais",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#f9fafb",
        )
        title.grid(row=0, column=0, sticky="w", padx=12, pady=10)

        return header

    def _build_header_actions(self, header: ctk.CTkFrame) -> None:
        self.load_structure_btn = ctk.CTkButton(
            header,
            text="Carregar estrutura no Terminal",
            width=210,
            state="disabled",
            command=self._load_selected_structure,
        )
        self.load_structure_btn.grid(row=0, column=1, sticky="e", padx=(8, 4), pady=10)

        export_csv_btn = ctk.CTkButton(
            header,
            text="Exportar CSV",
            width=120,
            fg_color="#166534",
            hover_color="#15803d",
            command=self._export_filtered_csv,
        )
        export_csv_btn.grid(row=0, column=2, sticky="e", padx=(4, 4), pady=10)

        refresh_btn = ctk.CTkButton(
            header,
            text="Atualizar",
            width=120,
            command=self.reload_decisions,
        )
        refresh_btn.grid(row=0, column=3, sticky="e", padx=(4, 12), pady=10)

    def _build_search_section(self, header: ctk.CTkFrame) -> None:
        self.search_entry = ctk.CTkEntry(
            header,
            placeholder_text="Buscar por decisão, ID ou nome da estrutura ativa...",
            height=32,
        )
        self.search_entry.grid(
            row=1,
            column=0,
            columnspan=4,
            sticky="ew",
            padx=(12, 12),
            pady=(0, 10),
        )
        self.search_entry.bind("<KeyRelease>", self._on_search_changed)

    def _build_filters_section(self, header: ctk.CTkFrame) -> None:
        filters_frame = ctk.CTkFrame(header, fg_color="#0f172a")
        filters_frame.grid(row=2, column=0, columnspan=4, sticky="ew", padx=12, pady=(0, 10))
        filters_frame.grid_columnconfigure(6, weight=1)

        self._build_level_filter_controls(filters_frame)
        self._build_dte_filter_controls(filters_frame)
        self._build_filter_action_buttons(filters_frame)
        self._build_filter_summary(filters_frame)

    def _build_level_filter_controls(self, filters_frame: ctk.CTkFrame) -> None:
        level_filter_label = ctk.CTkLabel(
            filters_frame,
            text="Level mín.",
            text_color="#d1d5db",
        )
        level_filter_label.grid(row=0, column=0, sticky="w", padx=(10, 4), pady=8)

        self.level_min_filter_entry = ctk.CTkEntry(
            filters_frame,
            placeholder_text="mín.",
            height=30,
            width=70,
        )
        self.level_min_filter_entry.grid(row=0, column=1, sticky="w", padx=(0, 8), pady=8)
        self.level_min_filter_entry.bind("<Return>", self._apply_advanced_filters)

    def _build_dte_filter_controls(self, filters_frame: ctk.CTkFrame) -> None:
        dte_filter_label = ctk.CTkLabel(
            filters_frame,
            text="DTE máx.",
            text_color="#d1d5db",
        )
        dte_filter_label.grid(row=0, column=2, sticky="w", padx=(0, 4), pady=8)

        self.dte_max_filter_entry = ctk.CTkEntry(
            filters_frame,
            placeholder_text="máx.",
            height=30,
            width=70,
        )
        self.dte_max_filter_entry.grid(row=0, column=3, sticky="w", padx=(0, 8), pady=8)
        self.dte_max_filter_entry.bind("<Return>", self._apply_advanced_filters)

    def _build_filter_action_buttons(self, filters_frame: ctk.CTkFrame) -> None:
        apply_filters_btn = ctk.CTkButton(
            filters_frame,
            text="Aplicar",
            width=90,
            height=30,
            command=self._apply_advanced_filters,
        )
        apply_filters_btn.grid(row=0, column=4, sticky="e", padx=(0, 6), pady=8)

        clear_filters_btn = ctk.CTkButton(
            filters_frame,
            text="Limpar tudo",
            width=110,
            height=30,
            fg_color="#374151",
            hover_color="#4b5563",
            command=self._clear_advanced_filters,
        )
        clear_filters_btn.grid(row=0, column=5, sticky="e", padx=(0, 8), pady=8)

    def _build_filter_summary(self, filters_frame: ctk.CTkFrame) -> None:
        self.filter_summary_label = ctk.CTkLabel(
            filters_frame,
            text="Filtros: sem dados carregados.",
            text_color="#9ca3af",
            anchor="e",
        )
        self.filter_summary_label.grid(row=0, column=6, sticky="e", padx=(0, 10), pady=8)

    def _build_list_section(self) -> None:
        self.list_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#020617",
            label_text="Listagem",
            label_text_color="#e5e7eb",
        )
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=(0, 10))

    def _build_detail_section(self) -> None:
        detail_frame = self._create_detail_frame()
        self._create_detail_title(detail_frame)
        self._create_copy_detail_button(detail_frame)
        self._create_details_textbox(detail_frame)
        self._set_detail_text("Nenhuma decisão selecionada.")

    def _create_detail_frame(self):
        detail_frame = ctk.CTkFrame(self, fg_color="#020617")
        detail_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=(0, 10))
        detail_frame.grid_columnconfigure(0, weight=1)
        detail_frame.grid_columnconfigure(1, weight=0)
        detail_frame.grid_rowconfigure(1, weight=1)
        return detail_frame

    def _create_detail_title(self, detail_frame) -> None:
        detail_title = ctk.CTkLabel(
            detail_frame,
            text="Detalhe da decisão selecionada",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#f9fafb",
        )
        detail_title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

    def _create_copy_detail_button(self, detail_frame) -> None:
        self.copy_detail_btn = ctk.CTkButton(
            detail_frame,
            text="Copiar detalhe",
            width=130,
            height=30,
            fg_color="#374151",
            hover_color="#4b5563",
            state="disabled",
            command=self._copy_selected_detail,
        )
        self.copy_detail_btn.grid(row=0, column=1, sticky="e", padx=(4, 12), pady=(12, 6))

    def _create_details_textbox(self, detail_frame) -> None:
        self.details_text = ctk.CTkTextbox(
            detail_frame,
            fg_color="#0f172a",
            text_color="#e5e7eb",
            border_width=1,
            border_color="#1f2937",
            wrap="word",
        )
        self.details_text.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=12,
            pady=(0, 12),
        )

    def reload_decisions(self) -> None:
        try:
            self._load_decisions_from_model()
            self._prepare_reloaded_decisions_view()
            self._render_reloaded_decisions_state()
        except Exception as exc:
            self._handle_decisions_load_error(exc)
    def _load_decisions_from_model(self) -> None:
        if self.app_service is not None:
            self.decisions = self.app_service.list_decisions()
            return

        if hasattr(self.data_model, "refresh"):
            self.data_model.refresh()

        decisions = self.data_model.get_decisions()
        self.decisions = list(decisions or [])
        self._refresh_structure_index()
        self._apply_filter(render=False)
        self._render_rows()

    def _render_reloaded_decisions_state(self) -> None:
        if self.filtered_decisions:
            self._render_reloaded_filtered_decisions_state()
            return

        if self.decisions:
            self._render_reloaded_empty_filter_state()
            return

        self._render_reloaded_empty_decisions_state()

    def _render_reloaded_filtered_decisions_state(self) -> None:
        self._select_decision(0, notify_status=False)

        if len(self.filtered_decisions) == len(self.decisions):
            self._status(f"{len(self.decisions)} decisões carregadas no modo dark")
            return

        self._status_filter_result(
            f"{len(self.filtered_decisions)} de {len(self.decisions)} decisões exibidas"
        )

    def _render_reloaded_empty_filter_state(self) -> None:
        self.load_structure_btn.configure(state="disabled")
        self._set_detail_text("Nenhuma decisão encontrada para o filtro atual.")
        self._status_filter_result(
            f"Filtro sem resultados: 0 de {len(self.decisions)} decisões exibidas"
        )

    def _render_reloaded_empty_decisions_state(self) -> None:
        self.load_structure_btn.configure(state="disabled")
        self._set_detail_text("Nenhuma decisão encontrada.")
        self._status("Nenhuma decisão encontrada no modo dark")

    def _handle_decisions_load_error(self, exc: Exception) -> None:
        self.decisions = []
        self.filtered_decisions = []
        self.structure_index = {}
        self.active_structure_ids = set()
        self._clear_selection()
        self._render_rows()
        self._set_detail_text(f"Erro ao carregar decisões:\n\n{exc}")
        self._status(f"Erro ao carregar decisões: {exc}")

    def _render_rows(self) -> None:
        self._clear_list_rows()

        if self._render_empty_rows_message_if_needed():
            return

        visible = self.filtered_decisions[:300]
        self._render_visible_rows(visible)
        self._render_more_rows_notice(len(visible))

    def _clear_list_rows(self) -> None:
        for child in self.list_frame.winfo_children():
            child.destroy()

        self._row_buttons = []

    def _render_empty_rows_message_if_needed(self) -> bool:
        if self.filtered_decisions:
            return False

        empty_text = "Nenhuma decisão disponível."
        if self.decisions:
            empty_text = "Nenhuma decisão encontrada para o filtro atual."

        empty = ctk.CTkLabel(
            self.list_frame,
            text=empty_text,
            text_color="#9ca3af",
        )
        empty.pack(fill="x", padx=8, pady=8)
        return True

    def _render_visible_rows(self, visible) -> None:
        for index, decision in enumerate(visible):
            btn = self._build_decision_row(decision, index)
            btn.pack(fill="x", padx=6, pady=3)
            self._row_buttons.append(btn)

    def _build_decision_row(self, decision, index: int) -> ctk.CTkButton:
        return ctk.CTkButton(
            self.list_frame,
            text=self._format_row(decision, index),
            anchor="w",
            height=44,
            fg_color="#111827",
            hover_color="#1f2937",
            text_color="#e5e7eb",
            command=lambda i=index: self._select_decision(i),
        )

    def _render_more_rows_notice(self, visible_count: int) -> None:
        if len(self.filtered_decisions) <= visible_count:
            return

        more = ctk.CTkLabel(
            self.list_frame,
            text=f"Exibindo 300 de {len(self.filtered_decisions)} decisões filtradas.",
            text_color="#fbbf24",
        )
        more.pack(fill="x", padx=8, pady=8)

    def _on_search_changed(self, _event=None) -> None:
        self._apply_filter(render=True)


    def _apply_advanced_filters(self, _event=None) -> None:
        self._apply_filter(render=True)

    def _clear_advanced_filters(self) -> None:
        for attr in (
            "search_entry",
            "level_min_filter_entry",
            "dte_max_filter_entry",
        ):
            widget = getattr(self, attr, None)
            if widget is None:
                continue

            try:
                widget.delete(0, "end")
            except Exception:
                continue

        self._apply_filter(render=True, announce_clear=True)

    def _entry_text(self, attr: str) -> str:
        widget = getattr(self, attr, None)
        if widget is None:
            return ""

        return widget.get().strip()

    def _parse_float_filter(self, attr: str) -> tuple[Optional[float], bool]:
        raw_value = self._entry_text(attr)
        if not raw_value:
            return None, True

        try:
            return float(raw_value.replace(",", ".")), True
        except ValueError:
            return None, False

    def _coerce_float(self, value: Any) -> Optional[float]:
        if value is None:
            return None

        if isinstance(value, (int, float)):
            return float(value)

        text = str(value).strip()
        if not text:
            return None

        try:
            return float(text.replace(",", "."))
        except ValueError:
            return None

    def _decision_numeric_value(self, decision: Dict[str, Any], *keys: str) -> Optional[float]:
        for key in keys:
            number = self._coerce_float(decision.get(key))
            if number is not None:
                return number

        return None

    def _update_filter_summary(
        self,
        visible_count: int,
        active_count: int,
        error: Optional[str] = None,
    ) -> None:
        if not hasattr(self, "filter_summary_label"):
            return

        if error:
            self._show_filter_summary_error(error)
            return

        self._show_filter_summary_counts(visible_count, active_count)

    def _show_filter_summary_error(self, error: str) -> None:
        self.filter_summary_label.configure(
            text=f"Filtros inválidos: {error}",
            text_color="#fca5a5",
        )

    def _show_filter_summary_counts(self, visible_count: int, active_count: int) -> None:
        self.filter_summary_label.configure(
            text=self._filter_summary_text(visible_count, active_count),
            text_color="#9ca3af",
        )

    def _filter_summary_text(self, visible_count: int, active_count: int) -> str:
        return (
            f"Exibindo {visible_count} de {active_count} decisões ativas "
            f"({len(self.decisions)} totais) — {self._filter_summary_suffix()}."
        )

    def _filter_summary_suffix(self) -> str:
        active_filters = self._active_filter_summary_labels()

        if not active_filters:
            return "sem filtros avançados"

        return "filtros: " + ", ".join(active_filters)

    def _active_filter_summary_labels(self) -> List[str]:
        active_filters = []

        if self._entry_text("search_entry"):
            active_filters.append("busca")

        if self._entry_text("level_min_filter_entry"):
            active_filters.append("level mín.")

        if self._entry_text("dte_max_filter_entry"):
            active_filters.append("DTE máx.")

        return active_filters

    def _refresh_structure_index(self) -> None:
        """
        Monta indice local de estruturas para:
        - filtrar somente decisoes de estruturas ativas;
        - permitir busca por ID ou nome da estrutura.
        """
        structures = self._load_structures_for_decision_filter()
        self._reset_structure_filter_index()
        self._index_structures_for_decision_filter(structures)
        self._apply_decision_structure_fallback_if_needed(structures)

    def _load_structures_for_decision_filter(self) -> List[Dict[str, Any]]:
        if not self.get_structures:
            return []

        try:
            return list(self.get_structures() or [])
        except Exception as exc:
            self._status(f"Erro ao carregar estruturas para filtro de decisões: {exc}")
            return []

    def _reset_structure_filter_index(self) -> None:
        self.structure_index = {}
        self.active_structure_ids = set()

    def _index_structures_for_decision_filter(self, structures: List[Dict[str, Any]]) -> None:
        for structure in structures:
            structure_id = self._structure_filter_id(structure)

            if structure_id is None:
                continue

            key = str(structure_id)
            self.structure_index[key] = structure

            if self._is_active_structure(structure):
                self.active_structure_ids.add(key)

    def _structure_filter_id(self, structure: Dict[str, Any]) -> Any:
        structure_id = structure.get("id")

        if structure_id is not None:
            return structure_id

        return structure.get("structure_id") or structure.get("aba")

    def _apply_decision_structure_fallback_if_needed(
        self,
        structures: List[Dict[str, Any]],
    ) -> None:
        # Fallback seguro: se nao houver informacao de estruturas, nao bloqueia a lista.
        if structures:
            return

        self.active_structure_ids = {
            str(decision.get("structure_id") or decision.get("aba"))
            for decision in self.decisions
            if decision.get("structure_id") is not None or decision.get("aba") is not None
        }

    def _is_active_structure(self, structure: Dict[str, Any]) -> bool:
        """
        Heuristica defensiva para identificar estrutura ativa sem depender
        de um unico nome de campo.
        """
        active_flag_key = self._active_structure_flag_key(structure)

        if active_flag_key is not None:
            return self._is_enabled_active_flag(structure.get(active_flag_key))

        status = self._structure_status_value(structure)

        if status:
            return not self._is_inactive_structure_status(status)

        # Se nao houver campo de status, assume ativa para preservar compatibilidade.
        return True

    def _active_structure_flag_key(self, structure: Dict[str, Any]) -> Any:
        for key in ("active", "is_active", "ativo", "enabled"):
            if key in structure:
                return key

        return None

    def _is_enabled_active_flag(self, value: Any) -> bool:
        if isinstance(value, str):
            normalized = value.strip().lower()
            return normalized not in self._inactive_active_flag_values()

        return bool(value)

    def _inactive_active_flag_values(self) -> set:
        return {"0", "false", "falso", "no", "nao", "não"}

    def _structure_status_value(self, structure: Dict[str, Any]) -> str:
        status = (
            structure.get("status")
            or structure.get("state")
            or structure.get("situacao")
            or structure.get("situação")
            or ""
        )
        return str(status).strip().lower() if status else ""

    def _is_inactive_structure_status(self, status: str) -> bool:
        inactive_values = {
            "inactive",
            "inativo",
            "inativa",
            "closed",
            "fechado",
            "fechada",
            "encerrado",
            "encerrada",
            "finalizado",
            "finalizada",
            "archived",
            "arquivado",
            "arquivada",
            "deleted",
            "removido",
            "removida",
            "cancelado",
            "cancelada",
        }
        return status in inactive_values

    def _free_search_text(self) -> str:
        search_var = getattr(self, "search_var", None)
        if search_var is not None:
            try:
                return str(search_var.get() or "").strip()
            except Exception:
                pass

        for attr in ("search_entry", "search_box", "search_input"):
            widget = getattr(self, attr, None)
            if widget is None:
                continue

            try:
                return str(widget.get() or "").strip()
            except Exception:
                continue

        return ""

    def _current_filter_state(self) -> _DecisionFilterState:
        raw_search = self._free_search_text()
        terms = [term for term in raw_search.lower().split() if term]

        level_min, level_min_valid = self._parse_float_filter("level_min_filter_entry")
        dte_max, dte_max_valid = self._parse_float_filter("dte_max_filter_entry")

        return _DecisionFilterState(
            raw_search=raw_search,
            terms=terms,
            level_min=level_min,
            level_min_valid=level_min_valid,
            dte_max=dte_max,
            dte_max_valid=dte_max_valid,
        )

    def _active_structure_decisions(self) -> List[Dict[str, Any]]:
        return [
            decision
            for decision in self.decisions
            if self._decision_structure_id(decision) in self.active_structure_ids
        ]

    def _filter_validation_error(self, state: _DecisionFilterState) -> Optional[str]:
        invalid_filters = []

        if not state.level_min_valid:
            invalid_filters.append("level mín.")

        if not state.dte_max_valid:
            invalid_filters.append("DTE máx.")

        if not invalid_filters:
            return None

        if len(invalid_filters) == 1:
            return f"{invalid_filters[0]} inválido"

        return f"{' e '.join(invalid_filters)} inválidos"

    def _filter_decisions(
        self,
        decisions: List[Dict[str, Any]],
        state: _DecisionFilterState,
    ) -> List[Dict[str, Any]]:
        filtered = list(decisions)

        if state.terms:
            filtered = self._filter_by_search_terms(filtered, state.terms)

        if state.level_min is not None:
            filtered = self._filter_by_level_min(filtered, state.level_min)

        if state.dte_max is not None:
            filtered = self._filter_by_dte_max(filtered, state.dte_max)

        return filtered

    def _filter_by_search_terms(
        self,
        decisions: List[Dict[str, Any]],
        terms: List[str],
    ) -> List[Dict[str, Any]]:
        return [
            decision
            for decision in decisions
            if self._decision_matches_filter(decision, terms)
        ]


    def _filter_by_level_min(
        self,
        decisions: List[Dict[str, Any]],
        level_min: float,
    ) -> List[Dict[str, Any]]:
        filtered = []

        for decision in decisions:
            value = self._decision_numeric_value(decision, "level", "nivel", "nível")
            if value is not None and value >= level_min:
                filtered.append(decision)

        return filtered

    def _filter_by_dte_max(
        self,
        decisions: List[Dict[str, Any]],
        dte_max: float,
    ) -> List[Dict[str, Any]]:
        filtered = []

        for decision in decisions:
            value = self._decision_numeric_value(decision, "dte_min", "dte", "DTE")
            if value is not None and value <= dte_max:
                filtered.append(decision)

        return filtered

    def _show_empty_filter_result(self, active_decisions: List[Dict[str, Any]]) -> None:
        if active_decisions:
            self._set_detail_text("Nenhuma decisão encontrada para o filtro atual.")
            self._status_filter_result(
                f"Filtro sem resultados: 0 de {len(active_decisions)} decisões de estruturas ativas"
            )
            return

        self._set_detail_text("Nenhuma decisão de estrutura ativa encontrada.")
        self._status_filter_result("Nenhuma decisão de estrutura ativa encontrada no modo dark")

    def _apply_filter(self, render: bool = True, announce_clear: bool = False) -> None:
        state = self._current_filter_state()
        self._clear_selection()

        active_decisions = self._active_structure_decisions()
        error_text = self._filter_validation_error(state)

        if error_text:
            self._apply_invalid_filter_state(error_text, active_decisions, render)
            return

        self._apply_valid_filter_state(state, active_decisions)

        if render:
            self._render_filter_result(active_decisions, announce_clear)

    def _apply_invalid_filter_state(
        self,
        error_text: str,
        active_decisions: List[Dict[str, Any]],
        render: bool,
    ) -> None:
        self.filtered_decisions = []
        self._update_filter_summary(0, len(active_decisions), error_text)

        if not render:
            return

        self._render_rows()
        self._set_detail_text("Corrija os filtros numéricos para listar decisões.")
        self._status_filter_result(f"Filtro inválido: {error_text}")

    def _apply_valid_filter_state(
        self,
        state: Dict[str, Any],
        active_decisions: List[Dict[str, Any]],
    ) -> None:
        self.filtered_decisions = self._filter_decisions(active_decisions, state)
        self._update_filter_summary(len(self.filtered_decisions), len(active_decisions))

    def _render_filter_result(
        self,
        active_decisions: List[Dict[str, Any]],
        announce_clear: bool,
    ) -> None:
        self._render_rows()

        if self.filtered_decisions:
            self._select_decision(0, notify_status=False)
            self._status_filter_summary(active_decisions, announce_clear)
            return

        self._show_empty_filter_result(active_decisions)

    def _has_active_filters(self) -> bool:
        return any(
            self._entry_text(attr)
            for attr in (
                "search_entry",
                "level_min_filter_entry",
                "dte_max_filter_entry",
            )
        )

    def _status_filter_summary(
        self,
        active_decisions: List[Dict[str, Any]],
        announce_clear: bool,
    ) -> None:
        active_count = len(active_decisions)
        filtered_count = len(self.filtered_decisions)
        active_label = self._active_decisions_label(active_count)

        if self._has_active_filters():
            if filtered_count == active_count:
                self._status_filter_result(
                    f"Filtro aplicado sem reduzir resultados: {active_label}"
                )
            else:
                self._status_filter_result(
                    f"Filtro aplicado: {filtered_count} de {active_label}"
                )
        elif announce_clear:
            self._status_filter_result(f"Filtros limpos: {active_label}")

    def _active_decisions_label(self, count: int) -> str:
        return f"{count} decisões de estruturas ativas"

    def _decision_matches_filter(self, decision: Dict[str, Any], terms: List[str]) -> bool:
        blob = self._decision_search_blob(decision)
        return all(term in blob for term in terms)

    def _decision_structure_id(self, decision: Dict[str, Any]) -> str:
        structure_id = decision.get("structure_id")
        if structure_id is None:
            structure_id = decision.get("aba")
        return str(structure_id)

    def _decision_search_blob(self, decision: Dict[str, Any]) -> str:
        """
        Busca unificada:
        - decisão;
        - ID da estrutura;
        - nome/rotulo/descricao da estrutura.
        """
        structure_id = self._decision_structure_id(decision)
        structure = self.structure_index.get(structure_id, {})
        parts: List[str] = [structure_id]

        self._append_decision_search_values(parts, decision)
        self._append_structure_search_values(parts, structure)

        return " ".join(parts).lower()

    def _append_decision_search_values(self, parts: List[str], decision: Dict[str, Any]) -> None:
        self._append_available_search_values(
            parts,
            decision,
            (
                "decision",
                "decisao",
                "decisão",
                "action",
                "acao",
                "ação",
                "signal",
                "sinal",
            ),
        )

    def _append_structure_search_values(self, parts: List[str], structure: Dict[str, Any]) -> None:
        self._append_available_search_values(
            parts,
            structure,
            (
                "name",
                "nome",
                "label",
                "title",
                "titulo",
                "título",
                "description",
                "descricao",
                "descrição",
                "structure_name",
                "nome_estrutura",
                "estrutura",
            ),
        )

    def _append_available_search_values(
        self,
        parts: List[str],
        source: Dict[str, Any],
        keys: tuple,
    ) -> None:
        for key in keys:
            if key in source and source.get(key) is not None:
                parts.append(str(source.get(key)))

    def _load_selected_structure(self) -> None:
        if self.selected_index is None:
            self._status("Nenhuma decisão selecionada para carregar estrutura")
            return

        if self.selected_index < 0 or self.selected_index >= len(self.filtered_decisions):
            self._status("Seleção de decisão inválida")
            return

        decision = self.filtered_decisions[self.selected_index]
        structure_id = decision.get("structure_id") or decision.get("aba")

        if structure_id is None:
            self._status("Decisão selecionada não possui structure_id")
            return

        if not self.on_load_structure:
            self._status("Carregamento de estrutura não está disponível")
            return

        self.on_load_structure(structure_id)

    def _select_decision(self, index: int, notify_status: bool = True) -> None:
        if not self._is_valid_decision_index(index):
            return

        self.selected_index = index
        self._highlight_selected_decision_row(index)

        decision = self.filtered_decisions[index]
        self._show_selected_decision_detail(decision)
        self._update_load_structure_button_for_decision(decision)
        self.copy_detail_btn.configure(state="normal")

        if notify_status:
            self._status_selected_decision(self._selected_decision_status_text(decision))

    def _is_valid_decision_index(self, index: int) -> bool:
        return 0 <= index < len(self.filtered_decisions)

    def _highlight_selected_decision_row(self, index: int) -> None:
        for i, btn in enumerate(self._row_buttons):
            if i == index:
                btn.configure(fg_color="#2563eb", hover_color="#1d4ed8")
            else:
                btn.configure(fg_color="#111827", hover_color="#1f2937")

    def _show_selected_decision_detail(self, decision: Dict[str, Any]) -> None:
        self._set_detail_text(self._format_detail(decision))

    def _update_load_structure_button_for_decision(self, decision: Dict[str, Any]) -> None:
        structure_id = decision.get("structure_id") or decision.get("aba") or "N/A"

        if structure_id != "N/A" and self.on_load_structure:
            self.load_structure_btn.configure(state="normal")
            return

        self.load_structure_btn.configure(state="disabled")

    def _selected_decision_status_text(self, decision: Dict[str, Any]) -> str:
        structure_id = decision.get("structure_id") or decision.get("aba") or "N/A"
        decision_text = decision.get("decision", "N/A")

        if len(self.filtered_decisions) == len(self.decisions):
            return f"Decisão selecionada: estrutura={structure_id}, decisão={decision_text}"

        return (
            f"Decisão selecionada: estrutura={structure_id}, decisão={decision_text} "
            f"({len(self.filtered_decisions)} de {len(self.decisions)} exibidas)"
        )

    def _clear_selection(self) -> None:
        self.selected_index = None
        self._last_decision_status_text = None

    def _status_selected_decision(self, status_text: str) -> None:
        if status_text == getattr(self, "_last_decision_status_text", None):
            return
        self._last_decision_status_text = status_text
        self._status(status_text)

    def _status_filter_result(self, status_text: str) -> None:
        if status_text == getattr(self, "_last_filter_status_text", None):
            return
        self._last_filter_status_text = status_text
        self._status(status_text)

    def _copy_selected_detail(self) -> None:
        selected_index = self._valid_selected_index()

        if selected_index is None:
            self._status("Nenhuma decisão selecionada para copiar")
            return

        detail_text = self.details_text.get("1.0", "end").strip()
        if not detail_text:
            self._status("Detalhe da decisão selecionada está vazio")
            return

        self.clipboard_clear()
        self.clipboard_append(detail_text)
        self._status("Detalhe da decisão copiado para a área de transferência")

    def _export_filtered_csv(self) -> None:
        if not self._can_export_filtered_csv():
            return

        file_path = self._ask_filtered_csv_path()

        if not file_path:
            self._status("Exportação CSV cancelada")
            return

        try:
            self._write_filtered_csv(file_path)
            self._show_filtered_csv_export_success(file_path)
        except Exception as exc:
            self._show_filtered_csv_export_error(exc)

    def _can_export_filtered_csv(self) -> bool:
        if self.filtered_decisions:
            return True

        self._status("Nenhuma decisão exibida para exportar")
        messagebox.showinfo(
            "Exportar CSV",
            "Não há decisões exibidas para exportar.",
        )
        return False

    def _ask_filtered_csv_path(self) -> str:
        default_name = f"decisoes_dark_filtradas_{datetime.now():%Y%m%d_%H%M%S}.csv"

        return filedialog.asksaveasfilename(
            title="Exportar decisões filtradas",
            defaultextension=".csv",
            initialfile=default_name,
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )

    def _write_filtered_csv(self, file_path: str) -> None:
        with open(file_path, "w", newline="", encoding="utf-8-sig") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self._filtered_csv_fieldnames())
            writer.writeheader()

            for index, decision in enumerate(self.filtered_decisions, start=1):
                writer.writerow(self._decision_export_row(decision, index))

    def _filtered_csv_fieldnames(self) -> List[str]:
        return [
            "export_index",
            "timestamp",
            "created_at",
            "structure_id",
            "structure_name",
            "structure_active",
            "decision",
            "level",
            "dte_min",
            "pl_atual",
            "pl_max",
            "pl_pct_of_max",
            "spot_reference",
            "spot_ref",
            "rationale",
            "why",
            "raw_json",
        ]

    def _show_filtered_csv_export_success(self, file_path: str) -> None:
        total = len(self.filtered_decisions)
        self._status(f"{total} decisões exportadas em CSV")
        messagebox.showinfo(
            "Exportar CSV",
            f"{total} decisões exportadas com sucesso.\n\n{file_path}",
        )

    def _show_filtered_csv_export_error(self, exc: Exception) -> None:
        self._status(f"Erro ao exportar CSV: {exc}")
        messagebox.showerror(
            "Erro ao exportar CSV",
            f"Não foi possível exportar o CSV.\n\n{exc}",
        )

    def _decision_export_row(self, decision: Dict[str, Any], index: int) -> Dict[str, Any]:
        structure_id = decision.get("structure_id")
        if structure_id is None:
            structure_id = decision.get("aba")

        return {
            "export_index": index,
            "timestamp": self._csv_value(decision.get("timestamp")),
            "created_at": self._csv_value(decision.get("created_at")),
            "structure_id": self._csv_value(structure_id),
            "structure_name": self._csv_value(self._structure_name(structure_id)),
            "structure_active": str(self._decision_structure_id(decision) in self.active_structure_ids),
            "decision": self._csv_value(decision.get("decision")),
            "level": self._csv_value(decision.get("level")),
            "dte_min": self._csv_value(decision.get("dte_min")),
            "pl_atual": self._csv_value(decision.get("pl_atual")),
            "pl_max": self._csv_value(decision.get("pl_max")),
            "pl_pct_of_max": self._csv_value(decision.get("pl_pct_of_max")),
            "spot_reference": self._csv_value(decision.get("spot_reference")),
            "spot_ref": self._csv_value(decision.get("spot_ref")),
            "rationale": self._csv_value(decision.get("rationale")),
            "why": self._csv_value(decision.get("why") or decision.get("why_json")),
            "raw_json": json.dumps(decision, ensure_ascii=False, default=str),
        }

    def _csv_value(self, value: Any) -> str:
        if value is None:
            return ""

        if isinstance(value, (dict, list)):
            return json.dumps(value, ensure_ascii=False, default=str)

        return str(value)

    def _structure_name(self, structure_id: Any) -> str:
        structure = self.structure_index.get(str(structure_id), {})
        for key in (
            "name",
            "nome",
            "label",
            "title",
            "titulo",
            "título",
            "description",
            "descricao",
            "descrição",
            "structure_name",
            "nome_estrutura",
            "estrutura",
        ):
            value = structure.get(key)
            if value:
                return str(value)
        return ""

    def _format_row(self, decision: Dict[str, Any], index: int) -> str:
        timestamp = decision.get("timestamp") or decision.get("created_at") or "sem timestamp"
        structure_id = decision.get("structure_id") or decision.get("aba") or "N/A"
        structure_name = self._structure_display_name(structure_id)
        decision_text = decision.get("decision") or "N/A"
        level = decision.get("level", "")
        dte = decision.get("dte_min", "")
        ratio = decision.get("pl_pct_of_max", "")

        return (
            f"{index + 1:03d} | {timestamp} | "
            f"estrutura {structure_id} {structure_name} | {decision_text} | "
            f"nivel {level} | dte {dte} | pl% {ratio}"
        )

    def _structure_display_name(self, structure_id: Any) -> str:
        structure = self.structure_index.get(str(structure_id), {})
        for key in (
            "name",
            "nome",
            "label",
            "title",
            "titulo",
            "título",
            "description",
            "descricao",
            "descrição",
            "structure_name",
            "nome_estrutura",
            "estrutura",
        ):
            value = structure.get(key)
            if value:
                return f"({value})"
        return ""

    def _structure_status_label(self, structure_id: Any) -> str:
        if structure_id is None or structure_id == "":
            return "N/A"

        structure_key = str(structure_id)
        if structure_key in self.active_structure_ids:
            return "Ativa"

        if structure_key in self.structure_index:
            return "Inativa ou fora da listagem ativa"

        return "Não localizada"

    def _format_money_value(self, value: Any) -> str:
        if value is None or value == "":
            return "N/A"

        try:
            number = float(value)
            formatted = f"{number:,.2f}"
            formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
            return f"R$ {formatted}"
        except Exception:
            return str(value)

    def _format_percent_value(self, value: Any) -> str:
        if value is None or value == "":
            return "N/A"

        try:
            number = float(value)
            if abs(number) <= 1:
                number = number * 100
            return f"{number:.1f}%"
        except Exception:
            return str(value)

    def _format_number_value(self, value: Any) -> str:
        if value is None or value == "":
            return "N/A"

        try:
            number = float(value)
            if number.is_integer():
                return str(int(number))
            return f"{number:.2f}"
        except Exception:
            return str(value)

    def _detail_value(self, decision: Dict[str, Any], *keys: str) -> Any:
        for key in keys:
            value = decision.get(key)
            if value is not None and value != "":
                return value
        return None

    def _format_detail_header(self, decision: Dict[str, Any]) -> str:
        values = self._detail_header_values(decision)
        return "\n".join(self._detail_header_lines(values))

    def _detail_header_values(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        structure_id = self._decision_structure_id(decision)

        return {
            "structure_id": structure_id,
            "structure_display": self._detail_structure_display(structure_id),
            "structure_status": self._structure_status_label(structure_id),
            "timestamp": self._detail_value(decision, "timestamp"),
            "created_at": self._detail_value(decision, "created_at"),
            "decision_text": self._detail_value(decision, "decision"),
            "level": self._detail_value(decision, "level"),
            "pl_atual": self._detail_value(decision, "pl_atual"),
            "pl_max": self._detail_value(decision, "pl_max"),
            "ratio": self._detail_value(decision, "pl_pct_of_max"),
            "dte_min": self._detail_value(decision, "dte_min"),
            "spot_ref": self._detail_value(decision, "spot_reference", "spot_ref"),
        }

    def _detail_structure_display(self, structure_id: Any) -> str:
        structure_name = self._structure_name(structure_id)
        structure_display = str(structure_id) if structure_id is not None else "N/A"

        if structure_name:
            return f"{structure_display} - {structure_name}"

        return structure_display

    def _detail_header_lines(self, values: Dict[str, Any]) -> List[str]:
        return [
            "Resumo operacional",
            "------------------",
            f"Estrutura: {values['structure_display']}",
            f"Status da estrutura: {values['structure_status']}",
            f"Decisão: {self._display_or_na(values['decision_text'])}",
            f"Nível: {self._display_or_na(values['level'])}",
            f"Timestamp: {self._display_or_na(values['timestamp'])}",
            f"Criada em: {self._display_or_na(values['created_at'])}",
            "",
            "Métricas principais",
            "-------------------",
            f"PL atual: {self._format_money_value(values['pl_atual'])}",
            f"PL máximo: {self._format_money_value(values['pl_max'])}",
            f"PL % do máximo: {self._format_percent_value(values['ratio'])}",
            f"DTE mínimo: {self._format_number_value(values['dte_min'])}",
            f"Spot referência: {self._format_number_value(values['spot_ref'])}",
        ]

    def _display_or_na(self, value: Any) -> Any:
        return value if value is not None else "N/A"

    def _format_detail(self, decision: Dict[str, Any]) -> str:
        lines = [self._format_detail_header(decision)]
        used = self._detail_used_fields()

        rationale_payload = decision.get("rationale")
        why_payload = decision.get("why") or decision.get("why_json")

        self._append_detail_rationale_sections(
            lines,
            used,
            rationale_payload,
            why_payload,
        )
        self._append_detail_extra_fields(lines, decision, used)

        return "\n".join(lines).strip() or "Decisão sem dados detalhados."

    def _detail_used_fields(self) -> set:
        return {
            "timestamp",
            "created_at",
            "structure_id",
            "aba",
            "decision",
            "level",
            "dte_min",
            "pl_atual",
            "pl_max",
            "pl_pct_of_max",
            "spot_reference",
            "spot_ref",
        }

    def _append_detail_rationale_sections(
        self,
        lines: List[str],
        used: set,
        rationale_payload: Any,
        why_payload: Any,
    ) -> None:
        if rationale_payload:
            used.add("rationale")
            self._append_detail_payload_section(lines, "Rationale", "---------", rationale_payload)

        if why_payload:
            used.add("why")
            used.add("why_json")
            self._append_detail_payload_section(lines, "Rationale / why", "---------------", why_payload)

        if not rationale_payload and not why_payload:
            lines.append("")
            lines.append("Rationale / why")
            lines.append("---------------")
            lines.append("Sem rationale disponível.")

    def _append_detail_payload_section(
        self,
        lines: List[str],
        title: str,
        separator: str,
        payload: Any,
    ) -> None:
        lines.append("")
        lines.append(title)
        lines.append(separator)
        lines.append(self._format_json_like(payload))

    def _append_detail_extra_fields(
        self,
        lines: List[str],
        decision: Dict[str, Any],
        used: set,
    ) -> None:
        extra = {
            key: value
            for key, value in sorted(decision.items())
            if key not in used
        }

        if not extra:
            return

        lines.append("")
        lines.append("Campos adicionais / raw")
        lines.append("-----------------------")

        for key, value in extra.items():
            lines.append(f"- {key}: {self._format_json_like(value)}")

    def _format_json_like(self, value: Any) -> str:
        if isinstance(value, (dict, list)):
            return json.dumps(value, ensure_ascii=False, indent=2)

        if isinstance(value, str):
            text = value.strip()
            try:
                parsed = json.loads(text)
                return json.dumps(parsed, ensure_ascii=False, indent=2)
            except Exception:
                return text

        return str(value)

    def _valid_selected_index(self) -> Optional[int]:
        selected_index = self.selected_index

        if (
            isinstance(selected_index, int)
            and selected_index >= 0
            and selected_index < len(self.filtered_decisions)
        ):
            return selected_index

        return None

    def _set_detail_text(self, text: str) -> None:
        self.details_text.configure(state="normal")
        self.details_text.delete("1.0", "end")
        self.details_text.insert("1.0", text)
        self.details_text.configure(state="disabled")

        if hasattr(self, "copy_detail_btn"):
            has_selection = self._valid_selected_index() is not None
            self.copy_detail_btn.configure(state="normal" if has_selection else "disabled")


    # [FRENTE 49] INICIO - correcao pontual bugs ui fluxo payoff
    def _prepare_reloaded_decisions_view(self, decisions=None):
        """Prepara a visao de decisoes recarregadas sem quebrar o fluxo da UI.

        Metodo de compatibilidade controlada para evitar falha quando o painel
        tenta chamar um preparador inexistente. A funcao nao acessa banco,
        nao altera persistencia e nao muda contrato operacional amplo.
        """

        if decisions is None:
            decisions = []

        if isinstance(decisions, dict):
            decisions = [decisions]

        try:
            return list(decisions)
        except TypeError:
            return []
    # [FRENTE 49] FIM - correcao pontual bugs ui fluxo payoff

