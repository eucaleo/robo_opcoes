# UI/components/payoff_chart.py
from matplotlib.ticker import FuncFormatter
import json
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from UI.debug_utils import payoff_debug, payoff_info
from tkinter import filedialog
from tkinter import ttk
from typing import List, Dict, Optional, Tuple

import matplotlib
matplotlib.use("TkAgg")  # necessário para renderizar no Tkinter


def _fmt_number_br(x: float, decimals: int = 2) -> str:
    """Formata número no padrão pt-BR: milhar '.' e decimal ','."""
    try:
        s = f"{float(x):,.{decimals}f}"
        # en-US -> 1,234.56; pt-BR -> 1.234,56
        return s.replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return str(x)


def _fmt_currency_br(x: float, decimals: int = 2) -> str:
    return f"R$ {_fmt_number_br(x, decimals=decimals)}"


class PayoffChart(ttk.Frame):

    def _as_dict(self, obj):
        """Normalize obj into dict when it may come as dict or JSON string or plain string."""
        if isinstance(obj, dict):
            return obj
        if isinstance(obj, str):
            s = obj.strip()
            # try JSON object
            if (s.startswith("{") and s.endswith("}")):
                try:
                    parsed = json.loads(s)
                    if isinstance(parsed, dict):
                        return parsed
                except Exception:
                    pass
            # treat plain string as 'aba'
            return {"aba": obj}
        return {}

    @staticmethod
    def _find_breakevens(spots: List[float], pls: List[float]) -> List[float]:
        """Retorna lista de spots onde PL cruza 0 (interpolação linear)."""
        bks = []
        if not spots or not pls or len(spots) != len(pls):
            return bks
        for i in range(len(spots) - 1):
            x0, y0 = spots[i], pls[i]
            x1, y1 = spots[i + 1], pls[i + 1]

            if y0 == 0:
                bks.append(float(x0))
                continue

            crosses = ((y0 < 0 and y1 > 0) or (y0 > 0 and y1 < 0) or (y1 == 0))
            if crosses:
                if y1 == y0:
                    continue
                xz = x0 + (-y0) * (x1 - x0) / (y1 - y0)
                bks.append(float(xz))

        # dedupe aproximado + ordenar
        out = []
        for x in sorted(bks):
            if not out or abs(x - out[-1]) > 1e-9:
                out.append(x)
        return out

    @staticmethod
    def _interp_y_at_x(
            xs: List[float],
            ys: List[float],
            x: float) -> Optional[float]:
        """Interpolação linear por segmento. Retorna None se fora do range ou inválido."""
        if not xs or not ys or len(xs) != len(ys):
            return None
        try:
            x = float(x)
        except Exception:
            return None

        # garantir monotônico crescente (sem reordenar agressivamente)
        for i in range(len(xs) - 1):
            x0, x1 = xs[i], xs[i + 1]
            y0, y1 = ys[i], ys[i + 1]
            if x0 == x1:
                continue
            if (x0 <= x <= x1) or (x1 <= x <= x0):
                # segmento contém x
                t = (x - x0) / (x1 - x0)
                try:
                    return float(y0 + t * (y1 - y0))
                except Exception:
                    return None
        return None

    def __init__(self, parent):
        super().__init__(parent, padding=6)
        self._last_breakevens: List[float] = []
        self._last_pl_at_spot_ref: Optional[float] = None
        self._build_canvas()
        # Comparação (P5.8.3): overlay de curvas
        # {"points": [...], "label": "...", "color": "..."}
        self._fixed_curve = None

    def _safe_draw_idle(self):
        """Garante draw no thread do Tk."""
        try:
            self.after(0, self.canvas.draw_idle)
        except Exception:
            try:
                self._safe_draw_idle()
            except Exception:
                pass

    def _build_canvas(self):
        # Top bar (toolbar + export)
        top = ttk.Frame(self)
        top.pack(fill="x", side="top")

        self.btn_export = ttk.Button(
            top, text="Exportar PNG", command=self.export_png)
        self.btn_export.pack(side="right", padx=(6, 0))
        self.btn_fix_curve = ttk.Button(
            top, text="Fixar Curva A", command=self.fix_current_curve)
        self.btn_fix_curve.pack(side="right", padx=(0, 6))

        self.btn_clear_comparison = ttk.Button(
            top, text="Limpar Comparação", command=self.clear_comparison)
        self.btn_clear_comparison.pack(side="right", padx=(0, 6))

        # Figure/canvas
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Toolbar do matplotlib (precisa do canvas existir)
        self.toolbar = NavigationToolbar2Tk(
            self.canvas, top, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.pack(side="left", fill="x", expand=True)

        self._reset_axes()
        self._safe_draw_idle()

        # IMPORTANT: ttk.Notebook pode criar o canvas com tamanho 0x0 quando a aba não está visível.
        # Ao redimensionar/mostrar, forçamos redraw.
        self.bind("<Configure>", self._on_configure, add=True)
    def _on_configure(self, event=None):
        # evita loop/desenho excessivo: só redesenha quando tem área útil
        try:
            w = int(self.winfo_width())
            h = int(self.winfo_height())
        except Exception:
            return
        if w <= 50 or h <= 50:
            return
        try:
            # atualiza toolbar e força redraw do canvas
            if hasattr(self, "toolbar"):
                self.toolbar.update()
        except Exception:
            pass
        self._safe_draw_idle()

    def _reset_axes(self):
        self.ax.clear()
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel("Spot")
        self.ax.set_ylabel("PL")
        # Format Y-axis as BRL with abbreviations (k/M/B) for readability
        def _brl_abbrev(x, pos=None):
            try:
                x = float(x)
            except Exception:
                return "R$ 0"
            ax = abs(x)
            sign = "-" if x < 0 else ""
            if ax >= 1_000_000_000:
                return "{}R$ {:.1f}B".format(sign, ax/1_000_000_000)
            if ax >= 1_000_000:
                return "{}R$ {:.1f}M".format(sign, ax/1_000_000)
            if ax >= 1_000:
                return "{}R$ {:.0f}k".format(sign, ax/1_000)
            return "{}R$ {:.0f}".format(sign, ax)
        self.ax.yaxis.set_major_formatter(FuncFormatter(_brl_abbrev))
        self.ax.set_title("Curva de Payoff")

        # Formatadores BR
        self.ax.xaxis.set_major_formatter(
            FuncFormatter(lambda v, pos: _fmt_number_br(v, 2)))
        # por padrão tratar PL como moeda (se quiser mudar depois, a gente
        # parametriza)
        self.ax.yaxis.set_major_formatter(
            FuncFormatter(
                lambda v, pos: _fmt_currency_br(
                    v, 0 if abs(v) >= 1000 else 2)))

    def clear(self):
        self._last_breakevens = []
        self._last_pl_at_spot_ref = None
        self._reset_axes()
        self._safe_draw_idle()

    def fix_current_curve(self):
        payoff_debug("FIX clicked")
        payoff_debug("FIX: self id=", id(self))
        payoff_debug("FIX: has _last_points=", hasattr(self, "_last_points"), "len=", (len(self._last_points) if getattr(self, "_last_points", None) else 0))
        """Fixa a curva atual como A para comparação"""
        if not hasattr(self, "_last_points") or not self._last_points:
            self._fixed_curve = None
            return

        # Salva no formato canônico esperado pelo overlay: points=[{spot, pl}, ...]
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

        # Redesenhar com overlay
        self._redraw_current()


    def clear_comparison(self):
        payoff_debug("CLEAR comparison clicked")
        payoff_debug("CLEAR: self id=", id(self))
        """Remove curva fixada"""
        self._fixed_curve = None
        # Redesenhar sem overlay
        if hasattr(self, '_last_points') and self._last_points:
            self._redraw_current()

    def _redraw_with_overlay(self):
        """Redesenha gráfico atual + curva fixada"""
        if not hasattr(self, '_last_points') or not self._last_points:
            return

        # Salvar dados atuais
        current_points = self._last_points
        current_decision = getattr(self, '_last_decision_data', {})

        # Redesenhar
        self._draw_curves_and_overlays(
            current_points,
            current_decision,
            overlay_curve=self._fixed_curve)

    def _redraw_current(self):
        """Redesenha apenas gráfico atual"""
        if hasattr(self, "_last_points") and self._last_points:
            current_points = self._last_points
            current_decision = getattr(self, "_last_decision_data", {}) or {}
            # Mantém overlay se houver curva fixada
            self._draw_curves_and_overlays(
                current_points, current_decision, overlay_curve=self._fixed_curve
            )



    def _get_field(self, obj, keys, default=None):
        """
        Tenta extrair campo de:
          - dict (várias chaves possíveis)
          - sqlite3.Row / Mapping
          - objeto com atributo
        """
        # dict-like
        try:
            if isinstance(obj, dict):
                for k in keys:
                    if k in obj:
                        return obj[k]
        except Exception:
            pass

        # mapping (sqlite row, etc)
        for k in keys:
            try:
                return obj[k]
            except Exception:
                pass

        # attribute
        for k in keys:
            try:
                if hasattr(obj, k):
                    return getattr(obj, k)
            except Exception:
                pass

        return default

    def _extract_xy(self, p):
        """
        Extrai (x,y) de formatos comuns.
        Retorna (None, None) se não conseguir.
        """
        # tupla/lista (spot, pl)
        try:
            if isinstance(p, (tuple, list)) and len(p) >= 2:
                return p[0], p[1]
        except Exception:
            pass

        x = self._get_field(p, ["point_spot", "spot", "x", "underlying", "price", "underlying_spot"])
        y = self._get_field(p, ["point_pl", "pl", "y", "pnl", "payoff", "profit_loss", "pl_value"])
        return x, y

    def update_chart(
            self,
            payoff_points: List[Dict],
            decision_data: Optional[Dict] = None) -> Dict:
        """Atualiza curva (preserva para comparação e redesenha com overlay se existir)"""
        # Salvar para comparação/redesenho
        self._last_points = list(payoff_points) if payoff_points else []
        self._last_decision_data = dict(decision_data) if decision_data else {}

        # Desenhar
        return self._draw_curves_and_overlays(
            payoff_points, decision_data, overlay_curve=self._fixed_curve)

    def _draw_curves_and_overlays(
            self,
            payoff_points: List[Dict],
            decision_data: Optional[Dict],
            overlay_curve: Optional[Dict]) -> Dict:
        """Versão unificada do desenho (curva principal + overlay + breakevens/spot_ref)"""
        self._reset_axes()

        if not payoff_points:
            self.ax.set_title("Sem dados de payoff")
            self._safe_draw_idle()
            self._last_breakevens = []
            self._last_pl_at_spot_ref = None
            return self.get_last_overlays()

        # === CURVA PRINCIPAL (B ou única) ===
        xs, ys = [], []  # payoff_points é lista; xs/ys serão reconstruídos abaixo
        if False and not xs:
            self.ax.set_title("Sem dados de payoff")
            self._safe_draw_idle()
            self._last_breakevens = []
            self._last_pl_at_spot_ref = None
            return self.get_last_overlays()

        # Label da curva principal
        main_label = "Payoff"
        if overlay_curve:
            aba = decision_data.get(
                'aba', 'Atual') if decision_data else 'Atual'
            main_label = f"B: {aba}"

        # DEBUG: valores sendo plotados
        if xs and ys:
            payoff_debug(f" xs: min={min(xs):.2f}, max={max(xs):.2f}, len={len(xs)}")
            payoff_debug(f" ys: min={min(ys):.6f}, max={max(ys):.6f}, len={len(ys)}")

        # DEBUG: quais variáveis existem aqui e quais têm len

        try:

            _brief = {}

            for _k, _v in list(locals().items()):

                if _k in ("self",):

                    continue

                _t = type(_v).__name__

                try:

                    _l = len(_v)

                except Exception:

                    _l = None

                _brief[_k] = (_t, _l)

            payoff_debug(" locals@plot:", _brief)

        except Exception as e:

            payoff_debug(" locals@plot failed:", e)

        # Rebuild xs/ys from payoff_points (canonical: point_spot/point_pl)

        try:

            _raw_pts = payoff_points

        except Exception:

            _raw_pts = []

        

        # Debug sample

        try:

            _sample = list(_raw_pts)[:3]

        except Exception:

            _sample = []

        payoff_debug(" payoff_points sample=", _sample)

        

        xs = []

        ys = []

        for _p in _raw_pts:

            _x, _y = self._extract_xy(_p)

            try:

                _x = float(_x)

                _y = float(_y)

            except Exception:

                continue

            xs.append(_x)

            ys.append(_y)

        

        if xs and ys:

            payoff_debug(" rebuilt xs: min={:.2f}, max={:.2f}, len={}".format(min(xs), max(xs), len(xs)))

            payoff_debug(" rebuilt ys: min={:.6f}, max={:.6f}, len={}".format(min(ys), max(ys), len(ys)))

        else:

            payoff_info("ERROR: não consegui extrair xs/ys de payoff_points (ver sample acima).")

        self.ax.plot(xs, ys, color="#1f77b4", linewidth=2, label=main_label)
        # === CURVA FIXA (A, se existir) ===
        if overlay_curve:
            # Extract xs, ys from overlay points list
            overlay_xs, overlay_ys = [], []
            for point in overlay_curve["points"]:
                try:
                    x, y = self._extract_xy(point)
                    overlay_xs.append(float(x))
                    overlay_ys.append(float(y))
                except Exception:
                    continue
            if overlay_xs:
                self.ax.plot(
                    overlay_xs, overlay_ys,
                    color=overlay_curve["color"],
                    linewidth=2,
                    linestyle='--',
                    alpha=0.8,
                    label=overlay_curve["label"]
                )

        # === OVERLAYS (só da curva principal) ===
        # PL=0
        self.ax.axhline(0, color="gray", linewidth=1, alpha=0.7)

        # Spot Ref
        spot_ref = None
        if decision_data:
            spot_ref = decision_data.get("spot_ref")
            if spot_ref is None:
                spot_ref = decision_data.get("spot_reference")
            if spot_ref is None:
                spot_ref = decision_data.get("spot_reference")
        try:
            spot_ref = float(spot_ref) if spot_ref is not None else None
        except Exception:
            spot_ref = None

        if spot_ref is not None:
            self.ax.axvline(
                spot_ref,
                color="#ff7f0e",
                linestyle="--",
                linewidth=1.5,
                label="Spot Ref")
            pl_ref = self._interp_y_at_x(xs, ys, spot_ref)
            self._last_pl_at_spot_ref = pl_ref
            if pl_ref is not None:
                self.ax.scatter(
                    [spot_ref],
                    [pl_ref],
                    s=45,
                    color="#ff7f0e",
                    zorder=5)
                self.ax.annotate(
                    f"Spot Ref: {_fmt_number_br(spot_ref, 2)}\nPL: {_fmt_currency_br(pl_ref, 2)}",
                    xy=(spot_ref, pl_ref),
                    xytext=(8, 8),
                    textcoords="offset points",
                    fontsize=8,
                    color="#ff7f0e",
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#ff7f0e", alpha=0.8),
                )
            else:
                self._last_pl_at_spot_ref = None

        # Breakevens (só da curva principal)
        bks = self._find_breakevens(xs, ys)
        self._last_breakevens = bks

        for bx in bks:
            self.ax.axvline(
                bx,
                color="green",
                linestyle=":",
                linewidth=1,
                alpha=0.85)
            self.ax.scatter([bx], [0], s=30, color="green", zorder=6)
            self.ax.annotate(
                f"BE {_fmt_number_br(bx, 2)}",
                xy=(bx, 0),
                xytext=(0, 10),
                textcoords="offset points",
                ha="center",
                fontsize=8,
                color="green",
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="green", alpha=0.75),
            )

        # Título
        title = "Curva de Payoff"
        if decision_data:
            aba = decision_data.get("aba", "")
            dec = decision_data.get("decision", "")
            title = f"Payoff - {aba} [{dec}]"
            if overlay_curve:
                title += " vs " + overlay_curve["label"]
        elif overlay_curve:
            title += " - Comparação"

        self.ax.set_title(title)
        self.ax.legend(loc="best")
        self._safe_draw_idle()
        return self.get_last_overlays()

    def _extract_xy_legacy__disabled_1(self, points: List[Dict]
                    ) -> Tuple[List[float], List[float]]:
        """Extrai listas xs, ys de pontos, ordenando por x"""
        if not points:
            return [], []

        xs, ys = [], []
        for p in points:
            try:
                # Aceita contrato UI {spot, pl} e contrato canônico DB {point_spot, point_pl}
                x = p.get("spot")
                y = p.get("pl")
                if x is None:
                    x = p.get("point_spot")
                if y is None:
                    y = p.get("point_pl")

                if x is None or y is None:
                    continue

                xs.append(float(x))
                ys.append(float(y))
            except Exception:
                continue

        if not xs or len(xs) != len(ys):
            return [], []

        # Ordenar por spot
        pts_sorted = sorted(zip(xs, ys), key=lambda t: t[0])
        return [a for a, _ in pts_sorted], [b for _, b in pts_sorted]

    def get_last_overlays(self) -> Dict:
        """Para integração com DetailsPanel: breakevens e PL interpolado no spot_ref."""
        return {
            "breakevens": list(self._last_breakevens),
            "pl_at_spot_ref": self._last_pl_at_spot_ref,
        }

    def export_png(self):
        """Exporta o gráfico atual para PNG."""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG", "*.png")],
                title="Salvar gráfico como PNG",
            )
            if not file_path:
                return
            self.fig.savefig(file_path, dpi=150, bbox_inches="tight")
        except Exception as e:
            print("[UI] Falha ao exportar PNG:", e)

        # Breakevens da curva principal
        breakevens = self._find_breakevens(xs, ys)
        self._last_breakevens = breakevens
        for be in breakevens:
            self.ax.axvline(be, color="red", linestyle=":", alpha=0.8, linewidth=1)

        # Spot reference (se existir na decisão)
        spot_ref = None
        if decision_data:
            spot_ref = decision_data.get('spot_reference')
            if spot_ref:
                self.ax.axvline(spot_ref, color="green", linestyle="-", alpha=0.9, linewidth=2, label="Spot Ref")
                # Calcular PL no spot reference
                pl_at_spot_ref = self._interp_y_at_x(xs, ys, spot_ref)
                self._last_pl_at_spot_ref = pl_at_spot_ref

        # Título com informações
        title_parts = []
        if decision_data:
            aba = decision_data.get('aba')
            if aba:
                title_parts.append(f"Aba: {aba}")
            decision = decision_data.get('decision')
            if decision:
                title_parts.append(f"Decisão: {decision}")

        if overlay_curve:
            title_parts.append("(Comparação)")

        title = " | ".join(title_parts) if title_parts else "Curva de Payoff"
        self.ax.set_title(title)

        # Legenda (se houver múltiplas curvas ou spot ref)
        if overlay_curve or spot_ref:
            self.ax.legend()

        self._safe_draw_idle()
        return self.get_last_overlays()

    def get_last_overlays(self) -> Dict:
        """Retorna dados dos overlays da última atualização"""
        return {
            'breakevens': list(self._last_breakevens),
            'pl_at_spot_ref': self._last_pl_at_spot_ref
        }

    def _extract_xy_legacy__disabled_2(self, points: List[Dict]) -> tuple:
        """Extrai listas de x,y dos pontos de payoff"""
        if not points:
            return [], []
        
        xs, ys = [], []
        for point in points:
            try:
                x = float(point.get('point_spot', 0))
                y = float(point.get('point_pl', 0))
                xs.append(x)
                ys.append(y)
            except (ValueError, TypeError):
                continue
                
        return xs, ys

    def export_png(self):
        """Exporta gráfico atual como PNG"""
        from tkinter import filedialog, messagebox
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Exportar gráfico"
        )
        
        if filename:
            try:
                self.fig.savefig(filename, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Sucesso", f"Gráfico salvo em {filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {e}")

