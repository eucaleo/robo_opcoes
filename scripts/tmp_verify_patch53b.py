"""
tmp_verify_patch53b.py — TEMPORÁRIO
Verifica: sem TODO patch_53 residual, sem SyntaxError, sem .bak sujo.
"""
import ast
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

TARGETS = [
    "db/derived_repo.py",
    "UI/models/ui_data.py",
    "UI/components/decisions_grid.py",
    "UI/components/payoff_chart.py",
    "repositories/market_snapshot_repository.py",
    "domain/payoff_features.py",
    "utils/leg_normalizers.py",
]

errors   = []
warnings = []
ok       = []

print("🔍 VERIFICAÇÃO PÓS-PATCH 53b")
print("=" * 60)

for rel in TARGETS:
    fpath = ROOT / rel
    if not fpath.exists():
        errors.append(f"❌ NÃO ENCONTRADO: {rel}")
        continue

    src = fpath.read_text(encoding="utf-8")

    # 1. SyntaxError
    try:
        ast.parse(src)
        ok.append(f"  ✅ syntax OK     : {rel}")
    except SyntaxError as e:
        errors.append(f"  ❌ SYNTAX ERROR  : {rel}:{e.lineno} — {e.msg}")

    # 2. TODO patch_53 residual
    for i, line in enumerate(src.splitlines(), 1):
        if "# TODO patch_53:" in line:
            errors.append(f"  ❌ TODO residual : {rel}:{i} → {line.strip()[:80]}")

    # 3. .bak ainda presente
    bak = fpath.with_suffix(fpath.suffix + ".bak")
    if bak.exists():
        warnings.append(f"  ⚠️  .bak presente : {rel}.bak  (pode remover)")

print("\n── Syntax & TODOs ──")
for m in ok:     print(m)
for m in errors: print(m)

if warnings:
    print("\n── Avisos ──")
    for m in warnings: print(m)

print("\n" + "─" * 60)
if errors:
    print(f"💥 {len(errors)} erro(s) crítico(s). Corrija antes do commit.")
    sys.exit(1)
else:
    print(f"✅ Todos os arquivos OK — zero TODOs, zero SyntaxErrors.")
    if warnings:
        print(f"ℹ️  {len(warnings)} aviso(s) não-crítico(s) (remover .bak após confirmar).")
    print("▶️  Próximo: git add -u && git commit")
