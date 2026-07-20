#!/usr/bin/env bash
set -u

echo "== Rodada 32.13: Bloqueio do calculo local de payoff na UI =="

echo
echo "== Auditoria antes do patch 32.13 =="
python scripts/audit/audit_32_13_ui_local_payoff_blocked.py || true

echo
echo "== Aplicando patch 32.13 =="
python scripts/audit/apply_patch_32_13_block_ui_local_payoff_calculation.py

echo
echo "== Auditoria depois do patch 32.13 =="
python scripts/audit/audit_32_13_ui_local_payoff_blocked.py || true

echo
echo "== Validando relatorios MD sem crase ASCII 96 =="
python - <<'PY'
from pathlib import Path

root = Path("AUDITORIA_POS_PATCH_32")
bad = []

for path in root.glob("RELATORIO_32_13_*.md"):
    text = path.read_text(encoding="utf-8", errors="replace")
    if "`" in text:
        bad.append(str(path))

if bad:
    print("ERRO: crase ASCII 96 encontrada em:")
    for item in bad:
        print(item)
    raise SystemExit(1)

print("OK: relatorios MD sem crase ASCII 96.")
PY

echo
echo "== Arquivos gerados =="
ls -1 AUDITORIA_POS_PATCH_32/RELATORIO_32_13_* 2>/dev/null || true

echo
echo "== Git status =="
git status --short

echo
echo "== Finalizado =="
