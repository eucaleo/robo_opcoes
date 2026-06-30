from pathlib import Path

path = Path("UI/components/terminal_vwap_payoff_dark_panel.py")

if not path.exists():
    raise SystemExit(f"Arquivo nao encontrado: {path}")

text = path.read_text(encoding="utf-8")
original = text

backup = Path("UI/components/terminal_vwap_payoff_dark_panel.py.bak_side_actions_fix")
if not backup.exists():
    backup.write_text(original, encoding="utf-8")

direct_imports = (
    "from tkinter import messagebox\n"
    "from repositories.structures_repository import StructuresRepository\n"
    "from UI.components.structure_editor_dialog import StructureEditorDialog\n"
)

guarded_imports = (
    "from tkinter import messagebox\n"
    "\n"
    "try:\n"
    "    from repositories.structures_repository import StructuresRepository\n"
    "except Exception:\n"
    "    StructuresRepository = None\n"
    "\n"
    "try:\n"
    "    from UI.components.structure_editor_dialog import StructureEditorDialog\n"
    "except Exception:\n"
    "    StructureEditorDialog = None\n"
)

if direct_imports in text and "StructuresRepository = None" not in text:
    text = text.replace(direct_imports, guarded_imports, 1)

btn_block = (
    "        btn_add = ctk.CTkButton(\n"
    "            self.side,\n"
    "            text=\"+ Nova Estrutura\",\n"
    "            height=32,\n"
    "            fg_color=GREEN,\n"
    "            hover_color=\"#059669\",\n"
    "            text_color=TEXT,\n"
    "            command=self.new_structure,\n"
    "        )\n"
    "        btn_add.pack(fill=\"x\", padx=10, pady=(8, 10))\n"
    "\n"
)

wrong_render_start = (
    "    def _render_structures_list(self) -> None:\n"
    f"{btn_block}"
    "        for widget in self.side.winfo_children():\n"
    "            widget.destroy()\n"
)

right_render_start = (
    "    def _render_structures_list(self) -> None:\n"
    "        for widget in self.side.winfo_children():\n"
    "            widget.destroy()\n"
    "\n"
    f"{btn_block}"
)

if wrong_render_start in text:
    text = text.replace(wrong_render_start, right_render_start, 1)

if (
    "    def _render_structures_list(self) -> None:\n"
    "        for widget in self.side.winfo_children():\n"
    "            widget.destroy()\n"
    "\n"
    "        btn_add = ctk.CTkButton(\n"
) not in text:
    marker = (
        "    def _render_structures_list(self) -> None:\n"
        "        for widget in self.side.winfo_children():\n"
        "            widget.destroy()\n"
    )
    if marker in text and "+ Nova Estrutura" not in text[text.find(marker):text.find(marker) + 500]:
        text = text.replace(marker, marker + "\n" + btn_block, 1)

new_structure_old = (
    "    def new_structure(self) -> None:\n"
    "        try:\n"
    "            dlg = StructureEditorDialog(\n"
)

new_structure_new = (
    "    def new_structure(self) -> None:\n"
    "        if StructureEditorDialog is None:\n"
    "            messagebox.showerror(\n"
    "                \"Editor indisponivel\",\n"
    "                \"StructureEditorDialog nao foi encontrado.\",\n"
    "                parent=self.winfo_toplevel(),\n"
    "            )\n"
    "            return\n"
    "\n"
    "        try:\n"
    "            dlg = StructureEditorDialog(\n"
)

if new_structure_old in text and "StructureEditorDialog is None" not in text[text.find("    def new_structure"):text.find("    def new_structure") + 500]:
    text = text.replace(new_structure_old, new_structure_new, 1)

edit_old = (
    "    def edit_selected_structure(self) -> None:\n"
    "        structure = self._require_selected_structure()\n"
    "        if not structure:\n"
    "            return\n"
    "\n"
    "        sid = structure.get(\"id\")\n"
    "\n"
    "        try:\n"
)

edit_new = (
    "    def edit_selected_structure(self) -> None:\n"
    "        structure = self._require_selected_structure()\n"
    "        if not structure:\n"
    "            return\n"
    "\n"
    "        if StructureEditorDialog is None:\n"
    "            messagebox.showerror(\n"
    "                \"Editor indisponivel\",\n"
    "                \"StructureEditorDialog nao foi encontrado.\",\n"
    "                parent=self.winfo_toplevel(),\n"
    "            )\n"
    "            return\n"
    "\n"
    "        sid = structure.get(\"id\")\n"
    "\n"
    "        try:\n"
)

if edit_old in text and "StructureEditorDialog is None" not in text[text.find("    def edit_selected_structure"):text.find("    def edit_selected_structure") + 700]:
    text = text.replace(edit_old, edit_new, 1)

archive_old = (
    "        sid = structure.get(\"id\")\n"
    "\n"
    "        ok = messagebox.askyesno(\n"
    "            \"Arquivar\",\n"
)

archive_new = (
    "        sid = structure.get(\"id\")\n"
    "\n"
    "        if StructuresRepository is None:\n"
    "            messagebox.showerror(\n"
    "                \"Repositorio indisponivel\",\n"
    "                \"StructuresRepository nao foi encontrado.\",\n"
    "                parent=self.winfo_toplevel(),\n"
    "            )\n"
    "            return\n"
    "\n"
    "        ok = messagebox.askyesno(\n"
    "            \"Arquivar\",\n"
)

archive_pos = text.find("    def archive_selected_structure")
if archive_pos != -1:
    archive_slice = text[archive_pos:archive_pos + 1200]
    if "StructuresRepository is None" not in archive_slice and archive_old in archive_slice:
        text = text[:archive_pos] + text[archive_pos:].replace(archive_old, archive_new, 1)

text = text.replace(
    "                self.on_status(f\"Falha ao abrir painel de acoes: {exc}\")\n    def _find_legs_table",
    "                self.on_status(f\"Falha ao abrir painel de acoes: {exc}\")\n\n    def _find_legs_table",
    1,
)

if text != original:
    path.write_text(text, encoding="utf-8", newline="\n")
    print("Correcoes aplicadas.")
    print(f"Backup criado em: {backup}")
else:
    print("Nenhuma correcao adicional necessaria.")
