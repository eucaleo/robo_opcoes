#!/usr/bin/env bash
set -euo pipefail

if [ ! -d "UI" ]; then
    echo "[ERRO] Execute este script na raiz do projeto."
    exit 1
fi

if [ ! -d "UI/components" ]; then
    echo "[ERRO] Pasta UI/components não encontrada."
    exit 1
fi

python - <<'PY'
try:
    import customtkinter
except Exception as exc:
    raise SystemExit(
        "[ERRO] customtkinter não está disponível. Instale com: pip install customtkinter\n"
        + str(exc)
    )
PY

stamp="$(date +%Y%m%d_%H%M%S)"

if [ -f "UI/main_window.py" ]; then
    cp "UI/main_window.py" "UI/main_window.py.bak_dark_layout_${stamp}"
    echo "[OK] Backup criado: UI/main_window.py.bak_dark_layout_${stamp}"
fi

if [ -f "UI/components/terminal_vwap_payoff_dark_panel.py" ]; then
    cp "UI/components/terminal_vwap_payoff_dark_panel.py" "UI/components/terminal_vwap_payoff_dark_panel.py.bak_${stamp}"
    echo "[OK] Backup criado: UI/components/terminal_vwap_payoff_dark_panel.py.bak_${stamp}"
fi

cat > UI/components/terminal_vwap_payoff_dark_panel.py <<'PY'
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
import sqlite3
import tkinter as tk
from tkinter import ttk

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


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


class TerminalVWAPPayoffDarkPanel(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        db_path: str,
        on_status=None,
    ) -> None:
        super().__init__(parent, fg_color=DARK_BG)

        self.db_path = str(db_path)
        self.on_status = on_status or (lambda _msg: None)

        self.menu_visible = True
        self.structures: List[Dict[str, Any]] = []
        self.selected_structure: Optional[Dict[str, Any]] = None

        self.canvas_vwap: Optional[FigureCanvasTkAgg] = None
        self.canvas_payoff: Optional[FigureCanvasTkAgg] = None

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
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.rail = ctk.CTkFrame(
            self,
            width=70,
            corner_radius=0,
            fg_color=RAIL_BG,
        )
        self.rail.grid(row=0, column=0, sticky="nsew")
        self.rail.grid_propagate(False)

        self.btn_toggle = ctk.CTkButton(
            self.rail,
            text="☰\n\nID",
            width=50,
            height=62,
            fg_color=GREEN,
            hover_color="#059669",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.toggle_structures_panel,
        )
        self.btn_toggle.pack(pady=20, padx=10)

        self.side = ctk.CTkFrame(
            self,
            width=255,
            corner_radius=0,
            fg_color=SIDE_BG,
        )
        self.side.grid(row=0, column=1, sticky="nsew")
        self.side.grid_propagate(False)

        self.main = ctk.CTkFrame(
            self,
            fg_color=DARK_BG,
        )
        self.main.grid(row=0, column=2, sticky="nsew", padx=15, pady=15)
        self.main.grid_columnconfigure((0, 1), weight=1)
        self.main.grid_rowconfigure(2, weight=3)
        self.main.grid_rowconfigure(3, weight=1)

        self.header = ctk.CTkLabel(
            self.main,
            text="Selecione uma estrutura no menu lateral para carregar a VWAP e Payoff",
            text_color=TEXT,
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.header.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

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

        self.alerts_box = ctk.CTkTextbox(
            self.bottom,
            fg_color=CARD_BG_2,
            text_color=TEXT,
            corner_radius=6,
            font=ctk.CTkFont(family="Consolas", size=12),
        )
        self.alerts_box.grid(row=1, column=1, sticky="nsew", padx=(6, 12), pady=(0, 12))
        self._set_alerts(["Nenhuma estrutura selecionada."])

        self._render_empty_charts()

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
        self.structures = self._load_structures()
        self._render_structures_list()
        self.on_status(f"{len(self.structures)} estruturas carregadas")

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
        for widget in self.side.winfo_children():
            widget.destroy()

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

        scroll = ctk.CTkScrollableFrame(
            self.side,
            fg_color="transparent",
        )
        scroll.pack(fill="both", expand=True, padx=5, pady=5)

        if not self.structures:
            lbl = ctk.CTkLabel(
                scroll,
                text="Nenhuma estrutura encontrada no app.db",
                text_color=MUTED,
                wraplength=210,
                justify="left",
            )
            lbl.pack(fill="x", padx=8, pady=8)
            return

        for structure in self.structures:
            sid = structure.get("id")
            name = structure.get("name")
            asset = structure.get("underlying_asset")
            status = structure.get("status")

            btn = ctk.CTkButton(
                scroll,
                text=f"ID {sid} | {asset}\n{name}\n{status}",
                anchor="w",
                justify="left",
                height=66,
                fg_color="#2B2B2B",
                hover_color="#3D3D3D",
                text_color=TEXT,
                command=lambda s=structure: self.select_structure(s),
            )
            btn.pack(fill="x", pady=5, padx=5)

    def select_structure(self, structure: Dict[str, Any]) -> None:
        self.selected_structure = dict(structure)

        sid = structure.get("id")
        name = structure.get("name")
        asset = structure.get("underlying_asset")

        legs = self._load_legs(sid)
        market = self._load_market(asset)
        payoff_points = self._load_payoff_points(sid, legs)

        self.header.configure(
            text=f"Análise ativa: ID {sid} - {name} | Ativo: {asset}"
        )

        self._update_kpis(market, payoff_points)
        self._render_legs(legs)
        self._render_charts(market, payoff_points, asset)
        self._render_alerts(market, payoff_points, legs)

        self.on_status(f"Estrutura carregada: ID {sid}")

        if self.menu_visible:
            self.toggle_structures_panel()

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
            schema = self._tables_cols(conn)
            table = self._find_legs_table(schema)
            if not table:
                return []

            cols = schema[table]
            sid_col = _first_col(cols, ["structure_id", "id_structure", "estrutura_id"])
            symbol_col = _first_col(cols, ["symbol", "simbolo", "ticker"])
            side_col = _first_col(cols, ["position_side", "side", "lado"])
            type_col = _first_col(cols, ["option_type", "type", "tipo"])
            strike_col = _first_col(cols, ["strike", "exercise_price"])
            exp_col = _first_col(cols, ["expiration_date", "expiration", "vencimento"])
            qty_col = _first_col(cols, ["quantity", "qty", "qtd", "quantidade"])
            prem_col = _first_col(cols, ["premium", "premio", "price", "preco"])
            mult_col = _first_col(cols, ["multiplier", "multiplicador"])

            if not sid_col:
                return []

            select_parts = [
                f"{_q(symbol_col)} AS symbol" if symbol_col else "NULL AS symbol",
                f"{_q(side_col)} AS position_side" if side_col else "NULL AS position_side",
                f"{_q(type_col)} AS option_type" if type_col else "NULL AS option_type",
                f"{_q(strike_col)} AS strike" if strike_col else "NULL AS strike",
                f"{_q(exp_col)} AS expiration_date" if exp_col else "NULL AS expiration_date",
                f"{_q(qty_col)} AS quantity" if qty_col else "NULL AS quantity",
                f"{_q(prem_col)} AS premium" if prem_col else "NULL AS premium",
                f"{_q(mult_col)} AS multiplier" if mult_col else "NULL AS multiplier",
            ]

            sql = (
                f"SELECT {', '.join(select_parts)} "
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
            "updated_at": None,
            "series": [],
        }

        if not asset or asset == "N/A":
            return result

        conn = self._connect()
        try:
            schema = self._tables_cols(conn)

            for table, cols in schema.items():
                asset_col = _first_col(cols, ["asset", "ativo", "symbol", "ticker", "underlying_asset"])
                price_col = _first_col(cols, ["current_price", "preco_atual", "price", "last_price", "last"])
                vwap_col = _first_col(cols, ["vwap", "vwap_price"])
                ts_col = _first_col(cols, ["timestamp", "updated_at", "created_at", "datetime", "dt_ref"])

                if not asset_col or not (price_col or vwap_col):
                    continue

                select_parts = [
                    f"{_q(price_col)} AS current_price" if price_col else "NULL AS current_price",
                    f"{_q(vwap_col)} AS vwap" if vwap_col else "NULL AS vwap",
                    f"{_q(ts_col)} AS updated_at" if ts_col else "NULL AS updated_at",
                ]

                order_sql = f" ORDER BY {_q(ts_col)} DESC" if ts_col else ""
                sql = (
                    f"SELECT {', '.join(select_parts)} "
                    f"FROM {_q(table)} "
                    f"WHERE {_q(asset_col)} = ?"
                    f"{order_sql} LIMIT 200"
                )

                rows = conn.execute(sql, (asset,)).fetchall()
                if not rows:
                    continue

                first = dict(rows[0])
                result["current_price"] = first.get("current_price")
                result["vwap"] = first.get("vwap")
                result["updated_at"] = first.get("updated_at")

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
                result["series"] = series
                return result

            return result
        finally:
            conn.close()

    def _load_payoff_points(
        self,
        structure_id: Any,
        legs: List[Dict[str, Any]],
    ) -> List[Dict[str, float]]:
        persisted = self._load_persisted_payoff_points(structure_id)
        if persisted:
            return persisted
        return self._calculate_payoff_from_legs(legs)

    def _load_persisted_payoff_points(self, structure_id: Any) -> List[Dict[str, float]]:
        conn = self._connect()
        try:
            schema = self._tables_cols(conn)
            for table, cols in schema.items():
                sid_col = _first_col(cols, ["structure_id", "id_structure", "estrutura_id"])
                spot_col = _first_col(cols, ["point_spot", "spot", "underlying", "x"])
                pl_col = _first_col(cols, ["point_pl", "pl", "payoff", "result", "resultado", "y"])
                ts_col = _first_col(cols, ["timestamp", "created_at", "dt_ref"])

                if not sid_col or not spot_col or not pl_col:
                    continue

                order_sql = f", {_q(ts_col)} DESC" if ts_col else ""
                sql = (
                    f"SELECT {_q(spot_col)} AS spot, {_q(pl_col)} AS pl "
                    f"FROM {_q(table)} "
                    f"WHERE {_q(sid_col)} = ? "
                    f"ORDER BY spot{order_sql}"
                )
                rows = conn.execute(sql, (structure_id,)).fetchall()
                points = []
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
        strikes = [_to_float(leg.get("strike")) for leg in legs]
        strikes = [s for s in strikes if s is not None]

        if not strikes:
            return []

        low = min(strikes)
        high = max(strikes)
        span = max(high - low, high * 0.20, 1.0)
        x_min = max(0.01, low - span)
        x_max = high + span

        points: List[Dict[str, float]] = []
        steps = 140

        for i in range(steps + 1):
            spot = x_min + (x_max - x_min) * i / steps
            total = 0.0

            for leg in legs:
                strike = _to_float(leg.get("strike"))
                if strike is None:
                    continue

                premium = _to_float(leg.get("premium"), 0.0) or 0.0
                quantity = abs(_to_float(leg.get("quantity"), 1.0) or 1.0)
                multiplier = abs(_to_float(leg.get("multiplier"), 1.0) or 1.0)

                side = str(leg.get("position_side") or "").upper()
                opt_type = str(leg.get("option_type") or "").upper()

                is_short = (
                    "VEND" in side
                    or "SELL" in side
                    or "SHORT" in side
                    or side in {"S", "-1"}
                )

                sign = -1.0 if is_short else 1.0

                if "PUT" in opt_type:
                    intrinsic = max(strike - spot, 0.0)
                else:
                    intrinsic = max(spot - strike, 0.0)

                total += sign * (intrinsic - premium) * quantity * multiplier

            points.append({"spot": spot, "pl": total})

        return points

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
            alerts.append("vwap ausente")
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
    ) -> None:
        self._render_vwap_chart(market, asset)
        self._render_payoff_chart(payoff_points)

    def _render_vwap_chart(self, market: Dict[str, Any], asset: Any) -> None:
        self._clear_canvas("canvas_vwap")

        fig, ax = self._figure()
        series = market.get("series") or []

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
        else:
            ax.text(
                0.5,
                0.5,
                "VWAP indisponível no app.db",
                color=MUTED,
                ha="center",
                va="center",
                transform=ax.transAxes,
                fontsize=11,
            )

        ax.set_title("Preço de Execução vs VWAP", color=MUTED, fontsize=10)
        ax.set_xlabel("Amostras", color=MUTED, fontsize=8)
        ax.set_ylabel("Preço", color=MUTED, fontsize=8)

        self.canvas_vwap = FigureCanvasTkAgg(fig, master=self.frame_vwap)
        self.canvas_vwap.draw()
        self.canvas_vwap.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def _render_payoff_chart(self, points: List[Dict[str, float]]) -> None:
        self._clear_canvas("canvas_payoff")

        fig, ax = self._figure()

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
PY

cat > UI/main_window.py <<'PY'
# UI/main_window.py
#!/usr/bin/env python3
"""
Janela principal operacional dark do Sistema de Derivados.

A interface canônica é o Terminal VWAP Payoff em modo escuro, com:
- barra lateral fixa;
- painel retrátil de estruturas;
- KPIs superiores;
- blocos grandes de VWAP e Payoff;
- tabela inferior de pernas.
"""

from pathlib import Path
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from UI.components.terminal_vwap_payoff_dark_panel import TerminalVWAPPayoffDarkPanel


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class MainWindow:
    def __init__(self) -> None:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Terminal de Análise Avançada - VWAP & Opções")
        self.root.geometry("1365x750")
        self.root.minsize(1180, 700)

        self._db_path = str(PROJECT_ROOT / "dados" / "app.db")
        self.terminal_panel = None

        self._setup_menu()
        self._setup_layout()
        self._bind_events()

    def _setup_menu(self) -> None:
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        app_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aplicação", menu=app_menu)

        app_menu.add_command(
            label="Atualizar estruturas",
            accelerator="F5",
            command=self.reload_structures,
        )

        app_menu.add_separator()

        app_menu.add_command(
            label="Sair",
            accelerator="Ctrl+Q",
            command=self.close,
        )

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=help_menu)

        help_menu.add_command(
            label="Sobre",
            command=self.show_about,
        )

    def _setup_layout(self) -> None:
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.terminal_panel = TerminalVWAPPayoffDarkPanel(
            parent=self.root,
            db_path=self._db_path,
            on_status=self.set_status,
        )
        self.terminal_panel.grid(row=0, column=0, sticky="nsew")

    def _bind_events(self) -> None:
        self.root.bind("<F5>", lambda _event: self.reload_structures())
        self.root.bind("<Control-q>", lambda _event: self.close())
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def set_status(self, message: str) -> None:
        print("[UI]", message)

    def reload_structures(self) -> None:
        if self.terminal_panel is not None:
            self.terminal_panel.reload_structures()

    def show_about(self) -> None:
        messagebox.showinfo(
            "Sobre",
            (
                "Sistema de Derivados\n"
                "Terminal de Análise Avançada - VWAP & Opções\n\n"
                "Interface dark operacional."
            ),
        )

    def close(self) -> None:
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
PY

python -m py_compile UI/components/terminal_vwap_payoff_dark_panel.py
python -m py_compile UI/main_window.py

python - <<'PY'
from pathlib import Path

main = Path("UI/main_window.py").read_text(encoding="utf-8")
panel = Path("UI/components/terminal_vwap_payoff_dark_panel.py").read_text(encoding="utf-8")

forbidden_main = [
    "UIDataModel",
    "PayoffChart",
    "DetailsPanel",
    "DecisionsGrid",
    "FiltersPanel",
    "StructuresListPanel",
    "StructureEditorDialog",
    "ttk.Notebook",
    "refresh_data",
    "_setup_terminal_vwap_payoff_tab",
]

hits = [term for term in forbidden_main if term in main]
if hits:
    raise SystemExit("[ERRO] main_window.py ainda contém legado: " + ", ".join(hits))

required_main = [
    "customtkinter",
    "TerminalVWAPPayoffDarkPanel",
    "Terminal de Análise Avançada - VWAP & Opções",
]

missing_main = [term for term in required_main if term not in main]
if missing_main:
    raise SystemExit("[ERRO] main_window.py sem itens obrigatórios: " + ", ".join(missing_main))

required_panel = [
    "barra lateral fixa",
    "painel lateral retrátil",
    "COMPONENTES DA ESTRUTURA",
    "AVISOS OPERACIONAIS",
    "Payoff Combinado da Estrutura",
    "Preço de Execução vs VWAP",
]

missing_panel = [term for term in required_panel if term not in panel]
if missing_panel:
    raise SystemExit("[ERRO] painel dark sem itens obrigatórios: " + ", ".join(missing_panel))

print("[OK] Layout dark operacional validado.")
PY

echo
echo "[OK] Atualização concluída."
echo "[INFO] Rode agora:"
echo "python run_ui.py"
echo
echo "[INFO] Diff:"
git diff -- UI/main_window.py UI/components/terminal_vwap_payoff_dark_panel.py
