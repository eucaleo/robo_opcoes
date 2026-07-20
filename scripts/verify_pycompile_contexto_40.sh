#!/usr/bin/env bash

set -u

echo
echo "==> verificacao 40 - contexto detalhado do erro de sintaxe em UI/main_window.py"
echo

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT_DIR" || exit 1

OUT_DIR="FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/VERIFICACAO_PYCOMPILE_CONTEXTO_40"
mkdir -p "$OUT_DIR"

RAW_FILE="$OUT_DIR/01_py_compile_UI_main_window_raw.txt"
CTX_FILE="$OUT_DIR/02_contexto_linha_erro_UI_main_window.txt"
DIFF_FILE="$OUT_DIR/03_diff_UI_main_window.txt"
STATUS_FILE="$OUT_DIR/04_status_git.txt"
SUMMARY_FILE="$OUT_DIR/05_resumo_operacional.txt"

TARGET="UI/main_window.py"

echo "Data local: $(date)" | tee "$SUMMARY_FILE"
echo "Diretorio raiz: $ROOT_DIR" | tee -a "$SUMMARY_FILE"
echo "Arquivo alvo: $TARGET" | tee -a "$SUMMARY_FILE"
echo | tee -a "$SUMMARY_FILE"

echo "==> status git inicial"
git status --short | tee "$STATUS_FILE"
echo

if [ ! -f "$TARGET" ]; then
    echo "FALHA: arquivo nao encontrado: $TARGET" | tee -a "$SUMMARY_FILE"
    echo
    echo "EXIT_CODE=1"
    read -r -p "Pressione ENTER para fechar..."
    exit 1
fi

echo "==> executando py_compile em $TARGET"
python -m py_compile "$TARGET" > "$RAW_FILE" 2>&1
PY_EXIT=$?

cat "$RAW_FILE"
echo

ERROR_LINE="$(
python - <<'PY' "$RAW_FILE" "$TARGET"
import re
import sys

raw_path = sys.argv[1]
target = sys.argv[2].replace("\\", "/")

text = open(raw_path, "r", encoding="utf-8", errors="replace").read()

matches = re.findall(r'File "([^"]+)", line ([0-9]+)', text)

line = ""
for path, num in matches:
    norm = path.replace("\\", "/")
    if norm.endswith(target):
        line = num

if not line and matches:
    line = matches[-1][1]

print(line)
PY
)"

{
    echo "==> contexto do erro em $TARGET"
    echo
    echo "Linha detectada: ${ERROR_LINE:-NAO_DETECTADA}"
    echo
} > "$CTX_FILE"

if [ -n "${ERROR_LINE:-}" ]; then
    START=$((ERROR_LINE - 35))
    END=$((ERROR_LINE + 35))

    if [ "$START" -lt 1 ]; then
        START=1
    fi

    {
        echo "==> linhas $START a $END de $TARGET"
        echo
        nl -ba "$TARGET" | sed -n "${START},${END}p"
    } >> "$CTX_FILE"
else
    {
        echo "Nao foi possivel detectar automaticamente a linha."
        echo
        echo "Primeiras 260 linhas para inspecao manual:"
        echo
        nl -ba "$TARGET" | sed -n '1,260p'
    } >> "$CTX_FILE"
fi

echo "==> salvando diff atual de $TARGET"
git diff -- "$TARGET" > "$DIFF_FILE" 2>&1

echo
echo "==> contexto salvo em:"
echo "$CTX_FILE"
echo

echo "==> exibindo contexto principal"
cat "$CTX_FILE"
echo

echo "==> resumo operacional" | tee -a "$SUMMARY_FILE"

if [ "$PY_EXIT" -eq 0 ]; then
    {
        echo "RESULTADO: OK"
        echo
        echo "O arquivo $TARGET passou no py_compile."
        echo "Agora rode novamente o verificador de aplicacao da correcao."
        echo
        echo "Sugestao:"
        echo "bash scripts/verify_aplicacao_correcao_38.sh"
        echo
        echo "IMPORTANTE: este script nao executou git add, commit ou push."
    } | tee -a "$SUMMARY_FILE"
else
    {
        echo "RESULTADO: FALHA"
        echo
        echo "O arquivo $TARGET ainda possui erro de sintaxe."
        echo
        echo "Abra estes arquivos:"
        echo "$RAW_FILE"
        echo "$CTX_FILE"
        echo "$DIFF_FILE"
        echo
        echo "Corrija primeiro a linha indicada no contexto."
        echo "Depois rode novamente:"
        echo "bash scripts/verify_pycompile_contexto_40.sh"
        echo
        echo "IMPORTANTE: nao executar git add, commit ou push ainda."
    } | tee -a "$SUMMARY_FILE"
fi

echo
echo "==> arquivos gerados em:"
echo "$OUT_DIR"
echo

echo "EXIT_CODE=$PY_EXIT"
read -r -p "Pressione ENTER para fechar..."
exit "$PY_EXIT"
