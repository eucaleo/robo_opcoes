#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
TARGET="$PROJECT_ROOT/UI/components/terminal_vwap_payoff_dark_panel.py"
MODE="${1:---dry-run}"

if [[ "$MODE" != "--dry-run" && "$MODE" != "--apply" ]]; then
  echo "Uso: bash ATT/CORRECAO_UI/scripts/patch_componentes_preco_atual.sh [--dry-run|--apply]"
  exit 2
fi

if [[ ! -f "$TARGET" ]]; then
  echo "[ERRO] Arquivo não encontrado: $TARGET"
  exit 1
fi

echo "============================================================"
echo "PATCH — COMPONENTES DA ESTRUTURA / PREÇO ATUAL DE OPÇÕES"
echo "============================================================"
echo "Projeto : $PROJECT_ROOT"
echo "Arquivo : UI/components/terminal_vwap_payoff_dark_panel.py"
echo "Modo    : $MODE"
echo

echo "---- Estado antes ----"
grep -nE \
  'columns=\("n", "symbol", "side", "type", "strike", "expiration", "qty", "premium"|\
"premium": "Prêmio"|"premium": 90|def _render_legs|_money\(leg\.get\("premium"\)\)' \
  "$TARGET" || true
echo

if [[ "$MODE" == "--dry-run" ]]; then
  echo "[OK] Dry-run concluído. Nenhum arquivo foi alterado."
  echo
  echo "Para aplicar:"
  echo "  bash ATT/CORRECAO_UI/scripts/patch_componentes_preco_atual.sh --apply"
  exit 0
fi

BACKUP="${TARGET}.bak.$(date +%Y%m%d_%H%M%S)"
cp "$TARGET" "$BACKUP"
echo "[OK] Backup criado: ${BACKUP#$PROJECT_ROOT/}"

TARGET="$TARGET" python - <<'PY'
from pathlib import Path
import os
import sys

path = Path(os.environ["TARGET"])
text = path.read_text(encoding="utf-8")

replacements = [
    (
        'columns=("n", "symbol", "side", "type", "strike", "expiration", "qty", "premium"),',
        'columns=("n", "symbol", "side", "type", "strike", "expiration", "qty", "premium", "current_price"),',
        "colunas da Treeview",
    ),
    (
        '"premium": "Prêmio",',
        '"premium": "Prêmio",\n            "current_price": "Preço atual",',
        "heading Preço atual",
    ),
    (
        '"premium": 90,',
        '"premium": 90,\n            "current_price": 100,',
        "largura Preço atual",
    ),
    (
        '                    _money(leg.get("premium")),\n                ),',
        '''                    _money(leg.get("premium")),
                    _money(
                        leg.get("current_price")
                        if leg.get("current_price") is not None
                        else leg.get("last_price")
                        if leg.get("last_price") is not None
                        else leg.get("price")
                    ),
                ),''',
        "renderização do preço atual",
    ),
]

for old, new, label in replacements:
    if new in text:
        print(f"[INFO] {label}: já aplicado.")
        continue

    count = text.count(old)
    if count != 1:
        print(
            f"[ERRO] Não foi possível aplicar '{label}': "
            f"ocorrências esperadas=1, encontradas={count}.",
            file=sys.stderr,
        )
        sys.exit(1)

    text = text.replace(old, new, 1)
    print(f"[OK] Aplicado: {label}")

path.write_text(text, encoding="utf-8")
PY

echo
echo "---- Estado depois ----"
grep -nE \
  'columns=\("n", "symbol", "side", "type", "strike", "expiration", "qty", "premium", "current_price"|\
"current_price": "Preço atual"|"current_price": 100|def _render_legs|leg\.get\("current_price"\)' \
  "$TARGET"

echo
echo "---- Validação sintática ----"
python -m py_compile "$TARGET"

echo
echo "---- Diff ----"
git diff -- UI/components/terminal_vwap_payoff_dark_panel.py

echo
echo "[OK] Patch aplicado e validado com sucesso."
echo "Backup: ${BACKUP#$PROJECT_ROOT/}"
