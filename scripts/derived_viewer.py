import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import ttk, messagebox

from services.derived_service import (
    get_connection,
    get_all_payoff_curves,
    get_recent_decisions,
)
from db.schema import ensure_derived_tables

# Cria/garante schema ao abrir o app
def init_app_db():
    conn = get_connection()
    ensure_derived_tables(conn)
    conn.close()

# Inicializa o banco ao abrir
init_app_db()

def exibir_payoff():
    try:
        payoffs = get_all_payoff_curves()
        txt.delete("1.0", tk.END)
        if not payoffs:
            txt.insert(tk.END, "Nenhum payoff encontrado.\n")
            return
        for p in payoffs[:500]:
            txt.insert(tk.END, f"{p}\n\n")
    except Exception as e:
        messagebox.showerror("Erro ao listar payoffs", str(e))

def exibir_decisions():
    try:
        decisions = get_recent_decisions()
        txt.delete("1.0", tk.END)
        if not decisions:
            txt.insert(tk.END, "Nenhuma decisão encontrada.\n")
            return
        for d in decisions[:200]:
            txt.insert(tk.END, f"{d}\n\n")
    except Exception as e:
        messagebox.showerror("Erro ao listar decisões", str(e))

root = tk.Tk()
root.title("Viewer: Payoff / Decisões")

frm = ttk.Frame(root, padding=10)
frm.grid()

ttk.Button(frm, text="Ver Payoffs", command=exibir_payoff).grid(column=0, row=0, padx=5, pady=5)
ttk.Button(frm, text="Ver Decisões", command=exibir_decisions).grid(column=1, row=0, padx=5, pady=5)

txt = tk.Text(frm, width=100, height=25)
txt.grid(column=0, row=1, columnspan=2, padx=5, pady=5)

root.mainloop()

