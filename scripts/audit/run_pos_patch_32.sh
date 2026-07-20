#!/usr/bin/env bash
set -euo pipefail

echo "== Rodada 32.1: Auditoria pós-patch / centro de verdade =="

mkdir -p AUDITORIA_POS_PATCH_32

echo ""
echo "== Validando sintaxe dos scripts de auditoria =="
python -m py_compile scripts/audit/auditoria_pos_patch_32.py
python -m py_compile scripts/audit/test_backend_payoff_flow_32.py

echo ""
echo "== Executando auditoria cirúrgica =="
python scripts/audit/auditoria_pos_patch_32.py

echo ""
if [[ -n "${APP_DB_PATH:-}" ]]; then
    echo "== Executando teste backend sem UI =="
    python scripts/audit/test_backend_payoff_flow_32.py
else
    echo "APP_DB_PATH não definido. Pulando teste backend."
    echo "Para executar:"
    echo "APP_DB_PATH='./db/app.db' STRUCTURE_ID=2 bash scripts/audit/run_pos_patch_32.sh"
fi

echo ""
echo "== Arquivos gerados =="
find AUDITORIA_POS_PATCH_32 -maxdepth 1 -type f -print

echo ""
echo "== Finalizado =="
