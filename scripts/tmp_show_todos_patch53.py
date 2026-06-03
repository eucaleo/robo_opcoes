"""
tmp_show_todos_patch53.py — exibe contexto completo dos TODOs patch_53
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

TODO_FILES = [
    "db/derived_repo.py",
    "UI/models/ui_data.py",
    "UI/components/decisions_grid.py",
    "UI/components/payoff_chart.py",
    "repositories/market_snapshot_repository.py",
    "domain/payoff_features.py",
    "utils/leg_normalizers.py",
]

CONTEXT = 6  # linhas antes e depois do TODO

for rel in TODO_FILES:
    fpath = ROOT / rel
    if not fpath.exists():
        print(f"\n❌ NÃO ENCONTRADO: {rel}")
        continue

    lines = fpath.read_text(encoding="utf-8").splitlines()
    todos = [i for i, l in enumerate(lines) if "# TODO patch_53:" in l]

    if not todos:
        print(f"\n✅ Sem TODOs: {rel}")
        continue

    print(f"\n{'='*70}")
    print(f"📄 {rel}  ({len(todos)} TODO(s))")
    print(f"{'='*70}")

    for idx in todos:
        start = max(0, idx - CONTEXT)
        end   = min(len(lines), idx + CONTEXT + 1)
        print(f"\n  ── TODO na linha {idx+1} ──")
        for i in range(start, end):
            marker = ">>>" if i == idx else "   "
            print(f"  {marker} {i+1:>4} │ {lines[i]}")

print(f"\n{'='*70}")
print(f"✅ Relatório concluído — cole o output acima para análise.")
