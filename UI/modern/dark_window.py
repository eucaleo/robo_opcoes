#!/usr/bin/env python3
"""
Launcher paralelo do layout DARK.

Este módulo NÃO substitui UI/main_window.py.
Ele abre diretamente o TerminalVWAPPayoffDarkPanel, que corresponde
ao layout escuro das telas de referência.
"""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk

from UI.modern.theme import CUSTOMTKINTER_APPEARANCE_MODE, CUSTOMTKINTER_COLOR_THEME

from UI.components.terminal_vwap_payoff_dark_panel import TerminalVWAPPayoffDarkPanel
from UI.components.decisions_dark_panel import DecisionsDarkPanel
from UI.models.ui_data import UIDataModel


PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_DB_PATH = PROJECT_ROOT / "dados" / "app.db"


class ModernDarkWindow:
    """
    Janela desktop paralela baseada no painel DARK existente.
    """

    def __init__(self) -> None:
        ctk.set_appearance_mode(CUSTOMTKINTER_APPEARANCE_MODE)
        ctk.set_default_color_theme(CUSTOMTKINTER_COLOR_THEME)

        self.root = ctk.CTk()
        self.root.title("Terminal de Análise Avançada - VWAP & Opções")
        self.root.geometry("1366x720")
        self.root.minsize(1180, 680)

        self.status_var = tk.StringVar(value="Inicializando layout DARK...")
        self.data_model = UIDataModel()

        self._build_menu()
        self._build_layout()

    def _build_menu(self) -> None:
        menu_bar = tk.Menu(self.root)

        app_menu = tk.Menu(menu_bar, tearoff=0)
        app_menu.add_command(label="Atualizar", command=self._reload_panel)
        app_menu.add_separator()
        app_menu.add_command(label="Sair", command=self.root.quit)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Sobre", command=self._show_about)

        menu_bar.add_cascade(label="Aplicação", menu=app_menu)
        menu_bar.add_cascade(label="Ajuda", menu=help_menu)

        self.root.configure(menu=menu_bar)

    def _build_layout(self) -> None:
        if not APP_DB_PATH.exists():
            messagebox.showwarning(
                "Banco não encontrado",
                f"Banco app.db não encontrado em:\n{APP_DB_PATH}",
                parent=self.root,
            )

        self.tabs = ctk.CTkTabview(self.root)
        self.tabs.pack(fill="both", expand=True)

        terminal_tab = self.tabs.add("Terminal VWAP")
        decisions_tab = self.tabs.add("Decisões")

        self.panel = TerminalVWAPPayoffDarkPanel(
            parent=terminal_tab,
            db_path=str(APP_DB_PATH),
            on_status=self.set_status,
        )
        self.panel.pack(fill="both", expand=True)

        self.decisions_panel = DecisionsDarkPanel(
            parent=decisions_tab,
            data_model=self.data_model,
            on_status=self.set_status,
            on_load_structure=self._load_structure_from_decision,
            get_structures=self._get_structures_for_decisions,
        )
        self.decisions_panel.pack(fill="both", expand=True)

    def set_status(self, message: str) -> None:
        self.status_var.set(message)
        print(f"[ModernDarkUI] {message}")

    def _reload_panel(self) -> None:
        try:
            reloaded = False

            if hasattr(self.panel, "reload_structures"):
                self.panel.reload_structures()
                reloaded = True

            if hasattr(self, "decisions_panel") and hasattr(self.decisions_panel, "reload_decisions"):
                self.decisions_panel.reload_decisions()
                reloaded = True

            if reloaded:
                self.set_status("Dados recarregados")
        except Exception as exc:
            messagebox.showerror(
                "Erro ao atualizar",
                str(exc),
                parent=self.root,
            )

    def _get_structures_for_decisions(self):
        """
        Fornece as estruturas carregadas no Terminal VWAP para a aba Decisões.
        Usado para restringir a busca a ID/nome e somente estruturas ativas.
        """
        try:
            structures = getattr(self.panel, "structures", None)

            if structures is None:
                structures = []

            if not structures and hasattr(self.panel, "reload_structures"):
                try:
                    self.panel.reload_structures()
                except Exception as exc:
                    self.set_status(f"Erro ao recarregar estruturas para decisões: {exc}")
                    return []

                structures = getattr(self.panel, "structures", []) or []

            return list(structures or [])

        except Exception as exc:
            self.set_status(f"Erro ao obter estruturas para decisões: {exc}")
            return []

    def _load_structure_from_decision(self, structure_id) -> None:
        """
        Carrega no Terminal VWAP a estrutura associada a uma decisão selecionada.
        """
        try:
            target = str(structure_id)

            structures = getattr(self.panel, "structures", None)
            if structures is None:
                structures = []

            if not structures and hasattr(self.panel, "reload_structures"):
                self.panel.reload_structures()
                structures = getattr(self.panel, "structures", []) or []

            selected = None
            for structure in structures:
                if str(structure.get("id")) == target:
                    selected = structure
                    break

            if selected is None:
                self.set_status(f"Estrutura {structure_id} não encontrada no Terminal VWAP")
                messagebox.showwarning(
                    "Estrutura não encontrada",
                    f"Estrutura {structure_id} não foi encontrada na lista do Terminal VWAP.",
                    parent=self.root,
                )
                return

            self.panel.select_structure(selected)

            try:
                self.tabs.set("Terminal VWAP")
            except Exception:
                pass

            self.set_status(f"Estrutura {structure_id} carregada a partir da decisão")

        except Exception as exc:
            self.set_status(f"Erro ao carregar estrutura da decisão: {exc}")
            messagebox.showerror(
                "Erro ao carregar estrutura",
                str(exc),
                parent=self.root,
            )

    def _show_about(self) -> None:
        messagebox.showinfo(
            "Sobre",
            "Layout DARK paralelo da UI.\n\n"
            "A UI antiga permanece preservada.",
            parent=self.root,
        )

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    app = ModernDarkWindow()
    app.run()


if __name__ == "__main__":
    main()
