# ATT/patches/patch_57b_cleanup_bak57b.py
"""
Remove os backups .bak57b criados pelo patch_57b_fix_future_import_order.py.
Executar APENAS após confirmar que os testes passam.

  python ATT/patches/patch_57b_cleanup_bak57b.py           # dry-run
  python ATT/patches/patch_57b_cleanup_bak57b.py --apply   # remove
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent

SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "env",
             "node_modules", "dist", "build"}


def collect(root: Path) -> list[Path]:
    found: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            if fname.endswith(".bak57b"):
                found.append(Path(dirpath) / fname)
    return found


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args  = parser.parse_args()
    files = collect(ROOT)

    if not files:
        print("[OK] Nenhum .bak57b encontrado.")
        return

    print(f"{'[DRY-RUN] ' if not args.apply else ''}Backups .bak57b ({len(files)}):")
    for f in sorted(files):
        rel = f.relative_to(ROOT)
        if not args.apply:
            print(f"  REMOVER: {rel}")
        else:
            f.unlink()
            print(f"  [OK] removido: {rel}")

    if not args.apply:
        print(f"\n[DRY-RUN] {len(files)} arquivo(s). Execute com --apply para remover.")
    else:
        print(f"\n[OK] {len(files)} backup(s) removido(s).")


if __name__ == "__main__":
    main()
