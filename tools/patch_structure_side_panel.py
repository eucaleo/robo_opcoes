import os
import re
from pathlib import Path


ROOT = Path.cwd()
TARGET_MARKER_FILE = ROOT / ".patch_structure_target"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def is_ignored(path: Path) -> bool:
    parts = set(path.parts)
    ignored = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "build",
        "dist",
        "tools",
        ".mypy_cache",
        ".pytest_cache",
    }
    return bool(parts & ignored)


def locate_target() -> Path:
    env_target = os.environ.get("TARGET_FILE")
    if env_target:
        path = ROOT / env_target
        if not path.exists():
            raise SystemExit(f"TARGET_FILE nao encontrado: {path}")
        return path

    candidates = []
    for path in ROOT.rglob("*.py"):
        if is_ignored(path):
            continue
        try:
            text = read_text(path)
        except UnicodeDecodeError:
            continue

        if (
            "def select_structure" in text
            and "def _render_structures_list" in text
            and "selected_structure" in text
        ):
            candidates.append(path)

    if not candidates:
        raise SystemExit(
            "Nao encontrei automaticamente o arquivo alvo. Rode novamente assim:\n"
            "TARGET_FILE=caminho/do/arquivo.py python tools/patch_structure_side_panel.py"
        )

    if len(candidates) > 1:
        print("Mais de um candidato encontrado. Usando o primeiro:")
        for item in candidates:
            print(f"  - {item}")

    return candidates[0]


def leading_spaces(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def insert_after_imports(text: str, chunk: str) -> str:
    if not chunk.strip():
        return text

    lines = text.splitlines()
    insert_at = 0

    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            insert_at = index + 1

    addition = chunk.strip("\n").splitlines()
    lines[insert_at:insert_at] = addition + [""]
    return "\n".join(lines) + "\n"


def ensure_imports(text: str) -> str:
    additions = []

    if "from tkinter import messagebox" not in text and "import messagebox" not in text:
        additions.append("from tkinter import messagebox")

    if "StructuresRepository" not in text:
        additions.append("from repositories.structures_repository import StructuresRepository")

    if "StructureEditorDialog" not in text:
        additions.append("from UI.components.structure_editor_dialog import StructureEditorDialog")

    if "Any" not in text:
        additions.append("from typing import Any")

    return insert_after_imports(text, "\n".join(additions))


def ensure_decision_helpers(text: str) -> str:
    if "BEGIN AUTO STRUCTURE DECISION HELPERS" in text:
        return text

    helper = """
# BEGIN AUTO STRUCTURE DECISION HELPERS
if "DECISION_LABELS" not in globals():
    DECISION_LABELS = {
        "HOLD": "Manter",
        "ADJUST": "Ajustar",
        "CLOSE": "Encerrar",
    }


def decision_label(value: Any) -> str:
    if value is None:
        return "--"
    raw = str(value).strip()
    return DECISION_LABELS.get(raw.upper(), raw)
# END AUTO STRUCTURE DECISION HELPERS
""".strip("\n")

    class_match = re.search(r"(?m)^class\s+\w+.*:\s*$", text)
    if class_match:
        return text[:class_match.start()] + helper + "\n\n" + text[class_match.start():]

    return text + "\n\n" + helper + "\n"


def find_method_region(lines: list[str], method_name: str):
    pattern = re.compile(rf"^(\s*)def\s+{re.escape(method_name)}\s*\(")

    start = None
    indent = None

    for index, line in enumerate(lines):
        match = pattern.match(line)
        if match:
            start = index
            indent = leading_spaces(line)
            break

    if start is None:
        return None

    end = len(lines)
    for index in range(start + 1, len(lines)):
        stripped = lines[index].strip()
        if not stripped:
            continue

        line_indent = leading_spaces(lines[index])
        if line_indent <= indent and (
            lines[index].lstrip().startswith("def ")
            or lines[index].lstrip().startswith("class ")
            or lines[index].lstrip().startswith("@")
        ):
            end = index
            break

    return start, end, indent


def patch_render_structures_list(text: str) -> str:
    lines = text.splitlines()
    region = find_method_region(lines, "_render_structures_list")
    if not region:
        print("Aviso: metodo _render_structures_list nao encontrado.")
        return text

    start, end, indent = region
    method_text = "\n".join(lines[start:end])

    if "+ Nova Estrutura" in method_text:
        return text

    body_indent = " " * (indent + 4)

    block = [
        f'{body_indent}btn_add = ctk.CTkButton(',
        f'{body_indent}    self.side,',
        f'{body_indent}    text="+ Nova Estrutura",',
        f'{body_indent}    height=32,',
        f'{body_indent}    fg_color=GREEN,',
        f'{body_indent}    hover_color="#059669",',
        f'{body_indent}    text_color=TEXT,',
        f'{body_indent}    command=self.new_structure,',
        f'{body_indent})',
        f'{body_indent}btn_add.pack(fill="x", padx=10, pady=(8, 10))',
        "",
    ]

    insert_at = start + 1
    for index in range(start + 1, end):
        if "_clear_side()" in lines[index]:
            insert_at = index + 1
            break

    lines[insert_at:insert_at] = block
    return "\n".join(lines) + "\n"


def patch_select_structure(text: str) -> str:
    lines = text.splitlines()
    region = find_method_region(lines, "select_structure")
    if not region:
        print("Aviso: metodo select_structure nao encontrado.")
        return text

    start, end, indent = region
    method_text = "\n".join(lines[start:end])

    if "self._render_structure_actions()" in method_text:
        return text

    body_indent = " " * (indent + 4)

    block = [
        "",
        f"{body_indent}try:",
        f"{body_indent}    self._render_structure_actions()",
        f"{body_indent}except Exception as exc:",
        f"{body_indent}    if hasattr(self, 'on_status'):",
        f'{body_indent}        self.on_status(f"Falha ao abrir painel de acoes: {{exc}}")',
    ]

    lines[end:end] = block
    return "\n".join(lines) + "\n"


def patch_fixed_rail_buttons(text: str) -> str:
    if "btn_new_fixed" in text and "btn_struct_actions" in text:
        return text

    lines = text.splitlines()

    command_line = None
    for index, line in enumerate(lines):
        if "command=self.reload_structures" in line:
            command_line = index
            break

    if command_line is None:
        print("Aviso: nao encontrei command=self.reload_structures para inserir botoes fixos da rail.")
        return text

    pack_line = None
    for index in range(command_line, min(command_line + 20, len(lines))):
        if ".pack(" in lines[index]:
            pack_line = index
            break

    if pack_line is None:
        print("Aviso: nao encontrei pack do botao de recarregar.")
        return text

    indent = " " * leading_spaces(lines[pack_line])

    block = [
        "",
        f"{indent}self.btn_new_fixed = ctk.CTkButton(",
        f"{indent}    self.rail,",
        f'{indent}    text="+",',
        f"{indent}    width=50,",
        f"{indent}    height=42,",
        f"{indent}    fg_color=GREEN,",
        f'{indent}    hover_color="#059669",',
        f"{indent}    text_color=TEXT,",
        f'{indent}    font=ctk.CTkFont(size=22, weight="bold"),',
        f"{indent}    command=self.new_structure,",
        f"{indent})",
        f"{indent}self.btn_new_fixed.pack(pady=6, padx=10)",
        "",
        f"{indent}self.btn_struct_actions = ctk.CTkButton(",
        f"{indent}    self.rail,",
        f'{indent}    text="Acoes",',
        f"{indent}    width=50,",
        f"{indent}    height=42,",
        f"{indent}    fg_color=CARD_BG_2,",
        f"{indent}    hover_color=BLUE,",
        f"{indent}    text_color=TEXT,",
        f'{indent}    font=ctk.CTkFont(size=11, weight="bold"),',
        f"{indent}    command=self._render_structure_actions,",
        f"{indent})",
        f"{indent}self.btn_struct_actions.pack(pady=6, padx=10)",
    ]

    lines[pack_line + 1:pack_line + 1] = block
    return "\n".join(lines) + "\n"


def find_owner_class_region(text: str):
    lines = text.splitlines()
    method_region = find_method_region(lines, "_render_structures_list")
    if not method_region:
        return None

    method_start = method_region[0]

    class_line = None
    for index in range(method_start, -1, -1):
        if re.match(r"^\s*class\s+\w+.*:\s*$", lines[index]):
            class_line = index
            break

    if class_line is None:
        return None

    class_indent = leading_spaces(lines[class_line])

    class_end = len(lines)
    for index in range(class_line + 1, len(lines)):
        stripped = lines[index].strip()
        if not stripped:
            continue

        if leading_spaces(lines[index]) <= class_indent and not lines[index].lstrip().startswith("#"):
            class_end = index
            break

    return class_line, class_end, class_indent


def ensure_class_methods(text: str) -> str:
    if "BEGIN AUTO STRUCTURE SIDE ACTIONS" in text:
        return text

    lines = text.splitlines()
    class_region = find_owner_class_region(text)
    if not class_region:
        print("Aviso: classe dona de _render_structures_list nao encontrada.")
        return text

    _, class_end, class_indent = class_region
    method_indent = " " * (class_indent + 4)

    raw_block = r'''
# BEGIN AUTO STRUCTURE SIDE ACTIONS
def _safe_status(self, message: str) -> None:
    if hasattr(self, "on_status"):
        self.on_status(message)


def _get_db_path(self) -> str:
    for attr in ("db_path", "database_path", "db_file", "database_file"):
        value = getattr(self, attr, None)
        if value:
            return value
    raise RuntimeError("Caminho do banco nao encontrado. Ajuste o atributo db_path neste componente.")


def _clear_side(self) -> None:
    for child in self.side.winfo_children():
        child.destroy()


def _require_selected_structure(self):
    structure = getattr(self, "selected_structure", None)
    if not structure:
        messagebox.showwarning(
            "Estrutura",
            "Selecione uma estrutura antes de executar esta acao.",
            parent=self.winfo_toplevel(),
        )
        return None
    return structure


def _side_section_title(self, text: str) -> None:
    label = ctk.CTkLabel(
        self.side,
        text=text,
        text_color=MUTED,
        font=ctk.CTkFont(size=11, weight="bold"),
        anchor="w",
    )
    label.pack(fill="x", padx=10, pady=(16, 6))


def _side_button(self, text: str, color: str, hover: str, command) -> None:
    button = ctk.CTkButton(
        self.side,
        text=text,
        height=34,
        fg_color=color,
        hover_color=hover,
        text_color=TEXT,
        command=command,
    )
    button.pack(fill="x", padx=10, pady=4)


def _render_structure_actions(self) -> None:
    structure = self._require_selected_structure()
    if not structure:
        self._render_structures_list()
        return

    self._clear_side()

    sid = structure.get("id")
    name = structure.get("name")
    asset = structure.get("underlying_asset")
    status = structure.get("status")

    title = ctk.CTkLabel(
        self.side,
        text="ESTRUTURA ATIVA",
        text_color=MUTED,
        font=ctk.CTkFont(size=11, weight="bold"),
        anchor="w",
    )
    title.pack(fill="x", pady=(15, 8), padx=10)

    info_frame = ctk.CTkFrame(self.side, fg_color=CARD_BG_2, corner_radius=8)
    info_frame.pack(fill="x", padx=10, pady=0)

    info = ctk.CTkLabel(
        info_frame,
        text=f"ID {sid}\n{name}\nAtivo: {asset}\nStatus: {status}",
        text_color=TEXT,
        justify="left",
        anchor="w",
    )
    info.pack(fill="x", padx=10, pady=10)

    self._side_section_title("PAYOFF")
    self._side_button(
        text="Recalcular Payoff",
        color=BLUE,
        hover="#2563EB",
        command=self.recalculate_selected_structure,
    )

    self._side_section_title("ESTRUTURA")
    self._side_button(
        text="Editar pernas",
        color=CARD_BG_2,
        hover="#374151",
        command=self.edit_selected_structure,
    )
    self._side_button(
        text="Duplicar estrutura",
        color=CARD_BG_2,
        hover="#374151",
        command=self.duplicate_selected_structure,
    )
    self._side_button(
        text="Arquivar estrutura",
        color="#92400E",
        hover="#78350F",
        command=self.archive_selected_structure,
    )

    self._side_section_title("DECISAO")
    self._side_button(
        text="Manter",
        color=GREEN,
        hover="#059669",
        command=lambda: self._register_structure_decision("HOLD"),
    )
    self._side_button(
        text="Ajustar / Trocar perna",
        color="#D97706",
        hover="#B45309",
        command=self._render_adjust_structure_block,
    )
    self._side_button(
        text="Encerrar",
        color="#DC2626",
        hover="#991B1B",
        command=lambda: self._register_structure_decision("CLOSE"),
    )

    self._side_button(
        text="Voltar para lista",
        color="#111827",
        hover="#1F2937",
        command=self._render_structures_list,
    )


def _render_adjust_structure_block(self) -> None:
    structure = self._require_selected_structure()
    if not structure:
        return

    self._clear_side()

    sid = structure.get("id")
    name = structure.get("name")
    asset = structure.get("underlying_asset")

    title = ctk.CTkLabel(
        self.side,
        text="AJUSTAR ESTRUTURA",
        text_color=MUTED,
        font=ctk.CTkFont(size=11, weight="bold"),
        anchor="w",
    )
    title.pack(fill="x", pady=(15, 8), padx=10)

    info_frame = ctk.CTkFrame(self.side, fg_color=CARD_BG_2, corner_radius=8)
    info_frame.pack(fill="x", padx=10, pady=0)

    info = ctk.CTkLabel(
        info_frame,
        text=f"ID {sid}\n{name}\nAtivo: {asset}",
        text_color=TEXT,
        justify="left",
        anchor="w",
    )
    info.pack(fill="x", padx=10, pady=10)

    self._side_section_title("ACAO")
    self._side_button(
        text="Editar pernas",
        color=BLUE,
        hover="#2563EB",
        command=self.edit_selected_structure,
    )
    self._side_button(
        text="Duplicar para ajuste",
        color=CARD_BG_2,
        hover="#374151",
        command=self.duplicate_selected_structure,
    )
    self._side_button(
        text="Registrar decisao ADJUST",
        color="#D97706",
        hover="#B45309",
        command=lambda: self._register_structure_decision("ADJUST"),
    )
    self._side_button(
        text="Voltar",
        color="#111827",
        hover="#1F2937",
        command=self._render_structure_actions,
    )


def new_structure(self) -> None:
    try:
        dlg = StructureEditorDialog(
            self.winfo_toplevel(),
            structure_id=None,
            db_path=self._get_db_path(),
        )
        self.wait_window(dlg)

        if getattr(dlg, "saved", False):
            self._safe_status("Nova estrutura salva")
            self.reload_structures()
            self._render_structures_list()
    except Exception as exc:
        messagebox.showerror("Erro ao criar estrutura", str(exc), parent=self.winfo_toplevel())


def edit_selected_structure(self) -> None:
    structure = self._require_selected_structure()
    if not structure:
        return

    sid = structure.get("id")

    try:
        db_path = self._get_db_path()
        dlg = StructureEditorDialog(
            self.winfo_toplevel(),
            structure_id=sid,
            db_path=db_path,
        )
        self.wait_window(dlg)

        if getattr(dlg, "saved", False):
            self._safe_status(f"Estrutura ID {sid} atualizada")
            self.reload_structures()

            try:
                repo = StructuresRepository(db_path)
                updated = repo.get_structure(sid)
                if updated:
                    self.select_structure(updated)
            except Exception:
                pass

            self._render_structure_actions()
    except Exception as exc:
        messagebox.showerror("Erro ao editar estrutura", str(exc), parent=self.winfo_toplevel())


def duplicate_selected_structure(self) -> None:
    try:
        if hasattr(self, "_cmd_duplicate"):
            self._cmd_duplicate()
            self.reload_structures()
            self._safe_status("Estrutura duplicada")
            return

        messagebox.showinfo(
            "Duplicar estrutura",
            "Metodo _cmd_duplicate nao encontrado neste componente.",
            parent=self.winfo_toplevel(),
        )
    except Exception as exc:
        messagebox.showerror("Erro ao duplicar estrutura", str(exc), parent=self.winfo_toplevel())


def recalculate_selected_structure(self) -> None:
    structure = self._require_selected_structure()
    if not structure:
        return

    sid = structure.get("id")
    name = structure.get("name")
    asset = structure.get("underlying_asset")

    try:
        legs = self._load_legs(sid)
        market = self._load_market(asset)
        payoff_points = self._calculate_payoff_from_legs(legs)

        self.header.configure(
            text=f"Analise ativa: ID {sid} - {name} | Ativo: {asset} | Payoff recalculado"
        )

        self._update_kpis(market, payoff_points)
        self._render_legs(legs)
        self._render_charts(market, payoff_points, asset)
        self._render_alerts(market, payoff_points, legs)

        self._safe_status(f"Payoff recalculado: ID {sid}")
    except Exception as exc:
        messagebox.showerror("Erro ao recalcular payoff", str(exc), parent=self.winfo_toplevel())


def archive_selected_structure(self) -> None:
    structure = self._require_selected_structure()
    if not structure:
        return

    sid = structure.get("id")

    ok = messagebox.askyesno(
        "Arquivar",
        f"Deseja arquivar a estrutura ID {sid}?",
        parent=self.winfo_toplevel(),
    )
    if not ok:
        return

    try:
        repo = StructuresRepository(self._get_db_path())
        repo.archive_structure(sid)

        self.selected_structure = None
        self._safe_status(f"Arquivada ID {sid}")
        self.reload_structures()
        self._render_structures_list()

        if hasattr(self, "header"):
            self.header.configure(
                text="Selecione uma estrutura no menu lateral para carregar a VWAP e Payoff"
            )
    except Exception as exc:
        messagebox.showerror("Erro ao arquivar estrutura", str(exc), parent=self.winfo_toplevel())


def _register_structure_decision(self, decision: str) -> None:
    structure = self._require_selected_structure()
    if not structure:
        return

    sid = structure.get("id")
    label = decision_label(decision)

    self._safe_status(f"Decisao para ID {sid}: {label} ({decision})")
    self._render_structure_actions()
# END AUTO STRUCTURE SIDE ACTIONS
'''.strip("\n")

    indented_block = "\n".join(
        (method_indent + line if line.strip() else "")
        for line in raw_block.splitlines()
    )

    lines[class_end:class_end] = ["", indented_block, ""]
    return "\n".join(lines) + "\n"


def main() -> None:
    target = locate_target()
    print(f"Arquivo alvo: {target}")

    text = read_text(target)
    original = text

    text = ensure_imports(text)
    text = ensure_decision_helpers(text)
    text = patch_fixed_rail_buttons(text)
    text = patch_render_structures_list(text)
    text = patch_select_structure(text)
    text = ensure_class_methods(text)

    if text != original:
        write_text(target, text)
        print("Patch aplicado com sucesso.")
    else:
        print("Nenhuma alteracao necessaria.")

    TARGET_MARKER_FILE.write_text(str(target), encoding="utf-8")


if __name__ == "__main__":
    main()
