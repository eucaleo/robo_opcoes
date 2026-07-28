#!/usr/bin/env bash
set -euo pipefail

MODE="${1:---dry-run}"

if [[ "$MODE" != "--dry-run" && "$MODE" != "--apply" ]]; then
  echo "Uso: bash ATT/CORRECAO_UI/scripts/patch_preco_atual_viewmodel.sh [--dry-run|--apply]"
  exit 2
fi

VM_FILE="services/terminal_vwap_payoff_viewmodel_service.py"
UI_FILE="UI/components/terminal_vwap_payoff_dark_panel.py"

for file in "$VM_FILE" "$UI_FILE"; do
  if [[ ! -f "$file" ]]; then
    echo "[ERRO] Arquivo não encontrado: $file"
    exit 1
  fi
done

echo "============================================================"
echo "PATCH — PREÇO ATUAL RTD NO VIEWMODEL E NA UI"
echo "============================================================"
echo "Modo: $MODE"
echo

python - "$MODE" "$VM_FILE" "$UI_FILE" <<'PY'
from __future__ import annotations

import shutil
import sys
from datetime import datetime
from pathlib import Path

mode = sys.argv[1]
vm_path = Path(sys.argv[2])
ui_path = Path(sys.argv[3])

vm = vm_path.read_text(encoding="utf-8")
ui = ui_path.read_text(encoding="utf-8")

vm_old = '''        strike = self._to_float(
            self._get(leg, "strike", "preco_exercicio", default=None)
        )

        return {
'''

vm_new = '''        strike = self._to_float(
            self._get(leg, "strike", "preco_exercicio", default=None)
        )

        # Preço de mercado da opção, independente do prêmio de entrada.
        # A prioridade segue o contrato RTD adotado no enrichment service.
        current_price = self._to_float(
            self._get(
                leg,
                "ultimo_preco",
                "last_price",
                "current_price",
                "price",
                default=None,
            )
        )

        return {
'''

vm_return_old = '''            "quantity": quantity,
            "premium": premium,
            "strike": strike,
'''

vm_return_new = '''            "quantity": quantity,
            "premium": premium,
            "current_price": current_price,
            "strike": strike,
'''

ui_old = '''                        leg.get("current_price")
                        if leg.get("current_price") is not None
                        else leg.get("last_price")
                        if leg.get("last_price") is not None
                        else leg.get("price")
'''

ui_new = '''                        leg.get("ultimo_preco")
                        if leg.get("ultimo_preco") is not None
                        else leg.get("last_price")
                        if leg.get("last_price") is not None
                        else leg.get("current_price")
                        if leg.get("current_price") is not None
                        else leg.get("price")
'''

changes = []

if vm_new not in vm:
    if vm_old not in vm:
        raise SystemExit(
            "[ERRO] Âncora não localizada no ViewModel para inserir current_price."
        )
    vm = vm.replace(vm_old, vm_new, 1)
    changes.append(f"{vm_path}: cálculo de current_price inserido")
else:
    print(f"[OK] Já presente: cálculo de current_price em {vm_path}")

if vm_return_new not in vm:
    if vm_return_old not in vm:
        raise SystemExit(
            "[ERRO] Âncora não localizada no retorno do ViewModel."
        )
    vm = vm.replace(vm_return_old, vm_return_new, 1)
    changes.append(f"{vm_path}: current_price exposto no payload da leg")
else:
    print(f"[OK] Já presente: current_price no retorno de {vm_path}")

if ui_new not in ui:
    if ui_old not in ui:
        raise SystemExit(
            "[ERRO] Âncora não localizada na renderização da tabela da UI."
        )
    ui = ui.replace(ui_old, ui_new, 1)
    changes.append(f"{ui_path}: fallback ultimo_preco inserido")
else:
    print(f"[OK] Já presente: fallback ultimo_preco em {ui_path}")

if not changes:
    print("\n[OK] Nenhuma alteração necessária.")
    raise SystemExit(0)

print("\nAlterações previstas:")
for change in changes:
    print(f"  - {change}")

if mode == "--dry-run":
    print("\n[OK] Dry-run concluído. Nenhum arquivo foi alterado.")
    raise SystemExit(0)

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
for path, content in ((vm_path, vm), (ui_path, ui)):
    backup = path.with_name(f"{path.name}.bak.{stamp}")
    shutil.copy2(path, backup)
    path.write_text(content, encoding="utf-8")
    print(f"[OK] Backup criado: {backup}")
    print(f"[OK] Atualizado: {path}")

print("\n[OK] Patch aplicado com sucesso.")
PY
