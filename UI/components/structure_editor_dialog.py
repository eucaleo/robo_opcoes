# UI/components/structure_editor_dialog.py
"""
StructureEditorDialog -- alteracao_10 / Fase 5
Dialog modal para criar / editar uma estrutura com suas legs.

Contrato com main_window.py:
    dlg = StructureEditorDialog(
        parent,
        structure_id: int | None,   # None -> nova estrutura
        db_path: str,
    )
    root.wait_window(dlg)
    if dlg.saved: ...               # True se o usuario clicou Salvar com sucesso

Atributos publicos esperados pelos testes de integracao:
    saved           bool
    _f_name         tk.StringVar
    _f_underlying   tk.StringVar
    _f_alias        tk.StringVar
    _f_status       tk.StringVar
    _f_notes        tk.StringVar
    _legs_rows      list[dict]
    _structure_id   int | None
    _repo           StructuresRepository
    _cmd_save()     metodo que executa a logica de salvar
    _load_existing()       sem argumento -- usa self._structure_id
    _build_legs_payload()  logica pura, testavel sem display
    _build_ui()     constroi todos os widgets
    _add_leg_row()  alias publico de _cmd_add_leg (exigido por checks estaticos)
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

from repositories.structures_repository import StructuresRepository


class StructureEditorDialog(tk.Toplevel):
    """Dialog modal de criacao / edicao de estrutura."""

    def __init__(
        self,
        parent: tk.Widget,
        structure_id: Optional[int] = None,
        db_path: str = "dados/app.db",
        *,
        _repo=None,                          # <-- injecao de dependencia (testes)
    ):
        super().__init__(parent)

        self._structure_id = structure_id
        self._db_path      = db_path
        self.saved         = False
        self._legs_rows: list[dict] = []

        # Injeta repositorio mockado em testes, ou cria o real em producao
        if _repo is not None:
            self._repo = _repo
        else:
            self._repo = StructuresRepository(db_path)

        # Variaveis de formulario -- inicializadas ANTES de _build_ui
        # para que _load_existing() possa fazer .set() mesmo se chamado
        # antes do mainloop (cenario de teste headless via object.__new__)
        self._f_name       = tk.StringVar()
        self._f_underlying = tk.StringVar()
        self._f_alias      = tk.StringVar()
        self._f_status     = tk.StringVar(value="active")
        self._f_notes      = tk.StringVar()

        self._build_ui()

        if structure_id is not None:
            self._load_existing()

        # Comportamento modal
        self.transient(parent)
        self.grab_set()
        self.resizable(True, True)
        self.minsize(640, 480)

    # ------------------------------------------------------------------
    # Construcao da UI
    # ------------------------------------------------------------------

    def _build_ui(self):
        title = "Nova Estrutura" if self._structure_id is None else "Editar Estrutura"
        self.title(title)

        # === Cabecalho ===
        hdr = ttk.LabelFrame(self, text="Dados Gerais", padding=8)
        hdr.pack(fill="x", padx=8, pady=(8, 4))

        fields = [
            ("Nome *",         self._f_name,       "entry", None),
            ("Ativo *",        self._f_underlying, "entry", None),
            ("Aba / Alias",    self._f_alias,      "entry", None),
            ("Status",         self._f_status,     "combo", ["active", "archived"]),
            ("Observacoes",    self._f_notes,      "entry", None),
        ]

        for row_idx, (label, var, widget_type, opts) in enumerate(fields):
            ttk.Label(hdr, text=label, anchor="e", width=14).grid(
                row=row_idx, column=0, sticky="e", padx=(0, 6), pady=2
            )
            if widget_type == "combo":
                w = ttk.Combobox(
                    hdr, textvariable=var, values=opts,
                    state="readonly", width=14,
                )
            else:
                w = ttk.Entry(hdr, textvariable=var, width=40)
            w.grid(row=row_idx, column=1, sticky="ew", pady=2)

        hdr.columnconfigure(1, weight=1)

        # === Legs ===
        legs_outer = ttk.LabelFrame(self, text="Legs", padding=8)
        legs_outer.pack(fill="both", expand=True, padx=8, pady=4)

        # Toolbar de legs
        leg_toolbar = ttk.Frame(legs_outer)
        leg_toolbar.pack(fill="x", pady=(0, 4))
        ttk.Button(leg_toolbar, text="+ Leg",    command=self._cmd_add_leg).pack(side="left", padx=2)
        ttk.Button(leg_toolbar, text="Remover",  command=self._cmd_remove_leg).pack(side="left", padx=2)
        ttk.Button(leg_toolbar, text="▲",        command=lambda: self._cmd_move_leg(-1)).pack(side="left", padx=1)
        ttk.Button(leg_toolbar, text="▼",        command=lambda: self._cmd_move_leg(+1)).pack(side="left", padx=1)

        # Treeview de legs
        leg_frame = ttk.Frame(legs_outer)
        leg_frame.pack(fill="both", expand=True)

        leg_cols   = ("order", "side", "type", "strike", "expiry", "qty", "premium", "mult", "symbol")
        leg_hdrs   = ["#", "Lado", "Tipo", "Strike", "Vencimento", "Qtde", "Premio", "Mult", "Simbolo"]
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

        # Formulario inline de edicao de leg
        self._build_leg_form(legs_outer)

        # === Botoes de acao ===
        btn_bar = ttk.Frame(self)
        btn_bar.pack(fill="x", padx=8, pady=8)

        ttk.Button(btn_bar, text="Cancelar",      command=self.destroy).pack(side="right", padx=4)
        ttk.Button(btn_bar, text="[SAVE] Salvar", command=self._cmd_save).pack(side="right", padx=4)

    def _build_leg_form(self, parent: tk.Widget):
        """Formulario colapsavel para editar / adicionar uma leg."""
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
            ("Lado",  self._lf_side, ["LONG", "SHORT"]),
            ("Tipo",  self._lf_type, ["CALL", "PUT"]),
        ]:
            ttk.Label(r1, text=label + ":").pack(side="left")
            ttk.Combobox(
                r1, textvariable=var, values=opts,
                state="readonly", width=8,
            ).pack(side="left", padx=(0, 8))

        for label, var in [
            ("Strike",              self._lf_strike),
            ("Venc (YYYY-MM-DD)",   self._lf_expiry),
        ]:
            ttk.Label(r1, text=label + ":").pack(side="left")
            ttk.Entry(r1, textvariable=var, width=13).pack(side="left", padx=(0, 8))

        # Linha 2
        r2 = ttk.Frame(form)
        r2.pack(fill="x", pady=1)
        for label, var in [
            ("Qtde",    self._lf_qty),
            ("Premio",  self._lf_premium),
            ("Mult",    self._lf_mult),
            ("Simbolo", self._lf_symbol),
        ]:
            ttk.Label(r2, text=label + ":").pack(side="left")
            ttk.Entry(r2, textvariable=var, width=10).pack(side="left", padx=(0, 8))

        # Botao aplicar
        ttk.Button(form, text="[v] Aplicar Leg", command=self._cmd_apply_leg).pack(
            anchor="e", pady=(4, 0)
        )

    # ------------------------------------------------------------------
    # Carregar estrutura existente
    # ------------------------------------------------------------------

    def _load_existing(self):
        """
        Carrega campos e legs de uma estrutura existente via repositorio.
        Usa self._structure_id (nao recebe argumento -- compativel com testes
        que chamam dlg._load_existing() sem parametros).
        """
        data = self._repo.get_structure(self._structure_id)
        if data is None:
            messagebox.showerror(
                "Erro",
                f"Estrutura {self._structure_id} nao encontrada.",
                parent=self,
            )
            self.destroy()
            return

        self._f_name.set(data.get("name", ""))
        self._f_underlying.set(data.get("underlying_asset", ""))
        self._f_alias.set(data.get("alias_legacy_aba") or "")
        self._f_status.set(data.get("status", "active"))
        self._f_notes.set(data.get("notes") or "")

        self._legs_rows = list(data.get("legs", []))
        self._refresh_leg_tree()

    # ------------------------------------------------------------------
    # Renderizacao da leg tree
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Callbacks de legs
    # ------------------------------------------------------------------

    def _on_leg_double_click(self, _event=None):
        """Popula o formulario com a leg duplo-clicada."""
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
        """Adiciona uma leg nova em branco e seleciona para edicao."""
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
        new_iid = str(len(self._legs_rows) - 1)
        self._leg_tree.selection_set(new_iid)
        self._on_leg_double_click()

    # ------------------------------------------------------------------
    # _add_leg_row: alias publico exigido pelos checks estaticos do alteracao_69
    # Delega para _cmd_add_leg mantendo compatibilidade total.
    # ------------------------------------------------------------------
    def _add_leg_row(self):
        """
        Alias publico de _cmd_add_leg().
        Exigido por test_classe_presente (alteracao_69) que verifica:
            hasattr(StructureEditorDialog, '_add_leg_row')
        """
        self._cmd_add_leg()

    def _cmd_remove_leg(self):
        idx = self._selected_leg_index()
        if idx is None:
            messagebox.showwarning("Remover Leg", "Selecione uma leg primeiro.", parent=self)
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
        """Aplica os valores do formulario na leg selecionada."""
        idx = self._selected_leg_index()
        if idx is None:
            messagebox.showwarning(
                "Aplicar Leg", "Selecione uma leg na lista primeiro.", parent=self
            )
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

    # ------------------------------------------------------------------
    # Logica de payload (pura -- testavel sem display)
    # ------------------------------------------------------------------

    def _build_legs_payload(self) -> list[dict]:
        """
        Constroi lista de legs com leg_order sequencial a partir de 1.

        Logica pura: nao modifica _legs_rows nem acessa Tk.
        Testavel sem display (TestBuildLegsPayload no alteracao_69).
        """
        return [
            {**leg, "leg_order": i}
            for i, leg in enumerate(self._legs_rows, 1)
        ]

    # ------------------------------------------------------------------
    # Salvar
    # ------------------------------------------------------------------

    def _cmd_save(self):
        name       = self._f_name.get().strip()
        underlying = self._f_underlying.get().strip()

        if not name:
            messagebox.showwarning("Salvar", "O campo 'Nome' e obrigatorio.", parent=self)
            return
        if not underlying:
            messagebox.showwarning("Salvar", "O campo 'Ativo' e obrigatorio.", parent=self)
            return

        structure_data = {
            "name":             name,
            "underlying_asset": underlying,
            "alias_legacy_aba": self._f_alias.get().strip() or None,
            "status":           self._f_status.get(),
            "notes":            self._f_notes.get().strip() or None,
        }

        legs_payload = self._build_legs_payload()

        try:
            if self._structure_id is None:
                # --- Modo criacao ---
                sid = self._repo.create_structure_with_legs(
                    structure_data,
                    legs_payload,
                )
            else:
                # --- Modo edicao ---
                sid = self._structure_id
                self._repo.update_structure(sid, structure_data)
                self._repo.replace_legs(sid, legs_payload)

            self.saved = True
            self.destroy()

        except ValueError as exc:
            messagebox.showerror("Erro de Validacao", str(exc), parent=self)
        except Exception as exc:
            messagebox.showerror("Erro", f"Falha ao salvar: {exc}", parent=self)
