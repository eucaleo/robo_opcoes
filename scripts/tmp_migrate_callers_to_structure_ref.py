"""
tmp_migrate_callers_to_structure_ref.py  —  TEMPORÁRIO (remover após patch_53)
VERSÃO 2 — com exclusões corretas
"""

import re
import shutil
import sys
from pathlib import Path

ROOT    = Path(__file__).parent.parent
DRY_RUN = "--dry-run" in sys.argv

# ------------------------------------------------------------------
# Arquivos/diretórios que NUNCA devem ser tocados
# ------------------------------------------------------------------
FROZEN_FILES = {
    "db/migrations/run_patch_33.py",
    "src/domain/refs/structure_ref.py",   # o próprio StructureRef
}

FROZEN_DIRS = {
    "ATT",          # patches e testes históricos — frozen
    "scripts",      # scripts temporários e utilitários — revisão manual
    ".git",
    "__pycache__",
    ".venv",
    "venv",
}

# ------------------------------------------------------------------
# Apenas estes diretórios de produção serão migrados
# ------------------------------------------------------------------
ALLOWED_ROOTS = {
    "db",
    "domain",
    "repositories",
    "services",
    "UI",
    "utils",
}

RULES = [
    (
        r"(def\s+\w+\s*\([^)]*?)\baba\s*:\s*str\b",
        r"\1ref: StructureRef",
        "parâmetro 'aba: str' → 'ref: StructureRef'",
    ),
    (
        r"WHERE\s+aba\s*=\s*\?",
        r"WHERE {ref.db_column()} = ?",
        "SQL WHERE aba = ? → WHERE {ref.db_column()} = ?",
    ),
    (
        r"\bparams\s*=\s*\[([^\]]*?)\baba\b([^\]]*?)\]",
        r"params=[\1ref.db_key()\2]",
        "params list: aba → ref.db_key()",
    ),
    (
        r"\bself\.aba\b(\s*=\s*)(?!None)",
        r"self.ref\1",
        "self.aba → self.ref",
    ),
    (
        r"(\.get\(['\"]aba['\"]|\[['\"]aba['\"]\])",
        r"\1  # TODO patch_53: converter para StructureRef",
        "marcação TODO para revisão manual (dict access)",
    ),
]

IMPORT_LINE   = "from src.domain.refs.structure_ref import StructureRef\n"
IMPORT_ANCHOR = re.compile(r"^(from\s+|import\s+)", re.MULTILINE)

def inject_import(content: str) -> str:
    if "from src.domain.refs.structure_ref import StructureRef" in content:
        return content
    match = IMPORT_ANCHOR.search(content)
    if match:
        pos = match.start()
        return content[:pos] + IMPORT_LINE + content[pos:]
    return IMPORT_LINE + content

def is_allowed(fpath: Path) -> tuple[bool, str]:
    """Retorna (permitido, motivo_se_negado)."""
    rel = fpath.relative_to(ROOT)
    parts = rel.parts

    # frozen por nome exato
    rel_str = str(rel).replace("\\", "/")
    if rel_str in FROZEN_FILES:
        return False, "frozen (arquivo protegido)"

    # frozen por diretório
    if parts[0] in FROZEN_DIRS:
        return False, f"frozen (diretório '{parts[0]}')"

    # somente allowed roots
    if parts[0] not in ALLOWED_ROOTS:
        return False, f"fora do escopo ('{parts[0]}' não está em ALLOWED_ROOTS)"

    return True, ""

def migrate_file(fpath: Path) -> tuple[int, list[str]]:
    allowed, reason = is_allowed(fpath)
    if not allowed:
        return 0, [f"  ⛔ SKIPPED ({reason}): {fpath.relative_to(ROOT)}"]

    original = fpath.read_text(encoding="utf-8")
    content  = original
    log      = []
    total    = 0

    for pattern, repl, desc in RULES:
        new_content, n = re.subn(pattern, repl, content, flags=re.MULTILINE)
        if n > 0:
            log.append(f"  ✏️  {n}x [{desc}]")
            total += n
            content = new_content

    if total > 0:
        content = inject_import(content)
        if not DRY_RUN:
            shutil.copy2(fpath, fpath.with_suffix(fpath.suffix + ".bak"))
            fpath.write_text(content, encoding="utf-8")
        label = "(dry-run)" if DRY_RUN else "(alterado — .bak criado)"
        log.insert(0, f"\n📄 {fpath.relative_to(ROOT)} {label}")

    return total, log

# ------------------------------------------------------------------
# Coleta todos os .py nas ALLOWED_ROOTS
# ------------------------------------------------------------------
files_to_migrate = []
for allowed_root in ALLOWED_ROOTS:
    target = ROOT / allowed_root
    if target.exists():
        files_to_migrate.extend(sorted(target.rglob("*.py")))

mode = "🔍 DRY-RUN" if DRY_RUN else "🔧 MIGRAÇÃO REAL"
print(f"\n{mode} — {len(files_to_migrate)} arquivos no escopo\n")
print(f"Escopo: {sorted(ALLOWED_ROOTS)}\n")

total_changes  = 0
skipped        = 0
files_changed  = 0

for fpath in files_to_migrate:
    n, logs = migrate_file(fpath)
    if n > 0:
        total_changes += n
        files_changed += 1
        for l in logs:
            print(l)
    elif any("SKIPPED" in l for l in logs):
        skipped += 1

print(f"\n{'─'*60}")
print(f"📁 Arquivos no escopo : {len(files_to_migrate)}")
print(f"✏️  Arquivos alterados : {files_changed}")
print(f"⛔ Arquivos pulados   : {skipped}")
print(f"🔢 Total substituições: {total_changes}")
if DRY_RUN:
    print("\n💡 Aprovado? Rode SEM --dry-run para aplicar.")
else:
    print("\n✅ Migração aplicada. Rode tmp_audit_post_patch53.py para validar.")
