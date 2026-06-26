from UI.components.ptbr_labels import decision_to_label
# UI/components/details_panel.py
import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Dict, Optional, Any
import json
import sqlite3
from pathlib import Path


class DetailsPanel(ttk.LabelFrame):
    def __init__(self, parent, on_recalculate=None, app_db_path=None):
        super().__init__(parent)
        self._on_recalculate_cb = on_recalculate
        self._app_db_path = str(app_db_path) if app_db_path else None
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

    def set_update_status(self, message: str, color: str = "gray"):
        """Atualiza o indicador visual de atualização dos dados exibidos."""
        try:
            if hasattr(self, "lbl_update_status") and self.lbl_update_status:
                self.lbl_update_status.config(text=message or "", foreground=color)
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Caminhos de DB
    # ------------------------------------------------------------------


    def _derived_db_path(self) -> Path:
        """
        Caminho do derived.db.

        Compatibilidade para testes:
        - se o painel tiver db_path/_db_path explícito, usa esse arquivo;
        - caso contrário, respeita self._project_root quando definido;
        - fallback final: raiz do projeto inferida pelo arquivo atual.
        """
        for attr in ("db_path", "_db_path", "database_path", "_database_path"):
            value = getattr(self, attr, None)
            if value and not callable(value):
                return Path(value)

        project_root = getattr(self, "_project_root", None)
        if project_root is None:
            project_root = Path(__file__).resolve().parents[2]
        else:
            project_root = Path(project_root)

        return project_root / "dados" / "derived.db"

    def _operational_app_db_path(self) -> Path:
        """
        Caminho do app.db usado para estado operacional.

        Importante: não usa self._db_path porque _derived_db_path() já trata
        esse atributo como caminho do derived.db em testes/compatibilidade.
        """
        if self._app_db_path:
            return Path(self._app_db_path)

        project_root = getattr(self, "_project_root", None)
        if project_root is None:
            project_root = Path(__file__).resolve().parents[2]
        else:
            project_root = Path(project_root)

        return project_root / "dados" / "app.db"

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

    def _get_latest_snapshot_timestamp_for_structure(self, structure_id):
        """
        Retorna o timestamp mais recente de snapshot para uma estrutura.

        Regra importante para compatibilidade com alteracao_35:
        - se a instância recebeu um caminho explícito de DB, usa somente ele;
        - se esse DB explícito não existe, retorna None;
        - só usa fallback em bancos default quando não há DB explícito na instância.
        """
        import sqlite3
        from pathlib import Path

        sid = self._resolve_structure_key(structure_id)
        sid_text = str(sid)

        def _safe_path(value):
            if value is None:
                return None
            try:
                if callable(value):
                    value = value()
            except TypeError:
                return None
            if value is None:
                return None
            try:
                return Path(value)
            except TypeError:
                return None

        def _looks_like_db_path(name, path):
            low_name = str(name).lower()
            try:
                suffix = Path(path).suffix.lower()
            except Exception:
                suffix = ""

            return (
                suffix in {".db", ".sqlite", ".sqlite3"}
                or "db" in low_name
                or "database" in low_name
                or "sqlite" in low_name
            )

        candidates = []
        primary_explicit = []
        derived_explicit = []

        # 1) Caminhos explicitamente configurados NA INSTÂNCIA.
        #
        # Regra crítica:
        # se existe raw/app DB explícito, usa SOMENTE ele.
        # Não pode cair para derived.db quando o raw/app não existe.
        instance_dict = getattr(self, "__dict__", {}) or {}

        preferred_instance_names = [
            "_raw_db_path",
            "raw_db_path",
            "_app_db_path",
            "app_db_path",
            "_db_path",
            "db_path",
            "_database_path",
            "database_path",
            "_sqlite_path",
            "sqlite_path",
            "_db_file",
            "db_file",
            "_derived_db_path",
            "derived_db_path",
        ]

        ordered_instance_names = []
        for name in preferred_instance_names:
            if name in instance_dict and name not in ordered_instance_names:
                ordered_instance_names.append(name)

        for name in instance_dict:
            if name not in ordered_instance_names:
                ordered_instance_names.append(name)

        for name in ordered_instance_names:
            value = instance_dict.get(name)
            p = _safe_path(value)
            if p is None:
                continue
            if not _looks_like_db_path(name, p):
                continue

            low_name = str(name).lower()
            low_path = str(p).lower()

            is_derived = (
                "derived" in low_name
                or "deriv" in low_name
                or low_path.endswith("derived.db")
                or "derived.db" in low_path
            )

            if is_derived:
                derived_explicit.append(p)
            else:
                primary_explicit.append(p)

        if primary_explicit:
            candidates = primary_explicit
        elif derived_explicit:
            candidates = derived_explicit
        else:
            # 2) Sem DB explícito na instância: agora sim pode usar defaults.
            class_level_names = [
                "_derived_db_path",
                "derived_db_path",
                "_raw_db_path",
                "raw_db_path",
                "_app_db_path",
                "app_db_path",
                "_db_path",
                "db_path",
                "_database_path",
                "database_path",
                "_sqlite_path",
                "sqlite_path",
                "_db_file",
                "db_file",
            ]

            for name in class_level_names:
                try:
                    attr = getattr(self, name, None)
                except Exception:
                    attr = None

                p = _safe_path(attr)
                if p is not None and _looks_like_db_path(name, p):
                    candidates.append(p)

            project_root = getattr(self, "_project_root", None)
            if project_root is not None:
                project_root = Path(project_root)
            else:
                project_root = Path(__file__).resolve().parents[2]

            candidates.extend(
                [
                    project_root / "app.db",
                    project_root / "app2.db",
                    project_root / "derived.db",
                    project_root / "dados" / "app.db",
                    project_root / "dados" / "app2.db",
                    project_root / "dados" / "derived.db",
                ]
            )

            for base in [project_root, project_root / "dados"]:
                try:
                    candidates.extend(sorted(base.glob("*.db")))
                except Exception:
                    pass

        # Remove duplicados preservando ordem.
        unique = []
        seen = set()
        for p in candidates:
            try:
                key = str(p.resolve()) if p.exists() else str(p)
            except Exception:
                key = str(p)
            if key not in seen:
                seen.add(key)
                unique.append(p)

        def q(identifier):
            return '"' + str(identifier).replace('"', '""') + '"'

        def table_names(cur):
            rows = cur.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                  AND name NOT LIKE 'sqlite_%'
                """
            ).fetchall()
            return [r[0] for r in rows]

        def columns_for(cur, table):
            rows = cur.execute(f"PRAGMA table_info({q(table)})").fetchall()
            return [r[1] for r in rows]

        def looks_like_structure_col(col):
            low = str(col).lower()
            return (
                low == "structure_id"
                or low == "id_structure"
                or low == "estrutura_id"
                or low == "id_estrutura"
                or low.endswith("_structure_id")
                or low.endswith("_estrutura_id")
            )

        def timestamp_score(col):
            low = str(col).lower()

            priority = {
                "timestamp": 100,
                "snapshot_timestamp": 99,
                "snapshot_ts": 98,
                "created_at": 97,
                "updated_at": 96,
                "ts": 95,
                "datetime": 94,
                "date": 93,
                "data_hora": 92,
            }

            if low in priority:
                return priority[low]

            if "timestamp" in low:
                return 90
            if "snapshot" in low and ("time" in low or "date" in low or "ts" in low):
                return 89
            if low.endswith("_ts"):
                return 88
            if "created" in low:
                return 87
            if "updated" in low:
                return 86
            if "time" in low:
                return 85
            if "date" in low:
                return 84
            if "data" in low:
                return 83

            return 0

        def latest_in_table(cur, table):
            cols = columns_for(cur, table)
            if not cols:
                return None

            structure_cols = [c for c in cols if looks_like_structure_col(c)]

            if not structure_cols:
                for c in cols:
                    low = str(c).lower()
                    if low in {"structure", "estrutura"}:
                        structure_cols.append(c)

            if not structure_cols:
                return None

            ts_cols = sorted(
                [c for c in cols if timestamp_score(c) > 0],
                key=timestamp_score,
                reverse=True,
            )

            if not ts_cols:
                ignored = {str(c).lower() for c in structure_cols}
                ignored.update(
                    {
                        "id",
                        "structure_id",
                        "id_structure",
                        "estrutura_id",
                        "id_estrutura",
                    }
                )
                ts_cols = [c for c in cols if str(c).lower() not in ignored]

            best = None

            for s_col in structure_cols:
                for ts_col in ts_cols:
                    try:
                        row = cur.execute(
                            f"""
                            SELECT MAX({q(ts_col)})
                            FROM {q(table)}
                            WHERE {q(s_col)} = ?
                               OR CAST({q(s_col)} AS TEXT) = ?
                            """,
                            (sid, sid_text),
                        ).fetchone()
                    except sqlite3.Error:
                        continue

                    if row and row[0] is not None:
                        value = str(row[0])
                        if best is None or value > best:
                            best = value

            return best

        preferred = [
            "robo_legs_snapshot",
            "robo_snapshot",
            "snapshots",
            "snapshot",
            "structure_snapshots",
            "structure_decisions",
            "payoff_curve_points",
        ]

        for db_path in unique:
            if not db_path.exists():
                continue

            try:
                con = sqlite3.connect(str(db_path))
                try:
                    cur = con.cursor()
                    tables = table_names(cur)

                    ordered = []
                    for t in preferred:
                        if t in tables and t not in ordered:
                            ordered.append(t)
                    for t in tables:
                        if t not in ordered:
                            ordered.append(t)

                    for table in ordered:
                        ts = latest_in_table(cur, table)
                        if ts is not None:
                            return ts
                finally:
                    con.close()
            except sqlite3.Error:
                continue

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
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Informações Básicas
        basic_frame = ttk.LabelFrame(self, text="Informações Básicas", padding=5)
        basic_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        basic_frame.grid_columnconfigure(1, weight=1)
        basic_frame.grid_columnconfigure(3, weight=1)

        ttk.Label(basic_frame, text="Data/Hora:").grid(
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

        ttk.Label(metrics_frame, text="Razão:").grid(
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

        ttk.Label(metrics_frame, text="Preço ref.:").grid(
            row=2, column=0, sticky="w", padx=(0, 5)
        )
        self.spot_ref_label = ttk.Label(
            metrics_frame, text="N/A", background="white", relief="sunken"
        )
        self.spot_ref_label.grid(row=2, column=1, sticky="ew", padx=(0, 10))

        ttk.Label(metrics_frame, text="Pontos de equilíbrio:").grid(
            row=2, column=2, sticky="w", padx=(0, 5)
        )
        self.breakevens_label = ttk.Label(
            metrics_frame, text="N/A", background="white", relief="sunken"
        )
        self.breakevens_label.grid(row=2, column=3, sticky="ew")

        # Estado Operacional
        operational_frame = ttk.LabelFrame(self, text="Estado Operacional", padding=5)
        operational_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)
        operational_frame.grid_columnconfigure(1, weight=1)
        operational_frame.grid_columnconfigure(3, weight=1)

        ttk.Label(operational_frame, text="Eventos aplicados:").grid(
            row=0, column=0, sticky="w", padx=(0, 5)
        )
        self.operational_events_applied_label = ttk.Label(
            operational_frame, text="N/A", background="white", relief="sunken"
        )
        self.operational_events_applied_label.grid(
            row=0, column=1, sticky="ew", padx=(0, 10)
        )

        ttk.Label(operational_frame, text="Cancelados ignorados:").grid(
            row=0, column=2, sticky="w", padx=(0, 5)
        )
        self.operational_cancelled_ignored_label = ttk.Label(
            operational_frame, text="N/A", background="white", relief="sunken"
        )
        self.operational_cancelled_ignored_label.grid(
            row=0, column=3, sticky="ew"
        )

        ttk.Label(operational_frame, text="Status:").grid(
            row=1, column=0, sticky="w", padx=(0, 5)
        )
        self.operational_status_label = ttk.Label(
            operational_frame, text="N/A", background="white", relief="sunken"
        )
        self.operational_status_label.grid(
            row=1, column=1, columnspan=3, sticky="ew"
        )

        # Justificativa JSON
        json_frame = ttk.LabelFrame(self, text="Justificativa / JSON", padding=5)
        json_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(5, 0))
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
        audit_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)
        audit_frame.grid_columnconfigure(1, weight=1)
        audit_frame.grid_columnconfigure(3, weight=1)

        ttk.Label(audit_frame, text="Fonte:").grid(
            row=0, column=0, sticky="w", padx=(0, 5)
        )
        self.source_label = ttk.Label(
            audit_frame, text="N/A", background="white", relief="sunken"
        )
        self.source_label.grid(row=0, column=1, sticky="ew", padx=(0, 10))

        ttk.Label(audit_frame, text="Criado em:").grid(
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

        update_status_frame = ttk.Frame(audit_frame)
        update_status_frame.grid(
            row=2, column=0, columnspan=4, sticky="ew", pady=(6, 0)
        )
        update_status_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(update_status_frame, text="Atualização visual:").grid(
            row=0, column=0, sticky="w", padx=(0, 5)
        )
        self.lbl_update_status = ttk.Label(
            update_status_frame,
            text="Aguardando atualização",
            foreground="gray",
        )
        self.lbl_update_status.grid(row=0, column=1, sticky="ew")

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def update_decision(self, decision_data: Dict):
        self._current_decision = dict(decision_data) if decision_data else None

        self.timestamp_label.config(text=decision_data.get("timestamp", "N/A"))

        # alteracao_36: structure_id é autoritativo; aba removido
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
        self._clear_operational_state()

        if structure_id != "N/A":
            self._refresh_operational_state_for_structure(structure_id)

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

        created_at_raw = info.get("created_at")
        updated_at_raw = info.get("updated_at")

        try:
            from core.datetime_utils import format_datetime_local
            created_at = format_datetime_local(created_at_raw, default="")
            updated_at = format_datetime_local(updated_at_raw, default="")
        except Exception:
            created_at = str(created_at_raw)[:19] if created_at_raw else ""
            updated_at = str(updated_at_raw)[:19] if updated_at_raw else ""

        if created_at and updated_at and created_at != updated_at:
            self.created_at_label.config(
                text=f"Criado: {created_at} | Atualizado: {updated_at}"
            )
        elif created_at:
            self.created_at_label.config(text=created_at)
        elif updated_at:
            self.created_at_label.config(text=f"Atualizado: {updated_at}")
        else:
            self.created_at_label.config(text="N/A")

    def clear(self):
        self._current_decision = None
        for lbl in [
            self.timestamp_label, self.structure_label, self.decision_label,
            self.level_label, self.pl_atual_label, self.pl_max_label,
            self.ratio_label, self.dte_label, self.spot_ref_label,
            self.breakevens_label, self.source_label, self.created_at_label,
            self.operational_events_applied_label,
            self.operational_cancelled_ignored_label,
            self.operational_status_label,
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

    def _clear_operational_state(self):
        for label_name in [
            "operational_events_applied_label",
            "operational_cancelled_ignored_label",
            "operational_status_label",
        ]:
            label = getattr(self, label_name, None)
            if label is not None:
                label.config(text="N/A")

    def update_operational_state(self, effective_structure: Dict[str, Any]):
        """
        Atualiza os widgets de Estado Operacional.

        Aceita o formato retornado por StructureEventsService.apply_events_to_structure:
        {
            "legs": [...],
            "operational_state": {
                "events_applied": int,
                "events_ignored_cancelled": int,
                "is_closed": bool,
            }
        }

        Também aceita formatos legados/testes com:
        - is_closed no topo;
        - applied_events;
        - ignored_events.
        """
        if not isinstance(effective_structure, dict):
            self._clear_operational_state()
            return

        state = effective_structure.get("operational_state")
        if not isinstance(state, dict):
            state = {}

        applied = state.get("events_applied")
        if applied is None and isinstance(effective_structure.get("applied_events"), list):
            applied = len(effective_structure.get("applied_events") or [])

        ignored = state.get("events_ignored_cancelled")
        if ignored is None and isinstance(effective_structure.get("ignored_events"), list):
            ignored = len(effective_structure.get("ignored_events") or [])

        is_closed = state.get("is_closed", effective_structure.get("is_closed"))

        if is_closed is True:
            status_text = "Encerrada"
        elif is_closed is False:
            status_text = "Aberta"
        else:
            status_text = "N/A"

        self.operational_events_applied_label.config(
            text=str(applied) if applied is not None else "N/A"
        )
        self.operational_cancelled_ignored_label.config(
            text=str(ignored) if ignored is not None else "N/A"
        )
        self.operational_status_label.config(text=status_text)

    def _fetch_effective_structure_local(self, structure_id) -> Optional[Dict[str, Any]]:
        """
        Busca estado efetivo pela camada local já existente.

        A UI atualmente não usa HTTP. Por isso este método usa diretamente
        repositories/services com o mesmo app.db da UI.
        Se a camada local não estiver disponível, falha silenciosamente
        e mantém N/A na tela.
        """
        try:
            sid = self._resolve_structure_key(structure_id)
        except Exception:
            return None

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
            label.config(text=str(value))

    def _fetch_latest_decision_from_derived(
        self, structure_id
    ) -> Optional[Dict[str, Any]]:
        """
        alteracao_36: filtra por structure_id (INTEGER) em structure_decisions.
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
                ORDER BY datetime(timestamp) DESC, id DESC
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
        alteracao_36: filtra por structure_id (INTEGER) em payoff_curve_points.
        Legado aba removido.

        Correção temporal:
        - busca somente o snapshot mais recente da estrutura;
        - ordena timestamps ISO com timezone usando datetime(timestamp);
        - evita misturar pontos de payoff de recálculos antigos e novos.
        """
        sid = self._resolve_structure_key(structure_id)
        db_path = self._derived_db_path()
        con = sqlite3.connect(str(db_path))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        try:
            latest_ts_row = cur.execute(
                """
                SELECT timestamp
                FROM payoff_curve_points
                WHERE structure_id = ?
                GROUP BY timestamp
                ORDER BY datetime(timestamp) DESC
                LIMIT 1
                """,
                (sid,),
            ).fetchone()

            if not latest_ts_row or not latest_ts_row["timestamp"]:
                return []

            latest_ts = latest_ts_row["timestamp"]

            rows = cur.execute(
                """
                SELECT point_spot, point_pl
                FROM payoff_curve_points
                WHERE structure_id = ?
                  AND timestamp = ?
                ORDER BY point_spot ASC
                """,
                (sid, latest_ts),
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
        alteracao_36: filtra por structure_id (INTEGER).
        Legado aba removido.

        Correção temporal:
        - created_at representa o primeiro snapshot conhecido da estrutura;
        - updated_at representa o último snapshot conhecido da estrutura;
        - ambos priorizam timestamp operacional com timezone;
        - ordenação usa datetime(timestamp), não comparação textual.
        """
        sid = self._resolve_structure_key(structure_id)
        db_path = self._derived_db_path()
        con = sqlite3.connect(str(db_path))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        try:
            created_row = cur.execute(
                """
                SELECT timestamp, created_at
                FROM structure_decisions
                WHERE structure_id = ?
                ORDER BY datetime(timestamp) ASC, id ASC
                LIMIT 1
                """,
                (sid,),
            ).fetchone()

            updated_row = cur.execute(
                """
                SELECT timestamp, created_at
                FROM structure_decisions
                WHERE structure_id = ?
                ORDER BY datetime(timestamp) DESC, id DESC
                LIMIT 1
                """,
                (sid,),
            ).fetchone()

            created_at = None
            updated_at = None

            if created_row:
                created_at = created_row["timestamp"] or created_row["created_at"]

            if updated_row:
                updated_at = updated_row["timestamp"] or updated_row["created_at"]

            latest_payoff_row = cur.execute(
                """
                SELECT timestamp, COUNT(*) AS n
                FROM payoff_curve_points
                WHERE structure_id = ?
                GROUP BY timestamp
                ORDER BY datetime(timestamp) DESC
                LIMIT 1
                """,
                (sid,),
            ).fetchone()

            latest_payoff_timestamp = None
            n_points = 0

            if latest_payoff_row:
                latest_payoff_timestamp = latest_payoff_row["timestamp"]
                n_points = int(latest_payoff_row["n"] or 0)

            return {
                "source_table": "derived.db:structure_decisions / payoff_curve_points",
                "created_at": created_at,
                "updated_at": updated_at,
                "latest_decision_timestamp": updated_at,
                "latest_payoff_timestamp": latest_payoff_timestamp,
                "n_points": n_points,
                "count_points": n_points,
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

        # alteracao_36: structure_id é único identificador
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

        # Botão manual: deve recalcular sempre que o usuário clicar.
        # A assinatura é mantida apenas para diagnóstico/estado, não para bloquear.
        sig = self._compute_recalc_signature(structure_id)

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
