#!/usr/bin/env python3
"""
Audita scripts/ para encontrar:
- arquivos referenciados (usados) no repo
- arquivos "órfãos" (sem referência) => candidatos a remoção
- backups (.bak), __pycache__, duplicados óbvios, etc.

Depois pode remover com --apply.

Uso:
  python scripts/audit_and_cleanup_scripts.py --dry-run
  python scripts/audit_and_cleanup_scripts.py --apply --remove-orphans
  python scripts/audit_and_cleanup_scripts.py --apply --remove-orphans --remove-bak --remove-pycache
"""
from __future__ import annotations

from pathlib import Path
import argparse
import re
import shutil
from collections import defaultdict

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"

TEXT_EXTS = {".py", ".sh", ".bash", ".zsh", ".md", ".txt", ".yml", ".yaml", ".toml", ".ini", ".cfg", ".json", ".make", ""}
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache", "dist", "build"}

def iter_text_files(root: Path):
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        # pula pastas ignoradas
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in TEXT_EXTS:
            yield p

def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        try:
            return p.read_text(errors="ignore")
        except Exception:
            return ""

def script_identities(script_path: Path) -> set[str]:
    """
    Padrões de referência comuns:
    - scripts/foo.py
    - python scripts/foo.py
    - ./scripts/foo.sh
    - import scripts.foo / from scripts.foo import ...
    """
    rel = script_path.relative_to(REPO_ROOT).as_posix()
    name = script_path.name
    stem = script_path.stem
    ids = {rel, f"./{rel}", name}

    if script_path.suffix == ".py":
        ids |= {
            f"python {rel}",
            f"python3 {rel}",
            f"py {rel}",
            f"python ./{rel}",
            f"python3 ./{rel}",
            f"import scripts.{stem}",
            f"from scripts.{stem} import",
        }
    if script_path.suffix in {".sh", ".bash", ".zsh"}:
        ids |= {f"bash {rel}", f"sh {rel}", f"./{rel}"}
    return ids

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Remove de verdade.")
    ap.add_argument("--dry-run", action="store_true", help="Força dry-run (padrão se --apply não for passado).")

    ap.add_argument("--remove-orphans", action="store_true", help="Remove scripts órfãos (sem referência detectada).")
    ap.add_argument("--remove-bak", action="store_true", help="Remove arquivos .bak.")
    ap.add_argument("--remove-pycache", action="store_true", help="Remove diretórios __pycache__ dentro de scripts/.")
    ap.add_argument("--remove-empty-init", action="store_true", help="Remove scripts/__init__.py se estiver vazio.")

    ap.add_argument("--keep", nargs="*", default=[], help="Lista de arquivos em scripts/ para sempre manter (ex: run_derived_pipeline.py).")
    args = ap.parse_args()

    dry = args.dry_run or (not args.apply)

    if not SCRIPTS_DIR.exists():
        print("[ERROR] scripts/ não existe.")
        return 2

    scripts = sorted([p for p in SCRIPTS_DIR.iterdir() if p.is_file()])
    keep_set = {k.strip() for k in args.keep}

    # index de referências
    refs = defaultdict(set)  # script -> set(files_that_reference_it)
    all_text_files = list(iter_text_files(REPO_ROOT))
    contents_cache = {}

    for tf in all_text_files:
        contents_cache[tf] = read_text(tf)

    for s in scripts:
        ids = script_identities(s)
        for tf in all_text_files:
            if tf == s:
                continue
            txt = contents_cache[tf]
            if not txt:
                continue
            # match simples por substring (rápido e eficaz)
            if any(i in txt for i in ids):
                refs[s.name].add(tf.relative_to(REPO_ROOT).as_posix())

    # classificar
    used = []
    orphan = []
    for s in scripts:
        if s.name in keep_set:
            used.append(s)
            continue
        if refs.get(s.name):
            used.append(s)
        else:
            orphan.append(s)

    # sugerir candidatos óbvios
    bak_files = sorted(SCRIPTS_DIR.glob("*.bak"))
    pycache_dirs = [p for p in (SCRIPTS_DIR / "__pycache__",) if p.exists()]

    empty_init = SCRIPTS_DIR / "__init__.py"
    init_is_empty = empty_init.exists() and empty_init.is_file() and empty_init.stat().st_size == 0

    print("=== AUDIT scripts/ ===")
    print("Repo:", REPO_ROOT)
    print("Mode:", "DRY-RUN" if dry else "APPLY")
    print()

    print(f"[INFO] Scripts encontrados: {len(scripts)}")
    print(f"[INFO] Usados (referenciados ou keep): {len(used)}")
    print(f"[INFO] Órfãos (sem referência detectada): {len(orphan)}")
    print()

    if used:
        print("USADOS (detecção por referência):")
        for s in used:
            where = sorted(refs.get(s.name, []))
            if s.name in keep_set:
                print(f" - {s.name} (KEEP manual)")
            else:
                print(f" - {s.name} (refs: {len(where)})")
        print()

    if orphan:
        print("ÓRFÃOS (candidatos a remoção, revise antes):")
        for s in orphan:
            print(" -", s.name)
        print()

    if bak_files:
        print("BACKUPS .bak:")
        for b in bak_files:
            print(" -", b.name)
        print()

    if pycache_dirs:
        print("__pycache__ dirs:")
        for d in pycache_dirs:
            print(" -", d.relative_to(REPO_ROOT).as_posix())
        print()

    if init_is_empty:
        print("[INFO] scripts/__init__.py está vazio (0 bytes).")
        print()

    # montar plano de remoção
    to_remove_files: list[Path] = []
    to_remove_dirs: list[Path] = []

    if args.remove_orphans:
        to_remove_files.extend(orphan)

    if args.remove_bak:
        to_remove_files.extend(bak_files)

    if args.remove_pycache:
        for d in pycache_dirs:
            to_remove_dirs.append(d)

    if args.remove_empty_init and init_is_empty:
        to_remove_files.append(empty_init)

    # dedupe
    seen = set()
    unique_files = []
    for f in to_remove_files:
        if f.resolve() not in seen:
            seen.add(f.resolve())
            unique_files.append(f)

    if unique_files or to_remove_dirs:
        print("PLANO DE REMOÇÃO:")
        for f in unique_files:
            print(" - file:", f.relative_to(REPO_ROOT).as_posix())
        for d in to_remove_dirs:
            print(" - dir :", d.relative_to(REPO_ROOT).as_posix())
        print()
    else:
        print("[INFO] Nenhuma remoção solicitada (passe flags).")
        print("      Sugestão: --remove-orphans --remove-bak --remove-pycache --remove-empty-init")
        return 0

    if dry:
        print("[INFO] Dry-run: nada foi removido.")
        return 0

    # aplicar
    for f in unique_files:
        try:
            f.unlink()
            print("[OK] Removed file:", f.relative_to(REPO_ROOT).as_posix())
        except Exception as e:
            print("[ERROR] Failed removing file:", f, "->", e)

    for d in to_remove_dirs:
        try:
            shutil.rmtree(d)
            print("[OK] Removed dir:", d.relative_to(REPO_ROOT).as_posix())
        except Exception as e:
            print("[ERROR] Failed removing dir:", d, "->", e)

    print("\n[OK] Cleanup concluído.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
