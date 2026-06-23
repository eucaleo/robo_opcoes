# Diagnostico de bugs provaveis - Fases 3 e 4

Data: Tue Jun 23 19:55:12     2026
Branch: reinicio-normalizacao-idioma-ptbr
HEAD: 545f4e6

## Status git
?? docs/checkpoints/evidencias/fase-3-4-alvos-provaveis-correcao.txt
?? docs/checkpoints/evidencias/fase-3-4-diagnostico-bugs-provaveis.md
?? docs/checkpoints/evidencias/fase-3-contexto-cirurgico-codigo.md
?? docs/checkpoints/evidencias/fase-3-correcao-codigo-inventario.txt
?? docs/checkpoints/evidencias/fase-4-contexto-cirurgico-codigo.md
?? docs/checkpoints/evidencias/fase-4-correcao-codigo-inventario.txt
?? tools/

## Regra de classificacao
TOLERADO:
- alias_legacy_aba em repositories/structures_repository.py;
- alias_legacy_aba em UI de cadastro/lista como campo informativo/editavel;
- aba em repositórios legados de RTD/robo legs;
- testes que garantem que alias_legacy_aba NAO entra no payload canonical.

CANDIDATO A BUG FASE 3:
- qualquer fluxo manual/canonical que falhe por alias_legacy_aba nulo;
- qualquer payload de pricing que exija ou exponha alias_legacy_aba;
- qualquer montagem de input que perca structure_id;
- qualquer fallback manual tratado como excecao inesperada.

CANDIDATO A BUG FASE 4:
- payoff/decisao consultados primariamente por aba;
- persistencia de payoff/decisao sem structure_id quando ele existe;
- UI que selecione payoff/decisao por aba quando tem structure_id;
- reintroducao de get_payoff_by_aba como API publica.

## Candidatos a bug Fase 3 - raise/erro relacionado a alias
ATT/tests/test_canonical_pricing_facade_manual_without_alias.py:63:        raise ValueError(f"alias_legacy_aba is null for structure_id={structure_id}")
ATT/tests/test_canonical_pricing_facade_manual_without_alias.py:98:    assert "alias_legacy_aba is null" in response["pricing_payload"]["meta"]["fallback_reason"]
ATT/tests/test_legacy_structure_legs_reader.py:251:        match=r"structure_id=123 sem alias_legacy_aba em structures",
repositories/_aba_resolver_mixin.py:84:                    "sem alias_legacy_aba em structures",
repositories/robo_legs_repository.py:248:                f"structure_id={structure_id} sem alias_legacy_aba em structures"
repositories/robo_legs_repository.py:277:                f"structure_id={structure_id} sem alias_legacy_aba em structures"
services/canonical_pricing_facade.py:65:        raise ValueError(f"alias_legacy_aba is null for structure_id={structure_id}")
services/canonical_pricing_facade.py:387:                if "alias_legacy_aba is null" not in message:
services/legacy_robo_legs_fallback.py:107:        return None, "missing", "alias_and_name_missing"

## Candidatos a bug Fase 3 - payload canonical expondo alias
services/canonical_input_service.py:102:            "alias_legacy_aba":  self._clean_text(structure.get("alias_legacy_aba")),
services/canonical_input_service.py:154:        aba              = structure.get("alias_legacy_aba")
services/canonical_pricing_facade.py:63:    aba = row["alias_legacy_aba"]
services/canonical_pricing_facade.py:421:                meta.setdefault("alias_legacy_aba", None)

## Candidatos a bug Fase 3 - perda de structure_id em payload/input
services/calculation_orchestrator.py:86:        structure_id=int(structure_row["id"]),
services/calculation_orchestrator.py:133:            "structure_id":     request.structure.structure_id,
services/calculation_orchestrator.py:218:        "structure_id":     request.structure.structure_id,
services/calculation_orchestrator.py:279:            structure_id=int(structure_dict["structure_id"]),
services/calculation_orchestrator.py:322:                "structure_id":     request.structure.structure_id,
services/calculation_orchestrator.py:400:            "structure_id":     request.structure.structure_id,
services/calculation_orchestrator.py:410:        structure_id: int,
services/calculation_orchestrator.py:433:        structure = self._structures_repo.get_structure(structure_id)
services/calculation_orchestrator.py:436:                f"Estrutura nao encontrada: structure_id={structure_id}"
services/calculation_orchestrator.py:441:                f"structure_id={structure_id}"
services/calculation_orchestrator.py:447:                f"Estrutura sem legs: structure_id={structure_id}"
services/calculation_orchestrator.py:464:            "structure_id":    structure["id"],
services/calculation_orchestrator.py:500:        structure_id: int,
services/calculation_orchestrator.py:506:        Retorna dict com chaves: structure_id, payoff, decision.
services/calculation_orchestrator.py:509:            structure_id=structure_id,
services/calculation_orchestrator.py:515:            "structure_id": structure_id,
services/canonical_input_service.py:23:from src.domain.refs.structure_ref import StructureRef
services/canonical_input_service.py:91:        structure_id: int,
services/canonical_input_service.py:94:        structure = self.repository.get_structure(structure_id)
services/canonical_input_service.py:96:            raise ValueError(f"structure not found: {structure_id}")
services/canonical_pricing_facade.py:45:def _get_structure_info(structure_id: int, db_path: Path) -> tuple[str, str]:
services/canonical_pricing_facade.py:57:            (structure_id,),
services/canonical_pricing_facade.py:61:        raise ValueError(f"structure not found: {structure_id}")
services/canonical_pricing_facade.py:65:        raise ValueError(f"alias_legacy_aba is null for structure_id={structure_id}")
services/canonical_pricing_facade.py:237:    structure_id: int,
services/canonical_pricing_facade.py:305:        "structure_id":     structure_id,
services/canonical_pricing_facade.py:325:        structure_id
services/canonical_pricing_facade.py:353:        structure_id: int,
services/canonical_pricing_facade.py:365:            #   structures.alias_legacy_aba NULL -> PricingInputService.build_pricing_payload().
services/canonical_pricing_facade.py:370:                    structure_id,
services/canonical_pricing_facade.py:378:                    structure_id=structure_id,
services/canonical_pricing_facade.py:396:                    pricing_payload = pricing_input_service.build_pricing_payload(
services/canonical_pricing_facade.py:397:                        structure_id=structure_id,
services/canonical_pricing_facade.py:401:                    pricing_payload = pricing_input_service.build_pricing_payload(
services/canonical_pricing_facade.py:402:                        structure_id=structure_id,
services/canonical_pricing_facade.py:407:                        "PricingInputService.build_pricing_payload() retornou payload inválido"
services/canonical_pricing_facade.py:410:                pricing_payload.setdefault("structure_id", structure_id)
services/pricing_input_service.py:14:    def build_pricing_payload(
services/pricing_input_service.py:16:        structure_id: int,
services/pricing_input_service.py:20:            structure_id=structure_id,
services/pricing_input_service.py:24:        return self.build_pricing_payload_from_canonical_input(canonical_input)
services/pricing_input_service.py:26:    def build_pricing_payload_from_canonical_input(
services/structure_input_mapper.py:51:def _map_leg_to_structure_input(leg: dict[str, Any]) -> dict[str, Any]:
services/structure_input_mapper.py:85:def to_structure_input(structure: dict[str, Any]) -> dict[str, Any]:
services/structure_input_mapper.py:92:        "structure_id": structure["id"],
services/structure_input_mapper.py:96:            _map_leg_to_structure_input(leg)
services/structure_market_input_assembler.py:3:from services.structure_input_mapper import to_structure_input
services/structure_market_input_assembler.py:16:    structure_input = to_structure_input(structure)

## Candidatos a bug Fase 4 - API publica por aba
services/derived_service.py:6:alteracao_65           -- get_payoff_by_aba() removida da interface pública (standalone).
services/derived_service.py:533:# get_payoff_by_aba() removida da interface pública.
services/derived_service.py:539:    alteracao_65: get_payoff_by_aba() nao exposta -- use get_payoff_by_structure_id().
services/derived_service.py:540:    get_payoff_by_aba() ausente por decisao de design (alteracao_65): interface simplificada.
services/derived_service.py:543:    # alteracao_65: get_payoff_by_aba() deliberadamente nao implementada nesta classe.

## Candidatos a bug Fase 4 - payoff/decision usando aba na UI
UI/components/decisions_grid.py:1:# UI/components/decisions_grid.py
UI/components/decisions_grid.py:9:class DecisionsGrid(ttk.LabelFrame):
UI/components/decisions_grid.py:26:            "structure_id",
UI/components/decisions_grid.py:27:            "decision",
UI/components/decisions_grid.py:44:        self.tree.heading("structure_id", text="Estrutura")
UI/components/decisions_grid.py:45:        self.tree.heading("decision", text="Decisão")
UI/components/decisions_grid.py:54:        self.tree.column("structure_id", width=100, anchor="center")
UI/components/decisions_grid.py:55:        self.tree.column("decision", width=100, anchor="center")
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
UI/main_window.py:50:        self.last_selected_decision: Optional[Dict] = None
UI/main_window.py:57:        # Não executa pipeline e não recalcula payoff.
UI/main_window.py:84:        # Painel direito: notebook com abas
UI/main_window.py:95:        self.decisions_grid = DecisionsGrid(
UI/main_window.py:97:            on_selection_change=self.on_decision_selected,
UI/main_window.py:99:        self.decisions_grid.pack(fill="both", expand=True, padx=5, pady=5)
UI/main_window.py:105:        # Aba 1: Detalhes da Decisão
UI/main_window.py:116:        # Aba 2: Gráfico de Payoff
UI/main_window.py:118:        right_notebook.add(chart_frame, text="Curva de Payoff")
UI/main_window.py:120:        self.payoff_chart = PayoffChart(chart_frame)
UI/main_window.py:121:        self.payoff_chart.pack(fill="both", expand=True, padx=5, pady=5)
UI/main_window.py:123:        # Aba 3: Estruturas (Fase 5 -- alteracao_10)
UI/main_window.py:153:        tools_menu.add_command(label="Verificar Bancos", command=self.check_databases)
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

## Candidatos a bug Fase 4 - persistencia sem structure_id
db/derived_repo.py:4:Tabelas: payoff_curve_points, structure_decisions
db/derived_repo.py:15:  - Suporte a StructureRef como argumento aba em _extract_ts_aba e get_recent_decisions
db/derived_repo.py:21:  - fix: 5 placeholders -> 6 nos INSERTs com structure_id
db/derived_repo.py:48:def _unwrap_aba(aba_or_ref) -> str:
db/derived_repo.py:50:    alteracao_56: aceita str ou StructureRef no parâmetro 'aba'.
db/derived_repo.py:51:    Extrai .aba como string canônica quando recebe StructureRef.
db/derived_repo.py:54:    if _StructureRef is not None and isinstance(aba_or_ref, _StructureRef):
db/derived_repo.py:55:        resolved = aba_or_ref.aba
db/derived_repo.py:58:                f"StructureRef.aba é None -- use StructureRef.from_aba() ou "
db/derived_repo.py:59:                f"verifique o mapeamento. ref={aba_or_ref!r}"
db/derived_repo.py:62:    return aba_or_ref  # já é str (ou None, para wildcards)
db/derived_repo.py:74:# alteracao_36_A: adicionar structure_id ao DDL de payoff_curve_points
db/derived_repo.py:76:_DDL_PAYOFF_CURVE_POINTS = """
db/derived_repo.py:77:CREATE TABLE IF NOT EXISTS payoff_curve_points (
db/derived_repo.py:79:    aba          TEXT NOT NULL,
db/derived_repo.py:80:    structure_id INTEGER,
db/derived_repo.py:91:ON payoff_curve_points (timestamp, aba, point_spot)
db/derived_repo.py:94:# alteracao_36_B: index por structure_id para queries canônicas
db/derived_repo.py:96:CREATE INDEX IF NOT EXISTS ix_payoff_structure_id
db/derived_repo.py:97:ON payoff_curve_points (structure_id, timestamp)
db/derived_repo.py:104:    aba           TEXT    NOT NULL,
db/derived_repo.py:116:    structure_id  INTEGER
db/derived_repo.py:122:ON structure_decisions (timestamp, aba)
db/derived_repo.py:125:_DDL_DECISIONS_IDX_ABA = """
db/derived_repo.py:126:CREATE INDEX IF NOT EXISTS idx_decisions_aba_ts
db/derived_repo.py:127:ON structure_decisions (aba, timestamp)
db/derived_repo.py:137:    "structure_id": (
db/derived_repo.py:138:        "ALTER TABLE payoff_curve_points ADD COLUMN structure_id INTEGER"
db/derived_repo.py:173:    conn.execute(_DDL_PAYOFF_CURVE_POINTS)
db/derived_repo.py:177:    # alteracao_36_A: migration incremental payoff_curve_points
db/derived_repo.py:178:    existing_cols = _table_columns(conn, "payoff_curve_points")
db/derived_repo.py:186:    # alteracao_36_B: index structure_id no payoff (após migration)
db/derived_repo.py:194:    conn.execute(_DDL_DECISIONS_IDX_ABA)
db/derived_repo.py:216:    alteracao_34: assinaturas alinhadas com o smoke 70 (decision_dict auto-extrai timestamp/aba).
db/derived_repo.py:217:    alteracao_55: suporte a StructureRef como argumento aba.
db/derived_repo.py:257:    def _extract_ts_aba(
db/derived_repo.py:260:        aba: Optional[str] = None,
db/derived_repo.py:263:        Extrai timestamp e aba do dict ou dos parâmetros explícitos.
db/derived_repo.py:264:        Permite tanto a API nova (só dict) quanto a legada (ts, aba, dict).
db/derived_repo.py:267:        if _StructureRef is not None and isinstance(aba, _StructureRef):
db/derived_repo.py:268:            _ref = aba
db/derived_repo.py:269:            aba = _ref.aba
db/derived_repo.py:270:            if _ref.structure_id is not None:
db/derived_repo.py:272:                decision_dict["structure_id"] = _ref.structure_id
db/derived_repo.py:275:        ab = aba       or decision_dict.get("aba")       or decision_dict.get("ticker", "unknown")
db/derived_repo.py:286:        aba: Optional[str] = None,
db/derived_repo.py:290:        API canônica: timestamp e aba extraídos do dict se não passados.
db/derived_repo.py:293:        ts, ab = self._extract_ts_aba(decision_dict, timestamp, aba)
db/derived_repo.py:298:                "DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",
db/derived_repo.py:311:        aba: Optional[str] = None,
db/derived_repo.py:315:        API canônica: timestamp e aba extraídos do dict se não passados.
db/derived_repo.py:318:        ts, ab = self._extract_ts_aba(decision_dict, timestamp, aba)
db/derived_repo.py:336:        aba: Optional[str] = None,
db/derived_repo.py:338:        structure_id: Optional[int] = None,
db/derived_repo.py:342:        timestamp e aba podem ser passados explicitamente ou via meta dict.
db/derived_repo.py:346:        ab  = aba          or (meta or {}).get("aba")          or "unknown"
db/derived_repo.py:347:        sid = structure_id or (meta or {}).get("structure_id")
db/derived_repo.py:354:                "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",
db/derived_repo.py:359:                INSERT INTO payoff_curve_points
db/derived_repo.py:360:                    (timestamp, aba, structure_id, point_spot, point_pl, meta_json)
db/derived_repo.py:386:        aba: Optional[str] = None,
db/derived_repo.py:389:        structure_id: Optional[int] = None,
db/derived_repo.py:391:        """INSERT OR REPLACE idempotente por (timestamp, aba, point_spot)."""
db/derived_repo.py:393:        ab  = aba          or (meta or {}).get("aba")          or "unknown"
db/derived_repo.py:394:        sid = structure_id or (meta or {}).get("structure_id")
db/derived_repo.py:402:                INSERT OR REPLACE INTO payoff_curve_points
db/derived_repo.py:403:                    (timestamp, aba, structure_id, point_spot, point_pl, meta_json)
db/derived_repo.py:434:        aba: Optional[str] = None,
db/derived_repo.py:438:        ts, ab = self._extract_ts_aba(decision_dict, timestamp, aba)
db/derived_repo.py:439:        sid = decision_dict.get("structure_id")
db/derived_repo.py:448:                "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",
db/derived_repo.py:453:                INSERT INTO payoff_curve_points
db/derived_repo.py:454:                    (timestamp, aba, structure_id, point_spot, point_pl, meta_json)
db/derived_repo.py:474:                "DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",
db/derived_repo.py:490:        aba: Optional[str] = None,
db/derived_repo.py:496:            if aba and timestamp:
db/derived_repo.py:499:                    SELECT timestamp, aba, point_spot, point_pl, meta_json
db/derived_repo.py:500:                    FROM payoff_curve_points
db/derived_repo.py:501:                    WHERE aba = ? AND timestamp = ?
db/derived_repo.py:504:                    (aba, timestamp),
db/derived_repo.py:506:            elif aba:
db/derived_repo.py:509:                    SELECT timestamp, aba, point_spot, point_pl, meta_json
db/derived_repo.py:510:                    FROM payoff_curve_points
db/derived_repo.py:511:                    WHERE aba = ?
db/derived_repo.py:515:                    (aba,),
db/derived_repo.py:520:                    SELECT timestamp, aba, point_spot, point_pl, meta_json
db/derived_repo.py:521:                    FROM payoff_curve_points
db/derived_repo.py:533:        aba: Optional[str] = None,
db/derived_repo.py:534:        structure_id: Optional[int] = None,
db/derived_repo.py:539:        if _StructureRef is not None and isinstance(aba, _StructureRef):
db/derived_repo.py:540:            if structure_id is None and aba.structure_id is not None:
db/derived_repo.py:541:                structure_id = aba.structure_id
db/derived_repo.py:542:            aba = aba.aba
db/derived_repo.py:549:            if aba is not None:
db/derived_repo.py:550:                conditions.append("aba = ?")
db/derived_repo.py:551:                params.append(aba)
db/derived_repo.py:552:            if structure_id is not None:
db/derived_repo.py:553:                conditions.append("structure_id = ?")
db/derived_repo.py:554:                params.append(structure_id)
db/derived_repo.py:555:            if ticker is not None and aba is None:
db/derived_repo.py:556:                conditions.append("aba = ?")
db/derived_repo.py:578:                SELECT d.aba, d.timestamp, COUNT(p.point_spot) as point_count
db/derived_repo.py:580:                LEFT JOIN payoff_curve_points p
db/derived_repo.py:581:                       ON (d.aba = p.aba AND d.timestamp = p.timestamp)
db/derived_repo.py:582:                GROUP BY d.aba, d.timestamp
db/derived_repo.py:587:                SELECT p.aba, p.timestamp, COUNT(DISTINCT p.point_spot)
db/derived_repo.py:588:                FROM payoff_curve_points p
db/derived_repo.py:590:                       ON (p.aba = d.aba AND p.timestamp = d.timestamp)
db/derived_repo.py:591:                WHERE d.aba IS NULL
db/derived_repo.py:592:                GROUP BY p.aba, p.timestamp
db/derived_repo.py:611:                f"DELETE FROM payoff_curve_points "
db/derived_repo.py:639:        aba: str,
db/derived_repo.py:649:                (timestamp, aba, decision, level, pl_atual, pl_max, pl_pct_of_max,
db/derived_repo.py:650:                 dte_min, why, why_json, spot_ref, meta_json, structure_id)
db/derived_repo.py:655:                aba,
db/derived_repo.py:666:                decision_dict.get("structure_id"),
db/derived_repo.py:679:    aba: str,
db/derived_repo.py:682:    structure_id: Optional[int] = None,
db/derived_repo.py:685:    if structure_id is None and isinstance(meta, dict):
db/derived_repo.py:686:        structure_id = meta.get("structure_id") or meta.get("payload_structure_id")
db/derived_repo.py:688:    aba = _unwrap_aba(aba)
db/derived_repo.py:691:        "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",
db/derived_repo.py:692:        (aba, timestamp),
db/derived_repo.py:695:        INSERT INTO payoff_curve_points
db/derived_repo.py:696:            (timestamp, aba, structure_id, point_spot, point_pl, meta_json)
db/derived_repo.py:711:        cur.execute(sql, (timestamp, aba, structure_id, x, y, meta_json))
db/derived_repo.py:719:    aba: str,
db/derived_repo.py:723:    aba = _unwrap_aba(aba)
db/derived_repo.py:726:        "DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",
db/derived_repo.py:727:        (aba, timestamp),
db/derived_repo.py:733:            (timestamp, aba, decision, level, pl_atual, pl_max, pl_pct_of_max,
db/derived_repo.py:734:             dte_min, why, why_json, spot_ref, meta_json, created_at, structure_id)
db/derived_repo.py:737:        timestamp, aba,
db/derived_repo.py:748:        decision_dict.get("structure_id"),
db/derived_repo.py:756:    aba: str,
db/derived_repo.py:762:    aba = _unwrap_aba(aba)
db/derived_repo.py:764:        pc  = write_payoff_snapshot_atomic(conn, timestamp, aba, points, points_meta, structure_id=decision_dict.get("structure_id"))
db/derived_repo.py:765:        did = write_decision_snapshot_atomic(conn, timestamp, aba, decision_dict)
db/derived_repo.py:772:    aba: str,
db/derived_repo.py:776:    structure_id: Optional[int] = None,
db/derived_repo.py:779:    if structure_id is None and isinstance(meta, dict):
db/derived_repo.py:780:        structure_id = meta.get("structure_id") or meta.get("payload_structure_id")
db/derived_repo.py:781:    aba = _unwrap_aba(aba)
db/derived_repo.py:785:        INSERT OR REPLACE INTO payoff_curve_points
db/derived_repo.py:786:            (timestamp, aba, structure_id, point_spot, point_pl, meta_json)
db/derived_repo.py:801:        cur.execute(sql, (timestamp, aba, structure_id, x, y, meta_json))
db/derived_repo.py:810:    aba: str,
db/derived_repo.py:814:    aba = _unwrap_aba(aba)
db/derived_repo.py:820:            (timestamp, aba, decision, level, pl_atual, pl_max, pl_pct_of_max,
db/derived_repo.py:821:             dte_min, why, why_json, spot_ref, meta_json, created_at, structure_id)
db/derived_repo.py:824:        timestamp, aba,
db/derived_repo.py:835:        decision_dict.get("structure_id"),
db/derived_repo.py:843:    aba: Optional[str] = None,
db/derived_repo.py:847:    aba = _unwrap_aba(aba)
db/derived_repo.py:849:    if aba and timestamp:
db/derived_repo.py:851:            SELECT timestamp, aba, point_spot, point_pl, meta_json
db/derived_repo.py:852:            FROM payoff_curve_points
db/derived_repo.py:853:            WHERE aba = ? AND timestamp = ?
db/derived_repo.py:855:        """, (aba, timestamp))
db/derived_repo.py:856:    elif aba:
db/derived_repo.py:858:            SELECT timestamp, aba, point_spot, point_pl, meta_json
db/derived_repo.py:859:            FROM payoff_curve_points
db/derived_repo.py:860:            WHERE aba = ?
db/derived_repo.py:863:        """, (aba,))
db/derived_repo.py:866:            SELECT timestamp, aba, point_spot, point_pl, meta_json
db/derived_repo.py:867:            FROM payoff_curve_points
db/derived_repo.py:879:        SELECT d.aba, d.timestamp, COUNT(p.point_spot) as point_count
db/derived_repo.py:881:        LEFT JOIN payoff_curve_points p ON (d.aba = p.aba AND d.timestamp = p.timestamp)
db/derived_repo.py:882:        GROUP BY d.aba, d.timestamp
db/derived_repo.py:887:        SELECT p.aba, p.timestamp, COUNT(DISTINCT p.point_spot)
db/derived_repo.py:888:        FROM payoff_curve_points p
db/derived_repo.py:889:        LEFT JOIN structure_decisions d ON (p.aba = d.aba AND p.timestamp = d.timestamp)
db/derived_repo.py:890:        WHERE d.aba IS NULL
db/derived_repo.py:891:        GROUP BY p.aba, p.timestamp
db/derived_repo.py:909:        DELETE FROM payoff_curve_points
db/import_excel.py:29:        "ABA": "aba",
db/import_excel.py:93:        # em algumas abas pode ter linhas totalmente vazias
db/migrations/add_structure_id_to_payoff_curve_points.py:1:# db/migrations/add_structure_id_to_payoff_curve_points.py
db/migrations/add_structure_id_to_payoff_curve_points.py:3:Migration: adiciona structure_id em payoff_curve_points
db/migrations/add_structure_id_to_payoff_curve_points.py:7:    python db/migrations/add_structure_id_to_payoff_curve_points.py
db/migrations/add_structure_id_to_payoff_curve_points.py:8:    python db/migrations/add_structure_id_to_payoff_curve_points.py --db dados/derived.db
db/migrations/add_structure_id_to_payoff_curve_points.py:18:    #  payoff_curve_points 
db/migrations/add_structure_id_to_payoff_curve_points.py:20:        "payoff_curve_points: verificar se structure_id já existe",
db/migrations/add_structure_id_to_payoff_curve_points.py:21:        None,  # tratado especialmente abaixo
db/migrations/add_structure_id_to_payoff_curve_points.py:24:        "payoff_curve_points: ADD COLUMN structure_id",
db/migrations/add_structure_id_to_payoff_curve_points.py:25:        "ALTER TABLE payoff_curve_points ADD COLUMN structure_id INTEGER",
db/migrations/add_structure_id_to_payoff_curve_points.py:28:        "payoff_curve_points: BACKFILL structure_id",
db/migrations/add_structure_id_to_payoff_curve_points.py:30:        UPDATE payoff_curve_points
db/migrations/add_structure_id_to_payoff_curve_points.py:31:        SET structure_id = (
db/migrations/add_structure_id_to_payoff_curve_points.py:32:            SELECT d.structure_id
db/migrations/add_structure_id_to_payoff_curve_points.py:34:            WHERE d.aba       = payoff_curve_points.aba
db/migrations/add_structure_id_to_payoff_curve_points.py:35:              AND d.timestamp = payoff_curve_points.timestamp
db/migrations/add_structure_id_to_payoff_curve_points.py:41:        "payoff_curve_points: CREATE INDEX sid+ts",
db/migrations/add_structure_id_to_payoff_curve_points.py:44:            ON payoff_curve_points (structure_id, timestamp)
db/migrations/add_structure_id_to_payoff_curve_points.py:49:        "payoff_curve_summary: ADD COLUMN structure_id",
db/migrations/add_structure_id_to_payoff_curve_points.py:50:        "ALTER TABLE payoff_curve_summary ADD COLUMN structure_id INTEGER",
db/migrations/add_structure_id_to_payoff_curve_points.py:53:        "payoff_curve_summary: BACKFILL structure_id",
db/migrations/add_structure_id_to_payoff_curve_points.py:56:        SET structure_id = (
db/migrations/add_structure_id_to_payoff_curve_points.py:57:            SELECT d.structure_id
db/migrations/add_structure_id_to_payoff_curve_points.py:59:            WHERE d.aba       = payoff_curve_summary.aba
db/migrations/add_structure_id_to_payoff_curve_points.py:69:            ON payoff_curve_summary (structure_id, timestamp)
db/migrations/add_structure_id_to_payoff_curve_points.py:92:                if "ADD COLUMN structure_id" in (sql or ""):
db/migrations/add_structure_id_to_payoff_curve_points.py:94:                    if col_exists(conn, table, "structure_id"):
db/migrations/add_structure_id_to_payoff_curve_points.py:106:        for table in ("payoff_curve_points", "payoff_curve_summary"):
db/migrations/add_structure_id_to_payoff_curve_points.py:109:                f"COUNT(structure_id) AS filled "
db/migrations/add_structure_id_to_payoff_curve_points.py:115:        print("\n[OK] Migration de structure_id aplicada com sucesso.")
db/reader.py:47:            aba: Nome da aba/estratégia
db/reader.py:58:                    FROM payoff_curve_points
db/reader.py:62:                params = (aba, timestamp)
db/reader.py:67:                    FROM payoff_curve_points
db/reader.py:69:                        SELECT MAX(timestamp) FROM payoff_curve_points WHERE {ref.db_column()} = ?
db/reader.py:73:                params = (aba, aba)
db/reader.py:90:            aba: Nome da aba/estratégia
db/reader.py:134:            df = pd.read_sql_query(query, conn, params=(aba, cutoff_date))
db/schema.py:7:CREATE TABLE IF NOT EXISTS payoff_curve_points (
db/schema.py:10:    aba TEXT NOT NULL,
db/schema.py:18:CREATE INDEX IF NOT EXISTS idx_payoff_timestamp_aba
db/schema.py:19:ON payoff_curve_points(timestamp, aba);
db/schema.py:22:ON payoff_curve_points(point_spot);
db/schema.py:28:    aba TEXT NOT NULL,
db/schema.py:45:CREATE INDEX IF NOT EXISTS idx_decisions_timestamp_aba
db/schema.py:46:ON structure_decisions(timestamp, aba);
db/schema.py:73:    structure_id   INTEGER NOT NULL,
db/schema.py:86:    FOREIGN KEY (structure_id) REFERENCES structures(id) ON DELETE CASCADE,
db/schema.py:90:CREATE INDEX IF NOT EXISTS idx_structure_events_structure_id
db/schema.py:91:ON structure_events(structure_id);
db/schema.py:106:ON structure_events(structure_id, event_date);
db/schema_excel.py:16:-- Snapshot agregado por ABA (ANALISE_ROBO)
db/schema_excel.py:19:  timestamp TEXT,                -- opcional (se você tiver; na planilha não tem nesta aba)
db/schema_excel.py:20:  aba TEXT NOT NULL,
db/schema_excel.py:35:CREATE INDEX IF NOT EXISTS ix_robo_snapshot_aba ON robo_snapshot(aba);
db/schema_excel.py:41:  aba TEXT NOT NULL,
db/schema_excel.py:64:CREATE INDEX IF NOT EXISTS ix_robo_legs_snapshot_aba ON robo_legs_snapshot(aba);
db/schema_excel.py:71:  aba TEXT NOT NULL,
db/schema_excel.py:87:CREATE INDEX IF NOT EXISTS ix_robo_legs_history_aba ON robo_legs_history(aba);
db/schema_excel.py:93:  aba TEXT,
db/writer.py:38:            aba: Nome da aba/estratégia
db/writer.py:68:                    timestamp, aba, float(spot), float(pl), meta_json
db/writer.py:72:                INSERT INTO payoff_curve_points 
db/writer.py:73:                (timestamp, aba, point_spot, point_pl, meta_json)
db/writer.py:117:            return write_decision_snapshot_atomic(conn, timestamp, aba, decision_dict)
db/writer.py:123:        """Retorna a última decisão para uma aba."""
db/writer.py:133:            """, (aba,))
db/writer.py:139:        """Retorna histórico de payoff points para uma aba."""
db/writer.py:146:                FROM payoff_curve_points 
db/writer.py:150:            """, (aba, limit))
infra/bootstrap_structures_schema.py:37:                alias_legacy_aba TEXT,
infra/bootstrap_structures_schema.py:53:                structure_id    INTEGER NOT NULL,
infra/bootstrap_structures_schema.py:66:                FOREIGN KEY (structure_id) REFERENCES structures(id) ON DELETE CASCADE
infra/bootstrap_structures_schema.py:79:                structure_id      INTEGER,
infra/bootstrap_structures_schema.py:91:                FOREIGN KEY (structure_id) REFERENCES structures(id)
infra/bootstrap_structures_schema.py:108:                structure_id INTEGER NOT NULL,
infra/bootstrap_structures_schema.py:115:                FOREIGN KEY (structure_id) REFERENCES structures(id)
infra/bootstrap_structures_schema.py:130:                structure_id          INTEGER NOT NULL,
infra/bootstrap_structures_schema.py:142:                FOREIGN KEY (structure_id) REFERENCES structures(id),
infra/bootstrap_structures_schema.py:157:                structure_id     INTEGER NOT NULL,
infra/bootstrap_structures_schema.py:172:                FOREIGN KEY (structure_id) REFERENCES structures(id),
infra/bootstrap_structures_schema.py:189:            CREATE INDEX IF NOT EXISTS idx_structures_alias_legacy_aba
infra/bootstrap_structures_schema.py:190:            ON structures(alias_legacy_aba)
infra/bootstrap_structures_schema.py:199:            CREATE INDEX IF NOT EXISTS idx_structure_legs_structure_id
infra/bootstrap_structures_schema.py:200:            ON structure_legs(structure_id)
infra/bootstrap_structures_schema.py:205:            CREATE INDEX IF NOT EXISTS idx_structure_legs_structure_id_leg_order
infra/bootstrap_structures_schema.py:206:            ON structure_legs(structure_id, leg_order)
infra/bootstrap_structures_schema.py:215:            CREATE INDEX IF NOT EXISTS idx_pricing_executions_structure_id
infra/bootstrap_structures_schema.py:216:            ON pricing_executions(structure_id)
infra/bootstrap_structures_schema.py:237:            CREATE INDEX IF NOT EXISTS idx_audit_log_structure_id
infra/bootstrap_structures_schema.py:238:            ON structure_audit_log(structure_id)
infra/bootstrap_structures_schema.py:259:            CREATE INDEX IF NOT EXISTS idx_structure_snapshots_structure_id
infra/bootstrap_structures_schema.py:260:            ON structure_snapshots(structure_id)
infra/bootstrap_structures_schema.py:272:            ON structure_snapshots(structure_id, created_at)
infra/bootstrap_structures_schema.py:299:            CREATE INDEX IF NOT EXISTS idx_structure_leg_snapshots_structure_id
infra/bootstrap_structures_schema.py:300:            ON structure_leg_snapshots(structure_id)
infra/bootstrap_structures_schema.py:321:    structure_id    INTEGER NOT NULL,
infra/bootstrap_structures_schema.py:333:    "CREATE INDEX IF NOT EXISTS idx_pricing_executions_structure_id   ON pricing_executions (structure_id);",
infra/bootstrap_structures_schema.py:336:    "CREATE INDEX IF NOT EXISTS idx_pricing_executions_structure_date ON pricing_executions (structure_id, reference_date);",
repositories/system_snapshots_repository.py:81:        structure_id: int,
repositories/system_snapshots_repository.py:101:        if not structure_id:
repositories/system_snapshots_repository.py:102:            raise ValueError("structure_id é obrigatório")
repositories/system_snapshots_repository.py:115:                    structure_id,
repositories/system_snapshots_repository.py:132:                    structure_id,
repositories/system_snapshots_repository.py:153:                    structure_id=structure_id,
repositories/system_snapshots_repository.py:165:        structure_id: int,
repositories/system_snapshots_repository.py:173:                structure_id,
repositories/system_snapshots_repository.py:192:                structure_id,
repositories/system_snapshots_repository.py:243:        structure_id: int,
repositories/system_snapshots_repository.py:257:                WHERE structure_id = ?
repositories/system_snapshots_repository.py:261:                (structure_id, limit),
repositories/system_snapshots_repository.py:268:        structure_id: int,
repositories/system_snapshots_repository.py:272:        snapshots = self.list_snapshots_for_structure(structure_id, limit=1)
services/derived_payoff_persistence.py:52:                "derived_payoff_persistence: decisão não gravada porque payoff não foi salvo -- structure_id=%s",
services/derived_payoff_persistence.py:53:                pricing_payload.get("structure_id"),
services/derived_payoff_persistence.py:60:                "derived_payoff_persistence: payoff salvo, mas decisão falhou -- structure_id=%s timestamp=%s",
services/derived_payoff_persistence.py:61:                pricing_payload.get("structure_id"),
services/derived_payoff_persistence.py:81:                    "derived_payoff_persistence: payoff sem pontos para structure_id=%s",
services/derived_payoff_persistence.py:82:                    pricing_payload.get("structure_id"),
services/derived_payoff_persistence.py:88:                "derived_payoff_persistence: %d pontos gravados -- structure_id=%s",
services/derived_payoff_persistence.py:90:                pricing_payload.get("structure_id"),
services/derived_payoff_persistence.py:96:                "derived_payoff_persistence: erro ao gravar payoff -- structure_id=%s",
services/derived_payoff_persistence.py:97:                pricing_payload.get("structure_id"),
services/derived_payoff_persistence.py:151:                    "structure_id":    pricing_payload.get("structure_id"),
services/derived_payoff_persistence.py:160:                structure_id=pricing_payload.get("structure_id"),
services/derived_payoff_persistence.py:166:                "derived_payoff_persistence: decisão gravada -- structure_id=%s",
services/derived_payoff_persistence.py:167:                pricing_payload.get("structure_id"),
services/derived_payoff_persistence.py:173:                "derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s",
services/derived_payoff_persistence.py:174:                pricing_payload.get("structure_id"),
services/derived_payoff_persistence.py:311:          B) flat:        { legs: [...], spot_price: ..., structure_id: ..., ... }
services/derived_payoff_persistence.py:321:        structure_id   = pricing_payload.get("structure_id")
services/derived_payoff_persistence.py:335:                "structure_id":    structure_id,
services/derived_service.py:5:alteracao_62           -- AbaResolverMixin extraído para repositories/_aba_resolver_mixin.py.
services/derived_service.py:6:alteracao_65           -- get_payoff_by_aba() removida da interface pública (standalone).
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
services/derived_service.py:166:    structure_id: Any = None,
services/derived_service.py:170:    _unwrap_ref() extrai a string aba de forma segura.
services/derived_service.py:175:        int(structure_id)
services/derived_service.py:176:        if structure_id is not None
services/derived_service.py:177:        else _resolve_structure_id(storage_key)
services/derived_service.py:194:        "structure_id": resolved_sid,
services/derived_service.py:202:            aba=storage_key,
services/derived_service.py:206:            structure_id=resolved_sid,
services/derived_service.py:212:    aba: Optional[str] = None,
services/derived_service.py:218:        aba=aba,
services/derived_service.py:219:        structure_id=payoff.get("structure_id"),
services/derived_service.py:224:    sid_from_payload = payoff.get("structure_id")
services/derived_service.py:228:        else _resolve_structure_id(storage_key)
services/derived_service.py:233:        structure_id=resolved_sid,
services/derived_service.py:243:        accepts_structure_id = (
services/derived_service.py:244:            "structure_id" in sig.parameters
services/derived_service.py:251:        accepts_structure_id = True
services/derived_service.py:253:    if accepts_structure_id:
services/derived_service.py:260:            structure_id=resolved_sid,
services/derived_service.py:277:    structure_id: Any = None,
services/derived_service.py:283:    - Preserva structure_id explícito recebido por argumento, pelo payload
services/derived_service.py:285:    - Só tenta resolver por storage_key/alias quando não há structure_id explícito.
services/derived_service.py:290:    explicit_sid = structure_id
services/derived_service.py:292:        explicit_sid = decision.get("structure_id")
services/derived_service.py:294:        explicit_sid = (decision.get("meta") or {}).get("structure_id")
services/derived_service.py:299:        else _resolve_structure_id(storage_key)
services/derived_service.py:304:        "structure_id": resolved_sid,
services/derived_service.py:308:            "structure_id": resolved_sid,
services/derived_service.py:317:            aba=storage_key,
services/derived_service.py:324:    structure_id: Any = None,
services/derived_service.py:327:    aba: Optional[str] = None,
services/derived_service.py:333:        aba=aba,
services/derived_service.py:334:        structure_id=structure_id,
services/derived_service.py:340:        int(structure_id)
services/derived_service.py:341:        if structure_id is not None
services/derived_service.py:342:        else _resolve_structure_id(storage_key)
services/derived_service.py:347:        "structure_id": resolved_sid,
services/derived_service.py:350:            "structure_id":     resolved_sid,
services/derived_service.py:384:            SELECT timestamp, aba, point_spot, point_pl, meta_json
services/derived_service.py:385:            FROM payoff_curve_points
services/derived_service.py:391:                "aba":        row[1],
services/derived_service.py:400:def get_payoff_by_structure_id(structure_id: int):
services/derived_service.py:405:    Importante: payoff_curve_points mantém histórico por timestamp.
services/derived_service.py:408:    ref = StructureRef.from_id(structure_id)
services/derived_service.py:416:              FROM payoff_curve_points
services/derived_service.py:420:                      FROM payoff_curve_points
services/derived_service.py:452:            "timestamp", "aba", "decision", "level",
services/derived_service.py:456:        if "structure_id" in cols:
services/derived_service.py:457:            select_cols.append("structure_id")
services/derived_service.py:491:            if item.get("structure_id") is None:
services/derived_service.py:498:                        sid = parsed.get("structure_id")
services/derived_service.py:500:                            item["structure_id"] = sid
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
services/derived_service.py:548:        return get_payoff_by_structure_id(structure_id)
services/pricing_execution_persistence_service.py:109:        structure_id = pricing_payload.get("structure_id") or record.get("structure_id")
services/pricing_execution_persistence_service.py:110:        if not structure_id:
services/pricing_execution_persistence_service.py:115:                structure_id=int(structure_id),
services/pricing_execution_persistence_service.py:143:            "structure_id": pricing_payload.get("structure_id"),

## Testes direcionados - resultado compacto

### Fase 3
....................                                               [100%]
20 passed, 6 subtests passed in 1.41s

### Fase 4
........................................................................ [ 45%]
........................................................................ [ 91%]
..............                                                           [100%]
158 passed, 513 deselected in 3.38s

### Compileall
Listing 'services'...
Listing 'domain'...
Listing 'repositories'...
Listing 'UI'...
Listing 'UI\\components'...
Listing 'UI\\models'...
Listing 'ATT/tests'...
