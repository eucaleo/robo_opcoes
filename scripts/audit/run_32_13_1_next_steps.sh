#!/usr/bin/env bash
set -u

echo "== Rodada 32.13.1: corrigir sintaxe do bloqueio local de payoff na UI =="
echo

echo "== Auditoria antes do patch 32.13.1 =="
python scripts/audit/audit_32_13_1_ui_syntax_and_local_payoff_block.py
AUDIT_BEFORE_STATUS=$?
echo

echo "== Aplicando patch 32.13.1 =="
python scripts/audit/apply_patch_32_13_1_fix_ui_local_payoff_block_syntax.py
PATCH_STATUS=$?
echo

echo "== Auditoria depois do patch 32.13.1 =="
python scripts/audit/audit_32_13_1_ui_syntax_and_local_payoff_block.py
AUDIT_AFTER_STATUS=$?
echo

echo "== Validando compilacao Python do arquivo UI =="
python -m py_compile UI/components/terminal_vwap_payoff_dark_panel.py
PYCOMPILE_STATUS=$?
echo

echo "== Validando relatorios MD sem crase ASCII 96 =="
python - <<'PY'
from pathlib import Path

base = Path("AUDITORIA_POS_PATCH_32")
bad = []

for path in base.glob("RELATORIO_32_13_1_*.md"):
    text = path.read_text(encoding="utf-8", errors="replace")
    if "`" in text:
        bad.append(str(path))

if bad:
    print("ERRO: relatorios com crase ASCII 96:")
    for item in bad:
        print(item)
    raise SystemExit(1)

print("OK: relatorios MD sem crase ASCII 96.")
PY
MD_STATUS=$?
echo

echo "== Arquivos gerados =="
ls -1 AUDITORIA_POS_PATCH_32/RELATORIO_32_13_1_* 2>/dev/null || true
echo

echo "== Git status =="
git status --short
echo

if [ "$PATCH_STATUS" -eq 0 ] && [ "$AUDIT_AFTER_STATUS" -eq 0 ] && [ "$PYCOMPILE_STATUS" -eq 0 ] && [ "$MD_STATUS" -eq 0 ]; then
  echo "== Finalizado com sucesso =="
  exit 0
fi

echo "== Finalizado com pendencias =="
echo "PATCH_STATUS=$PATCH_STATUS"
echo "AUDIT_AFTER_STATUS=$AUDIT_AFTER_STATUS"
echo "PYCOMPILE_STATUS=$PYCOMPILE_STATUS"
echo "MD_STATUS=$MD_STATUS"
exit 1
