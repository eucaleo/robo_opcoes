# UI/components/structures_list_panel.py
"""
StructuresListPanel -- patch_10 / Fase 5
Lista de estruturas com filtro de status, botões CRUD e duplicar.

Contrato com main_window.py:
    StructuresListPanel(
        parent,
        on_structure_selected: Callable[[dict | None], None],
        on_request_edit:       Callable[[int | None], None],
        db_path:               str,
    )

Atributos públicos esperados pelos testes de integração:
    _tree           ttk.Treeview
    _status_var     tk.StringVar  ("active" | "all")
    load()          recarrega a lista do banco
"""
from __future__ import annotations


import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional

from repositories.structures_repository import StructuresRepository


# 
# Constantes de layout
# 
_COLUMNS = ("id", "name", "underlying_asset", "alias", "status", "legs")
_HEADERS = {
    "id":               ("ID",       45,  "center"),
    "name":             ("Nome",     220, "w"),
    "underlying_asset": ("Ativo",    80,  "center"),
    "alias":            ("Aba/Alias",110, "w"),
    "status":           ("Status",   70,  "center"),
    "legs":             ("Legs",     45,  "center"),
}


class StructuresListPanel(ttk.Frame):
    """Painel esquerdo da aba Estruturas."""

    def __init__(
        self,
        parent: tk.Widget,
        on_structure_selected: Callable[[Optional[dict]], None],
        on_request_edit: Callable[[Optional[int]], None],
        db_path: str,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)

        self._on_structure_selected = on_structure_selected
        self._on_request_edit       = on_request_edit
        self._db_path               = db_path
        self._repo                  = StructuresRepository(db_path)
        self._current_rows: list[dict] = []   # cache da última lista carregada

        self._build_toolbar()
        self._build_tree()
        self._build_buttons()

        self.load()

    # 
    # Construção da UI
    # 

    def _build_toolbar(self):
        """Barra superior: filtro de status + busca por nome."""
        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", padx=4, pady=(4, 0))

        ttk.Label(toolbar, text="Status:").pack(side="left")

        self._status_var = tk.StringVar(value="active")
        status_cb = ttk.Combobox(
            toolbar,
            textvariable=self._status_var,
            values=["active", "all"],
            state="readonly",
            width=8,
        )
        status_cb.pack(side="left", padx=(2, 10))
        status_cb.bind("<<ComboboxSelected>>", lambda _e: self.load())

        ttk.Label(toolbar, text="Busca:").pack(side="left")
        self._search_var = tk.StringVar()
        search_entry = ttk.Entry(toolbar, textvariable=self._search_var, width=18)
        search_entry.pack(side="left", padx=(2, 4))
        self._search_var.trace_add("write", lambda *_: self._apply_filter())

        ttk.Button(toolbar, text="", width=3,
                   command=self.load).pack(side="left")

    def _build_tree(self):
        """Treeview + scrollbar."""
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=4, pady=4)

        self._tree = ttk.Treeview(
            frame,
            columns=_COLUMNS,
            show="headings",
            selectmode="browse",
        )

        for col in _COLUMNS:
            header, width, anchor = _HEADERS[col]
            self._tree.heading(col, text=header,
                               command=lambda c=col: self._sort_by(c))
            self._tree.column(col, width=width, anchor=anchor, stretch=(col == "name"))

        vsb = ttk.Scrollbar(frame, orient="vertical",   command=self._tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self._tree.xview)
        self._tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side="right",  fill="y")
        hsb.pack(side="bottom", fill="x")
        self._tree.pack(fill="both", expand=True)

        self._tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        self._tree.bind("<Double-1>",         self._on_tree_double_click)

        # Tags de cor por status
        self._tree.tag_configure("archived", foreground="#999999")
        self._tree.tag_configure("active",   foreground="#1a1a1a")

    def _build_buttons(self):
        """Barra inferior com botões de ação."""
        btn_bar = ttk.Frame(self)
        btn_bar.pack(fill="x", padx=4, pady=(0, 4))

        actions = [
            ("+ Nova",     self._cmd_new),
            (" Editar",   self._cmd_edit),
            (" Duplicar", self._cmd_duplicate),
            (" Arquivar", self._cmd_archive),
        ]
        for label, cmd in actions:
            ttk.Button(btn_bar, text=label, command=cmd).pack(
                side="left", padx=2, pady=2
            )


        # Label de feedback de status no rodapé do painel
        self._status_label_var = tk.StringVar(value="")
        ttk.Label(
            self,
            textvariable=self._status_label_var,
            foreground="#555555",
            anchor="w",
        ).pack(fill="x", padx=4, pady=(0, 2))
    # 
    # Carregamento / filtro
    # 

    def load(self):
        """Recarrega do banco respeitando o filtro de status atual."""
        include_archived = self._status_var.get() == "all"
        self._current_rows = self._repo.list_structures(
            include_archived=include_archived
        )
        self._apply_filter()

    def _apply_filter(self):
        """Filtra _current_rows pelo texto de busca e re-renderiza a tree."""
        term = self._search_var.get().strip().lower()

        filtered = self._current_rows
        if term:
            filtered = [
                r for r in filtered
                if term in r.get("name", "").lower()
                or term in r.get("underlying_asset", "").lower()
                or term in (r.get("alias_legacy_aba") or "").lower()
            ]

        # Salva seleção atual (por id) para restaurar depois
        sel_id = self._selected_id()

        self._tree.delete(*self._tree.get_children())
        for row in filtered:
            n_legs = row.get("n_legs", 0)
            iid = str(row["id"])
            self._tree.insert(
                "", "end", iid=iid,
                values=(
                    row["id"],
                    row["name"],
                    row["underlying_asset"],
                    row.get("alias_legacy_aba") or "--",
                    row["status"],
                    n_legs if n_legs else "--",
                ),
                tags=(row["status"],),
            )

        # Restaura seleção se o item ainda existe
        if sel_id and self._tree.exists(str(sel_id)):
            self._tree.selection_set(str(sel_id))
            self._tree.see(str(sel_id))

    # 
    # Helpers internos
    # 

    def _selected_id(self) -> Optional[int]:
        sel = self._tree.selection()
        if not sel:
            return None
        try:
            return int(self._tree.item(sel[0])["values"][0])
        except (IndexError, ValueError, TypeError):
            return None

    def _get_full_structure(self, structure_id: int) -> Optional[dict]:
        """Busca estrutura completa (com legs) pelo repositório."""
        try:
            return self._repo.get_structure(structure_id)
        except Exception:
            return None

    def _sort_by(self, col: str):
        """Ordena a tree pela coluna clicada (toggle asc/desc)."""
        items = [(self._tree.set(iid, col), iid)
                 for iid in self._tree.get_children("")]
        reverse = getattr(self, f"_sort_rev_{col}", False)
        try:
            items.sort(key=lambda x: (x[0] == "--", x[0]), reverse=reverse)
        except TypeError:
            items.sort(key=lambda x: str(x[0]), reverse=reverse)
        for idx, (_, iid) in enumerate(items):
            self._tree.move(iid, "", idx)
        setattr(self, f"_sort_rev_{col}", not reverse)

    # 
    # Callbacks da Treeview
    # 

    def _on_tree_select(self, _event=None):
        sid = self._selected_id()
        if sid is None:
            self._on_structure_selected(None)
            return
        structure = self._get_full_structure(sid)
        self._on_structure_selected(structure)

    def _on_tree_double_click(self, _event=None):
        sid = self._selected_id()
        if sid is not None:
            self._on_request_edit(sid)

    # 
    # Comandos dos botões
    # 

    def _cmd_new(self):
        self._on_request_edit(None)

    def _cmd_edit(self):
        sid = self._selected_id()
        if sid is None:
            messagebox.showwarning("Editar", "Selecione uma estrutura primeiro.")
            return
        self._on_request_edit(sid)

    def _cmd_duplicate(self):
        sid = self._selected_id()
        if sid is None:
            messagebox.showwarning("Duplicar", "Selecione uma estrutura primeiro.")
            return

        src = self._get_full_structure(sid)
        if src is None:
            messagebox.showerror("Duplicar", "Não foi possível carregar a estrutura.")
            return

        try:
            new_id = self._repo.create_structure({
                "name":             f"{src['name']} (cópia)",
                "underlying_asset": src["underlying_asset"],
                "alias_legacy_aba": src.get("alias_legacy_aba"),
                "status":           "active",
                "notes":            src.get("notes"),
            })
            legs_copy = [
                {k: v for k, v in leg.items()
                 if k not in ("id", "structure_id", "created_at", "updated_at")}
                for leg in src.get("legs", [])
            ]
            if legs_copy:
                self._repo.replace_legs(new_id, legs_copy)

            self.load()

            # Seleciona o novo item
            if self._tree.exists(str(new_id)):
                self._tree.selection_set(str(new_id))
                self._tree.see(str(new_id))

        except Exception as exc:
            messagebox.showerror("Duplicar", f"Erro ao duplicar: {exc}")

    def _cmd_archive(self):
        sid = self._selected_id()
        if sid is None:
            messagebox.showwarning("Arquivar", "Selecione uma estrutura primeiro.")
            return

        src = self._get_full_structure(sid)
        if src and src.get("status") == "archived":
            messagebox.showinfo("Arquivar", "Esta estrutura já está arquivada.")
            return

        name = src["name"] if src else f"ID={sid}"
        if not messagebox.askyesno(
            "Arquivar",
            f"Arquivar '{name}'?\nA estrutura ficará oculta (não será deletada).",
        ):
            return

        try:
            self._repo.archive_structure(sid)
            self._on_structure_selected(None)
            self.load()
            self._set_status(f"Estrutura '{name}' arquivada.")
        except Exception as exc:
            messagebox.showerror("Arquivar", f"Erro ao arquivar: {exc}")
            self._set_status(f"Erro ao arquivar: {exc}")

    # 
    # Feedback de status
    # 

    def _set_status(self, msg: str) -> None:
        """Atualiza o label de feedback no rodapé do painel."""
        try:
            self._status_label_var.set(msg)
        except Exception:
            pass
