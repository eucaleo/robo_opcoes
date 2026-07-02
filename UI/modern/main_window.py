#!/usr/bin/env python3
"""
Novo shell desktop paralelo da UI.

Este módulo NÃO substitui UI/main_window.py.
Ele reaproveita os componentes e serviços existentes, permitindo validar
o novo layout sem risco para a interface atual.
"""

from __future__ import annotations

import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Dict, List, Optional

from UI.components.decisions_grid import DecisionsGrid
from UI.components.details_panel import DetailsPanel
from UI.components.filters_panel import FiltersPanel
from UI.components.payoff_chart import PayoffChart
from UI.components.structure_editor_dialog import StructureEditorDialog
from UI.components.structures_list_panel import StructuresListPanel
from UI.models.ui_data import UIDataModel
from UI.debug_utils import debug


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class ModernMainWindow:
    """
    Shell desktop novo, em paralelo à MainWindow legado.

    Objetivos:
    - preservar regras e componentes existentes;
    - reorganizar visualmente a navegação;
    - manter a UI antiga intacta;
    - permitir evolução incremental.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Derivados - Novo Layout Desktop")
        self.root.geometry("1500x920")
        self.root.minsize(1200, 760)

        self.data_model = UIDataModel()
        self._db_path = str(PROJECT_ROOT / "dados" / "app.db")

        self._payoff_worker_id = 0
        self._loading_payoff = False
        self._recalc_in_progress = False
        self.last_selected_decision: Optional[Dict] = None

        self.status_var = tk.StringVar(value="Inicializando novo shell...")

        self._setup_style()
        self._setup_layout()
        self._bind_events()

        self.refresh_data()

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _setup_style(self) -> None:
        style = ttk.Style(self.root)

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("App.TFrame", background="#f3f5f8")
        style.configure("Header.TFrame", background="#101827")
        style.configure(
            "HeaderTitle.TLabel",
            background="#101827",
            foreground="#ffffff",
            font=("Segoe UI", 16, "bold"),
        )
        style.configure(
            "HeaderSub.TLabel",
            background="#101827",
            foreground="#b8c2d6",
            font=("Segoe UI", 9),
        )
        style.configure("Sidebar.TFrame", background="#182235")
        style.configure(
            "SidebarTitle.TLabel",
            background="#182235",
            foreground="#ffffff",
            font=("Segoe UI", 11, "bold"),
        )
        style.configure(
            "SidebarHint.TLabel",
            background="#182235",
            foreground="#aeb8cc",
            font=("Segoe UI", 8),
        )
        style.configure("Status.TLabel", padding=(8, 4))

    def _setup_layout(self) -> None:
        self.root.configure(background="#f3f5f8")

        shell = ttk.Frame(self.root, style="App.TFrame")
        shell.pack(fill="both", expand=True)

        self._build_header(shell)

        body = ttk.Frame(shell, style="App.TFrame")
        body.pack(fill="both", expand=True)

        self._build_sidebar(body)
        self._build_workspace(body)

        status = ttk.Label(
            self.root,
            textvariable=self.status_var,
            style="Status.TLabel",
            relief=tk.SUNKEN,
            anchor="w",
        )
        status.pack(side="bottom", fill="x")

    def _build_header(self, parent: tk.Widget) -> None:
        header = ttk.Frame(parent, style="Header.TFrame", padding=(14, 10))
        header.pack(fill="x")

        title = ttk.Label(
            header,
            text="Sistema de Derivados",
            style="HeaderTitle.TLabel",
        )
        title.pack(side="left")

        subtitle = ttk.Label(
            header,
            text="Novo layout desktop paralelo · UI antiga preservada",
            style="HeaderSub.TLabel",
        )
        subtitle.pack(side="left", padx=(16, 0), pady=(5, 0))

    def _build_sidebar(self, parent: tk.Widget) -> None:
        sidebar = ttk.Frame(parent, style="Sidebar.TFrame", width=220, padding=(12, 14))
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ttk.Label(
            sidebar,
            text="Ações",
            style="SidebarTitle.TLabel",
        ).pack(anchor="w", pady=(0, 10))

        self._side_button(sidebar, "Atualizar dados", self.refresh_data)
        self._side_button(sidebar, "Exportar CSV", self.export_csv)
        self._side_button(sidebar, "Executar pipeline", self.run_pipeline)
        self._side_button(sidebar, "Verificar bancos", self.check_databases)
        self._side_button(sidebar, "Limpar cache", self.clear_cache)

        ttk.Separator(sidebar).pack(fill="x", pady=14)

        ttk.Label(
            sidebar,
            text="Este shell é paralelo.\nNenhum arquivo legado foi substituído.",
            style="SidebarHint.TLabel",
            justify="left",
        ).pack(anchor="w")

        ttk.Frame(sidebar, style="Sidebar.TFrame").pack(fill="both", expand=True)

        self._side_button(sidebar, "Sair", self.root.quit)

    def _side_button(self, parent: tk.Widget, text: str, command) -> None:
        btn = ttk.Button(parent, text=text, command=command)
        btn.pack(fill="x", pady=3)

    def _build_workspace(self, parent: tk.Widget) -> None:
        workspace = ttk.Frame(parent, style="App.TFrame", padding=(8, 8))
        workspace.pack(side="left", fill="both", expand=True)

        self.main_notebook = ttk.Notebook(workspace)
        self.main_notebook.pack(fill="both", expand=True)

        self._build_analysis_tab(self.main_notebook)
        self._build_structures_tab(self.main_notebook)
        self._build_terminal_tab(self.main_notebook)

    def _build_analysis_tab(self, notebook: ttk.Notebook) -> None:
        tab = ttk.Frame(notebook, padding=6)
        notebook.add(tab, text="Análise")

        paned = ttk.PanedWindow(tab, orient="horizontal")
        paned.pack(fill="both", expand=True)

        left = ttk.Frame(paned)
        right = ttk.Frame(paned)

        paned.add(left, weight=1)
        paned.add(right, weight=2)

        self.filters_panel = FiltersPanel(
            parent=left,
            on_filter_change=self.on_filter_change,
        )
        self.filters_panel.pack(fill="x", padx=4, pady=(0, 6))

        self.decisions_grid = DecisionsGrid(
            parent=left,
            on_selection_change=self.on_decision_selected,
        )
        self.decisions_grid.pack(fill="both", expand=True, padx=4, pady=4)

        detail_notebook = ttk.Notebook(right)
        detail_notebook.pack(fill="both", expand=True, padx=4, pady=4)

        details_frame = ttk.Frame(detail_notebook)
        detail_notebook.add(details_frame, text="Detalhes da decisão")

        self.details_panel = DetailsPanel(
            details_frame,
            on_recalculate=self.recalculate_structure,
            app_db_path=self._db_path,
        )
        self.details_panel.pack(fill="both", expand=True, padx=4, pady=4)

        chart_frame = ttk.Frame(detail_notebook)
        detail_notebook.add(chart_frame, text="Curva de payoff")

        self.payoff_chart = PayoffChart(chart_frame)
        self.payoff_chart.pack(fill="both", expand=True, padx=4, pady=4)

    def _build_structures_tab(self, notebook: ttk.Notebook) -> None:
        tab = ttk.Frame(notebook, padding=6)
        notebook.add(tab, text="Estruturas")

        paned = ttk.PanedWindow(tab, orient="horizontal")
        paned.pack(fill="both", expand=True)

        left = ttk.Frame(paned)
        right = ttk.LabelFrame(paned, text="Detalhes", padding=8)

        paned.add(left, weight=1)
        paned.add(right, weight=1)

        self.structures_list = StructuresListPanel(
            left,
            on_structure_selected=self._on_structure_selected,
            on_request_edit=self._on_structure_edit_request,
            db_path=self._db_path,
        )
        self.structures_list.pack(fill="both", expand=True)

        self._struct_detail_text = tk.Text(
            right,
            state="disabled",
            wrap="word",
            font=("Consolas", 9),
            background="#fafafa",
        )
        self._struct_detail_text.pack(fill="both", expand=True)

    def _build_terminal_tab(self, notebook: ttk.Notebook) -> None:
        tab = ttk.Frame(notebook, padding=6)
        notebook.add(tab, text="Terminal VWAP Payoff")

        try:
            from controllers.terminal_vwap_payoff_controller import (
                TerminalVWAPPayoffController,
            )
            from repositories.structures_repository import StructuresRepository
            from services.terminal_vwap_payoff_app_service import (
                TerminalVWAPPayoffAppService,
            )
            from UI.components.terminal_vwap_payoff_panel import TerminalVWAPPayoffPanel

            repository = StructuresRepository(self._db_path)
            app_service = TerminalVWAPPayoffAppService(
                structure_repository=repository,
            )
            controller = TerminalVWAPPayoffController(app_service)

            self.terminal_vwap_payoff_panel = TerminalVWAPPayoffPanel(
                parent=tab,
                controller=controller,
                on_status=self.set_status,
            )
            self.terminal_vwap_payoff_panel.pack(
                fill="both",
                expand=True,
                padx=4,
                pady=4,
            )

        except Exception as exc:
            ttk.Label(
                tab,
                text=(
                    "Terminal VWAP Payoff indisponível neste shell.\n\n"
                    f"Erro ao inicializar integração local:\n{exc}"
                ),
                foreground="red",
                justify="left",
            ).pack(fill="both", expand=True, padx=12, pady=12)

    def _bind_events(self) -> None:
        self.root.bind("<F5>", lambda _e: self.refresh_data())
        self.root.bind("<Control-q>", lambda _e: self.root.quit())

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------

    def set_status(self, message: str) -> None:
        self.status_var.set(message)

    # ------------------------------------------------------------------
    # Decisões / filtros / payoff
    # ------------------------------------------------------------------

    def on_filter_change(self, filters: Dict) -> None:
        self.set_status("Aplicando filtros...")

        try:
            filtered_data = self.data_model.get_decisions(filters)
            self.decisions_grid.update_data(filtered_data)
            self.set_status(f"{len(filtered_data)} decisões encontradas")
        except Exception as exc:
            messagebox.showerror("Erro", f"Erro ao aplicar filtros: {exc}")
            self.set_status("Erro nos filtros")

    def on_decision_selected(self, decision_data: Dict) -> None:
        if not decision_data:
            return

        self.last_selected_decision = dict(decision_data)

        try:
            self.details_panel.update_decision(decision_data)
        except Exception as exc:
            print(f"[ModernUI] Erro ao atualizar detalhes: {exc}")

        structure_id = decision_data.get("structure_id")
        timestamp = decision_data.get("timestamp")

        if structure_id is not None:
            self._start_payoff_load(structure_id, timestamp, decision_data)
        else:
            self.payoff_chart.clear()
            self.set_status("Dados insuficientes para carregar payoff")

    def _start_payoff_load(
        self,
        structure_id,
        timestamp=None,
        decision_data=None,
    ) -> None:
        if decision_data is None:
            decision_data = {"structure_id": structure_id}

        self._payoff_worker_id += 1
        worker_id = self._payoff_worker_id
        self._loading_payoff = True
        self.set_status("Carregando payoff...")

        def worker() -> None:
            try:
                points, info_dict = self.data_model.get_payoff_curve_info(
                    structure_id,
                    timestamp,
                )

                try:
                    debug(
                        f"[ModernUI] payoff structure_id={structure_id} "
                        f"timestamp={timestamp} n={len(points or [])}"
                    )
                except Exception:
                    pass

                normalized = []
                for point in points or []:
                    if isinstance(point, dict):
                        if "spot" in point and "pl" in point:
                            normalized.append(
                                {"spot": point["spot"], "pl": point["pl"]}
                            )
                        elif "point_spot" in point and "point_pl" in point:
                            normalized.append(
                                {
                                    "spot": point["point_spot"],
                                    "pl": point["point_pl"],
                                }
                            )
                        else:
                            spot = point.get("x") if "x" in point else point.get("s")
                            pl = point.get("y") if "y" in point else point.get("p")
                            if spot is not None and pl is not None:
                                normalized.append({"spot": spot, "pl": pl})
                    elif isinstance(point, (list, tuple)) and len(point) >= 2:
                        normalized.append({"spot": point[0], "pl": point[1]})

                if worker_id != self._payoff_worker_id:
                    return

                self.root.after(
                    0,
                    self._finish_payoff_load,
                    normalized,
                    info_dict or {},
                    decision_data,
                    worker_id,
                )

            except Exception as exc:
                if worker_id == self._payoff_worker_id:
                    self.root.after(
                        0,
                        self._handle_payoff_error,
                        str(exc),
                        worker_id,
                    )

        threading.Thread(target=worker, daemon=True).start()

    def _finish_payoff_load(
        self,
        points: List[Dict],
        info_dict: Dict,
        decision_data: Dict,
        worker_id: int,
    ) -> None:
        if worker_id != self._payoff_worker_id:
            return

        self._loading_payoff = False

        try:
            if points:
                overlays = self.payoff_chart.update_chart(points, decision_data)

                try:
                    self.details_panel.update_breakevens(
                        overlays.get("breakevens"),
                        overlays.get("pl_at_spot_ref"),
                    )
                except Exception:
                    pass

                try:
                    self.details_panel.update_audit_info(info_dict or {})
                except Exception:
                    pass

                used_ts = (info_dict or {}).get("used_timestamp") or decision_data.get(
                    "timestamp"
                )
                source = (info_dict or {}).get("source_table", "payoff_curve_points")
                count = (info_dict or {}).get("count_points", len(points))

                msg = f"{count} pontos carregados ({source})"
                if used_ts and used_ts != decision_data.get("timestamp"):
                    msg += f" | ts usado: {used_ts}"

                self.set_status(msg)
            else:
                self.payoff_chart.clear()
                self.set_status("Sem dados de payoff para esta seleção")

        except Exception as exc:
            self._handle_payoff_error(str(exc), worker_id)

    def _handle_payoff_error(self, error_msg: str, worker_id: int) -> None:
        if worker_id != self._payoff_worker_id:
            return

        self._loading_payoff = False

        try:
            self.payoff_chart.clear()
        except Exception:
            pass

        self.set_status(f"Erro ao carregar payoff: {error_msg}")
        print(f"[ModernUI] Erro no payoff: {error_msg}")

    def refresh_data(self) -> None:
        self.set_status("Carregando dados...")

        try:
            self.data_model.refresh()

            try:
                self.filters_panel.update_structures(
                    self.data_model.get_structures()
                )
            except Exception:
                pass

            try:
                self.filters_panel.reset_filters()
            except Exception:
                pass

            decisions = self.data_model.get_decisions()
            self.decisions_grid.update_data(decisions)

            preserved = False
            previous = self.last_selected_decision

            if previous:
                structure_id = previous.get("structure_id")
                timestamp = previous.get("timestamp")

                if structure_id is not None:
                    try:
                        self.decisions_grid.select_by_key(structure_id, timestamp)
                    except Exception:
                        pass

                    try:
                        self.details_panel.update_decision(previous)
                    except Exception:
                        pass

                    try:
                        self._start_payoff_load(structure_id, timestamp, previous)
                        preserved = True
                    except Exception:
                        preserved = False

            if not preserved:
                try:
                    self.details_panel.clear()
                except Exception:
                    pass

                try:
                    self.payoff_chart.clear()
                except Exception:
                    pass

            self.set_status(f"Dados atualizados - {len(decisions)} decisões")

        except Exception as exc:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {exc}")
            self.set_status("Erro ao carregar dados")

    # ------------------------------------------------------------------
    # Ações globais
    # ------------------------------------------------------------------

    def export_csv(self) -> None:
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )

        if not filename:
            return

        try:
            current_data = self.decisions_grid.get_current_data()
            self.data_model.export_to_csv(current_data, filename)
            messagebox.showinfo("Sucesso", f"Dados exportados para {filename}")
            self.set_status(f"CSV exportado: {filename}")
        except Exception as exc:
            messagebox.showerror("Erro", f"Erro ao exportar: {exc}")
            self.set_status("Erro ao exportar CSV")

    def run_pipeline(self) -> None:
        confirmed = messagebox.askyesno(
            "Executar Pipeline",
            "Executar pipeline de derivados?\nIsso pode demorar alguns segundos.",
        )

        if not confirmed:
            return

        self.set_status("Executando pipeline...")

        try:
            script_path = PROJECT_ROOT / "scripts" / "run_derived_pipeline.py"
            if not script_path.exists():
                script_path = PROJECT_ROOT / "Scripts" / "run_derived_pipeline.py"

            if not script_path.exists():
                raise FileNotFoundError(
                    f"Não achei o script do pipeline em: {script_path}"
                )

            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(PROJECT_ROOT),
                check=True,
                capture_output=True,
                text=True,
            )

            if result.stdout:
                print("[ModernUI] Pipeline STDOUT:\n", result.stdout)
            if result.stderr:
                print("[ModernUI] Pipeline STDERR:\n", result.stderr)

            messagebox.showinfo("Sucesso", "Pipeline executado com sucesso.")
            self.refresh_data()

        except subprocess.CalledProcessError as exc:
            messagebox.showerror(
                "Erro",
                "Pipeline falhou:\n\nSTDOUT:\n"
                + (exc.stdout or "")
                + "\n\nSTDERR:\n"
                + (exc.stderr or ""),
            )
            self.set_status("Pipeline falhou")
        except Exception as exc:
            messagebox.showerror("Erro", f"Erro ao executar pipeline: {exc}")
            self.set_status("Erro ao executar pipeline")

    def recalculate_structure(self, structure_id: str) -> None:
        if self._recalc_in_progress:
            self.set_status(f"Recálculo já em andamento; ignorando {structure_id}")
            return

        self._recalc_in_progress = True

        try:
            self.payoff_chart.fix_current_curve()
        except Exception:
            pass

        self.set_status(f"Recalculando {structure_id}...")

        def finish(ok: bool, msg: str) -> None:
            self._recalc_in_progress = False
            self.set_status(msg)

            try:
                if hasattr(self.details_panel, "on_recalc_finished"):
                    self.details_panel.on_recalc_finished(
                        structure_id,
                        ok=ok,
                        message=msg,
                    )
            except Exception as exc:
                print("[ModernUI] Erro notificando details_panel:", exc)

        def worker() -> None:
            try:
                script_path = PROJECT_ROOT / "scripts" / "run_derived_pipeline.py"
                if not script_path.exists():
                    script_path = PROJECT_ROOT / "Scripts" / "run_derived_pipeline.py"

                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    cwd=str(PROJECT_ROOT),
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=120,
                )

                if result.stdout:
                    print("[ModernUI] Recalc STDOUT:\n", result.stdout)
                if result.stderr:
                    print("[ModernUI] Recalc STDERR:\n", result.stderr)

                self.root.after(0, self.refresh_data)
                self.root.after(
                    0,
                    lambda: finish(True, f"OK: {structure_id} recalculado"),
                )

            except subprocess.TimeoutExpired:
                self.root.after(0, lambda: finish(False, "Timeout no recálculo"))
            except subprocess.CalledProcessError as exc:
                if exc.stdout:
                    print("[ModernUI] Recalc STDOUT:\n", exc.stdout)
                if exc.stderr:
                    print("[ModernUI] Recalc STDERR:\n", exc.stderr)
                self.root.after(0, lambda: finish(False, "Falha no recálculo"))
            except Exception as exc:
                print("[ModernUI] Erro inesperado no recálculo:", exc)
                self.root.after(0, lambda: finish(False, "Erro no recálculo"))

        threading.Thread(target=worker, daemon=True).start()

    def check_databases(self) -> None:
        try:
            status = self.data_model.check_database_status()
            messagebox.showinfo("Status dos Bancos", status)
            self.set_status("Status dos bancos verificado")
        except Exception as exc:
            messagebox.showerror("Erro", f"Erro ao verificar bancos: {exc}")
            self.set_status("Erro ao verificar bancos")

    def clear_cache(self) -> None:
        self.data_model.clear_cache()
        messagebox.showinfo("Cache", "Cache limpo com sucesso.")
        self.set_status("Cache limpo")

    # ------------------------------------------------------------------
    # Estruturas
    # ------------------------------------------------------------------

    def _on_structure_selected(self, structure: Optional[Dict]) -> None:
        txt = self._struct_detail_text
        txt.config(state="normal")
        txt.delete("1.0", "end")

        if structure is None:
            txt.insert("end", "Nenhuma estrutura selecionada.")
        else:
            legs = structure.get("legs", [])
            lines = [
                f"ID         : {structure.get('id')}",
                f"Nome       : {structure.get('name')}",
                f"Ativo      : {structure.get('underlying_asset')}",
                f"Aba legado : {structure.get('alias_legacy_aba') or '--'}",
                f"Status     : {structure.get('status')}",
                f"Criado em  : {str(structure.get('created_at', ''))[:19]}",
                f"Atualizado : {str(structure.get('updated_at', ''))[:19]}",
                f"Obs        : {structure.get('notes') or '--'}",
                "",
                f"{len(legs)} leg(s)",
            ]

            for index, leg in enumerate(legs, 1):
                lines += [
                    "",
                    f"Leg {index}: {leg.get('position_side')} {leg.get('option_type')}",
                    f"  Strike : {leg.get('strike')}",
                    f"  Venc.  : {leg.get('expiration_date')}",
                    f"  Qtde   : {leg.get('quantity')}",
                    f"  Símbolo: {leg.get('symbol') or '--'}",
                    f"  Prêmio : {leg.get('premium')}",
                    f"  Mult.  : {leg.get('multiplier')}",
                ]

            txt.insert("end", "\n".join(lines))

        txt.config(state="disabled")

    def _on_structure_edit_request(self, structure_id: Optional[int]) -> None:
        dialog = StructureEditorDialog(
            self.root,
            structure_id=structure_id,
            db_path=self._db_path,
        )

        self.root.wait_window(dialog)

        if dialog.saved:
            self.structures_list.load()
            self.set_status("Estrutura salva com sucesso.")

    # ------------------------------------------------------------------
    # Execução
    # ------------------------------------------------------------------

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    app = ModernMainWindow()
    app.run()


if __name__ == "__main__":
    main()
