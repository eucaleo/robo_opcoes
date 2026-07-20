from pathlib import Path
import re

path = Path("UI/components/terminal_vwap_payoff_dark_panel.py")
text = path.read_text(encoding="utf-8")

original = text

# ---------------------------------------------------------------------
# 1) Garantir import os
# ---------------------------------------------------------------------
if "import os" not in text:
    text = re.sub(r"(^import .*$)", r"\1\nimport os", text, count=1, flags=re.M)

# ---------------------------------------------------------------------
# 2) Iniciar auto-refresh no __init__
#    Insere após self._render_empty_charts() se ainda não existir.
# ---------------------------------------------------------------------
marker = "self._start_auto_refresh_loop()"
if marker not in text:
    text = text.replace(
        "        self._render_empty_charts()\n",
        "        self._render_empty_charts()\n"
        "\n"
        "        # Auto-refresh: UI apenas consome snapshots persistidos.\n"
        "        # Configure com TERMINAL_VWAP_PAYOFF_REFRESH_SECONDS=10.\n"
        "        self._start_auto_refresh_loop()\n",
        1,
    )

# ---------------------------------------------------------------------
# 3) Substituir _load_payoff_points + _load_persisted_payoff_points
#    Regra: UI não calcula payoff. Somente carrega snapshot persistido.
# ---------------------------------------------------------------------
pattern_payoff_loader = re.compile(
    r"    def _load_payoff_points\(\n"
    r".*?"
    r"    def _calculate_payoff_from_legs\(",
    re.S,
)

replacement_payoff_loader = '''    def _load_payoff_points(
        self,
        structure_id: Any,
        legs: List[Dict[str, Any]],
    ) -> List[Dict[str, float]]:
        """
        Carrega payoff persistido.

        Importante:
        - A UI NÃO calcula payoff.
        - Se não houver curva persistida para a estrutura, retorna lista vazia.
        - O cálculo deve ocorrer fora da UI, no pipeline/backend/serviço derivado.
        """
        persisted = self._load_persisted_payoff_points(structure_id)
        if persisted:
            return persisted

        self._safe_status(
            f"Payoff persistido ausente para estrutura {structure_id}; aguardando backend."
        )
        return []

    def _load_persisted_payoff_points(self, structure_id: Any) -> List[Dict[str, float]]:
        """
        Busca a curva de payoff mais recente no banco.

        Correção importante:
        - Não mistura pontos de timestamps diferentes.
        - Se houver coluna de timestamp, primeiro resolve o último snapshot
          da estrutura e depois busca apenas esse snapshot.
        """
        if structure_id is None:
            return []

        conn = self._connect()
        try:
            schema = self._tables_cols(conn)

            preferred_tables = [
                "payoff_curve_points",
                "rtd_payoff_points",
                "rtd_payoff_curva",
                "payoff_points",
            ]

            table_order = [
                table for table in preferred_tables if table in schema
            ] + [
                table for table in schema.keys() if table not in preferred_tables
            ]

            for table in table_order:
                cols = schema.get(table) or {}

                sid_col = _first_col(cols, ["structure_id", "id_structure", "estrutura_id"])
                spot_col = _first_col(cols, ["point_spot", "spot", "underlying", "x"])
                pl_col = _first_col(cols, ["point_pl", "pl", "payoff", "result", "resultado", "y"])
                ts_col = _first_col(cols, ["timestamp", "updated_at", "created_at", "dt_ref"])

                if not sid_col or not spot_col or not pl_col:
                    continue

                params: tuple[Any, ...]
                where_sql = f"WHERE {_q(sid_col)} = ?"
                params = (structure_id,)

                if ts_col:
                    latest_sql = (
                        f"SELECT {_q(ts_col)} AS ts "
                        f"FROM {_q(table)} "
                        f"WHERE {_q(sid_col)} = ? "
                        f"ORDER BY {_q(ts_col)} DESC "
                        f"LIMIT 1"
                    )
                    latest_row = conn.execute(latest_sql, (structure_id,)).fetchone()

                    if not latest_row or latest_row["ts"] is None:
                        continue

                    latest_ts = latest_row["ts"]
                    where_sql += f" AND {_q(ts_col)} = ?"
                    params = (structure_id, latest_ts)

                sql = (
                    f"SELECT {_q(spot_col)} AS spot, {_q(pl_col)} AS pl "
                    f"FROM {_q(table)} "
                    f"{where_sql} "
                    f"ORDER BY CAST({_q(spot_col)} AS REAL)"
                )

                rows = conn.execute(sql, params).fetchall()

                points: List[Dict[str, float]] = []
                for row in rows:
                    spot = _to_float(row["spot"])
                    pl = _to_float(row["pl"])

                    if spot is not None and pl is not None:
                        points.append({"spot": spot, "pl": pl})

                if points:
                    return points

            return []
        finally:
            conn.close()

    def _calculate_payoff_from_legs('''

text, count = pattern_payoff_loader.subn(replacement_payoff_loader, text, count=1)

if count != 1:
    raise SystemExit(
        "ERRO: não consegui substituir _load_payoff_points/_load_persisted_payoff_points."
    )

# ---------------------------------------------------------------------
# 4) Substituir recalculate_selected_structure por refresh do banco.
#    Mantém o nome para não quebrar command= existente.
# ---------------------------------------------------------------------
pattern_recalculate = re.compile(
    r"    def recalculate_selected_structure\(self\) -> None:\n"
    r".*?"
    r"\n\n    def archive_selected_structure\(self\) -> None:",
    re.S,
)

replacement_recalculate = '''    def _start_auto_refresh_loop(self) -> None:
        """
        Inicia refresh automático da estrutura aberta.

        A UI apenas relê o banco e redesenha.
        Não calcula payoff.
        """
        if getattr(self, "_auto_refresh_loop_started", False):
            return

        self._auto_refresh_loop_started = True
        self._auto_refresh_after_id = None
        self._auto_refresh_in_progress = False

        try:
            seconds = float(os.getenv("TERMINAL_VWAP_PAYOFF_REFRESH_SECONDS", "10"))
        except Exception:
            seconds = 10.0

        if seconds <= 0:
            self._safe_status("Auto-refresh do payoff desativado.")
            return

        self._auto_refresh_interval_ms = max(1000, int(seconds * 1000))
        self._schedule_auto_refresh()

    def _schedule_auto_refresh(self) -> None:
        if not getattr(self, "_auto_refresh_loop_started", False):
            return

        if getattr(self, "_auto_refresh_after_id", None) is not None:
            return

        try:
            if not self.winfo_exists():
                return
        except Exception:
            return

        self._auto_refresh_after_id = self.after(
            getattr(self, "_auto_refresh_interval_ms", 10000),
            self._auto_refresh_tick,
        )

    def _auto_refresh_tick(self) -> None:
        self._auto_refresh_after_id = None

        try:
            if getattr(self, "_auto_refresh_in_progress", False):
                return

            self._auto_refresh_in_progress = True
            self._refresh_selected_structure_from_store(silent=True)

        except Exception as exc:
            self._safe_status(f"Auto-refresh falhou: {exc}")

        finally:
            self._auto_refresh_in_progress = False
            self._schedule_auto_refresh()

    def _refresh_selected_structure_from_store(self, silent: bool = False) -> bool:
        """
        Atualiza estrutura ativa consumindo dados persistidos.

        Este método:
        - relê viewmodel/payload;
        - relê payoff persistido;
        - redesenha KPI/pernas/gráficos/alertas;
        - não calcula payoff na UI.
        """
        structure = getattr(self, "selected_structure", None)

        if not structure:
            if not silent:
                structure = self._require_active_selected_structure("atualizar payoff")
            if not structure:
                return False

        sid = structure.get("id")

        if sid is None:
            if not silent:
                self._safe_status("Estrutura ativa sem ID; não foi possível atualizar.")
            return False

        viewmodel = self._build_operational_viewmodel(sid)
        payload = self._resolve_operational_payload(structure, viewmodel)

        operational_structure = payload["structure"]
        legs = payload["legs"]
        market = payload["market"]
        payoff_points = payload["payoff_points"]

        self.selected_structure = dict(operational_structure)

        sid = operational_structure.get("id") or sid
        name = operational_structure.get("name")
        asset = operational_structure.get("underlying_asset")

        self.header.configure(
            text=f"Analise ativa: ID {sid} - {name} | Ativo: {asset} | Dados atualizados"
        )

        self._update_kpis(market, payoff_points)
        self._render_legs(legs)
        self._render_charts(market, payoff_points, asset, legs)
        self._render_alerts(market, payoff_points, legs)

        if not silent:
            msg = f"Dados atualizados do banco para ID {sid}."
            self._safe_status(msg)
            self._render_structure_actions(notice=msg)

        return True

    def recalculate_selected_structure(self) -> None:
        """
        Nome mantido por compatibilidade com command= existente.

        Antes: recalculava payoff na UI.
        Agora: apenas atualiza do banco/snapshot persistido.
        """
        try:
            ok = self._refresh_selected_structure_from_store(silent=False)
            if not ok:
                return
        except Exception as exc:
            self._safe_status(f"Erro ao atualizar payoff: {exc}")
            messagebox.showerror("Erro ao atualizar payoff", str(exc), parent=self.winfo_toplevel())


    def archive_selected_structure(self) -> None:'''

text, count = pattern_recalculate.subn(replacement_recalculate, text, count=1)

if count != 1:
    raise SystemExit(
        "ERRO: não consegui substituir recalculate_selected_structure."
    )

# ---------------------------------------------------------------------
# 5) Ajustar textos do botão, se existirem.
# ---------------------------------------------------------------------
text = text.replace('text="Recalcular payoff"', 'text="Atualizar payoff"')
text = text.replace('text="Recalcular Payoff"', 'text="Atualizar payoff"')
text = text.replace('text="Calcular payoff"', 'text="Atualizar payoff"')
text = text.replace('text="Calcular Payoff"', 'text="Atualizar payoff"')

# ---------------------------------------------------------------------
# 6) Gravar
# ---------------------------------------------------------------------
if text == original:
    raise SystemExit("Nenhuma alteração aplicada.")

path.write_text(text, encoding="utf-8")

print("OK: patch aplicado em", path)
