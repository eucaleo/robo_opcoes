# FASE 5 — INSPEÇÃO CIRÚRGICA DO FLUXO REAL EM UI/main_window.py

## Ocorrências principais

18:from tkinter import ttk, messagebox
57:        # Não executa pipeline e não recalcula payoff.
127:        self.status_bar = ttk.Label(
133:        self.status_bar.pack(side="bottom", fill="x")
143:        file_menu.add_command(label="Recarregar Tela", command=self.refresh_data)
145:        file_menu.add_command(label="Exportar CSV...", command=self.export_csv)
147:        file_menu.add_command(label="Sair", command=self.close)
152:        tools_menu.add_command(label="Executar Pipeline", command=self.run_pipeline)
153:        tools_menu.add_command(label="Verificar Bancos", command=self.check_databases)
155:        tools_menu.add_command(label="Limpar Cache", command=self.clear_cache)
160:        help_menu.add_command(label="Sobre", command=self.show_about)
174:        self.status_bar.config(text="Aplicando filtros...")
179:            self.status_bar.config(text=f"{count} decisões encontradas")
181:            messagebox.showerror("Erro", f"Erro ao aplicar filtros: {e}")
182:            self.status_bar.config(text="Erro nos filtros")
207:            self.status_bar.config(text="Dados insuficientes para payoff")
225:            self.status_bar.config(text="Carregando payoff... (cancelando anterior)")
227:            self.status_bar.config(text="Carregando payoff...")
284:    def refresh_data(self, show_errors: bool = True):
288:        self.status_bar.config(text="Carregando dados...")
342:            self.status_bar.config(
348:                messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
351:            self.status_bar.config(text="Erro ao carregar dados")
400:        """Executa uma atualização automática sem pipeline e sem recálculo."""
420:                self.status_bar.config(
441:                messagebox.showinfo("Sucesso", f"Dados exportados para {filename}")
443:                messagebox.showerror("Erro", f"Erro ao exportar: {e}")
450:        - Este botão NÃO executa o pipeline completo.
455:                self.status_bar.config(
466:                self.status_bar.config(
481:            self.status_bar.config(text=f"Recalculando estrutura {sid}...")
489:                self.status_bar.config(text=msg)
561:    def _extract_pipeline_summary(self, stdout: str) -> Dict:
562:        """Extrai o resumo JSON emitido por scripts/run_derived_pipeline.py."""
576:    def _format_pipeline_value(self, value):
582:    def _build_pipeline_feedback_message(self, stdout: str) -> str:
583:        """Monta mensagem amigável para o usuário após executar pipeline."""
584:        summary = self._extract_pipeline_summary(stdout)
588:                "Pipeline executado com sucesso.\n\n"
589:                "Resumo operacional não disponível no stdout do pipeline."
593:            "Pipeline executado com sucesso.",
596:            f"- Estruturas: {self._format_pipeline_value(summary.get('structures'))}",
597:            f"- Decisões: {self._format_pipeline_value(summary.get('decisions'))}",
598:            f"- Pontos de payoff: {self._format_pipeline_value(summary.get('payoff_points'))}",
599:            f"- Resumos de payoff: {self._format_pipeline_value(summary.get('payoff_summaries'))}",
600:            f"- Execuções de pricing: {self._format_pipeline_value(summary.get('pricing_executions'))}",
601:            f"- Cotações RTD atualizadas: {self._format_pipeline_value(summary.get('rtd_quotes_updated'))}",
602:            f"- Avisos: {self._format_pipeline_value(summary.get('warnings'))}",
603:            f"- Erros: {self._format_pipeline_value(summary.get('errors'))}",
607:    def _build_pipeline_status_message(self, stdout: str) -> str:
608:        """Monta texto curto para status bar após pipeline."""
609:        summary = self._extract_pipeline_summary(stdout)
611:            return "Pipeline executado com sucesso"
613:        decisions = self._format_pipeline_value(summary.get("decisions"))
614:        payoff_points = self._format_pipeline_value(summary.get("payoff_points"))
615:        errors = self._format_pipeline_value(summary.get("errors"))
618:            f"Pipeline OK: decisões={decisions}; "
623:    def run_pipeline(self):
624:        """Executa o pipeline de derivados."""
625:        result = messagebox.askyesno(
626:            "Executar Pipeline",
627:            "Executar pipeline de derivados?\nIsso pode demorar alguns segundos.",
632:        self.status_bar.config(text="Executando pipeline...")
636:            script_path = project_root / "scripts" / "run_derived_pipeline.py"
638:                script_path = project_root / "Scripts" / "run_derived_pipeline.py"
642:                    f"Não achei o script do pipeline em: {script_path}"
645:            import subprocess
648:            res = subprocess.run(
657:                print("[UI] Pipeline STDOUT:\n", res.stdout)
659:                print("[UI] Pipeline STDERR:\n", res.stderr)
661:            feedback = self._build_pipeline_feedback_message(res.stdout or "")
662:            status_msg = self._build_pipeline_status_message(res.stdout or "")
664:            messagebox.showinfo("Sucesso", feedback)
666:            self.status_bar.config(text=status_msg)
668:        except subprocess.CalledProcessError as e:
669:            messagebox.showerror(
671:                "Pipeline falhou:\n\nSTDOUT:\n"
676:            self.status_bar.config(text="Pipeline falhou")
678:            messagebox.showerror("Erro", f"Erro ao executar pipeline: {e}")
679:            self.status_bar.config(text="Erro ao executar pipeline")
685:            messagebox.showinfo("Status dos Bancos", status)
687:            messagebox.showerror("Erro", f"Erro ao verificar bancos: {e}")
692:        messagebox.showinfo("Cache", "Cache limpo com sucesso")
699:Pipeline automático de payoff e decisões
708:        messagebox.showinfo("Sobre", about_text)
753:                self.status_bar.config(text=msg)
756:                self.status_bar.config(text="Sem dados de payoff para esta seleção")
769:        self.status_bar.config(text=f"Erro ao carregar payoff: {error_msg}")
786:            self.status_bar.config(text=f"{char} {base_text}")
882:                self.status_bar.config(text="Estrutura salva com sucesso.")
900:                self.status_bar.config(text=text)

## Trecho menus/botões

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


## Trecho refresh_data

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

    def refresh_data(self, show_errors: bool = True):
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
            if show_errors:
                messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
            else:
                print(f"[UI] Erro na atualização automática: {e}")
            self.status_bar.config(text="Erro ao carregar dados")

    def close(self):
        """Fecha a janela cancelando agendamentos automáticos pendentes."""
        self._closing = True
        self.stop_auto_refresh()
        try:
            self.root.quit()
        except Exception:
            pass

## Trecho resumo/pipeline

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
                self.root.after(0, self.refresh_data)
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

            feedback = self._build_pipeline_feedback_message(res.stdout or "")
            status_msg = self._build_pipeline_status_message(res.stdout or "")

            messagebox.showinfo("Sucesso", feedback)
            self.refresh_data()
            self.status_bar.config(text=status_msg)

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

## Trecho pós-pipeline / atualização da UI

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
