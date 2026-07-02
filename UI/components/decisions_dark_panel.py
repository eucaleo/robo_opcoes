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

import json
from typing import Any, Callable, Dict, List, Optional

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

        refresh_btn = ctk.CTkButton(
            header,
            text="Atualizar",
            width=120,
            command=self.reload_decisions,
        )
        refresh_btn.grid(row=0, column=2, sticky="e", padx=(4, 12), pady=10)

        self.search_entry = ctk.CTkEntry(
            header,
            placeholder_text="Buscar por ID ou nome da estrutura ativa...",
            height=32,
        )
        self.search_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(12, 4), pady=(0, 10))
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
        clear_search_btn.grid(row=1, column=2, sticky="e", padx=(4, 12), pady=(0, 10))

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
        detail_frame.grid_rowconfigure(1, weight=1)

        detail_title = ctk.CTkLabel(
            detail_frame,
            text="Detalhe da decisão selecionada",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#f9fafb",
        )
        detail_title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

        self.details_text = ctk.CTkTextbox(
            detail_frame,
            fg_color="#0f172a",
            text_color="#e5e7eb",
            border_width=1,
            border_color="#1f2937",
            wrap="word",
        )
        self.details_text.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self._set_detail_text("Nenhuma decisão selecionada.")

    def reload_decisions(self) -> None:
        try:
            if hasattr(self.data_model, "refresh"):
                self.data_model.refresh()

            decisions = self.data_model.get_decisions()
            self.decisions = list(decisions or [])
            self.selected_index = None
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
            self.selected_index = None
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
        query = ""
        if hasattr(self, "search_entry"):
            query = self.search_entry.get().strip().lower()

        self.selected_index = None

        active_decisions = [
            decision
            for decision in self.decisions
            if self._decision_structure_id(decision) in self.active_structure_ids
        ]

        if not query:
            self.filtered_decisions = active_decisions
        else:
            terms = [term for term in query.split() if term]
            self.filtered_decisions = [
                decision
                for decision in active_decisions
                if self._decision_matches_filter(decision, terms)
            ]

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
        decision_text = decision.get("decision", "N/A")
        if len(self.filtered_decisions) == len(self.decisions):
            self._status(f"Decisão selecionada: estrutura={structure_id}, decisão={decision_text}")
        else:
            self._status(
                f"Decisão selecionada: estrutura={structure_id}, decisão={decision_text} "
                f"({len(self.filtered_decisions)} de {len(self.decisions)} exibidas)"
            )

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

    def _format_detail(self, decision: Dict[str, Any]) -> str:
        lines = []

        main_fields = [
            ("timestamp", "Timestamp"),
            ("created_at", "Criada em"),
            ("structure_id", "Estrutura"),
            ("aba", "Aba"),
            ("decision", "Decisão"),
            ("level", "Nível"),
            ("dte_min", "DTE mínimo"),
            ("pl_atual", "PL atual"),
            ("pl_max", "PL máximo"),
            ("pl_pct_of_max", "PL % do máximo"),
            ("spot_reference", "Spot referência"),
            ("spot_ref", "Spot ref"),
        ]

        used = set()

        for key, label in main_fields:
            if key in decision:
                lines.append(f"{label}: {decision.get(key)}")
                used.add(key)

        why_payload = decision.get("why") or decision.get("why_json")
        if why_payload:
            used.add("why")
            used.add("why_json")
            lines.append("")
            lines.append("Rationale / why:")
            lines.append(self._format_json_like(why_payload))

        extra = {
            key: value
            for key, value in sorted(decision.items())
            if key not in used
        }

        if extra:
            lines.append("")
            lines.append("Campos adicionais:")
            for key, value in extra.items():
                lines.append(f"- {key}: {value}")

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

    def _set_detail_text(self, text: str) -> None:
        self.details_text.configure(state="normal")
        self.details_text.delete("1.0", "end")
        self.details_text.insert("1.0", text)
        self.details_text.configure(state="disabled")
