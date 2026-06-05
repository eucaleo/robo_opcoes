# ATT/patches/patch_71_structures_list_archive.py
"""
patch_71 -- StructuresListPanel: _set_status() + self._db_path canônico;
            Corrige também constantes tk.* inválidas (tk.W, tk.CENTER, etc.)
            que causam AttributeError na importação do módulo.

Alteração em apenas um arquivo:
    UI/components/structures_list_panel.py
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path
from datetime import datetime

PROJECT_ROOT     = Path(__file__).resolve().parents[2]
STRUCTURES_PANEL = PROJECT_ROOT / "UI" / "components" / "structures_list_panel.py"
BAK_DIR          = PROJECT_ROOT / "ATT" / "BAK"


# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------

def _bak(path: Path) -> Path:
    BAK_DIR.mkdir(parents=True, exist_ok=True)
    ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = BAK_DIR / f"{path.name}.bak_p71_{ts}"
    shutil.copy2(path, dst)
    return dst


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write(path: Path, src: str) -> None:
    path.write_text(src, encoding="utf-8")


# ---------------------------------------------------------------------------
# Patch A — structures_list_panel.py
# ---------------------------------------------------------------------------

def patch_structures_list_panel(dry_run: bool = False) -> list[str]:
    errors: list[str] = []
    src = _read(STRUCTURES_PANEL)

    # ------------------------------------------------------------------
    # 0. Constantes inválidas do tkinter → strings canônicas
    #    tk.CENTER, tk.W, tk.E, tk.N, tk.S etc. NÃO existem no módulo tk
    # ------------------------------------------------------------------
    _TK_CONST_MAP = {
        r"\btk\.CENTER\b": '"center"',
        r"\btk\.W\b":      '"w"',
        r"\btk\.E\b":      '"e"',
        r"\btk\.N\b":      '"n"',
        r"\btk\.S\b":      '"s"',
        r"\btk\.NW\b":     '"nw"',
        r"\btk\.NE\b":     '"ne"',
        r"\btk\.SW\b":     '"sw"',
        r"\btk\.SE\b":     '"se"',
    }
    _changed = False
    for _pattern, _replacement in _TK_CONST_MAP.items():
        new_src, count = re.subn(_pattern, _replacement, src)
        if count:
            src = new_src
            _changed = True
            print(f"[patch_71]   {_pattern} → {_replacement} ({count}x corrigido)")
    if _changed:
        print("[patch_71] Constantes tk.* inválidas corrigidas.")

    # ------------------------------------------------------------------
    # 1. self._db_path no __init__
    # ------------------------------------------------------------------
    if "self._db_path" not in src:
        match = re.search(
            r"([ \t]+self\._repo\s*=\s*StructuresRepository\(db_path\))",
            src,
        )
        if not match:
            errors.append(
                "PANEL: âncora 'self._repo = StructuresRepository(db_path)' não encontrada"
            )
        else:
            indent = re.match(r"([ \t]+)", match.group(1)).group(1)
            insertion = f"{indent}self._db_path               = db_path\n"
            src = src.replace(
                match.group(1),
                insertion + match.group(1),
                1,
            )

    # ------------------------------------------------------------------
    # 2. Label de status em _build_buttons
    # ------------------------------------------------------------------
    if "_status_label_var" not in src:
        match = re.search(
            r'([ \t]+for label, cmd in actions:.*?\.pack\(\s*\n'
            r'(?:[ \t]+side=["\']left["\'].*?\n)?'
            r'[ \t]+\)\s*\n)',
            src,
            re.DOTALL,
        )
        if not match:
            match = re.search(
                r'([ \t]+\.pack\(\s*\n[ \t]+side=["\']left["\'],\s*padx=2,\s*pady=2\s*\n[ \t]+\)\s*\n)',
                src,
            )

        if not match:
            errors.append(
                "PANEL: âncora do for-loop de botões não encontrada para inserir label de status"
            )
        else:
            end = match.end()
            indent = "        "
            label_block = (
                f"\n"
                f"{indent}# Label de feedback de status no rodapé do painel\n"
                f"{indent}self._status_label_var = tk.StringVar(value=\"\")\n"
                f"{indent}ttk.Label(\n"
                f"{indent}    self,\n"
                f"{indent}    textvariable=self._status_label_var,\n"
                f"{indent}    foreground=\"#555555\",\n"
                f"{indent}    anchor=\"w\",\n"
                f"{indent}).pack(fill=\"x\", padx=4, pady=(0, 2))\n"
            )
            src = src[:end] + label_block + src[end:]

    # ------------------------------------------------------------------
    # 3. _set_status chamado em _cmd_archive
    # ------------------------------------------------------------------
    if "_set_status" not in src:
        pattern = re.compile(
            r'([ \t]+)(try:\s*\n'
            r'[ \t]+self\._repo\.archive_structure\(sid\)\s*\n'
            r'[ \t]+self\._on_structure_selected\(None\)\s*\n'
            r'[ \t]+self\.load\(\)\s*\n)'
            r'([ \t]+except\s+Exception\s+as\s+exc:\s*\n)'
            r'([ \t]+messagebox\.showerror\([^)]+\))',
            re.MULTILINE,
        )
        m = pattern.search(src)
        if not m:
            errors.append(
                "PANEL: bloco try/except de _cmd_archive não encontrado pelo regex"
            )
        else:
            indent_base = m.group(1)
            new = (
                f"{indent_base}try:\n"
                f"{indent_base}    self._repo.archive_structure(sid)\n"
                f"{indent_base}    self._on_structure_selected(None)\n"
                f"{indent_base}    self.load()\n"
                f"{indent_base}    self._set_status(f\"Estrutura '{{name}}' arquivada.\")\n"
                f"{indent_base}except Exception as exc:\n"
                f"{indent_base}    messagebox.showerror(\"Arquivar\", f\"Erro ao arquivar: {{exc}}\")\n"
                f"{indent_base}    self._set_status(f\"Erro ao arquivar: {{exc}}\")"
            )
            src = src[:m.start()] + new + src[m.end():]

    # ------------------------------------------------------------------
    # 4. Método _set_status no final da classe
    # ------------------------------------------------------------------
    if "def _set_status" not in src:
        set_status_block = (
            "\n"
            "    # -------------------------------------------------------\n"
            "    # Feedback de status\n"
            "    # -------------------------------------------------------\n"
            "\n"
            "    def _set_status(self, msg: str) -> None:\n"
            "        \"\"\"Atualiza o label de feedback no rodapé do painel.\"\"\"\n"
            "        try:\n"
            "            self._status_label_var.set(msg)\n"
            "        except Exception:\n"
            "            pass\n"
        )
        src = src.rstrip() + "\n" + set_status_block

    if errors:
        return errors

    if not dry_run:
        _bak(STRUCTURES_PANEL)
        _write(STRUCTURES_PANEL, src)
        print("[patch_71] structures_list_panel.py atualizado.")
    else:
        print("[patch_71][dry-run] structures_list_panel.py -- sem escrita.")

    return []


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run(dry_run: bool = False) -> int:
    all_errors: list[str] = []

    all_errors += patch_structures_list_panel(dry_run=dry_run)

    if all_errors:
        print("\n[patch_71] ERROS encontrados:")
        for e in all_errors:
            print(f"  - {e}")
        return 1

    print("\n[patch_71] Concluido sem erros.")
    return 0


if __name__ == "__main__":
    import sys
    dry = "--dry-run" in sys.argv
    sys.exit(run(dry_run=dry))
