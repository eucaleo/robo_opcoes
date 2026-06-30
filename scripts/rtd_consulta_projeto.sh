#!/usr/bin/env bash

set -u

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT" || exit 1

RUN_ID="$(date '+%Y%m%d_%H%M%S')"
OUTDIR="docs/levantamentos"
OUT="$OUTDIR/consulta_projeto_rtd_$RUN_ID.txt"

mkdir -p "$OUTDIR"

echo "Consulta tecnica: iniciando"
echo "Consulta tecnica: saida em $OUT"

{
    echo "CONSULTA DO PROJETO - RTD EXCEL VIVO"
    echo "Data: $(date '+%d/%m/%Y %H:%M:%S')"
    echo "Raiz: $ROOT"
    echo ""

    echo "1. STATUS GIT"
    echo "----------------------------------------"
    git branch --show-current 2>/dev/null || true
    echo ""
    git status --short 2>/dev/null || true
    echo ""
    git log -1 --oneline 2>/dev/null || true
    echo ""

    echo "2. DOCUMENTOS RTD EM DOCS"
    echo "----------------------------------------"
    find docs -maxdepth 3 -type f 2>/dev/null | sort || true
    echo ""

    echo "3. ARQUIVOS PRINCIPAIS DO PROJETO ATE PROFUNDIDADE 4"
    echo "----------------------------------------"
    find . -maxdepth 4 -type f \
        ! -path "./.git/*" \
        ! -path "./.venv/*" \
        ! -path "./venv/*" \
        ! -path "./node_modules/*" \
        ! -path "./__pycache__/*" \
        ! -path "./docs/levantamentos/*" \
        2>/dev/null | sort
    echo ""

    echo "4. DIRETORIOS PRINCIPAIS ATE PROFUNDIDADE 4"
    echo "----------------------------------------"
    find . -maxdepth 4 -type d \
        ! -path "./.git/*" \
        ! -path "./.venv/*" \
        ! -path "./venv/*" \
        ! -path "./node_modules/*" \
        ! -path "./__pycache__/*" \
        ! -path "./docs/levantamentos/*" \
        2>/dev/null | sort
    echo ""

    echo "5. BUSCA CONTROLADA POR TERMOS RTD, EXCEL, BANCO E SUBPROCESSOS"
    echo "----------------------------------------"
    SEARCH_FILES="$(find . -maxdepth 6 -type f \
        ! -path "./.git/*" \
        ! -path "./.venv/*" \
        ! -path "./venv/*" \
        ! -path "./node_modules/*" \
        ! -path "./__pycache__/*" \
        ! -path "./docs/levantamentos/*" \
        \( \
            -name "*.py" \
            -o -name "*.md" \
            -o -name "*.txt" \
            -o -name "*.sql" \
            -o -name "*.json" \
            -o -name "*.yaml" \
            -o -name "*.yml" \
            -o -name "*.ini" \
            -o -name "*.toml" \
            -o -name "*.sh" \
        \) \
        2>/dev/null | sort || true)"

    if [ -n "$SEARCH_FILES" ]; then
        echo "$SEARCH_FILES" | while IFS= read -r file; do
            grep -InE "RTD|LISTA_RTD|rtd_option_quotes|derived\.db|subprocess|Popen|run\(|Excel|xlwings|win32com|openpyxl|VWAP|vwap" "$file" 2>/dev/null | sed "s#^#$file:#" || true
        done
    else
        echo "Nenhum arquivo textual encontrado para busca controlada."
    fi
    echo ""

    echo "6. BUSCA POR ARQUIVOS RELACIONADOS A RTD, EXCEL E BANCO"
    echo "----------------------------------------"
    find . -maxdepth 6 -type f \
        ! -path "./.git/*" \
        ! -path "./.venv/*" \
        ! -path "./venv/*" \
        ! -path "./node_modules/*" \
        ! -path "./__pycache__/*" \
        ! -path "./docs/levantamentos/*" \
        \( \
            -iname "*rtd*" \
            -o -iname "*excel*" \
            -o -iname "*option*" \
            -o -iname "*quote*" \
            -o -iname "*derived*" \
            -o -iname "*schema*" \
            -o -iname "*database*" \
            -o -iname "*repository*" \
            -o -iname "*service*" \
        \) \
        2>/dev/null | sort
    echo ""

    echo "7. VERIFICACAO DO BANCO dados/derived.db"
    echo "----------------------------------------"
    if [ -f "dados/derived.db" ]; then
        echo "Banco encontrado: dados/derived.db"

        if command -v sqlite3 >/dev/null 2>&1; then
            echo ""
            echo "Tabelas:"
            sqlite3 dados/derived.db ".tables" 2>/dev/null || true

            echo ""
            echo "Schema completo:"
            sqlite3 dados/derived.db ".schema" 2>/dev/null || true

            echo ""
            echo "Tabelas com rtd no nome:"
            sqlite3 dados/derived.db "SELECT name FROM sqlite_master WHERE type='table' AND lower(name) LIKE '%rtd%';" 2>/dev/null || true
        else
            echo "sqlite3 nao encontrado no PATH. Schema nao inspecionado automaticamente."
        fi
    else
        echo "Banco dados/derived.db nao encontrado."
    fi
    echo ""

    echo "8. VERIFICACAO DE ARQUIVO LISTA_RTD.xlsm"
    echo "----------------------------------------"
    find . -maxdepth 6 -type f -iname "LISTA_RTD.xlsm" 2>/dev/null | sort || true
    echo ""

    echo "FIM DA CONSULTA"
} > "$OUT"

echo "Consulta tecnica concluida:"
echo "$OUT"
