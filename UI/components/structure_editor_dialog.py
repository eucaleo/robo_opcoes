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
from repositories.rtd_option_quotes_repository import RtdOptionQuotesRepository
from services.structure_leg_rtd_enrichment_service import StructureLegRtdEnrichmentService
from domain.position_side import normalize_position_side


_STATUS_TO_LABEL = {
    "active": "Ativa",
    "archived": "Arquivada",
}

_LABEL_TO_STATUS = {
    label: status for status, label in _STATUS_TO_LABEL.items()
}


def _parse_decimal(value, field_name: str) -> float:
    if value is None:
        raise ValueError(f"{field_name} é obrigatório")

    if isinstance(value, str):
        value = value.strip()
        if not value:
            raise ValueError(f"{field_name} é obrigatório")

        if "," in value:
            value = value.replace(".", "").replace(",", ".")

    try:
        return float(value)
    except Exception as exc:
        raise ValueError(f"{field_name} deve ser numérico") from exc


class StructureEditorDialog(tk.Toplevel):
    """Dialog modal de criacao / edicao de estrutura."""

    def __init__(
        self,
        parent: tk.Widget,
        structure_id: Optional[int] = None,
        db_path: str = "dados/app.db",
        *,
        _repo=None,                          # <-- injecao de dependencia (testes)
        _leg_enrichment_service=None,        # <-- injecao opcional para testes
    ):
        super().__init__(parent)

        self._structure_id = structure_id
        self._db_path      = db_path
        self.saved         = False
        self.saved_structure_id = None
        self._legs_rows: list[dict] = []

        # Injeta repositorio mockado em testes, ou cria o real em producao
        if _repo is not None:
            self._repo = _repo
        else:
            self._repo = StructuresRepository(db_path)

        self._leg_enrichment_service = _leg_enrichment_service

        # Variaveis de formulario -- inicializadas ANTES de _build_ui
        # para que _load_existing() possa fazer .set() mesmo se chamado
        # antes do mainloop (cenario de teste headless via object.__new__)
        self._f_name       = tk.StringVar()
        self._f_underlying = tk.StringVar()
        self._f_alias      = tk.StringVar()
        self._f_status     = tk.StringVar(value="active")
        self._f_status_label = tk.StringVar(value=_STATUS_TO_LABEL["active"])
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
            ("Status",         self._f_status_label, "combo", ["Ativa", "Arquivada"]),
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

        # === Pernas ===
        legs_outer = ttk.LabelFrame(self, text="Pernas", padding=8)
        legs_outer.pack(fill="both", expand=True, padx=8, pady=4)

        # Toolbar de legs
        leg_toolbar = ttk.Frame(legs_outer)
        leg_toolbar.pack(fill="x", pady=(0, 4))
        ttk.Button(leg_toolbar, text="+ Perna",    command=self._cmd_add_leg).pack(side="left", padx=2)
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

    def _set_status_value(self, value: str):
        """Atualiza status interno e rotulo exibido no combobox."""
        raw = str(value or "active").strip()
        status = _LABEL_TO_STATUS.get(raw, raw)

        if status not in _STATUS_TO_LABEL:
            status = "active"

        status_var = getattr(self, "_f_status", None)
        if status_var is not None and hasattr(status_var, "set"):
            status_var.set(status)

        label_var = getattr(self, "_f_status_label", None)
        if label_var is not None and hasattr(label_var, "set"):
            label_var.set(_STATUS_TO_LABEL[status])

    def _get_status_value(self) -> str:
        """Retorna o valor interno do status a partir do rotulo exibido.

        Compatível também com testes que constroem o dialog sem executar
        __init__ completo e, portanto, sem _f_status_label.
        """
        status_var = getattr(self, "_f_status", None)
        label_var = getattr(self, "_f_status_label", None)

        raw = None

        if label_var is not None and hasattr(label_var, "get"):
            try:
                raw = label_var.get()
            except Exception:
                raw = None

        if raw in (None, "") and status_var is not None and hasattr(status_var, "get"):
            try:
                raw = status_var.get()
            except Exception:
                raw = None

        raw = str(raw or "active").strip()
        status = _LABEL_TO_STATUS.get(raw, raw)

        if status not in _STATUS_TO_LABEL:
            status = "active"

        if status_var is not None and hasattr(status_var, "set"):
            try:
                status_var.set(status)
            except Exception:
                pass

        if label_var is not None and hasattr(label_var, "set"):
            try:
                label_var.set(_STATUS_TO_LABEL[status])
            except Exception:
                pass

        return status

    def _build_leg_form(self, parent: tk.Widget):
        """Formulario colapsavel para editar / adicionar uma leg."""
        form = ttk.LabelFrame(parent, text="Editar Perna", padding=6)
        form.pack(fill="x", pady=(6, 0))

        self._lf_side    = tk.StringVar(value="COMPRADO")
        self._lf_type    = tk.StringVar(value="")
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
            ("Lado",  self._lf_side, ["COMPRADO", "VENDIDO"]),
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

        # Botoes da leg
        btns = ttk.Frame(form)
        btns.pack(fill="x", pady=(4, 0))

        ttk.Button(
            btns,
            text="Auto preencher por simbolo",
            command=self._cmd_enrich_current_leg,
        ).pack(side="right", padx=(4, 0))

        ttk.Button(
            btns,
            text="[v] Aplicar Perna",
            command=self._cmd_apply_leg,
        ).pack(side="right")

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
        self._set_status_value(data.get("status", "active"))
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

    def _set_editing_leg_index(self, idx: int | None) -> None:
        """Define qual leg esta sendo editada no formulario."""
        if idx is None:
            self._editing_leg_index = None
            return

        if idx < 0 or idx >= len(self._legs_rows):
            self._editing_leg_index = None
            return

        self._editing_leg_index = idx

    def _get_editing_leg_index(self) -> Optional[int]:
        """Retorna a leg em edicao, independente da selecao atual da tree."""
        idx = getattr(self, "_editing_leg_index", None)

        if idx is None:
            return None

        try:
            idx = int(idx)
        except (TypeError, ValueError):
            self._editing_leg_index = None
            return None

        if idx < 0 or idx >= len(self._legs_rows):
            self._editing_leg_index = None
            return None

        return idx

    def _assert_no_duplicate_symbol_for_leg(
        self,
        symbol: str | None,
        current_idx: int,
    ) -> None:
        """
        Impede simbolo duplicado dentro da mesma estrutura.

        Permite o mesmo simbolo em outra estrutura, pois aqui a validacao
        e apenas na lista de legs da estrutura atual.
        """
        normalized = str(symbol or "").strip().upper()
        if not normalized:
            return

        for idx, leg in enumerate(self._legs_rows):
            if idx == current_idx:
                continue

            other = str(leg.get("symbol") or "").strip().upper()
            if other == normalized:
                raise ValueError(
                    f"Opcao duplicada nesta estrutura: {normalized}. "
                    f"Ja existe na perna {idx + 1}."
                )

    # ------------------------------------------------------------------
    # Callbacks de legs
    # ------------------------------------------------------------------

    def _on_leg_double_click(self, _event=None):
        """Popula o formulario com a leg duplo-clicada."""
        idx = self._selected_leg_index()
        if idx is None:
            return

        self._set_editing_leg_index(idx)
        leg = self._legs_rows[idx]
        self._lf_side.set(normalize_position_side(leg.get("position_side", "COMPRADO")))
        self._lf_type.set(leg.get("option_type", ""))
        self._lf_strike.set(str(leg.get("strike", "")))
        self._lf_expiry.set(str(leg.get("expiration_date", "")))
        self._lf_qty.set(str(leg.get("quantity", "1")))
        self._lf_premium.set(str(leg.get("premium") or ""))
        self._lf_mult.set(str(leg.get("multiplier", 1)))
        self._lf_symbol.set(str(leg.get("symbol") or ""))

    def _cmd_add_leg(self):
        """Adiciona uma leg nova em branco e seleciona para edicao."""
        new_leg = {
            "position_side":   "COMPRADO",
            "option_type":     "",
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
            messagebox.showwarning("Remover Perna", "Selecione uma perna primeiro.", parent=self)
            return
        self._legs_rows.pop(idx)
        self._set_editing_leg_index(None)
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

        editing_idx = self._get_editing_leg_index()
        if editing_idx == idx:
            self._set_editing_leg_index(new_idx)
        elif editing_idx == new_idx:
            self._set_editing_leg_index(idx)

        self._refresh_leg_tree()
        self._leg_tree.selection_set(str(new_idx))


    def _get_leg_enrichment_service(self):
        """Cria/lê o service de enriquecimento por símbolo sob demanda."""
        service = getattr(self, "_leg_enrichment_service", None)

        # Em testes headless via object.__new__, pode existir atributo de classe
        # ou mock incompatível. Só reutiliza se parecer um service válido.
        if service is not None and hasattr(service, "enrich"):
            return service

        repo = RtdOptionQuotesRepository(getattr(self, "_db_path", "dados/app.db"))
        service = StructureLegRtdEnrichmentService(repo)
        self._leg_enrichment_service = service
        return service

    @staticmethod
    def _leg_has_manual_required_fields(leg_data: dict) -> bool:
        """Compatibilidade: permite leg manual completa mesmo sem cotacao RTD."""
        return all(
            str(leg_data.get(key) or "").strip()
            for key in ("option_type", "strike", "expiration_date")
        )

    def _enrich_leg_data_from_symbol(
        self,
        leg_data: dict,
        *,
        require_quote: bool,
    ) -> dict:
        """Enriquece uma leg por symbol/codigo_opcao quando informado.

        require_quote=True:
            usado no botao/aplicar leg; symbol invalido bloqueia.

        require_quote=False:
            usado no save/build payload; se a leg manual ja esta completa,
            preserva compatibilidade e nao acessa RTD.
        """
        symbol = str(leg_data.get("symbol") or leg_data.get("codigo_opcao") or "").strip()
        if not symbol:
            return leg_data

        # Compatibilidade com testes e com fluxo manual completo:
        # _build_legs_payload historicamente era uma rotina pura, sem I/O.
        if not require_quote and self._leg_has_manual_required_fields(leg_data):
            return leg_data

        try:
            enriched = self._get_leg_enrichment_service().enrich(leg_data)
        except Exception:
            if require_quote:
                self._refresh_rtd_quote_for_symbol(symbol)
                enriched = self._get_leg_enrichment_service().enrich(leg_data)
            else:
                if not require_quote and self._leg_has_manual_required_fields(leg_data):
                    return leg_data
                raise

        merged = dict(leg_data)
        merged.update(enriched)
        return merged


    def _refresh_rtd_quote_for_symbol(self, symbol: str) -> None:
        """Atualiza uma opção avulsa no RTD/Excel e importa para o cache local."""
        import subprocess
        import sys
        from pathlib import Path

        symbol = str(symbol or "").strip().upper()

        if not symbol:
            return

        project_root = Path(__file__).resolve().parents[2]

        script = project_root / "scripts" / "refresh_rtd_symbol_to_option_quotes_fallback.py"
        workbook_path = project_root / "LISTA_RTD.xlsm"

        db_candidate = (
            getattr(self, "_db_path", None)
            or getattr(self, "db_path", None)
            or project_root / "dados" / "app.db"
        )

        db_path = Path(db_candidate)

        if not db_path.is_absolute():
            db_path = project_root / db_path

        if not script.exists():
            raise ValueError(f"Script de refresh RTD não encontrado: {script}")

        if not workbook_path.exists():
            raise ValueError(f"Planilha RTD não encontrada: {workbook_path}")

        cmd = [
            sys.executable,
            str(script),
            "--symbol",
            symbol,
            "--db",
            str(db_path),
            "--workbook",
            str(workbook_path),
            "--wait-seconds",
            "10",
            "--json",
        ]

        completed = subprocess.run(
            cmd,
            cwd=str(project_root),
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=45,
            check=False,
        )

        if completed.returncode != 0:
            detail = "\n".join(
                part
                for part in [completed.stdout.strip(), completed.stderr.strip()]
                if part
            )

            if len(detail) > 2500:
                detail = detail[-2500:]

            raise ValueError(
                "Não foi possível atualizar a cotação RTD para "
                f"{symbol}.\n\n{detail}"
            )


    def _sync_underlying_from_enriched_leg(self, enriched: dict) -> None:
        """Preenche/valida o ativo objeto da estrutura a partir da opção."""
        underlying = str(enriched.get("underlying_asset") or "").strip().upper()
        if not underlying:
            return

        current = self._f_underlying.get().strip().upper()
        if current and current != underlying:
            raise ValueError(
                "Ativo objeto divergente do símbolo informado: "
                f"estrutura={current}, detectado={underlying}, "
                f"symbol={enriched.get('symbol')}"
            )

        if not current:
            self._f_underlying.set(underlying)

    def _current_leg_form_data(self, idx: int | None = None) -> dict:
        return {
            "position_side":   normalize_position_side(self._lf_side.get()),
            "option_type":     self._lf_type.get(),
            "strike":          self._lf_strike.get(),
            "expiration_date": self._lf_expiry.get(),
            "quantity":        self._lf_qty.get(),
            "premium":         self._lf_premium.get() or None,
            "multiplier":      self._lf_mult.get() or 1,
            "leg_order":       (idx + 1) if idx is not None else 1,
            "symbol":          self._lf_symbol.get() or None,
            "notes":           None,
        }

    def _apply_enriched_leg_to_form(self, enriched: dict) -> None:
        """Reflete dados detectados no formulario visual da leg."""
        if enriched.get("option_type"):
            self._lf_type.set(str(enriched["option_type"]).upper())
        if enriched.get("strike") is not None:
            self._lf_strike.set(str(enriched["strike"]))
        if enriched.get("expiration_date"):
            self._lf_expiry.set(str(enriched["expiration_date"]))
        if enriched.get("premium") is not None:
            self._lf_premium.set(str(enriched["premium"]))
        if enriched.get("multiplier") is not None:
            self._lf_mult.set(str(enriched["multiplier"]))
        if enriched.get("symbol"):
            self._lf_symbol.set(str(enriched["symbol"]).upper())

    def _cmd_enrich_current_leg(self):
        """Botao: auto preenche leg usando symbol/codigo_opcao."""
        idx = self._get_editing_leg_index()
        if idx is None:
            messagebox.showwarning(
                "Auto preencher",
                "De duplo clique em uma leg para edita-la antes de auto preencher.",
                parent=self,
            )
            return

        try:
            leg_data = self._current_leg_form_data(idx)
            enriched = self._enrich_leg_data_from_symbol(
                leg_data,
                require_quote=True,
            )
            self._sync_underlying_from_enriched_leg(enriched)
            self._apply_enriched_leg_to_form(enriched)
            self._assert_no_duplicate_symbol_for_leg(
                enriched.get("symbol"),
                idx,
            )
            self._legs_rows[idx] = enriched
            self._refresh_leg_tree()
        except ValueError as exc:
            messagebox.showerror("Auto preencher", str(exc), parent=self)

    def _cmd_apply_leg(self):
        """Aplica os valores do formulario na leg em edicao."""
        idx = self._get_editing_leg_index()
        if idx is None:
            messagebox.showwarning(
                "Aplicar Perna",
                "De duplo clique em uma perna para edita-la antes de aplicar.",
                parent=self,
            )
            return

        try:
            leg_data = self._current_leg_form_data(idx)

            # Fase 3: se houver simbolo, tenta reconhecer a opcao e preencher
            # ativo, tipo, strike, vencimento e multiplicador.
            if leg_data.get("symbol"):
                leg_data = self._enrich_leg_data_from_symbol(
                    leg_data,
                    require_quote=True,
                )
                self._sync_underlying_from_enriched_leg(leg_data)
                self._apply_enriched_leg_to_form(leg_data)

            self._assert_no_duplicate_symbol_for_leg(
                leg_data.get("symbol"),
                idx,
            )

            self._legs_rows[idx] = leg_data
            self._refresh_leg_tree()

        except ValueError as exc:
            messagebox.showerror("Erro de Validacao", str(exc), parent=self)

    # ------------------------------------------------------------------
    # Logica de payload (pura -- testavel sem display)
    # ------------------------------------------------------------------


    def _build_legs_payload(self) -> list[dict]:
        """
        Constrói lista de legs com leg_order sequencial a partir de 1.

        Regras:
        - Não modifica self._legs_rows.
        - Normaliza position_side legado: LONG/SHORT -> COMPRADO/VENDIDO.
        - Aceita decimal pt-BR com vírgula em strike, premium e multiplier.
        - Mantém premium None quando vazio.
        """

        def _parse_decimal(value, field_name: str) -> float:
            if value is None or value == "":
                raise ValueError(f"{field_name} é obrigatório")

            if isinstance(value, (int, float)):
                return float(value)

            text = str(value).strip()
            if not text:
                raise ValueError(f"{field_name} é obrigatório")

            # Suporta "100,50" e também "1.234,56".
            if "," in text and "." in text:
                text = text.replace(".", "").replace(",", ".")
            else:
                text = text.replace(",", ".")

            try:
                return float(text)
            except ValueError as exc:
                raise ValueError(f"{field_name} deve ser numérico") from exc

        def _parse_int(value, field_name: str) -> int:
            number = _parse_decimal(value, field_name)
            if int(number) != number:
                raise ValueError(f"{field_name} deve ser inteiro")
            return int(number)

        def _normalize_position_side(value) -> str:
            text = str(value or "").strip().upper()
            mapping = {
                "LONG": "COMPRADO",
                "BUY": "COMPRADO",
                "BOUGHT": "COMPRADO",
                "COMPRADO": "COMPRADO",
                "SHORT": "VENDIDO",
                "SELL": "VENDIDO",
                "SOLD": "VENDIDO",
                "VENDIDO": "VENDIDO",
            }
            return mapping.get(text, text)

        payload = []
        seen_symbols: dict[str, int] = {}

        for index, leg in enumerate(self._legs_rows, start=1):
            row = dict(leg)

            try:
                row = self._enrich_leg_data_from_symbol(
                    row,
                    require_quote=False,
                )
            except ValueError as exc:
                raise ValueError(f"Perna {index}: {exc}") from exc

            row["position_side"] = _normalize_position_side(
                row.get("position_side", "COMPRADO")
            )
            row["strike"] = _parse_decimal(row.get("strike"), "strike")
            row["quantity"] = _parse_int(row.get("quantity", 1), "quantity")

            premium_raw = row.get("premium")
            row["premium"] = (
                None
                if premium_raw in (None, "")
                else _parse_decimal(premium_raw, "premium")
            )

            multiplier_raw = row.get("multiplier")
            row["multiplier"] = (
                1
                if multiplier_raw in (None, "")
                else _parse_decimal(multiplier_raw, "multiplier")
            )

            row["leg_order"] = index

            symbol_norm = str(row.get("symbol") or "").strip().upper()
            if symbol_norm:
                previous_index = seen_symbols.get(symbol_norm)
                if previous_index is not None:
                    raise ValueError(
                        f"Opcao duplicada nesta estrutura: {symbol_norm}. "
                        f"Ja existe na perna {previous_index} e foi repetida na perna {index}."
                    )
                seen_symbols[symbol_norm] = index

            payload.append(row)

        return payload

    def _cmd_save(self):
        name       = self._f_name.get().strip()
        underlying = self._f_underlying.get().strip()

        if not name:
            messagebox.showwarning("Salvar", "O campo 'Nome' e obrigatorio.", parent=self)
            return

        try:
            legs_payload = self._build_legs_payload()
        except ValueError as exc:
            messagebox.showerror("Erro de Validacao", str(exc), parent=self)
            return

        if not underlying:
            detected_assets = sorted({
                str(leg.get("underlying_asset") or "").strip().upper()
                for leg in legs_payload
                if str(leg.get("underlying_asset") or "").strip()
            })
            if len(detected_assets) == 1:
                underlying = detected_assets[0]
                self._f_underlying.set(underlying)
            elif len(detected_assets) > 1:
                messagebox.showwarning(
                    "Salvar",
                    "As legs possuem ativos objeto diferentes: "
                    + ", ".join(detected_assets),
                    parent=self,
                )
                return

        if not underlying:
            messagebox.showwarning("Salvar", "O campo 'Ativo' e obrigatorio.", parent=self)
            return

        structure_data = {
            "name":             name,
            "underlying_asset": underlying,
            "alias_legacy_aba": self._f_alias.get().strip() or None,
            "status":           self._get_status_value(),
            "notes":            self._f_notes.get().strip() or None,
        }

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

            try:
                if getattr(self, "_structure_id", None) is not None:
                    self.saved_structure_id = int(self._structure_id)
                else:
                    _candidate_saved_structure_id = (
                        locals().get("created_structure_id")
                        or locals().get("new_structure_id")
                        or locals().get("structure_id")
                        or locals().get("sid")
                        or locals().get("new_id")
                        or locals().get("created_id")
                    )
                    self.saved_structure_id = (
                        int(_candidate_saved_structure_id)
                        if _candidate_saved_structure_id is not None
                        else None
                    )
            except Exception:
                self.saved_structure_id = getattr(self, "_structure_id", None)
            self.saved = True
            self.destroy()

        except ValueError as exc:
            messagebox.showerror("Erro de Validacao", str(exc), parent=self)
        except Exception as exc:
            messagebox.showerror("Erro", f"Falha ao salvar: {exc}", parent=self)
