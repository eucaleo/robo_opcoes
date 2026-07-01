# Fase 1 RTD - remoção de subprocesso no preenchimento de leg

Atualizado em: 20260630_221911

## Objetivo

Eliminar o fluxo sob demanda por símbolo no botão de preenchimento RTD da leg.

## Arquivo alterado

    UI/components/structure_editor_dialog.py

## Decisão

    O botão de preenchimento RTD não chama mais subprocesso.
    O botão não chama mais scripts de refresh por símbolo.
    O método _refresh_rtd_symbol_on_demand foi removido da UI.
    O preenchimento passa a usar diretamente o service de enriquecimento.
    O service lê o cache operacional em dados/app.db.rtd_option_quotes.

## Verificação de resíduos no arquivo

    Nenhum resíduo encontrado em UI/components/structure_editor_dialog.py.

## Trecho funcional após alteração

                "multiplier":      self._lf_mult.get() or 1,
                "leg_order":       idx + 1,
                "symbol":          self._lf_symbol.get() or None,
                "notes":           None,
            }
            self._refresh_leg_tree()
    
    
        def _get_rtd_leg_enrichment_service(self):
            """Cria/lazily retorna o service de preenchimento de leg via RTD."""
            if self._rtd_leg_enrichment_service is None:
                project_root = Path(__file__).resolve().parents[2]
                rtd_db_path = project_root / "dados" / "app.db"
                rtd_repo = RtdOptionQuotesRepository(rtd_db_path)
                self._rtd_leg_enrichment_service = StructureLegRtdEnrichmentService(
                    rtd_repo
                )
            return self._rtd_leg_enrichment_service
    
        @staticmethod
        def _normalize_option_type_for_ui(value) -> str:
            """Normaliza tipo de opcao para os valores aceitos pelo Combobox."""
            text = str(value or "").strip().upper()
            mapping = {
                "C": "CALL",
                "CALL": "CALL",
                "COMPRA": "CALL",
                "P": "PUT",
                "PUT": "PUT",
                "VENDA": "PUT",
            }
            return mapping.get(text, text)
    
        def _cmd_fill_leg_from_rtd(self):
            """Preenche a leg selecionada usando rtd_option_quotes.codigo_opcao."""
            idx = self._selected_leg_index()
            if idx is None:
                messagebox.showwarning(
                    "Preencher via RTD",
                    "Selecione uma leg na lista primeiro.",
                    parent=self,
                )
                return
    
            symbol = self._lf_symbol.get().strip().upper()
            if not symbol:
                messagebox.showwarning(
                    "Preencher via RTD",
                    "Informe o campo 'Simbolo' antes de consultar o RTD.",
                    parent=self,
                )
                return
    
            leg_data = {
                "symbol": symbol,
                "position_side": self._lf_side.get(),
                "quantity": self._lf_qty.get() or 1,
                "multiplier": self._lf_mult.get() or 1,
                "leg_order": idx + 1,
                "notes": self._legs_rows[idx].get("notes") if idx < len(self._legs_rows) else None,
            }
    
            try:
                enriched = self._get_rtd_leg_enrichment_service().enrich(leg_data)
            except Exception as exc:
                messagebox.showerror(
                    "Preencher via RTD",
                    f"Nao foi possivel preencher a leg pelo RTD:\n{exc}",
                    parent=self,
                )
                return
    
            option_type = self._normalize_option_type_for_ui(enriched.get("option_type"))
    
            self._lf_symbol.set(enriched.get("symbol") or symbol)
            self._lf_type.set(option_type)
            self._lf_strike.set(str(enriched.get("strike", "")))
            self._lf_expiry.set(str(enriched.get("expiration_date", "")))
            self._lf_qty.set(str(enriched.get("quantity", self._lf_qty.get() or 1)))
            self._lf_premium.set(str(enriched.get("premium", self._lf_premium.get() or "") or ""))
            self._lf_mult.set(str(enriched.get("multiplier", self._lf_mult.get() or 1)))
    
            if not self._f_underlying.get().strip() and enriched.get("underlying_asset"):
                self._f_underlying.set(str(enriched["underlying_asset"]))
    
            current = dict(self._legs_rows[idx])
            current.update(
                {
                    "position_side": normalize_position_side(self._lf_side.get()),
                    "option_type": option_type,
                    "strike": self._lf_strike.get(),
                    "expiration_date": self._lf_expiry.get(),
                    "quantity": self._lf_qty.get(),
                    "premium": self._lf_premium.get() or None,
                    "multiplier": self._lf_mult.get() or 1,
                    "leg_order": idx + 1,
                    "symbol": self._lf_symbol.get() or None,
                }
            )
            self._legs_rows[idx] = current
            self._refresh_leg_tree()
            self._leg_tree.selection_set(str(idx))
    
        # ------------------------------------------------------------------
        # Logica de payload (pura -- testavel sem display)
        # ------------------------------------------------------------------
    
        def _build_legs_payload(self) -> list[dict]:
            """
            Constroi lista de legs com leg_order sequencial a partir de 1.
    
            Logica pura: nao modifica _legs_rows nem acessa Tk.
            Testavel sem display (TestBuildLegsPayload no alteracao_69).
            """
            return [
                {
                    **leg,
                    "position_side": normalize_position_side(
                        leg.get("position_side", "COMPRADO")
                    ),
                    "strike": _parse_decimal(leg.get("strike"), "strike"),
