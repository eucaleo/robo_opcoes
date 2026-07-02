# Inventário focado da exportação PNG

Data de referência: 2026-07-02

Objetivo:

- localizar pontos reais de exportação PNG na UI;
- reduzir ruído do inventário amplo;
- identificar arquivo alvo para patch pequeno;
- não alterar código funcional nesta rodada.

## Escopo pesquisado

- UI
- ui
- app não encontrado
- components não encontrado
- services
- domain

## Padrões pesquisados

- savefig
- asksaveasfilename
- filedialog
- FigureCanvasTkAgg
- FigureCanvas
- NavigationToolbar2Tk
- class PayoffChart
- def export
- def salvar
- exportar
- png
- imagem

## Resumo por arquivo

| Arquivo | Ocorrências |
|---|---:|
| UI/components/payoff_chart.py | 13 |
| UI/components/terminal_vwap_payoff_dark_panel.py | 5 |
| UI/main_window.py | 6 |
| UI/models/ui_data.py | 1 |
| UI/modern/main_window.py | 6 |
| ui/components/payoff_chart.py | 13 |
| ui/components/terminal_vwap_payoff_dark_panel.py | 5 |
| ui/main_window.py | 6 |
| ui/models/ui_data.py | 1 |
| ui/modern/main_window.py | 6 |

## Ocorrências focadas

| Arquivo | Linha | Padrões | Trecho |
|---|---:|---|---|
| UI/components/payoff_chart.py | 6 | FigureCanvasTkAgg, FigureCanvas, NavigationToolbar2Tk | from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk |
| UI/components/payoff_chart.py | 9 | filedialog | from tkinter import filedialog, messagebox |
| UI/components/payoff_chart.py | 55 | class PayoffChart | class PayoffChart(ttk.Frame): |
| UI/components/payoff_chart.py | 81 | exportar, png | top, text="Exportar PNG", command=self.export_png |
| UI/components/payoff_chart.py | 99 | FigureCanvasTkAgg, FigureCanvas | self.canvas = FigureCanvasTkAgg(self.fig, master=self) |
| UI/components/payoff_chart.py | 103 | NavigationToolbar2Tk | self.toolbar = NavigationToolbar2Tk(self.canvas, top, pack_toolbar=False) |
| UI/components/payoff_chart.py | 221 | def export, png | def export_png(self): |
| UI/components/payoff_chart.py | 222 | png | """Exporta o gráfico atual para PNG.""" |
| UI/components/payoff_chart.py | 223 | asksaveasfilename, filedialog | file_path = filedialog.asksaveasfilename( |
| UI/components/payoff_chart.py | 224 | png | defaultextension=".png", |
| UI/components/payoff_chart.py | 225 | png | filetypes=[("PNG", "*.png"), ("All files", "*.*")], |
| UI/components/payoff_chart.py | 226 | exportar, png | title="Exportar gráfico como PNG", |
| UI/components/payoff_chart.py | 231 | savefig | self.fig.savefig(file_path, dpi=150, bbox_inches="tight") |
| UI/components/terminal_vwap_payoff_dark_panel.py | 29 | FigureCanvasTkAgg, FigureCanvas | from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg |
| UI/components/terminal_vwap_payoff_dark_panel.py | 145 | FigureCanvasTkAgg, FigureCanvas | self.canvas_vwap: Optional[FigureCanvasTkAgg] = None |
| UI/components/terminal_vwap_payoff_dark_panel.py | 146 | FigureCanvasTkAgg, FigureCanvas | self.canvas_payoff: Optional[FigureCanvasTkAgg] = None |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1102 | FigureCanvasTkAgg, FigureCanvas | self.canvas_vwap = FigureCanvasTkAgg(fig, master=self.frame_vwap) |
| UI/components/terminal_vwap_payoff_dark_panel.py | 1138 | FigureCanvasTkAgg, FigureCanvas | self.canvas_payoff = FigureCanvasTkAgg(fig, master=self.frame_payoff) |
| UI/main_window.py | 21 | FigureCanvasTkAgg, FigureCanvas | # FigureCanvasTkAgg importado lazily em _setup_chart para evitar side-effects no import |
| UI/main_window.py | 136 | exportar | file_menu.add_command(label="Exportar CSV...", command=self.export_csv) |
| UI/main_window.py | 339 | def export | def export_csv(self): |
| UI/main_window.py | 341 | filedialog | from tkinter import filedialog |
| UI/main_window.py | 343 | asksaveasfilename, filedialog | filename = filedialog.asksaveasfilename( |
| UI/main_window.py | 353 | exportar | messagebox.showerror("Erro", f"Erro ao exportar: {e}") |
| UI/models/ui_data.py | 600 | def export | def export_to_csv(self, data: List[Dict], filename: str): |
| UI/modern/main_window.py | 17 | filedialog | from tkinter import filedialog, messagebox, ttk |
| UI/modern/main_window.py | 160 | exportar | self._side_button(sidebar, "Exportar CSV", self.export_csv) |
| UI/modern/main_window.py | 557 | def export | def export_csv(self) -> None: |
| UI/modern/main_window.py | 558 | asksaveasfilename, filedialog | filename = filedialog.asksaveasfilename( |
| UI/modern/main_window.py | 572 | exportar | messagebox.showerror("Erro", f"Erro ao exportar: {exc}") |
| UI/modern/main_window.py | 573 | exportar | self.set_status("Erro ao exportar CSV") |
| ui/components/payoff_chart.py | 6 | FigureCanvasTkAgg, FigureCanvas, NavigationToolbar2Tk | from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk |
| ui/components/payoff_chart.py | 9 | filedialog | from tkinter import filedialog, messagebox |
| ui/components/payoff_chart.py | 55 | class PayoffChart | class PayoffChart(ttk.Frame): |
| ui/components/payoff_chart.py | 81 | exportar, png | top, text="Exportar PNG", command=self.export_png |
| ui/components/payoff_chart.py | 99 | FigureCanvasTkAgg, FigureCanvas | self.canvas = FigureCanvasTkAgg(self.fig, master=self) |
| ui/components/payoff_chart.py | 103 | NavigationToolbar2Tk | self.toolbar = NavigationToolbar2Tk(self.canvas, top, pack_toolbar=False) |
| ui/components/payoff_chart.py | 221 | def export, png | def export_png(self): |
| ui/components/payoff_chart.py | 222 | png | """Exporta o gráfico atual para PNG.""" |
| ui/components/payoff_chart.py | 223 | asksaveasfilename, filedialog | file_path = filedialog.asksaveasfilename( |
| ui/components/payoff_chart.py | 224 | png | defaultextension=".png", |
| ui/components/payoff_chart.py | 225 | png | filetypes=[("PNG", "*.png"), ("All files", "*.*")], |
| ui/components/payoff_chart.py | 226 | exportar, png | title="Exportar gráfico como PNG", |
| ui/components/payoff_chart.py | 231 | savefig | self.fig.savefig(file_path, dpi=150, bbox_inches="tight") |
| ui/components/terminal_vwap_payoff_dark_panel.py | 29 | FigureCanvasTkAgg, FigureCanvas | from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg |
| ui/components/terminal_vwap_payoff_dark_panel.py | 145 | FigureCanvasTkAgg, FigureCanvas | self.canvas_vwap: Optional[FigureCanvasTkAgg] = None |
| ui/components/terminal_vwap_payoff_dark_panel.py | 146 | FigureCanvasTkAgg, FigureCanvas | self.canvas_payoff: Optional[FigureCanvasTkAgg] = None |
| ui/components/terminal_vwap_payoff_dark_panel.py | 1102 | FigureCanvasTkAgg, FigureCanvas | self.canvas_vwap = FigureCanvasTkAgg(fig, master=self.frame_vwap) |
| ui/components/terminal_vwap_payoff_dark_panel.py | 1138 | FigureCanvasTkAgg, FigureCanvas | self.canvas_payoff = FigureCanvasTkAgg(fig, master=self.frame_payoff) |
| ui/main_window.py | 21 | FigureCanvasTkAgg, FigureCanvas | # FigureCanvasTkAgg importado lazily em _setup_chart para evitar side-effects no import |
| ui/main_window.py | 136 | exportar | file_menu.add_command(label="Exportar CSV...", command=self.export_csv) |
| ui/main_window.py | 339 | def export | def export_csv(self): |
| ui/main_window.py | 341 | filedialog | from tkinter import filedialog |
| ui/main_window.py | 343 | asksaveasfilename, filedialog | filename = filedialog.asksaveasfilename( |
| ui/main_window.py | 353 | exportar | messagebox.showerror("Erro", f"Erro ao exportar: {e}") |
| ui/models/ui_data.py | 600 | def export | def export_to_csv(self, data: List[Dict], filename: str): |
| ui/modern/main_window.py | 17 | filedialog | from tkinter import filedialog, messagebox, ttk |
| ui/modern/main_window.py | 160 | exportar | self._side_button(sidebar, "Exportar CSV", self.export_csv) |
| ui/modern/main_window.py | 557 | def export | def export_csv(self) -> None: |
| ui/modern/main_window.py | 558 | asksaveasfilename, filedialog | filename = filedialog.asksaveasfilename( |
| ui/modern/main_window.py | 572 | exportar | messagebox.showerror("Erro", f"Erro ao exportar: {exc}") |
| ui/modern/main_window.py | 573 | exportar | self.set_status("Erro ao exportar CSV") |

## Leitura esperada

- Se UI/components/payoff_chart.py aparecer com FigureCanvasTkAgg, ele provavelmente é o alvo de exportação.
- Se já existir savefig, o patch deve reaproveitar essa implementação.
- Se não existir savefig, o patch mínimo deve exportar a figura do gráfico atual.
- A implementação futura deve preservar banco, contratos canônicos e regras de negócio.

## Decisão pendente

- Definir o arquivo alvo.
- Definir o método de exportação.
- Definir o botão ou ação de UI.
- Definir mensagens de sucesso, cancelamento e erro.
