# UI/components/terminal_vwap_payoff_dark_panel.py
#!/usr/bin/env python3
"""
Painel operacional dark para análise VWAP e Payoff.

Layout:
- barra lateral fixa;
- painel lateral retrátil de estruturas;
- balões/KPIs superiores;
- blocos grandes para VWAP e Payoff;
- tabela inferior de pernas;
- avisos operacionais.

O painel lê dados do banco dados/app.db com introspecção defensiva de schema.
Quando não há curva de payoff persistida, calcula uma curva estimada a partir
das pernas da estrutura.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple
import math
import os
import sqlite3
import tkinter as tk
from tkinter import ttk

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog, messagebox

try:
    from repositories.structures_repository import StructuresRepository
except Exception:
    StructuresRepository = None

try:
    from UI.components.structure_editor_dialog import StructureEditorDialog
except Exception:
    StructureEditorDialog = None

try:
    from services.rtd_option_quotes_intraday_candle_chart_service import (
        RtdOptionQuotesIntradayCandleChartService,
    )
except Exception:
    RtdOptionQuotesIntradayCandleChartService = None



DARK_BG = "#121212"
RAIL_BG = "#1E1E1E"
SIDE_BG = "#252526"
CARD_BG = "#1E1E1E"
CARD_BG_2 = "#181818"
TEXT = "#F5F5F5"
MUTED = "#A3A3A3"
GREEN = "#10B981"
BLUE = "#1F538D"
YELLOW = "#EAB308"
RED = "#EF4444"
GRID = "#333333"


def _q(name: str) -> str:
    return '"' + str(name).replace('"', '""') + '"'


def _norm(name: str) -> str:
    return str(name or "").strip().lower()


def _first_col(cols: Sequence[str], candidates: Sequence[str]) -> Optional[str]:
    lookup = {_norm(c): c for c in cols}
    for cand in candidates:
        if _norm(cand) in lookup:
            return lookup[_norm(cand)]
    return None


def _to_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    if value is None:
        return default
    if isinstance(value, (int, float)):
        if math.isfinite(float(value)):
            return float(value)
        return default
    text = str(value).strip()
    if not text:
        return default
    text = text.replace("R$", "").replace(" ", "")
    if "," in text and "." in text:
        text = text.replace(".", "").replace(",", ".")
    elif "," in text:
        text = text.replace(",", ".")
    try:
        val = float(text)
        if math.isfinite(val):
            return val
    except Exception:
        pass
    return default


def _money(value: Any) -> str:
    val = _to_float(value)
    if val is None:
        return "N/A"
    return "R$ " + f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _number(value: Any) -> str:
    val = _to_float(value)
    if val is None:
        return "N/A"
    return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# BEGIN AUTO STRUCTURE DECISION HELPERS
if "DECISION_LABELS" not in globals():
    DECISION_LABELS = {
        "HOLD": "Manter",
        "ADJUST": "Ajustar",
        "CLOSE": "Encerrar",
    }


def decision_label(value: Any) -> str:
    if value is None:
        return "--"
    raw = str(value).strip()
    return DECISION_LABELS.get(raw.upper(), raw)
# END AUTO STRUCTURE DECISION HELPERS

class TerminalVWAPPayoffDarkPanel(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        db_path: str,
        on_status=None,
        app_service=None,
    ) -> None:
        super().__init__(parent, fg_color=DARK_BG)

        self.db_path = str(db_path)
        self.on_status = on_status or (lambda _msg: None)
        self._app_service = app_service

        self.menu_visible = True
        self.structures: List[Dict[str, Any]] = []
        self.selected_structure: Optional[Dict[str, Any]] = None

        self.canvas_vwap: Optional[FigureCanvasTkAgg] = None
        self.canvas_payoff: Optional[FigureCanvasTkAgg] = None
        self.fig_payoff: Optional[Figure] = None

        self._intraday_candle_chart_service = (
            RtdOptionQuotesIntradayCandleChartService(self.db_path)
            if RtdOptionQuotesIntradayCandleChartService is not None
            else None
        )

        self.kpi_labels: Dict[str, ctk.CTkLabel] = {}

        self._setup_style()
        self._setup_layout()
        self.reload_structures()

    def _setup_style(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Dark.Treeview",
            background=CARD_BG,
            foreground=TEXT,
            fieldbackground=CARD_BG,
            bordercolor=GRID,
            rowheight=26,
        )
        style.configure(
            "Dark.Treeview.Heading",
            background=CARD_BG_2,
            foreground=TEXT,
            relief="flat",
        )
        style.map(
            "Dark.Treeview",
            background=[("selected", BLUE)],
            foreground=[("selected", TEXT)],
        )

    def _setup_layout(self) -> None:
        self._configure_layout_grid()
        self._build_rail_panel()
        self._build_side_panel()
        self._build_main_panel()
        self._build_main_header()
        self._build_kpi_panel()
        self._build_chart_panels()
        self._build_bottom_panel()
        self._build_legs_table()
        self._build_alerts_box()
        self._render_empty_charts()

        # Auto-refresh: UI apenas consome snapshots persistidos.
        # Configure com TERMINAL_VWAP_PAYOFF_REFRESH_SECONDS=10.
        self._start_auto_refresh_loop()

    def _configure_layout_grid(self) -> None:
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def _build_rail_panel(self) -> None:
        self._build_rail_container()
        self._build_rail_toggle_button()
        self._build_rail_reload_button()
        self._build_rail_new_button()
        self._build_rail_actions_button()
        self._build_rail_open_button()

    def _build_rail_container(self) -> None:
        self.rail = ctk.CTkFrame(
            self,
            width=70,
            corner_radius=0,
            fg_color=RAIL_BG,
        )
        self.rail.grid(row=0, column=0, sticky="nsew")
        self.rail.grid_propagate(False)

    def _build_rail_toggle_button(self) -> None:
        self.btn_toggle = ctk.CTkButton(
            self.rail,
            text="☰\n\nID",
            width=50,
            height=58,
            fg_color="#111827",
            hover_color="#1F2937",
            text_color=TEXT,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.toggle_structures_panel,
        )
        self.btn_toggle.pack(pady=(20, 8), padx=10)

    def _build_rail_reload_button(self) -> None:
        self.btn_reload_fixed = ctk.CTkButton(
            self.rail,
            text="↻",
            width=50,
            height=44,
            fg_color="#111827",
            hover_color="#1F2937",
            text_color=BLUE,
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.reload_structures,
        )
        self.btn_reload_fixed.pack(pady=6, padx=10)

    def _build_rail_new_button(self) -> None:
        self.btn_new_fixed = ctk.CTkButton(
            self.rail,
            text="+",
            width=50,
            height=44,
            fg_color="#064E3B",
            hover_color="#065F46",
            text_color=TEXT,
            font=ctk.CTkFont(size=22, weight="bold"),
            command=self.new_structure,
        )
        self.btn_new_fixed.pack(pady=6, padx=10)

    def _build_rail_actions_button(self) -> None:
        self.btn_struct_actions = ctk.CTkButton(
            self.rail,
            text="Acoes",
            width=50,
            height=44,
            fg_color="#312E81",
            hover_color="#3730A3",
            text_color=TEXT,
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._render_structure_actions,
        )
        self.btn_struct_actions.pack(pady=6, padx=10)

    def _build_rail_open_button(self) -> None:
        self.btn_open_fixed = ctk.CTkButton(
            self.rail,
            text="ID",
            width=50,
            height=44,
            fg_color="#1F2937",
            hover_color="#374151",
            text_color=MUTED,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.toggle_structures_panel,
        )
        self.btn_open_fixed.pack(pady=6, padx=10)


    def _build_side_panel(self) -> None:
        self.side = ctk.CTkFrame(
            self,
            width=255,
            corner_radius=0,
            fg_color=SIDE_BG,
        )
        self.side.grid(row=0, column=1, sticky="nsew")
        self.side.grid_propagate(False)

    def _build_main_panel(self) -> None:
        self.main = ctk.CTkFrame(
            self,
            fg_color=DARK_BG,
        )
        self.main.grid(row=0, column=2, sticky="nsew", padx=15, pady=15)
        self.main.grid_columnconfigure((0, 1), weight=1)
        self.main.grid_rowconfigure(2, weight=3)
        self.main.grid_rowconfigure(3, weight=1)

    def _build_main_header(self) -> None:
        self.header = ctk.CTkLabel(
            self.main,
            text="Selecione uma estrutura no menu lateral para carregar a VWAP e Payoff",
            text_color=TEXT,
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.header.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

    def _build_kpi_panel(self) -> None:
        self.kpi_frame = ctk.CTkFrame(
            self.main,
            fg_color="transparent",
        )
        self.kpi_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        self.kpi_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self._create_kpi("preco", "Preço atual", "N/A", 0)
        self._create_kpi("vwap", "VWAP", "N/A", 1)
        self._create_kpi("diff", "Preço vs VWAP", "N/A", 2)
        self._create_kpi("pontos", "Pontos payoff", "0", 3)
        self._create_kpi("minmax", "Min / Máx", "N/A", 4)
        self._create_kpi("be", "Break-even", "N/A", 5)

    def _build_chart_panels(self) -> None:
        self.frame_vwap = ctk.CTkFrame(
            self.main,
            fg_color=CARD_BG,
            corner_radius=10,
        )
        self.frame_vwap.grid(row=2, column=0, sticky="nsew", padx=(0, 10), pady=5)

        self.frame_payoff = ctk.CTkFrame(
            self.main,
            fg_color=CARD_BG,
            corner_radius=10,
        )
        self.frame_payoff.grid(row=2, column=1, sticky="nsew", padx=(10, 0), pady=5)

    def _build_bottom_panel(self) -> None:
        self.bottom = ctk.CTkFrame(
            self.main,
            fg_color=CARD_BG,
            corner_radius=10,
        )
        self.bottom.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(12, 0))
        self.bottom.grid_columnconfigure(0, weight=3)
        self.bottom.grid_columnconfigure(1, weight=1)
        self.bottom.grid_rowconfigure(1, weight=1)

        self.legs_title = ctk.CTkLabel(
            self.bottom,
            text="COMPONENTES DA ESTRUTURA",
            text_color=BLUE,
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        self.legs_title.grid(row=0, column=0, sticky="w", padx=12, pady=(8, 4))

        self.alerts_title = ctk.CTkLabel(
            self.bottom,
            text="AVISOS OPERACIONAIS",
            text_color=YELLOW,
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        self.alerts_title.grid(row=0, column=1, sticky="w", padx=12, pady=(8, 4))

    def _build_legs_table(self) -> None:
        self.legs_table = ttk.Treeview(
            self.bottom,
            columns=("n", "symbol", "side", "type", "strike", "expiration", "qty", "premium"),
            show="headings",
            style="Dark.Treeview",
            height=7,
        )

        headers = {
            "n": "#",
            "symbol": "Símbolo",
            "side": "Lado",
            "type": "Tipo",
            "strike": "Strike",
            "expiration": "Vencimento",
            "qty": "Qtde",
            "premium": "Prêmio",
        }
        widths = {
            "n": 40,
            "symbol": 110,
            "side": 100,
            "type": 80,
            "strike": 90,
            "expiration": 100,
            "qty": 90,
            "premium": 90,
        }

        for col, title in headers.items():
            self.legs_table.heading(col, text=title)
            self.legs_table.column(col, width=widths[col], anchor="center")

        self.legs_table.grid(row=1, column=0, sticky="nsew", padx=(12, 6), pady=(0, 12))

    def _build_alerts_box(self) -> None:
        self.alerts_box = ctk.CTkTextbox(
            self.bottom,
            fg_color=CARD_BG_2,
            text_color=TEXT,
            corner_radius=6,
            font=ctk.CTkFont(family="Consolas", size=12),
        )
        self.alerts_box.grid(row=1, column=1, sticky="nsew", padx=(6, 12), pady=(0, 12))
        self._set_alerts(["Nenhuma estrutura selecionada."])

    def _create_kpi(self, key: str, title: str, value: str, column: int) -> None:
        card = ctk.CTkFrame(
            self.kpi_frame,
            fg_color=CARD_BG,
            corner_radius=10,
        )
        card.grid(row=0, column=column, sticky="ew", padx=5)

        lbl_title = ctk.CTkLabel(
            card,
            text=title,
            text_color=MUTED,
            font=ctk.CTkFont(size=11, weight="bold"),
        )
        lbl_title.pack(anchor="w", padx=12, pady=(8, 0))

        lbl_value = ctk.CTkLabel(
            card,
            text=value,
            text_color=TEXT,
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        lbl_value.pack(anchor="w", padx=12, pady=(0, 8))

        self.kpi_labels[key] = lbl_value

    def toggle_structures_panel(self) -> None:
        if self.menu_visible:
            self.side.grid_remove()
            self.btn_toggle.configure(fg_color=BLUE)
            self.menu_visible = False
        else:
            self.side.grid(row=0, column=1, sticky="nsew")
            self.btn_toggle.configure(fg_color=GREEN)
            self.menu_visible = True
            self._render_structures_list()

    def reload_structures(self) -> None:
        try:
            self.structures = self._load_structures()
        except Exception as exc:
            self.structures = []
            self._render_empty_active_structure_view()
            self._render_structures_list()
            self._safe_status(f"Erro ao carregar estruturas: {exc}")
            return

        self._render_structures_list()
        self._safe_status(f"{len(self.structures)} estruturas carregadas")

    def _render_empty_active_structure_view(self) -> None:
        self.selected_structure = None

        if hasattr(self, "header"):
            self.header.configure(
                text="Selecione uma estrutura no menu lateral para carregar a VWAP e Payoff"
            )

        default_kpis = {
            "preco": "N/A",
            "vwap": "N/A",
            "diff": "N/A",
            "pontos": "0",
            "minmax": "N/A",
            "be": "N/A",
        }

        labels = getattr(self, "kpi_labels", {}) or {}
        for key, value in default_kpis.items():
            label = labels.get(key)
            if label is None:
                continue

            try:
                label.configure(text=value)
            except Exception:
                pass

        render_calls = (
            ("_render_legs", ([],)),
            ("_render_alerts", ({}, [], [])),
            ("_render_empty_charts", ()),
        )

        for method_name, args in render_calls:
            method = getattr(self, method_name, None)
            if not callable(method):
                continue

            try:
                method(*args)
            except Exception:
                pass

    def _connect(self) -> sqlite3.Connection:
        db = Path(self.db_path)
        if not db.exists():
            raise FileNotFoundError(f"Banco app.db não encontrado em: {db}")
        conn = sqlite3.connect(str(db))
        conn.row_factory = sqlite3.Row
        return conn

    def _tables_cols(self, conn: sqlite3.Connection) -> Dict[str, List[str]]:
        rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        result: Dict[str, List[str]] = {}
        for row in rows:
            table = row["name"]
            try:
                cols = conn.execute(f"PRAGMA table_info({_q(table)})").fetchall()
                result[table] = [c["name"] for c in cols]
            except Exception:
                pass
        return result

    def _find_structures_table(self, schema: Dict[str, List[str]]) -> Optional[str]:
        preferred = [
            "structures",
            "structure",
            "option_structures",
            "estruturas",
        ]
        for table in preferred:
            if table in schema:
                return table

        for table, cols in schema.items():
            id_col = _first_col(cols, ["id", "structure_id"])
            name_col = _first_col(cols, ["name", "nome", "structure_name"])
            asset_col = _first_col(cols, ["underlying_asset", "ativo", "asset", "underlying"])
            if id_col and (name_col or asset_col):
                return table

        return None

    def _load_structures(self) -> List[Dict[str, Any]]:
        conn = self._connect()
        try:
            schema = self._tables_cols(conn)
            table = self._find_structures_table(schema)
            if not table:
                return []

            cols = schema[table]
            id_col = _first_col(cols, ["id", "structure_id"])
            name_col = _first_col(cols, ["name", "nome", "structure_name"])
            asset_col = _first_col(cols, ["underlying_asset", "ativo", "asset", "underlying"])
            status_col = _first_col(cols, ["status", "state", "situacao"])

            if not id_col:
                return []

            select_parts = [
                f"{_q(id_col)} AS id",
                f"{_q(name_col)} AS name" if name_col else "NULL AS name",
                f"{_q(asset_col)} AS underlying_asset" if asset_col else "NULL AS underlying_asset",
                f"{_q(status_col)} AS status" if status_col else "NULL AS status",
            ]

            sql = f"SELECT {', '.join(select_parts)} FROM {_q(table)} ORDER BY {_q(id_col)}"
            rows = conn.execute(sql).fetchall()

            structures: List[Dict[str, Any]] = []
            for row in rows:
                item = dict(row)
                item["id"] = item.get("id")
                item["name"] = item.get("name") or f"Estrutura {item.get('id')}"
                item["underlying_asset"] = item.get("underlying_asset") or "N/A"
                item["status"] = item.get("status") or "N/A"
                structures.append(item)

            return structures
        finally:
            conn.close()

    def _render_structures_list(self) -> None:
        self._clear_side()
        self._render_structures_list_actions()
        self._render_structures_list_header()

        scroll = self._build_structures_scroll()
        if not self.structures:
            self._render_empty_structures_message(scroll)
            return

        for structure in self.structures:
            self._render_structure_list_item(scroll, structure)

    def _render_structures_list_actions(self) -> None:
        btn_add = ctk.CTkButton(
            self.side,
            text="+ Nova Estrutura",
            height=32,
            fg_color=GREEN,
            hover_color="#059669",
            text_color=TEXT,
            command=self.new_structure,
        )
        btn_add.pack(fill="x", padx=10, pady=(8, 10))

    def _render_structures_list_header(self) -> None:
        title = ctk.CTkLabel(
            self.side,
            text="ESTRUTURAS DISPONÍVEIS",
            text_color=MUTED,
            font=ctk.CTkFont(size=11, weight="bold"),
        )
        title.pack(pady=(15, 8), padx=10, anchor="w")

        btn_reload = ctk.CTkButton(
            self.side,
            text="Atualizar",
            height=30,
            fg_color=BLUE,
            hover_color="#2563EB",
            command=self.reload_structures,
        )
        btn_reload.pack(fill="x", padx=10, pady=(0, 8))

    def _build_structures_scroll(self):
        scroll = ctk.CTkScrollableFrame(
            self.side,
            fg_color="transparent",
        )
        scroll.pack(fill="both", expand=True, padx=5, pady=5)
        return scroll

    def _render_empty_structures_message(self, parent) -> None:
        lbl = ctk.CTkLabel(
            parent,
            text="Nenhuma estrutura encontrada no app.db",
            text_color=MUTED,
            wraplength=210,
        )
        lbl.pack(fill="x", padx=8, pady=8)

    def _render_structure_list_item(self, parent, structure: Dict[str, Any]) -> None:
        sid = structure.get("id")
        name = structure.get("name")
        asset = structure.get("underlying_asset")
        status = structure.get("status")

        btn = ctk.CTkButton(
            parent,
            text=f"ID {sid} | {asset}\n{name}\n{status}",
            anchor="w",
            height=66,
            fg_color="#2B2B2B",
            hover_color="#3D3D3D",
            text_color=TEXT,
            command=lambda s=structure: self.select_structure(s),
        )
        btn.pack(fill="x", pady=5, padx=5)

    def select_structure(self, structure: Dict[str, Any]) -> None:
        viewmodel = self._build_operational_viewmodel(structure.get("id"))
        payload = self._resolve_operational_payload(structure, viewmodel)

        operational_structure = payload["structure"]
        legs = payload["legs"]
        market = payload["market"]
        payoff_points = payload["payoff_points"]

        self.selected_structure = dict(operational_structure)

        sid = operational_structure.get("id")
        name = operational_structure.get("name")
        asset = operational_structure.get("underlying_asset")

        self.header.configure(
            text=f"Análise ativa: ID {sid} - {name} | Ativo: {asset}"
        )

        self._update_kpis(market, payoff_points)
        self._render_legs(legs)
        self._render_charts(market, payoff_points, asset, legs)
        self._render_alerts(market, payoff_points, legs)

        self.on_status(f"Estrutura carregada: ID {sid}")

        # Menu lateral fixo: não recolher automaticamente após carregar estrutura.

        try:
            self._render_structure_actions()
        except Exception as exc:
            if hasattr(self, "on_status"):
                self.on_status(f"Falha ao abrir painel de acoes: {exc}")

    def _build_operational_viewmodel(self, structure_id: Any) -> Dict[str, Any]:
        service = getattr(self, "_app_service", None)
        if service is None or structure_id in (None, ""):
            return {}

        build = getattr(service, "build_for_structure_id", None)
        if not callable(build):
            return {}

        try:
            result = build(int(structure_id))
        except Exception as exc:
            self._safe_status(
                f"Falha ao carregar viewmodel operacional da estrutura {structure_id}: {exc}"
            )
            return {}

        return self._as_dict(result)

    def _resolve_operational_payload(
        self,
        structure: Dict[str, Any],
        viewmodel: Dict[str, Any],
    ) -> Dict[str, Any]:
        base_structure = dict(structure or {})
        vm_structure = self._first_dict_from(
            viewmodel,
            ("structure", "estrutura"),
        )

        operational_structure = {
            **base_structure,
            **vm_structure,
        }

        sid = operational_structure.get("id") or base_structure.get("id")
        asset = (
            operational_structure.get("underlying_asset")
            or operational_structure.get("asset")
            or base_structure.get("underlying_asset")
            or base_structure.get("asset")
        )

        if sid is not None and not operational_structure.get("id"):
            operational_structure["id"] = sid
        if asset is not None and not operational_structure.get("underlying_asset"):
            operational_structure["underlying_asset"] = asset

        legs = self._first_list_from(
            viewmodel,
            ("legs", "structure_legs", "pernas"),
        )
        if not legs:
            legs = self._as_list(vm_structure.get("legs"))
        if not legs:
            legs = self._load_legs(sid)

        market = self._first_dict_from(
            viewmodel,
            ("market", "market_snapshot", "snapshot"),
        )
        if not market:
            market = self._load_market(asset)

        payoff_points = self._first_list_from(
            viewmodel,
            ("payoff_points", "points", "curve"),
        )
        if not payoff_points:
            payoff = self._first_dict_from(viewmodel, ("payoff",))
            payoff_points = self._first_list_from(
                payoff,
                ("points", "payoff_points", "curve"),
            )
        if not payoff_points:
            payoff_points = self._load_payoff_points(sid, legs)

        return {
            "structure": operational_structure,
            "legs": legs,
            "market": market,
            "payoff_points": payoff_points,
        }

    def _safe_status(self, message: str) -> None:
        try:
            self.on_status(message)
        except Exception:
            pass

    @staticmethod
    def _as_dict(value: Any) -> Dict[str, Any]:
        return dict(value or {}) if isinstance(value, dict) else {}

    @staticmethod
    def _as_list(value: Any) -> List[Any]:
        return list(value or []) if isinstance(value, list) else []

    def _first_dict_from(
        self,
        source: Dict[str, Any],
        keys: tuple[str, ...],
    ) -> Dict[str, Any]:
        for key in keys:
            value = source.get(key) if isinstance(source, dict) else None
            if isinstance(value, dict) and value:
                return dict(value)
        return {}

    def _first_list_from(
        self,
        source: Dict[str, Any],
        keys: tuple[str, ...],
    ) -> List[Any]:
        for key in keys:
            value = source.get(key) if isinstance(source, dict) else None
            if isinstance(value, list) and value:
                return list(value)
        return []

    def _find_legs_table(self, schema: Dict[str, List[str]]) -> Optional[str]:
        preferred = [
            "structure_legs",
            "legs",
            "option_legs",
            "pernas",
            "estrutura_pernas",
        ]
        for table in preferred:
            if table in schema:
                return table

        for table, cols in schema.items():
            sid_col = _first_col(cols, ["structure_id", "id_structure", "estrutura_id"])
            strike_col = _first_col(cols, ["strike", "exercise_price"])
            option_col = _first_col(cols, ["option_type", "tipo", "type"])
            if sid_col and strike_col and option_col:
                return table

        return None

    def _load_legs(self, structure_id: Any) -> List[Dict[str, Any]]:
        conn = self._connect()
        try:
            schema, table = self._load_legs_schema(conn)
            if not table:
                return []

            cols = self._resolve_legs_columns(schema, table)
            if not cols["sid_col"]:
                return []

            select_parts = self._build_legs_select_parts(cols)
            rows = self._fetch_legs_rows(
                conn,
                table,
                cols["sid_col"],
                select_parts,
                structure_id,
            )

            return [dict(row) for row in rows]
        finally:
            conn.close()

    def _load_legs_schema(self, conn: Any) -> tuple[Dict[str, Any], Any]:
        schema = self._tables_cols(conn)
        table = self._find_legs_table(schema)
        return schema, table

    def _resolve_legs_columns(self, schema: Dict[str, Any], table: str) -> Dict[str, Any]:
        cols = schema[table]
        return {
            "sid_col": _first_col(cols, ["structure_id", "id_structure", "estrutura_id"]),
            "symbol_col": _first_col(cols, ["symbol", "simbolo", "ticker"]),
            "side_col": _first_col(cols, ["position_side", "side", "lado"]),
            "type_col": _first_col(cols, ["option_type", "type", "tipo"]),
            "strike_col": _first_col(cols, ["strike", "exercise_price"]),
            "exp_col": _first_col(cols, ["expiration_date", "expiration", "vencimento"]),
            "qty_col": _first_col(cols, ["quantity", "qty", "qtd", "quantidade"]),
            "prem_col": _first_col(cols, ["premium", "premio", "price", "preco"]),
            "mult_col": _first_col(cols, ["multiplier", "multiplicador"]),
        }

    def _build_legs_select_parts(self, cols: Dict[str, Any]) -> List[str]:
        return [
            f"{_q(cols['symbol_col'])} AS symbol" if cols["symbol_col"] else "NULL AS symbol",
            f"{_q(cols['side_col'])} AS position_side" if cols["side_col"] else "NULL AS position_side",
            f"{_q(cols['type_col'])} AS option_type" if cols["type_col"] else "NULL AS option_type",
            f"{_q(cols['strike_col'])} AS strike" if cols["strike_col"] else "NULL AS strike",
            f"{_q(cols['exp_col'])} AS expiration_date" if cols["exp_col"] else "NULL AS expiration_date",
            f"{_q(cols['qty_col'])} AS quantity" if cols["qty_col"] else "NULL AS quantity",
            f"{_q(cols['prem_col'])} AS premium" if cols["prem_col"] else "NULL AS premium",
            f"{_q(cols['mult_col'])} AS multiplier" if cols["mult_col"] else "NULL AS multiplier",
        ]

    def _fetch_legs_rows(
        self,
        conn: Any,
        table: str,
        sid_col: str,
        select_parts: List[str],
        structure_id: Any,
    ) -> List[Any]:
        sql = (
            f"SELECT {', '.join(select_parts)} "
            f"FROM {_q(table)} "
            f"WHERE {_q(sid_col)} = ?"
        )
        return conn.execute(sql, (structure_id,)).fetchall()

    def _load_market(self, asset: Any) -> Dict[str, Any]:
        result = self._empty_market_result()
        asset = self._normalize_market_asset(asset)

        if not asset:
            return result

        conn = self._connect()
        try:
            query = self._build_market_query(conn)
            if not query:
                return result

            rows = conn.execute(query["sql"], (asset,)).fetchall()
            return self._market_result_from_rows(result, rows, query)

        finally:
            conn.close()

    def _empty_market_result(self) -> Dict[str, Any]:
        return {
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

    def _normalize_market_asset(self, asset: Any) -> str:
        asset = str(asset or "").strip().upper()
        if not asset or asset == "N/A":
            return ""
        return asset

    def _build_market_query(self, conn: Any) -> Dict[str, Any]:
        table = "rtd_underlying_quotes"
        schema = self._tables_cols(conn)
        if table not in schema:
            return {}

        colmap = self._market_column_map(schema[table])
        if not colmap.get("asset") or not colmap.get("current_price"):
            return {}

        select_parts = self._market_select_parts(colmap)
        order_sql = self._market_order_sql(colmap)

        sql = (
            f"SELECT {', '.join(select_parts)} "
            f"FROM {_q(table)} "
            f"WHERE UPPER(CAST({_q(colmap['asset'])} AS TEXT)) = UPPER(?)"
            f"{order_sql} "
            f"LIMIT 200"
        )

        return {
            "sql": sql,
            "table": table,
            "has_vwap": bool(colmap.get("vwap")),
        }

    def _market_column_map(self, cols: Sequence[str]) -> Dict[str, Any]:
        return {
            "asset": _first_col(
                cols,
                ["ativo", "underlying_asset", "asset", "ticker", "symbol"],
            ),
            "current_price": _first_col(
                cols,
                ["ultimo_preco", "current_price", "preco_atual", "price", "last_price", "last"],
            ),
            "vwap": _first_col(cols, ["vwap", "vwap_price", "preco_medio"]),
            "bid": _first_col(cols, ["bid"]),
            "ask": _first_col(cols, ["ask"]),
            "close_price": _first_col(cols, ["close_price", "close", "fechamento"]),
            "prev_close": _first_col(
                cols,
                ["prev_close", "previous_close", "fechamento_anterior"],
            ),
            "open_price": _first_col(cols, ["open_price", "open", "abertura"]),
            "high_price": _first_col(cols, ["high_price", "high", "maxima"]),
            "low_price": _first_col(cols, ["low_price", "low", "minima"]),
            "volume": _first_col(cols, ["volume"]),
            "change_percent": _first_col(
                cols,
                ["change_percent", "variation_percent", "variacao_percentual"],
            ),
            "updated_at": _first_col(
                cols,
                ["updated_at", "created_at", "timestamp", "datetime", "dt_ref"],
            ),
            "id": _first_col(cols, ["id"]),
        }

    def _market_select_parts(self, colmap: Dict[str, Any]) -> List[str]:
        specs = [
            ("current_price", "current_price"),
            ("vwap", "vwap"),
            ("bid", "bid"),
            ("ask", "ask"),
            ("close_price", "close_price"),
            ("prev_close", "prev_close"),
            ("open_price", "open_price"),
            ("high_price", "high_price"),
            ("low_price", "low_price"),
            ("volume", "volume"),
            ("change_percent", "change_percent"),
            ("updated_at", "updated_at"),
        ]

        parts = []
        for key, alias in specs:
            col = colmap.get(key)
            parts.append(f"{_q(col)} AS {alias}" if col else f"NULL AS {alias}")
        return parts

    def _market_order_sql(self, colmap: Dict[str, Any]) -> str:
        order_parts = []

        if colmap.get("updated_at"):
            order_parts.append(f"{_q(colmap['updated_at'])} DESC")
        if colmap.get("id"):
            order_parts.append(f"{_q(colmap['id'])} DESC")

        if not order_parts:
            return ""

        return " ORDER BY " + ", ".join(order_parts)

    def _market_result_from_rows(
        self,
        result: Dict[str, Any],
        rows: Any,
        query: Dict[str, Any],
    ) -> Dict[str, Any]:
        if not rows:
            return result

        first = dict(rows[0])
        market_fields = [
            "current_price",
            "vwap",
            "bid",
            "ask",
            "close_price",
            "prev_close",
            "open_price",
            "high_price",
            "low_price",
            "volume",
            "change_percent",
            "updated_at",
        ]

        for field in market_fields:
            result[field] = first.get(field)

        result["source_table"] = query["table"]
        result["vwap_source"] = query["table"] if query.get("has_vwap") else None
        result["series"] = self._market_series_from_rows(rows)
        return result

    def _market_series_from_rows(self, rows: Any) -> List[Dict[str, Any]]:
        series = []

        for idx, row in enumerate(reversed(rows)):
            r = dict(row)
            price = _to_float(r.get("current_price"))
            vwap = _to_float(r.get("vwap"))

            if price is not None or vwap is not None:
                series.append(
                    {
                        "x": idx + 1,
                        "price": price,
                        "vwap": vwap,
                    }
                )

        return series

    def _load_payoff_points(
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
                    # Mantém a intenção explícita para validação arquitetural:
                    # buscar primeiro o último snapshot da estrutura.
                    if table == "payoff_curve_points" and ts_col == "timestamp":
                        latest_sql = (
                            f"SELECT MAX(timestamp) AS ultimo_timestamp "
                            f"FROM {_q(table)} "
                            f"WHERE {_q(sid_col)} = ?"
                        )
                        latest_alias = "ultimo_timestamp"
                    else:
                        latest_sql = (
                            f"SELECT MAX({_q(ts_col)}) AS ultimo_timestamp "
                            f"FROM {_q(table)} "
                            f"WHERE {_q(sid_col)} = ?"
                        )
                        latest_alias = "ultimo_timestamp"

                    latest_row = conn.execute(latest_sql, (structure_id,)).fetchone()

                    if not latest_row or latest_row[latest_alias] is None:
                        continue

                    latest_ts = latest_row[latest_alias]
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

    def _calculate_payoff_from_legs(self, legs: List[Dict[str, Any]]) -> List[Dict[str, float]]:
        strikes = self._collect_payoff_strikes(legs)

        if not strikes:
            return []

        x_min, x_max = self._calculate_payoff_spot_range(strikes)
        return self._calculate_payoff_points_for_range(legs, x_min, x_max)

    def _collect_payoff_strikes(self, legs: List[Dict[str, Any]]) -> List[float]:
        strikes = [_to_float(leg.get("strike")) for leg in legs]
        return [s for s in strikes if s is not None]

    def _calculate_payoff_spot_range(self, strikes: List[float]) -> tuple[float, float]:
        low = min(strikes)
        high = max(strikes)
        span = max(high - low, high * 0.20, 1.0)
        x_min = max(0.01, low - span)
        x_max = high + span
        return x_min, x_max

    def _calculate_payoff_points_for_range(
        self,
        legs: List[Dict[str, Any]],
        x_min: float,
        x_max: float,
    ) -> List[Dict[str, float]]:
        """
        PAYOFF_LOCAL_CALCULATION_BLOCKED_32_13_2
        Calculo local de payoff desabilitado na UI.
        A curva deve ser obtida exclusivamente do backend ou da persistencia oficial.
        """
        return []

    def _calculate_leg_payoff(self, leg: Dict[str, Any], spot: float) -> float:
        strike = _to_float(leg.get("strike"))
        if strike is None:
            return 0.0

        premium = _to_float(leg.get("premium"), 0.0) or 0.0
        quantity = abs(_to_float(leg.get("quantity"), 1.0) or 1.0)
        multiplier = abs(_to_float(leg.get("multiplier"), 1.0) or 1.0)

        side = str(leg.get("position_side") or "").upper()
        opt_type = str(leg.get("option_type") or "").upper()

        sign = -1.0 if self._is_short_payoff_leg(side) else 1.0

        if "PUT" in opt_type:
            intrinsic = max(strike - spot, 0.0)
        else:
            intrinsic = max(spot - strike, 0.0)

        return sign * (intrinsic - premium) * quantity * multiplier

    def _is_short_payoff_leg(self, side: str) -> bool:
        return (
            "VEND" in side
            or "SELL" in side
            or "SHORT" in side
            or side in {"S", "-1"}
        )

    def _breakevens(self, points: List[Dict[str, float]]) -> List[float]:
        bes: List[float] = []
        if len(points) < 2:
            return bes

        for prev, curr in zip(points, points[1:]):
            x1 = prev["spot"]
            y1 = prev["pl"]
            x2 = curr["spot"]
            y2 = curr["pl"]

            if y1 == 0:
                bes.append(x1)
            elif y1 * y2 < 0 and y2 != y1:
                x = x1 + (0 - y1) * (x2 - x1) / (y2 - y1)
                bes.append(x)

        clean: List[float] = []
        for value in bes:
            if not clean or abs(clean[-1] - value) > 0.01:
                clean.append(value)
        return clean

    def _update_kpis(
        self,
        market: Dict[str, Any],
        payoff_points: List[Dict[str, float]],
    ) -> None:
        current_price = _to_float(market.get("current_price"))
        vwap = _to_float(market.get("vwap"))

        self.kpi_labels["preco"].configure(text=_money(current_price))
        self.kpi_labels["vwap"].configure(text=_money(vwap))

        if current_price is not None and vwap is not None:
            diff = current_price - vwap
            diff_pct = diff / vwap * 100 if vwap else 0.0
            color = GREEN if diff >= 0 else RED
            self.kpi_labels["diff"].configure(
                text=f"{_money(diff)} | {diff_pct:.2f}%",
                text_color=color,
            )
        else:
            self.kpi_labels["diff"].configure(text="N/A", text_color=TEXT)

        self.kpi_labels["pontos"].configure(text=str(len(payoff_points)))

        if payoff_points:
            vals = [p["pl"] for p in payoff_points]
            self.kpi_labels["minmax"].configure(
                text=f"{_money(min(vals))} / {_money(max(vals))}"
            )
            bes = self._breakevens(payoff_points)
            if bes:
                self.kpi_labels["be"].configure(
                    text=", ".join(_number(x) for x in bes[:3])
                )
            else:
                self.kpi_labels["be"].configure(text="N/A")
        else:
            self.kpi_labels["minmax"].configure(text="N/A")
            self.kpi_labels["be"].configure(text="N/A")

    def _render_legs(self, legs: List[Dict[str, Any]]) -> None:
        for item in self.legs_table.get_children():
            self.legs_table.delete(item)

        for idx, leg in enumerate(legs, 1):
            self.legs_table.insert(
                "",
                "end",
                values=(
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
                pass
        setattr(self, attr, None)

    def _figure(self) -> Tuple[Figure, Any]:
        fig = Figure(figsize=(5, 3), dpi=100)
        fig.patch.set_facecolor(CARD_BG)
        ax = fig.add_subplot(111)
        ax.set_facecolor(CARD_BG)
        ax.tick_params(colors=MUTED, labelsize=8)
        for spine in ax.spines.values():
            spine.set_color(GRID)
        ax.grid(True, color=GRID, linestyle=":", linewidth=0.8)
        return fig, ax

    def _render_empty_charts(self) -> None:
        self._render_vwap_chart({"series": []}, "N/A")
        self._render_payoff_chart([])

    def _render_charts(
        self,
        market: Dict[str, Any],
        payoff_points: List[Dict[str, float]],
        asset: Any,
        legs: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        market_for_chart = self._market_with_intraday_candle_series(
            market,
            asset,
            legs or [],
        )
        self._render_vwap_chart(market_for_chart, asset)
        self._render_payoff_chart(payoff_points)

    def _market_with_intraday_candle_series(
        self,
        market: Dict[str, Any],
        asset: Any,
        legs: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        enriched = dict(market or {})
        series = self._load_intraday_candle_series(asset, legs)

        if not series:
            return enriched

        enriched["series"] = series
        enriched["series_source"] = "rtd_option_quotes_intraday_candles"

        latest = series[-1]
        if latest.get("price") is not None:
            enriched["current_price"] = latest.get("price")
        if latest.get("vwap") is not None:
            enriched["vwap"] = latest.get("vwap")
            enriched["vwap_source"] = "rtd_option_quotes_intraday_candles"

        return enriched

    def _load_intraday_candle_series(
        self,
        asset: Any,
        legs: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        service = getattr(self, "_intraday_candle_chart_service", None)
        if service is None:
            return []

        for symbol in self._intraday_candle_symbol_candidates(asset, legs):
            try:
                series = service.get_vwap_price_series(
                    symbol=symbol,
                    interval_minutes=1,
                    limit=240,
                )
            except Exception:
                series = []

            if series:
                return series

        return []

    def _intraday_candle_symbol_candidates(
        self,
        asset: Any,
        legs: List[Dict[str, Any]],
    ) -> List[str]:
        candidates: List[str] = []

        def add(value: Any) -> None:
            if value is None:
                return
            text = str(value).strip()
            if not text:
                return
            if text not in candidates:
                candidates.append(text)

        for leg in legs or []:
            if not isinstance(leg, dict):
                continue
            for key in (
                "symbol",
                "codigo_opcao",
                "option_symbol",
                "code",
                "codigo",
                "ticker",
            ):
                add(leg.get(key))

        add(asset)

        return candidates

    def _render_vwap_chart(self, market: Dict[str, Any], asset: Any) -> None:
        ax, fig, series = self._render_vwap_chart_stage_1(market)
        self._render_vwap_chart_stage_2(ax, series, asset)
        self._render_vwap_chart_stage_3(ax, fig)

    def _render_vwap_chart_stage_1(self, market):
        self._clear_canvas("canvas_vwap")

        fig, ax = self._figure()
        series = market.get("series") or []
        return ax, fig, series


    def _normalize_vwap_chart_series(self, series):
        """Normaliza pontos do gráfico VWAP para o contrato interno da UI.

        A renderização espera pontos com pelo menos:
            {"x": ..., "price": ..., "vwap": ...}

        Em runtime, alguns producers entregam chaves como time/timestamp,
        close/last/price/value etc. Este adaptador evita KeyError e mantém
        compatibilidade com os contratos antigos e novos.
        """
        normalized = []

        def first_value(mapping, *keys):
            for key in keys:
                if key in mapping and mapping[key] is not None:
                    return mapping[key]
            return None

        def maybe_float(value):
            if value is None:
                return None
            try:
                return float(value)
            except Exception:
                return value

        for idx, point in enumerate(series or []):
            if isinstance(point, dict):
                x_value = first_value(
                    point,
                    "x",
                    "time",
                    "timestamp",
                    "datetime",
                    "date",
                    "label",
                    "minute",
                    "created_at",
                    "ts",
                )
                price_value = first_value(
                    point,
                    "price",
                    "last",
                    "last_price",
                    "close",
                    "value",
                    "y",
                    "spot",
                    "underlying_price",
                )
                vwap_value = first_value(
                    point,
                    "vwap",
                    "vwap_price",
                    "avg_price",
                    "average_price",
                    "weighted_average_price",
                )

                if x_value is None:
                    x_value = idx

                if price_value is None and vwap_value is not None:
                    price_value = vwap_value

                if vwap_value is None and price_value is not None:
                    vwap_value = price_value

                if price_value is None and vwap_value is None:
                    continue

                normalized_point = dict(point)
                normalized_point["x"] = x_value
                normalized_point["price"] = maybe_float(price_value)
                normalized_point["vwap"] = maybe_float(vwap_value)
                normalized.append(normalized_point)
                continue

            if isinstance(point, (list, tuple)) and len(point) >= 2:
                x_value = point[0]
                price_value = point[1]
                vwap_value = point[2] if len(point) >= 3 else price_value
                normalized.append(
                    {
                        "x": x_value,
                        "price": maybe_float(price_value),
                        "vwap": maybe_float(vwap_value),
                    }
                )

        return normalized

    def _render_vwap_chart_stage_2(self, ax, series, asset) -> None:
        series = self._normalize_vwap_chart_series(series)

        if series:
            xs = [p["x"] for p in series]
            prices = [p.get("price") for p in series]
            vwaps = [p.get("vwap") for p in series]

            if any(p is not None for p in prices):
                ax.plot(
                    xs,
                    [p if p is not None else float("nan") for p in prices],
                    color=TEXT,
                    alpha=0.65,
                    linewidth=1.4,
                    label=f"Preço {asset}",
                )

            if any(v is not None for v in vwaps):
                ax.plot(
                    xs,
                    [v if v is not None else float("nan") for v in vwaps],
                    color=YELLOW,
                    linewidth=2.0,
                    label="VWAP",
                )

            ax.legend(loc="upper left", fontsize=8, frameon=False, labelcolor=TEXT)
            return

        ax.text(
            0.5,
            0.5,
            "VWAP do ativo-base indisponível no app.db",
            color=MUTED,
            ha="center",
            va="center",
            transform=ax.transAxes,
            fontsize=11,
        )
    def _render_vwap_chart_stage_3(self, ax, fig) -> None:
        ax.set_title("Preço atual do ativo-base vs VWAP", color=MUTED, fontsize=10)
        ax.set_xlabel("Amostras", color=MUTED, fontsize=8)
        ax.set_ylabel("Preço", color=MUTED, fontsize=8)

        self.canvas_vwap = FigureCanvasTkAgg(fig, master=self.frame_vwap)
        self.canvas_vwap.draw()
        self.canvas_vwap.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)


    def _render_payoff_chart(self, points: List[Dict[str, float]]) -> None:
        self._clear_canvas("canvas_payoff")
        self.fig_payoff = None
        self._build_payoff_export_button()

        fig, ax = self._figure()
        self.fig_payoff = fig

        if points:
            xs = [p["spot"] for p in points]
            ys = [p["pl"] for p in points]

            color = GREEN if max(ys) >= abs(min(ys)) else RED
            ax.plot(xs, ys, color=color, linewidth=2.0)
            ax.axhline(0, color="#666666", linewidth=1.0)

            bes = self._breakevens(points)
            for be in bes[:5]:
                ax.axvline(be, color=YELLOW, linestyle="--", linewidth=0.8, alpha=0.8)
        else:
            ax.text(
                0.5,
                0.5,
                "Payoff indisponível",
                color=MUTED,
                ha="center",
                va="center",
                transform=ax.transAxes,
                fontsize=11,
            )

        ax.set_title("Payoff Combinado da Estrutura", color=MUTED, fontsize=10)
        ax.set_xlabel("Spot", color=MUTED, fontsize=8)
        ax.set_ylabel("Resultado", color=MUTED, fontsize=8)

        self.canvas_payoff = FigureCanvasTkAgg(fig, master=self.frame_payoff)
        self.canvas_payoff.draw()
        self.canvas_payoff.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def _build_payoff_export_button(self) -> None:
        existing = getattr(self, "btn_export_payoff_png", None)
        try:
            if existing is not None and existing.winfo_exists():
                return
        except Exception:
            pass

        self.btn_export_payoff_png = ctk.CTkButton(
            self.frame_payoff,
            text="Exportar PNG",
            command=self.export_payoff_png,
            width=130,
            height=28,
            fg_color=BLUE,
            hover_color="#2563EB",
            text_color=TEXT,
        )
        self.btn_export_payoff_png.pack(anchor="ne", padx=10, pady=(10, 0))

    def export_payoff_png(self) -> None:
        fig = getattr(self, "fig_payoff", None)
        if fig is None:
            messagebox.showwarning(
                "Exportar PNG",
                "Nenhum grafico de payoff disponivel para exportar.",
                parent=self.winfo_toplevel(),
            )
            self._safe_status("Exportacao PNG indisponivel")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("All files", "*.*")],
            title="Exportar payoff como PNG",
            parent=self.winfo_toplevel(),
        )

        if not file_path:
            self._safe_status("Exportacao PNG cancelada")
            return

        try:
            fig.savefig(file_path, dpi=150, bbox_inches="tight")
            self._safe_status("Payoff exportado em PNG")
            messagebox.showinfo(
                "Exportar PNG",
                f"Grafico salvo em {file_path}",
                parent=self.winfo_toplevel(),
            )
        except Exception as exc:
            self._safe_status("Erro ao exportar PNG")
            messagebox.showerror(
                "Erro ao exportar PNG",
                f"Erro ao salvar: {exc}",
                parent=self.winfo_toplevel(),
            )

    # BEGIN AUTO STRUCTURE SIDE ACTIONS
    def _safe_status(self, message: str) -> None:
        if hasattr(self, "on_status"):
            self.on_status(message)


    def _get_db_path(self) -> str:
        for attr in ("db_path", "database_path", "db_file", "database_file"):
            value = getattr(self, attr, None)
            if value:
                return value
        raise RuntimeError("Caminho do banco nao encontrado. Ajuste o atributo db_path neste componente.")


    def _clear_side(self) -> None:
        for child in self.side.winfo_children():
            child.destroy()


    def _require_selected_structure(self):
        structure = getattr(self, "selected_structure", None)
        if structure:
            return structure

        message = (
            "Nenhuma estrutura selecionada. "
            "Selecione uma estrutura no menu lateral antes de executar esta acao."
        )
        self._safe_status(message)

        try:
            parent = self.winfo_toplevel()
        except Exception:
            parent = None

        messagebox.showwarning(
            "Estrutura",
            message,
            parent=parent,
        )
        return None


    def _require_active_selected_structure(self, action_label: str) -> Optional[Dict[str, Any]]:
        structure = self._require_selected_structure()
        if not structure:
            return None

        if self._is_structure_already_archived(structure):
            self._handle_archived_structure_action_blocked(structure, action_label)
            return None

        return structure

    def _handle_archived_structure_action_blocked(
        self,
        structure: Dict[str, Any],
        action_label: str,
    ) -> None:
        sid = structure.get("id")
        msg = (
            f"Estrutura ID {sid} esta encerrada/arquivada. "
            f"Acao bloqueada: {action_label}."
        )
        self._safe_status(msg)

        try:
            parent = self.winfo_toplevel()
        except Exception:
            parent = None

        messagebox.showwarning(
            "Estrutura arquivada",
            msg,
            parent=parent,
        )

    def _side_section_title(self, text: str) -> None:
        label = ctk.CTkLabel(
            self.side,
            text=text,
            text_color=MUTED,
            font=ctk.CTkFont(size=11, weight="bold"),
            anchor="w",
        )
        label.pack(fill="x", padx=10, pady=(16, 6))


    def _side_button(self, text: str, color: str, hover: str, command) -> None:
        button = ctk.CTkButton(
            self.side,
            text=text,
            height=34,
            fg_color=color,
            hover_color=hover,
            text_color=TEXT,
            command=command,
        )
        button.pack(fill="x", padx=10, pady=4)


    def _ensure_structure_decisions_table(self, conn: sqlite3.Connection) -> None:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS structure_decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                structure_id INTEGER NOT NULL,
                decision TEXT NOT NULL,
                label TEXT,
                note TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_structure_decisions_structure_id
            ON structure_decisions(structure_id)
            """
        )


    def _insert_structure_decision(self, sid: int, decision: str, note: Optional[str] = None) -> None:
        raw_decision = str(decision or "").strip().upper()
        if raw_decision not in DECISION_LABELS:
            raise ValueError(f"Decisao invalida: {decision}")

        label = decision_label(raw_decision)

        with self._connect() as conn:
            self._ensure_structure_decisions_table(conn)
            conn.execute(
                """
                INSERT INTO structure_decisions (
                    structure_id,
                    decision,
                    label,
                    note
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    int(sid),
                    raw_decision,
                    label,
                    note,
                ),
            )
            conn.commit()


    def _load_structure_decisions(self, sid: int, limit: int = 5) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            self._ensure_structure_decisions_table(conn)
            rows = conn.execute(
                """
                SELECT
                    id,
                    structure_id,
                    decision,
                    label,
                    note,
                    created_at
                FROM structure_decisions
                WHERE structure_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (
                    int(sid),
                    int(limit),
                ),
            ).fetchall()

        return [dict(row) for row in rows]


    def _render_decision_history(self, sid: Any) -> None:
        self._side_section_title("ULTIMAS DECISOES")
        box = self._build_decision_history_box()

        try:
            rows = self._load_structure_decisions(int(sid), limit=5)
        except Exception as exc:
            self._render_decision_history_error(box, exc)
            return

        if not rows:
            self._render_empty_decision_history(box)
            return

        for row in rows:
            self._render_decision_history_item(box, row)

    def _build_decision_history_box(self):
        box = ctk.CTkFrame(
            self.side,
            fg_color=CARD_BG_2,
            corner_radius=8,
        )
        box.pack(fill="x", padx=10, pady=(0, 8))
        return box

    def _render_decision_history_error(self, parent, exc: Exception) -> None:
        label = ctk.CTkLabel(
            parent,
            text=f"Historico indisponivel.\n{exc}",
            text_color=YELLOW,
            justify="left",
            anchor="w",
            wraplength=210,
        )
        label.pack(fill="x", padx=10, pady=8)

    def _render_empty_decision_history(self, parent) -> None:
        label = ctk.CTkLabel(
            parent,
            text="Nenhuma decisao registrada para esta estrutura.",
            text_color=MUTED,
            justify="left",
            anchor="w",
            wraplength=210,
        )
        label.pack(fill="x", padx=10, pady=8)

    def _render_decision_history_item(self, parent, row: Dict[str, Any]) -> None:
        decision = str(row.get("decision") or "").upper()
        label_text = row.get("label") or decision_label(decision)
        created_at = row.get("created_at") or "--"
        note = row.get("note") or ""

        text = f"{created_at}\n{label_text} ({decision})"
        if note:
            text += f"\n{note}"

        item = ctk.CTkLabel(
            parent,
            text=text,
            text_color=TEXT,
            justify="left",
            anchor="w",
            wraplength=210,
        )
        item.pack(fill="x", padx=10, pady=(8, 6))



    def _render_structure_actions(self, notice: Optional[str] = None) -> None:
        structure = self._require_selected_structure()
        if not structure:
            self._render_structures_list()
            return

        self._clear_side()

        sid = structure.get("id")
        summary = self._format_active_structure_summary(structure)

        self._render_side_panel_title("ESTRUTURA ATIVA")
        self._render_side_info_card(summary)

        if notice:
            self._render_side_notice_card(notice, fg_color="#064E3B")

        self._render_payoff_action_group()
        self._render_structure_management_action_group()
        self._render_structure_decision_action_group()

        self._render_decision_history(sid)
        self._render_back_to_structures_button()

    def _format_active_structure_summary(self, structure: Dict[str, Any]) -> str:
        sid = structure.get("id")
        name = structure.get("name")
        asset = structure.get("underlying_asset")
        status = structure.get("status")
        return f"ID {sid}\n{name}\nAtivo: {asset}\nStatus: {status}"

    def _render_side_panel_title(self, text: str) -> None:
        title = ctk.CTkLabel(
            self.side,
            text=text,
            text_color=MUTED,
            font=ctk.CTkFont(size=11, weight="bold"),
            anchor="w",
        )
        title.pack(fill="x", pady=(15, 8), padx=10)

    def _render_side_info_card(self, text: str) -> None:
        info_frame = ctk.CTkFrame(self.side, fg_color=CARD_BG_2, corner_radius=8)
        info_frame.pack(fill="x", padx=10, pady=0)

        info = ctk.CTkLabel(
            info_frame,
            text=text,
            text_color=TEXT,
            justify="left",
            anchor="w",
        )
        info.pack(fill="x", padx=10, pady=10)

    def _render_side_notice_card(self, text: str, fg_color: str) -> None:
        notice_frame = ctk.CTkFrame(self.side, fg_color=fg_color, corner_radius=8)
        notice_frame.pack(fill="x", padx=10, pady=(8, 0))

        notice_label = ctk.CTkLabel(
            notice_frame,
            text=text,
            text_color=TEXT,
            justify="left",
            anchor="w",
            wraplength=210,
        )
        notice_label.pack(fill="x", padx=10, pady=8)

    def _render_payoff_action_group(self) -> None:
        self._side_section_title("PAYOFF")
        self._side_button(
            text="Atualizar payoff",
            color=BLUE,
            hover="#2563EB",
            command=self.recalculate_selected_structure,
        )

    def _render_structure_management_action_group(self) -> None:
        self._side_section_title("ESTRUTURA")
        self._side_button(
            text="Editar pernas",
            color=CARD_BG_2,
            hover="#374151",
            command=self.edit_selected_structure,
        )
        self._side_button(
            text="Duplicar estrutura",
            color=CARD_BG_2,
            hover="#374151",
            command=self.duplicate_selected_structure,
        )
        self._side_button(
            text="Arquivar estrutura",
            color="#92400E",
            hover="#78350F",
            command=self.archive_selected_structure,
        )

    def _render_structure_decision_action_group(self) -> None:
        self._side_section_title("DECISAO")
        self._side_button(
            text="Manter",
            color=GREEN,
            hover="#059669",
            command=lambda: self._register_structure_decision("HOLD"),
        )
        self._side_button(
            text="Ajustar / Trocar perna",
            color="#D97706",
            hover="#B45309",
            command=self._render_adjust_structure_block,
        )
        self._side_button(
            text="Encerrar",
            color="#DC2626",
            hover="#991B1B",
            command=lambda: self._register_structure_decision("CLOSE"),
        )

    def _render_back_to_structures_button(self) -> None:
        self._side_button(
            text="Voltar para lista",
            color="#111827",
            hover="#1F2937",
            command=self._render_structures_list,
        )


    def _render_adjust_structure_block(self) -> None:
        structure = self._require_active_selected_structure("ajustar estrutura")
        if not structure:
            return

        self._clear_side()

        sid = structure.get("id")
        summary = self._format_adjust_structure_summary(structure)

        self._safe_status(f"Modo de ajuste aberto: ID {sid}")
        self._render_side_panel_title("AJUSTAR ESTRUTURA")
        self._render_side_info_card(summary)
        self._render_adjust_structure_notice()
        self._render_adjust_structure_actions()

    def _format_adjust_structure_summary(self, structure: Dict[str, Any]) -> str:
        sid = structure.get("id")
        name = structure.get("name")
        asset = structure.get("underlying_asset")
        return f"ID {sid}\n{name}\nAtivo: {asset}"

    def _render_adjust_structure_notice(self) -> None:
        self._render_side_notice_card(
            "Modo de ajuste aberto. Edite as pernas, duplique para ajuste ou registre a decisao ADJUST.",
            fg_color="#78350F",
        )

    def _render_adjust_structure_actions(self) -> None:
        self._side_section_title("ACAO")
        self._side_button(
            text="Editar pernas",
            color=BLUE,
            hover="#2563EB",
            command=self.edit_selected_structure,
        )
        self._side_button(
            text="Duplicar para ajuste",
            color=CARD_BG_2,
            hover="#374151",
            command=self.duplicate_selected_structure,
        )
        self._side_button(
            text="Registrar decisao ADJUST",
            color="#D97706",
            hover="#B45309",
            command=lambda: self._register_structure_decision("ADJUST"),
        )
        self._side_button(
            text="Voltar",
            color="#111827",
            hover="#1F2937",
            command=self._render_structure_actions,
        )


    def new_structure(self) -> None:
        if StructureEditorDialog is None:
            messagebox.showerror(
                "Editor indisponivel",
                "StructureEditorDialog nao foi encontrado.",
                parent=self.winfo_toplevel(),
            )
            return

        try:
            dlg = StructureEditorDialog(
                self.winfo_toplevel(),
                structure_id=None,
                db_path=self._get_db_path(),
            )
            self.wait_window(dlg)

            if getattr(dlg, "saved", False):
                self._safe_status("Nova estrutura salva")
                self.reload_structures()
                self._render_structures_list()
        except Exception as exc:
            messagebox.showerror("Erro ao criar estrutura", str(exc), parent=self.winfo_toplevel())


    def edit_selected_structure(self) -> None:
        structure = self._require_active_selected_structure("editar pernas")
        if not structure:
            return

        if not self._is_structure_editor_available():
            return

        sid = structure.get("id")

        try:
            db_path = self._get_db_path()
            dlg = self._open_structure_editor(sid, db_path)

            if getattr(dlg, "saved", False):
                self._handle_structure_editor_saved(sid, db_path)

        except Exception as exc:
            messagebox.showerror("Erro ao editar estrutura", str(exc), parent=self.winfo_toplevel())

    def _is_structure_editor_available(self) -> bool:
        if StructureEditorDialog is not None:
            return True

        messagebox.showerror(
            "Editor indisponivel",
            "StructureEditorDialog nao foi encontrado.",
            parent=self.winfo_toplevel(),
        )
        return False

    def _open_structure_editor(self, sid: Any, db_path: str) -> Any:
        dlg = StructureEditorDialog(
            self.winfo_toplevel(),
            structure_id=sid,
            db_path=db_path,
        )
        self.wait_window(dlg)
        return dlg

    def _handle_structure_editor_saved(self, sid: Any, db_path: str) -> None:
        self._safe_status(f"Estrutura ID {sid} atualizada")
        self.reload_structures()

        try:
            repo = StructuresRepository(db_path)
            updated = repo.get_structure(sid)
            if updated:
                self.select_structure(updated)
        except Exception:
            pass

        self._render_structure_actions(notice=f"Estrutura ID {sid} atualizada.")


    def duplicate_selected_structure(self) -> None:
        structure = self._require_selected_structure()
        if not structure:
            return

        if not self._is_structures_repository_available():
            return

        sid = structure.get("id")

        try:
            repo = StructuresRepository(self._get_db_path())
            src = self._load_structure_for_duplication(repo, sid)

            if src is None:
                return

            new_id = self._create_duplicate_structure(repo, src)
            self._duplicate_structure_legs(repo, src, new_id)
            self._refresh_after_structure_duplication(repo, new_id)

            self._safe_status(f"Estrutura duplicada: ID {new_id}")

        except Exception as exc:
            self._safe_status(f"Erro ao duplicar estrutura: {exc}")
            messagebox.showerror("Erro ao duplicar estrutura", str(exc), parent=self.winfo_toplevel())

    def _is_structures_repository_available(self) -> bool:
        if StructuresRepository is not None:
            return True

        messagebox.showerror(
            "Repositorio indisponivel",
            "StructuresRepository nao foi encontrado.",
            parent=self.winfo_toplevel(),
        )
        return False

    def _load_structure_for_duplication(self, repo: Any, sid: Any) -> Any:
        src = repo.get_structure(sid)

        if src is not None:
            return src

        messagebox.showerror(
            "Duplicar estrutura",
            "Nao foi possivel carregar a estrutura selecionada.",
            parent=self.winfo_toplevel(),
        )
        return None

    def _create_duplicate_structure(self, repo: Any, src: Dict[str, Any]) -> Any:
        return repo.create_structure({
            "name": f"{src.get('name') or 'Estrutura'} (copia)",
            "underlying_asset": src.get("underlying_asset"),
            "alias_legacy_aba": src.get("alias_legacy_aba"),
            "status": "active",
            "notes": src.get("notes"),
        })

    def _duplicate_structure_legs(self, repo: Any, src: Dict[str, Any], new_id: Any) -> None:
        legs_copy = self._build_duplicate_legs_payload(src)

        if legs_copy:
            repo.replace_legs(new_id, legs_copy)

    def _build_duplicate_legs_payload(self, src: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                k: v
                for k, v in leg.items()
                if k not in ("id", "structure_id", "created_at", "updated_at")
            }
            for leg in src.get("legs", [])
        ]

    def _refresh_after_structure_duplication(self, repo: Any, new_id: Any) -> None:
        self.reload_structures()

        duplicated = repo.get_structure(new_id)
        if duplicated:
            self.select_structure(duplicated)
            self._render_structure_actions(
                notice=f"Estrutura duplicada com sucesso. Nova ID {new_id}."
            )
        else:
            self._render_structures_list()


    def _start_auto_refresh_loop(self) -> None:
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


    def archive_selected_structure(self) -> None:
        structure = self._require_selected_structure()
        if not structure:
            return

        sid = structure.get("id")

        if not self._is_structures_repository_available():
            return

        try:
            repo = StructuresRepository(self._get_db_path())
            src = self._load_structure_for_archive(repo, sid, structure)
            name = self._structure_archive_name(src, sid)

            if self._is_structure_already_archived(src):
                self._handle_already_archived_structure(name)
                return

            if not self._confirm_archive_structure(name):
                self._handle_archive_cancelled()
                return

            self._archive_structure_in_repository(repo, sid)
            self._refresh_after_structure_archive(sid)
            self._show_archive_success(name)

        except Exception as exc:
            self._safe_status(f"Erro ao arquivar estrutura: {exc}")
            messagebox.showerror("Erro ao arquivar estrutura", str(exc), parent=self.winfo_toplevel())

    def _load_structure_for_archive(
        self,
        repo: Any,
        sid: Any,
        fallback_structure: Dict[str, Any],
    ) -> Dict[str, Any]:
        return repo.get_structure(sid) or fallback_structure

    def _structure_archive_name(self, structure: Dict[str, Any], sid: Any) -> str:
        return structure.get("name") or f"ID {sid}"

    def _is_structure_already_archived(self, structure: Dict[str, Any]) -> bool:
        status = str(structure.get("status") or "").strip().lower()
        return status in {
            "archived",
            "closed",
            "encerrada",
            "encerrado",
            "arquivada",
            "arquivado",
        }

    def _handle_already_archived_structure(self, name: str) -> None:
        msg = f"Estrutura '{name}' ja esta arquivada."
        self._safe_status(msg)
        self._render_structure_actions(notice=msg)
        messagebox.showinfo("Arquivar", msg, parent=self.winfo_toplevel())

    def _confirm_archive_structure(self, name: str) -> bool:
        return messagebox.askyesno(
            "Arquivar",
            f"Arquivar '{name}'?\nA estrutura ficara oculta e nao sera deletada.",
            parent=self.winfo_toplevel(),
        )

    def _handle_archive_cancelled(self) -> None:
        self._safe_status("Arquivamento cancelado")
        self._render_structure_actions(notice="Arquivamento cancelado.")

    def _archive_structure_in_repository(self, repo: Any, sid: Any) -> None:
        repo.archive_structure(sid)

    def _refresh_after_structure_archive(self, sid: Any) -> None:
        self.selected_structure = None
        self._safe_status(f"Estrutura arquivada: ID {sid}")
        self.reload_structures()
        self._render_structures_list()

        if hasattr(self, "header"):
            self.header.configure(
                text="Selecione uma estrutura no menu lateral para carregar a VWAP e Payoff"
            )

    def _show_archive_success(self, name: str) -> None:
        messagebox.showinfo(
            "Arquivar",
            f"Estrutura '{name}' arquivada com sucesso.",
            parent=self.winfo_toplevel(),
        )


    def _register_structure_decision(self, decision: str) -> None:
        structure = self._require_selected_structure()
        if not structure:
            return

        raw_decision = str(decision or "").strip().upper()
        sid = structure.get("id")
        name = structure.get("name") or f"ID {sid}"
        label = decision_label(raw_decision)

        if raw_decision != "CLOSE" and self._is_structure_already_archived(structure):
            self._handle_archived_structure_action_blocked(
                structure,
                f"registrar decisao {raw_decision}",
            )
            return

        if raw_decision == "CLOSE":
            self._register_close_structure_decision(
                structure,
                sid,
                name,
                raw_decision,
                label,
            )
            return

        self._register_regular_structure_decision(sid, raw_decision, label)

    def _register_close_structure_decision(
        self,
        structure: Dict[str, Any],
        sid: Any,
        name: str,
        decision: str,
        label: str,
    ) -> None:
        if self._is_structure_already_archived(structure):
            msg = f"Estrutura ID {sid} ja esta encerrada/arquivada."
            self._safe_status(msg)
            self._render_structure_actions(notice=msg)
            return

        if not self._is_structures_repository_available():
            return

        if not self._confirm_close_structure(name):
            self._safe_status("Encerramento cancelado")
            return

        try:
            repo = StructuresRepository(self._get_db_path())
            repo.archive_structure(int(sid))
            self._insert_structure_decision(int(sid), decision)

            msg = f"Decisao registrada para ID {sid}: {label} ({decision}). Estrutura encerrada."
            self._handle_closed_structure_decision_saved(sid, msg)

        except Exception as exc:
            self._safe_status(f"Erro ao encerrar estrutura: {exc}")
            messagebox.showerror("Erro ao encerrar estrutura", str(exc), parent=self.winfo_toplevel())

    def _confirm_close_structure(self, name: str) -> bool:
        return messagebox.askyesno(
            "Encerrar estrutura",
            f"Encerrar '{name}'?\nA estrutura sera marcada como arquivada.",
            parent=self.winfo_toplevel(),
        )

    def _handle_closed_structure_decision_saved(self, sid: Any, msg: str) -> None:
        self._safe_status(msg)
        self.reload_structures()

        try:
            self._load_structure(int(sid))
            self._render_structure_actions(notice=msg)
        except Exception:
            self._render_structures_list()

    def _register_regular_structure_decision(
        self,
        sid: Any,
        decision: str,
        label: str,
    ) -> None:
        try:
            self._insert_structure_decision(int(sid), decision)
        except Exception as exc:
            self._safe_status(f"Erro ao registrar decisao: {exc}")
            messagebox.showerror("Erro ao registrar decisao", str(exc), parent=self.winfo_toplevel())
            return

        msg = f"Decisao registrada para ID {sid}: {label} ({decision})"
        self._safe_status(msg)
        self._render_structure_actions(notice=msg)
    # END AUTO STRUCTURE SIDE ACTIONS


# PAYOFF_UI_DEBUG_MONKEYPATCH
def _install_payoff_ui_debug_monkeypatch():
    import os as _os

    if _os.getenv("PAYOFF_DEBUG", "").strip() not in {"1", "true", "TRUE", "yes", "YES"}:
        return

    cls = globals().get("TerminalVwapPayoffDarkPanel")
    if cls is None:
        return

    orig_load = getattr(cls, "_load_persisted_payoff_points", None)
    if callable(orig_load):
        def _debug_load_persisted_payoff_points(self, structure_id):
            pts = orig_load(self, structure_id)
            latest_ts = None
            rows = None

            try:
                with self._connect() as conn:
                    row = conn.execute(
                        """
                        SELECT MAX(timestamp) AS latest_ts
                        FROM payoff_curve_points
                        WHERE structure_id = ?
                        """,
                        (structure_id,),
                    ).fetchone()

                    latest_ts = row["latest_ts"] if row else None

                    if latest_ts:
                        row2 = conn.execute(
                            """
                            SELECT COUNT(*) AS rows
                            FROM payoff_curve_points
                            WHERE structure_id = ?
                              AND timestamp = ?
                            """,
                            (structure_id, latest_ts),
                        ).fetchone()
                        rows = row2["rows"] if row2 else None
            except Exception as exc:
                print(f"[PAYOFF-UI-DEBUG] erro consultando snapshot: {exc}")

            print(
                "[PAYOFF-UI-DEBUG] "
                f"structure_id={structure_id} "
                f"latest_ts={latest_ts} "
                f"db_rows={rows} "
                f"loaded_points={len(pts or [])}"
            )
            return pts

        cls._load_persisted_payoff_points = _debug_load_persisted_payoff_points

    orig_be = getattr(cls, "_breakevens", None)
    if callable(orig_be):
        def _debug_breakevens(self, points):
            bes = orig_be(self, points)
            print(
                "[PAYOFF-UI-DEBUG] "
                f"breakevens={bes} "
                f"points={len(points or [])}"
            )
            return bes

        cls._breakevens = _debug_breakevens


_install_payoff_ui_debug_monkeypatch()

