# ATT/patches/patch_57b_fix_future_import_order.py
"""
patch_57b -- corrige em lote o SyntaxError:
  "from __future__ imports must occur at the beginning of the file"

Causa: em vários serviços gerados pelo patch_57 (e anteriores), a linha
  from src.domain.refs.structure_ref import StructureRef
foi inserida ANTES de
  from __future__ import annotations
o que é SyntaxError no Python runtime.

Fix: move 'from __future__ import annotations' para ANTES de qualquer
outro import, preservando shebang, encoding e docstrings no topo.

Execução:
  python ATT/patches/patch_57b_fix_future_import_order.py           # dry-run
  python ATT/patches/patch_57b_fix_future_import_order.py --apply   # aplica
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).parent.parent.parent

SKIP_DIRS = {
    ".git", "__pycache__", ".venv", "venv", "env",
    "node_modules", ".mypy_cache", ".pytest_cache",
    "dist", "build", ".eggs", "backups",
    "ATT",   # arquivos de teste/patch não precisam de correção
}

# Padrão exato que causa o SyntaxError
FUTURE_LINE = "from __future__ import annotations\n"
FUTURE_PATTERN = re.compile(r"^from __future__ import annotations\s*$", re.MULTILINE)


def _needs_fix(source: str) -> bool:
    """
    Retorna True se 'from __future__ import annotations' existe no arquivo
    mas NÃO é a primeira instrução de código real (não é shebang/docstring/comentário).
    """
    if "from __future__ import annotations" not in source:
        return False

    lines = source.splitlines(keepends=True)
    future_idx = None
    first_code_idx = None

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Pula linhas vazias, comentários e shebang
        if not stripped or stripped.startswith("#"):
            continue

        # Pula docstrings de módulo (abertura e fechamento)
        if stripped.startswith('"""') or stripped.startswith("'''"):
            # Conta como não-código para fins de __future__
            continue

        # Primeira linha de código real encontrada
        if first_code_idx is None:
            first_code_idx = i

        if "from __future__ import annotations" in line:
            future_idx = i
            break

    if future_idx is None:
        return False

    # Problema: __future__ não é a primeira linha de código
    return future_idx != first_code_idx


def fix_source(source: str) -> str:
    """
    Remove 'from __future__ import annotations' de onde está
    e insere logo após o bloco de cabeçalho (shebang + comentários + docstring).
    """
    lines = source.splitlines(keepends=True)

    # 1. Remove a linha __future__ existente (pode haver duplicata -- remove todas)
    cleaned = [ln for ln in lines if "from __future__ import annotations" not in ln]

    # 2. Determina onde inserir: após shebang + comentários de encoding + docstring
    insert_at = 0
    in_docstring = False
    docstring_char = None

    for i, line in enumerate(cleaned):
        stripped = line.strip()

        # Shebang ou comentário de encoding/copyright no topo
        if stripped.startswith("#") and i < 5:
            insert_at = i + 1
            continue

        # Início de docstring de módulo
        if not in_docstring and (stripped.startswith('"""') or stripped.startswith("'''")):
            char = '"""' if stripped.startswith('"""') else "'''"
            # Docstring de uma linha só
            if stripped.count(char) >= 2 and len(stripped) > 3:
                insert_at = i + 1
                break
            # Docstring multilinha: precisa encontrar o fechamento
            in_docstring = True
            docstring_char = char
            insert_at = i + 1
            continue

        if in_docstring:
            insert_at = i + 1
            if docstring_char and docstring_char in stripped:
                in_docstring = False
                break
            continue

        # Primeira linha que não é cabeçalho -- insere aqui
        break

    # 3. Insere __future__ na posição correta
    # Garante linha em branco separadora se necessário
    result = cleaned[:insert_at] + [FUTURE_LINE] + cleaned[insert_at:]

    # 4. Remove linha em branco dupla acidental antes do primeiro import
    # (apenas normaliza -- não é obrigatório)
    return "".join(result)


def scan_and_fix(root: Path, apply: bool) -> None:
    targets: list[tuple[Path, str]] = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            if not fname.endswith(".py"):
                continue
            fpath = Path(dirpath) / fname
            try:
                src = fpath.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue

            if _needs_fix(src):
                targets.append((fpath, src))

    if not targets:
        print("[OK] Nenhum arquivo com __future__ fora de ordem encontrado.")
        return

    prefix = "[DRY-RUN] " if not apply else ""
    print(f"{prefix}Arquivos com SyntaxError de __future__ ({len(targets)}):")
    print("-" * 60)

    fixed = 0
    errors = 0

    for fpath, src in sorted(targets, key=lambda x: x[0]):
        rel = fpath.relative_to(root)
        if not apply:
            print(f"  CORRIGIR: {rel}")
        else:
            try:
                fixed_src = fix_source(src)
                # Backup antes de sobrescrever
                shutil.copy2(fpath, fpath.with_suffix(fpath.suffix + ".bak57b"))
                fpath.write_text(fixed_src, encoding="utf-8")
                print(f"  [OK] corrigido: {rel}")
                fixed += 1
            except Exception as exc:
                print(f"  [ERRO] {rel}: {exc}")
                errors += 1

    print("-" * 60)
    if not apply:
        print(f"[DRY-RUN] {len(targets)} arquivo(s) seriam corrigidos.")
        print(">  Execute com --apply para efetivar.")
        print(">  Depois: python ATT/patches/patch_57b_cleanup_bak57b.py --apply")
    else:
        print(f"[OK] {fixed} corrigido(s) | {errors} erro(s).")
        if errors:
            import sys
            sys.exit(1)
        print(">  Próximo: python -m pytest ATT/tests/ -v --tb=short 2>&1 | tail -30")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Fix em lote: __future__ fora de ordem")
    p.add_argument("--apply", action="store_true", help="Aplica correções (default: dry-run)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    scan_and_fix(ROOT, apply=args.apply)


if __name__ == "__main__":
    main()
