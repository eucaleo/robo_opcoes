# UI/components/details_panel.py
import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Dict, Optional, Any
import json
import sqlite3
from pathlib import Path


class DetailsPanel(ttk.LabelFrame):
    def __init__(self, parent, on_recalculate=None):
        super().__init__(parent)
        self._on_recalculate_cb = on_recalculate
        self._recalc_in_progress = False
        self._last_recalc_signature = None
        self._current_decision = None

        try:
            self._project_root = Path(__file__).resolve().parents[2]
        except Exception:
            self._project_root = None

        self._setup_widgets()

    # ------------------------------------------------------------------
    # Estado do recalc
    # ------------------------------------------------------------------

    def _set_recalc_ui_state(self, in_progress: bool, msg: str = "", color: str = "gray"):
        self._recalc_in_progress = in_progress
        try:
            if hasattr(self, "btn_recalculate") and self.btn_recalculate:
                self.btn_recalculate.config(
                    state="disabled" if in_progress else "normal"
                )
        except Exception:
            pass
        try:
            if hasattr(self, "lbl_recalc_status") and self.lbl_recalc_status:
                self.lbl_recalc_status.config(text=msg, foreground=color)
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Caminhos de DB
    # ------------------------------------------------------------------

    def _raw_db_path(self) -> Path:
        if self._project_root:
            return Path(self._project_root) / "dados" / "app.db"
        return Path("dados") / "app.db"

    def _derived_db_path(self) -> Path:
        project_root = Path(__file__).resolve().parents[2]
        return project_root / "dados" / "derived.db"

    # ------------------------------------------------------------------
    # patch_36: resolve structure_id como INTEGER
    # ------------------------------------------------------------------

    def _resolve_structure_key(self, structure_id) -> int:
        """
        structure_id é sempre INTEGER no DB.
        Aceita str ("7") ou int (7). Lança ValueError se não conversível.
        """
        try:
            return int(structure_id)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"structure_id inválido: {structure_id!r}. "
                "Esperado inteiro ou string numérica."
            ) from exc

    # ------------------------------------------------------------------
    # Assinatura de recalc (dedupe)
    # ------------------------------------------------------------------

    def _get_latest_snapshot_timestamp_for_structure(
        self, structure_id
    ) -> Optional[str]:
        """
        Busca o timestamp do snapshot mais recente no app.db para a estrutura.
        patch_36: usa apenas structure_id (INT); legado aba removido.
        PATCH_36_G: resolve structure_id -> aba via structures.alias_legacy_aba
        e busca timestamp em rtd_analise_robo_legs WHERE aba = ?
        Fallback: busca direta em structure_decisions do derived.db.
        """
        # --- Tentativa 1: app.db via aba ---
        db_path = self._raw_db_path()
        if db_path.exists():
            try:                                          # fix: Try -> try
                con = sqlite3.connect(str(db_path))
                try:
                    cur = con.cursor()

                    # Resolve aba a partir de structure_id
                    cur.execute(
                        "SELECT alias_legacy_aba FROM structures WHERE id = ? LIMIT 1",
                        (self._resolve_structure_key(structure_id),),
                    )
                    row = cur.fetchone()
                    aba = row[0] if row and row[0] else None

                    if aba:
                        # Verifica se rtd_analise_robo_legs existe
                        cur.execute(
                            "SELECT 1 FROM sqlite_master "
                            "WHERE type='table' AND name='rtd_analise_robo_legs' LIMIT 1"
                        )
                        if cur.fetchone():
                            cur.execute(
                                "SELECT MAX(timestamp) FROM rtd_analise_robo_legs "
                                "WHERE aba = ?",
                                (aba,),
                            )
                            row_ts = cur.fetchone()
                            if row_ts and row_ts[0]:
                                return str(row_ts[0])
                finally:
                    con.close()
            except Exception as exc:
                print(f"[details_panel] aviso ao buscar snapshot app.db: {exc}")

        # --- Tentativa 2: derived.db (fallback confiavel) ---
        try:
            derived_path = self._derived_db_path()
            if derived_path.exists():
                con = sqlite3.connect(str(derived_path))
                try:
                    sid = self._resolve_structure_key(structure_id)
                    cur = con.cursor()
                    cur.execute(
                        "SELECT MAX(created_at) FROM structure_decisions "
                        "WHERE structure_id = ?",
                        (sid,),
                    )
                    row = cur.fetchone()
                    if row and row[0]:
                        return str(row[0])
                finally:
                    con.close()
        except Exception as exc:
            print(f"[details_panel] aviso ao buscar snapshot derived.db: {exc}")

        return None

    def _compute_recalc_signature(self, structure_id):
        return (
            structure_id,
            self._get_latest_snapshot_timestamp_for_structure(structure_id),
        )

    # ------------------------------------------------------------------
    # Widgets
    # ------------------------------------------------------------------

    def _setup_widgets(self):
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Informações Básicas
        basic_frame = ttk.LabelFrame(self, text="Informações Básicas", padding=5)
        basic_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        basic_frame.grid_columnconfigure(1, weight=1)
        basic_frame.grid_columnconfigure(3, weight=1)

        ttk.Label(basic_frame, text="Timestamp:").grid(
            row=0, column=0, sticky="w", padx=(0, 5)
        )
        self.timestamp_label = ttk.Label(
            basic_frame, text="N/A", background="white", relief="sunken"
        )
        self.timestamp_label.grid(row=0, column=1, sticky="ew", padx=(0, 10))

        ttk.Label(basic_frame, text="Estrutura:").grid(
            row=0, column=2, sticky="w", padx=(0, 5)
        )
        self.structure_label = ttk.Label(
            basic_frame, text="N/A", background="white", relief="sunken"
        )
        self.structure_label.grid(row=0, column=3, sticky="ew")

        ttk.Label(basic_frame, text="Decisão:").grid(
            row=1, column=0, sticky="w", padx=(0, 5)
        )
        self.decision_label = ttk.Label(
            basic_frame, text="N/A", background="white", relief="sunken"
        )
        self.decision_label.grid(row=1, column=1, sticky="ew", padx=(0, 10))

        ttk.Label(basic_frame, text="Nível:").grid(
            row=1, column=2, sticky="w", padx=(0, 5)
        )
        self.level_label = ttk.Label(
            basic_frame, text="N/A", background="white", relief="sunken"
        )
        self.level_label.grid(row=1, column=3, sticky="ew")

        # Métricas Financeiras
        metrics_frame = ttk.LabelFrame(self, text="Métricas Financeiras", padding=5)
        metrics_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
        metrics_frame.grid_columnconfigure(1, weight=1)
        metrics_frame.grid_columnconfigure(3, weight=1)

        ttk.Label(metrics_frame, text="PL Atual:").grid(
            row=0, column=0, sticky="w", padx=(0, 5)
        )
        self.pl_atual_label = ttk.Label(
            metrics_frame, text="N/A", background="white", relief="sunken"
        )
        self.pl_atual_label.grid(row=0, column=1, sticky="ew", padx=(0, 10))

        ttk.Label(metrics_frame, text="PL Máximo:").grid(
            row=0, column=2, sticky="w", padx=(0, 5)
        )
        self.pl_max_label = ttk.Label(
            metrics_frame, text="N/A", background="white", relief="sunken"
        )
        self.pl_max_label.grid(row=0, column=3, sticky="ew")

        ttk.Label(metrics_frame, text="Ratio:").grid(
            row=1, column=0, sticky="w", padx=(0, 5)
        )
        self.ratio_label = ttk.Label(
            metrics_frame, text="N/A", background="white", relief="sunken"
        )
        self.ratio_label.grid(row=1, column=1, sticky="ew", padx=(0, 10))

        ttk.Label(metrics_frame, text="DTE Mín:").grid(
            row=1, column=2, sticky="w", padx=(0, 5)
        )
        self.dte_label = ttk.Label(
            metrics_frame, text="N/A", background="white", relief="sunken"
        )
        self.dte_label.grid(row=1, column=3, sticky="ew")

        ttk.Label(metrics_frame, text="Spot Ref:").grid(
            row=2, column=0, sticky="w", padx=(0, 5)
        )
        self.spot_ref_label = ttk.Label(
            metrics_frame, text="N/A", background="white", relief="sunken"
        )
        self.spot_ref_label.grid(row=2, column=1, sticky="ew", padx=(0, 10))

        ttk.Label(metrics_frame, text="Breakevens:").grid(
            row=2, column=2, sticky="w", padx=(0, 5)
        )
        self.breakevens_label = ttk.Label(
            metrics_frame, text="N/A", background="white", relief="sunken"
        )
        self.breakevens_label.grid(row=2, column=3, sticky="ew")

        # Rationale JSON
        json_frame = ttk.LabelFrame(self, text="Rationale / Why JSON", padding=5)
        json_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(5, 0))
        json_frame.grid_rowconfigure(0, weight=1)
        json_frame.grid_columnconfigure(0, weight=1)

        self.why_text = scrolledtext.ScrolledText(
            json_frame,
            height=8,
            wrap=tk.WORD,
            font=("Consolas", 9),
            background="#f8f9fa",
        )
        self.why_text.grid(row=0, column=0, sticky="nsew")

        # Auditoria & Ações
        audit_frame = ttk.LabelFrame(self, text="Auditoria & Ações", padding=5)
        audit_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)
        audit_frame.grid_columnconfigure(1, weight=1)
        audit_frame.grid_columnconfigure(3, weight=1)

        ttk.Label(audit_frame, text="Fonte:").grid(
            row=0, column=0, sticky="w", padx=(0, 5)
        )
        self.source_label = ttk.Label(
            audit_frame, text="N/A", background="white", relief="sunken"
        )
        self.source_label.grid(row=0, column=1, sticky="ew", padx=(0, 10))

        ttk.Label(audit_frame, text="Created At:").grid(
            row=0, column=2, sticky="w", padx=(0, 5)
        )
        self.created_at_label = ttk.Label(
            audit_frame, text="N/A", background="white", relief="sunken"
        )
        self.created_at_label.grid(row=0, column=3, sticky="ew")

        actions_frame = ttk.Frame(audit_frame)
        actions_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(5, 0))

        self.btn_recalculate = ttk.Button(
            actions_frame,
            text="Recalcular esta estrutura",
            command=self._on_recalculate_click,
        )
        self.btn_recalculate.pack(side="left", padx=(0, 10))

        self.lbl_recalc_status = ttk.Label(
            actions_frame, text="", foreground="gray"
        )
        self.lbl_recalc_status.pack(side="left")

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def update_decision(self, decision_data: Dict):
        self._current_decision = dict(decision_data) if decision_data else None

        self.timestamp_label.config(text=decision_data.get("timestamp", "N/A"))

        # patch_36: structure_id é autoritativo; aba removido
        structure_id = decision_data.get("structure_id") or "N/A"
        self.structure_label.config(text=str(structure_id))

        self.decision_label.config(text=decision_data.get("decision", "N/A"))
        self.level_label.config(text=str(decision_data.get("level", "N/A")))

        self._format_currency_label(self.pl_atual_label, decision_data.get("pl_atual"))
        self._format_currency_label(self.pl_max_label, decision_data.get("pl_max"))

        ratio = decision_data.get("pl_pct_of_max")
        self.ratio_label.config(
            text=f"{ratio * 100:.1f}%" if ratio is not None else "N/A"
        )

        self.dte_label.config(text=str(decision_data.get("dte_min", "N/A")))

        spot_ref = decision_data.get("spot_reference") or decision_data.get("spot_ref")
        if spot_ref is not None:
            try:
                self.spot_ref_label.config(text=f"{float(spot_ref):.2f}")
            except Exception:
                self.spot_ref_label.config(text=str(spot_ref))
        else:
            self.spot_ref_label.config(text="N/A")

        why_payload = decision_data.get("why") or decision_data.get("why_json")
        self.why_text.delete("1.0", tk.END)
        if why_payload:
            try:
                if isinstance(why_payload, str):
                    formatted = json.dumps(
                        json.loads(why_payload), indent=2, ensure_ascii=False
                    )
                else:
                    formatted = json.dumps(why_payload, indent=2, ensure_ascii=False)
                self.why_text.insert("1.0", formatted)
            except Exception:
                self.why_text.insert("1.0", str(why_payload))
        else:
            self.why_text.insert("1.0", "Sem rationale disponível")

        self.source_label.config(text="N/A")
        self.created_at_label.config(text="N/A")
        self.lbl_recalc_status.config(text="", foreground="gray")

    def update_breakevens(self, breakevens, pl_at_spot_ref):
        if breakevens:
            try:
                self.breakevens_label.config(
                    text=", ".join([f"{float(be):.2f}" for be in breakevens])
                )
            except Exception:
                self.breakevens_label.config(text=str(breakevens))
        else:
            self.breakevens_label.config(text="N/A")

    def update_audit_info(self, info: Dict):
        source_table = info.get("source_table", "N/A")
        n = info.get("count_points", info.get("points_count", ""))
        suffix = f" ({n} pts)" if n != "" else ""
        txt = f"{source_table}{suffix}"
        if info.get("fallback"):
            txt += " [fallback]"
        self.source_label.config(text=txt)

        created_at = info.get("created_at")
        self.created_at_label.config(text=created_at if created_at else "N/A")

    def clear(self):
        self._current_decision = None
        for lbl in [
            self.timestamp_label, self.structure_label, self.decision_label,
            self.level_label, self.pl_atual_label, self.pl_max_label,
            self.ratio_label, self.dte_label, self.spot_ref_label,
            self.breakevens_label, self.source_label, self.created_at_label,
        ]:
            lbl.config(text="N/A")
        self.why_text.delete("1.0", tk.END)
        self.lbl_recalc_status.config(text="", foreground="gray")

    def on_recalc_finished(self, structure_id, ok: bool, message: str = ""):
        """Chamado pelo MainWindow ao finalizar o subprocess do pipeline."""
        try:
            if ok:
                self._last_recalc_signature = self._compute_recalc_signature(
                    structure_id
                )
                self._set_recalc_ui_state(
                    False,
                    msg=message or f"OK: {structure_id} recalculado",
                    color="green",
                )
            else:
                self._set_recalc_ui_state(
                    False,
                    msg=message or "Falha no recálculo",
                    color="red",
                )
        except Exception:
            self._recalc_in_progress = False

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
            label.config(text=str(value))

    def _fetch_latest_decision_from_derived(
        self, structure_id
    ) -> Optional[Dict[str, Any]]:
        """
        patch_36: filtra por structure_id (INTEGER) em structure_decisions.
        Legado aba removido.
        """
        sid = self._resolve_structure_key(structure_id)
        db_path = self._derived_db_path()
        con = sqlite3.connect(str(db_path))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        try:
            select_cols = [
                "structure_id", "timestamp", "decision", "level",
                "pl_atual", "pl_max", "pl_pct_of_max", "dte_min",
                "spot_ref", "meta_json", "created_at", "why_json",
            ]

            row = cur.execute(
                f"""
                SELECT {", ".join(select_cols)}
                FROM structure_decisions
                WHERE structure_id = ?
                ORDER BY COALESCE(created_at, timestamp) DESC
                LIMIT 1
                """,
                (sid,),
            ).fetchone()

            if not row:
                return None

            d = dict(row)
            if d.get("why_json") is not None:
                d["why"] = d["why_json"]

            d["spot_reference"] = d.pop("spot_ref", None)
            return d
        finally:
            con.close()

    def _fetch_payoff_points_from_derived(self, structure_id):
        """
        patch_36: filtra por structure_id (INTEGER) em payoff_curve_points.
        Legado aba removido.
        """
        sid = self._resolve_structure_key(structure_id)
        db_path = self._derived_db_path()
        con = sqlite3.connect(str(db_path))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        try:
            rows = cur.execute(
                """
                SELECT point_spot, point_pl
                FROM payoff_curve_points
                WHERE structure_id = ?
                ORDER BY point_spot ASC
                """,
                (sid,),
            ).fetchall()
            return [
                (float(r["point_spot"]), float(r["point_pl"]))
                for r in rows
                if r["point_spot"] is not None and r["point_pl"] is not None
            ]
        finally:
            con.close()

    def _fetch_audit_info_from_derived(self, structure_id) -> Dict[str, Any]:
        """
        patch_36: filtra por structure_id (INTEGER).
        Legado aba removido.
        """
        sid = self._resolve_structure_key(structure_id)
        db_path = self._derived_db_path()
        con = sqlite3.connect(str(db_path))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        try:
            row = cur.execute(
                """
                SELECT created_at, timestamp
                FROM structure_decisions
                WHERE structure_id = ?
                ORDER BY COALESCE(created_at, timestamp) DESC
                LIMIT 1
                """,
                (sid,),
            ).fetchone()

            created_at = None
            if row:
                created_at = row["created_at"] or row["timestamp"]

            n_points = cur.execute(
                "SELECT COUNT(*) AS n FROM payoff_curve_points WHERE structure_id = ?",
                (sid,),
            ).fetchone()["n"]

            return {
                "source_table": "derived.db:structure_decisions / payoff_curve_points",
                "created_at": created_at,
                "count_points": n_points,
                "fallback": False,
            }
        finally:
            con.close()

    def _compute_breakevens_from_points(self, pts):
        if not pts or len(pts) < 2:
            return []
        breakevens = []
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            if y1 == 0.0:
                breakevens.append(x1)
                continue
            if y2 == 0.0:
                breakevens.append(x2)
                continue
            if (y1 < 0.0 and y2 > 0.0) or (y1 > 0.0 and y2 < 0.0):
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

    def _on_recalculate_click(self):
        decision = self._current_decision
        if not decision:
            self.lbl_recalc_status.config(
                text="Nenhuma decisão selecionada", foreground="red"
            )
            return

        # patch_36: structure_id é único identificador
        structure_id = decision.get("structure_id")
        if not structure_id:
            self.lbl_recalc_status.config(
                text="Estrutura não identificada", foreground="red"
            )
            return

        if getattr(self, "_recalc_in_progress", False):
            self._set_recalc_ui_state(
                True,
                msg=f"Recalc já em andamento ({structure_id})",
                color="orange",
            )
            return

        sig = self._compute_recalc_signature(structure_id)
        if self._last_recalc_signature == sig and sig[1] is not None:
            self._set_recalc_ui_state(
                False,
                msg="Snapshot não mudou; recálculo desnecessário",
                color="gray",
            )
            return

        if callable(getattr(self, "_on_recalculate_cb", None)):
            self._set_recalc_ui_state(
                True,
                msg=f"Recalculando {structure_id}...",
                color="blue",
            )
            try:
                self._on_recalculate_cb(structure_id)
                self._last_recalc_signature = sig
            except Exception as e:
                self._set_recalc_ui_state(
                    False, msg="Erro ao iniciar recálculo", color="red"
                )
                print(f"[UI] Erro delegando recalc: {e}")
            return

        self.lbl_recalc_status.config(
            text="Recalc indisponível: callback não configurado",
            foreground="red",
        )
