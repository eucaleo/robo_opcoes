# FASE 5 — CANDIDATOS PRINCIPAIS DO FLUXO ATUALIZAR DADOS

## Botão e handlers

17:UI/components/details_panel.py:694:            self._refresh_operational_state_for_structure(structure_id)
18:UI/components/details_panel.py:854:    def _refresh_operational_state_for_structure(self, structure_id):
19:UI/components/details_panel.py:1023:    def _refresh_current_from_derived(self, structure_id):
20:UI/components/structure_editor_dialog.py:280:        self._refresh_leg_tree()
21:UI/components/structure_editor_dialog.py:286:    def _refresh_leg_tree(self):
22:UI/components/structure_editor_dialog.py:344:        self._refresh_leg_tree()
23:UI/components/structure_editor_dialog.py:367:        self._refresh_leg_tree()
24:UI/components/structure_editor_dialog.py:380:        self._refresh_leg_tree()
25:UI/components/structure_editor_dialog.py:434:                self._refresh_rtd_quote_for_symbol(symbol)
26:UI/components/structure_editor_dialog.py:446:    def _refresh_rtd_quote_for_symbol(self, symbol: str) -> None:
27:UI/components/structure_editor_dialog.py:459:        script = project_root / "scripts" / "refresh_rtd_symbol_to_option_quotes_fallback.py"
28:UI/components/structure_editor_dialog.py:474:            raise ValueError(f"Script de refresh RTD não encontrado: {script}")
29:UI/components/structure_editor_dialog.py:515:                "Não foi possível atualizar a cotação RTD para "
30:UI/components/structure_editor_dialog.py:586:            self._refresh_leg_tree()
31:UI/components/structure_editor_dialog.py:613:            self._refresh_leg_tree()
32:UI/main_window.py:49:        # Última decisão selecionada (preservada entre refreshes)
33:UI/main_window.py:58:        self._auto_refresh_interval_ms = 30000
34:UI/main_window.py:59:        self._auto_refresh_enabled = True
35:UI/main_window.py:60:        self._auto_refresh_in_progress = False
36:UI/main_window.py:61:        self._auto_refresh_after_id = None
37:UI/main_window.py:70:        self.refresh_data()
38:UI/main_window.py:73:        self.start_auto_refresh()
39:UI/main_window.py:143:        file_menu.add_command(label="Recarregar Tela", command=self.refresh_data)
40:UI/main_window.py:164:        self.root.bind("<F5>", lambda e: self.refresh_data())
42:UI/main_window.py:197:            print(f"[UI] Erro ao atualizar detalhes: {e}")
43:UI/main_window.py:284:    def refresh_data(self, show_errors: bool = True):
44:UI/main_window.py:290:            self.data_model.refresh()
45:UI/main_window.py:356:        self.stop_auto_refresh()
46:UI/main_window.py:362:    def start_auto_refresh(self):
47:UI/main_window.py:364:        self._auto_refresh_enabled = True
48:UI/main_window.py:365:        self._schedule_auto_refresh()
49:UI/main_window.py:367:    def stop_auto_refresh(self):
50:UI/main_window.py:369:        self._auto_refresh_enabled = False
51:UI/main_window.py:370:        after_id = getattr(self, "_auto_refresh_after_id", None)
52:UI/main_window.py:371:        self._auto_refresh_after_id = None
53:UI/main_window.py:379:    def _schedule_auto_refresh(self):
54:UI/main_window.py:382:            not getattr(self, "_auto_refresh_enabled", False)
55:UI/main_window.py:387:        previous_after_id = getattr(self, "_auto_refresh_after_id", None)
56:UI/main_window.py:394:        self._auto_refresh_after_id = self.root.after(
57:UI/main_window.py:395:            self._auto_refresh_interval_ms,
58:UI/main_window.py:396:            self._auto_refresh_tick,
59:UI/main_window.py:399:    def _auto_refresh_tick(self):
60:UI/main_window.py:401:        self._auto_refresh_after_id = None
61:UI/main_window.py:404:            not getattr(self, "_auto_refresh_enabled", False)
62:UI/main_window.py:410:            getattr(self, "_auto_refresh_in_progress", False)
63:UI/main_window.py:413:            self._schedule_auto_refresh()
64:UI/main_window.py:416:        self._auto_refresh_in_progress = True
65:UI/main_window.py:418:            self.refresh_data(show_errors=False)
66:UI/main_window.py:426:            self._auto_refresh_in_progress = False
67:UI/main_window.py:427:            self._schedule_auto_refresh()
68:UI/main_window.py:545:                self.root.after(0, self.refresh_data)
69:UI/main_window.py:665:            self.refresh_data()
70:UI/main_window.py:929:                        self.refresh_data()
71:UI/models/ui_data.py:202:    def refresh(self):
72:UI/models/ui_data.py:254:            self.refresh()
73:UI/models/ui_data.py:488:            self.refresh()
74:UI/models/ui_data.py:623:        self.refresh()
75:scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:267:- Toda fase encerrada deve atualizar evidencias em docs.
76:scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:4:EVID="docs/checkpoints/evidencias/fase-4-diagnostico-atualizar-dados-limpo.txt"
77:scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:25:  grep -n "Atualizar Dados\|Executar Pipeline\|def refresh_data\|def run_pipeline\|Pipeline executado\|status_bar.config" UI/main_window.py || true
78:scripts/fase-5-diagnostico-rtd.sh:27:  echo "== Busca por handlers Atualizar Dados / Pipeline =="
79:scripts/fase-5-diagnostico-rtd.sh:29:    -E "Atualizar Dados|refresh_data|run_pipeline|Executar Pipeline" UI scripts services db repositories domain . 2>/dev/null | head -300
80:scripts/fase-5-diagnostico-rtd.sh:132:  echo "== Trecho UI/main_window.py refresh_data e run_pipeline =="
81:scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:53:    scripts/run_rtd_refresh_full.py \
82:scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:55:    scripts/refresh_rtd_option_quotes_excel.ps1 \
83:scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:74:    scripts/run_rtd_refresh_full.py \
85:scripts/fase-5c-restaurar-rtd-historico.sh:16:  "scripts/refresh_rtd_option_quotes_excel.ps1"
86:scripts/fase-5c-restaurar-rtd-historico.sh:19:  "scripts/run_rtd_refresh_full.py"
87:scripts/fase-5c-restaurar-rtd-historico.sh:75:    scripts/run_rtd_refresh_full.py
88:scripts/fase-5c-restaurar-rtd-historico.sh:87:  if [ -f scripts/refresh_rtd_option_quotes_excel.ps1 ]; then
89:scripts/fase-5c-restaurar-rtd-historico.sh:88:    sed -n '1,220p' scripts/refresh_rtd_option_quotes_excel.ps1
90:scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:51:  grep -R "RTD\\|rtd\\|Atualizar Dados\\|Executar Pipeline" -n \
91:scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:62:  find ATT/tests -type f | grep -Ei "derived|pipeline|orchestrator|refresh|rtd" | sort
92:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:85:    - Não aciona Excel, PowerShell, COM ou refresh RTD ao vivo.
93:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:462:    assert "refresh_rtd_option_quotes_excel" not in command_text
94:scripts/fase-diagnostico-recalc-pipeline-inicializacao.sh:8:  echo "== Diagnóstico: recalc/pipeline em inicialização e refresh =="
95:scripts/fase-diagnostico-recalc-pipeline-inicializacao.sh:27:  echo "== Trecho UI/main_window.py: init/menu/bind/refresh/auto-refresh/recalc =="
96:scripts/fase5_automacao_gitbash.sh:18:BUSCA_SCRIPT="$SCRIPTS_DIR/fase5_buscar_fluxo_atualizar_dados.sh"
97:scripts/fase5_automacao_gitbash.sh:59:Auditar e melhorar o comportamento do botão Atualizar Dados, garantindo que a ação executada pelo usuário seja rastreável, compreensível e verificável.
98:scripts/fase5_automacao_gitbash.sh:89:O botão Atualizar Dados pode executar ações importantes do pipeline, mas o usuário pode não receber feedback suficiente sobre o resultado.
99:scripts/fase5_automacao_gitbash.sh:117:1. Onde está o botão Atualizar Dados.
100:scripts/fase5_automacao_gitbash.sh:153:    scripts/run_rtd_refresh_full.py
101:scripts/fase5_automacao_gitbash.sh:154:    scripts/refresh_rtd_option_quotes_excel.ps1
102:scripts/fase5_automacao_gitbash.sh:164:    scripts/refresh_rtd_symbol_to_option_quotes.py
103:scripts/fase5_automacao_gitbash.sh:172:| Botão Atualizar Dados localizado | A validar |
104:scripts/fase5_automacao_gitbash.sh:192:1. Localizar o botão Atualizar Dados na interface.
106:scripts/fase5_automacao_gitbash.sh:212:A prioridade inicial é diagnosticar o fluxo real do botão Atualizar Dados e confirmar quais pipelines ele aciona.
107:scripts/fase5_automacao_gitbash.sh:275:    Fase 5 — Atualizar Dados e Resumo do Pipeline
108:scripts/fase5_automacao_gitbash.sh:316:    Fase 5 — Atualizar Dados e Resumo do Pipeline
109:scripts/fase5_automacao_gitbash.sh:386:  run_grep "Atualizar Dados|atualizar dados|Atualizar|atualizar|Refresh|refresh"
110:scripts/fase5_automacao_gitbash.sh:389:  run_grep "clicked.connect|command=|on_click|callback|handler|handle|atualizar|refresh"
111:scripts/fase5_automacao_gitbash.sh:392:  run_grep "run_derived_pipeline|run_rtd_option_quotes_pipeline|run_rtd_refresh_full|payoff_curve_points|structure_decisions|RTD|rtd|payoff|decision|decisions"
112:scripts/fase5_automacao_gitbash.sh:398:  echo "- Confirmar qual ocorrência representa o botão real Atualizar Dados."
113:scripts/fase5_automacao_gitbash.sh:422:  "scripts/run_rtd_refresh_full.py"
114:scripts/fase5_automacao_gitbash.sh:518:  echo "A Fase 5 deve garantir que o botão Atualizar Dados tenha retorno claro para:"
115:scripts/fase5_automacao_gitbash.sh:558:  commit_if_needed "docs: fecha fase 4 e abre fase 5 atualizar dados"
116:scripts/fase5_automacao_gitbash.sh:571:  commit_if_needed "chore: adiciona verificadores fase 5 atualizar dados"
117:scripts/fase5_buscar_fluxo_atualizar_dados.sh:57:  run_grep "Atualizar Dados|atualizar dados|Atualizar|atualizar|Refresh|refresh"
118:scripts/fase5_buscar_fluxo_atualizar_dados.sh:60:  run_grep "clicked.connect|command=|on_click|callback|handler|handle|atualizar|refresh"
119:scripts/fase5_buscar_fluxo_atualizar_dados.sh:63:  run_grep "run_derived_pipeline|run_rtd_option_quotes_pipeline|run_rtd_refresh_full|payoff_curve_points|structure_decisions|RTD|rtd|payoff|decision|decisions"
120:scripts/fase5_buscar_fluxo_atualizar_dados.sh:69:  echo "- Confirmar qual ocorrência representa o botão real Atualizar Dados."
121:scripts/fase5_checar_resumo_pipeline.sh:13:  "scripts/run_rtd_refresh_full.py"
122:scripts/fase5_checar_resumo_pipeline.sh:109:  echo "A Fase 5 deve garantir que o botão Atualizar Dados tenha retorno claro para:"
123:scripts/import_lista_rtd_excel_to_option_quotes.py:220:    - aguarda RTD atualizar;
124:scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:10:BASE_SCRIPT = Path(__file__).resolve().with_name("refresh_rtd_symbol_to_option_quotes.py")
125:scripts/run_derived_pipeline.py:77:    - Não aciona Excel, PowerShell, COM ou refresh RTD ao vivo.
126:scripts/run_rtd_refresh_full.py:76:        description="Pipeline completo: gerar símbolos RTD, atualizar Excel/CSV e importar cotações no SQLite."
127:scripts/run_rtd_refresh_full.py:87:    parser.add_argument("--skip-excel", action="store_true", help="Pula o refresh do Excel e importa o CSV existente.")
128:scripts/run_rtd_refresh_full.py:101:    ps1_script = Path("scripts/refresh_rtd_option_quotes_excel.ps1")
129:scripts/run_rtd_refresh_full.py:103:    print("=== RTD Refresh Full ===")
130:scripts/run_rtd_refresh_full.py:241:            print("Pipeline interrompido no refresh Excel/RTD.")
131:scripts/run_rtd_refresh_full.py:245:        print("Refresh Excel/RTD pulado por --skip-excel.")
132:ATT/tests/test_run_derived_pipeline_rtd_integration.py:112:    assert "refresh_rtd_option_quotes_excel" not in command_text
133:ATT/tests/test_ui_data_migration.py:22:    m.refresh()
135:## Candidatos de handler
137:UI/components/decisions_grid.py:73:        v_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
138:UI/components/decisions_grid.py:74:        self.tree.configure(yscrollcommand=v_scrollbar.set)
139:UI/components/decisions_grid.py:76:        h_scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
140:UI/components/decisions_grid.py:77:        self.tree.configure(xscrollcommand=h_scrollbar.set)
141:UI/components/details_panel.py:628:            command=self._on_recalculate_click,

## Pipelines

25:UI/components/structure_editor_dialog.py:434:                self._refresh_rtd_quote_for_symbol(symbol)
26:UI/components/structure_editor_dialog.py:446:    def _refresh_rtd_quote_for_symbol(self, symbol: str) -> None:
27:UI/components/structure_editor_dialog.py:459:        script = project_root / "scripts" / "refresh_rtd_symbol_to_option_quotes_fallback.py"
28:UI/components/structure_editor_dialog.py:474:            raise ValueError(f"Script de refresh RTD não encontrado: {script}")
29:UI/components/structure_editor_dialog.py:515:                "Não foi possível atualizar a cotação RTD para "
75:scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:267:- Toda fase encerrada deve atualizar evidencias em docs.
78:scripts/fase-5-diagnostico-rtd.sh:27:  echo "== Busca por handlers Atualizar Dados / Pipeline =="
79:scripts/fase-5-diagnostico-rtd.sh:29:    -E "Atualizar Dados|refresh_data|run_pipeline|Executar Pipeline" UI scripts services db repositories domain . 2>/dev/null | head -300
80:scripts/fase-5-diagnostico-rtd.sh:132:  echo "== Trecho UI/main_window.py refresh_data e run_pipeline =="
81:scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:53:    scripts/run_rtd_refresh_full.py \
82:scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:55:    scripts/refresh_rtd_option_quotes_excel.ps1 \
83:scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:74:    scripts/run_rtd_refresh_full.py \
84:scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:180:    -E "Excel.Application|Workbooks|RefreshAll|RTD|LISTA_RTD|RTD_LINKS|win32com|powershell|Start-Process" \
85:scripts/fase-5c-restaurar-rtd-historico.sh:16:  "scripts/refresh_rtd_option_quotes_excel.ps1"
86:scripts/fase-5c-restaurar-rtd-historico.sh:19:  "scripts/run_rtd_refresh_full.py"
87:scripts/fase-5c-restaurar-rtd-historico.sh:75:    scripts/run_rtd_refresh_full.py
88:scripts/fase-5c-restaurar-rtd-historico.sh:87:  if [ -f scripts/refresh_rtd_option_quotes_excel.ps1 ]; then
89:scripts/fase-5c-restaurar-rtd-historico.sh:88:    sed -n '1,220p' scripts/refresh_rtd_option_quotes_excel.ps1
90:scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:51:  grep -R "RTD\\|rtd\\|Atualizar Dados\\|Executar Pipeline" -n \
91:scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:62:  find ATT/tests -type f | grep -Ei "derived|pipeline|orchestrator|refresh|rtd" | sort
92:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:85:    - Não aciona Excel, PowerShell, COM ou refresh RTD ao vivo.
93:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:462:    assert "refresh_rtd_option_quotes_excel" not in command_text
100:scripts/fase5_automacao_gitbash.sh:153:    scripts/run_rtd_refresh_full.py
101:scripts/fase5_automacao_gitbash.sh:154:    scripts/refresh_rtd_option_quotes_excel.ps1
102:scripts/fase5_automacao_gitbash.sh:164:    scripts/refresh_rtd_symbol_to_option_quotes.py
111:scripts/fase5_automacao_gitbash.sh:392:  run_grep "run_derived_pipeline|run_rtd_option_quotes_pipeline|run_rtd_refresh_full|payoff_curve_points|structure_decisions|RTD|rtd|payoff|decision|decisions"
113:scripts/fase5_automacao_gitbash.sh:422:  "scripts/run_rtd_refresh_full.py"
119:scripts/fase5_buscar_fluxo_atualizar_dados.sh:63:  run_grep "run_derived_pipeline|run_rtd_option_quotes_pipeline|run_rtd_refresh_full|payoff_curve_points|structure_decisions|RTD|rtd|payoff|decision|decisions"
121:scripts/fase5_checar_resumo_pipeline.sh:13:  "scripts/run_rtd_refresh_full.py"
123:scripts/import_lista_rtd_excel_to_option_quotes.py:220:    - aguarda RTD atualizar;
124:scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:10:BASE_SCRIPT = Path(__file__).resolve().with_name("refresh_rtd_symbol_to_option_quotes.py")
125:scripts/run_derived_pipeline.py:77:    - Não aciona Excel, PowerShell, COM ou refresh RTD ao vivo.
126:scripts/run_rtd_refresh_full.py:76:        description="Pipeline completo: gerar símbolos RTD, atualizar Excel/CSV e importar cotações no SQLite."
127:scripts/run_rtd_refresh_full.py:87:    parser.add_argument("--skip-excel", action="store_true", help="Pula o refresh do Excel e importa o CSV existente.")
128:scripts/run_rtd_refresh_full.py:101:    ps1_script = Path("scripts/refresh_rtd_option_quotes_excel.ps1")
129:scripts/run_rtd_refresh_full.py:103:    print("=== RTD Refresh Full ===")
130:scripts/run_rtd_refresh_full.py:241:            print("Pipeline interrompido no refresh Excel/RTD.")
131:scripts/run_rtd_refresh_full.py:245:        print("Refresh Excel/RTD pulado por --skip-excel.")
132:ATT/tests/test_run_derived_pipeline_rtd_integration.py:112:    assert "refresh_rtd_option_quotes_excel" not in command_text
137:UI/components/decisions_grid.py:73:        v_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
138:UI/components/decisions_grid.py:74:        self.tree.configure(yscrollcommand=v_scrollbar.set)
139:UI/components/decisions_grid.py:76:        h_scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
140:UI/components/decisions_grid.py:77:        self.tree.configure(xscrollcommand=h_scrollbar.set)
148:UI/components/payoff_chart.py:81:            top, text="Exportar PNG", command=self.export_png
149:UI/components/payoff_chart.py:86:            top, text="Fixar Curva A", command=self.fix_current_curve
150:UI/components/payoff_chart.py:91:            top, text="Limpar Comparação", command=self.clear_comparison
172:UI/components/structure_editor_dialog.py:434:                self._refresh_rtd_quote_for_symbol(symbol)
173:UI/components/structure_editor_dialog.py:446:    def _refresh_rtd_quote_for_symbol(self, symbol: str) -> None:
174:UI/components/structure_editor_dialog.py:459:        script = project_root / "scripts" / "refresh_rtd_symbol_to_option_quotes_fallback.py"
175:UI/components/structure_editor_dialog.py:474:            raise ValueError(f"Script de refresh RTD não encontrado: {script}")
176:UI/components/structure_editor_dialog.py:515:                "Não foi possível atualizar a cotação RTD para "
195:UI/main_window.py:276:                        self._handle_payoff_error,
223:UI/main_window.py:758:            self._handle_payoff_error(str(e), worker_id)
224:UI/main_window.py:760:    def _handle_payoff_error(self, error_msg: str, worker_id: int):
230:scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:267:- Toda fase encerrada deve atualizar evidencias em docs.
234:scripts/fase-5-diagnostico-rtd.sh:27:  echo "== Busca por handlers Atualizar Dados / Pipeline =="
235:scripts/fase-5-diagnostico-rtd.sh:29:    -E "Atualizar Dados|refresh_data|run_pipeline|Executar Pipeline" UI scripts services db repositories domain . 2>/dev/null | head -300
236:scripts/fase-5-diagnostico-rtd.sh:132:  echo "== Trecho UI/main_window.py refresh_data e run_pipeline =="
237:scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:53:    scripts/run_rtd_refresh_full.py \
238:scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:55:    scripts/refresh_rtd_option_quotes_excel.ps1 \
239:scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:74:    scripts/run_rtd_refresh_full.py \
240:scripts/fase-5c-restaurar-rtd-historico.sh:16:  "scripts/refresh_rtd_option_quotes_excel.ps1"
241:scripts/fase-5c-restaurar-rtd-historico.sh:19:  "scripts/run_rtd_refresh_full.py"
242:scripts/fase-5c-restaurar-rtd-historico.sh:75:    scripts/run_rtd_refresh_full.py
243:scripts/fase-5c-restaurar-rtd-historico.sh:87:  if [ -f scripts/refresh_rtd_option_quotes_excel.ps1 ]; then
244:scripts/fase-5c-restaurar-rtd-historico.sh:88:    sed -n '1,220p' scripts/refresh_rtd_option_quotes_excel.ps1
245:scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:62:  find ATT/tests -type f | grep -Ei "derived|pipeline|orchestrator|refresh|rtd" | sort
246:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:85:    - Não aciona Excel, PowerShell, COM ou refresh RTD ao vivo.
247:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:462:    assert "refresh_rtd_option_quotes_excel" not in command_text
252:scripts/fase5_automacao_gitbash.sh:153:    scripts/run_rtd_refresh_full.py
253:scripts/fase5_automacao_gitbash.sh:154:    scripts/refresh_rtd_option_quotes_excel.ps1
254:scripts/fase5_automacao_gitbash.sh:164:    scripts/refresh_rtd_symbol_to_option_quotes.py
259:scripts/fase5_automacao_gitbash.sh:392:  run_grep "run_derived_pipeline|run_rtd_option_quotes_pipeline|run_rtd_refresh_full|payoff_curve_points|structure_decisions|RTD|rtd|payoff|decision|decisions"
261:scripts/fase5_automacao_gitbash.sh:422:  "scripts/run_rtd_refresh_full.py"
267:scripts/fase5_buscar_fluxo_atualizar_dados.sh:63:  run_grep "run_derived_pipeline|run_rtd_option_quotes_pipeline|run_rtd_refresh_full|payoff_curve_points|structure_decisions|RTD|rtd|payoff|decision|decisions"
269:scripts/fase5_checar_resumo_pipeline.sh:13:  "scripts/run_rtd_refresh_full.py"
270:scripts/import_lista_rtd_excel_to_option_quotes.py:220:    - aguarda RTD atualizar;
271:scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:10:BASE_SCRIPT = Path(__file__).resolve().with_name("refresh_rtd_symbol_to_option_quotes.py")
272:scripts/run_derived_pipeline.py:77:    - Não aciona Excel, PowerShell, COM ou refresh RTD ao vivo.
273:scripts/run_rtd_refresh_full.py:76:        description="Pipeline completo: gerar símbolos RTD, atualizar Excel/CSV e importar cotações no SQLite."
274:scripts/run_rtd_refresh_full.py:87:    parser.add_argument("--skip-excel", action="store_true", help="Pula o refresh do Excel e importa o CSV existente.")
275:scripts/run_rtd_refresh_full.py:101:    ps1_script = Path("scripts/refresh_rtd_option_quotes_excel.ps1")
276:scripts/run_rtd_refresh_full.py:241:            print("Pipeline interrompido no refresh Excel/RTD.")
277:ATT/tests/test_run_derived_pipeline_rtd_integration.py:112:    assert "refresh_rtd_option_quotes_excel" not in command_text
282:UI/components/decisions_grid.py:1:# UI/components/decisions_grid.py
283:UI/components/decisions_grid.py:27:            "decision",
284:UI/components/decisions_grid.py:45:        self.tree.heading("decision", text="Decisão")
285:UI/components/decisions_grid.py:55:        self.tree.column("decision", width=100, anchor="center")
286:UI/components/decisions_grid.py:100:    def update_data(self, decisions: List[Dict]):
287:UI/components/decisions_grid.py:102:        self.current_data = decisions.copy()
288:UI/components/decisions_grid.py:107:        for i, decision in enumerate(decisions, 1):
289:UI/components/decisions_grid.py:108:            timestamp = self._format_timestamp(decision.get("timestamp"))
290:UI/components/decisions_grid.py:111:                decision.get("structure_id") or decision.get("aba") or "N/A"
291:UI/components/decisions_grid.py:113:            decision_text = decision.get("decision", "N/A")
292:UI/components/decisions_grid.py:114:            level = decision.get("level", "")
293:UI/components/decisions_grid.py:115:            ratio = self._format_ratio(decision.get("pl_pct_of_max"))
294:UI/components/decisions_grid.py:116:            dte = decision.get("dte_min", "")
295:UI/components/decisions_grid.py:117:            pl_atual = self._format_currency(decision.get("pl_atual"))
296:UI/components/decisions_grid.py:118:            pl_max = self._format_currency(decision.get("pl_max"))
297:UI/components/decisions_grid.py:121:                decision_text
298:UI/components/decisions_grid.py:122:                if decision_text in ["HOLD", "PREPARE_ROLL", "CLOSE_REOPEN", "ROLL", "ENTER"]
299:UI/components/decisions_grid.py:133:                    decision_text,
300:UI/components/decisions_grid.py:181:    def get_selected_decision(self) -> Optional[Dict]:
301:UI/components/details_panel.py:17:        self._current_decision = None
302:UI/components/details_panel.py:410:            "structure_decisions",
303:UI/components/details_panel.py:411:            "payoff_curve_points",
304:UI/components/details_panel.py:482:        self.decision_label = ttk.Label(
305:UI/components/details_panel.py:485:        self.decision_label.grid(row=1, column=1, sticky="ew", padx=(0, 10))
306:UI/components/details_panel.py:641:    def update_decision(self, decision_data: Dict):
307:UI/components/details_panel.py:642:        self._current_decision = dict(decision_data) if decision_data else None
308:UI/components/details_panel.py:644:        self.timestamp_label.config(text=decision_data.get("timestamp", "N/A"))
309:UI/components/details_panel.py:647:        structure_id = decision_data.get("structure_id") or "N/A"
310:UI/components/details_panel.py:650:        self.decision_label.config(text=decision_data.get("decision", "N/A"))
311:UI/components/details_panel.py:651:        self.level_label.config(text=str(decision_data.get("level", "N/A")))
312:UI/components/details_panel.py:653:        self._format_currency_label(self.pl_atual_label, decision_data.get("pl_atual"))
313:UI/components/details_panel.py:654:        self._format_currency_label(self.pl_max_label, decision_data.get("pl_max"))
314:UI/components/details_panel.py:656:        ratio = decision_data.get("pl_pct_of_max")
315:UI/components/details_panel.py:661:        self.dte_label.config(text=str(decision_data.get("dte_min", "N/A")))
316:UI/components/details_panel.py:663:        spot_ref = decision_data.get("spot_reference") or decision_data.get("spot_ref")
317:UI/components/details_panel.py:672:        why_payload = decision_data.get("why") or decision_data.get("why_json")
318:UI/components/details_panel.py:720:        self._current_decision = None
319:UI/components/details_panel.py:722:            self.timestamp_label, self.structure_label, self.decision_label,
320:UI/components/details_panel.py:878:    def _fetch_latest_decision_from_derived(
321:UI/components/details_panel.py:882:        alteracao_36: filtra por structure_id (INTEGER) em structure_decisions.
322:UI/components/details_panel.py:892:                "structure_id", "timestamp", "decision", "level",
323:UI/components/details_panel.py:900:                FROM structure_decisions
324:UI/components/details_panel.py:920:    def _fetch_payoff_points_from_derived(self, structure_id):
325:UI/components/details_panel.py:922:        alteracao_36: filtra por structure_id (INTEGER) em payoff_curve_points.
326:UI/components/details_panel.py:934:                FROM payoff_curve_points
327:UI/components/details_panel.py:962:                FROM structure_decisions
328:UI/components/details_panel.py:975:                "SELECT COUNT(*) AS n FROM payoff_curve_points WHERE structure_id = ?",
329:UI/components/details_panel.py:980:                "source_table": "derived.db:structure_decisions / payoff_curve_points",
330:UI/components/details_panel.py:1025:        decision = self._fetch_latest_decision_from_derived(structure_id)
331:UI/components/details_panel.py:1026:        if decision:
332:UI/components/details_panel.py:1027:            self.update_decision(decision)
333:UI/components/details_panel.py:1029:        pts = self._fetch_payoff_points_from_derived(structure_id)
334:UI/components/details_panel.py:1033:        if decision:
335:UI/components/details_panel.py:1034:            spot_ref = decision.get("spot_reference")
336:UI/components/details_panel.py:1047:        decision = self._current_decision
337:UI/components/details_panel.py:1048:        if not decision:
338:UI/components/details_panel.py:1055:        structure_id = decision.get("structure_id")
339:UI/components/filters_panel.py:54:        self.decision_var = tk.StringVar()
340:UI/components/filters_panel.py:55:        self.decision_combo = ttk.Combobox(
341:UI/components/filters_panel.py:57:            textvariable=self.decision_var,
342:UI/components/filters_panel.py:62:        self.decision_combo.pack(side="left", padx=(5, 0))
343:UI/components/filters_panel.py:101:        self.decision_combo.bind("<<ComboboxSelected>>", lambda e: self._apply_filters())
344:UI/components/filters_panel.py:116:        if self.decision_var.get().strip():
345:UI/components/filters_panel.py:117:            filters["decision"] = self.decision_var.get().strip()
346:UI/components/filters_panel.py:139:        self.decision_var.set("")
347:UI/components/payoff_chart.py:1:# UI/components/payoff_chart.py
348:UI/components/payoff_chart.py:8:from UI.debug_utils import payoff_debug, payoff_info
349:UI/components/payoff_chart.py:66:        self._last_decision_data: Dict = {}
350:UI/components/payoff_chart.py:164:        self._last_decision_data = {}
351:UI/components/payoff_chart.py:170:        payoff_points: List[Dict],
352:UI/components/payoff_chart.py:171:        decision_data: Optional[Dict] = None,
353:UI/components/payoff_chart.py:178:        self._last_points = list(payoff_points) if payoff_points else []
354:UI/components/payoff_chart.py:179:        self._last_decision_data = dict(decision_data) if decision_data else {}
355:UI/components/payoff_chart.py:182:            payoff_points, decision_data, overlay_curve=self._fixed_curve
356:UI/components/payoff_chart.py:187:        payoff_debug("FIX clicked -- id=", id(self))
357:UI/components/payoff_chart.py:216:        payoff_debug("CLEAR comparison -- id=", id(self))

## Resumo e contadores

43:UI/main_window.py:284:    def refresh_data(self, show_errors: bool = True):
65:UI/main_window.py:418:            self.refresh_data(show_errors=False)
121:scripts/fase5_checar_resumo_pipeline.sh:13:  "scripts/run_rtd_refresh_full.py"
122:scripts/fase5_checar_resumo_pipeline.sh:109:  echo "A Fase 5 deve garantir que o botão Atualizar Dados tenha retorno claro para:"
196:UI/main_window.py:284:    def refresh_data(self, show_errors: bool = True):
218:UI/main_window.py:418:            self.refresh_data(show_errors=False)
269:scripts/fase5_checar_resumo_pipeline.sh:13:  "scripts/run_rtd_refresh_full.py"
449:UI/main_window.py:562:        """Extrai o resumo JSON emitido por scripts/run_derived_pipeline.py."""
450:UI/main_window.py:597:            f"- Decisões: {self._format_pipeline_value(summary.get('decisions'))}",
451:UI/main_window.py:598:            f"- Pontos de payoff: {self._format_pipeline_value(summary.get('payoff_points'))}",
452:UI/main_window.py:599:            f"- Resumos de payoff: {self._format_pipeline_value(summary.get('payoff_summaries'))}",
453:UI/main_window.py:601:            f"- Cotações RTD atualizadas: {self._format_pipeline_value(summary.get('rtd_quotes_updated'))}",
454:UI/main_window.py:613:        decisions = self._format_pipeline_value(summary.get("decisions"))
455:UI/main_window.py:614:        payoff_points = self._format_pipeline_value(summary.get("payoff_points"))
457:UI/main_window.py:619:            f"pontos_payoff={payoff_points}; erros={errors}"
577:scripts/dev/close_phase_5f_ui_pipeline.sh:144:      "rtd_quotes_updated": 4,
581:scripts/dev/close_phase_5f_ui_pipeline.sh:162:| Pontos de payoff exibidos no resumo | OK |
582:scripts/dev/close_phase_5f_ui_pipeline.sh:163:| Cotacoes RTD atualizadas exibidas no resumo | OK |
596:scripts/dev/close_phase_6_integrated_validation.sh:119:| Cotacoes RTD atualizadas exibidas no resumo | OK |
604:scripts/dev/close_phase_6_integrated_validation.sh:163:O sistema confirma execucao operacional pela UI, persistencia em dados/derived.db, resumo operacional ao usuario, decisoes calculadas, curva de payoff disponivel e suite automatizada sem regressao.
616:scripts/dev/open_phase_6_integrated_validation.sh:103:- Importacao RTD retorna sem erros
760:scripts/fase-3f-fix1-evidencia-final.sh:29:  echo "== Validação compute payoff V2 - resumo =="
797:scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:29:  grep -n "def main\|print\|run\|pipeline\|payoff\|decision\|summary\|count\|return" scripts/run_derived_pipeline.py || true
964:scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:30:  echo "== Ocorrencias de rtd_quotes_updated =="
965:scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:31:  grep -R "rtd_quotes_updated" -n . \
972:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:32:_RTD_METRIC_RE = re.compile(r"^\s*(input_rows|inserted|updated|skipped):\s*(-?\d+)\s*$")
976:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:67:def _rtd_quotes_updated_count(rtd_result: dict | None) -> int:
978:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:72:    return int(rtd_result.get("inserted") or 0) + int(rtd_result.get("updated") or 0)
989:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:157:    Placeholder: Gera payoff_curve_summary a partir de payoff_curve_points.
990:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:192:def _collect_pipeline_summary(rtd_result: dict | None = None) -> dict:
1003:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:234:                "payoff_curve_summary",
1005:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:236:                "derived_payoff_summary",
1006:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:243:            "rtd_quotes_updated": _rtd_quotes_updated_count(rtd_result),
1008:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:245:            "warnings": int((rtd_result or {}).get("warnings") or 0),
1009:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:246:            "errors": int((rtd_result or {}).get("errors") or 0),
1026:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:313:            summary = _collect_pipeline_summary(rtd_result)
1028:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:321:        summary = _collect_pipeline_summary(rtd_result)
1029:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:326:    summary = _collect_pipeline_summary(rtd_result)
1030:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:330:    print(f"  Decisões: {_display_summary_value(summary.get('decisions'))}")
1031:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:331:    print(f"  Pontos de payoff: {_display_summary_value(summary.get('payoff_points'))}")
1032:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:332:    print(f"  Resumos de payoff: {_display_summary_value(summary.get('payoff_summaries'))}")
1033:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:334:    print(f"  Cotações RTD atualizadas: {_display_summary_value(summary.get('rtd_quotes_updated'))}")
1040:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:392:def test_rtd_quotes_updated_count_sums_inserted_and_updated():
1041:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:395:    assert module._rtd_quotes_updated_count({"inserted": 2, "updated": 5}) == 7
1042:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:396:    assert module._rtd_quotes_updated_count({"inserted": None, "updated": 5}) == 5
1043:scripts/fase-5e-integrar-rtd-derived-pipeline.sh:397:    assert module._rtd_quotes_updated_count(None) == 0
1118:scripts/fase5_checar_resumo_pipeline.sh:11:  "scripts/run_derived_pipeline.py"
1119:scripts/fase5_checar_resumo_pipeline.sh:12:  "scripts/run_rtd_option_quotes_pipeline.py"
1120:scripts/fase5_checar_resumo_pipeline.sh:13:  "scripts/run_rtd_refresh_full.py"
1121:scripts/fase5_checar_resumo_pipeline.sh:86:  check_term "Pontos de payoff" "payoff_points|payoff_curve_points|pontos_payoff|pontos de payoff"
1122:scripts/fase5_checar_resumo_pipeline.sh:87:  check_term "Decisões" "decisions|structure_decisions|decisoes|decisões"
1123:scripts/fase5_checar_resumo_pipeline.sh:88:  check_term "Cotações RTD" "RTD|rtd|quotes|option_quotes|cotacoes|cotações"
1124:scripts/fase5_checar_resumo_pipeline.sh:99:  write_occurrences "Pontos de payoff" "payoff_points|payoff_curve_points|pontos_payoff|pontos de payoff"
1125:scripts/fase5_checar_resumo_pipeline.sh:100:  write_occurrences "Decisões" "decisions|structure_decisions|decisoes|decisões"
1126:scripts/fase5_checar_resumo_pipeline.sh:101:  write_occurrences "Cotações RTD" "RTD|rtd|quotes|option_quotes|cotacoes|cotações"
1127:scripts/fase5_checar_resumo_pipeline.sh:114:  echo "- pontos de payoff gerados;"
1128:scripts/fase5_checar_resumo_pipeline.sh:116:  echo "- cotações RTD atualizadas;"
1183:scripts/import_rtd_option_quotes_wide_csv.py:237:                "SELECT id, created_at FROM rtd_option_quotes WHERE codigo_opcao = ? ORDER BY id DESC LIMIT 1",
1259:scripts/purge_derived_snapshots.py:14:    "payoff_curve_summary",
1303:scripts/run_derived_pipeline.py:24:_RTD_METRIC_RE = re.compile(r"^\s*(input_rows|inserted|updated|skipped):\s*(-?\d+)\s*$")
1307:scripts/run_derived_pipeline.py:59:def _rtd_quotes_updated_count(rtd_result: dict | None) -> int:
1309:scripts/run_derived_pipeline.py:64:    return int(rtd_result.get("inserted") or 0) + int(rtd_result.get("updated") or 0)
1320:scripts/run_derived_pipeline.py:149:    Placeholder: Gera payoff_curve_summary a partir de payoff_curve_points.
1321:scripts/run_derived_pipeline.py:184:def _collect_pipeline_summary(rtd_result: dict | None = None) -> dict:
1334:scripts/run_derived_pipeline.py:226:                "payoff_curve_summary",
1336:scripts/run_derived_pipeline.py:228:                "derived_payoff_summary",
1337:scripts/run_derived_pipeline.py:235:            "rtd_quotes_updated": _rtd_quotes_updated_count(rtd_result),
1339:scripts/run_derived_pipeline.py:237:            "warnings": int((rtd_result or {}).get("warnings") or 0),
1340:scripts/run_derived_pipeline.py:238:            "errors": int((rtd_result or {}).get("errors") or 0),
1357:scripts/run_derived_pipeline.py:305:            summary = _collect_pipeline_summary(rtd_result)
1359:scripts/run_derived_pipeline.py:313:        summary = _collect_pipeline_summary(rtd_result)
1360:scripts/run_derived_pipeline.py:318:    summary = _collect_pipeline_summary(rtd_result)
1361:scripts/run_derived_pipeline.py:322:    print(f"  Decisões: {_display_summary_value(summary.get('decisions'))}")
1362:scripts/run_derived_pipeline.py:323:    print(f"  Pontos de payoff: {_display_summary_value(summary.get('payoff_points'))}")
1363:scripts/run_derived_pipeline.py:324:    print(f"  Resumos de payoff: {_display_summary_value(summary.get('payoff_summaries'))}")
1364:scripts/run_derived_pipeline.py:326:    print(f"  Cotações RTD atualizadas: {_display_summary_value(summary.get('rtd_quotes_updated'))}")
1454:repositories/market_snapshot_repository.py:257:      get_rtd_summary(aba)             -> dict com cabecalho RTD ou None
1467:repositories/market_snapshot_repository.py:349:    def get_rtd_summary(self, ref: StructureRef | str) -> Optional[dict]:
1472:repositories/market_snapshot_repository.py:376:            summary = self.get_rtd_summary(ref)
1793:ATT/tests/test_audit_rtd_option_quotes.py:86:            VALUES (?, 'PETR4', 'CALL', 30.0, 1.0, 1.1, 'rtd_links', {updated_at_sql}, CURRENT_TIMESTAMP)
1794:ATT/tests/test_audit_rtd_option_quotes.py:111:    assert "table not found: rtd_option_quotes" in result["errors"]
2048:ATT/tests/test_run_derived_pipeline_rtd_integration.py:42:def test_rtd_quotes_updated_count_sums_inserted_and_updated():
2049:ATT/tests/test_run_derived_pipeline_rtd_integration.py:45:    assert module._rtd_quotes_updated_count({"inserted": 2, "updated": 5}) == 7
2050:ATT/tests/test_run_derived_pipeline_rtd_integration.py:46:    assert module._rtd_quotes_updated_count({"inserted": None, "updated": 5}) == 5
2051:ATT/tests/test_run_derived_pipeline_rtd_integration.py:47:    assert module._rtd_quotes_updated_count(None) == 0
2103:ATT/tests/test_structure_analysis_service.py:185:    assert "validation_errors" in result["decision"]["why"]
2214:## Candidatos de resumo e contadores
2216:UI/components/details_panel.py:315:                "created_at": 97,
2217:UI/components/details_panel.py:316:                "updated_at": 96,
2218:UI/components/details_panel.py:332:            if "created" in low:
2219:UI/components/details_panel.py:334:            if "updated" in low:
2220:UI/components/details_panel.py:368:                ignored = {str(c).lower() for c in structure_cols}
2221:UI/components/details_panel.py:369:                ignored.update(
2222:UI/components/details_panel.py:378:                ts_cols = [c for c in cols if str(c).lower() not in ignored]
2223:UI/components/details_panel.py:568:        self.operational_cancelled_ignored_label = ttk.Label(
2224:UI/components/details_panel.py:571:        self.operational_cancelled_ignored_label.grid(
2225:UI/components/details_panel.py:617:        self.created_at_label = ttk.Label(
2226:UI/components/details_panel.py:620:        self.created_at_label.grid(row=0, column=3, sticky="ew")
2227:UI/components/details_panel.py:689:        self.created_at_label.config(text="N/A")
2228:UI/components/details_panel.py:716:        created_at = info.get("created_at")
2229:UI/components/details_panel.py:717:        self.created_at_label.config(text=created_at if created_at else "N/A")
2230:UI/components/details_panel.py:725:            self.breakevens_label, self.source_label, self.created_at_label,
2231:UI/components/details_panel.py:727:            self.operational_cancelled_ignored_label,
2232:UI/components/details_panel.py:758:            "operational_cancelled_ignored_label",
2233:UI/components/details_panel.py:774:                "events_ignored_cancelled": int,
2234:UI/components/details_panel.py:782:        - ignored_events.
2235:UI/components/details_panel.py:796:        ignored = state.get("events_ignored_cancelled")
2236:UI/components/details_panel.py:797:        if ignored is None and isinstance(effective_structure.get("ignored_events"), list):
2237:UI/components/details_panel.py:798:            ignored = len(effective_structure.get("ignored_events") or [])
2238:UI/components/details_panel.py:812:        self.operational_cancelled_ignored_label.config(
2239:UI/components/details_panel.py:813:            text=str(ignored) if ignored is not None else "N/A"
2240:UI/components/details_panel.py:894:                "spot_ref", "meta_json", "created_at", "why_json",
2241:UI/components/details_panel.py:902:                ORDER BY COALESCE(created_at, timestamp) DESC
2242:UI/components/details_panel.py:961:                SELECT created_at, timestamp
2243:UI/components/details_panel.py:964:                ORDER BY COALESCE(created_at, timestamp) DESC
2244:UI/components/details_panel.py:970:            created_at = None
2245:UI/components/details_panel.py:972:                created_at = row["created_at"] or row["timestamp"]
2246:UI/components/details_panel.py:981:                "created_at": created_at,
2247:UI/components/structures_list_panel.py:293:                 if k not in ("id", "structure_id", "created_at", "updated_at")}
2248:UI/components/structure_editor_dialog.py:499:            errors="replace",
2249:UI/components/structure_editor_dialog.py:776:                        locals().get("created_structure_id")
2250:UI/components/structure_editor_dialog.py:781:                        or locals().get("created_id")
2251:UI/main_window.py:284:    def refresh_data(self, show_errors: bool = True):
2252:UI/main_window.py:347:            if show_errors:
2253:UI/main_window.py:418:            self.refresh_data(show_errors=False)
2254:UI/main_window.py:561:    def _extract_pipeline_summary(self, stdout: str) -> Dict:
2255:UI/main_window.py:562:        """Extrai o resumo JSON emitido por scripts/run_derived_pipeline.py."""
2256:UI/main_window.py:577:        """Formata valores do resumo operacional para exibição."""
2257:UI/main_window.py:584:        summary = self._extract_pipeline_summary(stdout)
2258:UI/main_window.py:586:        if not summary:
2259:UI/main_window.py:596:            f"- Estruturas: {self._format_pipeline_value(summary.get('structures'))}",
2260:UI/main_window.py:597:            f"- Decisões: {self._format_pipeline_value(summary.get('decisions'))}",
2261:UI/main_window.py:598:            f"- Pontos de payoff: {self._format_pipeline_value(summary.get('payoff_points'))}",
2262:UI/main_window.py:599:            f"- Resumos de payoff: {self._format_pipeline_value(summary.get('payoff_summaries'))}",
2263:UI/main_window.py:600:            f"- Execuções de pricing: {self._format_pipeline_value(summary.get('pricing_executions'))}",
2264:UI/main_window.py:601:            f"- Cotações RTD atualizadas: {self._format_pipeline_value(summary.get('rtd_quotes_updated'))}",
2265:UI/main_window.py:602:            f"- Avisos: {self._format_pipeline_value(summary.get('warnings'))}",
2266:UI/main_window.py:603:            f"- Erros: {self._format_pipeline_value(summary.get('errors'))}",
2267:UI/main_window.py:609:        summary = self._extract_pipeline_summary(stdout)
2268:UI/main_window.py:610:        if not summary:
2269:UI/main_window.py:613:        decisions = self._format_pipeline_value(summary.get("decisions"))
2270:UI/main_window.py:614:        payoff_points = self._format_pipeline_value(summary.get("payoff_points"))
2271:UI/main_window.py:615:        errors = self._format_pipeline_value(summary.get("errors"))
2272:UI/main_window.py:619:            f"pontos_payoff={payoff_points}; erros={errors}"
2273:UI/main_window.py:850:                f"Criado em  : {str(structure.get('created_at', ''))[:19]}",
2274:UI/main_window.py:851:                f"Atualizado : {str(structure.get('updated_at', ''))[:19]}",
2275:UI/models/ui_data.py:520:                "created_at": None,
2276:UI/models/ui_data.py:528:                    extra_cols = ", meta_json, created_at"
2277:UI/models/ui_data.py:555:                    info["created_at"] = rows[0]["created_at"]
2278:scripts/apply_fase9_atomic_create.py:85:                    status, notes, created_at, updated_at
2279:scripts/apply_fase9_atomic_create.py:108:                    "created_at": now,
2280:scripts/apply_fase9_atomic_create.py:109:                    "updated_at": now,
2281:scripts/apply_fase9_atomic_create.py:119:                        multiplier, leg_order, notes, created_at, updated_at
2282:scripts/audit_rtd_option_quotes.py:43:    "updated_at",
2283:scripts/audit_rtd_option_quotes.py:44:    "created_at",
2284:scripts/audit_rtd_option_quotes.py:86:        "errors": [],
2285:scripts/audit_rtd_option_quotes.py:87:        "warnings": [],
2286:scripts/audit_rtd_option_quotes.py:95:        result["errors"].append("database file not found")
2287:scripts/audit_rtd_option_quotes.py:101:            result["errors"].append(f"table not found: {TABLE_NAME}")
2288:scripts/audit_rtd_option_quotes.py:113:            result["errors"].append(
