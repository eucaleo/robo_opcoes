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

import csv
import json
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from tkinter import filedialog, messagebox

import customtkinter as ctk


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
    ) -> None:
        super().__init__(parent, fg_color="#0f172a")

        self.data_model = data_model
        self.on_status = on_status
        self.on_load_structure = on_load_structure
        self.get_structures = get_structures
        self.decisions: List[Dict[str, Any]] = []
        self.filtered_decisions: List[Dict[str, Any]] = []
        self.structure_index: Dict[str, Dict[str, Any]] = {}
        self.active_structure_ids: set[str] = set()
        self.selected_index: Optional[int] = None
        self._last_decision_status_text: Optional[str] = None
        self._row_buttons: List[ctk.CTkButton] = []

        self._build_layout()

        self.after(100, self.reload_decisions)

    def _status(self, message: str) -> None:
        if self.on_status:
            self.on_status(message)

    def _build_layout(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)

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

        filters_frame = ctk.CTkFrame(header, fg_color="#0f172a")
        filters_frame.grid(row=2, column=0, columnspan=4, sticky="ew", padx=12, pady=(0, 10))
        filters_frame.grid_columnconfigure(1, weight=1)
        filters_frame.grid_columnconfigure(8, weight=1)

        decision_filter_label = ctk.CTkLabel(
            filters_frame,
            text="Decisão",
            text_color="#d1d5db",
        )
        decision_filter_label.grid(row=0, column=0, sticky="w", padx=(10, 4), pady=8)

        self.decision_filter_entry = ctk.CTkEntry(
            filters_frame,
            placeholder_text="Ex.: BUY, SELL, HOLD...",
            height=30,
            width=150,
        )
        self.decision_filter_entry.grid(row=0, column=1, sticky="ew", padx=(0, 8), pady=8)
        self.decision_filter_entry.bind("<Return>", self._apply_advanced_filters)

        level_filter_label = ctk.CTkLabel(
            filters_frame,
            text="Level mín.",
            text_color="#d1d5db",
        )
        level_filter_label.grid(row=0, column=2, sticky="w", padx=(0, 4), pady=8)

        self.level_min_filter_entry = ctk.CTkEntry(
            filters_frame,
            placeholder_text="mín.",
            height=30,
            width=70,
        )
        self.level_min_filter_entry.grid(row=0, column=3, sticky="w", padx=(0, 8), pady=8)
        self.level_min_filter_entry.bind("<Return>", self._apply_advanced_filters)

        dte_filter_label = ctk.CTkLabel(
            filters_frame,
            text="DTE máx.",
            text_color="#d1d5db",
        )
        dte_filter_label.grid(row=0, column=4, sticky="w", padx=(0, 4), pady=8)

        self.dte_max_filter_entry = ctk.CTkEntry(
            filters_frame,
            placeholder_text="máx.",
            height=30,
            width=70,
        )
        self.dte_max_filter_entry.grid(row=0, column=5, sticky="w", padx=(0, 8), pady=8)
        self.dte_max_filter_entry.bind("<Return>", self._apply_advanced_filters)

        apply_filters_btn = ctk.CTkButton(
            filters_frame,
            text="Aplicar",
            width=90,
            height=30,
            command=self._apply_advanced_filters,
        )
        apply_filters_btn.grid(row=0, column=6, sticky="e", padx=(0, 6), pady=8)

        clear_filters_btn = ctk.CTkButton(
            filters_frame,
            text="Limpar filtros",
            width=110,
            height=30,
            fg_color="#374151",
            hover_color="#4b5563",
            command=self._clear_advanced_filters,
        )
        clear_filters_btn.grid(row=0, column=7, sticky="e", padx=(0, 8), pady=8)

        self.filter_summary_label = ctk.CTkLabel(
            filters_frame,
            text="Filtros: sem dados carregados.",
            text_color="#9ca3af",
            anchor="e",
        )
        self.filter_summary_label.grid(row=0, column=8, sticky="e", padx=(0, 10), pady=8)

        self.search_entry = ctk.CTkEntry(
            header,
            placeholder_text="Buscar por ID ou nome da estrutura ativa...",
            height=32,
        )
        self.search_entry.grid(row=1, column=0, columnspan=3, sticky="ew", padx=(12, 4), pady=(0, 10))
        self.search_entry.bind("<KeyRelease>", self._on_search_changed)

        clear_search_btn = ctk.CTkButton(
            header,
            text="Limpar",
            width=120,
            height=32,
            fg_color="#374151",
            hover_color="#4b5563",
            command=self._clear_search,
        )
        clear_search_btn.grid(row=1, column=3, sticky="e", padx=(4, 12), pady=(0, 10))

        self.list_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#020617",
            label_text="Listagem",
            label_text_color="#e5e7eb",
        )
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=(0, 10))

        detail_frame = ctk.CTkFrame(self, fg_color="#020617")
        detail_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=(0, 10))
        detail_frame.grid_columnconfigure(0, weight=1)
        detail_frame.grid_columnconfigure(1, weight=0)
        detail_frame.grid_rowconfigure(1, weight=1)

        detail_title = ctk.CTkLabel(
            detail_frame,
            text="Detalhe da decisão selecionada",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#f9fafb",
        )
        detail_title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

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

        self.details_text = ctk.CTkTextbox(
            detail_frame,
            fg_color="#0f172a",
            text_color="#e5e7eb",
            border_width=1,
            border_color="#1f2937",
            wrap="word",
        )
        self.details_text.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=12, pady=(0, 12))
        self._set_detail_text("Nenhuma decisão selecionada.")

    def reload_decisions(self) -> None:
        try:
            if hasattr(self.data_model, "refresh"):
                self.data_model.refresh()

            decisions = self.data_model.get_decisions()
            self.decisions = list(decisions or [])
            self._clear_selection()
            self._refresh_structure_index()
            self._apply_filter(render=False)

            self._render_rows()

            if self.filtered_decisions:
                self._select_decision(0)
                if len(self.filtered_decisions) == len(self.decisions):
                    self._status(f"{len(self.decisions)} decisões carregadas no modo dark")
                else:
                    self._status(
                        f"{len(self.filtered_decisions)} de {len(self.decisions)} decisões exibidas"
                    )
            elif self.decisions:
                self.load_structure_btn.configure(state="disabled")
                self._set_detail_text("Nenhuma decisão encontrada para o filtro atual.")
                self._status(
                    f"Filtro sem resultados: 0 de {len(self.decisions)} decisões exibidas"
                )
            else:
                self.load_structure_btn.configure(state="disabled")
                self._set_detail_text("Nenhuma decisão encontrada.")
                self._status("Nenhuma decisão encontrada no modo dark")

        except Exception as exc:
            self.decisions = []
            self.filtered_decisions = []
            self.structure_index = {}
            self.active_structure_ids = set()
            self._clear_selection()
            self._render_rows()
            self._set_detail_text(f"Erro ao carregar decisões:\n\n{exc}")
            self._status(f"Erro ao carregar decisões: {exc}")

    def _render_rows(self) -> None:
        for child in self.list_frame.winfo_children():
            child.destroy()

        self._row_buttons = []

        if not self.filtered_decisions:
            empty_text = "Nenhuma decisão disponível."
            if self.decisions:
                empty_text = "Nenhuma decisão encontrada para o filtro atual."

            empty = ctk.CTkLabel(
                self.list_frame,
                text=empty_text,
                text_color="#9ca3af",
            )
            empty.pack(fill="x", padx=8, pady=8)
            return

        visible = self.filtered_decisions[:300]

        for index, decision in enumerate(visible):
            btn = ctk.CTkButton(
                self.list_frame,
                text=self._format_row(decision, index),
                anchor="w",
                height=44,
                fg_color="#111827",
                hover_color="#1f2937",
                text_color="#e5e7eb",
                command=lambda i=index: self._select_decision(i),
            )
            btn.pack(fill="x", padx=6, pady=3)
            self._row_buttons.append(btn)

        if len(self.filtered_decisions) > len(visible):
            more = ctk.CTkLabel(
                self.list_frame,
                text=f"Exibindo 300 de {len(self.filtered_decisions)} decisões filtradas.",
                text_color="#fbbf24",
            )
            more.pack(fill="x", padx=8, pady=8)

    def _on_search_changed(self, _event=None) -> None:
        self._apply_filter(render=True)

    def _clear_search(self) -> None:
        self.search_entry.delete(0, "end")
        self._apply_filter(render=True)

    def _apply_advanced_filters(self, _event=None) -> None:
        self._apply_filter(render=True)

    def _clear_advanced_filters(self) -> None:
        for attr in (
            "decision_filter_entry",
            "level_min_filter_entry",
            "dte_max_filter_entry",
        ):
            widget = getattr(self, attr, None)
            if widget is not None:
                widget.delete(0, "end")

        self._apply_filter(render=True)

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
            self.filter_summary_label.configure(
                text=f"Filtros inválidos: {error}",
                text_color="#fca5a5",
            )
            return

        active_filters = []

        if self._entry_text("search_entry"):
            active_filters.append("estrutura")

        if self._entry_text("decision_filter_entry"):
            active_filters.append("decisão")

        if self._entry_text("level_min_filter_entry"):
            active_filters.append("level mín.")

        if self._entry_text("dte_max_filter_entry"):
            active_filters.append("DTE máx.")

        suffix = "sem filtros avançados"
        if active_filters:
            suffix = "filtros: " + ", ".join(active_filters)

        self.filter_summary_label.configure(
            text=(
                f"Exibindo {visible_count} de {active_count} decisões ativas "
                f"({len(self.decisions)} totais) — {suffix}."
            ),
            text_color="#9ca3af",
        )

    def _refresh_structure_index(self) -> None:
        """
        Monta indice local de estruturas para:
        - filtrar somente decisoes de estruturas ativas;
        - permitir busca por ID ou nome da estrutura.
        """
        structures: List[Dict[str, Any]] = []

        if self.get_structures:
            try:
                structures = list(self.get_structures() or [])
            except Exception as exc:
                self._status(f"Erro ao carregar estruturas para filtro de decisões: {exc}")
                structures = []

        self.structure_index = {}
        self.active_structure_ids = set()

        for structure in structures:
            structure_id = structure.get("id")
            if structure_id is None:
                structure_id = structure.get("structure_id") or structure.get("aba")

            if structure_id is None:
                continue

            key = str(structure_id)
            self.structure_index[key] = structure

            if self._is_active_structure(structure):
                self.active_structure_ids.add(key)

        # Fallback seguro: se nao houver informacao de estruturas, nao bloqueia a lista.
        if not structures:
            ids = {
                str(decision.get("structure_id") or decision.get("aba"))
                for decision in self.decisions
                if decision.get("structure_id") is not None or decision.get("aba") is not None
            }
            self.active_structure_ids = ids

    def _is_active_structure(self, structure: Dict[str, Any]) -> bool:
        """
        Heuristica defensiva para identificar estrutura ativa sem depender
        de um unico nome de campo.
        """
        for key in ("active", "is_active", "ativo", "enabled"):
            if key in structure:
                value = structure.get(key)
                if isinstance(value, str):
                    return value.strip().lower() not in {"0", "false", "falso", "no", "nao", "não"}
                return bool(value)

        status = (
            structure.get("status")
            or structure.get("state")
            or structure.get("situacao")
            or structure.get("situação")
            or ""
        )

        if status:
            normalized = str(status).strip().lower()
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
            return normalized not in inactive_values

        # Se nao houver campo de status, assume ativa para preservar compatibilidade.
        return True

    def _apply_filter(self, render: bool = True) -> None:
        query = self._entry_text("search_entry").lower()
        decision_query = self._entry_text("decision_filter_entry").lower()
        level_min, level_min_valid = self._parse_float_filter("level_min_filter_entry")
        dte_max, dte_max_valid = self._parse_float_filter("dte_max_filter_entry")

        self._clear_selection()

        active_decisions = [
            decision
            for decision in self.decisions
            if self._decision_structure_id(decision) in self.active_structure_ids
        ]

        if not level_min_valid or not dte_max_valid:
            errors = []
            if not level_min_valid:
                errors.append("level mínimo deve ser numérico")
            if not dte_max_valid:
                errors.append("DTE máximo deve ser numérico")

            error_text = "; ".join(errors)
            self.filtered_decisions = []
            self._update_filter_summary(0, len(active_decisions), error_text)

            if render:
                self._render_rows()
                self.load_structure_btn.configure(state="disabled")
                self._set_detail_text(f"Filtro inválido: {error_text}.")
                self._status(f"Filtro inválido: {error_text}")

            return

        filtered_decisions = active_decisions

        if query:
            terms = [term for term in query.split() if term]
            filtered_decisions = [
                decision
                for decision in filtered_decisions
                if self._decision_matches_filter(decision, terms)
            ]

        if decision_query:
            filtered_decisions = [
                decision
                for decision in filtered_decisions
                if decision_query in str(decision.get("decision") or "").lower()
            ]

        if level_min is not None:
            filtered_decisions = [
                decision
                for decision in filtered_decisions
                if (
                    self._decision_numeric_value(decision, "level", "nivel", "nível")
                    is not None
                    and self._decision_numeric_value(decision, "level", "nivel", "nível") >= level_min
                )
            ]

        if dte_max is not None:
            filtered_decisions = [
                decision
                for decision in filtered_decisions
                if (
                    self._decision_numeric_value(decision, "dte_min", "dte", "DTE")
                    is not None
                    and self._decision_numeric_value(decision, "dte_min", "dte", "DTE") <= dte_max
                )
            ]

        self.filtered_decisions = filtered_decisions
        self._update_filter_summary(len(self.filtered_decisions), len(active_decisions))

        if render:
            self._render_rows()

            if self.filtered_decisions:
                self._select_decision(0)
            else:
                self.load_structure_btn.configure(state="disabled")
                if active_decisions:
                    self._set_detail_text("Nenhuma decisão encontrada para o filtro atual.")
                    self._status(
                        f"Filtro sem resultados: 0 de {len(active_decisions)} decisões de estruturas ativas"
                    )
                else:
                    self._set_detail_text("Nenhuma decisão de estrutura ativa encontrada.")
                    self._status("Nenhuma decisão de estrutura ativa encontrada no modo dark")

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
        Busca intencionalmente restrita:
        - ID da estrutura;
        - nome/rotulo/descricao da estrutura.
        """
        structure_id = self._decision_structure_id(decision)
        structure = self.structure_index.get(structure_id, {})

        parts: List[str] = [structure_id]

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
            if key in structure and structure.get(key) is not None:
                parts.append(str(structure.get(key)))

        return " ".join(parts).lower()

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

    def _select_decision(self, index: int) -> None:
        if index < 0 or index >= len(self.filtered_decisions):
            return

        self.selected_index = index

        for i, btn in enumerate(self._row_buttons):
            if i == index:
                btn.configure(fg_color="#2563eb", hover_color="#1d4ed8")
            else:
                btn.configure(fg_color="#111827", hover_color="#1f2937")

        decision = self.filtered_decisions[index]
        self._set_detail_text(self._format_detail(decision))

        structure_id = decision.get("structure_id") or decision.get("aba") or "N/A"
        if structure_id != "N/A" and self.on_load_structure:
            self.load_structure_btn.configure(state="normal")
        else:
            self.load_structure_btn.configure(state="disabled")

        self.copy_detail_btn.configure(state="normal")

        decision_text = decision.get("decision", "N/A")
        if len(self.filtered_decisions) == len(self.decisions):
            status_text = f"Decisão selecionada: estrutura={structure_id}, decisão={decision_text}"
        else:
            status_text = (
                f"Decisão selecionada: estrutura={structure_id}, decisão={decision_text} "
                f"({len(self.filtered_decisions)} de {len(self.decisions)} exibidas)"
            )
        self._status_selected_decision(status_text)

    def _clear_selection(self) -> None:
        self.selected_index = None
        self._last_decision_status_text = None

    def _status_selected_decision(self, status_text: str) -> None:
        if status_text == getattr(self, "_last_decision_status_text", None):
            return
        self._last_decision_status_text = status_text
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
        if not self.filtered_decisions:
            self._status("Nenhuma decisão exibida para exportar")
            messagebox.showinfo(
                "Exportar CSV",
                "Não há decisões exibidas para exportar.",
            )
            return

        default_name = f"decisoes_dark_filtradas_{datetime.now():%Y%m%d_%H%M%S}.csv"

        file_path = filedialog.asksaveasfilename(
            title="Exportar decisões filtradas",
            defaultextension=".csv",
            initialfile=default_name,
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )

        if not file_path:
            self._status("Exportação CSV cancelada")
            return

        fieldnames = [
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

        try:
            with open(file_path, "w", newline="", encoding="utf-8-sig") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

                for index, decision in enumerate(self.filtered_decisions, start=1):
                    writer.writerow(self._decision_export_row(decision, index))

            total = len(self.filtered_decisions)
            self._status(f"{total} decisões exportadas em CSV")
            messagebox.showinfo(
                "Exportar CSV",
                f"{total} decisões exportadas com sucesso.\n\n{file_path}",
            )
        except Exception as exc:
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
        structure_id = self._decision_structure_id(decision)
        structure_name = self._structure_name(structure_id)
        structure_display = str(structure_id) if structure_id is not None else "N/A"

        if structure_name:
            structure_display = f"{structure_display} - {structure_name}"

        timestamp = self._detail_value(decision, "timestamp")
        created_at = self._detail_value(decision, "created_at")
        decision_text = self._detail_value(decision, "decision")
        level = self._detail_value(decision, "level")

        pl_atual = self._detail_value(decision, "pl_atual")
        pl_max = self._detail_value(decision, "pl_max")
        ratio = self._detail_value(decision, "pl_pct_of_max")
        dte_min = self._detail_value(decision, "dte_min")
        spot_ref = self._detail_value(decision, "spot_reference", "spot_ref")

        lines = [
            "Resumo operacional",
            "------------------",
            f"Estrutura: {structure_display}",
            f"Status da estrutura: {self._structure_status_label(structure_id)}",
            f"Decisão: {decision_text if decision_text is not None else 'N/A'}",
            f"Nível: {level if level is not None else 'N/A'}",
            f"Timestamp: {timestamp if timestamp is not None else 'N/A'}",
            f"Criada em: {created_at if created_at is not None else 'N/A'}",
            "",
            "Métricas principais",
            "-------------------",
            f"PL atual: {self._format_money_value(pl_atual)}",
            f"PL máximo: {self._format_money_value(pl_max)}",
            f"PL % do máximo: {self._format_percent_value(ratio)}",
            f"DTE mínimo: {self._format_number_value(dte_min)}",
            f"Spot referência: {self._format_number_value(spot_ref)}",
        ]

        return "\n".join(lines)

    def _format_detail(self, decision: Dict[str, Any]) -> str:
        lines = [self._format_detail_header(decision)]

        structure_id = self._decision_structure_id(decision)

        used = {
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

        rationale_payload = decision.get("rationale")
        if rationale_payload:
            used.add("rationale")
            lines.append("")
            lines.append("Rationale")
            lines.append("---------")
            lines.append(self._format_json_like(rationale_payload))

        why_payload = decision.get("why") or decision.get("why_json")
        if why_payload:
            used.add("why")
            used.add("why_json")
            lines.append("")
            lines.append("Rationale / why")
            lines.append("---------------")
            lines.append(self._format_json_like(why_payload))

        if not rationale_payload and not why_payload:
            lines.append("")
            lines.append("Rationale / why")
            lines.append("---------------")
            lines.append("Sem rationale disponível.")

        extra = {
            key: value
            for key, value in sorted(decision.items())
            if key not in used
        }

        if extra:
            lines.append("")
            lines.append("Campos adicionais / raw")
            lines.append("-----------------------")
            for key, value in extra.items():
                lines.append(f"- {key}: {self._format_json_like(value)}")

        return "\n".join(lines).strip() or "Decisão sem dados detalhados."

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
