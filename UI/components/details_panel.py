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
        self._explicit_app_db_path = str(app_db_path) if app_db_path else None
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


    def _app_db_path(self) -> Path:
        """
        Caminho do app.db.

        Ordem:
        - usa app_db_path recebido no construtor;
        - se houver db_path/_db_path explícito em testes/compatibilidade, usa esse arquivo;
        - caso contrário, respeita self._project_root quando definido;
        - fallback final: raiz do projeto inferida pelo arquivo atual.
        """
        if self._explicit_app_db_path:
            return Path(self._explicit_app_db_path)

        for attr in ("db_path", "_db_path", "database_path", "_database_path"):
            value = getattr(self, attr, None)
            if value and not callable(value):
                return Path(value)

        project_root = getattr(self, "_project_root", None)
        if project_root is None:
            project_root = Path(__file__).resolve().parents[2]
        else:
            project_root = Path(project_root)

        return project_root / "dados" / "app.db"

    def _operational_app_db_path(self) -> Path:
        """
        Caminho do app.db usado para estado operacional.

        Importante: não usa self._db_path porque _app_db_path() já trata
        esse atributo como caminho do app.db em testes/compatibilidade.
        """
        if self._explicit_app_db_path:
            return Path(self._explicit_app_db_path)

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
        sid = self._resolve_structure_key(structure_id)
        sid_text = str(sid)

        for db_path in self._snapshot_candidate_db_paths():
            ts = self._latest_snapshot_timestamp_in_db(db_path, sid, sid_text)
            if ts is not None:
                return ts

        return None

    def _snapshot_candidate_db_paths(self):
        explicit_paths = self._explicit_instance_db_paths()

        if explicit_paths:
            return self._unique_paths(explicit_paths)

        return self._unique_paths(self._default_snapshot_db_paths())

    def _explicit_instance_db_paths(self):
        instance_dict = getattr(self, "__dict__", {}) or {}

        # No fluxo bd-unico-appdb, app_db_path recebido no construtor é
        # autoridade máxima para consultas operacionais/snapshot.
        explicit_app_path = self._safe_db_path(
            instance_dict.get("_explicit_app_db_path")
        )
        if explicit_app_path is not None and self._looks_like_db_path(
            "_explicit_app_db_path",
            explicit_app_path,
        ):
            return [explicit_app_path]

        ordered_names = self._ordered_instance_db_attribute_names(instance_dict)

        primary_explicit = []
        app_explicit = []

        for name in ordered_names:
            path = self._safe_db_path(instance_dict.get(name))
            if path is None or not self._looks_like_db_path(name, path):
                continue

            if self._is_app_db_path(name, path):
                app_explicit.append(path)
            else:
                primary_explicit.append(path)

        if primary_explicit:
            return primary_explicit

        return app_explicit

    def _ordered_instance_db_attribute_names(self, instance_dict):
        preferred_names = [
            "_explicit_app_db_path",
            "app_db_path",
            "_raw_db_path",
            "raw_db_path",
            "_db_path",
            "db_path",
            "_database_path",
            "database_path",
            "_sqlite_path",
            "sqlite_path",
            "_db_file",
            "db_file",
        ]

        ordered_names = []
        for name in preferred_names:
            if name in instance_dict and name not in ordered_names:
                ordered_names.append(name)

        for name in instance_dict:
            if name not in ordered_names:
                ordered_names.append(name)

        return ordered_names

    def _default_snapshot_db_paths(self):
        """
        Caminho default canônico para snapshots.

        No bd-unico-appdb, o caminho único é o app.db canônico
        resolvido por _app_db_path().
        """
        return [self._app_db_path()]

    def _safe_db_path(self, value):
        from pathlib import Path

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

    def _looks_like_db_path(self, name, path):
        from pathlib import Path

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

    def _is_app_db_path(self, name, path):
        low_name = str(name).lower()
        low_path = str(path).lower()

        return (
            "derived" in low_name
            or "deriv" in low_name
            or low_path.endswith("app.db")
            or "app.db" in low_path
        )

    def _unique_paths(self, paths):
        unique = []
        seen = set()

        for path in paths:
            key = self._path_identity(path)
            if key in seen:
                continue

            seen.add(key)
            unique.append(path)

        return unique

    def _path_identity(self, path):
        try:
            return str(path.resolve()) if path.exists() else str(path)
        except Exception:
            return str(path)

    def _latest_snapshot_timestamp_in_db(self, db_path, sid, sid_text):
        import sqlite3

        if not db_path.exists():
            return None

        try:
            con = sqlite3.connect(str(db_path))
            try:
                return self._latest_snapshot_timestamp_in_connection(con, sid, sid_text)
            finally:
                con.close()
        except sqlite3.Error:
            return None

    def _latest_snapshot_timestamp_in_connection(self, con, sid, sid_text):
        cur = con.cursor()
        tables = self._snapshot_ordered_table_names(cur)

        for table in tables:
            ts = self._latest_snapshot_timestamp_in_table(cur, table, sid, sid_text)
            if ts is not None:
                return ts

        return None

    def _snapshot_ordered_table_names(self, cur):
        tables = self._table_names(cur)
        preferred = [
            "robo_legs_snapshot",
            "robo_snapshot",
            "snapshots",
            "snapshot",
            "structure_snapshots",
            "structure_decisions",
            "payoff_curve_points",
        ]

        ordered = []
        for table in preferred:
            if table in tables and table not in ordered:
                ordered.append(table)

        for table in tables:
            if table not in ordered:
                ordered.append(table)

        return ordered

    def _table_names(self, cur):
        rows = cur.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            """
        ).fetchall()
        return [row[0] for row in rows]

    def _table_columns(self, cur, table):
        rows = cur.execute(
            f"PRAGMA table_info({self._quote_sql_identifier(table)})"
        ).fetchall()
        return [row[1] for row in rows]

    def _quote_sql_identifier(self, identifier):
        return '"' + str(identifier).replace('"', '""') + '"'

    def _latest_snapshot_timestamp_in_table(self, cur, table, sid, sid_text):
        cols = self._table_columns(cur, table)
        if not cols:
            return None

        structure_cols = self._structure_columns(cols)
        if not structure_cols:
            return None

        timestamp_cols = self._timestamp_columns(cols, structure_cols)
        return self._best_timestamp_for_structure(
            cur,
            table,
            structure_cols,
            timestamp_cols,
            sid,
            sid_text,
        )

    def _structure_columns(self, cols):
        structure_cols = [
            col
            for col in cols
            if self._looks_like_structure_column(col)
        ]

        if structure_cols:
            return structure_cols

        return [
            col
            for col in cols
            if str(col).lower() in {"structure", "estrutura"}
        ]

    def _looks_like_structure_column(self, col):
        low = str(col).lower()
        return (
            low == "structure_id"
            or low == "id_structure"
            or low == "estrutura_id"
            or low == "id_estrutura"
            or low.endswith("_structure_id")
            or low.endswith("_estrutura_id")
        )

    def _timestamp_columns(self, cols, structure_cols):
        timestamp_cols = sorted(
            [
                col
                for col in cols
                if self._timestamp_column_score(col) > 0
            ],
            key=self._timestamp_column_score,
            reverse=True,
        )

        if timestamp_cols:
            return timestamp_cols

        return self._fallback_timestamp_columns(cols, structure_cols)

    def _timestamp_column_score(self, col):
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

    def _fallback_timestamp_columns(self, cols, structure_cols):
        ignored = {str(col).lower() for col in structure_cols}
        ignored.update(
            {
                "id",
                "structure_id",
                "id_structure",
                "estrutura_id",
                "id_estrutura",
            }
        )

        return [
            col
            for col in cols
            if str(col).lower() not in ignored
        ]

    def _best_timestamp_for_structure(
        self,
        cur,
        table,
        structure_cols,
        timestamp_cols,
        sid,
        sid_text,
    ):
        best = None

        for structure_col in structure_cols:
            for timestamp_col in timestamp_cols:
                value = self._max_timestamp_for_structure_column(
                    cur,
                    table,
                    structure_col,
                    timestamp_col,
                    sid,
                    sid_text,
                )
                if value is not None and (best is None or value > best):
                    best = value

        return best

    def _max_timestamp_for_structure_column(
        self,
        cur,
        table,
        structure_col,
        timestamp_col,
        sid,
        sid_text,
    ):
        import sqlite3

        try:
            row = cur.execute(
                f"""
                SELECT MAX({self._quote_sql_identifier(timestamp_col)})
                FROM {self._quote_sql_identifier(table)}
                WHERE {self._quote_sql_identifier(structure_col)} = ?
                   OR CAST({self._quote_sql_identifier(structure_col)} AS TEXT) = ?
                """,
                (sid, sid_text),
            ).fetchone()
        except sqlite3.Error:
            return None

        if row and row[0] is not None:
            return str(row[0])

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
        self._configure_details_panel_grid()
        self._setup_basic_info_frame()
        self._setup_metrics_frame()
        self._setup_operational_frame()
        self._setup_why_json_frame()
        self._setup_audit_actions_frame()

    def _configure_details_panel_grid(self):
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def _setup_basic_info_frame(self):
        frame = self._create_two_column_label_frame(
            "Informações Básicas",
            row=0,
            pady=(0, 5),
        )

        self._add_value_field(frame, "Timestamp:", "timestamp_label", 0, 0)
        self._add_value_field(frame, "Estrutura:", "structure_label", 0, 2, value_padx=0)
        self._add_value_field(frame, "Decisão:", "decision_label", 1, 0)
        self._add_value_field(frame, "Nível:", "level_label", 1, 2, value_padx=0)

    def _setup_metrics_frame(self):
        frame = self._create_two_column_label_frame(
            "Métricas Financeiras",
            row=1,
            pady=5,
        )

        self._add_value_field(frame, "PL Atual:", "pl_atual_label", 0, 0)
        self._add_value_field(frame, "PL Máximo:", "pl_max_label", 0, 2, value_padx=0)
        self._add_value_field(frame, "Ratio:", "ratio_label", 1, 0)
        self._add_value_field(frame, "DTE Mín:", "dte_label", 1, 2, value_padx=0)
        self._add_value_field(frame, "Spot Ref:", "spot_ref_label", 2, 0)
        self._add_value_field(frame, "Breakevens:", "breakevens_label", 2, 2, value_padx=0)

    def _setup_operational_frame(self):
        frame = self._create_two_column_label_frame(
            "Estado Operacional",
            row=2,
            pady=5,
        )

        self._add_value_field(
            frame,
            "Eventos aplicados:",
            "operational_events_applied_label",
            0,
            0,
        )
        self._add_value_field(
            frame,
            "Cancelados ignorados:",
            "operational_cancelled_ignored_label",
            0,
            2,
            value_padx=0,
        )
        self._add_value_field(
            frame,
            "Status:",
            "operational_status_label",
            1,
            0,
            columnspan=3,
            value_padx=0,
        )

    def _setup_why_json_frame(self):
        json_frame = ttk.LabelFrame(self, text="Rationale / Why JSON", padding=5)
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

    def _setup_audit_actions_frame(self):
        audit_frame = self._create_two_column_label_frame(
            "Auditoria & Ações",
            row=4,
            pady=5,
        )

        self._add_value_field(audit_frame, "Fonte:", "source_label", 0, 0)
        self._add_value_field(
            audit_frame,
            "Created At:",
            "created_at_label",
            0,
            2,
            value_padx=0,
        )
        self._setup_recalculate_actions(audit_frame)

    def _create_two_column_label_frame(self, title, row, pady):
        frame = ttk.LabelFrame(self, text=title, padding=5)
        frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=pady)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(3, weight=1)
        return frame

    def _add_value_field(
        self,
        frame,
        label_text,
        attr_name,
        row,
        label_column,
        columnspan=1,
        value_padx=(0, 10),
    ):
        if value_padx == 0:
            value_padx = 0

        value_column = label_column + 1

        ttk.Label(frame, text=label_text).grid(
            row=row,
            column=label_column,
            sticky="w",
            padx=(0, 5),
        )

        value_label = ttk.Label(
            frame,
            text="N/A",
            background="white",
            relief="sunken",
        )
        value_label.grid(
            row=row,
            column=value_column,
            columnspan=columnspan,
            sticky="ew",
            padx=value_padx,
        )

        setattr(self, attr_name, value_label)
        return value_label

    def _setup_recalculate_actions(self, audit_frame):
        actions_frame = ttk.Frame(audit_frame)
        actions_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(5, 0))

        self.btn_recalculate = ttk.Button(
            actions_frame,
            text="Recalcular esta estrutura",
            command=self._on_recalculate_click,
        )
        self.btn_recalculate.pack(side="left", padx=(0, 10))

        self.lbl_recalc_status = ttk.Label(
            actions_frame,
            text="",
            foreground="gray",
        )
        self.lbl_recalc_status.pack(side="left")

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def update_decision(self, decision_data: Dict):
        self._current_decision = dict(decision_data) if decision_data else None

        self._update_basic_decision_labels(decision_data)
        self._update_financial_decision_labels(decision_data)
        self._update_decision_why_text(decision_data)
        self._reset_decision_audit_state()
        self._refresh_decision_operational_state(decision_data)

    def _update_basic_decision_labels(self, decision_data: Dict):
        self.timestamp_label.config(text=decision_data.get("timestamp", "N/A"))

        # alteracao_36: structure_id é autoritativo; aba removido
        structure_id = self._decision_structure_id_for_details(decision_data)
        self.structure_label.config(text=str(structure_id))

        self.decision_label.config(text=decision_data.get("decision", "N/A"))
        self.level_label.config(text=str(decision_data.get("level", "N/A")))

    def _decision_structure_id_for_details(self, decision_data: Dict):
        return decision_data.get("structure_id") or "N/A"

    def _update_financial_decision_labels(self, decision_data: Dict):
        self._format_currency_label(self.pl_atual_label, decision_data.get("pl_atual"))
        self._format_currency_label(self.pl_max_label, decision_data.get("pl_max"))

        self.ratio_label.config(
            text=self._format_ratio_text(decision_data.get("pl_pct_of_max"))
        )
        self.dte_label.config(text=str(decision_data.get("dte_min", "N/A")))
        self.spot_ref_label.config(
            text=self._format_spot_reference_text(decision_data)
        )

    def _format_ratio_text(self, ratio):
        return f"{ratio * 100:.1f}%" if ratio is not None else "N/A"

    def _format_spot_reference_text(self, decision_data: Dict):
        spot_ref = decision_data.get("spot_reference") or decision_data.get("spot_ref")

        if spot_ref is None:
            return "N/A"

        try:
            return f"{float(spot_ref):.2f}"
        except Exception:
            return str(spot_ref)

    def _update_decision_why_text(self, decision_data: Dict):
        why_payload = decision_data.get("why") or decision_data.get("why_json")
        self.why_text.delete("1.0", tk.END)
        self.why_text.insert("1.0", self._format_why_payload_text(why_payload))

    def _format_why_payload_text(self, why_payload):
        if not why_payload:
            return "Sem rationale disponível"

        try:
            if isinstance(why_payload, str):
                return json.dumps(
                    json.loads(why_payload),
                    indent=2,
                    ensure_ascii=False,
                )

            return json.dumps(why_payload, indent=2, ensure_ascii=False)
        except Exception:
            return str(why_payload)

    def _reset_decision_audit_state(self):
        self.source_label.config(text="N/A")
        self.created_at_label.config(text="N/A")
        self.lbl_recalc_status.config(text="", foreground="gray")
        self._clear_operational_state()

    def _refresh_decision_operational_state(self, decision_data: Dict):
        structure_id = self._decision_structure_id_for_details(decision_data)

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

        created_at = info.get("created_at")
        self.created_at_label.config(text=created_at if created_at else "N/A")

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
        """Chamado pelo MainWindow ao finalizar o fluxo externo legado do pipeline."""
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

        Aceita o formato retornado por StructureEventsService.apply_events_to_structure
        e formatos legados/testes com is_closed no topo, applied_events e ignored_events.
        """
        if not isinstance(effective_structure, dict):
            self._clear_operational_state()
            return

        values = self._operational_state_values(effective_structure)
        self._apply_operational_state_values(values)

    def _operational_state_values(self, effective_structure: Dict[str, Any]):
        state = self._operational_state_dict(effective_structure)

        return {
            "applied": self._operational_applied_count(effective_structure, state),
            "ignored": self._operational_ignored_count(effective_structure, state),
            "status": self._operational_status_text(effective_structure, state),
        }

    def _operational_state_dict(self, effective_structure: Dict[str, Any]):
        state = effective_structure.get("operational_state")

        if isinstance(state, dict):
            return state

        return {}

    def _operational_applied_count(self, effective_structure: Dict[str, Any], state: Dict[str, Any]):
        applied = state.get("events_applied")

        if applied is None and isinstance(effective_structure.get("applied_events"), list):
            return len(effective_structure.get("applied_events") or [])

        return applied

    def _operational_ignored_count(self, effective_structure: Dict[str, Any], state: Dict[str, Any]):
        ignored = state.get("events_ignored_cancelled")

        if ignored is None and isinstance(effective_structure.get("ignored_events"), list):
            return len(effective_structure.get("ignored_events") or [])

        return ignored

    def _operational_status_text(self, effective_structure: Dict[str, Any], state: Dict[str, Any]):
        is_closed = state.get("is_closed", effective_structure.get("is_closed"))

        if is_closed is True:
            return "Encerrada"

        if is_closed is False:
            return "Aberta"

        return "N/A"

    def _apply_operational_state_values(self, values):
        self.operational_events_applied_label.config(
            text=self._display_count_or_na(values["applied"])
        )
        self.operational_cancelled_ignored_label.config(
            text=self._display_count_or_na(values["ignored"])
        )
        self.operational_status_label.config(text=values["status"])

    def _display_count_or_na(self, value):
        return str(value) if value is not None else "N/A"

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

    def _fetch_latest_decision_from_app_db(
        self, structure_id
    ) -> Optional[Dict[str, Any]]:
        """
        alteracao_36: filtra por structure_id (INTEGER) em structure_decisions.
        Legado aba removido.
        """
        sid = self._resolve_structure_key(structure_id)
        db_path = self._app_db_path()
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

    def _fetch_payoff_points_from_app_db(self, structure_id):
        """
        alteracao_36: filtra por structure_id (INTEGER) em payoff_curve_points.
        Legado aba removido.
        """
        sid = self._resolve_structure_key(structure_id)
        db_path = self._app_db_path()
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

    def _fetch_audit_info_from_app_db(self, structure_id) -> Dict[str, Any]:
        """
        alteracao_36: filtra por structure_id (INTEGER).
        Legado aba removido.
        """
        sid = self._resolve_structure_key(structure_id)
        db_path = self._app_db_path()
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
                "source_table": "app.db:structure_decisions / payoff_curve_points",
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

    def _refresh_current_from_app_db(self, structure_id):
        """Recarrega somente a estrutura atual do app.db e atualiza widgets."""
        decision = self._fetch_latest_decision_from_app_db(structure_id)
        if decision:
            self.update_decision(decision)

        pts = self._fetch_payoff_points_from_app_db(structure_id)
        breakevens = self._compute_breakevens_from_points(pts)

        spot_ref = None
        if decision:
            spot_ref = decision.get("spot_reference")

        pl_at_spot = self._compute_pl_at_spot(pts, spot_ref)
        self.update_breakevens(breakevens, pl_at_spot)

        audit = self._fetch_audit_info_from_app_db(structure_id)
        self.update_audit_info(audit)

    # ------------------------------------------------------------------
    # Recalc click
    # ------------------------------------------------------------------

    def _on_recalculate_click(self):
        structure_id = self._selected_recalculate_structure_id()
        if not structure_id:
            return

        if self._recalculate_already_in_progress(structure_id):
            return

        signature = self._compute_recalc_signature(structure_id)
        if self._recalculate_snapshot_unchanged(signature):
            return

        self._start_recalculate_callback(structure_id, signature)

    def _selected_recalculate_structure_id(self):
        decision = self._current_decision
        if not decision:
            self.lbl_recalc_status.config(
                text="Nenhuma decisão selecionada",
                foreground="red",
            )
            return None

        # alteracao_36: structure_id é único identificador
        structure_id = decision.get("structure_id")
        if not structure_id:
            self.lbl_recalc_status.config(
                text="Estrutura não identificada",
                foreground="red",
            )
            return None

        return structure_id

    def _recalculate_already_in_progress(self, structure_id):
        if not getattr(self, "_recalc_in_progress", False):
            return False

        self._set_recalc_ui_state(
            True,
            msg=f"Recalc já em andamento ({structure_id})",
            color="orange",
        )
        return True

    def _recalculate_snapshot_unchanged(self, signature):
        if self._last_recalc_signature != signature or signature[1] is None:
            return False

        self._set_recalc_ui_state(
            False,
            msg="Snapshot não mudou; recálculo desnecessário",
            color="gray",
        )
        return True

    def _start_recalculate_callback(self, structure_id, signature):
        if not callable(getattr(self, "_on_recalculate_cb", None)):
            self.lbl_recalc_status.config(
                text="Recalc indisponível: callback não configurado",
                foreground="red",
            )
            return

        self._set_recalc_ui_state(
            True,
            msg=f"Recalculando {structure_id}...",
            color="blue",
        )

        try:
            self._on_recalculate_cb(structure_id)
            self._last_recalc_signature = signature
        except Exception as exc:
            self._set_recalc_ui_state(
                False,
                msg="Erro ao iniciar recálculo",
                color="red",
            )
            print(f"[UI] Erro delegando recalc: {exc}")
