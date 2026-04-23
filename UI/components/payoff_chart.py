# UI/components/payoff_chart.py
import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Optional

import matplotlib
matplotlib.use("Agg")  # backend neutro; canvas TkAgg criará a figura
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class PayoffChart(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=6)
        self._build_canvas()
    
    def _build_canvas(self):
        self.fig = Figure(figsize=(5,4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel("Spot")
        self.ax.set_ylabel("PL")
        self.ax.set_title("Curva de Payoff")
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        self.canvas.draw_idle()
    
    def clear(self):
        self.ax.clear()
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel("Spot")
        self.ax.set_ylabel("PL")
        self.ax.set_title("Curva de Payoff")
        self.canvas.draw_idle()
    
    def update_chart(self, payoff_points: List[Dict], decision_data: Optional[Dict] = None):
        self.ax.clear()
        self.ax.grid(True, alpha=0.3)
        if not payoff_points:
            self.ax.set_title("Sem dados de payoff")
            self.canvas.draw_idle()
            return
        
        xs = [p.get("spot") for p in payoff_points]
        ys = [p.get("pl") for p in payoff_points]
        self.ax.plot(xs, ys, color="#1f77b4", linewidth=2, label="Payoff")
        
        # Título contextual
        title = "Curva de Payoff"
        if decision_data:
            aba = decision_data.get("aba", "")
            dec = decision_data.get("decision", "")
            title = f"Payoff - {aba} [{dec}]"
        self.ax.set_title(title)
        self.ax.set_xlabel("Spot")
        self.ax.set_ylabel("PL")
        self.ax.legend(loc="best")
        self.canvas.draw_idle()
