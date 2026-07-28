#!/usr/bin/env bash
set -euo pipefail

MODE="${1:---dry-run}"

if [[ "$MODE" != "--dry-run" && "$MODE" != "--apply" ]]; then
  echo "Uso: bash ATT/CORRECAO_UI/scripts/patch_prioridade_preco_atual.sh [--dry-run|--apply]"
  exit 2
fi

echo "============================================================"
echo "PATCH — PRIORIDADE DO PREÇO ATUAL RTD"
echo "============================================================"
echo "Modo: $MODE"
echo

python - "$MODE" <<'PY'
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil
import sys

mode = sys.argv[1]

changes = {
    Path("services/terminal_vwap_payoff_viewmodel_service.py"): (
        '''                "ultimo_preco",
                "last_price",
                "current_price",
                "price",''',
        '''                "current_price",
                "ultimo_preco",
                "last_price",
                "price",''',
        "prioridade current_price no ViewModel",
    ),
    Path("UI/components/terminal_vwap_payoff_dark_panel.py"): (
        '''                        leg.get("ultimo_preco")
                        if leg.get("ultimo_preco") is not None
                        else leg.get("last_price")
                        if leg.get("last_price") is not None
                        else leg.get("current_price")
                        if leg.get("current_price") is not None
                        else leg.get("price")''',
        '''                        leg.get("current_price")
                        if leg.get("current_price") is not None
                        else leg.get("ultimo_preco")
                        if leg.get("ultimo_preco") is not None
                        else leg.get("last_price")
                        if leg.get("last_price") is not None
                        else leg.get("price")''',
        "prioridade current_price na UI",
    ),
}

pending = []

for path, (old, new, description) in changes.items():
    if not path.exists():
        raise SystemExit(f"[ERRO] Arquivo não encontrado: {path}")

    content = path.read_text(encoding="utf-8", newline="")

    if new in content:
        print(f"[OK] Já aplicado: {path} — {description}")
        continue

    occurrences = content.count(old)
    if occurrences != 1:
        raise SystemExit(
            f"[ERRO] Âncora inválida em {path}: esperava 1 ocorrência, encontrei {occurrences}."
        )

    pending.append((path, content.replace(old, new, 1), description))

if not pending:
    print()
    print("[OK] Nenhuma alteração pendente.")
    raise SystemExit(0)

print("Alterações previstas:")
for path, _, description in pending:
    print(f"  - {path}: {description}")

if mode == "--dry-run":
    print()
    print("[OK] Dry-run concluído. Nenhum arquivo foi alterado.")
    raise SystemExit(0)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

for path, updated, description in pending:
    backup = Path(f"{path}.bak.{timestamp}")
    shutil.copy2(path, backup)
    print(f"[OK] Backup criado: {backup}")

    path.write_text(updated, encoding="utf-8", newline="")
    print(f"[OK] Atualizado: {path} — {description}")

print()
print("[OK] Patch aplicado com sucesso.")
PY
