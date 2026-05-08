# main_window.py
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
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from UI.debug_utils import debug, info
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
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

        # Threading control (P5.7): evitar freeze da UI
        self._payoff_worker_id = 0
        # Loading animation
        self._loading_animation_active = False
        self._loading_animation_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self._loading_animation_index = 0
        self._loading_payoff = False
        self._stop_loading_animation()

        # Configurar layout principal
        self._setup_layout()
        self._setup_menus()
        self._bind_events()

        # Carregar dados iniciais
        self.refresh_data()

    def _setup_layout(self):
        """Organiza layout em painéis"""

        # Frame principal com divisões
        main_paned = ttk.PanedWindow(self.root, orient='horizontal')
        main_paned.pack(fill='both', expand=True, padx=5, pady=5)

        # Painel esquerdo (filtros + grid de decisões)
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)

        # Painel direito (detalhes + gráfico)
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)

        # === PAINEL ESQUERDO ===
        # Filtros no topo
        self.filters_panel = FiltersPanel(
            parent=left_frame,
            on_filter_change=self.on_filter_change
        )
        self.filters_panel.pack(fill='x', padx=5, pady=5)

        # Grid de decisões
        self.decisions_grid = DecisionsGrid(
            parent=left_frame,
            on_selection_change=self.on_decision_selected
        )
        self.decisions_grid.pack(fill='both', expand=True, padx=5, pady=5)

        # === PAINEL DIREITO ===
        # Notebook para abas de detalhes
        right_notebook = ttk.Notebook(right_frame)
        right_notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # Aba 1: Detalhes da Decisão
        details_frame = ttk.Frame(right_notebook)
        right_notebook.add(details_frame, text="Detalhes da Decisão")

        self.details_panel = DetailsPanel(details_frame, on_recalculate=self.recalculate_aba)
        self.details_panel.pack(fill='both', expand=True, padx=5, pady=5)

        # Aba 2: Gráfico de Payoff
        chart_frame = ttk.Frame(right_notebook)
        right_notebook.add(chart_frame, text="Curva de Payoff")

        self.payoff_chart = PayoffChart(chart_frame)
        self.payoff_chart.pack(fill='both', expand=True, padx=5, pady=5)

        # Status bar
        self.status_bar = ttk.Label(
            self.root,
            text="Pronto",
            relief=tk.SUNKEN,
            anchor='w'
        )
        self.status_bar.pack(side='bottom', fill='x')

    def _setup_menus(self):
        """Cria menu superior"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(
            label="Atualizar Dados",
            command=self.refresh_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exportar CSV...", command=self.export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)

        # Menu Ferramentas
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ferramentas", menu=tools_menu)
        tools_menu.add_command(
            label="Executar Pipeline",
            command=self.run_pipeline)
        tools_menu.add_command(
            label="Verificar Bancos",
            command=self.check_databases)
        tools_menu.add_separator()
        tools_menu.add_command(label="Limpar Cache", command=self.clear_cache)

        # Menu Ajuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Sobre", command=self.show_about)

    def _bind_events(self):
        """Vincula eventos"""
        # F5 = refresh
        self.root.bind('<F5>', lambda e: self.refresh_data())

        # Ctrl+Q = quit
        self.root.bind('<Control-q>', lambda e: self.root.quit())

    # === CALLBACKS ===

    def on_filter_change(self, filters: Dict):
        """Callback quando filtros mudam"""
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
        """Callback quando uma decisão é selecionada no grid (P5.7: threading)"""
        if not decision_data:
            return

        self.last_selected_decision = dict(decision_data)

        # Atualizar painel de detalhes imediatamente (síncrono, leve)
        try:
            self.details_panel.update_decision(decision_data)
        except Exception as e:
            print(f"[UI] Erro ao atualizar detalhes: {e}")

        # Carregar payoff em background thread (assíncrono, pesado)
        aba = decision_data.get("aba")
        timestamp = decision_data.get("timestamp")

        if aba and timestamp:
            self._start_payoff_load(aba, timestamp, decision_data)
        else:
            self.payoff_chart.clear()
            self.status_bar.config(text="Dados insuficientes para payoff")

    def _start_payoff_load(self, aba: str, timestamp: str, decision_data: Dict):
        """Inicia carregamento de payoff em thread separada"""
        import threading

        # Incrementar worker ID (cancela workers anteriores)
        self._payoff_worker_id += 1
        current_worker_id = self._payoff_worker_id

        if self._loading_payoff:
            self.status_bar.config(text="Carregando payoff... (cancelando anterior)")
        else:
            self.status_bar.config(text="Carregando payoff...")

        self._loading_payoff = True

        def load_worker():
            try:
                points, info = self.data_model.get_payoff_curve_info(aba, timestamp)
                try:
                    debug(f"payoff aba={aba} ts_req={timestamp} -> n={len(points or [])} info={info}")

                except Exception:
                    pass

                # Normalizar formato de pontos para o chart
                # Aceita {"point_spot","point_pl"} e converte para {"spot","pl"}
                norm = []
                for p in (points or []):
                    if isinstance(p, dict):
                        if "spot" in p and "pl" in p:
                            norm.append({"spot": p["spot"], "pl": p["pl"]})
                        elif "point_spot" in p and "point_pl" in p:
                            norm.append({"spot": p["point_spot"], "pl": p["point_pl"]})
                        else:
                            # tenta chaves alternativas comuns
                            spot = p.get("x") if "x" in p else p.get("s")
                            pl = p.get("y") if "y" in p else p.get("p")
                            if spot is not None and pl is not None:
                                norm.append({"spot": spot, "pl": pl})
                    elif isinstance(p, (list, tuple)) and len(p) >= 2:
                        norm.append({"spot": p[0], "pl": p[1]})
                points = norm

                # Verificar se ainda é o worker atual (não foi cancelado)
                if current_worker_id != self._payoff_worker_id:
                    return

                self.root.after(
                    0,
                    self._finish_payoff_load,
                    points,
                    info,
                    decision_data,
                    current_worker_id,
                )
            except Exception as e:
                if current_worker_id == self._payoff_worker_id:
                    self.root.after(0, self._handle_payoff_error, str(e), current_worker_id)

        thread = threading.Thread(target=load_worker, daemon=True)
        thread.start()

    def refresh_data(self):
        """Recarrega dados do banco"""
        self.status_bar.config(text="Carregando dados...")
        try:
            self.data_model.refresh()

            # Atualizar lista de abas no filtro
            try:
                self.filters_panel.update_abas(self.data_model.get_abas())
            except Exception:
                pass

            # Resetar filtros e recarregar grid
            try:
                self.filters_panel.reset_filters()
            except Exception:
                pass

            decisions = self.data_model.get_decisions()
            self.decisions_grid.update_data(decisions)

            # Best-effort: tentar re-selecionar última decisão
            preserved = False
            d = getattr(self, "last_selected_decision", None)

            if d:
                try:
                    target_aba = d.get("aba")
                    target_ts = d.get("timestamp")
                    if target_aba and target_ts:
                        self.decisions_grid.select_by_key(target_aba, target_ts)
                except Exception:
                    pass

                # Atualizar detalhes e payoff (payoff em thread)
                try:
                    self.details_panel.update_decision(d)
                except Exception:
                    pass

                try:
                    aba = d.get("aba")
                    timestamp = d.get("timestamp")
                    if aba and timestamp:
                        self._start_payoff_load(aba, timestamp, d)
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

            self.status_bar.config(text=f"Dados atualizados - {len(decisions)} decisões")

        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
            self.status_bar.config(text="Erro ao carregar dados")

    def export_csv(self):
        """Exporta dados filtrados para CSV"""
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            try:
                current_data = self.decisions_grid.get_current_data()
                self.data_model.export_to_csv(current_data, filename)
                messagebox.showinfo(
                    "Sucesso", f"Dados exportados para {filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar: {e}")

    def recalculate_aba(self, aba: str):
        """Recalcula a estrutura (ABA) e atualiza UI (modo B)."""
        # Check se já tem recalc rodando (dedupe)
        if getattr(self, "_recalc_in_progress", False):
            try:
                self.status_bar.config(text=f"Recalc já em andamento; ignorando ({aba})")
            except Exception:
                pass
            return
        
        self._recalc_in_progress = True

        # Fixar curva atual para comparação (se existir)
        try:
            self.payoff_chart.fix_current_curve()
        except Exception:
            pass

        import subprocess, sys
        from pathlib import Path
        import threading

        self.status_bar.config(text=f"Recalculando {aba}...")

        def finish(ok: bool, msg: str):
            self._recalc_in_progress = False
            try:
                self.status_bar.config(text=msg)
            except Exception:
                pass
            # Notificar DetailsPanel que terminou
            try:
                if hasattr(self, "details_panel") and hasattr(self.details_panel, "on_recalc_finished"):
                    self.details_panel.on_recalc_finished(aba, ok=ok, message=msg)
            except Exception as e:
                print("[UI] Erro notificando details_panel fim recalc:", e)

        def worker():
            try:
                project_root = Path(__file__).resolve().parents[1]
                # Tenta scripts/ primeiro, depois Scripts/
                script_path = project_root / "scripts" / "run_derived_pipeline.py"
                if not script_path.exists():
                    script_path = project_root / "Scripts" / "run_derived_pipeline.py"


                res = subprocess.run(
                    [sys.executable, str(script_path), "--aba", aba],
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

                # Atualizar UI no thread principal
                self.root.after(0, self.refresh_data)
                self.root.after(0, lambda: finish(True, f"OK: {aba} recalculado"))

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
        from tkinter import messagebox
        import subprocess
        import sys
        from pathlib import Path

        result = messagebox.askyesno(
            "Executar Pipeline",
            "Executar pipeline de derivados?\nIsso pode demorar alguns segundos."
        )
        if not result:
            return

        self.status_bar.config(text="Executando pipeline...")

        try:
            # Caminho robusto: relativo ao arquivo UI/main_window.py (projeto = pasta pai de UI/)
            project_root = Path(__file__).resolve().parents[1]
            script_path = project_root / "scripts" / "run_derived_pipeline.py"
            if not script_path.exists():
                script_path = project_root / "Scripts" / "run_derived_pipeline.py"
            
            if not script_path.exists():
                raise FileNotFoundError(f"Não achei o script do pipeline em: {script_path}")

            res = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(project_root),
                check=True,
                capture_output=True,
                text=True
            )

            # logs opcionais
            if res.stdout:
                print("[UI] Recalc STDOUT:\n", res.stdout)
            if res.stderr:
                print("[UI] Recalc STDERR:\n", res.stderr)

            messagebox.showinfo("Sucesso", "Pipeline executado com sucesso!")
            self.refresh_data()

        except subprocess.CalledProcessError as e:
            messagebox.showerror(
                "Erro",
                "Pipeline falhou:\n\nSTDOUT:\n"
                + (e.stdout or "")
                + "\n\nSTDERR:\n"
                + (e.stderr or "")
            )
            self.status_bar.config(text="Pipeline falhou")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao executar pipeline: {e}")
            self.status_bar.config(text="Erro ao executar pipeline")

    def check_databases(self):
        """Verifica status dos bancos de dados"""
        try:
            status = self.data_model.check_database_status()
            messagebox.showinfo("Status dos Bancos", status)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar bancos: {e}")

    def clear_cache(self):
        """Limpa cache interno"""
        self.data_model.clear_cache()
        messagebox.showinfo("Cache", "Cache limpo com sucesso")

    def show_about(self):
        """Mostra informações sobre o sistema"""
        about_text = """Sistema de Derivados v1.0

Desenvolvido para análise de estruturas de opções
Pipeline automático de payoff e decisões

Camadas:
• Excel RTD → CSV Bridge
• Ingest Python → app.db
• Domain Layer → derived.db
• UI Tkinter (esta interface)

Baseline: executed_v1 + baseline_v1b"""

        messagebox.showinfo("Sobre", about_text)


    def _finish_payoff_load(self, points, info, decision_data, worker_id):
        """Executado na thread principal quando a curva chega do worker."""
        if worker_id != self._payoff_worker_id:
            return

        self._loading_payoff = False
        self._stop_loading_animation()

        try:
            if points:
                overlays = self.payoff_chart.update_chart(points, decision_data)

                # breakevens -> detalhes
                try:
                    self.details_panel.update_breakevens(
                        overlays.get("breakevens"),
                        overlays.get("pl_at_spot_ref"),
                    )
                except Exception:
                    pass

                # auditoria -> detalhes
                try:
                    self.details_panel.update_audit_info(info or {})
                except Exception:
                    pass

                used_ts = (info or {}).get("used_timestamp") or decision_data.get("timestamp")
                src = (info or {}).get("source_table", "payoff_curve_points")
                n = (info or {}).get("count_points", len(points))
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



    def _start_loading_animation(self, base_text: str):
        """Inicia animação de loading no status bar"""
        self._loading_animation_active = True
        self._loading_animation_index = 0
        
        def animate():
            if not self._loading_animation_active:
                return
            char = self._loading_animation_chars[self._loading_animation_index]
            self.status_bar.config(text=f"{char} {base_text}")
            self._loading_animation_index = (self._loading_animation_index + 1) % len(self._loading_animation_chars)
            self.root.after(100, animate)  # 100ms entre frames
        
        animate()
    
    def _stop_loading_animation(self):
        """Para a animação de loading"""
        self._loading_animation_active = False

    def run(self):
        """Inicia a aplicação"""
        self.root.mainloop()


def main():
    """Entry point da UI"""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()

