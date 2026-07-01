# Fase 1 RTD - classificação de referências RTD na UI

Atualizado em: 20260630_222706

## Objetivo

Classificar referências RTD remanescentes em UI para identificar se ainda existe acoplamento indevido entre tela, banco operacional RTD, Excel ou refresh sob demanda.

## Critérios

    Crítico:
    UI chamando subprocesso.
    UI chamando script RTD/Excel.
    UI executando refresh sob demanda de RTD/Excel.
    UI abrindo conexão direta com dados/app.db para consultar tabelas RTD.

    Aceitável temporariamente:
    UI chamando service/repository já existente.
    UI exibindo alerta textual sobre dados RTD ausentes.
    UI usando método refresh apenas para atualizar estado visual/local, sem RTD/Excel/subprocess.

## Grep geral RTD/Excel/refresh/sqlite em UI

    UI/components/details_panel.py:6:import sqlite3
    UI/components/details_panel.py:116:        import sqlite3
    UI/components/details_panel.py:145:                suffix in {".db", ".sqlite", ".sqlite3"}
    UI/components/details_panel.py:394:                    except sqlite3.Error:
    UI/components/details_panel.py:419:                con = sqlite3.connect(str(db_path))
    UI/components/details_panel.py:438:            except sqlite3.Error:
    UI/components/details_panel.py:735:        """Chamado pelo MainWindow ao finalizar o subprocess do pipeline."""
    UI/components/details_panel.py:887:        con = sqlite3.connect(str(db_path))
    UI/components/details_panel.py:888:        con.row_factory = sqlite3.Row
    UI/components/details_panel.py:927:        con = sqlite3.connect(str(db_path))
    UI/components/details_panel.py:928:        con.row_factory = sqlite3.Row
    UI/components/details_panel.py:955:        con = sqlite3.connect(str(db_path))
    UI/components/details_panel.py:956:        con.row_factory = sqlite3.Row
    UI/components/structure_editor_dialog.py:40:from repositories.rtd_option_quotes_repository import RtdOptionQuotesRepository
    UI/components/structure_editor_dialog.py:41:from services.structure_leg_rtd_enrichment_service import StructureLegRtdEnrichmentService
    UI/components/structure_editor_dialog.py:73:        _rtd_leg_enrichment_service=None,    # <-- injecao opcional para testes/UI
    UI/components/structure_editor_dialog.py:88:        self._rtd_leg_enrichment_service = _rtd_leg_enrichment_service
    UI/components/structure_editor_dialog.py:244:            text="[RTD] Preencher por Simbolo",
    UI/components/structure_editor_dialog.py:245:            command=self._cmd_fill_leg_from_rtd,
    UI/components/structure_editor_dialog.py:408:    def _get_rtd_leg_enrichment_service(self):
    UI/components/structure_editor_dialog.py:409:        """Cria/lazily retorna o service de preenchimento de leg via RTD."""
    UI/components/structure_editor_dialog.py:410:        if self._rtd_leg_enrichment_service is None:
    UI/components/structure_editor_dialog.py:412:            rtd_db_path = project_root / "dados" / "app.db"
    UI/components/structure_editor_dialog.py:413:            rtd_repo = RtdOptionQuotesRepository(rtd_db_path)
    UI/components/structure_editor_dialog.py:414:            self._rtd_leg_enrichment_service = StructureLegRtdEnrichmentService(
    UI/components/structure_editor_dialog.py:415:                rtd_repo
    UI/components/structure_editor_dialog.py:417:        return self._rtd_leg_enrichment_service
    UI/components/structure_editor_dialog.py:433:    def _cmd_fill_leg_from_rtd(self):
    UI/components/structure_editor_dialog.py:434:        """Preenche a leg selecionada usando rtd_option_quotes.codigo_opcao."""
    UI/components/structure_editor_dialog.py:438:                "Preencher via RTD",
    UI/components/structure_editor_dialog.py:447:                "Preencher via RTD",
    UI/components/structure_editor_dialog.py:448:                "Informe o campo 'Simbolo' antes de consultar o RTD.",
    UI/components/structure_editor_dialog.py:463:            enriched = self._get_rtd_leg_enrichment_service().enrich(leg_data)
    UI/components/structure_editor_dialog.py:466:                "Preencher via RTD",
    UI/components/structure_editor_dialog.py:467:                f"Nao foi possivel preencher a leg pelo RTD:\n{exc}",
    UI/components/terminal_vwap_payoff_dark_panel.py:24:import sqlite3
    UI/components/terminal_vwap_payoff_dark_panel.py:427:    def _connect(self) -> sqlite3.Connection:
    UI/components/terminal_vwap_payoff_dark_panel.py:431:        conn = sqlite3.connect(str(db))
    UI/components/terminal_vwap_payoff_dark_panel.py:432:        conn.row_factory = sqlite3.Row
    UI/components/terminal_vwap_payoff_dark_panel.py:435:    def _tables_cols(self, conn: sqlite3.Connection) -> Dict[str, List[str]]:
    UI/components/terminal_vwap_payoff_dark_panel.py:468:        conn = self._connect()
    UI/components/terminal_vwap_payoff_dark_panel.py:606:        conn = self._connect()
    UI/components/terminal_vwap_payoff_dark_panel.py:672:        conn = self._connect()
    UI/components/terminal_vwap_payoff_dark_panel.py:676:            table = "rtd_underlying_quotes"
    UI/components/terminal_vwap_payoff_dark_panel.py:803:        conn = self._connect()
    UI/components/terminal_vwap_payoff_dark_panel.py:989:            alerts.append("VWAP do ativo-base ausente em rtd_underlying_quotes")
    UI/components/terminal_vwap_payoff_panel.py:608:                "Nenhum cálculo, RTD, banco ou serviço foi alterado nesta camada."
    UI/models/ui_data.py:5:import sqlite3
    UI/models/ui_data.py:6:from sqlite3 import Row
    UI/models/ui_data.py:70:    def _connect(self) -> sqlite3.Connection:
    UI/models/ui_data.py:75:        conn = sqlite3.connect(str(self.derived_db_path))
    UI/models/ui_data.py:76:        conn.row_factory = sqlite3.Row
    UI/models/ui_data.py:81:        conn = self._connect()
    UI/models/ui_data.py:108:        conn = self._connect()
    UI/models/ui_data.py:218:        conn = self._connect()
    UI/models/ui_data.py:360:        conn = self._connect()
    UI/models/ui_data.py:423:        conn = self._connect()
    UI/models/ui_data.py:624:        conn = self._connect()
    UI/models/ui_data.py:662:    def _connect_derived_threadsafe(self) -> sqlite3.Connection:
    UI/models/ui_data.py:663:        return self._connect()

## Trecho: UI/components/terminal_vwap_payoff_dark_panel.py linhas 640-710

                    f"FROM {_q(table)} "
                    f"WHERE {_q(sid_col)} = ?"
                )
                rows = conn.execute(sql, (structure_id,)).fetchall()
    
                return [dict(row) for row in rows]
            finally:
                conn.close()
    
        def _load_market(self, asset: Any) -> Dict[str, Any]:
            result = {
                "current_price": None,
                "vwap": None,
                "bid": None,
                "ask": None,
                "close_price": None,
                "prev_close": None,
                "open_price": None,
                "high_price": None,
                "low_price": None,
                "volume": None,
                "change_percent": None,
                "updated_at": None,
                "series": [],
                "source_table": None,
                "vwap_source": None,
            }
    
            asset = str(asset or "").strip().upper()
            if not asset or asset == "N/A":
                return result
    
            conn = self._connect()
            try:
                schema = self._tables_cols(conn)
    
                table = "rtd_underlying_quotes"
                if table not in schema:
                    return result
    
                cols = schema[table]
    
                ativo_col = _first_col(
                    cols,
                    ["ativo", "underlying_asset", "asset", "ticker", "symbol"],
                )
                price_col = _first_col(
                    cols,
                    ["ultimo_preco", "current_price", "preco_atual", "price", "last_price", "last"],
                )
                vwap_col = _first_col(
                    cols,
                    ["vwap", "vwap_price", "preco_medio"],
                )
                bid_col = _first_col(cols, ["bid"])
                ask_col = _first_col(cols, ["ask"])
                close_col = _first_col(cols, ["close_price", "close", "fechamento"])
                prev_close_col = _first_col(
                    cols,
                    ["prev_close", "previous_close", "fechamento_anterior"],
                )
                open_col = _first_col(cols, ["open_price", "open", "abertura"])
                high_col = _first_col(cols, ["high_price", "high", "maxima"])
                low_col = _first_col(cols, ["low_price", "low", "minima"])
                volume_col = _first_col(cols, ["volume"])
                change_col = _first_col(
                    cols,
                    ["change_percent", "variation_percent", "variacao_percentual"],
                )
                ts_col = _first_col(
                    cols,

## Trecho: UI/components/terminal_vwap_payoff_dark_panel.py linhas 960-1005

                        idx,
                        leg.get("symbol") or "--",
                        leg.get("position_side") or "--",
                        leg.get("option_type") or "--",
                        _number(leg.get("strike")),
                        leg.get("expiration_date") or "--",
                        _number(leg.get("quantity")),
                        _money(leg.get("premium")),
                    ),
                )
    
        def _set_alerts(self, alerts: List[str]) -> None:
            self.alerts_box.configure(state="normal")
            self.alerts_box.delete("1.0", "end")
            for alert in alerts:
                self.alerts_box.insert("end", "- " + alert + "\n")
            self.alerts_box.configure(state="disabled")
    
        def _render_alerts(
            self,
            market: Dict[str, Any],
            payoff_points: List[Dict[str, float]],
            legs: List[Dict[str, Any]],
        ) -> None:
            alerts: List[str] = []
    
            if _to_float(market.get("current_price")) is None:
                alerts.append("preço atual ausente")
            if _to_float(market.get("vwap")) is None:
                alerts.append("VWAP do ativo-base ausente em rtd_underlying_quotes")
            if not payoff_points:
                alerts.append("payoff sem pontos")
            if not legs:
                alerts.append("estrutura sem pernas carregadas")
    
            if not alerts:
                alerts.append("sem avisos críticos")
    
            self._set_alerts(alerts)
    
        def _clear_canvas(self, attr: str) -> None:
            canvas = getattr(self, attr)
            if canvas is not None:
                try:
                    canvas.get_tk_widget().destroy()
                except Exception:

## Trecho: UI/components/details_panel.py linhas 830-875

    
            try:
                from repositories.structures_repository import StructuresRepository
                from repositories.structure_events_repository import (
                    StructureEventsRepository,
                )
                from services.structure_events_service import StructureEventsService
    
                app_db_path = self._operational_app_db_path()
                structures_repo = StructuresRepository(app_db_path)
                events_repo = StructureEventsRepository(app_db_path)
                events_service = StructureEventsService(
                    structure_events_repository=events_repo
                )
    
                structure = structures_repo.get_structure(sid)
                if not structure:
                    return None
    
                effective = events_service.apply_events_to_structure(structure)
                return effective if isinstance(effective, dict) else None
            except Exception:
                return None
    
        def _refresh_operational_state_for_structure(self, structure_id):
            effective = self._fetch_effective_structure_local(structure_id)
            if effective:
                self.update_operational_state(effective)
            else:
                self._clear_operational_state()
    
        # ------------------------------------------------------------------
        # Helpers internos
        # ------------------------------------------------------------------
    
        def _format_currency_label(self, label: ttk.Label, value):
            if value is None:
                label.config(text="N/A")
                return
            try:
                v = float(value)
                formatted = (
                    f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                )
                label.config(text=formatted)
            except Exception:

## Trecho: UI/components/details_panel.py linhas 1000-1045

                    if x2 != x1:
                        x0 = x1 + (0.0 - y1) * (x2 - x1) / (y2 - y1)
                        breakevens.append(x0)
            out: list = []
            for be in sorted(breakevens):
                if not out or abs(be - out[-1]) > 1e-6:
                    out.append(be)
            return out
    
        def _compute_pl_at_spot(self, pts, spot_ref: Optional[float]) -> Optional[float]:
            if spot_ref is None or not pts or len(pts) < 2:
                return None
            x = float(spot_ref)
            if x < pts[0][0] or x > pts[-1][0]:
                return None
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                if x1 <= x <= x2:
                    if x2 == x1:
                        return y1
                    t = (x - x1) / (x2 - x1)
                    return y1 + t * (y2 - y1)
            return None
    
        def _refresh_current_from_derived(self, structure_id):
            """Recarrega somente a estrutura atual do derived.db e atualiza widgets."""
            decision = self._fetch_latest_decision_from_derived(structure_id)
            if decision:
                self.update_decision(decision)
    
            pts = self._fetch_payoff_points_from_derived(structure_id)
            breakevens = self._compute_breakevens_from_points(pts)
    
            spot_ref = None
            if decision:
                spot_ref = decision.get("spot_reference")
    
            pl_at_spot = self._compute_pl_at_spot(pts, spot_ref)
            self.update_breakevens(breakevens, pl_at_spot)
    
            audit = self._fetch_audit_info_from_derived(structure_id)
            self.update_audit_info(audit)
    
        # ------------------------------------------------------------------
        # Recalc click
        # ------------------------------------------------------------------
    

## Conclusão preliminar

    Pendente de revisão humana.
    Se terminal_vwap_payoff_dark_panel.py abrir app.db diretamente ou consultar rtd_underlying_quotes dentro da UI, classificar como próximo alvo de desacoplamento.
    Se details_panel.py apenas atualizar estado visual/derived sem RTD/Excel/subprocess, classificar como não crítico nesta fase.
