"""
patch_61 -- Remove scripts tmp_* residuais do patch_53b

Arquivos-alvo:
    scripts/tmp_fix_todos_patch53b.py
    scripts/tmp_show_todos_patch53.py
    scripts/tmp_verify_patch53b.py

Criterio de aceite:
    - zero arquivos tmp_*.py no diretorio scripts/
    - PATCHES.md atualizado
    - commit registrado
"""

from __future__ import annotations

import sys
import os
import shutil
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuracao
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = ROOT / "scripts"
BAK_DIR = ROOT / "ATT" / "BAK"
PATCHES_MD = ROOT / "ATT" / "PATCHES.md"

TMP_TARGETS = [
    "tmp_fix_todos_patch53b.py",
    "tmp_show_todos_patch53.py",
    "tmp_verify_patch53b.py",
]

DRY_RUN = "--dry-run" in sys.argv


def _log(msg: str) -> None:
    prefix = "[DRY-RUN]" if DRY_RUN else "[patch_61]"
    print(f"{prefix} {msg}")


def backup_file(src: Path) -> Path:
    BAK_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = BAK_DIR / f"{src.name}.bak_p61_{ts}"
    if not DRY_RUN:
        shutil.copy2(src, dst)
    _log(f"backup: {src.name} -> ATT/BAK/{dst.name}")
    return dst


def remove_tmp_scripts() -> list[str]:
    removed = []
    for name in TMP_TARGETS:
        path = SCRIPTS_DIR / name
        if path.exists():
            backup_file(path)
            if not DRY_RUN:
                path.unlink()
            _log(f"removido: scripts/{name}")
            removed.append(name)
        else:
            _log(f"nao encontrado (ja removido?): scripts/{name}")
    return removed


def verify_no_tmp_remaining() -> bool:
    remaining = list(SCRIPTS_DIR.glob("tmp_*.py"))
    if remaining:
        _log(f"ATENCAO: ainda existem tmp_*.py: {[f.name for f in remaining]}")
        return False
    _log("verificacao OK: zero tmp_*.py em scripts/")
    return True


def update_patches_md(removed: list[str]) -> None:
    if DRY_RUN:
        _log("PATCHES.md: sem alteracao (dry-run)")
        return
    if not PATCHES_MD.exists():
        _log("PATCHES.md nao encontrado, pulando atualizacao")
        return
    ts = datetime.now().strftime("%Y-%m-%d")
    entry = (
        f"\n## patch_61 -- {ts}\n"
        f"chore: remove tmp scripts residuais do patch_53b\n"
        f"Arquivos removidos: {', '.join(removed) if removed else 'nenhum (ja ausentes)'}\n"
    )
    with open(PATCHES_MD, "a", encoding="utf-8") as fh:
        fh.write(entry)
    _log("PATCHES.md atualizado")


def main() -> int:
    _log("iniciando patch_61")
    _log(f"ROOT: {ROOT}")

    removed = remove_tmp_scripts()
    ok = verify_no_tmp_remaining()
    update_patches_md(removed)

    if not ok:
        _log("FALHOU: ainda existem arquivos tmp_* apos remocao")
        return 1

    _log(f"patch_61 concluido -- {len(removed)} arquivo(s) removido(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
