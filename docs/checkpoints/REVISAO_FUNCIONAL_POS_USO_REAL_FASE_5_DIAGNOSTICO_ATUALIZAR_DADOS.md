# DIAGNÓSTICO FASE 5 — BOTÃO ATUALIZAR DADOS

## Status

Diagnóstico gerado automaticamente.

## Diretórios analisados

- UI
- scripts
- repositories
- services
- ATT

## Candidatos de botão

UI/components/details_panel.py:694:            self._refresh_operational_state_for_structure(structure_id)
UI/components/details_panel.py:854:    def _refresh_operational_state_for_structure(self, structure_id):
UI/components/details_panel.py:1023:    def _refresh_current_from_derived(self, structure_id):
UI/components/structure_editor_dialog.py:280:        self._refresh_leg_tree()
UI/components/structure_editor_dialog.py:286:    def _refresh_leg_tree(self):
UI/components/structure_editor_dialog.py:344:        self._refresh_leg_tree()
UI/components/structure_editor_dialog.py:367:        self._refresh_leg_tree()
UI/components/structure_editor_dialog.py:380:        self._refresh_leg_tree()
UI/components/structure_editor_dialog.py:434:                self._refresh_rtd_quote_for_symbol(symbol)
UI/components/structure_editor_dialog.py:446:    def _refresh_rtd_quote_for_symbol(self, symbol: str) -> None:
UI/components/structure_editor_dialog.py:459:        script = project_root / "scripts" / "refresh_rtd_symbol_to_option_quotes_fallback.py"
UI/components/structure_editor_dialog.py:474:            raise ValueError(f"Script de refresh RTD não encontrado: {script}")
UI/components/structure_editor_dialog.py:515:                "Não foi possível atualizar a cotação RTD para "
UI/components/structure_editor_dialog.py:586:            self._refresh_leg_tree()
UI/components/structure_editor_dialog.py:613:            self._refresh_leg_tree()
UI/main_window.py:49:        # Última decisão selecionada (preservada entre refreshes)
UI/main_window.py:58:        self._auto_refresh_interval_ms = 30000
UI/main_window.py:59:        self._auto_refresh_enabled = True
UI/main_window.py:60:        self._auto_refresh_in_progress = False
UI/main_window.py:61:        self._auto_refresh_after_id = None
UI/main_window.py:70:        self.refresh_data()
UI/main_window.py:73:        self.start_auto_refresh()
UI/main_window.py:143:        file_menu.add_command(label="Recarregar Tela", command=self.refresh_data)
UI/main_window.py:164:        self.root.bind("<F5>", lambda e: self.refresh_data())
UI/main_window.py:193:        # Atualizar painel de detalhes (síncrono, leve)
UI/main_window.py:197:            print(f"[UI] Erro ao atualizar detalhes: {e}")
UI/main_window.py:284:    def refresh_data(self, show_errors: bool = True):
UI/main_window.py:290:            self.data_model.refresh()
UI/main_window.py:356:        self.stop_auto_refresh()
UI/main_window.py:362:    def start_auto_refresh(self):
UI/main_window.py:364:        self._auto_refresh_enabled = True
UI/main_window.py:365:        self._schedule_auto_refresh()
UI/main_window.py:367:    def stop_auto_refresh(self):
UI/main_window.py:369:        self._auto_refresh_enabled = False
UI/main_window.py:370:        after_id = getattr(self, "_auto_refresh_after_id", None)
UI/main_window.py:371:        self._auto_refresh_after_id = None
UI/main_window.py:379:    def _schedule_auto_refresh(self):
UI/main_window.py:382:            not getattr(self, "_auto_refresh_enabled", False)
UI/main_window.py:387:        previous_after_id = getattr(self, "_auto_refresh_after_id", None)
UI/main_window.py:394:        self._auto_refresh_after_id = self.root.after(
UI/main_window.py:395:            self._auto_refresh_interval_ms,
UI/main_window.py:396:            self._auto_refresh_tick,
UI/main_window.py:399:    def _auto_refresh_tick(self):
UI/main_window.py:401:        self._auto_refresh_after_id = None
UI/main_window.py:404:            not getattr(self, "_auto_refresh_enabled", False)
UI/main_window.py:410:            getattr(self, "_auto_refresh_in_progress", False)
UI/main_window.py:413:            self._schedule_auto_refresh()
UI/main_window.py:416:        self._auto_refresh_in_progress = True
UI/main_window.py:418:            self.refresh_data(show_errors=False)
UI/main_window.py:426:            self._auto_refresh_in_progress = False
UI/main_window.py:427:            self._schedule_auto_refresh()
UI/main_window.py:545:                self.root.after(0, self.refresh_data)
UI/main_window.py:665:            self.refresh_data()
UI/main_window.py:929:                        self.refresh_data()
UI/models/ui_data.py:202:    def refresh(self):
UI/models/ui_data.py:254:            self.refresh()
UI/models/ui_data.py:488:            self.refresh()
UI/models/ui_data.py:623:        self.refresh()
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:267:- Toda fase encerrada deve atualizar evidencias em docs.
scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:4:EVID="docs/checkpoints/evidencias/fase-4-diagnostico-atualizar-dados-limpo.txt"
scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:25:  grep -n "Atualizar Dados\|Executar Pipeline\|def refresh_data\|def run_pipeline\|Pipeline executado\|status_bar.config" UI/main_window.py || true
scripts/fase-5-diagnostico-rtd.sh:27:  echo "== Busca por handlers Atualizar Dados / Pipeline =="
scripts/fase-5-diagnostico-rtd.sh:29:    -E "Atualizar Dados|refresh_data|run_pipeline|Executar Pipeline" UI scripts services db repositories domain . 2>/dev/null | head -300
scripts/fase-5-diagnostico-rtd.sh:132:  echo "== Trecho UI/main_window.py refresh_data e run_pipeline =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:53:    scripts/run_rtd_refresh_full.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:55:    scripts/refresh_rtd_option_quotes_excel.ps1 \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:74:    scripts/run_rtd_refresh_full.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:180:    -E "Excel.Application|Workbooks|RefreshAll|RTD|LISTA_RTD|RTD_LINKS|win32com|powershell|Start-Process" \
scripts/fase-5c-restaurar-rtd-historico.sh:16:  "scripts/refresh_rtd_option_quotes_excel.ps1"
scripts/fase-5c-restaurar-rtd-historico.sh:19:  "scripts/run_rtd_refresh_full.py"
scripts/fase-5c-restaurar-rtd-historico.sh:75:    scripts/run_rtd_refresh_full.py
scripts/fase-5c-restaurar-rtd-historico.sh:87:  if [ -f scripts/refresh_rtd_option_quotes_excel.ps1 ]; then
scripts/fase-5c-restaurar-rtd-historico.sh:88:    sed -n '1,220p' scripts/refresh_rtd_option_quotes_excel.ps1
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:51:  grep -R "RTD\\|rtd\\|Atualizar Dados\\|Executar Pipeline" -n \
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:62:  find ATT/tests -type f | grep -Ei "derived|pipeline|orchestrator|refresh|rtd" | sort
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:85:    - Não aciona Excel, PowerShell, COM ou refresh RTD ao vivo.
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:462:    assert "refresh_rtd_option_quotes_excel" not in command_text
scripts/fase-diagnostico-recalc-pipeline-inicializacao.sh:8:  echo "== Diagnóstico: recalc/pipeline em inicialização e refresh =="
scripts/fase-diagnostico-recalc-pipeline-inicializacao.sh:27:  echo "== Trecho UI/main_window.py: init/menu/bind/refresh/auto-refresh/recalc =="
scripts/fase5_automacao_gitbash.sh:18:BUSCA_SCRIPT="$SCRIPTS_DIR/fase5_buscar_fluxo_atualizar_dados.sh"
scripts/fase5_automacao_gitbash.sh:59:Auditar e melhorar o comportamento do botão Atualizar Dados, garantindo que a ação executada pelo usuário seja rastreável, compreensível e verificável.
scripts/fase5_automacao_gitbash.sh:89:O botão Atualizar Dados pode executar ações importantes do pipeline, mas o usuário pode não receber feedback suficiente sobre o resultado.
scripts/fase5_automacao_gitbash.sh:117:1. Onde está o botão Atualizar Dados.
scripts/fase5_automacao_gitbash.sh:153:    scripts/run_rtd_refresh_full.py
scripts/fase5_automacao_gitbash.sh:154:    scripts/refresh_rtd_option_quotes_excel.ps1
scripts/fase5_automacao_gitbash.sh:164:    scripts/refresh_rtd_symbol_to_option_quotes.py
scripts/fase5_automacao_gitbash.sh:172:| Botão Atualizar Dados localizado | A validar |
scripts/fase5_automacao_gitbash.sh:192:1. Localizar o botão Atualizar Dados na interface.
scripts/fase5_automacao_gitbash.sh:202:11. Atualizar auditoria.
scripts/fase5_automacao_gitbash.sh:212:A prioridade inicial é diagnosticar o fluxo real do botão Atualizar Dados e confirmar quais pipelines ele aciona.
scripts/fase5_automacao_gitbash.sh:275:    Fase 5 — Atualizar Dados e Resumo do Pipeline
scripts/fase5_automacao_gitbash.sh:316:    Fase 5 — Atualizar Dados e Resumo do Pipeline
scripts/fase5_automacao_gitbash.sh:386:  run_grep "Atualizar Dados|atualizar dados|Atualizar|atualizar|Refresh|refresh"
scripts/fase5_automacao_gitbash.sh:389:  run_grep "clicked.connect|command=|on_click|callback|handler|handle|atualizar|refresh"
scripts/fase5_automacao_gitbash.sh:392:  run_grep "run_derived_pipeline|run_rtd_option_quotes_pipeline|run_rtd_refresh_full|payoff_curve_points|structure_decisions|RTD|rtd|payoff|decision|decisions"
scripts/fase5_automacao_gitbash.sh:398:  echo "- Confirmar qual ocorrência representa o botão real Atualizar Dados."
scripts/fase5_automacao_gitbash.sh:422:  "scripts/run_rtd_refresh_full.py"
scripts/fase5_automacao_gitbash.sh:518:  echo "A Fase 5 deve garantir que o botão Atualizar Dados tenha retorno claro para:"
scripts/fase5_automacao_gitbash.sh:558:  commit_if_needed "docs: fecha fase 4 e abre fase 5 atualizar dados"
scripts/fase5_automacao_gitbash.sh:571:  commit_if_needed "chore: adiciona verificadores fase 5 atualizar dados"
scripts/fase5_buscar_fluxo_atualizar_dados.sh:57:  run_grep "Atualizar Dados|atualizar dados|Atualizar|atualizar|Refresh|refresh"
scripts/fase5_buscar_fluxo_atualizar_dados.sh:60:  run_grep "clicked.connect|command=|on_click|callback|handler|handle|atualizar|refresh"
scripts/fase5_buscar_fluxo_atualizar_dados.sh:63:  run_grep "run_derived_pipeline|run_rtd_option_quotes_pipeline|run_rtd_refresh_full|payoff_curve_points|structure_decisions|RTD|rtd|payoff|decision|decisions"
scripts/fase5_buscar_fluxo_atualizar_dados.sh:69:  echo "- Confirmar qual ocorrência representa o botão real Atualizar Dados."
scripts/fase5_checar_resumo_pipeline.sh:13:  "scripts/run_rtd_refresh_full.py"
scripts/fase5_checar_resumo_pipeline.sh:109:  echo "A Fase 5 deve garantir que o botão Atualizar Dados tenha retorno claro para:"
scripts/import_lista_rtd_excel_to_option_quotes.py:220:    - aguarda RTD atualizar;
scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:10:BASE_SCRIPT = Path(__file__).resolve().with_name("refresh_rtd_symbol_to_option_quotes.py")
scripts/run_derived_pipeline.py:77:    - Não aciona Excel, PowerShell, COM ou refresh RTD ao vivo.
scripts/run_rtd_refresh_full.py:76:        description="Pipeline completo: gerar símbolos RTD, atualizar Excel/CSV e importar cotações no SQLite."
scripts/run_rtd_refresh_full.py:87:    parser.add_argument("--skip-excel", action="store_true", help="Pula o refresh do Excel e importa o CSV existente.")
scripts/run_rtd_refresh_full.py:101:    ps1_script = Path("scripts/refresh_rtd_option_quotes_excel.ps1")
scripts/run_rtd_refresh_full.py:103:    print("=== RTD Refresh Full ===")
scripts/run_rtd_refresh_full.py:241:            print("Pipeline interrompido no refresh Excel/RTD.")
scripts/run_rtd_refresh_full.py:245:        print("Refresh Excel/RTD pulado por --skip-excel.")
ATT/tests/test_run_derived_pipeline_rtd_integration.py:112:    assert "refresh_rtd_option_quotes_excel" not in command_text
ATT/tests/test_ui_data_migration.py:22:    m.refresh()

## Candidatos de handler

UI/components/decisions_grid.py:73:        v_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
UI/components/decisions_grid.py:74:        self.tree.configure(yscrollcommand=v_scrollbar.set)
UI/components/decisions_grid.py:76:        h_scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
UI/components/decisions_grid.py:77:        self.tree.configure(xscrollcommand=h_scrollbar.set)
UI/components/details_panel.py:628:            command=self._on_recalculate_click,
UI/components/details_panel.py:694:            self._refresh_operational_state_for_structure(structure_id)
UI/components/details_panel.py:854:    def _refresh_operational_state_for_structure(self, structure_id):
UI/components/details_panel.py:1023:    def _refresh_current_from_derived(self, structure_id):
UI/components/details_panel.py:1091:            text="Recalc indisponível: callback não configurado",
UI/components/filters_panel.py:83:            btn_frame, text="Aplicar", command=self._apply_filters
UI/components/filters_panel.py:88:            btn_frame, text="Limpar", command=self.reset_filters
UI/components/payoff_chart.py:81:            top, text="Exportar PNG", command=self.export_png
UI/components/payoff_chart.py:86:            top, text="Fixar Curva A", command=self.fix_current_curve
UI/components/payoff_chart.py:91:            top, text="Limpar Comparação", command=self.clear_comparison
UI/components/structures_list_panel.py:100:                   command=self.load).pack(side="left")
UI/components/structures_list_panel.py:117:                               command=lambda c=col: self._sort_by(c))
UI/components/structures_list_panel.py:122:        vsb = ttk.Scrollbar(frame, orient="vertical",   command=self._tree.yview)
UI/components/structures_list_panel.py:123:        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self._tree.xview)
UI/components/structures_list_panel.py:124:        self._tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
UI/components/structures_list_panel.py:148:            ttk.Button(btn_bar, text=label, command=cmd).pack(
UI/components/structure_editor_dialog.py:151:        ttk.Button(leg_toolbar, text="+ Leg",    command=self._cmd_add_leg).pack(side="left", padx=2)
UI/components/structure_editor_dialog.py:152:        ttk.Button(leg_toolbar, text="Remover",  command=self._cmd_remove_leg).pack(side="left", padx=2)
UI/components/structure_editor_dialog.py:153:        ttk.Button(leg_toolbar, text="▲",        command=lambda: self._cmd_move_leg(-1)).pack(side="left", padx=1)
UI/components/structure_editor_dialog.py:154:        ttk.Button(leg_toolbar, text="▼",        command=lambda: self._cmd_move_leg(+1)).pack(side="left", padx=1)
UI/components/structure_editor_dialog.py:175:        leg_vsb = ttk.Scrollbar(leg_frame, orient="vertical", command=self._leg_tree.yview)
UI/components/structure_editor_dialog.py:176:        self._leg_tree.configure(yscrollcommand=leg_vsb.set)
UI/components/structure_editor_dialog.py:188:        ttk.Button(btn_bar, text="Cancelar",      command=self.destroy).pack(side="right", padx=4)
UI/components/structure_editor_dialog.py:189:        ttk.Button(btn_bar, text="[SAVE] Salvar", command=self._cmd_save).pack(side="right", padx=4)
UI/components/structure_editor_dialog.py:244:            command=self._cmd_enrich_current_leg,
UI/components/structure_editor_dialog.py:250:            command=self._cmd_apply_leg,
UI/components/structure_editor_dialog.py:280:        self._refresh_leg_tree()
UI/components/structure_editor_dialog.py:286:    def _refresh_leg_tree(self):
UI/components/structure_editor_dialog.py:344:        self._refresh_leg_tree()
UI/components/structure_editor_dialog.py:367:        self._refresh_leg_tree()
UI/components/structure_editor_dialog.py:380:        self._refresh_leg_tree()
UI/components/structure_editor_dialog.py:434:                self._refresh_rtd_quote_for_symbol(symbol)
UI/components/structure_editor_dialog.py:446:    def _refresh_rtd_quote_for_symbol(self, symbol: str) -> None:
UI/components/structure_editor_dialog.py:459:        script = project_root / "scripts" / "refresh_rtd_symbol_to_option_quotes_fallback.py"
UI/components/structure_editor_dialog.py:474:            raise ValueError(f"Script de refresh RTD não encontrado: {script}")
UI/components/structure_editor_dialog.py:515:                "Não foi possível atualizar a cotação RTD para "
UI/components/structure_editor_dialog.py:586:            self._refresh_leg_tree()
UI/components/structure_editor_dialog.py:613:            self._refresh_leg_tree()
UI/main_window.py:49:        # Última decisão selecionada (preservada entre refreshes)
UI/main_window.py:58:        self._auto_refresh_interval_ms = 30000
UI/main_window.py:59:        self._auto_refresh_enabled = True
UI/main_window.py:60:        self._auto_refresh_in_progress = False
UI/main_window.py:61:        self._auto_refresh_after_id = None
UI/main_window.py:70:        self.refresh_data()
UI/main_window.py:73:        self.start_auto_refresh()
UI/main_window.py:143:        file_menu.add_command(label="Recarregar Tela", command=self.refresh_data)
UI/main_window.py:145:        file_menu.add_command(label="Exportar CSV...", command=self.export_csv)
UI/main_window.py:147:        file_menu.add_command(label="Sair", command=self.close)
UI/main_window.py:152:        tools_menu.add_command(label="Executar Pipeline", command=self.run_pipeline)
UI/main_window.py:153:        tools_menu.add_command(label="Verificar Bancos", command=self.check_databases)
UI/main_window.py:155:        tools_menu.add_command(label="Limpar Cache", command=self.clear_cache)
UI/main_window.py:160:        help_menu.add_command(label="Sobre", command=self.show_about)
UI/main_window.py:164:        self.root.bind("<F5>", lambda e: self.refresh_data())
UI/main_window.py:197:            print(f"[UI] Erro ao atualizar detalhes: {e}")
UI/main_window.py:276:                        self._handle_payoff_error,
UI/main_window.py:284:    def refresh_data(self, show_errors: bool = True):
UI/main_window.py:290:            self.data_model.refresh()
UI/main_window.py:356:        self.stop_auto_refresh()
UI/main_window.py:362:    def start_auto_refresh(self):
UI/main_window.py:364:        self._auto_refresh_enabled = True
UI/main_window.py:365:        self._schedule_auto_refresh()
UI/main_window.py:367:    def stop_auto_refresh(self):
UI/main_window.py:369:        self._auto_refresh_enabled = False
UI/main_window.py:370:        after_id = getattr(self, "_auto_refresh_after_id", None)
UI/main_window.py:371:        self._auto_refresh_after_id = None
UI/main_window.py:379:    def _schedule_auto_refresh(self):
UI/main_window.py:382:            not getattr(self, "_auto_refresh_enabled", False)
UI/main_window.py:387:        previous_after_id = getattr(self, "_auto_refresh_after_id", None)
UI/main_window.py:394:        self._auto_refresh_after_id = self.root.after(
UI/main_window.py:395:            self._auto_refresh_interval_ms,
UI/main_window.py:396:            self._auto_refresh_tick,
UI/main_window.py:399:    def _auto_refresh_tick(self):
UI/main_window.py:401:        self._auto_refresh_after_id = None
UI/main_window.py:404:            not getattr(self, "_auto_refresh_enabled", False)
UI/main_window.py:410:            getattr(self, "_auto_refresh_in_progress", False)
UI/main_window.py:413:            self._schedule_auto_refresh()
UI/main_window.py:416:        self._auto_refresh_in_progress = True
UI/main_window.py:418:            self.refresh_data(show_errors=False)
UI/main_window.py:426:            self._auto_refresh_in_progress = False
UI/main_window.py:427:            self._schedule_auto_refresh()
UI/main_window.py:545:                self.root.after(0, self.refresh_data)
UI/main_window.py:665:            self.refresh_data()
UI/main_window.py:758:            self._handle_payoff_error(str(e), worker_id)
UI/main_window.py:760:    def _handle_payoff_error(self, error_msg: str, worker_id: int):
UI/main_window.py:929:                        self.refresh_data()
UI/models/ui_data.py:202:    def refresh(self):
UI/models/ui_data.py:254:            self.refresh()
UI/models/ui_data.py:488:            self.refresh()
UI/models/ui_data.py:623:        self.refresh()
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:267:- Toda fase encerrada deve atualizar evidencias em docs.
scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:4:EVID="docs/checkpoints/evidencias/fase-4-diagnostico-atualizar-dados-limpo.txt"
scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:24:  echo "== UI/main_window.py menus e handlers principais =="
scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:25:  grep -n "Atualizar Dados\|Executar Pipeline\|def refresh_data\|def run_pipeline\|Pipeline executado\|status_bar.config" UI/main_window.py || true
scripts/fase-5-diagnostico-rtd.sh:27:  echo "== Busca por handlers Atualizar Dados / Pipeline =="
scripts/fase-5-diagnostico-rtd.sh:29:    -E "Atualizar Dados|refresh_data|run_pipeline|Executar Pipeline" UI scripts services db repositories domain . 2>/dev/null | head -300
scripts/fase-5-diagnostico-rtd.sh:132:  echo "== Trecho UI/main_window.py refresh_data e run_pipeline =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:53:    scripts/run_rtd_refresh_full.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:55:    scripts/refresh_rtd_option_quotes_excel.ps1 \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:74:    scripts/run_rtd_refresh_full.py \
scripts/fase-5c-restaurar-rtd-historico.sh:16:  "scripts/refresh_rtd_option_quotes_excel.ps1"
scripts/fase-5c-restaurar-rtd-historico.sh:19:  "scripts/run_rtd_refresh_full.py"
scripts/fase-5c-restaurar-rtd-historico.sh:75:    scripts/run_rtd_refresh_full.py
scripts/fase-5c-restaurar-rtd-historico.sh:87:  if [ -f scripts/refresh_rtd_option_quotes_excel.ps1 ]; then
scripts/fase-5c-restaurar-rtd-historico.sh:88:    sed -n '1,220p' scripts/refresh_rtd_option_quotes_excel.ps1
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:62:  find ATT/tests -type f | grep -Ei "derived|pipeline|orchestrator|refresh|rtd" | sort
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:85:    - Não aciona Excel, PowerShell, COM ou refresh RTD ao vivo.
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:462:    assert "refresh_rtd_option_quotes_excel" not in command_text
scripts/fase-diagnostico-recalc-pipeline-inicializacao.sh:8:  echo "== Diagnóstico: recalc/pipeline em inicialização e refresh =="
scripts/fase-diagnostico-recalc-pipeline-inicializacao.sh:27:  echo "== Trecho UI/main_window.py: init/menu/bind/refresh/auto-refresh/recalc =="
scripts/fase-diagnostico-recalc-pipeline-inicializacao.sh:37:  echo "== Trecho UI/components/details_panel.py: botão e callback de recálculo =="
scripts/fase5_automacao_gitbash.sh:18:BUSCA_SCRIPT="$SCRIPTS_DIR/fase5_buscar_fluxo_atualizar_dados.sh"
scripts/fase5_automacao_gitbash.sh:153:    scripts/run_rtd_refresh_full.py
scripts/fase5_automacao_gitbash.sh:154:    scripts/refresh_rtd_option_quotes_excel.ps1
scripts/fase5_automacao_gitbash.sh:164:    scripts/refresh_rtd_symbol_to_option_quotes.py
scripts/fase5_automacao_gitbash.sh:193:2. Identificar o handler chamado pelo botão.
scripts/fase5_automacao_gitbash.sh:386:  run_grep "Atualizar Dados|atualizar dados|Atualizar|atualizar|Refresh|refresh"
scripts/fase5_automacao_gitbash.sh:388:  write_section "Candidatos de handler"
scripts/fase5_automacao_gitbash.sh:389:  run_grep "clicked.connect|command=|on_click|callback|handler|handle|atualizar|refresh"
scripts/fase5_automacao_gitbash.sh:392:  run_grep "run_derived_pipeline|run_rtd_option_quotes_pipeline|run_rtd_refresh_full|payoff_curve_points|structure_decisions|RTD|rtd|payoff|decision|decisions"
scripts/fase5_automacao_gitbash.sh:399:  echo "- Confirmar o handler chamado pelo clique."
scripts/fase5_automacao_gitbash.sh:422:  "scripts/run_rtd_refresh_full.py"
scripts/fase5_automacao_gitbash.sh:558:  commit_if_needed "docs: fecha fase 4 e abre fase 5 atualizar dados"
scripts/fase5_automacao_gitbash.sh:571:  commit_if_needed "chore: adiciona verificadores fase 5 atualizar dados"
scripts/fase5_buscar_fluxo_atualizar_dados.sh:57:  run_grep "Atualizar Dados|atualizar dados|Atualizar|atualizar|Refresh|refresh"
scripts/fase5_buscar_fluxo_atualizar_dados.sh:59:  write_section "Candidatos de handler"
scripts/fase5_buscar_fluxo_atualizar_dados.sh:60:  run_grep "clicked.connect|command=|on_click|callback|handler|handle|atualizar|refresh"
scripts/fase5_buscar_fluxo_atualizar_dados.sh:63:  run_grep "run_derived_pipeline|run_rtd_option_quotes_pipeline|run_rtd_refresh_full|payoff_curve_points|structure_decisions|RTD|rtd|payoff|decision|decisions"
scripts/fase5_buscar_fluxo_atualizar_dados.sh:70:  echo "- Confirmar o handler chamado pelo clique."
scripts/fase5_checar_resumo_pipeline.sh:13:  "scripts/run_rtd_refresh_full.py"
scripts/import_lista_rtd_excel_to_option_quotes.py:220:    - aguarda RTD atualizar;
scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:10:BASE_SCRIPT = Path(__file__).resolve().with_name("refresh_rtd_symbol_to_option_quotes.py")
scripts/run_derived_pipeline.py:77:    - Não aciona Excel, PowerShell, COM ou refresh RTD ao vivo.
scripts/run_rtd_refresh_full.py:76:        description="Pipeline completo: gerar símbolos RTD, atualizar Excel/CSV e importar cotações no SQLite."
scripts/run_rtd_refresh_full.py:87:    parser.add_argument("--skip-excel", action="store_true", help="Pula o refresh do Excel e importa o CSV existente.")
scripts/run_rtd_refresh_full.py:101:    ps1_script = Path("scripts/refresh_rtd_option_quotes_excel.ps1")
scripts/run_rtd_refresh_full.py:241:            print("Pipeline interrompido no refresh Excel/RTD.")
ATT/tests/test_run_derived_pipeline_rtd_integration.py:112:    assert "refresh_rtd_option_quotes_excel" not in command_text
ATT/tests/test_ui_data_migration.py:22:    m.refresh()

## Candidatos de pipeline

UI/components/decisions_grid.py:1:# UI/components/decisions_grid.py
UI/components/decisions_grid.py:27:            "decision",
UI/components/decisions_grid.py:45:        self.tree.heading("decision", text="Decisão")
UI/components/decisions_grid.py:55:        self.tree.column("decision", width=100, anchor="center")
UI/components/decisions_grid.py:100:    def update_data(self, decisions: List[Dict]):
UI/components/decisions_grid.py:102:        self.current_data = decisions.copy()
UI/components/decisions_grid.py:107:        for i, decision in enumerate(decisions, 1):
UI/components/decisions_grid.py:108:            timestamp = self._format_timestamp(decision.get("timestamp"))
UI/components/decisions_grid.py:111:                decision.get("structure_id") or decision.get("aba") or "N/A"
UI/components/decisions_grid.py:113:            decision_text = decision.get("decision", "N/A")
UI/components/decisions_grid.py:114:            level = decision.get("level", "")
UI/components/decisions_grid.py:115:            ratio = self._format_ratio(decision.get("pl_pct_of_max"))
UI/components/decisions_grid.py:116:            dte = decision.get("dte_min", "")
UI/components/decisions_grid.py:117:            pl_atual = self._format_currency(decision.get("pl_atual"))
UI/components/decisions_grid.py:118:            pl_max = self._format_currency(decision.get("pl_max"))
UI/components/decisions_grid.py:121:                decision_text
UI/components/decisions_grid.py:122:                if decision_text in ["HOLD", "PREPARE_ROLL", "CLOSE_REOPEN", "ROLL", "ENTER"]
UI/components/decisions_grid.py:133:                    decision_text,
UI/components/decisions_grid.py:181:    def get_selected_decision(self) -> Optional[Dict]:
UI/components/details_panel.py:17:        self._current_decision = None
UI/components/details_panel.py:410:            "structure_decisions",
UI/components/details_panel.py:411:            "payoff_curve_points",
UI/components/details_panel.py:482:        self.decision_label = ttk.Label(
UI/components/details_panel.py:485:        self.decision_label.grid(row=1, column=1, sticky="ew", padx=(0, 10))
UI/components/details_panel.py:641:    def update_decision(self, decision_data: Dict):
UI/components/details_panel.py:642:        self._current_decision = dict(decision_data) if decision_data else None
UI/components/details_panel.py:644:        self.timestamp_label.config(text=decision_data.get("timestamp", "N/A"))
UI/components/details_panel.py:647:        structure_id = decision_data.get("structure_id") or "N/A"
UI/components/details_panel.py:650:        self.decision_label.config(text=decision_data.get("decision", "N/A"))
UI/components/details_panel.py:651:        self.level_label.config(text=str(decision_data.get("level", "N/A")))
UI/components/details_panel.py:653:        self._format_currency_label(self.pl_atual_label, decision_data.get("pl_atual"))
UI/components/details_panel.py:654:        self._format_currency_label(self.pl_max_label, decision_data.get("pl_max"))
UI/components/details_panel.py:656:        ratio = decision_data.get("pl_pct_of_max")
UI/components/details_panel.py:661:        self.dte_label.config(text=str(decision_data.get("dte_min", "N/A")))
UI/components/details_panel.py:663:        spot_ref = decision_data.get("spot_reference") or decision_data.get("spot_ref")
UI/components/details_panel.py:672:        why_payload = decision_data.get("why") or decision_data.get("why_json")
UI/components/details_panel.py:720:        self._current_decision = None
UI/components/details_panel.py:722:            self.timestamp_label, self.structure_label, self.decision_label,
UI/components/details_panel.py:878:    def _fetch_latest_decision_from_derived(
UI/components/details_panel.py:882:        alteracao_36: filtra por structure_id (INTEGER) em structure_decisions.
UI/components/details_panel.py:892:                "structure_id", "timestamp", "decision", "level",
UI/components/details_panel.py:900:                FROM structure_decisions
UI/components/details_panel.py:920:    def _fetch_payoff_points_from_derived(self, structure_id):
UI/components/details_panel.py:922:        alteracao_36: filtra por structure_id (INTEGER) em payoff_curve_points.
UI/components/details_panel.py:934:                FROM payoff_curve_points
UI/components/details_panel.py:962:                FROM structure_decisions
UI/components/details_panel.py:975:                "SELECT COUNT(*) AS n FROM payoff_curve_points WHERE structure_id = ?",
UI/components/details_panel.py:980:                "source_table": "derived.db:structure_decisions / payoff_curve_points",
UI/components/details_panel.py:1025:        decision = self._fetch_latest_decision_from_derived(structure_id)
UI/components/details_panel.py:1026:        if decision:
UI/components/details_panel.py:1027:            self.update_decision(decision)
UI/components/details_panel.py:1029:        pts = self._fetch_payoff_points_from_derived(structure_id)
UI/components/details_panel.py:1033:        if decision:
UI/components/details_panel.py:1034:            spot_ref = decision.get("spot_reference")
UI/components/details_panel.py:1047:        decision = self._current_decision
UI/components/details_panel.py:1048:        if not decision:
UI/components/details_panel.py:1055:        structure_id = decision.get("structure_id")
UI/components/filters_panel.py:54:        self.decision_var = tk.StringVar()
UI/components/filters_panel.py:55:        self.decision_combo = ttk.Combobox(
UI/components/filters_panel.py:57:            textvariable=self.decision_var,
UI/components/filters_panel.py:62:        self.decision_combo.pack(side="left", padx=(5, 0))
UI/components/filters_panel.py:101:        self.decision_combo.bind("<<ComboboxSelected>>", lambda e: self._apply_filters())
UI/components/filters_panel.py:116:        if self.decision_var.get().strip():
UI/components/filters_panel.py:117:            filters["decision"] = self.decision_var.get().strip()
UI/components/filters_panel.py:139:        self.decision_var.set("")
UI/components/payoff_chart.py:1:# UI/components/payoff_chart.py
UI/components/payoff_chart.py:8:from UI.debug_utils import payoff_debug, payoff_info
UI/components/payoff_chart.py:66:        self._last_decision_data: Dict = {}
UI/components/payoff_chart.py:164:        self._last_decision_data = {}
UI/components/payoff_chart.py:170:        payoff_points: List[Dict],
UI/components/payoff_chart.py:171:        decision_data: Optional[Dict] = None,
UI/components/payoff_chart.py:178:        self._last_points = list(payoff_points) if payoff_points else []
UI/components/payoff_chart.py:179:        self._last_decision_data = dict(decision_data) if decision_data else {}
UI/components/payoff_chart.py:182:            payoff_points, decision_data, overlay_curve=self._fixed_curve
UI/components/payoff_chart.py:187:        payoff_debug("FIX clicked -- id=", id(self))
UI/components/payoff_chart.py:216:        payoff_debug("CLEAR comparison -- id=", id(self))
UI/components/payoff_chart.py:248:        """Redesenha com os dados salvos em _last_points/_last_decision_data."""
UI/components/payoff_chart.py:252:                self._last_decision_data or {},
UI/components/payoff_chart.py:258:        payoff_points: List[Dict],
UI/components/payoff_chart.py:259:        decision_data: Optional[Dict],
UI/components/payoff_chart.py:268:        if not payoff_points:
UI/components/payoff_chart.py:269:            self.ax.set_title("Sem dados de payoff")
UI/components/payoff_chart.py:281:        for p in payoff_points:
UI/components/payoff_chart.py:290:            payoff_info("ERROR: não consegui extrair xs/ys de payoff_points.")
UI/components/payoff_chart.py:291:            self.ax.set_title("Sem dados de payoff")
UI/components/payoff_chart.py:297:        payoff_debug(
UI/components/payoff_chart.py:300:        payoff_debug(
UI/components/payoff_chart.py:307:        if overlay_curve and decision_data:
UI/components/payoff_chart.py:309:                decision_data.get("structure_id")
UI/components/payoff_chart.py:310:                or decision_data.get("aba", "")
UI/components/payoff_chart.py:351:        if decision_data:
UI/components/payoff_chart.py:352:            raw = decision_data.get("spot_ref") or decision_data.get("spot_reference")
UI/components/payoff_chart.py:416:        if decision_data:
UI/components/payoff_chart.py:418:                decision_data.get("structure_id")
UI/components/payoff_chart.py:419:                or decision_data.get("aba", "")
UI/components/payoff_chart.py:421:            dec = decision_data.get("decision", "")
UI/components/payoff_chart.py:453:            p, ["point_pl", "pl", "y", "pnl", "payoff", "profit_loss", "pl_value"]
UI/components/structure_editor_dialog.py:38:from repositories.rtd_option_quotes_repository import RtdOptionQuotesRepository
UI/components/structure_editor_dialog.py:39:from services.structure_leg_rtd_enrichment_service import StructureLegRtdEnrichmentService
UI/components/structure_editor_dialog.py:400:        """Compatibilidade: permite leg manual completa mesmo sem cotacao RTD."""
UI/components/structure_editor_dialog.py:419:            preserva compatibilidade e nao acessa RTD.
UI/components/structure_editor_dialog.py:434:                self._refresh_rtd_quote_for_symbol(symbol)
UI/components/structure_editor_dialog.py:446:    def _refresh_rtd_quote_for_symbol(self, symbol: str) -> None:
UI/components/structure_editor_dialog.py:447:        """Atualiza uma opção avulsa no RTD/Excel e importa para o cache local."""
UI/components/structure_editor_dialog.py:459:        script = project_root / "scripts" / "refresh_rtd_symbol_to_option_quotes_fallback.py"
UI/components/structure_editor_dialog.py:460:        workbook_path = project_root / "LISTA_RTD.xlsm"
UI/components/structure_editor_dialog.py:474:            raise ValueError(f"Script de refresh RTD não encontrado: {script}")
UI/components/structure_editor_dialog.py:477:            raise ValueError(f"Workbook RTD não encontrado: {workbook_path}")
UI/components/structure_editor_dialog.py:515:                "Não foi possível atualizar a cotação RTD para "
UI/debug_utils.py:24:def payoff_debug(*args, **kwargs):
UI/debug_utils.py:25:    """Log de payoff chart apenas se debug ativo"""
UI/debug_utils.py:29:def payoff_info(*args, **kwargs):
UI/debug_utils.py:30:    """Log de payoff sempre"""
UI/main_window.py:5:Carrega dados de derived.db e app.db para exibir decisões e payoffs
UI/main_window.py:8:from UI.components.payoff_chart import PayoffChart
UI/main_window.py:10:from UI.components.decisions_grid import DecisionsGrid
UI/main_window.py:40:        self._payoff_worker_id = 0
UI/main_window.py:46:        self._loading_payoff = False
UI/main_window.py:50:        self.last_selected_decision: Optional[Dict] = None
UI/main_window.py:55:        # Controle de atualização automática da UI/RTD.
UI/main_window.py:57:        # Não executa pipeline e não recalcula payoff.
UI/main_window.py:95:        self.decisions_grid = DecisionsGrid(
UI/main_window.py:97:            on_selection_change=self.on_decision_selected,
UI/main_window.py:99:        self.decisions_grid.pack(fill="both", expand=True, padx=5, pady=5)
UI/main_window.py:120:        self.payoff_chart = PayoffChart(chart_frame)
UI/main_window.py:121:        self.payoff_chart.pack(fill="both", expand=True, padx=5, pady=5)
UI/main_window.py:176:            filtered_data = self.data_model.get_decisions(filters)
UI/main_window.py:177:            self.decisions_grid.update_data(filtered_data)
UI/main_window.py:184:    def on_decision_selected(self, decision_data: Dict):
UI/main_window.py:186:        alteracao_36: structure_id é suficiente para carregar payoff -- timestamp não é obrigatório.
UI/main_window.py:188:        if not decision_data:
UI/main_window.py:191:        self.last_selected_decision = dict(decision_data)
UI/main_window.py:195:            self.details_panel.update_decision(decision_data)
UI/main_window.py:199:        # Carregar payoff em background -- apenas structure_id necessário
UI/main_window.py:200:        structure_id = decision_data.get("structure_id")
UI/main_window.py:201:        timestamp = decision_data.get("timestamp")  # opcional
UI/main_window.py:204:            self._start_payoff_load(structure_id, timestamp, decision_data)
UI/main_window.py:206:            self.payoff_chart.clear()
UI/main_window.py:207:            self.status_bar.config(text="Dados insuficientes para payoff")
UI/main_window.py:209:    def _start_payoff_load(
UI/main_window.py:213:        decision_data=None,   # alteracao_36: opcional
UI/main_window.py:215:        """Inicia carregamento de payoff em thread separada.
UI/main_window.py:218:        if decision_data is None:
UI/main_window.py:219:            decision_data = {"structure_id": structure_id}
UI/main_window.py:221:        self._payoff_worker_id += 1
UI/main_window.py:222:        current_worker_id = self._payoff_worker_id
UI/main_window.py:224:        if self._loading_payoff:
UI/main_window.py:225:            self.status_bar.config(text="Carregando payoff... (cancelando anterior)")
UI/main_window.py:227:            self.status_bar.config(text="Carregando payoff...")
UI/main_window.py:229:        self._loading_payoff = True
UI/main_window.py:233:                points, info_dict = self.data_model.get_payoff_curve_info(
UI/main_window.py:238:                        f"payoff structure_id={structure_id} ts_req={timestamp} "
UI/main_window.py:261:                if current_worker_id != self._payoff_worker_id:
UI/main_window.py:266:                    self._finish_payoff_load,
UI/main_window.py:269:                    decision_data,
UI/main_window.py:273:                if current_worker_id == self._payoff_worker_id:
UI/main_window.py:276:                        self._handle_payoff_error,
UI/main_window.py:304:            decisions = self.data_model.get_decisions()
UI/main_window.py:305:            self.decisions_grid.update_data(decisions)
UI/main_window.py:308:            d = self.last_selected_decision
UI/main_window.py:317:                        self.decisions_grid.select_by_key(target_sid, target_ts)
UI/main_window.py:322:                        self.details_panel.update_decision(d)
UI/main_window.py:327:                        self._start_payoff_load(target_sid, target_ts, d)
UI/main_window.py:338:                    self.payoff_chart.clear()
UI/main_window.py:343:                text=f"Dados atualizados - {len(decisions)} decisões"
UI/main_window.py:439:                current_data = self.decisions_grid.get_current_data()
UI/main_window.py:476:            self.payoff_chart.fix_current_curve()
UI/main_window.py:562:        """Extrai o resumo JSON emitido por scripts/run_derived_pipeline.py."""
UI/main_window.py:597:            f"- Decisões: {self._format_pipeline_value(summary.get('decisions'))}",
UI/main_window.py:598:            f"- Pontos de payoff: {self._format_pipeline_value(summary.get('payoff_points'))}",
UI/main_window.py:599:            f"- Resumos de payoff: {self._format_pipeline_value(summary.get('payoff_summaries'))}",
UI/main_window.py:601:            f"- Cotações RTD atualizadas: {self._format_pipeline_value(summary.get('rtd_quotes_updated'))}",
UI/main_window.py:613:        decisions = self._format_pipeline_value(summary.get("decisions"))
UI/main_window.py:614:        payoff_points = self._format_pipeline_value(summary.get("payoff_points"))
UI/main_window.py:618:            f"Pipeline OK: decisões={decisions}; "
UI/main_window.py:619:            f"pontos_payoff={payoff_points}; erros={errors}"
UI/main_window.py:636:            script_path = project_root / "scripts" / "run_derived_pipeline.py"
UI/main_window.py:638:                script_path = project_root / "Scripts" / "run_derived_pipeline.py"
UI/main_window.py:699:Pipeline automático de payoff e decisões
UI/main_window.py:702:* Excel RTD  CSV Bridge
UI/main_window.py:711:    # Handlers de payoff (thread  main thread)
UI/main_window.py:714:    def _finish_payoff_load(
UI/main_window.py:718:        decision_data: Dict,
UI/main_window.py:722:        if worker_id != self._payoff_worker_id:
UI/main_window.py:725:        self._loading_payoff = False
UI/main_window.py:730:                overlays = self.payoff_chart.update_chart(points, decision_data)
UI/main_window.py:745:                used_ts = (info_dict or {}).get("used_timestamp") or decision_data.get(
UI/main_window.py:748:                src = (info_dict or {}).get("source_table", "payoff_curve_points")
UI/main_window.py:751:                if used_ts and used_ts != decision_data.get("timestamp"):
UI/main_window.py:755:                self.payoff_chart.clear()
UI/main_window.py:756:                self.status_bar.config(text="Sem dados de payoff para esta seleção")
UI/main_window.py:758:            self._handle_payoff_error(str(e), worker_id)
UI/main_window.py:760:    def _handle_payoff_error(self, error_msg: str, worker_id: int):
UI/main_window.py:761:        if worker_id != self._payoff_worker_id:
UI/main_window.py:763:        self._loading_payoff = False
UI/main_window.py:766:            self.payoff_chart.clear()
UI/main_window.py:769:        self.status_bar.config(text=f"Erro ao carregar payoff: {error_msg}")
UI/main_window.py:770:        print(f"[UI] Erro no payoff: {error_msg}")
UI/main_window.py:892:        Recalcula pricing/payoff/decisão após criação ou edição manual.
UI/main_window.py:911:        _post_status(f"Estrutura {sid} salva. Recalculando payoff...")
UI/main_window.py:927:                    _set_status(f"Estrutura {sid} salva e payoff recalculado.")
UI/models/ui_data.py:24:    "decision":      ["decision", "decisao", "action"],
UI/models/ui_data.py:40:    "pl":        ["point_pl", "pl", "pl_value", "y", "payoff", "pl_venc"],
UI/models/ui_data.py:61:        self._payoff_table: Optional[str] = None
UI/models/ui_data.py:63:        self._payoff_cols: Dict[str, str] = {}
UI/models/ui_data.py:66:        self._payoff_cache: Dict[Tuple[str, str], Dict[str, Any]] = {}
UI/models/ui_data.py:67:        self._payoff_cache_max = 128
UI/models/ui_data.py:103:                self._payoff_table = t
UI/models/ui_data.py:124:    def _build_payoff_colmap(self):
UI/models/ui_data.py:125:        if not self._payoff_table:
UI/models/ui_data.py:126:            self._payoff_cols = {}
UI/models/ui_data.py:129:        cols = self._inspect_columns(self._payoff_table)
UI/models/ui_data.py:132:        if self._payoff_table == "payoff_curve_points":
UI/models/ui_data.py:142:            print(f"[UI] Usando contrato canônico para {self._payoff_table}")
UI/models/ui_data.py:145:            print(f"[UI] Usando aliases flexíveis para {self._payoff_table}")
UI/models/ui_data.py:154:        self._payoff_cols = colmap
UI/models/ui_data.py:156:        if ("spot" not in self._payoff_cols) or ("pl" not in self._payoff_cols):
UI/models/ui_data.py:158:                f"Tabela {self._payoff_table} não apresenta colunas obrigatórias "
UI/models/ui_data.py:159:                f"para payoff (point_spot/point_pl ou spot/pl)."
UI/models/ui_data.py:163:        if "structure_id" not in self._payoff_cols:
UI/models/ui_data.py:165:                f"[UI] AVISO: {self._payoff_table} nao tem coluna structure_id. "
UI/models/ui_data.py:205:        self._build_payoff_colmap()
UI/models/ui_data.py:247:    def get_decisions(self, filters: Optional[Dict] = None) -> List[Dict]:
UI/models/ui_data.py:274:            "timestamp", "structure_id", "aba", "decision", "level",
UI/models/ui_data.py:336:            if filters.get("decision"):
UI/models/ui_data.py:337:                where.append("t.decision = ?")
UI/models/ui_data.py:338:                params.append(filters["decision"])
UI/models/ui_data.py:351:                t.timestamp, t.structure_id, t.aba, t.decision, t.level,
UI/models/ui_data.py:401:    def get_payoff_curve(self, structure_id: str, timestamp: str) -> List[Dict]:
UI/models/ui_data.py:410:        if hasattr(self, "_payoff_cache") and cache_key in self._payoff_cache:
UI/models/ui_data.py:411:            cached = self._payoff_cache[cache_key]
UI/models/ui_data.py:417:        if not self._payoff_table:
UI/models/ui_data.py:419:                "Tabela de payoff não encontrada. Esperadas: "
UI/models/ui_data.py:424:        p = self._payoff_cols
UI/models/ui_data.py:429:                f"Tabela {self._payoff_table} não possui colunas esperadas para payoff."
UI/models/ui_data.py:439:            FROM {self._payoff_table}
UI/models/ui_data.py:452:            FROM {self._payoff_table}
UI/models/ui_data.py:466:            FROM {self._payoff_table}
UI/models/ui_data.py:476:    def get_payoff_curve_info(
UI/models/ui_data.py:487:        if not self._payoff_table:
UI/models/ui_data.py:502:        p = self._payoff_cols
UI/models/ui_data.py:516:                "source_table": self._payoff_table,
UI/models/ui_data.py:524:            if self._payoff_table == "payoff_curve_points":
UI/models/ui_data.py:527:                if "meta_json" in self._inspect_columns("payoff_curve_points"):
UI/models/ui_data.py:532:                    f"FROM payoff_curve_points "
UI/models/ui_data.py:541:                        f"SELECT timestamp FROM payoff_curve_points "
UI/models/ui_data.py:562:                        f"Tabela {self._payoff_table} não possui colunas esperadas."
UI/models/ui_data.py:567:                    f"FROM {self._payoff_table} "
UI/models/ui_data.py:576:                        f"SELECT {p['timestamp']} AS ts FROM {self._payoff_table} "
UI/models/ui_data.py:603:                "timestamp", "structure_id", "aba", "decision", "level",
UI/models/ui_data.py:639:        payoff_ok = bool(self._payoff_table)
UI/models/ui_data.py:642:        p = self._payoff_cols
UI/models/ui_data.py:653:            f"Tabela de payoff: {self._payoff_table if payoff_ok else 'NÃO ENCONTRADA'}\n"
UI/models/ui_data.py:659:        self._payoff_cache = {}
UI/models/ui_data.py:667:            return self._payoff_cache.get(key)
UI/models/ui_data.py:673:            self._payoff_cache[key] = value
UI/models/ui_data.py:674:            mx = getattr(self, "_payoff_cache_max", 0) or 0
UI/models/ui_data.py:675:            if mx > 0 and len(self._payoff_cache) > mx:
UI/models/ui_data.py:676:                self._payoff_cache.pop(next(iter(self._payoff_cache)))
scripts/audit_rtd_option_quotes.py:3:Audita a tabela rtd_option_quotes em um banco SQLite.
scripts/audit_rtd_option_quotes.py:7:    python scripts/audit_rtd_option_quotes.py --db dados/app.db
scripts/audit_rtd_option_quotes.py:8:    python scripts/audit_rtd_option_quotes.py --db dados/app.db --json
scripts/audit_rtd_option_quotes.py:23:TABLE_NAME = "rtd_option_quotes"
scripts/audit_rtd_option_quotes.py:218:    print("Auditoria rtd_option_quotes")
scripts/audit_rtd_option_quotes.py:254:        description="Audita a tabela rtd_option_quotes em um banco SQLite."
scripts/build_rtd_symbols.py:81:def collect_from_rtd_option_quotes(cur):
scripts/build_rtd_symbols.py:82:    if not table_exists(cur, "rtd_option_quotes"):
scripts/build_rtd_symbols.py:87:        FROM rtd_option_quotes
scripts/build_rtd_symbols.py:129:            quote_symbols = collect_from_rtd_option_quotes(cur)
scripts/build_rtd_symbols.py:130:            sources.append(("rtd_option_quotes", quote_symbols))
scripts/check_rota_desenvolvimento.py:392:        "run_derived_pipeline.py",
scripts/create_rtd_option_quotes_sheet.py:27:RTD = 'RTD("btg_pro_rtd","","{topic}",$A{row})'
scripts/create_rtd_option_quotes_sheet.py:31:    return "=" + RTD.format(topic=topic, row=row)
scripts/create_rtd_option_quotes_sheet.py:40:        description="Cria/atualiza aba RTD_OPTION_QUOTES tabular em LISTA_RTD.xlsm."
scripts/create_rtd_option_quotes_sheet.py:42:    parser.add_argument("--workbook", default="LISTA_RTD.xlsm")
scripts/create_rtd_option_quotes_sheet.py:48:    parser.add_argument("--sheet", default="RTD_OPTION_QUOTES")
scripts/dev/close_phase_5f_ui_pipeline.sh:34:    - Pontos de payoff: 202
scripts/dev/close_phase_5f_ui_pipeline.sh:35:    - Resumos de payoff: n/d
scripts/dev/close_phase_5f_ui_pipeline.sh:37:    - Cotacoes RTD atualizadas: 4
scripts/dev/close_phase_5f_ui_pipeline.sh:52:    aab7e92 Integra importacao RTD CSV ao pipeline derived
scripts/dev/close_phase_5f_ui_pipeline.sh:53:    a64a464 Restaura e valida cadeia historica RTD de opcoes
scripts/dev/close_phase_5f_ui_pipeline.sh:55:    a1088b3 docs: add phase 3f payoff diagnostic evidence
scripts/dev/close_phase_5f_ui_pipeline.sh:56:    861c17f fix: normalize manual legs for derived payoff persistence
scripts/dev/close_phase_5f_ui_pipeline.sh:81:    Compiling 'ATT/tests\\test_run_derived_pipeline_rtd_integration.py'...
scripts/dev/close_phase_5f_ui_pipeline.sh:90:    [PIPELINE] Importando cotacoes RTD para derived.db...
scripts/dev/close_phase_5f_ui_pipeline.sh:91:    Importacao RTD wide CSV
scripts/dev/close_phase_5f_ui_pipeline.sh:99:    Auditoria rtd_option_quotes
scripts/dev/close_phase_5f_ui_pipeline.sh:101:    Tabela: rtd_option_quotes
scripts/dev/close_phase_5f_ui_pipeline.sh:120:      Pontos de payoff: 202
scripts/dev/close_phase_5f_ui_pipeline.sh:121:      Resumos de payoff: n/d
scripts/dev/close_phase_5f_ui_pipeline.sh:123:      Cotacoes RTD atualizadas: 4
scripts/dev/close_phase_5f_ui_pipeline.sh:130:      "decisions": 2,
scripts/dev/close_phase_5f_ui_pipeline.sh:132:      "payoff_points": 202,
scripts/dev/close_phase_5f_ui_pipeline.sh:133:      "payoff_summaries": null,
scripts/dev/close_phase_5f_ui_pipeline.sh:135:      "rtd_import": {
scripts/dev/close_phase_5f_ui_pipeline.sh:144:      "rtd_quotes_updated": 4,
scripts/dev/close_phase_5f_ui_pipeline.sh:147:        "payoff_curve_points": 202,
scripts/dev/close_phase_5f_ui_pipeline.sh:148:        "rtd_option_quotes": 4,
scripts/dev/close_phase_5f_ui_pipeline.sh:149:        "structure_decisions": 2
scripts/dev/close_phase_5f_ui_pipeline.sh:162:| Pontos de payoff exibidos no resumo | OK |
scripts/dev/close_phase_5f_ui_pipeline.sh:163:| Cotacoes RTD atualizadas exibidas no resumo | OK |
scripts/dev/close_phase_5f_ui_pipeline.sh:166:| Curva de payoff visivel | OK |
scripts/dev/close_phase_5f_ui_pipeline.sh:169:| Contrato canonico de payoff_curve_points usado | OK |
scripts/dev/close_phase_5f_ui_pipeline.sh:176:Os campos Estruturas, Resumos de payoff e Execucoes de pricing permanecem como n/d.
scripts/dev/close_phase_5f_ui_pipeline.sh:181:- pontos de payoff;
scripts/dev/close_phase_5f_ui_pipeline.sh:182:- cotacoes RTD atualizadas;
scripts/dev/close_phase_6_integrated_validation.sh:17:- ingestao RTD;
scripts/dev/close_phase_6_integrated_validation.sh:21:- persistencia de payoff;
scripts/dev/close_phase_6_integrated_validation.sh:39:| Fase 3F | Validada | Diagnostico de payoff |
scripts/dev/close_phase_6_integrated_validation.sh:97:    - Pontos de payoff: 202
scripts/dev/close_phase_6_integrated_validation.sh:98:    - Resumos de payoff: n/d
scripts/dev/close_phase_6_integrated_validation.sh:100:    - Cotacoes RTD atualizadas: 4
scripts/dev/close_phase_6_integrated_validation.sh:117:| Pontos de payoff persistidos | OK |
scripts/dev/close_phase_6_integrated_validation.sh:118:| Curva de payoff visivel | OK |
scripts/dev/close_phase_6_integrated_validation.sh:119:| Cotacoes RTD atualizadas exibidas no resumo | OK |
scripts/dev/close_phase_6_integrated_validation.sh:134:| Pontos de payoff | 202 |
scripts/dev/close_phase_6_integrated_validation.sh:135:| Resumos de payoff | n/d |
scripts/dev/close_phase_6_integrated_validation.sh:137:| Cotacoes RTD atualizadas | 4 |
scripts/dev/close_phase_6_integrated_validation.sh:143:Os campos Estruturas, Resumos de payoff e Execucoes de pricing permanecem como n/d.
scripts/dev/close_phase_6_integrated_validation.sh:149:- pontos de payoff persistidos;
scripts/dev/close_phase_6_integrated_validation.sh:150:- curva de payoff visivel;
scripts/dev/close_phase_6_integrated_validation.sh:151:- cotacoes RTD atualizadas;
scripts/dev/close_phase_6_integrated_validation.sh:163:O sistema confirma execucao operacional pela UI, persistencia em dados/derived.db, resumo operacional ao usuario, decisoes calculadas, curva de payoff disponivel e suite automatizada sem regressao.
scripts/dev/open_phase_6_integrated_validation.sh:19:- ingestao RTD;
scripts/dev/open_phase_6_integrated_validation.sh:23:- persistencia de payoff;
scripts/dev/open_phase_6_integrated_validation.sh:34:- Importacao de cotacoes RTD
scripts/dev/open_phase_6_integrated_validation.sh:35:- Auditoria da tabela rtd_option_quotes
scripts/dev/open_phase_6_integrated_validation.sh:39:- Curvas de payoff
scripts/dev/open_phase_6_integrated_validation.sh:49:| Fase 3F | Validada | Diagnostico de payoff |
scripts/dev/open_phase_6_integrated_validation.sh:64:    - Pontos de payoff: 202
scripts/dev/open_phase_6_integrated_validation.sh:65:    - Resumos de payoff: n/d
scripts/dev/open_phase_6_integrated_validation.sh:67:    - Cotacoes RTD atualizadas: 4
scripts/dev/open_phase_6_integrated_validation.sh:93:- Nenhuma regressao em payoff
scripts/dev/open_phase_6_integrated_validation.sh:94:- Nenhuma regressao em RTD
scripts/dev/open_phase_6_integrated_validation.sh:103:- Importacao RTD retorna sem erros
scripts/dev/open_phase_6_integrated_validation.sh:104:- Auditoria de RTD retorna status ok
scripts/dev/open_phase_6_integrated_validation.sh:107:- Resumo operacional apresenta pontos de payoff
scripts/dev/open_phase_6_integrated_validation.sh:108:- Resumo operacional apresenta cotacoes RTD atualizadas
scripts/dev/open_phase_6_integrated_validation.sh:121:- Curva de payoff permanece visivel
scripts/dev/open_phase_6_integrated_validation.sh:130:- payoff_curve_points possui pontos persistidos
scripts/dev/open_phase_6_integrated_validation.sh:131:- structure_decisions possui decisoes persistidas
scripts/dev/open_phase_6_integrated_validation.sh:132:- rtd_option_quotes possui cotacoes atualizadas
scripts/dev/open_phase_6_integrated_validation.sh:166:- as decisoes e a curva de payoff permanecerem visiveis;
scripts/dev/register_phase_7_delivery_package_matrix.sh:118:  echo "- Validar se LISTA_RTD.xlsm ainda e necessario ao fluxo real, pois ha muitas referencias textuais e ausencia no repositorio."
scripts/dev/register_phase_7_delivery_package_matrix.sh:120:  echo "- Confirmar se LISTA_RTD.xlsx e OPERACOES_E_OPCOES.xlsm devem permanecer no repositorio ou migrar para fixture controlada."
scripts/dev/register_phase_7_delivery_readiness_checklist.sh:92:  echo "- Decidir se LISTA_RTD.xlsx permanece no repositorio, entra no pacote interno ou deve ser substituido por fixture."
scripts/dev/register_phase_7_delivery_readiness_checklist.sh:94:  echo "- Decidir se LISTA_RTD.xlsm e pre-requisito externo, dependencia historica ou referencia obsoleta."
scripts/dev/register_phase_7_excel_packaging_guideline.sh:34:  echo "- Arquivo: LISTA_RTD.xlsx"
scripts/dev/register_phase_7_excel_packaging_guideline.sh:40:  echo "- Arquivo: LISTA_RTD.xlsm"
scripts/dev/register_phase_7_root_data_dependencies_review.sh:19:    git grep -n -I -E 'LISTA_RTD|OPERACOES_E_OPCOES|xlsx|xlsm|xls' -- . \
scripts/dev/register_phase_7_root_data_dependencies_review.sh:43:  echo "- LISTA_RTD.xlsx"
scripts/dev/register_phase_7_workbook_reference_gap_review.sh:18:  "LISTA_RTD.xlsx"
scripts/dev/register_phase_7_workbook_reference_gap_review.sh:19:  "LISTA_RTD.xlsm"
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:5:OUT="$EVID_DIR/fase-3a-diagnostico-cadastro-payoff-decisoes.txt"
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:10:    echo "== Fase 3A - Diagnostico cadastro manual, payoff e decisoes =="
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:32:        | grep -Ei 'structure|estrutura|payoff|decision|decis|pipeline|rtd|repository|service|dialog|editor|manual|leg' \
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:39:    grep -RInE "structure_decisions|payoff_curve_points|manual|Manual|payoff|decision|decis|canonical|structure_id|Salvar|Aplicar Leg|must be numeric" . \
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:72:    if any(term in low for term in ["structure", "estrutura", "leg", "payoff", "decision", "decis", "rtd", "quote"]):
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:81:    "payoff_curve_points",
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:82:    "structure_decisions",
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:83:    "rtd_option_quotes",
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:92:print("Schema resumido de estruturas, legs, payoff e decisoes:")
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:96:    if any(term in low for term in ["structure", "estrutura", "leg", "payoff", "decision", "decis"]):
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:113:terms = ("structure", "estrutura", "payoff", "decision", "decis", "manual", "leg")
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:127:    echo "6) Pytest focado em cadastro, structure, payoff, decision e leg"
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:129:    python -m pytest -q -k "manual or structure or payoff or decision or leg" || true
scripts/fase-3b-diagnostico-schema-canonico-estruturas.sh:55:        "scripts/run_derived_pipeline.py"
scripts/fase-3b-diagnostico-schema-canonico-estruturas.sh:108:    if any(term in name for term in ["structure", "leg", "payoff", "decision", "rtd", "quote"]):
scripts/fase-3c-diagnostico-appdb-ui-pricing-flow.sh:10:    echo "== Fase 3C - Diagnostico app.db, UI e fluxo pricing/payoff =="
scripts/fase-3c-diagnostico-appdb-ui-pricing-flow.sh:66:        "payoff_curve_points",
scripts/fase-3c-diagnostico-appdb-ui-pricing-flow.sh:67:        "structure_decisions",
scripts/fase-3c-diagnostico-appdb-ui-pricing-flow.sh:68:        "rtd_option_quotes",
scripts/fase-3c-diagnostico-appdb-ui-pricing-flow.sh:70:        "rtd_analise_robo_legs",
scripts/fase-3c-diagnostico-appdb-ui-pricing-flow.sh:82:        if any(t in low for t in ["structure", "leg", "pricing", "payoff", "decision", "rtd", "manual"]):
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:28:    echo "3) Ocorrencias CanonicalPricingFacade e persistencia payoff/decision"
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:30:    grep -RInE "class CanonicalPricingFacade|def .*price|def .*pricing|def .*persist|save_payoff|save_decision|structure_decisions|payoff_curve_points|PricingExecution|Derived|derived" \
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:43:        services/derived_payoff_persistence.py \
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:44:        services/payoff_persistence_port.py \
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:119:        "payoff_curve_points",
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:120:        "structure_decisions",
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:187:    (derived_db, ["payoff_curve_points", "structure_decisions"]),
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:294:    (derived_db, ["payoff_curve_points", "structure_decisions"]),
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:305:    (derived_db, "payoff_curve_points"),
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:306:    (derived_db, "structure_decisions"),
scripts/fase-3e-fix-facade-manual-sem-alias.sh:103:             usa MarketSnapshotSelector manual > rtd.
scripts/fase-3e-fix-facade-manual-sem-alias.sh:173:            #  2. Seleciona snapshot (manual > rtd)
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:4:EVID="docs/checkpoints/evidencias/fase-3f-diagnostico-payoff-manual-canonico.txt"
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:26:  echo "== Busca por referencias a payoff_curve_points =="
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:27:  grep -RIn "payoff_curve_points" repositories services domain UI ATT scripts 2>/dev/null || true
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:30:  echo "== Busca por referencias a structure_decisions =="
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:31:  grep -RIn "structure_decisions" repositories services domain UI ATT scripts 2>/dev/null || true
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:34:  echo "== Busca por referencias a Payoff/payoff =="
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:35:  grep -RIn "payoff\|Payoff" repositories services domain UI ATT 2>/dev/null || true
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:110:        "payoff_curve_points",
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:111:        "structure_decisions",
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:112:        "rtd_option_quotes",
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:176:            "payoff",
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:177:            "payoff_curve",
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:178:            "payoff_points",
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:181:            "decisions",
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:182:            "decision_results",
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:201:  echo "== Inspecao pos-execucao de payoff e decisoes =="
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:216:        "payoff_curve_points",
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:217:        "structure_decisions",
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:263:- Excel apenas como ponte RTD.
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:275:## Fase 3F - Diagnostico payoff estrutura manual canonica
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:284:Identificar por que a estrutura manual canonica structure_id=2 ainda nao gera pontos em payoff_curve_points.
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:287:docs/checkpoints/evidencias/fase-3f-diagnostico-payoff-manual-canonico.txt
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:4:EVID="docs/checkpoints/evidencias/fase-3f-fix1-diagnostico-compute-payoff-v2.txt"
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:26:  echo "== Trechos essenciais domain/payoff.py =="
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:27:  grep -n "def validate_canonical_input\|def _compute_leg_payoff_at_expiration\|def compute_payoff_curve_from_canonical_legs\|def compute_payoff_from_canonical_input" domain/payoff.py || true
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:29:  sed -n '1,230p' domain/payoff.py
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:33:  grep -n "def insert_payoff_points\|def save_payoff_curve\|def save_payoff_from_canonical_payload\|def save_decision_from_canonical_payload" services/derived_service.py || true
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:40:  echo "== Execucao isolada corrigida: pricing_payload -> canonical_input -> compute_payoff =="
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:64:    from services.derived_payoff_persistence import DerivedPayoffPersistence
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:65:    from domain.payoff import compute_payoff_from_canonical_input, validate_canonical_input
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:94:    payoff = compute_payoff_from_canonical_input(canonical_input)
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:97:    print("PAYOFF_TYPE:", type(payoff).__name__)
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:98:    if isinstance(payoff, dict):
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:99:        print("PAYOFF_KEYS:", sorted(payoff.keys()))
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:100:        print("PAYOFF_POINTS_LEN:", len(payoff.get("points") or []))
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:102:        print(json.dumps(payoff.get("meta"), ensure_ascii=False, default=str, indent=2))
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:104:        print(json.dumps((payoff.get("points") or [])[:10], ensure_ascii=False, default=str, indent=2))
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:107:            "structure_id": payoff.get("structure_id"),
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:108:            "structure_name": payoff.get("structure_name"),
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:109:            "underlying_asset": payoff.get("underlying_asset"),
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:110:            "spot_ref": payoff.get("spot_ref"),
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:111:            "pl_min": payoff.get("pl_min"),
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:112:            "pl_max": payoff.get("pl_max"),
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:115:        print(repr(payoff))
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:146:    from services.derived_payoff_persistence import DerivedPayoffPersistence
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:152:    before_payoff = conn.execute(
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:153:        "select count(*) from payoff_curve_points where structure_id=?",
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:156:    before_decisions = conn.execute(
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:157:        "select count(*) from structure_decisions where structure_id=?",
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:162:    print("Antes payoff_curve_points structure_id=2:", before_payoff)
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:163:    print("Antes structure_decisions structure_id=2:", before_decisions)
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:185:    after_payoff = conn.execute(
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:186:        "select count(*) from payoff_curve_points where structure_id=?",
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:189:    after_decisions = conn.execute(
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:190:        "select count(*) from structure_decisions where structure_id=?",
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:194:    print("Depois payoff_curve_points structure_id=2:", after_payoff)
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:195:    print("Depois structure_decisions structure_id=2:", after_decisions)
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:203:          from payoff_curve_points
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:217:        select id, timestamp, aba, decision, level, pl_atual, pl_max, spot_ref, structure_id, meta_json, why
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:218:          from structure_decisions
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:243:## Fase 3F Fix1 - Diagnostico compute payoff V2
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:256:docs/checkpoints/evidencias/fase-3f-fix1-diagnostico-compute-payoff-v2.txt
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:259:Diagnostico V2 executado. Proxima etapa: patch corretivo no contrato de payoff, se necessario.
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:263:echo "Diagnostico compute payoff V2 gerado em:"
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:4:EVID="docs/checkpoints/evidencias/fase-3f-fix1-diagnostico-compute-payoff.txt"
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:26:  echo "== Arquivo domain/payoff.py =="
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:27:  sed -n '1,420p' domain/payoff.py
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:34:  echo "== Execucao isolada: pricing_payload -> canonical_input -> compute_payoff =="
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:42:    from services.derived_payoff_persistence import DerivedPayoffPersistence
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:43:    from domain.payoff import compute_payoff_from_canonical_input
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:68:    payoff = compute_payoff_from_canonical_input(canonical_input)
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:71:    print("PAYOFF_TYPE:", type(payoff).__name__)
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:72:    if isinstance(payoff, dict):
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:73:        print("PAYOFF_KEYS:", sorted(payoff.keys()))
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:74:        for key, value in payoff.items():
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:84:        print(repr(payoff))
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:99:    from services.derived_payoff_persistence import DerivedPayoffPersistence
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:107:        "select count(*) from payoff_curve_points where structure_id=?",
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:112:    print("Antes payoff_curve_points structure_id=2:", before)
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:133:        "select count(*) from payoff_curve_points where structure_id=?",
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:136:    decisions = conn.execute(
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:137:        "select count(*) from structure_decisions where structure_id=?",
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:142:    print("Depois payoff_curve_points structure_id=2:", after)
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:143:    print("Depois structure_decisions structure_id=2:", decisions)
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:158:## Fase 3F Fix1 - Diagnostico compute payoff
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:168:compute_payoff_from_canonical_input() e DerivedPayoffPersistence.persist() para identificar
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:169:onde a geração/persistência do payoff falha.
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:172:docs/checkpoints/evidencias/fase-3f-fix1-diagnostico-compute-payoff.txt
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:175:Diagnostico executado. Proxima etapa: patch corretivo no contrato de payoff.
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:179:echo "Diagnostico compute payoff gerado em:"
scripts/fase-3f-fix1-evidencia-final.sh:25:  echo "== Diff services/derived_payoff_persistence.py =="
scripts/fase-3f-fix1-evidencia-final.sh:26:  git diff -- services/derived_payoff_persistence.py
scripts/fase-3f-fix1-evidencia-final.sh:29:  echo "== Validação compute payoff V2 - resumo =="
scripts/fase-3f-fix1-evidencia-final.sh:30:  grep -n "VALIDATION_ERRORS\|PAYOFF_POINTS_LEN\|PAYOFF_META\|Antes payoff\|Depois payoff\|Traceback\|TypeError\|ValueError\|warning\|erro" -A20 -B10 \
scripts/fase-3f-fix1-evidencia-final.sh:31:    docs/checkpoints/evidencias/fase-3f-fix1-diagnostico-compute-payoff-v2.txt || true
scripts/fase-3f-fix1-evidencia-final.sh:39:for table in ["payoff_curve_points", "structure_decisions"]:
scripts/fase-3f-fix1-evidencia-final.sh:49:      from payoff_curve_points
scripts/fase-3f-fix1-evidencia-final.sh:58:print("Amostra payoff:")
scripts/fase-3f-fix1-evidencia-final.sh:83:Normalização das legs em services/derived_payoff_persistence.py para preencher
scripts/fase-3f-fix1-evidencia-final.sh:84:position_side a partir de side antes de chamar domain.compute_payoff_from_canonical_input().
scripts/fase-3f-fix1-evidencia-final.sh:87:O payoff canônico validava structure.legs[n].position_side como obrigatório, enquanto
scripts/fase-3f-fix1-evidencia-final.sh:94:Patch aplicado e validado por diagnóstico de geração/persistência de payoff.
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:4:EVID="docs/checkpoints/evidencias/fase-3f-fix1-inspecao-contrato-payoff.txt"
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:26:  echo "== Schema payoff_curve_points em dados/derived.db =="
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:41:for table in ["payoff_curve_points", "structure_decisions"]:
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:81:  echo "== Busca arquivos de persistencia derivada/payoff =="
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:82:  find repositories services domain UI ATT -type f 2>/dev/null | grep -Ei "payoff|derived|decision|pricing" | sort
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:85:  echo "== Referencias diretas a payoff_curve_points =="
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:86:  grep -RIn "payoff_curve_points" repositories services domain UI ATT 2>/dev/null || true
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:97:  echo "== Testes atuais relacionados a pricing/payoff/canonical =="
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:98:  find ATT/tests -type f 2>/dev/null | grep -Ei "pricing|payoff|canonical|decision" | sort
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:109:## Fase 3F Fix1 - Inspecao contrato payoff
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:118:Inspecionar schema de payoff_curve_points, codigo da CanonicalPricingFacade e referencias existentes antes de implementar geracao de payoff canonico.
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:121:docs/checkpoints/evidencias/fase-3f-fix1-inspecao-contrato-payoff.txt
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:124:Inspecao executada. Proxima etapa: implementar geracao e persistencia de pontos de payoff para estrutura manual canonica.
scripts/fase-3f-fix1-patch-normaliza-position-side.py:3:path = Path("services/derived_payoff_persistence.py")
scripts/fase-3f-fix1-patch-normaliza-position-side.py:13:        Normaliza aliases de direção para o contrato canônico de payoff.
scripts/fase-3f-fix1-patch-normaliza-position-side.py:15:        domain/payoff.py exige leg["position_side"].
scripts/fase-3f-fix1-patch-normaliza-position-side.py:48:    def _normalize_leg_for_payoff(leg: Any) -> dict[str, Any]:
scripts/fase-3f-fix1-patch-normaliza-position-side.py:51:        esperado por domain.compute_payoff_from_canonical_input().
scripts/fase-3f-fix1-patch-normaliza-position-side.py:101:    def _normalize_canonical_input_for_payoff(
scripts/fase-3f-fix1-patch-normaliza-position-side.py:105:        Retorna uma cópia rasa do canonical_input com legs normalizadas para payoff.
scripts/fase-3f-fix1-patch-normaliza-position-side.py:115:            DerivedPayoffPersistence._normalize_leg_for_payoff(leg)
scripts/fase-3f-fix1-patch-normaliza-position-side.py:119:        meta.setdefault("payoff_leg_normalization", "fase_3f_fix1_position_side_from_side")
scripts/fase-3f-fix1-patch-normaliza-position-side.py:144:        # estrito de domain/payoff.py.
scripts/fase-3f-fix1-patch-normaliza-position-side.py:146:            return DerivedPayoffPersistence._normalize_canonical_input_for_payoff(
scripts/fase-3f-fix1-patch-normaliza-position-side.py:181:        meta.setdefault("payoff_leg_normalization", "fase_3f_fix1_position_side_from_side")
scripts/fase-3f-fix1-patch-normaliza-position-side.py:189:                    DerivedPayoffPersistence._normalize_leg_for_payoff(leg)
scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:28:  echo "== scripts/run_derived_pipeline.py pontos principais =="
scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:29:  grep -n "def main\|print\|run\|pipeline\|payoff\|decision\|summary\|count\|return" scripts/run_derived_pipeline.py || true
scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:33:  grep -n "def run_full_pipeline\|def run_full_pipeline_from_db\|payoff\|decision\|return" services/calculation_orchestrator.py || true
scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:48:  echo "== Trecho scripts/run_derived_pipeline.py 1-180 =="
scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:49:  sed -n '1,180p' scripts/run_derived_pipeline.py
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:30:grep -Ei '(canonical_pricing_facade|derived_payoff_persistence|derived_service|ui_data|main_window|pricing_execution|structure_analysis|payoff|decision|decisao|decisão)' "$TMP_CODE" \
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:34:  echo "== Fase 4 - Diagnostico minimo payoff/decisao =="
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:81:        | grep -Ei '^(\+\+\+|---|@@|[+-].*(payoff|decision|decisao|decisão|canonical|structure_id|manual|derived|execution|pricing|payload|result|alias_legacy_aba|payoff_curve_points|structure_decisions))' \
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:126:    pay_cols = cols("der", "payoff_curve_points")
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:127:    dec_cols = cols("der", "structure_decisions")
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:133:        ("der", "payoff_curve_points"),
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:134:        ("der", "structure_decisions"),
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:213:            payoff_total = None
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:214:            payoff_last = None
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:216:            if table_exists("der", "payoff_curve_points") and "structure_id" in pay_cols:
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:217:                payoff_total = con.execute(
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:218:                    "select count(*) as n from der.payoff_curve_points where cast(structure_id as text)=?",
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:224:                    payoff_last = con.execute(
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:227:                        from der.payoff_curve_points
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:233:            decision_total = None
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:234:            decision_last = None
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:236:            if table_exists("der", "structure_decisions") and "structure_id" in dec_cols:
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:237:                decision_total = con.execute(
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:238:                    "select count(*) as n from der.structure_decisions where cast(structure_id as text)=?",
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:244:                    decision_last = con.execute(
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:247:                        from der.structure_decisions
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:262:                f"payoff_points={payoff_total}",
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:263:                f"payoff_last={payoff_last}",
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:264:                f"decisions={decision_total}",
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:265:                f"decision_last={decision_last}",
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:272:        table_exists("der", "payoff_curve_points")
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:280:            from der.payoff_curve_points p
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:297:        table_exists("der", "structure_decisions")
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:305:            from der.structure_decisions d
scripts/fase-5-diagnostico-rtd.sh:4:OUT="docs/checkpoints/evidencias/fase-5-diagnostico-rtd.txt"
scripts/fase-5-diagnostico-rtd.sh:8:  echo "FASE 5 - DIAGNOSTICO RTD"
scripts/fase-5-diagnostico-rtd.sh:22:  echo "== Busca por RTD no projeto =="
scripts/fase-5-diagnostico-rtd.sh:24:    -E "RTD|rtd|rtd_option_quotes|option_quotes|quotes" . 2>/dev/null | head -300
scripts/fase-5-diagnostico-rtd.sh:34:    -E "connect_raw|connect_derived|sqlite|derived.db|raw.db|rtd_option_quotes" db repositories services scripts UI 2>/dev/null | head -300
scripts/fase-5-diagnostico-rtd.sh:37:  echo "== Arquivos candidatos RTD =="
scripts/fase-5-diagnostico-rtd.sh:39:    \( -iname '*rtd*' -o -iname '*quote*' -o -iname '*market*' \) \
scripts/fase-5-diagnostico-rtd.sh:62:        for target in ["rtd_option_quotes", "payoff_curve_points", "structure_decisions"]:
scripts/fase-5-diagnostico-rtd.sh:136:  echo "== Trecho scripts/run_derived_pipeline.py =="
scripts/fase-5-diagnostico-rtd.sh:137:  sed -n '1,240p' scripts/run_derived_pipeline.py 2>/dev/null
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:4:OUT="docs/checkpoints/evidencias/fase-5b-diagnostico-rtd-cadeia-real.txt"
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:8:  echo "FASE 5B - DIAGNOSTICO RTD CADEIA REAL E HISTORICO"
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:22:  echo "== Arquivos rastreados relacionados a RTD/quotes =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:23:  git ls-files | grep -Ei "rtd|quote|market|snapshot" | sort
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:26:  echo "== Arquivos atuais em scripts relacionados a RTD/quotes =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:28:    \( -iname '*rtd*' -o -iname '*quote*' -o -iname '*market*' -o -iname '*snapshot*' \) \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:33:  echo "== Arquivos atuais em infra relacionados a RTD/quotes =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:35:    \( -iname '*rtd*' -o -iname '*quote*' -o -iname '*market*' -o -iname '*snapshot*' \) \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:40:  echo "== Arquivos atuais em repositories/services relacionados a RTD/quotes =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:42:    \( -iname '*rtd*' -o -iname '*quote*' -o -iname '*market*' -o -iname '*snapshot*' \) \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:47:  echo "== Historico Git de scripts RTD conhecidos =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:49:    scripts/run_rtd_option_quotes_pipeline.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:50:    scripts/import_rtd_links_to_option_quotes.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:51:    scripts/import_rtd_option_quotes_wide_csv.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:52:    scripts/build_rtd_symbols.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:53:    scripts/run_rtd_refresh_full.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:54:    scripts/audit_rtd_option_quotes.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:55:    scripts/refresh_rtd_option_quotes_excel.ps1 \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:56:    infra/bootstrap_rtd_option_quotes_schema.py
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:64:  echo "== Alteracoes historicas por nome contendo RTD em scripts/infra =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:65:  git log --all --name-status -- scripts infra | grep -Ei "commit |rtd|quote|market" | head -500
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:68:  echo "== Conteudo atual dos scripts RTD existentes =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:70:    scripts/run_rtd_option_quotes_pipeline.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:71:    scripts/import_rtd_links_to_option_quotes.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:72:    scripts/import_rtd_option_quotes_wide_csv.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:73:    scripts/build_rtd_symbols.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:74:    scripts/run_rtd_refresh_full.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:75:    scripts/audit_rtd_option_quotes.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:76:    infra/bootstrap_rtd_option_quotes_schema.py
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:90:  echo "== Testes vigentes relacionados ao pipeline/import/audit RTD =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:92:    ATT/tests/test_run_rtd_option_quotes_pipeline.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:93:    ATT/tests/test_import_rtd_links_to_option_quotes.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:94:    ATT/tests/test_audit_rtd_option_quotes.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:95:    ATT/tests/test_rtd_option_quotes_repository_contract.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:96:    ATT/tests/test_structure_leg_rtd_enrichment_service.py
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:110:  echo "== Schema e contagem rtd_option_quotes em app.db e derived.db =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:127:            "SELECT name FROM sqlite_master WHERE type='table' AND name='rtd_option_quotes'"
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:129:        print(f"rtd_option_quotes existe: {bool(exists)}")
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:133:        count = con.execute("SELECT COUNT(*) AS c FROM rtd_option_quotes").fetchone()["c"]
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:137:        for col in con.execute("PRAGMA table_info(rtd_option_quotes)").fetchall():
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:144:            FROM rtd_option_quotes
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:158:  echo "== Arquivos de dados RTD atuais =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:159:  ls -la dados | grep -Ei "rtd|quote|lista" || true
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:162:  echo "== Primeiras linhas dados/RTD_LINKS.csv se existir =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:163:  if [ -f dados/RTD_LINKS.csv ]; then
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:166:p = Path("dados/RTD_LINKS.csv")
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:174:    echo "dados/RTD_LINKS.csv ausente"
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:178:  echo "== Busca por PowerShell/Excel/COM/RTD nos arquivos atuais =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:180:    -E "Excel.Application|Workbooks|RefreshAll|RTD|LISTA_RTD|RTD_LINKS|win32com|powershell|Start-Process" \
scripts/fase-5c-restaurar-rtd-historico.sh:4:OUT="docs/checkpoints/evidencias/fase-5c-restauracao-rtd-historico.txt"
scripts/fase-5c-restaurar-rtd-historico.sh:8:  "infra/bootstrap_rtd_option_quotes_schema.py"
scripts/fase-5c-restaurar-rtd-historico.sh:9:  "scripts/audit_rtd_option_quotes.py"
scripts/fase-5c-restaurar-rtd-historico.sh:10:  "scripts/build_rtd_symbols.py"
scripts/fase-5c-restaurar-rtd-historico.sh:11:  "scripts/create_rtd_option_quotes_sheet.py"
scripts/fase-5c-restaurar-rtd-historico.sh:12:  "scripts/import_lista_rtd_excel_to_option_quotes.py"
scripts/fase-5c-restaurar-rtd-historico.sh:13:  "scripts/import_rtd_links_to_option_quotes.py"
scripts/fase-5c-restaurar-rtd-historico.sh:14:  "scripts/import_rtd_option_quotes_wide_csv.py"
scripts/fase-5c-restaurar-rtd-historico.sh:15:  "scripts/mapear_automacao_opcoes_rtd.py"
scripts/fase-5c-restaurar-rtd-historico.sh:16:  "scripts/refresh_rtd_option_quotes_excel.ps1"
scripts/fase-5c-restaurar-rtd-historico.sh:17:  "scripts/run_lista_rtd_option_quotes_pipeline.py"
scripts/fase-5c-restaurar-rtd-historico.sh:18:  "scripts/run_rtd_option_quotes_pipeline.py"
scripts/fase-5c-restaurar-rtd-historico.sh:19:  "scripts/run_rtd_refresh_full.py"
scripts/fase-5c-restaurar-rtd-historico.sh:20:  "scripts/seed_current_rtd_option_quotes.py"
scripts/fase-5c-restaurar-rtd-historico.sh:21:  "ATT/tests/test_audit_rtd_option_quotes.py"
scripts/fase-5c-restaurar-rtd-historico.sh:22:  "ATT/tests/test_import_rtd_links_to_option_quotes.py"
scripts/fase-5c-restaurar-rtd-historico.sh:23:  "ATT/tests/test_run_rtd_option_quotes_pipeline.py"
scripts/fase-5c-restaurar-rtd-historico.sh:24:  "ATT/tests/test_rtd_option_quotes_repository_contract.py"
scripts/fase-5c-restaurar-rtd-historico.sh:29:  echo "FASE 5C - RESTAURACAO RTD HISTORICO"
scripts/fase-5c-restaurar-rtd-historico.sh:60:  echo "== Arquivos RTD restaurados =="
scripts/fase-5c-restaurar-rtd-historico.sh:70:    infra/bootstrap_rtd_option_quotes_schema.py \
scripts/fase-5c-restaurar-rtd-historico.sh:71:    scripts/audit_rtd_option_quotes.py \
scripts/fase-5c-restaurar-rtd-historico.sh:72:    scripts/build_rtd_symbols.py \
scripts/fase-5c-restaurar-rtd-historico.sh:73:    scripts/import_rtd_option_quotes_wide_csv.py \
scripts/fase-5c-restaurar-rtd-historico.sh:74:    scripts/run_rtd_option_quotes_pipeline.py \
scripts/fase-5c-restaurar-rtd-historico.sh:75:    scripts/run_rtd_refresh_full.py
scripts/fase-5c-restaurar-rtd-historico.sh:86:  echo "== PowerShell RTD restaurado se existir =="
scripts/fase-5c-restaurar-rtd-historico.sh:87:  if [ -f scripts/refresh_rtd_option_quotes_excel.ps1 ]; then
scripts/fase-5c-restaurar-rtd-historico.sh:88:    sed -n '1,220p' scripts/refresh_rtd_option_quotes_excel.ps1
scripts/fase-5c-restaurar-rtd-historico.sh:94:  echo "== Py compile dos arquivos Python RTD restaurados =="
scripts/fase-5c-restaurar-rtd-historico.sh:110:    echo "Nenhum arquivo Python RTD restaurado para compilar"
scripts/fase-5c-restaurar-rtd-historico.sh:114:  echo "== Testes RTD restaurados disponíveis =="
scripts/fase-5c-restaurar-rtd-historico.sh:116:    ATT/tests/test_audit_rtd_option_quotes.py \
scripts/fase-5c-restaurar-rtd-historico.sh:117:    ATT/tests/test_import_rtd_links_to_option_quotes.py \
scripts/fase-5c-restaurar-rtd-historico.sh:118:    ATT/tests/test_run_rtd_option_quotes_pipeline.py \
scripts/fase-5c-restaurar-rtd-historico.sh:119:    ATT/tests/test_rtd_option_quotes_repository_contract.py
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:4:OUT="docs/checkpoints/evidencias/fase-5d-validacao-rtd-restaurado-operacional.txt"
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:8:  echo "FASE 5D - VALIDACAO OPERACIONAL RTD RESTAURADO"
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:23:  if [ -f dados/RTD_LINKS.csv ]; then
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:24:    ls -l dados/RTD_LINKS.csv
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:27:    sed -n '1,10p' dados/RTD_LINKS.csv
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:29:    echo "ERRO: dados/RTD_LINKS.csv ausente"
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:34:  if [ -f dados/rtd_symbols.txt ]; then
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:35:    ls -l dados/rtd_symbols.txt
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:37:    cat dados/rtd_symbols.txt
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:39:    echo "dados/rtd_symbols.txt ausente"
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:44:  python scripts/audit_rtd_option_quotes.py --db dados/app.db --max-age-minutes 0
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:48:  python scripts/audit_rtd_option_quotes.py --db dados/derived.db --max-age-minutes 0
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:52:  python scripts/import_rtd_option_quotes_wide_csv.py \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:53:    --csv dados/RTD_LINKS.csv \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:59:  python scripts/import_rtd_option_quotes_wide_csv.py \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:60:    --csv dados/RTD_LINKS.csv \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:65:  echo "== Pipeline RTD restaurado - app.db =="
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:66:  python scripts/run_rtd_option_quotes_pipeline.py \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:67:    --csv dados/RTD_LINKS.csv \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:72:  echo "== Pipeline RTD restaurado - derived.db =="
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:73:  python scripts/run_rtd_option_quotes_pipeline.py \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:74:    --csv dados/RTD_LINKS.csv \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:80:  python scripts/audit_rtd_option_quotes.py --db dados/app.db --max-age-minutes 0
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:84:  python scripts/audit_rtd_option_quotes.py --db dados/derived.db --max-age-minutes 0
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:108:              AND name='rtd_option_quotes'
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:111:        print("rtd_option_quotes existe:", bool(exists))
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:122:            FROM rtd_option_quotes
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:140:            FROM rtd_option_quotes
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:152:  echo "== Testes RTD restaurados novamente =="
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:154:    ATT/tests/test_audit_rtd_option_quotes.py \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:155:    ATT/tests/test_import_rtd_links_to_option_quotes.py \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:156:    ATT/tests/test_run_rtd_option_quotes_pipeline.py \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:157:    ATT/tests/test_rtd_option_quotes_repository_contract.py
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:4:OUT="docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt"
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:8:  echo "FASE 5E - DIAGNOSTICO INTEGRACAO RTD NO DERIVED PIPELINE"
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:22:  echo "== scripts/run_derived_pipeline.py =="
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:23:  if [ -f scripts/run_derived_pipeline.py ]; then
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:24:    sed -n '1,260p' scripts/run_derived_pipeline.py
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:26:    echo "ERRO: scripts/run_derived_pipeline.py nao encontrado"
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:30:  echo "== Ocorrencias de rtd_quotes_updated =="
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:31:  grep -R "rtd_quotes_updated" -n . \
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:40:  echo "== Ocorrencias de run_derived_pipeline =="
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:41:  grep -R "run_derived_pipeline" -n . \
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:50:  echo "== Ocorrencias de RTD na UI/controladores =="
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:51:  grep -R "RTD\\|rtd\\|Atualizar Dados\\|Executar Pipeline" -n \
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:62:  find ATT/tests -type f | grep -Ei "derived|pipeline|orchestrator|refresh|rtd" | sort
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:7:path = Path("scripts/run_derived_pipeline.py")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:32:_RTD_METRIC_RE = re.compile(r"^\s*(input_rows|inserted|updated|skipped):\s*(-?\d+)\s*$")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:47:def _parse_rtd_pipeline_metrics(output: str) -> dict:
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:48:    """Extrai métricas textuais emitidas pelo pipeline RTD restaurado."""
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:57:        match = _RTD_METRIC_RE.match(line)
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:67:def _rtd_quotes_updated_count(rtd_result: dict | None) -> int:
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:69:    if not rtd_result:
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:72:    return int(rtd_result.get("inserted") or 0) + int(rtd_result.get("updated") or 0)
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:75:def _run_rtd_option_quotes_import(
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:77:    csv_path: str = "dados/RTD_LINKS.csv",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:81:    Executa a cadeia operacional RTD já restaurada contra o derived.db.
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:84:    - Usa somente CSV local dados/RTD_LINKS.csv.
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:85:    - Não aciona Excel, PowerShell, COM ou refresh RTD ao vivo.
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:86:    - Delega importação + auditoria para scripts/run_rtd_option_quotes_pipeline.py.
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:89:    pipeline_script = repo_root / "scripts" / "run_rtd_option_quotes_pipeline.py"
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:98:            "message": f"Script RTD não encontrado: {pipeline_script}",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:110:            "message": f"CSV RTD não encontrado: {resolved_csv}",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:142:    metrics = _parse_rtd_pipeline_metrics(stdout)
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:157:    Placeholder: Gera payoff_curve_summary a partir de payoff_curve_points.
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:192:def _collect_pipeline_summary(rtd_result: dict | None = None) -> dict:
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:197:    - Inclui a quantidade de cotações RTD inseridas/atualizadas.
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:199:    - Apenas lê contagens do banco depois que o pipeline RTD CSV já rodou.
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:219:            "decisions": _first_count(
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:221:                "decision_snapshots",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:222:                "decisions",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:223:                "structure_decisions",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:224:                "derived_decisions",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:226:            "payoff_points": _first_count(
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:228:                "payoff_curve_points",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:229:                "payoff_points",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:230:                "derived_payoff_points",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:232:            "payoff_summaries": _first_count(
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:234:                "payoff_curve_summary",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:235:                "payoff_summaries",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:236:                "derived_payoff_summary",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:243:            "rtd_quotes_updated": _rtd_quotes_updated_count(rtd_result),
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:244:            "rtd_import": rtd_result,
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:245:            "warnings": int((rtd_result or {}).get("warnings") or 0),
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:246:            "errors": int((rtd_result or {}).get("errors") or 0),
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:266:        "--skip-rtd",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:268:        help="Não importar dados/RTD_LINKS.csv para rtd_option_quotes no derived.db",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:271:        "--rtd-csv",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:272:        default="dados/RTD_LINKS.csv",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:273:        help="Caminho do CSV RTD usado pelo pipeline derivado",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:288:    rtd_result = None
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:289:    if args.skip_rtd:
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:290:        print("\n[PIPELINE] Importação RTD pulada por --skip-rtd.")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:291:        rtd_result = {
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:302:        print("\n[PIPELINE] Importando cotações RTD para derived.db...")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:303:        rtd_result = _run_rtd_option_quotes_import(
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:305:            csv_path=args.rtd_csv,
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:309:        if int(rtd_result.get("returncode") or 0) != 0:
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:310:            print("[ERROR] PIPELINE FALHOU: importação/auditoria RTD falhou")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:311:            if rtd_result.get("message"):
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:312:                print(f"[ERROR] {rtd_result.get('message')}")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:313:            summary = _collect_pipeline_summary(rtd_result)
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:315:            return int(rtd_result.get("returncode") or 1)
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:321:        summary = _collect_pipeline_summary(rtd_result)
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:326:    summary = _collect_pipeline_summary(rtd_result)
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:330:    print(f"  Decisões: {_display_summary_value(summary.get('decisions'))}")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:331:    print(f"  Pontos de payoff: {_display_summary_value(summary.get('payoff_points'))}")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:332:    print(f"  Resumos de payoff: {_display_summary_value(summary.get('payoff_summaries'))}")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:334:    print(f"  Cotações RTD atualizadas: {_display_summary_value(summary.get('rtd_quotes_updated'))}")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:350:cat > ATT/tests/test_run_derived_pipeline_rtd_integration.py <<'PY'
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:357:SCRIPT_PATH = ROOT / "scripts" / "run_derived_pipeline.py"
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:362:        "run_derived_pipeline_under_test",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:371:def test_parse_rtd_pipeline_metrics_from_stdout():
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:375:Importação RTD wide CSV
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:384:    assert module._parse_rtd_pipeline_metrics(output) == {
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:392:def test_rtd_quotes_updated_count_sums_inserted_and_updated():
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:395:    assert module._rtd_quotes_updated_count({"inserted": 2, "updated": 5}) == 7
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:396:    assert module._rtd_quotes_updated_count({"inserted": None, "updated": 5}) == 5
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:397:    assert module._rtd_quotes_updated_count(None) == 0
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:400:def test_run_rtd_option_quotes_import_uses_csv_pipeline_without_excel_or_powershell(
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:411:    (scripts_dir / "run_rtd_option_quotes_pipeline.py").write_text(
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:412:        "# fake rtd csv pipeline\n",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:415:    (dados_dir / "RTD_LINKS.csv").write_text(
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:439:    result = module._run_rtd_option_quotes_import(
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:441:        csv_path="dados/RTD_LINKS.csv",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:454:    assert command[1].endswith("run_rtd_option_quotes_pipeline.py")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:456:    assert "dados/RTD_LINKS.csv" in command
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:462:    assert "refresh_rtd_option_quotes_excel" not in command_text
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:463:    assert "lista_rtd.xlsm" not in command_text
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:4:OUT="docs/checkpoints/evidencias/fase-5e-validacao-integracao-rtd-derived-pipeline.txt"
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:8:  echo "FASE 5E - VALIDACAO INTEGRACAO RTD NO DERIVED PIPELINE"
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:22:  echo "== Diff scripts/run_derived_pipeline.py =="
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:23:  git diff -- scripts/run_derived_pipeline.py
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:27:  sed -n '1,260p' ATT/tests/test_run_derived_pipeline_rtd_integration.py
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:31:  python -m py_compile scripts/run_derived_pipeline.py
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:35:  echo "== Testes focados RTD/pipeline =="
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:37:    ATT/tests/test_run_derived_pipeline_rtd_integration.py \
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:38:    ATT/tests/test_run_rtd_option_quotes_pipeline.py \
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:39:    ATT/tests/test_audit_rtd_option_quotes.py \
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:40:    ATT/tests/test_import_rtd_links_to_option_quotes.py \
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:41:    ATT/tests/test_rtd_option_quotes_repository_contract.py \
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:45:  echo "== Execucao run_derived_pipeline.py --no-cleanup =="
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:46:  python scripts/run_derived_pipeline.py --no-cleanup
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:50:  python scripts/audit_rtd_option_quotes.py --db dados/derived.db --max-age-minutes 0
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:53:  echo "== Estado SQLite rtd_option_quotes derived.db =="
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:66:        "SELECT name FROM sqlite_master WHERE type='table' AND name='rtd_option_quotes'"
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:68:    print("rtd_option_quotes existe:", bool(exists))
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:77:            FROM rtd_option_quotes
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:84:            FROM rtd_option_quotes
scripts/fase-diagnostico-recalc-pipeline-inicializacao.sh:23:    "recalculate_structure\|_on_recalculate_cb\|on_recalculate\|_on_recalculate_click\|run_pipeline\|run_derived_pipeline\|_reprice_structure_after_save\|execute_pricing\|CanonicalPricingFacade" \
scripts/fase5_automacao_gitbash.sh:69:- quais pontos de payoff foram gerados;
scripts/fase5_automacao_gitbash.sh:70:- quais cotações RTD foram atualizadas;
scripts/fase5_automacao_gitbash.sh:83:Ela é iniciada após o encerramento da Fase 4, que validou a integração das estruturas manuais com payoff e decisões.
scripts/fase5_automacao_gitbash.sh:94:- nenhuma cotação RTD foi atualizada;
scripts/fase5_automacao_gitbash.sh:95:- nenhum ponto de payoff foi gerado;
scripts/fase5_automacao_gitbash.sh:138:| Pontos de payoff gerados | Quantidade de registros gerados em payoff_curve_points |
scripts/fase5_automacao_gitbash.sh:139:| Decisões geradas | Quantidade de registros gerados em structure_decisions |
scripts/fase5_automacao_gitbash.sh:140:| Cotações RTD atualizadas | Quantidade de cotações atualizadas |
scripts/fase5_automacao_gitbash.sh:151:    scripts/run_derived_pipeline.py
scripts/fase5_automacao_gitbash.sh:152:    scripts/run_rtd_option_quotes_pipeline.py
scripts/fase5_automacao_gitbash.sh:153:    scripts/run_rtd_refresh_full.py
scripts/fase5_automacao_gitbash.sh:154:    scripts/refresh_rtd_option_quotes_excel.ps1
scripts/fase5_automacao_gitbash.sh:155:    repositories/rtd_option_quotes_repository.py
scripts/fase5_automacao_gitbash.sh:157:    ATT/tests/test_run_rtd_option_quotes_pipeline.py
scripts/fase5_automacao_gitbash.sh:158:    ATT/tests/test_run_derived_pipeline_rtd_integration.py
scripts/fase5_automacao_gitbash.sh:159:    ATT/tests/test_rtd_option_quotes_repository_contract.py
scripts/fase5_automacao_gitbash.sh:160:    ATT/tests/test_structure_leg_rtd_enrichment_service.py
scripts/fase5_automacao_gitbash.sh:164:    scripts/refresh_rtd_symbol_to_option_quotes.py
scripts/fase5_automacao_gitbash.sh:176:| Contadores de RTD identificados ou criados | A validar |
scripts/fase5_automacao_gitbash.sh:177:| Contadores de payoff identificados ou criados | A validar |
scripts/fase5_automacao_gitbash.sh:252:- geração de payoff;
scripts/fase5_automacao_gitbash.sh:253:- geração de pontos em payoff_curve_points;
scripts/fase5_automacao_gitbash.sh:255:- geração ou justificativa em structure_decisions;
scripts/fase5_automacao_gitbash.sh:257:- normalização correta dos pontos de payoff.
scripts/fase5_automacao_gitbash.sh:281:    docs: fecha fase 4 payoff e decisoes
scripts/fase5_automacao_gitbash.sh:299:- geração de payoff para estruturas manuais válidas;
scripts/fase5_automacao_gitbash.sh:301:- gravação ou rastreabilidade de pontos de payoff;
scripts/fase5_automacao_gitbash.sh:303:- correção de normalização de pontos de payoff;
scripts/fase5_automacao_gitbash.sh:392:  run_grep "run_derived_pipeline|run_rtd_option_quotes_pipeline|run_rtd_refresh_full|payoff_curve_points|structure_decisions|RTD|rtd|payoff|decision|decisions"
scripts/fase5_automacao_gitbash.sh:402:  echo "- Confirmar se há contadores de RTD, payoff e decisões."
scripts/fase5_automacao_gitbash.sh:420:  "scripts/run_derived_pipeline.py"
scripts/fase5_automacao_gitbash.sh:421:  "scripts/run_rtd_option_quotes_pipeline.py"
scripts/fase5_automacao_gitbash.sh:422:  "scripts/run_rtd_refresh_full.py"
scripts/fase5_automacao_gitbash.sh:495:  check_term "Pontos de payoff" "payoff_points|payoff_curve_points|pontos_payoff|pontos de payoff"
scripts/fase5_automacao_gitbash.sh:496:  check_term "Decisões" "decisions|structure_decisions|decisoes|decisões"
scripts/fase5_automacao_gitbash.sh:497:  check_term "Cotações RTD" "RTD|rtd|quotes|option_quotes|cotacoes|cotações"
scripts/fase5_automacao_gitbash.sh:508:  write_occurrences "Pontos de payoff" "payoff_points|payoff_curve_points|pontos_payoff|pontos de payoff"
scripts/fase5_automacao_gitbash.sh:509:  write_occurrences "Decisões" "decisions|structure_decisions|decisoes|decisões"
scripts/fase5_automacao_gitbash.sh:510:  write_occurrences "Cotações RTD" "RTD|rtd|quotes|option_quotes|cotacoes|cotações"
scripts/fase5_automacao_gitbash.sh:523:  echo "- pontos de payoff gerados;"
scripts/fase5_automacao_gitbash.sh:525:  echo "- cotações RTD atualizadas;"
scripts/fase5_buscar_fluxo_atualizar_dados.sh:63:  run_grep "run_derived_pipeline|run_rtd_option_quotes_pipeline|run_rtd_refresh_full|payoff_curve_points|structure_decisions|RTD|rtd|payoff|decision|decisions"
scripts/fase5_buscar_fluxo_atualizar_dados.sh:73:  echo "- Confirmar se há contadores de RTD, payoff e decisões."
scripts/fase5_checar_resumo_pipeline.sh:11:  "scripts/run_derived_pipeline.py"
scripts/fase5_checar_resumo_pipeline.sh:12:  "scripts/run_rtd_option_quotes_pipeline.py"
scripts/fase5_checar_resumo_pipeline.sh:13:  "scripts/run_rtd_refresh_full.py"
scripts/fase5_checar_resumo_pipeline.sh:86:  check_term "Pontos de payoff" "payoff_points|payoff_curve_points|pontos_payoff|pontos de payoff"
scripts/fase5_checar_resumo_pipeline.sh:87:  check_term "Decisões" "decisions|structure_decisions|decisoes|decisões"
scripts/fase5_checar_resumo_pipeline.sh:88:  check_term "Cotações RTD" "RTD|rtd|quotes|option_quotes|cotacoes|cotações"
scripts/fase5_checar_resumo_pipeline.sh:99:  write_occurrences "Pontos de payoff" "payoff_points|payoff_curve_points|pontos_payoff|pontos de payoff"
scripts/fase5_checar_resumo_pipeline.sh:100:  write_occurrences "Decisões" "decisions|structure_decisions|decisoes|decisões"
scripts/fase5_checar_resumo_pipeline.sh:101:  write_occurrences "Cotações RTD" "RTD|rtd|quotes|option_quotes|cotacoes|cotações"
scripts/fase5_checar_resumo_pipeline.sh:114:  echo "- pontos de payoff gerados;"
scripts/fase5_checar_resumo_pipeline.sh:116:  echo "- cotações RTD atualizadas;"
scripts/import_legacy_structure_legs.py:28:            "Importa pernas legadas manual/rtd para structure_legs "
scripts/import_lista_rtd_excel_to_option_quotes.py:2:Importa cotações RTD de opções do LISTA_RTD.xlsm para rtd_option_quotes.
scripts/import_lista_rtd_excel_to_option_quotes.py:5:    LISTA_RTD.xlsm aberto no Excel
scripts/import_lista_rtd_excel_to_option_quotes.py:6:        -> aba RTD_OPTION_QUOTES ou RTD_PROBE_OPTIONS
scripts/import_lista_rtd_excel_to_option_quotes.py:7:        -> tabela rtd_option_quotes
scripts/import_lista_rtd_excel_to_option_quotes.py:10:    python scripts/import_lista_rtd_excel_to_option_quotes.py --db dados/app.db
scripts/import_lista_rtd_excel_to_option_quotes.py:11:    python scripts/import_lista_rtd_excel_to_option_quotes.py --db dados/app.db --dry-run
scripts/import_lista_rtd_excel_to_option_quotes.py:12:    python scripts/import_lista_rtd_excel_to_option_quotes.py --db dados/app.db --json
scripts/import_lista_rtd_excel_to_option_quotes.py:27:DEFAULT_WORKBOOK = "LISTA_RTD.xlsm"
scripts/import_lista_rtd_excel_to_option_quotes.py:28:DEFAULT_SHEETS = ["RTD_OPTION_QUOTES", "RTD_PROBE_OPTIONS", "RTD-BTG LISTA"]
scripts/import_lista_rtd_excel_to_option_quotes.py:220:    - aguarda RTD atualizar;
scripts/import_lista_rtd_excel_to_option_quotes.py:342:        "Nenhuma aba RTD encontrada. "
scripts/import_lista_rtd_excel_to_option_quotes.py:427:    columns = get_table_columns(conn, "rtd_option_quotes")
scripts/import_lista_rtd_excel_to_option_quotes.py:430:        raise RuntimeError("Tabela rtd_option_quotes não encontrada no banco.")
scripts/import_lista_rtd_excel_to_option_quotes.py:436:            "Tabela rtd_option_quotes está sem colunas obrigatórias: "
scripts/import_lista_rtd_excel_to_option_quotes.py:458:                "SELECT id FROM rtd_option_quotes WHERE codigo_opcao = ? LIMIT 1",
scripts/import_lista_rtd_excel_to_option_quotes.py:495:            "source": "lista_rtd_excel",
scripts/import_lista_rtd_excel_to_option_quotes.py:502:            UPDATE rtd_option_quotes
scripts/import_lista_rtd_excel_to_option_quotes.py:534:            INSERT INTO rtd_option_quotes (
scripts/import_lista_rtd_excel_to_option_quotes.py:588:        description="Importa LISTA_RTD.xlsm para rtd_option_quotes"
scripts/import_lista_rtd_excel_to_option_quotes.py:600:        help="Caminho do workbook RTD. Padrão: LISTA_RTD.xlsm",
scripts/import_lista_rtd_excel_to_option_quotes.py:607:            "Nome da aba. Se omitido, tenta RTD_OPTION_QUOTES "
scripts/import_lista_rtd_excel_to_option_quotes.py:608:            "e depois RTD_PROBE_OPTIONS."
scripts/import_lista_rtd_excel_to_option_quotes.py:694:            print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
scripts/import_lista_rtd_excel_to_option_quotes.py:704:        print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
scripts/import_rtd_links_to_option_quotes.py:3:Importa dados verticais de dados/RTD_LINKS.csv para rtd_option_quotes.
scripts/import_rtd_links_to_option_quotes.py:14:python scripts/import_rtd_links_to_option_quotes.py --csv dados/RTD_LINKS.csv --db dados/app.db
scripts/import_rtd_links_to_option_quotes.py:15:python scripts/import_rtd_links_to_option_quotes.py --csv dados/RTD_LINKS.csv --db dados/app.db --dry-run
scripts/import_rtd_links_to_option_quotes.py:212:        "source": "rtd_links",
scripts/import_rtd_links_to_option_quotes.py:307:        FROM rtd_option_quotes
scripts/import_rtd_links_to_option_quotes.py:323:        "ativo_base = COALESCE(excluded.ativo_base, rtd_option_quotes.ativo_base)",
scripts/import_rtd_links_to_option_quotes.py:324:        "call_put = COALESCE(excluded.call_put, rtd_option_quotes.call_put)",
scripts/import_rtd_links_to_option_quotes.py:325:        "strike = COALESCE(excluded.strike, rtd_option_quotes.strike)",
scripts/import_rtd_links_to_option_quotes.py:326:        "vencimento = COALESCE(excluded.vencimento, rtd_option_quotes.vencimento)",
scripts/import_rtd_links_to_option_quotes.py:327:        "ultimo_preco = COALESCE(excluded.ultimo_preco, rtd_option_quotes.ultimo_preco)",
scripts/import_rtd_links_to_option_quotes.py:328:        "ultima_quantidade = COALESCE(excluded.ultima_quantidade, rtd_option_quotes.ultima_quantidade)",
scripts/import_rtd_links_to_option_quotes.py:329:        "bid = COALESCE(excluded.bid, rtd_option_quotes.bid)",
scripts/import_rtd_links_to_option_quotes.py:330:        "ask = COALESCE(excluded.ask, rtd_option_quotes.ask)",
scripts/import_rtd_links_to_option_quotes.py:331:        "volume = COALESCE(excluded.volume, rtd_option_quotes.volume)",
scripts/import_rtd_links_to_option_quotes.py:332:        "iv = COALESCE(excluded.iv, rtd_option_quotes.iv)",
scripts/import_rtd_links_to_option_quotes.py:333:        "delta = COALESCE(excluded.delta, rtd_option_quotes.delta)",
scripts/import_rtd_links_to_option_quotes.py:334:        "gamma = COALESCE(excluded.gamma, rtd_option_quotes.gamma)",
scripts/import_rtd_links_to_option_quotes.py:335:        "theta = COALESCE(excluded.theta, rtd_option_quotes.theta)",
scripts/import_rtd_links_to_option_quotes.py:336:        "vega = COALESCE(excluded.vega, rtd_option_quotes.vega)",
scripts/import_rtd_links_to_option_quotes.py:343:        INSERT INTO rtd_option_quotes ({columns_sql})
scripts/import_rtd_links_to_option_quotes.py:386:        description="Importa dados/RTD_LINKS.csv para rtd_option_quotes"
scripts/import_rtd_links_to_option_quotes.py:391:        default="dados/RTD_LINKS.csv",
scripts/import_rtd_links_to_option_quotes.py:392:        help="Caminho do CSV RTD_LINKS.csv",
scripts/import_rtd_links_to_option_quotes.py:419:    print("Importação RTD_LINKS.csv -> rtd_option_quotes")
scripts/import_rtd_option_quotes_wide_csv.py:14:from infra.bootstrap_rtd_option_quotes_schema import ensure_rtd_option_quotes_schema
scripts/import_rtd_option_quotes_wide_csv.py:196:                "source": "BTG_RTD_EXCEL",
scripts/import_rtd_option_quotes_wide_csv.py:207:        CREATE INDEX IF NOT EXISTS idx_rtd_option_quotes_codigo_opcao
scripts/import_rtd_option_quotes_wide_csv.py:208:        ON rtd_option_quotes(codigo_opcao)
scripts/import_rtd_option_quotes_wide_csv.py:226:    ensure_rtd_option_quotes_schema(db_path)
scripts/import_rtd_option_quotes_wide_csv.py:237:                "SELECT id, created_at FROM rtd_option_quotes WHERE codigo_opcao = ? ORDER BY id DESC LIMIT 1",
scripts/import_rtd_option_quotes_wide_csv.py:251:                    UPDATE rtd_option_quotes
scripts/import_rtd_option_quotes_wide_csv.py:299:                    INSERT INTO rtd_option_quotes (
scripts/import_rtd_option_quotes_wide_csv.py:369:        print("Importação RTD wide CSV")
scripts/mapear_automacao_opcoes_rtd.py:11:OUT_MD = ROOT / "docs" / "mapeamento_automacao_opcoes_rtd.md"
scripts/mapear_automacao_opcoes_rtd.py:12:OUT_JSON = ROOT / "docs" / "mapeamento_automacao_opcoes_rtd.json"
scripts/mapear_automacao_opcoes_rtd.py:58:    "rtd": ["rtd", "rtd_links", "option_quotes"],
scripts/mapear_automacao_opcoes_rtd.py:65:    "calculo": ["calculation", "pricing", "payoff", "metric", "metrics", "grega", "gregas"],
scripts/mapear_automacao_opcoes_rtd.py:69:    "repositories/rtd_option_quotes_repository.py": "Prioritário para auditoria de persistência RTD.",
scripts/mapear_automacao_opcoes_rtd.py:75:    "dados/RTD_LINKS.csv": "Prioritário para auditoria do contrato RTD/Excel.",
scripts/mapear_automacao_opcoes_rtd.py:211:        "# Mapeamento automação opções RTD — ROTA_MESTRE_2 Fase 1",
scripts/mapear_automacao_opcoes_rtd.py:217:        "Mapeamento amplo de RTD, Excel, bridge, opções, persistência, serviços e UI.",
scripts/patch_derived_payoff_timestamp_consistency.sh:8:path = Path("services/derived_payoff_persistence.py")
scripts/patch_derived_payoff_timestamp_consistency.sh:11:    raise SystemExit("[ERROR] Arquivo não encontrado: services/derived_payoff_persistence.py")
scripts/patch_derived_payoff_timestamp_consistency.sh:38:# persist(): criar timestamp único e só gravar decisão se payoff gravou
scripts/patch_derived_payoff_timestamp_consistency.sh:43:        """        self._persist_payoff(pricing_payload, result)
scripts/patch_derived_payoff_timestamp_consistency.sh:44:        self._persist_decision(pricing_payload, result)
scripts/patch_derived_payoff_timestamp_consistency.sh:46:        """        # Timestamp único para payoff + decisão.
scripts/patch_derived_payoff_timestamp_consistency.sh:50:        payoff_saved = self._persist_payoff(pricing_payload, result, snapshot_ts)
scripts/patch_derived_payoff_timestamp_consistency.sh:51:        if not payoff_saved:
scripts/patch_derived_payoff_timestamp_consistency.sh:53:                "derived_payoff_persistence: decisão não gravada porque payoff não foi salvo -- structure_id=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:58:        decision_saved = self._persist_decision(pricing_payload, result, snapshot_ts)
scripts/patch_derived_payoff_timestamp_consistency.sh:59:        if not decision_saved:
scripts/patch_derived_payoff_timestamp_consistency.sh:61:                "derived_payoff_persistence: payoff salvo, mas decisão falhou -- structure_id=%s timestamp=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:70:# _persist_payoff signature: retorna bool e recebe snapshot_ts
scripts/patch_derived_payoff_timestamp_consistency.sh:75:        """    def _persist_payoff(
scripts/patch_derived_payoff_timestamp_consistency.sh:81:        """    def _persist_payoff(
scripts/patch_derived_payoff_timestamp_consistency.sh:88:        "_persist_payoff signature",
scripts/patch_derived_payoff_timestamp_consistency.sh:91:# payoff sem pontos deve retornar False
scripts/patch_derived_payoff_timestamp_consistency.sh:93:    """            if not payoff_result.get("points"):
scripts/patch_derived_payoff_timestamp_consistency.sh:95:                    "derived_payoff_persistence: payoff sem pontos para structure_id=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:100:    """            if not payoff_result.get("points"):
scripts/patch_derived_payoff_timestamp_consistency.sh:102:                    "derived_payoff_persistence: payoff sem pontos para structure_id=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:110:# salvar payoff com timestamp único
scripts/patch_derived_payoff_timestamp_consistency.sh:112:    "            save_payoff_from_canonical_payload(payoff_result)\n",
scripts/patch_derived_payoff_timestamp_consistency.sh:113:    "            save_payoff_from_canonical_payload(payoff_result, timestamp=snapshot_ts)\n",
scripts/patch_derived_payoff_timestamp_consistency.sh:117:# payoff sucesso retorna True
scripts/patch_derived_payoff_timestamp_consistency.sh:118:if 'derived_payoff_persistence: %d pontos gravados -- structure_id=%s' in text and "return True\n\n        except Exception:" not in text:
scripts/patch_derived_payoff_timestamp_consistency.sh:122:                "derived_payoff_persistence: %d pontos gravados -- structure_id=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:123:                len(payoff_result["points"]),
scripts/patch_derived_payoff_timestamp_consistency.sh:130:                "derived_payoff_persistence: %d pontos gravados -- structure_id=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:131:                len(payoff_result["points"]),
scripts/patch_derived_payoff_timestamp_consistency.sh:138:        "_persist_payoff return True",
scripts/patch_derived_payoff_timestamp_consistency.sh:141:# payoff exception retorna False
scripts/patch_derived_payoff_timestamp_consistency.sh:142:if "erro ao gravar payoff" in text and "return False\n\n    # -------------------------------------------------------------- #\n    #  decisão" not in text:
scripts/patch_derived_payoff_timestamp_consistency.sh:146:                "derived_payoff_persistence: erro ao gravar payoff -- structure_id=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:153:                "derived_payoff_persistence: erro ao gravar payoff -- structure_id=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:160:        "_persist_payoff return False exception",
scripts/patch_derived_payoff_timestamp_consistency.sh:164:# _persist_decision signature: retorna bool e recebe snapshot_ts
scripts/patch_derived_payoff_timestamp_consistency.sh:167:    # cuidado: já pode existir no payoff; testar assinatura específica da decisão
scripts/patch_derived_payoff_timestamp_consistency.sh:170:if """    def _persist_decision(
scripts/patch_derived_payoff_timestamp_consistency.sh:178:        """    def _persist_decision(
scripts/patch_derived_payoff_timestamp_consistency.sh:184:        """    def _persist_decision(
scripts/patch_derived_payoff_timestamp_consistency.sh:191:        "_persist_decision signature",
scripts/patch_derived_payoff_timestamp_consistency.sh:207:        "save_decision timestamp",
scripts/patch_derived_payoff_timestamp_consistency.sh:211:if 'derived_payoff_persistence: decisão gravada -- structure_id=%s' in text and "return True\n\n        except Exception:" in text:
scripts/patch_derived_payoff_timestamp_consistency.sh:212:    # Já existe return True em payoff; precisamos garantir decisão também.
scripts/patch_derived_payoff_timestamp_consistency.sh:215:decision_success_old = """            logger.info(
scripts/patch_derived_payoff_timestamp_consistency.sh:216:                "derived_payoff_persistence: decisão gravada -- structure_id=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:223:decision_success_new = """            logger.info(
scripts/patch_derived_payoff_timestamp_consistency.sh:224:                "derived_payoff_persistence: decisão gravada -- structure_id=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:233:if decision_success_old in text:
scripts/patch_derived_payoff_timestamp_consistency.sh:234:    text = text.replace(decision_success_old, decision_success_new, 1)
scripts/patch_derived_payoff_timestamp_consistency.sh:237:decision_exception_old = """            logger.exception(
scripts/patch_derived_payoff_timestamp_consistency.sh:238:                "derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:245:decision_exception_new = """            logger.exception(
scripts/patch_derived_payoff_timestamp_consistency.sh:246:                "derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:254:if decision_exception_old in text:
scripts/patch_derived_payoff_timestamp_consistency.sh:255:    text = text.replace(decision_exception_old, decision_exception_new, 1)
scripts/patch_derived_payoff_timestamp_consistency.sh:263:    "save_payoff_from_canonical_payload(payoff_result, timestamp=snapshot_ts)",
scripts/patch_derived_payoff_timestamp_consistency.sh:265:    "payoff_saved = self._persist_payoff(pricing_payload, result, snapshot_ts)",
scripts/patch_derived_payoff_timestamp_consistency.sh:266:    "decision_saved = self._persist_decision(pricing_payload, result, snapshot_ts)",
scripts/patch_derived_payoff_timestamp_consistency.sh:280:    print("[OK] Patch aplicado em services/derived_payoff_persistence.py")
scripts/patch_derived_payoff_timestamp_consistency.sh:283:python -m py_compile services/derived_payoff_persistence.py
scripts/purge_derived_snapshots.py:12:    "payoff_curve_points",
scripts/purge_derived_snapshots.py:13:    "structure_decisions",
scripts/purge_derived_snapshots.py:14:    "payoff_curve_summary",
scripts/refresh_rtd_option_quotes_excel.ps1:2:    [string]$WorkbookPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "LISTA_RTD.xlsm"),
scripts/refresh_rtd_option_quotes_excel.ps1:3:    [string]$SymbolsPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "dados\rtd_symbols.txt"),
scripts/refresh_rtd_option_quotes_excel.ps1:4:    [string]$CsvPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "dados\RTD_LINKS.csv"),
scripts/refresh_rtd_option_quotes_excel.ps1:61:    $sheetName = "RTD_OPTION_QUOTES"
scripts/refresh_rtd_option_quotes_excel.ps1:125:            $formula = '=RTD("btg_pro_rtd";"";"' + $field + '";$A' + $row + ')'
scripts/refresh_rtd_option_quotes_excel.ps1:137:    Write-Host "Aba RTD_OPTION_QUOTES preenchida. Linhas:" $symbols.Count
scripts/refresh_rtd_option_quotes_excel.ps1:138:    Write-Host "Recalculando Excel/RTD..."
scripts/refresh_rtd_option_quotes_excel.ps1:150:    # Copia somente a aba RTD_OPTION_QUOTES para novo workbook e salva como CSV UTF-8.
scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:10:BASE_SCRIPT = Path(__file__).resolve().with_name("refresh_rtd_symbol_to_option_quotes.py")
scripts/repair_derived_db_consistency.py:20:        FROM structure_decisions d
scripts/repair_derived_db_consistency.py:21:        LEFT JOIN payoff_curve_points p
scripts/repair_derived_db_consistency.py:27:    orphan_decisions = cur.fetchall()
scripts/repair_derived_db_consistency.py:31:        FROM payoff_curve_points p
scripts/repair_derived_db_consistency.py:32:        LEFT JOIN structure_decisions d
scripts/repair_derived_db_consistency.py:41:        not orphan_decisions and not orphan_points,
scripts/repair_derived_db_consistency.py:42:        len(orphan_decisions),
scripts/repair_derived_db_consistency.py:73:        "--prune-unmatched-decisions",
scripts/repair_derived_db_consistency.py:122:            FROM payoff_curve_points
scripts/repair_derived_db_consistency.py:127:        decisions = con.execute("""
scripts/repair_derived_db_consistency.py:133:            FROM structure_decisions
scripts/repair_derived_db_consistency.py:138:        used_decision_ids: set[int] = set()
scripts/repair_derived_db_consistency.py:142:            for d in decisions:
scripts/repair_derived_db_consistency.py:143:                if d["id"] in used_decision_ids:
scripts/repair_derived_db_consistency.py:166:            used_decision_ids.add(nearest["id"])
scripts/repair_derived_db_consistency.py:186:            for _, decision_id, delta, old_ts, new_ts, sid, aba in updates:
scripts/repair_derived_db_consistency.py:188:                    f"[MATCH] decision_id={decision_id} "
scripts/repair_derived_db_consistency.py:196:                for new_ts, decision_id, *_rest in updates:
scripts/repair_derived_db_consistency.py:199:                        UPDATE structure_decisions
scripts/repair_derived_db_consistency.py:203:                        (new_ts, decision_id),
scripts/repair_derived_db_consistency.py:216:        deleted_decisions = 0
scripts/repair_derived_db_consistency.py:219:        if args.prune_unmatched_decisions:
scripts/repair_derived_db_consistency.py:222:                FROM structure_decisions d
scripts/repair_derived_db_consistency.py:223:                LEFT JOIN payoff_curve_points p
scripts/repair_derived_db_consistency.py:244:                        f"DELETE FROM structure_decisions WHERE id IN ({placeholders})",
scripts/repair_derived_db_consistency.py:247:                    deleted_decisions = cur.rowcount
scripts/repair_derived_db_consistency.py:248:                print(f"[APPLY] Decisões órfãs removidas: {deleted_decisions}")
scripts/repair_derived_db_consistency.py:255:                FROM payoff_curve_points p
scripts/repair_derived_db_consistency.py:256:                LEFT JOIN structure_decisions d
scripts/repair_derived_db_consistency.py:275:                        DELETE FROM payoff_curve_points
scripts/repair_derived_db_consistency.py:278:                            FROM structure_decisions d
scripts/repair_derived_db_consistency.py:279:                            WHERE d.aba = payoff_curve_points.aba
scripts/repair_derived_db_consistency.py:280:                              AND d.timestamp = payoff_curve_points.timestamp
scripts/repair_derived_db_consistency.py:295:        print(f"[INFO] Decisões removidas: {deleted_decisions}")
scripts/run_derived_pipeline.py:24:_RTD_METRIC_RE = re.compile(r"^\s*(input_rows|inserted|updated|skipped):\s*(-?\d+)\s*$")
scripts/run_derived_pipeline.py:39:def _parse_rtd_pipeline_metrics(output: str) -> dict:
scripts/run_derived_pipeline.py:40:    """Extrai métricas textuais emitidas pelo pipeline RTD restaurado."""
scripts/run_derived_pipeline.py:49:        match = _RTD_METRIC_RE.match(line)
scripts/run_derived_pipeline.py:59:def _rtd_quotes_updated_count(rtd_result: dict | None) -> int:
scripts/run_derived_pipeline.py:61:    if not rtd_result:
scripts/run_derived_pipeline.py:64:    return int(rtd_result.get("inserted") or 0) + int(rtd_result.get("updated") or 0)
scripts/run_derived_pipeline.py:67:def _run_rtd_option_quotes_import(
scripts/run_derived_pipeline.py:69:    csv_path: str = "dados/RTD_LINKS.csv",
scripts/run_derived_pipeline.py:73:    Executa a cadeia operacional RTD já restaurada contra o derived.db.
scripts/run_derived_pipeline.py:76:    - Usa somente CSV local dados/RTD_LINKS.csv.
scripts/run_derived_pipeline.py:77:    - Não aciona Excel, PowerShell, COM ou refresh RTD ao vivo.
scripts/run_derived_pipeline.py:78:    - Delega importação + auditoria para scripts/run_rtd_option_quotes_pipeline.py.
scripts/run_derived_pipeline.py:81:    pipeline_script = repo_root / "scripts" / "run_rtd_option_quotes_pipeline.py"
scripts/run_derived_pipeline.py:90:            "message": f"Script RTD não encontrado: {pipeline_script}",
scripts/run_derived_pipeline.py:102:            "message": f"CSV RTD não encontrado: {resolved_csv}",
scripts/run_derived_pipeline.py:134:    metrics = _parse_rtd_pipeline_metrics(stdout)
scripts/run_derived_pipeline.py:149:    Placeholder: Gera payoff_curve_summary a partir de payoff_curve_points.
scripts/run_derived_pipeline.py:184:def _collect_pipeline_summary(rtd_result: dict | None = None) -> dict:
scripts/run_derived_pipeline.py:189:    - Inclui a quantidade de cotações RTD inseridas/atualizadas.
scripts/run_derived_pipeline.py:191:    - Apenas lê contagens do banco depois que o pipeline RTD CSV já rodou.
scripts/run_derived_pipeline.py:211:            "decisions": _first_count(
scripts/run_derived_pipeline.py:213:                "decision_snapshots",
scripts/run_derived_pipeline.py:214:                "decisions",
scripts/run_derived_pipeline.py:215:                "structure_decisions",
scripts/run_derived_pipeline.py:216:                "derived_decisions",
scripts/run_derived_pipeline.py:218:            "payoff_points": _first_count(
scripts/run_derived_pipeline.py:220:                "payoff_curve_points",
scripts/run_derived_pipeline.py:221:                "payoff_points",
scripts/run_derived_pipeline.py:222:                "derived_payoff_points",
scripts/run_derived_pipeline.py:224:            "payoff_summaries": _first_count(
scripts/run_derived_pipeline.py:226:                "payoff_curve_summary",
scripts/run_derived_pipeline.py:227:                "payoff_summaries",
scripts/run_derived_pipeline.py:228:                "derived_payoff_summary",
scripts/run_derived_pipeline.py:235:            "rtd_quotes_updated": _rtd_quotes_updated_count(rtd_result),
scripts/run_derived_pipeline.py:236:            "rtd_import": rtd_result,
scripts/run_derived_pipeline.py:237:            "warnings": int((rtd_result or {}).get("warnings") or 0),
scripts/run_derived_pipeline.py:238:            "errors": int((rtd_result or {}).get("errors") or 0),
scripts/run_derived_pipeline.py:258:        "--skip-rtd",
scripts/run_derived_pipeline.py:260:        help="Não importar dados/RTD_LINKS.csv para rtd_option_quotes no derived.db",
scripts/run_derived_pipeline.py:263:        "--rtd-csv",
scripts/run_derived_pipeline.py:264:        default="dados/RTD_LINKS.csv",
scripts/run_derived_pipeline.py:265:        help="Caminho do CSV RTD usado pelo pipeline derivado",
scripts/run_derived_pipeline.py:280:    rtd_result = None
scripts/run_derived_pipeline.py:281:    if args.skip_rtd:
scripts/run_derived_pipeline.py:282:        print("\n[PIPELINE] Importação RTD pulada por --skip-rtd.")
scripts/run_derived_pipeline.py:283:        rtd_result = {
scripts/run_derived_pipeline.py:294:        print("\n[PIPELINE] Importando cotações RTD para derived.db...")
scripts/run_derived_pipeline.py:295:        rtd_result = _run_rtd_option_quotes_import(
scripts/run_derived_pipeline.py:297:            csv_path=args.rtd_csv,
scripts/run_derived_pipeline.py:301:        if int(rtd_result.get("returncode") or 0) != 0:
scripts/run_derived_pipeline.py:302:            print("[ERROR] PIPELINE FALHOU: importação/auditoria RTD falhou")
scripts/run_derived_pipeline.py:303:            if rtd_result.get("message"):
scripts/run_derived_pipeline.py:304:                print(f"[ERROR] {rtd_result.get('message')}")
scripts/run_derived_pipeline.py:305:            summary = _collect_pipeline_summary(rtd_result)
scripts/run_derived_pipeline.py:307:            return int(rtd_result.get("returncode") or 1)
scripts/run_derived_pipeline.py:313:        summary = _collect_pipeline_summary(rtd_result)
scripts/run_derived_pipeline.py:318:    summary = _collect_pipeline_summary(rtd_result)
scripts/run_derived_pipeline.py:322:    print(f"  Decisões: {_display_summary_value(summary.get('decisions'))}")
scripts/run_derived_pipeline.py:323:    print(f"  Pontos de payoff: {_display_summary_value(summary.get('payoff_points'))}")
scripts/run_derived_pipeline.py:324:    print(f"  Resumos de payoff: {_display_summary_value(summary.get('payoff_summaries'))}")
scripts/run_derived_pipeline.py:326:    print(f"  Cotações RTD atualizadas: {_display_summary_value(summary.get('rtd_quotes_updated'))}")
scripts/run_lista_rtd_option_quotes_pipeline.py:3:Pipeline LISTA_RTD.xlsm -> rtd_option_quotes.
scripts/run_lista_rtd_option_quotes_pipeline.py:6:    1. scripts/import_lista_rtd_excel_to_option_quotes.py
scripts/run_lista_rtd_option_quotes_pipeline.py:7:    2. scripts/audit_rtd_option_quotes.py
scripts/run_lista_rtd_option_quotes_pipeline.py:10:    python scripts/run_lista_rtd_option_quotes_pipeline.py --db dados/app.db --sheet RTD_PROBE_OPTIONS
scripts/run_lista_rtd_option_quotes_pipeline.py:11:    python scripts/run_lista_rtd_option_quotes_pipeline.py --db dados/app.db --sheet RTD_PROBE_OPTIONS --json
scripts/run_lista_rtd_option_quotes_pipeline.py:12:    python scripts/run_lista_rtd_option_quotes_pipeline.py --dry-run --json
scripts/run_lista_rtd_option_quotes_pipeline.py:25:IMPORT_SCRIPT = Path("scripts/import_lista_rtd_excel_to_option_quotes.py")
scripts/run_lista_rtd_option_quotes_pipeline.py:26:AUDIT_SCRIPT = Path("scripts/audit_rtd_option_quotes.py")
scripts/run_lista_rtd_option_quotes_pipeline.py:60:        description="Executa pipeline LISTA_RTD.xlsm -> rtd_option_quotes."
scripts/run_lista_rtd_option_quotes_pipeline.py:71:        default="LISTA_RTD.xlsm",
scripts/run_lista_rtd_option_quotes_pipeline.py:72:        help="Caminho do workbook RTD. Padrão: LISTA_RTD.xlsm",
scripts/run_lista_rtd_option_quotes_pipeline.py:79:            "Aba RTD. Se omitida, o importador tenta RTD_OPTION_QUOTES "
scripts/run_lista_rtd_option_quotes_pipeline.py:80:            "e depois RTD_PROBE_OPTIONS."
scripts/run_lista_rtd_option_quotes_pipeline.py:148:            print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
scripts/run_lista_rtd_option_quotes_pipeline.py:210:        print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
scripts/run_rtd_option_quotes_pipeline.py:3:Executa o pipeline operacional de cotações RTD de opções.
scripts/run_rtd_option_quotes_pipeline.py:7:    dados/RTD_LINKS.csv -> rtd_option_quotes -> auditoria
scripts/run_rtd_option_quotes_pipeline.py:11:    python scripts/run_rtd_option_quotes_pipeline.py
scripts/run_rtd_option_quotes_pipeline.py:12:    python scripts/run_rtd_option_quotes_pipeline.py --csv dados/RTD_LINKS.csv --db dados/app.db
scripts/run_rtd_option_quotes_pipeline.py:13:    python scripts/run_rtd_option_quotes_pipeline.py --dry-run
scripts/run_rtd_option_quotes_pipeline.py:14:    python scripts/run_rtd_option_quotes_pipeline.py --fail-on-warn
scripts/run_rtd_option_quotes_pipeline.py:28:IMPORT_SCRIPT = SCRIPTS_DIR / "import_rtd_option_quotes_wide_csv.py"
scripts/run_rtd_option_quotes_pipeline.py:29:AUDIT_SCRIPT = SCRIPTS_DIR / "audit_rtd_option_quotes.py"
scripts/run_rtd_option_quotes_pipeline.py:89:    csv_path: str = "dados/RTD_LINKS.csv",
scripts/run_rtd_option_quotes_pipeline.py:96:    print("Pipeline RTD option quotes")
scripts/run_rtd_option_quotes_pipeline.py:142:        description="Executa importação e auditoria de rtd_option_quotes."
scripts/run_rtd_option_quotes_pipeline.py:146:        default="dados/RTD_LINKS.csv",
scripts/run_rtd_option_quotes_pipeline.py:147:        help="Caminho do CSV RTD_LINKS.csv. Padrão: dados/RTD_LINKS.csv",
scripts/run_rtd_refresh_full.py:43:            FROM rtd_option_quotes
scripts/run_rtd_refresh_full.py:76:        description="Pipeline completo: gerar símbolos RTD, atualizar Excel/CSV e importar cotações no SQLite."
scripts/run_rtd_refresh_full.py:80:    parser.add_argument("--symbols", default="dados/rtd_symbols.txt")
scripts/run_rtd_refresh_full.py:81:    parser.add_argument("--csv", default="dados/RTD_LINKS.csv")
scripts/run_rtd_refresh_full.py:82:    parser.add_argument("--workbook", default="LISTA_RTD.xlsm")
scripts/run_rtd_refresh_full.py:99:    build_script = Path("scripts/build_rtd_symbols.py")
scripts/run_rtd_refresh_full.py:100:    import_script = Path("scripts/import_rtd_option_quotes_wide_csv.py")
scripts/run_rtd_refresh_full.py:101:    ps1_script = Path("scripts/refresh_rtd_option_quotes_excel.ps1")
scripts/run_rtd_refresh_full.py:103:    print("=== RTD Refresh Full ===")
scripts/run_rtd_refresh_full.py:195:        print("- Cadastre uma estrutura pelo sistema ou rode sem --strict para usar fallback de rtd_option_quotes.")
scripts/run_rtd_refresh_full.py:205:        print("Pipeline interrompido: nenhum símbolo para consultar no RTD.")
scripts/run_rtd_refresh_full.py:241:            print("Pipeline interrompido no refresh Excel/RTD.")
scripts/run_rtd_refresh_full.py:245:        print("Refresh Excel/RTD pulado por --skip-excel.")
scripts/run_rtd_refresh_full.py:271:    print("OK: pipeline RTD finalizado.")
scripts/seed_current_rtd_option_quotes.py:3:Limpa e popula rtd_option_quotes com dados manuais atuais das estruturas
scripts/seed_current_rtd_option_quotes.py:8:    python scripts/seed_current_rtd_option_quotes.py
scripts/seed_current_rtd_option_quotes.py:9:    python scripts/seed_current_rtd_option_quotes.py --db dados/app.db
scripts/seed_current_rtd_option_quotes.py:13:- O script limpa somente a tabela rtd_option_quotes.
scripts/seed_current_rtd_option_quotes.py:136:        if not table_exists(connection, "rtd_option_quotes"):
scripts/seed_current_rtd_option_quotes.py:137:            raise RuntimeError("Tabela rtd_option_quotes não encontrada.")
scripts/seed_current_rtd_option_quotes.py:140:            "SELECT COUNT(*) FROM rtd_option_quotes"
scripts/seed_current_rtd_option_quotes.py:143:        connection.execute("DELETE FROM rtd_option_quotes")
scripts/seed_current_rtd_option_quotes.py:146:            INSERT INTO rtd_option_quotes (
scripts/seed_current_rtd_option_quotes.py:224:            "SELECT COUNT(*) FROM rtd_option_quotes"
scripts/seed_current_rtd_option_quotes.py:229:    print("Seed rtd_option_quotes concluído.")
scripts/seed_current_rtd_option_quotes.py:240:        description="Limpa e popula rtd_option_quotes com dados atuais de SMAL e PRIO."
scripts/validate_derived_db.py:65:        points_count = safe_count("payoff_curve_points")
scripts/validate_derived_db.py:66:        decisions_count = safe_count("structure_decisions")
scripts/validate_derived_db.py:71:            print("[WARN] Tabela payoff_curve_points nao acessivel (ou nao existe).")
scripts/validate_derived_db.py:73:        if decisions_count is not None:
scripts/validate_derived_db.py:74:            print(f"[INFO] Decisoes: {decisions_count}")
scripts/validate_derived_db.py:76:            print("[WARN] Tabela structure_decisions nao acessivel (ou nao existe).")
scripts/verificar_andamento_rota.py:21:    "docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_6_RTD.md",
scripts/verificar_andamento_rota.py:38:    "payoff_pricing_engine",
scripts/verificar_andamento_rota.py:103:            "--grep=payoff_pricing_engine",
scripts/verificar_andamento_rota.py:353:        if "rtd_option_quotes" in table_names:
scripts/verificar_andamento_rota.py:354:            print_subsection("RTD option quotes")
scripts/verificar_andamento_rota.py:358:                FROM rtd_option_quotes
scripts/verificar_andamento_rota.py:361:            print(f"total_rtd_option_quotes={rows[0]['total']}")
scripts/verificar_andamento_rota.py:363:        if "payoff_curve_points" in table_names:
scripts/verificar_andamento_rota.py:368:                FROM payoff_curve_points
scripts/verificar_andamento_rota.py:371:            print(f"total_payoff_curve_points={rows[0]['total']}")
scripts/verificar_andamento_rota.py:373:        if "structure_decisions" in table_names:
scripts/verificar_andamento_rota.py:374:            print_subsection("Structure decisions")
scripts/verificar_andamento_rota.py:378:                FROM structure_decisions
scripts/verificar_andamento_rota.py:381:            print(f"total_structure_decisions={rows[0]['total']}")
repositories/market_snapshot_repository.py:5:Le legs RTD (rtd_analise_robo_legs), cotações RTD de opções
repositories/market_snapshot_repository.py:6:(rtd_option_quotes) e manuais (manual_analise_robo_legs), normaliza os campos
repositories/market_snapshot_repository.py:28:RTD_OPTION_QUOTES_SOURCE = "rtd_option_quotes"
repositories/market_snapshot_repository.py:32:_SQL_RTD_LEGS = """
repositories/market_snapshot_repository.py:54:    FROM rtd_analise_robo_legs
repositories/market_snapshot_repository.py:88:_SQL_RTD_SUMMARY = """
repositories/market_snapshot_repository.py:102:    FROM rtd_analise_robo
repositories/market_snapshot_repository.py:191:def _row_to_rtd_option_quote_leg(
repositories/market_snapshot_repository.py:196:    Converte uma cotação de rtd_option_quotes em LegMarketSnapshot mantendo
repositories/market_snapshot_repository.py:197:    os campos posicionais da leg RTD original.
repositories/market_snapshot_repository.py:199:    A tabela rtd_option_quotes é cache de cotação. Ela não define composição
repositories/market_snapshot_repository.py:201:    em rtd_analise_robo_legs.
repositories/market_snapshot_repository.py:242:        source=RTD_OPTION_QUOTES_SOURCE,
repositories/market_snapshot_repository.py:254:      get_rtd_legs(aba)                -> lista de LegMarketSnapshot source=RTD
repositories/market_snapshot_repository.py:255:      get_rtd_option_quote_legs(aba)   -> lista enriquecida source=rtd_option_quotes
repositories/market_snapshot_repository.py:257:      get_rtd_summary(aba)             -> dict com cabecalho RTD ou None
repositories/market_snapshot_repository.py:271:    # -- RTD ------------------------------------------------------------------
repositories/market_snapshot_repository.py:273:    def get_rtd_legs(self, ref: StructureRef | str) -> list[LegMarketSnapshot]:
repositories/market_snapshot_repository.py:276:            rows = conn.execute(_SQL_RTD_LEGS, (aba,)).fetchall()
repositories/market_snapshot_repository.py:277:        return [_row_to_leg(r, SnapshotSource.RTD) for r in rows]
repositories/market_snapshot_repository.py:279:    def get_rtd_option_quote_legs(self, ref: StructureRef | str) -> list[LegMarketSnapshot]:
repositories/market_snapshot_repository.py:281:        Retorna legs RTD enriquecidas com rtd_option_quotes.
repositories/market_snapshot_repository.py:283:        A composição da estrutura vem de rtd_analise_robo_legs. Para cada ativo
repositories/market_snapshot_repository.py:284:        dessa composição, se houver cotação em rtd_option_quotes.codigo_opcao,
repositories/market_snapshot_repository.py:287:        base_legs = self.get_rtd_legs(ref)
repositories/market_snapshot_repository.py:321:            FROM rtd_option_quotes
repositories/market_snapshot_repository.py:330:            # Banco sem tabela rtd_option_quotes: mantém compatibilidade com
repositories/market_snapshot_repository.py:345:                enriched.append(_row_to_rtd_option_quote_leg(base_leg, quote_row))
repositories/market_snapshot_repository.py:349:    def get_rtd_summary(self, ref: StructureRef | str) -> Optional[dict]:
repositories/market_snapshot_repository.py:352:            row = conn.execute(_SQL_RTD_SUMMARY, (aba,)).fetchone()
repositories/market_snapshot_repository.py:370:        source: SnapshotSource = SnapshotSource.RTD,
repositories/market_snapshot_repository.py:374:        if source == SnapshotSource.RTD:
repositories/market_snapshot_repository.py:375:            legs = self.get_rtd_legs(ref)
repositories/market_snapshot_repository.py:376:            summary = self.get_rtd_summary(ref)
repositories/robo_legs_repository.py:36:      manual_analise_robo_legs > rtd_analise_robo_legs
repositories/robo_legs_repository.py:57:        - Se vazio, tenta RTD
repositories/robo_legs_repository.py:72:        rtd = self._query_legs(
repositories/robo_legs_repository.py:73:            table="rtd_analise_robo_legs",
repositories/robo_legs_repository.py:76:            fonte=FonteType.RTD,
repositories/robo_legs_repository.py:78:        return rtd
repositories/robo_legs_repository.py:101:        prefer: str = "manual_then_rtd",
repositories/robo_legs_repository.py:112:                    SELECT timestamp FROM rtd_analise_robo_legs WHERE aba = ?
repositories/robo_legs_repository.py:128:                "SELECT DISTINCT timestamp FROM rtd_analise_robo_legs "
repositories/robo_legs_repository.py:271:        prefer: str = "manual_then_rtd",
repositories/robo_legs_status_repository.py:47:        Retorna (manual_latest_ts, rtd_latest_ts) para a aba.
repositories/robo_legs_status_repository.py:57:                "SELECT MAX(timestamp) AS ts FROM rtd_analise_robo_legs WHERE aba = ?",
repositories/robo_legs_status_repository.py:76:        Retorna (manual_latest_ts, rtd_latest_ts).
repositories/rtd_option_quotes_repository.py:1:# repositories/rtd_option_quotes_repository.py
repositories/rtd_option_quotes_repository.py:3:Repositorio para consulta de cotações de opções em rtd_option_quotes.
repositories/rtd_option_quotes_repository.py:35:            FROM rtd_option_quotes
repositories/rtd_option_quotes_repository.py:55:            FROM rtd_option_quotes
repositories/rtd_option_quotes_repository.py:68:            FROM rtd_option_quotes
repositories/structure_events_repository.py:15:Tabelas legadas como rtd_encerramentos_manuais e rtd_rolls_detectados seguem
repositories/system_snapshots_repository.py:16:    "payoff_json",
repositories/system_snapshots_repository.py:17:    "decision_json",
repositories/system_snapshots_repository.py:90:        payoff_json: dict[str, Any] | list[Any] | None = None,
repositories/system_snapshots_repository.py:91:        decision_json: dict[str, Any] | list[Any] | None = None,
repositories/system_snapshots_repository.py:123:                    payoff_json,
repositories/system_snapshots_repository.py:124:                    decision_json,
repositories/system_snapshots_repository.py:140:                    _to_json(payoff_json),
repositories/system_snapshots_repository.py:141:                    _to_json(decision_json),
repositories/ui_data_table_candidates.py:8:legados de staging, como tabelas rtd_*.
repositories/ui_data_table_candidates.py:12:    "structure_decisions",
repositories/ui_data_table_candidates.py:13:    "rtd_consolidacoes",
repositories/ui_data_table_candidates.py:14:    "rtd_consolidations",
repositories/ui_data_table_candidates.py:15:    "decisions",
repositories/ui_data_table_candidates.py:16:    "rtd_decisions",
repositories/ui_data_table_candidates.py:20:    "payoff_curve_points",
repositories/ui_data_table_candidates.py:21:    "rtd_payoff_points",
repositories/ui_data_table_candidates.py:22:    "rtd_payoff_curva",
repositories/ui_data_table_candidates.py:23:    "payoff_points",
services/calculation_orchestrator.py:3:# alteracao_46: _request_to_payoff_dict, run_payoff, run_decision
services/calculation_orchestrator.py:4:# alteracao_47: run_full_pipeline, multiplier fix (1.0), run_decision auto-extract
services/calculation_orchestrator.py:20:from domain.payoff import compute_payoff_from_canonical_input
services/calculation_orchestrator.py:21:from domain.decision import compute_decision_from_contract
services/calculation_orchestrator.py:97:        source=str(snapshot_row.get("source", "rtd")),
services/calculation_orchestrator.py:111:def _request_to_payoff_dict(
services/calculation_orchestrator.py:149:def run_payoff(
services/calculation_orchestrator.py:156:    """Executa calculo de payoff a partir de um CalculationRequest."""
services/calculation_orchestrator.py:157:    canonical = _request_to_payoff_dict(request, extra_meta=extra_meta)
services/calculation_orchestrator.py:158:    return compute_payoff_from_canonical_input(
services/calculation_orchestrator.py:166:def run_decision(
services/calculation_orchestrator.py:168:    payoff: Optional[dict] = None,
services/calculation_orchestrator.py:175:    if _pl_max is None and payoff:
services/calculation_orchestrator.py:176:        _pl_max = float(payoff.get("pl_max") or 0.0)
services/calculation_orchestrator.py:181:    if _pl_atual is None and payoff:
services/calculation_orchestrator.py:182:        _pl_atual = float(payoff.get("pl_atual") or payoff.get("pl_now") or 0.0)
services/calculation_orchestrator.py:195:    return compute_decision_from_contract(contract, payoff=payoff)
services/calculation_orchestrator.py:205:    """alteracao_47: pipeline completo payoff + decision."""
services/calculation_orchestrator.py:206:    payoff_result = run_payoff(
services/calculation_orchestrator.py:213:    decision_result = run_decision(request, payoff=payoff_result)
services/calculation_orchestrator.py:216:        "payoff":           payoff_result,
services/calculation_orchestrator.py:217:        "decision":         decision_result,
services/calculation_orchestrator.py:233:    - Executar payoff e decisao sem acessar raw DB diretamente
services/calculation_orchestrator.py:291:            source=str(market_snapshot_dict.get("source", "rtd")),
services/calculation_orchestrator.py:303:    def _request_to_payoff_dict(self, request: CalculationRequest) -> Dict[str, Any]:
services/calculation_orchestrator.py:304:        """Converte CalculationRequest para o dict de payoff."""
services/calculation_orchestrator.py:338:    # run_payoff / run_decision / run_full_pipeline
services/calculation_orchestrator.py:341:    def run_payoff(
services/calculation_orchestrator.py:348:        canonical = self._request_to_payoff_dict(request)
services/calculation_orchestrator.py:349:        return compute_payoff_from_canonical_input(
services/calculation_orchestrator.py:356:    def run_decision(
services/calculation_orchestrator.py:359:        payoff_result: Optional[Dict[str, Any]] = None,
services/calculation_orchestrator.py:361:        if payoff_result is None:
services/calculation_orchestrator.py:362:            payoff_result = self.run_payoff(request)
services/calculation_orchestrator.py:365:            payoff_result.get("pl_max") or payoff_result.get("max_profit") or 0.0
services/calculation_orchestrator.py:368:            payoff_result.get("pl_atual")
services/calculation_orchestrator.py:369:            or payoff_result.get("current_pl")
services/calculation_orchestrator.py:370:            or payoff_result.get("pl_now")
services/calculation_orchestrator.py:374:            payoff_result.get("dte_min")
services/calculation_orchestrator.py:384:        return compute_decision_from_contract(contract, payoff=payoff_result)
services/calculation_orchestrator.py:393:        """Executa run_payoff -> run_decision em sequencia."""
services/calculation_orchestrator.py:394:        payoff_result   = self.run_payoff(request, low_pct=low_pct, high_pct=high_pct, step_pct=step_pct)
services/calculation_orchestrator.py:395:        decision_result = self.run_decision(request, payoff_result=payoff_result)
services/calculation_orchestrator.py:398:            "payoff":           payoff_result,
services/calculation_orchestrator.py:399:            "decision":         decision_result,
services/calculation_orchestrator.py:490:            "source":             snapshot.get("source", "rtd"),
services/calculation_orchestrator.py:506:        Retorna dict com chaves: structure_id, payoff, decision.
services/calculation_orchestrator.py:516:            "payoff":       pipeline_result["payoff"],
services/calculation_orchestrator.py:517:            "decision":     pipeline_result["decision"],
services/canonical_input_service.py:8:  - _resolve_legs            → MarketSnapshotSelector (manual > rtd por ativo)
services/canonical_input_service.py:151:        legs pelo resultado do selector (manual > rtd).
services/canonical_input_service.py:188:    # Legs via selector (manual > rtd)
services/canonical_input_service.py:199:        consumidores downstream (pricing, greeks, payoff) tenham os dados.
services/canonical_pricing_facade.py:21:  C5: DerivedPayoffPersistence injetado como payoff_persistence_port
services/canonical_pricing_facade.py:34:from services.derived_payoff_persistence import DerivedPayoffPersistence
services/canonical_pricing_facade.py:91:            # Formatos comuns vindos de RTD/planilha:
services/canonical_pricing_facade.py:272:            # campos canônicos esperados pelo fluxo pricing/payoff
services/canonical_pricing_facade.py:347:            payoff_persistence_port=DerivedPayoffPersistence(),
services/canonical_pricing_facade.py:459:                    result={"engine": "payoff_pricing_engine", "status": "error", "error_message": error_message},
services/derived_payoff_persistence.py:1:# services/derived_payoff_persistence.py
services/derived_payoff_persistence.py:6:from domain.payoff import compute_payoff_from_canonical_input
services/derived_payoff_persistence.py:7:from services.derived_service import save_payoff_from_canonical_payload, save_decision_from_canonical_payload
services/derived_payoff_persistence.py:18:      2. Calcular a curva de payoff via domain/payoff.py
services/derived_payoff_persistence.py:33:            logger.debug("derived_payoff_persistence: pricing_payload vazio, skip.")
services/derived_payoff_persistence.py:40:                "derived_payoff_persistence: status=%r não elegível para payoff, skip.",
services/derived_payoff_persistence.py:45:        # Timestamp único para payoff + decisão.
services/derived_payoff_persistence.py:49:        payoff_saved = self._persist_payoff(pricing_payload, result, snapshot_ts)
services/derived_payoff_persistence.py:50:        if not payoff_saved:
services/derived_payoff_persistence.py:52:                "derived_payoff_persistence: decisão não gravada porque payoff não foi salvo -- structure_id=%s",
services/derived_payoff_persistence.py:57:        decision_saved = self._persist_decision(pricing_payload, result, snapshot_ts)
services/derived_payoff_persistence.py:58:        if not decision_saved:
services/derived_payoff_persistence.py:60:                "derived_payoff_persistence: payoff salvo, mas decisão falhou -- structure_id=%s timestamp=%s",
services/derived_payoff_persistence.py:66:    #  payoff                                                          #
services/derived_payoff_persistence.py:69:    def _persist_payoff(
services/derived_payoff_persistence.py:77:            payoff_result = compute_payoff_from_canonical_input(canonical_input)
services/derived_payoff_persistence.py:79:            if not payoff_result.get("points"):
services/derived_payoff_persistence.py:81:                    "derived_payoff_persistence: payoff sem pontos para structure_id=%s",
services/derived_payoff_persistence.py:86:            inserted = save_payoff_from_canonical_payload(
services/derived_payoff_persistence.py:87:                payoff_result,
services/derived_payoff_persistence.py:91:                "derived_payoff_persistence: %d pontos gravados -- structure_id=%s",
services/derived_payoff_persistence.py:99:                "derived_payoff_persistence: erro ao gravar payoff -- structure_id=%s",
services/derived_payoff_persistence.py:108:    def _persist_decision(
services/derived_payoff_persistence.py:139:            decision_dict = {
services/derived_payoff_persistence.py:140:                "decision":      "HOLD",
services/derived_payoff_persistence.py:161:            save_decision_from_canonical_payload(
services/derived_payoff_persistence.py:162:                decision=decision_dict,
services/derived_payoff_persistence.py:169:                "derived_payoff_persistence: decisão gravada -- structure_id=%s",
services/derived_payoff_persistence.py:176:                "derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s",
services/derived_payoff_persistence.py:189:        Normaliza aliases de direção para o contrato canônico de payoff.
services/derived_payoff_persistence.py:191:        domain/payoff.py exige leg["position_side"].
services/derived_payoff_persistence.py:224:    def _normalize_leg_for_payoff(leg: Any) -> dict[str, Any]:
services/derived_payoff_persistence.py:227:        esperado por domain.compute_payoff_from_canonical_input().
services/derived_payoff_persistence.py:277:    def _normalize_canonical_input_for_payoff(
services/derived_payoff_persistence.py:281:        Retorna uma cópia rasa do canonical_input com legs normalizadas para payoff.
services/derived_payoff_persistence.py:291:            DerivedPayoffPersistence._normalize_leg_for_payoff(leg)
services/derived_payoff_persistence.py:295:        meta.setdefault("payoff_leg_normalization", "fase_3f_fix1_position_side_from_side")
services/derived_payoff_persistence.py:310:        Monta o canonical_input esperado por compute_payoff_from_canonical_input().
services/derived_payoff_persistence.py:317:        # estrito de domain/payoff.py.
services/derived_payoff_persistence.py:319:            return DerivedPayoffPersistence._normalize_canonical_input_for_payoff(
services/derived_payoff_persistence.py:334:        meta.setdefault("payoff_leg_normalization", "fase_3f_fix1_position_side_from_side")
services/derived_payoff_persistence.py:342:                    DerivedPayoffPersistence._normalize_leg_for_payoff(leg)
services/derived_service.py:4:alteracao_30/alteracao_57c -- Servico de persistencia de dados derivados (payoff + decisoes).
services/derived_service.py:6:alteracao_65           -- get_payoff_by_aba() removida da interface pública (standalone).
services/derived_service.py:17:    cleanup_old_decisions,
services/derived_service.py:18:    cleanup_old_payoff_data,
services/derived_service.py:20:    insert_payoff_points,
services/derived_service.py:21:    insert_structure_decision,
services/derived_service.py:160:def save_payoff_curve(
services/derived_service.py:209:        return insert_payoff_points(
services/derived_service.py:220:def save_payoff_from_canonical_payload(
services/derived_service.py:221:    payoff: Dict[str, Any],
services/derived_service.py:229:        structure_id=payoff.get("structure_id"),
services/derived_service.py:230:        structure_name=payoff.get("structure_name"),
services/derived_service.py:231:        underlying_asset=payoff.get("underlying_asset"),
services/derived_service.py:234:    sid_from_payload = payoff.get("structure_id")
services/derived_service.py:242:        meta=payoff.get("meta"),
services/derived_service.py:244:        structure_name=payoff.get("structure_name"),
services/derived_service.py:245:        underlying_asset=payoff.get("underlying_asset"),
services/derived_service.py:246:        reference_date=payoff.get("reference_date"),
services/derived_service.py:247:        input_meta=payoff.get("input_meta"),
services/derived_service.py:252:        sig = inspect.signature(save_payoff_curve)
services/derived_service.py:264:        return save_payoff_curve(
services/derived_service.py:266:            points=payoff.get("points", []),
services/derived_service.py:267:            spot_ref=payoff.get("spot_ref"),
services/derived_service.py:273:    return save_payoff_curve(
services/derived_service.py:275:        points=payoff.get("points", []),
services/derived_service.py:276:        spot_ref=payoff.get("spot_ref"),
services/derived_service.py:283:def save_decision(
services/derived_service.py:285:    decision: Dict[str, Any],
services/derived_service.py:302:        explicit_sid = decision.get("structure_id")
services/derived_service.py:304:        explicit_sid = (decision.get("meta") or {}).get("structure_id")
services/derived_service.py:312:    enriched_decision = {
services/derived_service.py:313:        **decision,
services/derived_service.py:316:            **(decision.get("meta") or {}),
services/derived_service.py:324:        return insert_structure_decision(
services/derived_service.py:328:            decision_dict=enriched_decision,
services/derived_service.py:332:def save_decision_from_canonical_payload(
services/derived_service.py:333:    decision: Dict[str, Any],
services/derived_service.py:355:    enriched_decision = {
services/derived_service.py:356:        **decision,
services/derived_service.py:359:            **(decision.get("meta") or {}),
services/derived_service.py:367:    return save_decision(
services/derived_service.py:369:        decision=enriched_decision,
services/derived_service.py:381:        deleted_payoff = cleanup_old_payoff_data(conn, days_to_keep=days_to_keep)
services/derived_service.py:382:        deleted_dec    = cleanup_old_decisions(conn, days_to_keep=days_to_keep)
services/derived_service.py:383:        return {"payoff_deleted": deleted_payoff, "decisions_deleted": deleted_dec}
services/derived_service.py:390:def get_all_payoff_curves():
services/derived_service.py:395:            FROM payoff_curve_points
services/derived_service.py:410:def get_payoff_by_structure_id(structure_id: int):
services/derived_service.py:412:    alteracao_56/alteracao_65: único ponto de entrada canônico para leitura de payoff.
services/derived_service.py:415:    Importante: payoff_curve_points mantém histórico por timestamp.
services/derived_service.py:426:              FROM payoff_curve_points
services/derived_service.py:430:                      FROM payoff_curve_points
services/derived_service.py:449:def get_recent_decisions():
services/derived_service.py:457:                "PRAGMA table_info(structure_decisions)"
services/derived_service.py:462:            "timestamp", "aba", "decision", "level",
services/derived_service.py:475:            FROM structure_decisions
services/derived_service.py:480:        decisions = []
services/derived_service.py:515:            decisions.append(item)
services/derived_service.py:517:        return decisions
services/derived_service.py:543:# get_payoff_by_aba() removida da interface pública.
services/derived_service.py:544:# get_payoff_by_structure_id() é o único ponto de entrada canônico.
services/derived_service.py:549:    alteracao_65: get_payoff_by_aba() nao exposta -- use get_payoff_by_structure_id().
services/derived_service.py:550:    get_payoff_by_aba() ausente por decisao de design (alteracao_65): interface simplificada.
services/derived_service.py:553:    # alteracao_65: get_payoff_by_aba() deliberadamente nao implementada nesta classe.
services/derived_service.py:554:    # Chamadores legados devem migrar para get_payoff_by_structure_id().
services/derived_service.py:556:    def get_payoff_by_structure_id(self, structure_id: int):
services/derived_service.py:557:        """Retorna pontos de payoff para a estrutura informada."""
services/derived_service.py:558:        return get_payoff_by_structure_id(structure_id)
services/derived_service.py:560:    def save_payoff_curve(self, *args, **kwargs):
services/derived_service.py:561:        return save_payoff_curve(*args, **kwargs)
services/derived_service.py:563:    def save_decision(self, *args, **kwargs):
services/derived_service.py:564:        return save_decision(*args, **kwargs)
services/legacy_structure_legs_reader.py:16:      - ler pernas legadas manual/rtd;
services/market_snapshot_selector.py:3:Política de precedência de snapshots: manual > rtd_option_quotes > rtd.
services/market_snapshot_selector.py:7:  - Caso contrário, se existir cotação em rtd_option_quotes para a leg RTD, usa rtd_option_quotes
services/market_snapshot_selector.py:8:  - Caso contrário, usa rtd_analise_robo_legs
services/market_snapshot_selector.py:19:RTD_OPTION_QUOTES_SOURCE = "rtd_option_quotes"
services/market_snapshot_selector.py:47:    Aplica a política manual > rtd_option_quotes > rtd para selecionar o snapshot canônico.
services/market_snapshot_selector.py:75:        rtd_legs = self._repo.get_rtd_legs(effective_ref)
services/market_snapshot_selector.py:77:        get_rtd_option_quote_legs = getattr(
services/market_snapshot_selector.py:79:            "get_rtd_option_quote_legs",
services/market_snapshot_selector.py:82:        if callable(get_rtd_option_quote_legs):
services/market_snapshot_selector.py:83:            rtd_option_quote_legs = get_rtd_option_quote_legs(effective_ref)
services/market_snapshot_selector.py:85:            rtd_option_quote_legs = []
services/market_snapshot_selector.py:95:        rtd_option_quote_by_ativo: dict[str, LegMarketSnapshot] = {}
services/market_snapshot_selector.py:96:        for leg in rtd_option_quote_legs:
services/market_snapshot_selector.py:97:            if leg.ativo and leg.ativo not in rtd_option_quote_by_ativo:
services/market_snapshot_selector.py:98:                rtd_option_quote_by_ativo[leg.ativo] = leg
services/market_snapshot_selector.py:100:        rtd_by_ativo: dict[str, LegMarketSnapshot] = {}
services/market_snapshot_selector.py:101:        for leg in rtd_legs:
services/market_snapshot_selector.py:102:            if leg.ativo and leg.ativo not in rtd_by_ativo:
services/market_snapshot_selector.py:103:                rtd_by_ativo[leg.ativo] = leg
services/market_snapshot_selector.py:107:            | set(rtd_option_quote_by_ativo)
services/market_snapshot_selector.py:108:            | set(rtd_by_ativo)
services/market_snapshot_selector.py:117:                if ativo in rtd_option_quote_by_ativo or ativo in rtd_by_ativo:
services/market_snapshot_selector.py:119:            elif ativo in rtd_option_quote_by_ativo:
services/market_snapshot_selector.py:120:                legs_selected.append(rtd_option_quote_by_ativo[ativo])
services/market_snapshot_selector.py:122:                legs_selected.append(rtd_by_ativo[ativo])
services/market_snapshot_selector.py:126:        elif rtd_option_quote_legs:
services/market_snapshot_selector.py:127:            source = RTD_OPTION_QUOTES_SOURCE
services/market_snapshot_selector.py:129:            source = SnapshotSource.RTD
services/payoff_persistence_port.py:1:# services/payoff_persistence_port.py
services/payoff_persistence_port.py:7:    Contrato de persistência derivada (payoff + decisão).
services/payoff_pricing_engine.py:3:from domain.payoff import compute_payoff_curve_from_canonical_legs
services/payoff_pricing_engine.py:9:    Motor financeiro inicial baseado na curva de payoff canônica.
services/payoff_pricing_engine.py:18:    engine_name = "payoff_pricing_engine"
services/payoff_pricing_engine.py:40:        payoff = compute_payoff_curve_from_canonical_legs(
services/payoff_pricing_engine.py:48:        pl_max = payoff.get("pl_max")
services/payoff_pricing_engine.py:49:        pl_min = payoff.get("pl_min")
services/payoff_pricing_engine.py:72:                "payoff_points": len(payoff.get("points") or []),
services/payoff_pricing_engine.py:85:                "method": "expiration_payoff_grid",
services/payoff_pricing_engine.py:87:            "payoff": payoff,
services/pricing_execution_app_service.py:6:  - execute_pricing() agora usa CanonicalPricingFacade (manual > rtd, caminho canônico)
services/pricing_execution_orchestration_service.py:64:                    "engine": "payoff_pricing_engine",
services/pricing_execution_persistence_service.py:7:from services.payoff_persistence_port import PayoffPersistencePort
services/pricing_execution_persistence_service.py:16:        payoff_persistence_port: PayoffPersistencePort | None = None,
services/pricing_execution_persistence_service.py:22:        self._payoff_port = payoff_persistence_port
services/pricing_execution_persistence_service.py:67:        #  alteracao_21 -- persistência derivada (payoff + decisão)           #
services/pricing_execution_persistence_service.py:70:        if self._payoff_port is not None:
services/pricing_execution_persistence_service.py:72:                self._payoff_port.persist(
services/pricing_execution_persistence_service.py:78:                    "payoff_persistence_port.persist() falhou -- execução id=%s não afetada",
services/pricing_execution_persistence_service.py:124:                payoff_json=self._extract_result_field(inner, "payoff"),
services/pricing_execution_persistence_service.py:125:                decision_json=self._extract_result_field(inner, "decision"),
services/pricing_execution_service.py:3:from services.payoff_pricing_engine import PayoffPricingEngine
services/robo_legs_service.py:23:      - obtém legs com regra manual > rtd
services/robo_legs_status_service.py:65:            manual_latest, rtd_latest = self.status_repo.latest_timestamps(ref=ref)
services/robo_legs_status_service.py:69:            manual_latest, rtd_latest = self.status_repo.latest_timestamps(aba)
services/robo_legs_status_service.py:74:        elif rtd_latest is not None:
services/robo_legs_status_service.py:75:            chosen_fonte = FonteType.RTD
services/robo_legs_status_service.py:76:            chosen_ts = rtd_latest
services/robo_legs_status_service.py:85:                rtd_latest_ts=None,
services/robo_legs_status_service.py:106:            rtd_latest_ts=rtd_latest,
services/structure_analysis_service.py:6:from domain.decision import compute_decision_from_payoff
services/structure_analysis_service.py:7:from domain.payoff import compute_payoff_from_canonical_input
services/structure_analysis_service.py:61:        # 6. Calcula payoff
services/structure_analysis_service.py:62:        payoff = compute_payoff_from_canonical_input(canonical_input)
services/structure_analysis_service.py:64:        # 7. Valida payoff -- se inválido, retorna HOLD com erro estruturado
services/structure_analysis_service.py:65:        if not payoff or not payoff.get("pl_max"):
services/structure_analysis_service.py:67:                "error": "payoff is required",
services/structure_analysis_service.py:69:                "reasons": ["invalid_payoff"],
services/structure_analysis_service.py:72:            decision = {
services/structure_analysis_service.py:73:                "decision":      "HOLD",
services/structure_analysis_service.py:91:                "payoff":   payoff,
services/structure_analysis_service.py:92:                "decision": decision,
services/structure_analysis_service.py:96:        decision = compute_decision_from_payoff(
services/structure_analysis_service.py:97:            payoff=payoff,
services/structure_analysis_service.py:105:        decision["dte_min"] = dte_min_effective
services/structure_analysis_service.py:108:        decision["why"]["dte_gate"] = dte_gate
services/structure_analysis_service.py:119:            "payoff":   payoff,
services/structure_analysis_service.py:120:            "decision": decision,
services/structure_leg_rtd_enrichment_service.py:1:"""Service de enriquecimento de legs de estruturas via RTD.
services/structure_leg_rtd_enrichment_service.py:5:- consultar rtd_option_quotes por codigo_opcao;
services/structure_leg_rtd_enrichment_service.py:18:    """Enriquece uma leg de estrutura usando dados de rtd_option_quotes."""
services/structure_leg_rtd_enrichment_service.py:20:    def __init__(self, rtd_option_quotes_repository: Any) -> None:
services/structure_leg_rtd_enrichment_service.py:21:        self._repo = rtd_option_quotes_repository
services/structure_leg_rtd_enrichment_service.py:31:        Campos enriquecidos via RTD:
services/structure_leg_rtd_enrichment_service.py:42:            raise ValueError("symbol is required for RTD leg enrichment")
services/structure_leg_rtd_enrichment_service.py:123:        2. ultimo_preco vindo do RTD/cache;
services/structure_leg_rtd_enrichment_service.py:175:                raise ValueError(f"missing required RTD field: {field}")
services/structure_leg_rtd_enrichment_service.py.bak_premium_from_rtd:1:"""Service de enriquecimento de legs de estruturas via RTD.
services/structure_leg_rtd_enrichment_service.py.bak_premium_from_rtd:5:- consultar rtd_option_quotes por codigo_opcao;
services/structure_leg_rtd_enrichment_service.py.bak_premium_from_rtd:18:    """Enriquece uma leg de estrutura usando dados de rtd_option_quotes."""
services/structure_leg_rtd_enrichment_service.py.bak_premium_from_rtd:20:    def __init__(self, rtd_option_quotes_repository: Any) -> None:
services/structure_leg_rtd_enrichment_service.py.bak_premium_from_rtd:21:        self._repo = rtd_option_quotes_repository
services/structure_leg_rtd_enrichment_service.py.bak_premium_from_rtd:31:        Campos enriquecidos via RTD:
services/structure_leg_rtd_enrichment_service.py.bak_premium_from_rtd:42:            raise ValueError("symbol is required for RTD leg enrichment")
services/structure_leg_rtd_enrichment_service.py.bak_premium_from_rtd:154:                raise ValueError(f"missing required RTD field: {field}")
ATT/checks/check_cleanup_residuals.py:76:    "scripts/patch_derived_payoff_timestamp_consistency.sh",
ATT/checks/check_cleanup_residuals.py:79:    "scripts/run_derived_pipeline.py",
ATT/checks/check_end_to_end.py:21:    ROOT_DIR / "domain" / "payoff.py",
ATT/checks/check_end_to_end.py:22:    ROOT_DIR / "domain" / "payoff_features.py",
ATT/checks/check_end_to_end.py:34:    ROOT_DIR / "Scripts" / "run_derived_pipeline.py",
ATT/checks/check_end_to_end.py:36:    ROOT_DIR / "Scripts" / "build_payoff_summaries.py",
ATT/checks/check_structures.py:22:    ROOT_DIR / "domain" / "payoff.py",
ATT/checks/check_structures.py:23:    ROOT_DIR / "domain" / "payoff_features.py",
ATT/checks/check_structures.py:32:    ROOT_DIR / "Scripts" / "run_derived_pipeline.py",
ATT/checks/check_structures.py:33:    ROOT_DIR / "Scripts" / "build_payoff_summaries.py",
ATT/tests/test_audit_rtd_option_quotes.py:12:    / "audit_rtd_option_quotes.py"
ATT/tests/test_audit_rtd_option_quotes.py:18:        "audit_rtd_option_quotes_under_test",
ATT/tests/test_audit_rtd_option_quotes.py:33:            CREATE TABLE rtd_option_quotes (
ATT/tests/test_audit_rtd_option_quotes.py:50:                source TEXT NOT NULL DEFAULT 'rtd_links',
ATT/tests/test_audit_rtd_option_quotes.py:75:            INSERT INTO rtd_option_quotes (
ATT/tests/test_audit_rtd_option_quotes.py:86:            VALUES (?, 'PETR4', 'CALL', 30.0, 1.0, 1.1, 'rtd_links', {updated_at_sql}, CURRENT_TIMESTAMP)
ATT/tests/test_audit_rtd_option_quotes.py:111:    assert "table not found: rtd_option_quotes" in result["errors"]
ATT/tests/test_audit_rtd_option_quotes.py:151:            CREATE TABLE rtd_option_quotes (
ATT/tests/test_canonical_pricing_facade.py:13:        "source": "rtd",
ATT/tests/test_canonical_pricing_facade.py:30:def test_snapshot_result_to_payload_normalizes_common_rtd_number_formats(
ATT/tests/test_canonical_pricing_facade.py:72:                "source": "rtd_option_quotes",
ATT/tests/test_canonical_pricing_facade.py:93:        "snapshot_source": "rtd",
ATT/tests/test_canonical_pricing_facade.py:109:    assert leg["source"] == "rtd_option_quotes"
ATT/tests/test_decision.py:1:from domain.decision import compute_decision_from_payoff
ATT/tests/test_decision.py:4:def test_compute_decision_from_payoff_should_work_without_alias_legacy_aba():
ATT/tests/test_decision.py:6:    Garante que compute_decision_from_payoff funciona com payoff canônico
ATT/tests/test_decision.py:9:    payoff = {
ATT/tests/test_decision.py:17:    result = compute_decision_from_payoff(
ATT/tests/test_decision.py:18:        payoff=payoff,
ATT/tests/test_decision.py:22:    assert "decision" in result
ATT/tests/test_decision.py:24:    assert result["decision"] in ("HOLD", "WATCH", "PREPARE", "PREPARE_ROLL", "CLOSE_REOPEN", "CLOSE")
ATT/tests/test_derived_service.py:86:def test_save_payoff_from_canonical_payload_should_use_resolved_storage_key(monkeypatch):
ATT/tests/test_derived_service.py:89:    def fake_save_payoff_curve(ref, points, spot_ref=None, meta=None, timestamp=None):
ATT/tests/test_derived_service.py:97:    monkeypatch.setattr(ds, "save_payoff_curve", fake_save_payoff_curve)
ATT/tests/test_derived_service.py:110:    result = ds.save_payoff_from_canonical_payload(payload)
ATT/tests/test_derived_service.py:125:def test_save_decision_from_canonical_payload_should_enrich_meta(monkeypatch):
ATT/tests/test_derived_service.py:128:    def fake_save_decision(ref, decision, timestamp=None):
ATT/tests/test_derived_service.py:130:        captured["decision"] = decision
ATT/tests/test_derived_service.py:134:    monkeypatch.setattr(ds, "save_decision", fake_save_decision)
ATT/tests/test_derived_service.py:141:    result = ds.save_decision_from_canonical_payload(
ATT/tests/test_derived_service.py:142:        decision=payload,
ATT/tests/test_derived_service.py:151:    assert captured["decision"]["meta"]["origin"] == "test"
ATT/tests/test_derived_service.py:152:    assert captured["decision"]["meta"]["structure_id"] == 321
ATT/tests/test_derived_service.py:153:    assert captured["decision"]["meta"]["structure_name"] == "Fence"
ATT/tests/test_derived_service.py:154:    assert captured["decision"]["meta"]["underlying_asset"] == "VALE3"
ATT/tests/test_derived_service.py:155:    assert captured["decision"]["meta"]["storage_key"] == "structure:321"
ATT/tests/test_derived_service.py:159:def test_save_decision_preserva_structure_id_explicito_sem_alias(monkeypatch):
ATT/tests/test_derived_service.py:171:    def fake_insert_structure_decision(conn, timestamp, aba, decision_dict):
ATT/tests/test_derived_service.py:174:        captured["decision_dict"] = decision_dict
ATT/tests/test_derived_service.py:180:    monkeypatch.setattr(svc, "insert_structure_decision", fake_insert_structure_decision)
ATT/tests/test_derived_service.py:182:    result = svc.save_decision(
ATT/tests/test_derived_service.py:184:        decision={
ATT/tests/test_derived_service.py:186:            "decision": "hold",
ATT/tests/test_derived_service.py:194:    assert captured["decision_dict"]["structure_id"] == 7
ATT/tests/test_derived_service.py:195:    assert captured["decision_dict"]["meta"]["structure_id"] == 7
ATT/tests/test_derived_service.py:196:    assert captured["decision_dict"]["meta"]["storage_key"] == "structure:7"
ATT/tests/test_import_rtd_links_to_option_quotes.py:11:SCRIPT_PATH = ROOT / "scripts" / "import_rtd_links_to_option_quotes.py"
ATT/tests/test_import_rtd_links_to_option_quotes.py:15:    "import_rtd_links_to_option_quotes",
ATT/tests/test_import_rtd_links_to_option_quotes.py:24:def create_rtd_option_quotes_schema(db_path: Path) -> None:
ATT/tests/test_import_rtd_links_to_option_quotes.py:30:            CREATE TABLE rtd_option_quotes (
ATT/tests/test_import_rtd_links_to_option_quotes.py:53:                source TEXT NOT NULL DEFAULT 'rtd_links',
ATT/tests/test_import_rtd_links_to_option_quotes.py:68:def write_rtd_links_csv(path: Path, rows: list[list[str]]) -> None:
ATT/tests/test_import_rtd_links_to_option_quotes.py:103:            FROM rtd_option_quotes
ATT/tests/test_import_rtd_links_to_option_quotes.py:116:        return conn.execute("SELECT COUNT(*) FROM rtd_option_quotes").fetchone()[0]
ATT/tests/test_import_rtd_links_to_option_quotes.py:144:    csv_path = tmp_path / "RTD_LINKS.csv"
ATT/tests/test_import_rtd_links_to_option_quotes.py:146:    write_rtd_links_csv(
ATT/tests/test_import_rtd_links_to_option_quotes.py:176:    assert record["source"] == "rtd_links"
ATT/tests/test_import_rtd_links_to_option_quotes.py:183:    csv_path = tmp_path / "RTD_LINKS.csv"
ATT/tests/test_import_rtd_links_to_option_quotes.py:185:    create_rtd_option_quotes_schema(db_path)
ATT/tests/test_import_rtd_links_to_option_quotes.py:187:    write_rtd_links_csv(
ATT/tests/test_import_rtd_links_to_option_quotes.py:211:    csv_path = tmp_path / "RTD_LINKS.csv"
ATT/tests/test_import_rtd_links_to_option_quotes.py:213:    create_rtd_option_quotes_schema(db_path)
ATT/tests/test_import_rtd_links_to_option_quotes.py:215:    write_rtd_links_csv(
ATT/tests/test_import_rtd_links_to_option_quotes.py:235:    write_rtd_links_csv(
ATT/tests/test_import_rtd_links_to_option_quotes.py:264:    assert option["source"] == "rtd_links"
ATT/tests/test_legacy_structure_legs_importer_integration.py:65:        CREATE TABLE rtd_analise_robo_legs (
ATT/tests/test_legacy_structure_legs_importer_integration.py:128:def _insert_legacy_rtd_leg(db_path):
ATT/tests/test_legacy_structure_legs_importer_integration.py:132:        INSERT INTO rtd_analise_robo_legs (
ATT/tests/test_legacy_structure_legs_importer_integration.py:139:            190.0, 1000, 'rtdleg190', '2026-06-20', 0.55
ATT/tests/test_legacy_structure_legs_importer_integration.py:175:    # Insere RTD e MANUAL no mesmo timestamp.
ATT/tests/test_legacy_structure_legs_importer_integration.py:177:    _insert_legacy_rtd_leg(db_path)
ATT/tests/test_legacy_structure_legs_importer_integration.py:226:    # Garante que a leg antiga foi substituida e que RTD nao foi usado
ATT/tests/test_legacy_structure_legs_importer_integration.py:229:    assert imported_leg["symbol"] != "RTDLEG190"
ATT/tests/test_legacy_structure_legs_reader.py:142:        CREATE TABLE rtd_analise_robo_legs (
ATT/tests/test_legacy_structure_legs_reader.py:160:def test_read_by_structure_id_integrates_structure_alias_with_rtd_legs(tmp_path):
ATT/tests/test_legacy_structure_legs_reader.py:180:        INSERT INTO rtd_analise_robo_legs
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:8:def _create_rtd_legs_table(conn):
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:11:        CREATE TABLE rtd_analise_robo_legs (
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:37:def _create_rtd_option_quotes_table(conn):
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:40:        CREATE TABLE rtd_option_quotes (
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:65:def _insert_base_rtd_leg(conn):
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:68:        INSERT INTO rtd_analise_robo_legs (
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:117:def test_get_rtd_option_quote_legs_enriches_base_rtd_leg_with_quote_cache(tmp_path):
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:121:        _create_rtd_legs_table(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:122:        _create_rtd_option_quotes_table(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:123:        _insert_base_rtd_leg(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:127:            INSERT INTO rtd_option_quotes (
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:166:                "rtd_option_quotes",
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:176:    legs = repo.get_rtd_option_quote_legs("BOVA11")
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:182:    # Identidade/composição vêm da leg estrutural RTD.
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:190:    # Cotação/greeks vêm do cache centralizado rtd_option_quotes.
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:191:    assert leg.source == "rtd_option_quotes"
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:207:def test_get_rtd_option_quote_legs_returns_empty_list_when_cache_table_is_missing(tmp_path):
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:211:        _create_rtd_legs_table(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:212:        _insert_base_rtd_leg(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:217:    assert repo.get_rtd_option_quote_legs("BOVA11") == []
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:220:def _insert_rtd_option_quote(
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:240:        INSERT INTO rtd_option_quotes (
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:279:            "rtd_option_quotes",
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:287:def test_get_rtd_option_quote_legs_ignores_orphan_quote_without_structural_leg(tmp_path):
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:291:        _create_rtd_legs_table(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:292:        _create_rtd_option_quotes_table(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:294:        _insert_rtd_option_quote(
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:308:    assert repo.get_rtd_option_quote_legs("BOVA11") == []
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:311:def test_get_rtd_option_quote_legs_uses_latest_quote_when_cache_has_duplicates(tmp_path):
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:315:        _create_rtd_legs_table(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:316:        _create_rtd_option_quotes_table(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:317:        _insert_base_rtd_leg(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:319:        _insert_rtd_option_quote(
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:334:        _insert_rtd_option_quote(
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:353:    legs = repo.get_rtd_option_quote_legs("BOVA11")
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:359:    assert leg.source == "rtd_option_quotes"
ATT/tests/test_market_snapshot_selector.py:16:    def __init__(self, *, manual=None, rtd_option_quotes=None, rtd=None):
ATT/tests/test_market_snapshot_selector.py:18:        self.rtd_option_quotes = rtd_option_quotes or []
ATT/tests/test_market_snapshot_selector.py:19:        self.rtd = rtd or []
ATT/tests/test_market_snapshot_selector.py:24:    def get_rtd_option_quote_legs(self, ref):
ATT/tests/test_market_snapshot_selector.py:25:        return self.rtd_option_quotes
ATT/tests/test_market_snapshot_selector.py:27:    def get_rtd_legs(self, ref):
ATT/tests/test_market_snapshot_selector.py:28:        return self.rtd
ATT/tests/test_market_snapshot_selector.py:31:def test_selector_prioritizes_rtd_option_quotes_over_legacy_rtd_when_no_manual_exists():
ATT/tests/test_market_snapshot_selector.py:32:    legacy_rtd_leg = _leg("BOVAE195", "rtd", 1.10)
ATT/tests/test_market_snapshot_selector.py:33:    quote_leg = _leg("BOVAE195", "rtd_option_quotes", 1.23)
ATT/tests/test_market_snapshot_selector.py:37:            rtd=[legacy_rtd_leg],
ATT/tests/test_market_snapshot_selector.py:38:            rtd_option_quotes=[quote_leg],
ATT/tests/test_market_snapshot_selector.py:45:    assert result.source == "rtd_option_quotes"
ATT/tests/test_market_snapshot_selector.py:50:def test_selector_keeps_manual_leg_ahead_of_rtd_option_quotes():
ATT/tests/test_market_snapshot_selector.py:52:    quote_leg = _leg("BOVAE195", "rtd_option_quotes", 1.23)
ATT/tests/test_market_snapshot_selector.py:53:    legacy_rtd_leg = _leg("BOVAE195", "rtd", 1.10)
ATT/tests/test_market_snapshot_selector.py:58:            rtd_option_quotes=[quote_leg],
ATT/tests/test_market_snapshot_selector.py:59:            rtd=[legacy_rtd_leg],
ATT/tests/test_orchestrator_run_methods.py:2:Testes para os métodos run_payoff e run_decision
ATT/tests/test_orchestrator_run_methods.py:16:    _request_to_payoff_dict,
ATT/tests/test_orchestrator_run_methods.py:17:    run_decision,
ATT/tests/test_orchestrator_run_methods.py:18:    run_payoff,
ATT/tests/test_orchestrator_run_methods.py:64:# Testes: _request_to_payoff_dict
ATT/tests/test_orchestrator_run_methods.py:71:        result = _request_to_payoff_dict(req)
ATT/tests/test_orchestrator_run_methods.py:76:        s = _request_to_payoff_dict(req)["structure"]
ATT/tests/test_orchestrator_run_methods.py:86:        legs = _request_to_payoff_dict(req)["structure"]["legs"]
ATT/tests/test_orchestrator_run_methods.py:93:        m = _request_to_payoff_dict(req)["market"]
ATT/tests/test_orchestrator_run_methods.py:100:        result = _request_to_payoff_dict(req, extra_meta=meta)
ATT/tests/test_orchestrator_run_methods.py:105:        result = _request_to_payoff_dict(req)
ATT/tests/test_orchestrator_run_methods.py:114:        result_legs = _request_to_payoff_dict(req)["structure"]["legs"]
ATT/tests/test_orchestrator_run_methods.py:120:# Testes: run_payoff
ATT/tests/test_orchestrator_run_methods.py:125:    @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input")
ATT/tests/test_orchestrator_run_methods.py:130:        result = run_payoff(req)
ATT/tests/test_orchestrator_run_methods.py:138:    @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input")
ATT/tests/test_orchestrator_run_methods.py:143:        run_payoff(req, low_pct=0.8, high_pct=1.2, step_pct=0.005)
ATT/tests/test_orchestrator_run_methods.py:150:    @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input")
ATT/tests/test_orchestrator_run_methods.py:155:        run_payoff(req, extra_meta={"tag": "ci"})
ATT/tests/test_orchestrator_run_methods.py:160:    @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input")
ATT/tests/test_orchestrator_run_methods.py:166:        result = run_payoff(req)
ATT/tests/test_orchestrator_run_methods.py:172:# Testes: run_decision
ATT/tests/test_orchestrator_run_methods.py:177:    @patch("services.calculation_orchestrator.compute_decision_from_contract")
ATT/tests/test_orchestrator_run_methods.py:179:        mock_decide.return_value = {"decision": "hold", "score": 0.7}
ATT/tests/test_orchestrator_run_methods.py:182:        result = run_decision(req, pl_atual=200.0, pl_max=500.0, dte_min=10)
ATT/tests/test_orchestrator_run_methods.py:189:        assert result == {"decision": "hold", "score": 0.7}
ATT/tests/test_orchestrator_run_methods.py:191:    @patch("services.calculation_orchestrator.compute_decision_from_contract")
ATT/tests/test_orchestrator_run_methods.py:192:    def test_payoff_dict_repassado(self, mock_decide):
ATT/tests/test_orchestrator_run_methods.py:195:        payoff = {"pl_max": 600.0, "points": [{"spot": 50, "pl": 0}]}
ATT/tests/test_orchestrator_run_methods.py:197:        run_decision(req, payoff=payoff, pl_max=600.0, pl_atual=100.0)
ATT/tests/test_orchestrator_run_methods.py:200:        assert kwargs["payoff"] == payoff
ATT/tests/test_orchestrator_run_methods.py:202:    @patch("services.calculation_orchestrator.compute_decision_from_contract")
ATT/tests/test_orchestrator_run_methods.py:207:        run_decision(req)
ATT/tests/test_orchestrator_run_methods.py:214:    @patch("services.calculation_orchestrator.compute_decision_from_contract")
ATT/tests/test_orchestrator_run_methods.py:219:        run_decision(req, pl_max=300.0)
ATT/tests/test_orchestrator_run_methods.py:224:    @patch("services.calculation_orchestrator.compute_decision_from_contract")
ATT/tests/test_orchestrator_run_methods.py:226:        expected = {"decision": "close", "reason": "dte_gate"}
ATT/tests/test_orchestrator_run_methods.py:230:        result = run_decision(req, pl_max=100.0, pl_atual=80.0, dte_min=2)
ATT/tests/test_orchestrator_run_methods.py:241:    Chama run_payoff sem mock.
ATT/tests/test_orchestrator_run_methods.py:245:    def test_sanidade_run_payoff_call_chain(self):
ATT/tests/test_orchestrator_run_methods.py:246:        pytest.importorskip("domain.payoff")
ATT/tests/test_orchestrator_run_methods.py:260:            result = run_payoff(req, low_pct=0.8, high_pct=1.2, step_pct=0.05)
ATT/tests/test_orchestrator_run_methods.py:261:            assert isinstance(result, dict), "run_payoff deve retornar dict"
ATT/tests/test_payoff_canonical.py:1:from domain.payoff import compute_payoff_from_canonical_input
ATT/tests/test_payoff_canonical.py:4:def test_compute_payoff_from_canonical_input_should_preserve_canonical_metadata():
ATT/tests/test_payoff_canonical.py:37:    result = compute_payoff_from_canonical_input(canonical_input)
ATT/tests/test_payoff_chart.py:1:# C:/users/eucal/projeto/ATT/tests/test_payoff_chart.py
ATT/tests/test_payoff_chart.py:3:Testes unitários para UI/components/payoff_chart.py
ATT/tests/test_payoff_chart.py:51:from UI.components.payoff_chart import (  # noqa: E402
ATT/tests/test_payoff_chart.py:65:    with patch("UI.components.payoff_chart.FigureCanvasTkAgg"), \
ATT/tests/test_payoff_chart.py:66:         patch("UI.components.payoff_chart.NavigationToolbar2Tk"), \
ATT/tests/test_payoff_chart.py:67:         patch("UI.components.payoff_chart.Figure") as MockFig, \
ATT/tests/test_payoff_chart.py:68:         patch("UI.components.payoff_chart.ttk.Frame.__init__", return_value=None), \
ATT/tests/test_payoff_chart.py:69:         patch("UI.components.payoff_chart.ttk.Frame.pack",     return_value=None), \
ATT/tests/test_payoff_chart.py:70:         patch("UI.components.payoff_chart.ttk.Frame.bind",     return_value=None):
ATT/tests/test_payoff_chart.py:85:        chart._last_decision_data  = {}
ATT/tests/test_payoff_chart.py:332:    def test_update_chart_saves_decision_data(self):
ATT/tests/test_payoff_chart.py:334:        dd  = {"structure_id": "collar_1", "decision": "BUY", "spot_ref": 100.0}
ATT/tests/test_payoff_chart.py:335:        self.chart.update_chart(pts, decision_data=dd)
ATT/tests/test_payoff_chart.py:336:        self.assertEqual(self.chart._last_decision_data["structure_id"], "collar_1")
ATT/tests/test_payoff_chart.py:352:        result = self.chart.update_chart(pts, decision_data={"spot_ref": 100.0})
ATT/tests/test_payoff_chart.py:357:        result = self.chart.update_chart(_linear_points(), decision_data={})
ATT/tests/test_payoff_chart.py:395:        dd  = {"structure_id": "strangle_X", "aba": "old_aba", "decision": "BUY"}
ATT/tests/test_payoff_chart.py:396:        self.chart.update_chart(pts, decision_data=dd)
ATT/tests/test_payoff_chart.py:402:        dd  = {"aba": "straddle_Y", "decision": "SELL"}
ATT/tests/test_payoff_chart.py:403:        self.chart.update_chart(pts, decision_data=dd)
ATT/tests/test_payoff_chart.py:427:    def test_update_chart_none_decision_data(self):
ATT/tests/test_payoff_chart.py:428:        result = self.chart.update_chart(_linear_points(), decision_data=None)
ATT/tests/test_payoff_pricing_engine.py:3:from services.payoff_pricing_engine import PayoffPricingEngine
ATT/tests/test_payoff_pricing_engine.py:6:def test_run_returns_payoff_based_metrics_and_valuation():
ATT/tests/test_payoff_pricing_engine.py:30:    assert result["engine"] == "payoff_pricing_engine"
ATT/tests/test_payoff_pricing_engine.py:41:    assert result["metrics"]["payoff_points"] == 101
ATT/tests/test_payoff_pricing_engine.py:51:    assert "payoff" in result
ATT/tests/test_payoff_pricing_engine.py:52:    assert len(result["payoff"]["points"]) == 101
ATT/tests/test_payoff_pricing_engine.py:80:    assert result["metrics"]["payoff_points"] == 101
ATT/tests/test_pricing_execution_persistence_service.py:220:            "payoff": {
ATT/tests/test_pricing_execution_persistence_service.py:223:            "decision": {
ATT/tests/test_pricing_execution_persistence_service.py:258:    assert call["payoff_json"] == {
ATT/tests/test_pricing_execution_persistence_service.py:261:    assert call["decision_json"] == {
ATT/tests/test_robo_legs_repository.py:25:        CREATE TABLE rtd_analise_robo_legs (
ATT/tests/test_robo_legs_repository.py:42:def test_get_legs_prefers_manual_over_rtd(tmp_path):
ATT/tests/test_robo_legs_repository.py:54:        INSERT INTO rtd_analise_robo_legs
ATT/tests/test_robo_legs_repository.py:72:def test_get_legs_falls_back_to_rtd_when_manual_empty(tmp_path):
ATT/tests/test_robo_legs_repository.py:79:        INSERT INTO rtd_analise_robo_legs
ATT/tests/test_robo_legs_repository.py:116:def test_list_timestamps_prefers_manual_then_rtd(tmp_path):
ATT/tests/test_robo_legs_repository.py:133:        INSERT INTO rtd_analise_robo_legs
ATT/tests/test_robo_legs_repository.py:158:        INSERT INTO rtd_analise_robo_legs
ATT/tests/test_robo_legs_status_repository.py:9:def test_latest_timestamps_returns_parsed_manual_and_rtd(tmp_path):
ATT/tests/test_robo_legs_status_repository.py:15:    conn.execute("CREATE TABLE rtd_analise_robo_legs (aba TEXT, timestamp TEXT)")
ATT/tests/test_robo_legs_status_repository.py:26:        "INSERT INTO rtd_analise_robo_legs (aba, timestamp) VALUES (?, ?)",
ATT/tests/test_robo_legs_status_repository.py:36:    manual_latest, rtd_latest = repo.latest_timestamps("TESTE")
ATT/tests/test_robo_legs_status_repository.py:39:    assert rtd_latest == datetime(2026, 5, 19, 10, 30, 0)
ATT/tests/test_robo_legs_status_repository.py:48:    conn.execute("CREATE TABLE rtd_analise_robo_legs (aba TEXT, timestamp TEXT)")
ATT/tests/test_robo_legs_status_repository.py:56:    manual_latest, rtd_latest = repo.latest_timestamps("INEXISTENTE")
ATT/tests/test_robo_legs_status_repository.py:59:    assert rtd_latest is None
ATT/tests/test_robo_legs_status_service.py:14:    def __init__(self, manual_latest=None, rtd_latest=None):
ATT/tests/test_robo_legs_status_service.py:16:        self._rtd_latest = rtd_latest
ATT/tests/test_robo_legs_status_service.py:21:        return self._manual_latest, self._rtd_latest
ATT/tests/test_robo_legs_status_service.py:31:        status_repo=DummyStatusRepo(manual_latest=None, rtd_latest=None),
ATT/tests/test_robo_legs_status_service.py:43:    assert result.rtd_latest_ts is None
ATT/tests/test_robo_legs_status_service.py:50:    rtd_latest = datetime(2026, 5, 19, 10, 1, 0)
ATT/tests/test_robo_legs_status_service.py:54:        status_repo=DummyStatusRepo(manual_latest=manual_latest, rtd_latest=rtd_latest),
ATT/tests/test_robo_legs_status_service.py:63:    assert result.rtd_latest_ts == rtd_latest
ATT/tests/test_robo_legs_status_service.py:68:def test_status_uses_rtd_when_manual_missing():
ATT/tests/test_robo_legs_status_service.py:69:    rtd_latest = datetime(2026, 5, 19, 10, 0, 0)
ATT/tests/test_robo_legs_status_service.py:73:        status_repo=DummyStatusRepo(manual_latest=None, rtd_latest=rtd_latest),
ATT/tests/test_robo_legs_status_service.py:79:    assert result.chosen_fonte == FonteType.RTD
ATT/tests/test_robo_legs_status_service.py:80:    assert result.chosen_ts == rtd_latest
ATT/tests/test_robo_legs_status_service.py:82:    assert result.rtd_latest_ts == rtd_latest
ATT/tests/test_robo_legs_status_service.py:92:        status_repo=DummyStatusRepo(manual_latest=manual_latest, rtd_latest=None),
ATT/tests/test_robo_legs_status_service.py:108:        status_repo=DummyStatusRepo(manual_latest=manual_latest, rtd_latest=None),
ATT/tests/test_robo_legs_status_service.py:123:        status_repo=DummyStatusRepo(manual_latest=manual_latest, rtd_latest=None),
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:46:                "source": "rtd_option_quotes",
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:51:def test_rtd_legacy_fallback_can_feed_pricing_payload_when_no_canonical_legs_exist():
ATT/tests/test_rtd_option_quotes_repository_contract.py:6:from repositories.rtd_option_quotes_repository import RtdOptionQuotesRepository
ATT/tests/test_rtd_option_quotes_repository_contract.py:13:            CREATE TABLE rtd_option_quotes (
ATT/tests/test_rtd_option_quotes_repository_contract.py:46:            INSERT INTO rtd_option_quotes (
ATT/tests/test_rtd_option_quotes_repository_contract.py:85:                "rtd_option_quotes",
ATT/tests/test_rtd_option_quotes_repository_contract.py:102:    assert quote["source"] == "rtd_option_quotes"
ATT/tests/test_rtd_option_quotes_repository_contract.py:122:            INSERT INTO rtd_option_quotes (
ATT/tests/test_rtd_option_quotes_repository_contract.py:142:                "rtd_option_quotes",
ATT/tests/test_rtd_option_quotes_repository_contract.py:177:            INSERT INTO rtd_option_quotes (
ATT/tests/test_rtd_option_quotes_repository_contract.py:188:            VALUES (?, ?, ?, ?, ?, ?, 'rtd_option_quotes', '2026-06-18 10:00:00', '2026-06-18 09:59:00')
ATT/tests/test_rtd_option_quotes_repository_contract.py:213:            INSERT INTO rtd_option_quotes (
ATT/tests/test_rtd_option_quotes_repository_contract.py:224:            VALUES (?, ?, ?, ?, ?, ?, 'rtd_option_quotes', '2026-06-18 10:00:00', '2026-06-18 09:59:00')
ATT/tests/test_run_derived_pipeline_rtd_integration.py:7:SCRIPT_PATH = ROOT / "scripts" / "run_derived_pipeline.py"
ATT/tests/test_run_derived_pipeline_rtd_integration.py:12:        "run_derived_pipeline_under_test",
ATT/tests/test_run_derived_pipeline_rtd_integration.py:21:def test_parse_rtd_pipeline_metrics_from_stdout():
ATT/tests/test_run_derived_pipeline_rtd_integration.py:25:Importação RTD wide CSV
ATT/tests/test_run_derived_pipeline_rtd_integration.py:34:    assert module._parse_rtd_pipeline_metrics(output) == {
ATT/tests/test_run_derived_pipeline_rtd_integration.py:42:def test_rtd_quotes_updated_count_sums_inserted_and_updated():
ATT/tests/test_run_derived_pipeline_rtd_integration.py:45:    assert module._rtd_quotes_updated_count({"inserted": 2, "updated": 5}) == 7
ATT/tests/test_run_derived_pipeline_rtd_integration.py:46:    assert module._rtd_quotes_updated_count({"inserted": None, "updated": 5}) == 5
ATT/tests/test_run_derived_pipeline_rtd_integration.py:47:    assert module._rtd_quotes_updated_count(None) == 0
ATT/tests/test_run_derived_pipeline_rtd_integration.py:50:def test_run_rtd_option_quotes_import_uses_csv_pipeline_without_excel_or_powershell(
ATT/tests/test_run_derived_pipeline_rtd_integration.py:61:    (scripts_dir / "run_rtd_option_quotes_pipeline.py").write_text(
ATT/tests/test_run_derived_pipeline_rtd_integration.py:62:        "# fake rtd csv pipeline\n",
ATT/tests/test_run_derived_pipeline_rtd_integration.py:65:    (dados_dir / "RTD_LINKS.csv").write_text(
ATT/tests/test_run_derived_pipeline_rtd_integration.py:89:    result = module._run_rtd_option_quotes_import(
ATT/tests/test_run_derived_pipeline_rtd_integration.py:91:        csv_path="dados/RTD_LINKS.csv",
ATT/tests/test_run_derived_pipeline_rtd_integration.py:104:    assert command[1].endswith("run_rtd_option_quotes_pipeline.py")
ATT/tests/test_run_derived_pipeline_rtd_integration.py:106:    assert "dados/RTD_LINKS.csv" in command
ATT/tests/test_run_derived_pipeline_rtd_integration.py:112:    assert "refresh_rtd_option_quotes_excel" not in command_text
ATT/tests/test_run_derived_pipeline_rtd_integration.py:113:    assert "lista_rtd.xlsm" not in command_text
ATT/tests/test_run_rtd_option_quotes_pipeline.py:11:    / "run_rtd_option_quotes_pipeline.py"
ATT/tests/test_run_rtd_option_quotes_pipeline.py:17:        "run_rtd_option_quotes_pipeline_under_test",
ATT/tests/test_run_rtd_option_quotes_pipeline.py:30:        csv_path="dados/RTD_LINKS.csv",
ATT/tests/test_run_rtd_option_quotes_pipeline.py:35:    assert command[1].endswith("import_rtd_option_quotes_wide_csv.py")
ATT/tests/test_run_rtd_option_quotes_pipeline.py:37:    assert "dados/RTD_LINKS.csv" in command
ATT/tests/test_run_rtd_option_quotes_pipeline.py:47:        csv_path="dados/RTD_LINKS.csv",
ATT/tests/test_run_rtd_option_quotes_pipeline.py:64:    assert command[1].endswith("audit_rtd_option_quotes.py")
ATT/tests/test_run_rtd_option_quotes_pipeline.py:98:        csv_path="dados/RTD_LINKS.csv",
ATT/tests/test_run_rtd_option_quotes_pipeline.py:104:    assert calls[0][1].endswith("import_rtd_option_quotes_wide_csv.py")
ATT/tests/test_run_rtd_option_quotes_pipeline.py:118:        csv_path="dados/RTD_LINKS.csv",
ATT/tests/test_run_rtd_option_quotes_pipeline.py:124:    assert calls[0][1].endswith("import_rtd_option_quotes_wide_csv.py")
ATT/tests/test_run_rtd_option_quotes_pipeline.py:125:    assert calls[1][1].endswith("audit_rtd_option_quotes.py")
ATT/tests/test_run_rtd_option_quotes_pipeline.py:139:        csv_path="dados/RTD_LINKS.csv",
ATT/tests/test_run_rtd_option_quotes_pipeline.py:146:    assert calls[0][1].endswith("import_rtd_option_quotes_wide_csv.py")
ATT/tests/test_run_rtd_option_quotes_pipeline.py:156:        if command[1].endswith("import_rtd_option_quotes_wide_csv.py"):
ATT/tests/test_run_rtd_option_quotes_pipeline.py:163:        csv_path="dados/RTD_LINKS.csv",
ATT/tests/test_structure_analysis_service.py:124:    assert "payoff" in result
ATT/tests/test_structure_analysis_service.py:125:    assert "decision" in result
ATT/tests/test_structure_analysis_service.py:134:    payoff = result["payoff"]
ATT/tests/test_structure_analysis_service.py:135:    assert payoff is not None
ATT/tests/test_structure_analysis_service.py:136:    assert payoff["pl_max"] == 10000.0
ATT/tests/test_structure_analysis_service.py:137:    assert payoff["spot_ref"] == 198.35
ATT/tests/test_structure_analysis_service.py:138:    assert "points" in payoff
ATT/tests/test_structure_analysis_service.py:139:    assert len(payoff["points"]) > 0
ATT/tests/test_structure_analysis_service.py:141:    decision = result["decision"]
ATT/tests/test_structure_analysis_service.py:142:    assert decision is not None
ATT/tests/test_structure_analysis_service.py:143:    assert decision["decision"] == "HOLD"
ATT/tests/test_structure_analysis_service.py:144:    assert decision["dte_min"] == 0
ATT/tests/test_structure_analysis_service.py:145:    assert "why" in decision
ATT/tests/test_structure_analysis_service.py:146:    assert "why_json" in decision
ATT/tests/test_structure_analysis_service.py:147:    assert isinstance(decision["why"], dict)
ATT/tests/test_structure_analysis_service.py:148:    assert "reasons" in decision["why"]
ATT/tests/test_structure_analysis_service.py:149:    assert "alternatives" in decision["why"]
ATT/tests/test_structure_analysis_service.py:166:    assert result["decision"]["dte_min"] == 9
ATT/tests/test_structure_analysis_service.py:169:def test_structure_analysis_service_analyze_returns_structured_decision_for_invalid_payoff():
ATT/tests/test_structure_analysis_service.py:179:    assert "payoff" in result
ATT/tests/test_structure_analysis_service.py:180:    assert "decision" in result
ATT/tests/test_structure_analysis_service.py:181:    assert result["decision"] is not None
ATT/tests/test_structure_analysis_service.py:182:    assert result["decision"]["decision"] == "HOLD"
ATT/tests/test_structure_analysis_service.py:183:    assert result["decision"]["level"] == 0
ATT/tests/test_structure_analysis_service.py:184:    assert result["decision"]["why"]["error"] == "payoff is required"
ATT/tests/test_structure_analysis_service.py:185:    assert "validation_errors" in result["decision"]["why"]
ATT/tests/test_structure_analysis_service.py:206:    decision = result["decision"]
ATT/tests/test_structure_analysis_service.py:208:    assert decision is not None
ATT/tests/test_structure_analysis_service.py:209:    assert "why" in decision
ATT/tests/test_structure_analysis_service.py:210:    assert decision["why"]["thresholds_used"] == thresholds
ATT/tests/test_structure_analysis_service.py:211:    assert decision["why"]["dte_gate"] == 10
ATT/tests/test_structure_analysis_service.py:227:        for alternative in result["decision"]["why"]["alternatives"]
ATT/tests/test_structure_analysis_service.py:262:def test_structure_analysis_service_passes_effective_dte_to_decision(monkeypatch):
ATT/tests/test_structure_analysis_service.py:273:    def fake_compute_payoff_from_canonical_input(canonical_input):
ATT/tests/test_structure_analysis_service.py:276:    def fake_compute_decision_from_payoff(
ATT/tests/test_structure_analysis_service.py:277:        payoff,
ATT/tests/test_structure_analysis_service.py:283:        captured["payoff"] = payoff
ATT/tests/test_structure_analysis_service.py:289:            "decision": "HOLD",
ATT/tests/test_structure_analysis_service.py:300:        "services.structure_analysis_service.compute_payoff_from_canonical_input",
ATT/tests/test_structure_analysis_service.py:301:        fake_compute_payoff_from_canonical_input,
ATT/tests/test_structure_analysis_service.py:304:        "services.structure_analysis_service.compute_decision_from_payoff",
ATT/tests/test_structure_analysis_service.py:305:        fake_compute_decision_from_payoff,
ATT/tests/test_structure_analysis_service.py:316:        "payoff": {"pl_max": 1.0, "spot_ref": 198.35, "points": []},
ATT/tests/test_structure_analysis_service.py:324:    assert result["decision"]["dte_min"] == 3
ATT/tests/test_structure_analysis_service.py:336:    def fake_compute_payoff_from_canonical_input(canonical_input):
ATT/tests/test_structure_analysis_service.py:339:    def fake_compute_decision_from_payoff(
ATT/tests/test_structure_analysis_service.py:340:        payoff,
ATT/tests/test_structure_analysis_service.py:347:            "decision": "HOLD",
ATT/tests/test_structure_analysis_service.py:358:        "services.structure_analysis_service.compute_payoff_from_canonical_input",
ATT/tests/test_structure_analysis_service.py:359:        fake_compute_payoff_from_canonical_input,
ATT/tests/test_structure_analysis_service.py:362:        "services.structure_analysis_service.compute_decision_from_payoff",
ATT/tests/test_structure_analysis_service.py:363:        fake_compute_decision_from_payoff,
ATT/tests/test_structure_analysis_service.py:370:    assert result["decision"]["dte_min"] == 0
ATT/tests/test_structure_analysis_service.py:384:    def fake_compute_payoff_from_canonical_input(canonical_input):
ATT/tests/test_structure_analysis_service.py:387:    def fake_compute_decision_from_payoff(
ATT/tests/test_structure_analysis_service.py:388:        payoff,
ATT/tests/test_structure_analysis_service.py:396:            "decision": "HOLD",
ATT/tests/test_structure_analysis_service.py:407:        "services.structure_analysis_service.compute_payoff_from_canonical_input",
ATT/tests/test_structure_analysis_service.py:408:        fake_compute_payoff_from_canonical_input,
ATT/tests/test_structure_analysis_service.py:411:        "services.structure_analysis_service.compute_decision_from_payoff",
ATT/tests/test_structure_analysis_service.py:412:        fake_compute_decision_from_payoff,
ATT/tests/test_structure_analysis_service.py:423:    assert result["decision"]["dte_min"] == 9
ATT/tests/test_structure_analysis_service.py:504:    def fake_compute_payoff_from_canonical_input(canonical_input):
ATT/tests/test_structure_analysis_service.py:507:    def fake_compute_decision_from_payoff(
ATT/tests/test_structure_analysis_service.py:508:        payoff,
ATT/tests/test_structure_analysis_service.py:516:            "decision": "HOLD",
ATT/tests/test_structure_analysis_service.py:523:        "services.structure_analysis_service.compute_payoff_from_canonical_input",
ATT/tests/test_structure_analysis_service.py:524:        fake_compute_payoff_from_canonical_input,
ATT/tests/test_structure_analysis_service.py:527:        "services.structure_analysis_service.compute_decision_from_payoff",
ATT/tests/test_structure_analysis_service.py:528:        fake_compute_decision_from_payoff,
ATT/tests/test_structure_analysis_service.py:550:    def fake_compute_payoff_from_canonical_input(canonical_input):
ATT/tests/test_structure_analysis_service.py:553:    def fake_compute_decision_from_payoff(
ATT/tests/test_structure_analysis_service.py:554:        payoff,
ATT/tests/test_structure_analysis_service.py:562:            "decision": "HOLD",
ATT/tests/test_structure_analysis_service.py:569:        "services.structure_analysis_service.compute_payoff_from_canonical_input",
ATT/tests/test_structure_analysis_service.py:570:        fake_compute_payoff_from_canonical_input,
ATT/tests/test_structure_analysis_service.py:573:        "services.structure_analysis_service.compute_decision_from_payoff",
ATT/tests/test_structure_analysis_service.py:574:        fake_compute_decision_from_payoff,
ATT/tests/test_structure_analysis_service.py:597:    def fake_compute_payoff_from_canonical_input(canonical_input):
ATT/tests/test_structure_analysis_service.py:600:    def fake_compute_decision_from_payoff(
ATT/tests/test_structure_analysis_service.py:601:        payoff,
ATT/tests/test_structure_analysis_service.py:608:            "decision": "HOLD",
ATT/tests/test_structure_analysis_service.py:615:        "services.structure_analysis_service.compute_payoff_from_canonical_input",
ATT/tests/test_structure_analysis_service.py:616:        fake_compute_payoff_from_canonical_input,
ATT/tests/test_structure_analysis_service.py:619:        "services.structure_analysis_service.compute_decision_from_payoff",
ATT/tests/test_structure_analysis_service.py:620:        fake_compute_decision_from_payoff,
ATT/tests/test_structure_leg_rtd_enrichment_service.py:3:from services.structure_leg_rtd_enrichment_service import (
ATT/tests/test_structure_leg_rtd_enrichment_service.py:18:def test_enrich_leg_from_symbol_uses_rtd_quote_and_returns_canonical_leg():
ATT/tests/test_structure_leg_rtd_enrichment_service.py:108:def test_enrich_leg_raises_value_error_when_rtd_quote_is_not_found():
ATT/tests/test_structure_leg_rtd_enrichment_service.py:123:def test_enrich_leg_raises_value_error_when_rtd_quote_has_missing_required_fields():
ATT/tests/test_structure_leg_rtd_enrichment_service.py:137:    with pytest.raises(ValueError, match="missing required RTD field"):
ATT/tests/test_system_snapshots_repository.py:120:        payoff_json={"max_gain": 1000},
ATT/tests/test_system_snapshots_repository.py:121:        decision_json={"action": "hold"},
ATT/tests/test_system_snapshots_repository.py:167:    assert snapshot["payoff_json"] == {"max_gain": 1000}
ATT/tests/test_system_snapshots_repository.py:168:    assert snapshot["decision_json"] == {"action": "hold"}
ATT/tests/test_system_snapshots_schema.py:68:        "payoff_json",
ATT/tests/test_system_snapshots_schema.py:69:        "decision_json",
ATT/tests/test_ui_data_migration.py:27:def decisions(model):
ATT/tests/test_ui_data_migration.py:28:    return model.get_decisions()
ATT/tests/test_ui_data_migration.py:46:def non_empty_decisions(decisions):
ATT/tests/test_ui_data_migration.py:47:    if not decisions:
ATT/tests/test_ui_data_migration.py:49:    return decisions
ATT/tests/test_ui_data_migration.py:86:# Nível 2 -- get_decisions() com structure_id
ATT/tests/test_ui_data_migration.py:89:def test_decisions_nao_vazia(non_empty_decisions):
ATT/tests/test_ui_data_migration.py:90:    assert len(non_empty_decisions) > 0, "Deve haver ao menos uma decisão no banco"
ATT/tests/test_ui_data_migration.py:93:def test_decisions_tem_structure_id(decisions):
ATT/tests/test_ui_data_migration.py:94:    for d in decisions:
ATT/tests/test_ui_data_migration.py:98:def test_decisions_tem_aba(decisions):
ATT/tests/test_ui_data_migration.py:99:    for d in decisions:
ATT/tests/test_ui_data_migration.py:103:def test_structure_id_igual_a_aba(decisions):
ATT/tests/test_ui_data_migration.py:108:    for d in decisions:
ATT/tests/test_ui_data_migration.py:120:def test_decisions_tem_timestamp(decisions):
ATT/tests/test_ui_data_migration.py:121:    for d in decisions:
ATT/tests/test_ui_data_migration.py:137:    filtered = model.get_decisions(filters={"structure_id": sid_str})
ATT/tests/test_ui_data_migration.py:146:def test_filtro_por_aba_continuidade(model, decisions):
ATT/tests/test_ui_data_migration.py:152:    if not decisions:
ATT/tests/test_ui_data_migration.py:154:    aba_real = decisions[0]["aba"]        # ex: 'SBSP3'
ATT/tests/test_ui_data_migration.py:155:    filtered_aba = model.get_decisions(filters={"aba": aba_real})
ATT/tests/test_ui_data_migration.py:167:# Nível 4 -- get_payoff_curve_info()
ATT/tests/test_ui_data_migration.py:170:def test_payoff_curve_info_retorna_dados(model, non_empty_decisions):
ATT/tests/test_ui_data_migration.py:171:    d0 = non_empty_decisions[0]
ATT/tests/test_ui_data_migration.py:172:    pts, info = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"])
ATT/tests/test_ui_data_migration.py:173:    assert isinstance(pts, list), "Pontos do payoff devem ser uma lista"
ATT/tests/test_ui_data_migration.py:174:    assert isinstance(info, dict), "info do payoff deve ser dict"
ATT/tests/test_ui_data_migration.py:177:def test_payoff_curve_info_tem_structure_id(model, non_empty_decisions):
ATT/tests/test_ui_data_migration.py:178:    d0 = non_empty_decisions[0]
ATT/tests/test_ui_data_migration.py:179:    _, info = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"])
ATT/tests/test_ui_data_migration.py:180:    assert "structure_id" in info, "info do payoff deve conter 'structure_id'"
ATT/tests/test_ui_data_migration.py:183:def test_payoff_curve_info_aba_continuidade(model, non_empty_decisions):
ATT/tests/test_ui_data_migration.py:184:    d0 = non_empty_decisions[0]
ATT/tests/test_ui_data_migration.py:185:    _, info = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"])
ATT/tests/test_ui_data_migration.py:186:    assert "aba" in info, "info do payoff deve ainda conter 'aba' (continuidade)"
ATT/tests/test_ui_data_migration.py:192:def test_payoff_curve_info_pontos_validos(model, non_empty_decisions):
ATT/tests/test_ui_data_migration.py:193:    d0 = non_empty_decisions[0]
ATT/tests/test_ui_data_migration.py:194:    pts, _ = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"])

## Candidatos de resumo e contadores

UI/components/details_panel.py:315:                "created_at": 97,
UI/components/details_panel.py:316:                "updated_at": 96,
UI/components/details_panel.py:332:            if "created" in low:
UI/components/details_panel.py:334:            if "updated" in low:
UI/components/details_panel.py:368:                ignored = {str(c).lower() for c in structure_cols}
UI/components/details_panel.py:369:                ignored.update(
UI/components/details_panel.py:378:                ts_cols = [c for c in cols if str(c).lower() not in ignored]
UI/components/details_panel.py:568:        self.operational_cancelled_ignored_label = ttk.Label(
UI/components/details_panel.py:571:        self.operational_cancelled_ignored_label.grid(
UI/components/details_panel.py:617:        self.created_at_label = ttk.Label(
UI/components/details_panel.py:620:        self.created_at_label.grid(row=0, column=3, sticky="ew")
UI/components/details_panel.py:689:        self.created_at_label.config(text="N/A")
UI/components/details_panel.py:716:        created_at = info.get("created_at")
UI/components/details_panel.py:717:        self.created_at_label.config(text=created_at if created_at else "N/A")
UI/components/details_panel.py:725:            self.breakevens_label, self.source_label, self.created_at_label,
UI/components/details_panel.py:727:            self.operational_cancelled_ignored_label,
UI/components/details_panel.py:758:            "operational_cancelled_ignored_label",
UI/components/details_panel.py:774:                "events_ignored_cancelled": int,
UI/components/details_panel.py:782:        - ignored_events.
UI/components/details_panel.py:796:        ignored = state.get("events_ignored_cancelled")
UI/components/details_panel.py:797:        if ignored is None and isinstance(effective_structure.get("ignored_events"), list):
UI/components/details_panel.py:798:            ignored = len(effective_structure.get("ignored_events") or [])
UI/components/details_panel.py:812:        self.operational_cancelled_ignored_label.config(
UI/components/details_panel.py:813:            text=str(ignored) if ignored is not None else "N/A"
UI/components/details_panel.py:894:                "spot_ref", "meta_json", "created_at", "why_json",
UI/components/details_panel.py:902:                ORDER BY COALESCE(created_at, timestamp) DESC
UI/components/details_panel.py:961:                SELECT created_at, timestamp
UI/components/details_panel.py:964:                ORDER BY COALESCE(created_at, timestamp) DESC
UI/components/details_panel.py:970:            created_at = None
UI/components/details_panel.py:972:                created_at = row["created_at"] or row["timestamp"]
UI/components/details_panel.py:981:                "created_at": created_at,
UI/components/structures_list_panel.py:293:                 if k not in ("id", "structure_id", "created_at", "updated_at")}
UI/components/structure_editor_dialog.py:499:            errors="replace",
UI/components/structure_editor_dialog.py:776:                        locals().get("created_structure_id")
UI/components/structure_editor_dialog.py:781:                        or locals().get("created_id")
UI/main_window.py:284:    def refresh_data(self, show_errors: bool = True):
UI/main_window.py:347:            if show_errors:
UI/main_window.py:418:            self.refresh_data(show_errors=False)
UI/main_window.py:561:    def _extract_pipeline_summary(self, stdout: str) -> Dict:
UI/main_window.py:562:        """Extrai o resumo JSON emitido por scripts/run_derived_pipeline.py."""
UI/main_window.py:577:        """Formata valores do resumo operacional para exibição."""
UI/main_window.py:584:        summary = self._extract_pipeline_summary(stdout)
UI/main_window.py:586:        if not summary:
UI/main_window.py:596:            f"- Estruturas: {self._format_pipeline_value(summary.get('structures'))}",
UI/main_window.py:597:            f"- Decisões: {self._format_pipeline_value(summary.get('decisions'))}",
UI/main_window.py:598:            f"- Pontos de payoff: {self._format_pipeline_value(summary.get('payoff_points'))}",
UI/main_window.py:599:            f"- Resumos de payoff: {self._format_pipeline_value(summary.get('payoff_summaries'))}",
UI/main_window.py:600:            f"- Execuções de pricing: {self._format_pipeline_value(summary.get('pricing_executions'))}",
UI/main_window.py:601:            f"- Cotações RTD atualizadas: {self._format_pipeline_value(summary.get('rtd_quotes_updated'))}",
UI/main_window.py:602:            f"- Avisos: {self._format_pipeline_value(summary.get('warnings'))}",
UI/main_window.py:603:            f"- Erros: {self._format_pipeline_value(summary.get('errors'))}",
UI/main_window.py:609:        summary = self._extract_pipeline_summary(stdout)
UI/main_window.py:610:        if not summary:
UI/main_window.py:613:        decisions = self._format_pipeline_value(summary.get("decisions"))
UI/main_window.py:614:        payoff_points = self._format_pipeline_value(summary.get("payoff_points"))
UI/main_window.py:615:        errors = self._format_pipeline_value(summary.get("errors"))
UI/main_window.py:619:            f"pontos_payoff={payoff_points}; erros={errors}"
UI/main_window.py:850:                f"Criado em  : {str(structure.get('created_at', ''))[:19]}",
UI/main_window.py:851:                f"Atualizado : {str(structure.get('updated_at', ''))[:19]}",
UI/models/ui_data.py:520:                "created_at": None,
UI/models/ui_data.py:528:                    extra_cols = ", meta_json, created_at"
UI/models/ui_data.py:555:                    info["created_at"] = rows[0]["created_at"]
scripts/apply_fase9_atomic_create.py:85:                    status, notes, created_at, updated_at
scripts/apply_fase9_atomic_create.py:108:                    "created_at": now,
scripts/apply_fase9_atomic_create.py:109:                    "updated_at": now,
scripts/apply_fase9_atomic_create.py:119:                        multiplier, leg_order, notes, created_at, updated_at
scripts/audit_rtd_option_quotes.py:43:    "updated_at",
scripts/audit_rtd_option_quotes.py:44:    "created_at",
scripts/audit_rtd_option_quotes.py:86:        "errors": [],
scripts/audit_rtd_option_quotes.py:87:        "warnings": [],
scripts/audit_rtd_option_quotes.py:95:        result["errors"].append("database file not found")
scripts/audit_rtd_option_quotes.py:101:            result["errors"].append(f"table not found: {TABLE_NAME}")
scripts/audit_rtd_option_quotes.py:113:            result["errors"].append(
scripts/audit_rtd_option_quotes.py:123:            result["warnings"].append("table is empty")
scripts/audit_rtd_option_quotes.py:175:                result["errors"].append(
scripts/audit_rtd_option_quotes.py:180:                result["errors"].append(
scripts/audit_rtd_option_quotes.py:184:        if "updated_at" in column_set and max_age_minutes > 0:
scripts/audit_rtd_option_quotes.py:191:                    WHERE updated_at IS NOT NULL
scripts/audit_rtd_option_quotes.py:192:                      AND datetime(updated_at) < datetime('now', 'localtime', ?)
scripts/audit_rtd_option_quotes.py:203:                result["warnings"].append(
scripts/audit_rtd_option_quotes.py:207:    if result["errors"]:
scripts/audit_rtd_option_quotes.py:209:    elif result["warnings"]:
scripts/audit_rtd_option_quotes.py:237:    warnings = result.get("warnings") or []
scripts/audit_rtd_option_quotes.py:238:    if warnings:
scripts/audit_rtd_option_quotes.py:241:        for warning in warnings:
scripts/audit_rtd_option_quotes.py:244:    errors = result.get("errors") or []
scripts/audit_rtd_option_quotes.py:245:    if errors:
scripts/audit_rtd_option_quotes.py:248:        for error in errors:
scripts/audit_rtd_option_quotes.py:265:        help="Idade máxima esperada para updated_at. Use 0 para desabilitar.",
scripts/audit_rtd_option_quotes.py:275:        help="Retorna exit code 1 também quando houver avisos.",
scripts/dev/close_phase_5f_ui_pipeline.sh:9:# Fase 5F - Validacao da UI do resumo do pipeline
scripts/dev/close_phase_5f_ui_pipeline.sh:13:Validar que a interface executa o pipeline e exibe corretamente o resumo operacional ao usuario.
scripts/dev/close_phase_5f_ui_pipeline.sh:95:    updated: 4
scripts/dev/close_phase_5f_ui_pipeline.sh:97:    updated_at: 2026-06-22 09:24:21
scripts/dev/close_phase_5f_ui_pipeline.sh:131:      "errors": 0,
scripts/dev/close_phase_5f_ui_pipeline.sh:136:        "errors": 0,
scripts/dev/close_phase_5f_ui_pipeline.sh:141:        "updated": 4,
scripts/dev/close_phase_5f_ui_pipeline.sh:142:        "warnings": 0
scripts/dev/close_phase_5f_ui_pipeline.sh:144:      "rtd_quotes_updated": 4,
scripts/dev/close_phase_5f_ui_pipeline.sh:151:      "warnings": 0
scripts/dev/close_phase_5f_ui_pipeline.sh:161:| Decisoes exibidas no resumo | OK |
scripts/dev/close_phase_5f_ui_pipeline.sh:162:| Pontos de payoff exibidos no resumo | OK |
scripts/dev/close_phase_5f_ui_pipeline.sh:163:| Cotacoes RTD atualizadas exibidas no resumo | OK |
scripts/dev/close_phase_5f_ui_pipeline.sh:178:Isso nao bloqueia a Fase 5F, pois o objetivo desta validacao era confirmar que a interface exibe corretamente o resumo operacional principal do pipeline, incluindo:
scripts/dev/close_phase_5f_ui_pipeline.sh:183:- avisos;
scripts/dev/close_phase_5f_ui_pipeline.sh:184:- erros;
scripts/dev/close_phase_5f_ui_pipeline.sh:191:A UI confirma a execucao do pipeline, apresenta o resumo operacional esperado, reflete corretamente os dados persistidos no derived.db e mantem coerencia com a execucao em terminal.
scripts/dev/close_phase_6_integrated_validation.sh:23:- resumo operacional;
scripts/dev/close_phase_6_integrated_validation.sh:41:| Fase 5F | Validada | UI do resumo operacional do pipeline |
scripts/dev/close_phase_6_integrated_validation.sh:119:| Cotacoes RTD atualizadas exibidas no resumo | OK |
scripts/dev/close_phase_6_integrated_validation.sh:152:- ausencia de erros;
scripts/dev/close_phase_6_integrated_validation.sh:153:- ausencia de avisos;
scripts/dev/close_phase_6_integrated_validation.sh:163:O sistema confirma execucao operacional pela UI, persistencia em dados/derived.db, resumo operacional ao usuario, decisoes calculadas, curva de payoff disponivel e suite automatizada sem regressao.
scripts/dev/open_phase_6_integrated_validation.sh:25:- resumo operacional;
scripts/dev/open_phase_6_integrated_validation.sh:51:| Fase 5F | Validada | UI do resumo operacional do pipeline |
scripts/dev/open_phase_6_integrated_validation.sh:103:- Importacao RTD retorna sem erros
scripts/dev/open_phase_6_integrated_validation.sh:164:- o pipeline executar sem erros;
scripts/dev/open_phase_6_integrated_validation.sh:165:- a UI exibir o resumo operacional corretamente;
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:125:            for candidate in ["id", "created_at", "updated_at", "snapshot_id"]:
scripts/fase-3f-fix1-evidencia-final.sh:29:  echo "== Validação compute payoff V2 - resumo =="
scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:29:  grep -n "def main\|print\|run\|pipeline\|payoff\|decision\|summary\|count\|return" scripts/run_derived_pipeline.py || true
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:146:        order_col = "created_at" if "created_at" in app_struct_cols else "id"
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:149:            "id", "created_at", "updated_at", "name", "underlying_asset",
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:203:                if "created_at" in app_exec_cols:
scripts/fase-4-diagnostico-minimo-payoff-decisao.sh:206:                        select max(created_at) as v
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:143:            SELECT codigo_opcao, ativo_base, call_put, strike, ultimo_preco, bid, ask, source, updated_at, created_at
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:145:            ORDER BY updated_at DESC, id DESC
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:169:with p.open("r", encoding="utf-8-sig", errors="replace") as f:
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:120:                MIN(updated_at) AS min_updated_at,
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:121:                MAX(updated_at) AS max_updated_at
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:139:                updated_at
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:30:  echo "== Ocorrencias de rtd_quotes_updated =="
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:31:  grep -R "rtd_quotes_updated" -n . \
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:32:_RTD_METRIC_RE = re.compile(r"^\s*(input_rows|inserted|updated|skipped):\s*(-?\d+)\s*$")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:52:        "updated": 0,
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:67:def _rtd_quotes_updated_count(rtd_result: dict | None) -> int:
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:72:    return int(rtd_result.get("inserted") or 0) + int(rtd_result.get("updated") or 0)
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:96:            "errors": 1,
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:97:            "warnings": 0,
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:101:            "updated": 0,
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:108:            "errors": 1,
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:109:            "warnings": 0,
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:113:            "updated": 0,
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:147:        "errors": 0 if completed.returncode == 0 else 1,
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:148:        "warnings": 0,
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:157:    Placeholder: Gera payoff_curve_summary a partir de payoff_curve_points.
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:165:    """Lista tabelas do banco derived para resumo operacional."""
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:192:def _collect_pipeline_summary(rtd_result: dict | None = None) -> dict:
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:194:    Coleta resumo operacional do derived.db após execução/validação.
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:234:                "payoff_curve_summary",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:236:                "derived_payoff_summary",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:243:            "rtd_quotes_updated": _rtd_quotes_updated_count(rtd_result),
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:245:            "warnings": int((rtd_result or {}).get("warnings") or 0),
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:246:            "errors": int((rtd_result or {}).get("errors") or 0),
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:253:def _display_summary_value(value):
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:254:    """Formata valores do resumo operacional para stdout."""
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:293:            "errors": 0,
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:294:            "warnings": 1,
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:298:            "updated": 0,
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:313:            summary = _collect_pipeline_summary(rtd_result)
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:314:            print("[PIPELINE_SUMMARY_JSON] " + json.dumps(summary, ensure_ascii=False, sort_keys=True))
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:321:        summary = _collect_pipeline_summary(rtd_result)
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:322:        summary["errors"] = int(summary.get("errors") or 0) + 1
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:323:        print("[PIPELINE_SUMMARY_JSON] " + json.dumps(summary, ensure_ascii=False, sort_keys=True))
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:326:    summary = _collect_pipeline_summary(rtd_result)
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:329:    print(f"  Estruturas: {_display_summary_value(summary.get('structures'))}")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:330:    print(f"  Decisões: {_display_summary_value(summary.get('decisions'))}")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:331:    print(f"  Pontos de payoff: {_display_summary_value(summary.get('payoff_points'))}")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:332:    print(f"  Resumos de payoff: {_display_summary_value(summary.get('payoff_summaries'))}")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:333:    print(f"  Execuções de pricing: {_display_summary_value(summary.get('pricing_executions'))}")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:334:    print(f"  Cotações RTD atualizadas: {_display_summary_value(summary.get('rtd_quotes_updated'))}")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:335:    print(f"  Avisos: {_display_summary_value(summary.get('warnings'))}")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:336:    print(f"  Erros: {_display_summary_value(summary.get('errors'))}")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:337:    print("[PIPELINE_SUMMARY_JSON] " + json.dumps(summary, ensure_ascii=False, sort_keys=True))
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:379:updated: 3
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:381:updated_at: 2026-06-22 09:10:00
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:387:        "updated": 3,
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:392:def test_rtd_quotes_updated_count_sums_inserted_and_updated():
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:395:    assert module._rtd_quotes_updated_count({"inserted": 2, "updated": 5}) == 7
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:396:    assert module._rtd_quotes_updated_count({"inserted": None, "updated": 5}) == 5
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:397:    assert module._rtd_quotes_updated_count(None) == 0
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:433:            stdout="input_rows: 1\ninserted: 0\nupdated: 1\nskipped: 0\n",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:448:    assert result["updated"] == 1
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:75:                MIN(updated_at) AS min_updated_at,
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:76:                MAX(updated_at) AS max_updated_at
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:83:                   ultimo_preco, bid, ask, source, updated_at
scripts/fase5_automacao_gitbash.sh:19:CONTRATO_SCRIPT="$SCRIPTS_DIR/fase5_checar_resumo_pipeline.sh"
scripts/fase5_automacao_gitbash.sh:71:- se houve avisos;
scripts/fase5_automacao_gitbash.sh:72:- se houve erros;
scripts/fase5_automacao_gitbash.sh:99:- houve rejeições ou avisos não exibidos.
scripts/fase5_automacao_gitbash.sh:109:    Atualização executada, mas nenhum dado novo foi gerado.
scripts/fase5_automacao_gitbash.sh:123:7. Como erros são capturados.
scripts/fase5_automacao_gitbash.sh:124:8. Como avisos são tratados.
scripts/fase5_automacao_gitbash.sh:127:11. Se existe diferença entre sucesso com dados e sucesso sem dados novos.
scripts/fase5_automacao_gitbash.sh:131:## Informações mínimas esperadas no resumo
scripts/fase5_automacao_gitbash.sh:136:| Estruturas processadas | Quantidade de estruturas efetivamente processadas |
scripts/fase5_automacao_gitbash.sh:137:| Estruturas ignoradas | Quantidade de estruturas ignoradas |
scripts/fase5_automacao_gitbash.sh:141:| Avisos | Lista ou quantidade de avisos |
scripts/fase5_automacao_gitbash.sh:142:| Erros | Lista ou quantidade de erros |
scripts/fase5_automacao_gitbash.sh:143:| Status final | Sucesso, sucesso sem dados novos, aviso ou erro |
scripts/fase5_automacao_gitbash.sh:180:| Execução sem dados novos não mostra sucesso genérico | A validar |
scripts/fase5_automacao_gitbash.sh:195:4. Verificar se o pipeline retorna resumo estruturado.
scripts/fase5_automacao_gitbash.sh:197:6. Criar ou ajustar resumo de execução, se necessário.
scripts/fase5_automacao_gitbash.sh:199:8. Diferenciar sucesso com dados, sucesso sem dados novos, sucesso com avisos e erro.
scripts/fase5_automacao_gitbash.sh:304:- diagnóstico para identificar estruturas processadas, ignoradas ou rejeitadas.
scripts/fase5_automacao_gitbash.sh:394:  write_section "Candidatos de resumo e contadores"
scripts/fase5_automacao_gitbash.sh:395:  run_grep "summary|resumo|processed|processadas|ignored|ignoradas|created|generated|updated|warnings|avisos|errors|erros|nenhum dado novo|sem dados"
scripts/fase5_automacao_gitbash.sh:401:  echo "- Confirmar se existe resumo estruturado."
scripts/fase5_automacao_gitbash.sh:403:  echo "- Confirmar se sucesso sem dados novos é tratado diferente de sucesso com dados."
scripts/fase5_automacao_gitbash.sh:493:  check_term "Estruturas processadas" "structures_processed|estruturas_processadas|processed|processadas"
scripts/fase5_automacao_gitbash.sh:494:  check_term "Estruturas ignoradas" "structures_ignored|estruturas_ignoradas|ignored|ignoradas"
scripts/fase5_automacao_gitbash.sh:498:  check_term "Avisos" "warnings|avisos|warning"
scripts/fase5_automacao_gitbash.sh:499:  check_term "Erros" "errors|erros|exception|traceback"
scripts/fase5_automacao_gitbash.sh:500:  check_term "Sucesso sem dados novos" "nenhum dado novo|no new data|sem dados|nothing|zero"
scripts/fase5_automacao_gitbash.sh:506:  write_occurrences "Estruturas processadas" "structures_processed|estruturas_processadas|processed|processadas"
scripts/fase5_automacao_gitbash.sh:507:  write_occurrences "Estruturas ignoradas" "structures_ignored|estruturas_ignoradas|ignored|ignoradas"
scripts/fase5_automacao_gitbash.sh:511:  write_occurrences "Avisos" "warnings|avisos|warning"
scripts/fase5_automacao_gitbash.sh:512:  write_occurrences "Erros" "errors|erros|exception|traceback"
scripts/fase5_automacao_gitbash.sh:513:  write_occurrences "Sucesso sem dados novos" "nenhum dado novo|no new data|sem dados|nothing|zero"
scripts/fase5_automacao_gitbash.sh:521:  echo "- estruturas processadas;"
scripts/fase5_automacao_gitbash.sh:522:  echo "- estruturas ignoradas;"
scripts/fase5_automacao_gitbash.sh:526:  echo "- avisos;"
scripts/fase5_automacao_gitbash.sh:527:  echo "- erros;"
scripts/fase5_automacao_gitbash.sh:528:  echo "- execução sem dados novos."
scripts/fase5_buscar_fluxo_atualizar_dados.sh:65:  write_section "Candidatos de resumo e contadores"
scripts/fase5_buscar_fluxo_atualizar_dados.sh:66:  run_grep "summary|resumo|processed|processadas|ignored|ignoradas|created|generated|updated|warnings|avisos|errors|erros|nenhum dado novo|sem dados"
scripts/fase5_buscar_fluxo_atualizar_dados.sh:72:  echo "- Confirmar se existe resumo estruturado."
scripts/fase5_buscar_fluxo_atualizar_dados.sh:74:  echo "- Confirmar se sucesso sem dados novos é tratado diferente de sucesso com dados."
scripts/fase5_checar_resumo_pipeline.sh:84:  check_term "Estruturas processadas" "structures_processed|estruturas_processadas|processed|processadas"
scripts/fase5_checar_resumo_pipeline.sh:85:  check_term "Estruturas ignoradas" "structures_ignored|estruturas_ignoradas|ignored|ignoradas"
scripts/fase5_checar_resumo_pipeline.sh:89:  check_term "Avisos" "warnings|avisos|warning"
scripts/fase5_checar_resumo_pipeline.sh:90:  check_term "Erros" "errors|erros|exception|traceback"
scripts/fase5_checar_resumo_pipeline.sh:91:  check_term "Sucesso sem dados novos" "nenhum dado novo|no new data|sem dados|nothing|zero"
scripts/fase5_checar_resumo_pipeline.sh:97:  write_occurrences "Estruturas processadas" "structures_processed|estruturas_processadas|processed|processadas"
scripts/fase5_checar_resumo_pipeline.sh:98:  write_occurrences "Estruturas ignoradas" "structures_ignored|estruturas_ignoradas|ignored|ignoradas"
scripts/fase5_checar_resumo_pipeline.sh:102:  write_occurrences "Avisos" "warnings|avisos|warning"
scripts/fase5_checar_resumo_pipeline.sh:103:  write_occurrences "Erros" "errors|erros|exception|traceback"
scripts/fase5_checar_resumo_pipeline.sh:104:  write_occurrences "Sucesso sem dados novos" "nenhum dado novo|no new data|sem dados|nothing|zero"
scripts/fase5_checar_resumo_pipeline.sh:112:  echo "- estruturas processadas;"
scripts/fase5_checar_resumo_pipeline.sh:113:  echo "- estruturas ignoradas;"
scripts/fase5_checar_resumo_pipeline.sh:117:  echo "- avisos;"
scripts/fase5_checar_resumo_pipeline.sh:118:  echo "- erros;"
scripts/fase5_checar_resumo_pipeline.sh:119:  echo "- execução sem dados novos."
scripts/import_lista_rtd_excel_to_option_quotes.py:48:    "updated_at",
scripts/import_lista_rtd_excel_to_option_quotes.py:49:    "created_at",
scripts/import_lista_rtd_excel_to_option_quotes.py:451:        "updated": 0,
scripts/import_lista_rtd_excel_to_option_quotes.py:463:                stats["updated"] += 1
scripts/import_lista_rtd_excel_to_option_quotes.py:497:            "updated_at": now,
scripts/import_lista_rtd_excel_to_option_quotes.py:519:                   updated_at = :updated_at
scripts/import_lista_rtd_excel_to_option_quotes.py:526:            stats["updated"] += 1
scripts/import_lista_rtd_excel_to_option_quotes.py:530:        params_insert["created_at"] = now
scripts/import_lista_rtd_excel_to_option_quotes.py:552:                updated_at,
scripts/import_lista_rtd_excel_to_option_quotes.py:553:                created_at
scripts/import_lista_rtd_excel_to_option_quotes.py:573:                :updated_at,
scripts/import_lista_rtd_excel_to_option_quotes.py:574:                :created_at
scripts/import_lista_rtd_excel_to_option_quotes.py:653:        "errors": [],
scripts/import_lista_rtd_excel_to_option_quotes.py:689:        result["errors"].append(f"{type(exc).__name__}: {exc}")
scripts/import_lista_rtd_excel_to_option_quotes.py:696:            for error in result["errors"]:
scripts/import_rtd_links_to_option_quotes.py:78:    "updated_at",
scripts/import_rtd_links_to_option_quotes.py:85:    rows_ignored: int = 0
scripts/import_rtd_links_to_option_quotes.py:88:    updated: int = 0
scripts/import_rtd_links_to_option_quotes.py:175:    sample = csv_path.read_text(encoding="utf-8-sig", errors="replace")[:4096]
scripts/import_rtd_links_to_option_quotes.py:214:        "updated_at": None,
scripts/import_rtd_links_to_option_quotes.py:250:                stats.rows_ignored += 1
scripts/import_rtd_links_to_option_quotes.py:256:                stats.rows_ignored += 1
scripts/import_rtd_links_to_option_quotes.py:274:                stats.rows_ignored += 1
scripts/import_rtd_links_to_option_quotes.py:278:                current = record.get("updated_at")
scripts/import_rtd_links_to_option_quotes.py:280:                    record["updated_at"] = atualizado_em
scripts/import_rtd_links_to_option_quotes.py:287:        if not record.get("updated_at"):
scripts/import_rtd_links_to_option_quotes.py:288:            record["updated_at"] = now
scripts/import_rtd_links_to_option_quotes.py:339:        "updated_at = excluded.updated_at",
scripts/import_rtd_links_to_option_quotes.py:371:        stats.updated = sum(1 for code in codes if code in already_existing)
scripts/import_rtd_links_to_option_quotes.py:372:        stats.inserted = len(codes) - stats.updated
scripts/import_rtd_links_to_option_quotes.py:426:    print(f"Atualizados estimados: {stats.updated}")
scripts/import_rtd_links_to_option_quotes.py:427:    print(f"Registros ignorados: {stats.rows_ignored}")
scripts/import_rtd_option_quotes_wide_csv.py:147:    sample = Path(csv_path).read_text(encoding="utf-8-sig", errors="replace")[:4096]
scripts/import_rtd_option_quotes_wide_csv.py:213:    updated_at = now_text()
scripts/import_rtd_option_quotes_wide_csv.py:218:        "updated": 0,
scripts/import_rtd_option_quotes_wide_csv.py:220:        "updated_at": updated_at,
scripts/import_rtd_option_quotes_wide_csv.py:237:                "SELECT id, created_at FROM rtd_option_quotes WHERE codigo_opcao = ? ORDER BY id DESC LIMIT 1",
scripts/import_rtd_option_quotes_wide_csv.py:243:                "updated_at": updated_at,
scripts/import_rtd_option_quotes_wide_csv.py:247:                row_id, created_at = existing
scripts/import_rtd_option_quotes_wide_csv.py:269:                        updated_at = ?
scripts/import_rtd_option_quotes_wide_csv.py:289:                        payload["updated_at"],
scripts/import_rtd_option_quotes_wide_csv.py:294:                stats["updated"] += 1
scripts/import_rtd_option_quotes_wide_csv.py:317:                        updated_at,
scripts/import_rtd_option_quotes_wide_csv.py:318:                        created_at
scripts/import_rtd_option_quotes_wide_csv.py:340:                        payload["updated_at"],
scripts/import_rtd_option_quotes_wide_csv.py:341:                        payload["updated_at"],
scripts/mapear_automacao_opcoes_rtd.py:102:        return data.decode("utf-8", errors="replace")
scripts/mapear_automacao_opcoes_rtd.py:195:        "generated_at": datetime.now().isoformat(timespec="seconds"),
scripts/mapear_automacao_opcoes_rtd.py:213:        f"Gerado em: `{payload['generated_at']}`",
scripts/purge_derived_snapshots.py:14:    "payoff_curve_summary",
scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:78:        "errors": data.get("errors") if isinstance(data, dict) else None,
scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:88:        "errors": attempt["errors"],
scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:96:            "errors": [f"Script base não encontrado: {BASE_SCRIPT}"],
scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:110:            "errors": ["Falha ao executar tentativa visível."],
scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:143:        "errors": ["Tentativa invisível falhou e tentativa visível também não retornou JSON válido."],
scripts/run_derived_pipeline.py:24:_RTD_METRIC_RE = re.compile(r"^\s*(input_rows|inserted|updated|skipped):\s*(-?\d+)\s*$")
scripts/run_derived_pipeline.py:44:        "updated": 0,
scripts/run_derived_pipeline.py:59:def _rtd_quotes_updated_count(rtd_result: dict | None) -> int:
scripts/run_derived_pipeline.py:64:    return int(rtd_result.get("inserted") or 0) + int(rtd_result.get("updated") or 0)
scripts/run_derived_pipeline.py:88:            "errors": 1,
scripts/run_derived_pipeline.py:89:            "warnings": 0,
scripts/run_derived_pipeline.py:93:            "updated": 0,
scripts/run_derived_pipeline.py:100:            "errors": 1,
scripts/run_derived_pipeline.py:101:            "warnings": 0,
scripts/run_derived_pipeline.py:105:            "updated": 0,
scripts/run_derived_pipeline.py:139:        "errors": 0 if completed.returncode == 0 else 1,
scripts/run_derived_pipeline.py:140:        "warnings": 0,
scripts/run_derived_pipeline.py:149:    Placeholder: Gera payoff_curve_summary a partir de payoff_curve_points.
scripts/run_derived_pipeline.py:157:    """Lista tabelas do banco derived para resumo operacional."""
scripts/run_derived_pipeline.py:184:def _collect_pipeline_summary(rtd_result: dict | None = None) -> dict:
scripts/run_derived_pipeline.py:186:    Coleta resumo operacional do derived.db após execução/validação.
scripts/run_derived_pipeline.py:226:                "payoff_curve_summary",
scripts/run_derived_pipeline.py:228:                "derived_payoff_summary",
scripts/run_derived_pipeline.py:235:            "rtd_quotes_updated": _rtd_quotes_updated_count(rtd_result),
scripts/run_derived_pipeline.py:237:            "warnings": int((rtd_result or {}).get("warnings") or 0),
scripts/run_derived_pipeline.py:238:            "errors": int((rtd_result or {}).get("errors") or 0),
scripts/run_derived_pipeline.py:245:def _display_summary_value(value):
scripts/run_derived_pipeline.py:246:    """Formata valores do resumo operacional para stdout."""
scripts/run_derived_pipeline.py:285:            "errors": 0,
scripts/run_derived_pipeline.py:286:            "warnings": 1,
scripts/run_derived_pipeline.py:290:            "updated": 0,
scripts/run_derived_pipeline.py:305:            summary = _collect_pipeline_summary(rtd_result)
scripts/run_derived_pipeline.py:306:            print("[PIPELINE_SUMMARY_JSON] " + json.dumps(summary, ensure_ascii=False, sort_keys=True))
scripts/run_derived_pipeline.py:313:        summary = _collect_pipeline_summary(rtd_result)
scripts/run_derived_pipeline.py:314:        summary["errors"] = int(summary.get("errors") or 0) + 1
scripts/run_derived_pipeline.py:315:        print("[PIPELINE_SUMMARY_JSON] " + json.dumps(summary, ensure_ascii=False, sort_keys=True))
scripts/run_derived_pipeline.py:318:    summary = _collect_pipeline_summary(rtd_result)
scripts/run_derived_pipeline.py:321:    print(f"  Estruturas: {_display_summary_value(summary.get('structures'))}")
scripts/run_derived_pipeline.py:322:    print(f"  Decisões: {_display_summary_value(summary.get('decisions'))}")
scripts/run_derived_pipeline.py:323:    print(f"  Pontos de payoff: {_display_summary_value(summary.get('payoff_points'))}")
scripts/run_derived_pipeline.py:324:    print(f"  Resumos de payoff: {_display_summary_value(summary.get('payoff_summaries'))}")
scripts/run_derived_pipeline.py:325:    print(f"  Execuções de pricing: {_display_summary_value(summary.get('pricing_executions'))}")
scripts/run_derived_pipeline.py:326:    print(f"  Cotações RTD atualizadas: {_display_summary_value(summary.get('rtd_quotes_updated'))}")
scripts/run_derived_pipeline.py:327:    print(f"  Avisos: {_display_summary_value(summary.get('warnings'))}")
scripts/run_derived_pipeline.py:328:    print(f"  Erros: {_display_summary_value(summary.get('errors'))}")
scripts/run_derived_pipeline.py:329:    print("[PIPELINE_SUMMARY_JSON] " + json.dumps(summary, ensure_ascii=False, sort_keys=True))
scripts/run_lista_rtd_option_quotes_pipeline.py:95:        help="Idade máxima permitida para updated_at na auditoria. Padrão: 30.",
scripts/run_lista_rtd_option_quotes_pipeline.py:133:        "errors": [],
scripts/run_lista_rtd_option_quotes_pipeline.py:138:        result["errors"].append(f"script not found: {IMPORT_SCRIPT}")
scripts/run_lista_rtd_option_quotes_pipeline.py:142:        result["errors"].append(f"script not found: {AUDIT_SCRIPT}")
scripts/run_lista_rtd_option_quotes_pipeline.py:144:    if result["errors"]:
scripts/run_lista_rtd_option_quotes_pipeline.py:150:            for error in result["errors"]:
scripts/run_lista_rtd_option_quotes_pipeline.py:180:        result["errors"].append("import step failed")
scripts/run_lista_rtd_option_quotes_pipeline.py:199:            result["errors"].append("audit step failed")
scripts/run_lista_rtd_option_quotes_pipeline.py:248:        if result["errors"]:
scripts/run_lista_rtd_option_quotes_pipeline.py:251:            for error in result["errors"]:
scripts/run_rtd_option_quotes_pipeline.py:163:        help="Idade máxima esperada para updated_at na auditoria. Use 0 para desabilitar.",
scripts/run_rtd_refresh_full.py:20:            errors="replace",
scripts/run_rtd_refresh_full.py:42:                MAX(updated_at)
scripts/run_rtd_refresh_full.py:48:            "max_updated_at": row[1] if row else None,
scripts/run_rtd_refresh_full.py:53:            "max_updated_at": None,
scripts/run_rtd_refresh_full.py:67:        for line in p.read_text(encoding="utf-8", errors="replace").splitlines()
scripts/seed_current_rtd_option_quotes.py:15:- updated_at e created_at são preenchidos com o timestamp atual.
scripts/seed_current_rtd_option_quotes.py:164:                updated_at,
scripts/seed_current_rtd_option_quotes.py:165:                created_at
scripts/seed_current_rtd_option_quotes.py:185:                :updated_at,
scripts/seed_current_rtd_option_quotes.py:186:                :created_at
scripts/seed_current_rtd_option_quotes.py:217:                "updated_at": now,
scripts/seed_current_rtd_option_quotes.py:218:                "created_at": now,
scripts/verificar_andamento_rota.py:74:def git_summary() -> None:
scripts/verificar_andamento_rota.py:134:def document_summary() -> None:
scripts/verificar_andamento_rota.py:183:def search_summary() -> None:
scripts/verificar_andamento_rota.py:214:                    content = file_path.read_text(encoding="utf-8", errors="ignore")
scripts/verificar_andamento_rota.py:228:def database_summary() -> None:
scripts/verificar_andamento_rota.py:268:                    created_at
scripts/verificar_andamento_rota.py:283:                        f"created_at={row['created_at']}"
scripts/verificar_andamento_rota.py:296:                    MAX(created_at) AS ultima_execucao
scripts/verificar_andamento_rota.py:312:                print("(sem resumo disponível)")
scripts/verificar_andamento_rota.py:321:                for name in ["id", "name", "structure_name", "underlying_asset", "status", "created_at"]
scripts/verificar_andamento_rota.py:387:def test_summary(run_tests: bool) -> None:
scripts/verificar_andamento_rota.py:440:    git_summary()
scripts/verificar_andamento_rota.py:441:    document_summary()
scripts/verificar_andamento_rota.py:442:    search_summary()
scripts/verificar_andamento_rota.py:443:    database_summary()
scripts/verificar_andamento_rota.py:444:    test_summary(run_tests=args.run_tests)
repositories/market_snapshot_repository.py:82:        created_at
repositories/market_snapshot_repository.py:238:            quote_row["updated_at"],
repositories/market_snapshot_repository.py:239:            quote_row["created_at"],
repositories/market_snapshot_repository.py:257:      get_rtd_summary(aba)             -> dict com cabecalho RTD ou None
repositories/market_snapshot_repository.py:319:                updated_at,
repositories/market_snapshot_repository.py:320:                created_at
repositories/market_snapshot_repository.py:323:            ORDER BY updated_at DESC, created_at DESC
repositories/market_snapshot_repository.py:349:    def get_rtd_summary(self, ref: StructureRef | str) -> Optional[dict]:
repositories/market_snapshot_repository.py:376:            summary = self.get_rtd_summary(ref)
repositories/market_snapshot_repository.py:379:            summary = None
repositories/market_snapshot_repository.py:383:                _parse_br_float(summary[key])
repositories/market_snapshot_repository.py:384:                if summary and summary.get(key) is not None
repositories/market_snapshot_repository.py:402:            alertas_v2=summary.get("alertas_v2") if summary else None,
repositories/pricing_executions_repository.py:45:        created_at = datetime.now(UTC).isoformat().replace("+00:00", "Z")
repositories/pricing_executions_repository.py:59:                    created_at, structure_id, underlying_asset, reference_date,
repositories/pricing_executions_repository.py:66:                    created_at, structure_id, underlying_asset, reference_date,
repositories/pricing_executions_repository.py:79:            "created_at": created_at,
repositories/pricing_executions_repository.py:148:                ORDER BY created_at DESC
repositories/pricing_executions_repository.py:210:                ORDER BY created_at DESC
repositories/robo_legs_repository.py:197:            created_at=None,
repositories/robo_legs_repository.py:198:            updated_at=None,
repositories/rtd_option_quotes_repository.py:7:- erros sqlite3.OperationalError propagam;
repositories/rtd_option_quotes_repository.py:38:                COALESCE(updated_at, created_at, '') DESC,
repositories/structures_repository.py:201:                leg_order, notes, created_at, updated_at
repositories/structures_repository.py:316:                    status, notes, created_at, updated_at
repositories/structures_repository.py:333:                after={**payload, "id": new_id, "created_at": now, "updated_at": now},
repositories/structures_repository.py:370:                    status, notes, created_at, updated_at
repositories/structures_repository.py:393:                    "created_at": now,
repositories/structures_repository.py:394:                    "updated_at": now,
repositories/structures_repository.py:404:                        multiplier, leg_order, notes, created_at, updated_at
repositories/structures_repository.py:453:                   status, notes, created_at, updated_at
repositories/structures_repository.py:477:                       status, notes, created_at, updated_at
repositories/structures_repository.py:520:                    status=?, notes=?, updated_at=?
repositories/structures_repository.py:536:                after={**payload, "id": structure_id, "updated_at": now},
repositories/structures_repository.py:562:                "UPDATE structures SET status=?, updated_at=? WHERE id=?",
repositories/structures_repository.py:572:                after={**before_snap, "status": "archived", "updated_at": now},
repositories/structures_repository.py:599:                    multiplier, leg_order, notes, created_at, updated_at
repositories/structures_repository.py:612:                "UPDATE structures SET updated_at=? WHERE id=?",
repositories/structures_repository.py:653:                        multiplier, leg_order, notes, created_at, updated_at
repositories/structures_repository.py:665:                "UPDATE structures SET updated_at=? WHERE id=?",
repositories/structures_repository.py:714:                       status, notes, created_at, updated_at
repositories/structure_events_repository.py:212:                created_at     TEXT    NOT NULL,
repositories/structure_events_repository.py:213:                updated_at     TEXT    NOT NULL,
repositories/structure_events_repository.py:334:                    created_at,
repositories/structure_events_repository.py:335:                    updated_at
repositories/structure_events_repository.py:389:                    updated_at = ?
repositories/system_snapshots_repository.py:94:        created_at: str | None = None,
repositories/system_snapshots_repository.py:107:        created_at = created_at or _utc_now_iso()
repositories/system_snapshots_repository.py:114:                    created_at,
repositories/system_snapshots_repository.py:131:                    created_at,
repositories/system_snapshots_repository.py:258:                ORDER BY created_at DESC, id DESC
repositories/_aba_resolver_mixin.py:58:        Nunca propaga exceção: erros são logados e retornam None,
services/canonical_input_service.py:371:            "structure_events_ignored_cancelled": operational_state.get(
services/canonical_input_service.py:372:                "events_ignored_cancelled",
services/derived_service.py:464:            "spot_ref", "meta_json", "created_at",
services/legacy_structure_legs_importer.py:69:        Retorna resumo da importacao:
services/pricing_execution_app_service.py:53:        # propaga erros como ValueError para manter contrato com callers existentes
services/pricing_execution_app_service.py:85:    def get_latest_execution_summary(
services/pricing_execution_app_service.py:92:        return self.pricing_execution_query_service.get_latest_execution_summary(
services/pricing_execution_query_service.py:16:    def _validate_summary_filters(
services/pricing_execution_query_service.py:46:    def _load_executions_for_summary(
services/pricing_execution_query_service.py:83:        self._validate_summary_filters(
services/pricing_execution_query_service.py:90:        executions = self._load_executions_for_summary(
services/pricing_execution_query_service.py:107:            summary = {
services/pricing_execution_query_service.py:109:                "created_at": execution["created_at"],
services/pricing_execution_query_service.py:134:            if structure_id is not None and summary["structure_id"] != structure_id:
services/pricing_execution_query_service.py:138:                if str(summary["underlying_asset"]).upper() != underlying_asset.upper():
services/pricing_execution_query_service.py:141:            if status is not None and summary["execution_status"] != status:
services/pricing_execution_query_service.py:144:            if reference_date is not None and summary["reference_date"] != reference_date:
services/pricing_execution_query_service.py:147:            summaries.append(summary)
services/pricing_execution_query_service.py:162:        self._validate_summary_filters(
services/pricing_execution_query_service.py:200:    def get_latest_execution_summary(
services/pricing_execution_query_service.py:207:        self._validate_summary_filters(
services/robo_legs_service.py:55:                first = report.errors[0]
services/robo_legs_service.py:78:                first = report.errors[0]
services/structure_analysis_service.py:68:                "validation_errors": ["pl_max ausente ou zero"],
services/structure_events_service.py:338:        ignored_cancelled_count = 0
services/structure_events_service.py:344:                ignored_cancelled_count += 1
services/structure_events_service.py:389:            "events_ignored_cancelled": ignored_cancelled_count,
ATT/checks/check_legs.py:31:    return data.decode("latin-1", errors="replace"), "latin-1-replace"
ATT/tests/test_audit_rtd_option_quotes.py:52:                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
ATT/tests/test_audit_rtd_option_quotes.py:53:                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
ATT/tests/test_audit_rtd_option_quotes.py:63:    updated_at: str = "CURRENT_TIMESTAMP",
ATT/tests/test_audit_rtd_option_quotes.py:65:    if updated_at == "CURRENT_TIMESTAMP":
ATT/tests/test_audit_rtd_option_quotes.py:66:        updated_at_sql = "CURRENT_TIMESTAMP"
ATT/tests/test_audit_rtd_option_quotes.py:69:        updated_at_sql = "?"
ATT/tests/test_audit_rtd_option_quotes.py:70:        params = (codigo_opcao, updated_at)
ATT/tests/test_audit_rtd_option_quotes.py:83:                updated_at,
ATT/tests/test_audit_rtd_option_quotes.py:84:                created_at
ATT/tests/test_audit_rtd_option_quotes.py:86:            VALUES (?, 'PETR4', 'CALL', 30.0, 1.0, 1.1, 'rtd_links', {updated_at_sql}, CURRENT_TIMESTAMP)
ATT/tests/test_audit_rtd_option_quotes.py:98:    assert "database file not found" in result["errors"]
ATT/tests/test_audit_rtd_option_quotes.py:111:    assert "table not found: rtd_option_quotes" in result["errors"]
ATT/tests/test_audit_rtd_option_quotes.py:128:    assert result["errors"] == []
ATT/tests/test_audit_rtd_option_quotes.py:141:    assert "table is empty" in result["warnings"]
ATT/tests/test_audit_rtd_option_quotes.py:161:    assert result["errors"]
ATT/tests/test_audit_rtd_option_quotes.py:176:    assert "duplicated codigo_opcao groups: 1" in result["errors"]
ATT/tests/test_audit_rtd_option_quotes.py:184:    insert_quote(db_path, "PETRA300", updated_at="2000-01-01 00:00:00")
ATT/tests/test_audit_rtd_option_quotes.py:190:    assert "rows older than 30 minutes: 1" in result["warnings"]
ATT/tests/test_canonical_validators.py:30:    errors = validate_canonical_input(canonical_input)
ATT/tests/test_canonical_validators.py:32:    assert errors == []
ATT/tests/test_import_rtd_links_to_option_quotes.py:56:                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
ATT/tests/test_import_rtd_links_to_option_quotes.py:57:                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
ATT/tests/test_import_rtd_links_to_option_quotes.py:101:                updated_at,
ATT/tests/test_import_rtd_links_to_option_quotes.py:162:    assert stats.rows_ignored == 0
ATT/tests/test_import_rtd_links_to_option_quotes.py:177:    assert record["updated_at"] == "2026-06-06 17:50:00"
ATT/tests/test_import_rtd_links_to_option_quotes.py:205:    assert stats.updated == 0
ATT/tests/test_import_rtd_links_to_option_quotes.py:232:    assert first_stats.updated == 0
ATT/tests/test_import_rtd_links_to_option_quotes.py:252:    assert second_stats.updated == 1
ATT/tests/test_import_rtd_links_to_option_quotes.py:265:    assert option["updated_at"] == "2026-06-06 18:00:00"
ATT/tests/test_legacy_structure_legs_importer.py:21:            created_at TEXT,
ATT/tests/test_legacy_structure_legs_importer.py:22:            updated_at TEXT
ATT/tests/test_legacy_structure_legs_importer.py:40:            created_at TEXT NOT NULL,
ATT/tests/test_legacy_structure_legs_importer.py:41:            updated_at TEXT NOT NULL,
ATT/tests/test_legacy_structure_legs_importer.py:58:            status, notes, created_at, updated_at
ATT/tests/test_legacy_structure_legs_importer.py:76:            multiplier, leg_order, notes, created_at, updated_at
ATT/tests/test_legacy_structure_legs_importer_integration.py:24:            created_at TEXT,
ATT/tests/test_legacy_structure_legs_importer_integration.py:25:            updated_at TEXT
ATT/tests/test_legacy_structure_legs_importer_integration.py:43:            created_at TEXT NOT NULL,
ATT/tests/test_legacy_structure_legs_importer_integration.py:44:            updated_at TEXT NOT NULL,
ATT/tests/test_legacy_structure_legs_importer_integration.py:92:            status, notes, created_at, updated_at
ATT/tests/test_legacy_structure_legs_importer_integration.py:113:            multiplier, leg_order, notes, created_at, updated_at
ATT/tests/test_legacy_structure_legs_reader.py:87:def test_read_by_structure_id_propagates_mapper_errors():
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:58:            updated_at TEXT,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:59:            created_at TEXT
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:145:                updated_at,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:146:                created_at
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:236:    updated_at="2026-05-18 10:05:00",
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:258:            updated_at,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:259:            created_at
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:281:            updated_at,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:282:            updated_at,
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:301:            updated_at="2026-05-18 10:05:00",
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:331:            updated_at="2026-05-18 10:01:00",
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:346:            updated_at="2026-05-18 10:09:00",
ATT/tests/test_pricing_executions_repository.py:16:            created_at         TEXT    NOT NULL,
ATT/tests/test_pricing_executions_repository.py:75:    assert record["created_at"].endswith("Z")
ATT/tests/test_pricing_executions_repository.py:138:    # list_executions retorna ORDER BY created_at DESC; valida por conteúdo, não posição
ATT/tests/test_pricing_execution_app_service.py:26:    def get_latest_execution_summary(self, structure_id=None, underlying_asset=None,
ATT/tests/test_pricing_execution_app_service.py:28:        self.calls.append(("get_latest_execution_summary", {
ATT/tests/test_pricing_execution_app_service.py:136:def test_get_latest_execution_summary_delegates_to_query_service():
ATT/tests/test_pricing_execution_app_service.py:139:    result = service.get_latest_execution_summary(
ATT/tests/test_pricing_execution_app_service.py:144:    assert query_service.calls[0] == ("get_latest_execution_summary", {
ATT/tests/test_pricing_execution_controller.py:22:        self.get_latest_execution_summary_response = {"id": 2}
ATT/tests/test_pricing_execution_controller.py:27:        self.get_latest_execution_summary_exception = None
ATT/tests/test_pricing_execution_controller.py:70:    def get_latest_execution_summary(
ATT/tests/test_pricing_execution_controller.py:79:                "get_latest_execution_summary",
ATT/tests/test_pricing_execution_controller.py:88:        if self.get_latest_execution_summary_exception:
ATT/tests/test_pricing_execution_controller.py:89:            raise self.get_latest_execution_summary_exception
ATT/tests/test_pricing_execution_controller.py:90:        return self.get_latest_execution_summary_response
ATT/tests/test_pricing_execution_controller.py:236:    fake_service.get_latest_execution_summary_response = {"id": 5, "execution_status": "ok"}
ATT/tests/test_pricing_execution_controller.py:252:            "get_latest_execution_summary",
ATT/tests/test_pricing_execution_controller.py:264:def test_get_latest_pricing_execution_returns_404_when_no_summary_found():
ATT/tests/test_pricing_execution_controller.py:266:    fake_service.get_latest_execution_summary_exception = ValueError(
ATT/tests/test_pricing_execution_controller.py:281:    fake_service.get_latest_execution_summary_exception = ValueError(
ATT/tests/test_pricing_execution_query_service.py:36:        "created_at": f"2026-05-16T12:00:0{execution_id}Z",
ATT/tests/test_pricing_execution_query_service.py:319:def test_get_latest_execution_summary_returns_highest_id_after_filtering():
ATT/tests/test_pricing_execution_query_service.py:329:    latest = service.get_latest_execution_summary(status="ok")
ATT/tests/test_pricing_execution_query_service.py:335:def test_get_latest_execution_summary_raises_when_no_items_found():
ATT/tests/test_pricing_execution_query_service.py:341:        service.get_latest_execution_summary()
ATT/tests/test_rtd_option_quotes_repository_contract.py:32:                updated_at TEXT,
ATT/tests/test_rtd_option_quotes_repository_contract.py:33:                created_at TEXT
ATT/tests/test_rtd_option_quotes_repository_contract.py:64:                updated_at,
ATT/tests/test_rtd_option_quotes_repository_contract.py:65:                created_at
ATT/tests/test_rtd_option_quotes_repository_contract.py:103:    assert quote["updated_at"] == "2026-06-18 10:00:00"
ATT/tests/test_rtd_option_quotes_repository_contract.py:130:                updated_at,
ATT/tests/test_rtd_option_quotes_repository_contract.py:131:                created_at
ATT/tests/test_rtd_option_quotes_repository_contract.py:185:                updated_at,
ATT/tests/test_rtd_option_quotes_repository_contract.py:186:                created_at
ATT/tests/test_rtd_option_quotes_repository_contract.py:221:                updated_at,
ATT/tests/test_rtd_option_quotes_repository_contract.py:222:                created_at
ATT/tests/test_run_derived_pipeline_rtd_integration.py:29:updated: 3
ATT/tests/test_run_derived_pipeline_rtd_integration.py:31:updated_at: 2026-06-22 09:10:00
ATT/tests/test_run_derived_pipeline_rtd_integration.py:37:        "updated": 3,
ATT/tests/test_run_derived_pipeline_rtd_integration.py:42:def test_rtd_quotes_updated_count_sums_inserted_and_updated():
ATT/tests/test_run_derived_pipeline_rtd_integration.py:45:    assert module._rtd_quotes_updated_count({"inserted": 2, "updated": 5}) == 7
ATT/tests/test_run_derived_pipeline_rtd_integration.py:46:    assert module._rtd_quotes_updated_count({"inserted": None, "updated": 5}) == 5
ATT/tests/test_run_derived_pipeline_rtd_integration.py:47:    assert module._rtd_quotes_updated_count(None) == 0
ATT/tests/test_run_derived_pipeline_rtd_integration.py:83:            stdout="input_rows: 1\ninserted: 0\nupdated: 1\nskipped: 0\n",
ATT/tests/test_run_derived_pipeline_rtd_integration.py:98:    assert result["updated"] == 1
ATT/tests/test_structures_api.py:10:  - TestListStructures   : serialização dos campos do summary
ATT/tests/test_structures_api.py:36:    "created_at": "2026-06-01T00:00:00+00:00",
ATT/tests/test_structures_api.py:37:    "updated_at": "2026-06-01T00:00:00+00:00",
ATT/tests/test_structures_api.py:52:            "created_at": "2026-06-01T00:00:00+00:00",
ATT/tests/test_structures_api.py:53:            "updated_at": "2026-06-01T00:00:00+00:00",
ATT/tests/test_structures_api.py:266:    def test_campos_obrigatorios_no_summary(self, client):
ATT/tests/test_structures_api.py:270:        for campo in ("id", "name", "underlying_asset", "status", "created_at", "updated_at"):
ATT/tests/test_structures_api.py:271:            assert campo in item, f"campo ausente no summary: {campo}"
ATT/tests/test_structures_api.py:273:    def test_summary_nao_contem_legs(self, client):
ATT/tests/test_structures_api.py:340:        for campo in ("id", "name", "underlying_asset", "status", "legs", "created_at", "updated_at"):
ATT/tests/test_structures_archive_wiring.py:539:                " notes TEXT, created_at TEXT, updated_at TEXT)"
ATT/tests/test_structures_archive_wiring.py:547:                " notes TEXT, created_at TEXT, updated_at TEXT)"
ATT/tests/test_structures_archive_wiring.py:576:                " notes TEXT, created_at TEXT, updated_at TEXT)"
ATT/tests/test_structures_legs_endpoints.py:48:    "created_at":        "2026-01-01T00:00:00+00:00",
ATT/tests/test_structures_legs_endpoints.py:49:    "updated_at":        "2026-01-01T00:00:00+00:00",
ATT/tests/test_structure_analysis_service.py:185:    assert "validation_errors" in result["decision"]["why"]
ATT/tests/test_structure_events_api.py:17:    "created_at": "2026-01-01T00:00:00+00:00",
ATT/tests/test_structure_events_api.py:18:    "updated_at": "2026-01-01T00:00:00+00:00",
ATT/tests/test_structure_events_api.py:35:    "created_at": "2026-06-12T00:00:00Z",
ATT/tests/test_structure_events_api.py:36:    "updated_at": "2026-06-12T00:00:00Z",
ATT/tests/test_structure_events_api.py:56:    "ignored_events": [],
ATT/tests/test_structure_events_effective_state.py:104:def test_apply_events_cancelled_event_is_ignored():
ATT/tests/test_structure_events_effective_state.py:126:    assert result["operational_state"]["events_ignored_cancelled"] == 1
ATT/tests/test_structure_events_repository.py:95:    assert event["created_at"].endswith("Z")
ATT/tests/test_structure_events_repository.py:96:    assert event["updated_at"].endswith("Z")
ATT/tests/test_structure_events_service.py:8:        self.created = []
ATT/tests/test_structure_events_service.py:22:            "id": len(self.created) + 1,
ATT/tests/test_structure_events_service.py:25:        self.created.append(record)
ATT/tests/test_structure_events_service.py:115:    assert fake_repo.created == [record]
ATT/tests/test_system_snapshots_repository.py:21:            created_at,
ATT/tests/test_system_snapshots_repository.py:22:            updated_at
ATT/tests/test_system_snapshots_repository.py:61:            created_at,
ATT/tests/test_system_snapshots_repository.py:62:            updated_at
ATT/tests/test_system_snapshots_repository.py:112:        created_at="2026-06-12T15:00:00Z",
ATT/tests/test_system_snapshots_repository.py:181:def test_list_snapshots_for_structure_orders_by_created_at_desc(tmp_path: Path):
ATT/tests/test_system_snapshots_repository.py:192:        created_at="2026-06-12T10:00:00Z",
ATT/tests/test_system_snapshots_repository.py:197:        created_at="2026-06-12T11:00:00Z",
ATT/tests/test_system_snapshots_repository.py:219:        created_at="2026-06-12T10:00:00Z",
ATT/tests/test_system_snapshots_repository.py:225:        created_at="2026-06-12T11:00:00Z",
ATT/tests/test_system_snapshots_schema.py:59:        "created_at",
ATT/tests/test_system_snapshots_schema.py:76:        "idx_structure_snapshots_created_at",
ATT/tests/test_system_snapshots_schema.py:77:        "idx_structure_snapshots_structure_created",

## Próximos passos

- Confirmar qual ocorrência representa o botão real Atualizar Dados.
- Confirmar o handler chamado pelo clique.
- Confirmar o pipeline acionado.
- Confirmar se existe resumo estruturado.
- Confirmar se há contadores de RTD, payoff e decisões.
- Confirmar se sucesso sem dados novos é tratado diferente de sucesso com dados.
