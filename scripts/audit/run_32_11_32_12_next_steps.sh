#!/usr/bin/env bash
set -euo pipefail

echo "== Rodada 32.11: Quarentena do script paralelo de payoff =="

python -m py_compile \
  scripts/audit/audit_32_11_quarantine_parallel_payoff_scripts.py \
  scripts/audit/apply_patch_32_11_quarantine_parallel_payoff_scripts.py \
  scripts/audit/audit_32_12_ui_local_payoff_scope.py

echo ""
echo "== Auditoria antes do patch 32.11 =="
python scripts/audit/audit_32_11_quarantine_parallel_payoff_scripts.py

echo ""
echo "== Aplicando patch 32.11 =="
python scripts/audit/apply_patch_32_11_quarantine_parallel_payoff_scripts.py

echo ""
echo "== Auditoria depois do patch 32.11 =="
python scripts/audit/audit_32_11_quarantine_parallel_payoff_scripts.py

echo ""
echo "== Rodada 32.12: Auditoria UI para calculo local/fallback =="
python scripts/audit/audit_32_12_ui_local_payoff_scope.py

echo ""
echo "== Validando relatorios sem crase ASCII 96 =="
python - <<'PY'
from pathlib import Path

base = Path("AUDITORIA_POS_PATCH_32")
files = [
    base / "RELATORIO_32_11_AUDIT_QUARANTINE_PARALLEL_PAYOFF_SCRIPTS.md",
    base / "RELATORIO_32_11_PATCH_QUARANTINE_PARALLEL_PAYOFF_SCRIPTS.md",
    base / "RELATORIO_32_12_AUDIT_UI_LOCAL_PAYOFF_SCOPE.md",
]

failed = []
for path in files:
    if path.exists() and "`" in path.read_text(encoding="utf-8", errors="replace"):
        failed.append(str(path))

if failed:
    raise SystemExit("ERRO: relatorios com crase ASCII 96: " + ", ".join(failed))

print("OK: relatorios MD sem crase ASCII 96.")
PY

echo ""
echo "== Arquivos gerados =="
ls -1 AUDITORIA_POS_PATCH_32/RELATORIO_32_11_* AUDITORIA_POS_PATCH_32/RELATORIO_32_12_* 2>/dev/null || true

echo ""
echo "== Git status =="
git status --short

echo ""
echo "== Finalizado =="
