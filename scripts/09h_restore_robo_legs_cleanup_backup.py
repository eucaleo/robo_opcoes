from __future__ import annotations

import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TARGET = PROJECT_ROOT / "repositories" / "robo_legs_repository.py"
BACKUP = PROJECT_ROOT / "repositories" / "robo_legs_repository.py.cleanup.bak"


def fail(msg: str) -> int:
    print(f"ERRO: {msg}")
    return 1


def main() -> int:
    print("== RESTORE ROBO LEGS CLEANUP BACKUP ==")
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"TARGET: {TARGET}")
    print(f"BACKUP: {BACKUP}")

    if not BACKUP.exists():
        return fail(f"Backup não encontrado: {BACKUP}")

    shutil.copy2(BACKUP, TARGET)
    print("- Arquivo restaurado com sucesso a partir do backup do cleanup.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
