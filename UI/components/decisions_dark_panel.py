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
    ) -> None:
        super().__init__(parent, fg_color="#0f172a")

        self.data_model = data_model
        self.on_status = on_status
        self.on_load_structure = on_load_structure
        self.decisions: List[Dict[str, Any]] = []
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

            self._render_rows()

            if self.decisions:
                self._select_decision(0)
                self._status(f"{len(self.decisions)} decisões carregadas no modo dark")
            else:
                self.load_structure_btn.configure(state="disabled")
                self._set_detail_text("Nenhuma decisão encontrada.")
                self._status("Nenhuma decisão encontrada no modo dark")

        except Exception as exc:
            self.decisions = []
            self.selected_index = None
            self._render_rows()
            self._set_detail_text(f"Erro ao carregar decisões:\n\n{exc}")
            self._status(f"Erro ao carregar decisões: {exc}")

    def _render_rows(self) -> None:
        for child in self.list_frame.winfo_children():
            child.destroy()

        self._row_buttons = []

        if not self.decisions:
            empty = ctk.CTkLabel(
                self.list_frame,
                text="Nenhuma decisão disponível.",
                text_color="#9ca3af",
            )
            empty.pack(fill="x", padx=8, pady=8)
            return

        visible = self.decisions[:300]

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

        if len(self.decisions) > len(visible):
            more = ctk.CTkLabel(
                self.list_frame,
                text=f"Exibindo 300 de {len(self.decisions)} decisões.",
                text_color="#fbbf24",
            )
            more.pack(fill="x", padx=8, pady=8)

    def _load_selected_structure(self) -> None:
        if self.selected_index is None:
            self._status("Nenhuma decisão selecionada para carregar estrutura")
            return

        if self.selected_index < 0 or self.selected_index >= len(self.decisions):
            self._status("Seleção de decisão inválida")
            return

        decision = self.decisions[self.selected_index]
        structure_id = decision.get("structure_id") or decision.get("aba")

        if structure_id is None:
            self._status("Decisão selecionada não possui structure_id")
            return

        if not self.on_load_structure:
            self._status("Carregamento de estrutura não está disponível")
            return

        self.on_load_structure(structure_id)

    def _select_decision(self, index: int) -> None:
        if index < 0 or index >= len(self.decisions):
            return

        self.selected_index = index

        for i, btn in enumerate(self._row_buttons):
            if i == index:
                btn.configure(fg_color="#2563eb", hover_color="#1d4ed8")
            else:
                btn.configure(fg_color="#111827", hover_color="#1f2937")

        decision = self.decisions[index]
        self._set_detail_text(self._format_detail(decision))

        structure_id = decision.get("structure_id") or decision.get("aba") or "N/A"
        if structure_id != "N/A" and self.on_load_structure:
            self.load_structure_btn.configure(state="normal")
        else:
            self.load_structure_btn.configure(state="disabled")
        decision_text = decision.get("decision", "N/A")
        self._status(f"Decisão selecionada: estrutura={structure_id}, decisão={decision_text}")

    def _format_row(self, decision: Dict[str, Any], index: int) -> str:
        timestamp = decision.get("timestamp") or decision.get("created_at") or "sem timestamp"
        structure_id = decision.get("structure_id") or decision.get("aba") or "N/A"
        decision_text = decision.get("decision") or "N/A"
        level = decision.get("level", "")
        dte = decision.get("dte_min", "")
        ratio = decision.get("pl_pct_of_max", "")

        return (
            f"{index + 1:03d} | {timestamp} | "
            f"estrutura {structure_id} | {decision_text} | "
            f"nivel {level} | dte {dte} | pl% {ratio}"
        )

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
