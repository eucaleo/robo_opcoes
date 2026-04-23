# UI/components/details_panel.py
import tkinter as tk
from tkinter import ttk
import json
from typing import Dict, Optional


class DetailsPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self._build_ui()
    
    def _build_ui(self):
        # Grid de pares chave-valor
        info = ttk.LabelFrame(self, text="Resumo", padding=10)
        info.pack(fill='x')
        
        self.vars = {
            "Aba": tk.StringVar(),
            "Data/Hora": tk.StringVar(),
            "Decisão": tk.StringVar(),
            "Nível": tk.StringVar(),
            "PL % Máx": tk.StringVar(),
            "DTE (min)": tk.StringVar(),
        }
        
        row = 0
        for label, var in self.vars.items():
            ttk.Label(info, text=f"{label}:").grid(row=row, column=0, sticky='w', padx=(0,8), pady=2)
            ttk.Label(info, textvariable=var).grid(row=row, column=1, sticky='w', pady=2)
            row += 1
        
        # Why JSON
        whyf = ttk.LabelFrame(self, text="Why (JSON)", padding=10)
        whyf.pack(fill='both', expand=True, pady=(8,0))
        self.txt = tk.Text(whyf, height=12, wrap='word')
        self.txt.pack(fill='both', expand=True)
        self.txt.configure(state='disabled')
        
        btns = ttk.Frame(whyf)
        btns.pack(fill='x', pady=(6,0))
        ttk.Button(btns, text="Copiar", command=self._copy).pack(side='left')
        ttk.Button(btns, text="Limpar", command=self.clear).pack(side='left', padx=6)
    
    def _copy(self):
        try:
            self.txt.clipboard_clear()
            content = self.txt.get("1.0", "end-1c")
            self.txt.clipboard_append(content)
        except Exception:
            pass
    
    def clear(self):
        for v in self.vars.values():
            v.set("")
        self.txt.configure(state='normal')
        self.txt.delete("1.0", "end")
        self.txt.configure(state='disabled')
    
    def update_decision(self, d: Dict):
        self.vars["Aba"].set(d.get("aba", ""))
        self.vars["Data/Hora"].set((d.get("timestamp") or "")[:19])
        self.vars["Decisão"].set(d.get("decision", ""))
        self.vars["Nível"].set(str(d.get("level") if d.get("level") is not None else ""))
        plp = d.get("pl_pct_of_max")
        self.vars["PL % Máx"].set(f"{plp:.2%}" if isinstance(plp, (int,float)) and plp is not None else "N/A")
        self.vars["DTE (min)"].set(str(d.get("dte_min") if d.get("dte_min") is not None else ""))
        
        # Why JSON
        raw = d.get("why_json")
        pretty = ""
        if raw:
            try:
                obj = json.loads(raw) if isinstance(raw, str) else raw
                pretty = json.dumps(obj, ensure_ascii=False, indent=2)
            except Exception:
                pretty = str(raw)
        self.txt.configure(state='normal')
        self.txt.delete("1.0", "end")
        self.txt.insert("1.0", pretty)
        self.txt.configure(state='disabled')
