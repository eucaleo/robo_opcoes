# UI/main_window.py
#!/usr/bin/env python3
"""
Janela principal operacional dark do Sistema de Derivados.

A interface canônica é o Terminal VWAP Payoff em modo escuro, com:
- barra lateral fixa;
- painel retrátil de estruturas;
- KPIs superiores;
- blocos grandes de VWAP e Payoff;
- tabela inferior de pernas.
"""

from pathlib import Path
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from UI.components.terminal_vwap_payoff_dark_panel import TerminalVWAPPayoffDarkPanel


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class MainWindow:
    def __init__(self) -> None:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Terminal de Análise Avançada - VWAP & Opções")
        self.root.geometry("1365x750")
        self.root.minsize(1180, 700)

        self._db_path = str(PROJECT_ROOT / "dados" / "app.db")
        self.terminal_panel = None

        self._setup_menu()
        self._setup_layout()
        self._bind_events()

    def _setup_menu(self) -> None:
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        app_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aplicação", menu=app_menu)

        app_menu.add_command(
            label="Atualizar estruturas",
            accelerator="F5",
            command=self.reload_structures,
        )

        app_menu.add_separator()

        app_menu.add_command(
            label="Sair",
            accelerator="Ctrl+Q",
            command=self.close,
        )

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=help_menu)

        help_menu.add_command(
            label="Sobre",
            command=self.show_about,
        )

    def _setup_layout(self) -> None:
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.terminal_panel = TerminalVWAPPayoffDarkPanel(
            parent=self.root,
            db_path=self._db_path,
            on_status=self.set_status,
        )
        self.terminal_panel.grid(row=0, column=0, sticky="nsew")

    def _bind_events(self) -> None:
        self.root.bind("<F5>", lambda _event: self.reload_structures())
        self.root.bind("<Control-q>", lambda _event: self.close())
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def set_status(self, message: str) -> None:
        print("[UI]", message)

    def reload_structures(self) -> None:
        if self.terminal_panel is not None:
            self.terminal_panel.reload_structures()

    def show_about(self) -> None:
        messagebox.showinfo(
            "Sobre",
            (
                "Sistema de Derivados\n"
                "Terminal de Análise Avançada - VWAP & Opções\n\n"
                "Interface dark operacional."
            ),
        )

    def close(self) -> None:
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
