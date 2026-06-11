# UI/main_window.py
#!/usr/bin/env python3
"""
UI Principal - Sistema de Derivados
Carrega dados de derived.db e app.db para exibir decisões e payoffs
"""
from UI.models.ui_data import UIDataModel
from UI.components.payoff_chart import PayoffChart
from UI.components.details_panel import DetailsPanel
from UI.components.decisions_grid import DecisionsGrid
from UI.components.filters_panel import FiltersPanel
from UI.components.structures_list_panel import StructuresListPanel
from UI.components.structure_editor_dialog import StructureEditorDialog
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from UI.debug_utils import debug, info
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
# FigureCanvasTkAgg importado lazily em _setup_chart para evitar side-effects no import
from pathlib import Path
import threading
import time

PROJECT_ROOT = Path(__file__).resolve().parents[1]

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Derivados - Análise de Decisões")
        self.root.geometry("1400x900")

        # Data model
        self.data_model = UIDataModel()

        # Caminho canônico ao banco operacional (alteracao_70/71)
        self._db_path = str(PROJECT_ROOT / "dados" / "app.db")

        # Threading control: evitar freeze da UI
        self._payoff_worker_id = 0

        # Loading animation
        self._loading_animation_active = False
        self._loading_animation_chars = ["", "", "", "", "", "", "", "", "", ""]
        self._loading_animation_index = 0
        self._loading_payoff = False
        self._stop_loading_animation()

        # Última decisão selecionada (preservada entre refreshes)
        self.last_selected_decision: Optional[Dict] = None

        # Controle de recalc em andamento
        self._recalc_in_progress = False

        # Configurar layout principal
        self._setup_layout()
        self._setup_menus()
        self._bind_events()

        # Carregar dados iniciais
        self.refresh_data()

    def _setup_layout(self):
        """Organiza layout em painéis."""
        main_paned = ttk.PanedWindow(self.root, orient="horizontal")
        main_paned.pack(fill="both", expand=True, padx=5, pady=5)

        # Painel esquerdo: filtros + grid
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)

        # Painel direito: notebook com abas
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)

        # === PAINEL ESQUERDO ===
        self.filters_panel = FiltersPanel(
            parent=left_frame,
            on_filter_change=self.on_filter_change,
        )
        self.filters_panel.pack(fill="x", padx=5, pady=5)

        self.decisions_grid = DecisionsGrid(
            parent=left_frame,
            on_selection_change=self.on_decision_selected,
        )
        self.decisions_grid.pack(fill="both", expand=True, padx=5, pady=5)

        # === PAINEL DIREITO ===
        right_notebook = ttk.Notebook(right_frame)
        right_notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # Aba 1: Detalhes da Decisão
        details_frame = ttk.Frame(right_notebook)
        right_notebook.add(details_frame, text="Detalhes da Decisão")

        self.details_panel = DetailsPanel(
            details_frame,
            on_recalculate=self.recalculate_structure,
        )
        self.details_panel.pack(fill="both", expand=True, padx=5, pady=5)

        # Aba 2: Gráfico de Payoff
        chart_frame = ttk.Frame(right_notebook)
        right_notebook.add(chart_frame, text="Curva de Payoff")

        self.payoff_chart = PayoffChart(chart_frame)
        self.payoff_chart.pack(fill="both", expand=True, padx=5, pady=5)

        # Aba 3: Estruturas (Fase 5 -- alteracao_10)
        self._setup_structures_tab(right_notebook)

        # Status bar
        self.status_bar = ttk.Label(
            self.root,
            text="Pronto",
            relief=tk.SUNKEN,
            anchor="w",
        )
        self.status_bar.pack(side="bottom", fill="x")

    def _setup_menus(self):
        """Cria menu superior."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Atualizar Dados", command=self.refresh_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exportar CSV...", command=self.export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)

        # Menu Ferramentas
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ferramentas", menu=tools_menu)
        tools_menu.add_command(label="Executar Pipeline", command=self.run_pipeline)
        tools_menu.add_command(label="Verificar Bancos", command=self.check_databases)
        tools_menu.add_separator()
        tools_menu.add_command(label="Limpar Cache", command=self.clear_cache)

        # Menu Ajuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Sobre", command=self.show_about)

    def _bind_events(self):
        """Vincula atalhos de teclado."""
        self.root.bind("<F5>", lambda e: self.refresh_data())
        self.root.bind("<Control-q>", lambda e: self.root.quit())

    # ------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------

    def on_filter_change(self, filters: Dict):
        """Callback quando filtros mudam."""
        self.status_bar.config(text="Aplicando filtros...")
        try:
            filtered_data = self.data_model.get_decisions(filters)
            self.decisions_grid.update_data(filtered_data)
            count = len(filtered_data)
            self.status_bar.config(text=f"{count} decisões encontradas")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aplicar filtros: {e}")
            self.status_bar.config(text="Erro nos filtros")

    def on_decision_selected(self, decision_data: Dict):
        """Callback quando uma decisão é selecionada no grid.
        alteracao_36: structure_id é suficiente para carregar payoff -- timestamp não é obrigatório.
        """
        if not decision_data:
            return

        self.last_selected_decision = dict(decision_data)

        # Atualizar painel de detalhes (síncrono, leve)
        try:
            self.details_panel.update_decision(decision_data)
        except Exception as e:
            print(f"[UI] Erro ao atualizar detalhes: {e}")

        # Carregar payoff em background -- apenas structure_id necessário
        structure_id = decision_data.get("structure_id")
        timestamp = decision_data.get("timestamp")  # opcional

        if structure_id is not None:
            self._start_payoff_load(structure_id, timestamp, decision_data)
        else:
            self.payoff_chart.clear()
            self.status_bar.config(text="Dados insuficientes para payoff")

    def _start_payoff_load(
        self,
        structure_id,
        timestamp=None,       # alteracao_36: opcional
        decision_data=None,   # alteracao_36: opcional
    ):
        """Inicia carregamento de payoff em thread separada.
        alteracao_36: structure_id é a única chave obrigatória.
        """
        if decision_data is None:
            decision_data = {"structure_id": structure_id}

        self._payoff_worker_id += 1
        current_worker_id = self._payoff_worker_id

        if self._loading_payoff:
            self.status_bar.config(text="Carregando payoff... (cancelando anterior)")
        else:
            self.status_bar.config(text="Carregando payoff...")

        self._loading_payoff = True

        def load_worker():
            try:
                points, info_dict = self.data_model.get_payoff_curve_info(
                    structure_id, timestamp
                )
                try:
                    debug(
                        f"payoff structure_id={structure_id} ts_req={timestamp} "
                        f"-> n={len(points or [])} info={info_dict}"
                    )
                except Exception:
                    pass

                # Normalizar formato de pontos para o chart
                norm = []
                for p in points or []:
                    if isinstance(p, dict):
                        if "spot" in p and "pl" in p:
                            norm.append({"spot": p["spot"], "pl": p["pl"]})
                        elif "point_spot" in p and "point_pl" in p:
                            norm.append({"spot": p["point_spot"], "pl": p["point_pl"]})
                        else:
                            spot = p.get("x") if "x" in p else p.get("s")
                            pl = p.get("y") if "y" in p else p.get("p")
                            if spot is not None and pl is not None:
                                norm.append({"spot": spot, "pl": pl})
                    elif isinstance(p, (list, tuple)) and len(p) >= 2:
                        norm.append({"spot": p[0], "pl": p[1]})
                points = norm

                if current_worker_id != self._payoff_worker_id:
                    return

                self.root.after(
                    0,
                    self._finish_payoff_load,
                    points,
                    info_dict,
                    decision_data,
                    current_worker_id,
                )
            except Exception as e:
                if current_worker_id == self._payoff_worker_id:
                    self.root.after(
                        0,
                        self._handle_payoff_error,
                        str(e),
                        current_worker_id,
                    )

        thread = threading.Thread(target=load_worker, daemon=True)
        thread.start()

    def refresh_data(self):
        """Recarrega dados do banco.
        alteracao_36: preserva seleção usando structure_id como chave -- timestamp é auxiliar.
        """
        self.status_bar.config(text="Carregando dados...")
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
            d = self.last_selected_decision

            if d:
                target_sid = d.get("structure_id")  # chave canônica
                target_ts = d.get("timestamp")       # auxiliar

                # Reselecionar na grid: structure_id é suficiente
                if target_sid is not None:
                    try:
                        self.decisions_grid.select_by_key(target_sid, target_ts)
                    except Exception:
                        pass

                    try:
                        self.details_panel.update_decision(d)
                    except Exception:
                        pass

                    try:
                        self._start_payoff_load(target_sid, target_ts, d)
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

            self.status_bar.config(
                text=f"Dados atualizados - {len(decisions)} decisões"
            )

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
            self.status_bar.config(text="Erro ao carregar dados")
    def export_csv(self):
        """Exporta dados filtrados para CSV."""
        from tkinter import filedialog

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if filename:
            try:
                current_data = self.decisions_grid.get_current_data()
                self.data_model.export_to_csv(current_data, filename)
                messagebox.showinfo("Sucesso", f"Dados exportados para {filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar: {e}")

    def recalculate_structure(self, structure_id: str):
        """
        Recalcula a estrutura identificada por structure_id e atualiza a UI.
        alteracao_36: recalculate_aba() removida; este é o único entry point.
        """
        if self._recalc_in_progress:
            try:
                self.status_bar.config(
                    text=f"Recalc já em andamento; ignorando ({structure_id})"
                )
            except Exception:
                pass
            return

        self._recalc_in_progress = True

        try:
            self.payoff_chart.fix_current_curve()
        except Exception:
            pass

        import subprocess
        import sys

        self.status_bar.config(text=f"Recalculando {structure_id}...")

        def finish(ok: bool, msg: str):
            self._recalc_in_progress = False
            try:
                self.status_bar.config(text=msg)
            except Exception:
                pass
            try:
                if hasattr(self, "details_panel") and hasattr(
                    self.details_panel, "on_recalc_finished"
                ):
                    self.details_panel.on_recalc_finished(
                        structure_id, ok=ok, message=msg
                    )
            except Exception as e:
                print("[UI] Erro notificando details_panel fim recalc:", e)

        def worker():
            try:
                project_root = Path(__file__).resolve().parents[1]
                script_path = project_root / "scripts" / "run_derived_pipeline.py"
                if not script_path.exists():
                    script_path = project_root / "Scripts" / "run_derived_pipeline.py"

                res = subprocess.run(
                    [sys.executable, str(script_path)],
                    cwd=str(project_root),
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=120,
                )

                if res.stdout:
                    print("[UI] Recalc STDOUT:\n", res.stdout)
                if res.stderr:
                    print("[UI] Recalc STDERR:\n", res.stderr)

                self.root.after(0, self.refresh_data)
                self.root.after(
                    0, lambda: finish(True, f"OK: {structure_id} recalculado")
                )

            except subprocess.TimeoutExpired:
                self.root.after(0, lambda: finish(False, "Timeout no recálculo"))
            except subprocess.CalledProcessError as e:
                if e.stdout:
                    print("[UI] Recalc STDOUT:\n", e.stdout)
                if e.stderr:
                    print("[UI] Recalc STDERR:\n", e.stderr)
                self.root.after(0, lambda: finish(False, "Falha no recálculo"))
            except Exception as e:
                print("[UI] Erro inesperado recalc:", e)
                self.root.after(0, lambda: finish(False, "Erro no recálculo"))

        threading.Thread(target=worker, daemon=True).start()

    def run_pipeline(self):
        """Executa o pipeline de derivados."""
        result = messagebox.askyesno(
            "Executar Pipeline",
            "Executar pipeline de derivados?\nIsso pode demorar alguns segundos.",
        )
        if not result:
            return

        self.status_bar.config(text="Executando pipeline...")

        try:
            project_root = Path(__file__).resolve().parents[1]
            script_path = project_root / "scripts" / "run_derived_pipeline.py"
            if not script_path.exists():
                script_path = project_root / "Scripts" / "run_derived_pipeline.py"

            if not script_path.exists():
                raise FileNotFoundError(
                    f"Não achei o script do pipeline em: {script_path}"
                )

            import subprocess
            import sys

            res = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(project_root),
                check=True,
                capture_output=True,
                text=True,
            )

            if res.stdout:
                print("[UI] Pipeline STDOUT:\n", res.stdout)
            if res.stderr:
                print("[UI] Pipeline STDERR:\n", res.stderr)

            messagebox.showinfo("Sucesso", "Pipeline executado com sucesso!")
            self.refresh_data()

        except subprocess.CalledProcessError as e:
            messagebox.showerror(
                "Erro",
                "Pipeline falhou:\n\nSTDOUT:\n"
                + (e.stdout or "")
                + "\n\nSTDERR:\n"
                + (e.stderr or ""),
            )
            self.status_bar.config(text="Pipeline falhou")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao executar pipeline: {e}")
            self.status_bar.config(text="Erro ao executar pipeline")

    def check_databases(self):
        """Verifica status dos bancos de dados."""
        try:
            status = self.data_model.check_database_status()
            messagebox.showinfo("Status dos Bancos", status)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar bancos: {e}")

    def clear_cache(self):
        """Limpa cache interno."""
        self.data_model.clear_cache()
        messagebox.showinfo("Cache", "Cache limpo com sucesso")

    def show_about(self):
        """Mostra informações sobre o sistema."""
        about_text = """Sistema de Derivados v1.0

Desenvolvido para análise de estruturas de opções
Pipeline automático de payoff e decisões

Camadas:
* Excel RTD  CSV Bridge
* Ingest Python  app.db
* Domain Layer  derived.db
* UI Tkinter (esta interface)

Baseline: executed_v1 + baseline_v1b"""
        messagebox.showinfo("Sobre", about_text)

    # ------------------------------------------------------------------
    # Handlers de payoff (thread  main thread)
    # ------------------------------------------------------------------

    def _finish_payoff_load(
        self,
        points: List[Dict],
        info_dict: Dict,
        decision_data: Dict,
        worker_id: int,
    ):
        """Executado na thread principal quando a curva chega do worker."""
        if worker_id != self._payoff_worker_id:
            return

        self._loading_payoff = False
        self._stop_loading_animation()

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
                src = (info_dict or {}).get("source_table", "payoff_curve_points")
                n = (info_dict or {}).get("count_points", len(points))
                msg = f"{n} pontos ({src})"
                if used_ts and used_ts != decision_data.get("timestamp"):
                    msg += f" | ts usado: {used_ts}"
                self.status_bar.config(text=msg)
            else:
                self.payoff_chart.clear()
                self.status_bar.config(text="Sem dados de payoff para esta seleção")
        except Exception as e:
            self._handle_payoff_error(str(e), worker_id)

    def _handle_payoff_error(self, error_msg: str, worker_id: int):
        if worker_id != self._payoff_worker_id:
            return
        self._loading_payoff = False
        self._stop_loading_animation()
        try:
            self.payoff_chart.clear()
        except Exception:
            pass
        self.status_bar.config(text=f"Erro ao carregar payoff: {error_msg}")
        print(f"[UI] Erro no payoff: {error_msg}")
        import traceback
        traceback.print_exc()

    # ------------------------------------------------------------------
    # Loading animation
    # ------------------------------------------------------------------

    def _start_loading_animation(self, base_text: str):
        self._loading_animation_active = True
        self._loading_animation_index = 0

        def animate():
            if not self._loading_animation_active:
                return
            char = self._loading_animation_chars[self._loading_animation_index]
            self.status_bar.config(text=f"{char} {base_text}")
            self._loading_animation_index = (
                self._loading_animation_index + 1
            ) % len(self._loading_animation_chars)
            self.root.after(100, animate)

        animate()

    def _stop_loading_animation(self):
        self._loading_animation_active = False

    # ------------------------------------------------------------------
    # Aba Estruturas (Fase 5 -- alteracao_10)
    # ------------------------------------------------------------------

    def _setup_structures_tab(self, notebook: ttk.Notebook):
        """Aba 'Estruturas' no notebook principal."""
        outer = ttk.Frame(notebook)
        notebook.add(outer, text=" Estruturas")

        paned = ttk.PanedWindow(outer, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=4, pady=4)

        # Painel esquerdo -- lista
        list_frame = ttk.Frame(paned)
        paned.add(list_frame, weight=1)

        self.structures_list = StructuresListPanel(
            list_frame,
            on_structure_selected=self._on_structure_selected,
            on_request_edit=self._on_structure_edit_request,
            db_path=self._db_path,
        )
        self.structures_list.pack(fill="both", expand=True)

        # Painel direito -- detalhes somente leitura
        detail_frame = ttk.LabelFrame(paned, text="Detalhes", padding=8)
        paned.add(detail_frame, weight=1)

        self._struct_detail_text = tk.Text(
            detail_frame,
            state="disabled",
            wrap="word",
            font=("Consolas", 9),
            background="#fafafa",
        )
        self._struct_detail_text.pack(fill="both", expand=True)

    def _on_structure_selected(self, structure: Optional[Dict]):
        """Exibe detalhes da estrutura selecionada no painel direito."""
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
                f" {len(legs)} Leg(s) ",
            ]
            for i, leg in enumerate(legs, 1):
                lines += [
                    f"  Leg {i}: {leg.get('position_side')} {leg.get('option_type')}",
                    f"         Strike : {leg.get('strike')}  Venc: {leg.get('expiration_date')}",
                    f"         Qtde   : {leg.get('quantity')}  Símbolo: {leg.get('symbol') or '--'}",
                    f"         Prêmio : {leg.get('premium')}  Mult: {leg.get('multiplier')}",
                    "",
                ]
            txt.insert("end", "\n".join(lines))

        txt.config(state="disabled")

    def _on_structure_edit_request(self, structure_id: Optional[int]):
        """Abre dialog de criação (None) ou edição (int)."""
        dlg = StructureEditorDialog(
            self.root,
            structure_id=structure_id,
            db_path=self._db_path,                            # ← usa instância
        )
        self.root.wait_window(dlg)
        if dlg.saved:
            self.structures_list.load()

            try:
                self.status_bar.config(text="Estrutura salva com sucesso.")
            except Exception:
                pass

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def run(self):
        """Inicia a aplicação."""
        self.root.mainloop()

def main():
    """Entry point da UI."""
    app = MainWindow()
    app.run()

if __name__ == "__main__":
    main()
