# UI/components/decisions_grid.py
import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Callable


def _fmt_pct(x):
    try:
        return f"{float(x):.1%}"
    except Exception:
        return "N/A"


class DecisionsGrid(ttk.LabelFrame):
    def __init__(self, parent, on_selection_change: Callable):
        super().__init__(parent, text="Decisões", padding=5)
        self.on_selection_change = on_selection_change
        self.current_data: List[Dict] = []
        self._setup_treeview()
    
    def _setup_treeview(self):
        frame = ttk.Frame(self)
        frame.pack(fill='both', expand=True)
        
        columns = ('timestamp', 'aba', 'decision', 'level', 'pl_pct', 'dte_min')
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', height=16)
        
        self.tree.heading('timestamp', text='Data/Hora')
        self.tree.heading('aba', text='Aba')
        self.tree.heading('decision', text='Decisão')
        self.tree.heading('level', text='Nível')
        self.tree.heading('pl_pct', text='PL %')
        self.tree.heading('dte_min', text='DTE')
        
        self.tree.column('timestamp', width=140, anchor='w')
        self.tree.column('aba', width=100, anchor='w')
        self.tree.column('decision', width=130, anchor='center')
        self.tree.column('level', width=60, anchor='center')
        self.tree.column('pl_pct', width=90, anchor='e')
        self.tree.column('dte_min', width=60, anchor='e')
        
        vbar = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
        hbar = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        vbar.grid(row=0, column=1, sticky='ns')
        hbar.grid(row=1, column=0, sticky='ew')
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        self.tree.bind('<<TreeviewSelect>>', self._on_select)
        
        # Tags (cores)
        self.tree.tag_configure('close', background='#ffcccc')   # CLOSE_REOPEN
        self.tree.tag_configure('prepare', background='#ffffcc') # PREPARE_ROLL
        self.tree.tag_configure('watch', background='#ccffcc')   # HOLD nível > 0
    
    def _on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        try:
            idx = int(iid) - 1
        except Exception:
            idx = 0
        if 0 <= idx < len(self.current_data):
            self.on_selection_change(self.current_data[idx])
    
    def update_data(self, decisions: List[Dict]):
        self.current_data = decisions or []
        # limpar
        for iid in self.tree.get_children():
            self.tree.delete(iid)
        # repopular
        for i, d in enumerate(self.current_data, start=1):
            ts = (d.get('timestamp') or '')[:19]
            aba = d.get('aba') or ''
            dec = d.get('decision') or ''
            lvl = d.get('level') if d.get('level') is not None else ''
            plp = _fmt_pct(d.get('pl_pct_of_max')) if d.get('pl_pct_of_max') is not None else 'N/A'
            dte = d.get('dte_min') if d.get('dte_min') is not None else ''
            iid = str(i)
            self.tree.insert('', 'end', iid=iid, values=(ts, aba, dec, lvl, plp, dte))
            # tags
            if dec == "CLOSE_REOPEN":
                self.tree.item(iid, tags=('close',))
            elif dec == "PREPARE_ROLL":
                self.tree.item(iid, tags=('prepare',))
            elif dec == "HOLD" and isinstance(lvl, (int, float)) and lvl > 0:
                self.tree.item(iid, tags=('watch',))
    
    def get_current_data(self) -> List[Dict]:
        return list(self.current_data or [])
