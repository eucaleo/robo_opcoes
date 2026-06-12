#!/usr/bin/env bash
set -euo pipefail

echo "[INFO] Patch Fase 9 - criacao atomica de estrutura com legs"

python scripts/apply_fase9_atomic_create.py

echo "[INFO] Rodando py_compile"

python -m py_compile \
  repositories/structures_repository.py \
  UI/components/structure_editor_dialog.py

echo "[OK] py_compile passou."

echo "[INFO] Rodando testes curtos"

python -m pytest \
  ATT/tests/test_structures_repository.py \
  ATT/tests/test_structure_editor_dialog.py \
  ATT/tests/test_structure_editor_integration.py

echo "[OK] Patch Fase 9 aplicado e validado."
