import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional, Callable
from datetime import datetime, timedelta


class FiltersPanel(ttk.LabelFrame):
    def __init__(self, parent, on_filter_change: Callable[[Dict], None]):
        super().__init__(parent, text="Filtros", padding=10)

        self.on_filter_change = on_filter_change
        self._setup_widgets()
        self._bind_events()

    def _setup_widgets(self):
        # Linha 1: Período
        row1 = ttk.Frame(self)
        row1.pack(fill='x', pady=(0, 5))

        ttk.Label(row1, text="Período:", width=10).pack(side='left')

        self.date_from_var = tk.StringVar()
        self.date_to_var = tk.StringVar()

        # Default: últimos 30 dias
        today = datetime.now()
        month_ago = today - timedelta(days=30)
        self.date_from_var.set(month_ago.strftime("%Y-%m-%d"))
        self.date_to_var.set(today.strftime("%Y-%m-%d"))

        ttk.Label(row1, text="De:").pack(side='left', padx=(10, 5))
        self.date_from_entry = ttk.Entry(
            row1, textvariable=self.date_from_var, width=12)
        self.date_from_entry.pack(side='left')

        ttk.Label(row1, text="Até:").pack(side='left', padx=(10, 5))
        self.date_to_entry = ttk.Entry(
            row1, textvariable=self.date_to_var, width=12)
        self.date_to_entry.pack(side='left')

        # Linha 2: Aba e Decisão
        row2 = ttk.Frame(self)
        row2.pack(fill='x', pady=5)

        ttk.Label(row2, text="Aba:", width=10).pack(side='left')
        self.aba_var = tk.StringVar()
        self.aba_combo = ttk.Combobox(
            row2,
            textvariable=self.aba_var,
            width=15,
            state='readonly')
        self.aba_combo.pack(side='left', padx=(0, 10))

        ttk.Label(row2, text="Decisão:").pack(side='left')
        self.decision_var = tk.StringVar()
        self.decision_combo = ttk.Combobox(
            row2,
            textvariable=self.decision_var,
            values=[
                '',
                'HOLD',
                'PREPARE_ROLL',
                'CLOSE_REOPEN',
                'ROLL',
                'ENTER'],
            width=15,
            state='readonly')
        self.decision_combo.pack(side='left', padx=(5, 0))

        # Linha 3: Level e DTE
        row3 = ttk.Frame(self)
        row3.pack(fill='x', pady=5)

        ttk.Label(row3, text="Level >=:", width=10).pack(side='left')
        self.level_var = tk.StringVar()
        self.level_entry = ttk.Entry(
            row3, textvariable=self.level_var, width=5)
        self.level_entry.pack(side='left', padx=(0, 10))

        ttk.Label(row3, text="DTE <=:").pack(side='left')
        self.dte_var = tk.StringVar()
        self.dte_entry = ttk.Entry(row3, textvariable=self.dte_var, width=5)
        self.dte_entry.pack(side='left', padx=(5, 10))

        # Botões
        btn_frame = ttk.Frame(row3)
        btn_frame.pack(side='right')

        self.apply_btn = ttk.Button(
            btn_frame,
            text="Aplicar",
            command=self._apply_filters)
        self.apply_btn.pack(side='left', padx=(0, 5))

        self.reset_btn = ttk.Button(
            btn_frame,
            text="Limpar",
            command=self.reset_filters)
        self.reset_btn.pack(side='left')

        # Status
        self.status_label = ttk.Label(
            self, text="Filtros prontos", foreground='green')
        self.status_label.pack(fill='x', pady=(5, 0))

    def _bind_events(self):
        # Enter em qualquer campo aplica filtros
        widgets = [
            self.date_from_entry,
            self.date_to_entry,
            self.level_entry,
            self.dte_entry]
        for w in widgets:
            w.bind('<Return>', lambda e: self._apply_filters())

        # Mudança nos combos aplica automaticamente
        self.aba_combo.bind(
            '<<ComboboxSelected>>',
            lambda e: self._apply_filters())
        self.decision_combo.bind(
            '<<ComboboxSelected>>',
            lambda e: self._apply_filters())

    def _apply_filters(self):
        filters = {}

        if self.date_from_var.get().strip():
            filters['date_from'] = self.date_from_var.get().strip()

        if self.date_to_var.get().strip():
            filters['date_to'] = self.date_to_var.get().strip()

        if self.aba_var.get().strip():
            filters['aba'] = self.aba_var.get().strip()

        if self.decision_var.get().strip():
            filters['decision'] = self.decision_var.get().strip()

        if self.level_var.get().strip():
            try:
                filters['level_min'] = int(self.level_var.get().strip())
            except ValueError:
                pass

        if self.dte_var.get().strip():
            try:
                filters['dte_max'] = int(self.dte_var.get().strip())
            except ValueError:
                pass

        self.status_label.config(
            text=f"Filtros aplicados ({
                len(filters)} ativos)",
            foreground='blue')
        self.on_filter_change(filters)

    def reset_filters(self):
        self.aba_var.set('')
        self.decision_var.set('')
        self.level_var.set('')
        self.dte_var.set('')

        # Manter período padrão (30 dias)
        today = datetime.now()
        month_ago = today - timedelta(days=30)
        self.date_from_var.set(month_ago.strftime("%Y-%m-%d"))
        self.date_to_var.set(today.strftime("%Y-%m-%d"))

        self.status_label.config(text="Filtros limpos", foreground='green')
        self._apply_filters()

    def update_abas(self, abas: List[str]):
        """Atualiza lista de abas no combo"""
        current = self.aba_var.get()
        values = [''] + sorted(abas)
        self.aba_combo.config(values=values)

        # Manter seleção se ainda válida
        if current not in values:
            self.aba_var.set('')
