# ATT/patches/patch_57_cleanup.py
"""
patch_57 -- limpeza de arquivos temporarios e backups residuais.

Remove:
  - scripts/tmp_show_todos_patch53.py
  - scripts/tmp_fix_todos_patch53b.py
  - scripts/tmp_verify_patch53b.py
  - patches/backups/patch_56/  (6 arquivos .py)
  - ATT/patches/backups/patch_56/  (2 arquivos .py)
  - Qualquer .bak ou .bak_emoji em services/, db/, UI/

Execucao:
  python ATT/patches/patch_57_cleanup.py           # dry-run
  python ATT/patches/patch_57_cleanup.py --apply   # aplica remocoes
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Limpeza de temporarios do patch_57")
    p.add_argument("--apply", action="store_true", help="Aplica remocoes (default: dry-run)")
    return p.parse_args()


def collect_targets(root: Path) -> list[Path]:
    targets: list[Path] = []

    # 1. scripts tmp_* do patch_53
    for name in [
        "tmp_show_todos_patch53.py",
        "tmp_fix_todos_patch53b.py",
        "tmp_verify_patch53b.py",
    ]:
        p = root / "scripts" / name
        if p.exists():
            targets.append(p)

    # 2. backups .py do patch_56
    for bak_dir in [
        root / "patches"     / "backups" / "patch_56",
        root / "ATT" / "patches" / "backups" / "patch_56",
    ]:
        if bak_dir.exists():
            for f in bak_dir.glob("*.py"):
                targets.append(f)

    # 3. arquivos .bak e .bak_emoji em services/, db/, UI/
    for subdir in ["services", "db", "UI"]:
        for dirpath, _, filenames in os.walk(root / subdir):
            for fname in filenames:
                if fname.endswith(".bak") or fname.endswith(".bak_emoji"):
                    targets.append(Path(dirpath) / fname)

    return targets


def main() -> None:
    args    = parse_args()
    dry_run = not args.apply
    targets = collect_targets(ROOT)

    if not targets:
        print("[OK] Nenhum arquivo temporario encontrado. Nada a remover.")
        return

    print(f"{'[DRY-RUN] ' if dry_run else ''}Arquivos a remover ({len(targets)}):")
    print("-" * 60)

    removed = 0
    errors  = 0

    for path in sorted(targets):
        rel = path.relative_to(ROOT)
        if dry_run:
            print(f"  REMOVER: {rel}")
        else:
            try:
                path.unlink()
                print(f"  [OK] removido: {rel}")
                removed += 1
            except OSError as exc:
                print(f"  [ERRO] {rel}: {exc}")
                errors += 1

    print("-" * 60)
    if dry_run:
        print(f"[DRY-RUN] {len(targets)} arquivo(s) seriam removidos.")
        print(">  Execute com --apply para efetivar.")
    else:
        print(f"[OK] {removed} removido(s) | {errors} erro(s).")
        if errors:
            sys.exit(1)


if __name__ == "__main__":
    main()
