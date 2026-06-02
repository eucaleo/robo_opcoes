# UI/components/structure_editor_dialog.py
"""
StructureEditorDialog — patch_10 / Fase 5
Dialog modal para criar / editar uma estrutura com suas legs.

Contrato com main_window.py:
    dlg = StructureEditorDialog(
        parent,
        structure_id: int | None,   # None → nova estrutura
        db_path: str,
    )
    root.wait_window(dlg)
    if dlg.saved: ...               # True se o usuário clicou Salvar com sucesso

Atributos públicos esperados pelos testes de integração:
    saved           bool
    _f_name         tk.StringVar
    _f_underlying   tk.StringVar
    _cmd_save()     método que executa a lógica de salvar
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

from repositories.structures_repository import StructuresRepository


# ─────────────────────────────────────────────────────────────────────────────
class StructureEditorDialog(tk.Toplevel):
    """Dialog modal de criação / edição de estrutura."""

    def __init__(
        self,
        parent: tk.Widget,
        structure_id: Optional[int],
        db_path: str,
    ):
        super().__init__(parent)

        self._repo         = StructuresRepository(db_path)
        self._structure_id = structure_id
        self.saved         = False

        self._legs_rows: list[dict] = []   # lista de dicts de legs em edição

        self._build_ui()

        if structure_id is not None:
            self._load_existing(structure_id)

        # Comportamento modal
        self.transient(parent)
        self.grab_set()
        self.resizable(True, True)
        self.minsize(640, 480)

    # ─────────────────────────────────────────────────────────────────
    # Construção da UI
    # ─────────────────────────────────────────────────────────────────

    def _build_ui(self):
        title = "Nova Estrutura" if self._structure_id is None else "Editar Estrutura"
        self.title(title)

        # ── Cabeçalho ──────────────────────────────────────────────
        hdr = ttk.LabelFrame(self, text="Dados Gerais", padding=8)
        hdr.pack(fill="x", padx=8, pady=(8, 4))

        self._f_name       = tk.StringVar()
        self._f_underlying = tk.StringVar()
        self._f_alias      = tk.StringVar()
        self._f_status     = tk.StringVar(value="active")
        self._f_notes      = tk.StringVar()

        fields = [
            ("Nome *",         self._f_name,       "entry",    None),
            ("Ativo *",        self._f_underlying, "entry",    None),
            ("Aba / Alias",    self._f_alias,      "entry",    None),
            ("Status",         self._f_status,     "combo",    ["active", "archived"]),
            ("Observações",    self._f_notes,      "entry",    None),
        ]

        for row_idx, (label, var, widget_type, opts) in enumerate(fields):
            ttk.Label(hdr, text=label, anchor="e", width=14).grid(
                row=row_idx, column=0, sticky="e", padx=(0, 6), pady=2
            )
            if widget_type == "combo":
                w = ttk.Combobox(hdr, textvariable=var, values=opts,
                                 state="readonly", width=14)
            else:
                w = ttk.Entry(hdr, textvariable=var, width=40)
            w.grid(row=row_idx, column=1, sticky="ew", pady=2)

        hdr.columnconfigure(1, weight=1)

        # ── Legs ───────────────────────────────────────────────────
        legs_outer = ttk.LabelFrame(self, text="Legs", padding=8)
        legs_outer.pack(fill="both", expand=True, padx=8, pady=4)

        # Toolbar de legs
        leg_toolbar = ttk.Frame(legs_outer)
        leg_toolbar.pack(fill="x", pady=(0, 4))
        ttk.Button(leg_toolbar, text="+ Leg",    command=self._cmd_add_leg).pack(side="left", padx=2)
        ttk.Button(leg_toolbar, text="✕ Remover", command=self._cmd_remove_leg).pack(side="left", padx=2)
        ttk.Button(leg_toolbar, text="↑",         command=lambda: self._cmd_move_leg(-1)).pack(side="left", padx=1)
        ttk.Button(leg_toolbar, text="↓",         command=lambda: self._cmd_move_leg(+1)).pack(side="left", padx=1)

        # Treeview de legs
        leg_frame = ttk.Frame(legs_outer)
        leg_frame.pack(fill="both", expand=True)

        leg_cols = ("order", "side", "type", "strike", "expiry", "qty", "premium", "mult", "symbol")
        leg_hdrs = ["#", "Lado", "Tipo", "Strike", "Vencimento", "Qtde", "Prêmio", "Mult", "Símbolo"]
        leg_widths = [30, 60, 55, 80, 100, 55, 70, 50, 90]

        self._leg_tree = ttk.Treeview(
            leg_frame,
            columns=leg_cols,
            show="headings",
            height=6,
            selectmode="browse",
        )
        for col, hdr_text, w in zip(leg_cols, leg_hdrs, leg_widths):
            self._leg_tree.heading(col, text=hdr_text)
            self._leg_tree.column(col, width=w, anchor=tk.CENTER, stretch=(col == "expiry"))

        leg_vsb = ttk.Scrollbar(leg_frame, orient="vertical", command=self._leg_tree.yview)
        self._leg_tree.configure(yscrollcommand=leg_vsb.set)
        leg_vsb.pack(side="right", fill="y")
        self._leg_tree.pack(fill="both", expand=True)
        self._leg_tree.bind("<Double-1>", self._on_leg_double_click)

        # Formulário inline de edição de leg
        self._build_leg_form(legs_outer)

        # ── Botões de ação ─────────────────────────────────────────
        btn_bar = ttk.Frame(self)
        btn_bar.pack(fill="x", padx=8, pady=8)

        ttk.Button(btn_bar, text="Cancelar", command=self.destroy).pack(side="right", padx=4)
        ttk.Button(btn_bar, text="💾 Salvar",  command=self._cmd_save).pack(side="right", padx=4)

    def _build_leg_form(self, parent: tk.Widget):
        """Formulário colapsável para editar/adicionar uma leg."""
        form = ttk.LabelFrame(parent, text="Editar Leg", padding=6)
        form.pack(fill="x", pady=(6, 0))

        self._lf_side    = tk.StringVar(value="LONG")
        self._lf_type    = tk.StringVar(value="CALL")
        self._lf_strike  = tk.StringVar()
        self._lf_expiry  = tk.StringVar()
        self._lf_qty     = tk.StringVar(value="1")
        self._lf_premium = tk.StringVar()
        self._lf_mult    = tk.StringVar(value="1")
        self._lf_symbol  = tk.StringVar()

        # Linha 1
        r1 = ttk.Frame(form)
        r1.pack(fill="x", pady=1)
        for label, var, opts in [
            ("Lado",   self._lf_side,   ["LONG", "SHORT"]),
            ("Tipo",   self._lf_type,   ["CALL", "PUT"]),
        ]:
            ttk.Label(r1, text=label + ":").pack(side="left")
            ttk.Combobox(r1, textvariable=var, values=opts,
                         state="readonly", width=8).pack(side="left", padx=(0, 8))

        for label, var in [
            ("Strike",  self._lf_strike),
            ("Venc (YYYY-MM-DD)", self._lf_expiry),
        ]:
            ttk.Label(r1, text=label + ":").pack(side="left")
            ttk.Entry(r1, textvariable=var, width=13).pack(side="left", padx=(0, 8))

        # Linha 2
        r2 = ttk.Frame(form)
        r2.pack(fill="x", pady=1)
        for label, var in [
            ("Qtde",    self._lf_qty),
            ("Prêmio",  self._lf_premium),
            ("Mult",    self._lf_mult),
            ("Símbolo", self._lf_symbol),
        ]:
            ttk.Label(r2, text=label + ":").pack(side="left")
            ttk.Entry(r2, textvariable=var, width=10).pack(side="left", padx=(0, 8))

        # Botão aplicar
        ttk.Button(form, text="✔ Aplicar Leg", command=self._cmd_apply_leg).pack(
            anchor="e", pady=(4, 0)
        )

    # ─────────────────────────────────────────────────────────────────
    # Carregar estrutura existente
    # ─────────────────────────────────────────────────────────────────

    def _load_existing(self, structure_id: int):
        data = self._repo.get_structure(structure_id)
        if data is None:
            messagebox.showerror("Erro", f"Estrutura {structure_id} não encontrada.")
            self.destroy()
            return

        self._f_name.set(data.get("name", ""))
        self._f_underlying.set(data.get("underlying_asset", ""))
        self._f_alias.set(data.get("alias_legacy_aba") or "")
        self._f_status.set(data.get("status", "active"))
        self._f_notes.set(data.get("notes") or "")

        self._legs_rows = list(data.get("legs", []))
        self._refresh_leg_tree()

    # ─────────────────────────────────────────────────────────────────
    # Renderização da leg tree
    # ─────────────────────────────────────────────────────────────────

    def _refresh_leg_tree(self):
        self._leg_tree.delete(*self._leg_tree.get_children())
        for i, leg in enumerate(self._legs_rows, 1):
            self._leg_tree.insert("", "end", iid=str(i - 1), values=(
                i,
                leg.get("position_side", ""),
                leg.get("option_type", ""),
                leg.get("strike", ""),
                leg.get("expiration_date", ""),
                leg.get("quantity", ""),
                leg.get("premium") or "",
                leg.get("multiplier", 1),
                leg.get("symbol") or "",
            ))

    def _selected_leg_index(self) -> Optional[int]:
        sel = self._leg_tree.selection()
        if not sel:
            return None
        try:
            return int(sel[0])
        except (ValueError, TypeError):
            return None

    # ─────────────────────────────────────────────────────────────────
    # Callbacks de legs
    # ─────────────────────────────────────────────────────────────────

    def _on_leg_double_click(self, _event=None):
        """Popula o formulário com a leg duplo-clicada."""
        idx = self._selected_leg_index()
        if idx is None:
            return
        leg = self._legs_rows[idx]
        self._lf_side.set(leg.get("position_side", "LONG"))
        self._lf_type.set(leg.get("option_type", "CALL"))
        self._lf_strike.set(str(leg.get("strike", "")))
        self._lf_expiry.set(str(leg.get("expiration_date", "")))
        self._lf_qty.set(str(leg.get("quantity", "1")))
        self._lf_premium.set(str(leg.get("premium") or ""))
        self._lf_mult.set(str(leg.get("multiplier", 1)))
        self._lf_symbol.set(str(leg.get("symbol") or ""))

    def _cmd_add_leg(self):
        """Adiciona uma leg nova em branco e seleciona para edição."""
        new_leg = {
            "position_side":   "LONG",
            "option_type":     "CALL",
            "strike":          "",
            "expiration_date": "",
            "quantity":        1,
            "premium":         None,
            "multiplier":      1.0,
            "leg_order":       len(self._legs_rows) + 1,
            "symbol":          None,
            "notes":           None,
        }
        self._legs_rows.append(new_leg)
        self._refresh_leg_tree()
        # Seleciona o novo item
        new_iid = str(len(self._legs_rows) - 1)
        self._leg_tree.selection_set(new_iid)
        self._on_leg_double_click()

    def _cmd_remove_leg(self):
        idx = self._selected_leg_index()
        if idx is None:
            messagebox.showwarning("Remover Leg", "Selecione uma leg primeiro.")
            return
        self._legs_rows.pop(idx)
        self._refresh_leg_tree()

    def _cmd_move_leg(self, direction: int):
        idx = self._selected_leg_index()
        if idx is None:
            return
        new_idx = idx + direction
        if new_idx < 0 or new_idx >= len(self._legs_rows):
            return
        self._legs_rows[idx], self._legs_rows[new_idx] = (
            self._legs_rows[new_idx],
            self._legs_rows[idx],
        )
        self._refresh_leg_tree()
        self._leg_tree.selection_set(str(new_idx))

    def _cmd_apply_leg(self):
        """Aplica os valores do formulário na leg selecionada."""
        idx = self._selected_leg_index()
        if idx is None:
            messagebox.showwarning("Aplicar Leg", "Selecione uma leg na lista primeiro.")
            return

        self._legs_rows[idx] = {
            "position_side":   self._lf_side.get(),
            "option_type":     self._lf_type.get(),
            "strike":          self._lf_strike.get(),
            "expiration_date": self._lf_expiry.get(),
            "quantity":        self._lf_qty.get(),
            "premium":         self._lf_premium.get() or None,
            "multiplier":      self._lf_mult.get() or 1,
            "leg_order":       idx + 1,
            "symbol":          self._lf_symbol.get() or None,
            "notes":           None,
        }
        self._refresh_leg_tree()

    # ─────────────────────────────────────────────────────────────────
    # Salvar
    # ─────────────────────────────────────────────────────────────────

    def _cmd_save(self):
        name       = self._f_name.get().strip()
        underlying = self._f_underlying.get().strip()

        if not name:
            messagebox.showwarning("Salvar", "O campo 'Nome' é obrigatório.")
            return
        if not underlying:
            messagebox.showwarning("Salvar", "O campo 'Ativo' é obrigatório.")
            return

        structure_data = {
            "name":             name,
            "underlying_asset": underlying,
            "alias_legacy_aba": self._f_alias.get().strip() or None,
            "status":           self._f_status.get(),
            "notes":            self._f_notes.get().strip() or None,
        }

        # Prepara legs com leg_order atualizado
        legs_payload = []
        for i, leg in enumerate(self._legs_rows, 1):
            legs_payload.append({**leg, "leg_order": i})

        try:
            if self._structure_id is None:
                sid = self._repo.create_structure(structure_data)
            else:
                sid = self._structure_id
                self._repo.update_structure(sid, structure_data)

            if legs_payload:
                self._repo.replace_legs(sid, legs_payload)
            else:
                self._repo.replace_legs(sid, [])

            self.saved = True
            self.destroy()

        except ValueError as exc:
            messagebox.showerror("Erro de Validação", str(exc))
        except Exception as exc:
            messagebox.showerror("Erro", f"Falha ao salvar: {exc}")
