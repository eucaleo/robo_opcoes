#!/usr/bin/env python3
"""
Launcher paralelo do layout DARK.

Este módulo NÃO substitui UI/main_window.py.
Ele abre diretamente o TerminalVWAPPayoffDarkPanel, que corresponde
ao layout escuro das telas de referência.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from rtd_bridge.excel_rtd_connection_status_presenter import get_excel_rtd_status_payload
from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk

from UI.components.terminal_vwap_payoff_dark_panel import TerminalVWAPPayoffDarkPanel
from UI.components.decisions_dark_panel import DecisionsDarkPanel
from UI.models.ui_data import UIDataModel


# CustomTkinter runtime configuration for the modernDarkUI visual contract.
CUSTOMTKINTER_APPEARANCE_MODE = "Dark"
CUSTOMTKINTER_COLOR_THEME = "blue"

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
        help_menu.add_command(label="Status RTD Excel", command=self._show_excel_rtd_status)
        help_menu.add_separator()
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
            target = int(str(structure_id).strip())

            structures = getattr(self.panel, "structures", None)
            if structures is None:
                structures = []

            if not structures and hasattr(self.panel, "reload_structures"):
                try:
                    self.panel.reload_structures()
                except Exception as exc:
                    self.set_status(
                        f"Erro ao recarregar estruturas para decisão {structure_id}: {exc}"
                    )
                    messagebox.showwarning(
                        "Estruturas indisponíveis",
                        (
                            "Não foi possível recarregar as estruturas do Terminal VWAP.\n\n"
                            f"Erro: {exc}"
                        ),
                        parent=self.root,
                    )
                    return

                structures = getattr(self.panel, "structures", []) or []

            selected = None
            for structure in structures:
                try:
                    candidate = int(str(structure.get("id")).strip())
                except (TypeError, ValueError):
                    continue

                if candidate == target:
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

            current_selection = None
            for attr_name in ("selected_structure", "current_structure", "active_structure"):
                current_selection = getattr(self.panel, attr_name, None)
                if current_selection is not None:
                    break

            if current_selection is not None:
                try:
                    if isinstance(current_selection, dict):
                        current_selection_id = current_selection.get("id")
                    else:
                        current_selection_id = getattr(current_selection, "id")

                    if int(str(current_selection_id).strip()) == target:
                        return
                except (AttributeError, TypeError, ValueError):
                    pass

            try:
                self.panel.select_structure(selected)
            except Exception as exc:
                self.set_status(f"Erro ao selecionar estrutura {structure_id}: {exc}")
                messagebox.showerror(
                    "Erro ao selecionar estrutura",
                    str(exc),
                    parent=self.root,
                )
                return

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

    def _show_excel_rtd_status(self) -> None:
        """Exibe resumo operacional da conexão RTD/Excel."""
        payload = get_excel_rtd_status_payload()
        title = str(payload.get("title") or "Status RTD Excel")
        message = _format_excel_rtd_status_message(payload)
        severity = str(payload.get("severity") or "warning")

        if severity == "ok":
            messagebox.showinfo(title, message)
            return

        if severity == "warning":
            messagebox.showwarning(title, message)
            return

        messagebox.showerror(title, message)

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

def _format_excel_rtd_status_message(payload: dict) -> str:
    """Formata payload RTD/Excel para exibição amigável em messagebox."""
    lines: list[str] = []

    main_message = str(payload.get("message") or "").strip()
    if main_message:
        lines.append(main_message)
        lines.append("")

    lines.append(f"Pronto para leitura: {_format_bool_pt_br(bool(payload.get('ready')))}")
    lines.append(f"Severidade: {payload.get('severity') or 'indefinida'}")
    lines.append(f"Workbook: {payload.get('workbook_name') or '-'}")
    lines.append(f"Aba: {payload.get('worksheet_name') or '-'}")

    workbook_full_name = payload.get("workbook_full_name")
    if workbook_full_name:
        lines.append(f"Arquivo: {workbook_full_name}")

    checked_at = payload.get("checked_at")
    if checked_at:
        lines.append(f"Verificado em: {checked_at}")

    missing_headers = payload.get("missing_headers") or []
    if missing_headers:
        lines.append("")
        lines.append("Cabeçalhos ausentes:")
        for header in missing_headers:
            lines.append(f"- {header}")

    checks = payload.get("checks") or []
    if checks:
        lines.append("")
        lines.append("Checks:")
        for check in checks:
            label = check.get("label") if isinstance(check, dict) else ""
            ok = check.get("ok") if isinstance(check, dict) else False
            detail = check.get("detail") if isinstance(check, dict) else ""
            lines.append(f"- {label}: {_format_bool_pt_br(bool(ok))} ({detail})")

    return "\n".join(lines)


def _format_bool_pt_br(value: bool) -> str:
    if value:
        return "Sim"

    return "Não"

