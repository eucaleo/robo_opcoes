# Fase 1 RTD - remoção de subprocesso no preenchimento de leg

Atualizado em: 20260630_221556

## Objetivo

Eliminar o fluxo sob demanda por símbolo no botão de preenchimento RTD da leg.

## Arquivo alterado

    UI/components/structure_editor_dialog.py

## Decisão

    O botão de preenchimento RTD não chama mais subprocesso.
    O botão não chama mais scripts de refresh por símbolo.
    O preenchimento passa a usar o service de enriquecimento.
    O service lê o cache operacional em dados/app.db.rtd_option_quotes.

## Verificação de resíduos no arquivo

3:import json
4:import subprocess
5:import sys
411:    def _refresh_rtd_symbol_on_demand(self, codigo_opcao: str) -> tuple[bool, str]:
419:        script_path = project_root / "scripts" / "refresh_rtd_symbol_to_option_quotes_fallback.py"
438:            completed = subprocess.run(
529:            ok, message = self._refresh_rtd_symbol_on_demand(symbol)

## Trecho funcional após alteração

            "expiration_date": self._lf_expiry.get(),
            "quantity":        self._lf_qty.get(),
            "premium":         self._lf_premium.get() or None,
            "multiplier":      self._lf_mult.get() or 1,
            "leg_order":       idx + 1,
            "symbol":          self._lf_symbol.get() or None,
            "notes":           None,
        }
        self._refresh_leg_tree()


    def _refresh_rtd_symbol_on_demand(self, codigo_opcao: str) -> tuple[bool, str]:
        """Atualiza uma opcao via RTD/Excel e grava o cache em dados/app.db."""
        symbol = str(codigo_opcao or "").strip().upper()

        if not symbol:
            return False, "Codigo da opcao vazio."

        project_root = Path(__file__).resolve().parents[2]
        script_path = project_root / "scripts" / "refresh_rtd_symbol_to_option_quotes_fallback.py"
        db_path = project_root / "dados" / "app.db"

        if not script_path.exists():
            return False, f"Script RTD nao encontrado: {script_path}"

        cmd = [
            sys.executable,
            str(script_path),
            "--symbol",
            symbol,
            "--db",
            str(db_path),
            "--wait-seconds",
            "3",
            "--json",
        ]

        try:
            completed = subprocess.run(
                cmd,
                cwd=str(project_root),
                text=True,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                timeout=20,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return False, f"Timeout ao atualizar RTD para {symbol}."

        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()

        if completed.returncode != 0:
            detail = stderr or stdout or "sem detalhe"
            return False, f"Falha ao atualizar RTD para {symbol}: {detail}"

        try:
            data = json.loads(stdout)
        except json.JSONDecodeError:
            return False, f"RTD atualizou, mas retornou JSON invalido: {stdout[:500]}"

        if data.get("status") != "ok":
            errors = data.get("errors") or []
            return False, f"RTD retornou erro para {symbol}: {errors}"

        quote = data.get("quote")

        if not quote:
            return False, f"RTD executou, mas nao retornou cotacao para {symbol}."

        return True, "OK"

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
            ok, message = self._refresh_rtd_symbol_on_demand(symbol)
            
            if not ok:
                messagebox.showwarning(
                    "Preencher via RTD",
                    message,
                    parent=self,
                )
                return
            
            enriched = self._get_rtd_leg_enrichment_service().enrich(leg_data)
        except Exception as exc:
