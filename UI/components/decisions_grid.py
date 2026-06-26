from UI.components.ptbr_labels import decision_to_label
# UI/components/decisions_grid.py
from src.domain.refs.structure_ref import StructureRef
import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional, Callable
import json


class DecisionsGrid(ttk.LabelFrame):
    def __init__(
        self,
        parent,
        on_selection_change: Callable[[Optional[Dict]], None],
    ):
        super().__init__(parent, text="Decisões", padding=5)

        self.on_selection_change = on_selection_change
        self.current_data: List[Dict] = []

        self._setup_treeview()
        self._setup_scrollbars()

    def _setup_treeview(self):
        columns = (
            "timestamp",
            "structure_id",
            "decision",
            "level",
            "ratio",
            "dte",
            "pl_atual",
            "pl_max",
        )

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=12,
        )

        # Cabeçalhos
        self.tree.heading("timestamp", text="Data/Hora")
        self.tree.heading("structure_id", text="Estrutura")
        self.tree.heading("decision", text="Decisão")
        self.tree.heading("level", text="Nível")
        self.tree.heading("ratio", text="Razão %")
        self.tree.heading("dte", text="DTE")
        self.tree.heading("pl_atual", text="PL Atual")
        self.tree.heading("pl_max", text="PL Máx")

        # Larguras
        self.tree.column("timestamp", width=140, anchor="center")
        self.tree.column("structure_id", width=100, anchor="center")
        self.tree.column("decision", width=100, anchor="center")
        self.tree.column("level", width=50, anchor="center")
        self.tree.column("ratio", width=80, anchor="center")
        self.tree.column("dte", width=50, anchor="center")
        self.tree.column("pl_atual", width=80, anchor="e")
        self.tree.column("pl_max", width=80, anchor="e")

        # Evento de seleção
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        # Tags de cor por decisão
        self.tree.tag_configure("HOLD", background="#e8f5e8")
        self.tree.tag_configure("PREPARE_ROLL", background="#fff3cd")
        self.tree.tag_configure("CLOSE_REOPEN", background="#f8d7da")
        self.tree.tag_configure("ROLL", background="#d1ecf1")
        self.tree.tag_configure("ENTER", background="#d4edda")

    def _setup_scrollbars(self):
        v_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scrollbar.set)

        h_scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=h_scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _on_tree_select(self, event):
        selection = self.tree.selection()
        if not selection:
            self.on_selection_change(None)
            return

        item_id = selection[0]
        try:
            index = int(item_id) - 1
            if 0 <= index < len(self.current_data):
                self.on_selection_change(self.current_data[index])
        except (ValueError, IndexError):
            self.on_selection_change(None)

    def update_data(self, decisions: List[Dict]):
        """Atualiza grid com nova lista de decisões."""
        self.current_data = decisions.copy()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, decision in enumerate(decisions, 1):
            timestamp = self._format_timestamp(decision.get("timestamp"))
            # Exibe structure_id; fallback para aba (compat)
            structure_id = (
                decision.get("structure_id") or decision.get("aba") or "N/A"
            )
            decision_text = decision.get("decision", "N/A")
            decision_label = decision_to_label(decision_text)
            level = decision.get("level", "")
            ratio = self._format_ratio(decision.get("pl_pct_of_max"))
            dte = decision.get("dte_min", "")
            pl_atual = self._format_currency(decision.get("pl_atual"))
            pl_max = self._format_currency(decision.get("pl_max"))

            tag = (
                decision_text
                if decision_text in ["HOLD", "PREPARE_ROLL", "CLOSE_REOPEN", "ROLL", "ENTER"]
                else ""
            )

            self.tree.insert(
                "",
                "end",
                iid=str(i),
                values=(
                    timestamp,
                    structure_id,
                    decision_label,
                    level,
                    ratio,
                    dte,
                    pl_atual,
                    pl_max,
                ),
                tags=(tag,),
            )

    def _format_timestamp(self, timestamp_str: Optional[str]) -> str:
        """Formata timestamp sempre em America/Sao_Paulo."""
        if not timestamp_str:
            return ""

        try:
            from core.datetime_utils import format_datetime_local
            return format_datetime_local(
                timestamp_str,
                default=str(timestamp_str)[:16],
                fmt="%d/%m/%Y %H:%M",
            )
        except Exception:
            return str(timestamp_str)[:16] if len(str(timestamp_str)) > 16 else str(timestamp_str)

    def _format_ratio(self, ratio: Optional[float]) -> str:
        if ratio is None:
            return "N/A"
        try:
            return f"{ratio * 100:.1f}%"
        except (TypeError, ValueError):
            return "N/A"

    def _format_currency(self, value: Optional[float]) -> str:
        if value is None:
            return "N/A"
        try:
            if abs(value) >= 1000:
                return f"{value:,.0f}".replace(",", ".")
            else:
                return f"{value:.1f}"
        except (TypeError, ValueError):
            return "N/A"

    def get_current_data(self) -> List[Dict]:
        """Retorna dados atualmente exibidos (para export)."""
        return self.current_data.copy()

    def get_selected_decision(self) -> Optional[Dict]:
        """Retorna decisão atualmente selecionada."""
        selection = self.tree.selection()
        if not selection:
            return None
        try:
            index = int(selection[0]) - 1
            if 0 <= index < len(self.current_data):
                return self.current_data[index]
        except (ValueError, IndexError):
            pass
        return None

    def select_by_key(self, structure_id: str, timestamp: str) -> bool:
        """
        Seleciona a linha cujo (structure_id, timestamp) bate no dataset.
        Aceita tanto 'structure_id' quanto 'aba' nos dicts (compat).
        Retorna True se encontrou.
        """
        if not structure_id or not timestamp:
            return False

        for idx, row in enumerate(self.current_data):
            row_sid = row.get("structure_id") or row.get("aba")
            if row_sid == structure_id and row.get("timestamp") == timestamp:
                iid = str(idx + 1)
                try:
                    self.tree.selection_set(iid)
                    self.tree.focus(iid)
                    self.tree.see(iid)
                    self.tree.focus_set()
                    return True
                except Exception:
                    return False
        return False
