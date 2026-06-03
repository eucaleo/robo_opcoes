"""
tmp_fix_todos_patch53b.py — TEMPORÁRIO (remover após patch_53b)
Corrige TODOs malformados e remove marcadores onde não cabe conversão.
"""
import re
import shutil
from pathlib import Path

ROOT     = Path(__file__).parent.parent
DRY_RUN  = False  # altere para True para simular

# ------------------------------------------------------------------
# Correções cirúrgicas por arquivo
# Cada entrada: (arquivo, lista de (linha_1based, conteúdo_novo))
# ------------------------------------------------------------------

FIXES: dict[str, list[tuple[int, str]]] = {

    # ── db/derived_repo.py ────────────────────────────────────────
    # TODO estava DENTRO do .get() → SyntaxError
    "db/derived_repo.py": [
        (228,
         '        ab  = aba        or decision_dict.get("aba")          '
         'or decision_dict.get("ticker", "unknown")\n'),
        (298,
         '        ab = aba       or (meta or {}).get("aba")             '
         'or "unknown"\n'),
        (342,
         '        ab = aba       or (meta or {}).get("aba")             '
         'or "unknown"\n'),
    ],

    # ── UI/models/ui_data.py ──────────────────────────────────────
    "UI/models/ui_data.py": [
        # linha 277 — sintaxe quebrada: TODO dentro do .get()
        (277,
         '                aba_src = c.get("aba")  '
         '# patch_53b: aba é coluna TEXT do banco; StructureRef é criado na camada de serviço\n'),
        # linha 323 — sintaxe quebrada: TODO dentro do .get()
        (323,
         '            aba_filter = filters.get("aba")  '
         '# patch_53b: filtro por aba TEXT — compat legado\n'),
        # linha 358 — TODO dentro do .get() (parte do if)
        (358,
         '            if item.get("structure_id") is None and item.get("aba") is not None:\n'),
        # linha 361 — TODO dentro do int()
        (361,
         '                    item["structure_id"] = int(item["aba"])\n'),
        # linha 365 — TODO dentro do .get() (segundo if)
        (365,
         '            if item.get("aba") is None and item.get("structure_id") is not None:\n'),
        # linha 366 — TODO virou assignment quebrado: item["aba"]  # TODO = ...
        (366,
         '                item["aba"] = str(item["structure_id"])\n'),
    ],

    # ── UI/components/decisions_grid.py ───────────────────────────
    "UI/components/decisions_grid.py": [
        (111,
         '                decision.get("structure_id") or decision.get("aba") or "N/A"\n'),
        (204,
         '            row_sid = row.get("structure_id") or row.get("aba")\n'),
    ],

    # ── UI/components/payoff_chart.py ─────────────────────────────
    "UI/components/payoff_chart.py": [
        (310,
         '                or decision_data.get("aba", "")\n'),
        (419,
         '                or decision_data.get("aba", "")\n'),
    ],

    # ── repositories/market_snapshot_repository.py ────────────────
    "repositories/market_snapshot_repository.py": [
        (138,
         '        aba             = row["aba"],\n'),
    ],

    # ── domain/payoff_features.py ─────────────────────────────────
    "domain/payoff_features.py": [
        (222,
         '                "aba":               features.get("aba"),\n'),
    ],

    # ── utils/leg_normalizers.py ──────────────────────────────────
    "utils/leg_normalizers.py": [
        (159,
         "            'aba': str(data.get('aba', '')).strip(),\n"),
    ],
}

# ------------------------------------------------------------------
results = []
for rel, changes in FIXES.items():
    fpath = ROOT / rel
    if not fpath.exists():
        results.append(f"❌ NÃO ENCONTRADO: {rel}")
        continue

    lines = fpath.read_text(encoding="utf-8").splitlines(keepends=True)
    touched = []

    for lineno, new_content in changes:
        idx = lineno - 1
        if idx >= len(lines):
            results.append(f"⚠️  {rel}:{lineno} — linha fora do range")
            continue
        old = lines[idx]
        if old == new_content:
            results.append(f"  ✅ {rel}:{lineno} — já correto (sem alteração)")
            continue
        lines[idx] = new_content
        touched.append(lineno)

    if touched:
        results.append(f"\n📄 {rel}")
        for ln in touched:
            results.append(f"  ✏️  linha {ln} corrigida")
        if not DRY_RUN:
            shutil.copy2(fpath, fpath.with_suffix(fpath.suffix + ".bak"))
            fpath.write_text("".join(lines), encoding="utf-8")
            results.append(f"  💾 salvo (.bak criado)")
        else:
            results.append(f"  🔍 DRY-RUN — não salvo")

for r in results:
    print(r)

print("\n" + "─"*60)
if DRY_RUN:
    print("🔍 DRY-RUN concluído — nenhum arquivo alterado.")
else:
    print("✅ Correções aplicadas.")
    print("▶️  Próximo: python scripts/tmp_verify_patch53b.py")
