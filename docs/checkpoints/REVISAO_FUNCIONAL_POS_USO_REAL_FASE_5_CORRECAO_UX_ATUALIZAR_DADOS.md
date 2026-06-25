# FASE 5 — CORREÇÃO UX ATUALIZAR DADOS

## Decisão

- O menu funcional que executa o pipeline era Ferramentas > Executar Pipeline.
- O fluxo de Recarregar Tela permanece separado e apenas recarrega a UI.
- A ação principal foi renomeada para Atualizar Dados, mantendo o handler run_pipeline.

## Evidência em UI/main_window.py

70:        self.refresh_data()
143:        file_menu.add_command(label="Recarregar Tela", command=self.refresh_data)
152:        tools_menu.add_command(label="Atualizar Dados", command=self.run_pipeline)
164:        self.root.bind("<F5>", lambda e: self.refresh_data())
284:    def refresh_data(self, show_errors: bool = True):
418:            self.refresh_data(show_errors=False)
545:                self.root.after(0, self.refresh_data)
588:                "Pipeline executado com sucesso.\n\n"
593:            "Pipeline executado com sucesso.",
611:            return "Pipeline executado com sucesso"
623:    def run_pipeline(self):
626:            "Atualizar Dados",
632:        self.status_bar.config(text="Atualizando dados via pipeline...")
664:            messagebox.showinfo("Atualização concluída", feedback)
665:            self.refresh_data()
678:            messagebox.showerror("Erro", f"Erro ao atualizar dados: {e}")
679:            self.status_bar.config(text="Erro ao atualizar dados")
929:                        self.refresh_data()

## Trecho menus

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

## Trecho run_pipeline

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
            self.status_bar.config(text="Atualização de dados falhou")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar dados: {e}")
            self.status_bar.config(text="Erro ao atualizar dados")

    def check_databases(self):
        """Verifica status dos bancos de dados."""
