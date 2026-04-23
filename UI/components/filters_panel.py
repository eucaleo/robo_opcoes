# UI/components/filters_panel.py
import tkinter as tk
from tkinter import ttk
from typing import Dict, Callable
from datetime import datetime, timedelta


class FiltersPanel(ttk.LabelFrame):
    def __init__(self, parent, on_filter_change: Callable):
        super().__init__(parent, text="Filtros", padding=10)
        self.on_filter_change = on_filter_change
        self._setup_widgets()
        self._bind_events()
    
    def _setup_widgets(self):
        # Linha 1: Período
        row1 = ttk.Frame(self)
        row1.pack(fill='x', pady=2)
        ttk.Label(row1, text="Período:").pack(side='left', padx=(0, 5))
        
        self.date_from = ttk.Entry(row1, width=12)
        self.date_from.pack(side='left', padx=2)
        self.date_from.insert(0, (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"))
        
        ttk.Label(row1, text="até").pack(side='left', padx=5)
        
        self.date_to = ttk.Entry(row1, width=12)
        self.date_to.pack(side='left', padx=2)
        self.date_to.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Linha 2: Aba e Decisão
        row2 = ttk.Frame(self)
        row2.pack(fill='x', pady=2)
        ttk.Label(row2, text="Aba:").pack(side='left', padx=(0, 5))
        
        self.aba_combo = ttk.Combobox(row2, width=18, state="readonly")
        self.aba_combo.pack(side='left', padx=2)
        
        ttk.Label(row2, text="Decisão:").pack(side='left', padx=(15, 5))
        self.decision_combo = ttk.Combobox(row2, width=18, state="readonly")
        self.decision_combo['values'] = ["Todas", "HOLD", "PREPARE_ROLL", "CLOSE_REOPEN"]
        self.decision_combo.set("Todas")
        self.decision_combo.pack(side='left', padx=2)
        
        # Botões
        btn_frame = ttk.Frame(row2)
        btn_frame.pack(side='right', padx=10)
        ttk.Button(btn_frame, text="Aplicar", command=self._apply_filters).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Limpar", command=self.reset_filters).pack(side='left', padx=2)
    
    def _bind_events(self):
        self.date_from.bind('<Return>', lambda e: self._apply_filters())
        self.date_to.bind('<Return>', lambda e: self._apply_filters())
        self.aba_combo.bind('<<ComboboxSelected>>', lambda e: self._apply_filters())
        self.decision_combo.bind('<<ComboboxSelected>>', lambda e: self._apply_filters())
    
    def _apply_filters(self):
        filters = {
            'date_from': self.date_from.get().strip(),
            'date_to': self.date_to.get().strip(),
            'aba': self.aba_combo.get().strip() if self.aba_combo.get().strip() and self.aba_combo.get() != "Todas" else None,
            'decision': self.decision_combo.get() if self.decision_combo.get() != "Todas" else None
        }
        if self.on_filter_change:
            self.on_filter_change(filters)
    
    def reset_filters(self):
        self.date_from.delete(0, 'end')
        self.date_from.insert(0, (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"))
        self.date_to.delete(0, 'end')
        self.date_to.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.aba_combo.set("Todas" if "Todas" in (self.aba_combo['values'] or []) else "")
        self.decision_combo.set("Todas")
        self._apply_filters()
    
    def update_abas(self, abas_list):
        values = ["Todas"] + sorted(abas_list or [])
        self.aba_combo['values'] = values
        if not self.aba_combo.get():
            self.aba_combo.set("Todas")
