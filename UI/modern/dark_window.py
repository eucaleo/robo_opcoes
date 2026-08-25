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
from services.operational_data_status_service import build_operational_data_status
from pathlib import Path
from dataclasses import asdict, is_dataclass
from tkinter import messagebox

import customtkinter as ctk

from repositories.structures_repository import StructuresRepository
from repositories.rtd_option_quotes_repository import RtdOptionQuotesRepository
from repositories.decision_repository import DecisionRepository
from services.terminal_vwap_payoff_app_service import TerminalVWAPPayoffAppService
from services.structure_leg_rtd_enrichment_service import StructureLegRtdEnrichmentService
from UI.components.terminal_vwap_payoff_dark_panel import TerminalVWAPPayoffDarkPanel
from UI.components.decisions_dark_panel import DecisionsDarkPanel
from UI.models.ui_data import UIDataModel
from services.rtd_option_quotes_snapshot_status_service import read_rtd_option_quotes_max_updated_at


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

        self._rtd_option_quotes_poll_ms = 15_000
        self._last_rtd_option_quotes_updated_at = None
        self._rtd_option_quotes_watch_started = False
        self._rtd_option_quotes_refreshing = False

        self._build_menu()
        self._build_layout()
        self._start_rtd_option_quotes_watcher()

    def _build_menu(self) -> None:
        menu_bar = tk.Menu(self.root)

        app_menu = tk.Menu(menu_bar, tearoff=0)
        app_menu.add_command(label="Atualizar", command=self._reload_panel)
        app_menu.add_separator()
        app_menu.add_command(label="Sair", command=self.root.quit)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Status RTD Excel", command=self._show_excel_rtd_status)
        help_menu.add_command(label="Status dados operacionais", command=self._show_operational_data_status)
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

        structure_repository = StructuresRepository(str(APP_DB_PATH))
        rtd_option_quotes_repository = RtdOptionQuotesRepository(db_path=str(APP_DB_PATH))
        rtd_leg_enrichment_service = StructureLegRtdEnrichmentService(
            rtd_option_quotes_repository
        )

        decision_repository = DecisionRepository(db_path=str(APP_DB_PATH))

        terminal_app_service = TerminalVWAPPayoffAppService(
            structure_repository=structure_repository,
            rtd_leg_enrichment_service=rtd_leg_enrichment_service,
            decision_repository=decision_repository,
        )

        self.panel = TerminalVWAPPayoffDarkPanel(
            parent=terminal_tab,
            db_path=str(APP_DB_PATH),
            on_status=self.set_status,
            app_service=terminal_app_service,
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

    def _start_rtd_option_quotes_watcher(self) -> None:
        """
        Monitora o snapshot rtd_option_quotes atualizado pelo loop externo
        scripts/run_excel_rtd_option_quotes_snapshot_loop.py.

        A UI não chama Excel aqui. Ela apenas observa o banco e recarrega
        a estrutura ativa quando MAX(updated_at) muda.
        """
        if self._rtd_option_quotes_watch_started:
            return

        self._rtd_option_quotes_watch_started = True
        self._last_rtd_option_quotes_updated_at = self._read_rtd_option_quotes_max_updated_at()

        try:
            self.root.after(
                self._rtd_option_quotes_poll_ms,
                self._poll_rtd_option_quotes_snapshot,
            )
        except Exception as exc:
            self.set_status(f"Watcher RTD não iniciado: {exc}")

    def _read_rtd_option_quotes_max_updated_at(self):
        return read_rtd_option_quotes_max_updated_at(APP_DB_PATH)
    def _poll_rtd_option_quotes_snapshot(self) -> None:
        try:
            current = self._read_rtd_option_quotes_max_updated_at()
            previous = self._last_rtd_option_quotes_updated_at

            if current and previous and current != previous:
                self._last_rtd_option_quotes_updated_at = current
                self._handle_rtd_option_quotes_snapshot_changed(previous, current)
            elif current and previous is None:
                self._last_rtd_option_quotes_updated_at = current

        finally:
            try:
                self.root.after(
                    self._rtd_option_quotes_poll_ms,
                    self._poll_rtd_option_quotes_snapshot,
                )
            except Exception:
                pass

    def _handle_rtd_option_quotes_snapshot_changed(self, previous, current) -> None:
        if self._rtd_option_quotes_refreshing:
            return

        self._rtd_option_quotes_refreshing = True
        try:
            self.set_status(
                f"Snapshot RTD alterado: {previous} -> {current}. Recarregando UI..."
            )
            self._refresh_terminal_after_rtd_option_quotes_change()
        except Exception as exc:
            self.set_status(f"Erro ao atualizar UI após RTD: {exc}")
        finally:
            self._rtd_option_quotes_refreshing = False

    def _extract_structure_id(self, structure):
        if structure is None:
            return None

        if isinstance(structure, dict):
            value = structure.get("id") or structure.get("structure_id")
        else:
            value = (
                getattr(structure, "id", None)
                or getattr(structure, "structure_id", None)
            )

        try:
            return int(str(value).strip())
        except (TypeError, ValueError):
            return None

    def _find_structure_by_id(self, structure_id):
        try:
            target = int(str(structure_id).strip())
        except (TypeError, ValueError):
            return None

        for structure in getattr(self.panel, "structures", []) or []:
            try:
                candidate = int(str(structure.get("id")).strip())
            except (AttributeError, TypeError, ValueError):
                continue

            if candidate == target:
                return structure

        return None

    def _refresh_terminal_after_rtd_option_quotes_change(self) -> None:
        """
        Recarrega o painel operacional usando o snapshot RTD mais recente.

        Fluxo:
        rtd_option_quotes mudou -> reload_structures -> reselect estrutura ativa
        -> TerminalVWAPPayoffAppService reconstrói market/payoff/viewmodel.
        """
        selected = getattr(self.panel, "selected_structure", None)
        selected_id = self._extract_structure_id(selected)

        if hasattr(self.panel, "reload_structures"):
            self.panel.reload_structures()

        if selected_id is not None and hasattr(self.panel, "select_structure"):
            refreshed_structure = self._find_structure_by_id(selected_id)

            if refreshed_structure is None and isinstance(selected, dict):
                refreshed_structure = dict(selected)

            if refreshed_structure is not None:
                self.panel.select_structure(refreshed_structure)
                self.set_status(
                    f"RTD atualizado; estrutura {selected_id} recarregada automaticamente"
                )
            else:
                self.set_status(
                    f"RTD atualizado; estrutura ativa {selected_id} não encontrada após reload"
                )
        else:
            self.set_status("RTD atualizado; nenhuma estrutura ativa para recarregar")

        if (
            hasattr(self, "decisions_panel")
            and hasattr(self.decisions_panel, "reload_decisions")
        ):
            try:
                self.decisions_panel.reload_decisions()
            except Exception as exc:
                self.set_status(f"RTD atualizado, mas decisões não recarregaram: {exc}")

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

    def _show_operational_data_status(self) -> None:
        """Exibe resumo operacional dos dados persistidos."""
        title = "Status dados operacionais"

        try:
            status = build_operational_data_status(APP_DB_PATH)
            message = _format_operational_data_status_message(status)
            status_name = str(getattr(status, "status", "") or "").strip().lower()

            if status_name in {
                "ok",
                "ready",
                "online",
                "healthy",
                "available",
                "operational",
            }:
                messagebox.showinfo(title, message)
                return

            messagebox.showwarning(title, message)
        except Exception as exc:
            messagebox.showerror(
                title,
                "Erro ao obter status dos dados operacionais:\n\n" + str(exc),
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

def _format_operational_data_status_message(status: object) -> str:
    """Formata status operacional para exibicao amigavel em messagebox."""
    if is_dataclass(status) and not isinstance(status, type):
        data = asdict(status)
    elif isinstance(status, dict):
        data = dict(status)
    else:
        data = {}
        for name in dir(status):
            if name.startswith("_"):
                continue

            try:
                value = getattr(status, name)
            except Exception:
                continue

            if callable(value):
                continue

            if isinstance(value, (str, int, float, bool, list, tuple, dict, type(None))):
                data[name] = value

    status_name = data.get("status", "indisponivel")

    lines = [
        "Resumo operacional dos dados",
        "",
        f"Banco: {APP_DB_PATH}",
        f"Status: {status_name}",
    ]

    for key in sorted(data):
        if key == "status":
            continue

        value = data[key]
        if isinstance(value, dict):
            value = _format_operational_data_status_dict(value)
        elif isinstance(value, (list, tuple)):
            value = ", ".join(str(item) for item in value) if value else "vazio"

        lines.append(f"{_format_operational_data_status_label(key)}: {value}")

    return "\n".join(lines)


def _format_operational_data_status_dict(value: dict) -> str:
    if not value:
        return "vazio"

    parts = []
    for key in sorted(value):
        parts.append(f"{key}: {value[key]}")
    return "; ".join(parts)


def _format_operational_data_status_label(key: str) -> str:
    return str(key).replace("_", " ").strip().capitalize()


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

