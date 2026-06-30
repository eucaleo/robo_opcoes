#!/usr/bin/env bash
set -euo pipefail

if [ ! -d "UI" ]; then
    echo "[ERRO] Execute este script na raiz do projeto."
    exit 1
fi

if [ ! -f "UI/main_window.py" ]; then
    echo "[ERRO] Arquivo UI/main_window.py não encontrado."
    exit 1
fi

stamp="$(date +%Y%m%d_%H%M%S)"
backup="UI/main_window.py.bak_terminal_operacional_${stamp}"

cp "UI/main_window.py" "$backup"
echo "[OK] Backup criado em: $backup"

cat > UI/main_window.py <<'PY'
# UI/main_window.py
#!/usr/bin/env python3
"""
Janela principal operacional do Sistema de Derivados.

A interface canônica da aplicação Tkinter é o Terminal VWAP Payoff.
Este arquivo não monta o shell legado de decisões, filtros, gráfico antigo
ou notebook intermediário.

Fluxo canônico:

run_ui.py
    -> UI.main_window.main()
        -> MainWindow
            -> TerminalVWAPPayoffPanel
"""

from pathlib import Path
from typing import Optional
import tkinter as tk
from tkinter import ttk, messagebox

from UI.components.terminal_vwap_payoff_panel import TerminalVWAPPayoffPanel
from repositories.structures_repository import StructuresRepository
from services.terminal_vwap_payoff_app_service import TerminalVWAPPayoffAppService
from controllers.terminal_vwap_payoff_controller import TerminalVWAPPayoffController


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class MainWindow:
    """Janela principal canônica da UI operacional."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Sistema de Derivados - Terminal VWAP Payoff")
        self.root.geometry("1400x900")
        self.root.minsize(1100, 700)

        self._db_path = str(PROJECT_ROOT / "dados" / "app.db")
        self.terminal_vwap_payoff_panel: Optional[TerminalVWAPPayoffPanel] = None

        self._setup_menus()
        self._bind_events()
        self._setup_layout()

    def _setup_menus(self) -> None:
        """Cria menu superior enxuto da aplicação operacional."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        app_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aplicação", menu=app_menu)

        app_menu.add_command(
            label="Atualizar estruturas",
            accelerator="F5",
            command=self.reload_terminal_structures,
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

    def _bind_events(self) -> None:
        """Vincula atalhos operacionais."""
        self.root.bind("<F5>", lambda _event: self.reload_terminal_structures())
        self.root.bind("<Control-q>", lambda _event: self.close())
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def _setup_layout(self) -> None:
        """Monta exclusivamente o Terminal VWAP Payoff operacional."""
        self.status_bar = ttk.Label(
            self.root,
            text="Pronto",
            relief=tk.SUNKEN,
            anchor="w",
        )
        self.status_bar.pack(side="bottom", fill="x")

        container = ttk.Frame(self.root)
        container.pack(side="top", fill="both", expand=True, padx=5, pady=5)

        controller = self._build_terminal_controller()

        self.terminal_vwap_payoff_panel = TerminalVWAPPayoffPanel(
            parent=container,
            controller=controller,
            on_status=self.set_status,
        )

        self.terminal_vwap_payoff_panel.pack(
            fill="both",
            expand=True,
        )

        self.set_status("Terminal VWAP Payoff pronto")

    def _build_terminal_controller(self) -> TerminalVWAPPayoffController:
        """Cria a cadeia canônica repository -> service -> controller."""
        structure_repository = StructuresRepository(self._db_path)

        app_service = TerminalVWAPPayoffAppService(
            structure_repository=structure_repository,
        )

        return TerminalVWAPPayoffController(app_service)

    def set_status(self, message: str) -> None:
        """Atualiza a barra de status."""
        try:
            self.status_bar.config(text=message)
        except Exception:
            pass

    def reload_terminal_structures(self) -> None:
        """Atualiza as estruturas exibidas no terminal operacional."""
        if self.terminal_vwap_payoff_panel is None:
            return

        try:
            self.terminal_vwap_payoff_panel.reload_structures()
            self.set_status("Estruturas atualizadas")
        except Exception as exc:
            self.set_status("Erro ao atualizar estruturas")
            messagebox.showerror(
                "Erro ao atualizar estruturas",
                str(exc),
            )
            raise

    def show_about(self) -> None:
        """Exibe informações da aplicação."""
        messagebox.showinfo(
            "Sobre",
            (
                "Sistema de Derivados\n"
                "Terminal VWAP Payoff Operacional\n\n"
                "UI canônica: TerminalVWAPPayoffPanel"
            ),
        )

    def close(self) -> None:
        """Fecha a aplicação."""
        self.root.destroy()

    def run(self) -> None:
        """Inicia a aplicação."""
        self.root.mainloop()


def main() -> None:
    """Entry point da UI Tkinter."""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
PY

python -m py_compile UI/main_window.py

python - <<'PY'
from pathlib import Path

path = Path("UI/main_window.py")
text = path.read_text(encoding="utf-8")

forbidden_terms = [
    "UIDataModel",
    "PayoffChart",
    "DetailsPanel",
    "DecisionsGrid",
    "FiltersPanel",
    "StructuresListPanel",
    "StructureEditorDialog",
    "ttk.Notebook",
    "refresh_data",
    "_setup_structures_tab",
    "_setup_terminal_vwap_payoff_tab",
    "on_decision_selected",
    "on_filter_change",
    "recalculate_structure",
    "run_pipeline",
    "check_databases",
    "clear_cache",
    "export_csv",
    "_start_payoff_load",
    "_finish_payoff_load",
    "_handle_payoff_error",
]

required_terms = [
    "class MainWindow:",
    "TerminalVWAPPayoffPanel",
    "StructuresRepository",
    "TerminalVWAPPayoffAppService",
    "TerminalVWAPPayoffController",
    "def main()",
]

hits = [term for term in forbidden_terms if term in text]
missing = [term for term in required_terms if term not in text]

if hits:
    raise SystemExit(
        "[ERRO] main_window.py ainda contém termos legados: "
        + ", ".join(hits)
    )

if missing:
    raise SystemExit(
        "[ERRO] main_window.py não contém termos obrigatórios: "
        + ", ".join(missing)
    )

print("[OK] main_window.py operacional validado sem shell legado.")
PY

echo
echo "[OK] Atualização concluída."
echo "[INFO] Diff gerado abaixo:"
echo

git diff -- UI/main_window.py
