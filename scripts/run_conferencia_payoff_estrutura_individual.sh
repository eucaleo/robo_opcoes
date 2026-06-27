#!/usr/bin/env bash
set -u

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT_DIR" || exit 1

echo "== Conferencia Payoff por Estrutura Individual =="
echo "Diretorio: $ROOT_DIR"
echo "Branch: $(git branch --show-current 2>/dev/null)"
echo "Commit: $(git rev-parse --short HEAD 2>/dev/null)"
echo ""

echo "== 1. Py compile dos scripts de conferencia =="
python -m py_compile scripts/conferir_db_payoff_estrutura.py
PY_STATUS=$?
if [ "$PY_STATUS" -ne 0 ]; then
    echo "FALHA no py_compile"
    exit "$PY_STATUS"
fi

echo ""
echo "== 2. Buscas Git/Grep =="
bash scripts/conferir_payoff_buscas_git.sh

echo ""
echo "== 3. Conferencia DB =="
if [ -f "dados/app.db" ]; then
    python scripts/conferir_db_payoff_estrutura.py dados/app.db
else
    echo "AVISO: dados/app.db nao encontrado. Pulando conferencia DB."
fi

echo ""
echo "== 4. Status Git =="
git status --short

echo ""
echo "Conferencia concluida."
echo "Relatorios em: reports/payoff_conferencia"
