from __future__ import annotations

import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
EVID_DIR = ROOT / "FRENTE_BD_UNICO_APPDB" / "evidencias"
BACKUP_DIR = ROOT / "FRENTE_BD_UNICO_APPDB" / "backups_phase1f"
OUT = EVID_DIR / "41_phase1f_semantic_cleanup_appdb_labels.txt"

EXCLUDE_DIR_NAMES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "dados",
    "backups",
    "backups_phase1f",
}

EXCLUDE_PATH_PARTS = {
    "FRENTE_BD_UNICO_APPDB/evidencias",
    "FRENTE_BD_UNICO_APPDB/backups",
    "FRENTE_BD_UNICO_APPDB/backups_phase1f",
}

EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
}

REPLACEMENTS = [
    ("app.db", "app.db"),
    ("App DB", "App DB"),
    ("app DB", "app DB"),
    ("APP DB", "APP DB"),
    ("Banco app", "Banco app"),
    ("banco app", "banco app"),
    ("dados consolidados", "dados consolidados"),
    ("snapshots consolidados", "snapshots consolidados"),
]


PYTEST_CMD = [
    sys.executable,
    "-m",
    "pytest",
    "ATT/tests/test_ui_data_migration.py",
    "ATT/tests/test_structure_editor_integration.py",
    "ATT/tests/test_derived_service.py",
    "-q",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_DIR_NAMES:
        return True

    rp = rel(path)
    for token in EXCLUDE_PATH_PARTS:
        if rp.startswith(token):
            return True

    return False


def iter_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if should_skip(path):
            continue
        if path.suffix.lower() not in EXTENSIONS:
            continue
        files.append(path)
    return sorted(files)


def run_cmd(cmd: list[str], fh, title: str) -> int:
    print(file=fh)
    print(f"===== {title} =====", file=fh)
    print("cmd:", " ".join(cmd), file=fh)

    proc = subprocess.run(
        cmd,
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    print(proc.stdout, file=fh)
    print(f"returncode: {proc.returncode}", file=fh)
    return proc.returncode


def restore(backups: dict[Path, Path], fh) -> None:
    print(file=fh)
    print("===== RESTAURANDO ALTERACOES FASE 1F-A =====", file=fh)

    for original, backup in backups.items():
        if backup.exists():
            shutil.copy2(backup, original)
            print(f"[OK] restaurado: {rel(original)}", file=fh)


def main() -> int:
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_backup_dir = BACKUP_DIR / f"phase1f_a_{stamp}"
    run_backup_dir.mkdir(parents=True, exist_ok=True)

    changed: list[Path] = []
    backups: dict[Path, Path] = {}

    with OUT.open("w", encoding="utf-8") as fh:
        print("===== DATA =====", file=fh)
        print(datetime.now().isoformat(sep=" ", timespec="seconds"), file=fh)
        print(file=fh)

        print("===== OBJETIVO =====", file=fh)
        print("Limpeza segura de textos/caminhos literais app.db -> app.db.", file=fh)
        print("Nao renomeia APIs, modulos ou parametros derived_* nesta subfase.", file=fh)
        print(file=fh)

        print("===== ALTERACOES =====", file=fh)

        for path in iter_files():
            try:
                original = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            new = original
            for old, repl in REPLACEMENTS:
                new = new.replace(old, repl)

            if new != original:
                backup = run_backup_dir / rel(path)
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, backup)
                backups[path] = backup

                path.write_text(new, encoding="utf-8")
                changed.append(path)

                print(f"[M] {rel(path)}", file=fh)

        if not changed:
            print("[INFO] Nenhum arquivo alterado.", file=fh)

        print(file=fh)
        print("changed_count:", len(changed), file=fh)

        compile_rc = run_cmd(
            [sys.executable, "-m", "compileall", "-q", "ATT", "UI", "db", "domain", "repositories", "scripts", "services"],
            fh,
            "PY_COMPILE / COMPILEALL POS-LIMPEZA",
        )

        pytest_rc = run_cmd(PYTEST_CMD, fh, "PYTEST DIRECIONADO POS-LIMPEZA")

        print(file=fh)
        print("===== DECISAO =====", file=fh)

        if compile_rc == 0 and pytest_rc == 0:
            print("[OK] Fase 1F-A aprovada.", file=fh)
            print("[OK] Limpeza semantica literal app.db -> app.db preservada.", file=fh)
            print(f"[OK] backups locais em: {run_backup_dir}", file=fh)
            return 0

        print("[ERRO] Fase 1F-A falhou. Restaurando arquivos alterados.", file=fh)
        restore(backups, fh)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
