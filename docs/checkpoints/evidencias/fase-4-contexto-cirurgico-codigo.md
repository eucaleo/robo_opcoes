# Fase 4 - Contexto cirurgico para alteracao de codigo

Data: Tue Jun 23 19:55:00     2026
Branch: reinicio-normalizacao-idioma-ptbr
HEAD: 545f4e6

## Status git
?? docs/checkpoints/evidencias/fase-3-4-alvos-provaveis-correcao.txt
?? docs/checkpoints/evidencias/fase-3-contexto-cirurgico-codigo.md
?? docs/checkpoints/evidencias/fase-3-correcao-codigo-inventario.txt
?? docs/checkpoints/evidencias/fase-4-contexto-cirurgico-codigo.md
?? docs/checkpoints/evidencias/fase-4-correcao-codigo-inventario.txt
?? tools/

## Objetivo tecnico da Fase 4
Encerrar a Fase 4 com alteracao real de codigo:
- payoff e decisao devem operar por structure_id;
- get_payoff_by_aba nao deve voltar como interface publica;
- persistencia deve gravar e consultar dados por structure_id quando disponivel;
- UI deve renderizar payoff/decisao por structure_id;
- alias/aba legado pode existir somente como compatibilidade historica ou fonte RTD legada.

## Ocorrencias criticas em codigo produtivo - payoff/decision/persistencia/UI
UI/components/decisions_grid.py:1:# UI/components/decisions_grid.py
UI/components/decisions_grid.py:9:class DecisionsGrid(ttk.LabelFrame):
UI/components/decisions_grid.py:26:            "structure_id",
UI/components/decisions_grid.py:27:            "decision",
UI/components/decisions_grid.py:44:        self.tree.heading("structure_id", text="Estrutura")
UI/components/decisions_grid.py:45:        self.tree.heading("decision", text="Decisão")
UI/components/decisions_grid.py:54:        self.tree.column("structure_id", width=100, anchor="center")
UI/components/decisions_grid.py:55:        self.tree.column("decision", width=100, anchor="center")
UI/components/decisions_grid.py:65:        # Tags de cor por decisão
UI/components/decisions_grid.py:100:    def update_data(self, decisions: List[Dict]):
UI/components/decisions_grid.py:102:        self.current_data = decisions.copy()
UI/components/decisions_grid.py:107:        for i, decision in enumerate(decisions, 1):
UI/components/decisions_grid.py:108:            timestamp = self._format_timestamp(decision.get("timestamp"))
UI/components/decisions_grid.py:109:            # Exibe structure_id; fallback para aba (compat)
UI/components/decisions_grid.py:110:            structure_id = (
UI/components/decisions_grid.py:111:                decision.get("structure_id") or decision.get("aba") or "N/A"
UI/components/decisions_grid.py:113:            decision_text = decision.get("decision", "N/A")
UI/components/decisions_grid.py:114:            level = decision.get("level", "")
UI/components/decisions_grid.py:115:            ratio = self._format_ratio(decision.get("pl_pct_of_max"))
UI/components/decisions_grid.py:116:            dte = decision.get("dte_min", "")
UI/components/decisions_grid.py:117:            pl_atual = self._format_currency(decision.get("pl_atual"))
UI/components/decisions_grid.py:118:            pl_max = self._format_currency(decision.get("pl_max"))
UI/components/decisions_grid.py:121:                decision_text
UI/components/decisions_grid.py:122:                if decision_text in ["HOLD", "PREPARE_ROLL", "CLOSE_REOPEN", "ROLL", "ENTER"]
UI/components/decisions_grid.py:132:                    structure_id,
UI/components/decisions_grid.py:133:                    decision_text,
UI/components/decisions_grid.py:181:    def get_selected_decision(self) -> Optional[Dict]:
UI/components/decisions_grid.py:182:        """Retorna decisão atualmente selecionada."""
UI/components/decisions_grid.py:194:    def select_by_key(self, structure_id: str, timestamp: str) -> bool:
UI/components/decisions_grid.py:196:        Seleciona a linha cujo (structure_id, timestamp) bate no dataset.
UI/components/decisions_grid.py:197:        Aceita tanto 'structure_id' quanto 'aba' nos dicts (compat).
UI/components/decisions_grid.py:200:        if not structure_id or not timestamp:
UI/components/decisions_grid.py:204:            row_sid = row.get("structure_id") or row.get("aba")
UI/components/decisions_grid.py:205:            if row_sid == structure_id and row.get("timestamp") == timestamp:
UI/components/details_panel.py:17:        self._current_decision = None
UI/components/details_panel.py:59:        for attr in ("db_path", "_db_path", "database_path", "_database_path"):
UI/components/details_panel.py:90:    def _resolve_structure_key(self, structure_id) -> int:
UI/components/details_panel.py:92:        structure_id é sempre INTEGER no DB.
UI/components/details_panel.py:96:            return int(structure_id)
UI/components/details_panel.py:99:                f"structure_id inválido: {structure_id!r}. "
UI/components/details_panel.py:107:    def _get_latest_snapshot_timestamp_for_structure(self, structure_id):
UI/components/details_panel.py:119:        sid = self._resolve_structure_key(structure_id)
UI/components/details_panel.py:147:                or "database" in low_name
UI/components/details_panel.py:169:            "_database_path",
UI/components/details_panel.py:170:            "database_path",
UI/components/details_panel.py:226:                "_database_path",
UI/components/details_panel.py:227:                "database_path",
UI/components/details_panel.py:300:                low == "structure_id"
UI/components/details_panel.py:304:                or low.endswith("_structure_id")
UI/components/details_panel.py:372:                        "structure_id",
UI/components/details_panel.py:410:            "structure_decisions",
UI/components/details_panel.py:411:            "payoff_curve_points",
UI/components/details_panel.py:443:    def _compute_recalc_signature(self, structure_id):
UI/components/details_panel.py:445:            structure_id,
UI/components/details_panel.py:446:            self._get_latest_snapshot_timestamp_for_structure(structure_id),
UI/components/details_panel.py:479:        ttk.Label(basic_frame, text="Decisão:").grid(
UI/components/details_panel.py:482:        self.decision_label = ttk.Label(
UI/components/details_panel.py:485:        self.decision_label.grid(row=1, column=1, sticky="ew", padx=(0, 10))
UI/components/details_panel.py:641:    def update_decision(self, decision_data: Dict):
UI/components/details_panel.py:642:        self._current_decision = dict(decision_data) if decision_data else None
UI/components/details_panel.py:644:        self.timestamp_label.config(text=decision_data.get("timestamp", "N/A"))
UI/components/details_panel.py:646:        # alteracao_36: structure_id é autoritativo; aba removido
UI/components/details_panel.py:647:        structure_id = decision_data.get("structure_id") or "N/A"
UI/components/details_panel.py:648:        self.structure_label.config(text=str(structure_id))
UI/components/details_panel.py:650:        self.decision_label.config(text=decision_data.get("decision", "N/A"))
UI/components/details_panel.py:651:        self.level_label.config(text=str(decision_data.get("level", "N/A")))
UI/components/details_panel.py:653:        self._format_currency_label(self.pl_atual_label, decision_data.get("pl_atual"))
UI/components/details_panel.py:654:        self._format_currency_label(self.pl_max_label, decision_data.get("pl_max"))
UI/components/details_panel.py:656:        ratio = decision_data.get("pl_pct_of_max")
UI/components/details_panel.py:661:        self.dte_label.config(text=str(decision_data.get("dte_min", "N/A")))
UI/components/details_panel.py:663:        spot_ref = decision_data.get("spot_reference") or decision_data.get("spot_ref")
UI/components/details_panel.py:672:        why_payload = decision_data.get("why") or decision_data.get("why_json")
UI/components/details_panel.py:693:        if structure_id != "N/A":
UI/components/details_panel.py:694:            self._refresh_operational_state_for_structure(structure_id)
UI/components/details_panel.py:720:        self._current_decision = None
UI/components/details_panel.py:722:            self.timestamp_label, self.structure_label, self.decision_label,
UI/components/details_panel.py:734:    def on_recalc_finished(self, structure_id, ok: bool, message: str = ""):
UI/components/details_panel.py:739:                    structure_id
UI/components/details_panel.py:743:                    msg=message or f"OK: {structure_id} recalculado",
UI/components/details_panel.py:817:    def _fetch_effective_structure_local(self, structure_id) -> Optional[Dict[str, Any]]:
UI/components/details_panel.py:827:            sid = self._resolve_structure_key(structure_id)
UI/components/details_panel.py:854:    def _refresh_operational_state_for_structure(self, structure_id):
UI/components/details_panel.py:855:        effective = self._fetch_effective_structure_local(structure_id)
UI/components/details_panel.py:878:    def _fetch_latest_decision_from_derived(
UI/components/details_panel.py:879:        self, structure_id
UI/components/details_panel.py:882:        alteracao_36: filtra por structure_id (INTEGER) em structure_decisions.
UI/components/details_panel.py:883:        Legado aba removido.
UI/components/details_panel.py:885:        sid = self._resolve_structure_key(structure_id)
UI/components/details_panel.py:892:                "structure_id", "timestamp", "decision", "level",
UI/components/details_panel.py:900:                FROM structure_decisions
UI/components/details_panel.py:901:                WHERE structure_id = ?
UI/components/details_panel.py:920:    def _fetch_payoff_points_from_derived(self, structure_id):
UI/components/details_panel.py:922:        alteracao_36: filtra por structure_id (INTEGER) em payoff_curve_points.
UI/components/details_panel.py:923:        Legado aba removido.
UI/components/details_panel.py:925:        sid = self._resolve_structure_key(structure_id)
UI/components/details_panel.py:934:                FROM payoff_curve_points
UI/components/details_panel.py:935:                WHERE structure_id = ?
UI/components/details_panel.py:948:    def _fetch_audit_info_from_derived(self, structure_id) -> Dict[str, Any]:
UI/components/details_panel.py:950:        alteracao_36: filtra por structure_id (INTEGER).
UI/components/details_panel.py:951:        Legado aba removido.
UI/components/details_panel.py:953:        sid = self._resolve_structure_key(structure_id)
UI/components/details_panel.py:962:                FROM structure_decisions
UI/components/details_panel.py:963:                WHERE structure_id = ?
UI/components/details_panel.py:975:                "SELECT COUNT(*) AS n FROM payoff_curve_points WHERE structure_id = ?",
UI/components/details_panel.py:980:                "source_table": "derived.db:structure_decisions / payoff_curve_points",
UI/components/details_panel.py:1023:    def _refresh_current_from_derived(self, structure_id):
UI/components/details_panel.py:1025:        decision = self._fetch_latest_decision_from_derived(structure_id)
UI/components/details_panel.py:1026:        if decision:
UI/components/details_panel.py:1027:            self.update_decision(decision)
UI/components/details_panel.py:1029:        pts = self._fetch_payoff_points_from_derived(structure_id)
UI/components/details_panel.py:1033:        if decision:
UI/components/details_panel.py:1034:            spot_ref = decision.get("spot_reference")
UI/components/details_panel.py:1039:        audit = self._fetch_audit_info_from_derived(structure_id)
UI/components/details_panel.py:1047:        decision = self._current_decision
UI/components/details_panel.py:1048:        if not decision:
UI/components/details_panel.py:1050:                text="Nenhuma decisão selecionada", foreground="red"
UI/components/details_panel.py:1054:        # alteracao_36: structure_id é único identificador
UI/components/details_panel.py:1055:        structure_id = decision.get("structure_id")
UI/components/details_panel.py:1056:        if not structure_id:
UI/components/details_panel.py:1065:                msg=f"Recalc já em andamento ({structure_id})",
UI/components/details_panel.py:1072:        sig = self._compute_recalc_signature(structure_id)
UI/components/details_panel.py:1077:                msg=f"Recalculando {structure_id}...",
UI/components/details_panel.py:1081:                self._on_recalculate_cb(structure_id)
UI/components/payoff_chart.py:1:# UI/components/payoff_chart.py
UI/components/payoff_chart.py:8:from UI.debug_utils import payoff_debug, payoff_info
UI/components/payoff_chart.py:55:class PayoffChart(ttk.Frame):
UI/components/payoff_chart.py:66:        self._last_decision_data: Dict = {}
UI/components/payoff_chart.py:144:        self.ax.set_title("Curva de Payoff")
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
UI/components/payoff_chart.py:305:        # Label da curva principal (B quando há overlay, senão "Payoff")
UI/components/payoff_chart.py:307:        if overlay_curve and decision_data:
UI/components/payoff_chart.py:309:                decision_data.get("structure_id")
UI/components/payoff_chart.py:310:                or decision_data.get("aba", "")
UI/components/payoff_chart.py:314:            main_label = "Payoff"
UI/components/payoff_chart.py:351:        if decision_data:
UI/components/payoff_chart.py:352:            raw = decision_data.get("spot_ref") or decision_data.get("spot_reference")
UI/components/payoff_chart.py:416:        if decision_data:
UI/components/payoff_chart.py:418:                decision_data.get("structure_id")
UI/components/payoff_chart.py:419:                or decision_data.get("aba", "")
UI/components/payoff_chart.py:421:            dec = decision_data.get("decision", "")
UI/components/payoff_chart.py:422:            title = f"Payoff -- {sid} [{dec}]"
UI/components/payoff_chart.py:426:            title = "Curva de Payoff -- Comparação"
UI/components/payoff_chart.py:428:            title = "Curva de Payoff"
UI/components/payoff_chart.py:453:            p, ["point_pl", "pl", "y", "pnl", "payoff", "profit_loss", "pl_value"]
UI/main_window.py:5:Carrega dados de derived.db e app.db para exibir decisões e payoffs
UI/main_window.py:8:from UI.components.payoff_chart import PayoffChart
UI/main_window.py:10:from UI.components.decisions_grid import DecisionsGrid
UI/main_window.py:40:        self._payoff_worker_id = 0
UI/main_window.py:46:        self._loading_payoff = False
UI/main_window.py:49:        # Última decisão selecionada (preservada entre refreshes)
UI/main_window.py:50:        self.last_selected_decision: Optional[Dict] = None
UI/main_window.py:57:        # Não executa pipeline e não recalcula payoff.
UI/main_window.py:84:        # Painel direito: notebook com abas
UI/main_window.py:95:        self.decisions_grid = DecisionsGrid(
UI/main_window.py:97:            on_selection_change=self.on_decision_selected,
UI/main_window.py:99:        self.decisions_grid.pack(fill="both", expand=True, padx=5, pady=5)
UI/main_window.py:105:        # Aba 1: Detalhes da Decisão
UI/main_window.py:107:        right_notebook.add(details_frame, text="Detalhes da Decisão")
UI/main_window.py:116:        # Aba 2: Gráfico de Payoff
UI/main_window.py:118:        right_notebook.add(chart_frame, text="Curva de Payoff")
UI/main_window.py:120:        self.payoff_chart = PayoffChart(chart_frame)
UI/main_window.py:121:        self.payoff_chart.pack(fill="both", expand=True, padx=5, pady=5)
UI/main_window.py:123:        # Aba 3: Estruturas (Fase 5 -- alteracao_10)
UI/main_window.py:153:        tools_menu.add_command(label="Verificar Bancos", command=self.check_databases)
UI/main_window.py:176:            filtered_data = self.data_model.get_decisions(filters)
UI/main_window.py:177:            self.decisions_grid.update_data(filtered_data)
UI/main_window.py:184:    def on_decision_selected(self, decision_data: Dict):
UI/main_window.py:185:        """Callback quando uma decisão é selecionada no grid.
UI/main_window.py:186:        alteracao_36: structure_id é suficiente para carregar payoff -- timestamp não é obrigatório.
UI/main_window.py:188:        if not decision_data:
UI/main_window.py:191:        self.last_selected_decision = dict(decision_data)
UI/main_window.py:195:            self.details_panel.update_decision(decision_data)
UI/main_window.py:199:        # Carregar payoff em background -- apenas structure_id necessário
UI/main_window.py:200:        structure_id = decision_data.get("structure_id")
UI/main_window.py:201:        timestamp = decision_data.get("timestamp")  # opcional
UI/main_window.py:203:        if structure_id is not None:
UI/main_window.py:204:            self._start_payoff_load(structure_id, timestamp, decision_data)
UI/main_window.py:206:            self.payoff_chart.clear()
UI/main_window.py:207:            self.status_bar.config(text="Dados insuficientes para payoff")
UI/main_window.py:209:    def _start_payoff_load(
UI/main_window.py:211:        structure_id,
UI/main_window.py:213:        decision_data=None,   # alteracao_36: opcional
UI/main_window.py:215:        """Inicia carregamento de payoff em thread separada.
UI/main_window.py:216:        alteracao_36: structure_id é a única chave obrigatória.
UI/main_window.py:218:        if decision_data is None:
UI/main_window.py:219:            decision_data = {"structure_id": structure_id}
UI/main_window.py:221:        self._payoff_worker_id += 1
UI/main_window.py:222:        current_worker_id = self._payoff_worker_id
UI/main_window.py:224:        if self._loading_payoff:
UI/main_window.py:225:            self.status_bar.config(text="Carregando payoff... (cancelando anterior)")
UI/main_window.py:227:            self.status_bar.config(text="Carregando payoff...")
UI/main_window.py:229:        self._loading_payoff = True
UI/main_window.py:233:                points, info_dict = self.data_model.get_payoff_curve_info(
UI/main_window.py:234:                    structure_id, timestamp
UI/main_window.py:238:                        f"payoff structure_id={structure_id} ts_req={timestamp} "
UI/main_window.py:261:                if current_worker_id != self._payoff_worker_id:
UI/main_window.py:266:                    self._finish_payoff_load,
UI/main_window.py:269:                    decision_data,
UI/main_window.py:273:                if current_worker_id == self._payoff_worker_id:
UI/main_window.py:276:                        self._handle_payoff_error,
UI/main_window.py:286:        alteracao_36: preserva seleção usando structure_id como chave -- timestamp é auxiliar.
UI/main_window.py:304:            decisions = self.data_model.get_decisions()
UI/main_window.py:305:            self.decisions_grid.update_data(decisions)
UI/main_window.py:308:            d = self.last_selected_decision
UI/main_window.py:311:                target_sid = d.get("structure_id")  # chave canônica
UI/main_window.py:314:                # Reselecionar na grid: structure_id é suficiente
UI/main_window.py:317:                        self.decisions_grid.select_by_key(target_sid, target_ts)
UI/main_window.py:322:                        self.details_panel.update_decision(d)
UI/main_window.py:327:                        self._start_payoff_load(target_sid, target_ts, d)
UI/main_window.py:338:                    self.payoff_chart.clear()
UI/main_window.py:343:                text=f"Dados atualizados - {len(decisions)} decisões"
UI/main_window.py:439:                current_data = self.decisions_grid.get_current_data()
UI/main_window.py:445:    def recalculate_structure(self, structure_id: str):
UI/main_window.py:447:        Recalcula a estrutura identificada por structure_id e atualiza a UI.
UI/main_window.py:456:                    text=f"Recalc já em andamento; ignorando ({structure_id})"
UI/main_window.py:463:            sid = int(structure_id)
UI/main_window.py:467:                    text=f"structure_id inválido para recálculo: {structure_id}"
UI/main_window.py:476:            self.payoff_chart.fix_current_curve()
UI/main_window.py:517:                print(f"[UI] Recalc structure_id={sid} result:", result)
UI/main_window.py:597:            f"- Decisões: {self._format_pipeline_value(summary.get('decisions'))}",
UI/main_window.py:598:            f"- Pontos de payoff: {self._format_pipeline_value(summary.get('payoff_points'))}",
UI/main_window.py:599:            f"- Resumos de payoff: {self._format_pipeline_value(summary.get('payoff_summaries'))}",
UI/main_window.py:613:        decisions = self._format_pipeline_value(summary.get("decisions"))
UI/main_window.py:614:        payoff_points = self._format_pipeline_value(summary.get("payoff_points"))
UI/main_window.py:618:            f"Pipeline OK: decisões={decisions}; "
UI/main_window.py:619:            f"pontos_payoff={payoff_points}; erros={errors}"
UI/main_window.py:681:    def check_databases(self):
UI/main_window.py:684:            status = self.data_model.check_database_status()
UI/main_window.py:699:Pipeline automático de payoff e decisões
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
UI/main_window.py:798:    # Aba Estruturas (Fase 5 -- alteracao_10)
UI/main_window.py:802:        """Aba 'Estruturas' no notebook principal."""
UI/main_window.py:848:                f"Aba legado : {structure.get('alias_legacy_aba') or '--'}",
UI/main_window.py:868:    def _on_structure_edit_request(self, structure_id: Optional[int]):
UI/main_window.py:872:            structure_id=structure_id,
UI/main_window.py:877:            saved_structure_id = getattr(dlg, "saved_structure_id", None) or structure_id
UI/main_window.py:886:            if saved_structure_id is not None:
UI/main_window.py:887:                self._reprice_structure_after_save(int(saved_structure_id))
UI/main_window.py:890:    def _reprice_structure_after_save(self, structure_id: int) -> None:
UI/main_window.py:892:        Recalcula pricing/payoff/decisão após criação ou edição manual.
UI/main_window.py:910:        sid = int(structure_id)
UI/main_window.py:911:        _post_status(f"Estrutura {sid} salva. Recalculando payoff...")
UI/main_window.py:927:                    _set_status(f"Estrutura {sid} salva e payoff recalculado.")
UI/models/ui_data.py:16:    CANDIDATE_PAYOFF_TABLES,
UI/models/ui_data.py:22:    "structure_id":  ["structure_id"],                              #  alteracao_33: chave canônica
UI/models/ui_data.py:23:    "aba":           ["aba", "sheet", "tab"],                       # mantido para compat
UI/models/ui_data.py:24:    "decision":      ["decision", "decisao", "action"],
UI/models/ui_data.py:36:PAYOFF_COLUMN_ALIASES = {
UI/models/ui_data.py:38:    "structure_id": ["structure_id"],   #  alteracao_33
UI/models/ui_data.py:40:    "pl":        ["point_pl", "pl", "pl_value", "y", "payoff", "pl_venc"],
UI/models/ui_data.py:61:        self._payoff_table: Optional[str] = None
UI/models/ui_data.py:63:        self._payoff_cols: Dict[str, str] = {}
UI/models/ui_data.py:66:        self._payoff_cache: Dict[Tuple[str, str], Dict[str, Any]] = {}
UI/models/ui_data.py:67:        self._payoff_cache_max = 128
UI/models/ui_data.py:101:        for t in CANDIDATE_PAYOFF_TABLES:
UI/models/ui_data.py:103:                self._payoff_table = t
UI/models/ui_data.py:124:    def _build_payoff_colmap(self):
UI/models/ui_data.py:125:        if not self._payoff_table:
UI/models/ui_data.py:126:            self._payoff_cols = {}
UI/models/ui_data.py:129:        cols = self._inspect_columns(self._payoff_table)
UI/models/ui_data.py:132:        if self._payoff_table == "payoff_curve_points":
UI/models/ui_data.py:137:                # alteracao_36_F: structure_id e opcional aqui --
UI/models/ui_data.py:140:                "structure_id": ["structure_id"],   #  alteracao_34: único identificador canônico
UI/models/ui_data.py:142:            print(f"[UI] Usando contrato canônico para {self._payoff_table}")
UI/models/ui_data.py:144:            aliases = PAYOFF_COLUMN_ALIASES
UI/models/ui_data.py:145:            print(f"[UI] Usando aliases flexíveis para {self._payoff_table}")
UI/models/ui_data.py:151:            # alteracao_36_F: nao lanca erro se structure_id ausente --
UI/models/ui_data.py:154:        self._payoff_cols = colmap
UI/models/ui_data.py:156:        if ("spot" not in self._payoff_cols) or ("pl" not in self._payoff_cols):
UI/models/ui_data.py:158:                f"Tabela {self._payoff_table} não apresenta colunas obrigatórias "
UI/models/ui_data.py:159:                f"para payoff (point_spot/point_pl ou spot/pl)."
UI/models/ui_data.py:162:        # alteracao_36_F: aviso explicito quando structure_id ausente (pre-migration)
UI/models/ui_data.py:163:        if "structure_id" not in self._payoff_cols:
UI/models/ui_data.py:165:                f"[UI] AVISO: {self._payoff_table} nao tem coluna structure_id. "
UI/models/ui_data.py:171:    #   Prioriza structure_id; cai em aba se structure_id não mapeado.
UI/models/ui_data.py:175:        alteracao_34: retorna apenas o nome da coluna structure_id.
UI/models/ui_data.py:176:        Branch aba removido -- schemas sem structure_id nao sao mais suportados.
UI/models/ui_data.py:178:        if colmap.get("structure_id"):
UI/models/ui_data.py:179:            return colmap["structure_id"]
UI/models/ui_data.py:181:            "Coluna 'structure_id' nao encontrada no colmap. "
UI/models/ui_data.py:185:    def _resolve_structure_key(self, structure_id: str) -> int:
UI/models/ui_data.py:187:        alteracao_34: structure_id e sempre INTEGER.
UI/models/ui_data.py:191:            return int(structure_id)
UI/models/ui_data.py:194:                f"structure_id invalido: {structure_id!r}. "
UI/models/ui_data.py:205:        self._build_payoff_colmap()
UI/models/ui_data.py:211:        if not c.get("structure_id"):
UI/models/ui_data.py:213:                "Coluna 'structure_id' nao encontrada em "
UI/models/ui_data.py:217:        sid_col = c["structure_id"]
UI/models/ui_data.py:221:                f"SELECT DISTINCT CAST({sid_col} AS TEXT) AS structure_id "
UI/models/ui_data.py:224:                f"ORDER BY structure_id"
UI/models/ui_data.py:227:            return [r["structure_id"] for r in rows]
UI/models/ui_data.py:232:        """Alias de get_structure_ids() para compatibilidade."""
UI/models/ui_data.py:237:    def get_structure_ids(self) -> List[str]:
UI/models/ui_data.py:243:    def get_abas(self) -> list:
UI/models/ui_data.py:244:        """Alias readonly de get_structure_ids() -- compat UI (alteracao_34:filtro_aba)."""
UI/models/ui_data.py:245:        return self.get_structure_ids()
UI/models/ui_data.py:247:    def get_decisions(self, filters: Optional[Dict] = None) -> List[Dict]:
UI/models/ui_data.py:250:        alteracao_33: filtra por structure_id quando disponível.
UI/models/ui_data.py:271:        # patch_3a: deriva aba <-> structure_id quando coluna física ausente
UI/models/ui_data.py:274:            "timestamp", "structure_id", "aba", "decision", "level",
UI/models/ui_data.py:280:            elif alias == "aba":
UI/models/ui_data.py:281:                sid_src = c.get("structure_id")
UI/models/ui_data.py:283:                    select_parts.append(f"CAST({sid_src} AS TEXT) AS aba")
UI/models/ui_data.py:285:                    select_parts.append("NULL AS aba")
UI/models/ui_data.py:286:            elif alias == "structure_id":
UI/models/ui_data.py:287:                aba_src = c.get("aba")
UI/models/ui_data.py:288:                if aba_src:
UI/models/ui_data.py:290:                        f"CASE WHEN CAST({aba_src} AS TEXT) GLOB '[0-9]*' "
UI/models/ui_data.py:291:                        f"THEN CAST({aba_src} AS INTEGER) ELSE NULL END AS structure_id"
UI/models/ui_data.py:294:                    select_parts.append("NULL AS structure_id")
UI/models/ui_data.py:321:            structure_filter = filters.get("structure_id")
UI/models/ui_data.py:324:                    where.append("t.structure_id = ?")
UI/models/ui_data.py:328:                        f"structure_id deve ser inteiro; recebido: {structure_filter!r}"
UI/models/ui_data.py:331:            aba_filter = filters.get("aba")
UI/models/ui_data.py:332:            if aba_filter is not None:
UI/models/ui_data.py:333:                where.append("t.aba = ?")
UI/models/ui_data.py:334:                params.append(str(aba_filter))
UI/models/ui_data.py:336:            if filters.get("decision"):
UI/models/ui_data.py:337:                where.append("t.decision = ?")
UI/models/ui_data.py:338:                params.append(filters["decision"])
UI/models/ui_data.py:351:                t.timestamp, t.structure_id, t.aba, t.decision, t.level,
UI/models/ui_data.py:370:            if item.get("structure_id") is None and item.get("aba") is not None:
UI/models/ui_data.py:372:                    item["structure_id"] = int(item["aba"])
UI/models/ui_data.py:376:            if item.get("aba") is None and item.get("structure_id") is not None:
UI/models/ui_data.py:377:                item["aba"] = str(item["structure_id"])
UI/models/ui_data.py:401:    def get_payoff_curve(self, structure_id: str, timestamp: str) -> List[Dict]:
UI/models/ui_data.py:404:        Aceita structure_id como inteiro ou string numerica ("7").
UI/models/ui_data.py:408:        cache_key = (str(structure_id), ts_key)
UI/models/ui_data.py:410:        if hasattr(self, "_payoff_cache") and cache_key in self._payoff_cache:
UI/models/ui_data.py:411:            cached = self._payoff_cache[cache_key]
UI/models/ui_data.py:417:        if not self._payoff_table:
UI/models/ui_data.py:419:                "Tabela de payoff não encontrada. Esperadas: "
UI/models/ui_data.py:420:                + ", ".join(CANDIDATE_PAYOFF_TABLES)
UI/models/ui_data.py:424:        p = self._payoff_cols
UI/models/ui_data.py:429:                f"Tabela {self._payoff_table} não possui colunas esperadas para payoff."
UI/models/ui_data.py:433:        # alteracao_34: structure_id e sempre INTEGER
UI/models/ui_data.py:435:        filter_val = self._resolve_structure_key(structure_id)
UI/models/ui_data.py:439:            FROM {self._payoff_table}
UI/models/ui_data.py:452:            FROM {self._payoff_table}
UI/models/ui_data.py:466:            FROM {self._payoff_table}
UI/models/ui_data.py:476:    def get_payoff_curve_info(
UI/models/ui_data.py:477:        self, structure_id: str, timestamp: str
UI/models/ui_data.py:480:         alteracao_33: usa structure_id como chave primária quando disponível.
UI/models/ui_data.py:481:        Fallback para aba mantido para compatibilidade.
UI/models/ui_data.py:487:        if not self._payoff_table:
UI/models/ui_data.py:491:        cache_key = (str(structure_id), ts_key)
UI/models/ui_data.py:502:        p = self._payoff_cols
UI/models/ui_data.py:504:        # alteracao_34: structure_id e sempre INTEGER
UI/models/ui_data.py:509:            filter_val = self._resolve_structure_key(structure_id)
UI/models/ui_data.py:511:                "structure_id": structure_id,
UI/models/ui_data.py:512:                "aba": structure_id,   #  patch_3a: aba espelha structure_id (compat)
UI/models/ui_data.py:516:                "source_table": self._payoff_table,
UI/models/ui_data.py:524:            if self._payoff_table == "payoff_curve_points":
UI/models/ui_data.py:527:                if "meta_json" in self._inspect_columns("payoff_curve_points"):
UI/models/ui_data.py:532:                    f"FROM payoff_curve_points "
UI/models/ui_data.py:541:                        f"SELECT timestamp FROM payoff_curve_points "
UI/models/ui_data.py:562:                        f"Tabela {self._payoff_table} não possui colunas esperadas."
UI/models/ui_data.py:567:                    f"FROM {self._payoff_table} "
UI/models/ui_data.py:576:                        f"SELECT {p['timestamp']} AS ts FROM {self._payoff_table} "
UI/models/ui_data.py:603:                "timestamp", "structure_id", "aba", "decision", "level",
UI/models/ui_data.py:622:    def check_database_status(self) -> str:
UI/models/ui_data.py:639:        payoff_ok = bool(self._payoff_table)
UI/models/ui_data.py:642:        p = self._payoff_cols
UI/models/ui_data.py:653:            f"Tabela de payoff: {self._payoff_table if payoff_ok else 'NÃO ENCONTRADA'}\n"
UI/models/ui_data.py:659:        self._payoff_cache = {}
UI/models/ui_data.py:667:            return self._payoff_cache.get(key)
UI/models/ui_data.py:673:            self._payoff_cache[key] = value
UI/models/ui_data.py:674:            mx = getattr(self, "_payoff_cache_max", 0) or 0
UI/models/ui_data.py:675:            if mx > 0 and len(self._payoff_cache) > mx:
UI/models/ui_data.py:676:                self._payoff_cache.pop(next(iter(self._payoff_cache)))
domain/decision.py:3:Domain: Decision logic (30/60/80 thresholds + DTE gate) from real data.
domain/decision.py:6:Funcoes canonicas: compute_decision_from_inputs, compute_decision_from_payoff,
domain/decision.py:7:compute_decision_from_contract.
domain/decision.py:19:# Constantes de decisão
domain/decision.py:32:def _interp_payoff(points: List[Tuple[float, float]], spot: float) -> float:
domain/decision.py:55:# Mapeamento decision  level
domain/decision.py:56:_DECISION_LEVEL = {
domain/decision.py:58:    "WATCH":        1,   # nível interno, mapeado para decision="HOLD" level=1
domain/decision.py:68:def compute_decision_from_inputs(
domain/decision.py:114:    decision = "HOLD" if _internal == "WATCH" else _internal
domain/decision.py:129:        "decision":      decision,
domain/decision.py:139:def compute_decision_from_payoff(
domain/decision.py:140:    payoff: Dict[str, Any],
domain/decision.py:147:    Decide a partir de um dict de payoff.
domain/decision.py:148:    Payoff vazio ou inválido  HOLD com 'error' em why_json.
domain/decision.py:150:    if not payoff:
domain/decision.py:151:        why_dict = {"error": "payoff vazio ou invalido", "reason": "invalid_input"}
domain/decision.py:153:            "decision":      "HOLD",
domain/decision.py:162:    pl_atual = payoff.get("pl_atual") or payoff.get("pl_now") or 0.0
domain/decision.py:163:    pl_max   = payoff.get("pl_max") or 0.0
domain/decision.py:166:    points = payoff.get("points") or []
domain/decision.py:167:    spot   = payoff.get("spot")
domain/decision.py:169:        pl_atual = _interp_payoff(points, float(spot))
domain/decision.py:174:            "decision":      "HOLD",
domain/decision.py:183:    return compute_decision_from_inputs(
domain/decision.py:193:def compute_decision_from_contract(
domain/decision.py:195:    payoff: Optional[Dict[str, Any]] = None,
domain/decision.py:201:    if payoff:
domain/decision.py:202:        return compute_decision_from_payoff(payoff=payoff, dte_min=dte_min)
domain/decision.py:209:    return compute_decision_from_inputs(
domain/payoff.py:27:def _compute_leg_payoff_at_expiration(leg: dict[str, Any], spot_at_expiration: float) -> float:
domain/payoff.py:43:    payoff_unit = intrinsic - premium_value
domain/payoff.py:46:        payoff_unit = -payoff_unit
domain/payoff.py:48:    return payoff_unit * quantity * multiplier
domain/payoff.py:51:def compute_payoff_curve_from_canonical_legs(
domain/payoff.py:90:            pl_total += _compute_leg_payoff_at_expiration(
domain/payoff.py:123:def compute_payoff_from_canonical_input(
domain/payoff.py:144:            "structure_id": structure.get("structure_id"),
domain/payoff.py:157:    result = compute_payoff_curve_from_canonical_legs(
domain/payoff.py:167:        "structure_id": structure.get("structure_id"),
domain/payoff_features.py:8:Patch 24: chave de upsert migrada de (timestamp, aba)
domain/payoff_features.py:9:          para (structure_id, reference_date).
domain/payoff_features.py:10:          aba e timestamp mantidos como colunas opcionais de rastreabilidade.
domain/payoff_features.py:99:    structure_id: Optional[str] = None,
domain/payoff_features.py:102:    aba: Optional[str] = None,
domain/payoff_features.py:106:    Computa features da curva de payoff.
domain/payoff_features.py:108:    Chave canônica : structure_id + reference_date   upsert no derived.db.
domain/payoff_features.py:109:    timestamp + aba                rastreabilidade opcional (legado RTD).
domain/payoff_features.py:127:        "structure_id":      structure_id,
domain/payoff_features.py:130:        "aba":               aba,
domain/payoff_features.py:146:    INSERT INTO payoff_curve_summary (
domain/payoff_features.py:147:        structure_id, reference_date,
domain/payoff_features.py:148:        timestamp, aba,
domain/payoff_features.py:155:        :structure_id, :reference_date,
domain/payoff_features.py:156:        :timestamp, :aba,
domain/payoff_features.py:163:    ON CONFLICT(structure_id, reference_date) DO UPDATE SET
domain/payoff_features.py:165:        aba                = excluded.aba,
domain/payoff_features.py:185:    Upsert por (structure_id, reference_date) -- chave canônica.
domain/payoff_features.py:187:    Patch 24: substituída chave legada (timestamp, aba)
domain/payoff_features.py:188:              pela chave canônica (structure_id, reference_date).
domain/payoff_features.py:189:              As colunas aba e timestamp permanecem na tabela como
domain/payoff_features.py:203:    structure_id   = features.get("structure_id")
domain/payoff_features.py:206:    if not structure_id or not reference_date:
domain/payoff_features.py:208:            "features precisa de structure_id e reference_date para upsert canônico"
domain/payoff_features.py:219:                "structure_id":      structure_id,
domain/payoff_features.py:222:                "aba":               features.get("aba"),
repositories/system_snapshots_repository.py:16:    "payoff_json",
repositories/system_snapshots_repository.py:17:    "decision_json",
repositories/system_snapshots_repository.py:81:        structure_id: int,
repositories/system_snapshots_repository.py:90:        payoff_json: dict[str, Any] | list[Any] | None = None,
repositories/system_snapshots_repository.py:91:        decision_json: dict[str, Any] | list[Any] | None = None,
repositories/system_snapshots_repository.py:101:        if not structure_id:
repositories/system_snapshots_repository.py:102:            raise ValueError("structure_id é obrigatório")
repositories/system_snapshots_repository.py:115:                    structure_id,
repositories/system_snapshots_repository.py:123:                    payoff_json,
repositories/system_snapshots_repository.py:124:                    decision_json,
repositories/system_snapshots_repository.py:132:                    structure_id,
repositories/system_snapshots_repository.py:140:                    _to_json(payoff_json),
repositories/system_snapshots_repository.py:141:                    _to_json(decision_json),
repositories/system_snapshots_repository.py:153:                    structure_id=structure_id,
repositories/system_snapshots_repository.py:165:        structure_id: int,
repositories/system_snapshots_repository.py:173:                structure_id,
repositories/system_snapshots_repository.py:192:                structure_id,
repositories/system_snapshots_repository.py:243:        structure_id: int,
repositories/system_snapshots_repository.py:257:                WHERE structure_id = ?
repositories/system_snapshots_repository.py:261:                (structure_id, limit),
repositories/system_snapshots_repository.py:268:        structure_id: int,
repositories/system_snapshots_repository.py:272:        snapshots = self.list_snapshots_for_structure(structure_id, limit=1)
repositories/ui_data_table_candidates.py:12:    "structure_decisions",
repositories/ui_data_table_candidates.py:15:    "decisions",
repositories/ui_data_table_candidates.py:16:    "rtd_decisions",
repositories/ui_data_table_candidates.py:19:CANDIDATE_PAYOFF_TABLES = [
repositories/ui_data_table_candidates.py:20:    "payoff_curve_points",
repositories/ui_data_table_candidates.py:21:    "rtd_payoff_points",
repositories/ui_data_table_candidates.py:22:    "rtd_payoff_curva",
repositories/ui_data_table_candidates.py:23:    "payoff_points",
services/derived_payoff_persistence.py:1:# services/derived_payoff_persistence.py
services/derived_payoff_persistence.py:6:from domain.payoff import compute_payoff_from_canonical_input
services/derived_payoff_persistence.py:7:from services.derived_service import save_payoff_from_canonical_payload, save_decision_from_canonical_payload
services/derived_payoff_persistence.py:12:class DerivedPayoffPersistence:
services/derived_payoff_persistence.py:14:    Implementação concreta de PayoffPersistencePort.
services/derived_payoff_persistence.py:18:      2. Calcular a curva de payoff via domain/payoff.py
services/derived_payoff_persistence.py:20:      4. Persistir decisão básica derivada do resultado do engine
services/derived_payoff_persistence.py:24:    #  PayoffPersistencePort.persist()                                 #
services/derived_payoff_persistence.py:33:            logger.debug("derived_payoff_persistence: pricing_payload vazio, skip.")
services/derived_payoff_persistence.py:40:                "derived_payoff_persistence: status=%r não elegível para payoff, skip.",
services/derived_payoff_persistence.py:45:        # Timestamp único para payoff + decisão.
services/derived_payoff_persistence.py:49:        payoff_saved = self._persist_payoff(pricing_payload, result, snapshot_ts)
services/derived_payoff_persistence.py:50:        if not payoff_saved:
services/derived_payoff_persistence.py:52:                "derived_payoff_persistence: decisão não gravada porque payoff não foi salvo -- structure_id=%s",
services/derived_payoff_persistence.py:53:                pricing_payload.get("structure_id"),
services/derived_payoff_persistence.py:57:        decision_saved = self._persist_decision(pricing_payload, result, snapshot_ts)
services/derived_payoff_persistence.py:58:        if not decision_saved:
services/derived_payoff_persistence.py:60:                "derived_payoff_persistence: payoff salvo, mas decisão falhou -- structure_id=%s timestamp=%s",
services/derived_payoff_persistence.py:61:                pricing_payload.get("structure_id"),
services/derived_payoff_persistence.py:66:    #  payoff                                                          #
services/derived_payoff_persistence.py:69:    def _persist_payoff(
services/derived_payoff_persistence.py:77:            payoff_result = compute_payoff_from_canonical_input(canonical_input)
services/derived_payoff_persistence.py:79:            if not payoff_result.get("points"):
services/derived_payoff_persistence.py:81:                    "derived_payoff_persistence: payoff sem pontos para structure_id=%s",
services/derived_payoff_persistence.py:82:                    pricing_payload.get("structure_id"),
services/derived_payoff_persistence.py:86:            save_payoff_from_canonical_payload(payoff_result, timestamp=snapshot_ts)
services/derived_payoff_persistence.py:88:                "derived_payoff_persistence: %d pontos gravados -- structure_id=%s",
services/derived_payoff_persistence.py:89:                len(payoff_result["points"]),
services/derived_payoff_persistence.py:90:                pricing_payload.get("structure_id"),
services/derived_payoff_persistence.py:96:                "derived_payoff_persistence: erro ao gravar payoff -- structure_id=%s",
services/derived_payoff_persistence.py:97:                pricing_payload.get("structure_id"),
services/derived_payoff_persistence.py:102:    #  decisão                                                         #
services/derived_payoff_persistence.py:105:    def _persist_decision(
services/derived_payoff_persistence.py:136:            decision_dict = {
services/derived_payoff_persistence.py:137:                "decision":      "HOLD",
services/derived_payoff_persistence.py:151:                    "structure_id":    pricing_payload.get("structure_id"),
services/derived_payoff_persistence.py:158:            save_decision_from_canonical_payload(
services/derived_payoff_persistence.py:159:                decision=decision_dict,
services/derived_payoff_persistence.py:160:                structure_id=pricing_payload.get("structure_id"),
services/derived_payoff_persistence.py:166:                "derived_payoff_persistence: decisão gravada -- structure_id=%s",
services/derived_payoff_persistence.py:167:                pricing_payload.get("structure_id"),
services/derived_payoff_persistence.py:173:                "derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s",
services/derived_payoff_persistence.py:174:                pricing_payload.get("structure_id"),
services/derived_payoff_persistence.py:186:        Normaliza aliases de direção para o contrato canônico de payoff.
services/derived_payoff_persistence.py:188:        domain/payoff.py exige leg["position_side"].
services/derived_payoff_persistence.py:221:    def _normalize_leg_for_payoff(leg: Any) -> dict[str, Any]:
services/derived_payoff_persistence.py:224:        esperado por domain.compute_payoff_from_canonical_input().
services/derived_payoff_persistence.py:236:        normalized_side = DerivedPayoffPersistence._normalize_position_side(
services/derived_payoff_persistence.py:274:    def _normalize_canonical_input_for_payoff(
services/derived_payoff_persistence.py:278:        Retorna uma cópia rasa do canonical_input com legs normalizadas para payoff.
services/derived_payoff_persistence.py:288:            DerivedPayoffPersistence._normalize_leg_for_payoff(leg)
services/derived_payoff_persistence.py:292:        meta.setdefault("payoff_leg_normalization", "fase_3f_fix1_position_side_from_side")
services/derived_payoff_persistence.py:307:        Monta o canonical_input esperado por compute_payoff_from_canonical_input().
services/derived_payoff_persistence.py:311:          B) flat:        { legs: [...], spot_price: ..., structure_id: ..., ... }
services/derived_payoff_persistence.py:314:        # estrito de domain/payoff.py.
services/derived_payoff_persistence.py:316:            return DerivedPayoffPersistence._normalize_canonical_input_for_payoff(
services/derived_payoff_persistence.py:321:        structure_id   = pricing_payload.get("structure_id")
services/derived_payoff_persistence.py:331:        meta.setdefault("payoff_leg_normalization", "fase_3f_fix1_position_side_from_side")
services/derived_payoff_persistence.py:335:                "structure_id":    structure_id,
services/derived_payoff_persistence.py:339:                    DerivedPayoffPersistence._normalize_leg_for_payoff(leg)
services/derived_service.py:4:alteracao_30/alteracao_57c -- Servico de persistencia de dados derivados (payoff + decisoes).
services/derived_service.py:5:alteracao_62           -- AbaResolverMixin extraído para repositories/_aba_resolver_mixin.py.
services/derived_service.py:6:alteracao_65           -- get_payoff_by_aba() removida da interface pública (standalone).
services/derived_service.py:17:    cleanup_old_decisions,
services/derived_service.py:18:    cleanup_old_payoff_data,
services/derived_service.py:20:    insert_payoff_points,
services/derived_service.py:21:    insert_structure_decision,
services/derived_service.py:27:# Cache modulo-level: aba -> structure_id
services/derived_service.py:30:_ABA_TO_STRUCTURE_ID: Dict[str, int] = {}
services/derived_service.py:31:_ABA_CACHE_LOADED: bool = False
services/derived_service.py:34:def _load_aba_cache() -> None:
services/derived_service.py:35:    global _ABA_TO_STRUCTURE_ID, _ABA_CACHE_LOADED
services/derived_service.py:39:                SELECT id, alias_legacy_aba
services/derived_service.py:41:                WHERE alias_legacy_aba IS NOT NULL
services/derived_service.py:42:                  AND alias_legacy_aba != ''
services/derived_service.py:44:            _ABA_TO_STRUCTURE_ID = {row[1]: row[0] for row in cur.fetchall()}
services/derived_service.py:46:        _ABA_TO_STRUCTURE_ID = {}
services/derived_service.py:48:        _ABA_CACHE_LOADED = True
services/derived_service.py:51:def _resolve_structure_id(aba: Optional[str]) -> Optional[int]:
services/derived_service.py:52:    if not _ABA_CACHE_LOADED:
services/derived_service.py:53:        _load_aba_cache()
services/derived_service.py:54:    if not aba:
services/derived_service.py:56:    return _ABA_TO_STRUCTURE_ID.get(aba)
services/derived_service.py:59:def invalidate_aba_cache() -> None:
services/derived_service.py:60:    global _ABA_CACHE_LOADED
services/derived_service.py:61:    _ABA_CACHE_LOADED = False
services/derived_service.py:81:    alteracao_57: extrai string aba de StructureRef ou passa str diretamente.
services/derived_service.py:82:    Equivalente a _unwrap_aba do derived_repo, mas para a camada de servico.
services/derived_service.py:85:        return ref.aba
services/derived_service.py:90:    aba: Optional[str] = None,
services/derived_service.py:91:    structure_id: Any = None,
services/derived_service.py:95:    # 1. aba explícita tem prioridade máxima
services/derived_service.py:96:    resolved_aba = _safe_str(aba)
services/derived_service.py:97:    if resolved_aba:
services/derived_service.py:98:        return resolved_aba
services/derived_service.py:100:    # 2. structure_id → resolver alias_legacy_aba via cache (FIX alteracao_66)
services/derived_service.py:101:    resolved_sid = _safe_str(structure_id)
services/derived_service.py:105:            if not _ABA_CACHE_LOADED:
services/derived_service.py:106:                _load_aba_cache()
services/derived_service.py:107:            id_to_aba = {v: k for k, v in _ABA_TO_STRUCTURE_ID.items()}
services/derived_service.py:108:            alias = id_to_aba.get(sid_int)
services/derived_service.py:129:    structure_id: Any = None,
services/derived_service.py:138:        "structure_id":     structure_id,
services/derived_service.py:157:# Payoff
services/derived_service.py:160:def save_payoff_curve(
services/derived_service.py:166:    structure_id: Any = None,
services/derived_service.py:170:    _unwrap_ref() extrai a string aba de forma segura.
services/derived_service.py:175:        int(structure_id)
services/derived_service.py:176:        if structure_id is not None
services/derived_service.py:177:        else _resolve_structure_id(storage_key)
services/derived_service.py:194:        "structure_id": resolved_sid,
services/derived_service.py:199:        return insert_payoff_points(
services/derived_service.py:202:            aba=storage_key,
services/derived_service.py:206:            structure_id=resolved_sid,
services/derived_service.py:210:def save_payoff_from_canonical_payload(
services/derived_service.py:211:    payoff: Dict[str, Any],
services/derived_service.py:212:    aba: Optional[str] = None,
services/derived_service.py:218:        aba=aba,
services/derived_service.py:219:        structure_id=payoff.get("structure_id"),
services/derived_service.py:220:        structure_name=payoff.get("structure_name"),
services/derived_service.py:221:        underlying_asset=payoff.get("underlying_asset"),
services/derived_service.py:224:    sid_from_payload = payoff.get("structure_id")
services/derived_service.py:228:        else _resolve_structure_id(storage_key)
services/derived_service.py:232:        meta=payoff.get("meta"),
services/derived_service.py:233:        structure_id=resolved_sid,
services/derived_service.py:234:        structure_name=payoff.get("structure_name"),
services/derived_service.py:235:        underlying_asset=payoff.get("underlying_asset"),
services/derived_service.py:236:        reference_date=payoff.get("reference_date"),
services/derived_service.py:237:        input_meta=payoff.get("input_meta"),
services/derived_service.py:242:        sig = inspect.signature(save_payoff_curve)
services/derived_service.py:243:        accepts_structure_id = (
services/derived_service.py:244:            "structure_id" in sig.parameters
services/derived_service.py:251:        accepts_structure_id = True
services/derived_service.py:253:    if accepts_structure_id:
services/derived_service.py:254:        return save_payoff_curve(
services/derived_service.py:256:            points=payoff.get("points", []),
services/derived_service.py:257:            spot_ref=payoff.get("spot_ref"),
services/derived_service.py:260:            structure_id=resolved_sid,
services/derived_service.py:263:    return save_payoff_curve(
services/derived_service.py:265:        points=payoff.get("points", []),
services/derived_service.py:266:        spot_ref=payoff.get("spot_ref"),
services/derived_service.py:273:def save_decision(
services/derived_service.py:275:    decision: Dict[str, Any],
services/derived_service.py:277:    structure_id: Any = None,
services/derived_service.py:283:    - Preserva structure_id explícito recebido por argumento, pelo payload
services/derived_service.py:285:    - Só tenta resolver por storage_key/alias quando não há structure_id explícito.
services/derived_service.py:290:    explicit_sid = structure_id
services/derived_service.py:292:        explicit_sid = decision.get("structure_id")
services/derived_service.py:294:        explicit_sid = (decision.get("meta") or {}).get("structure_id")
services/derived_service.py:299:        else _resolve_structure_id(storage_key)
services/derived_service.py:302:    enriched_decision = {
services/derived_service.py:303:        **decision,
services/derived_service.py:304:        "structure_id": resolved_sid,
services/derived_service.py:306:            **(decision.get("meta") or {}),
services/derived_service.py:308:            "structure_id": resolved_sid,
services/derived_service.py:314:        return insert_structure_decision(
services/derived_service.py:317:            aba=storage_key,
services/derived_service.py:318:            decision_dict=enriched_decision,
services/derived_service.py:322:def save_decision_from_canonical_payload(
services/derived_service.py:323:    decision: Dict[str, Any],
services/derived_service.py:324:    structure_id: Any = None,
services/derived_service.py:327:    aba: Optional[str] = None,
services/derived_service.py:333:        aba=aba,
services/derived_service.py:334:        structure_id=structure_id,
services/derived_service.py:340:        int(structure_id)
services/derived_service.py:341:        if structure_id is not None
services/derived_service.py:342:        else _resolve_structure_id(storage_key)
services/derived_service.py:345:    enriched_decision = {
services/derived_service.py:346:        **decision,
services/derived_service.py:347:        "structure_id": resolved_sid,
services/derived_service.py:349:            **(decision.get("meta") or {}),
services/derived_service.py:350:            "structure_id":     resolved_sid,
services/derived_service.py:357:    return save_decision(
services/derived_service.py:359:        decision=enriched_decision,
services/derived_service.py:371:        deleted_payoff = cleanup_old_payoff_data(conn, days_to_keep=days_to_keep)
services/derived_service.py:372:        deleted_dec    = cleanup_old_decisions(conn, days_to_keep=days_to_keep)
services/derived_service.py:373:        return {"payoff_deleted": deleted_payoff, "decisions_deleted": deleted_dec}
services/derived_service.py:380:def get_all_payoff_curves():
services/derived_service.py:384:            SELECT timestamp, aba, point_spot, point_pl, meta_json
services/derived_service.py:385:            FROM payoff_curve_points
services/derived_service.py:391:                "aba":        row[1],
services/derived_service.py:400:def get_payoff_by_structure_id(structure_id: int):
services/derived_service.py:402:    alteracao_56/alteracao_65: único ponto de entrada canônico para leitura de payoff.
services/derived_service.py:405:    Importante: payoff_curve_points mantém histórico por timestamp.
services/derived_service.py:408:    ref = StructureRef.from_id(structure_id)
services/derived_service.py:416:              FROM payoff_curve_points
services/derived_service.py:420:                      FROM payoff_curve_points
services/derived_service.py:439:def get_recent_decisions():
services/derived_service.py:447:                "PRAGMA table_info(structure_decisions)"
services/derived_service.py:452:            "timestamp", "aba", "decision", "level",
services/derived_service.py:456:        if "structure_id" in cols:
services/derived_service.py:457:            select_cols.append("structure_id")
services/derived_service.py:465:            FROM structure_decisions
services/derived_service.py:470:        decisions = []
services/derived_service.py:491:            if item.get("structure_id") is None:
services/derived_service.py:498:                        sid = parsed.get("structure_id")
services/derived_service.py:500:                            item["structure_id"] = sid
services/derived_service.py:505:            decisions.append(item)
services/derived_service.py:507:        return decisions
services/derived_service.py:511:# alteracao_59 -- format_report + snapshot_aba (surface canônica)
services/derived_service.py:515:    """Formata relatório de auditoria de surface ABA em texto legível."""
services/derived_service.py:518:        aba_str = getattr(e, "aba_str", str(getattr(e, "structure_id", "")))
services/derived_service.py:519:        sid     = getattr(e, "structure_id", "?")
services/derived_service.py:521:        lines.append(f"{sid} | {ref} | {aba_str}")
services/derived_service.py:525:def snapshot_aba(ref: "StructureRef") -> str:
services/derived_service.py:526:    """Retorna aba_str canônico a partir de um StructureRef."""
services/derived_service.py:527:    aba_str = ref.aba if hasattr(ref, "aba") and ref.aba else str(ref.structure_id)
services/derived_service.py:528:    return aba_str
services/derived_service.py:533:# get_payoff_by_aba() removida da interface pública.
services/derived_service.py:534:# get_payoff_by_structure_id() é o único ponto de entrada canônico.
services/derived_service.py:539:    alteracao_65: get_payoff_by_aba() nao exposta -- use get_payoff_by_structure_id().
services/derived_service.py:540:    get_payoff_by_aba() ausente por decisao de design (alteracao_65): interface simplificada.
services/derived_service.py:543:    # alteracao_65: get_payoff_by_aba() deliberadamente nao implementada nesta classe.
services/derived_service.py:544:    # Chamadores legados devem migrar para get_payoff_by_structure_id().
services/derived_service.py:546:    def get_payoff_by_structure_id(self, structure_id: int):
services/derived_service.py:547:        """Retorna pontos de payoff para a estrutura informada."""
services/derived_service.py:548:        return get_payoff_by_structure_id(structure_id)
services/derived_service.py:550:    def save_payoff_curve(self, *args, **kwargs):
services/derived_service.py:551:        return save_payoff_curve(*args, **kwargs)
services/derived_service.py:553:    def save_decision(self, *args, **kwargs):
services/derived_service.py:554:        return save_decision(*args, **kwargs)
services/payoff_persistence_port.py:1:# services/payoff_persistence_port.py
services/payoff_persistence_port.py:5:class PayoffPersistencePort(Protocol):
services/payoff_persistence_port.py:7:    Contrato de persistência derivada (payoff + decisão).
services/payoff_pricing_engine.py:3:from domain.payoff import compute_payoff_curve_from_canonical_legs
services/payoff_pricing_engine.py:7:class PayoffPricingEngine:
services/payoff_pricing_engine.py:9:    Motor financeiro inicial baseado na curva de payoff canônica.
services/payoff_pricing_engine.py:18:    engine_name = "payoff_pricing_engine"
services/payoff_pricing_engine.py:40:        payoff = compute_payoff_curve_from_canonical_legs(
services/payoff_pricing_engine.py:48:        pl_max = payoff.get("pl_max")
services/payoff_pricing_engine.py:49:        pl_min = payoff.get("pl_min")
services/payoff_pricing_engine.py:63:            "structure_id": pricing_payload.get("structure_id"),
services/payoff_pricing_engine.py:72:                "payoff_points": len(payoff.get("points") or []),
services/payoff_pricing_engine.py:85:                "method": "expiration_payoff_grid",
services/payoff_pricing_engine.py:87:            "payoff": payoff,
services/pricing_execution_app_service.py:9:  - Validações _validate_structure_id / _validate_reference_date mantidas
services/pricing_execution_app_service.py:42:        structure_id: int,
services/pricing_execution_app_service.py:45:        self._validate_structure_id(structure_id)
services/pricing_execution_app_service.py:49:            structure_id=structure_id,
services/pricing_execution_app_service.py:71:        structure_id: int | None = None,
services/pricing_execution_app_service.py:78:            structure_id=structure_id,
services/pricing_execution_app_service.py:87:        structure_id: int | None = None,
services/pricing_execution_app_service.py:93:            structure_id=structure_id,
services/pricing_execution_app_service.py:104:        structure_id: int | None = None,
services/pricing_execution_app_service.py:113:            structure_id=structure_id,
services/pricing_execution_app_service.py:126:    def _validate_structure_id(self, structure_id: int) -> None:
services/pricing_execution_app_service.py:127:        if structure_id <= 0:
services/pricing_execution_app_service.py:128:            raise ValueError("structure_id must be greater than zero")
services/pricing_execution_orchestration_service.py:4:from repositories.system_snapshots_repository import SystemSnapshotsRepository
services/pricing_execution_orchestration_service.py:26:                system_snapshots_repository=SystemSnapshotsRepository(),
services/pricing_execution_orchestration_service.py:32:        structure_id: int,
services/pricing_execution_orchestration_service.py:39:                structure_id=structure_id,
services/pricing_execution_orchestration_service.py:64:                    "engine": "payoff_pricing_engine",
services/pricing_execution_persistence_service.py:6:from repositories.system_snapshots_repository import SystemSnapshotsRepository
services/pricing_execution_persistence_service.py:7:from services.payoff_persistence_port import PayoffPersistencePort
services/pricing_execution_persistence_service.py:16:        payoff_persistence_port: PayoffPersistencePort | None = None,
services/pricing_execution_persistence_service.py:17:        system_snapshots_repository: SystemSnapshotsRepository | None = None,
services/pricing_execution_persistence_service.py:22:        self._payoff_port = payoff_persistence_port
services/pricing_execution_persistence_service.py:23:        self._system_snapshots_repository = system_snapshots_repository
services/pricing_execution_persistence_service.py:67:        #  alteracao_21 -- persistência derivada (payoff + decisão)           #
services/pricing_execution_persistence_service.py:70:        if self._payoff_port is not None:
services/pricing_execution_persistence_service.py:72:                self._payoff_port.persist(
services/pricing_execution_persistence_service.py:78:                    "payoff_persistence_port.persist() falhou -- execução id=%s não afetada",
services/pricing_execution_persistence_service.py:100:        if self._system_snapshots_repository is None:
services/pricing_execution_persistence_service.py:109:        structure_id = pricing_payload.get("structure_id") or record.get("structure_id")
services/pricing_execution_persistence_service.py:110:        if not structure_id:
services/pricing_execution_persistence_service.py:114:            return self._system_snapshots_repository.create_snapshot(
services/pricing_execution_persistence_service.py:115:                structure_id=int(structure_id),
services/pricing_execution_persistence_service.py:124:                payoff_json=self._extract_result_field(inner, "payoff"),
services/pricing_execution_persistence_service.py:125:                decision_json=self._extract_result_field(inner, "decision"),
services/pricing_execution_persistence_service.py:135:                "system_snapshots_repository.create_snapshot() falhou -- execução id=%s não afetada",
services/pricing_execution_persistence_service.py:143:            "structure_id": pricing_payload.get("structure_id"),
services/pricing_execution_query_service.py:18:        structure_id: int | None = None,
services/pricing_execution_query_service.py:23:        if structure_id is not None and structure_id <= 0:
services/pricing_execution_query_service.py:24:            raise ValueError("structure_id must be greater than zero")
services/pricing_execution_query_service.py:48:        structure_id: int | None = None,
services/pricing_execution_query_service.py:62:                structure_id=structure_id,
services/pricing_execution_query_service.py:77:        structure_id: int | None = None,
services/pricing_execution_query_service.py:84:            structure_id=structure_id,
services/pricing_execution_query_service.py:91:            structure_id=structure_id,
services/pricing_execution_query_service.py:110:                "structure_id": execution["structure_id"],
services/pricing_execution_query_service.py:134:            if structure_id is not None and summary["structure_id"] != structure_id:
services/pricing_execution_query_service.py:154:        structure_id: int | None = None,
services/pricing_execution_query_service.py:163:            structure_id=structure_id,
services/pricing_execution_query_service.py:176:            structure_id=structure_id,
services/pricing_execution_query_service.py:202:        structure_id: int | None = None,
services/pricing_execution_query_service.py:208:            structure_id=structure_id,
services/pricing_execution_query_service.py:215:            structure_id=structure_id,
services/structure_analysis_service.py:6:from domain.decision import compute_decision_from_payoff
services/structure_analysis_service.py:7:from domain.payoff import compute_payoff_from_canonical_input
services/structure_analysis_service.py:20:        structure_id: int,
services/structure_analysis_service.py:30:            structure_id=structure_id,
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
services/structure_analysis_service.py:95:        # 8. Computa decisão -- passa TODOS os parâmetros como keyword
services/structure_analysis_service.py:96:        decision = compute_decision_from_payoff(
services/structure_analysis_service.py:97:            payoff=payoff,
services/structure_analysis_service.py:105:        decision["dte_min"] = dte_min_effective
services/structure_analysis_service.py:108:        decision["why"]["dte_gate"] = dte_gate
services/structure_analysis_service.py:119:            "payoff":   payoff,
services/structure_analysis_service.py:120:            "decision": decision,

## Ocorrencias criticas em testes Fase 4
ATT/tests/test_decision.py:1:from domain.decision import compute_decision_from_payoff
ATT/tests/test_decision.py:4:def test_compute_decision_from_payoff_should_work_without_alias_legacy_aba():
ATT/tests/test_decision.py:6:    Garante que compute_decision_from_payoff funciona com payoff canônico
ATT/tests/test_decision.py:7:    que não carrega alias_legacy_aba -- substitui o teste de contract com dict.
ATT/tests/test_decision.py:9:    payoff = {
ATT/tests/test_decision.py:17:    result = compute_decision_from_payoff(
ATT/tests/test_decision.py:18:        payoff=payoff,
ATT/tests/test_decision.py:22:    assert "decision" in result
ATT/tests/test_decision.py:24:    assert result["decision"] in ("HOLD", "WATCH", "PREPARE", "PREPARE_ROLL", "CLOSE_REOPEN", "CLOSE")
ATT/tests/test_decision.py:26:    # com dte_min=12 > dte_gate=7 não há gate, decisão depende do ratio
ATT/tests/test_derived_service.py:13:def test_resolve_storage_key_should_prefer_aba_when_present():
ATT/tests/test_derived_service.py:15:        aba="BOVA11",
ATT/tests/test_derived_service.py:16:        structure_id=7,
ATT/tests/test_derived_service.py:24:def test_resolve_storage_key_should_fallback_to_structure_id():
ATT/tests/test_derived_service.py:26:        aba=None,
ATT/tests/test_derived_service.py:27:        structure_id=7,
ATT/tests/test_derived_service.py:37:        aba=None,
ATT/tests/test_derived_service.py:38:        structure_id=None,
ATT/tests/test_derived_service.py:48:        aba=None,
ATT/tests/test_derived_service.py:49:        structure_id=None,
ATT/tests/test_derived_service.py:59:        aba=None,
ATT/tests/test_derived_service.py:60:        structure_id=None,
ATT/tests/test_derived_service.py:71:        structure_id=7,
ATT/tests/test_derived_service.py:79:    assert result["structure_id"] == 7
ATT/tests/test_derived_service.py:86:def test_save_payoff_from_canonical_payload_should_use_resolved_storage_key(monkeypatch):
ATT/tests/test_derived_service.py:89:    def fake_save_payoff_curve(ref, points, spot_ref=None, meta=None, timestamp=None):
ATT/tests/test_derived_service.py:90:        captured["aba"] = ref
ATT/tests/test_derived_service.py:97:    monkeypatch.setattr(ds, "save_payoff_curve", fake_save_payoff_curve)
ATT/tests/test_derived_service.py:100:        "structure_id": 99,
ATT/tests/test_derived_service.py:110:    result = ds.save_payoff_from_canonical_payload(payload)
ATT/tests/test_derived_service.py:113:    assert captured["aba"] == "structure:99"
ATT/tests/test_derived_service.py:117:    assert captured["meta"]["structure_id"] == 99
ATT/tests/test_derived_service.py:125:def test_save_decision_from_canonical_payload_should_enrich_meta(monkeypatch):
ATT/tests/test_derived_service.py:128:    def fake_save_decision(ref, decision, timestamp=None):
ATT/tests/test_derived_service.py:129:        captured["aba"] = ref
ATT/tests/test_derived_service.py:130:        captured["decision"] = decision
ATT/tests/test_derived_service.py:134:    monkeypatch.setattr(ds, "save_decision", fake_save_decision)
ATT/tests/test_derived_service.py:141:    result = ds.save_decision_from_canonical_payload(
ATT/tests/test_derived_service.py:142:        decision=payload,
ATT/tests/test_derived_service.py:143:        structure_id=321,
ATT/tests/test_derived_service.py:146:        aba=None,
ATT/tests/test_derived_service.py:150:    assert captured["aba"] == "structure:321"
ATT/tests/test_derived_service.py:151:    assert captured["decision"]["meta"]["origin"] == "test"
ATT/tests/test_derived_service.py:152:    assert captured["decision"]["meta"]["structure_id"] == 321
ATT/tests/test_derived_service.py:153:    assert captured["decision"]["meta"]["structure_name"] == "Fence"
ATT/tests/test_derived_service.py:154:    assert captured["decision"]["meta"]["underlying_asset"] == "VALE3"
ATT/tests/test_derived_service.py:155:    assert captured["decision"]["meta"]["storage_key"] == "structure:321"
ATT/tests/test_derived_service.py:159:def test_save_decision_preserva_structure_id_explicito_sem_alias(monkeypatch):
ATT/tests/test_derived_service.py:171:    def fake_insert_structure_decision(conn, timestamp, aba, decision_dict):
ATT/tests/test_derived_service.py:173:        captured["aba"] = aba
ATT/tests/test_derived_service.py:174:        captured["decision_dict"] = decision_dict
ATT/tests/test_derived_service.py:179:    monkeypatch.setattr(svc, "_resolve_structure_id", lambda storage_key: None)
ATT/tests/test_derived_service.py:180:    monkeypatch.setattr(svc, "insert_structure_decision", fake_insert_structure_decision)
ATT/tests/test_derived_service.py:182:    result = svc.save_decision(
ATT/tests/test_derived_service.py:184:        decision={
ATT/tests/test_derived_service.py:185:            "structure_id": 7,
ATT/tests/test_derived_service.py:186:            "decision": "hold",
ATT/tests/test_derived_service.py:193:    assert captured["aba"] == "structure:7"
ATT/tests/test_derived_service.py:194:    assert captured["decision_dict"]["structure_id"] == 7
ATT/tests/test_derived_service.py:195:    assert captured["decision_dict"]["meta"]["structure_id"] == 7
ATT/tests/test_derived_service.py:196:    assert captured["decision_dict"]["meta"]["storage_key"] == "structure:7"
ATT/tests/test_orchestrator_run_methods.py:2:Testes para os métodos run_payoff e run_decision
ATT/tests/test_orchestrator_run_methods.py:16:    _request_to_payoff_dict,
ATT/tests/test_orchestrator_run_methods.py:17:    run_decision,
ATT/tests/test_orchestrator_run_methods.py:18:    run_payoff,
ATT/tests/test_orchestrator_run_methods.py:48:        structure_id="struct-001",
ATT/tests/test_orchestrator_run_methods.py:64:# Testes: _request_to_payoff_dict
ATT/tests/test_orchestrator_run_methods.py:67:class TestRequestToPayoffDict:
ATT/tests/test_orchestrator_run_methods.py:71:        result = _request_to_payoff_dict(req)
ATT/tests/test_orchestrator_run_methods.py:76:        s = _request_to_payoff_dict(req)["structure"]
ATT/tests/test_orchestrator_run_methods.py:77:        assert s["structure_id"] == "struct-001"
ATT/tests/test_orchestrator_run_methods.py:86:        legs = _request_to_payoff_dict(req)["structure"]["legs"]
ATT/tests/test_orchestrator_run_methods.py:93:        m = _request_to_payoff_dict(req)["market"]
ATT/tests/test_orchestrator_run_methods.py:100:        result = _request_to_payoff_dict(req, extra_meta=meta)
ATT/tests/test_orchestrator_run_methods.py:105:        result = _request_to_payoff_dict(req)
ATT/tests/test_orchestrator_run_methods.py:114:        result_legs = _request_to_payoff_dict(req)["structure"]["legs"]
ATT/tests/test_orchestrator_run_methods.py:120:# Testes: run_payoff
ATT/tests/test_orchestrator_run_methods.py:123:class TestRunPayoff:
ATT/tests/test_orchestrator_run_methods.py:125:    @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input")
ATT/tests/test_orchestrator_run_methods.py:130:        result = run_payoff(req)
ATT/tests/test_orchestrator_run_methods.py:134:        assert canonical["structure"]["structure_id"] == "struct-001"
ATT/tests/test_orchestrator_run_methods.py:138:    @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input")
ATT/tests/test_orchestrator_run_methods.py:143:        run_payoff(req, low_pct=0.8, high_pct=1.2, step_pct=0.005)
ATT/tests/test_orchestrator_run_methods.py:150:    @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input")
ATT/tests/test_orchestrator_run_methods.py:155:        run_payoff(req, extra_meta={"tag": "ci"})
ATT/tests/test_orchestrator_run_methods.py:160:    @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input")
ATT/tests/test_orchestrator_run_methods.py:166:        result = run_payoff(req)
ATT/tests/test_orchestrator_run_methods.py:172:# Testes: run_decision
ATT/tests/test_orchestrator_run_methods.py:175:class TestRunDecision:
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
ATT/tests/test_orchestrator_run_methods.py:239:class TestRunPayoffIntegration:
ATT/tests/test_orchestrator_run_methods.py:241:    Chama run_payoff sem mock.
ATT/tests/test_orchestrator_run_methods.py:245:    def test_sanidade_run_payoff_call_chain(self):
ATT/tests/test_orchestrator_run_methods.py:246:        pytest.importorskip("domain.payoff")
ATT/tests/test_orchestrator_run_methods.py:260:            result = run_payoff(req, low_pct=0.8, high_pct=1.2, step_pct=0.05)
ATT/tests/test_orchestrator_run_methods.py:261:            assert isinstance(result, dict), "run_payoff deve retornar dict"
ATT/tests/test_payoff_canonical.py:1:from domain.payoff import compute_payoff_from_canonical_input
ATT/tests/test_payoff_canonical.py:4:def test_compute_payoff_from_canonical_input_should_preserve_canonical_metadata():
ATT/tests/test_payoff_canonical.py:7:            "structure_id": 7,
ATT/tests/test_payoff_canonical.py:37:    result = compute_payoff_from_canonical_input(canonical_input)
ATT/tests/test_payoff_canonical.py:39:    assert result["structure_id"] == 7
ATT/tests/test_payoff_chart.py:1:# C:/users/eucal/projeto/ATT/tests/test_payoff_chart.py
ATT/tests/test_payoff_chart.py:3:Testes unitários para UI/components/payoff_chart.py
ATT/tests/test_payoff_chart.py:9:  - PayoffChart.clear()
ATT/tests/test_payoff_chart.py:10:  - PayoffChart.update_chart()
ATT/tests/test_payoff_chart.py:11:  - PayoffChart.fix_current_curve() / clear_comparison()
ATT/tests/test_payoff_chart.py:12:  - PayoffChart.get_last_overlays()
ATT/tests/test_payoff_chart.py:51:from UI.components.payoff_chart import (  # noqa: E402
ATT/tests/test_payoff_chart.py:52:    PayoffChart,
ATT/tests/test_payoff_chart.py:60:# Fixture: instância de PayoffChart com Tk fake
ATT/tests/test_payoff_chart.py:63:def _make_chart() -> PayoffChart:
ATT/tests/test_payoff_chart.py:64:    """Cria PayoffChart com dependências Tk mockadas."""
ATT/tests/test_payoff_chart.py:65:    with patch("UI.components.payoff_chart.FigureCanvasTkAgg"), \
ATT/tests/test_payoff_chart.py:66:         patch("UI.components.payoff_chart.NavigationToolbar2Tk"), \
ATT/tests/test_payoff_chart.py:67:         patch("UI.components.payoff_chart.Figure") as MockFig, \
ATT/tests/test_payoff_chart.py:68:         patch("UI.components.payoff_chart.ttk.Frame.__init__", return_value=None), \
ATT/tests/test_payoff_chart.py:69:         patch("UI.components.payoff_chart.ttk.Frame.pack",     return_value=None), \
ATT/tests/test_payoff_chart.py:70:         patch("UI.components.payoff_chart.ttk.Frame.bind",     return_value=None):
ATT/tests/test_payoff_chart.py:77:        chart = PayoffChart.__new__(PayoffChart)
ATT/tests/test_payoff_chart.py:85:        chart._last_decision_data  = {}
ATT/tests/test_payoff_chart.py:171:        return PayoffChart._find_breakevens(spots, pls)
ATT/tests/test_payoff_chart.py:225:        return PayoffChart._interp_y_at_x(xs, ys, x)
ATT/tests/test_payoff_chart.py:305:# Testes de PayoffChart (estado e lógica)
ATT/tests/test_payoff_chart.py:308:class TestPayoffChartState(unittest.TestCase):
ATT/tests/test_payoff_chart.py:332:    def test_update_chart_saves_decision_data(self):
ATT/tests/test_payoff_chart.py:334:        dd  = {"structure_id": "collar_1", "decision": "BUY", "spot_ref": 100.0}
ATT/tests/test_payoff_chart.py:335:        self.chart.update_chart(pts, decision_data=dd)
ATT/tests/test_payoff_chart.py:336:        self.assertEqual(self.chart._last_decision_data["structure_id"], "collar_1")
ATT/tests/test_payoff_chart.py:352:        result = self.chart.update_chart(pts, decision_data={"spot_ref": 100.0})
ATT/tests/test_payoff_chart.py:357:        result = self.chart.update_chart(_linear_points(), decision_data={})
ATT/tests/test_payoff_chart.py:393:    def test_title_uses_structure_id(self):
ATT/tests/test_payoff_chart.py:395:        dd  = {"structure_id": "strangle_X", "aba": "old_aba", "decision": "BUY"}
ATT/tests/test_payoff_chart.py:396:        self.chart.update_chart(pts, decision_data=dd)
ATT/tests/test_payoff_chart.py:400:    def test_title_fallback_to_aba(self):
ATT/tests/test_payoff_chart.py:402:        dd  = {"aba": "straddle_Y", "decision": "SELL"}
ATT/tests/test_payoff_chart.py:403:        self.chart.update_chart(pts, decision_data=dd)
ATT/tests/test_payoff_chart.py:422:class TestPayoffChartRobustness(unittest.TestCase):
ATT/tests/test_payoff_chart.py:427:    def test_update_chart_none_decision_data(self):
ATT/tests/test_payoff_chart.py:428:        result = self.chart.update_chart(_linear_points(), decision_data=None)
ATT/tests/test_payoff_chart.py:456:            PayoffChart._find_breakevens(list(range(10)), [100.0] * 10), []
ATT/tests/test_payoff_chart.py:460:        self.assertEqual(PayoffChart._find_breakevens([100.0], [0.0]), [])
ATT/tests/test_payoff_chart.py:463:        result = PayoffChart._interp_y_at_x([100.0, 100.0], [0.0, 500.0], 100.0)
ATT/tests/test_payoff_pricing_engine.py:3:from services.payoff_pricing_engine import PayoffPricingEngine
ATT/tests/test_payoff_pricing_engine.py:6:def test_run_returns_payoff_based_metrics_and_valuation():
ATT/tests/test_payoff_pricing_engine.py:7:    engine = PayoffPricingEngine()
ATT/tests/test_payoff_pricing_engine.py:10:        "structure_id": 123,
ATT/tests/test_payoff_pricing_engine.py:30:    assert result["engine"] == "payoff_pricing_engine"
ATT/tests/test_payoff_pricing_engine.py:32:    assert result["structure_id"] == 123
ATT/tests/test_payoff_pricing_engine.py:41:    assert result["metrics"]["payoff_points"] == 101
ATT/tests/test_payoff_pricing_engine.py:51:    assert "payoff" in result
ATT/tests/test_payoff_pricing_engine.py:52:    assert len(result["payoff"]["points"]) == 101
ATT/tests/test_payoff_pricing_engine.py:56:    engine = PayoffPricingEngine()
ATT/tests/test_payoff_pricing_engine.py:59:        "structure_id": 123,
ATT/tests/test_payoff_pricing_engine.py:80:    assert result["metrics"]["payoff_points"] == 101
ATT/tests/test_payoff_pricing_engine.py:84:    engine = PayoffPricingEngine()
ATT/tests/test_payoff_pricing_engine.py:91:    engine = PayoffPricingEngine()
ATT/tests/test_payoff_pricing_engine.py:94:        "structure_id": 123,
ATT/tests/test_payoff_pricing_engine.py:108:    engine = PayoffPricingEngine()
ATT/tests/test_payoff_pricing_engine.py:111:        "structure_id": 123,
ATT/tests/test_pricing_execution_app_service.py:9:    def execute_pricing(self, structure_id: int, reference_date: str | None = None):
ATT/tests/test_pricing_execution_app_service.py:10:        self.calls.append({"structure_id": structure_id, "reference_date": reference_date})
ATT/tests/test_pricing_execution_app_service.py:18:    def list_execution_summaries(self, structure_id=None, underlying_asset=None,
ATT/tests/test_pricing_execution_app_service.py:21:            "structure_id": structure_id, "underlying_asset": underlying_asset,
ATT/tests/test_pricing_execution_app_service.py:26:    def get_latest_execution_summary(self, structure_id=None, underlying_asset=None,
ATT/tests/test_pricing_execution_app_service.py:29:            "structure_id": structure_id, "underlying_asset": underlying_asset,
ATT/tests/test_pricing_execution_app_service.py:38:    def paginate_execution_summaries(self, structure_id=None, underlying_asset=None,
ATT/tests/test_pricing_execution_app_service.py:42:            "structure_id": structure_id, "underlying_asset": underlying_asset,
ATT/tests/test_pricing_execution_app_service.py:59:        "persisted": {"record": {"id": 123, "structure_id": 10, "reference_date": "2026-05-16"}}
ATT/tests/test_pricing_execution_app_service.py:65:    result = service.execute_pricing(structure_id=10, reference_date="2026-05-16")
ATT/tests/test_pricing_execution_app_service.py:66:    assert result == {"id": 123, "structure_id": 10, "reference_date": "2026-05-16"}
ATT/tests/test_pricing_execution_app_service.py:67:    assert facade.calls == [{"structure_id": 10, "reference_date": "2026-05-16"}]
ATT/tests/test_pricing_execution_app_service.py:77:    result = service.execute_pricing(structure_id=11, reference_date="2026-05-16")
ATT/tests/test_pricing_execution_app_service.py:81:def test_execute_pricing_rejects_invalid_structure_id():
ATT/tests/test_pricing_execution_app_service.py:88:        service.execute_pricing(structure_id=0, reference_date="2026-05-16")
ATT/tests/test_pricing_execution_app_service.py:91:        assert str(exc) == "structure_id must be greater than zero"
ATT/tests/test_pricing_execution_app_service.py:102:        service.execute_pricing(structure_id=10, reference_date="16-05-2026")
ATT/tests/test_pricing_execution_app_service.py:117:    result = service.execute_pricing(structure_id=10, reference_date=None)
ATT/tests/test_pricing_execution_app_service.py:119:    assert facade.calls == [{"structure_id": 10, "reference_date": None}]
ATT/tests/test_pricing_execution_app_service.py:126:        structure_id=1, underlying_asset="PETR4",
ATT/tests/test_pricing_execution_app_service.py:131:        "structure_id": 1, "underlying_asset": "PETR4",
ATT/tests/test_pricing_execution_app_service.py:140:        structure_id=2, underlying_asset="VALE3",
ATT/tests/test_pricing_execution_app_service.py:145:        "structure_id": 2, "underlying_asset": "VALE3",
ATT/tests/test_pricing_execution_app_service.py:162:        structure_id=1, underlying_asset="PETR4",
ATT/tests/test_pricing_execution_app_service.py:169:        "structure_id": 1, "underlying_asset": "PETR4",
ATT/tests/test_pricing_execution_orchestration_service.py:7:    def build_pricing_payload(self, structure_id: int, reference_date: str | None = None):
ATT/tests/test_pricing_execution_orchestration_service.py:9:            "structure_id": structure_id,
ATT/tests/test_pricing_execution_orchestration_service.py:20:    def execute(self, structure_id: int, reference_date: str | None = None):
ATT/tests/test_pricing_execution_orchestration_service.py:23:                "structure_id": structure_id,
ATT/tests/test_pricing_execution_orchestration_service.py:33:                "structure_id": structure_id,
ATT/tests/test_pricing_execution_orchestration_service.py:82:        structure_id=123,
ATT/tests/test_pricing_execution_orchestration_service.py:88:            "structure_id": 123,
ATT/tests/test_pricing_execution_orchestration_service.py:93:    assert result["pricing_payload"]["structure_id"] == 123
ATT/tests/test_pricing_execution_orchestration_service.py:99:    assert persisted_call["pricing_payload"]["structure_id"] == 123
ATT/tests/test_pricing_execution_orchestration_service.py:115:        structure_id=999,
ATT/tests/test_pricing_execution_orchestration_service.py:121:            "structure_id": 999,
ATT/tests/test_pricing_execution_persistence_service.py:49:        "structure_id": 123,
ATT/tests/test_pricing_execution_persistence_service.py:186:        "structure_id": 123,
ATT/tests/test_pricing_execution_persistence_service.py:220:            "payoff": {
ATT/tests/test_pricing_execution_persistence_service.py:223:            "decision": {
ATT/tests/test_pricing_execution_persistence_service.py:247:    assert call["structure_id"] == 123
ATT/tests/test_pricing_execution_persistence_service.py:252:    assert call["structure_json"]["structure_id"] == 123
ATT/tests/test_pricing_execution_persistence_service.py:258:    assert call["payoff_json"] == {
ATT/tests/test_pricing_execution_persistence_service.py:261:    assert call["decision_json"] == {
ATT/tests/test_pricing_execution_persistence_service.py:316:            "structure_id": 123,
ATT/tests/test_pricing_execution_persistence_service.py:352:            "structure_id": 123,
ATT/tests/test_pricing_execution_query_service.py:20:    structure_id: int = 1,
ATT/tests/test_pricing_execution_query_service.py:37:        "structure_id": structure_id,
ATT/tests/test_pricing_execution_query_service.py:48:            "structure_id": structure_id,
ATT/tests/test_pricing_execution_query_service.py:147:def test_list_execution_summaries_filters_by_structure_id():
ATT/tests/test_pricing_execution_query_service.py:149:        make_execution(1, structure_id=10),
ATT/tests/test_pricing_execution_query_service.py:150:        make_execution(2, structure_id=20),
ATT/tests/test_pricing_execution_query_service.py:156:    summaries = service.list_execution_summaries(structure_id=20)
ATT/tests/test_pricing_execution_query_service.py:159:    assert summaries[0]["structure_id"] == 20
ATT/tests/test_pricing_execution_query_service.py:211:def test_list_execution_summaries_rejects_invalid_structure_id():
ATT/tests/test_pricing_execution_query_service.py:217:        service.list_execution_summaries(structure_id=0)
ATT/tests/test_pricing_execution_query_service.py:220:        assert str(exc) == "structure_id must be greater than zero"
ATT/tests/test_structure_analysis_service.py:13:        structure_id: int,
ATT/tests/test_structure_analysis_service.py:18:                "structure_id": structure_id,
ATT/tests/test_structure_analysis_service.py:28:                "structure_id": structure_id,
ATT/tests/test_structure_analysis_service.py:31:                "alias_legacy_aba": "BOVA11",
ATT/tests/test_structure_analysis_service.py:65:                "legacy_aba": "BOVA11",
ATT/tests/test_structure_analysis_service.py:77:        structure_id: int,
ATT/tests/test_structure_analysis_service.py:82:                "structure_id": structure_id,
ATT/tests/test_structure_analysis_service.py:89:                "structure_id": structure_id,
ATT/tests/test_structure_analysis_service.py:92:                "alias_legacy_aba": "BOVA11",
ATT/tests/test_structure_analysis_service.py:105:                "legacy_aba": "BOVA11",
ATT/tests/test_structure_analysis_service.py:117:        structure_id=1,
ATT/tests/test_structure_analysis_service.py:124:    assert "payoff" in result
ATT/tests/test_structure_analysis_service.py:125:    assert "decision" in result
ATT/tests/test_structure_analysis_service.py:127:    assert result["canonical_input"]["structure"]["structure_id"] == 1
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
ATT/tests/test_structure_analysis_service.py:158:        structure_id=1,
ATT/tests/test_structure_analysis_service.py:166:    assert result["decision"]["dte_min"] == 9
ATT/tests/test_structure_analysis_service.py:169:def test_structure_analysis_service_analyze_returns_structured_decision_for_invalid_payoff():
ATT/tests/test_structure_analysis_service.py:175:        structure_id=999,
ATT/tests/test_structure_analysis_service.py:179:    assert "payoff" in result
ATT/tests/test_structure_analysis_service.py:180:    assert "decision" in result
ATT/tests/test_structure_analysis_service.py:181:    assert result["decision"] is not None
ATT/tests/test_structure_analysis_service.py:182:    assert result["decision"]["decision"] == "HOLD"
ATT/tests/test_structure_analysis_service.py:183:    assert result["decision"]["level"] == 0
ATT/tests/test_structure_analysis_service.py:184:    assert result["decision"]["why"]["error"] == "payoff is required"
ATT/tests/test_structure_analysis_service.py:185:    assert "validation_errors" in result["decision"]["why"]
ATT/tests/test_structure_analysis_service.py:200:        structure_id=1,
ATT/tests/test_structure_analysis_service.py:206:    decision = result["decision"]
ATT/tests/test_structure_analysis_service.py:208:    assert decision is not None
ATT/tests/test_structure_analysis_service.py:209:    assert "why" in decision
ATT/tests/test_structure_analysis_service.py:210:    assert decision["why"]["thresholds_used"] == thresholds
ATT/tests/test_structure_analysis_service.py:211:    assert decision["why"]["dte_gate"] == 10
ATT/tests/test_structure_analysis_service.py:220:        structure_id=1,
ATT/tests/test_structure_analysis_service.py:227:        for alternative in result["decision"]["why"]["alternatives"]
ATT/tests/test_structure_analysis_service.py:238:        structure_id=77,
ATT/tests/test_structure_analysis_service.py:244:            "structure_id": 77,
ATT/tests/test_structure_analysis_service.py:259:        service.analyze(structure_id=404)
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
ATT/tests/test_structure_analysis_service.py:309:        structure_id=1,
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
ATT/tests/test_structure_analysis_service.py:366:    result = service.analyze(structure_id=1)
ATT/tests/test_structure_analysis_service.py:370:    assert result["decision"]["dte_min"] == 0
ATT/tests/test_structure_analysis_service.py:384:    def fake_compute_payoff_from_canonical_input(canonical_input):
ATT/tests/test_structure_analysis_service.py:387:    def fake_compute_decision_from_payoff(
ATT/tests/test_structure_analysis_service.py:388:        payoff,
ATT/tests/test_structure_analysis_service.py:396:            "decision": "HOLD",
ATT/tests/test_structure_analysis_service.py:407:        "services.structure_analysis_service.compute_payoff_from_canonical_input",
ATT/tests/test_structure_analysis_service.py:408:        fake_compute_payoff_from_canonical_input,
ATT/tests/test_structure_analysis_service.py:411:        "services.structure_analysis_service.compute_decision_from_payoff",
ATT/tests/test_structure_analysis_service.py:412:        fake_compute_decision_from_payoff,
ATT/tests/test_structure_analysis_service.py:416:        structure_id=1,
ATT/tests/test_structure_analysis_service.py:423:    assert result["decision"]["dte_min"] == 9
ATT/tests/test_structure_analysis_service.py:430:        structure_id: int,
ATT/tests/test_structure_analysis_service.py:435:                "structure_id": structure_id,
ATT/tests/test_structure_analysis_service.py:442:                "structure_id": structure_id,
ATT/tests/test_structure_analysis_service.py:445:                "alias_legacy_aba": "BOVA11",
ATT/tests/test_structure_analysis_service.py:491:                "legacy_aba": "BOVA11",
ATT/tests/test_structure_analysis_service.py:504:    def fake_compute_payoff_from_canonical_input(canonical_input):
ATT/tests/test_structure_analysis_service.py:507:    def fake_compute_decision_from_payoff(
ATT/tests/test_structure_analysis_service.py:508:        payoff,
ATT/tests/test_structure_analysis_service.py:516:            "decision": "HOLD",
ATT/tests/test_structure_analysis_service.py:523:        "services.structure_analysis_service.compute_payoff_from_canonical_input",
ATT/tests/test_structure_analysis_service.py:524:        fake_compute_payoff_from_canonical_input,
ATT/tests/test_structure_analysis_service.py:527:        "services.structure_analysis_service.compute_decision_from_payoff",
ATT/tests/test_structure_analysis_service.py:528:        fake_compute_decision_from_payoff,
ATT/tests/test_structure_analysis_service.py:532:        structure_id=1,
ATT/tests/test_structure_analysis_service.py:550:    def fake_compute_payoff_from_canonical_input(canonical_input):
ATT/tests/test_structure_analysis_service.py:553:    def fake_compute_decision_from_payoff(
ATT/tests/test_structure_analysis_service.py:554:        payoff,
ATT/tests/test_structure_analysis_service.py:562:            "decision": "HOLD",
ATT/tests/test_structure_analysis_service.py:569:        "services.structure_analysis_service.compute_payoff_from_canonical_input",
ATT/tests/test_structure_analysis_service.py:570:        fake_compute_payoff_from_canonical_input,
ATT/tests/test_structure_analysis_service.py:573:        "services.structure_analysis_service.compute_decision_from_payoff",
ATT/tests/test_structure_analysis_service.py:574:        fake_compute_decision_from_payoff,
ATT/tests/test_structure_analysis_service.py:578:        structure_id=1,
ATT/tests/test_structure_analysis_service.py:597:    def fake_compute_payoff_from_canonical_input(canonical_input):
ATT/tests/test_structure_analysis_service.py:600:    def fake_compute_decision_from_payoff(
ATT/tests/test_structure_analysis_service.py:601:        payoff,
ATT/tests/test_structure_analysis_service.py:608:            "decision": "HOLD",
ATT/tests/test_structure_analysis_service.py:615:        "services.structure_analysis_service.compute_payoff_from_canonical_input",
ATT/tests/test_structure_analysis_service.py:616:        fake_compute_payoff_from_canonical_input,
ATT/tests/test_structure_analysis_service.py:619:        "services.structure_analysis_service.compute_decision_from_payoff",
ATT/tests/test_structure_analysis_service.py:620:        fake_compute_decision_from_payoff,
ATT/tests/test_structure_analysis_service.py:624:        structure_id=1,
ATT/tests/test_system_snapshots_repository.py:18:            alias_legacy_aba,
ATT/tests/test_system_snapshots_repository.py:42:    structure_id: int,
ATT/tests/test_system_snapshots_repository.py:50:            structure_id,
ATT/tests/test_system_snapshots_repository.py:67:            structure_id,
ATT/tests/test_system_snapshots_repository.py:90:        structure_id = _insert_structure(conn)
ATT/tests/test_system_snapshots_repository.py:93:            structure_id=structure_id,
ATT/tests/test_system_snapshots_repository.py:100:            structure_id=structure_id,
ATT/tests/test_system_snapshots_repository.py:109:        structure_id=structure_id,
ATT/tests/test_system_snapshots_repository.py:114:            "id": structure_id,
ATT/tests/test_system_snapshots_repository.py:120:        payoff_json={"max_gain": 1000},
ATT/tests/test_system_snapshots_repository.py:121:        decision_json={"action": "hold"},
ATT/tests/test_system_snapshots_repository.py:160:    assert snapshot["structure_id"] == structure_id
ATT/tests/test_system_snapshots_repository.py:167:    assert snapshot["payoff_json"] == {"max_gain": 1000}
ATT/tests/test_system_snapshots_repository.py:168:    assert snapshot["decision_json"] == {"action": "hold"}
ATT/tests/test_system_snapshots_repository.py:186:        structure_id = _insert_structure(conn)
ATT/tests/test_system_snapshots_repository.py:191:        structure_id=structure_id,
ATT/tests/test_system_snapshots_repository.py:196:        structure_id=structure_id,
ATT/tests/test_system_snapshots_repository.py:201:    snapshots = repo.list_snapshots_for_structure(structure_id)
ATT/tests/test_system_snapshots_repository.py:213:        structure_id = _insert_structure(conn)
ATT/tests/test_system_snapshots_repository.py:218:        structure_id=structure_id,
ATT/tests/test_system_snapshots_repository.py:224:        structure_id=structure_id,
ATT/tests/test_system_snapshots_repository.py:242:    latest = repo.get_latest_snapshot_for_structure(structure_id)
ATT/tests/test_system_snapshots_repository.py:259:def test_create_snapshot_requires_structure_id_and_structure_json(tmp_path: Path):
ATT/tests/test_system_snapshots_repository.py:264:    with pytest.raises(ValueError, match="structure_id"):
ATT/tests/test_system_snapshots_repository.py:266:            structure_id=0,
ATT/tests/test_system_snapshots_repository.py:272:            structure_id=1,
ATT/tests/test_ui_data_migration.py:27:def decisions(model):
ATT/tests/test_ui_data_migration.py:28:    return model.get_decisions()
ATT/tests/test_ui_data_migration.py:46:def non_empty_decisions(decisions):
ATT/tests/test_ui_data_migration.py:47:    if not decisions:
ATT/tests/test_ui_data_migration.py:49:    return decisions
ATT/tests/test_ui_data_migration.py:66:# Nível 1 -- get_structures / get_abas
ATT/tests/test_ui_data_migration.py:77:def test_get_abas_alias_de_get_structures(model, structures):
ATT/tests/test_ui_data_migration.py:78:    assert hasattr(model, "get_abas"), "get_abas() deve existir para continuidade operacional"
ATT/tests/test_ui_data_migration.py:79:    assert callable(model.get_abas), "get_abas() deve ser callable"
ATT/tests/test_ui_data_migration.py:80:    assert model.get_abas() == structures, (
ATT/tests/test_ui_data_migration.py:81:        "get_abas() deve retornar o mesmo que get_structures()"
ATT/tests/test_ui_data_migration.py:86:# Nível 2 -- get_decisions() com structure_id
ATT/tests/test_ui_data_migration.py:89:def test_decisions_nao_vazia(non_empty_decisions):
ATT/tests/test_ui_data_migration.py:90:    assert len(non_empty_decisions) > 0, "Deve haver ao menos uma decisão no banco"
ATT/tests/test_ui_data_migration.py:93:def test_decisions_tem_structure_id(decisions):
ATT/tests/test_ui_data_migration.py:94:    for d in decisions:
ATT/tests/test_ui_data_migration.py:95:        assert "structure_id" in d, f"Faltou 'structure_id' no dict: {d}"
ATT/tests/test_ui_data_migration.py:98:def test_decisions_tem_aba(decisions):
ATT/tests/test_ui_data_migration.py:99:    for d in decisions:
ATT/tests/test_ui_data_migration.py:100:        assert "aba" in d, f"Campo 'aba' desapareceu do dict: {d}"
ATT/tests/test_ui_data_migration.py:103:def test_structure_id_igual_a_aba(decisions):
ATT/tests/test_ui_data_migration.py:105:    migração structure_id: structure_id (int) e aba (ticker str) sao campos distintos.
ATT/tests/test_ui_data_migration.py:106:    Verificamos que structure_id e int positivo e aba e str nao-vazia.
ATT/tests/test_ui_data_migration.py:108:    for d in decisions:
ATT/tests/test_ui_data_migration.py:109:        assert isinstance(d["structure_id"], int), (
ATT/tests/test_ui_data_migration.py:110:            f"structure_id deve ser int: {d['structure_id']!r}"
ATT/tests/test_ui_data_migration.py:112:        assert d["structure_id"] > 0, (
ATT/tests/test_ui_data_migration.py:113:            f"structure_id deve ser positivo: {d['structure_id']}"
ATT/tests/test_ui_data_migration.py:115:        assert isinstance(d["aba"], str) and d["aba"].strip(), (
ATT/tests/test_ui_data_migration.py:116:            f"aba deve ser str nao-vazia: {d['aba']!r}"
ATT/tests/test_ui_data_migration.py:120:def test_decisions_tem_timestamp(decisions):
ATT/tests/test_ui_data_migration.py:121:    for d in decisions:
ATT/tests/test_ui_data_migration.py:130:def test_filtro_por_structure_id(model, non_empty_structures):
ATT/tests/test_ui_data_migration.py:132:    migração structure_id: structures retorna lista de str numericas; converte para int
ATT/tests/test_ui_data_migration.py:133:    antes de comparar com d["structure_id"] que e sempre int canonico.
ATT/tests/test_ui_data_migration.py:137:    filtered = model.get_decisions(filters={"structure_id": sid_str})
ATT/tests/test_ui_data_migration.py:139:    assert len(filtered) > 0, f"Filtro structure_id='{sid_str}' retornou vazio"
ATT/tests/test_ui_data_migration.py:141:        assert d["structure_id"] == sid_int, (
ATT/tests/test_ui_data_migration.py:142:            f"Decisao filtrada com structure_id errado: {d['structure_id']!r} != {sid_int}"
ATT/tests/test_ui_data_migration.py:146:def test_filtro_por_aba_continuidade(model, decisions):
ATT/tests/test_ui_data_migration.py:148:    migração structure_id: filtro por 'aba' usa ticker (ex: 'SBSP3'), nao id numerico.
ATT/tests/test_ui_data_migration.py:149:    Verificamos que filtrar por aba de uma decisao real retorna >= 1 resultado
ATT/tests/test_ui_data_migration.py:150:    e que todos os resultados tem a aba correspondente.
ATT/tests/test_ui_data_migration.py:152:    if not decisions:
ATT/tests/test_ui_data_migration.py:153:        pytest.skip("Sem decisoes para testar filtro por aba")
ATT/tests/test_ui_data_migration.py:154:    aba_real = decisions[0]["aba"]        # ex: 'SBSP3'
ATT/tests/test_ui_data_migration.py:155:    filtered_aba = model.get_decisions(filters={"aba": aba_real})
ATT/tests/test_ui_data_migration.py:156:    assert isinstance(filtered_aba, list), "Filtro aba deve retornar lista"
ATT/tests/test_ui_data_migration.py:157:    assert len(filtered_aba) >= 1, (
ATT/tests/test_ui_data_migration.py:158:        f"Filtro aba='{aba_real}' retornou vazio"
ATT/tests/test_ui_data_migration.py:160:    for d in filtered_aba:
ATT/tests/test_ui_data_migration.py:161:        assert d["aba"] == aba_real, (
ATT/tests/test_ui_data_migration.py:162:            f"Decisao com aba errada: esperado '{aba_real}', recebido '{d['aba']}'"
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
ATT/tests/test_ui_data_migration.py:187:    assert info["aba"] == d0["structure_id"], (
ATT/tests/test_ui_data_migration.py:188:        f"info['aba']='{info['aba']}' != structure_id='{d0['structure_id']}'"
ATT/tests/test_ui_data_migration.py:192:def test_payoff_curve_info_pontos_validos(model, non_empty_decisions):
ATT/tests/test_ui_data_migration.py:193:    d0 = non_empty_decisions[0]
ATT/tests/test_ui_data_migration.py:194:    pts, _ = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"])

## Arquivos completos com numeracao - Fase 4

## FILE: services/derived_service.py
```python
     1	from __future__ import annotations
     2	# services/derived_service.py
     3	"""
     4	alteracao_30/alteracao_57c -- Servico de persistencia de dados derivados (payoff + decisoes).
     5	alteracao_62           -- AbaResolverMixin extraído para repositories/_aba_resolver_mixin.py.
     6	alteracao_65           -- get_payoff_by_aba() removida da interface pública (standalone).
     7	"""
     8	
     9	import inspect
    10	import json
    11	import sqlite3
    12	from datetime import datetime, timezone
    13	from typing import Any, Dict, List, Optional, Tuple, Union
    14	
    15	from db.config import connect_app, connect_derived
    16	from db.derived_repo import (
    17	    cleanup_old_decisions,
    18	    cleanup_old_payoff_data,
    19	    ensure_derived_tables,
    20	    insert_payoff_points,
    21	    insert_structure_decision,
    22	)
    23	from src.domain.refs.structure_ref import StructureRef
    24	
    25	
    26	# ------------------------------------------------------------------
    27	# Cache modulo-level: aba -> structure_id
    28	# ------------------------------------------------------------------
    29	
    30	_ABA_TO_STRUCTURE_ID: Dict[str, int] = {}
    31	_ABA_CACHE_LOADED: bool = False
    32	
    33	
    34	def _load_aba_cache() -> None:
    35	    global _ABA_TO_STRUCTURE_ID, _ABA_CACHE_LOADED
    36	    try:
    37	        with connect_app() as conn:
    38	            cur = conn.execute("""
    39	                SELECT id, alias_legacy_aba
    40	                FROM structures
    41	                WHERE alias_legacy_aba IS NOT NULL
    42	                  AND alias_legacy_aba != ''
    43	            """)
    44	            _ABA_TO_STRUCTURE_ID = {row[1]: row[0] for row in cur.fetchall()}
    45	    except Exception:
    46	        _ABA_TO_STRUCTURE_ID = {}
    47	    finally:
    48	        _ABA_CACHE_LOADED = True
    49	
    50	
    51	def _resolve_structure_id(aba: Optional[str]) -> Optional[int]:
    52	    if not _ABA_CACHE_LOADED:
    53	        _load_aba_cache()
    54	    if not aba:
    55	        return None
    56	    return _ABA_TO_STRUCTURE_ID.get(aba)
    57	
    58	
    59	def invalidate_aba_cache() -> None:
    60	    global _ABA_CACHE_LOADED
    61	    _ABA_CACHE_LOADED = False
    62	
    63	
    64	# ------------------------------------------------------------------
    65	# Helpers internos
    66	# ------------------------------------------------------------------
    67	
    68	def _now_iso() -> str:
    69	    return datetime.now(timezone.utc).isoformat()
    70	
    71	
    72	def _safe_str(value: Any) -> Optional[str]:
    73	    if value is None:
    74	        return None
    75	    text = str(value).strip()
    76	    return text or None
    77	
    78	
    79	def _unwrap_ref(ref: Any) -> Optional[str]:
    80	    """
    81	    alteracao_57: extrai string aba de StructureRef ou passa str diretamente.
    82	    Equivalente a _unwrap_aba do derived_repo, mas para a camada de servico.
    83	    """
    84	    if isinstance(ref, StructureRef):
    85	        return ref.aba
    86	    return _safe_str(ref)
    87	
    88	
    89	def _resolve_storage_key(
    90	    aba: Optional[str] = None,
    91	    structure_id: Any = None,
    92	    structure_name: Any = None,
    93	    underlying_asset: Any = None,
    94	) -> str:
    95	    # 1. aba explícita tem prioridade máxima
    96	    resolved_aba = _safe_str(aba)
    97	    if resolved_aba:
    98	        return resolved_aba
    99	
   100	    # 2. structure_id → resolver alias_legacy_aba via cache (FIX alteracao_66)
   101	    resolved_sid = _safe_str(structure_id)
   102	    if resolved_sid:
   103	        try:
   104	            sid_int = int(resolved_sid)
   105	            if not _ABA_CACHE_LOADED:
   106	                _load_aba_cache()
   107	            id_to_aba = {v: k for k, v in _ABA_TO_STRUCTURE_ID.items()}
   108	            alias = id_to_aba.get(sid_int)
   109	            if alias:
   110	                return alias  # "BOVA11" em vez de "structure:7"
   111	        except (ValueError, TypeError):
   112	            pass
   113	        return f"structure:{resolved_sid}"  # fallback sem alias
   114	
   115	    # 3. fallbacks por nome/ativo
   116	    resolved_structure_name = _safe_str(structure_name)
   117	    if resolved_structure_name:
   118	        return resolved_structure_name
   119	
   120	    resolved_underlying_asset = _safe_str(underlying_asset)
   121	    if resolved_underlying_asset:
   122	        return resolved_underlying_asset
   123	
   124	    return "unknown"
   125	
   126	
   127	def _merge_meta(
   128	    meta: Optional[Dict[str, Any]] = None,
   129	    structure_id: Any = None,
   130	    structure_name: Any = None,
   131	    underlying_asset: Any = None,
   132	    reference_date: Any = None,
   133	    input_meta: Optional[Dict[str, Any]] = None,
   134	    storage_key: Optional[str] = None,
   135	) -> Dict[str, Any]:
   136	    return {
   137	        **(meta or {}),
   138	        "structure_id":     structure_id,
   139	        "structure_name":   structure_name,
   140	        "underlying_asset": underlying_asset,
   141	        "reference_date":   reference_date,
   142	        "input_meta":       input_meta or {},
   143	        "storage_key":      storage_key,
   144	    }
   145	
   146	
   147	# ------------------------------------------------------------------
   148	# Init
   149	# ------------------------------------------------------------------
   150	
   151	def init_db():
   152	    with connect_derived() as conn:
   153	        ensure_derived_tables(conn)
   154	
   155	
   156	# ------------------------------------------------------------------
   157	# Payoff
   158	# ------------------------------------------------------------------
   159	
   160	def save_payoff_curve(
   161	    ref: Any,
   162	    points: List[Union[Tuple[float, float], Dict[str, float]]],
   163	    spot_ref: Optional[float] = None,
   164	    meta: Optional[Dict[str, Any]] = None,
   165	    timestamp: Optional[str] = None,
   166	    structure_id: Any = None,
   167	) -> int:
   168	    """
   169	    alteracao_57: 'ref' aceita StructureRef, str ou None.
   170	    _unwrap_ref() extrai a string aba de forma segura.
   171	    """
   172	    ts           = timestamp or _now_iso()
   173	    storage_key  = _unwrap_ref(ref) or "unknown"
   174	    resolved_sid = (
   175	        int(structure_id)
   176	        if structure_id is not None
   177	        else _resolve_structure_id(storage_key)
   178	    )
   179	
   180	    norm_points: List[Tuple[float, float]] = []
   181	    for p in points or []:
   182	        if isinstance(p, (tuple, list)) and len(p) == 2:
   183	            norm_points.append((float(p[0]), float(p[1])))
   184	        elif isinstance(p, dict):
   185	            x = p.get("point_spot") or p.get("s_t")
   186	            y = p.get("point_pl")   or p.get("pl_venc")
   187	            if x is None or y is None:
   188	                continue
   189	            norm_points.append((float(x), float(y)))
   190	
   191	    effective_meta = {
   192	        **(meta or {}),
   193	        "storage_key":  storage_key,
   194	        "structure_id": resolved_sid,
   195	    }
   196	
   197	    with connect_derived() as conn:
   198	        ensure_derived_tables(conn)
   199	        return insert_payoff_points(
   200	            conn=conn,
   201	            timestamp=ts,
   202	            aba=storage_key,
   203	            points=norm_points,
   204	            spot_ref=spot_ref,
   205	            meta=effective_meta,
   206	            structure_id=resolved_sid,
   207	        )
   208	
   209	
   210	def save_payoff_from_canonical_payload(
   211	    payoff: Dict[str, Any],
   212	    aba: Optional[str] = None,
   213	    timestamp: Optional[str] = None,
   214	) -> int:
   215	    ts = timestamp or _now_iso()
   216	
   217	    storage_key = _resolve_storage_key(
   218	        aba=aba,
   219	        structure_id=payoff.get("structure_id"),
   220	        structure_name=payoff.get("structure_name"),
   221	        underlying_asset=payoff.get("underlying_asset"),
   222	    )
   223	
   224	    sid_from_payload = payoff.get("structure_id")
   225	    resolved_sid = (
   226	        int(sid_from_payload)
   227	        if sid_from_payload is not None
   228	        else _resolve_structure_id(storage_key)
   229	    )
   230	
   231	    meta = _merge_meta(
   232	        meta=payoff.get("meta"),
   233	        structure_id=resolved_sid,
   234	        structure_name=payoff.get("structure_name"),
   235	        underlying_asset=payoff.get("underlying_asset"),
   236	        reference_date=payoff.get("reference_date"),
   237	        input_meta=payoff.get("input_meta"),
   238	        storage_key=storage_key,
   239	    )
   240	
   241	    try:
   242	        sig = inspect.signature(save_payoff_curve)
   243	        accepts_structure_id = (
   244	            "structure_id" in sig.parameters
   245	            or any(
   246	                p.kind == inspect.Parameter.VAR_KEYWORD
   247	                for p in sig.parameters.values()
   248	            )
   249	        )
   250	    except (TypeError, ValueError):
   251	        accepts_structure_id = True
   252	
   253	    if accepts_structure_id:
   254	        return save_payoff_curve(
   255	            ref=storage_key,
   256	            points=payoff.get("points", []),
   257	            spot_ref=payoff.get("spot_ref"),
   258	            meta=meta,
   259	            timestamp=ts,
   260	            structure_id=resolved_sid,
   261	        )
   262	
   263	    return save_payoff_curve(
   264	        ref=storage_key,
   265	        points=payoff.get("points", []),
   266	        spot_ref=payoff.get("spot_ref"),
   267	        meta=meta,
   268	        timestamp=ts,
   269	    )
   270	
   271	
   272	
   273	def save_decision(
   274	    ref: Any,
   275	    decision: Dict[str, Any],
   276	    timestamp: Optional[str] = None,
   277	    structure_id: Any = None,
   278	) -> int:
   279	    """
   280	    alteracao_57: 'ref' aceita StructureRef, str ou None.
   281	
   282	    Fase 3A.4:
   283	    - Preserva structure_id explícito recebido por argumento, pelo payload
   284	      ou pelo meta.
   285	    - Só tenta resolver por storage_key/alias quando não há structure_id explícito.
   286	    """
   287	    ts = timestamp or _now_iso()
   288	    storage_key = _unwrap_ref(ref) or "unknown"
   289	
   290	    explicit_sid = structure_id
   291	    if explicit_sid is None:
   292	        explicit_sid = decision.get("structure_id")
   293	    if explicit_sid is None:
   294	        explicit_sid = (decision.get("meta") or {}).get("structure_id")
   295	
   296	    resolved_sid = (
   297	        int(explicit_sid)
   298	        if explicit_sid is not None
   299	        else _resolve_structure_id(storage_key)
   300	    )
   301	
   302	    enriched_decision = {
   303	        **decision,
   304	        "structure_id": resolved_sid,
   305	        "meta": {
   306	            **(decision.get("meta") or {}),
   307	            "storage_key": storage_key,
   308	            "structure_id": resolved_sid,
   309	        },
   310	    }
   311	
   312	    with connect_derived() as conn:
   313	        ensure_derived_tables(conn)
   314	        return insert_structure_decision(
   315	            conn=conn,
   316	            timestamp=ts,
   317	            aba=storage_key,
   318	            decision_dict=enriched_decision,
   319	        )
   320	
   321	
   322	def save_decision_from_canonical_payload(
   323	    decision: Dict[str, Any],
   324	    structure_id: Any = None,
   325	    structure_name: Any = None,
   326	    underlying_asset: Any = None,
   327	    aba: Optional[str] = None,
   328	    timestamp: Optional[str] = None,
   329	) -> int:
   330	    ts = timestamp or _now_iso()
   331	
   332	    storage_key = _resolve_storage_key(
   333	        aba=aba,
   334	        structure_id=structure_id,
   335	        structure_name=structure_name,
   336	        underlying_asset=underlying_asset,
   337	    )
   338	
   339	    resolved_sid = (
   340	        int(structure_id)
   341	        if structure_id is not None
   342	        else _resolve_structure_id(storage_key)
   343	    )
   344	
   345	    enriched_decision = {
   346	        **decision,
   347	        "structure_id": resolved_sid,
   348	        "meta": {
   349	            **(decision.get("meta") or {}),
   350	            "structure_id":     resolved_sid,
   351	            "structure_name":   structure_name,
   352	            "underlying_asset": underlying_asset,
   353	            "storage_key":      storage_key,
   354	        },
   355	    }
   356	
   357	    return save_decision(
   358	        ref=storage_key,
   359	        decision=enriched_decision,
   360	        timestamp=ts,
   361	    )
   362	
   363	
   364	# ------------------------------------------------------------------
   365	# Cleanup
   366	# ------------------------------------------------------------------
   367	
   368	def cleanup_derived(days_to_keep: int = 30) -> Dict[str, int]:
   369	    with connect_derived() as conn:
   370	        ensure_derived_tables(conn)
   371	        deleted_payoff = cleanup_old_payoff_data(conn, days_to_keep=days_to_keep)
   372	        deleted_dec    = cleanup_old_decisions(conn, days_to_keep=days_to_keep)
   373	        return {"payoff_deleted": deleted_payoff, "decisions_deleted": deleted_dec}
   374	
   375	
   376	# ------------------------------------------------------------------
   377	# Leituras
   378	# ------------------------------------------------------------------
   379	
   380	def get_all_payoff_curves():
   381	    with connect_derived() as conn:
   382	        cursor = conn.cursor()
   383	        cursor.execute("""
   384	            SELECT timestamp, aba, point_spot, point_pl, meta_json
   385	            FROM payoff_curve_points
   386	            ORDER BY timestamp DESC, point_spot
   387	        """)
   388	        return [
   389	            {
   390	                "timestamp":  row[0],
   391	                "aba":        row[1],
   392	                "point_spot": row[2],
   393	                "point_pl":   row[3],
   394	                "meta_json":  json.loads(row[4]) if row[4] else None,
   395	            }
   396	            for row in cursor.fetchall()
   397	        ]
   398	
   399	
   400	def get_payoff_by_structure_id(structure_id: int):
   401	    """
   402	    alteracao_56/alteracao_65: único ponto de entrada canônico para leitura de payoff.
   403	
   404	    Retorna somente a curva mais recente da estrutura.
   405	    Importante: payoff_curve_points mantém histórico por timestamp.
   406	    Sem filtrar MAX(timestamp), a UI pode misturar curvas antigas e novas.
   407	    """
   408	    ref = StructureRef.from_id(structure_id)
   409	    col, val = ref.db_pair()
   410	
   411	    with connect_derived() as conn:
   412	        cursor = conn.cursor()
   413	        cursor.execute(
   414	            f"""
   415	            SELECT timestamp, point_spot, point_pl, meta_json
   416	              FROM payoff_curve_points
   417	             WHERE {col} = ?
   418	               AND timestamp = (
   419	                    SELECT MAX(timestamp)
   420	                      FROM payoff_curve_points
   421	                     WHERE {col} = ?
   422	               )
   423	             ORDER BY point_spot
   424	            """,
   425	            (val, val),
   426	        )
   427	        return [
   428	            {
   429	                "timestamp":  row[0],
   430	                "point_spot": row[1],
   431	                "point_pl":   row[2],
   432	                "meta_json":  json.loads(row[3]) if row[3] else None,
   433	            }
   434	            for row in cursor.fetchall()
   435	        ]
   436	
   437	
   438	
   439	def get_recent_decisions():
   440	    with connect_derived() as conn:
   441	        conn.row_factory = sqlite3.Row
   442	        cursor = conn.cursor()
   443	
   444	        cols = [
   445	            row["name"]
   446	            for row in cursor.execute(
   447	                "PRAGMA table_info(structure_decisions)"
   448	            ).fetchall()
   449	        ]
   450	
   451	        select_cols = [
   452	            "timestamp", "aba", "decision", "level",
   453	            "pl_atual", "pl_max", "pl_pct_of_max", "dte_min",
   454	            "spot_ref", "meta_json", "created_at",
   455	        ]
   456	        if "structure_id" in cols:
   457	            select_cols.append("structure_id")
   458	        if "why" in cols:
   459	            select_cols.append("why")
   460	        if "why_json" in cols:
   461	            select_cols.append("why_json")
   462	
   463	        cursor.execute(f"""
   464	            SELECT {", ".join(select_cols)}
   465	            FROM structure_decisions
   466	            ORDER BY timestamp DESC
   467	            LIMIT 50
   468	        """)
   469	
   470	        decisions = []
   471	        for row in cursor.fetchall():
   472	            item = dict(row)
   473	            why_val      = item.get("why")
   474	            why_json_val = item.get("why_json")
   475	
   476	            if isinstance(why_val, str):
   477	                try:
   478	                    item["why"] = json.loads(why_val)
   479	                except Exception:
   480	                    pass
   481	            elif why_val is None and why_json_val is not None:
   482	                try:
   483	                    item["why"] = (
   484	                        json.loads(why_json_val)
   485	                        if isinstance(why_json_val, str)
   486	                        else why_json_val
   487	                    )
   488	                except Exception:
   489	                    item["why"] = why_json_val
   490	
   491	            if item.get("structure_id") is None:
   492	                for src_key in ("why_json", "meta_json"):
   493	                    raw = item.get(src_key)
   494	                    if not raw:
   495	                        continue
   496	                    try:
   497	                        parsed = json.loads(raw) if isinstance(raw, str) else raw
   498	                        sid = parsed.get("structure_id")
   499	                        if sid is not None:
   500	                            item["structure_id"] = sid
   501	                            break
   502	                    except Exception:
   503	                        pass
   504	
   505	            decisions.append(item)
   506	
   507	        return decisions
   508	
   509	
   510	# ---------------------------------------------------------------------------
   511	# alteracao_59 -- format_report + snapshot_aba (surface canônica)
   512	# ---------------------------------------------------------------------------
   513	
   514	def format_report(entries) -> str:
   515	    """Formata relatório de auditoria de surface ABA em texto legível."""
   516	    lines: list[str] = []
   517	    for e in entries:
   518	        aba_str = getattr(e, "aba_str", str(getattr(e, "structure_id", "")))
   519	        sid     = getattr(e, "structure_id", "?")
   520	        ref     = getattr(e, "reference_date", "?")
   521	        lines.append(f"{sid} | {ref} | {aba_str}")
   522	    return "\n".join(lines)
   523	
   524	
   525	def snapshot_aba(ref: "StructureRef") -> str:
   526	    """Retorna aba_str canônico a partir de um StructureRef."""
   527	    aba_str = ref.aba if hasattr(ref, "aba") and ref.aba else str(ref.structure_id)
   528	    return aba_str
   529	
   530	
   531	# ------------------------------------------------------------------
   532	# alteracao_65 -- DerivedService: fachada orientada a objetos
   533	# get_payoff_by_aba() removida da interface pública.
   534	# get_payoff_by_structure_id() é o único ponto de entrada canônico.
   535	# ------------------------------------------------------------------
   536	
   537	class DerivedService:
   538	    """Fachada OO sobre as funcoes standalone do derived_service.
   539	    alteracao_65: get_payoff_by_aba() nao exposta -- use get_payoff_by_structure_id().
   540	    get_payoff_by_aba() ausente por decisao de design (alteracao_65): interface simplificada.
   541	    """
   542	
   543	    # alteracao_65: get_payoff_by_aba() deliberadamente nao implementada nesta classe.
   544	    # Chamadores legados devem migrar para get_payoff_by_structure_id().
   545	
   546	    def get_payoff_by_structure_id(self, structure_id: int):
   547	        """Retorna pontos de payoff para a estrutura informada."""
   548	        return get_payoff_by_structure_id(structure_id)
   549	
   550	    def save_payoff_curve(self, *args, **kwargs):
   551	        return save_payoff_curve(*args, **kwargs)
   552	
   553	    def save_decision(self, *args, **kwargs):
   554	        return save_decision(*args, **kwargs)
   555	
   556	    def cleanup_derived(self, days_to_keep: int = 30):
   557	        return cleanup_derived(days_to_keep)
```

## FILE: services/derived_payoff_persistence.py
```python
     1	# services/derived_payoff_persistence.py
     2	import logging
     3	from datetime import datetime, timezone
     4	from typing import Any
     5	
     6	from domain.payoff import compute_payoff_from_canonical_input
     7	from services.derived_service import save_payoff_from_canonical_payload, save_decision_from_canonical_payload
     8	
     9	logger = logging.getLogger(__name__)
    10	
    11	
    12	class DerivedPayoffPersistence:
    13	    """
    14	    Implementação concreta de PayoffPersistencePort.
    15	
    16	    Responsabilidades:
    17	      1. Montar o canonical_input a partir do pricing_payload
    18	      2. Calcular a curva de payoff via domain/payoff.py
    19	      3. Persistir pontos no derived.db via derived_service
    20	      4. Persistir decisão básica derivada do resultado do engine
    21	    """
    22	
    23	    # -------------------------------------------------------------- #
    24	    #  PayoffPersistencePort.persist()                                 #
    25	    # -------------------------------------------------------------- #
    26	
    27	    def persist(
    28	        self,
    29	        pricing_payload: dict[str, Any] | None,
    30	        result: dict[str, Any],
    31	    ) -> None:
    32	        if not pricing_payload:
    33	            logger.debug("derived_payoff_persistence: pricing_payload vazio, skip.")
    34	            return
    35	
    36	        inner = result.get("result", result) if isinstance(result, dict) else{}
    37	        status = inner.get("status", "")
    38	        if status not in ("success", "ok", "completed"):
    39	            logger.debug(
    40	                "derived_payoff_persistence: status=%r não elegível para payoff, skip.",
    41	                status,
    42	            )
    43	            return
    44	
    45	        # Timestamp único para payoff + decisão.
    46	        # Evita snapshots inconsistentes por diferença de milissegundos entre gravações.
    47	        snapshot_ts = datetime.now(timezone.utc).isoformat()
    48	
    49	        payoff_saved = self._persist_payoff(pricing_payload, result, snapshot_ts)
    50	        if not payoff_saved:
    51	            logger.warning(
    52	                "derived_payoff_persistence: decisão não gravada porque payoff não foi salvo -- structure_id=%s",
    53	                pricing_payload.get("structure_id"),
    54	            )
    55	            return
    56	
    57	        decision_saved = self._persist_decision(pricing_payload, result, snapshot_ts)
    58	        if not decision_saved:
    59	            logger.error(
    60	                "derived_payoff_persistence: payoff salvo, mas decisão falhou -- structure_id=%s timestamp=%s",
    61	                pricing_payload.get("structure_id"),
    62	                snapshot_ts,
    63	            )
    64	
    65	    # -------------------------------------------------------------- #
    66	    #  payoff                                                          #
    67	    # -------------------------------------------------------------- #
    68	
    69	    def _persist_payoff(
    70	        self,
    71	        pricing_payload: dict[str, Any],
    72	        result: dict[str, Any],
    73	        snapshot_ts: str,
    74	    ) -> bool:
    75	        try:
    76	            canonical_input = self._build_canonical_input(pricing_payload, result)
    77	            payoff_result = compute_payoff_from_canonical_input(canonical_input)
    78	
    79	            if not payoff_result.get("points"):
    80	                logger.warning(
    81	                    "derived_payoff_persistence: payoff sem pontos para structure_id=%s",
    82	                    pricing_payload.get("structure_id"),
    83	                )
    84	                return False
    85	
    86	            save_payoff_from_canonical_payload(payoff_result, timestamp=snapshot_ts)
    87	            logger.info(
    88	                "derived_payoff_persistence: %d pontos gravados -- structure_id=%s",
    89	                len(payoff_result["points"]),
    90	                pricing_payload.get("structure_id"),
    91	            )
    92	            return True
    93	
    94	        except Exception:
    95	            logger.exception(
    96	                "derived_payoff_persistence: erro ao gravar payoff -- structure_id=%s",
    97	                pricing_payload.get("structure_id"),
    98	            )
    99	            return False
   100	
   101	    # -------------------------------------------------------------- #
   102	    #  decisão                                                         #
   103	    # -------------------------------------------------------------- #
   104	
   105	    def _persist_decision(
   106	        self,
   107	        pricing_payload: dict[str, Any],
   108	        result: dict[str, Any],
   109	        snapshot_ts: str,
   110	    ) -> bool:
   111	        try:
   112	            if not isinstance(result, dict):
   113	                inner = {}
   114	            else:
   115	                inner = result.get("result") or result
   116	
   117	            valuation = inner.get("valuation") or {}
   118	            metrics   = inner.get("metrics")   or {}
   119	
   120	            theoretical_value = valuation.get("theoretical_value")
   121	            pl_max            = valuation.get("pl_max")
   122	            pl_atual          = valuation.get("pl_atual") or theoretical_value
   123	            dte_min           = metrics.get("dte_min")
   124	            spot_ref          = pricing_payload.get("spot_price")
   125	            
   126	            if spot_ref is None:
   127	                spot_ref = (pricing_payload.get("market") or {}).get("spot_price")
   128	
   129	            pl_pct_of_max = None
   130	            if pl_max and pl_atual is not None:
   131	                try:
   132	                    pl_pct_of_max = round(float(pl_atual) / float(pl_max), 6)
   133	                except (ZeroDivisionError, TypeError, ValueError):
   134	                    pass
   135	
   136	            decision_dict = {
   137	                "decision":      "HOLD",
   138	                "level":         0,
   139	                "pl_atual":      pl_atual,
   140	                "pl_max":        pl_max,
   141	                "pl_pct_of_max": pl_pct_of_max,
   142	                "dte_min":       dte_min,
   143	                "spot_ref":      spot_ref,
   144	                "why": {
   145	                    "source":           "pricing_engine",
   146	                    "engine":           inner.get("engine"),
   147	                    "execution_status": inner.get("status"),
   148	                    "theoretical_value": theoretical_value,
   149	                },
   150	                "meta": {
   151	                    "structure_id":    pricing_payload.get("structure_id"),
   152	                    "structure_name":  pricing_payload.get("structure_name"),
   153	                    "underlying_asset": pricing_payload.get("underlying_asset"),
   154	                    "reference_date":  pricing_payload.get("reference_date"),
   155	                },
   156	            }
   157	
   158	            save_decision_from_canonical_payload(
   159	                decision=decision_dict,
   160	                structure_id=pricing_payload.get("structure_id"),
   161	                structure_name=pricing_payload.get("structure_name"),
   162	                underlying_asset=pricing_payload.get("underlying_asset"),
   163	                timestamp=snapshot_ts,
   164	            )
   165	            logger.info(
   166	                "derived_payoff_persistence: decisão gravada -- structure_id=%s",
   167	                pricing_payload.get("structure_id"),
   168	            )
   169	            return True
   170	
   171	        except Exception:
   172	            logger.exception(
   173	                "derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s",
   174	                pricing_payload.get("structure_id"),
   175	            )
   176	            return False
   177	
   178	    # -------------------------------------------------------------- #
   179	    #  helpers                                                         #
   180	    # -------------------------------------------------------------- #
   181	
   182	
   183	    @staticmethod
   184	    def _normalize_position_side(value: Any, quantity: Any = None) -> str | None:
   185	        """
   186	        Normaliza aliases de direção para o contrato canônico de payoff.
   187	
   188	        domain/payoff.py exige leg["position_side"].
   189	        Payloads vindos da UI/manual podem vir com leg["side"].
   190	        """
   191	        raw = "" if value is None else str(value).strip().upper()
   192	
   193	        aliases = {
   194	            "BUY": "LONG",
   195	            "BOUGHT": "LONG",
   196	            "COMPRA": "LONG",
   197	            "COMPRADO": "LONG",
   198	            "LONG": "LONG",
   199	            "SELL": "SHORT",
   200	            "SOLD": "SHORT",
   201	            "VENDA": "SHORT",
   202	            "VENDIDO": "SHORT",
   203	            "SHORT": "SHORT",
   204	        }
   205	
   206	        if raw in aliases:
   207	            return aliases[raw]
   208	
   209	        try:
   210	            q = float(quantity)
   211	            if q < 0:
   212	                return "SHORT"
   213	            if q > 0:
   214	                return "LONG"
   215	        except (TypeError, ValueError):
   216	            pass
   217	
   218	        return None
   219	
   220	    @staticmethod
   221	    def _normalize_leg_for_payoff(leg: Any) -> dict[str, Any]:
   222	        """
   223	        Adapta uma leg recebida de fontes legadas/manuais para o contrato
   224	        esperado por domain.compute_payoff_from_canonical_input().
   225	
   226	        Correção principal da Fase 3F Fix1:
   227	          side -> position_side
   228	
   229	        Também mantém aliases úteis sem remover os campos originais.
   230	        """
   231	        data = dict(leg) if isinstance(leg, dict) else dict(vars(leg))
   232	
   233	        quantity = data.get("quantity", data.get("quant"))
   234	        position_side = data.get("position_side") or data.get("side")
   235	
   236	        normalized_side = DerivedPayoffPersistence._normalize_position_side(
   237	            position_side,
   238	            quantity,
   239	        )
   240	
   241	        if normalized_side:
   242	            data["position_side"] = normalized_side
   243	            data.setdefault("side", normalized_side)
   244	
   245	        if quantity is not None:
   246	            try:
   247	                # No contrato canônico, a direção fica em position_side.
   248	                # A quantidade deve ser magnitude positiva.
   249	                data["quantity"] = abs(float(quantity))
   250	            except (TypeError, ValueError):
   251	                data["quantity"] = quantity
   252	
   253	        option_type = data.get("option_type")
   254	        if option_type is not None:
   255	            data["option_type"] = str(option_type).strip().upper()
   256	
   257	        instrument_type = data.get("instrument_type")
   258	        if instrument_type is not None:
   259	            data["instrument_type"] = str(instrument_type).strip().upper()
   260	
   261	        # Aliases defensivos para eventuais payloads de outras origens.
   262	        if "premium" not in data and "price" in data:
   263	            data["premium"] = data.get("price")
   264	
   265	        if "price" not in data and "premium" in data:
   266	            data["price"] = data.get("premium")
   267	
   268	        if "symbol" not in data:
   269	            data["symbol"] = data.get("asset") or data.get("ativo")
   270	
   271	        return data
   272	
   273	    @staticmethod
   274	    def _normalize_canonical_input_for_payoff(
   275	        canonical_input: dict[str, Any],
   276	    ) -> dict[str, Any]:
   277	        """
   278	        Retorna uma cópia rasa do canonical_input com legs normalizadas para payoff.
   279	        """
   280	        normalized = dict(canonical_input)
   281	
   282	        structure = dict(normalized.get("structure") or {})
   283	        market = dict(normalized.get("market") or {})
   284	        meta = dict(normalized.get("meta") or {})
   285	
   286	        legs = structure.get("legs") or []
   287	        structure["legs"] = [
   288	            DerivedPayoffPersistence._normalize_leg_for_payoff(leg)
   289	            for leg in legs
   290	        ]
   291	
   292	        meta.setdefault("payoff_leg_normalization", "fase_3f_fix1_position_side_from_side")
   293	
   294	        normalized["structure"] = structure
   295	        normalized["market"] = market
   296	        normalized["meta"] = meta
   297	
   298	        return normalized
   299	
   300	
   301	    @staticmethod
   302	    def _build_canonical_input(
   303	        pricing_payload: dict[str, Any],
   304	        result: dict[str, Any],
   305	    ) -> dict[str, Any]:
   306	        """
   307	        Monta o canonical_input esperado por compute_payoff_from_canonical_input().
   308	
   309	        Suporta dois formatos de pricing_payload:
   310	          A) já canônico: { structure: { legs, ... }, market: { spot_price, ... } }
   311	          B) flat:        { legs: [...], spot_price: ..., structure_id: ..., ... }
   312	        """
   313	        # Formato A -- já canônico, mas ainda assim normalizado para o contrato
   314	        # estrito de domain/payoff.py.
   315	        if "structure" in pricing_payload and "market" in pricing_payload:
   316	            return DerivedPayoffPersistence._normalize_canonical_input_for_payoff(
   317	                pricing_payload
   318	            )
   319	
   320	        # Formato B -- flat  montar canônico
   321	        structure_id   = pricing_payload.get("structure_id")
   322	        structure_name = pricing_payload.get("structure_name")
   323	        underlying     = pricing_payload.get("underlying_asset")
   324	        spot_price     = pricing_payload.get("spot_price") or 0.0
   325	        reference_date = pricing_payload.get("reference_date")
   326	        legs           = pricing_payload.get("legs") or []
   327	
   328	        payload_meta = pricing_payload.get("meta")
   329	        meta = dict(payload_meta) if isinstance(payload_meta, dict) else {}
   330	        meta.setdefault("source", "pricing_execution_persistence")
   331	        meta.setdefault("payoff_leg_normalization", "fase_3f_fix1_position_side_from_side")
   332	
   333	        canonical_input = {
   334	            "structure": {
   335	                "structure_id":    structure_id,
   336	                "name":            structure_name,
   337	                "underlying_asset": underlying,
   338	                "legs": [
   339	                    DerivedPayoffPersistence._normalize_leg_for_payoff(leg)
   340	                    for leg in legs
   341	                ],
   342	            },
   343	            "market": {
   344	                "spot_price":       spot_price,
   345	                "underlying_asset": underlying,
   346	                "reference_date":   reference_date,
   347	            },
   348	            "meta": meta,
   349	        }
   350	
   351	        return canonical_input
```

## FILE: services/payoff_persistence_port.py
```python
     1	# services/payoff_persistence_port.py
     2	from typing import Any, Protocol
     3	
     4	
     5	class PayoffPersistencePort(Protocol):
     6	    """
     7	    Contrato de persistência derivada (payoff + decisão).
     8	
     9	    Implementações devem gravar os dados no derived.db após
    10	    uma execução de pricing bem-sucedida.
    11	    """
    12	
    13	    def persist(
    14	        self,
    15	        pricing_payload: dict[str, Any] | None,
    16	        result: dict[str, Any],
    17	    ) -> None:
    18	        ...
```

## FILE: services/payoff_pricing_engine.py
```python
     1	from typing import Any
     2	
     3	from domain.payoff import compute_payoff_curve_from_canonical_legs
     4	from domain.position_side import to_pricing_engine_side
     5	
     6	
     7	class PayoffPricingEngine:
     8	    """
     9	    Motor financeiro inicial baseado na curva de payoff canônica.
    10	
    11	    Objetivo:
    12	    - substituir o motor stub no fluxo real;
    13	    - manter o contrato de saída esperado por PricingExecutionService;
    14	    - gerar métricas financeiras não nulas quando houver dados suficientes;
    15	    - não depender ainda de Black-Scholes.
    16	    """
    17	
    18	    engine_name = "payoff_pricing_engine"
    19	
    20	    def run(self, pricing_payload: dict[str, Any]) -> dict[str, Any]:
    21	        if not pricing_payload:
    22	            raise ValueError("pricing_payload is required")
    23	
    24	        legs = pricing_payload.get("legs") or []
    25	        if not legs:
    26	            raise ValueError("pricing_payload.legs is required")
    27	
    28	        spot_price = float(pricing_payload.get("spot_price") or 0.0)
    29	        if spot_price <= 0:
    30	            raise ValueError("pricing_payload.spot_price is required")
    31	
    32	        normalized_legs = [self._normalize_leg(leg) for leg in legs]
    33	
    34	        total_quantity = sum(
    35	            int(float(leg.get("quantity") or 0))
    36	            for leg in normalized_legs
    37	        )
    38	        number_of_legs = len(normalized_legs)
    39	
    40	        payoff = compute_payoff_curve_from_canonical_legs(
    41	            legs=normalized_legs,
    42	            spot_ref=spot_price,
    43	            low_pct=0.5,
    44	            high_pct=1.5,
    45	            step_pct=0.01,
    46	        )
    47	
    48	        pl_max = payoff.get("pl_max")
    49	        pl_min = payoff.get("pl_min")
    50	        pl_atual = self._compute_pl_at_spot(
    51	            legs=normalized_legs,
    52	            spot_price=spot_price,
    53	        )
    54	
    55	        premium_paid = self._compute_net_premium_paid(normalized_legs)
    56	
    57	        max_profit = pl_max
    58	        max_loss = pl_min
    59	
    60	        return {
    61	            "engine": self.engine_name,
    62	            "status": "ok",
    63	            "structure_id": pricing_payload.get("structure_id"),
    64	            "underlying_asset": pricing_payload.get("underlying_asset"),
    65	            "reference_date": pricing_payload.get("reference_date"),
    66	            "metrics": {
    67	                "number_of_legs": number_of_legs,
    68	                "total_quantity": total_quantity,
    69	                "spot_price": spot_price,
    70	                "interest_rate": float(pricing_payload.get("interest_rate") or 0.0),
    71	                "volatility": float(pricing_payload.get("volatility") or 0.0),
    72	                "payoff_points": len(payoff.get("points") or []),
    73	                "pl_max": pl_max,
    74	                "pl_min": pl_min,
    75	                "pl_atual": pl_atual,
    76	            },
    77	            "valuation": {
    78	                "theoretical_value": pl_atual,
    79	                "premium_paid": premium_paid,
    80	                "max_profit": max_profit,
    81	                "max_loss": max_loss,
    82	                "pl_max": pl_max,
    83	                "pl_min": pl_min,
    84	                "pl_atual": pl_atual,
    85	                "method": "expiration_payoff_grid",
    86	            },
    87	            "payoff": payoff,
    88	        }
    89	
    90	    @staticmethod
    91	    def _normalize_leg(leg: dict[str, Any]) -> dict[str, Any]:
    92	        normalized = dict(leg)
    93	
    94	        side = (
    95	            normalized.get("position_side")
    96	            or normalized.get("side")
    97	            or normalized.get("direction")
    98	        )
    99	        normalized["position_side"] = to_pricing_engine_side(side)
   100	
   101	        normalized["option_type"] = str(
   102	            normalized.get("option_type")
   103	            or normalized.get("type")
   104	            or normalized.get("kind")
   105	            or ""
   106	        ).strip().upper()
   107	
   108	        normalized["strike"] = float(normalized.get("strike") or 0.0)
   109	        normalized["quantity"] = float(normalized.get("quantity") or 0.0)
   110	        normalized["multiplier"] = float(normalized.get("multiplier") or 1.0)
   111	
   112	        premium = (
   113	            normalized.get("premium")
   114	            if normalized.get("premium") is not None
   115	            else normalized.get("entry_price")
   116	        )
   117	        if premium is None:
   118	            premium = normalized.get("price")
   119	        if premium is None:
   120	            premium = normalized.get("last_price")
   121	        if premium is None:
   122	            premium = 0.0
   123	
   124	        normalized["premium"] = float(premium)
   125	
   126	        return normalized
   127	
   128	    @staticmethod
   129	    def _intrinsic_value(option_type: str, strike: float, spot: float) -> float:
   130	        if option_type == "CALL":
   131	            return max(spot - strike, 0.0)
   132	        if option_type == "PUT":
   133	            return max(strike - spot, 0.0)
   134	        return 0.0
   135	
   136	    def _compute_pl_at_spot(
   137	        self,
   138	        legs: list[dict[str, Any]],
   139	        spot_price: float,
   140	    ) -> float:
   141	        total = 0.0
   142	
   143	        for leg in legs:
   144	            intrinsic = self._intrinsic_value(
   145	                option_type=str(leg.get("option_type") or "").upper(),
   146	                strike=float(leg.get("strike") or 0.0),
   147	                spot=spot_price,
   148	            )
   149	
   150	            premium = float(leg.get("premium") or 0.0)
   151	            quantity = float(leg.get("quantity") or 0.0)
   152	            multiplier = float(leg.get("multiplier") or 1.0)
   153	
   154	            unit_pl = intrinsic - premium
   155	
   156	            if leg.get("position_side") == "SHORT":
   157	                unit_pl = -unit_pl
   158	
   159	            total += unit_pl * quantity * multiplier
   160	
   161	        return round(float(total), 6)
   162	
   163	    @staticmethod
   164	    def _compute_net_premium_paid(legs: list[dict[str, Any]]) -> float:
   165	        total = 0.0
   166	
   167	        for leg in legs:
   168	            premium = float(leg.get("premium") or 0.0)
   169	            quantity = float(leg.get("quantity") or 0.0)
   170	            multiplier = float(leg.get("multiplier") or 1.0)
   171	
   172	            amount = premium * quantity * multiplier
   173	
   174	            if leg.get("position_side") == "SHORT":
   175	                amount = -amount
   176	
   177	            total += amount
   178	
   179	        return round(float(total), 6)
```

## FILE: services/structure_analysis_service.py
```python
     1	# services/structure_analysis_service.py
     2	from __future__ import annotations
     3	
     4	from typing import Any, Dict, Optional
     5	
     6	from domain.decision import compute_decision_from_payoff
     7	from domain.payoff import compute_payoff_from_canonical_input
     8	from domain.structure_metrics import (
     9	    compute_dte_min_from_canonical_input,
    10	    compute_structure_metrics_from_canonical_input,
    11	)
    12	
    13	
    14	class StructureAnalysisService:
    15	    def __init__(self, canonical_input_service):
    16	        self._canonical_input_service = canonical_input_service
    17	
    18	    def analyze(
    19	        self,
    20	        structure_id: int,
    21	        reference_date: Optional[str] = None,
    22	        dte_min: Optional[int] = None,
    23	        spread_pct_medio: Optional[float] = None,
    24	        thresholds: Optional[Dict[str, float]] = None,
    25	        dte_gate: int = 7,
    26	    ) -> Dict[str, Any]:
    27	
    28	        # 1. Busca input canônico
    29	        canonical_input = self._canonical_input_service.build_structure_market_input(
    30	            structure_id=structure_id,
    31	            reference_date=reference_date,
    32	        )
    33	
    34	        # 2. Calcula métricas internas da estrutura
    35	        structure_metrics = compute_structure_metrics_from_canonical_input(canonical_input)
    36	
    37	        # 3. Calcula DTE inferido preservando o contrato legado
    38	        #
    39	        # Mantemos compute_dte_min_from_canonical_input como fonte explícita do
    40	        # dte_min_inferred para compatibilidade com testes e integrações já
    41	        # existentes. O motor novo também calcula dte_min, mas nesta etapa ele é
    42	        # exposto dentro de structure_metrics.
    43	        dte_min_inferred = compute_dte_min_from_canonical_input(canonical_input)
    44	
    45	        # 4. DTE efetivo: explícito > inferido > 0
    46	        if dte_min is not None:
    47	            dte_min_effective = dte_min
    48	        elif dte_min_inferred is not None:
    49	            dte_min_effective = dte_min_inferred
    50	        else:
    51	            dte_min_effective = 0
    52	
    53	        # 5. Spread efetivo: explícito > calculado internamente
    54	        spread_pct_medio_inferred = structure_metrics.get("spread_pct_medio")
    55	
    56	        if spread_pct_medio is not None:
    57	            spread_pct_medio_effective = spread_pct_medio
    58	        else:
    59	            spread_pct_medio_effective = spread_pct_medio_inferred
    60	
    61	        # 6. Calcula payoff
    62	        payoff = compute_payoff_from_canonical_input(canonical_input)
    63	
    64	        # 7. Valida payoff -- se inválido, retorna HOLD com erro estruturado
    65	        if not payoff or not payoff.get("pl_max"):
    66	            why_dict = {
    67	                "error": "payoff is required",
    68	                "validation_errors": ["pl_max ausente ou zero"],
    69	                "reasons": ["invalid_payoff"],
    70	                "alternatives": [],
    71	            }
    72	            decision = {
    73	                "decision":      "HOLD",
    74	                "level":         0,
    75	                "ratio":         0.0,
    76	                "pl_pct_of_max": 0.0,
    77	                "dte_min":       dte_min_effective,
    78	                "why":           why_dict,
    79	                "why_json":      "{}",
    80	                "alternatives":  [],
    81	            }
    82	            return {
    83	                "canonical_input": canonical_input,
    84	                "metrics": {
    85	                    "dte_min_inferred":             dte_min_inferred,
    86	                    "dte_min_effective":            dte_min_effective,
    87	                    "spread_pct_medio":             spread_pct_medio_effective,
    88	                    "spread_pct_medio_inferred":    spread_pct_medio_inferred,
    89	                    "structure_metrics":            structure_metrics,
    90	                },
    91	                "payoff":   payoff,
    92	                "decision": decision,
    93	            }
    94	
    95	        # 8. Computa decisão -- passa TODOS os parâmetros como keyword
    96	        decision = compute_decision_from_payoff(
    97	            payoff=payoff,
    98	            dte_min=dte_min_effective,
    99	            spread_pct_medio=spread_pct_medio_effective,
   100	            thresholds=thresholds,
   101	            dte_gate=dte_gate,
   102	        )
   103	
   104	        # 9. Injeta dte_min no retorno (esperado pelos testes)
   105	        decision["dte_min"] = dte_min_effective
   106	
   107	        # 10. Injeta dte_gate em why (esperado por test_propagates_custom_thresholds_and_dte_gate)
   108	        decision["why"]["dte_gate"] = dte_gate
   109	
   110	        return {
   111	            "canonical_input": canonical_input,
   112	            "metrics": {
   113	                "dte_min_inferred":             dte_min_inferred,
   114	                "dte_min_effective":            dte_min_effective,
   115	                "spread_pct_medio":             spread_pct_medio_effective,
   116	                "spread_pct_medio_inferred":    spread_pct_medio_inferred,
   117	                "structure_metrics":            structure_metrics,
   118	            },
   119	            "payoff":   payoff,
   120	            "decision": decision,
   121	        }
```

## FILE: services/pricing_execution_persistence_service.py
```python
     1	# services/pricing_execution_persistence_service.py
     2	import logging
     3	from typing import Any
     4	
     5	from repositories.pricing_executions_repository import PricingExecutionsRepository
     6	from repositories.system_snapshots_repository import SystemSnapshotsRepository
     7	from services.payoff_persistence_port import PayoffPersistencePort
     8	
     9	logger = logging.getLogger(__name__)
    10	
    11	
    12	class PricingExecutionPersistenceService:
    13	    def __init__(
    14	        self,
    15	        pricing_executions_repository: PricingExecutionsRepository | None = None,
    16	        payoff_persistence_port: PayoffPersistencePort | None = None,
    17	        system_snapshots_repository: SystemSnapshotsRepository | None = None,
    18	    ):
    19	        self.pricing_executions_repository = (
    20	            pricing_executions_repository or PricingExecutionsRepository()
    21	        )
    22	        self._payoff_port = payoff_persistence_port
    23	        self._system_snapshots_repository = system_snapshots_repository
    24	
    25	    def persist_execution(
    26	        self,
    27	        pricing_payload: dict[str, Any] | None,
    28	        result: dict[str, Any],
    29	        duration_ms: int | None = None,
    30	        error_message: str | None = None,
    31	    ) -> dict[str, Any]:
    32	        # result pode chegar como wrapper {"result": {...}} ou já desempacotado
    33	        inner = result.get("result", result) if isinstance(result, dict) else result
    34	        metrics = inner.get("metrics", {}) if isinstance(inner, dict) else {}
    35	        valuation = inner.get("valuation", {}) if isinstance(inner, dict) else {}
    36	
    37	        execution_engine = inner.get("engine") if isinstance(inner, dict) else None
    38	        execution_status = inner.get("status") if isinstance(inner, dict) else None
    39	        persisted_error_message = error_message or (
    40	            inner.get("error_message") if isinstance(inner, dict) else None
    41	        )
    42	        number_of_legs = metrics.get("number_of_legs")
    43	        total_quantity = metrics.get("total_quantity")
    44	        theoretical_value = valuation.get("theoretical_value")
    45	
    46	        record = self.pricing_executions_repository.save_execution(
    47	            pricing_payload=pricing_payload,
    48	            result=result,
    49	            execution_status=execution_status,
    50	            execution_engine=execution_engine,
    51	            error_message=persisted_error_message,
    52	            duration_ms=duration_ms,
    53	            number_of_legs=number_of_legs,
    54	            total_quantity=total_quantity,
    55	            theoretical_value=theoretical_value,
    56	        )
    57	
    58	        snapshot_id = self._create_system_snapshot_if_applicable(
    59	            record=record,
    60	            pricing_payload=pricing_payload,
    61	            result=result,
    62	            inner=inner,
    63	            execution_status=execution_status,
    64	        )
    65	
    66	        # ------------------------------------------------------------------ #
    67	        #  alteracao_21 -- persistência derivada (payoff + decisão)           #
    68	        #  Fire-and-forget: falha aqui nunca derruba a execução principal.    #
    69	        # ------------------------------------------------------------------ #
    70	        if self._payoff_port is not None:
    71	            try:
    72	                self._payoff_port.persist(
    73	                    pricing_payload=pricing_payload,
    74	                    result=result,
    75	                )
    76	            except Exception:
    77	                logger.exception(
    78	                    "payoff_persistence_port.persist() falhou -- execução id=%s não afetada",
    79	                    record.get("id"),
    80	                )
    81	
    82	        response = {
    83	            "record": record,
    84	        }
    85	
    86	        if snapshot_id is not None:
    87	            response["snapshot_id"] = snapshot_id
    88	
    89	        return response
    90	
    91	    def _create_system_snapshot_if_applicable(
    92	        self,
    93	        *,
    94	        record: dict[str, Any],
    95	        pricing_payload: dict[str, Any] | None,
    96	        result: dict[str, Any],
    97	        inner: Any,
    98	        execution_status: str | None,
    99	    ) -> int | None:
   100	        if self._system_snapshots_repository is None:
   101	            return None
   102	
   103	        if not pricing_payload:
   104	            return None
   105	
   106	        if execution_status != "ok":
   107	            return None
   108	
   109	        structure_id = pricing_payload.get("structure_id") or record.get("structure_id")
   110	        if not structure_id:
   111	            return None
   112	
   113	        try:
   114	            return self._system_snapshots_repository.create_snapshot(
   115	                structure_id=int(structure_id),
   116	                pricing_execution_id=record.get("id"),
   117	                underlying_asset=pricing_payload.get("underlying_asset"),
   118	                reference_date=pricing_payload.get("reference_date"),
   119	                snapshot_source="system_pricing_execution",
   120	                structure_json=self._build_structure_json(pricing_payload),
   121	                legs=pricing_payload.get("legs") or [],
   122	                market_json=self._build_market_json(pricing_payload),
   123	                metrics_json=self._extract_result_field(inner, "metrics"),
   124	                payoff_json=self._extract_result_field(inner, "payoff"),
   125	                decision_json=self._extract_result_field(inner, "decision"),
   126	                alerts_json=self._extract_result_field(inner, "alerts"),
   127	                operation_state_json={
   128	                    "pricing_execution": record,
   129	                    "pricing_payload": pricing_payload,
   130	                    "result": result,
   131	                },
   132	            )
   133	        except Exception:
   134	            logger.exception(
   135	                "system_snapshots_repository.create_snapshot() falhou -- execução id=%s não afetada",
   136	                record.get("id"),
   137	            )
   138	            return None
   139	
   140	    @staticmethod
   141	    def _build_structure_json(pricing_payload: dict[str, Any]) -> dict[str, Any]:
   142	        return {
   143	            "structure_id": pricing_payload.get("structure_id"),
   144	            "structure_name": pricing_payload.get("structure_name"),
   145	            "underlying_asset": pricing_payload.get("underlying_asset"),
   146	            "reference_date": pricing_payload.get("reference_date"),
   147	            "meta": pricing_payload.get("meta"),
   148	        }
   149	
   150	    @staticmethod
   151	    def _build_market_json(pricing_payload: dict[str, Any]) -> dict[str, Any]:
   152	        return {
   153	            "spot_price": pricing_payload.get("spot_price"),
   154	            "interest_rate": pricing_payload.get("interest_rate"),
   155	            "volatility": pricing_payload.get("volatility"),
   156	        }
   157	
   158	    @staticmethod
   159	    def _extract_result_field(inner: Any, field: str) -> Any:
   160	        if not isinstance(inner, dict):
   161	            return None
   162	
   163	        value = inner.get(field)
   164	        return value if value not in ({}, [], None) else None
```

## FILE: services/pricing_execution_app_service.py
```python
     1	# services/pricing_execution_app_service.py
     2	"""
     3	alteracao_18 -- execute_pricing() delegado para CanonicalPricingFacade.
     4	
     5	Alterações:
     6	  - execute_pricing() agora usa CanonicalPricingFacade (manual > rtd, caminho canônico)
     7	  - PricingExecutionOrchestrationService removido do __init__ (não mais necessário aqui)
     8	  - Todos os métodos de query (list, get, paginate, latest) inalterados
     9	  - Validações _validate_structure_id / _validate_reference_date mantidas
    10	"""
    11	
    12	from datetime import datetime
    13	from pathlib import Path
    14	from typing import Any
    15	
    16	from services.canonical_pricing_facade import CanonicalPricingFacade
    17	from services.pricing_execution_query_service import PricingExecutionQueryService
    18	
    19	_DEFAULT_DB = Path("dados/app.db")
    20	
    21	
    22	class PricingExecutionAppService:
    23	    def __init__(
    24	        self,
    25	        canonical_pricing_facade: CanonicalPricingFacade | None = None,
    26	        pricing_execution_query_service: PricingExecutionQueryService | None = None,
    27	        db_path: Path | str = _DEFAULT_DB,
    28	    ):
    29	        self._facade = canonical_pricing_facade or CanonicalPricingFacade(
    30	            db_path=db_path,
    31	        )
    32	        self.pricing_execution_query_service = (
    33	            pricing_execution_query_service or PricingExecutionQueryService()
    34	        )
    35	
    36	    # ------------------------------------------------------------------
    37	    # Execução
    38	    # ------------------------------------------------------------------
    39	
    40	    def execute_pricing(
    41	        self,
    42	        structure_id: int,
    43	        reference_date: str | None = None,
    44	    ) -> dict[str, Any]:
    45	        self._validate_structure_id(structure_id)
    46	        self._validate_reference_date(reference_date)
    47	
    48	        response = self._facade.execute_pricing(
    49	            structure_id=structure_id,
    50	            reference_date=reference_date,
    51	        )
    52	
    53	        # propaga erros como ValueError para manter contrato com callers existentes
    54	        if response.get("status") == "error":
    55	            raise ValueError(response.get("error_message", "pricing execution failed"))
    56	
    57	        persisted = response.get("persisted")
    58	        if isinstance(persisted, dict):
    59	            record = persisted.get("record")
    60	            if isinstance(record, dict):
    61	                return record
    62	
    63	        return response
    64	
    65	    # ------------------------------------------------------------------
    66	    # Queries -- inalteradas
    67	    # ------------------------------------------------------------------
    68	
    69	    def list_execution_summaries(
    70	        self,
    71	        structure_id: int | None = None,
    72	        underlying_asset: str | None = None,
    73	        status: str | None = None,
    74	        reference_date: str | None = None,
    75	        descending: bool = True,
    76	    ) -> list[dict[str, Any]]:
    77	        return self.pricing_execution_query_service.list_execution_summaries(
    78	            structure_id=structure_id,
    79	            underlying_asset=underlying_asset,
    80	            status=status,
    81	            reference_date=reference_date,
    82	            descending=descending,
    83	        )
    84	
    85	    def get_latest_execution_summary(
    86	        self,
    87	        structure_id: int | None = None,
    88	        underlying_asset: str | None = None,
    89	        status: str | None = None,
    90	        reference_date: str | None = None,
    91	    ) -> dict[str, Any]:
    92	        return self.pricing_execution_query_service.get_latest_execution_summary(
    93	            structure_id=structure_id,
    94	            underlying_asset=underlying_asset,
    95	            status=status,
    96	            reference_date=reference_date,
    97	        )
    98	
    99	    def get_execution(self, execution_id: int) -> dict[str, Any]:
   100	        return self.pricing_execution_query_service.get_execution(execution_id)
   101	
   102	    def paginate_execution_summaries(
   103	        self,
   104	        structure_id: int | None = None,
   105	        underlying_asset: str | None = None,
   106	        status: str | None = None,
   107	        reference_date: str | None = None,
   108	        descending: bool = True,
   109	        page: int = 1,
   110	        page_size: int = 10,
   111	    ) -> dict[str, Any]:
   112	        return self.pricing_execution_query_service.paginate_execution_summaries(
   113	            structure_id=structure_id,
   114	            underlying_asset=underlying_asset,
   115	            status=status,
   116	            reference_date=reference_date,
   117	            descending=descending,
   118	            page=page,
   119	            page_size=page_size,
   120	        )
   121	
   122	    # ------------------------------------------------------------------
   123	    # Validações
   124	    # ------------------------------------------------------------------
   125	
   126	    def _validate_structure_id(self, structure_id: int) -> None:
   127	        if structure_id <= 0:
   128	            raise ValueError("structure_id must be greater than zero")
   129	
   130	    def _validate_reference_date(self, reference_date: str | None) -> None:
   131	        if reference_date is None:
   132	            return
   133	
   134	        try:
   135	            parsed = datetime.strptime(reference_date, "%Y-%m-%d")
   136	        except ValueError as exc:
   137	            raise ValueError("reference_date must be in YYYY-MM-DD format") from exc
   138	
   139	        if parsed.strftime("%Y-%m-%d") != reference_date:
   140	            raise ValueError("reference_date must be in YYYY-MM-DD format")
```

## FILE: services/pricing_execution_orchestration_service.py
```python
     1	import time
     2	from typing import Any
     3	
     4	from repositories.system_snapshots_repository import SystemSnapshotsRepository
     5	from services.pricing_execution_persistence_service import (
     6	    PricingExecutionPersistenceService,
     7	)
     8	from services.pricing_execution_service import PricingExecutionService
     9	from services.pricing_input_service import PricingInputService
    10	
    11	
    12	class PricingExecutionOrchestrationService:
    13	    def __init__(
    14	        self,
    15	        pricing_input_service: PricingInputService | None = None,
    16	        pricing_execution_service: PricingExecutionService | None = None,
    17	        pricing_execution_persistence_service: PricingExecutionPersistenceService | None = None,
    18	    ):
    19	        self.pricing_input_service = pricing_input_service or PricingInputService()
    20	        self.pricing_execution_service = pricing_execution_service or PricingExecutionService(
    21	            pricing_input_service=self.pricing_input_service,
    22	        )
    23	        self.pricing_execution_persistence_service = (
    24	            pricing_execution_persistence_service
    25	            or PricingExecutionPersistenceService(
    26	                system_snapshots_repository=SystemSnapshotsRepository(),
    27	            )
    28	        )
    29	
    30	    def execute_and_persist(
    31	        self,
    32	        structure_id: int,
    33	        reference_date: str | None = None,
    34	    ) -> dict[str, Any]:
    35	        started_at = time.perf_counter()
    36	
    37	        try:
    38	            result = self.pricing_execution_service.execute(
    39	                structure_id=structure_id,
    40	                reference_date=reference_date,
    41	            )
    42	            duration_ms = int((time.perf_counter() - started_at) * 1000)
    43	
    44	            persisted = self.pricing_execution_persistence_service.persist_execution(
    45	                pricing_payload=result["pricing_payload"],
    46	                result=result,
    47	                duration_ms=duration_ms,
    48	                error_message=None,
    49	            )
    50	
    51	            return {
    52	                "pricing_payload": result["pricing_payload"],
    53	                "result": result,
    54	                "persisted": persisted,
    55	            }
    56	
    57	        except Exception as exc:
    58	            duration_ms = int((time.perf_counter() - started_at) * 1000)
    59	            error_message = str(exc)
    60	
    61	            result = {
    62	                "pricing_payload": None,
    63	                "result": {
    64	                    "engine": "payoff_pricing_engine",
    65	                    "status": "error",
    66	                    "error_message": error_message,
    67	                },
    68	            }
    69	
    70	            persisted = self.pricing_execution_persistence_service.persist_execution(
    71	                pricing_payload=None,
    72	                result=result,
    73	                duration_ms=duration_ms,
    74	                error_message=error_message,
    75	            )
    76	
    77	            return {
    78	                "pricing_payload": None,
    79	                "result": result,
    80	                "persisted": persisted,
    81	            }
```

## FILE: services/pricing_execution_query_service.py
```python
     1	from datetime import datetime
     2	from typing import Any
     3	
     4	from repositories.pricing_executions_repository import PricingExecutionsRepository
     5	
     6	
     7	class PricingExecutionQueryService:
     8	    def __init__(
     9	        self,
    10	        pricing_executions_repository: PricingExecutionsRepository | None = None,
    11	    ):
    12	        self.pricing_executions_repository = (
    13	            pricing_executions_repository or PricingExecutionsRepository()
    14	        )
    15	
    16	    def _validate_summary_filters(
    17	        self,
    18	        structure_id: int | None = None,
    19	        underlying_asset: str | None = None,
    20	        status: str | None = None,
    21	        reference_date: str | None = None,
    22	    ) -> None:
    23	        if structure_id is not None and structure_id <= 0:
    24	            raise ValueError("structure_id must be greater than zero")
    25	
    26	        if underlying_asset is not None and not underlying_asset.strip():
    27	            raise ValueError("underlying_asset must not be empty")
    28	
    29	        if status is not None and status not in {"ok", "error"}:
    30	            raise ValueError("status must be either 'ok' or 'error'")
    31	
    32	        if reference_date is not None:
    33	            if not reference_date.strip():
    34	                raise ValueError("reference_date must not be empty")
    35	
    36	            try:
    37	                datetime.strptime(reference_date, "%Y-%m-%d")
    38	            except ValueError as exc:
    39	                raise ValueError(
    40	                    "reference_date must be in YYYY-MM-DD format"
    41	                ) from exc
    42	
    43	    def list_executions(self) -> list[dict[str, Any]]:
    44	        return self.pricing_executions_repository.list_executions()
    45	
    46	    def _load_executions_for_summary(
    47	        self,
    48	        structure_id: int | None = None,
    49	        status: str | None = None,
    50	        reference_date: str | None = None,
    51	    ) -> list[dict[str, Any]]:
    52	        """
    53	        Compatibilidade:
    54	        - repositório real pode aceitar page/page_size/filtros;
    55	        - fakes antigos dos testes aceitam list_executions() sem kwargs.
    56	        """
    57	        try:
    58	            executions = self.pricing_executions_repository.list_executions(
    59	                page=1,
    60	                page_size=10_000,
    61	                status=status,
    62	                structure_id=structure_id,
    63	                reference_date=reference_date,
    64	            )
    65	        except TypeError as exc:
    66	            if "unexpected keyword argument" not in str(exc):
    67	                raise
    68	            executions = self.pricing_executions_repository.list_executions()
    69	
    70	        if isinstance(executions, dict):
    71	            executions = executions.get("items", [])
    72	
    73	        return list(executions or [])
    74	
    75	    def list_execution_summaries(
    76	        self,
    77	        structure_id: int | None = None,
    78	        underlying_asset: str | None = None,
    79	        status: str | None = None,
    80	        reference_date: str | None = None,
    81	        descending: bool = True,
    82	    ) -> list[dict[str, Any]]:
    83	        self._validate_summary_filters(
    84	            structure_id=structure_id,
    85	            underlying_asset=underlying_asset,
    86	            status=status,
    87	            reference_date=reference_date,
    88	        )
    89	
    90	        executions = self._load_executions_for_summary(
    91	            structure_id=structure_id,
    92	            status=status,
    93	            reference_date=reference_date,
    94	        )
    95	
    96	        summaries = []
    97	        for execution in executions:
    98	            persisted_number_of_legs = execution.get("number_of_legs")
    99	            persisted_total_quantity = execution.get("total_quantity")
   100	            persisted_theoretical_value = execution.get("theoretical_value")
   101	
   102	            nested_result = execution.get("result", {}) or {}
   103	            engine_result = nested_result.get("result", nested_result)
   104	            metrics = engine_result.get("metrics", {}) or {}
   105	            valuation = engine_result.get("valuation", {}) or {}
   106	
   107	            summary = {
   108	                "id": execution["id"],
   109	                "created_at": execution["created_at"],
   110	                "structure_id": execution["structure_id"],
   111	                "underlying_asset": execution["underlying_asset"],
   112	                "reference_date": execution["reference_date"],
   113	                "execution_engine": execution.get("execution_engine"),
   114	                "execution_status": execution.get("execution_status"),
   115	                "duration_ms": execution.get("duration_ms"),
   116	                "error_message": execution.get("error_message"),
   117	                "number_of_legs": (
   118	                    persisted_number_of_legs
   119	                    if persisted_number_of_legs is not None
   120	                    else metrics.get("number_of_legs")
   121	                ),
   122	                "total_quantity": (
   123	                    persisted_total_quantity
   124	                    if persisted_total_quantity is not None
   125	                    else metrics.get("total_quantity")
   126	                ),
   127	                "theoretical_value": (
   128	                    persisted_theoretical_value
   129	                    if persisted_theoretical_value is not None
   130	                    else valuation.get("theoretical_value")
   131	                ),
   132	            }
   133	
   134	            if structure_id is not None and summary["structure_id"] != structure_id:
   135	                continue
   136	
   137	            if underlying_asset is not None:
   138	                if str(summary["underlying_asset"]).upper() != underlying_asset.upper():
   139	                    continue
   140	
   141	            if status is not None and summary["execution_status"] != status:
   142	                continue
   143	
   144	            if reference_date is not None and summary["reference_date"] != reference_date:
   145	                continue
   146	
   147	            summaries.append(summary)
   148	
   149	        summaries.sort(key=lambda item: item["id"], reverse=descending)
   150	        return summaries
   151	
   152	    def paginate_execution_summaries(
   153	        self,
   154	        structure_id: int | None = None,
   155	        underlying_asset: str | None = None,
   156	        status: str | None = None,
   157	        reference_date: str | None = None,
   158	        descending: bool = True,
   159	        page: int = 1,
   160	        page_size: int = 10,
   161	    ) -> dict[str, Any]:
   162	        self._validate_summary_filters(
   163	            structure_id=structure_id,
   164	            underlying_asset=underlying_asset,
   165	            status=status,
   166	            reference_date=reference_date,
   167	        )
   168	
   169	        if page <= 0:
   170	            raise ValueError("page must be greater than zero")
   171	
   172	        if page_size <= 0:
   173	            raise ValueError("page_size must be greater than zero")
   174	
   175	        summaries = self.list_execution_summaries(
   176	            structure_id=structure_id,
   177	            underlying_asset=underlying_asset,
   178	            status=status,
   179	            reference_date=reference_date,
   180	            descending=descending,
   181	        )
   182	
   183	        total_items = len(summaries)
   184	        total_pages = (
   185	            (total_items + page_size - 1) // page_size if total_items > 0 else 0
   186	        )
   187	
   188	        start = (page - 1) * page_size
   189	        end = start + page_size
   190	        items = summaries[start:end]
   191	
   192	        return {
   193	            "items": items,
   194	            "page": page,
   195	            "page_size": page_size,
   196	            "total_items": total_items,
   197	            "total_pages": total_pages,
   198	        }
   199	
   200	    def get_latest_execution_summary(
   201	        self,
   202	        structure_id: int | None = None,
   203	        underlying_asset: str | None = None,
   204	        status: str | None = None,
   205	        reference_date: str | None = None,
   206	    ) -> dict[str, Any]:
   207	        self._validate_summary_filters(
   208	            structure_id=structure_id,
   209	            underlying_asset=underlying_asset,
   210	            status=status,
   211	            reference_date=reference_date,
   212	        )
   213	
   214	        summaries = self.list_execution_summaries(
   215	            structure_id=structure_id,
   216	            underlying_asset=underlying_asset,
   217	            status=status,
   218	            reference_date=reference_date,
   219	            descending=True,
   220	        )
   221	
   222	        if not summaries:
   223	            raise ValueError("no pricing execution summaries found")
   224	
   225	        return summaries[0]
   226	
   227	    def get_execution(self, execution_id: int) -> dict[str, Any]:
   228	        if execution_id <= 0:
   229	            raise ValueError("execution_id must be greater than zero")
   230	
   231	        execution = self.pricing_executions_repository.get_execution(execution_id)
   232	
   233	        if execution is None:
   234	            raise ValueError(f"pricing execution {execution_id} not found")
   235	
   236	        return execution
   237	
   238	    def get_execution_details(self, execution_id: int) -> dict[str, Any]:
   239	        return self.get_execution(execution_id)
```

## FILE: domain/payoff.py
```python
     1	from typing import Any
     2	
     3	from domain.canonical_validators import validate_canonical_input
     4	from domain.position_side import to_pricing_engine_side
     5	
     6	
     7	def _round_money(value: float, digits: int = 6) -> float:
     8	    return round(float(value), digits)
     9	
    10	
    11	def _normalize_side(value: Any) -> str:
    12	    return to_pricing_engine_side(value)
    13	
    14	
    15	def _normalize_option_type(value: Any) -> str:
    16	    return str(value or "").strip().upper()
    17	
    18	
    19	def _intrinsic_value(option_type: str, strike: float, spot_at_expiration: float) -> float:
    20	    if option_type == "CALL":
    21	        return max(spot_at_expiration - strike, 0.0)
    22	    if option_type == "PUT":
    23	        return max(strike - spot_at_expiration, 0.0)
    24	    return 0.0
    25	
    26	
    27	def _compute_leg_payoff_at_expiration(leg: dict[str, Any], spot_at_expiration: float) -> float:
    28	    position_side = _normalize_side(leg.get("position_side"))
    29	    option_type = _normalize_option_type(leg.get("option_type"))
    30	
    31	    strike = float(leg.get("strike") or 0.0)
    32	    quantity = float(leg.get("quantity") or 0.0)
    33	    multiplier = float(leg.get("multiplier") or 1.0)
    34	    premium = leg.get("premium")
    35	    premium_value = float(premium) if premium is not None else 0.0
    36	
    37	    intrinsic = _intrinsic_value(
    38	        option_type=option_type,
    39	        strike=strike,
    40	        spot_at_expiration=spot_at_expiration,
    41	    )
    42	
    43	    payoff_unit = intrinsic - premium_value
    44	
    45	    if position_side == "SHORT":
    46	        payoff_unit = -payoff_unit
    47	
    48	    return payoff_unit * quantity * multiplier
    49	
    50	
    51	def compute_payoff_curve_from_canonical_legs(
    52	    legs: list[dict[str, Any]],
    53	    spot_ref: float,
    54	    low_pct: float = 0.5,
    55	    high_pct: float = 1.5,
    56	    step_pct: float = 0.01,
    57	) -> dict[str, Any]:
    58	    if not legs:
    59	        return {
    60	            "points": [],
    61	            "pl_max": 0.0,
    62	            "pl_min": 0.0,
    63	            "spot_ref": _round_money(spot_ref, 6),
    64	            "meta": {
    65	                "legs_count": 0,
    66	                "input_type": "canonical_legs",
    67	                "grid_params": {
    68	                    "low_pct": low_pct,
    69	                    "high_pct": high_pct,
    70	                    "step_pct": step_pct,
    71	                },
    72	            },
    73	        }
    74	
    75	    s_min = float(spot_ref) * float(low_pct)
    76	    s_max = float(spot_ref) * float(high_pct)
    77	    step = float(spot_ref) * float(step_pct)
    78	
    79	    if step <= 0:
    80	        step = 1.0
    81	
    82	    points: list[tuple[float, float]] = []
    83	    pl_values: list[float] = []
    84	
    85	    s_t = s_min
    86	    while s_t <= s_max + (step / 2):
    87	        pl_total = 0.0
    88	
    89	        for leg in legs:
    90	            pl_total += _compute_leg_payoff_at_expiration(
    91	                leg=leg,
    92	                spot_at_expiration=s_t,
    93	            )
    94	
    95	        s_t_rounded = _round_money(s_t, 6)
    96	        pl_total_rounded = _round_money(pl_total, 6)
    97	
    98	        points.append((s_t_rounded, pl_total_rounded))
    99	        pl_values.append(pl_total_rounded)
   100	
   101	        s_t += step
   102	
   103	    pl_max = _round_money(max(pl_values), 6) if pl_values else 0.0
   104	    pl_min = _round_money(min(pl_values), 6) if pl_values else 0.0
   105	
   106	    return {
   107	        "points": points,
   108	        "pl_max": pl_max,
   109	        "pl_min": pl_min,
   110	        "spot_ref": _round_money(spot_ref, 6),
   111	        "meta": {
   112	            "legs_count": len(legs),
   113	            "input_type": "canonical_legs",
   114	            "grid_params": {
   115	                "low_pct": low_pct,
   116	                "high_pct": high_pct,
   117	                "step_pct": step_pct,
   118	            },
   119	        },
   120	    }
   121	
   122	
   123	def compute_payoff_from_canonical_input(
   124	    canonical_input: dict[str, Any],
   125	    low_pct: float = 0.5,
   126	    high_pct: float = 1.5,
   127	    step_pct: float = 0.01,
   128	) -> dict[str, Any]:
   129	    structure = canonical_input.get("structure") or {}
   130	    market = canonical_input.get("market") or {}
   131	    input_meta = canonical_input.get("meta") or {}
   132	
   133	    errors = validate_canonical_input(canonical_input)
   134	    if errors:
   135	        return {
   136	            "points": [],
   137	            "pl_max": 0.0,
   138	            "pl_min": 0.0,
   139	            "spot_ref": float(market.get("spot_price") or 0.0),
   140	            "meta": {
   141	                "input_type": "canonical_legs",
   142	                "validation_errors": errors,
   143	            },
   144	            "structure_id": structure.get("structure_id"),
   145	            "structure_name": structure.get("name"),
   146	            "underlying_asset": (
   147	                market.get("underlying_asset")
   148	                or structure.get("underlying_asset")
   149	            ),
   150	            "reference_date": market.get("reference_date") or input_meta.get("reference_date"),
   151	            "input_meta": input_meta,
   152	        }
   153	
   154	    legs = structure.get("legs") or []
   155	    spot_ref = float(market.get("spot_price") or 0.0)
   156	
   157	    result = compute_payoff_curve_from_canonical_legs(
   158	        legs=legs,
   159	        spot_ref=spot_ref,
   160	        low_pct=low_pct,
   161	        high_pct=high_pct,
   162	        step_pct=step_pct,
   163	    )
   164	
   165	    return {
   166	        **result,
   167	        "structure_id": structure.get("structure_id"),
   168	        "structure_name": structure.get("name"),
   169	        "underlying_asset": (
   170	            market.get("underlying_asset")
   171	            or structure.get("underlying_asset")
   172	        ),
   173	        "reference_date": market.get("reference_date") or input_meta.get("reference_date"),
   174	        "input_meta": input_meta,
   175	    }
```

## FILE: domain/decision.py
```python
     1	#!/usr/bin/env python3
     2	"""
     3	Domain: Decision logic (30/60/80 thresholds + DTE gate) from real data.
     4	
     5	Codigo legado removido neste modulo.
     6	Funcoes canonicas: compute_decision_from_inputs, compute_decision_from_payoff,
     7	compute_decision_from_contract.
     8	"""
     9	from __future__ import annotations
    10	
    11	import json
    12	import math
    13	from typing import Any, Dict, List, Optional, Tuple
    14	
    15	from domain.contracts import CanonicalStructureMarketInput
    16	
    17	
    18	# ---------------------------------------------------------------------------
    19	# Constantes de decisão
    20	# ---------------------------------------------------------------------------
    21	THRESHOLD_CLOSE   = 0.80
    22	THRESHOLD_PREPARE = 0.60
    23	THRESHOLD_WATCH   = 0.30
    24	
    25	DTE_GATE_DEFAULT  = 7
    26	
    27	
    28	# ---------------------------------------------------------------------------
    29	# Helpers internos (exportados para testes de interpolação)
    30	# ---------------------------------------------------------------------------
    31	
    32	def _interp_payoff(points: List[Tuple[float, float]], spot: float) -> float:
    33	    """Interpola P&L no spot dado a partir dos pontos da curva."""
    34	    if not points:
    35	        return 0.0
    36	    xs = [p[0] for p in points]
    37	    ys = [p[1] for p in points]
    38	    if spot <= xs[0]:
    39	        return ys[0]
    40	    if spot >= xs[-1]:
    41	        return ys[-1]
    42	    for i in range(len(xs) - 1):
    43	        if xs[i] <= spot <= xs[i + 1]:
    44	            t = (spot - xs[i]) / (xs[i + 1] - xs[i])
    45	            return ys[i] + t * (ys[i + 1] - ys[i])
    46	    return 0.0
    47	
    48	
    49	def _ratio(numerator: float, denominator: float) -> float:
    50	    if denominator == 0.0:
    51	        return 0.0
    52	    return numerator / denominator
    53	
    54	
    55	# Mapeamento decision  level
    56	_DECISION_LEVEL = {
    57	    "HOLD":         0,
    58	    "WATCH":        1,   # nível interno, mapeado para decision="HOLD" level=1
    59	    "PREPARE_ROLL": 2,
    60	    "CLOSE_REOPEN": 3,
    61	}
    62	
    63	
    64	# ---------------------------------------------------------------------------
    65	# API pública
    66	# ---------------------------------------------------------------------------
    67	
    68	def compute_decision_from_inputs(
    69	    pl_atual: float,
    70	    pl_max: float,
    71	    dte_min: Optional[int] = None,
    72	    dte_gate: int = DTE_GATE_DEFAULT,
    73	    spread_pct_medio: Optional[float] = None,
    74	    thresholds: Optional[Dict[str, float]] = None,
    75	) -> Dict[str, Any]:
    76	    _t_close   = (thresholds or {}).get("close",   THRESHOLD_CLOSE)
    77	    _t_prepare = (thresholds or {}).get("prepare", THRESHOLD_PREPARE)
    78	    _t_watch   = (thresholds or {}).get("watch",   THRESHOLD_WATCH)
    79	
    80	    ratio = _ratio(pl_atual, pl_max)
    81	    alts: List[str] = []
    82	
    83	    if spread_pct_medio is not None and spread_pct_medio > 0.015:
    84	        alts.append("Spread alto -- aguardar execução")
    85	
    86	    # [OK] Gate só dispara se dte_min foi fornecido E é > 0
    87	    #    dte_min=0 significa "expirado/sem DTE real" -- não aciona gate
    88	    if dte_min is not None and dte_min > 0 and dte_min <= dte_gate:
    89	        _internal = "CLOSE_REOPEN"
    90	        level = 3
    91	        reason = "DTE gate"
    92	        extra: Dict[str, Any] = {"dte_min": dte_min, "dte_gate": dte_gate}
    93	    elif ratio >= _t_close:
    94	        _internal = "CLOSE_REOPEN"
    95	        level = 3
    96	        reason = "threshold_close"
    97	        extra = {}
    98	    elif ratio >= _t_prepare:
    99	        _internal = "PREPARE_ROLL"
   100	        level = 2
   101	        reason = "threshold_prepare"
   102	        extra = {}
   103	    elif ratio >= _t_watch:
   104	        _internal = "WATCH"
   105	        level = 1
   106	        reason = "threshold_watch"
   107	        extra = {}
   108	    else:
   109	        _internal = "HOLD"
   110	        level = 0
   111	        reason = "below_watch"
   112	        extra = {}
   113	
   114	    decision = "HOLD" if _internal == "WATCH" else _internal
   115	
   116	    why_dict: Dict[str, Any] = {
   117	        "reasons":        [reason],
   118	        "ratio":          round(ratio, 4),
   119	        "alternatives":   alts,
   120	        "thresholds_used": {
   121	            "watch":   _t_watch,
   122	            "prepare": _t_prepare,
   123	            "close":   _t_close,
   124	        },
   125	        **extra,
   126	    }
   127	
   128	    return {
   129	        "decision":      decision,
   130	        "level":         level,
   131	        "ratio":         round(ratio, 4),
   132	        "pl_pct_of_max": round(ratio, 4),
   133	        "why_json":      json.dumps(why_dict),
   134	        "why":           why_dict,
   135	        "alternatives":  alts,
   136	    }
   137	
   138	
   139	def compute_decision_from_payoff(
   140	    payoff: Dict[str, Any],
   141	    dte_min: Optional[int] = None,
   142	    dte_gate: int = DTE_GATE_DEFAULT,
   143	    spread_pct_medio: Optional[float] = None,
   144	    thresholds: Optional[Dict[str, float]] = None,
   145	) -> Dict[str, Any]:
   146	    """
   147	    Decide a partir de um dict de payoff.
   148	    Payoff vazio ou inválido  HOLD com 'error' em why_json.
   149	    """
   150	    if not payoff:
   151	        why_dict = {"error": "payoff vazio ou invalido", "reason": "invalid_input"}
   152	        return {
   153	            "decision":      "HOLD",
   154	            "level":         0,
   155	            "ratio":         0.0,
   156	            "pl_pct_of_max": 0.0,
   157	            "why_json":      json.dumps(why_dict),
   158	            "why":           why_dict,
   159	            "alternatives":  [],
   160	        }
   161	
   162	    pl_atual = payoff.get("pl_atual") or payoff.get("pl_now") or 0.0
   163	    pl_max   = payoff.get("pl_max") or 0.0
   164	
   165	    # Interpolação via points + spot, se disponíveis
   166	    points = payoff.get("points") or []
   167	    spot   = payoff.get("spot")
   168	    if points and spot is not None and pl_atual == 0.0:
   169	        pl_atual = _interp_payoff(points, float(spot))
   170	
   171	    if not math.isfinite(float(pl_max)):
   172	        why_dict = {"error": "pl_max invalido", "reason": "invalid_pl_max"}
   173	        return {
   174	            "decision":      "HOLD",
   175	            "level":         0,
   176	            "ratio":         0.0,
   177	            "pl_pct_of_max": 0.0,
   178	            "why_json":      json.dumps(why_dict),
   179	            "why":           why_dict,
   180	            "alternatives":  [],
   181	        }
   182	
   183	    return compute_decision_from_inputs(
   184	        pl_atual=float(pl_atual),
   185	        pl_max=float(pl_max),
   186	        dte_min=dte_min,
   187	        dte_gate=dte_gate,
   188	        spread_pct_medio=spread_pct_medio,
   189	        thresholds=thresholds,
   190	    )
   191	
   192	
   193	def compute_decision_from_contract(
   194	    contract: CanonicalStructureMarketInput,
   195	    payoff: Optional[Dict[str, Any]] = None,
   196	) -> Dict[str, Any]:
   197	    """Entrada canônica via CanonicalStructureMarketInput."""
   198	    pl_max  = float(getattr(contract, "pl_max",  None) or 0.0)
   199	    dte_min = getattr(contract, "dte_min", None)
   200	
   201	    if payoff:
   202	        return compute_decision_from_payoff(payoff=payoff, dte_min=dte_min)
   203	
   204	    pl_atual = float(
   205	        getattr(contract, "pl_atual", None)
   206	        or getattr(contract, "pl_now", None)
   207	        or 0.0
   208	    )
   209	    return compute_decision_from_inputs(
   210	        pl_atual=pl_atual,
   211	        pl_max=pl_max,
   212	        dte_min=dte_min,
   213	    )
```

## FILE: domain/payoff_features.py
```python
     1	from src.domain.refs.structure_ref import StructureRef
     2	import json
     3	import sqlite3
     4	from pathlib import Path
     5	from typing import Any, Dict, List, Optional, Tuple
     6	
     7	"""
     8	Patch 24: chave de upsert migrada de (timestamp, aba)
     9	          para (structure_id, reference_date).
    10	          aba e timestamp mantidos como colunas opcionais de rastreabilidade.
    11	"""
    12	
    13	
    14	def get_derived_db_connection() -> sqlite3.Connection:
    15	    db_path = Path("dados/derived.db").resolve()
    16	    return sqlite3.connect(str(db_path))
    17	
    18	
    19	def _as_sorted_points(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    20	    pts = [(float(x), float(y)) for x, y in points]
    21	    pts.sort(key=lambda t: t[0])
    22	    return pts
    23	
    24	
    25	def _interp_y_at_x(points: List[Tuple[float, float]], x: float) -> Optional[float]:
    26	    pts = _as_sorted_points(points)
    27	    if len(pts) < 2:
    28	        return None
    29	    if x < pts[0][0] or x > pts[-1][0]:
    30	        return None
    31	    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
    32	        if x0 <= x <= x1:
    33	            if x1 == x0:
    34	                return y0
    35	            t = (x - x0) / (x1 - x0)
    36	            return y0 + t * (y1 - y0)
    37	    return None
    38	
    39	
    40	def _find_breakevens(points: List[Tuple[float, float]], eps: float = 1e-12) -> List[float]:
    41	    pts = _as_sorted_points(points)
    42	    if len(pts) < 2:
    43	        return []
    44	    bes: List[float] = []
    45	    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
    46	        if abs(y0) <= eps:
    47	            bes.append(x0)
    48	        if (y0 < -eps and y1 > eps) or (y0 > eps and y1 < -eps):
    49	            denom = y1 - y0
    50	            if abs(denom) > eps:
    51	                t = (-y0) / denom
    52	                bes.append(x0 + t * (x1 - x0))
    53	    if abs(pts[-1][1]) <= eps:
    54	        bes.append(pts[-1][0])
    55	    bes.sort()
    56	    out: List[float] = []
    57	    for x in bes:
    58	        if not out or abs(x - out[-1]) > 1e-6:
    59	            out.append(float(x))
    60	    return out
    61	
    62	
    63	def _positive_ranges(
    64	    points: List[Tuple[float, float]],
    65	    eps: float = 0.0,
    66	) -> List[Tuple[float, float]]:
    67	    pts = _as_sorted_points(points)
    68	    if len(pts) < 2:
    69	        return []
    70	    bes = _find_breakevens(pts)
    71	    xs = sorted(set(float(x) for x in [pts[0][0]] + bes + [pts[-1][0]]))
    72	    ranges: List[Tuple[float, float]] = []
    73	    curr_start: Optional[float] = None
    74	
    75	    def mid(a: float, b: float) -> float:
    76	        return (a + b) / 2.0
    77	
    78	    for a, b in zip(xs, xs[1:]):
    79	        if b <= a:
    80	            continue
    81	        ym = _interp_y_at_x(pts, mid(a, b))
    82	        if ym is None:
    83	            continue
    84	        if ym >= -eps:
    85	            if curr_start is None:
    86	                curr_start = a
    87	        else:
    88	            if curr_start is not None:
    89	                ranges.append((curr_start, a))
    90	                curr_start = None
    91	    if curr_start is not None:
    92	        ranges.append((curr_start, xs[-1]))
    93	    return [(float(a), float(b)) for a, b in ranges if b - a > 1e-9]
    94	
    95	
    96	def compute_curve_features(
    97	    points: List[Tuple[float, float]],
    98	    spot_ref: Optional[float] = None,
    99	    structure_id: Optional[str] = None,
   100	    reference_date: Optional[str] = None,
   101	    timestamp: Optional[str] = None,
   102	    aba: Optional[str] = None,
   103	    meta: Optional[Dict[str, Any]] = None,
   104	) -> Dict[str, Any]:
   105	    """
   106	    Computa features da curva de payoff.
   107	
   108	    Chave canônica : structure_id + reference_date   upsert no derived.db.
   109	    timestamp + aba                rastreabilidade opcional (legado RTD).
   110	    """
   111	    pts = _as_sorted_points(points)
   112	    if not pts:
   113	        raise ValueError("points vazio")
   114	
   115	    ys = [y for _, y in pts]
   116	    pl_min = float(min(ys))
   117	    pl_max = float(max(ys))
   118	
   119	    pl_at_spot_ref = None
   120	    if spot_ref is not None:
   121	        pl_at_spot_ref = _interp_y_at_x(pts, float(spot_ref))
   122	
   123	    bes = _find_breakevens(pts)
   124	    pos_ranges = _positive_ranges(pts)
   125	
   126	    return {
   127	        "structure_id":      structure_id,
   128	        "reference_date":    reference_date,
   129	        "timestamp":         timestamp,
   130	        "aba":               aba,
   131	        "spot_ref":          float(spot_ref) if spot_ref is not None else None,
   132	        "points_count":      int(len(pts)),
   133	        "pl_min":            pl_min,
   134	        "pl_max":            pl_max,
   135	        "pl_at_spot_ref":    float(pl_at_spot_ref) if pl_at_spot_ref is not None else None,
   136	        "breakevens":        bes,
   137	        "be_count":          int(len(bes)),
   138	        "pos_ranges":        [[a, b] for a, b in pos_ranges],
   139	        "pos_ranges_count":  int(len(pos_ranges)),
   140	        "max_drawdown_like": float(pl_max - pl_min),
   141	        "meta":              meta or {},
   142	    }
   143	
   144	
   145	_SQL_UPSERT = """
   146	    INSERT INTO payoff_curve_summary (
   147	        structure_id, reference_date,
   148	        timestamp, aba,
   149	        spot_ref, points_count,
   150	        pl_min, pl_max, pl_at_spot_ref,
   151	        breakevens_json, be_count,
   152	        pos_ranges_json, pos_ranges_count,
   153	        max_drawdown_like, meta_json
   154	    ) VALUES (
   155	        :structure_id, :reference_date,
   156	        :timestamp, :aba,
   157	        :spot_ref, :points_count,
   158	        :pl_min, :pl_max, :pl_at_spot_ref,
   159	        :breakevens_json, :be_count,
   160	        :pos_ranges_json, :pos_ranges_count,
   161	        :max_drawdown_like, :meta_json
   162	    )
   163	    ON CONFLICT(structure_id, reference_date) DO UPDATE SET
   164	        timestamp          = excluded.timestamp,
   165	        aba                = excluded.aba,
   166	        spot_ref           = excluded.spot_ref,
   167	        points_count       = excluded.points_count,
   168	        pl_min             = excluded.pl_min,
   169	        pl_max             = excluded.pl_max,
   170	        pl_at_spot_ref     = excluded.pl_at_spot_ref,
   171	        breakevens_json    = excluded.breakevens_json,
   172	        be_count           = excluded.be_count,
   173	        pos_ranges_json    = excluded.pos_ranges_json,
   174	        pos_ranges_count   = excluded.pos_ranges_count,
   175	        max_drawdown_like  = excluded.max_drawdown_like,
   176	        meta_json          = excluded.meta_json
   177	"""
   178	
   179	
   180	def upsert_curve_summary(
   181	    features: Dict[str, Any],
   182	    _conn_override: Optional[sqlite3.Connection] = None,
   183	) -> None:
   184	    """
   185	    Upsert por (structure_id, reference_date) -- chave canônica.
   186	
   187	    Patch 24: substituída chave legada (timestamp, aba)
   188	              pela chave canônica (structure_id, reference_date).
   189	              As colunas aba e timestamp permanecem na tabela como
   190	              rastreabilidade opcional, sem participar da constraint UNIQUE.
   191	
   192	    Patch 20: conexão própria (quando não há _conn_override) gerenciada
   193	              internamente com try/finally, garantindo conn.close() mesmo
   194	              em caso de exceção (ResourceWarning fix).
   195	
   196	    Args:
   197	        features       : dict retornado por compute_curve_features().
   198	        _conn_override : conexão SQLite para injeção em testes. Quando
   199	                         fornecida, o ciclo de vida da conexão é
   200	                         responsabilidade do caller -- esta função NÃO
   201	                         fecha a conexão injetada.
   202	    """
   203	    structure_id   = features.get("structure_id")
   204	    reference_date = features.get("reference_date")
   205	
   206	    if not structure_id or not reference_date:
   207	        raise ValueError(
   208	            "features precisa de structure_id e reference_date para upsert canônico"
   209	        )
   210	
   211	    _owns_conn = _conn_override is None
   212	    conn = _conn_override if _conn_override is not None else get_derived_db_connection()
   213	
   214	    try:
   215	        cur = conn.cursor()
   216	        cur.execute(
   217	            _SQL_UPSERT,
   218	            {
   219	                "structure_id":      structure_id,
   220	                "reference_date":    reference_date,
   221	                "timestamp":         features.get("timestamp"),
   222	                "aba":               features.get("aba"),
   223	                "spot_ref":          features.get("spot_ref"),
   224	                "points_count":      features.get("points_count"),
   225	                "pl_min":            features.get("pl_min"),
   226	                "pl_max":            features.get("pl_max"),
   227	                "pl_at_spot_ref":    features.get("pl_at_spot_ref"),
   228	                "breakevens_json":   json.dumps(features.get("breakevens", [])),
   229	                "be_count":          features.get("be_count"),
   230	                "pos_ranges_json":   json.dumps(features.get("pos_ranges", [])),
   231	                "pos_ranges_count":  features.get("pos_ranges_count"),
   232	                "max_drawdown_like": features.get("max_drawdown_like"),
   233	                "meta_json":         json.dumps(features.get("meta", {})),
   234	            },
   235	        )
   236	        conn.commit()
   237	    finally:
   238	        # Fecha apenas conexões criadas por esta função.
   239	        # Conexões injetadas via _conn_override são responsabilidade do caller.
   240	        if _owns_conn:
   241	            conn.close()
```

## FILE: domain/structure_metrics.py
```python
     1	from datetime import date, datetime
     2	from typing import Any, Iterable
     3	
     4	from domain.position_side import to_pricing_engine_side
     5	
     6	
     7	def _parse_date(value: str | None) -> date | None:
     8	    if not value:
     9	        return None
    10	
    11	    value = str(value).strip()
    12	    if not value:
    13	        return None
    14	
    15	    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
    16	        try:
    17	            return datetime.strptime(value, fmt).date()
    18	        except ValueError:
    19	            continue
    20	
    21	    return None
    22	
    23	
    24	def _to_float(value: Any) -> float | None:
    25	    if value is None:
    26	        return None
    27	
    28	    if isinstance(value, bool):
    29	        return None
    30	
    31	    if isinstance(value, int | float):
    32	        return float(value)
    33	
    34	    text = str(value).strip()
    35	    if not text:
    36	        return None
    37	
    38	    text = text.replace(".", "").replace(",", ".") if "," in text else text
    39	
    40	    try:
    41	        return float(text)
    42	    except ValueError:
    43	        return None
    44	
    45	
    46	def _first_value(source: dict[str, Any], keys: Iterable[str]) -> Any:
    47	    for key in keys:
    48	        value = source.get(key)
    49	        if value is not None and str(value).strip() != "":
    50	            return value
    51	
    52	    return None
    53	
    54	
    55	def _first_float(source: dict[str, Any], keys: Iterable[str]) -> float | None:
    56	    for key in keys:
    57	        value = _to_float(source.get(key))
    58	        if value is not None:
    59	            return value
    60	
    61	    return None
    62	
    63	
    64	def _average(values: Iterable[float | None]) -> float | None:
    65	    valid_values = [value for value in values if value is not None]
    66	
    67	    if not valid_values:
    68	        return None
    69	
    70	    return sum(valid_values) / len(valid_values)
    71	
    72	
    73	def compute_dte(reference_date: str | None, expiration_date: str | None) -> int | None:
    74	    ref = _parse_date(reference_date)
    75	    exp = _parse_date(expiration_date)
    76	
    77	    if ref is None or exp is None:
    78	        return None
    79	
    80	    return (exp - ref).days
    81	
    82	
    83	def compute_dte_min_from_canonical_input(canonical_input: dict[str, Any]) -> int | None:
    84	    structure = canonical_input.get("structure") or {}
    85	    market = canonical_input.get("market") or {}
    86	
    87	    reference_date = market.get("reference_date")
    88	    legs = structure.get("legs", [])
    89	
    90	    dtes = []
    91	    for leg in legs:
    92	        expiration_date = leg.get("expiration_date")
    93	        dte = compute_dte(reference_date, expiration_date)
    94	        if dte is not None:
    95	            dtes.append(dte)
    96	
    97	    if not dtes:
    98	        return None
    99	
   100	    return min(dtes)
   101	
   102	
   103	def compute_mid(bid: Any, ask: Any) -> float | None:
   104	    bid_value = _to_float(bid)
   105	    ask_value = _to_float(ask)
   106	
   107	    if bid_value is None or ask_value is None:
   108	        return None
   109	
   110	    return (bid_value + ask_value) / 2
   111	
   112	
   113	def compute_spread(bid: Any, ask: Any) -> float | None:
   114	    bid_value = _to_float(bid)
   115	    ask_value = _to_float(ask)
   116	
   117	    if bid_value is None or ask_value is None:
   118	        return None
   119	
   120	    return ask_value - bid_value
   121	
   122	
   123	def compute_spread_pct(bid: Any, ask: Any, mid: Any = None) -> float | None:
   124	    spread = compute_spread(bid, ask)
   125	    mid_value = _to_float(mid)
   126	
   127	    if mid_value is None:
   128	        mid_value = compute_mid(bid, ask)
   129	
   130	    if spread is None or mid_value is None or mid_value == 0:
   131	        return None
   132	
   133	    return spread / mid_value
   134	
   135	
   136	def normalize_position_side(leg: dict[str, Any]) -> str | None:
   137	    side = _first_value(
   138	        leg,
   139	        (
   140	            "position_side",
   141	            "side",
   142	            "cv",
   143	            "compra_venda",
   144	            "buy_sell",
   145	        ),
   146	    )
   147	
   148	    if side is None:
   149	        quantity = _first_float(leg, ("quantity", "quant", "qty", "qtd"))
   150	        if quantity is None:
   151	            return None
   152	        return "SHORT" if quantity < 0 else "LONG"
   153	
   154	    try:
   155	        return to_pricing_engine_side(side)
   156	    except ValueError:
   157	        return None
   158	
   159	
   160	def position_multiplier(leg: dict[str, Any]) -> int:
   161	    side = normalize_position_side(leg)
   162	
   163	    if side == "SHORT":
   164	        return -1
   165	
   166	    return 1
   167	
   168	
   169	def leg_quantity(leg: dict[str, Any]) -> float | None:
   170	    quantity = _first_float(leg, ("quantity", "quant", "qty", "qtd"))
   171	
   172	    if quantity is None:
   173	        return None
   174	
   175	    return abs(quantity)
   176	
   177	
   178	def compute_realistic_price(leg: dict[str, Any]) -> float | None:
   179	    side = normalize_position_side(leg)
   180	
   181	    bid = _first_float(leg, ("bid",))
   182	    ask = _first_float(leg, ("ask",))
   183	    mid = _first_float(leg, ("mid",))
   184	    last = _first_float(leg, ("last", "ultimo", "último", "preco", "price"))
   185	
   186	    if mid is None:
   187	        mid = compute_mid(bid, ask)
   188	
   189	    if side == "SHORT":
   190	        for value in (ask, mid, bid, last):
   191	            if value is not None:
   192	                return value
   193	
   194	        return None
   195	
   196	    for value in (bid, mid, ask, last):
   197	        if value is not None:
   198	            return value
   199	
   200	    return None
   201	
   202	def compute_pl_realista(leg: dict[str, Any]) -> float | None:
   203	    quantity = leg_quantity(leg)
   204	
   205	    entry_price = _first_float(
   206	        leg,
   207	        (
   208	            "valor_executado",
   209	            "execution_price",
   210	            "entry_price",
   211	            "preco_execucao",
   212	            "preço_execução",
   213	            "preco_entrada",
   214	            "preço_entrada",
   215	        ),
   216	    )
   217	
   218	    realistic_price = compute_realistic_price(leg)
   219	
   220	    if entry_price is None:
   221	        premium = _first_float(leg, ("premium", "premio", "prêmio"))
   222	
   223	        if premium is not None:
   224	            entry_price = premium
   225	
   226	            bid = _first_float(leg, ("bid",))
   227	            ask = _first_float(leg, ("ask",))
   228	            mid = _first_float(leg, ("mid",))
   229	
   230	            if mid is None:
   231	                mid = compute_mid(bid, ask)
   232	
   233	            if mid is not None:
   234	                realistic_price = mid
   235	
   236	    if quantity is None or entry_price is None or realistic_price is None:
   237	        return _first_float(leg, ("pl_realista",))
   238	
   239	    return (realistic_price - entry_price) * quantity * position_multiplier(leg)
   240	
   241	def compute_greek_exposure(leg: dict[str, Any], greek_name: str) -> float | None:
   242	    greek_value = _first_float(leg, (greek_name,))
   243	    quantity = leg_quantity(leg)
   244	
   245	    if greek_value is None or quantity is None:
   246	        return None
   247	
   248	    return greek_value * quantity * position_multiplier(leg)
   249	
   250	
   251	def compute_leg_metrics(
   252	    leg: dict[str, Any],
   253	    reference_date: str | None = None,
   254	) -> dict[str, Any]:
   255	    bid = _first_float(leg, ("bid",))
   256	    ask = _first_float(leg, ("ask",))
   257	
   258	    mid = compute_mid(bid, ask)
   259	    if mid is None:
   260	        mid = _first_float(leg, ("mid",))
   261	
   262	    spread = compute_spread(bid, ask)
   263	    if spread is None:
   264	        spread = _first_float(leg, ("spread",))
   265	
   266	    spread_pct = compute_spread_pct(bid, ask, mid)
   267	    if spread_pct is None:
   268	        spread_pct = _first_float(leg, ("spread_pct",))
   269	
   270	    dte = _first_float(leg, ("dte",))
   271	    if dte is not None:
   272	        dte = int(dte)
   273	    else:
   274	        expiration_date = _first_value(
   275	            leg,
   276	            (
   277	                "expiration_date",
   278	                "vencimento",
   279	                "maturity_date",
   280	                "expiry",
   281	            ),
   282	        )
   283	        dte = compute_dte(reference_date, expiration_date)
   284	
   285	    return {
   286	        "side": normalize_position_side(leg),
   287	        "quantity": leg_quantity(leg),
   288	        "mid": mid,
   289	        "spread": spread,
   290	        "spread_pct": spread_pct,
   291	        "preco_realista": compute_realistic_price(leg),
   292	        "pl_realista": compute_pl_realista(leg),
   293	        "delta_exposto": compute_greek_exposure(leg, "delta"),
   294	        "gamma_exposto": compute_greek_exposure(leg, "gamma"),
   295	        "theta_exposto": compute_greek_exposure(leg, "theta"),
   296	        "vega_exposto": compute_greek_exposure(leg, "vega"),
   297	        "dte": dte,
   298	    }
   299	
   300	
   301	def compute_structure_metrics(
   302	    legs: list[dict[str, Any]],
   303	    reference_date: str | None = None,
   304	) -> dict[str, Any]:
   305	    computed_legs = []
   306	
   307	    for leg in legs:
   308	        leg_metrics = compute_leg_metrics(leg, reference_date=reference_date)
   309	        computed_legs.append(
   310	            {
   311	                **leg,
   312	                **leg_metrics,
   313	            }
   314	        )
   315	
   316	    pl_values = [leg.get("pl_realista") for leg in computed_legs]
   317	    delta_values = [leg.get("delta_exposto") for leg in computed_legs]
   318	    gamma_values = [leg.get("gamma_exposto") for leg in computed_legs]
   319	    theta_values = [leg.get("theta_exposto") for leg in computed_legs]
   320	    vega_values = [leg.get("vega_exposto") for leg in computed_legs]
   321	    dte_values = [leg.get("dte") for leg in computed_legs if leg.get("dte") is not None]
   322	
   323	    valid_pl_values = [value for value in pl_values if value is not None]
   324	    valid_delta_values = [value for value in delta_values if value is not None]
   325	    valid_gamma_values = [value for value in gamma_values if value is not None]
   326	    valid_theta_values = [value for value in theta_values if value is not None]
   327	    valid_vega_values = [value for value in vega_values if value is not None]
   328	
   329	    return {
   330	        "num_pernas": len(computed_legs),
   331	        "legs": computed_legs,
   332	        "pl_realista_total": sum(valid_pl_values) if valid_pl_values else None,
   333	        "delta_liq": sum(valid_delta_values) if valid_delta_values else None,
   334	        "gamma_liq": sum(valid_gamma_values) if valid_gamma_values else None,
   335	        "theta_liq": sum(valid_theta_values) if valid_theta_values else None,
   336	        "vega_liq": sum(valid_vega_values) if valid_vega_values else None,
   337	        "spread_medio": _average(leg.get("spread") for leg in computed_legs),
   338	        "spread_pct_medio": _average(leg.get("spread_pct") for leg in computed_legs),
   339	        "dte_min": min(dte_values) if dte_values else None,
   340	    }
   341	
   342	
   343	def compute_structure_metrics_from_canonical_input(
   344	    canonical_input: dict[str, Any],
   345	) -> dict[str, Any]:
   346	    structure = canonical_input.get("structure") or {}
   347	    market = canonical_input.get("market") or {}
   348	
   349	    reference_date = market.get("reference_date")
   350	    legs = structure.get("legs", [])
   351	
   352	    return compute_structure_metrics(legs, reference_date=reference_date)
```

## FILE: repositories/system_snapshots_repository.py
```python
     1	from __future__ import annotations
     2	
     3	import json
     4	import sqlite3
     5	from datetime import datetime, timezone
     6	from pathlib import Path
     7	from typing import Any
     8	
     9	from infra.bootstrap_structures_schema import DB_PATH, ensure_structures_schema
    10	
    11	
    12	_JSON_COLUMNS_SNAPSHOT = {
    13	    "structure_json",
    14	    "market_json",
    15	    "metrics_json",
    16	    "payoff_json",
    17	    "decision_json",
    18	    "alerts_json",
    19	    "operation_state_json",
    20	}
    21	
    22	_JSON_COLUMNS_LEG = {
    23	    "metrics_json",
    24	    "market_json",
    25	    "raw_json",
    26	}
    27	
    28	
    29	def _utc_now_iso() -> str:
    30	    return datetime.now(timezone.utc).isoformat()
    31	
    32	
    33	def _to_json(value: Any) -> str | None:
    34	    if value is None:
    35	        return None
    36	
    37	    if isinstance(value, str):
    38	        return value
    39	
    40	    return json.dumps(value, ensure_ascii=False, sort_keys=True)
    41	
    42	
    43	def _from_json(value: Any) -> Any:
    44	    if value is None:
    45	        return None
    46	
    47	    if not isinstance(value, str):
    48	        return value
    49	
    50	    value = value.strip()
    51	
    52	    if value == "":
    53	        return None
    54	
    55	    try:
    56	        return json.loads(value)
    57	    except json.JSONDecodeError:
    58	        return value
    59	
    60	
    61	def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    62	    return {key: row[key] for key in row.keys()}
    63	
    64	
    65	class SystemSnapshotsRepository:
    66	    """Persistência do histórico operacional oficial gerado pelo sistema."""
    67	
    68	    def __init__(self, db_path: str | Path = DB_PATH) -> None:
    69	        self.db_path = Path(db_path)
    70	        ensure_structures_schema(self.db_path)
    71	
    72	    def _connect(self) -> sqlite3.Connection:
    73	        conn = sqlite3.connect(self.db_path)
    74	        conn.row_factory = sqlite3.Row
    75	        conn.execute("PRAGMA foreign_keys = ON")
    76	        return conn
    77	
    78	    def create_snapshot(
    79	        self,
    80	        *,
    81	        structure_id: int,
    82	        structure_json: dict[str, Any],
    83	        legs: list[dict[str, Any]] | None = None,
    84	        pricing_execution_id: int | None = None,
    85	        underlying_asset: str | None = None,
    86	        reference_date: str | None = None,
    87	        snapshot_source: str = "system",
    88	        market_json: dict[str, Any] | list[Any] | None = None,
    89	        metrics_json: dict[str, Any] | list[Any] | None = None,
    90	        payoff_json: dict[str, Any] | list[Any] | None = None,
    91	        decision_json: dict[str, Any] | list[Any] | None = None,
    92	        alerts_json: dict[str, Any] | list[Any] | None = None,
    93	        operation_state_json: dict[str, Any] | list[Any] | None = None,
    94	        created_at: str | None = None,
    95	    ) -> int:
    96	        """Cria um snapshot e suas pernas associadas.
    97	
    98	        Retorna o id gerado em structure_snapshots.
    99	        """
   100	
   101	        if not structure_id:
   102	            raise ValueError("structure_id é obrigatório")
   103	
   104	        if not structure_json:
   105	            raise ValueError("structure_json é obrigatório")
   106	
   107	        created_at = created_at or _utc_now_iso()
   108	        legs = legs or []
   109	
   110	        with self._connect() as conn:
   111	            cur = conn.execute(
   112	                """
   113	                INSERT INTO structure_snapshots (
   114	                    created_at,
   115	                    structure_id,
   116	                    pricing_execution_id,
   117	                    underlying_asset,
   118	                    reference_date,
   119	                    snapshot_source,
   120	                    structure_json,
   121	                    market_json,
   122	                    metrics_json,
   123	                    payoff_json,
   124	                    decision_json,
   125	                    alerts_json,
   126	                    operation_state_json
   127	                )
   128	                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
   129	                """,
   130	                (
   131	                    created_at,
   132	                    structure_id,
   133	                    pricing_execution_id,
   134	                    underlying_asset,
   135	                    reference_date,
   136	                    snapshot_source,
   137	                    _to_json(structure_json),
   138	                    _to_json(market_json),
   139	                    _to_json(metrics_json),
   140	                    _to_json(payoff_json),
   141	                    _to_json(decision_json),
   142	                    _to_json(alerts_json),
   143	                    _to_json(operation_state_json),
   144	                ),
   145	            )
   146	
   147	            snapshot_id = int(cur.lastrowid)
   148	
   149	            for index, leg in enumerate(legs, start=1):
   150	                self._insert_leg_snapshot(
   151	                    conn=conn,
   152	                    snapshot_id=snapshot_id,
   153	                    structure_id=structure_id,
   154	                    leg=leg,
   155	                    default_leg_order=index,
   156	                )
   157	
   158	            return snapshot_id
   159	
   160	    def _insert_leg_snapshot(
   161	        self,
   162	        *,
   163	        conn: sqlite3.Connection,
   164	        snapshot_id: int,
   165	        structure_id: int,
   166	        leg: dict[str, Any],
   167	        default_leg_order: int,
   168	    ) -> None:
   169	        conn.execute(
   170	            """
   171	            INSERT INTO structure_leg_snapshots (
   172	                snapshot_id,
   173	                structure_id,
   174	                leg_id,
   175	                leg_order,
   176	                position_side,
   177	                option_type,
   178	                symbol,
   179	                strike,
   180	                expiration_date,
   181	                quantity,
   182	                premium,
   183	                multiplier,
   184	                metrics_json,
   185	                market_json,
   186	                raw_json
   187	            )
   188	            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
   189	            """,
   190	            (
   191	                snapshot_id,
   192	                structure_id,
   193	                leg.get("leg_id") or leg.get("id"),
   194	                leg.get("leg_order", default_leg_order),
   195	                leg.get("position_side"),
   196	                leg.get("option_type"),
   197	                leg.get("symbol"),
   198	                leg.get("strike"),
   199	                leg.get("expiration_date"),
   200	                leg.get("quantity"),
   201	                leg.get("premium"),
   202	                leg.get("multiplier"),
   203	                _to_json(leg.get("metrics_json")),
   204	                _to_json(leg.get("market_json")),
   205	                _to_json(leg.get("raw_json", leg)),
   206	            ),
   207	        )
   208	
   209	    def get_snapshot(self, snapshot_id: int) -> dict[str, Any] | None:
   210	        """Retorna um snapshot com suas pernas, ou None se não existir."""
   211	
   212	        with self._connect() as conn:
   213	            snapshot_row = conn.execute(
   214	                """
   215	                SELECT *
   216	                FROM structure_snapshots
   217	                WHERE id = ?
   218	                """,
   219	                (snapshot_id,),
   220	            ).fetchone()
   221	
   222	            if snapshot_row is None:
   223	                return None
   224	
   225	            snapshot = self._decode_snapshot_row(snapshot_row)
   226	
   227	            leg_rows = conn.execute(
   228	                """
   229	                SELECT *
   230	                FROM structure_leg_snapshots
   231	                WHERE snapshot_id = ?
   232	                ORDER BY leg_order, id
   233	                """,
   234	                (snapshot_id,),
   235	            ).fetchall()
   236	
   237	            snapshot["legs"] = [self._decode_leg_row(row) for row in leg_rows]
   238	
   239	            return snapshot
   240	
   241	    def list_snapshots_for_structure(
   242	        self,
   243	        structure_id: int,
   244	        *,
   245	        limit: int = 50,
   246	    ) -> list[dict[str, Any]]:
   247	        """Lista snapshots de uma estrutura, do mais recente para o mais antigo."""
   248	
   249	        if limit <= 0:
   250	            raise ValueError("limit deve ser maior que zero")
   251	
   252	        with self._connect() as conn:
   253	            rows = conn.execute(
   254	                """
   255	                SELECT *
   256	                FROM structure_snapshots
   257	                WHERE structure_id = ?
   258	                ORDER BY created_at DESC, id DESC
   259	                LIMIT ?
   260	                """,
   261	                (structure_id, limit),
   262	            ).fetchall()
   263	
   264	        return [self._decode_snapshot_row(row) for row in rows]
   265	
   266	    def get_latest_snapshot_for_structure(
   267	        self,
   268	        structure_id: int,
   269	    ) -> dict[str, Any] | None:
   270	        """Retorna o snapshot mais recente de uma estrutura."""
   271	
   272	        snapshots = self.list_snapshots_for_structure(structure_id, limit=1)
   273	
   274	        if not snapshots:
   275	            return None
   276	
   277	        return self.get_snapshot(int(snapshots[0]["id"]))
   278	
   279	    def _decode_snapshot_row(self, row: sqlite3.Row) -> dict[str, Any]:
   280	        data = _row_to_dict(row)
   281	
   282	        for column in _JSON_COLUMNS_SNAPSHOT:
   283	            data[column] = _from_json(data.get(column))
   284	
   285	        return data
   286	
   287	    def _decode_leg_row(self, row: sqlite3.Row) -> dict[str, Any]:
   288	        data = _row_to_dict(row)
   289	
   290	        for column in _JSON_COLUMNS_LEG:
   291	            data[column] = _from_json(data.get(column))
   292	
   293	        return data
```

## FILE: repositories/ui_data_table_candidates.py
```python
     1	"""
     2	Candidatos de tabelas para leitura de dados da UI.
     3	
     4	Este módulo concentra aliases físicos/canônicos usados para detectar
     5	schemas existentes no banco derivado.
     6	
     7	A UI deve consumir estas listas sem conhecer diretamente nomes físicos
     8	legados de staging, como tabelas rtd_*.
     9	"""
    10	
    11	CANDIDATE_CONSOLIDATION_TABLES = [
    12	    "structure_decisions",
    13	    "rtd_consolidacoes",
    14	    "rtd_consolidations",
    15	    "decisions",
    16	    "rtd_decisions",
    17	]
    18	
    19	CANDIDATE_PAYOFF_TABLES = [
    20	    "payoff_curve_points",
    21	    "rtd_payoff_points",
    22	    "rtd_payoff_curva",
    23	    "payoff_points",
    24	]
```

## FILE: UI/models/ui_data.py
```python
     1	# UI/models/ui_data.py
     2	# alteracao_36_E: eliminar self._conn compartilhada
     3	# Toda conexao de leitura passa a ser por chamada (igual a _connect_derived_threadsafe)
     4	from src.domain.refs.structure_ref import StructureRef
     5	import sqlite3
     6	from sqlite3 import Row
     7	from pathlib import Path
     8	from typing import Dict, List, Optional, Tuple, Any
     9	from db.config import DERIVED_DB_PATH
    10	import json
    11	import csv
    12	from datetime import datetime
    13	
    14	from repositories.ui_data_table_candidates import (
    15	    CANDIDATE_CONSOLIDATION_TABLES,
    16	    CANDIDATE_PAYOFF_TABLES,
    17	)
    18	
    19	# Mapeamento de colunas preferidas -> alternativas
    20	COLUMN_ALIASES = {
    21	    "timestamp":     ["timestamp", "ts", "decided_at", "dt_ref"],
    22	    "structure_id":  ["structure_id"],                              #  alteracao_33: chave canônica
    23	    "aba":           ["aba", "sheet", "tab"],                       # mantido para compat
    24	    "decision":      ["decision", "decisao", "action"],
    25	    "level":         ["level", "nivel", "severity_level"],
    26	    "pl_pct_of_max": ["pl_pct_of_max", "pl_ratio", "pl_pct"],
    27	    "ratio":         ["ratio", "pl_ratio", "pl_pct_of_max", "pl_pct"],
    28	    "dte_min":       ["dte_min", "dte", "days_to_expiry"],
    29	    "why":           ["why", "rationale", "rationale_json"],
    30	    "why_json":      ["why_json", "meta_json"],
    31	    "pl_atual":      ["pl_atual", "pl_current"],
    32	    "pl_max":        ["pl_max", "pl_best", "pl_top"],
    33	    "spot_ref":      ["spot_ref", "spot_reference", "ref_spot"],
    34	}
    35	
    36	PAYOFF_COLUMN_ALIASES = {
    37	    "timestamp": ["timestamp", "ts", "dt_ref"],
    38	    "structure_id": ["structure_id"],   #  alteracao_33
    39	    "spot":      ["point_spot", "spot", "underlying", "x", "s_t"],
    40	    "pl":        ["point_pl", "pl", "pl_value", "y", "payoff", "pl_venc"],
    41	}
    42	
    43	def _first_match(cols: List[str], candidates: List[str]) -> Optional[str]:
    44	    for c in candidates:
    45	        if c in cols:
    46	            return c
    47	    return None
    48	
    49	class UIDataModel:
    50	    def __init__(self, derived_db_path: Optional[Path] = None):
    51	        from db.config import DERIVED_DB_PATH
    52	        self.derived_db_path = (
    53	            Path(derived_db_path).resolve()
    54	            if derived_db_path
    55	            else Path(DERIVED_DB_PATH).resolve()
    56	        )
    57	        print(f"[UI] Usando derived DB: {self.derived_db_path}")
    58	
    59	        # alteracao_36_E: self._conn REMOVIDO -- cada metodo abre sua propria conexao
    60	        self._consolidations_table: Optional[str] = None
    61	        self._payoff_table: Optional[str] = None
    62	        self._consolidations_cols: Dict[str, str] = {}
    63	        self._payoff_cols: Dict[str, str] = {}
    64	        self._cache_structures: List[str] = []
    65	
    66	        self._payoff_cache: Dict[Tuple[str, str], Dict[str, Any]] = {}
    67	        self._payoff_cache_max = 128
    68	
    69	    # alteracao_36_E: _connect agora e sempre uma nova conexao por chamada
    70	    def _connect(self) -> sqlite3.Connection:
    71	        if not self.derived_db_path.exists():
    72	            raise FileNotFoundError(
    73	                f"Banco derived.db nao encontrado em: {self.derived_db_path}"
    74	            )
    75	        conn = sqlite3.connect(str(self.derived_db_path))
    76	        conn.row_factory = sqlite3.Row
    77	        return conn
    78	
    79	    def _list_tables(self) -> List[str]:
    80	        # alteracao_36_E: abre e fecha conexao local
    81	        conn = self._connect()
    82	        try:
    83	            cur = conn.execute(
    84	                "SELECT name FROM sqlite_master WHERE type='table'"
    85	            )
    86	            return [r["name"] for r in cur.fetchall()]
    87	        finally:
    88	            conn.close()
    89	
    90	    def _detect_tables(self):
    91	        tables = self._list_tables()
    92	        for t in CANDIDATE_CONSOLIDATION_TABLES:
    93	            if t in tables:
    94	                self._consolidations_table = t
    95	                break
    96	        if not self._consolidations_table:
    97	            raise RuntimeError(
    98	                "Tabela de consolidações não encontrada. Esperadas: "
    99	                + ", ".join(CANDIDATE_CONSOLIDATION_TABLES)
   100	            )
   101	        for t in CANDIDATE_PAYOFF_TABLES:
   102	            if t in tables:
   103	                self._payoff_table = t
   104	                break
   105	
   106	    def _inspect_columns(self, table: str) -> List[str]:
   107	        # alteracao_36_E: abre e fecha conexao local
   108	        conn = self._connect()
   109	        try:
   110	            cur = conn.execute(f"PRAGMA table_info({table})")
   111	            return [r["name"] for r in cur.fetchall()]
   112	        finally:
   113	            conn.close()
   114	
   115	    def _build_consolidations_colmap(self):
   116	        cols = self._inspect_columns(self._consolidations_table)
   117	        colmap = {}
   118	        for alias, candidates in COLUMN_ALIASES.items():
   119	            m = _first_match(cols, candidates)
   120	            if m:
   121	                colmap[alias] = m
   122	        self._consolidations_cols = colmap
   123	
   124	    def _build_payoff_colmap(self):
   125	        if not self._payoff_table:
   126	            self._payoff_cols = {}
   127	            return
   128	
   129	        cols = self._inspect_columns(self._payoff_table)
   130	        colmap = {}
   131	
   132	        if self._payoff_table == "payoff_curve_points":
   133	            aliases = {
   134	                "spot":         ["point_spot"],
   135	                "pl":           ["point_pl"],
   136	                "timestamp":    ["timestamp"],
   137	                # alteracao_36_F: structure_id e opcional aqui --
   138	                # pode nao existir ainda se a migration ainda nao rodou.
   139	                # _structure_filter_col vai lancar RuntimeError com mensagem clara.
   140	                "structure_id": ["structure_id"],   #  alteracao_34: único identificador canônico
   141	            }
   142	            print(f"[UI] Usando contrato canônico para {self._payoff_table}")
   143	        else:
   144	            aliases = PAYOFF_COLUMN_ALIASES
   145	            print(f"[UI] Usando aliases flexíveis para {self._payoff_table}")
   146	
   147	        for alias, candidates in aliases.items():
   148	            m = _first_match(cols, candidates)
   149	            if m:
   150	                colmap[alias] = m
   151	            # alteracao_36_F: nao lanca erro se structure_id ausente --
   152	            # isso ocorre antes da migration e e tratado em _structure_filter_col
   153	
   154	        self._payoff_cols = colmap
   155	
   156	        if ("spot" not in self._payoff_cols) or ("pl" not in self._payoff_cols):
   157	            raise RuntimeError(
   158	                f"Tabela {self._payoff_table} não apresenta colunas obrigatórias "
   159	                f"para payoff (point_spot/point_pl ou spot/pl)."
   160	            )
   161	
   162	        # alteracao_36_F: aviso explicito quando structure_id ausente (pre-migration)
   163	        if "structure_id" not in self._payoff_cols:
   164	            print(
   165	                f"[UI] AVISO: {self._payoff_table} nao tem coluna structure_id. "
   166	                "Execute a migration (alteracao_36) para habilitar filtro canonico."
   167	            )
   168	
   169	    # ------------------------------------------------------------------
   170	    #  alteracao_33: resolve a coluna de filtro por estrutura
   171	    #   Prioriza structure_id; cai em aba se structure_id não mapeado.
   172	    # ------------------------------------------------------------------
   173	    def _structure_filter_col(self, colmap: Dict[str, str]) -> str:
   174	        """
   175	        alteracao_34: retorna apenas o nome da coluna structure_id.
   176	        Branch aba removido -- schemas sem structure_id nao sao mais suportados.
   177	        """
   178	        if colmap.get("structure_id"):
   179	            return colmap["structure_id"]
   180	        raise RuntimeError(
   181	            "Coluna 'structure_id' nao encontrada no colmap. "
   182	            "Execute a migration do alteracao_33 antes de continuar."
   183	        )
   184	
   185	    def _resolve_structure_key(self, structure_id: str) -> int:
   186	        """
   187	        alteracao_34: structure_id e sempre INTEGER.
   188	        Aceita str ("7") ou int (7). Lanca ValueError se nao conversivel.
   189	        """
   190	        try:
   191	            return int(structure_id)
   192	        except (TypeError, ValueError) as exc:
   193	            raise ValueError(
   194	                f"structure_id invalido: {structure_id!r}. "
   195	                "Esperado inteiro ou string numerica."
   196	            ) from exc
   197	
   198	    # ------------------------------------------------------------------
   199	    # API pública
   200	    # ------------------------------------------------------------------
   201	
   202	    def refresh(self):
   203	        self._detect_tables()
   204	        self._build_consolidations_colmap()
   205	        self._build_payoff_colmap()
   206	        self._cache_structures = self._load_structures()
   207	
   208	    def _load_structures(self) -> List[str]:
   209	        # alteracao_36_E: abre e fecha conexao local
   210	        c = self._consolidations_cols
   211	        if not c.get("structure_id"):
   212	            raise RuntimeError(
   213	                "Coluna 'structure_id' nao encontrada em "
   214	                f"{self._consolidations_table}. "
   215	                "Execute a migration do alteracao_33 antes de continuar."
   216	            )
   217	        sid_col = c["structure_id"]
   218	        conn = self._connect()
   219	        try:
   220	            q = (
   221	                f"SELECT DISTINCT CAST({sid_col} AS TEXT) AS structure_id "
   222	                f"FROM {self._consolidations_table} "
   223	                f"WHERE {sid_col} IS NOT NULL "
   224	                f"ORDER BY structure_id"
   225	            )
   226	            rows = conn.execute(q).fetchall()
   227	            return [r["structure_id"] for r in rows]
   228	        finally:
   229	            conn.close()
   230	
   231	    def get_structures(self) -> List[str]:
   232	        """Alias de get_structure_ids() para compatibilidade."""
   233	        if not self._cache_structures:
   234	            self._cache_structures = self._load_structures()
   235	        return list(self._cache_structures)
   236	
   237	    def get_structure_ids(self) -> List[str]:
   238	        """alteracao_34: metodo canonico. Substitui get_structures()."""
   239	        if not self._cache_structures:
   240	            self._cache_structures = self._load_structures()
   241	        return list(self._cache_structures)
   242	
   243	    def get_abas(self) -> list:
   244	        """Alias readonly de get_structure_ids() -- compat UI (alteracao_34:filtro_aba)."""
   245	        return self.get_structure_ids()
   246	
   247	    def get_decisions(self, filters: Optional[Dict] = None) -> List[Dict]:
   248	        """
   249	        Retorna lista de decisões.
   250	        alteracao_33: filtra por structure_id quando disponível.
   251	        alteracao_36_E: conn local por chamada.
   252	        """
   253	        if not self._consolidations_table:
   254	            self.refresh()
   255	
   256	        c = self._consolidations_cols
   257	
   258	        # Expressão para pl_pct_of_max
   259	        if c.get("pl_pct_of_max"):
   260	            pl_pct_expr = c["pl_pct_of_max"]
   261	        elif c.get("ratio"):
   262	            pl_pct_expr = c["ratio"]
   263	        elif c.get("pl_atual") and c.get("pl_max"):
   264	            pl_pct_expr = (
   265	                f"CASE WHEN {c['pl_max']} IS NULL OR {c['pl_max']} = 0 "
   266	                f"THEN NULL ELSE ({c['pl_atual']} * 1.0 / {c['pl_max']}) END"
   267	            )
   268	        else:
   269	            pl_pct_expr = "NULL"
   270	
   271	        # patch_3a: deriva aba <-> structure_id quando coluna física ausente
   272	        select_parts = []
   273	        for alias in [
   274	            "timestamp", "structure_id", "aba", "decision", "level",
   275	            "dte_min", "why", "why_json", "pl_atual", "pl_max", "spot_ref",
   276	        ]:
   277	            src = c.get(alias)
   278	            if src:
   279	                select_parts.append(f"{src} AS {alias}")
   280	            elif alias == "aba":
   281	                sid_src = c.get("structure_id")
   282	                if sid_src:
   283	                    select_parts.append(f"CAST({sid_src} AS TEXT) AS aba")
   284	                else:
   285	                    select_parts.append("NULL AS aba")
   286	            elif alias == "structure_id":
   287	                aba_src = c.get("aba")
   288	                if aba_src:
   289	                    select_parts.append(
   290	                        f"CASE WHEN CAST({aba_src} AS TEXT) GLOB '[0-9]*' "
   291	                        f"THEN CAST({aba_src} AS INTEGER) ELSE NULL END AS structure_id"
   292	                    )
   293	                else:
   294	                    select_parts.append("NULL AS structure_id")
   295	            else:
   296	                select_parts.append(f"NULL AS {alias}")
   297	
   298	        select_parts.append(f"({pl_pct_expr}) AS pl_pct_of_max")
   299	
   300	        subq = f"(SELECT {', '.join(select_parts)} FROM {self._consolidations_table}) t"
   301	
   302	        where = []
   303	        params = []
   304	        if filters:
   305	            if filters.get("date_from"):
   306	                try:
   307	                    dt_from = datetime.strptime(filters["date_from"], "%Y-%m-%d")
   308	                    where.append("t.timestamp >= ?")
   309	                    params.append(dt_from.strftime("%Y-%m-%d 00:00:00"))
   310	                except Exception:
   311	                    pass
   312	
   313	            if filters.get("date_to"):
   314	                try:
   315	                    dt_to = datetime.strptime(filters["date_to"], "%Y-%m-%d")
   316	                    where.append("t.timestamp <= ?")
   317	                    params.append(dt_to.strftime("%Y-%m-%d 23:59:59"))
   318	                except Exception:
   319	                    pass
   320	
   321	            structure_filter = filters.get("structure_id")
   322	            if structure_filter is not None:
   323	                try:
   324	                    where.append("t.structure_id = ?")
   325	                    params.append(int(structure_filter))
   326	                except (TypeError, ValueError) as exc:
   327	                    raise ValueError(
   328	                        f"structure_id deve ser inteiro; recebido: {structure_filter!r}"
   329	                    ) from exc
   330	
   331	            aba_filter = filters.get("aba")
   332	            if aba_filter is not None:
   333	                where.append("t.aba = ?")
   334	                params.append(str(aba_filter))
   335	
   336	            if filters.get("decision"):
   337	                where.append("t.decision = ?")
   338	                params.append(filters["decision"])
   339	
   340	            if filters.get("level_min"):
   341	                where.append("t.level >= ?")
   342	                params.append(int(filters["level_min"]))
   343	
   344	            if filters.get("dte_max"):
   345	                where.append("t.dte_min <= ?")
   346	                params.append(int(filters["dte_max"]))
   347	
   348	        where_sql = f"WHERE {' AND '.join(where)}" if where else ""
   349	        sql = f"""
   350	            SELECT
   351	                t.timestamp, t.structure_id, t.aba, t.decision, t.level,
   352	                t.pl_pct_of_max, t.dte_min, t.why, t.why_json,
   353	                t.pl_atual, t.pl_max, t.spot_ref
   354	            FROM {subq}
   355	            {where_sql}
   356	            ORDER BY t.timestamp DESC
   357	        """
   358	
   359	        # ✅ CORREÇÃO: conn criada AQUI, antes de ser usada
   360	        conn = self._connect()
   361	        try:
   362	            rows = conn.execute(sql, params).fetchall()
   363	        finally:
   364	            conn.close()  # ✅ sempre fechada, mesmo em erro
   365	
   366	        result = []
   367	        for r in rows:
   368	            item = dict(r)
   369	
   370	            if item.get("structure_id") is None and item.get("aba") is not None:
   371	                try:
   372	                    item["structure_id"] = int(item["aba"])
   373	                except (TypeError, ValueError):
   374	                    pass
   375	
   376	            if item.get("aba") is None and item.get("structure_id") is not None:
   377	                item["aba"] = str(item["structure_id"])
   378	
   379	            # Normalizar why
   380	            why_val = item.get("why")
   381	            why_json_val = item.get("why_json")
   382	            if isinstance(why_val, str):
   383	                try:
   384	                    item["why"] = json.loads(why_val)
   385	                except Exception:
   386	                    pass
   387	            elif why_val is None and why_json_val is not None:
   388	                try:
   389	                    item["why"] = (
   390	                        json.loads(why_json_val)
   391	                        if isinstance(why_json_val, str)
   392	                        else why_json_val
   393	                    )
   394	                except Exception:
   395	                    item["why"] = why_json_val
   396	
   397	            result.append(item)
   398	
   399	        return result
   400	
   401	    def get_payoff_curve(self, structure_id: str, timestamp: str) -> List[Dict]:
   402	        """
   403	         alteracao_33: resolve chave via _structure_filter_col.
   404	        Aceita structure_id como inteiro ou string numerica ("7").
   405	        Strings nao-numericas lancam ValueError.
   406	        """
   407	        ts_key = timestamp if timestamp is not None else "__latest__"
   408	        cache_key = (str(structure_id), ts_key)
   409	
   410	        if hasattr(self, "_payoff_cache") and cache_key in self._payoff_cache:
   411	            cached = self._payoff_cache[cache_key]
   412	            if isinstance(cached, list):
   413	                return cached
   414	            if isinstance(cached, dict) and "points" in cached:
   415	                return cached["points"]
   416	
   417	        if not self._payoff_table:
   418	            raise RuntimeError(
   419	                "Tabela de payoff não encontrada. Esperadas: "
   420	                + ", ".join(CANDIDATE_PAYOFF_TABLES)
   421	            )
   422	
   423	        conn = self._connect()
   424	        p = self._payoff_cols
   425	
   426	        required = ["timestamp", "spot", "pl"]
   427	        if any(k not in p for k in required):
   428	            raise RuntimeError(
   429	                f"Tabela {self._payoff_table} não possui colunas esperadas para payoff."
   430	            )
   431	
   432	        #  alteracao_33: resolve coluna de estrutura
   433	        # alteracao_34: structure_id e sempre INTEGER
   434	        filter_col = self._structure_filter_col(p)
   435	        filter_val = self._resolve_structure_key(structure_id)
   436	
   437	        sql_exact = f"""
   438	            SELECT {p['spot']} AS spot, {p['pl']} AS pl
   439	            FROM {self._payoff_table}
   440	            WHERE {filter_col} = ? AND {p['timestamp']} = ?
   441	            ORDER BY spot
   442	        """
   443	        pts = conn.execute(sql_exact, (filter_val, timestamp)).fetchall()
   444	        if pts:
   445	            res = [dict(r) for r in pts]
   446	            self._cache_put(cache_key, res)
   447	            return res
   448	
   449	        # Fallback: timestamp mais recente
   450	        sql_ts = f"""
   451	            SELECT {p['timestamp']} AS ts
   452	            FROM {self._payoff_table}
   453	            WHERE {filter_col} = ?
   454	            ORDER BY ts DESC
   455	            LIMIT 1
   456	        """
   457	        r = conn.execute(sql_ts, (filter_val,)).fetchone()
   458	        if not r:
   459	            self._cache_put(cache_key, [])
   460	            return []
   461	
   462	        ts_near = r["ts"]
   463	        pts2 = conn.execute(
   464	            f"""
   465	            SELECT {p['spot']} AS spot, {p['pl']} AS pl
   466	            FROM {self._payoff_table}
   467	            WHERE {filter_col} = ? AND {p['timestamp']} = ?
   468	            ORDER BY spot
   469	            """,
   470	            (filter_val, ts_near),
   471	        ).fetchall()
   472	        res = [dict(x) for x in pts2]
   473	        self._cache_put(cache_key, res)
   474	        return res
   475	
   476	    def get_payoff_curve_info(
   477	        self, structure_id: str, timestamp: str
   478	    ) -> Tuple[List[Dict], Dict]:
   479	        """
   480	         alteracao_33: usa structure_id como chave primária quando disponível.
   481	        Fallback para aba mantido para compatibilidade.
   482	        """
   483	        import time
   484	
   485	        t0 = time.time()
   486	
   487	        if not self._payoff_table:
   488	            self.refresh()
   489	
   490	        ts_key = timestamp if timestamp is not None else "__latest__"
   491	        cache_key = (str(structure_id), ts_key)
   492	        cached = self._cache_get(cache_key)
   493	
   494	        if (
   495	            cached is not None
   496	            and isinstance(cached, dict)
   497	            and "points" in cached
   498	            and "info" in cached
   499	        ):
   500	            return cached.get("points", []), cached.get("info", {})
   501	
   502	        p = self._payoff_cols
   503	        #  alteracao_33: resolve coluna + valor de filtro
   504	        # alteracao_34: structure_id e sempre INTEGER
   505	        filter_col = self._structure_filter_col(p)
   506	
   507	        conn = self._connect_derived_threadsafe()
   508	        try:
   509	            filter_val = self._resolve_structure_key(structure_id)
   510	            info: Dict[str, Any] = {
   511	                "structure_id": structure_id,
   512	                "aba": structure_id,   #  patch_3a: aba espelha structure_id (compat)
   513	                "requested_timestamp": timestamp,
   514	                "used_timestamp": timestamp,
   515	                "fallback": False,
   516	                "source_table": self._payoff_table,
   517	                "filter_col": filter_col,       #  alteracao_33: auditoria
   518	                "filter_val": filter_val,       #  alteracao_33: auditoria
   519	                "count_points": 0,
   520	                "created_at": None,
   521	                "meta_json": None,
   522	            }
   523	
   524	            if self._payoff_table == "payoff_curve_points":
   525	                # Contrato canônico: colunas fixas, só muda o filtro
   526	                extra_cols = ""
   527	                if "meta_json" in self._inspect_columns("payoff_curve_points"):
   528	                    extra_cols = ", meta_json, created_at"
   529	
   530	                sql = (
   531	                    f"SELECT point_spot AS spot, point_pl AS pl{extra_cols} "
   532	                    f"FROM payoff_curve_points "
   533	                    f"WHERE {filter_col} = ? AND timestamp = ? "
   534	                    f"ORDER BY point_spot"
   535	                )
   536	                rows = conn.execute(sql, (filter_val, timestamp)).fetchall()
   537	                used_ts = timestamp
   538	
   539	                if not rows:
   540	                    row_ts = conn.execute(
   541	                        f"SELECT timestamp FROM payoff_curve_points "
   542	                        f"WHERE {filter_col} = ? ORDER BY timestamp DESC LIMIT 1",
   543	                        (filter_val,),
   544	                    ).fetchone()
   545	                    if row_ts and row_ts["timestamp"]:
   546	                        used_ts = row_ts["timestamp"]
   547	                        info["used_timestamp"] = used_ts
   548	                        info["fallback"] = True
   549	                        rows = conn.execute(sql, (filter_val, used_ts)).fetchall()
   550	
   551	                points = [{"spot": r["spot"], "pl": r["pl"]} for r in rows]
   552	                info["count_points"] = len(points)
   553	
   554	                if rows and extra_cols:
   555	                    info["created_at"] = rows[0]["created_at"]
   556	                    info["meta_json"] = rows[0]["meta_json"]
   557	
   558	            else:
   559	                required = ["timestamp", "spot", "pl"]
   560	                if any(k not in p for k in required):
   561	                    raise RuntimeError(
   562	                        f"Tabela {self._payoff_table} não possui colunas esperadas."
   563	                    )
   564	
   565	                sql_exact = (
   566	                    f"SELECT {p['spot']} AS spot, {p['pl']} AS pl "
   567	                    f"FROM {self._payoff_table} "
   568	                    f"WHERE {filter_col} = ? AND {p['timestamp']} = ? "
   569	                    f"ORDER BY spot"
   570	                )
   571	                rows = conn.execute(sql_exact, (filter_val, timestamp)).fetchall()
   572	                used_ts = timestamp
   573	
   574	                if not rows:
   575	                    sql_ts = (
   576	                        f"SELECT {p['timestamp']} AS ts FROM {self._payoff_table} "
   577	                        f"WHERE {filter_col} = ? ORDER BY ts DESC LIMIT 1"
   578	                    )
   579	                    rts = conn.execute(sql_ts, (filter_val,)).fetchone()
   580	                    if rts and rts["ts"]:
   581	                        used_ts = rts["ts"]
   582	                        info["used_timestamp"] = used_ts
   583	                        info["fallback"] = True
   584	                        rows = conn.execute(sql_exact, (filter_val, used_ts)).fetchall()
   585	
   586	                points = [{"spot": r["spot"], "pl": r["pl"]} for r in rows]
   587	                info["count_points"] = len(points)
   588	
   589	        finally:
   590	            try:
   591	                conn.close()
   592	            except Exception:
   593	                pass
   594	
   595	        info["query_ms"] = int((time.time() - t0) * 1000)
   596	        payload = {"points": points, "info": info}
   597	        self._cache_put(cache_key, payload)
   598	        return points, info
   599	
   600	    def export_to_csv(self, data: List[Dict], filename: str):
   601	        if not data:
   602	            headers = [
   603	                "timestamp", "structure_id", "aba", "decision", "level",
   604	                "pl_pct_of_max", "dte_min", "why", "why_json",
   605	                "pl_atual", "pl_max", "spot_ref",
   606	            ]
   607	            with open(filename, "w", newline="", encoding="utf-8") as f:
   608	                w = csv.DictWriter(f, fieldnames=headers)
   609	                w.writeheader()
   610	            return
   611	
   612	        headers = list({k for row in data for k in row.keys()})
   613	        with open(filename, "w", newline="", encoding="utf-8") as f:
   614	            w = csv.DictWriter(f, fieldnames=headers)
   615	            w.writeheader()
   616	            for row in data:
   617	                out = dict(row)
   618	                if isinstance(out.get("why"), (dict, list)):
   619	                    out["why"] = json.dumps(out["why"], ensure_ascii=False)
   620	                w.writerow(out)
   621	
   622	    def check_database_status(self) -> str:
   623	        self.refresh()
   624	        conn = self._connect()
   625	        ctbl = self._consolidations_table
   626	        c = self._consolidations_cols
   627	
   628	        cnt = conn.execute(f"SELECT COUNT(*) AS n FROM {ctbl}").fetchone()["n"]
   629	
   630	        ts_col = c.get("timestamp")
   631	        last_ts = None
   632	        if ts_col:
   633	            r = conn.execute(
   634	                f"SELECT {ts_col} AS ts FROM {ctbl} ORDER BY ts DESC LIMIT 1"
   635	            ).fetchone()
   636	            last_ts = r["ts"] if r else None
   637	
   638	        n_structures = len(self._cache_structures)
   639	        payoff_ok = bool(self._payoff_table)
   640	
   641	        #  alteracao_33: reporta qual coluna de filtro está ativa
   642	        p = self._payoff_cols
   643	        try:
   644	            filter_col = self._structure_filter_col(p)
   645	            filter_info = f"{filter_col} (mode=canonical)"  # alteracao_34: sempre canonico
   646	        except Exception:
   647	            filter_info = "N/A"
   648	
   649	        return (
   650	            f"derived.db: OK\n"
   651	            f"Consolidações: {ctbl} (linhas: {cnt}, estruturas: {n_structures})\n"
   652	            f"Timestamp mais recente: {last_ts}\n"
   653	            f"Tabela de payoff: {self._payoff_table if payoff_ok else 'NÃO ENCONTRADA'}\n"
   654	            f"Filtro de estrutura ativo: {filter_info}"    #  alteracao_33
   655	        )
   656	
   657	    def clear_cache(self):
   658	        self._cache_structures = []
   659	        self._payoff_cache = {}
   660	
   661	    # _connect_derived_threadsafe agora e apenas alias de _connect
   662	    def _connect_derived_threadsafe(self) -> sqlite3.Connection:
   663	        return self._connect()
   664	
   665	    def _cache_get(self, key: Tuple) -> Optional[Any]:
   666	        try:
   667	            return self._payoff_cache.get(key)
   668	        except Exception:
   669	            return None
   670	
   671	    def _cache_put(self, key: Tuple, value: Any):
   672	        try:
   673	            self._payoff_cache[key] = value
   674	            mx = getattr(self, "_payoff_cache_max", 0) or 0
   675	            if mx > 0 and len(self._payoff_cache) > mx:
   676	                self._payoff_cache.pop(next(iter(self._payoff_cache)))
   677	        except Exception:
   678	            pass
```

## FILE: UI/components/details_panel.py
```python
     1	# UI/components/details_panel.py
     2	import tkinter as tk
     3	from tkinter import ttk, scrolledtext
     4	from typing import Dict, Optional, Any
     5	import json
     6	import sqlite3
     7	from pathlib import Path
     8	
     9	
    10	class DetailsPanel(ttk.LabelFrame):
    11	    def __init__(self, parent, on_recalculate=None, app_db_path=None):
    12	        super().__init__(parent)
    13	        self._on_recalculate_cb = on_recalculate
    14	        self._app_db_path = str(app_db_path) if app_db_path else None
    15	        self._recalc_in_progress = False
    16	        self._last_recalc_signature = None
    17	        self._current_decision = None
    18	
    19	        try:
    20	            self._project_root = Path(__file__).resolve().parents[2]
    21	        except Exception:
    22	            self._project_root = None
    23	
    24	        self._setup_widgets()
    25	
    26	    # ------------------------------------------------------------------
    27	    # Estado do recalc
    28	    # ------------------------------------------------------------------
    29	
    30	    def _set_recalc_ui_state(self, in_progress: bool, msg: str = "", color: str = "gray"):
    31	        self._recalc_in_progress = in_progress
    32	        try:
    33	            if hasattr(self, "btn_recalculate") and self.btn_recalculate:
    34	                self.btn_recalculate.config(
    35	                    state="disabled" if in_progress else "normal"
    36	                )
    37	        except Exception:
    38	            pass
    39	        try:
    40	            if hasattr(self, "lbl_recalc_status") and self.lbl_recalc_status:
    41	                self.lbl_recalc_status.config(text=msg, foreground=color)
    42	        except Exception:
    43	            pass
    44	
    45	    # ------------------------------------------------------------------
    46	    # Caminhos de DB
    47	    # ------------------------------------------------------------------
    48	
    49	
    50	    def _derived_db_path(self) -> Path:
    51	        """
    52	        Caminho do derived.db.
    53	
    54	        Compatibilidade para testes:
    55	        - se o painel tiver db_path/_db_path explícito, usa esse arquivo;
    56	        - caso contrário, respeita self._project_root quando definido;
    57	        - fallback final: raiz do projeto inferida pelo arquivo atual.
    58	        """
    59	        for attr in ("db_path", "_db_path", "database_path", "_database_path"):
    60	            value = getattr(self, attr, None)
    61	            if value and not callable(value):
    62	                return Path(value)
    63	
    64	        project_root = getattr(self, "_project_root", None)
    65	        if project_root is None:
    66	            project_root = Path(__file__).resolve().parents[2]
    67	        else:
    68	            project_root = Path(project_root)
    69	
    70	        return project_root / "dados" / "derived.db"
    71	
    72	    def _operational_app_db_path(self) -> Path:
    73	        """
    74	        Caminho do app.db usado para estado operacional.
    75	
    76	        Importante: não usa self._db_path porque _derived_db_path() já trata
    77	        esse atributo como caminho do derived.db em testes/compatibilidade.
    78	        """
    79	        if self._app_db_path:
    80	            return Path(self._app_db_path)
    81	
    82	        project_root = getattr(self, "_project_root", None)
    83	        if project_root is None:
    84	            project_root = Path(__file__).resolve().parents[2]
    85	        else:
    86	            project_root = Path(project_root)
    87	
    88	        return project_root / "dados" / "app.db"
    89	
    90	    def _resolve_structure_key(self, structure_id) -> int:
    91	        """
    92	        structure_id é sempre INTEGER no DB.
    93	        Aceita str ("7") ou int (7). Lança ValueError se não conversível.
    94	        """
    95	        try:
    96	            return int(structure_id)
    97	        except (TypeError, ValueError) as exc:
    98	            raise ValueError(
    99	                f"structure_id inválido: {structure_id!r}. "
   100	                "Esperado inteiro ou string numérica."
   101	            ) from exc
   102	
   103	    # ------------------------------------------------------------------
   104	    # Assinatura de recalc (dedupe)
   105	    # ------------------------------------------------------------------
   106	
   107	    def _get_latest_snapshot_timestamp_for_structure(self, structure_id):
   108	        """
   109	        Retorna o timestamp mais recente de snapshot para uma estrutura.
   110	
   111	        Regra importante para compatibilidade com alteracao_35:
   112	        - se a instância recebeu um caminho explícito de DB, usa somente ele;
   113	        - se esse DB explícito não existe, retorna None;
   114	        - só usa fallback em bancos default quando não há DB explícito na instância.
   115	        """
   116	        import sqlite3
   117	        from pathlib import Path
   118	
   119	        sid = self._resolve_structure_key(structure_id)
   120	        sid_text = str(sid)
   121	
   122	        def _safe_path(value):
   123	            if value is None:
   124	                return None
   125	            try:
   126	                if callable(value):
   127	                    value = value()
   128	            except TypeError:
   129	                return None
   130	            if value is None:
   131	                return None
   132	            try:
   133	                return Path(value)
   134	            except TypeError:
   135	                return None
   136	
   137	        def _looks_like_db_path(name, path):
   138	            low_name = str(name).lower()
   139	            try:
   140	                suffix = Path(path).suffix.lower()
   141	            except Exception:
   142	                suffix = ""
   143	
   144	            return (
   145	                suffix in {".db", ".sqlite", ".sqlite3"}
   146	                or "db" in low_name
   147	                or "database" in low_name
   148	                or "sqlite" in low_name
   149	            )
   150	
   151	        candidates = []
   152	        primary_explicit = []
   153	        derived_explicit = []
   154	
   155	        # 1) Caminhos explicitamente configurados NA INSTÂNCIA.
   156	        #
   157	        # Regra crítica:
   158	        # se existe raw/app DB explícito, usa SOMENTE ele.
   159	        # Não pode cair para derived.db quando o raw/app não existe.
   160	        instance_dict = getattr(self, "__dict__", {}) or {}
   161	
   162	        preferred_instance_names = [
   163	            "_raw_db_path",
   164	            "raw_db_path",
   165	            "_app_db_path",
   166	            "app_db_path",
   167	            "_db_path",
   168	            "db_path",
   169	            "_database_path",
   170	            "database_path",
   171	            "_sqlite_path",
   172	            "sqlite_path",
   173	            "_db_file",
   174	            "db_file",
   175	            "_derived_db_path",
   176	            "derived_db_path",
   177	        ]
   178	
   179	        ordered_instance_names = []
   180	        for name in preferred_instance_names:
   181	            if name in instance_dict and name not in ordered_instance_names:
   182	                ordered_instance_names.append(name)
   183	
   184	        for name in instance_dict:
   185	            if name not in ordered_instance_names:
   186	                ordered_instance_names.append(name)
   187	
   188	        for name in ordered_instance_names:
   189	            value = instance_dict.get(name)
   190	            p = _safe_path(value)
   191	            if p is None:
   192	                continue
   193	            if not _looks_like_db_path(name, p):
   194	                continue
   195	
   196	            low_name = str(name).lower()
   197	            low_path = str(p).lower()
   198	
   199	            is_derived = (
   200	                "derived" in low_name
   201	                or "deriv" in low_name
   202	                or low_path.endswith("derived.db")
   203	                or "derived.db" in low_path
   204	            )
   205	
   206	            if is_derived:
   207	                derived_explicit.append(p)
   208	            else:
   209	                primary_explicit.append(p)
   210	
   211	        if primary_explicit:
   212	            candidates = primary_explicit
   213	        elif derived_explicit:
   214	            candidates = derived_explicit
   215	        else:
   216	            # 2) Sem DB explícito na instância: agora sim pode usar defaults.
   217	            class_level_names = [
   218	                "_derived_db_path",
   219	                "derived_db_path",
   220	                "_raw_db_path",
   221	                "raw_db_path",
   222	                "_app_db_path",
   223	                "app_db_path",
   224	                "_db_path",
   225	                "db_path",
   226	                "_database_path",
   227	                "database_path",
   228	                "_sqlite_path",
   229	                "sqlite_path",
   230	                "_db_file",
   231	                "db_file",
   232	            ]
   233	
   234	            for name in class_level_names:
   235	                try:
   236	                    attr = getattr(self, name, None)
   237	                except Exception:
   238	                    attr = None
   239	
   240	                p = _safe_path(attr)
   241	                if p is not None and _looks_like_db_path(name, p):
   242	                    candidates.append(p)
   243	
   244	            project_root = getattr(self, "_project_root", None)
   245	            if project_root is not None:
   246	                project_root = Path(project_root)
   247	            else:
   248	                project_root = Path(__file__).resolve().parents[2]
   249	
   250	            candidates.extend(
   251	                [
   252	                    project_root / "app.db",
   253	                    project_root / "app2.db",
   254	                    project_root / "derived.db",
   255	                    project_root / "dados" / "app.db",
   256	                    project_root / "dados" / "app2.db",
   257	                    project_root / "dados" / "derived.db",
   258	                ]
   259	            )
   260	
   261	            for base in [project_root, project_root / "dados"]:
   262	                try:
   263	                    candidates.extend(sorted(base.glob("*.db")))
   264	                except Exception:
   265	                    pass
   266	
   267	        # Remove duplicados preservando ordem.
   268	        unique = []
   269	        seen = set()
   270	        for p in candidates:
   271	            try:
   272	                key = str(p.resolve()) if p.exists() else str(p)
   273	            except Exception:
   274	                key = str(p)
   275	            if key not in seen:
   276	                seen.add(key)
   277	                unique.append(p)
   278	
   279	        def q(identifier):
   280	            return '"' + str(identifier).replace('"', '""') + '"'
   281	
   282	        def table_names(cur):
   283	            rows = cur.execute(
   284	                """
   285	                SELECT name
   286	                FROM sqlite_master
   287	                WHERE type = 'table'
   288	                  AND name NOT LIKE 'sqlite_%'
   289	                """
   290	            ).fetchall()
   291	            return [r[0] for r in rows]
   292	
   293	        def columns_for(cur, table):
   294	            rows = cur.execute(f"PRAGMA table_info({q(table)})").fetchall()
   295	            return [r[1] for r in rows]
   296	
   297	        def looks_like_structure_col(col):
   298	            low = str(col).lower()
   299	            return (
   300	                low == "structure_id"
   301	                or low == "id_structure"
   302	                or low == "estrutura_id"
   303	                or low == "id_estrutura"
   304	                or low.endswith("_structure_id")
   305	                or low.endswith("_estrutura_id")
   306	            )
   307	
   308	        def timestamp_score(col):
   309	            low = str(col).lower()
   310	
   311	            priority = {
   312	                "timestamp": 100,
   313	                "snapshot_timestamp": 99,
   314	                "snapshot_ts": 98,
   315	                "created_at": 97,
   316	                "updated_at": 96,
   317	                "ts": 95,
   318	                "datetime": 94,
   319	                "date": 93,
   320	                "data_hora": 92,
   321	            }
   322	
   323	            if low in priority:
   324	                return priority[low]
   325	
   326	            if "timestamp" in low:
   327	                return 90
   328	            if "snapshot" in low and ("time" in low or "date" in low or "ts" in low):
   329	                return 89
   330	            if low.endswith("_ts"):
   331	                return 88
   332	            if "created" in low:
   333	                return 87
   334	            if "updated" in low:
   335	                return 86
   336	            if "time" in low:
   337	                return 85
   338	            if "date" in low:
   339	                return 84
   340	            if "data" in low:
   341	                return 83
   342	
   343	            return 0
   344	
   345	        def latest_in_table(cur, table):
   346	            cols = columns_for(cur, table)
   347	            if not cols:
   348	                return None
   349	
   350	            structure_cols = [c for c in cols if looks_like_structure_col(c)]
   351	
   352	            if not structure_cols:
   353	                for c in cols:
   354	                    low = str(c).lower()
   355	                    if low in {"structure", "estrutura"}:
   356	                        structure_cols.append(c)
   357	
   358	            if not structure_cols:
   359	                return None
   360	
   361	            ts_cols = sorted(
   362	                [c for c in cols if timestamp_score(c) > 0],
   363	                key=timestamp_score,
   364	                reverse=True,
   365	            )
   366	
   367	            if not ts_cols:
   368	                ignored = {str(c).lower() for c in structure_cols}
   369	                ignored.update(
   370	                    {
   371	                        "id",
   372	                        "structure_id",
   373	                        "id_structure",
   374	                        "estrutura_id",
   375	                        "id_estrutura",
   376	                    }
   377	                )
   378	                ts_cols = [c for c in cols if str(c).lower() not in ignored]
   379	
   380	            best = None
   381	
   382	            for s_col in structure_cols:
   383	                for ts_col in ts_cols:
   384	                    try:
   385	                        row = cur.execute(
   386	                            f"""
   387	                            SELECT MAX({q(ts_col)})
   388	                            FROM {q(table)}
   389	                            WHERE {q(s_col)} = ?
   390	                               OR CAST({q(s_col)} AS TEXT) = ?
   391	                            """,
   392	                            (sid, sid_text),
   393	                        ).fetchone()
   394	                    except sqlite3.Error:
   395	                        continue
   396	
   397	                    if row and row[0] is not None:
   398	                        value = str(row[0])
   399	                        if best is None or value > best:
   400	                            best = value
   401	
   402	            return best
   403	
   404	        preferred = [
   405	            "robo_legs_snapshot",
   406	            "robo_snapshot",
   407	            "snapshots",
   408	            "snapshot",
   409	            "structure_snapshots",
   410	            "structure_decisions",
   411	            "payoff_curve_points",
   412	        ]
   413	
   414	        for db_path in unique:
   415	            if not db_path.exists():
   416	                continue
   417	
   418	            try:
   419	                con = sqlite3.connect(str(db_path))
   420	                try:
   421	                    cur = con.cursor()
   422	                    tables = table_names(cur)
   423	
   424	                    ordered = []
   425	                    for t in preferred:
   426	                        if t in tables and t not in ordered:
   427	                            ordered.append(t)
   428	                    for t in tables:
   429	                        if t not in ordered:
   430	                            ordered.append(t)
   431	
   432	                    for table in ordered:
   433	                        ts = latest_in_table(cur, table)
   434	                        if ts is not None:
   435	                            return ts
   436	                finally:
   437	                    con.close()
   438	            except sqlite3.Error:
   439	                continue
   440	
   441	        return None
   442	
   443	    def _compute_recalc_signature(self, structure_id):
   444	        return (
   445	            structure_id,
   446	            self._get_latest_snapshot_timestamp_for_structure(structure_id),
   447	        )
   448	
   449	    # ------------------------------------------------------------------
   450	    # Widgets
   451	    # ------------------------------------------------------------------
   452	
   453	    def _setup_widgets(self):
   454	        self.grid_rowconfigure(3, weight=1)
   455	        self.grid_columnconfigure(1, weight=1)
   456	
   457	        # Informações Básicas
   458	        basic_frame = ttk.LabelFrame(self, text="Informações Básicas", padding=5)
   459	        basic_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 5))
   460	        basic_frame.grid_columnconfigure(1, weight=1)
   461	        basic_frame.grid_columnconfigure(3, weight=1)
   462	
   463	        ttk.Label(basic_frame, text="Timestamp:").grid(
   464	            row=0, column=0, sticky="w", padx=(0, 5)
   465	        )
   466	        self.timestamp_label = ttk.Label(
   467	            basic_frame, text="N/A", background="white", relief="sunken"
   468	        )
   469	        self.timestamp_label.grid(row=0, column=1, sticky="ew", padx=(0, 10))
   470	
   471	        ttk.Label(basic_frame, text="Estrutura:").grid(
   472	            row=0, column=2, sticky="w", padx=(0, 5)
   473	        )
   474	        self.structure_label = ttk.Label(
   475	            basic_frame, text="N/A", background="white", relief="sunken"
   476	        )
   477	        self.structure_label.grid(row=0, column=3, sticky="ew")
   478	
   479	        ttk.Label(basic_frame, text="Decisão:").grid(
   480	            row=1, column=0, sticky="w", padx=(0, 5)
   481	        )
   482	        self.decision_label = ttk.Label(
   483	            basic_frame, text="N/A", background="white", relief="sunken"
   484	        )
   485	        self.decision_label.grid(row=1, column=1, sticky="ew", padx=(0, 10))
   486	
   487	        ttk.Label(basic_frame, text="Nível:").grid(
   488	            row=1, column=2, sticky="w", padx=(0, 5)
   489	        )
   490	        self.level_label = ttk.Label(
   491	            basic_frame, text="N/A", background="white", relief="sunken"
   492	        )
   493	        self.level_label.grid(row=1, column=3, sticky="ew")
   494	
   495	        # Métricas Financeiras
   496	        metrics_frame = ttk.LabelFrame(self, text="Métricas Financeiras", padding=5)
   497	        metrics_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
   498	        metrics_frame.grid_columnconfigure(1, weight=1)
   499	        metrics_frame.grid_columnconfigure(3, weight=1)
   500	
   501	        ttk.Label(metrics_frame, text="PL Atual:").grid(
   502	            row=0, column=0, sticky="w", padx=(0, 5)
   503	        )
   504	        self.pl_atual_label = ttk.Label(
   505	            metrics_frame, text="N/A", background="white", relief="sunken"
   506	        )
   507	        self.pl_atual_label.grid(row=0, column=1, sticky="ew", padx=(0, 10))
   508	
   509	        ttk.Label(metrics_frame, text="PL Máximo:").grid(
   510	            row=0, column=2, sticky="w", padx=(0, 5)
   511	        )
   512	        self.pl_max_label = ttk.Label(
   513	            metrics_frame, text="N/A", background="white", relief="sunken"
   514	        )
   515	        self.pl_max_label.grid(row=0, column=3, sticky="ew")
   516	
   517	        ttk.Label(metrics_frame, text="Ratio:").grid(
   518	            row=1, column=0, sticky="w", padx=(0, 5)
   519	        )
   520	        self.ratio_label = ttk.Label(
   521	            metrics_frame, text="N/A", background="white", relief="sunken"
   522	        )
   523	        self.ratio_label.grid(row=1, column=1, sticky="ew", padx=(0, 10))
   524	
   525	        ttk.Label(metrics_frame, text="DTE Mín:").grid(
   526	            row=1, column=2, sticky="w", padx=(0, 5)
   527	        )
   528	        self.dte_label = ttk.Label(
   529	            metrics_frame, text="N/A", background="white", relief="sunken"
   530	        )
   531	        self.dte_label.grid(row=1, column=3, sticky="ew")
   532	
   533	        ttk.Label(metrics_frame, text="Spot Ref:").grid(
   534	            row=2, column=0, sticky="w", padx=(0, 5)
   535	        )
   536	        self.spot_ref_label = ttk.Label(
   537	            metrics_frame, text="N/A", background="white", relief="sunken"
   538	        )
   539	        self.spot_ref_label.grid(row=2, column=1, sticky="ew", padx=(0, 10))
   540	
   541	        ttk.Label(metrics_frame, text="Breakevens:").grid(
   542	            row=2, column=2, sticky="w", padx=(0, 5)
   543	        )
   544	        self.breakevens_label = ttk.Label(
   545	            metrics_frame, text="N/A", background="white", relief="sunken"
   546	        )
   547	        self.breakevens_label.grid(row=2, column=3, sticky="ew")
   548	
   549	        # Estado Operacional
   550	        operational_frame = ttk.LabelFrame(self, text="Estado Operacional", padding=5)
   551	        operational_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)
   552	        operational_frame.grid_columnconfigure(1, weight=1)
   553	        operational_frame.grid_columnconfigure(3, weight=1)
   554	
   555	        ttk.Label(operational_frame, text="Eventos aplicados:").grid(
   556	            row=0, column=0, sticky="w", padx=(0, 5)
   557	        )
   558	        self.operational_events_applied_label = ttk.Label(
   559	            operational_frame, text="N/A", background="white", relief="sunken"
   560	        )
   561	        self.operational_events_applied_label.grid(
   562	            row=0, column=1, sticky="ew", padx=(0, 10)
   563	        )
   564	
   565	        ttk.Label(operational_frame, text="Cancelados ignorados:").grid(
   566	            row=0, column=2, sticky="w", padx=(0, 5)
   567	        )
   568	        self.operational_cancelled_ignored_label = ttk.Label(
   569	            operational_frame, text="N/A", background="white", relief="sunken"
   570	        )
   571	        self.operational_cancelled_ignored_label.grid(
   572	            row=0, column=3, sticky="ew"
   573	        )
   574	
   575	        ttk.Label(operational_frame, text="Status:").grid(
   576	            row=1, column=0, sticky="w", padx=(0, 5)
   577	        )
   578	        self.operational_status_label = ttk.Label(
   579	            operational_frame, text="N/A", background="white", relief="sunken"
   580	        )
   581	        self.operational_status_label.grid(
   582	            row=1, column=1, columnspan=3, sticky="ew"
   583	        )
   584	
   585	        # Rationale JSON
   586	        json_frame = ttk.LabelFrame(self, text="Rationale / Why JSON", padding=5)
   587	        json_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(5, 0))
   588	        json_frame.grid_rowconfigure(0, weight=1)
   589	        json_frame.grid_columnconfigure(0, weight=1)
   590	
   591	        self.why_text = scrolledtext.ScrolledText(
   592	            json_frame,
   593	            height=8,
   594	            wrap=tk.WORD,
   595	            font=("Consolas", 9),
   596	            background="#f8f9fa",
   597	        )
   598	        self.why_text.grid(row=0, column=0, sticky="nsew")
   599	
   600	        # Auditoria & Ações
   601	        audit_frame = ttk.LabelFrame(self, text="Auditoria & Ações", padding=5)
   602	        audit_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)
   603	        audit_frame.grid_columnconfigure(1, weight=1)
   604	        audit_frame.grid_columnconfigure(3, weight=1)
   605	
   606	        ttk.Label(audit_frame, text="Fonte:").grid(
   607	            row=0, column=0, sticky="w", padx=(0, 5)
   608	        )
   609	        self.source_label = ttk.Label(
   610	            audit_frame, text="N/A", background="white", relief="sunken"
   611	        )
   612	        self.source_label.grid(row=0, column=1, sticky="ew", padx=(0, 10))
   613	
   614	        ttk.Label(audit_frame, text="Created At:").grid(
   615	            row=0, column=2, sticky="w", padx=(0, 5)
   616	        )
   617	        self.created_at_label = ttk.Label(
   618	            audit_frame, text="N/A", background="white", relief="sunken"
   619	        )
   620	        self.created_at_label.grid(row=0, column=3, sticky="ew")
   621	
   622	        actions_frame = ttk.Frame(audit_frame)
   623	        actions_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(5, 0))
   624	
   625	        self.btn_recalculate = ttk.Button(
   626	            actions_frame,
   627	            text="Recalcular esta estrutura",
   628	            command=self._on_recalculate_click,
   629	        )
   630	        self.btn_recalculate.pack(side="left", padx=(0, 10))
   631	
   632	        self.lbl_recalc_status = ttk.Label(
   633	            actions_frame, text="", foreground="gray"
   634	        )
   635	        self.lbl_recalc_status.pack(side="left")
   636	
   637	    # ------------------------------------------------------------------
   638	    # API pública
   639	    # ------------------------------------------------------------------
   640	
   641	    def update_decision(self, decision_data: Dict):
   642	        self._current_decision = dict(decision_data) if decision_data else None
   643	
   644	        self.timestamp_label.config(text=decision_data.get("timestamp", "N/A"))
   645	
   646	        # alteracao_36: structure_id é autoritativo; aba removido
   647	        structure_id = decision_data.get("structure_id") or "N/A"
   648	        self.structure_label.config(text=str(structure_id))
   649	
   650	        self.decision_label.config(text=decision_data.get("decision", "N/A"))
   651	        self.level_label.config(text=str(decision_data.get("level", "N/A")))
   652	
   653	        self._format_currency_label(self.pl_atual_label, decision_data.get("pl_atual"))
   654	        self._format_currency_label(self.pl_max_label, decision_data.get("pl_max"))
   655	
   656	        ratio = decision_data.get("pl_pct_of_max")
   657	        self.ratio_label.config(
   658	            text=f"{ratio * 100:.1f}%" if ratio is not None else "N/A"
   659	        )
   660	
   661	        self.dte_label.config(text=str(decision_data.get("dte_min", "N/A")))
   662	
   663	        spot_ref = decision_data.get("spot_reference") or decision_data.get("spot_ref")
   664	        if spot_ref is not None:
   665	            try:
   666	                self.spot_ref_label.config(text=f"{float(spot_ref):.2f}")
   667	            except Exception:
   668	                self.spot_ref_label.config(text=str(spot_ref))
   669	        else:
   670	            self.spot_ref_label.config(text="N/A")
   671	
   672	        why_payload = decision_data.get("why") or decision_data.get("why_json")
   673	        self.why_text.delete("1.0", tk.END)
   674	        if why_payload:
   675	            try:
   676	                if isinstance(why_payload, str):
   677	                    formatted = json.dumps(
   678	                        json.loads(why_payload), indent=2, ensure_ascii=False
   679	                    )
   680	                else:
   681	                    formatted = json.dumps(why_payload, indent=2, ensure_ascii=False)
   682	                self.why_text.insert("1.0", formatted)
   683	            except Exception:
   684	                self.why_text.insert("1.0", str(why_payload))
   685	        else:
   686	            self.why_text.insert("1.0", "Sem rationale disponível")
   687	
   688	        self.source_label.config(text="N/A")
   689	        self.created_at_label.config(text="N/A")
   690	        self.lbl_recalc_status.config(text="", foreground="gray")
   691	        self._clear_operational_state()
   692	
   693	        if structure_id != "N/A":
   694	            self._refresh_operational_state_for_structure(structure_id)
   695	
   696	    def update_breakevens(self, breakevens, pl_at_spot_ref):
   697	        if breakevens:
   698	            try:
   699	                self.breakevens_label.config(
   700	                    text=", ".join([f"{float(be):.2f}" for be in breakevens])
   701	                )
   702	            except Exception:
   703	                self.breakevens_label.config(text=str(breakevens))
   704	        else:
   705	            self.breakevens_label.config(text="N/A")
   706	
   707	    def update_audit_info(self, info: Dict):
   708	        source_table = info.get("source_table", "N/A")
   709	        n = info.get("count_points", info.get("points_count", ""))
   710	        suffix = f" ({n} pts)" if n != "" else ""
   711	        txt = f"{source_table}{suffix}"
   712	        if info.get("fallback"):
   713	            txt += " [fallback]"
   714	        self.source_label.config(text=txt)
   715	
   716	        created_at = info.get("created_at")
   717	        self.created_at_label.config(text=created_at if created_at else "N/A")
   718	
   719	    def clear(self):
   720	        self._current_decision = None
   721	        for lbl in [
   722	            self.timestamp_label, self.structure_label, self.decision_label,
   723	            self.level_label, self.pl_atual_label, self.pl_max_label,
   724	            self.ratio_label, self.dte_label, self.spot_ref_label,
   725	            self.breakevens_label, self.source_label, self.created_at_label,
   726	            self.operational_events_applied_label,
   727	            self.operational_cancelled_ignored_label,
   728	            self.operational_status_label,
   729	        ]:
   730	            lbl.config(text="N/A")
   731	        self.why_text.delete("1.0", tk.END)
   732	        self.lbl_recalc_status.config(text="", foreground="gray")
   733	
   734	    def on_recalc_finished(self, structure_id, ok: bool, message: str = ""):
   735	        """Chamado pelo MainWindow ao finalizar o subprocess do pipeline."""
   736	        try:
   737	            if ok:
   738	                self._last_recalc_signature = self._compute_recalc_signature(
   739	                    structure_id
   740	                )
   741	                self._set_recalc_ui_state(
   742	                    False,
   743	                    msg=message or f"OK: {structure_id} recalculado",
   744	                    color="green",
   745	                )
   746	            else:
   747	                self._set_recalc_ui_state(
   748	                    False,
   749	                    msg=message or "Falha no recálculo",
   750	                    color="red",
   751	                )
   752	        except Exception:
   753	            self._recalc_in_progress = False
   754	
   755	    def _clear_operational_state(self):
   756	        for label_name in [
   757	            "operational_events_applied_label",
   758	            "operational_cancelled_ignored_label",
   759	            "operational_status_label",
   760	        ]:
   761	            label = getattr(self, label_name, None)
   762	            if label is not None:
   763	                label.config(text="N/A")
   764	
   765	    def update_operational_state(self, effective_structure: Dict[str, Any]):
   766	        """
   767	        Atualiza os widgets de Estado Operacional.
   768	
   769	        Aceita o formato retornado por StructureEventsService.apply_events_to_structure:
   770	        {
   771	            "legs": [...],
   772	            "operational_state": {
   773	                "events_applied": int,
   774	                "events_ignored_cancelled": int,
   775	                "is_closed": bool,
   776	            }
   777	        }
   778	
   779	        Também aceita formatos legados/testes com:
   780	        - is_closed no topo;
   781	        - applied_events;
   782	        - ignored_events.
   783	        """
   784	        if not isinstance(effective_structure, dict):
   785	            self._clear_operational_state()
   786	            return
   787	
   788	        state = effective_structure.get("operational_state")
   789	        if not isinstance(state, dict):
   790	            state = {}
   791	
   792	        applied = state.get("events_applied")
   793	        if applied is None and isinstance(effective_structure.get("applied_events"), list):
   794	            applied = len(effective_structure.get("applied_events") or [])
   795	
   796	        ignored = state.get("events_ignored_cancelled")
   797	        if ignored is None and isinstance(effective_structure.get("ignored_events"), list):
   798	            ignored = len(effective_structure.get("ignored_events") or [])
   799	
   800	        is_closed = state.get("is_closed", effective_structure.get("is_closed"))
   801	
   802	        if is_closed is True:
   803	            status_text = "Encerrada"
   804	        elif is_closed is False:
   805	            status_text = "Aberta"
   806	        else:
   807	            status_text = "N/A"
   808	
   809	        self.operational_events_applied_label.config(
   810	            text=str(applied) if applied is not None else "N/A"
   811	        )
   812	        self.operational_cancelled_ignored_label.config(
   813	            text=str(ignored) if ignored is not None else "N/A"
   814	        )
   815	        self.operational_status_label.config(text=status_text)
   816	
   817	    def _fetch_effective_structure_local(self, structure_id) -> Optional[Dict[str, Any]]:
   818	        """
   819	        Busca estado efetivo pela camada local já existente.
   820	
   821	        A UI atualmente não usa HTTP. Por isso este método usa diretamente
   822	        repositories/services com o mesmo app.db da UI.
   823	        Se a camada local não estiver disponível, falha silenciosamente
   824	        e mantém N/A na tela.
   825	        """
   826	        try:
   827	            sid = self._resolve_structure_key(structure_id)
   828	        except Exception:
   829	            return None
   830	
   831	        try:
   832	            from repositories.structures_repository import StructuresRepository
   833	            from repositories.structure_events_repository import (
   834	                StructureEventsRepository,
   835	            )
   836	            from services.structure_events_service import StructureEventsService
   837	
   838	            app_db_path = self._operational_app_db_path()
   839	            structures_repo = StructuresRepository(app_db_path)
   840	            events_repo = StructureEventsRepository(app_db_path)
   841	            events_service = StructureEventsService(
   842	                structure_events_repository=events_repo
   843	            )
   844	
   845	            structure = structures_repo.get_structure(sid)
   846	            if not structure:
   847	                return None
   848	
   849	            effective = events_service.apply_events_to_structure(structure)
   850	            return effective if isinstance(effective, dict) else None
   851	        except Exception:
   852	            return None
   853	
   854	    def _refresh_operational_state_for_structure(self, structure_id):
   855	        effective = self._fetch_effective_structure_local(structure_id)
   856	        if effective:
   857	            self.update_operational_state(effective)
   858	        else:
   859	            self._clear_operational_state()
   860	
   861	    # ------------------------------------------------------------------
   862	    # Helpers internos
   863	    # ------------------------------------------------------------------
   864	
   865	    def _format_currency_label(self, label: ttk.Label, value):
   866	        if value is None:
   867	            label.config(text="N/A")
   868	            return
   869	        try:
   870	            v = float(value)
   871	            formatted = (
   872	                f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
   873	            )
   874	            label.config(text=formatted)
   875	        except Exception:
   876	            label.config(text=str(value))
   877	
   878	    def _fetch_latest_decision_from_derived(
   879	        self, structure_id
   880	    ) -> Optional[Dict[str, Any]]:
   881	        """
   882	        alteracao_36: filtra por structure_id (INTEGER) em structure_decisions.
   883	        Legado aba removido.
   884	        """
   885	        sid = self._resolve_structure_key(structure_id)
   886	        db_path = self._derived_db_path()
   887	        con = sqlite3.connect(str(db_path))
   888	        con.row_factory = sqlite3.Row
   889	        cur = con.cursor()
   890	        try:
   891	            select_cols = [
   892	                "structure_id", "timestamp", "decision", "level",
   893	                "pl_atual", "pl_max", "pl_pct_of_max", "dte_min",
   894	                "spot_ref", "meta_json", "created_at", "why_json",
   895	            ]
   896	
   897	            row = cur.execute(
   898	                f"""
   899	                SELECT {", ".join(select_cols)}
   900	                FROM structure_decisions
   901	                WHERE structure_id = ?
   902	                ORDER BY COALESCE(created_at, timestamp) DESC
   903	                LIMIT 1
   904	                """,
   905	                (sid,),
   906	            ).fetchone()
   907	
   908	            if not row:
   909	                return None
   910	
   911	            d = dict(row)
   912	            if d.get("why_json") is not None:
   913	                d["why"] = d["why_json"]
   914	
   915	            d["spot_reference"] = d.pop("spot_ref", None)
   916	            return d
   917	        finally:
   918	            con.close()
   919	
   920	    def _fetch_payoff_points_from_derived(self, structure_id):
   921	        """
   922	        alteracao_36: filtra por structure_id (INTEGER) em payoff_curve_points.
   923	        Legado aba removido.
   924	        """
   925	        sid = self._resolve_structure_key(structure_id)
   926	        db_path = self._derived_db_path()
   927	        con = sqlite3.connect(str(db_path))
   928	        con.row_factory = sqlite3.Row
   929	        cur = con.cursor()
   930	        try:
   931	            rows = cur.execute(
   932	                """
   933	                SELECT point_spot, point_pl
   934	                FROM payoff_curve_points
   935	                WHERE structure_id = ?
   936	                ORDER BY point_spot ASC
   937	                """,
   938	                (sid,),
   939	            ).fetchall()
   940	            return [
   941	                (float(r["point_spot"]), float(r["point_pl"]))
   942	                for r in rows
   943	                if r["point_spot"] is not None and r["point_pl"] is not None
   944	            ]
   945	        finally:
   946	            con.close()
   947	
   948	    def _fetch_audit_info_from_derived(self, structure_id) -> Dict[str, Any]:
   949	        """
   950	        alteracao_36: filtra por structure_id (INTEGER).
   951	        Legado aba removido.
   952	        """
   953	        sid = self._resolve_structure_key(structure_id)
   954	        db_path = self._derived_db_path()
   955	        con = sqlite3.connect(str(db_path))
   956	        con.row_factory = sqlite3.Row
   957	        cur = con.cursor()
   958	        try:
   959	            row = cur.execute(
   960	                """
   961	                SELECT created_at, timestamp
   962	                FROM structure_decisions
   963	                WHERE structure_id = ?
   964	                ORDER BY COALESCE(created_at, timestamp) DESC
   965	                LIMIT 1
   966	                """,
   967	                (sid,),
   968	            ).fetchone()
   969	
   970	            created_at = None
   971	            if row:
   972	                created_at = row["created_at"] or row["timestamp"]
   973	
   974	            n_points = cur.execute(
   975	                "SELECT COUNT(*) AS n FROM payoff_curve_points WHERE structure_id = ?",
   976	                (sid,),
   977	            ).fetchone()["n"]
   978	
   979	            return {
   980	                "source_table": "derived.db:structure_decisions / payoff_curve_points",
   981	                "created_at": created_at,
   982	                "count_points": n_points,
   983	                "fallback": False,
   984	            }
   985	        finally:
   986	            con.close()
   987	
   988	    def _compute_breakevens_from_points(self, pts):
   989	        if not pts or len(pts) < 2:
   990	            return []
   991	        breakevens = []
   992	        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
   993	            if y1 == 0.0:
   994	                breakevens.append(x1)
   995	                continue
   996	            if y2 == 0.0:
   997	                breakevens.append(x2)
   998	                continue
   999	            if (y1 < 0.0 and y2 > 0.0) or (y1 > 0.0 and y2 < 0.0):
  1000	                if x2 != x1:
  1001	                    x0 = x1 + (0.0 - y1) * (x2 - x1) / (y2 - y1)
  1002	                    breakevens.append(x0)
  1003	        out: list = []
  1004	        for be in sorted(breakevens):
  1005	            if not out or abs(be - out[-1]) > 1e-6:
  1006	                out.append(be)
  1007	        return out
  1008	
  1009	    def _compute_pl_at_spot(self, pts, spot_ref: Optional[float]) -> Optional[float]:
  1010	        if spot_ref is None or not pts or len(pts) < 2:
  1011	            return None
  1012	        x = float(spot_ref)
  1013	        if x < pts[0][0] or x > pts[-1][0]:
  1014	            return None
  1015	        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
  1016	            if x1 <= x <= x2:
  1017	                if x2 == x1:
  1018	                    return y1
  1019	                t = (x - x1) / (x2 - x1)
  1020	                return y1 + t * (y2 - y1)
  1021	        return None
  1022	
  1023	    def _refresh_current_from_derived(self, structure_id):
  1024	        """Recarrega somente a estrutura atual do derived.db e atualiza widgets."""
  1025	        decision = self._fetch_latest_decision_from_derived(structure_id)
  1026	        if decision:
  1027	            self.update_decision(decision)
  1028	
  1029	        pts = self._fetch_payoff_points_from_derived(structure_id)
  1030	        breakevens = self._compute_breakevens_from_points(pts)
  1031	
  1032	        spot_ref = None
  1033	        if decision:
  1034	            spot_ref = decision.get("spot_reference")
  1035	
  1036	        pl_at_spot = self._compute_pl_at_spot(pts, spot_ref)
  1037	        self.update_breakevens(breakevens, pl_at_spot)
  1038	
  1039	        audit = self._fetch_audit_info_from_derived(structure_id)
  1040	        self.update_audit_info(audit)
  1041	
  1042	    # ------------------------------------------------------------------
  1043	    # Recalc click
  1044	    # ------------------------------------------------------------------
  1045	
  1046	    def _on_recalculate_click(self):
  1047	        decision = self._current_decision
  1048	        if not decision:
  1049	            self.lbl_recalc_status.config(
  1050	                text="Nenhuma decisão selecionada", foreground="red"
  1051	            )
  1052	            return
  1053	
  1054	        # alteracao_36: structure_id é único identificador
  1055	        structure_id = decision.get("structure_id")
  1056	        if not structure_id:
  1057	            self.lbl_recalc_status.config(
  1058	                text="Estrutura não identificada", foreground="red"
  1059	            )
  1060	            return
  1061	
  1062	        if getattr(self, "_recalc_in_progress", False):
  1063	            self._set_recalc_ui_state(
  1064	                True,
  1065	                msg=f"Recalc já em andamento ({structure_id})",
  1066	                color="orange",
  1067	            )
  1068	            return
  1069	
  1070	        # Botão manual: deve recalcular sempre que o usuário clicar.
  1071	        # A assinatura é mantida apenas para diagnóstico/estado, não para bloquear.
  1072	        sig = self._compute_recalc_signature(structure_id)
  1073	
  1074	        if callable(getattr(self, "_on_recalculate_cb", None)):
  1075	            self._set_recalc_ui_state(
  1076	                True,
  1077	                msg=f"Recalculando {structure_id}...",
  1078	                color="blue",
  1079	            )
  1080	            try:
  1081	                self._on_recalculate_cb(structure_id)
  1082	                self._last_recalc_signature = sig
  1083	            except Exception as e:
  1084	                self._set_recalc_ui_state(
  1085	                    False, msg="Erro ao iniciar recálculo", color="red"
  1086	                )
  1087	                print(f"[UI] Erro delegando recalc: {e}")
  1088	            return
  1089	
  1090	        self.lbl_recalc_status.config(
  1091	            text="Recalc indisponível: callback não configurado",
  1092	            foreground="red",
  1093	        )
```

## FILE: UI/components/decisions_grid.py
```python
     1	# UI/components/decisions_grid.py
     2	from src.domain.refs.structure_ref import StructureRef
     3	import tkinter as tk
     4	from tkinter import ttk
     5	from typing import Dict, List, Optional, Callable
     6	import json
     7	
     8	
     9	class DecisionsGrid(ttk.LabelFrame):
    10	    def __init__(
    11	        self,
    12	        parent,
    13	        on_selection_change: Callable[[Optional[Dict]], None],
    14	    ):
    15	        super().__init__(parent, text="Decisões", padding=5)
    16	
    17	        self.on_selection_change = on_selection_change
    18	        self.current_data: List[Dict] = []
    19	
    20	        self._setup_treeview()
    21	        self._setup_scrollbars()
    22	
    23	    def _setup_treeview(self):
    24	        columns = (
    25	            "timestamp",
    26	            "structure_id",
    27	            "decision",
    28	            "level",
    29	            "ratio",
    30	            "dte",
    31	            "pl_atual",
    32	            "pl_max",
    33	        )
    34	
    35	        self.tree = ttk.Treeview(
    36	            self,
    37	            columns=columns,
    38	            show="headings",
    39	            height=12,
    40	        )
    41	
    42	        # Cabeçalhos
    43	        self.tree.heading("timestamp", text="Data/Hora")
    44	        self.tree.heading("structure_id", text="Estrutura")
    45	        self.tree.heading("decision", text="Decisão")
    46	        self.tree.heading("level", text="Nível")
    47	        self.tree.heading("ratio", text="Ratio %")
    48	        self.tree.heading("dte", text="DTE")
    49	        self.tree.heading("pl_atual", text="PL Atual")
    50	        self.tree.heading("pl_max", text="PL Máx")
    51	
    52	        # Larguras
    53	        self.tree.column("timestamp", width=140, anchor="center")
    54	        self.tree.column("structure_id", width=100, anchor="center")
    55	        self.tree.column("decision", width=100, anchor="center")
    56	        self.tree.column("level", width=50, anchor="center")
    57	        self.tree.column("ratio", width=80, anchor="center")
    58	        self.tree.column("dte", width=50, anchor="center")
    59	        self.tree.column("pl_atual", width=80, anchor="e")
    60	        self.tree.column("pl_max", width=80, anchor="e")
    61	
    62	        # Evento de seleção
    63	        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)
    64	
    65	        # Tags de cor por decisão
    66	        self.tree.tag_configure("HOLD", background="#e8f5e8")
    67	        self.tree.tag_configure("PREPARE_ROLL", background="#fff3cd")
    68	        self.tree.tag_configure("CLOSE_REOPEN", background="#f8d7da")
    69	        self.tree.tag_configure("ROLL", background="#d1ecf1")
    70	        self.tree.tag_configure("ENTER", background="#d4edda")
    71	
    72	    def _setup_scrollbars(self):
    73	        v_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
    74	        self.tree.configure(yscrollcommand=v_scrollbar.set)
    75	
    76	        h_scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
    77	        self.tree.configure(xscrollcommand=h_scrollbar.set)
    78	
    79	        self.tree.grid(row=0, column=0, sticky="nsew")
    80	        v_scrollbar.grid(row=0, column=1, sticky="ns")
    81	        h_scrollbar.grid(row=1, column=0, sticky="ew")
    82	
    83	        self.grid_rowconfigure(0, weight=1)
    84	        self.grid_columnconfigure(0, weight=1)
    85	
    86	    def _on_tree_select(self, event):
    87	        selection = self.tree.selection()
    88	        if not selection:
    89	            self.on_selection_change(None)
    90	            return
    91	
    92	        item_id = selection[0]
    93	        try:
    94	            index = int(item_id) - 1
    95	            if 0 <= index < len(self.current_data):
    96	                self.on_selection_change(self.current_data[index])
    97	        except (ValueError, IndexError):
    98	            self.on_selection_change(None)
    99	
   100	    def update_data(self, decisions: List[Dict]):
   101	        """Atualiza grid com nova lista de decisões."""
   102	        self.current_data = decisions.copy()
   103	
   104	        for item in self.tree.get_children():
   105	            self.tree.delete(item)
   106	
   107	        for i, decision in enumerate(decisions, 1):
   108	            timestamp = self._format_timestamp(decision.get("timestamp"))
   109	            # Exibe structure_id; fallback para aba (compat)
   110	            structure_id = (
   111	                decision.get("structure_id") or decision.get("aba") or "N/A"
   112	            )
   113	            decision_text = decision.get("decision", "N/A")
   114	            level = decision.get("level", "")
   115	            ratio = self._format_ratio(decision.get("pl_pct_of_max"))
   116	            dte = decision.get("dte_min", "")
   117	            pl_atual = self._format_currency(decision.get("pl_atual"))
   118	            pl_max = self._format_currency(decision.get("pl_max"))
   119	
   120	            tag = (
   121	                decision_text
   122	                if decision_text in ["HOLD", "PREPARE_ROLL", "CLOSE_REOPEN", "ROLL", "ENTER"]
   123	                else ""
   124	            )
   125	
   126	            self.tree.insert(
   127	                "",
   128	                "end",
   129	                iid=str(i),
   130	                values=(
   131	                    timestamp,
   132	                    structure_id,
   133	                    decision_text,
   134	                    level,
   135	                    ratio,
   136	                    dte,
   137	                    pl_atual,
   138	                    pl_max,
   139	                ),
   140	                tags=(tag,),
   141	            )
   142	
   143	    def _format_timestamp(self, timestamp_str: Optional[str]) -> str:
   144	        if not timestamp_str:
   145	            return "N/A"
   146	        try:
   147	            for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
   148	                try:
   149	                    from datetime import datetime
   150	                    dt = datetime.strptime(timestamp_str, fmt)
   151	                    return dt.strftime("%d/%m/%Y %H:%M")
   152	                except ValueError:
   153	                    continue
   154	            return timestamp_str[:16] if len(timestamp_str) > 16 else timestamp_str
   155	        except Exception:
   156	            return "N/A"
   157	
   158	    def _format_ratio(self, ratio: Optional[float]) -> str:
   159	        if ratio is None:
   160	            return "N/A"
   161	        try:
   162	            return f"{ratio * 100:.1f}%"
   163	        except (TypeError, ValueError):
   164	            return "N/A"
   165	
   166	    def _format_currency(self, value: Optional[float]) -> str:
   167	        if value is None:
   168	            return "N/A"
   169	        try:
   170	            if abs(value) >= 1000:
   171	                return f"{value:,.0f}".replace(",", ".")
   172	            else:
   173	                return f"{value:.1f}"
   174	        except (TypeError, ValueError):
   175	            return "N/A"
   176	
   177	    def get_current_data(self) -> List[Dict]:
   178	        """Retorna dados atualmente exibidos (para export)."""
   179	        return self.current_data.copy()
   180	
   181	    def get_selected_decision(self) -> Optional[Dict]:
   182	        """Retorna decisão atualmente selecionada."""
   183	        selection = self.tree.selection()
   184	        if not selection:
   185	            return None
   186	        try:
   187	            index = int(selection[0]) - 1
   188	            if 0 <= index < len(self.current_data):
   189	                return self.current_data[index]
   190	        except (ValueError, IndexError):
   191	            pass
   192	        return None
   193	
   194	    def select_by_key(self, structure_id: str, timestamp: str) -> bool:
   195	        """
   196	        Seleciona a linha cujo (structure_id, timestamp) bate no dataset.
   197	        Aceita tanto 'structure_id' quanto 'aba' nos dicts (compat).
   198	        Retorna True se encontrou.
   199	        """
   200	        if not structure_id or not timestamp:
   201	            return False
   202	
   203	        for idx, row in enumerate(self.current_data):
   204	            row_sid = row.get("structure_id") or row.get("aba")
   205	            if row_sid == structure_id and row.get("timestamp") == timestamp:
   206	                iid = str(idx + 1)
   207	                try:
   208	                    self.tree.selection_set(iid)
   209	                    self.tree.focus(iid)
   210	                    self.tree.see(iid)
   211	                    self.tree.focus_set()
   212	                    return True
   213	                except Exception:
   214	                    return False
   215	        return False
```

## FILE: UI/components/payoff_chart.py
```python
     1	# UI/components/payoff_chart.py
     2	from src.domain.refs.structure_ref import StructureRef
     3	from matplotlib.ticker import FuncFormatter
     4	import json
     5	from matplotlib.figure import Figure
     6	from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
     7	import tkinter as tk
     8	from UI.debug_utils import payoff_debug, payoff_info
     9	from tkinter import filedialog, messagebox
    10	from tkinter import ttk
    11	from typing import List, Dict, Optional, Tuple
    12	
    13	import matplotlib
    14	matplotlib.use("TkAgg")  # necessário para renderizar no Tkinter
    15	
    16	
    17	# ---------------------------------------------------------------------------
    18	# Helpers de formatação pt-BR
    19	# ---------------------------------------------------------------------------
    20	
    21	def _fmt_number_br(x: float, decimals: int = 2) -> str:
    22	    """Formata número no padrão pt-BR: milhar '.' e decimal ','."""
    23	    try:
    24	        s = f"{float(x):,.{decimals}f}"
    25	        return s.replace(",", "X").replace(".", ",").replace("X", ".")
    26	    except Exception:
    27	        return str(x)
    28	
    29	
    30	def _fmt_currency_br(x: float, decimals: int = 2) -> str:
    31	    return f"R$ {_fmt_number_br(x, decimals=decimals)}"
    32	
    33	
    34	def _brl_abbrev(x, pos=None) -> str:
    35	    """Formata eixo Y com abreviações k/M/B para legibilidade."""
    36	    try:
    37	        x = float(x)
    38	    except Exception:
    39	        return "R$ 0"
    40	    ax = abs(x)
    41	    sign = "-" if x < 0 else ""
    42	    if ax >= 1_000_000_000:
    43	        return f"{sign}R$ {ax / 1_000_000_000:.1f}B"
    44	    if ax >= 1_000_000:
    45	        return f"{sign}R$ {ax / 1_000_000:.1f}M"
    46	    if ax >= 1_000:
    47	        return f"{sign}R$ {ax / 1_000:.0f}k"
    48	    return f"{sign}R$ {ax:.0f}"
    49	
    50	
    51	# ---------------------------------------------------------------------------
    52	# Classe principal
    53	# ---------------------------------------------------------------------------
    54	
    55	class PayoffChart(ttk.Frame):
    56	
    57	    # ------------------------------------------------------------------
    58	    # Inicialização
    59	    # ------------------------------------------------------------------
    60	
    61	    def __init__(self, parent):
    62	        super().__init__(parent, padding=6)
    63	        self._last_breakevens: List[float] = []
    64	        self._last_pl_at_spot_ref: Optional[float] = None
    65	        self._last_points: List[Dict] = []
    66	        self._last_decision_data: Dict = {}
    67	        # Comparação: overlay de curvas {"points": [...], "label": "...", "color": "..."}
    68	        self._fixed_curve: Optional[Dict] = None
    69	        self._build_canvas()
    70	
    71	    # ------------------------------------------------------------------
    72	    # Canvas / toolbar
    73	    # ------------------------------------------------------------------
    74	
    75	    def _build_canvas(self):
    76	        # Barra superior: toolbar matplotlib + botões de ação
    77	        top = ttk.Frame(self)
    78	        top.pack(fill="x", side="top")
    79	
    80	        self.btn_export = ttk.Button(
    81	            top, text="Exportar PNG", command=self.export_png
    82	        )
    83	        self.btn_export.pack(side="right", padx=(6, 0))
    84	
    85	        self.btn_fix_curve = ttk.Button(
    86	            top, text="Fixar Curva A", command=self.fix_current_curve
    87	        )
    88	        self.btn_fix_curve.pack(side="right", padx=(0, 6))
    89	
    90	        self.btn_clear_comparison = ttk.Button(
    91	            top, text="Limpar Comparação", command=self.clear_comparison
    92	        )
    93	        self.btn_clear_comparison.pack(side="right", padx=(0, 6))
    94	
    95	        # Figure / canvas matplotlib
    96	        self.fig = Figure(figsize=(5, 4), dpi=100)
    97	        self.ax = self.fig.add_subplot(111)
    98	
    99	        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
   100	        self.canvas.get_tk_widget().pack(fill="both", expand=True)
   101	
   102	        # Toolbar do matplotlib (fica na barra superior)
   103	        self.toolbar = NavigationToolbar2Tk(self.canvas, top, pack_toolbar=False)
   104	        self.toolbar.update()
   105	        self.toolbar.pack(side="left", fill="x", expand=True)
   106	
   107	        self._reset_axes()
   108	        self._safe_draw_idle()
   109	
   110	        # Forçar redraw quando o widget é exibido/redimensionado
   111	        self.bind("<Configure>", self._on_configure, add=True)
   112	
   113	    def _on_configure(self, event=None):
   114	        try:
   115	            w = int(self.winfo_width())
   116	            h = int(self.winfo_height())
   117	        except Exception:
   118	            return
   119	        if w <= 50 or h <= 50:
   120	            return
   121	        try:
   122	            if hasattr(self, "toolbar"):
   123	                self.toolbar.update()
   124	        except Exception:
   125	            pass
   126	        self._safe_draw_idle()
   127	
   128	    def _safe_draw_idle(self):
   129	        """Agenda draw_idle na thread do Tk."""
   130	        try:
   131	            self.after(0, self.canvas.draw_idle)
   132	        except Exception:
   133	            pass
   134	
   135	    # ------------------------------------------------------------------
   136	    # Eixos
   137	    # ------------------------------------------------------------------
   138	
   139	    def _reset_axes(self):
   140	        self.ax.clear()
   141	        self.ax.grid(True, alpha=0.3)
   142	        self.ax.set_xlabel("Spot")
   143	        self.ax.set_ylabel("PL")
   144	        self.ax.set_title("Curva de Payoff")
   145	
   146	        self.ax.xaxis.set_major_formatter(
   147	            FuncFormatter(lambda v, pos: _fmt_number_br(v, 2))
   148	        )
   149	        self.ax.yaxis.set_major_formatter(
   150	            FuncFormatter(
   151	                lambda v, pos: _fmt_currency_br(v, 0 if abs(v) >= 1000 else 2)
   152	            )
   153	        )
   154	
   155	    # ------------------------------------------------------------------
   156	    # API pública
   157	    # ------------------------------------------------------------------
   158	
   159	    def clear(self):
   160	        """Limpa o gráfico e reseta estado interno."""
   161	        self._last_breakevens = []
   162	        self._last_pl_at_spot_ref = None
   163	        self._last_points = []
   164	        self._last_decision_data = {}
   165	        self._reset_axes()
   166	        self._safe_draw_idle()
   167	
   168	    def update_chart(
   169	        self,
   170	        payoff_points: List[Dict],
   171	        decision_data: Optional[Dict] = None,
   172	    ) -> Dict:
   173	        """
   174	        Atualiza a curva principal.
   175	        Preserva pontos para comparação e redesenha com overlay se houver.
   176	        Retorna dict com breakevens e pl_at_spot_ref.
   177	        """
   178	        self._last_points = list(payoff_points) if payoff_points else []
   179	        self._last_decision_data = dict(decision_data) if decision_data else {}
   180	
   181	        return self._draw_curves_and_overlays(
   182	            payoff_points, decision_data, overlay_curve=self._fixed_curve
   183	        )
   184	
   185	    def fix_current_curve(self):
   186	        """Fixa a curva atual como Curva A para comparação."""
   187	        payoff_debug("FIX clicked -- id=", id(self))
   188	
   189	        if not self._last_points:
   190	            self._fixed_curve = None
   191	            return
   192	
   193	        points = []
   194	        for p in self._last_points:
   195	            try:
   196	                x, y = self._extract_xy(p)
   197	                if x is None or y is None:
   198	                    continue
   199	                points.append({"spot": float(x), "pl": float(y)})
   200	            except Exception:
   201	                continue
   202	
   203	        if len(points) < 2:
   204	            self._fixed_curve = None
   205	            return
   206	
   207	        self._fixed_curve = {
   208	            "label": "Curva A (fixada)",
   209	            "color": "red",
   210	            "points": points,
   211	        }
   212	        self._redraw_current()
   213	
   214	    def clear_comparison(self):
   215	        """Remove a curva fixada."""
   216	        payoff_debug("CLEAR comparison -- id=", id(self))
   217	        self._fixed_curve = None
   218	        if self._last_points:
   219	            self._redraw_current()
   220	
   221	    def export_png(self):
   222	        """Exporta o gráfico atual para PNG."""
   223	        file_path = filedialog.asksaveasfilename(
   224	            defaultextension=".png",
   225	            filetypes=[("PNG", "*.png"), ("All files", "*.*")],
   226	            title="Exportar gráfico como PNG",
   227	        )
   228	        if not file_path:
   229	            return
   230	        try:
   231	            self.fig.savefig(file_path, dpi=150, bbox_inches="tight")
   232	            messagebox.showinfo("Sucesso", f"Gráfico salvo em {file_path}")
   233	        except Exception as e:
   234	            messagebox.showerror("Erro", f"Erro ao salvar: {e}")
   235	
   236	    def get_last_overlays(self) -> Dict:
   237	        """Para integração com DetailsPanel: breakevens e PL interpolado no spot_ref."""
   238	        return {
   239	            "breakevens": list(self._last_breakevens),
   240	            "pl_at_spot_ref": self._last_pl_at_spot_ref,
   241	        }
   242	
   243	    # ------------------------------------------------------------------
   244	    # Redesenho interno
   245	    # ------------------------------------------------------------------
   246	
   247	    def _redraw_current(self):
   248	        """Redesenha com os dados salvos em _last_points/_last_decision_data."""
   249	        if self._last_points:
   250	            self._draw_curves_and_overlays(
   251	                self._last_points,
   252	                self._last_decision_data or {},
   253	                overlay_curve=self._fixed_curve,
   254	            )
   255	
   256	    def _draw_curves_and_overlays(
   257	        self,
   258	        payoff_points: List[Dict],
   259	        decision_data: Optional[Dict],
   260	        overlay_curve: Optional[Dict],
   261	    ) -> Dict:
   262	        """
   263	        Núcleo de renderização: curva principal + overlay (Curva A) +
   264	        breakevens + spot_ref.
   265	        """
   266	        self._reset_axes()
   267	
   268	        if not payoff_points:
   269	            self.ax.set_title("Sem dados de payoff")
   270	            self._safe_draw_idle()
   271	            self._last_breakevens = []
   272	            self._last_pl_at_spot_ref = None
   273	            return self.get_last_overlays()
   274	
   275	        # ------------------------------------------------------------------
   276	        # Extrair xs / ys da curva principal
   277	        # ------------------------------------------------------------------
   278	        xs: List[float] = []
   279	        ys: List[float] = []
   280	
   281	        for p in payoff_points:
   282	            x, y = self._extract_xy(p)
   283	            try:
   284	                xs.append(float(x))
   285	                ys.append(float(y))
   286	            except Exception:
   287	                continue
   288	
   289	        if not xs:
   290	            payoff_info("ERROR: não consegui extrair xs/ys de payoff_points.")
   291	            self.ax.set_title("Sem dados de payoff")
   292	            self._safe_draw_idle()
   293	            self._last_breakevens = []
   294	            self._last_pl_at_spot_ref = None
   295	            return self.get_last_overlays()
   296	
   297	        payoff_debug(
   298	            f"rebuilt xs: min={min(xs):.2f}, max={max(xs):.2f}, len={len(xs)}"
   299	        )
   300	        payoff_debug(
   301	            f"rebuilt ys: min={min(ys):.6f}, max={max(ys):.6f}, len={len(ys)}"
   302	        )
   303	
   304	        # ------------------------------------------------------------------
   305	        # Label da curva principal (B quando há overlay, senão "Payoff")
   306	        # ------------------------------------------------------------------
   307	        if overlay_curve and decision_data:
   308	            sid = (
   309	                decision_data.get("structure_id")
   310	                or decision_data.get("aba", "")
   311	            )
   312	            main_label = f"B: {sid}"
   313	        else:
   314	            main_label = "Payoff"
   315	
   316	        self.ax.plot(xs, ys, color="#1f77b4", linewidth=2, label=main_label)
   317	
   318	        # ------------------------------------------------------------------
   319	        # Curva A (overlay fixado)
   320	        # ------------------------------------------------------------------
   321	        if overlay_curve:
   322	            overlay_xs: List[float] = []
   323	            overlay_ys: List[float] = []
   324	            for point in overlay_curve["points"]:
   325	                try:
   326	                    x, y = self._extract_xy(point)
   327	                    overlay_xs.append(float(x))
   328	                    overlay_ys.append(float(y))
   329	                except Exception:
   330	                    continue
   331	            if overlay_xs:
   332	                self.ax.plot(
   333	                    overlay_xs,
   334	                    overlay_ys,
   335	                    color=overlay_curve["color"],
   336	                    linewidth=2,
   337	                    linestyle="--",
   338	                    alpha=0.8,
   339	                    label=overlay_curve["label"],
   340	                )
   341	
   342	        # ------------------------------------------------------------------
   343	        # Linha PL = 0
   344	        # ------------------------------------------------------------------
   345	        self.ax.axhline(0, color="gray", linewidth=1, alpha=0.7)
   346	
   347	        # ------------------------------------------------------------------
   348	        # Spot Ref
   349	        # ------------------------------------------------------------------
   350	        spot_ref: Optional[float] = None
   351	        if decision_data:
   352	            raw = decision_data.get("spot_ref") or decision_data.get("spot_reference")
   353	            try:
   354	                spot_ref = float(raw) if raw is not None else None
   355	            except Exception:
   356	                spot_ref = None
   357	
   358	        if spot_ref is not None:
   359	            self.ax.axvline(
   360	                spot_ref,
   361	                color="#ff7f0e",
   362	                linestyle="--",
   363	                linewidth=1.5,
   364	                label="Spot Ref",
   365	            )
   366	            pl_ref = self._interp_y_at_x(xs, ys, spot_ref)
   367	            self._last_pl_at_spot_ref = pl_ref
   368	            if pl_ref is not None:
   369	                self.ax.scatter([spot_ref], [pl_ref], s=45, color="#ff7f0e", zorder=5)
   370	                self.ax.annotate(
   371	                    f"Spot Ref: {_fmt_number_br(spot_ref, 2)}\n"
   372	                    f"PL: {_fmt_currency_br(pl_ref, 2)}",
   373	                    xy=(spot_ref, pl_ref),
   374	                    xytext=(8, 8),
   375	                    textcoords="offset points",
   376	                    fontsize=8,
   377	                    color="#ff7f0e",
   378	                    bbox=dict(
   379	                        boxstyle="round,pad=0.2",
   380	                        fc="white",
   381	                        ec="#ff7f0e",
   382	                        alpha=0.8,
   383	                    ),
   384	                )
   385	        else:
   386	            self._last_pl_at_spot_ref = None
   387	
   388	        # ------------------------------------------------------------------
   389	        # Breakevens (só da curva principal)
   390	        # ------------------------------------------------------------------
   391	        bks = self._find_breakevens(xs, ys)
   392	        self._last_breakevens = bks
   393	
   394	        for bx in bks:
   395	            self.ax.axvline(bx, color="green", linestyle=":", linewidth=1, alpha=0.85)
   396	            self.ax.scatter([bx], [0], s=30, color="green", zorder=6)
   397	            self.ax.annotate(
   398	                f"BE {_fmt_number_br(bx, 2)}",
   399	                xy=(bx, 0),
   400	                xytext=(0, 10),
   401	                textcoords="offset points",
   402	                ha="center",
   403	                fontsize=8,
   404	                color="green",
   405	                bbox=dict(
   406	                    boxstyle="round,pad=0.15",
   407	                    fc="white",
   408	                    ec="green",
   409	                    alpha=0.75,
   410	                ),
   411	            )
   412	
   413	        # ------------------------------------------------------------------
   414	        # Título
   415	        # ------------------------------------------------------------------
   416	        if decision_data:
   417	            sid = (
   418	                decision_data.get("structure_id")
   419	                or decision_data.get("aba", "")
   420	            )
   421	            dec = decision_data.get("decision", "")
   422	            title = f"Payoff -- {sid} [{dec}]"
   423	            if overlay_curve:
   424	                title += f" vs {overlay_curve['label']}"
   425	        elif overlay_curve:
   426	            title = "Curva de Payoff -- Comparação"
   427	        else:
   428	            title = "Curva de Payoff"
   429	
   430	        self.ax.set_title(title)
   431	        self.ax.legend(loc="best")
   432	        self._safe_draw_idle()
   433	        return self.get_last_overlays()
   434	
   435	    # ------------------------------------------------------------------
   436	    # Utilitários de extração e interpolação
   437	    # ------------------------------------------------------------------
   438	
   439	    def _extract_xy(self, p) -> Tuple[Optional[float], Optional[float]]:
   440	        """
   441	        Extrai (x, y) de múltiplos formatos:
   442	        - tuple/list   (p[0], p[1])
   443	        - dict         chaves canônicas e alternativas
   444	        - sqlite Row   idem via indexação
   445	        """
   446	        if isinstance(p, (tuple, list)) and len(p) >= 2:
   447	            return p[0], p[1]
   448	
   449	        x = self._get_field(
   450	            p, ["point_spot", "spot", "x", "underlying", "price", "underlying_spot"]
   451	        )
   452	        y = self._get_field(
   453	            p, ["point_pl", "pl", "y", "pnl", "payoff", "profit_loss", "pl_value"]
   454	        )
   455	        return x, y
   456	
   457	    def _get_field(self, obj, keys: List[str], default=None):
   458	        """Tenta extrair campo de dict, Mapping ou objeto com atributo."""
   459	        if isinstance(obj, dict):
   460	            for k in keys:
   461	                if k in obj:
   462	                    return obj[k]
   463	        for k in keys:
   464	            try:
   465	                return obj[k]
   466	            except Exception:
   467	                pass
   468	        for k in keys:
   469	            try:
   470	                if hasattr(obj, k):
   471	                    return getattr(obj, k)
   472	            except Exception:
   473	                pass
   474	        return default
   475	
   476	    @staticmethod
   477	    def _find_breakevens(spots: List[float], pls: List[float]) -> List[float]:
   478	        """Retorna lista de spots onde PL cruza zero (interpolação linear)."""
   479	        bks: List[float] = []
   480	        if not spots or not pls or len(spots) != len(pls):
   481	            return bks
   482	
   483	        for i in range(len(spots) - 1):
   484	            x0, y0 = spots[i], pls[i]
   485	            x1, y1 = spots[i + 1], pls[i + 1]
   486	
   487	            if y0 == 0:
   488	                bks.append(float(x0))
   489	                continue
   490	
   491	            crosses = (y0 < 0 and y1 > 0) or (y0 > 0 and y1 < 0) or (y1 == 0)
   492	            if crosses:
   493	                if y1 == y0:
   494	                    continue
   495	                xz = x0 + (-y0) * (x1 - x0) / (y1 - y0)
   496	                bks.append(float(xz))
   497	
   498	        # Deduplicar e ordenar
   499	        out: List[float] = []
   500	        for x in sorted(bks):
   501	            if not out or abs(x - out[-1]) > 1e-9:
   502	                out.append(x)
   503	        return out
   504	
   505	    @staticmethod
   506	    def _interp_y_at_x(
   507	        xs: List[float], ys: List[float], x: float
   508	    ) -> Optional[float]:
   509	        """Interpolação linear por segmento. Retorna None se fora do range."""
   510	        if not xs or not ys or len(xs) != len(ys):
   511	            return None
   512	        try:
   513	            x = float(x)
   514	        except Exception:
   515	            return None
   516	
   517	        for i in range(len(xs) - 1):
   518	            x0, x1 = xs[i], xs[i + 1]
   519	            y0, y1 = ys[i], ys[i + 1]
   520	            if x0 == x1:
   521	                continue
   522	            if (x0 <= x <= x1) or (x1 <= x <= x0):
   523	                t = (x - x0) / (x1 - x0)
   524	                try:
   525	                    return float(y0 + t * (y1 - y0))
   526	                except Exception:
   527	                    return None
   528	        return None
```

## FILE: UI/main_window.py
```python
     1	# UI/main_window.py
     2	#!/usr/bin/env python3
     3	"""
     4	UI Principal - Sistema de Derivados
     5	Carrega dados de derived.db e app.db para exibir decisões e payoffs
     6	"""
     7	from UI.models.ui_data import UIDataModel
     8	from UI.components.payoff_chart import PayoffChart
     9	from UI.components.details_panel import DetailsPanel
    10	from UI.components.decisions_grid import DecisionsGrid
    11	from UI.components.filters_panel import FiltersPanel
    12	from UI.components.structures_list_panel import StructuresListPanel
    13	from UI.components.structure_editor_dialog import StructureEditorDialog
    14	from datetime import datetime, timedelta
    15	from typing import Dict, List, Optional
    16	from UI.debug_utils import debug, info
    17	import tkinter as tk
    18	from tkinter import ttk, messagebox
    19	import matplotlib.pyplot as plt
    20	# FigureCanvasTkAgg importado lazily em _setup_chart para evitar side-effects no import
    21	from pathlib import Path
    22	import threading
    23	import time
    24	
    25	PROJECT_ROOT = Path(__file__).resolve().parents[1]
    26	
    27	class MainWindow:
    28	    def __init__(self):
    29	        self.root = tk.Tk()
    30	        self.root.title("Sistema de Derivados - Análise de Decisões")
    31	        self.root.geometry("1400x900")
    32	
    33	        # Data model
    34	        self.data_model = UIDataModel()
    35	
    36	        # Caminho canônico ao banco operacional (alteracao_70/71)
    37	        self._db_path = str(PROJECT_ROOT / "dados" / "app.db")
    38	
    39	        # Threading control: evitar freeze da UI
    40	        self._payoff_worker_id = 0
    41	
    42	        # Loading animation
    43	        self._loading_animation_active = False
    44	        self._loading_animation_chars = ["", "", "", "", "", "", "", "", "", ""]
    45	        self._loading_animation_index = 0
    46	        self._loading_payoff = False
    47	        self._stop_loading_animation()
    48	
    49	        # Última decisão selecionada (preservada entre refreshes)
    50	        self.last_selected_decision: Optional[Dict] = None
    51	
    52	        # Controle de recalc em andamento
    53	        self._recalc_in_progress = False
    54	
    55	        # Controle de atualização automática da UI/RTD.
    56	        # Este ciclo apenas recarrega dados já persistidos.
    57	        # Não executa pipeline e não recalcula payoff.
    58	        self._auto_refresh_interval_ms = 30000
    59	        self._auto_refresh_enabled = True
    60	        self._auto_refresh_in_progress = False
    61	        self._auto_refresh_after_id = None
    62	        self._closing = False
    63	
    64	        # Configurar layout principal
    65	        self._setup_layout()
    66	        self._setup_menus()
    67	        self._bind_events()
    68	
    69	        # Carregar dados iniciais
    70	        self.refresh_data()
    71	
    72	        # Iniciar atualização automática controlada.
    73	        self.start_auto_refresh()
    74	
    75	    def _setup_layout(self):
    76	        """Organiza layout em painéis."""
    77	        main_paned = ttk.PanedWindow(self.root, orient="horizontal")
    78	        main_paned.pack(fill="both", expand=True, padx=5, pady=5)
    79	
    80	        # Painel esquerdo: filtros + grid
    81	        left_frame = ttk.Frame(main_paned)
    82	        main_paned.add(left_frame, weight=1)
    83	
    84	        # Painel direito: notebook com abas
    85	        right_frame = ttk.Frame(main_paned)
    86	        main_paned.add(right_frame, weight=2)
    87	
    88	        # === PAINEL ESQUERDO ===
    89	        self.filters_panel = FiltersPanel(
    90	            parent=left_frame,
    91	            on_filter_change=self.on_filter_change,
    92	        )
    93	        self.filters_panel.pack(fill="x", padx=5, pady=5)
    94	
    95	        self.decisions_grid = DecisionsGrid(
    96	            parent=left_frame,
    97	            on_selection_change=self.on_decision_selected,
    98	        )
    99	        self.decisions_grid.pack(fill="both", expand=True, padx=5, pady=5)
   100	
   101	        # === PAINEL DIREITO ===
   102	        right_notebook = ttk.Notebook(right_frame)
   103	        right_notebook.pack(fill="both", expand=True, padx=5, pady=5)
   104	
   105	        # Aba 1: Detalhes da Decisão
   106	        details_frame = ttk.Frame(right_notebook)
   107	        right_notebook.add(details_frame, text="Detalhes da Decisão")
   108	
   109	        self.details_panel = DetailsPanel(
   110	            details_frame,
   111	            on_recalculate=self.recalculate_structure,
   112	            app_db_path=self._db_path,
   113	        )
   114	        self.details_panel.pack(fill="both", expand=True, padx=5, pady=5)
   115	
   116	        # Aba 2: Gráfico de Payoff
   117	        chart_frame = ttk.Frame(right_notebook)
   118	        right_notebook.add(chart_frame, text="Curva de Payoff")
   119	
   120	        self.payoff_chart = PayoffChart(chart_frame)
   121	        self.payoff_chart.pack(fill="both", expand=True, padx=5, pady=5)
   122	
   123	        # Aba 3: Estruturas (Fase 5 -- alteracao_10)
   124	        self._setup_structures_tab(right_notebook)
   125	
   126	        # Status bar
   127	        self.status_bar = ttk.Label(
   128	            self.root,
   129	            text="Pronto",
   130	            relief=tk.SUNKEN,
   131	            anchor="w",
   132	        )
   133	        self.status_bar.pack(side="bottom", fill="x")
   134	
   135	    def _setup_menus(self):
   136	        """Cria menu superior."""
   137	        menubar = tk.Menu(self.root)
   138	        self.root.config(menu=menubar)
   139	
   140	        # Menu Arquivo
   141	        file_menu = tk.Menu(menubar, tearoff=0)
   142	        menubar.add_cascade(label="Arquivo", menu=file_menu)
   143	        file_menu.add_command(label="Recarregar Tela", command=self.refresh_data)
   144	        file_menu.add_separator()
   145	        file_menu.add_command(label="Exportar CSV...", command=self.export_csv)
   146	        file_menu.add_separator()
   147	        file_menu.add_command(label="Sair", command=self.close)
   148	
   149	        # Menu Ferramentas
   150	        tools_menu = tk.Menu(menubar, tearoff=0)
   151	        menubar.add_cascade(label="Ferramentas", menu=tools_menu)
   152	        tools_menu.add_command(label="Executar Pipeline", command=self.run_pipeline)
   153	        tools_menu.add_command(label="Verificar Bancos", command=self.check_databases)
   154	        tools_menu.add_separator()
   155	        tools_menu.add_command(label="Limpar Cache", command=self.clear_cache)
   156	
   157	        # Menu Ajuda
   158	        help_menu = tk.Menu(menubar, tearoff=0)
   159	        menubar.add_cascade(label="Ajuda", menu=help_menu)
   160	        help_menu.add_command(label="Sobre", command=self.show_about)
   161	
   162	    def _bind_events(self):
   163	        """Vincula atalhos de teclado."""
   164	        self.root.bind("<F5>", lambda e: self.refresh_data())
   165	        self.root.bind("<Control-q>", lambda e: self.close())
   166	        self.root.protocol("WM_DELETE_WINDOW", self.close)
   167	
   168	    # ------------------------------------------------------------------
   169	    # Callbacks
   170	    # ------------------------------------------------------------------
   171	
   172	    def on_filter_change(self, filters: Dict):
   173	        """Callback quando filtros mudam."""
   174	        self.status_bar.config(text="Aplicando filtros...")
   175	        try:
   176	            filtered_data = self.data_model.get_decisions(filters)
   177	            self.decisions_grid.update_data(filtered_data)
   178	            count = len(filtered_data)
   179	            self.status_bar.config(text=f"{count} decisões encontradas")
   180	        except Exception as e:
   181	            messagebox.showerror("Erro", f"Erro ao aplicar filtros: {e}")
   182	            self.status_bar.config(text="Erro nos filtros")
   183	
   184	    def on_decision_selected(self, decision_data: Dict):
   185	        """Callback quando uma decisão é selecionada no grid.
   186	        alteracao_36: structure_id é suficiente para carregar payoff -- timestamp não é obrigatório.
   187	        """
   188	        if not decision_data:
   189	            return
   190	
   191	        self.last_selected_decision = dict(decision_data)
   192	
   193	        # Atualizar painel de detalhes (síncrono, leve)
   194	        try:
   195	            self.details_panel.update_decision(decision_data)
   196	        except Exception as e:
   197	            print(f"[UI] Erro ao atualizar detalhes: {e}")
   198	
   199	        # Carregar payoff em background -- apenas structure_id necessário
   200	        structure_id = decision_data.get("structure_id")
   201	        timestamp = decision_data.get("timestamp")  # opcional
   202	
   203	        if structure_id is not None:
   204	            self._start_payoff_load(structure_id, timestamp, decision_data)
   205	        else:
   206	            self.payoff_chart.clear()
   207	            self.status_bar.config(text="Dados insuficientes para payoff")
   208	
   209	    def _start_payoff_load(
   210	        self,
   211	        structure_id,
   212	        timestamp=None,       # alteracao_36: opcional
   213	        decision_data=None,   # alteracao_36: opcional
   214	    ):
   215	        """Inicia carregamento de payoff em thread separada.
   216	        alteracao_36: structure_id é a única chave obrigatória.
   217	        """
   218	        if decision_data is None:
   219	            decision_data = {"structure_id": structure_id}
   220	
   221	        self._payoff_worker_id += 1
   222	        current_worker_id = self._payoff_worker_id
   223	
   224	        if self._loading_payoff:
   225	            self.status_bar.config(text="Carregando payoff... (cancelando anterior)")
   226	        else:
   227	            self.status_bar.config(text="Carregando payoff...")
   228	
   229	        self._loading_payoff = True
   230	
   231	        def load_worker():
   232	            try:
   233	                points, info_dict = self.data_model.get_payoff_curve_info(
   234	                    structure_id, timestamp
   235	                )
   236	                try:
   237	                    debug(
   238	                        f"payoff structure_id={structure_id} ts_req={timestamp} "
   239	                        f"-> n={len(points or [])} info={info_dict}"
   240	                    )
   241	                except Exception:
   242	                    pass
   243	
   244	                # Normalizar formato de pontos para o chart
   245	                norm = []
   246	                for p in points or []:
   247	                    if isinstance(p, dict):
   248	                        if "spot" in p and "pl" in p:
   249	                            norm.append({"spot": p["spot"], "pl": p["pl"]})
   250	                        elif "point_spot" in p and "point_pl" in p:
   251	                            norm.append({"spot": p["point_spot"], "pl": p["point_pl"]})
   252	                        else:
   253	                            spot = p.get("x") if "x" in p else p.get("s")
   254	                            pl = p.get("y") if "y" in p else p.get("p")
   255	                            if spot is not None and pl is not None:
   256	                                norm.append({"spot": spot, "pl": pl})
   257	                    elif isinstance(p, (list, tuple)) and len(p) >= 2:
   258	                        norm.append({"spot": p[0], "pl": p[1]})
   259	                points = norm
   260	
   261	                if current_worker_id != self._payoff_worker_id:
   262	                    return
   263	
   264	                self.root.after(
   265	                    0,
   266	                    self._finish_payoff_load,
   267	                    points,
   268	                    info_dict,
   269	                    decision_data,
   270	                    current_worker_id,
   271	                )
   272	            except Exception as e:
   273	                if current_worker_id == self._payoff_worker_id:
   274	                    self.root.after(
   275	                        0,
   276	                        self._handle_payoff_error,
   277	                        str(e),
   278	                        current_worker_id,
   279	                    )
   280	
   281	        thread = threading.Thread(target=load_worker, daemon=True)
   282	        thread.start()
   283	
   284	    def refresh_data(self, show_errors: bool = True):
   285	        """Recarrega dados do banco.
   286	        alteracao_36: preserva seleção usando structure_id como chave -- timestamp é auxiliar.
   287	        """
   288	        self.status_bar.config(text="Carregando dados...")
   289	        try:
   290	            self.data_model.refresh()
   291	
   292	            try:
   293	                self.filters_panel.update_structures(
   294	                    self.data_model.get_structures()
   295	                )
   296	            except Exception:
   297	                pass
   298	
   299	            try:
   300	                self.filters_panel.reset_filters()
   301	            except Exception:
   302	                pass
   303	
   304	            decisions = self.data_model.get_decisions()
   305	            self.decisions_grid.update_data(decisions)
   306	
   307	            preserved = False
   308	            d = self.last_selected_decision
   309	
   310	            if d:
   311	                target_sid = d.get("structure_id")  # chave canônica
   312	                target_ts = d.get("timestamp")       # auxiliar
   313	
   314	                # Reselecionar na grid: structure_id é suficiente
   315	                if target_sid is not None:
   316	                    try:
   317	                        self.decisions_grid.select_by_key(target_sid, target_ts)
   318	                    except Exception:
   319	                        pass
   320	
   321	                    try:
   322	                        self.details_panel.update_decision(d)
   323	                    except Exception:
   324	                        pass
   325	
   326	                    try:
   327	                        self._start_payoff_load(target_sid, target_ts, d)
   328	                        preserved = True
   329	                    except Exception:
   330	                        preserved = False
   331	
   332	            if not preserved:
   333	                try:
   334	                    self.details_panel.clear()
   335	                except Exception:
   336	                    pass
   337	                try:
   338	                    self.payoff_chart.clear()
   339	                except Exception:
   340	                    pass
   341	
   342	            self.status_bar.config(
   343	                text=f"Dados atualizados - {len(decisions)} decisões"
   344	            )
   345	
   346	        except Exception as e:
   347	            if show_errors:
   348	                messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
   349	            else:
   350	                print(f"[UI] Erro na atualização automática: {e}")
   351	            self.status_bar.config(text="Erro ao carregar dados")
   352	
   353	    def close(self):
   354	        """Fecha a janela cancelando agendamentos automáticos pendentes."""
   355	        self._closing = True
   356	        self.stop_auto_refresh()
   357	        try:
   358	            self.root.quit()
   359	        except Exception:
   360	            pass
   361	
   362	    def start_auto_refresh(self):
   363	        """Inicia o ciclo de atualização automática da tela."""
   364	        self._auto_refresh_enabled = True
   365	        self._schedule_auto_refresh()
   366	
   367	    def stop_auto_refresh(self):
   368	        """Interrompe o ciclo de atualização automática da tela."""
   369	        self._auto_refresh_enabled = False
   370	        after_id = getattr(self, "_auto_refresh_after_id", None)
   371	        self._auto_refresh_after_id = None
   372	
   373	        if after_id is not None:
   374	            try:
   375	                self.root.after_cancel(after_id)
   376	            except Exception:
   377	                pass
   378	
   379	    def _schedule_auto_refresh(self):
   380	        """Agenda a próxima atualização automática, garantindo um único after."""
   381	        if (
   382	            not getattr(self, "_auto_refresh_enabled", False)
   383	            or getattr(self, "_closing", False)
   384	        ):
   385	            return
   386	
   387	        previous_after_id = getattr(self, "_auto_refresh_after_id", None)
   388	        if previous_after_id is not None:
   389	            try:
   390	                self.root.after_cancel(previous_after_id)
   391	            except Exception:
   392	                pass
   393	
   394	        self._auto_refresh_after_id = self.root.after(
   395	            self._auto_refresh_interval_ms,
   396	            self._auto_refresh_tick,
   397	        )
   398	
   399	    def _auto_refresh_tick(self):
   400	        """Executa uma atualização automática sem pipeline e sem recálculo."""
   401	        self._auto_refresh_after_id = None
   402	
   403	        if (
   404	            not getattr(self, "_auto_refresh_enabled", False)
   405	            or getattr(self, "_closing", False)
   406	        ):
   407	            return
   408	
   409	        if (
   410	            getattr(self, "_auto_refresh_in_progress", False)
   411	            or getattr(self, "_recalc_in_progress", False)
   412	        ):
   413	            self._schedule_auto_refresh()
   414	            return
   415	
   416	        self._auto_refresh_in_progress = True
   417	        try:
   418	            self.refresh_data(show_errors=False)
   419	            try:
   420	                self.status_bar.config(
   421	                    text=f"Dados atualizados automaticamente às {datetime.now():%H:%M:%S}"
   422	                )
   423	            except Exception:
   424	                pass
   425	        finally:
   426	            self._auto_refresh_in_progress = False
   427	            self._schedule_auto_refresh()
   428	
   429	    def export_csv(self):
   430	        """Exporta dados filtrados para CSV."""
   431	        from tkinter import filedialog
   432	
   433	        filename = filedialog.asksaveasfilename(
   434	            defaultextension=".csv",
   435	            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
   436	        )
   437	        if filename:
   438	            try:
   439	                current_data = self.decisions_grid.get_current_data()
   440	                self.data_model.export_to_csv(current_data, filename)
   441	                messagebox.showinfo("Sucesso", f"Dados exportados para {filename}")
   442	            except Exception as e:
   443	                messagebox.showerror("Erro", f"Erro ao exportar: {e}")
   444	
   445	    def recalculate_structure(self, structure_id: str):
   446	        """
   447	        Recalcula a estrutura identificada por structure_id e atualiza a UI.
   448	
   449	        Importante:
   450	        - Este botão NÃO executa o pipeline completo.
   451	        - Ele recalcula somente a estrutura selecionada via CanonicalPricingFacade.
   452	        """
   453	        if self._recalc_in_progress:
   454	            try:
   455	                self.status_bar.config(
   456	                    text=f"Recalc já em andamento; ignorando ({structure_id})"
   457	                )
   458	            except Exception:
   459	                pass
   460	            return
   461	
   462	        try:
   463	            sid = int(structure_id)
   464	        except (TypeError, ValueError):
   465	            try:
   466	                self.status_bar.config(
   467	                    text=f"structure_id inválido para recálculo: {structure_id}"
   468	                )
   469	            except Exception:
   470	                pass
   471	            return
   472	
   473	        self._recalc_in_progress = True
   474	
   475	        try:
   476	            self.payoff_chart.fix_current_curve()
   477	        except Exception:
   478	            pass
   479	
   480	        try:
   481	            self.status_bar.config(text=f"Recalculando estrutura {sid}...")
   482	        except Exception:
   483	            pass
   484	
   485	        def finish(ok: bool, msg: str):
   486	            self._recalc_in_progress = False
   487	
   488	            try:
   489	                self.status_bar.config(text=msg)
   490	            except Exception:
   491	                pass
   492	
   493	            try:
   494	                if hasattr(self, "details_panel") and hasattr(
   495	                    self.details_panel, "on_recalc_finished"
   496	                ):
   497	                    self.details_panel.on_recalc_finished(
   498	                        str(sid), ok=ok, message=msg
   499	                    )
   500	            except Exception as e:
   501	                print("[UI] Erro notificando details_panel fim recalc:", e)
   502	
   503	        def clear_ui_cache():
   504	            try:
   505	                if hasattr(self, "data_model") and hasattr(self.data_model, "clear_cache"):
   506	                    self.data_model.clear_cache()
   507	            except Exception as e:
   508	                print("[UI] Erro limpando cache após recalc:", e)
   509	
   510	        def worker():
   511	            try:
   512	                from services.canonical_pricing_facade import CanonicalPricingFacade
   513	
   514	                facade = CanonicalPricingFacade(db_path=self._db_path)
   515	                result = facade.execute_pricing(sid)
   516	
   517	                print(f"[UI] Recalc structure_id={sid} result:", result)
   518	
   519	                if not isinstance(result, dict):
   520	                    raise RuntimeError(f"Resposta inválida do pricing facade: {result!r}")
   521	
   522	                ok_statuses = {"success", "ok", "completed"}
   523	
   524	                top_status = result.get("status")
   525	                if top_status is not None and str(top_status).lower() not in ok_statuses:
   526	                    msg = (
   527	                        result.get("error_message")
   528	                        or result.get("message")
   529	                        or f"Falha no recálculo da estrutura {sid}: status={top_status}"
   530	                    )
   531	                    raise RuntimeError(msg)
   532	
   533	                inner = result.get("result")
   534	                if isinstance(inner, dict):
   535	                    inner_status = inner.get("status")
   536	                    if inner_status is not None and str(inner_status).lower() not in ok_statuses:
   537	                        msg = (
   538	                            inner.get("error_message")
   539	                            or inner.get("message")
   540	                            or f"Falha no recálculo da estrutura {sid}: status={inner_status}"
   541	                        )
   542	                        raise RuntimeError(msg)
   543	
   544	                self.root.after(0, clear_ui_cache)
   545	                self.root.after(0, self.refresh_data)
   546	                self.root.after(
   547	                    0,
   548	                    lambda: finish(True, f"OK: estrutura {sid} recalculada"),
   549	                )
   550	
   551	            except Exception as e:
   552	                print("[UI] Erro inesperado recalc:", e)
   553	                self.root.after(
   554	                    0,
   555	                    lambda: finish(False, f"Erro no recálculo da estrutura {sid}: {e}"),
   556	                )
   557	
   558	        threading.Thread(target=worker, daemon=True).start()
   559	
   560	
   561	    def _extract_pipeline_summary(self, stdout: str) -> Dict:
   562	        """Extrai o resumo JSON emitido por scripts/run_derived_pipeline.py."""
   563	        import json
   564	
   565	        marker = "[PIPELINE_SUMMARY_JSON]"
   566	        for line in reversed((stdout or "").splitlines()):
   567	            if marker in line:
   568	                payload = line.split(marker, 1)[1].strip()
   569	                try:
   570	                    data = json.loads(payload)
   571	                    return data if isinstance(data, dict) else {}
   572	                except Exception:
   573	                    return {}
   574	        return {}
   575	
   576	    def _format_pipeline_value(self, value):
   577	        """Formata valores do resumo operacional para exibição."""
   578	        if value is None:
   579	            return "n/d"
   580	        return str(value)
   581	
   582	    def _build_pipeline_feedback_message(self, stdout: str) -> str:
   583	        """Monta mensagem amigável para o usuário após executar pipeline."""
   584	        summary = self._extract_pipeline_summary(stdout)
   585	
   586	        if not summary:
   587	            return (
   588	                "Pipeline executado com sucesso.\n\n"
   589	                "Resumo operacional não disponível no stdout do pipeline."
   590	            )
   591	
   592	        lines = [
   593	            "Pipeline executado com sucesso.",
   594	            "",
   595	            "Resumo operacional:",
   596	            f"- Estruturas: {self._format_pipeline_value(summary.get('structures'))}",
   597	            f"- Decisões: {self._format_pipeline_value(summary.get('decisions'))}",
   598	            f"- Pontos de payoff: {self._format_pipeline_value(summary.get('payoff_points'))}",
   599	            f"- Resumos de payoff: {self._format_pipeline_value(summary.get('payoff_summaries'))}",
   600	            f"- Execuções de pricing: {self._format_pipeline_value(summary.get('pricing_executions'))}",
   601	            f"- Cotações RTD atualizadas: {self._format_pipeline_value(summary.get('rtd_quotes_updated'))}",
   602	            f"- Avisos: {self._format_pipeline_value(summary.get('warnings'))}",
   603	            f"- Erros: {self._format_pipeline_value(summary.get('errors'))}",
   604	        ]
   605	        return "\n".join(lines)
   606	
   607	    def _build_pipeline_status_message(self, stdout: str) -> str:
   608	        """Monta texto curto para status bar após pipeline."""
   609	        summary = self._extract_pipeline_summary(stdout)
   610	        if not summary:
   611	            return "Pipeline executado com sucesso"
   612	
   613	        decisions = self._format_pipeline_value(summary.get("decisions"))
   614	        payoff_points = self._format_pipeline_value(summary.get("payoff_points"))
   615	        errors = self._format_pipeline_value(summary.get("errors"))
   616	
   617	        return (
   618	            f"Pipeline OK: decisões={decisions}; "
   619	            f"pontos_payoff={payoff_points}; erros={errors}"
   620	        )
   621	
   622	
   623	    def run_pipeline(self):
   624	        """Executa o pipeline de derivados."""
   625	        result = messagebox.askyesno(
   626	            "Executar Pipeline",
   627	            "Executar pipeline de derivados?\nIsso pode demorar alguns segundos.",
   628	        )
   629	        if not result:
   630	            return
   631	
   632	        self.status_bar.config(text="Executando pipeline...")
   633	
   634	        try:
   635	            project_root = Path(__file__).resolve().parents[1]
   636	            script_path = project_root / "scripts" / "run_derived_pipeline.py"
   637	            if not script_path.exists():
   638	                script_path = project_root / "Scripts" / "run_derived_pipeline.py"
   639	
   640	            if not script_path.exists():
   641	                raise FileNotFoundError(
   642	                    f"Não achei o script do pipeline em: {script_path}"
   643	                )
   644	
   645	            import subprocess
   646	            import sys
   647	
   648	            res = subprocess.run(
   649	                [sys.executable, str(script_path)],
   650	                cwd=str(project_root),
   651	                check=True,
   652	                capture_output=True,
   653	                text=True,
   654	            )
   655	
   656	            if res.stdout:
   657	                print("[UI] Pipeline STDOUT:\n", res.stdout)
   658	            if res.stderr:
   659	                print("[UI] Pipeline STDERR:\n", res.stderr)
   660	
   661	            feedback = self._build_pipeline_feedback_message(res.stdout or "")
   662	            status_msg = self._build_pipeline_status_message(res.stdout or "")
   663	
   664	            messagebox.showinfo("Sucesso", feedback)
   665	            self.refresh_data()
   666	            self.status_bar.config(text=status_msg)
   667	
   668	        except subprocess.CalledProcessError as e:
   669	            messagebox.showerror(
   670	                "Erro",
   671	                "Pipeline falhou:\n\nSTDOUT:\n"
   672	                + (e.stdout or "")
   673	                + "\n\nSTDERR:\n"
   674	                + (e.stderr or ""),
   675	            )
   676	            self.status_bar.config(text="Pipeline falhou")
   677	        except Exception as e:
   678	            messagebox.showerror("Erro", f"Erro ao executar pipeline: {e}")
   679	            self.status_bar.config(text="Erro ao executar pipeline")
   680	
   681	    def check_databases(self):
   682	        """Verifica status dos bancos de dados."""
   683	        try:
   684	            status = self.data_model.check_database_status()
   685	            messagebox.showinfo("Status dos Bancos", status)
   686	        except Exception as e:
   687	            messagebox.showerror("Erro", f"Erro ao verificar bancos: {e}")
   688	
   689	    def clear_cache(self):
   690	        """Limpa cache interno."""
   691	        self.data_model.clear_cache()
   692	        messagebox.showinfo("Cache", "Cache limpo com sucesso")
   693	
   694	    def show_about(self):
   695	        """Mostra informações sobre o sistema."""
   696	        about_text = """Sistema de Derivados v1.0
   697	
   698	Desenvolvido para análise de estruturas de opções
   699	Pipeline automático de payoff e decisões
   700	
   701	Camadas:
   702	* Excel RTD  CSV Bridge
   703	* Ingest Python  app.db
   704	* Domain Layer  derived.db
   705	* UI Tkinter (esta interface)
   706	
   707	Baseline: executed_v1 + baseline_v1b"""
   708	        messagebox.showinfo("Sobre", about_text)
   709	
   710	    # ------------------------------------------------------------------
   711	    # Handlers de payoff (thread  main thread)
   712	    # ------------------------------------------------------------------
   713	
   714	    def _finish_payoff_load(
   715	        self,
   716	        points: List[Dict],
   717	        info_dict: Dict,
   718	        decision_data: Dict,
   719	        worker_id: int,
   720	    ):
   721	        """Executado na thread principal quando a curva chega do worker."""
   722	        if worker_id != self._payoff_worker_id:
   723	            return
   724	
   725	        self._loading_payoff = False
   726	        self._stop_loading_animation()
   727	
   728	        try:
   729	            if points:
   730	                overlays = self.payoff_chart.update_chart(points, decision_data)
   731	
   732	                try:
   733	                    self.details_panel.update_breakevens(
   734	                        overlays.get("breakevens"),
   735	                        overlays.get("pl_at_spot_ref"),
   736	                    )
   737	                except Exception:
   738	                    pass
   739	
   740	                try:
   741	                    self.details_panel.update_audit_info(info_dict or {})
   742	                except Exception:
   743	                    pass
   744	
   745	                used_ts = (info_dict or {}).get("used_timestamp") or decision_data.get(
   746	                    "timestamp"
   747	                )
   748	                src = (info_dict or {}).get("source_table", "payoff_curve_points")
   749	                n = (info_dict or {}).get("count_points", len(points))
   750	                msg = f"{n} pontos ({src})"
   751	                if used_ts and used_ts != decision_data.get("timestamp"):
   752	                    msg += f" | ts usado: {used_ts}"
   753	                self.status_bar.config(text=msg)
   754	            else:
   755	                self.payoff_chart.clear()
   756	                self.status_bar.config(text="Sem dados de payoff para esta seleção")
   757	        except Exception as e:
   758	            self._handle_payoff_error(str(e), worker_id)
   759	
   760	    def _handle_payoff_error(self, error_msg: str, worker_id: int):
   761	        if worker_id != self._payoff_worker_id:
   762	            return
   763	        self._loading_payoff = False
   764	        self._stop_loading_animation()
   765	        try:
   766	            self.payoff_chart.clear()
   767	        except Exception:
   768	            pass
   769	        self.status_bar.config(text=f"Erro ao carregar payoff: {error_msg}")
   770	        print(f"[UI] Erro no payoff: {error_msg}")
   771	        import traceback
   772	        traceback.print_exc()
   773	
   774	    # ------------------------------------------------------------------
   775	    # Loading animation
   776	    # ------------------------------------------------------------------
   777	
   778	    def _start_loading_animation(self, base_text: str):
   779	        self._loading_animation_active = True
   780	        self._loading_animation_index = 0
   781	
   782	        def animate():
   783	            if not self._loading_animation_active:
   784	                return
   785	            char = self._loading_animation_chars[self._loading_animation_index]
   786	            self.status_bar.config(text=f"{char} {base_text}")
   787	            self._loading_animation_index = (
   788	                self._loading_animation_index + 1
   789	            ) % len(self._loading_animation_chars)
   790	            self.root.after(100, animate)
   791	
   792	        animate()
   793	
   794	    def _stop_loading_animation(self):
   795	        self._loading_animation_active = False
   796	
   797	    # ------------------------------------------------------------------
   798	    # Aba Estruturas (Fase 5 -- alteracao_10)
   799	    # ------------------------------------------------------------------
   800	
   801	    def _setup_structures_tab(self, notebook: ttk.Notebook):
   802	        """Aba 'Estruturas' no notebook principal."""
   803	        outer = ttk.Frame(notebook)
   804	        notebook.add(outer, text=" Estruturas")
   805	
   806	        paned = ttk.PanedWindow(outer, orient="horizontal")
   807	        paned.pack(fill="both", expand=True, padx=4, pady=4)
   808	
   809	        # Painel esquerdo -- lista
   810	        list_frame = ttk.Frame(paned)
   811	        paned.add(list_frame, weight=1)
   812	
   813	        self.structures_list = StructuresListPanel(
   814	            list_frame,
   815	            on_structure_selected=self._on_structure_selected,
   816	            on_request_edit=self._on_structure_edit_request,
   817	            db_path=self._db_path,
   818	        )
   819	        self.structures_list.pack(fill="both", expand=True)
   820	
   821	        # Painel direito -- detalhes somente leitura
   822	        detail_frame = ttk.LabelFrame(paned, text="Detalhes", padding=8)
   823	        paned.add(detail_frame, weight=1)
   824	
   825	        self._struct_detail_text = tk.Text(
   826	            detail_frame,
   827	            state="disabled",
   828	            wrap="word",
   829	            font=("Consolas", 9),
   830	            background="#fafafa",
   831	        )
   832	        self._struct_detail_text.pack(fill="both", expand=True)
   833	
   834	    def _on_structure_selected(self, structure: Optional[Dict]):
   835	        """Exibe detalhes da estrutura selecionada no painel direito."""
   836	        txt = self._struct_detail_text
   837	        txt.config(state="normal")
   838	        txt.delete("1.0", "end")
   839	
   840	        if structure is None:
   841	            txt.insert("end", "Nenhuma estrutura selecionada.")
   842	        else:
   843	            legs = structure.get("legs", [])
   844	            lines = [
   845	                f"ID         : {structure.get('id')}",
   846	                f"Nome       : {structure.get('name')}",
   847	                f"Ativo      : {structure.get('underlying_asset')}",
   848	                f"Aba legado : {structure.get('alias_legacy_aba') or '--'}",
   849	                f"Status     : {structure.get('status')}",
   850	                f"Criado em  : {str(structure.get('created_at', ''))[:19]}",
   851	                f"Atualizado : {str(structure.get('updated_at', ''))[:19]}",
   852	                f"Obs        : {structure.get('notes') or '--'}",
   853	                "",
   854	                f" {len(legs)} Leg(s) ",
   855	            ]
   856	            for i, leg in enumerate(legs, 1):
   857	                lines += [
   858	                    f"  Leg {i}: {leg.get('position_side')} {leg.get('option_type')}",
   859	                    f"         Strike : {leg.get('strike')}  Venc: {leg.get('expiration_date')}",
   860	                    f"         Qtde   : {leg.get('quantity')}  Símbolo: {leg.get('symbol') or '--'}",
   861	                    f"         Prêmio : {leg.get('premium')}  Mult: {leg.get('multiplier')}",
   862	                    "",
   863	                ]
   864	            txt.insert("end", "\n".join(lines))
   865	
   866	        txt.config(state="disabled")
   867	
   868	    def _on_structure_edit_request(self, structure_id: Optional[int]):
   869	        """Abre dialog de criação (None) ou edição (int)."""
   870	        dlg = StructureEditorDialog(
   871	            self.root,
   872	            structure_id=structure_id,
   873	            db_path=self._db_path,                            # ← usa instância
   874	        )
   875	        self.root.wait_window(dlg)
   876	        if dlg.saved:
   877	            saved_structure_id = getattr(dlg, "saved_structure_id", None) or structure_id
   878	
   879	            self.structures_list.load()
   880	
   881	            try:
   882	                self.status_bar.config(text="Estrutura salva com sucesso.")
   883	            except Exception:
   884	                pass
   885	
   886	            if saved_structure_id is not None:
   887	                self._reprice_structure_after_save(int(saved_structure_id))
   888	
   889	
   890	    def _reprice_structure_after_save(self, structure_id: int) -> None:
   891	        """
   892	        Recalcula pricing/payoff/decisão após criação ou edição manual.
   893	
   894	        Usa thread para não congelar a UI.
   895	        Falhas não desfazem o cadastro da estrutura.
   896	        """
   897	
   898	        def _set_status(text: str) -> None:
   899	            try:
   900	                self.status_bar.config(text=text)
   901	            except Exception:
   902	                pass
   903	
   904	        def _post_status(text: str) -> None:
   905	            try:
   906	                self.root.after(0, lambda: _set_status(text))
   907	            except Exception:
   908	                _set_status(text)
   909	
   910	        sid = int(structure_id)
   911	        _post_status(f"Estrutura {sid} salva. Recalculando payoff...")
   912	
   913	        def _worker() -> None:
   914	            try:
   915	                # Import lazy para evitar side-effects no import da UI/testes.
   916	                from services.canonical_pricing_facade import CanonicalPricingFacade
   917	
   918	                facade = CanonicalPricingFacade(db_path=self._db_path)
   919	                result = facade.execute_pricing(sid)
   920	
   921	                if isinstance(result, dict) and result.get("status") == "error":
   922	                    raise RuntimeError(
   923	                        result.get("error_message") or "Erro no recálculo automático"
   924	                    )
   925	
   926	                def _after_success() -> None:
   927	                    _set_status(f"Estrutura {sid} salva e payoff recalculado.")
   928	                    try:
   929	                        self.refresh_data()
   930	                    except Exception:
   931	                        pass
   932	
   933	                try:
   934	                    self.root.after(0, _after_success)
   935	                except Exception:
   936	                    _after_success()
   937	
   938	            except Exception as exc:
   939	                _post_status(
   940	                    f"Estrutura {sid} salva, mas o recálculo automático falhou: {exc}"
   941	                )
   942	
   943	        threading.Thread(target=_worker, daemon=True).start()
   944	
   945	
   946	    # ------------------------------------------------------------------
   947	    # Entry point
   948	    # ------------------------------------------------------------------
   949	
   950	    def run(self):
   951	        """Inicia a aplicação."""
   952	        self.root.mainloop()
   953	
   954	def main():
   955	    """Entry point da UI."""
   956	    app = MainWindow()
   957	    app.run()
   958	
   959	if __name__ == "__main__":
   960	    main()
```

## FILE: ATT/tests/test_decision.py
```python
     1	from domain.decision import compute_decision_from_payoff
     2	
     3	
     4	def test_compute_decision_from_payoff_should_work_without_alias_legacy_aba():
     5	    """
     6	    Garante que compute_decision_from_payoff funciona com payoff canônico
     7	    que não carrega alias_legacy_aba -- substitui o teste de contract com dict.
     8	    """
     9	    payoff = {
    10	        "pl_atual": 120.0,
    11	        "pl_max":   200.0,
    12	        "pl_min":   -50.0,
    13	        "points":   [],
    14	        "spot":     198.35,
    15	    }
    16	
    17	    result = compute_decision_from_payoff(
    18	        payoff=payoff,
    19	        dte_min=12,
    20	    )
    21	
    22	    assert "decision" in result
    23	    assert "why" in result
    24	    assert result["decision"] in ("HOLD", "WATCH", "PREPARE", "PREPARE_ROLL", "CLOSE_REOPEN", "CLOSE")
    25	    # dte_min é registrado no why quando DTE gate é ativado
    26	    # com dte_min=12 > dte_gate=7 não há gate, decisão depende do ratio
    27	    assert isinstance(result.get("why"), dict)
```

## FILE: ATT/tests/test_payoff_canonical.py
```python
     1	from domain.payoff import compute_payoff_from_canonical_input
     2	
     3	
     4	def test_compute_payoff_from_canonical_input_should_preserve_canonical_metadata():
     5	    canonical_input = {
     6	        "structure": {
     7	            "structure_id": 7,
     8	            "name": "BOVA11 Condor Maio/2026",
     9	            "underlying_asset": "BOVA11",
    10	            "legs": [
    11	                {
    12	                    "position_side": "LONG",
    13	                    "option_type": "CALL",
    14	                    "symbol": "BOVAE195",
    15	                    "strike": 195.0,
    16	                    "expiration_date": "2026-05-15",
    17	                    "quantity": 1,
    18	                    "premium": 2.0,
    19	                    "multiplier": 1.0,
    20	                }
    21	            ],
    22	        },
    23	        "market": {
    24	            "reference_date": "2026-05-18",
    25	            "underlying_asset": "BOVA11",
    26	            "spot_price": 198.35,
    27	            "interest_rate": 0.1175,
    28	            "volatility": 0.22,
    29	        },
    30	        "meta": {
    31	            "reference_date": "2026-05-18",
    32	            "legs_source": "canonical",
    33	            "input_source": "test",
    34	        },
    35	    }
    36	
    37	    result = compute_payoff_from_canonical_input(canonical_input)
    38	
    39	    assert result["structure_id"] == 7
    40	    assert result["structure_name"] == "BOVA11 Condor Maio/2026"
    41	    assert result["underlying_asset"] == "BOVA11"
    42	    assert result["reference_date"] == "2026-05-18"
    43	    assert result["input_meta"]["legs_source"] == "canonical"
```

## FILE: ATT/tests/test_payoff_chart.py
```python
     1	# C:/users/eucal/projeto/ATT/tests/test_payoff_chart.py
     2	"""
     3	Testes unitários para UI/components/payoff_chart.py
     4	Cobertura:
     5	  - _fmt_number_br / _fmt_currency_br / _brl_abbrev
     6	  - _find_breakevens
     7	  - _interp_y_at_x
     8	  - _extract_xy (tuple, dict, objeto)
     9	  - PayoffChart.clear()
    10	  - PayoffChart.update_chart()
    11	  - PayoffChart.fix_current_curve() / clear_comparison()
    12	  - PayoffChart.get_last_overlays()
    13	"""
    14	
    15	import sys
    16	import os
    17	import unittest
    18	from unittest.mock import MagicMock, patch
    19	
    20	# ---------------------------------------------------------------------------
    21	# Raiz do projeto: C:/users/eucal/projeto
    22	# tests/ está em ATT/tests/, então subimos UM nível para chegar em ATT/
    23	# e mais UM para chegar na raiz C:/users/eucal/projeto
    24	# ---------------------------------------------------------------------------
    25	PROJECT_ROOT = os.path.abspath(
    26	    os.path.join(os.path.dirname(__file__), "..", "..")
    27	    # ATT/tests/ -> ATT/ -> projeto/
    28	)
    29	if PROJECT_ROOT not in sys.path:
    30	    sys.path.insert(0, PROJECT_ROOT)
    31	
    32	# ---------------------------------------------------------------------------
    33	# Stub de módulos que exigem display ou infra real
    34	# ---------------------------------------------------------------------------
    35	_STUBS = {
    36	    "matplotlib":                        MagicMock(),
    37	    "matplotlib.use":                    MagicMock(),
    38	    "matplotlib.figure":                 MagicMock(),
    39	    "matplotlib.ticker":                 MagicMock(),
    40	    "matplotlib.backends":               MagicMock(),
    41	    "matplotlib.backends.backend_tkagg": MagicMock(),
    42	    "UI.debug_utils":                    MagicMock(),
    43	}
    44	for _mod, _stub in _STUBS.items():
    45	    sys.modules.setdefault(_mod, _stub)
    46	
    47	# FuncFormatter precisa ser chamável
    48	sys.modules["matplotlib.ticker"].FuncFormatter = lambda f: f
    49	
    50	# Importa DEPOIS dos stubs
    51	from UI.components.payoff_chart import (  # noqa: E402
    52	    PayoffChart,
    53	    _fmt_number_br,
    54	    _fmt_currency_br,
    55	    _brl_abbrev,
    56	)
    57	
    58	
    59	# ---------------------------------------------------------------------------
    60	# Fixture: instância de PayoffChart com Tk fake
    61	# ---------------------------------------------------------------------------
    62	
    63	def _make_chart() -> PayoffChart:
    64	    """Cria PayoffChart com dependências Tk mockadas."""
    65	    with patch("UI.components.payoff_chart.FigureCanvasTkAgg"), \
    66	         patch("UI.components.payoff_chart.NavigationToolbar2Tk"), \
    67	         patch("UI.components.payoff_chart.Figure") as MockFig, \
    68	         patch("UI.components.payoff_chart.ttk.Frame.__init__", return_value=None), \
    69	         patch("UI.components.payoff_chart.ttk.Frame.pack",     return_value=None), \
    70	         patch("UI.components.payoff_chart.ttk.Frame.bind",     return_value=None):
    71	
    72	        mock_fig = MagicMock()
    73	        mock_ax  = MagicMock()
    74	        mock_fig.add_subplot.return_value = mock_ax
    75	        MockFig.return_value = mock_fig
    76	
    77	        chart = PayoffChart.__new__(PayoffChart)
    78	        chart.fig     = mock_fig
    79	        chart.ax      = mock_ax
    80	        chart.canvas  = MagicMock()
    81	        chart.toolbar = MagicMock()
    82	        chart._last_breakevens     = []
    83	        chart._last_pl_at_spot_ref = None
    84	        chart._last_points         = []
    85	        chart._last_decision_data  = {}
    86	        chart._fixed_curve         = None
    87	
    88	    return chart
    89	
    90	
    91	# ---------------------------------------------------------------------------
    92	# Sample data helpers
    93	# ---------------------------------------------------------------------------
    94	
    95	def _linear_points(n: int = 20, x_start=90.0, x_end=110.0,
    96	                   y_start=-1000.0, y_end=1000.0):
    97	    """Gera pontos lineares cruzando zero."""
    98	    points = []
    99	    for i in range(n):
   100	        t = i / (n - 1)
   101	        x = x_start + t * (x_end - x_start)
   102	        y = y_start + t * (y_end - y_start)
   103	        points.append({"spot": x, "pl": y})
   104	    return points
   105	
   106	
   107	def _flat_points(n: int = 10, x_start=90.0, x_end=110.0, y=500.0):
   108	    """Pontos com PL constante (sem breakeven)."""
   109	    return [
   110	        {"spot": x_start + i * (x_end - x_start) / (n - 1), "pl": y}
   111	        for i in range(n)
   112	    ]
   113	
   114	
   115	# ===========================================================================
   116	# Testes de Formatação
   117	# ===========================================================================
   118	
   119	class TestFormatters(unittest.TestCase):
   120	
   121	    def test_fmt_number_br_basic(self):
   122	        self.assertEqual(_fmt_number_br(1234.56), "1.234,56")
   123	
   124	    def test_fmt_number_br_zero(self):
   125	        self.assertEqual(_fmt_number_br(0), "0,00")
   126	
   127	    def test_fmt_number_br_negative(self):
   128	        self.assertEqual(_fmt_number_br(-1500.0), "-1.500,00")
   129	
   130	    def test_fmt_number_br_million(self):
   131	        self.assertEqual(_fmt_number_br(1_000_000), "1.000.000,00")
   132	
   133	    def test_fmt_number_br_custom_decimals(self):
   134	        self.assertEqual(_fmt_number_br(100.1, 0), "100")
   135	
   136	    def test_fmt_currency_br_basic(self):
   137	        self.assertEqual(_fmt_currency_br(500.0), "R$ 500,00")
   138	
   139	    def test_fmt_currency_br_negative(self):
   140	        self.assertTrue(_fmt_currency_br(-200.5).startswith("R$"))
   141	
   142	    def test_brl_abbrev_below_1k(self):
   143	        self.assertIn("500", _brl_abbrev(500))
   144	
   145	    def test_brl_abbrev_thousands(self):
   146	        self.assertIn("k", _brl_abbrev(1500))
   147	
   148	    def test_brl_abbrev_millions(self):
   149	        self.assertIn("M", _brl_abbrev(2_500_000))
   150	
   151	    def test_brl_abbrev_billions(self):
   152	        self.assertIn("B", _brl_abbrev(3_000_000_000))
   153	
   154	    def test_brl_abbrev_negative(self):
   155	        result = _brl_abbrev(-5000)
   156	        self.assertIn("-", result)
   157	        self.assertIn("k", result)
   158	
   159	    def test_brl_abbrev_invalid(self):
   160	        result = _brl_abbrev("NaN")
   161	        self.assertIn("R$", result)
   162	
   163	
   164	# ===========================================================================
   165	# Testes de _find_breakevens
   166	# ===========================================================================
   167	
   168	class TestFindBreakevens(unittest.TestCase):
   169	
   170	    def _be(self, spots, pls):
   171	        return PayoffChart._find_breakevens(spots, pls)
   172	
   173	    def test_single_crossing_zero(self):
   174	        spots = [90.0, 95.0, 100.0, 105.0, 110.0]
   175	        pls   = [-200, -100, 0, 100, 200]
   176	        bks   = self._be(spots, pls)
   177	        self.assertEqual(len(bks), 1)
   178	        self.assertAlmostEqual(bks[0], 100.0, places=5)
   179	
   180	    def test_interpolated_crossing(self):
   181	        spots = [98.0, 102.0]
   182	        pls   = [-100.0, 100.0]
   183	        bks   = self._be(spots, pls)
   184	        self.assertEqual(len(bks), 1)
   185	        self.assertAlmostEqual(bks[0], 100.0, places=5)
   186	
   187	    def test_no_crossing(self):
   188	        spots = [90.0, 100.0, 110.0]
   189	        pls   = [100.0, 200.0, 300.0]
   190	        bks   = self._be(spots, pls)
   191	        self.assertEqual(bks, [])
   192	
   193	    def test_two_crossings(self):
   194	        spots = [80.0, 90.0, 100.0, 110.0, 120.0]
   195	        pls   = [100.0, -50.0, -100.0, -50.0, 100.0]
   196	        bks   = self._be(spots, pls)
   197	        self.assertEqual(len(bks), 2)
   198	
   199	    def test_touching_zero_without_crossing(self):
   200	        spots = [95.0, 100.0, 105.0]
   201	        pls   = [100.0, 0.0, 100.0]
   202	        bks   = self._be(spots, pls)
   203	        self.assertIn(100.0, bks)
   204	
   205	    def test_empty_inputs(self):
   206	        self.assertEqual(self._be([], []), [])
   207	
   208	    def test_mismatched_lengths(self):
   209	        self.assertEqual(self._be([1, 2], [1]), [])
   210	
   211	    def test_deduplication(self):
   212	        spots = [99.9999, 100.0, 100.0001]
   213	        pls   = [-1e-10, 0.0, 1e-10]
   214	        bks   = self._be(spots, pls)
   215	        self.assertLessEqual(len(bks), 2)
   216	
   217	
   218	# ===========================================================================
   219	# Testes de _interp_y_at_x
   220	# ===========================================================================
   221	
   222	class TestInterpYAtX(unittest.TestCase):
   223	
   224	    def _interp(self, xs, ys, x):
   225	        return PayoffChart._interp_y_at_x(xs, ys, x)
   226	
   227	    def test_exact_point(self):
   228	        xs = [90.0, 100.0, 110.0]
   229	        ys = [0.0,  500.0, 1000.0]
   230	        self.assertAlmostEqual(self._interp(xs, ys, 100.0), 500.0)
   231	
   232	    def test_midpoint_interpolation(self):
   233	        xs = [0.0, 10.0]
   234	        ys = [0.0, 100.0]
   235	        self.assertAlmostEqual(self._interp(xs, ys, 5.0), 50.0)
   236	
   237	    def test_out_of_range_returns_none(self):
   238	        xs = [90.0, 110.0]
   239	        ys = [0.0, 100.0]
   240	        self.assertIsNone(self._interp(xs, ys, 200.0))
   241	
   242	    def test_empty_returns_none(self):
   243	        self.assertIsNone(self._interp([], [], 100.0))
   244	
   245	    def test_mismatched_returns_none(self):
   246	        self.assertIsNone(self._interp([1, 2, 3], [1, 2], 1.5))
   247	
   248	    def test_negative_ys(self):
   249	        xs = [0.0, 10.0]
   250	        ys = [-100.0, 100.0]
   251	        self.assertAlmostEqual(self._interp(xs, ys, 5.0), 0.0)
   252	
   253	    def test_single_segment_boundary_right(self):
   254	        xs = [10.0, 20.0]
   255	        ys = [0.0, 10.0]
   256	        self.assertAlmostEqual(self._interp(xs, ys, 20.0), 10.0)
   257	
   258	
   259	# ===========================================================================
   260	# Testes de _extract_xy
   261	# ===========================================================================
   262	
   263	class TestExtractXY(unittest.TestCase):
   264	
   265	    def _ex(self, p):
   266	        return _make_chart()._extract_xy(p)
   267	
   268	    def test_tuple_format(self):
   269	        x, y = self._ex((100.0, 500.0))
   270	        self.assertAlmostEqual(x, 100.0)
   271	        self.assertAlmostEqual(y, 500.0)
   272	
   273	    def test_list_format(self):
   274	        x, y = self._ex([95.0, -200.0])
   275	        self.assertAlmostEqual(x, 95.0)
   276	        self.assertAlmostEqual(y, -200.0)
   277	
   278	    def test_dict_spot_pl(self):
   279	        x, y = self._ex({"spot": 100.5, "pl": 300.0})
   280	        self.assertAlmostEqual(x, 100.5)
   281	        self.assertAlmostEqual(y, 300.0)
   282	
   283	    def test_dict_point_spot_point_pl(self):
   284	        x, y = self._ex({"point_spot": 99.0, "point_pl": -50.0})
   285	        self.assertAlmostEqual(x, 99.0)
   286	        self.assertAlmostEqual(y, -50.0)
   287	
   288	    def test_dict_x_y(self):
   289	        x, y = self._ex({"x": 50.0, "y": 1000.0})
   290	        self.assertAlmostEqual(x, 50.0)
   291	        self.assertAlmostEqual(y, 1000.0)
   292	
   293	    def test_dict_pnl(self):
   294	        x, y = self._ex({"spot": 105.0, "pnl": 750.0})
   295	        self.assertAlmostEqual(x, 105.0)
   296	        self.assertAlmostEqual(y, 750.0)
   297	
   298	    def test_unknown_format_returns_none(self):
   299	        x, y = self._ex({})
   300	        self.assertIsNone(x)
   301	        self.assertIsNone(y)
   302	
   303	
   304	# ===========================================================================
   305	# Testes de PayoffChart (estado e lógica)
   306	# ===========================================================================
   307	
   308	class TestPayoffChartState(unittest.TestCase):
   309	
   310	    def setUp(self):
   311	        self.chart = _make_chart()
   312	
   313	    def test_clear_resets_state(self):
   314	        self.chart._last_breakevens     = [100.0]
   315	        self.chart._last_pl_at_spot_ref = 500.0
   316	        self.chart._last_points         = [{"spot": 100.0, "pl": 0.0}]
   317	        self.chart.clear()
   318	        self.assertEqual(self.chart._last_breakevens, [])
   319	        self.assertIsNone(self.chart._last_pl_at_spot_ref)
   320	        self.assertEqual(self.chart._last_points, [])
   321	
   322	    def test_update_chart_empty_returns_dict(self):
   323	        result = self.chart.update_chart([])
   324	        self.assertIn("breakevens", result)
   325	        self.assertIn("pl_at_spot_ref", result)
   326	
   327	    def test_update_chart_saves_points(self):
   328	        pts = _linear_points()
   329	        self.chart.update_chart(pts)
   330	        self.assertEqual(len(self.chart._last_points), len(pts))
   331	
   332	    def test_update_chart_saves_decision_data(self):
   333	        pts = _linear_points()
   334	        dd  = {"structure_id": "collar_1", "decision": "BUY", "spot_ref": 100.0}
   335	        self.chart.update_chart(pts, decision_data=dd)
   336	        self.assertEqual(self.chart._last_decision_data["structure_id"], "collar_1")
   337	
   338	    def test_update_chart_finds_breakeven(self):
   339	        pts    = _linear_points(n=200, x_start=90, x_end=110,
   340	                                y_start=-1000, y_end=1000)
   341	        result = self.chart.update_chart(pts)
   342	        self.assertGreater(len(result["breakevens"]), 0)
   343	        self.assertAlmostEqual(result["breakevens"][0], 100.0, delta=0.2)
   344	
   345	    def test_update_chart_no_breakeven_flat(self):
   346	        result = self.chart.update_chart(_flat_points(y=500.0))
   347	        self.assertEqual(result["breakevens"], [])
   348	
   349	    def test_update_chart_pl_at_spot_ref(self):
   350	        pts    = _linear_points(n=200, x_start=90, x_end=110,
   351	                                y_start=-1000, y_end=1000)
   352	        result = self.chart.update_chart(pts, decision_data={"spot_ref": 100.0})
   353	        self.assertIsNotNone(result["pl_at_spot_ref"])
   354	        self.assertAlmostEqual(result["pl_at_spot_ref"], 0.0, delta=20.0)
   355	
   356	    def test_update_chart_spot_ref_none_when_missing(self):
   357	        result = self.chart.update_chart(_linear_points(), decision_data={})
   358	        self.assertIsNone(result["pl_at_spot_ref"])
   359	
   360	    def test_fix_current_curve_sets_fixed(self):
   361	        self.chart._last_points = _linear_points()
   362	        self.chart.fix_current_curve()
   363	        self.assertIsNotNone(self.chart._fixed_curve)
   364	        self.assertIn("points", self.chart._fixed_curve)
   365	
   366	    def test_fix_empty_clears_fixed(self):
   367	        self.chart._last_points = []
   368	        self.chart.fix_current_curve()
   369	        self.assertIsNone(self.chart._fixed_curve)
   370	
   371	    def test_fix_curve_label(self):
   372	        self.chart._last_points = _linear_points()
   373	        self.chart.fix_current_curve()
   374	        self.assertIn("Curva A", self.chart._fixed_curve["label"])
   375	
   376	    def test_fix_curve_color_is_red(self):
   377	        self.chart._last_points = _linear_points()
   378	        self.chart.fix_current_curve()
   379	        self.assertEqual(self.chart._fixed_curve["color"], "red")
   380	
   381	    def test_clear_comparison_removes_fixed(self):
   382	        self.chart._last_points = _linear_points()
   383	        self.chart.fix_current_curve()
   384	        self.chart.clear_comparison()
   385	        self.assertIsNone(self.chart._fixed_curve)
   386	
   387	    def test_get_last_overlays_structure(self):
   388	        ov = self.chart.get_last_overlays()
   389	        self.assertIn("breakevens", ov)
   390	        self.assertIn("pl_at_spot_ref", ov)
   391	        self.assertIsInstance(ov["breakevens"], list)
   392	
   393	    def test_title_uses_structure_id(self):
   394	        pts = _linear_points()
   395	        dd  = {"structure_id": "strangle_X", "aba": "old_aba", "decision": "BUY"}
   396	        self.chart.update_chart(pts, decision_data=dd)
   397	        calls = [str(c) for c in self.chart.ax.set_title.call_args_list]
   398	        self.assertTrue(any("strangle_X" in c for c in calls))
   399	
   400	    def test_title_fallback_to_aba(self):
   401	        pts = _linear_points()
   402	        dd  = {"aba": "straddle_Y", "decision": "SELL"}
   403	        self.chart.update_chart(pts, decision_data=dd)
   404	        calls = [str(c) for c in self.chart.ax.set_title.call_args_list]
   405	        self.assertTrue(any("straddle_Y" in c for c in calls))
   406	
   407	    def test_update_chart_with_tuple_points(self):
   408	        pts    = [(90 + i, -500 + i * 100) for i in range(11)]
   409	        result = self.chart.update_chart(pts)
   410	        self.assertIsInstance(result["breakevens"], list)
   411	
   412	    def test_update_chart_with_list_points(self):
   413	        pts    = [[90 + i, -500 + i * 100] for i in range(11)]
   414	        result = self.chart.update_chart(pts)
   415	        self.assertIsInstance(result["breakevens"], list)
   416	
   417	
   418	# ===========================================================================
   419	# Testes de robustez / edge cases
   420	# ===========================================================================
   421	
   422	class TestPayoffChartRobustness(unittest.TestCase):
   423	
   424	    def setUp(self):
   425	        self.chart = _make_chart()
   426	
   427	    def test_update_chart_none_decision_data(self):
   428	        result = self.chart.update_chart(_linear_points(), decision_data=None)
   429	        self.assertIsNotNone(result)
   430	
   431	    def test_update_chart_single_point(self):
   432	        try:
   433	            self.chart.update_chart([{"spot": 100.0, "pl": 0.0}])
   434	        except Exception as e:
   435	            self.fail(f"Lançou exceção com 1 ponto: {e}")
   436	
   437	    def test_update_chart_all_zero_pl(self):
   438	        pts    = [{"spot": 90 + i, "pl": 0.0} for i in range(10)]
   439	        result = self.chart.update_chart(pts)
   440	        self.assertIsNotNone(result)
   441	
   442	    def test_update_chart_invalid_pl_skipped(self):
   443	        pts = [
   444	            {"spot": 90.0,  "pl": "invalid"},
   445	            {"spot": 100.0, "pl": 500.0},
   446	            {"spot": 110.0, "pl": 1000.0},
   447	        ]
   448	        try:
   449	            result = self.chart.update_chart(pts)
   450	            self.assertIsNotNone(result)
   451	        except Exception as e:
   452	            self.fail(f"Lançou exceção com pl inválido: {e}")
   453	
   454	    def test_find_breakevens_constant_positive(self):
   455	        self.assertEqual(
   456	            PayoffChart._find_breakevens(list(range(10)), [100.0] * 10), []
   457	        )
   458	
   459	    def test_find_breakevens_single_point(self):
   460	        self.assertEqual(PayoffChart._find_breakevens([100.0], [0.0]), [])
   461	
   462	    def test_interp_same_x_values(self):
   463	        result = PayoffChart._interp_y_at_x([100.0, 100.0], [0.0, 500.0], 100.0)
   464	        self.assertIsNone(result)
   465	
   466	    def test_fix_and_update_keeps_fixed_curve(self):
   467	        self.chart._last_points = _linear_points()
   468	        self.chart.fix_current_curve()
   469	        fixed_before = self.chart._fixed_curve
   470	
   471	        self.chart.update_chart(_linear_points(x_start=85, x_end=115))
   472	        self.assertEqual(self.chart._fixed_curve, fixed_before)
   473	
   474	
   475	if __name__ == "__main__":
   476	    unittest.main(verbosity=2)
```

## FILE: ATT/tests/test_payoff_pricing_engine.py
```python
     1	import pytest
     2	
     3	from services.payoff_pricing_engine import PayoffPricingEngine
     4	
     5	
     6	def test_run_returns_payoff_based_metrics_and_valuation():
     7	    engine = PayoffPricingEngine()
     8	
     9	    pricing_payload = {
    10	        "structure_id": 123,
    11	        "underlying_asset": "BOVA11",
    12	        "reference_date": "2026-05-16",
    13	        "spot_price": 100.0,
    14	        "interest_rate": 0.1175,
    15	        "volatility": 0.22,
    16	        "legs": [
    17	            {
    18	                "side": "LONG",
    19	                "option_type": "CALL",
    20	                "strike": 100.0,
    21	                "quantity": 1,
    22	                "multiplier": 100,
    23	                "premium": 5.0,
    24	            }
    25	        ],
    26	    }
    27	
    28	    result = engine.run(pricing_payload)
    29	
    30	    assert result["engine"] == "payoff_pricing_engine"
    31	    assert result["status"] == "ok"
    32	    assert result["structure_id"] == 123
    33	    assert result["underlying_asset"] == "BOVA11"
    34	    assert result["reference_date"] == "2026-05-16"
    35	
    36	    assert result["metrics"]["number_of_legs"] == 1
    37	    assert result["metrics"]["total_quantity"] == 1
    38	    assert result["metrics"]["spot_price"] == 100.0
    39	    assert result["metrics"]["interest_rate"] == 0.1175
    40	    assert result["metrics"]["volatility"] == 0.22
    41	    assert result["metrics"]["payoff_points"] == 101
    42	
    43	    assert result["valuation"]["premium_paid"] == 500.0
    44	    assert result["valuation"]["theoretical_value"] == -500.0
    45	    assert result["valuation"]["pl_atual"] == -500.0
    46	    assert result["valuation"]["pl_min"] == -500.0
    47	    assert result["valuation"]["pl_max"] == 4500.0
    48	    assert result["valuation"]["max_profit"] == 4500.0
    49	    assert result["valuation"]["max_loss"] == -500.0
    50	
    51	    assert "payoff" in result
    52	    assert len(result["payoff"]["points"]) == 101
    53	
    54	
    55	def test_run_accepts_position_side_alias():
    56	    engine = PayoffPricingEngine()
    57	
    58	    pricing_payload = {
    59	        "structure_id": 123,
    60	        "underlying_asset": "BOVA11",
    61	        "reference_date": "2026-05-16",
    62	        "spot_price": 100.0,
    63	        "interest_rate": 0.0,
    64	        "volatility": 0.0,
    65	        "legs": [
    66	            {
    67	                "position_side": "LONG",
    68	                "option_type": "PUT",
    69	                "strike": 100.0,
    70	                "quantity": 1,
    71	                "multiplier": 100,
    72	                "premium": 4.0,
    73	            }
    74	        ],
    75	    }
    76	
    77	    result = engine.run(pricing_payload)
    78	
    79	    assert result["status"] == "ok"
    80	    assert result["metrics"]["payoff_points"] == 101
    81	
    82	
    83	def test_run_raises_when_pricing_payload_is_missing():
    84	    engine = PayoffPricingEngine()
    85	
    86	    with pytest.raises(ValueError, match="pricing_payload is required"):
    87	        engine.run({})
    88	
    89	
    90	def test_run_raises_when_legs_are_missing():
    91	    engine = PayoffPricingEngine()
    92	
    93	    pricing_payload = {
    94	        "structure_id": 123,
    95	        "underlying_asset": "BOVA11",
    96	        "reference_date": "2026-05-16",
    97	        "spot_price": 100.0,
    98	        "interest_rate": 0.0,
    99	        "volatility": 0.0,
   100	        "legs": [],
   101	    }
   102	
   103	    with pytest.raises(ValueError, match="pricing_payload.legs is required"):
   104	        engine.run(pricing_payload)
   105	
   106	
   107	def test_run_raises_when_spot_price_is_missing():
   108	    engine = PayoffPricingEngine()
   109	
   110	    pricing_payload = {
   111	        "structure_id": 123,
   112	        "underlying_asset": "BOVA11",
   113	        "reference_date": "2026-05-16",
   114	        "spot_price": 0.0,
   115	        "interest_rate": 0.0,
   116	        "volatility": 0.0,
   117	        "legs": [
   118	            {
   119	                "side": "LONG",
   120	                "option_type": "CALL",
   121	                "strike": 100.0,
   122	                "quantity": 1,
   123	                "multiplier": 100,
   124	                "premium": 5.0,
   125	            }
   126	        ],
   127	    }
   128	
   129	    with pytest.raises(ValueError, match="pricing_payload.spot_price is required"):
   130	        engine.run(pricing_payload)
```

## FILE: ATT/tests/test_structure_analysis_service.py
```python
     1	import pytest
     2	
     3	from services.structure_analysis_service import StructureAnalysisService
     4	
     5	
     6	class FakeCanonicalInputService:
     7	    def __init__(self, error=None):
     8	        self.error = error
     9	        self.calls = []
    10	
    11	    def build_structure_market_input(
    12	        self,
    13	        structure_id: int,
    14	        reference_date: str | None = None,
    15	    ):
    16	        self.calls.append(
    17	            {
    18	                "structure_id": structure_id,
    19	                "reference_date": reference_date,
    20	            }
    21	        )
    22	
    23	        if self.error is not None:
    24	            raise self.error
    25	
    26	        return {
    27	            "structure": {
    28	                "structure_id": structure_id,
    29	                "name": "BOVA11 Condor Maio/2026 - Atualizada",
    30	                "underlying_asset": "BOVA11",
    31	                "alias_legacy_aba": "BOVA11",
    32	                "legs": [
    33	                    {
    34	                        "position_side": "LONG",
    35	                        "option_type": "PUT",
    36	                        "symbol": "BOVAM190",
    37	                        "strike": 190.0,
    38	                        "expiration_date": "2026-05-15",
    39	                        "quantity": 2000,
    40	                        "premium": None,
    41	                        "multiplier": 1.0,
    42	                    },
    43	                    {
    44	                        "position_side": "SHORT",
    45	                        "option_type": "PUT",
    46	                        "symbol": "BOVAM185",
    47	                        "strike": 185.0,
    48	                        "expiration_date": "2026-05-15",
    49	                        "quantity": 2000,
    50	                        "premium": None,
    51	                        "multiplier": 1.0,
    52	                    },
    53	                ],
    54	            },
    55	            "market": {
    56	                "reference_date": reference_date or "2026-05-15",
    57	                "underlying_asset": "BOVA11",
    58	                "spot_price": 198.35,
    59	                "interest_rate": 0.1175,
    60	                "volatility": 0.22,
    61	            },
    62	            "meta": {
    63	                "reference_date": reference_date or "2026-05-15",
    64	                "legs_source": "canonical",
    65	                "legacy_aba": "BOVA11",
    66	                "legacy_timestamp": None,
    67	            },
    68	        }
    69	
    70	
    71	class FakeInvalidCanonicalInputService:
    72	    def __init__(self):
    73	        self.calls = []
    74	
    75	    def build_structure_market_input(
    76	        self,
    77	        structure_id: int,
    78	        reference_date: str | None = None,
    79	    ):
    80	        self.calls.append(
    81	            {
    82	                "structure_id": structure_id,
    83	                "reference_date": reference_date,
    84	            }
    85	        )
    86	
    87	        return {
    88	            "structure": {
    89	                "structure_id": structure_id,
    90	                "name": "Estrutura inválida",
    91	                "underlying_asset": "BOVA11",
    92	                "alias_legacy_aba": "BOVA11",
    93	                "legs": [],
    94	            },
    95	            "market": {
    96	                "reference_date": reference_date or "2026-05-15",
    97	                "underlying_asset": "BOVA11",
    98	                "spot_price": 198.35,
    99	                "interest_rate": 0.1175,
   100	                "volatility": 0.22,
   101	            },
   102	            "meta": {
   103	                "reference_date": reference_date or "2026-05-15",
   104	                "legs_source": "canonical",
   105	                "legacy_aba": "BOVA11",
   106	                "legacy_timestamp": None,
   107	            },
   108	        }
   109	
   110	
   111	def test_structure_analysis_service_analyze_returns_full_pipeline():
   112	    service = StructureAnalysisService(
   113	        canonical_input_service=FakeCanonicalInputService()
   114	    )
   115	
   116	    result = service.analyze(
   117	        structure_id=1,
   118	        reference_date="2026-05-15",
   119	        spread_pct_medio=0.02,
   120	    )
   121	
   122	    assert "canonical_input" in result
   123	    assert "metrics" in result
   124	    assert "payoff" in result
   125	    assert "decision" in result
   126	
   127	    assert result["canonical_input"]["structure"]["structure_id"] == 1
   128	    assert result["canonical_input"]["market"]["reference_date"] == "2026-05-15"
   129	
   130	    assert result["metrics"]["dte_min_inferred"] == 0
   131	    assert result["metrics"]["dte_min_effective"] == 0
   132	    assert result["metrics"]["spread_pct_medio"] == 0.02
   133	
   134	    payoff = result["payoff"]
   135	    assert payoff is not None
   136	    assert payoff["pl_max"] == 10000.0
   137	    assert payoff["spot_ref"] == 198.35
   138	    assert "points" in payoff
   139	    assert len(payoff["points"]) > 0
   140	
   141	    decision = result["decision"]
   142	    assert decision is not None
   143	    assert decision["decision"] == "HOLD"
   144	    assert decision["dte_min"] == 0
   145	    assert "why" in decision
   146	    assert "why_json" in decision
   147	    assert isinstance(decision["why"], dict)
   148	    assert "reasons" in decision["why"]
   149	    assert "alternatives" in decision["why"]
   150	
   151	
   152	def test_structure_analysis_service_analyze_uses_explicit_dte_min_over_inferred():
   153	    service = StructureAnalysisService(
   154	        canonical_input_service=FakeCanonicalInputService()
   155	    )
   156	
   157	    result = service.analyze(
   158	        structure_id=1,
   159	        reference_date="2026-05-15",
   160	        dte_min=9,
   161	        spread_pct_medio=0.02,
   162	    )
   163	
   164	    assert result["metrics"]["dte_min_inferred"] == 0
   165	    assert result["metrics"]["dte_min_effective"] == 9
   166	    assert result["decision"]["dte_min"] == 9
   167	
   168	
   169	def test_structure_analysis_service_analyze_returns_structured_decision_for_invalid_payoff():
   170	    service = StructureAnalysisService(
   171	        canonical_input_service=FakeInvalidCanonicalInputService()
   172	    )
   173	
   174	    result = service.analyze(
   175	        structure_id=999,
   176	        reference_date="2026-05-15",
   177	    )
   178	
   179	    assert "payoff" in result
   180	    assert "decision" in result
   181	    assert result["decision"] is not None
   182	    assert result["decision"]["decision"] == "HOLD"
   183	    assert result["decision"]["level"] == 0
   184	    assert result["decision"]["why"]["error"] == "payoff is required"
   185	    assert "validation_errors" in result["decision"]["why"]
   186	
   187	
   188	def test_structure_analysis_service_analyze_propagates_custom_thresholds_and_dte_gate():
   189	    service = StructureAnalysisService(
   190	        canonical_input_service=FakeCanonicalInputService()
   191	    )
   192	
   193	    thresholds = {
   194	        "watch": 0.10,
   195	        "prepare": 0.20,
   196	        "close": 0.30,
   197	    }
   198	
   199	    result = service.analyze(
   200	        structure_id=1,
   201	        reference_date="2026-05-15",
   202	        thresholds=thresholds,
   203	        dte_gate=10,
   204	    )
   205	
   206	    decision = result["decision"]
   207	
   208	    assert decision is not None
   209	    assert "why" in decision
   210	    assert decision["why"]["thresholds_used"] == thresholds
   211	    assert decision["why"]["dte_gate"] == 10
   212	
   213	
   214	def test_structure_analysis_service_analyze_propagates_spread_warning():
   215	    service = StructureAnalysisService(
   216	        canonical_input_service=FakeCanonicalInputService()
   217	    )
   218	
   219	    result = service.analyze(
   220	        structure_id=1,
   221	        reference_date="2026-05-15",
   222	        spread_pct_medio=0.02,
   223	    )
   224	
   225	    assert any(
   226	        "Spread alto" in alternative
   227	        for alternative in result["decision"]["why"]["alternatives"]
   228	    )
   229	
   230	
   231	def test_structure_analysis_service_forwards_reference_date_to_canonical_service():
   232	    fake_canonical_service = FakeCanonicalInputService()
   233	    service = StructureAnalysisService(
   234	        canonical_input_service=fake_canonical_service
   235	    )
   236	
   237	    service.analyze(
   238	        structure_id=77,
   239	        reference_date="2026-06-01",
   240	    )
   241	
   242	    assert fake_canonical_service.calls == [
   243	        {
   244	            "structure_id": 77,
   245	            "reference_date": "2026-06-01",
   246	        }
   247	    ]
   248	
   249	
   250	def test_structure_analysis_service_propagates_canonical_input_service_error():
   251	    fake_canonical_service = FakeCanonicalInputService(
   252	        error=ValueError("structure not found: 404")
   253	    )
   254	    service = StructureAnalysisService(
   255	        canonical_input_service=fake_canonical_service
   256	    )
   257	
   258	    with pytest.raises(ValueError, match="structure not found: 404"):
   259	        service.analyze(structure_id=404)
   260	
   261	
   262	def test_structure_analysis_service_passes_effective_dte_to_decision(monkeypatch):
   263	    fake_canonical_service = FakeCanonicalInputService()
   264	    service = StructureAnalysisService(
   265	        canonical_input_service=fake_canonical_service
   266	    )
   267	
   268	    captured = {}
   269	
   270	    def fake_compute_dte_min_from_canonical_input(canonical_input):
   271	        return 3
   272	
   273	    def fake_compute_payoff_from_canonical_input(canonical_input):
   274	        return {"pl_max": 1.0, "spot_ref": 198.35, "points": []}
   275	
   276	    def fake_compute_decision_from_payoff(
   277	        payoff,
   278	        dte_min,
   279	        spread_pct_medio,
   280	        thresholds,
   281	        dte_gate,
   282	    ):
   283	        captured["payoff"] = payoff
   284	        captured["dte_min"] = dte_min
   285	        captured["spread_pct_medio"] = spread_pct_medio
   286	        captured["thresholds"] = thresholds
   287	        captured["dte_gate"] = dte_gate
   288	        return {
   289	            "decision": "HOLD",
   290	            "dte_min": dte_min,
   291	            "why": {},
   292	            "why_json": "{}",
   293	        }
   294	
   295	    monkeypatch.setattr(
   296	        "services.structure_analysis_service.compute_dte_min_from_canonical_input",
   297	        fake_compute_dte_min_from_canonical_input,
   298	    )
   299	    monkeypatch.setattr(
   300	        "services.structure_analysis_service.compute_payoff_from_canonical_input",
   301	        fake_compute_payoff_from_canonical_input,
   302	    )
   303	    monkeypatch.setattr(
   304	        "services.structure_analysis_service.compute_decision_from_payoff",
   305	        fake_compute_decision_from_payoff,
   306	    )
   307	
   308	    result = service.analyze(
   309	        structure_id=1,
   310	        spread_pct_medio=0.015,
   311	        thresholds={"watch": 0.1},
   312	        dte_gate=5,
   313	    )
   314	
   315	    assert captured == {
   316	        "payoff": {"pl_max": 1.0, "spot_ref": 198.35, "points": []},
   317	        "dte_min": 3,
   318	        "spread_pct_medio": 0.015,
   319	        "thresholds": {"watch": 0.1},
   320	        "dte_gate": 5,
   321	    }
   322	    assert result["metrics"]["dte_min_inferred"] == 3
   323	    assert result["metrics"]["dte_min_effective"] == 3
   324	    assert result["decision"]["dte_min"] == 3
   325	
   326	
   327	def test_structure_analysis_service_uses_zero_when_inferred_dte_is_none(monkeypatch):
   328	    fake_canonical_service = FakeCanonicalInputService()
   329	    service = StructureAnalysisService(
   330	        canonical_input_service=fake_canonical_service
   331	    )
   332	
   333	    def fake_compute_dte_min_from_canonical_input(canonical_input):
   334	        return None
   335	
   336	    def fake_compute_payoff_from_canonical_input(canonical_input):
   337	        return {"pl_max": 1.0, "spot_ref": 198.35, "points": []}
   338	
   339	    def fake_compute_decision_from_payoff(
   340	        payoff,
   341	        dte_min,
   342	        spread_pct_medio,
   343	        thresholds,
   344	        dte_gate,
   345	    ):
   346	        return {
   347	            "decision": "HOLD",
   348	            "dte_min": dte_min,
   349	            "why": {},
   350	            "why_json": "{}",
   351	        }
   352	
   353	    monkeypatch.setattr(
   354	        "services.structure_analysis_service.compute_dte_min_from_canonical_input",
   355	        fake_compute_dte_min_from_canonical_input,
   356	    )
   357	    monkeypatch.setattr(
   358	        "services.structure_analysis_service.compute_payoff_from_canonical_input",
   359	        fake_compute_payoff_from_canonical_input,
   360	    )
   361	    monkeypatch.setattr(
   362	        "services.structure_analysis_service.compute_decision_from_payoff",
   363	        fake_compute_decision_from_payoff,
   364	    )
   365	
   366	    result = service.analyze(structure_id=1)
   367	
   368	    assert result["metrics"]["dte_min_inferred"] is None
   369	    assert result["metrics"]["dte_min_effective"] == 0
   370	    assert result["decision"]["dte_min"] == 0
   371	
   372	
   373	def test_structure_analysis_service_explicit_dte_overrides_inferred_value(monkeypatch):
   374	    fake_canonical_service = FakeCanonicalInputService()
   375	    service = StructureAnalysisService(
   376	        canonical_input_service=fake_canonical_service
   377	    )
   378	
   379	    captured = {}
   380	
   381	    def fake_compute_dte_min_from_canonical_input(canonical_input):
   382	        return 2
   383	
   384	    def fake_compute_payoff_from_canonical_input(canonical_input):
   385	        return {"pl_max": 1.0, "spot_ref": 198.35, "points": []}
   386	
   387	    def fake_compute_decision_from_payoff(
   388	        payoff,
   389	        dte_min,
   390	        spread_pct_medio,
   391	        thresholds,
   392	        dte_gate,
   393	    ):
   394	        captured["dte_min"] = dte_min
   395	        return {
   396	            "decision": "HOLD",
   397	            "dte_min": dte_min,
   398	            "why": {},
   399	            "why_json": "{}",
   400	        }
   401	
   402	    monkeypatch.setattr(
   403	        "services.structure_analysis_service.compute_dte_min_from_canonical_input",
   404	        fake_compute_dte_min_from_canonical_input,
   405	    )
   406	    monkeypatch.setattr(
   407	        "services.structure_analysis_service.compute_payoff_from_canonical_input",
   408	        fake_compute_payoff_from_canonical_input,
   409	    )
   410	    monkeypatch.setattr(
   411	        "services.structure_analysis_service.compute_decision_from_payoff",
   412	        fake_compute_decision_from_payoff,
   413	    )
   414	
   415	    result = service.analyze(
   416	        structure_id=1,
   417	        dte_min=9,
   418	    )
   419	
   420	    assert captured["dte_min"] == 9
   421	    assert result["metrics"]["dte_min_inferred"] == 2
   422	    assert result["metrics"]["dte_min_effective"] == 9
   423	    assert result["decision"]["dte_min"] == 9
   424	class FakeCanonicalInputServiceWithMarketMetrics:
   425	    def __init__(self):
   426	        self.calls = []
   427	
   428	    def build_structure_market_input(
   429	        self,
   430	        structure_id: int,
   431	        reference_date: str | None = None,
   432	    ):
   433	        self.calls.append(
   434	            {
   435	                "structure_id": structure_id,
   436	                "reference_date": reference_date,
   437	            }
   438	        )
   439	
   440	        return {
   441	            "structure": {
   442	                "structure_id": structure_id,
   443	                "name": "BOVA11 Condor com Mercado",
   444	                "underlying_asset": "BOVA11",
   445	                "alias_legacy_aba": "BOVA11",
   446	                "legs": [
   447	                    {
   448	                        "position_side": "LONG",
   449	                        "option_type": "PUT",
   450	                        "symbol": "BOVAM190",
   451	                        "strike": 190.0,
   452	                        "expiration_date": "2026-05-20",
   453	                        "quantity": 10,
   454	                        "execution_price": 1.00,
   455	                        "bid": 1.20,
   456	                        "ask": 1.40,
   457	                        "delta": 0.40,
   458	                        "gamma": 0.01,
   459	                        "theta": -0.02,
   460	                        "vega": 0.03,
   461	                        "multiplier": 1.0,
   462	                    },
   463	                    {
   464	                        "position_side": "SHORT",
   465	                        "option_type": "PUT",
   466	                        "symbol": "BOVAM185",
   467	                        "strike": 185.0,
   468	                        "expiration_date": "2026-05-17",
   469	                        "quantity": 10,
   470	                        "execution_price": 1.00,
   471	                        "bid": 0.70,
   472	                        "ask": 0.80,
   473	                        "delta": 0.40,
   474	                        "gamma": 0.01,
   475	                        "theta": -0.02,
   476	                        "vega": 0.03,
   477	                        "multiplier": 1.0,
   478	                    },
   479	                ],
   480	            },
   481	            "market": {
   482	                "reference_date": reference_date or "2026-05-15",
   483	                "underlying_asset": "BOVA11",
   484	                "spot_price": 198.35,
   485	                "interest_rate": 0.1175,
   486	                "volatility": 0.22,
   487	            },
   488	            "meta": {
   489	                "reference_date": reference_date or "2026-05-15",
   490	                "legs_source": "canonical",
   491	                "legacy_aba": "BOVA11",
   492	                "legacy_timestamp": None,
   493	            },
   494	        }
   495	
   496	
   497	def test_structure_analysis_service_infers_spread_pct_medio_from_internal_metrics(monkeypatch):
   498	    service = StructureAnalysisService(
   499	        canonical_input_service=FakeCanonicalInputServiceWithMarketMetrics()
   500	    )
   501	
   502	    captured = {}
   503	
   504	    def fake_compute_payoff_from_canonical_input(canonical_input):
   505	        return {"pl_max": 1.0, "spot_ref": 198.35, "points": []}
   506	
   507	    def fake_compute_decision_from_payoff(
   508	        payoff,
   509	        dte_min,
   510	        spread_pct_medio,
   511	        thresholds,
   512	        dte_gate,
   513	    ):
   514	        captured["spread_pct_medio"] = spread_pct_medio
   515	        return {
   516	            "decision": "HOLD",
   517	            "dte_min": dte_min,
   518	            "why": {},
   519	            "why_json": "{}",
   520	        }
   521	
   522	    monkeypatch.setattr(
   523	        "services.structure_analysis_service.compute_payoff_from_canonical_input",
   524	        fake_compute_payoff_from_canonical_input,
   525	    )
   526	    monkeypatch.setattr(
   527	        "services.structure_analysis_service.compute_decision_from_payoff",
   528	        fake_compute_decision_from_payoff,
   529	    )
   530	
   531	    result = service.analyze(
   532	        structure_id=1,
   533	        reference_date="2026-05-15",
   534	    )
   535	
   536	    expected_spread_pct_medio = ((0.20 / 1.30) + (0.10 / 0.75)) / 2
   537	
   538	    assert result["metrics"]["spread_pct_medio"] == pytest.approx(expected_spread_pct_medio)
   539	    assert result["metrics"]["spread_pct_medio_inferred"] == pytest.approx(expected_spread_pct_medio)
   540	    assert captured["spread_pct_medio"] == pytest.approx(expected_spread_pct_medio)
   541	
   542	
   543	def test_structure_analysis_service_explicit_spread_pct_overrides_internal_metrics(monkeypatch):
   544	    service = StructureAnalysisService(
   545	        canonical_input_service=FakeCanonicalInputServiceWithMarketMetrics()
   546	    )
   547	
   548	    captured = {}
   549	
   550	    def fake_compute_payoff_from_canonical_input(canonical_input):
   551	        return {"pl_max": 1.0, "spot_ref": 198.35, "points": []}
   552	
   553	    def fake_compute_decision_from_payoff(
   554	        payoff,
   555	        dte_min,
   556	        spread_pct_medio,
   557	        thresholds,
   558	        dte_gate,
   559	    ):
   560	        captured["spread_pct_medio"] = spread_pct_medio
   561	        return {
   562	            "decision": "HOLD",
   563	            "dte_min": dte_min,
   564	            "why": {},
   565	            "why_json": "{}",
   566	        }
   567	
   568	    monkeypatch.setattr(
   569	        "services.structure_analysis_service.compute_payoff_from_canonical_input",
   570	        fake_compute_payoff_from_canonical_input,
   571	    )
   572	    monkeypatch.setattr(
   573	        "services.structure_analysis_service.compute_decision_from_payoff",
   574	        fake_compute_decision_from_payoff,
   575	    )
   576	
   577	    result = service.analyze(
   578	        structure_id=1,
   579	        reference_date="2026-05-15",
   580	        spread_pct_medio=0.015,
   581	    )
   582	
   583	    expected_spread_pct_medio_inferred = ((0.20 / 1.30) + (0.10 / 0.75)) / 2
   584	
   585	    assert result["metrics"]["spread_pct_medio"] == 0.015
   586	    assert result["metrics"]["spread_pct_medio_inferred"] == pytest.approx(
   587	        expected_spread_pct_medio_inferred
   588	    )
   589	    assert captured["spread_pct_medio"] == 0.015
   590	
   591	
   592	def test_structure_analysis_service_exposes_internal_structure_metrics(monkeypatch):
   593	    service = StructureAnalysisService(
   594	        canonical_input_service=FakeCanonicalInputServiceWithMarketMetrics()
   595	    )
   596	
   597	    def fake_compute_payoff_from_canonical_input(canonical_input):
   598	        return {"pl_max": 1.0, "spot_ref": 198.35, "points": []}
   599	
   600	    def fake_compute_decision_from_payoff(
   601	        payoff,
   602	        dte_min,
   603	        spread_pct_medio,
   604	        thresholds,
   605	        dte_gate,
   606	    ):
   607	        return {
   608	            "decision": "HOLD",
   609	            "dte_min": dte_min,
   610	            "why": {},
   611	            "why_json": "{}",
   612	        }
   613	
   614	    monkeypatch.setattr(
   615	        "services.structure_analysis_service.compute_payoff_from_canonical_input",
   616	        fake_compute_payoff_from_canonical_input,
   617	    )
   618	    monkeypatch.setattr(
   619	        "services.structure_analysis_service.compute_decision_from_payoff",
   620	        fake_compute_decision_from_payoff,
   621	    )
   622	
   623	    result = service.analyze(
   624	        structure_id=1,
   625	        reference_date="2026-05-15",
   626	    )
   627	
   628	    structure_metrics = result["metrics"]["structure_metrics"]
   629	
   630	    assert structure_metrics["num_pernas"] == 2
   631	    assert structure_metrics["pl_realista_total"] == pytest.approx(4.0)
   632	    assert structure_metrics["delta_liq"] == pytest.approx(0.0)
   633	    assert structure_metrics["gamma_liq"] == pytest.approx(0.0)
   634	    assert structure_metrics["theta_liq"] == pytest.approx(0.0)
   635	    assert structure_metrics["vega_liq"] == pytest.approx(0.0)
   636	    assert structure_metrics["dte_min"] == 2
   637	    assert len(structure_metrics["legs"]) == 2
```

## FILE: ATT/tests/test_derived_service.py
```python
     1	from datetime import datetime
     2	
     3	import services.derived_service as ds
     4	
     5	
     6	def test_now_iso_should_be_parseable_and_timezone_aware():
     7	    value = ds._now_iso()
     8	    parsed = datetime.fromisoformat(value)
     9	
    10	    assert parsed.tzinfo is not None
    11	
    12	
    13	def test_resolve_storage_key_should_prefer_aba_when_present():
    14	    result = ds._resolve_storage_key(
    15	        aba="BOVA11",
    16	        structure_id=7,
    17	        structure_name="BOVA11 Condor Maio/2026",
    18	        underlying_asset="BOVA11",
    19	    )
    20	
    21	    assert result == "BOVA11"
    22	
    23	
    24	def test_resolve_storage_key_should_fallback_to_structure_id():
    25	    result = ds._resolve_storage_key(
    26	        aba=None,
    27	        structure_id=7,
    28	        structure_name="BOVA11 Condor Maio/2026",
    29	        underlying_asset="BOVA11",
    30	    )
    31	
    32	    assert result == "structure:7"
    33	
    34	
    35	def test_resolve_storage_key_should_use_structure_name_when_id_missing():
    36	    result = ds._resolve_storage_key(
    37	        aba=None,
    38	        structure_id=None,
    39	        structure_name="Trava XYZ",
    40	        underlying_asset="PETR4",
    41	    )
    42	
    43	    assert result == "Trava XYZ"
    44	
    45	
    46	def test_resolve_storage_key_should_use_underlying_asset_as_last_named_key():
    47	    result = ds._resolve_storage_key(
    48	        aba=None,
    49	        structure_id=None,
    50	        structure_name=None,
    51	        underlying_asset="PETR4",
    52	    )
    53	
    54	    assert result == "PETR4"
    55	
    56	
    57	def test_resolve_storage_key_should_return_unknown_when_all_missing():
    58	    result = ds._resolve_storage_key(
    59	        aba=None,
    60	        structure_id=None,
    61	        structure_name=None,
    62	        underlying_asset=None,
    63	    )
    64	
    65	    assert result == "unknown"
    66	
    67	
    68	def test_merge_meta_should_enrich_with_canonical_identity():
    69	    result = ds._merge_meta(
    70	        meta={"origin": "test"},
    71	        structure_id=7,
    72	        structure_name="BOVA11 Condor Maio/2026",
    73	        underlying_asset="BOVA11",
    74	        reference_date="2026-05-18",
    75	        input_meta={"legs_source": "canonical"},
    76	    )
    77	
    78	    assert result["origin"] == "test"
    79	    assert result["structure_id"] == 7
    80	    assert result["structure_name"] == "BOVA11 Condor Maio/2026"
    81	    assert result["underlying_asset"] == "BOVA11"
    82	    assert result["reference_date"] == "2026-05-18"
    83	    assert result["input_meta"]["legs_source"] == "canonical"
    84	
    85	
    86	def test_save_payoff_from_canonical_payload_should_use_resolved_storage_key(monkeypatch):
    87	    captured = {}
    88	
    89	    def fake_save_payoff_curve(ref, points, spot_ref=None, meta=None, timestamp=None):
    90	        captured["aba"] = ref
    91	        captured["points"] = points
    92	        captured["spot_ref"] = spot_ref
    93	        captured["meta"] = meta
    94	        captured["timestamp"] = timestamp
    95	        return 777
    96	
    97	    monkeypatch.setattr(ds, "save_payoff_curve", fake_save_payoff_curve)
    98	
    99	    payload = {
   100	        "structure_id": 99,
   101	        "structure_name": "Iron Condor",
   102	        "underlying_asset": "PETR4",
   103	        "reference_date": "2026-05-19",
   104	        "input_meta": {"x": 1},
   105	        "meta": {"source": "test"},
   106	        "points": [{"point_spot": 10, "point_pl": 20}],
   107	        "spot_ref": 11.5,
   108	    }
   109	
   110	    result = ds.save_payoff_from_canonical_payload(payload)
   111	
   112	    assert result == 777
   113	    assert captured["aba"] == "structure:99"
   114	    assert captured["points"] == [{"point_spot": 10, "point_pl": 20}]
   115	    assert captured["spot_ref"] == 11.5
   116	    assert captured["meta"]["source"] == "test"
   117	    assert captured["meta"]["structure_id"] == 99
   118	    assert captured["meta"]["structure_name"] == "Iron Condor"
   119	    assert captured["meta"]["underlying_asset"] == "PETR4"
   120	    assert captured["meta"]["reference_date"] == "2026-05-19"
   121	    assert captured["meta"]["input_meta"] == {"x": 1}
   122	    assert captured["meta"]["storage_key"] == "structure:99"
   123	
   124	
   125	def test_save_decision_from_canonical_payload_should_enrich_meta(monkeypatch):
   126	    captured = {}
   127	
   128	    def fake_save_decision(ref, decision, timestamp=None):
   129	        captured["aba"] = ref
   130	        captured["decision"] = decision
   131	        captured["timestamp"] = timestamp
   132	        return 888
   133	
   134	    monkeypatch.setattr(ds, "save_decision", fake_save_decision)
   135	
   136	    payload = {
   137	        "action": "hold",
   138	        "meta": {"origin": "test"},
   139	    }
   140	
   141	    result = ds.save_decision_from_canonical_payload(
   142	        decision=payload,
   143	        structure_id=321,
   144	        structure_name="Fence",
   145	        underlying_asset="VALE3",
   146	        aba=None,
   147	    )
   148	
   149	    assert result == 888
   150	    assert captured["aba"] == "structure:321"
   151	    assert captured["decision"]["meta"]["origin"] == "test"
   152	    assert captured["decision"]["meta"]["structure_id"] == 321
   153	    assert captured["decision"]["meta"]["structure_name"] == "Fence"
   154	    assert captured["decision"]["meta"]["underlying_asset"] == "VALE3"
   155	    assert captured["decision"]["meta"]["storage_key"] == "structure:321"
   156	
   157	# FASE_3A4_TESTS_DERIVED_SERVICE
   158	
   159	def test_save_decision_preserva_structure_id_explicito_sem_alias(monkeypatch):
   160	    import services.derived_service as svc
   161	
   162	    captured = {}
   163	
   164	    class FakeConn:
   165	        def __enter__(self):
   166	            return self
   167	
   168	        def __exit__(self, exc_type, exc, tb):
   169	            return False
   170	
   171	    def fake_insert_structure_decision(conn, timestamp, aba, decision_dict):
   172	        captured["timestamp"] = timestamp
   173	        captured["aba"] = aba
   174	        captured["decision_dict"] = decision_dict
   175	        return 1
   176	
   177	    monkeypatch.setattr(svc, "connect_derived", lambda: FakeConn())
   178	    monkeypatch.setattr(svc, "ensure_derived_tables", lambda conn: None)
   179	    monkeypatch.setattr(svc, "_resolve_structure_id", lambda storage_key: None)
   180	    monkeypatch.setattr(svc, "insert_structure_decision", fake_insert_structure_decision)
   181	
   182	    result = svc.save_decision(
   183	        ref="structure:7",
   184	        decision={
   185	            "structure_id": 7,
   186	            "decision": "hold",
   187	            "meta": {"source": "test"},
   188	        },
   189	        timestamp="2026-06-21T00:00:00+00:00",
   190	    )
   191	
   192	    assert result == 1
   193	    assert captured["aba"] == "structure:7"
   194	    assert captured["decision_dict"]["structure_id"] == 7
   195	    assert captured["decision_dict"]["meta"]["structure_id"] == 7
   196	    assert captured["decision_dict"]["meta"]["storage_key"] == "structure:7"
```

## FILE: ATT/tests/test_orchestrator_run_methods.py
```python
     1	"""
     2	Testes para os métodos run_payoff e run_decision
     3	adicionados ao calculation_orchestrator.
     4	
     5	Estratégia: mockar o domínio para isolar o orquestrador
     6	e garantir que a tradução de CalculationRequest está correta.
     7	"""
     8	from __future__ import annotations
     9	
    10	from types import SimpleNamespace
    11	from unittest.mock import patch
    12	
    13	import pytest
    14	
    15	from services.calculation_orchestrator import (
    16	    _request_to_payoff_dict,
    17	    run_decision,
    18	    run_payoff,
    19	)
    20	
    21	
    22	# ---------------------------------------------------------------------------
    23	# Fixtures -- objetos mínimos que imitam CalculationRequest
    24	# ---------------------------------------------------------------------------
    25	
    26	def _make_leg(**kwargs):
    27	    defaults = dict(
    28	        position_side="long",
    29	        option_type="call",
    30	        strike=100.0,
    31	        expiration_date="2026-12-19",
    32	        quantity=1,
    33	        symbol="PETR4C100",
    34	        premium=3.5,
    35	        multiplier=100,
    36	        leg_order=0,
    37	        notes=None,
    38	    )
    39	    defaults.update(kwargs)
    40	    return SimpleNamespace(**defaults)
    41	
    42	
    43	def _make_request(*, spot=50.0, underlying="PETR4", legs=None):
    44	    if legs is None:
    45	        legs = [_make_leg()]
    46	
    47	    structure = SimpleNamespace(
    48	        structure_id="struct-001",
    49	        underlying_asset=underlying,
    50	        name="Teste Estrutura",
    51	        legs=legs,
    52	    )
    53	    market = SimpleNamespace(
    54	        spot_price=spot,
    55	        underlying_asset=underlying,
    56	        snapshot_timestamp="2026-06-02T00:00:00Z",
    57	        option_quotes={},
    58	        greeks={},
    59	    )
    60	    return SimpleNamespace(structure=structure, market_snapshot=market)
    61	
    62	
    63	# ---------------------------------------------------------------------------
    64	# Testes: _request_to_payoff_dict
    65	# ---------------------------------------------------------------------------
    66	
    67	class TestRequestToPayoffDict:
    68	
    69	    def test_chaves_raiz_presentes(self):
    70	        req = _make_request()
    71	        result = _request_to_payoff_dict(req)
    72	        assert set(result.keys()) == {"structure", "market", "meta"}
    73	
    74	    def test_structure_fields(self):
    75	        req = _make_request(underlying="VALE3")
    76	        s = _request_to_payoff_dict(req)["structure"]
    77	        assert s["structure_id"] == "struct-001"
    78	        assert s["underlying_asset"] == "VALE3"
    79	        assert s["name"] == "Teste Estrutura"
    80	        assert isinstance(s["legs"], list)
    81	        assert len(s["legs"]) == 1
    82	
    83	    def test_leg_fields(self):
    84	        leg = _make_leg(strike=110.0, option_type="put", position_side="short")
    85	        req = _make_request(legs=[leg])
    86	        legs = _request_to_payoff_dict(req)["structure"]["legs"]
    87	        assert legs[0]["strike"] == 110.0
    88	        assert legs[0]["option_type"] == "put"
    89	        assert legs[0]["position_side"] == "short"
    90	
    91	    def test_market_fields(self):
    92	        req = _make_request(spot=55.5)
    93	        m = _request_to_payoff_dict(req)["market"]
    94	        assert m["spot_price"] == 55.5
    95	        assert m["underlying_asset"] == "PETR4"
    96	
    97	    def test_extra_meta_propagado(self):
    98	        req = _make_request()
    99	        meta = {"source": "unit-test", "version": 2}
   100	        result = _request_to_payoff_dict(req, extra_meta=meta)
   101	        assert result["meta"] == meta
   102	
   103	    def test_meta_default_vazio(self):
   104	        req = _make_request()
   105	        result = _request_to_payoff_dict(req)
   106	        assert result["meta"] == {}
   107	
   108	    def test_multiplas_legs(self):
   109	        legs = [
   110	            _make_leg(strike=100.0, leg_order=0),
   111	            _make_leg(strike=110.0, option_type="put", leg_order=1),
   112	        ]
   113	        req = _make_request(legs=legs)
   114	        result_legs = _request_to_payoff_dict(req)["structure"]["legs"]
   115	        assert len(result_legs) == 2
   116	        assert result_legs[1]["strike"] == 110.0
   117	
   118	
   119	# ---------------------------------------------------------------------------
   120	# Testes: run_payoff
   121	# ---------------------------------------------------------------------------
   122	
   123	class TestRunPayoff:
   124	
   125	    @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input")
   126	    def test_chama_dominio_com_dict_correto(self, mock_compute):
   127	        mock_compute.return_value = {"pl_max": 500.0, "points": []}
   128	        req = _make_request(spot=50.0)
   129	
   130	        result = run_payoff(req)
   131	
   132	        assert mock_compute.called
   133	        canonical = mock_compute.call_args[0][0]
   134	        assert canonical["structure"]["structure_id"] == "struct-001"
   135	        assert canonical["market"]["spot_price"] == 50.0
   136	        assert result == {"pl_max": 500.0, "points": []}
   137	
   138	    @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input")
   139	    def test_parametros_de_range_repassados(self, mock_compute):
   140	        mock_compute.return_value = {}
   141	        req = _make_request()
   142	
   143	        run_payoff(req, low_pct=0.8, high_pct=1.2, step_pct=0.005)
   144	
   145	        _, kwargs = mock_compute.call_args
   146	        assert kwargs["low_pct"] == 0.8
   147	        assert kwargs["high_pct"] == 1.2
   148	        assert kwargs["step_pct"] == 0.005
   149	
   150	    @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input")
   151	    def test_extra_meta_repassado(self, mock_compute):
   152	        mock_compute.return_value = {}
   153	        req = _make_request()
   154	
   155	        run_payoff(req, extra_meta={"tag": "ci"})
   156	
   157	        canonical = mock_compute.call_args[0][0]
   158	        assert canonical["meta"] == {"tag": "ci"}
   159	
   160	    @patch("services.calculation_orchestrator.compute_payoff_from_canonical_input")
   161	    def test_retorna_resultado_do_dominio(self, mock_compute):
   162	        expected = {"pl_max": 1200.0, "pl_min": -300.0, "breakeven": [105.0]}
   163	        mock_compute.return_value = expected
   164	        req = _make_request()
   165	
   166	        result = run_payoff(req)
   167	
   168	        assert result is expected
   169	
   170	
   171	# ---------------------------------------------------------------------------
   172	# Testes: run_decision
   173	# ---------------------------------------------------------------------------
   174	
   175	class TestRunDecision:
   176	
   177	    @patch("services.calculation_orchestrator.compute_decision_from_contract")
   178	    def test_chama_dominio_com_contract_correto(self, mock_decide):
   179	        mock_decide.return_value = {"decision": "hold", "score": 0.7}
   180	        req = _make_request()
   181	
   182	        result = run_decision(req, pl_atual=200.0, pl_max=500.0, dte_min=10)
   183	
   184	        assert mock_decide.called
   185	        contract = mock_decide.call_args[0][0]
   186	        assert contract.pl_atual == 200.0
   187	        assert contract.pl_max == 500.0
   188	        assert contract.dte_min == 10
   189	        assert result == {"decision": "hold", "score": 0.7}
   190	
   191	    @patch("services.calculation_orchestrator.compute_decision_from_contract")
   192	    def test_payoff_dict_repassado(self, mock_decide):
   193	        mock_decide.return_value = {}
   194	        req = _make_request()
   195	        payoff = {"pl_max": 600.0, "points": [{"spot": 50, "pl": 0}]}
   196	
   197	        run_decision(req, payoff=payoff, pl_max=600.0, pl_atual=100.0)
   198	
   199	        _, kwargs = mock_decide.call_args
   200	        assert kwargs["payoff"] == payoff
   201	
   202	    @patch("services.calculation_orchestrator.compute_decision_from_contract")
   203	    def test_defaults_pl_zerados(self, mock_decide):
   204	        mock_decide.return_value = {}
   205	        req = _make_request()
   206	
   207	        run_decision(req)
   208	
   209	        contract = mock_decide.call_args[0][0]
   210	        assert contract.pl_atual == 0.0
   211	        assert contract.pl_max == 0.0
   212	        assert contract.dte_min is None
   213	
   214	    @patch("services.calculation_orchestrator.compute_decision_from_contract")
   215	    def test_dte_min_none_quando_omitido(self, mock_decide):
   216	        mock_decide.return_value = {}
   217	        req = _make_request()
   218	
   219	        run_decision(req, pl_max=300.0)
   220	
   221	        contract = mock_decide.call_args[0][0]
   222	        assert contract.dte_min is None
   223	
   224	    @patch("services.calculation_orchestrator.compute_decision_from_contract")
   225	    def test_retorna_resultado_do_dominio(self, mock_decide):
   226	        expected = {"decision": "close", "reason": "dte_gate"}
   227	        mock_decide.return_value = expected
   228	        req = _make_request()
   229	
   230	        result = run_decision(req, pl_max=100.0, pl_atual=80.0, dte_min=2)
   231	
   232	        assert result is expected
   233	
   234	
   235	# ---------------------------------------------------------------------------
   236	# Sanidade real -- sem mock
   237	# ---------------------------------------------------------------------------
   238	
   239	class TestRunPayoffIntegration:
   240	    """
   241	    Chama run_payoff sem mock.
   242	    Pula automaticamente se o domínio não estiver configurado.
   243	    """
   244	
   245	    def test_sanidade_run_payoff_call_chain(self):
   246	        pytest.importorskip("domain.payoff")
   247	
   248	        leg = _make_leg(
   249	            strike=50.0,
   250	            option_type="call",
   251	            position_side="long",
   252	            premium=2.0,
   253	            quantity=1,
   254	            multiplier=100,
   255	            expiration_date="2026-12-19",
   256	        )
   257	        req = _make_request(spot=50.0, legs=[leg])
   258	
   259	        try:
   260	            result = run_payoff(req, low_pct=0.8, high_pct=1.2, step_pct=0.05)
   261	            assert isinstance(result, dict), "run_payoff deve retornar dict"
   262	        except Exception as exc:
   263	            pytest.skip(f"Dominio indisponivel ou mal configurado: {exc}")
```

## FILE: ATT/tests/test_pricing_execution_persistence_service.py
```python
     1	from services.pricing_execution_persistence_service import (
     2	    PricingExecutionPersistenceService,
     3	)
     4	
     5	
     6	class FakePricingExecutionsRepository:
     7	    def __init__(self):
     8	        self.calls = []
     9	
    10	    def save_execution(
    11	        self,
    12	        pricing_payload,
    13	        result,
    14	        execution_status,
    15	        execution_engine,
    16	        error_message,
    17	        duration_ms,
    18	        number_of_legs,
    19	        total_quantity,
    20	        theoretical_value,
    21	    ):
    22	        self.calls.append(
    23	            {
    24	                "pricing_payload": pricing_payload,
    25	                "result": result,
    26	                "execution_status": execution_status,
    27	                "execution_engine": execution_engine,
    28	                "error_message": error_message,
    29	                "duration_ms": duration_ms,
    30	                "number_of_legs": number_of_legs,
    31	                "total_quantity": total_quantity,
    32	                "theoretical_value": theoretical_value,
    33	            }
    34	        )
    35	        return {
    36	            "id": 1,
    37	            "execution_status": execution_status,
    38	            "execution_engine": execution_engine,
    39	        }
    40	
    41	
    42	def test_persist_execution_extracts_fields_and_saves_record():
    43	    repository = FakePricingExecutionsRepository()
    44	    service = PricingExecutionPersistenceService(
    45	        pricing_executions_repository=repository,
    46	    )
    47	
    48	    pricing_payload = {
    49	        "structure_id": 123,
    50	        "reference_date": "2026-05-16",
    51	    }
    52	    result = {
    53	        "result": {
    54	            "engine": "stub",
    55	            "status": "ok",
    56	            "metrics": {
    57	                "number_of_legs": 2,
    58	                "total_quantity": 2000,
    59	            },
    60	            "valuation": {
    61	                "theoretical_value": 321.45,
    62	            },
    63	        }
    64	    }
    65	
    66	    persisted = service.persist_execution(
    67	        pricing_payload=pricing_payload,
    68	        result=result,
    69	        duration_ms=87,
    70	    )
    71	
    72	    assert repository.calls == [
    73	        {
    74	            "pricing_payload": pricing_payload,
    75	            "result": result,
    76	            "execution_status": "ok",
    77	            "execution_engine": "stub",
    78	            "error_message": None,
    79	            "duration_ms": 87,
    80	            "number_of_legs": 2,
    81	            "total_quantity": 2000,
    82	            "theoretical_value": 321.45,
    83	        }
    84	    ]
    85	    assert persisted == {
    86	        "record": {
    87	            "id": 1,
    88	            "execution_status": "ok",
    89	            "execution_engine": "stub",
    90	        }
    91	    }
    92	
    93	
    94	def test_persist_execution_accepts_none_pricing_payload_and_explicit_error_message():
    95	    repository = FakePricingExecutionsRepository()
    96	    service = PricingExecutionPersistenceService(
    97	        pricing_executions_repository=repository,
    98	    )
    99	
   100	    result = {
   101	        "result": {
   102	            "engine": "stub",
   103	            "status": "error",
   104	            "error_message": "engine internal error",
   105	            "metrics": {},
   106	            "valuation": {},
   107	        }
   108	    }
   109	
   110	    persisted = service.persist_execution(
   111	        pricing_payload=None,
   112	        result=result,
   113	        duration_ms=15,
   114	        error_message="execution failed",
   115	    )
   116	
   117	    assert repository.calls == [
   118	        {
   119	            "pricing_payload": None,
   120	            "result": result,
   121	            "execution_status": "error",
   122	            "execution_engine": "stub",
   123	            "error_message": "execution failed",
   124	            "duration_ms": 15,
   125	            "number_of_legs": None,
   126	            "total_quantity": None,
   127	            "theoretical_value": None,
   128	        }
   129	    ]
   130	    assert persisted == {
   131	        "record": {
   132	            "id": 1,
   133	            "execution_status": "error",
   134	            "execution_engine": "stub",
   135	        }
   136	    }
   137	
   138	
   139	def test_persist_execution_uses_result_error_message_when_explicit_error_not_provided():
   140	    repository = FakePricingExecutionsRepository()
   141	    service = PricingExecutionPersistenceService(
   142	        pricing_executions_repository=repository,
   143	    )
   144	
   145	    result = {
   146	        "result": {
   147	            "engine": "stub",
   148	            "status": "error",
   149	            "error_message": "engine internal error",
   150	        }
   151	    }
   152	
   153	    service.persist_execution(
   154	        pricing_payload=None,
   155	        result=result,
   156	        duration_ms=22,
   157	    )
   158	
   159	    assert repository.calls[0]["error_message"] == "engine internal error"
   160	
   161	
   162	class FakeSystemSnapshotsRepository:
   163	    def __init__(self):
   164	        self.calls = []
   165	
   166	    def create_snapshot(self, **kwargs):
   167	        self.calls.append(kwargs)
   168	        return 99
   169	
   170	
   171	class RaisingSystemSnapshotsRepository:
   172	    def create_snapshot(self, **kwargs):
   173	        raise RuntimeError("snapshot failure")
   174	
   175	
   176	def test_persist_execution_creates_system_snapshot_for_successful_execution():
   177	    repository = FakePricingExecutionsRepository()
   178	    snapshots_repository = FakeSystemSnapshotsRepository()
   179	
   180	    service = PricingExecutionPersistenceService(
   181	        pricing_executions_repository=repository,
   182	        system_snapshots_repository=snapshots_repository,
   183	    )
   184	
   185	    pricing_payload = {
   186	        "structure_id": 123,
   187	        "structure_name": "Iron Condor",
   188	        "underlying_asset": "PETR4",
   189	        "reference_date": "2026-05-16",
   190	        "spot_price": 35.50,
   191	        "interest_rate": 0.0,
   192	        "volatility": 0.0,
   193	        "meta": {
   194	            "snapshot_source": "manual",
   195	            "legs_count": 2,
   196	        },
   197	        "legs": [
   198	            {
   199	                "leg_order": 1,
   200	                "position_side": "LONG",
   201	                "option_type": "CALL",
   202	                "symbol": "PETR4C360",
   203	                "strike": 36.0,
   204	                "quantity": 100,
   205	                "premium": 1.23,
   206	            }
   207	        ],
   208	    }
   209	    result = {
   210	        "result": {
   211	            "engine": "stub",
   212	            "status": "ok",
   213	            "metrics": {
   214	                "number_of_legs": 1,
   215	                "total_quantity": 100,
   216	            },
   217	            "valuation": {
   218	                "theoretical_value": 123.45,
   219	            },
   220	            "payoff": {
   221	                "points": [],
   222	            },
   223	            "decision": {
   224	                "action": "HOLD",
   225	            },
   226	            "alerts": [
   227	                {
   228	                    "level": "info",
   229	                    "message": "ok",
   230	                }
   231	            ],
   232	        }
   233	    }
   234	
   235	    persisted = service.persist_execution(
   236	        pricing_payload=pricing_payload,
   237	        result=result,
   238	        duration_ms=87,
   239	    )
   240	
   241	    assert persisted["record"]["id"] == 1
   242	    assert persisted["snapshot_id"] == 99
   243	
   244	    assert len(snapshots_repository.calls) == 1
   245	    call = snapshots_repository.calls[0]
   246	
   247	    assert call["structure_id"] == 123
   248	    assert call["pricing_execution_id"] == 1
   249	    assert call["underlying_asset"] == "PETR4"
   250	    assert call["reference_date"] == "2026-05-16"
   251	    assert call["snapshot_source"] == "system_pricing_execution"
   252	    assert call["structure_json"]["structure_id"] == 123
   253	    assert call["market_json"]["spot_price"] == 35.50
   254	    assert call["metrics_json"] == {
   255	        "number_of_legs": 1,
   256	        "total_quantity": 100,
   257	    }
   258	    assert call["payoff_json"] == {
   259	        "points": [],
   260	    }
   261	    assert call["decision_json"] == {
   262	        "action": "HOLD",
   263	    }
   264	    assert call["alerts_json"] == [
   265	        {
   266	            "level": "info",
   267	            "message": "ok",
   268	        }
   269	    ]
   270	    assert call["legs"] == pricing_payload["legs"]
   271	
   272	
   273	def test_persist_execution_does_not_create_system_snapshot_without_pricing_payload():
   274	    repository = FakePricingExecutionsRepository()
   275	    snapshots_repository = FakeSystemSnapshotsRepository()
   276	
   277	    service = PricingExecutionPersistenceService(
   278	        pricing_executions_repository=repository,
   279	        system_snapshots_repository=snapshots_repository,
   280	    )
   281	
   282	    persisted = service.persist_execution(
   283	        pricing_payload=None,
   284	        result={
   285	            "result": {
   286	                "engine": "stub",
   287	                "status": "error",
   288	                "error_message": "failed",
   289	            }
   290	        },
   291	        duration_ms=10,
   292	        error_message="failed",
   293	    )
   294	
   295	    assert persisted == {
   296	        "record": {
   297	            "id": 1,
   298	            "execution_status": "error",
   299	            "execution_engine": "stub",
   300	        }
   301	    }
   302	    assert snapshots_repository.calls == []
   303	
   304	
   305	def test_persist_execution_does_not_create_system_snapshot_for_non_ok_status():
   306	    repository = FakePricingExecutionsRepository()
   307	    snapshots_repository = FakeSystemSnapshotsRepository()
   308	
   309	    service = PricingExecutionPersistenceService(
   310	        pricing_executions_repository=repository,
   311	        system_snapshots_repository=snapshots_repository,
   312	    )
   313	
   314	    persisted = service.persist_execution(
   315	        pricing_payload={
   316	            "structure_id": 123,
   317	            "underlying_asset": "PETR4",
   318	            "reference_date": "2026-05-16",
   319	            "legs": [],
   320	        },
   321	        result={
   322	            "result": {
   323	                "engine": "stub",
   324	                "status": "error",
   325	                "error_message": "failed",
   326	            }
   327	        },
   328	        duration_ms=10,
   329	        error_message="failed",
   330	    )
   331	
   332	    assert persisted == {
   333	        "record": {
   334	            "id": 1,
   335	            "execution_status": "error",
   336	            "execution_engine": "stub",
   337	        }
   338	    }
   339	    assert snapshots_repository.calls == []
   340	
   341	
   342	def test_persist_execution_ignores_system_snapshot_failure():
   343	    repository = FakePricingExecutionsRepository()
   344	
   345	    service = PricingExecutionPersistenceService(
   346	        pricing_executions_repository=repository,
   347	        system_snapshots_repository=RaisingSystemSnapshotsRepository(),
   348	    )
   349	
   350	    persisted = service.persist_execution(
   351	        pricing_payload={
   352	            "structure_id": 123,
   353	            "underlying_asset": "PETR4",
   354	            "reference_date": "2026-05-16",
   355	            "spot_price": 35.50,
   356	            "legs": [],
   357	        },
   358	        result={
   359	            "result": {
   360	                "engine": "stub",
   361	                "status": "ok",
   362	            }
   363	        },
   364	        duration_ms=10,
   365	    )
   366	
   367	    assert persisted == {
   368	        "record": {
   369	            "id": 1,
   370	            "execution_status": "ok",
   371	            "execution_engine": "stub",
   372	        }
   373	    }
```

## FILE: ATT/tests/test_pricing_execution_app_service.py
```python
     1	from services.pricing_execution_app_service import PricingExecutionAppService
     2	
     3	
     4	class FakeCanonicalPricingFacade:
     5	    def __init__(self, response):
     6	        self.response = response
     7	        self.calls = []
     8	
     9	    def execute_pricing(self, structure_id: int, reference_date: str | None = None):
    10	        self.calls.append({"structure_id": structure_id, "reference_date": reference_date})
    11	        return self.response
    12	
    13	
    14	class FakePricingExecutionQueryService:
    15	    def __init__(self):
    16	        self.calls = []
    17	
    18	    def list_execution_summaries(self, structure_id=None, underlying_asset=None,
    19	                                  status=None, reference_date=None, descending=True):
    20	        self.calls.append(("list_execution_summaries", {
    21	            "structure_id": structure_id, "underlying_asset": underlying_asset,
    22	            "status": status, "reference_date": reference_date, "descending": descending,
    23	        }))
    24	        return [{"id": 1}, {"id": 2}]
    25	
    26	    def get_latest_execution_summary(self, structure_id=None, underlying_asset=None,
    27	                                      status=None, reference_date=None):
    28	        self.calls.append(("get_latest_execution_summary", {
    29	            "structure_id": structure_id, "underlying_asset": underlying_asset,
    30	            "status": status, "reference_date": reference_date,
    31	        }))
    32	        return {"id": 99}
    33	
    34	    def get_execution(self, execution_id: int):
    35	        self.calls.append(("get_execution", {"execution_id": execution_id}))
    36	        return {"id": execution_id}
    37	
    38	    def paginate_execution_summaries(self, structure_id=None, underlying_asset=None,
    39	                                      status=None, reference_date=None, descending=True,
    40	                                      page=1, page_size=10):
    41	        self.calls.append(("paginate_execution_summaries", {
    42	            "structure_id": structure_id, "underlying_asset": underlying_asset,
    43	            "status": status, "reference_date": reference_date,
    44	            "descending": descending, "page": page, "page_size": page_size,
    45	        }))
    46	        return {"items": [{"id": 10}], "page": page, "page_size": page_size,
    47	                "total_items": 1, "total_pages": 1}
    48	
    49	
    50	def _make_service(response, query_service=None):
    51	    return PricingExecutionAppService(
    52	        canonical_pricing_facade=FakeCanonicalPricingFacade(response),
    53	        pricing_execution_query_service=query_service or FakePricingExecutionQueryService(),
    54	    )
    55	
    56	
    57	def test_execute_pricing_returns_persisted_record_when_present():
    58	    facade = FakeCanonicalPricingFacade(response={
    59	        "persisted": {"record": {"id": 123, "structure_id": 10, "reference_date": "2026-05-16"}}
    60	    })
    61	    service = PricingExecutionAppService(
    62	        canonical_pricing_facade=facade,
    63	        pricing_execution_query_service=FakePricingExecutionQueryService(),
    64	    )
    65	    result = service.execute_pricing(structure_id=10, reference_date="2026-05-16")
    66	    assert result == {"id": 123, "structure_id": 10, "reference_date": "2026-05-16"}
    67	    assert facade.calls == [{"structure_id": 10, "reference_date": "2026-05-16"}]
    68	
    69	
    70	def test_execute_pricing_returns_raw_response_when_persisted_record_is_missing():
    71	    raw_response = {"execution": {"status": "ok"}, "persisted": {"something_else": True}}
    72	    facade = FakeCanonicalPricingFacade(response=raw_response)
    73	    service = PricingExecutionAppService(
    74	        canonical_pricing_facade=facade,
    75	        pricing_execution_query_service=FakePricingExecutionQueryService(),
    76	    )
    77	    result = service.execute_pricing(structure_id=11, reference_date="2026-05-16")
    78	    assert result == raw_response
    79	
    80	
    81	def test_execute_pricing_rejects_invalid_structure_id():
    82	    facade = FakeCanonicalPricingFacade(response={})
    83	    service = PricingExecutionAppService(
    84	        canonical_pricing_facade=facade,
    85	        pricing_execution_query_service=FakePricingExecutionQueryService(),
    86	    )
    87	    try:
    88	        service.execute_pricing(structure_id=0, reference_date="2026-05-16")
    89	        assert False, "expected ValueError"
    90	    except ValueError as exc:
    91	        assert str(exc) == "structure_id must be greater than zero"
    92	    assert facade.calls == []
    93	
    94	
    95	def test_execute_pricing_rejects_invalid_reference_date():
    96	    facade = FakeCanonicalPricingFacade(response={})
    97	    service = PricingExecutionAppService(
    98	        canonical_pricing_facade=facade,
    99	        pricing_execution_query_service=FakePricingExecutionQueryService(),
   100	    )
   101	    try:
   102	        service.execute_pricing(structure_id=10, reference_date="16-05-2026")
   103	        assert False, "expected ValueError"
   104	    except ValueError as exc:
   105	        assert str(exc) == "reference_date must be in YYYY-MM-DD format"
   106	    assert facade.calls == []
   107	
   108	
   109	def test_execute_pricing_accepts_none_reference_date():
   110	    facade = FakeCanonicalPricingFacade(
   111	        response={"persisted": {"record": {"id": 55}}}
   112	    )
   113	    service = PricingExecutionAppService(
   114	        canonical_pricing_facade=facade,
   115	        pricing_execution_query_service=FakePricingExecutionQueryService(),
   116	    )
   117	    result = service.execute_pricing(structure_id=10, reference_date=None)
   118	    assert result == {"id": 55}
   119	    assert facade.calls == [{"structure_id": 10, "reference_date": None}]
   120	
   121	
   122	def test_list_execution_summaries_delegates_to_query_service():
   123	    query_service = FakePricingExecutionQueryService()
   124	    service = _make_service(response={}, query_service=query_service)
   125	    result = service.list_execution_summaries(
   126	        structure_id=1, underlying_asset="PETR4",
   127	        status="ok", reference_date="2026-05-16", descending=False,
   128	    )
   129	    assert result == [{"id": 1}, {"id": 2}]
   130	    assert query_service.calls[0] == ("list_execution_summaries", {
   131	        "structure_id": 1, "underlying_asset": "PETR4",
   132	        "status": "ok", "reference_date": "2026-05-16", "descending": False,
   133	    })
   134	
   135	
   136	def test_get_latest_execution_summary_delegates_to_query_service():
   137	    query_service = FakePricingExecutionQueryService()
   138	    service = _make_service(response={}, query_service=query_service)
   139	    result = service.get_latest_execution_summary(
   140	        structure_id=2, underlying_asset="VALE3",
   141	        status="error", reference_date="2026-05-15",
   142	    )
   143	    assert result == {"id": 99}
   144	    assert query_service.calls[0] == ("get_latest_execution_summary", {
   145	        "structure_id": 2, "underlying_asset": "VALE3",
   146	        "status": "error", "reference_date": "2026-05-15",
   147	    })
   148	
   149	
   150	def test_get_execution_delegates_to_query_service():
   151	    query_service = FakePricingExecutionQueryService()
   152	    service = _make_service(response={}, query_service=query_service)
   153	    result = service.get_execution(88)
   154	    assert result == {"id": 88}
   155	    assert query_service.calls[0] == ("get_execution", {"execution_id": 88})
   156	
   157	
   158	def test_paginate_execution_summaries_delegates_to_query_service():
   159	    query_service = FakePricingExecutionQueryService()
   160	    service = _make_service(response={}, query_service=query_service)
   161	    result = service.paginate_execution_summaries(
   162	        structure_id=1, underlying_asset="PETR4",
   163	        status="ok", reference_date="2026-05-16",
   164	        descending=False, page=2, page_size=5,
   165	    )
   166	    assert result == {"items": [{"id": 10}], "page": 2, "page_size": 5,
   167	                      "total_items": 1, "total_pages": 1}
   168	    assert query_service.calls[0] == ("paginate_execution_summaries", {
   169	        "structure_id": 1, "underlying_asset": "PETR4",
   170	        "status": "ok", "reference_date": "2026-05-16",
   171	        "descending": False, "page": 2, "page_size": 5,
   172	    })
```

## FILE: ATT/tests/test_pricing_execution_orchestration_service.py
```python
     1	from services.pricing_execution_orchestration_service import (
     2	    PricingExecutionOrchestrationService,
     3	)
     4	
     5	
     6	class FakePricingInputService:
     7	    def build_pricing_payload(self, structure_id: int, reference_date: str | None = None):
     8	        return {
     9	            "structure_id": structure_id,
    10	            "reference_date": reference_date,
    11	            "payload_source": "fake_input_service",
    12	        }
    13	
    14	
    15	class FakePricingExecutionService:
    16	    def __init__(self, should_raise: bool = False):
    17	        self.should_raise = should_raise
    18	        self.calls = []
    19	
    20	    def execute(self, structure_id: int, reference_date: str | None = None):
    21	        self.calls.append(
    22	            {
    23	                "structure_id": structure_id,
    24	                "reference_date": reference_date,
    25	            }
    26	        )
    27	
    28	        if self.should_raise:
    29	            raise RuntimeError("execution failed")
    30	
    31	        return {
    32	            "pricing_payload": {
    33	                "structure_id": structure_id,
    34	                "reference_date": reference_date,
    35	                "payload_source": "fake_execution_service",
    36	            },
    37	            "result": {
    38	                "engine": "stub",
    39	                "status": "ok",
    40	                "npv": 123.45,
    41	            },
    42	        }
    43	
    44	
    45	class FakePricingExecutionPersistenceService:
    46	    def __init__(self):
    47	        self.calls = []
    48	
    49	    def persist_execution(
    50	        self,
    51	        pricing_payload,
    52	        result,
    53	        duration_ms: int,
    54	        error_message: str | None = None,
    55	    ):
    56	        self.calls.append(
    57	            {
    58	                "pricing_payload": pricing_payload,
    59	                "result": result,
    60	                "duration_ms": duration_ms,
    61	                "error_message": error_message,
    62	            }
    63	        )
    64	        return {
    65	            "status": "persisted",
    66	            "duration_ms": duration_ms,
    67	            "error_message": error_message,
    68	        }
    69	
    70	
    71	def test_execute_and_persist_success():
    72	    execution_service = FakePricingExecutionService(should_raise=False)
    73	    persistence_service = FakePricingExecutionPersistenceService()
    74	
    75	    service = PricingExecutionOrchestrationService(
    76	        pricing_input_service=FakePricingInputService(),
    77	        pricing_execution_service=execution_service,
    78	        pricing_execution_persistence_service=persistence_service,
    79	    )
    80	
    81	    result = service.execute_and_persist(
    82	        structure_id=123,
    83	        reference_date="2026-05-15",
    84	    )
    85	
    86	    assert execution_service.calls == [
    87	        {
    88	            "structure_id": 123,
    89	            "reference_date": "2026-05-15",
    90	        }
    91	    ]
    92	
    93	    assert result["pricing_payload"]["structure_id"] == 123
    94	    assert result["pricing_payload"]["reference_date"] == "2026-05-15"
    95	    assert result["result"]["result"]["status"] == "ok"
    96	    assert result["persisted"]["status"] == "persisted"
    97	
    98	    persisted_call = persistence_service.calls[0]
    99	    assert persisted_call["pricing_payload"]["structure_id"] == 123
   100	    assert persisted_call["error_message"] is None
   101	    assert isinstance(persisted_call["duration_ms"], int)
   102	
   103	
   104	def test_execute_and_persist_error():
   105	    execution_service = FakePricingExecutionService(should_raise=True)
   106	    persistence_service = FakePricingExecutionPersistenceService()
   107	
   108	    service = PricingExecutionOrchestrationService(
   109	        pricing_input_service=FakePricingInputService(),
   110	        pricing_execution_service=execution_service,
   111	        pricing_execution_persistence_service=persistence_service,
   112	    )
   113	
   114	    result = service.execute_and_persist(
   115	        structure_id=999,
   116	        reference_date="2026-05-16",
   117	    )
   118	
   119	    assert execution_service.calls == [
   120	        {
   121	            "structure_id": 999,
   122	            "reference_date": "2026-05-16",
   123	        }
   124	    ]
   125	
   126	    assert result["pricing_payload"] is None
   127	    assert result["result"]["result"]["status"] == "error"
   128	    assert result["result"]["result"]["error_message"] == "execution failed"
   129	    assert result["persisted"]["status"] == "persisted"
   130	
   131	    persisted_call = persistence_service.calls[0]
   132	    assert persisted_call["pricing_payload"] is None
   133	    assert persisted_call["error_message"] == "execution failed"
   134	    assert isinstance(persisted_call["duration_ms"], int)
```

## FILE: ATT/tests/test_pricing_execution_query_service.py
```python
     1	from services.pricing_execution_query_service import PricingExecutionQueryService
     2	
     3	
     4	class FakePricingExecutionsRepository:
     5	    def __init__(self, records=None):
     6	        self.records = records or []
     7	
     8	    def list_executions(self):
     9	        return self.records
    10	
    11	    def get_execution(self, execution_id: int):
    12	        for record in self.records:
    13	            if record["id"] == execution_id:
    14	                return record
    15	        return None
    16	
    17	
    18	def make_execution(
    19	    execution_id: int,
    20	    structure_id: int = 1,
    21	    underlying_asset: str = "PETR4",
    22	    reference_date: str = "2026-05-16",
    23	    execution_status: str = "ok",
    24	    execution_engine: str = "stub-engine",
    25	    duration_ms: int = 25,
    26	    error_message: str | None = None,
    27	    number_of_legs=None,
    28	    total_quantity=None,
    29	    theoretical_value=None,
    30	    nested_number_of_legs: int = 2,
    31	    nested_total_quantity: int = 200,
    32	    nested_theoretical_value: float = 123.45,
    33	):
    34	    return {
    35	        "id": execution_id,
    36	        "created_at": f"2026-05-16T12:00:0{execution_id}Z",
    37	        "structure_id": structure_id,
    38	        "underlying_asset": underlying_asset,
    39	        "reference_date": reference_date,
    40	        "execution_engine": execution_engine,
    41	        "execution_status": execution_status,
    42	        "duration_ms": duration_ms,
    43	        "error_message": error_message,
    44	        "number_of_legs": number_of_legs,
    45	        "total_quantity": total_quantity,
    46	        "theoretical_value": theoretical_value,
    47	        "pricing_payload": {
    48	            "structure_id": structure_id,
    49	            "underlying_asset": underlying_asset,
    50	            "reference_date": reference_date,
    51	        },
    52	        "result": {
    53	            "result": {
    54	                "metrics": {
    55	                    "number_of_legs": nested_number_of_legs,
    56	                    "total_quantity": nested_total_quantity,
    57	                },
    58	                "valuation": {
    59	                    "theoretical_value": nested_theoretical_value,
    60	                },
    61	            }
    62	        },
    63	    }
    64	
    65	
    66	def test_list_executions_returns_repository_records():
    67	    records = [make_execution(1), make_execution(2)]
    68	    service = PricingExecutionQueryService(
    69	        pricing_executions_repository=FakePricingExecutionsRepository(records)
    70	    )
    71	
    72	    result = service.list_executions()
    73	
    74	    assert result == records
    75	
    76	
    77	def test_list_execution_summaries_returns_summaries_sorted_descending_by_default():
    78	    records = [make_execution(1), make_execution(3), make_execution(2)]
    79	    service = PricingExecutionQueryService(
    80	        pricing_executions_repository=FakePricingExecutionsRepository(records)
    81	    )
    82	
    83	    summaries = service.list_execution_summaries()
    84	
    85	    assert [item["id"] for item in summaries] == [3, 2, 1]
    86	
    87	
    88	def test_list_execution_summaries_can_sort_ascending():
    89	    records = [make_execution(1), make_execution(3), make_execution(2)]
    90	    service = PricingExecutionQueryService(
    91	        pricing_executions_repository=FakePricingExecutionsRepository(records)
    92	    )
    93	
    94	    summaries = service.list_execution_summaries(descending=False)
    95	
    96	    assert [item["id"] for item in summaries] == [1, 2, 3]
    97	
    98	
    99	def test_list_execution_summaries_uses_persisted_metrics_when_available():
   100	    records = [
   101	        make_execution(
   102	            1,
   103	            number_of_legs=9,
   104	            total_quantity=999,
   105	            theoretical_value=777.77,
   106	            nested_number_of_legs=2,
   107	            nested_total_quantity=200,
   108	            nested_theoretical_value=123.45,
   109	        )
   110	    ]
   111	    service = PricingExecutionQueryService(
   112	        pricing_executions_repository=FakePricingExecutionsRepository(records)
   113	    )
   114	
   115	    summaries = service.list_execution_summaries()
   116	
   117	    assert len(summaries) == 1
   118	    assert summaries[0]["number_of_legs"] == 9
   119	    assert summaries[0]["total_quantity"] == 999
   120	    assert summaries[0]["theoretical_value"] == 777.77
   121	
   122	
   123	def test_list_execution_summaries_falls_back_to_nested_result_metrics_when_persisted_are_none():
   124	    records = [
   125	        make_execution(
   126	            1,
   127	            number_of_legs=None,
   128	            total_quantity=None,
   129	            theoretical_value=None,
   130	            nested_number_of_legs=4,
   131	            nested_total_quantity=400,
   132	            nested_theoretical_value=456.78,
   133	        )
   134	    ]
   135	    service = PricingExecutionQueryService(
   136	        pricing_executions_repository=FakePricingExecutionsRepository(records)
   137	    )
   138	
   139	    summaries = service.list_execution_summaries()
   140	
   141	    assert len(summaries) == 1
   142	    assert summaries[0]["number_of_legs"] == 4
   143	    assert summaries[0]["total_quantity"] == 400
   144	    assert summaries[0]["theoretical_value"] == 456.78
   145	
   146	
   147	def test_list_execution_summaries_filters_by_structure_id():
   148	    records = [
   149	        make_execution(1, structure_id=10),
   150	        make_execution(2, structure_id=20),
   151	    ]
   152	    service = PricingExecutionQueryService(
   153	        pricing_executions_repository=FakePricingExecutionsRepository(records)
   154	    )
   155	
   156	    summaries = service.list_execution_summaries(structure_id=20)
   157	
   158	    assert len(summaries) == 1
   159	    assert summaries[0]["structure_id"] == 20
   160	    assert summaries[0]["id"] == 2
   161	
   162	
   163	def test_list_execution_summaries_filters_by_underlying_asset():
   164	    records = [
   165	        make_execution(1, underlying_asset="PETR4"),
   166	        make_execution(2, underlying_asset="VALE3"),
   167	    ]
   168	    service = PricingExecutionQueryService(
   169	        pricing_executions_repository=FakePricingExecutionsRepository(records)
   170	    )
   171	
   172	    summaries = service.list_execution_summaries(underlying_asset="VALE3")
   173	
   174	    assert len(summaries) == 1
   175	    assert summaries[0]["underlying_asset"] == "VALE3"
   176	    assert summaries[0]["id"] == 2
   177	
   178	
   179	def test_list_execution_summaries_filters_by_status():
   180	    records = [
   181	        make_execution(1, execution_status="ok"),
   182	        make_execution(2, execution_status="error"),
   183	    ]
   184	    service = PricingExecutionQueryService(
   185	        pricing_executions_repository=FakePricingExecutionsRepository(records)
   186	    )
   187	
   188	    summaries = service.list_execution_summaries(status="error")
   189	
   190	    assert len(summaries) == 1
   191	    assert summaries[0]["execution_status"] == "error"
   192	    assert summaries[0]["id"] == 2
   193	
   194	
   195	def test_list_execution_summaries_filters_by_reference_date():
   196	    records = [
   197	        make_execution(1, reference_date="2026-05-15"),
   198	        make_execution(2, reference_date="2026-05-16"),
   199	    ]
   200	    service = PricingExecutionQueryService(
   201	        pricing_executions_repository=FakePricingExecutionsRepository(records)
   202	    )
   203	
   204	    summaries = service.list_execution_summaries(reference_date="2026-05-16")
   205	
   206	    assert len(summaries) == 1
   207	    assert summaries[0]["reference_date"] == "2026-05-16"
   208	    assert summaries[0]["id"] == 2
   209	
   210	
   211	def test_list_execution_summaries_rejects_invalid_structure_id():
   212	    service = PricingExecutionQueryService(
   213	        pricing_executions_repository=FakePricingExecutionsRepository([])
   214	    )
   215	
   216	    try:
   217	        service.list_execution_summaries(structure_id=0)
   218	        assert False, "expected ValueError"
   219	    except ValueError as exc:
   220	        assert str(exc) == "structure_id must be greater than zero"
   221	
   222	
   223	def test_list_execution_summaries_rejects_empty_underlying_asset():
   224	    service = PricingExecutionQueryService(
   225	        pricing_executions_repository=FakePricingExecutionsRepository([])
   226	    )
   227	
   228	    try:
   229	        service.list_execution_summaries(underlying_asset="   ")
   230	        assert False, "expected ValueError"
   231	    except ValueError as exc:
   232	        assert str(exc) == "underlying_asset must not be empty"
   233	
   234	
   235	def test_list_execution_summaries_rejects_invalid_status():
   236	    service = PricingExecutionQueryService(
   237	        pricing_executions_repository=FakePricingExecutionsRepository([])
   238	    )
   239	
   240	    try:
   241	        service.list_execution_summaries(status="running")
   242	        assert False, "expected ValueError"
   243	    except ValueError as exc:
   244	        assert str(exc) == "status must be either 'ok' or 'error'"
   245	
   246	
   247	def test_list_execution_summaries_rejects_invalid_reference_date():
   248	    service = PricingExecutionQueryService(
   249	        pricing_executions_repository=FakePricingExecutionsRepository([])
   250	    )
   251	
   252	    try:
   253	        service.list_execution_summaries(reference_date="16-05-2026")
   254	        assert False, "expected ValueError"
   255	    except ValueError as exc:
   256	        assert str(exc) == "reference_date must be in YYYY-MM-DD format"
   257	
   258	
   259	def test_paginate_execution_summaries_returns_page_metadata_and_items():
   260	    records = [
   261	        make_execution(1),
   262	        make_execution(2),
   263	        make_execution(3),
   264	        make_execution(4),
   265	        make_execution(5),
   266	    ]
   267	    service = PricingExecutionQueryService(
   268	        pricing_executions_repository=FakePricingExecutionsRepository(records)
   269	    )
   270	
   271	    page = service.paginate_execution_summaries(page=2, page_size=2)
   272	
   273	    assert page["page"] == 2
   274	    assert page["page_size"] == 2
   275	    assert page["total_items"] == 5
   276	    assert page["total_pages"] == 3
   277	    assert [item["id"] for item in page["items"]] == [3, 2]
   278	
   279	
   280	def test_paginate_execution_summaries_returns_empty_items_when_page_exceeds_total_pages():
   281	    records = [make_execution(1), make_execution(2)]
   282	    service = PricingExecutionQueryService(
   283	        pricing_executions_repository=FakePricingExecutionsRepository(records)
   284	    )
   285	
   286	    page = service.paginate_execution_summaries(page=3, page_size=2)
   287	
   288	    assert page["page"] == 3
   289	    assert page["page_size"] == 2
   290	    assert page["total_items"] == 2
   291	    assert page["total_pages"] == 1
   292	    assert page["items"] == []
   293	
   294	
   295	def test_paginate_execution_summaries_rejects_invalid_page():
   296	    service = PricingExecutionQueryService(
   297	        pricing_executions_repository=FakePricingExecutionsRepository([])
   298	    )
   299	
   300	    try:
   301	        service.paginate_execution_summaries(page=0, page_size=10)
   302	        assert False, "expected ValueError"
   303	    except ValueError as exc:
   304	        assert str(exc) == "page must be greater than zero"
   305	
   306	
   307	def test_paginate_execution_summaries_rejects_invalid_page_size():
   308	    service = PricingExecutionQueryService(
   309	        pricing_executions_repository=FakePricingExecutionsRepository([])
   310	    )
   311	
   312	    try:
   313	        service.paginate_execution_summaries(page=1, page_size=0)
   314	        assert False, "expected ValueError"
   315	    except ValueError as exc:
   316	        assert str(exc) == "page_size must be greater than zero"
   317	
   318	
   319	def test_get_latest_execution_summary_returns_highest_id_after_filtering():
   320	    records = [
   321	        make_execution(1, execution_status="ok"),
   322	        make_execution(2, execution_status="error"),
   323	        make_execution(3, execution_status="ok"),
   324	    ]
   325	    service = PricingExecutionQueryService(
   326	        pricing_executions_repository=FakePricingExecutionsRepository(records)
   327	    )
   328	
   329	    latest = service.get_latest_execution_summary(status="ok")
   330	
   331	    assert latest["id"] == 3
   332	    assert latest["execution_status"] == "ok"
   333	
   334	
   335	def test_get_latest_execution_summary_raises_when_no_items_found():
   336	    service = PricingExecutionQueryService(
   337	        pricing_executions_repository=FakePricingExecutionsRepository([])
   338	    )
   339	
   340	    try:
   341	        service.get_latest_execution_summary()
   342	        assert False, "expected ValueError"
   343	    except ValueError as exc:
   344	        assert str(exc) == "no pricing execution summaries found"
   345	
   346	
   347	def test_get_execution_returns_record_when_found():
   348	    records = [make_execution(1), make_execution(2)]
   349	    service = PricingExecutionQueryService(
   350	        pricing_executions_repository=FakePricingExecutionsRepository(records)
   351	    )
   352	
   353	    execution = service.get_execution(2)
   354	
   355	    assert execution["id"] == 2
   356	
   357	
   358	def test_get_execution_rejects_invalid_execution_id():
   359	    service = PricingExecutionQueryService(
   360	        pricing_executions_repository=FakePricingExecutionsRepository([])
   361	    )
   362	
   363	    try:
   364	        service.get_execution(0)
   365	        assert False, "expected ValueError"
   366	    except ValueError as exc:
   367	        assert str(exc) == "execution_id must be greater than zero"
   368	
   369	
   370	def test_get_execution_raises_not_found_when_missing():
   371	    service = PricingExecutionQueryService(
   372	        pricing_executions_repository=FakePricingExecutionsRepository([])
   373	    )
   374	
   375	    try:
   376	        service.get_execution(123)
   377	        assert False, "expected ValueError"
   378	    except ValueError as exc:
   379	        assert str(exc) == "pricing execution 123 not found"
   380	
   381	
   382	def test_get_execution_details_delegates_to_get_execution():
   383	    records = [make_execution(7)]
   384	    service = PricingExecutionQueryService(
   385	        pricing_executions_repository=FakePricingExecutionsRepository(records)
   386	    )
   387	
   388	    execution = service.get_execution_details(7)
   389	
   390	    assert execution["id"] == 7
```

## FILE: ATT/tests/test_ui_data_migration.py
```python
     1	# tests/test_ui_data_migration.py
     2	import pytest
     3	import sys
     4	from pathlib import Path
     5	
     6	PROJECT_ROOT = Path(__file__).resolve().parents[2]
     7	if str(PROJECT_ROOT) not in sys.path:
     8	    sys.path.insert(0, str(PROJECT_ROOT))
     9	
    10	DB_PATH = PROJECT_ROOT / "dados" / "derived.db"
    11	from UI.models.ui_data import UIDataModel
    12	
    13	
    14	@pytest.fixture(scope="module")
    15	def model():
    16	    assert DB_PATH.exists(), (
    17	        f"\n\nBanco não encontrado!\n"
    18	        f"  Esperado     : {DB_PATH}\n"
    19	        f"  PROJECT_ROOT : {PROJECT_ROOT}\n"
    20	    )
    21	    m = UIDataModel(derived_db_path=str(DB_PATH))
    22	    m.refresh()
    23	    return m
    24	
    25	
    26	@pytest.fixture(scope="module")
    27	def decisions(model):
    28	    return model.get_decisions()
    29	
    30	
    31	@pytest.fixture(scope="module")
    32	def structures(model):
    33	    return model.get_structures()
    34	
    35	
    36	
    37	
    38	@pytest.fixture(scope="module")
    39	def non_empty_structures(structures):
    40	    if not structures:
    41	        pytest.skip("Sem estruturas no banco de migração")
    42	    return structures
    43	
    44	
    45	@pytest.fixture(scope="module")
    46	def non_empty_decisions(decisions):
    47	    if not decisions:
    48	        pytest.skip("Sem decisões no banco de migração")
    49	    return decisions
    50	
    51	# 
    52	# Sanidade -- banco acessível
    53	# 
    54	
    55	def test_db_existe():
    56	    assert DB_PATH.exists(), f"Banco não encontrado: {DB_PATH}"
    57	
    58	
    59	def test_db_project_root_correto():
    60	    assert (PROJECT_ROOT / "dados").exists(), (
    61	        f"Pasta 'dados/' não encontrada em: {PROJECT_ROOT}"
    62	    )
    63	
    64	
    65	# 
    66	# Nível 1 -- get_structures / get_abas
    67	# 
    68	
    69	def test_get_structures_retorna_lista(structures):
    70	    assert isinstance(structures, list), "get_structures() deve retornar lista"
    71	
    72	
    73	def test_get_structures_nao_vazia(non_empty_structures):
    74	    assert len(non_empty_structures) > 0, "Deve haver ao menos uma estrutura cadastrada"
    75	
    76	
    77	def test_get_abas_alias_de_get_structures(model, structures):
    78	    assert hasattr(model, "get_abas"), "get_abas() deve existir para continuidade operacional"
    79	    assert callable(model.get_abas), "get_abas() deve ser callable"
    80	    assert model.get_abas() == structures, (
    81	        "get_abas() deve retornar o mesmo que get_structures()"
    82	    )
    83	
    84	
    85	# 
    86	# Nível 2 -- get_decisions() com structure_id
    87	# 
    88	
    89	def test_decisions_nao_vazia(non_empty_decisions):
    90	    assert len(non_empty_decisions) > 0, "Deve haver ao menos uma decisão no banco"
    91	
    92	
    93	def test_decisions_tem_structure_id(decisions):
    94	    for d in decisions:
    95	        assert "structure_id" in d, f"Faltou 'structure_id' no dict: {d}"
    96	
    97	
    98	def test_decisions_tem_aba(decisions):
    99	    for d in decisions:
   100	        assert "aba" in d, f"Campo 'aba' desapareceu do dict: {d}"
   101	
   102	
   103	def test_structure_id_igual_a_aba(decisions):
   104	    """
   105	    migração structure_id: structure_id (int) e aba (ticker str) sao campos distintos.
   106	    Verificamos que structure_id e int positivo e aba e str nao-vazia.
   107	    """
   108	    for d in decisions:
   109	        assert isinstance(d["structure_id"], int), (
   110	            f"structure_id deve ser int: {d['structure_id']!r}"
   111	        )
   112	        assert d["structure_id"] > 0, (
   113	            f"structure_id deve ser positivo: {d['structure_id']}"
   114	        )
   115	        assert isinstance(d["aba"], str) and d["aba"].strip(), (
   116	            f"aba deve ser str nao-vazia: {d['aba']!r}"
   117	        )
   118	
   119	
   120	def test_decisions_tem_timestamp(decisions):
   121	    for d in decisions:
   122	        assert "timestamp" in d, f"Faltou 'timestamp' no dict: {d}"
   123	        assert d["timestamp"], "timestamp não pode ser vazio ou None"
   124	
   125	
   126	# 
   127	# Nível 3 -- Filtros
   128	# 
   129	
   130	def test_filtro_por_structure_id(model, non_empty_structures):
   131	    """
   132	    migração structure_id: structures retorna lista de str numericas; converte para int
   133	    antes de comparar com d["structure_id"] que e sempre int canonico.
   134	    """
   135	    sid_str = non_empty_structures[0]          # ex: '36'
   136	    sid_int = int(sid_str)           # 36
   137	    filtered = model.get_decisions(filters={"structure_id": sid_str})
   138	    assert isinstance(filtered, list), "Filtro deve retornar lista"
   139	    assert len(filtered) > 0, f"Filtro structure_id='{sid_str}' retornou vazio"
   140	    for d in filtered:
   141	        assert d["structure_id"] == sid_int, (
   142	            f"Decisao filtrada com structure_id errado: {d['structure_id']!r} != {sid_int}"
   143	        )
   144	
   145	
   146	def test_filtro_por_aba_continuidade(model, decisions):
   147	    """
   148	    migração structure_id: filtro por 'aba' usa ticker (ex: 'SBSP3'), nao id numerico.
   149	    Verificamos que filtrar por aba de uma decisao real retorna >= 1 resultado
   150	    e que todos os resultados tem a aba correspondente.
   151	    """
   152	    if not decisions:
   153	        pytest.skip("Sem decisoes para testar filtro por aba")
   154	    aba_real = decisions[0]["aba"]        # ex: 'SBSP3'
   155	    filtered_aba = model.get_decisions(filters={"aba": aba_real})
   156	    assert isinstance(filtered_aba, list), "Filtro aba deve retornar lista"
   157	    assert len(filtered_aba) >= 1, (
   158	        f"Filtro aba='{aba_real}' retornou vazio"
   159	    )
   160	    for d in filtered_aba:
   161	        assert d["aba"] == aba_real, (
   162	            f"Decisao com aba errada: esperado '{aba_real}', recebido '{d['aba']}'"
   163	        )
   164	
   165	
   166	# 
   167	# Nível 4 -- get_payoff_curve_info()
   168	# 
   169	
   170	def test_payoff_curve_info_retorna_dados(model, non_empty_decisions):
   171	    d0 = non_empty_decisions[0]
   172	    pts, info = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"])
   173	    assert isinstance(pts, list), "Pontos do payoff devem ser uma lista"
   174	    assert isinstance(info, dict), "info do payoff deve ser dict"
   175	
   176	
   177	def test_payoff_curve_info_tem_structure_id(model, non_empty_decisions):
   178	    d0 = non_empty_decisions[0]
   179	    _, info = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"])
   180	    assert "structure_id" in info, "info do payoff deve conter 'structure_id'"
   181	
   182	
   183	def test_payoff_curve_info_aba_continuidade(model, non_empty_decisions):
   184	    d0 = non_empty_decisions[0]
   185	    _, info = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"])
   186	    assert "aba" in info, "info do payoff deve ainda conter 'aba' (continuidade)"
   187	    assert info["aba"] == d0["structure_id"], (
   188	        f"info['aba']='{info['aba']}' != structure_id='{d0['structure_id']}'"
   189	    )
   190	
   191	
   192	def test_payoff_curve_info_pontos_validos(model, non_empty_decisions):
   193	    d0 = non_empty_decisions[0]
   194	    pts, _ = model.get_payoff_curve_info(d0["structure_id"], d0["timestamp"])
   195	    for pt in pts:
   196	        assert isinstance(pt, dict), f"Ponto deve ser dict: {pt}"
   197	        assert "spot" in pt, f"Faltou chave 'spot' no ponto: {pt}"
   198	        assert "pl" in pt, f"Faltou chave 'pl' no ponto: {pt}"
```

## FILE: ATT/tests/test_system_snapshots_repository.py
```python
     1	from __future__ import annotations
     2	
     3	import sqlite3
     4	from pathlib import Path
     5	
     6	import pytest
     7	
     8	from infra.bootstrap_structures_schema import ensure_structures_schema
     9	from repositories.system_snapshots_repository import SystemSnapshotsRepository
    10	
    11	
    12	def _insert_structure(conn: sqlite3.Connection) -> int:
    13	    cur = conn.execute(
    14	        """
    15	        INSERT INTO structures (
    16	            name,
    17	            underlying_asset,
    18	            alias_legacy_aba,
    19	            status,
    20	            notes,
    21	            created_at,
    22	            updated_at
    23	        )
    24	        VALUES (?, ?, ?, ?, ?, ?, ?)
    25	        """,
    26	        (
    27	            "Teste Snapshot",
    28	            "PETR4",
    29	            "PETR4_TESTE",
    30	            "active",
    31	            "estrutura para teste",
    32	            "2026-06-12T12:00:00Z",
    33	            "2026-06-12T12:00:00Z",
    34	        ),
    35	    )
    36	    return int(cur.lastrowid)
    37	
    38	
    39	def _insert_leg(
    40	    conn: sqlite3.Connection,
    41	    *,
    42	    structure_id: int,
    43	    leg_order: int,
    44	    symbol: str,
    45	    strike: float,
    46	) -> int:
    47	    cur = conn.execute(
    48	        """
    49	        INSERT INTO structure_legs (
    50	            structure_id,
    51	            position_side,
    52	            option_type,
    53	            symbol,
    54	            strike,
    55	            expiration_date,
    56	            quantity,
    57	            premium,
    58	            multiplier,
    59	            leg_order,
    60	            notes,
    61	            created_at,
    62	            updated_at
    63	        )
    64	        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    65	        """,
    66	        (
    67	            structure_id,
    68	            "long",
    69	            "call",
    70	            symbol,
    71	            strike,
    72	            "2026-12-18",
    73	            100,
    74	            1.25,
    75	            1,
    76	            leg_order,
    77	            None,
    78	            "2026-06-12T12:00:00Z",
    79	            "2026-06-12T12:00:00Z",
    80	        ),
    81	    )
    82	    return int(cur.lastrowid)
    83	
    84	
    85	def test_create_snapshot_persists_snapshot_and_legs(tmp_path: Path):
    86	    db_path = tmp_path / "app.db"
    87	    ensure_structures_schema(db_path)
    88	
    89	    with sqlite3.connect(db_path) as conn:
    90	        structure_id = _insert_structure(conn)
    91	        leg_1_id = _insert_leg(
    92	            conn,
    93	            structure_id=structure_id,
    94	            leg_order=1,
    95	            symbol="PETRA10",
    96	            strike=10.0,
    97	        )
    98	        leg_2_id = _insert_leg(
    99	            conn,
   100	            structure_id=structure_id,
   101	            leg_order=2,
   102	            symbol="PETRA12",
   103	            strike=12.0,
   104	        )
   105	
   106	    repo = SystemSnapshotsRepository(db_path)
   107	
   108	    snapshot_id = repo.create_snapshot(
   109	        structure_id=structure_id,
   110	        underlying_asset="PETR4",
   111	        reference_date="2026-06-12",
   112	        created_at="2026-06-12T15:00:00Z",
   113	        structure_json={
   114	            "id": structure_id,
   115	            "name": "Teste Snapshot",
   116	            "underlying_asset": "PETR4",
   117	        },
   118	        market_json={"spot": 31.25},
   119	        metrics_json={"theoretical_value": 2.5},
   120	        payoff_json={"max_gain": 1000},
   121	        decision_json={"action": "hold"},
   122	        alerts_json=[{"level": "info", "message": "ok"}],
   123	        operation_state_json={"state": "active"},
   124	        legs=[
   125	            {
   126	                "leg_id": leg_1_id,
   127	                "leg_order": 1,
   128	                "position_side": "long",
   129	                "option_type": "call",
   130	                "symbol": "PETRA10",
   131	                "strike": 10.0,
   132	                "expiration_date": "2026-12-18",
   133	                "quantity": 100,
   134	                "premium": 1.25,
   135	                "multiplier": 1,
   136	                "metrics_json": {"delta": 0.55},
   137	                "market_json": {"bid": 1.2, "ask": 1.3},
   138	            },
   139	            {
   140	                "leg_id": leg_2_id,
   141	                "leg_order": 2,
   142	                "position_side": "long",
   143	                "option_type": "call",
   144	                "symbol": "PETRA12",
   145	                "strike": 12.0,
   146	                "expiration_date": "2026-12-18",
   147	                "quantity": 100,
   148	                "premium": 0.95,
   149	                "multiplier": 1,
   150	                "metrics_json": {"delta": 0.42},
   151	                "market_json": {"bid": 0.9, "ask": 1.0},
   152	            },
   153	        ],
   154	    )
   155	
   156	    snapshot = repo.get_snapshot(snapshot_id)
   157	
   158	    assert snapshot is not None
   159	    assert snapshot["id"] == snapshot_id
   160	    assert snapshot["structure_id"] == structure_id
   161	    assert snapshot["underlying_asset"] == "PETR4"
   162	    assert snapshot["reference_date"] == "2026-06-12"
   163	    assert snapshot["snapshot_source"] == "system"
   164	    assert snapshot["structure_json"]["name"] == "Teste Snapshot"
   165	    assert snapshot["market_json"] == {"spot": 31.25}
   166	    assert snapshot["metrics_json"] == {"theoretical_value": 2.5}
   167	    assert snapshot["payoff_json"] == {"max_gain": 1000}
   168	    assert snapshot["decision_json"] == {"action": "hold"}
   169	    assert snapshot["alerts_json"] == [{"level": "info", "message": "ok"}]
   170	    assert snapshot["operation_state_json"] == {"state": "active"}
   171	
   172	    assert len(snapshot["legs"]) == 2
   173	    assert snapshot["legs"][0]["leg_id"] == leg_1_id
   174	    assert snapshot["legs"][0]["symbol"] == "PETRA10"
   175	    assert snapshot["legs"][0]["metrics_json"] == {"delta": 0.55}
   176	    assert snapshot["legs"][1]["leg_id"] == leg_2_id
   177	    assert snapshot["legs"][1]["symbol"] == "PETRA12"
   178	    assert snapshot["legs"][1]["market_json"] == {"bid": 0.9, "ask": 1.0}
   179	
   180	
   181	def test_list_snapshots_for_structure_orders_by_created_at_desc(tmp_path: Path):
   182	    db_path = tmp_path / "app.db"
   183	    ensure_structures_schema(db_path)
   184	
   185	    with sqlite3.connect(db_path) as conn:
   186	        structure_id = _insert_structure(conn)
   187	
   188	    repo = SystemSnapshotsRepository(db_path)
   189	
   190	    first_id = repo.create_snapshot(
   191	        structure_id=structure_id,
   192	        created_at="2026-06-12T10:00:00Z",
   193	        structure_json={"version": 1},
   194	    )
   195	    second_id = repo.create_snapshot(
   196	        structure_id=structure_id,
   197	        created_at="2026-06-12T11:00:00Z",
   198	        structure_json={"version": 2},
   199	    )
   200	
   201	    snapshots = repo.list_snapshots_for_structure(structure_id)
   202	
   203	    assert [snapshot["id"] for snapshot in snapshots] == [second_id, first_id]
   204	    assert snapshots[0]["structure_json"] == {"version": 2}
   205	    assert snapshots[1]["structure_json"] == {"version": 1}
   206	
   207	
   208	def test_get_latest_snapshot_for_structure_returns_snapshot_with_legs(tmp_path: Path):
   209	    db_path = tmp_path / "app.db"
   210	    ensure_structures_schema(db_path)
   211	
   212	    with sqlite3.connect(db_path) as conn:
   213	        structure_id = _insert_structure(conn)
   214	
   215	    repo = SystemSnapshotsRepository(db_path)
   216	
   217	    repo.create_snapshot(
   218	        structure_id=structure_id,
   219	        created_at="2026-06-12T10:00:00Z",
   220	        structure_json={"version": 1},
   221	    )
   222	
   223	    latest_id = repo.create_snapshot(
   224	        structure_id=structure_id,
   225	        created_at="2026-06-12T11:00:00Z",
   226	        structure_json={"version": 2},
   227	        legs=[
   228	            {
   229	                "leg_order": 1,
   230	                "position_side": "short",
   231	                "option_type": "put",
   232	                "symbol": "PETRM30",
   233	                "strike": 30.0,
   234	                "expiration_date": "2026-12-18",
   235	                "quantity": -100,
   236	                "premium": 2.1,
   237	                "multiplier": 1,
   238	            }
   239	        ],
   240	    )
   241	
   242	    latest = repo.get_latest_snapshot_for_structure(structure_id)
   243	
   244	    assert latest is not None
   245	    assert latest["id"] == latest_id
   246	    assert latest["structure_json"] == {"version": 2}
   247	    assert len(latest["legs"]) == 1
   248	    assert latest["legs"][0]["symbol"] == "PETRM30"
   249	
   250	
   251	def test_get_snapshot_returns_none_when_not_found(tmp_path: Path):
   252	    db_path = tmp_path / "app.db"
   253	
   254	    repo = SystemSnapshotsRepository(db_path)
   255	
   256	    assert repo.get_snapshot(999999) is None
   257	
   258	
   259	def test_create_snapshot_requires_structure_id_and_structure_json(tmp_path: Path):
   260	    db_path = tmp_path / "app.db"
   261	
   262	    repo = SystemSnapshotsRepository(db_path)
   263	
   264	    with pytest.raises(ValueError, match="structure_id"):
   265	        repo.create_snapshot(
   266	            structure_id=0,
   267	            structure_json={"ok": True},
   268	        )
   269	
   270	    with pytest.raises(ValueError, match="structure_json"):
   271	        repo.create_snapshot(
   272	            structure_id=1,
   273	            structure_json={},
   274	        )
```

## Coleta dos testes Fase 4
ATT/tests/test_decision.py::test_compute_decision_from_payoff_should_work_without_alias_legacy_aba
ATT/tests/test_derived_service.py::test_save_payoff_from_canonical_payload_should_use_resolved_storage_key
ATT/tests/test_derived_service.py::test_save_decision_from_canonical_payload_should_enrich_meta
ATT/tests/test_derived_service.py::test_save_decision_preserva_structure_id_explicito_sem_alias
ATT/tests/test_orchestrator_run_methods.py::TestRequestToPayoffDict::test_chaves_raiz_presentes
ATT/tests/test_orchestrator_run_methods.py::TestRequestToPayoffDict::test_structure_fields
ATT/tests/test_orchestrator_run_methods.py::TestRequestToPayoffDict::test_leg_fields
ATT/tests/test_orchestrator_run_methods.py::TestRequestToPayoffDict::test_market_fields
ATT/tests/test_orchestrator_run_methods.py::TestRequestToPayoffDict::test_extra_meta_propagado
ATT/tests/test_orchestrator_run_methods.py::TestRequestToPayoffDict::test_meta_default_vazio
ATT/tests/test_orchestrator_run_methods.py::TestRequestToPayoffDict::test_multiplas_legs
ATT/tests/test_orchestrator_run_methods.py::TestRunPayoff::test_chama_dominio_com_dict_correto
ATT/tests/test_orchestrator_run_methods.py::TestRunPayoff::test_parametros_de_range_repassados
ATT/tests/test_orchestrator_run_methods.py::TestRunPayoff::test_extra_meta_repassado
ATT/tests/test_orchestrator_run_methods.py::TestRunPayoff::test_retorna_resultado_do_dominio
ATT/tests/test_orchestrator_run_methods.py::TestRunDecision::test_chama_dominio_com_contract_correto
ATT/tests/test_orchestrator_run_methods.py::TestRunDecision::test_payoff_dict_repassado
ATT/tests/test_orchestrator_run_methods.py::TestRunDecision::test_defaults_pl_zerados
ATT/tests/test_orchestrator_run_methods.py::TestRunDecision::test_dte_min_none_quando_omitido
ATT/tests/test_orchestrator_run_methods.py::TestRunDecision::test_retorna_resultado_do_dominio
ATT/tests/test_orchestrator_run_methods.py::TestRunPayoffIntegration::test_sanidade_run_payoff_call_chain
ATT/tests/test_payoff_canonical.py::test_compute_payoff_from_canonical_input_should_preserve_canonical_metadata
ATT/tests/test_payoff_chart.py::TestFormatters::test_brl_abbrev_below_1k
ATT/tests/test_payoff_chart.py::TestFormatters::test_brl_abbrev_billions
ATT/tests/test_payoff_chart.py::TestFormatters::test_brl_abbrev_invalid
ATT/tests/test_payoff_chart.py::TestFormatters::test_brl_abbrev_millions
ATT/tests/test_payoff_chart.py::TestFormatters::test_brl_abbrev_negative
ATT/tests/test_payoff_chart.py::TestFormatters::test_brl_abbrev_thousands
ATT/tests/test_payoff_chart.py::TestFormatters::test_fmt_currency_br_basic
ATT/tests/test_payoff_chart.py::TestFormatters::test_fmt_currency_br_negative
ATT/tests/test_payoff_chart.py::TestFormatters::test_fmt_number_br_basic
ATT/tests/test_payoff_chart.py::TestFormatters::test_fmt_number_br_custom_decimals
ATT/tests/test_payoff_chart.py::TestFormatters::test_fmt_number_br_million
ATT/tests/test_payoff_chart.py::TestFormatters::test_fmt_number_br_negative
ATT/tests/test_payoff_chart.py::TestFormatters::test_fmt_number_br_zero
ATT/tests/test_payoff_chart.py::TestFindBreakevens::test_deduplication
ATT/tests/test_payoff_chart.py::TestFindBreakevens::test_empty_inputs
ATT/tests/test_payoff_chart.py::TestFindBreakevens::test_interpolated_crossing
ATT/tests/test_payoff_chart.py::TestFindBreakevens::test_mismatched_lengths
ATT/tests/test_payoff_chart.py::TestFindBreakevens::test_no_crossing
ATT/tests/test_payoff_chart.py::TestFindBreakevens::test_single_crossing_zero
ATT/tests/test_payoff_chart.py::TestFindBreakevens::test_touching_zero_without_crossing
ATT/tests/test_payoff_chart.py::TestFindBreakevens::test_two_crossings
ATT/tests/test_payoff_chart.py::TestInterpYAtX::test_empty_returns_none
ATT/tests/test_payoff_chart.py::TestInterpYAtX::test_exact_point
ATT/tests/test_payoff_chart.py::TestInterpYAtX::test_midpoint_interpolation
ATT/tests/test_payoff_chart.py::TestInterpYAtX::test_mismatched_returns_none
ATT/tests/test_payoff_chart.py::TestInterpYAtX::test_negative_ys
ATT/tests/test_payoff_chart.py::TestInterpYAtX::test_out_of_range_returns_none
ATT/tests/test_payoff_chart.py::TestInterpYAtX::test_single_segment_boundary_right
ATT/tests/test_payoff_chart.py::TestExtractXY::test_dict_pnl
ATT/tests/test_payoff_chart.py::TestExtractXY::test_dict_point_spot_point_pl
ATT/tests/test_payoff_chart.py::TestExtractXY::test_dict_spot_pl
ATT/tests/test_payoff_chart.py::TestExtractXY::test_dict_x_y
ATT/tests/test_payoff_chart.py::TestExtractXY::test_list_format
ATT/tests/test_payoff_chart.py::TestExtractXY::test_tuple_format
ATT/tests/test_payoff_chart.py::TestExtractXY::test_unknown_format_returns_none
ATT/tests/test_payoff_chart.py::TestPayoffChartState::test_clear_comparison_removes_fixed
ATT/tests/test_payoff_chart.py::TestPayoffChartState::test_clear_resets_state
ATT/tests/test_payoff_chart.py::TestPayoffChartState::test_fix_current_curve_sets_fixed
ATT/tests/test_payoff_chart.py::TestPayoffChartState::test_fix_curve_color_is_red
ATT/tests/test_payoff_chart.py::TestPayoffChartState::test_fix_curve_label
ATT/tests/test_payoff_chart.py::TestPayoffChartState::test_fix_empty_clears_fixed
ATT/tests/test_payoff_chart.py::TestPayoffChartState::test_get_last_overlays_structure
ATT/tests/test_payoff_chart.py::TestPayoffChartState::test_title_fallback_to_aba
ATT/tests/test_payoff_chart.py::TestPayoffChartState::test_title_uses_structure_id
ATT/tests/test_payoff_chart.py::TestPayoffChartState::test_update_chart_empty_returns_dict
ATT/tests/test_payoff_chart.py::TestPayoffChartState::test_update_chart_finds_breakeven
ATT/tests/test_payoff_chart.py::TestPayoffChartState::test_update_chart_no_breakeven_flat
ATT/tests/test_payoff_chart.py::TestPayoffChartState::test_update_chart_pl_at_spot_ref
ATT/tests/test_payoff_chart.py::TestPayoffChartState::test_update_chart_saves_decision_data
ATT/tests/test_payoff_chart.py::TestPayoffChartState::test_update_chart_saves_points
ATT/tests/test_payoff_chart.py::TestPayoffChartState::test_update_chart_spot_ref_none_when_missing
ATT/tests/test_payoff_chart.py::TestPayoffChartState::test_update_chart_with_list_points
ATT/tests/test_payoff_chart.py::TestPayoffChartState::test_update_chart_with_tuple_points
ATT/tests/test_payoff_chart.py::TestPayoffChartRobustness::test_find_breakevens_constant_positive
ATT/tests/test_payoff_chart.py::TestPayoffChartRobustness::test_find_breakevens_single_point
ATT/tests/test_payoff_chart.py::TestPayoffChartRobustness::test_fix_and_update_keeps_fixed_curve
ATT/tests/test_payoff_chart.py::TestPayoffChartRobustness::test_interp_same_x_values
ATT/tests/test_payoff_chart.py::TestPayoffChartRobustness::test_update_chart_all_zero_pl
ATT/tests/test_payoff_chart.py::TestPayoffChartRobustness::test_update_chart_invalid_pl_skipped
ATT/tests/test_payoff_chart.py::TestPayoffChartRobustness::test_update_chart_none_decision_data
ATT/tests/test_payoff_chart.py::TestPayoffChartRobustness::test_update_chart_single_point
ATT/tests/test_payoff_pricing_engine.py::test_run_returns_payoff_based_metrics_and_valuation
ATT/tests/test_payoff_pricing_engine.py::test_run_accepts_position_side_alias
ATT/tests/test_payoff_pricing_engine.py::test_run_raises_when_pricing_payload_is_missing
ATT/tests/test_payoff_pricing_engine.py::test_run_raises_when_legs_are_missing
ATT/tests/test_payoff_pricing_engine.py::test_run_raises_when_spot_price_is_missing
ATT/tests/test_pricing_execution_app_service.py::test_execute_pricing_returns_persisted_record_when_present
ATT/tests/test_pricing_execution_app_service.py::test_execute_pricing_returns_raw_response_when_persisted_record_is_missing
ATT/tests/test_pricing_execution_app_service.py::test_execute_pricing_rejects_invalid_structure_id
ATT/tests/test_pricing_execution_app_service.py::test_execute_pricing_rejects_invalid_reference_date
ATT/tests/test_pricing_execution_app_service.py::test_execute_pricing_accepts_none_reference_date
ATT/tests/test_pricing_execution_app_service.py::test_list_execution_summaries_delegates_to_query_service
ATT/tests/test_pricing_execution_app_service.py::test_get_latest_execution_summary_delegates_to_query_service
ATT/tests/test_pricing_execution_app_service.py::test_get_execution_delegates_to_query_service
ATT/tests/test_pricing_execution_app_service.py::test_paginate_execution_summaries_delegates_to_query_service
ATT/tests/test_pricing_execution_controller.py::test_create_pricing_execution_returns_200_and_payload
ATT/tests/test_pricing_execution_controller.py::test_create_pricing_execution_returns_404_when_value_error_contains_not_found
ATT/tests/test_pricing_execution_controller.py::test_create_pricing_execution_returns_400_for_generic_value_error
ATT/tests/test_pricing_execution_controller.py::test_list_pricing_executions_returns_paginated_response
ATT/tests/test_pricing_execution_controller.py::test_list_pricing_executions_returns_400_on_service_value_error
ATT/tests/test_pricing_execution_controller.py::test_get_latest_pricing_execution_returns_200
ATT/tests/test_pricing_execution_controller.py::test_get_latest_pricing_execution_returns_404_when_no_summary_found
ATT/tests/test_pricing_execution_controller.py::test_get_latest_pricing_execution_returns_400_for_generic_value_error
ATT/tests/test_pricing_execution_controller.py::test_get_pricing_execution_returns_200
ATT/tests/test_pricing_execution_controller.py::test_get_pricing_execution_returns_404_when_not_found
ATT/tests/test_pricing_execution_controller.py::test_get_pricing_execution_returns_400_for_generic_value_error
ATT/tests/test_pricing_execution_orchestration_service.py::test_execute_and_persist_success
ATT/tests/test_pricing_execution_orchestration_service.py::test_execute_and_persist_error
ATT/tests/test_pricing_execution_persistence_service.py::test_persist_execution_extracts_fields_and_saves_record
ATT/tests/test_pricing_execution_persistence_service.py::test_persist_execution_accepts_none_pricing_payload_and_explicit_error_message
ATT/tests/test_pricing_execution_persistence_service.py::test_persist_execution_uses_result_error_message_when_explicit_error_not_provided
ATT/tests/test_pricing_execution_persistence_service.py::test_persist_execution_creates_system_snapshot_for_successful_execution
ATT/tests/test_pricing_execution_persistence_service.py::test_persist_execution_does_not_create_system_snapshot_without_pricing_payload
ATT/tests/test_pricing_execution_persistence_service.py::test_persist_execution_does_not_create_system_snapshot_for_non_ok_status
ATT/tests/test_pricing_execution_persistence_service.py::test_persist_execution_ignores_system_snapshot_failure
ATT/tests/test_pricing_execution_query_service.py::test_list_executions_returns_repository_records
ATT/tests/test_pricing_execution_query_service.py::test_list_execution_summaries_returns_summaries_sorted_descending_by_default
ATT/tests/test_pricing_execution_query_service.py::test_list_execution_summaries_can_sort_ascending
ATT/tests/test_pricing_execution_query_service.py::test_list_execution_summaries_uses_persisted_metrics_when_available
ATT/tests/test_pricing_execution_query_service.py::test_list_execution_summaries_falls_back_to_nested_result_metrics_when_persisted_are_none
ATT/tests/test_pricing_execution_query_service.py::test_list_execution_summaries_filters_by_structure_id
ATT/tests/test_pricing_execution_query_service.py::test_list_execution_summaries_filters_by_underlying_asset
ATT/tests/test_pricing_execution_query_service.py::test_list_execution_summaries_filters_by_status
ATT/tests/test_pricing_execution_query_service.py::test_list_execution_summaries_filters_by_reference_date
ATT/tests/test_pricing_execution_query_service.py::test_list_execution_summaries_rejects_invalid_structure_id
ATT/tests/test_pricing_execution_query_service.py::test_list_execution_summaries_rejects_empty_underlying_asset
ATT/tests/test_pricing_execution_query_service.py::test_list_execution_summaries_rejects_invalid_status
ATT/tests/test_pricing_execution_query_service.py::test_list_execution_summaries_rejects_invalid_reference_date
ATT/tests/test_pricing_execution_query_service.py::test_paginate_execution_summaries_returns_page_metadata_and_items
ATT/tests/test_pricing_execution_query_service.py::test_paginate_execution_summaries_returns_empty_items_when_page_exceeds_total_pages
ATT/tests/test_pricing_execution_query_service.py::test_paginate_execution_summaries_rejects_invalid_page
ATT/tests/test_pricing_execution_query_service.py::test_paginate_execution_summaries_rejects_invalid_page_size
ATT/tests/test_pricing_execution_query_service.py::test_get_latest_execution_summary_returns_highest_id_after_filtering
ATT/tests/test_pricing_execution_query_service.py::test_get_latest_execution_summary_raises_when_no_items_found
ATT/tests/test_pricing_execution_query_service.py::test_get_execution_returns_record_when_found
ATT/tests/test_pricing_execution_query_service.py::test_get_execution_rejects_invalid_execution_id
ATT/tests/test_pricing_execution_query_service.py::test_get_execution_raises_not_found_when_missing
ATT/tests/test_pricing_execution_query_service.py::test_get_execution_details_delegates_to_get_execution
ATT/tests/test_pricing_execution_service.py::test_execute_builds_payload_and_runs_engine
ATT/tests/test_pricing_execution_service.py::test_execute_payload_runs_engine_and_returns_wrapped_result
ATT/tests/test_pricing_executions_repository.py::test_save_execution_persists_record_with_payload_and_result
ATT/tests/test_pricing_executions_repository.py::test_save_execution_accepts_none_pricing_payload
ATT/tests/test_pricing_executions_repository.py::test_save_execution_raises_when_result_is_missing
ATT/tests/test_pricing_executions_repository.py::test_list_and_get_execution_return_persisted_records
ATT/tests/test_pricing_executions_repository.py::test_get_execution_returns_none_when_not_found
ATT/tests/test_pricing_executions_repository.py::test_read_all_raises_when_storage_is_not_a_list
ATT/tests/test_structure_analysis_service.py::test_structure_analysis_service_analyze_returns_structured_decision_for_invalid_payoff
ATT/tests/test_structure_analysis_service.py::test_structure_analysis_service_passes_effective_dte_to_decision
ATT/tests/test_ui_data_migration.py::test_decisions_nao_vazia
ATT/tests/test_ui_data_migration.py::test_decisions_tem_structure_id
ATT/tests/test_ui_data_migration.py::test_decisions_tem_aba
ATT/tests/test_ui_data_migration.py::test_decisions_tem_timestamp
ATT/tests/test_ui_data_migration.py::test_payoff_curve_info_retorna_dados
ATT/tests/test_ui_data_migration.py::test_payoff_curve_info_tem_structure_id
ATT/tests/test_ui_data_migration.py::test_payoff_curve_info_aba_continuidade
ATT/tests/test_ui_data_migration.py::test_payoff_curve_info_pontos_validos

158/671 tests collected (513 deselected) in 2.60s

## Execucao dos testes Fase 4
........................................................................ [ 45%]
........................................................................ [ 91%]
..............                                                           [100%]
158 passed, 513 deselected in 3.30s
