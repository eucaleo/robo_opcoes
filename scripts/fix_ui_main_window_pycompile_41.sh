#!/usr/bin/env bash
set -u -o pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

OUT="FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/CORRECAO_PYCOMPILE_UI_41"
mkdir -p "$OUT"

echo "==> correcao 41 - reparar erro de sintaxe em UI/main_window.py"
echo "Data local: $(date)" | tee "$OUT/00_inicio.txt"
echo "Diretorio raiz: $ROOT" | tee -a "$OUT/00_inicio.txt"

echo
echo "==> status git inicial"
git status --short | tee "$OUT/01_status_git_inicial.txt"

if command -v python >/dev/null 2>&1; then
  PYTHON_CMD=(python)
elif command -v py >/dev/null 2>&1; then
  PYTHON_CMD=(py -3)
else
  echo "FALHA: python nao encontrado no PATH." | tee "$OUT/99_resultado.txt"
  exit 1
fi

APPLY_RC=0

"${PYTHON_CMD[@]}" - <<'PY' > "$OUT/02_aplicacao_correcao_41.txt" 2>&1 || APPLY_RC=$?
from pathlib import Path
import sys

target = Path("UI/main_window.py")
out_dir = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/CORRECAO_PYCOMPILE_UI_41")

if not target.exists():
    print(f"FALHA: arquivo nao encontrado: {target}")
    sys.exit(1)

text = target.read_text(encoding="utf-8")
backup = out_dir / "UI_main_window.py.bak_antes_correcao_41"
backup.write_text(text, encoding="utf-8")

lines = text.splitlines(keepends=True)

start = None
for idx, line in enumerate(lines):
    if line.startswith("def _blocked_ui_external_process_call(*args, **kwargs):"):
        start = idx
        break

if start is None:
    print("INFO: bloco _blocked_ui_external_process_call nao encontrado no ponto quebrado.")
    print("Nenhuma alteracao aplicada.")
    sys.exit(0)

context_before = "".join(lines[max(0, start - 12):start])

if "from controllers.terminal_vwap_payoff_controller import (" not in context_before:
    print("FALHA: bloco encontrado, mas nao esta imediatamente dentro do import quebrado esperado.")
    print("Por seguranca, nenhuma alteracao foi aplicada.")
    sys.exit(2)

end = None
for idx in range(start + 1, min(len(lines), start + 100)):
    if "TerminalVWAPPayoffController" in lines[idx]:
        end = idx
        break

if end is None:
    print("FALHA: nao foi possivel localizar TerminalVWAPPayoffController apos o bloco quebrado.")
    print("Por seguranca, nenhuma alteracao foi aplicada.")
    sys.exit(3)

removed = "".join(lines[start:end])
(out_dir / "03_bloco_removido_41.txt").write_text(removed, encoding="utf-8")

new_text = "".join(lines[:start] + lines[end:])
target.write_text(new_text, encoding="utf-8")

print("OK: bloco inserido indevidamente dentro do import foi removido.")
print("OK: backup salvo em:", backup)
print("OK: bloco removido salvo em:", out_dir / "03_bloco_removido_41.txt")
PY

echo
echo "==> resultado da aplicacao"
cat "$OUT/02_aplicacao_correcao_41.txt"

echo
echo "==> executando py_compile em UI/main_window.py"
PYCOMPILE_RC=0
"${PYTHON_CMD[@]}" -m py_compile UI/main_window.py > "$OUT/04_py_compile_UI_main_window.txt" 2>&1 || PYCOMPILE_RC=$?

if [ "$PYCOMPILE_RC" -eq 0 ]; then
  echo "OK: py_compile passou em UI/main_window.py"
else
  echo "FALHA: py_compile ainda falhou em UI/main_window.py"
  cat "$OUT/04_py_compile_UI_main_window.txt"
fi

echo
echo "==> registrando diff sem stage"
git diff -- UI/main_window.py > "$OUT/05_diff_UI_main_window.txt"
git status --short > "$OUT/06_status_git_final.txt"

echo
echo "==> status git final"
cat "$OUT/06_status_git_final.txt"

echo
echo "==> conclusao"
if [ "$APPLY_RC" -eq 0 ] && [ "$PYCOMPILE_RC" -eq 0 ]; then
  {
    echo "RESULTADO: OK"
    echo
    echo "UI/main_window.py corrigido quanto ao erro de sintaxe."
    echo "Nenhum git add, commit ou push foi executado."
    echo
    echo "Proximo passo sugerido:"
    echo "bash scripts/verify_pycompile_contexto_40.sh"
    echo "bash scripts/verify_pycompile_detalhado_39.sh"
    echo "bash scripts/verify_aplicacao_correcao_38.sh"
  } | tee "$OUT/99_resultado.txt"
  exit 0
else
  {
    echo "RESULTADO: FALHA"
    echo
    echo "A correcao automatica nao fechou completamente."
    echo "Abrir arquivos em:"
    echo "$OUT"
    echo
    echo "Principal:"
    echo "$OUT/04_py_compile_UI_main_window.txt"
    echo "$OUT/05_diff_UI_main_window.txt"
    echo
    echo "Nao executar git add, commit ou push."
  } | tee "$OUT/99_resultado.txt"
  exit 1
fi
