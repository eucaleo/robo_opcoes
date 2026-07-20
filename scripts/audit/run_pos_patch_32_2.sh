#!/usr/bin/env bash
set -euo pipefail

echo "== Rodada 32.2: Diagnóstico do gap de persistência de payoff =="

echo
echo "== Validando sintaxe =="
python -m py_compile scripts/audit/diagnose_payoff_persistence_gap_32_2.py

echo
echo "== Executando diagnóstico =="
python scripts/audit/diagnose_payoff_persistence_gap_32_2.py

echo
echo "== Arquivos gerados =="
find AUDITORIA_POS_PATCH_32 -maxdepth 1 -type f | sort

echo
echo "== Finalizado =="
