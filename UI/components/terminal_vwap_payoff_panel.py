# UI/components/terminal_vwap_payoff_panel.py
"""
Painel nativo Tkinter do Terminal VWAP Payoff.

Este componente pertence à UI principal. Ele não é uma aplicação separada,
não abre janela própria e não acessa banco diretamente.

Fluxo esperado:
    MainWindow
      -> TerminalVWAPPayoffPanel
         -> TerminalVWAPPayoffController
            -> TerminalVWAPPayoffAppService
               -> repositórios/providers
               -> TerminalVWAPPayoffViewModelService

O painel consome somente ViewModel normalizado.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any, Callable


def _to_float(value: Any) -> float | None:
    if value is None:
        return None

    if isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()
    if not text:
        return None

    try:
        if "," in text:
            text = text.replace(".", "").replace(",", ".")
        return float(text)
    except Exception:
        return None


def _safe_text(value: Any, default: str = "N/A") -> str:
    if value is None:
        return default

    text = str(value).strip()
    return text if text else default


def _format_number_br(value: Any, decimals: int = 2) -> str:
    number = _to_float(value)
    if number is None:
        return "N/A"

    rendered = f"{number:,.{decimals}f}"
    return rendered.replace(",", "X").replace(".", ",").replace("X", ".")


def _format_currency_br(value: Any, decimals: int = 2) -> str:
    number = _to_float(value)
    if number is None:
        return "N/A"

    return f"R$ {_format_number_br(number, decimals)}"


def _format_percent_br(value: Any, decimals: int = 2) -> str:
    number = _to_float(value)
    if number is None:
        return "N/A"

    return f"{_format_number_br(number, decimals)}%"


def _extract_leg_table_rows(viewmodel: dict[str, Any]) -> list[tuple[str, ...]]:
    rows: list[tuple[str, ...]] = []

    for leg in viewmodel.get("legs") or []:
        rows.append(
            (
                _safe_text(leg.get("leg_order")),
                _safe_text(leg.get("symbol")),
                _safe_text(leg.get("position_side")),
                _safe_text(leg.get("option_type")),
                _format_number_br(leg.get("strike"), 2),
                _safe_text(leg.get("expiration_date")),
                _format_number_br(leg.get("quantity"), 0),
                _format_currency_br(leg.get("premium"), 2),
            )
        )

    return rows


def _extract_payoff_table_rows(
    viewmodel: dict[str, Any],
    *,
    limit: int | None = None,
) -> list[tuple[str, str]]:
    payoff = viewmodel.get("payoff") or {}
    points = payoff.get("points") or []

    if limit is not None:
        points = points[:limit]

    rows: list[tuple[str, str]] = []
    for point in points:
        rows.append(
            (
                _format_number_br(point.get("underlying_price"), 2),
                _format_currency_br(point.get("result"), 2),
            )
        )

    return rows


def _summarize_viewmodel(viewmodel: dict[str, Any]) -> dict[str, str]:
    structure = viewmodel.get("structure") or {}
    market = viewmodel.get("market") or {}
    payoff = viewmodel.get("payoff") or {}

    return {
        "structure_id": _safe_text(structure.get("structure_id")),
        "name": _safe_text(structure.get("name")),
        "underlying_asset": _safe_text(structure.get("underlying_asset")),
        "status": _safe_text(structure.get("status")),
        "current_price": _format_number_br(market.get("current_price"), 2),
        "vwap": _format_number_br(market.get("vwap"), 2),
        "price_vs_vwap_percent": _format_percent_br(
            market.get("price_vs_vwap_percent"),
            2,
        ),
        "market_source": _safe_text(market.get("source")),
        "market_timestamp": _safe_text(market.get("timestamp")),
        "points_count": _safe_text(payoff.get("points_count")),
        "min_result": _format_currency_br(payoff.get("min_result"), 2),
        "max_result": _format_currency_br(payoff.get("max_result"), 2),
        "break_even_points": ", ".join(
            _format_number_br(item, 2)
            for item in payoff.get("break_even_points") or []
        ) or "N/A",
    }


class TerminalVWAPPayoffPanel(ttk.Frame):
    """Aba nativa do Terminal VWAP Payoff na UI principal."""

    def __init__(
        self,
        parent: tk.Widget,
        controller: Any,
        *,
        on_status: Callable[[str], None] | None = None,
    ) -> None:
        super().__init__(parent, padding=6)

        if controller is None:
            raise ValueError("controller é obrigatório")

        self._controller = controller
        self._on_status = on_status
        self._structures: list[dict[str, Any]] = []
        self._current_viewmodel: dict[str, Any] | None = None

        self._build_ui()
        self.reload_structures()

    # ------------------------------------------------------------------
    # Construção visual
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        outer = ttk.PanedWindow(self, orient="horizontal")
        outer.pack(fill="both", expand=True)

        left = ttk.Frame(outer)
        right = ttk.Frame(outer)

        outer.add(left, weight=1)
        outer.add(right, weight=3)

        self._build_left_panel(left)
        self._build_right_panel(right)

        self._status_var = tk.StringVar(value="Terminal VWAP Payoff pronto")
        ttk.Label(
            self,
            textvariable=self._status_var,
            relief=tk.SUNKEN,
            anchor="w",
        ).pack(side="bottom", fill="x", pady=(6, 0))

    def _build_left_panel(self, parent: tk.Widget) -> None:
        box = ttk.LabelFrame(parent, text="Estruturas", padding=6)
        box.pack(fill="both", expand=True)

        toolbar = ttk.Frame(box)
        toolbar.pack(fill="x", pady=(0, 6))

        ttk.Button(
            toolbar,
            text="Atualizar",
            command=self.reload_structures,
        ).pack(side="left")

        ttk.Button(
            toolbar,
            text="Carregar",
            command=self.load_selected_structure,
        ).pack(side="left", padx=(6, 0))

        columns = ("structure_id", "name", "underlying_asset", "status", "legs")
        self._structures_tree = ttk.Treeview(
            box,
            columns=columns,
            show="headings",
            selectmode="browse",
            height=12,
        )

        headers = {
            "structure_id": ("ID", 55, "center"),
            "name": ("Nome", 190, "w"),
            "underlying_asset": ("Ativo", 75, "center"),
            "status": ("Status", 75, "center"),
            "legs": ("Legs", 55, "center"),
        }

        for column in columns:
            text, width, anchor = headers[column]
            self._structures_tree.heading(column, text=text)
            self._structures_tree.column(
                column,
                width=width,
                anchor=anchor,
                stretch=(column == "name"),
            )

        vsb = ttk.Scrollbar(
            box,
            orient="vertical",
            command=self._structures_tree.yview,
        )
        self._structures_tree.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        self._structures_tree.pack(fill="both", expand=True)

        self._structures_tree.bind("<Double-1>", lambda _e: self.load_selected_structure())

    def _build_right_panel(self, parent: tk.Widget) -> None:
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)

        header = ttk.Frame(parent, padding=(6, 0, 6, 6))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        self._active_structure_title_var = tk.StringVar(
            value="Nenhuma estrutura carregada"
        )
        self._active_structure_subtitle_var = tk.StringVar(
            value="Selecione uma estrutura à esquerda para carregar VWAP, payoff e pernas."
        )

        ttk.Label(
            header,
            textvariable=self._active_structure_title_var,
            font=("Segoe UI", 13, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew")

        ttk.Label(
            header,
            textvariable=self._active_structure_subtitle_var,
            anchor="w",
        ).grid(row=1, column=0, sticky="ew", pady=(2, 0))

        actions = ttk.Frame(header)
        actions.grid(row=0, column=1, rowspan=2, sticky="e", padx=(12, 0))

        ttk.Button(
            actions,
            text="Atualizar estruturas",
            command=self.reload_structures,
        ).pack(side="left")

        ttk.Button(
            actions,
            text="Carregar selecionada",
            command=self.load_selected_structure,
        ).pack(side="left", padx=(6, 0))

        body = ttk.Frame(parent, padding=(6, 0, 6, 0))
        body.grid(row=1, column=0, sticky="nsew")
        body.columnconfigure(0, weight=1)
        body.rowconfigure(1, weight=1)

        cards = ttk.Frame(body)
        cards.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        self._build_summary_tab(cards)

        workspace = ttk.PanedWindow(body, orient="vertical")
        workspace.grid(row=1, column=0, sticky="nsew")

        charts_area = ttk.PanedWindow(workspace, orient="horizontal")

        market_box = ttk.LabelFrame(
            charts_area,
            text="VWAP / Mercado",
            padding=8,
        )
        payoff_box = ttk.LabelFrame(
            charts_area,
            text="Payoff",
            padding=8,
        )

        charts_area.add(market_box, weight=1)
        charts_area.add(payoff_box, weight=2)

        self._market_text = tk.Text(
            market_box,
            height=10,
            wrap="word",
            relief=tk.FLAT,
            padx=8,
            pady=8,
        )
        self._market_text.pack(fill="both", expand=True)
        self._market_text.insert(
            "1.0",
            "Carregue uma estrutura para visualizar preço atual, VWAP, fonte e atualização.",
        )
        self._market_text.configure(state="disabled")

        self._build_payoff_tab(payoff_box)

        legs_box = ttk.LabelFrame(
            workspace,
            text="Pernas da estrutura",
            padding=8,
        )
        self._build_legs_tab(legs_box)

        workspace.add(charts_area, weight=3)
        workspace.add(legs_box, weight=2)

        warnings_box = ttk.LabelFrame(
            body,
            text="Avisos operacionais",
            padding=6,
        )
        warnings_box.grid(row=2, column=0, sticky="ew", pady=(8, 0))
        self._build_warnings_tab(warnings_box)

    def _build_summary_tab(self, parent: tk.Widget) -> None:
        self._summary_vars: dict[str, tk.StringVar] = {}

        groups = [
            (
                "Estrutura",
                [
                    ("structure_id", "ID"),
                    ("name", "Nome"),
                    ("underlying_asset", "Ativo"),
                    ("status", "Status"),
                ],
            ),
            (
                "Mercado e VWAP",
                [
                    ("current_price", "Preço atual"),
                    ("vwap", "VWAP"),
                    ("price_vs_vwap_percent", "Preço vs VWAP"),
                    ("market_source", "Fonte"),
                    ("market_timestamp", "Atualizado em"),
                ],
            ),
            (
                "Payoff",
                [
                    ("points_count", "Pontos"),
                    ("min_result", "Resultado mín."),
                    ("max_result", "Resultado máx."),
                    ("break_even_points", "Break-even"),
                ],
            ),
        ]

        for column_index, (group_title, fields) in enumerate(groups):
            parent.columnconfigure(column_index, weight=1)

            group = ttk.LabelFrame(parent, text=group_title, padding=8)
            group.grid(
                row=0,
                column=column_index,
                sticky="nsew",
                padx=(0, 8 if column_index < len(groups) - 1 else 0),
            )
            group.columnconfigure(1, weight=1)

            for row, (key, label) in enumerate(fields):
                ttk.Label(group, text=f"{label}:", width=16, anchor="e").grid(
                    row=row,
                    column=0,
                    sticky="e",
                    padx=(0, 8),
                    pady=2,
                )

                var = tk.StringVar(value="N/A")
                self._summary_vars[key] = var

                ttk.Label(
                    group,
                    textvariable=var,
                    anchor="w",
                ).grid(
                    row=row,
                    column=1,
                    sticky="ew",
                    pady=2,
                )

    def _build_legs_tab(self, parent: tk.Widget) -> None:
        columns = (
            "order",
            "symbol",
            "side",
            "type",
            "strike",
            "expiry",
            "quantity",
            "premium",
        )

        self._legs_tree = ttk.Treeview(parent, columns=columns, show="headings")

        headers = {
            "order": ("#", 45, "center"),
            "symbol": ("Símbolo", 110, "center"),
            "side": ("Lado", 90, "center"),
            "type": ("Tipo", 70, "center"),
            "strike": ("Strike", 90, "e"),
            "expiry": ("Vencimento", 105, "center"),
            "quantity": ("Qtde", 85, "e"),
            "premium": ("Prêmio", 95, "e"),
        }

        for column in columns:
            text, width, anchor = headers[column]
            self._legs_tree.heading(column, text=text)
            self._legs_tree.column(column, width=width, anchor=anchor)

        vsb = ttk.Scrollbar(parent, orient="vertical", command=self._legs_tree.yview)
        self._legs_tree.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        self._legs_tree.pack(fill="both", expand=True)

    def _build_payoff_tab(self, parent: tk.Widget) -> None:
        top = ttk.Frame(parent)
        top.pack(fill="x", pady=(0, 6))

        self._payoff_summary_var = tk.StringVar(value="Payoff ainda não carregado")
        ttk.Label(
            top,
            textvariable=self._payoff_summary_var,
            anchor="w",
        ).pack(side="left", fill="x", expand=True)

        columns = ("underlying_price", "result")
        self._payoff_tree = ttk.Treeview(parent, columns=columns, show="headings")

        self._payoff_tree.heading("underlying_price", text="Spot")
        self._payoff_tree.heading("result", text="Resultado")

        self._payoff_tree.column("underlying_price", width=120, anchor="e")
        self._payoff_tree.column("result", width=140, anchor="e")

        vsb = ttk.Scrollbar(parent, orient="vertical", command=self._payoff_tree.yview)
        self._payoff_tree.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        self._payoff_tree.pack(fill="both", expand=True)

    def _build_warnings_tab(self, parent: tk.Widget) -> None:
        self._warnings_text = tk.Text(parent, height=8, wrap="word")
        self._warnings_text.pack(fill="both", expand=True)
        self._warnings_text.configure(state="disabled")

    # ------------------------------------------------------------------
    # Ações
    # ------------------------------------------------------------------

    def reload_structures(self) -> None:
        try:
            structures = self._controller.list_structures()
        except Exception as exc:
            self._set_status(f"Erro ao listar estruturas: {exc}")
            messagebox.showerror(
                "Terminal VWAP Payoff",
                f"Erro ao listar estruturas:\n{exc}",
            )
            return

        self._structures = list(structures or [])
        self._render_structures()
        self._set_status(f"{len(self._structures)} estruturas disponíveis no terminal")

    def load_selected_structure(self) -> None:
        selected = self._structures_tree.selection()
        if not selected:
            self._set_status("Selecione uma estrutura para carregar")
            return

        item_id = selected[0]
        try:
            index = int(item_id)
            structure = self._structures[index]
        except Exception:
            self._set_status("Seleção inválida")
            return

        structure_id = structure.get("structure_id")
        self.load_structure(structure_id)

    def load_structure(self, structure_id: Any) -> None:
        try:
            self._set_status(f"Carregando estrutura {structure_id}...")
            viewmodel = self._controller.load_structure(structure_id)
        except Exception as exc:
            self._set_status(f"Erro ao carregar estrutura {structure_id}: {exc}")
            messagebox.showerror(
                "Terminal VWAP Payoff",
                f"Erro ao carregar estrutura {structure_id}:\n{exc}",
            )
            return

        self.render_viewmodel(viewmodel)
        self._set_status(f"Estrutura {structure_id} carregada no Terminal VWAP Payoff")

    # ------------------------------------------------------------------
    # Renderização
    # ------------------------------------------------------------------

    def _render_structures(self) -> None:
        for item in self._structures_tree.get_children():
            self._structures_tree.delete(item)

        for index, structure in enumerate(self._structures):
            self._structures_tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    _safe_text(structure.get("structure_id")),
                    _safe_text(structure.get("name")),
                    _safe_text(structure.get("underlying_asset")),
                    _safe_text(structure.get("status")),
                    _safe_text(structure.get("legs_count")),
                ),
            )

    def render_viewmodel(self, viewmodel: dict[str, Any]) -> None:
        self._current_viewmodel = dict(viewmodel or {})

        summary = _summarize_viewmodel(self._current_viewmodel)
        for key, var in self._summary_vars.items():
            var.set(summary.get(key, "N/A"))

        if hasattr(self, "_active_structure_title_var"):
            self._active_structure_title_var.set(
                "{name} | {asset} | ID {structure_id}".format(
                    name=summary.get("name", "N/A"),
                    asset=summary.get("underlying_asset", "N/A"),
                    structure_id=summary.get("structure_id", "N/A"),
                )
            )

        if hasattr(self, "_active_structure_subtitle_var"):
            self._active_structure_subtitle_var.set(
                "Status: {status} | Preço atual: {price} | VWAP: {vwap} | Preço vs VWAP: {spread}".format(
                    status=summary.get("status", "N/A"),
                    price=summary.get("current_price", "N/A"),
                    vwap=summary.get("vwap", "N/A"),
                    spread=summary.get("price_vs_vwap_percent", "N/A"),
                )
            )

        if hasattr(self, "_market_text"):
            market_text = (
                "Leitura operacional VWAP\n\n"
                f"Ativo: {summary.get('underlying_asset', 'N/A')}\n"
                f"Preço atual: {summary.get('current_price', 'N/A')}\n"
                f"VWAP: {summary.get('vwap', 'N/A')}\n"
                f"Preço vs VWAP: {summary.get('price_vs_vwap_percent', 'N/A')}\n"
                f"Fonte: {summary.get('market_source', 'N/A')}\n"
                f"Atualizado em: {summary.get('market_timestamp', 'N/A')}\n\n"
                "Este bloco consolida os dados de mercado usados pelo terminal. "
                "Nenhum cálculo, RTD, banco ou serviço foi alterado nesta camada."
            )
            self._market_text.configure(state="normal")
            self._market_text.delete("1.0", tk.END)
            self._market_text.insert("1.0", market_text)
            self._market_text.configure(state="disabled")

        self._render_legs(self._current_viewmodel)
        self._render_payoff(self._current_viewmodel)
        self._render_warnings(self._current_viewmodel)

    def _render_legs(self, viewmodel: dict[str, Any]) -> None:
        for item in self._legs_tree.get_children():
            self._legs_tree.delete(item)

        for index, row in enumerate(_extract_leg_table_rows(viewmodel)):
            self._legs_tree.insert("", "end", iid=str(index), values=row)

    def _render_payoff(self, viewmodel: dict[str, Any]) -> None:
        for item in self._payoff_tree.get_children():
            self._payoff_tree.delete(item)

        rows = _extract_payoff_table_rows(viewmodel)
        for index, row in enumerate(rows):
            self._payoff_tree.insert("", "end", iid=str(index), values=row)

        payoff = viewmodel.get("payoff") or {}
        self._payoff_summary_var.set(
            "Pontos: {points} | Mín: {min_result} | Máx: {max_result} | BE: {be}".format(
                points=_safe_text(payoff.get("points_count")),
                min_result=_format_currency_br(payoff.get("min_result"), 2),
                max_result=_format_currency_br(payoff.get("max_result"), 2),
                be=", ".join(
                    _format_number_br(item, 2)
                    for item in payoff.get("break_even_points") or []
                ) or "N/A",
            )
        )

    def _render_warnings(self, viewmodel: dict[str, Any]) -> None:
        meta = viewmodel.get("meta") or {}
        warnings = meta.get("warnings") or []

        text = "\n".join(f"- {item}" for item in warnings) if warnings else "Sem avisos."

        self._warnings_text.configure(state="normal")
        self._warnings_text.delete("1.0", tk.END)
        self._warnings_text.insert("1.0", text)
        self._warnings_text.configure(state="disabled")

    def _set_status(self, message: str) -> None:
        if hasattr(self, "_status_var"):
            self._status_var.set(message)

        if self._on_status is not None:
            try:
                self._on_status(message)
            except Exception:
                pass
