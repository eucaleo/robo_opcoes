#!/usr/bin/env python3
"""
UI Principal - Sistema de Derivados
Carrega dados de derived.db e app.db para exibir decisões e payoffs
"""
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from .components.filters_panel import FiltersPanel
from .components.decisions_grid import DecisionsGrid
from .components.details_panel import DetailsPanel
from .components.payoff_chart import PayoffChart
from .models.ui_data import UIDataModel


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Derivados - Análise de Decisões")
        self.root.geometry("1400x900")
        
        # Data model
        self.data_model = UIDataModel()
        
        # Configurar layout principal
        self._setup_layout()
        self._setup_menus()
        self._bind_events()
        
        # Carregar dados iniciais
        self.refresh_data()
    
    def _setup_layout(self):
        """Organiza layout em painéis"""
        
        # Frame principal com divisões
        main_paned = ttk.PanedWindow(self.root, orient='horizontal')
        main_paned.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Painel esquerdo (filtros + grid de decisões)
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        
        # Painel direito (detalhes + gráfico)
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)
        
        # === PAINEL ESQUERDO ===
        # Filtros no topo
        self.filters_panel = FiltersPanel(
            parent=left_frame,
            on_filter_change=self.on_filter_change
        )
        self.filters_panel.pack(fill='x', padx=5, pady=5)
        
        # Grid de decisões
        self.decisions_grid = DecisionsGrid(
            parent=left_frame,
            on_selection_change=self.on_decision_selected
        )
        self.decisions_grid.pack(fill='both', expand=True, padx=5, pady=5)
        
        # === PAINEL DIREITO ===
        # Notebook para abas de detalhes
        right_notebook = ttk.Notebook(right_frame)
        right_notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Aba 1: Detalhes da Decisão
        details_frame = ttk.Frame(right_notebook)
        right_notebook.add(details_frame, text="Detalhes da Decisão")
        
        self.details_panel = DetailsPanel(details_frame)
        self.details_panel.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Aba 2: Gráfico de Payoff
        chart_frame = ttk.Frame(right_notebook)
        right_notebook.add(chart_frame, text="Curva de Payoff")
        
        self.payoff_chart = PayoffChart(chart_frame)
        self.payoff_chart.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Status bar
        self.status_bar = ttk.Label(
            self.root, 
            text="Pronto", 
            relief=tk.SUNKEN,
            anchor='w'
        )
        self.status_bar.pack(side='bottom', fill='x')
    
    def _setup_menus(self):
        """Cria menu superior"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Atualizar Dados", command=self.refresh_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exportar CSV...", command=self.export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)
        
        # Menu Ferramentas
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ferramentas", menu=tools_menu)
        tools_menu.add_command(label="Executar Pipeline", command=self.run_pipeline)
        tools_menu.add_command(label="Verificar Bancos", command=self.check_databases)
        tools_menu.add_separator()
        tools_menu.add_command(label="Limpar Cache", command=self.clear_cache)
        
        # Menu Ajuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Sobre", command=self.show_about)
    
    def _bind_events(self):
        """Vincula eventos"""
        # F5 = refresh
        self.root.bind('<F5>', lambda e: self.refresh_data())
        
        # Ctrl+Q = quit
        self.root.bind('<Control-q>', lambda e: self.root.quit())
    
    # === CALLBACKS ===
    
    def on_filter_change(self, filters: Dict):
        """Callback quando filtros mudam"""
        self.status_bar.config(text="Aplicando filtros...")
        try:
            filtered_data = self.data_model.get_decisions(filters)
            self.decisions_grid.update_data(filtered_data)
            count = len(filtered_data)
            self.status_bar.config(text=f"{count} decisões encontradas")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aplicar filtros: {e}")
            self.status_bar.config(text="Erro nos filtros")
    
    def on_decision_selected(self, decision_data: Dict):
        """Callback quando uma decisão é selecionada no grid"""
        if not decision_data:
            return
        
        try:
            # Atualizar painel de detalhes
            self.details_panel.update_decision(decision_data)
            
            # Carregar e exibir curva de payoff
            aba = decision_data.get('aba')
            timestamp = decision_data.get('timestamp')
            
            if aba and timestamp:
                payoff_points = self.data_model.get_payoff_curve(aba, timestamp)
                self.payoff_chart.update_chart(payoff_points, decision_data)
                
                self.status_bar.config(
                    text=f"Carregado: {aba} - {decision_data.get('decision', 'N/A')}"
                )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar detalhes: {e}")
    
    # === AÇÕES DOS MENUS ===
    
    def refresh_data(self):
        """Recarrega dados do banco"""
        self.status_bar.config(text="Carregando dados...")
        try:
            self.data_model.refresh()

            # NOVO: atualizar lista de abas no filtro
            self.filters_panel.update_abas(self.data_model.get_abas())
            
            # Resetar filtros e recarregar grid
            self.filters_panel.reset_filters()
            decisions = self.data_model.get_decisions()
            self.decisions_grid.update_data(decisions)
            
            # Limpar painéis de detalhes
            self.details_panel.clear()
            self.payoff_chart.clear()
            
            count = len(decisions)
            self.status_bar.config(text=f"Dados atualizados - {count} decisões")
            
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
            self.status_bar.config(text="Erro ao carregar dados")
    
    def export_csv(self):
        """Exporta dados filtrados para CSV"""
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            try:
                current_data = self.decisions_grid.get_current_data()
                self.data_model.export_to_csv(current_data, filename)
                messagebox.showinfo("Sucesso", f"Dados exportados para {filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar: {e}")
    
    def run_pipeline(self):
        """Executa pipeline de derivados"""
        import subprocess
        import os
        
        result = messagebox.askyesno(
            "Executar Pipeline",
            "Executar pipeline de derivados?\nIsso pode demorar alguns segundos."
        )
        
        if result:
            self.status_bar.config(text="Executando pipeline...")
            try:
                # Executar pipeline
                script_path = Path("Scripts/run_derived_pipeline.py")
                subprocess.run([
                    "python", str(script_path)
                ], check=True, capture_output=True, text=True)
                
                messagebox.showinfo("Sucesso", "Pipeline executado com sucesso!")
                self.refresh_data()
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Erro", f"Pipeline falhou:\n{e.stderr}")
                self.status_bar.config(text="Pipeline falhou")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao executar pipeline: {e}")
    
    def check_databases(self):
        """Verifica status dos bancos de dados"""
        try:
            status = self.data_model.check_database_status()
            messagebox.showinfo("Status dos Bancos", status)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar bancos: {e}")
    
    def clear_cache(self):
        """Limpa cache interno"""
        self.data_model.clear_cache()
        messagebox.showinfo("Cache", "Cache limpo com sucesso")
    
    def show_about(self):
        """Mostra informações sobre o sistema"""
        about_text = """Sistema de Derivados v1.0
        
Desenvolvido para análise de estruturas de opções
Pipeline automático de payoff e decisões

Camadas:
• Excel RTD → CSV Bridge
• Ingest Python → app.db
• Domain Layer → derived.db  
• UI Tkinter (esta interface)

Baseline: executed_v1 + baseline_v1b"""
        
        messagebox.showinfo("Sobre", about_text)
    
    def run(self):
        """Inicia a aplicação"""
        self.root.mainloop()


def main():
    """Entry point da UI"""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
