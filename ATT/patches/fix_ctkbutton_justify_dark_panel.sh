#!/usr/bin/env bash
set -euo pipefail

file="UI/components/terminal_vwap_payoff_dark_panel.py"

if [ ! -f "$file" ]; then
    echo "[ERRO] Arquivo não encontrado: $file"
    exit 1
fi

stamp="$(date +%Y%m%d_%H%M%S)"
cp "$file" "${file}.bak_fix_justify_${stamp}"
echo "[OK] Backup criado: ${file}.bak_fix_justify_${stamp}"

python - <<'PY'
from pathlib import Path

path = Path("UI/components/terminal_vwap_payoff_dark_panel.py")
text = path.read_text(encoding="utf-8")

# CTkButton não suporta justify. Removemos o argumento.
text = text.replace('                justify="left",\n', '')
text = text.replace('            justify="left",\n', '')
text = text.replace('        justify="left",\n', '')

path.write_text(text, encoding="utf-8")

print("[OK] Argumentos justify removidos.")
PY

python -m py_compile UI/components/terminal_vwap_payoff_dark_panel.py
python -m py_compile UI/main_window.py

echo
echo "[OK] Correção aplicada."
echo "[INFO] Rode agora:"
echo "python run_ui.py"
