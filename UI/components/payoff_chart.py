# UI/components/payoff_chart.py
from src.domain.refs.structure_ref import StructureRef
from matplotlib.ticker import FuncFormatter
import json
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from UI.debug_utils import payoff_debug, payoff_info
from tkinter import filedialog, messagebox
from tkinter import ttk
from typing import List, Dict, Optional, Tuple

import matplotlib
matplotlib.use("TkAgg")  # necessário para renderizar no Tkinter


# ---------------------------------------------------------------------------
# Helpers de formatação pt-BR
# ---------------------------------------------------------------------------

def _fmt_number_br(x: float, decimals: int = 2) -> str:
    """Formata número no padrão pt-BR: milhar '.' e decimal ','."""
    try:
        s = f"{float(x):,.{decimals}f}"
        return s.replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return str(x)


def _fmt_currency_br(x: float, decimals: int = 2) -> str:
    return f"R$ {_fmt_number_br(x, decimals=decimals)}"


def _brl_abbrev(x, pos=None) -> str:
    """Formata eixo Y com abreviações k/M/B para legibilidade."""
    try:
        x = float(x)
    except Exception:
        return "R$ 0"
    ax = abs(x)
    sign = "-" if x < 0 else ""
    if ax >= 1_000_000_000:
        return f"{sign}R$ {ax / 1_000_000_000:.1f}B"
    if ax >= 1_000_000:
        return f"{sign}R$ {ax / 1_000_000:.1f}M"
    if ax >= 1_000:
        return f"{sign}R$ {ax / 1_000:.0f}k"
    return f"{sign}R$ {ax:.0f}"


# ---------------------------------------------------------------------------
# Classe principal
# ---------------------------------------------------------------------------

class PayoffChart(ttk.Frame):

    # ------------------------------------------------------------------
    # Inicialização
    # ------------------------------------------------------------------

    def __init__(self, parent):
        super().__init__(parent, padding=6)
        self._last_breakevens: List[float] = []
        self._last_pl_at_spot_ref: Optional[float] = None
        self._last_points: List[Dict] = []
        self._last_decision_data: Dict = {}
        self._last_payoff_comment: str = "Sem dados de payoff para interpretação."
        self._comment_var: Optional[tk.StringVar] = None
        self._comment_label = None
        # Comparação: overlay de curvas {"points": [...], "label": "...", "color": "..."}
        self._fixed_curve: Optional[Dict] = None
        self._build_canvas()

    # ------------------------------------------------------------------
    # Canvas / toolbar
    # ------------------------------------------------------------------

    def _build_canvas(self):
        # Barra superior: toolbar matplotlib + botões de ação
        top = ttk.Frame(self)
        top.pack(fill="x", side="top")

        self.btn_export = ttk.Button(
            top, text="Exportar PNG", command=self.export_png
        )
        self.btn_export.pack(side="right", padx=(6, 0))

        self.btn_fix_curve = ttk.Button(
            top, text="Fixar Curva A", command=self.fix_current_curve
        )
        self.btn_fix_curve.pack(side="right", padx=(0, 6))

        self.btn_clear_comparison = ttk.Button(
            top, text="Limpar Comparação", command=self.clear_comparison
        )
        self.btn_clear_comparison.pack(side="right", padx=(0, 6))

        # Comentário interpretativo do payoff
        comment_frame = ttk.LabelFrame(self, text="Comentário do payoff")
        comment_frame.pack(fill="x", side="bottom", pady=(6, 0))

        self._comment_var = tk.StringVar(value=self._last_payoff_comment)
        self._comment_label = ttk.Label(
            comment_frame,
            textvariable=self._comment_var,
            justify="left",
            anchor="w",
            wraplength=900,
        )
        self._comment_label.pack(fill="x", padx=6, pady=4)

        # Figure / canvas matplotlib
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Toolbar do matplotlib (fica na barra superior)
        self.toolbar = NavigationToolbar2Tk(self.canvas, top, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.pack(side="left", fill="x", expand=True)

        self._reset_axes()
        self._safe_draw_idle()

        # Forçar redraw quando o widget é exibido/redimensionado
        self.bind("<Configure>", self._on_configure, add=True)

    def _on_configure(self, event=None):
        try:
            w = int(self.winfo_width())
            h = int(self.winfo_height())
        except Exception:
            return
        if w <= 50 or h <= 50:
            return
        try:
            if self._comment_label is not None:
                self._comment_label.configure(wraplength=max(300, w - 40))
        except Exception:
            pass
        try:
            if hasattr(self, "toolbar"):
                self.toolbar.update()
        except Exception:
            pass
        self._safe_draw_idle()

    def _safe_draw_idle(self):
        """Agenda draw_idle na thread do Tk."""
        try:
            self.after(0, self.canvas.draw_idle)
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Eixos
    # ------------------------------------------------------------------

    def _reset_axes(self):
        self.ax.clear()
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel("Spot")
        self.ax.set_ylabel("PL")
        self.ax.set_title("Curva de Payoff")

        self.ax.xaxis.set_major_formatter(
            FuncFormatter(lambda v, pos: _fmt_number_br(v, 2))
        )
        self.ax.yaxis.set_major_formatter(
            FuncFormatter(
                lambda v, pos: _fmt_currency_br(v, 0 if abs(v) >= 1000 else 2)
            )
        )

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def clear(self):
        """Limpa o gráfico e reseta estado interno."""
        self._last_breakevens = []
        self._last_pl_at_spot_ref = None
        self._last_points = []
        self._last_decision_data = {}
        self._set_payoff_comment("Sem dados de payoff para interpretação.")
        self._reset_axes()
        self._safe_draw_idle()

    def update_chart(
        self,
        payoff_points: List[Dict],
        decision_data: Optional[Dict] = None,
    ) -> Dict:
        """
        Atualiza a curva principal.
        Preserva pontos para comparação e redesenha com overlay se houver.
        Retorna dict com breakevens e pl_at_spot_ref.
        """
        self._last_points = list(payoff_points) if payoff_points else []
        self._last_decision_data = dict(decision_data) if decision_data else {}

        return self._draw_curves_and_overlays(
            payoff_points, decision_data, overlay_curve=self._fixed_curve
        )

    def fix_current_curve(self):
        """Fixa a curva atual como Curva A para comparação."""
        payoff_debug("FIX clicked -- id=", id(self))

        if not self._last_points:
            self._fixed_curve = None
            return

        points = []
        for p in self._last_points:
            try:
                x, y = self._extract_xy(p)
                if x is None or y is None:
                    continue
                points.append({"spot": float(x), "pl": float(y)})
            except Exception:
                continue

        if len(points) < 2:
            self._fixed_curve = None
            return

        self._fixed_curve = {
            "label": "Curva A (fixada)",
            "color": "red",
            "points": points,
        }
        self._redraw_current()

    def clear_comparison(self):
        """Remove a curva fixada."""
        payoff_debug("CLEAR comparison -- id=", id(self))
        self._fixed_curve = None
        if self._last_points:
            self._redraw_current()

    def export_png(self):
        """Exporta o gráfico atual para PNG."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("Todos os arquivos", "*.*")],
            title="Exportar gráfico como PNG",
        )
        if not file_path:
            return
        try:
            self.fig.savefig(file_path, dpi=150, bbox_inches="tight")
            messagebox.showinfo("Sucesso", f"Gráfico salvo em {file_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    def get_last_overlays(self) -> Dict:
        """Para integração com DetailsPanel: breakevens e PL interpolado no spot_ref."""
        return {
            "breakevens": list(self._last_breakevens),
            "pl_at_spot_ref": self._last_pl_at_spot_ref,
            "payoff_comment": self._last_payoff_comment,
        }

    # ------------------------------------------------------------------
    # Redesenho interno
    # ------------------------------------------------------------------

    def _redraw_current(self):
        """Redesenha com os dados salvos em _last_points/_last_decision_data."""
        if self._last_points:
            self._draw_curves_and_overlays(
                self._last_points,
                self._last_decision_data or {},
                overlay_curve=self._fixed_curve,
            )

    def _draw_curves_and_overlays(
        self,
        payoff_points: List[Dict],
        decision_data: Optional[Dict],
        overlay_curve: Optional[Dict],
    ) -> Dict:
        """
        Núcleo de renderização: curva principal + overlay (Curva A) +
        breakevens + spot_ref.
        """
        self._reset_axes()

        if not payoff_points:
            self.ax.set_title("Sem dados de payoff")
            self._safe_draw_idle()
            self._last_breakevens = []
            self._last_pl_at_spot_ref = None
            self._set_payoff_comment(
                "Não há dados de payoff suficientes para interpretar ganho, perda, "
                "ponto de equilíbrio ou situação atual."
            )
            return self.get_last_overlays()

        # ------------------------------------------------------------------
        # Extrair xs / ys da curva principal
        # ------------------------------------------------------------------
        xs: List[float] = []
        ys: List[float] = []

        for p in payoff_points:
            x, y = self._extract_xy(p)
            try:
                xs.append(float(x))
                ys.append(float(y))
            except Exception:
                continue

        if not xs:
            payoff_info("ERROR: não consegui extrair xs/ys de payoff_points.")
            self.ax.set_title("Sem dados de payoff")
            self._safe_draw_idle()
            self._last_breakevens = []
            self._last_pl_at_spot_ref = None
            self._set_payoff_comment(
                "Os pontos de payoff foram encontrados, mas não foi possível "
                "extrair valores numéricos válidos para gerar a interpretação."
            )
            return self.get_last_overlays()

        payoff_debug(
            f"rebuilt xs: min={min(xs):.2f}, max={max(xs):.2f}, len={len(xs)}"
        )
        payoff_debug(
            f"rebuilt ys: min={min(ys):.6f}, max={max(ys):.6f}, len={len(ys)}"
        )

        # ------------------------------------------------------------------
        # Label da curva principal (B quando há overlay, senão "Payoff")
        # ------------------------------------------------------------------
        if overlay_curve and decision_data:
            sid = (
                decision_data.get("structure_id")
                or decision_data.get("aba", "")
            )
            main_label = f"B: {sid}"
        else:
            main_label = "Payoff"

        self.ax.plot(xs, ys, color="#1f77b4", linewidth=2, label=main_label)

        # ------------------------------------------------------------------
        # Curva A (overlay fixado)
        # ------------------------------------------------------------------
        if overlay_curve:
            overlay_xs: List[float] = []
            overlay_ys: List[float] = []
            for point in overlay_curve["points"]:
                try:
                    x, y = self._extract_xy(point)
                    overlay_xs.append(float(x))
                    overlay_ys.append(float(y))
                except Exception:
                    continue
            if overlay_xs:
                self.ax.plot(
                    overlay_xs,
                    overlay_ys,
                    color=overlay_curve["color"],
                    linewidth=2,
                    linestyle="--",
                    alpha=0.8,
                    label=overlay_curve["label"],
                )

        # ------------------------------------------------------------------
        # Linha PL = 0
        # ------------------------------------------------------------------
        self.ax.axhline(0, color="gray", linewidth=1, alpha=0.7)

        # ------------------------------------------------------------------
        # Preço de referência
        # ------------------------------------------------------------------
        spot_ref: Optional[float] = None
        if decision_data:
            raw = decision_data.get("spot_ref") or decision_data.get("spot_reference")
            try:
                spot_ref = float(raw) if raw is not None else None
            except Exception:
                spot_ref = None

        if spot_ref is not None:
            self.ax.axvline(
                spot_ref,
                color="#ff7f0e",
                linestyle="--",
                linewidth=1.5,
                label="Preço ref.",
            )
            pl_ref = self._interp_y_at_x(xs, ys, spot_ref)
            self._last_pl_at_spot_ref = pl_ref
            if pl_ref is not None:
                self.ax.scatter([spot_ref], [pl_ref], s=45, color="#ff7f0e", zorder=5)
                self.ax.annotate(
                    f"Preço ref.: {_fmt_number_br(spot_ref, 2)}\n"
                    f"PL: {_fmt_currency_br(pl_ref, 2)}",
                    xy=(spot_ref, pl_ref),
                    xytext=(8, 8),
                    textcoords="offset points",
                    fontsize=8,
                    color="#ff7f0e",
                    bbox=dict(
                        boxstyle="round,pad=0.2",
                        fc="white",
                        ec="#ff7f0e",
                        alpha=0.8,
                    ),
                )
        else:
            self._last_pl_at_spot_ref = None

        # ------------------------------------------------------------------
        # Pontos de equilíbrio (só da curva principal)
        # ------------------------------------------------------------------
        bks = self._find_breakevens(xs, ys)
        self._last_breakevens = bks

        for bx in bks:
            self.ax.axvline(bx, color="green", linestyle=":", linewidth=1, alpha=0.85)
            self.ax.scatter([bx], [0], s=30, color="green", zorder=6)
            self.ax.annotate(
                f"BE {_fmt_number_br(bx, 2)}",
                xy=(bx, 0),
                xytext=(0, 10),
                textcoords="offset points",
                ha="center",
                fontsize=8,
                color="green",
                bbox=dict(
                    boxstyle="round,pad=0.15",
                    fc="white",
                    ec="green",
                    alpha=0.75,
                ),
            )

        # ------------------------------------------------------------------
        # Comentário interpretativo
        # ------------------------------------------------------------------
        self._set_payoff_comment(
            self._build_payoff_comment(
                xs=xs,
                ys=ys,
                breakevens=bks,
                spot_ref=spot_ref,
                pl_ref=self._last_pl_at_spot_ref,
            )
        )

        # ------------------------------------------------------------------
        # Título
        # ------------------------------------------------------------------
        if decision_data:
            sid = (
                decision_data.get("structure_id")
                or decision_data.get("aba", "")
            )
            dec = decision_data.get("decision", "")
            title = f"Payoff -- {sid} [{dec}]"
            if overlay_curve:
                title += f" vs {overlay_curve['label']}"
        elif overlay_curve:
            title = "Curva de Payoff -- Comparação"
        else:
            title = "Curva de Payoff"

        self.ax.set_title(title)
        self.ax.legend(loc="best")
        self._safe_draw_idle()
        return self.get_last_overlays()

    # ------------------------------------------------------------------
    # Comentário interpretativo
    # ------------------------------------------------------------------

    def _set_payoff_comment(self, text: str):
        """Atualiza o comentário interpretativo exibido junto ao gráfico."""
        comment = text or "Sem dados de payoff para interpretação."
        self._last_payoff_comment = comment
        try:
            if self._comment_var is not None:
                self._comment_var.set(comment)
        except Exception:
            pass

    def _build_payoff_comment(
        self,
        xs: List[float],
        ys: List[float],
        breakevens: List[float],
        spot_ref: Optional[float],
        pl_ref: Optional[float],
    ) -> str:
        """Monta comentário textual em Português Brasil com base na curva calculada."""
        if not xs or not ys or len(xs) != len(ys):
            return (
                "Não há dados de payoff suficientes para interpretar ganho, perda, "
                "ponto de equilíbrio ou situação atual."
            )

        try:
            pairs = sorted((float(x), float(y)) for x, y in zip(xs, ys))
        except Exception:
            return (
                "Os dados de payoff não estão em formato numérico válido para "
                "gerar interpretação."
            )

        if not pairs:
            return (
                "Não há pontos válidos de payoff para interpretar a posição."
            )

        ordered_xs = [p[0] for p in pairs]
        ordered_ys = [p[1] for p in pairs]

        min_idx = min(range(len(ordered_ys)), key=lambda i: ordered_ys[i])
        max_idx = max(range(len(ordered_ys)), key=lambda i: ordered_ys[i])

        min_spot = ordered_xs[min_idx]
        min_pl = ordered_ys[min_idx]
        max_spot = ordered_xs[max_idx]
        max_pl = ordered_ys[max_idx]

        ganho = self._describe_pl_regions(ordered_xs, ordered_ys, positive=True)
        perda = self._describe_pl_regions(ordered_xs, ordered_ys, positive=False)

        if breakevens:
            pontos_equilibrio = ", ".join(_fmt_number_br(x, 2) for x in breakevens)
            equilibrio_txt = f"Ponto ou faixa de equilíbrio: {pontos_equilibrio}."
        else:
            equilibrio_txt = (
                "Ponto de equilíbrio: não identificado na faixa calculada."
            )

        if max_pl > 0:
            melhor_txt = (
                "Melhor região observada para ganho: próxima de "
                f"{_fmt_number_br(max_spot, 2)}, com PL estimado de "
                f"{_fmt_currency_br(max_pl, 2)}."
            )
        else:
            melhor_txt = (
                "Melhor região observada: a curva não mostra ganho positivo "
                "na faixa calculada; o melhor ponto reduz a perda para "
                f"{_fmt_currency_br(max_pl, 2)} próximo de "
                f"{_fmt_number_br(max_spot, 2)}."
            )

        if min_pl < 0:
            pior_txt = (
                "Pior região observada: próxima de "
                f"{_fmt_number_br(min_spot, 2)}, com PL estimado de "
                f"{_fmt_currency_br(min_pl, 2)}."
            )
        else:
            pior_txt = (
                "Pior região observada: a curva não mostra perda negativa "
                "na faixa calculada; o menor PL observado é "
                f"{_fmt_currency_br(min_pl, 2)} próximo de "
                f"{_fmt_number_br(min_spot, 2)}."
            )

        situacao_txt = self._describe_spot_ref_status(spot_ref, pl_ref)

        return (
            f"Região de ganho: {ganho}. "
            f"Região de perda: {perda}. "
            f"{melhor_txt} "
            f"{pior_txt} "
            f"{equilibrio_txt} "
            f"{situacao_txt} "
            "Comentário baseado apenas na curva calculada pelo sistema, sem promessa "
            "de resultado financeiro."
        )

    def _describe_spot_ref_status(
        self,
        spot_ref: Optional[float],
        pl_ref: Optional[float],
    ) -> str:
        """Descreve a situação atual em relação ao preço de referência."""
        if spot_ref is None:
            return (
                "Situação atual: preço de referência não informado para esta curva."
            )

        if pl_ref is None:
            return (
                "Situação atual: o preço de referência "
                f"{_fmt_number_br(spot_ref, 2)} está fora da faixa calculada "
                "ou não pôde ser interpolado."
            )

        if pl_ref > 0:
            status = "em região de ganho"
        elif pl_ref < 0:
            status = "em região de perda"
        else:
            status = "próxima do equilíbrio"

        return (
            "Situação atual: no preço de referência "
            f"{_fmt_number_br(spot_ref, 2)}, o PL estimado é "
            f"{_fmt_currency_br(pl_ref, 2)}, indicando posição {status}."
        )

    @classmethod
    def _describe_pl_regions(
        cls,
        xs: List[float],
        ys: List[float],
        positive: bool,
    ) -> str:
        """Descreve faixas aproximadas de ganho ou perda na curva calculada."""
        if not xs or not ys or len(xs) != len(ys):
            return "não identificada por falta de dados"

        try:
            pairs = sorted((float(x), float(y)) for x, y in zip(xs, ys))
        except Exception:
            return "não identificada por dados inválidos"

        if len(pairs) == 1:
            x, y = pairs[0]
            if positive and y > 0:
                return f"no ponto calculado {_fmt_number_br(x, 2)}"
            if not positive and y < 0:
                return f"no ponto calculado {_fmt_number_br(x, 2)}"
            return "não identificada na faixa calculada"

        ordered_xs = [p[0] for p in pairs]
        ordered_ys = [p[1] for p in pairs]
        breakevens = cls._find_breakevens(ordered_xs, ordered_ys)

        intervals: List[Tuple[float, float]] = []
        tol = 1e-9

        for i in range(len(ordered_xs) - 1):
            x0 = ordered_xs[i]
            x1 = ordered_xs[i + 1]

            if x0 == x1:
                continue

            low = min(x0, x1)
            high = max(x0, x1)

            cuts = [low]
            for bk in breakevens:
                if low < bk < high:
                    cuts.append(bk)
            cuts.append(high)
            cuts = sorted(cuts)

            for j in range(len(cuts) - 1):
                a = cuts[j]
                b = cuts[j + 1]
                if abs(a - b) <= tol:
                    continue

                mid = (a + b) / 2
                y_mid = cls._interp_y_at_x(ordered_xs, ordered_ys, mid)
                if y_mid is None:
                    continue

                if positive and y_mid > tol:
                    intervals.append((a, b))
                elif not positive and y_mid < -tol:
                    intervals.append((a, b))

        if not intervals:
            isolated = []
            for x, y in pairs:
                if positive and y > tol:
                    isolated.append(x)
                elif not positive and y < -tol:
                    isolated.append(x)

            if isolated:
                if len(isolated) == 1:
                    return f"próxima de {_fmt_number_br(isolated[0], 2)}"
                return (
                    "entre aproximadamente "
                    f"{_fmt_number_br(min(isolated), 2)} e "
                    f"{_fmt_number_br(max(isolated), 2)}"
                )

            return "não identificada na faixa calculada"

        merged: List[Tuple[float, float]] = []
        for a, b in sorted(intervals):
            if not merged:
                merged.append((a, b))
                continue

            last_a, last_b = merged[-1]
            if abs(a - last_b) <= 1e-7 or a <= last_b:
                merged[-1] = (last_a, max(last_b, b))
            else:
                merged.append((a, b))

        full_low = min(ordered_xs)
        full_high = max(ordered_xs)
        if (
            len(merged) == 1
            and abs(merged[0][0] - full_low) <= 1e-7
            and abs(merged[0][1] - full_high) <= 1e-7
        ):
            return (
                "em toda a faixa calculada "
                f"({_fmt_number_br(full_low, 2)} até {_fmt_number_br(full_high, 2)})"
            )

        parts = [
            f"{_fmt_number_br(a, 2)} até {_fmt_number_br(b, 2)}"
            for a, b in merged[:3]
        ]
        if len(merged) > 3:
            parts.append("outras faixas calculadas")

        return "aproximadamente de " + "; ".join(parts)

    # ------------------------------------------------------------------
    # Utilitários de extração e interpolação
    # ------------------------------------------------------------------

    def _extract_xy(self, p) -> Tuple[Optional[float], Optional[float]]:
        """
        Extrai (x, y) de múltiplos formatos:
        - tuple/list   (p[0], p[1])
        - dict         chaves canônicas e alternativas
        - sqlite Row   idem via indexação
        """
        if isinstance(p, (tuple, list)) and len(p) >= 2:
            return p[0], p[1]

        x = self._get_field(
            p, ["point_spot", "spot", "x", "underlying", "price", "underlying_spot"]
        )
        y = self._get_field(
            p, ["point_pl", "pl", "y", "pnl", "payoff", "profit_loss", "pl_value"]
        )
        return x, y

    def _get_field(self, obj, keys: List[str], default=None):
        """Tenta extrair campo de dict, Mapping ou objeto com atributo."""
        if isinstance(obj, dict):
            for k in keys:
                if k in obj:
                    return obj[k]
        for k in keys:
            try:
                return obj[k]
            except Exception:
                pass
        for k in keys:
            try:
                if hasattr(obj, k):
                    return getattr(obj, k)
            except Exception:
                pass
        return default

    @staticmethod
    def _find_breakevens(spots: List[float], pls: List[float]) -> List[float]:
        """Retorna lista de spots onde PL cruza zero (interpolação linear)."""
        bks: List[float] = []
        if not spots or not pls or len(spots) != len(pls):
            return bks

        for i in range(len(spots) - 1):
            x0, y0 = spots[i], pls[i]
            x1, y1 = spots[i + 1], pls[i + 1]

            if y0 == 0:
                bks.append(float(x0))
                continue

            crosses = (y0 < 0 and y1 > 0) or (y0 > 0 and y1 < 0) or (y1 == 0)
            if crosses:
                if y1 == y0:
                    continue
                xz = x0 + (-y0) * (x1 - x0) / (y1 - y0)
                bks.append(float(xz))

        # Deduplicar e ordenar
        out: List[float] = []
        for x in sorted(bks):
            if not out or abs(x - out[-1]) > 1e-9:
                out.append(x)
        return out

    @staticmethod
    def _interp_y_at_x(
        xs: List[float], ys: List[float], x: float
    ) -> Optional[float]:
        """Interpolação linear por segmento. Retorna None se fora do range."""
        if not xs or not ys or len(xs) != len(ys):
            return None
        try:
            x = float(x)
        except Exception:
            return None

        for i in range(len(xs) - 1):
            x0, x1 = xs[i], xs[i + 1]
            y0, y1 = ys[i], ys[i + 1]
            if x0 == x1:
                continue
            if (x0 <= x <= x1) or (x1 <= x <= x0):
                t = (x - x0) / (x1 - x0)
                try:
                    return float(y0 + t * (y1 - y0))
                except Exception:
                    return None
        return None
