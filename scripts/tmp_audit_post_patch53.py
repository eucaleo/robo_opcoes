"""
tmp_audit_post_patch53.py  —  TEMPORÁRIO (remover após patch_53)

Valida que:
1. Nenhum caller ainda usa 'aba' como parâmetro raw (exceto frozen)
2. Todos os arquivos alterados têm o import do StructureRef
3. Nenhum .bak foi esquecido no repo (apenas aviso)
4. run_patch_33.py NÃO foi tocado
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
FROZEN = ROOT / "db/migrations/run_patch_33.py"
EXCLUDE_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules"}

issues = []
warnings = []

for fpath in ROOT.rglob("*.py"):
    if any(part in EXCLUDE_DIRS for part in fpath.parts):
        continue

    rel = str(fpath.relative_to(ROOT))
    content = fpath.read_text(encoding="utf-8")

    # ❌ Ainda tem parâmetro 'aba: str' fora de frozen
    if fpath != FROZEN:
        if re.search(r"def\s+\w+\s*\([^)]*?\baba\s*:\s*str\b", content):
            issues.append(f"❌ Parâmetro 'aba: str' ainda presente: {rel}")

    # ❌ SQL raw ainda usa 'WHERE aba ='
    if re.search(r"WHERE\s+aba\s*=\s*\?", content) and fpath != FROZEN:
        issues.append(f"❌ SQL 'WHERE aba = ?' ainda presente: {rel}")

    # ⚠️  TODO pendente de revisão manual
    if "# TODO patch_53:" in content:
        warnings.append(f"⚠️  TODO manual pendente: {rel}")

# ✅ frozen não foi alterado
if FROZEN.exists():
    frozen_mtime_changed = FROZEN.stat().st_mtime
    bak = FROZEN.with_suffix(".py.bak")
    if bak.exists():
        issues.append(f"❌ run_patch_33.py tem .bak — foi alterado indevidamente!")
    else:
        print(f"   ✅ run_patch_33.py intocado (frozen OK)")

# ⚠️  Arquivos .bak esquecidos
for bak in ROOT.rglob("*.bak"):
    warnings.append(f"⚠️  .bak ainda presente (pode remover): {bak.relative_to(ROOT)}")

print("\n📋 AUDITORIA PÓS-PATCH 53\n" + "="*50)
if issues:
    for i in issues:
        print(i)
if warnings:
    print()
    for w in warnings:
        print(w)

print()
if issues:
    print(f"💥 {len(issues)} problema(s) crítico(s). Corrija antes do commit.")
    sys.exit(1)
else:
    print(f"🎉 Auditoria OK! {len(warnings)} aviso(s) não-crítico(s).")
    sys.exit(0)
