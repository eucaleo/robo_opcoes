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

        # Controle de atualização automática da UI/RTD.
        # Este ciclo apenas recarrega dados já persistidos.
        # Não executa pipeline e não recalcula payoff.
        self._auto_refresh_interval_ms = 30000
        self._auto_refresh_enabled = True
        self._auto_refresh_in_progress = False
        self._auto_refresh_after_id = None
        self._closing = False

        # Assinatura da última atualização visual exibida.
        # Usada apenas para informar se houve mudança aparente na tela.
        self._last_visual_update_signature = None

        # Configurar layout principal
        self._setup_layout()
        self._setup_menus()
        self._bind_events()

        # Carregar dados iniciais
        self.refresh_data(source="inicial")

        # Iniciar atualização automática controlada.
        self.start_auto_refresh()

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
            app_db_path=self._db_path,
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
        file_menu.add_command(label="Recarregar Tela", command=self.refresh_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exportar CSV...", command=self.export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.close)

        # Menu Ferramentas
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ferramentas", menu=tools_menu)
        tools_menu.add_command(label="Atualizar Dados", command=self.run_pipeline)
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
        self.root.bind("<Control-q>", lambda e: self.close())
        self.root.protocol("WM_DELETE_WINDOW", self.close)

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

    def _set_details_update_status(self, message: str, color: str = "gray"):
        """Atualiza, quando disponível, o indicador visual no painel de detalhes."""
        try:
            if hasattr(self, "details_panel") and hasattr(
                self.details_panel, "set_update_status"
            ):
                self.details_panel.set_update_status(message, color=color)
        except Exception:
            pass

    def _build_visual_update_signature(self, decisions: List[Dict]):
        """
        Cria uma assinatura leve dos dados visíveis.

        Não altera regra de negócio; serve apenas para informar se o refresh
        trouxe mudança aparente para a tela.
        """
        signature = []
        for item in decisions or []:
            signature.append(
                (
                    str(item.get("structure_id", "")),
                    str(item.get("timestamp", "")),
                    str(item.get("decision", "")),
                    str(item.get("level", "")),
                    str(item.get("pl_atual", "")),
                    str(item.get("pl_max", "")),
                    str(item.get("pl_pct_of_max", "")),
                )
            )
        return tuple(signature)

    def refresh_data(self, show_errors: bool = True, source: str = "manual"):
        """Recarrega dados do banco.
        alteracao_36: preserva seleção usando structure_id como chave -- timestamp é auxiliar.
        """
        source_label = source or "manual"
        self.status_bar.config(text="Carregando dados...")
        self._set_details_update_status(
            f"Atualização {source_label} iniciada às {datetime.now():%H:%M:%S}",
            color="blue",
        )
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

            previous_signature = self._last_visual_update_signature
            current_signature = self._build_visual_update_signature(decisions)
            self._last_visual_update_signature = current_signature

            if previous_signature is None:
                visual_change_status = "dados carregados"
            elif previous_signature == current_signature:
                visual_change_status = "sem mudança aparente"
            else:
                visual_change_status = "com mudanças visíveis"

            preserved = False
            d = self.last_selected_decision

            if d:
                target_sid = d.get("structure_id")  # chave canônica
                target_ts = d.get("timestamp")       # auxiliar legado

                # Após refresh, não reaplicar o dict antigo no painel.
                # A seleção é preservada por structure_id, mas os widgets devem
                # receber a decisão recém-carregada do data_model.
                fresh_decision = None
                if target_sid is not None:
                    for item in decisions:
                        if str(item.get("structure_id")) == str(target_sid):
                            fresh_decision = item
                            break

                if fresh_decision is None:
                    fresh_decision = d

                fresh_ts = fresh_decision.get("timestamp", target_ts)

                # Reselecionar na grid usando a versão fresca quando disponível.
                if target_sid is not None:
                    try:
                        self.decisions_grid.select_by_key(target_sid, fresh_ts)
                    except Exception:
                        pass

                    try:
                        self.last_selected_decision = dict(fresh_decision)
                        self.details_panel.update_decision(fresh_decision)
                    except Exception:
                        pass

                    try:
                        self._start_payoff_load(target_sid, fresh_ts, fresh_decision)
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

            self._set_details_update_status(
                (
                    f"Atualização {source_label} concluída às {datetime.now():%H:%M:%S} "
                    f"— {len(decisions)} decisões — {visual_change_status}"
                ),
                color="green",
            )

            self.status_bar.config(
                text=f"Dados atualizados - {len(decisions)} decisões"
            )

        except Exception as e:
            if show_errors:
                messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
            else:
                print(f"[UI] Erro na atualização automática: {e}")
            self.status_bar.config(text="Erro ao carregar dados")
            self._set_details_update_status(
                f"Erro na atualização {source_label} às {datetime.now():%H:%M:%S}",
                color="red",
            )

    def close(self):
        """Fecha a janela cancelando agendamentos automáticos pendentes."""
        self._closing = True
        self.stop_auto_refresh()
        try:
            self.root.quit()
        except Exception:
            pass

    def start_auto_refresh(self):
        """Inicia o ciclo de atualização automática da tela."""
        self._auto_refresh_enabled = True
        self._schedule_auto_refresh()

    def stop_auto_refresh(self):
        """Interrompe o ciclo de atualização automática da tela."""
        self._auto_refresh_enabled = False
        after_id = getattr(self, "_auto_refresh_after_id", None)
        self._auto_refresh_after_id = None

        if after_id is not None:
            try:
                self.root.after_cancel(after_id)
            except Exception:
                pass

    def _schedule_auto_refresh(self):
        """Agenda a próxima atualização automática, garantindo um único after."""
        if (
            not getattr(self, "_auto_refresh_enabled", False)
            or getattr(self, "_closing", False)
        ):
            return

        previous_after_id = getattr(self, "_auto_refresh_after_id", None)
        if previous_after_id is not None:
            try:
                self.root.after_cancel(previous_after_id)
            except Exception:
                pass

        self._auto_refresh_after_id = self.root.after(
            self._auto_refresh_interval_ms,
            self._auto_refresh_tick,
        )

    def _auto_refresh_tick(self):
        """Executa uma atualização automática sem pipeline e sem recálculo."""
        self._auto_refresh_after_id = None

        if (
            not getattr(self, "_auto_refresh_enabled", False)
            or getattr(self, "_closing", False)
        ):
            return

        if (
            getattr(self, "_auto_refresh_in_progress", False)
            or getattr(self, "_recalc_in_progress", False)
        ):
            self._schedule_auto_refresh()
            return

        self._auto_refresh_in_progress = True
        try:
            self.refresh_data(show_errors=False, source="automática")
            try:
                self.status_bar.config(
                    text=f"Dados atualizados automaticamente às {datetime.now():%H:%M:%S}"
                )
            except Exception:
                pass
        finally:
            self._auto_refresh_in_progress = False
            self._schedule_auto_refresh()

    def export_csv(self):
        """Exporta dados filtrados para CSV."""
        from tkinter import filedialog

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")],
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

        Importante:
        - Este botão NÃO executa o pipeline completo.
        - Ele recalcula somente a estrutura selecionada via CanonicalPricingFacade.
        """
        if self._recalc_in_progress:
            try:
                self.status_bar.config(
                    text=f"Recalc já em andamento; ignorando ({structure_id})"
                )
            except Exception:
                pass
            return

        try:
            sid = int(structure_id)
        except (TypeError, ValueError):
            try:
                self.status_bar.config(
                    text=f"structure_id inválido para recálculo: {structure_id}"
                )
            except Exception:
                pass
            return

        self._recalc_in_progress = True

        try:
            self.payoff_chart.fix_current_curve()
        except Exception:
            pass

        self._set_details_update_status(
            f"Recálculo da estrutura {sid} iniciado às {datetime.now():%H:%M:%S}",
            color="blue",
        )

        try:
            self.status_bar.config(text=f"Recalculando estrutura {sid}...")
        except Exception:
            pass

        def finish(ok: bool, msg: str):
            self._recalc_in_progress = False

            try:
                self.status_bar.config(text=msg)
            except Exception:
                pass

            self._set_details_update_status(
                (
                    f"Recálculo concluído às {datetime.now():%H:%M:%S}: {msg}"
                    if ok
                    else f"Erro no recálculo às {datetime.now():%H:%M:%S}: {msg}"
                ),
                color="green" if ok else "red",
            )

            try:
                if hasattr(self, "details_panel") and hasattr(
                    self.details_panel, "on_recalc_finished"
                ):
                    self.details_panel.on_recalc_finished(
                        str(sid), ok=ok, message=msg
                    )
            except Exception as e:
                print("[UI] Erro notificando details_panel fim recalc:", e)

        def clear_ui_cache():
            try:
                if hasattr(self, "data_model") and hasattr(self.data_model, "clear_cache"):
                    self.data_model.clear_cache()
            except Exception as e:
                print("[UI] Erro limpando cache após recalc:", e)

        def worker():
            try:
                from services.canonical_pricing_facade import CanonicalPricingFacade

                facade = CanonicalPricingFacade(db_path=self._db_path)
                result = facade.execute_pricing(sid)

                print(f"[UI] Recalc structure_id={sid} result:", result)

                if not isinstance(result, dict):
                    raise RuntimeError(f"Resposta inválida do pricing facade: {result!r}")

                ok_statuses = {"success", "ok", "completed"}

                top_status = result.get("status")
                if top_status is not None and str(top_status).lower() not in ok_statuses:
                    msg = (
                        result.get("error_message")
                        or result.get("message")
                        or f"Falha no recálculo da estrutura {sid}: status={top_status}"
                    )
                    raise RuntimeError(msg)

                inner = result.get("result")
                if isinstance(inner, dict):
                    inner_status = inner.get("status")
                    if inner_status is not None and str(inner_status).lower() not in ok_statuses:
                        msg = (
                            inner.get("error_message")
                            or inner.get("message")
                            or f"Falha no recálculo da estrutura {sid}: status={inner_status}"
                        )
                        raise RuntimeError(msg)

                self.root.after(0, clear_ui_cache)
                self.root.after(0, lambda: self.refresh_data(source="recálculo"))
                self.root.after(
                    0,
                    lambda: finish(True, f"OK: estrutura {sid} recalculada"),
                )

            except Exception as e:
                print("[UI] Erro inesperado recalc:", e)
                self.root.after(
                    0,
                    lambda: finish(False, f"Erro no recálculo da estrutura {sid}: {e}"),
                )

        threading.Thread(target=worker, daemon=True).start()


    def _extract_pipeline_summary(self, stdout: str) -> Dict:
        """Extrai o resumo JSON emitido por scripts/run_derived_pipeline.py."""
        import json

        marker = "[PIPELINE_SUMMARY_JSON]"
        for line in reversed((stdout or "").splitlines()):
            if marker in line:
                payload = line.split(marker, 1)[1].strip()
                try:
                    data = json.loads(payload)
                    return data if isinstance(data, dict) else {}
                except Exception:
                    return {}
        return {}

    def _format_pipeline_value(self, value):
        """Formata valores do resumo operacional para exibição."""
        if value is None:
            return "n/d"
        return str(value)

    def _build_pipeline_feedback_message(self, stdout: str) -> str:
        """Monta mensagem amigável para o usuário após executar pipeline."""
        summary = self._extract_pipeline_summary(stdout)

        if not summary:
            return (
                "Pipeline executado com sucesso.\n\n"
                "Resumo operacional não disponível no stdout do pipeline."
            )

        lines = [
            "Pipeline executado com sucesso.",
            "",
            "Resumo operacional:",
            f"- Estruturas: {self._format_pipeline_value(summary.get('structures'))}",
            f"- Decisões: {self._format_pipeline_value(summary.get('decisions'))}",
            f"- Pontos de payoff: {self._format_pipeline_value(summary.get('payoff_points'))}",
            f"- Resumos de payoff: {self._format_pipeline_value(summary.get('payoff_summaries'))}",
            f"- Execuções de pricing: {self._format_pipeline_value(summary.get('pricing_executions'))}",
            f"- Cotações RTD atualizadas: {self._format_pipeline_value(summary.get('rtd_quotes_updated'))}",
            f"- Avisos: {self._format_pipeline_value(summary.get('warnings'))}",
            f"- Erros: {self._format_pipeline_value(summary.get('errors'))}",
        ]
        return "\n".join(lines)

    def _build_pipeline_status_message(self, stdout: str) -> str:
        """Monta texto curto para status bar após pipeline."""
        summary = self._extract_pipeline_summary(stdout)
        if not summary:
            return "Pipeline executado com sucesso"

        decisions = self._format_pipeline_value(summary.get("decisions"))
        payoff_points = self._format_pipeline_value(summary.get("payoff_points"))
        errors = self._format_pipeline_value(summary.get("errors"))

        return (
            f"Pipeline OK: decisões={decisions}; "
            f"pontos_payoff={payoff_points}; erros={errors}"
        )


    def run_pipeline(self):
        """Atualiza os dados executando o pipeline de derivados."""
        result = messagebox.askyesno(
            "Atualizar Dados",
            "Atualizar dados executando o pipeline de derivados?\nIsso pode demorar alguns segundos.",
        )
        if not result:
            return

        self.status_bar.config(text="Atualizando dados via pipeline...")
        self._set_details_update_status(
            f"Pipeline iniciado às {datetime.now():%H:%M:%S}",
            color="blue",
        )

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

            feedback = self._build_pipeline_feedback_message(res.stdout or "")
            status_msg = self._build_pipeline_status_message(res.stdout or "")

            messagebox.showinfo("Atualização concluída", feedback)
            self.refresh_data(source="pipeline")
            self.status_bar.config(text=status_msg)
            self._set_details_update_status(
                f"Pipeline concluído às {datetime.now():%H:%M:%S}",
                color="green",
            )

        except subprocess.CalledProcessError as e:
            messagebox.showerror(
                "Erro",
                "Pipeline falhou:\n\nSTDOUT:\n"
                + (e.stdout or "")
                + "\n\nSTDERR:\n"
                + (e.stderr or ""),
            )
            self.status_bar.config(text="Atualização de dados falhou")
            self._set_details_update_status(
                f"Pipeline falhou às {datetime.now():%H:%M:%S}",
                color="red",
            )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar dados: {e}")
            self.status_bar.config(text="Erro ao atualizar dados")
            self._set_details_update_status(
                f"Erro ao atualizar dados às {datetime.now():%H:%M:%S}",
                color="red",
            )

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

    def _fetch_structure_temporal_audit_for_details(self, structure_id):
        """
        Busca datas operacionais da estrutura a partir dos snapshots em derived.db.

        Retorna:
        - created_at: primeiro snapshot conhecido em structure_decisions
        - updated_at: último snapshot conhecido em structure_decisions
        """
        if structure_id in (None, ""):
            return {}

        try:
            sid = int(structure_id)
        except Exception:
            return {}

        # Preferência: reaproveitar o DetailsPanel, que já sabe localizar derived.db.
        try:
            panel = getattr(self, "details_panel", None)
            if panel is not None and hasattr(panel, "_fetch_audit_info_from_derived"):
                info = panel._fetch_audit_info_from_derived(sid) or {}
                return {
                    "created_at": info.get("created_at"),
                    "updated_at": info.get("updated_at"),
                }
        except Exception:
            pass

        # Fallback direto no banco.
        try:
            import importlib
            from pathlib import Path as _Path

            sqlite3 = importlib.import_module("sqlite3")

            candidates = []

            for attr in ("derived_db_path", "db_path", "derived_db"):
                val = getattr(self, attr, None)
                if val:
                    candidates.append(_Path(val))

            candidates.append(_Path("dados") / "derived.db")
            candidates.append(_Path("data") / "derived.db")
            candidates.append(_Path("derived.db"))

            db_path = next((p for p in candidates if p.exists()), None)
            if db_path is None:
                return {}

            with sqlite3.connect(str(db_path)) as conn:
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()

                created_row = cur.execute(
                    """
                    SELECT timestamp, created_at
                    FROM structure_decisions
                    WHERE structure_id = ?
                    ORDER BY datetime(timestamp) ASC, id ASC
                    LIMIT 1
                    """,
                    (sid,),
                ).fetchone()

                updated_row = cur.execute(
                    """
                    SELECT timestamp, created_at
                    FROM structure_decisions
                    WHERE structure_id = ?
                    ORDER BY datetime(timestamp) DESC, id DESC
                    LIMIT 1
                    """,
                    (sid,),
                ).fetchone()

                created_at = None
                updated_at = None

                if created_row:
                    created_at = created_row["timestamp"] or created_row["created_at"]

                if updated_row:
                    updated_at = updated_row["timestamp"] or updated_row["created_at"]

                return {
                    "created_at": created_at,
                    "updated_at": updated_at,
                }

        except Exception:
            return {}


    def _on_structure_selected(self, structure: Optional[Dict]):
        """Exibe detalhes da estrutura selecionada no painel direito."""
        txt = self._struct_detail_text
        txt.config(state="normal")
        txt.delete("1.0", "end")

        if structure is None:
            txt.insert("end", "Nenhuma estrutura selecionada.")
        else:
            audit_dates = self._fetch_structure_temporal_audit_for_details(
                structure.get("id") or structure.get("structure_id")
            )
            created_at_display = audit_dates.get("created_at") or structure.get("created_at", "")
            updated_at_display = audit_dates.get("updated_at") or structure.get("updated_at", "")

            try:
                from core.datetime_utils import format_datetime_local
                created_at_display = format_datetime_local(created_at_display, default="")
                updated_at_display = format_datetime_local(updated_at_display, default="")
            except Exception:
                created_at_display = str(created_at_display)[:19] if created_at_display else ""
                updated_at_display = str(updated_at_display)[:19] if updated_at_display else ""

            legs = structure.get("legs", [])
            lines = [
                f"ID         : {structure.get('id')}",
                f"Nome       : {structure.get('name')}",
                f"Ativo      : {structure.get('underlying_asset')}",
                f"Aba legado : {structure.get('alias_legacy_aba') or '--'}",
                f"Status     : {structure.get('status')}",
                f"Criado em  : {created_at_display or '--'}",
                f"Atualizado : {updated_at_display or '--'}",
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
            saved_structure_id = getattr(dlg, "saved_structure_id", None) or structure_id

            self.structures_list.load()

            try:
                self.status_bar.config(text="Estrutura salva com sucesso.")
            except Exception:
                pass

            if saved_structure_id is not None:
                self._reprice_structure_after_save(int(saved_structure_id))


    def _reprice_structure_after_save(self, structure_id: int) -> None:
        """
        Recalcula pricing/payoff/decisão após criação ou edição manual.

        Usa thread para não congelar a UI.
        Falhas não desfazem o cadastro da estrutura.
        """

        def _set_status(text: str) -> None:
            try:
                self.status_bar.config(text=text)
            except Exception:
                pass

        def _post_status(text: str) -> None:
            try:
                self.root.after(0, lambda: _set_status(text))
            except Exception:
                _set_status(text)

        sid = int(structure_id)
        _post_status(f"Estrutura {sid} salva. Recalculando payoff...")

        def _worker() -> None:
            try:
                # Import lazy para evitar side-effects no import da UI/testes.
                from services.canonical_pricing_facade import CanonicalPricingFacade

                facade = CanonicalPricingFacade(db_path=self._db_path)
                result = facade.execute_pricing(sid)

                if isinstance(result, dict) and result.get("status") == "error":
                    raise RuntimeError(
                        result.get("error_message") or "Erro no recálculo automático"
                    )

                def _after_success() -> None:
                    _set_status(f"Estrutura {sid} salva e payoff recalculado.")
                    try:
                        self.refresh_data()
                    except Exception:
                        pass

                try:
                    self.root.after(0, _after_success)
                except Exception:
                    _after_success()

            except Exception as exc:
                _post_status(
                    f"Estrutura {sid} salva, mas o recálculo automático falhou: {exc}"
                )

        threading.Thread(target=_worker, daemon=True).start()


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
