import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import ttk, messagebox

from db.config import connect_derived
from db.derived_repo import ensure_derived_tables


def init_derived_db():
    conn = connect_derived()
    try:
        ensure_derived_tables(conn)
    finally:
        conn.close()


def fetch_payoff_samples(limit: int = 500):
    conn = connect_derived()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT aba, timestamp, point_spot, point_pl
            FROM payoff_curve_points
            ORDER BY timestamp DESC, aba, point_spot
            LIMIT ?
            """,
            (limit,),
        )
        rows = cur.fetchall()
        return [
            {"aba": r[0], "timestamp": r[1], "point_spot": r[2], "point_pl": r[3]}
            for r in rows
        ]
    finally:
        conn.close()


def fetch_recent_decisions(limit: int = 200):
    conn = connect_derived()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
              aba, timestamp, decision,
              level, pl_atual, pl_max, pl_pct_of_max, dte_min
            FROM structure_decisions
            ORDER BY timestamp DESC, aba
            LIMIT ?
            """,
            (limit,),
        )
        rows = cur.fetchall()
        return [
            {
                "aba": r[0],
                "timestamp": r[1],
                "decision": r[2],
                "level": r[3],
                "pl_atual": r[4],
                "pl_max": r[5],
                "pl_pct_of_max": r[6],
                "dte_min": r[7],
            }
            for r in rows
        ]
    finally:
        conn.close()


# init
init_derived_db()

root = tk.Tk()
root.title("Derived Viewer (payoff + decisions)")

frm = ttk.Frame(root, padding=10)
frm.grid(sticky="nsew")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

txt = tk.Text(frm, width=110, height=28)
txt.grid(column=0, row=1, columnspan=2, padx=5, pady=5, sticky="nsew")

frm.grid_rowconfigure(1, weight=1)
frm.grid_columnconfigure(0, weight=1)
frm.grid_columnconfigure(1, weight=1)


def exibir_payoff():
    try:
        rows = fetch_payoff_samples()
        txt.delete("1.0", tk.END)
        if not rows:
            txt.insert(tk.END, "Nenhum payoff encontrado.\n")
            return
        for r in rows:
            txt.insert(
                tk.END,
                f"{r['timestamp']} | {r['aba']} | spot={r['point_spot']:.4f} | pl={r['point_pl']:.4f}\n",
            )
    except Exception as e:
        messagebox.showerror("Erro ao listar payoffs", str(e))


def exibir_decisions():
    try:
        rows = fetch_recent_decisions()
        txt.delete("1.0", tk.END)
        if not rows:
            txt.insert(tk.END, "Nenhuma decisão encontrada.\n")
            return
        for r in rows:
            txt.insert(
                tk.END,
                f"{r['timestamp']} | {r['aba']} | {r['decision']} | lvl={r['level']} | "
                f"pl_atual={r['pl_atual']} | pl_max={r['pl_max']} | pct={r['pl_pct_of_max']} | dte={r['dte_min']}\n"
            )
    except Exception as e:
        messagebox.showerror("Erro ao listar decisões", str(e))


ttk.Button(frm, text="Ver Payoff (amostra)", command=exibir_payoff).grid(column=0, row=0, padx=5, pady=5, sticky="w")
ttk.Button(frm, text="Ver Decisões (recentes)", command=exibir_decisions).grid(column=1, row=0, padx=5, pady=5, sticky="e")

root.mainloop()
