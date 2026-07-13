#!/usr/bin/env bash
set -u

ROOT="$(pwd)"
OUT_DIR="FRENTE_RTD_EXCEL_BTG_ONLINE/output"
TS="$(date +%Y%m%d_%H%M%S)"
AUDIT="${OUT_DIR}/25_PRECHECK_FASE4_CANDLES_${TS}.txt"

mkdir -p "$OUT_DIR"

TMP_AUDIT="$(mktemp)"
trap 'rm -f "$TMP_AUDIT"' EXIT

safe_find_files() {
    find . \
        -path "./.git" -prune -o \
        -path "./.venv" -prune -o \
        -path "./venv" -prune -o \
        -path "./__pycache__" -prune -o \
        -path "./FRENTE_RTD_EXCEL_BTG_ONLINE/output" -prune -o \
        -type f "$@" \
        -print 2>/dev/null | sort
}

safe_grep() {
    local pattern="$1"
    grep -RInE \
        --exclude-dir=".git" \
        --exclude-dir=".venv" \
        --exclude-dir="venv" \
        --exclude-dir="__pycache__" \
        --exclude-dir="output" \
        --exclude="25_PRECHECK_FASE4_CANDLES_*.txt" \
        --exclude="precheck_fase4_candles.sh" \
        "$pattern" . 2>/dev/null || true
}

{
    echo "===== PRECHECK FASE 4 CANDLES ====="
    date
    echo "ROOT=${ROOT}"
    echo "AUDIT=${AUDIT}"
    echo

    echo "===== GIT ====="
    git branch --show-current 2>/dev/null || true
    git status --short 2>/dev/null || true
    git log --oneline -10 2>/dev/null || true
    echo

    echo "===== ARQUIVOS DOCUMENTAIS DA FRENTE ====="
    find FRENTE_RTD_EXCEL_BTG_ONLINE \
        -path "FRENTE_RTD_EXCEL_BTG_ONLINE/output" -prune -o \
        -type f \
        \( -iname "*.md" -o -iname "*.txt" \) \
        -print 2>/dev/null | sort
    echo

    echo "===== BUSCA DOCUMENTAL DE FASES ====="
    safe_grep "Fase 3|Fase 4|Historico intraday|Histórico intraday|Motor de candles|candles|VWAP"
    echo

    echo "===== ARQUIVOS CANDIDATOS DE CÓDIGO ====="
    safe_find_files \( \
        -iname "*candle*.py" -o \
        -iname "*candles*.py" -o \
        -iname "*intraday*.py" -o \
        -iname "*rtd_option_quotes*.py" \
    \)
    echo

    echo "===== ARQUIVOS CANDIDATOS DE TESTE ====="
    find ATT/tests \
        -type f \
        \( -iname "*candle*" -o -iname "*candles*" -o -iname "*intraday*" -o -iname "*rtd_option_quotes*" -o -iname "test_*.py" \) \
        -print 2>/dev/null | sort
    echo

    echo "===== BUSCA EM CÓDIGO: CANDLES / INTRADAY ====="
    safe_grep "candle|candles|intraday|ohlc|open|high|low|close|vwap|volume"
    echo

    echo "===== BUSCA DE SUBPROCESS / EXCEL / RTD ====="
    safe_grep "subprocess|win32com|Dispatch|Excel.Application|RTD|LISTA_RTD|rtd_option_quotes"
    echo

    echo "===== SQLITE: TABELAS ====="
    DB="dados/app.db"
    if [ -f "$DB" ] && command -v sqlite3 >/dev/null 2>&1; then
        sqlite3 "$DB" ".tables" 2>/dev/null || true
    else
        echo "sqlite3 indisponivel ou banco dados/app.db nao encontrado."
    fi
    echo

    echo "===== SQLITE: SCHEMA HISTORICO INTRADAY ====="
    if [ -f "$DB" ] && command -v sqlite3 >/dev/null 2>&1; then
        sqlite3 "$DB" ".schema rtd_option_quotes_intraday_history" 2>/dev/null || true
    else
        echo "sqlite3 indisponivel ou banco dados/app.db nao encontrado."
    fi
    echo

    echo "===== SQLITE: SCHEMA CANDLES ====="
    if [ -f "$DB" ] && command -v sqlite3 >/dev/null 2>&1; then
        sqlite3 "$DB" ".schema rtd_option_quotes_intraday_candles" 2>/dev/null || true
        sqlite3 "$DB" ".schema intraday_candles" 2>/dev/null || true
    else
        echo "sqlite3 indisponivel ou banco dados/app.db nao encontrado."
    fi
    echo

    echo "===== CHECAGEM DE ARTEFATOS FORA DAS PASTAS OFICIAIS ====="
    find . \
        -path "./.git" -prune -o \
        -path "./.venv" -prune -o \
        -path "./venv" -prune -o \
        -path "./__pycache__" -prune -o \
        -path "./FRENTE_RTD_EXCEL_BTG_ONLINE/output" -prune -o \
        -type f \( \
            -iname "*precheck*" -o \
            -iname "*check*" -o \
            -iname "*patch*" -o \
            -iname "*temp*" -o \
            -iname "*tmp*" -o \
            -iname "*auditoria*" \
        \) \
        ! -path "./FRENTE_RTD_EXCEL_BTG_ONLINE/*" \
        ! -path "./ATT/tests/*" \
        ! -path "./ATT/patches/*" \
        -print 2>/dev/null | sort
    echo

    echo "===== FIM PRECHECK FASE 4 CANDLES ====="
} > "$TMP_AUDIT"

mv "$TMP_AUDIT" "$AUDIT"
trap - EXIT

echo "OK: auditoria gerada em $AUDIT"
