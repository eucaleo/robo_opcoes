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

from UI.components.terminal_vwap_payoff_dark_panel import TerminalVWAPPayoffDarkPanel


PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_DB_PATH = PROJECT_ROOT / "dados" / "app.db"


class ModernDarkWindow:
    """
    Janela desktop paralela baseada no painel DARK existente.
    """

    def __init__(self) -> None:
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Terminal de Análise Avançada - VWAP & Opções")
        self.root.geometry("1366x720")
        self.root.minsize(1180, 680)

        self.status_var = tk.StringVar(value="Inicializando layout DARK...")

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

        self.panel = TerminalVWAPPayoffDarkPanel(
            parent=self.root,
            db_path=str(APP_DB_PATH),
            on_status=self.set_status,
        )
        self.panel.pack(fill="both", expand=True)

    def set_status(self, message: str) -> None:
        self.status_var.set(message)
        print(f"[ModernDarkUI] {message}")

    def _reload_panel(self) -> None:
        try:
            if hasattr(self.panel, "reload_structures"):
                self.panel.reload_structures()
                self.set_status("Estruturas recarregadas")
        except Exception as exc:
            messagebox.showerror(
                "Erro ao atualizar",
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
